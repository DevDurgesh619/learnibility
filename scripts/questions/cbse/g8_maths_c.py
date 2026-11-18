"""CBSE class 8 maths (Ganita Prakash) families, chapters 10-14."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, frac, name, two_names, inr, num_distractors, CITIES

S = 'cbse-g8-maths-ch'
ITEMS = [('school bag', 600, 1800), ('cycle', 3500, 9000), ('mobile phone', 6000, 18000), ('pressure cooker', 900, 2500), ('table fan', 1200, 3200),
         ('cricket bat', 800, 2400), ('watch', 700, 3000), ('saree', 1500, 6000), ('study table', 2500, 7000), ('mixer grinder', 1800, 4500)]


def item(r):
    n, lo, hi = r.choice(ITEMS)
    return n, r.randrange(lo, hi, 50)


# ---------------- ch10 Proportional Reasoning-2 ----------------
# st1 Percentages and percentage change

def c10s1_to_pct(r):
    n, d = r.choice([(3, 8), (7, 20), (3, 5), (9, 25), (1, 8), (11, 40), (13, 20)])
    return {'stem': f'Write {n}/{d} as a percentage.', 'answer': f'{num(100 * n / d)}%', 'key': f'{n}/{d} × 100 = {num(100 * n / d)}%.',
            'distractors': [f'{n}{d}%', f'{num(n / d, 3)}%', f'{num(100 * d / n)}%']}


def c10s1_of(r):
    p = r.choice([5, 12, 15, 18, 25, 35, 40, 62.5, 7.5])
    x = r.choice([240, 360, 480, 640, 800, 1200, 1600])
    return {'stem': f'Find {num(p)}% of {x}.', 'answer': num(p * x / 100), 'key': f'{num(p)}/100 × {x} = {num(p * x / 100)}.',
            'distractors': num_distractors(p * x / 100, p * x / 10, x / p, p + x)}


def c10s1_change(r):
    old = r.randrange(200, 2000, 20)
    pct = r.choice([5, 10, 12, 15, 20, 25, 30, 40])
    up = r.random() < 0.5
    new = old * (1 + pct / 100) if up else old * (1 - pct / 100)
    thing = r.choice(['the price of a litre of milk (in paise)', 'a school\'s enrolment', 'the number of visitors to a museum', 'a family\'s electricity bill (₹)'])
    return {'stem': f'{thing.capitalize()} changed from {old} to {num(new)}. Find the percentage {"increase" if up else "decrease"}.', 'answer': f'{pct}%',
            'key': f'Change {num(abs(new - old))}; ÷ original {old} × 100 = {pct}%.', 'distractors': [f'{num(round(abs(new - old) / new * 100, 1))}%', f'{pct * 2}%', f'{num(abs(new - old))}%']}


def c10s1_by_to(r):
    x = r.randrange(400, 2000, 100)
    p = r.choice([10, 20, 25, 50])
    return {'stem': f'Explain the difference between "increased BY {p}%" and "increased TO {100 + p}%" for a price of {inr(x)}. What is the new price in each case?',
            'answer': f'Both give {inr(x * (100 + p) / 100)}', 'key': f'"By {p}%" adds {p}% of the price; "to {100 + p}%" means the new price is {100 + p}% of the old: same value.', 'gap': 'G7'}


def c10s1_reverse(r):
    p = r.choice([10, 20, 25, 40, 50])
    new = r.randrange(300, 3000, 60)
    old = new / (1 + p / 100)
    while not float(old).is_integer():
        new += 60
        old = new / (1 + p / 100)
    return {'stem': f'After a {p}% increase, a train ticket costs {inr(new)}. What was the price before the increase?', 'answer': inr(old),
            'key': f'{100 + p}% of the old price = {new}; old = {new} × 100/{100 + p} = {inr(old)}.', 'distractors': [inr(new * (1 - p / 100)), inr(new - p), inr(new / (p / 10))]}


def c10s1_successive(r):
    a, b = r.choice([(10, 10), (20, 10), (20, 20), (10, 20), (25, 20), (50, 50)])
    net = ((1 + a / 100) * (1 - b / 100) - 1) * 100
    return {'stem': f'A price is first increased by {a}% and then decreased by {b}%. Is the final price the same as the original? Find the overall percentage change.',
            'answer': f'No; {"increase" if net > 0 else "decrease"} of {num(abs(net))}%', 'key': f'× {1 + a / 100} × {1 - b / 100} = × {num((1 + a / 100) * (1 - b / 100), 4)}.'}


def c10s1_ar(r):
    return ar('A 50% increase followed by a 50% decrease brings a price back to where it started.', 'The 50% decrease is calculated on the larger, increased price.', 'd',
              'A is false (100 → 150 → 75); R is true and shows why.')


def c10s1_marks(r):
    who = name(r)
    got, tot = r.randint(40, 78), r.choice([80, 100, 120])
    got2, tot2 = r.randint(30, 45), 50
    return {'stem': f'{who} scored {got}/{tot} in Maths and {got2}/{tot2} in Science. In which subject did {who} do better? Use percentages.',
            'answer': 'Maths' if got / tot > got2 / tot2 else 'Science', 'key': f'{num(round(100 * got / tot, 1))}% vs {num(round(100 * got2 / tot2, 1))}%.'}


def c10s1_case(r):
    a, b = r.randrange(1200, 2400, 100), r.randrange(1500, 3000, 100)
    return {'stem': (f'A school library had {a} books in 2024 and {b} in 2025; in 2026 it added 10% more than in 2025. '
                     f'(i) Find the percentage change from 2024 to 2025. (ii) How many books in 2026? (iii) Find the overall percentage change from 2024 to 2026.'),
            'answer': f'(i) {num(round(100 * (b - a) / a, 1))}% (ii) {num(b * 1.1)} (iii) {num(round(100 * (b * 1.1 - a) / a, 1))}%',
            'key': '(i) change ÷ 2024 value (ii) 110% of 2025 (iii) change over two years ÷ 2024 value, not the sum of the two percentages.'}


# st2 Profit, loss, discount and tax

def c10s2_formula(r):
    return mcq('Profit percentage is calculated as …', '(Profit ÷ Cost price) × 100', ['(Profit ÷ Selling price) × 100', '(Cost price ÷ Profit) × 100', '(Selling price − Profit) × 100'],
               'Profit and loss percentages are always on the cost price.', r)


def c10s2_profit(r):
    n, cp = item(r)
    p = r.choice([5, 8, 10, 12, 15, 20, 25])
    sp = cp * (1 + p / 100)
    return {'stem': f'A shopkeeper buys a {n} for {inr(cp)} and sells it for {inr(sp)}. Find the profit percentage.', 'answer': f'{p}%',
            'key': f'Profit {inr(sp - cp)}; {num(sp - cp)}/{cp} × 100 = {p}%.', 'distractors': [f'{num(round(100 * (sp - cp) / sp, 2))}%', f'{num(sp - cp)}%', f'{p + 5}%']}


def c10s2_sp(r):
    n, cp = item(r)
    l = r.choice([5, 10, 12, 15, 20])
    return {'stem': f'A {n} bought for {inr(cp)} is sold at a loss of {l}%. Find the selling price.', 'answer': inr(cp * (1 - l / 100)),
            'key': f'SP = {100 - l}% of {cp} = {inr(cp * (1 - l / 100))}.', 'distractors': [inr(cp * (1 + l / 100)), inr(cp - l), inr(cp / (1 - l / 100))]}


def c10s2_discount(r):
    n, mp = item(r)
    d = r.choice([10, 15, 20, 25, 30, 40])
    return {'stem': f'A {n} is marked at {inr(mp)}. During a Diwali sale a discount of {d}% is given. Find the sale price.', 'answer': inr(mp * (1 - d / 100)),
            'key': f'Discount {inr(mp * d / 100)}; sale price {inr(mp * (1 - d / 100))}.', 'distractors': [inr(mp - d), inr(mp * d / 100), inr(mp * (1 + d / 100))]}


def c10s2_gst(r):
    n, p = item(r)
    g = r.choice([5, 12, 18, 28])
    return {'stem': f'The price of a {n} is {inr(p)} before GST. GST is charged at {g}%. How much does the customer pay?', 'answer': inr(p * (1 + g / 100)),
            'key': f'GST = {g}% of {p} = {inr(p * g / 100)}; total {inr(p * (1 + g / 100))}.'}


def c10s2_discount_then_gst(r):
    n, mp = item(r)
    d, g = r.choice([10, 20, 25]), r.choice([5, 12, 18])
    after = mp * (1 - d / 100)
    return {'stem': f'A {n} marked {inr(mp)} is sold at {d}% discount, and then {g}% GST is added on the discounted price. Find the final bill. Does it matter whether discount or GST is applied first?',
            'answer': f'{inr(after * (1 + g / 100))}; no', 'key': f'{mp} × {1 - d / 100} × {1 + g / 100}; multiplication is commutative, so the order does not change the result.'}


def c10s2_cp_from_sp(r):
    p = r.choice([10, 20, 25])
    sp = r.randrange(1100, 6000, 100)
    while (sp * 100) % (100 + p):
        sp += 100
    return {'stem': f'By selling a {item(r)[0]} for {inr(sp)}, a shopkeeper makes a profit of {p}%. Find the cost price.', 'answer': inr(sp * 100 / (100 + p)),
            'key': f'CP = SP × 100/(100 + {p}) = {inr(sp * 100 / (100 + p))}. A common error is taking {p}% of the SP.'}


def c10s2_explain(r):
    return {'stem': 'Explain why a shop that gives a 20% discount on the marked price can still make a profit.', 'answer': 'The marked price is set above the cost price, so 80% of it can still exceed the cost.',
            'key': 'Discount is on marked price; profit is measured on cost price.'}


def c10s2_ar(r):
    return ar('If CP = ₹500 and SP = ₹600, the profit is 20%.', 'Profit % is calculated on the cost price.', 'a', '100/500 × 100 = 20%.')


def c10s2_two_items(r):
    p = r.randrange(1000, 3000, 100)
    k = r.choice([10, 20, 25])
    return {'stem': f'A trader sells two phones at {inr(p)} each, gaining {k}% on one and losing {k}% on the other. Find the overall profit or loss percentage.',
            'answer': f'Loss of {num(round(k * k / 100, 2))}%', 'key': f'CPs {inr(round(p / (1 + k / 100), 2))} and {inr(round(p / (1 - k / 100), 2))}; total CP > total SP; loss % = (k/10)² = {num(k * k / 100)}%.'}


def c10s2_case(r):
    mp = r.randrange(2000, 5000, 100)
    return {'stem': (f'An online store lists headphones at {inr(mp)} with "Flat 30% off + extra 10% off on the sale price". A rival offers "40% off". '
                     f'(i) Find the price at each store. (ii) Which is cheaper and by how much? (iii) Why is 30% + 10% not the same as 40%?'),
            'answer': f'(i) {inr(mp * 0.63)}, {inr(mp * 0.6)} (ii) rival cheaper by {inr(mp * 0.03)} (iii) the second discount is on a smaller amount',
            'key': f'(i) {mp} × 0.7 × 0.9 = {num(mp * 0.63)}; {mp} × 0.6 = {num(mp * 0.6)}.'}


# st3 Simple and compound interest

def c10s3_si_formula(r):
    return mcq('The formula for simple interest is …', 'SI = P × R × T ÷ 100', ['SI = P × (1 + R/100)ᵀ', 'SI = P + R + T', 'SI = P × R ÷ (100 × T)'], 'Interest proportional to principal, rate and time.', r)


def c10s3_si(r):
    P = r.randrange(5000, 50000, 500)
    R = r.choice([4, 5, 6, 7.5, 8, 9, 10, 12])
    T = r.choice([2, 3, 4, 5])
    si = P * R * T / 100
    return {'stem': f'Find the simple interest on {inr(P)} at {num(R)}% per annum for {T} years.', 'answer': inr(si), 'key': f'{P} × {num(R)} × {T} ÷ 100 = {inr(si)}.',
            'distractors': [inr(P * R / 100), inr(si + P), inr(P * (1 + R / 100) ** T - P)]}


def c10s3_ci(r):
    P = r.randrange(5000, 40000, 1000)
    R = r.choice([5, 8, 10, 12, 20])
    T = r.choice([2, 3])
    A = P * (1 + R / 100) ** T
    return {'stem': f'Find the compound interest on {inr(P)} at {R}% per annum, compounded annually, for {T} years.', 'answer': inr(round(A - P, 2)),
            'key': f'A = {P}(1 + {R}/100){sup(T)} = {inr(round(A, 2))}; CI = A − P = {inr(round(A - P, 2))}.',
            'distractors': [inr(P * R * T / 100), inr(round(A, 2)), inr(round(A - P, 2) + 100)]}


def c10s3_diff(r):
    P = r.randrange(4000, 30000, 1000)
    R = r.choice([5, 10, 15, 20])
    d = P * (R / 100) ** 2
    return {'stem': f'Find the difference between compound interest and simple interest on {inr(P)} at {R}% per annum for 2 years.', 'answer': inr(d),
            'key': f'CI − SI = P(R/100)² = {P} × {num((R / 100) ** 2, 4)} = {inr(d)} (interest on the first year\'s interest).'}


def c10s3_explain(r):
    return {'stem': 'Explain in two lines why compound interest is more than simple interest for the same principal, rate and time (more than one year).',
            'answer': 'In compound interest, each year\'s interest earns interest in the following years.', 'key': 'Principal grows each year for CI; stays fixed for SI.'}


def c10s3_find_rate(r):
    P = r.randrange(2000, 20000, 500)
    R = r.choice([4, 5, 6, 8, 10])
    T = r.choice([2, 3, 4, 5])
    return {'stem': f'At what rate of simple interest will {inr(P)} amount to {inr(P + P * R * T / 100)} in {T} years?', 'answer': f'{R}% per annum',
            'key': f'SI = {inr(P * R * T / 100)}; R = SI × 100/(P × T) = {R}%.'}


def c10s3_ar(r):
    return ar('For one year, compounded annually, CI and SI on the same sum are equal.', 'In the first year interest is calculated on the original principal in both cases.', 'a', 'R explains why they match.')


def c10s3_depreciation(r):
    v = r.randrange(40000, 90000, 5000)
    d = r.choice([10, 15, 20])
    return {'stem': f'A scooter bought for {inr(v)} loses {d}% of its value every year. What will it be worth after 2 years?', 'answer': inr(v * (1 - d / 100) ** 2),
            'key': f'{v} × (1 − {d}/100)² = {inr(v * (1 - d / 100) ** 2)} (depreciation compounds like interest).'}


def c10s3_population(r):
    p = r.randrange(20000, 80000, 1000)
    g = r.choice([2, 4, 5, 10])
    town = r.choice(CITIES)
    return {'stem': f'The population of a ward in {town} is {p} and grows at {g}% per year. Estimate the population after 3 years.', 'answer': f'{round(p * (1 + g / 100) ** 3)}',
            'key': f'{p} × (1 + {g}/100)³ ≈ {round(p * (1 + g / 100) ** 3)}.'}


def c10s3_half(r):
    P = r.randrange(10000, 40000, 2000)
    R = r.choice([8, 10, 12])
    A = P * (1 + R / 200) ** 2
    return {'stem': f'Find the amount on {inr(P)} for 1 year at {R}% per annum compounded half-yearly. Compare it with yearly compounding.', 'answer': inr(round(A, 2)),
            'key': f'Rate per half-year {R / 2}%, 2 periods: {P}(1 + {R / 200})² = {inr(round(A, 2))}; yearly gives {inr(P * (1 + R / 100))}, which is less.'}


def c10s3_case(r):
    P = r.choice([50000, 100000, 200000])
    return {'stem': (f'Two banks offer an education deposit for {inr(P)} for 3 years: Bank A pays 8% simple interest, Bank B pays 7.5% compounded annually. '
                     f'(i) Find the amount from each bank. (ii) Which is better? (iii) Would the answer change for 10 years? Explain.'),
            'answer': f'(i) A {inr(P * 1.24)}, B {inr(round(P * 1.075 ** 3, 2))} (ii) Bank A (iii) yes, compounding wins over long periods',
            'key': f'(iii) 10 years: A {inr(P * 1.8)}, B {inr(round(P * 1.075 ** 10, 2))}.'}


# ---------------- ch11 Exploring Some Geometric Themes ----------------
# st1 Line and rotational symmetry

SHAPES = {'square': (4, 4), 'equilateral triangle': (3, 3), 'rectangle': (2, 2), 'rhombus': (2, 2), 'regular hexagon': (6, 6), 'regular pentagon': (5, 5),
          'isosceles triangle': (1, 1), 'parallelogram (not a rectangle or rhombus)': (0, 2), 'circle': ('infinitely many', 'infinite'), 'kite': (1, 1), 'regular octagon': (8, 8)}


def c11s1_lines(r):
    s = r.choice([k for k in SHAPES if k != 'circle'])
    n = SHAPES[s][0]
    return {'stem': f'How many lines of symmetry does a {s} have?', 'answer': str(n), 'key': f'{s}: {n}.',
            'distractors': [str(x) for x in r.sample([y for y in range(0, 9) if y != n], 3)]}


def c11s1_order(r):
    s = r.choice([k for k in SHAPES if k not in ('circle', 'isosceles triangle', 'kite')])
    n = SHAPES[s][1]
    return {'stem': f'What is the order of rotational symmetry of a {s}?', 'answer': str(n), 'key': f'It looks the same {n} times in a full turn (every {360 // n}°).',
            'distractors': [str(x) for x in r.sample([y for y in range(1, 9) if y != n], 3)]}


def c11s1_letters(r):
    word = r.choice(['MATH', 'HOOK', 'NOON', 'SWIM', 'TAXI', 'BOX', 'ZONE', 'HIKE'])
    lines = {'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'H': 2, 'I': 2, 'K': 1, 'M': 1, 'N': 0, 'O': 2, 'S': 0, 'T': 1, 'W': 1, 'X': 2, 'Z': 0}
    rot = {'H', 'I', 'N', 'O', 'S', 'X', 'Z'}
    have = [c for c in word if c in rot]
    return {'stem': f'Which letters of the word {word} (in capitals) have rotational symmetry of order 2? Which have no line of symmetry?',
            'answer': f'Rotational: {", ".join(sorted(set(have))) or "none"}; no line: {", ".join(sorted({c for c in word if lines.get(c, 1) == 0})) or "none"}',
            'key': 'H, I, N, O, S, X, Z look the same after a half turn; N, S, Z have no line of symmetry.'}


def c11s1_explain(r):
    return {'stem': 'Explain why a parallelogram that is not a rectangle or rhombus has rotational symmetry but no line of symmetry.',
            'answer': 'A half turn about the intersection of its diagonals maps it onto itself, but folding along any line does not.', 'key': 'Diagonals bisect each other → order 2; no fold line matches sides and angles.'}


def c11s1_angle(r):
    n = r.choice([3, 4, 5, 6, 8, 9, 10, 12])
    return {'stem': f'A regular polygon has rotational symmetry of order {n}. What is the smallest angle of rotation that maps it onto itself?', 'answer': f'{num(360 / n)}°',
            'key': f'360° ÷ {n}.', 'distractors': [f'{num(180 / n)}°', f'{num((n - 2) * 180 / n)}°', f'{n * 10}°']}


def c11s1_ar(r):
    return ar('A regular hexagon has 6 lines of symmetry.', 'A regular polygon with n sides has n lines of symmetry.', 'a', 'R is the general rule; n = 6.')


def c11s1_rangoli(r):
    n = r.choice([4, 6, 8])
    return {'stem': f'Ananya is drawing a rangoli with {n} identical petals arranged evenly around a centre. State the order of rotational symmetry and the number of lines of symmetry (if each petal is itself symmetric). How would adding one dot on only one petal change your answers?',
            'answer': f'Order {n}, {n} lines; with the extra dot: order 1 and at most 1 line', 'key': 'Symmetry needs every part to match; one extra dot breaks the matching.'}


# st2 Geometric constructions and patterns

def c11s2_tools(r):
    return mcq('Which two instruments are used in a classical geometric construction?', 'Ruler (straight edge) and compass', ['Protractor and set square', 'Ruler and protractor', 'Compass and protractor'],
               'Classical constructions use only an unmarked straight edge and a compass.', r)


def c11s2_bisector(r):
    l = r.randint(5, 12)
    return {'stem': f'Write the steps to construct the perpendicular bisector of a line segment AB of length {l} cm, using ruler and compass only.', 'answer': 'Arcs from A and B with radius more than half AB; join the two crossing points.',
            'key': f'Radius > {num(l / 2)} cm; the line through the two intersections bisects AB at 90°.'}


def c11s2_angle(r):
    a = r.choice([60, 30, 90, 45, 120, 15])
    how = {60: 'arc from the vertex, then an equal arc from where it cuts the arm', 30: 'construct 60° then bisect it', 90: 'construct a perpendicular (or 60° + 30°)',
           45: 'construct 90° and bisect it', 120: 'two consecutive 60° steps', 15: 'construct 60°, bisect to 30°, bisect again'}
    return {'stem': f'How can an angle of {a}° be constructed with ruler and compass only?', 'answer': how[a], 'key': 'Standard construction steps.'}


def c11s2_hexagon(r):
    rad = r.randint(3, 6)
    return {'stem': f'Explain why stepping off the radius ({rad} cm) six times around a circle gives a regular hexagon.', 'answer': 'Each chord equals the radius, so each centre triangle is equilateral with 60° at the centre; 6 × 60° = 360°.',
            'key': 'Six equilateral triangles.'}


def c11s2_ar(r):
    return ar('An angle of 75° can be constructed with ruler and compass.', '75° = 60° + 15°, and both can be constructed.', 'a', '15° by bisecting 30°.')


def c11s2_pattern(r):
    n = r.randint(3, 7)
    return {'stem': f'Circles of equal radius are drawn so that each passes through the centres of its neighbours, in a row of {n} circles. How many points are there where two circles cross?',
            'answer': str(2 * (n - 1)), 'key': f'Each neighbouring pair crosses twice: 2 × ({n} − 1) = {2 * (n - 1)}.'}


def c11s2_triangle(r):
    a, b, c = sorted(r.sample(range(3, 11), 3))
    ok = a + b > c
    return {'stem': f'Can a triangle with sides {a} cm, {b} cm and {c} cm be constructed? Explain.', 'answer': 'Yes' if ok else 'No',
            'key': f'{a} + {b} = {a + b} {">" if ok else "≤"} {c}.', 'distractors': ['No' if ok else 'Yes', 'Only a right triangle', 'Only with a protractor']}


# st3 Tessellations and tilings

def c11s3_def(r):
    return mcq('A tessellation is …', 'a covering of a flat surface with shapes, leaving no gaps and no overlaps', ['any pattern with a line of symmetry', 'a solid made of polygons', 'a pattern of circles only'],
               'Definition.', r)


def c11s3_regular(r):
    n = r.choice([3, 4, 5, 6, 8, 10, 12])
    ang = (n - 2) * 180 / n
    ok = 360 % ang == 0
    return {'stem': f'Can regular {n}-sided polygons tessellate on their own? Justify using the interior angle.', 'answer': 'Yes' if ok else 'No',
            'key': f'Interior angle {num(ang)}°; 360 ÷ {num(ang)} = {num(360 / ang, 2)} {"is" if ok else "is not"} a whole number.',
            'distractors': ['No' if ok else 'Yes', 'Only if the side is 1 cm', 'Only with circles']}


def c11s3_vertex(r):
    combo, ok = r.choice([('two octagons and a square', True), ('a hexagon, two squares and a triangle', True), ('two hexagons and two triangles', True),
                          ('a pentagon and two hexagons', False), ('three triangles and two squares', True), ('two pentagons and a decagon', True)])
    return {'stem': f'Regular polygons meet at a point: {combo}. Do their angles fit exactly around the point? Show your working.', 'answer': 'Yes' if ok else 'No',
            'key': 'Add the interior angles (triangle 60, square 90, pentagon 108, hexagon 120, octagon 135, decagon 144) and compare with 360°.'}


def c11s3_explain(r):
    return {'stem': 'Explain why any triangle (not only an equilateral one) can tessellate.', 'answer': 'Two copies make a parallelogram; parallelograms tile in strips. At each vertex the three angles appear twice: 2 × 180° = 360°.',
            'key': 'Angle-sum argument at a vertex.'}


def c11s3_ar(r):
    return ar('Regular pentagons cannot tessellate on their own.', 'The interior angle of a regular pentagon, 108°, does not divide 360° exactly.', 'a', '360 ÷ 108 is not whole.')


def c11s3_floor(r):
    l, b = r.randint(3, 8), r.randint(2, 6)
    t = r.choice([20, 25, 40, 50])
    return {'stem': f'A floor {l} m by {b} m is to be covered with square tiles of side {t} cm. How many tiles are needed?', 'answer': str(int(l * 100 / t) * int(b * 100 / t)),
            'key': f'{l * 100 // t} tiles along the length × {b * 100 // t} along the width.' if (l * 100) % t == 0 and (b * 100) % t == 0 else 'Area ÷ tile area.'}


# ---------------- ch12 Tales by Dots and Lines ----------------
# st1 Coordinate plane and plotting points

def c12s1_origin(r):
    return mcq('What are the coordinates of the origin?', '(0, 0)', ['(1, 1)', '(0, 1)', '(1, 0)'], 'The origin is where the axes meet.', r)


def c12s1_quadrant(r):
    x, y = r.choice([-1, 1]) * r.randint(1, 9), r.choice([-1, 1]) * r.randint(1, 9)
    q = {(1, 1): 'I', (-1, 1): 'II', (-1, -1): 'III', (1, -1): 'IV'}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
    return {'stem': f'In which quadrant does the point ({num(x)}, {num(y)}) lie?', 'answer': f'Quadrant {q}', 'key': 'Signs of x and y.',
            'distractors': [f'Quadrant {z}' for z in ('I', 'II', 'III', 'IV') if z != q]}


def c12s1_axis(r):
    a = r.randint(2, 9)
    p = r.choice([(a, 0), (0, a), (-a, 0), (0, -a)])
    ax = 'x-axis' if p[1] == 0 else 'y-axis'
    return {'stem': f'On which axis does the point ({num(p[0])}, {num(p[1])}) lie? Explain.', 'answer': ax.capitalize(), 'key': f'Its {"y" if ax == "x-axis" else "x"}-coordinate is 0.'}


def c12s1_rect(r):
    a, b = r.randint(2, 7), r.randint(2, 6)
    return {'stem': f'Three vertices of a rectangle are (0, 0), ({a}, 0) and ({a}, {b}). Find the fourth vertex and the area of the rectangle.', 'answer': f'(0, {b}); {a * b} square units',
            'key': 'Opposite sides parallel to the axes.'}


def c12s1_mirror(r):
    x, y = r.randint(1, 9), r.randint(1, 9)
    return {'stem': f'Reflect the point ({x}, {y}) in the x-axis and then in the y-axis. Where does it end up, and how is this related to a half turn about the origin?',
            'answer': f'(−{x}, −{y}); the same as a 180° rotation', 'key': 'Each reflection changes the sign of one coordinate.'}


def c12s1_ar(r):
    return ar('The point (−3, 5) lies in the second quadrant.', 'In the second quadrant x is negative and y is positive.', 'a', 'R explains A.')


def pt(p):
    return f'({num(p[0])}, {num(p[1])})'


def c12s1_map(r):
    places = r.sample(['school', 'library', 'park', 'temple', 'market', 'post office', 'hospital'], 3)
    pts = [(r.randint(-6, 6), r.randint(-6, 6)) for _ in places]
    return {'stem': f'On a town grid (1 unit = 100 m), the {places[0]} is at {pt(pts[0])}, the {places[1]} at {pt(pts[1])} and the {places[2]} at {pt(pts[2])}. Walking only along grid lines, how far is it from the {places[0]} to the {places[1]}?',
            'answer': f'{(abs(pts[0][0] - pts[1][0]) + abs(pts[0][1] - pts[1][1])) * 100} m', 'key': 'Horizontal difference + vertical difference, × 100 m.'}


# st2 Reading and drawing line graphs

def c12s2_flat(r):
    return mcq('On a distance–time graph, a horizontal segment means the object is …', 'at rest', ['moving at constant speed', 'speeding up', 'moving backwards'],
               'Distance does not change with time.', r)


def c12s2_read(r):
    hrs = [6, 8, 10, 12, 14, 16]
    temps = [r.randint(18, 24)]
    for _ in range(5):
        temps.append(temps[-1] + r.choice([-1, 1, 2, 3, 2, -2]))
    i = r.randint(1, 5)
    return {'stem': f'A line graph of temperature in {r.choice(CITIES)} shows these points (hour, °C): ' + ', '.join(f'({h}, {t})' for h, t in zip(hrs, temps)) +
                    f'. Between which two readings did the temperature rise the most?',
            'answer': max(((hrs[k], hrs[k + 1], temps[k + 1] - temps[k]) for k in range(5)), key=lambda x: x[2]).__str__(),
            'key': 'Compare the differences between consecutive readings; the steepest rising segment.'}


def c12s2_speed(r):
    t = r.randint(2, 5)
    d = r.choice([30, 40, 45, 60]) * t
    return {'stem': f'A distance–time graph of a bus is a straight line from (0 h, 0 km) to ({t} h, {d} km). What is its speed? What would a steeper line mean?', 'answer': f'{d // t} km/h; a higher speed',
            'key': 'Speed = distance ÷ time = slope of the line.'}


def c12s2_choose(r):
    data = r.choice([('a patient\'s temperature every hour', 'line graph'), ('favourite sports of 40 students', 'bar graph'),
                     ('height of a plant every week', 'line graph'), ('how a family\'s budget is divided', 'pie chart')])
    return {'stem': f'Which graph would you use to show {data[0]}? Give a reason.', 'answer': data[1].capitalize(),
            'key': 'Line graphs show change over time; bar graphs compare categories; pie charts show parts of a whole.',
            'distractors': [g.capitalize() for g in ('line graph', 'bar graph', 'pie chart', 'histogram') if g != data[1]]}


def c12s2_ar(r):
    return ar('A line graph is suitable for showing how a child\'s height changes over the years.', 'Line graphs show how one quantity changes as another, such as time, changes.', 'a', 'R explains A.')


def c12s2_trip(r):
    who = name(r)
    a, b = r.randint(10, 20), r.randint(5, 15)
    return {'stem': f'{who} cycles {a} km in the first hour, rests for 30 minutes, then cycles {b} km in the next hour. Describe the shape of the distance–time graph and find the average speed for the whole trip.',
            'answer': f'Rising line, flat segment, rising line; {num(round((a + b) / 2.5, 2))} km/h', 'key': f'Total {a + b} km in 2.5 h.'}


def c12s2_case(r):
    m = [r.randint(150, 400) for _ in range(6)]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    return {'stem': ('A family\'s electricity use (units) was: ' + ', '.join(f'{a} {b}' for a, b in zip(months, m)) +
                     '. (i) Which month had the highest use? (ii) Between which two months was the largest increase? (iii) Suggest a reason for the trend from March to June.'),
            'answer': f'(i) {months[m.index(max(m))]} (ii) ' + max(((months[k], months[k + 1], m[k + 1] - m[k]) for k in range(5)), key=lambda x: x[2])[0] + ' to ' +
                      max(((months[k], months[k + 1], m[k + 1] - m[k]) for k in range(5)), key=lambda x: x[2])[1] + ' (iii) e.g. summer: fans and coolers',
            'key': '1 + 2 + 1 marks; any sensible reason for (iii).'}


# st3 Linear relationships from tables to graphs

def c12s3_value(r):
    k = r.randint(2, 9)
    x = r.randint(3, 12)
    return {'stem': f'For y = {k}x, find y when x = {x}.', 'answer': str(k * x), 'key': f'{k} × {x}.', 'distractors': num_distractors(k * x, k + x, k * x + k, x)}


def c12s3_rule(r):
    m, c = r.randint(2, 6), r.randint(1, 9)
    xs = [1, 2, 3, 4]
    return {'stem': f'Find the rule connecting x and y: x = 1, 2, 3, 4; y = {", ".join(str(m * x + c) for x in xs)}.', 'answer': f'y = {m}x + {c}',
            'key': f'y increases by {m} each time x increases by 1; at x = 1, y = {m + c} so c = {c}.', 'distractors': [f'y = {m + c}x', f'y = {c}x + {m}', f'y = x + {m + c - 1}']}


def c12s3_through_origin(r):
    m, c = r.randint(2, 6), r.randint(1, 9)
    return {'stem': f'Will the graph of y = {m}x + {c} pass through the origin? Explain, and say how it differs from y = {m}x.', 'answer': 'No',
            'key': f'At x = 0, y = {c} ≠ 0. It is parallel to y = {m}x, shifted up by {c}.'}


def c12s3_taxi(r):
    fix, per = r.choice([30, 40, 50, 60]), r.choice([12, 14, 15, 18, 20])
    km = r.randint(5, 25)
    return {'stem': f'A taxi charges {inr(fix)} plus {inr(per)} per km. Write the rule for the fare y (₹) for x km, find the fare for {km} km, and say whether the graph is a straight line.',
            'answer': f'y = {per}x + {fix}; {inr(per * km + fix)}; yes', 'key': 'Linear: constant increase per km.'}


def c12s3_ar(r):
    return ar('The points (1, 3), (2, 5) and (3, 7) lie on a straight line.', 'y increases by the same amount for each equal increase in x.', 'a', 'Constant difference → linear.')


def c12s3_check(r):
    m, c = r.randint(2, 5), r.randint(0, 6)
    x = r.randint(2, 9)
    y = m * x + c + r.choice([0, 0, 1, -1])
    ok = y == m * x + c
    return {'stem': f'Does the point ({x}, {y}) lie on the line y = {m}x + {c}?', 'answer': 'Yes' if ok else 'No', 'key': f'{m} × {x} + {c} = {m * x + c}.',
            'distractors': ['No' if ok else 'Yes', 'Only if x is negative', 'It lies on the y-axis']}


def c12s3_case(r):
    rate = r.choice([2, 3, 4, 5])
    start = r.randint(5, 20)
    return {'stem': (f'A candle is {start + 6 * rate} cm tall and burns {rate} cm every hour. (i) Make a table for 0 to 4 hours. (ii) Write the rule for the height h after t hours. '
                     f'(iii) When will the candle burn out?'),
            'answer': f'(ii) h = {start + 6 * rate} − {rate}t (iii) after {num((start + 6 * rate) / rate)} hours', 'key': 'Decreasing linear relationship.'}


# ---------------- ch13 Algebra Play ----------------
# st1 Algebraic identities

def c13s1_complete(r):
    which = r.choice(['(a + b)²', '(a − b)²', '(a + b)(a − b)'])
    ans = {'(a + b)²': 'a² + 2ab + b²', '(a − b)²': 'a² − 2ab + b²', '(a + b)(a − b)': 'a² − b²'}[which]
    others = [v for v in ['a² + 2ab + b²', 'a² − 2ab + b²', 'a² − b²', 'a² + b²', 'a² − 2ab − b²'] if v != ans]
    return mcq(f'{which} = ?', ans, r.sample(others, 3), 'Standard identity.', r)


def c13s1_expand(r):
    a, b = r.randint(2, 7), r.randint(1, 9)
    s = r.choice(['+', '−'])
    return {'stem': f'Expand ({a}x {s} {b})² using an identity.', 'answer': f'{a * a}x² {s} {2 * a * b}x + {b * b}',
            'key': f'(p {s} q)² = p² {s} 2pq + q² with p = {a}x, q = {b}.', 'distractors': [f'{a * a}x² + {b * b}', f'{a}x² {s} {2 * a * b}x + {b * b}', f'{a * a}x² {s} {a * b}x + {b * b}']}


def c13s1_mental(r):
    n = r.choice([r.randint(101, 109), r.randint(91, 99), r.randint(41, 49) * 1, r.randint(51, 59)])
    base = round(n, -1) if n % 10 < 5 else round(n, -1)
    d = n - base
    return {'stem': f'Use an identity to find {n}² mentally.', 'answer': str(n * n),
            'key': f'({base} {"+" if d >= 0 else "−"} {abs(d)})² = {base * base} {"+" if d >= 0 else "−"} {2 * base * abs(d)} + {d * d} = {n * n}.',
            'distractors': num_distractors(n * n, base * base + d * d, n * n - 2 * base, n * n + 100)}


def c13s1_diff_sq(r):
    a = r.randint(51, 99)
    b = r.randint(11, a - 5)
    return {'stem': f'Find {a}² − {b}² without squaring either number.', 'answer': str(a * a - b * b), 'key': f'({a} + {b})({a} − {b}) = {a + b} × {a - b} = {a * a - b * b}.'}


def c13s1_explain(r):
    return {'stem': r.choice(['Explain, using areas of squares and rectangles, why (a + b)² ≠ a² + b².', 'Use a diagram of a square of side (a + b) to show that (a + b)² = a² + 2ab + b².']),
            'answer': 'The big square splits into a², b² and two rectangles of area ab.', 'key': 'Area decomposition with the two ab rectangles named.'}


def c13s1_value(r):
    s, p = r.randint(5, 15), r.randint(4, 30)
    return {'stem': f'If a + b = {s} and ab = {p}, find a² + b².', 'answer': str(s * s - 2 * p), 'key': f'(a + b)² − 2ab = {s * s} − {2 * p} = {s * s - 2 * p}.'}


def c13s1_ar(r):
    return ar('(x + 3)² = x² + 9.', '(a + b)² = a² + 2ab + b².', 'd', 'A is false (missing 6x); R is true.')


def c13s1_product(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return {'stem': f'Use (x + a)(x + b) = x² + (a + b)x + ab to multiply (y + {a})(y + {b}), and then find the value when y = 10.',
            'answer': f'y² + {a + b}y + {a * b}; {(10 + a) * (10 + b)}', 'key': f'At y = 10: 100 + {10 * (a + b)} + {a * b}.'}


def c13s1_case(r):
    a = r.randint(6, 15)
    w = r.choice([1, 2, 3])
    return {'stem': (f'A square courtyard of side a m has a path of width {w} m around it on the outside. '
                     f'(i) Write the outer area using an identity. (ii) Find the area of the path as an expression. (iii) Find it when a = {a}.'),
            'answer': f'(i) a² + {4 * w}a + {4 * w * w} (ii) {4 * w}a + {4 * w * w} (iii) {4 * w * a + 4 * w * w} m²', 'key': f'(a + {2 * w})² − a².'}


# st2 Factorisation of expressions

def c13s2_hcf(r):
    a, b = r.choice([(12, 18), (8, 20), (15, 25), (14, 21), (16, 24)])
    p, q = r.randint(2, 3), 1
    g = math.gcd(a, b)
    return {'stem': f'What is the highest common factor of {a}x{sup(p)} and {b}x?', 'answer': f'{g}x', 'key': f'HCF of {a} and {b} is {g}; lowest power of x is 1.',
            'distractors': [f'{g}x{sup(p)}', f'{a * b // g}x{sup(p)}', f'{g}']}


def c13s2_common(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6)
    g = c * math.gcd(a, b)
    p, q = a * c // g, b * c // g
    return {'stem': f'Factorise {a * c}x² + {b * c}x.', 'answer': f'{g}x({"" if p == 1 else p}x + {q})',
            'key': 'Take out the HCF of all terms.'}


def c13s2_identity(r):
    a, b = r.randint(2, 9), r.randint(1, 9)
    kind = r.choice(['sq', 'diff'])
    if kind == 'sq':
        return {'stem': f'Factorise {a * a}x² + {2 * a * b}x + {b * b}.', 'answer': f'({a}x + {b})²', 'key': 'Matches p² + 2pq + q².',
                'distractors': [f'({a}x + {b})({a}x − {b})', f'({a * a}x + {b})²', f'({a}x + {b * b})²']}
    return {'stem': f'Factorise {a * a}x² − {b * b}.', 'answer': f'({a}x + {b})({a}x − {b})', 'key': 'Difference of squares.',
            'distractors': [f'({a}x − {b})²', f'({a}x + {b})²', f'{a}x({a}x − {b})']}


def c13s2_trinomial(r):
    p, q = r.randint(1, 9), r.randint(1, 9)
    sp, sq_ = r.choice([1, -1]), r.choice([1, -1])
    P, Q = sp * p, sq_ * q
    def sg(v):
        return f'{"+" if v >= 0 else "−"} {abs(v)}'
    mid = P + Q
    expr = f'x² {sg(mid)}x {sg(P * Q)}'.replace('+ 0x ', '').replace('+ 1x', '+ x').replace('− 1x', '− x')
    return {'stem': f'Factorise {expr}.', 'answer': f'(x {sg(P)})(x {sg(Q)})', 'key': f'Two numbers with product {P * Q} and sum {mid}: {P} and {Q}.'}


def c13s2_group(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return {'stem': f'Factorise by grouping: x² + {a}x + {b}x + {a * b}.', 'answer': f'(x + {a})(x + {b})', 'key': f'x(x + {a}) + {b}(x + {a}).'}


def c13s2_explain(r):
    return {'stem': 'Explain why factorising is the reverse of expanding, using x² + 5x + 6 = (x + 2)(x + 3) as an example. How can you check a factorisation?',
            'answer': 'Expanding (x + 2)(x + 3) gives back x² + 5x + 6; check by multiplying out or substituting a value.', 'key': 'Reverse process + any check.'}


def c13s2_ar(r):
    return ar('x² − 9 = (x − 3)(x + 3).', 'a² − b² = (a − b)(a + b).', 'a', 'Identity with a = x, b = 3.')


def c13s2_area(r):
    p, q = r.randint(1, 8), r.randint(1, 8)
    return {'stem': f'The area of a rectangle is (x² + {p + q}x + {p * q}) cm². Find possible expressions for its length and breadth, and the perimeter.',
            'answer': f'(x + {max(p, q)}) and (x + {min(p, q)}); perimeter (4x + {2 * (p + q)}) cm', 'key': 'Factorise the area.'}


def c13s2_numbers(r):
    a = r.randint(61, 99)
    b = r.randint(11, 39)
    return {'stem': f'Without a calculator, show that {a}² − {b}² is divisible by {a + b}.', 'answer': f'{a}² − {b}² = {a + b} × {a - b}', 'key': 'Difference of squares.'}


# st3 Linear equations in one variable and word problems

def c13s3_simple(r):
    a, x = r.randint(2, 30), r.randint(2, 30)
    return {'stem': f'Solve x + {a} = {x + a}.', 'answer': f'x = {x}', 'key': f'Subtract {a} from both sides.', 'distractors': [f'x = {x + 2 * a}', f'x = {a}', f'x = {x + 1}']}


def c13s3_two_step(r):
    a, b, x = r.randint(2, 9), r.randint(1, 20), r.randint(-5, 15)
    return {'stem': f'Solve {a}x − {b} = {a * x - b}.', 'answer': f'x = {x}', 'key': f'Add {b}: {a}x = {a * x}; divide by {a}.',
            'distractors': [f'x = {num((a * x - b - b) / a, 2)}', f'x = {x + 1}', f'x = {a * x}']}


def c13s3_both(r):
    a, c = r.randint(3, 9), r.randint(1, 2)
    x = r.randint(1, 12)
    b, d = r.randint(1, 15), None
    d = a * x + b - c * x
    return {'stem': f'Solve {a}x + {b} = {c}x + {d}.', 'answer': f'x = {x}', 'key': f'{a - c}x = {d - b} → x = {x}.'}


def c13s3_fraction(r):
    x = r.randint(2, 12) * 6
    return {'stem': f'Solve x/2 + x/3 = {x // 2 + x // 3}.', 'answer': f'x = {x}', 'key': f'Multiply by 6: 3x + 2x = {6 * (x // 2 + x // 3)} → 5x = {5 * x}.'}


def c13s3_age(r):
    who, other = two_names(r)
    k, y = r.randint(3, 5), r.randint(5, 15)
    son = r.randint(6, 14)
    father = k * son
    later = father + y
    return {'stem': f'{who}\'s father is {k} times as old as {who}. In {y} years, the sum of their ages will be {son + father + 2 * y}. Find their present ages.',
            'answer': f'{who} {son}, father {father}', 'key': f'x + {k}x + {2 * y} = {son + father + 2 * y} → {k + 1}x = {son + father} → x = {son}.'}


def c13s3_consecutive(r):
    n = r.randint(10, 60)
    kind = r.choice(['consecutive', 'consecutive even', 'consecutive odd'])
    step = 1 if kind == 'consecutive' else 2
    if kind == 'consecutive even' and n % 2:
        n += 1
    if kind == 'consecutive odd' and n % 2 == 0:
        n += 1
    tot = 3 * n + 3 * step
    return {'stem': f'The sum of three {kind} numbers is {tot}. Find the numbers.', 'answer': f'{n}, {n + step}, {n + 2 * step}', 'key': f'x + (x + {step}) + (x + {2 * step}) = {tot}.'}


def c13s3_coins(r):
    a, b = r.randint(5, 20), r.randint(5, 20)
    who = name(r)
    return {'stem': f'{who} has {a + b} coins, all ₹5 and ₹2, worth ₹{5 * a + 2 * b} in total. How many of each coin are there?', 'answer': f'{a} ₹5 coins, {b} ₹2 coins',
            'key': f'Let x be ₹5 coins: 5x + 2({a + b} − x) = {5 * a + 2 * b} → 3x = {3 * a}.'}


def c13s3_explain(r):
    return {'stem': 'Explain why the same number can be added to or subtracted from both sides of an equation without changing its solution.', 'answer': 'An equation is a balance; doing the same thing to both sides keeps it balanced.',
            'key': 'Balance idea.'}


def c13s3_ar(r):
    return ar('The solution of 3x + 5 = 20 is x = 5.', '3 × 5 + 5 = 20.', 'a', 'Substitution confirms the solution.')


def c13s3_perimeter(r):
    w = r.randint(4, 20)
    k = r.randint(2, 8)
    return {'stem': f'The length of a rectangle is {k} m more than its breadth. Its perimeter is {2 * (2 * w + k)} m. Find its length and breadth.', 'answer': f'{w + k} m and {w} m',
            'key': f'2(x + x + {k}) = {2 * (2 * w + k)} → x = {w}.'}


def c13s3_case(r):
    t = r.choice([300, 400, 500])
    s = r.choice([20, 25, 30])
    return {'stem': (f'A school trip costs {inr(t * 20)} for the bus plus {inr(s * 10)} per student for entry. The class collected {inr(t * 20 + s * 10 * 34)}. '
                     f'(i) Write an equation for the number of students n. (ii) Solve it. (iii) If 4 students drop out, how much should each remaining student pay so the bus is still covered?'),
            'answer': f'(i) {t * 20} + {s * 10}n = {t * 20 + s * 10 * 34} (ii) n = 34 (iii) {inr(round(s * 10 + t * 20 / 30, 2))}',
            'key': f'(iii) bus cost {t * 20} shared by 30 plus entry {s * 10} each.'}


# ---------------- ch14 Area ----------------
# st1 Area of quadrilaterals, trapezium and polygons

def c14s1_formula(r):
    return mcq('The area of a trapezium with parallel sides a and b and height h is …', '½ × (a + b) × h', ['(a + b) × h', '½ × a × b × h', 'a × b × h'], 'Average of parallel sides × height.', r)


def c14s1_trap(r):
    a, b, h = r.randint(6, 20), r.randint(4, 15), r.randint(3, 12)
    return {'stem': f'Find the area of a trapezium whose parallel sides are {a} cm and {b} cm and whose height is {h} cm.', 'answer': f'{num((a + b) * h / 2)} cm²',
            'key': f'½ × ({a} + {b}) × {h}.', 'distractors': [f'{(a + b) * h} cm²', f'{num(a * b * h / 2)} cm²', f'{num((a + b) / 2 + h)} cm²']}


def c14s1_rhombus(r):
    d1, d2 = r.randint(6, 24), r.randint(6, 24)
    return {'stem': f'Find the area of a rhombus whose diagonals are {d1} cm and {d2} cm.', 'answer': f'{num(d1 * d2 / 2)} cm²', 'key': f'½ × d₁ × d₂ = ½ × {d1} × {d2}.',
            'distractors': [f'{d1 * d2} cm²', f'{2 * (d1 + d2)} cm²', f'{num(d1 * d2 / 4)} cm²']}


def c14s1_find_h(r):
    a, b, h = r.randint(6, 20), r.randint(4, 15), r.randint(3, 12)
    return {'stem': f'The area of a trapezium is {num((a + b) * h / 2)} cm² and its parallel sides are {a} cm and {b} cm. Find its height.', 'answer': f'{h} cm', 'key': f'h = 2 × area ÷ ({a} + {b}).'}


def c14s1_explain(r):
    return {'stem': 'Explain how the area formula of a trapezium can be found by joining two identical trapeziums.', 'answer': 'Two copies form a parallelogram of base (a + b) and height h; one trapezium is half of it.',
            'key': 'Parallelogram argument.'}


def c14s1_quad(r):
    d, h1, h2 = r.randint(8, 20), r.randint(3, 9), r.randint(3, 9)
    return {'stem': f'A quadrilateral field has a diagonal of {d} m. The perpendiculars from the other two corners to this diagonal are {h1} m and {h2} m. Find the area.', 'answer': f'{num(d * (h1 + h2) / 2)} m²',
            'key': f'½ × {d} × ({h1} + {h2}).'}


def c14s1_ar(r):
    return ar('A rhombus with diagonals 10 cm and 8 cm has area 40 cm².', 'The diagonals of a rhombus divide it into four congruent right triangles.', 'a', '4 × ½ × 5 × 4 = 40; R explains the ½d₁d₂ formula.')


def c14s1_hex(r):
    s = r.randint(4, 10)
    h = r.randint(3, 8)
    return {'stem': f'A regular hexagon of side {s} cm is split into a rectangle and two isosceles triangles. The rectangle is {s} cm by {2 * h} cm and each triangle has base {2 * h} cm and height {num(round(math.sqrt(s * s - h * h), 2))} cm. Find the area.',
            'answer': f'{num(round(s * 2 * h + 2 * 0.5 * 2 * h * math.sqrt(s * s - h * h), 2))} cm²' if s > h else 'n/a', 'key': 'Rectangle + 2 triangles.'}


def c14s1_case(r):
    a, b, h = r.randint(20, 40), r.randint(10, 25), r.randint(10, 20)
    rate = r.choice([8, 10, 12, 15])
    return {'stem': (f'A trapezium-shaped garden has parallel sides {a} m and {b} m, {h} m apart. '
                     f'(i) Find its area. (ii) Grass costs {inr(rate)} per m². Find the cost. (iii) If the shorter parallel side is increased by 6 m, by how much does the cost go up?'),
            'answer': f'(i) {num((a + b) * h / 2)} m² (ii) {inr((a + b) * h / 2 * rate)} (iii) {inr(3 * h * rate)}', 'key': f'(iii) extra area ½ × 6 × {h} = {3 * h} m².'}


# st2 Circle: circumference and area

def c14s2_formula(r):
    return mcq('The circumference of a circle of radius r is …', '2πr', ['πr²', 'πr', '2πr²'], 'C = 2πr = πd.', r)


def c14s2_circ(r):
    rad = r.choice([7, 14, 21, 3.5, 10.5, 28, 35])
    return {'stem': f'Find the circumference of a circle of radius {num(rad)} cm (use π = 22/7).', 'answer': f'{num(2 * 22 / 7 * rad)} cm', 'key': f'2 × 22/7 × {num(rad)}.',
            'distractors': [f'{num(22 / 7 * rad)} cm', f'{num(22 / 7 * rad * rad)} cm', f'{num(2 * rad * 3)} cm']}


def c14s2_area(r):
    rad = r.choice([7, 14, 21, 3.5, 28, 35])
    return {'stem': f'Find the area of a circle of radius {num(rad)} cm (use π = 22/7).', 'answer': f'{num(22 / 7 * rad * rad)} cm²', 'key': f'22/7 × {num(rad)}².',
            'distractors': [f'{num(2 * 22 / 7 * rad)} cm²', f'{num(22 / 7 * rad * 2)} cm²', f'{num(22 / 7 * rad * rad * 2)} cm²']}


def c14s2_reverse(r):
    rad = r.choice([7, 14, 21, 35, 42])
    return {'stem': f'The circumference of a circular park is {num(2 * 22 / 7 * rad)} m. Find its area (π = 22/7).', 'answer': f'{num(22 / 7 * rad * rad)} m²', 'key': f'r = C ÷ 2π = {rad}; area = πr².'}


def c14s2_wheel(r):
    d = r.choice([56, 70, 63, 84])
    km = r.choice([0.88, 1.32, 2.2, 1.76])
    rev = km * 100000 / (22 / 7 * d)
    return {'stem': f'A cycle wheel has a diameter of {d} cm. How many complete revolutions does it make in {num(km)} km? (π = 22/7)', 'answer': f'{num(round(rev, 2))}',
            'key': f'Circumference {num(22 / 7 * d)} cm; {num(km * 100000)} ÷ {num(22 / 7 * d)}.'}


def c14s2_explain(r):
    return {'stem': 'Explain how cutting a circle into many thin sectors and rearranging them shows that its area is πr².', 'answer': 'The sectors form a near-rectangle of length πr (half the circumference) and height r.',
            'key': 'Rearrangement argument.'}


def c14s2_double(r):
    return {'stem': 'If the radius of a circle is doubled, what happens to (i) its circumference, (ii) its area? Explain.', 'answer': '(i) doubles (ii) becomes 4 times',
            'key': 'C ∝ r; A ∝ r².', 'distractors': ['(i) doubles (ii) doubles', '(i) 4 times (ii) 4 times', '(i) doubles (ii) 8 times']}


def c14s2_ar(r):
    return ar('If the radius of a circle is doubled, its area becomes four times.', 'Area of a circle is proportional to the square of its radius.', 'a', '(2r)² = 4r².')


def c14s2_ring(r):
    R, rr = r.choice([(14, 7), (21, 14), (35, 28), (10.5, 7)])
    return {'stem': f'A circular path runs around a circular pond. The outer radius is {num(R)} m and the pond\'s radius is {num(rr)} m. Find the area of the path (π = 22/7).',
            'answer': f'{num(22 / 7 * (R * R - rr * rr))} m²', 'key': 'π(R² − r²).'}


# st3 Composite figures

def c14s3_first(r):
    return mcq('To find the area of an L-shaped figure, the first step is usually to …', 'split it into rectangles', ['multiply all the sides', 'find its perimeter', 'draw its diagonal'],
               'Split into simple shapes (or subtract).', r)


def c14s3_L(r):
    a, b = r.randint(8, 16), r.randint(6, 12)
    c, d = r.randint(2, a - 3), r.randint(2, b - 3)
    return {'stem': f'An L-shaped room is a {a} m × {b} m rectangle with a {c} m × {d} m rectangle cut out of one corner. Find the area of the room.', 'answer': f'{a * b - c * d} m²',
            'key': f'{a * b} − {c * d}.', 'distractors': [f'{a * b + c * d} m²', f'{2 * (a + b)} m²', f'{a * b} m²']}


def c14s3_semicircle(r):
    l, w = r.choice([(14, 7), (20, 14), (21, 14), (28, 14)])
    return {'stem': f'A window is a rectangle {l} dm wide and {w} dm high with a semicircle on top (diameter = width). Find its area (π = 22/7).', 'answer': f'{num(l * w + 22 / 7 * (l / 2) ** 2 / 2)} dm²',
            'key': f'{l * w} + ½ × 22/7 × {num(l / 2)}².'}


def c14s3_shaded(r):
    a = r.choice([14, 28, 21, 7])
    return {'stem': f'A circle is drawn inside a square of side {a} cm, touching all four sides. Find the area of the region inside the square but outside the circle (π = 22/7).', 'answer': f'{num(a * a - 22 / 7 * (a / 2) ** 2)} cm²',
            'key': f'{a}² − 22/7 × {num(a / 2)}².'}


def c14s3_path(r):
    l, b, w = r.randint(20, 40), r.randint(12, 25), r.choice([1, 1.5, 2, 2.5])
    return {'stem': f'A rectangular park {l} m × {b} m has a path {num(w)} m wide inside it along all four edges. Find the area of the path.', 'answer': f'{num(l * b - (l - 2 * w) * (b - 2 * w))} m²',
            'key': f'{l * b} − {num(l - 2 * w)} × {num(b - 2 * w)}.'}


def c14s3_explain(r):
    return {'stem': 'Explain two different ways to find the area of an L-shaped figure and why both give the same answer.', 'answer': 'Split into two rectangles and add, or subtract the missing rectangle from the big one.',
            'key': 'Both methods partition the same region.'}


def c14s3_ar(r):
    return ar('The area of a composite figure can be found by adding the areas of non-overlapping parts.', 'Area is additive for regions that do not overlap.', 'a', 'R explains A.')


def c14s3_cross(r):
    l, w = r.randint(20, 50), r.randint(10, 30)
    p = r.choice([2, 3, 4])
    rate = r.choice([20, 25, 40])
    return {'stem': f'Two roads, each {p} m wide, cross each other at the centre of a {l} m × {w} m rectangular field, parallel to its sides. Find the area of the roads and the cost of paving them at {inr(rate)} per m².',
            'answer': f'{l * p + w * p - p * p} m²; {inr((l * p + w * p - p * p) * rate)}', 'key': 'Do not count the central square twice.'}


def c14s3_case(r):
    s = r.choice([14, 28])
    return {'stem': (f'A logo is made from a square of side {s} cm with a quarter circle of radius {s} cm drawn inside it, centred at one corner. '
                     f'(i) Find the area of the quarter circle. (ii) Find the area of the square outside the quarter circle. (iii) Find the perimeter of the region in (ii). (π = 22/7)'),
            'answer': f'(i) {num(22 / 7 * s * s / 4)} cm² (ii) {num(s * s - 22 / 7 * s * s / 4)} cm² (iii) {num(2 * s + 22 / 7 * s / 2)} cm',
            'key': f'(iii) two sides {s} + {s} and the arc ¼ × 2π × {s}.'}


# st4 Surface area and volume of cube, cuboid, cylinder

def c14s4_tsa_cube(r):
    return mcq('The total surface area of a cube of edge a is …', '6a²', ['a³', '4a²', '12a'], 'Six square faces.', r)


def c14s4_cuboid_vol(r):
    l, b, h = r.randint(5, 20), r.randint(3, 12), r.randint(2, 10)
    return {'stem': f'Find the volume of a cuboid {l} cm × {b} cm × {h} cm.', 'answer': f'{l * b * h} cm³', 'key': 'l × b × h.',
            'distractors': [f'{2 * (l * b + b * h + h * l)} cm³', f'{l + b + h} cm³', f'{l * b} cm³']}


def c14s4_cuboid_tsa(r):
    l, b, h = r.randint(5, 20), r.randint(3, 12), r.randint(2, 10)
    return {'stem': f'Find the total surface area of a box {l} cm × {b} cm × {h} cm.', 'answer': f'{2 * (l * b + b * h + h * l)} cm²', 'key': '2(lb + bh + hl).'}


def c14s4_cyl(r):
    rad, h = r.choice([7, 14, 3.5, 21]), r.randint(5, 20)
    return {'stem': f'Find the volume of a cylindrical water tank of radius {num(rad)} m and height {h} m (π = 22/7). How many litres does it hold? (1 m³ = 1000 L)',
            'answer': f'{num(22 / 7 * rad * rad * h)} m³; {num(22 / 7 * rad * rad * h * 1000)} L', 'key': 'πr²h.'}


def c14s4_csa(r):
    rad, h = r.choice([7, 14, 3.5, 10.5]), r.randint(5, 30)
    return {'stem': f'A label covers the curved surface of a tin of radius {num(rad)} cm and height {h} cm. Find the area of the label (π = 22/7).', 'answer': f'{num(2 * 22 / 7 * rad * h)} cm²', 'key': '2πrh.'}


def c14s4_explain(r):
    return {'stem': 'Explain why the curved surface area of a cylinder is 2πrh by unrolling it.', 'answer': 'Unrolled, it is a rectangle of length 2πr (the circumference) and width h.', 'key': 'Net argument.'}


def c14s4_scale(r):
    k = r.choice([2, 3])
    return {'stem': f'If every edge of a cube is multiplied by {k}, by what factor do its surface area and volume change?', 'answer': f'Surface area × {k * k}, volume × {k ** 3}',
            'key': 'Area scales as k², volume as k³.', 'distractors': [f'Surface area × {k}, volume × {k}', f'Surface area × {k * k}, volume × {k * k}', f'Surface area × {k ** 3}, volume × {k * k}']}


def c14s4_ar(r):
    return ar('Two cuboids with the same volume always have the same surface area.', 'Volume of a cuboid = l × b × h.', 'd', 'A is false (e.g. 1×1×8 and 2×2×2); R is true.')


def c14s4_bricks(r):
    l, w, h = r.choice([(10, 0.25, 2), (8, 0.3, 2.5), (12, 0.2, 1.5)])
    bl, bw, bh = 25, 12.5, 7.5
    n = l * 100 * w * 100 * h * 100 / (bl * bw * bh)
    return {'stem': f'How many bricks of size {bl} cm × {bw} cm × {bh} cm are needed to build a wall {l} m long, {num(w)} m thick and {num(h)} m high (ignore mortar)?', 'answer': f'{num(round(n, 1))}',
            'key': 'Wall volume ÷ brick volume in the same units.'}


def c14s4_case(r):
    l, b, h = r.choice([(2, 1.5, 1), (3, 2, 1.5), (2.5, 2, 1.2)])
    return {'stem': (f'An open rectangular water tank (no lid) is {num(l)} m long, {num(b)} m wide and {num(h)} m deep. '
                     f'(i) How many litres does it hold? (ii) Find the area to be painted inside (four walls and floor). (iii) If a tap fills 50 litres per minute, how long does it take to fill?'),
            'answer': f'(i) {num(l * b * h * 1000)} L (ii) {num(l * b + 2 * h * (l + b))} m² (iii) {num(l * b * h * 1000 / 50)} min', 'key': '(ii) no top face.'}


FAMILIES = {
    S + '10-st1': [F('C1', 'D2', 'short', c10s1_to_pct), F('C1', 'D1', 'short', c10s1_of), F('C2', 'D2', 'explain', c10s1_by_to), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s1_change), F('C3', 'D3', 'numerical', c10s1_reverse), F('C3', 'D1', 'numerical', c10s1_marks),
                   F('C4', 'D4', 'multi_step', c10s1_successive), F('C4', 'D3', 'case', c10s1_case)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_formula), F('C2', 'D2', 'explain', c10s2_explain), F('C2', 'D2', 'mcq', c10s2_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c10s2_profit),
                   F('C3', 'D2', 'numerical', c10s2_sp), F('C3', 'D2', 'numerical', c10s2_discount), F('C3', 'D3', 'numerical', c10s2_gst), F('C3', 'D4', 'multi_step', c10s2_discount_then_gst),
                   F('C4', 'D3', 'multi_step', c10s2_cp_from_sp), F('C4', 'D5', 'multi_step', c10s2_two_items), F('C4', 'D4', 'case', c10s2_case)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_si_formula), F('C2', 'D2', 'explain', c10s3_explain), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c10s3_si),
                   F('C3', 'D2', 'numerical', c10s3_find_rate), F('C3', 'D3', 'numerical', c10s3_ci), F('C3', 'D4', 'multi_step', c10s3_depreciation), F('C4', 'D3', 'numerical', c10s3_diff),
                   F('C4', 'D4', 'multi_step', c10s3_half), F('C3', 'D3', 'numerical', c10s3_population), F('C4', 'D5', 'case', c10s3_case)],
    S + '11-st1': [F('C1', 'D2', 'short', c11s1_lines), F('C1', 'D1', 'short', c11s1_order), F('C2', 'D2', 'explain', c11s1_explain), F('C2', 'D2', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c11s1_angle), F('C3', 'D3', 'short', c11s1_letters), F('C4', 'D3', 'explain', c11s1_rangoli)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_tools), F('C1', 'D1', 'short', c11s2_triangle), F('C2', 'D2', 'explain', c11s2_hexagon), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'long', c11s2_bisector), F('C3', 'D3', 'explain', c11s2_angle), F('C4', 'D4', 'short', c11s2_pattern)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_def), F('C2', 'D2', 'explain', c11s3_explain), F('C2', 'D2', 'mcq', c11s3_ar, kinds=('ar',)), F('C3', 'D2', 'short', c11s3_regular),
                   F('C3', 'D3', 'numerical', c11s3_vertex), F('C3', 'D1', 'numerical', c11s3_floor), F('C4', 'D3', 'numerical', c11s3_vertex)],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_origin), F('C1', 'D1', 'short', c12s1_quadrant), F('C2', 'D2', 'explain', c12s1_axis), F('C2', 'D2', 'mcq', c12s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c12s1_rect), F('C3', 'D3', 'short', c12s1_mirror), F('C4', 'D3', 'multi_step', c12s1_map, gap='G7')],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_flat), F('C1', 'D1', 'short', c12s2_choose), F('C2', 'D2', 'explain', c12s2_speed), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c12s2_read), F('C3', 'D4', 'multi_step', c12s2_trip, gap='G7'), F('C4', 'D3', 'case', c12s2_case)],
    S + '12-st3': [F('C1', 'D2', 'short', c12s3_value), F('C1', 'D1', 'short', c12s3_check), F('C2', 'D2', 'explain', c12s3_through_origin), F('C2', 'D2', 'mcq', c12s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c12s3_rule), F('C3', 'D3', 'multi_step', c12s3_taxi, gap='G7'), F('C4', 'D4', 'case', c12s3_case)],
    S + '13-st1': [F('C1', 'D2', 'mcq', c13s1_complete), F('C2', 'D2', 'explain', c13s1_explain), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c13s1_expand),
                   F('C3', 'D2', 'numerical', c13s1_mental), F('C3', 'D3', 'numerical', c13s1_diff_sq), F('C3', 'D2', 'numerical', c13s1_product), F('C4', 'D4', 'multi_step', c13s1_value),
                   F('C4', 'D3', 'case', c13s1_case)],
    S + '13-st2': [F('C1', 'D2', 'short', c13s2_hcf), F('C1', 'D1', 'short', c13s2_common), F('C2', 'D2', 'explain', c13s2_explain), F('C2', 'D2', 'mcq', c13s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s2_identity), F('C3', 'D3', 'numerical', c13s2_trinomial), F('C3', 'D4', 'numerical', c13s2_group), F('C4', 'D3', 'multi_step', c13s2_area),
                   F('C4', 'D4', 'explain', c13s2_numbers)],
    S + '13-st3': [F('C1', 'D1', 'short', c13s3_simple), F('C1', 'D2', 'short', c13s3_two_step), F('C2', 'D2', 'explain', c13s3_explain), F('C2', 'D2', 'mcq', c13s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s3_both), F('C3', 'D3', 'numerical', c13s3_fraction), F('C3', 'D3', 'multi_step', c13s3_perimeter, gap='G7'),
                   F('C3', 'D4', 'multi_step', c13s3_age, gap='G7'), F('C4', 'D3', 'multi_step', c13s3_consecutive, gap='G7'), F('C4', 'D4', 'multi_step', c13s3_coins, gap='G7'),
                   F('C4', 'D5', 'case', c13s3_case, gap='G7')],
    S + '14-st1': [F('C1', 'D2', 'mcq', c14s1_formula), F('C2', 'D2', 'explain', c14s1_explain), F('C2', 'D2', 'mcq', c14s1_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c14s1_trap),
                   F('C3', 'D2', 'numerical', c14s1_rhombus), F('C3', 'D3', 'numerical', c14s1_find_h), F('C3', 'D3', 'numerical', c14s1_quad), F('C4', 'D4', 'case', c14s1_case)],
    S + '14-st2': [F('C1', 'D2', 'mcq', c14s2_formula), F('C2', 'D2', 'explain', c14s2_explain), F('C2', 'D3', 'short', c14s2_double), F('C2', 'D2', 'mcq', c14s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'numerical', c14s2_circ), F('C3', 'D2', 'numerical', c14s2_area), F('C3', 'D3', 'numerical', c14s2_reverse), F('C3', 'D4', 'multi_step', c14s2_wheel),
                   F('C4', 'D3', 'numerical', c14s2_ring)],
    S + '14-st3': [F('C1', 'D2', 'mcq', c14s3_first), F('C2', 'D2', 'explain', c14s3_explain), F('C2', 'D2', 'mcq', c14s3_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c14s3_L),
                   F('C3', 'D2', 'numerical', c14s3_semicircle), F('C3', 'D3', 'numerical', c14s3_shaded), F('C3', 'D4', 'multi_step', c14s3_path), F('C4', 'D4', 'multi_step', c14s3_cross),
                   F('C4', 'D5', 'case', c14s3_case), F('C4', 'D3', 'numerical', c14s3_shaded)],
    S + '14-st4': [F('C1', 'D2', 'mcq', c14s4_tsa_cube), F('C2', 'D2', 'explain', c14s4_explain), F('C2', 'D3', 'short', c14s4_scale), F('C2', 'D3', 'mcq', c14s4_ar, kinds=('ar',)),
                   F('C3', 'D1', 'numerical', c14s4_cuboid_vol), F('C3', 'D2', 'numerical', c14s4_cuboid_tsa), F('C3', 'D3', 'numerical', c14s4_csa), F('C3', 'D4', 'multi_step', c14s4_cyl),
                   F('C4', 'D4', 'multi_step', c14s4_bricks), F('C4', 'D4', 'case', c14s4_case)],
}
