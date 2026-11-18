"""CBSE class 11 physics (NCERT Physics XI) families, chapters 1-5."""
from __future__ import annotations

import math
from math import gcd
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, sup, name, two_names, CITIES
from g11_physics_util import polish, sig, g, NUM, NUM2, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq, pick, ordn

S = 'cbse-g11-physics-ch'
G = 9.8


# ======================================================== ch01 Units and Measurements
# st1 SI units and significant figures

SI_UNITS = [('length', 'metre (m)'), ('mass', 'kilogram (kg)'), ('time', 'second (s)'), ('electric current', 'ampere (A)'),
            ('thermodynamic temperature', 'kelvin (K)'), ('amount of substance', 'mole (mol)'), ('luminous intensity', 'candela (cd)'),
            ('force', 'newton (N)'), ('energy', 'joule (J)'), ('power', 'watt (W)'), ('pressure', 'pascal (Pa)'), ('frequency', 'hertz (Hz)')]
c1s1_units = term_mcq(SI_UNITS, 'What is the SI unit of {a}?', 'Which physical quantity has the SI unit {b}?', 'The SI unit of {a} is the {b}.')

BIG_UNITS = [('1 astronomical unit (AU)', '1.496 × 10¹¹ m'), ('1 light year (ly)', '9.46 × 10¹⁵ m'), ('1 parsec', '3.08 × 10¹⁶ m'),
             ('1 fermi (fm)', '10⁻¹⁵ m'), ('1 angstrom (Å)', '10⁻¹⁰ m'), ('1 micron (μm)', '10⁻⁶ m'), ('1 nanometre (nm)', '10⁻⁹ m')]
c1s1_bigunits = term_mcq(BIG_UNITS, '{a} is approximately equal to', 'Which unit of length is approximately equal to {b}?', '{a} ≈ {b}.')


def _sf_string(r):
    n = r.randint(2, 5)
    d = str(r.randint(1, 9)) + ''.join(r.choice('0123456789') for _ in range(n - 1))
    kind = r.randint(0, 2)
    t = r.choice([0, 0, 1, 2])
    if kind == 0:
        s = '0.' + '0' * r.randint(1, 3) + d + '0' * t
    elif kind == 1:
        k = r.randint(1, n - 1)
        s = d[:k] + '.' + d[k:] + '0' * t
    else:
        s = d[0] + '.' + d[1:] + '0' * t + f' × 10{sup(r.choice([-7, -5, -3, 3, 4, 6, 8]))}'
    return s, n + t


def c1s1_count_sf(r):
    s, n = _sf_string(r)
    unit = r.choice(['m', 'kg', 's', 'g', 'cm', 'J'])
    return mcq(f'How many significant figures are there in the measurement {s} {unit}?', str(n),
               [str(x) for x in r.sample([x for x in range(1, 9) if x != n], 3)],
               f'{n}: non-zero digits and zeros between them count; leading zeros only fix the decimal point; trailing zeros after a decimal point are significant; the power of 10 is not counted.', r)


def c1s1_add_rule(r):
    a = Decimal(r.randint(10000, 99999)) / 100
    b = Decimal(r.randint(1000, 9999)) / 10
    c = Decimal(r.randint(100, 999)) / 1000
    tot = a + b + c
    rounded = tot.quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
    who = name(r)
    return {'stem': f'{who} weighs three samples in the school lab: {a} g, {b} g and {c} g. Find the total mass, quoted to the correct number of significant figures.',
            'answer': f'{rounded} g', 'key': f'Sum = {tot} g; in addition the result keeps the least number of decimal places in the data (one, from {b} g), so {rounded} g.',
            'distractors': [f'{tot} g', f'{tot.quantize(Decimal("0.01"))} g', f'{tot.quantize(Decimal("1"))} g']}


def c1s1_mul_rule(r):
    l = r.randint(1000, 9999) / 1000 * r.choice([1, 10])
    b = r.randint(100, 999) / 100
    A = l * b
    return {'stem': f'The length and breadth of a rectangular sheet are {sig(l, 4)} m and {sig(b, 3)} m. Find its area to the correct number of significant figures.',
            'answer': f'{sig(A, 3)} m²', 'key': f'{sig(l, 4)} × {sig(b, 3)} = {A:.6g} m²; the product keeps the least number of significant figures in the data (three, from {sig(b, 3)} m), so {sig(A, 3)} m².',
            'distractors': [f'{A:.6g} m²', f'{sig(A, 4)} m²', f'{sig(A, 2)} m²']}


def c1s1_round(r):
    while True:
        x = r.randint(100000, 999999) / 10 ** r.randint(2, 5)
        digits = f'{x:.6e}'.replace('.', '')
        if digits[3] != '5':
            break
    return {'stem': f'Round off {x} to three significant figures.', 'answer': sig(x, 3),
            'key': f'Keep three significant figures; the next digit is {digits[3]}, so the third digit is {"raised by one" if int(digits[3]) > 5 else "left unchanged"}: {sig(x, 3)}.',
            'distractors': [sig(x, 2), sig(x, 4), sig(x * 10, 3)]}


def c1s1_cube(r):
    a = r.randint(1001, 9999) / 1000 * r.choice([1, 10])
    sa, v = 6 * a * a, a ** 3
    return {'stem': f'Each side of a cube is measured to be {sig(a, 4)} m. What are the total surface area and the volume of the cube to appropriate significant figures?',
            'answer': f'Surface area {sig(sa, 4)} m²; volume {sig(v, 4)} m³',
            'key': f'Side has 4 significant figures. Area = 6a² = {sa:.6g} → {sig(sa, 4)} m² (1.5 marks); volume = a³ = {v:.6g} → {sig(v, 4)} m³ (1.5 marks).'}


DENS = [('mercury', 13.6), ('copper', 8.96), ('aluminium', 2.70), ('iron', 7.87), ('silver', 10.5), ('lead', 11.3)]


def c1s1_density(r):
    m, rho = r.choice(DENS)
    v = r.choice([50, 75, 120, 150, 200, 250, 400])
    mass = rho * v / 1000
    return {'stem': f'The density of {m} is {rho} g cm⁻³. (i) Express it in SI units. (ii) Find the mass of {v} cm³ of {m} in kilogram, to three significant figures.',
            'answer': f'(i) {g(rho * 1000)} kg m⁻³ (ii) {sig(mass, 3)} kg',
            'key': f'(i) 1 g cm⁻³ = 10⁻³ kg / 10⁻⁶ m³ = 10³ kg m⁻³, so {g(rho * 1000)} kg m⁻³ (1 mark). (ii) m = ρV = {rho} × {v} = {g(rho * v)} g = {sig(mass, 3)} kg (2 marks).'}


c1s1_explain = pool_txt([
    ('Why is a length recorded as 4.700 m said to be more precise than one recorded as 4.7 m?',
     'The trailing zeros in 4.700 m are significant, so the length is known to 1 mm, not just to 0.1 m.',
     'Trailing zeros after the decimal point are significant (1 mark); more significant figures = finer resolution of the measuring instrument (1 mark).'),
    ('Show that changing the unit of 2.308 cm to metre does not change its number of significant figures.',
     '2.308 cm = 0.02308 m = 2.308 × 10⁻² m: still four significant figures.',
     'The zeros in 0.02308 only locate the decimal point and are not significant (1 mark); scientific notation shows four significant figures (1 mark).'),
    ('A length is written as 4700 m. Why is this ambiguous, and how does scientific notation remove the ambiguity?',
     'It is not clear whether the trailing zeros are measured; 4.7 × 10³ m (two s.f.) or 4.700 × 10³ m (four s.f.) states it clearly.',
     'Trailing zeros in a number without a decimal point may not be significant (1 mark); writing a × 10ᵇ shows exactly which digits are significant (1 mark).'),
    ('A student multiplies 3.2 m by 1.256 m and writes the area as 4.0192 m². Explain what is wrong.',
     'The answer cannot be more precise than the least precise datum; it should be 4.0 m² (two significant figures).',
     'Rule: product has as many s.f. as the factor with the fewest (1 mark); 3.2 has two s.f., so 4.0 m² (1 mark).'),
    ('Why is it said that the number of significant figures in a measurement depends on the measuring instrument and not on the unit chosen?',
     'Significant figures report the reliably known digits plus one uncertain digit, fixed by the instrument\'s least count; changing units only moves the decimal point.',
     'Significant figures = reliable digits + first uncertain digit (1 mark); unit change multiplies by powers of 10, which adds or removes only non-significant zeros (1 mark).'),
    ('Explain why the SI system needs only seven base units even though physics uses hundreds of quantities.',
     'All other quantities can be expressed as combinations of the seven base quantities, so their units are derived units.',
     'Base vs derived quantities (1 mark) with an example such as 1 N = 1 kg m s⁻² (1 mark).'),
])

c1s1_ar = pool_ar([
    ('The number 0.007 m has one significant figure.', 'Zeros to the left of the first non-zero digit in a number less than one are not significant.', 'a', 'Both true; R is the rule that gives A.'),
    ('The length 4.700 m has four significant figures.', 'Trailing zeros in a number with a decimal point are significant.', 'a', 'Both true; R explains A.'),
    ('The sum 436.32 g + 227.2 g + 0.301 g should be reported as 663.8 g.', 'In addition, the result keeps the least number of significant figures in any of the numbers added.', 'c',
     'A is true, but the addition rule is about decimal places, not significant figures, so R is false.'),
    ('Writing 2.308 cm as 0.02308 m increases the number of significant figures.', 'Zeros that appear because of a change of units are not significant.', 'd', 'A is false (still four s.f.); R is true.'),
    ('The kilogram is an SI base unit.', 'The SI system has seven base units.', 'b', 'Both true, but the number of base units does not explain why the kilogram is one of them.'),
    ('A light year is a unit of time.', 'One light year is the distance travelled by light in one year.', 'd', 'A is false: R shows it is a unit of length.'),
])


# st2 Dimensions and dimensional analysis

DIMS = {'force': (1, 1, -2), 'work': (1, 2, -2), 'power': (1, 2, -3), 'pressure': (1, -1, -2), 'momentum': (1, 1, -1),
        'impulse': (1, 1, -1), 'gravitational constant G': (-1, 3, -2), 'Planck\'s constant': (1, 2, -1), 'surface tension': (1, 0, -2),
        'coefficient of viscosity': (1, -1, -1), 'angular momentum': (1, 2, -1), 'torque': (1, 2, -2), 'spring constant': (1, 0, -2),
        'Young\'s modulus': (1, -1, -2), 'frequency': (0, 0, -1), 'acceleration': (0, 1, -2), 'density': (1, -3, 0),
        'gravitational potential': (0, 2, -2), 'moment of inertia': (1, 2, 0), 'angular velocity': (0, 0, -1), 'strain': (0, 0, 0),
        'stress': (1, -1, -2), 'velocity': (0, 1, -1), 'latent heat': (0, 2, -2), 'kinetic energy': (1, 2, -2)}


def dstr(d) -> str:
    if not any(d):
        return '[M⁰ L⁰ T⁰]'
    parts = []
    for sym, e in zip('MLT', d):
        if e == 0:
            continue
        if isinstance(e, Fr) and e.denominator != 1:
            parts.append(f'{sym}^({e})'.replace('-', '−'))
        else:
            parts.append(sym if e == 1 else f'{sym}{sup(int(e))}')
    return '[' + ' '.join(parts) + ']'


def c1s2_dimform(r):
    q = r.choice(list(DIMS))
    d = DIMS[q]
    wrong = list(dict.fromkeys(dstr(v) for k, v in DIMS.items() if v != d))
    return mcq(f'What is the dimensional formula of {q}?', dstr(d), r.sample(wrong, 3), f'{q.capitalize()}: {dstr(d)}.', r)


def c1s2_same_pair(r):
    groups = {}
    for k, v in DIMS.items():
        groups.setdefault(v, []).append(k)
    multi = [v for v in groups.values() if len(v) >= 2]
    a, b = r.sample(r.choice(multi), 2)
    keys = list(DIMS)
    wrongs = set()
    while len(wrongs) < 3:
        x, y = r.sample(keys, 2)
        if DIMS[x] != DIMS[y]:
            wrongs.add(f'{x} and {y}')
    return mcq('Which of the following pairs of physical quantities have the same dimensions?', f'{a} and {b}', list(wrongs),
               f'Both {a} and {b} have dimensions {dstr(DIMS[a])}.', r)


EQ_OK = ['v = u + at', 's = ut + ½at²', 'v² = u² + 2as', 'T = 2π√(l/g)', 'F = mv²/r', 'E = ½mv² + mgh', 'P = Fv', 'v = √(2gh)', 'p = ρgh', 'λ = h/(mv)']
EQ_BAD = [('s = ut + ½at³', 'at³ has dimensions [L T], not [L]'), ('v = u + as', 'as has dimensions [L² T⁻²], not [L T⁻¹]'),
          ('T = 2π√(g/l)', '√(g/l) has dimensions [T⁻¹]'), ('F = mv/r', 'mv/r has dimensions [M T⁻¹]'),
          ('E = mv + mgh', 'mv has dimensions [M L T⁻¹], not energy'), ('v² = u + 2as', 'u has dimensions [L T⁻¹] but v² is [L² T⁻²]'),
          ('p = ρg/h', 'ρg/h has dimensions [M L⁻³ T⁻²]')]


def c1s2_check_eq(r):
    bad, why = r.choice(EQ_BAD)
    return mcq('Using the principle of homogeneity of dimensions, which of the following equations is dimensionally INCORRECT?', bad, r.sample(EQ_OK, 3),
               f'{bad} is wrong: {why}; every term of a correct equation must have the same dimensions.', r)


SYSTEMS = [('1 g', 1e-3, '1 cm', 1e-2, '1 s', 1), ('100 g', 0.1, '10 cm', 0.1, '1 min', 60), ('10 kg', 10, '1 km', 1e3, '1 min', 60),
           ('0.5 kg', 0.5, '2 m', 2, '0.1 s', 0.1), ('2 kg', 2, '10 m', 10, '5 s', 5), ('1 g', 1e-3, '1 mm', 1e-3, '1 ms', 1e-3)]
CONV_Q = [('a force of {v} N', 'force'), ('an energy of {v} J', 'work'), ('a pressure of {v} Pa', 'pressure'), ('a power of {v} W', 'power'),
          ('a momentum of {v} kg m s⁻¹', 'momentum'), ('a density of {v} kg m⁻³', 'density')]


def c1s2_convert(r):
    sm, xm, sl, xl, st, xt = r.choice(SYSTEMS)
    desc, q = r.choice(CONV_Q)
    a, b, c = DIMS[q]
    n1 = r.choice([2, 4.2, 5, 8, 12, 20, 25, 50, 100, 1000])
    n2 = n1 * xm ** -a * xl ** -b * xt ** -c
    return NUM(f'A new system of units takes {sm} as the unit of mass, {sl} as the unit of length and {st} as the unit of time. '
               f'What is the numerical value of {desc.format(v=g(n1))} in this system?', n2, '',
               f'n₂ = n₁ (M₁/M₂)ᵃ (L₁/L₂)ᵇ (T₁/T₂)ᶜ with {q} = {dstr((a, b, c))}: n₂ = {g(n1)} × ({_ratio(xm)}){sup(a)} × ({_ratio(xl)}){sup(b)} × ({_ratio(xt)}){sup(c)} = {{ans}}.',
               wrongs=[n1 * xm ** a * xl ** b * xt ** c, n1 * xm ** -a * xl ** -b, n1 * xl ** -b * xt ** -c])


def _ratio(x):
    return f'1/{g(x)}' if x >= 1 else g(1 / x)


def _pw(sym, e):
    e = Fr(e)
    if e == 0:
        return ''
    if e == 1:
        return sym
    if e.denominator == 1:
        return sym + sup(int(e))
    return f'{sym}^({_exp(e)})'


def _lin(coefs, names, rhs):
    terms = []
    for c, nme in zip(coefs, names):
        if c == 0:
            continue
        t = nme if abs(c) == 1 else f'{abs(c)}{nme}'
        terms.append(('− ' if c < 0 else '+ ') + t)
    s = ' '.join(terms).lstrip('+ ')
    if s.startswith('− '):
        s = '−' + s[2:]
    return f'{s} = {str(rhs).replace("-", "−")}'


