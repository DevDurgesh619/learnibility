"""Cambridge International AS Level Physics 9702, AS topics 1-11 (grade 11).

CUP Coursebook (3rd ed.) chapters 1-15 plus AS practical skills (Paper 3):
1 Physical quantities and units, 2 Kinematics, 3 Accelerated motion, 4 Dynamics, 5 Momentum,
6 Forces and equilibrium, 7 Density and pressure, 8 Work, energy and power, 9 Deformation of solids,
10 Waves, 11 Superposition, 12 Electricity, 13 D.C. circuits, 14 Particle physics, 15 Practical skills.

One Topic per W2 subtopic (name = subtopic name). Fixed C1 lists are Paper 1 style MCQs (auto-paired
into two-part recall items); fixed C2 lists are short explanations with mark points; parameterised
templates carry Paper 2 calculations and Paper 3 data/uncertainty work and scale with D; compose()
builds Paper 2 structured items with "[n]" part marks. Data as on 9702 papers: g = 9.81 m s⁻²,
e = 1.60 × 10⁻¹⁹ C, c = 3.00 × 10⁸ m s⁻¹, units written in the m s⁻¹ style.
"""
import math
import re
import unicodedata
from ._lib import topic, mcq, relation, sf, sci, sup, person, two_people, city, num_mcq, near
from .g9_physics import cap, neg, Q, compose, FX, numq
from decimal import Decimal, ROUND_HALF_UP

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
GR = 9.81
QE = 1.60e-19
C0 = 3.00e8


def nf(x, n=3):
    """Number for display in 9702 style.

    ints print as they are; a float whose shortest form has at most n significant figures (given data
    or an exact result) is padded to at least min(2, n) s.f. (0.8 -> 0.80, 3.0 -> 3.0); otherwise it is
    rounded half-up to n s.f. keeping trailing zeros (2.6999 -> 2.70)."""
    if isinstance(x, int):
        return str(x) if abs(x) < 10000 else f'{x:,}'.replace(',', ' ')
    if x == 0:
        return '0'
    d0 = Decimal(repr(float(x)))
    sig = len(d0.normalize().as_tuple().digits)
    keep = max(sig, min(2, n)) if sig <= n else n
    e = d0.adjusted()
    q = Decimal(1).scaleb(e - keep + 1)
    v = d0.quantize(q, rounding=ROUND_HALF_UP)
    if v.adjusted() > e:  # rounding carried into a new digit (9.99 -> 10.0)
        v = v.quantize(Decimal(1).scaleb(e - keep + 2), rounding=ROUND_HALF_UP)
    if v == v.to_integral_value() and abs(v) >= 1 and v.as_tuple().exponent >= 0:
        iv = int(v)
        return str(iv) if abs(iv) < 10000 else f'{iv:,}'.replace(',', ' ')
    out = f'{v:f}'
    return out


def E(x, n=3):
    """Display a number: plain for 0.001 <= |x| < 100 000, otherwise standard form."""
    if x == 0:
        return '0'
    if 1e-3 <= abs(x) < 1e5:
        return nf(x, n)
    return sci(x, n)


def f3(x):
    return E(x, 3)


def f2(x):
    return E(x, 2)


def deg(x):
    return f'{x:.0f}°' if abs(x - round(x)) < 1e-9 else f'{x:.1f}°'


def lab(r):
    return r.choice([f'a school laboratory in {city(r)}', f'a college physics laboratory in {city(r)}', f'a practical class in {city(r)}', f'an AS Physics lesson in {city(r)}'])


def pickf(r, frames, **kw):
    return r.choice(frames).format(p=person(r), c=city(r), **kw)


# ===================================================================== 1 Physical quantities and units
N11 = 'SI base units, derived units and homogeneity of equations'
t11 = topic(N11, N11.lower(), 'si base units', 'homogeneity')
FX(t11, 'C1', (1, 2), [
    ('Which list contains only SI base quantities?', 'mass, length, time, temperature', 'The SI base quantities are mass, length, time, current, temperature and amount of substance.',
     ['mass, weight, time, temperature', 'length, time, charge, current', 'mass, length, force, time']),
    ('Which unit is an SI base unit?', 'ampere', 'The ampere (current) is a base unit; coulomb, volt and newton are derived.', ['coulomb', 'volt', 'newton']),
    ('What is the newton expressed in SI base units?', 'kg m s⁻²', 'F = ma, so N = kg × m s⁻² = kg m s⁻².', ['kg m s⁻¹', 'kg m² s⁻²', 'kg s⁻²']),
    ('What is the joule expressed in SI base units?', 'kg m² s⁻²', 'W = Fs: (kg m s⁻²)(m) = kg m² s⁻².', ['kg m s⁻²', 'kg m² s⁻³', 'kg m⁻¹ s⁻²']),
    ('What is the watt expressed in SI base units?', 'kg m² s⁻³', 'P = W/t: kg m² s⁻² ÷ s = kg m² s⁻³.', ['kg m² s⁻²', 'kg m s⁻³', 'kg m² s⁻¹']),
    ('What is the pascal expressed in SI base units?', 'kg m⁻¹ s⁻²', 'p = F/A: kg m s⁻² ÷ m² = kg m⁻¹ s⁻².', ['kg m s⁻²', 'kg m⁻² s⁻²', 'kg m² s⁻²']),
    ('Which quantity is NOT an SI base quantity?', 'electric charge', 'Charge is derived: Q = It, unit A s.', ['electric current', 'thermodynamic temperature', 'amount of substance']),
    ('What is the coulomb expressed in SI base units?', 'A s', 'Q = It, so C = A s.', ['A s⁻¹', 'A⁻¹ s', 'kg A s']),
    ('What is the volt expressed in SI base units?', 'kg m² s⁻³ A⁻¹', 'V = P/I: kg m² s⁻³ ÷ A.', ['kg m² s⁻² A⁻¹', 'kg m² s⁻³ A', 'kg m s⁻³ A⁻¹']),
    ('What is the ohm expressed in SI base units?', 'kg m² s⁻³ A⁻²', 'R = V/I: kg m² s⁻³ A⁻¹ ÷ A.', ['kg m² s⁻³ A⁻¹', 'kg m² s⁻² A⁻²', 'kg m s⁻³ A⁻²']),
    ('State what is meant by a homogeneous equation.', 'An equation in which every term has the same base units.', 'each term (both sides) has the same base units [1]'),
    ('State the six SI base quantities.', 'mass, length, time, electric current, thermodynamic temperature and amount of substance.', 'all six correct [2]; four or five correct [1] [2]'),
])
FX(t11, 'C2', (1, 2, 3, 4), [
    ('Explain why an equation that is homogeneous may still be physically incorrect.', 'Homogeneity only checks the units; the equation may have a missing or wrong pure number (such as ½ or 2π), or a missing dimensionless term, which units cannot reveal.', 'units the same does not check numerical constants [1]; example such as ½ or 2π or missing term [1] [2]'),
    ('Show that the equation s = ut + ½at² is homogeneous.', 's: m; ut: (m s⁻¹)(s) = m; ½at²: (m s⁻²)(s²) = m. Every term has units of m, so it is homogeneous (½ has no unit).', 'units of ut = m [1]; units of at² = m and conclusion [1] [2]'),
    ('Show that the equation v² = u² + 2as is homogeneous.', 'v² and u²: m² s⁻²; as: (m s⁻²)(m) = m² s⁻². All terms have the same base units.', 'v², u² in m² s⁻² [1]; 2as in m² s⁻² and conclusion [1] [2]'),
    ('Explain the difference between a base quantity and a derived quantity, giving one example of each.', 'A base quantity is one of the six chosen independent quantities (e.g. mass, unit kg); a derived quantity is defined in terms of base quantities (e.g. speed = distance/time, unit m s⁻¹).', 'base: fundamental/independent with example [1]; derived: defined from base quantities with example [1] [2]'),
    ('Explain why the kilogram and the second are called base units but the newton is not.', 'The kilogram and second are defined independently; the newton is defined from them through F = ma (1 N = 1 kg m s⁻²), so it is a derived unit.', 'kg and s defined independently [1]; N derived from F = ma as kg m s⁻² [1] [2]'),
    ('A student claims that kinetic energy could be given by E = mv. Use base units to show that this is impossible.', 'mv has base units kg m s⁻¹, but energy has base units kg m² s⁻², so the equation is not homogeneous.', 'units of mv = kg m s⁻¹ [1]; energy kg m² s⁻², not equal so wrong [1] [2]'),
    ('Show that the equation T = 2π√(l/g) for a pendulum is homogeneous.', 'l/g has units m ÷ m s⁻² = s², so √(l/g) has units s, the same as T; 2π has no units.', 'l/g gives s² [1]; square root gives s, same as T [1] [2]'),
])
EQS = [  # (equation text, constant, base units of constant, working)
    ('the drag force F on a car moving at speed v is F = kv²', 'k', 'kg m⁻¹', 'k = F/v² = kg m s⁻² ÷ m² s⁻²', ['kg m s⁻¹', 'kg m⁻² s', 'kg s⁻¹']),
    ('the viscous force F on a sphere of radius r moving at speed v through a fluid is F = 6πηrv', 'η', 'kg m⁻¹ s⁻¹', 'η = F/(6πrv) = kg m s⁻² ÷ (m × m s⁻¹)', ['kg m s⁻¹', 'kg m⁻² s⁻¹', 'kg m⁻¹ s⁻²']),
    ('the force F needed to stretch a spring by extension x is F = kx', 'k', 'kg s⁻²', 'k = F/x = kg m s⁻² ÷ m', ['kg m s⁻²', 'kg m² s⁻²', 'kg m⁻¹ s⁻²']),
    ('the power P radiated by a surface of area A at thermodynamic temperature T is P = σAT⁴', 'σ', 'kg s⁻³ K⁻⁴', 'σ = P/(AT⁴) = kg m² s⁻³ ÷ (m² K⁴)', ['kg m² s⁻³ K⁻⁴', 'kg s⁻² K⁻⁴', 'kg m⁻² s⁻³ K⁻⁴']),
    ('the energy E of a photon of frequency f is E = hf', 'h', 'kg m² s⁻¹', 'h = E/f = kg m² s⁻² ÷ s⁻¹', ['kg m² s⁻³', 'kg m s⁻¹', 'kg m² s']),
    ('the gravitational force between masses M and m a distance r apart is F = GMm/r²', 'G', 'kg⁻¹ m³ s⁻²', 'G = Fr²/(Mm) = kg m s⁻² × m² ÷ kg²', ['kg m³ s⁻²', 'kg⁻² m³ s⁻²', 'kg⁻¹ m² s⁻²']),
    ('the speed v of a wave on a string of tension T and mass per unit length μ is v = √(T/μ)', 'μ', 'kg m⁻¹', 'μ = T/v² = kg m s⁻² ÷ m² s⁻²', ['kg m', 'kg m⁻² s', 'kg s⁻²']),
    ('the rate of thermal energy flow Q/t through a slab of area A and thickness x with temperature difference ΔT is Q/t = kAΔT/x', 'k', 'kg m s⁻³ K⁻¹', 'k = (Q/t)x/(AΔT) = kg m² s⁻³ × m ÷ (m² K)', ['kg m² s⁻³ K⁻¹', 'kg m s⁻² K⁻¹', 'kg m⁻¹ s⁻³ K⁻¹']),
    ('the resistance R of a wire of length L and cross-sectional area A is R = ρL/A', 'ρ', 'kg m³ s⁻³ A⁻²', 'ρ = RA/L = kg m² s⁻³ A⁻² × m² ÷ m', ['kg m² s⁻³ A⁻²', 'kg m³ s⁻³ A⁻¹', 'kg m s⁻³ A⁻²']),
    ('the pressure p exerted by a fluid of density ρ flowing at speed v against a wall is p = Cρv²', 'C', 'no units (it is dimensionless)', 'ρv² = kg m⁻³ × m² s⁻² = kg m⁻¹ s⁻², same as pressure', ['kg m⁻¹', 'm s⁻¹', 'kg m⁻³']),
    ('the frequency f of oscillation of a mass m on a spring of stiffness k is f = C√(k/m)', 'C', 'no units (it is dimensionless)', 'k/m = kg s⁻² ÷ kg = s⁻², √ gives s⁻¹, same as f', ['s', 'kg s⁻¹', 's⁻¹']),
    ('the volume flow rate V/t of a liquid through a pipe of radius r and length l with pressure difference p is V/t = πpr⁴/(8ηl)', 'η', 'kg m⁻¹ s⁻¹', 'η = πpr⁴/(8l × V/t) = kg m⁻¹ s⁻² × m⁴ ÷ (m × m³ s⁻¹)', ['kg m s⁻¹', 'kg m⁻¹ s⁻²', 'kg m⁻² s⁻¹']),
]


@t11.add('C1', (1, 2, 3))
def t11_const(r, D):
    eq, k, ans, wk, wrong = r.choice(EQS)
    if D <= 2:
        opts, a = mcq(r, ans, wrong)
        return Q(f'In a model, {eq}. What are the SI base units of {k}?', a, f'{wk} = {ans}.', opts=opts)
    return Q(f'In a model, {eq}. Determine the SI base units of {k}.', ans, f'rearrange for {k} [1]; {wk} = {ans} [1] [2]', 'short')


@t11.add('C3', (2, 3, 4, 5), 'numerical')
def t11_derive(r, D):
    eq, k, ans, wk, _ = r.choice(EQS)
    lead = r.choice(['A physicist proposes that', 'A textbook states that', 'In an engineering model,', 'A student reads that'])
    if D <= 3:
        return Q(f'{lead} {eq}. Determine the SI base units of {k}. Show your working.', ans, f'base units of each other quantity identified [1]; rearrangement {wk} [1]; {ans} [1] [3]')
    return Q(f'{lead} {eq}. (a) Determine the SI base units of {k}. (b) Explain why finding these units does not show that the equation is correct.', f'(a) {ans} (b) Units cannot check pure numbers (e.g. 6π, ½) or missing dimensionless factors; only experiment can confirm the equation.',
             f'(a) base units of other quantities [1]; {wk} [1]; {ans} [1] (b) numerical constants not tested by units [1] [4]', 'multi_step')


HOMO = [('P = Fv (power = force × velocity)', True, 'Fv: kg m s⁻² × m s⁻¹ = kg m² s⁻³ = W'),
        ('E = ½mv² (kinetic energy)', True, '½mv²: kg × m² s⁻² = kg m² s⁻² = J'),
        ('p = ρgh (pressure in a liquid)', True, 'ρgh: kg m⁻³ × m s⁻² × m = kg m⁻¹ s⁻² = Pa'),
        ('E = mgh² (potential energy)', False, 'mgh²: kg × m s⁻² × m² = kg m³ s⁻², but energy is kg m² s⁻²'),
        ('v = fλ² (wave speed)', False, 'fλ²: s⁻¹ × m² = m² s⁻¹, but speed is m s⁻¹'),
        ('F = mv/t (force from momentum change)', True, 'mv/t: kg × m s⁻¹ ÷ s = kg m s⁻²'),
        ('p = F/A² (pressure)', False, 'F/A²: kg m s⁻² ÷ m⁴ = kg m⁻³ s⁻², but pressure is kg m⁻¹ s⁻²'),
        ('W = pΔV (work done by a gas)', True, 'pΔV: kg m⁻¹ s⁻² × m³ = kg m² s⁻² = J'),
        ('I = nAvq (current in a conductor)', True, 'nAvq: m⁻³ × m² × m s⁻¹ × A s = A'),
        ('s = ut + at² (displacement)', True, 'ut and at² both have units m, so the equation is homogeneous even though the factor ½ is missing'),
        ('a = v²r (centripetal acceleration)', False, 'v²r: m² s⁻² × m = m³ s⁻², but acceleration is m s⁻²'),
        ('E = Fs/t (energy)', False, 'Fs/t: kg m² s⁻³ (a power), but energy is kg m² s⁻²')]


@t11.add('C2', (2, 3, 4), 'explain')
def t11_homo(r, D):
    eq, ok, wk = r.choice(HOMO)
    who = person(r)
    lead = r.choice([f'{who} writes the equation', f'A revision sheet in {city(r)} quotes', f'{who} is checking the equation'])
    extra = ' If it is homogeneous, state whether this proves it is correct.' if D >= 3 else ''
    ans = f'{"Homogeneous" if ok else "Not homogeneous"}: {wk}.' + (' Homogeneity does not prove it is correct: numerical factors are not checked.' if (ok and D >= 3) else '')
    return Q(f'{lead} {eq}. Use SI base units to determine whether the equation is homogeneous.{extra}', ans,
             f'base units of each side found [1]; correct conclusion [1]' + (' ; comment that homogeneity cannot check numerical constants [1] [3]' if D >= 3 else ' [2]'))


def _units_c4(r, D):
    eq, k, ans, wk, _ = r.choice(EQS)
    who = person(r)
    intro = r.choice([f'{who} is researching a formula used by engineers in {city(r)}: {eq}.', f'A data booklet states that {eq}.', f'During a project, {who} finds that {eq}.'])
    parts = [
        lambda r: ('State the difference between a base unit and a derived unit.', 'Base units are the defined SI units (kg, m, s, A, K, mol); derived units are combinations of base units.', 'base units listed/independent [1]; derived from combinations [1] [2]'),
        lambda r: (f'Determine the SI base units of {k}.', ans, f'{wk} [1]; = {ans} [1] [2]'),
        lambda r: ('Explain why the equation must be homogeneous if it is correct.', 'Quantities can only be equated or added if they are the same kind of quantity, so every term must have the same base units.', 'only like quantities can be equal/added [1]; same base units each term [1] [2]'),
        lambda r: ('Suggest why a homogeneous equation may still be wrong.', 'It may have the wrong dimensionless constant or a missing dimensionless term.', 'dimensionless constants not tested [1]'),
        lambda r: ('State the SI base units of force and of energy.', 'force kg m s⁻²; energy kg m² s⁻²', 'force [1]; energy [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t11.add('C4', (2, 3, 4, 5), 'multi_step')(_units_c4)

N12 = 'Prefixes, standard form and estimating physical quantities'
t12 = topic(N12, N12.lower(), 'prefixes', 'estimating physical quantities')
PRE = [('p', 'pico', -12), ('n', 'nano', -9), ('µ', 'micro', -6), ('m', 'milli', -3), ('c', 'centi', -2), ('d', 'deci', -1), ('k', 'kilo', 3), ('M', 'mega', 6), ('G', 'giga', 9), ('T', 'tera', 12)]
FX(t12, 'C1', (1, 2), [
    ('What is the value of the prefix pico (p)?', '10⁻¹²', 'pico = 10⁻¹².', ['10⁻⁹', '10⁻¹⁵', '10⁻⁶']),
    ('What is the value of the prefix tera (T)?', '10¹²', 'tera = 10¹².', ['10⁹', '10¹⁵', '10⁶']),
    ('Which is the best estimate of the mass of an adult person?', '70 kg', 'A typical adult has a mass of about 60–80 kg.', ['7 kg', '700 kg', '7000 kg']),
    ('Which is the best estimate of the wavelength of visible light?', '5 × 10⁻⁷ m', 'Visible light: 400–700 nm, about 5 × 10⁻⁷ m.', ['5 × 10⁻⁴ m', '5 × 10⁻¹⁰ m', '5 × 10⁻¹² m']),
    ('Which is the best estimate of the diameter of an atom?', '10⁻¹⁰ m', 'Atoms are about 0.1 nm = 10⁻¹⁰ m across.', ['10⁻¹⁵ m', '10⁻⁶ m', '10⁻⁸ m']),
    ('Which is the best estimate of the speed of a sprinter?', '10 m s⁻¹', '100 m in about 10 s.', ['1 m s⁻¹', '40 m s⁻¹', '100 m s⁻¹']),
    ('Which is the best estimate of the power of a domestic kettle?', '2 kW', 'Kettles are typically 2–3 kW.', ['20 W', '200 kW', '2 MW']),
    ('Which is the best estimate of the volume of air in a classroom?', '200 m³', 'About 10 m × 8 m × 3 m ≈ 240 m³.', ['2 m³', '20 000 m³', '20 m³']),
    ('Which is the best estimate of the diameter of a nucleus?', '10⁻¹⁴ m', 'Nuclear diameters are about 10⁻¹⁵–10⁻¹⁴ m.', ['10⁻¹⁰ m', '10⁻⁸ m', '10⁻²⁰ m']),
    ('Which is the best estimate of the weight of an apple?', '1 N', 'An apple has mass about 0.1 kg, weight ≈ 1 N.', ['0.01 N', '10 N', '100 N']),
    ('State the value of the prefix micro (µ).', '10⁻⁶', 'micro = 10⁻⁶ [1]'),
    ('State the value of the prefix giga (G).', '10⁹', 'giga = 10⁹ [1]'),
])
FX(t12, 'C2', (1, 2, 3), [
    ('Explain why a physicist would write 0.000 000 52 m as 520 nm or 5.2 × 10⁻⁷ m.', 'Prefixes and standard form make very small or large numbers easier to read and compare, reduce copying errors and show the number of significant figures clearly.', 'easier to read/compare [1]; shows significant figures / fewer errors [1] [2]'),
    ('Explain why the conversion from cm² to m² involves dividing by 10⁴ and not by 100.', '1 m = 100 cm, so 1 m² = (100 cm)² = 10⁴ cm²; the prefix factor is squared because area has two length dimensions.', '(100)² [1]; prefix squared for area [1] [2]'),
    ('Estimate the kinetic energy of a car travelling on a motorway, stating the values you use.', 'm ≈ 1000 kg, v ≈ 30 m s⁻¹; E = ½mv² ≈ ½ × 1000 × 900 ≈ 5 × 10⁵ J.', 'sensible m and v [1]; E ≈ 10⁵–10⁶ J [1] [2]'),
    ('Estimate the pressure exerted on the floor by a person standing on both feet, stating your estimates.', 'Weight ≈ 700 N; area of two feet ≈ 2 × 0.025 m² = 0.05 m²; p ≈ 700/0.05 ≈ 1.4 × 10⁴ Pa.', 'sensible weight and area [1]; p ≈ 10⁴ Pa [1] [2]'),
    ('Estimate the energy needed to climb a flight of stairs in a house, stating your estimates.', 'm ≈ 60 kg, height ≈ 3 m; E = mgh ≈ 60 × 9.81 × 3 ≈ 1.8 × 10³ J.', 'sensible m and h [1]; E ≈ 2 kJ [1] [2]'),
    ('Explain why 1 mm³ is equal to 10⁻⁹ m³.', '1 mm = 10⁻³ m, so 1 mm³ = (10⁻³ m)³ = 10⁻⁹ m³.', 'prefix value 10⁻³ [1]; cubed for volume [1] [2]'),
])
CONV = [('a capacitor of', 4.7, 'µF', 'F', -6), ('a wavelength of', 589, 'nm', 'm', -9), ('a resistance of', 3.3, 'MΩ', 'Ω', 6), ('a frequency of', 2.4, 'GHz', 'Hz', 9), ('a current of', 25, 'mA', 'A', -3),
        ('a power output of', 1.8, 'GW', 'W', 9), ('a time interval of', 450, 'ps', 's', -12), ('a distance of', 6.4, 'Mm', 'm', 6), ('a charge of', 12, 'nC', 'C', -9), ('an energy of', 7.5, 'TJ', 'J', 12),
        ('a wire diameter of', 0.38, 'mm', 'm', -3), ('a pressure of', 101, 'kPa', 'Pa', 3)]


@t12.add('C3', (1, 2, 3), 'numerical')
def t12_conv(r, D):
    what, v, u, base, e = r.choice(CONV)
    v = v * r.choice([1, 2, 3, 0.5, 1.5])
    val = v * 10 ** e
    if D <= 1:
        opts, a = num_mcq(r, val, [v * 10 ** (e + 3), v * 10 ** (e - 3), v * 10 ** (e + 1)], fmtf=lambda x: sci(x, 2), unit=' ' + base)
        return Q(f'A component has {what} {nf(v)} {u}. What is this in {base}?', a, f'{u[:-len(base)] or u} = 10{sup(e)}; {nf(v)} × 10{sup(e)} = {sci(val, 2)} {base}.', opts=opts)
    if D == 2:
        return Q(f'Express {what} {nf(v)} {u} in {base}, in standard form.', f'{sci(val, 2)} {base}', f'prefix = 10{sup(e)} [1]; {sci(val, 2)} {base} [1] [2]', 'short')
    sq = r.choice([('area', 2, 'mm²', 'm²', -6, 'mm'), ('volume', 3, 'cm³', 'm³', -6, 'cm'), ('area', 2, 'cm²', 'm²', -4, 'cm'), ('volume', 3, 'mm³', 'm³', -9, 'mm')])
    x = r.choice([0.25, 0.50, 1.2, 2.5, 3.8, 45, 120, 7.9])
    return Q(f'The cross-sectional {sq[0]} of a component is quoted as {nf(x)} {sq[2]}. Convert this to {sq[3]}, explaining your conversion factor.', f'{sci(x * 10 ** sq[4], 2)} {sq[3]}',
             f'1 {sq[5]} = 10{sup(-2 if sq[5] == "cm" else -3)} m [1]; factor raised to power {sq[1]} = 10{sup(sq[4])} [1]; {sci(x * 10 ** sq[4], 2)} {sq[3]} [1] [3]')


EST = [('the mass of a full 1 litre bottle of water', 1, 'kg', [0.01, 100, 10000]), ('the height of a door', 2, 'm', [0.2, 20, 200]),
       ('the time for a heartbeat', 1, 's', [0.01, 10, 100]), ('the density of air', 1.2, 'kg m⁻³', [0.012, 120, 1200]),
       ('the mass of a car', 1000, 'kg', [10, 100000, 10000000]), ('the thickness of a sheet of paper', 1e-4, 'm', [1e-7, 1e-2, 1e-6]),
       ('the current in a torch bulb', 0.3, 'A', [0.0003, 30, 300]), ('the speed of sound in air', 330, 'm s⁻¹', [3.3, 33000, 3.3e6]),
       ('the wavelength of a radio wave from an FM station', 3, 'm', [3e-4, 3e3, 3e-7]), ('the mass of an electron', 9.1e-31, 'kg', [9.1e-28, 1.7e-27, 9.1e-34]),
       ('the power of a filament lamp used in a house', 60, 'W', [0.6, 6000, 600000]), ('atmospheric pressure at sea level', 1e5, 'Pa', [1e2, 1e3, 1e8])]


@t12.add('C1', (1, 2, 3))
def t12_est(r, D):
    what, v, u, w = r.choice(EST)
    fm = lambda x: (f'{x:g}' if 1e-3 <= x < 1e5 else sci(x, 2).replace('.0 ×', ' ×').replace('1.0 × ', '').replace('10 × ', ''))
    c = fm(v) + ' ' + u
    opts, a = mcq(r, c, [fm(x) + ' ' + u for x in w])
    if D >= 3:
        return Q(f'Which is the best estimate of {what}? Give a brief justification.', c, f'order of magnitude {c} [1]; justification from everyday knowledge [1] [2]', 'short')
    return Q(f'Which is the best estimate of {what}?', a, f'Order of magnitude: {c}.', opts=opts)


ESTC = [
    ('the kinetic energy of a sprinter running at full speed', 'm ≈ 70 kg, v ≈ 10 m s⁻¹', 0.5 * 70 * 100, 'J', 'E = ½mv²'),
    ('the weight of a bag of sugar', 'm ≈ 1 kg', 1 * GR, 'N', 'W = mg'),
    ('the gravitational potential energy gained by a student climbing to the top floor of a three-storey building', 'm ≈ 60 kg, h ≈ 9 m', 60 * GR * 9, 'J', 'ΔE = mgh'),
    ('the momentum of a cyclist', 'm ≈ 80 kg (with bicycle), v ≈ 5 m s⁻¹', 80 * 5, 'kg m s⁻¹', 'p = mv'),
    ('the power of a student running up a 3 m flight of stairs in 3 s', 'm ≈ 60 kg, h ≈ 3 m, t ≈ 3 s', 60 * GR * 3 / 3, 'W', 'P = mgh/t'),
    ('the mass of air in a room 5 m × 4 m × 3 m', 'ρ ≈ 1.2 kg m⁻³, V = 60 m³', 1.2 * 60, 'kg', 'm = ρV'),
    ('the pressure on the ground under an elephant standing on four feet', 'm ≈ 5000 kg, area of each foot ≈ 0.1 m²', 5000 * GR / 0.4, 'Pa', 'p = F/A'),
    ('the number of heartbeats in a lifetime', '70 beats per minute for 75 years', 70 * 60 * 24 * 365 * 75, '', 'number = rate × time'),
]


@t12.add('C3', (2, 3, 4), 'numerical')
def t12_estcalc(r, D):
    what, vals, v, u, eq = r.choice(ESTC)
    ans = f'about {E(v, 1)} {u}'.strip()
    lead = r.choice(['Estimate', 'Make a reasoned estimate of', 'By making suitable estimates, determine the order of magnitude of'])
    return Q(f'{lead} {what}. State the values you use.', ans + f' (using {vals})', f'sensible estimates ({vals}) [1]; {eq} applied [1]; answer within an order of magnitude of {E(v, 1)} {u} [1] [3]')


def _pre_c4(r, D):
    lam = r.choice([450, 520, 589, 633, 680])
    f = C0 / (lam * 1e-9)
    d = r.choice([0.20, 0.25, 0.32, 0.45])
    A = math.pi * (d * 1e-3) ** 2 / 4
    intro = r.choice([f'A laser in {lab(r)} emits light of wavelength {lam} nm. It is used to measure a wire of diameter {nf(d)} mm.',
                      f'{person(r)} is writing a report on an optical experiment using light of wavelength {lam} nm and a wire of diameter {nf(d)} mm.'])
    parts = [
        lambda r: ('Express the wavelength in metres in standard form.', f'{sci(lam * 1e-9, 3)} m', f'nm = 10⁻⁹ [1]'),
        lambda r: ('Calculate the frequency of the light (c = 3.00 × 10⁸ m s⁻¹).', f'{sci(f, 3)} Hz', f'f = c/λ = 3.00 × 10⁸ / {sci(lam * 1e-9, 3)} [2]'),
        lambda r: ('Calculate the cross-sectional area of the wire in m².', f'{sci(A, 3)} m²', f'A = πd²/4 with d = {sci(d * 1e-3, 2)} m [2]'),
        lambda r: ('State the frequency using a suitable prefix.', f'{nf(f / 1e12, 3)} THz', 'THz = 10¹² Hz [1]'),
        lambda r: ('Estimate how many wavelengths of the light would fit across the diameter of the wire.', f'about {nf(d * 1e-3 / (lam * 1e-9), 2)}', f'{sci(d * 1e-3, 2)} / {sci(lam * 1e-9, 3)} [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12.add('C4', (2, 3, 4, 5), 'multi_step')(_pre_c4)

N13 = 'Errors and uncertainties: systematic and random, precision and accuracy and combining uncertainties'
t13 = topic(N13, N13.lower(), 'errors and uncertainties', 'combining uncertainties')
FX(t13, 'C1', (1, 2), [
    ('Which describes a systematic error?', 'An error that makes every reading too large (or too small) by the same amount or proportion', 'Systematic errors shift all readings in the same direction, e.g. a zero error; repeating does not remove them.',
     ['An error that makes readings scatter randomly about the true value', 'An error caused only by a mistake in arithmetic', 'An error that is removed by averaging many readings']),
    ('A set of readings is close together but all far from the true value. The readings are', 'precise but not accurate', 'Precise: small spread; accurate: close to the true value.', ['accurate but not precise', 'both accurate and precise', 'neither accurate nor precise']),
    ('Which error can be reduced by taking repeat readings and averaging?', 'Random error', 'Averaging reduces random scatter; it does not affect systematic error.', ['Zero error', 'Systematic error', 'Calibration error']),
    ('A micrometer screw gauge reads 0.02 mm when its jaws are closed. This is an example of', 'a zero error, which is systematic', 'A non-zero reading with nothing measured is a zero error and shifts every reading.', ['a random error', 'a parallax error, which is random', 'a reading error that averaging removes']),
    ('A length is 25.0 ± 0.5 cm. What is its percentage uncertainty?', '2%', '0.5/25.0 × 100 = 2%.', ['0.5%', '5%', '0.02%']),
    ('A quantity is calculated from x = a × b. How are the uncertainties combined?', 'The percentage uncertainties of a and b are added', 'For products and quotients, add fractional (percentage) uncertainties.', ['The absolute uncertainties of a and b are added', 'The percentage uncertainties are multiplied', 'The larger percentage uncertainty is used alone']),
    ('A quantity is calculated from y = a − b. How is the uncertainty in y found?', 'The absolute uncertainties of a and b are added', 'For sums and differences, add absolute uncertainties.', ['The absolute uncertainties are subtracted', 'The percentage uncertainties are added', 'The percentage uncertainties are subtracted']),
    ('The percentage uncertainty in the diameter of a wire is 2%. What is the percentage uncertainty in its cross-sectional area?', '4%', 'A ∝ d², so % uncertainty doubles: 2 × 2% = 4%.', ['2%', '1%', '8%']),
    ('State what is meant by the precision of a measurement.', 'How close repeated readings are to each other (small spread / scatter).', 'closeness of repeated readings to each other [1]'),
    ('State what is meant by the accuracy of a measurement.', 'How close a measurement is to the true value.', 'closeness to the true value [1]'),
])
FX(t13, 'C2', (1, 2, 3, 4), [
    ('Explain the difference between a systematic error and a random error, giving an example of each.', 'A systematic error shifts all readings the same way (e.g. a zero error on a meter); a random error causes readings to scatter unpredictably about the mean (e.g. reaction time when using a stopwatch).', 'systematic: same direction/size with example [1]; random: scatter with example [1] [2]'),
    ('Explain why taking repeat readings does not reduce a systematic error.', 'Every reading is shifted by the same amount in the same direction, so the mean is shifted too; the error must be found and corrected (e.g. by subtracting a zero error or recalibrating).', 'all readings shifted equally / mean also shifted [1]; must correct the instrument or reading [1] [2]'),
    ('A student measures the period of a pendulum by timing 20 oscillations. Explain why this reduces the percentage uncertainty in the period.', 'The absolute uncertainty in the timing (reaction time) is about the same whatever the total time, so dividing by 20 makes the uncertainty in one period 20 times smaller; the percentage uncertainty is reduced.', 'uncertainty in total time roughly constant [1]; divided over 20 periods / larger time gives smaller percentage [1] [2]'),
    ('Explain why a quantity that depends on d² has a percentage uncertainty twice that of d.', 'd² = d × d; for a product the percentage uncertainties add, so % in d² = % in d + % in d = 2 × % in d.', 'product rule: percentages add [1]; d × d gives 2 × % [1] [2]'),
    ('Explain why an ammeter with a zero error can give precise but inaccurate readings.', 'The readings may be close together (small random scatter, so precise), but each is shifted from the true value by the zero error (so not accurate).', 'precise: small scatter [1]; inaccurate: shifted by zero error [1] [2]'),
    ('A digital stopwatch reads to 0.01 s. Explain why the uncertainty in a hand-timed interval is larger than 0.01 s.', 'Human reaction time at starting and stopping (about 0.1–0.2 s) is much larger than the resolution of the watch, so it dominates the uncertainty.', 'reaction time [1]; much larger than 0.01 s resolution [1] [2]'),
])


def _pct(x, dx):
    return 100 * dx / x


@t13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_combine(r, D):
    kind = r.choice(['rho_cyl', 'pend', 'res', 'sphere', 'speed'])
    if kind == 'pend':
        l = r.choice([0.500, 0.650, 0.800, 0.950, 1.200]); dl = 0.002
        n = 20; T = 2 * math.pi * math.sqrt(l / GR); tt = round(n * T, 1); dt = r.choice([0.2, 0.3, 0.4])
        Tm = tt / n; gv = 4 * math.pi ** 2 * l / Tm ** 2
        pc = _pct(l, dl) + 2 * _pct(tt, dt)
        setup = f'The acceleration of free fall is found from g = 4π²l/T². A student measures l = {l:.3f} ± {dl:.3f} m and the time for {n} oscillations as {tt:.1f} ± {dt:.1f} s.'
        if D <= 2:
            return numq(r, D, setup, 'percentage uncertainty in g', pc, '%', f'%g = %l + 2 × %t = {nf(_pct(l, dl), 2)}% + 2 × {nf(_pct(tt, dt), 2)}%', [_pct(l, dl) + _pct(tt, dt), 2 * _pct(l, dl) + _pct(tt, dt), _pct(tt, dt)], fm=lambda x: nf(x, 2))
        return Q(setup + ' Calculate g and its absolute uncertainty.', f'g = {nf(gv, 3)} ± {nf(gv * pc / 100, 1)} m s⁻²',
                 f'T = {tt:.1f}/{n} = {nf(Tm, 4)} s [1]; g = {nf(gv, 3)} m s⁻² [1]; %g = {nf(_pct(l, dl), 2)} + 2 × {nf(_pct(tt, dt), 2)} = {nf(pc, 2)}% [1]; Δg = {nf(gv * pc / 100, 1)} m s⁻² [1] [4]')
    if kind == 'rho_cyl':
        m = r.choice([24.6, 38.2, 52.8, 61.5, 77.0]); dm = 0.1
        d = r.choice([1.50, 1.80, 2.00, 2.20, 2.50]); dd = 0.01
        L = r.choice([3.20, 4.00, 4.50, 5.10, 6.00]); dL = 0.05
        rho = m / (math.pi * d ** 2 / 4 * L)
        pc = _pct(m, dm) + 2 * _pct(d, dd) + _pct(L, dL)
        setup = f'A metal cylinder has mass {m} ± {dm} g, diameter {d:.2f} ± {dd:.2f} cm and length {L:.2f} ± {dL:.2f} cm. Its density is ρ = 4m/(πd²L).'
        if D <= 2:
            return numq(r, D, setup, 'percentage uncertainty in ρ', pc, '%', f'%ρ = %m + 2%d + %L = {nf(_pct(m, dm), 2)} + 2 × {nf(_pct(d, dd), 2)} + {nf(_pct(L, dL), 2)}', [_pct(m, dm) + _pct(d, dd) + _pct(L, dL), 2 * pc, _pct(d, dd)], fm=lambda x: nf(x, 2))
        return Q(setup + ' Calculate the density in g cm⁻³ and its absolute uncertainty.', f'ρ = {nf(rho, 3)} ± {nf(rho * pc / 100, 1)} g cm⁻³',
                 f'ρ = 4 × {m}/(π × {d:.2f}² × {L:.2f}) = {nf(rho, 3)} g cm⁻³ [1]; % = {nf(_pct(m, dm), 2)} + {nf(2 * _pct(d, dd), 2)} + {nf(_pct(L, dL), 2)} = {nf(pc, 2)}% [2]; Δρ = {nf(rho * pc / 100, 1)} g cm⁻³ [1] [4]')
    if kind == 'res':
        V = r.choice([2.40, 3.60, 4.50, 5.20, 6.00]); dV = 0.05
        I = r.choice([0.120, 0.250, 0.320, 0.480]); dI = 0.005
        R = V / I; pc = _pct(V, dV) + _pct(I, dI)
        setup = f'The p.d. across a resistor is {V:.2f} ± {dV:.2f} V and the current is {I:.3f} ± {dI:.3f} A.'
        if D <= 2:
            return numq(r, D, setup, 'percentage uncertainty in the resistance', pc, '%', f'%R = %V + %I = {nf(_pct(V, dV), 2)} + {nf(_pct(I, dI), 2)}', [abs(_pct(I, dI) - _pct(V, dV)) or 0.3, _pct(I, dI), _pct(V, dV) * _pct(I, dI)], fm=lambda x: nf(x, 2))
        return Q(setup + ' Calculate the resistance and its absolute uncertainty, giving both to an appropriate number of significant figures.', f'R = {nf(R, 2 if R * pc / 100 >= 1 else 3)} ± {nf(R * pc / 100, 1)} Ω',
                 f'R = V/I = {nf(R, 4)} Ω [1]; %R = {nf(_pct(V, dV), 2)} + {nf(_pct(I, dI), 2)} = {nf(pc, 2)}% [1]; ΔR = {nf(R * pc / 100, 1)} Ω [1]; R quoted to same decimal place as ΔR [1] [4]')
    if kind == 'sphere':
        d = r.choice([12.0, 15.5, 18.2, 20.0, 24.6]); dd = 0.1
        V = math.pi * d ** 3 / 6; pc = 3 * _pct(d, dd)
        setup = f'The diameter of a ball bearing is measured as {d:.1f} ± {dd:.1f} mm.'
        if D <= 2:
            return numq(r, D, setup, 'percentage uncertainty in its volume', pc, '%', f'V ∝ d³, so %V = 3 × {nf(_pct(d, dd), 2)}%', [_pct(d, dd), 2 * _pct(d, dd), _pct(d, dd) ** 3], fm=lambda x: nf(x, 2))
        return Q(setup + ' Calculate its volume in mm³ and the absolute uncertainty in the volume.', f'V = {nf(V, 3)} ± {nf(V * pc / 100, 1)} mm³',
                 f'V = πd³/6 = {nf(V, 4)} mm³ [1]; %V = 3 × {nf(_pct(d, dd), 2)}% = {nf(pc, 2)}% [1]; ΔV = {nf(V * pc / 100, 1)} mm³ [1] [3]')
    x1 = r.choice([12.4, 15.6, 18.0, 22.5]); x2 = x1 + r.choice([36.2, 48.4, 52.0, 61.8]); dx = 0.1
    t = r.choice([2.45, 3.10, 3.62, 4.08]); dt = r.choice([0.05, 0.10])
    s = x2 - x1; v = s / t / 100; pc = _pct(s, 2 * dx) + _pct(t, dt)
    setup = f'A trolley passes a mark at {x1:.1f} ± {dx:.1f} cm and a second mark at {x2:.1f} ± {dx:.1f} cm, taking {t:.2f} ± {dt:.2f} s.'
    if D <= 2:
        return numq(r, D, setup, 'absolute uncertainty in the distance between the marks', 2 * dx, ' cm', f'difference: add absolute uncertainties = {dx} + {dx}', [dx, 0.05, 0.4], fm=lambda x: nf(x, 2))
    return Q(setup + ' Calculate the average speed in m s⁻¹ and its percentage uncertainty.', f'v = {nf(v, 3)} m s⁻¹ ± {nf(pc, 2)}%',
             f's = {nf(s, 3)} ± {nf(2 * dx, 1)} cm (absolute uncertainties add) [1]; v = {nf(s, 3)}/{t:.2f} = {nf(v, 3)} m s⁻¹ [1]; % = {nf(_pct(s, 2 * dx), 2)} + {nf(_pct(t, dt), 2)} = {nf(pc, 2)}% [1] [3]')


@t13.add('C2', (2, 3, 4), 'explain')
def t13_acc(r, D):
    true = r.choice([9.81, 1.50, 2.70, 340, 0.250])
    spread = r.choice(['small', 'large']); off = r.choice([True, False])
    vals = []
    for i in range(4):
        base = true * (1.12 if off else 1.0)
        dv = (0.004 if spread == 'small' else 0.06) * true
        vals.append(base + r.choice([-1, 1]) * dv * r.choice([0.5, 1, 1.5]))
    acc = 'accurate' if not off else 'not accurate'
    pre = 'precise' if spread == 'small' else 'not precise'
    q = r.choice(['the acceleration of free fall', 'the resistance of a standard resistor', 'the density of aluminium', 'the speed of sound', 'the mass of a standard sample'])
    return Q(f'Four measurements of {q} are ' + ', '.join(nf(v, 3) for v in vals) + f' (same unit). The accepted value is {nf(true, 3)}. Describe the readings in terms of accuracy and precision, and suggest what type of error is most likely present.',
             f'They are {pre} and {acc}. ' + ('A systematic error (e.g. zero or calibration error) is likely because the mean is shifted from the true value.' if off else 'Mainly random error; no systematic shift is evident.') + (' The large scatter shows significant random error.' if spread == 'large' else ''),
             'precision judged from spread [1]; accuracy judged from mean vs accepted value [1]; correct error type [1] [3]')


def _unc_c4(r, D):
    L = r.choice([0.800, 1.000, 1.200, 1.500]); dL = 0.002
    d = r.choice([0.28, 0.32, 0.36, 0.40]); dd = 0.01
    R = r.choice([4.2, 5.6, 6.8, 8.1]); dR = 0.1
    A = math.pi * (d * 1e-3) ** 2 / 4
    rho = R * A / L
    pc = _pct(R, dR) + 2 * _pct(d, dd) + _pct(L, dL)
    intro = r.choice([f'{person(r)} determines the resistivity of a metal wire using ρ = RA/L. The measurements are L = {L:.3f} ± {dL:.3f} m, diameter d = {d:.2f} ± {dd:.2f} mm and R = {R:.1f} ± {dR:.1f} Ω.',
                      f'In {lab(r)}, the resistivity of a wire is found from ρ = RA/L, with R = {R:.1f} ± {dR:.1f} Ω, L = {L:.3f} ± {dL:.3f} m and d = {d:.2f} ± {dd:.2f} mm.'])
    parts = [
        lambda r: ('Calculate the cross-sectional area of the wire.', f'{sci(A, 3)} m²', f'A = πd²/4 = π × ({sci(d * 1e-3, 2)})²/4 [2]'),
        lambda r: ('Calculate the resistivity.', f'{sci(rho, 3)} Ω m', f'ρ = RA/L = {R:.1f} × {sci(A, 3)}/{L:.3f} [2]'),
        lambda r: ('Calculate the percentage uncertainty in the resistivity.', f'{nf(pc, 2)}%', f'%R + 2%d + %L = {nf(_pct(R, dR), 2)} + {nf(2 * _pct(d, dd), 2)} + {nf(_pct(L, dL), 2)} [3]'),
        lambda r: ('State which measurement contributes most to the uncertainty and suggest how to reduce it.', 'The diameter (its percentage is doubled); measure with a micrometer at several points along the wire and average.', 'diameter identified [1]; micrometer/repeat at different places [1] [2]'),
        lambda r: ('Explain why the micrometer should be checked for zero error before use.', 'A zero error is systematic and would shift every diameter reading, giving an inaccurate area and resistivity.', 'zero error systematic [1]; shifts all readings/affects ρ via d² [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t13.add('C4', (2, 3, 4, 5), 'multi_step')(_unc_c4)

N14 = 'Scalars and vectors: adding, subtracting and resolving vectors'
t14 = topic(N14, N14.lower(), 'scalars and vectors', 'resolving vectors')
FX(t14, 'C1', (1, 2), [
    ('Which list contains only vector quantities?', 'displacement, acceleration, momentum', 'All three have direction.', ['speed, acceleration, momentum', 'displacement, work, force', 'mass, weight, velocity']),
    ('Which list contains only scalar quantities?', 'kinetic energy, power, temperature', 'None of these has direction.', ['kinetic energy, momentum, power', 'mass, weight, density', 'distance, velocity, time']),
    ('A force F acts at an angle θ above the horizontal. What is its horizontal component?', 'F cos θ', 'The component adjacent to θ is F cos θ.', ['F sin θ', 'F tan θ', 'F/cos θ']),
    ('Two forces of 3.0 N and 4.0 N act on a point. Which resultant is NOT possible?', '8.0 N', 'Resultant lies between 4.0 − 3.0 = 1.0 N and 4.0 + 3.0 = 7.0 N.', ['1.0 N', '5.0 N', '7.0 N']),
    ('Two perpendicular forces of 5.0 N and 12.0 N act on an object. What is the magnitude of the resultant?', '13.0 N', '√(5² + 12²) = 13 N.', ['17.0 N', '7.0 N', '60.0 N']),
    ('Which is the correct method to find the change in velocity of an object?', 'Add the final velocity vector to the reverse of the initial velocity vector', 'Δv = v − u = v + (−u).', ['Subtract the final speed from the initial speed', 'Add the initial and final velocity vectors', 'Multiply the initial velocity by the final velocity']),
    ('A ball moving at 6 m s⁻¹ rebounds from a wall at 4 m s⁻¹ along the same line. What is the magnitude of its change in velocity?', '10 m s⁻¹', 'Taking towards the wall positive: Δv = −4 − 6 = −10 m s⁻¹.', ['2 m s⁻¹', '24 m s⁻¹', '5 m s⁻¹']),
    ('State what is meant by a vector quantity.', 'A quantity that has both magnitude and direction.', 'magnitude and direction [1]'),
])
FX(t14, 'C2', (1, 2, 3, 4), [
    ('Explain why the resultant of two forces of 6 N and 8 N can have any value between 2 N and 14 N.', 'When the forces are in the same direction the resultant is the sum, 14 N; in opposite directions it is the difference, 2 N; at other angles it takes intermediate values.', 'same direction gives 14 N [1]; opposite gives 2 N, intermediate otherwise [1] [2]'),
    ('Explain why resolving a force into two perpendicular components is useful.', 'Perpendicular components act independently, so the effects in each direction can be analysed separately (e.g. for motion on a slope or projectiles).', 'components independent [1]; allows each direction to be treated separately with example [1] [2]'),
    ('Explain why a car going around a bend at constant speed has a changing velocity.', 'Velocity is a vector; its direction changes on the bend so the velocity changes although its magnitude (speed) is constant.', 'velocity has direction [1]; direction changes [1] [2]'),
    ('An aircraft flies north while a wind blows from the west. Explain why its velocity relative to the ground is not due north.', 'The ground velocity is the vector sum of the air velocity (north) and the wind velocity (east), so the resultant points east of north.', 'vector addition of air and wind velocity [1]; resultant east of north [1] [2]'),
    ('Describe how to find the resultant of two non-perpendicular forces by scale drawing.', 'Choose a scale, draw the first force to scale, draw the second from its tip at the correct angle (tip to tail), then measure the length and angle of the line from start to end.', 'scale and tip-to-tail [1]; closing side measured for magnitude [1]; direction measured [1] [3]'),
])


@t14.add('C3', (1, 2, 3, 4), 'numerical')
def t14_resolve(r, D):
    F = r.choice([12, 15, 20, 25, 40, 50, 64, 80, 120, 250])
    th = r.choice([20, 25, 30, 35, 40, 50, 55, 60, 65])
    ctx = r.choice([(f'A rope pulls a sledge with a force of {F} N at {th}° above the horizontal.', 'horizontal'), (f'A cable on a crane exerts a force of {F} N at {th}° to the horizontal.', 'horizontal'),
                    (f'A child pulls a suitcase with a force of {F} N along its handle, which is at {th}° to the horizontal.', 'horizontal'), (f'A force of {F} N acts at {th}° to the vertical on a bracket.', 'vertical')])
    s, dirn = ctx
    comp = F * math.cos(math.radians(th)); other = F * math.sin(math.radians(th))
    oth = 'vertical' if dirn == 'horizontal' else 'horizontal'
    if D <= 2:
        return numq(r, D, s, f'{dirn} component of the force', comp, ' N', f'{F} cos {th}°', [other, F * math.tan(math.radians(th)), F], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + f' Calculate the {dirn} and {oth} components of the force.', f'{dirn} {nf(comp, 3)} N; {oth} {nf(other, 3)} N',
                 f'{F} cos {th}° = {nf(comp, 3)} N [1]; {F} sin {th}° = {nf(other, 3)} N [1]; correct assignment [1] [3]')
    Rf = r.choice([5, 8, 10, 15]) * F / 50
    return Q(s + f' A horizontal resistive force of {nf(Rf, 2)} N also acts. Calculate the resultant horizontal force and state one assumption.' if dirn == 'horizontal' else s + ' Calculate both components and show that their resultant is the original force.',
             (f'{nf(comp - Rf, 3)} N; assume the {nf(Rf, 2)} N force acts horizontally opposite to motion.' if dirn == 'horizontal' else f'{dirn} {nf(comp, 3)} N, {oth} {nf(other, 3)} N; √({nf(comp, 3)}² + {nf(other, 3)}²) = {F} N'),
             (f'horizontal component {F} cos {th}° = {nf(comp, 3)} N [1]; subtract resistive force [1]; {nf(comp - Rf, 3)} N [1]; assumption [1] [4]' if dirn == 'horizontal' else f'components [2]; Pythagoras [1]; = {F} N [1] [4]'))


@t14.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_add(r, D):
    a = r.choice([3.0, 4.5, 6.0, 8.0, 12, 15, 20]); b = r.choice([2.5, 4.0, 5.0, 7.5, 9.0, 16, 24])
    kind = r.choice(['walk', 'boat', 'plane', 'force'])
    if D <= 3:
        R = math.hypot(a, b); ang = math.degrees(math.atan2(b, a))
        if kind == 'walk':
            s = f'{person(r)} walks {nf(a)} km due east and then {nf(b)} km due north.'
            q, u, ans2 = 'magnitude of the displacement', ' km', f'{nf(ang, 3)}° north of east'
        elif kind == 'boat':
            s = f'A boat in {city(r)} harbour heads due north at {nf(a)} m s⁻¹ relative to the water, while a current flows due east at {nf(b)} m s⁻¹.'
            q, u, ans2 = 'resultant speed of the boat', ' m s⁻¹', f'{nf(90 - ang, 3)}° east of north'
        elif kind == 'plane':
            s = f'A light aircraft has an air speed of {nf(10 * a)} m s⁻¹ due south. A wind blows at {nf(b)} m s⁻¹ towards the west.'
            a = 10 * a; R = math.hypot(a, b); ang = math.degrees(math.atan2(b, a))
            q, u, ans2 = 'resultant speed of the aircraft', ' m s⁻¹', f'{nf(ang, 3)}° west of south'
        else:
            s = f'Two forces of {nf(a)} N and {nf(b)} N act at right angles on a small ring.'
            q, u, ans2 = 'magnitude of the resultant force', ' N', f'{nf(ang, 3)}° to the {nf(a)} N force'
        if D <= 2:
            return numq(r, D, s, q, R, u, f'√({nf(a)}² + {nf(b)}²)', [a + b, abs(a - b), a * b / 2], fm=lambda x: nf(x, 3))
        return Q(s + f' Calculate the {q} and its direction.', f'{nf(R, 3)}{u}, {ans2}', f'Pythagoras: √({nf(a)}² + {nf(b)}²) [1] = {nf(R, 3)}{u} [1]; trigonometry for angle: {ans2} [1] [3]')
    th = r.choice([40, 50, 60, 70, 110, 120, 135])
    R = math.sqrt(a * a + b * b + 2 * a * b * math.cos(math.radians(th)))
    return Q(f'Two forces of {nf(a)} N and {nf(b)} N act at a point. The angle between their directions is {th}°. By resolving or by using the cosine rule, determine the magnitude of the resultant force.' + (' Check your answer is between the minimum and maximum possible resultants.' if D >= 5 else ''),
             f'{nf(R, 3)} N', f'resolve along and perpendicular to one force: ({nf(a)} + {nf(b)} cos {th}°) and {nf(b)} sin {th}° [2]; combine by Pythagoras = {nf(R, 3)} N [1]; ' + (f'correct magnitude [1]; check: between {nf(abs(a - b))} N and {nf(a + b)} N [1] [5]' if D >= 5 else 'correct magnitude to 3 s.f. [1] [4]'))


@t14.add('C3', (2, 3, 4), 'numerical')
def t14_dv(r, D):
    u = r.choice([4.0, 5.0, 6.0, 8.0, 12, 15]); v = r.choice([3.0, 4.0, 5.0, 6.0, 9.0, 10])
    kind = r.choice(['rebound', 'turn'])
    if kind == 'rebound':
        s = r.choice([f'A tennis ball hits a wall at {nf(u)} m s⁻¹ and rebounds along the same line at {nf(v)} m s⁻¹.', f'A squash ball travelling at {nf(u)} m s⁻¹ bounces straight back from the front wall at {nf(v)} m s⁻¹.', f'A trolley moving at {nf(u)} m s⁻¹ hits a buffer and moves back along its path at {nf(v)} m s⁻¹.'])
        return Q(s + ' Calculate the change in velocity, stating its direction.', f'{nf(u + v)} m s⁻¹ away from the wall (opposite to the initial velocity)', f'sign convention: Δv = (−{nf(v)}) − {nf(u)} [1]; magnitude {nf(u + v)} m s⁻¹ [1]; direction away from the wall [1] [3]')
    dv = math.hypot(u, v)
    return Q(f'A car travelling due east at {nf(u)} m s⁻¹ turns a corner and then travels due north at {nf(v)} m s⁻¹. Determine the magnitude and direction of its change in velocity.', f'{nf(dv, 3)} m s⁻¹ directed {nf(math.degrees(math.atan2(v, u)), 3)}° north of west',
             f'Δv = v + (−u) drawn as a vector triangle [1]; √({nf(u)}² + {nf(v)}²) = {nf(dv, 3)} m s⁻¹ [1]; direction tan⁻¹({nf(v)}/{nf(u)}) north of west [1] [3]')


def _vec_c4(r, D):
    W = r.choice([150, 200, 240, 300, 360]); th = r.choice([20, 25, 30, 35])
    intro = r.choice([f'A box of weight {W} N rests on a ramp inclined at {th}° to the horizontal in a warehouse in {city(r)}.', f'A skier of weight {W} N stands on a slope inclined at {th}° to the horizontal.', f'A crate of weight {W} N is held at rest on a smooth slope of angle {th}° by a rope parallel to the slope.'])
    par = W * math.sin(math.radians(th)); perp = W * math.cos(math.radians(th))
    parts = [
        lambda r: ('State the difference between a scalar and a vector, using weight and mass as examples.', 'Weight is a vector (magnitude and direction, downwards); mass is a scalar (magnitude only).', 'definition [1]; weight vector, mass scalar [1] [2]'),
        lambda r: ('Calculate the component of the weight parallel to the slope.', f'{nf(par, 3)} N', f'W sin θ = {W} sin {th}° [2]'),
        lambda r: ('Calculate the component of the weight perpendicular to the slope.', f'{nf(perp, 3)} N', f'W cos θ = {W} cos {th}° [2]'),
        lambda r: ('State the size of the normal contact force from the slope, explaining your answer.', f'{nf(perp, 3)} N, because there is no acceleration perpendicular to the slope.', 'equal to the perpendicular component [1]; no perpendicular acceleration [1] [2]'),
        lambda r: (f'The angle of the slope is increased. Explain how the two components change.', 'The parallel component (W sin θ) increases and the perpendicular component (W cos θ) decreases.', 'parallel increases [1]; perpendicular decreases [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t14.add('C4', (2, 3, 4, 5), 'multi_step')(_vec_c4)

CHAPTERS[1] = [t11, t12, t13, t14]


# ===================================================================== 2 Kinematics
N21 = 'Distance, displacement, speed, velocity and acceleration'
t21 = topic(N21, N21.lower(), 'displacement', 'speed velocity acceleration')
FX(t21, 'C1', (1, 2), [
    ('Which is the correct definition of displacement?', 'Distance moved in a specified direction', 'Displacement is a vector: distance in a stated direction from a reference point.',
     ['Total length of the path travelled', 'Rate of change of distance', 'Speed in a specified direction']),
    ('Which is the correct definition of velocity?', 'Rate of change of displacement', 'v = Δs/Δt, a vector.', ['Distance travelled per unit time', 'Rate of change of speed', 'Displacement multiplied by time']),
    ('Which is the correct definition of acceleration?', 'Rate of change of velocity', 'a = Δv/Δt, unit m s⁻².', ['Rate of change of speed', 'Change of velocity multiplied by time', 'Rate of change of displacement']),
    ('A runner completes exactly one lap of a 400 m circular track in 80 s. What is the average velocity?', '0 m s⁻¹', 'Displacement after one lap is zero, so average velocity is zero (average speed is 5 m s⁻¹).',
     ['5 m s⁻¹', '0.2 m s⁻¹', '32 000 m s⁻¹']),
    ('A car speeds up from 10 m s⁻¹ to 25 m s⁻¹ in 5.0 s. What is its average acceleration?', '3.0 m s⁻²', 'a = (25 − 10)/5.0 = 3.0 m s⁻².', ['5.0 m s⁻²', '7.0 m s⁻²', '2.0 m s⁻²']),
    ('What is 72 km h⁻¹ in m s⁻¹?', '20 m s⁻¹', '72 000 m ÷ 3600 s = 20 m s⁻¹.', ['72 m s⁻¹', '260 m s⁻¹', '7.2 m s⁻¹']),
    ('Which quantity can be negative?', 'velocity', 'Velocity is a vector; a negative sign shows direction.', ['speed', 'distance', 'time interval']),
    ('State what is meant by speed.', 'Distance travelled per unit time (rate of change of distance).', 'distance per unit time [1]'),
    ('State the SI unit of acceleration.', 'm s⁻²', 'm s⁻² [1]'),
])
FX(t21, 'C2', (1, 2, 3, 4), [
    ('Explain why an object moving at constant speed can still be accelerating.', 'Acceleration is the rate of change of velocity; if the direction of motion changes (e.g. in a circle), the velocity changes even though the speed is constant.', 'acceleration = rate of change of velocity [1]; direction change means velocity change [1] [2]'),
    ('Explain the difference between average speed and average velocity for a journey that returns to its starting point.', 'Average speed = total distance/total time, which is non-zero; average velocity = displacement/time, which is zero because the displacement is zero.', 'speed uses distance (non-zero) [1]; velocity uses displacement (zero) [1] [2]'),
    ('A ball is thrown vertically upwards. Explain why its velocity at the top is zero but its acceleration is not.', 'At the top the ball is momentarily at rest, so v = 0, but its velocity is still changing (from upwards to downwards) at 9.81 m s⁻² due to gravity.', 'v = 0 momentarily [1]; velocity still changing, a = g downwards [1] [2]'),
    ('Explain what is meant by a negative acceleration when the velocity is positive.', 'The acceleration is in the opposite direction to the velocity, so the object is slowing down (decelerating).', 'acceleration opposite to velocity [1]; speed decreasing [1] [2]'),
    ('A car speedometer reads a steady 50 km h⁻¹ as the car travels around a roundabout. Explain whether the car is in equilibrium.', 'No: its direction changes, so its velocity changes and it accelerates; a resultant force (towards the centre) acts, so it is not in equilibrium.', 'velocity changing / accelerating [1]; resultant force so not in equilibrium [1] [2]'),
])


@t21.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_avg(r, D):
    a = r.choice([300, 400, 450, 600, 800, 1200]); b = r.choice([150, 200, 250, 350, 500])
    t1 = r.choice([60, 80, 100, 120, 150]); t2 = r.choice([40, 50, 70, 90, 110])
    who = person(r)
    kind = r.choice(['line', 'perp'])
    if kind == 'line':
        s = f'{who} walks {a} m due east in {t1} s and then {b} m due west in {t2} s.'
        disp = abs(a - b); dirn = 'east' if a > b else 'west'
    else:
        s = f'{who} cycles {a} m due north in {t1} s and then {b} m due east in {t2} s.'
        disp = math.hypot(a, b); dirn = f'{nf(math.degrees(math.atan2(b, a)), 3)}° east of north'
    sp = (a + b) / (t1 + t2); vel = disp / (t1 + t2)
    if D <= 2:
        return numq(r, D, s, 'average speed for the whole journey', sp, ' m s⁻¹', f'({a} + {b})/({t1} + {t2})', [vel, a / t1, (a / t1 + b / t2) / 2 * 1.37], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the average speed and the magnitude of the average velocity for the whole journey.', f'speed {nf(sp, 3)} m s⁻¹; velocity {nf(vel, 3)} m s⁻¹',
                 f'total distance {a + b} m ÷ {t1 + t2} s = {nf(sp, 3)} m s⁻¹ [1]; displacement {nf(disp, 3)} m [1]; velocity {nf(vel, 3)} m s⁻¹ [1] [3]')
    return Q(s + ' (a) Calculate the average speed. (b) Determine the average velocity (magnitude and direction). (c) Explain why the two answers differ.',
             f'(a) {nf(sp, 3)} m s⁻¹ (b) {nf(vel, 3)} m s⁻¹, {dirn} (c) speed uses total distance (scalar); velocity uses displacement (vector), which is shorter.',
             f'(a) {a + b}/{t1 + t2} = {nf(sp, 3)} m s⁻¹ [1] (b) displacement {nf(disp, 3)} m [1]; {nf(vel, 3)} m s⁻¹ [1]; direction {dirn} [1] (c) distance vs displacement [1] [5]', 'multi_step')


@t21.add('C3', (1, 2, 3, 4), 'numerical')
def t21_acc(r, D):
    u = r.choice([0, 18, 36, 54, 72, 90]); v = u + r.choice([18, 36, 54, 72])
    t = r.choice([4.0, 5.0, 6.0, 8.0, 10, 12])
    veh = r.choice(['a car on a motorway near ' + city(r), 'a train leaving a station', 'a motorcycle', 'a bus pulling away from a stop', 'an electric scooter'])
    a = (v - u) / 3.6 / t
    if D <= 2:
        return numq(r, D, f'The speed of {veh} increases from {u} km h⁻¹ to {v} km h⁻¹ in {nf(t)} s.', 'average acceleration', a, ' m s⁻²', f'Δv = {v - u} km h⁻¹ = {nf((v - u) / 3.6, 3)} m s⁻¹; a = Δv/t', [(v - u) / t, v / 3.6 / t, (v - u) / 3.6 * t], fm=lambda x: nf(x, 3))
    s = (u + v) / 2 / 3.6 * t
    return Q(f'The speed of {veh} increases uniformly from {u} km h⁻¹ to {v} km h⁻¹ in {nf(t)} s. Calculate (a) the acceleration in m s⁻² and (b) the distance travelled in this time.', f'(a) {nf(a, 3)} m s⁻² (b) {nf(s, 3)} m',
             f'(a) convert: {nf(u / 3.6, 3)} and {nf(v / 3.6, 3)} m s⁻¹ [1]; a = Δv/t = {nf(a, 3)} m s⁻² [1] (b) s = ½(u + v)t = {nf(s, 3)} m [2] [4]', 'multi_step')


@t21.add('C2', (2, 3, 4), 'explain')
def t21_err(r, D):
    R_ = r.choice([20, 25, 30, 40, 50]); T = r.choice([20, 30, 40, 60])
    who = person(r)
    return Q(f'{who} runs half-way round a circular track of radius {R_} m in {T} s and claims: "My average velocity was {nf(math.pi * R_ / T, 3)} m s⁻¹." Identify the error and calculate the correct average velocity.',
             f'{who} used the distance (πr = {nf(math.pi * R_, 3)} m), which gives the average speed. Displacement is the diameter, {2 * R_} m, so average velocity = {nf(2 * R_ / T, 3)} m s⁻¹ across the track.',
             'used distance not displacement [1]; displacement = diameter [1]; correct value with direction [1] [3]')


def _kin_c4(r, D):
    u = r.choice([8, 10, 12, 15]); t1 = r.choice([10, 12, 15, 20]); t2 = r.choice([5, 6, 8])
    who = person(r)
    intro = r.choice([f'{who} drives a delivery van along a straight road in {city(r)} at a constant {u} m s⁻¹ for {t1} s, then brakes uniformly to rest in {t2} s.',
                      f'A tram travels along a straight track at {u} m s⁻¹ for {t1} s and then decelerates uniformly, stopping {t2} s later.'])
    d1 = u * t1; d2 = 0.5 * u * t2
    parts = [
        lambda r: ('Calculate the distance travelled at constant speed.', f'{d1} m', f's = vt = {u} × {t1} [1]'),
        lambda r: ('Calculate the deceleration.', f'{nf(u / t2, 3)} m s⁻²', f'a = Δv/t = {u}/{t2} [2]'),
        lambda r: ('Calculate the total distance travelled.', f'{nf(d1 + d2, 3)} m', f'{d1} + ½ × {u} × {t2} = {nf(d1 + d2, 3)} [2]'),
        lambda r: ('Calculate the average speed for the whole motion.', f'{nf((d1 + d2) / (t1 + t2), 3)} m s⁻¹', f'{nf(d1 + d2, 3)}/{t1 + t2} [2]'),
        lambda r: ('Explain why the average speed is less than the initial speed.', 'During braking the van moves more slowly than its initial speed, so the total distance per unit time is reduced.', 'slower during deceleration [1]'),
        lambda r: ('State the difference between speed and velocity.', 'Velocity is speed in a stated direction (a vector); speed is a scalar.', 'vector vs scalar [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t21.add('C4', (2, 3, 4, 5), 'multi_step')(_kin_c4)

N22 = 'Displacement-time and velocity-time graphs: gradients and areas'
t22 = topic(N22, N22.lower(), 'velocity-time graphs', 'gradients and areas')
FX(t22, 'C1', (1, 2), [
    ('What does the gradient of a displacement-time graph represent?', 'Velocity', 'Gradient = Δs/Δt = velocity.', ['Acceleration', 'Displacement', 'Distance travelled']),
    ('What does the gradient of a velocity-time graph represent?', 'Acceleration', 'Gradient = Δv/Δt = acceleration.', ['Displacement', 'Velocity', 'Rate of change of acceleration']),
    ('What does the area under a velocity-time graph represent?', 'Displacement', 'Area = ∫v dt = displacement.', ['Acceleration', 'Velocity', 'Momentum']),
    ('A displacement-time graph is a horizontal straight line. The object is', 'stationary', 'Zero gradient means zero velocity.', ['moving at constant velocity', 'accelerating uniformly', 'decelerating uniformly']),
    ('A velocity-time graph is a straight line sloping upwards from the origin. The object has', 'constant acceleration from rest', 'Constant positive gradient: uniform acceleration from v = 0.', ['constant velocity', 'increasing acceleration', 'zero acceleration']),
    ('A displacement-time graph is a curve whose gradient increases with time. The object is', 'accelerating', 'Increasing gradient means increasing velocity.', ['decelerating', 'moving at constant velocity', 'at rest']),
    ('On a velocity-time graph, the line crosses below the time axis. This shows that the object', 'is moving in the opposite direction', 'Negative velocity: motion in the negative direction.', ['has stopped permanently', 'is decelerating to rest', 'has negative mass']),
    ('State how the acceleration at an instant is found from a curved velocity-time graph.', 'Draw a tangent to the curve at that instant and find its gradient.', 'tangent [1]; gradient of tangent [1] [2]'),
])
FX(t22, 'C2', (1, 2, 3, 4), [
    ('Explain how a velocity-time graph shows a body moving with decreasing acceleration.', 'The gradient (acceleration) decreases with time, so the line is a curve that becomes less steep (flattens out).', 'gradient = acceleration [1]; curve becoming less steep [1] [2]'),
    ('A ball is dropped and bounces several times. Explain why its velocity-time graph has straight sections that are all parallel.', 'Between bounces the only force is weight (ignoring air resistance), so acceleration is g every time; equal gradients give parallel lines.', 'acceleration = g in flight [1]; gradient = acceleration so parallel [1] [2]'),
    ('Explain why the area under a speed-time graph gives distance but the area under a velocity-time graph gives displacement.', 'Speed is always positive so all area adds as distance; velocity can be negative, so areas below the axis are subtracted, giving displacement.', 'speed positive → distance [1]; negative velocity areas subtract → displacement [1] [2]'),
    ('Describe the displacement-time graph of a ball thrown vertically upwards and caught at the same height.', 'A symmetrical curve (inverted parabola): displacement rises with decreasing gradient to a maximum (zero gradient at the top), then falls with increasing negative gradient to zero.', 'parabolic/symmetrical [1]; gradient zero at top [1]; returns to zero [1] [3]'),
    ('Explain how to use a displacement-time graph to find the instantaneous velocity of an object that is accelerating.', 'Draw a tangent to the curve at the chosen time; the gradient of the tangent (Δs/Δt using a large triangle) is the instantaneous velocity.', 'tangent at the point [1]; gradient = velocity, large triangle [1] [2]'),
])


def _vt(r):
    v1 = r.choice([6, 8, 10, 12, 15, 18, 20, 24])
    ta = r.choice([2, 3, 4, 5, 6]); tb = r.choice([4, 5, 6, 8, 10]); tc = r.choice([2, 3, 4, 5, 6])
    return v1, ta, tb, tc


@t22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_vt(r, D):
    v1, ta, tb, tc = _vt(r)
    thing = r.choice(['a cyclist', 'a lift moving upwards', 'a sprinter', 'a car in a test track', 'a toy train', 'a delivery drone flying horizontally'])
    desc = f'A velocity-time graph for {thing} shows a straight line from (0, 0) to ({ta} s, {v1} m s⁻¹), a horizontal line to ({ta + tb} s, {v1} m s⁻¹) and a straight line down to ({ta + tb + tc} s, 0).'
    s = 0.5 * v1 * ta + v1 * tb + 0.5 * v1 * tc
    if D <= 1:
        return numq(r, D, desc, 'acceleration in the first section', v1 / ta, ' m s⁻²', f'gradient = {v1}/{ta}', [v1 * ta, v1 / (ta + tb), ta / v1], fm=lambda x: nf(x, 3))
    if D == 2:
        return Q(desc + ' Calculate the total displacement.', f'{nf(s, 3)} m', f'area = ½ × {ta} × {v1} + {tb} × {v1} + ½ × {tc} × {v1} [1]; = {nf(s, 3)} m [1] [2]')
    if D == 3:
        return Q(desc + ' Calculate the deceleration in the final section and the average velocity for the whole journey.', f'deceleration {nf(v1 / tc, 3)} m s⁻²; average velocity {nf(s / (ta + tb + tc), 3)} m s⁻¹',
                 f'{v1}/{tc} = {nf(v1 / tc, 3)} m s⁻² [1]; area = {nf(s, 3)} m [1]; ÷ {ta + tb + tc} s = {nf(s / (ta + tb + tc), 3)} m s⁻¹ [1] [3]')
    return Q(desc + ' (a) Calculate the acceleration in each section. (b) Calculate the total displacement. (c) Describe the shape of the corresponding displacement-time graph.',
             f'(a) {nf(v1 / ta, 3)} m s⁻², 0, −{nf(v1 / tc, 3)} m s⁻² (b) {nf(s, 3)} m (c) curve of increasing gradient, then straight line, then curve of decreasing gradient levelling off at {nf(s, 3)} m.',
             f'(a) three gradients [2] (b) total area {nf(s, 3)} m [1] (c) curve up / straight / curve flattening [2] [5]', 'multi_step')


@t22.add('C3', (1, 2, 3, 4), 'numerical')
def t22_st(r, D):
    v = r.choice([1.5, 2.0, 2.5, 3.0, 4.0, 5.0]); t1 = r.choice([4, 5, 6, 8]); t2 = r.choice([3, 4, 5, 6])
    s1 = v * t1
    v2 = r.choice([1.0, 2.0, 3.0])
    who = person(r)
    desc = f'The displacement-time graph for {who} walking along a straight corridor is a straight line from (0, 0) to ({t1} s, {nf(s1)} m), then a horizontal line until {t1 + t2} s, then a straight line back to zero displacement taking {nf(s1 / v2)} s.'
    if D <= 2:
        return numq(r, D, desc, 'velocity during the first section', v, ' m s⁻¹', f'gradient = {nf(s1)}/{t1}', [s1, s1 * t1, t1 / s1], fm=lambda x: nf(x, 3))
    tt = t1 + t2 + s1 / v2
    return Q(desc + ' Determine the velocity in each section and the average speed for the whole motion.', f'{nf(v, 3)} m s⁻¹, 0, −{nf(v2, 3)} m s⁻¹; average speed {nf(2 * s1 / tt, 3)} m s⁻¹',
             f'gradients: {nf(v)} m s⁻¹ and 0 [1]; return section negative: −{nf(v2)} m s⁻¹ [1]; total distance {nf(2 * s1)} m ÷ {nf(tt, 3)} s [1]; = {nf(2 * s1 / tt, 3)} m s⁻¹ [1] [4]')


@t22.add('C3', (2, 3, 4), 'numerical')
def t22_tangent(r, D):
    a = r.choice([0.5, 0.8, 1.2, 1.5, 2.0, 2.5]); t = r.choice([2, 3, 4, 5, 6])
    v = a * t
    t0 = t - r.choice([1, 2]); t1_ = 2 * t - t0
    s0 = 0.5 * a * t0 ** 2; s1 = 0.5 * a * t1_ ** 2
    return Q(f'A trolley starts from rest and accelerates uniformly. Its displacement is {nf(s0, 4)} m at t = {t0} s and {nf(s1, 4)} m at t = {t1_} s, and the displacement-time graph is a parabola through the origin. Explain why the gradient of the chord between these points gives the velocity at t = {t} s, and calculate this velocity.',
             f'{nf(v, 3)} m s⁻¹', f'for uniform acceleration the chord gradient equals the tangent gradient at the mid-time {t} s [1]; gradient = ({nf(s1, 4)} − {nf(s0, 4)})/({t1_} − {t0}) [1]; = {nf(v, 3)} m s⁻¹ [1] [3]')


relation(t22, 'C2', (2, 3), 'area under v-t graph = ½vt', 'distance travelled while accelerating from rest', {'final velocity': 1, 'time taken': 1},
         ['A velocity-time graph for a car accelerating uniformly from rest is a straight line through the origin.', 'A sprinter accelerates uniformly from rest; the v-t graph is a straight line from the origin.'])


def _graph_c4(r, D):
    v1, ta, tb, tc = _vt(r)
    tc2 = r.choice([2, 3, 4]); vneg = r.choice([2, 3, 4, 5])
    intro = r.choice([f'A lift starts from rest at the ground floor. It accelerates uniformly to {v1 / 4:.1f} m s⁻¹ in {ta} s, travels at constant velocity for {tb} s and then decelerates uniformly to rest in {tc} s.',
                      f'A remote-controlled car accelerates uniformly from rest to {v1 / 4:.1f} m s⁻¹ in {ta} s, moves at this velocity for {tb} s, then slows uniformly to rest in {tc} s.'])
    v = v1 / 4
    s = 0.5 * v * ta + v * tb + 0.5 * v * tc
    parts = [
        lambda r: ('Sketch the velocity-time graph, labelling key values.', f'straight line up to {v:.1f} m s⁻¹ at {ta} s, horizontal to {ta + tb} s, straight line down to 0 at {ta + tb + tc} s', 'three sections correct [1]; values labelled [1] [2]'),
        lambda r: ('Calculate the acceleration in the first stage.', f'{nf(v / ta, 3)} m s⁻²', f'{v:.1f}/{ta} [2]'),
        lambda r: ('Calculate the total distance travelled.', f'{nf(s, 3)} m', f'area of trapezium = {nf(s, 3)} m [2]'),
        lambda r: ('Calculate the average velocity for the journey.', f'{nf(s / (ta + tb + tc), 3)} m s⁻¹', f'{nf(s, 3)}/{ta + tb + tc} [2]'),
        lambda r: ('Describe how the displacement-time graph would show the constant-velocity stage.', 'A straight line with a constant positive gradient equal to the velocity.', 'straight line [1]; gradient = velocity [1] [2]'),
        lambda r: ('Explain how the graph would show the object later moving backwards.', 'The velocity would become negative: the line goes below the time axis and the area below the axis is subtracted from the displacement.', 'line below axis [1]; negative area reduces displacement [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t22.add('C4', (2, 3, 4, 5), 'multi_step')(_graph_c4)

N23 = 'Determining the acceleration of free fall experimentally'
t23 = topic(N23, N23.lower(), 'acceleration of free fall', 'experimentally')
FX(t23, 'C1', (1, 2), [
    ('A steel ball is released from rest and falls a height h in time t. Which graph gives a straight line through the origin with gradient g/2?', 'h against t²', 'h = ½gt², so h ∝ t² with gradient g/2.', ['h against t', 't against h', 'h² against t']),
    ('Why is a small steel ball used rather than a table-tennis ball when measuring g?', 'Air resistance has a smaller effect on its motion', 'A dense ball has a large weight compared with air resistance.', ['It falls with constant velocity', 'It has a smaller weight', 'It is easier to see']),
    ('In a light-gate experiment, a card of length 5.0 cm passes through a gate in 0.020 s. What is its speed?', '2.5 m s⁻¹', 'v = 0.050/0.020 = 2.5 m s⁻¹.', ['0.25 m s⁻¹', '1.0 m s⁻¹', '25 m s⁻¹']),
    ('Which is the main advantage of using an electromagnet and trapdoor with an electronic timer to measure g?', 'It removes human reaction-time error', 'The timer starts when the magnet releases the ball and stops when it hits the trapdoor.', ['It removes air resistance', 'It makes the ball fall faster', 'It increases the height of fall']),
    ('A ball falls from rest for 0.45 s. Taking g = 9.81 m s⁻², how far does it fall?', '0.99 m', 's = ½gt² = 0.5 × 9.81 × 0.45² = 0.99 m.', ['2.2 m', '4.4 m', '0.49 m']),
    ('State one source of systematic error when timing a falling ball with an electromagnet release.', 'Delay in the release of the ball as the magnetism decays (residual magnetism).', 'delay in release / residual magnetism / h measured to wrong point [1]'),
])
FX(t23, 'C2', (1, 2, 3, 4), [
    ('Explain why plotting h against t² is better than calculating g from a single drop.', 'A graph uses many readings, averages out random errors, reveals anomalous points and shows a systematic error as a non-zero intercept; g = 2 × gradient.', 'uses many readings / reduces random error [1]; intercept reveals systematic error [1] [2]'),
    ('A graph of h against t² for a falling ball has a positive intercept on the t² axis. Suggest a cause.', 'The timer starts before the ball actually begins to fall (e.g. delay in release from the electromagnet), so every measured time is too long by a fixed amount.', 'times systematically too long [1]; release delay cause [1] [2]'),
    ('Explain why the height should be measured from the bottom of the ball at release to the trapdoor.', 'The ball travels this distance before it opens the trapdoor; measuring from its top or centre would give a systematically wrong h.', 'distance actually fallen [1]; other points give systematic error [1] [2]'),
    ('Describe how two light gates can be used to determine g.', 'Drop a card/interrupter of known length through two gates a measured distance h apart; find v₁ and v₂ from length/time at each gate; g = (v₂² − v₁²)/(2h).', 'two gates and measured separation [1]; speeds from length ÷ time [1]; v² = u² + 2as rearranged [1] [3]'),
    ('Explain why a ball dropped from a large height gives a smaller value of g than one dropped from a small height, if timing is accurate.', 'At larger speeds air resistance becomes significant, reducing the acceleration so the ball takes longer, giving a smaller calculated g.', 'air resistance increases with speed [1]; acceleration less than g / longer time [1] [2]'),
])


@t23.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_drop(r, D):
    gtrue = r.choice([9.6, 9.7, 9.8, 9.9, 10.0])
    h = r.choice([0.400, 0.600, 0.800, 1.000, 1.200, 1.500])
    t = math.sqrt(2 * h / gtrue); t = round(t, 3)
    gv = 2 * h / t ** 2
    s = f'{person(r)} releases a steel ball from an electromagnet. An electronic timer records that it takes {t:.3f} s to fall {h:.3f} m onto a trapdoor.'
    if D <= 2:
        return numq(r, D, s, 'value of g obtained', gv, ' m s⁻²', f'g = 2h/t² = 2 × {h:.3f}/{t:.3f}²', [h / t ** 2, 2 * h / t, h / (2 * t ** 2)], fm=lambda x: nf(x, 3))
    dh = 0.002; dt = 0.005 if D == 3 else 0.010
    pc = _pct(h, dh) + 2 * _pct(t, dt)
    return Q(s + f' The uncertainty in h is ±{dh:.3f} m and in t is ±{dt:.3f} s. Calculate g and its absolute uncertainty.', f'g = {nf(gv, 3)} ± {nf(gv * pc / 100, 1)} m s⁻²',
             f'g = 2h/t² = {nf(gv, 3)} m s⁻² [1]; %g = %h + 2%t = {nf(_pct(h, dh), 2)} + {nf(2 * _pct(t, dt), 2)} = {nf(pc, 2)}% [1]; Δg = {nf(gv * pc / 100, 1)} m s⁻² [1]' + (' [3]' if D == 3 else '; g quoted to a precision consistent with Δg [1] [4]'))


@t23.add('C3', (2, 3, 4, 5), 'numerical')
def t23_gates(r, D):
    L = r.choice([0.020, 0.025, 0.040, 0.050])
    v1 = r.choice([0.8, 1.0, 1.2, 1.5]); h = r.choice([0.300, 0.400, 0.500, 0.600])
    gt = r.choice([9.7, 9.8, 9.9])
    v2 = math.sqrt(v1 ** 2 + 2 * gt * h)
    t1 = round(L / v1, 4); t2 = round(L / v2, 4)
    V1, V2 = L / t1, L / t2
    gv = (V2 ** 2 - V1 ** 2) / (2 * h)
    return Q(f'A card of length {L * 100:.1f} cm falls vertically through two light gates {h * 100:.1f} cm apart. The card takes {t1 * 1000:.1f} ms to pass the upper gate and {t2 * 1000:.1f} ms to pass the lower gate. Determine the acceleration of free fall.',
             f'{nf(gv, 3)} m s⁻²', f'v₁ = {L}/{t1} = {nf(V1, 3)} m s⁻¹ and v₂ = {nf(V2, 3)} m s⁻¹ [1]; v₂² = v₁² + 2gh [1]; g = ({nf(V2, 3)}² − {nf(V1, 3)}²)/(2 × {h}) [1]; = {nf(gv, 3)} m s⁻² [1] [4]')


@t23.add('C3', (3, 4, 5), 'case')
def t23_graph(r, D):
    gt = r.choice([9.5, 9.6, 9.7, 9.8, 9.9])
    hs = [0.20, 0.40, 0.60, 0.80, 1.00]
    off = r.choice([0.0, 0.0, 0.01, 0.015])
    ts = [math.sqrt(2 * h / gt) + off for h in hs]
    rows = '; '.join(f'h = {h:.2f} m, t = {t:.3f} s' for h, t in zip(hs, ts))
    t2 = [t * t for t in ts]
    grad = (hs[-1] - hs[0]) / (t2[-1] - t2[0])
    gv = 2 * grad
    return Q(f'A student records these results for a ball falling from rest: {rows}. (a) Explain why a graph of h against t² should be a straight line. (b) Use the first and last points of the graph of h against t² to determine g. (c) State what a non-zero intercept would indicate.',
             f'(a) h = ½gt² so h ∝ t² (gradient g/2) (b) gradient = {nf(grad, 3)} m s⁻², g = {nf(gv, 3)} m s⁻² (c) a systematic error such as a delay in release (constant extra time).',
             f'(a) h = ½gt², gradient g/2 [1] (b) t² values {nf(t2[0], 3)} and {nf(t2[-1], 3)} s² [1]; gradient {nf(grad, 3)} [1]; g = 2 × gradient = {nf(gv, 3)} m s⁻² [1] (c) systematic error [1] [5]')


def _gexp_c4(r, D):
    h = r.choice([0.500, 0.750, 1.000]); t = round(math.sqrt(2 * h / 9.81) + r.choice([0, 0.004, 0.008]), 3)
    intro = r.choice([f'{person(r)} plans an experiment in {lab(r)} to determine g by dropping a steel ball through a measured height h and timing the fall.',
                      'A student measures the acceleration of free fall using an electromagnet, a steel ball, a trapdoor and an electronic timer.'])
    gv = 2 * h / t ** 2
    parts = [
        lambda r: (f'For h = {h:.3f} m the time is {t:.3f} s. Calculate g.', f'{nf(gv, 3)} m s⁻²', f'g = 2h/t² [2]'),
        lambda r: ('Explain why the ball must be released from rest.', 'The equation h = ½gt² assumes u = 0; a non-zero initial velocity would give an incorrect (smaller) time.', 'u = 0 assumed in h = ½gt² [1]; otherwise time too short/g wrong [1] [2]'),
        lambda r: ('Describe how the results can be plotted to find g more reliably.', 'Measure t for several h; plot h against t²; g = 2 × gradient.', 'several heights [1]; h vs t², g = 2 × gradient [1] [2]'),
        lambda r: ('Suggest two reasons why the value of g obtained may differ from 9.81 m s⁻².', 'Air resistance; delay in release from the electromagnet; error in measuring h (wrong reference point).', 'first valid reason [1]; second valid reason [1] [2]'),
        lambda r: ('State why a stopwatch operated by hand is unsuitable for this experiment.', 'The fall time is under half a second; reaction time (≈0.2 s) would be a large fraction of it.', 'reaction time large compared with t [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t23.add('C4', (2, 3, 4, 5), 'multi_step')(_gexp_c4)

CHAPTERS[2] = [t21, t22, t23]

# ===================================================================== 3 Accelerated motion
N31 = 'Deriving and using the equations of uniformly accelerated motion'
t31 = topic(N31, N31.lower(), 'equations of uniformly accelerated motion', 'suvat')
FX(t31, 'C1', (1, 2), [
    ('Which equation does NOT apply to uniformly accelerated motion in a straight line?', 's = vt²', 'The suvat equations are v = u + at, s = ½(u + v)t, s = ut + ½at², v² = u² + 2as.', ['v = u + at', 's = ½(u + v)t', 'v² = u² + 2as']),
    ('A car accelerates uniformly from rest at 2.0 m s⁻² for 5.0 s. How far does it travel?', '25 m', 's = ½at² = 0.5 × 2.0 × 25 = 25 m.', ['10 m', '50 m', '5.0 m']),
    ('A train slows uniformly from 30 m s⁻¹ to rest in 600 m. What is the deceleration?', '0.75 m s⁻²', 'a = v²/(2s) = 900/1200 = 0.75 m s⁻².', ['0.05 m s⁻²', '1.5 m s⁻²', '20 m s⁻²']),
    ('The equations of uniformly accelerated motion can only be used when', 'the acceleration is constant', 'They are derived assuming constant acceleration in a straight line.', ['the velocity is constant', 'the object starts from rest', 'the acceleration is zero']),
    ('Which equation is derived from the area under a velocity-time graph for uniform acceleration?', 's = ½(u + v)t', 'The area of the trapezium = ½(u + v)t.', ['v = u + at', 'a = (v − u)/t', 'v = s/t']),
    ('A cyclist moving at 4.0 m s⁻¹ accelerates at 0.50 m s⁻² for 6.0 s. What is the final velocity?', '7.0 m s⁻¹', 'v = u + at = 4.0 + 3.0 = 7.0 m s⁻¹.', ['3.0 m s⁻¹', '4.5 m s⁻¹', '10 m s⁻¹']),
    ('State the quantities represented by u and s in the equations of motion.', 'u is the initial velocity; s is the displacement.', 'both correct [1]'),
])
FX(t31, 'C2', (1, 2, 3, 4), [
    ('Starting from the definition of acceleration, derive v = u + at.', 'a = (v − u)/t for uniform acceleration; rearranging gives v − u = at, so v = u + at.', 'a = (v − u)/t [1]; rearrangement [1] [2]'),
    ('Use a velocity-time graph to derive s = ut + ½at².', 'The area under the line from u to v in time t is a rectangle ut plus a triangle ½(v − u)t; since v − u = at, s = ut + ½at².', 'area = rectangle + triangle [1]; substitute v − u = at [1] [2]'),
    ('Derive v² = u² + 2as from s = ½(u + v)t and v = u + at.', 'From v = u + at, t = (v − u)/a. Substitute: s = ½(u + v)(v − u)/a = (v² − u²)/(2a), so v² = u² + 2as.', 'eliminate t [1]; algebra to v² = u² + 2as [1] [2]'),
    ('Explain why the equations of uniformly accelerated motion cannot be used for a skydiver from the moment of leaving the aircraft until opening the parachute.', 'Air resistance increases with speed, so the resultant force and acceleration decrease; the acceleration is not constant.', 'air resistance varies with speed [1]; acceleration not constant [1] [2]'),
    ('Explain why s = ut + ½at² can give two positive values of t for a given displacement s.', 'If the acceleration is opposite to u, the object passes the position s twice: once on the way out and once on the way back.', 'acceleration opposite to velocity [1]; passes the point twice [1] [2]'),
])

SUV = [('a car', 'joins a motorway', 'accelerates'), ('a train', 'leaves a station in ' + 'the city', 'accelerates'), ('an aircraft', 'moves along a runway', 'accelerates'), ('a cyclist', 'rides down a hill', 'accelerates'),
       ('a lorry', 'approaches traffic lights', 'decelerates'), ('a bus', 'pulls into a stop', 'decelerates'), ('a sprinter', 'leaves the blocks', 'accelerates'), ('a tram', 'approaches a platform', 'decelerates')]


@t31.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t31_suvat(r, D):
    who, doing, how = r.choice(SUV)
    if how == 'accelerates':
        u = r.choice([0, 2.0, 4.0, 5.0, 8.0, 10.0]); a = r.choice([0.50, 0.80, 1.2, 1.5, 2.0, 2.5, 3.0]); t = r.choice([4.0, 5.0, 6.0, 8.0, 10.0, 12.0])
    else:
        u = r.choice([12.0, 15.0, 18.0, 20.0, 25.0]); a = -r.choice([1.0, 1.5, 2.0, 2.5, 3.0]); t = min(r.choice([3.0, 4.0, 5.0, 6.0]), -u / a * 0.95)
        t = round(t, 1)
    v = u + a * t; s = u * t + 0.5 * a * t * t
    find = r.choice(['s', 'v', 'a', 't'])
    city_ = city(r)
    base = f'{cap(who)} {doing.replace("the city", city_)} and {how} uniformly'
    if find == 's':
        setup, qty, val, unit, wk, wr = f'{base} from {nf(u)} m s⁻¹ at {nf(abs(a))} m s⁻² for {nf(t)} s.', 'displacement in this time', s, ' m', f's = ut + ½at² = {nf(u)} × {nf(t)} + ½ × {nf(a)} × {nf(t)}²', [u * t, 0.5 * abs(a) * t * t, v * t]
    elif find == 'v':
        setup, qty, val, unit, wk, wr = f'{base} from {nf(u)} m s⁻¹ at {nf(abs(a))} m s⁻² for {nf(t)} s.', 'final velocity', v, ' m s⁻¹', f'v = u + at = {nf(u)} + ({nf(a)})({nf(t)})', [u - a * t, a * t, u + 0.5 * a * t]
    elif find == 'a':
        setup, qty, val, unit, wk, wr = f'{base} from {nf(u)} m s⁻¹ to {nf(v, 3)} m s⁻¹ over a distance of {nf(s, 3)} m.', 'magnitude of the acceleration', abs(a), ' m s⁻²', f'a = (v² − u²)/(2s) = ({nf(v, 3)}² − {nf(u)}²)/(2 × {nf(s, 3)})', [abs(v - u) / s * 10, abs(v * v - u * u) / s, abs(a) * 2]
    else:
        setup, qty, val, unit, wk, wr = f'{base} from {nf(u)} m s⁻¹ to {nf(v, 3)} m s⁻¹ at {nf(abs(a))} m s⁻².', 'time taken', t, ' s', f't = (v − u)/a = ({nf(v, 3)} − {nf(u)})/{nf(a)}', [abs(v + u) / abs(a), abs(v - u) * abs(a), t * 2]
    if D <= 3:
        return numq(r, D, setup, qty, val, unit, wk, wr, fm=lambda x: nf(x, 3))
    v2 = r.choice([0.6, 0.7, 0.8])
    return Q(f'{base} from {nf(u)} m s⁻¹ at {nf(abs(a))} m s⁻² for {nf(t)} s. (a) Calculate the final velocity. (b) Calculate the displacement. (c) Calculate the average velocity and show it equals ½(u + v).',
             f'(a) {nf(v, 3)} m s⁻¹ (b) {nf(s, 3)} m (c) {nf(s / t, 3)} m s⁻¹ = ½({nf(u)} + {nf(v, 3)})',
             f'(a) v = u + at [1] = {nf(v, 3)} m s⁻¹ [1] (b) s = ut + ½at² = {nf(s, 3)} m [1] (c) s/t = {nf(s / t, 3)} m s⁻¹ and ½(u + v) = {nf((u + v) / 2, 3)} m s⁻¹ [1]' + (' [4]' if D == 4 else '; valid because acceleration is uniform [1] [5]'), 'multi_step')


@t31.add('C3', (2, 3, 4, 5), 'numerical')
def t31_stop(r, D):
    v = r.choice([13.4, 15.0, 20.0, 22.4, 25.0, 31.3]); tr = r.choice([0.6, 0.7, 0.8, 1.0, 1.2]); a = r.choice([5.0, 6.0, 6.5, 7.0, 7.5])
    think = v * tr; brake = v * v / (2 * a)
    who = person(r)
    s = f'{who} is driving at {nf(v)} m s⁻¹ on a road near {city(r)} when a hazard appears. Reaction time is {nf(tr)} s and the brakes then give a uniform deceleration of {nf(a)} m s⁻².'
    if D <= 2:
        return numq(r, D, s, 'braking distance', brake, ' m', f'v² = u² + 2as → s = u²/(2a) = {nf(v)}²/(2 × {nf(a)})', [v * v / a, v / (2 * a), think], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the total stopping distance.', f'{nf(think + brake, 3)} m', f'thinking distance = {nf(v)} × {nf(tr)} = {nf(think, 3)} m [1]; braking = u²/2a = {nf(brake, 3)} m [1]; total {nf(think + brake, 3)} m [1] [3]')
    gap = round((think + brake) * r.choice([0.85, 0.95, 1.1, 1.2]))
    stops = think + brake <= gap
    return Q(s + f' The hazard is {gap} m ahead. (a) Calculate the stopping distance. (b) Determine whether the car stops in time. (c) Explain how the stopping distance would change if the driver were tired.',
             f'(a) {nf(think + brake, 3)} m (b) {"yes" if stops else "no"}: {nf(think + brake, 3)} m {"<" if stops else ">"} {gap} m (c) reaction time increases so thinking distance increases (braking distance unchanged).',
             f'(a) thinking {nf(think, 3)} m [1]; braking {nf(brake, 3)} m [1] (b) comparison and conclusion [1] (c) thinking distance increases [1]' + (' [4]' if D == 4 else '; braking distance unchanged [1] [5]'), 'multi_step')


@t31.add('C2', (2, 3, 4), 'explain')
def t31_err(r, D):
    u = r.choice([5.0, 8.0, 10.0, 12.0]); a = r.choice([2.0, 3.0, 4.0]); t = r.choice([3.0, 4.0, 5.0])
    wrong = u * t + a * t * t; right = u * t + 0.5 * a * t * t
    who = person(r)
    return Q(f'{who} calculates the distance travelled by a car that accelerates uniformly from {nf(u)} m s⁻¹ at {nf(a)} m s⁻² for {nf(t)} s and writes "s = ut + at² = {nf(wrong)} m". Identify the error and give the correct distance. Explain how a velocity-time graph supports the correct equation.',
             f'The factor ½ is missing: s = ut + ½at² = {nf(right, 3)} m. On the v-t graph the area above the rectangle ut is a triangle of area ½ × t × at.',
             'missing ½ identified [1]; correct value [1]; triangle area ½t(at) [1] [3]')


def _suvat_c4(r, D):
    u = r.choice([0, 3.0, 5.0]); a = r.choice([1.5, 2.0, 2.5]); t1 = r.choice([6.0, 8.0, 10.0]); v = u + a * t1; ad = r.choice([3.0, 4.0, 5.0])
    s1 = u * t1 + 0.5 * a * t1 * t1; s2 = v * v / (2 * ad)
    intro = r.choice([f'A test car on a track in {city(r)} accelerates uniformly from {nf(u)} m s⁻¹ at {nf(a)} m s⁻² for {nf(t1)} s, then brakes with a uniform deceleration of {nf(ad)} m s⁻² until it stops.',
                      f'A rocket sled starts at {nf(u)} m s⁻¹ and accelerates uniformly at {nf(a)} m s⁻² for {nf(t1)} s. It then decelerates uniformly at {nf(ad)} m s⁻² to rest.'])
    parts = [
        lambda r: ('Calculate the maximum speed.', f'{nf(v, 3)} m s⁻¹', 'v = u + at [2]'),
        lambda r: ('Calculate the distance travelled while accelerating.', f'{nf(s1, 3)} m', 's = ut + ½at² [2]'),
        lambda r: ('Calculate the braking distance.', f'{nf(s2, 3)} m', 's = v²/(2a) [2]'),
        lambda r: ('Calculate the total time from start to stop.', f'{nf(t1 + v / ad, 3)} s', f'braking time = {nf(v, 3)}/{nf(ad)} = {nf(v / ad, 3)} s, add {nf(t1)} s [2]'),
        lambda r: ('State the assumption made in using the equations of uniformly accelerated motion.', 'The acceleration is constant during each stage (and motion is in a straight line).', 'constant acceleration [1]'),
        lambda r: ('Sketch the velocity-time graph for the whole motion.', 'Straight line rising from u to the maximum speed, then a steeper straight line falling to zero.', 'rising line [1]; falling line steeper/shallower as appropriate to zero [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t31.add('C4', (2, 3, 4, 5), 'multi_step')(_suvat_c4)

N32 = 'Motion under gravity and the effect of air resistance'
t32 = topic(N32, N32.lower(), 'motion under gravity', 'air resistance')
FX(t32, 'C1', (1, 2), [
    ('A ball is thrown vertically upwards. Ignoring air resistance, what is its acceleration at the highest point?', '9.81 m s⁻² downwards', 'The only force is weight; a = g downwards throughout the flight.', ['zero', '9.81 m s⁻² upwards', 'It depends on the speed of throw']),
    ('A stone is dropped from rest. Ignoring air resistance, what is its speed after 2.0 s?', '19.6 m s⁻¹', 'v = gt = 9.81 × 2.0 = 19.6 m s⁻¹.', ['9.81 m s⁻¹', '39.2 m s⁻¹', '4.9 m s⁻¹']),
    ('A feather and a hammer are dropped together in a vacuum. Which statement is correct?', 'They hit the ground at the same time', 'In a vacuum there is no air resistance; all objects fall with acceleration g.', ['The hammer lands first', 'The feather lands first', 'The feather floats']),
    ('A ball is thrown upwards at 15 m s⁻¹. Ignoring air resistance, how long does it take to reach its maximum height?', '1.5 s', 't = u/g = 15/9.81 = 1.5 s.', ['3.1 s', '0.65 s', '15 s']),
    ('A skydiver reaches terminal velocity. Which statement is correct?', 'The air resistance equals the weight', 'At terminal velocity the resultant force is zero.', ['The air resistance is zero', 'The acceleration is 9.81 m s⁻²', 'The weight is zero']),
    ('When air resistance is taken into account, the time for a ball thrown upwards to rise to its highest point is', 'less than the time to fall back down', 'Air resistance adds to weight on the way up and opposes it on the way down, so the descent takes longer.', ['more than the time to fall back down', 'equal to the time to fall back down', 'zero']),
    ('State the value of the acceleration of free fall near the Earth\'s surface used in AS Physics.', '9.81 m s⁻²', '9.81 m s⁻² [1]'),
])
FX(t32, 'C2', (1, 2, 3, 4), [
    ('Explain why a skydiver falling from rest reaches a terminal velocity.', 'As speed increases, air resistance increases; the resultant force (weight − drag) and so the acceleration decrease until drag equals weight; then the acceleration is zero and speed is constant.', 'drag increases with speed [1]; resultant force decreases to zero [1]; constant (terminal) velocity [1] [3]'),
    ('Explain why a skydiver slows down when the parachute opens.', 'The larger area greatly increases air resistance so drag exceeds weight; the resultant force is upwards, causing deceleration until a new, lower terminal velocity is reached.', 'drag increases (larger area) [1]; drag > weight so deceleration [1]; lower terminal velocity [1] [3]'),
    ('Describe the velocity-time graph for a ball thrown vertically upwards and caught at the same level, ignoring air resistance.', 'A straight line of constant negative gradient (−g), crossing the time axis at the top of the flight; the final velocity is equal in magnitude and opposite in direction to the initial velocity.', 'straight line gradient −g [1]; crosses axis at top; symmetrical [1] [2]'),
    ('Explain how air resistance changes the velocity-time graph of a falling ball.', 'The gradient starts at g but decreases as speed increases (curve that flattens), approaching a constant terminal velocity.', 'gradient decreases [1]; levels off at terminal velocity [1] [2]'),
    ('Explain why the acceleration of a falling object is independent of its mass when air resistance is negligible.', 'a = F/m = mg/m = g; both the weight and the inertia are proportional to mass.', 'weight ∝ m [1]; a = mg/m = g [1] [2]'),
])


@t32.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t32_up(r, D):
    u = r.choice([8.0, 10.0, 12.0, 14.0, 15.0, 18.0, 20.0, 24.0])
    thing = r.choice(['a ball', 'a stone', 'a tennis ball', 'a small rocket (after its motor stops)', 'a coin'])
    s = f'{cap(thing)} is projected vertically upwards at {nf(u)} m s⁻¹. Air resistance is negligible.'
    H = u * u / (2 * GR); tup = u / GR
    if D <= 2:
        k = r.choice(['H', 't'])
        if k == 'H':
            return numq(r, D, s, 'maximum height reached', H, ' m', f'h = u²/(2g) = {nf(u)}²/(2 × 9.81)', [u * u / GR, u / GR, u * u / 9.81 / 4], fm=lambda x: nf(x, 3))
        return numq(r, D, s, 'time taken to reach maximum height', tup, ' s', f't = u/g = {nf(u)}/9.81', [2 * tup, u * GR / 100, tup / 2], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the maximum height and the total time before it returns to the point of projection.', f'{nf(H, 3)} m; {nf(2 * tup, 3)} s',
                 f'0 = u² − 2gh → h = {nf(H, 3)} m [1]; t up = {nf(tup, 3)} s [1]; total = {nf(2 * tup, 3)} s [1] [3]')
    h0 = r.choice([10.0, 15.0, 20.0, 25.0, 30.0])
    # -h0 = u t - 0.5 g t^2  -> 0.5 g t^2 - u t - h0 = 0
    t = (u + math.sqrt(u * u + 2 * GR * h0)) / GR
    vimp = math.sqrt(u * u + 2 * GR * h0)
    return Q(f'{cap(thing)} is projected vertically upwards at {nf(u)} m s⁻¹ from the edge of a cliff {nf(h0)} m above the sea. Air resistance is negligible. (a) Calculate the time taken to reach the sea. (b) Calculate the speed with which it hits the sea.',
             f'(a) {nf(t, 3)} s (b) {nf(vimp, 3)} m s⁻¹',
             f'(a) taking up as positive: −{nf(h0)} = {nf(u)}t − 4.905t² [1]; solve quadratic [1]; t = {nf(t, 3)} s [1] (b) v² = {nf(u)}² + 2 × 9.81 × {nf(h0)} [1]; v = {nf(vimp, 3)} m s⁻¹ [1] [5]', 'multi_step')


@t32.add('C3', (1, 2, 3, 4), 'numerical')
def t32_drop(r, D):
    h = r.choice([5.0, 8.0, 12.0, 20.0, 30.0, 45.0, 80.0])
    thing = r.choice(['a stone falls from rest down a well', 'a ball is dropped from a balcony', 'a coin is released from rest at the top of a tower', 'a parcel falls from rest from a stationary helicopter'])
    t = math.sqrt(2 * h / GR); v = math.sqrt(2 * GR * h)
    if D <= 2:
        return numq(r, D, f'{cap(thing)} through a height of {nf(h)} m. Air resistance is negligible.', 'time of fall', t, ' s', f't = √(2h/g) = √(2 × {nf(h)}/9.81)', [h / GR, 2 * h / GR, math.sqrt(h / GR)], fm=lambda x: nf(x, 3))
    snd = 330
    tt = t + h / snd
    return Q(f'{cap(thing)}. The sound of it landing is heard {nf(tt, 3)} s after release. Taking the speed of sound as {snd} m s⁻¹ and ignoring air resistance, show that the height is about {nf(h, 2)} m' + (' and explain why ignoring the time for the sound gives an overestimate of the height.' if D >= 4 else '.'),
             f'h = {nf(h, 3)} m' + ('; ignoring sound time makes the fall time too long, so ½gt² is too large.' if D >= 4 else ''),
             f'tfall + h/{snd} = {nf(tt, 3)} [1]; with tfall = √(2h/g), h = {nf(h, 3)} m satisfies this (or trial values) [1]; check [1]' + (' ; overestimate explanation [1] [4]' if D >= 4 else ' [3]'))


@t32.add('C2', (2, 3, 4), 'explain')
def t32_compare(r, D):
    a, b = r.sample(['a steel ball bearing', 'a table-tennis ball', 'a sheet of paper', 'a crumpled ball of paper', 'a coin', 'a feather', 'a marble', 'a balloon'], 2)
    h = r.choice([2.0, 3.0, 5.0, 10.0])
    return Q(f'{cap(a)} and {b} are released together from a height of {nf(h)} m in air. Explain whether they reach the ground at the same time, and what would happen in a vacuum.',
             'In air the object with the greater weight compared with its air resistance (larger mass per unit area) has the greater acceleration and lands first; in a vacuum both fall with acceleration g and land together.',
             'air resistance relative to weight decides acceleration [1]; correct object lands first [1]; vacuum: same acceleration g [1] [3]')


def _grav_c4(r, D):
    m = r.choice([60, 70, 75, 80, 90]); vt = r.choice([50, 55, 60]); vt2 = r.choice([5, 6, 7])
    intro = r.choice([f'A skydiver of mass {m} kg jumps from a hovering helicopter above {city(r)}. She reaches a terminal velocity of {vt} m s⁻¹ before opening her parachute, after which her new terminal velocity is {vt2} m s⁻¹.',
                      f'A skydiver of total mass {m} kg falls from rest, reaching {vt} m s⁻¹ terminal velocity; after the parachute opens the terminal velocity is {vt2} m s⁻¹.'])
    W = m * GR
    parts = [
        lambda r: ('Calculate the weight of the skydiver.', f'{nf(W, 3)} N', 'W = mg [1]'),
        lambda r: ('State the acceleration at the instant of leaving the helicopter, giving a reason.', '9.81 m s⁻²: the speed is zero so there is no air resistance; only weight acts.', 'g [1]; no drag at zero speed [1] [2]'),
        lambda r: ('State the air resistance at terminal velocity.', f'{nf(W, 3)} N (equal to weight)', 'equal to weight [1]'),
        lambda r: ('Explain why the skydiver decelerates when the parachute opens.', 'Drag increases suddenly (larger area) above the weight; resultant force upwards causes deceleration.', 'drag > weight [1]; resultant upwards [1] [2]'),
        lambda r: ('Sketch the velocity-time graph from leaving the helicopter to landing.', f'curve rising with decreasing gradient to {vt} m s⁻¹; sharp drop when parachute opens; curve levelling at {vt2} m s⁻¹', 'curve to first terminal velocity [1]; drop to lower terminal velocity [1] [2]'),
        lambda r: ('Explain why the equations of uniformly accelerated motion cannot be used for the fall.', 'The acceleration is not constant because drag changes with speed.', 'acceleration not constant [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t32.add('C4', (2, 3, 4, 5), 'multi_step')(_grav_c4)

N33 = 'Projectile motion: independent horizontal and vertical components'
t33 = topic(N33, N33.lower(), 'projectile motion', 'horizontal and vertical components')
FX(t33, 'C1', (1, 2), [
    ('A ball is thrown horizontally from a cliff. Ignoring air resistance, which quantity stays constant during its flight?', 'The horizontal component of velocity', 'No horizontal force acts, so horizontal velocity is constant.', ['The vertical component of velocity', 'The speed', 'The kinetic energy']),
    ('Two balls are released at the same time from the same height: one is dropped and the other is projected horizontally. Ignoring air resistance,', 'they hit the ground at the same time', 'Vertical motion is independent of horizontal motion; both start with zero vertical velocity.', ['the dropped ball lands first', 'the projected ball lands first', 'the faster ball has a greater vertical acceleration']),
    ('A projectile is launched at 20 m s⁻¹ at 30° above the horizontal. What is the initial vertical component of velocity?', '10 m s⁻¹', 'u sin θ = 20 × sin 30° = 10 m s⁻¹.', ['17 m s⁻¹', '20 m s⁻¹', '5.0 m s⁻¹']),
    ('At the highest point of the path of a projectile (no air resistance), which is correct?', 'The vertical velocity is zero and the acceleration is g downwards', 'At the top v_y = 0 but the horizontal velocity and the acceleration g remain.', ['The velocity is zero', 'The acceleration is zero', 'The horizontal velocity is zero']),
    ('Ignoring air resistance, which launch angle gives the maximum range on level ground?', '45°', 'R = u² sin 2θ/g is greatest when 2θ = 90°.', ['30°', '60°', '90°']),
    ('What is the shape of the path of a projectile when air resistance is negligible?', 'A parabola', 'Constant horizontal velocity with uniform vertical acceleration gives a parabolic path.', ['A circle', 'A straight line', 'A hyperbola']),
    ('State why the horizontal and vertical motions of a projectile can be treated separately.', 'Perpendicular components are independent: the vertical force (weight) has no horizontal component.', 'perpendicular components independent [1]'),
])
FX(t33, 'C2', (1, 2, 3, 4), [
    ('Explain why the path of a projectile is curved.', 'The horizontal velocity is constant but the vertical velocity increases uniformly downwards due to g, so the direction of motion continuously changes.', 'constant horizontal velocity [1]; vertical velocity changes due to g [1] [2]'),
    ('Explain how air resistance affects the range and maximum height of a projectile.', 'Air resistance opposes the motion, reducing both components of velocity; the maximum height and the range are both reduced and the path is no longer symmetrical (steeper descent).', 'both reduced [1]; path asymmetric/steeper descent [1] [2]'),
    ('Explain why a bullet fired horizontally and one dropped from the same height at the same instant hit level ground together.', 'Both have zero initial vertical velocity and the same vertical acceleration g, so they take the same time to fall the same height; horizontal velocity does not affect vertical motion.', 'same initial vertical velocity (zero) and same g [1]; independence of components [1] [2]'),
    ('Explain why launch angles of 30° and 60° give the same range on level ground (no air resistance).', 'Range = u² sin 2θ / g and sin 60° = sin 120°, so both give the same range; the 60° launch goes higher and takes longer but moves more slowly horizontally.', 'sin 2θ equal for complementary angles [1]; trade-off of time and horizontal speed [1] [2]'),
    ('Describe how the velocity of a projectile changes from launch to its highest point.', 'The horizontal component is constant; the vertical component decreases uniformly to zero, so the speed decreases to a minimum (equal to the horizontal component) and the direction becomes horizontal.', 'horizontal constant [1]; vertical decreases to zero; minimum speed at top [1] [2]'),
])


@t33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t33_horiz(r, D):
    h = r.choice([1.2, 1.8, 2.5, 5.0, 10.0, 20.0, 45.0]); u = r.choice([3.0, 4.0, 5.0, 8.0, 12.0, 15.0, 25.0])
    thing = r.choice(['A ball rolls off a horizontal table', 'A stone is thrown horizontally from a bridge', 'A dart is thrown horizontally', 'A parcel is released from a drone moving horizontally', 'Water leaves a horizontal hosepipe'])
    t = math.sqrt(2 * h / GR); R = u * t; vy = GR * t; v = math.hypot(u, vy)
    s = f'{thing} at {nf(u)} m s⁻¹ from a height of {nf(h)} m above level ground. Air resistance is negligible.'
    if D <= 2:
        return numq(r, D, s, 'time taken to reach the ground', t, ' s', f'h = ½gt² → t = √(2 × {nf(h)}/9.81)', [h / u, 2 * h / GR, math.sqrt(h / GR)], fm=lambda x: nf(x, 3))
    if D == 3:
        return Q(s + ' Calculate the horizontal distance travelled before it hits the ground.', f'{nf(R, 3)} m', f't = √(2h/g) = {nf(t, 3)} s [1]; horizontal velocity constant [1]; x = ut = {nf(R, 3)} m [1] [3]')
    return Q(s + ' (a) Calculate the horizontal distance travelled. (b) Calculate the speed and the angle below the horizontal at which it hits the ground.',
             f'(a) {nf(R, 3)} m (b) {nf(v, 3)} m s⁻¹ at {nf(math.degrees(math.atan2(vy, u)), 3)}° below the horizontal',
             f'(a) t = {nf(t, 3)} s [1]; x = {nf(R, 3)} m [1] (b) vy = gt = {nf(vy, 3)} m s⁻¹ [1]; v = √(u² + vy²) = {nf(v, 3)} m s⁻¹ [1]; tan⁻¹(vy/u) = {nf(math.degrees(math.atan2(vy, u)), 3)}° [1] [5]', 'multi_step')


@t33.add('C3', (2, 3, 4, 5), 'numerical')
def t33_angle(r, D):
    u = r.choice([12.0, 15.0, 18.0, 20.0, 25.0, 30.0]); th = r.choice([25, 30, 35, 40, 50, 55, 60])
    thing = r.choice(['A footballer kicks a ball', 'A golf ball is struck', 'A shot is put', 'A water jet leaves a fountain nozzle', 'A javelin is thrown'])
    ux = u * math.cos(math.radians(th)); uy = u * math.sin(math.radians(th))
    T = 2 * uy / GR; H = uy * uy / (2 * GR); R = ux * T
    s = f'{thing} from ground level at {nf(u)} m s⁻¹ at {th}° above the horizontal. Air resistance is negligible and the ground is level.'
    if D == 2:
        return Q(s + ' Calculate the horizontal and vertical components of the initial velocity.', f'{nf(ux, 3)} m s⁻¹ horizontally, {nf(uy, 3)} m s⁻¹ vertically', f'u cos θ = {nf(ux, 3)} m s⁻¹ [1]; u sin θ = {nf(uy, 3)} m s⁻¹ [1] [2]')
    if D == 3:
        return Q(s + ' Calculate the maximum height reached.', f'{nf(H, 3)} m', f'uy = {nf(uy, 3)} m s⁻¹ [1]; 0 = uy² − 2gH [1]; H = {nf(H, 3)} m [1] [3]')
    if D == 4:
        return Q(s + ' Calculate the time of flight and the range.', f'{nf(T, 3)} s; {nf(R, 3)} m', f'uy = {nf(uy, 3)} m s⁻¹ [1]; T = 2uy/g = {nf(T, 3)} s [1]; ux = {nf(ux, 3)} m s⁻¹ [1]; R = ux T = {nf(R, 3)} m [1] [4]')
    th2 = 90 - th
    return Q(s + f' (a) Calculate the range. (b) Show that a launch at {th2}° with the same speed gives the same range, and state one difference between the two paths.',
             f'(a) {nf(R, 3)} m (b) R = u² sin 2θ/g and sin {2 * th}° = sin {2 * th2}°, so same range; the {max(th, th2)}° path is higher and takes longer.',
             f'(a) components [1]; time of flight {nf(T, 3)} s [1]; range {nf(R, 3)} m [1] (b) equal sin 2θ shown [1]; difference in height/time [1] [5]', 'multi_step')


def _proj_c4(r, D):
    u = r.choice([14.0, 16.0, 20.0, 22.0]); th = r.choice([30, 35, 40, 45]); h = r.choice([1.5, 2.0, 2.5])
    ux = u * math.cos(math.radians(th)); uy = u * math.sin(math.radians(th))
    t = (uy + math.sqrt(uy * uy + 2 * GR * h)) / GR
    intro = r.choice([f'An athlete in {city(r)} releases a shot at a height of {nf(h)} m above level ground with a speed of {nf(u)} m s⁻¹ at {th}° above the horizontal.',
                      f'A ball is thrown from a height of {nf(h)} m above level ground at {nf(u)} m s⁻¹ and {th}° above the horizontal by {person(r)}.'])
    parts = [
        lambda r: ('Calculate the initial horizontal and vertical components of the velocity.', f'{nf(ux, 3)} m s⁻¹ and {nf(uy, 3)} m s⁻¹', 'u cos θ and u sin θ [2]'),
        lambda r: ('Calculate the maximum height above the ground.', f'{nf(h + uy * uy / (2 * GR), 3)} m', f'uy²/(2g) = {nf(uy * uy / (2 * GR), 3)} m, add {nf(h)} m [2]'),
        lambda r: ('Calculate the time of flight.', f'{nf(t, 3)} s', f'−{nf(h)} = {nf(uy, 3)}t − 4.905t² solved [3]'),
        lambda r: ('Calculate the horizontal distance travelled.', f'{nf(ux * t, 3)} m', f'x = ux t [1]'),
        lambda r: ('State the speed of the projectile at its highest point.', f'{nf(ux, 3)} m s⁻¹', 'vertical component zero; speed = horizontal component [1]'),
        lambda r: ('Explain how the range would change if air resistance were significant.', 'The range would be smaller because air resistance reduces the horizontal velocity (and the height reached).', 'smaller range [1]; horizontal velocity reduced [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t33.add('C4', (2, 3, 4, 5), 'multi_step')(_proj_c4)

CHAPTERS[3] = [t31, t32, t33]


# ===================================================================== 4 Dynamics
N41 = "Newton's laws of motion and F = ma, mass as resistance to change in velocity"
t41 = topic(N41, N41.lower(), "newton's laws", 'f = ma')
FX(t41, 'C1', (1, 2), [
    ("Which statement is Newton's first law?", 'An object remains at rest or moves with constant velocity unless acted on by a resultant force', 'First law: no resultant force → no change in velocity.',
     ['Every action has an equal and opposite reaction', 'Force equals mass times acceleration', 'An object always moves in the direction of the largest force']),
    ('A resultant force of 12 N acts on a mass of 3.0 kg. What is the acceleration?', '4.0 m s⁻²', 'a = F/m = 12/3.0 = 4.0 m s⁻².', ['36 m s⁻²', '0.25 m s⁻²', '9.0 m s⁻²']),
    ('The property of an object that resists changes to its velocity is its', 'mass', 'Mass is a measure of inertia.', ['weight', 'momentum', 'speed']),
    ("Newton's third law pairs of forces", 'act on different objects and are of the same type', 'N3 pairs: equal magnitude, opposite direction, same type, on different bodies.',
     ['act on the same object and cancel out', 'are always gravitational', 'are of different types, such as weight and normal contact force']),
    ('A book rests on a table. Which force forms a Newton\'s third law pair with the weight of the book?', 'The gravitational pull of the book on the Earth', 'Weight is the Earth pulling the book; its pair is the book pulling the Earth (both gravitational).',
     ['The normal contact force of the table on the book', 'The weight of the table', 'The friction on the book']),
    ('Which unit is equivalent to the newton?', 'kg m s⁻²', 'F = ma.', ['kg m s⁻¹', 'kg m² s⁻²', 'kg s m⁻¹']),
    ('A car of mass 1200 kg accelerates at 2.5 m s⁻². What resultant force acts on it?', '3000 N', 'F = ma = 1200 × 2.5.', ['480 N', '1202.5 N', '12 000 N']),
    ("State Newton's second law of motion.", 'The resultant force on an object is proportional to its rate of change of momentum (F = ma for constant mass).', 'resultant force ∝ rate of change of momentum / F = ma [1]'),
])
FX(t41, 'C2', (1, 2, 3, 4), [
    ('Explain why a passenger in a bus lurches forward when the bus brakes suddenly.', 'The passenger has inertia and tends to continue moving at the original velocity (first law); the brakes act on the bus, not directly on the passenger, until the seat or belt provides a force.', 'inertia / first law [1]; no force on passenger initially to decelerate them [1] [2]'),
    ('Explain why the normal contact force on a book on a table is not the Newton\'s third law pair of its weight.', 'The two forces act on the same object (the book) and are of different types (contact and gravitational); a third law pair acts on different objects and is the same type.', 'same object [1]; different types [1] [2]'),
    ('Explain what is meant by saying that mass is a measure of an object\'s resistance to changes in velocity.', 'For a given resultant force, a = F/m, so a larger mass gives a smaller acceleration: the velocity changes less quickly.', 'a = F/m [1]; larger mass → smaller acceleration for same force [1] [2]'),
    ('A rocket in deep space with its engine off continues to move. Explain why no force is needed to keep it moving.', 'By Newton\'s first law a body moves with constant velocity unless a resultant force acts; with no drag or gravity, no force is needed to maintain the velocity.', 'first law [1]; force needed only to change velocity [1] [2]'),
    ('Explain how a rocket engine produces a forward force on the rocket.', 'The engine pushes exhaust gas backwards (giving it momentum); by Newton\'s third law the gas pushes the rocket forwards with an equal force.', 'force on gas backwards [1]; equal and opposite force on rocket (N3) [1] [2]'),
])


@t41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t41_fma(r, D):
    obj = r.choice([('a car', [900, 1100, 1200, 1500]), ('a lorry', [8000, 12000, 15000]), ('a trolley', [0.50, 0.80, 1.2, 2.0]), ('a cyclist and bicycle', [75, 80, 90]), ('a train', [40000, 60000, 80000]), ('a sledge', [20, 25, 40])])
    name, ms = obj
    m = r.choice(ms)
    a = r.choice([0.25, 0.40, 0.50, 0.80, 1.2, 1.5, 2.0, 2.5])
    F = m * a
    k = r.choice(['F', 'a', 'm'])
    if D <= 2:
        if k == 'F':
            return numq(r, D, f'{cap(name)} of mass {nf(m)} kg accelerates at {nf(a)} m s⁻².', 'resultant force on it', F, ' N', f'F = ma = {nf(m)} × {nf(a)}', [m / a, m * GR, m + a], fm=f3)
        if k == 'a':
            return numq(r, D, f'A resultant force of {f3(F)} N acts on {name} of mass {nf(m)} kg.', 'acceleration', a, ' m s⁻²', f'a = F/m = {f3(F)}/{nf(m)}', [F * m / 1e4, m / F, a * GR], fm=f3)
        return numq(r, D, f'A resultant force of {f3(F)} N gives {name} an acceleration of {nf(a)} m s⁻².', 'mass', m, ' kg', f'm = F/a = {f3(F)}/{nf(a)}', [F * a, F / GR, a / F * 1e4], fm=f3)
    Rf = round(F * r.choice([0.2, 0.25, 0.4, 0.5]), 3)
    Fd = F + Rf
    u = r.choice([0, 2.0, 4.0, 5.0]); t = r.choice([4.0, 5.0, 6.0, 8.0])
    v = u + a * t
    if D == 3:
        return Q(f'{cap(name)} of mass {nf(m)} kg is pulled by a driving force of {f3(Fd)} N against a total resistive force of {f3(Rf)} N. Calculate the acceleration.', f'{nf(a, 3)} m s⁻²',
                 f'resultant = {f3(Fd)} − {f3(Rf)} = {f3(F)} N [1]; a = F/m [1]; = {nf(a, 3)} m s⁻² [1] [3]')
    return Q(f'{cap(name)} of mass {nf(m)} kg moving at {nf(u)} m s⁻¹ experiences a driving force of {f3(Fd)} N and a resistive force of {f3(Rf)} N for {nf(t)} s. (a) Calculate the acceleration. (b) Calculate the final speed. (c) Calculate the distance travelled in this time.',
             f'(a) {nf(a, 3)} m s⁻² (b) {nf(v, 3)} m s⁻¹ (c) {nf(u * t + 0.5 * a * t * t, 3)} m',
             f'(a) resultant {f3(F)} N [1]; a = {nf(a, 3)} m s⁻² [1] (b) v = u + at = {nf(v, 3)} m s⁻¹ [1] (c) s = ut + ½at² = {nf(u * t + 0.5 * a * t * t, 3)} m [1]' + (' [4]' if D == 4 else '; assumption that forces are constant [1] [5]'), 'multi_step')


N3PAIRS = [('the Earth pulls a satellite towards it', 'the satellite pulls the Earth towards it with an equal gravitational force'),
           ('a swimmer pushes water backwards', 'the water pushes the swimmer forwards'),
           ('a hammer hits a nail', 'the nail exerts an equal force back on the hammer'),
           ('a car tyre pushes backwards on the road', 'the road pushes forwards on the tyre (friction)'),
           ('a magnet attracts an iron nail', 'the nail attracts the magnet with an equal magnetic force'),
           ('a person leans against a wall', 'the wall pushes back on the person with an equal contact force'),
           ('a gun pushes a bullet forwards', 'the bullet pushes the gun backwards (recoil)')]


@t41.add('C2', (2, 3, 4), 'explain')
def t41_n3(r, D):
    a, b = r.choice(N3PAIRS)
    who = person(r)
    return Q(f'Describe the Newton\'s third law pair force when {a}. {who} says the two forces cancel. Explain why {who} is wrong.',
             f'The pair force: {b}. They act on different objects, so they cannot cancel; each affects the motion of the object it acts on.',
             'pair force described with same type and magnitude [1]; acts on different object [1]; so cannot cancel [1] [3]')


relation(t41, 'C2', (2, 3), 'a = F/m', 'acceleration', {'resultant force': 1, 'mass': -1},
         ['A trolley is pulled along a smooth bench by a constant force.', 'A rocket sled is driven along a frictionless track by its engine.', 'An ice-hockey puck is struck and then pushed by a constant force on smooth ice.'])


def _n2_c4(r, D):
    m1 = r.choice([1200, 1500, 1800]); m2 = r.choice([400, 600, 800]); F = r.choice([2400, 3000, 3600, 4200]); Rf = r.choice([200, 300, 400])
    a = (F - Rf) / (m1 + m2); T = m2 * a + Rf * m2 / (m1 + m2)
    intro = r.choice([f'A car of mass {m1} kg tows a trailer of mass {m2} kg along a straight, level road in {city(r)}. The driving force from the car is {F} N and the total resistive force on car and trailer is {Rf} N, shared in proportion to their masses.',
                      f'A tractor of mass {m1} kg pulls a cart of mass {m2} kg on a level track with a driving force of {F} N. Resistive forces total {Rf} N and are shared in proportion to mass.'])
    parts = [
        lambda r: ('Calculate the acceleration of the system.', f'{nf(a, 3)} m s⁻²', f'a = ({F} − {Rf})/({m1} + {m2}) [2]'),
        lambda r: ('Calculate the tension in the tow bar.', f'{nf(T, 3)} N', f'for trailer: T − {nf(Rf * m2 / (m1 + m2), 3)} = {m2} × {nf(a, 3)} [3]'),
        lambda r: ("State Newton's third law and apply it to the tow bar.", 'If A exerts a force on B, B exerts an equal and opposite force of the same type on A: the bar pulls the trailer forwards and the trailer pulls the car backwards with equal force.', 'statement [1]; application [1] [2]'),
        lambda r: ('Explain why the acceleration is less when the trailer is loaded with more mass.', 'For the same resultant force, a = F/m; a larger total mass gives a smaller acceleration.', 'a = F/m [1]; larger mass [1] [2]'),
        lambda r: ('State what happens to the motion if the driving force becomes equal to the resistive force.', 'The resultant force is zero, so the system moves at constant velocity (first law).', 'constant velocity [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t41.add('C4', (2, 3, 4, 5), 'multi_step')(_n2_c4)

N42 = 'Weight, friction, drag and terminal velocity'
t42 = topic(N42, N42.lower(), 'weight friction drag', 'terminal velocity')
FX(t42, 'C1', (1, 2), [
    ('Which is the correct expression for the weight of an object of mass m?', 'mg', 'Weight = mass × gravitational field strength.', ['m/g', 'mg²', 'm + g']),
    ('What is the weight of a 65 kg astronaut on Earth?', '638 N', 'W = 65 × 9.81 = 638 N.', ['65 N', '6.6 N', '6380 N']),
    ('Which statement about drag force on an object moving through a fluid is correct?', 'It increases as the speed of the object increases', 'Drag depends on speed (often ∝ v²), shape and the fluid.', ['It is independent of speed', 'It acts in the direction of motion', 'It only acts in liquids']),
    ('At terminal velocity, the resultant force on a falling object is', 'zero', 'Drag (plus upthrust) equals weight, so acceleration is zero.', ['equal to its weight', 'equal to twice its weight', 'directed downwards and decreasing']),
    ('Friction between two surfaces always acts', 'to oppose relative motion (or the tendency to move) between the surfaces', 'Friction opposes relative sliding.', ['in the direction of motion', 'perpendicular to the surfaces', 'only when the object is stationary']),
    ('The mass of an object is 4.0 kg on Earth. What is its mass on the Moon?', '4.0 kg', 'Mass does not depend on location; weight does.', ['0.67 kg', '6.5 kg', '24 kg']),
    ('State the difference between mass and weight.', 'Mass is the amount of matter (resistance to acceleration), a scalar in kg; weight is the gravitational force on it, a vector in N.', 'mass: matter/inertia scalar [1]; weight: gravitational force [1] [2]'),
])
FX(t42, 'C2', (1, 2, 3, 4), [
    ('A ball-bearing is released in a tall tube of oil. Describe and explain its motion.', 'It accelerates initially; as speed increases, viscous drag increases, reducing the resultant force and acceleration; when drag + upthrust = weight, it moves at constant terminal velocity.', 'initial acceleration [1]; drag increases with speed [1]; terminal velocity when forces balance [1] [3]'),
    ('Explain why a car reaches a top speed even though the engine still provides a driving force.', 'Air resistance and other resistive forces increase with speed; at top speed they equal the driving force so the resultant force and acceleration are zero.', 'resistive forces increase with speed [1]; equal driving force → zero resultant [1] [2]'),
    ('Explain why a skydiver in a head-down position has a higher terminal velocity than one spread out horizontally.', 'A smaller cross-sectional area gives less drag at a given speed, so the speed must be higher before drag equals weight.', 'smaller area, less drag [1]; higher speed needed to balance weight [1] [2]'),
    ('Explain why the weight of an astronaut is less on the Moon although the mass is unchanged.', 'Weight = mg; g on the Moon (about 1.6 N kg⁻¹) is smaller than on Earth, while mass (amount of matter) does not depend on location.', 'W = mg with smaller g [1]; mass unchanged [1] [2]'),
    ('Explain why a cyclist free-wheeling down a slope reaches a constant speed.', 'The component of weight down the slope is constant but air resistance increases with speed until it (plus friction) equals that component; then the resultant force is zero.', 'weight component constant [1]; drag increases to balance it [1] [2]'),
])


@t42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t42_term(r, D):
    thing, m, vt0 = r.choice([('a hailstone', r.choice([0.0020, 0.0040, 0.0080]), 20), ('a table-tennis ball', 0.0027, 9), ('a shuttlecock', 0.0050, 6.5), ('a model parachute', r.choice([0.050, 0.080, 0.12]), 4),
                              ('a plastic sphere', r.choice([0.012, 0.020, 0.050]), 15), ('a golf ball', 0.046, 40), ('a tennis ball', 0.057, 25)])
    W = m * GR
    k = float(sci(W / (vt0 * r.choice([0.9, 1.0, 1.1, 1.2])) ** 2, 2).replace(' × 10', 'e').translate(str.maketrans('⁻⁰¹²³⁴⁵⁶⁷⁸⁹', '-0123456789')))
    vt = math.sqrt(W / k)
    s = f'{cap(thing)} of mass {f3(m)} kg falls through air. The drag force is given by F = kv² where k = {sci(k, 2)} kg m⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'terminal velocity', vt, ' m s⁻¹', f'at terminal velocity kv² = mg → v = √(mg/k) = √({f3(W)}/{sci(k, 2)})', [W / k, math.sqrt(m / k), vt * vt / 10], fm=f3)
    v = vt * r.choice([0.4, 0.5, 0.6, 0.7])
    a = (W - k * v * v) / m
    if D == 3:
        return Q(s + f' Calculate its acceleration when its speed is {f3(v)} m s⁻¹.', f'{f3(a)} m s⁻²', f'drag = kv² = {f3(k * v * v)} N [1]; resultant = {f3(W)} − {f3(k * v * v)} N [1]; a = F/m = {f3(a)} m s⁻² [1] [3]')
    return Q(s + f' (a) Calculate its terminal velocity. (b) Calculate its acceleration when its speed is {f3(v)} m s⁻¹. (c) Explain why its acceleration decreases as it falls.',
             f'(a) {f3(vt)} m s⁻¹ (b) {f3(a)} m s⁻² (c) drag increases with speed, so the resultant force decreases.',
             f'(a) kv² = mg [1]; v = {f3(vt)} m s⁻¹ [1] (b) resultant force = {f3(W - k * v * v)} N [1]; a = {f3(a)} m s⁻² [1] (c) drag ∝ v² increases, resultant decreases [1] [5]', 'multi_step')


@t42.add('C3', (1, 2, 3, 4), 'numerical')
def t42_fric(r, D):
    m = r.choice([5.0, 8.0, 10.0, 15.0, 20.0, 25.0]); F = r.choice([30, 40, 50, 60, 80]); fr = r.choice([10, 12, 15, 20, 25])
    if fr >= F:
        fr = F / 2
    a = (F - fr) / m
    s = r.choice([f'A box of mass {nf(m)} kg is pushed across a warehouse floor with a horizontal force of {F} N. The friction force is {nf(fr)} N.', f'{person(r)} drags a crate of mass {nf(m)} kg with a horizontal rope tension of {F} N against friction of {nf(fr)} N.'])
    if D <= 2:
        return numq(r, D, s, 'acceleration of the box', a, ' m s⁻²', f'a = ({F} − {nf(fr)})/{nf(m)}', [F / m, (F + fr) / m, (F - fr) * m / 100], fm=f3)
    t = r.choice([2.0, 3.0, 4.0])
    v = a * t
    dec = fr / m
    return Q(s + f' The box starts from rest and the push lasts {nf(t)} s, after which only friction acts. Calculate the maximum speed and the further distance travelled before the box stops.',
             f'{f3(v)} m s⁻¹; {f3(v * v / (2 * dec))} m', f'a = {f3(a)} m s⁻² [1]; v = at = {f3(v)} m s⁻¹ [1]; deceleration = {nf(fr)}/{nf(m)} = {f3(dec)} m s⁻² [1]; s = v²/2a = {f3(v * v / (2 * dec))} m [1] [4]')


@t42.add('C2', (2, 3, 4), 'explain')
def t42_planet(r, D):
    pl = r.choice([('the Moon', 1.62), ('Mars', 3.71), ('Jupiter', 24.8), ('Venus', 8.87), ('Mercury', 3.70)])
    m = r.choice([50, 60, 70, 80, 100])
    return Q(f'A rover of mass {m} kg is weighed on Earth and then on {pl[0]}, where g = {pl[1]} N kg⁻¹. State its mass and weight in each place and explain the difference.',
             f'Mass {m} kg in both places; weight {nf(m * GR, 3)} N on Earth and {nf(m * pl[1], 3)} N on {pl[0]}. Mass is the quantity of matter; weight = mg depends on the local field strength.',
             f'mass unchanged [1]; both weights correct [1]; explanation W = mg depends on g [1] [3]')


def _drag_c4(r, D):
    m = r.choice([0.020, 0.040, 0.060]); vt = r.choice([4.0, 5.0, 6.0, 8.0])
    k = m * GR / vt ** 2
    intro = r.choice([f'A small sphere of mass {f3(m)} kg is dropped from a tall building in {city(r)}. Its terminal velocity in air is {nf(vt)} m s⁻¹, and the drag force is proportional to v².',
                      f'A model parachute of mass {f3(m)} kg is released from rest. It reaches a terminal velocity of {nf(vt)} m s⁻¹; drag ∝ v².'])
    parts = [
        lambda r: ('Calculate the drag force at terminal velocity.', f'{f3(m * GR)} N', 'drag = weight = mg [1]'),
        lambda r: ('Determine the constant k in F = kv².', f'{sci(k, 3)} kg m⁻¹', f'k = mg/v² [2]'),
        lambda r: (f'Calculate the acceleration when the speed is {nf(vt / 2)} m s⁻¹.', f'{f3(GR * 0.75)} m s⁻²', f'drag = ¼ weight so resultant = ¾mg; a = 0.75g [2]'),
        lambda r: ('Sketch the acceleration-time graph from release.', 'Starts at 9.81 m s⁻² and decreases (curving) towards zero.', 'starts at g [1]; decreases to zero [1] [2]'),
        lambda r: ('Explain why a heavier object of the same size and shape has a greater terminal velocity.', 'It needs a larger drag force to balance its larger weight, which requires a higher speed.', 'larger weight to balance [1]; higher speed needed [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t42.add('C4', (2, 3, 4, 5), 'multi_step')(_drag_c4)

N43 = 'Free-body diagrams and resultant force in one dimension'
t43 = topic(N43, N43.lower(), 'free-body diagrams', 'resultant force')
FX(t43, 'C1', (1, 2), [
    ('What does a free-body diagram show?', 'All the forces acting on one object', 'A free-body diagram isolates one object and shows every force acting on it.', ['All the forces the object exerts on other objects', 'Only the resultant force', 'The forces acting on all objects in a system']),
    ('A lift of mass 800 kg accelerates upwards at 1.5 m s⁻². What is the tension in the cable?', '9050 N', 'T − mg = ma: T = 800(9.81 + 1.5) = 9050 N.', ['7850 N', '1200 N', '6650 N']),
    ('A person stands on scales in a lift that is moving upwards at constant velocity. The scales read', 'the person\'s true weight', 'Constant velocity: zero acceleration, so normal force = weight.', ['more than the weight', 'less than the weight', 'zero']),
    ('A box of weight 50 N is pulled up at constant velocity by a rope. What is the tension?', '50 N', 'Constant velocity: resultant force zero, T = W.', ['0 N', 'more than 50 N', 'less than 50 N']),
    ('Forces of 20 N to the right and 35 N to the left act on a block. What is the resultant force?', '15 N to the left', 'Resultant = 35 − 20 = 15 N towards the larger force.', ['55 N to the left', '15 N to the right', '55 N to the right']),
    ('State the condition for an object to be moving at constant velocity.', 'The resultant force on it is zero.', 'resultant force zero [1]'),
])
FX(t43, 'C2', (1, 2, 3, 4), [
    ('Explain why a person in a lift feels heavier as the lift starts to move upwards.', 'The floor must provide a resultant upward force to accelerate the person, so the normal contact force is greater than the weight; the person feels this larger contact force.', 'upward acceleration needs resultant upward force [1]; normal force > weight [1] [2]'),
    ('Draw and describe the free-body diagram for a parachutist falling at terminal velocity.', 'Two forces: weight downwards and drag (air resistance) upwards, of equal length.', 'weight down and drag up [1]; equal magnitude [1] [2]'),
    ('Explain why the normal contact force on a box on a slope is less than its weight.', 'The normal force balances only the component of weight perpendicular to the slope, W cos θ, which is less than W.', 'balances perpendicular component [1]; W cos θ < W [1] [2]'),
    ('A student draws a free-body diagram for a ball in flight showing a "force of the throw". Explain the error.', 'Once the ball leaves the hand, no force from the throw acts; only weight (and air resistance) act. The ball continues moving because of its inertia.', 'no throw force after release [1]; only weight (and drag); motion from inertia [1] [2]'),
])


@t43.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t43_lift(r, D):
    m = r.choice([500, 650, 800, 1000, 1200]); a = r.choice([0.50, 0.80, 1.0, 1.2, 1.5, 2.0])
    up = r.choice([True, False])
    T = m * (GR + a) if up else m * (GR - a)
    phase = 'accelerates upwards' if up else 'accelerates downwards'
    s = f'A lift of total mass {m} kg {phase} at {nf(a)} m s⁻².'
    if D <= 2:
        return numq(r, D, s, 'tension in the cable', T, ' N', f'T − mg = ±ma → T = {m}(9.81 {"+" if up else "−"} {nf(a)})', [m * GR, m * (GR - a) if up else m * (GR + a), m * a], fm=f3)
    mp = r.choice([50, 60, 70, 80])
    N = mp * (GR + a) if up else mp * (GR - a)
    return Q(s + f' A passenger of mass {mp} kg stands on bathroom scales calibrated in newtons inside the lift. (a) Draw a free-body diagram for the passenger. (b) Calculate the reading on the scales. (c) Calculate the tension in the cable.',
             f'(a) weight {f3(mp * GR)} N down, normal force up (b) {f3(N)} N (c) {f3(T)} N',
             f'(a) two forces correctly labelled [1] (b) N − mg = ma (with sign) [1]; N = {f3(N)} N [1] (c) T = {m}(9.81 {"+" if up else "−"} {nf(a)}) = {f3(T)} N [1]' + (' [4]' if D <= 4 else '; comment that scales read more/less than weight [1] [5]'), 'multi_step')


@t43.add('C3', (2, 3, 4), 'numerical')
def t43_slope(r, D):
    m = r.choice([2.0, 5.0, 8.0, 12.0, 20.0]); th = r.choice([15, 20, 25, 30, 35]); fr = r.choice([0, 0.2, 0.3]) * m * GR
    a = GR * math.sin(math.radians(th)) - fr / m
    if a <= 0:
        return None
    s = f'A block of mass {nf(m)} kg slides down a slope inclined at {th}° to the horizontal' + (f' against a friction force of {f3(fr)} N.' if fr else ' with negligible friction.')
    return Q(s + ' Calculate the acceleration of the block down the slope and the normal contact force.', f'a = {f3(a)} m s⁻²; N = {f3(m * GR * math.cos(math.radians(th)))} N',
             f'component down slope mg sin {th}° = {f3(m * GR * math.sin(math.radians(th)))} N [1]; resultant ÷ m: a = {f3(a)} m s⁻² [1]; N = mg cos {th}° = {f3(m * GR * math.cos(math.radians(th)))} N [1] [3]')


@t43.add('C2', (2, 3, 4), 'explain')
def t43_fbd(r, D):
    sc = r.choice([('a car accelerating along a level road', 'weight down, normal reactions up (equal to weight), driving force forwards larger than air resistance and friction backwards'),
                   ('a box being pulled along a rough floor at constant speed by a horizontal rope', 'weight down, normal force up (equal), tension forwards equal to friction backwards'),
                   ('a hot-air balloon rising at constant velocity', 'weight down, upthrust up, air resistance down; upthrust = weight + drag'),
                   ('a boat accelerating across a lake', 'weight down, upthrust up (equal), thrust forwards larger than water resistance backwards'),
                   ('a ball hanging at rest from a string', 'weight down, tension up, equal in size'),
                   ('a parachutist decelerating just after the parachute opens', 'weight down, air resistance up, with air resistance larger than weight')])
    return Q(f'Describe the free-body diagram for {sc[0]}, identifying every force and comparing their sizes. State the direction of the resultant force.', cap(sc[1]) + '.',
             'all forces identified [1]; correct relative sizes [1]; resultant direction consistent with motion [1] [3]')


def _fbd_c4(r, D):
    m = r.choice([60, 70, 80]); M = r.choice([700, 800, 900]); a = r.choice([0.6, 1.0, 1.4]); v = r.choice([2.0, 3.0])
    intro = r.choice([f'A passenger of mass {m} kg rides in a lift of mass {M} kg in an office block in {city(r)}. The lift accelerates upwards at {nf(a)} m s⁻², travels at a constant {nf(v)} m s⁻¹ and then decelerates at {nf(a)} m s⁻² to rest.',
                      f'In a hotel in {city(r)}, a lift of mass {M} kg carrying a passenger of mass {m} kg speeds up at {nf(a)} m s⁻², moves at {nf(v)} m s⁻¹, then slows at {nf(a)} m s⁻² to stop at the top floor.'])
    parts = [
        lambda r: ('Calculate the cable tension while accelerating upwards.', f'{f3((M + m) * (GR + a))} N', 'T = (M + m)(g + a) [2]'),
        lambda r: ('Calculate the cable tension at constant velocity.', f'{f3((M + m) * GR)} N', 'T = (M + m)g [1]'),
        lambda r: ('Calculate the contact force on the passenger while decelerating.', f'{f3(m * (GR - a))} N', 'N = m(g − a) [2]'),
        lambda r: ('Explain why the passenger feels lighter while the lift slows down at the top.', 'The lift accelerates downwards so the resultant force on the passenger is downwards; the normal force is less than the weight.', 'acceleration downwards [1]; normal force < weight [1] [2]'),
        lambda r: ('Calculate the time taken to reach the constant speed.', f'{f3(v / a)} s', 't = v/a [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t43.add('C4', (2, 3, 4, 5), 'multi_step')(_fbd_c4)

CHAPTERS[4] = [t41, t42, t43]

# ===================================================================== 5 Momentum
N51 = 'Linear momentum and force as rate of change of momentum'
t51 = topic(N51, N51.lower(), 'linear momentum', 'rate of change of momentum')
FX(t51, 'C1', (1, 2), [
    ('What is the momentum of a 1500 kg car moving at 20 m s⁻¹?', '30 000 kg m s⁻¹', 'p = mv = 1500 × 20.', ['75 kg m s⁻¹', '300 000 kg m s⁻¹', '1520 kg m s⁻¹']),
    ('Which unit is equivalent to kg m s⁻¹?', 'N s', 'Impulse FΔt = Δp, so N s = kg m s⁻¹.', ['N s⁻¹', 'N m', 'J s']),
    ('Which statement is Newton\'s second law in terms of momentum?', 'The resultant force is equal to the rate of change of momentum', 'F = Δp/Δt.', ['The resultant force is equal to the change of momentum', 'The momentum is equal to force × distance', 'The momentum of a system is always zero']),
    ('A ball of mass 0.20 kg hits a wall at 5.0 m s⁻¹ and rebounds at 5.0 m s⁻¹. What is the magnitude of its change in momentum?', '2.0 kg m s⁻¹', 'Δp = 0.20 × (5.0 − (−5.0)) = 2.0 kg m s⁻¹.', ['0', '1.0 kg m s⁻¹', '10 kg m s⁻¹']),
    ('The area under a force-time graph represents', 'the change in momentum (impulse)', 'Area = ∫F dt = Δp.', ['the work done', 'the acceleration', 'the power']),
    ('A force of 50 N acts on an object for 0.40 s. What is its change in momentum?', '20 N s', 'Δp = FΔt = 50 × 0.40.', ['125 N s', '0.008 N s', '50 N s']),
    ('Define linear momentum.', 'The product of mass and velocity.', 'p = mv [1]'),
])
FX(t51, 'C2', (1, 2, 3, 4), [
    ('Explain how a car crumple zone reduces the force on passengers in a collision.', 'The passengers\' change in momentum is fixed; the crumple zone increases the time over which the momentum changes, so the rate of change of momentum, and hence the force, is smaller.', 'Δp fixed [1]; longer time [1]; F = Δp/Δt smaller [1] [3]'),
    ('Explain why a cricketer moves the hands backwards when catching a fast ball.', 'This increases the time taken to stop the ball for the same change in momentum, reducing the force on the hands.', 'increases stopping time [1]; F = Δp/Δt reduced [1] [2]'),
    ('Explain why a ball that bounces back from a wall experiences a larger force than one that stops dead in the same time.', 'Momentum is a vector; rebounding reverses the velocity, so the change in momentum is larger (up to double), and so the force (Δp/Δt) is larger.', 'Δp larger when direction reverses [1]; F = Δp/Δt [1] [2]'),
    ('Show that F = ma is a special case of F = Δp/Δt.', 'Δp/Δt = Δ(mv)/Δt; for constant mass, = m Δv/Δt = ma.', 'mass constant taken out [1]; Δv/Δt = a [1] [2]'),
    ('Explain why momentum is a vector quantity.', 'p = mv; mass is a scalar and velocity is a vector, so their product has direction (the direction of the velocity).', 'velocity is a vector [1]; momentum in direction of velocity [1] [2]'),
])


@t51.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t51_force(r, D):
    sc = r.choice([('A tennis ball', [0.057, 0.058]), ('A football', [0.43, 0.45]), ('A golf ball', [0.046]), ('A hockey ball', [0.16]), ('A cricket ball', [0.16]), ('A squash ball', [0.024])])
    name, ms = sc; m = r.choice(ms)
    u = r.choice([8.0, 10.0, 15.0, 20.0, 25.0]); v = r.choice([0, 5.0, 8.0, 12.0]); t = r.choice([0.005, 0.008, 0.010, 0.015, 0.020])
    reb = v > 0
    dp = m * (u + v)
    F = dp / t
    s = f'{name} of mass {nf(m)} kg moving at {nf(u)} m s⁻¹ hits a wall ' + (f'and rebounds along the same line at {nf(v)} m s⁻¹.' if reb else 'and stops.') + f' It is in contact with the wall for {nf(t * 1000)} ms.'
    if D <= 2:
        return numq(r, D, s, 'average force exerted by the wall on the ball', F, ' N', f'F = Δp/Δt = {nf(m)} × ({nf(u)} + {nf(v)})/{nf(t)}', [m * abs(u - v) / t if reb else m * u / t / 2, dp, F * 1000], fm=f3)
    if D == 3:
        return Q(s + ' Calculate the change in momentum and the average force on the ball.', f'Δp = {f3(dp)} kg m s⁻¹ away from the wall; F = {f3(F)} N',
                 f'Δp = m(v − u) with sign convention = {f3(dp)} kg m s⁻¹ [1]; F = Δp/Δt [1]; = {f3(F)} N [1] [3]')
    return Q(s + ' (a) Calculate the average force on the ball. (b) State the force exerted by the ball on the wall and the law used. (c) Explain why a softer ball with the same speeds would exert a smaller force.',
             f'(a) {f3(F)} N (b) {f3(F)} N towards the wall, by Newton\'s third law (c) longer contact time, so smaller rate of change of momentum.',
             f'(a) Δp = {f3(dp)} kg m s⁻¹ [1]; F = {f3(F)} N [1] (b) equal and opposite, N3 [1] (c) Δt larger, F = Δp/Δt smaller [1]' + (' [4]' if D == 4 else '; Δp unchanged [1] [5]'), 'multi_step')


@t51.add('C3', (2, 3, 4), 'numerical')
def t51_jet(r, D):
    rate = r.choice([2.0, 3.0, 4.0, 5.0, 8.0]); v = r.choice([10, 12, 15, 20, 25])
    sc = r.choice(['A hosepipe directs a horizontal jet of water at a wall; the water hits the wall and runs down it', 'A fire hose sends a horizontal jet of water against a door; the water does not bounce back', 'A garden sprinkler jet strikes a vertical board horizontally and the water falls away'])
    F = rate * v
    return Q(f'{sc}. Water leaves the hose at {nf(v)} m s⁻¹ at a rate of {nf(rate)} kg s⁻¹. Calculate the force exerted on the wall by the water.', f'{f3(F)} N',
             f'momentum lost per second = (mass per second) × v [1]; F = {nf(rate)} × {nf(v)} [1]; = {f3(F)} N [1] [3]')


@t51.add('C3', (2, 3, 4), 'numerical')
def t51_graph(r, D):
    Fm = r.choice([200, 400, 600, 800, 1200]); t = r.choice([0.010, 0.020, 0.040, 0.050]); m = r.choice([0.15, 0.40, 0.45, 0.60])
    imp = 0.5 * Fm * t
    return Q(f'The force on a ball of mass {nf(m)} kg, initially at rest, during a kick rises uniformly from zero to {Fm} N and then falls uniformly to zero, the whole contact lasting {nf(t * 1000)} ms. Calculate the speed of the ball after the kick.', f'{f3(imp / m)} m s⁻¹',
             f'impulse = area of triangle = ½ × {Fm} × {nf(t)} = {f3(imp)} N s [1]; = Δp [1]; v = {f3(imp)}/{nf(m)} = {f3(imp / m)} m s⁻¹ [1] [3]')


def _mom_c4(r, D):
    m = r.choice([60, 70, 75]); v = r.choice([8.0, 10.0, 12.0]); t1 = r.choice([0.08, 0.10, 0.12]); t2 = r.choice([0.6, 0.8, 1.0])
    intro = r.choice([f'In a crash test in {city(r)}, a dummy of mass {m} kg travelling at {nf(v)} m s⁻¹ is brought to rest. Without an airbag the stopping time is {nf(t1)} s; with an airbag it is {nf(t2)} s.',
                      f'A {m} kg stunt performer falling at {nf(v)} m s⁻¹ lands either on hard ground (stopping time {nf(t1)} s) or on an air cushion (stopping time {nf(t2)} s).'])
    dp = m * v
    parts = [
        lambda r: ('Calculate the change in momentum.', f'{f3(dp)} kg m s⁻¹', 'Δp = mv [1]'),
        lambda r: ('Calculate the average force in each case.', f'{f3(dp / t1)} N and {f3(dp / t2)} N', 'F = Δp/Δt for each [2]'),
        lambda r: ('Explain why the longer stopping time is safer.', 'The same Δp over a longer time gives a smaller force (and deceleration), so less injury.', 'same Δp, longer t [1]; smaller force [1] [2]'),
        lambda r: ('State Newton\'s second law in terms of momentum.', 'The resultant force is proportional to (equal to) the rate of change of momentum.', 'statement [1]'),
        lambda r: ('Calculate the average deceleration in the shorter collision.', f'{f3(v / t1)} m s⁻²', 'a = v/t [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t51.add('C4', (2, 3, 4, 5), 'multi_step')(_mom_c4)

N52 = 'Conservation of momentum in one and two dimensions'
t52 = topic(N52, N52.lower(), 'conservation of momentum', 'two dimensions')
FX(t52, 'C1', (1, 2), [
    ('State the principle of conservation of momentum.', 'The total momentum of a system of interacting objects remains constant provided no resultant external force acts.', 'total momentum constant [1]; no external resultant force [1] [2]'),
    ('A 2.0 kg trolley moving at 3.0 m s⁻¹ collides with and sticks to a stationary 1.0 kg trolley. What is their common velocity?', '2.0 m s⁻¹', '2.0 × 3.0 = 3.0 v → v = 2.0 m s⁻¹.', ['3.0 m s⁻¹', '1.5 m s⁻¹', '1.0 m s⁻¹']),
    ('A gun recoils when it fires a bullet. Before firing, the total momentum is zero. After firing, the total momentum is', 'zero', 'No external horizontal force: momentum conserved; bullet and gun have equal and opposite momenta.', ['equal to the momentum of the bullet', 'twice the momentum of the bullet', 'equal to the kinetic energy of the bullet']),
    ('In which situation is the momentum of the system NOT conserved?', 'A car speeds up because of friction from the road', 'The road exerts an external force on the car.', ['Two ice skaters push apart on smooth ice', 'Two trolleys collide on a frictionless track', 'A stationary firework explodes in mid-air']),
    ('In a two-dimensional collision, momentum is conserved', 'separately in each of two perpendicular directions', 'Momentum is a vector, so each component is conserved.', ['only along the original direction of motion', 'only if kinetic energy is conserved', 'only for the larger mass']),
    ('Two skaters at rest push apart. The 60 kg skater moves at 2.0 m s⁻¹. How fast does the 40 kg skater move?', '3.0 m s⁻¹', '60 × 2.0 = 40v → v = 3.0 m s⁻¹.', ['2.0 m s⁻¹', '1.3 m s⁻¹', '5.0 m s⁻¹']),
])
FX(t52, 'C2', (1, 2, 3, 4), [
    ('Use Newton\'s third law to explain why momentum is conserved when two trolleys collide.', 'During the collision each trolley exerts an equal and opposite force on the other for the same time; so their momentum changes are equal and opposite and the total momentum is unchanged.', 'equal and opposite forces (N3) [1]; same contact time [1]; equal and opposite Δp [1] [3]'),
    ('Explain why a rifle recoils when it fires a bullet.', 'Total momentum is zero before firing; the bullet gains forward momentum so the rifle must gain equal backward momentum.', 'initial momentum zero [1]; rifle gains equal and opposite momentum [1] [2]'),
    ('Explain why the momentum of a ball falling towards the Earth is not conserved, but the momentum of the ball and the Earth together is.', 'Weight is an external force on the ball alone, so its momentum changes; for ball + Earth the gravitational forces are internal and equal and opposite, so total momentum is constant.', 'external force on ball alone [1]; internal forces for the system [1] [2]'),
    ('Describe how momentum is conserved when a stationary nucleus emits an α-particle.', 'Total momentum is zero before; afterwards the α-particle and the daughter nucleus move in opposite directions with equal magnitudes of momentum.', 'zero total before [1]; equal and opposite momenta after [1] [2]'),
])


@t52.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t52_1d(r, D):
    m1 = r.choice([0.50, 0.80, 1.0, 1.5, 2.0, 1200, 900]); big = m1 > 100
    m2 = r.choice([0.50, 1.0, 1.5, 2.5]) if not big else r.choice([800, 1000, 1500])
    u1 = r.choice([2.0, 3.0, 4.0, 5.0]) if not big else r.choice([10.0, 12.0, 15.0, 20.0])
    u2 = r.choice([0, 0, -1.0, 1.0]) if not big else r.choice([0, 0, 5.0, -5.0])
    what = ('trolley A', 'trolley B') if not big else ('car A', 'car B')
    v = (m1 * u1 + m2 * u2) / (m1 + m2)
    move = 'is at rest' if u2 == 0 else (f'moves at {nf(abs(u2))} m s⁻¹ in the {"same" if u2 > 0 else "opposite"} direction')
    s = f'{cap(what[0])} of mass {nf(m1)} kg moving at {nf(u1)} m s⁻¹ collides with {what[1]} of mass {nf(m2)} kg, which {move}. They stick together.'
    if D <= 2:
        return numq(r, D, s, 'speed immediately after the collision', abs(v), ' m s⁻¹', f'v = (m₁u₁ + m₂u₂)/(m₁ + m₂) = ({f3(m1 * u1)} + {f3(m2 * u2)})/{nf(m1 + m2)}', [u1 * m1 / m2, (u1 + u2) / 2 + 0.3, m1 * u1 / (m1 + m2) * 2], fm=f3)
    ke1 = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2; ke2 = 0.5 * (m1 + m2) * v ** 2
    if D == 3:
        return Q(s + ' Calculate the common velocity after the collision, stating its direction.', f'{f3(abs(v))} m s⁻¹ in the original direction of {what[0]}' if v > 0 else f'{f3(abs(v))} m s⁻¹ opposite to the original direction of {what[0]}',
                 f'momentum before = {f3(m1 * u1 + m2 * u2)} kg m s⁻¹ (signs) [1]; ÷ total mass [1]; {f3(v)} m s⁻¹ with direction [1] [3]')
    return Q(s + ' (a) Calculate their common velocity. (b) Calculate the loss of kinetic energy. (c) State what happens to this energy.',
             f'(a) {f3(v)} m s⁻¹ (b) {f3(ke1 - ke2)} J (c) transferred to thermal energy, sound and deformation of the bodies.',
             f'(a) conservation of momentum [1]; v = {f3(v)} m s⁻¹ [1] (b) KE before {f3(ke1)} J, after {f3(ke2)} J [1]; loss {f3(ke1 - ke2)} J [1] (c) heat/sound/deformation [1] [5]', 'multi_step')


@t52.add('C3', (2, 3, 4, 5), 'numerical')
def t52_explode(r, D):
    M = r.choice([2.0, 3.0, 5.0, 6.0]); f = r.choice([0.25, 0.4, 0.5]); m1 = M * f; m2 = M - m1; v1 = r.choice([6.0, 8.0, 10.0, 12.0])
    v2 = m1 * v1 / m2
    sc = r.choice([f'A stationary firework of mass {nf(M)} kg explodes into two pieces. A piece of mass {f3(m1)} kg moves off at {nf(v1)} m s⁻¹.',
                   f'Two trolleys of total mass {nf(M)} kg are held together at rest with a compressed spring between them. When released, the {f3(m1)} kg trolley moves at {nf(v1)} m s⁻¹.',
                   f'A {nf(M)} kg block at rest on smooth ice splits into two parts when a small charge detonates; the {f3(m1)} kg part slides off at {nf(v1)} m s⁻¹.'])
    ke = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
    if D <= 3:
        return Q(sc + ' Calculate the velocity of the other piece.', f'{f3(v2)} m s⁻¹ in the opposite direction', f'total momentum zero [1]; {f3(m1)} × {nf(v1)} = {f3(m2)} × v [1]; v = {f3(v2)} m s⁻¹ opposite [1] [3]')
    return Q(sc + ' Calculate the velocity of the other piece and the total kinetic energy released. Explain why momentum is conserved but kinetic energy is not.',
             f'{f3(v2)} m s⁻¹ opposite; {f3(ke)} J; momentum conserved (no external force); KE comes from chemical/elastic energy, so it increases.',
             f'momentum: v = {f3(v2)} m s⁻¹ opposite [2]; KE total = {f3(ke)} J [1]; explanation of conservation vs energy source [1] [4]')


@t52.add('C3', (3, 4, 5), 'multi_step')
def t52_2d(r, D):
    m = r.choice([0.17, 0.20, 0.25, 1.0, 2.0]); u = r.choice([2.0, 3.0, 4.0, 5.0])
    a1 = r.choice([30, 35, 40, 45]); a2 = 90 - a1
    v1 = u * math.cos(math.radians(a1)); v2 = u * math.sin(math.radians(a1))
    sc = r.choice(['A snooker ball', 'A puck on an air table', 'A steel sphere on a smooth surface'])
    return Q(f'{sc} of mass {nf(m)} kg moving at {nf(u)} m s⁻¹ strikes an identical stationary one. After the collision the first moves at {a1}° and the second at {a2}° to the original direction, on opposite sides. Using conservation of momentum in two perpendicular directions, determine the speed of each ball after the collision.',
             f'first {f3(v1)} m s⁻¹, second {f3(v2)} m s⁻¹', f'along original direction: u = v₁ cos {a1}° + v₂ cos {a2}° [1]; perpendicular: v₁ sin {a1}° = v₂ sin {a2}° [1]; solve: v₁ = {f3(v1)} m s⁻¹ [1]; v₂ = {f3(v2)} m s⁻¹ [1] [4]')


def _cons_c4(r, D):
    m1 = r.choice([0.020, 0.010, 0.015]); M = r.choice([1.0, 1.5, 2.0]); v = r.choice([200, 250, 300, 400])
    V = m1 * v / (m1 + M); h = V * V / (2 * GR)
    intro = r.choice([f'A bullet of mass {nf(m1)} kg travelling horizontally at {v} m s⁻¹ embeds itself in a wooden block of mass {nf(M)} kg hanging at rest from strings (a ballistic pendulum).',
                      f'In a forensic test in {city(r)}, a {nf(m1)} kg pellet moving at {v} m s⁻¹ is fired into a suspended {nf(M)} kg block, which swings upwards.'])
    parts = [
        lambda r: ('Calculate the speed of the block and bullet just after impact.', f'{f3(V)} m s⁻¹', 'conservation of momentum [2]'),
        lambda r: ('Calculate the height to which the block rises.', f'{f3(h)} m', 'h = V²/(2g) [2]'),
        lambda r: ('Calculate the percentage of the bullet\'s kinetic energy that is lost in the impact.', f'{nf(100 * M / (m1 + M), 3)}%', f'KE after/KE before = m/(m + M) [3]'),
        lambda r: ('State and explain whether the collision is elastic.', 'Inelastic: kinetic energy is not conserved (most becomes thermal energy and deformation).', 'inelastic [1]; KE lost [1] [2]'),
        lambda r: ('Explain why momentum is conserved during the impact even though the strings exert forces.', 'The impact is very brief and the strings are vertical, so there is no horizontal external force during the impact.', 'no horizontal external force [1]; short duration [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t52.add('C4', (2, 3, 4, 5), 'multi_step')(_cons_c4)

N53 = 'Elastic and inelastic collisions and relative speed of approach and separation'
t53 = topic(N53, N53.lower(), 'elastic and inelastic collisions', 'relative speed of approach')
FX(t53, 'C1', (1, 2), [
    ('In a perfectly elastic collision, which quantities are conserved?', 'Both total momentum and total kinetic energy', 'Elastic: KE conserved; momentum is always conserved in an isolated system.', ['Momentum only', 'Kinetic energy only', 'Neither momentum nor kinetic energy']),
    ('For a perfectly elastic collision between two bodies, the relative speed of approach is', 'equal to the relative speed of separation', 'This follows from conservation of both momentum and KE.', ['greater than the relative speed of separation', 'less than the relative speed of separation', 'zero']),
    ('In an inelastic collision, which is true?', 'Total momentum is conserved but some kinetic energy is transferred to other forms', 'Kinetic energy is not conserved in an inelastic collision.', ['Total kinetic energy is conserved but momentum is not', 'Neither momentum nor total energy is conserved', 'The bodies must stick together']),
    ('Two balls approach each other at 3.0 m s⁻¹ and 2.0 m s⁻¹. What is their relative speed of approach?', '5.0 m s⁻¹', 'Opposite directions: relative speed = 3.0 + 2.0.', ['1.0 m s⁻¹', '6.0 m s⁻¹', '2.5 m s⁻¹']),
    ('A collision in which the two objects stick together is', 'inelastic', 'Objects that stick together always lose kinetic energy.', ['perfectly elastic', 'superelastic', 'impossible if momentum is conserved']),
    ('State what is meant by a perfectly elastic collision.', 'A collision in which the total kinetic energy is conserved.', 'total KE conserved [1]'),
])
FX(t53, 'C2', (1, 2, 3, 4), [
    ('Explain why total energy is always conserved in a collision even though kinetic energy may not be.', 'Energy cannot be created or destroyed; kinetic energy lost is transferred to other stores such as thermal energy, sound and deformation (strain) energy.', 'total energy conserved [1]; KE transferred to other forms [1] [2]'),
    ('Explain how to test whether a collision between two gliders on an air track is elastic using only velocity measurements.', 'Measure the velocities before and after; calculate the relative speed of approach and of separation; if they are equal the collision is perfectly elastic.', 'measure velocities [1]; compare relative speeds of approach and separation [1] [2]'),
    ('A ball dropped onto a hard floor rebounds to almost the same height. Explain what this shows about the collision.', 'The rebound speed nearly equals the impact speed, so very little kinetic energy is lost: the collision is nearly elastic.', 'speeds nearly equal [1]; KE nearly conserved/nearly elastic [1] [2]'),
    ('Explain why, in a head-on elastic collision between equal masses with one initially at rest, the moving body stops.', 'Momentum and KE conservation together require the velocities to be exchanged: the first stops and the second moves off with the original velocity.', 'both conservation laws applied [1]; velocities exchanged [1] [2]'),
])


@t53.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t53_check(r, D):
    m1 = r.choice([0.50, 1.0, 2.0]); m2 = r.choice([0.50, 1.0, 1.5, 3.0]); u1 = r.choice([2.0, 3.0, 4.0, 6.0])
    elastic = r.choice([True, False])
    if elastic:
        v1 = (m1 - m2) / (m1 + m2) * u1; v2 = 2 * m1 / (m1 + m2) * u1
    else:
        e = r.choice([0.4, 0.5, 0.6])
        v = m1 * u1 / (m1 + m2)
        v2 = v + e * u1 * m1 / (m1 + m2)
        v1 = (m1 * u1 - m2 * v2) / m1
    s = f'A glider of mass {nf(m1)} kg moving at {nf(u1)} m s⁻¹ on an air track hits a stationary glider of mass {nf(m2)} kg. Afterwards, the second glider moves at {f3(v2)} m s⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'speed of the first glider after the collision', abs(v1), ' m s⁻¹', f'{nf(m1)} × {nf(u1)} = {nf(m1)}v₁ + {nf(m2)} × {f3(v2)}', [u1 - v2 + 0.4, abs(m1 * u1 - m2 * v2) / m2, u1 / 2 + 0.1], fm=f3)
    sep = v2 - v1
    return Q(s + ' Calculate the velocity of the first glider after the collision and determine whether the collision is elastic using relative speeds.',
             f'v₁ = {f3(v1)} m s⁻¹; approach {nf(u1)} m s⁻¹, separation {f3(sep)} m s⁻¹, so the collision is {"elastic" if elastic else "inelastic"}.',
             f'momentum: v₁ = {f3(v1)} m s⁻¹ [1]; relative speed of approach = {nf(u1)} m s⁻¹ [1]; separation = {f3(v2)} − ({f3(v1)}) = {f3(sep)} m s⁻¹ [1]; conclusion [1] [4]')


@t53.add('C3', (2, 3, 4, 5), 'numerical')
def t53_solve(r, D):
    m1 = r.choice([1.0, 2.0, 3.0]); m2 = r.choice([1.0, 2.0, 4.0]); u1 = r.choice([3.0, 4.0, 6.0, 8.0]); u2 = r.choice([0, -2.0, 1.0])
    v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2); v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
    u2s = 'is at rest' if u2 == 0 else (f'moves at {nf(abs(u2))} m s⁻¹ ' + ('towards it' if u2 < 0 else 'in the same direction'))
    return Q(f'Sphere A of mass {nf(m1)} kg moving at {nf(u1)} m s⁻¹ has a perfectly elastic head-on collision with sphere B of mass {nf(m2)} kg, which {u2s}. Using conservation of momentum and the relative speed of approach equals the relative speed of separation, determine the velocities of A and B after the collision.',
             f'A: {f3(v1)} m s⁻¹, B: {f3(v2)} m s⁻¹ (positive = original direction of A)',
             f'momentum: {nf(m1)}({nf(u1)}) + {nf(m2)}({nf(u2)}) = {nf(m1)}v_A + {nf(m2)}v_B [1]; relative speeds: {nf(u1 - u2)} = v_B − v_A [1]; solve simultaneously [1]; v_A = {f3(v1)}, v_B = {f3(v2)} m s⁻¹ [1] [4]')


@t53.add('C2', (2, 3, 4), 'explain')
def t53_claim(r, D):
    m = r.choice([1.0, 2.0, 0.5]); u = r.choice([3.0, 4.0, 5.0])
    who = person(r)
    return Q(f'Two identical trolleys, each of mass {nf(m)} kg, collide head-on, each moving at {nf(u)} m s⁻¹, and stop dead. {who} says "momentum was lost, so this breaks the law of conservation of momentum." Explain why {who} is wrong, and state what happened to the kinetic energy.',
             f'The total momentum before was zero (equal and opposite momenta), and it is zero after, so momentum is conserved. All {nf(m * u * u)} J of kinetic energy was transferred to thermal energy, sound and deformation (a totally inelastic collision).',
             'momenta equal and opposite: total zero before [1]; zero after so conserved [1]; KE transferred to other forms [1] [3]')


def _coll_c4(r, D):
    m1 = r.choice([2.0, 3.0]); m2 = r.choice([1.0, 2.0]); u1 = r.choice([4.0, 5.0, 6.0])
    v1 = (m1 - m2) / (m1 + m2) * u1; v2 = 2 * m1 / (m1 + m2) * u1; vs = m1 * u1 / (m1 + m2)
    intro = r.choice([f'In a physics laboratory in {city(r)}, a glider of mass {nf(m1)} kg moving at {nf(u1)} m s⁻¹ collides with a stationary glider of mass {nf(m2)} kg on a level air track.',
                      f'A {nf(m1)} kg trolley travelling at {nf(u1)} m s⁻¹ hits a stationary {nf(m2)} kg trolley on a frictionless runway.'])
    parts = [
        lambda r: ('The gliders stick together. Calculate their common speed.', f'{f3(vs)} m s⁻¹', 'conservation of momentum [2]'),
        lambda r: ('For the sticking collision, calculate the kinetic energy lost.', f'{f3(0.5 * m1 * u1 ** 2 - 0.5 * (m1 + m2) * vs ** 2)} J', 'KE before − KE after [2]'),
        lambda r: ('Instead, the collision is perfectly elastic. Calculate both velocities after the collision.', f'{f3(v1)} m s⁻¹ and {f3(v2)} m s⁻¹', 'momentum equation [1]; relative speed equation [1]; values [1] [3]'),
        lambda r: ('State what is meant by the relative speed of separation.', 'The speed of one body measured relative to the other as they move apart.', 'definition [1]'),
        lambda r: ('Explain why an air track is used.', 'It removes friction, so no external horizontal force acts and momentum is conserved.', 'friction negligible [1]; momentum conserved [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t53.add('C4', (2, 3, 4, 5), 'multi_step')(_coll_c4)

CHAPTERS[5] = [t51, t52, t53]

# ===================================================================== 6 Forces and equilibrium
N61 = 'Turning effects: moment of a force and couples and torque'
t61 = topic(N61, N61.lower(), 'moment of a force', 'couples and torque')
FX(t61, 'C1', (1, 2), [
    ('Which is the definition of the moment of a force about a point?', 'Force × perpendicular distance from the point to the line of action of the force', 'Moment = F × d⊥.', ['Force × distance moved by the force', 'Force ÷ perpendicular distance', 'Force × distance from the point to where the force acts, in any direction']),
    ('What is a couple?', 'A pair of equal and opposite forces whose lines of action do not coincide', 'A couple produces rotation without translation.', ['Two equal forces in the same direction', 'A single force acting through the pivot', 'Two forces that are Newton\'s third law pairs']),
    ('Two forces of 15 N form a couple with a perpendicular separation of 0.40 m. What is the torque?', '6.0 N m', 'Torque = F × separation = 15 × 0.40.', ['12 N m', '3.0 N m', '37.5 N m']),
    ('What is the SI unit of moment of a force?', 'N m', 'Force (N) × distance (m).', ['N m⁻¹', 'J s', 'N s']),
    ('A force of 40 N acts at 30° to a spanner of length 0.25 m. What is the moment about the nut?', '5.0 N m', 'Perpendicular component: 40 sin 30° × 0.25 = 5.0 N m.', ['10 N m', '8.7 N m', '160 N m']),
    ('The resultant force produced by a couple is', 'zero', 'The forces are equal and opposite, so the resultant is zero; only the torque remains.', ['equal to one of the forces', 'twice one of the forces', 'equal to the torque']),
    ('State what is meant by the torque of a couple.', 'The product of one of the forces and the perpendicular distance between the lines of action of the forces.', 'one force × perpendicular separation [1]'),
])
FX(t61, 'C2', (1, 2, 3, 4), [
    ('Explain why it is easier to undo a tight nut with a long spanner.', 'The moment is F × perpendicular distance; a longer spanner gives a larger distance so the same moment needs a smaller force.', 'moment = F × d [1]; larger d, smaller F for same moment [1] [2]'),
    ('Explain why a couple causes rotation but no acceleration of the centre of mass.', 'The two forces are equal and opposite so the resultant force is zero (no translation), but their moments add, giving a resultant torque.', 'resultant force zero [1]; moments in same sense give torque [1] [2]'),
    ('Explain why a door handle is placed far from the hinges.', 'The perpendicular distance from the hinge (pivot) is large, so a small force produces a large enough moment to turn the door.', 'large perpendicular distance from pivot [1]; small force needed [1] [2]'),
    ('Explain why pushing a door at an angle to its surface is less effective than pushing perpendicularly.', 'Only the component of force perpendicular to the door (F sin θ) produces a moment; the perpendicular distance from the hinge to the line of action is smaller.', 'only perpendicular component turns [1]; smaller moment for same force [1] [2]'),
    ('Show that the torque of a couple is the same about any point.', 'Take a point a distance x from one force, separation d: moments are F(x + d) and −Fx; total = Fd, independent of x.', 'moments about arbitrary point [1]; x cancels leaving Fd [1] [2]'),
])


@t61.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t61_moment(r, D):
    F = r.choice([20, 25, 30, 40, 50, 60, 80, 120]); d = r.choice([0.15, 0.20, 0.25, 0.30, 0.40, 0.60, 0.80]); th = r.choice([90, 90, 30, 45, 60, 70])
    M = F * d * math.sin(math.radians(th))
    sc = r.choice([f'A mechanic pulls on the end of a spanner {nf(d)} m long with a force of {F} N', f'{person(r)} pushes on a door {nf(d)} m from its hinge with a force of {F} N', f'A cyclist presses on a pedal crank of length {nf(d)} m with a force of {F} N'])
    s = sc + (', perpendicular to it.' if th == 90 else f' at {th}° to it.')
    if D <= 2:
        return numq(r, D, s, 'moment of the force about the pivot', M, ' N m', f'M = F × d⊥ = {F} × {nf(d)}' + ('' if th == 90 else f' × sin {th}°'), [F * d, F / d, F * d * math.cos(math.radians(th)) if th != 90 else F * d / 2], fm=f3)
    need = r.choice([15, 20, 25, 30, 40])
    Fmin = need / d
    return Q(s + f' Calculate the moment produced. The nut needs a moment of {need} N m to turn. Calculate the minimum force needed at the same point, and explain why it is a minimum.',
             f'{f3(M)} N m; {f3(Fmin)} N applied perpendicular to the spanner (largest perpendicular distance)',
             f'M = F d sin θ = {f3(M)} N m [1]; F = {need}/{nf(d)} [1]; = {f3(Fmin)} N [1]; perpendicular force gives maximum moment arm [1] [4]')


@t61.add('C3', (2, 3, 4), 'numerical')
def t61_couple(r, D):
    F = r.choice([8, 12, 15, 20, 30]); d = r.choice([0.12, 0.20, 0.25, 0.35, 0.40])
    sc = r.choice([f'A driver turns a steering wheel of diameter {nf(d * 2)} m by applying equal and opposite forces of {F} N tangentially at opposite ends of a diameter.',
                   f'A tap is turned by forces of {F} N applied in opposite directions at the ends of a handle {nf(2 * d)} m long, perpendicular to it.',
                   f'A wheel brace has arms of total length {nf(2 * d)} m. Equal and opposite forces of {F} N are applied perpendicularly at the ends.'])
    T = F * 2 * d
    if D <= 2:
        return Q(sc + ' Calculate the torque of the couple.', f'{f3(T)} N m', f'torque = F × perpendicular separation = {F} × {nf(2 * d)} [1]; = {f3(T)} N m [1] [2]')
    return Q(sc + ' Calculate the torque of the couple and state the resultant force on the object. Explain why a single force of the same size at one end would also tend to move the axle sideways.',
             f'{f3(T)} N m; resultant force zero; a single force has a non-zero resultant, which must be balanced by a force at the axle.',
             f'torque = {f3(T)} N m [1]; resultant zero [1]; single force gives unbalanced translation force [1] [3]')


def _mom_couple_c4(r, D):
    F = r.choice([20, 25, 40]); d = r.choice([0.15, 0.20, 0.30]); th = r.choice([50, 60, 70])
    intro = r.choice([f'A mechanic in {city(r)} uses a two-handed wheel brace with arms of length {nf(d)} m each side of the nut. She applies forces of {F} N perpendicular to the arms at each end, in opposite directions.', f'A plumber turns a valve wheel of radius {nf(d)} m by pushing and pulling with forces of {F} N tangentially at opposite ends of a diameter.'])
    parts = [
        lambda r: ('Calculate the torque of the couple.', f'{f3(2 * F * d)} N m', f'{F} × {nf(2 * d)} [2]'),
        lambda r: ('State the resultant force on the brace and explain your answer.', 'Zero: the forces are equal and opposite.', 'zero [1]; equal and opposite [1] [2]'),
        lambda r: (f'A single force of {F} N is instead applied at one end at {th}° to the arm (or radius). Calculate its moment about the centre.', f'{f3(F * d * math.sin(math.radians(th)))} N m', f'F d sin θ [2]'),
        lambda r: ('Define the moment of a force.', 'Force × perpendicular distance from the pivot to the line of action of the force.', 'definition [1]'),
        lambda r: ('Explain why the moment arm is measured perpendicular to the line of action.', 'Only the perpendicular distance determines the turning effect; a component along the arm passes through the pivot and has no moment.', 'perpendicular distance determines turning [1]; component through pivot gives no moment [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t61.add('C4', (2, 3, 4, 5), 'multi_step')(_mom_couple_c4)

N62 = 'Equilibrium: principle of moments and triangle of forces'
t62 = topic(N62, N62.lower(), 'principle of moments', 'triangle of forces')
FX(t62, 'C1', (1, 2), [
    ('State the two conditions for an object to be in equilibrium.', 'There is no resultant force and no resultant moment (torque) about any point.', 'resultant force zero [1]; resultant moment zero [1] [2]'),
    ('State the principle of moments.', 'For a body in equilibrium, the sum of clockwise moments about any point equals the sum of anticlockwise moments about the same point.', 'clockwise = anticlockwise [1]; about the same point, in equilibrium [1] [2]'),
    ('Three forces act on a body in equilibrium. When drawn tip to tail, the vectors form', 'a closed triangle', 'Zero resultant: the vector triangle closes.', ['a straight line', 'an open triangle', 'a right angle in every case']),
    ('A uniform metre rule is balanced at its 50 cm mark. A 2.0 N weight hangs at the 20 cm mark. Where must a 3.0 N weight hang to balance it?', 'At the 70 cm mark', '2.0 × 30 = 3.0 × d → d = 20 cm from the pivot.', ['At the 80 cm mark', 'At the 95 cm mark', 'At the 65 cm mark']),
    ('Three forces acting on a body in equilibrium must', 'pass through a single point (if not parallel)', 'Otherwise they would produce a resultant moment.', ['all be equal in magnitude', 'all be perpendicular', 'all act vertically']),
    ('A uniform plank of weight 200 N rests on supports at each end. A 100 N box is at its centre. What force does each support provide?', '150 N', 'Symmetry: total 300 N shared equally.', ['100 N', '200 N', '300 N']),
])
FX(t62, 'C2', (1, 2, 3, 4), [
    ('Explain why a ladder leaning against a smooth wall needs friction at the ground to stay in equilibrium.', 'The smooth wall gives only a horizontal normal force; for zero resultant horizontal force, an equal and opposite horizontal force (friction at the ground) is needed.', 'wall force horizontal [1]; friction balances it [1] [2]'),
    ('Explain why taking moments about the point where an unknown force acts simplifies a problem.', 'That force has zero moment about its own point of application, so it does not appear in the equation and another unknown can be found.', 'zero moment about its own point [1]; eliminates unknown [1] [2]'),
    ('Describe how a triangle of forces is used to find an unknown force on an object in equilibrium.', 'Draw the known forces to scale tip to tail in their directions; the line that closes the triangle gives the magnitude and direction of the unknown force.', 'scale drawing tip to tail [1]; closing side gives the unknown [1] [2]'),
    ('A picture hangs from a nail by a string with its two halves at equal angles to the horizontal. Explain why the tension increases as the string is made more nearly horizontal.', 'The vertical components 2T sin θ must equal the weight; as θ decreases, sin θ decreases, so T must increase.', '2T sin θ = W [1]; smaller θ needs larger T [1] [2]'),
])


@t62.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t62_beam(r, D):
    L = r.choice([2.0, 3.0, 4.0, 5.0, 6.0]); W = r.choice([100, 150, 200, 300, 400]); P = r.choice([200, 300, 400, 500, 600, 800]); x = round(L * r.choice([0.2, 0.25, 0.3, 0.4, 0.75]), 2)
    # supports at ends A (0) and B (L)
    RB = (W * L / 2 + P * x) / L; RA = W + P - RB
    sc = r.choice([f'A uniform plank of length {nf(L)} m and weight {W} N rests on supports at its ends A and B. A load of {P} N is placed {nf(x)} m from A.',
                   f'A uniform bridge of length {nf(L)} m and weight {W} N is supported at each end. A person of weight {P} N stands {nf(x)} m from end A.',
                   f'A uniform shelf of length {nf(L)} m and weight {W} N rests on brackets at its ends A and B. A box of weight {P} N is {nf(x)} m from A.'])
    if D <= 2:
        return numq(r, D, sc, 'force exerted by support B', RB, ' N', f'moments about A: R_B × {nf(L)} = {W} × {nf(L / 2)} + {P} × {nf(x)}', [RA, (W + P) / 2 + 37, P * x], fm=f3)
    if D == 3:
        return Q(sc + ' Calculate the forces exerted by both supports.', f'A: {f3(RA)} N; B: {f3(RB)} N', f'moments about A [1]; R_B = {f3(RB)} N [1]; R_A = {W + P} − R_B = {f3(RA)} N [1] [3]')
    return Q(sc + ' (a) Calculate the force from each support. (b) Determine how far from A the load must be for the force at B to equal the force at A. (c) State the two conditions for equilibrium used.',
             f'(a) A {f3(RA)} N, B {f3(RB)} N (b) {nf(L / 2)} m (the centre) (c) zero resultant force and zero resultant moment.',
             f'(a) moments about A [1]; R_B = {f3(RB)} N [1]; R_A = {f3(RA)} N [1] (b) equal forces require load at centre by symmetry [1] (c) both conditions [1] [5]', 'multi_step')


@t62.add('C3', (2, 3, 4, 5), 'numerical')
def t62_tri(r, D):
    W = r.choice([20, 30, 40, 50, 80, 120]); th = r.choice([20, 25, 30, 40, 50, 60])
    kind = r.choice(['sym', 'horiz'])
    if kind == 'sym':
        T = W / (2 * math.sin(math.radians(th)))
        sc = r.choice([f'A lamp of weight {W} N hangs from the midpoint of a wire. Each half of the wire makes {th}° with the horizontal.', f'A sign of weight {W} N is suspended from the middle of a cable whose two halves are each at {th}° to the horizontal.'])
        return Q(sc + ' Calculate the tension in the wire.', f'{f3(T)} N', f'vertical equilibrium: 2T sin {th}° = {W} [1]; T = {W}/(2 sin {th}°) [1]; = {f3(T)} N [1] [3]')
    T = W / math.cos(math.radians(th)); H = W * math.tan(math.radians(th))
    sc = f'A ball of weight {W} N hangs on a string. A horizontal force F pulls the ball sideways so that the string makes {th}° with the vertical, and the ball is in equilibrium.'
    return Q(sc + ' By drawing a triangle of forces or resolving, determine F and the tension in the string.', f'F = {f3(H)} N; T = {f3(T)} N',
             f'vertical: T cos {th}° = {W} [1]; T = {f3(T)} N [1]; horizontal: F = T sin {th}° [1]; = {f3(H)} N [1] [4]')


@t62.add('C3', (3, 4, 5), 'multi_step')
def t62_strut(r, D):
    L = r.choice([1.2, 1.5, 2.0]); W = r.choice([40, 60, 80]); P = r.choice([50, 100, 150]); th = r.choice([30, 35, 40, 45])
    # horizontal uniform beam hinged at wall, cable from end at angle th above horizontal
    T = (W * L / 2 + P * L) / (L * math.sin(math.radians(th)))
    H = T * math.cos(math.radians(th)); V = W + P - T * math.sin(math.radians(th))
    return Q(f'A uniform horizontal beam of length {nf(L)} m and weight {W} N is hinged to a wall at one end. A sign of weight {P} N hangs from the other end, which is held by a cable at {th}° above the horizontal attached to the wall. Calculate the tension in the cable and the horizontal and vertical components of the force at the hinge.',
             f'T = {f3(T)} N; hinge: horizontal {f3(H)} N, vertical {f3(abs(V))} N' + (' upwards' if V > 0 else ' downwards'),
             f'moments about hinge: T sin {th}° × {nf(L)} = {W} × {nf(L / 2)} + {P} × {nf(L)} [1]; T = {f3(T)} N [1]; horizontal: H = T cos {th}° = {f3(H)} N [1]; vertical: V = {W + P} − T sin {th}° = {f3(V)} N [1] [4]')


def _eq_c4(r, D):
    L = r.choice([4.0, 5.0, 6.0]); W = r.choice([300, 400, 500]); P = r.choice([600, 700, 800]); d = r.choice([1.0, 1.5])
    x = L * 0.75
    RB = (W * L / 2 + P * x) / L; RA = W + P - RB
    intro = r.choice([f'A uniform diving board of length {nf(L)} m and weight {W} N is supported at both ends A and B.', f'A uniform gangplank of length {nf(L)} m and weight {W} N rests on a support at each end, A and B, at a port in {city(r)}.'])
    parts = [
        lambda r: ('State the principle of moments.', 'In equilibrium, sum of clockwise moments = sum of anticlockwise moments about any point.', 'clockwise moments = anticlockwise moments [1]; about the same point, body in equilibrium [1] [2]'),
        lambda r: (f'A person of weight {P} N stands {nf(x)} m from A. Calculate the force at B.', f'{f3(RB)} N', 'moments about A [2]'),
        lambda r: ('Calculate the force at A.', f'{f3(RA)} N', 'vertical equilibrium [1]'),
        lambda r: ('Explain how the force at A changes as the person walks towards B.', 'It decreases, because the moment of the person\'s weight about B decreases.', 'decreases [1]; reason using moments [1] [2]'),
        lambda r: ('Explain why the weight of a uniform board can be taken to act at its midpoint.', 'For a uniform board the centre of gravity is at its geometric centre.', 'centre of gravity at centre [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t62.add('C4', (2, 3, 4, 5), 'multi_step')(_eq_c4)

N63 = 'Centre of gravity and stability'
t63 = topic(N63, N63.lower(), 'centre of gravity', 'stability')
FX(t63, 'C1', (1, 2), [
    ('What is meant by the centre of gravity of an object?', 'The point through which the whole weight of the object may be considered to act', 'Definition of centre of gravity.', ['The point where the mass is greatest', 'The geometric centre of every object', 'The lowest point of the object']),
    ('Which change makes a bus more stable?', 'Lowering its centre of gravity', 'A lower centre of gravity and wider base increase stability.', ['Raising its centre of gravity', 'Making its wheelbase narrower', 'Carrying heavy luggage on the roof']),
    ('An object will topple when', 'the vertical line through its centre of gravity falls outside its base', 'The weight then produces a moment that rotates it further over.', ['its centre of gravity is above its base', 'its weight is greater than its normal force', 'it has a wide base']),
    ('Where is the centre of gravity of a uniform metre rule?', 'At the 50 cm mark', 'For a uniform object it is at the geometric centre.', ['At the 0 cm mark', 'At the 100 cm mark', 'It depends on where it is pivoted']),
    ('A thin irregular lamina is hung freely from a pin. Where does its centre of gravity lie?', 'Vertically below the pin', 'In equilibrium the weight has no moment about the pin.', ['Vertically above the pin', 'At the pin', 'Horizontally to one side of the pin']),
    ('State the condition for an object resting on a surface not to topple.', 'The line of action of its weight must pass through its base.', 'vertical through c.g. within base [1]'),
])
FX(t63, 'C2', (1, 2, 3, 4), [
    ('Describe how to find the centre of gravity of an irregular piece of card.', 'Hang it freely from a pin through one hole with a plumb line; draw the vertical line; repeat from another hole; the centre of gravity is where the lines cross.', 'suspend freely with plumb line [1]; mark vertical [1]; repeat and intersect [1] [3]'),
    ('Explain why racing cars are designed to be low and wide.', 'A low centre of gravity and a wide base mean the car must tilt through a large angle before its weight acts outside the base, so it is less likely to topple on bends.', 'low c.g. [1]; wide base [1]; larger tilt needed to topple [1] [3]'),
    ('Explain why a person carrying a heavy bag in one hand leans the other way.', 'Leaning moves the combined centre of gravity back over the feet (the base) so there is no resultant moment that would cause toppling.', 'combined c.g. moves [1]; kept above base [1] [2]'),
    ('Explain why a tall, thin vase is easily knocked over.', 'Its centre of gravity is high and its base narrow, so only a small tilt moves the line of action of the weight outside the base, giving a toppling moment.', 'high c.g. and narrow base [1]; small tilt makes weight act outside base [1] [2]'),
])


@t63.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t63_topple(r, D):
    w = r.choice([0.40, 0.50, 0.60, 0.80, 1.0, 1.2]); h = r.choice([0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.4])
    obj = r.choice(['A uniform rectangular cabinet', 'A uniform block', 'A uniform bookcase', 'A fridge (treated as a uniform block)'])
    ang = math.degrees(math.atan((w / 2) / (h / 2)))
    s = f'{obj} has a base width of {nf(w)} m and a height of {nf(h)} m. It is tilted about one edge of its base.'
    if D <= 2:
        return numq(r, D, s, 'angle of tilt from the vertical at which it just topples (in degrees)', ang, '°', f'tan θ = (w/2)/(h/2) = {nf(w)}/{nf(h)}', [90 - ang, math.degrees(math.atan(w / h / 2)), math.degrees(math.atan(2 * w / h))], fm=f3)
    W = r.choice([300, 500, 800, 1200])
    F = W * (w / 2) / h
    return Q(s + f' Its weight is {W} N. (a) Calculate the angle of tilt at which it topples. (b) Calculate the minimum horizontal force applied at the top edge needed to start tipping it, assuming it does not slide.',
             f'(a) {f3(ang)}° (b) {f3(F)} N', f'(a) tan θ = {nf(w)}/{nf(h)} [1]; θ = {f3(ang)}° [1] (b) moments about the tipping edge: F × {nf(h)} = {W} × {nf(w / 2)} [1]; F = {f3(F)} N [1]' + (' [4]' if D <= 4 else '; c.g. at centre of uniform block [1] [5]'), 'multi_step')


@t63.add('C3', (2, 3, 4), 'numerical')
def t63_find(r, D):
    L = r.choice([1.0, 1.5, 2.0, 2.5]); W = r.choice([40, 60, 80, 120]); x = round(L * r.choice([0.3, 0.35, 0.4, 0.6, 0.65]), 2)
    # non-uniform rod on two scales at ends
    RB = W * x / L; RA = W - RB
    obj = r.choice(['A non-uniform plank', 'A non-uniform pole', 'A tapered wooden beam', 'A loaded stretcher'])
    return Q(f'{obj} of length {nf(L)} m rests horizontally on two bathroom scales, one at each end, A and B. Scale A reads {f3(RA)} N and scale B reads {f3(RB)} N. Determine the weight and the distance of the centre of gravity from A.',
             f'W = {f3(W)} N; {f3(x)} m from A', f'W = sum of readings = {f3(W)} N [1]; moments about A: {f3(W)} × x = {f3(RB)} × {nf(L)} [1]; x = {f3(x)} m [1] [3]')


def _cg_c4(r, D):
    w = r.choice([1.8, 2.0, 2.4]); h = r.choice([3.0, 3.5, 4.0]); W = r.choice([4.0e4, 6.0e4, 8.0e4])
    intro = r.choice([f'A double-decker bus is tested on a tilt table in {city(r)}. Its wheels are {nf(w)} m apart and its centre of gravity is {nf(h / 3)} m above the road, midway between the wheels.',
                      f'A loaded lorry has its wheels {nf(w)} m apart and its centre of gravity {nf(h / 3)} m above the road, midway between the wheels.'])
    hc = h / 3
    ang = math.degrees(math.atan((w / 2) / hc))
    parts = [
        lambda r: ('Define centre of gravity.', 'The point where the whole weight of the body may be taken to act.', 'definition [1]'),
        lambda r: ('Calculate the angle of tilt at which it would topple.', f'{f3(ang)}°', f'tan θ = {nf(w / 2)}/{nf(hc, 3)} [2]'),
        lambda r: ('Explain why loading passengers on the upper deck reduces the angle of tilt at which it topples.', 'The centre of gravity rises, so a smaller tilt moves the line of action of the weight outside the wheelbase.', 'c.g. higher [1]; smaller tilt needed [1] [2]'),
        lambda r: ('Explain, in terms of moments, why the vehicle returns upright if released before it reaches the toppling angle.', 'The weight acts inside the base, giving a restoring moment about the lower wheels.', 'weight inside base [1]; restoring moment [1] [2]'),
        lambda r: ('Suggest two design features that increase stability.', 'Wider wheelbase; heavy components (engine, fuel tank) mounted low.', 'wider base [1]; lower centre of gravity / heavy parts low [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t63.add('C4', (2, 3, 4, 5), 'multi_step')(_cg_c4)

CHAPTERS[6] = [t61, t62, t63]


# ===================================================================== 7 Density and pressure
MATS = [('aluminium', 2700), ('steel', 7800), ('copper', 8900), ('lead', 11300), ('brass', 8500), ('concrete', 2400), ('granite', 2700), ('oak', 750), ('ice', 920), ('glass', 2500)]
FLUIDS = [('water', 1000), ('sea water', 1030), ('oil', 900), ('mercury', 13600), ('glycerol', 1260), ('paraffin', 800)]

N71 = 'Density and pressure p = F/A'
t71 = topic(N71, N71.lower(), 'density', 'pressure')
FX(t71, 'C1', (1, 2), [
    ('Which is the definition of pressure?', 'Normal force per unit area', 'p = F/A with F perpendicular to the surface.', ['Force × area', 'Force per unit volume', 'Weight per unit mass']),
    ('Which is the definition of density?', 'Mass per unit volume', 'ρ = m/V.', ['Weight per unit volume', 'Volume per unit mass', 'Mass per unit area']),
    ('What is 1 g cm⁻³ in kg m⁻³?', '1000 kg m⁻³', '1 g cm⁻³ = 10⁻³ kg / 10⁻⁶ m³ = 10³ kg m⁻³.', ['1 kg m⁻³', '100 kg m⁻³', '0.001 kg m⁻³']),
    ('A force of 600 N acts on an area of 0.030 m². What is the pressure?', '2.0 × 10⁴ Pa', 'p = 600/0.030 = 20 000 Pa.', ['18 Pa', '5.0 × 10⁻⁵ Pa', '2.0 × 10² Pa']),
    ('Which unit is equivalent to the pascal?', 'N m⁻²', '1 Pa = 1 N m⁻².', ['N m', 'N m⁻¹', 'kg m⁻³']),
    ('A cube of side 2.0 cm has mass 64 g. What is its density?', '8.0 g cm⁻³', 'V = 8.0 cm³; ρ = 64/8.0.', ['32 g cm⁻³', '16 g cm⁻³', '4.0 g cm⁻³']),
    ('State why a sharp knife cuts more easily than a blunt one.', 'The contact area is smaller, so the same force gives a greater pressure.', 'smaller area → larger pressure [1]'),
])
FX(t71, 'C2', (1, 2, 3, 4), [
    ('Explain why snowshoes stop a person sinking into soft snow.', 'They spread the person\'s weight over a larger area, reducing the pressure on the snow below the value at which it gives way.', 'larger area [1]; smaller pressure for same weight [1] [2]'),
    ('Explain why the density of a gas is much lower than that of the same substance as a liquid.', 'The molecules in a gas are much further apart, so the same mass occupies a much larger volume.', 'molecules far apart [1]; larger volume for same mass [1] [2]'),
    ('Describe how to determine the density of an irregular stone in the laboratory.', 'Measure the mass on a balance; find the volume by displacement in a measuring cylinder (difference in readings); ρ = m/V; repeat and average.', 'mass by balance [1]; volume by displacement [1]; ρ = m/V [1] [3]'),
    ('Explain why a drawing pin has a broad head and a sharp point.', 'The force is the same at both ends; the broad head gives low pressure on the thumb, the small point gives a very high pressure that pierces the board.', 'same force both ends [1]; large area low pressure, small area high pressure [1] [2]'),
])


@t71.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t71_dens(r, D):
    mat, rho = r.choice(MATS)
    shape = r.choice(['cube', 'cylinder', 'sphere'])
    if shape == 'cube':
        a = r.choice([2.0, 3.0, 4.0, 5.0]) * 1e-2; V = a ** 3; dim = f'a cube of side {nf(a * 100)} cm'
    elif shape == 'cylinder':
        d = r.choice([2.0, 3.0, 4.0]) * 1e-2; L = r.choice([5.0, 8.0, 10.0]) * 1e-2; V = math.pi * d * d / 4 * L; dim = f'a cylinder of diameter {nf(d * 100)} cm and length {nf(L * 100)} cm'
    else:
        d = r.choice([2.0, 3.0, 4.0, 5.0]) * 1e-2; V = math.pi * d ** 3 / 6; dim = f'a sphere of diameter {nf(d * 100)} cm'
    m = rho * V
    if D <= 2:
        return numq(r, D, f'A sample of {mat} is {dim} with a mass of {f3(m * 1000)} g.', 'density in kg m⁻³', rho, ' kg m⁻³', f'V = {sci(V, 3)} m³; ρ = {sci(m, 3)}/{sci(V, 3)}', [rho / 1000, rho * 10, m / V / 100], fm=f3)
    W = m * GR
    if shape == 'cube':
        p = W / (a * a)
        return Q(f'A solid {mat} cube of side {nf(a * 100)} cm (density {rho} kg m⁻³) rests on a table. Calculate (a) its mass and (b) the pressure it exerts on the table.', f'(a) {f3(m)} kg (b) {f3(p)} Pa',
                 f'(a) m = ρV = {rho} × {sci(V, 3)} [1] = {f3(m)} kg [1] (b) p = mg/A = {f3(W)}/{sci(a * a, 3)} [1] = {f3(p)} Pa [1] [4]', 'multi_step')
    return Q(f'A sample of {mat} (density {rho} kg m⁻³) is {dim}. Calculate its volume and its mass.', f'V = {sci(V, 3)} m³; m = {f3(m)} kg', f'volume formula with lengths in m [1]; V = {sci(V, 3)} m³ [1]; m = ρV = {f3(m)} kg [1] [3]')


@t71.add('C3', (1, 2, 3, 4), 'numerical')
def t71_press(r, D):
    sc = r.choice([('an elephant standing on four feet', 5000, 4, 0.10), ('a woman standing on two stiletto heels', 60, 2, 1.0e-4), ('a car resting on four tyres', 1200, 4, 0.015),
                   ('a crate resting on its base', 250, 1, 0.80), ('a camel standing on four feet', 600, 4, 0.025), ('a tractor on four wide tyres', 4000, 4, 0.12)])
    what, m, n, A = sc
    W = m * GR; p = W / (n * A)
    if D <= 2:
        return numq(r, D, f'Estimate data: {what}; mass {m} kg, contact area {sci(A, 2) if A < 1e-3 else nf(A)} m² for each contact.', 'pressure on the ground', p, ' Pa', f'p = mg/(nA) = {f3(W)}/({n} × {sci(A, 2) if A < 1e-3 else nf(A)})', [m / (n * A), W / A, W * n * A], fm=f3)
    return Q(f'Compare the pressure exerted on the ground by {what} (mass {m} kg, contact area {sci(A, 2) if A < 1e-3 else nf(A)} m² for each of the {n} contact{"s" if n > 1 else ""}) with atmospheric pressure (1.0 × 10⁵ Pa), and comment on the result.',
             f'p = {f3(p)} Pa, which is {nf(p / 1e5, 2)} times atmospheric pressure.', f'weight = {f3(W)} N [1]; p = W/(total area) = {f3(p)} Pa [1]; comparison ratio {nf(p / 1e5, 2)} [1]; sensible comment [1] [4]')


def _dp_c4(r, D):
    mat, rho = r.choice(MATS[:6])
    a = r.choice([0.10, 0.20, 0.25]); b = r.choice([0.05, 0.10]); c = r.choice([0.40, 0.50, 0.60])
    V = a * b * c; m = rho * V; W = m * GR
    intro = r.choice([f'A rectangular block of {mat} (density {rho} kg m⁻³) measures {nf(a)} m × {nf(b)} m × {nf(c)} m.', f'An engineer in {city(r)} has a {mat} block {nf(a)} m by {nf(b)} m by {nf(c)} m, of density {rho} kg m⁻³.'])
    parts = [
        lambda r: ('Calculate its mass.', f'{f3(m)} kg', 'm = ρV [2]'),
        lambda r: ('Calculate its weight.', f'{f3(W)} N', 'W = mg [1]'),
        lambda r: ('Calculate the maximum pressure it can exert when resting on a flat floor.', f'{f3(W / (a * b))} Pa', f'smallest face {nf(a)} × {nf(b)} [2]'),
        lambda r: ('Calculate the minimum pressure it can exert on the floor.', f'{f3(W / (a * c) if a * c > b * c else W / (b * c))} Pa', 'largest face [2]'),
        lambda r: ('Explain why the pressure depends on which face it rests on although the weight does not change.', 'p = F/A: the force is constant but the area of contact differs.', 'p = F/A [1]; area changes [1] [2]'),
        lambda r: ('Define density.', 'Mass per unit volume.', 'definition [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t71.add('C4', (2, 3, 4, 5), 'multi_step')(_dp_c4)

N72 = 'Hydrostatic pressure Δp = ρgΔh'
t72 = topic(N72, N72.lower(), 'hydrostatic pressure', 'Δp = ρgΔh')
FX(t72, 'C1', (1, 2), [
    ('What is the pressure due to 10 m of water (density 1000 kg m⁻³)?', '9.8 × 10⁴ Pa', 'Δp = ρgh = 1000 × 9.81 × 10.', ['1.0 × 10⁴ Pa', '9.8 × 10² Pa', '9.8 × 10⁵ Pa']),
    ('The pressure at a point in a liquid at rest depends on', 'the depth and the density of the liquid', 'Δp = ρgΔh; it is independent of the shape of the container.', ['the shape of the container', 'the total volume of liquid', 'the area of the container base']),
    ('In a liquid at rest, the pressure at a given depth acts', 'equally in all directions', 'Fluid pressure at a point acts equally in all directions.', ['only downwards', 'only upwards', 'only sideways']),
    ('A diver descends from 5 m to 15 m in sea water of density 1030 kg m⁻³. What is the increase in pressure?', '1.0 × 10⁵ Pa', 'Δp = 1030 × 9.81 × 10 = 1.01 × 10⁵ Pa.', ['1.5 × 10⁵ Pa', '5.1 × 10⁴ Pa', '1.0 × 10⁴ Pa']),
    ('A manometer contains water. The difference in levels is 12 cm. What is the pressure difference?', '1.2 × 10³ Pa', 'Δp = 1000 × 9.81 × 0.12 = 1180 Pa.', ['1.2 × 10⁵ Pa', '1.2 Pa', '1.2 × 10² Pa']),
    ('State the equation for the pressure difference between two points in a fluid.', 'Δp = ρgΔh', 'Δp = ρgΔh [1]'),
])
FX(t72, 'C2', (1, 2, 3, 4), [
    ('Derive the equation Δp = ρgΔh for a column of liquid.', 'Consider a column of height Δh and base area A: volume AΔh, mass ρAΔh, weight ρAΔhg; pressure = weight/area = ρgΔh.', 'mass = ρAΔh [1]; weight ÷ area = ρgΔh [1] [2]'),
    ('Explain why a dam is built much thicker at the bottom than at the top.', 'Pressure in water increases with depth (Δp = ρgΔh), so the force on each square metre of the dam is largest at the bottom.', 'pressure increases with depth [1]; larger force near base needs thicker wall [1] [2]'),
    ('Explain why the total pressure at the bottom of a swimming pool is not just ρgh.', 'Atmospheric pressure acts on the surface and is transmitted through the water, so p = p_atm + ρgh.', 'atmospheric pressure acts on surface [1]; added to ρgh [1] [2]'),
    ('Explain why water in two connected tubes of different widths settles at the same height.', 'Pressure at the same depth in a connected fluid at rest must be equal; pressure depends only on depth, not on tube width, so the surfaces are level.', 'equal pressure at same level [1]; independent of width [1] [2]'),
])


@t72.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t72_depth(r, D):
    fl, rho = r.choice(FLUIDS[:3] + FLUIDS[4:])
    h = r.choice([2.5, 5.0, 8.0, 12.0, 20.0, 35.0, 50.0])
    sc = r.choice([f'A diver swims {nf(h)} m below the surface of {fl}', f'A pressure sensor is lowered to a depth of {nf(h)} m in a tank of {fl}', f'A submarine window is {nf(h)} m below the surface of {fl}'])
    dp = rho * GR * h
    if D <= 2:
        return numq(r, D, f'{sc} (density {rho} kg m⁻³).', 'pressure due to the liquid alone', dp, ' Pa', f'Δp = ρgh = {rho} × 9.81 × {nf(h)}', [rho * h, dp / GR / GR, dp * 10], fm=f3)
    pa = 1.01e5
    if D == 3:
        return Q(f'{sc} (density {rho} kg m⁻³). Atmospheric pressure is 1.01 × 10⁵ Pa. Calculate the total pressure at this depth.', f'{f3(dp + pa)} Pa', f'Δp = ρgh = {f3(dp)} Pa [1]; add atmospheric [1]; = {f3(dp + pa)} Pa [1] [3]')
    A = r.choice([0.020, 0.050, 0.080, 0.12])
    return Q(f'{sc} (density {rho} kg m⁻³). Atmospheric pressure is 1.01 × 10⁵ Pa. A circular window of area {nf(A)} m² faces sideways at this depth, with air at atmospheric pressure inside. (a) Calculate the total pressure outside. (b) Calculate the resultant force on the window. (c) Explain why pressure acts on a sideways-facing window.',
             f'(a) {f3(dp + pa)} Pa (b) {f3(dp * A)} N (c) pressure in a fluid acts equally in all directions.',
             f'(a) ρgh + p_atm = {f3(dp + pa)} Pa [1] (b) pressure difference = {f3(dp)} Pa [1]; F = ΔpA = {f3(dp * A)} N [1] (c) fluid pressure acts in all directions [1]' + (' [4]' if D == 4 else '; atmospheric pressure cancels on both sides [1] [5]'), 'multi_step')


@t72.add('C3', (2, 3, 4), 'numerical')
def t72_mano(r, D):
    fl, rho = r.choice([('water', 1000), ('oil', 900), ('mercury', 13600)])
    dh = r.choice([0.050, 0.080, 0.12, 0.15, 0.24]) if fl != 'mercury' else r.choice([0.020, 0.035, 0.050, 0.076])
    dp = rho * GR * dh
    sc = r.choice([f'A U-tube manometer containing {fl} (density {rho} kg m⁻³) is connected to a gas supply in a laboratory in {city(r)}.', f'A {fl} manometer (density {rho} kg m⁻³) measures the pressure of air in a blown-up balloon.'])
    return Q(sc + f' The liquid level on the open side is {nf(dh * 100)} cm higher than on the gas side. Atmospheric pressure is 1.01 × 10⁵ Pa. Calculate the pressure of the gas.', f'{f3(1.01e5 + dp)} Pa',
             f'Δp = ρgΔh = {rho} × 9.81 × {nf(dh)} = {f3(dp)} Pa [1]; gas pressure is greater than atmospheric as open side higher [1]; p = {f3(1.01e5 + dp)} Pa [1] [3]')


relation(t72, 'C2', (2, 3), 'Δp = ρgΔh', 'pressure due to the liquid', {'depth': 1, 'density of the liquid': 1},
         ['A pressure sensor is held in a tank of liquid.', 'A diver measures the pressure due to the water above her.', 'A water storage tank supplies water to taps below it.'])


def _hyd_c4(r, D):
    h = r.choice([8.0, 10.0, 15.0]); rho = 1030
    intro = r.choice([f'A diver in the sea near {city(r)} (sea water density 1030 kg m⁻³) descends to {nf(h)} m. Atmospheric pressure is 1.01 × 10⁵ Pa.', f'An underwater camera housing is lowered to a depth of {nf(h)} m in sea water of density 1030 kg m⁻³; atmospheric pressure is 1.01 × 10⁵ Pa.'])
    dp = rho * GR * h
    parts = [
        lambda r: ('Calculate the pressure due to the water at this depth.', f'{f3(dp)} Pa', 'ρgh [2]'),
        lambda r: ('Calculate the total pressure at this depth.', f'{f3(dp + 1.01e5)} Pa', 'add atmospheric [1]'),
        lambda r: ('Calculate the depth at which the total pressure is double atmospheric pressure.', f'{f3(1.01e5 / (rho * GR))} m', 'ρgh = p_atm [2]'),
        lambda r: ('Show that Δp = ρgΔh by considering a column of water.', 'weight of column ρAΔhg divided by area A gives ρgΔh', 'mass of column [1]; divide by area [1] [2]'),
        lambda r: ('Explain why the pressure on the diver\'s ears is the same whether she faces up, down or sideways.', 'Pressure at a point in a fluid acts equally in all directions.', 'acts in all directions [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t72.add('C4', (2, 3, 4, 5), 'multi_step')(_hyd_c4)

N73 = "Upthrust and Archimedes' principle F = ρgV"
t73 = topic(N73, N73.lower(), 'upthrust', "archimedes' principle")
FX(t73, 'C1', (1, 2), [
    ("Which statement is Archimedes' principle?", 'The upthrust on a body is equal to the weight of the fluid it displaces', 'F = ρ_fluid g V_displaced.', ['The upthrust equals the weight of the body', 'The upthrust equals the mass of fluid displaced', 'The upthrust equals the pressure at the bottom of the body']),
    ('A block of volume 2.0 × 10⁻³ m³ is fully submerged in water (density 1000 kg m⁻³). What is the upthrust?', '19.6 N', 'F = ρgV = 1000 × 9.81 × 2.0 × 10⁻³.', ['2.0 N', '196 N', '0.20 N']),
    ('Upthrust arises because', 'the pressure on the bottom of an object is greater than the pressure on its top', 'Pressure increases with depth, giving a net upward force.', ['the object is less dense than the fluid', 'the weight of the object acts upwards', 'the fluid attracts the object']),
    ('A floating object is in equilibrium. Which is correct?', 'Upthrust = weight of the object', 'Zero resultant force.', ['Upthrust > weight of the object', 'Upthrust = 0', 'Weight of displaced fluid > weight of the object']),
    ('A solid sinks in water. Its apparent weight in water is', 'its weight minus the upthrust', 'Apparent weight = W − F_up.', ['its weight plus the upthrust', 'equal to the upthrust', 'zero']),
    ('State the equation for the upthrust on a body fully immersed in a fluid.', 'F = ρgV, where ρ is the density of the fluid and V is the volume of the body.', 'F = ρgV with ρ of fluid [1]'),
])
FX(t73, 'C2', (1, 2, 3, 4), [
    ('Use the idea of pressure to explain why a fully submerged block experiences an upthrust.', 'The bottom face is deeper than the top face, so the pressure there is greater (Δp = ρgΔh); the upward force on the bottom exceeds the downward force on the top.', 'pressure greater at bottom [1]; resultant upward force [1] [2]'),
    ('Show that the upthrust on a cuboid of height h and face area A submerged vertically in a fluid of density ρ is ρgV.', 'Force difference = (p_bottom − p_top)A = ρghA = ρgV, since V = Ah.', 'pressure difference ρgh [1]; × A = ρgV [1] [2]'),
    ('Explain why a ship floats higher in sea water than in fresh water.', 'Sea water is denser; the same upthrust (equal to the ship\'s weight) is produced by a smaller volume of displaced water.', 'same upthrust = weight [1]; denser fluid → less volume displaced [1] [2]'),
    ('Explain why a helium balloon rises in air but a balloon filled with air does not.', 'Upthrust = weight of air displaced; the helium balloon\'s total weight is less than this, giving a resultant upward force; the air balloon\'s weight (air + rubber) exceeds it.', 'upthrust = weight of displaced air [1]; comparison of weights [1] [2]'),
])


@t73.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t73_up(r, D):
    mat, rho = r.choice([m for m in MATS if m[1] > 1100])
    fl, rf = r.choice(FLUIDS[:3])
    V = r.choice([2.0e-4, 5.0e-4, 8.0e-4, 1.2e-3, 2.5e-3, 4.0e-3])
    U = rf * GR * V; W = rho * GR * V
    sc = f'A {mat} block of volume {sci(V, 2)} m³ is fully immersed in {fl} (density {rf} kg m⁻³), hanging from a newton meter.'
    if D <= 2:
        return numq(r, D, sc, 'upthrust on the block', U, ' N', f'F = ρgV = {rf} × 9.81 × {sci(V, 2)}', [W, rf * V, U * 10], fm=f3)
    if D == 3:
        return Q(sc + f' The density of {mat} is {rho} kg m⁻³. Calculate the reading on the newton meter.', f'{f3(W - U)} N', f'W = ρ_block gV = {f3(W)} N [1]; upthrust = {f3(U)} N [1]; reading = W − U = {f3(W - U)} N [1] [3]')
    Wa = W - U
    return Q(f'A metal object weighs {f3(W)} N in air and {f3(Wa)} N when fully immersed in {fl} (density {rf} kg m⁻³). (a) Calculate the upthrust. (b) Calculate the volume of the object. (c) Determine its density and suggest what it is made of.',
             f'(a) {f3(U)} N (b) {sci(V, 3)} m³ (c) {f3(rho)} kg m⁻³: {mat}',
             f'(a) {f3(W)} − {f3(Wa)} = {f3(U)} N [1] (b) V = U/(ρg) = {sci(V, 3)} m³ [1] (c) m = W/g = {f3(W / GR)} kg [1]; ρ = m/V = {f3(rho)} kg m⁻³ [1]' + (' [4]' if D == 4 else f'; identifies {mat} [1] [5]'), 'multi_step')


@t73.add('C3', (2, 3, 4), 'numerical')
def t73_float(r, D):
    mat, rho = r.choice([('oak', 750), ('pine', 500), ('ice', 920), ('polystyrene', 50), ('cork', 240), ('plastic', 850)])
    fl, rf = r.choice(FLUIDS[:3])
    if rho >= rf:
        return None
    frac = rho / rf
    V = r.choice([0.010, 0.020, 0.050, 0.080, 0.12])
    return Q(f'A block of {mat} (density {rho} kg m⁻³) of volume {nf(V)} m³ floats in {fl} (density {rf} kg m⁻³). Calculate the fraction of its volume below the surface and the upthrust on it.',
             f'fraction {nf(frac, 3)}; upthrust {f3(rho * V * GR)} N', f'floating: upthrust = weight [1]; ρ_f g V_sub = ρ g V so V_sub/V = {rho}/{rf} = {nf(frac, 3)} [1]; upthrust = weight = {f3(rho * V * GR)} N [1] [3]')


def _up_c4(r, D):
    V = r.choice([0.50, 0.80, 1.2]); m = r.choice([200, 300, 400]); rf = 1030
    intro = r.choice([f'A buoy of volume {nf(V)} m³ and mass {m} kg floats in sea water (density 1030 kg m⁻³) in a harbour at {city(r)}.', f'A sealed drum of volume {nf(V)} m³ and mass {m} kg is used as a float in sea water of density 1030 kg m⁻³.'])
    parts = [
        lambda r: ("State Archimedes' principle.", 'The upthrust equals the weight of fluid displaced.', 'statement [1]'),
        lambda r: ('Calculate the upthrust when the buoy floats.', f'{f3(m * GR)} N', 'equals weight mg [1]'),
        lambda r: ('Calculate the volume of the buoy below the water surface.', f'{f3(m / rf)} m³', 'V = m/ρ_f [2]'),
        lambda r: ('Calculate the extra downward force needed to submerge it completely.', f'{f3(rf * GR * V - m * GR)} N', 'full upthrust − weight [2]'),
        lambda r: ('Explain why the upthrust does not increase further once the buoy is fully submerged and pushed deeper.', 'The displaced volume no longer changes, and pressure difference between top and bottom stays ρgh (h = height of buoy).', 'volume displaced constant [1]; pressure difference unchanged [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t73.add('C4', (2, 3, 4, 5), 'multi_step')(_up_c4)

CHAPTERS[7] = [t71, t72, t73]

# ===================================================================== 8 Work, energy and power
N81 = 'Work done as force × displacement in the direction of the force'
t81 = topic(N81, N81.lower(), 'work done', 'force × displacement')
FX(t81, 'C1', (1, 2), [
    ('Which is the definition of work done by a force?', 'Force × displacement in the direction of the force', 'W = Fs cos θ.', ['Force × distance moved in any direction', 'Force × time', 'Force ÷ displacement']),
    ('A force of 50 N pulls a box 4.0 m along the floor in the direction of the force. What work is done?', '200 J', 'W = 50 × 4.0.', ['12.5 J', '54 J', '0.08 J']),
    ('A force of 20 N acts at 60° to the direction of motion of an object that moves 5.0 m. What work is done by the force?', '50 J', 'W = Fs cos 60° = 20 × 5.0 × 0.5.', ['100 J', '87 J', '4.0 J']),
    ('A satellite moves in a circular orbit at constant speed. How much work does gravity do on it?', 'zero', 'The gravitational force is perpendicular to the motion.', ['mg × orbit circumference', 'equal to its kinetic energy', 'equal to its potential energy']),
    ('One joule is the work done when', 'a force of 1 N moves its point of application 1 m in the direction of the force', 'Definition of the joule.', ['a force of 1 N acts for 1 s', 'a mass of 1 kg moves 1 m', 'a power of 1 W acts for 1 m']),
    ('State the principle of conservation of energy.', 'Energy cannot be created or destroyed; it can only be transferred from one form to another (total energy of a closed system is constant).', 'cannot be created or destroyed [1]'),
])
FX(t81, 'C2', (1, 2, 3, 4), [
    ('Explain why a person holding a heavy suitcase at rest does no work on it.', 'Work = force × displacement in the direction of the force; the suitcase does not move, so no work is done on it (although the muscles transfer energy internally).', 'no displacement [1]; W = Fs = 0 [1] [2]'),
    ('Explain why the work done by the normal contact force on a box sliding along a horizontal floor is zero.', 'The normal force is perpendicular to the displacement (θ = 90°, cos 90° = 0), so no work is done.', 'perpendicular [1]; cos 90° = 0 [1] [2]'),
    ('Explain why work done against friction results in an increase in thermal energy.', 'The force does work over a displacement but the kinetic energy does not increase; the energy is transferred to internal (thermal) energy of the surfaces.', 'work done against friction [1]; energy transferred to thermal energy of surfaces [1] [2]'),
    ('Explain why it is easier to push a load up a long gentle ramp than to lift it straight up, although the work done against gravity is the same.', 'The work mgh is the same, but over a longer distance a smaller force is needed (W = Fs).', 'same work mgh [1]; longer distance, smaller force [1] [2]'),
])


@t81.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t81_work(r, D):
    F = r.choice([30, 40, 60, 80, 120, 150, 250]); s = r.choice([2.0, 3.5, 5.0, 8.0, 12.0, 20.0]); th = r.choice([0, 20, 25, 30, 35, 40, 45, 60])
    sc = r.choice([f'A child pulls a sledge {nf(s)} m across snow with a rope that makes {th}° with the horizontal; the tension is {F} N.', f'A worker pulls a crate {nf(s)} m along a floor using a rope at {th}° to the floor with a force of {F} N.', f'A tug pulls a barge {nf(s)} m with a cable at {th}° to the direction of motion and tension {F} N.'])
    if th == 0:
        sc = sc.replace(f' that makes {th}° with the horizontal', ' held horizontally').replace(f' at {th}° to the floor', ' held parallel to the floor').replace(f' at {th}° to the direction of motion', ' parallel to the motion')
    W = F * s * math.cos(math.radians(th))
    if D <= 2:
        return numq(r, D, sc, 'work done by the tension', W, ' J', f'W = Fs cos θ = {F} × {nf(s)} × cos {th}°', [F * s, F * s * math.sin(math.radians(th)) or F * s / 2, F / s], fm=f3)
    fr = round(F * math.cos(math.radians(th)) * r.choice([0.6, 0.8, 1.0]), 1)
    return Q(sc + f' A friction force of {nf(fr)} N acts on the load. Calculate the work done by the tension, the work done against friction and the gain in kinetic energy.',
             f'{f3(W)} J; {f3(fr * s)} J; {f3(W - fr * s)} J', f'W_T = Fs cos θ = {f3(W)} J [1]; W_f = {nf(fr)} × {nf(s)} = {f3(fr * s)} J [1]; ΔKE = difference = {f3(W - fr * s)} J [1]' + (' [3]' if D == 3 else '; justification via work-energy principle [1] [4]'))


@t81.add('C3', (2, 3, 4), 'numerical')
def t81_graph(r, D):
    F1 = r.choice([10, 20, 30, 40]); F2 = F1 + r.choice([20, 30, 40, 60]); s = r.choice([0.50, 1.0, 2.0, 4.0])
    W = 0.5 * (F1 + F2) * s
    return Q(f'The force on a trolley increases uniformly from {F1} N to {F2} N as it moves {nf(s)} m in the direction of the force. Calculate the work done, explaining how it is obtained from a force-displacement graph.',
             f'{f3(W)} J', f'work = area under F-s graph [1]; trapezium ½({F1} + {F2}) × {nf(s)} [1]; = {f3(W)} J [1] [3]')


def _work_c4(r, D):
    m = r.choice([40, 60, 80]); th = r.choice([20, 25, 30]); s = r.choice([5.0, 8.0, 10.0]); F = r.choice([300, 400, 500]); fr = r.choice([40, 60, 80])
    h = s * math.sin(math.radians(th))
    intro = r.choice([f'A crate of mass {m} kg is pushed {nf(s)} m up a ramp inclined at {th}° to the horizontal by a force of {F} N parallel to the ramp. A friction force of {fr} N acts.', f'In a warehouse in {city(r)}, a {m} kg box is pushed {nf(s)} m up a {th}° slope with a force of {F} N along the slope against friction of {fr} N.'])
    parts = [
        lambda r: ('Calculate the work done by the pushing force.', f'{f3(F * s)} J', 'W = Fs [1]'),
        lambda r: ('Calculate the gain in gravitational potential energy.', f'{f3(m * GR * h)} J', f'h = {nf(s)} sin {th}° [2]'),
        lambda r: ('Calculate the work done against friction.', f'{f3(fr * s)} J', 'W = fs [1]'),
        lambda r: ('Calculate the gain in kinetic energy.', f'{f3(F * s - fr * s - m * GR * h)} J', 'work-energy balance [2]'),
        lambda r: ('Explain why the normal contact force does no work.', 'It is perpendicular to the displacement.', 'perpendicular [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t81.add('C4', (2, 3, 4, 5), 'multi_step')(_work_c4)

N82 = 'Gravitational potential energy and kinetic energy and their derivations'
t82 = topic(N82, N82.lower(), 'gravitational potential energy', 'kinetic energy')
FX(t82, 'C1', (1, 2), [
    ('A 2.0 kg mass is raised through 3.0 m. What is its gain in gravitational potential energy?', '59 J', 'ΔE = mgΔh = 2.0 × 9.81 × 3.0.', ['6.0 J', '29 J', '590 J']),
    ('What is the kinetic energy of a 0.50 kg ball moving at 4.0 m s⁻¹?', '4.0 J', 'E = ½mv² = 0.5 × 0.50 × 16.', ['1.0 J', '8.0 J', '2.0 J']),
    ('The speed of a car doubles. Its kinetic energy', 'is multiplied by 4', 'E ∝ v².', ['doubles', 'halves', 'stays the same']),
    ('The equation ΔE = mgΔh is valid', 'only for small changes in height near the Earth\'s surface where g is constant', 'It assumes a uniform gravitational field.', ['for any change in height', 'only in a vacuum', 'only for objects at rest']),
    ('A ball falls from rest through 5.0 m. Ignoring air resistance, its speed is', '9.9 m s⁻¹', 'v = √(2gh) = √(98.1).', ['49 m s⁻¹', '7.0 m s⁻¹', '98 m s⁻¹']),
    ('State what is meant by kinetic energy.', 'The energy an object has because of its motion.', 'energy due to motion [1]'),
])
FX(t82, 'C2', (1, 2, 3, 4), [
    ('Derive the equation E_k = ½mv² for a body accelerated from rest by a constant force.', 'Work done W = Fs = (ma)s; with v² = 2as from rest, as = v²/2; so W = m(v²/2) = ½mv², which becomes kinetic energy.', 'W = Fs = mas [1]; v² = 2as [1]; substitution gives ½mv² [1] [3]'),
    ('Derive ΔE_p = mgΔh for an object lifted at constant speed.', 'The lifting force equals the weight mg; work done = force × distance = mgΔh, which is stored as gravitational potential energy.', 'force = mg at constant speed [1]; W = mgΔh [1] [2]'),
    ('Explain why a pendulum bob swinging in air eventually stops.', 'Work is done against air resistance (and friction at the pivot), so the mechanical energy is gradually transferred to thermal energy of the surroundings.', 'work against air resistance/friction [1]; energy transferred to thermal [1] [2]'),
    ('Explain why a ball dropped from a height h reaches the same speed whatever its mass, if air resistance is negligible.', 'mgh = ½mv², and m cancels, so v = √(2gh) is independent of mass.', 'energy equation [1]; mass cancels [1] [2]'),
])


@t82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t82_energy(r, D):
    h = r.choice([1.5, 2.5, 4.0, 8.0, 12.0, 25.0])
    fr_, ms = r.choice([('A roller-coaster car of mass {m} kg descends a vertical height of {h} m from rest', [400, 500, 650]), ('A ball of mass {m} kg falls from rest through {h} m', [0.20, 0.45, 0.60]),
                        ('A skier of mass {m} kg slides from rest down a slope with a vertical drop of {h} m', [55, 60, 70, 80]), ('A sledge and rider of total mass {m} kg slide from rest down a hill with a vertical drop of {h} m', [40, 50, 75])])
    if 'ball' in fr_:
        h = min(h, 8.0)
    m = r.choice(ms)
    sc = fr_.format(m=nf(m), h=nf(h))
    v = math.sqrt(2 * GR * h); Ep = m * GR * h
    if D <= 2:
        return numq(r, D, sc + '. Resistive forces are negligible.', 'speed at the bottom', v, ' m s⁻¹', f'mgh = ½mv² → v = √(2 × 9.81 × {nf(h)})', [2 * GR * h, math.sqrt(GR * h), GR * h / 2], fm=f3)
    frac = r.choice([0.10, 0.15, 0.20, 0.25, 0.30])
    vr = math.sqrt(2 * GR * h * (1 - frac))
    if D == 3:
        return Q(sc + f'. {nf(frac * 100)}% of the potential energy lost is transferred to thermal energy by resistive forces. Calculate its speed at the bottom.', f'{f3(vr)} m s⁻¹',
                 f'ΔE_p = mgh = {f3(Ep)} J [1]; E_k = {nf(1 - frac, 2)} × {f3(Ep)} J [1]; v = √(2E_k/m) = {f3(vr)} m s⁻¹ [1] [3]')
    if 'falls' in sc:
        return None
    s = r.choice([20, 30, 40, 60])
    fr = Ep * frac / s
    return Q(sc + f' along a path of length {s} m and reaches a speed of {f3(vr)} m s⁻¹. (a) Calculate the loss of gravitational potential energy. (b) Calculate the kinetic energy at the bottom. (c) Calculate the average resistive force along the path.',
             f'(a) {f3(Ep)} J (b) {f3(Ep * (1 - frac))} J (c) {f3(fr)} N', f'(a) mgh = {f3(Ep)} J [1] (b) ½mv² = {f3(Ep * (1 - frac))} J [1] (c) energy lost = {f3(Ep * frac)} J [1]; F = {f3(Ep * frac)}/{s} = {f3(fr)} N [1]' + (' [4]' if D == 4 else '; assumption that resistive force is constant [1] [5]'), 'multi_step')


@t82.add('C3', (2, 3, 4), 'numerical')
def t82_throw(r, D):
    m = r.choice([0.15, 0.20, 0.45, 0.60]); u = r.choice([8.0, 10.0, 12.0, 15.0, 20.0]); h = r.choice([5.0, 10.0, 15.0])
    v = math.sqrt(u * u + 2 * GR * h)
    return Q(f'A ball of mass {nf(m)} kg is thrown from the top of a building {nf(h)} m high with a speed of {nf(u)} m s⁻¹. Use energy considerations to calculate its speed just before it hits the ground, ignoring air resistance. Explain why the direction of the throw does not matter.',
             f'{f3(v)} m s⁻¹; energy is a scalar, so the final kinetic energy depends only on initial KE and height lost.', f'½mu² + mgh = ½mv² [1]; v = √({nf(u)}² + 2 × 9.81 × {nf(h)}) = {f3(v)} m s⁻¹ [1]; energy is scalar / independent of direction [1] [3]')


def _ke_c4(r, D):
    m = r.choice([0.050, 0.10, 0.20]); h = r.choice([1.2, 1.8, 2.5]); hb = h * r.choice([0.6, 0.7, 0.8])
    intro = r.choice([f'A ball of mass {nf(m)} kg is dropped from rest from a height of {nf(h)} m onto a hard floor in {lab(r)}. It rebounds to a height of {nf(hb, 3)} m.', f'{person(r)} drops a {nf(m)} kg rubber ball from {nf(h)} m; it bounces back up to {nf(hb, 3)} m.'])
    parts = [
        lambda r: ('Calculate the speed just before impact.', f'{f3(math.sqrt(2 * GR * h))} m s⁻¹', 'v = √(2gh) [2]'),
        lambda r: ('Calculate the speed just after the bounce.', f'{f3(math.sqrt(2 * GR * hb))} m s⁻¹', 'v = √(2gh) [2]'),
        lambda r: ('Calculate the kinetic energy lost in the bounce.', f'{f3(m * GR * (h - hb))} J', 'mg(h − h_b) [2]'),
        lambda r: ('Calculate the change in momentum of the ball during the bounce.', f'{f3(m * (math.sqrt(2 * GR * h) + math.sqrt(2 * GR * hb)))} kg m s⁻¹', 'velocity reverses: m(v₁ + v₂) [2]'),
        lambda r: ('Derive the expression for gravitational potential energy change ΔE = mgΔh.', 'work = force × distance = mg × Δh', 'force mg [1]; × Δh [1] [2]'),
        lambda r: ('State and explain whether the bounce is elastic.', 'Inelastic: kinetic energy is lost (rebound height is less).', 'inelastic with reason [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t82.add('C4', (2, 3, 4, 5), 'multi_step')(_ke_c4)

N83 = 'Work done by a gas: W = pΔV'
t83 = topic(N83, N83.lower(), 'work done by a gas', 'w = pδv')
FX(t83, 'C1', (1, 2), [
    ('A gas expands at constant pressure p from volume V₁ to V₂. What work does it do?', 'p(V₂ − V₁)', 'W = pΔV at constant pressure.', ['p(V₁ + V₂)', 'pV₂', '(V₂ − V₁)/p']),
    ('A gas at 2.0 × 10⁵ Pa expands by 3.0 × 10⁻³ m³ at constant pressure. What work is done by the gas?', '600 J', 'W = 2.0 × 10⁵ × 3.0 × 10⁻³.', ['60 J', '6000 J', '1.5 × 10⁻⁸ J']),
    ('On a graph of pressure against volume, the work done by a gas is represented by', 'the area under the line', 'W = ∫p dV.', ['the gradient of the line', 'the intercept on the pressure axis', 'the product of the final pressure and volume']),
    ('When a gas is compressed at constant pressure, the work done by the gas is', 'negative (work is done on the gas)', 'ΔV is negative.', ['positive', 'zero', 'equal to its internal energy']),
    ('Which unit is the same as Pa m³?', 'J', 'N m⁻² × m³ = N m = J.', ['W', 'N', 'Pa']),
    ('State the condition under which W = pΔV can be used.', 'The pressure stays constant during the volume change.', 'constant pressure [1]'),
])
FX(t83, 'C2', (1, 2, 3, 4), [
    ('Derive W = pΔV for a gas pushing a piston of area A through a distance Δx.', 'Force on piston F = pA; work = FΔx = pAΔx = pΔV since AΔx = ΔV.', 'F = pA [1]; W = pAΔx = pΔV [1] [2]'),
    ('Explain why a gas expanding against a piston does work.', 'The gas exerts a force on the piston (pressure × area) and the piston moves in the direction of that force, so work is done by the gas.', 'force from pressure on piston [1]; displacement in direction of force [1] [2]'),
    ('Explain why W = pΔV cannot be used directly for a gas whose pressure changes during expansion.', 'p is not constant; the work must be found from the area under the p-V graph instead.', 'pressure varies [1]; use area under p-V graph [1] [2]'),
])


@t83.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t83_w(r, D):
    p = r.choice([1.0e5, 1.5e5, 2.0e5, 2.5e5, 3.0e5]); V1 = r.choice([1.0e-3, 2.0e-3, 2.5e-3, 4.0e-3]); dV = r.choice([0.5e-3, 1.0e-3, 1.5e-3, 3.0e-3])
    sc = r.choice([f'Gas in a cylinder at a constant pressure of {sci(p, 2)} Pa expands from {sci(V1, 2)} m³ to {sci(V1 + dV, 2)} m³, pushing a piston.', f'Air in a syringe is heated and expands at constant pressure {sci(p, 2)} Pa from {sci(V1, 2)} m³ to {sci(V1 + dV, 2)} m³.',
                    f'The gas in an engine cylinder at a constant {sci(p, 2)} Pa increases in volume from {sci(V1, 2)} m³ to {sci(V1 + dV, 2)} m³.'])
    W = p * dV
    if D <= 2:
        return numq(r, D, sc, 'work done by the gas', W, ' J', f'W = pΔV = {sci(p, 2)} × {sci(dV, 2)}', [p * (V1 + dV), p * V1, W / 10], fm=f3)
    A = r.choice([2.0e-3, 4.0e-3, 5.0e-3, 8.0e-3])
    return Q(sc + f' The piston has area {sci(A, 2)} m². Calculate the work done by the gas, the force on the piston and the distance the piston moves. Show that your answers are consistent.',
             f'W = {f3(W)} J; F = {f3(p * A)} N; d = {f3(dV / A)} m; F × d = {f3(W)} J', f'W = pΔV = {f3(W)} J [1]; F = pA = {f3(p * A)} N [1]; d = ΔV/A = {f3(dV / A)} m [1]; Fd = pΔV check [1] [4]')


@t83.add('C3', (3, 4, 5), 'case')
def t83_pv(r, D):
    p1 = r.choice([1.0e5, 2.0e5, 3.0e5]); V1 = r.choice([1.0e-3, 2.0e-3]); V2 = V1 * r.choice([2, 3]); p2 = p1 * V1 / V2
    W_iso = 0.5 * (p1 + p2) * (V2 - V1)
    return Q(f'A gas expands from {sci(V1, 2)} m³ at {sci(p1, 2)} Pa to {sci(V2, 2)} m³ at {sci(p2, 3)} Pa. On a p-V graph the path is approximated as a straight line. (a) Estimate the work done by the gas. (b) Explain why W = pΔV cannot be used with a single value of p. (c) State how the estimate would compare with the true value if the true path curves below the straight line.',
             f'(a) {f3(W_iso)} J (b) the pressure changes during the expansion (c) the true work is smaller (less area under the curve).',
             f'(a) area of trapezium ½(p₁ + p₂)ΔV [1]; = {f3(W_iso)} J [1] (b) p not constant [1] (c) smaller area so overestimate [1] [4]')


def _gas_c4(r, D):
    p = r.choice([1.2e5, 1.5e5, 2.0e5]); dV = r.choice([2.0e-4, 4.0e-4, 6.0e-4]); Q_ = r.choice([150, 200, 250])
    intro = r.choice([f'A gas in a cylinder with a freely moving piston is heated in {lab(r)}. The pressure stays at {sci(p, 2)} Pa and the volume increases by {sci(dV, 2)} m³. {Q_} J of thermal energy is supplied.', f'The gas in a balloon-type actuator expands by {sci(dV, 2)} m³ at a constant {sci(p, 2)} Pa when {Q_} J of heat is supplied.'])
    W = p * dV
    parts = [
        lambda r: ('Calculate the work done by the gas.', f'{f3(W)} J', 'W = pΔV [2]'),
        lambda r: ('Calculate the increase in internal energy of the gas.', f'{f3(Q_ - W)} J', 'heat supplied − work done by gas [2]'),
        lambda r: ('Derive W = pΔV for a piston of area A.', 'F = pA, W = FΔx = pAΔx = pΔV', 'F = pA [1]; AΔx = ΔV [1] [2]'),
        lambda r: ('Sketch the p-V graph for this change and shade the work done.', 'horizontal line at constant p from V₁ to V₂; rectangle under it shaded', 'horizontal line [1]; area shaded [1] [2]'),
        lambda r: ('State what would happen to the work done if the same expansion occurred at twice the pressure.', 'It would double.', 'doubles [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t83.add('C4', (2, 3, 4, 5), 'multi_step')(_gas_c4)

N84 = 'Power P = W/t = Fv and efficiency'
t84 = topic(N84, N84.lower(), 'power', 'efficiency')
FX(t84, 'C1', (1, 2), [
    ('Which is the definition of power?', 'Work done per unit time', 'P = W/t.', ['Work done × time', 'Force × distance', 'Energy per unit distance']),
    ('A car moves at a constant 25 m s⁻¹ against a resistive force of 800 N. What useful power does the engine deliver?', '20 kW', 'P = Fv = 800 × 25.', ['32 W', '825 W', '2.0 kW']),
    ('A motor lifts a 50 kg load through 6.0 m in 10 s. What is the useful power output?', '294 W', 'P = mgh/t = 50 × 9.81 × 6.0/10.', ['30 W', '2940 W', '3000 W']),
    ('A machine has an input power of 400 W and a useful output power of 300 W. What is its efficiency?', '75%', 'Efficiency = 300/400.', ['133%', '25%', '0.75%']),
    ('Which unit is equivalent to the watt?', 'J s⁻¹', '1 W = 1 J s⁻¹.', ['J s', 'N s', 'N m s']),
    ('A lamp has an efficiency of 20%. For every 100 J of electrical energy supplied, how much is wasted?', '80 J', 'Useful 20 J; wasted 80 J.', ['20 J', '100 J', '120 J']),
    ('State the equation linking power, force and velocity.', 'P = Fv', 'P = Fv [1]'),
])
FX(t84, 'C2', (1, 2, 3, 4), [
    ('Derive P = Fv from the definition of power.', 'P = W/t = Fs/t = F(s/t) = Fv, for a constant force in the direction of motion at velocity v.', 'P = W/t and W = Fs [1]; s/t = v [1] [2]'),
    ('Explain why no machine can have an efficiency greater than 100%.', 'Energy is conserved, so the useful output energy cannot exceed the input; some energy is always transferred to wasted forms (e.g. thermal) by friction.', 'conservation of energy [1]; output ≤ input, always some loss [1] [2]'),
    ('Explain why a car needs more power to travel at a constant high speed than at a constant low speed.', 'At constant speed driving force = resistive force, which increases with speed; P = Fv increases because both F and v are larger.', 'resistive force increases with v [1]; P = Fv so increases [1] [2]'),
    ('Two cranes lift identical loads to the same height, one in half the time. Compare the work done and the power.', 'Same work done (mgh) but the faster crane has twice the power (P = W/t).', 'same work [1]; double power [1] [2]'),
])


@t84.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t84_power(r, D):
    kind = r.choice(['lift', 'car', 'pump'])
    if kind == 'lift':
        m = r.choice([200, 300, 450, 600, 800]); h = r.choice([8.0, 12.0, 15.0, 20.0, 30.0]); t = r.choice([10, 15, 20, 25, 30]); eff = r.choice([0.40, 0.50, 0.60, 0.75, 0.80])
        Pu = m * GR * h / t
        s = f'An electric motor in {city(r)} lifts a load of {m} kg through a height of {nf(h)} m at constant speed in {t} s.'
        if D <= 2:
            return numq(r, D, s, 'useful power output', Pu, ' W', f'P = mgh/t = {m} × 9.81 × {nf(h)}/{t}', [m * h / t, m * GR * h * t, m * GR * h], fm=f3)
        return Q(s + f' The motor is {nf(eff * 100)}% efficient. Calculate the useful power, the input power and the energy wasted in the {t} s.', f'{f3(Pu)} W; {f3(Pu / eff)} W; {f3(Pu / eff * t - Pu * t)} J',
                 f'P_out = mgh/t = {f3(Pu)} W [1]; P_in = P_out/η = {f3(Pu / eff)} W [1]; wasted = (P_in − P_out)t = {f3(Pu / eff * t - Pu * t)} J [1]' + (' [3]' if D == 3 else '; form of wasted energy (thermal/sound) [1] [4]'))
    if kind == 'car':
        F = r.choice([500, 600, 800, 1200, 1500]); v = r.choice([15, 20, 25, 30, 35])
        P = F * v
        s = f'A car travels at a constant {v} m s⁻¹ along a level road. The total resistive force is {F} N.'
        if D <= 2:
            return numq(r, D, s, 'output power of the engine', P, ' W', f'P = Fv = {F} × {v}', [F / v, F * v * v, F + v], fm=f3)
        Pmax = P * r.choice([1.5, 2.0, 2.5]); m = r.choice([1000, 1200, 1500])
        a = (Pmax / v - F) / m
        return Q(s + f' The engine can deliver a maximum power of {f3(Pmax)} W and the car has mass {m} kg. Calculate the power needed at {v} m s⁻¹ and the maximum possible acceleration at this speed.', f'{f3(P)} W; {f3(a)} m s⁻²',
                 f'P = Fv = {f3(P)} W [1]; max driving force = P_max/v = {f3(Pmax / v)} N [1]; resultant = {f3(Pmax / v - F)} N [1]; a = {f3(a)} m s⁻² [1] [4]')
    rate = r.choice([2.0, 5.0, 8.0, 12.0]); h = r.choice([5.0, 10.0, 15.0, 25.0])
    P = rate * GR * h
    s = f'A pump raises water through a vertical height of {nf(h)} m at a rate of {nf(rate)} kg s⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'useful power output', P, ' W', f'P = (m/t)gh = {nf(rate)} × 9.81 × {nf(h)}', [rate * h, rate * GR, P * 10], fm=f3)
    v = r.choice([3.0, 4.0, 5.0])
    P2 = P + 0.5 * rate * v * v
    return Q(s + f' The water leaves the pipe at {nf(v)} m s⁻¹. Calculate the minimum power output of the pump, taking into account the kinetic energy given to the water.', f'{f3(P2)} W',
             f'GPE per second = {f3(P)} W [1]; KE per second = ½ × {nf(rate)} × {nf(v)}² = {f3(0.5 * rate * v * v)} W [1]; total = {f3(P2)} W [1] [3]')


relation(t84, 'C2', (2, 3), 'P = Fv', 'useful power needed', {'resistive force': 1, 'speed': 1},
         ['A delivery van travels at constant speed on a level road.', 'A cyclist rides at constant speed into a headwind.', 'A boat moves at constant speed through calm water.'])


def _pow_c4(r, D):
    m = r.choice([60, 70, 80]); h = r.choice([3.0, 4.0, 4.5]); t = r.choice([3.0, 4.0, 5.0]); eff = r.choice([0.20, 0.25])
    intro = r.choice([f'A student of mass {m} kg runs up a flight of stairs of vertical height {nf(h)} m in {nf(t)} s in a school in {city(r)}.', f'An athlete of mass {m} kg climbs a staircase rising {nf(h)} m in {nf(t)} s during a fitness test.'])
    P = m * GR * h / t
    parts = [
        lambda r: ('Calculate the gain in gravitational potential energy.', f'{f3(m * GR * h)} J', 'mgh [1]'),
        lambda r: ('Calculate the useful power developed.', f'{f3(P)} W', 'P = W/t [2]'),
        lambda r: (f'The body converts chemical energy with an efficiency of {nf(eff * 100)}%. Calculate the rate of chemical energy use.', f'{f3(P / eff)} W', 'P_in = P_out/η [2]'),
        lambda r: ('Define efficiency.', 'useful energy (or power) output ÷ total energy (or power) input', 'definition [1]'),
        lambda r: ('Suggest why the measured power is an underestimate of the power actually developed.', 'Energy is also transferred to kinetic energy and thermal energy, and the arms/legs move; only mgh is counted.', 'other energy transfers not counted [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t84.add('C4', (2, 3, 4, 5), 'multi_step')(_pow_c4)

CHAPTERS[8] = [t81, t82, t83, t84]

# ===================================================================== 9 Deformation of solids
WIRES = [('steel', 2.0e11), ('copper', 1.2e11), ('brass', 1.0e11), ('aluminium', 7.0e10), ('nylon', 3.0e9), ('tungsten', 4.1e11)]

N91 = 'Stress, strain and the Young modulus'
t91 = topic(N91, N91.lower(), 'stress strain', 'young modulus')
FX(t91, 'C1', (1, 2), [
    ('Which is the definition of tensile stress?', 'Force per unit cross-sectional area', 'σ = F/A.', ['Extension per unit length', 'Force per unit extension', 'Force × cross-sectional area']),
    ('Which is the definition of tensile strain?', 'Extension divided by original length', 'ε = x/L, no unit.', ['Extension × original length', 'Force divided by extension', 'Original length divided by extension']),
    ('What is the unit of the Young modulus?', 'Pa', 'Stress (Pa) ÷ strain (no unit).', ['N m⁻¹', 'N', 'no unit']),
    ('A wire of length 2.0 m extends by 1.0 mm. What is the strain?', '5.0 × 10⁻⁴', 'ε = 1.0 × 10⁻³/2.0.', ['2.0 × 10³', '5.0 × 10⁻¹', '2.0 × 10⁻³']),
    ('A force of 200 N acts on a wire of cross-sectional area 1.0 × 10⁻⁶ m². What is the stress?', '2.0 × 10⁸ Pa', 'σ = 200/1.0 × 10⁻⁶.', ['2.0 × 10⁻⁴ Pa', '2.0 × 10² Pa', '5.0 × 10⁻⁹ Pa']),
    ('Two wires of the same material have the same length; wire X has twice the diameter of wire Y. For the same load, the extension of X is', 'a quarter of that of Y', 'Area ∝ d², so stress and extension are ¼.', ['half that of Y', 'twice that of Y', 'the same as that of Y']),
    ('State the equation defining the Young modulus.', 'E = stress/strain', 'E = σ/ε [1]'),
])
FX(t91, 'C2', (1, 2, 3, 4), [
    ('Explain why the Young modulus is a property of a material but the spring constant is a property of a particular sample.', 'E = stress/strain does not depend on the dimensions of the sample; k = F/x depends on the length and cross-sectional area as well as the material (k = EA/L).', 'E independent of dimensions [1]; k depends on L and A [1] [2]'),
    ('Describe how to measure the Young modulus of a metal wire in the laboratory.', 'Clamp a long thin wire; measure L with a metre rule and d at several places with a micrometer; add loads and measure extension with a vernier/marker against a reference wire; plot stress against strain; E = gradient of the linear region.', 'long wire and measurement of L [1]; micrometer for d [1]; extension measured as load added [1]; E from gradient of stress-strain [1] [4]'),
    ('Explain why a long, thin wire is used to measure the Young modulus.', 'A long wire gives a larger extension (x ∝ L) and a thin wire gives a large stress for a given load, so the extension is large enough to measure with small percentage uncertainty.', 'long → larger extension [1]; thin → larger stress/extension [1] [2]'),
    ('Explain why the diameter of the wire should be measured at several points along its length.', 'The wire may not be uniform; averaging several readings (at different orientations) gives a more reliable value for the area, and d is squared in A so its uncertainty matters.', 'non-uniform wire [1]; average reduces uncertainty, which is doubled in A [1] [2]'),
])


@t91.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t91_young(r, D):
    mat, E_ = r.choice(WIRES)
    L = r.choice([1.50, 2.00, 2.50, 3.00]); d = r.choice([0.30, 0.40, 0.50, 0.60, 0.80]) * 1e-3; F = r.choice([40, 50, 80, 100, 120, 150])
    A = math.pi * d * d / 4; st = F / A; ep = st / E_; x = ep * L
    s = f'A {mat} wire of length {nf(L)} m and diameter {nf(d * 1000)} mm supports a load of {F} N. The Young modulus of {mat} is {sci(E_, 2)} Pa.'
    if D <= 1:
        return numq(r, D, f'A {mat} wire has cross-sectional area {sci(A, 3)} m² and supports a load of {F} N.', 'tensile stress', st, ' Pa', f'σ = F/A = {F}/{sci(A, 3)}', [F * A * 1e12, F / (d * d), st / 4], fm=lambda x: sci(x, 3))
    if D == 2:
        return Q(s + ' Calculate the stress in the wire.', f'{sci(st, 3)} Pa', f'A = πd²/4 = {sci(A, 3)} m² [1]; σ = F/A = {sci(st, 3)} Pa [1] [2]')
    if D == 3:
        return Q(s + ' Calculate the extension of the wire.', f'{f3(x * 1000)} mm', f'σ = F/A = {sci(st, 3)} Pa [1]; ε = σ/E = {sci(ep, 3)} [1]; x = εL = {sci(x, 3)} m = {f3(x * 1000)} mm [1] [3]')
    return Q(f'A wire of length {nf(L)} m and diameter {nf(d * 1000)} mm extends by {f3(x * 1000)} mm when a load of {F} N is added. (a) Calculate the stress and the strain. (b) Calculate the Young modulus and suggest the material, using: steel 2.0 × 10¹¹ Pa, copper 1.2 × 10¹¹ Pa, brass 1.0 × 10¹¹ Pa, aluminium 7.0 × 10¹⁰ Pa, nylon 3.0 × 10⁹ Pa, tungsten 4.1 × 10¹¹ Pa.',
             f'(a) σ = {sci(st, 3)} Pa, ε = {sci(ep, 3)} (b) E = {sci(E_, 3)} Pa: {mat}',
             f'(a) A = {sci(A, 3)} m² [1]; σ = {sci(st, 3)} Pa [1]; ε = x/L = {sci(ep, 3)} [1] (b) E = σ/ε = {sci(E_, 3)} Pa [1]; {mat} [1] [5]', 'multi_step')


@t91.add('C3', (2, 3, 4), 'numerical')
def t91_compare(r, D):
    mat, E_ = r.choice(WIRES[:4])
    k = r.choice([2, 3]); j = r.choice([2, 0.5])
    fac = j / (k * k)
    return Q(f'Wire P and wire Q are made of {mat}. Q has {k} times the diameter of P and {"twice" if j == 2 else "half"} the length. The same load is hung on each. Determine the ratio extension of Q / extension of P.',
             f'{nf(fac, 3)}', f'x = FL/(AE) [1]; A ∝ d² so A_Q = {k * k}A_P [1]; ratio = {nf(j)}/{k * k} = {nf(fac, 3)} [1] [3]')


relation(t91, 'C2', (2, 3), 'x = FL/(EA)', 'extension', {'load': 1, 'original length': 1, 'cross-sectional area': -1},
         ['A steel cable supports a load within its limit of proportionality.', 'A copper wire is stretched in a Young modulus experiment, within the elastic limit.', 'A guitar string is tightened within its limit of proportionality.'])


def _ym_c4(r, D):
    mat, E_ = r.choice(WIRES[:3])
    L = r.choice([2.00, 2.50]); d = r.choice([0.40, 0.50]) * 1e-3; F = r.choice([60, 80, 100])
    A = math.pi * d * d / 4; x = F * L / (A * E_)
    intro = r.choice([f'In {lab(r)}, a student hangs loads on a {mat} wire of length {nf(L)} m and diameter {nf(d * 1000)} mm to find its Young modulus.', f'A {mat} wire {nf(L)} m long with diameter {nf(d * 1000)} mm is fixed to a ceiling beam and loaded with masses.'])
    parts = [
        lambda r: ('Define stress and strain.', 'stress = force/cross-sectional area; strain = extension/original length', 'stress [1]; strain [1] [2]'),
        lambda r: ('Calculate the cross-sectional area of the wire.', f'{sci(A, 3)} m²', 'πd²/4 [1]'),
        lambda r: (f'With a load of {F} N the extension is {f3(x * 1000)} mm. Calculate the Young modulus.', f'{sci(E_, 3)} Pa', 'σ/ε [3]'),
        lambda r: ('Suggest why a reference wire with a vernier scale is used to measure the extension.', 'It compensates for sagging of the support and temperature changes; the vernier measures small extensions precisely.', 'compensates sag/temperature [1]; precise small extension [1] [2]'),
        lambda r: ('State one safety precaution for this experiment.', 'Wear safety goggles in case the wire snaps / place a box of sand under the masses.', 'precaution [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t91.add('C4', (2, 3, 4, 5), 'multi_step')(_ym_c4)

N92 = 'Elastic and plastic deformation and force-extension graphs'
t92 = topic(N92, N92.lower(), 'elastic and plastic deformation', 'force-extension graphs')
FX(t92, 'C1', (1, 2), [
    ('What is meant by elastic deformation?', 'Deformation from which the material returns to its original shape when the load is removed', 'Elastic: fully recoverable.', ['Deformation that is permanent', 'Deformation in which the material breaks', 'Deformation that only occurs in rubber']),
    ('What is meant by plastic deformation?', 'Permanent deformation that remains when the load is removed', 'Plastic: beyond the elastic limit.', ['Deformation that is fully recovered', 'Deformation obeying Hooke\'s law', 'Deformation only under compression']),
    ("Hooke's law states that the extension of a spring is proportional to the load", 'up to the limit of proportionality', 'Beyond this point the graph curves.', ['for all loads', 'only beyond the elastic limit', 'only for plastic materials']),
    ('A spring extends 4.0 cm under a load of 2.0 N. What is the spring constant?', '50 N m⁻¹', 'k = F/x = 2.0/0.040.', ['0.5 N m⁻¹', '8.0 N m⁻¹', '2.0 N m⁻¹']),
    ('Two identical springs of spring constant k are joined in series. What is the spring constant of the combination?', 'k/2', 'Each spring carries the full load; extension doubles.', ['2k', 'k', 'k/4']),
    ('Two identical springs of spring constant k are joined in parallel. What is the spring constant of the combination?', '2k', 'Each spring carries half the load; extension halves.', ['k/2', 'k', '4k']),
    ('State what is meant by the elastic limit.', 'The maximum load (or stress) beyond which the material will not return to its original length when the load is removed.', 'beyond it deformation is permanent [1]'),
])
FX(t92, 'C2', (1, 2, 3, 4), [
    ('Describe the force-extension graph for a ductile metal such as copper, loaded until it breaks.', 'Straight line through the origin (Hooke\'s law) to the limit of proportionality; then curves past the elastic limit; large plastic extension with little extra force (necking) until fracture.', 'linear region [1]; elastic limit then plastic region with large extension [1]; breaks after necking [1] [3]'),
    ('Explain the difference between a brittle and a ductile material, giving an example of each.', 'A brittle material (e.g. glass) breaks with little or no plastic deformation; a ductile material (e.g. copper) undergoes large plastic deformation before breaking and can be drawn into wires.', 'brittle: no plastic deformation, example [1]; ductile: large plastic deformation, example [1] [2]'),
    ('Explain how you could show that a spring has been loaded beyond its elastic limit.', 'Remove the load and measure the length; if it does not return to its original length there is a permanent extension, so the elastic limit was exceeded.', 'unload and measure length [1]; permanent extension shows limit exceeded [1] [2]'),
    ('Describe the loading and unloading curves for a rubber band.', 'Non-linear loading curve; the unloading curve lies below it (hysteresis) but returns to near zero extension; the area between the curves is energy converted to thermal energy.', 'non-linear [1]; unloading below loading [1]; area = energy dissipated [1] [3]'),
])


@t92.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t92_springs(r, D):
    k = r.choice([20, 25, 40, 50, 80, 100, 200]); F = r.choice([2.0, 4.0, 5.0, 6.0, 8.0, 10.0])
    x = F / k
    if D <= 2:
        return numq(r, D, f'A spring of spring constant {k} N m⁻¹ obeys Hooke\'s law.', f'extension produced by a load of {nf(F)} N, in cm', x * 100, ' cm', f'x = F/k = {nf(F)}/{k} m', [F * k / 100, k / F, x * 1000], fm=f3)
    arr = r.choice(['series', 'parallel'])
    keff = k / 2 if arr == 'series' else 2 * k
    if D == 3:
        return Q(f'Two identical springs, each of spring constant {k} N m⁻¹, are connected in {arr}. A load of {nf(F)} N hangs from the combination. Calculate the total extension.', f'{f3(F / keff * 100)} cm',
                 f'effective k = {nf(keff)} N m⁻¹ [1]; x = F/k = {nf(F)}/{nf(keff)} [1]; = {f3(F / keff * 100)} cm [1] [3]')
    k2 = r.choice([30, 60, 120])
    ks = 1 / (1 / k + 1 / k2)
    return Q(f'A spring of spring constant {k} N m⁻¹ is connected in series with a spring of spring constant {k2} N m⁻¹. A load of {nf(F)} N hangs from the lower spring. (a) Calculate the extension of each spring. (b) Calculate the spring constant of the combination. (c) State the assumption made.',
             f'(a) {f3(F / k * 100)} cm and {f3(F / k2 * 100)} cm (b) {f3(ks)} N m⁻¹ (c) both springs obey Hooke\'s law and have negligible mass.',
             f'(a) same tension in each [1]; extensions F/k each [1] (b) k = F/(x₁ + x₂) = {f3(ks)} N m⁻¹ [1]; (c) Hooke\'s law obeyed / massless springs [1]' + (' [4]' if D == 4 else '; check with 1/k = 1/k₁ + 1/k₂ [1] [5]'), 'multi_step')


@t92.add('C3', (2, 3, 4), 'case')
def t92_data(r, D):
    k = r.choice([20, 25, 40, 50]); lim = r.choice([4, 5])
    loads = [1, 2, 3, 4, 5, 6]
    xs = []
    for F in loads:
        x = F / k * 100
        if F > lim:
            x *= 1 + 0.25 * (F - lim)
        xs.append(round(x, 1))
    rows = ', '.join(f'{F} N: {x} cm' for F, x in zip(loads, xs))
    return Q(f'A student loads a spring and records the extension: {rows}. (a) Determine the spring constant from the linear region. (b) Estimate the load at the limit of proportionality. (c) Explain how the student could check whether the elastic limit was exceeded.',
             f'(a) {k} N m⁻¹ (b) about {lim} N (c) remove the loads and check whether the spring returns to its original length.',
             f'(a) k = F/x from linear region = {k} N m⁻¹ [1] (b) {lim} N where proportionality ends [1] (c) unload and measure length [1] [3]')


def _def_c4(r, D):
    intro = r.choice([f'A student in {lab(r)} investigates samples of copper wire, glass fibre and rubber by loading them and measuring extension.', 'Engineers compare the force-extension behaviour of a steel cable, a rubber mounting and a ceramic rod.'])
    parts = [
        lambda r: ('Distinguish between elastic and plastic deformation.', 'Elastic: returns to original shape when load removed; plastic: permanent change in shape.', 'elastic [1]; plastic [1] [2]'),
        lambda r: ('Sketch and describe the force-extension graph for the ductile metal.', 'Linear to limit of proportionality, then curve with large plastic extension before breaking.', 'linear region [1]; plastic region and fracture [1] [2]'),
        lambda r: ('Describe the behaviour of the brittle material.', 'Linear up to fracture with no plastic region.', 'linear then sudden break [1]'),
        lambda r: ('Explain what the area between the loading and unloading curves for rubber represents.', 'Energy transferred to thermal energy (hysteresis) in each cycle.', 'energy lost per loading cycle [1]; transferred to thermal energy (hysteresis) [1] [2]'),
        lambda r: ("State Hooke's law.", 'Extension is proportional to load provided the limit of proportionality is not exceeded.', 'proportionality and condition [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t92.add('C4', (2, 3, 4, 5), 'multi_step')(_def_c4)

N93 = 'Elastic potential energy as area under a force-extension graph'
t93 = topic(N93, N93.lower(), 'elastic potential energy', 'area under a force-extension graph')
FX(t93, 'C1', (1, 2), [
    ('The elastic potential energy stored in a stretched wire is represented by', 'the area under the force-extension graph', 'Work done stretching = ∫F dx.', ['the gradient of the force-extension graph', 'the force × original length', 'the area under the stress-strain graph multiplied by the mass']),
    ('A spring of spring constant 200 N m⁻¹ is stretched by 0.10 m. What elastic potential energy is stored?', '1.0 J', 'E = ½kx² = 0.5 × 200 × 0.01.', ['2.0 J', '20 J', '10 J']),
    ('A wire stretches 2.0 mm under a load of 50 N within its limit of proportionality. What energy is stored?', '0.050 J', 'E = ½Fx = 0.5 × 50 × 2.0 × 10⁻³.', ['0.10 J', '100 J', '50 J']),
    ('The extension of a spring is doubled within its limit of proportionality. The elastic potential energy', 'is multiplied by 4', 'E = ½kx² ∝ x².', ['doubles', 'halves', 'is unchanged']),
    ('Which expression gives the elastic potential energy of a material obeying Hooke\'s law?', '½Fx', 'Area of the triangle under the F-x line.', ['Fx', '2Fx', 'F/x']),
    ('State the equation for elastic potential energy in terms of the spring constant.', 'E = ½kx²', 'E = ½kx² [1]'),
])
FX(t93, 'C2', (1, 2, 3, 4), [
    ('Derive E = ½Fx for a material that obeys Hooke\'s law.', 'The force rises linearly from 0 to F as the extension goes from 0 to x; the work done is the area of the triangle under the graph, ½Fx.', 'work = area under graph [1]; triangle area ½Fx [1] [2]'),
    ('Explain why the energy released when a wire stretched beyond its elastic limit is unloaded is less than the work done in stretching it.', 'Some of the work done causes plastic deformation and is transferred to thermal energy; only the elastic part is recovered.', 'plastic deformation [1]; energy dissipated as thermal, not recovered [1] [2]'),
    ('Explain why E = ½kx² cannot be used beyond the limit of proportionality.', 'The force is no longer proportional to extension, so the area under the graph is not a triangle; the energy must be found from the actual area.', 'F not ∝ x [1]; find area under curve [1] [2]'),
])


@t93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t93_epe(r, D):
    k = r.choice([50, 80, 120, 200, 400, 800]); x = r.choice([0.020, 0.040, 0.050, 0.080, 0.10, 0.15])
    E_ = 0.5 * k * x * x
    sc = r.choice([f'A spring of spring constant {k} N m⁻¹ is compressed by {nf(x * 100)} cm', f'A catapult band behaves like a spring of constant {k} N m⁻¹ and is stretched by {nf(x * 100)} cm', f'A trampoline spring with k = {k} N m⁻¹ is extended by {nf(x * 100)} cm'])
    if D <= 2:
        return numq(r, D, sc + ', within the limit of proportionality.', 'elastic potential energy stored', E_, ' J', f'E = ½kx² = ½ × {k} × {nf(x)}²', [k * x * x, 0.5 * k * x, k * x], fm=f3)
    m = r.choice([0.010, 0.020, 0.050, 0.10])
    v = math.sqrt(2 * E_ / m)
    if D == 3:
        return Q(sc + f' and used to launch a ball of mass {nf(m)} kg horizontally. Assuming all the elastic energy becomes kinetic energy, calculate the launch speed.', f'{f3(v)} m s⁻¹',
                 f'E = ½kx² = {f3(E_)} J [1]; ½mv² = E [1]; v = {f3(v)} m s⁻¹ [1] [3]')
    eff = r.choice([0.60, 0.70, 0.80])
    h = E_ * eff / (m * GR)
    return Q(sc + f' and used to launch a ball of mass {nf(m)} kg vertically upwards. {nf(eff * 100)}% of the stored energy becomes gravitational potential energy at the top. (a) Calculate the energy stored. (b) Calculate the maximum height. (c) Suggest where the rest of the energy goes.',
             f'(a) {f3(E_)} J (b) {f3(h)} m (c) thermal energy in the spring and air (air resistance), sound, KE of the spring.',
             f'(a) ½kx² = {f3(E_)} J [1] (b) mgh = {nf(eff)} × {f3(E_)} [1]; h = {f3(h)} m [1] (c) sensible losses [1]' + (' [4]' if D == 4 else '; justification of assumption that k is constant [1] [5]'), 'multi_step')


@t93.add('C3', (2, 3, 4), 'numerical')
def t93_area(r, D):
    F1 = r.choice([20, 30, 40]); x1 = r.choice([2.0, 3.0, 4.0]); F2 = F1 + r.choice([5, 10]); x2 = x1 + r.choice([2.0, 3.0, 4.0])
    E1 = 0.5 * F1 * x1 * 1e-3; E2 = E1 + 0.5 * (F1 + F2) * (x2 - x1) * 1e-3
    return Q(f'The force-extension graph for a metal wire is a straight line from the origin to ({x1} mm, {F1} N) and then a straight line to ({x2} mm, {F2} N). Calculate the work done in stretching the wire to an extension of {x2} mm.', f'{f3(E2)} J',
             f'triangle ½ × {F1} × {x1} × 10⁻³ = {f3(E1)} J [1]; trapezium ½({F1} + {F2}) × {nf(x2 - x1)} × 10⁻³ [1]; total {f3(E2)} J [1] [3]')


def _epe_c4(r, D):
    k = r.choice([500, 800, 1200]); x = r.choice([0.05, 0.08, 0.10]); m = r.choice([0.50, 1.0, 2.0])
    E_ = 0.5 * k * x * x
    intro = r.choice([f'A toy launcher contains a spring of spring constant {k} N m⁻¹. It is compressed by {nf(x * 100)} cm and used to fire a {nf(m)} kg block along a smooth horizontal track.', f'A buffer spring at the end of a model railway in {city(r)} has k = {k} N m⁻¹. A {nf(m)} kg truck compresses it by {nf(x * 100)} cm before stopping.'])
    parts = [
        lambda r: ('Calculate the elastic potential energy stored at maximum compression.', f'{f3(E_)} J', '½kx² [2]'),
        lambda r: ('Calculate the speed of the block when it leaves the spring (or arrives at it).', f'{f3(math.sqrt(2 * E_ / m))} m s⁻¹', 'energy conservation [2]'),
        lambda r: ('Calculate the maximum force exerted by the spring.', f'{f3(k * x)} N', 'F = kx [1]'),
        lambda r: ('Explain why the elastic potential energy is the area under the force-compression graph.', 'Work done = force × displacement; the force varies, so the work is the area under the graph.', 'work = ∫F dx [1]; area [1] [2]'),
        lambda r: ('State one assumption made in your calculation.', "The spring obeys Hooke's law / no energy lost to friction or heat.", 'assumption [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t93.add('C4', (2, 3, 4, 5), 'multi_step')(_epe_c4)

CHAPTERS[9] = [t91, t92, t93]


# ===================================================================== 10 Waves
N101 = 'Progressive waves: displacement, amplitude, phase difference, period, frequency and wavelength'
t101 = topic(N101, N101.lower(), 'progressive waves', 'phase difference')
FX(t101, 'C1', (1, 2), [
    ('What is the phase difference between two points on a progressive wave that are half a wavelength apart?', '180° (π rad)', 'Phase difference = 360° × Δx/λ = 180°.', ['90° (π/2 rad)', '360° (2π rad)', '45° (π/4 rad)']),
    ('A wave has a period of 4.0 ms. What is its frequency?', '250 Hz', 'f = 1/T = 1/0.0040.', ['4.0 Hz', '25 Hz', '2500 Hz']),
    ('Which is the definition of wavelength?', 'The minimum distance between two points on a wave that are in phase', 'For example, crest to adjacent crest.', ['The distance from a crest to the next trough', 'The maximum displacement from equilibrium', 'The distance travelled by the wave in one second']),
    ('In a longitudinal wave, the particles of the medium oscillate', 'parallel to the direction of energy transfer', 'Compressions and rarefactions form along the direction of travel.', ['perpendicular to the direction of energy transfer', 'in circles', 'only in a vacuum']),
    ('A sound wave of frequency 680 Hz travels at 340 m s⁻¹. What is its wavelength?', '0.50 m', 'λ = v/f = 340/680.', ['2.0 m', '2.3 × 10⁵ m', '0.25 m']),
    ('What is meant by the amplitude of a wave?', 'The maximum displacement of a particle from its equilibrium position', 'Amplitude is the maximum displacement.', ['The distance between a crest and a trough', 'The number of oscillations per second', 'The speed of the wave']),
    ('Two points on a wave 0.15 m apart have a phase difference of 90°. What is the wavelength?', '0.60 m', 'Δx = λ/4.', ['0.30 m', '0.15 m', '1.2 m']),
    ('State what is meant by the displacement of a particle in a wave.', 'The distance (in a given direction) of the particle from its equilibrium position.', 'distance from equilibrium position [1]'),
])
FX(t101, 'C2', (1, 2, 3, 4), [
    ('Derive v = fλ from the definitions of frequency and wavelength.', 'In one period T the wave travels one wavelength λ, so v = λ/T; since f = 1/T, v = fλ.', 'distance λ in time T [1]; T = 1/f gives v = fλ [1] [2]'),
    ('Explain the difference between transverse and longitudinal waves, giving an example of each.', 'Transverse: oscillations perpendicular to energy transfer (e.g. light, waves on a string); longitudinal: oscillations parallel to energy transfer (e.g. sound).', 'transverse definition with example [1]; longitudinal definition with example [1] [2]'),
    ('Explain how a cathode-ray oscilloscope (CRO) trace can be used to find the frequency of a sound wave.', 'Measure the horizontal length of one (or several) complete cycles in divisions; multiply by the time-base setting to get the period T; f = 1/T.', 'measure divisions for a cycle [1]; × time-base gives T [1]; f = 1/T [1] [3]'),
    ('Explain why points on a progressive wave one wavelength apart oscillate in phase.', 'The wave pattern repeats every wavelength, so the two points have the same displacement and velocity at all times.', 'pattern repeats each λ [1]; same displacement and motion at every instant [1] [2]'),
])


@t101.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t101_cro(r, D):
    tb = r.choice([0.5, 1.0, 2.0, 5.0]); div = r.choice([2.0, 2.5, 4.0, 5.0]); yg = r.choice([0.5, 1.0, 2.0, 5.0]); h = r.choice([1.5, 2.0, 2.5, 3.0])
    T = tb * div * 1e-3; f = 1 / T
    s = f'A microphone connected to a cathode-ray oscilloscope detects a sound wave. One complete wave occupies {nf(div)} divisions horizontally; the time-base is set at {nf(tb)} ms div⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'frequency of the sound', f, ' Hz', f'T = {nf(div)} × {nf(tb)} ms = {nf(T * 1000, 3)} ms; f = 1/T', [1 / (tb * 1e-3), div / tb * 1000, f / 2], fm=f3)
    v = r.choice([330, 340])
    if D == 3:
        return Q(s + f' The speed of sound is {v} m s⁻¹. Calculate the frequency and the wavelength.', f'f = {f3(f)} Hz; λ = {f3(v / f)} m', f'T = {nf(T * 1000, 3)} ms [1]; f = 1/T = {f3(f)} Hz [1]; λ = v/f = {f3(v / f)} m [1] [3]')
    return Q(s + f' The trace has a peak-to-peak height of {nf(2 * h)} divisions and the y-gain is {nf(yg)} mV div⁻¹. (a) Calculate the frequency. (b) Calculate the amplitude of the signal. (c) Describe the change to the trace if the frequency is doubled with the same amplitude.',
             f'(a) {f3(f)} Hz (b) {f3(h * yg)} mV (c) twice as many cycles on the screen (each cycle occupies {nf(div / 2)} divisions); height unchanged.',
             f'(a) T = {nf(T * 1000, 3)} ms [1]; f = {f3(f)} Hz [1] (b) amplitude = {nf(h)} div × {nf(yg)} mV div⁻¹ = {f3(h * yg)} mV [1] (c) cycles halve in width [1]' + (' [4]' if D == 4 else '; height unchanged [1] [5]'), 'multi_step')


@t101.add('C3', (1, 2, 3, 4), 'numerical')
def t101_phase(r, D):
    lam = r.choice([0.40, 0.60, 0.80, 1.2, 2.0, 2.4]); frac = r.choice([0.125, 0.25, 0.375, 0.5, 0.75])
    dx = lam * frac; ph = 360 * frac
    if D <= 2:
        return numq(r, D, f'A progressive wave has wavelength {nf(lam)} m. Two points P and Q on the wave are {nf(dx, 3)} m apart along the direction of travel.', 'phase difference between P and Q in degrees', ph, '°', f'φ = 360° × {nf(dx, 3)}/{nf(lam)}', [ph / 2, 360 * dx, ph * 2 if ph < 180 else ph / 3], fm=f3)
    f = r.choice([5, 10, 20, 25, 50])
    dt = r.choice([0.25, 0.5]) / f
    return Q(f'A wave of frequency {f} Hz and wavelength {nf(lam)} m travels along a rope. (a) Calculate the wave speed. (b) Calculate the phase difference, in radians, between two points {nf(dx, 3)} m apart. (c) Calculate the phase difference at one point between times separated by {nf(dt * 1000, 3)} ms.',
             f'(a) {f3(f * lam)} m s⁻¹ (b) {nf(2 * frac, 3)}π rad (c) {nf(2 * f * dt, 3)}π rad',
             f'(a) v = fλ = {f3(f * lam)} m s⁻¹ [1] (b) 2π × Δx/λ = {nf(2 * frac, 3)}π rad [1] (c) 2π × Δt/T = 2π × {nf(dt * 1000, 3)} ms × {f} Hz [1]; = {nf(2 * f * dt, 3)}π rad [1] [4]', 'multi_step')


def _wave_c4(r, D):
    f = r.choice([2.0, 2.5, 4.0, 5.0]); lam = r.choice([0.020, 0.025, 0.030, 0.040]); A = r.choice([3.0, 4.0, 5.0])
    intro = r.choice([f'Water waves in a ripple tank in {lab(r)} have frequency {nf(f)} Hz, wavelength {nf(lam * 100)} cm and amplitude {nf(A)} mm.', f'A vibration generator sends transverse waves of frequency {nf(f)} Hz, wavelength {nf(lam * 100)} cm and amplitude {nf(A)} mm along a long spring.'])
    parts = [
        lambda r: ('Calculate the speed of the waves.', f'{f3(f * lam)} m s⁻¹', 'v = fλ [2]'),
        lambda r: ('Calculate the period.', f'{f3(1 / f)} s', 'T = 1/f [1]'),
        lambda r: (f'Calculate the phase difference between two points {nf(lam * 25)} cm apart.', '90° (π/2 rad)', 'separation = λ/4 [1]; phase difference = 360° × ¼ = 90° [1] [2]'),
        lambda r: ('Sketch a displacement-distance graph for two wavelengths, labelling the amplitude and wavelength.', f'sinusoid with peak {nf(A)} mm, repeating every {nf(lam * 100)} cm', 'shape [1]; labels [1] [2]'),
        lambda r: ('Calculate the total distance moved by a particle on the wave in 1.0 s.', f'{f3(4 * A * f)} mm', '4A per cycle × f [2]'),
        lambda r: ('Explain how the wave transfers energy without transferring matter.', 'Each particle oscillates about its equilibrium position, passing energy to neighbouring particles.', 'oscillation about fixed position [1]; energy passed on [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t101.add('C4', (2, 3, 4, 5), 'multi_step')(_wave_c4)

N102 = 'Intensity of waves and its dependence on amplitude'
t102 = topic(N102, N102.lower(), 'intensity of waves', 'amplitude')
FX(t102, 'C1', (1, 2), [
    ('Which is the definition of intensity of a wave?', 'Power per unit area perpendicular to the direction of travel', 'I = P/A, unit W m⁻².', ['Energy per unit volume', 'Power per unit wavelength', 'Amplitude per unit area']),
    ('The amplitude of a wave is doubled. The intensity', 'is multiplied by 4', 'I ∝ A².', ['doubles', 'halves', 'is unchanged']),
    ('What is the unit of intensity?', 'W m⁻²', 'Power per unit area.', ['W m⁻¹', 'J m⁻²', 'W m²']),
    ('A point source emits waves equally in all directions. The distance from the source is doubled. The intensity', 'falls to a quarter', 'I = P/(4πr²) ∝ 1/r².', ['halves', 'falls to an eighth', 'is unchanged']),
    ('A solar panel of area 2.0 m² receives a power of 1.6 kW. What is the intensity of the sunlight?', '800 W m⁻²', 'I = 1600/2.0.', ['3200 W m⁻²', '0.80 W m⁻²', '1.25 × 10⁻³ W m⁻²']),
    ('State the relationship between intensity and amplitude.', 'Intensity is proportional to the square of the amplitude.', 'I ∝ A² [1]'),
])
FX(t102, 'C2', (1, 2, 3, 4), [
    ('Explain why the intensity of sound from a small source decreases with distance.', 'The power spreads over the surface of an ever larger sphere (area 4πr²), so the power per unit area falls as 1/r² (ignoring absorption).', 'power spread over larger area [1]; I = P/(4πr²) ∝ 1/r² [1] [2]'),
    ('Explain why the intensity of a laser beam hardly decreases over a short distance.', 'The beam does not spread out much, so the area over which the power is spread stays almost constant.', 'little spreading [1]; area constant so I constant [1] [2]'),
    ('Explain why the intensity of a wave is proportional to the square of its amplitude.', 'Energy of an oscillating particle ∝ (amplitude)²; intensity is the rate of energy transfer per unit area, so I ∝ A².', 'energy ∝ A² [1]; intensity ∝ energy transfer rate [1] [2]'),
])


@t102.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t102_point(r, D):
    P = r.choice([0.50, 2.0, 5.0, 20, 60, 100]); rr = r.choice([1.5, 2.0, 3.0, 5.0, 8.0, 10.0])
    I = P / (4 * math.pi * rr * rr)
    src = r.choice(['A small loudspeaker emits sound', 'A small lamp radiates light', 'A point source of ultrasound emits waves', 'A siren on a pole emits sound'])
    s = f'{src} uniformly in all directions with a power of {nf(P)} W.'
    if D <= 2:
        return numq(r, D, s, f'intensity at a distance of {nf(rr)} m', I, ' W m⁻²', f'I = P/(4πr²) = {nf(P)}/(4π × {nf(rr)}²)', [P / (math.pi * rr * rr), P / (4 * math.pi * rr), P / rr ** 2], fm=f3)
    k = r.choice([2, 3, 4])
    if D == 3:
        return Q(s + f' Calculate the intensity at {nf(rr)} m and at {nf(k * rr)} m, and state the ratio of the intensities.', f'{f3(I)} W m⁻²; {f3(I / k ** 2)} W m⁻²; ratio {k * k} : 1',
                 f'I = P/(4πr²) = {f3(I)} W m⁻² [1]; at {nf(k * rr)} m: {f3(I / k ** 2)} W m⁻² [1]; ratio {k * k} (inverse square) [1] [3]')
    A1 = r.choice([2.0, 3.0, 4.0])
    return Q(s + f' At {nf(rr)} m the amplitude of the wave is {nf(A1)} µm. (a) Calculate the intensity at {nf(rr)} m. (b) Calculate the distance at which the intensity is a quarter of this. (c) Calculate the amplitude at that distance.',
             f'(a) {f3(I)} W m⁻² (b) {nf(2 * rr)} m (c) {nf(A1 / 2)} µm',
             f'(a) I = P/(4πr²) = {f3(I)} W m⁻² [1] (b) I ∝ 1/r² so r doubles: {nf(2 * rr)} m [1] (c) I ∝ A² so A halves [1]; = {nf(A1 / 2)} µm [1]' + (' [4]' if D == 4 else '; assumption: no absorption, uniform emission [1] [5]'), 'multi_step')


@t102.add('C3', (2, 3, 4), 'numerical')
def t102_amp(r, D):
    I1 = r.choice([0.20, 0.50, 0.80, 1.2, 3.0]); A1 = r.choice([2.0, 3.0, 4.0, 5.0]); A2 = A1 * r.choice([0.5, 1.5, 2.0, 3.0])
    I2 = I1 * (A2 / A1) ** 2
    return Q(f'A wave of amplitude {nf(A1)} mm has intensity {nf(I1)} W m⁻². The amplitude changes to {nf(A2)} mm with the frequency unchanged. Calculate the new intensity.', f'{f3(I2)} W m⁻²',
             f'I ∝ A² [1]; I₂ = {nf(I1)} × ({nf(A2)}/{nf(A1)})² [1]; = {f3(I2)} W m⁻² [1] [3]')


relation(t102, 'C2', (2, 3), 'I ∝ A²', 'intensity', {'amplitude': 2},
         ['A loudspeaker produces a sound wave of constant frequency.', 'A water wave travels across a deep tank.', 'A light source produces waves detected by a sensor at a fixed distance.'])


def _int_c4(r, D):
    P = r.choice([1.0, 2.0, 4.0]); rr = r.choice([2.0, 3.0, 4.0]); Ar = r.choice([2.0e-4, 5.0e-4])
    I = P / (4 * math.pi * rr * rr)
    intro = r.choice([f'A small speaker at an outdoor concert in {city(r)} radiates {nf(P)} W of sound uniformly in all directions.', f'A point source of sound of power {nf(P)} W is placed in an open field.'])
    parts = [
        lambda r: ('Define intensity.', 'Power per unit area (normal to the direction of travel).', 'definition [1]'),
        lambda r: (f'Calculate the intensity at {nf(rr)} m.', f'{f3(I)} W m⁻²', 'I = P/(4πr²) [2]'),
        lambda r: (f'An eardrum of area {sci(Ar, 1)} m² is at {nf(rr)} m. Calculate the power received.', f'{sci(I * Ar, 3)} W', 'P = IA [2]'),
        lambda r: ('Explain why the intensity falls with distance.', 'Power spreads over a larger spherical area 4πr².', 'larger area [1]; inverse square [1] [2]'),
        lambda r: (f'Calculate the ratio of the amplitudes at {nf(rr)} m and {nf(2 * rr)} m.', '2 : 1', 'I ∝ 1/r² so intensity ratio 4 : 1 [1]; A ∝ √I gives 2 : 1 [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t102.add('C4', (2, 3, 4, 5), 'multi_step')(_int_c4)

N103 = 'The Doppler effect for sound waves'
t103 = topic(N103, N103.lower(), 'doppler effect', 'sound waves')
FX(t103, 'C1', (1, 2), [
    ('A source of sound moves towards a stationary observer. The observed frequency is', 'higher than the source frequency', 'Wavefronts are bunched ahead of the moving source, so λ decreases and f increases.', ['lower than the source frequency', 'equal to the source frequency', 'zero']),
    ('Which equation gives the observed frequency f₀ for a source of frequency f_s moving at speed v_s away from a stationary observer (wave speed v)?', 'f₀ = f_s v/(v + v_s)', 'Moving away: wavelength stretched.', ['f₀ = f_s v/(v − v_s)', 'f₀ = f_s (v + v_s)/v', 'f₀ = f_s v_s/v']),
    ('As an ambulance passes a pedestrian, the pitch of its siren appears to', 'fall', 'Approaching: higher f; receding: lower f.', ['rise', 'stay constant', 'rise then stay constant']),
    ('The Doppler effect for a moving source changes', 'the wavelength of the waves received', 'The source moves between emitting wavefronts, compressing or stretching λ.', ['the speed of the waves in air', 'the amplitude only', 'the frequency emitted by the source']),
    ('A source of frequency 500 Hz moves towards a stationary observer at 34 m s⁻¹. The speed of sound is 340 m s⁻¹. What is the observed frequency?', '556 Hz', 'f₀ = 500 × 340/(340 − 34) = 556 Hz.', ['455 Hz', '550 Hz', '450 Hz']),
    ('State what is meant by the Doppler effect.', 'The change in observed frequency of a wave when the source moves relative to the observer.', 'change in observed frequency due to relative motion [1]'),
])
FX(t103, 'C2', (1, 2, 3, 4), [
    ('Explain, in terms of wavefronts, why the frequency heard from an approaching source is higher than the emitted frequency.', 'The source moves towards the observer between emitting successive wavefronts, so they are closer together (shorter λ); the wave speed is unchanged so more wavefronts arrive per second.', 'source moves between emissions [1]; λ shorter [1]; same v so higher f [1] [3]'),
    ('Explain why the speed of the sound waves is not changed by the motion of the source.', 'The speed of sound depends only on the medium (air) and its conditions, not on the motion of the source.', 'speed set by medium [1]'),
    ('Describe how the frequency heard by a stationary observer changes as a train sounding its horn passes at constant speed.', 'Higher than emitted as it approaches (constant), drops quickly as it passes, then constant and lower than emitted as it recedes.', 'higher on approach [1]; lower when receding with sudden drop [1] [2]'),
])


@t103.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t103_dopp(r, D):
    fs = r.choice([400, 500, 600, 750, 800, 1000, 1200]); vs = r.choice([10, 15, 20, 25, 30, 40]); v = r.choice([330, 340])
    src = r.choice(['an ambulance siren', 'a train horn', 'a police car siren', 'a racing car engine note', 'a whistle on a moving cart'])
    towards = r.choice([True, False])
    fo = fs * v / (v - vs) if towards else fs * v / (v + vs)
    s = f'{cap(src)} emits sound of frequency {fs} Hz while moving at {vs} m s⁻¹ {"towards" if towards else "away from"} a stationary observer. The speed of sound is {v} m s⁻¹.'
    if D <= 2:
        return numq(r, D, s, 'frequency heard by the observer', fo, ' Hz', f'f₀ = f_s v/(v {"−" if towards else "+"} v_s) = {fs} × {v}/({v} {"−" if towards else "+"} {vs})', [fs * v / (v + vs) if towards else fs * v / (v - vs), fs * (v + vs) / v if towards else fs * (v - vs) / v, fs], fm=f3)
    fa = fs * v / (v - vs); fr = fs * v / (v + vs)
    if D == 3:
        return Q(f'{cap(src)} of frequency {fs} Hz passes a stationary observer at a constant {vs} m s⁻¹. The speed of sound is {v} m s⁻¹. Calculate the frequencies heard as it approaches and as it recedes.', f'{f3(fa)} Hz approaching; {f3(fr)} Hz receding',
                 f'approaching f_s v/(v − v_s) = {f3(fa)} Hz [1]; receding f_s v/(v + v_s) = {f3(fr)} Hz [1]; correct assignment [1] [3]')
    f1 = round(fa); f2 = round(fr)
    vsc = v * (f1 - f2) / (f1 + f2); fsc = 2 * f1 * f2 / (f1 + f2)
    return Q(f'An observer by a straight road in {city(r)} hears {src} at {f1} Hz as it approaches and {f2} Hz as it moves away at the same speed. The speed of sound is {v} m s⁻¹. Determine the speed of the source and the frequency it emits.',
             f'v_s = {f3(vsc)} m s⁻¹; f_s = {f3(fsc)} Hz', f'{f1} = f_s v/(v − v_s) and {f2} = f_s v/(v + v_s) [1]; divide: {f1}/{f2} = (v + v_s)/(v − v_s) [1]; v_s = {f3(vsc)} m s⁻¹ [1]; f_s = {f3(fsc)} Hz [1]' + (' [4]' if D == 4 else '; assumes source moves directly along line to observer [1] [5]'), 'multi_step')


def _dop_c4(r, D):
    fs = r.choice([600, 800, 900]); vs = r.choice([20, 25, 30]); v = 340
    intro = r.choice([f'A fire engine with a siren of frequency {fs} Hz drives past {person(r)} at {vs} m s⁻¹ on a straight road in {city(r)}. The speed of sound is {v} m s⁻¹.', f'A model aircraft emitting a {fs} Hz tone flies past a microphone at {vs} m s⁻¹. The speed of sound is {v} m s⁻¹.'])
    parts = [
        lambda r: ('Calculate the frequency heard as the source approaches.', f'{f3(fs * v / (v - vs))} Hz', 'f_s v/(v − v_s) [2]'),
        lambda r: ('Calculate the frequency heard as the source moves away.', f'{f3(fs * v / (v + vs))} Hz', 'f_s v/(v + v_s) [2]'),
        lambda r: ('Calculate the wavelength of the sound in front of the source.', f'{f3((v - vs) / fs)} m', 'λ = (v − v_s)/f_s [2]'),
        lambda r: ('Explain why the observed frequency changes although the source frequency is constant.', 'The source moves between emitting wavefronts, changing the wavelength reaching the observer; wave speed is constant so frequency changes.', 'wavelength changes [1]; same speed so f changes [1] [2]'),
        lambda r: ('Sketch how the observed frequency varies with time as the source passes.', 'constant high value, rapid drop at closest approach, constant low value', 'shape [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t103.add('C4', (2, 3, 4, 5), 'multi_step')(_dop_c4)

N104 = 'Electromagnetic spectrum and speed of light'
t104 = topic(N104, N104.lower(), 'electromagnetic spectrum', 'speed of light')
EMR = [('radio waves', '> 10⁻¹ m', 1.0), ('microwaves', '10⁻³ m to 10⁻¹ m', 1e-2), ('infrared', '7 × 10⁻⁷ m to 10⁻³ m', 1e-5), ('visible light', '4 × 10⁻⁷ m to 7 × 10⁻⁷ m', 5e-7),
       ('ultraviolet', '10⁻⁸ m to 4 × 10⁻⁷ m', 1e-7), ('X-rays', '10⁻¹³ m to 10⁻⁸ m', 1e-10), ('γ-rays', '< 10⁻¹¹ m', 1e-13)]
FX(t104, 'C1', (1, 2), [
    ('What is the speed of electromagnetic waves in a vacuum?', '3.00 × 10⁸ m s⁻¹', 'c = 3.00 × 10⁸ m s⁻¹ for all EM waves.', ['3.40 × 10² m s⁻¹', '3.00 × 10⁶ m s⁻¹', 'It depends on the frequency']),
    ('Which list is in order of increasing wavelength?', 'γ-rays, X-rays, ultraviolet, visible', 'Wavelength increases from γ-rays to radio.', ['radio, microwave, infrared, visible', 'visible, ultraviolet, X-rays, γ-rays', 'X-rays, γ-rays, visible, ultraviolet']),
    ('Which is the approximate wavelength range of visible light in a vacuum?', '400 nm to 700 nm', 'Violet ≈ 400 nm to red ≈ 700 nm.', ['40 nm to 70 nm', '4 µm to 7 µm', '400 µm to 700 µm']),
    ('All electromagnetic waves', 'are transverse and can travel through a vacuum', 'They are oscillating electric and magnetic fields.', ['are longitudinal', 'need a medium', 'have the same frequency']),
    ('What is the frequency of microwaves of wavelength 3.0 cm?', '1.0 × 10¹⁰ Hz', 'f = c/λ = 3.0 × 10⁸/0.030.', ['1.0 × 10⁸ Hz', '9.0 × 10⁶ Hz', '1.0 × 10⁻¹⁰ Hz']),
    ('Which electromagnetic radiation has a wavelength of about 10⁻¹⁰ m?', 'X-rays', 'Around atomic spacing: X-rays.', ['infrared', 'microwaves', 'radio waves']),
    ('State the order of magnitude of the wavelength of infrared radiation.', '10⁻⁶ m to 10⁻⁵ m (between 7 × 10⁻⁷ m and 10⁻³ m)', 'any value in the infrared range [1]'),
])
FX(t104, 'C2', (1, 2, 3, 4), [
    ('Explain why electromagnetic waves can be polarised but sound waves in air cannot.', 'EM waves are transverse (the oscillations can be restricted to one plane); sound in air is longitudinal, with oscillations along the direction of travel.', 'EM transverse [1]; sound longitudinal [1] [2]'),
    ('State two properties shared by all electromagnetic waves and one property that differs between regions.', 'Shared: transverse, travel at 3.00 × 10⁸ m s⁻¹ in a vacuum, need no medium; different: wavelength/frequency (and photon energy).', 'two shared properties [1]; differing property [1] [2]'),
    ('Explain why there is a time delay in a radio conversation with astronauts on the Moon.', 'Radio waves travel at a finite speed c; the Moon is about 3.8 × 10⁸ m away, so each signal takes about 1.3 s.', 'finite speed c [1]; delay from distance/c [1] [2]'),
])


@t104.add('C1', (1, 2, 3))
def t104_region(r, D):
    nm, rng, lam = r.choice(EMR)
    x = lam * r.choice([1, 2, 3, 5])
    fm = lambda v: sci(v, 1).replace('.0 ×', ' ×')
    opts, a = mcq(r, nm, [e[0] for e in EMR if e[0] != nm])
    if D >= 3:
        return Q(f'Electromagnetic radiation has a frequency of {sci(C0 / x, 2)} Hz. Calculate its wavelength and identify the region of the spectrum.', f'{sci(x, 2)} m: {nm}', f'λ = c/f = {sci(x, 2)} m [1]; {nm} (range {rng}) [1] [2]', 'short')
    return Q(f'Electromagnetic radiation has a wavelength of {fm(x)} m in a vacuum. In which region of the spectrum is it?', a, f'{cap(nm)}: wavelength range {rng}.', opts=opts)


@t104.add('C3', (1, 2, 3, 4), 'numerical')
def t104_calc(r, D):
    sc = r.choice([('An FM radio station broadcasts at', 'MHz', [88.1, 94.6, 101.3, 105.8], 1e6), ('A Wi-Fi router transmits at', 'GHz', [2.4, 5.0, 5.8], 1e9), ('A mobile phone signal has a frequency of', 'MHz', [900, 1800, 2100], 1e6),
                   ('A green laser emits light of frequency', 'THz', [563, 545], 1e12), ('An AM radio station broadcasts at', 'kHz', [198, 648, 909, 1215], 1e3)])
    lead, u, vals, mul = sc
    f = r.choice(vals) * mul
    lam = C0 / f
    if D <= 2:
        return numq(r, D, f'{lead} {nf(f / mul)} {u}.', 'wavelength in a vacuum', lam, ' m', f'λ = c/f = 3.00 × 10⁸/{sci(f, 3)}', [lam * 1000, lam / 1000, f / C0], fm=lambda x: E(x, 3))
    d = r.choice([3.84e8, 1.5e11, 3.6e7, 4.2e16])
    nm = {3.84e8: 'the Moon', 1.5e11: 'the Sun', 3.6e7: 'a geostationary satellite', 4.2e16: 'the nearest star, Proxima Centauri'}[d]
    t = d / C0
    return Q(f'{lead} {nf(f / mul)} {u}. Calculate the wavelength of the signal and the time taken for an electromagnetic signal to travel from Earth to {nm}, a distance of {sci(d, 2)} m.', f'λ = {E(lam, 3)} m; t = {E(t, 3)} s',
             f'λ = c/f = {E(lam, 3)} m [1]; t = d/c [1]; = {E(t, 3)} s [1]' + (' [3]' if D == 3 else '; correct use of prefix/standard form throughout [1] [4]'))


def _em_c4(r, D):
    lam1 = r.choice([450, 500, 550, 600]) * 1e-9; f2 = r.choice([2.4, 5.0]) * 1e9
    intro = r.choice([f'A space probe sends data to Earth by microwaves of frequency {nf(f2 / 1e9)} GHz and carries a camera sensitive to light of wavelength {nf(lam1 * 1e9)} nm.', f'A communications satellite above {city(r)} uses microwaves of frequency {nf(f2 / 1e9)} GHz and an optical link using light of wavelength {nf(lam1 * 1e9)} nm.'])
    parts = [
        lambda r: ('Calculate the wavelength of the microwaves.', f'{f3(C0 / f2)} m', 'λ = c/f [2]'),
        lambda r: ('Calculate the frequency of the light.', f'{sci(C0 / lam1, 3)} Hz', 'f = c/λ [2]'),
        lambda r: ('State two properties common to both radiations.', 'transverse; speed 3.00 × 10⁸ m s⁻¹ in a vacuum; no medium needed', 'any two of: transverse [1]; same speed c in a vacuum [1]; no medium needed [1] (max 2) [2]'),
        lambda r: ('Name a region of the spectrum with wavelengths between those of the two radiations.', 'infrared', 'infrared [1]'),
        lambda r: ('Explain why both signals from a distant probe arrive at the same time if sent together.', 'All EM waves travel at the same speed c in a vacuum.', 'same speed [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t104.add('C4', (2, 3, 4, 5), 'multi_step')(_em_c4)

N105 = "Polarisation and Malus's law"
t105 = topic(N105, N105.lower(), 'polarisation', "malus's law")
FX(t105, 'C1', (1, 2), [
    ('Which type of wave can be polarised?', 'Transverse waves only', 'Polarisation restricts oscillations to one plane perpendicular to the direction of travel.', ['Longitudinal waves only', 'Both transverse and longitudinal waves', 'Sound waves only']),
    ("Plane-polarised light of intensity I₀ passes through a polariser whose transmission axis is at angle θ to the plane of polarisation. What is the transmitted intensity (Malus's law)?", 'I₀ cos² θ', "Malus's law: I = I₀ cos² θ.", ['I₀ cos θ', 'I₀ sin² θ', 'I₀/cos² θ']),
    ('Plane-polarised light passes through a polarising filter at 90° to its plane of polarisation. The transmitted intensity is', 'zero', 'cos² 90° = 0.', ['I₀', 'I₀/2', 'I₀/4']),
    ('Unpolarised light passes through one ideal polarising filter. What fraction of the intensity is transmitted?', 'one half', 'Average of cos² θ over all angles is ½.', ['all of it', 'one quarter', 'none of it']),
    ('Plane-polarised light passes through an analyser at 60° to its plane of polarisation. What fraction of the intensity is transmitted?', '0.25', 'cos² 60° = 0.25.', ['0.50', '0.75', '0.87']),
    ('State what is meant by plane-polarised light.', 'Light in which the oscillations (of the electric field) are in one plane only, containing the direction of travel.', 'oscillations in one plane [1]'),
])
FX(t105, 'C2', (1, 2, 3, 4), [
    ('Explain why polarisation provides evidence that light is a transverse wave.', 'Only transverse waves have oscillations perpendicular to the direction of travel that can be restricted to one plane; light can be polarised (blocked by crossed polaroids), so it must be transverse.', 'polarisation only possible for transverse [1]; light is polarised by filters [1] [2]'),
    ('Describe what is seen when an analyser is rotated through 360° in front of a beam of plane-polarised light.', 'The transmitted intensity varies: maximum when axes are parallel, zero when perpendicular; two maxima and two minima per rotation.', 'varies between max and zero [1]; two of each per rotation [1] [2]'),
    ('Explain how polarising sunglasses reduce glare from a wet road.', 'Light reflected from horizontal surfaces is partly polarised horizontally; the lenses have vertical transmission axes and absorb much of it.', 'reflected light partially polarised [1]; filter axis perpendicular absorbs it [1] [2]'),
])


@t105.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t105_malus(r, D):
    I0 = r.choice([4.0, 6.0, 8.0, 12.0, 20.0, 50.0]); th = r.choice([15, 20, 30, 40, 45, 50, 60, 70])
    I = I0 * math.cos(math.radians(th)) ** 2
    s = f'Plane-polarised light of intensity {nf(I0)} W m⁻² is incident on a polarising filter whose transmission axis is at {th}° to the plane of polarisation.'
    if D <= 2:
        return numq(r, D, s, 'transmitted intensity', I, ' W m⁻²', f'I = I₀ cos² θ = {nf(I0)} × cos² {th}°', [I0 * math.cos(math.radians(th)), I0 * math.sin(math.radians(th)) ** 2, I0 / 2], fm=f3)
    if D == 3:
        frac = r.choice([0.25, 0.50, 0.75, 0.10])
        ang = math.degrees(math.acos(math.sqrt(frac)))
        return Q(f'Plane-polarised light of intensity {nf(I0)} W m⁻² passes through an analyser. Calculate the angle between the plane of polarisation and the transmission axis of the analyser for the transmitted intensity to be {nf(frac * I0, 3)} W m⁻².', f'{f3(ang)}°',
                 f'cos² θ = {nf(frac * I0, 3)}/{nf(I0)} = {nf(frac)} [1]; cos θ = {nf(math.sqrt(frac), 3)} [1]; θ = {f3(ang)}° [1] [3]')
    I1 = I0 / 2; I2 = I1 * math.cos(math.radians(th)) ** 2
    return Q(f'Unpolarised light of intensity {nf(I0)} W m⁻² passes through a polariser and then an analyser whose axis is at {th}° to that of the polariser. (a) Calculate the intensity after the polariser. (b) Calculate the intensity after the analyser. (c) State the angle that would give zero final intensity.',
             f'(a) {f3(I1)} W m⁻² (b) {f3(I2)} W m⁻² (c) 90°', f'(a) half transmitted: {f3(I1)} W m⁻² [1] (b) I = {f3(I1)} cos² {th}° [1]; = {f3(I2)} W m⁻² [1] (c) 90° (crossed) [1]' + (' [4]' if D == 4 else '; ideal filters assumed (no absorption of the transmitted component) [1] [5]'), 'multi_step')


@t105.add('C2', (2, 3, 4), 'explain')
def t105_err(r, D):
    I0 = r.choice([8.0, 10.0, 12.0, 16.0]); th = r.choice([30, 45, 60])
    who = person(r)
    wrong = I0 * math.cos(math.radians(th))
    return Q(f'{who} calculates the intensity of plane-polarised light ({nf(I0)} W m⁻²) transmitted by a filter at {th}° to the plane of polarisation as {nf(wrong, 3)} W m⁻². Identify the error and give the correct value. Explain why the amplitude is reduced by cos θ but the intensity by cos² θ.',
             f'{who} used cos θ instead of cos² θ; I = {nf(I0 * math.cos(math.radians(th)) ** 2, 3)} W m⁻². The filter transmits the component of the amplitude A cos θ, and intensity ∝ amplitude².',
             'cos θ used instead of cos² θ [1]; correct value [1]; amplitude component A cos θ and I ∝ A² [1] [3]')


def _pol_c4(r, D):
    I0 = r.choice([10.0, 16.0, 24.0]); th = r.choice([30, 40, 60])
    intro = r.choice([f'A student in {lab(r)} shines unpolarised light of intensity {nf(I0)} W m⁻² through two polarising filters, P and Q, and onto a light sensor.', f'Two polaroid sheets are placed in a beam of unpolarised light of intensity {nf(I0)} W m⁻².'])
    parts = [
        lambda r: ('State the intensity after the first filter.', f'{nf(I0 / 2)} W m⁻²', 'half [1]'),
        lambda r: (f'Filter Q is at {th}° to filter P. Calculate the intensity reaching the sensor.', f'{f3(I0 / 2 * math.cos(math.radians(th)) ** 2)} W m⁻²', "Malus's law [2]"),
        lambda r: ("State Malus's law.", 'I = I₀ cos² θ, where θ is the angle between the plane of polarisation and the transmission axis.', 'equation with θ defined [1]'),
        lambda r: ('Explain why this experiment shows light is a transverse wave.', 'Intensity falls to zero when the filters are crossed; only transverse waves can be polarised.', 'zero when crossed [1]; transverse only [1] [2]'),
        lambda r: ('A third filter is placed between P and Q when they are crossed. Explain why some light now reaches the sensor.', 'The middle filter at an intermediate angle transmits a component of the polarised light, which then has a component along Q\'s axis.', 'middle filter changes plane of polarisation [1]; component passes Q [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t105.add('C4', (2, 3, 4, 5), 'multi_step')(_pol_c4)

CHAPTERS[10] = [t101, t102, t103, t104, t105]

# ===================================================================== 11 Superposition
N111 = 'Stationary waves: formation, nodes and antinodes'
t111 = topic(N111, N111.lower(), 'stationary waves', 'nodes and antinodes')
FX(t111, 'C1', (1, 2), [
    ('What is the distance between two adjacent nodes on a stationary wave?', 'Half a wavelength', 'Nodes are λ/2 apart.', ['One wavelength', 'A quarter of a wavelength', 'Two wavelengths']),
    ('A stationary wave is formed by', 'two waves of the same frequency travelling in opposite directions overlapping', 'Superposition of identical waves travelling in opposite directions.', ['two waves of different frequency travelling in the same direction', 'a single wave reflecting at an angle', 'two waves with different speeds']),
    ('Points between two adjacent nodes on a stationary wave', 'oscillate in phase with different amplitudes', 'All points in one loop are in phase; amplitude varies from zero at nodes to maximum at the antinode.', ['oscillate with the same amplitude and different phases', 'do not oscillate', 'have a phase difference of 90°']),
    ('A string fixed at both ends vibrates at its fundamental frequency. Its length L is related to the wavelength by', 'L = λ/2', 'Nodes at each end, one antinode in the middle.', ['L = λ', 'L = λ/4', 'L = 2λ']),
    ('An air column closed at one end resonates at its lowest frequency. The length of the column is', 'λ/4', 'Node at the closed end, antinode at the open end.', ['λ/2', 'λ', '3λ/2']),
    ('Unlike a progressive wave, a stationary wave', 'does not transfer energy along the wave', 'Energy is stored in the oscillation, not transmitted.', ['transfers energy faster', 'has no nodes', 'has points with all phases']),
    ('State what is meant by a node.', 'A point on a stationary wave where the amplitude is always zero.', 'zero amplitude / no displacement [1]'),
])
FX(t111, 'C2', (1, 2, 3, 4), [
    ('Explain how a stationary wave is formed on a string fixed at both ends.', 'A wave travels along the string and is reflected at the fixed ends; the incident and reflected waves (same speed, frequency and amplitude) travel in opposite directions and superpose, giving fixed nodes and antinodes.', 'reflection at ends [1]; waves travelling in opposite directions with same f [1]; superposition forms nodes/antinodes [1] [3]'),
    ('State two differences between a stationary wave and a progressive wave.', 'Stationary: no energy transfer along the wave; amplitude varies with position (nodes and antinodes); points in a loop are in phase. Progressive: transfers energy; constant amplitude; phase varies continuously.', 'any two correct differences [2]'),
    ('Describe how microwaves and a metal plate can be used to measure the wavelength of microwaves.', 'Reflect microwaves from a metal plate to form a stationary wave; move a detector along the line and find positions of minimum signal (nodes); distance between adjacent nodes = λ/2; measure across several nodes.', 'stationary wave by reflection [1]; locate nodes with detector [1]; node spacing = λ/2 over several nodes [1] [3]'),
    ('Explain why there is always a node at the closed end of a resonance tube.', 'Air molecules at the closed end cannot move (displacement must be zero), so there is a displacement node.', 'air cannot move at closed end [1]; displacement node [1] [2]'),
])


@t111.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t111_string(r, D):
    L = r.choice([0.60, 0.75, 0.80, 1.0, 1.2, 1.5]); n = r.choice([1, 2, 3, 4]); f = r.choice([50, 60, 80, 100, 120, 150])
    lam = 2 * L / n; v = f * lam
    s = f'A string of length {nf(L)} m is fixed at both ends and vibrated by a signal generator at {f} Hz. A stationary wave with {n} loop{"s" if n > 1 else ""} (antinode{"s" if n > 1 else ""}) is seen.'
    if D <= 2:
        return numq(r, D, s, 'wavelength of the waves on the string', lam, ' m', f'{n} loops = {n} × λ/2 = {nf(L)} m → λ = 2L/{n}', [L / n, L * n, 4 * L / n], fm=f3)
    if D == 3:
        return Q(s + ' Calculate the speed of the waves on the string and the fundamental frequency.', f'v = {f3(v)} m s⁻¹; f₁ = {f3(v / (2 * L))} Hz', f'λ = 2L/{n} = {f3(lam)} m [1]; v = fλ = {f3(v)} m s⁻¹ [1]; f₁ = v/(2L) = {f3(v / (2 * L))} Hz [1] [3]')
    return Q(s + ' (a) Calculate the speed of the waves. (b) Calculate the frequency needed for one more loop. (c) State the number of nodes and the distance between adjacent antinodes. (d) Explain why points in adjacent loops are in antiphase.',
             f'(a) {f3(v)} m s⁻¹ (b) {f3(v * (n + 1) / (2 * L))} Hz (c) {n + 1} nodes; {f3(lam / 2)} m (d) the displacement reverses across each node.',
             f'(a) λ = {f3(lam)} m, v = fλ = {f3(v)} m s⁻¹ [1] (b) f = (n + 1)v/2L = {f3(v * (n + 1) / (2 * L))} Hz [1] (c) {n + 1} nodes [1]; λ/2 = {f3(lam / 2)} m [1] (d) antiphase across a node [1] [5]', 'multi_step')


@t111.add('C3', (2, 3, 4, 5), 'numerical')
def t111_tube(r, D):
    v = r.choice([330, 336, 340, 344]); f = r.choice([256, 288, 320, 384, 426, 512])
    lam = v / f; l1 = lam / 4; l2 = 3 * lam / 4
    sc = f'A tuning fork of frequency {f} Hz is held over a resonance tube closed at one end by water. The first resonance occurs when the air column is {nf(l1 * 100, 3)} cm long and the second when it is {nf(l2 * 100, 3)} cm long.'
    if D <= 3:
        return Q(sc + ' Use the difference between the lengths to calculate the speed of sound.', f'{f3(v)} m s⁻¹', f'l₂ − l₁ = λ/2 = {nf((l2 - l1) * 100, 3)} cm [1]; λ = {f3(lam)} m [1]; v = fλ = {f3(v)} m s⁻¹ [1] [3]')
    e = 0.3 * r.choice([1.0, 1.2]) * 0.02
    return Q(sc.replace(f'{nf(l1 * 100, 3)} cm long', f'{nf((l1 - e) * 100, 3)} cm long').replace(f'{nf(l2 * 100, 3)} cm long', f'{nf((l2 - e) * 100, 3)} cm long') + ' (a) Calculate the speed of sound. (b) Show that λ/4 is greater than the first length and explain why. (c) Explain why using the difference between the two lengths gives a more accurate result.',
             f'(a) {f3(v)} m s⁻¹ (b) λ/4 = {nf(l1 * 100, 3)} cm > {nf((l1 - e) * 100, 3)} cm because the antinode is slightly above the open end (end correction). (c) The end correction cancels in the difference.',
             f'(a) λ/2 = difference [1]; v = {f3(v)} m s⁻¹ [1] (b) λ/4 = {nf(l1 * 100, 3)} cm [1]; end correction [1] (c) end correction cancels [1] [5]', 'multi_step')


@t111.add('C3', (2, 3, 4), 'numerical')
def t111_micro(r, D):
    lam = r.choice([2.8, 3.0, 3.2]) * 1e-2; n = r.choice([4, 5, 6, 8])
    d = n * lam / 2
    return Q(f'Microwaves reflected from a metal plate form a stationary wave. A detector moved along the line finds {n + 1} consecutive minima spread over a distance of {nf(d * 100, 3)} cm. Calculate the wavelength and the frequency of the microwaves.',
             f'λ = {nf(lam * 100, 3)} cm; f = {sci(C0 / lam, 3)} Hz', f'{n + 1} minima span {n} half-wavelengths [1]; λ = 2 × {nf(d * 100, 3)}/{n} = {nf(lam * 100, 3)} cm [1]; f = c/λ = {sci(C0 / lam, 3)} Hz [1] [3]')


def _sw_c4(r, D):
    L = r.choice([0.80, 1.0, 1.2]); f1 = r.choice([60, 75, 90])
    v = 2 * L * f1
    intro = r.choice([f'A string of length {nf(L)} m on an instrument made in {city(r)} has a fundamental frequency of {f1} Hz.', f'In {lab(r)}, a wire of length {nf(L)} m is stretched between two fixed points; its fundamental frequency is {f1} Hz.'])
    parts = [
        lambda r: ('Sketch the stationary wave at the fundamental frequency, labelling nodes N and antinodes A.', 'one loop: N at each end, A in the middle', 'N at ends [1]; A in middle [1] [2]'),
        lambda r: ('Calculate the wavelength of the fundamental.', f'{nf(2 * L)} m', 'λ = 2L [1]'),
        lambda r: ('Calculate the speed of waves on the string.', f'{f3(v)} m s⁻¹', 'v = fλ [2]'),
        lambda r: ('Calculate the frequency of the second harmonic.', f'{2 * f1} Hz', '2f₁ [1]'),
        lambda r: ('Explain how the stationary wave is formed.', 'waves reflected at the fixed ends travel in opposite directions and superpose', 'reflection [1]; superposition of opposite waves [1] [2]'),
        lambda r: ('State the phase difference between points on either side of a node.', '180° (π rad)', 'antiphase [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t111.add('C4', (2, 3, 4, 5), 'multi_step')(_sw_c4)

N112 = 'Diffraction of waves'
t112 = topic(N112, N112.lower(), 'diffraction')
FX(t112, 'C1', (1, 2), [
    ('What is meant by diffraction?', 'The spreading of a wave as it passes through a gap or around an edge', 'Diffraction is spreading at gaps/edges.', ['The change of direction of a wave entering a new medium', 'The bouncing of a wave off a surface', 'The addition of two waves']),
    ('Diffraction through a gap is most noticeable when the gap width is', 'similar to the wavelength', 'Maximum spreading when gap ≈ λ.', ['much larger than the wavelength', 'much smaller than the amplitude', 'equal to the amplitude']),
    ('When a wave diffracts through a gap, its wavelength', 'stays the same', 'Speed and frequency unchanged, so λ unchanged.', ['increases', 'decreases', 'becomes zero']),
    ('Why can sound be heard round a corner but light cannot be seen round it?', 'Sound wavelengths are comparable to doorways but light wavelengths are much smaller', 'Diffraction depends on λ compared with the gap.', ['Sound travels faster than light', 'Light cannot be diffracted', 'Sound is a transverse wave']),
    ('Water waves pass through a gap. The gap is made narrower (but still wider than λ). The diffraction', 'increases', 'Narrower gap, closer to λ, more spreading.', ['decreases', 'stays the same', 'stops']),
    ('State what happens to the frequency of a wave when it is diffracted.', 'It is unchanged.', 'unchanged [1]'),
])
FX(t112, 'C2', (1, 2, 3, 4), [
    ('Describe how a ripple tank can be used to demonstrate diffraction.', 'Plane waves from a vibrating bar pass through a gap between barriers; the pattern of wavefronts beyond the gap is viewed by shining light from above; vary the gap width to compare spreading.', 'plane waves and gap [1]; observe wavefronts beyond gap [1]; vary gap [1] [3]'),
    ('Explain why long-wave radio signals can be received in valleys where short-wave signals cannot.', 'Long-wave radio has wavelengths comparable to hills, so it diffracts around them; shorter wavelengths diffract much less.', 'long λ diffracts round hills [1]; short λ little diffraction [1] [2]'),
    ('Explain why a satellite dish must be accurately aligned with the satellite.', 'The microwaves have a short wavelength compared with the dish size, so they diffract very little and form a narrow beam.', 'λ ≪ dish size [1]; little diffraction / narrow beam [1] [2]'),
])


@t112.add('C2', (2, 3, 4), 'explain')
def t112_gap(r, D):
    sc = r.choice([('sound of frequency {f} Hz', 340, [170, 340, 680, 1000, 3400]), ('water waves of wavelength {l} cm in a ripple tank', None, [1.0, 1.5, 2.0, 3.0]), ('microwaves of frequency {f} GHz', 3e8, [10, 12, 15])])
    txt, v, vals = sc
    x = r.choice(vals)
    if v is None:
        lam = x / 100; desc = txt.format(l=nf(x))
    elif v == 340:
        lam = v / x; desc = txt.format(f=x)
    else:
        lam = v / (x * 1e9); desc = txt.format(f=x)
    gap = lam * r.choice([0.8, 1.0, 10, 30])
    much = gap > 5 * lam
    return Q(f'Waves of {desc} pass through a gap {E(gap, 2)} m wide. The wavelength is {E(lam, 2)} m. Describe and explain the diffraction observed beyond the gap.',
             ('Little diffraction: the gap is much wider than the wavelength, so the wavefronts pass through mostly straight with slight curving at the edges.' if much else 'Strong diffraction: the gap is similar to the wavelength, so the waves spread out into nearly circular wavefronts.') + ' The wavelength is unchanged.',
             'compares gap with wavelength [1]; correct extent of spreading [1]; wavelength unchanged [1] [3]')


@t112.add('C3', (1, 2, 3, 4), 'numerical')
def t112_lam(r, D):
    f = r.choice([256, 340, 512, 680, 1000, 2000]); v = 340
    lam = v / f
    door = r.choice([0.8, 0.9, 1.0])
    if D <= 2:
        return numq(r, D, f'Sound of frequency {f} Hz travels at {v} m s⁻¹ towards a doorway {nf(door)} m wide.', 'wavelength of the sound', lam, ' m', f'λ = v/f = {v}/{f}', [f / v, v * f / 1e4, lam * 2], fm=f3)
    lam_l = 5.5e-7
    return Q(f'Sound of frequency {f} Hz (speed {v} m s⁻¹) and green light (wavelength 550 nm) pass through an open doorway {nf(door)} m wide. Calculate the ratio gap/wavelength for each and use the values to explain why a person beyond the doorway, out of line of sight, can hear but not see a speaker.',
             f'sound: {f3(door / lam)}; light: {sci(door / lam_l, 2)}. Sound diffracts significantly (gap ≈ λ); light hardly diffracts (gap ≫ λ).',
             f'λ_sound = {f3(lam)} m [1]; ratios {f3(door / lam)} and {sci(door / lam_l, 2)} [1]; significant diffraction only when gap ~ λ [1]' + (' [3]' if D == 3 else '; conclusion linked to hearing but not seeing [1] [4]'))


def _diff_c4(r, D):
    lam = r.choice([1.5, 2.0, 2.5]); g1 = lam; g2 = lam * 8
    intro = r.choice([f'Plane water waves of wavelength {nf(lam)} cm in a ripple tank in {lab(r)} meet a barrier containing a gap.', f'A harbour model is built in a ripple tank; waves of wavelength {nf(lam)} cm approach the harbour entrance.'])
    parts = [
        lambda r: (f'Describe the wavefronts beyond a gap of width {nf(g1)} cm.', 'Strongly curved, nearly semicircular, same wavelength', 'semicircular spreading [1]; same λ [1] [2]'),
        lambda r: (f'Describe the wavefronts beyond a gap of width {nf(g2)} cm.', 'Mostly straight with slight curving at the edges, same wavelength', 'mostly straight [1]; edges curved [1] [2]'),
        lambda r: ('State what is meant by diffraction.', 'Spreading of a wave through a gap or around an obstacle.', 'definition [1]'),
        lambda r: ('Explain why the speed of the waves does not change on diffraction.', 'The medium (depth of water) is unchanged; speed depends on the medium.', 'same medium [1]'),
        lambda r: ('Suggest why harbour engineers prefer a wide entrance for calm water beside the entrance.', 'Waves through a gap much wider than λ spread little into the sheltered areas.', 'little spreading [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t112.add('C4', (2, 3, 4, 5), 'multi_step')(_diff_c4)
t112.add('C3', (3, 4, 5), 'multi_step')(_diff_c4)

N113 = 'Interference, coherence and the double-slit experiment λ = ax/D'
t113 = topic(N113, N113.lower(), 'interference', 'double-slit experiment')
FX(t113, 'C1', (1, 2), [
    ('What is meant by coherent sources?', 'Sources that have a constant phase difference', 'Coherence: constant phase difference (and so same frequency).', ['Sources that have the same amplitude', 'Sources that are in the same place', 'Sources that have different frequencies']),
    ('For constructive interference between waves from two coherent sources in phase, the path difference must be', 'a whole number of wavelengths', 'Path difference = nλ.', ['an odd number of half wavelengths', 'zero only', 'a quarter of a wavelength']),
    ('In a double-slit experiment, λ = 600 nm, slit separation a = 0.50 mm and D = 2.0 m. What is the fringe separation?', '2.4 mm', 'x = λD/a = 600 × 10⁻⁹ × 2.0/0.50 × 10⁻³.', ['0.24 mm', '24 mm', '1.5 mm']),
    ('In a double-slit experiment the slit separation is halved. The fringe separation', 'doubles', 'x = λD/a ∝ 1/a.', ['halves', 'stays the same', 'quadruples']),
    ('Destructive interference occurs where the path difference is', 'an odd number of half wavelengths', '(n + ½)λ gives antiphase waves.', ['a whole number of wavelengths', 'zero', 'equal to the slit separation']),
    ('Which change makes the fringes in a double-slit experiment closer together?', 'Using blue light instead of red light', 'x ∝ λ; blue has a shorter wavelength.', ['Moving the screen further away', 'Using slits closer together', 'Using red light instead of blue light']),
    ('State the principle of superposition.', 'When two or more waves meet at a point, the resultant displacement is the sum of the individual displacements.', 'resultant displacement = sum of displacements [1]'),
])
FX(t113, 'C2', (1, 2, 3, 4), [
    ('Explain why two separate lamps do not produce a visible interference pattern.', 'They are not coherent: light is emitted in random bursts so the phase difference changes rapidly and randomly, and the pattern moves too fast to be seen.', 'not coherent / phase difference not constant [1]; pattern changes too rapidly [1] [2]'),
    ('Explain how a bright fringe and a dark fringe are formed in Young\'s double-slit experiment.', 'Light diffracts through each slit and the waves overlap; where the path difference is nλ the waves arrive in phase (constructive, bright); where it is (n + ½)λ they arrive in antiphase (destructive, dark).', 'diffraction and overlap [1]; path difference nλ bright [1]; (n + ½)λ dark [1] [3]'),
    ('State the conditions needed for an observable two-source interference pattern.', 'Coherent sources (constant phase difference), similar amplitudes, same type of wave (same polarisation for light), and waves must overlap.', 'coherent [1]; similar amplitude / overlap [1] [2]'),
    ('Explain why the slits in a double-slit experiment must be narrow.', 'Narrow slits diffract the light widely so that the waves from the two slits overlap over a wide region of the screen.', 'narrow slits diffract more [1]; waves overlap [1] [2]'),
])


@t113.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t113_young(r, D):
    lam = r.choice([450, 500, 550, 589, 633, 650, 700]) * 1e-9; a = r.choice([0.20, 0.25, 0.30, 0.40, 0.50, 0.80]) * 1e-3; Dd = r.choice([1.20, 1.50, 2.00, 2.50, 3.00])
    x = lam * Dd / a
    src = r.choice(['A laser', 'A sodium lamp with a filter', 'A helium-neon laser', 'A green laser pointer', 'A red diode laser'])
    k = r.choice(['x', 'lam', 'a'])
    if D <= 2:
        if k == 'x':
            return numq(r, D, f'{src} of wavelength {nf(lam * 1e9)} nm illuminates two slits {nf(a * 1000)} mm apart. Fringes form on a screen {nf(Dd)} m away.', 'fringe separation', x * 1000, ' mm', f'x = λD/a = {sci(lam, 3)} × {nf(Dd)}/{sci(a, 2)}', [x * 1e6, lam * a / Dd * 1e3 * 1e6, x * 500], fm=f3)
        if k == 'lam':
            return numq(r, D, f'{src} illuminates two slits {nf(a * 1000)} mm apart. On a screen {nf(Dd)} m away the fringe separation is {f3(x * 1000)} mm.', 'wavelength in nm', lam * 1e9, ' nm', f'λ = ax/D = {sci(a, 2)} × {sci(x, 3)}/{nf(Dd)}', [lam * 1e10, x * Dd / a * 1e6, lam * 5e8], fm=f3)
        return numq(r, D, f'{src} of wavelength {nf(lam * 1e9)} nm gives fringes {f3(x * 1000)} mm apart on a screen {nf(Dd)} m from two slits.', 'slit separation in mm', a * 1000, ' mm', f'a = λD/x', [a * 1e4, a * 100, a * 2000], fm=f3)
    n = r.choice([5, 6, 8, 10])
    if D == 3:
        return Q(f'{src} illuminates two slits {nf(a * 1000)} mm apart. On a screen {nf(Dd)} m away, {n + 1} bright fringes span {f3(n * x * 1000)} mm (centre to centre). Calculate the wavelength.', f'{f3(lam * 1e9)} nm',
                 f'{n + 1} fringes = {n} spacings: x = {f3(x * 1000)} mm [1]; λ = ax/D [1]; = {f3(lam * 1e9)} nm [1] [3]')
    return Q(f'{src} illuminates two slits {nf(a * 1000)} mm apart; the screen is {nf(Dd)} m away and {n + 1} bright fringes span {f3(n * x * 1000)} mm. (a) Calculate the wavelength. (b) Explain why measuring across {n + 1} fringes improves the result. (c) Predict the fringe separation if the screen is moved to {nf(Dd * 1.5)} m and a source of wavelength {nf(lam * 1e9 * 0.8)} nm is used.',
             f'(a) {f3(lam * 1e9)} nm (b) reduces the percentage uncertainty in x (c) {f3(x * 1.5 * 0.8 * 1000)} mm',
             f'(a) x = {f3(x * 1000)} mm [1]; λ = ax/D = {f3(lam * 1e9)} nm [1] (b) larger distance measured, smaller % uncertainty [1] (c) x ∝ λD: × 1.5 × 0.8 [1]; = {f3(x * 1.2 * 1000)} mm [1] [5]', 'multi_step')


@t113.add('C3', (2, 3, 4), 'numerical')
def t113_path(r, D):
    f = r.choice([500, 680, 850, 1000, 1700]); v = 340; lam = v / f
    d1 = r.choice([3.0, 4.0, 5.0, 6.0]); n = r.choice([0.5, 1, 1.5, 2, 2.5]); d2 = d1 + n * lam
    con = abs(n - round(n)) < 1e-9
    return Q(f'Two loudspeakers connected to the same signal generator emit sound of frequency {f} Hz in phase (speed of sound {v} m s⁻¹). A microphone is {nf(d1, 3)} m from one speaker and {nf(d2, 3)} m from the other. Determine whether the microphone detects a loud or a quiet sound.',
             f'Path difference = {nf(d2 - d1, 3)} m = {nf(n)}λ, so {"constructive interference: loud" if con else "destructive interference: quiet"}.',
             f'λ = v/f = {f3(lam)} m [1]; path difference = {nf(d2 - d1, 3)} m = {nf(n)}λ [1]; correct conclusion [1] [3]')


def _ds_c4(r, D):
    lam = r.choice([589, 633, 650]) * 1e-9; a = r.choice([0.30, 0.40, 0.50]) * 1e-3; Dd = r.choice([1.5, 2.0, 2.5])
    x = lam * Dd / a
    intro = r.choice([f'In {lab(r)}, laser light of wavelength {nf(lam * 1e9)} nm passes through a double slit of separation {nf(a * 1000)} mm onto a screen {nf(Dd)} m away.', f'{person(r)} repeats Young\'s double-slit experiment with light of wavelength {nf(lam * 1e9)} nm, slit separation {nf(a * 1000)} mm and slit-screen distance {nf(Dd)} m.'])
    parts = [
        lambda r: ('Calculate the fringe separation.', f'{f3(x * 1000)} mm', 'x = λD/a [2]'),
        lambda r: ('Explain what is meant by coherence and why the laser is suitable.', 'Constant phase difference; light from the laser passing through both slits comes from the same wavefront.', 'definition [1]; same source [1] [2]'),
        lambda r: ('State the path difference to the second bright fringe from the centre.', f'2λ = {f3(2 * lam * 1e9)} nm', '2λ [1]'),
        lambda r: ('Describe the effect on the pattern of covering one slit.', 'The interference fringes disappear; only a single-slit diffraction pattern (broad central band) remains.', 'fringes disappear [1]; diffraction pattern remains [1] [2]'),
        lambda r: ('Suggest why the fringe separation is measured across several fringes.', 'It reduces the percentage uncertainty in x.', 'reduces uncertainty [1]'),
        lambda r: ('Describe how the pattern changes if white light is used.', 'White central fringe; other fringes coloured (blue inner, red outer edges) and fewer visible.', 'white centre [1]; coloured fringes [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t113.add('C4', (2, 3, 4, 5), 'multi_step')(_ds_c4)

N114 = 'The diffraction grating d sin θ = nλ'
t114 = topic(N114, N114.lower(), 'diffraction grating', 'd sin θ = nλ')
FX(t114, 'C1', (1, 2), [
    ('A diffraction grating has 500 lines per mm. What is the line spacing d?', '2.0 × 10⁻⁶ m', 'd = 1/(500 × 10³) m.', ['5.0 × 10⁻⁵ m', '2.0 × 10⁻³ m', '5.0 × 10⁵ m']),
    ('Light of wavelength 500 nm falls normally on a grating of spacing 2.0 × 10⁻⁶ m. What is sin θ for the first order?', '0.25', 'sin θ = λ/d = 500 × 10⁻⁹/2.0 × 10⁻⁶.', ['0.50', '4.0', '0.0025']),
    ('Compared with a double slit, a diffraction grating gives maxima that are', 'sharper, brighter and more widely spaced', 'Many slits give narrow bright maxima at large angles.', ['broader and dimmer', 'closer together and dimmer', 'the same']),
    ('The highest order visible with a grating is limited because', 'sin θ cannot exceed 1', 'n ≤ d/λ.', ['the grating has too few lines', 'higher orders are always invisible', 'the wavelength changes with order']),
    ('In the zero-order maximum of a grating illuminated with white light, the light is', 'white', 'Path difference zero for all wavelengths.', ['red', 'violet', 'absent']),
    ('Which wavelength is diffracted through the largest angle in a given order?', 'red light', 'sin θ = nλ/d; red has the longest visible wavelength.', ['violet light', 'green light', 'blue light']),
    ('State the equation for a diffraction grating, defining each symbol.', 'd sin θ = nλ, where d is the line spacing, θ the angle of the nth-order maximum from the normal, n the order and λ the wavelength.', 'equation [1]; symbols defined [1] [2]'),
])
FX(t114, 'C2', (1, 2, 3, 4), [
    ('Explain why a diffraction grating gives a more accurate value of wavelength than a double-slit experiment.', 'The maxima are sharp and bright and at large, easily measured angles, so the percentage uncertainty in θ (and so in λ) is small.', 'sharp, bright maxima [1]; large angles, small % uncertainty [1] [2]'),
    ('Explain how a diffraction grating separates white light into a spectrum.', 'Each wavelength has its maxima at a different angle (sin θ = nλ/d); longer wavelengths (red) are diffracted more, so the colours spread out in each order except the zero order.', 'angle depends on λ [1]; red diffracted most, spectrum in each order [1] [2]'),
    ('Explain why the zero-order maximum is the same colour as the source.', 'At θ = 0 the path difference is zero for every wavelength, so all wavelengths interfere constructively at the same place.', 'path difference zero for all λ [1]; all colours combine [1] [2]'),
])


@t114.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t114_grating(r, D):
    N = r.choice([100, 300, 400, 500, 600, 800]); lam = r.choice([436, 486, 546, 589, 633, 656]) * 1e-9
    d = 1e-3 / N
    n = r.choice([1, 2]) if N >= 500 else r.choice([1, 2, 3])
    sn = n * lam / d
    if sn >= 1:
        n = 1; sn = lam / d
    th = math.degrees(math.asin(sn))
    src = r.choice(['Light from a laser', 'Monochromatic light from a discharge lamp', 'Light from a green laser', 'A narrow beam of light'])
    s = f'{src} of wavelength {nf(lam * 1e9)} nm is incident normally on a diffraction grating with {N} lines per mm.'
    if D <= 2:
        return numq(r, D, s, f'angle of the order {n} maximum from the normal (in degrees)', th, '°', f'd = {sci(d, 3)} m; sin θ = nλ/d = {nf(sn, 3)}', [math.degrees(math.asin(min(sn / 2, 0.99))), sn * 57.3 * 1.3, 90 - th], fm=f3)
    nmax = int(d / lam)
    if D == 3:
        return Q(s + ' Calculate the angle of the first-order maximum and the highest order that can be observed.', f'{f3(math.degrees(math.asin(lam / d)))}°; n_max = {nmax}',
                 f'd = {sci(d, 3)} m [1]; sin θ = λ/d → θ = {f3(math.degrees(math.asin(lam / d)))}° [1]; n ≤ d/λ = {nf(d / lam, 3)} so n_max = {nmax} [1] [3]')
    lam2 = lam + r.choice([20, 40, 60]) * 1e-9
    t1 = math.degrees(math.asin(lam / d)); t2 = math.degrees(math.asin(lam2 / d))
    return Q(f'Light containing wavelengths {nf(lam * 1e9)} nm and {nf(lam2 * 1e9)} nm falls normally on a grating with {N} lines per mm. (a) Calculate the first-order angles for each wavelength. (b) Calculate their angular separation. (c) Determine the total number of maxima seen for the {nf(lam * 1e9)} nm light.',
             f'(a) {f3(t1)}° and {f3(t2)}° (b) {f3(t2 - t1)}° (c) {2 * nmax + 1}', f'(a) d = {sci(d, 3)} m [1]; sin θ = λ/d for each [1] (b) difference {f3(t2 - t1)}° [1] (c) n_max = {nmax} [1]; total = 2 × {nmax} + 1 = {2 * nmax + 1} [1] [5]', 'multi_step')


@t114.add('C3', (2, 3, 4), 'numerical')
def t114_find(r, D):
    N = r.choice([300, 500, 600]); lam = r.choice([546, 589, 633]) * 1e-9; d = 1e-3 / N
    th = math.degrees(math.asin(2 * lam / d)) if 2 * lam / d < 1 else math.degrees(math.asin(lam / d))
    n = 2 if 2 * lam / d < 1 else 1
    th2 = 2 * th
    return Q(f'A student measures the angle between the two order-{n} maxima (on either side of the centre) produced by a grating with {N} lines per mm as {f3(th2)}°. Calculate the wavelength of the light.', f'{f3(lam * 1e9)} nm',
             f'θ = half of {f3(th2)}° = {f3(th)}° [1]; d = {sci(d, 3)} m [1]; λ = d sin θ/{n} = {f3(lam * 1e9)} nm [1] [3]')


relation(t114, 'C2', (2, 3), 'd sin θ = nλ', 'value of sin θ for the first-order maximum', {'wavelength': 1, 'line spacing d': -1},
         ['Light is incident normally on a diffraction grating.', 'A spectrometer uses a diffraction grating to analyse a laser beam.', 'Monochromatic light passes through a grating onto a screen.'])


def _gr_c4(r, D):
    N = r.choice([300, 400, 600]); l1 = r.choice([450, 480]) * 1e-9; l2 = r.choice([650, 700]) * 1e-9; d = 1e-3 / N
    intro = r.choice([f'White light is shone normally onto a grating with {N} lines per mm in {lab(r)}. The visible spectrum ranges from {nf(l1 * 1e9)} nm to {nf(l2 * 1e9)} nm.', f'An astronomer analyses light from a star with a grating of {N} lines per mm; the light spans {nf(l1 * 1e9)} nm to {nf(l2 * 1e9)} nm.'])
    t1 = math.degrees(math.asin(l1 / d)); t2 = math.degrees(math.asin(l2 / d))
    parts = [
        lambda r: ('Calculate the line spacing of the grating.', f'{sci(d, 3)} m', 'd = 1/N [1]'),
        lambda r: ('Calculate the angular width of the first-order spectrum.', f'{f3(t2 - t1)}°', f'angles {f3(t1)}° and {f3(t2)}° [3]'),
        lambda r: ('Determine whether the second- and third-order spectra overlap.', 'Yes' if 3 * l1 < 2 * l2 else 'No', f'compare 2 × {nf(l2 * 1e9)} nm with 3 × {nf(l1 * 1e9)} nm [2]'),
        lambda r: ('Explain why the central maximum is white.', 'Zero path difference for all wavelengths.', 'zero path difference [1]'),
        lambda r: ('Explain why the grating gives sharper maxima than a double slit.', 'Many slits: waves cancel except at exact angles where all are in phase.', 'many slits [1]; cancellation away from exact angle [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t114.add('C4', (2, 3, 4, 5), 'multi_step')(_gr_c4)

CHAPTERS[11] = [t111, t112, t113, t114]


# ===================================================================== 12 Electricity
N121 = 'Electric current, charge and the elementary charge, I = Anvq'
t121 = topic(N121, N121.lower(), 'electric current', 'i = anvq')
FX(t121, 'C1', (1, 2), [
    ('Which is the definition of the coulomb?', 'The charge passing a point when a current of 1 A flows for 1 s', 'Q = It: 1 C = 1 A s.', ['The charge on one electron', 'The current that flows when 1 V is applied across 1 Ω', 'The energy transferred per unit current']),
    ('A current of 0.40 A flows for 2.0 minutes. How much charge passes?', '48 C', 'Q = It = 0.40 × 120.', ['0.80 C', '0.20 C', '300 C']),
    ('What is the magnitude of the elementary charge?', '1.60 × 10⁻¹⁹ C', 'e = 1.60 × 10⁻¹⁹ C.', ['9.11 × 10⁻³¹ C', '6.25 × 10¹⁸ C', '1.67 × 10⁻²⁷ C']),
    ('Which charge is NOT possible for an isolated object?', '2.4 × 10⁻¹⁹ C', 'Charge is quantised in multiples of 1.60 × 10⁻¹⁹ C; 2.4 × 10⁻¹⁹ = 1.5e.', ['3.2 × 10⁻¹⁹ C', '4.8 × 10⁻¹⁹ C', '8.0 × 10⁻¹⁹ C']),
    ('In the equation I = Anvq, what does n represent?', 'The number of charge carriers per unit volume', 'n: number density of charge carriers (m⁻³).', ['The number of electrons in the wire', 'The number of turns', 'The refractive index']),
    ('Two wires of the same metal carry the same current. Wire X has half the cross-sectional area of wire Y. The drift speed in X is', 'twice that in Y', 'v = I/(nAq) ∝ 1/A.', ['half that in Y', 'the same as in Y', 'four times that in Y']),
    ('State what is meant by electric current.', 'The rate of flow of charge.', 'rate of flow of charge [1]'),
])
FX(t121, 'C2', (1, 2, 3, 4), [
    ('Explain why a lamp lights almost instantly when switched on, although the drift speed of electrons is very small.', 'The wire is already full of free electrons; the electric field is set up throughout the circuit at nearly the speed of light, so electrons everywhere start drifting at once.', 'free electrons already present throughout [1]; field established almost instantly [1] [2]'),
    ('Explain why the drift speed of electrons in a semiconductor is much greater than in a metal for the same current and area.', 'A semiconductor has far fewer charge carriers per unit volume (n much smaller); since v = I/(nAq), v must be much larger.', 'n much smaller [1]; v = I/(nAq) [1] [2]'),
    ('Explain what is meant by saying that charge is quantised.', 'Charge exists only in whole-number multiples of the elementary charge e = 1.60 × 10⁻¹⁹ C.', 'multiples of e [1]; value of e [1] [2]'),
    ('Explain why the current is the same at all points in a series circuit.', 'Charge is conserved; charge cannot build up anywhere, so the rate of flow of charge past every point is the same.', 'charge conserved [1]; no accumulation so same rate everywhere [1] [2]'),
])


@t121.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t121_q(r, D):
    I = r.choice([0.15, 0.25, 0.40, 0.60, 1.2, 2.5, 3.0]); t = r.choice([30, 45, 60, 90, 120, 300, 600])
    dev = r.choice(['a lamp', 'a heater', 'an electric motor', 'a phone charger cable', 'a resistor in a sensor circuit'])
    Q_ = I * t; N = Q_ / QE
    if D <= 2:
        return numq(r, D, f'A current of {nf(I)} A flows through {dev} for {t} s.', 'charge that flows', Q_, ' C', f'Q = It = {nf(I)} × {t}', [I / t, t / I, Q_ * 60], fm=f3)
    return Q(f'A current of {nf(I)} A flows through {dev} for {nf(t / 60, 3)} minutes. Calculate the charge that flows and the number of electrons passing any point in the circuit.', f'Q = {f3(Q_)} C; N = {sci(N, 3)}',
             f't = {t} s [1]; Q = It = {f3(Q_)} C [1]; N = Q/e = {sci(N, 3)} [1]' + (' [3]' if D == 3 else '; justification that charge is quantised in units of e [1] [4]'))


@t121.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t121_drift(r, D):
    mat, n = r.choice([('copper', 8.5e28), ('aluminium', 6.0e28), ('silver', 5.9e28), ('gold', 5.9e28)])
    dmm = r.choice([0.50, 0.80, 1.0, 1.2, 1.5, 2.0]); I = r.choice([0.50, 1.0, 2.0, 3.0, 5.0])
    A = math.pi * (dmm * 1e-3) ** 2 / 4
    v = I / (n * A * QE)
    s = f'A {mat} wire of diameter {nf(dmm)} mm carries a current of {nf(I)} A. The number of free electrons per unit volume is {sci(n, 2)} m⁻³.'
    if D <= 2:
        return numq(r, D, f'A {mat} wire of cross-sectional area {sci(A, 3)} m² carries a current of {nf(I)} A. The number of free electrons per unit volume is {sci(n, 2)} m⁻³.', 'drift speed of the electrons', v, ' m s⁻¹', f'v = I/(nAe) = {nf(I)}/({sci(n, 2)} × {sci(A, 3)} × 1.60 × 10⁻¹⁹)', [v * 1000, v / 1000, v * 4], fm=lambda x: sci(x, 3))
    if D == 3:
        return Q(s + ' Calculate the drift speed of the electrons.', f'{sci(v, 3)} m s⁻¹', f'A = πd²/4 = {sci(A, 3)} m² [1]; v = I/(nAe) [1]; = {sci(v, 3)} m s⁻¹ [1] [3]')
    return Q(s + ' (a) Calculate the drift speed. (b) The wire is joined in series to a wire of the same metal with half the diameter. Calculate the drift speed in the thinner wire and explain your answer. (c) Calculate the time for an electron to drift 1.0 m along the thicker wire.',
             f'(a) {sci(v, 3)} m s⁻¹ (b) {sci(4 * v, 3)} m s⁻¹: same current, quarter of the area (c) {sci(1 / v, 3)} s',
             f'(a) A = {sci(A, 3)} m² [1]; v = I/(nAe) = {sci(v, 3)} m s⁻¹ [1] (b) I same, A ÷ 4, so v × 4 = {sci(4 * v, 3)} m s⁻¹ [1]; reason [1] (c) t = 1.0/v = {sci(1 / v, 3)} s [1] [5]', 'multi_step')


def _cur_c4(r, D):
    I = r.choice([1.5, 2.0, 3.0]); dmm = r.choice([1.0, 1.5]); n = 8.5e28; t = r.choice([60, 120])
    A = math.pi * (dmm * 1e-3) ** 2 / 4; v = I / (n * A * QE)
    intro = r.choice([f'A copper cable of diameter {nf(dmm)} mm in a building in {city(r)} carries a steady current of {nf(I)} A. Copper has 8.5 × 10²⁸ free electrons per m³.', f'A copper connecting lead of diameter {nf(dmm)} mm carries {nf(I)} A (n = 8.5 × 10²⁸ m⁻³).'])
    parts = [
        lambda r: (f'Calculate the charge passing a point in {t} s.', f'{f3(I * t)} C', 'Q = It [1]'),
        lambda r: (f'Calculate the number of electrons passing a point in {t} s.', f'{sci(I * t / QE, 3)}', 'N = Q/e [2]'),
        lambda r: ('Calculate the drift speed.', f'{sci(v, 3)} m s⁻¹', 'v = I/(nAe) [3]'),
        lambda r: ('State what is meant by a current of one ampere in terms of charge flow.', 'One coulomb of charge passing a point per second.', '1 C s⁻¹ [1]'),
        lambda r: ('Explain why the cable does not become charged although electrons flow through it.', 'Electrons enter and leave at the same rate; the number of free electrons in the cable stays constant.', 'same rate in and out [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t121.add('C4', (2, 3, 4, 5), 'multi_step')(_cur_c4)

N122 = 'Potential difference and power: V = W/Q and P = VI = I²R'
t122 = topic(N122, N122.lower(), 'potential difference', 'p = vi')
FX(t122, 'C1', (1, 2), [
    ('Which is the definition of potential difference?', 'Energy transferred per unit charge from electrical to other forms', 'V = W/Q.', ['Charge flowing per unit time', 'Energy transferred per unit time', 'Force per unit charge']),
    ('Which unit is equivalent to the volt?', 'J C⁻¹', 'V = W/Q.', ['C J⁻¹', 'J s⁻¹', 'A Ω⁻¹']),
    ('A charge of 30 C passes through a lamp with a p.d. of 6.0 V across it. How much energy is transferred?', '180 J', 'W = QV.', ['5.0 J', '0.20 J', '36 J']),
    ('A heater has a resistance of 20 Ω and a current of 3.0 A. What is its power?', '180 W', 'P = I²R = 9.0 × 20.', ['60 W', '1200 W', '6.7 W']),
    ('A 2.0 kW kettle runs on a 230 V supply. What is the current?', '8.7 A', 'I = P/V = 2000/230.', ['460 A', '0.12 A', '115 A']),
    ('A resistor has a p.d. of 12 V across it and dissipates 36 W. What is its resistance?', '4.0 Ω', 'R = V²/P = 144/36.', ['3.0 Ω', '0.33 Ω', '432 Ω']),
    ('State the three equations for electrical power.', 'P = VI, P = I²R, P = V²/R', 'all three [2]; two [1] [2]'),
])
FX(t122, 'C2', (1, 2, 3, 4), [
    ('Derive P = I²R and P = V²/R from P = VI.', 'Using V = IR: P = I(IR) = I²R; using I = V/R: P = V(V/R) = V²/R.', 'substitute V = IR [1]; substitute I = V/R [1] [2]'),
    ('Explain why electrical power is transmitted at high voltage.', 'For a given power, P = VI so a higher V means a smaller I; the power lost in the cables, I²R, is greatly reduced.', 'higher V, lower I for same P [1]; less I²R loss [1] [2]'),
    ('Distinguish between electromotive force and potential difference.', 'e.m.f. is energy transferred from other forms to electrical per unit charge (by a source); p.d. is energy transferred from electrical to other forms per unit charge (in a component).', 'e.m.f.: other forms → electrical per unit charge [1]; p.d.: electrical → other forms [1] [2]'),
    ('Explain why a 60 W lamp and a 100 W lamp connected in series across the mains do not give their rated power outputs.', 'They are rated for the full mains voltage across each; in series they share the voltage, so each has a smaller p.d. and current, and the power of each is much less than rated.', 'voltage shared [1]; smaller power than rated [1] [2]'),
])


@t122.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t122_power(r, D):
    V = r.choice([6.0, 9.0, 12.0, 24.0, 110, 230]); R = r.choice([4.0, 6.0, 8.0, 12.0, 24.0, 48.0, 100.0, 500.0])
    if V > 100:
        R = r.choice([26.5, 40.0, 53.0, 120.0, 400.0])
    I = V / R; P = V * I
    dev = r.choice(['heating element', 'filament lamp (at its operating temperature)', 'resistor', 'immersion heater', 'hair dryer element'])
    s = f'A {dev} has a resistance of {nf(R)} Ω when connected to a {nf(V)} V supply.'
    if D <= 2:
        return numq(r, D, s, 'power dissipated', P, ' W', f'P = V²/R = {nf(V)}²/{nf(R)}', [V / R, V * R, V * V * R / 1e3], fm=f3)
    t = r.choice([5, 10, 15, 30]) * 60
    if D == 3:
        return Q(s + f' Calculate the current, the power and the energy transferred in {t // 60} minutes.', f'I = {f3(I)} A; P = {f3(P)} W; E = {f3(P * t)} J',
                 f'I = V/R = {f3(I)} A [1]; P = VI = {f3(P)} W [1]; E = Pt = {f3(P * t)} J [1] [3]')
    Q_ = I * t
    return Q(s + f' (a) Calculate the charge passing through it in {t // 60} minutes. (b) Use V = W/Q to calculate the energy transferred. (c) The supply p.d. falls by 10%. Calculate the percentage fall in power, assuming R is constant.',
             f'(a) {f3(Q_)} C (b) {f3(Q_ * V)} J (c) 19%', f'(a) I = {f3(I)} A, Q = It = {f3(Q_)} C [1] (b) W = QV = {f3(Q_ * V)} J [1] (c) P ∝ V² [1]; 0.9² = 0.81 [1]; 19% fall [1] [5]', 'multi_step')


@t122.add('C3', (2, 3, 4), 'numerical')
def t122_cable(r, D):
    P = r.choice([10, 20, 50, 100]) * 1e6; Rc = r.choice([2.0, 4.0, 5.0, 8.0]); V1 = r.choice([33, 132, 275, 400]) * 1e3
    I = P / V1; loss = I * I * Rc
    return Q(f'A power station in {city(r)} transmits {sci(P, 2)} W through cables of total resistance {nf(Rc)} Ω at {nf(V1 / 1000)} kV. Calculate the current in the cables and the power lost in them, and express the loss as a percentage of the power transmitted.',
             f'I = {f3(I)} A; loss = {E(loss, 3)} W; {nf(100 * loss / P, 2)}%', f'I = P/V = {f3(I)} A [1]; P_loss = I²R = {E(loss, 3)} W [1]; percentage = {nf(100 * loss / P, 2)}% [1] [3]')


relation(t122, 'C2', (2, 3), 'P = I²R', 'power dissipated in the resistor', {'current': 2},
         ['A fixed resistor obeys Ohm\'s law and stays at constant temperature.', 'A heating element of constant resistance is connected to a variable supply.', 'A transmission cable has a constant resistance.'])


def _pd_c4(r, D):
    P = r.choice([1200, 2000, 2500]); V = 230; t = r.choice([3, 4, 5])
    intro = r.choice([f'An electric kettle in a home in {city(r)} is rated at {P} W, {V} V. It takes {t} minutes to boil some water.', f'A {P} W, {V} V heater is switched on for {t} minutes.'])
    I = P / V; R = V * V / P
    parts = [
        lambda r: ('Calculate the current.', f'{f3(I)} A', 'I = P/V [1]'),
        lambda r: ('Calculate the resistance of the element.', f'{f3(R)} Ω', 'R = V²/P [2]'),
        lambda r: ('Calculate the charge that flows.', f'{f3(I * t * 60)} C', 'Q = It [2]'),
        lambda r: ('Calculate the energy transferred.', f'{f3(P * t * 60)} J', 'W = Pt or QV [2]'),
        lambda r: ('Define the volt.', 'One joule of energy transferred per coulomb of charge.', 'J C⁻¹ [1]'),
        lambda r: ('Explain why the fuse should have a rating just above the normal current.', 'It melts and breaks the circuit if the current rises above normal, protecting the cable from overheating.', 'melts if current too high [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t122.add('C4', (2, 3, 4, 5), 'multi_step')(_pd_c4)

N123 = 'Resistance and resistivity R = ρL/A'
t123 = topic(N123, N123.lower(), 'resistivity', 'resistance')
RHO = [('copper', 1.7e-8), ('aluminium', 2.8e-8), ('nichrome', 1.1e-6), ('constantan', 4.9e-7), ('tungsten', 5.6e-8), ('manganin', 4.4e-7)]
FX(t123, 'C1', (1, 2), [
    ('What is the unit of resistivity?', 'Ω m', 'ρ = RA/L: Ω × m²/m.', ['Ω m⁻¹', 'Ω', 'Ω m²']),
    ('A wire is stretched to twice its length with its volume unchanged. Its resistance', 'is multiplied by 4', 'L × 2 and A ÷ 2, so R = ρL/A × 4.', ['doubles', 'halves', 'is unchanged']),
    ('Two wires of the same material and length: X has twice the diameter of Y. The ratio R_X/R_Y is', '0.25', 'A ∝ d², so R ∝ 1/d².', ['0.5', '2', '4']),
    ('Which is the definition of resistance?', 'The ratio of the potential difference across a component to the current in it', 'R = V/I.', ['The product of p.d. and current', 'The current per unit p.d.', 'The energy per unit charge']),
    ("Ohm's law applies to a conductor if", 'the current is proportional to the p.d. at constant temperature', 'Ohmic conductor: V ∝ I at constant temperature.', ['its resistance increases with current', 'it is a filament lamp', 'its resistance is very small']),
    ('The resistance of a metal wire increases with temperature because', 'the lattice ions vibrate more, increasing collisions with free electrons', 'Greater vibration impedes electron flow.', ['the number of free electrons decreases', 'the wire becomes shorter', 'the electrons gain charge']),
    ('State the equation linking resistance, resistivity, length and cross-sectional area.', 'R = ρL/A', 'R = ρL/A [1]'),
])
FX(t123, 'C2', (1, 2, 3, 4), [
    ('Explain the difference between resistance and resistivity.', 'Resistance depends on the material and the dimensions of the sample; resistivity is a property of the material only (R = ρL/A), at a given temperature.', 'resistance depends on dimensions [1]; resistivity only on material (and temperature) [1] [2]'),
    ('Describe an experiment to determine the resistivity of a metal wire.', 'Measure the diameter with a micrometer at several points; measure R (V/I with ammeter and voltmeter) for several lengths L; plot R against L; ρ = gradient × A.', 'micrometer for d [1]; R for several lengths [1]; graph R vs L [1]; ρ = gradient × A [1] [4]'),
    ('Explain why the resistance of a thermistor (NTC) decreases as its temperature increases.', 'More charge carriers are released as temperature rises, increasing n; this outweighs the increased lattice vibration, so resistance falls.', 'more charge carriers released [1]; outweighs lattice vibration [1] [2]'),
])


@t123.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t123_res(r, D):
    mat, rho = r.choice(RHO)
    L = r.choice([0.50, 1.00, 1.50, 2.00, 5.00, 10.0]); dmm = r.choice([0.20, 0.25, 0.32, 0.40, 0.56, 0.80, 1.0])
    A = math.pi * (dmm * 1e-3) ** 2 / 4; R = rho * L / A
    s = f'A {mat} wire (resistivity {sci(rho, 2)} Ω m) has length {nf(L)} m and diameter {nf(dmm)} mm.'
    if D <= 2:
        return numq(r, D, f'A {mat} wire (resistivity {sci(rho, 2)} Ω m) has length {nf(L)} m and cross-sectional area {sci(A, 3)} m².', 'resistance of the wire', R, ' Ω', f'R = ρL/A = {sci(rho, 2)} × {nf(L)}/{sci(A, 3)}', [rho * A / L * 1e12, R * 4, R / 2], fm=f3)
    if D == 3:
        return Q(s + ' Calculate its resistance.', f'{f3(R)} Ω', f'A = πd²/4 = {sci(A, 3)} m² [1]; R = ρL/A [1]; = {f3(R)} Ω [1] [3]')
    Rt = r.choice([2.0, 5.0, 10.0, 20.0])
    Ln = Rt * A / rho
    return Q(s + f' (a) Calculate its resistance. (b) Calculate the length of the same wire needed to make a {nf(Rt)} Ω resistor. (c) The wire is replaced by one of the same material with twice the diameter and the same length. State the new resistance.',
             f'(a) {f3(R)} Ω (b) {f3(Ln)} m (c) {f3(R / 4)} Ω', f'(a) A = {sci(A, 3)} m² [1]; R = {f3(R)} Ω [1] (b) L = RA/ρ = {f3(Ln)} m [1] (c) A × 4 [1]; R ÷ 4 = {f3(R / 4)} Ω [1] [5]', 'multi_step')


@t123.add('C3', (2, 3, 4, 5), 'case')
def t123_graph(r, D):
    mat, rho = r.choice(RHO[2:])
    dmm = r.choice([0.25, 0.32, 0.38, 0.46]); A = math.pi * (dmm * 1e-3) ** 2 / 4
    Ls = [0.20, 0.40, 0.60, 0.80, 1.00]; c = r.choice([0.0, 0.1, 0.2])
    Rs = [rho * L / A + c for L in Ls]
    rows = '; '.join(f'L = {L:.2f} m, R = {nf(R_, 3)} Ω' for L, R_ in zip(Ls, Rs))
    grad = (Rs[-1] - Rs[0]) / (Ls[-1] - Ls[0])
    return Q(f'A student measures the resistance R of different lengths L of a wire of diameter {nf(dmm)} mm: {rows}. (a) Determine the gradient of a graph of R against L. (b) Calculate the resistivity of the metal. (c) Suggest why the graph ' + ('passes through the origin.' if c == 0 else 'has a small positive intercept.'),
             f'(a) {f3(grad)} Ω m⁻¹ (b) {sci(grad * A, 3)} Ω m (c) ' + ('there is no extra resistance in the connections.' if c == 0 else 'the resistance of the contacts/connecting leads adds a constant to every reading.'),
             f'(a) gradient from first and last points = {f3(grad)} Ω m⁻¹ [1] (b) A = {sci(A, 3)} m² [1]; ρ = gradient × A = {sci(grad * A, 3)} Ω m [1] (c) explanation [1] [4]')


def _rho_c4(r, D):
    mat, rho = r.choice(RHO[2:])
    L = r.choice([0.80, 1.00]); dmm = r.choice([0.30, 0.40]); A = math.pi * (dmm * 1e-3) ** 2 / 4; R = rho * L / A
    intro = r.choice([f'{person(r)} is asked to determine the resistivity of {mat} using a wire of length {nf(L)} m and diameter about {nf(dmm)} mm.', f'In {lab(r)}, a {nf(L)} m length of {mat} wire of diameter {nf(dmm)} mm is used to find the resistivity of the alloy.'])
    parts = [
        lambda r: ('Calculate the cross-sectional area of the wire.', f'{sci(A, 3)} m²', 'πd²/4 [1]'),
        lambda r: (f'With a p.d. of {nf(R * 0.5, 3)} V the current is 0.50 A. Calculate the resistivity.', f'{sci(rho, 3)} Ω m', 'R = V/I then ρ = RA/L [3]'),
        lambda r: ('State the instrument used to measure the diameter and explain why several readings are taken.', 'Micrometer screw gauge; the wire may not be uniform, and d is squared so its uncertainty matters.', 'micrometer [1]; non-uniform / averaging [1] [2]'),
        lambda r: ('Explain why the current should be kept small.', 'A large current heats the wire, increasing its resistance (and resistivity).', 'heating [1]; resistance changes [1] [2]'),
        lambda r: ('Distinguish between resistance and resistivity.', 'Resistance depends on dimensions; resistivity is a property of the material.', 'distinction [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t123.add('C4', (2, 3, 4, 5), 'multi_step')(_rho_c4)

N124 = 'I-V characteristics of resistors, filament lamps, diodes, thermistors and LDRs'
t124 = topic(N124, N124.lower(), 'i-v characteristics', 'filament lamps diodes')
FX(t124, 'C1', (1, 2), [
    ('What is the shape of the I-V characteristic of a metallic conductor at constant temperature?', 'A straight line through the origin', 'Ohmic: I ∝ V.', ['A curve that flattens at high voltage', 'Zero current until about 0.6 V, then rising steeply', 'A horizontal line']),
    ('Why does the I-V graph of a filament lamp curve?', 'The resistance increases as the filament gets hotter', 'Higher temperature → more lattice vibration → higher R; gradient of I-V falls.', ['The resistance decreases as it gets hotter', 'The filament obeys Ohm\'s law', 'The lamp only conducts in one direction']),
    ('A semiconductor diode in forward bias conducts significantly only when the p.d. exceeds about', '0.6 V', 'Silicon diode threshold ~0.6–0.7 V.', ['0.06 V', '6 V', '60 V']),
    ('In reverse bias, the current through an ideal diode is', 'zero', 'Very high resistance in reverse bias.', ['very large', 'the same as in forward bias', 'proportional to the p.d.']),
    ('The resistance of a light-dependent resistor (LDR)', 'decreases as light intensity increases', 'More light releases more charge carriers.', ['increases as light intensity increases', 'does not depend on light', 'increases with temperature only']),
    ('The resistance of an NTC thermistor', 'decreases as temperature increases', 'NTC: negative temperature coefficient.', ['increases as temperature increases', 'is constant', 'depends only on light intensity']),
    ('State what is meant by an ohmic conductor.', 'A conductor for which the current is directly proportional to the p.d. (at constant temperature).', 'I ∝ V at constant temperature [1]'),
])
FX(t124, 'C2', (1, 2, 3, 4), [
    ('Sketch and explain the I-V characteristic of a filament lamp for both positive and negative p.d.', 'An S-shaped curve through the origin, symmetrical about the origin; the gradient decreases at larger |V| because the filament heats up and its resistance increases.', 'S-shape through origin, symmetrical [1]; gradient decreases [1]; resistance increases with temperature [1] [3]'),
    ('Explain why a diode is used in a mains adapter circuit.', 'A diode allows current in one direction only (low resistance forward, very high reverse), so it converts alternating current to direct current (rectification).', 'conducts one direction only [1]; rectification of a.c. [1] [2]'),
    ('Explain why it is incorrect to say the resistance of a filament lamp is the gradient of its I-V graph.', 'Resistance at a point is V/I (the ratio of coordinates), not the gradient (which gives ΔI/ΔV); for a non-linear graph these differ.', 'R = V/I at that point [1]; gradient is not resistance for curve [1] [2]'),
    ('Describe the I-V characteristic of a silicon diode.', 'Almost zero current in reverse bias and in forward bias below about 0.6 V; above this the current rises very steeply with p.d.', 'zero in reverse [1]; steep rise above ~0.6 V forward [1] [2]'),
])


@t124.add('C3', (1, 2, 3, 4), 'numerical')
def t124_lamp(r, D):
    V1 = r.choice([1.0, 2.0, 3.0]); I1 = r.choice([0.10, 0.15, 0.20]); V2 = r.choice([6.0, 9.0, 12.0]); I2 = I1 * r.choice([2.0, 2.4, 2.8])
    R1 = V1 / I1; R2 = V2 / I2
    if D <= 2:
        return numq(r, D, f'For a filament lamp, the current is {nf(I2)} A when the p.d. is {nf(V2)} V.', 'resistance of the lamp at this p.d.', R2, ' Ω', f'R = V/I = {nf(V2)}/{nf(I2)}', [I2 / V2, V2 * I2, (V2 - V1) / (I2 - I1)], fm=f3)
    return Q(f'A filament lamp carries {nf(I1)} A at {nf(V1)} V and {nf(I2, 3)} A at {nf(V2)} V. Calculate its resistance at each p.d. and explain the difference.', f'{f3(R1)} Ω and {f3(R2)} Ω; resistance increases because the filament is hotter at the higher p.d.',
             f'R = V/I: {f3(R1)} Ω [1]; {f3(R2)} Ω [1]; higher temperature, more lattice vibration [1]' + (' [3]' if D == 3 else '; comment that the gradient of the I-V graph is not R [1] [4]'))


@t124.add('C2', (2, 3, 4), 'explain')
def t124_id(r, D):
    comp = r.choice([('a fixed resistor', 'straight line through the origin with constant gradient (constant resistance)'), ('a filament lamp', 'curve through the origin with decreasing gradient at higher |V|, symmetrical'),
                     ('a semiconductor diode', 'zero current in reverse bias and up to about 0.6 V forward, then a steep rise'), ('an NTC thermistor whose temperature rises as current increases', 'curve through the origin with increasing gradient (resistance falls as it warms)')])
    return Q(f'Describe the shape of the I-V characteristic of {comp[0]} and explain what it shows about the resistance.', cap(comp[1]) + '.', 'correct shape [1]; correct link to resistance [1]; explanation of cause [1] [3]')


@t124.add('C3', (2, 3, 4, 5), 'numerical')
def t124_diode(r, D):
    Vs = r.choice([3.0, 4.5, 5.0, 6.0, 9.0]); Vd = 0.70; I = r.choice([10, 15, 20, 25]) * 1e-3
    R = (Vs - Vd) / I
    return Q(f'A silicon diode is connected in forward bias in series with a resistor and a {nf(Vs)} V supply of negligible internal resistance. The p.d. across the diode is {nf(Vd)} V when the current is {nf(I * 1000)} mA. Calculate the resistance of the resistor and of the diode at this current. State what happens if the diode is reversed.',
             f'resistor {f3(R)} Ω; diode {f3(Vd / I)} Ω; reversed: almost no current flows.', f'p.d. across resistor {nf(Vs - Vd)} V [1]; R = {f3(R)} Ω [1]; diode R = V/I = {f3(Vd / I)} Ω [1]; reverse: no current [1] [4]')


def _iv_c4(r, D):
    intro = r.choice([f'{person(r)} investigates the I-V characteristics of a fixed resistor, a filament lamp and a diode in {lab(r)}.', 'A student is given three unlabelled components and asked to identify them from their I-V characteristics.'])
    parts = [
        lambda r: ('Draw a circuit diagram suitable for obtaining I-V data, including a way of reversing the p.d.', 'Supply with variable resistor or potential divider, ammeter in series, voltmeter in parallel with component; reverse connections for negative values.', 'ammeter series, voltmeter parallel [1]; variable supply/potential divider [1] [2]'),
        lambda r: ('Describe how the graph identifies the filament lamp.', 'Curve through origin with decreasing gradient, symmetrical for negative p.d.', 'shape [1]; symmetrical [1] [2]'),
        lambda r: ('Describe how the graph identifies the diode.', 'No current in reverse; current only above ~0.6 V forward.', 'zero current in reverse bias [1]; conducts only above about 0.6 V forward [1] [2]'),
        lambda r: ('Explain why the resistance of the lamp increases with p.d.', 'Higher current heats the filament; increased lattice vibrations impede electrons.', 'temperature rises [1]; lattice vibrations [1] [2]'),
        lambda r: ('Explain why a potential divider is better than a series variable resistor for this experiment.', 'It allows the p.d. to be varied from zero.', 'starts from zero [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t124.add('C4', (2, 3, 4, 5), 'multi_step')(_iv_c4)

CHAPTERS[12] = [t121, t122, t123, t124]

# ===================================================================== 13 D.C. circuits
N131 = 'Electromotive force and internal resistance'
t131 = topic(N131, N131.lower(), 'electromotive force', 'internal resistance')
FX(t131, 'C1', (1, 2), [
    ('Which is the definition of electromotive force?', 'Energy transferred from other forms to electrical energy per unit charge', 'e.m.f. = W/Q for a source.', ['Force on a unit charge', 'Energy transferred per unit time', 'Energy transferred from electrical to other forms per unit charge']),
    ('A cell of e.m.f. 1.5 V and internal resistance 0.50 Ω is connected to a 2.5 Ω resistor. What is the current?', '0.50 A', 'I = E/(R + r) = 1.5/3.0.', ['0.60 A', '3.0 A', '0.75 A']),
    ('The terminal p.d. of a cell is less than its e.m.f. when it delivers a current because', 'energy is transferred to thermal energy in its internal resistance', 'Lost volts = Ir.', ['the e.m.f. decreases instantly', 'charge is lost inside the cell', 'the external resistance is zero']),
    ('A battery of e.m.f. 12 V gives a terminal p.d. of 11 V when the current is 2.0 A. What is its internal resistance?', '0.50 Ω', 'r = (E − V)/I = 1.0/2.0.', ['5.5 Ω', '2.0 Ω', '6.0 Ω']),
    ('When a cell is short-circuited, the current is limited by', 'its internal resistance', 'I = E/r with R = 0.', ['the external resistance', 'the ammeter only', 'nothing; it is infinite']),
    ('State the equation linking e.m.f., terminal p.d., current and internal resistance.', 'E = V + Ir', 'E = V + Ir [1]'),
])
FX(t131, 'C2', (1, 2, 3, 4), [
    ('Explain why the headlights of a car dim when the starter motor is operated.', 'The starter motor draws a very large current; the lost volts Ir across the battery\'s internal resistance increase, so the terminal p.d. across the headlights falls.', 'large current [1]; larger Ir so terminal p.d. falls [1] [2]'),
    ('Explain why a high-voltage power supply is designed with a very large internal resistance.', 'If the terminals are short-circuited (e.g. by a person), the large internal resistance limits the current to a safe value.', 'limits current on short circuit [1]; safety [1] [2]'),
    ('Describe how to determine the e.m.f. and internal resistance of a cell using a graph.', 'Measure terminal p.d. V and current I for several external resistances; plot V against I; e.m.f. = y-intercept; internal resistance = −gradient.', 'measure V and I for varying R [1]; V vs I graph [1]; E = intercept, r = −gradient [1] [3]'),
    ('Explain why a voltmeter connected directly across a cell reads very nearly its e.m.f.', 'A voltmeter has a very high resistance so the current is almost zero; the lost volts Ir are negligible.', 'very small current [1]; Ir negligible [1] [2]'),
])


@t131.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t131_emf(r, D):
    E_ = r.choice([1.5, 3.0, 4.5, 6.0, 9.0, 12.0]); ri = r.choice([0.20, 0.50, 0.80, 1.0, 1.5, 2.0]); R = r.choice([2.0, 3.0, 4.0, 5.0, 8.0, 10.0])
    I = E_ / (R + ri); V = I * R
    src = r.choice(['A cell', 'A battery', 'A solar cell module', 'A power pack'])
    s = f'{src} of e.m.f. {nf(E_)} V and internal resistance {nf(ri)} Ω is connected to a {nf(R)} Ω resistor.'
    if D <= 2:
        k = r.choice(['I', 'V'])
        if k == 'I':
            return numq(r, D, s, 'current in the circuit', I, ' A', f'I = E/(R + r) = {nf(E_)}/({nf(R)} + {nf(ri)})', [E_ / R, E_ / ri, E_ * (R + ri) / 10], fm=f3)
        return numq(r, D, s, 'terminal p.d.', V, ' V', f'I = {f3(I)} A; V = IR', [E_, I * ri, E_ - V / 2], fm=f3)
    if D == 3:
        return Q(s + ' Calculate the current, the terminal p.d. and the power wasted inside the source.', f'{f3(I)} A; {f3(V)} V; {f3(I * I * ri)} W',
                 f'I = E/(R + r) = {f3(I)} A [1]; V = IR = {f3(V)} V [1]; P = I²r = {f3(I * I * ri)} W [1] [3]')
    R2 = r.choice([1.0, 2.0, 0.5]) * ri
    return Q(f'{src} has e.m.f. {nf(E_)} V and internal resistance {nf(ri)} Ω. (a) Calculate the terminal p.d. when the external resistance is {nf(R)} Ω. (b) Calculate the power delivered to an external resistance of {nf(R2, 3)} Ω. (c) Show that the power delivered is greatest when the external resistance equals {nf(ri)} Ω by comparing values.',
             f'(a) {f3(V)} V (b) {f3((E_ / (R2 + ri)) ** 2 * R2)} W (c) P at R = r: {f3(E_ * E_ / (4 * ri))} W, larger than at R = {nf(R)} Ω ({f3(I * I * R)} W) and at other values.',
             f'(a) I = {f3(I)} A; V = {f3(V)} V [1] (b) I = {f3(E_ / (R2 + ri))} A [1]; P = I²R = {f3((E_ / (R2 + ri)) ** 2 * R2)} W [1] (c) P(R = r) = E²/4r = {f3(E_ * E_ / (4 * ri))} W [1]; comparison with other values [1] [5]', 'multi_step')


@t131.add('C3', (2, 3, 4, 5), 'case')
def t131_graph(r, D):
    E_ = r.choice([1.50, 1.55, 3.00, 4.50, 6.00]); ri = r.choice([0.40, 0.60, 0.80, 1.20, 2.00])
    Is = [0.20, 0.40, 0.60, 0.80, 1.00] if E_ / ri > 1.4 else [0.10, 0.20, 0.30, 0.40, 0.50]
    Vs = [E_ - I * ri for I in Is]
    rows = '; '.join(f'I = {I:.2f} A, V = {v_:.2f} V' for I, v_ in zip(Is, Vs))
    return Q(f'A student measures the terminal p.d. V of a battery for different currents I: {rows}. Use a graph of V against I (or the data) to determine the e.m.f. and the internal resistance.' + (' Explain why the e.m.f. is the intercept.' if D >= 4 else ''),
             f'E = {nf(E_, 3)} V; r = {nf(ri, 3)} Ω' + ('; when I = 0 there are no lost volts, so V = E.' if D >= 4 else ''),
             f'V = E − Ir, straight line [1]; gradient = −{nf(ri, 3)} Ω so r = {nf(ri, 3)} Ω [1]; intercept E = {nf(E_, 3)} V [1]' + (' [3]' if D < 4 else '; I = 0 means no lost volts [1] [4]'))


def _emf_c4(r, D):
    E_ = r.choice([6.0, 9.0, 12.0]); ri = r.choice([0.5, 1.0, 1.5]); R = r.choice([4.0, 5.0, 8.0])
    I = E_ / (R + ri)
    intro = r.choice([f'A battery of e.m.f. {nf(E_)} V and internal resistance {nf(ri)} Ω powers a {nf(R)} Ω heater in a camping lamp bought in {city(r)}.', f'A {nf(E_)} V battery with internal resistance {nf(ri)} Ω is connected to a {nf(R)} Ω resistor.'])
    parts = [
        lambda r: ('Define e.m.f.', 'Energy transferred from other forms to electrical energy per unit charge passing through the source.', 'definition [1]'),
        lambda r: ('Calculate the current.', f'{f3(I)} A', 'I = E/(R + r) [2]'),
        lambda r: ('Calculate the terminal p.d.', f'{f3(I * R)} V', 'V = E − Ir [1]'),
        lambda r: ('Calculate the efficiency of energy transfer to the external resistor.', f'{nf(100 * R / (R + ri), 3)}%', 'R/(R + r) [2]'),
        lambda r: ('Explain why the battery becomes warm.', 'Energy is transferred to thermal energy in the internal resistance (I²r).', 'I²r heating [1]'),
        lambda r: ('Calculate the maximum current the battery could supply.', f'{f3(E_ / ri)} A', 'short circuit E/r [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t131.add('C4', (2, 3, 4, 5), 'multi_step')(_emf_c4)

N132 = "Kirchhoff's first and second laws and combining resistors"
t132 = topic(N132, N132.lower(), "kirchhoff's laws", 'combining resistors')
FX(t132, 'C1', (1, 2), [
    ("Kirchhoff's first law is a consequence of the conservation of", 'charge', 'Sum of currents into a junction = sum out.', ['energy', 'momentum', 'mass']),
    ("Kirchhoff's second law is a consequence of the conservation of", 'energy', 'Sum of e.m.f.s = sum of p.d.s round a loop.', ['charge', 'momentum', 'current']),
    ('Resistors of 6.0 Ω and 3.0 Ω are connected in parallel. What is the combined resistance?', '2.0 Ω', '1/R = 1/6 + 1/3 = 1/2.', ['9.0 Ω', '4.5 Ω', '0.50 Ω']),
    ('Three 12 Ω resistors are connected in parallel. What is the combined resistance?', '4.0 Ω', '12/3.', ['36 Ω', '12 Ω', '0.25 Ω']),
    ('Currents of 2.0 A and 3.5 A enter a junction. One wire carries 1.5 A out. What is the current in the only other wire?', '4.0 A out of the junction', '2.0 + 3.5 = 1.5 + I.', ['7.0 A out of the junction', '4.0 A into the junction', '0 A']),
    ('A 4.0 Ω resistor is in series with a parallel pair of 4.0 Ω resistors. What is the total resistance?', '6.0 Ω', '4.0 + 2.0.', ['12 Ω', '1.3 Ω', '8.0 Ω']),
    ("State Kirchhoff's second law.", 'In any closed loop, the sum of the e.m.f.s equals the sum of the p.d.s.', 'sum e.m.f. = sum p.d. round a loop [1]'),
])
FX(t132, 'C2', (1, 2, 3, 4), [
    ('Derive the formula for the combined resistance of two resistors in series using Kirchhoff\'s laws.', 'Same current I in each (first law); V = V₁ + V₂ (second law) so IR = IR₁ + IR₂, giving R = R₁ + R₂.', 'same current [1]; p.d.s add, divide by I [1] [2]'),
    ('Derive the formula for the combined resistance of two resistors in parallel using Kirchhoff\'s laws.', 'Same p.d. V across each; I = I₁ + I₂ (first law), so V/R = V/R₁ + V/R₂, giving 1/R = 1/R₁ + 1/R₂.', 'same p.d. [1]; currents add, divide by V [1] [2]'),
    ('Explain why the combined resistance of resistors in parallel is less than the smallest resistance.', 'Adding another path increases the total current for the same p.d., so the total resistance decreases below that of any single branch.', 'extra path, more current [1]; R = V/I smaller [1] [2]'),
    ("Explain how Kirchhoff's first law follows from conservation of charge.", 'Charge cannot build up at a junction, so the charge flowing in per second equals the charge flowing out per second.', 'no accumulation [1]; rate in = rate out [1] [2]'),
])


@t132.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t132_comb(r, D):
    R1 = r.choice([2.0, 3.0, 4.0, 5.0, 6.0, 10.0]); R2 = r.choice([3.0, 4.0, 6.0, 12.0, 15.0, 20.0]); R3 = r.choice([4.0, 6.0, 8.0, 12.0])
    Rp = R2 * R3 / (R2 + R3); Rt = R1 + Rp
    V = r.choice([6.0, 9.0, 12.0, 24.0])
    s = f'A {nf(R1)} Ω resistor is connected in series with a parallel combination of {nf(R2)} Ω and {nf(R3)} Ω resistors.'
    if D <= 2:
        return numq(r, D, s, 'total resistance', Rt, ' Ω', f'R = {nf(R1)} + ({nf(R2)} × {nf(R3)})/({nf(R2)} + {nf(R3)})', [R1 + R2 + R3, Rp, R1 * (R2 + R3) / (R1 + R2 + R3)], fm=f3)
    I = V / Rt; Vp = I * Rp; I2 = Vp / R2; I3 = Vp / R3
    if D == 3:
        return Q(s + f' The combination is connected to a {nf(V)} V supply of negligible internal resistance. Calculate the current from the supply and the p.d. across the parallel section.', f'I = {f3(I)} A; V = {f3(Vp)} V',
                 f'R_total = {f3(Rt)} Ω [1]; I = V/R = {f3(I)} A [1]; V_parallel = I × {f3(Rp)} = {f3(Vp)} V [1] [3]')
    return Q(s + f' It is connected to a {nf(V)} V supply of negligible internal resistance. (a) Calculate the total resistance. (b) Calculate the current in each resistor. (c) Show that your currents obey Kirchhoff\'s first law and that the p.d.s obey the second law.',
             f'(a) {f3(Rt)} Ω (b) {nf(R1)} Ω: {f3(I)} A; {nf(R2)} Ω: {f3(I2)} A; {nf(R3)} Ω: {f3(I3)} A (c) {f3(I2)} + {f3(I3)} = {f3(I)} A; {f3(I * R1)} + {f3(Vp)} = {nf(V)} V',
             f'(a) parallel {f3(Rp)} Ω [1]; total {f3(Rt)} Ω [1] (b) I = {f3(I)} A [1]; branch currents {f3(I2)} A and {f3(I3)} A [1] (c) both laws checked [1] [5]', 'multi_step')


@t132.add('C3', (3, 4, 5), 'multi_step')
def t132_two(r, D):
    E1 = r.choice([6.0, 9.0, 12.0]); E2 = r.choice([3.0, 4.5, 6.0]); R1 = r.choice([2.0, 4.0, 6.0]); R2 = r.choice([2.0, 3.0, 6.0]); R3 = r.choice([4.0, 6.0, 12.0])
    # two sources each with series resistor feeding common R3; node voltage V
    V = (E1 / R1 + E2 / R2) / (1 / R1 + 1 / R2 + 1 / R3)
    I1 = (E1 - V) / R1; I2 = (E2 - V) / R2; I3 = V / R3
    return Q(f'Cell A (e.m.f. {nf(E1)} V) in series with a {nf(R1)} Ω resistor and cell B (e.m.f. {nf(E2)} V) in series with a {nf(R2)} Ω resistor are connected in parallel, positive terminals joined, across a {nf(R3)} Ω load. The cells have negligible internal resistance. Use Kirchhoff\'s laws to determine the current in the load and in each cell.',
             f'load {f3(I3)} A; cell A {f3(I1)} A; cell B {f3(I2)} A' + (' (negative: B is being charged)' if I2 < 0 else ''),
             f'first law: I₁ + I₂ = I₃ [1]; loop A: {nf(E1)} = {nf(R1)}I₁ + {nf(R3)}I₃ [1]; loop B: {nf(E2)} = {nf(R2)}I₂ + {nf(R3)}I₃ [1]; solving: I₃ = {f3(I3)} A, I₁ = {f3(I1)} A, I₂ = {f3(I2)} A [1] [4]')


@t132.add('C2', (2, 3, 4), 'explain')
def t132_err(r, D):
    a = r.choice([4.0, 6.0, 10.0, 12.0]); b = r.choice([3.0, 5.0, 12.0, 15.0])
    who = person(r)
    return Q(f'{who} calculates the combined resistance of {nf(a)} Ω and {nf(b)} Ω in parallel as 1/{nf(a)} + 1/{nf(b)} = {nf(1 / a + 1 / b, 3)} Ω. Identify the error, give the correct value, and explain how {who} could have checked the answer.',
             f'{who} found 1/R and did not invert it: R = 1/{nf(1 / a + 1 / b, 3)} = {f3(a * b / (a + b))} Ω. Check: the combined resistance must be less than the smaller resistor ({nf(min(a, b))} Ω).',
             'failed to take reciprocal [1]; correct value [1]; check: less than smallest resistor [1] [3]')


def _kir_c4(r, D):
    E_ = r.choice([9.0, 12.0]); R1 = r.choice([4.0, 6.0]); R2 = r.choice([6.0, 12.0]); R3 = r.choice([4.0, 12.0])
    Rp = R2 * R3 / (R2 + R3); I = E_ / (R1 + Rp)
    intro = r.choice([f'A {nf(E_)} V battery of negligible internal resistance is connected to a {nf(R1)} Ω resistor in series with a parallel combination of {nf(R2)} Ω and {nf(R3)} Ω resistors in a circuit board built in {city(r)}.', f'In a test circuit, a {nf(E_)} V supply (negligible internal resistance) drives current through {nf(R1)} Ω in series with {nf(R2)} Ω parallel to {nf(R3)} Ω.'])
    parts = [
        lambda r: ("State Kirchhoff's first law.", 'The sum of currents into a junction equals the sum of currents out.', 'statement [1]'),
        lambda r: ('Calculate the total resistance.', f'{f3(R1 + Rp)} Ω', 'parallel then series [2]'),
        lambda r: ('Calculate the current from the battery.', f'{f3(I)} A', 'I = E/R [1]'),
        lambda r: (f'Calculate the current in the {nf(R2)} Ω resistor.', f'{f3(I * Rp / R2)} A', 'p.d. across parallel ÷ R [2]'),
        lambda r: ('Calculate the power dissipated in the whole circuit.', f'{f3(E_ * I)} W', 'P = EI [1]'),
        lambda r: (f'The {nf(R3)} Ω resistor is removed. State and explain the effect on the current from the battery.', 'It decreases, because the total resistance increases.', 'decreases [1]; total R increases [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t132.add('C4', (2, 3, 4, 5), 'multi_step')(_kir_c4)

N133 = 'Potential dividers, potentiometers and sensors'
t133 = topic(N133, N133.lower(), 'potential dividers', 'potentiometers')
FX(t133, 'C1', (1, 2), [
    ('A 12 V supply is connected across resistors of 2.0 kΩ and 4.0 kΩ in series. What is the p.d. across the 4.0 kΩ resistor?', '8.0 V', 'V_out = 12 × 4.0/6.0.', ['4.0 V', '6.0 V', '12 V']),
    ('In a potential divider containing a thermistor and a fixed resistor, the temperature rises. The p.d. across the fixed resistor', 'increases', 'NTC resistance falls, so the fixed resistor takes a larger share of the p.d.', ['decreases', 'stays the same', 'becomes zero']),
    ('A potentiometer is balanced when', 'the galvanometer reads zero', 'At balance no current flows through the galvanometer.', ['the galvanometer reads its maximum', 'the driver cell is disconnected', 'the wire is fully used']),
    ('An advantage of using a potentiometer to compare e.m.f.s is that', 'no current is drawn from the cell being tested at balance', 'So there are no lost volts in its internal resistance.', ['it needs no driver cell', 'it works with a.c. only', 'it measures current directly']),
    ('An LDR and a fixed resistor form a potential divider. The light level falls. The p.d. across the LDR', 'increases', 'LDR resistance rises in the dark, taking a larger share.', ['decreases', 'stays the same', 'falls to zero']),
    ('State the potential divider equation.', 'V_out = V_in × R₂/(R₁ + R₂)', 'V_out = V_in R₂/(R₁ + R₂) [1]'),
])
FX(t133, 'C2', (1, 2, 3, 4), [
    ('Explain how a potential divider containing an LDR can be used to switch on a street lamp when it gets dark.', 'In the dark the LDR resistance increases, so the p.d. across it rises; if the output is taken across the LDR, this larger p.d. triggers the switching circuit to turn on the lamp.', 'LDR resistance rises in dark [1]; larger share of p.d. across LDR [1]; output across LDR triggers switch [1] [3]'),
    ('Explain why a potentiometer measures the e.m.f. of a cell more accurately than a voltmeter.', 'At balance no current flows from the cell, so there are no lost volts across its internal resistance; a voltmeter draws a small current and reads slightly less than the e.m.f.', 'no current at balance [1]; voltmeter draws current / lost volts [1] [2]'),
    ('Explain why connecting a voltmeter of low resistance across the output of a potential divider changes the output p.d.', 'The voltmeter in parallel with the output resistor reduces the combined resistance of that section, so it takes a smaller share of the supply p.d.', 'parallel combination lower resistance [1]; output p.d. decreases [1] [2]'),
])


@t133.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t133_div(r, D):
    Vin = r.choice([5.0, 6.0, 9.0, 12.0]); R1 = r.choice([1.0, 2.2, 3.3, 4.7, 10]) * 1e3; R2 = r.choice([1.0, 2.0, 4.7, 6.8, 10, 15]) * 1e3
    Vout = Vin * R2 / (R1 + R2)
    s = f'A potential divider consists of a {nf(R1 / 1000)} kΩ resistor and a {nf(R2 / 1000)} kΩ resistor in series across a {nf(Vin)} V supply of negligible internal resistance.'
    if D <= 2:
        return numq(r, D, s, f'p.d. across the {nf(R2 / 1000)} kΩ resistor', Vout, ' V', f'V_out = {nf(Vin)} × {nf(R2 / 1000)}/({nf(R1 / 1000)} + {nf(R2 / 1000)})', [Vin * R1 / (R1 + R2), Vin * R2 / R1 if R2 < R1 else Vin / 2 + 0.3, Vin / 2], fm=f3)
    Rv = r.choice([10, 20, 47]) * 1e3
    Rp = R2 * Rv / (R2 + Rv); Vl = Vin * Rp / (R1 + Rp)
    return Q(s + f' A voltmeter of resistance {nf(Rv / 1000)} kΩ is connected across the {nf(R2 / 1000)} kΩ resistor. Calculate the expected output p.d. without the voltmeter and the reading on the voltmeter. Explain the difference.',
             f'{f3(Vout)} V; {f3(Vl)} V; the voltmeter in parallel lowers the resistance of that section, so it takes a smaller share of the p.d.',
             f'V_out = {f3(Vout)} V [1]; parallel resistance = {f3(Rp / 1000)} kΩ [1]; reading = {f3(Vl)} V [1]' + (' [3]' if D == 3 else '; explanation [1] [4]'))


@t133.add('C3', (2, 3, 4, 5), 'numerical')
def t133_sensor(r, D):
    Vin = r.choice([5.0, 6.0, 9.0, 12.0]); Rf = r.choice([1.0, 2.2, 4.7, 10]) * 1e3
    kind = r.choice([('thermistor', 'at 20 °C', 'at 60 °C', r.choice([5.0, 8.0, 12.0]) * 1e3, r.choice([0.8, 1.2, 1.5]) * 1e3), ('LDR', 'in daylight', 'in darkness', r.choice([0.5, 0.8, 1.0]) * 1e3, r.choice([50, 80, 100]) * 1e3)])
    nm, c1, c2, Ra, Rb = kind
    Va = Vin * Rf / (Rf + Ra); Vb = Vin * Rf / (Rf + Rb)
    return Q(f'A {nm} is connected in series with a {nf(Rf / 1000)} kΩ fixed resistor across a {nf(Vin)} V supply. The resistance of the {nm} is {nf(Ra / 1000)} kΩ {c1} and {nf(Rb / 1000)} kΩ {c2}. Calculate the p.d. across the fixed resistor in each condition and describe how the circuit could act as a sensor.',
             f'{c1}: {f3(Va)} V; {c2}: {f3(Vb)} V. The output across the fixed resistor changes with {"temperature" if nm == "thermistor" else "light level"}, so it can trigger a switch or be calibrated as a sensor.',
             f'{c1}: {f3(Va)} V [1]; {c2}: {f3(Vb)} V [1]; output changes with condition, used to trigger/calibrate [1]' + (' [3]' if D <= 3 else '; correct direction of change explained via resistance share [1] [4]'))


@t133.add('C3', (2, 3, 4, 5), 'numerical')
def t133_pot(r, D):
    Ed = r.choice([2.0, 3.0, 4.0]); L = 1.00; E1 = r.choice([1.0, 1.08, 1.5]); E2 = r.choice([1.2, 1.35, 1.02])
    if E1 >= Ed or E2 >= Ed:
        return None
    l1 = L * E1 / Ed; l2 = L * E2 / Ed
    return Q(f'A potentiometer wire of length 1.000 m has a driver cell that gives a uniform p.d. of {nf(Ed)} V across it. A standard cell of e.m.f. {nf(E1, 3)} V balances at {nf(l1 * 100, 3)} cm. A test cell balances at {nf(l2 * 100, 3)} cm. Calculate the e.m.f. of the test cell and explain why the balance length gives the e.m.f. and not the terminal p.d.',
             f'{f3(E2)} V; at balance no current flows through the test cell, so there are no lost volts.', f'E ∝ balance length [1]; E = {nf(E1, 3)} × {nf(l2 * 100, 3)}/{nf(l1 * 100, 3)} = {f3(E2)} V [1]; no current at balance [1] [3]')


def _div_c4(r, D):
    Vin = r.choice([6.0, 9.0]); Rf = r.choice([2.2, 4.7]) * 1e3; Rc = r.choice([10, 15]) * 1e3; Rh = r.choice([1.0, 1.5]) * 1e3
    intro = r.choice([f'A temperature alarm for a greenhouse in {city(r)} uses a thermistor in series with a {nf(Rf / 1000)} kΩ resistor across a {nf(Vin)} V supply. The thermistor resistance is {nf(Rc / 1000)} kΩ when cold and {nf(Rh / 1000)} kΩ when hot.', f'A fire alarm uses a {nf(Vin)} V supply to drive a thermistor (resistance {nf(Rc / 1000)} kΩ cold, {nf(Rh / 1000)} kΩ hot) in series with a {nf(Rf / 1000)} kΩ fixed resistor; the alarm sounds when the p.d. across the fixed resistor is large.'])
    parts = [
        lambda r: ('Calculate the p.d. across the fixed resistor when cold.', f'{f3(Vin * Rf / (Rf + Rc))} V', 'potential divider equation [2]'),
        lambda r: ('Calculate the p.d. across the fixed resistor when hot.', f'{f3(Vin * Rf / (Rf + Rh))} V', 'potential divider equation [2]'),
        lambda r: ('Explain why the output across the fixed resistor rises as temperature increases.', 'Thermistor resistance falls, so the fixed resistor takes a larger share of the supply p.d.', 'R_thermistor falls [1]; larger share [1] [2]'),
        lambda r: ('Suggest a change so that the alarm triggers at a different temperature.', 'Replace the fixed resistor with a variable resistor and adjust it.', 'variable resistor [1]'),
        lambda r: ('Explain why the resistance of an NTC thermistor falls with temperature.', 'More charge carriers become free as temperature increases.', 'more charge carriers [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t133.add('C4', (2, 3, 4, 5), 'multi_step')(_div_c4)

CHAPTERS[13] = [t131, t132, t133]


# ===================================================================== 14 Particle physics
N141 = 'Atoms, nuclei and the α-particle scattering experiment'
t141 = topic(N141, N141.lower(), 'α-particle scattering', 'atoms nuclei')
FX(t141, 'C1', (1, 2), [
    ('In the α-particle scattering experiment, most α-particles passed straight through the gold foil. This showed that', 'most of the atom is empty space', 'Very few α-particles came close to a nucleus.', ['the nucleus is positive', 'electrons are very light', 'the atom is solid throughout']),
    ('A very small fraction of α-particles were deflected through more than 90°. This showed that', 'the positive charge and most of the mass are concentrated in a tiny nucleus', 'Large deflections need a small, massive, positive centre.', ['electrons orbit in shells', 'the foil was very thin', 'α-particles are negatively charged']),
    ('What is the approximate diameter of a nucleus?', '10⁻¹⁴ m', 'Nuclei: 10⁻¹⁵–10⁻¹⁴ m; atoms ~10⁻¹⁰ m.', ['10⁻¹⁰ m', '10⁻⁸ m', '10⁻¹⁹ m']),
    ('Why was a very thin gold foil used in the scattering experiment?', 'So that each α-particle was scattered by at most one nucleus', 'Thin foil avoids multiple scattering and absorption.', ['So that gold atoms could be seen', 'Because gold is a poor conductor', 'To make the α-particles faster']),
    ('Why was the α-particle scattering apparatus evacuated?', 'So that the α-particles were not absorbed or scattered by air', 'α-particles have a range of only a few cm in air.', ['To keep the gold foil cold', 'To increase the charge of the nucleus', 'To slow the α-particles down']),
    ('The ratio of the diameter of an atom to that of its nucleus is about', '10⁴ to 10⁵', '10⁻¹⁰ m / 10⁻¹⁵–10⁻¹⁴ m.', ['10', '10²', '10¹⁰']),
    ('State the conclusion from the α-particle scattering experiment about the charge of the nucleus.', 'The nucleus is positively charged (it repels the positive α-particles).', 'positive [1]'),
])
FX(t141, 'C2', (1, 2, 3, 4), [
    ('Describe the observations of the α-particle scattering experiment and state the conclusion drawn from each.', 'Most passed straight through: atom mostly empty space. Some deflected through small angles: a positive charge concentrated in the atom. A very few deflected through > 90°: a tiny, dense, positive nucleus containing most of the mass.', 'most undeflected → empty space [1]; small deflections → positive charge [1]; large deflections → small massive nucleus [1] [3]'),
    ('Explain why an α-particle approaching a nucleus head-on is deflected back along its path.', 'The α-particle and nucleus are both positive; the electrostatic repulsion increases as it approaches, doing work against its kinetic energy until it stops and is pushed back.', 'electrostatic repulsion [1]; KE converted, stops and returns [1] [2]'),
    ('Explain why α-particle scattering is not affected significantly by the electrons in the gold atoms.', 'Electrons have a very small mass compared with an α-particle (and small charge), so they cannot deflect it significantly.', 'electron mass very small [1]; little deflection [1] [2]'),
    ('Describe the nuclear model of the atom.', 'A tiny, positively charged nucleus containing protons and neutrons (most of the mass) surrounded by negatively charged electrons at relatively large distances; mostly empty space.', 'small positive nucleus with most mass [1]; electrons outside, mostly empty space [1] [2]'),
])


@t141.add('C3', (1, 2, 3, 4), 'numerical')
def t141_scale(r, D):
    el = r.choice([('gold', 1.5e-10, 1.4e-14), ('hydrogen', 1.1e-10, 1.7e-15), ('carbon', 1.4e-10, 5.4e-15), ('uranium', 3.5e-10, 1.5e-14), ('iron', 2.5e-10, 9.6e-15)])
    nm, da, dn = el
    ratio = da / dn
    if D <= 2:
        return numq(r, D, f'An atom of {nm} has a diameter of about {sci(da, 2)} m and its nucleus has a diameter of about {sci(dn, 2)} m.', 'ratio of atomic diameter to nuclear diameter', ratio, '', f'{sci(da, 2)}/{sci(dn, 2)}', [ratio ** 0.5, ratio * 100, ratio / 100], fm=lambda x: sci(x, 2))
    m = r.choice([0.5, 1.0, 2.0])
    return Q(f'An atom of {nm} has a diameter of about {sci(da, 2)} m and its nucleus about {sci(dn, 2)} m. In a scale model the nucleus is a marble {nf(m)} cm across. Calculate the diameter of the model atom in metres and use it to explain why most α-particles pass straight through a thin foil.',
             f'{f3(m * ratio / 100)} m; the nucleus occupies a tiny fraction of the atom so most α-particles do not pass near one.',
             f'ratio = {sci(ratio, 2)} [1]; model diameter = {f3(m * ratio / 100)} m [1]; mostly empty space explanation [1]' + (' [3]' if D == 3 else '; volume fraction ≈ (1/ratio)³ comment [1] [4]'))


@t141.add('C2', (2, 3, 4), 'explain')
def t141_path(r, D):
    case = r.choice([('passes far from any nucleus', 'It travels straight through with negligible deflection because the repulsive force is negligible at large distances.'),
                     ('passes close to a nucleus', 'It is deflected through a small or moderate angle by the electrostatic repulsion, following a curved (hyperbolic) path.'),
                     ('approaches a nucleus almost head-on', 'It slows as kinetic energy becomes electric potential energy, stops at its closest approach and is repelled back through a large angle (> 90°).')])
    sp = r.choice(['high-energy', 'low-energy'])
    return Q(f'An α-particle in a scattering experiment {case[0]}. Describe and explain its path. Suggest how the path would differ for a {"higher" if sp == "high-energy" else "lower"}-energy α-particle on the same initial line.',
             case[1] + (' A higher-energy α-particle would be deflected less.' if sp == 'high-energy' else ' A lower-energy α-particle would be deflected more.'),
             'path described [1]; explained by electrostatic repulsion [1]; effect of energy [1] [3]')


def _alpha_c4(r, D):
    intro = r.choice([f'In 1909 Geiger and Marsden fired α-particles at a thin gold foil in a vacuum and counted scattered particles at different angles. A student in {city(r)} is studying their results.', 'The α-particle scattering experiment provided evidence for the nuclear model of the atom.'])
    parts = [
        lambda r: ('State the observation that shows the atom is mostly empty space.', 'Most α-particles passed straight through undeflected.', 'observation [1]'),
        lambda r: ('State the observation that shows that the nucleus contains most of the mass and is very small.', 'A very small number were deflected through angles greater than 90°.', 'observation [1]'),
        lambda r: ('Explain why the experiment is carried out in a vacuum.', 'α-particles would be absorbed/scattered by air molecules.', 'absorption by air [1]'),
        lambda r: ('Explain why the foil must be very thin.', 'So each α-particle is scattered by only one nucleus.', 'single scattering [1]'),
        lambda r: ('Sketch the paths of three α-particles passing at different distances from a nucleus.', 'distant: almost straight; nearer: small deflection; head-on: reflected back', 'distant path almost undeviated [1]; closer paths deflected more, head-on reflected back [1] [2]'),
        lambda r: ('Describe the structure of the atom suggested by these results.', 'Small, dense, positive nucleus with electrons around it; mostly empty space.', 'nucleus [1]; electrons/empty space [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t141.add('C4', (2, 3, 4, 5), 'multi_step')(_alpha_c4)

N142 = 'Nucleons, isotopes and nuclear decay equations including β⁺ and the neutrino'
t142 = topic(N142, N142.lower(), 'isotopes', 'nuclear decay equations')
NUC = [('U', 92, 238), ('Ra', 88, 226), ('Po', 84, 210), ('Th', 90, 232), ('Am', 95, 241), ('Rn', 86, 222), ('Pu', 94, 239)]
BETAM = [('C', 6, 14, 'N'), ('Sr', 38, 90, 'Y'), ('Co', 27, 60, 'Ni'), ('I', 53, 131, 'Xe'), ('Cs', 55, 137, 'Ba'), ('H', 1, 3, 'He'), ('P', 15, 32, 'S')]
BETAP = [('F', 9, 18, 'O'), ('Na', 11, 22, 'Ne'), ('C', 6, 11, 'B'), ('N', 7, 13, 'C'), ('O', 8, 15, 'N'), ('K', 19, 40, 'Ar')]
ELS = {92: 'U', 90: 'Th', 88: 'Ra', 86: 'Rn', 84: 'Po', 82: 'Pb', 93: 'Np', 95: 'Am', 94: 'Pu', 91: 'Pa', 89: 'Ac', 87: 'Fr', 85: 'At', 83: 'Bi'}
FX(t142, 'C1', (1, 2), [
    ('A nucleus of ²³⁵₉₂U contains', '92 protons and 143 neutrons', 'Neutrons = 235 − 92.', ['92 protons and 235 neutrons', '143 protons and 92 neutrons', '235 protons and 92 neutrons']),
    ('Isotopes of an element have', 'the same number of protons but different numbers of neutrons', 'Same proton number, different nucleon number.', ['the same number of neutrons but different numbers of protons', 'the same nucleon number', 'different numbers of electrons in the neutral atom']),
    ('In β⁻ decay, which particles are emitted?', 'An electron and an electron antineutrino', 'n → p + e⁻ + ν̄ₑ.', ['A positron and an electron neutrino', 'An electron and an electron neutrino', 'A helium nucleus']),
    ('In β⁺ decay, which particles are emitted?', 'A positron and an electron neutrino', 'p → n + e⁺ + νₑ.', ['An electron and an electron antineutrino', 'A positron and an electron antineutrino', 'A neutron and a proton']),
    ('In α decay, the nucleon number of the nucleus', 'decreases by 4', 'An α-particle is ⁴₂He.', ['decreases by 2', 'increases by 4', 'stays the same']),
    ('Why was the neutrino proposed to explain β decay?', 'The β-particles have a continuous range of kinetic energies', 'A third particle shares the energy released.', ['β-particles all have the same energy', 'β-particles are positive', 'The nucleus gains mass']),
    ('γ-radiation is emitted when', 'a nucleus in an excited state loses energy', 'γ-emission changes neither A nor Z.', ['a proton becomes a neutron', 'an electron leaves an atom', 'a nucleus splits in two']),
    ('State what is meant by the nucleon number.', 'The total number of protons and neutrons in the nucleus.', 'protons + neutrons [1]'),
])
FX(t142, 'C2', (1, 2, 3, 4), [
    ('Explain why the β-particles from a radioactive source have a continuous range of energies, while α-particles from one nuclide have a single energy.', 'In β decay the energy released is shared between the β-particle and a (anti)neutrino in varying proportions; in α decay only two bodies share the energy, so each α has the same energy.', 'energy shared with (anti)neutrino [1]; two-body α decay gives fixed energy [1] [2]'),
    ('Explain why isotopes of an element have the same chemical properties.', 'They have the same number of protons and so the same number of electrons in the neutral atom; chemical behaviour depends on the electrons.', 'same number of electrons [1]; chemistry depends on electrons [1] [2]'),
    ('Compare the charge, mass and penetrating power of α, β⁻ and γ radiation.', 'α: +2e, 4u, stopped by paper; β⁻: −e, ~1/2000 u, stopped by a few mm of aluminium; γ: no charge or mass, reduced by thick lead.', 'charges [1]; masses [1]; penetration [1] [3]'),
    ('Explain why γ-emission does not change the nucleon number or proton number of a nucleus.', 'A γ-ray photon has no charge and no mass; it carries away only energy from an excited nucleus.', 'no charge and no mass [1]; only energy lost [1] [2]'),
])


SUBT = str.maketrans('-+0123456789', '₋₊₀₁₂₃₄₅₆₇₈₉')


def nuc(A, Z, X):
    """Nuclide notation with nucleon number as superscript and proton number as subscript, e.g. ¹⁴₆C."""
    return f'{sup(A)}{str(Z).translate(SUBT)}{X}'


EMI = '⁰₋₁e'
POS = '⁰₊₁e'
ALP = '⁴₂α'


def _nucsym(A, Z, X):
    return f'{sup(A)}{X}' + f' (Z = {Z})'


@t142.add('C1', (1, 2, 3))
def t142_count(r, D):
    X, Z, A = r.choice(NUC + [(b[0], b[1], b[2]) for b in BETAM])
    N = A - Z
    c = f'{Z} protons and {N} neutrons'
    opts, a = mcq(r, c, [f'{N} protons and {Z} neutrons', f'{Z} protons and {A} neutrons', f'{A} protons and {Z} neutrons', f'{Z} protons and {A + Z} neutrons'])
    if D >= 3:
        return Q(f'A nucleus is represented by the nucleon number {A} and proton number {Z} ({X}). State the number of protons, neutrons and electrons in a neutral atom of this nuclide.', f'{Z} protons, {N} neutrons, {Z} electrons', f'protons and neutrons [1]; electrons = {Z} [1] [2]', 'short')
    return Q(f'What does a nucleus of {nuc(A, Z, X)} contain?', a, f'neutrons = A − Z = {A} − {Z} = {N}.', opts=opts)


@t142.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t142_eq(r, D):
    kind = r.choice(['alpha', 'bm', 'bp'])
    if kind == 'alpha':
        X, Z, A = r.choice(NUC)
        Y = ELS.get(Z - 2, 'Y')
        eq = f'{nuc(A, Z, X)} → {nuc(A - 4, Z - 2, Y)} + {ALP}'
        dA, dZ = A - 4, Z - 2
        what = 'α-decay'
    elif kind == 'bm':
        X, Z, A, Y = r.choice(BETAM)
        eq = f'{nuc(A, Z, X)} → {nuc(A, Z + 1, Y)} + {EMI} + ν̄ₑ'
        dA, dZ = A, Z + 1
        what = 'β⁻ decay'
    else:
        X, Z, A, Y = r.choice(BETAP)
        eq = f'{nuc(A, Z, X)} → {nuc(A, Z - 1, Y)} + {POS} + νₑ'
        dA, dZ = A, Z - 1
        what = 'β⁺ decay'
    s = f'A nucleus of {nuc(A, Z, X)} (nucleon number {A}, proton number {Z}) undergoes {what}.'
    if D <= 2:
        c = f'nucleon number {dA}, proton number {dZ}'
        opts, a = mcq(r, c, [f'nucleon number {dA}, proton number {Z}', f'nucleon number {A - 4 if dA == A else A}, proton number {dZ}', f'nucleon number {dA}, proton number {2 * Z - dZ}', f'nucleon number {A + 4}, proton number {Z + 2}'])
        return Q(s + ' What are the nucleon number and proton number of the daughter nucleus?', a, f'{eq}; nucleon and proton numbers balance.', opts=opts)
    if D == 3:
        return Q(s + ' Write the nuclear equation, showing nucleon and proton numbers, and state the particles emitted.', eq, f'daughter nuclide correct [1]; emitted particle(s) with nucleon and proton numbers [1]; ' + ('(anti)neutrino included [1] [3]' if kind != 'alpha' else 'A and Z balance shown [1] [3]'))
    return Q(s + ' (a) Write the nuclear equation. (b) Show that nucleon number and charge are conserved. (c) ' + ('Explain why a neutrino must also be emitted.' if kind != 'alpha' else 'State why the α-particles from this nuclide all have the same kinetic energy.'),
             f'(a) {eq} (b) nucleon numbers: {A} = {dA} + {A - dA}; proton numbers (charge): {Z} = {dZ} + ({Z - dZ}) (c) ' + ('the β-particles have a range of energies, so a third particle (neutrino) carries the remainder; it also conserves lepton number.' if kind != 'alpha' else 'only two products share the energy, so each has a fixed share.'),
             f'(a) equation [2] (b) A conserved [1]; Z/charge conserved [1] (c) explanation [1] [5]', 'multi_step')


@t142.add('C3', (3, 4, 5), 'multi_step')
def t142_chain(r, D):
    X, Z, A = r.choice(NUC)
    na = r.choice([1, 2, 3]); nb = r.choice([1, 2])
    A2 = A - 4 * na; Z2 = Z - 2 * na + nb
    Y = ELS.get(Z2, 'X')
    return Q(f'A nucleus of {nuc(A, Z, X)} decays by a series of {na} α-decay{"s" if na > 1 else ""} and {nb} β⁻ decay{"s" if nb > 1 else ""}. Determine the nucleon number and proton number of the final nucleus, and its number of neutrons.',
             f'A = {A2}, Z = {Z2} ({Y}); {A2 - Z2} neutrons', f'each α: A − 4, Z − 2 [1]; each β⁻: Z + 1 [1]; A = {A2}, Z = {Z2} [1]; N = {A2 - Z2} [1] [4]')


def _decay_c4(r, D):
    X, Z, A, Y = r.choice(BETAP)
    intro = r.choice([f'The isotope {nuc(A, Z, X)} is used in medical imaging at a hospital in {city(r)}. It decays by β⁺ emission.', f'A nucleus of {nuc(A, Z, X)} is a β⁺ emitter used in a research laboratory.'])
    parts = [
        lambda r: ('State the numbers of protons and neutrons in the nucleus.', f'{Z} protons, {A - Z} neutrons', 'both [1]'),
        lambda r: ('Write the decay equation.', f'{nuc(A, Z, X)} → {nuc(A, Z - 1, Y)} + {POS} + νₑ', 'daughter [1]; positron and neutrino [1] [2]'),
        lambda r: ('State what is meant by isotopes, using this element as an example.', f'Nuclei with the same proton number ({Z}) but different nucleon numbers.', 'definition [1]'),
        lambda r: ('State the antiparticle of the positron and how it differs.', 'The electron: same mass, opposite charge.', 'electron [1]; same mass opposite charge [1] [2]'),
        lambda r: ('Explain why the positrons emitted have a range of kinetic energies.', 'The energy released is shared with the neutrino in varying proportions.', 'shared with neutrino [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t142.add('C4', (2, 3, 4, 5), 'multi_step')(_decay_c4)

N143 = 'Fundamental particles: quarks, antiparticles, hadrons and leptons'
t143 = topic(N143, N143.lower(), 'quarks', 'hadrons and leptons')
HADRONS = [('proton', 'uud', '+e', 'baryon'), ('neutron', 'udd', '0', 'baryon'), ('π⁺ meson', 'ud̄', '+e', 'meson'), ('π⁻ meson', 'ūd', '−e', 'meson'), ('K⁺ meson', 'us̄', '+e', 'meson'),
           ('K⁰ meson', 'ds̄', '0', 'meson'), ('antiproton', 'ūūd̄', '−e', 'antibaryon'), ('Σ⁺ baryon', 'uus', '+e', 'baryon'), ('Λ⁰ baryon', 'uds', '0', 'baryon')]
FX(t143, 'C1', (1, 2), [
    ('What is the quark composition of a proton?', 'uud', 'Charge: +⅔ + ⅔ − ⅓ = +1.', ['udd', 'uuu', 'ud̄']),
    ('What is the quark composition of a neutron?', 'udd', 'Charge: +⅔ − ⅓ − ⅓ = 0.', ['uud', 'ddd', 'us̄']),
    ('What is the charge of an up quark?', '+⅔e', 'u: +⅔e; d and s: −⅓e.', ['−⅓e', '+⅓e', '+e']),
    ('Which particle is a lepton?', 'electron neutrino', 'Leptons: electron, muon, tau and their neutrinos.', ['proton', 'neutron', 'pion']),
    ('A meson consists of', 'a quark and an antiquark', 'Mesons: qq̄; baryons: qqq.', ['three quarks', 'three antiquarks', 'two leptons']),
    ('Which statement about an antiparticle is correct?', 'It has the same mass as its particle but opposite charge', 'Antiparticles have equal mass and opposite charge (and other quantum numbers).', ['It has opposite mass and the same charge', 'It always has zero charge', 'It is always heavier than its particle']),
    ('Hadrons are particles that', 'are made of quarks and feel the strong force', 'Baryons and mesons are hadrons.', ['are fundamental and do not feel the strong force', 'have zero mass', 'are always leptons']),
    ('State the charge of a strange quark.', '−⅓e', '−⅓e [1]'),
])
FX(t143, 'C2', (1, 2, 3, 4), [
    ('Explain why a proton is not a fundamental particle but an electron is.', 'A proton is made of three quarks (uud), so it has internal structure; an electron (a lepton) is not made of smaller particles.', 'proton made of quarks [1]; electron is fundamental lepton [1] [2]'),
    ('Distinguish between hadrons and leptons.', 'Hadrons are made of quarks and experience the strong force (baryons and mesons); leptons are fundamental and do not experience the strong force (e.g. electron, neutrino).', 'hadrons: quarks, strong force [1]; leptons: fundamental, no strong force [1] [2]'),
    ('Distinguish between a baryon and a meson.', 'A baryon is made of three quarks (e.g. proton uud); a meson is made of a quark and an antiquark (e.g. π⁺ = ud̄).', 'baryon three quarks with example [1]; meson quark-antiquark with example [1] [2]'),
    ('State the four fundamental interactions and the particles on which the strong interaction acts.', 'Gravitational, electromagnetic, weak and strong; the strong force acts between hadrons (quarks) only.', 'four forces [1]; strong acts on hadrons/quarks only [1] [2]'),
])


def _qtoks(qs):
    """Split a quark string such as 'ud̄' into tokens (NFD, antiquarks keep the combining macron)."""
    qs = unicodedata.normalize('NFD', qs)
    out, i = [], 0
    while i < len(qs):
        if i + 1 < len(qs) and qs[i + 1] == '\u0304':
            out.append(qs[i:i + 2]); i += 2
        else:
            out.append(qs[i]); i += 1
    return out


QCH = {'u': 2, 'd': -1, 's': -1, 'c': 2, 't': 2, 'b': -1}


def _qcharge(tok):
    return -QCH[tok[0]] if len(tok) > 1 else QCH[tok]


CHS = {3: '+e', 0: '0', -3: '−e', 6: '+2e', -6: '−2e'}


def _thirds(v):
    return ('+' if v > 0 else '−') + f'{abs(v)}/3'


@t143.add('C1', (1, 2, 3))
def t143_charge(r, D):
    nm, qs, ch, kind = r.choice(HADRONS)
    toks = _qtoks(qs)
    tot = sum(_qcharge(t) for t in toks)
    c = CHS.get(tot, f'{tot}/3 e')
    opts, a = mcq(r, c, [x for x in ['+e', '0', '−e', '+2e', '−2e'] if x != c])
    work = ' + '.join(f'({_thirds(_qcharge(t))})' for t in toks)
    if D >= 3:
        return Q(f'A {nm} has quark composition {qs}. Calculate its charge and state whether it is a baryon, an antibaryon or a meson.', f'{c}; {kind}', f'{work} = {c} [1]; {kind} ({len(toks)} quarks/antiquarks) [1] [2]', 'short')
    return Q(f'A particle has quark composition {qs}. What is its charge?', a, f'{work} = {c}: the {nm}.', opts=opts)


@t143.add('C2', (2, 3, 4), 'explain')
def t143_class(r, D):
    p = r.choice([('electron', 'lepton', 'fundamental; does not feel the strong force'), ('muon', 'lepton', 'fundamental; does not feel the strong force'), ('electron neutrino', 'lepton', 'fundamental, nearly massless, neutral; weak interaction only'),
                  ('proton', 'hadron (baryon)', 'made of three quarks uud; feels the strong force'), ('neutron', 'hadron (baryon)', 'made of three quarks udd; feels the strong force'),
                  ('π⁺ meson', 'hadron (meson)', 'quark-antiquark pair ud̄; feels the strong force'), ('positron', 'lepton (antiparticle)', 'antiparticle of the electron: same mass, charge +e'), ('antiproton', 'hadron (antibaryon)', 'made of ūūd̄; same mass as proton, charge −e')])
    return Q(f'Classify the {p[0]} as a hadron or a lepton and justify your answer by describing its structure. State whether it experiences the strong interaction.', f'{cap(p[1])}: {p[2]}.', 'correct class [1]; structure [1]; strong force statement [1] [3]')


@t143.add('C3', (2, 3, 4), 'numerical')
def t143_anti(r, D):
    nm, qs, ch, kind = r.choice([h for h in HADRONS if h[0] not in ('antiproton',)])
    toks = [t[0] if len(t) > 1 else t + '\u0304' for t in _qtoks(qs)]
    anti = unicodedata.normalize('NFC', ''.join(toks))
    tot = sum(_qcharge(t) for t in toks)
    c = CHS.get(tot, f'{tot}/3 e')
    return Q(f'The {nm} has quark composition {qs}. State the quark composition and the charge of its antiparticle, and explain how the masses compare.', f'{anti}; charge {c}; same mass as the {nm}',
             f'each quark replaced by its antiquark (and vice versa): {anti} [1]; charge {c} [1]; same mass [1] [3]')


def _quark_c4(r, D):
    intro = r.choice([f'A student at a summer school in {city(r)} is learning about the standard model of particle physics.', 'Particle accelerators produce many hadrons, which can be described by the quark model.'])
    parts = [
        lambda r: ('State the charges of the up, down and strange quarks.', 'u: +⅔e; d: −⅓e; s: −⅓e', 'u = +⅔e [1]; d and s = −⅓e [1] [2]'),
        lambda r: ('Use the quark model to show that the neutron is neutral.', '+⅔ − ⅓ − ⅓ = 0', 'udd [1]; sum zero [1] [2]'),
        lambda r: ('The π⁻ meson has quark composition ūd. Determine its charge.', '−⅔ − ⅓ = −e', 'calculation [1]'),
        lambda r: ('State what is meant by an antiparticle.', 'A particle with the same mass but opposite charge (and other quantum numbers).', 'definition [1]'),
        lambda r: ('Name two leptons.', 'electron and electron neutrino (also muon, tau, their neutrinos)', 'two [1]'),
        lambda r: ('Distinguish between hadrons and leptons in terms of the forces they experience.', 'Hadrons feel the strong force; leptons do not.', 'distinction [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t143.add('C4', (2, 3, 4, 5), 'multi_step')(_quark_c4)

N144 = 'Quark models of β⁻ and β⁺ decay'
t144 = topic(N144, N144.lower(), 'quark models', 'β⁻ and β⁺ decay')
FX(t144, 'C1', (1, 2), [
    ('In β⁻ decay, which quark change occurs?', 'A down quark changes into an up quark', 'n (udd) → p (uud): d → u + e⁻ + ν̄ₑ.', ['An up quark changes into a down quark', 'A down quark changes into a strange quark', 'An up quark changes into a strange quark']),
    ('In β⁺ decay, which quark change occurs?', 'An up quark changes into a down quark', 'p (uud) → n (udd): u → d + e⁺ + νₑ.', ['A down quark changes into an up quark', 'An up quark is destroyed', 'A down quark changes into a strange quark']),
    ('Which interaction is responsible for β decay?', 'the weak interaction', 'Quark flavour changes only occur via the weak interaction.', ['the strong interaction', 'the electromagnetic interaction', 'the gravitational interaction']),
    ('In the quark model of β⁻ decay, d → u + e⁻ + ν̄ₑ. Which quantity confirms that charge is conserved?', '−⅓e = +⅔e − e + 0', 'Charge on each side: −⅓e.', ['−⅓e = +⅔e + e', '+⅔e = −⅓e − e', '0 = +⅔e − ⅓e']),
    ('Which particles are emitted with the up quark when a down quark changes in β⁻ decay?', 'An electron and an electron antineutrino', 'd → u + e⁻ + ν̄ₑ.', ['A positron and an electron neutrino', 'A proton and an electron', 'Two electrons']),
    ('State the quark change in β⁺ decay.', 'u → d + e⁺ + νₑ', 'up to down [1]'),
])
FX(t144, 'C2', (1, 2, 3, 4), [
    ('Use the quark model to describe β⁻ decay of a neutron.', 'A neutron (udd) becomes a proton (uud): one down quark changes to an up quark, emitting an electron and an electron antineutrino via the weak interaction.', 'udd → uud [1]; d → u [1]; e⁻ and ν̄ₑ emitted [1] [3]'),
    ('Use the quark model to describe β⁺ decay of a proton in a nucleus.', 'A proton (uud) becomes a neutron (udd): one up quark changes to a down quark, emitting a positron and an electron neutrino.', 'uud → udd [1]; u → d [1]; e⁺ and νₑ emitted [1] [3]'),
    ('Show that charge is conserved in the quark change u → d + e⁺ + νₑ.', 'Left: +⅔e. Right: −⅓e + (+e) + 0 = +⅔e.', 'left charge [1]; right charge sums to +⅔e [1] [2]'),
    ('Explain why a free proton does not undergo β⁺ decay, although a proton in some nuclei can.', 'A free neutron is more massive than a proton, so p → n + e⁺ + ν needs an energy input; inside a nucleus the change in nuclear binding energy can supply it.', 'neutron heavier, energy needed [1]; nucleus provides energy [1] [2]'),
])


@t144.add('C2', (2, 3, 4), 'explain')
def t144_identify(r, D):
    bm = r.choice([True, False])
    X, Z, A, Y = r.choice(BETAM if bm else BETAP)
    return Q(f'A nucleus of {nuc(A, Z, X)} decays to {nuc(A, Z + 1 if bm else Z - 1, Y)}. Identify the type of decay and describe the change at quark level, naming all the particles emitted.',
             (f'β⁻ decay: a neutron (udd) becomes a proton (uud); d → u + e⁻ + ν̄ₑ.' if bm else f'β⁺ decay: a proton (uud) becomes a neutron (udd); u → d + e⁺ + νₑ.'),
             'type identified from change in Z [1]; quark change [1]; particles emitted [1] [3]')


@t144.add('C3', (1, 2, 3, 4), 'numerical')
def t144_cons(r, D):
    bm = r.choice([True, False])
    if D <= 2:
        c = 'd → u + e⁻ + ν̄ₑ' if bm else 'u → d + e⁺ + νₑ'
        opts, a = mcq(r, c, ['d → u + e⁺ + νₑ', 'u → d + e⁻ + ν̄ₑ', 'd → u + e⁻ + νₑ', 'u → d + e⁺ + ν̄ₑ', 'd → s + e⁻ + ν̄ₑ'])
        return Q(f'Which equation correctly shows the quark change in {"β⁻" if bm else "β⁺"} decay?', a, f'{c}: charge {"−⅓ = +⅔ − 1 + 0" if bm else "+⅔ = −⅓ + 1 + 0"}; lepton number conserved.', opts=opts)
    eq = 'd → u + e⁻ + ν̄ₑ' if bm else 'u → d + e⁺ + νₑ'
    return Q(f'For {"β⁻" if bm else "β⁺"} decay, write the quark-level equation and show that charge is conserved. State the interaction responsible.' + (' Explain why an antineutrino, not a neutrino, is emitted.' if (D >= 4 and bm) else (' Explain why a neutrino, not an antineutrino, is emitted.' if D >= 4 else '')),
             eq + f'; charge: {"−⅓e = +⅔e − e + 0" if bm else "+⅔e = −⅓e + e + 0"}; weak interaction.' + (' Lepton number: the electron (+1) must be balanced by an antilepton (−1).' if (D >= 4 and bm) else (' Lepton number: the positron (−1) must be balanced by a lepton (+1).' if D >= 4 else '')),
             'equation [1]; charge balance [1]; weak interaction [1]' + (' ; lepton number argument [1] [4]' if D >= 4 else ' [3]'))


def _qb_c4(r, D):
    X, Z, A, Y = r.choice(BETAM)
    intro = r.choice([f'The radioactive isotope {nuc(A, Z, X)} decays by β⁻ emission. It is used as a tracer by researchers in {city(r)}.', f'A nucleus of {nuc(A, Z, X)} undergoes β⁻ decay.'])
    parts = [
        lambda r: ('Write the nuclear equation.', f'{nuc(A, Z, X)} → {nuc(A, Z + 1, Y)} + {EMI} + ν̄ₑ', 'daughter [1]; e⁻ and ν̄ₑ [1] [2]'),
        lambda r: ('Describe the change in quark composition of a nucleon.', 'udd → uud: a down quark becomes an up quark.', 'd → u [1]; n → p [1] [2]'),
        lambda r: ('Show that charge is conserved in the quark change.', '−⅓e = +⅔e + (−e) + 0', 'both sides [1]'),
        lambda r: ('Name the interaction responsible.', 'weak interaction', '[1]'),
        lambda r: ('State one property of the antineutrino.', 'neutral / very small mass / rarely interacts', 'property [1]'),
        lambda r: ('Compare this with the quark change in β⁺ decay.', 'β⁺: up quark → down quark, emitting e⁺ and νₑ.', 'u → d [1]; positron and neutrino [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t144.add('C4', (2, 3, 4, 5), 'multi_step')(_qb_c4)

CHAPTERS[14] = [t141, t142, t143, t144]

# ===================================================================== 15 Practical skills (AS)
INSTR = [('the diameter of a wire', 'a micrometer screw gauge', '0.01 mm', ['a metre rule', 'a vernier caliper reading to 0.1 mm', 'a 30 cm ruler']),
         ('the length of a pendulum (about 80 cm)', 'a metre rule', '1 mm', ['a micrometer screw gauge', 'a vernier caliper', 'a measuring tape reading to 1 cm']),
         ('the internal diameter of a beaker', 'vernier calipers', '0.1 mm', ['a micrometer screw gauge', 'a metre rule', 'a protractor']),
         ('the time for 20 oscillations of a pendulum', 'a stopwatch reading to 0.01 s', '0.01 s (but reaction time dominates)', ['a clock with a seconds hand', 'a light gate with no timer', 'a metronome']),
         ('the angle through which a ray is refracted', 'a protractor', '1°', ['a micrometer', 'a set square', 'a ruler']),
         ('the current through a thermistor', 'a digital milliammeter', '0.1 mA', ['a voltmeter', 'a galvanometer with no scale', 'a 10 A analogue ammeter']),
         ('the mass of a small coin', 'a top-pan balance reading to 0.01 g', '0.01 g', ['a newton meter reading to 0.1 N', 'a kitchen scale reading to 10 g', 'a spring balance reading to 10 g']),
         ('the thickness of a sheet of card', 'a micrometer screw gauge', '0.01 mm', ['a metre rule', 'a measuring tape', 'a protractor'])]

N151 = 'Manipulation, measurement and observation: using instruments and recording data'
t151 = topic(N151, N151.lower(), 'manipulation, measurement and observation', 'using instruments')
FX(t151, 'C1', (1, 2), [
    ('A micrometer screw gauge reads 0.03 mm with the jaws closed. A wire then gives a reading of 0.52 mm. What is the diameter of the wire?', '0.49 mm', 'Subtract the zero error: 0.52 − 0.03.', ['0.55 mm', '0.52 mm', '0.46 mm']),
    ('Readings of a length are 54.2 cm, 54.6 cm and 54.4 cm. Which is the best way to record the result?', '54.4 ± 0.2 cm', 'Mean 54.4 cm; uncertainty = half the range = 0.2 cm.', ['54.4 ± 0.4 cm', '54.40 ± 0.02 cm', '54 ± 1 cm']),
    ('What is the resolution of a typical metre rule?', '1 mm', 'Smallest scale division.', ['0.1 mm', '1 cm', '0.01 mm']),
    ('How should a column heading for time in seconds be written in a results table?', 't / s', 'Quantity / unit (solidus notation).', ['t (seconds)', 's / t', 'time s']),
    ('A student times 20 oscillations three times: 24.6 s, 24.9 s, 24.3 s. What is the period?', '1.23 s', 'Mean = 24.6 s; T = 24.6/20.', ['24.6 s', '0.81 s', '1.2 s']),
    ('Why should a student look perpendicularly at a scale when taking a reading?', 'To avoid parallax error', 'Viewing at an angle displaces the apparent reading.', ['To reduce random error from the instrument', 'To avoid zero error', 'To increase the resolution']),
    ('State how the uncertainty in a quantity is estimated from repeated readings.', 'Half the range of the readings (if larger than the instrument resolution).', 'half the range [1]'),
])
FX(t151, 'C2', (1, 2, 3, 4), [
    ('Explain why the number of significant figures in a calculated quantity should match those of the raw data.', 'The precision of a result cannot be greater than the precision of the measurements used; quote it to the same (or one more) significant figures as the least precise data.', 'precision limited by data [1]; same s.f. as least precise data [1] [2]'),
    ('Explain why all the raw readings in a column should be recorded to the same number of decimal places.', 'They are taken with the same instrument and so have the same precision; consistent decimal places show the resolution of that instrument.', 'same instrument, same precision [1]; d.p. shows resolution [1] [2]'),
    ('Describe how to measure the diameter of a wire accurately.', 'Check the micrometer for zero error; close the jaws on the wire using the ratchet; take readings at several points along the wire and in different orientations; average and correct for zero error.', 'zero error checked [1]; ratchet [1]; several positions and orientations, averaged [1] [3]'),
    ('Explain why a light gate and an electronic timer are often better than a stopwatch.', 'They remove human reaction time, which is a large and variable source of error in short time intervals.', 'removes reaction time [1]; significant for short times [1] [2]'),
])


@t151.add('C1', (1, 2, 3))
def t151_instr(r, D):
    what, ins, res, wrong = r.choice(INSTR)
    opts, a = mcq(r, ins, wrong)
    if D >= 3:
        return Q(f'Suggest the most suitable instrument for measuring {what}, and state its resolution.', f'{cap(ins)}; resolution {res}.', f'instrument [1]; resolution [1] [2]', 'short')
    return Q(f'Which instrument is most suitable for measuring {what}?', a, f'{cap(ins)} (resolution {res}).', opts=opts)


@t151.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t151_repeat(r, D):
    base = r.choice([12.4, 25.6, 34.8, 48.2, 61.5]); n = r.choice([10, 20])
    vals = [round(base + r.choice([-0.4, -0.2, 0, 0.2, 0.3, 0.5]), 1) for _ in range(3)]
    if len(set(vals)) == 1:
        vals[0] = round(vals[0] + 0.2, 1)
    mean = sum(vals) / 3; half = (max(vals) - min(vals)) / 2
    T = mean / n
    s = f'A student times {n} oscillations of a mass on a spring three times: ' + ', '.join(f'{v:.1f} s' for v in vals) + '.'
    if D <= 2:
        return numq(r, D, s, 'period of one oscillation', T, ' s', f'mean = {nf(mean, 4)} s; T = mean/{n}', [mean, T * 2, mean / (n + 1)], fm=lambda x: nf(x, 3))
    pct = 100 * half / mean
    return Q(s + ' Calculate the period and its absolute and percentage uncertainty, taking the uncertainty in the mean time as half the range.', f'T = {nf(T, 3)} s ± {nf(half / n, 1)} s ({nf(pct, 2)}%)',
             f'mean = {nf(mean, 4)} s [1]; half range = {nf(half, 2)} s [1]; T = {nf(T, 3)} s, ΔT = {nf(half / n, 1)} s [1]; percentage {nf(pct, 2)}% (same for T and total time) [1]' + (' [4]' if D <= 4 else '; suggests timing more oscillations to reduce % uncertainty [1] [5]'))


@t151.add('C3', (2, 3, 4), 'numerical')
def t151_read(r, D):
    kind = r.choice(['micrometer', 'vernier'])
    if kind == 'micrometer':
        main = r.choice([0.5, 1.0, 1.5, 2.0, 3.5]); thim = r.choice([12, 18, 23, 31, 44]); z = r.choice([0.02, -0.01, 0.03, 0.00])
        rd = main + thim * 0.01
        return Q(f'A micrometer screw gauge has a zero error of {z:+.2f} mm. When measuring a ball bearing, the main scale shows {main:.1f} mm and the thimble scale shows {thim} divisions (each 0.01 mm). Calculate the corrected diameter and state its uncertainty.',
                 f'{rd - z:.2f} ± 0.01 mm', f'reading = {main:.1f} + {thim} × 0.01 = {rd:.2f} mm [1]; corrected = {rd:.2f} − ({z:+.2f}) = {rd - z:.2f} mm [1]; uncertainty ±0.01 mm [1] [3]')
    main = r.choice([2.3, 3.1, 4.6, 5.8]); v = r.choice([3, 5, 7, 8])
    rd = main + v * 0.01
    return Q(f'Vernier calipers are used to measure the width of a block. The zero of the vernier scale lies just past {main:.1f} cm on the main scale and the {v}th vernier division lines up with a main-scale mark (vernier resolution 0.01 cm). State the reading and its uncertainty.',
             f'{rd:.2f} ± 0.01 cm', f'main scale {main:.1f} cm [1]; + {v} × 0.01 = {rd:.2f} cm [1]; ±0.01 cm [1] [3]')


def _mmo_c4(r, D):
    intro = r.choice([f'In a Paper 3 practical in {city(r)}, a candidate investigates how the period T of a mass on a spring depends on the mass m.', f'{person(r)} investigates how the time for a ball to roll down a ramp depends on the height of the ramp.'])
    spring = 'spring' in intro
    parts = [
        lambda r: ('State the independent and dependent variables.', ('m (independent); T (dependent)' if spring else 'height (independent); time (dependent)'), 'both [1]'),
        lambda r: ('State two variables that should be kept constant.', ('same spring; same amplitude/displacement' if spring else 'same ball; same ramp length/surface'), 'first control variable [1]; second control variable [1] [2]'),
        lambda r: ('Describe how to measure the time accurately.', ('time 20 oscillations with a fiducial marker at the equilibrium position; repeat and average' if spring else 'use light gates or repeat timings with a stopwatch and average'), 'technique [1]; repeats [1] [2]'),
        lambda r: ('Draw the headings for a suitable results table.', ('m / kg | time for 20 oscillations / s (×2) | mean / s | T / s' if spring else 'h / m | t₁ / s | t₂ / s | mean t / s'), 'quantity/unit headings [1]; repeats and derived columns [1] [2]'),
        lambda r: ('State how many sets of readings should be taken and over what range.', 'At least six values spread over the widest possible range.', 'six or more [1]; wide range [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t151.add('C4', (2, 3, 4, 5), 'multi_step')(_mmo_c4)

N152 = 'Presentation of data: tables, graphs, gradients and intercepts'
t152 = topic(N152, N152.lower(), 'presentation of data', 'gradients and intercepts')
LIN = [('T = 2π√(l/g)', 'T²', 'l', '4π²/g', 'zero'), ('h = ½gt²', 'h', 't²', 'g/2', 'zero'), ('V = E − Ir', 'V', 'I', '−r', 'E'),
       ('R = ρL/A', 'R', 'L', 'ρ/A', 'zero'), ('v² = u² + 2as', 'v²', 's', '2a', 'u²'), ('E = ½kx²', 'E', 'x²', 'k/2', 'zero'),
       ('y = ax^n', 'lg y', 'lg x', 'n', 'lg a'), ('I = I₀ cos² θ', 'I', 'cos² θ', 'I₀', 'zero'), ('F = kx', 'F', 'x', 'k', 'zero'), ('f = (1/2L)√(T/μ)', 'f²', 'T', '1/(4L²μ)', 'zero')]
FX(t152, 'C1', (1, 2), [
    ('A graph of T² against l for a simple pendulum is a straight line through the origin. What is the gradient?', '4π²/g', 'T² = (4π²/g) l.', ['g/4π²', '2π/g', '2π√g']),
    ('To test whether y = ax^n, which graph should be plotted?', 'lg y against lg x', 'lg y = n lg x + lg a: gradient n, intercept lg a.', ['y against x', 'y against lg x', 'lg y against x']),
    ('When drawing a line of best fit through plotted points, which is correct?', 'The points should be balanced on either side of the line', 'A line of best fit balances the scatter.', ['The line must pass through the first and last points', 'The line must pass through the origin', 'The line should join each point to the next']),
    ('When calculating the gradient of a best-fit line, the triangle used should', 'be large, covering more than half of the line', 'A large triangle reduces the percentage error in reading values.', ['use two adjacent data points', 'be as small as possible', 'start at the origin in every case']),
    ('A graph of V against I for a cell has gradient −0.80 Ω and y-intercept 1.52 V. What is the e.m.f.?', '1.52 V', 'V = E − Ir: intercept = E.', ['0.80 V', '1.90 V', '0.72 V']),
    ('Plotted points on a graph should occupy', 'more than half of the graph grid in both directions', 'Choose scales so the points fill more than half the grid.', ['exactly one quarter of the grid', 'only the bottom-left corner', 'one column of squares']),
    ('State what is plotted on the x-axis of a graph.', 'The independent variable (or the quantity chosen to give a straight line).', 'independent variable [1]'),
])
FX(t152, 'C2', (1, 2, 3, 4), [
    ('Explain why plotting a straight-line graph is useful in analysing an experiment.', 'A straight line is easy to recognise and fit; the gradient and intercept give the constants in the relationship, and scatter or curvature shows errors or a wrong model.', 'easy to judge linearity [1]; gradient/intercept give constants [1] [2]'),
    ('Explain why a scale such as 3 cm to represent 1 unit is not suitable on a graph.', 'Awkward scales (multiples of 3, 7, etc.) make plotting and reading values difficult and lead to errors; scales of 1, 2 or 5 per division are used.', 'awkward scale causes reading errors [1]; use 1, 2, 5 [1] [2]'),
    ('Describe how to find the uncertainty in the gradient of a straight-line graph.', 'Plot error bars; draw the best-fit line and the worst acceptable straight line through the error bars; uncertainty = |best gradient − worst gradient|.', 'error bars [1]; worst acceptable line [1]; difference of gradients [1] [3]'),
])


@t152.add('C3', (1, 2, 3, 4), 'numerical')
def t152_lin(r, D):
    eq, y, x, grad, icpt = r.choice(LIN)
    if D <= 2:
        c = f'{y} against {x}'
        opts, a = mcq(r, c, [f'{x} against {y}', f'{y} against {x}²' if '²' not in x else f'{y} against √{x}', f'lg {y} against {x}' if 'lg' not in y else f'{y} against {x}'.replace('lg ', ''), f'{y}² against {x}'])
        return Q(f'A student wants to test the relationship {eq} using a straight-line graph. Which graph should be plotted?', a, f'Plot {y} (y-axis) against {x} (x-axis): gradient {grad}, y-intercept {icpt}.', opts=opts)
    return Q(f'A student tests the relationship {eq}. State the quantities to plot on each axis to give a straight line, and give expressions for the gradient and the y-intercept.', f'y-axis {y}, x-axis {x}; gradient = {grad}; intercept = {icpt}',
             f'axes [1]; gradient = {grad} [1]; intercept = {icpt} [1]' + (' [3]' if D == 3 else '; explanation of how the constant is found from gradient or intercept [1] [4]'))


@t152.add('C3', (2, 3, 4, 5), 'case')
def t152_grad(r, D):
    kind = r.choice(['pend', 'spring', 'cell'])
    if kind == 'pend':
        gv = r.choice([9.6, 9.7, 9.8, 9.9]); ls = [0.200, 0.400, 0.600, 0.800, 1.000]
        T2 = [4 * math.pi ** 2 * l / gv for l in ls]
        rows = '; '.join(f'l = {l:.3f} m, T² = {t:.3f} s²' for l, t in zip(ls, T2))
        gr = (T2[-1] - T2[0]) / (ls[-1] - ls[0])
        return Q(f'Results for a simple pendulum: {rows}. A graph of T² against l is plotted. (a) Determine the gradient. (b) Use the gradient to determine g.' + (' (c) Explain why the line should pass through the origin.' if D >= 4 else ''),
                 f'(a) {nf(gr, 3)} s² m⁻¹ (b) g = 4π²/gradient = {nf(4 * math.pi ** 2 / gr, 3)} m s⁻²' + (' (c) T² = (4π²/g)l has no constant term: T = 0 when l = 0.' if D >= 4 else ''),
                 f'(a) gradient from large triangle = {nf(gr, 3)} s² m⁻¹ [1] (b) g = 4π²/gradient [1]; = {nf(4 * math.pi ** 2 / gr, 3)} m s⁻² [1]' + (' (c) no intercept term [1] [4]' if D >= 4 else ' [3]'))
    if kind == 'spring':
        k = r.choice([20, 25, 40, 50]); ms = [0.050, 0.100, 0.150, 0.200, 0.250]
        xs = [m * GR / k * 100 for m in ms]
        rows = '; '.join(f'm = {m:.3f} kg, x = {x:.1f} cm' for m, x in zip(ms, xs))
        gr = (xs[-1] - xs[0]) / (ms[-1] - ms[0])
        return Q(f'A spring is loaded with masses m and the extension x recorded: {rows}. (a) Determine the gradient of a graph of x (in m) against m. (b) Determine the spring constant.' + (' (c) State the unit of the gradient.' if D >= 4 else ''),
                 f'(a) {nf(gr / 100, 3)} m kg⁻¹ (b) k = g/gradient = {nf(k, 3)} N m⁻¹' + (' (c) m kg⁻¹' if D >= 4 else ''),
                 f'(a) gradient = {nf(gr / 100, 3)} m kg⁻¹ [1] (b) x = (g/k)m so k = g/gradient [1]; = {nf(k, 3)} N m⁻¹ [1]' + (' (c) m kg⁻¹ [1] [4]' if D >= 4 else ' [3]'))
    E_ = r.choice([1.50, 3.00, 4.50]); ri = r.choice([0.50, 0.80, 1.20]); Is = [0.20, 0.40, 0.60, 0.80, 1.00]
    Vs = [E_ - I * ri for I in Is]
    rows = '; '.join(f'I = {I:.2f} A, V = {v:.2f} V' for I, v in zip(Is, Vs))
    return Q(f'For a cell, terminal p.d. V and current I are: {rows}. (a) Determine the gradient and y-intercept of a graph of V against I. (b) Hence state the e.m.f. and internal resistance.' + (' (c) Explain why the gradient is negative.' if D >= 4 else ''),
             f'(a) gradient −{nf(ri, 3)} Ω, intercept {nf(E_, 3)} V (b) E = {nf(E_, 3)} V, r = {nf(ri, 3)} Ω' + (' (c) V = E − Ir: lost volts increase with I.' if D >= 4 else ''),
             f'(a) gradient [1]; intercept [1] (b) E and r identified [1]' + (' (c) lost volts Ir [1] [4]' if D >= 4 else ' [3]'))


@t152.add('C2', (2, 3, 4), 'explain')
def t152_table(r, D):
    err = r.choice([('the column heading is written "Length (cm)" and values are 12, 15.5, 18.25 cm', 'Heading should be "length / cm" (quantity / unit) and raw readings should all have the same number of decimal places (e.g. 12.0, 15.5, 18.3 cm, as read with a ruler to 0.1 cm).'),
                    ('the values of 1/T are recorded as 0.8333333 s⁻¹', 'A calculated value should have the same number of significant figures as the raw data (or one more), e.g. 0.833 s⁻¹.'),
                    ('the time column shows only a single reading of each time, with no repeats', 'Repeat readings should be taken (at least twice) and the mean recorded, to reduce random error and identify anomalies.'),
                    ('the student uses only four values of the independent variable over a narrow range', 'At least six values should be taken spread over as wide a range as possible.'),
                    ('the heading "T² s²" is used for a column of squared periods', 'The heading should be "T² / s²" with a solidus separating quantity and unit.')])
    return Q(f'In a Paper 3 results table, {err[0]}. Identify what is wrong and state how it should be corrected.', err[1], 'error identified [1]; correct practice stated [1] [2]')


def _pres_c4(r, D):
    gv = r.choice([9.7, 9.8]); ls = [0.30, 0.50, 0.70, 0.90]
    intro = r.choice([f'A candidate in {city(r)} measures the period T of a pendulum for lengths l of 0.30 m, 0.50 m, 0.70 m and 0.90 m.', 'A student investigates how the period T of a simple pendulum depends on its length l.'])
    T = [round(2 * math.pi * math.sqrt(l / gv), 2) for l in ls]
    parts = [
        lambda r: ('Explain why T² is plotted against l rather than T against l.', 'T = 2π√(l/g) so T² = (4π²/g)l, giving a straight line through the origin.', 'T² ∝ l [1]; straight line [1] [2]'),
        lambda r: (f'For l = 0.90 m, T = {nf(T[3], 3)} s. Calculate T² to an appropriate number of significant figures.', f'{nf(T[3] ** 2, 3)} s²', 'value with 3 s.f. [1]'),
        lambda r: ('State how the gradient is used to find g.', 'g = 4π²/gradient', 'expression [1]'),
        lambda r: ('Describe how to draw the line of best fit and find its gradient.', 'Straight line with points balanced either side; use a triangle covering more than half the line.', 'balanced line [1]; large triangle [1] [2]'),
        lambda r: ('Suggest two further lengths that would improve the data set.', 'e.g. 0.20 m and 1.10 m (extend range; at least six values)', 'two sensible values [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t152.add('C4', (2, 3, 4, 5), 'multi_step')(_pres_c4)

N153 = 'Analysis, conclusions and evaluation including estimating uncertainties'
t153 = topic(N153, N153.lower(), 'analysis, conclusions and evaluation', 'estimating uncertainties')
FX(t153, 'C1', (1, 2), [
    ('A student tests whether T ∝ √m by calculating k = T/√m for two trials and gets 1.25 and 1.31. The percentage uncertainty in k is 3%. What should the student conclude?', 'The relationship is not supported because the values differ by more than 3%', '(1.31 − 1.25)/1.25 ≈ 4.8% > 3%.', ['The relationship is supported because the values are close', 'The relationship is proved', 'No conclusion can be drawn about k']),
    ('Two values of a constant k are 4.82 and 4.96. What is the percentage difference between them?', '2.9%', '(4.96 − 4.82)/4.82 × 100 = 2.9%.', ['0.14%', '14%', '1.4%']),
    ('The uncertainty in a gradient is found from', 'the difference between the gradients of the best-fit line and the worst acceptable line', 'Standard Paper 3/5 method.', ['the uncertainty in the first data point', 'the range of the y-values', 'the gradient multiplied by 10%']),
    ('A length is measured as 25.0 cm with an uncertainty of ±0.5 cm. Its percentage uncertainty is', '2%', '0.5/25.0 × 100.', ['0.5%', '5%', '0.2%']),
    ('A student calculates g = 9.734 m s⁻². The raw data are given to 3 significant figures. How should g be quoted?', '9.73 m s⁻²', 'Same number of s.f. as the data.', ['9.734 m s⁻²', '9.7 m s⁻²', '10 m s⁻²']),
    ('State what the criterion should be based on when judging whether two calculated values of k support a proportional relationship.', 'The percentage uncertainty in the measurements (the values should agree within this).', 'based on % uncertainty in raw data [1]'),
])
FX(t153, 'C2', (1, 2, 3, 4), [
    ('Explain why a student should state a criterion before judging whether two k values agree.', 'Without a criterion based on the experimental uncertainty, the judgement of "close enough" is arbitrary; the values should be compared with the percentage uncertainty in the data.', 'criterion needed for a valid conclusion [1]; based on percentage uncertainty [1] [2]'),
    ('Explain why two readings are insufficient to draw a valid conclusion about a relationship.', 'With only two points any relationship can appear to hold or fail by chance; more readings over a wide range are needed to establish a trend and reduce random error.', 'too few to establish trend [1]; random error/chance [1] [2]'),
    ('Explain how error bars help to judge whether a straight line through the origin is consistent with data.', 'If a straight line through the origin can be drawn passing through all (or most) of the error bars, the data are consistent with proportionality within the uncertainties.', 'line through error bars [1]; consistent within uncertainty [1] [2]'),
])


@t153.add('C3', (1, 2, 3, 4, 5), 'case')
def t153_k(r, D):
    rel = r.choice([('T', 'm', 'T/√m', lambda a, b: a / math.sqrt(b), 's', 'kg'), ('F', 'x', 'F/x', lambda a, b: a / b, 'N', 'm'), ('V', 'I', 'V/I', lambda a, b: a / b, 'V', 'A'), ('h', 't', 'h/t²', lambda a, b: a / b ** 2, 'm', 's')])
    y, x, kexp, fn, uy, ux = rel
    k0 = r.choice([1.2, 2.5, 4.9, 6.4])
    agree = r.choice([True, False])
    x1, x2 = r.choice([(0.20, 0.60), (0.30, 0.80), (0.25, 0.75), (1.0, 3.0)])
    def yof(xx, k):
        if kexp == 'T/√m':
            return k * math.sqrt(xx)
        if kexp == 'h/t²':
            return k * xx * xx
        return k * xx
    y1 = yof(x1, k0); y2 = yof(x2, k0 * (1.02 if agree else 1.12))
    k1 = fn(y1, x1); k2 = fn(y2, x2)
    pdiff = abs(k2 - k1) / k1 * 100
    unc = r.choice([5, 8, 10])
    s = f'A student suggests that {y} is related to {x} by {y} = k{"√" + x if kexp == "T/√m" else (x + "²" if kexp == "h/t²" else x)}, where k is a constant. Two sets of readings are: {x} = {nf(x1, 3)} {ux}, {y} = {nf(y1, 3)} {uy}; and {x} = {nf(x2, 3)} {ux}, {y} = {nf(y2, 3)} {uy}.'
    if D <= 2:
        return numq(r, D, s, 'value of k from the first set of readings', k1, '', f'k = {kexp} = {nf(y1, 3)}/{nf(x1, 3)}' + ('' if kexp == 'F/x' or kexp == 'V/I' else ' (with root or square as needed)'), [y1 * x1, k1 * 2, x1 / y1], fm=lambda v: nf(v, 3))
    sup_ = pdiff <= unc
    return Q(s + f' (a) Calculate two values of k. (b) Justify the number of significant figures you have given. (c) The student estimates the percentage uncertainty in the results as {unc}%. Explain whether the results support the suggested relationship.',
             f'(a) {nf(k1, 3)} and {nf(k2, 3)} (b) 3 s.f., matching the raw data (c) percentage difference {nf(pdiff, 2)}% is {"less" if sup_ else "more"} than {unc}%, so the relationship is {"supported" if sup_ else "not supported"}.',
             f'(a) both k values [1] (b) s.f. same as raw data [1] (c) percentage difference = {nf(pdiff, 2)}% [1]; valid comparison with {unc}% and conclusion [1]' + (' [4]' if D <= 4 else '; comment that only two readings is a limitation [1] [5]'))


@t153.add('C3', (2, 3, 4, 5), 'case')
def t153_worst(r, D):
    gb = r.choice([2.45, 3.12, 4.80, 0.682, 1.56]); f = r.choice([0.04, 0.05, 0.06, 0.08])
    gw = gb * (1 + f * r.choice([1, -1]))
    ib = r.choice([0.12, 0.25, 0.40, 1.50]); iw = ib * (1 + r.choice([0.15, -0.20, 0.30]))
    dg = abs(gb - gw); di = abs(ib - iw)
    return Q(f'From a graph with error bars, the line of best fit has gradient {nf(gb, 3)} and y-intercept {nf(ib, 3)}. The worst acceptable line has gradient {nf(gw, 3)} and y-intercept {nf(iw, 3)} (same units). State the gradient and intercept with their absolute uncertainties, and calculate the percentage uncertainty in the gradient.',
             f'gradient = {nf(gb, 3)} ± {nf(dg, 1)}; intercept = {nf(ib, 3)} ± {nf(di, 1)}; {nf(100 * dg / gb, 2)}%',
             f'Δgradient = |{nf(gb, 3)} − {nf(gw, 3)}| = {nf(dg, 1)} [1]; Δintercept = {nf(di, 1)} [1]; percentage = {nf(100 * dg / gb, 2)}% [1]' + (' [3]' if D <= 3 else '; values quoted to precision consistent with uncertainty [1] [4]'))


def _ana_c4(r, D):
    T1 = r.choice([0.82, 0.95, 1.10]); m1 = 0.100; m2 = 0.300; T2 = T1 * math.sqrt(3) * r.choice([0.97, 1.0, 1.04])
    k1 = T1 / math.sqrt(m1); k2 = T2 / math.sqrt(m2)
    pd = abs(k2 - k1) / k1 * 100; crit = 100 * 0.02 / T1
    intro = r.choice([f'A candidate in {city(r)} investigates a mass on a spring. With m = {m1:.3f} kg the period is {T1:.2f} s; with m = {m2:.3f} kg it is {T2:.2f} s. It is suggested that T = k√m.', f'For a mass-spring system, T = {T1:.2f} s when m = {m1:.3f} kg and T = {T2:.2f} s when m = {m2:.3f} kg. The relationship T = k√m is to be tested.'])
    parts = [
        lambda r: ('Calculate two values of k.', f'{nf(k1, 3)} and {nf(k2, 3)} s kg⁻¹ᐟ²', 'both [2]'),
        lambda r: ('The period was found by timing 10 oscillations with an uncertainty of 0.2 s. Estimate the percentage uncertainty in the first period.', f'{nf(100 * 0.02 / T1, 2)}%', f'ΔT = 0.02 s; ÷ {T1:.2f} [2]'),
        lambda r: ('Taking the percentage uncertainty in T as the criterion, state whether the results support the relationship.', f'percentage difference in k = {nf(pd, 2)}%, ' + ('less' if pd <= crit else 'greater') + f' than {nf(crit, 2)}%, so the relationship is ' + ('supported' if pd <= crit else 'not supported') + '.', 'percentage difference [1]; comparison and conclusion [1] [2]'),
        lambda r: ('Identify two limitations of the procedure.', 'only two values of m; difficult to judge start/end of oscillation; spring oscillates sideways', 'first valid limitation [1]; second valid limitation [1] [2]'),
        lambda r: ('Suggest improvements for the limitations.', 'take more readings over a wider range and plot T² against m; use a fiducial marker or motion sensor; guide the motion', 'improvement matching first limitation [1]; improvement matching second limitation [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t153.add('C4', (2, 3, 4, 5), 'multi_step')(_ana_c4)

N154 = 'Identifying limitations and suggesting improvements to experiments'
t154 = topic(N154, N154.lower(), 'limitations', 'improvements to experiments')
LIMS = [
    ('timing the fall of a paper cone dropped from a height of 1.5 m with a stopwatch', 'the time is short, so reaction time causes a large percentage uncertainty', 'use a longer drop height or a video camera with a timer / light gates'),
    ('measuring the period of a pendulum by timing one oscillation', 'one oscillation is too short to time accurately (reaction time)', 'time 20 oscillations and divide by 20, using a fiducial marker'),
    ('measuring the rebound height of a bouncing ball by eye against a metre rule', 'it is difficult to judge the maximum height (parallax and the ball moves quickly)', 'film the bounce against a scale and use frame-by-frame playback'),
    ('measuring the diameter of a wire once with a micrometer', 'the wire may not be uniform, so one reading may not be representative', 'measure at several points along the wire and in different orientations, then average'),
    ('measuring the temperature of a liquid with a thermometer while it is heated', 'the liquid may not be at a uniform temperature', 'stir the liquid before each reading'),
    ('measuring the extension of a long wire with a ruler held by hand', 'the extension is very small and the ruler moves, giving a large uncertainty', 'use a vernier scale attached to a reference wire / a travelling microscope'),
    ('measuring the current in a thermistor that warms up as current flows', 'the current heats the thermistor, changing its resistance during the reading', 'use a small current / switch off between readings / allow to reach steady state'),
    ('taking only two readings to test whether two quantities are proportional', 'two readings are not enough to draw a valid conclusion', 'take at least six readings over a wide range and plot a graph'),
    ('releasing a trolley by hand at the top of a ramp', 'the trolley may be given an initial push, so it does not start from rest', 'hold it with a barrier/electromagnet and release it'),
    ('measuring the distance a ball rolls along a carpet', 'the ball may veer to one side and the carpet surface is uneven', 'use a guide rail / a smoother uniform surface'),
]
FX(t154, 'C1', (1, 2), [
    ('A student times a falling object over a short distance with a hand-held stopwatch. Which is the most significant source of uncertainty?', 'Human reaction time in starting and stopping the stopwatch', 'Reaction time is large compared with a short interval.', ['The resolution of the stopwatch', 'The mass of the object', 'The colour of the object']),
    ('Which improvement reduces the random error in measuring the period of a pendulum?', 'Timing many oscillations and repeating the measurement', 'Larger total time and averaging reduce random error.', ['Using a heavier bob', 'Using a stopwatch with more digits', 'Measuring the length more carefully']),
    ('In Paper 3, which is NOT an acceptable improvement?', '"Be more careful"', 'Improvements must be specific and practical.', ['Use a fiducial marker at the centre of the swing', 'Use light gates connected to a timer', 'Take more readings and plot a graph']),
    ('A student finds that the temperature of a wire rises during a resistance experiment. A suitable improvement is to', 'use a smaller current or switch off between readings', 'Reduces heating so resistance is not changed.', ['use a thicker voltmeter lead', 'record more significant figures', 'use a longer metre rule']),
    ('Repeating readings is an improvement that reduces', 'random errors', 'Averaging reduces random scatter.', ['systematic errors', 'zero errors', 'calibration errors']),
    ('State the general improvement when only two sets of readings have been taken.', 'Take more readings (at least six) over a wide range and plot a graph.', 'more readings and plot graph [1]'),
])
FX(t154, 'C2', (1, 2, 3, 4), [
    ('Explain why "use a computer" is not an acceptable improvement in Paper 3, and give an example of how it could be made acceptable.', 'It does not say what is measured or how; an acceptable version names the equipment and its purpose, e.g. "use a motion sensor connected to a data logger to measure the speed of the trolley".', 'vague/does not state what or how [1]; specific example with purpose [1] [2]'),
    ('Explain the difference between a limitation and a source of uncertainty that is not significant.', 'A limitation is a significant source of error in the specific experiment that affects the result; trivial issues (e.g. "human error") are not credited.', 'limitation is significant/specific to experiment [1]; vague or trivial points not credited [1] [2]'),
    ('Explain why improving the precision of an instrument does not always improve the result.', 'If the dominant uncertainty is elsewhere (e.g. reaction time or difficulty judging the moment), a more precise instrument does not reduce the overall uncertainty.', 'dominant uncertainty elsewhere [1]; precision of instrument not limiting [1] [2]'),
])


@t154.add('C2', (2, 3, 4), 'explain')
def t154_lim(r, D):
    exp_, lim, imp = r.choice(LIMS)
    return Q(f'A student in {city(r)} is {exp_}. Identify a significant limitation of this method and suggest a specific improvement.', f'Limitation: {lim}. Improvement: {imp}.', 'limitation specific to the experiment [1]; matching, practical improvement [1] [2]')


@t154.add('C3', (2, 3, 4), 'case')
def t154_pair(r, D):
    a, b = r.sample(LIMS, 2)
    return Q(f'In one investigation, a student is (i) {a[0]} and (ii) {b[0]}. For each, describe one limitation and suggest an improvement.',
             f'(i) {a[1]}; improve: {a[2]}. (ii) {b[1]}; improve: {b[2]}.', '(i) limitation [1]; improvement [1] (ii) limitation [1]; improvement [1] [4]')


def _lim_c4(r, D):
    ex = r.choice([('a student drops a paper cone from different heights and times its fall with a stopwatch to see whether it reaches terminal velocity', [
        ('Identify the limitation caused by the timing method and suggest an improvement.', 'Reaction time is significant for short falls; use a video with a timer or light gates.'),
        ('Identify a limitation in releasing the cone and suggest an improvement.', 'The cone may not be released from rest or may tilt; release it from a clamp/electromagnet or hold by a thread and burn it.'),
        ('Identify a limitation caused by air movement and suggest an improvement.', 'Draughts deflect the cone; close windows and doors/use a tall tube.'),
        ('Identify a limitation of the number of readings and suggest an improvement.', 'Only one or two heights; take readings at six or more heights and repeat each.')]),
        ('a student rolls a ball down a ramp and measures how far it travels along the floor for different ramp heights', [
        ('Identify a limitation in measuring the ramp height and suggest an improvement.', 'Height difficult to measure vertically; use a set square/spirit level with a metre rule.'),
        ('Identify a limitation in the ball\'s path on the floor and suggest an improvement.', 'The ball curves or the floor is uneven; use a guide channel/smooth level board.'),
        ('Identify a limitation in judging where the ball stops and suggest an improvement.', 'Ball may still be rolling slowly; mark the position with sand tray/video.'),
        ('Identify a limitation of the release and suggest an improvement.', 'Ball may be pushed; release by removing a barrier.')])])
    desc, items = ex
    intro = f'In a Paper 3 investigation in {city(r)}, {desc}.'
    parts = [(lambda r, q=q, a=a: (q, a, 'limitation [1]; improvement [1] [2]')) for q, a in items]
    parts.append(lambda r: ('Explain why vague suggestions such as "repeat more carefully" do not gain credit.', 'They do not identify a specific cause or a practical change to the method.', 'not specific / no practical change [1]'))
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t154.add('C4', (2, 3, 4, 5), 'multi_step')(_lim_c4)
t154.add('C3', (3, 4, 5), 'case')(_lim_c4)

CHAPTERS[15] = [t151, t152, t153, t154]
