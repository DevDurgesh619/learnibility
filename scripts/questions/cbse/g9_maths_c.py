"""CBSE class 9 maths (Ganita Manjari) families, chapters 11-14."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, frac, name, two_names, inr, num_distractors
from g9_maths_h import nz, Q, mcqbank, arbank, xbank, P, fn, rad, is_sq, poly, lin, term, triple, signed, bracket, PI, pistr, ordinal, eq2

S = 'cbse-g9-maths-ch'


# ---------------- ch11 Algorithms ----------------

def collatz_steps(n):
    k = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        k += 1
    return k


def c11s1_mcq(r):
    return mcqbank([
        ('An algorithm is …', 'a finite sequence of clear steps that solves a problem', ['any guess that gives an answer', 'a single formula', 'a type of graph'], 'Definition.'),
        ('In a flowchart, a decision (yes/no question) is shown by …', 'a diamond', ['a rectangle', 'an oval', 'an arrow'], 'Standard flowchart symbol.'),
        ('In a flowchart, the start and end are shown by …', 'an oval (terminal)', ['a diamond', 'a parallelogram', 'a rectangle'], 'Terminal symbol.'),
        ('Which of these is NOT a property of a good algorithm?', 'It may go on forever without stopping', ['Each step is clear', 'It finishes after a finite number of steps', 'It gives the correct output'], 'An algorithm must terminate.'),
    ])(r)


def c11s1_trace(r):
    a, b = r.randint(2, 9), r.randint(2, 6)
    n = r.randint(3, 5)
    x = a
    for _ in range(n):
        x = x * 2 - b
    return Q(f'Follow the algorithm: Step 1: let x = {a}. Step 2: replace x by 2x − {b}. Step 3: repeat Step 2 until it has been done {n} times in all. Step 4: output x. What is the output?', fn(x),
             f'Apply 2x − {b} {n} times starting from {a}.', num_distractors(x, x + b, 2 * x, a * 2 ** n))


def c11s1_collatz(r):
    n = r.choice([6, 7, 9, 10, 12, 3, 5, 11, 13, 17])
    k = collatz_steps(n)
    return Q(f'Algorithm: if n is even, replace n by n/2; if n is odd, replace n by 3n + 1; stop when n = 1. Starting with n = {n}, how many replacements are made before stopping?', str(k),
             f'Trace the sequence from {n} to 1: {k} steps.', num_distractors(k, k + 1, k - 1, n))


def c11s1_digitsum(r):
    n = r.randint(10000, 999999)
    s = n
    steps = []
    while s >= 10:
        s = sum(map(int, str(s)))
        steps.append(s)
    return Q(f'Algorithm: add the digits of the number; if the result has more than one digit, repeat. What is the final single digit for {n}?', str(s),
             ' → '.join([str(n)] + list(map(str, steps))) + f'; the result equals the remainder of {n} on division by 9 (9 if divisible).', num_distractors(s, (s % 9) + 1, steps[0] if steps else s + 2, 9 - s if s != 9 else 1))


def c11s1_explain(r):
    return xbank([
        ('Write an algorithm (numbered steps) to find the larger of two numbers a and b, and explain where a decision is needed.', '1. Read a, b. 2. If a > b, output a; else output b. 3. Stop.', 'Steps (1), decision step identified (1).'),
        ('Explain why "keep dividing by 2 until you get 0" is not a good algorithm for positive numbers.', 'Dividing a positive number by 2 never gives 0 exactly, so the steps never end.', '2 marks.'),
        ('Explain why column addition is an algorithm.', 'It is a fixed finite sequence of clear steps (add units, carry, add tens, …) that always gives the sum.', '2 marks.'),
    ])(r)


def c11s1_ar(r):
    return arbank([
        ('Long division is an algorithm.', 'It is a finite sequence of well-defined steps that always produces the quotient and remainder.', 'a', 'R explains A.'),
        ('A recipe can be thought of as an algorithm.', 'A recipe is a sequence of steps that produces a result.', 'a', 'R explains A.'),
        ('An algorithm can have a step "choose any number you like".', 'Every step of an algorithm must be clear and unambiguous.', 'd', 'A vague step is not allowed; A false, R true.'),
    ])(r)


def c11s1_case(r):
    p = r.choice([100, 150, 200, 250])
    d = r.choice([10, 20])
    t = r.choice([500, 1000, 1500])
    return Q((f'A shop billing flowchart: Start → read price P → if P ≥ ₹{t}, give {d}% discount, else no discount → add 5% GST on the amount after discount → output bill → End. '
              f'(i) Name the shape used for "if P ≥ ₹{t}". (ii) Find the bill for P = ₹{p * 2}. (iii) Find the bill for P = ₹{t + p * 2}. (iv) Write the steps as a numbered algorithm.'),
             f'(i) diamond (ii) {inr(p * 2 * 1.05) if p * 2 < t else inr(p * 2 * (1 - d / 100) * 1.05)} (iii) {inr((t + p * 2) * (1 - d / 100) * 1.05)} (iv) 1. Read P 2. If P ≥ {t}, P = P − {d}% of P 3. Bill = 1.05P 4. Output bill',
             '1 mark each part.')


# st2 Euclid's algorithm

def euclid_steps(a, b):
    st = []
    while b:
        q, rr = divmod(a, b)
        st.append((a, b, q, rr))
        a, b = b, rr
    return a, st


def euclid_pair(r):
    g = r.randint(2, 30)
    while True:
        x, y = r.randint(5, 60), r.randint(5, 60)
        if math.gcd(x, y) == 1 and x != y:
            return max(x, y) * g, min(x, y) * g, g


def c11s2_hcf(r):
    a, b, g = euclid_pair(r)
    _, st = euclid_steps(a, b)
    steps = '; '.join(f'{x} = {y} × {q} + {rr}' for x, y, q, rr in st)
    return Q(f"Use Euclid's division algorithm to find the HCF of {a} and {b}.", str(g), f'{steps}; last non-zero remainder (divisor) = {g}.',
             num_distractors(g, g * 2, a - b, g // 2 if g > 2 else g + 3))


def c11s2_mcq(r):
    return mcqbank([
        ("Euclid's division lemma states that for positive integers a and b there exist unique q and r with …", 'a = bq + r, 0 ≤ r < b', ['a = bq + r, 0 < r ≤ b', 'a = bq − r, r < q', 'b = aq + r, 0 ≤ r < a'], 'Division with remainder.'),
        ("In Euclid's algorithm, the HCF is …", 'the last non-zero remainder (the divisor at the final step)', ['the first quotient', 'the last quotient', 'the product of the remainders'], 'The algorithm stops at remainder 0.'),
        ("Euclid's algorithm works because HCF(a, b) equals …", 'HCF(b, r), where r is the remainder of a ÷ b', ['HCF(a, r)', 'a − b', 'LCM(b, r)'], 'Common divisors of a and b are the same as those of b and r.'),
        ('HCF × LCM of two numbers equals …', 'the product of the two numbers', ['their sum', 'their difference', 'the square of the HCF'], 'For two positive integers.'),
    ])(r)


def c11s2_count(r):
    a, b, g = euclid_pair(r)
    _, st = euclid_steps(a, b)
    return Q(f"How many division steps does Euclid's algorithm take to find HCF({a}, {b})?", str(len(st)), '; '.join(f'{x} = {y} × {q} + {rr}' for x, y, q, rr in st) + '.',
             num_distractors(len(st), len(st) + 1, len(st) - 1 if len(st) > 1 else 4, len(st) + 2))


def c11s2_lcm(r):
    a, b, g = euclid_pair(r)
    l = a * b // g
    return Q(f'The HCF of {a} and {b} is {g}. Find their LCM.', str(l), f'LCM = ({a} × {b}) ÷ {g} = {l}.', num_distractors(l, a * b, l // 2, a + b))


def c11s2_explain(r):
    a, b, g = euclid_pair(r)
    q, rr = divmod(a, b)
    return Q(f'Explain why any number that divides both {a} and {b} must also divide {rr}, the remainder when {a} is divided by {b}.', f'{rr} = {a} − {q} × {b}',
             'If d divides a and b, it divides a − qb = r (2 marks).')


def c11s2_ar(r):
    a, b, g = euclid_pair(r)
    return arbank([
        (f'HCF({a}, {b}) = {g}.', "Euclid's algorithm repeatedly replaces (a, b) by (b, r) until the remainder is 0.", 'a', 'R is the method that gives A.'),
        ('HCF(a, b) × LCM(a, b) = a × b for any two positive integers.', 'Every common multiple of a and b is a multiple of their LCM.', 'b', 'Both true, but R does not explain the product rule.'),
        (f'The remainder when {a} is divided by {b} can be {b}.', 'In a = bq + r, 0 ≤ r < b.', 'd', 'r < b; A false, R true.'),
    ])(r)


def c11s2_case(r):
    a, b, g = euclid_pair(r)
    return Q((f'A school has {a} notebooks and {b} pencils to pack into identical kits, with no item left over and each kit having the same number of notebooks and the same number of pencils. '
              f"(i) Use Euclid's algorithm to find the greatest number of kits. (ii) How many notebooks and pencils are in each kit? (iii) How many division steps did the algorithm take?"),
             f'(i) {g} kits (ii) {a // g} notebooks and {b // g} pencils (iii) {len(euclid_steps(a, b)[1])}', 'HCF by Euclid (2), division (1), count (1).')


def c11s2_three(r):
    g = r.randint(2, 15)
    xs = r.sample(range(5, 40), 3)
    while math.gcd(math.gcd(xs[0], xs[1]), xs[2]) != 1:
        xs = r.sample(range(5, 40), 3)
    a, b, c = [x * g for x in xs]
    return Q(f"Find the HCF of {a}, {b} and {c} by applying Euclid's algorithm twice.", str(g), f'HCF({a}, {b}) = {math.gcd(a, b)}; HCF({math.gcd(a, b)}, {c}) = {g} (3 marks).')


# st3 searching and sorting

def c11s3_linear(r):
    lst = r.sample(range(10, 99), r.randint(8, 12))
    if r.random() < 0.7:
        t = r.choice(lst)
        k = lst.index(t) + 1
        ans = f'{k} comparisons'
    else:
        t = r.choice([x for x in range(10, 99) if x not in lst])
        k = len(lst)
        ans = f'{k} comparisons (not found)'
    return Q(f'Linear search is used to look for {t} in the list {", ".join(map(str, lst))}, starting from the left. How many comparisons are made?', ans,
             'Compare with each item in order until it is found or the list ends.', [f'{x} comparisons' for x in dict.fromkeys([k + 1, k - 1, len(lst) // 2, k + 2, 1]) if x != k and x > 0][:3])


def c11s3_binary(r):
    n = r.choice([7, 15, 31, 63, 100, 127, 1000, 1023])
    k = math.ceil(math.log2(n + 1))
    return Q(f'Binary search is used on a sorted list of {n} items. What is the greatest number of comparisons needed to find an item (or show it is absent)?', str(k),
             f'Each comparison halves the list; 2^{k} − 1 = {2 ** k - 1} ≥ {n}.', num_distractors(k, n // 2, k + 1, k - 1))


def c11s3_bubble(r):
    lst = r.sample(range(1, 30), 5)
    a = lst[:]
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
    return Q(f'Apply one pass of bubble sort (compare neighbours left to right, swap if the left one is larger) to {", ".join(map(str, lst))}. Write the list after the pass.', ', '.join(map(str, a)),
             'After one pass the largest number is at the end.', [', '.join(map(str, sorted(lst))), ', '.join(map(str, lst[::-1])), ', '.join(map(str, lst[1:] + lst[:1]))])


def c11s3_mcq(r):
    return mcqbank([
        ('Binary search can be used only when the list is …', 'sorted', ['short', 'made of even numbers', 'unsorted'], 'It compares with the middle and discards one half.'),
        ('After the first pass of bubble sort (ascending), the … element is in its correct place.', 'largest', ['smallest', 'middle', 'first'], 'It bubbles to the end.'),
        ('In the worst case, linear search on n items needs …', 'n comparisons', ['log₂ n comparisons', '1 comparison', 'n² comparisons'], 'It may check every item.'),
        ('Guessing a number from 1 to 100 by always guessing the middle of the remaining range is an example of …', 'binary search', ['linear search', 'bubble sort', 'selection sort'], 'Halving the range.'),
    ])(r)


def c11s3_guess(r):
    n = r.choice([100, 64, 50, 128, 200])
    t = r.randint(1, n)
    lo, hi, k, gs = 1, n, 0, []
    while True:
        k += 1
        m = (lo + hi) // 2
        gs.append(m)
        if m == t:
            break
        if m < t:
            lo = m + 1
        else:
            hi = m - 1
    return Q(f'{name(r)} thinks of a number from 1 to {n}. You always guess the middle of the remaining range (rounding down) and are told "higher" or "lower". If the number is {t}, list your guesses.', ', '.join(map(str, gs)),
             f'Halve the range each time: {", ".join(map(str, gs))} ({k} guesses).')


def c11s3_explain(r):
    return xbank([
        ('Explain why binary search is faster than linear search on a long sorted list.', 'Each comparison halves the remaining list, so about log₂ n steps are needed instead of up to n.', '2 marks.'),
        ('Explain why binary search does not work on an unsorted list.', 'Discarding half the list after comparing with the middle item is only valid if the list is in order.', '2 marks.'),
        ('Explain how you look up a word in a dictionary and which search method it resembles.', 'Open near the middle, decide which half the word is in, repeat — like binary search.', '2 marks.'),
    ])(r)


def c11s3_ar(r):
    return arbank([
        ('Binary search on 1,000 sorted items needs at most 10 comparisons.', '2¹⁰ = 1,024 is greater than 1,000.', 'a', 'R explains A.'),
        ('Bubble sort places the smallest number first after one pass.', 'Each pass of bubble sort moves the largest remaining number to its final place.', 'd', 'The largest goes to the end; A false, R true.'),
        ('Linear search works on any list.', 'Linear search checks the items one by one.', 'a', 'R explains A.'),
    ])(r)


def c11s3_case(r):
    lst = r.sample(range(10, 60), 6)
    s = sorted(lst)
    a = lst[:]
    first = None
    passes = 0
    while True:
        sw = False
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sw = True
        passes += 1
        if first is None:
            first = a[:]
        if not sw:
            break
    t = r.choice(s)
    return Q((f'A librarian wants to arrange 6 books by their accession numbers {", ".join(map(str, lst))}. (i) Write the list after the first pass of bubble sort. (ii) How many passes are needed until a pass makes no swaps? '
              f'(iii) In the sorted list, how many comparisons does binary search need to find {t}? (iv) Why sort first?'),
             f'(i) {", ".join(map(str, first))} (ii) {passes} (iii) at most 3 (iv) binary search needs a sorted list',
             '1 mark each part; (i) largest number moves to the end.')


# st4 efficiency

def c11s4_compare(r):
    n = r.choice([16, 32, 64, 128, 256, 1024])
    return Q(f'For a sorted list of {n} items, compare the worst-case number of comparisons for linear search and binary search.', f'Linear {n}, binary {int(math.log2(n)) + 1}',
             f'Linear: n = {n}. Binary: ⌊log₂ {n}⌋ + 1 = {int(math.log2(n)) + 1}.', [f'Linear {n}, binary {n // 2}', f'Linear {n // 2}, binary {int(math.log2(n))}', f'Linear {n * n}, binary {n}'])


def c11s4_bubble_count(r):
    n = r.randint(5, 30)
    return Q(f'In the simplest form of bubble sort on n items, there are n − 1 passes and pass k makes n − k comparisons. How many comparisons are made in total for {n} items?', str(n * (n - 1) // 2),
             f'(n − 1) + (n − 2) + … + 1 = n(n − 1)/2 = {n * (n - 1) // 2}.', num_distractors(n * (n - 1) // 2, n * n, n * (n - 1), n - 1))


def c11s4_mcq(r):
    return mcqbank([
        ('If the number of items doubles, the worst-case comparisons in binary search …', 'increase by about 1', ['double', 'stay the same', 'become four times'], 'One more halving step.'),
        ('If the number of items doubles, the worst-case comparisons in linear search …', 'double', ['increase by 1', 'stay the same', 'halve'], 'Proportional to n.'),
        ('An algorithm whose steps grow like n² is … than one whose steps grow like n for large n.', 'slower', ['faster', 'equally fast', 'always incorrect'], 'n² grows faster than n.'),
    ])(r)


def c11s4_explain(r):
    return xbank([
        ('Explain why counting steps is a better way to compare algorithms than timing them on one computer.', 'Step counts do not depend on the speed of a particular machine.', '2 marks.'),
        ('Explain why doubling the list size adds only one step to binary search.', 'One extra comparison halves the doubled list back to the original size.', '2 marks.'),
    ])(r)


def c11s4_ar(r):
    return arbank([
        ('Binary search is more efficient than linear search for large sorted lists.', 'The number of comparisons in binary search grows like log₂ n.', 'a', 'R explains A.'),
        ('Bubble sort on 10 items needs at most 45 comparisons (simple version).', 'n(n − 1)/2 = 45 for n = 10.', 'a', 'R explains A.'),
        ('For 4 items, binary search is always much faster than linear search.', 'Binary search needs at most 3 comparisons for 4 items.', 'd', 'For tiny lists the saving is negligible (4 vs 3); A false, R true.'),
    ])(r)


def c11s4_case(r):
    n = r.choice([1000, 10000, 100000, 1000000])
    t = r.choice([1, 2, 5])
    k = math.ceil(math.log2(n + 1))
    return Q((f'A school database stores {n:,} student records sorted by roll number. One comparison takes {t} microsecond{"s" if t > 1 else ""}. '.replace(',', ',') +
              f'(i) Find the worst-case number of comparisons for linear search. (ii) For binary search. (iii) Find the time taken by each in the worst case. (iv) If the records double, how do the two counts change?'),
             f'(i) {n:,} (ii) {k} (iii) {n * t:,} μs and {k * t} μs (iv) linear doubles to {2 * n:,}; binary increases by 1 to {k + 1}', '1 mark each part.')


# ---------------- ch12 Quadrilaterals ----------------

def c12s1_ratio(r):
    rs = r.choice([(1, 2, 3, 4), (2, 3, 3, 4), (3, 4, 5, 6), (1, 1, 2, 2), (2, 3, 4, 6), (3, 5, 9, 13), (4, 5, 6, 9)])
    k = Fr(360, sum(rs))
    angs = [fn(x * k) for x in rs]
    return Q(f'The angles of a quadrilateral are in the ratio {" : ".join(map(str, rs))}. Find all the angles.', ', '.join(a + '°' for a in angs),
             f'Sum = 360°; one part = 360/{sum(rs)} = {fn(k)}°.', [', '.join(fn(x * Fr(180, sum(rs))) + '°' for x in rs), ', '.join(fn(x * 10) + '°' for x in rs), ', '.join(fn(x * k + 5) + '°' for x in rs)])


def c12s1_fourth(r):
    a, b, c = r.randint(50, 130), r.randint(50, 130), r.randint(50, 120)
    d = 360 - a - b - c
    if not 20 < d < 180:
        raise ValueError
    return Q(f'Three angles of a quadrilateral are {a}°, {b}° and {c}°. Find the fourth angle.', f'{d}°', f'360° − ({a} + {b} + {c})° = {d}°.', [f'{d + 10}°', f'{abs(180 - a - b - c)}°' if abs(180 - a - b - c) != d else f'{d - 10}°', f'{360 - a - b}°'])


def c12s1_mcq(r):
    return mcqbank([
        ('A quadrilateral with exactly one pair of parallel sides is a …', 'trapezium', ['parallelogram', 'rhombus', 'kite'], 'Definition.'),
        ('A parallelogram with all sides equal is a …', 'rhombus', ['rectangle', 'trapezium', 'kite'], 'Definition.'),
        ('Which statement is true?', 'Every square is a rhombus.', ['Every rhombus is a square.', 'Every parallelogram is a rectangle.', 'Every trapezium is a parallelogram.'], 'A square has all sides equal.'),
        ('The sum of the angles of a quadrilateral is …', '360°', ['180°', '540°', '270°'], 'A diagonal splits it into two triangles.'),
        ('A quadrilateral with two pairs of equal adjacent sides is a …', 'kite', ['rhombus always', 'trapezium', 'rectangle'], 'Definition.'),
    ])(r)


def c12s1_explain(r):
    return xbank([
        ('Explain why the angles of a quadrilateral add up to 360°.', 'A diagonal divides it into two triangles, each with angle sum 180°.', '2 marks.'),
        ('Can a quadrilateral have angles 100°, 100°, 100° and 70°? Explain.', 'No.', 'They add to 370°, not 360° (2 marks).'),
        ('Explain why a square is a rectangle, a rhombus and a parallelogram.', 'It has all the properties of each: opposite sides parallel, all angles 90°, all sides equal.', '2 marks.'),
    ])(r)


def c12s1_ar(r):
    return arbank([
        ('A quadrilateral can have three obtuse angles.', 'The angles of a quadrilateral add up to 360°.', 'a', 'e.g. 100°, 100°, 100°, 60°; R allows this.'),
        ('A quadrilateral can have four obtuse angles.', 'The angles of a quadrilateral add up to 360°.', 'd', 'Four obtuse angles exceed 360°; A false, R true.'),
        ('Every rhombus is a kite.', 'A rhombus has two pairs of equal adjacent sides.', 'a', 'R explains A.'),
    ])(r)


def c12s1_expr(r):
    x = r.randint(10, 30)
    cs = [r.randint(-10, 30) for _ in range(3)]
    ms = [r.randint(1, 4) for _ in range(4)]
    c4 = 360 - sum(ms) * x - sum(cs)
    angs = [ms[i] * x + (cs + [c4])[i] for i in range(4)]
    if min(angs) < 20 or max(angs) >= 180:
        raise ValueError
    parts = [f'({term(ms[i], "x", first=True)} {signed((cs + [c4])[i])})°' for i in range(4)]
    return Q(f'The angles of a quadrilateral are {", ".join(parts)}. Find x and the largest angle.', f'x = {x}; largest angle {max(angs)}°',
             f'Sum = {sum(ms)}x {signed(sum(cs) + c4)} = 360 ⇒ x = {x} (3 marks).')


def c12s1_case(r):
    a, b = r.randint(60, 80), r.randint(100, 120)
    return Q((f'A kite (the toy) has the shape of a quadrilateral ABCD with AB = AD and CB = CD. ∠A = {a}° and ∠C = {b}°. '
              f'(i) Name the type of quadrilateral. (ii) Which two angles are equal? (iii) Find ∠B and ∠D. (iv) Is ABCD a parallelogram? Why?'),
             f'(i) kite (ii) ∠B = ∠D (iii) {num((360 - a - b) / 2)}° each (iv) no; its opposite sides are not parallel/equal',
             '1 mark each part.')


# st2 parallelogram properties

def c12s2_adj(r):
    a = r.randint(40, 140)
    if a == 90:
        a = 70
    return Q(f'One angle of a parallelogram is {a}°. Find the other three angles.', f'{180 - a}°, {a}°, {180 - a}°', 'Opposite angles are equal; adjacent angles are supplementary.',
             [f'{a}°, {a}°, {a}°', f'{360 - 3 * a if 360 - 3 * a > 0 else 90}°, {a}°, {a}°', f'{90 - a if a < 90 else a - 90}°, {a}°, {180 - a}°'])


def c12s2_mcq(r):
    return mcqbank([
        ('The diagonals of a parallelogram …', 'bisect each other', ['are always equal', 'are always perpendicular', 'bisect the angles'], 'Theorem.'),
        ('The diagonals of a rhombus …', 'bisect each other at right angles', ['are equal', 'do not bisect each other', 'are parallel'], 'Theorem.'),
        ('The diagonals of a rectangle are …', 'equal and bisect each other', ['perpendicular always', 'unequal', 'parallel'], 'Theorem.'),
        ('A diagonal of a parallelogram divides it into …', 'two congruent triangles', ['two similar but unequal triangles', 'four congruent triangles', 'a square and a triangle'], 'ASA congruence.'),
    ])(r)


def c12s2_expr(r):
    x = r.randint(10, 40)
    a, b = r.randint(2, 5), r.randint(1, 4)
    while a == b:
        b = r.randint(1, 4)
    c1 = r.randint(-10, 20)
    c2 = (a - b) * x + c1
    if not 20 < a * x + c1 < 160:
        raise ValueError
    return Q(f'In parallelogram ABCD, ∠A = ({a}x {signed(c1)})° and ∠C = ({term(b, "x", first=True)} {signed(c2)})°. Find x and ∠B.', f'x = {x}; ∠B = {180 - (a * x + c1)}°',
             f'Opposite angles equal: {a}x {signed(c1)} = {term(b, "x", first=True)} {signed(c2)} ⇒ x = {x}; ∠B = 180° − ∠A.')


def c12s2_diag(r):
    x = r.randint(2, 10)
    a, b = r.randint(2, 4), r.randint(1, 9)
    c = a + r.randint(1, 3)
    d = a * x + b - c * x
    if d <= -20:
        raise ValueError
    # OA = a x + b, OC = c x + d  -> equal
    return Q(f'The diagonals of parallelogram PQRS meet at O. If OP = ({a}y {signed(b)}) cm and OR = ({c}y {signed(d)}) cm, find y and the length of diagonal PR.', f'y = {x}; PR = {2 * (a * x + b)} cm',
             f'Diagonals bisect each other: {a}y {signed(b)} = {c}y {signed(d)} ⇒ y = {x}; PR = 2 × {a * x + b} (3 marks).')


def c12s2_explain(r):
    return xbank([
        ('Prove that the opposite sides of a parallelogram are equal.', 'Draw diagonal AC; △ABC ≅ △CDA (ASA: alternate angles, AC common) ⇒ AB = CD, BC = DA.', '3 marks.'),
        ('Prove that the diagonals of a parallelogram bisect each other.', 'With O the intersection, △AOB ≅ △COD (ASA: AB = CD, alternate angles) ⇒ OA = OC, OB = OD.', '3 marks.'),
        ('Explain why adjacent angles of a parallelogram are supplementary.', 'They are co-interior angles between parallel sides cut by a transversal side.', '2 marks.'),
    ])(r)


def c12s2_ar(r):
    a = r.randint(50, 130)
    return arbank([
        (f'If one angle of a parallelogram is {a}°, the adjacent angle is {180 - a}°.', 'Adjacent angles of a parallelogram are co-interior angles between parallel lines.', 'a', 'R explains A.'),
        ('The diagonals of every parallelogram are equal.', 'The diagonals of a parallelogram bisect each other.', 'd', 'Only for rectangles; A false, R true.'),
        ('A diagonal of a parallelogram divides it into two congruent triangles.', 'Opposite sides of a parallelogram are parallel.', 'a', 'Alternate angles + common side give ASA.'),
    ])(r)


def c12s2_rhombus(r):
    p, q, s = triple(r)
    return Q(f'The diagonals of a rhombus are {2 * p} cm and {2 * q} cm. Find the length of each side, giving reasons.', f'{s} cm',
             f'Diagonals bisect at right angles: half-diagonals {p} and {q}; side = √({p}² + {q}²) = {s} (3 marks).', [f'{p + q} cm', f'{2 * s} cm', f'{s + 1} cm'])


def c12s2_case(r):
    a, b = r.randint(8, 20), r.randint(5, 15)
    ang = r.randint(55, 80)
    return Q((f'A gate in a farmhouse is made in the shape of a parallelogram ABCD with AB = {a} dm, BC = {b} dm and ∠A = {ang}°. '
              f'(i) Find CD and DA. (ii) Find ∠B, ∠C and ∠D. (iii) The diagonals meet at O. If AO = {b - 1} dm, find AC. (iv) Find the perimeter of the gate.'),
             f'(i) {a} dm, {b} dm (ii) {180 - ang}°, {ang}°, {180 - ang}° (iii) {2 * (b - 1)} dm (iv) {2 * (a + b)} dm', '1 mark each part.')


# st3 conditions for a parallelogram

def c12s3_mcq(r):
    return mcqbank([
        ('A quadrilateral is a parallelogram if …', 'its diagonals bisect each other', ['its diagonals are equal', 'one pair of opposite sides is equal', 'two adjacent angles are equal'], 'Converse theorem.'),
        ('A quadrilateral in which one pair of opposite sides is both equal and parallel is …', 'a parallelogram', ['a trapezium only', 'a kite', 'not necessarily a parallelogram'], 'Theorem.'),
        ('A quadrilateral with both pairs of opposite angles equal is …', 'a parallelogram', ['a kite', 'a trapezium', 'always a square'], 'Converse theorem.'),
        ('Which condition does NOT guarantee a parallelogram?', 'one pair of sides parallel and the other pair equal', ['both pairs of opposite sides equal', 'diagonals bisect each other', 'both pairs of opposite angles equal'], 'An isosceles trapezium satisfies it.'),
    ])(r)


def c12s3_check(r):
    a, b = r.randint(4, 15), r.randint(4, 15)
    case = r.choice(['sides', 'angles', 'diag', 'fail'])
    if case == 'sides':
        return Q(f'In quadrilateral ABCD, AB = {a} cm, BC = {b} cm, CD = {a} cm and DA = {b} cm. Is ABCD a parallelogram? Give the condition used.', 'Yes', 'Both pairs of opposite sides are equal.')
    if case == 'angles':
        x = r.randint(60, 120)
        return Q(f'In quadrilateral PQRS, ∠P = {x}°, ∠Q = {180 - x}°, ∠R = {x}° and ∠S = {180 - x}°. Is PQRS a parallelogram? Give the condition used.', 'Yes', 'Both pairs of opposite angles are equal.')
    if case == 'diag':
        return Q(f'The diagonals of quadrilateral WXYZ meet at O with OW = OY = {a} cm and OX = OZ = {b} cm. Is WXYZ a parallelogram? Give the condition used.', 'Yes', 'The diagonals bisect each other.')
    return Q(f'In quadrilateral KLMN, KL ∥ NM and LM = KN = {a} cm, but KL = {a + 3} cm and NM = {a + 7} cm. Is KLMN a parallelogram?', 'No (it is an isosceles trapezium)', 'The parallel sides are unequal, so the other pair is not parallel.')


def c12s3_explain(r):
    return xbank([
        ('Prove that if the diagonals of a quadrilateral bisect each other, it is a parallelogram.', '△AOB ≅ △COD (SAS) ⇒ ∠OAB = ∠OCD ⇒ AB ∥ CD; similarly AD ∥ BC.', '3 marks.'),
        ('Prove that a quadrilateral with one pair of opposite sides equal and parallel is a parallelogram.', 'Draw diagonal AC; △ABC ≅ △CDA (SAS) ⇒ ∠BCA = ∠DAC ⇒ BC ∥ AD.', '3 marks.'),
        ('Explain why the converse of "the diagonals of a parallelogram bisect each other" is useful.', 'It gives a test: if diagonals bisect each other, the shape is a parallelogram.', '2 marks.'),
    ])(r)


def c12s3_ar(r):
    return arbank([
        ('A quadrilateral whose diagonals bisect each other is a parallelogram.', 'This is the converse of a property of parallelograms, and it can be proved using congruent triangles.', 'a', 'R explains A.'),
        ('A quadrilateral with equal diagonals is a rectangle.', 'The diagonals of a rectangle are equal.', 'd', 'An isosceles trapezium also has equal diagonals; A false, R true.'),
        ('If ABCD has AB ∥ DC and AB = DC, then AD = BC.', 'A quadrilateral with one pair of opposite sides equal and parallel is a parallelogram.', 'a', 'R gives a parallelogram, so AD = BC.'),
    ])(r)


def c12s3_coord(r):
    A = (r.randint(-5, 2), r.randint(-5, 2))
    u = (r.randint(2, 6), r.randint(-2, 3))
    v = (r.randint(-2, 2), r.randint(2, 6))
    B = (A[0] + u[0], A[1] + u[1])
    C = (B[0] + v[0], B[1] + v[1])
    D = (A[0] + v[0], A[1] + v[1])
    return Q(f'Show that A{P(*A)}, B{P(*B)}, C{P(*C)} and D{P(*D)} form a parallelogram by finding the mid-points of the diagonals AC and BD.', f'Both mid-points are {P(Fr(A[0] + C[0], 2), Fr(A[1] + C[1], 2))}',
             'Equal mid-points ⇒ diagonals bisect each other ⇒ parallelogram (3 marks).')


def c12s3_case(r):
    a = r.randint(20, 50)
    return Q((f'A carpenter checks a window frame ABCD. She measures AB = CD = {a} cm and AD = BC = {a + 15} cm. (i) Can she conclude ABCD is a parallelogram? Which condition? '
              f'(ii) She also finds the diagonals are equal. What more can she conclude? (iii) Which single extra measurement would show the frame is a square if all sides were equal? (iv) Why is checking only one pair of equal opposite sides not enough?'),
             '(i) yes; both pairs of opposite sides equal (ii) it is a rectangle (iii) one angle = 90° or equal diagonals (iv) a quadrilateral with one pair of equal opposite sides may be an isosceles trapezium',
             '1 mark each part.')


# st4 mid-point theorem

def c12s4_half(r):
    bc = r.choice([6, 8, 9, 10, 12, 14, 15, 7.5, 11])
    return Q(f'In △ABC, D and E are the mid-points of AB and AC. If BC = {num(bc)} cm, find DE.', f'{num(bc / 2)} cm', 'Mid-point theorem: DE ∥ BC and DE = ½ BC.',
             [f'{num(bc)} cm', f'{num(bc * 2)} cm', f'{num(bc / 4)} cm'])


def c12s4_perim(r):
    a, b, c = r.randint(5, 20), r.randint(5, 20), r.randint(5, 20)
    if not (a + b > c and b + c > a and a + c > b):
        raise ValueError
    return Q(f'The sides of a triangle are {a} cm, {b} cm and {c} cm. Find the perimeter of the triangle formed by joining the mid-points of its sides.', f'{num((a + b + c) / 2)} cm',
             'Each side of the mid-point triangle is half a side of the original.', [f'{a + b + c} cm', f'{num((a + b + c) / 4)} cm', f'{2 * (a + b + c)} cm'])


def c12s4_mcq(r):
    return mcqbank([
        ('The line segment joining the mid-points of two sides of a triangle is …', 'parallel to the third side and half of it', ['equal to the third side', 'perpendicular to the third side', 'parallel to the third side and twice it'], 'Mid-point theorem.'),
        ('A line through the mid-point of one side of a triangle, parallel to another side, …', 'bisects the third side', ['is perpendicular to the third side', 'meets the third side at a vertex', 'is equal to the third side'], 'Converse of the mid-point theorem.'),
        ('The quadrilateral formed by joining the mid-points of the sides of any quadrilateral, in order, is a …', 'parallelogram', ['rectangle always', 'rhombus always', 'trapezium only'], 'Each side is parallel to a diagonal.'),
    ])(r)


def c12s4_explain(r):
    return xbank([
        ('Prove the mid-point theorem: in △ABC, if D and E are the mid-points of AB and AC, then DE ∥ BC and DE = ½ BC.', 'Extend DE to F with EF = DE; △ADE ≅ △CFE (SAS) ⇒ CF = AD = DB and CF ∥ AB ⇒ DBCF is a parallelogram ⇒ DF = BC, DE = ½ BC.', '4 marks.'),
        ('Explain why joining the mid-points of a rectangle\'s sides gives a rhombus.', 'Each side of the inner figure is half a diagonal of the rectangle, and the diagonals of a rectangle are equal.', '2 marks.'),
        ('Explain why joining the mid-points of a rhombus\'s sides gives a rectangle.', 'Inner sides are parallel to the diagonals, which are perpendicular in a rhombus.', '2 marks.'),
    ])(r)


def c12s4_ar(r):
    bc = r.randint(6, 20)
    return arbank([
        (f'If D, E are mid-points of AB, AC of △ABC and BC = {bc} cm, then DE = {num(bc / 2)} cm.', 'The segment joining the mid-points of two sides of a triangle is half the third side.', 'a', 'R explains A.'),
        ('Joining the mid-points of the sides of any quadrilateral gives a parallelogram.', 'The diagonals of a parallelogram bisect each other.', 'b', 'Both true; A follows from the mid-point theorem, not from R.'),
        ('The figure formed by joining mid-points of a square\'s sides is a rectangle that is not a square.', 'The diagonals of a square are equal and perpendicular.', 'd', 'It is a square; A false, R true.'),
    ])(r)


def c12s4_trap(r):
    a, b = r.randint(6, 20), r.randint(6, 20)
    if a == b:
        b += 4
    return Q(f'In trapezium ABCD, AB ∥ DC, AB = {a} cm and DC = {b} cm. E and F are the mid-points of AD and BC. Using the mid-point theorem (draw diagonal AC), find EF.', f'{num((a + b) / 2)} cm',
             f'Let AC meet EF at G: EG = ½ DC = {num(b / 2)}, GF = ½ AB = {num(a / 2)}; EF = {num((a + b) / 2)} (4 marks).')


def c12s4_case(r):
    a, b, c = r.choice([(30, 40, 50), (24, 32, 40), (60, 80, 100), (18, 24, 30)])
    return Q((f'A triangular plot ABC has AB = {a} m, BC = {b} m and CA = {c} m. A gardener joins the mid-points D, E, F of AB, BC and CA with ropes. '
              f'(i) Find the lengths DE, EF and FD. (ii) Find the total rope used. (iii) How many smaller triangles are formed, and how are they related? (iv) What fraction of the plot\'s area is △DEF?'),
             f'(i) DE = {c // 2} m, EF = {a // 2} m, FD = {b // 2} m (ii) {(a + b + c) // 2} m (iii) 4 congruent triangles (iv) ¼', '1 mark each part.')


# ---------------- ch13 Linear equations in two variables ----------------

def c13s1_form(r):
    who = name(r)
    p, q = r.choice([10, 12, 15, 20, 25]), r.choice([5, 6, 8, 30, 40])
    t = r.randint(5, 20) * 10
    item = r.choice([('notebooks', 'pens', 'each'), ('apples', 'bananas', 'each'), ('adult tickets', 'child tickets', 'each'), ('kg of rice', 'kg of dal', 'per kg'), ('geometry boxes', 'erasers', 'each')])
    return Q(f'{who} buys x {item[0]} at ₹{p} {item[2]} and y {item[1]} at ₹{q} {item[2]} and spends ₹{t} in all. Write a linear equation in two variables for this situation.', f'{p}x + {q}y = {t}',
             f'Cost of the {item[0]} is {p}x and of the {item[1]} is {q}y; together they equal {t}.', [f'{p}x − {q}y = {t}', f'{q}x + {p}y = {t}', f'x + y = {t}'])


def c13s1_abc(r):
    a, b, c = nz2(r), nz2(r), nz2(r)
    return Q(f'Write {eq2(a, b, c)} in the form ax + by + c = 0 and state a, b and c.', f'a = {fn(a)}, b = {fn(b)}, c = {fn(-c)}',
             f'{term(a, "x", first=True)}{term(b, "y")} {signed(-c)} = 0.', [f'a = {fn(a)}, b = {fn(b)}, c = {fn(c)}', f'a = {fn(b)}, b = {fn(a)}, c = {fn(-c)}', f'a = {fn(-a)}, b = {fn(-b)}, c = {fn(-c)}'])


def nz2(r, lo=1, hi=9):
    return r.choice([-1, 1]) * r.randint(lo, hi)


def c13s1_mcq(r):
    return mcqbank([
        ('Which of the following is a linear equation in two variables?', '3x − 2y = 7', ['x² + y = 4', 'xy = 6', '3x + 5 = 11'], 'Degree 1 in x and y, both present.'),
        ('The equation x = 5, written as a linear equation in two variables, is …', '1·x + 0·y = 5', ['x + y = 5', '0·x + 1·y = 5', 'x + 5y = 0'], 'Coefficient of y is 0.'),
        ('In 2x + 3y = 12, if y = 0 then x = …', '6', ['4', '12', '0'], '2x = 12.'),
    ])(r)


def c13s1_explain(r):
    return xbank([
        ('Explain why x + 2y = 6 is called a linear equation in two variables.', 'It has two variables, each with power 1 and no product xy.', '2 marks.'),
        ('"The cost of a pen is ₹5 more than twice the cost of a pencil." Explain how this becomes a linear equation in two variables.', 'Let pen = x, pencil = y: x = 2y + 5, i.e. x − 2y − 5 = 0.', '2 marks.'),
        ('Can y = 3 be treated as a linear equation in two variables? Explain.', 'Yes: 0·x + 1·y = 3; every point with y = 3 is a solution.', '2 marks.'),
    ])(r)


def c13s1_ar(r):
    return arbank([
        ('2x + 3y = 5 is a linear equation in two variables.', 'Each variable appears with power 1.', 'a', 'R explains A.'),
        ('xy = 4 is a linear equation in two variables.', 'It contains two variables.', 'd', 'The term xy has degree 2; A false, R true.'),
        ('y = 7 can be written as 0x + y = 7.', 'Any linear equation in one variable can be written in two variables with a zero coefficient.', 'a', 'R explains A.'),
    ])(r)


def c13s1_case(r):
    a, c = r.choice([(100, 50), (80, 40), (150, 50), (200, 100), (120, 60)])
    t = c * r.randint(30, 60)
    n = r.randint(3, t // a - 1)
    pairs = [(x, (t - a * x) // c) for x in range(0, t // a + 1) if (t - a * x) % c == 0 and x != n]
    two = r.sample(pairs, 2)
    return Q((f'At a science fair in Chandigarh, adult tickets cost ₹{a} and child tickets ₹{c}. The total collection was ₹{t}. (i) Write a linear equation for x adult and y child tickets. '
              f'(ii) If {n} adults came, how many children came? (iii) Can the number of adults be {t // a + 1}? Why? (iv) Find two other possible pairs (x, y).'),
             f'(i) {a}x + {c}y = {t} (ii) {(t - a * n) // c} (iii) no; {a} × {t // a + 1} = {a * (t // a + 1)} > {t} (iv) e.g. {P(*two[0])}, {P(*two[1])} (any whole-number solutions)',
             '1 mark each part.')


# st2 solutions

def c13s2_check(r):
    a, b = nz2(r, 1, 6), nz2(r, 1, 6)
    x, y = nz2(r, 0, 6), nz2(r, 0, 6)
    c = a * x + b * y + r.choice([0, 0, 1, -2])
    ok = a * x + b * y == c
    return Q(f'Is ({fn(x)}, {fn(y)}) a solution of {eq2(a, b, c)}? Show your check.', 'Yes' if ok else 'No',
             f'LHS = {fn(a)} × {bracket(x)} + {bracket(b)} × {bracket(y)} = {fn(a * x + b * y)}; RHS = {fn(c)}.', ['No' if ok else 'Yes', 'Only if x = 0', 'Cannot be decided'])


def c13s2_k(r):
    a, b = nz2(r, 1, 6), nz2(r, 1, 6)
    x, y = nz2(r, 1, 5), nz2(r, 1, 5)
    k = a * x + b * y
    return Q(f'If x = {fn(x)}, y = {fn(y)} is a solution of {term(a, "x", first=True)}{term(b, "y")} = k, find k.', fn(k), f'k = {fn(a)}({fn(x)}) + {bracket(b)}({fn(y)}) = {fn(k)}.',
             num_distractors(k, a * x - b * y, a + b, a * y + b * x))


def c13s2_find(r):
    a, b = r.randint(1, 6), nz2(r, 1, 6)
    x0, y0 = r.randint(-4, 4), r.randint(-4, 4)
    c = a * x0 + b * y0
    sols = []
    for x in range(-6, 7):
        if (c - a * x) % b == 0:
            sols.append((x, (c - a * x) // b))
    pick = r.sample(sols, min(3, len(sols)))
    return Q(f'Find three different solutions of {eq2(a, b, c)}.', ', '.join(P(*s) for s in pick) + ' (any three correct)',
             'Choose values of x and solve for y; check each pair (1 mark each).')


def c13s2_mcq(r):
    a, b = r.randint(1, 5), r.randint(1, 5)
    x, y = r.randint(-3, 5), r.randint(-3, 5)
    c = a * x + b * y
    wrong = [(x + 1, y), (x - 1, y + 2), (x, y - 1)]
    if any(a * px + b * py == c for px, py in wrong):
        raise ValueError
    return mcq(f'Which of the following is a solution of {eq2(a, b, c)}?', P(x, y), [P(*w) for w in wrong], 'Substitute each pair.', r)


def c13s2_explain(r):
    a, b, c = r.randint(1, 5), r.randint(1, 5), r.randint(5, 20)
    return Q(f'Explain why the equation {eq2(a, b, c)} has infinitely many solutions.', 'For every value of x there is a value of y that satisfies it.',
             (f'y = ({c} − {a}x)/{b}' if b > 1 else f'y = {c} − {a}x') + ' gives a solution for each real x (2 marks).')


def c13s2_ar(r):
    return arbank([
        ('A linear equation in two variables has infinitely many solutions.', 'For each value of x, a corresponding value of y can be found.', 'a', 'R explains A.'),
        ('(2, 3) is a solution of x + y = 5.', 'A solution makes the left side equal to the right side.', 'a', '2 + 3 = 5.'),
        ('2x + 3y = 12 has exactly one solution (3, 2).', 'Substituting (3, 2) gives 6 + 6 = 12.', 'd', 'It has infinitely many solutions, e.g. (0, 4); A false, R true.'),
    ])(r)


def c13s2_case(r):
    who = name(r)
    p, q = r.choice([(2, 3), (3, 5), (4, 5), (2, 5), (3, 4)])
    t = p * q * r.randint(2, 4)
    sols = [(x, (t - p * x) // q) for x in range(0, t // p + 1) if (t - p * x) % q == 0]
    return Q((f'In an inter-school quiz, each easy question answered correctly earns {p} points and each hard question {q} points. {who} scored {t} points in all, '
              f'answering x easy and y hard questions correctly. (i) Write an equation. (ii) List all whole-number solutions. (iii) Which solution has the fewest correct answers in total? (iv) Why are fractional solutions not acceptable here?'),
             f'(i) {p}x + {q}y = {t} (ii) {", ".join(P(*s_) for s_ in sols)} (iii) {P(*min(sols, key=lambda s_: s_[0] + s_[1]))} (iv) questions are counted in whole numbers',
             '1 mark each part.')


# st3 graph

def c13s3_intercepts(r):
    a, b = nz2(r, 1, 6), nz2(r, 1, 6)
    c = a * b * nz2(r, 1, 3)
    return Q(f'Find the points where the graph of {eq2(a, b, c)} cuts the x-axis and the y-axis.', f'x-axis {P(Fr(c, a), 0)}, y-axis {P(0, Fr(c, b))}',
             'Put y = 0 for the x-intercept and x = 0 for the y-intercept.',
             list(dict.fromkeys(w for w in [f'x-axis {P(Fr(c, b), 0)}, y-axis {P(0, Fr(c, a))}', f'x-axis {P(-Fr(c, a), 0)}, y-axis {P(0, -Fr(c, b))}', f'x-axis {P(0, Fr(c, a))}, y-axis {P(Fr(c, b), 0)}', f'x-axis {P(a, 0)}, y-axis {P(0, b)}']
                                    if w != f'x-axis {P(Fr(c, a), 0)}, y-axis {P(0, Fr(c, b))}'))[:3])


def c13s3_mcq(r):
    return mcqbank([
        ('The graph of a linear equation in two variables is …', 'a straight line', ['a parabola', 'a circle', 'a pair of points'], 'Every solution lies on one line.'),
        ('Every point on the graph of a linear equation is …', 'a solution of the equation', ['the origin', 'on the x-axis', 'not a solution'], 'Definition of the graph.'),
        ('The graph of y = kx always passes through …', 'the origin', ['(k, 0)', '(0, k)', '(1, 1)'], 'x = 0 gives y = 0.'),
        ('How many linear equations in two variables can pass through the point (2, 3)?', 'infinitely many', ['only one', 'two', 'none'], 'Infinitely many lines pass through a point.'),
    ])(r)


def c13s3_table(r):
    a, b = r.randint(1, 4), nz2(r, 1, 8)
    xs = [-1, 0, 1, 2]
    return Q(f'Complete the table of values for y = {lin(a, b)} at x = −1, 0, 1, 2 and say what the graph looks like.', ', '.join(fn(a * x + b) for x in xs) + '; a straight line',
             'Substitute each x (2 marks).')


def c13s3_area(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    c = a * b * r.randint(1, 4)
    X, Y = Fr(c, a), Fr(c, b)
    return Q(f'Draw the graph of {eq2(a, b, c)} (describe the two points used) and find the area of the triangle it forms with the coordinate axes.', f'{fn(X * Y / 2)} square units',
             f'Intercepts ({fn(X)}, 0) and (0, {fn(Y)}); area = ½ × {fn(X)} × {fn(Y)} = {fn(X * Y / 2)} (4 marks).')


def c13s3_explain(r):
    return xbank([
        ('Explain why two points are enough to draw the graph of a linear equation in two variables, and why a third point is useful.', 'A line is fixed by two points; a third point checks for errors.', '2 marks.'),
        ('Explain why the point where a line cuts the y-axis has x-coordinate 0.', 'Every point on the y-axis has abscissa 0.', '2 marks.'),
        ('Explain how to check from a graph whether (4, 1) is a solution of x − 2y = 2.', 'See whether the point (4, 1) lies on the line; algebraically 4 − 2 = 2, so yes.', '2 marks.'),
    ])(r)


def c13s3_ar(r):
    a, b = r.randint(1, 5), r.randint(1, 5)
    return arbank([
        (f'The graph of y = {a}x passes through the origin.', '(0, 0) satisfies y = kx for every k.', 'a', 'R explains A.'),
        (f'The point (0, {b}) lies on the graph of x + y = {b}.', 'A point lies on the graph if its coordinates satisfy the equation.', 'a', f'0 + {b} = {b}.'),
        ('The graph of 2x + 3y = 6 passes through (3, 2).', 'The graph of a linear equation is a straight line.', 'd', '2(3) + 3(2) = 12 ≠ 6; A false, R true.'),
    ])(r)


def c13s3_case(r):
    f, k = r.choice([(30, 10), (50, 12), (40, 15), (25, 8)])
    return Q((f'An auto-rickshaw charges ₹{f} for the first km and ₹{k} for each later km. (i) Taking distance x km and fare ₹y, write a linear equation (x ≥ 1). '
              f'(ii) Find the fare for 6 km. (iii) Find two points to draw the graph. (iv) From the equation, find the distance for a fare of ₹{f + 9 * k}.'),
             f'(i) y = {f} + {k}(x − 1), i.e. y = {k}x + {f - k} (ii) ₹{f + 5 * k} (iii) e.g. (1, {f}) and (6, {f + 5 * k}) (iv) 10 km', '1 mark each part.')


# st4 lines parallel to axes

def c13s4_mcq(r):
    k = nz2(r, 1, 9)
    if r.random() < 0.5:
        return mcq(f'The graph of x = {fn(k)} is …', 'a line parallel to the y-axis', ['a line parallel to the x-axis', 'a line through the origin', 'the x-axis'], f'All points have abscissa {fn(k)}.', r)
    return mcq(f'The graph of y = {fn(k)} is …', 'a line parallel to the x-axis', ['a line parallel to the y-axis', 'a line through the origin', 'the y-axis'], f'All points have ordinate {fn(k)}.', r)


def c13s4_eq(r):
    k = nz2(r, 1, 9)
    ax = r.choice(['x-axis', 'y-axis'])
    side = r.choice(['above', 'below']) if ax == 'x-axis' else r.choice(['to the right of', 'to the left of'])
    sgn = 1 if side in ('above', 'to the right of') else -1
    ans = f'y = {fn(sgn * abs(k))}' if ax == 'x-axis' else f'x = {fn(sgn * abs(k))}'
    return Q(f'Write the equation of the line parallel to the {ax} at a distance of {abs(k)} units {side} it.', ans, 'Lines parallel to the x-axis are y = c; parallel to the y-axis are x = c.',
             [ans.replace('y =', 'x =') if ax == 'x-axis' else ans.replace('x =', 'y ='), ans.replace(fn(sgn * abs(k)), fn(-sgn * abs(k))), f'x + y = {abs(k)}'])


def c13s4_meet(r):
    a, b = nz2(r, 1, 8), nz2(r, 1, 8)
    return Q(f'Find the point of intersection of the lines x = {fn(a)} and y = {fn(b)}, and the area of the rectangle formed by these lines and the coordinate axes.', f'{P(a, b)}; {abs(a * b)} sq units',
             f'Both conditions hold at {P(a, b)}; rectangle sides {abs(a)} and {abs(b)}.', [f'{P(b, a)}; {abs(a * b)} sq units', f'{P(a, b)}; {abs(a) + abs(b)} sq units', f'{P(a, b)}; {2 * (abs(a) + abs(b))} sq units'])


def c13s4_explain(r):
    return xbank([
        ('Explain why x = 3 represents a single point on a number line but a line on the Cartesian plane.', 'In one variable it is the number 3; in two variables, every point (3, y) satisfies it.', '2 marks.'),
        ('Explain why the equation of the x-axis is y = 0.', 'Every point on the x-axis has ordinate 0.', '2 marks.'),
    ])(r)


def c13s4_ar(r):
    k = nz2(r, 1, 9)
    return arbank([
        (f'The graph of y = {fn(k)} is parallel to the x-axis.', f'Every point on the graph has the same y-coordinate {fn(k)}.', 'a', 'R explains A.'),
        ('The graph of x = 0 is the x-axis.', 'Points on the y-axis have x-coordinate 0.', 'd', 'x = 0 is the y-axis; A false, R true.'),
        (f'The lines x = {fn(k)} and y = {fn(k)} are perpendicular.', 'A line parallel to the x-axis is perpendicular to a line parallel to the y-axis.', 'a', 'R explains A.'),
    ])(r)


def c13s4_read(r):
    c = r.choice([0, 32])
    temp = r.randint(-10, 45)
    return Q(f'The relation between Fahrenheit and Celsius is F = (9/5)C + 32. (i) Find F when C = {temp}. (ii) Find C when F = 212. (iii) Is there a temperature that is numerically the same in both scales? Find it.',
             f'(i) {num(9 * temp / 5 + 32)} °F (ii) 100 °C (iii) yes, −40°', 'Substitution (1 + 1), solve F = C (2).')


def c13s4_case(r):
    s = r.choice([40, 50, 60])
    t = r.randint(2, 5)
    return Q((f'A car travels at a uniform speed of {s} km/h on a highway. (i) Write the distance d (km) as a linear equation in t (hours). (ii) Find d for t = {t}. '
              f'(iii) Another car stands parked at the 100 km mark. Write the equation of its "graph". (iv) After how long does the first car pass the parked car?'),
             f'(i) d = {s}t (ii) {s * t} km (iii) d = 100 (a line parallel to the t-axis) (iv) {num(100 / s)} h', '1 mark each part.')


# ---------------- ch14 Surface area and volume ----------------

def c14s1_mcq(r):
    return mcqbank([
        ('The total surface area of a cuboid of length l, breadth b and height h is …', '2(lb + bh + hl)', ['lbh', 'l + b + h', '2h(l + b)'], 'Six rectangular faces.'),
        ('The lateral (curved) surface area of a cylinder of radius r and height h is …', '2πrh', ['πr²h', '2πr(r + h)', 'πrh'], 'Unroll to a rectangle 2πr × h.'),
        ('The volume of a cylinder of radius r and height h is …', 'πr²h', ['2πrh', '⅓πr²h', 'πrh²'], 'Base area × height.'),
        ('The total surface area of a cube of edge a is …', '6a²', ['4a²', 'a³', '12a'], 'Six square faces.'),
    ])(r)


def c14s1_cuboid(r):
    l, b, h = r.randint(5, 30), r.randint(4, 20), r.randint(3, 15)
    return Q(f'Find the total surface area and volume of a cuboid {l} cm × {b} cm × {h} cm.', f'TSA {2 * (l * b + b * h + h * l)} cm², volume {l * b * h} cm³',
             f'2({l * b} + {b * h} + {h * l}) = {2 * (l * b + b * h + h * l)}; {l} × {b} × {h} = {l * b * h}.',
             [f'TSA {l * b + b * h + h * l} cm², volume {l * b * h} cm³', f'TSA {2 * (l * b + b * h + h * l)} cm², volume {2 * l * b * h} cm³', f'TSA {2 * h * (l + b)} cm², volume {l * b * h} cm³'])


def c14s1_cyl(r):
    rr, h = r.choice([7, 14, 3.5, 10.5, 21]), r.randint(5, 30)
    V = PI * Fr(rr) ** 2 * h
    C = 2 * PI * Fr(rr) * h
    return Q(f'Find the curved surface area and the volume of a cylinder of radius {num(rr)} cm and height {h} cm (π = 22/7).', f'CSA {pistr(C)} cm², volume {pistr(V)} cm³',
             '2πrh and πr²h.', [f'CSA {pistr(V)} cm², volume {pistr(C)} cm³', f'CSA {pistr(C / 2)} cm², volume {pistr(V)} cm³', f'CSA {pistr(C)} cm², volume {pistr(V / 3)} cm³'])


def c14s1_cube(r):
    a = r.randint(3, 20)
    return Q(f'A cube has edge {a} cm. Find its lateral surface area.', f'{4 * a * a} cm²', f'4a² = 4 × {a * a}.', [f'{6 * a * a} cm²', f'{a ** 3} cm²', f'{12 * a} cm²'])


def c14s1_explain(r):
    return xbank([
        ('Explain why the curved surface area of a cylinder is 2πrh.', 'Cut and unroll it into a rectangle whose length is the circumference 2πr and width h.', '2 marks.'),
        ('Explain the difference between the lateral surface area and the total surface area of a cuboid, with an example of when each is needed.', 'Lateral = four walls 2h(l + b) (e.g. painting walls of a room); total includes top and bottom (e.g. wrapping a box).', '2 marks.'),
        ('If each edge of a cube is doubled, by what factor do its surface area and volume change? Explain.', 'Surface area × 4, volume × 8.', 'Area ∝ a², volume ∝ a³ (2 marks).'),
    ])(r)


def c14s1_ar(r):
    a = r.randint(2, 9)
    return arbank([
        (f'The volume of a cube of edge {a} cm is {a ** 3} cm³.', 'Volume of a cube = a³.', 'a', 'R gives A.'),
        ('Two cuboids with the same volume have the same surface area.', 'Volume of a cuboid = lbh.', 'd', 'e.g. 1 × 1 × 8 and 2 × 2 × 2; A false, R true.'),
        ('A cylinder of radius r and height h holds πr²h units of liquid.', 'The volume of a cylinder = base area × height.', 'a', 'R explains A.'),
    ])(r)


def c14s1_room(r):
    l, b, h = r.randint(4, 8), r.randint(3, 6), 3
    door, win = 2, r.randint(1, 3) * 1.5
    rate = r.choice([20, 25, 30, 40])
    A = 2 * h * (l + b) + l * b - door - win
    return Q((f'A classroom is {l} m long, {b} m wide and {h} m high. The four walls and the ceiling are to be painted, leaving a door of area {door} m² and windows of total area {num(win)} m². '
              f'Find the area to be painted and the cost at ₹{rate} per m².'), f'{num(A)} m²; {inr(A * rate)}',
             f'Walls 2h(l + b) = {2 * h * (l + b)}, ceiling {l * b}, minus {door} and {num(win)} (4 marks).')


def c14s1_case(r):
    rr, h = r.choice([(7, 20), (14, 30), (3.5, 10), (10.5, 20)])
    V = PI * Fr(rr) ** 2 * h
    return Q((f'A cylindrical water tank on a roof in Jaipur has internal radius {num(rr)} dm and height {h} dm (π = 22/7). (i) Find its capacity in litres (1 dm³ = 1 L). '
              f'(ii) Find the area of metal sheet needed for its curved surface. (iii) If a family uses 150 L a day, how many full days does a full tank last? (iv) If the radius were doubled, how would the capacity change?'),
             f'(i) {pistr(V)} L (ii) {pistr(2 * PI * Fr(rr) * h)} dm² (iii) {int(V // 150)} days (iv) 4 times', '1 mark each part.')


# st2 cone

def cone(r):
    a, b, c = triple(r)
    k = r.choice([1, 1, 2])
    # radius a*k (prefer multiples of 7), height b*k, slant c*k
    return a * k, b * k, c * k


def c14s2_slant(r):
    rr, h, l = cone(r)
    return Q(f'A right circular cone has radius {rr} cm and height {h} cm. Find its slant height.', f'{l} cm', f'l = √(r² + h²) = √({rr * rr} + {h * h}) = {l}.', [f'{rr + h} cm', f'{abs(h - rr)} cm', f'{l * l} cm'])


def c14s2_mcq(r):
    return mcqbank([
        ('The curved surface area of a cone of radius r and slant height l is …', 'πrl', ['2πrl', 'πr²l', '⅓πrl'], 'Formula from the sector net.'),
        ('The volume of a cone is … the volume of a cylinder with the same base and height.', 'one-third', ['half', 'equal to', 'twice'], 'V = ⅓πr²h.'),
        ('The slant height l of a cone with radius r and height h is …', '√(r² + h²)', ['r + h', '√(h² − r²)', 'r² + h²'], 'Pythagoras on the right triangle.'),
        ('The total surface area of a cone is …', 'πr(l + r)', ['πrl', '2πr(l + r)', 'πr² + 2πrl'], 'Curved + base.'),
    ])(r)


def c14s2_csa(r):
    rr = r.choice([7, 14, 21, 3.5])
    l = r.randint(10, 30)
    A = PI * Fr(rr) * l
    return Q(f'Find the curved surface area of a cone with base radius {num(rr)} cm and slant height {l} cm (π = 22/7).', f'{pistr(A)} cm²', 'CSA = πrl.',
             [f'{pistr(2 * A)} cm²', f'{pistr(A + PI * Fr(rr) ** 2)} cm²', f'{pistr(PI * Fr(rr) ** 2 * l / 3)} cm²'])


def c14s2_vol(r):
    rr = r.choice([7, 14, 21, 3.5])
    h = r.choice([6, 9, 12, 15, 24, 30])
    V = Fr(1, 3) * PI * Fr(rr) ** 2 * h
    return Q(f'Find the volume of a cone of radius {num(rr)} cm and height {h} cm (π = 22/7).', f'{pistr(V)} cm³', '⅓πr²h.',
             [f'{pistr(3 * V)} cm³', f'{pistr(V / 2)} cm³', f'{pistr(PI * Fr(rr) * h / 3)} cm³'])


def c14s2_tsa(r):
    rr, h, l = cone(r)
    A = PI * rr * (l + rr)
    return Q(f'A cone has radius {rr} cm and height {h} cm. Find its total surface area (π = 22/7).', f'{pistr(A)} cm²',
             f'l = √({rr}² + {h}²) = {l}; TSA = πr(l + r) = 22/7 × {rr} × {l + rr} (3 marks).')


def c14s2_explain(r):
    return xbank([
        ('Explain, using the NCERT activity of filling a cylinder with a cone of the same base and height, why the volume of a cone is ⅓πr²h.', 'The cone filled with sand/water needs to be emptied 3 times to fill the cylinder.', '2 marks.'),
        ('Explain why the curved surface of a cone opens out into a sector of a circle of radius l.', 'Every point on the base circle is at distance l from the vertex, so the net is part of a circle of radius l; its arc is 2πr.', '2 marks.'),
    ])(r)


def c14s2_ar(r):
    rr, h, l = cone(r)
    return arbank([
        (f'A cone with radius {rr} cm and height {h} cm has slant height {l} cm.', 'The radius, height and slant height of a cone form a right triangle.', 'a', 'R explains A.'),
        ('A cone and a cylinder with the same base and height have equal volumes.', 'The volume of a cone is ⅓πr²h.', 'd', 'The cone is one-third; A false, R true.'),
        ('Doubling the height of a cone doubles its volume.', 'Volume of a cone is proportional to its height for a fixed radius.', 'a', 'R explains A.'),
    ])(r)


def c14s2_tent(r):
    rr, h, l = r.choice([(7, 24, 25), (6, 8, 10), (14, 48, 50), (12, 5, 13), (21, 20, 29)])
    w = r.choice([2, 3, 4])
    A = PI * rr * l
    return Q((f'A conical tent has base radius {rr} m and height {h} m. (i) Find its slant height. (ii) Find the area of canvas needed (π = 22/7). '
              f'(iii) If the canvas is {w} m wide, find the length required (ignore wastage). (iv) Find the volume of air inside.'),
             f'(i) {l} m (ii) {pistr(A)} m² (iii) {pistr(A / w)} m (iv) {pistr(Fr(1, 3) * PI * rr * rr * h)} m³', '1 mark each part.')


# st3 sphere

def c14s3_mcq(r):
    return mcqbank([
        ('The surface area of a sphere of radius r is …', '4πr²', ['2πr²', '3πr²', '⁴⁄₃πr³'], 'Formula.'),
        ('The total surface area of a solid hemisphere of radius r is …', '3πr²', ['2πr²', '4πr²', 'πr²'], 'Curved 2πr² + base πr².'),
        ('The volume of a hemisphere of radius r is …', '⅔πr³', ['⁴⁄₃πr³', '⅓πr³', '2πr³'], 'Half of ⁴⁄₃πr³.'),
        ('If the radius of a sphere is doubled, its volume becomes …', '8 times', ['2 times', '4 times', '6 times'], 'V ∝ r³.'),
    ])(r)


def c14s3_sa(r):
    rr = r.choice([7, 14, 21, 3.5, 10.5])
    A = 4 * PI * Fr(rr) ** 2
    return Q(f'Find the surface area of a sphere of radius {num(rr)} cm (π = 22/7).', f'{pistr(A)} cm²', '4πr².', [f'{pistr(A / 2)} cm²', f'{pistr(Fr(4, 3) * PI * Fr(rr) ** 3)} cm²', f'{pistr(PI * Fr(rr) ** 2)} cm²'])


def c14s3_vol(r):
    rr = r.choice([7, 14, 21, 3.5])
    V = Fr(4, 3) * PI * Fr(rr) ** 3
    return Q(f'Find the volume of a sphere of radius {num(rr)} cm (π = 22/7).', f'{pistr(V)} cm³', '⁴⁄₃πr³.', [f'{pistr(V / 2)} cm³', f'{pistr(4 * PI * Fr(rr) ** 2)} cm³', f'{pistr(V * 3 / 4)} cm³'])


def c14s3_hemi(r):
    rr = r.choice([7, 14, 21, 3.5, 10.5])
    A = 3 * PI * Fr(rr) ** 2
    V = Fr(2, 3) * PI * Fr(rr) ** 3
    return Q(f'A solid hemisphere has radius {num(rr)} cm. Find its total surface area and volume (π = 22/7).', f'TSA {pistr(A)} cm², volume {pistr(V)} cm³', '3πr² and ⅔πr³ (3 marks).')


def c14s3_ratio(r):
    a, b = r.sample(range(1, 7), 2)
    return Q(f'The radii of two spheres are in the ratio {a} : {b}. Find the ratio of their surface areas and of their volumes.', f'{a * a} : {b * b} and {a ** 3} : {b ** 3}',
             'Area ∝ r², volume ∝ r³.', [f'{a} : {b} and {a * a} : {b * b}', f'{a * a} : {b * b} and {a * a} : {b * b}', f'{a ** 3} : {b ** 3} and {a * a} : {b * b}'])


def c14s3_explain(r):
    return xbank([
        ('Explain, using the NCERT activity with a ball and strings, why the surface area of a sphere is 4πr².', 'String wound on the hemisphere fills exactly four circles of radius r, so the sphere\'s surface = 4πr².', '2 marks.'),
        ('Explain why the total surface area of a hemispherical bowl (open) is 2πr², but of a solid hemisphere is 3πr².', 'Open bowl: curved surface only; solid: add the flat circular face πr².', '2 marks.'),
    ])(r)


def c14s3_ar(r):
    return arbank([
        ('If the radius of a sphere is halved, its surface area becomes one-fourth.', 'The surface area of a sphere is proportional to r².', 'a', 'R explains A.'),
        ('The total surface area of a solid hemisphere is 2πr².', 'The curved surface area of a hemisphere is half that of a sphere.', 'd', 'TSA is 3πr² (add the base); A false, R true.'),
        ('The volume of a hemisphere is half the volume of a sphere of the same radius.', 'A plane through the centre cuts a sphere into two equal halves.', 'a', 'R explains A.'),
    ])(r)


def c14s3_balloon(r):
    a, b = r.choice([(7, 14), (3.5, 7), (7, 21), (14, 21)])
    return Q(f'A spherical balloon is inflated so that its radius increases from {num(a)} cm to {num(b)} cm. Find the ratio of the surface areas before and after, and the increase in surface area (π = 22/7).',
             f'{fn(Fr(a) ** 2 / Fr(b) ** 2)} ({int(a * 2) ** 2 // math.gcd(int(a * 2) ** 2, int(b * 2) ** 2)} : {int(b * 2) ** 2 // math.gcd(int(a * 2) ** 2, int(b * 2) ** 2)}); increase {pistr(4 * PI * (Fr(b) ** 2 - Fr(a) ** 2))} cm²',
             '4πr² each (4 marks).')


def c14s3_case_fix(r):
    rr = r.choice([7, 10.5, 14])
    rate = r.choice([16, 20, 24])
    V = Fr(2, 3) * PI * Fr(rr) ** 3
    A = 2 * PI * Fr(rr) ** 2
    return Q((f'A hemispherical bowl made of steel has inner radius {num(rr)} cm (π = 22/7). (i) Find its capacity in litres. (ii) Find the inner curved surface area. '
              f'(iii) If it is tin-plated inside at ₹{rate} per 100 cm², find the cost. (iv) Why do we not add the area of a flat face here?'),
             f'(i) ≈ {num(float(V) / 1000, 3)} L (ii) {pistr(A)} cm² (iii) {inr(float(A) * rate / 100)} (iv) the bowl is open at the top',
             '1 mark each part.')


# st4 capacity and recasting

def c14s4_litres(r):
    l, b, h = r.randint(1, 4), r.choice([1, 1.5, 2]), r.choice([0.5, 1, 1.5])
    V = l * b * h
    return Q(f'A rectangular tank is {l} m × {num(b)} m × {num(h)} m. How many litres of water can it hold?', f'{num(V * 1000)} L', '1 m³ = 1000 L.',
             [f'{num(V * 100)} L', f'{num(V)} L', f'{num(V * 10000)} L'])


def c14s4_mcq(r):
    return mcqbank([
        ('1 litre equals …', '1000 cm³', ['100 cm³', '1 m³', '10 cm³'], '1 L = 1 dm³ = 1000 cm³.'),
        ('1 m³ equals …', '1000 litres', ['100 litres', '10 litres', '1 litre'], '1 m³ = 1000 dm³.'),
        ('When a solid is melted and recast into another shape, … remains the same.', 'the volume', ['the surface area', 'the height', 'the radius'], 'Metal is neither lost nor gained.'),
    ])(r)


def c14s4_recast(r):
    R = r.choice([3, 6, 9, 12])
    rr = r.choice([1, 1.5, 3])
    if rr >= R:
        raise ValueError
    n = Fr(R) ** 3 / Fr(rr) ** 3
    if n.denominator != 1:
        raise ValueError
    return Q(f'A metallic sphere of radius {R} cm is melted and recast into small spheres of radius {num(rr)} cm. How many small spheres are made?', str(n),
             f'(⁴⁄₃πR³)/(⁴⁄₃πr³) = ({R}/{num(rr)})³ = {n}.', num_distractors(int(n), int(R / rr) ** 2, int(R / rr), int(n) // 2))


def c14s4_cones(r):
    rr, h = r.choice([(7, 12), (3.5, 10), (14, 9), (7, 15)])
    H = h * r.randint(1, 3)
    n = Fr(PI * Fr(rr) ** 2 * H, Fr(1, 3) * PI * Fr(rr) ** 2 * h)
    return Q(f'How many cones of radius {num(rr)} cm and height {h} cm can be filled from a cylinder of the same radius and height {H} cm (full each time)?', str(n),
             f'Cylinder ÷ cone = πr²·{H} ÷ (⅓πr²·{h}) = {n}.', num_distractors(int(n), H // h, 3, int(n) * 2))


def c14s4_explain(r):
    return xbank([
        ('Explain why, when a cylinder is melted and recast into a cone of the same radius, the cone is three times as tall.', 'Volumes equal: πr²h = ⅓πr²H ⇒ H = 3h.', '2 marks.'),
        ('Explain why 1 litre = 1000 cm³.', '1 L = 1 dm³ and 1 dm = 10 cm, so 1 dm³ = 10 × 10 × 10 cm³.', '2 marks.'),
    ])(r)


def c14s4_ar(r):
    return arbank([
        ('A cylinder of volume 1 m³ holds 1000 L of water.', '1 m³ = 1000 dm³ and 1 dm³ = 1 L.', 'a', 'R explains A.'),
        ('When a sphere is recast into a cone, the surface area stays the same.', 'The volume stays the same when a solid is recast.', 'd', 'Surface area usually changes; A false, R true.'),
        ('8 spheres of radius 1 cm can be made from a sphere of radius 2 cm.', 'Volume of a sphere is proportional to r³.', 'a', '(2/1)³ = 8; R explains A.'),
    ])(r)


def c14s4_well(r):
    rr, d = r.choice([(3.5, 10), (1.75, 14), (2, 21), (3.5, 20), (7, 10)])
    L, B = r.choice([(22, 14), (44, 20), (33, 28), (28, 22)])
    V = PI * Fr(rr) ** 2 * d
    rise = V / (L * B)
    return Q((f'A well of diameter {num(2 * rr)} m is dug {d} m deep in a village near Nagpur. The earth taken out is spread evenly over a rectangular field {L} m × {B} m. '
              f'Find the volume of earth dug out and the height by which the field is raised (π = 22/7).'), f'{pistr(V)} m³; ' + (f'{pistr(rise)} m' if len(num(float(rise), 6)) <= 6 else f'≈ {num(float(rise), 3)} m ({num(float(rise) * 100, 1)} cm)'),
             f'Volume = πr²h = 22/7 × {num(rr)}² × {d}; height = volume ÷ ({L} × {B}) (5 marks).')


def c14s4_case(r):
    rr, h = r.choice([(7, 10), (3.5, 8), (14, 5)])
    V = PI * Fr(rr) ** 2 * h
    cup = r.choice([150, 200, 250])
    return Q((f'A cylindrical milk container in a dairy has radius {num(rr)} cm and height {h} cm (π = 22/7). (i) Find its capacity in cm³. (ii) Convert it to litres. '
              f'(iii) How many full cups of {cup} mL can be filled from it? (iv) If milk costs ₹60 per litre, find the value of a full container.'),
             f'(i) {pistr(V)} cm³ (ii) {num(float(V) / 1000, 3)} L (iii) {int(V // cup)} cups (iv) {inr(round(float(V) / 1000 * 60, 2))}', '1 mark each part.')


FAMILIES = {
    S + '11-st1': [F('C1', 'D2', 'mcq', c11s1_mcq), F('C1', 'D1', 'short', c11s1_trace), F('C2', 'D2', 'explain', c11s1_explain), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c11s1_digitsum), F('C3', 'D3', 'numerical', c11s1_collatz), F('C4', 'D3', 'case', c11s1_case)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_mcq), F('C1', 'D1', 'short', c11s2_lcm), F('C2', 'D2', 'explain', c11s2_explain), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s2_hcf), F('C3', 'D3', 'numerical', c11s2_count), F('C3', 'D4', 'multi_step', c11s2_three), F('C4', 'D3', 'case', c11s2_case)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_mcq), F('C1', 'D1', 'short', c11s3_linear), F('C2', 'D2', 'explain', c11s3_explain), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c11s3_bubble), F('C3', 'D3', 'numerical', c11s3_binary), F('C3', 'D3', 'multi_step', c11s3_guess), F('C4', 'D4', 'case', c11s3_case)],
    S + '11-st4': [F('C1', 'D2', 'mcq', c11s4_mcq), F('C2', 'D2', 'explain', c11s4_explain), F('C2', 'D2', 'mcq', c11s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c11s4_compare),
                   F('C3', 'D2', 'numerical', c11s4_bubble_count), F('C3', 'D3', 'numerical', c11s4_compare), F('C4', 'D3', 'case', c11s4_case)],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_mcq), F('C1', 'D1', 'short', c12s1_fourth), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s1_ratio), F('C3', 'D3', 'numerical', c12s1_expr), F('C4', 'D3', 'case', c12s1_case)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s2_mcq), F('C1', 'D1', 'short', c12s2_adj), F('C2', 'D2', 'explain', c12s2_explain), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s2_expr), F('C3', 'D3', 'numerical', c12s2_diag), F('C3', 'D4', 'multi_step', c12s2_rhombus), F('C4', 'D3', 'case', c12s2_case),
                   F('C4', 'D4', 'long', c12s2_explain)],
    S + '12-st3': [F('C1', 'D2', 'mcq', c12s3_mcq), F('C2', 'D2', 'explain', c12s3_check), F('C2', 'D3', 'mcq', c12s3_ar, kinds=('ar',)), F('C3', 'D1', 'short', c12s3_check),
                   F('C3', 'D2', 'explain', c12s3_explain), F('C3', 'D3', 'numerical', c12s3_coord), F('C4', 'D3', 'case', c12s3_case)],
    S + '12-st4': [F('C1', 'D2', 'mcq', c12s4_mcq), F('C1', 'D1', 'short', c12s4_half), F('C2', 'D2', 'explain', c12s4_explain), F('C2', 'D3', 'mcq', c12s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s4_perim), F('C3', 'D3', 'numerical', c12s4_half), F('C3', 'D4', 'multi_step', c12s4_trap), F('C4', 'D3', 'case', c12s4_case),
                   F('C4', 'D4', 'long', c12s4_trap)],
    S + '13-st1': [F('C1', 'D2', 'mcq', c13s1_mcq), F('C1', 'D1', 'short', c13s1_abc), F('C2', 'D2', 'explain', c13s1_explain), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c13s1_form), F('C3', 'D3', 'short', c13s1_form), F('C4', 'D3', 'case', c13s1_case)],
    S + '13-st2': [F('C1', 'D2', 'mcq', c13s2_mcq), F('C1', 'D1', 'short', c13s2_check), F('C2', 'D2', 'explain', c13s2_explain), F('C2', 'D2', 'mcq', c13s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c13s2_k), F('C3', 'D3', 'short', c13s2_find), F('C4', 'D3', 'case', c13s2_case)],
    S + '13-st3': [F('C1', 'D2', 'mcq', c13s3_mcq), F('C1', 'D1', 'short', c13s3_table), F('C2', 'D2', 'explain', c13s3_explain), F('C2', 'D3', 'mcq', c13s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c13s3_intercepts), F('C3', 'D3', 'numerical', c13s3_intercepts), F('C3', 'D4', 'multi_step', c13s3_area), F('C4', 'D3', 'case', c13s3_case),
                   F('C4', 'D4', 'long', c13s3_area)],
    S + '13-st4': [F('C1', 'D2', 'mcq', c13s4_mcq), F('C1', 'D1', 'short', c13s4_eq), F('C2', 'D2', 'explain', c13s4_explain), F('C2', 'D3', 'mcq', c13s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'short', c13s4_meet), F('C3', 'D3', 'numerical', c13s4_read), F('C4', 'D3', 'case', c13s4_case)],
    S + '14-st1': [F('C1', 'D2', 'mcq', c14s1_mcq), F('C1', 'D1', 'short', c14s1_cube), F('C2', 'D2', 'explain', c14s1_explain), F('C2', 'D3', 'mcq', c14s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c14s1_cuboid), F('C3', 'D3', 'numerical', c14s1_cyl), F('C4', 'D3', 'multi_step', c14s1_room, gap='G7'), F('C4', 'D4', 'case', c14s1_case)],
    S + '14-st2': [F('C1', 'D2', 'mcq', c14s2_mcq), F('C1', 'D1', 'short', c14s2_slant), F('C2', 'D2', 'explain', c14s2_explain), F('C2', 'D3', 'mcq', c14s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c14s2_csa), F('C3', 'D3', 'numerical', c14s2_vol), F('C3', 'D4', 'multi_step', c14s2_tsa), F('C4', 'D3', 'case', c14s2_tent),
                   F('C4', 'D4', 'case', c14s2_tent, gap='G7')],
    S + '14-st3': [F('C1', 'D2', 'mcq', c14s3_mcq), F('C1', 'D1', 'short', c14s3_sa), F('C2', 'D2', 'explain', c14s3_explain), F('C2', 'D3', 'mcq', c14s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'short', c14s3_ratio), F('C3', 'D2', 'numerical', c14s3_vol), F('C3', 'D3', 'numerical', c14s3_hemi), F('C3', 'D4', 'multi_step', c14s3_balloon),
                   F('C4', 'D3', 'case', c14s3_case_fix), F('C4', 'D4', 'long', c14s3_balloon)],
    S + '14-st4': [F('C1', 'D2', 'mcq', c14s4_mcq), F('C1', 'D1', 'short', c14s4_litres), F('C2', 'D2', 'explain', c14s4_explain), F('C2', 'D3', 'mcq', c14s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c14s4_recast), F('C3', 'D3', 'numerical', c14s4_cones), F('C4', 'D3', 'case', c14s4_case), F('C4', 'D4', 'long', c14s4_well, gap='G7'),
                   F('C4', 'D5', 'long', c14s4_well, gap='G7')],
}
