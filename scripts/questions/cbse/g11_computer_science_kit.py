"""Shared code families for the CBSE class 11 Computer Science (083) and Informatics Practices (065) banks.

Every answer here is computed: conversions with int()/format(), Boolean expressions by evaluating them over all
inputs, character codes with ord()/str.encode(), and every Python output, exception name or program check by running
the code (g12_computer_science_kit.run / exc). Families take r (random.Random) and return a variant dict.
"""
from __future__ import annotations

import itertools
import keyword
from fractions import Fraction

from qbank import mcq, ar
from g12_computer_science_kit import run, exc, run_or_err, uniq, NAMES, WORDS, SENTS, compiles

PIPE = ' | '


def more_wrong(out):
    """Plausible slips of a computed output: off-by-one numbers, reordered or truncated sequences, changed case."""
    import ast
    w = []
    o = out.strip()
    try:
        v = ast.literal_eval(o)
    except Exception:
        v = None
    if isinstance(v, bool):
        w += [str(not v)]
    elif isinstance(v, int):
        w += [str(v + 1), str(v - 1), str(v * 2), str(v + 10)]
    elif isinstance(v, float):
        w += [str(int(v)) if v != int(v) else str(int(v)), str(v + 1), str(round(v * 2, 2))]
    elif isinstance(v, (list, tuple)) and v:
        seqs = [v[::-1], v[1:], v[:-1], v[1:] + v[:1]]
        w += [repr(type(v)(x)) if not isinstance(v, tuple) else repr(tuple(x)) for x in seqs]
    elif isinstance(v, dict) and v:
        ks = list(v)
        w += [repr({k: v[k] for k in ks[1:]}), repr(dict(zip(ks, list(v.values())[::-1]))), repr(list(v))]
    toks = o.split(' ')
    if len(toks) > 1:
        w.append(' '.join(toks[::-1]))
        for i, t in enumerate(toks):
            if t.lstrip('-').isdigit():
                tt = toks[:]
                tt[i] = str(int(t) + 1)
                w.append(' '.join(tt))
            elif t in ('True', 'False'):
                tt = toks[:]
                tt[i] = 'False' if t == 'True' else 'True'
                w.append(' '.join(tt))
    if v is None and o:
        w += [o[::-1], o.swapcase(), o[:-1] if len(o) > 1 else o + o]
    return [x for x in w if x and x.strip() != o]


def fill(wrong, out, n=3):
    w = uniq(list(wrong) + more_wrong(out), [out])
    if len(w) < n:
        raise ValueError('few')
    return w


def _py(x):
    return x


# ====================================================================== memory units
UNITS = ['bit', 'nibble', 'byte', 'KB', 'MB', 'GB', 'TB', 'PB']
UNIT_BITS = {'bit': 1, 'nibble': 4, 'byte': 8}
for _i, _u in enumerate(['KB', 'MB', 'GB', 'TB', 'PB']):
    UNIT_BITS[_u] = 8 * 1024 ** (_i + 1)


