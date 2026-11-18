"""CBSE class 11 Applied Mathematics (241) families, chapters 1-4, plus shared helpers for _b and _c.

Topics shared with NCERT Mathematics XI (sets, sequences, limits, P&C, probability, statistics, lines,
conics) reuse the validated cbse-g11-maths families (copied Family objects; any variant that mentions a
trigonometric function is rejected, since Applied Mathematics has no trigonometry). Everything else is
written here; all answers are computed in code.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import itertools
import math
import re
from fractions import Fraction as Fr

from qbank import F, ar, mcq, num, sup, frac, name, two_names, inr, CITIES, GIRLS, BOYS  # noqa: F401
from g11_physics_util import pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq, sig  # noqa: F401
from g11_maths_a import Q, fs, poly, lin, setstr, ordn  # noqa: F401
import g11_maths_a
import g11_maths_b
import g11_maths_c

S = 'cbse-g11-applied-maths-ch'

# ---------------------------------------------------------------- reuse of cbse-g11-maths families

_G11 = {}
for _m in (g11_maths_a, g11_maths_b, g11_maths_c):
    _G11.update(_m.FAMILIES)

_TRIG = re.compile(r'\b(sin|cos|tan|cot|sec|cosec)\b|π|radian|°')


def _notrig(g0):
    def gen(r):
        v = g0(r)
        txt = ' '.join([v['stem'], v['answer'], v['key']] + [str(o) for o in v.get('options') or []])
        if _TRIG.search(txt):
            raise ValueError('trigonometry is not in Applied Mathematics')
        return v
    return gen


def reuse(key: str, skip=()) -> list:
    """Fresh copies of the cbse-g11-maths families of subtopic key (e.g. '08-st2'), minus indices in skip."""
    return [dataclasses.replace(f, gen=_notrig(f.gen), used=0, exhausted=False, st='')
            for i, f in enumerate(_G11['cbse-g11-maths-ch' + key]) if i not in skip]


# ---------------------------------------------------------------- small helpers

def mixed(x: Fr) -> str:
    """Fraction as a mixed number: 16 4/11."""
    x = Fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    w, rem = divmod(x.numerator, x.denominator)
    return f'{w} {rem}/{x.denominator}' if w else f'{rem}/{x.denominator}'


def d1(x: float) -> str:
    return num(round(x, 2), 2)


def nd(ans: str, cands) -> list:
    out = []
    for c in cands:
        c = str(c)
        if c != ans and c not in out:
            out.append(c)
    return out


WD = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def dstr(d: dt.date) -> str:
    return f'{d.day} {MONTHS[d.month - 1]} {d.year}'


def wday(d: dt.date) -> str:
    return WD[d.weekday()]


def wd_dis(ans: str, r) -> list:
    i = WD.index(ans)
    return [WD[(i + k) % 7] for k in (1, -1, 2)]


def leap(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


# ======================================================== ch01 Numbers, quantification and numerical applications
# st1 binary numbers

def b2(n: int) -> str:
    return bin(n)[2:]


def c1s1_place(r):
    k = r.randint(2, 7)
    return mcq(f'In a binary numeral, the place value of a 1 written in the {ordn(k + 1)} position from the right is',
               str(2 ** k), [str(2 ** (k + 1)), str(2 * k), str(10 ** k)], f'Positions carry 2⁰, 2¹, 2², … from the right, so the {ordn(k + 1)} place is 2{sup(k)} = {2 ** k}.', r)


def c1s1_valid(r):
    n = r.randint(9, 120)
    good = b2(n)
    bad = []
    while len(bad) < 3:
        s = list(b2(r.randint(9, 120)))
        s[r.randrange(len(s))] = r.choice('23')
        if ''.join(s) not in bad:
            bad.append(''.join(s))
    return mcq('Which of the following is a valid binary numeral?', good, bad, f'A binary numeral uses only the digits 0 and 1; only {good} qualifies.', r)


def c1s1_d2b(r):
    n = r.randint(11, 250)
    ans = f'({b2(n)})₂'
    return Q(f'Convert the decimal number {n} into a binary number.', ans,
             f'Divide by 2 repeatedly and read the remainders from bottom to top: {n} = {ans}.',
             [f'({b2(n)[::-1]})₂', f'({b2(n + 1)})₂', f'({b2(n - 1)})₂', f'({b2(n + 2)})₂'])


def c1s1_b2d(r):
    n = r.randint(19, 255)
    s = b2(n)
    terms = ' + '.join(f'{c}×2{sup(len(s) - 1 - i)}' for i, c in enumerate(s) if c == '1')
    return Q(f'Convert ({s})₂ into a decimal number.', str(n), f'{terms} = {n}.', [str(n + 1), str(n - 2), str(int(s[::-1], 2)) if int(s[::-1], 2) != n else str(n + 4)])


def c1s1_add(r):
    a, b = r.randint(9, 60), r.randint(9, 60)
    op = r.choice(['+', '−'])
    if op == '−' and a < b:
        a, b = b, a
    if a == b:
        a += 3
    res = a + b if op == '+' else a - b
    return Q(f'Find ({b2(a)})₂ {op} ({b2(b)})₂ and give the answer in binary. Verify in decimal.', f'({b2(res)})₂',
             f'Column {"addition" if op == "+" else "subtraction"} with carries/borrows in base 2 gives ({b2(res)})₂. Check: {a} {op} {b} = {res}.',
             [f'({b2(res + 1)})₂', f'({b2(res - 1)})₂', f'({b2(res + 2)})₂'])


FRACS = [(Fr(1, 2), '1'), (Fr(1, 4), '01'), (Fr(3, 4), '11'), (Fr(1, 8), '001'), (Fr(3, 8), '011'), (Fr(5, 8), '101'),
         (Fr(7, 8), '111'), (Fr(5, 16), '0101'), (Fr(13, 16), '1101'), (Fr(3, 16), '0011')]


def c1s1_frac(r):
    n = r.randint(2, 30)
    f, bits = r.choice(FRACS)
    dec = num(float(n + f), 4)
    if r.random() < 0.5:
        return Q(f'Convert {dec} into a binary number.', f'({b2(n)}.{bits})₂',
                 f'Integer part: {n} = ({b2(n)})₂ by repeated division. Fractional part {num(float(f), 4)}: multiply by 2 repeatedly and record the integer parts: .{bits}. So {dec} = ({b2(n)}.{bits})₂.')
    return Q(f'Convert ({b2(n)}.{bits})₂ into a decimal number.', dec,
             f'Integer part ({b2(n)})₂ = {n}; fractional part uses 2⁻¹, 2⁻², …: .{bits} = {num(float(f), 4)}. Total {dec}.')


def c1s1_mult(r):
    a, b = r.randint(5, 15), r.randint(3, 7)
    return Q(f'Multiply ({b2(a)})₂ by ({b2(b)})₂. Give the product in binary and check your answer by converting to decimal.', f'({b2(a * b)})₂',
             f'Shift-and-add: write ({b2(a)})₂ shifted for each 1 in ({b2(b)})₂ and add (2). Check: {a} × {b} = {a * b} = ({b2(a * b)})₂ (1).')


def c1s1_explain(r):
    n = r.randint(20, 99)
    return {'stem': f'Explain why the decimal number {n} needs {len(b2(n))} binary digits (bits).', 'answer': f'2{sup(len(b2(n)) - 1)} = {2 ** (len(b2(n)) - 1)} ≤ {n} < 2{sup(len(b2(n)))} = {2 ** len(b2(n))}, so {n} = ({b2(n)})₂ has {len(b2(n))} bits.',
            'key': f'Highest power of 2 not exceeding {n} is 2{sup(len(b2(n)) - 1)} (1); hence {len(b2(n))} places, ({b2(n)})₂ (1).'}


def c1s1_ar(r):
    n = r.randint(9, 63)
    s = b2(n)
    if r.random() < 0.5:
        return ar(f'({s})₂ = {n}.', 'Each binary digit is multiplied by the power of 2 for its position and the products are added.', 'a', f'Expanding ({s})₂ in powers of 2 gives {n}; R is the method used.')
    w = n + r.choice([1, 2, -1, 4])
    return ar(f'({s})₂ = {w}.', 'Each binary digit is multiplied by the power of 2 for its position and the products are added.', 'd', f'A is false: ({s})₂ = {n}. R is true.')


def c1s1_case(r):
    who = name(r)
    a, b = r.randint(20, 90), r.randint(20, 90)
    return {'stem': (f'{who} is learning how a computer stores whole numbers in 8-bit memory cells.\n'
                     f'(i) What is the largest number that can be stored in 8 bits? (1)\n(ii) Write {a} as an 8-bit binary number. (1)\n'
                     f'(iii) The cell holds ({b2(b).zfill(8)})₂. What decimal number is stored? Add it to {a} and give the sum in binary. (2)'),
            'answer': f'(i) 255 = (11111111)₂ (ii) {b2(a).zfill(8)} (iii) {b}; sum {a + b} = ({b2(a + b)})₂',
            'key': f'(i) 2⁸ − 1 = 255 (1). (ii) {a} = ({b2(a)})₂ padded to 8 bits (1). (iii) {b} (1); {a} + {b} = {a + b} = ({b2(a + b)})₂ (1).'}


c1s1_tf = tf_mcq('the binary number system', [
    'The binary system has base 2 and uses only the digits 0 and 1.', 'The place values in a binary numeral are powers of 2.',
    'A binary digit is called a bit.', 'Every natural number has a unique binary representation.', '(1000)₂ = 8.'],
    ['The binary system has base 10.', 'The digit 2 is allowed in a binary numeral.', '(1000)₂ = 1000.', 'Place values in a binary numeral are powers of 10.',
     'To convert decimal to binary we divide repeatedly by 10.'])

# st2 indices, logarithms and antilogarithms

LOGS = {2: 3010, 3: 4771, 5: 6990, 7: 8451}   # log10 in ten-thousandths (as in log tables)


def lg(n_parts: dict) -> int:
    return sum(LOGS[p] * e for p, e in n_parts.items())


def l4(v: int) -> str:
    """ten-thousandths to text, e.g. 13802 -> 1.3802"""
    s = '−' if v < 0 else ''
    v = abs(v)
    return f'{s}{v // 10000}.{v % 10000:04d}'


POWBASES = [(4, 2, 2), (8, 2, 3), (9, 3, 2), (16, 2, 4), (25, 5, 2), (27, 3, 3), (32, 2, 5), (64, 2, 6), (81, 3, 4),
            (125, 5, 3), (243, 3, 5), (625, 5, 4)]


def c1s2_index(r):
    b, c, k = r.choice(POWBASES)
    j = r.choice([x for x in range(-3, 4) if x != 0 and x != k])
    e = Fr(j, k)
    val = Fr(c) ** j
    es = fs(e)
    return Q(f'Evaluate ({b})^({es}).', fs(val), f'{b} = {c}{sup(k)}, so ({c}{sup(k)})^({es}) = {c}^{j} = {fs(val)}.',
             [fs(Fr(b) * e) if (Fr(b) * e) != val else fs(val + 1), fs(1 / val), fs(Fr(c) ** (j + (1 if j > 0 else -1)))])


def c1s2_loglaw(r):
    b = r.choice([10, 2, 3])
    k = r.choice([1, 2, 3]) if b == 10 else r.choice([2, 3, 4, 5])
    T = b ** k
    for _ in range(200):
        m, n = r.randint(2, 60), r.randint(2, 60)
        if (m * n) % T == 0 and m * n // T > 1 and m * n // T not in (m, n):
            p = m * n // T
            break
    else:
        raise ValueError
    base = '' if b == 10 else f'_{b}'
    lb = 'log' + ('' if b == 10 else f'₍{b}₎')
    return Q(f'Without using tables, evaluate {lb} {m} + {lb} {n} − {lb} {p}.', str(k),
             f'{lb} ({m} × {n} / {p}) = {lb} {T} = {k} (product and quotient laws).', [str(k + 1), str(k - 1) if k > 1 else str(k + 2), str(k + 2)])


def c1s2_known(r):
    parts = {}
    for p in (2, 3, 5, 7):
        if r.random() < 0.55:
            parts[p] = r.randint(1, 3)
    if not parts:
        parts = {r.choice([2, 3]): r.randint(2, 4)}
    if 2 in parts and 5 in parts:
        del parts[5]
    N = 1
    for p, e in parts.items():
        N *= p ** e
    if N in (2, 3, 5, 7) or N > 5000:
        raise ValueError
    shift = r.choice([0, 0, 1, -1])
    val = lg(parts) + shift * 10000
    Nt = num(N * 10 ** shift, 4) if shift >= 0 else num(N / 10, 4)
    given = ', '.join(f'log {p} = 0.{LOGS[p]:04d}' for p in sorted(parts))
    fac = ' × '.join(f'{p}{sup(e) if e > 1 else ""}' for p, e in sorted(parts.items())) + (' × 10' if shift == 1 else (' ÷ 10' if shift == -1 else ''))
    return Q(f'Given {given}, find log {Nt}.', l4(val), f'{Nt} = {fac}; log {Nt} = {" + ".join(f"{e}(0.{LOGS[p]:04d})" for p, e in sorted(parts.items()))}{" + 1" if shift == 1 else (" − 1" if shift == -1 else "")} = {l4(val)}.',
             [l4(val + 10000), l4(val - 3010), l4(val + 4771)])


ANTI = [(2, 3010), (3, 4771), (4, 6020), (5, 6990), (6, 7781), (7, 8451), (8, 9030), (9, 9542)]


def c1s2_antilog(r):
    d, m = r.choice(ANTI)
    k = r.randint(0, 4)
    x = d * 10 ** k
    hint = {2: 'log 2 = 0.3010', 3: 'log 3 = 0.4771', 4: 'log 2 = 0.3010', 5: 'log 2 = 0.3010', 6: 'log 2 = 0.3010 and log 3 = 0.4771',
            7: 'log 7 = 0.8451', 8: 'log 2 = 0.3010', 9: 'log 3 = 0.4771'}[d]
    return Q(f'If log x = {k}.{m:04d}, find x. (Use {hint}.)', f'{x:,}'.replace(',', ''),
             f'Characteristic {k} ⇒ x has {k + 1} digit(s) before the decimal point; mantissa 0.{m:04d} = log {d}. So x = antilog = {d} × 10{sup(k)} = {x}.',
             [str(d * 10 ** (k + 1)), str(d * 10 ** max(k - 1, 0)) if k else str(d + 1), str((d + 1) * 10 ** k)])


def c1s2_digits(r):
    b = r.choice([2, 3])
    n = r.randint(15, 80)
    lgv = LOGS[b]
    digits = (n * lgv) // 10000 + 1
    if digits != len(str(b ** n)):
        raise ValueError
    return Q(f'Using log {b} = 0.{lgv:04d}, find the number of digits in {b}{sup(n)}.', str(digits),
             f'log {b}{sup(n)} = {n} × 0.{lgv:04d} = {l4(n * lgv)}; characteristic {digits - 1}, so the number has {digits} digits.',
             [str(digits - 1), str(digits + 1), str(n)])


def c1s2_expeq(r):
    c = r.choice([2, 3, 5])
    x = r.randint(-2, 5)
    p = r.choice([1, 2, 3])
    q = r.randint(-3, 3)
    s = p * x + q
    if s < -3 or c ** abs(s) > 3200 or s == 0:
        raise ValueError
    rhs = str(c ** s) if s > 0 else f'1/{c ** (-s)}'
    lhs = f'{c}^({lin(p, q)})'
    return Q(f'Solve for x: {lhs} = {rhs}.', f'x = {x}', f'Write {rhs} = {c}^{s}; equate exponents: {lin(p, q)} = {s} ⇒ x = {x}.',
             [f'x = {x + 1}', f'x = {x - 1}', f'x = {fs(Fr(s, p))}' if Fr(s, p) != x else f'x = {x + 2}'])


def c1s2_logbase(r):
    x = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    k = r.choice([2, 3]) if x <= 10 else 2
    N = x ** k
    if r.random() < 0.5:
        return Q(f'If log₍ₓ₎ {N} = {k}, find x.', str(x), f'x{sup(k)} = {N} ⇒ x = {x} (base must be positive).', [str(x * x), str(x + 1), str(N // x)])
    return Q(f'Find the value of log₍{x}₎ {N}.', str(k), f'{x}{sup(k)} = {N}, so log₍{x}₎ {N} = {k}.', [str(k + 1), str(N // x), str(k - 1)])


def c1s2_prove(r):
    k = r.choice([3, 4, 5, 6])
    return {'stem': f'If log ((a + b)/{k}) = ½(log a + log b), prove that a/b + b/a = {k * k - 2}.',
            'answer': f'(a + b)/{k} = √(ab) ⇒ (a + b)² = {k * k}ab ⇒ a² + b² = {k * k - 2}ab ⇒ a/b + b/a = {k * k - 2}.',
            'key': f'½(log a + log b) = log √(ab) (1); equate arguments (1); square and expand (1); divide by ab (1); conclusion (1).'}


def c1s2_case(r):
    who = name(r)
    d, m = r.choice(ANTI[:4] + ANTI[5:])
    k = r.randint(1, 3)
    return {'stem': (f'{who} uses logarithms to handle large numbers in a science project. She notes that log x = {k}.{m:04d}.\n'
                     f'(i) Write the characteristic and the mantissa of log x. (1)\n(ii) How many digits does the integral part of x have? (1)\n'
                     f'(iii) Find x and hence log (x²). (2)').replace('She', 'She' if who in GIRLS else 'He'),
            'answer': f'(i) characteristic {k}, mantissa 0.{m:04d} (ii) {k + 1} (iii) x = {d * 10 ** k}; log x² = {l4(2 * (k * 10000 + m))}',
            'key': f'(i) integral and decimal parts (1). (ii) characteristic + 1 = {k + 1} (1). (iii) antilog: {d} × 10{sup(k)} (1); log x² = 2 log x (1).'}


def c1s2_explain(r):
    a, b = r.sample([2, 3, 5, 7], 2)
    return {'stem': f'State the product and power laws of logarithms and use them to express log ({a}² × {b}³) in terms of log {a} and log {b}.',
            'answer': f'log (mn) = log m + log n; log mᵏ = k log m; so log ({a}² × {b}³) = 2 log {a} + 3 log {b}.',
            'key': 'Product law (½), power law (½), correct expression (1).'}


def c1s2_ar(r):
    b, k = r.choice([(2, 5), (3, 4), (5, 3), (10, 3), (4, 3), (2, 7)])
    if r.random() < 0.6:
        return ar(f'log₍{b}₎ {b ** k} = {k}.', 'log₍a₎ aⁿ = n for a > 0, a ≠ 1.', 'a', f'{b ** k} = {b}{sup(k)}, so R gives A.')
    return ar(f'log₍{b}₎ {b ** k} = {b ** k // b}.', 'log₍a₎ aⁿ = n for a > 0, a ≠ 1.', 'd', f'A is false: the value is {k}. R is true.')


c1s2_tf = tf_mcq('logarithms', [
    'log₍a₎ 1 = 0 for every admissible base a.', 'log₍a₎ a = 1.', 'log (mn) = log m + log n.', 'log (m/n) = log m − log n.',
    'The logarithm of a negative number is not defined in real numbers.', 'log m = log₍e₎ m / log₍e₎ 10 (change of base).'],
    ['log (m + n) = log m + log n.', 'log (mn) = log m × log n.', 'log₍a₎ 1 = 1.', 'log 0 = 0.', 'log (m/n) = log m / log n.'])

# st3 clock and calendar


def hand_angle(h, m):
    a = abs(30 * h - Fr(11, 2) * m)
    a = a % 360
    return min(a, 360 - a)


def c1s3_angle(r):
    h = r.randint(1, 12)
    m = r.choice(range(5, 60, 5)) if r.random() < 0.6 else r.randint(1, 59)
    a = hand_angle(h % 12, m)
    t = f'{h}:{m:02d}'
    return Q(f'Find the angle between the hour hand and the minute hand of a clock at {t}.', f'{mixed(a)}°',
             f'Angle = |30H − (11/2)M| = |30×{h % 12} − 5.5×{m}| = {mixed(abs(30 * (h % 12) - Fr(11, 2) * m))}°; take the smaller angle: {mixed(a)}°.',
             [f'{mixed(abs(a - 30) if a >= 30 else a + 30)}°', f'{mixed(360 - a)}°' if a != 180 else '90°', f'{mixed(abs(30 * (h % 12) - 6 * m) % 360)}°'])


def c1s3_coincide(r):
    h = r.randint(1, 10)
    kind = r.choice(['together', 'right', 'opposite'])
    if kind == 'together':
        M = Fr(60 * h, 11)
        txt = 'together (coincide)'
    else:
        target = 90 if kind == 'right' else 180
        cands = []
        for k in range(-3, 4):
            for sg in (1, -1):
                Mx = Fr(2 * (30 * h + sg * target + 360 * k), 11)
                if 0 < Mx < 60:
                    cands.append(Mx)
        M = min(cands)
        txt = 'at right angles' if kind == 'right' else 'in opposite directions (in a straight line, 180° apart)'
    return Q(f'At what time between {h} and {h + 1} o\'clock will the hands of a clock {"first be " if kind != "together" else "be "}{txt}?',
             f'{mixed(M)} minutes past {h}',
             f'Minute hand gains 5.5° per minute on the hour hand; at {h} o\'clock the gap is {30 * h}°. Solve 5.5M − {30 * h} = required angle: M = {mixed(M)} min past {h}.',
             [f'{mixed(M + 1)} minutes past {h}', f'{mixed(Fr(60 * h, 12))} minutes past {h}' if Fr(60 * h, 12) != M else f'{mixed(M - 1)} minutes past {h}', f'{mixed(M + Fr(5, 11) * 2)} minutes past {h}'])


def c1s3_leapmcq(r):
    lp = r.choice([y for y in range(1600, 2500, 4) if leap(y)])
    non = set()
    while len(non) < 3:
        y = r.choice([r.choice([1700, 1800, 1900, 2100, 2200, 2300]), r.randint(1801, 2399)])
        if not leap(y):
            non.add(y)
    return mcq('Which of the following years is a leap year?', str(lp), [str(y) for y in non],
               f'{lp} is divisible by 4{" and, being a century year, by 400" if lp % 100 == 0 else " and is not a century year"}. Century years such as 1900 are leap years only if divisible by 400.', r)


def c1s3_oddmcq(r):
    return pool_mcq([
        ('The number of odd days in an ordinary year is', '1', ['2', '0', '3'], '365 = 52 × 7 + 1.'),
        ('The number of odd days in a leap year is', '2', ['1', '0', '3'], '366 = 52 × 7 + 2.'),
        ('The number of odd days in 100 years is', '5', ['1', '3', '0'], '100 years have 24 leap years: 76 + 48 = 124 odd days ≡ 5.'),
        ('The number of odd days in 400 years is', '0', ['1', '5', '3'], '400 years: 4 × 5 + 1 = 21 ≡ 0.'),
        ('The minute hand of a clock moves through', '6° per minute', ['0.5° per minute', '30° per minute', '1° per minute'], '360° in 60 minutes.'),
        ('The hour hand of a clock moves through', '0.5° per minute', ['6° per minute', '30° per minute', '1° per minute'], '30° in 60 minutes.'),
        ('In 12 hours, the hands of a clock coincide', '11 times', ['12 times', '24 times', '22 times'], 'They coincide every 65 5/11 minutes, 11 times in 12 hours.'),
        ('In a day (24 hours), the hands of a clock are at right angles', '44 times', ['48 times', '24 times', '22 times'], '22 times in 12 hours.'),
        ('The number of odd days in 200 years is', '3', ['5', '1', '0'], '2 × 5 = 10 ≡ 3.'),
        ('The number of odd days in 300 years is', '1', ['3', '5', '0'], '3 × 5 = 15 ≡ 1.'),
    ])(r)


def c1s3_after(r):
    d0 = r.choice(WD)
    n = r.randint(20, 400)
    ans = WD[(WD.index(d0) + n) % 7]
    return Q(f'Today is {d0}. What day of the week will it be after {n} days?', ans, f'{n} = 7 × {n // 7} + {n % 7}; {n % 7} odd day(s) after {d0} is {ans}.', wd_dis(ans, r))


def c1s3_date(r):
    y = r.randint(2015, 2032)
    a = dt.date(y, 1, 1)
    b = a + dt.timedelta(days=r.randint(40, 360))
    ans = wday(b)
    days = (b - a).days
    return Q(f'1 January {y} was a {wday(a)}. On what day of the week does {b.day} {MONTHS[b.month - 1]} {y} fall?', ans,
             f'{"Leap" if leap(y) else "Ordinary"} year. Days after 1 January = {days} = 7 × {days // 7} + {days % 7}; {days % 7} odd days after {wday(a)} gives {ans}.',
             wd_dis(ans, r))


def c1s3_history(r):
    d = dt.date(r.randint(1901, 2030), r.randint(1, 12), r.randint(1, 28))
    y = d.year
    lp = (y - 1) // 4 - (y - 1) // 100 + (y - 1) // 400
    ody = ((y - 1) + lp) % 7
    doy = d.timetuple().tm_yday
    tot = (ody + doy) % 7
    names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    ans = names[tot]
    assert ans == wday(d)
    return Q(f'Using the method of odd days, find the day of the week on {dstr(d)}.', ans,
             f'Odd days in the first {y - 1} years = ({y - 1} + {lp} leap years) mod 7 = {ody}. Days of {y} up to {dstr(d)} = {doy} ≡ {doy % 7}. Total ≡ {tot} ⇒ {ans} (0 = Sunday, 1 = Monday, …).',
             wd_dis(ans, r))


def c1s3_repeat(r):
    y = r.randint(2009, 2031)
    z = y + 1
    while not (dt.date(z, 1, 1).weekday() == dt.date(y, 1, 1).weekday() and leap(z) == leap(y)):
        z += 1
    return Q(f'The calendar of the year {y} can be used again in which year (the next year with an identical calendar)?', str(z),
             f'We need the same starting day and the same type of year ({"leap" if leap(y) else "ordinary"}). Counting odd days from {y}: the total is a multiple of 7 first at {z}, which is also {"a leap" if leap(z) else "an ordinary"} year.',
             nd(str(z), [str(y + 7), str(y + 6), str(y + 11), str(y + 28), str(z + 1)]))


def c1s3_gain(r):
    g = r.choice([2, 3, 4, 5, 6])
    days = r.choice([1, 2, 3])
    extra = r.choice([0, 6, 12])
    hours = 24 * days + extra
    gained = Fr(g * hours, 24)
    if gained.denominator != 1:
        raise ValueError
    start = dt.datetime(2026, 3, 2, 8, 0)
    true_t = start + dt.timedelta(hours=hours)
    shown = true_t + dt.timedelta(minutes=int(gained))
    f = lambda t: t.strftime('%I:%M %p').lstrip('0').replace('AM', 'a.m.').replace('PM', 'p.m.') + f' on {wday(t.date())}'
    return Q(f'A clock is set right at 8:00 a.m. on Monday. It gains {g} minutes in every 24 hours. What time will it show at {f(true_t)} (true time)?',
             f(shown), f'Time elapsed = {hours} h; gain = {g} × {hours}/24 = {int(gained)} min. Clock shows {f(true_t)} + {int(gained)} min = {f(shown)}.',
             [f(true_t - dt.timedelta(minutes=int(gained))), f(true_t + dt.timedelta(minutes=g)), f(true_t + dt.timedelta(minutes=int(gained) * 2))])


def c1s3_ar(r):
    y = r.choice([1700, 1800, 1900, 2100, 2200, 2000, 2400, 1600, 2024, 2028, 1996, 2012])
    R = 'A century year is a leap year only if it is divisible by 400.'
    if y % 100 == 0 and not leap(y):
        return ar(f'{y} is a leap year.', R, 'd', f'A is false: {y} is a century year not divisible by 400. R is true.')
    if y % 100 == 0:
        return ar(f'{y} is a leap year.', R, 'a', f'{y} is a century year divisible by 400, so R explains A.')
    return ar(f'{y} is a leap year.', R, 'b', f'{y} is a leap year because it is divisible by 4 and is not a century year; R is true but is about century years.')


def c1s3_explain(r):
    n = r.choice([500, 600, 700, 800, 900, 1100, 1200, 1300, 1500, 1600, 1700, 1800, 1900, 2000])
    lp = n // 4 - n // 100 + n // 400
    return {'stem': f'Find the number of odd days in the first {n} years (from 1 AD). Explain your method.',
            'answer': f'{(n + lp) % 7}', 'key': f'{n} years contain {lp} leap years (divisible by 4, except century years not divisible by 400) (1). Odd days = {n} − {lp} + 2×{lp} = {n + lp} ≡ {(n + lp) % 7} (mod 7) (1).'}


def c1s3_case(r):
    who = name(r)
    y = r.randint(2024, 2031)
    a = dt.date(y, 1, 26)
    b = dt.date(y, 8, 15)
    c = dt.date(y, 10, 2)
    return {'stem': (f'{who} is preparing the school activity calendar for {y}. Republic Day, 26 January {y}, falls on a {wday(a)}.\n'
                     f'(i) Is {y} a leap year? (1)\n(ii) On what day does Independence Day, 15 August {y}, fall? (1)\n'
                     f'(iii) Find the day of the week of 2 October {y}, and the number of days from 15 August to 2 October (both days excluded). (2)'),
            'answer': f'(i) {"Yes" if leap(y) else "No"} (ii) {wday(b)} (iii) {wday(c)}; {(c - b).days - 1} days',
            'key': f'(i) divisibility by 4 (1). (ii) {(b - a).days} days later ≡ {(b - a).days % 7} odd days (1). (iii) {(c - b).days} days ≡ {(c - b).days % 7} odd days → {wday(c)} (1); {(c - b).days - 1} days between (1).'}


# st4 time, speed and distance

SPEEDS = [(36, 10), (54, 15), (72, 20), (90, 25), (108, 30), (18, 5), (45, 12.5), (63, 17.5), (81, 22.5)]


def c1s4_conv(r):
    k, m = r.choice(SPEEDS)
    if r.random() < 0.5:
        return Q(f'Express a speed of {k} km/h in m/s.', f'{num(m)} m/s', f'{k} × 5/18 = {num(m)} m/s.', [f'{num(k * 18 / 5)} m/s', f'{num(m * 2)} m/s', f'{num(k / 3.6 + 2.5)} m/s'])
    return Q(f'Express a speed of {num(m)} m/s in km/h.', f'{k} km/h', f'{num(m)} × 18/5 = {k} km/h.', [f'{num(m * 5 / 18, 2)} km/h', f'{k + 18} km/h', f'{num(m * 3)} km/h'])


def c1s4_pole(r):
    k, m = r.choice(SPEEDS[:5])
    t = r.randint(6, 30)
    L = int(m * t)
    if r.random() < 0.5:
        return Q(f'A train {L} m long runs at {k} km/h. How long does it take to pass a telegraph pole?', f'{t} s', f'Speed = {k} × 5/18 = {num(m)} m/s; time = {L}/{num(m)} = {t} s.',
                 [f'{t * 2} s', f'{num(L / k, 2)} s', f'{t + 5} s'])
    return Q(f'A train running at {k} km/h passes a signal post in {t} seconds. Find the length of the train.', f'{L} m', f'Length = speed × time = {num(m)} m/s × {t} s = {L} m.',
             [f'{k * t} m', f'{L // 2} m', f'{L + 50} m'])


def c1s4_platform(r):
    k, m = r.choice(SPEEDS[:5])
    t = r.randint(15, 45)
    total = int(m * t)
    L = r.randrange(100, total - 50, 10) if total > 160 else None
    if not L:
        raise ValueError
    P = total - L
    return Q(f'A train {L} m long, running at {k} km/h, crosses a platform in {t} seconds. Find the length of the platform.', f'{P} m',
             f'Distance covered = train + platform = {num(m)} × {t} = {total} m; platform = {total} − {L} = {P} m.',
             [f'{total} m', f'{P + L // 2} m', f'{abs(P - 40) or 40} m'])


def c1s4_two(r):
    (k1, m1), (k2, m2) = r.sample(SPEEDS[:5], 2)
    L1, L2 = r.randrange(100, 300, 10), r.randrange(100, 300, 10)
    same = r.random() < 0.5
    rel = abs(m1 - m2) if same else m1 + m2
    if rel == 0:
        raise ValueError
    t = Fr(L1 + L2) / Fr(rel).limit_denominator(4)
    return Q(f'Two trains of lengths {L1} m and {L2} m run on parallel tracks at {k1} km/h and {k2} km/h in the {"same" if same else "opposite"} direction. '
             f'How long will they take to cross each other completely?', f'{d1(float(t))} s',
             f'Relative speed = {num(m1)} {"−" if same else "+"} {num(m2)} = {num(rel)} m/s (|difference| for same direction); distance = {L1} + {L2} = {L1 + L2} m; time = {d1(float(t))} s.',
             [f'{d1((L1 + L2) / (m1 + m2 if same else abs(m1 - m2) or 1))} s', f'{d1(max(L1, L2) / rel)} s', f'{d1(float(t) * 2)} s'])


def c1s4_boat(r):
    b = r.randint(6, 20)
    s = r.randint(1, b - 2)
    t1, t2 = r.randint(2, 6), r.randint(2, 6)
    D1, D2 = (b + s) * t1, (b - s) * t2
    return Q(f'A boat goes {D1} km downstream in {t1} hours and {D2} km upstream in {t2} hours. Find the speed of the boat in still water and the speed of the stream.',
             f'{b} km/h; {s} km/h', f'Downstream speed = {D1}/{t1} = {b + s} km/h; upstream = {D2}/{t2} = {b - s} km/h. Boat = ½({b + s} + {b - s}) = {b}; stream = ½({b + s} − {b - s}) = {s}.',
             [f'{b + s} km/h; {b - s} km/h', f'{s} km/h; {b} km/h', f'{b} km/h; {2 * s} km/h'])


def c1s4_avg(r):
    x, y = r.choice([(40, 60), (30, 60), (20, 30), (36, 45), (60, 90), (12, 18), (45, 90), (50, 75), (24, 40)])
    a = Fr(2 * x * y, x + y)
    c1, c2 = r.sample(CITIES, 2)
    return Q(f'{name(r)} drives from {c1} to {c2} at {x} km/h and returns along the same road at {y} km/h. Find the average speed for the whole journey.',
             f'{mixed(a)} km/h', f'Average speed = total distance/total time = 2xy/(x + y) = 2×{x}×{y}/{x + y} = {mixed(a)} km/h.',
             [f'{mixed(Fr(x + y, 2))} km/h', f'{mixed(Fr(x * y, x + y))} km/h', f'{mixed(Fr(x + y, 2) + 2)} km/h'])


def c1s4_avg_explain(r):
    x, y = r.choice([(30, 50), (40, 60), (20, 60), (45, 90), (60, 40)])
    return {'stem': f'A cyclist covers half a route at {x} km/h and the other half at {y} km/h. Explain why the average speed is not ({x} + {y})/2 = {num((x + y) / 2)} km/h, and find it.',
            'answer': f'{mixed(Fr(2 * x * y, x + y))} km/h', 'key': f'Equal distances, not equal times, so more time is spent at the slower speed (1); average = 2xy/(x + y) = {mixed(Fr(2 * x * y, x + y))} km/h (1).'}


def _clock(tm: Fr) -> str:
    mins = int(round(tm * 60))
    hh, mm = divmod(mins, 60)
    h12 = hh if 1 <= hh <= 12 else (hh - 12 if hh > 12 else 12)
    return f'{h12}:{mm:02d} {"a.m." if hh < 12 else "p.m."}'


def c1s4_meet(r):
    v1, v2 = r.choice([(40, 50), (45, 60), (60, 75), (50, 70), (36, 54), (55, 65)])
    t = r.choice([Fr(2), Fr(5, 2), Fr(3), Fr(4), Fr(3, 2)])
    gap = r.choice([0, 1])
    D = v1 * gap + (v1 + v2) * t
    if D.denominator != 1:
        raise ValueError
    A, B = r.sample(CITIES, 2)
    h0 = r.choice([6, 7, 8, 9])
    tm = Fr(h0 + gap) + t
    when = _clock(tm)
    dist = v1 * (gap + t)
    first = f'In the first hour the first train covers {v1} km; the ' if gap else 'The '
    return Q(f'Stations {A} and {B} are {int(D)} km apart. A train leaves {A} for {B} at {h0}:00 a.m. at {v1} km/h. {"Another" if not gap else "One hour later, another"} train leaves {B} for {A} '
             f'{"at the same time " if not gap else ""}at {v2} km/h. When and where will they meet?', f'at {when}, {mixed(dist)} km from {A}',
             f'{first}remaining {mixed(D - v1 * gap)} km is closed at {v1 + v2} km/h in {mixed(t)} h. They meet at {when}, {v1} × {mixed(gap + t)} = {mixed(dist)} km from {A}.',
             [f'at {when}, {mixed(D - dist)} km from {A}', f'at {_clock(tm + 1)}, {mixed(dist)} km from {A}', f'at {when}, {mixed(D / 2)} km from {A}'])


def c1s4_late(r):
    a, b = r.choice([(4, 5), (5, 6), (3, 4), (30, 40), (40, 50), (6, 8), (10, 12), (36, 45)])
    for _ in range(100):
        D = r.randint(2, 60) * (1 if a < 20 else 5)
        T = Fr(60 * D * (b - a), a * b)
        if T.denominator == 1 and 10 <= T <= 90:
            break
    else:
        raise ValueError
    T = int(T)
    late = r.randint(2, T - 2)
    early = T - late
    usual = Fr(D, a) * 60 - late
    who = name(r)
    return Q(f'{"Walking" if a < 15 else "Driving"} at {a} km/h, {who} reaches the office {late} minutes late; at {b} km/h {who} reaches {early} minutes early. Find the distance to the office and the time it should take.',
             f'{D} km; {mixed(usual)} minutes', f'D/{a} − D/{b} = ({late} + {early})/60 h ⇒ D × {b - a}/{a * b} = {T}/60 ⇒ D = {D} km. Time at {a} km/h = {mixed(Fr(D, a) * 60)} min, so the right time is {mixed(usual)} min.',
             [f'{D * 2} km; {mixed(usual)} minutes', f'{D} km; {mixed(Fr(D, a) * 60)} minutes', f'{D + a} km; {mixed(usual + 5)} minutes'])


def c1s4_ar(r):
    k, m = r.choice(SPEEDS[:5])
    if r.random() < 0.5:
        return ar(f'A speed of {k} km/h is the same as {num(m)} m/s.', '1 km/h = 5/18 m/s.', 'a', f'{k} × 5/18 = {num(m)}; R explains A.')
    return ar('Two trains moving in the same direction cross each other faster than when moving in opposite directions.', 'In the same direction, the relative speed is the difference of the speeds.', 'd',
              'A is false: the relative speed is smaller in the same direction, so crossing takes longer. R is true.')


def c1s4_case(r):
    k1, m1 = r.choice(SPEEDS[1:5])
    L = r.randrange(150, 300, 10)
    P = r.randrange(200, 400, 10)
    t1 = Fr(L, 1) / Fr(m1)
    t2 = Fr(L + P) / Fr(m1)
    c1, c2 = r.sample(CITIES, 2)
    D = r.choice([180, 240, 270, 360, 450])
    T = Fr(D, k1)
    return {'stem': (f'An express train from {c1} to {c2} is {L} m long and runs at a steady {k1} km/h.\n'
                     f'(i) Express its speed in m/s. (1)\n(ii) How long does it take to pass a signal pole? (1)\n'
                     f'(iii) How long does it take to cross a {P} m long platform, and how long does the {D} km journey take at this speed? (2)'),
            'answer': f'(i) {num(m1)} m/s (ii) {d1(float(t1))} s (iii) {d1(float(t2))} s; {mixed(T)} h',
            'key': f'(i) × 5/18 (1). (ii) {L}/{num(m1)} (1). (iii) ({L} + {P})/{num(m1)} (1); {D}/{k1} h (1).'}


c1s4_tf = tf_mcq('time, speed and distance', [
    'To convert km/h into m/s, multiply by 5/18.', 'When two bodies move in opposite directions, their relative speed is the sum of their speeds.',
    'A train passing a pole covers a distance equal to its own length.', 'A train crossing a platform covers its own length plus the length of the platform.',
    'Speed downstream = speed of boat in still water + speed of stream.'],
    ['To convert km/h into m/s, multiply by 18/5.', 'A train passing a pole covers no distance.', 'For equal distances, the average speed is the arithmetic mean of the two speeds.',
     'Speed upstream = speed of boat in still water + speed of stream.', 'When two trains move in the same direction, the relative speed is the sum of their speeds.'])

# st5 time and work; seating arrangement; mensuration puzzles

WORK_PAIRS = [(10, 15), (12, 24), (20, 30), (15, 10), (6, 12), (8, 24), (18, 36), (12, 4), (20, 5), (30, 60), (10, 40), (14, 21), (9, 18), (24, 40)]


def c1s5_rate(r):
    a = r.randint(4, 25)
    k = r.randint(2, a - 1)
    return Q(f'{name(r)} can finish a piece of work in {a} days. What fraction of the work is done in {k} days?', fs(Fr(k, a)),
             f'One day\'s work = 1/{a}; in {k} days: {k}/{a} = {fs(Fr(k, a))}.', [fs(Fr(1, a)), fs(Fr(a - k, a)), fs(Fr(k, a + k))])


def c1s5_together(r):
    a, b = r.choice(WORK_PAIRS)
    A, B = two_names(r)
    t = Fr(a * b, a + b)
    return Q(f'{A} can do a piece of work in {a} days and {B} can do it in {b} days. In how many days can they finish it working together?', f'{mixed(t)} days',
             f'Combined one-day work = 1/{a} + 1/{b} = {fs(Fr(a + b, a * b))}; time = {mixed(t)} days.',
             [f'{mixed(Fr(a + b, 2))} days', f'{a + b} days', f'{mixed(t + 1)} days'])


def c1s5_leave(r):
    a, b = r.choice(WORK_PAIRS)
    A, B = two_names(r)
    t = Fr(a * b, a + b)
    x = r.randint(1, max(1, int(t) - 1))
    rem = 1 - x * (Fr(1, a) + Fr(1, b))
    if rem <= 0:
        raise ValueError
    y = rem * b
    return Q(f'{A} and {B} can do a job in {a} and {b} days respectively. They work together for {x} day{"s" if x > 1 else ""}, after which {A} leaves. In how many more days will {B} finish the job?',
             f'{mixed(y)} days', f'Work done together in {x} day(s) = {x}({fs(Fr(1, a))} + {fs(Fr(1, b))}) = {fs(1 - rem)}; remaining {fs(rem)} at {fs(Fr(1, b))} per day = {mixed(y)} days.',
             [f'{mixed(rem * a)} days', f'{mixed(y + x)} days', f'{mixed(b - x)} days' if b - x != y else f'{mixed(y + 2)} days'])


def c1s5_pipes(r):
    a = r.randint(2, 12)
    b = r.randint(a + 1, 3 * a + 4)
    t = Fr(a * b, b - a)
    return Q(f'A pipe can fill a tank in {a} hours and another pipe can empty the full tank in {b} hours. If both are opened together on an empty tank, in how much time will it be filled?',
             f'{mixed(t)} hours', f'Net filling per hour = 1/{a} − 1/{b} = {fs(Fr(b - a, a * b))}; time = {mixed(t)} hours.',
             [f'{mixed(Fr(a * b, a + b))} hours', f'{b - a} hours', f'{mixed(t + 2)} hours'])


def c1s5_wages(r):
    a, b = r.choice(WORK_PAIRS)
    W = r.choice([3000, 4500, 6000, 7200, 9000, 12000, 15000, 18000])
    A, B = two_names(r)
    shA = Fr(W) * Fr(b, a + b)
    if shA.denominator != 1:
        raise ValueError
    return Q(f'{A} and {B} can complete a job in {a} and {b} days respectively. Working together they complete it and receive {inr(W)}. How should the money be shared?',
             f'{A}: {inr(int(shA))}; {B}: {inr(W - int(shA))}', f'Share in the ratio of work done per day = 1/{a} : 1/{b} = {b} : {a}. {A} gets {inr(int(shA))} and {B} gets {inr(W - int(shA))}.',
             [f'{A}: {inr(W - int(shA))}; {B}: {inr(int(shA))}', f'{A}: {inr(W // 2)}; {B}: {inr(W - W // 2)}', f'{A}: {inr(int(shA) + 500)}; {B}: {inr(W - int(shA) - 500)}'])


def c1s5_explain(r):
    a, b = r.choice(WORK_PAIRS)
    return {'stem': f'Explain why two workers who take {a} days and {b} days alone do not take {num((a + b) / 2)} days together. How long do they take?',
            'answer': f'{mixed(Fr(a * b, a + b))} days', 'key': f'Rates add, not times: 1/{a} + 1/{b} = {fs(Fr(a + b, a * b))} per day (1); time = {mixed(Fr(a * b, a + b))} days, less than either alone (1).'}


def c1s5_ar(r):
    a, b = r.choice(WORK_PAIRS)
    t = Fr(a * b, a + b)
    if r.random() < 0.5:
        return ar(f'If A takes {a} days and B takes {b} days for a job, together they take {mixed(t)} days.', 'When people work together, their one-day works are added.', 'a', f'1/{a} + 1/{b} = 1/{mixed(t)}; R explains A.')
    return ar(f'If A takes {a} days and B takes {b} days for a job, together they take {a + b} days.', 'When people work together, their one-day works are added.', 'd', f'A is false: the time is {mixed(t)} days. R is true.')


# seating arrangement puzzle (people in a row facing north)

def _clues(order):
    n = len(order)
    pos = {p: i for i, p in enumerate(order)}
    cl = []
    cl.append(('end', order[0], 'left'))
    cl.append(('end', order[-1], 'right'))
    for i in range(n - 1):
        cl.append(('imm', order[i], order[i + 1]))
    for i in range(1, n - 1):
        cl.append(('between', order[i], order[i - 1], order[i + 1]))
    for a, b in itertools.combinations(order, 2):
        k = abs(pos[a] - pos[b]) - 1
        if k >= 1:
            cl.append(('gap', a, b, k))
    for p in order[1:-1]:
        cl.append(('notend', p))
    return cl


def _holds(c, perm):
    pos = {p: i for i, p in enumerate(perm)}
    n = len(perm)
    if c[0] == 'end':
        return pos[c[1]] == (0 if c[2] == 'left' else n - 1)
    if c[0] == 'imm':
        return pos[c[1]] + 1 == pos[c[2]]
    if c[0] == 'between':
        return {pos[c[2]], pos[c[3]]} == {pos[c[1]] - 1, pos[c[1]] + 1}
    if c[0] == 'gap':
        return abs(pos[c[1]] - pos[c[2]]) - 1 == c[3]
    return 0 < pos[c[1]] < n - 1


def _say(c):
    if c[0] == 'end':
        return f'{c[1]} sits at the extreme {c[2]} end.'
    if c[0] == 'imm':
        return f'{c[1]} sits immediately to the left of {c[2]}.'
    if c[0] == 'between':
        return f'{c[1]} sits between {c[2]} and {c[3]}.'
    if c[0] == 'gap':
        return f'Exactly {c[3]} {"person sits" if c[3] == 1 else "people sit"} between {c[1]} and {c[2]}.'
    return f'{c[1]} does not sit at either end.'


def c1s5_seat(r):
    n = 5
    ppl = r.sample(GIRLS + BOYS, n)
    order = ppl[:]
    r.shuffle(order)
    cl = _clues(order)
    r.shuffle(cl)
    cl.sort(key=lambda c: c[0] == 'end')   # prefer harder clues first
    perms = list(itertools.permutations(ppl))
    chosen = []
    live = perms
    for c in cl:
        nl = [p for p in live if _holds(c, p)]
        if len(nl) < len(live):
            chosen.append(c)
            live = nl
        if len(live) == 1:
            break
    if len(live) != 1 or len(chosen) > 6:
        raise ValueError
    for c in chosen[:]:
        rest = [x for x in chosen if x is not c]
        if sum(all(_holds(x, p) for x in rest) for p in perms) == 1:
            chosen = rest
    r.shuffle(chosen)
    qpos = r.choice([(2, 'in the middle'), (1, 'second from the left end'), (3, 'second from the right end'), (0, 'at the extreme left end')])
    ans = order[qpos[0]]
    return Q(f'Five friends {", ".join(sorted(ppl)[:-1])} and {sorted(ppl)[-1]} sit in a row facing north.\n' + '\n'.join(f'• {_say(c)}' for c in chosen) +
             f'\nWho sits {qpos[1]}?', ans, f'The only arrangement (left to right) satisfying all clues is {", ".join(order)}; so {ans} sits {qpos[1]}.',
             [p for p in ppl if p != ans][:3] + [p for p in ppl if p != ans][3:])


def c1s5_path(r):
    L, B = r.randrange(30, 120, 5), r.randrange(20, 80, 5)
    w = r.choice([1, 1.5, 2, 2.5, 3])
    rate = r.choice([40, 50, 60, 75, 80, 100, 120])
    area = (L + 2 * w) * (B + 2 * w) - L * B
    return Q(f'A rectangular park in {r.choice(CITIES)} is {L} m long and {B} m wide. A path {num(w)} m wide runs all around it on the outside. Find the area of the path and the cost of paving it at {inr(rate)} per m².',
             f'{num(area)} m²; {inr(area * rate)}', f'Outer rectangle {num(L + 2 * w)} m × {num(B + 2 * w)} m; path area = {num((L + 2 * w) * (B + 2 * w))} − {L * B} = {num(area)} m²; cost = {num(area)} × {rate} = {inr(area * rate)}.',
             [f'{num(area - 4 * w * w)} m²; {inr((area - 4 * w * w) * rate)}', f'{num(2 * w * (L + B))} m²; {inr(2 * w * (L + B) * rate)}', f'{num(area * 2)} m²; {inr(area * 2 * rate)}'])


def c1s5_tank(r):
    l, b, h = r.choice([2, 3, 4, 5]), r.choice([1.5, 2, 2.5, 3]), r.choice([1, 1.2, 1.5, 2])
    rate = r.choice([50, 60, 75, 100, 120, 150, 200, 250])
    vol = l * b * h * 1000
    t = vol / rate
    if abs(t - round(t)) > 1e-9:
        raise ValueError
    return Q(f'A rectangular water tank is {l} m long, {num(b)} m wide and {num(h)} m deep. A pipe fills it at {rate} litres per minute. How long will it take to fill the empty tank? (1 m³ = 1000 litres)',
             f'{int(t)} minutes ({int(t) // 60} h {int(t) % 60} min)', f'Volume = {l} × {num(b)} × {num(h)} = {num(l * b * h)} m³ = {num(vol)} L; time = {num(vol)}/{rate} = {int(t)} min.',
             [f'{int(t * 2)} minutes ({int(t * 2) // 60} h {int(t * 2) % 60} min)', f'{int(t // 10)} minutes (0 h {int(t // 10)} min)' if t // 10 < 60 else f'{int(t / 2)} minutes', f'{int(t + 60)} minutes ({int(t + 60) // 60} h {int(t + 60) % 60} min)'])


def c1s5_case(r):
    A, B = two_names(r)
    a, b = r.choice([(12, 18), (10, 15), (20, 30), (15, 30), (24, 36)])
    W = r.choice([6000, 9000, 12000, 15000])
    t = Fr(a * b, a + b)
    sh = Fr(W * b, a + b)
    return {'stem': (f'{A} and {B} take up a contract to paint a school building in {r.choice(CITIES)}. {A} alone can finish it in {a} days and {B} alone in {b} days. The contract amount is {inr(W)}.\n'
                     f'(i) What part of the work do they do together in one day? (1)\n(ii) In how many days will they finish the work together? (1)\n'
                     f'(iii) How should the {inr(W)} be divided between them, and why? (2)'),
            'answer': f'(i) {fs(Fr(a + b, a * b))} (ii) {mixed(t)} days (iii) {A} {inr(float(sh))}, {B} {inr(W - float(sh))}, in the ratio {b} : {a} of their daily work',
            'key': f'(i) 1/{a} + 1/{b} (1). (ii) reciprocal (1). (iii) ratio of efficiencies 1/{a} : 1/{b} (1); shares (1).'}


c1s5_tf = tf_mcq('time and work', [
    'If A can do a work in n days, A\'s one day\'s work is 1/n.', 'Wages are shared in the ratio of the work done.',
    'If A is twice as efficient as B, A takes half the time B takes.', 'An emptying pipe is treated as doing negative work.',
    'The time taken by two workers together is less than the time taken by either alone.'],
    ['If A can do a work in n days, A\'s one day\'s work is n.', 'Time taken together is the average of the individual times.',
     'Wages are shared in the ratio of the time taken.', 'If A is twice as efficient as B, A takes twice the time B takes.', 'An emptying pipe increases the rate of filling.'])

# ======================================================== ch02 Sets and relations
# st4 types of relations (new)

def _rel_props(A, R):
    Rs = set(R)
    refl = all((a, a) in Rs for a in A)
    sym = all((b, a) in Rs for a, b in Rs)
    tra = all((a, d) in Rs for a, b in Rs for c, d in Rs if b == c)
    return refl, sym, tra


def _rstr(R):
    return '{' + ', '.join(f'({a}, {b})' for a, b in sorted(R)) + '}'


def _label(p):
    refl, sym, tra = p
    names = [n for n, v in zip(['reflexive', 'symmetric', 'transitive'], p) if v]
    if all(p):
        return 'an equivalence relation'
    if not names:
        return 'neither reflexive, nor symmetric, nor transitive'
    return ' and '.join(names) + ' only'


ALL_LABELS = ['an equivalence relation', 'reflexive only', 'symmetric only', 'transitive only', 'reflexive and symmetric only',
              'reflexive and transitive only', 'symmetric and transitive only', 'neither reflexive, nor symmetric, nor transitive']


def _rand_rel(r, A):
    pairs = [(a, b) for a in A for b in A]
    R = set(r.sample(pairs, r.randint(2, 6)))
    if r.random() < 0.5:
        R |= {(a, a) for a in A}
    if r.random() < 0.4:
        R |= {(b, a) for a, b in R}
    return sorted(R)


def c2s4_classify(r):
    A = [1, 2, 3]
    R = _rand_rel(r, A)
    lab = _label(_rel_props(A, R))
    p = _rel_props(A, R)
    why = '; '.join([f'{"" if p[0] else "not "}reflexive', f'{"" if p[1] else "not "}symmetric', f'{"" if p[2] else "not "}transitive'])
    return mcq(f'Let A = {{1, 2, 3}} and R = {_rstr(R)} be a relation on A. Then R is', lab, r.sample([x for x in ALL_LABELS if x != lab], 3), f'Check each property: {why}.', r)


def c2s4_add(r):
    n = r.choice([3, 4])
    A = list(range(1, n + 1))
    R = set(r.sample([(a, b) for a in A for b in A if a != b], r.randint(1, 3))) | set(r.sample([(a, a) for a in A], r.randint(0, n - 1)))
    miss = [(a, a) for a in A if (a, a) not in R]
    if not miss:
        raise ValueError
    return Q(f'Let A = {setstr(A)} and R = {_rstr(R)}. Write the least number of ordered pairs that must be added to R to make it reflexive.',
             f'{len(miss)}: {", ".join(f"({a}, {a})" for a, _ in miss)}', f'Reflexive needs (a, a) for every a ∈ A; missing pairs: {", ".join(f"({a}, {a})" for a, _ in miss)}.',
             [f'{len(miss) + 1}', f'{n}', f'{len(miss) - 1 if len(miss) > 1 else 0}'])


def _closure(A, R):
    S_ = set(R) | {(a, a) for a in A}
    while True:
        new = S_ | {(b, a) for a, b in S_} | {(a, d) for a, b in S_ for c, d in S_ if b == c}
        if new == S_:
            return S_
        S_ = new


def c2s4_equiv_add(r):
    A = [1, 2, 3, 4]
    R = set(r.sample([(a, b) for a in A for b in A if a != b], 2))
    cl = _closure(A, R)
    add = sorted(cl - R)
    return Q(f'Let A = {{1, 2, 3, 4}} and R = {_rstr(R)}. Find the minimum number of ordered pairs to be added to R so that the enlarged relation is an equivalence relation.',
             str(len(add)), f'Add all (a, a) (4 pairs), the reverses needed for symmetry and pairs forced by transitivity: smallest equivalence relation containing R has {len(cl)} pairs, so {len(add)} must be added: {_rstr(add)}.',
             nd(str(len(add)), [str(len(add) - 1), str(len(add) + 1), str(len(add) + 2), '4']))


def c2s4_count(r):
    n = r.randint(2, 5)
    kind = r.choice(['reflexive', 'symmetric', 'all'])
    if kind == 'reflexive':
        v, f = 2 ** (n * n - n), f'2^(n² − n) = 2{sup(n * n - n)}'
    elif kind == 'symmetric':
        v, f = 2 ** (n * (n + 1) // 2), f'2^(n(n + 1)/2) = 2{sup(n * (n + 1) // 2)}'
    else:
        v, f = 2 ** (n * n), f'2^(n²) = 2{sup(n * n)}'
    what = {'reflexive': 'reflexive relations', 'symmetric': 'symmetric relations', 'all': 'relations'}[kind]
    return Q(f'How many {what} can be defined on a set with {n} elements?', str(v),
             f'{"Each of the n² − n off-diagonal pairs may be in or out; diagonal pairs must be in" if kind == "reflexive" else ("Choose freely the n diagonal pairs and the n(n − 1)/2 unordered off-diagonal pairs" if kind == "symmetric" else "Any subset of A × A, which has n² pairs")}: {f} = {v}.',
             nd(str(v), [str(2 ** n), str(n * n), str(2 ** (n * n) if kind != 'all' else 2 ** (n * n - n)), str(2 ** (n + 1))]))


RULES = [('a R b if a ≤ b', lambda a, b: a <= b), ('a R b if a < b', lambda a, b: a < b), ('a R b if a divides b', lambda a, b: b % a == 0),
         ('a R b if |a − b| ≤ 1', lambda a, b: abs(a - b) <= 1), ('a R b if a + b is even', lambda a, b: (a + b) % 2 == 0),
         ('a R b if a − b is a multiple of 3', lambda a, b: (a - b) % 3 == 0), ('a R b if a = b', lambda a, b: a == b),
         ('a R b if b = a + 1', lambda a, b: b == a + 1), ('a R b if a × b is odd', lambda a, b: (a * b) % 2 == 1), ('a R b if a ≠ b', lambda a, b: a != b)]


def c2s4_rule(r):
    txt, f = r.choice(RULES)
    n = r.randint(4, 6)
    A = list(range(1, n + 1))
    R = [(a, b) for a in A for b in A if f(a, b)]
    p = _rel_props(A, R)
    lab = _label(p)
    reasons = []
    for nm, ok in zip(['reflexive', 'symmetric', 'transitive'], p):
        reasons.append(f'{nm}: {"yes" if ok else "no"}')
    return Q(f'A relation R on A = {setstr(A)} is defined by {txt}. Check whether R is reflexive, symmetric and transitive.', f'R is {lab}',
             f'{"; ".join(reasons)}. Give a counter-example for each property that fails (1 mark each property).', ['R is ' + x for x in r.sample([y for y in ALL_LABELS if y != lab], 3)])


def c2s4_mod(r):
    k = r.choice([2, 3, 4, 5])
    return {'stem': f'Show that the relation R on Z defined by R = {{(a, b) : a − b is divisible by {k}}} is an equivalence relation.',
            'answer': f'Reflexive: a − a = 0 divisible by {k}. Symmetric: a − b = {k}m ⇒ b − a = {k}(−m). Transitive: a − b = {k}m, b − c = {k}n ⇒ a − c = {k}(m + n). Hence an equivalence relation.',
            'key': 'Reflexive (1), symmetric (1), transitive (1) with algebraic reason; conclusion.'}


def c2s4_class(r):
    k = r.choice([2, 3, 4, 5])
    n = r.randint(8, 15)
    a = r.randint(1, k)
    cls = [x for x in range(1, n + 1) if (x - a) % k == 0]
    return Q(f'R is the relation on A = {{1, 2, …, {n}}} given by a R b if |a − b| is a multiple of {k}. Find the equivalence class [{a}].', setstr(cls),
             f'[{a}] contains every x ∈ A with x − {a} a multiple of {k}: {setstr(cls)}.', [setstr(cls[:-1]), setstr([x for x in range(1, n + 1) if x % k == 0]), setstr(cls + [cls[-1] + 1])])


def c2s4_ar(r):
    A = [1, 2, 3]
    R = _rand_rel(r, A)
    p = _rel_props(A, R)
    prop = r.choice([0, 1, 2])
    nm = ['reflexive', 'symmetric', 'transitive'][prop]
    defn = ['(a, a) ∈ R for every a ∈ A', '(a, b) ∈ R ⇒ (b, a) ∈ R', '(a, b), (b, c) ∈ R ⇒ (a, c) ∈ R'][prop]
    if p[prop]:
        return ar(f'On A = {{1, 2, 3}}, the relation R = {_rstr(R)} is {nm}.', f'A relation R on A is {nm} if {defn}.', 'a', f'R satisfies the condition {defn}; R explains A.')
    return ar(f'On A = {{1, 2, 3}}, the relation R = {_rstr(R)} is {nm}.', f'A relation R on A is {nm} if {defn}.', 'd', f'A is false: R fails the condition {defn}. R is the correct definition.')


c2s4_terms = term_mcq([
    ('a reflexive relation', '(a, a) ∈ R for every a ∈ A'), ('a symmetric relation', '(a, b) ∈ R always implies (b, a) ∈ R'),
    ('a transitive relation', '(a, b) ∈ R and (b, c) ∈ R always imply (a, c) ∈ R'), ('an equivalence relation', 'R is reflexive, symmetric and transitive'),
    ('the empty relation', 'no element of A is related to any element of A, i.e. R = φ'), ('the universal relation', 'every element of A is related to every element of A, i.e. R = A × A'),
    ('the identity relation', 'every element of A is related to itself and to nothing else, i.e. R = {(a, a) : a ∈ A}')],
    'A relation R on a set A is called {a} if', 'A relation R on a set A such that {b} is called', '{a}: {b}.')

c2s4_tf = tf_mcq('relations on a set', [
    'The identity relation on a set is an equivalence relation.', 'The universal relation A × A is an equivalence relation.',
    'The empty relation on a non-empty set is symmetric and transitive but not reflexive.', 'The relation "is parallel to" on lines in a plane (a line is parallel to itself) is an equivalence relation.',
    'The relation "≤" on R is reflexive and transitive but not symmetric.'],
    ['The relation "<" on R is reflexive.', 'Every symmetric relation is transitive.', 'The relation "is a brother of" on a set of people is always symmetric.',
     'The empty relation is reflexive on every non-empty set.', 'The relation "divides" on N is symmetric.'])


def c2s4_case(r):
    k = r.choice([3, 4, 5])
    n = r.choice([12, 15, 20])
    return {'stem': (f'In a school quiz, {n} students with roll numbers 1 to {n} are placed in teams: two students are in the same team if the difference of their roll numbers is divisible by {k}.\n'
                     f'(i) Is the relation "is in the same team as" reflexive? (1)\n(ii) Is it symmetric and transitive? (1)\n(iii) How many teams are formed, and which roll numbers are in the team of roll number 1? (2)'),
            'answer': f'(i) Yes (ii) Yes – an equivalence relation (iii) {k} teams; {setstr([x for x in range(1, n + 1) if (x - 1) % k == 0])}',
            'key': f'(i) a − a = 0 (1). (ii) symmetric and transitive by divisibility (1). (iii) one class per remainder mod {k} (1); class of 1 listed (1).'}


# ======================================================== ch03 Sequences and series
# st2 additions: infinite GP

def c3s2_inf(r):
    a = r.choice([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 18, 24, 27])
    q = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(-1, 2), Fr(-1, 3), Fr(1, 5)])
    s = Fr(a) / (1 - q)
    terms = ', '.join(fs(a * q ** i) for i in range(3))
    return Q(f'Find the sum to infinity of the GP {terms}, …', fs(s), f'r = {fs(q)}, |r| < 1, so S∞ = a/(1 − r) = {a}/(1 − ({fs(q)})) = {fs(s)}.',
             [fs(Fr(a) / (1 + q)), fs(s + 1), fs(Fr(a) * q / (1 - q))])


def c3s2_rec(r):
    d = r.choice([1, 2])
    digits = ''.join(str(r.randint(0, 9)) for _ in range(d))
    if set(digits) == {'0'} or set(digits) == {'9'}:
        raise ValueError
    whole = r.randint(0, 3)
    val = whole + Fr(int(digits), 10 ** d - 1)
    show = f'{whole}.' + digits * 3 + '…'
    return Q(f'Using the sum of an infinite GP, express the recurring decimal {show} as a rational number p/q.', fs(val),
             f'0.{digits}{digits}… = {int(digits)}/{10 ** d} + {int(digits)}/{10 ** (2 * d)} + … = ({int(digits)}/{10 ** d})/(1 − 1/{10 ** d}) = {fs(Fr(int(digits), 10 ** d - 1))}; add {whole}: {fs(val)}.',
             [fs(whole + Fr(int(digits), 10 ** d)), fs(val + Fr(1, 10 ** d - 1)), fs(whole + Fr(int(digits), 10 ** d + 1))])


def c3s2_findr(r):
    a = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    q = r.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(1, 5), Fr(2, 5)])
    s = Fr(a) / (1 - q)
    return Q(f'The sum to infinity of a GP is {fs(s)} and its first term is {a}. Find the common ratio and the second term.', f'r = {fs(q)}; second term = {fs(a * q)}',
             f'{fs(s)} = {a}/(1 − r) ⇒ 1 − r = {fs(Fr(a) / s)} ⇒ r = {fs(q)}; second term = ar = {fs(a * q)}.',
             [f'r = {fs(1 - q)}; second term = {fs(a * (1 - q))}', f'r = {fs(q)}; second term = {fs(a / q)}', f'r = {fs(q * 2) if q * 2 < 1 else fs(q / 2)}; second term = {fs(a * q * 2)}'])


def c3s2_bounce(r):
    h = r.choice([10, 12, 15, 16, 18, 20, 24, 27, 30])
    q = r.choice([Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(1, 3), Fr(3, 5)])
    tot = h + 2 * h * q / (1 - q)
    return Q(f'A ball is dropped from a height of {h} m. Each time it hits the ground it rebounds to {fs(q)} of the height from which it fell. Find the total distance travelled before it comes to rest.',
             f'{mixed(tot)} m', f'Down {h}; then up and down {fs(h * q)}, {fs(h * q * q)}, … Total = {h} + 2 × {fs(h * q)}/(1 − {fs(q)}) = {mixed(tot)} m.',
             [f'{mixed(Fr(h) / (1 - q))} m', f'{mixed(h + h * q / (1 - q))} m', f'{mixed(tot * 2)} m'])


def c3s2_infar(r):
    q = r.choice([Fr(1, 2), Fr(1, 3), Fr(3, 2), Fr(2), Fr(-1, 2)])
    a = r.choice([2, 3, 4, 6])
    if abs(q) < 1:
        return ar(f'The sum to infinity of the GP {a}, {fs(a * q)}, {fs(a * q * q)}, … is {fs(a / (1 - q))}.', 'S∞ = a/(1 − r) when |r| < 1.', 'a', f'|r| = {fs(abs(q))} < 1 and a/(1 − r) = {fs(a / (1 - q))}.')
    return ar(f'The sum to infinity of the GP {a}, {fs(a * q)}, {fs(a * q * q)}, … is {fs(a / (1 - q))}.', 'S∞ = a/(1 − r) when |r| < 1.', 'd', f'A is false: |r| = {fs(abs(q))} ≥ 1, so the series has no finite sum. R is true.')


c3s2_infmcq = pool_mcq([
    ('The sum to infinity of a GP with first term a and common ratio r exists when', '|r| < 1', ['r > 1', 'r = 1', '|r| ≥ 1'], 'Terms shrink to 0 only if |r| < 1.'),
    ('For a GP with |r| < 1, the sum to infinity is', 'a/(1 − r)', ['a/(r − 1)', 'a(1 − r)', 'ar/(1 − r)'], 'Limit of a(1 − rⁿ)/(1 − r) as n → ∞.'),
    ('Which of the following GPs has a finite sum to infinity?', '5, 5/2, 5/4, …', ['2, 4, 8, …', '1, −1, 1, …', '3, 3, 3, …'], 'Only r = 1/2 satisfies |r| < 1.'),
    ('The value of 1 + 1/3 + 1/9 + … is', '3/2', ['4/3', '2', '3'], '1/(1 − 1/3) = 3/2.'),
])

# st4 special series

def c3s4_formula(r):
    return pool_mcq([
        ('The sum 1 + 2 + 3 + … + n equals', 'n(n + 1)/2', ['n(n − 1)/2', 'n²', 'n(n + 1)(2n + 1)/6'], 'Standard result.'),
        ('The sum 1² + 2² + … + n² equals', 'n(n + 1)(2n + 1)/6', ['n(n + 1)/2', '[n(n + 1)/2]²', 'n²(n + 1)/2'], 'Standard result.'),
        ('The sum 1³ + 2³ + … + n³ equals', '[n(n + 1)/2]²', ['n(n + 1)(2n + 1)/6', 'n³(n + 1)/3', 'n(n + 1)/2'], 'Standard result: the square of Σn.'),
        ('The sum of the first n odd natural numbers is', 'n²', ['n(n + 1)', '2n − 1', 'n(n + 1)/2'], 'Σ(2k − 1) = n(n + 1) − n = n².'),
        ('The sum of the first n even natural numbers is', 'n(n + 1)', ['n²', 'n(n − 1)', '2n²'], 'Σ2k = 2 × n(n + 1)/2.'),
    ])(r)


def c3s4_eval(r):
    n = r.randint(8, 30)
    kind = r.choice([1, 2, 3])
    vals = {1: n * (n + 1) // 2, 2: n * (n + 1) * (2 * n + 1) // 6, 3: (n * (n + 1) // 2) ** 2}
    lab = {1: f'1 + 2 + 3 + … + {n}', 2: f'1² + 2² + 3² + … + {n}²', 3: f'1³ + 2³ + 3³ + … + {n}³'}[kind]
    f = {1: 'n(n + 1)/2', 2: 'n(n + 1)(2n + 1)/6', 3: '[n(n + 1)/2]²'}[kind]
    return Q(f'Find the sum {lab}.', str(vals[kind]), f'Use {f} with n = {n}: {vals[kind]}.', nd(str(vals[kind]), [str(v) for k, v in vals.items() if k != kind] + [str(vals[kind] + n)]))


def c3s4_range(r):
    m = r.randint(5, 15)
    n = r.randint(m + 8, m + 25)
    kind = r.choice([2, 3])
    f = (lambda k: k * (k + 1) * (2 * k + 1) // 6) if kind == 2 else (lambda k: (k * (k + 1) // 2) ** 2)
    v = f(n) - f(m - 1)
    p = sup(kind)
    return Q(f'Find the value of {m}{p} + {m + 1}{p} + … + {n}{p}.', str(v), f'Σ(1 to {n}) − Σ(1 to {m - 1}) = {f(n)} − {f(m - 1)} = {v}.', [str(f(n) - f(m)), str(f(n)), str(v + m ** kind)])


def c3s4_nterm(r):
    a, b, c = r.randint(0, 3), r.randint(-3, 4), r.randint(-4, 5)
    if a == 0 and b == 0:
        a = 1
    n = r.randint(5, 15)
    S1, S2 = n * (n + 1) // 2, n * (n + 1) * (2 * n + 1) // 6
    v = a * S2 + b * S1 + c * n
    return Q(f'The nth term of a series is aₙ = {poly([a, b, c], "n")}. Find the sum of its first {n} terms.', str(v),
             f'Sₙ = {a}Σn² + {b}Σn + {c}n with n = {n}: {a}({S2}) + {b}({S1}) + {c}({n}) = {v}.', [str(v + a * S1), str(a * S2 + b * S1), str(v - c * n + c)])


def c3s4_prod(r):
    n = r.randint(6, 20)
    kind = r.choice(['k(k+1)', 'k(k+2)', 'k²(k+1)'])
    if kind == 'k(k+1)':
        v, ser, gt = sum(k * (k + 1) for k in range(1, n + 1)), '1×2 + 2×3 + 3×4 + …', 'k(k + 1) = k² + k'
    elif kind == 'k(k+2)':
        v, ser, gt = sum(k * (k + 2) for k in range(1, n + 1)), '1×3 + 2×4 + 3×5 + …', 'k(k + 2) = k² + 2k'
    else:
        v, ser, gt = sum(k * k * (k + 1) for k in range(1, n + 1)), '1²×2 + 2²×3 + 3²×4 + …', 'k²(k + 1) = k³ + k²'
    return Q(f'Find the sum of the first {n} terms of the series {ser}', str(v), f'General term {gt}; sum the standard series for n = {n}: {v}.', [str(v - n), str(v + n * (n + 1) // 2), str(v // 2)])


def c3s4_explain(r):
    n = r.randint(4, 12)
    s1 = n * (n + 1) // 2
    return {'stem': f'Verify that 1³ + 2³ + … + {n}³ = (1 + 2 + … + {n})². What general result does this illustrate?',
            'answer': f'Both equal {s1 * s1}; Σk³ = (Σk)² = [n(n + 1)/2]².', 'key': f'Σk = {s1} (½); its square {s1 * s1} (½); Σk³ = {s1 * s1} (½); general statement (½).'}


def c3s4_ar(r):
    n = r.randint(5, 20)
    s1 = n * (n + 1) // 2
    if r.random() < 0.5:
        return ar(f'1³ + 2³ + … + {n}³ = {s1 * s1}.', 'The sum of the cubes of the first n natural numbers is the square of their sum.', 'a', f'(Σk)² = {s1}² = {s1 * s1}; R explains A.')
    return ar(f'1² + 2² + … + {n}² = {s1 * s1}.', 'The sum of the cubes of the first n natural numbers is the square of their sum.', 'd',
              f'A is false: Σk² = {n * (n + 1) * (2 * n + 1) // 6}; {s1 * s1} is Σk³. R is true.')


def c3s4_case(r):
    n = r.randint(8, 15)
    who = name(r)
    return {'stem': (f'{who} stacks oranges for a fruit stall in {r.choice(CITIES)} as a square pyramid: the top layer has 1 orange, the next 2 × 2 = 4, then 3 × 3 = 9, and so on, with {n} layers.\n'
                     f'(i) How many oranges are in the bottom layer? (1)\n(ii) Write the total as a series and name the formula needed. (1)\n(iii) Find the total number of oranges. (2)'),
            'answer': f'(i) {n * n} (ii) 1² + 2² + … + {n}², Σk² = n(n + 1)(2n + 1)/6 (iii) {n * (n + 1) * (2 * n + 1) // 6}',
            'key': f'(i) {n}² (1). (ii) series and formula (1). (iii) substitution (1), value (1).'}


# ======================================================== ch04 Functions
# st1 dependent/independent variables; domain and range

def c4s1_dep(r):
    k = r.choice([
        ('A taxi fare F (₹) is F = 50 + 14d, where d is the distance in km.', 'd', 'F'),
        ('The cost C (₹) of producing x units is C = 2000 + 35x.', 'x', 'C'),
        ('The area A of a circle depends on its radius r: A = πr².', 'r', 'A'),
        ('The simple interest I on ₹5,000 at 8% p.a. for t years is I = 400t.', 't', 'I'),
        ('The revenue R (₹) from selling q items at ₹120 each is R = 120q.', 'q', 'R'),
        ('The electricity bill B (₹) for u units is B = 150 + 6u.', 'u', 'B'),
    ])
    stem, ind, dep = k
    if r.random() < 0.5:
        return mcq(f'{stem} Which is the dependent variable?', dep, [ind, 'both', 'neither'], f'{dep} is found from the value of {ind}, so {dep} is dependent and {ind} is independent.', r)
    return mcq(f'{stem} Which is the independent variable?', ind, [dep, 'both', 'neither'], f'{ind} is chosen freely; {dep} depends on it.', r)


def c4s1_sqrt(r):
    a = r.randint(1, 9)
    kind = r.choice(['x-a', 'a-x', 'x2-a2', '1/sqrt'])
    if kind == 'x-a':
        return Q(f'Find the domain of f(x) = √(x − {a}).', f'[{a}, ∞)', f'x − {a} ≥ 0 ⇒ x ≥ {a}.', [f'({a}, ∞)', f'(−∞, {a}]', 'R'])
    if kind == 'a-x':
        return Q(f'Find the domain of f(x) = √({a} − x).', f'(−∞, {a}]', f'{a} − x ≥ 0 ⇒ x ≤ {a}.', [f'[{a}, ∞)', f'(−∞, {a})', f'[−{a}, {a}]'])
    if kind == 'x2-a2':
        return Q(f'Find the domain of f(x) = √({a * a} − x²).', f'[−{a}, {a}]', f'{a * a} − x² ≥ 0 ⇒ −{a} ≤ x ≤ {a}.', [f'(−{a}, {a})', f'[0, {a}]', f'(−∞, −{a}] ∪ [{a}, ∞)'])
    return Q(f'Find the domain of f(x) = 1/√(x − {a}).', f'({a}, ∞)', f'Need x − {a} > 0 (root defined and non-zero): x > {a}.', [f'[{a}, ∞)', f'R − {{{a}}}', f'(−∞, {a})'])


def c4s1_range_lin(r):
    m = r.choice([2, 3, -2, 4, 5, -3])
    c = r.randint(-5, 8)
    a, b = sorted(r.sample(range(-4, 8), 2))
    lo, hi = sorted([m * a + c, m * b + c])
    return Q(f'Find the range of f(x) = {lin(m, c)} for x ∈ [{a}, {b}].', f'[{lo}, {hi}]', f'f is linear, so its extreme values are at the end points: f({a}) = {m * a + c}, f({b}) = {m * b + c}. Range [{lo}, {hi}].',
             [f'[{m * a}, {m * b}]' if m > 0 else f'[{m * b}, {m * a}]', f'({lo}, {hi})', f'[{a}, {b}]'])


def c4s1_context(r):
    cap_ = r.choice([40, 50, 60, 80])
    fee = r.choice([150, 200, 250, 300])
    return Q(f'A coaching centre in {r.choice(CITIES)} has {cap_} seats. Its weekly fee income is I(n) = {fee}n, where n is the number of students enrolled. Write the domain and range of I in this context.',
             f'Domain {{0, 1, 2, …, {cap_}}}; range {{0, {fee}, {2 * fee}, …, {fee * cap_}}}', f'n is a whole number from 0 to {cap_} (1); I takes the values {fee}n, from 0 to {inr(fee * cap_)} (1).',
             [f'Domain [0, ∞); range [0, ∞)', f'Domain {{1, …, {cap_}}}; range [0, {fee * cap_}]', f'Domain R; range R'])


def c4s1_range_quad(r):
    h, k = r.choice([x for x in range(-4, 5) if x]), r.choice([x for x in range(-6, 7) if x])
    a = r.choice([1, 2, -1, -2])
    expr = f'{"" if a == 1 else ("−" if a == -1 else a)}(x {"−" if h >= 0 else "+"} {abs(h)})² {"+" if k >= 0 else "−"} {abs(k)}'
    ans = f'[{k}, ∞)' if a > 0 else f'(−∞, {k}]'
    return Q(f'Find the range of f(x) = {expr}, x ∈ R.', ans, f'(x {"−" if h >= 0 else "+"} {abs(h)})² ≥ 0, so f(x) {"≥" if a > 0 else "≤"} {k}, with equality at x = {h}. Range {ans}.',
             [f'[{h}, ∞)', f'(−∞, {k}]' if a > 0 else f'[{k}, ∞)', 'R'])


def c4s1_rational(r):
    a, b = r.sample(range(-6, 7), 2)
    return Q(f'Find the domain of f(x) = (x + {r.randint(1, 9)})/((x {"−" if a >= 0 else "+"} {abs(a)})(x {"−" if b >= 0 else "+"} {abs(b)})).', f'R − {{{min(a, b)}, {max(a, b)}}}',
             f'The denominator vanishes at x = {a} and x = {b}; exclude them.', [f'R − {{{-a}, {-b}}}' if (a, b) != (0, 0) else 'R', 'R', f'R − {{{a}}}'])


def c4s1_explain(r):
    v = r.choice([('f(x) = √(x − 3)', 'x ≥ 3, i.e. [3, ∞)', 'a square root of a negative number is not real'),
                  ('f(x) = 1/(x − 5)', 'R − {5}', 'division by zero is undefined at x = 5'),
                  ('f(x) = log (x + 2)', 'x > −2, i.e. (−2, ∞)', 'log is defined only for positive arguments'),
                  ('f(x) = √(16 − x²)', '[−4, 4]', '16 − x² must be non-negative'),
                  ('f(x) = 1/√(9 − x)', 'x < 9, i.e. (−∞, 9)', 'the root must be real and non-zero')])
    return {'stem': f'Explain how you find the domain of {v[0]} and write the domain.', 'answer': v[1], 'key': f'Reason: {v[2]} (1); domain {v[1]} (1).'}


def c4s1_ar(r):
    a = r.randint(1, 9)
    if r.random() < 0.5:
        return ar(f'The domain of f(x) = √(x − {a}) is [{a}, ∞).', 'The square root of a negative real number is not a real number.', 'a', 'R explains why x − a ≥ 0 is required.')
    return ar(f'The range of f(x) = x² + {a}, x ∈ R, is R.', f'x² ≥ 0 for every real x.', 'd', f'A is false: the range is [{a}, ∞). R is true.')


def c4s1_case(r):
    F0, v = r.choice([(5000, 40), (8000, 25), (12000, 60), (3000, 15)])
    p = v + r.choice([20, 30, 40])
    cap_ = r.choice([500, 800, 1000])
    q = r.randint(100, cap_)
    be = Fr(F0, p - v)
    return {'stem': (f'A small unit makes school bags. Its monthly cost is C(x) = {F0} + {v}x rupees for x bags, and each bag sells for ₹{p}. At most {cap_} bags can be made in a month.\n'
                     f'(i) Name the dependent and independent variables in C(x). (1)\n(ii) Write the domain of C in this context. (1)\n'
                     f'(iii) Write the profit function P(x) and find P({q}). (1)\n(iv) For how many bags does the unit break even? (1)'),
            'answer': f'(i) C dependent, x independent (ii) {{0, 1, 2, …, {cap_}}} (iii) P(x) = {p - v}x − {F0}; P({q}) = {inr((p - v) * q - F0)} (iv) {f"{be} bags" if be.denominator == 1 else f"{mixed(be)} bags, so at least {math.ceil(be)} bags to cover costs"}',
            'key': '(i) 1 (ii) whole numbers up to capacity (1) (iii) R − C (½) value (½) (iv) P(x) = 0 (1).'}


c4s1_tf = tf_mcq('domain and range of functions', [
    'The domain of a polynomial function is R.', 'The range of f(x) = x², x ∈ R, is [0, ∞).', 'The domain of f(x) = 1/x is R − {0}.',
    'The domain of a logarithmic function log x is (0, ∞).', 'In C = 500 + 20x, C is the dependent variable.'],
    ['The domain of f(x) = √x is R.', 'The range of f(x) = x², x ∈ R, is R.', 'The domain of f(x) = 1/x is R.', 'The range of a constant function is R.',
     'In C = 500 + 20x, x is the dependent variable.'])

# st2 types of functions (extra)

FTYPES = [('f(x) = 3x² − 5x + 2', 'polynomial function'), ('f(x) = (x + 1)/(x − 2)', 'rational function'), ('f(x) = 2ˣ', 'exponential function'),
          ('f(x) = log₍₃₎ x', 'logarithmic function'), ('f(x) = |x − 4|', 'modulus function'), ('f(x) = [x]', 'greatest integer (step) function'),
          ('f(x) = 5ˣ⁺¹', 'exponential function'), ('f(x) = log (x + 3)', 'logarithmic function'),
          ('f(x) = x³ + 2x', 'polynomial function'), ('f(x) = (2x² + 1)/(x² − 9)', 'rational function'), ('f(x) = |2x + 1|', 'modulus function'),
          ('f(x) = eˣ', 'exponential function')]


def c4s2_type(r):
    fx, t = r.choice(FTYPES)
    wrong = list(dict.fromkeys(x for _, x in FTYPES if x != t))
    return mcq(f'The function {fx} is a', t, r.sample(wrong, 3), f'{fx} is a {t}.', r)


def c4s2_step(r):
    x = Fr(r.randint(-40, 40), r.choice([2, 3, 4, 5, 10]))
    if x.denominator == 1:
        raise ValueError
    v = math.floor(x)
    xs = num(float(x), 2) if x.denominator in (2, 4, 5, 10) else fs(x)
    return Q(f'If f(x) = [x] is the greatest integer function, find f({xs}).', str(v), f'[x] is the greatest integer ≤ x: [{xs}] = {v}.', [str(v + 1), str(-v) if v else '1', str(math.ceil(x) + 1)])


def c4s2_exp(r):
    a = r.choice([100, 200, 500, 1000, 2000])
    b = r.choice([2, 3])
    t = r.randint(2, 6)
    return Q(f'The number of bacteria in a culture is N(t) = {a} × {b}ᵗ, where t is in hours. Find N({t}) and state the type of function.', f'{a * b ** t:,}; exponential function'.replace(',', ''),
             f'N({t}) = {a} × {b}{sup(t)} = {a * b ** t}; the variable is in the exponent, so N is exponential.',
             [f'{a * b * t}; linear function', f'{a * t ** b}; polynomial function', f'{a * b ** (t - 1)}; exponential function'])


def c4s2_logdom(r):
    a, b = r.randint(1, 6), r.choice([2, 3])
    sgn = r.choice([1, -1])
    if sgn > 0:
        return Q(f'Find the domain of f(x) = log ({b}x − {a * b}).', f'({a}, ∞)', f'Need {b}x − {a * b} > 0 ⇒ x > {a}.', [f'[{a}, ∞)', f'(−∞, {a})', 'R'])
    return Q(f'Find the domain of f(x) = log ({a * b} − {b}x).', f'(−∞, {a})', f'Need {a * b} − {b}x > 0 ⇒ x < {a}.', [f'(−∞, {a}]', f'({a}, ∞)', 'R'])


def c4s2_mod(r):
    a = r.randint(-5, 5)
    xs = r.sample(range(-6, 7), 3)
    vals = [abs(x - a) for x in xs]
    return Q(f'For f(x) = |x {"−" if a >= 0 else "+"} {abs(a)}|, find f({xs[0]}), f({xs[1]}) and f({xs[2]}).', ', '.join(map(str, vals)),
             f'Substitute and take the absolute value: {", ".join(f"|{x - a}| = {v}" for x, v in zip(xs, vals))}.', [', '.join(str(x - a) for x in xs), ', '.join(str(abs(x + a)) for x in xs), ', '.join(str(v + 1) for v in vals)])


def c4s2_tax(r):
    lim = r.choice([20, 30, 50])
    base, rate = r.choice([(40, 3), (50, 4), (30, 2)])
    u = r.randint(lim + 5, lim + 60)
    v = base + rate * (u - lim)
    return Q(f'A mobile data plan charges ₹{base} for up to {lim} GB and ₹{rate} for each extra GB. Write the charge C(x) as a piecewise function of the data x GB used, and find C({u}).',
             f'C(x) = {base} for 0 ≤ x ≤ {lim}; C(x) = {base} + {rate}(x − {lim}) for x > {lim}; C({u}) = ₹{v}', f'Two pieces (1); {base} + {rate} × {u - lim} = {v} (1).',
             [f'C({u}) = ₹{rate * u}', f'C({u}) = ₹{base + rate * u}', f'C({u}) = ₹{v + rate}'])

# st3 graphs and transformations


BASEF = [('x²', lambda x: x * x), ('|x|', abs), ('x³', lambda x: x ** 3), ('√x', None)]


def c4s3_shift(r):
    f = r.choice(['x²', '|x|', 'x³', '2ˣ', 'log x'])
    h, k = r.choice([(r.randint(1, 5), 0), (-r.randint(1, 5), 0), (0, r.randint(1, 5)), (0, -r.randint(1, 5))])
    inner = (f.replace('x', f'(x {"−" if h > 0 else "+"} {abs(h)})') if h else f)
    if f == '2ˣ' and h:
        inner = f'2^(x {"−" if h > 0 else "+"} {abs(h)})'
    if f == 'log x' and h:
        inner = f'log (x {"−" if h > 0 else "+"} {abs(h)})'
    g_ = inner + (f' {"+" if k > 0 else "−"} {abs(k)}' if k else '')
    if h:
        u = 'unit' if abs(h) == 1 else 'units'
        ans = f'shifting the graph of y = {f} by {abs(h)} {u} to the {"right" if h > 0 else "left"}'
        wr = [f'shifting the graph of y = {f} by {abs(h)} {u} to the {"left" if h > 0 else "right"}', f'shifting the graph of y = {f} by {abs(h)} {u} {"up" if h > 0 else "down"}',
              f'stretching the graph of y = {f} vertically by a factor {abs(h)}']
    else:
        u = 'unit' if abs(k) == 1 else 'units'
        ans = f'shifting the graph of y = {f} by {abs(k)} {u} {"up" if k > 0 else "down"}'
        wr = [f'shifting the graph of y = {f} by {abs(k)} {u} {"down" if k > 0 else "up"}', f'shifting the graph of y = {f} by {abs(k)} {u} to the {"right" if k > 0 else "left"}',
              f'stretching the graph of y = {f} vertically by a factor {abs(k)}']
    return mcq(f'The graph of y = {g_} is obtained by', ans, wr, 'y = f(x − h) shifts right by h (left if h < 0); y = f(x) + k shifts up by k (down if k < 0).', r)


def c4s3_vertex(r):
    h, k = r.choice([x for x in range(-5, 6) if x]), r.choice([x for x in range(-5, 6) if x])
    f = r.choice(['|x', '(x'])
    hs = f'x {"−" if h >= 0 else "+"} {abs(h)}'
    g_ = (f'|{hs}|' if f == '|x' else f'({hs})²') + (f' {"+" if k >= 0 else "−"} {abs(k)}' if k else '')
    nm = 'modulus graph (V shape)' if f == '|x' else 'parabola'
    return Q(f'Write the vertex of the graph of y = {g_} and state its range. Describe how it is obtained from the graph of y = {"|x|" if f == "|x" else "x²"}.',
             f'vertex ({h}, {k}); range [{k}, ∞); shift {abs(h)} units {"right" if h >= 0 else "left"} and {abs(k)} units {"up" if k >= 0 else "down"}',
             f'The {nm} has its lowest point where the bracket is 0, at x = {h}, y = {k} (1); range [{k}, ∞) (½); translation described (½).',
             [f'vertex ({-h}, {k}); range [{k}, ∞)', f'vertex ({h}, {-k}); range [{-k}, ∞)', f'vertex ({k}, {h}); range [{h}, ∞)'])


def c4s3_reflect(r):
    f = r.choice(['x²', '|x|', '2ˣ', 'x³', '√x'])
    t = r.choice(['−f(x)', 'f(−x)', '2f(x)'])
    d = {'−f(x)': 'reflection of the graph in the x-axis', 'f(−x)': 'reflection of the graph in the y-axis', '2f(x)': 'vertical stretch of the graph by a factor of 2'}
    wrong = [v for k_, v in d.items() if k_ != t] + ['reflection of the graph in the line y = x']
    return mcq(f'If f(x) = {f}, the graph of y = {t} is the', d[t], wrong, f'{t}: {d[t]}.', r)


def c4s3_intercepts(r):
    a, b = r.randint(1, 5), r.randint(1, 6)
    k = r.choice([1, 2, 3])
    # y = (x - a)^2 - b^2 k ... keep integer roots: y = (x − a)² − m², roots a ± m
    m = r.randint(1, 4)
    yint = a * a - m * m
    return Q(f'The graph of y = x² is shifted {a} units to the right and {m * m} units down. Write the equation of the new graph and find where it cuts the x-axis and the y-axis.',
             f'y = (x − {a})² − {m * m}; x-intercepts {a - m} and {a + m}; y-intercept {yint}', f'Shift right: x → x − {a}; down: subtract {m * m} (1). y = 0 ⇒ x − {a} = ±{m} (1). x = 0 ⇒ y = {yint} (1).',
             [f'y = (x + {a})² − {m * m}; x-intercepts {-a - m} and {-a + m}', f'y = (x − {a})² + {m * m}; no x-intercepts', f'y = (x − {a})² − {m * m}; x-intercepts {a} and {m}'])


def c4s3_table(r):
    f = r.choice([('|x − 2|', lambda x: abs(x - 2)), ('x² − 4', lambda x: x * x - 4), ('2ˣ', lambda x: Fr(2) ** x), ('[x] + 1', lambda x: math.floor(x) + 1), ('3 − |x|', lambda x: 3 - abs(x))])
    xs = [-2, -1, 0, 1, 2, 3]
    vals = [fs(f[1](x)) for x in xs]
    return {'stem': f'Complete a table of values of y = {f[0]} for x = −2, −1, 0, 1, 2, 3 and use it to sketch the graph. State the range of the function on these points.',
            'answer': '; '.join(f'({x}, {v})' for x, v in zip(xs, vals)) + f'. Range on these points {{{", ".join(sorted(set(vals), key=lambda s: Fr(s.replace("−", "-"))))}}}.',
            'key': 'Correct table (1); plotted points joined suitably (1); range (1).'}


def c4s3_ar(r):
    h = r.randint(1, 6)
    if r.random() < 0.5:
        return ar(f'The graph of y = (x − {h})² is the graph of y = x² shifted {h} units to the right.', 'The graph of y = f(x − h), h > 0, is the graph of y = f(x) shifted h units to the right.', 'a', 'R is the general rule; A applies it.')
    return ar(f'The graph of y = (x + {h})² is the graph of y = x² shifted {h} units to the right.', 'The graph of y = f(x − h), h > 0, is the graph of y = f(x) shifted h units to the right.', 'd', f'A is false: (x + {h})² = f(x − (−{h})) shifts {h} units to the left. R is true.')


def c4s3_explain(r):
    a, k = r.randint(2, 6), r.randint(2, 6)
    return {'stem': f'Explain, step by step, how the graph of y = |x + {a}| − {k} can be drawn from the graph of y = |x|. Where is its vertex?',
            'answer': f'Shift y = |x| {a} units left to get y = |x + {a}|, then {k} units down. Vertex (−{a}, −{k}).', 'key': 'Horizontal shift (½), vertical shift (½), vertex (1).'}


def c4s3_case(r):
    F0 = r.choice([100, 150, 200])
    v = r.choice([5, 8, 10, 12])
    up = r.choice([50, 75, 100])
    q = r.randint(10, 40)
    return {'stem': (f'A courier company charges C(x) = {F0} + {v}x rupees to deliver a parcel of x kg. During the festival season it adds a flat surcharge of ₹{up} to every parcel.\n'
                     f'(i) Write the new charge function N(x). (1)\n(ii) Describe how the graph of N is obtained from that of C. (1)\n(iii) Find C({q}) and N({q}), and state whether the slope changes. (2)'),
            'answer': f'(i) N(x) = {F0 + up} + {v}x (ii) shift the graph of C up by {up} units (iii) C({q}) = ₹{F0 + v * q}, N({q}) = ₹{F0 + up + v * q}; slope stays {v}',
            'key': '(i) add constant (1). (ii) vertical translation (1). (iii) two values (1), slope unchanged (1).'}


c4s3_tf = tf_mcq('graphs of functions', [
    'The graph of y = f(x) + 3 is the graph of y = f(x) moved 3 units up.', 'The graph of y = −f(x) is the reflection of y = f(x) in the x-axis.',
    'The graph of y = |x| is V-shaped with vertex at the origin.', 'The graph of y = 2ˣ lies entirely above the x-axis.', 'The graph of y = log x cuts the x-axis at (1, 0).'],
    ['The graph of y = f(x − 3) is the graph of y = f(x) moved 3 units to the left.', 'The graph of y = f(−x) is the reflection of y = f(x) in the x-axis.',
     'The graph of y = 2ˣ cuts the x-axis at (0, 1).', 'The graph of y = log x is defined for all real x.', 'The graph of y = [x] is a straight line.'])

# st4 composition and inverse


def c4s4_comp(r):
    a, b = r.choice([1, 2, 3, -1, 4]), r.randint(-5, 5)
    p, q = r.choice([1, 2, 3, -2]), r.randint(-5, 5)
    x0 = r.randint(-3, 4)
    which = r.choice(['fog', 'gof'])
    f = lambda x: x * x + a * x + b
    g_ = lambda x: p * x + q
    v = f(g_(x0)) if which == 'fog' else g_(f(x0))
    fs_ = poly([1, a, b])
    gs_ = lin(p, q)
    w = g_(f(x0)) if which == 'fog' else f(g_(x0))
    return Q(f'If f(x) = {fs_} and g(x) = {gs_}, find ({which[0]}o{which[2]})({x0}).', str(v),
             f'{"g(" + str(x0) + ") = " + str(g_(x0)) + ", f(" + str(g_(x0)) + ") = " + str(v) if which == "fog" else "f(" + str(x0) + ") = " + str(f(x0)) + ", g(" + str(f(x0)) + ") = " + str(v)}.',
             nd(str(v), [str(w), str(f(x0) * g_(x0)), str(f(x0) + g_(x0)), str(v + 1)]))


def c4s4_compexpr(r):
    a, b = r.choice([2, 3, -1, 4, 5]), r.randint(-6, 6)
    p, q = r.choice([2, 3, -2, 1]), r.randint(-6, 6)
    fog = lin(a * p, a * q + b)
    gof = lin(a * p, p * b + q)
    return Q(f'If f(x) = {lin(a, b)} and g(x) = {lin(p, q)}, find fog(x) and gof(x). Is fog = gof?', f'fog(x) = {fog}; gof(x) = {gof}; {"equal" if fog == gof else "not equal"}',
             f'fog(x) = f({lin(p, q)}) = {fog} (1); gof(x) = g({lin(a, b)}) = {gof} (1); compare (1).', [f'fog(x) = {gof}; gof(x) = {fog}', f'fog(x) = {lin(a + p, b + q)}; gof(x) = {lin(a + p, b + q)}', f'fog(x) = {lin(a * p, b * q)}; gof(x) = {lin(a * p, b * q)}'])


def c4s4_inv(r):
    a, b = r.choice([2, 3, 4, 5, -2, -3]), r.choice([x for x in range(-9, 10) if x])
    inv = f'(x {"−" if b > 0 else "+"} {abs(b)})/{a}' if a > 0 else f'({b} − x)/{abs(a)}'.replace('(-', '(−')
    return Q(f'Find the inverse of f(x) = {lin(a, b)}, x ∈ R.', f'f⁻¹(x) = {inv}', f'Put y = {lin(a, b)} and solve for x: x = (y − ({b}))/({a}); interchange x and y: f⁻¹(x) = {inv}.',
             [f'f⁻¹(x) = 1/({lin(a, b)})', f'f⁻¹(x) = {lin(a, -b)}', f'f⁻¹(x) = (x {"+" if b > 0 else "−"} {abs(b)})/{a}'])


def c4s4_invrat(r):
    a, b, c, d = r.randint(1, 5), r.randint(-5, 5), r.randint(1, 4), r.randint(-5, 5)
    if a * d - b * c == 0 or a == -d:
        raise ValueError
    # y = (ax + b)/(cx + d) -> x = (dy - b)/(a - cy) => f^-1(x) = (dx - b)/(a - cx)
    num_, den_ = (d, -b), (-c, a)
    if -c < 0:
        num_, den_ = (-d, b), (c, -a)
    top = lin(*num_) if num_[0] else fs(num_[1])
    return Q(f'Find f⁻¹(x) for f(x) = ({lin(a, b)})/({lin(c, d)}), x ≠ {fs(Fr(-d, c))}.', f'f⁻¹(x) = ({top})/({lin(*den_)})',
             f'y(cx + d) = ax + b ⇒ x(cy − a) = b − dy ⇒ x = (dy − b)/(a − cy) (2); interchange x and y (1).')


def c4s4_check(r):
    a, b = r.choice([2, 3, 5, 4]), r.randint(1, 9)
    return {'stem': f'Show that f(x) = {lin(a, b)} and g(x) = (x − {b})/{a} are inverses of each other by finding fog and gof.',
            'answer': f'fog(x) = {a}((x − {b})/{a}) + {b} = x; gof(x) = ({lin(a, b)} − {b})/{a} = x. Both are the identity, so g = f⁻¹.',
            'key': 'fog = x (1); gof = x (1); conclusion (½ + ½).'}


def c4s4_ar(r):
    a, b = r.choice([2, 3, 4]), r.randint(1, 6)
    if r.random() < 0.5:
        return ar(f'The inverse of f(x) = {lin(a, b)} is f⁻¹(x) = (x − {b})/{a}.', 'f and f⁻¹ satisfy fof⁻¹(x) = f⁻¹of(x) = x.', 'a', f'f((x − {b})/{a}) = x; R gives the test.')
    return ar(f'For f(x) = x + {b} and g(x) = {a}x, fog = gof.', 'Composition of functions is not commutative in general.', 'd', f'A is false: fog(x) = {a}x + {b}, gof(x) = {a}x + {a * b}. R is true.')


c4s4_tf = tf_mcq('composition and inverse of functions', [
    'In general fog ≠ gof.', 'A function has an inverse only if it is one-one and onto.', 'The graph of f⁻¹ is the reflection of the graph of f in the line y = x.',
    'If f(x) = 2x, then f⁻¹(x) = x/2.', '(fog)(x) means f(g(x)).'],
    ['fog = gof for all functions f and g.', 'f⁻¹(x) means 1/f(x).', 'Every function has an inverse.', '(fog)(x) means g(f(x)).', 'The graph of f⁻¹ is the reflection of the graph of f in the x-axis.'])


def c4s4_case(r):
    c = r.choice([80, 85, 90])
    fee = r.choice([20, 30, 50])
    pct = r.choice([2, 5])
    usd = r.choice([100, 200, 500])
    return {'stem': (f'A currency exchange counter at {r.choice(CITIES)} airport converts US dollars to rupees using f(x) = {c}x (x in dollars) and then deducts a service charge: g(y) = y − {fee} (y in rupees).\n'
                     f'(i) Find (gof)(x) and explain what it represents. (1)\n(ii) How many rupees does a traveller get for ${usd}? (1)\n'
                     f'(iii) Find the inverse of gof and use it to find how many dollars must be exchanged to receive ₹{c * usd - fee + c * 10}. (2)'),
            'answer': f'(i) (gof)(x) = {c}x − {fee}: rupees received for x dollars (ii) ₹{c * usd - fee} (iii) (gof)⁻¹(x) = (x + {fee})/{c}; ${usd + 10}',
            'key': '(i) composition (1). (ii) substitution (1). (iii) inverse (1), value (1).'}


# ======================================================== FAMILIES

FAMILIES = {
    S + '01-st1': [F('C1', 'D1', 'mcq', c1s1_place), F('C1', 'D2', 'mcq', c1s1_valid), F('C1', 'D2', 'mcq', c1s1_tf), F('C2', 'D2', 'explain', c1s1_explain),
                   F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)), F('C2', 'D2', 'short', c1s1_b2d), F('C3', 'D1', 'short', c1s1_d2b), F('C3', 'D2', 'numerical', c1s1_add),
                   F('C3', 'D3', 'numerical', c1s1_frac), F('C4', 'D3', 'multi_step', c1s1_mult), F('C3', 'D3', 'case', c1s1_case, marks=4, minutes=6)],
    S + '01-st2': [F('C1', 'D1', 'mcq', c1s2_logbase), F('C1', 'D2', 'mcq', c1s2_tf), F('C2', 'D2', 'explain', c1s2_explain), F('C2', 'D3', 'mcq', c1s2_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c1s2_index), F('C3', 'D1', 'short', c1s2_loglaw), F('C3', 'D2', 'numerical', c1s2_known), F('C3', 'D3', 'numerical', c1s2_antilog),
                   F('C3', 'D4', 'numerical', c1s2_digits), F('C4', 'D3', 'multi_step', c1s2_expeq), F('C4', 'D5', 'long', c1s2_prove, kinds=('long5',)),
                   F('C3', 'D3', 'case', c1s2_case, marks=4, minutes=6)],
    S + '01-st3': [F('C1', 'D1', 'mcq', c1s3_oddmcq), F('C1', 'D2', 'mcq', c1s3_leapmcq), F('C2', 'D2', 'explain', c1s3_explain), F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c1s3_after), F('C3', 'D1', 'short', c1s3_angle), F('C3', 'D2', 'numerical', c1s3_date), F('C3', 'D3', 'numerical', c1s3_coincide),
                   F('C4', 'D3', 'multi_step', c1s3_history), F('C4', 'D4', 'multi_step', c1s3_gain), F('C4', 'D4', 'numerical', c1s3_repeat),
                   F('C3', 'D3', 'case', c1s3_case, marks=4, minutes=6)],
    S + '01-st4': [F('C1', 'D1', 'mcq', c1s4_conv), F('C1', 'D2', 'mcq', c1s4_tf), F('C2', 'D2', 'explain', c1s4_avg_explain), F('C2', 'D3', 'mcq', c1s4_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c1s4_avg), F('C3', 'D1', 'short', c1s4_pole), F('C3', 'D2', 'numerical', c1s4_platform), F('C3', 'D3', 'numerical', c1s4_two),
                   F('C3', 'D4', 'multi_step', c1s4_boat), F('C4', 'D3', 'multi_step', c1s4_meet), F('C4', 'D4', 'long', c1s4_late, kinds=('long5',)),
                   F('C3', 'D3', 'case', c1s4_case, marks=4, minutes=6)],
    S + '01-st5': [F('C1', 'D1', 'mcq', c1s5_rate), F('C1', 'D2', 'mcq', c1s5_tf), F('C2', 'D2', 'explain', c1s5_explain), F('C2', 'D3', 'mcq', c1s5_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c1s5_together), F('C3', 'D2', 'numerical', c1s5_pipes), F('C3', 'D3', 'numerical', c1s5_leave), F('C3', 'D2', 'numerical', c1s5_wages),
                   F('C4', 'D3', 'multi_step', c1s5_seat), F('C4', 'D4', 'multi_step', c1s5_path, kinds=('long5',)), F('C3', 'D3', 'numerical', c1s5_tank),
                   F('C3', 'D3', 'case', c1s5_case, marks=4, minutes=6)],
    S + '02-st1': reuse('01-st1') + reuse('01-st2') + reuse('01-st3'),
    S + '02-st2': reuse('01-st4') + reuse('01-st5'),
    S + '02-st3': reuse('02-st1') + reuse('02-st2'),
    S + '02-st4': [F('C1', 'D1', 'mcq', c2s4_terms), F('C1', 'D2', 'mcq', c2s4_tf), F('C2', 'D2', 'explain', c2s4_mod), F('C2', 'D3', 'mcq', c2s4_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', c2s4_classify), F('C3', 'D1', 'short', c2s4_add), F('C3', 'D2', 'numerical', c2s4_class), F('C3', 'D3', 'numerical', c2s4_count),
                   F('C4', 'D3', 'multi_step', c2s4_rule), F('C4', 'D5', 'long', c2s4_equiv_add, kinds=('long5',)), F('C3', 'D3', 'case', c2s4_case, marks=4, minutes=6)],
    S + '03-st1': reuse('08-st2') + reuse('08-st1'),
    S + '03-st2': reuse('08-st3', skip=(6,)) + [F('C1', 'D1', 'mcq', c3s2_infmcq), F('C2', 'D3', 'mcq', c3s2_infar, kinds=('ar',)), F('C3', 'D2', 'numerical', c3s2_inf),
                                     F('C3', 'D3', 'numerical', c3s2_rec), F('C4', 'D3', 'numerical', c3s2_findr), F('C4', 'D4', 'multi_step', c3s2_bounce, kinds=('long5',))],
    S + '03-st3': reuse('08-st4'),
    S + '03-st4': [F('C1', 'D1', 'mcq', c3s4_formula), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c3s4_eval),
                   F('C3', 'D2', 'numerical', c3s4_range), F('C3', 'D3', 'numerical', c3s4_prod), F('C4', 'D3', 'multi_step', c3s4_nterm), F('C3', 'D3', 'case', c3s4_case, marks=4, minutes=6)],
    S + '04-st1': [F('C1', 'D1', 'mcq', c4s1_dep), F('C1', 'D2', 'mcq', c4s1_tf), F('C2', 'D2', 'explain', c4s1_explain), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)),
                   F('C2', 'D2', 'short', c4s1_sqrt), F('C3', 'D1', 'short', c4s1_rational), F('C3', 'D2', 'numerical', c4s1_range_lin), F('C3', 'D3', 'numerical', c4s1_range_quad),
                   F('C4', 'D3', 'multi_step', c4s1_context), F('C3', 'D3', 'case', c4s1_case, marks=4, minutes=6)] + reuse('02-st3', skip=(0, 1, 2, 3, 4, 5, 6, 7, 10)),
    S + '04-st2': reuse('02-st3', skip=(8, 9)) + [F('C1', 'D1', 'mcq', c4s2_type), F('C2', 'D2', 'short', c4s2_step), F('C3', 'D2', 'numerical', c4s2_exp),
                                                  F('C3', 'D2', 'short', c4s2_logdom), F('C3', 'D1', 'short', c4s2_mod), F('C4', 'D3', 'multi_step', c4s2_tax)] + reuse('02-st4'),
    S + '04-st3': [F('C1', 'D1', 'mcq', c4s3_reflect), F('C1', 'D2', 'mcq', c4s3_tf), F('C2', 'D2', 'explain', c4s3_explain), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', c4s3_shift), F('C3', 'D2', 'numerical', c4s3_vertex), F('C3', 'D3', 'multi_step', c4s3_intercepts), F('C4', 'D3', 'multi_step', c4s3_table),
                   F('C3', 'D3', 'case', c4s3_case, marks=4, minutes=6)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_tf), F('C2', 'D2', 'explain', c4s4_check), F('C2', 'D3', 'mcq', c4s4_ar, kinds=('ar',)), F('C3', 'D1', 'short', c4s4_comp),
                   F('C3', 'D2', 'numerical', c4s4_compexpr), F('C3', 'D2', 'short', c4s4_inv), F('C4', 'D4', 'multi_step', c4s4_invrat, kinds=('long5',)),
                   F('C3', 'D3', 'case', c4s4_case, marks=4, minutes=6)],
}