def solve3(A, bvec):
    M = [[Fr(x) for x in row] + [Fr(y)] for row, y in zip(A, bvec)]
    n = len(M)
    for i in range(n):
        p = next(j for j in range(i, n) if M[j][i] != 0)
        M[i], M[p] = M[p], M[i]
        for j in range(n):
            if j != i and M[j][i] != 0:
                f = M[j][i] / M[i][i]
                M[j] = [a - f * b for a, b in zip(M[j], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


DERIV = [
    ('the time period T of a simple pendulum', 'T', (0, 0, 1), [('m', 'the mass m of the bob', (1, 0, 0)), ('l', 'its length l', (0, 1, 0)), ('g', 'the acceleration due to gravity g', (0, 1, -2))], 'T = k√(l/g)'),
    ('the speed v of a transverse wave on a stretched string', 'v', (0, 1, -1), [('F', 'the tension F', (1, 1, -2)), ('μ', 'the mass per unit length μ', (1, -1, 0)), ('l', 'the length l of the string', (0, 1, 0))], 'v = k√(F/μ)'),
    ('the viscous drag F on a small sphere falling through a liquid', 'F', (1, 1, -2), [('η', 'the coefficient of viscosity η', (1, -1, -1)), ('r', 'the radius r', (0, 1, 0)), ('v', 'the speed v', (0, 1, -1))], 'F = kηrv'),
    ('the frequency ν of vibration of a stretched string', 'ν', (0, 0, -1), [('F', 'the tension F', (1, 1, -2)), ('l', 'the length l', (0, 1, 0)), ('μ', 'the mass per unit length μ', (1, -1, 0))], 'ν = (k/l)√(F/μ)'),
    ('the centripetal force F on a body moving in a circle', 'F', (1, 1, -2), [('m', 'its mass m', (1, 0, 0)), ('v', 'its speed v', (0, 1, -1)), ('r', 'the radius r', (0, 1, 0))], 'F = kmv²/r'),
    ('the escape speed v from a planet', 'v', (0, 1, -1), [('G', 'the gravitational constant G', (-1, 3, -2)), ('M', 'the mass M of the planet', (1, 0, 0)), ('R', 'its radius R', (0, 1, 0))], 'v = k√(GM/R)'),
    ('the time period T of a mass-spring oscillator', 'T', (0, 0, 1), [('m', 'the mass m', (1, 0, 0)), ('k', 'the spring constant k', (1, 0, -2)), ('A', 'the amplitude A', (0, 1, 0))], 'T = C√(m/k), independent of A'),
    ('the speed v of sound in a medium', 'v', (0, 1, -1), [('B', 'the bulk modulus B', (1, -1, -2)), ('ρ', 'the density ρ', (1, -3, 0)), ('λ', 'the wavelength λ', (0, 1, 0))], 'v = k√(B/ρ)'),
    ('the period T of a satellite in a circular orbit', 'T', (0, 0, 1), [('G', 'the gravitational constant G', (-1, 3, -2)), ('M', 'the mass M of the planet', (1, 0, 0)), ('R', 'the orbit radius R', (0, 1, 0))], 'T = k√(R³/(GM))'),
    ('the pressure p exerted by a gas', 'p', (1, -1, -2), [('ρ', 'its density ρ', (1, -3, 0)), ('v', 'the root-mean-square speed v of its molecules', (0, 1, -1)), ('m', 'the mass m of one molecule', (1, 0, 0))], 'p = kρv²'),
]


def _exp(e: Fr) -> str:
    return str(e).replace('-', '−')


def c1s2_derive(r):
    what, sym, tgt, vars_, final = r.choice(DERIV)
    A = [[v[2][i] for v in vars_] for i in range(3)]
    x = solve3(A, list(tgt))
    names = ', '.join(v[1] for v in vars_[:-1]) + ' and ' + vars_[-1][1]
    form = f'{sym} = k ' + ' '.join(p for p in (_pw(v[0], e) for v, e in zip(vars_, x)) if p)
    eqs = '; '.join(f'{s}: ' + _lin([v[2][i] for v in vars_], 'abc', tgt[i]) for i, s in enumerate('MLT'))
    return {'stem': f'Assuming that {what} depends on {names}, use the method of dimensions to find the relation (take the dimensionless constant as k).',
            'answer': f'{form}, i.e. {final}',
            'key': f'Write {sym} = k {vars_[0][0]}ᵃ {vars_[1][0]}ᵇ {vars_[2][0]}ᶜ and equate powers ({eqs}) (2 marks); a = {_exp(x[0])}, b = {_exp(x[1])}, c = {_exp(x[2])} (1 mark), so {final}.'}


LHS = [('force F', (1, 1, -2)), ('energy E', (1, 2, -2)), ('velocity v', (0, 1, -1)), ('pressure p', (1, -1, -2)), ('power P', (1, 2, -3)), ('displacement y', (0, 1, 0))]


def c1s2_constants(r):
    (lq, d) = r.choice(LHS)
    p, q = r.choice([(1, 2), (2, 1), (2, 3), (3, 2), (1, 3), (Fr(1, 2), 2), (2, Fr(1, 2))])
    sym = lq.split()[-1]
    da = (d[0], d[1] - p, d[2])
    db = (d[0], d[1], d[2] - q)

    def pw(v, e):
        return v if e == 1 else (f'√{v}' if e == Fr(1, 2) else f'{v}{sup(int(e))}')
    return {'stem': f'The {lq} of a body varies as {sym} = a{pw("x", p)} + b{pw("t", q)}, where x is a distance and t is time. Find the dimensions of a and b.',
            'answer': f'a: {dstr(da)}; b: {dstr(db)}',
            'key': f'Each term must have the dimensions of {lq.split()[0]} {dstr(d)} (1 mark). a = {dstr(d)}/{dstr((0, Fr(p), 0))} = {dstr(da)} (1 mark); b = {dstr(d)}/{dstr((0, 0, Fr(q)))} = {dstr(db)} (1 mark).'}


c1s2_correct_eq = pool_txt([
    ('A student writes the time period of a mass-spring oscillator as T = 2π√(k/m). Use dimensions to show it is wrong and write the correct form.',
     'T = 2π√(m/k)', '√(k/m) = √([M T⁻²]/[M]) = [T⁻¹], not [T] (2 marks); inverting gives √(m/k) with dimension [T] (1 mark).'),
    ('A student writes the escape speed as v = √(2GMR). Check it dimensionally and correct it.',
     'v = √(2GM/R)', 'GMR = [M⁻¹L³T⁻²][M][L] = [L⁴T⁻²], √ gives [L²T⁻¹], not a speed (2 marks); GM/R = [L²T⁻²] gives [L T⁻¹] (1 mark).'),
    ('A student writes the speed of a wave on a string as v = √(μ/F), where F is the tension and μ the mass per unit length. Check and correct.',
     'v = √(F/μ)', 'μ/F = [M L⁻¹]/[M L T⁻²] = [L⁻² T²], √ gives [L⁻¹ T] (2 marks); F/μ gives [L T⁻¹] (1 mark).'),
    ('Bernoulli\'s equation is written by a student as P + ½ρv + ρgh = constant. Use dimensions to find the error.',
     'The term should be ½ρv².', 'P and ρgh are [M L⁻¹ T⁻²], ½ρv is [M L⁻² T⁻¹] (2 marks); ½ρv² is [M L⁻¹ T⁻²] (1 mark).'),
    ('A student writes the centripetal acceleration as a = v/r². Check dimensionally and correct it.',
     'a = v²/r', 'v/r² = [L⁻¹ T⁻¹], not [L T⁻²] (2 marks); v²/r = [L T⁻²] (1 mark).'),
    ('A student writes the kinetic energy of a body as K = ½m²v. Check it dimensionally and correct it.',
     'K = ½mv²', 'm²v = [M² L T⁻¹] ≠ [M L² T⁻²] (2 marks); mv² = [M L² T⁻²] (1 mark).'),
])

c1s2_planck = pool_txt([
    ('Using Planck\'s constant h, the speed of light c and the gravitational constant G, form a quantity with the dimension of length (the Planck length).',
     'l = √(hG/c³)', 'h = [ML²T⁻¹], c = [LT⁻¹], G = [M⁻¹L³T⁻²]; l = hᵃcᵇGᶜ gives a + … : M: a − c = 0, L: 2a + b + 3c = 1, T: −a − b − 2c = 0 (3 marks); a = c = ½, b = −3/2 (2 marks).'),
    ('Using h, c and G, form a quantity with the dimension of time (the Planck time).',
     't = √(hG/c⁵)', 'M: a − c = 0, L: 2a + b + 3c = 0, T: −a − b − 2c = 1 (3 marks); a = c = ½, b = −5/2 (2 marks).'),
    ('Using h, c and G, form a quantity with the dimension of mass (the Planck mass).',
     'm = √(hc/G)', 'M: a − c = 1, L: 2a + b + 3c = 0, T: −a − b − 2c = 0 (3 marks); a = ½, b = ½, c = −½ (2 marks).'),
])

c1s2_explain = pool_txt([
    ('State two limitations of the method of dimensional analysis.',
     'It cannot give dimensionless constants (like 2π or ½), and it cannot derive relations with sums of terms or with trigonometric, exponential or logarithmic functions.',
     'Any two valid limitations, 1 mark each.'),
    ('State the principle of homogeneity of dimensions and explain how it is used to check an equation.',
     'Every term on both sides of a physical equation must have the same dimensions; if any term differs, the equation is wrong.',
     'Statement (1 mark); use: compare dimensions of each term (1 mark).'),
    ('Plane angle has a unit (radian) but no dimensions. Explain why.',
     'An angle is arc length divided by radius, a ratio of two lengths, so its dimensional formula is [M⁰ L⁰ T⁰].',
     'θ = arc/radius (1 mark); ratio of like quantities is dimensionless (1 mark).'),
    ('Why must the argument of a sine, exponential or logarithm function in a physical equation be dimensionless?',
     'These functions are defined by power series in their argument; adding x, x², x³ … is meaningful only if x has no dimensions.',
     'Series argument (1 mark); hence ωt in sin(ωt) must be dimensionless (1 mark).'),
    ('Quantities with different dimensions cannot be added, but they can be multiplied. Explain with an example.',
     'Adding mass to time is meaningless, but force × time = impulse is a new physical quantity with its own dimensions.',
     'Addition needs like quantities (1 mark); product gives a new quantity, e.g. impulse [M L T⁻¹] (1 mark).'),
])

c1s2_ar = pool_ar([
    ('Pressure and Young\'s modulus have the same dimensions.', 'Both are a force per unit area.', 'a', 'Both are [M L⁻¹ T⁻²]; R explains A.'),
    ('Work and torque have the same dimensions.', 'Work and torque are both scalar quantities.', 'c', 'A is true ([M L² T⁻²]); R is false because torque is a vector.'),
    ('Dimensional analysis cannot give the complete relation T = 2π√(l/g).', 'The constant 2π is dimensionless.', 'a', 'R explains why the method misses it.'),
    ('In y = A sin(ωt), ωt must be dimensionless.', 'The argument of a trigonometric function must be dimensionless.', 'a', 'R is the general rule; A is a case of it.'),
    ('Strain has a unit in SI.', 'Strain is the ratio of change in length to original length.', 'd', 'A is false: as a ratio of lengths strain has no unit; R is true.'),
    ('s = ut + at² is dimensionally correct but is not the correct equation of motion.', 'Dimensional analysis cannot determine dimensionless constants such as ½.', 'a', 'Both true; R explains why a dimensionally correct equation can still be wrong.'),
])

STOKES = [('water at 20 °C', 1.0e-3), ('glycerine', 1.5), ('castor oil', 0.99), ('blood at 37 °C', 2.7e-3), ('honey', 10.0), ('machine oil', 0.25)]


def c1s2_case(r):
    liq, eta = r.choice(STOKES)
    who = name(r)
    return {'stem': (f'{who} reads that the viscous force on a small ball falling through {liq} is F = 6πηrv, where r is the radius, v the speed and η the coefficient of viscosity. '
                     f'The value of η for {liq} is {g(eta)} Pa s.\n(i) Find the dimensional formula of η. (ii) Express η for {liq} in the CGS unit (poise = g cm⁻¹ s⁻¹). '
                     '(iii) Could dimensional analysis alone have given the factor 6π? (iv) Is F = 6πηr²v dimensionally correct?'),
            'answer': f'(i) [M L⁻¹ T⁻¹] (ii) {g(eta * 10)} poise (iii) No (iv) No',
            'key': f'(i) η = F/(6πrv) = [MLT⁻²]/([L][LT⁻¹]) = [M L⁻¹ T⁻¹] (1). (ii) 1 Pa s = 10³ g/(10² cm × 1 s) = 10 poise, so {g(eta * 10)} poise (1). '
                   '(iii) No: 6π is dimensionless (1). (iv) No: ηr²v has dimensions [M L T⁻¹] (1).'}


# st3 Errors in measurement

c1s3_mcq = pool_mcq([
    ('The zero error of a screw gauge is an example of', 'a systematic error', ['a random error', 'a least count error', 'a relative error'], 'An instrumental error that shifts every reading the same way is systematic.'),
    ('Random errors in a measurement can be reduced by', 'taking a large number of readings and averaging them', ['using a different system of units', 'applying a zero correction', 'using a heavier object'], 'Random errors are irregular in sign and average out.'),
    ('The relative error in a measured quantity a is', 'Δa_mean / a_mean', ['Δa_mean × a_mean', 'a_mean / Δa_mean', 'a_mean − Δa_mean'], 'Relative error = mean absolute error ÷ mean value.'),
    ('When two measured quantities are added or subtracted, the maximum absolute error in the result is', 'the sum of their absolute errors', ['the difference of their absolute errors', 'the product of their absolute errors', 'the larger of the two absolute errors'], 'ΔZ = ΔA + ΔB for both Z = A + B and Z = A − B.'),
    ('When two measured quantities are multiplied, the maximum relative error in the product is', 'the sum of their relative errors', ['the product of their relative errors', 'the difference of their relative errors', 'the ratio of their relative errors'], 'ΔZ/Z = ΔA/A + ΔB/B.'),
    ('If Z = Aⁿ, the relative error in Z is', 'n times the relative error in A', ['the relative error in A divided by n', 'the relative error in A raised to the power n', 'equal to the relative error in A'], 'ΔZ/Z = n ΔA/A.'),
    ('Accuracy of a measurement means', 'how close the measured value is to the true value', ['the resolution of the instrument', 'the number of readings taken', 'the smallest division on the scale'], 'Precision is about resolution; accuracy about closeness to the true value.'),
    ('The least count of an ordinary metre scale is', '1 mm', ['1 cm', '0.1 mm', '0.01 mm'], 'The smallest division on a metre scale is 1 mm.'),
])


def c1s3_mean_error(r):
    base = r.choice([2.5, 1.8, 3.2, 0.95, 4.1])
    vals = [round(base + r.randint(-20, 20) / 100, 2) for _ in range(5)]
    m = sum(vals) / 5
    m2 = round(m, 2)
    devs = [abs(v - m2) for v in vals]
    da = sum(devs) / 5
    da2 = round(da, 2)
    pct = da2 / m2 * 100
    who = name(r)
    return {'stem': f'{who} measured the period of oscillation of a simple pendulum five times: {", ".join(f"{v:.2f}" for v in vals)} s. Find the mean period, the mean absolute error and the percentage error.',
            'answer': f'T = ({m2:.2f} ± {da2:.2f}) s; percentage error ≈ {pct:.0f}%',
            'key': f'Mean = {sum(vals):.2f}/5 = {m2:.2f} s (1); |ΔT| values {", ".join(f"{d:.2f}" for d in devs)}; mean absolute error = {da:.3f} ≈ {da2:.2f} s (1); percentage error = {da2:.2f}/{m2:.2f} × 100 ≈ {pct:.0f}% (1).'}


def c1s3_sum_err(r):
    a, b = r.randint(50, 300), r.randint(50, 300)
    da, db = r.choice([1, 2, 3, 4, 5]), r.choice([1, 2, 3, 4, 5, 6])
    if r.random() < 0.5:
        return {'stem': f'Two resistors of resistances R₁ = ({a} ± {da}) Ω and R₂ = ({b} ± {db}) Ω are connected in series. Find the equivalent resistance with its error.',
                'answer': f'({a + b} ± {da + db}) Ω', 'key': f'R = R₁ + R₂ = {a + b} Ω; ΔR = ΔR₁ + ΔR₂ = {da + db} Ω.',
                'distractors': [f'({a + b} ± {x}) Ω' for x in dict.fromkeys([abs(da - db), da * db, max(da, db), (da + db) / 2, da + db + 1, 2 * (da + db)]) if x != da + db]}
    t1, t2 = sorted([round(a / 10, 1), round(b / 10, 1)])
    if t1 == t2:
        t2 += 1
    return {'stem': f'The temperatures of two bodies are measured as t₁ = ({t1} ± 0.5) °C and t₂ = ({t2} ± 0.5) °C. Find the temperature difference and its error.',
            'answer': f'({num(t2 - t1, 1)} ± 1) °C', 'key': f't₂ − t₁ = {num(t2 - t1, 1)} °C; in a difference the absolute errors add: 0.5 + 0.5 = 1 °C.',
            'distractors': [f'({num(t2 - t1, 1)} ± 0) °C', f'({num(t2 - t1, 1)} ± 0.5) °C', f'({num(t2 - t1, 1)} ± 0.25) °C']}


def c1s3_power_err(r):
    p, q, s_ = r.choice([1, 2, 3]), r.choice([1, 2, 3]), r.choice([Fr(1, 2), 1, 2, 3])
    ea, eb, ec = r.choice([1, 2, 3]), r.choice([1, 2, 3, 4]), r.choice([1, 2, 4])
    tot = float(p * ea + q * eb + s_ * ec)

    def pw(v, e):
        return v if e == 1 else (f'√{v}' if e == Fr(1, 2) else f'{v}{sup(int(e))}')
    ws = [float(x) for x in (ea + eb + ec, p * ea + q * eb - s_ * ec, tot + 1, tot * 2)]
    ws = [f'{g(x)}%' for x in dict.fromkeys(ws) if x != tot and x > 0]
    return {'stem': f'A physical quantity is given by Z = {pw("A", p)}{pw("B", q)}/{pw("C", s_)}. The percentage errors in A, B and C are {ea}%, {eb}% and {ec}%. Find the maximum percentage error in Z.',
            'answer': f'{g(tot)}%', 'key': f'ΔZ/Z = {p}(ΔA/A) + {q}(ΔB/B) + {_exp(Fr(s_))}(ΔC/C) = {p}×{ea} + {q}×{eb} + {_exp(Fr(s_))}×{ec} = {g(tot)}% (errors add even for the divided quantity).',
            'distractors': ws}


def c1s3_lc(r):
    n = r.choice([10, 20, 25, 50])
    return {'stem': f'In a vernier callipers, {n} vernier scale divisions coincide with {n - 1} main scale divisions of 1 mm each. What is its least count?',
            'answer': f'{g(1 / n)} mm', 'key': f'LC = 1 MSD − 1 VSD = 1 − {n - 1}/{n} = 1/{n} mm = {g(1 / n)} mm.',
            'distractors': [f'{g(1 / (n - 1))} mm', f'{g((n - 1) / n)} mm', f'{g(10 / n)} mm']}


def c1s3_g_err(r):
    L = r.choice([50.0, 75.0, 80.0, 100.0, 120.0])
    dL = r.choice([0.1, 0.2, 0.5])
    T = r.choice([1.42, 1.74, 1.79, 2.01, 2.20])
    dT = r.choice([0.01, 0.02])
    pct = (dL / L + 2 * dT / T) * 100
    return NUM(f'In a simple pendulum experiment the length is measured as ({g(L)} ± {g(dL)}) cm and the period as ({T:.2f} ± {dT:.2f}) s. '
               'Since g = 4π²L/T², find the maximum percentage error in g.', pct, '%',
               f'Δg/g = ΔL/L + 2ΔT/T = {g(dL)}/{g(L)} + 2 × {dT}/{T} = {dL / L:.4f} + {2 * dT / T:.4f}; × 100 = {{ans}}.',
               wrongs=[(dL / L + dT / T) * 100, (dL / L - 2 * dT / T) * 100, 2 * (dL / L + dT / T) * 100], n=2)


def c1s3_sphere(r):
    m, dm = r.choice([(45.0, 0.1), (60.0, 0.2), (32.5, 0.1), (80.0, 0.5)])
    dd = r.choice([(2.50, 0.01), (2.24, 0.01), (3.00, 0.02), (1.80, 0.01)])
    d, Dd = dd
    rho = m / (math.pi * d ** 3 / 6)
    pct = (dm / m + 3 * Dd / d) * 100
    return {'stem': f'A steel ball has mass ({g(m)} ± {g(dm)}) g and diameter ({d:.2f} ± {Dd:.2f}) cm measured with a vernier callipers. Find its density and the percentage error in the density.',
            'answer': f'ρ ≈ {sig(rho, 3)} g cm⁻³; error ≈ {sig(pct, 2)}%',
            'key': f'ρ = m/(πd³/6) = {g(m)}/({math.pi * d ** 3 / 6:.3f}) = {sig(rho, 3)} g cm⁻³ (1.5). Δρ/ρ = Δm/m + 3Δd/d = {dm / m:.4f} + {3 * Dd / d:.4f} → {sig(pct, 2)}% (1.5).'}


def c1s3_case(r):
    pitch, nd = r.choice([(0.5, 50), (1.0, 100), (0.5, 100)])
    lc = pitch / nd
    ze = r.choice([-3, -2, 2, 3, 4, 5])
    msr = r.choice([1.5, 2.0, 2.5, 3.0, 4.5]) if pitch == 0.5 else r.choice([1.0, 2.0, 3.0, 4.0])
    csr = r.randint(10, nd - 10)
    obs = msr + csr * lc
    corr = obs - ze * lc
    return {'stem': (f'In the physics lab a screw gauge has pitch {pitch} mm and {nd} divisions on its circular scale. With the jaws closed, the zero of the circular scale is '
                     f'{abs(ze)} divisions {"below" if ze > 0 else "above"} the reference line. For a wire, the main scale reads {msr} mm and the {csr}th circular division is on the line.\n'
                     '(i) Find the least count. (ii) State the zero error with sign. (iii) Find the observed diameter. (iv) Find the corrected diameter.'),
            'answer': f'(i) {g(lc)} mm (ii) {"+" if ze > 0 else "−"}{g(abs(ze) * lc)} mm (iii) {g(obs, 3)} mm (iv) {g(corr, 3)} mm',
            'key': f'(i) LC = pitch/divisions = {pitch}/{nd} = {g(lc)} mm (1). (ii) zero error = {"+" if ze > 0 else "−"}{abs(ze)} × {g(lc)} = {g(ze * lc)} mm (1). '
                   f'(iii) {msr} + {csr} × {g(lc)} = {g(obs, 3)} mm (1). (iv) corrected = observed − zero error = {g(corr, 3)} mm (1).', 'gap': 'G7'}


c1s3_explain = pool_txt([
    ('The true thickness of a sheet is 3.678 cm. Instrument A (resolution 0.1 cm) reads 3.5 cm and instrument B (resolution 0.01 cm) reads 3.38 cm. Which is more accurate and which is more precise?',
     'A is more accurate; B is more precise.', 'A is closer to the true value (1 mark); B has the finer resolution (1 mark).'),
    ('Why does a physics practical ask you to take several readings of the same quantity and use their mean?',
     'Random errors are equally likely to be positive or negative, so the mean of many readings is closer to the true value.', 'Random errors (1 mark); averaging reduces them (1 mark).'),
    ('In Z = A²B³/C, which quantity should be measured most carefully? Explain.',
     'B, because its relative error is multiplied by 3, the largest power.', 'ΔZ/Z = 2ΔA/A + 3ΔB/B + ΔC/C (1 mark); largest power contributes most (1 mark).'),
    ('Explain why the absolute error in a difference A − B is ΔA + ΔB and not ΔA − ΔB.',
     'In the worst case the errors act in opposite directions, so the difference can be off by ΔA + ΔB.', 'Worst-case combination (1 mark); errors never cancel in the maximum estimate (1 mark).'),
    ('Distinguish between systematic and random errors, giving one example of each.',
     'Systematic errors shift readings in one direction (e.g. zero error); random errors vary irregularly (e.g. fluctuations in reaction time).', 'Each correct definition with example, 1 mark.'),
])

c1s3_ar = pool_ar([
    ('In g = 4π²L/T², the period T should be measured more accurately than the length L.', 'The relative error in T is multiplied by 2 in the relative error of g.', 'a', 'R explains A.'),
    ('Systematic errors can be removed by taking many readings and averaging.', 'Systematic errors tend to be in one direction.', 'd', 'A is false (averaging does not remove a one-sided error); R is true.'),
    ('The percentage error in the volume of a sphere is three times the percentage error in its radius.', 'The volume of a sphere is proportional to r³.', 'a', 'ΔV/V = 3Δr/r; R explains A.'),
    ('A measurement can be precise without being accurate.', 'Precision depends on the resolution of the instrument, accuracy on closeness to the true value.', 'a', 'R explains A.'),
    ('When two lengths are subtracted, their absolute errors are subtracted.', 'Maximum errors always add.', 'd', 'A is false; R is true.'),
])


# ======================================================== ch02 Motion in a Straight Line
# st1 position, displacement, velocity

c2s1_tf = tf_mcq('motion in a straight line',
                 ['Displacement can be zero even when the path length is not zero.', 'The magnitude of displacement is never more than the path length.',
                  'Average speed is never less than the magnitude of average velocity over the same interval.', 'Instantaneous velocity is the slope of the position-time graph at that instant.',
                  'Displacement depends only on the initial and final positions.'],
                 ['Path length can be negative.', 'Average speed always equals the magnitude of average velocity.', 'Displacement is a scalar quantity.',
                  'Instantaneous speed can be different from the magnitude of instantaneous velocity.', 'A body moving at constant speed must have constant velocity even if it reverses direction.'])

c2s1_terms = term_mcq([('average speed', 'total path length ÷ total time interval'), ('average velocity', 'displacement ÷ time interval'),
                       ('instantaneous velocity', 'limit of Δx/Δt as Δt → 0'), ('displacement', 'change in position, x₂ − x₁'), ('path length', 'total length of the path actually travelled')],
                      'Which of the following defines {a}?', 'Which quantity is defined as {b}?', '{a}: {b}.')

c2s1_explain = pool_txt([
    ('A runner completes one full lap of a 400 m track. What are the path length and displacement? Explain the difference.',
     'Path length 400 m; displacement 0', 'Path length counts the whole track (1 mark); displacement is final minus initial position, which coincide (1 mark).'),
    ('Can the average speed of a body be greater than the magnitude of its average velocity? Give an example.',
     'Yes: when it changes direction, e.g. going to a shop and returning gives zero average velocity but non-zero average speed.', 'Yes with reason (1 mark), example (1 mark).'),
    ('Why do we say that the speedometer of a car shows instantaneous speed and not average speed?',
     'It shows the speed at that instant (over a very short interval), which changes from moment to moment.', 'Instantaneous = limit over very small Δt (1 mark); reading changes continuously (1 mark).'),
    ('Explain why the position-time graph of a body at rest is a straight line parallel to the time axis.',
     'x does not change with t, so the slope (velocity) is zero.', 'Constant x (1 mark); zero slope = zero velocity (1 mark).'),
])

c2s1_ar = pool_ar([
    ('A body can have zero average velocity but non-zero average speed.', 'Average velocity depends on displacement while average speed depends on path length.', 'a', 'R explains A.'),
    ('The magnitude of displacement can exceed the path length.', 'Displacement is the shortest distance between initial and final positions.', 'd', 'A is false; R is true and shows displacement ≤ path length.'),
    ('The slope of a position-time graph gives velocity.', 'Velocity is the rate of change of position with time.', 'a', 'R explains A.'),
    ('A car moving on a circular track at constant speed has constant velocity.', 'Velocity is a vector.', 'd', 'A is false because direction keeps changing; R is true.'),
])


def c2s1_walk(r):
    who = name(r)
    d1 = r.randrange(300, 1500, 50)
    d2 = r.randrange(100, d1, 50)
    t1, t2 = r.randint(5, 15), r.randint(3, 12)
    T = (t1 + t2) * 60
    return {'stem': f'{who} walks {d1} m due east to a market in {t1} min and then {d2} m due west in {t2} min. Find (i) the path length, (ii) the displacement, (iii) the average speed and (iv) the average velocity, in SI units.',
            'answer': f'(i) {d1 + d2} m (ii) {d1 - d2} m east (iii) {sig((d1 + d2) / T)} m s⁻¹ (iv) {sig((d1 - d2) / T)} m s⁻¹ east',
            'key': f'Path {d1} + {d2} = {d1 + d2} m; displacement {d1} − {d2} = {d1 - d2} m east; time {t1 + t2} min = {T} s; '
                   f'average speed {d1 + d2}/{T} = {sig((d1 + d2) / T)} m s⁻¹; average velocity {d1 - d2}/{T} = {sig((d1 - d2) / T)} m s⁻¹ east.'}


def c2s1_halves(r):
    v1, v2 = r.sample([20, 30, 40, 45, 50, 60, 72, 80, 90], 2)
    city1, city2 = r.sample(CITIES, 2)
    va = 2 * v1 * v2 / (v1 + v2)
    return NUM(f'A bus covers the first half of the distance from {city1} to {city2} at {v1} km h⁻¹ and the second half at {v2} km h⁻¹. Find its average speed for the whole journey.',
               va, 'km h⁻¹', f'Time = (d/2)/{v1} + (d/2)/{v2}; v_av = d/time = 2v₁v₂/(v₁ + v₂) = 2 × {v1} × {v2}/{v1 + v2} = {{ans}}.',
               wrongs=[(v1 + v2) / 2, math.sqrt(v1 * v2), (v1 + v2) / 2 + 5])


def c2s1_kmh(r):
    v = r.choice([18, 36, 54, 72, 90, 108, 126, 144, 45, 63])
    return NUM(f'Convert a speed of {v} km h⁻¹ into m s⁻¹.', v * 5 / 18, 'm s⁻¹', f'1 km h⁻¹ = 1000/3600 = 5/18 m s⁻¹; {v} × 5/18 = {{ans}}.',
               wrongs=[v * 18 / 5, v / 3.6 * 10, v / 36], n=3)


def c2s1_xt(r):
    a, b, c = r.randint(1, 9), r.randint(2, 12), r.choice([0.5, 1, 1.5, 2, 2.5, 3])
    t1, t2 = sorted(r.sample(range(1, 7), 2))
    x = lambda t: a + b * t + c * t * t
    vt = b + 2 * c * t2
    vav = (x(t2) - x(t1)) / (t2 - t1)
    return {'stem': f'The position of a particle moving along the x-axis is x = {a} + {b}t + {g(c) if c != 1 else ''}t² (x in metres, t in seconds). Find (i) its velocity at t = {t2} s and (ii) its average velocity between t = {t1} s and t = {t2} s.',
            'answer': f'(i) {g(vt)} m s⁻¹ (ii) {g(vav)} m s⁻¹',
            'key': f'(i) v = dx/dt = {b} + {g(2 * c)}t = {g(vt)} m s⁻¹ (1.5). (ii) x({t2}) = {g(x(t2))} m, x({t1}) = {g(x(t1))} m; v_av = {g(x(t2) - x(t1))}/{t2 - t1} = {g(vav)} m s⁻¹ (1.5).'}


def c2s1_market(r):
    who = name(r)
    d = r.choice([2.5, 3, 2, 1.5, 4])
    v1, v2 = r.choice([(5, 7.5), (4, 6), (5, 10), (6, 9), (4, 8)])
    to = d / v1 * 60
    tb = d / v2 * 60
    t = int(to + tb * r.choice([0.25, 0.4, 0.5, 0.6, 0.75]))
    if t <= to:
        raise ValueError
    back = v2 * (t - to) / 60
    path, disp = d + back, d - back
    return {'stem': f'{who} walks from home to a market {g(d)} km away at {g(v1)} km h⁻¹. Finding it closed, {who} turns back at once and walks home at {g(v2)} km h⁻¹. '
                    f'Find the magnitude of average velocity and the average speed over the interval 0 to {t} min.',
            'answer': f'Average velocity {sig(disp / (t / 60))} km h⁻¹; average speed {sig(path / (t / 60))} km h⁻¹',
            'key': f'Outward time {g(to, 1)} min. In the remaining {g(t - to, 1)} min the return distance is {g(v2)} × {g((t - to) / 60, 4)} = {g(back, 3)} km. '
                   f'Displacement {g(disp, 3)} km, path {g(path, 3)} km in {t} min = {g(t / 60, 4)} h; |v_av| = {sig(disp / (t / 60))} km h⁻¹, speed = {sig(path / (t / 60))} km h⁻¹.', 'gap': 'G7'}


def c2s1_case(r):
    s = r.randint(4, 9)
    d = [round(r.uniform(0.9, 2.2), 1) for _ in range(3)]
    tm = [r.randint(2, 4) for _ in range(3)]
    stop = 0.5
    city = r.choice(['Delhi', 'Mumbai', 'Bengaluru', 'Kolkata', 'Chennai', 'Lucknow', 'Jaipur', 'Pune'])
    tot_d, tot_t = sum(d), sum(tm) + 2 * stop
    return {'stem': (f'A {city} Metro train runs along a straight track through stations P, Q, R and S. The gaps are PQ = {d[0]} km, QR = {d[1]} km and RS = {d[2]} km. '
                     f'It takes {tm[0]} min, {tm[1]} min and {tm[2]} min for the three runs and stops for {stop} min at Q and at R.\n'
                     '(i) What is the displacement from P to S? (ii) Find the average speed from P to S in km h⁻¹. (iii) Find the average speed between P and Q in m s⁻¹. '
                     '(iv) If the train returns from S to P, what is its average velocity for the round trip?'),
            'answer': f'(i) {g(tot_d)} km (ii) {sig(tot_d / (tot_t / 60))} km h⁻¹ (iii) {sig(d[0] * 1000 / (tm[0] * 60))} m s⁻¹ (iv) zero',
            'key': f'(i) {d[0]} + {d[1]} + {d[2]} = {g(tot_d)} km (1). (ii) time = {g(tot_t)} min; {g(tot_d)}/({g(tot_t)}/60) = {sig(tot_d / (tot_t / 60))} km h⁻¹ (1). '
                   f'(iii) {g(d[0] * 1000)} m / {tm[0] * 60} s = {sig(d[0] * 1000 / (tm[0] * 60))} m s⁻¹ (1). (iv) Displacement zero, so average velocity zero (1).'}


# st2 acceleration and kinematic equations

c2s2_tf = tf_mcq('acceleration',
                 ['A body can have zero velocity and non-zero acceleration at the same instant.', 'Negative acceleration does not always mean the body is slowing down.',
                  'For uniformly accelerated motion the velocity-time graph is a straight line.', 'The area under an acceleration-time graph gives the change in velocity.'],
                 ['A body with zero velocity must have zero acceleration.', 'Negative acceleration always means the speed is decreasing.',
                  'Acceleration is always in the direction of motion.', 'For uniformly accelerated motion the position-time graph is a straight line.'])

c2s2_which_eq = pool_mcq([
    ('Which equation of uniformly accelerated motion does NOT contain the displacement x?', 'v = v₀ + at', ['x = v₀t + ½at²', 'v² = v₀² + 2ax', 'x = ½(v₀ + v)t'], 'v = v₀ + at links velocity and time only.'),
    ('Which kinematic equation should be used when the time taken is not known?', 'v² = v₀² + 2ax', ['v = v₀ + at', 'x = v₀t + ½at²', 'x = vt'], 'v² = v₀² + 2ax has no t.'),
    ('Which kinematic equation does NOT contain the final velocity v?', 'x = v₀t + ½at²', ['v = v₀ + at', 'v² = v₀² + 2ax', 'x = ½(v₀ + v)t'], 'x = v₀t + ½at² has no v.'),
    ('Which kinematic equation does NOT contain the acceleration a?', 'x = ½(v₀ + v)t', ['v = v₀ + at', 'v² = v₀² + 2ax', 'x = v₀t + ½at²'], 'Average velocity × time; no a.'),
])

c2s2_explain = pool_txt([
    ('A ball thrown up is momentarily at rest at the highest point. Is its acceleration zero there? Explain.',
     'No; its acceleration is g downwards even when its velocity is zero.', 'Velocity zero but still changing (1 mark); acceleration = g downward (1 mark).'),
    ('Give an example where the acceleration is negative but the body speeds up.',
     'A body moving in the −x direction with increasing speed, e.g. a ball falling when upward is taken as positive.', 'Sign convention (1 mark); valid example (1 mark).'),
    ('Why do the kinematic equations v = v₀ + at etc. not apply to a car in city traffic?',
     'They hold only for constant (uniform) acceleration; city traffic has continually changing acceleration.', 'Uniform acceleration condition (1 mark); application (1 mark).'),
    ('Explain why the stopping distance of a vehicle becomes four times when its initial speed is doubled (same braking).',
     'Stopping distance = v₀²/2a ∝ v₀², so doubling v₀ gives 4 times the distance.', 'v² = v₀² − 2ax with v = 0 (1 mark); x ∝ v₀² (1 mark).'),
])

c2s2_ar = pool_ar([
    ('A body can have zero velocity and still be accelerating.', 'Acceleration is the rate of change of velocity, not velocity itself.', 'a', 'R explains A (e.g. top of flight).'),
    ('The stopping distance of a car is proportional to the square of its initial speed.', 'For uniform retardation, v₀² = 2ax.', 'a', 'R explains A.'),
    ('If the acceleration is negative the body must be slowing down.', 'The sign of acceleration depends on the chosen positive direction.', 'd', 'A is false; R is true.'),
    ('The velocity-time graph for uniformly accelerated motion is a parabola.', 'v = v₀ + at.', 'd', 'A is false: v = v₀ + at is a straight line; R is true.'),
    ('The area under a velocity-time graph gives the displacement.', 'Displacement = ∫v dt.', 'a', 'R explains A.'),
])


def c2s2_vuat(r):
    u, a, t = r.choice([0, 2, 5, 8, 10, 12]), r.choice([0.5, 1.5, 2, 2.5, 3, 4]), r.randint(3, 15)
    v = u + a * t
    return NUM(f'A scooter moving at {u} m s⁻¹ accelerates uniformly at {g(a)} m s⁻² for {t} s. Find its final velocity and the distance travelled in this time.',
               v, 'm s⁻¹', f'v = u + at = {u} + {g(a)} × {t} = {g(v)} m s⁻¹; s = ut + ½at² = {g(u * t + 0.5 * a * t * t)} m.',
               wrongs=[u + 0.5 * a * t, a * t, u * t + 0.5 * a * t * t]) | {'answer': f'{g(v)} m s⁻¹; {g(u * t + 0.5 * a * t * t)} m',
                                                                          'distractors': [f'{g(u + 0.5 * a * t)} m s⁻¹; {g(u * t + a * t * t)} m', f'{g(a * t)} m s⁻¹; {g(0.5 * a * t * t)} m', f'{g(v)} m s⁻¹; {g(u * t + a * t * t)} m']}


def c2s2_brake(r):
    v = r.choice([36, 54, 72, 90, 108])
    s = r.choice([20, 25, 30, 40, 50, 60, 75])
    u = v * 5 / 18
    a = u * u / (2 * s)
    return NUM2(f'A car moving at {v} km h⁻¹ is brought to rest in {s} m by applying the brakes uniformly. Find the retardation and the time taken to stop.',
                (a, u / a), ('m s⁻²', 's'), f'u = {g(u)} m s⁻¹; 0 = u² − 2as ⇒ a = u²/2s = {g(u * u)}/{2 * s} = {sig(a)} m s⁻²; t = u/a = {sig(u / a)} s.',
                wrongs=[(u / s, s / u), (u * u / s, 2 * s / u), (v * v / (2 * s), 2 * s / v)])


def c2s2_stopping(r):
    v = r.choice([36, 54, 72, 90])
    tr = r.choice([0.5, 0.6, 0.7, 0.8, 1.0])
    a = r.choice([4, 5, 6, 7.5, 8])
    u = v * 5 / 18
    d1, d2 = u * tr, u * u / (2 * a)
    who = name(r)
    return {'stem': f'{who} is driving at {v} km h⁻¹ when a child runs onto the road. {who}\'s reaction time is {g(tr)} s and the brakes give a retardation of {g(a)} m s⁻². '
                    f'Find the total stopping distance. What would it be at {2 * v} km h⁻¹ with the same reaction time and braking?',
            'answer': f'{sig(d1 + d2)} m; at {2 * v} km h⁻¹: {sig(2 * d1 + 4 * d2)} m',
            'key': f'u = {g(u)} m s⁻¹. Reaction distance = u t_r = {g(d1)} m (1); braking distance = u²/2a = {sig(d2)} m (1); total {sig(d1 + d2)} m (1). '
                   f'Doubling u doubles the reaction distance and quadruples the braking distance: {sig(2 * d1 + 4 * d2)} m.', 'gap': 'G7'}


def c2s2_nth(r):
    u, a, n = r.choice([0, 2, 4, 5, 10]), r.choice([1, 2, 3, 4, 6]), r.randint(3, 12)
    sn = u + a * (2 * n - 1) / 2
    return NUM(f'A body starts {'from rest' if u == 0 else f'with velocity {u} m s⁻¹'} and moves with uniform acceleration {a} m s⁻². How far does it travel during the {ordn(n)} second?',
               sn, 'm', f's_n = u + (a/2)(2n − 1) = {u} + ({a}/2)({2 * n - 1}) = {{ans}}.',
               wrongs=[u * n + 0.5 * a * n * n, u + a * n / 2, u + a * (2 * n + 1) / 2], n=3)


def c2s2_catch(r):
    v = r.choice([10, 12, 15, 20])
    a = r.choice([1, 1.5, 2, 2.5, 4])
    t = 2 * v / a
    s = v * t
    who, oth = two_names(r)
    return {'stem': f'{who}\'s car waits at a traffic signal. As the light turns green, it starts with uniform acceleration {g(a)} m s⁻². At that instant {oth}\'s car passes it at a constant {v} m s⁻¹. '
                    f'When and where does {who} overtake {oth}? What is {who}\'s speed then?',
            'answer': f'After {sig(t)} s, {sig(s)} m from the signal; speed {sig(a * t)} m s⁻¹',
            'key': f'½at² = vt ⇒ t = 2v/a = {sig(t)} s (1.5); distance vt = {sig(s)} m (1); speed at = {sig(a * t)} m s⁻¹ (0.5).', 'gap': 'G7'}


def c2s2_train(r):
    a1, t1, t2, a2 = r.choice([0.5, 1, 1.5, 2]), r.randint(10, 30), r.randint(20, 90), r.choice([1, 2, 2.5, 3])
    v = a1 * t1
    t3 = v / a2
    s = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    T = t1 + t2 + t3
    return {'stem': f'A local train starts from rest and accelerates uniformly at {g(a1)} m s⁻² for {t1} s, then runs at constant speed for {t2} s and finally retards uniformly at {g(a2)} m s⁻² to stop. '
                    'Find the total distance covered and the average speed.',
            'answer': f'{sig(s)} m; {sig(s / T)} m s⁻¹',
            'key': f'Max speed {g(v)} m s⁻¹ (1); distances {g(0.5 * v * t1)} m + {g(v * t2)} m + {g(0.5 * v * t3)} m = {sig(s)} m (2); time {g(T)} s; average {sig(s / T)} m s⁻¹ (1).'}


def c2s2_two_intervals(r):
    u, a, t = r.choice([1, 2, 3, 4, 5]), r.choice([1, 2, 3, 4]), r.choice([2, 3, 4, 5])
    s1 = u * t + 0.5 * a * t * t
    s2 = (u * 2 * t + 0.5 * a * 4 * t * t) - s1
    return {'stem': f'A uniformly accelerated body covers {g(s1)} m in the first {t} s and {g(s2)} m in the next {t} s. Find its initial velocity and acceleration.',
            'answer': f'u = {u} m s⁻¹, a = {a} m s⁻²',
            'key': f'{g(s1)} = {t}u + ½a({t})²; {g(s1 + s2)} = {2 * t}u + ½a({2 * t})² (2 marks). Solving: a = (s₂ − s₁)/t² = {a} m s⁻², u = {u} m s⁻¹ (3 marks).'}


c2s2_derive = pool_txt([
    ('Derive v = v₀ + at for uniformly accelerated motion using a velocity-time graph.', 'v = v₀ + at',
     'Draw v-t straight line from v₀ (1); slope = acceleration a = (v − v₀)/t (2); rearrange (2).'),
    ('Using the velocity-time graph, derive x = v₀t + ½at² for uniformly accelerated motion.', 'x = v₀t + ½at²',
     'Area under v-t graph = displacement (1); rectangle v₀t (1) + triangle ½(v − v₀)t (1); use v − v₀ = at (2).'),
    ('Derive v² = v₀² + 2ax using the calculus method (a = v dv/dx).', 'v² = v₀² + 2ax',
     'a = dv/dt = v dv/dx (2); ∫v dv from v₀ to v = a ∫dx from 0 to x (2); ½(v² − v₀²) = ax (1).'),
    ('Derive x = v₀t + ½at² by integrating v = v₀ + at.', 'x = v₀t + ½at² (taking x₀ = 0)',
     'v = dx/dt = v₀ + at (1); dx = (v₀ + at)dt (1); integrate from 0 to t (2); result (1).'),
])


# st3 graphs and free fall

c2s3_graphs = term_mcq([('slope of a position-time graph', 'velocity'), ('slope of a velocity-time graph', 'acceleration'),
                        ('area under a velocity-time graph', 'displacement'), ('area under an acceleration-time graph', 'change in velocity')],
                       'What does the {a} represent?', 'Which feature of a motion graph gives the {b}?', 'The {a} gives the {b}.')

c2s3_tf = tf_mcq('a ball thrown vertically upward (air resistance neglected)',
                 ['Its acceleration is g downward throughout the flight.', 'Its velocity at the highest point is zero.', 'The time of ascent equals the time of descent.',
                  'It returns to the thrower\'s hand with the speed it was thrown with.'],
                 ['Its acceleration is zero at the highest point.', 'Its acceleration is upward during ascent.', 'The time of descent is greater than the time of ascent.',
                  'Its velocity-time graph is a parabola.'])

c2s3_explain = pool_txt([
    ('Why can a position-time graph never be a vertical line?', 'A vertical line would mean infinite velocity, or the body being at many positions at one instant.', 'Slope → ∞ (1 mark); impossible (1 mark).'),
    ('State Galileo\'s law of odd numbers for a body falling from rest and justify it.', 'Distances in successive equal intervals are in the ratio 1 : 3 : 5 : 7 …',
     's ∝ t² from rest (1 mark); differences of squares give odd numbers (1 mark).'),
    ('Two balls are dropped from the same height at the same time, one heavy and one light. In the absence of air resistance, which reaches first? Explain.',
     'Both together.', 'Free-fall acceleration g is the same for all bodies (1 mark); same h, same t = √(2h/g) (1 mark).'),
    ('The velocity-time graph of a ball thrown upward is a straight line crossing the time axis. What does the crossing point show and why is the slope negative?',
     'The crossing is the highest point (v = 0); slope = −g because acceleration is downward.', 'Each point 1 mark.'),
])

c2s3_ar = pool_ar([
    ('The velocity of a ball thrown up is zero at its highest point, but its acceleration is not.', 'Gravity acts on the ball throughout its motion.', 'a', 'R explains A.'),
    ('A body falling freely from rest covers distances in the ratio 1 : 3 : 5 in successive equal intervals.', 'For free fall from rest, distance ∝ t².', 'a', 'R explains A.'),
    ('In the absence of air, a feather and a coin dropped together reach the ground together.', 'The acceleration due to gravity is independent of the mass of the body.', 'a', 'R explains A.'),
    ('The velocity-time graph of a freely falling body has zero slope.', 'The acceleration of a freely falling body is constant.', 'd', 'A is false (slope = g); R is true.'),
    ('A ball thrown up takes longer to come down than to go up (no air resistance).', 'The ball\'s acceleration is the same during ascent and descent.', 'd', 'A is false: times are equal; R is true.'),
])


def c2s3_drop(r):
    h = r.choice([5, 10, 19.6, 20, 30, 44.1, 45, 80, 122.5])
    t = math.sqrt(2 * h / G)
    v = G * t
    place = r.choice(['the top of a building', 'a bridge over the Yamuna', 'the roof of the school', 'a cliff at Lonavala', 'a water tank'])
    return NUM2(f'A stone is dropped from {place} {g(h)} m high. Find the time taken to reach the ground and the speed on reaching it. (g = 9.8 m s⁻²; neglect air resistance)',
                (t, v), ('s', 'm s⁻¹'), f'h = ½gt² ⇒ t = √(2h/g) = √(2 × {g(h)}/9.8) = {sig(t)} s; v = gt = {sig(v)} m s⁻¹.',
                wrongs=[(math.sqrt(h / G), G * math.sqrt(h / G)), (2 * h / G, G * 2 * h / G), (t, G * h)])


def c2s3_up(r):
    u = r.choice([9.8, 14.7, 19.6, 24.5, 29.4, 10, 15, 20, 25])
    H, T = u * u / (2 * G), 2 * u / G
    return NUM2(f'A ball is thrown vertically upward with a speed of {g(u)} m s⁻¹. Find the maximum height it reaches and the time after which it returns to the thrower\'s hand. (g = 9.8 m s⁻²)',
                (H, T), ('m', 's'), f'H = u²/2g = {g(u * u)}/19.6 = {sig(H)} m; T = 2u/g = {sig(T)} s.',
                wrongs=[(u * u / G, u / G), (H, u / G), (2 * H, T)])


def c2s3_tower(r):
    h = r.choice([20, 25, 30, 40, 50, 60])
    u = r.choice([10, 15, 20])
    g_ = 10
    t = (u + math.sqrt(u * u + 2 * g_ * h)) / g_
    return {'stem': f'A ball is thrown vertically upward with a velocity of {u} m s⁻¹ from the top of a multistorey building {h} m high. Taking g = 10 m s⁻², '
                    '(i) how high above the ground will it rise, and (ii) how long after being thrown will it hit the ground?',
            'answer': f'(i) {g(h + u * u / 20)} m (ii) {sig(t)} s',
            'key': f'(i) rise above top = u²/2g = {g(u * u / 20)} m, so {g(h + u * u / 20)} m above ground (1.5). (ii) take up as +: −{h} = {u}t − 5t² ⇒ 5t² − {u}t − {h} = 0 ⇒ t = {sig(t)} s (rejecting the negative root) (1.5).'}


def c2s3_vt_area(r):
    v = r.choice([10, 12, 15, 20, 24, 30])
    t1, t2, t3 = r.randint(2, 8), r.randint(4, 15), r.randint(2, 8)
    s = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    T = t1 + t2 + t3
    return {'stem': f'The velocity-time graph of a car rises in a straight line from 0 to {v} m s⁻¹ in {t1} s, stays at {v} m s⁻¹ for the next {t2} s and then falls in a straight line to zero in {t3} s. '
                    'Find (i) the acceleration in the first part, (ii) the total distance and (iii) the average speed.',
            'answer': f'(i) {sig(v / t1)} m s⁻² (ii) {g(s)} m (iii) {sig(s / T)} m s⁻¹',
            'key': f'(i) slope {v}/{t1} = {sig(v / t1)} m s⁻² (1). (ii) area = ½·{v}·{t1} + {v}·{t2} + ½·{v}·{t3} = {g(s)} m (1.5). (iii) {g(s)}/{T} = {sig(s / T)} m s⁻¹ (0.5).'}


def c2s3_rect(r):
    v, t = r.randint(3, 25), r.randint(4, 20)
    return NUM(f'The velocity-time graph of a cyclist is a horizontal line at {v} m s⁻¹ from t = 0 to t = {t} s. How far does the cyclist travel?', v * t, 'm',
               f'Area under the v-t graph = {v} × {t} = {{ans}}.', wrongs=[v / t, 0.5 * v * t, v + t])


def c2s3_balloon(r):
    u = r.choice([5, 8, 10, 12, 15])
    h = r.choice([40, 60, 80, 100, 120])
    g_ = 9.8
    t = (u + math.sqrt(u * u + 2 * g_ * h)) / g_
    return {'stem': f'A balloon is rising vertically at a steady {u} m s⁻¹. When it is {h} m above the ground, a packet is released from it. Find the time taken by the packet to reach the ground and its speed on hitting the ground. (g = 9.8 m s⁻²)',
            'answer': f'{sig(t)} s; {sig(math.sqrt(u * u + 2 * g_ * h))} m s⁻¹',
            'key': f'The packet starts with the balloon\'s velocity {u} m s⁻¹ upward (1). −{h} = {u}t − 4.9t² ⇒ t = {sig(t)} s (2). v² = u² + 2gh ⇒ v = {sig(math.sqrt(u * u + 2 * g_ * h))} m s⁻¹ (1).', 'gap': 'G5'}


def c2s3_nth_fall(r):
    n = r.randint(2, 9)
    d = G * (2 * n - 1) / 2
    return {'stem': f'A body falls freely from rest. How far does it fall during the {ordn(n)} second? (g = 9.8 m s⁻²) What is the ratio of this to the distance fallen in the 1st second?',
            'answer': f'{sig(d)} m; {2 * n - 1} : 1', 'key': f's_n = (g/2)(2n − 1) = 4.9 × {2 * n - 1} = {sig(d)} m; ratio {2 * n - 1} : 1 (Galileo\'s law of odd numbers).',
            'distractors': [f'{sig(0.5 * G * n * n)} m; {n * n} : 1', f'{sig(G * n)} m; {2 * n} : 1', f'{sig(0.5 * G * (2 * n + 1))} m; {2 * n + 1} : 1']}


def c2s3_case(r):
    who = name(r)
    u = r.choice([14.7, 19.6, 24.5, 9.8])
    return {'stem': (f'During a school sports day, {who} tosses a cricket ball vertically upward with a speed of {g(u)} m s⁻¹ and catches it at the same height. Take g = 9.8 m s⁻² and upward as positive.\n'
                     '(i) What is the velocity of the ball at the highest point? (ii) Find the maximum height. (iii) Find the total time in the air. (iv) What is the acceleration of the ball at the highest point?'),
            'answer': f'(i) 0 (ii) {sig(u * u / (2 * G))} m (iii) {sig(2 * u / G)} s (iv) 9.8 m s⁻² downward',
            'key': f'(i) 0 (1). (ii) u²/2g = {sig(u * u / (2 * G))} m (1). (iii) 2u/g = {sig(2 * u / G)} s (1). (iv) −9.8 m s⁻², i.e. g downward (1).'}


# st4 relative velocity in one dimension

c2s4_tf = tf_mcq('relative velocity in one dimension',
                 ['The velocity of A relative to B is v_A − v_B.', 'v_AB = −v_BA.', 'Two bodies moving with equal velocities appear at rest relative to each other.',
                  'For bodies moving in opposite directions, the magnitude of relative velocity is the sum of their speeds.'],
                 ['The velocity of A relative to B is v_A + v_B for bodies moving in the same direction.', 'v_AB = v_BA.',
                  'Relative velocity is always greater than the velocity of either body.', 'Two bodies with equal velocities have relative velocity 2v.'])

c2s4_explain = pool_txt([
    ('Two trains run on parallel tracks in the same direction at the same speed. Describe how a passenger in one sees the other.', 'The other train appears to be at rest.',
     'v_AB = v_A − v_B = 0 (1 mark); positions do not change relative to each other (1 mark).'),
    ('Why does a train coming from the opposite direction seem to pass much faster than one overtaking you?',
     'In opposite directions the relative speed is the sum of the speeds; in the same direction it is the difference.', 'Each case 1 mark.'),
    ('Show that the position-time graphs of two bodies moving with equal velocities are parallel straight lines.',
     'Both have the same slope, so the gap x_B − x_A stays constant.', 'Slope = velocity (1 mark); constant separation (1 mark).'),
])

c2s4_ar = pool_ar([
    ('A passenger in a train moving at 60 km h⁻¹ sees a parallel train moving at 60 km h⁻¹ in the same direction as stationary.', 'Their relative velocity is zero.', 'a', 'R explains A.'),
    ('The relative velocity of two bodies moving in opposite directions is the difference of their speeds.', 'Relative velocity v_AB = v_A − v_B.', 'd', 'A is false: with opposite signs the magnitudes add; R is true.'),
    ('v_AB = −v_BA.', 'Relative velocity depends on the frame from which it is observed.', 'b', 'Both true, but R does not explain the sign relation.'),
])


def c2s4_rel(r):
    v1, v2 = r.sample([36, 45, 54, 60, 72, 80, 90, 108], 2)
    same = r.random() < 0.5
    rel = abs(v1 - v2) if same else v1 + v2
    return NUM(f'Two cars move on a straight highway {"in the same direction" if same else "towards each other"} at {v1} km h⁻¹ and {v2} km h⁻¹. What is the magnitude of the velocity of one relative to the other?',
               rel, 'km h⁻¹', f'{"Same direction: |v₁ − v₂|" if same else "Opposite directions: v₁ + v₂"} = {{ans}}.',
               wrongs=[v1 + v2 if same else abs(v1 - v2), (v1 + v2) / 2, max(v1, v2)])


def c2s4_cross(r):
    L1, L2 = r.choice([100, 120, 150, 200, 250]), r.choice([100, 150, 180, 200, 300])
    v1, v2 = r.sample([36, 45, 54, 72, 90], 2)
    same = r.random() < 0.5
    rel = abs(v1 - v2) * 5 / 18 if same else (v1 + v2) * 5 / 18
    t = (L1 + L2) / rel
    return NUM(f'Two trains of lengths {L1} m and {L2} m run on parallel tracks {"in the same direction" if same else "in opposite directions"} at {v1} km h⁻¹ and {v2} km h⁻¹. '
               f'How long do they take to {"pass each other completely (the faster overtaking the slower)" if same else "cross each other"}?',
               t, 's', f'Relative speed = {g(rel)} m s⁻¹; distance to cover = {L1} + {L2} = {L1 + L2} m; t = {L1 + L2}/{g(rel)} = {{ans}}.',
               wrongs=[max(L1, L2) / rel, (L1 + L2) / ((v1 + v2) * 5 / 18 if same else abs(v1 - v2) * 5 / 18), (L1 + L2) / rel / 3.6], gap='G7')


def c2s4_chase(r):
    d = r.choice([200, 300, 400, 500, 800, 1000])
    vt, vp = r.choice([(54, 72), (60, 90), (72, 108), (45, 72), (36, 54)])
    rel = (vp - vt) * 5 / 18
    t = d / rel
    return {'stem': f'A police jeep is chasing a speeding car on a straight highway. The car moves at {vt} km h⁻¹ and the jeep at {vp} km h⁻¹; initially the jeep is {d} m behind. '
                    'How long does the jeep take to catch the car, and how far does the car travel in that time?',
            'answer': f'{sig(t)} s; {sig(vt * 5 / 18 * t)} m',
            'key': f'Relative speed ({vp} − {vt}) km h⁻¹ = {g(rel)} m s⁻¹ (1); t = {d}/{g(rel)} = {sig(t)} s (1); car moves {g(vt * 5 / 18)} × {sig(t)} = {sig(vt * 5 / 18 * t)} m (1).', 'gap': 'G7'}


def c2s4_simple(r):
    va, vb = r.randint(5, 30), r.randint(5, 30)
    if va == vb:
        vb += 3
    return NUM(f'Two cyclists ride along a straight road in the same direction. A moves at {va} m s⁻¹ and B at {vb} m s⁻¹. What is the velocity of B relative to A?', vb - va,
               'm s⁻¹', f'v_BA = v_B − v_A = {vb} − {va} = {{ans}} ({"ahead" if vb > va else "falling behind"}).', wrongs=[va - vb, va + vb, vb], n=2)


# ======================================================== ch03 Motion in a Plane
# st1 vectors

VEC = ['displacement', 'velocity', 'acceleration', 'force', 'momentum', 'impulse', 'torque', 'electric field', 'weight']
SCA = ['mass', 'speed', 'distance', 'work', 'energy', 'power', 'temperature', 'time', 'volume', 'density', 'pressure', 'electric charge']


def c3s1_classify(r):
    if r.random() < 0.5:
        c = r.choice(VEC)
        return mcq('Which of the following is a vector quantity?', c, r.sample(SCA, 3), f'{c.capitalize()} has both magnitude and direction; the others are scalars.', r)
    c = r.choice(SCA)
    return mcq('Which of the following is a scalar quantity?', c, r.sample(VEC, 3), f'{c.capitalize()} has magnitude only; the others are vectors.', r)


c3s1_tf = tf_mcq('vectors',
                 ['A unit vector has magnitude 1 and no units.', 'Vector addition is commutative: A + B = B + A.', 'The magnitude of A + B can never exceed |A| + |B|.',
                  'A null vector has zero magnitude.', 'Subtracting B is the same as adding −B.'],
                 ['The magnitude of A + B is always |A| + |B|.', 'A unit vector has the unit of the quantity it represents.', 'Two vectors of unequal magnitudes can add to give zero.',
                  'Vector addition is not commutative.', 'Multiplying a vector by a negative number does not change its direction.'])

c3s1_explain = pool_txt([
    ('Can three vectors of magnitudes 2, 3 and 7 units add to give zero? Explain.', 'No.', 'For zero resultant they must form a triangle; 2 + 3 < 7, so no triangle (2 marks).'),
    ('Explain why two vectors of unequal magnitudes cannot give a zero resultant.', 'Zero resultant needs equal magnitudes in opposite directions.', 'Minimum |A + B| = | |A| − |B| | > 0 (2 marks).'),
    ('State the parallelogram law of vector addition.', 'If two vectors are represented by two adjacent sides of a parallelogram from a common point, the diagonal from that point represents their resultant.', 'Correct statement (2 marks).'),
    ('Why is the time interval a scalar even though it can be "positive" or "negative"?', 'A scalar can have a sign; the sign is not a direction in space.', 'Scalars have magnitude only (1 mark); sign ≠ spatial direction (1 mark).'),
])

c3s1_ar = pool_ar([
    ('The magnitude of the resultant of two vectors lies between |A − B| and A + B.', 'The resultant is largest when the vectors are parallel and smallest when antiparallel.', 'a', 'R explains A.'),
    ('A vector can have zero magnitude.', 'A null vector has zero magnitude and arbitrary direction.', 'a', 'R explains A.'),
    ('Mass is a vector quantity.', 'Mass has magnitude and obeys the laws of algebra.', 'd', 'A is false (mass is a scalar); R is true.'),
    ('Three vectors of magnitudes 4, 5 and 10 units can give zero resultant.', 'The resultant is zero only if the vectors can form a closed triangle.', 'd', 'A is false: 4 + 5 < 10; R is true.'),
])


def c3s1_resultant(r):
    A, B = r.randint(3, 15), r.randint(3, 15)
    th = r.choice([30, 45, 60, 90, 120, 135, 150])
    t = math.radians(th)
    R = math.sqrt(A * A + B * B + 2 * A * B * math.cos(t))
    al = math.degrees(math.atan2(B * math.sin(t), A + B * math.cos(t)))
    R2 = math.sqrt(A * A + B * B)
    return NUM2(f'Two forces of {A} N and {B} N act on a body with an angle of {th}° between them. Find the magnitude of the resultant and its angle with the {A} N force.',
                (R, al), ('N', '°'), f'R = √(A² + B² + 2AB cos θ) = √({A * A} + {B * B} + {g(2 * A * B * math.cos(t))}) = {sig(R)} N; tan α = B sin θ/(A + B cos θ) ⇒ α = {sig(al)}°.',
                wrongs=[(A + B, th / 2), (R2, math.degrees(math.atan2(B, A))), (math.sqrt(abs(A * A + B * B - 2 * A * B * math.cos(t))), al)], sep=' at an angle of ')


def c3s1_resolve(r):
    A = r.choice([10, 20, 25, 40, 50, 100])
    th = r.choice([30, 37, 45, 53, 60])
    t = math.radians(th)
    return {'stem': f'A force of {A} N acts at {th}° to the positive x-axis in the x-y plane. Find its x- and y-components.',
            'answer': f'Fx = {sig(A * math.cos(t))} N, Fy = {sig(A * math.sin(t))} N',
            'key': f'Fx = F cos θ = {A} cos {th}° = {sig(A * math.cos(t))} N; Fy = F sin θ = {sig(A * math.sin(t))} N.',
            'distractors': [f'Fx = {sig(A * math.sin(t))} N, Fy = {sig(A * math.cos(t))} N', f'Fx = {sig(A / math.cos(t))} N, Fy = {sig(A / math.sin(t))} N', f'Fx = {sig(A * math.cos(t) / 2)} N, Fy = {sig(A * math.sin(t) / 2)} N']}


def c3s1_ijk(r):
    a = [r.randint(-6, 8) for _ in range(2)]
    b = [r.randint(-6, 8) for _ in range(2)]
    c = [r.randint(-6, 8) for _ in range(2)]
    s = [a[i] + b[i] + c[i] for i in range(2)]
    if s == [0, 0]:
        s = [1, 1]
        c[0] += 1
        c[1] += 1
    mag = math.hypot(*s)
    ang = math.degrees(math.atan2(s[1], s[0]))

    def v(x):
        return f'{x[0]}î {"+" if x[1] >= 0 else "−"} {abs(x[1])}ĵ'.replace('-', '−')
    return {'stem': f'Three displacements are A = ({v(a)}) m, B = ({v(b)}) m and C = ({v(c)}) m. Find the resultant displacement, its magnitude and the angle it makes with the x-axis.',
            'answer': f'R = ({v(s)}) m; |R| = {sig(mag)} m; {num(ang, 1)}° with +x-axis',
            'key': f'Add components: Rx = {num(s[0])}, Ry = {num(s[1])} (1); |R| = √({s[0] ** 2} + {s[1] ** 2}) = {sig(mag)} m (1); θ = tan⁻¹(Ry/Rx) taking quadrant into account = {num(ang, 1)}° (1).'}


def c3s1_equal_mag(r):
    a = r.randint(4, 20)
    R = r.choice([0.5, 1, 1.2, 1.414, 1.6, 1.732]) * a
    th = 2 * math.degrees(math.acos(R / (2 * a)))
    return NUM(f'Two vectors, each of magnitude {a} units, have a resultant of magnitude {g(R, 2)} units. Find the angle between them.', th, '°',
               f'R² = 2a²(1 + cos θ) ⇒ cos θ = R²/(2a²) − 1 = {g(R * R / (2 * a * a) - 1, 3)} ⇒ θ = {{ans}}.'.replace(' °', '°'),
               wrongs=[180 - th, th / 2, 90 + th / 4])


def c3s1_walk(r):
    who = name(r)
    d1, d2, d3 = r.randint(2, 9) * 50, r.randint(2, 9) * 50, r.randint(1, 6) * 50
    th = r.choice([30, 45, 60])
    t = math.radians(th)
    x = d2 * math.sin(t) - d3
    y = d1 + d2 * math.cos(t)
    if abs(x) < 5:
        raise ValueError
    mag = math.hypot(x, y)
    ang = math.degrees(math.atan2(x, y))
    return {'stem': f'{who} walks {d1} m north, then {d2} m in a direction {th}° east of north, and finally {d3} m west. Find the magnitude and direction of the resultant displacement.',
            'answer': f'{sig(mag)} m, {num(abs(ang), 1)}° {"east" if ang >= 0 else "west"} of north',
            'key': f'Take x east, y north: x = {d2} sin {th}° − {d3} = {g(x, 2)} m; y = {d1} + {d2} cos {th}° = {g(y, 2)} m (2); magnitude √(x² + y²) = {sig(mag)} m (1); direction tan⁻¹(|x|/y) = {num(abs(ang), 1)}° {"east" if ang >= 0 else "west"} of north (1).', 'gap': 'G7'}


def c3s1_range(r):
    A, B = r.sample(range(3, 16), 2)
    lo, hi = abs(A - B), A + B
    bad = r.choice([hi + r.randint(1, 5), max(0, lo - r.randint(1, lo)) if lo > 1 else hi + 2])
    ok = r.sample(range(lo, hi + 1), 3)
    if bad in ok:
        bad = hi + 3
    return mcq(f'Two forces of {A} N and {B} N act at a point. Which of the following CANNOT be the magnitude of their resultant?', f'{bad} N', [f'{o} N' for o in ok],
               f'The resultant lies between |{A} − {B}| = {lo} N and {A} + {B} = {hi} N; {bad} N is outside this range.', r)


def c3s1_unit(r):
    a, b, c = [r.choice([1, 2, 3, 4, 6, -2, -3]) for _ in range(3)]
    m = math.sqrt(a * a + b * b + c * c)

    def s(x, u, first=False):
        if first:
            return f'{x}{u}'.replace('-', '−')
        return f' {"+" if x >= 0 else "−"} {abs(x)}{u}'
    v = s(a, 'î', True) + s(b, 'ĵ') + s(c, 'k̂')
    return {'stem': f'Find the magnitude of the vector A = {v} and the unit vector along A.', 'answer': f'|A| = {sig(m)}; Â = ({v})/{sig(m)}',
            'key': f'|A| = √({a * a} + {b * b} + {c * c}) = √{a * a + b * b + c * c} = {sig(m)} (1); Â = A/|A| (1).'}


# st2 motion in a plane with constant acceleration; relative velocity in 2D

c3s2_tf = tf_mcq('motion in a plane',
                 ['Motion in a plane with constant acceleration can be treated as two independent one-dimensional motions.', 'The velocity of a particle is always along the tangent to its path.',
                  'Rain falling vertically appears slanted to a person walking in the rain.', 'The relative velocity of A with respect to B is v_A − v_B.'],
                 ['The velocity of a particle is always along the acceleration.', 'A swimmer heading perpendicular to the current reaches the point directly opposite.',
                  'The x and y motions of a projectile affect each other.', 'Relative velocity in two dimensions is found by adding the magnitudes of the two velocities.'])

c3s2_explain = pool_txt([
    ('Why must a person walking fast in vertical rain hold the umbrella tilted forward?', 'Relative to the person the rain comes at an angle from the front, so the umbrella must face that direction.',
     'v_rain,person = v_rain − v_person points forward-downward (1 mark); tilt forward (1 mark).'),
    ('A boat heads straight across a flowing river. Does it land directly opposite? Explain.', 'No; the current carries it downstream while it crosses.', 'Resultant velocity is the vector sum (1 mark); drift downstream (1 mark).'),
    ('Explain why the time to cross a river is least when the boat heads perpendicular to the bank.', 'Only the component across the river matters for crossing time; it is largest (the full boat speed) when heading perpendicular.',
     'Crossing time = width / perpendicular component (1 mark); maximum at 90° (1 mark).'),
])

c3s2_ar = pool_ar([
    ('A swimmer who heads perpendicular to the current crosses the river in the least time.', 'The current does not change the velocity component perpendicular to the bank.', 'a', 'R explains A.'),
    ('To reach the point directly opposite, a boat must head upstream.', 'Its velocity component along the stream must cancel the river velocity.', 'a', 'R explains A.'),
    ('A person in a car moving at constant velocity sees vertical rain as slanted.', 'Relative velocity of rain with respect to the car is v_rain − v_car.', 'a', 'R explains A.'),
    ('In two-dimensional motion with constant acceleration, the path is always a straight line.', 'Motion in x and y can be treated independently.', 'd', 'A is false (a projectile\'s path is a parabola); R is true.'),
])


def c3s2_umbrella(r):
    vr, vm = r.choice([(30, 10), (35, 12), (20, 5), (15, 5), (25, 8), (30, 15)])
    th = math.degrees(math.atan(vm / vr))
    who = name(r)
    return NUM(f'Rain is falling vertically at {vr} m s⁻¹. {who} rides a bicycle due east at {vm} m s⁻¹. In which direction should {who} hold the umbrella?', th, '°',
               f'Relative velocity of rain = v_r − v_m; tan θ = v_m/v_r = {vm}/{vr} ⇒ θ = {{ans}} from the vertical, towards the east (front).'.replace(' °', '°'),
               wrongs=[90 - th, math.degrees(math.atan(vr / vm)) / 2, th * 2]) | {'answer': f'{sig(th)}° from the vertical, tilted forward (towards the east)',
                                                                                   'distractors': [f'{sig(90 - th)}° from the vertical, tilted forward', f'{sig(th)}° from the vertical, tilted backward', 'vertically upward']}


def c3s2_river(r):
    w = r.choice([200, 300, 400, 500, 600, 1000])
    vb, vr = r.choice([(4, 3), (5, 2), (2, 1.5), (3, 1), (6, 4), (5, 3)])
    t = w / vb
    return {'stem': f'A boat can move at {g(vb)} m s⁻¹ in still water. It heads perpendicular to the bank of a river {w} m wide flowing at {g(vr)} m s⁻¹. Find the time to cross and how far downstream it lands.',
            'answer': f'{sig(t)} s; {sig(vr * t)} m downstream', 'key': f't = width/v_b = {w}/{g(vb)} = {sig(t)} s; drift = v_r t = {g(vr)} × {sig(t)} = {sig(vr * t)} m.',
            'distractors': [f'{sig(w / math.hypot(vb, vr))} s; {sig(vr * w / math.hypot(vb, vr))} m downstream', f'{sig(w / (vb - vr))} s; 0 m downstream', f'{sig(t)} s; {sig(vb * t)} m downstream']}


def c3s2_straight(r):
    w = r.choice([200, 300, 400, 500, 800])
    vb, vr = r.choice([(5, 3), (10, 6), (2.5, 1.5), (5, 4), (4, 2), (6, 3)])
    th = math.degrees(math.asin(vr / vb))
    t = w / math.sqrt(vb * vb - vr * vr)
    return {'stem': f'A swimmer can swim at {g(vb)} m s⁻¹ in still water. A river {w} m wide flows at {g(vr)} m s⁻¹. In which direction must the swimmer head to reach the point directly opposite, and how long will it take?',
            'answer': f'{sig(th)}° upstream from the perpendicular; {sig(t)} s',
            'key': f'Along-stream component cancels: v_b sin θ = v_r ⇒ sin θ = {g(vr)}/{g(vb)} ⇒ θ = {sig(th)}° (1.5); across speed √(v_b² − v_r²) = {sig(math.sqrt(vb * vb - vr * vr))} m s⁻¹; t = {sig(t)} s (1.5).'}


def c3s2_rt(r):
    a, b, t = r.randint(2, 9), r.choice([0.5, 1, 1.5, 2, 3]), r.randint(1, 5)
    vx, vy = a, 2 * b * t
    return {'stem': f'The position of a particle is r = {a}t î + {g(b)}t² ĵ (in metres, t in seconds). Find its velocity and acceleration at t = {t} s, and the speed at that instant.',
            'answer': f'v = {a}î + {g(vy)}ĵ m s⁻¹; a = {g(2 * b)}ĵ m s⁻²; speed {sig(math.hypot(vx, vy))} m s⁻¹',
            'key': f'v = dr/dt = {a}î + {g(2 * b)}t ĵ → {a}î + {g(vy)}ĵ (1); a = dv/dt = {g(2 * b)}ĵ (1); |v| = √({a * a} + {g(vy * vy)}) = {sig(math.hypot(vx, vy))} m s⁻¹ (1).'}


def c3s2_r0(r):
    v0 = r.randint(2, 12)
    ax, ay = r.choice([0, 1, 2, 3]), r.choice([1, 2, 3, 4, 5])
    t = r.randint(2, 6)
    x, y = v0 * t + 0.5 * ax * t * t, 0.5 * ay * t * t
    vx, vy = v0 + ax * t, ay * t
    return {'stem': f'A particle starts from the origin at t = 0 with velocity {v0}î m s⁻¹ and moves in the x-y plane with a constant acceleration ({ax}î + {ay}ĵ) m s⁻². Find its position and speed at t = {t} s.',
            'answer': f'r = ({g(x)}î + {g(y)}ĵ) m; speed {sig(math.hypot(vx, vy))} m s⁻¹',
            'key': f'r = v₀t + ½at²: x = {v0}×{t} + ½×{ax}×{t * t} = {g(x)} m, y = ½×{ay}×{t * t} = {g(y)} m (2); v = v₀ + at = {g(vx)}î + {g(vy)}ĵ; speed {sig(math.hypot(vx, vy))} m s⁻¹ (2).'}


def c3s2_relform(r):
    return pool_mcq([
        ('If the velocities of two objects A and B are v_A and v_B, the velocity of A relative to B is', 'v_A − v_B', ['v_A + v_B', 'v_B − v_A', '(v_A + v_B)/2'], 'v_AB = v_A − v_B.'),
        ('The velocity of B relative to A, v_BA, is related to v_AB by', 'v_BA = −v_AB', ['v_BA = v_AB', 'v_BA = 2v_AB', 'v_BA = v_AB/2'], 'Reversing the observer reverses the relative velocity.'),
        ('A person in a car moving east at 15 m s⁻¹ sees rain falling vertically. Relative to the ground, the rain', 'has a horizontal component of 15 m s⁻¹ towards the east', ['falls vertically', 'has a horizontal component of 15 m s⁻¹ towards the west', 'is at rest'], 'v_rain = v_rain,car + v_car.'),
    ])(r)


# st3 projectile motion

c3s3_formula = term_mcq([('time of flight', '2u sin θ / g'), ('maximum height', 'u² sin²θ / 2g'), ('horizontal range', 'u² sin 2θ / g'), ('maximum horizontal range', 'u²/g (at θ = 45°)')],
                        'For a projectile launched with speed u at angle θ to the horizontal, the {a} is', 'For a projectile launched with speed u at angle θ, which quantity equals {b}?', 'The {a} = {b}.')

c3s3_tf = tf_mcq('projectile motion (air resistance neglected)',
                 ['The horizontal component of velocity remains constant.', 'At the highest point the velocity is horizontal.', 'The range is maximum for a launch angle of 45°.',
                  'Launch angles θ and (90° − θ) give the same range.', 'The path is a parabola.'],
                 ['The velocity at the highest point is zero.', 'The vertical component of velocity remains constant.', 'The range is maximum for a launch angle of 60°.',
                  'The acceleration changes direction at the highest point.', 'The horizontal and vertical motions depend on each other.'])

c3s3_explain = pool_txt([
    ('Why is the velocity of a projectile at the top of its path not zero?', 'Only the vertical component becomes zero; the horizontal component u cos θ remains.', 'Two components (1 mark); horizontal constant (1 mark).'),
    ('Show that the ranges for launch angles θ and (90° − θ) are equal.', 'sin 2(90° − θ) = sin(180° − 2θ) = sin 2θ, so R is the same.', 'Use R = u² sin 2θ/g (1 mark); identity (1 mark).'),
    ('Two balls are released together from the same height: one dropped, one thrown horizontally. Which lands first? Explain.', 'They land together.', 'Vertical motion is identical (initial vertical velocity 0, acceleration g) (2 marks).'),
    ('Why does a long jumper try to take off at nearly 45°?', 'For a given take-off speed the horizontal range u² sin 2θ/g is greatest when sin 2θ = 1, i.e. θ = 45°.', 'Range formula (1 mark); maximum at 45° (1 mark).'),
])

c3s3_ar = pool_ar([
    ('At the highest point of its path, a projectile has zero velocity.', 'At the highest point the vertical component of velocity is zero.', 'd', 'A is false (the horizontal component remains); R is true.'),
    ('Projectiles launched at 30° and 60° with the same speed have the same range.', 'Range depends on sin 2θ, and sin 60° = sin 120°.', 'a', 'R explains A.'),
    ('The horizontal velocity of a projectile is constant.', 'There is no horizontal acceleration when air resistance is neglected.', 'a', 'R explains A.'),
    ('The trajectory of a projectile is a parabola.', 'y depends linearly on x and quadratically on x² in y = x tan θ − gx²/(2u² cos² θ).', 'a', 'The equation of trajectory is of the form y = ax − bx², a parabola.'),
    ('A ball dropped and a ball thrown horizontally from the same height land at different times.', 'Both have the same vertical motion.', 'd', 'A is false; R is true.'),
])


def c3s3_thr(r):
    u = r.choice([10, 15, 20, 25, 30, 40])
    th = r.choice([15, 30, 37, 45, 53, 60, 75])
    t = math.radians(th)
    T, H, R = 2 * u * math.sin(t) / G, (u * math.sin(t)) ** 2 / (2 * G), u * u * math.sin(2 * t) / G
    return {'stem': f'A ball is projected with a speed of {u} m s⁻¹ at {th}° to the horizontal. Find its time of flight, maximum height and horizontal range. (g = 9.8 m s⁻²)',
            'answer': f'T = {sig(T)} s, H = {sig(H)} m, R = {sig(R)} m',
            'key': f'T = 2u sin θ/g = {sig(T)} s; H = u² sin²θ/2g = {sig(H)} m; R = u² sin 2θ/g = {sig(R)} m.',
            'distractors': [f'T = {sig(T / 2)} s, H = {sig(H)} m, R = {sig(R / 2)} m', f'T = {sig(T)} s, H = {sig(2 * H)} m, R = {sig(R)} m', f'T = {sig(2 * u * math.cos(t) / G)} s, H = {sig((u * math.cos(t)) ** 2 / (2 * G))} m, R = {sig(R)} m']}


def c3s3_horiz(r):
    h = r.choice([4.9, 19.6, 44.1, 78.4, 20, 45, 80, 125])
    u = r.choice([5, 8, 10, 12, 15, 20, 25])
    t = math.sqrt(2 * h / G)
    ctx = r.choice(['from the edge of a cliff', 'from the top of a tower', 'off a table top' if h < 5 else 'from the roof of a building'])
    return NUM(f'A stone is thrown horizontally with a speed of {u} m s⁻¹ {ctx} {g(h)} m high. How far from the foot does it land? (g = 9.8 m s⁻²)',
               u * t, 'm', f't = √(2h/g) = {sig(t)} s (vertical motion); x = ut = {u} × {sig(t)} = {{ans}}.', wrongs=[u * 2 * h / G, u * u / G, u * t / 2])


def c3s3_angle_for_range(r):
    u = r.choice([20, 25, 30, 40, 50])
    Rmax = u * u / G
    R = round(Rmax * r.choice([0.5, 0.6, 0.7, 0.8, 0.866, 0.9]), 1)
    s2 = R * G / (u * u)
    t1 = math.degrees(math.asin(s2)) / 2
    return {'stem': f'A fielder throws a ball at {u} m s⁻¹. At what angles to the horizontal can it be thrown to land {g(R)} m away on level ground? (g = 9.8 m s⁻²)',
            'answer': f'{num(t1, 1)}° or {num(90 - t1, 1)}°',
            'key': f'sin 2θ = Rg/u² = {g(R)} × 9.8/{u * u} = {s2:.3f} (1.5); 2θ = {num(2 * t1, 1)}° or {num(180 - 2 * t1, 1)}°; θ = {num(t1, 1)}° or {num(90 - t1, 1)}° (complementary angles) (1.5).'}


def c3s3_ratio(r):
    k = r.choice([1, 2, 4, 4 * math.sqrt(3), 4 / math.sqrt(3), 8])
    th = math.degrees(math.atan(4 / k))
    ks = {1: '', 2: '2', 4: '4', 8: '8'}.get(k, '4√3' if abs(k - 4 * math.sqrt(3)) < 1e-9 else '(4/√3)')
    return NUM(f'For a projectile, the horizontal range is {ks + " times" if ks else "equal to"} the maximum height. Find the angle of projection.'.replace('  ', ' '),
               th, '°', f'H/R = tan θ/4 ⇒ tan θ = 4H/R = 4/{ks or 1} ⇒ θ = {{ans}}.'.replace(' °', '°'), wrongs=[90 - th, th / 2, 45.0 if abs(th - 45) > 1 else 30.0])


def c3s3_cricketer(r):
    Rm = r.choice([60, 80, 100, 120, 90, 70])
    return {'stem': f'A cricketer can throw a ball to a maximum horizontal distance of {Rm} m. How high above the ground can the cricketer throw the same ball (same speed)?',
            'answer': f'{g(Rm / 2)} m', 'key': f'R_max = u²/g = {Rm} m (1). Thrown vertically, H = u²/2g = R_max/2 = {g(Rm / 2)} m (2).',
            'distractors': [f'{Rm} m', f'{g(Rm / 4)} m', f'{g(Rm * 2)} m']}


def c3s3_aircraft(r):
    u = r.choice([600, 500, 450, 700])
    v = r.choice([720, 900, 1080]) * 5 / 18
    h = r.choice([1000, 1500, 2000])
    if v >= u:
        v = u * 0.4
    th = math.degrees(math.acos(v / u))
    hmax = (u * math.sin(math.radians(th))) ** 2 / (2 * G)
    return {'stem': f'A fighter plane flies horizontally at an altitude of {h} m with speed {g(v)} m s⁻¹ and passes directly overhead an anti-aircraft gun. The muzzle speed of the shell is {u} m s⁻¹. '
                    'At what angle with the vertical should the gun be fired to hit the plane? At what minimum altitude must the pilot fly to avoid being hit? (g = 9.8 m s⁻²)',
            'answer': f'{num(90 - th, 1)}° with the vertical; above about {sig(hmax / 1000)} km',
            'key': f'Shell and plane must share the horizontal velocity: u cos θ = v ⇒ cos θ = {g(v)}/{u} ⇒ θ = {num(th, 1)}° with the horizontal, {num(90 - th, 1)}° with the vertical (2). '
                   f'Maximum height of shell = (u sin θ)²/2g = {sig(hmax)} m ≈ {sig(hmax / 1000)} km (2); the pilot must fly higher (1).', 'gap': 'G5'}


c3s3_derive = pool_txt([
    ('Show that the path of a projectile is a parabola. Derive the equation of its trajectory.', 'y = x tan θ − gx²/(2u² cos²θ)',
     'x = u cos θ·t, y = u sin θ·t − ½gt² (2); eliminate t (2); form y = ax − bx² is a parabola (1).'),
    ('Derive expressions for the time of flight, maximum height and horizontal range of a projectile launched with speed u at angle θ.', 'T = 2u sin θ/g, H = u² sin²θ/2g, R = u² sin 2θ/g',
     'T from y = 0 (2); H from v_y = 0 (1.5); R = u cos θ × T (1.5).'),
    ('Prove that the maximum horizontal range is four times the maximum height attained by the projectile in that case.', 'At 45°, R = u²/g and H = u²/4g, so R = 4H.',
     'R_max at θ = 45° (2); H at 45° = u²/4g (2); ratio (1).'),
])


def c3s3_case(r):
    who = name(r)
    u = r.choice([8, 9, 10, 11])
    th = r.choice([20, 25, 30, 35, 40])
    t = math.radians(th)
    R = u * u * math.sin(2 * t) / G
    Rm = u * u / G
    return {'stem': (f'At a district athletics meet, {who} takes off for a long jump at {u} m s⁻¹ at {th}° to the horizontal. Treat {who} as a projectile (g = 9.8 m s⁻²).\n'
                     '(i) Find the horizontal component of take-off velocity. (ii) Find the time in the air. (iii) Find the length of the jump. (iv) What would the jump be at the same speed if the take-off angle were 45°?'),
            'answer': f'(i) {sig(u * math.cos(t))} m s⁻¹ (ii) {sig(2 * u * math.sin(t) / G)} s (iii) {sig(R)} m (iv) {sig(Rm)} m',
            'key': f'(i) u cos θ (1). (ii) 2u sin θ/g (1). (iii) u² sin 2θ/g = {sig(R)} m (1). (iv) u²/g = {sig(Rm)} m (1).'}


# st4 uniform circular motion

c3s4_tf = tf_mcq('uniform circular motion',
                 ['The speed is constant but the velocity changes.', 'The acceleration is directed towards the centre.', 'The magnitude of centripetal acceleration is v²/r = ω²r.',
                  'The velocity at any point is along the tangent.'],
                 ['The acceleration is zero because the speed is constant.', 'The acceleration is along the tangent.', 'The velocity is constant.',
                  'The centripetal acceleration is v/r.'])

c3s4_explain = pool_txt([
    ('A body moves in a circle at constant speed. Why is it said to be accelerated?', 'The direction of velocity changes continuously, so velocity changes and there is an acceleration (towards the centre).', 'Velocity is a vector (1 mark); direction changes ⇒ acceleration (1 mark).'),
    ('Show that the centripetal acceleration a = v²/r can also be written as ω²r.', 'v = ωr, so v²/r = ω²r²/r = ω²r.', 'v = ωr (1 mark); substitution (1 mark).'),
    ('A stone tied to a string is whirled in a circle and the string breaks. In which direction does it fly off? Why?', 'Along the tangent at the point of release.', 'No centripetal force (1 mark); moves with its instantaneous (tangential) velocity (1 mark).'),
])

c3s4_ar = pool_ar([
    ('A body in uniform circular motion is accelerated.', 'The direction of its velocity changes continuously.', 'a', 'R explains A.'),
    ('In uniform circular motion the acceleration is constant.', 'The magnitude of centripetal acceleration v²/r is constant.', 'd', 'A is false because the direction of acceleration changes; R is true.'),
    ('The angular speed of the minute hand of a clock is 2π/3600 rad s⁻¹.', 'The minute hand completes one revolution in one hour.', 'a', 'ω = 2π/T with T = 3600 s.'),
])


def c3s4_acc(r):
    rr = r.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
    n = r.choice([7, 10, 14, 15, 20, 25])
    t = r.choice([25, 50, 100, 60, 30])
    nu = n / t
    w = 2 * math.pi * nu
    a = w * w * rr
    return NUM(f'A stone tied to the end of a string {g(rr * 100)} cm long is whirled in a horizontal circle with constant speed. It makes {n} revolutions in {t} s. Find the magnitude and direction of its acceleration.',
               a, 'm s⁻²', f'ν = {n}/{t} = {g(nu)} s⁻¹; ω = 2πν = {sig(w)} rad s⁻¹; a = ω²r = {{ans}}, directed towards the centre.',
               wrongs=[w * rr, nu * nu * rr, 2 * math.pi * nu * rr])


def c3s4_speed(r):
    rr = r.choice([25, 40, 50, 80, 100, 150, 200])
    v = r.choice([8, 10, 12, 15, 20, 25])
    return NUM(f'A car moves on a circular track of radius {rr} m at a constant speed of {v} m s⁻¹. Find its centripetal acceleration.', v * v / rr, 'm s⁻²',
               f'a = v²/r = {v * v}/{rr} = {{ans}}.', wrongs=[v / rr, v * v * rr, v * rr])


def c3s4_omega(r):
    T = r.choice([2, 4, 5, 10, 12, 20, 60, 3600])
    return NUM(f'A wheel completes one revolution in {T} s. What is its angular speed?', 2 * math.pi / T, 'rad s⁻¹', f'ω = 2π/T = 2π/{T} = {{ans}}.',
               wrongs=[1 / T, math.pi / T, T / (2 * math.pi)])


def c3s4_loop(r):
    v = r.choice([720, 900, 1080]) * 5 / 18
    rr = r.choice([0.5, 1, 1.5, 2]) * 1000
    a = v * v / rr
    return {'stem': f'An aircraft executes a horizontal loop of radius {g(rr / 1000)} km with a steady speed of {g(v * 18 / 5)} km h⁻¹. Compare its centripetal acceleration with the acceleration due to gravity.',
            'answer': f'a = {sig(a)} m s⁻² ≈ {sig(a / G, 2)} g',
            'key': f'v = {g(v)} m s⁻¹ (1); a = v²/r = {g(v * v)}/{g(rr)} = {sig(a)} m s⁻² (1); a/g = {sig(a / G, 2)} (1).'}


def c3s4_insect(r):
    rr = r.choice([8, 10, 12, 15, 20])
    n = r.choice([5, 6, 7, 8, 10])
    t = r.choice([50, 100, 60, 25])
    w = 2 * math.pi * n / t
    return {'stem': f'An insect trapped in a circular groove of radius {rr} cm moves along the groove steadily and completes {n} revolutions in {t} s. (i) What is its angular speed and linear speed? (ii) Is the acceleration vector constant? Explain.',
            'answer': f'(i) ω = {sig(w)} rad s⁻¹, v = {sig(w * rr)} cm s⁻¹ (ii) No; magnitude {sig(w * w * rr)} cm s⁻² is constant but the direction changes',
            'key': f'(i) ν = {n}/{t}; ω = 2πν = {sig(w)} rad s⁻¹ (1); v = ωr = {sig(w * rr)} cm s⁻¹ (1). (ii) a = ω²r = {sig(w * w * rr)} cm s⁻² towards the centre; its direction changes, so the vector is not constant (1).'}


def c3s4_earth(r):
    lat = r.choice([0, 13, 19, 23, 28, 30, 45])
    city = {0: 'the equator', 13: 'Chennai (13° N)', 19: 'Mumbai (19° N)', 23: 'Bhopal (23° N)', 28: 'Delhi (28.6° N ≈ 28° N)', 30: 'Chandigarh (30° N)', 45: 'a place at 45° N'}[lat]
    w = 2 * math.pi / 86400
    R = 6.4e6
    a = w * w * R * math.cos(math.radians(lat))
    return NUM(f'Find the centripetal acceleration of a point at {city} due to the Earth\'s rotation about its axis. (R = 6400 km; take one day = 24 h)', a, 'm s⁻²',
               f'ω = 2π/86400 = 7.27 × 10⁻⁵ rad s⁻¹; radius of the circle = R cos λ = {sig(R * math.cos(math.radians(lat)))} m; a = ω²R cos λ = {{ans}}.',
               wrongs=[w * w * R, w * R * math.cos(math.radians(lat)), w * w * R * math.sin(math.radians(lat)) + 1e-4], gap='G5')


# ======================================================== ch04 Laws of Motion
# st1 Newton's laws, momentum, impulse

c4s1_terms = term_mcq([('inertia', 'the tendency of a body to resist a change in its state of rest or uniform motion'), ('impulse', 'the product of force and time, equal to the change in momentum'),
                       ('linear momentum', 'the product of mass and velocity'), ('newton', 'the force that gives a mass of 1 kg an acceleration of 1 m s⁻²'),
                       ('Newton\'s third law', 'to every action there is an equal and opposite reaction')],
                      'Which of the following describes {a}?', 'Which term is described by: "{b}"?', '{a}: {b}.')

c4s1_tf = tf_mcq('Newton\'s laws of motion',
                 ['Action and reaction act on different bodies.', 'The net force on a body moving with constant velocity is zero.', 'Force equals the rate of change of momentum.',
                  'The first law defines inertia.', 'Impulse equals the change in momentum.'],
                 ['Action and reaction cancel because they act on the same body.', 'A force is needed to keep a body moving with constant velocity.',
                  'A heavier body always has more momentum than a lighter one.', 'The third law applies only to bodies at rest.', 'Impulse is measured in N m.'])

c4s1_explain = pool_txt([
    ('Why does a cricketer move his hands backward while catching a fast ball?', 'Increasing the time of impact reduces the average force on the hands for the same change in momentum.', 'F = Δp/Δt (1 mark); larger Δt ⇒ smaller F (1 mark).'),
    ('When a bus starts suddenly, standing passengers fall backward. Explain.', 'Inertia of rest: the feet move with the bus but the upper body tends to remain at rest.', 'Inertia (1 mark); applied to the situation (1 mark).'),
    ('A gun recoils when a bullet is fired. Explain using conservation of momentum.', 'Total momentum before is zero; the bullet gains forward momentum, so the gun gets equal backward momentum.', 'Conservation (1 mark); recoil direction (1 mark).'),
    ('A horse pulling a cart: if action and reaction are equal and opposite, how does the cart move?', 'Action and reaction act on different bodies; the cart moves because the net external force on it (pull minus friction) is non-zero.', 'Different bodies (1 mark); net force on cart (1 mark).'),
    ('Why is it easier to stop a tennis ball than a cricket ball moving with the same speed?', 'The cricket ball has more mass and hence more momentum; a larger impulse is needed to stop it.', 'p = mv (1 mark); larger momentum needs larger impulse (1 mark).'),
])

c4s1_ar = pool_ar([
    ('A cricketer pulls his hands back while catching a ball.', 'Increasing the time of impact decreases the average force for a given change in momentum.', 'a', 'R explains A.'),
    ('Action and reaction forces cancel each other.', 'Action and reaction are equal and opposite.', 'd', 'A is false: they act on different bodies; R is true.'),
    ('A body moving with constant velocity has no net force on it.', 'By Newton\'s first law, a body continues in uniform motion unless a net external force acts.', 'a', 'R explains A.'),
    ('The momentum of a system of bodies is conserved in an explosion.', 'The internal forces in the explosion are equal and opposite.', 'a', 'Internal forces cancel in pairs, so total momentum is unchanged.'),
    ('Impulse and momentum have the same unit.', 'Impulse is force multiplied by distance.', 'c', 'A is true (N s = kg m s⁻¹); R is false (force × time).'),
])


def c4s1_fma(r):
    m = r.choice([0.5, 2, 5, 10, 20, 50, 1000, 1200])
    u, v, t = r.choice([0, 5, 10]), r.choice([15, 20, 25, 30]), r.randint(2, 20)
    F_ = m * (v - u) / t
    return NUM(f'A body of mass {g(m)} kg changes its velocity from {u} m s⁻¹ to {v} m s⁻¹ in {t} s under a constant force. Find the force.', F_, 'N',
               f'F = m(v − u)/t = {g(m)} × {v - u}/{t} = {{ans}}.', wrongs=[m * v / t, m * (v + u) / t, m * (v - u)])


def c4s1_bat(r):
    m = r.choice([0.15, 0.16, 0.17, 0.06, 0.4])
    u, v = r.randint(10, 30), r.randint(10, 40)
    dt = r.choice([0.01, 0.02, 0.005, 0.05])
    J = m * (u + v)
    return {'stem': f'A ball of mass {g(m * 1000)} g moving at {u} m s⁻¹ is hit by a bat and returns along the same line at {v} m s⁻¹. If the contact lasts {g(dt)} s, find the impulse and the average force on the ball.',
            'answer': f'Impulse {sig(J)} N s; force {sig(J / dt)} N', 'key': f'Taking the return direction as +: Δp = m(v − (−u)) = {g(m)} × {u + v} = {sig(J)} N s; F = Δp/Δt = {sig(J / dt)} N.',
            'distractors': [f'Impulse {sig(m * abs(v - u))} N s; force {sig(m * abs(v - u) / dt)} N', f'Impulse {sig(J)} N s; force {sig(J * dt)} N', f'Impulse {sig(m * v)} N s; force {sig(m * v / dt)} N']}


def c4s1_recoil(r):
    M = r.choice([2, 3, 4, 5, 8, 10])
    m = r.choice([10, 20, 25, 40, 50])
    v = r.choice([300, 400, 500, 600, 800])
    V = m / 1000 * v / M
    return {'stem': f'A shell of mass {m} g is fired horizontally from a gun of mass {M} kg with a muzzle speed of {v} m s⁻¹. Find the recoil speed of the gun. If the gun is stopped by the shoulder in 0.2 s, what is the average force on the shoulder?',
            'answer': f'{sig(V)} m s⁻¹; {sig(M * V / 0.2)} N', 'key': f'0 = mv − MV ⇒ V = mv/M = {g(m / 1000)} × {v}/{M} = {sig(V)} m s⁻¹ (2); F = MV/t = {sig(M * V / 0.2)} N (1).'}


def c4s1_block(r):
    m = r.choice([5, 10, 20, 30, 50])
    v = r.choice([100, 150, 200, 300])
    d = r.choice([2, 3, 4, 5, 6])
    F_ = (m / 1000) * v * v / (2 * d / 100)
    return NUM(f'A bullet of mass {m} g moving at {v} m s⁻¹ penetrates {d} cm into a wooden block before coming to rest. Find the average resistive force exerted by the wood.',
               F_, 'N', f'a = v²/2s = {v * v}/(2 × {g(d / 100)}) m s⁻²; F = ma = {g(m / 1000)} × {g(v * v / (2 * d / 100))} = {{ans}}.',
               wrongs=[m * v * v / (2 * d), (m / 1000) * v / (d / 100), F_ * 2])


def c4s1_mgun(r):
    n = r.choice([120, 180, 240, 300, 600])
    m = r.choice([20, 30, 40, 50])
    v = r.choice([400, 500, 600, 800])
    F_ = n / 60 * m / 1000 * v
    return {'stem': f'A machine gun fires {n} bullets per minute, each of mass {m} g, with a speed of {v} m s⁻¹. What force is needed to hold the gun in position?',
            'answer': f'{sig(F_)} N', 'key': f'Bullets per second = {n}/60 = {g(n / 60)} (1); momentum per bullet = {g(m / 1000)} × {v} = {g(m / 1000 * v)} kg m s⁻¹ (1); F = rate of change of momentum = {sig(F_)} N (1).'}


# st2 equilibrium, FBD, connected bodies

c4s2_tf = tf_mcq('equilibrium and free-body diagrams',
                 ['For a particle in equilibrium the vector sum of forces on it is zero.', 'A free-body diagram shows only the forces acting on the chosen body.',
                  'The tension in a light string is the same throughout when it passes over a frictionless pulley.', 'Three forces in equilibrium can be represented by the sides of a closed triangle.'],
                 ['A free-body diagram includes the forces the body exerts on others.', 'A body in equilibrium must be at rest.',
                  'The tension in a light string over a frictionless pulley is different on the two sides.', 'Normal reaction is always equal to the weight of a body.'])

c4s2_explain = pool_txt([
    ('Why does a person in a lift feel heavier when the lift starts moving up?', 'The floor must push with R = m(g + a) > mg to accelerate the person upward; we feel this normal force as weight.', 'FBD with R − mg = ma (1 mark); R > mg (1 mark).'),
    ('What is the apparent weight of a person in a freely falling lift? Explain.', 'Zero.', 'a = g ⇒ R = m(g − a) = 0 (2 marks).'),
    ('Draw (describe) the free-body diagram of a book lying on a table and state which forces form an action-reaction pair.', 'Weight mg downward and normal force N upward act on the book; they balance but are not an action-reaction pair. N pairs with the book\'s push on the table.',
     'Correct forces (1 mark); correct pairing (1 mark).'),
])

c4s2_ar = pool_ar([
    ('The apparent weight of a person in a lift moving up with constant velocity equals the true weight.', 'With zero acceleration, R − mg = 0.', 'a', 'R explains A.'),
    ('A person in a freely falling lift feels weightless.', 'In free fall the normal reaction is zero.', 'a', 'R explains A.'),
    ('The weight of a book on a table and the normal force on it form an action-reaction pair.', 'They are equal and opposite.', 'd', 'A is false: both act on the book; R is true for a book at rest.'),
    ('In an Atwood machine with unequal masses, the tension is less than the weight of the heavier mass.', 'The heavier mass accelerates downward.', 'a', 'mg − T = ma > 0 ⇒ T < mg; R explains A.'),
])


def c4s2_lift(r):
    m = r.choice([40, 50, 60, 70, 80])
    a = r.choice([1, 1.5, 2, 2.5, 3])
    up = r.random() < 0.5
    R = m * (G + a) if up else m * (G - a)
    who = name(r)
    return NUM(f'{who}, of mass {m} kg, stands on a weighing machine in a lift that is accelerating {"upward" if up else "downward"} at {g(a)} m s⁻². What does the machine read (in newton)? (g = 9.8 m s⁻²)',
               R, 'N', f'R − mg = {"+" if up else "−"}ma ⇒ R = m(g {"+" if up else "−"} a) = {m} × {g(G + a if up else G - a)} = {{ans}}.',
               wrongs=[m * (G - a) if up else m * (G + a), m * G, m * a])


def c4s2_push(r):
    m1, m2 = r.sample([2, 3, 4, 5, 6, 8, 10], 2)
    F_ = r.choice([10, 12, 15, 20, 24, 30, 40])
    a = F_ / (m1 + m2)
    return {'stem': f'Two blocks of masses {m1} kg and {m2} kg are in contact on a frictionless table. A horizontal force of {F_} N pushes the {m1} kg block. Find the acceleration and the force of contact between the blocks.',
            'answer': f'a = {sig(a)} m s⁻²; contact force {sig(m2 * a)} N', 'key': f'a = F/(m₁ + m₂) = {F_}/{m1 + m2} = {sig(a)} m s⁻²; contact force on {m2} kg = m₂a = {sig(m2 * a)} N.',
            'distractors': [f'a = {sig(a)} m s⁻²; contact force {sig(m1 * a)} N', f'a = {sig(F_ / m1)} m s⁻²; contact force {sig(m2 * F_ / m1)} N', f'a = {sig(a)} m s⁻²; contact force {F_} N']}


def c4s2_atwood(r):
    m1, m2 = sorted(r.sample([2, 3, 4, 5, 6, 8], 2), reverse=True)
    a = (m1 - m2) * G / (m1 + m2)
    T = 2 * m1 * m2 * G / (m1 + m2)
    return {'stem': f'Two masses {m1} kg and {m2} kg are tied to the ends of a light inextensible string passing over a frictionless pulley. Find the acceleration of the masses and the tension in the string when they are released. (g = 9.8 m s⁻²)',
            'answer': f'a = {sig(a)} m s⁻²; T = {sig(T)} N',
            'key': f'{m1}g − T = {m1}a and T − {m2}g = {m2}a (1); adding: a = (m₁ − m₂)g/(m₁ + m₂) = {sig(a)} m s⁻² (1); T = 2m₁m₂g/(m₁ + m₂) = {sig(T)} N (1).'}


def c4s2_side(r):
    m = r.choice([2, 4, 5, 6, 8, 10])
    F_ = r.choice([10, 20, 30, 40, 50])
    th = math.degrees(math.atan(F_ / (m * G)))
    T = math.hypot(F_, m * G)
    return {'stem': f'A mass of {m} kg hangs from a light rope fixed to the ceiling. A horizontal force of {F_} N is applied to the mass and it comes to rest with the rope inclined. Find the angle of the rope with the vertical and the tension. (g = 9.8 m s⁻²)',
            'answer': f'{num(th, 1)}°; {sig(T)} N', 'key': f'T cos θ = mg, T sin θ = F (1); tan θ = F/mg = {F_}/{g(m * G)} ⇒ θ = {num(th, 1)}° (1); T = √(F² + (mg)²) = {sig(T)} N (1).'}


def c4s2_three(r):
    m = r.sample([1, 2, 3, 4, 5, 6], 3)
    F_ = r.choice([12, 18, 24, 30, 36, 60])
    a = F_ / sum(m)
    T1 = (m[1] + m[2]) * a
    T2 = m[2] * a
    return {'stem': f'Three blocks A ({m[0]} kg), B ({m[1]} kg) and C ({m[2]} kg) are connected by light strings A–B and B–C on a smooth horizontal surface. A is pulled with a horizontal force of {F_} N. Find the acceleration and the tensions in the two strings.',
            'answer': f'a = {sig(a)} m s⁻²; T(A–B) = {sig(T1)} N; T(B–C) = {sig(T2)} N',
            'key': f'a = F/(total mass) = {F_}/{sum(m)} = {sig(a)} m s⁻² (1); string A–B pulls B and C: T₁ = ({m[1]} + {m[2]})a = {sig(T1)} N (1); string B–C pulls C: T₂ = {m[2]}a = {sig(T2)} N (1).'}


# st3 friction, inclined plane

c4s3_tf = tf_mcq('friction',
                 ['Static friction adjusts itself up to a maximum value μₛN.', 'Kinetic friction is usually less than limiting static friction.', 'Rolling friction is much smaller than sliding friction.',
                  'Friction opposes relative motion between surfaces in contact.', 'Within limits, friction is independent of the area of contact.'],
                 ['Static friction is always equal to μₛN.', 'Kinetic friction is greater than limiting static friction.', 'Friction always opposes the motion of a body relative to the ground.',
                  'Friction increases with the area of contact.', 'Friction can never help a body to move.'])

c4s3_terms = term_mcq([('limiting friction', 'the maximum static friction, μₛN'), ('kinetic friction', 'friction between surfaces in relative sliding, μₖN'),
                       ('angle of repose', 'the angle at which a body just begins to slide down an incline, tan θ = μₛ'), ('rolling friction', 'opposition to rolling, much less than sliding friction')],
                      'Which statement describes {a}?', 'Which term matches: {b}?', '{a}: {b}.')

c4s3_explain = pool_txt([
    ('Why is it easier to pull a lawn roller than to push it?', 'Pulling at an angle reduces the normal reaction (and hence friction); pushing increases it.', 'N = mg − F sin θ for pull, mg + F sin θ for push (2 marks).'),
    ('Explain how friction helps us walk.', 'The foot pushes the ground backward; static friction on the foot acts forward and propels us.', 'Backward push (1 mark); forward friction (1 mark).'),
    ('Why are ball bearings used in machines?', 'They replace sliding friction by much smaller rolling friction, reducing energy loss and wear.', 'Rolling < sliding (2 marks).'),
    ('A box is kept on the floor of a truck. When the truck accelerates, the box moves with it. Which force accelerates the box?', 'Static friction exerted by the truck floor on the box, in the direction of the acceleration.', 'Static friction (1 mark); direction forward (1 mark).'),
])

c4s3_ar = pool_ar([
    ('It is easier to pull a lawn roller than to push it.', 'Pulling at an angle reduces the normal reaction and hence friction.', 'a', 'R explains A.'),
    ('Static friction is a self-adjusting force.', 'Static friction equals the applied force until the limiting value is reached.', 'a', 'R explains A.'),
    ('The coefficient of static friction equals the tangent of the angle of repose.', 'At the angle of repose mg sin θ = μₛ mg cos θ.', 'a', 'R explains A.'),
    ('Friction always opposes the motion of a body.', 'Friction opposes relative motion between surfaces in contact.', 'd', 'A is false (friction drives walking or a box in a truck); R is true.'),
    ('Kinetic friction is greater than limiting static friction.', 'It is harder to start a body moving than to keep it moving.', 'd', 'A is false; R is true.'),
])


def c4s3_limit(r):
    m = r.choice([2, 5, 10, 20, 25, 40])
    mu = r.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6])
    return NUM(f'A box of mass {m} kg rests on a horizontal floor. The coefficient of static friction is {mu}. What minimum horizontal force is needed to just move it? (g = 9.8 m s⁻²)',
               mu * m * G, 'N', f'f_max = μₛN = μₛmg = {mu} × {m} × 9.8 = {{ans}}.', wrongs=[mu * m, m * G, m * G / mu])