def unit_convert(r):
    """Memory-unit conversion (1 KB = 1024 bytes as in NCERT)."""
    t = r.randrange(4)
    if t == 0:
        big = r.choice(['KB', 'MB', 'GB', 'TB'])
        small = UNITS[UNITS.index(big) - 1]
        n = r.randint(2, 64)
        ans = n * UNIT_BITS[big] // UNIT_BITS[small]
        stem = f'How many {small}s are there in {n} {big}?'
        wrong = [n * 1000, n * 1024 * 1024 if small != 'byte' else n * 8, n * 512, ans // 2 if ans % 2 == 0 else ans * 2]
    elif t == 1:
        n = r.choice([2, 4, 8, 16, 32, 64, 128])
        ans = n * 8
        stem = f'How many bits are there in {n} bytes?'
        wrong = [n * 4, n * 1024, n // 8 if n >= 8 else n * 16, n * 2]
    elif t == 2:
        n = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
        ans = n * 1024 * 1024
        stem = f'How many KB are there in {n} GB?'
        wrong = [n * 1000 * 1000, n * 1024, n * 1024 * 1024 * 1024, n * 1000]
    else:
        n = r.choice([4, 8, 12, 16, 20, 24, 32, 40])
        stem = f'How many nibbles make up {n // 2} bytes?'
        ans = n
        wrong = [n // 2, n * 2, n * 4, n // 4 if n >= 8 else n + 2]
    wrong = [str(w) for w in uniq([str(w) for w in wrong], [str(ans)]) if str(w) != '0'][:3]
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(stem, str(ans), wrong, f'1 nibble = 4 bits, 1 byte = 8 bits, 1 KB = 1024 bytes and each larger unit is 1024 times the one before. Answer: {ans}.', r)


def unit_written(r):
    """Two-part written conversion with working."""
    a = r.choice([2, 3, 4, 5, 6, 8])
    b = r.choice([3, 5, 6, 7, 10, 12])
    big1, big2 = r.sample(['MB', 'GB', 'TB'], 2)
    s1 = UNITS[UNITS.index(big1) - 1]
    v1 = a * 1024
    v2 = b * UNIT_BITS[big2] // 8
    return {'stem': f'Convert: (i) {a} {big1} into {s1}s (ii) {b} {big2} into bytes. Show the steps.',
            'answer': f'(i) {a} × 1024 = {v1} {s1}s (ii) {b} {big2} = {b} × 1024^{UNITS.index(big2) - 2} bytes = {v2} bytes',
            'key': f'1 mark each: (i) {v1} {s1}s (ii) {v2} bytes (1 KB = 1024 bytes; each unit is 1024 times the previous).', 'marks': 2}


# ====================================================================== number systems
BASES = {2: 'binary', 8: 'octal', 10: 'decimal', 16: 'hexadecimal'}


def tob(n, b):
    return {2: format(n, 'b'), 8: format(n, 'o'), 10: str(n), 16: format(n, 'X')}[b]


def lab(s, b):
    return f'({s}){b}'


def _conv_wrong(n, b):
    s = tob(n, b)
    w = [tob(n + 1, b), tob(n - 1, b), s[::-1], tob(n * 2, b), tob(n + b, b)]
    return uniq([x for x in w if x != s and x], [s])


def dec_to_base(r):
    b = r.choice([2, 2, 8, 16])
    n = r.randint(20, 255) if b == 2 else r.randint(60, 999)
    s = tob(n, b)
    wrong = _conv_wrong(n, b)
    if s[::-1] == s:
        raise ValueError('palindrome')
    steps = []
    m = n
    while m:
        steps.append(f'{m} ÷ {b} = {m // b} r {tob(m % b, 16)}')
        m //= b
    return mcq(f'What is the {BASES[b]} equivalent of the decimal number {n}?', lab(s, b), [lab(x, b) for x in wrong[:3]],
               f'Repeated division by {b}: ' + '; '.join(steps) + f'. Reading remainders from bottom to top gives {s}.', r)


def base_to_dec(r):
    b = r.choice([2, 2, 8, 16])
    n = r.randint(20, 255) if b == 2 else r.randint(60, 999)
    s = tob(n, b)
    digs = list(s)
    terms = ' + '.join(f'{int(d, 16)}×{b}^{len(s) - 1 - i}' for i, d in enumerate(digs))
    wrong = uniq([str(n + 1), str(n - 1), str(int(s[::-1], b)), str(n + b), str(n * 2)], [str(n)])
    return mcq(f'What is the decimal equivalent of {lab(s, b)}?', str(n), wrong[:3], f'{terms} = {n}.', r)


def conv_written(r):
    """Short answer (1 mark) conversion in either direction."""
    b = r.choice([2, 8, 16])
    n = r.randint(30, 255) if b == 2 else r.randint(100, 1500)
    s = tob(n, b)
    if r.random() < 0.5:
        return {'stem': f'Convert the decimal number {n} into its {BASES[b]} equivalent.', 'answer': lab(s, b),
                'key': f'1 mark: repeated division of {n} by {b}, remainders read from bottom to top: {lab(s, b)}.',
                'distractors': [lab(x, b) for x in _conv_wrong(n, b)[:3]], 'marks': 1}
    terms = ' + '.join(f'{int(d, 16)}×{b}^{len(s) - 1 - i}' for i, d in enumerate(s))
    return {'stem': f'Convert {lab(s, b)} into its decimal equivalent.', 'answer': f'({n})10',
            'key': f'1 mark: {terms} = {n}.', 'distractors': [f'({x})10' for x in (n + 1, n - 1, int(s[::-1], b))], 'marks': 1}


def group_conv(r):
    """Binary <-> octal / hexadecimal by grouping bits."""
    n = r.randint(64, 4095)
    s = tob(n, 2)
    t = r.randrange(4)
    if t == 0:
        b, size = 8, 3
    elif t == 1:
        b, size = 16, 4
    elif t == 2:
        b, size = 8, 3
    else:
        b, size = 16, 4
    pad = s.zfill((len(s) + size - 1) // size * size)
    groups = [pad[i:i + size] for i in range(0, len(pad), size)]
    tgt = tob(n, b)
    if t < 2:
        stem = f'Convert {lab(s, 2)} into its {BASES[b]} equivalent.'
        ans = lab(tgt, b)
        key = f'Group the bits in {size}s from the right: {" ".join(groups)} → {" ".join(tob(int(g, 2), 16) for g in groups)}, so the answer is {ans}.'
        wrong = [lab(x, b) for x in _conv_wrong(n, b)[:3]]
    else:
        stem = f'Convert {lab(tgt, b)} into its binary equivalent.'
        ans = lab(s, 2)
        key = f'Write each {BASES[b]} digit as {size} bits: {" ".join(groups)}; dropping leading zeros gives {ans}.'
        wrong = [lab(x, 2) for x in uniq([tob(n + 1, 2), tob(n ^ 1 << r.randint(1, 4), 2), s[::-1], tob(n - 1, 2)], [s])[:3]]
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(stem, ans, wrong, key, r)


def oct_hex(r):
    n = r.randint(64, 4095)
    if r.random() < 0.5:
        src, dst = 8, 16
    else:
        src, dst = 16, 8
    s, tgt = tob(n, src), tob(n, dst)
    b = tob(n, 2)
    return {'stem': f'Convert {lab(s, src)} into its {BASES[dst]} equivalent using binary as the intermediate form.',
            'answer': f'{lab(s, src)} = {lab(b, 2)} = {lab(tgt, dst)}',
            'key': f'2 marks: 1 for the binary form {b}, 1 for regrouping it into {lab(tgt, dst)}.',
            'distractors': [lab(x, dst) for x in _conv_wrong(n, dst)[:3]], 'marks': 2}


def _bin_frac(fr: Fraction, places=8):
    out = ''
    while fr and len(out) < places:
        fr *= 2
        out += '1' if fr >= 1 else '0'
        if fr >= 1:
            fr -= 1
    return out


def frac_to_bin(r):
    ip = r.randint(1, 63)
    m = r.choice([2, 3, 3, 4])
    k = r.choice([x for x in range(1, 2 ** m) if x % 2 == 1])
    fr = Fraction(k, 2 ** m)
    dec = ip + k / 2 ** m
    bits = _bin_frac(fr)
    ans = f'({tob(ip, 2)}.{bits})2'
    steps = []
    f2 = fr
    while f2:
        f2 *= 2
        steps.append(f'{float(f2 / 2):g} × 2 = {float(f2):g} → {int(f2 >= 1)}')
        if f2 >= 1:
            f2 -= 1
    wrong = uniq([f'({tob(ip, 2)}.{bits[::-1]})2', f'({tob(ip, 2)[::-1]}.{bits})2', f'({tob(ip + 1, 2)}.{bits})2', f'({tob(ip, 2)}.{tob(k, 2)}1)2'], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Convert the decimal number {dec:g} into binary.', 'answer': ans,
            'key': f'2 marks: integer part {ip} = {tob(ip, 2)} (repeated division by 2); fractional part by repeated multiplication by 2: '
                   + '; '.join(steps) + f'. Answer {ans}.', 'distractors': wrong[:3], 'marks': 2}


def bin_frac_to_dec(r):
    ip = r.randint(1, 31)
    m = r.choice([2, 3, 4])
    k = r.choice([x for x in range(1, 2 ** m) if x % 2 == 1])
    bits = format(k, f'0{m}b')
    val = ip + k / 2 ** m
    terms = ' + '.join(f'{d}×2^-{i + 1}' for i, d in enumerate(bits))
    ans = f'{val:g}'
    wrong = uniq([f'{ip + int(bits) / 10 ** m:g}', f'{ip + k / 10:g}', f'{ip + int(bits[::-1], 2) / 2 ** m:g}', f'{ip + 1 + k / 2 ** m:g}'], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'What is the decimal equivalent of ({tob(ip, 2)}.{bits})2?', ans, wrong[:3],
               f'Integer part {tob(ip, 2)} = {ip}; fractional part {terms} = {k / 2 ** m:g}; total {ans}.', r)


def valid_number(r):
    b = r.choice([2, 8, 16])
    digits = {2: '01', 8: '01234567', 16: '0123456789ABCDEF'}[b]
    bad_digits = {2: '23456789', 8: '89', 16: 'GHJK'}[b]
    good = [''.join(r.choice(digits[1:]) + ''.join(r.choice(digits) for _ in range(r.randint(2, 4))))]
    bad = []
    while len(bad) < 3:
        s = list(r.choice(digits[1:]) + ''.join(r.choice(digits) for _ in range(r.randint(2, 4))))
        s[r.randrange(len(s))] = r.choice(bad_digits)
        bad.append(''.join(s))
    bad = uniq(bad)
    if len(bad) < 3:
        raise ValueError('few')
    if r.random() < 0.5:
        return mcq(f'Which of the following is a valid {BASES[b]} number?', good[0], bad[:3],
                   f'A {BASES[b]} number may use only the digits {", ".join(digits) if b != 16 else "0–9 and A–F"}.', r)
    goods = [''.join(r.choice(digits[1:]) + ''.join(r.choice(digits) for _ in range(3))) for _ in range(3)]
    goods = uniq(goods)
    if len(goods) < 3:
        raise ValueError('few')
    return mcq(f'Which of the following is NOT a valid {BASES[b]} number?', bad[0], goods[:3],
               f'{bad[0]} contains a digit that is not allowed in base {b}.', r)


def compare_bases(r):
    vals = r.sample(range(40, 250), 4)
    bs = r.sample([2, 8, 10, 16], 4)
    reps = [lab(tob(v, b), b) for v, b in zip(vals, bs)]
    mx = reps[vals.index(max(vals))]
    if r.random() < 0.5:
        return mcq('Which of the following numbers has the largest value?', mx, [x for x in reps if x != mx],
                   'In decimal: ' + ', '.join(f'{x} = {v}' for x, v in zip(reps, vals)) + f'; the largest is {mx}.', r)
    mn = reps[vals.index(min(vals))]
    return mcq('Which of the following numbers has the smallest value?', mn, [x for x in reps if x != mn],
               'In decimal: ' + ', '.join(f'{x} = {v}' for x, v in zip(reps, vals)) + f'; the smallest is {mn}.', r)


def conv_multi(r):
    """3-mark multi-step: three conversions with working."""
    n1 = r.randint(100, 500)
    n2 = r.randint(64, 1023)
    n3 = r.randint(256, 4000)
    f_ip, f_k = r.randint(2, 30), r.choice([1, 3, 5, 7])
    dec = f_ip + f_k / 8
    a1 = tob(n1, 8)
    a2 = tob(n2, 16)
    a3 = f'{tob(f_ip, 2)}.{format(f_k, "03b")}'
    return {'stem': f'Convert the following, showing your working:\n(i) ({n1})10 to octal\n(ii) ({tob(n2, 2)})2 to hexadecimal\n(iii) ({dec:g})10 to binary',
            'answer': f'(i) ({a1})8 (ii) ({a2})16 (iii) ({a3})2',
            'key': f'1 mark each: (i) repeated division by 8 gives {a1}; (ii) groups of 4 bits give {a2}; (iii) {f_ip} = {tob(f_ip, 2)} and '
                   f'{f_k / 8:g} × 2 repeatedly gives .{format(f_k, "03b")}, so {a3}.', 'marks': 3}


def colour_case(r):
    """4-mark case: hexadecimal colour codes."""
    who = r.choice(NAMES)
    rgb = [r.randint(16, 255) for _ in range(3)]
    code = ''.join(format(x, '02X') for x in rgb)
    comp = r.randrange(3)
    names = ['red', 'green', 'blue']
    return {'stem': (f'{who} is designing a school website. The colour of the heading is written as the hexadecimal code #{code}, '
                     f'where the first two digits give the red value, the next two the green value and the last two the blue value.\n'
                     f'(i) Why do designers prefer hexadecimal over binary for such codes? (1)\n(ii) Find the decimal value of each of red, green and blue. (2)\n'
                     f'(iii) Write the {names[comp]} value in binary. (1)'),
            'answer': (f'(i) Each hexadecimal digit stands for 4 bits, so the code is short and easy to read. (ii) red = {rgb[0]}, green = {rgb[1]}, blue = {rgb[2]} '
                       f'(iii) {tob(rgb[comp], 2).zfill(8)}'),
            'key': (f'1 + 2 + 1 marks: (ii) e.g. {code[:2]} = {int(code[0], 16)}×16 + {int(code[1], 16)} = {rgb[0]}; (iii) each hexadecimal digit as 4 bits: '
                    f'{code[2 * comp]} = {format(int(code[2 * comp], 16), "04b")}, {code[2 * comp + 1]} = {format(int(code[2 * comp + 1], 16), "04b")}.'),
            'marks': 4}


# ====================================================================== encoding
def ascii_code(r):
    c = r.choice([chr(x) for x in list(range(65, 91)) + list(range(97, 123)) + list(range(48, 58))])
    o = ord(c)
    if r.random() < 0.5:
        wrong = uniq([str(o + 1), str(o - 1), str(o ^ 32) if c.isalpha() else str(o + 10), str(o + 2)], [str(o)])
        return mcq(f"What is the ASCII code (in decimal) of the character '{c}'?", str(o), wrong[:3],
                   f"ASCII codes: 'A' = 65, 'a' = 97, '0' = 48; so '{c}' = {o}.", r)
    b = format(o, '07b')
    wrong = uniq([format(o + 1, '07b'), format(o - 1, '07b'), b[::-1], format(o ^ 32, '07b') if c.isalpha() else format(o + 8, '07b')], [b])
    return mcq(f"What is the 7-bit binary ASCII code of the character '{c}'?", b, wrong[:3], f"'{c}' has ASCII code {o} = {b} in binary.", r)


def ascii_decode(r):
    w = r.choice([x for x in WORDS if x.isalpha() and len(x) <= 7])
    codes = [ord(c) for c in w]
    t = r.randrange(2)
    if t == 0:
        return {'stem': f'The following decimal ASCII codes represent a word: {" ".join(map(str, codes))}. Decode the word.',
                'answer': w, 'key': f"1 mark: 65–90 are 'A'–'Z' and 97–122 are 'a'–'z'; the word is {w}.",
                'distractors': [w.upper() if w != w.upper() else w.lower(), w[::-1], w[1:] + w[0]], 'marks': 1}
    return {'stem': f'Write the decimal ASCII codes of the characters of the word "{w}".', 'answer': ' '.join(map(str, codes)),
            'key': "1 mark: 'A' = 65 and 'a' = 97; each following letter adds 1.", 'distractors': [' '.join(str(c + 1) for c in codes), ' '.join(str(c ^ 32) for c in codes)],
            'marks': 1}


HINDI = ['कमल', 'नगर', 'भवन', 'सरल', 'महल', 'जल', 'फल', 'घर', 'बस', 'कलम', 'नमन', 'चमन', 'वन', 'पद']


def utf_bytes(r):
    en = r.choice([x for x in WORDS if x.isalpha() and len(x) <= 8])
    hi = r.choice(HINDI)
    t = r.randrange(3)
    if t == 0:
        s = hi
        what = f'the Hindi word "{s}" (each letter is one Unicode character with no vowel sign)'
    elif t == 1:
        s = en + ' ' + hi
        what = f'the text "{s}" (the Hindi letters have no vowel signs; the space is one character)'
    else:
        s = en + '₹' + str(r.randint(10, 99))
        what = f'the text "{s}"'
    u8 = len(s.encode('utf-8'))
    u32 = len(s.encode('utf-32-le'))
    enc = r.choice(['UTF-8', 'UTF-32'])
    ans = u8 if enc == 'UTF-8' else u32
    wrong = uniq([str(len(s)), str(u8 if enc == 'UTF-32' else u32), str(len(s) * 2), str(ans + len(s))], [str(ans)])
    return mcq(f'How many bytes are needed to store {what} in {enc}?', str(ans), wrong[:3],
               f'UTF-8 uses 1 byte for English letters, digits and space and 3 bytes for Devanagari letters and ₹; UTF-32 uses 4 bytes for every character. '
               f'Here: {len(s)} characters → {u8} bytes in UTF-8, {u32} bytes in UTF-32.', r)


# ====================================================================== Boolean logic
GATES = {
    'AND': lambda a, b: a & b, 'OR': lambda a, b: a | b, 'NAND': lambda a, b: 1 - (a & b),
    'NOR': lambda a, b: 1 - (a | b), 'XOR': lambda a, b: a ^ b,
}


def _expr_pool(vars_):
    A, B = vars_[0], vars_[1]
    C = vars_[2] if len(vars_) > 2 else None
    pool = [
        (f'NOT ({A} AND {B})', lambda v: 1 - (v[A] & v[B])),
        (f'(NOT {A}) OR (NOT {B})', lambda v: (1 - v[A]) | (1 - v[B])),
        (f'NOT ({A} OR {B})', lambda v: 1 - (v[A] | v[B])),
        (f'(NOT {A}) AND (NOT {B})', lambda v: (1 - v[A]) & (1 - v[B])),
        (f'{A} XOR {B}', lambda v: v[A] ^ v[B]),
        (f'({A} AND NOT {B}) OR (NOT {A} AND {B})', lambda v: (v[A] & (1 - v[B])) | ((1 - v[A]) & v[B])),
        (f'{A} AND (NOT {B})', lambda v: v[A] & (1 - v[B])),
        (f'(NOT {A}) OR {B}', lambda v: (1 - v[A]) | v[B]),
        (f'{A} OR (NOT {B})', lambda v: v[A] | (1 - v[B])),
        (f'{A} AND {B}', lambda v: v[A] & v[B]),
        (f'{A} OR {B}', lambda v: v[A] | v[B]),
        (f'NOT ({A} XOR {B})', lambda v: 1 - (v[A] ^ v[B])),
    ]
    if C:
        pool += [
            (f'({A} AND {B}) OR {C}', lambda v: (v[A] & v[B]) | v[C]),
            (f'{A} AND ({B} OR {C})', lambda v: v[A] & (v[B] | v[C])),
            (f'({A} AND {B}) OR ({A} AND {C})', lambda v: (v[A] & v[B]) | (v[A] & v[C])),
            (f'NOT ({A} AND {B}) OR {C}', lambda v: (1 - (v[A] & v[B])) | v[C]),
            (f'({A} OR {B}) AND NOT {C}', lambda v: (v[A] | v[B]) & (1 - v[C])),
            (f'NOT ({A} OR {B} OR {C})', lambda v: 1 - (v[A] | v[B] | v[C])),
            (f'(NOT {A}) AND (NOT {B}) AND (NOT {C})', lambda v: (1 - v[A]) & (1 - v[B]) & (1 - v[C])),
            (f'{A} XOR {B} XOR {C}', lambda v: v[A] ^ v[B] ^ v[C]),
            (f'({A} OR {B}) AND ({A} OR {C})', lambda v: (v[A] | v[B]) & (v[A] | v[C])),
            (f'{A} OR ({B} AND {C})', lambda v: v[A] | (v[B] & v[C])),
        ]
    return pool


def _rows(vars_):
    return [dict(zip(vars_, bits)) for bits in itertools.product([0, 1], repeat=len(vars_))]


def _col(f, vars_):
    return tuple(f(v) for v in _rows(vars_))


def bool_eval(r):
    vars_ = r.choice([['A', 'B', 'C'], ['X', 'Y', 'Z'], ['P', 'Q', 'R']])
    e, f = r.choice(_expr_pool(vars_))
    vals = {v: r.randint(0, 1) for v in vars_}
    used = [v for v in vars_ if v in e]
    out = f(vals)
    given = ', '.join(f'{v} = {vals[v]}' for v in used)
    return mcq(f'What is the value of the Boolean expression {e} when {given}?', str(out), [str(1 - out), 'Cannot be determined', 'Both 0 and 1'],
               f'Substituting {given}: NOT is applied first, then AND, then OR; the result is {out}.', r)


def gate_identify(r):
    g = r.choice(list(GATES))
    col = [GATES[g](a, b) for a, b in itertools.product([0, 1], repeat=2)]
    rows = ', '.join(f'({a}, {b}) → {o}' for (a, b), o in zip(itertools.product([0, 1], repeat=2), col))
    return mcq(f'A two-input logic gate gives these outputs for the inputs (A, B): {rows}. Which gate is it?', f'{g} gate',
               [f'{x} gate' for x in r.sample([x for x in GATES if x != g], 3)],
               f'The output column {"".join(map(str, col))} for inputs 00, 01, 10, 11 is that of the {g} gate.', r)


def gate_out(r):
    g = r.choice(list(GATES))
    a, b = r.randint(0, 1), r.randint(0, 1)
    out = GATES[g](a, b)
    g2 = r.choice([x for x in GATES if x != g])
    c = r.randint(0, 1)
    out2 = GATES[g2](out, c)
    return {'stem': f'The output of a {g} gate with inputs A = {a} and B = {b} is fed, along with C = {c}, into a {g2} gate. What is the final output? Show the intermediate output.',
            'answer': f'{g}({a}, {b}) = {out}; {g2}({out}, {c}) = {out2}', 'key': f'1 mark for the intermediate output {out}, 1 mark for the final output {out2}.',
            'distractors': [str(1 - out2)], 'marks': 2}


def truth_table(r):
    vars_ = r.choice([['A', 'B'], ['A', 'B', 'C'], ['X', 'Y'], ['X', 'Y', 'Z']])
    pool = [p for p in _expr_pool(vars_) if all(v in p[0] for v in vars_)]
    e, f = r.choice(pool)
    rows = _rows(vars_)
    head = ' '.join(vars_) + ' | ' + e
    lines = [' '.join(str(v[x]) for x in vars_) + ' | ' + str(f(v)) for v in rows]
    marks = 2 if len(vars_) == 2 else 3
    return {'stem': f'Draw the truth table for the Boolean expression {e}.', 'answer': head + '\n' + '\n'.join(lines),
            'key': f'{marks} marks: all {len(rows)} input combinations ({1 if marks == 2 else 1} mark) and the correct output column {"".join(str(f(v)) for v in rows)} '
                   f'({marks - 1} mark{"s" if marks > 2 else ""}).', 'marks': marks}


def equivalent(r):
    vars_ = r.choice([['A', 'B'], ['A', 'B', 'C'], ['P', 'Q', 'R']])
    pool = _expr_pool(vars_)
    cols = {}
    for e, f in pool:
        cols.setdefault(_col(f, vars_), []).append(e)
    groups = [g for g in cols.values() if len(g) >= 2]
    g = r.choice(groups)
    a, b = r.sample(g, 2)
    others = [e for c, es in cols.items() for e in es if e not in g]
    if len(others) < 3:
        raise ValueError('few')
    return mcq(f'Which of the following Boolean expressions is equivalent to {a}?', b, r.sample(others, 3),
               f'{a} and {b} give the same output for every combination of inputs (check the truth table){"; this is De Morgan\'s law" if "NOT (" in a or "NOT (" in b else ""}.', r)


def demorgan_verify(r):
    v = r.choice([('A', 'B'), ('X', 'Y'), ('P', 'Q')])
    A, B = v
    law = r.randrange(2)
    if law == 0:
        l, rr = f'NOT ({A} AND {B})', f'(NOT {A}) OR (NOT {B})'
        f1 = lambda a, b: 1 - (a & b)
        f2 = lambda a, b: (1 - a) | (1 - b)
    else:
        l, rr = f'NOT ({A} OR {B})', f'(NOT {A}) AND (NOT {B})'
        f1 = lambda a, b: 1 - (a | b)
        f2 = lambda a, b: (1 - a) & (1 - b)
    lines = [f'{a} {b} | {f1(a, b)} | {f2(a, b)}' for a, b in itertools.product([0, 1], repeat=2)]
    return {'stem': f"Verify De Morgan's law {l} = {rr} using a truth table.",
            'answer': f'{A} {B} | {l} | {rr}\n' + '\n'.join(lines) + '\nThe last two columns are identical, so the law is verified.',
            'key': '3 marks: 1 for the input combinations, 1 for each correct output column (the two columns must match).', 'marks': 3}


def logic_case(r):
    who = r.choice(NAMES)
    t = r.randrange(3)
    if t == 0:
        story = (f'{who} designs an alarm for a school lab. The alarm (Y) should ring when the door is open (D = 1) AND the lab is locked for the night (L = 1), '
                 'OR when smoke is detected (S = 1).')
        expr, f = '(D AND L) OR S', lambda d, l, s: (d & l) | s
        vs = ['D', 'L', 'S']
    elif t == 1:
        story = (f'{who} builds a voting machine for three judges P, Q and R. The light (Y) should glow only when judge P approves (P = 1) AND at least one of '
                 'Q and R approves.')
        expr, f = 'P AND (Q OR R)', lambda p, q, rr: p & (q | rr)
        vs = ['P', 'Q', 'R']
    else:
        story = (f'{who} wires a staircase light controlled by two switches A and B at the two ends. The light (Y) is on when exactly one of the switches is up (1), '
                 'and a master switch M must also be on.')
        expr, f = '(A XOR B) AND M', lambda a, b, m: (a ^ b) & m
        vs = ['A', 'B', 'M']
    rows = list(itertools.product([0, 1], repeat=3))
    ones = [rw for rw in rows if f(*rw)]
    test = r.choice(rows)
    return {'stem': (f'{story}\n(i) Write the Boolean expression for Y. (1)\n(ii) How many of the 8 input combinations make Y = 1? (1)\n'
                     f'(iii) What is Y when {", ".join(f"{v} = {x}" for v, x in zip(vs, test))}? Show the working. (2)'),
            'answer': f'(i) Y = {expr} (ii) {len(ones)} (iii) Y = {f(*test)}',
            'key': f'1 + 1 + 2 marks: (iii) substitute the values into {expr} to get {f(*test)}.', 'marks': 4}


# ====================================================================== algorithm tracing (pseudocode -> equivalent Python)
PSEUDO = [
    ('INPUT N\nSET SUM = 0\nSET I = 1\nWHILE I <= N DO\n    SUM = SUM + I * I\n    I = I + 1\nEND WHILE\nPRINT SUM',
     'N = {n}\nSUM = 0\nI = 1\nwhile I <= N:\n    SUM = SUM + I * I\n    I = I + 1\nprint(SUM)', 'N', (3, 9)),
    ('INPUT N\nSET F = 1\nFOR I = 1 TO N\n    F = F * I\nEND FOR\nPRINT F',
     'N = {n}\nF = 1\nfor I in range(1, N + 1):\n    F = F * I\nprint(F)', 'N', (3, 8)),
    ('INPUT N\nSET C = 0\nWHILE N > 0 DO\n    N = N // 10\n    C = C + 1\nEND WHILE\nPRINT C',
     'N = {n}\nC = 0\nwhile N > 0:\n    N = N // 10\n    C = C + 1\nprint(C)', 'N', (100, 9999999)),
    ('INPUT N\nSET R = 0\nWHILE N > 0 DO\n    D = N MOD 10\n    R = R * 10 + D\n    N = N // 10\nEND WHILE\nPRINT R',
     'N = {n}\nR = 0\nwhile N > 0:\n    D = N % 10\n    R = R * 10 + D\n    N = N // 10\nprint(R)', 'N', (102, 98765)),
    ('INPUT A, B\nWHILE B != 0 DO\n    T = B\n    B = A MOD B\n    A = T\nEND WHILE\nPRINT A',
     'A, B = {a}, {b}\nwhile B != 0:\n    T = B\n    B = A % B\n    A = T\nprint(A)', 'AB', (12, 99)),
    ('INPUT N\nSET A = 0\nSET B = 1\nFOR I = 1 TO N\n    PRINT A\n    C = A + B\n    A = B\n    B = C\nEND FOR',
     'N = {n}\nA = 0\nB = 1\nfor I in range(1, N + 1):\n    print(A, end=" ")\n    C = A + B\n    A = B\n    B = C', 'N', (5, 10)),
    ('INPUT N\nSET S = 0\nWHILE N > 0 DO\n    IF N MOD 2 = 0 THEN\n        S = S + N\n    END IF\n    N = N - 3\nEND WHILE\nPRINT S',
     'N = {n}\nS = 0\nwhile N > 0:\n    if N % 2 == 0:\n        S = S + N\n    N = N - 3\nprint(S)', 'N', (10, 30)),
    ('INPUT N\nSET COUNT = 0\nFOR I = 1 TO N\n    IF N MOD I = 0 THEN\n        COUNT = COUNT + 1\n    END IF\nEND FOR\nPRINT COUNT',
     'N = {n}\nCOUNT = 0\nfor I in range(1, N + 1):\n    if N % I == 0:\n        COUNT = COUNT + 1\nprint(COUNT)', 'N', (12, 60)),
]


def pseudo_trace(r, marks=2):
    p, py, kind, (lo, hi) = r.choice(PSEUDO)
    if kind == 'AB':
        g = r.randint(2, 9)
        a, b = g * r.randint(2, 11), g * r.randint(2, 11)
        if a == b:
            raise ValueError('same')
        code = py.format(a=a, b=b)
        given = f'A = {a} and B = {b}'
    else:
        n = r.randint(lo, hi)
        code = py.format(n=n)
        given = f'N = {n}'
    out = run(code)
    return {'stem': f'Dry run the following pseudocode for the input {given} and write the output.\n{p}',
            'answer': out, 'key': f'{marks} marks for the correct output {out} (trace the variables in each pass; 1 mark if the trace is right but the final value slips).',
            'marks': marks, 'distractors': uniq([run_or_err(code.replace('<=', '<')), run_or_err(code.replace('+ 1', '+ 2', 1))], [out])}


def pseudo_trace_mcq(r):
    v = pseudo_trace(r)
    w = [x for x in v.get('distractors', []) if x and not x.startswith('Error')]
    out = v['answer']
    if out.strip().lstrip('-').isdigit():
        w += [str(int(out) + 1), str(int(out) - 1), str(int(out) * 2)]
    w = fill(w, out)
    return mcq(v['stem'].replace(' and write the output.', '. What is the output?'), out, w[:3], v['key'].replace('2 marks for the', 'The'), r)


def compare_algos(r):
    t = r.randrange(3)
    if t == 0:
        n = r.choice([p for p in range(53, 400) if all(p % d for d in range(2, int(p ** .5) + 1))])
        a = n - 2
        b = int(n ** 0.5) - 1
        return {'stem': (f'To check whether {n} is prime, Algorithm 1 divides it by every number from 2 to {n - 1}, while Algorithm 2 divides it only by '
                         f'the numbers from 2 to the square root of {n} (rounded down). How many divisions does each algorithm make? Which is more efficient?'),
                'answer': f'Algorithm 1: {a} divisions; Algorithm 2: {b} divisions (2 to {int(n ** .5)}); Algorithm 2 is more efficient.',
                'key': f'1 mark for both counts ({a} and {b}), 1 mark for choosing Algorithm 2 with the reason (fewer steps for the same result).', 'marks': 2}
    if t == 1:
        L = r.sample(range(10, 99), r.randint(8, 12))
        k = r.randrange(len(L))
        x = L[k]
        return {'stem': f'A list has the elements {L}. How many comparisons does linear search make to find {x}, starting from the first element? '
                        f'How many would it make if the element were not present?',
                'answer': f'{k + 1} comparisons to find {x}; {len(L)} comparisons if it is absent.',
                'key': f'1 mark each: {x} is at position {k + 1}, so {k + 1} comparisons; an absent element is compared with all {len(L)} elements.', 'marks': 2}
    n = r.randint(20, 200)
    loop = n
    return {'stem': (f'Two algorithms find the sum of the first {n} natural numbers. Algorithm A adds the numbers one by one in a loop; '
                     f'Algorithm B uses the formula n(n + 1)/2. How many additions does Algorithm A make, what result do both give, and which is better?'),
            'answer': f'Algorithm A makes {loop} additions (starting from a sum of 0); both give {n * (n + 1) // 2}; Algorithm B is better as it takes a fixed number of steps.',
            'key': f'2 marks: 1 for {loop} additions and the sum {n * (n + 1) // 2}, 1 for choosing B with the reason.', 'marks': 2}


# ====================================================================== Python basics
NON_KW = ['print', 'input', 'main', 'Print', 'list', 'string', 'integer', 'value', 'loop', 'then', 'go', 'switch', 'case_', 'end',
          'Else', 'TRUE', 'num', 'int', 'str', 'float', 'range', 'len']
KWS = ['if', 'else', 'elif', 'while', 'for', 'break', 'continue', 'def', 'return', 'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is',
       'import', 'from', 'pass', 'global', 'lambda', 'try', 'except', 'finally', 'class', 'with', 'as', 'del', 'assert', 'raise', 'yield']
assert all(keyword.iskeyword(k) for k in KWS) and not any(keyword.iskeyword(k) for k in NON_KW)


def keyword_pick(r):
    if r.random() < 0.6:
        k = r.choice(KWS)
        return mcq('Which of the following is a keyword in Python?', k, r.sample(NON_KW, 3),
                   f'{k} is a reserved word (keyword); print, input, len and data-type names are built-in names, not keywords.', r)
    n = r.choice(NON_KW)
    return mcq('Which of the following is NOT a keyword in Python?', n, r.sample(KWS, 3), f'{n} is not in the list of Python keywords.', r)


ID_POOL = ['total_marks', '_count', 'Roll2', 'marks2024', 'StudentName', 'x', 'sum_of_n', 'NAME', 'a1b2', '_', 'avg_score', 'Value_1',
           '2ndValue', 'roll no', 'total-marks', '@name', 'for', 'class', 'marks%', 'my.var', '1abc', 'while', 'True', 'first name', 'rate#',
           'None', 'is', 'def', 'gross$pay', '9lives']


def ident_ok(s):
    return s.isidentifier() and not keyword.iskeyword(s)


def ident_valid(r):
    good = [s for s in ID_POOL if ident_ok(s)]
    bad = [s for s in ID_POOL if not ident_ok(s)]
    if r.random() < 0.5:
        g = r.choice(good)
        return mcq('Which of the following is a valid identifier in Python?', g, r.sample(bad, 3),
                   f'{g} begins with a letter or underscore, has only letters, digits and underscores, and is not a keyword.', r)
    b = r.choice(bad)
    why = ('it is a keyword' if keyword.iskeyword(b) else 'it begins with a digit' if b[0].isdigit() else 'it contains a character other than letters, digits and underscore')
    return mcq('Which of the following is NOT a valid identifier in Python?', b, r.sample(good, 3), f'{b} is invalid because {why}.', r)


def ident_classify(r):
    pick = r.sample(ID_POOL, 6)
    ok = [s for s in pick if ident_ok(s)]
    no = [s for s in pick if not ident_ok(s)]
    if not ok or not no:
        raise ValueError('one-sided')
    return {'stem': f'Identify the valid and invalid identifiers from the following, giving a reason for each invalid one: {", ".join(pick)}',
            'answer': f'Valid: {", ".join(ok)}. Invalid: ' + '; '.join(
                f'{b} ({"keyword" if keyword.iskeyword(b) else "starts with a digit" if b[0].isdigit() else "has a space or special character"})' for b in no),
            'key': '2 marks: ½ mark for each correct classification with reason (any four).', 'marks': 2}


TYPE_EXPRS = ['7 / 2', '7 // 2', '7.0 // 2', '3 + 4j', '"25"', '25 > 3', '[1, 2]', '(1, 2)', '(5)', '(5,)', '{1: "a"}', 'None', '2 ** 3', '2 ** -1',
              'int("12")', 'float(3)', 'str(4.5)', 'True + 1', '3 * 1.0', 'list("ab")', '"5" * 2', 'len("abc")', 'abs(-3.5)', '10 % 3']


def type_out(r):
    e = r.choice(TYPE_EXPRS)
    out = run(f'print(type({e}))')
    allt = ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>", "<class 'list'>", "<class 'tuple'>", "<class 'complex'>",
            "<class 'dict'>", "<class 'NoneType'>"]
    wrong = r.sample([t for t in allt if t != out], 3)
    return mcq(f'What is the output of the following statement?\nprint(type({e}))', out, wrong, f'{e} evaluates to {run_or_err("print(repr(" + e + "))")}, whose type is {out}.', r)


MUT = [('L = [10, 20, 30]\nL[1] = 25\nprint(L)', None), ('T = (10, 20, 30)\nT[1] = 25\nprint(T)', 'TypeError'),
       ('S = "{w}"\nS[0] = "Z"\nprint(S)', 'TypeError'), ('S = "{w}"\nS = "Z" + S[1:]\nprint(S)', None),
       ('D = {{"a": 1}}\nD["a"] = 5\nprint(D)', None), ('T = (1, 2)\nT = T + (3,)\nprint(T)', None),
       ('x = 5\nx = x + 1\nprint(x)', None), ('T = ([1, 2], 3)\nT[0].append(9)\nprint(T)', None),
       ('S = "{w}"\nprint(S.upper(), S)', None), ('L = [1, 2]\nL.append([3])\nprint(L, len(L))', None)]


def mutability(r):
    tpl, _ = r.choice(MUT)
    code = tpl.format(w=r.choice([w for w in WORDS if w.isalpha()]))
    out, e = exc(code)
    ans = f'Error: {e}' if e else out
    first = code.split('\n')[0]
    unchanged = run_or_err(first + '\nprint(' + first.split(' = ')[0] + ')')
    wrong = ['Error: TypeError', 'Error: AttributeError', 'Error: IndexError', unchanged]
    wrong = uniq([w for w in wrong if not w.startswith('Error (')], [ans])
    return mcq(f'What happens when the following code is run?\n{code}', ans, r.sample(wrong, 3),
               'Lists and dictionaries are mutable; strings, tuples and numbers are immutable, so item assignment on them raises TypeError. '
               f'Result: {ans}.', r)


def ops_out(r):
    a, b = r.randint(2, 30), r.randint(2, 9)
    L = r.sample(range(1, 20), 4)
    w = r.choice([x for x in WORDS if x.isalpha()])
    t = r.randrange(7)
    if t == 0:
        code = f'A = {L}\nB = A\nC = {L}\nprint(A is B, A is C, A == C)'
    elif t == 1:
        code = f'S = "{w}"\nprint("{w[1:3]}" in S, "{w[0].lower() if w[0].isupper() else w[0].upper()}" in S, "z" not in S)'
    elif t == 2:
        code = f'x = {a}\nx += {b}\nx *= 2\nx //= {b}\nx %= 7\nprint(x)'
    elif t == 3:
        code = f'print({a} > {b} and {b} > {a % 7}, not {a} == {b}, {a} != {b} or {a} < 0)'
    elif t == 4:
        code = f'print(0 and {a}, {b} or 0, not {a}, {a} and {b})'
    elif t == 5:
        code = f'print({a} // {b}, {a} % {b}, -{a} // {b}, {a} / {b * 2})'
    else:
        code = f'x = None\ny = {L}\nprint(x is None, y is not None, {L[0]} in y, {L[0] + 20} in y)'
    out = run(code)
    alts = [code.replace(' is C', ' is B'), code.replace('and', 'or', 1), code.replace('//=', '/='), code.replace(' not in ', ' in '),
            code.replace('-' + str(a), str(a)), code.replace(f'{L[0]} in y', f'{L[0]} not in y')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error')]
    if len(wrong) < 3:
        parts = out.split()
        for i in range(len(parts)):
            p = parts[:]
            p[i] = {'True': 'False', 'False': 'True'}.get(p[i], p[i] + '0' if p[i].lstrip('-').isdigit() else p[i])
            wrong.append(' '.join(p))
        wrong = uniq(wrong, [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3],
               f'Evaluate each operator (identity: is, membership: in, assignment operators, short-circuit and/or). Output: {out}', r)


def conv_out(r):
    a = r.randint(2, 30)
    f = round(r.uniform(1, 9), 1) + 0.0
    if float(f).is_integer():
        f += 0.4
    s = str(r.randint(10, 99))
    t = r.randrange(6)
    if t == 0:
        code = f'x = "{s}"\ny = {a}\nprint(x * 2, int(x) * 2, x + str(y))'
    elif t == 1:
        code = f'print(int({f}), float({a}), str({a}) + "{s}", int("{s}") + {a})'
    elif t == 2:
        code = f'print({a} + {f}, True + {a}, {a} / {a})'
    elif t == 3:
        code = f'print(bool(0), bool("{s}"), bool(""), int(True))'
    elif t == 4:
        code = f'x = {a}\ny = float(x)\nz = int(y * 3)\nprint(y, z, type(z).__name__)'
    else:
        code = f'print(int("{s}", 8) if "8" not in "{s}" and "9" not in "{s}" else int("{s}"), round({f}), str({f})[::-1])'
    out = run(code)
    alts = [code.replace('x * 2', 'int(x) * 2', 1), code.replace('int(', 'float(', 1), code.replace('True +', 'False +'), code.replace('bool(0)', 'bool(1)'),
            code.replace('* 3', '* 2'), code.replace('[::-1]', '')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error')]
    if len(wrong) < 3:
        wrong += [out.replace('.0', '', 1), out + '.0', out.replace(' ', ', ')]
        wrong = uniq(wrong, [out])
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3],
               f'Explicit conversion with int(), float(), str() and bool(); implicit conversion of int to float in mixed arithmetic. Output: {out}', r)


def input_out(r):
    v = r.choice(['x', 'n', 'num', 'a', 'val'])
    data = str(r.randint(2, 40))
    k = r.randint(2, 4)
    t = r.randrange(4)
    if t == 0:
        code = f'{v} = input("Enter a number: ")\nprint({v} * {k})'
        runc = f'{v} = "{data}"\nprint({v} * {k})'
    elif t == 1:
        code = f'{v} = int(input("Enter a number: "))\nprint({v} * {k}, {v} ** 2)'
        runc = f'{v} = int("{data}")\nprint({v} * {k}, {v} ** 2)'
    elif t == 2:
        code = f'{v} = float(input("Enter a number: "))\nprint({v} / {k}, {v} // {k})'
        runc = f'{v} = float("{data}")\nprint({v} / {k}, {v} // {k})'
    else:
        code = f'{v} = input("Enter a number: ")\nprint({v} + "{k}", int({v}) + {k})'
        runc = f'{v} = "{data}"\nprint({v} + "{k}", int({v}) + {k})'
    out = run(runc)
    alt = [runc.replace(f'"{data}"', data, 1) if 'int(' not in runc and 'float(' not in runc else runc.replace('int(', 'str(').replace('float(', 'str('),
           runc.replace(f'* {k}', f'+ {k}'), runc.replace('//', '/')]
    wrong = [x for x in uniq([run_or_err(c) for c in alt], [out]) if not x.startswith('Error')]
    wrong = fill(wrong + ['Error: TypeError'], out)
    return mcq(f'The user enters {data} when the following code runs. What is printed after the prompt?\n{code}', out, wrong[:3],
               f'input() always returns a string; int() or float() converts it. Output: {out}', r)


def print_out(r):
    a, b, c = r.sample(WORDS[:12], 3)
    n = r.randint(1, 9)
    sep = r.choice(['-', '*', '#', ', ', ''])
    end = r.choice(['!', ' ', '@', '...'])
    t = r.randrange(3)
    if t == 0:
        code = f'print("{a}", "{b}", sep="{sep}", end="{end}")\nprint("{c}")'
    elif t == 1:
        code = f'print("{a}", {n}, "{b}", sep="{sep}")'
    else:
        code = f'print("{a}", end="{end}")\nprint("{b}", "{c}", sep="{sep}")'
    out = run(code)
    alts = [code.replace(f'sep="{sep}"', 'sep=" "'), code.replace(f', end="{end}"', ''), code.replace(f'sep="{sep}"', f'sep="{sep}{sep}"')]
    wrong = [x for x in uniq([run_or_err(q) for q in alts], [out]) if not x.startswith('Error')]
    if len(wrong) < 3:
        wrong.append(out.replace(sep, ' ') if sep else out + ' ')
        wrong = uniq(wrong, [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'sep goes between values and end is printed after the last value (default newline). Output: {out}', r)


ERR_KIND = [
    ('print("Total" {a})', 'syntax'), ('if {a} > {b}\n    print("big")', 'syntax'), ('x = ({a} + {b}\nprint(x)', 'syntax'),
    ('for i in range({a}):\nprint(i)', 'syntax'), ('print({a} / 0)', 'runtime'), ('L = [{a}, {b}]\nprint(L[{c}])', 'runtime'),
    ('print(int("{w}"))', 'runtime'), ('print(value + {a})', 'runtime'), ('print("{w}" + {a})', 'runtime'),
    ('marks = {a}\nwhile marks > 0\n    marks = marks - 1', 'syntax'), ('D = {{"x": {a}}}\nprint(D["y"])', 'runtime'),
    ('import maths\nprint(maths.sqrt({a}))', 'runtime'), ('def f(n):\nreturn n * 2', 'syntax'), ('print(len({a}))', 'runtime'),
    ('# average of {a} and {b}\nprint({a} + {b} / 2)', 'logical'), ('# area of a rectangle {a} by {b}\nprint(2 * ({a} + {b}))', 'logical'),
    ('# percentage of {a} out of 50\nprint({a} / 50 * 10)', 'logical'), ('# check if {a} is even\nprint({a} % 2 == 1)', 'logical'),
    ('# sum of 1 to {b}\ns = 0\nfor i in range(1, {b}):\n    s = s + i\nprint(s)', 'logical'),
]


def error_kind(r):
    tpl, kind = r.choice(ERR_KIND)
    a, b, c = r.randint(11, 49), r.randint(2, 9), r.randint(3, 6)
    code = tpl.format(a=a, b=b, c=c, w=r.choice([x for x in WORDS if x.isalpha()]))
    if kind == 'syntax':
        assert not compiles(code)
        ans = 'Syntax error'
        why = 'the code breaks the rules of the language, so Python reports it before running it'
    elif kind == 'runtime':
        _, e = exc(code)
        assert e
        ans = f'Runtime error ({e})'
        why = f'the code is grammatically correct but raises {e} while running'
    else:
        assert compiles(code) and exc(code)[1] is None
        ans = 'Logical error'
        why = 'the program runs without any error message but gives a wrong result for the stated task'
    opts = ['Syntax error', 'Logical error', 'Runtime error (ZeroDivisionError)', 'Runtime error (ValueError)', 'Runtime error (NameError)',
            'Runtime error (IndexError)', 'Runtime error (TypeError)', 'No error']
    wrong = [o for o in opts if o != ans and not (ans.startswith('Runtime') and o.startswith('Runtime'))]
    if ans.startswith('Runtime'):
        wrong = r.sample([o for o in opts if o.startswith('Runtime') and o != ans], 1) + ['Syntax error', 'Logical error']
    else:
        wrong = r.sample(wrong, 3)
    return mcq(f'Which type of error does the following code have?\n{code}', ans, wrong[:3], f'{ans}: {why}.', r)


# ====================================================================== flow of control
def if_out(r):
    t = r.randrange(5)
    if t == 0:
        m = r.randint(20, 99)
        code = (f'marks = {m}\nif marks >= 90:\n    grade = "A"\nelif marks >= 75:\n    grade = "B"\nelif marks >= 60:\n    grade = "C"\n'
                f'elif marks >= 33:\n    grade = "D"\nelse:\n    grade = "E"\nprint(marks, grade)')
        alts = [code.replace('elif', 'if'), code.replace('>= 75', '> 75'), code.replace('>= 60', '>= 70')]
    elif t == 1:
        y = r.choice([1900, 2000, 2024, 2023, 2100, 1996, 2022, 2400, 1800, 2016])
        code = (f'y = {y}\nif y % 400 == 0:\n    print(y, "is a leap year")\nelif y % 100 == 0:\n    print(y, "is not a leap year")\n'
                f'elif y % 4 == 0:\n    print(y, "is a leap year")\nelse:\n    print(y, "is not a leap year")')
        alts = [code.replace('if y % 400 == 0:\n    print(y, "is a leap year")\nelif', 'if'), code.replace('y % 4 == 0', 'y % 4 != 0'), code.replace('% 100', '% 200')]
    elif t == 2:
        a, b, c = r.sample(range(1, 60), 3)
        code = f'a, b, c = {a}, {b}, {c}\nif a > b:\n    if a > c:\n        print(a)\n    else:\n        print(c)\nelif b > c:\n    print(b)\nelse:\n    print(c)'
        alts = [code.replace('a > b', 'a < b'), code.replace('b > c', 'b < c'), code.replace('print(a)', 'print(b)')]
    elif t == 3:
        x = r.randint(-30, 30)
        code = f'x = {x}\nif x > 0 and x % 2 == 0:\n    print("positive even")\nelif x > 0:\n    print("positive odd")\nelif x == 0:\n    print("zero")\nelse:\n    print("negative")'
        alts = [code.replace('and', 'or'), code.replace('x > 0:', 'x >= 0:'), code.replace('"zero"', '"negative"')]
    else:
        amt = r.choice([450, 999, 1000, 1500, 2499, 2500, 4000, 5000, 7200])
        code = (f'amount = {amt}\nif amount >= 5000:\n    disc = 20\nelif amount >= 2500:\n    disc = 10\nelif amount >= 1000:\n    disc = 5\nelse:\n    disc = 0\n'
                f'pay = amount - amount * disc // 100\nprint(disc, pay)')
        alts = [code.replace('>= 2500', '> 2500'), code.replace('>= 1000', '> 1000'), code.replace('// 100', '// 10')]
    out = run(code)
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error')]
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': out,
            'key': f'Only the first true condition of an if-elif ladder runs. Output: {out}', 'distractors': wrong, 'marks': 1}


def range_out(r):
    a = r.randint(-5, 10)
    b = a + r.randint(5, 25)
    c = r.choice([1, 2, 3, 4, 5])
    t = r.randrange(4)
    if t == 0:
        e = f'list(range({a}, {b}, {c}))'
        ans = run(f'print({e})')
        wrong = [run(f'print(list(range({a}, {b + 1}, {c})))'), run(f'print(list(range({a + 1}, {b}, {c})))'), run(f'print(list(range({a}, {b}, {c + 1})))')]
        stem = f'What is the output of print({e})?'
    elif t == 1:
        e = f'range({b}, {a}, -{c})'
        ans = str(len(range(b, a, -c)))
        wrong = [str(len(range(b, a - 1, -c))), str(len(range(b, a, -c)) - 1), str(abs(b - a))]
        stem = f'How many times will the loop for i in {e}: run?'
    elif t == 2:
        n = r.randint(3, 12)
        code = f'i = {a}\ncount = 0\nwhile i < {b}:\n    i = i + {c}\n    count = count + 1\nprint(count, i)'
        ans = run(code)
        wrong = [run(code.replace(f'i < {b}', f'i <= {b}')), run(code.replace('count = count + 1', 'count = count + 2')), run(code.replace('print(count, i)', 'print(count - 1, i)'))]
        stem = f'What is the output of the following code?\n{code}'
    else:
        e = f'sum(range({a}, {b}, {c}))'
        ans = run(f'print({e})')
        wrong = [run(f'print(sum(range({a}, {b + 1}, {c})))'), run(f'print(sum(range({a + 1}, {b}, {c})))'), run(f'print(sum(range({a}, {b})))')]
        stem = f'What is the output of print({e})?'
    wrong = fill(wrong, ans)
    return mcq(stem, ans, wrong[:3], f'range(start, stop, step) stops before stop. Answer: {ans}', r)


def break_continue(r):
    t = r.randrange(5)
    a, b = r.randint(1, 4), r.randint(10, 20)
    k = r.randint(3, 7)
    if t == 0:
        code = f'for i in range({a}, {b}):\n    if i % {k} == 0:\n        break\n    print(i, end=" ")'
    elif t == 1:
        code = f'for i in range({a}, {b}):\n    if i % {k} == 0:\n        continue\n    print(i, end=" ")'
    elif t == 2:
        w = r.choice([x for x in WORDS if x.isalpha()])
        ch = r.choice(w[1:])
        code = f'for ch in "{w}":\n    if ch == "{ch}":\n        break\n    print(ch, end="")\nprint("#")'
    elif t == 3:
        n = r.randint(3, 9)
        code = f'n = {n * k + r.randint(1, 5)}\ns = 0\nwhile n > 0:\n    n = n - 1\n    if n % {k} == 0:\n        continue\n    s = s + n\nprint(s)'
    else:
        L = r.sample(range(-9, 40), 7)
        code = f'L = {L}\ntotal = 0\nfor x in L:\n    if x < 0:\n        break\n    if x % 2 == 1:\n        continue\n    total += x\nprint(total)'
    out = run(code)
    alts = [code.replace('break', 'continue'), code.replace('continue', 'break'), code.replace('== 0', '!= 0', 1), code.replace(f'range({a},', f'range({a + 1},')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error') and x.strip()]
    if not out.strip() or len(wrong) < 2:
        raise ValueError('weak')
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': out,
            'key': f'2 marks for the exact output (break leaves the loop, continue skips to the next iteration): {out}', 'distractors': wrong, 'marks': 2}


def bc_mcq(r):
    v = break_continue(r)
    w = fill(v['distractors'], v['answer'])
    return mcq(v['stem'].replace('Write the output', 'What is the output'), v['answer'], w[:3], v['key'].replace('2 marks for the exact output ', 'Output '), r)


PATTERNS = [
    ('for i in range(1, {n} + 1):\n    print("{s}" * i)', 'right-angled triangle of {s}'),
    ('for i in range({n}, 0, -1):\n    print("{s}" * i)', 'inverted triangle of {s}'),
    ('for i in range(1, {n} + 1):\n    for j in range(1, i + 1):\n        print(j, end=" ")\n    print()', 'number triangle'),
    ('for i in range(1, {n} + 1):\n    for j in range(i):\n        print(i, end=" ")\n    print()', 'repeated-number triangle'),
    ('for i in range(1, {n} + 1):\n    for j in range(i):\n        print(chr(65 + j), end="")\n    print()', 'letter triangle'),
    ('for i in range(1, {n} + 1):\n    print(" " * ({n} - i) + "{s}" * i)', 'right-aligned triangle'),
    ('for i in range({n}, 0, -1):\n    for j in range(1, i + 1):\n        print(j, end="")\n    print()', 'inverted number triangle'),
    ('k = 1\nfor i in range(1, {n} + 1):\n    for j in range(i):\n        print(k, end=" ")\n        k = k + 1\n    print()', "Floyd's triangle"),
]


def nested_out(r):
    tpl, _ = r.choice(PATTERNS)
    n = r.randint(3, 5)
    s = r.choice(['*', '#', '@'])
    code = tpl.format(n=n, s=s)
    out = run(code)
    alts = [code.replace(f'{n} + 1', f'{n}'), code.replace('range(i)', 'range(i + 1)'), code.replace('i + 1)', 'i)'), code.replace(f'range({n}, 0, -1)', f'range({n}, 1, -1)')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error') and x.strip()]
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': out, 'key': f'2 marks for the exact pattern:\n{out}',
            'distractors': wrong, 'marks': 2}


def pattern_write(r, marks=3):
    tpl, name = r.choice(PATTERNS)
    n = r.randint(4, 6)
    s = r.choice(['*', '#', '@'])
    code = tpl.format(n=n, s=s)
    out = run(code)
    return {'stem': f'Write a program using nested loops (or a loop) to display the following pattern:\n{out}', 'answer': code,
            'key': f'{marks} marks: outer loop for the {n} rows 1, inner loop or repetition for each row 1, correct printing and line breaks {marks - 2}. '
                   f'The model program prints exactly the pattern shown.', 'marks': marks}


PROGS = [
    ('Write a program to input a number and display its factorial.', 'n = int(input("Enter a number: "))\nf = 1\nfor i in range(1, n + 1):\n    f = f * i\nprint("Factorial =", f)', '5', 'Factorial = 120'),
    ('Write a program to input a number and check whether it is prime.', 'n = int(input("Enter a number: "))\nprime = n > 1\nfor i in range(2, n):\n    if n % i == 0:\n        prime = False\n        break\nif prime:\n    print(n, "is prime")\nelse:\n    print(n, "is not prime")', '29', '29 is prime'),
    ('Write a program to display the multiplication table of a number entered by the user (up to 10).', 'n = int(input("Enter a number: "))\nfor i in range(1, 11):\n    print(n, "x", i, "=", n * i)', '7', None),
    ('Write a program to display the first n terms of the Fibonacci series.', 'n = int(input("How many terms? "))\na, b = 0, 1\nfor i in range(n):\n    print(a, end=" ")\n    a, b = b, a + b', '7', '0 1 1 2 3 5 8'),
    ('Write a program to input a number and display the sum of its digits.', 'n = int(input("Enter a number: "))\ns = 0\nwhile n > 0:\n    s = s + n % 10\n    n = n // 10\nprint("Sum of digits =", s)', '4096', 'Sum of digits = 19'),
    ('Write a program to input a number and display it with its digits reversed.', 'n = int(input("Enter a number: "))\nrev = 0\nwhile n > 0:\n    rev = rev * 10 + n % 10\n    n = n // 10\nprint("Reversed:", rev)', '1234', 'Reversed: 4321'),
    ('Write a program to find the sum of the series 1 + 1/2 + 1/3 + ... + 1/n.', 'n = int(input("Enter n: "))\ns = 0\nfor i in range(1, n + 1):\n    s = s + 1 / i\nprint("Sum =", round(s, 3))', '4', 'Sum = 2.083'),
    ('Write a program to input three numbers and display the largest.', 'a = int(input("First: "))\nb = int(input("Second: "))\nc = int(input("Third: "))\nif a >= b and a >= c:\n    print(a, "is the largest")\nelif b >= c:\n    print(b, "is the largest")\nelse:\n    print(c, "is the largest")', '4\n19\n7', '19 is the largest'),
    ('Write a program to input a number and check whether it is an Armstrong number of three digits (for example, 153 = 1³ + 5³ + 3³).', 'n = int(input("Enter a 3-digit number: "))\ns = 0\nt = n\nwhile t > 0:\n    d = t % 10\n    s = s + d ** 3\n    t = t // 10\nif s == n:\n    print(n, "is an Armstrong number")\nelse:\n    print(n, "is not an Armstrong number")', '371', '371 is an Armstrong number'),
    ('Write a program to input marks out of 100 and display the grade: A (90 and above), B (75–89), C (50–74) and D (below 50).', 'm = int(input("Marks: "))\nif m >= 90:\n    print("A")\nelif m >= 75:\n    print("B")\nelif m >= 50:\n    print("C")\nelse:\n    print("D")', '82', 'B'),
    ('Write a program to display all even numbers between 1 and n, and their sum.', 'n = int(input("Enter n: "))\ns = 0\nfor i in range(2, n + 1, 2):\n    print(i, end=" ")\n    s = s + i\nprint()\nprint("Sum =", s)', '10', '2 4 6 8 10\nSum = 30'),
    ('Write a program to find the GCD (HCF) of two numbers entered by the user.', 'a = int(input("First: "))\nb = int(input("Second: "))\nwhile b != 0:\n    a, b = b, a % b\nprint("GCD =", a)', '36\n60', 'GCD = 12'),
]


def run_with_input(code, data):
    feed = data.split('\n')
    pre = 'import builtins\n_feed = ' + repr(feed) + '\ndef input(p=""):\n    return _feed.pop(0)\n'
    return run(pre + code)


def prog_write(r, marks=3, pool=None):
    stem, code, data, expect = r.choice(pool or PROGS)
    out = run_with_input(code, data)
    if expect is not None:
        assert '\n'.join(x.rstrip() for x in out.split('\n')) == expect, (out, expect)
    run_note = (f'# Sample run: input {data.replace(chr(10), ", ")} → output: ' if data else '# Output: ') + out.replace(chr(10), ' / ')
    return {'stem': stem, 'answer': code + '\n' + run_note,
            'key': f'{marks} marks: input and conversion 1, correct loop/condition logic {marks - 2}, correct output statement 1.', 'marks': marks}


def prog_pair(r, pool=None):
    a, b = r.sample(pool or PROGS, 2)
    x = prog_write(r, 2, [a])
    y = prog_write(r, 3, [b])
    return {'stem': f'(a) {x["stem"]} (2)\n(b) {y["stem"]} (3)', 'answer': f'(a)\n{x["answer"]}\n(b)\n{y["answer"]}',
            'key': '5 marks: (a) input 1, logic and output 1; (b) input 1, loop/condition 1, output 1.', 'marks': 5}


# ====================================================================== strings
def str_ops(r):
    s = r.choice([w for w in WORDS if w.isalpha()])
    t = r.choice([w for w in WORDS if w.isalpha() and w != s])
    n = r.randint(2, 3)
    i = r.randint(1, len(s) - 2)
    k = r.randrange(5)
    if k == 0:
        code = f's = "{s}"\nprint(s[{i}] + s[-{i}], len(s))'
    elif k == 1:
        code = f's = "{s}"\nt = "{t}"\nprint(s[:{i}] + t[{i}:])'
    elif k == 2:
        code = f's = "{s}"\nprint(s[{i}] * {n} + s[-1])'
    elif k == 3:
        code = f's = "{s}"\nprint("{s[i:i + 2]}" in s, "{s[i:i + 2].swapcase()}" in s, s[{i}:] not in s)'
    else:
        code = f's = "{s}"\nprint(s[-{i}:] + s[:-{i}])'
    out = run(code)
    alts = [code.replace(f'[{i}]', f'[{i + 1}]'), code.replace(f'-{i}', f'-{i + 1}'), code.replace(f'{i}:', f'{i - 1}:'), code.replace(f'* {n}', f'* {n + 1}')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error')]
    if len(wrong) < 3:
        wrong = uniq(wrong + [out[::-1], out.upper(), out.lower()], [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'Indexing starts at 0 (−1 is the last character); + joins and * repeats strings. Output: {out}', r)


def str_traverse(r):
    s = r.choice(SENTS + [w for w in WORDS if len(w) > 5])
    t = r.randrange(6)
    if t == 0:
        code = f's = "{s}"\nv = c = 0\nfor ch in s:\n    if ch.lower() in "aeiou":\n        v += 1\n    elif ch.isalpha():\n        c += 1\nprint(v, c)'
    elif t == 1:
        code = f's = "{s}"\nr = ""\nfor ch in s:\n    if ch.isupper():\n        r = r + ch.lower()\n    elif ch.islower():\n        r = r + ch.upper()\n    else:\n        r = r + "_"\nprint(r)'
    elif t == 2:
        code = f's = "{s}"\nr = ""\nfor i in range(len(s)):\n    if i % 2 == 0:\n        r = r + s[i]\nprint(r)'
    elif t == 3:
        code = f's = "{s}"\nr = ""\nfor ch in s:\n    r = ch + r\nprint(r)'
    elif t == 4:
        code = f's = "{s}"\ncount = 0\nfor w in s.split():\n    if len(w) > 3:\n        count += 1\nprint(count, len(s.split()))'
    else:
        code = f's = "{s}"\nr = ""\nfor ch in s:\n    if ch not in "aeiouAEIOU ":\n        r = r + ch\nprint(r)'
    out = run(code)
    alts = [code.replace('elif', 'if'), code.replace('i % 2 == 0', 'i % 2 == 1'), code.replace('r = ch + r', 'r = r + ch'), code.replace('> 3', '>= 3'),
            code.replace('"aeiouAEIOU "', '"aeiouAEIOU"'), code.replace('r + "_"', 'r + ch')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error')]
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': out, 'key': f'2 marks for the exact output: {out}', 'distractors': wrong, 'marks': 2}


METHODS = ['upper()', 'lower()', 'title()', 'capitalize()', 'swapcase()', 'isalpha()', 'isdigit()', 'isalnum()', 'islower()', 'isupper()', 'istitle()',
           'startswith("{p}")', 'endswith("{q}")', 'find("{c}")', 'index("{c}")', 'count("{c}")', 'replace("{c}", "*")', 'split("{c}")',
           'partition("{c}")', 'strip("{e}")', 'lstrip("{e}")', 'rstrip("{e}")', 'isspace()', 'split()']


def str_method(r):
    s = r.choice(SENTS + WORDS)
    m = r.choice(METHODS)
    letters = [c for c in s if c.isalpha()]
    c = r.choice(letters).lower() if any(x.islower() for x in letters) else r.choice(letters)
    if c not in s:
        c = r.choice(letters)
    mm = m.format(p=s[:2], q=s[-2:], c=c, e=s[0])
    code = f's = "{s}"\nprint(s.{mm})'
    out = run(code)
    others = r.sample([x for x in METHODS if x != m], 6)
    wrong = []
    for o in others:
        w = run_or_err(f's = "{s}"\nprint(s.{o.format(p=s[:2], q=s[-2:], c=c, e=s[0])})')
        if not w.startswith('Error'):
            wrong.append(w)
    wrong = uniq(wrong, [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f's.{mm} returns {out}.', r)


STR_PROGS = [
    ('Write a program to input a string and check whether it is a palindrome.', 's = input("Enter a string: ")\nif s == s[::-1]:\n    print(s, "is a palindrome")\nelse:\n    print(s, "is not a palindrome")', 'madam', 'madam is a palindrome'),
    ('Write a program to input a string and count the number of vowels in it.', 's = input("Enter a string: ")\ncount = 0\nfor ch in s:\n    if ch in "aeiouAEIOU":\n        count += 1\nprint("Vowels:", count)', 'Education', 'Vowels: 5'),
    ('Write a program to input a string and display it in reverse order without using slicing.', 's = input("Enter a string: ")\nr = ""\nfor ch in s:\n    r = ch + r\nprint(r)', 'Python', 'nohtyP'),
    ('Write a program to count the number of uppercase letters, lowercase letters and digits in a string.', 's = input("Enter a string: ")\nu = l = d = 0\nfor ch in s:\n    if ch.isupper():\n        u += 1\n    elif ch.islower():\n        l += 1\n    elif ch.isdigit():\n        d += 1\nprint(u, l, d)', 'CBSE Exam 2025', '5 3 4'),
    ('Write a program to input a sentence and display the number of words in it.', 's = input("Enter a sentence: ")\nprint("Words:", len(s.split()))', 'India is my country', 'Words: 4'),
    ('Write a program to input a sentence and display the longest word.', 's = input("Enter a sentence: ")\nlongest = ""\nfor w in s.split():\n    if len(w) > len(longest):\n        longest = w\nprint(longest)', 'Practice makes perfect', 'Practice'),
    ('Write a program to input a string and replace every space in it with a hyphen, without using replace().', 's = input("Enter a string: ")\nr = ""\nfor ch in s:\n    if ch == " ":\n        r = r + "-"\n    else:\n        r = r + ch\nprint(r)', 'Save water save life', 'Save-water-save-life'),
    ('Write a program to input a string and a character and count how many times the character occurs in the string (without using count()).', 's = input("Enter a string: ")\nc = input("Enter a character: ")\nn = 0\nfor ch in s:\n    if ch == c:\n        n += 1\nprint(n)', 'banana\na', '3'),
    ('Write a program to input a sentence and display each word with its first letter capitalised, without using title().', 's = input("Enter a sentence: ")\nr = ""\nfor w in s.split():\n    r = r + w[0].upper() + w[1:] + " "\nprint(r.strip())', 'unity in diversity', 'Unity In Diversity'),
]


# ====================================================================== lists
def list_index(r):
    L = r.sample(range(1, 90), r.randint(6, 8))
    v = r.choice(['L', 'A', 'nums', 'marks', 'data'])
    i, j = sorted(r.sample(range(1, len(L) - 1), 2))
    t = r.randrange(5)
    if t == 0:
        e = f'{v}[{i}] + {v}[-{j}]'
    elif t == 1:
        e = f'{v}[{i}:{j + 1}]'
    elif t == 2:
        e = f'{v}[::-2]'
    elif t == 3:
        e = f'{v}[-{j}:] + {v}[:{i}]'
    else:
        e = f'{v}[{i}:] * 2 if len({v}[{i}:]) < 4 else {v}[{i}:{i + 2}] * 2'
    code = f'{v} = {L}\nprint({e})'
    out = run(code)
    alts = [code.replace(f'[{i}]', f'[{i + 1}]'), code.replace(f'-{j}', f'-{j + 1}'), code.replace('::-2', '::2'), code.replace(f'{j + 1}]', f'{j}]'), code.replace('* 2', '+ [2]')]
    wrong = [x for x in uniq([run_or_err(c) for c in alts], [out]) if not x.startswith('Error')]
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'List indexing and slicing work like strings; slicing returns a new list. Output: {out}', r)


def list_method(r):
    L = r.sample(range(1, 50), 5)
    L.insert(r.randint(1, 4), L[0])
    v = r.choice(['L', 'A', 'nums', 'items'])
    x = r.randint(51, 80)
    t = r.randrange(7)
    if t == 0:
        code = f'{v} = {L}\ny = {v}.pop({r.randint(1, 3)})\nprint(y, {v})'
    elif t == 1:
        code = f'{v} = {L}\nprint({v}.count({L[0]}), {v}.index({L[0]}), {v}.index({L[3]}))'
    elif t == 2:
        code = f'{v} = {L}\n{v}.remove({L[0]})\n{v}.insert(2, {x})\nprint({v})'
    elif t == 3:
        code = f'{v} = {L}\nB = sorted({v})\n{v}.sort(reverse=True)\nprint(B[0], {v}[0], {v}[-1])'
    elif t == 4:
        code = f'{v} = {L}\n{v}.append([{x}, {x + 1}])\nprint(len({v}), {v}[-1][0])'
    elif t == 5:
        code = f'{v} = {L}\n{v}.extend([{x}, {x + 1}])\nprint(len({v}), {v}[-1])'
    else:
        code = f'{v} = {L}\nprint(max({v}) - min({v}), sum({v}), len({v}))'
    out = run(code)
    alts = [code.replace('pop(', 'pop(1 + '), code.replace(f'index({L[0]})', f'count({L[3]})'), code.replace('remove', 'pop') if t == 2 else code.replace('insert(2', 'insert(1'),
            code.replace('reverse=True', 'reverse=False'), code.replace('append', 'extend'), code.replace('extend', 'append'), code.replace('sum(', 'len(')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'Trace each list method in order. Output: {out}', r)


def nested_list(r):
    rows = [r.sample(range(1, 50), 3) for _ in range(3)]
    v = r.choice(['M', 'T', 'grid', 'L'])
    i, j = r.randint(0, 2), r.randint(0, 2)
    t = r.randrange(5)
    if t == 0:
        code = f'{v} = {rows}\nprint({v}[{i}][{j}], {v}[-1][0], len({v}))'
    elif t == 1:
        code = f'{v} = {rows}\ns = 0\nfor row in {v}:\n    s = s + row[{j}]\nprint(s)'
    elif t == 2:
        code = f'{v} = {rows}\nfor row in {v}:\n    print(max(row), end=" ")'
    elif t == 3:
        code = f'{v} = {rows}\n{v}[{i}].append(0)\nprint(len({v}), len({v}[{i}]), {v}[{i}])'
    else:
        code = f'{v} = {rows}\nprint([row[{j}] for row in {v}] if False else {v}[{i}][::-1])'
    out = run(code)
    alts = [code.replace(f'[{i}][{j}]', f'[{j}][{i}]'), code.replace(f'row[{j}]', f'row[{(j + 1) % 3}]'), code.replace('max(row)', 'min(row)'),
            code.replace(f'len({v}), ', ''), code.replace('[::-1]', '')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'{v}[i][j] is element j of row i. Output: {out}', r)


def copy_out(r):
    L = r.sample(range(1, 40), 4)
    x = r.randint(41, 99)
    t = r.randrange(4)
    if t == 0:
        code = f'A = {L}\nB = A\nC = list(A)\nA[0] = {x}\nprint(B[0], C[0])'
    elif t == 1:
        code = f'A = {L}\nB = A.copy()\nB.append({x})\nprint(len(A), len(B))'
    elif t == 2:
        code = f'A = {L}\nB = A[:]\nA.sort()\nprint(A == B, A is B)'
    else:
        code = f'A = {L}\nB = A\nB += [{x}]\nC = A + [{x}]\nprint(len(A), len(C), A is B)'
    out = run(code)
    alts = [code.replace('B = A\n', 'B = A[:]\n'), code.replace('.copy()', ''), code.replace('A[:]', 'A'), code.replace('list(A)', 'A')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    if len(wrong) < 3:
        wrong = uniq(wrong + [' '.join(reversed(out.split()))], [out])
    if len(wrong) < 3:
        parts = out.split()
        p = [{'True': 'False', 'False': 'True'}.get(x, str(int(x) + 1) if x.isdigit() else x) for x in parts]
        wrong = uniq(wrong + [' '.join(p)], [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3],
               f'B = A makes another name for the same list; list(A), A[:] and A.copy() make a new list. Output: {out}', r)


LIST_PROGS = [
    ('Write a program to input a list of numbers and display the largest and smallest numbers without using max() and min().', 'L = eval(input("Enter a list: "))\nbig = small = L[0]\nfor x in L:\n    if x > big:\n        big = x\n    if x < small:\n        small = x\nprint("Largest:", big, "Smallest:", small)', '[12, 45, 7, 30]', 'Largest: 45 Smallest: 7'),
    ('Write a program to find the mean of the numbers in a list.', 'L = eval(input("Enter a list: "))\ntotal = 0\nfor x in L:\n    total = total + x\nprint("Mean =", total / len(L))', '[10, 20, 30, 40]', 'Mean = 25.0'),
    ('Write a program to search for an element in a list using linear search and display its position.', 'L = eval(input("Enter a list: "))\nx = int(input("Element to search: "))\nfor i in range(len(L)):\n    if L[i] == x:\n        print(x, "found at position", i + 1)\n        break\nelse:\n    print(x, "not found")', '[4, 9, 16, 25]\n16', '16 found at position 3'),
    ('Write a program to count the frequency of a given element in a list (without using count()).', 'L = eval(input("Enter a list: "))\nx = int(input("Element: "))\nc = 0\nfor y in L:\n    if y == x:\n        c = c + 1\nprint(x, "occurs", c, "times")', '[2, 5, 2, 8, 2]\n2', '2 occurs 3 times'),
    ('Write a program to input a list and create a new list containing only the even numbers of the list.', 'L = eval(input("Enter a list: "))\nE = []\nfor x in L:\n    if x % 2 == 0:\n        E.append(x)\nprint(E)', '[3, 8, 11, 14, 20]', '[8, 14, 20]'),
    ('Write a program to swap the elements at even and odd positions of a list of even length (0 with 1, 2 with 3, and so on).', 'L = eval(input("Enter a list: "))\nfor i in range(0, len(L) - 1, 2):\n    L[i], L[i + 1] = L[i + 1], L[i]\nprint(L)', '[1, 2, 3, 4, 5, 6]', '[2, 1, 4, 3, 6, 5]'),
    ('Write a program to input a list of marks and count how many students scored above the average.', 'L = eval(input("Enter marks: "))\navg = sum(L) / len(L)\nc = 0\nfor m in L:\n    if m > avg:\n        c = c + 1\nprint("Above average:", c)', '[40, 75, 90, 55, 60]', 'Above average: 2'),
    ('Write a program to remove all duplicate elements from a list, keeping the first occurrence of each.', 'L = eval(input("Enter a list: "))\nU = []\nfor x in L:\n    if x not in U:\n        U.append(x)\nprint(U)', '[3, 5, 3, 7, 5, 9]', '[3, 5, 7, 9]'),
]


def list_prog_out(r):
    L = r.sample(range(1, 60), 6)
    t = r.randrange(4)
    if t == 0:
        x = r.choice(L + [r.randint(61, 90)])
        code = f'L = {L}\nx = {x}\npos = -1\nfor i in range(len(L)):\n    if L[i] == x:\n        pos = i\n        break\nprint(pos)'
    elif t == 1:
        code = f'L = {L}\nbig = L[0]\nfor x in L:\n    if x > big:\n        big = x\nprint(big, L.index(big))'
    elif t == 2:
        code = f'L = {L}\nfor i in range(len(L)):\n    if L[i] % 3 == 0:\n        L[i] = 0\nprint(L)'
    else:
        code = f'L = {L}\ns = 0\nfor x in L:\n    s = s + x\nprint(s, s / len(L))'
    out = run(code)
    alts = [code.replace('> big', '< big'), code.replace('% 3 == 0', '% 3 != 0'), code.replace('pos = i\n        break', 'pos = i'), code.replace('s / len(L)', 's // len(L)')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': out, 'key': f'2 marks for the correct output: {out}', 'distractors': wrong, 'marks': 2}


# ====================================================================== tuples and dictionaries
def tuple_out(r):
    T = tuple(r.sample(range(1, 60), r.randint(4, 6)))
    v = r.choice(['T', 'tup', 'A', 'marks'])
    x = r.randint(61, 90)
    t = r.randrange(8)
    if t == 0:
        code = f'{v} = {T}\nprint({v}[1:3] + ({x},), len({v}))'
    elif t == 1:
        code = f'{v} = {T}\nprint({v}[::-1][:2] * 2)'
    elif t == 2:
        code = f'{v} = {T + (T[0],)}\nprint({v}.count({T[0]}), {v}.index({T[2]}))'
    elif t == 3:
        code = f'a, b, c = {T[:3]}\na, c = c, a\nprint(a, b, c)'
    elif t == 4:
        code = f'{v} = ({T[0]}, ({T[1]}, {T[2]}), [{T[3]}, {x}])\nprint({v}[1][0], {v}[2][1], len({v}))'
    elif t == 5:
        code = f'{v} = {T}\nprint(max({v}), min({v}), sum({v}))'
    elif t == 6:
        code = f'x = ({x})\ny = ({x},)\nprint(type(x).__name__, type(y).__name__, len(y))'
    else:
        w = r.choice([s for s in WORDS if s.isalpha() and len(s) <= 7])
        code = f'{v} = tuple("{w}")\nprint({v}[{r.randint(0, 2)}], len({v}), "{w[1]}" in {v})'
    out = run(code)
    alts = [code.replace('1:3', '1:4'), code.replace('[:2]', '[:3]'), code.replace(f'.index({T[2]})', f'.index({T[1]})'), code.replace('a, c = c, a', 'a, b = b, a'),
            code.replace('[1][0]', '[1][1]'), code.replace('sum(', 'len('), code.replace(f'y = ({x},)', f'y = ({x})').replace(', len(y)', ''), code.replace(' in ', ' not in ')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    if len(wrong) < 3:
        wrong = uniq(wrong + ['Error: TypeError'], [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'Tuples support indexing, slicing, +, *, count() and index(); a one-element tuple needs a comma. Output: {out}', r)


def tuple_exc(r):
    T = tuple(r.sample(range(1, 40), 4))
    x = r.randint(41, 90)
    t = r.randrange(5)
    snippets = [f'T = {T}\nT[0] = {x}\nprint(T)', f'T = {T}\nT.append({x})\nprint(T)', f'T = {T}\nT = T + ({x},)\nprint(T)',
                f'T = {T}\nprint(T[{len(T)}])', f'T = {T}\ndel T[1]\nprint(T)']
    code = snippets[t]
    out, e = exc(code)
    ans = f'Error: {e}' if e else out
    pool = ['Error: TypeError', 'Error: AttributeError', 'Error: IndexError', str(T), str(T + (x,)), str((x,) + T[1:])]
    wrong = uniq([p for p in pool if p != ans], [ans])
    return mcq(f'What happens when the following code is run?\n{code}', ans, r.sample(wrong, 3),
               f'Tuples are immutable: item assignment, del of an item and methods like append() are not allowed, but a new tuple can be made with +. Result: {ans}', r)


def dict_method(r):
    ks = r.sample(NAMES, 4)
    vals = r.sample(range(40, 100), 4)
    D = dict(zip(ks[:3], vals[:3]))
    v = r.choice(['D', 'marks', 'stock', 'result'])
    t = r.randrange(7)
    if t == 0:
        code = f'{v} = {D}\nprint(list({v}.keys())[1], list({v}.values())[-1], len({v}))'
    elif t == 1:
        code = f'{v} = {D}\nprint({v}.get("{ks[3]}"), {v}.get("{ks[3]}", -1), "{ks[0]}" in {v})'
    elif t == 2:
        code = f'{v} = {D}\n{v}.update({{"{ks[0]}": {vals[3]}, "{ks[3]}": {vals[0]}}})\nprint({v})'
    elif t == 3:
        code = f'{v} = {D}\ndel {v}["{ks[1]}"]\n{v}["{ks[3]}"] = {vals[3]}\nprint({v})'
    elif t == 4:
        code = f'{v} = {D}\nfor k, val in {v}.items():\n    print(k[0], val % 10, end="; ")'
    elif t == 5:
        code = f'{v} = {D}\nx = {v}.pop("{ks[2]}")\nprint(x, len({v}), {v}.get("{ks[2]}", "absent"))'
    else:
        code = f'{v} = {D}\n{v}.clear()\nprint({v}, len({v}))'
    out = run(code)
    alts = [code.replace('[1]', '[0]'), code.replace(', -1)', ')'), code.replace(f'"{ks[0]}": {vals[3]}, ', ''), code.replace(f'del {v}["{ks[1]}"]\n', ''),
            code.replace('val % 10', 'val // 10'), code.replace('.pop(', '.get('), code.replace('.clear()', '.copy()')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    if len(wrong) < 3:
        wrong = uniq(wrong + ['Error: KeyError', '{}', 'None'], [out])
    wrong = fill(wrong, out)
    return mcq(f'What is the output of the following code?\n{code}', out, wrong[:3], f'Trace the dictionary methods. Output: {out}', r)


def freq_out(r):
    t = r.randrange(3)
    if t == 0:
        w = r.choice(['banana', 'mississippi', 'committee', 'balloon', 'assessment', 'success', 'letter', 'coffee', 'bookkeeper', 'tattoo'])
        code = f'w = "{w}"\nD = {{}}\nfor ch in w:\n    if ch in D:\n        D[ch] += 1\n    else:\n        D[ch] = 1\nprint(D)'
    elif t == 1:
        L = [r.choice([2, 3, 5, 7]) for _ in range(7)]
        code = f'L = {L}\nD = {{}}\nfor x in L:\n    D[x] = D.get(x, 0) + 1\nprint(D)'
    else:
        s = r.choice(SENTS)
        code = f's = "{s}"\nD = {{}}\nfor w in s.split():\n    n = len(w)\n    D[n] = D.get(n, 0) + 1\nprint(D)'
    out = run(code)
    alts = [code.replace('+= 1', '= 1'), code.replace('D.get(x, 0) + 1', '1'), code.replace('D.get(n, 0) + 1', 'D.get(n, 1)')]
    wrong = [w for w in uniq([run_or_err(c) for c in alts], [out]) if not w.startswith('Error')]
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': out, 'key': f'2 marks for the correct dictionary: {out}', 'distractors': wrong, 'marks': 2}


DICT_PROGS = [
    ('Write a program to input a string and display the frequency of each character using a dictionary.', 's = input("Enter a string: ")\nD = {}\nfor ch in s:\n    D[ch] = D.get(ch, 0) + 1\nfor k in D:\n    print(k, D[k])', 'level', None),
    ('Write a program to create a dictionary of n students with roll number as key and marks as value, and display the students who scored more than 75.', 'n = int(input("Number of students: "))\nD = {}\nfor i in range(n):\n    roll = int(input("Roll no: "))\n    m = int(input("Marks: "))\n    D[roll] = m\nfor roll in D:\n    if D[roll] > 75:\n        print(roll, D[roll])', '3\n1\n80\n2\n60\n3\n92', '1 80\n3 92'),
    ('Write a program to input a list of words and create a dictionary with each word as key and its length as value.', 'L = input("Enter words: ").split()\nD = {}\nfor w in L:\n    D[w] = len(w)\nprint(D)', 'pen book bag', "{'pen': 3, 'book': 4, 'bag': 3}"),
    ('Write a program that keeps item prices in a dictionary, increases every price by 10% and displays the updated dictionary.', 'D = {"pen": 20, "bag": 500, "book": 150}\nfor k in D:\n    D[k] = D[k] * 1.1\nprint(D)', '', None),
    ('Write a program to count the number of words in a sentence that begin with each letter, using a dictionary.', 's = input("Enter a sentence: ")\nD = {}\nfor w in s.lower().split():\n    D[w[0]] = D.get(w[0], 0) + 1\nprint(D)', 'Save water save life', "{'s': 2, 'w': 1, 'l': 1}"),
    ('Write a program to input names and phone numbers of n friends into a dictionary and then search for a phone number by name.', 'n = int(input("How many? "))\nD = {}\nfor i in range(n):\n    name = input("Name: ")\n    D[name] = input("Phone: ")\nq = input("Search name: ")\nprint(D.get(q, "Not found"))', '2\nAsha\n98100\nRavi\n98200\nRavi', '98200'),
]


# ====================================================================== error finding (class 11 programs)
ERR11 = [
    [('n = int(input("Enter n: "))', 'n = int(input("Enter n: ")'), ('for i in range(1, n + 1):', 'for i in range(1, n + 1)'), ('    if i % 2 == 0:', '    if i % 2 = 0:'),
     ('        print(i, "even")', '        print(i "even")'), ('    else:', '    else'), '        print(i, "odd")'],
    ['s = 0', ('i = 1', 'i == 1'), ('while i <= 10:', 'While i <= 10:'), ('    s = s + i', '    s = s + I'), '    i = i + 1', ('print("Sum is", s)', 'print("Sum is", s')],
    [('word = input("Enter a word: ")', 'word = input("Enter a word: )'), 'count = 0', ('for ch in word:', 'for ch in word'), ('    if ch in "aeiou":', '    if ch in "aeiou"'),
     ('        count = count + 1', '        count = count +'), ('print(count)', 'print count')],
    [('L = [5, 10, 15, 20]', 'L = [5, 10, 15, 20'), 'total = 0', ('for x in L:', 'for x in L'), ('    total += x', '    total =+ x' if False else '    total + = x'),
     ('avg = total / len(L)', 'avg = total / Len(L)'), ('print("Average", avg)', 'print("Average" avg)')],
    [('D = {"pen": 10, "ink": 25}', 'D = {"pen": 10, "ink": 25'), ('for k in D:', 'for k in D'), ('    print(k, D[k])', '    print(k, D(k))'),
     ('D["nib"] = 5', 'D["nib"] == 5' if False else 'D["nib"] = 5)'), ('print(len(D))', 'print(len(D)')],
    [('def area(l, b):', 'def area(l, b)'), ('    return l * b', '    return l x b'), ('a = area(4, 5)', 'a = area(4, 5'), ('if a > 10:', 'if a > 10'),
     ('    print("Large")', '    print("Large)'), ('else:', 'else if:'), '    print("Small")'],
    [('T = (3, 6, 9)', 'T = (3, 6, 9'), ('for t in T:', 'foreach t in T:'), ('    print(t * 2, end=" ")', '    print(t * 2, end=" "'), ('m = max(T)', 'm = max T'),
     ('print("Max", m)', 'print("Max", m))')],
]


def error_find11(r):
    prog = r.choice(ERR11)
    errs = [i for i, ln in enumerate(prog) if isinstance(ln, tuple)]
    chosen = set(r.sample(errs, 4))
    good, bad, fixes = [], [], []
    for i, ln in enumerate(prog):
        if isinstance(ln, tuple):
            g, b = ln
            good.append(g)
            bad.append(b if i in chosen else g)
            if i in chosen:
                fixes.append(f'{b.strip()}  →  {g.strip()}')
        else:
            good.append(ln)
            bad.append(ln)
    gcode = '\n'.join(good)
    assert compiles(gcode), gcode
    return {'stem': f'{r.choice(NAMES)} wrote the following code, but it has errors. Rewrite the correct code and underline the corrections made.\n' + '\n'.join(bad),
            'answer': 'Corrected code:\n' + gcode + '\nCorrections: ' + '; '.join(fixes), 'key': '½ mark for each of the 4 corrections.', 'marks': 2}


# ====================================================================== case-based (4 marks) code scenarios
def _case(who, intro, code, parts):
    """parts: list of (question, expression-or-code-producing-answer, marks). Answers come from running code."""
    qs, ans = [], []
    for i, (q, a, m) in enumerate(parts):
        lab = ['i', 'ii', 'iii', 'iv'][i]
        qs.append(f'({lab}) {q} ({m})')
        ans.append(f'({lab}) {a}')
    return {'stem': f'{who} {intro}\n{code}\n' + '\n'.join(qs), 'answer': ' '.join(ans),
            'key': ' + '.join(str(m) for _, _, m in parts) + ' marks: ' + ' '.join(ans), 'marks': sum(m for _, _, m in parts)}


def py_case(r):
    who = r.choice(NAMES)
    item = r.choice(['notebook', 'pen', 'geometry box', 'water bottle', 'school bag'])
    price = round(r.uniform(20, 400), 1)
    qty = r.randint(2, 9)
    disc = r.choice([5, 10, 12, 15])
    code = (f'item = "{item}"\nprice = {price}\nqty = {qty}\ndiscount = {disc}\npaid = qty >= 5\n'
            f'total = price * qty\nbill = total - total * discount / 100\nprint(item.upper(), qty * 2, round(bill, 2), paid)')
    out = run(code)
    types = run('print(type(' + str(price) + ').__name__, type(' + str(qty) + ').__name__, type(' + str(qty >= 5) + ').__name__)')
    return _case(who, 'wrote this program to prepare a shop bill:', code,
                 [('Write the data types of price, qty and paid.', types.replace(' ', ', '), 1),
                  ('Which operator gives a float result even when both operands are integers? Name one relational operator used.', '/ (true division); >= ', 1),
                  ('Write the exact output of the program.', out, 2)])


def loop_case(r):
    who = r.choice(NAMES)
    n = r.randint(10000, 999999)
    k = int(r.choice(str(n)[1:-1]))
    code = f'n = {n}\ns = 0\ncount = 0\nwhile n > 0:\n    d = n % 10\n    n = n // 10\n    count += 1\n    if d == {k}:\n        continue\n    s = s + d\nprint(count, s)'
    out = run(code)
    alt = run(code.replace('continue', 'break'))
    return _case(who, 'wrote the following code to work with the digits of a number:', code,
                 [('How many times does the loop run?', out.split()[0], 1),
                  ('Write the output of the code.', out, 1),
                  ('Write the output if continue is replaced by break, and explain the difference.', f'{alt}; break leaves the loop at the first digit {k} '
                   f'met, while continue only skips adding that digit', 2)])


def module_case(r):
    who = r.choice(NAMES)
    x = round(r.uniform(2, 9), 2)
    data = [r.randint(1, 20) for _ in range(5)]
    data[3] = data[1]
    import statistics as st
    if len(set(data)) == 5:
        raise ValueError('mode')
    a, b = r.randint(1, 5), r.randint(6, 12)
    code = (f'import math\nimport random\nimport statistics\nx = {x}\nL = {data}\nprint(math.ceil(x), math.floor(x), math.sqrt({r.choice([16, 25, 49, 64, 81])}))\n'
            f'print(statistics.median(L), statistics.mode(L))\nn = random.randint({a}, {b})\nprint(n * 2)')
    lines = run(code.replace(f'random.randint({a}, {b})', str(a))).split('\n')
    return _case(who, 'wrote this program using modules:', code,
                 [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second print statement.', lines[1], 1),
                  ('What are the smallest and largest values the last line can print? Which module function would give a float between 0 and 1?',
                   f'{2 * a} and {2 * b}; random.random()', 2)])


def str_case(r):
    who = r.choice(NAMES)
    dom = r.choice(['school.in', 'mail.com', 'cbse.org', 'learn.edu'])
    em = f'{who.lower()}.{r.choice(["k", "s", "r"])}{r.randint(10, 99)}@{dom}'
    code = f'email = "{em}"\nuser, site = email.split("@")\nprint(site, email.find("@"), email.count("."))\nprint(user[:3].upper() + user[-2:])'
    lines = run(code).split('\n')
    chk = run(f'print("{em}".endswith(".in"), "{em}"[0].isupper())')
    return _case(who, 'is checking e-mail addresses in a school database:', code,
                 [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second print statement.', lines[1], 1),
                  (f'What do email.endswith(".in") and email[0].isupper() return? Why can email[0] = "X" not be used to change the first character?',
                   f'{chk.replace(" ", " and ")}; strings are immutable, so item assignment raises TypeError', 2)])


def list_case(r):
    who = r.choice(NAMES)
    L = r.sample(range(30, 100), 6)
    x = r.choice(L[1:])
    code = f'marks = {L}\nmarks.sort(reverse=True)\ntop3 = marks[:3]\nmarks.append({x})\nprint(top3, marks.count({x}), marks.index({x}))\nprint(sum(top3) / 3)'
    lines = run(code).split('\n')
    return _case(who, 'stores the test marks of a group in a list:', code,
                 [('Write the output of the first print statement.', lines[0], 2), ('Write the output of the second print statement.', lines[1], 1),
                  ('Write a statement to remove the lowest mark from the list marks.', 'marks.remove(min(marks))  (or marks.pop(marks.index(min(marks))))', 1)])


def dict_case(r):
    who = r.choice(NAMES)
    items = r.sample(['pen', 'pencil', 'eraser', 'ruler', 'notebook', 'marker', 'stapler'], 4)
    qty = r.sample(range(5, 60), 4)
    D = dict(zip(items[:3], qty[:3]))
    code = (f'stock = {D}\nstock["{items[3]}"] = {qty[3]}\nstock["{items[0]}"] -= 5\nT = tuple(stock.values())\n'
            f'print(len(stock), stock.get("{items[1]}", 0), stock.get("glue", 0))\nprint(T[1:3], max(T))')
    lines = run(code).split('\n')
    return _case(who, 'keeps the stock of a stationery shop in a dictionary:', code,
                 [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second print statement.', lines[1], 1),
                  ('Why is get() used for "glue" instead of stock["glue"]? Can T[0] = 10 be used to change T? Why?',
                   'get() returns the default 0 instead of raising KeyError for a missing key; no – T is a tuple, which is immutable (TypeError)', 2)])


# ====================================================================== guard for engine source-extract items
def no_open_pick(fams):
    """Regenerate a source-extract (case) variant whose open part (i) is a recall line worded to pick from options
    ('Which of the following ...', '... NOT ...') that the extract item does not show, or whose part (ii) asks to
    explain the term that answers part (i)."""
    import re
    for fs in fams.values():
        for f in fs:
            if f.type == 'case':
                def gen(r, g=f.gen):
                    v = g(r)
                    p1 = re.search(r"\(i\) (.*?) \(1\)", v['stem'])
                    if p1 and re.search(r"Which of (these|the following)|\bNOT\b", p1.group(1)):
                        raise ValueError('open part (i) cannot ask to pick from unseen options')
                    t = re.search(r"\(ii\) Explain the term '([^']+)'", v['stem'])
                    a = re.search(r"^\(i\) (.*?) \(ii\)", v['answer'])
                    if t and a and a.group(1).strip().rstrip('.').lower() == t.group(1).lower():
                        raise ValueError('source item asks the same term twice')
                    return v
                f.gen = gen
    return fams
