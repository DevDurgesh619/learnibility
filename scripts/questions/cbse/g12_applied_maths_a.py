"""CBSE class 12 Applied Mathematics (241): families for ch01 (numbers, quantification and numerical
applications), ch02 (numerical inequalities) and ch03 (matrices and determinants)."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import SUP
from g12_applied_maths_h import (F, Q, ar, mcq, mcqbank, arbank, xbank, fz, fpar, term, dist3, name, two_names, inr, num,
                                 CITIES, hm, mixed, ratio, ratio3, rs, interval, reuse, det, mstr, unimod, lin_eq)

S = 'cbse-g12-applied-maths-ch'
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def _order(b, n):
    k, x = 1, b % n
    while x != 1:
        x = x * b % n
        k += 1
    return k


# ======================================================================= ch01 st1 modulo arithmetic

a1s1_mcq = mcqbank([
    ('For integers a, b and a natural number n, a ≡ b (mod n) means …', 'n divides a − b', ['a divides b', 'a − b = n', 'n divides a + b'], 'Definition of congruence modulo n.'),
    ('If a ≡ b (mod n) and c ≡ d (mod n), then a + c ≡ …', 'b + d (mod n)', ['b − d (mod n)', 'bd (mod n)', 'b + d (mod 2n)'], 'Addition property of congruences.'),
    ('If a ≡ b (mod n) and c ≡ d (mod n), then ac ≡ …', 'bd (mod n)', ['b + d (mod n)', 'bd (mod n²)', 'ad (mod 2n)'], 'Multiplication property of congruences.'),
    ('If a ≡ b (mod n), then for every natural number k, aᵏ ≡ …', 'bᵏ (mod n)', ['kb (mod n)', 'b (mod kn)', 'bᵏ (mod nᵏ)'], 'Power property (repeated multiplication).'),
    ('The possible remainders on division by 7 are …', '0, 1, 2, 3, 4, 5, 6', ['1, 2, 3, 4, 5, 6, 7', '0, 1, 2, …, 7', '1, 2, 3, 4, 5, 6'], 'Remainders lie between 0 and n − 1.'),
    ('Congruence modulo n on the set of integers is …', 'an equivalence relation', ['reflexive only', 'symmetric but not transitive', 'neither reflexive nor symmetric'], 'It is reflexive, symmetric and transitive.'),
    ('Clock arithmetic on a 12-hour clock is arithmetic modulo …', '12', ['24', '60', '7'], 'The hours repeat every 12.'),
    ('Days of the week repeat in arithmetic modulo …', '7', ['12', '30', '365'], 'A week has 7 days.'),
    ('a mod n always lies in the set …', '{0, 1, …, n − 1}', ['{1, 2, …, n}', '{−n, …, n}', '{0, 1, …, n}'], 'Least non-negative remainder.'),
    ('If a ≡ b (mod n), then a − b is …', 'a multiple of n', ['equal to n', 'less than n', 'a factor of n'], 'n | (a − b).'),
])


def a1s1_mod(r):
    n = r.randint(3, 13)
    a = r.choice([r.randint(-120, -5), r.randint(20, 400)])
    if a % n == 0:
        raise ValueError
    q, rem = a // n, a % n
    stem = r.choice([f'Find {fz(a)} mod {n}.', f'Find the least non-negative integer r such that {fz(a)} ≡ r (mod {n}).'])
    return Q(stem, str(rem), f'{fz(a)} = {n} × {fpar(q)} + {rem}, and 0 ≤ {rem} < {n}.',
             dist3(str(rem), [abs(a) % n, n - rem, (rem + 1) % n, rem + n, abs(q)]))


def a1s1_cong(r):
    n = r.randint(4, 13)
    a = r.randint(20, 300)
    yes = r.random() < 0.5
    b = a - n * r.randint(2, 15) if yes else a - n * r.randint(2, 15) + r.randint(1, n - 1)
    if b <= 0:
        raise ValueError
    d = a - b
    ans = 'Yes' if yes else 'No'
    return Q(f'Is {a} ≡ {b} (mod {n})? Justify.', ans,
             f'{a} − {b} = {d}, which ' + (f'is divisible by {n} ({d} = {n} × {d // n}), so the congruence holds.' if yes else f'is not divisible by {n} (remainder {d % n}), so the congruence does not hold.'))


def a1s1_arith(r):
    n = r.randint(5, 13)
    a, b = r.randint(100, 999), r.randint(100, 999)
    op = r.choice(['+', '×', '−'])
    val = {'+': a + b, '×': a * b, '−': a - b}[op] % n
    ra, rb = a % n, b % n
    comb = {'+': f'{ra} + {rb}', '×': f'{ra} × {rb}', '−': f'{ra} − {rb}'}[op]
    return Q(f'Using the properties of congruence, find ({a} {op} {b}) mod {n}.', str(val),
             f'{a} ≡ {ra} and {b} ≡ {rb} (mod {n}); so ({a} {op} {b}) ≡ {comb} ≡ {val} (mod {n}).',
             dist3(str(val), [(ra + rb) % n if op != '+' else (ra * rb) % n, (val + 1) % n, ra, (n - val) % n, rb]))


def a1s1_power(r):
    while True:
        n = r.choice([5, 7, 9, 11, 13, 10, 8])
        b = r.randint(2, 12)
        if math.gcd(b, n) == 1 and b % n not in (0, 1):
            break
    k = _order(b, n)
    e = r.randint(25, 160)
    val = pow(b, e, n)
    q, s = divmod(e, k)
    E = lambda t: str(t).translate(SUP)
    tail = f' × {b}{E(s)}' if s else ''
    return Q(f'Find the remainder when {b}{E(e)} is divided by {n}.', str(val),
             f'{b}{E(k)} ≡ 1 (mod {n}) (1 mark); {e} = {k} × {q} + {s}, so {b}{E(e)} = ({b}{E(k)}){E(q)}{tail} ≡ {val} (mod {n}) (2 marks).'.replace('¹ ', ' '),
             dist3(str(val), [pow(b, s + 1, n), (val + 1) % n, b % n, (n - val) % n, pow(b, e % n, n)]))


def a1s1_solve(r):
    n = r.choice([5, 7, 8, 9, 11, 12, 13])
    a = r.choice([x for x in range(2, n) if math.gcd(x, n) == 1])
    c = r.randint(1, n - 1)
    x = next(t for t in range(n) if (a * t - c) % n == 0)
    others = [x + n * k for k in range(1, 3)]
    return Q(f'Find the least non-negative integer x such that {a}x ≡ {c} (mod {n}), and write two more solutions.', f'x = {x}; e.g. {others[0]}, {others[1]}',
             f'Test x = 0, 1, …, {n - 1}: {a} × {x} = {a * x} ≡ {c} (mod {n}) (2 marks); all solutions are x = {x} + {n}k (1 mark).',
             dist3(f'x = {x}; e.g. {others[0]}, {others[1]}', [f'x = {(c * a) % n}; e.g. {(c * a) % n + n}, {(c * a) % n + 2 * n}', f'x = {(x + 1) % n}; e.g. {(x + 1) % n + n}, {(x + 1) % n + 2 * n}', f'x = {c}; e.g. {c + n}, {c + 2 * n}']))


def a1s1_day(r):
    d0 = r.randrange(7)
    N = r.randint(40, 500)
    ans = DAYS[(d0 + N) % 7]
    who = name(r)
    return Q(f'Today is {DAYS[d0]}. {who}\'s exam is after {N} days. On which day of the week is the exam?', ans,
             f'{N} = 7 × {N // 7} + {N % 7}, so the day moves {N % 7} place(s) on from {DAYS[d0]}: {ans}.',
             dist3(ans, [DAYS[(d0 + N % 7 + 1) % 7], DAYS[(d0 - N) % 7], DAYS[(d0 + N % 7 + 6) % 7], DAYS[d0]]))


def a1s1_clock(r):
    h = r.randint(0, 23)
    T = r.randint(30, 400)
    end = (h + T) % 24
    return Q(f'A machine on a factory floor in {r.choice(CITIES)} is switched on at {h:02d}:00 (24-hour clock) and runs for {T} hours. At what time (24-hour clock) does it stop?', f'{end:02d}:00',
             f'({h} + {T}) mod 24 = {h + T} mod 24 = {end}.', dist3(f'{end:02d}:00', [f'{(h + T) % 12:02d}:00', f'{(end + 1) % 24:02d}:00', f'{(T % 24):02d}:00', f'{(end + 12) % 24:02d}:00']))


def a1s1_ar(r):
    k = r.randint(0, 3)
    n = r.randint(4, 12)
    if k == 0:
        a = r.randint(30, 200)
        b = a - n * r.randint(2, 9)
        return ar(f'{a} ≡ {b} (mod {n}).', 'a ≡ b (mod n) if and only if n divides a − b.', 'a', f'{a} − {b} = {a - b} is a multiple of {n}.')
    if k == 1:
        a = r.randint(30, 200)
        b = a - n * r.randint(2, 9) - r.randint(1, n - 1)
        return ar(f'{a} ≡ {b} (mod {n}).', 'a ≡ b (mod n) if and only if n divides a − b.', 'd', f'{a} − {b} = {a - b} is not a multiple of {n}; A false, R true.')
    if k == 2:
        a = r.randint(-90, -10)
        if a % n == 0:
            raise ValueError
        return ar(f'{a} mod {n} = {a % n}.', f'The value of a mod n is the remainder r with 0 ≤ r < n in a = nq + r.', 'a', f'{a} = {n} × ({a // n}) + {a % n}.')
    return ar('If 2x ≡ 2y (mod 6), then x ≡ y (mod 6).', 'A common factor can be cancelled from a congruence only when it is coprime to the modulus.', 'd',
              'x = 0, y = 3 gives 0 ≡ 6 (mod 6) but 0 ≢ 3 (mod 6); A false, R true.')


def a1s1_explain(r):
    return xbank([
        ('Show that congruence modulo n is an equivalence relation on Z.', 'It is reflexive, symmetric and transitive.',
         'n | (a − a) = 0; if n | (a − b) then n | (b − a); if n | (a − b) and n | (b − c) then n | (a − c) (2 marks).'),
        ('Explain why a mod n cannot be equal to n.', 'Remainders on division by n lie in 0, 1, …, n − 1.', 'If the remainder were n, one more n could be taken out (2 marks).'),
        ('Explain how clock time on a 12-hour clock uses modulo arithmetic.', 'Hours after 12 wrap round: time ≡ hours (mod 12).', '12 is treated as 0; add hours and reduce modulo 12 (2 marks).'),
        ('Explain why 10ⁿ ≡ 1 (mod 9) for every natural number n.', '10 ≡ 1 (mod 9), so 10ⁿ ≡ 1ⁿ = 1 (mod 9).', 'Power property of congruences (2 marks).'),
    ])(r)


def a1s1_case(r):
    who = name(r)
    d0 = r.randrange(7)
    N = r.randint(60, 300)
    h = r.randint(6, 22)
    T = r.randint(30, 150)
    b, e, n = r.choice([(2, r.randint(30, 90), 7), (3, r.randint(30, 90), 7), (4, r.randint(30, 90), 5), (2, r.randint(30, 90), 5)])
    return Q((f'{who} manages shift schedules at a factory in {r.choice(CITIES)}. (i) Today is {DAYS[d0]}; a machine is due for service after {N} days. On which day is the service? '
              f'(ii) A batch starts at {h:02d}:00 and takes {T} hours. At what time (24-hour clock) does it end? (iii) Find the remainder when {b}{str(e).translate(SUP)} is divided by {n}.'),
             f'(i) {DAYS[(d0 + N) % 7]} (ii) {(h + T) % 24:02d}:00 (iii) {pow(b, e, n)}',
             f'(i) {N} mod 7 = {N % 7} (1 mark) (ii) ({h} + {T}) mod 24 = {(h + T) % 24} (1 mark) (iii) cycle of powers modulo {n} (2 marks).')


# ======================================================================= ch01 st2 alligation and mixture

GOODS = [('rice', 'kg'), ('tea', 'kg'), ('sugar', 'kg'), ('pulses', 'kg'), ('wheat', 'kg'), ('coffee powder', 'kg'), ('oil', 'L'), ('ghee', 'kg')]

a1s2_mcq = mcqbank([
    ('By the rule of alligation, if c < m < d are the cost prices (per unit) of the cheaper, mean and dearer items, then (cheaper quantity) : (dearer quantity) = …', '(d − m) : (m − c)', ['(m − c) : (d − m)', '(d − c) : (m − c)', 'c : d'], 'Rule of alligation.'),
    ('The mean price of a mixture of two varieties always lies …', 'between the two prices', ['below the cheaper price', 'above the dearer price', 'at the average of the two prices'], 'Weighted average of the two prices.'),
    ('Alligation is a rule to find …', 'the ratio in which ingredients at given prices must be mixed to get a mixture at a given price', ['the profit on a mixture', 'the selling price of a mixture', 'the total quantity of a mixture'], 'Definition.'),
    ('If x litres are taken out of a vessel of V litres of milk and replaced by water, and this is done n times, the milk left is …', 'V(1 − x/V)ⁿ litres', ['V(1 − x/V) litres', 'V − nx litres', 'V(x/V)ⁿ litres'], 'Repeated replacement.'),
    ('Two varieties priced ₹40 and ₹60 per kg are mixed in the ratio 1 : 1. The mean price is …', '₹50 per kg', ['₹48 per kg', '₹52 per kg', '₹100 per kg'], '(40 + 60)/2 = 50.'),
    ('The mean price of a mixture is the …', 'weighted average of the prices, weighted by the quantities', ['simple average of the prices', 'difference of the prices', 'larger of the two prices'], 'Definition.'),
])


def _cmd(r):
    while True:
        c = r.randint(20, 120)
        d = c + r.randint(6, 60)
        m = r.randint(c + 2, d - 2)
        if (d - m) != (m - c):
            return c, d, m


def a1s2_ratio(r):
    c, d, m = _cmd(r)
    g, u = r.choice(GOODS)
    ans = ratio(d - m, m - c)
    return Q(f'In what ratio must {g} costing ₹{c} per {u} be mixed with {g} costing ₹{d} per {u} so that the mixture costs ₹{m} per {u}?', ans,
             f'By alligation, cheaper : dearer = (d − m) : (m − c) = ({d} − {m}) : ({m} − {c}) = {d - m} : {m - c} = {ans}.',
             dist3(ans, [ratio(m - c, d - m), ratio(d - c, m - c), ratio(c, d), ratio(d - m, d - c)]))


def a1s2_mean(r):
    g, u = r.choice(GOODS)
    c, d = r.randint(20, 90), r.randint(95, 200)
    T = r.choice([5, 8, 10, 20, 25, 40, 50])
    x = r.randint(1, T - 1)
    y = T - x
    mp = Fr(x * c + y * d, x + y)
    ans = f'₹{num(float(mp))} per {u}'
    return Q(f'A trader mixes {x} {u} of {g} costing ₹{c} per {u} with {y} {u} of {g} costing ₹{d} per {u}. Find the cost price of the mixture per {u}.', ans,
             f'Mean price = ({x} × {c} + {y} × {d})/({x} + {y}) = {x * c + y * d}/{x + y} = {num(float(mp))}.',
             dist3(ans, [f'₹{num((c + d) / 2)} per {u}', f'₹{num(float(Fr(x * d + y * c, x + y)))} per {u}', f'₹{num(float(mp) + 1)} per {u}']))


def a1s2_water(r):
    p = r.choice([40, 45, 48, 50, 54, 56, 60, 64, 72])
    m = r.randint(p // 2, p - 2)
    ans = ratio(p - m, m)
    return Q(f'In what ratio must water be mixed with milk costing ₹{p} per litre so that the mixture is worth ₹{m} per litre?', f'water : milk = {ans}',
             f'Water costs ₹0. By alligation, water : milk = ({p} − {m}) : ({m} − 0) = {ans}.',
             dist3(f'water : milk = {ans}', [f'water : milk = {ratio(m, p - m)}', f'water : milk = {ratio(p - m, p)}', f'water : milk = {ratio(m, p)}']))


def a1s2_replace(r):
    V = r.choice([20, 40, 50, 60, 80, 100])
    x = r.choice([d for d in (2, 4, 5, 8, 10, 20) if d < V and V % d == 0 and Fr(d, V) <= Fr(1, 4)])
    n = r.choice([2, 3])
    left = Fr(V) * (1 - Fr(x, V)) ** n
    water = V - left
    who = name(r)
    return Q(f'A vessel at {who}\'s dairy contains {V} litres of milk. {x} litres of milk are taken out and replaced by water. This process is done {n} times in all. How much milk is now in the vessel, and what is the ratio of milk to water?',
             f'{num(float(left), 3)} litres; milk : water = {ratio(left, water)}',
             f'Milk left = V(1 − x/V)ⁿ = {V}(1 − {x}/{V})^{n} = {num(float(left), 3)} L (2 marks); water = {num(float(water), 3)} L, ratio {ratio(left, water)} (1 mark).',
             dist3(f'{num(float(left), 3)} litres; milk : water = {ratio(left, water)}', [f'{V - n * x} litres; milk : water = {ratio(V - n * x, n * x)}', f'{num(float(V * (1 - Fr(x, V))), 3)} litres; milk : water = {ratio(V - x, x)}', f'{num(float(left), 3)} litres; milk : water = {ratio(water, left)}']))


def a1s2_two(r):
    while True:
        a, b, c, d = r.randint(1, 7), r.randint(1, 7), r.randint(1, 7), r.randint(1, 7)
        if Fr(a, a + b) != Fr(c, c + d):
            break
    p, q = r.choice([(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)])
    milk = p * Fr(a, a + b) + q * Fr(c, c + d)
    water = p * Fr(b, a + b) + q * Fr(d, c + d)
    ans = ratio(milk, water)
    how = 'equal quantities of the two are' if p == q else f'the two are mixed in the ratio {p} : {q} and'
    return Q(f'Two vessels contain milk and water in the ratios {a} : {b} and {c} : {d}. If {how} poured into a third vessel, find the ratio of milk to water in it.', ans,
             f'Milk = {p}({a}/{a + b}) + {q}({c}/{c + d}) = {fz(milk)}, water = {p}({b}/{a + b}) + {q}({d}/{c + d}) = {fz(water)} (2 marks); ratio {ans} (1 mark).'.replace('1(', '('),
             dist3(ans, [ratio(a + c, b + d), ratio(water, milk), ratio(a * c, b * d), ratio(milk + 1, water)]))


def a1s2_qty(r):
    while True:
        c, d, m = _cmd(r)
        Qd = r.randint(5, 60)
        x = Fr(Qd * (d - m), m - c)
        if x.denominator == 1:
            break
    g, u = r.choice(GOODS)
    return Q(f'How many {u} of {g} costing ₹{c} per {u} must be mixed with {Qd} {u} of {g} costing ₹{d} per {u} so that the mixture costs ₹{m} per {u}?', f'{fz(x)} {u}',
             f'Cheaper : dearer = ({d} − {m}) : ({m} − {c}) = {ratio(d - m, m - c)} (1 mark); cheaper = {Qd} × {d - m}/{m - c} = {fz(x)} {u} (2 marks).',
             dist3(f'{fz(x)} {u}', [f'{fz(Fr(Qd * (m - c), d - m))} {u}', f'{fz(x + Qd)} {u}', f'{Qd} {u}', f'{fz(x / 2)} {u}']))


def a1s2_profit(r):
    while True:
        c, d, m = _cmd(r)
        x, y = [int(t) for t in ratio(d - m, m - c).split(' : ')]
        sp = m + r.choice([2, 4, 5, 6, 8, 10, 12, 15])
        prof = Fr(sp - m, m) * 100
        if prof.denominator in (1, 2, 4, 5) and x + y <= 30:
            break
    g, u = r.choice(GOODS)
    who = name(r)
    return Q(f'{who}, a grocer, mixes two varieties of {g} costing ₹{c} and ₹{d} per {u} in the ratio {x} : {y} and sells the mixture at ₹{sp} per {u}. Find the profit per cent.', f'{num(float(prof))}%',
             f'Cost of mixture = ({x} × {c} + {y} × {d})/{x + y} = ₹{m} per {u} (2 marks); profit % = ({sp} − {m})/{m} × 100 = {num(float(prof))}% (1 mark).',
             dist3(f'{num(float(prof))}%', [f'{num(float(Fr(sp - m, sp) * 100))}%', f'{num(float((sp - Fr(c + d, 2)) / Fr(c + d, 2) * 100))}%', f'{sp - m}%']))


def a1s2_ar(r):
    k = r.randint(0, 2)
    if k == 0:
        c, d, m = _cmd(r)
        return ar(f'Two varieties costing ₹{c} and ₹{d} per kg must be mixed in the ratio {ratio(d - m, m - c)} to get a mixture costing ₹{m} per kg.', 'Cheaper : dearer = (d − m) : (m − c).', 'a', 'Rule of alligation.')
    if k == 1:
        c, d = r.randint(20, 60), r.randint(70, 120)
        return ar(f'A mixture of varieties costing ₹{c} and ₹{d} per kg can cost ₹{d + r.randint(2, 20)} per kg.', 'The mean price lies between the cheaper and the dearer prices.', 'd', 'The mean price must lie between the two prices; A false, R true.')
    c, d = r.randint(20, 60), r.randint(70, 120)
    return ar(f'Varieties costing ₹{c} and ₹{d} per kg mixed in equal quantities give a mixture costing ₹{fz(Fr(c + d, 2))} per kg.', 'The mean price is always the simple average of the two prices.', 'c', 'A is true for equal quantities; R is false in general (it is a weighted average).')


def a1s2_case(r):
    who = name(r)
    c, d, m = _cmd(r)
    x, y = [int(t) for t in ratio(d - m, m - c).split(' : ')]
    T = (x + y) * r.randint(2, 6)
    sp = m + r.choice([4, 5, 6, 10])
    return Q((f'{who} runs a tea stall in {r.choice(CITIES)} and blends two kinds of tea leaves costing ₹{c} and ₹{d} per kg to get a blend costing ₹{m} per kg. '
              f'(i) In what ratio must they be mixed? (ii) How much of each is needed for {T} kg of the blend? (iii) If the blend is sold at ₹{sp} per kg, find the total profit on {T} kg.'),
             f'(i) {x} : {y} (ii) {T * x // (x + y)} kg and {T * y // (x + y)} kg (iii) ₹{(sp - m) * T}',
             '(i) alligation (1 mark) (ii) divide in the ratio (1 mark) (iii) profit per kg × quantity (2 marks).')


# ======================================================================= ch01 st3 boats and streams; pipes and cisterns

a1s3_mcq = mcqbank([
    ('If the speed of a boat in still water is u km/h and the speed of the stream is v km/h (u > v), its downstream speed is …', '(u + v) km/h', ['(u − v) km/h', 'uv km/h', '(u + v)/2 km/h'], 'The stream helps the boat.'),
    ('If a boat\'s downstream speed is a km/h and upstream speed is b km/h, the speed of the stream is …', '(a − b)/2 km/h', ['(a + b)/2 km/h', 'a − b km/h', 'ab km/h'], 'a = u + v, b = u − v.'),
    ('If a boat\'s downstream speed is a km/h and upstream speed is b km/h, its speed in still water is …', '(a + b)/2 km/h', ['(a − b)/2 km/h', 'a + b km/h', '2ab/(a + b) km/h'], 'Add a = u + v and b = u − v.'),
    ('A pipe that empties a tank is called …', 'an outlet', ['an inlet', 'a cistern', 'a leak-proof pipe'], 'Terminology.'),
    ('If a pipe fills a tank in x hours, the part filled in 1 hour is …', '1/x', ['x', 'x − 1', '1 − 1/x'], 'Unitary method.'),
    ('Pipes A and B fill a tank in a and b hours. Together they fill it in …', 'ab/(a + b) hours', ['(a + b)/2 hours', 'a + b hours', '(a + b)/ab hours'], '1/a + 1/b = (a + b)/ab.'),
    ('An inlet fills a tank in a hours and an outlet empties it in b hours (b > a). With both open, the tank fills in …', 'ab/(b − a) hours', ['ab/(a + b) hours', '(b − a) hours', 'ab/(a − b) hours'], '1/a − 1/b = (b − a)/ab.'),
])


def a1s3_speeds(r):
    u, v = r.randint(6, 25), r.randint(1, 5)
    if v >= u:
        raise ValueError
    ans = f'downstream {u + v} km/h, upstream {u - v} km/h'
    return Q(f'A boat moves at {u} km/h in still water and the stream flows at {v} km/h. Find its downstream and upstream speeds.', ans,
             f'Downstream u + v = {u + v}; upstream u − v = {u - v}.', dist3(ans, [f'downstream {u - v} km/h, upstream {u + v} km/h', f'downstream {u + v} km/h, upstream {u} km/h', f'downstream {u * v} km/h, upstream {u - v} km/h']))


def a1s3_find(r):
    u, v = r.randint(5, 20), r.randint(1, 6)
    if v >= u:
        raise ValueError
    t1, t2 = r.randint(1, 5), r.randint(1, 5)
    d1, d2 = (u + v) * t1, (u - v) * t2
    who = name(r)
    ans = f'{u} km/h and {v} km/h'
    return Q(f'{who} rows {d1} km downstream in {t1} hour{"s" if t1 > 1 else ""} and {d2} km upstream in {t2} hour{"s" if t2 > 1 else ""}. Find the speed of the boat in still water and the speed of the stream.', ans,
             f'Downstream speed = {d1}/{t1} = {u + v}, upstream speed = {d2}/{t2} = {u - v} (1 mark); u = ({u + v} + {u - v})/2 = {u}, v = ({u + v} − {u - v})/2 = {v} (2 marks).',
             dist3(ans, [f'{v} km/h and {u} km/h', f'{u + v} km/h and {u - v} km/h', f'{u} km/h and {2 * v} km/h']))


def a1s3_round(r):
    while True:
        u, v = r.randint(5, 15), r.randint(1, 4)
        T = Fr(r.randint(2, 10))
        d = T * (u * u - v * v) / (2 * u)
        if v < u and d.denominator in (1, 2, 4):
            break
    who = name(r)
    return Q(f'{who} can row at {u} km/h in still water. The river flows at {v} km/h. It takes {fz(T)} hours to row to a place and come back. How far is the place?', f'{num(float(d))} km',
             f'Let distance = d. d/{u + v} + d/{u - v} = {fz(T)} (1 mark) ⇒ d = {fz(T)} × {u + v} × {u - v}/{2 * u} = {num(float(d))} km (2 marks).',
             dist3(f'{num(float(d))} km', [f'{num(float(T * u / 2))} km', f'{num(float(T * (u + v) / 2))} km', f'{num(float(d * 2))} km']))


def _pipes(r, k):
    while True:
        rates = [r.randint(2, 20) for _ in range(k)]
        if len(set(rates)) < k:
            continue
        sgn = [1] * k
        if k == 3:
            sgn[2] = -1
        net = sum(Fr(s, t) for s, t in zip(sgn, rates))
        if net <= 0:
            continue
        T = 1 / net
        if (T * 60).denominator == 1 and T < 40:
            return rates, T


def a1s3_pipes(r):
    k = r.choice([2, 2, 3])
    rates, T = _pipes(r, k)
    if k == 2:
        a, b = rates
        return Q(f'Two pipes A and B can fill a tank in {a} hours and {b} hours respectively. How long will they take to fill it together?', hm(T),
                 f'Part filled in 1 hour = 1/{a} + 1/{b} = {fz(1 / T)}; time = {fz(T)} hours = {hm(T)}.',
                 dist3(hm(T), [hm(Fr(a + b, 2)), hm(Fr(a * b, abs(a - b))) if a != b else '1 hour', f'{a + b} hours', hm(T + 1)]))
    a, b, c = rates
    return Q(f'Pipes A and B can fill a tank in {a} hours and {b} hours, and pipe C can empty it in {c} hours. If all three are opened together, in how much time will the empty tank be filled?', hm(T),
             f'Net part filled in 1 hour = 1/{a} + 1/{b} − 1/{c} = {fz(1 / T)} (2 marks); time = {fz(T)} hours = {hm(T)} (1 mark).',
             dist3(hm(T), [hm(1 / (Fr(1, a) + Fr(1, b) + Fr(1, c))), hm(Fr(a + b + c, 3)), hm(T + 2), f'{a + b - c} hours' if a + b > c else hm(T * 2)]))


def a1s3_leak(r):
    while True:
        a = r.randint(2, 12)
        b = a + r.randint(1, 6)
        L = Fr(a * b, b - a)
        if (L * 60).denominator == 1:
            break
    return Q(f'A pipe can fill a tank in {a} hours. Because of a leak at the bottom, it takes {b} hours to fill the tank. In how much time can the leak alone empty the full tank?', hm(L),
             f'Leak rate = 1/{a} − 1/{b} = {fz(1 / L)} of the tank per hour (2 marks); time = {fz(L)} hours = {hm(L)} (1 mark).',
             dist3(hm(L), [hm(Fr(a * b, a + b)), f'{b - a} hours', hm(L + 1), f'{a + b} hours']))


def a1s3_off(r):
    while True:
        a, b = r.randint(10, 40), r.randint(10, 40)
        t = r.randint(2, 8)
        done = t * (Fr(1, a) + Fr(1, b))
        if a == b or done >= 1:
            continue
        rest = (1 - done) * a
        if rest.denominator == 1:
            break
    return Q(f'Pipes A and B can fill a tank in {a} minutes and {b} minutes respectively. Both are opened together, but after {t} minutes pipe B is turned off. How much more time will A take to fill the tank, and what is the total time?',
             f'{fz(rest)} more minutes; total {fz(rest + t)} minutes',
             f'In {t} minutes both fill {t}(1/{a} + 1/{b}) = {fz(done)} of the tank (2 marks); remaining {fz(1 - done)} takes A {fz(1 - done)} × {a} = {fz(rest)} minutes (2 marks); total {fz(rest + t)} minutes (1 mark).',
             dist3(f'{fz(rest)} more minutes; total {fz(rest + t)} minutes', [f'{fz(rest + t)} more minutes; total {fz(rest + 2 * t)} minutes', f'{a - t} more minutes; total {a} minutes', f'{fz((1 - done) * b)} more minutes; total {fz((1 - done) * b + t)} minutes']))


def a1s3_ar(r):
    k = r.randint(0, 2)
    if k == 0:
        u, v = r.randint(6, 20), r.randint(1, 5)
        return ar(f'A boat with speed {u} km/h in still water in a stream of {v} km/h covers {(u - v) * 2} km upstream in 2 hours.', 'Upstream speed = (speed in still water) − (speed of stream).', 'a', f'Upstream speed {u - v} km/h.')
    if k == 1:
        a, b = r.randint(3, 9), r.randint(10, 15)
        return ar(f'Pipes filling a tank in {a} h and {b} h together fill it in {a + b} h.', 'Rates of work (parts per hour) are added when pipes work together.', 'd', f'Together: {fz(Fr(a * b, a + b))} h; A false, R true.')
    return ar('A boat\'s speed in still water is the average of its downstream and upstream speeds.', 'The stream adds to the downstream speed and subtracts the same amount from the upstream speed.', 'a', '(u + v + u − v)/2 = u.')


def a1s3_case(r):
    rates, T = _pipes(r, 2)
    a, b = rates
    c = r.randint(max(a, b) + 2, 60)
    net = Fr(1, a) + Fr(1, b) - Fr(1, c)
    who = name(r)
    return Q((f'The overhead tank of {who}\'s housing society in {r.choice(CITIES)} has two inlet pipes A and B that fill it in {a} hours and {b} hours, and an outlet C that empties it in {c} hours. '
              f'(i) What part of the tank does A fill in 1 hour? (ii) How long do A and B take together (C closed)? (iii) If C is also open, how long does it take to fill the empty tank?'),
             f'(i) 1/{a} (ii) {hm(T)} (iii) {hm(1 / net)}',
             '(i) 1 mark (ii) 1 mark (iii) net rate 1/a + 1/b − 1/c (2 marks).')


# ======================================================================= ch01 st4 races, games and partnership

a1s4_mcq = mcqbank([
    ('"A beats B by 20 m in a 100 m race" means …', 'when A finishes 100 m, B has run 80 m', ['when B finishes, A has run 120 m', 'A runs 20 m less than B', 'A starts 20 m behind B'], 'Meaning of "beats by".'),
    ('"A gives B a start of 10 m in a 100 m race" means …', 'B starts 10 m ahead of A and runs only 90 m', ['A starts 10 m ahead', 'B runs 110 m', 'A runs 90 m'], 'Meaning of "start".'),
    ('A race in which all runners reach the finishing line at the same time is a …', 'dead heat', ['handicap race', 'relay', 'start'], 'Terminology.'),
    ('In a simple partnership the profit is shared in the ratio of …', 'the capitals invested', ['the times of investment', 'the number of partners', 'equal shares'], 'Same period for all partners.'),
    ('In a compound partnership the profit is shared in the ratio of …', 'capital × time for each partner', ['capital only', 'time only', 'capital ÷ time'], 'Different periods of investment.'),
    ('A partner who takes part in running the business is called …', 'a working (active) partner', ['a sleeping partner', 'a creditor', 'a shareholder'], 'Terminology.'),
    ('A partner who only invests money and does not run the business is called …', 'a sleeping partner', ['a working partner', 'a manager', 'a debtor'], 'Terminology.'),
])


def a1s4_chain(r):
    while True:
        L = r.choice([100, 200, 500, 1000])
        x, y = r.randint(1, L // 5), r.randint(1, L // 5)
        z = L - Fr((L - x) * (L - y), L)
        if z.denominator == 1 and x % 5 == 0 and y % 5 == 0:
            break
    ans = f'{fz(z)} m'
    return Q(f'In a {L} m race, A beats B by {x} m and B beats C by {y} m. By how many metres does A beat C in a {L} m race?', ans,
             f'When A runs {L}, B runs {L - x}; when B runs {L}, C runs {L - y}, so when B runs {L - x}, C runs {fz(Fr((L - x) * (L - y), L))} (2 marks); A beats C by {ans} (1 mark).',
             dist3(ans, [f'{x + y} m', f'{abs(x - y)} m', f'{fz(z + 5)} m', f'{fz(z - 5)} m']))


def a1s4_time(r):
    while True:
        L = r.choice([100, 200, 400, 500, 1000])
        vB = r.choice([4, 5, 6, 8, Fr(25, 4), Fr(20, 3), 10])
        t = r.randint(2, 20)
        d = vB * t
        tB = Fr(L) / vB
        tA = tB - t
        if d.denominator == 1 and tA > 0 and tA.denominator in (1, 2) and d < L / 3:
            break
    return Q(f'In a {L} m race, A beats B by {fz(d)} m or {t} seconds. Find B\'s speed and A\'s time for the race.', f'B: {fz(vB)} m/s; A: {num(float(tA))} s',
             f'B runs {fz(d)} m in {t} s, so B\'s speed = {fz(d)}/{t} = {fz(vB)} m/s (1 mark); B\'s time = {L}/{fz(vB)} = {num(float(tB))} s (1 mark); A\'s time = {num(float(tB))} − {t} = {num(float(tA))} s (1 mark).',
             dist3(f'B: {fz(vB)} m/s; A: {num(float(tA))} s', [f'B: {fz(vB)} m/s; A: {num(float(tB))} s', f'B: {fz(Fr(L, t))} m/s; A: {num(float(tA))} s', f'B: {fz(vB)} m/s; A: {num(float(tB + t))} s']))


def a1s4_start(r):
    while True:
        L = r.choice([100, 200, 400, 500, 1000])
        a = r.randint(10, 200)
        b = a + r.randint(1, 30)
        st = L - Fr(L * a, b)
        if st.denominator == 1 and 0 < st < L / 3:
            break
    return Q(f'A can run {L} m in {a} seconds and B in {b} seconds. How many metres\' start can A give B so that the race ends in a dead heat?', f'{fz(st)} m',
             f'In {a} s, B runs {L} × {a}/{b} = {fz(L - st)} m (2 marks); start = {L} − {fz(L - st)} = {fz(st)} m (1 mark).',
             dist3(f'{fz(st)} m', [f'{b - a} m', f'{fz(Fr(L * (b - a), a))} m', f'{fz(st + 5)} m']))


def a1s4_game(r):
    while True:
        P = r.choice([50, 60, 100, 120, 150, 200])
        x, y = r.randint(1, P // 3), r.randint(1, P // 3)
        if y <= x:
            continue
        give = P - Fr((P - y) * P, P - x)
        if give.denominator == 1 and give > 0:
            break
    return Q(f'In a game of {P} points, A can give B {x} points and C {y} points. How many points can B give C in a game of {P} points?', f'{fz(give)} points',
             f'B : C = ({P} − {x}) : ({P} − {y}) = {P - x} : {P - y} (1 mark); when B scores {P}, C scores {P} × {P - y}/{P - x} = {fz(P - give)} (1 mark); B gives C {fz(give)} points (1 mark).',
             dist3(f'{fz(give)} points', [f'{y - x} points', f'{x + y} points', f'{fz(give + 2)} points']))


def a1s4_partner(r):
    n = r.choice([2, 3])
    names = ['A', 'B', 'C'][:n]
    caps = [r.choice(range(20000, 200001, 5000)) for _ in range(n)]
    months = [r.choice([12, 12, 9, 8, 6, 10, 4]) for _ in range(n)]
    w = [c * m for c, m in zip(caps, months)]
    g = math.gcd(*w)
    parts = [x // g for x in w]
    if sum(parts) > 60:
        raise ValueError
    P = sum(parts) * r.randint(100, 2000) * 10
    shares = [P * p // sum(parts) for p in parts]
    inv = ', '.join(f'{nm} invests {inr(c)} for {m} months' for nm, c, m in zip(names, caps, months))
    ans = '; '.join(f'{nm}: {inr(s)}' for nm, s in zip(names, shares))
    wrong = [P * c // sum(caps) if (P * c) % sum(caps) == 0 else round(P * c / sum(caps)) for c in caps]
    return Q(f'In a business, {inv}. The profit at the end of the year is {inr(P)}. Find each partner\'s share.', ans,
             f'Profit is shared in the ratio of capital × time = {" : ".join(str(x) for x in parts)} (2 marks); shares {", ".join(inr(s) for s in shares)} (1 mark).',
             dist3(ans, ['; '.join(f'{nm}: {inr(s)}' for nm, s in zip(names, wrong)), '; '.join(f'{nm}: {inr(s)}' for nm, s in zip(names, reversed(shares))), '; '.join(f'{nm}: {inr(P // n)}' for nm in names)]))


def a1s4_join(r):
    A = r.choice(range(30000, 150001, 10000))
    B = r.choice(range(30000, 150001, 10000))
    m = r.choice([2, 3, 4, 5, 6, 8])
    w1, w2 = A * 12, B * (12 - m)
    g = math.gcd(w1, w2)
    p1, p2 = w1 // g, w2 // g
    if p1 + p2 > 40:
        raise ValueError
    P = (p1 + p2) * r.randint(50, 900) * 100
    a, b = two_names(r)
    sb = P * p2 // (p1 + p2)
    return Q(f'{a} starts a business with {inr(A)}. After {m} months, {b} joins with {inr(B)}. At the end of the year the profit is {inr(P)}. Find {b}\'s share.', inr(sb),
             f'Ratio = {A} × 12 : {B} × {12 - m} = {p1} : {p2} (2 marks); {b}\'s share = {p2}/{p1 + p2} × {P} = {inr(sb)} (1 mark).',
             dist3(inr(sb), [inr(P * B // (A + B)) if (P * B) % (A + B) == 0 else inr(round(P * B / (A + B))), inr(P - sb), inr(P // 2), inr(round(P * B * m / (A * 12 + B * m)))]))


def a1s4_working(r):
    a, b = two_names(r)
    A = r.choice(range(50000, 300001, 10000))
    B = r.choice(range(50000, 300001, 10000))
    g = math.gcd(A, B)
    p1, p2 = A // g, B // g
    if p1 + p2 > 30:
        raise ValueError
    s = r.choice([5, 10, 12, 15, 20])
    P = (p1 + p2) * r.randint(20, 400) * 100
    sal = P * s // 100
    rest = P - sal
    if rest % (p1 + p2):
        raise ValueError
    sa = sal + rest * p1 // (p1 + p2)
    sb = rest * p2 // (p1 + p2)
    return Q(f'{a} and {b} invest {inr(A)} and {inr(B)} in a business. {a} is the working partner and gets {s}% of the profit as salary; the rest is shared in the ratio of capitals. If the profit is {inr(P)}, find what each receives.',
             f'{a}: {inr(sa)}; {b}: {inr(sb)}',
             f'Salary = {s}% of {inr(P)} = {inr(sal)} (1 mark); remaining {inr(rest)} in the ratio {p1} : {p2} (2 marks): {inr(rest * p1 // (p1 + p2))} and {inr(sb)} (1 mark); {a} gets {inr(sa)} in all (1 mark).',
             dist3(f'{a}: {inr(sa)}; {b}: {inr(sb)}', [f'{a}: {inr(P * p1 // (p1 + p2))}; {b}: {inr(P * p2 // (p1 + p2))}', f'{a}: {inr(rest * p1 // (p1 + p2))}; {b}: {inr(sb + sal)}', f'{a}: {inr(sa + sal)}; {b}: {inr(sb - sal)}']))


def a1s4_ar(r):
    k = r.randint(0, 2)
    if k == 0:
        return ar('In a 100 m race, if A beats B by 10 m and B beats C by 10 m, then A beats C by 20 m.', 'Distances in a race are reduced in the same ratio, not by subtraction.', 'd', 'A beats C by 100 − 90 × 0.9 = 19 m; A false, R true.')
    if k == 1:
        c1, c2 = r.choice(range(10000, 90001, 10000)), r.choice(range(10000, 90001, 10000))
        return ar(f'If A invests {inr(c1)} for 12 months and B invests {inr(c2)} for 12 months, the profit is shared in the ratio {ratio(c1, c2)}.', 'When the periods are equal, profit is shared in the ratio of capitals.', 'a', 'Simple partnership.')
    return ar('A sleeping partner receives no share of the profit.', 'A sleeping partner does not take part in running the business.', 'd', 'A sleeping partner shares profit in the ratio of capital; A false, R true.')


def a1s4_case(r):
    a, b = two_names(r)
    A, B = r.choice(range(40000, 200001, 20000)), r.choice(range(40000, 200001, 20000))
    m = r.choice([3, 4, 6])
    w1, w2 = A * 12, B * (12 - m)
    g = math.gcd(w1, w2)
    p1, p2 = w1 // g, w2 // g
    if p1 + p2 > 30:
        raise ValueError
    P = (p1 + p2) * r.randint(100, 900) * 100
    return Q((f'{a} opens a bakery in {r.choice(CITIES)} with {inr(A)}. {m} months later {b} joins with {inr(B)}. The year\'s profit is {inr(P)}. '
              f'(i) Is this a simple or a compound partnership? (ii) Find the ratio in which profit is shared. (iii) Find each partner\'s share.'),
             f'(i) Compound (ii) {p1} : {p2} (iii) {a}: {inr(P * p1 // (p1 + p2))}, {b}: {inr(P * p2 // (p1 + p2))}',
             '(i) different periods (1 mark) (ii) capital × time (1 mark) (iii) shares (2 marks).')


# ======================================================================= ch02 st1 rules and solving linear inequalities

a2s1_mcq = mcqbank([
    ('If a < b and c < 0, then …', 'ac > bc', ['ac < bc', 'ac = bc', 'a/c < b/c'], 'Multiplying by a negative number reverses the inequality.'),
    ('If a < b, then for every real c, …', 'a + c < b + c', ['a + c > b + c', 'ac < bc', 'a − c > b − c'], 'Adding the same number keeps the sign.'),
    ('If a > b > 0, then …', '1/a < 1/b', ['1/a > 1/b', '1/a = 1/b', '−a > −b'], 'Taking reciprocals of positive numbers reverses the sign.'),
    ('The solution of −3x > 12 is …', 'x < −4', ['x > −4', 'x < 4', 'x > 4'], 'Divide by −3 and reverse.'),
    ('The solution set of 2x + 3 > 2x + 1 is …', 'R (every real number)', ['∅ (no solution)', 'x > 0', 'x > 1'], '3 > 1 is always true.'),
    ('The solution set of x + 5 < x + 2 is …', '∅ (no solution)', ['R', 'x < −3', 'x > 3'], '5 < 2 is never true.'),
    ('If x ∈ N and 2x − 1 < 7, the solution set is …', '{1, 2, 3}', ['{1, 2, 3, 4}', '{0, 1, 2, 3}', '{x : x < 4}'], 'x < 4 with x natural.'),
    ('An inequality in which both sides are linear expressions in x is called …', 'a linear inequality in one variable', ['a quadratic inequality', 'a linear equation', 'an identity'], 'Definition.'),
])


def a2s1_lin(r):
    while True:
        a, c = r.randint(-6, 8), r.randint(-6, 8)
        b, d = r.randint(-12, 12), r.randint(-12, 12)
        if a != c and a and c:
            break
    sg = r.choice(['<', '≤', '>', '≥'])
    k = a - c
    bd = Fr(d - b, k)
    rev = {'<': '>', '≤': '≥', '>': '<', '≥': '≤'}
    s2 = sg if k > 0 else rev[sg]
    ans = f'x {s2} {fz(bd)}'
    lhs = term(a, 'x', first=True) + (term(b, '') if b else '')
    rhs = term(c, 'x', first=True) + (term(d, '') if d else '')
    return Q(f'Solve the inequality {lhs} {sg} {rhs} for real x.', ans,
             f'{term(k, "x", first=True)} {sg} {fz(d - b)}' + (f'; divide by {fz(k)} < 0 and reverse the sign: {ans}.' if k < 0 else f'; divide by {fz(k)}: {ans}.'),
             dist3(ans, [f'x {rev[s2]} {fz(bd)}', f'x {s2} {fz(-bd)}', f'x {s2} {fz(Fr(d + b, k))}']))


def a2s1_frac(r):
    p, q = r.randint(1, 9), r.choice([2, 3, 4, 5])
    s, t = r.randint(1, 9), r.choice([2, 3, 4, 5, 6])
    if q == t:
        raise ValueError
    k = r.randint(-3, 4)
    # (x − p)/q − (x + s)/t ≥ k  ⇒ x(1/q − 1/t) ≥ k + p/q + s/t
    co = Fr(1, q) - Fr(1, t)
    rhs = k + Fr(p, q) + Fr(s, t)
    bd = rhs / co
    sg = r.choice(['≥', '>', '≤', '<'])
    rev = {'<': '>', '≤': '≥', '>': '<', '≥': '≤'}
    s2 = sg if co > 0 else rev[sg]
    ans = f'x {s2} {fz(bd)}'
    return Q(f'Solve (x − {p})/{q} − (x + {s})/{t} {sg} {k} for real x.', ans,
             f'Multiply by {q * t // math.gcd(q, t)} (1 mark); collect terms: ({fz(co)})x {sg} {fz(rhs)} (1 mark); ' + ('divide by a negative number and reverse: ' if co < 0 else 'so ') + f'{ans} (1 mark).',
             dist3(ans, [f'x {rev[s2]} {fz(bd)}', f'x {s2} {fz(-bd)}', f'x {s2} {fz(bd + 1)}']))


def a2s1_double(r):
    while True:
        b = r.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        c = r.randint(-9, 9)
        d = r.choice([1, 2, 3, 4])
        lo, hi = r.randint(-8, 2), r.randint(3, 10)
        x1, x2 = Fr(lo * d - c, b), Fr(hi * d - c, b)
        if x1.denominator <= 3 and x2.denominator <= 3:
            break
    s1, s2 = r.choice([('≤', '<'), ('<', '≤'), ('≤', '≤'), ('<', '<')])
    expr = f'({term(b, "x", first=True)}{term(c, "") if c else ""})/{d}' if d > 1 else f'{term(b, "x", first=True)}{term(c, "") if c else ""}'
    if b > 0:
        ans = f'{fz(x1)} {s1} x {s2} {fz(x2)}'
        iv = interval(x1, x2, s1 == '≤', s2 == '≤')
    else:
        ans = f'{fz(x2)} {s2} x {s1} {fz(x1)}'
        iv = interval(x2, x1, s2 == '≤', s1 == '≤')
    return Q(f'Solve {lo} {s1} {expr} {s2} {hi} and write the solution as an interval.', f'{ans}, i.e. x ∈ {iv}',
             ', '.join(([f'multiply through by {d}'] if d > 1 else []) + ([f'subtract {fpar(c)}'] if c else []) + [f'divide by {fpar(b)}' + (' and reverse both signs' if b < 0 else '')]).capitalize() + f' (2 marks): {ans} (1 mark).',
             dist3(f'{ans}, i.e. x ∈ {iv}', [f'{fz(x1)} {s1} x {s2} {fz(x2)}, i.e. x ∈ {interval(x1, x2, s1 == "≤", s2 == "≤")}' if b < 0 else f'{fz(x2)} {s2} x {s1} {fz(x1)}, i.e. x ∈ {interval(x2, x1, s2 == "≤", s1 == "≤")}',
                                             f'{fz(lo * d + c)} {s1} x {s2} {fz(hi * d + c)}, i.e. x ∈ {interval(lo * d + c, hi * d + c, s1 == "≤", s2 == "≤")}', f'{ans}, i.e. x ∈ {interval(min(x1, x2), max(x1, x2), True, True)}']))


def a2s1_nat(r):
    a = r.randint(2, 7)
    b = r.randint(-5, 10)
    c = r.randint(10, 45)
    sg = r.choice(['<', '≤'])
    bound = Fr(c - b, a)
    xs = [x for x in range(1, 60) if (a * x + b < c if sg == '<' else a * x + b <= c)]
    if not xs or len(xs) > 12:
        raise ValueError
    ans = '{' + ', '.join(map(str, xs)) + '}'
    return Q(f'Solve {a}x{term(b, "") if b else ""} {sg} {c} when x is a natural number.', ans,
             f'x {sg} {fz(bound)} (1 mark); natural numbers satisfying this: {ans} (1 mark).',
             dist3(ans, ['{' + ', '.join(map(str, [0] + xs)) + '}', '{' + ', '.join(map(str, xs + [xs[-1] + 1])) + '}', '{' + ', '.join(map(str, xs[:-1])) + '}' if len(xs) > 1 else '∅']))


def a2s1_ar(r):
    k = r.randint(0, 3)
    a = r.randint(2, 9)
    b = r.randint(2, 20)
    if k == 0:
        return ar(f'If −{a}x < {a * b}, then x > −{b}.', 'Dividing both sides of an inequality by a negative number reverses the inequality sign.', 'a', f'Divide by −{a} and reverse.')
    if k == 1:
        return ar(f'If −{a}x < {a * b}, then x < −{b}.', 'Dividing both sides of an inequality by a negative number reverses the inequality sign.', 'd', f'Correct: x > −{b}; A false, R true.')
    if k == 2:
        return ar(f'x + {a} > x + {a - 1} for every real x.', 'Subtracting the same number from both sides does not change an inequality.', 'a', f'It reduces to {a} > {a - 1}, always true.')
    return ar(f'If x < {b}, then x² < {b * b}.', 'Squaring both sides of an inequality between positive numbers keeps its direction.', 'd', f'x = −{b + 1} < {b} but x² > {b * b}; A false, R true.')


def a2s1_case(r):
    who = name(r)
    m1, m2 = r.randint(55, 90), r.randint(55, 90)
    A = r.choice([70, 75, 80, 85])
    need = 3 * A - m1 - m2
    if not 30 <= need <= 100:
        raise ValueError
    c = r.randint(2, 6)
    k = r.randint(5, 25)
    return Q((f'{who} wants an average of at least {A} marks in three unit tests. The first two scores are {m1} and {m2}. '
              f'(i) Write the inequality for the third score x. (ii) Find the least score needed. (iii) Solve −{c}x + {k} ≤ {k - c * 4} and state the rule used.'),
             f'(i) ({m1} + {m2} + x)/3 ≥ {A} (ii) {need} (iii) x ≥ 4; dividing by a negative number reverses the sign',
             '(i) 1 mark (ii) 1 mark (iii) solving with the reversal rule (2 marks).')


# ======================================================================= ch02 st2 number line and intervals

a2s2_mcq = mcqbank([
    ('On a number line, the solution of x ≥ 3 is shown by …', 'a filled (closed) circle at 3 and the line to the right shaded', ['an open circle at 3 and the line to the right shaded', 'a filled circle at 3 and the line to the left shaded', 'only the point 3'], 'The end point is included.'),
    ('On a number line, the solution of x < −1 is shown by …', 'an open circle at −1 and the line to the left shaded', ['a filled circle at −1 and the line to the left shaded', 'an open circle at −1 and the line to the right shaded', 'only the point −1'], 'The end point is excluded.'),
    ('In interval notation, {x : −2 < x ≤ 5} is …', '(−2, 5]', ['[−2, 5)', '(−2, 5)', '[−2, 5]'], 'Round bracket: excluded; square bracket: included.'),
    ('The interval [−1, ∞) represents …', 'x ≥ −1', ['x > −1', 'x ≤ −1', 'x < −1'], 'Square bracket includes −1.'),
    ('An open circle at a point on the number line shows that the point is …', 'not included in the solution', ['included in the solution', 'the only solution', 'a boundary of a closed interval'], 'Convention.'),
    ('The solution set of x > 2 and x < 2 together is …', '∅ (empty set)', ['{2}', 'R', '(2, ∞)'], 'No number satisfies both.'),
])


def a2s2_interval(r):
    lo, hi = sorted(r.sample(range(-9, 10), 2))
    a, b = r.choice([(True, True), (True, False), (False, True), (False, False)])
    s1, s2 = ('≤' if a else '<'), ('≤' if b else '<')
    ans = interval(lo, hi, a, b)
    return Q(f'Write {{x ∈ R : {lo} {s1} x {s2} {hi}}} in interval notation and describe its graph on the number line.', ans,
             f'{"Filled" if a else "Open"} circle at {lo}, {"filled" if b else "open"} circle at {hi}, segment between shaded (1 mark each).',
             dist3(ans, [interval(lo, hi, not a, not b), interval(lo, hi, True, True) if not (a and b) else interval(lo, hi, False, False), interval(lo, hi, b, a)]))


def a2s2_graph(r):
    k = r.randint(0, 2)
    p = r.randint(-8, 8)
    q = p + r.randint(2, 9)
    if k == 0:
        closed = r.random() < 0.5
        right = r.random() < 0.5
        sg = ('≥' if closed else '>') if right else ('≤' if closed else '<')
        ans = f'x {sg} {p}'
        desc = f'{"a filled" if closed else "an open"} circle at {p} and the part of the line to the {"right" if right else "left"} of {p} shaded'
        wrong = [f'x {s} {p}' for s in ('≥', '>', '≤', '<') if s != sg]
        return Q(f'The solution of an inequality is shown on a number line by {desc}. Write the inequality.', ans, 'Filled circle: end point included; open circle: excluded; the arrow shows the direction.', wrong)
    c1, c2 = r.random() < 0.5, r.random() < 0.5
    ans = f'{p} {"≤" if c1 else "<"} x {"≤" if c2 else "<"} {q}'
    desc = f'{"a filled" if c1 else "an open"} circle at {p}, {"a filled" if c2 else "an open"} circle at {q} and the segment between them shaded'
    return Q(f'The solution of an inequality is shown on a number line by {desc}. Write the inequality and the interval.', f'{ans}, i.e. {interval(p, q, c1, c2)}',
             'Read the end points and whether each is included.', dist3(f'{ans}, i.e. {interval(p, q, c1, c2)}', [f'{p} {"<" if c1 else "≤"} x {"<" if c2 else "≤"} {q}, i.e. {interval(p, q, not c1, not c2)}',
                                                                                                                 f'x ≤ {p} or x ≥ {q}, i.e. (−∞, {p}] ∪ [{q}, ∞)', f'{p} ≤ x ≤ {q}, i.e. [{p}, {q}]' if not (c1 and c2) else f'{p} < x < {q}, i.e. ({p}, {q})']))


def a2s2_system(r):
    a1, b1 = r.randint(1, 5), r.randint(-10, 10)
    a2, b2 = r.randint(1, 5), r.randint(-10, 10)
    x1 = r.randint(-6, 6)
    x2 = x1 + r.choice([-3, -2, 2, 3, 4, 5, 6])
    c1 = a1 * x1 + b1
    c2 = a2 * x2 + b2
    e1 = f'{term(a1, "x", first=True)}{term(b1, "") if b1 else ""} ≥ {c1}'
    e2 = f'{term(a2, "x", first=True)}{term(b2, "") if b2 else ""} < {c2}'
    if x1 < x2:
        ans = f'{x1} ≤ x < {x2}, i.e. [{x1}, {x2})'
    else:
        ans = 'no solution (∅)'
    return Q(f'Solve the system {e1} and {e2}, and represent the solution on the number line.', ans,
             f'First gives x ≥ {x1}, second gives x < {x2} (2 marks); common part: {ans} (1 mark).',
             dist3(ans, [f'x ≥ {x1}', f'x < {x2}', f'{min(x1, x2)} < x ≤ {max(x1, x2)}, i.e. ({min(x1, x2)}, {max(x1, x2)}]', 'no solution (∅)' if x1 < x2 else f'{x2} < x ≤ {x1}, i.e. ({x2}, {x1}]']))


def a2s2_explain(r):
    return xbank([
        ('Explain the difference between the graphs of x > 2 and x ≥ 2 on a number line.', 'x > 2 uses an open circle at 2; x ≥ 2 uses a filled circle at 2; both shade to the right.', 'Open versus filled circle (2 marks).'),
        ('Why is the solution of 3x − 5 < 3x + 1 the whole real line?', 'It reduces to −5 < 1, which is true for every x.', 'Variable terms cancel and a true statement remains (2 marks).'),
        ('Why can ∞ never be written with a square bracket in an interval?', '∞ is not a real number, so it cannot be included.', 'Intervals include only real end points (2 marks).'),
        ('Explain how to represent x ≤ −3 or x > 4 on a number line.', 'Filled circle at −3 shading left, open circle at 4 shading right.', 'Union of two rays (2 marks).'),
    ])(r)


def a2s2_ar(r):
    p = r.randint(-6, 6)
    k = r.randint(0, 2)
    if k == 0:
        return ar(f'The solution of x ≥ {p} is drawn with a filled circle at {p}.', 'A filled circle shows that the end point belongs to the solution set.', 'a', 'The end point is included.')
    if k == 1:
        return ar(f'(−∞, {p}] is the same as x < {p}.', 'A square bracket shows that the end point is included.', 'd', f'(−∞, {p}] means x ≤ {p}; A false, R true.')
    return ar(f'The system x > {p} and x < {p} has no solution.', 'No real number can be both greater and less than the same number.', 'a', 'The intersection is empty.')


def a2s2_case(r):
    who = name(r)
    lo, hi = r.randint(15, 25), r.randint(30, 40)
    return Q((f'A cold-storage unit managed by {who} in {r.choice(CITIES)} must keep fruit between {lo} °F and {hi} °F inclusive. '
              f'(i) Write this as an inequality in F. (ii) Write the interval. (iii) Using F = 9C/5 + 32, find the range of C and draw it on a number line.'),
             f'(i) {lo} ≤ F ≤ {hi} (ii) [{lo}, {hi}] (iii) {fz(Fr(5 * (lo - 32), 9))} ≤ C ≤ {fz(Fr(5 * (hi - 32), 9))}',
             '(i) 1 mark (ii) 1 mark (iii) substitute and solve, graph with filled circles (2 marks).')


# ======================================================================= ch02 st3 word problems

a2s3_mcq = mcqbank([
    ('"The cost must not exceed ₹500" is written as …', 'cost ≤ 500', ['cost < 500', 'cost ≥ 500', 'cost > 500'], '"Not exceed" means at most.'),
    ('"At least 40 students" is written as …', 'n ≥ 40', ['n > 40', 'n ≤ 40', 'n < 40'], '"At least" includes 40.'),
    ('"More than 18 years old" is written as …', 'age > 18', ['age ≥ 18', 'age < 18', 'age ≤ 18'], 'Strict inequality.'),
    ('The sum of two consecutive odd natural numbers is less than 40. If the smaller is x, the inequality is …', 'x + (x + 2) < 40', ['x + (x + 1) < 40', '2x < 40', 'x + (x + 2) ≤ 40'], 'Consecutive odd numbers differ by 2.'),
    ('"A minimum of ₹2000 must be saved" is written as …', 'savings ≥ 2000', ['savings > 2000', 'savings ≤ 2000', 'savings = 2000'], '"Minimum" means at least.'),
])


def a2s3_marks(r):
    who = name(r)
    n = r.choice([3, 4])
    ms = [r.randint(50, 95) for _ in range(n - 1)]
    A = r.choice([60, 65, 70, 75, 80, 85])
    need = n * A - sum(ms)
    if not 20 <= need <= 100:
        raise ValueError
    return Q(f'{who} scored {", ".join(map(str, ms[:-1]))} and {ms[-1]} in the first {n - 1} tests. Find the minimum marks needed in test {n} to get an average of at least {A}.', str(need),
             f'({" + ".join(map(str, ms))} + x)/{n} ≥ {A} ⇒ x ≥ {n * A} − {sum(ms)} = {need}.', dist3(str(need), [need - 1, need + 1, A, n * A - sum(ms) // n]))


def a2s3_budget(r):
    who = name(r)
    B = r.choice(range(500, 3001, 100))
    p = r.randint(15, 80)
    q, k = r.randint(40, 200), r.randint(1, 5)
    rest = B - q * k
    if rest <= 0:
        raise ValueError
    x = rest // p
    item1, item2 = r.choice([('pens', 'notebooks'), ('pencils', 'files'), ('mangoes', 'boxes of dates'), ('plants', 'pots')])
    return Q(f'{who} has ₹{B} and buys {k} {item2} at ₹{q} each. With the rest, {item1} costing ₹{p} each are bought. Form an inequality and find the greatest number of {item1} that can be bought.', f'{q * k} + {p}x ≤ {B}; at most {x}',
             f'{q}({k}) + {p}x ≤ {B} ⇒ x ≤ {fz(Fr(rest, p))} (2 marks); x is a whole number, so at most {x} (1 mark).',
             dist3(f'{q * k} + {p}x ≤ {B}; at most {x}', [f'{q * k} + {p}x ≤ {B}; at most {x + 1}', f'{q * k} + {p}x ≥ {B}; at least {x + 1}', f'{p}x ≤ {B}; at most {B // p}']))


def a2s3_temp(r):
    lo, hi = sorted(r.sample(range(5, 45, 5), 2))
    F1, F2 = Fr(9 * lo, 5) + 32, Fr(9 * hi, 5) + 32
    return Q(f'A solution must be kept between {lo} °C and {hi} °C. What is the range of temperature in degrees Fahrenheit if F = (9/5)C + 32?', f'{fz(F1)} °F < F < {fz(F2)} °F',
             f'{lo} < C < {hi} ⇒ {lo} < (5/9)(F − 32) < {hi} (1 mark) ⇒ {fz(F1)} < F < {fz(F2)} (2 marks).',
             dist3(f'{fz(F1)} °F < F < {fz(F2)} °F', [f'{fz(Fr(5 * (lo - 32), 9))} °F < F < {fz(Fr(5 * (hi - 32), 9))} °F', f'{9 * lo // 5} °F < F < {9 * hi // 5} °F', f'{lo + 32} °F < F < {hi + 32} °F']))


def a2s3_consec(r):
    kind = r.choice(['odd', 'even'])
    lo = r.randint(3, 20)
    S = r.randint(lo * 2 + 10, lo * 2 + 50)
    start = lo + 1 if (lo + 1) % 2 == (1 if kind == 'odd' else 0) else lo + 2
    pairs = [(x, x + 2) for x in range(start, S, 2) if x + x + 2 < S]
    if not 1 <= len(pairs) <= 8:
        raise ValueError
    ans = ', '.join(f'({a}, {b})' for a, b in pairs)
    return Q(f'Find all pairs of consecutive {kind} natural numbers, both greater than {lo}, such that their sum is less than {S}.', ans,
             f'x > {lo} and x + (x + 2) < {S} ⇒ {lo} < x < {fz(Fr(S - 2, 2))} with x {kind} (2 marks); pairs {ans} (1 mark).',
             dist3(ans, [', '.join(f'({a}, {b})' for a, b in pairs[:-1]) or '(none)', ', '.join(f'({a}, {a + 1})' for a, b in pairs), ', '.join(f'({a}, {b})' for a, b in pairs + [(pairs[-1][1], pairs[-1][1] + 2)])]))


def a2s3_acid(r):
    while True:
        V = r.choice([300, 400, 500, 600, 800, 1000])
        p0 = r.choice([8, 10, 12, 15])
        p1 = r.choice([25, 30, 40, 50])
        lo, hi = sorted(r.sample(range(p0 + 2, p1 - 2), 2))
        x1 = Fr(V * (lo - p0), p1 - lo)
        x2 = Fr(V * (hi - p0), p1 - hi)
        if x1.denominator == 1 and x2.denominator == 1:
            break
    return Q(f'How many litres of a {p1}% acid solution must be added to {V} litres of a {p0}% acid solution so that the acid content of the mixture is more than {lo}% but less than {hi}%?',
             f'more than {fz(x1)} L but less than {fz(x2)} L',
             f'Acid = {p0}% of {V} + {p1}% of x (1 mark); {lo}% of ({V} + x) < that < {hi}% of ({V} + x) (2 marks); solving: {fz(x1)} < x < {fz(x2)} (2 marks).',
             dist3(f'more than {fz(x1)} L but less than {fz(x2)} L', [f'more than {fz(x2)} L but less than {fz(x1) if x1 > x2 else fz(x2 * 2)} L', f'more than {V * lo // 100} L but less than {V * hi // 100} L', f'more than {fz(x1 / 2)} L but less than {fz(x2 / 2)} L']))


def a2s3_ar(r):
    k = r.randint(0, 3)
    n = r.choice(range(200, 5001, 100))
    m = r.randint(10, 90)
    if k == 0:
        return ar(f'"The bill cannot exceed ₹{n}" is written as B ≤ {n}.', '"Cannot exceed" allows equality.', 'a', 'At most.')
    if k == 1:
        return ar(f'"At least {m} seats" is written as s > {m}.', '"At least" includes the boundary value.', 'd', f'It is s ≥ {m}; A false, R true.')
    if k == 2:
        p = r.randint(15, 90)
        return ar(f'With ₹{n} and pens at ₹{p} each, at most {n // p} pens can be bought.', 'The number of pens x satisfies {p}x ≤ {n} with x a whole number.'.replace('{p}', str(p)).replace('{n}', str(n)), 'a', f'x ≤ {fz(Fr(n, p))}, so the greatest whole number is {n // p}.')
    return ar(f'"Fewer than {m} absentees" is written as a ≤ {m}.', '"Fewer than" excludes the boundary value.', 'd', f'It is a < {m}; A false, R true.')


def a2s3_case(r):
    who = name(r)
    F0 = r.choice(range(2000, 8001, 500))
    v = r.choice([40, 50, 60, 75, 80])
    pr = v + r.choice([20, 25, 30, 40, 50])
    n = F0 / (pr - v)
    nmin = math.floor(n) + 1
    return Q((f'{who} makes handmade candles in {r.choice(CITIES)}. Fixed monthly costs are ₹{F0}, each candle costs ₹{v} to make and sells for ₹{pr}. '
              f'(i) Write the cost C(x) and revenue R(x) for x candles. (ii) Write the inequality for a profit. (iii) Find the least number of candles for a profit.'),
             f'(i) C(x) = {F0} + {v}x, R(x) = {pr}x (ii) {pr}x > {F0} + {v}x (iii) {nmin}',
             '(i) 1 mark (ii) R(x) > C(x) (1 mark) (iii) x > ' + fz(Fr(F0, pr - v)) + f', least whole number {nmin} (2 marks).')


# ======================================================================= ch03 Cramer's rule (st4); st1–st3 re-use 041 families

a3s4_mcq = mcqbank([
    ('By Cramer\'s rule, for a₁x + b₁y = c₁, a₂x + b₂y = c₂ with D ≠ 0, x = …', 'D₁/D', ['D/D₁', 'D₁D₂/D', 'D₂/D'], 'D₁ replaces the x-column by the constants.'),
    ('Cramer\'s rule can be used only when …', 'the coefficient determinant D ≠ 0', ['D = 0', 'all constants are zero', 'the system has two equations only'], 'Unique solution condition.'),
    ('If D = 0 and at least one of D₁, D₂, D₃ is non-zero, the system is …', 'inconsistent (no solution)', ['consistent with a unique solution', 'consistent with infinitely many solutions', 'homogeneous'], 'Cramer\'s rule test.'),
    ('In Cramer\'s rule, D₂ is obtained by …', 'replacing the second column of D by the constants', ['replacing the second row of D by the constants', 'deleting the second column', 'transposing D'], 'Definition.'),
    ('A homogeneous system AX = O with |A| ≠ 0 has …', 'only the trivial solution', ['infinitely many solutions', 'no solution', 'exactly two solutions'], 'x = D₁/D = 0, etc.'),
])


def _sys2(r):
    while True:
        A = [[r.randint(-6, 7) for _ in range(2)] for _ in range(2)]
        D = det(A)
        if D != 0 and all(A[i][j] for i in range(2) for j in range(2)):
            break
    x, y = r.randint(-6, 8), r.randint(-6, 8)
    c = [A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y]
    return A, c, x, y


def a3s4_two(r):
    A, c, x, y = _sys2(r)
    D = det(A)
    D1 = det([[c[0], A[0][1]], [c[1], A[1][1]]])
    D2 = det([[A[0][0], c[0]], [A[1][0], c[1]]])
    ans = f'x = {x}, y = {y}'
    return Q(f'Solve by Cramer\'s rule: {lin_eq(A[0], c[0], "xy")}, {lin_eq(A[1], c[1], "xy")}.', ans,
             f'D = {fz(D)}, D₁ = {fz(D1)}, D₂ = {fz(D2)} (2 marks); x = D₁/D = {x}, y = D₂/D = {y} (1 mark).',
             dist3(ans, [f'x = {y}, y = {x}', f'x = {-x}, y = {y}', f'x = {fz(Fr(D, D1)) if D1 else 0}, y = {fz(Fr(D, D2)) if D2 else 0}', f'x = {x}, y = {-y}']))


def a3s4_three(r):
    A = unimod(r, 3, dets=(1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6))
    X = [r.randint(-4, 5) for _ in range(3)]
    c = [sum(A[i][j] * X[j] for j in range(3)) for i in range(3)]
    D = det(A)
    Ds = []
    for j in range(3):
        M = [row[:] for row in A]
        for i in range(3):
            M[i][j] = c[i]
        Ds.append(det(M))
    ans = f'x = {X[0]}, y = {X[1]}, z = {X[2]}'
    return Q('Solve by Cramer\'s rule: ' + ', '.join(lin_eq(A[i], c[i]) for i in range(3)) + '.', ans,
             f'D = {fz(D)} (1 mark); D₁ = {fz(Ds[0])}, D₂ = {fz(Ds[1])}, D₃ = {fz(Ds[2])} (3 marks); x = D₁/D, y = D₂/D, z = D₃/D (1 mark).',
             dist3(ans, [f'x = {X[1]}, y = {X[0]}, z = {X[2]}', f'x = {-X[0]}, y = {-X[1]}, z = {-X[2]}', f'x = {X[0]}, y = {X[2]}, z = {X[1]}', f'x = {X[0] + 1}, y = {X[1]}, z = {X[2] - 1}']))


def a3s4_consist(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    k = r.randint(2, 4)
    c = r.randint(1, 12)
    kind = r.randint(0, 1)
    if kind == 0:
        c2 = k * c + r.randint(1, 5)
        ans = 'Inconsistent (no solution)'
        D1 = c * k * b - b * c2
        key = f'D = {a}({k * b}) − {b}({k * a}) = 0 and D₁ = {fz(D1)} ≠ 0, so no solution.'
    else:
        c2 = k * c
        ans = 'Consistent with infinitely many solutions'
        key = 'D = D₁ = D₂ = 0: the second equation is a multiple of the first.'
    return Q(f'Using determinants, examine the consistency of {lin_eq([a, b], c, "xy")}, {lin_eq([k * a, k * b], c2, "xy")}.', ans, key,
             dist3(ans, ['Consistent with a unique solution', 'Inconsistent (no solution)', 'Consistent with infinitely many solutions', 'Only the trivial solution']))


def a3s4_word(r):
    items = r.choice([('pens', 'pencils', 'erasers'), ('apples', 'bananas', 'oranges'), ('notebooks', 'files', 'markers')])
    while True:
        A = [[r.randint(1, 5) for _ in range(3)] for _ in range(3)]
        if det(A) != 0:
            break
    X = [r.choice(range(5, 61, 5)) for _ in range(3)]
    c = [sum(A[i][j] * X[j] for j in range(3)) for i in range(3)]
    names = r.sample(['Aarav', 'Kavya', 'Imran', 'Riya', 'Harpreet', 'Tara', 'Dev'], 3)
    lines = '; '.join(f'{nm} buys {A[i][0]} {items[0]}, {A[i][1]} {items[1]} and {A[i][2]} {items[2]} for ₹{c[i]}' for i, nm in enumerate(names))
    ans = f'{items[0]} ₹{X[0]}, {items[1]} ₹{X[1]}, {items[2]} ₹{X[2]} each'
    return Q(f'At a stationery fair: {lines}. Using Cramer\'s rule, find the price of each item.', ans,
             f'Form the equations (1 mark); D = {fz(det(A))} (1 mark); D₁, D₂, D₃ (2 marks); prices (1 mark).',
             dist3(ans, [f'{items[0]} ₹{X[1]}, {items[1]} ₹{X[0]}, {items[2]} ₹{X[2]} each', f'{items[0]} ₹{X[0]}, {items[1]} ₹{X[2]}, {items[2]} ₹{X[1]} each', f'{items[0]} ₹{X[2]}, {items[1]} ₹{X[1]}, {items[2]} ₹{X[0]} each']))


def a3s4_ar(r):
    k = r.randint(0, 2)
    if k == 0:
        A, c, x, y = _sys2(r)
        return ar(f'The system {lin_eq(A[0], c[0], "xy")}, {lin_eq(A[1], c[1], "xy")} has a unique solution.', f'Its coefficient determinant is {fz(det(A))} ≠ 0.', 'a', 'D ≠ 0 ⇒ unique solution by Cramer\'s rule.')
    if k == 1:
        a, b = r.randint(1, 5), r.randint(1, 5)
        return ar(f'Cramer\'s rule gives the solution of {lin_eq([a, b], 3, "xy")}, {lin_eq([2 * a, 2 * b], 7, "xy")}.', 'Cramer\'s rule applies only when D ≠ 0.', 'd', 'Here D = 0 (the system is inconsistent); A false, R true.')
    return ar('If D = 0 and D₁ = D₂ = D₃ = 0, the system may have infinitely many solutions.', 'In that case Cramer\'s rule cannot be applied and the equations must be examined further.', 'b', 'Both true; R is about method, not the reason for A.')


def a3s4_case(r):
    A, c, x, y = _sys2(r)
    a, b = abs(A[0][0]) + 1, abs(A[0][1]) + 1
    p, q = r.randint(20, 90), r.randint(20, 90)
    a2, b2 = r.randint(1, 6), r.randint(1, 6)
    if a * b2 - a2 * b == 0:
        raise ValueError
    who = name(r)
    return Q((f'{who}\'s school canteen sells samosas at ₹x and juice at ₹y. One group buys {a} samosas and {b} juices for ₹{a * p + b * q}; another buys {a2} samosas and {b2} juices for ₹{a2 * p + b2 * q}. '
              f'(i) Write the system of equations. (ii) Find D. (iii) Find x and y by Cramer\'s rule.'),
             f'(i) {a}x + {b}y = {a * p + b * q}, {a2}x + {b2}y = {a2 * p + b2 * q} (ii) D = {a * b2 - a2 * b} (iii) x = {p}, y = {q}'.replace(' 1x', ' x').replace(' 1y', ' y'),
             '(i) 1 mark (ii) 1 mark (iii) D₁, D₂ and the quotients (2 marks).')


def a3s4_explain(r):
    return xbank([
        ('State Cramer\'s rule for a system of two linear equations in two variables.', 'If D ≠ 0, x = D₁/D and y = D₂/D, where D₁, D₂ replace the x- and y-columns of D by the constants.', 'Statement with D ≠ 0 (2 marks).'),
        ('Why can Cramer\'s rule not be used when D = 0?', 'x = D₁/D would need division by zero; the system has no solution or infinitely many.', 'Division by zero and its meaning (2 marks).'),
        ('Explain how Cramer\'s rule shows that a homogeneous system with D ≠ 0 has only the trivial solution.', 'All of D₁, D₂, D₃ have a column of zeros, so they are 0 and x = y = z = 0.', 'Zero column ⇒ zero determinant (2 marks).'),
    ])(r)


# ======================================================================= table

FAMILIES = {
    S + '01-st1': [F('C1', 'D2', 'mcq', a1s1_mcq), F('C1', 'D1', 'short', a1s1_mod), F('C2', 'D2', 'explain', a1s1_cong), F('C2', 'D3', 'mcq', a1s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a1s1_arith), F('C3', 'D3', 'numerical', a1s1_day), F('C3', 'D4', 'multi_step', a1s1_power), F('C4', 'D3', 'case', a1s1_case),
                   F('C4', 'D4', 'multi_step', a1s1_solve), F('C4', 'D5', 'long', a1s1_power, marks=5), F('C3', 'D1', 'numerical', a1s1_clock), F('C2', 'D2', 'explain', a1s1_explain), F('C2', 'D2', 'numerical', a1s1_mod)],
    S + '01-st2': [F('C1', 'D2', 'mcq', a1s2_mcq), F('C1', 'D1', 'short', a1s2_mean), F('C2', 'D2', 'numerical', a1s2_ratio), F('C2', 'D3', 'mcq', a1s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a1s2_water), F('C3', 'D3', 'multi_step', a1s2_qty), F('C3', 'D4', 'multi_step', a1s2_replace), F('C4', 'D3', 'case', a1s2_case),
                   F('C4', 'D4', 'multi_step', a1s2_two), F('C4', 'D5', 'long', a1s2_profit), F('C3', 'D1', 'numerical', a1s2_ratio)],
    S + '01-st3': [F('C1', 'D2', 'mcq', a1s3_mcq), F('C1', 'D1', 'short', a1s3_speeds), F('C2', 'D2', 'numerical', a1s3_pipes), F('C2', 'D3', 'mcq', a1s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a1s3_leak), F('C3', 'D3', 'multi_step', a1s3_find), F('C3', 'D4', 'multi_step', a1s3_round), F('C4', 'D3', 'case', a1s3_case),
                   F('C4', 'D4', 'long', a1s3_off), F('C4', 'D5', 'long', a1s3_off), F('C3', 'D1', 'numerical', a1s3_pipes)],
    S + '01-st4': [F('C1', 'D2', 'mcq', a1s4_mcq), F('C1', 'D1', 'short', a1s4_partner), F('C2', 'D2', 'numerical', a1s4_chain), F('C2', 'D3', 'mcq', a1s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a1s4_start), F('C3', 'D3', 'multi_step', a1s4_time), F('C3', 'D4', 'multi_step', a1s4_game), F('C4', 'D3', 'case', a1s4_case),
                   F('C4', 'D4', 'multi_step', a1s4_join), F('C4', 'D5', 'long', a1s4_working), F('C3', 'D1', 'numerical', a1s4_partner)],
    S + '02-st1': [F('C1', 'D2', 'mcq', a2s1_mcq), F('C1', 'D1', 'short', a2s1_lin), F('C2', 'D2', 'numerical', a2s1_lin), F('C2', 'D3', 'mcq', a2s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a2s1_nat), F('C3', 'D3', 'multi_step', a2s1_frac), F('C3', 'D4', 'multi_step', a2s1_double), F('C4', 'D3', 'case', a2s1_case),
                   F('C4', 'D4', 'multi_step', a2s1_double), F('C4', 'D5', 'long', a2s1_frac, marks=5), F('C3', 'D1', 'numerical', a2s1_nat)],
    S + '02-st2': [F('C1', 'D2', 'mcq', a2s2_mcq), F('C1', 'D1', 'short', a2s2_interval), F('C2', 'D2', 'explain', a2s2_explain), F('C2', 'D3', 'mcq', a2s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a2s2_graph), F('C3', 'D3', 'multi_step', a2s2_system), F('C4', 'D3', 'case', a2s2_case), F('C4', 'D4', 'multi_step', a2s2_system),
                   F('C3', 'D1', 'numerical', a2s2_interval), F('C2', 'D2', 'numerical', a2s2_graph)],
    S + '02-st3': [F('C1', 'D2', 'mcq', a2s3_mcq), F('C1', 'D1', 'short', a2s3_marks), F('C2', 'D2', 'numerical', a2s3_budget), F('C2', 'D3', 'mcq', a2s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a2s3_temp), F('C3', 'D3', 'multi_step', a2s3_consec), F('C3', 'D4', 'long', a2s3_acid), F('C4', 'D3', 'case', a2s3_case),
                   F('C4', 'D4', 'long', a2s3_acid), F('C4', 'D5', 'long', a2s3_acid), F('C3', 'D1', 'numerical', a2s3_marks)],
    S + '03-st1': reuse('03-st1') + reuse('03-st2', skip=('c3s2_ch',)),
    S + '03-st2': reuse('04-st1') + reuse('04-st3', skip=('c4s3_inv3',)),
    S + '03-st3': reuse('03-st4') + reuse('04-st4') + [F('C4', 'D5', 'long', reuse('04-st3')[6].gen)],
    S + '03-st4': [F('C1', 'D2', 'mcq', a3s4_mcq), F('C1', 'D1', 'short', a3s4_consist), F('C2', 'D2', 'explain', a3s4_explain), F('C2', 'D3', 'mcq', a3s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', a3s4_two), F('C3', 'D3', 'multi_step', a3s4_two), F('C3', 'D4', 'long', a3s4_three), F('C4', 'D3', 'case', a3s4_case),
                   F('C4', 'D4', 'long', a3s4_word), F('C4', 'D5', 'long', a3s4_three), F('C3', 'D1', 'numerical', a3s4_two), F('C2', 'D2', 'numerical', a3s4_consist)],
}