def c4s3_slide(r):
    v = r.choice([2, 3, 4, 5, 6, 8, 10])
    mu = r.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4])
    s = v * v / (2 * mu * G)
    return NUM(f'A block is given an initial speed of {v} m s⁻¹ along a rough horizontal floor (μₖ = {mu}). How far does it slide before stopping? (g = 9.8 m s⁻²)',
               s, 'm', f'Retardation a = μₖg = {g(mu * G)} m s⁻²; s = v²/2a = {v * v}/{g(2 * mu * G)} = {{ans}}.', wrongs=[v * v / (mu * G), v / (mu * G), v * v * mu / (2 * G)])


def c4s3_incline(r):
    th = r.choice([30, 37, 45, 53, 60])
    mu = r.choice([0.1, 0.2, 0.25, 0.3, 0.4])
    t = math.radians(th)
    if math.tan(t) <= mu:
        mu = 0.2
    a = G * (math.sin(t) - mu * math.cos(t))
    return NUM(f'A block slides down a rough plane inclined at {th}° to the horizontal. The coefficient of kinetic friction is {mu}. Find its acceleration. (g = 9.8 m s⁻²)',
               a, 'm s⁻²', f'Along the plane: mg sin θ − μₖmg cos θ = ma ⇒ a = g(sin θ − μₖ cos θ) = 9.8({math.sin(t):.3f} − {mu} × {math.cos(t):.3f}) = {{ans}}.',
               wrongs=[G * math.sin(t), G * (math.sin(t) + mu * math.cos(t)), G * (math.cos(t) - mu * math.sin(t))])


def c4s3_repose(r):
    th = r.choice([15, 20, 25, 30, 35, 37])
    mu = math.tan(math.radians(th))
    return NUM(f'A wooden block placed on a plank just begins to slide when the plank is tilted to {th}° with the horizontal. Find the coefficient of static friction.', mu, '',
               f'At the angle of repose, μₛ = tan θ = tan {th}° = {{ans}}.', wrongs=[math.sin(math.radians(th)), math.cos(math.radians(th)), 1 / mu])


def c4s3_truck(r):
    mu = r.choice([0.15, 0.2, 0.25, 0.3, 0.4])
    m = r.choice([20, 40, 50, 100])
    a_try = r.choice([1, 2, 3, 4, 5])
    amax = mu * G
    slips = a_try > amax
    return {'stem': f'A crate of mass {m} kg lies on the floor of a truck. The coefficient of static friction between the crate and the floor is {mu}. (i) What is the maximum acceleration of the truck for which the crate does not slide? (ii) Will the crate slide if the truck accelerates at {a_try} m s⁻²?',
            'answer': f'(i) {sig(amax)} m s⁻² (ii) {"Yes" if slips else "No"}',
            'key': f'(i) Static friction provides the crate\'s acceleration: ma ≤ μₛmg ⇒ a_max = μₛg = {sig(amax)} m s⁻² (2). (ii) {a_try} {">" if slips else "<"} {sig(amax)}, so the crate {"slides" if slips else "does not slide"} (1).'}


def c4s3_up(r):
    m = r.choice([5, 10, 20, 25])
    th = r.choice([30, 37, 45])
    mu = r.choice([0.1, 0.2, 0.3])
    t = math.radians(th)
    F_ = m * G * (math.sin(t) + mu * math.cos(t))
    return {'stem': f'What force parallel to the incline is needed to push a {m} kg box up a plane inclined at {th}° at constant speed, if μₖ = {mu}? How does it compare with the force needed to let it slide down at constant speed? (g = 9.8 m s⁻²)',
            'answer': f'Up: {sig(F_)} N; down: {sig(abs(m * G * (math.sin(t) - mu * math.cos(t))))} N (applied {"up" if math.sin(t) > mu * math.cos(t) else "down"} the plane)',
            'key': f'Up at constant speed: F = mg sin θ + μmg cos θ = {sig(F_)} N (2). Down at constant speed, friction acts up the slope: F = mg sin θ − μmg cos θ = {sig(m * G * (math.sin(t) - mu * math.cos(t)))} N (1).'}


def c4s3_angle_pull(r):
    m = r.choice([10, 20, 25, 40])
    F_ = r.choice([50, 80, 100, 120, 150])
    th = r.choice([30, 37, 45, 53])
    mu = r.choice([0.2, 0.25, 0.3])
    t = math.radians(th)
    N = m * G - F_ * math.sin(t)
    a = (F_ * math.cos(t) - mu * N) / m
    if a <= 0 or N <= 0:
        raise ValueError
    return {'stem': f'{name(r)} pulls a {m} kg trunk along a rough floor (μₖ = {mu}) with a rope at {th}° above the horizontal, with a force of {F_} N. Find the normal reaction and the acceleration of the trunk. (g = 9.8 m s⁻²)',
            'answer': f'N = {sig(N)} N; a = {sig(a)} m s⁻²',
            'key': f'Vertical: N + F sin θ = mg ⇒ N = {g(m * G)} − {sig(F_ * math.sin(t))} = {sig(N)} N (2). Horizontal: F cos θ − μN = ma ⇒ a = ({sig(F_ * math.cos(t))} − {sig(mu * N)})/{m} = {sig(a)} m s⁻² (3).', 'gap': 'G5'}


def c4s3_case(r):
    who = name(r)
    m = r.choice([0.5, 1.0, 1.5, 2.0])
    th = r.choice([17, 20, 22, 25, 28])
    mus = math.tan(math.radians(th))
    mk = round(mus * r.choice([0.7, 0.75, 0.8]), 2)
    return {'stem': (f'In a lab activity, {who} places a {g(m)} kg wooden block on a plank and slowly raises one end. The block just starts sliding at {th}°. From a separate sliding test she finds μₖ = {mk} for the same pair of surfaces.\n'
                     f'(i) Find μₛ. (ii) Find the limiting friction at {th}°. (iii) Why is μₖ less than μₛ? (iv) Find the acceleration of the block at {th}° once it is sliding. (g = 9.8 m s⁻²)'),
            'answer': f'(i) {sig(mus)} (ii) {sig(m * G * math.sin(math.radians(th)))} N (iii) Once sliding, surface bonds have less time to form (kinetic friction < limiting friction) (iv) {sig(G * (math.sin(math.radians(th)) - mk * math.cos(math.radians(th))))} m s⁻²',
            'key': f'(i) μₛ = tan {th}° (1). (ii) f = mg sin θ = {sig(m * G * math.sin(math.radians(th)))} N (1). (iii) kinetic friction is less than limiting static friction (1). (iv) a = g(sin θ − μₖ cos θ) (1).'}


# st4 banking of roads

c4s4_tf = tf_mcq('a car going round a curved road',
                 ['On a level road the centripetal force is provided by friction.', 'On a banked road part of the normal reaction provides the centripetal force.',
                  'The optimum speed on a banked road is √(rg tan θ).', 'The maximum safe speed on a level curve is √(μₛrg).'],
                 ['On a level road the centripetal force is provided by the weight of the car.', 'The maximum safe speed on a level curve is independent of μₛ.',
                  'The optimum speed on a banked road depends on the mass of the car.', 'A banked road needs more friction than a level road at the optimum speed.'])

c4s4_explain = pool_txt([
    ('Why are curved roads and railway tracks banked?', 'The horizontal component of the normal reaction then supplies the centripetal force, so less reliance on friction and less wear and skidding.', 'N sin θ provides centripetal force (1 mark); reduces friction need (1 mark).'),
    ('Why does a cyclist lean inward while taking a turn?', 'The horizontal component of the ground\'s reaction then provides the centripetal force needed for the turn.', 'Centripetal force needed (1 mark); leaning provides it (1 mark).'),
    ('Why do cars skid outward on a wet curved road?', 'Wet surfaces reduce μₛ, so friction cannot provide mv²/r at that speed.', 'v_max = √(μₛrg) decreases (2 marks).'),
])

c4s4_ar = pool_ar([
    ('A car can take a level curve only up to a certain maximum speed.', 'Static friction can provide at most μₛmg as centripetal force.', 'a', 'mv²/r ≤ μₛmg gives v_max; R explains A.'),
    ('The optimum speed on a banked road does not depend on the mass of the vehicle.', 'v_o = √(rg tan θ).', 'a', 'R explains A.'),
    ('On a banked road no friction is needed at any speed.', 'At the optimum speed the normal reaction alone provides the centripetal force.', 'd', 'A is false (only at the optimum speed); R is true.'),
])


def c4s4_level(r):
    rr = r.choice([20, 30, 40, 50, 80, 100])
    mu = r.choice([0.2, 0.3, 0.4, 0.5, 0.6])
    v = math.sqrt(mu * rr * G)
    return NUM(f'A car takes an unbanked circular turn of radius {rr} m. If μₛ between tyres and road is {mu}, what is the maximum speed for a safe turn? (g = 9.8 m s⁻²)', v, 'm s⁻¹',
               f'mv²/r ≤ μₛmg ⇒ v_max = √(μₛrg) = √({mu} × {rr} × 9.8) = {{ans}} ({sig(v * 3.6)} km h⁻¹).', wrongs=[mu * rr * G, math.sqrt(rr * G), math.sqrt(mu * rr)])


def c4s4_bank(r):
    rr = r.choice([100, 150, 200, 300, 400])
    v = r.choice([36, 54, 72, 90])
    u = v * 5 / 18
    th = math.degrees(math.atan(u * u / (rr * G)))
    return NUM(f'A highway curve of radius {rr} m is to be designed for vehicles moving at {v} km h⁻¹ so that no friction is needed. At what angle should it be banked? (g = 9.8 m s⁻²)', th, '°',
               f'tan θ = v²/rg = {g(u * u)}/({rr} × 9.8) = {u * u / (rr * G):.4f} ⇒ θ = {{ans}}.'.replace(' °', '°'),
               wrongs=[math.degrees(math.atan(v * v / (rr * G))) % 90, math.degrees(math.asin(min(1, u * u / (rr * G)))) + 1, 90 - th])


def c4s4_bank_mu(r):
    rr = r.choice([100, 200, 300, 400])
    th = r.choice([10, 15, 20, 30])
    mu = r.choice([0.1, 0.2, 0.3, 0.4])
    t = math.tan(math.radians(th))
    vo = math.sqrt(rr * G * t)
    vm = math.sqrt(rr * G * (mu + t) / (1 - mu * t))
    return {'stem': f'A circular race track of radius {rr} m is banked at {th}°. If μₛ = {mu}, find (i) the optimum speed of a race car to avoid wear and tear of its tyres and (ii) the maximum permissible speed to avoid slipping. (g = 9.8 m s⁻²)',
            'answer': f'(i) {sig(vo)} m s⁻¹ (ii) {sig(vm)} m s⁻¹',
            'key': f'(i) v₀ = √(rg tan θ) = √({rr} × 9.8 × {t:.3f}) = {sig(vo)} m s⁻¹ (2). (ii) v_max = √[rg(μₛ + tan θ)/(1 − μₛ tan θ)] = {sig(vm)} m s⁻¹ (3).'}


def c4s4_cyclist(r):
    v = r.choice([5, 6, 8, 10, 12])
    rr = r.choice([10, 15, 20, 25, 30])
    th = math.degrees(math.atan(v * v / (rr * G)))
    return NUM(f'A cyclist rides at {v} m s⁻¹ around a curve of radius {rr} m. At what angle with the vertical must the cyclist lean? (g = 9.8 m s⁻²)', th, '°',
               f'tan θ = v²/rg = {v * v}/{g(rr * G)} ⇒ θ = {{ans}}.'.replace(' °', '°'), wrongs=[90 - th, math.degrees(math.atan(v / (rr * G))) + 0.5, th * 2])


def c4s4_string(r):
    m = r.choice([0.1, 0.2, 0.25, 0.5])
    L = r.choice([0.5, 1, 1.5, 2])
    T = r.choice([20, 25, 50, 100])
    v = math.sqrt(T * L / m)
    return {'stem': f'A stone of mass {g(m)} kg tied to a string {g(L)} m long is whirled in a horizontal circle on a smooth table. The string can bear a maximum tension of {T} N. Find the maximum speed of the stone. In which direction does the stone move if the string breaks?',
            'answer': f'{sig(v)} m s⁻¹; along the tangent at that point', 'key': f'T = mv²/L ⇒ v_max = √(TL/m) = √({T} × {g(L)}/{g(m)}) = {sig(v)} m s⁻¹ (2); with no centripetal force it moves along the tangent (1).'}


# ======================================================== ch05 Work, Energy and Power
# st1 work done by constant and variable forces

c5s1_tf = tf_mcq('work',
                 ['Work done by a force perpendicular to the displacement is zero.', 'Work done by kinetic friction on a sliding body is negative.', 'Work is the scalar product F·d.',
                  'The area under a force-displacement graph gives the work done.', 'The SI unit of work is the joule.'],
                 ['Work done by the centripetal force in uniform circular motion is positive.', 'Work is a vector quantity.', 'A coolie carrying a load on his head and walking on a level road does positive work against gravity.',
                  'Work done by a force is always positive.', 'Work done is the vector product F × d.'])

c5s1_terms = pool_mcq([
    ('The work done by gravity on a satellite moving in a circular orbit is', 'zero', ['positive', 'negative', 'equal to its kinetic energy'], 'Gravity is perpendicular to the velocity at every point.'),
    ('The work done by friction on a block sliding on a floor is', 'negative', ['positive', 'zero', 'positive or negative depending on speed'], 'Friction opposes the displacement (θ = 180°).'),
    ('A man lifts a bucket of water from a well. The work done by the man on the bucket is', 'positive', ['negative', 'zero', 'positive only if the bucket accelerates'], 'Force and displacement are both upward.'),
    ('The work done by the gravitational force on a body moving up an incline is', 'negative', ['positive', 'zero', 'equal to mgl'], 'Gravity has a component opposite to the displacement.'),
    ('If F = (3î + 4ĵ) N and d = (4î − 3ĵ) m, the work done is', '0 J', ['25 J', '24 J', '7 J'], 'F·d = 12 − 12 = 0.'),
])

c5s1_explain = pool_txt([
    ('A coolie carries a suitcase on his head and walks on a level platform. How much work does he do on the suitcase against gravity? Explain.', 'Zero.', 'His upward force is perpendicular to the horizontal displacement, so W = Fd cos 90° = 0 (2 marks).'),
    ('Why is the work done by the centripetal force on a body moving in a circle zero?', 'The centripetal force is always perpendicular to the velocity (displacement).', 'θ = 90° ⇒ W = 0 (2 marks).'),
    ('When can the work done by a force be negative? Give an example.', 'When the angle between force and displacement is more than 90°, e.g. friction on a sliding block or gravity on a rising ball.', 'Condition (1 mark); example (1 mark).'),
    ('Explain why the work done by a variable force is found from the area under the force-displacement graph.', 'Splitting the displacement into small steps, W = ΣF Δx, which becomes ∫F dx: the area under the graph.', 'Small-step sum (1 mark); integral = area (1 mark).'),
])

c5s1_ar = pool_ar([
    ('The work done by the centripetal force in uniform circular motion is zero.', 'The centripetal force is perpendicular to the velocity.', 'a', 'R explains A.'),
    ('Work done by friction is always negative.', 'Friction can act in the direction of motion of a body, e.g. a box on an accelerating truck.', 'd', 'A is false (friction can do positive work); R is true.'),
    ('Work is a scalar quantity.', 'Work is the scalar product of force and displacement.', 'a', 'R explains A.'),
    ('A person standing still holding a heavy box does no work on the box.', 'The box has no displacement.', 'a', 'W = F·d = 0 because d = 0.'),
])


def c5s1_wfd(r):
    F_ = r.choice([10, 20, 25, 40, 50, 80, 100])
    d = r.choice([2, 3, 5, 8, 10, 12])
    th = r.choice([0, 30, 37, 45, 53, 60])
    W = F_ * d * math.cos(math.radians(th))
    if abs(W) < 1e-9:
        W = 0.0
    ans = '0 J' if W == 0 else sig(W) + ' J'
    return {'stem': f'{name(r)} pulls a trolley in a supermarket with a force of {F_} N directed at {th}° to the horizontal. How much work is done in moving it {d} m along the floor?',
            'answer': ans, 'key': f'W = Fd cos θ = {F_} × {d} × cos {th}° = {ans}.',
            'distractors': [sig(F_ * d) + ' J', sig(F_ * d * math.sin(math.radians(th))) + ' J' if th not in (0, 180) else sig(F_ * d * 2) + ' J', sig(F_ * d / 2) + ' J', sig(F_ + d) + ' J']}


def c5s1_dot(r):
    F_ = [r.randint(-5, 8) for _ in range(3)]
    d = [r.randint(-5, 8) for _ in range(3)]
    W = sum(a * b for a, b in zip(F_, d))
    mf, md = math.sqrt(sum(a * a for a in F_)), math.sqrt(sum(b * b for b in d))
    if mf == 0 or md == 0:
        raise ValueError
    th = math.degrees(math.acos(W / (mf * md)))

    def v(x):
        s = f'{x[0]}î'
        for c, u in zip(x[1:], ['ĵ', 'k̂']):
            s += f' {"+" if c >= 0 else "−"} {abs(c)}{u}'
        return s.replace('-', '−')
    return {'stem': f'A force F = ({v(F_)}) N acts on a particle that is displaced by d = ({v(d)}) m. Find the work done and the angle between F and d.'.replace('k̂', 'k̂'),
            'answer': f'W = {W} J; θ = {num(th, 1)}°'.replace('-', '−'),
            'key': f'W = F·d = {" + ".join(f"({a})({b})" for a, b in zip(F_, d))} = {W} J (1.5); cos θ = W/(|F||d|) = {W}/({sig(mf)} × {sig(md)}) ⇒ θ = {num(th, 1)}° (1.5).'.replace('-', '−')}


def c5s1_spring_work(r):
    k = r.choice([100, 200, 250, 400, 500, 800])
    x1, x2 = sorted(r.sample([0, 2, 3, 4, 5, 6, 8, 10], 2))
    W = 0.5 * k * ((x2 / 100) ** 2 - (x1 / 100) ** 2)
    return NUM(f'How much work is needed to stretch a spring of spring constant {k} N m⁻¹ from an extension of {x1} cm to {x2} cm?', W, 'J',
               f'W = ½k(x₂² − x₁²) = ½ × {k} × ({g(x2 / 100)}² − {g(x1 / 100)}²) = {{ans}}.', wrongs=[0.5 * k * ((x2 - x1) / 100) ** 2, k * ((x2 / 100) ** 2 - (x1 / 100) ** 2), 0.5 * k * (x2 * x2 - x1 * x1)])


def c5s1_fx_graph(r):
    F1, F2 = r.sample([2, 4, 5, 6, 8, 10, 12], 2)
    x1, x2 = r.randint(2, 5), r.randint(6, 12)
    W = F1 * x1 + 0.5 * (F1 + F2) * (x2 - x1)
    return {'stem': f'A force acting on a body along the x-axis is {F1} N (constant) from x = 0 to x = {x1} m and then changes linearly to {F2} N at x = {x2} m. Find the total work done by the force from x = 0 to x = {x2} m.',
            'answer': f'{g(W)} J', 'key': f'Area of rectangle = {F1} × {x1} = {F1 * x1} J (1); trapezium = ½({F1} + {F2})({x2 - x1}) = {g(0.5 * (F1 + F2) * (x2 - x1))} J (1); total {g(W)} J (1).'}


def c5s1_incline_work(r):
    m = r.choice([2, 5, 10, 20])
    L = r.choice([2, 3, 4, 5, 8])
    th = r.choice([30, 37, 45, 60])
    mu = r.choice([0.1, 0.2, 0.3])
    t = math.radians(th)
    Wg = m * G * L * math.sin(t)
    Wf = -mu * m * G * math.cos(t) * L
    return {'stem': f'A {m} kg block slides {L} m down a rough plane inclined at {th}° (μₖ = {mu}). Find the work done on it by (i) gravity, (ii) friction and (iii) the normal force, and the net work. (g = 9.8 m s⁻²)',
            'answer': f'(i) {sig(Wg)} J (ii) {sig(Wf)} J (iii) 0 J; net {sig(Wg + Wf)} J',
            'key': f'(i) W_g = mgL sin θ = {sig(Wg)} J (1). (ii) W_f = −μmg cos θ · L = {sig(Wf)} J (1). (iii) N ⊥ displacement ⇒ 0; net = {sig(Wg + Wf)} J (1).'}


# st2 work-energy theorem; KE; PE of a spring

c5s2_tf = tf_mcq('kinetic energy and the work-energy theorem',
                 ['The work done by the net force equals the change in kinetic energy.', 'Kinetic energy can never be negative.', 'For the same momentum, a lighter body has more kinetic energy.',
                  'Doubling the speed of a body makes its kinetic energy four times.'],
                 ['The work done by the net force equals the change in potential energy.', 'For the same momentum, a heavier body has more kinetic energy.',
                  'Doubling the speed of a body doubles its kinetic energy.', 'The potential energy of a spring is ½kx regardless of the sign of x.'])

c5s2_explain = pool_txt([
    ('A light body and a heavy body have the same momentum. Which has more kinetic energy? Explain.', 'The light body.', 'K = p²/2m; for the same p, K ∝ 1/m (2 marks).'),
    ('State the work-energy theorem and write it as an equation.', 'The work done by the net force on a body equals the change in its kinetic energy: W = K_f − K_i.', 'Statement (1 mark); equation (1 mark).'),
    ('Why is the potential energy of a spring the same whether it is stretched or compressed by x?', 'V = ½kx² depends on x², which is the same for +x and −x.', 'Formula (1 mark); x² argument (1 mark).'),
    ('A raindrop falls at terminal velocity. Is the work-energy theorem violated since gravity does work but the KE stays the same?', 'No: air resistance does equal negative work, so the net work and the change in KE are both zero.', 'Net work = 0 (1 mark); ΔK = 0 (1 mark).'),
])

c5s2_ar = pool_ar([
    ('When the speed of a body is doubled, its kinetic energy becomes four times.', 'Kinetic energy is proportional to the square of speed.', 'a', 'R explains A.'),
    ('A light body and a heavy body with equal kinetic energies have equal momenta.', 'p = √(2mK).', 'd', 'A is false (the heavy body has more momentum); R is true.'),
    ('The work done by the net force on a body moving with constant speed in a circle is zero.', 'Its kinetic energy does not change.', 'a', 'By the work-energy theorem, W = ΔK = 0.'),
    ('The potential energy of a spring is negative when it is compressed.', 'The spring force is restoring.', 'd', 'A is false: V = ½kx² ≥ 0; R is true.'),
])


KE_OBJ = [('bullet', 0.01, 0.05, [300, 400, 500]), ('cricket ball', 0.16, 0.16, [20, 25, 30, 35]), ('stone', 0.5, 2, [5, 8, 10, 12]),
          ('cyclist with cycle', 60, 80, [4, 5, 6, 8]), ('car', 1000, 1500, [10, 15, 20, 25]), ('sprinter', 50, 70, [8, 9, 10])]


def c5s2_ke(r):
    obj, lo, hi, vs = r.choice(KE_OBJ)
    m = r.choice(sorted({lo, hi, round((lo + hi) / 2, 3)}))
    v = r.choice(vs)
    K = 0.5 * m * v * v
    return NUM(f'Find the kinetic energy of a {g(m)} kg {obj} moving at {v} m s⁻¹.', K, 'J', f'K = ½mv² = ½ × {g(m)} × {v}² = {{ans}}.', wrongs=[m * v * v, 0.5 * m * v, m * v])


def c5s2_wet(r):
    m = r.choice([1000, 1200, 1500])
    v = r.choice([36, 54, 72, 90])
    F_ = r.choice([3000, 4000, 5000, 6000, 7500])
    u = v * 5 / 18
    s = 0.5 * m * u * u / F_
    return NUM(f'A car of mass {m} kg moving at {v} km h⁻¹ is brought to rest by a constant braking force of {F_} N. Use the work-energy theorem to find the stopping distance.', s, 'm',
               f'K_i = ½ × {m} × {g(u)}² = {g(0.5 * m * u * u)} J; F s = K_i ⇒ s = {g(0.5 * m * u * u)}/{F_} = {{ans}}.', wrongs=[m * u * u / F_, 0.5 * m * v * v / F_, m * u / F_])


def c5s2_raindrop(r):
    m = r.choice([1, 2, 1.5, 0.5])
    h = r.choice([500, 800, 1000, 1200])
    v = r.choice([10, 20, 25, 50])
    mk = m / 1000
    Wg = mk * G * h
    Wr = 0.5 * mk * v * v - Wg
    return {'stem': f'A raindrop of mass {g(m)} g falls from a height of {g(h / 1000)} km and hits the ground with a speed of {v} m s⁻¹. Find (i) the work done by gravity and (ii) the work done by the unknown resistive force of air. (g = 9.8 m s⁻²)',
            'answer': f'(i) {sig(Wg)} J (ii) {sig(Wr)} J', 'key': f'(i) W_g = mgh = {g(mk)} × 9.8 × {h} = {sig(Wg)} J (1). (ii) ΔK = ½mv² = {sig(0.5 * mk * v * v)} J = W_g + W_r ⇒ W_r = {sig(Wr)} J (2).'}


def c5s2_spring(r):
    m = r.choice([0.5, 1, 2, 5])
    v = r.choice([1, 1.5, 2, 3, 4])
    k = r.choice([100, 200, 500, 800, 1000])
    x = v * math.sqrt(m / k)
    return NUM(f'A block of mass {g(m)} kg moving at {g(v)} m s⁻¹ on a smooth floor hits a spring (k = {k} N m⁻¹) fixed at its far end. Find the maximum compression of the spring.', x * 100, 'cm',
               f'½mv² = ½kx² ⇒ x = v√(m/k) = {g(v)} × √({g(m)}/{k}) = {sig(x)} m = {{ans}}.', wrongs=[m * v * v / k * 100, v * m / k * 100, x * 141.4])


def c5s2_spring_friction(r):
    m = r.choice([1000, 1200, 800])
    v = r.choice([18, 36])
    k = r.choice([6.25e3, 5e3, 7.5e3, 1e4])
    mu = r.choice([0.3, 0.5])
    u = v * 5 / 18
    f = mu * m * G
    a = 0.5 * k
    x = (-f + math.sqrt(f * f + 4 * a * 0.5 * m * u * u)) / (2 * a)
    return {'stem': f'To simulate car accidents, a car of mass {m} kg moving at {v} km h⁻¹ on a horizontal road collides with a horizontally mounted spring of constant {g(k)} N m⁻¹. Taking the coefficient of kinetic friction as {mu}, find the maximum compression of the spring. (g = 9.8 m s⁻²)',
            'answer': f'{sig(x)} m', 'key': f'½mv² = ½kx² + μmgx (2): ½ × {m} × {g(u)}² = {g(0.5 * k)}x² + {g(f)}x (1); solve the quadratic, take the positive root: x = {sig(x)} m (2). (Without friction x would be {sig(u * math.sqrt(m / k))} m.)', 'gap': 'G5'}


def c5s2_same_p(r):
    m1, m2 = r.sample([1, 2, 3, 4, 5, 8, 10], 2)
    return NUM(f'Two bodies of masses {m1} kg and {m2} kg have equal linear momenta. Find the ratio of their kinetic energies K₁ : K₂.', m2 / m1, '',
               f'K = p²/2m, so K₁/K₂ = m₂/m₁ = {m2}/{m1} = {{ans}}.', wrongs=[m1 / m2, (m2 / m1) ** 2, math.sqrt(m2 / m1)]) | {'answer': f'{m2 // gcd(m1, m2)} : {m1 // gcd(m1, m2)}', 'distractors': [f'{m1 // gcd(m1, m2)} : {m2 // gcd(m1, m2)}', f'{(m2 // gcd(m1, m2)) ** 2} : {(m1 // gcd(m1, m2)) ** 2}', '1 : 1']}


c5s2_derive = pool_txt([
    ('State and prove the work-energy theorem for a constant force.', 'W_net = ΔK', 'v² − u² = 2as (1); multiply by m/2: ½mv² − ½mu² = mas = Fs (2); Fs = W, so W = ΔK (2).'),
    ('Derive the work-energy theorem for a variable force using calculus.', 'W = ∫F dx = K_f − K_i', 'dK/dt = mv dv/dt = Fv (2); dK = F dx (1); integrate from x_i to x_f (2).'),
    ('Show that the potential energy stored in a spring stretched by x is ½kx².', 'V = ½kx²', 'Spring force −kx (1); work by applied force ∫₀ˣ kx dx (2) = ½kx² stored as PE (2).'),
])


# st3 conservation of mechanical energy; power

c5s3_tf = tf_mcq('mechanical energy and power',
                 ['Mechanical energy is conserved when only conservative forces do work.', 'The SI unit of power is the watt (J s⁻¹).', '1 kWh = 3.6 × 10⁶ J.',
                  'Instantaneous power P = F·v.', 'Work done by a conservative force around a closed path is zero.'],
                 ['Friction is a conservative force.', 'The kilowatt-hour is a unit of power.', '1 horsepower = 1000 W.', 'Mechanical energy is conserved even when friction acts.',
                  'Power is a vector quantity.'])

c5s3_explain = pool_txt([
    ('Why is the kilowatt-hour a unit of energy and not of power?', 'It is power (kW) multiplied by time (h); 1 kWh = 3.6 × 10⁶ J.', 'Power × time = energy (1 mark); conversion (1 mark).'),
    ('A ball dropped from a height does not bounce back to the same height. Is energy conserved? Explain.', 'Total energy is conserved, but some mechanical energy changes into heat, sound and deformation.', 'Total vs mechanical energy (1 mark); forms (1 mark).'),
    ('What is a conservative force? Give one example of a conservative and one of a non-conservative force.', 'A force whose work depends only on the end points (zero around a closed path), e.g. gravity; friction is non-conservative.', 'Definition (1 mark); examples (1 mark).'),
    ('A bob is released from a horizontal position. Explain, using energy, why its speed is greatest at the lowest point.', 'Potential energy is least there, so (with mechanical energy conserved) kinetic energy is greatest.', 'K + U constant (1 mark); U minimum at bottom (1 mark).'),
])

c5s3_ar = pool_ar([
    ('Mechanical energy of a body sliding down a frictionless incline is conserved.', 'Only the conservative force of gravity does work on it.', 'a', 'The normal force does no work; R explains A.'),
    ('Work done by friction around a closed path is not zero.', 'Friction is a non-conservative force.', 'a', 'R explains A.'),
    ('The kilowatt-hour is a unit of power.', '1 kWh = 3.6 × 10⁶ J.', 'd', 'A is false (it is a unit of energy); R is true.'),
    ('For a vehicle moving at constant velocity on a rough road the engine power is F·v.', 'Instantaneous power is the dot product of force and velocity.', 'a', 'R explains A.'),
])


def c5s3_pump(r):
    V = r.choice([500, 1000, 1500, 2000, 3000])
    h = r.choice([10, 12, 15, 20, 25, 30])
    t = r.choice([5, 10, 15, 20, 30])
    eff = r.choice([1.0, 0.8, 0.75, 0.6])
    P = V * G * h / (t * 60) / eff
    return NUM(f'A pump on the ground floor of a building in {r.choice(CITIES)} can pump up water to fill a tank of volume {V} L on the roof {h} m high in {t} min. '
               f'{"If the efficiency of the pump is " + str(int(eff * 100)) + "%, how much electric power does it consume?" if eff < 1 else "Find the power of the pump."} (g = 9.8 m s⁻²; 1 L of water = 1 kg)',
               P, 'W', f'Useful power = mgh/t = {V} × 9.8 × {h}/({t} × 60) = {sig(V * G * h / (t * 60))} W{"; input = useful/efficiency" if eff < 1 else ""} = {{ans}}.',
               wrongs=[V * G * h / t, V * G * h / (t * 60) * eff, V * h / (t * 60)])


def c5s3_slide(r):
    h = r.choice([2, 3, 5, 7.5, 10, 20])
    v = math.sqrt(2 * G * h)
    return NUM(f'A child slides from rest down a frictionless slide in a park. The top is {g(h)} m above the bottom. Find the child\'s speed at the bottom. (g = 9.8 m s⁻²)', v, 'm s⁻¹',
               f'mgh = ½mv² ⇒ v = √(2gh) = √(2 × 9.8 × {g(h)}) = {{ans}} (independent of the shape of the slide).', wrongs=[2 * G * h, math.sqrt(G * h), G * h])


def c5s3_pendulum(r):
    L = r.choice([0.5, 1, 1.5, 2])
    th = r.choice([30, 37, 45, 60, 90])
    v = math.sqrt(2 * G * L * (1 - math.cos(math.radians(th))))
    return NUM(f'A pendulum bob on a string {g(L)} m long is pulled aside until the string makes {th}° with the vertical, and released. Find its speed at the lowest point. (g = 9.8 m s⁻²)', v, 'm s⁻¹',
               f'Height fall h = L(1 − cos θ) = {g(L * (1 - math.cos(math.radians(th))))} m; v = √(2gh) = {{ans}}.', wrongs=[math.sqrt(2 * G * L), math.sqrt(2 * G * L * math.cos(math.radians(th))), math.sqrt(G * L * (1 - math.cos(math.radians(th))))])


def c5s3_lift(r):
    M = r.choice([1500, 1800, 2000])
    f = r.choice([2000, 3000, 4000])
    v = r.choice([1, 2, 2.5, 3])
    P = (M * G + f) * v
    return {'stem': f'An elevator with a maximum load of {M} kg (elevator + passengers) moves up with a constant speed of {g(v)} m s⁻¹. The frictional force opposing the motion is {f} N. Find the minimum power delivered by the motor in watt and in horsepower. (g = 9.8 m s⁻²; 1 hp = 746 W)',
            'answer': f'{sig(P)} W ≈ {sig(P / 746)} hp', 'key': f'F = Mg + f = {g(M * G)} + {f} = {g(M * G + f)} N (1); P = Fv = {sig(P)} W (1); ÷ 746 = {sig(P / 746)} hp (1).'}


def c5s3_loop(r):
    L = r.choice([0.5, 1, 1.5, 2, 2.5])
    return {'stem': f'A bob of mass m tied to a string of length {g(L)} m is to complete a vertical circle. Find the minimum speeds at the lowest and highest points. (g = 9.8 m s⁻²)',
            'answer': f'Lowest {sig(math.sqrt(5 * G * L))} m s⁻¹; highest {sig(math.sqrt(G * L))} m s⁻¹',
            'key': f'At the top, T ≥ 0 ⇒ mv²/L ≥ mg ⇒ v_top = √(gL) = {sig(math.sqrt(G * L))} m s⁻¹ (1.5). Energy: ½mv_b² = ½mv_t² + 2mgL ⇒ v_b = √(5gL) = {sig(math.sqrt(5 * G * L))} m s⁻¹ (1.5).', 'gap': 'G5'}


def c5s3_bill(r):
    P = r.choice([60, 100, 750, 1000, 1500, 2000])
    h = r.choice([2, 3, 4, 5, 6, 8])
    rate = r.choice([5, 6, 6.5, 7, 8])
    app = {60: 'fan', 100: 'bulb', 750: 'water pump', 1000: 'iron', 1500: 'air conditioner', 2000: 'geyser'}[P]
    E = P * h * 30 / 1000
    return NUM(f'A {P} W {app} is used for {h} hours every day. How many units (kWh) of electricity does it consume in 30 days, and what is the cost at ₹{g(rate)} per unit?', E, 'kWh',
               f'E = P × t = {P} W × {h} h × 30 = {g(P * h * 30)} Wh = {{ans}}; cost = {g(E)} × {g(rate)} = ₹{g(E * rate)}.', wrongs=[P * h * 30, P * h / 1000, E * 3.6]) | {'answer': f'{g(E)} kWh; ₹{g(E * rate)}',
                                                                                                                                                   'distractors': [f'{g(E * 1000)} kWh; ₹{g(E * rate * 1000)}', f'{g(E / 30)} kWh; ₹{g(E * rate / 30)}', f'{g(E * 3.6)} kWh; ₹{g(E * 3.6 * rate)}']}


def c5s3_case(r):
    h = r.choice([20, 30, 40, 50])
    who = name(r)
    m = r.choice([400, 500, 600])
    eff = r.choice([0.6, 0.7, 0.8])
    return {'stem': (f'At a small hydroelectric plant in Himachal Pradesh, water falls through a height of {h} m and {m} kg of water passes through the turbine every second. {who} learns that the plant converts {int(eff * 100)}% of the water\'s potential energy into electrical energy. (g = 9.8 m s⁻²)\n'
                     '(i) Find the potential energy lost by the water per second. (ii) Find the electrical power output. (iii) Find the speed of the water just before reaching the turbine (no losses). (iv) Name one form into which the remaining energy is converted.'),
            'answer': f'(i) {sig(m * G * h)} J (ii) {sig(eff * m * G * h / 1000)} kW (iii) {sig(math.sqrt(2 * G * h))} m s⁻¹ (iv) heat/sound (internal energy)',
            'key': f'(i) mgh per second = {sig(m * G * h)} J (1). (ii) {int(eff * 100)}% of it = {sig(eff * m * G * h)} W (1). (iii) √(2gh) (1). (iv) heat, sound or friction losses (1).'}


# st4 collisions

c5s4_terms = term_mcq([('elastic collision', 'both total linear momentum and total kinetic energy are conserved'), ('inelastic collision', 'momentum is conserved but some kinetic energy is lost'),
                       ('completely inelastic collision', 'the bodies stick together after the collision'), ('head-on (one-dimensional) collision', 'the velocities before and after lie along the same line')],
                      'In a(n) {a},', 'Which type of collision is described: {b}?', '{a}: {b}.')

c5s4_tf = tf_mcq('collisions',
                 ['Linear momentum is conserved in all collisions if no external force acts.', 'In an elastic head-on collision of equal masses (one at rest), the velocities are exchanged.',
                  'In a completely inelastic collision, the loss of kinetic energy is maximum.', 'In an elastic collision the total kinetic energy after equals the total before.'],
                 ['Kinetic energy is conserved in all collisions.', 'Momentum is conserved only in elastic collisions.', 'In a completely inelastic collision no kinetic energy is lost.',
                  'In an elastic oblique collision of equal masses (one at rest), the bodies move off at 60° to each other.'])

c5s4_explain = pool_txt([
    ('Why is momentum conserved in a collision even though large forces act?', 'The forces are internal: equal and opposite on the two bodies, so the total momentum does not change.', 'Third law pairs (1 mark); no external impulse (1 mark).'),
    ('In nuclear reactors, why is a moderator with light nuclei (like heavy water) used to slow down neutrons?', 'In an elastic collision a neutron loses most energy when the target mass is close to its own.', 'Energy transfer 4m₁m₂/(m₁ + m₂)² is maximum for m₁ = m₂ (2 marks).'),
    ('Show that in a one-dimensional elastic collision of two equal masses, one initially at rest, the velocities are exchanged.', 'v₁ = (m₁ − m₂)u/(m₁ + m₂) = 0 and v₂ = 2m₁u/(m₁ + m₂) = u.', 'Formulae (1 mark); substitution m₁ = m₂ (1 mark).'),
])

c5s4_ar = pool_ar([
    ('In an elastic collision between equal masses, one at rest, the moving body stops.', 'v₁ = (m₁ − m₂)u₁/(m₁ + m₂).', 'a', 'With m₁ = m₂, v₁ = 0; R explains A.'),
    ('Kinetic energy is conserved in every collision.', 'Momentum is conserved in every collision without external forces.', 'd', 'A is false; R is true.'),
    ('When two bodies stick together after colliding, kinetic energy is lost.', 'Some kinetic energy is converted into heat, sound and deformation.', 'a', 'R explains A.'),
    ('In an oblique elastic collision of equal masses with one at rest, they move off at right angles.', 'Both momentum and kinetic energy are conserved.', 'a', 'u² = v₁² + v₂² with u = v₁ + v₂ forces v₁ ⊥ v₂; R explains A.'),
])


def c5s4_stick(r):
    m1, m2 = r.sample([1, 2, 3, 4, 5, 6, 8, 10], 2)
    u1 = r.choice([2, 3, 4, 5, 6, 8, 10])
    v = m1 * u1 / (m1 + m2)
    loss = 0.5 * m1 * u1 * u1 - 0.5 * (m1 + m2) * v * v
    return NUM2(f'A trolley of mass {m1} kg moving at {u1} m s⁻¹ collides with a stationary trolley of mass {m2} kg and they move off together. Find their common velocity and the loss in kinetic energy.',
                (v, loss), ('m s⁻¹', 'J'), f'm₁u₁ = (m₁ + m₂)v ⇒ v = {m1 * u1}/{m1 + m2} = {sig(v)} m s⁻¹; KE loss = {g(0.5 * m1 * u1 * u1)} − {sig(0.5 * (m1 + m2) * v * v)} = {sig(loss)} J.',
                wrongs=[(m1 * u1 / m2, loss), (u1 / 2, 0.25 * m1 * u1 * u1), (m2 * u1 / (m1 + m2), 0.5 * m1 * u1 * u1 - 0.5 * (m1 + m2) * (m2 * u1 / (m1 + m2)) ** 2)])


def c5s4_elastic(r):
    m1, m2 = r.sample([1, 2, 3, 4, 5, 6], 2)
    u = r.choice([2, 3, 4, 5, 6, 10])
    v1 = (m1 - m2) * u / (m1 + m2)
    v2 = 2 * m1 * u / (m1 + m2)
    return {'stem': f'A ball of mass {m1} kg moving at {u} m s⁻¹ makes a head-on elastic collision with a ball of mass {m2} kg at rest. Find their velocities after the collision.',
            'answer': f'v₁ = {sig(v1)} m s⁻¹, v₂ = {sig(v2)} m s⁻¹', 'key': f'v₁ = (m₁ − m₂)u/(m₁ + m₂) = {sig(v1)} m s⁻¹ ({"rebounds" if v1 < 0 else "moves on"}); v₂ = 2m₁u/(m₁ + m₂) = {sig(v2)} m s⁻¹.',
            'distractors': [f'v₁ = {sig(-v1) if v1 else "1.00"} m s⁻¹, v₂ = {sig(v2)} m s⁻¹', f'v₁ = 0 m s⁻¹, v₂ = {u} m s⁻¹' if m1 != m2 else 'v₁ = 1 m s⁻¹, v₂ = 1 m s⁻¹', f'v₁ = {sig(m1 * u / (m1 + m2))} m s⁻¹, v₂ = {sig(m1 * u / (m1 + m2))} m s⁻¹']}


def c5s4_ballistic(r):
    m = r.choice([10, 20, 25, 50])
    M = r.choice([1, 2, 4, 5])
    v = r.choice([200, 300, 400, 500])
    V = (m / 1000) * v / (M + m / 1000)
    h = V * V / (2 * G)
    return {'stem': f'A bullet of mass {m} g moving horizontally at {v} m s⁻¹ gets embedded in a wooden block of mass {M} kg hanging from long strings. To what height does the block rise? What fraction of the bullet\'s KE is lost? (g = 9.8 m s⁻²)',
            'answer': f'{sig(h * 100)} cm; {sig(M / (M + m / 1000) * 100)}% lost',
            'key': f'Momentum: V = mv/(m + M) = {sig(V)} m s⁻¹ (1); energy after collision: h = V²/2g = {sig(h)} m (1); fraction lost = M/(m + M) = {sig(M / (M + m / 1000) * 100)}% (1).'}


def c5s4_neutron(r):
    A, nm = r.choice([(2, 'deuterium'), (12, 'carbon'), (1, 'hydrogen'), (4, 'helium'), (16, 'oxygen')])
    f = 4 * A / (1 + A) ** 2
    return NUM(f'A neutron (mass 1 u) makes a head-on elastic collision with a {nm} nucleus (mass {A} u) at rest. What fraction of its kinetic energy is transferred to the nucleus?', f, '',
               f'Fraction = 4m₁m₂/(m₁ + m₂)² = 4 × {A}/{(1 + A) ** 2} = {{ans}}.', wrongs=[1 / A if A > 1 else 0.5, ((A - 1) / (A + 1)) ** 2 if A > 1 else 0.25, 2 * A / (1 + A) ** 2])


def c5s4_2d(r):
    m1, m2 = r.choice([(1000, 1500), (1200, 800), (1500, 1500), (1000, 2000)])
    v1, v2 = r.choice([(20, 15), (15, 10), (12, 16), (25, 10)])
    p = math.hypot(m1 * v1, m2 * v2)
    V = p / (m1 + m2)
    th = math.degrees(math.atan2(m2 * v2, m1 * v1))
    return {'stem': f'At a crossing, a car of mass {m1} kg moving east at {v1} m s⁻¹ collides with a car of mass {m2} kg moving north at {v2} m s⁻¹. They lock together. Find their velocity just after the collision.',
            'answer': f'{sig(V)} m s⁻¹ at {num(th, 1)}° north of east',
            'key': f'p_x = {m1 * v1}, p_y = {m2 * v2} kg m s⁻¹ (1); |p| = {sig(p)} (1); V = p/(m₁ + m₂) = {sig(V)} m s⁻¹ (0.5); tan θ = p_y/p_x ⇒ {num(th, 1)}° N of E (0.5).', 'gap': 'G5'}


def c5s4_bounce(r):
    h = r.choice([1, 2, 5, 10, 20])
    f = r.choice([10, 20, 25, 40, 50])
    n = r.randint(2, 4)
    hn = h * (1 - f / 100) ** n
    return {'stem': f'A ball dropped from a height of {h} m loses {f}% of its kinetic energy at every bounce on the floor. How high does it rise after the {ordn(n)} bounce? What is the total kinetic energy fraction lost by then?',
            'answer': f'{sig(hn)} m; {sig((1 - (1 - f / 100) ** n) * 100)}%',
            'key': f'After each bounce, height ∝ KE just after: h_k = h(1 − {f / 100:g})ᵏ (2); h_{n} = {h} × {1 - f / 100:g}^{n} = {sig(hn)} m (2); lost fraction 1 − {1 - f / 100:g}^{n} (1).', 'gap': 'G5'}


def c5s4_case(r):
    m1, m2, u = r.choice([(0.17, 0.17, 2), (0.16, 0.16, 3), (0.2, 0.2, 1.5)])
    who = name(r)
    return {'stem': (f'{who} is playing carrom-style billiards. A striker of mass {g(m1 * 1000)} g moving at {u} m s⁻¹ hits an identical stationary ball head-on.\n'
                     '(i) If the collision is elastic, find the velocities after collision. (ii) If instead they stick together, find the common velocity. (iii) Find the KE lost in case (ii). (iv) In which case is momentum conserved?'),
            'answer': f'(i) striker 0, ball {u} m s⁻¹ (ii) {g(u / 2)} m s⁻¹ (iii) {sig(0.25 * m1 * u * u)} J (iv) both',
            'key': f'(i) equal masses exchange velocities (1). (ii) v = u/2 (1). (iii) ½mu² − ½(2m)(u/2)² = ¼mu² = {sig(0.25 * m1 * u * u)} J (1). (iv) both (1).'}


c5s4_derive = pool_txt([
    ('Derive expressions for the final velocities of two bodies in a one-dimensional elastic collision, the second initially at rest.', 'v₁ = (m₁ − m₂)u₁/(m₁ + m₂), v₂ = 2m₁u₁/(m₁ + m₂)',
     'Momentum equation (1); KE equation (1); combine to get u₁ + v₁ = v₂ (1); solve (2).'),
    ('Show that in a completely inelastic collision of m₁ (speed u₁) with m₂ at rest, the loss of kinetic energy is ½ m₁m₂u₁²/(m₁ + m₂).', 'ΔK = ½ m₁m₂u₁²/(m₁ + m₂)',
     'v = m₁u₁/(m₁ + m₂) (2); ΔK = ½m₁u₁² − ½(m₁ + m₂)v² (2); simplify (1).'),
])


# ======================================================== families
FAMILIES = {
    S + '01-st1': [F('C1', 'D1', 'mcq', c1s1_units), F('C1', 'D2', 'mcq', c1s1_bigunits), F('C1', 'D2', 'mcq', c1s1_count_sf), F('C2', 'D2', 'explain', c1s1_explain),
                   F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c1s1_add_rule), F('C3', 'D3', 'numerical', c1s1_mul_rule), F('C3', 'D1', 'short', c1s1_round),
                   F('C4', 'D3', 'multi_step', c1s1_cube), F('C4', 'D4', 'multi_step', c1s1_density)],
    S + '01-st2': [F('C1', 'D2', 'mcq', c1s2_dimform), F('C1', 'D1', 'mcq', c1s2_same_pair), F('C2', 'D2', 'explain', c1s2_explain), F('C2', 'D3', 'mcq', c1s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c1s2_check_eq), F('C3', 'D3', 'numerical', c1s2_convert), F('C3', 'D4', 'multi_step', c1s2_derive), F('C4', 'D3', 'multi_step', c1s2_constants),
                   F('C4', 'D4', 'multi_step', c1s2_correct_eq), F('C4', 'D5', 'long', c1s2_planck), F('C3', 'D3', 'case', c1s2_case)],
    S + '01-st3': [F('C1', 'D2', 'mcq', c1s3_mcq), F('C2', 'D2', 'explain', c1s3_explain), F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)), F('C3', 'D2', 'multi_step', c1s3_mean_error),
                   F('C3', 'D3', 'short', c1s3_sum_err), F('C3', 'D3', 'numerical', c1s3_power_err), F('C3', 'D1', 'short', c1s3_lc), F('C4', 'D3', 'numerical', c1s3_g_err),
                   F('C4', 'D4', 'multi_step', c1s3_sphere), F('C3', 'D3', 'case', c1s3_case, kinds=('case',))],
    S + '02-st1': [F('C1', 'D2', 'mcq', c2s1_tf), F('C1', 'D1', 'mcq', c2s1_terms), F('C2', 'D2', 'explain', c2s1_explain), F('C2', 'D3', 'mcq', c2s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'multi_step', c2s1_walk), F('C3', 'D3', 'numerical', c2s1_halves), F('C3', 'D1', 'short', c2s1_kmh), F('C4', 'D3', 'multi_step', c2s1_xt),
                   F('C4', 'D4', 'multi_step', c2s1_market), F('C3', 'D3', 'case', c2s1_case)],
    S + '02-st2': [F('C1', 'D2', 'mcq', c2s2_tf), F('C1', 'D1', 'mcq', c2s2_which_eq), F('C2', 'D2', 'explain', c2s2_explain), F('C2', 'D3', 'mcq', c2s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c2s2_vuat), F('C3', 'D3', 'numerical', c2s2_brake), F('C3', 'D4', 'multi_step', c2s2_stopping), F('C4', 'D3', 'numerical', c2s2_nth),
                   F('C4', 'D4', 'multi_step', c2s2_catch), F('C4', 'D4', 'long', c2s2_train), F('C4', 'D5', 'long', c2s2_two_intervals), F('C2', 'D3', 'long', c2s2_derive)],
    S + '02-st3': [F('C1', 'D2', 'mcq', c2s3_graphs), F('C1', 'D1', 'mcq', c2s3_tf), F('C2', 'D2', 'explain', c2s3_explain), F('C2', 'D3', 'mcq', c2s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c2s3_drop), F('C3', 'D3', 'numerical', c2s3_up), F('C3', 'D4', 'multi_step', c2s3_tower), F('C4', 'D3', 'multi_step', c2s3_vt_area),
                   F('C3', 'D1', 'short', c2s3_rect), F('C4', 'D4', 'multi_step', c2s3_balloon), F('C3', 'D3', 'numerical', c2s3_nth_fall), F('C3', 'D3', 'case', c2s3_case)],
    S + '02-st4': [F('C1', 'D2', 'mcq', c2s4_tf), F('C2', 'D2', 'explain', c2s4_explain), F('C2', 'D3', 'mcq', c2s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c2s4_rel),
                   F('C3', 'D3', 'numerical', c2s4_cross), F('C4', 'D3', 'multi_step', c2s4_chase), F('C3', 'D1', 'short', c2s4_simple)],
    S + '03-st1': [F('C1', 'D2', 'mcq', c3s1_tf), F('C1', 'D1', 'mcq', c3s1_classify), F('C2', 'D2', 'explain', c3s1_explain), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s1_resultant), F('C3', 'D3', 'numerical', c3s1_resolve), F('C3', 'D4', 'multi_step', c3s1_ijk), F('C4', 'D3', 'numerical', c3s1_equal_mag),
                   F('C4', 'D4', 'multi_step', c3s1_walk), F('C3', 'D2', 'mcq', c3s1_range), F('C3', 'D1', 'short', c3s1_unit)],
    S + '03-st2': [F('C1', 'D2', 'mcq', c3s2_tf), F('C1', 'D1', 'mcq', c3s2_relform), F('C2', 'D2', 'explain', c3s2_explain), F('C2', 'D3', 'mcq', c3s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s2_umbrella), F('C3', 'D3', 'numerical', c3s2_river), F('C3', 'D4', 'multi_step', c3s2_straight), F('C4', 'D3', 'multi_step', c3s2_rt),
                   F('C4', 'D4', 'multi_step', c3s2_r0)],
    S + '03-st3': [F('C1', 'D2', 'mcq', c3s3_formula), F('C1', 'D1', 'mcq', c3s3_tf), F('C2', 'D2', 'explain', c3s3_explain), F('C2', 'D3', 'mcq', c3s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s3_thr), F('C3', 'D3', 'numerical', c3s3_horiz), F('C3', 'D4', 'multi_step', c3s3_angle_for_range), F('C4', 'D3', 'numerical', c3s3_ratio),
                   F('C4', 'D4', 'multi_step', c3s3_cricketer), F('C4', 'D5', 'long', c3s3_aircraft), F('C2', 'D3', 'long', c3s3_derive), F('C3', 'D3', 'case', c3s3_case)],
    S + '03-st4': [F('C1', 'D2', 'mcq', c3s4_tf), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c3s4_speed),
                   F('C3', 'D3', 'numerical', c3s4_acc), F('C3', 'D1', 'short', c3s4_omega), F('C4', 'D3', 'multi_step', c3s4_loop), F('C4', 'D4', 'multi_step', c3s4_insect),
                   F('C4', 'D4', 'numerical', c3s4_earth)],
    S + '04-st1': [F('C1', 'D2', 'mcq', c4s1_tf), F('C1', 'D1', 'mcq', c4s1_terms), F('C2', 'D2', 'explain', c4s1_explain), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c4s1_fma), F('C3', 'D3', 'numerical', c4s1_bat), F('C3', 'D4', 'multi_step', c4s1_recoil), F('C4', 'D3', 'numerical', c4s1_block),
                   F('C4', 'D4', 'multi_step', c4s1_mgun)],
    S + '04-st2': [F('C1', 'D2', 'mcq', c4s2_tf), F('C2', 'D2', 'explain', c4s2_explain), F('C2', 'D3', 'mcq', c4s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c4s2_lift),
                   F('C3', 'D3', 'numerical', c4s2_push), F('C3', 'D4', 'multi_step', c4s2_atwood), F('C4', 'D3', 'multi_step', c4s2_side), F('C4', 'D4', 'long', c4s2_three)],
    S + '04-st3': [F('C1', 'D2', 'mcq', c4s3_tf), F('C1', 'D1', 'mcq', c4s3_terms), F('C2', 'D2', 'explain', c4s3_explain), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c4s3_limit), F('C3', 'D3', 'numerical', c4s3_slide), F('C3', 'D4', 'numerical', c4s3_incline), F('C3', 'D1', 'short', c4s3_repose),
                   F('C4', 'D3', 'multi_step', c4s3_truck), F('C4', 'D4', 'multi_step', c4s3_up), F('C4', 'D5', 'long', c4s3_angle_pull), F('C3', 'D3', 'case', c4s3_case)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_tf), F('C2', 'D2', 'explain', c4s4_explain), F('C2', 'D3', 'mcq', c4s4_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c4s4_level),
                   F('C3', 'D3', 'numerical', c4s4_bank), F('C4', 'D4', 'long', c4s4_bank_mu), F('C3', 'D1', 'short', c4s4_cyclist), F('C4', 'D3', 'multi_step', c4s4_string)],
    S + '05-st1': [F('C1', 'D2', 'mcq', c5s1_tf), F('C1', 'D1', 'mcq', c5s1_terms), F('C2', 'D2', 'explain', c5s1_explain), F('C2', 'D3', 'mcq', c5s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s1_wfd), F('C3', 'D3', 'numerical', c5s1_dot), F('C3', 'D3', 'numerical', c5s1_spring_work), F('C4', 'D3', 'multi_step', c5s1_fx_graph),
                   F('C4', 'D4', 'multi_step', c5s1_incline_work)],
    S + '05-st2': [F('C1', 'D2', 'mcq', c5s2_tf), F('C2', 'D2', 'explain', c5s2_explain), F('C2', 'D3', 'mcq', c5s2_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c5s2_ke),
                   F('C3', 'D3', 'numerical', c5s2_wet), F('C3', 'D4', 'multi_step', c5s2_raindrop), F('C4', 'D3', 'numerical', c5s2_spring), F('C4', 'D5', 'long', c5s2_spring_friction),
                   F('C3', 'D1', 'short', c5s2_same_p), F('C2', 'D3', 'long', c5s2_derive)],
    S + '05-st3': [F('C1', 'D2', 'mcq', c5s3_tf), F('C2', 'D2', 'explain', c5s3_explain), F('C2', 'D3', 'mcq', c5s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c5s3_pump),
                   F('C3', 'D3', 'numerical', c5s3_slide), F('C3', 'D3', 'numerical', c5s3_pendulum), F('C4', 'D3', 'multi_step', c5s3_lift), F('C4', 'D4', 'multi_step', c5s3_loop),
                   F('C3', 'D1', 'short', c5s3_bill), F('C3', 'D3', 'case', c5s3_case)],
    S + '05-st4': [F('C1', 'D2', 'mcq', c5s4_tf), F('C1', 'D1', 'mcq', c5s4_terms), F('C2', 'D2', 'explain', c5s4_explain), F('C2', 'D3', 'mcq', c5s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c5s4_stick), F('C3', 'D3', 'numerical', c5s4_elastic), F('C3', 'D4', 'multi_step', c5s4_ballistic), F('C4', 'D3', 'numerical', c5s4_neutron),
                   F('C4', 'D4', 'long', c5s4_2d), F('C4', 'D5', 'long', c5s4_bounce), F('C3', 'D3', 'case', c5s4_case), F('C2', 'D3', 'long', c5s4_derive)],
}
FAMILIES = polish(FAMILIES)
