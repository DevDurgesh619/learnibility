"""Cambridge International AS Level Computer Science 9618 (syllabus sections 1-12), grade 11.

Paper 1 (Theory Fundamentals) and Paper 2 (Fundamental Problem-solving and Programming) style items.
Pseudocode follows the Cambridge 9618 pseudocode guide (DECLARE, <-, IF ... THEN ... ENDIF, FOR ... NEXT,
WHILE ... ENDWHILE, REPEAT ... UNTIL, CASE OF ... ENDCASE, PROCEDURE/FUNCTION ... RETURNS, BYREF/BYVAL,
OPENFILE/READFILE/WRITEFILE/CLOSEFILE, MID/LEFT/RIGHT/LENGTH, MOD/DIV). Assembly language uses the
9618 instruction set (LDM, LDD, LDI, LDX, LDR, MOV, STO, ADD, SUB, INC, DEC, JMP, CMP, CMI, JPE, JPN,
AND, OR, XOR, LSL, LSR, END). Every computed answer is produced by the code that builds the stem.
"""
import math
import random
import re

from ._lib import topic, mcq, compose, person, two_people, city, CTX  # noqa: F401

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# =============================================================================== shared helpers
ORGS = [('Riverside Medical Centre', 'medical centre'), ('BlueWave Supermarkets', 'supermarket chain'), ('Northfield Academy', 'school'),
        ('Harbour Bank', 'bank'), ('SkyLink Airways', 'airline'), ('City Central Library', 'library'), ('SwiftCar Rentals', 'car rental company'),
        ('Starlight Cinemas', 'cinema chain'), ('Palm Grove Hotel', 'hotel'), ('TransGlobal Logistics', 'logistics company'),
        ('Eagles Sports Club', 'sports club'), ('GreenLeaf Pharmacy', 'pharmacy'), ('Summit Engineering', 'engineering firm'),
        ('Coral Bay Aquarium', 'aquarium'), ('MetroBus', 'bus company'), ('Sunrise Bakery', 'bakery'), ('Orbit Games Studio', 'games studio'),
        ('Lakeside College', 'college'), ('Pioneer Insurance', 'insurance company'), ('FreshFarm Foods', 'food producer'),
        ('Nova Telecom', 'telecommunications company'), ('Atlas Museum', 'museum'), ('Peak Fitness', 'gym chain'), ('Horizon Travel', 'travel agency')]

_PH = re.compile(r'\{(\w+)\}')
_MK = re.compile(r'\[(\d+)\]\s*$')


def ctx(r):
    a, b = r.sample(['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Ethan', 'Priya', 'Omar', 'Chloe',
                     'Daniel', 'Mei', 'Tariq', 'Hana', 'Jonas', 'Ines', 'Kwame', 'Yusuf', 'Elena', 'Ravi', 'Freya', 'Diego', 'Nadia',
                     'Samuel', 'Ana', 'Felix', 'Sipho', 'Lina', 'Arjun', 'Grace', 'Mohammed', 'Isla', 'Tomás'], 2)
    o, ot = r.choice(ORGS)
    return {'p': a, 'q': b, 'city': city(r), 'org': o, 'otype': ot, 'aot': ('an ' if ot[0] in 'aeiou' else 'a ') + ot}


def fill(s, d):
    return _PH.sub(lambda m: str(d.get(m.group(1), m.group(0))), s)


def Q(stem, ans, key, marks=None, typ=None, opts=None):
    q = {'stem': stem, 'answer': ans, 'key': key}
    if marks:
        q['marks'] = marks
    if typ:
        q['type'] = typ
    if opts:
        q['options'] = opts
    return q


def MCQ(r, stem, ans, dis, key):
    ds = []
    for d in dis:
        d = str(d)
        if d != ans and d not in ds:
            ds.append(d)
    if len(ds) < 3:
        return None
    last = re.split(r'(?<=[.?])\s+', stem.strip())[-1]
    if stem.endswith('.') and re.match(r'(What|How|Which|Who|Why|When|Where)\b', last):
        stem = stem[:-1] + '?'
    opts, a = mcq(r, ans, ds)
    return {'stem': stem, 'options': opts, 'answer': a, 'key': key, 'marks': 1}


def code(lines):
    """Render pseudocode/assembly lines (strings) as a block."""
    return '\n'.join(lines)


def items(t, C, D, entries, typ=None, name='items'):
    """Template drawing one entry and filling {placeholders}; entries (stem, answer, key[, distractors])."""
    def fn(r, D_):
        e = r.choice(entries)
        d = ctx(r)
        stem, ans, key = fill(e[0], d), fill(e[1], d), fill(e[2], d)
        if len(e) > 3 and e[3]:
            return MCQ(r, stem, ans, [fill(x, d) for x in e[3]], key)
        return Q(stem, ans, key, typ=typ)
    fn.__name__ = name
    t.add(C, D, typ or ('short' if C == 'C3' else None))(fn)
    return fn


def scen(t, C, D, intros, parts, k=(2, 3), typ=None, name='scen'):
    """Structured multi-part item: random intro (placeholders filled) + random subset of parts.
    parts: (text, answer, key-with-[n]) tuples or callables (r, d) -> tuple."""
    def fn(r, D_):
        d = ctx(r)
        d['D'] = D_
        intro = fill(r.choice(intros), d)
        ps = []
        for p in parts:
            if callable(p):
                ps.append(lambda rr, p=p: p(rr, d))
            else:
                ps.append(lambda rr, p=p: (fill(p[0], d), fill(p[1], d), fill(p[2], d)))
        return compose(r, intro, ps, k=k, type_=typ or ('multi_step' if C == 'C4' else ('explain' if C == 'C2' else 'short')))
    fn.__name__ = name
    t.add(C, D, typ)(fn)
    return fn


ESSAY_FORMS = ['Evaluate {p}.', 'Discuss {p}.', 'Assess {p}.', 'Discuss, with reasons, {p}.']
ESSAY_MARKS = {1: 4, 2: 4, 3: 6, 4: 8, 5: 9}


def essay(t, prompts, scenes, D=(3, 4, 5)):
    """C4 extended response. prompts: (task phrase, points for, points against/other side, conclusion hint)."""
    def fn(r, D_):
        task, pro, con, concl = r.choice(prompts)
        d = ctx(r)
        scene = fill(r.choice(scenes), d)
        form = r.choice(ESSAY_FORMS)
        stem = scene + ' ' + fill(form.replace('{p}', task), d)
        m = ESSAY_MARKS[D_]
        ans = fill(f'Points in favour: {pro} Points against / limitations: {con} Conclusion: {concl}', d)
        key = (f'Up to {m // 2} marks for relevant technical points correctly applied to the scenario; up to {m - m // 2} marks for '
               f'developed explanation that weighs both sides and reaches a justified conclusion. Indicative content: {fill(pro, d)} / {fill(con, d)} [{m}]')
        return Q(stem, ans, key, marks=m, typ='long')
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)
    return fn


AR_OPTS = ['Both A and R are true, and R is the correct explanation of A',
           'Both A and R are true, but R is not the correct explanation of A',
           'A is true but R is false', 'A is false but R is true']


def ar(t, pairs, falses, D=(2, 3)):
    """Assertion-Reason MCQs. pairs: (assertion, reason that explains it); falses: false statements."""
    def fn(r, D_):
        case = r.randrange(4)
        i = r.randrange(len(pairs))
        if case == 0:
            a, rr = pairs[i]
        elif case == 1:
            j = r.choice([x for x in range(len(pairs)) if x != i])
            a, rr = pairs[i][0], pairs[j][1]
        elif case == 2:
            a, rr = pairs[i][0], r.choice(falses)
        else:
            a, rr = r.choice(falses), pairs[i][1]
        stem = f'Assertion (A): {a} Reason (R): {rr} Which option is correct?'
        key = {0: 'A is true and R gives the reason for it.', 1: 'A and R are both true statements, but R does not explain A.',
               2: f'A is true; R is false: "{rr}" is incorrect.', 3: f'A is false: "{a}" is incorrect; R is a true statement.'}[case]
        return {'stem': stem, 'options': list(AR_OPTS), 'answer': AR_OPTS[case], 'key': key, 'marks': 1}
    fn.__name__ = 'ar'
    t.add('C2', D, 'mcq')(fn)
    return fn


def finalize(chapters):
    """Give every single-part item marks equal to the trailing [n] of its key."""
    for tps in chapters.values():
        for tp in tps:
            for tpl in tp.templates:
                if getattr(tpl, '_w', False):
                    continue
                tpl._w = True
                f = tpl.fn

                def g(r, D, f=f):
                    q = f(r, D)
                    if q and 'marks' not in q:
                        if q.get('options'):
                            q['marks'] = 1
                        else:
                            m = _MK.search(q['key'])
                            if m:
                                q['marks'] = int(m.group(1))
                    return q
                tpl.fn = g


def b(n, w=8):
    return format(n % (1 << w), f'0{w}b')


def hx(n, w=2):
    return format(n, f'0{w}X')


def tc(n, w=8):
    return b(n, w)


def from_tc(s):
    v = int(s, 2)
    return v - (1 << len(s)) if s[0] == '1' else v


def places(w):
    return ', '.join(str(1 << i) for i in range(w - 1, -1, -1))


def plural(n, w):
    return f'{n} {w}' + ('' if n == 1 else 's')


# =============================================================================== Chapter 1 Information representation
t1_1 = topic('Binary, denary and hexadecimal conversion; binary and decimal prefixes (kibi, mebi vs kilo, mega)', 'binary, denary and hexadecimal', 'binary and decimal prefixes')
t1_1.fixed('C1', (1, 2), [
    ('How many bytes are there in one kibibyte (KiB)?', '1024', '1 KiB = 2¹⁰ bytes = 1024 bytes; 1 kB = 1000 bytes.', ['1000', '1024 000', '8192']),
    ('Which prefix represents 10⁶ bytes?', 'mega (MB)', 'Decimal prefixes: kilo 10³, mega 10⁶, giga 10⁹; binary prefixes: kibi 2¹⁰, mebi 2²⁰, gibi 2³⁰.', ['mebi (MiB)', 'kibi (KiB)', 'gibi (GiB)']),
    ('How many bytes are there in one mebibyte (MiB)?', '1 048 576', '1 MiB = 2²⁰ = 1024 × 1024 = 1 048 576 bytes.', ['1 000 000', '1 024 000', '1 000 024']),
    ('What is the largest denary value that can be stored in one unsigned byte?', '255', '8 bits: 2⁸ − 1 = 255.', ['256', '127', '128']),
    ('Which hexadecimal digit represents denary 13?', 'D', 'A = 10, B = 11, C = 12, D = 13, E = 14, F = 15.', ['C', 'E', 'B']),
    ('How many bits are needed to represent one hexadecimal digit?', '4', 'One hex digit has 16 values = 2⁴, so one nibble (4 bits).', ['2', '8', '16']),
    ('What is a nibble?', 'A group of 4 bits', 'A nibble is half a byte: 4 bits.', ['A group of 8 bits', 'A group of 2 bits', 'A group of 16 bits']),
    ('Which of these is a binary (IEC) prefix?', 'gibi', 'Binary prefixes: kibi, mebi, gibi, tebi (powers of 2¹⁰).', ['giga', 'mega', 'tera']),
    ('State what is meant by a byte.', 'A group of 8 bits, the unit used to represent one character in ASCII and to address memory.', '1 mark: 8 bits [1]'),
])
t1_1.fixed('C2', (2, 3, 4), [
    ('Explain why a storage device advertised as 500 GB appears smaller when its capacity is shown by an operating system in GiB.',
     'The manufacturer uses decimal prefixes (1 GB = 10⁹ bytes) but the operating system reports binary prefixes (1 GiB = 2³⁰ bytes). Since 2³⁰ > 10⁹, the same number of bytes gives a smaller number of GiB (about 466 GiB).',
     '1 mark: GB = 10⁹ bytes; 1 mark: GiB = 2³⁰ bytes, which is larger; 1 mark: so the same capacity is a smaller number of GiB [3]'),
    ('Explain why hexadecimal is often used by programmers instead of binary.',
     'Hexadecimal is shorter and easier to read, write and remember; there are fewer errors when copying; each hex digit maps directly onto 4 bits so conversion is simple.',
     '1 mark each, max 2: shorter/easier to read; fewer errors; direct 4-bit mapping [2]'),
    ('Give two uses of hexadecimal in computer science and explain why it is suitable for each.',
     'MAC addresses and colour codes in HTML/CSS (e.g. #FF8800); memory dumps and error codes. Each hex digit maps to 4 bits so long binary values are shown compactly.',
     '1 mark per use (MAC address, HTML colour codes, memory dumps, assembly/machine code addresses, error codes), max 2; 1 mark for the reason [3]'),
    ('Explain the difference between a kilobyte and a kibibyte.',
     'A kilobyte (kB) is a decimal unit of 1000 bytes; a kibibyte (KiB) is a binary unit of 1024 bytes (2¹⁰).',
     '1 mark: kB = 1000 bytes (10³); 1 mark: KiB = 1024 bytes (2¹⁰) [2]'),
    ('Explain why computers use binary to represent data.',
     'Computers are built from switches (transistors) with two states, on and off, which map directly to 1 and 0; two states are easy to distinguish reliably.',
     '1 mark: electronic circuits/transistors have two states; 1 mark: two states map to 1/0 and are reliable to distinguish [2]'),
])


def _conv(r, D):
    w = 8 if D <= 2 else (12 if D == 3 else 16)
    n = r.randrange(16, 1 << w)
    kind = r.choice(['d2b', 'b2d', 'd2h', 'h2d', 'b2h', 'h2b'])
    hw = w // 4
    B, H = b(n, w), hx(n, hw)
    work_b = f'place values {places(w)}: ' + ' + '.join(str(1 << (w - 1 - i)) for i, c in enumerate(B) if c == '1') + f' = {n}'
    nib = ' '.join(B[i:i + 4] for i in range(0, w, 4))
    if kind == 'd2b':
        stem, ans, key = f'Convert the denary number {n} into {w}-bit binary.', B, f'{work_b}, so {n} = {B} [2]'
        dis = [b(n + 1, w), b(n - 1, w), B[::-1] if B[::-1] != B else b(n ^ 3, w)]
    elif kind == 'b2d':
        stem, ans, key = f'Convert the {w}-bit binary number {B} into denary.', str(n), f'{work_b} [2]'
        dis = [str(n + 1), str(int(B[::-1], 2)) if int(B[::-1], 2) != n else str(n + 2), str(n - 1), str(n * 2)]
    elif kind == 'd2h':
        stem, ans, key = f'Convert the denary number {n} into hexadecimal.', H, f'{n} = {nib} in binary; each nibble gives one hex digit: {H} [2]'
        dis = [hx(n + 1, hw), hx(n - 1, hw), H[::-1] if H[::-1] != H else hx(n + 16, hw)]
    elif kind == 'h2d':
        stem, ans, key = f'Convert the hexadecimal number {H} into denary.', str(n), ' + '.join(f'{int(c, 16)} × {16 ** (hw - 1 - i)}' for i, c in enumerate(H)) + f' = {n} [2]'
        dis = [str(n + 1), str(n - 1), str(int(H[::-1], 16)) if int(H[::-1], 16) != n else str(n + 16)]
    elif kind == 'b2h':
        stem, ans, key = f'Convert the binary number {B} into hexadecimal.', H, f'Split into nibbles {nib}; convert each nibble: {H} [2]'
        dis = [hx(n + 1, hw), H[::-1] if H[::-1] != H else hx(n + 1, hw), hx(n - 1, hw), hx(n ^ 0x11, hw)]
    else:
        stem, ans, key = f'Convert the hexadecimal number {H} into {w}-bit binary.', B, f'Each hex digit becomes 4 bits: {nib} [2]'
        dis = [b(n + 1, w), b(n - 1, w), B[::-1] if B[::-1] != B else b(n ^ 5, w)]
    if D == 1:
        return MCQ(r, stem.replace('Convert', 'What is the result of converting').rstrip('.') + '?', ans, dis, key.replace(' [2]', ''))
    if D >= 4:
        return Q(stem + ' Show your working.', ans, key.replace(' [2]', '; 1 mark method, 1 mark answer [2]'), marks=2)
    return Q(stem, ans, key, marks=2)


t1_1.add('C3', (1, 2, 3, 4, 5))(_conv)


@t1_1.add('C3', (1, 2, 3, 4))
def t1_1_prefix(r, D):
    kind = r.choice(['kib', 'mib', 'diff', 'gib', 'bits'])
    n = r.choice([2, 3, 4, 5, 6, 8, 12, 16, 20, 24, 32, 64])
    if kind == 'kib':
        v = n * 1024
        stem, ans, key = f'A text file has a size of {n} KiB. Calculate its size in bytes.', f'{v} bytes', f'1 KiB = 1024 bytes; {n} × 1024 = {v} bytes [1]'
        dis = [f'{n * 1000} bytes', f'{n * 8 * 1024} bytes', f'{n * 1024 * 1024} bytes']
    elif kind == 'mib':
        v = n * 1024
        stem, ans, key = f'A photograph is {n} MiB. How many KiB is this?', f'{v} KiB', f'1 MiB = 1024 KiB; {n} × 1024 = {v} KiB [1]'
        dis = [f'{n * 1000} KiB', f'{n * 1024 * 1024} KiB', f'{n * 8} KiB']
    elif kind == 'diff':
        v = n * 1048576 - n * 1000000
        stem, ans, key = f'Calculate the difference, in bytes, between {n} MiB and {n} MB.', f'{v:,} bytes', f'{n} MiB = {n} × 1 048 576 = {n * 1048576:,}; {n} MB = {n * 1000000:,}; difference = {v:,} bytes [2]'
        dis = [f'{n * 24:,} bytes', f'{n * 24576:,} bytes', f'{v * 8:,} bytes']
    elif kind == 'gib':
        v = n * 1024
        stem, ans, key = f'A memory card holds {n} GiB. State its capacity in MiB.', f'{v} MiB', f'1 GiB = 1024 MiB; {n} × 1024 = {v} MiB [1]'
        dis = [f'{n * 1000} MiB', f'{n * 1024 * 1024} MiB', f'{n * 100} MiB']
    else:
        v = n * 1024 * 8
        stem, ans, key = f'How many bits are there in {n} KiB?', f'{v:,} bits', f'{n} KiB = {n} × 1024 bytes = {n * 1024} bytes; × 8 = {v:,} bits [2]'
        dis = [f'{n * 8000:,} bits', f'{n * 1024:,} bits', f'{n * 1024 * 1024 * 8:,} bits']
    if D <= 2 and r.random() < 0.6:
        return MCQ(r, stem.replace('Calculate', 'What is').replace('. How', '. How').replace('State', 'What is'), ans, dis, key)
    return Q(stem + (' Show your working.' if D >= 3 else ''), ans, key)


@t1_1.add('C2', (2, 3, 4), 'explain')
def t1_1_error(r, D):
    n = r.randrange(40, 250)
    B = b(n)
    d = ctx(r)
    kind = r.choice(['hex', 'den'])
    if kind == 'hex':
        right = hx(n)
        wrong = hx(int(B[4:] + B[:4], 2))
        if wrong == right:
            return None
        stem = f'{d["p"]} converts the binary number {B} into hexadecimal and writes {wrong}. Explain the error and give the correct answer.'
        ans = f'{d["p"]} converted the nibbles in the wrong order. Split into {B[:4]} {B[4:]}: the left nibble gives {right[0]} and the right gives {right[1]}, so the answer is {right}.'
        key = '1 mark: identifies nibbles swapped/read in wrong order; 1 mark: correct answer ' + right + ' [2]'
    else:
        wrong = int(B[::-1], 2)
        if wrong == n:
            return None
        stem = f'{d["p"]} converts {B} into denary and gets {wrong}. Identify the mistake and state the correct denary value.'
        ans = f'The place values were applied from the wrong end (the leftmost bit is the most significant, worth 128). Correct value: {n}.'
        key = f'1 mark: place values applied right-to-left / MSB taken as 1; 1 mark: {n} [2]'
    return Q(stem, ans, key)


def _p_hexcolour(r, d):
    R, G, B_ = r.randrange(256), r.randrange(256), r.randrange(256)
    code_ = hx(R) + hx(G) + hx(B_)
    return (f'A web page uses the colour code #{code_}. Convert the red component ({hx(R)}) into denary.', str(R), f'{hx(R)}: {int(hx(R)[0], 16)} × 16 + {int(hx(R)[1], 16)} = {R} [2]')


def _p_mac(r, d):
    v = r.randrange(16, 256)
    return (f'One byte of a MAC address is {hx(v)}. Write this byte in 8-bit binary.', b(v), f'{hx(v)[0]} → {b(int(hx(v)[0], 16), 4)}, {hx(v)[1]} → {b(int(hx(v)[1], 16), 4)}: {b(v)} [2]')


def _p_add(r, d):
    a, c = r.randrange(20, 120), r.randrange(20, 120)
    return (f'Two counters hold the hexadecimal values {hx(a)} and {hx(c)}. Calculate their sum, giving your answer in hexadecimal.', hx(a + c),
            f'{hx(a)} = {a}, {hx(c)} = {c}; sum = {a + c} = {hx(a + c)} [2]')


def _p_largest(r, d):
    w = r.choice([10, 12, 16, 20])
    return (f'State the largest unsigned denary value that can be stored in {w} bits.', str((1 << w) - 1), f'2^{w} − 1 = {(1 << w) - 1} [1]')


scen(t1_1, 'C4', (2, 3, 4, 5), [
    'A technician at {org} in {city} is examining values stored in a computer system.',
    '{p} is writing a program for {org} that displays numbers in several number bases.',
    'A memory dump from a computer at {org} shows several values written in hexadecimal.',
], [_p_hexcolour, _p_mac, _p_add, _p_largest,
    ('Explain why the technician reads the values in hexadecimal rather than binary.', 'Hex is shorter, easier to read and less error-prone; each digit maps to 4 bits.', '1 mark: shorter/easier; 1 mark: direct mapping to nibbles [2]'),
    ('State the number of bytes in 3 KiB and the number in 3 kB.', '3072 bytes; 3000 bytes', '1 mark each: 3 × 1024 = 3072, 3 × 1000 = 3000 [2]')], k=(3, 4))

# ----------------------------------------------------------------------------- 1.2 two's complement
t1_2 = topic("Two's complement, binary addition and subtraction, overflow and BCD", "two's complement", 'binary addition', 'bcd')
t1_2.fixed('C1', (1, 2), [
    ("What is the range of denary values that can be stored in 8-bit two's complement?", '−128 to +127', "Range = −2⁷ to 2⁷ − 1.", ['−127 to +127', '0 to 255', '−128 to +128']),
    ("In 8-bit two's complement, what is the place value of the most significant bit?", '−128', "The MSB has a negative weight of −2⁷ = −128.", ['128', '−1', '−127']),
    ('What is meant by overflow in binary arithmetic?', 'The result is too large to be stored in the number of bits available', 'Overflow: the result of a calculation needs more bits than the register holds, so the stored value is wrong.',
     ['The result is negative', 'A carry is produced from bit 0 to bit 1', 'The number has too many decimal places']),
    ('How many bits are used to store each denary digit in binary coded decimal (BCD)?', '4', 'BCD codes each denary digit 0–9 as a separate nibble.', ['8', '2', '10']),
    ("Which 8-bit two's complement value represents −1?", '11111111', "−1 = −128 + 127, all bits set.", ['10000001', '00000001', '10000000']),
    ('Which of these is NOT a valid BCD nibble?', '1010', 'BCD nibbles only represent 0–9 (0000–1001); 1010 to 1111 are unused.', ['1001', '0111', '0000']),
    ("State the denary value of the 8-bit two's complement number 10000000.", '−128', 'MSB weight −128, all other bits 0 [1]'),
])
t1_2.fixed('C2', (2, 3, 4), [
    ("Explain how to find the two's complement of a positive binary number to represent its negative.", 'Invert (flip) every bit, then add 1 to the result.', '1 mark: invert all bits (one\'s complement); 1 mark: add 1 [2]'),
    ('Explain one practical use of binary coded decimal (BCD).', 'Digital clocks/calculators/displays, where each digit is shown separately; BCD lets each nibble drive one digit of the display and avoids rounding errors in currency.',
     '1 mark: use (digital display, clock, calculator, financial values); 1 mark: each denary digit stored/displayed separately or exact decimal representation [2]'),
    ("Explain why two's complement is preferred to sign and magnitude for storing signed integers.", 'There is only one representation of zero, and addition and subtraction work with the same circuit (subtraction by adding the negative).',
     '1 mark: single zero; 1 mark: arithmetic works directly / subtraction becomes addition [2]'),
    ('Explain how a processor can detect overflow when two positive numbers are added in two\'s complement.', 'If the two operands have sign bit 0 but the result has sign bit 1, the true answer is too large and overflow has occurred.',
     '1 mark: both operands positive (MSB 0); 1 mark: result MSB is 1 / appears negative so overflow flag set [2]'),
])


def _tc_rng(r, D):
    if D <= 2:
        return r.choice([r.randrange(-60, -1), r.randrange(-128, -60)])
    return r.choice([r.randrange(-128, -1), r.randrange(1, 127)])


@t1_2.add('C3', (1, 2, 3, 4, 5))
def t1_2_tc(r, D):
    n = _tc_rng(r, D)
    w = 8 if D < 5 else 12
    if D == 5:
        n = r.randrange(-2048, -129)
    s = tc(n, w)
    if r.random() < 0.5:
        stem = f"Convert the denary number {n} into {w}-bit two's complement binary."
        ans = s
        pos = b(abs(n), w)
        key = (f'+{abs(n)} = {pos}; invert = {"".join("1" if c == "0" else "0" for c in pos)}; add 1 = {s} [2]' if n < 0 else f'Positive: same as unsigned binary, {s} [2]')
        dis = [b(abs(n), w), '1' + b(abs(n), w)[1:], tc(n - 1, w), tc(-n - 1, w)]
    else:
        stem = f"The {w}-bit binary number {s} is in two's complement. Convert it into denary."
        ans = str(n)
        bits = [(1 << (w - 1 - i)) * (-1 if i == 0 else 1) for i, c in enumerate(s) if c == '1']
        key = ' + '.join(f'({x})' if x < 0 else str(x) for x in bits) + f' = {n} [2]'
        dis = [str(int(s, 2)), str(-n), str(n + 1), str(n - 1)]
    if D == 1:
        return MCQ(r, stem.rstrip('.') + '. Which is correct?', ans, dis, key.replace(' [2]', ''))
    return Q(stem, ans, key, marks=2)


@t1_2.add('C3', (2, 3, 4, 5), 'numerical')
def t1_2_add(r, D):
    mode = r.choice(['unsigned', 'signed', 'sub']) if D >= 3 else r.choice(['unsigned', 'sub'])
    if mode == 'unsigned':
        a, c = r.randrange(30, 220), r.randrange(30, 220)
        if D <= 2:
            c = r.randrange(10, 255 - a) if a < 245 else 5
        s = a + c
        ov = s > 255
        stem = f'Add the unsigned 8-bit binary numbers {b(a)} and {b(c)}. Give the 8-bit result and state whether overflow has occurred.'
        ans = f'{b(s)}; ' + ('overflow has occurred (a carry out of bit 7; true sum ' + str(s) + ' > 255)' if ov else 'no overflow')
        key = f'{a} + {c} = {s}; column addition with carries gives {b(s)} [1]; ' + ('carry out of the MSB so overflow [1]' if ov else 'no carry out of MSB, no overflow [1]') + ' [2]'
    elif mode == 'signed':
        a, c = r.randrange(-100, 120), r.randrange(-100, 120)
        s = a + c
        ov = not (-128 <= s <= 127)
        stem = f"The 8-bit two's complement numbers {tc(a)} and {tc(c)} are added. Give the 8-bit result, its denary value, and state whether overflow occurs."
        res = tc(s)
        ans = f'{res}; ' + (f'overflow: the true result {s} is outside −128 to 127, so the stored value {from_tc(res)} is wrong' if ov else f'= {s}, no overflow')
        key = f'{tc(a)} = {a}, {tc(c)} = {c}; sum {res} [1]; ' + (f'signs of operands same but result sign different → overflow [1]' if ov else f'denary {s} [1]') + '; overflow decision [1] [3]'
        return Q(stem, ans, key, marks=3)
    else:
        a, c = r.randrange(20, 127), r.randrange(5, 127)
        s = a - c
        stem = f"Using two's complement, show how the 8-bit processor calculates {a} − {c}. Give the result in binary."
        ans = tc(s) + f' (= {s})'
        key = f'{a} = {b(a)} [1]; −{c} = {tc(-c)} [1]; add, ignore carry out of bit 7: {tc(s)} = {s} [1] [3]'
        return Q(stem, ans, key, marks=3)
    return Q(stem, ans, key, marks=2)


@t1_2.add('C3', (1, 2, 3))
def t1_2_bcd(r, D):
    n = r.randrange(10, 1000) if D >= 2 else r.randrange(10, 100)
    s = ' '.join(b(int(c), 4) for c in str(n))
    if r.random() < 0.5:
        stem, ans = f'Write the denary number {n} in binary coded decimal (BCD).', s
        key = ', '.join(f'{c} → {b(int(c), 4)}' for c in str(n)) + ' [2]'
        dis = [b(n, 4 * len(str(n))), ' '.join(b(int(c), 4)[::-1] for c in str(n)), ' '.join(b(int(c) + 1, 4) for c in str(n))]
    else:
        stem, ans = f'The BCD value {s} is shown on a digital display. State the denary number it represents.', str(n)
        key = 'Each nibble is one digit: ' + ', '.join(f'{b(int(c), 4)} = {c}' for c in str(n)) + ' [1]'
        dis = [str(int(s.replace(' ', ''), 2)), str(n)[::-1] if str(n)[::-1] != str(n) else str(n + 1), str(n + 10)]
    if D == 1:
        return MCQ(r, stem.replace('Write', 'Which is').replace('State', 'What is'), ans, dis, key)
    return Q(stem, ans, key)


@t1_2.add('C2', (2, 3, 4), 'explain')
def t1_2_err(r, D):
    n = r.randrange(5, 120)
    d = ctx(r)
    wrong = '1' + b(n)[1:]
    stem = f"{d['p']} says that −{n} in 8-bit two's complement is {wrong}. Explain why this is incorrect and give the correct representation."
    ans = f'{d["p"]} has used sign and magnitude (just setting the MSB to 1). In two\'s complement, invert the bits of {b(n)} and add 1: {tc(-n)}.'
    key = f'1 mark: identifies sign-and-magnitude method used / MSB worth −128; 1 mark: correct value {tc(-n)} [2]'
    return Q(stem, ans, key)


def _p_ov(r, d):
    a, c = r.randrange(70, 127), r.randrange(70, 127)
    return (f'The sensor readings {a} and {c} are added in an 8-bit two\'s complement register. Show the result in binary and explain what has happened.', f'{tc(a + c)}; overflow – the result appears to be {from_tc(tc(a + c))} because {a + c} > 127',
            f'1 mark: binary result {tc(a + c)}; 1 mark: overflow, two positives give a negative; 1 mark: true value {a + c} exceeds 127 [3]')


def _p_neg(r, d):
    n = r.randrange(-120, -5)
    return (f'A temperature of {n} °C must be stored. Give its 8-bit two\'s complement representation.', tc(n), f'1 mark for working (invert and add 1), 1 mark for {tc(n)} [2]')


def _p_bcd(r, d):
    n = r.randrange(10, 60)
    return (f'The display shows the minutes value {n} using BCD. Write the BCD code.', ' '.join(b(int(c), 4) for c in str(n)), f'1 mark per correct nibble [2]')


scen(t1_2, 'C4', (2, 3, 4, 5), [
    'A weather station in {city} stores temperature readings as 8-bit two\'s complement integers and shows the time on a digital display.',
    'An embedded weather logger built for {org} uses 8-bit two\'s complement registers for temperatures and a digital clock display.',
], [_p_ov, _p_neg, _p_bcd,
    ('Suggest how the problem of overflow could be avoided.', 'Use more bits (e.g. a 16-bit register) for the result.', '1 mark: larger register / more bits; 1 mark: justification that the range increases to −32768 to 32767 [2]'),
    ('Explain why the station might store the display time in BCD rather than pure binary.', 'Each digit can be sent straight to one 7-segment display; no conversion is needed.', '1 mark: each digit stored separately; 1 mark: easy to drive digital display [2]')], k=(3, 4))

# ----------------------------------------------------------------------------- 1.3 character sets
t1_3 = topic('Character sets: ASCII, extended ASCII and Unicode', 'character sets', 'ascii', 'unicode')
t1_3.fixed('C1', (1, 2), [
    ('How many bits does standard ASCII use for each character code?', '7', 'Standard ASCII is a 7-bit code (128 characters); extended ASCII uses 8 bits (256).', ['8', '16', '32']),
    ('How many different characters can extended ASCII represent?', '256', 'Extended ASCII uses 8 bits: 2⁸ = 256 codes.', ['128', '65 536', '512']),
    ('What is a character set?', 'All the characters a computer can represent, each with a unique binary code', 'Character set: the set of symbols recognised by the computer, each mapped to a unique code.',
     ['The fonts installed on a computer', 'The keys on a keyboard', 'The set of instructions a processor can execute']),
    ('Why was Unicode developed?', 'To represent the characters of all the world\'s languages', 'ASCII could not represent non-Latin scripts; Unicode gives a code to characters from all languages and symbols such as emoji.',
     ['To make text files smaller than ASCII', 'To replace binary with hexadecimal', 'To encrypt text']),
    ('If the ASCII code of "A" is 65, what is the ASCII code of "a"?', '97', 'Lower-case letters are 32 more than upper-case.', ['66', '33', '129']),
    ('The ASCII code for the character "0" is 48. What is the code for "7"?', '55', 'Digits are consecutive: 48 + 7 = 55.', ['7', '56', '103']),
])
t1_3.fixed('C2', (2, 3, 4), [
    ('Explain why a text file saved using Unicode may be larger than the same file saved in ASCII.', 'Unicode uses more bits per character (for example 16 or 32 bits) than ASCII (7 or 8 bits), so each character takes more storage.',
     '1 mark: Unicode uses more bits/bytes per character; 1 mark: comparison of bits (e.g. 16/32 v 8) [2]'),
    ('Explain why the characters "5" and the integer 5 are stored differently.', 'The character "5" is stored as its character code (ASCII 53, 00110101); the integer 5 is stored as its binary value 00000101.',
     '1 mark: character stored as its code (53); 1 mark: integer stored as pure binary 101 [2]'),
    ('Explain how sorting text alphabetically can use character codes, and one problem with doing this.', 'Codes are in alphabetical order so strings can be compared code by code; but upper case codes are less than lower case codes, so "Zebra" is sorted before "apple".',
     '1 mark: compare codes character by character; 1 mark: problem with case (upper before lower) or accented letters [2]'),
    ('Explain why an international company would choose Unicode rather than ASCII for its customer database.', 'Customers\' names and addresses may use non-Latin scripts (Arabic, Chinese, Devanagari); ASCII cannot represent them, Unicode can.',
     '1 mark: need for many languages/scripts; 1 mark: ASCII limited to 128/256 characters, mostly English [2]'),
])


@t1_3.add('C3', (1, 2, 3, 4))
def t1_3_code(r, D):
    up = r.random() < 0.6
    base = 65 if up else 97
    ch = chr(base + r.randrange(1, 26))
    c = ord(ch)
    ref = 'A' if up else 'a'
    fmt_ = r.choice(['denary', 'binary', 'hexadecimal']) if D >= 2 else 'denary'
    val = {'denary': str(c), 'binary': b(c), 'hexadecimal': hx(c)}[fmt_]
    stem = f'The ASCII code for "{ref}" is {base} in denary. State the ASCII code for "{ch}" in {fmt_}' + (' (8 bits)' if fmt_ == 'binary' else '') + '.'
    key = f'"{ch}" is {c - base} letters after "{ref}": {base} + {c - base} = {c}' + (f' = {val}' if fmt_ != 'denary' else '') + ' [2]'
    if D == 1:
        return MCQ(r, stem.replace('State', 'What is').rstrip('.') + '?', val, [str(c + 1), str(c - 1), str(c + 32 if up else c - 32)], key.replace(' [2]', ''))
    return Q(stem, val, key, marks=2)


@t1_3.add('C3', (2, 3, 4, 5), 'numerical')
def t1_3_size(r, D):
    n = r.choice([200, 250, 400, 500, 800, 1000, 1200, 1500, 2000, 2500, 4000, 5000])
    enc = r.choice([('extended ASCII', 1), ('a 16-bit Unicode encoding', 2), ('a 32-bit Unicode encoding', 4)])
    other = r.choice([e for e in [('extended ASCII', 1), ('a 16-bit Unicode encoding', 2), ('a 32-bit Unicode encoding', 4)] if e != enc])
    d = ctx(r)
    s1, s2 = n * enc[1], n * other[1]
    stem = f'{d["p"]} writes a message of {n} characters. Calculate the storage needed in bytes using {enc[0]}, and the extra storage needed if {other[0]} is used instead.'
    diff = s2 - s1
    ans = f'{s1} bytes; {"extra" if diff > 0 else "saving of"} {abs(diff)} bytes'
    key = f'{n} × {enc[1]} = {s1} bytes [1]; {n} × {other[1]} = {s2} bytes [1]; difference {abs(diff)} bytes ({"more" if diff > 0 else "less"}) [1] [3]'
    return Q(stem, ans, key, marks=3)


@t1_3.add('C3', (2, 3, 4))
def t1_3_decode(r, D):
    words = ['CODE', 'BYTE', 'DATA', 'LOOP', 'GATE', 'NODE', 'HASH', 'FILE', 'TREE', 'STACK', 'QUEUE', 'ARRAY', 'PIXEL', 'CACHE', 'LOGIC']
    w = r.choice(words) if D < 4 else r.choice(words).lower()
    fmt_ = r.choice(['denary', 'binary', 'hexadecimal'])
    cs = [str(ord(c)) if fmt_ == 'denary' else (b(ord(c)) if fmt_ == 'binary' else hx(ord(c))) for c in w]
    stem = f'Using ASCII, where "A" is 65 and "a" is 97 in denary, decode the {fmt_} character codes {", ".join(cs)}.'
    return Q(stem, w, ' '.join(f'{x} = {ord(c)} = {c}' for x, c in zip(cs, w)) + f' [{min(3, len(w) - 1)}]')


ar(t1_3, [('Unicode can represent characters from many different languages.', 'Unicode uses more bits per character than ASCII, giving many more unique codes.'),
          ('Upper-case letters are sorted before lower-case letters when character codes are compared.', 'The ASCII codes for upper-case letters (65–90) are smaller than those for lower-case letters (97–122).'),
          ('Standard ASCII can represent 128 characters.', 'Standard ASCII uses a 7-bit code and 2⁷ = 128.'),
          ('A text file saved in a 32-bit Unicode encoding is four times the size of the extended ASCII version.', 'Each character uses 4 bytes instead of 1 byte.')],
   ['ASCII uses 16 bits for each character.', 'Unicode can only represent the English alphabet.', 'The character "9" has the ASCII code 9.', 'Extended ASCII represents 65 536 characters.'])


scen(t1_3, 'C4', (2, 3, 4, 5), [
    '{org} in {city} is developing a messaging app that will be used by customers in several countries.',
    '{p} is designing a text-processing program that stores messages typed by users around the world.',
], [('Explain why the app should use Unicode rather than ASCII.', 'Users write in many scripts; ASCII has only 128/256 codes, Unicode covers all languages and emoji.', '1 mark: many languages; 1 mark: ASCII too few codes [2]'),
    lambda r, d: (f'A message contains {(n := r.choice([120, 160, 240, 300]))} characters. Calculate its size in bytes if each character is stored in 16 bits.', f'{2 * n} bytes', f'{n} × 2 bytes = {2 * n} bytes [2]'),
    ('Describe one drawback of using Unicode.', 'Files and messages need more storage and take longer to transmit than with ASCII.', '1 mark: larger file/more bandwidth; 1 mark: developed (more bits per character) [2]'),
    lambda r, d: (f'The letter "{(c := chr(r.randrange(66, 90)))}" has ASCII code {ord(c)}. Give the code for "{c.lower()}" in 8-bit binary and explain your method.', b(ord(c) + 32), f'Add 32 (lower case is 32 more): {ord(c) + 32} [1] = {b(ord(c) + 32)} [1] [2]')], k=(3, 4))

# ----------------------------------------------------------------------------- 1.4 graphics
t1_4 = topic('Bitmap and vector graphics: resolution, colour depth and file size calculations', 'bitmap and vector graphics', 'colour depth', 'file size calculations')
t1_4.fixed('C1', (1, 2), [
    ('What is meant by the colour depth of a bitmap image?', 'The number of bits used to represent the colour of each pixel', 'Colour depth = bits per pixel; n bits give 2ⁿ colours.',
     ['The number of pixels in the image', 'The number of pixels per inch', 'The number of colours in the palette divided by 8']),
    ('How many different colours can be represented with a colour depth of 8 bits?', '256', '2⁸ = 256.', ['8', '16', '512']),
    ('What is a pixel?', 'The smallest addressable element of a bitmap image', 'Pixel = picture element, the smallest unit of a bitmap that can be given a colour.', ['A drawing object in a vector graphic', 'A unit of storage of 8 bits', 'The header of an image file']),
    ('What does a vector graphic store?', 'A drawing list of objects and their properties', 'Vector graphics store objects (lines, circles, polygons) with properties such as coordinates, line colour and fill colour.',
     ['The colour of each pixel', 'A compressed list of pixel colours', 'Only the image resolution']),
    ('What is meant by the image resolution of a bitmap?', 'The number of pixels in the image, given as width × height', 'Image resolution = total pixels (width × height); screen resolution is the number of pixels a display can show.',
     ['The number of bits per pixel', 'The number of colours used', 'The file size in bytes']),
    ('What is stored in the file header of a bitmap image?', 'Data such as image width, height and colour depth', 'File header holds metadata: dimensions, colour depth, file type, compression used.',
     ['The colour of the first pixel only', 'The drawing list', 'The password for the file']),
])
t1_4.fixed('C2', (2, 3, 4), [
    ('Explain why a vector graphic can be enlarged without losing quality but a bitmap cannot.', 'A vector graphic is redrawn from its mathematical object properties at the new size; a bitmap has a fixed number of pixels which are enlarged, causing pixelation.',
     '1 mark: vector objects recalculated/redrawn; 1 mark: bitmap pixels stretched, image becomes pixelated [2]'),
    ('Explain why a photograph is normally stored as a bitmap rather than a vector graphic.', 'A photograph has continuous variation in colour and detail that cannot be described by simple shapes; a bitmap records the colour of every pixel.',
     '1 mark: complex/continuous colour detail; 1 mark: cannot be broken into geometric objects / bitmap stores each pixel [2]'),
    ('Explain the effect on file size of increasing the colour depth of a bitmap image.', 'More bits are stored per pixel, so the file size increases in proportion (e.g. 8 to 16 bits doubles it), but more colours can be shown.',
     '1 mark: more bits per pixel; 1 mark: file size increases proportionally [2]'),
    ('Describe two properties that would be stored in the drawing list for a circle in a vector graphic.', 'Centre coordinates, radius, line colour, line thickness, fill colour.', '1 mark per property, max 2 [2]'),
])


def _img(r, D):
    w = r.choice([64, 128, 256, 320, 512, 640, 800, 1024, 1280, 1600, 2048])
    h = r.choice([64, 128, 256, 480, 512, 600, 768, 1024, 1200])
    depth = r.choice([1, 4, 8, 16, 24, 32]) if D >= 3 else r.choice([1, 8, 16, 24])
    return w, h, depth


@t1_4.add('C3', (1, 2, 3, 4, 5))
def t1_4_size(r, D):
    w, h, depth = _img(r, D)
    bits = w * h * depth
    by = bits // 8
    unit = 'KiB' if D <= 3 else r.choice(['KiB', 'MiB'])
    div = 1024 if unit == 'KiB' else 1048576
    val = by / div
    vs = (str(int(val)) if val == int(val) else f'{val:.2f}')
    d = ctx(r)
    stem = f'{d["p"]} creates a bitmap image of {w} × {h} pixels with a colour depth of {depth} bits. Calculate the file size in {unit}' + (', ignoring the file header' if D >= 2 else '') + '.'
    key = f'{w} × {h} × {depth} = {bits:,} bits [1]; ÷ 8 = {by:,} bytes [1]; ÷ {div:,} = {vs} {unit} [1] [3]'
    if D == 1:
        dis = [f'{by:,} {unit}', f'{(str(int(val * 8)) if val * 8 == int(val * 8) else f"{val * 8:.2f}")} {unit}', f'{(str(int(val / 8)) if val / 8 == int(val / 8) else f"{val / 8:.2f}")} {unit}', f'{bits:,} {unit}']
        return MCQ(r, stem.replace('Calculate', 'What is'), f'{vs} {unit}', dis, key.replace(' [3]', ''))
    return Q(stem, f'{vs} {unit}', key, marks=3)


@t1_4.add('C3', (1, 2, 3))
def t1_4_colours(r, D):
    if r.random() < 0.5:
        n = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 16, 24])
        stem, ans, key = f'How many different colours can be represented with a colour depth of {n} bits?', f'{1 << n:,}', f'2^{n} = {1 << n:,} [1]'
        dis = [f'{n * n}', f'{2 * n}', f'{(1 << n) - 1:,}', f'{1 << (n + 1):,}']
    else:
        c = r.choice([5, 12, 20, 30, 50, 100, 200, 300, 500, 1000, 3000])
        n = math.ceil(math.log2(c))
        stem, ans, key = f'An image uses {c} different colours. State the minimum colour depth needed.', f'{n} bits', f'2^{n - 1} = {1 << (n - 1)} < {c} ≤ 2^{n} = {1 << n}, so {n} bits [1]'
        dis = [f'{n - 1} bits', f'{n + 1} bits', f'{c} bits', f'{c // 8} bits']
    if D <= 2:
        return MCQ(r, stem.replace('State', 'What is'), ans, dis, key)
    return Q(stem, ans, key)


@t1_4.add('C3', (3, 4, 5), 'numerical')
def t1_4_change(r, D):
    w, h, depth = _img(r, D)
    f1 = r.choice([2, 3])
    nd = r.choice([x for x in [1, 4, 8, 16, 24, 32] if x != depth])
    old = w * h * depth
    new = (w * f1) * (h * f1) * nd
    ratio = new / old
    rs = str(int(ratio)) if ratio == int(ratio) else f'{ratio:.3g}'
    stem = f'A {w} × {h} bitmap has colour depth {depth} bits. Its width and height are both multiplied by {f1} and the colour depth is changed to {nd} bits. Calculate how many times larger the new file is, and the new file size in bytes.'
    return Q(stem, f'{rs} times; {new // 8:,} bytes', f'pixels × {f1 * f1} [1]; bits per pixel × {nd}/{depth} [1]; overall ×{rs} [1]; {w * f1} × {h * f1} × {nd} ÷ 8 = {new // 8:,} bytes [1] [4]', marks=4)


scen(t1_4, 'C4', (2, 3, 4, 5), [
    '{org} in {city} is creating images for its website and printed brochures.',
    '{p} is designing a logo and taking photographs for {org}.',
], [lambda r, d: (f'A photograph is {(w := r.choice([800, 1024, 1280]))} × {(h := r.choice([600, 768, 1024]))} pixels with 24-bit colour. Calculate its size in KiB.', f'{w * h * 3 // 1024:,} KiB' if w * h * 3 % 1024 == 0 else f'{w * h * 3 / 1024:.1f} KiB', f'{w} × {h} × 24 ÷ 8 = {w * h * 3:,} bytes [1]; ÷ 1024 [1] [2]'),
    ('Explain why the logo should be stored as a vector graphic.', 'It can be scaled to any size for web and print without losing quality and has a small file size.', '1 mark: scalable without pixelation; 1 mark: small file / easily edited [2]'),
    ('Explain why reducing the colour depth of the photographs would reduce download times, and one drawback.', 'Fewer bits per pixel means a smaller file and less data to transmit; but fewer colours so lower quality/banding.', '1 mark: smaller file; 1 mark: drawback (fewer colours/quality) [2]'),
    ('State two items of data stored in the file header of the bitmap.', 'Width and height (resolution), colour depth, file type, compression used.', '1 mark each, max 2 [2]')], k=(3, 4))

# ----------------------------------------------------------------------------- 1.5 sound and compression
t1_5 = topic('Sound representation, sampling rate and resolution; lossy and lossless compression including run-length encoding', 'sound representation', 'sampling rate', 'compression', 'run-length encoding')
t1_5.fixed('C1', (1, 2), [
    ('What is meant by the sampling rate of a sound recording?', 'The number of samples taken per second', 'Sampling rate is measured in hertz (samples per second).',
     ['The number of bits per sample', 'The length of the recording', 'The loudness of the sound']),
    ('What is meant by sampling resolution?', 'The number of bits used to store each sample', 'Sampling resolution (bit depth): bits per sample; more bits give more amplitude levels.',
     ['The number of samples per second', 'The frequency of the sound', 'The number of channels']),
    ('Which type of compression permanently removes data?', 'Lossy', 'Lossy compression discards data judged less important (e.g. sounds humans cannot hear); the original cannot be reconstructed.', ['Lossless', 'Run-length encoding', 'Huffman coding']),
    ('Which file type would normally use lossless compression?', 'A program source file', 'Text and program files must be restored exactly, so lossless compression is used.', ['A streamed film', 'A music track for a phone', 'A photograph for social media']),
    ('What does run-length encoding (RLE) replace?', 'A run of identical data values with the value and a count', 'RLE stores runs such as AAAAA as 5A.', ['Each character with a shorter code based on frequency', 'Sounds outside the hearing range', 'Every second pixel']),
    ('What is the effect of increasing the sampling rate?', 'The recording is more accurate but the file is larger', 'More samples per second → closer to the analogue wave, larger file.',
     ['The file becomes smaller', 'Each sample uses fewer bits', 'The sound becomes louder']),
])
t1_5.fixed('C2', (2, 3, 4), [
    ('Explain why a sound file recorded at a higher sampling resolution sounds more accurate.', 'More bits per sample give more possible amplitude levels, so each sample is closer to the true amplitude and quantisation error is smaller.',
     '1 mark: more amplitude levels/values; 1 mark: smaller rounding (quantisation) error / closer to original [2]'),
    ('Explain why run-length encoding is not effective for compressing a photograph.', 'Photographs have few runs of identical neighbouring pixel colours, so RLE pairs may make the file the same size or larger.',
     '1 mark: few runs of identical values; 1 mark: may increase file size [2]'),
    ('Explain how perceptual coding is used in lossy compression of music.', 'Sounds that humans cannot hear (outside the hearing range or masked by louder sounds) are removed, reducing file size with little noticeable loss.',
     '1 mark: removes sounds that cannot be heard / masked; 1 mark: reduced file size, little perceived quality loss [2]'),
    ('Explain why lossless compression must be used for a spreadsheet file.', 'All data must be restored exactly; losing any values or characters would corrupt the data/formulae.', '1 mark: file must be reconstructed exactly; 1 mark: any loss would change the data/make it unusable [2]'),
    ('Explain the difference between lossy and lossless compression.', 'Lossless reduces file size without permanent data loss, so the original can be restored exactly; lossy permanently removes some data so the original cannot be restored.',
     '1 mark: lossless — no data lost/original restored; 1 mark: lossy — data permanently removed [2]'),
])


@t1_5.add('C3', (1, 2, 3, 4, 5))
def t1_5_size(r, D):
    rate = r.choice([8000, 16000, 20000, 32000, 40000, 48000])
    res = r.choice([8, 16, 24])
    secs = r.choice([5, 10, 15, 20, 30, 45, 60, 90, 120])
    ch = 1 if D <= 2 else r.choice([1, 2])
    by = rate * res * secs * ch // 8
    unit = 'bytes' if D <= 2 else 'MB'
    val = f'{by:,} bytes' if unit == 'bytes' else (f'{by / 1e6:g} MB')
    d = ctx(r)
    stem = (f'{d["p"]} records a {"stereo (2-channel)" if ch == 2 else "mono"} sound clip lasting {secs} seconds at a sampling rate of {rate // 1000} kHz and a sampling resolution of {res} bits. '
            f'Calculate the file size in {unit}' + (' (1 MB = 1 000 000 bytes)' if unit == 'MB' else '') + '.')
    key = f'{rate} × {res} × {secs}' + (' × 2' if ch == 2 else '') + f' = {by * 8:,} bits [1]; ÷ 8 = {by:,} bytes [1]' + (f'; ÷ 1 000 000 = {by / 1e6:g} MB [1] [3]' if unit == 'MB' else ' [2]')
    if D == 1:
        return MCQ(r, stem.replace('Calculate', 'What is'), val, [f'{by * 8:,} bytes', f'{by // 2:,} bytes', f'{by * 2:,} bytes'], key.replace(' [2]', ''))
    return Q(stem, val, key, marks=3 if unit == 'MB' else 2)


def _runs(s):
    out = []
    for c in s:
        if out and out[-1][1] == c:
            out[-1][0] += 1
        else:
            out.append([1, c])
    return out


@t1_5.add('C3', (1, 2, 3, 4))
def t1_5_rle(r, D):
    alph = r.choice(['ABC', 'WB', 'RGB', 'XYZ', 'PQ'])
    n = r.randrange(4, 7) if D <= 2 else r.randrange(6, 9)
    s = ''.join(r.choice(alph) * r.randrange(1, 7) for _ in range(n))
    runs = _runs(s)
    enc = ' '.join(f'{k}{c}' for k, c in runs)
    if r.random() < 0.5:
        stem = f'Use run-length encoding to compress the string {s}. Give each run as a count followed by the character.'
        ans, key = enc, f'Runs: {enc} [2]'
        dis = [' '.join(f'{c}{k}' for k, c in runs), ' '.join(f'{k}{c}' for k, c in runs[:-1]), ' '.join(f'{k + 1}{c}' for k, c in runs)]
    else:
        stem = f'The run-length encoded data {enc} represents a row of characters (count then character). Write out the original string and state its length.'
        ans, key = f'{s} ({len(s)} characters)', f'Expand each pair: {s} [1]; length {len(s)} [1] [2]'
        dis = [f'{s[:-1]} ({len(s) - 1} characters)', f'{"".join(c for _, c in runs)} ({len(runs)} characters)', f'{s}{s[-1]} ({len(s) + 1} characters)']
    if D == 1:
        return MCQ(r, stem, ans, dis, key.replace(' [2]', ''))
    if D >= 3:
        saved = len(s) - 2 * len(runs)
        stem += ' Calculate how many bytes are saved if each character and each count is stored in one byte.'
        ans += f'; {saved} bytes saved' if saved >= 0 else f'; the encoded form is {-saved} bytes larger'
        key = key.replace(' [2]', '') + f'; original {len(s)} bytes, encoded {2 * len(runs)} bytes, difference {saved} [1] [3]'
        return Q(stem, ans, key, marks=3)
    return Q(stem, ans, key, marks=2)


@t1_5.add('C4', (3, 4, 5), 'multi_step')
def t1_5_stream(r, D):
    rate, res, mins = r.choice([40000, 48000]), 16, r.choice([2, 3, 4, 5])
    by = rate * res * 60 * mins * 2 // 8
    ratio = r.choice([4, 5, 8, 10])
    d = ctx(r)
    stem = (f'A music streaming company in {d["city"]} sells tracks online. A {mins}-minute stereo track is recorded at {rate // 1000} kHz with 16-bit resolution. '
            f'(a) Calculate the uncompressed file size in MB (1 MB = 1 000 000 bytes). (b) A lossy codec reduces the file to 1/{ratio} of its size; give the new size. '
            f'(c) Explain why lossy compression is acceptable for this music but would not be acceptable for the company\'s customer records.')
    ans = f'(a) {by / 1e6:g} MB (b) {by / ratio / 1e6:g} MB (c) Lost sound data is mostly inaudible (perceptual coding) so quality is acceptable; customer records must be restored exactly so need lossless.'
    key = (f'(a) {rate} × 16 × {60 * mins} × 2 = {by * 8:,} bits; ÷ 8 = {by:,} bytes = {by / 1e6:g} MB [2] (b) {by / 1e6:g} ÷ {ratio} = {by / ratio / 1e6:g} MB [1] '
           f'(c) inaudible sounds removed / slight quality loss acceptable; data files must be exact, any loss corrupts data [2]')
    return Q(stem, ans, key, marks=5, typ='multi_step')


scen(t1_5, 'C4', (2, 3, 4), [
    '{p} records podcasts for {org} and needs to upload them quickly.',
    'A radio station in {city} archives its interviews as digital sound files.',
], [('Describe how analogue sound is converted into a digital sound file.', 'The amplitude of the sound wave is measured (sampled) at regular intervals and each sample is stored as a binary number using an ADC.', '1 mark: sampled at regular intervals; 1 mark: amplitude stored as binary; 1 mark: ADC [3]'),
    ('Explain the effect of halving the sampling rate on the file and on the quality.', 'File size halves; fewer samples so the recording is less accurate and high frequencies are lost.', '1 mark: file size halves; 1 mark: lower quality / less accurate [2]'),
    ('Recommend, with a reason, whether lossy or lossless compression should be used for the archive.', 'Lossless, so that the original recording is preserved exactly for future use (or lossy if storage is very limited, accepting some loss).', '1 mark: choice; 1 mark: justification [2]'),
    ('Give one reason why sampled sound can never be an exact copy of the original analogue sound.', 'The amplitude between samples is not recorded and each sample is rounded to the nearest level.', '1 mark [1]')], k=(2, 3))

CHAPTERS[1] = [t1_1, t1_2, t1_3, t1_4, t1_5]

# =============================================================================== Chapter 2 Communication
t2_1 = topic('Networks: LAN and WAN, client–server and peer-to-peer models, thin and thick clients', 'networks: lan and wan', 'client–server', 'peer-to-peer', 'thin and thick clients')
t2_1.fixed('C1', (1, 2), [
    ('What is a LAN?', 'A network covering a small geographical area such as one building or site', 'LAN = local area network: small area, infrastructure usually owned by the organisation.',
     ['A network covering a country or the world', 'A network that only uses wireless connections', 'A single computer connected to the internet']),
    ('Which is the best example of a WAN?', 'The internet', 'A WAN connects networks over a large geographical area, often using leased telecommunication lines.', ['A school computer room', 'Two laptops sharing a printer at home', 'A Bluetooth headset and phone']),
    ('In a client–server network, what does the server do?', 'Provides services or resources to client computers', 'Servers provide centralised services (files, printing, email, web pages); clients request them.',
     ['Requests services from every client', 'Acts only as a wireless access point', 'Stores no data']),
    ('What is a thin client?', 'A device that relies heavily on a server for processing and storage', 'Thin client: minimal local processing/storage; depends on a server/network connection.',
     ['A device that can carry out all processing without a server', 'A very lightweight laptop', 'A server with a small hard disk']),
    ('In a peer-to-peer network, which statement is true?', 'Each computer can act as both client and server', 'P2P: no central server; peers share resources directly with equal status.',
     ['All files are stored on one central server', 'Only one computer can print', 'Peers must be connected by a WAN']),
    ('State one characteristic of a thick client.', 'It can carry out most processing and store data locally, and can work without a constant server connection.', '1 mark: own processing/storage/can run offline [1]'),
])
t2_1.fixed('C2', (2, 3, 4), [
    ('Explain two advantages of a client–server network over a peer-to-peer network for an organisation.', 'Centralised security and access control; centralised backups; files stored in one place so easier to manage; better performance for large numbers of users.',
     '1 mark per advantage with explanation, max 2 points × 1 + 1 expansion [3]'),
    ('Explain why a small home office might choose a peer-to-peer network.', 'It is cheap to set up with no dedicated server or specialist staff; easy to share a printer and files among a few computers.',
     '1 mark: no server needed / low cost; 1 mark: simple to set up for few users [2]'),
    ('Explain one disadvantage of using thin clients.', 'They depend completely on the server and network; if the server or connection fails, the clients cannot work. A powerful server and good bandwidth are needed.',
     '1 mark: dependent on server/network; 1 mark: consequence (cannot work if it fails / needs high bandwidth) [2]'),
    ('Explain the difference between a LAN and a WAN in terms of area and ownership of infrastructure.', 'A LAN covers a small area and its cables/devices are owned by the organisation; a WAN covers a large area and usually uses infrastructure leased from telecommunications companies.',
     '1 mark: area; 1 mark: ownership [2]'),
])
scen(t2_1, 'C3', (1, 2, 3, 4), [
    '{org} in {city} has 40 staff who share files, printers and an internet connection in one building.',
    '{p} runs a design business from home with three computers and one printer.',
    '{org} has offices in {city} and two other cities and wants all offices to share one customer database.',
    'A school wants pupils to log in from any computer and see their own files.',
], [('State whether this situation needs a LAN or a WAN, giving a reason.', 'LAN if a single site; WAN if several sites in different cities must be connected.', '1 mark: correct choice; 1 mark: reason linked to geographical area [2]'),
    ('Recommend either a client–server or a peer-to-peer model, with a justification.', 'Client–server for many users needing central security/backups; peer-to-peer for a few computers with low budget.', '1 mark: model; 2 marks: justification linked to scenario [3]'),
    ('Identify two services a server could provide here.', 'File server, print server, email server, web server, authentication/login server.', '1 mark each, max 2 [2]'),
    ('Suggest whether thin or thick clients would be more suitable, and why.', 'Thin clients if a reliable server and network exist and central management is wanted; thick clients if users need to work offline or run demanding software.', '1 mark: choice; 1 mark: reason [2]')], k=(2, 3))
scen(t2_1, 'C4', (2, 3, 4, 5), [
    '{org} is moving from five separate offices in {city} into one new building and will also open a branch abroad.',
    'The managers of {org} want to replace a peer-to-peer network that has grown to 60 computers.',
], [('Explain why the peer-to-peer model becomes unsuitable as the network grows.', 'No central security or backups; files spread over many machines; performance falls when peers serve many requests; hard to manage.', '1 mark per point, max 3 [3]'),
    ('Describe how a client–server model would improve security.', 'Central user accounts and access rights on the server; central firewall and anti-malware; centralised backups.', '1 mark per point, max 2 [2]'),
    ('Explain why a WAN is needed to connect the branch abroad.', 'The branch is far away; a WAN uses public/leased telecommunications infrastructure to connect separate LANs.', '1 mark: distance; 1 mark: leased/public infrastructure links LANs [2]'),
    ('Evaluate the use of thin clients for the office staff.', 'Lower cost per device and central management/updates; but dependency on server and network, and high bandwidth needed.', '1 mark advantage, 1 mark disadvantage, 1 mark conclusion [3]')], k=(3, 4))

t2_2 = topic('Network topologies (bus, star, mesh, hybrid) and cloud computing', 'network topologies', 'cloud computing', 'bus star mesh')
t2_2.fixed('C1', (1, 2), [
    ('In which topology are all devices connected to a single central cable?', 'Bus', 'Bus: one backbone cable with terminators at both ends.', ['Star', 'Mesh', 'Ring']),
    ('In a star topology, what device is usually at the centre?', 'A switch', 'Each device has its own cable to a central switch (or hub).', ['A router at each end', 'A terminator', 'A repeater on every device']),
    ('Which topology gives each device a connection to every other device?', 'Full mesh', 'Full mesh: every node links directly to every other node.', ['Bus', 'Star', 'Hybrid']),
    ('What is a hybrid topology?', 'A network made by combining two or more different topologies', 'e.g. several star networks joined by a bus backbone.', ['A network with wireless and wired devices', 'A network with exactly two computers', 'A topology without any cables']),
    ('What is meant by public cloud?', 'Cloud services provided by a third party over the internet and shared by many customers', 'Public cloud: provider owns infrastructure, shared; private cloud: dedicated to one organisation.',
     ['Cloud storage that belongs to one organisation only', 'A LAN inside a school', 'Software installed on a local hard disk']),
    ('Which is an advantage of cloud computing?', 'Data can be accessed from anywhere with an internet connection', 'Access anywhere; no need to buy/maintain own servers; scalable.', ['It works without an internet connection', 'The user keeps full physical control of the hardware', 'Data is never stored on a third-party server']),
])
t2_2.fixed('C2', (2, 3, 4), [
    ('Explain why a failure of one cable in a star topology does not stop the rest of the network working.', 'Each device has its own cable to the switch; only the device on the broken cable loses its connection.',
     '1 mark: separate cable per device; 1 mark: only that device affected [2]'),
    ('Explain one disadvantage of a bus topology.', 'If the main cable fails the whole network stops; performance falls with many devices because only one can transmit at once (collisions).',
     '1 mark: single point of failure / collisions; 1 mark: explanation [2]'),
    ('Explain why a mesh topology is used for the internet backbone.', 'There are many alternative routes, so if one link fails data can be re-routed; it is fault-tolerant.',
     '1 mark: multiple routes; 1 mark: reliability/fault tolerance [2]'),
    ('Explain two concerns a company might have before moving its data to a public cloud.', 'Security and privacy of data on third-party servers; loss of access if the internet or provider fails; dependence on the provider; legal issues about where data is stored.',
     '1 mark per concern with brief explanation, max 2 [2]'),
])


@t2_2.add('C3', (1, 2, 3, 4))
def t2_2_links(r, D):
    n = r.randrange(4, 13)
    kind = r.choice(['mesh', 'star', 'mesh2'])
    if kind == 'mesh':
        v = n * (n - 1) // 2
        stem = f'A network has {n} devices connected in a full mesh topology. Calculate the number of cables (links) needed.'
        key = f'Each pair is linked: n(n − 1)/2 = {n} × {n - 1} ÷ 2 = {v} [2]'
        dis = [n * (n - 1), n, n - 1, v + n]
    elif kind == 'star':
        v = n
        stem = f'A star network has {n} computers connected to a central switch. How many cables are needed, and how many does each computer use?'
        key = f'One cable per computer to the switch: {n} cables; each computer uses 1 [2]'
        dis = [n - 1, n * (n - 1) // 2, 2 * n]
        return MCQ(r, stem.replace(', and how many does each computer use?', '?'), str(v), [str(x) for x in dis], key) if D <= 2 else Q(stem, f'{n} cables; 1 each', key, marks=2)
    else:
        m = n + 1
        v = m * (m - 1) // 2 - n * (n - 1) // 2
        stem = f'A full mesh network of {n} routers has one more router added. Calculate how many extra links are needed.'
        key = f'{m}×{m - 1}/2 − {n}×{n - 1}/2 = {m * (m - 1) // 2} − {n * (n - 1) // 2} = {v} (the new router links to all {n} existing ones) [2]'
        dis = [1, n + 1, m * (m - 1) // 2]
    if D <= 2:
        return MCQ(r, stem.replace('Calculate the number', 'How many').replace(' needed.', ' are needed?').replace('Calculate how many', 'How many'), str(v), [str(x) for x in dis], key)
    return Q(stem, str(v), key, marks=2)


scen(t2_2, 'C3', (2, 3, 4), [
    '{org} in {city} is designing a new network for a building with 30 computers and is considering moving its file storage to the cloud.',
    '{p} is advising {org} on a new office network and on whether to move file storage and email to the cloud.',
    'A hospital in {city} needs a network where a single cable fault will not cut off patient monitoring, and is considering cloud storage for records.',
], [('Recommend a topology and justify your choice.', 'Star: a single cable failure only affects one device; easy to add devices; switch reduces collisions (or mesh for critical reliability).', '1 mark: topology; 2 marks: justification [3]'),
    ('Describe one benefit and one drawback of private cloud compared with public cloud for this organisation.', 'Private: more control and security; but expensive to buy and maintain.', '1 mark benefit; 1 mark drawback [2]'),
    ('Explain how a hybrid topology could be used if the organisation has several floors.', 'A star network on each floor, linked by a bus or mesh backbone between floor switches.', '1 mark: combination; 1 mark: description [2]'),
    ('Give two advantages of cloud storage for the staff.', 'Access from anywhere; automatic backups by provider; no hardware to maintain; scalable storage.', '1 mark each, max 2 [2]')], k=(2, 3))
essay(t2_2, [
    ('whether {org} should move all of its data and software to a public cloud', 'access from any location; no need to buy servers; provider handles backups and maintenance; scalable pay-as-you-go cost.',
     'security/privacy risk of third-party storage; reliance on internet connection and provider; ongoing subscription costs; legal issues about data location.', 'a hybrid or careful contract may give the benefits while controlling risks.'),
    ('the choice of star topology instead of bus topology for the new network at {org}', 'cable failure affects only one device; switch sends data only to the intended device so fewer collisions; easy to add devices.',
     'more cable and a switch are needed so higher cost; the switch is a single point of failure.', 'star is usually preferred because reliability and performance outweigh the cost.'),
], ['{org} is reviewing its IT infrastructure in {city}.', '{p} has been asked to write a report for the managers of {org}.'])

t2_3 = topic('Wired and wireless transmission media; Ethernet, CSMA/CD and network hardware (switch, router, NIC, WAP)', 'transmission media', 'ethernet', 'csma/cd', 'network hardware')
t2_3.fixed('C1', (1, 2), [
    ('Which device connects a LAN to the internet and forwards packets between networks?', 'Router', 'A router forwards packets between different networks using IP addresses.', ['Switch', 'Network interface card', 'Repeater']),
    ('Which device sends a frame only to the device with the matching MAC address within a LAN?', 'Switch', 'A switch uses a table of MAC addresses to forward frames only to the destination port.', ['Hub', 'Router', 'Wireless access point']),
    ('What does a NIC provide?', 'The hardware connection to a network and a unique MAC address', 'Network interface card: connects the device to the network; has a MAC address.', ['An IP address that never changes', 'Wireless internet for a whole building', 'Routing between networks']),
    ('What is the purpose of a wireless access point (WAP)?', 'To allow wireless devices to connect to a wired network', 'A WAP connects Wi-Fi devices to the wired LAN.', ['To encrypt all data on a hard disk', 'To translate domain names into IP addresses', 'To connect two WANs']),
    ('Which transmission medium is least affected by electromagnetic interference?', 'Fibre-optic cable', 'Fibre carries light, so it is immune to electrical interference and supports long distances at high bandwidth.', ['Twisted-pair cable', 'Coaxial cable', 'Radio waves']),
    ('What does CSMA/CD stand for?', 'Carrier Sense Multiple Access with Collision Detection', 'Used in (shared) Ethernet to detect and recover from collisions.', ['Central Server Multiple Access with Collision Delay', 'Carrier Signal Multiple Address with Cable Detection', 'Collision Sense Multiple Access with Carrier Detection']),
    ('What is a repeater used for?', 'To regenerate a signal so it can travel further', 'Repeaters boost/regenerate weakened signals over long cable runs.', ['To connect two different networks', 'To filter packets', 'To give each device an IP address']),
])
t2_3.fixed('C2', (2, 3, 4), [
    ('Describe how CSMA/CD works.', 'A device listens to check the channel is idle before transmitting; while transmitting it monitors for a collision; if a collision is detected it sends a jam signal and waits a random time before trying again.',
     '1 mark: listen/sense carrier before sending; 1 mark: collision detected (jam signal); 1 mark: random back-off and retry [3]'),
    ('Explain why fibre-optic cable is used for long-distance network links.', 'Very high bandwidth; little signal loss (attenuation) over long distances so fewer repeaters; not affected by electromagnetic interference.',
     '1 mark per point, max 2 [2]'),
    ('Compare wired and wireless networks in terms of speed and security.', 'Wired is usually faster and more reliable; wireless signals can be intercepted more easily so need strong encryption (WPA2/3) but give mobility.',
     '1 mark: speed comparison; 1 mark: security comparison [2]'),
    ('Explain the difference between a switch and a router.', 'A switch connects devices within one LAN and forwards frames by MAC address; a router connects different networks and forwards packets by IP address.',
     '1 mark: switch within LAN / MAC; 1 mark: router between networks / IP [2]'),
])


def _xfer(r, D):
    rate = r.choice([8, 10, 16, 20, 25, 40, 50, 80, 100, 200])
    secs = r.choice([2, 4, 5, 8, 10, 12, 15, 20, 30, 40, 60])
    mb = rate * secs / 8
    if mb != int(mb):
        return None
    return rate, secs, int(mb)


@t2_3.add('C3', (1, 2, 3, 4, 5))
def t2_3_time(r, D):
    x = _xfer(r, D)
    if not x:
        return None
    rate, secs, mb = x
    d = ctx(r)
    kind = r.choice(['time', 'size', 'rate']) if D >= 3 else 'time'
    if kind == 'time':
        stem = f'{d["p"]} downloads a {mb} MB file over a connection with a transfer rate of {rate} Mbps. Calculate the time taken, in seconds (1 MB = 8 megabits).'
        ans, key = f'{secs} s', f'{mb} MB × 8 = {mb * 8} megabits [1]; {mb * 8} ÷ {rate} = {secs} s [1] [2]'
        dis = [f'{mb / rate:g} s', f'{secs * 8} s', f'{rate * mb} s']
    elif kind == 'size':
        stem = f'A video stream at {rate} Mbps runs for {secs} seconds. Calculate the amount of data transferred in megabytes (1 byte = 8 bits).'
        ans, key = f'{mb} MB', f'{rate} × {secs} = {rate * secs} megabits [1]; ÷ 8 = {mb} MB [1] [2]'
        dis = [f'{rate * secs} MB', f'{rate * secs * 8} MB', f'{mb * 2} MB']
    else:
        stem = f'A {mb} MB file must be transmitted in {secs} seconds. Calculate the minimum transfer rate needed in Mbps (1 MB = 8 megabits).'
        ans, key = f'{rate} Mbps', f'{mb} × 8 = {mb * 8} megabits [1]; ÷ {secs} = {rate} Mbps [1] [2]'
        dis = [f'{mb / secs:g} Mbps', f'{rate * 8} Mbps', f'{mb * secs} Mbps']
    if D == 1:
        return MCQ(r, stem.replace('Calculate', 'What is'), ans, dis, key.replace(' [2]', ''))
    if D >= 4:
        over = r.choice([10, 20, 25])
        stem += f' In practice {over}% of the bandwidth is used by protocol overheads; state the effect on your answer.'
        ans += '; ' + ('takes longer: ' + f'{secs / (1 - over / 100):.3g} s' if kind == 'time' else 'less useful data / a higher rate is needed')
        key = key.replace(' [2]', '') + '; effective rate reduced so answer adjusted [1] [3]'
        return Q(stem, ans, key, marks=3)
    return Q(stem, ans, key, marks=2)


scen(t2_3, 'C4', (2, 3, 4, 5), [
    '{org} is installing a network in a new building in {city}. The building has a public Wi-Fi area for visitors and a workshop with heavy electrical machinery.',
    'A factory owned by {org} near {city} is being networked; it has a visitor Wi-Fi area and network cables must run past heavy electrical machinery.',
], [('Identify the hardware needed to connect the wireless devices to the wired network, and to connect the network to the internet.', 'Wireless access point(s); router (with switch for wired devices).', '1 mark WAP; 1 mark router [2]'),
    ('Recommend a cable type for the link near the machinery, with a reason.', 'Fibre-optic: immune to electromagnetic interference.', '1 mark choice; 1 mark reason [2]'),
    ('Explain why the switch improves performance compared with a hub.', 'A switch forwards frames only to the destination port (using MAC addresses) so there is less traffic and fewer collisions.', '1 mark: only to destination; 1 mark: less traffic/collisions [2]'),
    ('Describe the security measures needed for the visitor Wi-Fi.', 'Separate guest network (VLAN) isolated from staff data; WPA2/WPA3 encryption; password/login portal; firewall.', '1 mark per point, max 3 [3]'),
    _xfer and (lambda r, d: (lambda x: (f'Staff upload {x[2]} MB files over a {x[0]} Mbps link. Calculate the upload time in seconds.', f'{x[1]} s', f'{x[2]} × 8 = {x[2] * 8} Mb [1]; ÷ {x[0]} = {x[1]} s [1] [2]') if x else None)(_xfer(r, 3)))], k=(3, 4))

# ----------------------------------------------------------------------------- 2.4 IP addressing
t2_4 = topic('IP addressing: IPv4, IPv6, subnetting, public and private addresses, DNS and URLs', 'ip addressing', 'ipv4', 'ipv6', 'subnetting', 'dns')
t2_4.fixed('C1', (1, 2), [
    ('How many bits are in an IPv4 address?', '32', 'IPv4: 32 bits written as four denary octets.', ['64', '128', '48']),
    ('How many bits are in an IPv6 address?', '128', 'IPv6: 128 bits as eight groups of four hex digits.', ['32', '64', '256']),
    ('What is the role of a DNS server?', 'To translate a domain name into an IP address', 'DNS resolves URLs/domain names (e.g. www.example.com) to IP addresses.', ['To assign MAC addresses', 'To encrypt web pages', 'To store web pages']),
    ('Which of these is a private IPv4 address?', '192.168.4.20', 'Private ranges: 10.0.0.0/8, 172.16.0.0–172.31.255.255, 192.168.0.0/16.', ['8.8.8.8', '172.40.1.2', '200.10.5.1']),
    ('What is a static IP address?', 'An address that does not change each time a device connects', 'Static: fixed, set manually; dynamic: assigned (by DHCP) and may change.', ['An address that changes every time a device connects', 'An address used only by printers', 'An IPv6 address']),
    ('Why was IPv6 introduced?', 'IPv4 addresses were running out', 'IPv4 gives about 4.3 billion addresses; IPv6 gives 2¹²⁸.', ['IPv4 could not be used on wireless networks', 'IPv6 addresses are shorter', 'IPv4 does not work with DNS']),
    ('In the URL https://www.example.org/news/index.html, what is "www.example.org"?', 'The domain name', 'Protocol https; domain name www.example.org; path /news/index.html.', ['The protocol', 'The file name', 'The IP address']),
])
t2_4.fixed('C2', (2, 3, 4), [
    ('Explain why private IP addresses can be reused in many different LANs.', 'Private addresses are not routed on the internet; the router uses NAT to share one public address, so the same private range can exist in every LAN.',
     '1 mark: private addresses not routable on internet; 1 mark: NAT/router translates to public address [2]'),
    ('Explain why subnetting is used in a large network.', 'It divides the network into smaller sub-networks, reducing broadcast traffic, improving security (separating departments) and making management easier.',
     '1 mark per benefit, max 2 [2]'),
    ('Describe the steps taken when a browser uses DNS to find a web page.', 'Browser sends the domain name to a DNS server; if found, the IP address is returned; if not, the request is passed up to other DNS servers; the browser then sends the request to the IP address.',
     '1 mark: domain sent to DNS server; 1 mark: lookup/forwarded to other DNS servers; 1 mark: IP returned and used to contact web server [3]'),
    ('Explain one reason an organisation might give its web server a static IP address.', 'The DNS record points to a fixed address so users can always find the server; dynamic addresses could change and break the link.',
     '1 mark: address must not change; 1 mark: so DNS/users can always locate it [2]'),
])


def _ip(r):
    return [r.randrange(1, 224), r.randrange(256), r.randrange(256), r.randrange(1, 255)]


def _ipv6(r, D):
    groups = [r.randrange(1, 0x10000) for _ in range(8)]
    start = r.randrange(1, 6)
    ln = r.randrange(2, 5) if D >= 3 else 2
    for i in range(start, min(8, start + ln)):
        groups[i] = 0
    for i in range(8):
        if groups[i] and r.random() < 0.4:
            groups[i] = r.randrange(1, 0x100)
    full = ':'.join(format(g, '04x') for g in groups)
    # shorthand: drop leading zeros, replace longest run (>=2) of zero groups (first if tie)
    best, cur = (0, -1), None
    for i, g in enumerate(groups + [1]):
        if i < 8 and g == 0:
            cur = cur if cur is not None else i
        else:
            if cur is not None and i - cur > best[0]:
                best = (i - cur, cur)
            cur = None
    parts = [format(g, 'x') for g in groups]
    if best[0] >= 2:
        s, e = best[1], best[1] + best[0]
        short = ':'.join(parts[:s]) + '::' + ':'.join(parts[e:])
    else:
        short = ':'.join(parts)
    return full, short


@t2_4.add('C3', (1, 2, 3, 4, 5))
def t2_4_ip(r, D):
    kind = r.choice(['bin', 'hosts', 'netaddr', 'v6', 'private']) if D >= 2 else r.choice(['bin', 'hosts', 'private'])
    if kind == 'bin':
        ip = _ip(r)
        i = r.randrange(4)
        stem = f'The IPv4 address {".".join(map(str, ip))} is stored in binary. Give octet {i + 1} ({ip[i]}) as 8-bit binary.'
        return MCQ(r, stem.replace('Give', 'What is').replace(' as 8-bit binary.', ' in 8-bit binary?'), b(ip[i]), [b(ip[i] + 1), b(ip[i])[::-1] if b(ip[i])[::-1] != b(ip[i]) else b(ip[i] ^ 2), b((ip[i] + 128) % 256)], f'{ip[i]} = {b(ip[i])}') if D == 1 else \
            Q(stem, b(ip[i]), f'{ip[i]} = {b(ip[i])} [1]')
    if kind == 'hosts':
        pre = r.choice([24, 25, 26, 27, 28, 29, 30, 22, 23, 20])
        h = (1 << (32 - pre)) - 2
        mask = (0xFFFFFFFF << (32 - pre)) & 0xFFFFFFFF
        md = '.'.join(str((mask >> s) & 255) for s in (24, 16, 8, 0))
        stem = f'A subnet uses the prefix /{pre}. State the subnet mask in dotted denary and calculate the maximum number of hosts on the subnet.'
        key = f'{pre} ones then {32 - pre} zeros: {md} [1]; hosts = 2^{32 - pre} − 2 = {h} (network and broadcast addresses excluded) [1] [2]'
        if D == 1:
            return MCQ(r, f'How many usable host addresses are there on a /{pre} subnet?', str(h), [str(h + 2), str(1 << pre), str((h + 2) // 2)], key.replace(' [2]', ''))
        return Q(stem, f'{md}; {h} hosts', key, marks=2)
    if kind == 'netaddr':
        ip = _ip(r)
        pre = r.choice([24, 26, 27, 28]) if D < 4 else r.choice([20, 22, 26, 27, 28, 29])
        v = (ip[0] << 24) | (ip[1] << 16) | (ip[2] << 8) | ip[3]
        mask = (0xFFFFFFFF << (32 - pre)) & 0xFFFFFFFF
        net = v & mask
        bc = net | (~mask & 0xFFFFFFFF)
        dd = lambda x: '.'.join(str((x >> s) & 255) for s in (24, 16, 8, 0))
        stem = f'A computer has IP address {dd(v)} with subnet mask {dd(mask)}. Calculate the network address' + (' and the broadcast address of its subnet.' if D >= 4 else '.')
        ans = dd(net) + (f'; broadcast {dd(bc)}' if D >= 4 else '')
        key = f'AND the address with the mask bit by bit: network address {dd(net)} [2]' if D < 4 else f'AND with mask: {dd(net)} [2]; set host bits to 1: {dd(bc)} [1] [3]'
        return Q(stem, ans, key, marks=2 if D < 4 else 3)
    if kind == 'v6':
        full, short = _ipv6(r, D)
        stem = f'Write the IPv6 address {full} in its shortest valid form.'
        return Q(stem, short, f'Remove leading zeros in each group [1]; replace the longest run of consecutive zero groups with :: (once only) [1]: {short} [2]', marks=2)
    pool = [('10.' + '.'.join(str(r.randrange(256)) for _ in range(3)), 'private'), ('192.168.' + f'{r.randrange(256)}.{r.randrange(1, 255)}', 'private'),
            (f'172.{r.randrange(16, 32)}.{r.randrange(256)}.{r.randrange(1, 255)}', 'private'), (f'172.{r.randrange(32, 64)}.{r.randrange(256)}.{r.randrange(1, 255)}', 'public'),
            (f'{r.choice([8, 31, 52, 81, 104, 142, 185, 203])}.{r.randrange(256)}.{r.randrange(256)}.{r.randrange(1, 255)}', 'public'), (f'192.{r.choice([0, 100, 200, 169])}.{r.randrange(256)}.{r.randrange(1, 255)}', 'public')]
    a, kind2 = r.choice(pool)
    stem = f'State whether the IPv4 address {a} is public or private, giving a reason.'
    reason = 'it is in a reserved private range (10.0.0.0/8, 172.16.0.0–172.31.255.255 or 192.168.0.0/16)' if kind2 == 'private' else 'it is not in any of the private ranges (10.x.x.x, 172.16–31.x.x, 192.168.x.x)'
    if D == 1:
        return MCQ(r, f'Which description of the IPv4 address {a} is correct?', 'private' if kind2 == 'private' else 'public', ['private' if kind2 != 'private' else 'public', 'IPv6', 'loopback only'], f'{a} is {kind2}: {reason}.')
    return Q(stem, f'{kind2.capitalize()}: {reason}', f'1 mark: {kind2}; 1 mark: reason [2]', marks=2)


@t2_4.add('C2', (2, 3, 4), 'explain')
def t2_4_err(r, D):
    d = ctx(r)
    if r.random() < 0.5:
        l1, l2 = r.choice([(2, 2), (2, 3), (3, 2)])
        g = [r.randrange(0x100, 0x10000) for _ in range(8)]
        s1 = r.randrange(1, 8 - l1 - l2)
        s2 = r.randrange(s1 + l1 + 1, 8 - l2 + 1)
        for i in list(range(s1, s1 + l1)) + list(range(s2, s2 + l2)):
            g[i] = 0
        full = ':'.join(format(x, '04x') for x in g)
        p = [format(x, 'x') for x in g]
        wrong = ':'.join(p[:s1]) + '::' + ':'.join(p[s1 + l1:s2]) + '::' + ':'.join(p[s2 + l2:])
        if l2 > l1:
            short = ':'.join(p[:s2]) + '::' + ':'.join(p[s2 + l2:])
        else:
            short = ':'.join(p[:s1]) + '::' + ':'.join(p[s1 + l1:])
        stem = f'{d["p"]} shortens the IPv6 address {full} to {wrong}. Explain why this is not valid and give the correct shortest form.'
        return Q(stem, f'"::" may only appear once, otherwise it is impossible to tell how many zero groups each "::" replaces. Correct form: {short}.',
                 f'1 mark: :: used only once / ambiguity; 1 mark: longest zero run replaced, other written as 0 groups: {short} [2]')
    g = [r.randrange(0x1000, 0x10000) for _ in range(8)]
    i = r.randrange(8)
    g[i] = r.randrange(0x10, 0x100) * 0x100
    full = ':'.join(format(x, '04x') for x in g)
    p = [format(x, 'x') for x in g]
    wp = list(p)
    wp[i] = p[i].rstrip('0')
    wrong = ':'.join(wp)
    stem = f'{d["p"]} shortens the IPv6 address {full} to {wrong}. Explain the error and give the correct form.'
    return Q(stem, f'Only leading zeros in a group may be removed; trailing zeros are significant, so group {full.split(":")[i]} becomes {p[i]}, not {wp[i]}. Correct: {":".join(p)}.',
             f'1 mark: only leading zeros can be omitted; 1 mark: {":".join(p)} [2]')


scen(t2_4, 'C4', (2, 3, 4, 5), [
    '{org} in {city} has 200 computers on its LAN, divided into departments, and a public website hosted on its own server.',
    '{p} is the network manager of {org}, which has a LAN divided into departmental subnets and its own public web server.',
], [('Explain why the computers on the LAN can use private IP addresses.', 'They do not need to be reached directly from the internet; the router uses NAT with a public address.', '1 mark: not directly accessed from internet; 1 mark: NAT/router public address [2]'),
    ('Explain why the web server needs a public static IP address.', 'It must be reachable from the internet and DNS must always point to the same address.', '1 mark: public so reachable; 1 mark: static so DNS entry stays valid [2]'),
    lambda r, d: (lambda pre: (f'The network manager chooses a /{pre} subnet for each department. Calculate the maximum number of hosts per subnet.', str((1 << (32 - pre)) - 2), f'2^{32 - pre} − 2 = {(1 << (32 - pre)) - 2} [2]'))(r.choice([25, 26, 27, 28])),
    ('Describe how a user\'s browser finds the IP address of the company website.', 'Domain name sent to DNS resolver; looked up / passed up the DNS hierarchy; IP returned to browser which then connects.', '1 mark per step, max 3 [3]'),
    ('Give two benefits of IPv6 over IPv4.', 'Far more addresses (2¹²⁸); no need for NAT; simpler header/built-in security (IPsec), auto-configuration.', '1 mark each, max 2 [2]')], k=(3, 4))

CHAPTERS[2] = [t2_1, t2_2, t2_3, t2_4]

# =============================================================================== Chapter 3 Hardware
t3_1 = topic('Input, output and storage devices: laser printer, 3D printer, microphone, speakers, SSD, magnetic and optical storage', 'input, output and storage devices', 'laser printer', '3d printer', 'ssd')
t3_1.fixed('C1', (1, 2), [
    ('In a laser printer, what attracts the toner to the drum?', 'An electrostatic charge pattern created by the laser', 'The laser discharges areas of the charged drum; charged toner sticks to the pattern, is transferred to paper and fused by heat.',
     ['Magnetism from a print head', 'Heat from the fuser', 'Ink sprayed from nozzles']),
    ('Which storage device has no moving parts?', 'Solid-state drive (SSD)', 'SSDs use NAND flash memory (floating-gate transistors); no platters or read heads.', ['Hard disk drive', 'DVD drive', 'Magnetic tape']),
    ('How is data read from an optical disc?', 'A laser reflects off pits and lands on the disc surface', 'Changes between pits and lands alter the reflected light, which is detected as 1s and 0s.',
     ['A read head detects magnetic fields', 'Electrical charge in transistors is measured', 'A stylus touches the surface']),
    ('In a hard disk drive, what moves to position the read/write head over the correct track?', 'The actuator arm', 'Platters spin; the actuator arm moves the head across tracks; data stored as magnetised regions.', ['The spindle', 'The laser', 'The buffer']),
    ('Which device converts sound waves into an electrical signal?', 'Microphone', 'A microphone diaphragm vibrates, moving a coil in a magnetic field (or changing capacitance), producing a varying voltage.', ['Speaker', 'Actuator', '3D printer']),
    ('How does a 3D printer build an object?', 'By depositing material in thin layers, one on top of another', 'Additive manufacturing: layers of plastic/resin/metal built up from a digital model.', ['By cutting away material from a block', 'By pressing a mould', 'By projecting light onto paper']),
    ('What component in a speaker causes the cone to vibrate?', 'A coil in a magnetic field carrying a varying current', 'Varying current in the voice coil creates a changing magnetic field that interacts with the permanent magnet.', ['A laser', 'A piezoelectric crystal in all speakers', 'A spinning platter']),
])
t3_1.fixed('C2', (2, 3, 4), [
    ('Explain why an SSD is more suitable than a hard disk drive for a laptop.', 'No moving parts so more robust if dropped; faster access; lighter and uses less power, so better battery life.', '1 mark per point, max 3 [3]'),
    ('Describe how a laser printer produces a printed page.', 'The drum is given a charge; a laser removes charge where the image is not wanted (or creates the image pattern); toner is attracted to the charged areas; toner is transferred to charged paper; the fuser melts the toner onto the paper; the drum is discharged.',
     '1 mark per correct stage in sequence, max 4 [4]'),
    ('Explain why magnetic tape is still used for backups by large organisations.', 'Very high capacity at low cost per gigabyte; long-term reliable; backups are accessed sequentially so slow random access does not matter.', '1 mark per point, max 2 [2]'),
    ('Describe how a speaker produces sound from a digital file.', 'A DAC converts the digital data to an analogue signal; the varying current flows through the coil, creating a changing magnetic field; the coil and cone move in and out, creating sound waves.',
     '1 mark: DAC; 1 mark: current in coil/magnetic field; 1 mark: cone vibrates producing pressure waves [3]'),
    ('Explain why an SSD can wear out over time.', 'Flash memory cells can only be written/erased a limited number of times before they fail.', '1 mark: limited write/erase cycles; 1 mark: cells degrade [2]'),
])


@t3_1.add('C3', (1, 2, 3, 4))
def t3_1_cap(r, D):
    dev = r.choice([('a memory card', 'GB', 1000), ('an SSD', 'GB', 1000), ('a portable drive', 'TB', 1000000)])
    cap = r.choice([16, 32, 64, 128, 256, 512]) if dev[1] == 'GB' else r.choice([1, 2, 4])
    item = r.choice([('photographs', [2, 4, 5, 8, 10, 16, 20, 25]), ('songs', [4, 5, 8, 10]), ('videos', [200, 250, 400, 500, 800, 1000])])
    sz = r.choice(item[1])
    tot = cap * dev[2]
    n = tot // sz
    stem = f'{dev[0].capitalize()} has a capacity of {cap} {dev[1]}. Each of the {item[0]} to be stored is {sz} MB. Calculate how many {item[0]} can be stored (1 {dev[1]} = {dev[2]:,} MB).'
    key = f'{cap} × {dev[2]:,} = {tot:,} MB [1]; {tot:,} ÷ {sz} = {n:,} [1] [2]'
    if D == 1:
        return MCQ(r, stem.replace('Calculate how many', 'How many').replace(' can be stored (', ' can be stored? (').rstrip('.'), f'{n:,}', [f'{n * 8:,}', f'{n // 1000 or 1:,}', f'{tot * sz:,}', f'{n // 8:,}'], key.replace(' [2]', ''))
    return Q(stem, f'{n:,}', key, marks=2)


scen(t3_1, 'C3', (2, 3, 4), [
    '{org} in {city} needs to choose devices for a new office.',
    '{p} is setting up equipment for a small design studio.',
    'A school in {city} is buying hardware for a technology classroom.',
], [('Recommend a printer for printing 2000 high-quality black-and-white pages a day, with a reason.', 'Laser printer: fast, high volume, low cost per page, sharp text.', '1 mark: laser; 1 mark: reason [2]'),
    ('Explain why a 3D printer would be useful for producing prototypes.', 'Physical models can be made directly from a CAD design quickly and cheaply, and changed easily.', '1 mark: object from CAD/digital model; 1 mark: fast/cheap/customised [2]'),
    ('Choose a storage device for daily backups of 4 TB of data and justify your choice.', 'Magnetic tape or external HDD: high capacity, low cost per GB; backups need not be fast to access.', '1 mark device; 1 mark justification [2]'),
    ('Recommend storage for distributing a training video to 500 people without internet access.', 'Optical disc (DVD/Blu-ray) or USB flash drive: cheap, portable, read in most computers.', '1 mark choice; 1 mark reason [2]'),
    ('Explain why the computers should be fitted with SSDs rather than HDDs.', 'Faster boot and file access; no moving parts so more reliable; quieter.', '1 mark per point, max 2 [2]')], k=(2, 3))
essay(t3_1, [
    ('the replacement of all hard disk drives with solid-state drives in the computers at {org}', 'faster access and boot times; no moving parts so robust; lower power and heat; silent.',
     'higher cost per GB; limited write cycles; data recovery after failure is harder; existing HDDs still work.', 'SSDs for operating system and active work, HDD/tape for bulk archives is a common compromise.'),
    ('the use of 3D printers by {org} to make spare parts on demand', 'parts made quickly when needed; less stock held; custom designs; less transport.',
     'printers and materials can be expensive; parts may be weaker than manufactured ones; slow for large quantities; staff training.', 'suitable for small runs and rare parts, not mass production.'),
], ['{org} in {city} is reviewing its hardware budget.', 'The IT manager at {org} has been asked to prepare a recommendation.'])

t3_2 = topic('Primary memory: RAM and ROM, SRAM and DRAM, PROM, EPROM and EEPROM', 'primary memory', 'ram and rom', 'sram and dram', 'eeprom')
t3_2.fixed('C1', (1, 2), [
    ('Which type of memory is volatile?', 'RAM', 'RAM loses its contents when power is removed; ROM is non-volatile.', ['ROM', 'EEPROM', 'Flash memory in an SSD']),
    ('Which type of RAM must be refreshed regularly?', 'DRAM', 'DRAM stores bits as charge on capacitors, which leaks, so must be refreshed thousands of times per second.', ['SRAM', 'ROM', 'PROM']),
    ('Which memory is normally used for cache?', 'SRAM', 'SRAM uses flip-flops: faster, no refresh, but more expensive and less dense.', ['DRAM', 'EPROM', 'Magnetic tape']),
    ('How is an EPROM erased?', 'By exposing it to ultraviolet light', 'EPROM: erased with UV light through a quartz window; EEPROM: erased electrically.', ['By applying a voltage while in the circuit', 'It cannot be erased', 'By deleting files in the OS']),
    ('What is PROM?', 'ROM that can be programmed once after manufacture', 'Programmable ROM: blank chip, programmed once by blowing fuses; cannot be changed.', ['ROM that can be erased electrically', 'RAM that keeps data after power off', 'Memory that is written during manufacture only']),
    ('What is typically stored in ROM in a computer?', 'The start-up instructions (BIOS/bootstrap)', 'ROM stores firmware such as the bootstrap loader, needed when power is first applied.', ['The user\'s documents', 'The data being processed by open applications', 'The operating system page file']),
    ('Which memory can be erased and reprogrammed electrically without removing it from the circuit?', 'EEPROM', 'EEPROM (and flash) are electrically erasable in-circuit.', ['EPROM', 'PROM', 'DRAM']),
])
t3_2.fixed('C2', (2, 3, 4), [
    ('Explain why DRAM is used for main memory while SRAM is used for cache.', 'DRAM is cheaper and has higher density so large capacities are affordable; SRAM is faster (no refresh needed) so is used for small cache close to the CPU.',
     '1 mark: DRAM cheaper/denser; 1 mark: SRAM faster; 1 mark: matched to use [3]'),
    ('Describe two differences between RAM and ROM.', 'RAM is volatile, ROM non-volatile; RAM can be read and written, ROM is (normally) read only; RAM holds programs/data in use, ROM holds start-up firmware.', '1 mark per difference, max 2 [2]'),
    ('Explain why a manufacturer of washing machines might use EEPROM rather than ROM for the control program.', 'The firmware can be updated electrically in the field to fix bugs or add features without replacing the chip.', '1 mark: can be reprogrammed/updated; 1 mark: without removing/replacing chip [2]'),
    ('Explain why SRAM does not need refreshing but DRAM does.', 'SRAM stores each bit in a flip-flop that holds its state while powered; DRAM stores a bit as charge on a capacitor that leaks away.', '1 mark: SRAM flip-flops; 1 mark: DRAM capacitors leak [2]'),
])
ar(t3_2, [('DRAM needs to be refreshed regularly.', 'DRAM stores each bit as a charge on a capacitor, and the charge leaks away.'),
          ('SRAM is used for cache memory.', 'SRAM has faster access times than DRAM.'),
          ('ROM is used to store the bootstrap program.', 'ROM is non-volatile, so its contents remain when the power is switched off.'),
          ('An EEPROM can be updated without removing it from the device.', 'EEPROM can be erased and rewritten electrically.')],
   ['SRAM is cheaper per gigabyte than DRAM.', 'RAM keeps its contents when the power is removed.', 'EPROM is erased by applying a voltage in the circuit.', 'PROM can be reprogrammed many times.'])
scen(t3_2, 'C3', (2, 3, 4), [
    '{org} in {city} is designing a new games console with RAM, ROM and cache memory.',
    '{p} is choosing the memory for a new laptop to be sold by {org}.',
], [('State which type of memory should store the start-up firmware, and why.', 'ROM/EEPROM: non-volatile so the program is present when the device is switched on.', '1 mark type; 1 mark reason [2]'),
    ('Explain why adding more RAM can improve performance.', 'More programs/data held in RAM so less use of virtual memory (swapping to disk), which is slow.', '1 mark: less virtual memory/paging; 1 mark: disk access slower than RAM [2]'),
    ('Suggest why EEPROM is better than PROM for the firmware.', 'Firmware updates/bug fixes can be installed later; PROM can only be written once.', '1 mark: updatable; 1 mark: PROM one-time [2]'),
    ('Explain why the device uses a small amount of SRAM as well as DRAM.', 'SRAM is fast so used as cache for frequently used data; DRAM is cheap for large main memory.', '1 mark each [2]')], k=(2, 3))
scen(t3_2, 'C4', (2, 3, 4, 5), [
    'Engineers at {org} are choosing memory for a new tablet computer.',
    '{p} is writing a buying guide that explains computer memory.',
], [('Compare SRAM and DRAM in terms of speed, cost and density.', 'SRAM faster, more expensive, lower density; DRAM slower, cheaper, higher density.', '1 mark each comparison [3]'),
    ('Explain the role of ROM in the start-up of the device.', 'ROM holds the bootstrap/BIOS which tests hardware and loads the OS from storage into RAM.', '1 mark: holds bootstrap; 1 mark: loads OS into RAM [2]'),
    ('Evaluate the choice of EEPROM over EPROM for storing firmware.', 'EEPROM is erased electrically in-circuit, so updates are easy; EPROM needs removal and UV light; EEPROM has limited write cycles but firmware is rarely updated.', '1 mark per point; 1 mark conclusion [3]'),
    ('Explain why RAM is described as volatile and the consequence for users.', 'Contents lost when power off, so unsaved work is lost.', '1 mark each [2]')], k=(3, 4))

t3_3 = topic('Embedded systems and buffers', 'embedded systems', 'buffers')
t3_3.fixed('C1', (1, 2), [
    ('What is an embedded system?', 'A computer system built into a larger device to perform a dedicated function', 'e.g. microcontroller in a washing machine; dedicated task, often real-time, limited interface.',
     ['A general-purpose desktop computer', 'A program that runs inside a web browser', 'A server in a data centre']),
    ('What is a buffer?', 'A temporary memory area that holds data being transferred between devices', 'Buffers compensate for differences in speed between devices (e.g. CPU and printer).',
     ['A permanent backup of a file', 'A type of processor register used for addresses only', 'A cable that connects devices']),
    ('Which is an example of an embedded system?', 'The controller in a microwave oven', 'Embedded systems are found in appliances, cars, medical devices, etc.', ['A laptop running a word processor', 'A web server', 'A smartphone app']),
    ('Why are buffers used when streaming video?', 'To store data in advance so playback continues smoothly if the download rate varies', 'The buffer is filled ahead of playback; the player reads from it at a steady rate.',
     ['To compress the video', 'To encrypt the video', 'To increase the screen resolution']),
])
t3_3.fixed('C2', (2, 3, 4), [
    ('Give two advantages and one disadvantage of embedded systems.', 'Advantages: small, cheap to mass-produce, low power, reliable/dedicated, fast response. Disadvantage: difficult to upgrade; limited user interface; hard to repair.', '1 mark per point, max 3 [3]'),
    ('Explain how a buffer is used when a document is sent from a computer to a printer.', 'Data is sent to the printer buffer at high speed; the printer reads it at its own slower speed; the CPU can continue other tasks; when the buffer is empty an interrupt requests more data.',
     '1 mark per point, max 3 [3]'),
    ('Explain why embedded systems are often programmed in firmware stored in ROM or flash memory.', 'The program must be available immediately at power-on and rarely changes; non-volatile memory keeps it without power.', '1 mark: non-volatile; 1 mark: fixed dedicated function [2]'),
])
scen(t3_3, 'C3', (2, 3, 4), [
    'A car manufacturer in {city} fits many microcontrollers in each car, including one in the entertainment system that streams music.',
    '{org} sells a smart TV that contains embedded systems and streams films over the internet.',
    '{p} uses a smart speaker containing an embedded system to stream radio from the internet.',
], [('Identify two embedded systems in this context and their functions.', 'e.g. engine management, anti-lock brakes, air-conditioning control, display controller.', '1 mark each with function [2]'),
    ('Explain why a buffer is needed in this situation.', 'Data arrives at a different/variable rate to the rate it is used; the buffer smooths this out so the device does not wait or lose data.', '1 mark: speed difference; 1 mark: smooths flow/prevents pauses [2]'),
    ('Describe one security risk of an embedded system that is connected to the internet.', 'It may be hacked because firmware is rarely updated; it could be used in a botnet or reveal personal data.', '1 mark risk; 1 mark explanation [2]'),
    ('State two characteristics of an embedded system.', 'Dedicated task; part of a larger device; real-time; low power; firmware in ROM.', '1 mark each [2]')], k=(2, 3))
essay(t3_3, [
    ('the use of internet-connected embedded systems in homes, such as smart thermostats and door locks', 'remote control and monitoring; energy savings; convenience; automatic updates.',
     'security vulnerabilities and hacking; privacy of data collected; failure if network down; devices hard to update.', 'benefits are large if devices are kept updated and secured.'),
], ['{org} in {city} sells smart-home devices.', '{p} is writing a consumer guide to smart-home technology.'])

CHAPTERS[3] = [t3_1, t3_2, t3_3]

# =============================================================================== Chapter 4 Logic gates
GATES = {'AND': lambda a, c: a & c, 'OR': lambda a, c: a | c, 'NAND': lambda a, c: 1 - (a & c), 'NOR': lambda a, c: 1 - (a | c), 'XOR': lambda a, c: a ^ c}


def lg_eval(e, env):
    if e[0] == 'V':
        return env[e[1]]
    if e[0] == 'NOT':
        return 1 - lg_eval(e[1], env)
    return GATES[e[0]](lg_eval(e[1], env), lg_eval(e[2], env))


def lg_str(e, top=True):
    if e[0] == 'V':
        return e[1]
    if e[0] == 'NOT':
        inner = lg_str(e[1], False)
        return f'NOT {inner}'
    s = f'{lg_str(e[1], False)} {e[0]} {lg_str(e[2], False)}'
    return s if top else f'({s})'


def lg_gates(e):
    if e[0] == 'V':
        return 0
    return 1 + sum(lg_gates(x) for x in e[1:])


def lg_vars(e):
    if e[0] == 'V':
        return {e[1]}
    out = set()
    for x in e[1:]:
        out |= lg_vars(x)
    return out


def lg_rand(r, vs, n_gates, ops=('AND', 'OR', 'NAND', 'NOR', 'XOR')):
    """Random expression using every variable in vs at least once, with about n_gates gates."""
    leaves = [('V', v) for v in vs]
    r.shuffle(leaves)
    nodes = leaves[:]
    while len(nodes) > 1:
        i, j = r.sample(range(len(nodes)), 2)
        a, c = nodes[i], nodes[j]
        if r.random() < 0.25 and a[0] != 'NOT':
            a = ('NOT', a)
        new = (r.choice(ops), a, c)
        nodes = [x for k, x in enumerate(nodes) if k not in (i, j)] + [new]
    e = nodes[0]
    while lg_gates(e) < n_gates:
        v = ('V', r.choice(vs))
        e = (r.choice(ops), e, v) if r.random() < 0.5 else (r.choice(ops), v, e)
    if r.random() < 0.2 and lg_gates(e) < n_gates + 1:
        e = ('NOT', e)
    return e


def lg_table(e, vs):
    rows = []
    for i in range(1 << len(vs)):
        env = {v: (i >> (len(vs) - 1 - k)) & 1 for k, v in enumerate(vs)}
        rows.append(lg_eval(e, env))
    return rows


def lg_words(e, names=None):
    names = names or {}
    if e[0] == 'V':
        return f'{names.get(e[1], e[1])} is 1'
    if e[0] == 'NOT':
        if e[1][0] == 'V':
            return f'{names.get(e[1][1], e[1][1])} is 0'
        return f'it is not true that ({lg_words(e[1], names)})'
    a, c = lg_words(e[1], names), lg_words(e[2], names)
    if e[1][0] not in ('V', 'NOT'):
        a = f'({a})'
    if e[2][0] not in ('V', 'NOT'):
        c = f'({c})'
    w = {'AND': f'{a} and {c}', 'OR': f'{a} or {c}', 'XOR': f'either {a} or {c} but not both', 'NAND': f'not both {a} and {c}', 'NOR': f'neither {a} nor {c}'}[e[0]]
    return w


def tt_text(vs, outs, label='X'):
    rows = []
    for i, o in enumerate(outs):
        bits = format(i, f'0{len(vs)}b')
        rows.append(''.join(bits) + f'→{o}')
    return ' '.join(rows)


t4_1 = topic('Logic gates (NOT, AND, OR, NAND, NOR, XOR) and their truth tables', 'logic gates', 'truth tables', 'nand nor xor')
t4_1.fixed('C1', (1, 2), [
    ('Which gate gives an output of 1 only when both inputs are 1?', 'AND', 'AND: X = 1 only if A = 1 and B = 1.', ['OR', 'XOR', 'NOR']),
    ('Which gate gives an output of 1 when the inputs are different?', 'XOR', 'XOR (exclusive OR): 1 when exactly one input is 1.', ['OR', 'AND', 'NAND']),
    ('Which gate gives an output of 0 only when both inputs are 1?', 'NAND', 'NAND = NOT AND: outputs 1, 1, 1, 0.', ['NOR', 'AND', 'XOR']),
    ('Which gate gives an output of 1 only when both inputs are 0?', 'NOR', 'NOR = NOT OR: outputs 1, 0, 0, 0.', ['NAND', 'NOT', 'XOR']),
    ('How many rows are needed in a truth table for a circuit with 3 inputs?', '8', '2³ = 8 combinations.', ['3', '6', '9']),
    ('Which gate has only one input?', 'NOT', 'NOT (inverter) has one input and outputs the opposite value.', ['AND', 'XOR', 'NAND']),
    ('What is the output of an OR gate when its inputs are A = 0 and B = 1?', '1', 'OR outputs 1 if at least one input is 1.', ['0', 'It is undefined', 'Both 0 and 1']),
    ('How many rows are needed in a truth table for a circuit with 4 inputs?', '16', '2⁴ = 16.', ['4', '8', '12']),
])
t4_1.fixed('C2', (2, 3, 4), [
    ('Explain the difference between the OR gate and the XOR gate.', 'Both give 1 when exactly one input is 1; when both inputs are 1, OR gives 1 but XOR gives 0.', '1 mark: same for one input 1; 1 mark: differ when both 1 [2]'),
    ('Explain why NAND gates are called universal gates.', 'Any other logic gate (and so any logic circuit) can be built from NAND gates alone.', '1 mark: any gate/circuit; 1 mark: from NAND only [2]'),
    ('Explain why NOT (A AND B) is not the same as (NOT A) AND (NOT B), using one row of a truth table.', 'For A = 1, B = 0: NOT(A AND B) = NOT 0 = 1, but (NOT A) AND (NOT B) = 0 AND 1 = 0.', '1 mark: chosen row; 1 mark: both values shown differing [2]'),
])


@t4_1.add('C3', (1, 2, 3))
def t4_1_gate(r, D):
    g = r.choice(list(GATES) + ['NOT'])
    if g == 'NOT':
        a = r.randrange(2)
        stem = f'Input A = {a} is applied to a NOT gate. State the output.'
        return MCQ(r, stem.replace('State the output.', 'What is the output?'), str(1 - a), [str(a), 'undefined', 'both 0 and 1'], f'NOT inverts: {1 - a}') if D == 1 else Q(stem, str(1 - a), f'NOT inverts the input: {1 - a} [1]')
    outs = [GATES[g](a, c) for a in (0, 1) for c in (0, 1)]
    if r.random() < 0.5 or D == 1:
        stem = f'A logic gate with inputs A and B gives the outputs {", ".join(map(str, outs))} for the inputs AB = 00, 01, 10, 11 respectively. Identify the gate.'
        others = [x for x in GATES if x != g]
        return MCQ(r, stem.replace('Identify the gate.', 'Which gate is it?'), g, others, f'{g} truth table: {", ".join(map(str, outs))}.') if D <= 2 else Q(stem, g, f'{g} [1]')
    a, c = r.randrange(2), r.randrange(2)
    e = ('NOT', (g, ('V', 'A'), ('V', 'B'))) if D == 3 else (g, ('V', 'A'), ('V', 'B'))
    v = lg_eval(e, {'A': a, 'B': c})
    return Q(f'Give the output of X = {lg_str(e)} when A = {a} and B = {c}.', str(v), f'{g}({a}, {c}) = {GATES[g](a, c)}' + (f'; NOT gives {v}' if D == 3 else '') + ' [1]')


@t4_1.add('C3', (2, 3, 4, 5), 'numerical')
def t4_1_table(r, D):
    vs = ['A', 'B'] if D <= 2 else ['A', 'B', 'C']
    e = lg_rand(r, vs, 1 if D <= 2 else D - 1)
    outs = lg_table(e, vs)
    stem = f'Complete the output column X of the truth table for X = {lg_str(e)}. Give X for the inputs {"".join(vs)} = ' + ', '.join(format(i, f"0{len(vs)}b") for i in range(1 << len(vs))) + ' in order.'
    m = 2 if len(vs) == 2 else (3 if D < 5 else 4)
    return Q(stem, ''.join(map(str, outs)), f'X = {", ".join(map(str, outs))}. ' + ('1 mark for each 2 correct rows' if len(vs) == 2 else f'Award {m} marks for 8 correct rows, {m - 1} for 6–7, {m - 2} for 4–5') + f' [{m}]', marks=m)


scen(t4_1, 'C4', (2, 3, 4, 5), [
    'A circuit designer at {org} is testing logic gates for a new control board.',
    '{p} is studying a circuit diagram in a logic simulator.',
], [lambda r, d: (lambda e: (f'For X = {lg_str(e)}, give the output for each input combination AB = 00, 01, 10, 11.', ''.join(map(str, lg_table(e, ['A', 'B']))), f'{", ".join(map(str, lg_table(e, ["A", "B"])))} [2]'))(lg_rand(r, ['A', 'B'], 2)),
    lambda r, d: (lambda g: (f'State the name of the single gate whose output is {", ".join(str(GATES[g](a, c)) for a in (0, 1) for c in (0, 1))} for AB = 00, 01, 10, 11.', g, f'{g} [1]'))(r.choice(list(GATES))),
    ('Explain why a truth table for 3 inputs has 8 rows.', 'Each input can be 0 or 1, so there are 2 × 2 × 2 = 2³ = 8 combinations.', '1 mark: 2 states per input; 1 mark: 2³ [2]'),
    ('Draw (describe) the symbol for a NAND gate.', 'An AND gate shape (D-shape) with a small circle (inversion bubble) on the output.', '1 mark D-shape; 1 mark bubble on output [2]'),
    lambda r, d: (lambda e: (f'Write a logic expression for a circuit in which {lg_words(e)}; the output is X.', 'X = ' + lg_str(e), f'1 mark per correct gate/operator, {lg_gates(e)} gates [{lg_gates(e)}]'))(lg_rand(r, ['A', 'B', 'C'], 2))], k=(3, 4))

# ----------------------------------------------------------------------------- 4.2 constructing circuits
SCEN_LG = [
    ('greenhouse', {'A': 'the temperature sensor input T', 'B': 'the window sensor input W', 'C': 'the humidity sensor input H'}, ['T', 'W', 'H'],
     'A greenhouse monitoring system sounds an alarm X. Input T = 1 if the temperature is above 30 °C, W = 1 if the window is open and H = 1 if the humidity is high.'),
    ('factory', {'A': 'P', 'B': 'S', 'C': 'L'}, ['P', 'S', 'L'],
     'A machine in a factory stops (output X = 1) depending on three inputs: P = 1 if the pressure is too high, S = 1 if the safety guard is open and L = 1 if the oil level is low.'),
    ('car', {'A': 'D', 'B': 'K', 'C': 'B'}, ['D', 'K', 'B'],
     'A car warning light X depends on three inputs: D = 1 if a door is open, K = 1 if the key is in the ignition and B = 1 if the seat belt is fastened.'),
    ('pool', {'A': 'F', 'B': 'T', 'C': 'C'}, ['F', 'T', 'C'],
     'A swimming pool pump control X depends on inputs F (1 = filter blocked), T (1 = water temperature too low) and C (1 = chlorine level correct).'),
    ('plant', {'A': 'R', 'B': 'M', 'C': 'V'}, ['R', 'M', 'V'],
     'A chemical plant safety system gives an output X from inputs R (1 = reactor temperature high), M (1 = mixer running) and V (1 = valve open).'),
    ('lift', {'A': 'O', 'B': 'W', 'C': 'E'}, ['O', 'W', 'E'],
     'A lift control circuit has output X from inputs O (1 = door open), W (1 = weight limit exceeded) and E (1 = emergency button pressed).'),
]


def _lg_scenario(r, D):
    sc = r.choice(SCEN_LG)
    vs = sc[2]
    e = lg_rand(r, vs, 2 if D <= 2 else (3 if D <= 4 else 4), ops=('AND', 'OR', 'XOR', 'NOR') if D >= 3 else ('AND', 'OR'))
    return sc, vs, e


@t4_1.add('C2', (2, 3, 4), 'explain')
def t4_1_spot(r, D):
    g = r.choice(['AND', 'OR', 'NAND', 'NOR', 'XOR'])
    outs = [GATES[g](a, c) for a in (0, 1) for c in (0, 1)]
    i = r.randrange(4)
    wrong = outs[:]
    wrong[i] = 1 - wrong[i]
    d = ctx(r)
    ab = format(i, '02b')
    return Q(f'{d["p"]} writes the truth table for {"an" if g in ("AND", "OR", "XOR") else "a"} {g} gate as X = {", ".join(map(str, wrong))} for AB = 00, 01, 10, 11. Identify and correct the error, explaining why.',
             f'Row AB = {ab} is wrong: X should be {outs[i]}, because {"an" if g in ("AND", "OR", "XOR") else "a"} {g} gate ' + {'AND': 'gives 1 only when both inputs are 1', 'OR': 'gives 1 when at least one input is 1', 'NAND': 'gives 0 only when both inputs are 1',
                                                                                   'NOR': 'gives 1 only when both inputs are 0', 'XOR': 'gives 1 only when the inputs differ'}[g] + '.',
             f'1 mark: identifies row {ab}; 1 mark: correct value with reason [2]')


t4_2 = topic('Constructing logic circuits and truth tables from problem statements and logic expressions', 'constructing logic circuits', 'problem statements', 'logic expressions')
t4_2.fixed('C1', (1, 2, 3), [
    ('In a logic expression, which operation is usually written as "A AND NOT B"?', 'Output 1 when A is 1 and B is 0', 'NOT B is 1 when B = 0; AND requires both.', ['Output 1 when A is 0 and B is 1', 'Output 1 when A and B are both 1', 'Output 1 when A or B is 0']),
    ('How many logic gates are needed to build X = (A AND B) OR NOT C?', '3', 'AND, OR and NOT: 3 gates.', ['2', '4', '5']),
    ('A circuit has inputs A, B and C. How many rows does its truth table have?', '8', '2³ = 8.', ['6', '3', '9']),
    ('What is a logic expression?', 'A statement of how the output depends on the inputs, using logic operators', 'e.g. X = (A AND B) OR C.', ['A diagram of transistors', 'A list of input values only', 'A program written in assembly language']),
    ('What is meant by a problem statement in logic circuit design?', 'A written description of the conditions under which the output is 1', 'The statement is translated into an expression, circuit or truth table.', ['A list of gates that are faulty', 'The truth table of a NOT gate', 'An error report from a simulator']),
])
t4_2.fixed('C2', (2, 3, 4), [
    ('Explain how a truth table can be used to check that a logic circuit matches its problem statement.', 'Work out the output of the circuit for every combination of inputs and compare each row with the output required by the statement; any difference shows an error.',
     '1 mark: evaluate every input combination; 1 mark: compare with required output [2]'),
    ('Explain why working columns are useful when completing a truth table for a complex expression.', 'Intermediate results (e.g. the output of each gate) are recorded so each step is simple and errors are easier to find.', '1 mark: record intermediate gate outputs; 1 mark: reduce errors/easier checking [2]'),
])


@t4_2.add('C3', (1, 2, 3, 4, 5))
def t4_2_expr(r, D):
    sc, vs, e = _lg_scenario(r, D)
    names = {v: v for v in vs}
    words = lg_words(e, names)
    stem = f'{sc[3]} The output X is 1 when {words}. Write the logic expression for X.'
    ans = 'X = ' + lg_str(e)
    if D == 1:
        alt = lg_rand(r, vs, 2, ops=('AND', 'OR'))
        alts = []
        for g in ('AND', 'OR', 'XOR'):
            if e[0] in GATES and e[0] != g:
                alts.append('X = ' + lg_str((g,) + e[1:]))
        alts.append('X = ' + lg_str(alt))
        alts.append('X = ' + lg_str(('NOT', e)))
        return MCQ(r, stem.replace('Write the logic expression for X.', 'Which logic expression is correct?'), ans, alts, ans)
    g = lg_gates(e)
    return Q(stem, ans, f'{ans}. 1 mark per correctly placed operator/gate [{g}]', marks=g)


@t4_2.add('C3', (2, 3, 4, 5), 'numerical')
def t4_2_tt(r, D):
    sc, vs, e = _lg_scenario(r, D)
    outs = lg_table(e, vs)
    stem = f'{sc[3]} The output is given by X = {lg_str(e)}. Complete the truth table: give X for {"".join(vs)} = 000, 001, 010, 011, 100, 101, 110, 111 in order.'
    m = 4 if D >= 4 else 3
    return Q(stem, ''.join(map(str, outs)), f'X = {", ".join(map(str, outs))}. {m} marks for all 8 rows correct, {m - 1} for 6–7, {m - 2} for 4–5 [{m}]', marks=m)


@t4_2.add('C4', (2, 3, 4, 5), 'multi_step')
def t4_2_full(r, D):
    sc, vs, e = _lg_scenario(r, D)
    outs = lg_table(e, vs)
    ones = [format(i, '03b') for i, o in enumerate(outs) if o]
    g = lg_gates(e)
    stem = (f'{sc[3]} The output X is 1 when {lg_words(e)}. (a) Write a logic expression for X. (b) Complete the truth table, giving X for {"".join(vs)} = 000 to 111 in order. '
            f'(c) State the number of logic gates needed if each operator (including NOT) is one gate.')
    if D >= 4:
        stem += ' (d) List the input combinations that make X = 1.'
    ans = f'(a) X = {lg_str(e)} (b) {"".join(map(str, outs))} (c) {g}' + (f' (d) {", ".join(ones) if ones else "none"}' if D >= 4 else '')
    key = f'(a) X = {lg_str(e)} [{min(g, 3)}] (b) {", ".join(map(str, outs))} [3] (c) {g} [1]' + (' (d) [1]' if D >= 4 else '')
    return Q(stem, ans, key, marks=min(g, 3) + 4 + (1 if D >= 4 else 0), typ='multi_step')


@t4_2.add('C2', (2, 3, 4), 'explain')
def t4_2_check(r, D):
    sc, vs, e = _lg_scenario(r, 3)
    outs = lg_table(e, vs)
    i = r.randrange(8)
    d = ctx(r)
    row = format(i, '03b')
    wrong = 1 - outs[i]
    env = {v: int(row[k]) for k, v in enumerate(vs)}
    return Q(f'For X = {lg_str(e)}, {d["p"]} says that when {", ".join(f"{v} = {env[v]}" for v in vs)} the output is {wrong}. Explain whether {d["p"]} is correct.',
             f'Incorrect: substituting gives X = {outs[i]}.', f'1 mark: correct substitution of each part; 1 mark: X = {outs[i]} so {d["p"]} is wrong [2]')


t4_3 = topic('Simplifying logic circuits and expressions using NAND/NOR equivalence', 'simplifying logic circuits', 'nand/nor equivalence')
t4_3.fixed('C1', (1, 2, 3), [
    ('A NAND gate has both inputs connected to A. What is the output?', 'NOT A', 'A NAND A = NOT (A AND A) = NOT A.', ['A', '1', '0']),
    ('A NOR gate has both inputs connected to A. What is the output?', 'NOT A', 'A NOR A = NOT (A OR A) = NOT A.', ['A', '0', '1']),
    ('What is the minimum number of NAND gates needed to make an AND gate?', '2', 'NAND then NAND-as-NOT: (A NAND B) NAND (A NAND B).', ['1', '3', '4']),
    ('What is the minimum number of NAND gates needed to make an OR gate?', '3', 'A OR B = (A NAND A) NAND (B NAND B).', ['2', '4', '1']),
    ('What is the minimum number of NOR gates needed to make an OR gate?', '2', '(A NOR B) NOR (A NOR B) = A OR B.', ['1', '3', '4']),
    ('What is the minimum number of NAND gates needed to make an XOR gate?', '4', 'Standard 4-NAND XOR circuit.', ['2', '3', '5']),
    ('Why might a circuit designer simplify a logic circuit?', 'To use fewer gates, reducing cost, power and delay', 'Fewer gates: cheaper, smaller, faster, less power and heat.', ['To add more inputs', 'To make the truth table longer', 'To change the function of the circuit']),
])
t4_3.fixed('C2', (2, 3, 4), [
    ('Explain why manufacturers often build circuits only from NAND gates.', 'NAND is universal so any circuit can be built; using one gate type simplifies manufacture and NAND gates are cheap and fast in CMOS.', '1 mark: universal; 1 mark: one type of chip/cheaper manufacture [2]'),
    ('Show how A OR B can be built using only NAND gates.', '(A NAND A) gives NOT A; (B NAND B) gives NOT B; (NOT A) NAND (NOT B) = A OR B (De Morgan).', '1 mark: NOT A and NOT B from NANDs; 1 mark: final NAND; 1 mark: justification [3]'),
    ('Show how a NOT gate can be made from a NOR gate.', 'Connect both inputs of the NOR gate to A: A NOR A = NOT (A OR A) = NOT A.', '1 mark: both inputs joined; 1 mark: justification [2]'),
])
NAMED = {(0, 0, 0, 1): 'AND', (0, 1, 1, 1): 'OR', (1, 1, 1, 0): 'NAND', (1, 0, 0, 0): 'NOR', (0, 1, 1, 0): 'XOR', (1, 0, 0, 1): 'XNOR',
         (1, 1, 0, 0): 'NOT A', (1, 0, 1, 0): 'NOT B', (0, 0, 1, 1): 'A', (0, 1, 0, 1): 'B', (0, 0, 1, 0): 'A AND NOT B', (0, 1, 0, 0): 'NOT A AND B',
         (1, 1, 0, 1): 'NOT A OR B', (1, 0, 1, 1): 'A OR NOT B'}


def _uni(r, op, depth):
    leaves = [('V', 'A'), ('V', 'B')]
    if depth == 0:
        return r.choice(leaves)
    a = _uni(r, op, depth - 1) if r.random() < 0.7 else r.choice(leaves)
    c = a if r.random() < 0.3 else (_uni(r, op, depth - 1) if r.random() < 0.6 else r.choice(leaves))
    return (op, a, c)


@t4_3.add('C3', (1, 2, 3, 4, 5))
def t4_3_uni(r, D):
    op = r.choice(['NAND', 'NOR'])
    for _ in range(40):
        e = _uni(r, op, 2 if D <= 3 else 3)
        if e[0] == 'V' or lg_gates(e) < 2 or lg_vars(e) != {'A', 'B'}:
            continue
        outs = tuple(lg_table(e, ['A', 'B']))
        if outs in NAMED and NAMED[outs] not in ('A', 'B'):
            name = NAMED[outs]
            stem = f'A circuit made only of {op} gates gives X = {lg_str(e)}. Complete the truth table for AB = 00, 01, 10, 11 and state the single function that the circuit is equivalent to.'
            key = f'Outputs {", ".join(map(str, outs))} [2]; equivalent to {name} [1] [3]'
            if D == 1:
                return MCQ(r, f'A circuit made only of {op} gates gives X = {lg_str(e)}. Which single function is it equivalent to?', name, [v for v in NAMED.values() if v != name][:6], key.replace(' [3]', ''))
            return Q(stem, f'{"".join(map(str, outs))}; {name}', key, marks=3)
    return None


@t4_3.add('C3', (2, 3, 4))
def t4_3_count(r, D):
    op = r.choice(['NAND', 'NOR'])
    tbl = {'NAND': {'NOT': 1, 'AND': 2, 'OR': 3, 'NOR': 4, 'XOR': 4}, 'NOR': {'NOT': 1, 'OR': 2, 'AND': 3, 'NAND': 4}}[op]
    gs = r.sample(list(tbl), 2)
    tot = tbl[gs[0]] + tbl[gs[1]]
    stem = f'A designer must replace one {gs[0]} gate and one {gs[1]} gate with circuits made only from {op} gates. State the minimum number of {op} gates needed for each and the total.'
    return Q(stem, f'{gs[0]}: {tbl[gs[0]]}; {gs[1]}: {tbl[gs[1]]}; total {tot}', f'{gs[0]} = {tbl[gs[0]]} [1]; {gs[1]} = {tbl[gs[1]]} [1]; total {tot} [1] [3]', marks=3)


@t4_3.add('C4', (2, 3, 4, 5), 'multi_step')
def t4_3_equiv(r, D):
    vs = ['A', 'B', 'C']
    e = lg_rand(r, vs, 3 if D <= 3 else 4)
    outs = lg_table(e, vs)
    ones = [format(i, '03b') for i, o in enumerate(outs) if o]
    if not ones or len(ones) == 8:
        return None
    sop = ' OR '.join('(' + ' AND '.join((v if bit == '1' else f'NOT {v}') for v, bit in zip(vs, row)) + ')' for row in ones)
    d = ctx(r)
    stem = (f'{d["p"]} at {d["org"]} has designed a circuit with output X = {lg_str(e)}. (a) Complete the truth table for ABC = 000 to 111. (b) Write a sum-of-products expression for X from your truth table. '
            f'(c) Explain why a simplified circuit with the same truth table would be preferred.')
    return Q(stem, f'(a) {"".join(map(str, outs))} (b) X = {sop} (c) fewer gates: cheaper, less power, less delay, same function',
             f'(a) {", ".join(map(str, outs))} [3] (b) one AND term per row where X = 1: {sop} [2] (c) any two of fewer gates/cost/power/heat/speed [2]', marks=7, typ='multi_step')


@t4_3.add('C2', (2, 3, 4), 'explain')
def t4_3_claim(r, D):
    pairs = [('X = NOT (A AND B)', 'X = (NOT A) OR (NOT B)', True), ('X = NOT (A OR B)', 'X = (NOT A) AND (NOT B)', True),
             ('X = NOT (A AND B)', 'X = (NOT A) AND (NOT B)', False), ('X = NOT (A OR B)', 'X = (NOT A) OR (NOT B)', False),
             ('X = (A NAND A) NAND (B NAND B)', 'X = A OR B', True), ('X = (A NOR B) NOR (A NOR B)', 'X = A OR B', True),
             ('X = (A NAND B) NAND (A NAND B)', 'X = A OR B', False), ('X = (A NOR A) NOR (B NOR B)', 'X = A AND B', True)]
    a, c, same = r.choice(pairs)
    d = ctx(r)
    return Q(f'{d["p"]} claims that the circuits {a} and {c} are equivalent. Use a truth table or a logic argument to decide whether the claim is correct.',
             ('Correct: both have the same output for all four input combinations.' if same else 'Incorrect: the outputs differ for at least one input combination (e.g. A = 1, B = 0).'),
             '1 mark: evaluates both for all input rows; 1 mark: correct conclusion [2]')


CHAPTERS[4] = [t4_1, t4_2, t4_3]

# =============================================================================== Chapter 5 Processor fundamentals
REGS = [('PC', 'Program Counter', 'holds the address of the next instruction to be fetched'),
        ('MAR', 'Memory Address Register', 'holds the address of the memory location currently being read from or written to'),
        ('MDR', 'Memory Data Register', 'holds the data or instruction just read from memory, or to be written to memory'),
        ('CIR', 'Current Instruction Register', 'holds the instruction currently being decoded and executed'),
        ('ACC', 'Accumulator', 'a general-purpose register that holds values being processed and the results of ALU operations'),
        ('IX', 'Index Register', 'holds a value added to an address to give the effective address in indexed addressing'),
        ('SR', 'Status Register', 'holds flags (bits) set by operations, such as carry, negative, overflow and zero')]
t5_1 = topic('Von Neumann architecture: registers (PC, MDR, MAR, ACC, IX, CIR, status), ALU, CU, clock and system buses', 'von neumann architecture', 'registers', 'system buses')
t5_1.fixed('C1', (1, 2), [
    ('What is the key feature of the Von Neumann architecture?', 'Instructions and data are stored together in the same main memory', 'Stored-program concept: program and data share memory and buses; one instruction fetched at a time.',
     ['Instructions and data are stored in separate memories', 'There is no main memory', 'Each instruction has its own processor']),
    ('Which bus is unidirectional?', 'Address bus', 'Address bus: CPU → memory only; data and control buses are bidirectional.', ['Data bus', 'Control bus', 'All system buses']),
    ('What is the role of the control unit (CU)?', 'To decode instructions and send control signals to coordinate the other components', 'CU: decodes, sends signals on the control bus, synchronises with clock.',
     ['To perform arithmetic and logic operations', 'To store the next instruction address', 'To hold data permanently']),
    ('What does the ALU do?', 'Carries out arithmetic and logical operations', 'ALU: addition, subtraction, comparisons, AND/OR, shifts.', ['Fetches instructions', 'Decodes instructions', 'Stores the operating system']),
    ('What is the purpose of the system clock?', 'To generate timing signals that synchronise the components of the processor', 'Clock pulses: each step of the fetch–execute cycle occurs on a clock tick.',
     ['To show the time to the user', 'To count the number of programs running', 'To store the date of files']),
    ('Which signals are carried on the control bus?', 'Signals such as memory read, memory write and interrupt request', 'Control bus carries timing and command signals (read/write, clock, interrupt, bus request).',
     ['Memory addresses only', 'Only data values', 'Only the contents of the PC']),
] + [(f'What is the role of the {n} ({a})?', role[0].upper() + role[1:], f'{a}: {role}.', [x[2][0].upper() + x[2][1:] for x in REGS if x[0] != a][:5]) for a, n, role in REGS])
t5_1.fixed('C2', (2, 3, 4), [
    ('Explain the difference between general-purpose registers and special-purpose registers.', 'General-purpose registers (e.g. ACC) hold any data being processed; special-purpose registers (e.g. PC, MAR, MDR, CIR) each have one specific role in the fetch–execute cycle.',
     '1 mark: general purpose — temporary data/any use; 1 mark: special purpose — dedicated function with example [2]'),
    ('Explain why the address bus is unidirectional but the data bus is bidirectional.', 'Only the processor sends addresses to memory/devices; data must travel both from memory to the processor (read) and from the processor to memory (write).',
     '1 mark: address only from CPU; 1 mark: data both ways (read and write) [2]'),
    ('Explain the role of the status register after a subtraction gives a negative result.', 'The negative flag is set to 1 (and possibly carry/overflow flags), so a later conditional jump can test it.', '1 mark: flag set; 1 mark: used by conditional instructions [2]'),
    ('Describe the role of the MAR and MDR when data is read from memory.', 'The address is placed in the MAR and sent on the address bus; the data at that address is sent on the data bus into the MDR.', '1 mark: MAR holds address; 1 mark: MDR receives data [2]'),
])
ar(t5_1, [('The address bus is unidirectional.', 'Addresses are only ever sent from the processor to memory or I/O devices.'),
          ('The MDR is used when writing data to memory.', 'Data to be written is placed in the MDR and sent on the data bus to the address held in the MAR.'),
          ('The PC is incremented during the fetch stage.', 'The next instruction is normally stored at the next memory address.'),
          ('The Von Neumann architecture can suffer from a bottleneck.', 'Instructions and data share the same bus, so only one can be transferred at a time.')],
   ['The CIR holds the address of the next instruction.', 'The control bus carries memory addresses.', 'The ALU decodes instructions.', 'The data bus is unidirectional.'])
scen(t5_1, 'C3', (2, 3, 4), [
    'The processor in a laptop used by {p} is executing a program stored in RAM.',
    'A student at {org} is using a simulator to watch the registers of a Von Neumann processor.',
], [lambda r, d: (lambda x: (f'State the full name of the {x[0]} register and describe its role.', f'{x[1]}: {x[2]}', f'1 mark name; 1 mark role [2]'))(r.choice(REGS)),
    ('Identify the bus used to send the address of an instruction to memory and the bus used to return the instruction.', 'Address bus; data bus.', '1 mark each [2]'),
    ('Describe the role of the control unit during the execution of an ADD instruction.', 'Decodes the instruction and sends control signals so the operand is fetched and the ALU adds it to the ACC.', '1 mark decode; 1 mark control signals to ALU/registers [2]'),
    ('Explain why the processor has a clock.', 'To synchronise operations; each step occurs on a clock pulse.', '1 mark [1]'),
    lambda r, d: (lambda n: (f'The address bus has {n} lines. Calculate how many memory locations can be addressed.', f'{1 << n:,}', f'2^{n} = {1 << n:,} [1]'))(r.choice([12, 16, 20, 24]))], k=(2, 3))
scen(t5_1, 'C4', (2, 3, 4, 5), [
    '{org} is designing a simple processor for an embedded controller, based on the Von Neumann model.',
    '{p} is writing a revision guide explaining how a Von Neumann processor works.',
], [('Describe the roles of the PC, MAR and CIR when an instruction is fetched.', 'PC holds address of next instruction, copied to MAR; instruction copied (via MDR) into CIR for decoding; PC incremented.', '1 mark per register role [3]'),
    ('Explain the Von Neumann bottleneck and one way to reduce it.', 'Data and instructions share one bus so cannot be fetched at once, limiting speed; reduce with cache memory or separate buses/Harvard design.', '1 mark: shared bus; 1 mark: limits speed; 1 mark: cache/separate buses [3]'),
    ('State the purpose of the IX register.', 'Holds a value added to an address for indexed addressing (e.g. stepping through an array).', '1 mark [1]'),
    ('Explain the purpose of the status register.', 'Its flags record the outcome of operations (zero, negative, carry, overflow), used by conditional instructions and interrupt handling.', '1 mark: flags; 1 mark: use [2]')], k=(3, 4))

t5_2 = topic('Factors affecting performance: clock speed, cores, bus width and cache memory', 'factors affecting performance', 'clock speed', 'cores', 'cache memory')
t5_2.fixed('C1', (1, 2), [
    ('What is meant by clock speed?', 'The number of clock cycles the processor completes per second', 'Measured in Hz (e.g. 3.2 GHz = 3.2 × 10⁹ cycles per second).', ['The number of programs run per second', 'The width of the data bus', 'The time taken to boot the computer']),
    ('Why does increasing the width of the data bus improve performance?', 'More bits can be transferred in each operation', 'A 64-bit data bus moves 64 bits per transfer vs 32 bits.', ['More memory locations can be addressed', 'The clock speed doubles', 'The processor needs fewer cores']),
    ('What is the main effect of increasing the width of the address bus?', 'More memory locations can be addressed', 'n address lines → 2ⁿ locations.', ['More bits transferred per cycle', 'The cache becomes larger', 'The ALU becomes faster']),
    ('What is cache memory?', 'Small, fast memory close to the processor that holds frequently used data and instructions', 'Cache (SRAM) reduces the time spent fetching from slower RAM.', ['Large, slow secondary storage', 'Memory used only for the operating system', 'A buffer for printers']),
    ('Why might doubling the number of cores not double performance?', 'Some programs cannot be split into tasks that run in parallel', 'Software must be written to use multiple cores; there is also overhead in communication between cores.',
     ['Cores share the same clock so each runs at half speed', 'Each core needs its own operating system', 'Only one core can access RAM']),
])
t5_2.fixed('C2', (2, 3, 4), [
    ('Explain how cache memory improves the performance of a processor.', 'Frequently used data/instructions are stored in fast cache near the CPU, so they are fetched more quickly than from RAM, reducing the time the processor waits.',
     '1 mark: stores frequently used data/instructions; 1 mark: faster access than RAM; 1 mark: less waiting / fewer RAM fetches [3]'),
    ('Explain why increasing clock speed can cause problems.', 'More heat is generated, which may cause instability or damage, so better cooling is needed; components may not keep up.', '1 mark: heat; 1 mark: consequence [2]'),
    ('Explain how a multi-core processor can improve performance.', 'Each core can fetch and execute instructions independently, so different tasks/threads run at the same time.', '1 mark: cores execute independently; 1 mark: parallel tasks [2]'),
])


@t5_2.add('C3', (1, 2, 3, 4, 5))
def t5_2_calc(r, D):
    kind = r.choice(['addr', 'mem', 'cycles', 'transfer']) if D >= 2 else r.choice(['addr', 'mem'])
    if kind == 'addr':
        n = r.choice([8, 10, 12, 16, 20, 24])
        stem, ans, key = f'A processor has a {n}-bit address bus. How many different memory locations can it address?', f'{1 << n:,}', f'2^{n} = {1 << n:,} [1]'
        dis = [f'{n * n:,}', f'{(1 << n) - 1:,}', f'{1 << (n - 1):,}', f'{2 * n}']
    elif kind == 'mem':
        n = r.choice([16, 20, 24, 30, 32])
        ws = r.choice([1, 2, 4])
        tot = (1 << n) * ws
        units = [(1 << 30, 'GiB'), (1 << 20, 'MiB'), (1 << 10, 'KiB')]
        u = next(x for x in units if tot >= x[0])
        v = tot // u[0]
        stem = f'A computer has a {n}-bit address bus and each memory location holds {ws} byte{"s" if ws > 1 else ""}. Calculate the maximum memory size in {u[1]}.'
        ans, key = f'{v} {u[1]}', f'2^{n} locations × {ws} = {tot:,} bytes [1]; ÷ {u[0]:,} = {v} {u[1]} [1] [2]'
        dis = [f'{v * 2} {u[1]}', f'{max(1, v // 2)} {u[1]}' if v > 1 else f'{v * 8} {u[1]}', f'{n * ws} {u[1]}', f'{v * 1024} {u[1]}']
    elif kind == 'cycles':
        ghz = r.choice([1, 2, 2.5, 3, 4])
        cpi = r.choice([2, 4, 5, 8, 10])
        ips = ghz * 1e9 / cpi
        stem = f'A {ghz:g} GHz processor takes an average of {cpi} clock cycles to execute each instruction. Calculate the number of instructions executed per second.'
        ans, key = f'{ips / 1e6:g} million', f'{ghz:g} × 10⁹ cycles per second ÷ {cpi} = {ips / 1e6:g} × 10⁶ instructions per second [2]'
        dis = [f'{ghz * 1000 * cpi:g} million', f'{ghz * 1000:g} million', f'{ips / 1e5:g} million']
    else:
        bw = r.choice([16, 32, 64])
        nb = r.choice([256, 512, 1024, 2048, 4096])
        t_ = nb * 8 // bw
        stem = f'Data is transferred across a {bw}-bit data bus, one transfer per clock cycle. Calculate how many clock cycles are needed to transfer {nb} bytes, and state the effect of doubling the bus width.'
        ans, key = f'{t_} cycles; halved to {t_ // 2}', f'{nb} × 8 = {nb * 8} bits [1]; ÷ {bw} = {t_} cycles [1]; doubling width halves cycles to {t_ // 2} [1] [3]'
        dis = [f'{t_ * 2} cycles', f'{nb // bw} cycles', f'{nb} cycles']
    if D == 1 or (D == 2 and kind != 'transfer' and r.random() < 0.5):
        return MCQ(r, stem.replace('Calculate the maximum', 'What is the maximum').replace('Calculate the number', 'What is the number').replace('Calculate how many', 'How many'), ans, dis, key.replace(' [1]', '').replace(' [2]', ''))
    return Q(stem, ans, key)


scen(t5_2, 'C4', (2, 3, 4, 5), [
    '{p} is choosing between two laptops for video editing. Laptop P has a 3.6 GHz dual-core processor with 4 MiB cache; laptop Q has a 2.8 GHz eight-core processor with 16 MiB cache.',
    '{org} must choose new processors for its servers in {city}. Option 1: 4 cores at 4.0 GHz, 8 MiB cache. Option 2: 16 cores at 2.6 GHz, 32 MiB cache.',
], [('Explain how the number of cores affects performance for this use.', 'More cores let independent tasks/threads run at once; video editing/servers have many parallel tasks so benefit.', '1 mark: parallel execution; 1 mark: linked to the use [2]'),
    ('Explain why the option with the lower clock speed may still perform better.', 'More cores and larger cache can outweigh lower clock speed when tasks are parallel and data is reused.', '1 mark cores; 1 mark cache; 1 mark conclusion [3]'),
    ('Describe how a larger cache improves performance.', 'More frequently used data/instructions fit in fast cache, fewer slow RAM accesses.', '1 mark each [2]'),
    ('Give one factor, other than the processor, that affects the computer\'s performance.', 'Amount of RAM, storage speed (SSD), bus width, GPU.', '1 mark [1]'),
    ('Make and justify a recommendation.', 'Choose the multi-core, large-cache option for parallel workloads; the higher clock speed option for single-threaded tasks.', '1 mark choice; 1 mark justification [2]')], k=(3, 4))

t5_3 = topic('Ports (USB, HDMI, VGA) and the fetch–execute cycle in register transfer notation', 'ports (usb, hdmi, vga)', 'fetch–execute cycle', 'register transfer notation')
FE = ['MAR ← [PC]', 'PC ← [PC] + 1', 'MDR ← [[MAR]]', 'CIR ← [MDR]']
t5_3.fixed('C1', (1, 2), [
    ('In register transfer notation, what does MAR ← [PC] mean?', 'The contents of the PC are copied into the MAR', 'Square brackets mean "the contents of"; ← means "is copied into".', ['The MAR is copied into the PC', 'The PC is cleared', 'The address in the PC is incremented']),
    ('What does MDR ← [[MAR]] mean?', 'The contents of the memory location whose address is in the MAR are copied into the MDR', 'Double brackets: the contents of the address held in MAR.',
     ['The contents of the MAR are copied into the MDR', 'The MDR is copied into memory', 'The MAR is incremented']),
    ('Which port is designed to carry both digital video and audio?', 'HDMI', 'HDMI carries high-definition digital video and audio; VGA is analogue video only.', ['VGA', 'USB 1.1', 'PS/2']),
    ('Which statement about VGA is correct?', 'It carries analogue video signals only', 'VGA is an older analogue video standard with no audio.', ['It carries digital video and audio', 'It is used to charge devices', 'It is faster than HDMI']),
    ('Which is a feature of USB?', 'Devices are automatically detected and can be powered through the cable', 'USB: plug and play, standard connector, supplies power, many devices on one controller.',
     ['It can only connect printers', 'It carries analogue video only', 'Devices must be configured manually every time']),
    ('During the fetch stage, when is the PC incremented?', 'After its contents have been copied to the MAR', 'MAR ← [PC] then PC ← [PC] + 1 (may happen while memory is read).', ['Before it is copied to the MAR', 'Only after the instruction has been executed', 'Never']),
])
t5_3.fixed('C2', (2, 3, 4), [
    ('Describe the fetch stage of the fetch–execute cycle using register transfer notation.', 'MAR ← [PC]; PC ← [PC] + 1; MDR ← [[MAR]]; CIR ← [MDR].', '1 mark per correct step in order [4]'),
    ('Explain why the PC is incremented during the fetch stage.', 'So that it holds the address of the next instruction, ready for the next cycle (unless a jump changes it).', '1 mark: points to next instruction; 1 mark: ready for next fetch / jump may overwrite [2]'),
    ('Explain two benefits of USB for connecting peripherals.', 'Plug and play — drivers loaded automatically; one standard connector for many devices; supplies power; backward compatible.', '1 mark per benefit, max 2 [2]'),
    ('Describe what happens in the decode and execute stages after an instruction reaches the CIR.', 'The CU splits the instruction into opcode and operand and decodes the opcode; control signals are sent so the instruction is carried out (e.g. ALU operation, memory transfer, or PC changed for a jump).',
     '1 mark: opcode/operand split; 1 mark: decoded by CU; 1 mark: executed with control signals [3]'),
])


@t5_3.add('C3', (1, 2, 3, 4))
def t5_3_rtn(r, D):
    i = r.randrange(4)
    if D <= 2:
        stem = f'In the fetch stage, which register transfer happens immediately after {FE[i - 1] if i else "the start of the cycle"}?'
        return MCQ(r, stem, FE[i], [x for x in FE if x != FE[i]] + ['CIR ← [PC]', 'PC ← [MAR]'], f'Order: {"; ".join(FE)}.')
    pc = r.randrange(100, 900)
    instr = r.choice(['LDD', 'ADD', 'STO', 'SUB'])
    opnd = r.randrange(200, 999)
    stem = (f'The PC contains {pc}. Memory location {pc} contains the instruction {instr} {opnd}. Give the contents of the PC, MAR, MDR and CIR at the end of the fetch stage.')
    return Q(stem, f'PC = {pc + 1}, MAR = {pc}, MDR = {instr} {opnd}, CIR = {instr} {opnd}', f'1 mark each: PC {pc + 1}; MAR {pc}; MDR {instr} {opnd}; CIR {instr} {opnd} [4]', marks=4)


@t5_3.add('C2', (2, 3, 4), 'explain')
def t5_3_err(r, D):
    seq = FE[:]
    i, j = sorted(r.sample(range(4), 2))
    seq[i], seq[j] = seq[j], seq[i]
    d = ctx(r)
    return Q(f'{d["p"]} writes the fetch stage as: {"; ".join(seq)}. Identify the error and write the correct sequence.',
             f'Steps "{FE[i]}" and "{FE[j]}" are in the wrong order. Correct: {"; ".join(FE)}.', '1 mark: identifies the misplaced steps with reason; 1 mark: correct order [2]')


scen(t5_3, 'C4', (2, 3, 4, 5), [
    'A technician at {org} in {city} is connecting monitors, printers and an old projector to classroom computers, and is explaining to students how the processor runs programs.',
    '{p} is setting up a computer lab at {org}: connecting a monitor with speakers, a projector and USB devices, and teaching how the processor fetches instructions.',
], [('Recommend a port for connecting a modern monitor with speakers, with a reason.', 'HDMI: carries digital video and audio in one cable, high resolution.', '1 mark port; 1 mark reason [2]'),
    ('Explain why an old projector may need a VGA connection.', 'Older projectors only accept analogue video; VGA carries analogue signals.', '1 mark each [2]'),
    ('Describe the fetch stage using register transfer notation.', 'MAR ← [PC]; PC ← [PC] + 1; MDR ← [[MAR]]; CIR ← [MDR].', '1 mark per step [4]'),
    ('State what happens to the PC when a JMP instruction is executed.', 'The PC is loaded with the address given in the operand.', '1 mark [1]'),
    ('Explain why USB devices can be connected without restarting the computer.', 'USB is plug and play / hot-swappable: the OS detects the device and loads the driver automatically.', '1 mark detection; 1 mark driver loaded [2]')], k=(3, 4))

t5_4 = topic('Interrupts and interrupt service routines', 'interrupts', 'interrupt service routines')
t5_4.fixed('C1', (1, 2), [
    ('What is an interrupt?', 'A signal to the processor that a device or program needs attention', 'Interrupts can come from hardware (e.g. printer out of paper) or software (e.g. division by zero).',
     ['A fault that permanently stops the computer', 'An instruction to delete a program', 'A type of storage device']),
    ('When does the processor check for interrupts?', 'At the end of each fetch–execute cycle', 'The CPU checks the interrupt register after each instruction completes.', ['Only when the computer starts', 'Before each fetch stage begins writing to memory', 'Only when a program ends']),
    ('What is an interrupt service routine (ISR)?', 'A program that handles a particular interrupt', 'The ISR is called to deal with the cause of the interrupt, then the original task resumes.', ['The program that caused the error', 'The part of the CU that generates the clock', 'A utility for backing up data']),
    ('Which is an example of a hardware interrupt?', 'A key being pressed on the keyboard', 'Hardware interrupts come from devices: keyboard, printer, timer, power failure.', ['A division by zero in a program', 'A program requesting a file', 'A loop counter reaching 10']),
    ('Why are the contents of registers saved on the stack when an interrupt is serviced?', 'So the interrupted program can be resumed exactly where it stopped', 'Registers (PC, ACC, status, etc.) are pushed onto the stack and restored after the ISR.',
     ['To delete the interrupted program', 'To increase the clock speed', 'To make the ISR run faster']),
])
t5_4.fixed('C2', (2, 3, 4), [
    ('Describe the sequence of steps taken by the processor when an interrupt is detected.', 'At end of current cycle, check priority; save registers (PC etc.) on the stack; load PC with start address of the ISR; run ISR; restore registers from the stack; continue original program.',
     '1 mark per step in order, max 4 [4]'),
    ('Explain why interrupts are given priorities.', 'Some events (e.g. power failure, hardware fault) are more urgent; a higher-priority interrupt can interrupt a lower-priority ISR, so critical events are handled first.', '1 mark: some more urgent; 1 mark: higher priority handled first/can interrupt lower [2]'),
    ('Explain the difference between a hardware interrupt and a software interrupt, giving an example of each.', 'Hardware: generated by a device (printer out of paper, key press); software: generated by a program (division by zero, request for OS service).', '1 mark each with example [2]'),
])
scen(t5_4, 'C3', (2, 3, 4), [
    '{p} is printing a long report at {org} while editing a spreadsheet.',
    'A computer at {org} detects that the power supply is failing while a program is running.',
    'A program written by {p} attempts to divide a number by zero.',
], [('Identify the interrupt in this situation and state whether it is a hardware or software interrupt.', 'e.g. printer out of paper/buffer empty (hardware); power failure (hardware); division by zero (software).', '1 mark interrupt; 1 mark type [2]'),
    ('Explain what happens to the current task when the interrupt is serviced.', 'Its registers are saved on the stack; the ISR runs; registers restored and the task resumes.', '1 mark save; 1 mark resume [2]'),
    ('Suggest why this interrupt might be given a high priority.', 'Data could be lost or the system damaged if it is not dealt with immediately.', '1 mark [1]'),
    ('Explain why the processor checks for interrupts only at the end of a fetch–execute cycle.', 'So that the current instruction completes and the state can be saved consistently.', '1 mark [1]')], k=(2, 3))
essay(t5_4, [('the importance of interrupts in a multitasking operating system', 'devices signal when ready so CPU does not waste time polling; urgent events handled at once; enables time-slicing via timer interrupts.',
              'too many interrupts add overhead from saving/restoring registers; badly prioritised interrupts can delay important tasks.', 'interrupts are essential for efficient multitasking but need careful priority management.')],
      ['{org} in {city} runs many programs at the same time on each computer.', '{p} is writing a report on how operating systems manage hardware.'])

CHAPTERS[5] = [t5_1, t5_2, t5_3, t5_4]

# =============================================================================== Chapter 6 Assembly language
INSTR = [('LDM #n', 'Immediate addressing. Load the number n to ACC'), ('LDD <address>', 'Direct addressing. Load the contents of the location at the given address to ACC'),
         ('LDI <address>', 'Indirect addressing. The address to be used is at the given address. Load the contents of this second address to ACC'),
         ('LDX <address>', 'Indexed addressing. Form the address from <address> + the contents of the index register. Copy the contents of this calculated address to ACC'),
         ('LDR #n', 'Immediate addressing. Load the number n to IX'), ('STO <address>', 'Store the contents of ACC at the given address'),
         ('ADD <address>', 'Add the contents of the given address to the ACC'), ('INC <register>', 'Add 1 to the contents of the register (ACC or IX)'),
         ('CMP #n', 'Compare the contents of ACC with number n'), ('JPE <address>', 'Following a compare instruction, jump to <address> if the compare was True'),
         ('JPN <address>', 'Following a compare instruction, jump to <address> if the compare was False'), ('JMP <address>', 'Jump to the given address'),
         ('LSL #n', 'Bits in ACC are shifted logically n places to the left. Zeros are introduced on the right hand end'),
         ('AND #n', 'Bitwise AND operation of the contents of ACC with the operand')]


class Asm:
    """Minimal 9618 assembly simulator. prog: {addr: (op, operand)}; mem: {addr: value}."""

    def __init__(self, prog, mem):
        self.p, self.m = prog, dict(mem)
        self.acc, self.ix, self.flag = 0, 0, False
        self.out = []
        self.trace = []

    def val(self, s):
        if s.startswith('#B') or s.startswith('B'):
            return int(s.lstrip('#')[1:], 2)
        if s.startswith('#&'):
            return int(s[2:], 16)
        return int(s[1:]) if s.startswith('#') else self.m.get(int(s), 0)

    def run(self, start, limit=400):
        pc = start
        for _ in range(limit):
            op, o = self.p[pc]
            nxt = pc + 1
            if op == 'LDM':
                self.acc = int(o[1:])
            elif op == 'LDD':
                self.acc = self.m.get(int(o), 0)
            elif op == 'LDI':
                self.acc = self.m.get(self.m.get(int(o), 0), 0)
            elif op == 'LDX':
                self.acc = self.m.get(int(o) + self.ix, 0)
            elif op == 'LDR':
                self.ix = int(o[1:])
            elif op == 'MOV':
                self.ix = self.acc
            elif op == 'STO':
                self.m[int(o)] = self.acc
            elif op == 'ADD':
                self.acc = (self.acc + self.val(o))
            elif op == 'SUB':
                self.acc = (self.acc - self.val(o))
            elif op == 'INC':
                if o == 'ACC':
                    self.acc += 1
                else:
                    self.ix += 1
            elif op == 'DEC':
                if o == 'ACC':
                    self.acc -= 1
                else:
                    self.ix -= 1
            elif op == 'CMP':
                self.flag = self.acc == self.val(o)
            elif op == 'CMI':
                self.flag = self.acc == self.m.get(self.m.get(int(o), 0), 0)
            elif op == 'JPE':
                if self.flag:
                    nxt = int(o)
            elif op == 'JPN':
                if not self.flag:
                    nxt = int(o)
            elif op == 'JMP':
                nxt = int(o)
            elif op == 'AND':
                self.acc &= self.val(o)
            elif op == 'OR':
                self.acc |= self.val(o)
            elif op == 'XOR':
                self.acc ^= self.val(o)
            elif op == 'LSL':
                self.acc = (self.acc << int(o[1:])) & 0xFF
            elif op == 'LSR':
                self.acc = (self.acc & 0xFF) >> int(o[1:])
            elif op == 'OUT':
                self.out.append(self.acc)
            elif op == 'END':
                self.trace.append((pc, op, o, self.acc, self.ix))
                return True
            self.trace.append((pc, op, o, self.acc, self.ix))
            pc = nxt
        return False


def asm_text(prog):
    return code([f'{a}  {op} {o}'.rstrip() for a, (op, o) in sorted(prog.items())])


def mem_text(mem):
    return ', '.join(f'[{a}] = {v}' for a, v in sorted(mem.items()))


def _addr_setup(r):
    base = r.choice([100, 150, 200, 300, 400, 500])
    mem = {}
    for k in range(6):
        mem[base + k] = r.randrange(1, 60)
    # make one location point inside the block for indirect addressing
    mem[base + 1] = base + r.randrange(2, 6)
    ix = r.randrange(1, 4)
    return base, mem, ix


t6_1 = topic('Assembly language and machine code; two-pass assemblers', 'assembly language and machine code', 'two-pass assemblers')
t6_1.fixed('C1', (1, 2), [
    ('What is machine code?', 'Binary instructions that the processor can execute directly', 'Machine code: binary opcodes and operands specific to the processor\'s instruction set.',
     ['A high-level language', 'Instructions written using mnemonics', 'Pseudocode used for design']),
    ('What is a mnemonic in assembly language?', 'A short code that represents an opcode, such as LDD or ADD', 'Mnemonics are human-readable abbreviations of machine-code opcodes.', ['A label for a memory address', 'A type of variable', 'A comment in the code']),
    ('What does an assembler do?', 'Translates assembly language into machine code', 'Assembler: one assembly instruction → one machine-code instruction (mostly).', ['Translates high-level code line by line as it runs', 'Links library files only', 'Converts machine code into high-level code']),
    ('What is stored in the symbol table during the first pass of a two-pass assembler?', 'Labels (symbolic addresses) and their memory addresses', 'Pass 1 records each label and its address, so forward references can be resolved in pass 2.',
     ['The machine code for each instruction', 'The error messages', 'The values of all variables at run time']),
    ('Why is a two-pass assembler needed?', 'To deal with forward references to labels not yet defined', 'A jump to a later label cannot be translated until its address is known; pass 1 finds all label addresses.',
     ['To translate the program into two languages', 'To run the program twice for testing', 'To compress the machine code']),
    ('An instruction is made up of an opcode and an operand. What does the operand hold?', 'The data, or the address of the data, that the instruction uses', 'Opcode = operation (and addressing mode); operand = data/address/register.',
     ['The operation to be carried out', 'The address of the next instruction', 'The result of the instruction']),
])
t6_1.fixed('C2', (2, 3, 4), [
    ('Describe what happens in each pass of a two-pass assembler.', 'Pass 1: reads the program, removes comments, and builds the symbol table of labels and their addresses (and handles directives). Pass 2: uses the symbol table to replace labels with addresses and translates opcodes into machine code.',
     '1 mark: pass 1 builds symbol table; 1 mark: forward references/labels recorded; 1 mark: pass 2 generates machine code with addresses replaced [3]'),
    ('Explain why a programmer might write part of a program in assembly language.', 'For direct control of hardware/registers; for code that must be very fast or very small, e.g. a device driver or embedded system.', '1 mark: hardware control; 1 mark: speed/memory efficiency [2]'),
    ('Explain one disadvantage of writing in assembly language rather than a high-level language.', 'It is specific to one processor so not portable, and is harder and slower to write, read and debug.', '1 mark: not portable/hard to write; 1 mark: explanation [2]'),
])


@t6_1.add('C3', (2, 3, 4, 5))
def t6_1_symtab(r, D):
    start = r.randrange(10, 90) * 10
    l1, l2 = r.sample(['LOOP', 'START', 'AGAIN', 'REPEAT', 'TOP'], 2), r.sample(['DONE', 'FINISH', 'STOP', 'ENDPROG', 'EXIT'], 1)[0]
    l1 = l1[0]
    dn = r.sample(['STEP', 'COUNT', 'TOTAL', 'VALUE', 'LIMIT', 'NUM'], 2)
    body = [(l1, f'LDD {dn[0]}'), ('', 'CMP #0'), ('', f'JPE {l2}'), ('', 'DEC ACC'), ('', f'STO {dn[0]}'), ('', f'LDD {dn[1]}'), ('', f'ADD #{r.randrange(2, 9)}'),
            ('', f'STO {dn[1]}'), ('', f'JMP {l1}'), (l2, 'END'), (dn[0], str(r.randrange(2, 9))), (dn[1], '0')]
    if D <= 3:
        body = body[:6] + body[7:]
    tbl, lines = {}, []
    for i, (lab, ins) in enumerate(body):
        if lab:
            tbl[lab] = start + i
        lines.append(f'{start + i}  ' + (f'{lab}: ' if lab else '') + ins)
    stem = 'A two-pass assembler translates the program below. Complete the symbol table (each label and its address) produced by pass 1, and identify one forward reference.\n' + code(lines)
    ans = ', '.join(f'{k} = {v}' for k, v in sorted(tbl.items(), key=lambda x: x[1])) + f'; forward reference: {l2} (or {dn[0]}) used before it is defined'
    return Q(stem, ans, f'1 mark per two correct entries ({len(tbl)} labels) [2]; forward reference identified [1] [3]', marks=3)


scen(t6_1, 'C4', (2, 3, 4, 5), [
    '{p} is writing part of a device driver for {org} in assembly language. The program includes a JMP to a label defined later in the program.',
    'A programmer at {org} in {city} has written a hardware control routine in assembly language; it contains a jump to a label that appears later in the code.',
], [('Explain why the program must be translated before it can be run.', 'The processor can only execute machine code (binary); assembly mnemonics must be converted by an assembler.', '1 mark each [2]'),
    ('Explain how a two-pass assembler deals with the forward reference.', 'Pass 1 records the label address in the symbol table; pass 2 substitutes the address when generating machine code.', '1 mark pass 1; 1 mark pass 2 [2]'),
    ('Give two reasons for using assembly language for this task.', 'Direct access to registers/hardware; efficient (fast, small) code.', '1 mark each [2]'),
    ('Describe two features of the symbol table.', 'Holds labels/symbolic names; their addresses; built in pass 1; used in pass 2.', '1 mark each [2]'),
    ('Explain the difference between an opcode and an operand.', 'Opcode specifies the operation (and addressing mode); operand holds the data or address used.', '1 mark each [2]')], k=(3, 4))

t6_2 = topic('Instruction groups and addressing modes: immediate, direct, indirect, indexed and relative', 'instruction groups', 'addressing modes')
t6_2.fixed('C1', (1, 2), [
    ('Which addressing mode is used by LDM #25?', 'Immediate', 'Immediate: the operand is the value itself.', ['Direct', 'Indirect', 'Indexed']),
    ('Which addressing mode is used by LDD 200?', 'Direct', 'Direct: the operand is the address of the data.', ['Immediate', 'Indirect', 'Relative']),
    ('In indirect addressing, what does the operand hold?', 'The address of a location that holds the address of the data', 'LDI 200: go to 200, read an address, load the contents of that address.', ['The data value', 'An offset from the PC', 'The contents of the index register']),
    ('In indexed addressing, how is the effective address calculated?', 'Operand address + contents of the index register', 'LDX 300 with IX = 2 loads from address 302.', ['Operand address × IX', 'Operand address + contents of ACC', 'Contents of the PC + 1']),
    ('In relative addressing, the address is calculated relative to what?', 'The address of the current instruction (or the PC)', 'Relative: effective address = current instruction address + offset; allows relocatable code.', ['The index register', 'The start of RAM', 'The accumulator']),
    ('Which group does the instruction JPE belong to?', 'Jump (conditional) instructions', 'Instruction groups: data movement, I/O, arithmetic, unconditional/conditional jump, compare, bitwise.', ['Data movement', 'Input and output', 'Arithmetic']),
    ('Which group does the instruction STO belong to?', 'Data movement', 'STO copies the ACC to memory: data movement.', ['Arithmetic', 'Compare', 'Bit manipulation']),
])
t6_2.fixed('C2', (2, 3, 4), [
    ('Explain why indexed addressing is useful when processing an array.', 'The base address stays the same while the index register is incremented, so a loop can access consecutive elements with one instruction.', '1 mark: base + IX; 1 mark: increment IX in loop to step through elements [2]'),
    ('Explain the benefit of relative addressing for code that may be loaded anywhere in memory.', 'Jumps are given as offsets from the current instruction, so the code works whatever its start address (relocatable).', '1 mark: offset from current address; 1 mark: relocatable [2]'),
])


@t6_2.add('C3', (1, 2, 3, 4, 5))
def t6_2_mode(r, D):
    base, mem, ix = _addr_setup(r)
    mode = r.choice(['LDM', 'LDD', 'LDI', 'LDX'])
    a = base + (1 if mode == 'LDI' else r.randrange(0, 3))
    if mode == 'LDM':
        n = r.randrange(base, base + 6)
        res, how = n, f'immediate: the operand {n} itself is loaded'
        ins = f'LDM #{n}'
    elif mode == 'LDD':
        res, how = mem[a], f'direct: contents of {a}'
        ins = f'LDD {a}'
    elif mode == 'LDI':
        res, how = mem.get(mem[a], 0), f'indirect: [{a}] = {mem[a]}, then contents of {mem[a]} = {mem.get(mem[a], 0)}'
        ins = f'LDI {a}'
    else:
        res, how = mem.get(a + ix, 0), f'indexed: {a} + IX ({ix}) = {a + ix}, contents {mem.get(a + ix, 0)}'
        ins = f'LDX {a}'
    stem = f'The memory contains {mem_text(mem)} and the index register (IX) contains {ix}. State the value in the ACC after the instruction {ins} is executed.'
    others = [mem.get(a, 0), mem.get(mem.get(a, 0), 0), mem.get(a + ix, 0), a, a + ix]
    if D <= 2:
        return MCQ(r, stem.replace('State the value', 'What is the value').rstrip('.') + '?', str(res), [str(x) for x in others], f'{how}.')
    if D >= 4:
        mode2 = r.choice([m for m in ['LDD', 'LDI', 'LDX'] if m != mode])
        a2 = base + 1
        res2 = {'LDD': mem[a2], 'LDI': mem.get(mem[a2], 0), 'LDX': mem.get(a2 + ix, 0)}[mode2]
        stem += f' Then state the value after {mode2} {a2} is executed instead, and name both addressing modes.'
        names = {'LDM': 'immediate', 'LDD': 'direct', 'LDI': 'indirect', 'LDX': 'indexed'}
        return Q(stem, f'{res}; {res2}; {names[mode]} and {names[mode2]}', f'{how} [1]; {mode2} {a2} gives {res2} [1]; modes named [2] [4]', marks=4)
    return Q(stem, str(res), f'{how} [2]', marks=2)


@t6_2.add('C4', (2, 3, 4, 5), 'multi_step')
def t6_2_prog(r, D):
    base, mem, ix = _addr_setup(r)
    out = base + 8
    lines = [('LDR', f'#{ix}'), ('LDX', str(base)), ('ADD', str(base + 2)), ('STO', str(out)), ('LDI', str(base + 1)), ('ADD', f'#{r.randrange(1, 10)}'), ('STO', str(out + 1)), ('END', '')]
    prog = {50 + i: x for i, x in enumerate(lines)}
    sim = Asm(prog, mem)
    sim.run(50)
    stem = f'The memory contains {mem_text(mem)}. The program below is executed.\n{asm_text(prog)}\n(a) Give the value stored at address {out}. (b) Give the value stored at address {out + 1}. (c) Name the addressing mode used by each LD instruction.'
    return Q(stem, f'(a) {sim.m[out]} (b) {sim.m[out + 1]} (c) LDR immediate, LDX indexed, LDI indirect',
             f'(a) LDX {base} with IX = {ix} loads [{base + ix}] = {mem.get(base + ix, 0)}; + [{base + 2}] = {mem[base + 2]} → {sim.m[out]} [2] (b) LDI {base + 1}: [{base + 1}] = {mem[base + 1]}, [{mem[base + 1]}] = {mem.get(mem[base + 1], 0)}; plus immediate → {sim.m[out + 1]} [2] (c) [2]',
             marks=6, typ='multi_step')


@t6_2.add('C2', (2, 3, 4), 'explain')
def t6_2_group(r, D):
    ins = r.choice([('LDD 300', 'data movement'), ('STO 205', 'data movement'), ('ADD #5', 'arithmetic'), ('SUB 210', 'arithmetic'), ('CMP #0', 'compare'),
                    ('JPN 120', 'conditional jump'), ('JMP 100', 'unconditional jump'), ('IN', 'input/output'), ('OUT', 'input/output'), ('AND #B00001111', 'bit manipulation'),
                    ('LSL #2', 'bit manipulation'), ('INC IX', 'arithmetic'), ('LDX 400', 'data movement'), ('MOV IX', 'data movement')])
    ins2 = r.choice([('JPE 150', 'conditional jump'), ('LDM #12', 'data movement'), ('DEC ACC', 'arithmetic'), ('CMI 200', 'compare'), ('XOR #B10000001', 'bit manipulation')])
    return Q(f'State the instruction group for each of the instructions {ins[0]} and {ins2[0]}, and describe what each one does.', f'{ins[0]}: {ins[1]}; {ins2[0]}: {ins2[1]}.',
             '1 mark per correct group; 1 mark per description [4]', marks=4)


t6_3 = topic('Tracing simple assembly language programs', 'tracing simple assembly language programs', 'trace assembly')
t6_3.fixed('C1', (1, 2), [
    ('What does CMP #0 do?', 'Compares the contents of ACC with 0', 'CMP sets a flag used by the next JPE/JPN.', ['Copies 0 into the ACC', 'Jumps to address 0', 'Clears the memory']),
    ('After CMP #5, the instruction JPN 120 is executed and ACC contains 5. What happens?', 'The next instruction is the one after JPN (no jump)', 'JPN jumps if the compare was false; ACC = 5 so the compare was true, no jump.',
     ['Execution jumps to address 120', 'The program ends', 'ACC is set to 120']),
    ('What does INC IX do?', 'Adds 1 to the index register', 'INC <register> adds 1 to ACC or IX.', ['Adds 1 to the ACC', 'Loads 1 into IX', 'Increments the PC by 2']),
    ('Which instruction stops execution of a program?', 'END', 'END returns control to the operating system.', ['JMP 0', 'STO 0', 'CMP #0']),
    ('In a trace table for an assembly program, what is recorded?', 'The values in registers and memory locations after each instruction', 'A trace table follows the changes to ACC, IX, memory and output as each instruction runs.',
     ['The machine code for each line', 'The time taken by each instruction', 'The labels in the symbol table']),
])
t6_3.fixed('C2', (2, 3, 4), [
    ('Explain how a loop is created in assembly language.', 'A compare instruction tests a counter; a conditional jump (JPE/JPN) leaves the loop when the condition is met; an unconditional JMP at the end goes back to the start of the loop.',
     '1 mark: counter changed each iteration; 1 mark: CMP and conditional jump; 1 mark: JMP back to start [3]'),
    ('Explain why a trace table is useful when testing an assembly language program.', 'It records the value of each register/memory location after every instruction, so the programmer can see where the values first differ from those expected.', '1 mark: records values step by step; 1 mark: locates logic errors [2]'),
])


def _loop_prog(r, D):
    n = r.randrange(2, 5) if D <= 3 else r.randrange(3, 7)
    t0 = r.randrange(0, 10)
    st = r.randrange(2, 9)
    C, T, S = 300, 301, 302
    prog = {200: ('LDD', str(C)), 201: ('CMP', '#0'), 202: ('JPE', '210'), 203: ('DEC', 'ACC'), 204: ('STO', str(C)), 205: ('LDD', str(T)),
            206: ('ADD', str(S)), 207: ('STO', str(T)), 208: ('JMP', '200'), 210: ('END', '')}
    mem = {C: n, T: t0, S: st}
    return prog, mem, (C, T, S)


def _search_prog(r, D):
    vals = r.sample(range(1, 40), 5)
    target = r.choice(vals + [41]) if D >= 3 else r.choice(vals)
    base = 400
    mem = {base + i: v for i, v in enumerate(vals)}
    mem[500] = 0
    prog = {100: ('LDR', '#0'), 101: ('LDX', str(base)), 102: ('CMP', f'#{target}'), 103: ('JPE', '110'), 104: ('INC', 'IX'), 105: ('LDD', '500'),
            106: ('INC', 'ACC'), 107: ('STO', '500'), 108: ('CMP', '#5'), 109: ('JPN', '101'), 110: ('END', '')}
    return prog, mem, target


@t6_3.add('C3', (1, 2, 3, 4, 5))
def t6_3_loop(r, D):
    prog, mem, (C, T, S) = _loop_prog(r, D)
    sim = Asm(prog, mem)
    sim.run(200)
    fin = sim.m[T]
    stem = f'Memory contains {mem_text(mem)}. Trace the program below and state the final value stored at address {T} and at address {C}.\n{asm_text(prog)}'
    reps = mem[C]
    key = f'The loop runs {reps} times, adding [{S}] = {mem[S]} each time: {mem[T]} + {reps} × {mem[S]} = {fin}; [{C}] counts down to 0 [2]'
    if D == 1:
        return MCQ(r, stem.replace('state the final value stored at address ' + str(T) + ' and at address ' + str(C) + '.', f'what is the final value stored at address {T}?').replace('Trace the program below and', 'The program below runs;'), str(fin),
                   [str(fin + mem[S]), str(fin - mem[S]), str(mem[T] + mem[S]), str(reps * mem[S])], key.replace(' [2]', ''))
    if D >= 4:
        stem += f'\nAlso state how many times the instruction at address 206 is executed and explain the purpose of the instruction at address 202.'
        return Q(stem, f'[{T}] = {fin}; [{C}] = 0; 206 runs {reps} times; JPE 210 leaves the loop when the counter reaches 0',
                 key.replace(' [2]', '') + f'; 206 executed {reps} times [1]; JPE exits loop when ACC = 0 [1] [4]', marks=4)
    return Q(stem, f'[{T}] = {fin}; [{C}] = 0', key, marks=2)


@t6_3.add('C4', (3, 4, 5), 'multi_step')
def t6_3_search(r, D):
    prog, mem, target = _search_prog(r, D)
    sim = Asm(prog, mem)
    sim.run(100)
    found = target in [mem[400 + i] for i in range(5)]
    stem = (f'Memory contains {mem_text(mem)}. The program below is executed.\n{asm_text(prog)}\n(a) State the purpose of the program. (b) Give the final values of IX and of the contents of address 500. '
            f'(c) Explain what the final value of IX tells the user.')
    ans = f'(a) Linear search of the 5 values at 400–404 for {target} (b) IX = {sim.ix}, [500] = {sim.m[500]} (c) ' + (f'{target} was found at address {400 + sim.ix}; IX = {sim.ix} is its offset from address 400' if found else f'IX = 5 means {target} is not in the list')
    return Q(stem, ans, f'(a) searches for {target} [1] (b) IX = {sim.ix} [1]; [500] = {sim.m[500]} [1] (c) correct interpretation [2]', marks=5, typ='multi_step')


@t6_3.add('C2', (2, 3, 4), 'explain')
def t6_3_bug(r, D):
    prog, mem, (C, T, S) = _loop_prog(r, 2)
    bug = r.choice(['jpn', 'nostore'])
    bp = dict(prog)
    if bug == 'jpn':
        bp[202] = ('JPN', '210')
        why = 'JPN 210 jumps when the counter is NOT zero, so the loop ends immediately without adding anything; it should be JPE 210.'
        fix = '202 should be JPE 210'
    else:
        bp[204] = ('STO', str(T))
        why = f'STO {T} stores the decremented counter in the total instead of in {C}, so the counter never reaches 0 correctly; it should be STO {C}.'
        fix = f'204 should be STO {C}'
    stem = f'This program should add [{S}] to [{T}] the number of times given in [{C}]. Identify the error and correct it.\n{asm_text(bp)}'
    return Q(stem, why, f'1 mark: identifies line ({fix.split()[0]}); 1 mark: correction ({fix}) [2]')


t6_4 = topic('Bit manipulation: logical and arithmetic shifts and masking to test and set bits', 'bit manipulation', 'logical and arithmetic shifts', 'masking')
t6_4.fixed('C1', (1, 2), [
    ('What is the effect of a logical shift left of one place on an unsigned binary number (no bits lost)?', 'It multiplies the value by 2', 'Each bit moves to the next higher place value; a 0 enters on the right.', ['It divides the value by 2', 'It adds 1', 'It changes the sign']),
    ('In an arithmetic shift right, what happens to the most significant bit?', 'It is copied into the vacated position so the sign is kept', 'Arithmetic right shift preserves the sign bit in two\'s complement.', ['It is set to 0', 'It is lost and the result becomes positive', 'It is moved to the right-hand end']),
    ('Which operation is used with a mask to test whether a bit is set?', 'AND', 'AND with a mask that has 1 in the bit position; the result is non-zero if the bit is set.', ['OR', 'XOR', 'LSL']),
    ('Which operation sets a bit to 1 without changing the other bits?', 'OR with a mask that has 1 in that position', 'x OR 1 = 1; x OR 0 = x.', ['AND with a mask that has 1 in that position', 'XOR with all zeros', 'Logical shift right']),
    ('Which operation toggles (flips) selected bits?', 'XOR with a mask that has 1s in those positions', 'x XOR 1 = NOT x; x XOR 0 = x.', ['OR with a mask', 'AND with a mask', 'Arithmetic shift left']),
    ('In a cyclic shift, what happens to a bit shifted out of one end?', 'It re-enters at the other end', 'Cyclic (rotate) shift: no bits lost.', ['It is lost', 'It is copied to the carry flag only', 'It is set to 0']),
])
t6_4.fixed('C2', (2, 3, 4), [
    ('Explain the difference between a logical shift and an arithmetic shift to the right.', 'Logical shift right inserts 0 at the MSB end; arithmetic shift right copies the sign bit, so negative two\'s complement numbers stay negative (division by 2).',
     '1 mark: logical inserts 0; 1 mark: arithmetic keeps sign bit [2]'),
    ('Explain how a mask can be used to clear (set to 0) the lower four bits of a register.', 'AND the register with 11110000: bits ANDed with 0 become 0, bits ANDed with 1 are unchanged.', '1 mark: AND; 1 mark: mask 11110000 with explanation [2]'),
])


@t6_4.add('C3', (1, 2, 3, 4, 5))
def t6_4_op(r, D):
    v = r.randrange(1, 256)
    op = r.choice(['LSL', 'LSR', 'AND', 'OR', 'XOR', 'ASR']) if D >= 3 else r.choice(['LSL', 'LSR', 'AND', 'OR', 'XOR'])
    if op in ('LSL', 'LSR', 'ASR'):
        n = r.randrange(1, 4)
        if op == 'LSL':
            res = (v << n) & 0xFF
            desc = f'logical shift left {n} place{"s" if n > 1 else ""}'
            ins = f'LSL #{n}'
        elif op == 'LSR':
            res = v >> n
            desc = f'logical shift right {n} place{"s" if n > 1 else ""}'
            ins = f'LSR #{n}'
        else:
            sv = from_tc(b(v))
            res = (sv >> n) & 0xFF
            desc = f'arithmetic shift right {n} place{"s" if n > 1 else ""}'
            ins = f'arithmetic shift right {n}'
        stem = f'The ACC contains {b(v)}. Give the contents of the ACC after a {desc}' + (f' ({ins})' if op != 'ASR' else '') + '.'
        key = f'{b(v)} → {b(res)}' + (' (sign bit copied)' if op == 'ASR' else ' (zeros enter, bits shifted out are lost)') + ' [1]'
    else:
        m = r.randrange(1, 256)
        res = {'AND': v & m, 'OR': v | m, 'XOR': v ^ m}[op]
        stem = f'The ACC contains {b(v)}. Give the contents of the ACC after {op} #B{b(m)}.'
        key = f'bitwise {op}: {b(v)} {op} {b(m)} = {b(res)} [1]'
    if D == 1:
        return MCQ(r, stem.replace('Give', 'What are').rstrip('.') + '?', b(res), [b(res ^ 1), b(v), b((res << 1) & 0xFF), b(res >> 1), b(~res & 0xFF)], key.replace(' [1]', ''))
    if D >= 4:
        stem += ' Then give the denary value of the result and explain the effect of the operation.'
        return Q(stem, f'{b(res)} = {res if op != "ASR" else from_tc(b(res))}', key.replace(' [1]', ' [1]; denary value [1]; effect (e.g. ×2ⁿ / ÷2ⁿ / bits set, cleared or toggled) [1] [3]'), marks=3)
    return Q(stem, b(res), key)


@t6_4.add('C3', (2, 3, 4, 5))
def t6_4_mask(r, D):
    bits = sorted(r.sample(range(8), r.randrange(1, 4)))
    task = r.choice(['test', 'set', 'clear', 'toggle'])
    mask = sum(1 << (7 - i) for i in bits)
    pos = ', '.join(str(i + 1) for i in bits)
    if task == 'clear':
        mask = (~mask) & 0xFF
    op = {'test': 'AND', 'set': 'OR', 'clear': 'AND', 'toggle': 'XOR'}[task]
    v = r.randrange(256)
    res = {'AND': v & mask, 'OR': v | mask, 'XOR': v ^ mask}[op]
    stem = f'Bit positions are numbered 1 (most significant) to 8 (least significant). Write an instruction with a mask to {task} bit{"s" if len(bits) > 1 else ""} {pos} of the ACC, and give the result when the ACC contains {b(v)}.'
    ans = f'{op} #B{b(mask)}; result {b(res)}'
    extra = ''
    if task == 'test':
        extra = '; result non-zero → at least one tested bit is 1' if res else '; result is zero → the tested bit(s) are 0'
    return Q(stem, ans + extra, f'1 mark: {op}; 1 mark: mask {b(mask)}; 1 mark: result {b(res)} [3]', marks=3)


@t6_4.add('C4', (3, 4, 5), 'multi_step')
def t6_4_prog(r, D):
    v = r.randrange(1, 256)
    m = r.randrange(1, 255)
    n = r.randrange(1, 3)
    prog = {100: ('LDD', '200'), 101: ('AND', f'#B{b(m)}'), 102: ('LSL', f'#{n}'), 103: ('STO', '201'), 104: ('LDD', '200'), 105: ('XOR', '#B11111111'), 106: ('STO', '202'), 107: ('END', '')}
    sim = Asm(prog, {200: v})
    sim.run(100)
    stem = f'Address 200 contains {b(v)}. The program below is executed.\n{asm_text(prog)}\n(a) Give the binary value stored at 201. (b) Give the binary value stored at 202 and describe what instruction 105 does. (c) State the denary value at 201.'
    return Q(stem, f'(a) {b(sim.m[201])} (b) {b(sim.m[202])}; inverts every bit (one\'s complement) (c) {sim.m[201]}',
             f'(a) {b(v)} AND {b(m)} = {b(v & m)} [1], shifted left {n} → {b(sim.m[201])} [1] (b) {b(sim.m[202])} [1]; flips all bits [1] (c) {sim.m[201]} [1]', marks=5, typ='multi_step')


CHAPTERS[6] = [t6_1, t6_2, t6_3, t6_4]

# =============================================================================== Chapter 7 Monitoring and control
SENSORS = [('temperature', 'thermistor/temperature sensor', 'greenhouse heater', 'heater'), ('light', 'light sensor (photoresistor)', 'street lighting', 'lamp'),
           ('moisture', 'moisture sensor', 'soil irrigation system', 'water valve'), ('pressure', 'pressure sensor', 'burglar alarm under a doormat', 'siren'),
           ('infrared', 'infrared/motion sensor', 'automatic door', 'door motor'), ('pH', 'pH sensor', 'swimming pool chemical control', 'chemical pump'),
           ('humidity', 'humidity sensor', 'museum climate control', 'dehumidifier'), ('gas', 'gas (CO₂/smoke) sensor', 'factory ventilation', 'ventilation fan'),
           ('sound', 'sound/acoustic sensor', 'noise monitoring at an airport', 'warning display'), ('proximity', 'proximity/ultrasonic sensor', 'car parking assistant', 'buzzer')]
t7_1 = topic('Sensors and actuators in monitoring and control systems', 'sensors and actuators', 'monitoring and control systems')
t7_1.fixed('C1', (1, 2), [
    ('What is the role of a sensor?', 'To measure a physical property and send the reading to the computer', 'Sensors measure properties such as temperature or light; they do not make decisions.', ['To switch devices on and off', 'To store readings permanently', 'To decide what action to take']),
    ('What is an actuator?', 'A device that carries out a physical action on a signal from the computer', 'Actuators: motors, valves, relays, pumps, heaters.', ['A device that measures temperature', 'A program that analyses data', 'A type of input device such as a keyboard']),
    ('What is the difference between a monitoring system and a control system?', 'A control system acts on the environment; a monitoring system only records/reports readings', 'Monitoring: readings compared, warnings given; control: actuators change conditions.',
     ['A monitoring system uses actuators; a control system does not', 'There is no difference', 'Only monitoring systems use sensors']),
    ('Which of these is an actuator?', 'A motor that opens a window', 'Motors, pumps, valves, heaters are actuators.', ['A thermistor', 'A light sensor', 'An analogue-to-digital converter']),
    ('Which sensor would be used to detect an intruder walking through a room?', 'Infrared (motion) sensor', 'Passive infrared sensors detect body heat movement.', ['pH sensor', 'Moisture sensor', 'Humidity sensor']),
])
t7_1.fixed('C2', (2, 3, 4), [
    ('Explain why a sensor alone does not control a device.', 'The sensor only measures and sends data; the microprocessor compares the data with stored values and sends signals to an actuator, which carries out the action.',
     '1 mark: sensor only measures; 1 mark: processor decides/actuator acts [2]'),
    ('Describe the difference between a monitoring system and a control system, giving an example of each.', 'Monitoring: readings collected and displayed/warnings sounded but no action on the process, e.g. patient monitoring in a hospital. Control: processor uses actuators to change the process, e.g. greenhouse heating.',
     '1 mark each description; 1 mark each example [4]'),
])


@t7_1.add('C3', (1, 2, 3, 4))
def t7_1_pick(r, D):
    s = r.choice(SENSORS)
    if D <= 2:
        return MCQ(r, f'Which sensor is most suitable for a {s[2]}?', s[1], [x[1] for x in SENSORS if x[1] != s[1]], f'A {s[2]} needs to measure {s[0]}: {s[1]}.')
    d = ctx(r)
    return Q(f'{d["org"]} in {d["city"]} is installing a {s[2]}. Identify a suitable sensor and actuator and describe how the system works.',
             f'Sensor: {s[1]}; actuator: {s[3]}. The sensor sends readings (via an ADC) to the microprocessor, which compares them with a pre-set value and switches the {s[3]} on or off as needed; this repeats continuously.',
             '1 mark sensor; 1 mark actuator; 1 mark comparison with pre-set value; 1 mark actuator switched / continuous loop [4]', marks=4)


scen(t7_1, 'C4', (2, 3, 4, 5), [
    'A greenhouse owned by {org} near {city} grows tropical plants that need a temperature of 24 °C to 28 °C and moist soil.',
    'A hospital in {city} uses a computer system to watch patients in an intensive care unit.',
    'A museum in {city} must keep the humidity of its galleries between 45% and 55%.',
], [('Identify two sensors needed and state what each measures.', 'e.g. temperature sensor (temperature), moisture/humidity sensor (moisture/humidity).', '1 mark each [2]'),
    ('State whether this is a monitoring or a control system, with a reason.', 'Control if actuators change conditions (greenhouse/museum); monitoring if only warnings are given (hospital).', '1 mark choice; 1 mark reason [2]'),
    ('Describe how the microprocessor uses the sensor readings.', 'Readings converted by ADC; compared with stored limits; if outside range, signals sent to actuators/alarm; repeated continuously.', '1 mark per point, max 3 [3]'),
    ('Explain why a computer system is better than a human for this task.', 'Works 24/7; reacts faster; readings more accurate; no fatigue; data logged automatically.', '1 mark per point, max 2 [2]'),
    ('Name two actuators that could be used.', 'Heater, motor (window), water valve/pump, fan, dehumidifier.', '1 mark each [2]')], k=(3, 4))

t7_2 = topic('Feedback in control systems and the need for analogue-to-digital conversion', 'feedback in control systems', 'analogue-to-digital conversion')
t7_2.fixed('C1', (1, 2), [
    ('Why is an analogue-to-digital converter (ADC) needed in a control system?', 'Sensors produce analogue signals but the computer processes digital data', 'ADC converts the continuously varying sensor voltage into binary values.', ['To amplify the output to actuators', 'To store sensor readings', 'To encrypt the data']),
    ('What is feedback in a control system?', 'The output of the system affects the next input readings', 'Closed loop: the effect of the actuator is measured by the sensor and used for the next decision.', ['Comments from the users of the system', 'An error message from the processor', 'A log file of readings']),
    ('Why might a DAC be needed in a control system?', 'Some actuators need an analogue signal to operate', 'Digital-to-analogue converter changes processor output to a varying voltage, e.g. to set motor speed.', ['To read sensors', 'To convert analogue sensor readings to digital', 'To store data on a disk']),
    ('What is a closed-loop control system?', 'A system that uses feedback from sensors to adjust its output', 'Closed loop: sensor → processor → actuator → environment → sensor.', ['A system that runs without sensors', 'A system that cannot be switched off', 'A system that has no actuators']),
])
t7_2.fixed('C2', (2, 3, 4), [
    ('Explain how feedback is used in a central heating system to keep a room at 21 °C.', 'The sensor measures the temperature; the processor compares it with 21 °C; if lower, the heater is switched on, if higher it is switched off; the change in temperature is measured again, so the output affects the next input.',
     '1 mark sensor measures; 1 mark compared with set point; 1 mark heater switched; 1 mark loop repeated / output affects input [4]'),
    ('Explain why a range is often used instead of a single target value in a control system.', 'If a single value is used the actuator would switch on and off very rapidly (hunting), causing wear; a small range (hysteresis) prevents this.', '1 mark: rapid switching; 1 mark: wear/energy, range prevents it [2]'),
])


@t7_2.add('C3', (1, 2, 3, 4, 5))
def t7_2_adc(r, D):
    n = r.choice([4, 6, 8, 10, 12])
    vmax = r.choice([5, 10, 3.3]) if D >= 3 else 5
    levels = 1 << n
    reading = r.randrange(1, levels)
    v = vmax * reading / (levels - 1)
    kind = r.choice(['levels', 'volt']) if D >= 3 else 'levels'
    if kind == 'levels':
        stem = f'An ADC uses {n} bits for each sensor reading. How many different values can it produce?'
        if D <= 2:
            return MCQ(r, stem, f'{levels:,}', [f'{n * 2}', f'{levels - 1:,}', f'{levels * 2:,}', f'{n * n}'], f'2^{n} = {levels:,}.')
        return Q(stem + ' Explain the effect of using more bits.', f'{levels:,}; more bits give more levels so a more accurate (higher resolution) reading', f'2^{n} = {levels:,} [1]; smaller step between levels / more accurate [1] [2]', marks=2)
    stem = f'A {n}-bit ADC converts sensor voltages from 0 V to {vmax:g} V, with 0 V giving 0 and {vmax:g} V giving {levels - 1}. A reading of {reading} is produced. Calculate the voltage it represents, to 2 decimal places.'
    return Q(stem, f'{v:.2f} V', f'{reading} ÷ {levels - 1} × {vmax:g} [1] = {v:.2f} V [1] [2]', marks=2)


@t7_2.add('C3', (2, 3, 4), 'numerical')
def t7_2_trace(r, D):
    lo, hi = r.choice([(18, 22), (20, 24), (24, 28), (35, 40), (45, 55)])
    readings = [r.randrange(lo - 4, hi + 5) for _ in range(5 if D < 4 else 7)]
    state = 'OFF'
    acts = []
    for t_ in readings:
        if t_ < lo:
            state = 'ON'
        elif t_ > hi:
            state = 'OFF'
        acts.append(state)
    d = ctx(r)
    stem = (f'A heater in {d["org"]} is switched ON when the temperature is below {lo} and OFF when it is above {hi}; otherwise it stays as it is. It starts OFF. '
            f'For the readings {", ".join(map(str, readings))}, give the state of the heater after each reading.')
    return Q(stem, ', '.join(acts), f'{", ".join(f"{a}→{s}" for a, s in zip(readings, acts))}. 1 mark per 2 correct states [{(len(readings) + 1) // 2}]', marks=(len(readings) + 1) // 2)


scen(t7_2, 'C4', (2, 3, 4, 5), [
    'An automatic irrigation system for a farm near {city} keeps soil moisture between 30% and 40%.',
    'A water tank at {org} uses a level sensor and a pump to keep the tank between 60% and 80% full.',
], [('Explain why an ADC is needed in this system.', 'The sensor produces a continuous analogue voltage; the microprocessor needs digital values.', '1 mark each [2]'),
    ('Describe how feedback is used to keep the value in range.', 'Sensor reading compared with limits; actuator switched on/off; resulting change measured again, affecting next decision.', '1 mark per point, max 3 [3]'),
    ('Explain why the system uses a range rather than one target value.', 'Prevents the actuator switching rapidly on and off, reducing wear and energy use.', '1 mark each [2]'),
    ('Describe what would happen if the sensor became faulty and always gave a low reading.', 'The processor would keep the pump/valve on, overfilling/overwatering; feedback fails.', '1 mark each [2]')], k=(3, 4))

t7_3 = topic('Using bit manipulation to monitor and control devices', 'using bit manipulation to monitor and control devices', 'control devices bits')
t7_3.fixed('C1', (1, 2), [
    ('A control byte uses one bit per device, where 1 means ON. Which operation switches one device ON without changing the others?', 'OR with a mask that has 1 in that bit position', 'OR sets the bit; other bits ORed with 0 are unchanged.', ['AND with that mask', 'XOR with 11111111', 'Shift right by one place']),
    ('Which operation, with a suitable mask, switches one device OFF without changing the others?', 'AND with a mask that has 0 in that bit position and 1 elsewhere', 'AND with 0 clears the bit; AND with 1 keeps the others.', ['OR with a mask that has 0 in that position', 'XOR with 00000000', 'LSL #1']),
    ('Why is a single byte often used to store the status of eight devices?', 'Each bit can represent the on/off state of one device, saving memory', 'One bit per device: compact and fast to test/set with masks.', ['Because each device needs 8 bits', 'Because bytes cannot store numbers', 'To make the program run slower']),
])
t7_3.fixed('C2', (2, 3, 4), [
    ('Explain how a program can test whether a particular sensor flag is set in a status byte.', 'AND the status byte with a mask that has 1 only in that bit position; if the result is non-zero (or equals the mask) the flag is set; then use CMP and a conditional jump.',
     '1 mark: AND with mask; 1 mark: compare result/conditional jump [2]'),
])
DEVICES = ['fan', 'heater', 'lamp', 'pump', 'alarm', 'valve', 'motor', 'buzzer']


@t7_3.add('C3', (1, 2, 3, 4, 5))
def t7_3_ctrl(r, D):
    devs = r.sample(DEVICES, 8)
    v = r.randrange(256)
    i = r.randrange(8)
    task = r.choice(['on', 'off', 'test', 'toggle'])
    m = 1 << (7 - i)
    if task == 'on':
        op, mask, res = 'OR', m, v | m
    elif task == 'off':
        op, mask, res = 'AND', (~m) & 0xFF, v & ~m & 0xFF
    elif task == 'toggle':
        op, mask, res = 'XOR', m, v ^ m
    else:
        op, mask, res = 'AND', m, v & m
    layout = ', '.join(f'bit {k + 1} {d}' for k, d in enumerate(devs))
    word = {'on': 'switch the ' + devs[i] + ' ON', 'off': 'switch the ' + devs[i] + ' OFF', 'test': 'test whether the ' + devs[i] + ' is ON', 'toggle': 'toggle the ' + devs[i]}[task]
    stem = f'A control register holds one bit per device ({layout}; bit 1 is the most significant, 1 = ON). It currently holds {b(v)}. Give the bitwise operation and mask needed to {word}, and the resulting value.'
    ans = f'{op} {b(mask)} → {b(res)}' + ((' (non-zero, so ON)' if res else ' (zero, so OFF)') if task == 'test' else '')
    if D == 1:
        return MCQ(r, stem.replace('Give the bitwise operation and mask needed to', 'Which operation will').replace(', and the resulting value.', '?'), f'{op} {b(mask)}',
                   [f'{o} {b(mm)}' for o, mm in [('AND', m), ('OR', (~m) & 0xFF), ('XOR', (~m) & 0xFF), ('AND', (~m) & 0xFF), ('OR', m), ('XOR', m)] if f'{o} {b(mm)}' != f'{op} {b(mask)}'], f'{op} with {b(mask)}.')
    return Q(stem, ans, f'1 mark operation {op}; 1 mark mask {b(mask)}; 1 mark result {b(res)} [3]', marks=3)


@t7_3.add('C4', (2, 3, 4, 5), 'multi_step')
def t7_3_prog(r, D):
    devs = r.sample(DEVICES, 4)
    v = r.randrange(16)
    a, c = r.sample(range(4), 2)
    ma, mc = 1 << (3 - a), 1 << (3 - c)
    after = (v | ma) & (~mc & 0x0F)
    stem = (f'A greenhouse controller stores the states of four devices in the lower four bits of address 300 (bit 5 = {devs[0]}, bit 6 = {devs[1]}, bit 7 = {devs[2]}, bit 8 = {devs[3]}; bit 8 least significant; 1 = ON). '
            f'Address 300 contains {b(v)}. (a) Write assembly code using LDD, OR, AND and STO to switch the {devs[a]} ON and the {devs[c]} OFF. (b) Give the new contents of address 300. (c) Explain why masks are used rather than storing a new value directly.')
    return Q(stem, f'(a) LDD 300; OR #B{b(ma)}; AND #B{b(~mc & 0xFF)}; STO 300 (b) {b(after)} (c) only the chosen bits change; other devices keep their current state',
             f'(a) LDD and STO [1]; OR #B{b(ma)} [1]; AND #B{b(~mc & 0xFF)} [1] (b) {b(after)} [1] (c) [1]', marks=5, typ='multi_step')


@t7_3.add('C2', (2, 3, 4), 'explain')
def t7_3_err(r, D):
    v = r.randrange(256)
    i = r.randrange(8)
    m = 1 << (7 - i)
    d = ctx(r)
    return Q(f'{d["p"]} wants to switch OFF only the device controlled by bit {i + 1} (bit 1 most significant) of the value {b(v)}, and uses AND #B{b(m)}. Explain the problem and give the correct mask.',
             f'AND with {b(m)} clears every bit except bit {i + 1}, so all other devices are switched off. The mask should be {b(~m & 0xFF)} (0 in bit {i + 1}, 1 elsewhere), giving {b(v & ~m & 0xFF)}.',
             f'1 mark: explains other bits cleared; 1 mark: correct mask {b(~m & 0xFF)} [2]')


CHAPTERS[7] = [t7_1, t7_2, t7_3]

# =============================================================================== Chapter 8 System software
t8_1 = topic('Operating system functions: memory, file, security, hardware and process management; user interface', 'operating system functions', 'memory management', 'process management', 'user interface')
t8_1.fixed('C1', (1, 2), [
    ('Why does a computer need an operating system?', 'To provide an interface between the user/applications and the hardware and to manage resources', 'OS: manages hardware, memory, files, processes and security; provides a user interface and platform for applications.',
     ['To translate programs into machine code', 'To stop the computer being hacked', 'To compress files automatically']),
    ('Which OS function allocates RAM to programs and prevents them overwriting each other?', 'Memory management', 'Memory management: allocation, protection, virtual memory.', ['File management', 'Hardware management', 'Process management']),
    ('Which OS function uses device drivers to communicate with peripherals?', 'Hardware (peripheral) management', 'Device drivers translate OS requests into device-specific commands.', ['Security management', 'Memory management', 'File management']),
    ('What is a GUI?', 'A user interface that uses windows, icons, menus and a pointer', 'GUI (WIMP): easy for beginners; uses more resources than a CLI.', ['A command-line interface', 'A type of compiler', 'A network protocol']),
    ('Which OS function schedules which program gets processor time?', 'Process management', 'Process management: scheduling, multitasking, handling interrupts, resource allocation.', ['File management', 'User interface', 'Security management']),
    ('Which OS function provides user accounts and passwords?', 'Security management', 'Security management: user accounts, access rights, firewalls, updates.', ['Hardware management', 'Memory management', 'Process management']),
    ('What is a command-line interface?', 'An interface where the user types text commands', 'CLI: needs knowledge of commands; uses few resources; powerful for scripting.', ['An interface operated by touch', 'An interface with icons', 'A voice-only interface']),
])
t8_1.fixed('C2', (2, 3, 4), [
    ('Describe two tasks carried out by the file management function of an operating system.', 'Organises files in a directory/folder structure; controls naming, creation, deletion, copying, moving; manages access rights to files; allocates storage space on disk.', '1 mark per task, max 2 [2]'),
    ('Explain why a network technician might prefer a command-line interface to a GUI.', 'Commands can be combined and scripted to automate tasks; direct access to settings; uses fewer resources; works remotely over slow links.', '1 mark per point, max 2 [2]'),
    ('Explain how the operating system allows several programs to appear to run at the same time on one processor core.', 'Process management/scheduling gives each process a short time slice in turn; interrupts switch between them; this happens so fast that they appear simultaneous.', '1 mark: time slices/scheduling; 1 mark: rapid switching via interrupts [2]'),
    ('Describe the role of memory management.', 'Allocates memory to processes and frees it when they end; prevents one process using another\'s memory (protection); manages virtual memory/paging when RAM is full.', '1 mark per point, max 3 [3]'),
])
scen(t8_1, 'C3', (2, 3, 4), [
    '{p} uses a laptop at {org} to run a web browser, a spreadsheet and a music player at the same time.',
    '{org} in {city} is installing an operating system on 50 new office computers.',
    'A new printer is connected to the computer of {p}.',
], [('Identify the OS function that ensures each program has its own area of RAM, and explain why this is needed.', 'Memory management: protects programs from overwriting each other\'s data and crashing.', '1 mark function; 1 mark reason [2]'),
    ('Explain how the OS enables the new printer to be used.', 'Hardware management installs/loads the device driver, which translates OS commands into printer commands; manages the print queue/buffer.', '1 mark driver; 1 mark explanation [2]'),
    ('Describe how the OS keeps each user\'s files private.', 'User accounts with passwords; access rights/permissions for files and folders.', '1 mark each [2]'),
    ('State two features of the GUI that help a new user.', 'Icons, menus, windows, pointer, help screens, drag and drop.', '1 mark each [2]'),
    ('Explain why the OS must handle interrupts.', 'Devices and programs signal events; OS responds by running ISRs and scheduling, ensuring urgent events are dealt with.', '1 mark each [2]')], k=(2, 3))
essay(t8_1, [('whether a GUI or a command-line interface is more suitable for the staff at {org}', 'GUI: intuitive, little training, visual, suitable for most office staff; CLI: fast for experts, scriptable, low resources, remote use.',
              'GUI uses more memory/processing and hides advanced options; CLI needs commands to be learned and errors are easy to make.', 'GUI for general staff, CLI for technical administrators.')],
      ['{org} in {city} is choosing the user interface for its computers.', 'The IT team at {org} is writing a policy on computer use.'])

t8_2 = topic('Utility software: disk formatter, virus checker, defragmenter, compression and back-up; program libraries and DLLs', 'utility software', 'defragmenter', 'program libraries', 'dlls')
t8_2.fixed('C1', (1, 2), [
    ('What does a disk defragmenter do?', 'Rearranges the parts of files on a hard disk so each file is stored in contiguous blocks', 'Defragmentation reduces read-head movement, speeding up file access on HDDs.', ['Deletes all files on a disk', 'Checks for viruses', 'Compresses all files']),
    ('What does disk formatting do?', 'Prepares a storage device for use by setting up a file system, removing existing data', 'Formatting creates tracks/sectors/file system structures.', ['Sorts files into alphabetical order', 'Encrypts the disk', 'Repairs physically damaged sectors']),
    ('What is a program library?', 'A collection of pre-written, tested routines that programmers can use', 'Libraries save development time; routines are already tested.', ['A list of installed applications', 'A folder of user documents', 'A database of viruses']),
    ('What is a DLL?', 'A library file that is linked to a program when the program runs', 'Dynamic link library: loaded at run time, shared by many programs.', ['A library that is copied into the executable when it is compiled', 'A type of virus', 'A disk utility']),
    ('Why should defragmentation not normally be run on an SSD?', 'Access time does not depend on the physical position of data, and extra writes reduce the SSD\'s lifespan', 'SSDs have no moving head; writes wear flash cells.', ['SSDs cannot store files', 'It would delete the operating system', 'SSDs are always full']),
    ('How does a virus checker detect known viruses?', 'By comparing files with a database of virus signatures', 'Signature-based detection; heuristic checking looks for suspicious behaviour.', ['By checking the file size only', 'By defragmenting the disk', 'By formatting the disk']),
])
t8_2.fixed('C2', (2, 3, 4), [
    ('Explain why defragmenting a hard disk drive can improve performance.', 'Fragmented files are spread across the disk so the read head must move many times; after defragmentation each file is in contiguous sectors, so fewer head movements and faster access.',
     '1 mark: fragments scattered; 1 mark: head movement/seek time reduced; 1 mark: faster access [3]'),
    ('Give two advantages and one disadvantage of using DLL files.', 'Advantages: executable files are smaller; many programs share one copy in memory; library can be updated without recompiling programs. Disadvantage: program fails if the DLL is missing or an incompatible version is installed.',
     '1 mark per point, max 3 [3]'),
    ('Explain why an organisation should make regular back-ups and store a copy off site.', 'Data can be restored if lost through hardware failure, malware, accidental deletion or fire/theft; off-site copy survives a disaster at the main site.', '1 mark: restore after loss with cause; 1 mark: off-site protects against disaster [2]'),
    ('Explain two benefits to a programmer of using library routines.', 'Saves time as code does not need writing; routines are already tested so fewer errors; written by experts so efficient.', '1 mark each [2]'),
])
scen(t8_2, 'C3', (2, 3, 4), [
    'The computers at {org} in {city} have become slow and some files are being lost.',
    '{p} is responsible for maintaining the computers at a small office.',
    'A programmer at {org} is writing an application that needs complex mathematical functions.',
], [('Recommend a utility to speed up file access on the hard disk and explain how it works.', 'Defragmenter: moves file fragments into contiguous blocks so less head movement.', '1 mark utility; 2 marks explanation [3]'),
    ('Describe a back-up strategy for the office.', 'Full back-up weekly and incremental daily; automatic; copy stored off site/cloud; tested restores.', '1 mark per point, max 3 [3]'),
    ('Explain how a virus checker protects the computers.', 'Scans files against virus signatures; heuristic checks; quarantines/deletes infected files; real-time scanning; needs regular updates.', '1 mark per point, max 3 [3]'),
    ('Explain why the programmer would use a library of mathematical routines.', 'Saves development time; pre-tested and reliable.', '1 mark each [2]'),
    ('Explain how file compression helps when emailing large reports.', 'Smaller file size so faster to send and within attachment limits.', '1 mark each [2]')], k=(2, 3))
ar(t8_2, [('Defragmentation can speed up access to files on a hard disk drive.', 'After defragmentation, the parts of each file are stored in contiguous sectors, reducing read-head movement.'),
          ('Programs that use DLLs have smaller executable files.', 'DLL routines are linked when the program runs rather than copied into the executable.'),
          ('A virus checker must be updated regularly.', 'New viruses are created all the time and their signatures must be added to the database.')],
   ['Formatting a disk removes fragmentation without losing data.', 'A DLL is copied into the program when it is compiled.', 'Defragmenting an SSD increases its lifespan.'])

t8_3 = topic('Language translators: assembler, compiler and interpreter; advantages and disadvantages', 'language translators', 'compiler and interpreter')
t8_3.fixed('C1', (1, 2), [
    ('What does a compiler do?', 'Translates the whole high-level program into machine code before it is run', 'Compiler produces an executable file; errors reported after the whole program is translated.', ['Translates and executes one line at a time', 'Translates assembly language into machine code', 'Checks files for viruses']),
    ('What does an interpreter do?', 'Translates and executes a high-level program one statement at a time', 'Interpreter stops at the first error; no executable produced.', ['Produces an executable file', 'Translates assembly language', 'Links library routines into a program']),
    ('Which translator is needed every time an interpreted program is run?', 'The interpreter', 'No object code is saved, so the source code and interpreter are needed each time.', ['The compiler', 'The assembler', 'The linker']),
    ('Which statement about compiled programs is correct?', 'They usually run faster than interpreted programs', 'Translation is done once in advance; execution does not include translation.', ['They need the source code to run', 'They are translated each time they run', 'They stop at the first error while running']),
    ('Why are Java programs sometimes described as partially compiled and partially interpreted?', 'They are compiled to intermediate bytecode, which is then interpreted by a virtual machine', 'Bytecode is portable; the JVM interprets (or JIT-compiles) it.', ['They are compiled twice', 'They are written in assembly language', 'They do not need a translator']),
])
t8_3.fixed('C2', (2, 3, 4), [
    ('Explain why an interpreter is useful when a program is being developed.', 'Errors are reported as soon as the line is reached, so they can be corrected and the program continued immediately; parts of the program can be tested without translating everything.',
     '1 mark: stops at error, easy to locate; 1 mark: test partial programs / no recompiling [2]'),
    ('Explain why a software company distributes its finished product as compiled code.', 'Compiled code runs without the translator and faster; the source code is not given to users so it is protected from copying or alteration.', '1 mark: no translator needed/faster; 1 mark: source code protected [2]'),
    ('Compare a compiler and an interpreter in terms of how errors are reported.', 'A compiler reports all errors found after translating the whole program; an interpreter stops at the first error it meets.', '1 mark each [2]'),
])
scen(t8_3, 'C3', (2, 3, 4), [
    '{p} is learning to program and writing short programs at school.',
    '{org} in {city} is about to sell a game it has developed.',
    'A team at {org} is developing a large application that takes several minutes to translate.',
], [('Recommend a compiler or an interpreter for this situation and justify your choice.', 'Interpreter for learning/development (immediate error feedback); compiler for distribution (fast, protected, no translator needed).', '1 mark choice; 2 marks justification [3]'),
    ('Give one advantage of an interpreter for this situation.', 'Errors found line by line; easier debugging; no waiting for full compilation.', '1 mark [1]'),
    ('Give one disadvantage of an interpreter for this situation.', 'Slower execution; source code must be distributed; interpreter needed on each machine.', '1 mark [1]'),
    ('Explain the role of an IDE\'s translator in finding syntax errors.', 'The translator checks statements against the language rules and reports errors with line numbers.', '1 mark each [2]')], k=(2, 3))
essay(t8_3, [('the use of a compiler rather than an interpreter by {org} for its new commercial software', 'compiled code runs faster; no translator needed by customers; source code is protected; all errors listed at once.',
              'compilation of large programs can be slow during development; executables are platform-specific; harder debugging than with an interpreter.', 'use an interpreter or IDE debugging during development and a compiler for the final release.')],
      ['{org} in {city} is developing software that it will sell to customers.', '{p} leads a software project at {org}.'])

t8_4 = topic('Integrated development environment features: prettyprint, context-sensitive prompts, debugging tools', 'integrated development environment', 'prettyprint', 'debugging tools')
t8_4.fixed('C1', (1, 2), [
    ('What is prettyprint in an IDE?', 'Displaying code with colour-coded keywords and automatic indentation', 'Prettyprinting improves readability: keywords, strings, comments shown in different colours; indentation.', ['Printing code on paper', 'Removing all comments', 'Compressing the source code']),
    ('What is a breakpoint?', 'A point where execution is paused so values can be examined', 'Breakpoints stop the program at a chosen line during debugging.', ['A syntax error', 'The end of the program', 'A point where the program is compiled']),
    ('What does single stepping do?', 'Executes the program one statement at a time', 'Lets the programmer watch the effect of each line.', ['Runs the whole program at full speed', 'Removes one line of code', 'Compiles one module only']),
    ('What is a context-sensitive prompt?', 'A suggestion of possible keywords, variables or parameters based on what is being typed', 'Autocomplete/intellisense shows options valid in the current context.', ['An error message from the compiler', 'A pop-up advert in the IDE', 'A message that the program has finished']),
    ('What does a variable watch window show?', 'The current values of chosen variables while the program runs', 'Report window/watch window shows variable contents as code executes or at breakpoints.', ['The list of files in the project', 'The machine code', 'The program\'s output only']),
    ('What is dynamic syntax checking?', 'Syntax errors are highlighted as code is typed', 'Errors underlined immediately, before translation.', ['Checking the program while it runs on test data', 'Checking the logic of an algorithm', 'Checking spelling of comments only']),
])
t8_4.fixed('C2', (2, 3, 4), [
    ('Explain how breakpoints and a variable watch window can be used together to find a logic error.', 'Set a breakpoint just before the suspected error; when execution pauses, inspect variable values in the watch window and compare with expected values; step through to see where they first go wrong.',
     '1 mark: breakpoint pauses at chosen line; 1 mark: inspect variables; 1 mark: compare with expected / single step to locate [3]'),
    ('Explain how expanding and collapsing code blocks helps a programmer.', 'Large programs are easier to navigate; the programmer can hide finished modules and focus on the part being written.', '1 mark each [2]'),
])
scen(t8_4, 'C3', (2, 3, 4), [
    '{p} is using an IDE to write a program for {org}. The program runs but gives the wrong total.',
    'A student at {org} is using an IDE to develop a program that adds up sales figures; it runs but the total is wrong.',
], [('Describe two IDE features that help when writing code.', 'Context-sensitive prompts (autocomplete), prettyprint, dynamic syntax checking, expand/collapse blocks.', '1 mark each [2]'),
    ('Describe how the IDE could be used to find where the total goes wrong.', 'Breakpoints and variable watch; single stepping through the loop; compare values with a trace table.', '1 mark per point, max 3 [3]'),
    ('Explain why prettyprint reduces errors.', 'Colour and indentation show structure clearly so missing ENDIF/ENDWHILE or wrong nesting is easier to see.', '1 mark each [2]'),
    ('State one feature of an IDE that helps with syntax errors.', 'Dynamic syntax checking / error highlighting with line numbers.', '1 mark [1]')], k=(2, 3))
scen(t8_4, 'C4', (3, 4, 5), [
    '{org} is choosing an IDE for its team of programmers in {city}.',
], [('Explain how an IDE helps during the coding stage.', 'Prettyprint, autocomplete, syntax checking, code templates.', '1 mark per feature explained, max 3 [3]'),
    ('Explain how an IDE helps during testing and debugging.', 'Breakpoints, single stepping, variable watch, report windows.', '1 mark per feature explained, max 3 [3]'),
    ('Evaluate whether it is worth paying for a commercial IDE rather than using a free text editor.', 'IDE saves time and reduces errors with integrated tools; cost and learning curve; free IDEs exist.', '1 mark each side; 1 mark conclusion [3]')], k=(2, 3))

essay(t8_2, [('the utility software and back-up procedures that {org} should use', 'virus checker protects against malware; defragmenter speeds up HDD access; compression saves storage and transmission time; regular full and incremental back-ups with off-site copies allow recovery.',
              'utilities use processing time and may slow computers while running; back-ups need storage and must be tested; defragmenting SSDs is harmful.', 'a scheduled maintenance plan run out of hours gives protection with little disruption.'),
             ('the use of dynamic link libraries rather than static libraries in the software written by {org}', 'smaller executables; shared memory use; library updates without recompiling.',
              'missing or incompatible DLL versions stop programs running; harder to distribute a single self-contained file.', 'DLLs suit large systems with many programs; static linking suits standalone tools.')],
      ['{org} in {city} has 200 computers and a file server.', '{p} is the IT technician at {org}.'])

CHAPTERS[8] = [t8_1, t8_2, t8_3, t8_4]

# =============================================================================== Chapter 9 Security, privacy and data integrity
THREATS = [('malware', 'software designed to damage a system or gain unauthorised access, e.g. viruses, worms, spyware, ransomware'),
           ('hacking', 'gaining unauthorised access to a computer system'),
           ('phishing', 'sending emails that appear to be from a trusted source to trick users into giving personal data'),
           ('pharming', 'malicious code that redirects a user from a genuine website to a fake one to capture personal data'),
           ('spyware', 'software that secretly records user activity such as key presses and sends it to a third party'),
           ('a worm', 'malware that replicates itself across a network without needing to attach to a file'),
           ('ransomware', 'malware that encrypts a user\'s files and demands payment for the key'),
           ('a denial of service attack', 'flooding a server with requests so that genuine users cannot access it')]
t9_1 = topic('Security of data and systems: threats such as malware, hacking, phishing and pharming', 'security of data and systems', 'malware', 'phishing', 'pharming')
t9_1.fixed('C1', (1, 2), [(f'What is meant by {n}?', d[0].upper() + d[1:], f'{n}: {d}.', [x[1][0].upper() + x[1][1:] for x in THREATS if x[0] != n][:5]) for n, d in THREATS] + [
    ('What is the difference between data security and data privacy?', 'Security protects data from loss or corruption; privacy keeps data available only to those authorised to see it', 'Security: protection; privacy: who may see it.',
     ['They mean the same thing', 'Privacy protects against viruses; security protects against people', 'Security is only about passwords']),
])
t9_1.fixed('C2', (2, 3, 4), [
    ('Explain the difference between phishing and pharming.', 'Phishing relies on the user clicking a link in a fake email; pharming uses malicious code/DNS poisoning to redirect the user to a fake website even when the correct address is typed.',
     '1 mark: phishing — email/link from apparently trusted source; 1 mark: pharming — redirection without user action [2]'),
    ('Explain how a virus differs from a worm.', 'A virus attaches to a file/program and needs the user to run it to spread; a worm is standalone and replicates itself across networks automatically.', '1 mark each [2]'),
    ('Explain why a hacker might target a company\'s customer database.', 'To steal personal or financial data for fraud or identity theft, to sell it, or to hold it to ransom.', '1 mark motive; 1 mark consequence [2]'),
])
scen(t9_1, 'C3', (2, 3, 4), [
    'Staff at {org} in {city} have received an email that appears to come from their bank asking them to confirm their password.',
    'Customers of {org} report that the company website looks slightly different and asks for card details twice.',
    'Files on the computers at {org} have been encrypted and a message demands payment.',
], [('Identify the threat and explain how it works.', 'Phishing / pharming / ransomware, with correct description.', '1 mark threat; 2 marks description [3]'),
    ('Describe two signs that should make the user suspicious.', 'Spelling errors; generic greeting; urgent request; unexpected attachment; URL not matching; no HTTPS padlock.', '1 mark each [2]'),
    ('Describe two actions the organisation should take to reduce the risk.', 'Staff training; email filters; anti-malware; firewall; regular backups; 2FA.', '1 mark each [2]'),
    ('Explain the possible consequences for the organisation.', 'Data stolen/lost; financial loss; reputational damage; legal penalties; downtime.', '1 mark per point, max 2 [2]')], k=(2, 3))

essay(t9_1, [('the threats to the data held by {org} and how serious each is', 'malware can corrupt or encrypt data; hacking can steal customer data; phishing and pharming target staff and customers to obtain passwords.',
              'the likelihood of each threat depends on staff awareness and existing defences; some threats are reduced by back-ups and training.', 'phishing is often the most serious because it bypasses technical defences through people.')],
      ['{org} in {city} stores the personal details of 50 000 customers.', '{p} has been asked to brief the directors of {org} on cyber threats.'])

t9_2 = topic('Security measures: user accounts, passwords, firewalls, encryption, anti-malware, access rights', 'security measures', 'firewalls', 'encryption', 'access rights')
t9_2.fixed('C1', (1, 2), [
    ('What does a firewall do?', 'Monitors and filters network traffic, blocking data that does not meet set rules', 'Firewall checks packets against rules (IP addresses, ports), blocks unauthorised access.', ['Removes viruses from files', 'Encrypts all data on a disk', 'Backs up data']),
    ('What is the purpose of encryption?', 'To make intercepted data unreadable without the key', 'Encryption does not stop interception; it stops data being understood.', ['To stop data being intercepted', 'To compress data', 'To detect viruses']),
    ('What are access rights?', 'Permissions that control what each user can view or change', 'e.g. read-only, read/write, no access to certain files/folders.', ['The passwords of all users', 'The right to buy software', 'Copyright permissions']),
    ('What is two-factor authentication?', 'Requiring two different types of evidence of identity, e.g. a password and a code sent to a phone', 'Something you know + something you have/are.', ['Using two passwords', 'Logging in twice', 'Using a firewall and anti-virus']),
    ('Which is an example of biometric security?', 'Fingerprint recognition', 'Biometrics: fingerprint, face, iris, voice.', ['A strong password', 'A firewall', 'An encrypted file']),
    ('What is a proxy server used for in network security?', 'Acting as an intermediary that hides internal IP addresses and filters web requests', 'A proxy server acts as an intermediary between users and the internet.', ['Encrypting files on a disk', 'Formatting disks', 'Checking spelling']),
])
t9_2.fixed('C2', (2, 3, 4), [
    ('Explain why a strong password policy improves security.', 'Long passwords with mixed character types are harder to guess or crack by brute force; regular changes limit damage if one is stolen.', '1 mark: harder to guess/crack; 1 mark: rule explained [2]'),
    ('Explain why encryption does not prevent data being intercepted.', 'Encryption scrambles the data so it is meaningless without the key, but the data can still be captured in transit.', '1 mark each [2]'),
    ('Describe how a firewall protects a network.', 'It sits between the network and the internet; examines incoming and outgoing packets against rules (addresses, ports, protocols); blocks unauthorised traffic and logs attempts.', '1 mark per point, max 3 [3]'),
])
scen(t9_2, 'C3', (2, 3, 4), [
    '{org} in {city} stores medical and payment data about its customers.',
    '{p} manages the network for {org}, where staff work from home and in the office.',
], [('Describe how access rights could be used.', 'Different groups of staff given read-only, read/write or no access to particular files depending on their job.', '1 mark each point, max 2 [2]'),
    ('Explain why data sent between home and office should be encrypted.', 'If intercepted it cannot be understood without the key; protects confidential data.', '1 mark each [2]'),
    ('Describe two measures to protect the network from malware.', 'Anti-malware with updated signatures; firewall; restricting downloads/USB; staff training; OS updates.', '1 mark each [2]'),
    ('Suggest a password policy.', 'Minimum length/complexity; regular changes; no reuse; lock-out after failed attempts; 2FA.', '1 mark per rule, max 3 [3]'),
    ('Explain the benefit of two-factor authentication.', 'Even if the password is stolen, the attacker also needs the second factor (phone/biometric).', '1 mark each [2]')], k=(2, 3))
essay(t9_2, [('the security measures {org} should use to protect its customer data', 'user accounts and strong passwords with 2FA; access rights by role; firewall; encryption of stored and transmitted data; anti-malware; back-ups.',
              'measures cost money and staff time; strong rules may annoy users who then write passwords down; no measure is complete without staff training.', 'a layered approach with training gives the best protection.')],
      ['{org} in {city} has recently suffered a data breach.', 'The managers of {org} have asked {p} to review security.'])

t9_3 = topic('Data integrity: validation (range, format, length, presence, existence, check digit) and verification (double entry, parity, checksums)', 'data integrity', 'validation', 'verification', 'check digit', 'parity')
t9_3.fixed('C1', (1, 2), [
    ('What is validation?', 'A check by the computer that data is reasonable and meets set rules', 'Validation cannot ensure data is correct, only sensible/allowed.', ['A check that data has been copied accurately', 'Encrypting data', 'Removing duplicate data']),
    ('What is verification?', 'A check that data has been accurately entered or transferred', 'e.g. double entry, visual check, parity, checksum.', ['A check that data is within a range', 'A check that a field is not empty', 'Scanning for malware']),
    ('Which check makes sure that a field has not been left blank?', 'Presence check', 'Presence check: data must be entered.', ['Range check', 'Format check', 'Length check']),
    ('Which check would ensure a date is entered as DD/MM/YYYY?', 'Format check', 'Format (picture) check: data matches a pattern.', ['Range check', 'Existence check', 'Presence check']),
    ('Which validation check makes sure an entered product code is one that is stored in the database?', 'Existence check', 'Existence (lookup) check: value must exist in a list or file.', ['Length check', 'Format check', 'Range check']),
    ('In even parity, what is true of each byte?', 'The total number of 1 bits is even', 'The parity bit is chosen so the count of 1s (including the parity bit) is even.', ['The value is an even number', 'The last bit is always 0', 'There are always four 1 bits']),
    ('Why can parity checking fail to detect an error?', 'If two bits are changed, the parity is still correct', 'An even number of bit errors keeps the parity unchanged.', ['Parity bits are never transmitted', 'Parity only works with letters', 'The parity bit is always 1']),
])
t9_3.fixed('C2', (2, 3, 4), [
    ('Explain why validation cannot guarantee that data is correct.', 'Validation only checks data is reasonable/within rules; a wrong value that is still within the rules (e.g. age 34 instead of 43) is accepted.', '1 mark: only checks rules; 1 mark: example of valid but wrong data [2]'),
    ('Describe how double entry is used as a verification method.', 'The data is entered twice (e.g. a new password); the computer compares the two entries and asks for re-entry if they differ.', '1 mark each [2]'),
    ('Explain how a checksum is used to verify data after transmission.', 'The sender calculates a value from the data block and sends it; the receiver recalculates it; if the values differ, an error has occurred and the data is re-sent.', '1 mark per point, max 3 [3]'),
    ('Explain how a parity block can identify which bit is wrong.', 'Parity bits are added to each byte (row) and each bit position (column); a single error makes one row and one column fail; the bit where they cross is wrong and can be flipped.', '1 mark: row and column parity; 1 mark: intersection identifies bit [2]'),
])


def mod11(digits):
    w = list(range(len(digits) + 1, 1, -1))
    s = sum(d * k for d, k in zip(digits, w))
    c = (11 - s % 11) % 11
    return s, w, c


@t9_3.add('C3', (1, 2, 3, 4, 5))
def t9_3_parity(r, D):
    data = [r.randrange(2) for _ in range(7)]
    kind = r.choice(['even', 'odd'])
    ones = sum(data)
    pb = (ones % 2) if kind == 'even' else (1 - ones % 2)
    s = ''.join(map(str, data))
    if D <= 2 or r.random() < 0.4:
        stem = f'The 7-bit data {s} is to be sent using {kind} parity, with the parity bit as the most significant bit. Give the 8-bit byte that is sent.'
        ans = f'{pb}{s}'
        key = f'{ones} ones in the data; parity bit {pb} makes the total {"even" if kind == "even" else "odd"} [1]'
        if D == 1:
            return MCQ(r, stem.replace('Give the 8-bit byte that is sent.', 'Which byte is sent?'), ans, [f'{1 - pb}{s}', f'{s}{pb}', f'{pb}{s[::-1]}' if s[::-1] != s else f'{pb}{s[:-1]}{1 - data[-1]}'], key.replace(' [1]', ''))
        return Q(stem, ans, key)
    # received bytes, find the error
    bytes_ = []
    for _ in range(4):
        dd = [r.randrange(2) for _ in range(7)]
        p_ = (sum(dd) % 2) if kind == 'even' else 1 - sum(dd) % 2
        bytes_.append([p_] + dd)
    bad = r.randrange(4)
    bit = r.randrange(8)
    bytes_[bad][bit] ^= 1
    shown = ', '.join(''.join(map(str, x)) for x in bytes_)
    stem = f'Four bytes are received using {kind} parity: {shown}. Identify the byte that contains an error and explain how you know.'
    return Q(stem, f'Byte {bad + 1} ({"".join(map(str, bytes_[bad]))}): it has {sum(bytes_[bad])} ones, which is {"odd" if sum(bytes_[bad]) % 2 else "even"}, but {kind} parity is used.',
             f'1 mark: byte {bad + 1}; 1 mark: counts 1s and compares with {kind} parity [2]', marks=2)


@t9_3.add('C3', (2, 3, 4, 5), 'numerical')
def t9_3_check(r, D):
    n = r.randrange(4, 7)
    for _ in range(20):
        digs = [r.randrange(10) for _ in range(n)]
        s, w, c = mod11(digs)
        if c != 10:
            break
    else:
        return None
    code_ = ''.join(map(str, digs))
    if r.random() < 0.5:
        stem = f'A product code uses a modulo-11 check digit. Each digit is multiplied by a weight, starting at {n + 1} for the leftmost digit and decreasing by 1; the products are added; the check digit is (11 − (total MOD 11)) MOD 11. Calculate the check digit for {code_}.'
        key = ' + '.join(f'{d}×{k}' for d, k in zip(digs, w)) + f' = {s} [1]; {s} MOD 11 = {s % 11} [1]; check digit = {c} [1] [3]'
        return Q(stem, str(c), key, marks=3)
    wrong = (c + r.randrange(1, 10)) % 11
    if wrong == 10:
        wrong = (c + 1) % 10
    ok = r.random() < 0.5
    given = c if ok else wrong
    stem = f'A code {code_}{given} ends with a modulo-11 check digit (weights {n + 1} down to 2 for the first {n} digits; check digit = (11 − (total MOD 11)) MOD 11). Determine whether the code is valid.'
    return Q(stem, ('Valid' if ok else f'Invalid: the check digit should be {c}, not {given}'), ' + '.join(f'{d}×{k}' for d, k in zip(digs, w)) + f' = {s} [1]; check digit {c} [1]; comparison and conclusion [1] [3]', marks=3)


VALID_FIELDS = [('age of a student in years', 'range check (e.g. 11 to 19)', 'range'), ('date of birth', 'format check DD/MM/YYYY (and range)', 'format'),
                ('customer surname', 'presence check (and length check)', 'presence'), ('telephone number', 'length check / format check (digits only)', 'length'),
                ('product code', 'existence (lookup) check against the product file', 'existence'), ('ISBN of a book', 'check digit', 'check digit'),
                ('percentage mark in a test', 'range check 0 to 100', 'range'), ('email address', 'format check (contains @ and a dot)', 'format'),
                ('membership number', 'length check / check digit', 'length'), ('country of residence', 'existence check against a list of countries', 'existence')]


@t9_3.add('C3', (1, 2, 3))
def t9_3_pick(r, D):
    f = r.choice(VALID_FIELDS)
    d = ctx(r)
    if D <= 2:
        return MCQ(r, f'{d["org"]} is designing a data entry form. Which validation check is most appropriate for the field "{f[0]}"?', f[2] + ' check' if f[2] != 'check digit' else 'check digit',
                   [x + ' check' for x in ['range', 'format', 'presence', 'length', 'existence'] if x != f[2]] + (['check digit'] if f[2] != 'check digit' else []), f'{f[0]}: {f[1]}.')
    g = r.choice([x for x in VALID_FIELDS if x != f])
    return Q(f'{d["org"]} is designing a data entry form. Identify a suitable validation check for "{f[0]}" and for "{g[0]}", and describe each check.',
             f'{f[0]}: {f[1]}; {g[0]}: {g[1]}', '1 mark per correct check, 1 mark per description [4]', marks=4)


scen(t9_3, 'C4', (2, 3, 4, 5), [
    '{org} in {city} enters customer orders into a database and sends them to a warehouse over a network.',
    'Staff at {org} type orders from paper forms into a new computer system and send them to a warehouse over a network.',
], [('Explain the difference between validation and verification in this context.', 'Validation: the system checks entered data follows rules; verification: checks the data entered/transferred matches the original.', '1 mark each [2]'),
    ('Describe two validation checks the order form should use.', 'e.g. range check on quantity, existence check on product code, presence check on customer ID, format check on date.', '1 mark each with field [2]'),
    ('Describe how data is verified when it is sent to the warehouse.', 'Parity checks / checksums calculated by sender and receiver; if mismatch, data re-sent (ARQ).', '1 mark per point, max 3 [3]'),
    ('Explain why double entry might be used when staff type in data.', 'Typing errors are detected because two independent entries are unlikely to contain the same mistake.', '1 mark each [2]'),
    ('Explain one limitation of parity checks.', 'They cannot detect an even number of bit errors and cannot correct errors (unless a parity block is used).', '1 mark [1]')], k=(3, 4))

CHAPTERS[9] = [t9_1, t9_2, t9_3]

# =============================================================================== Chapter 10 Ethics and ownership
t10_1 = topic('Professional ethics and codes of conduct (BCS, IEEE)', 'professional ethics', 'codes of conduct', 'bcs', 'ieee')
t10_1.fixed('C1', (1, 2), [
    ('What is meant by ethics in computing?', 'Moral principles that guide the behaviour of computing professionals', 'Ethics: what is right/wrong in professional conduct.', ['The laws about copyright', 'Rules of a programming language', 'The speed of a computer']),
    ('What does BCS stand for?', 'British Computer Society (The Chartered Institute for IT)', 'BCS has a code of conduct for IT professionals.', ['British Computer Software', 'Binary Coded Systems', 'Basic Computer Standards']),
    ('Which is a principle in the BCS code of conduct?', 'Act in the public interest', 'BCS principles: public interest, professional competence and integrity, duty to relevant authority, duty to the profession.', ['Always maximise profit', 'Never share knowledge', 'Work only on open-source software']),
    ('What is the IEEE?', 'A professional organisation for engineers, including computer engineers, with its own code of ethics', 'Institute of Electrical and Electronics Engineers; ACM/IEEE Software Engineering Code of Ethics.', ['A government law on computing', 'A type of encryption', 'A programming language']),
    ('Why do professional bodies publish codes of conduct?', 'To set standards of professional behaviour that members are expected to follow', 'Codes guide decisions and protect the public and the reputation of the profession.', ['To make software cheaper', 'To replace the law', 'To advertise products']),
])
t10_1.fixed('C2', (2, 3, 4), [
    ('Explain why a software engineer should only accept work they are competent to do.', 'Lack of competence could lead to faulty software that harms clients or the public; the code requires professional competence and honesty about limitations.', '1 mark: risk of harm/poor work; 1 mark: duty of competence/integrity [2]'),
    ('Explain one way in which acting in the public interest might conflict with an employer\'s wishes.', 'An employer may want to release software quickly with known safety or security flaws; the engineer\'s duty to the public requires the risk to be reported or the release delayed.', '1 mark: example conflict; 1 mark: public interest outweighs employer [2]'),
])
items(t10_1, 'C3', (2, 3, 4), [
    ('{p} works for {org} and discovers that the software being shipped to hospitals has a bug that could cause wrong medicine doses. Explain, with reference to a professional code of conduct, what {p} should do.',
     '{p} should report the bug to managers and refuse to sign off the release until it is fixed; if ignored, escalate to the relevant authority. The code requires acting in the public interest and protecting health and safety.',
     '1 mark: report/raise concern; 1 mark: not release; 1 mark: links to public interest/safety principle [3]'),
    ('A manager at {org} asks {p} to copy code from a competitor\'s product found online. Explain why this is unethical and what {p} should do.',
     'It breaches copyright and professional integrity; {p} should refuse, explain the legal and ethical issues and suggest writing original code or licensing the code.',
     '1 mark: copyright/integrity; 1 mark: refuse/explain; 1 mark: alternative [3]'),
    ('{p} is asked to collect more personal data from users of an app made by {org} than the app needs. Discuss the ethical issues involved.',
     'Privacy of users, informed consent, data protection law; the code requires respect for privacy and acting in the public interest; {p} should challenge the request and collect only necessary data.',
     '1 mark per relevant issue, max 3 [3]'),
    ('{p} is offered a gift by a supplier while choosing software for {org}. Explain why accepting it could breach a code of conduct.',
     'It creates a conflict of interest and may bias the decision; codes require integrity and honest, impartial judgement in the employer\'s interest.',
     '1 mark: conflict of interest; 1 mark: integrity/impartiality [2]'),
])
essay(t10_1, [('the importance of professional codes of conduct for programmers working on safety-critical systems', 'codes require competence, honesty, public interest; reduce risks to life; maintain public trust; guide difficult decisions.',
               'codes are not legally binding; membership is voluntary; commercial pressure may override them; codes are general and need interpretation.', 'codes are valuable but must be backed by law, testing standards and company culture.')],
      ['{org} develops software for aircraft and medical devices.', '{p} is joining {org} as a junior software engineer.'])

t10_2 = topic('Copyright legislation and software licensing: free software, open source, shareware and commercial', 'copyright legislation', 'software licensing', 'open source', 'shareware')
LIC = [('commercial software', 'paid for; source code not available; cannot be copied or modified; licence limits number of users'),
       ('shareware', 'free to try for a limited time or with limited features; payment needed to continue/unlock; source code not available'),
       ('free software (Free Software Foundation)', 'users are free to run, study, modify and redistribute the software; source code available; modified versions must keep the same freedoms'),
       ('open source software (Open Source Initiative)', 'source code available and can be modified and redistributed under the licence terms; may be used commercially')]
t10_2.fixed('C1', (1, 2), [
    ('What is the purpose of copyright legislation?', 'To protect the creator\'s rights over their work and prevent unauthorised copying', 'Copyright gives the creator control of copying, distribution and modification.', ['To make all software free', 'To encrypt files', 'To stop software being sold']),
    ('Which type of licence normally allows a user to try software for free for a limited period?', 'Shareware', 'Shareware: trial, then pay.', ['Commercial', 'Free software', 'Public domain']),
    ('Which type of software gives users access to the source code?', 'Open source', 'Open source (and free software) make the source code available.', ['Commercial', 'Shareware', 'Freeware with no source']),
    ('What is a software licence?', 'A legal agreement setting out how the software may be used', 'Licence: number of users, copying, modification, distribution terms.', ['The installation file', 'A password for the software', 'A guarantee that the software has no bugs']),
] + [(f'Which describes {n}?', d[0].upper() + d[1:], f'{n}: {d}.', [x[1][0].upper() + x[1][1:] for x in LIC if x[0] != n]) for n, d in LIC])
t10_2.fixed('C2', (2, 3, 4), [
    ('Explain why a company might choose open source software rather than commercial software.', 'No licence fee; the source code can be modified to suit the company\'s needs; large community support and frequent updates.', '1 mark per point, max 2 [2]'),
    ('Explain the difference between free software and freeware.', 'Free software gives the freedom to study, modify and share the source code (free as in freedom); freeware is just free of charge, with no access to the source code.', '1 mark each [2]'),
    ('Explain why software companies need copyright protection.', 'Software is expensive to develop and easy to copy; without protection they would lose income and could not fund development.', '1 mark each [2]'),
])
items(t10_2, 'C3', (2, 3, 4), [
    ('{org} in {city} wants an office suite that it can modify to add its own features without paying licence fees. Recommend a type of licence and justify it.', 'Open source or free software: source code available to modify, no licence fee.', '1 mark type; 2 marks justification [3]'),
    ('{p} downloads a photo-editing program that stops working after 30 days unless a key is bought. Identify the type of licence and give one advantage to the user.', 'Shareware: the user can try it before deciding to pay.', '1 mark type; 1 mark advantage [2]'),
    ('{org} buys a licence for 20 users of an accounting package but installs it on 35 computers. Explain the legal issue.', 'Breach of licence agreement and copyright; only 20 installations are allowed; the company could be fined/sued.', '1 mark breach; 1 mark consequence [2]'),
    ('{p} modifies an open source program and wants to sell it. Explain what {p} must consider about the licence.', 'The licence terms may require the modified source to be released under the same licence and credit the original authors.', '1 mark each [2]'),
    ('{org} is deciding whether to use commercial or open source software for its payroll system. Give one advantage of each for {org}.', 'Commercial: guaranteed support/updates and warranty; open source: no fee and can be customised.', '1 mark each [2]'),
])
essay(t10_2, [('whether {org} should use open source software instead of commercial software', 'no licence cost; source can be adapted and checked for security; community support; no vendor lock-in.',
               'support may be informal; may need in-house expertise; compatibility with partners\' commercial file formats; training costs.', 'depends on in-house skills and need for guaranteed support.')],
      ['{org} in {city} is reviewing its software costs.', '{p} manages the IT budget at {org}.'])

t10_3 = topic('Artificial intelligence: social, economic and environmental impacts', 'artificial intelligence', 'social, economic and environmental impacts')
t10_3.fixed('C1', (1, 2), [
    ('What is artificial intelligence (AI)?', 'The ability of a computer system to perform tasks that normally need human intelligence', 'e.g. learning, reasoning, recognising speech or images.', ['Any program that uses a database', 'A very fast processor', 'A robot with a camera']),
    ('Which is an example of AI in everyday use?', 'A voice assistant that understands spoken questions', 'Speech recognition, recommendation systems, image recognition.', ['A calculator adding numbers', 'A word processor saving a file', 'A printer driver']),
    ('Which is a social impact of AI?', 'Changes in the types of jobs available', 'AI automates routine tasks, creating some jobs and removing others.', ['Faster clock speeds', 'Larger hard drives', 'Wider data buses']),
    ('Which is an environmental impact of AI?', 'High energy use by data centres used to train models', 'Training large models uses much electricity; AI can also optimise energy use.', ['Fewer software bugs', 'Lower ink use', 'More copyright laws']),
])
t10_3.fixed('C2', (2, 3, 4), [
    ('Explain one economic advantage and one economic disadvantage of AI for a manufacturing company.', 'Advantage: lower labour costs and faster, more consistent production. Disadvantage: high cost of buying/developing and maintaining AI systems; need for specialist staff.', '1 mark each [2]'),
    ('Explain how bias can arise in AI systems.', 'AI learns from training data; if the data is unrepresentative or reflects past discrimination, the AI repeats it in its decisions.', '1 mark: training data; 1 mark: biased decisions [2]'),
])
items(t10_3, 'C3', (2, 3, 4), [
    ('{org} in {city} plans to use AI chatbots instead of call-centre staff. Describe one social and one economic impact.', 'Social: staff lose jobs/need retraining; customers may find chatbots frustrating. Economic: lower costs; 24/7 service.', '1 mark each impact with explanation [2]'),
    ('A hospital in {city} uses AI to analyse X-ray images. Give two benefits and one concern.', 'Benefits: faster diagnosis; detects patterns doctors miss. Concern: errors/bias; responsibility for mistakes; patient privacy.', '1 mark per point [3]'),
    ('A city council in {city} uses AI to control traffic lights. Explain one environmental benefit.', 'Smoother traffic flow reduces idling and fuel use, lowering emissions.', '1 mark each [2]'),
    ('{org} uses AI to screen job applications. Explain one ethical issue.', 'The AI may be biased against some groups if trained on biased data; lack of transparency in decisions.', '1 mark each [2]'),
    ('Self-driving delivery vans are being tested in {city}. Describe one social and one environmental impact.', 'Social: drivers lose jobs / safety questions; environmental: efficient driving lowers emissions, but more vehicles may be used.', '1 mark each [2]'),
])
essay(t10_3, [('the impact of artificial intelligence on employment', 'automation of repetitive work; new jobs in AI development and maintenance; higher productivity.',
               'job losses in routine roles; need for retraining; inequality between skilled and unskilled workers.', 'the overall effect depends on retraining and government policy.'),
              ('the use of AI to make decisions about people, such as loans or medical treatment', 'consistent, fast decisions; can analyse vast data; may reduce some human errors.',
               'bias in training data; lack of transparency; accountability for mistakes; privacy.', 'AI should support, not replace, human judgement for decisions about people.'),
              ('the environmental impact of artificial intelligence', 'optimises energy use in buildings, traffic and power grids; improves climate modelling.',
               'training and running models uses large amounts of electricity and water; hardware manufacture and e-waste.', 'impact depends on renewable energy and efficient models.')],
      ['{org} in {city} is considering investing in AI.', 'A newspaper in {city} has asked {p} to write an article about AI.', 'The government in {city} is consulting the public about AI.'])

ar(t10_1, [('Professional bodies publish codes of conduct for their members.', 'Codes set out the standards of behaviour expected of computing professionals.'),
           ('A programmer should report a serious safety flaw even if a manager wants to ship the product.', 'Codes of conduct require members to act in the public interest.'),
           ('A software engineer should refuse work beyond their competence.', 'Codes of conduct require members to work only within their professional competence.'),
           ('Accepting gifts from suppliers can breach a code of conduct.', 'It creates a conflict of interest that may bias professional judgement.')],
   ['Codes of conduct are criminal laws enforced by the police.', 'The BCS code requires members to maximise their employer\'s profit above all else.', 'Ethical codes only apply to hardware engineers.', 'A professional may share client data freely if it is useful.'])
items(t10_1, 'C2', (2, 3, 4), [
    ('{p}, a developer at {org}, is told to hide the fact that an app collects users\' locations. Explain which principle of a professional code of conduct this breaks.', 'Acting in the public interest and with integrity: users must be told what data is collected; hiding it is dishonest and may breach privacy law.', '1 mark: principle (public interest/integrity/honesty); 1 mark: applied to the scenario [2]'),
    ('{p} is asked to sign off testing for software at {org} that has not been tested. Explain why this would be unethical.', 'It is dishonest and could put users at risk; codes require honesty and professional competence.', '1 mark: dishonesty/risk; 1 mark: principle [2]'),
    ('{p} takes credit at {org} for code written by a colleague. Explain which part of a code of conduct this breaks.', 'Integrity/duty to the profession: professionals must respect the work of others and not misrepresent it.', '1 mark each [2]'),
    ('{p} leaves {org} and joins a competitor, taking copies of client files. Explain the ethical and legal issues.', 'Breach of confidentiality and duty to the previous employer/client; possible breach of data protection and copyright law.', '1 mark ethical; 1 mark legal [2]'),
    ('{org} asks {p} to design a website that is difficult for disabled users to access. Explain why a professional code of conduct would discourage this.', 'Codes require consideration of the public interest and equality/accessibility; excluding users is discriminatory.', '1 mark each [2]'),
    ('{p} notices that {org} is storing customer passwords in plain text. Explain what a professional should do and why.', 'Raise it with managers and recommend hashing; the duty to protect the public and data security requires action.', '1 mark each [2]'),
])
ar(t10_2, [('Software is protected by copyright.', 'Program code is the original work of its author and copying it without permission is illegal.'),
           ('Users of open source software can modify it.', 'The source code is made available under the licence.'),
           ('A shareware program may stop working after a trial period.', 'Shareware is free to try but must be paid for to continue using it.'),
           ('A company may be fined for installing more copies of software than its licence allows.', 'The licence is a legal agreement that limits the number of installations.')],
   ['Commercial software always includes its source code.', 'Shareware gives the user full rights to modify the source code.', 'Copyright only applies to printed books.', 'Free software must always be sold at a low price.'])
items(t10_2, 'C2', (2, 3, 4), [
    ('{p} wants to share a copy of a commercial game bought for {org} with a friend. Explain why this is not allowed.', 'The licence allows use by the purchaser only; copying breaches copyright and the licence agreement.', '1 mark each [2]'),
    ('{org} uses an open source web server. Explain one benefit and one risk of this choice.', 'Benefit: no cost/can be modified; risk: support depends on the community and the company needs expertise.', '1 mark each [2]'),
    ('Explain why a developer at {org} might release a utility as shareware rather than commercial software.', 'Users can try it before paying, so more people use it and some pay; low distribution cost.', '1 mark each [2]'),
    ('Explain why software licensed under the GNU General Public Licence cannot be turned into closed commercial software by {org}.', 'The licence requires modified versions to be distributed with source code under the same free terms.', '1 mark each [2]'),
    ('{p} finds code on the internet and wants to use it in a product for {org}. Explain what {p} must check.', 'The licence terms: whether commercial use/modification is allowed, whether attribution is required, whether derived code must be open source.', '1 mark per point, max 2 [2]'),
    ('Explain the difference between a single-user licence and a site licence for {org}.', 'Single-user: one person/computer; site licence: any number of users at one site/organisation, usually cheaper per user.', '1 mark each [2]'),
])
ar(t10_3, [('AI systems can show bias.', 'They learn from training data that may contain bias.'),
           ('AI can reduce the cost of some services.', 'AI can automate tasks previously carried out by paid staff.'),
           ('Training large AI models has an environmental impact.', 'Training uses large amounts of electricity in data centres.'),
           ('AI can improve medical diagnosis.', 'AI can detect patterns in large numbers of images that humans may miss.')],
   ['AI systems never make mistakes.', 'AI only affects the computer industry.', 'AI systems do not need data to learn.', 'Using AI has no effect on employment.'])
items(t10_3, 'C2', (2, 3, 4), [
    ('A bank in {city} uses AI to decide who gets a loan. Explain why the bank must be able to explain the AI\'s decisions.', 'Customers have a right to know why they were refused; unexplained decisions may hide bias and breach regulations.', '1 mark each [2]'),
    ('{org} replaces warehouse staff in {city} with AI-controlled robots. Explain one economic benefit for {org} and one social cost.', 'Benefit: lower long-term costs/24-hour working; cost: unemployment/need for retraining in the area.', '1 mark each [2]'),
    ('Explain how AI could help reduce energy use in buildings managed by {org}.', 'AI learns occupancy patterns and adjusts heating, cooling and lighting automatically, reducing waste.', '1 mark each [2]'),
    ('Explain why AI-generated news articles raise ethical concerns for a newspaper in {city}.', 'They may contain errors or misinformation, may copy others\' work, and readers may not know they were AI-written.', '1 mark per point, max 2 [2]'),
    ('{p} says AI will create more jobs than it destroys. Explain one argument for and one against this view.', 'For: new jobs in AI development, maintenance and data; against: many routine jobs automated faster than new ones appear.', '1 mark each [2]'),
    ('A school in {city} uses AI to mark essays. Explain one benefit and one concern.', 'Benefit: fast feedback/consistency; concern: may misjudge creativity or be biased; teacher oversight needed.', '1 mark each [2]'),
])

CHAPTERS[10] = [t10_1, t10_2, t10_3]

# =============================================================================== Chapter 11 Databases
FIRST = ['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Ethan', 'Priya', 'Omar', 'Chloe', 'Daniel', 'Mei', 'Tariq', 'Hana', 'Jonas']


def _rows_product(r):
    cats = ['Snacks', 'Drinks', 'Bakery', 'Dairy', 'Frozen']
    names = {'Snacks': ['Crisps', 'Pretzels', 'Nuts', 'Popcorn', 'Crackers'], 'Drinks': ['Juice', 'Water', 'Cola', 'Iced Tea', 'Lemonade'], 'Bakery': ['Bagels', 'Croissant', 'Rolls', 'Muffin', 'Loaf'],
             'Dairy': ['Yoghurt', 'Butter', 'Cheese', 'Milk', 'Cream'], 'Frozen': ['Peas', 'Pizza', 'Ice Cream', 'Fish Fingers', 'Berries']}
    rows, used = [], set()
    ids = r.sample(range(101, 200), 7)
    for i in ids:
        c = r.choice(cats)
        n = r.choice([x for x in names[c] if x not in used] or names[c])
        used.add(n)
        rows.append({'ProductID': f'P{i}', 'ProductName': n, 'Category': c, 'Price': round(r.randrange(50, 1000) / 100, 2), 'StockLevel': r.randrange(0, 80)})
    return rows


def _rows_student(r):
    rows = []
    for i, n in zip(r.sample(range(1001, 1100), 7), r.sample(FIRST, 7)):
        rows.append({'StudentID': str(i), 'FirstName': n, 'TutorGroup': r.choice(['11A', '11B', '11C']), 'Age': r.choice([15, 16, 17]), 'House': r.choice(['Red', 'Blue', 'Green', 'Yellow'])})
    return rows


def _rows_employee(r):
    rows = []
    for i, n in zip(r.sample(range(201, 300), 7), r.sample(FIRST, 7)):
        rows.append({'EmployeeID': f'E{i}', 'Name': n, 'Department': r.choice(['Sales', 'IT', 'Finance', 'HR']), 'Salary': r.randrange(28, 80) * 1000, 'StartYear': r.randrange(2008, 2025)})
    return rows


def _rows_book(r):
    titles = ['River Song', 'Night Train', 'Blue Planet', 'Code Breakers', 'Silent Hill', 'Lost City', 'Star Map', 'Deep Ocean', 'Iron Bridge', 'Green Valley', 'Last Light', 'Hidden Path']
    rows = []
    for i, t in zip(r.sample(range(1, 99), 7), r.sample(titles, 7)):
        rows.append({'BookID': f'B{i:02d}', 'Title': t, 'Genre': r.choice(['Fiction', 'Science', 'History', 'Travel']), 'YearPublished': r.randrange(1995, 2025), 'Copies': r.randrange(1, 9)})
    return rows


SCHEMAS = [
    ('PRODUCT', _rows_product, 'ProductID', [('ProductID', 'VARCHAR(4)'), ('ProductName', 'VARCHAR(20)'), ('Category', 'VARCHAR(10)'), ('Price', 'REAL'), ('StockLevel', 'INTEGER')], 'a shop'),
    ('STUDENT', _rows_student, 'StudentID', [('StudentID', 'CHARACTER(4)'), ('FirstName', 'VARCHAR(20)'), ('TutorGroup', 'CHARACTER(3)'), ('Age', 'INTEGER'), ('House', 'VARCHAR(10)')], 'a school'),
    ('EMPLOYEE', _rows_employee, 'EmployeeID', [('EmployeeID', 'VARCHAR(4)'), ('Name', 'VARCHAR(20)'), ('Department', 'VARCHAR(10)'), ('Salary', 'INTEGER'), ('StartYear', 'INTEGER')], 'a company'),
    ('BOOK', _rows_book, 'BookID', [('BookID', 'CHARACTER(3)'), ('Title', 'VARCHAR(30)'), ('Genre', 'VARCHAR(10)'), ('YearPublished', 'INTEGER'), ('Copies', 'INTEGER')], 'a library'),
]
NUMF = {'Price', 'StockLevel', 'Age', 'Salary', 'StartYear', 'YearPublished', 'Copies'}


def sqlv(v):
    if isinstance(v, str):
        return f"'{v}'"
    return f'{v:g}' if isinstance(v, float) else str(v)


def tbl_text(name, rows, cols=None):
    cols = cols or list(rows[0])
    lines = [f'Table {name}: ' + ' | '.join(cols)] + [' | '.join(sqlv(x[c]).strip("'") if not isinstance(x[c], float) else f'{x[c]:.2f}' for c in cols) for x in rows]
    return code(lines)


def _cond(r, rows, D):
    keys = list(rows[0])
    conds = []
    nf = [k for k in keys if k in NUMF]
    sf_ = [k for k in keys if k not in NUMF and not k.endswith('ID')]
    f = r.choice(nf)
    vals = sorted({x[f] for x in rows})
    v = vals[len(vals) // 2]
    op = r.choice(['>', '<', '>=', '<=']) if D >= 2 else r.choice(['>', '<'])
    conds.append((f, op, v))
    if D >= 3:
        g = r.choice(sf_)
        conds.append((g, '=', r.choice([x[g] for x in rows])))
    return conds


def _test(x, c):
    f, op, v = c
    a = x[f]
    return {'>': a > v, '<': a < v, '>=': a >= v, '<=': a <= v, '=': a == v, '<>': a != v}[op]


def cond_sql(conds, conj='AND'):
    return f' {conj} '.join(f'{f} {op} {sqlv(v)}' for f, op, v in conds)


def cond_words(conds, conj='and'):
    w = {'>': 'greater than', '<': 'less than', '>=': 'at least', '<=': 'at most', '=': 'equal to'}
    return f' {conj} '.join(f'{f} {w[op]} {v if not isinstance(v, str) else repr(v).replace(chr(39), chr(34))}' for f, op, v in conds)


def _query(r, D):
    name, gen, pk, fields, where = r.choice(SCHEMAS)
    rows = gen(r)
    conds = _cond(r, rows, D)
    conj = 'OR' if D >= 4 and len(conds) > 1 and r.random() < 0.4 else 'AND'
    cols = r.sample([f for f, _ in fields], 2)
    order = r.choice([None, (r.choice([f for f, _ in fields]), r.choice(['ASC', 'DESC']))]) if D >= 2 else None
    sel = [x for x in rows if (all(_test(x, c) for c in conds) if conj == 'AND' else any(_test(x, c) for c in conds))]
    if order:
        sel = sorted(sel, key=lambda x: x[order[0]], reverse=order[1] == 'DESC')
    sql = f'SELECT {", ".join(cols)} FROM {name} WHERE {cond_sql(conds, conj)}' + (f' ORDER BY {order[0]} {order[1]}' if order else '') + ';'
    return name, rows, cols, conds, conj, order, sel, sql, fields


t11_1 = topic('Limitations of file-based systems and features of a relational database: entity, table, record, field, keys', 'limitations of file-based systems', 'relational database', 'entity, table, record, field', 'keys')
t11_1.fixed('C1', (1, 2), [
    ('What is a primary key?', 'A field (or fields) that uniquely identifies each record in a table', 'Primary key values must be unique and not empty.', ['A field that links to another table', 'The first field in every table', 'A password for the database']),
    ('What is a foreign key?', 'A field in one table that is the primary key of another table, used to link them', 'Foreign keys create relationships between tables.', ['A key that is used in another country', 'A field that is always unique in its own table', 'An encrypted field']),
    ('What is a candidate key?', 'Any field or combination of fields that could be chosen as the primary key', 'Candidate keys are unique and minimal; one is chosen as the primary key.', ['A key that has been deleted', 'A foreign key with no matching record', 'A field that contains only numbers']),
    ('What is a secondary key?', 'A field that is indexed to allow fast searching but is not the primary key', 'e.g. Surname indexed for quick look-up.', ['A second primary key', 'A key used to encrypt data', 'A key for a backup copy']),
    ('In a relational database, what is a record?', 'One row of a table, holding data about one instance of the entity', 'Record = tuple/row; field = attribute/column.', ['One column of a table', 'The whole table', 'The data dictionary']),
    ('What is meant by data redundancy?', 'The same data being stored unnecessarily more than once', 'Redundancy wastes storage and can lead to inconsistency.', ['Data that has been deleted', 'Data that is encrypted', 'Data that is no longer needed']),
    ('What is an entity?', 'Anything about which data can be stored, such as a person, place or event', 'Each entity becomes a table in a relational database.', ['A single item of data', 'A relationship between tables', 'A type of query']),
    ('What is referential integrity?', 'Making sure every foreign key value matches an existing primary key value', 'Prevents orphan records and keeps relationships consistent.', ['Making sure all fields are filled in', 'Encrypting all records', 'Making sure each table has an index']),
])
t11_1.fixed('C2', (2, 3, 4), [
    ('Explain two limitations of a file-based approach to storing data.', 'Data redundancy — the same data held in several files; data inconsistency — copies updated in one file but not another; data dependency — programs tied to file structure; hard to share/secure data.', '1 mark per limitation with explanation, max 2 × 2 [4]'),
    ('Explain how a relational database reduces data inconsistency.', 'Data about each entity is stored once in its own table and linked by keys, so an update is made in one place and every query sees the same value.', '1 mark: stored once; 1 mark: updated in one place/linked by keys [2]'),
    ('Explain why a primary key is needed in each table.', 'It uniquely identifies each record so records can be found, updated and linked through foreign keys without ambiguity.', '1 mark: unique identification; 1 mark: linking/searching [2]'),
    ('Explain the difference between a primary key and a foreign key.', 'A primary key uniquely identifies records in its own table; a foreign key is an attribute in another table that refers to that primary key to create a relationship.', '1 mark each [2]'),
])


@t11_1.add('C3', (1, 2, 3, 4))
def t11_1_keys(r, D):
    name, gen, pk, fields, where = r.choice(SCHEMAS)
    rows = gen(r)
    if D <= 2:
        others = [f for f, _ in fields if f != pk]
        return MCQ(r, f'{tbl_text(name, rows)}\nWhich field is the most suitable primary key for the table {name}?', pk, others, f'{pk} is unique for each record; other fields may repeat.')
    nrec, nf = len(rows), len(fields)
    stem = f'{tbl_text(name, rows)}\n(a) State the number of records and fields in the table. (b) Identify the primary key and explain why the field {fields[2][0]} is not suitable as a primary key.'
    dup = [x[fields[2][0]] for x in rows]
    reason = 'its values are repeated (e.g. ' + str(next((v for v in dup if dup.count(v) > 1), dup[0])) + ')' if len(set(dup)) < len(dup) else 'its values could be repeated as more records are added'
    return Q(stem, f'(a) {nrec} records, {nf} fields (b) {pk}; {fields[2][0]} is not suitable because {reason}', f'(a) {nrec} records [1]; {nf} fields [1] (b) {pk} [1]; reason [1] [4]', marks=4)


scen(t11_1, 'C4', (2, 3, 4, 5), [
    '{org} in {city} stores customer and order data in separate spreadsheet files used by different departments.',
    '{org} in {city} keeps customer details in one file for the sales team and a separate file of orders for the warehouse.',
], [('Explain two problems caused by the file-based approach.', 'Redundancy (same customer details in several files); inconsistency (address updated in one only); difficult to query across files; poor security.', '1 mark each problem, 1 mark explanation [4]'),
    ('Describe how a relational database would be structured instead.', 'Separate tables for each entity (CUSTOMER, ORDER) linked by primary/foreign keys; data stored once.', '1 mark tables; 1 mark keys/link [2]'),
    ('Identify a suitable primary key and foreign key for the ORDER table.', 'Primary key OrderID; foreign key CustomerID.', '1 mark each [2]'),
    ('Explain how referential integrity prevents errors.', 'Each foreign key must match an existing primary key so an order cannot refer to a customer who does not exist.', '1 mark each [2]')], k=(3, 4))

ER = [('CUSTOMER', 'ORDER', 'one-to-many', 'each customer can place many orders, but each order is placed by one customer'),
      ('STUDENT', 'COURSE', 'many-to-many', 'a student can take many courses and each course has many students'),
      ('DEPARTMENT', 'EMPLOYEE', 'one-to-many', 'a department has many employees, but each employee works in one department'),
      ('PERSON', 'PASSPORT', 'one-to-one', 'each person has one current passport and each passport belongs to one person'),
      ('AUTHOR', 'BOOK', 'many-to-many', 'an author can write many books and a book can have several authors'),
      ('TEAM', 'PLAYER', 'one-to-many', 'a team has many players but each player plays for one team'),
      ('FLIGHT', 'PASSENGER', 'many-to-many', 'a flight carries many passengers and a passenger can take many flights'),
      ('HOTEL', 'ROOM', 'one-to-many', 'a hotel has many rooms and each room is in one hotel'),
      ('ACTOR', 'FILM', 'many-to-many', 'an actor appears in many films and a film has many actors'),
      ('COUNTRY', 'CAPITAL', 'one-to-one', 'each country has one capital city and each capital belongs to one country'),
      ('DOCTOR', 'APPOINTMENT', 'one-to-many', 'a doctor has many appointments but each appointment is with one doctor'),
      ('SUPPLIER', 'PRODUCT', 'one-to-many', 'a supplier supplies many products but each product comes from one supplier')]
NORM = [
    {'un': 'ORDER(OrderID, OrderDate, CustomerID, CustomerName, CustomerPhone, ProductID, ProductName, UnitPrice, Quantity)', 'ctx': 'an online shop',
     'pk': 'OrderID + ProductID', 'partial': 'ProductName depends only on ProductID (part of the key)', 'trans': 'CustomerName depends on CustomerID, which depends on OrderID',
     '3nf': 'CUSTOMER(CustomerID, CustomerName, CustomerPhone); ORDER(OrderID, OrderDate, CustomerID); PRODUCT(ProductID, ProductName, UnitPrice); ORDER_LINE(OrderID, ProductID, Quantity)'},
    {'un': 'ENROLMENT(StudentID, StudentName, TutorID, TutorName, CourseID, CourseName, Grade)', 'ctx': 'a college',
     'pk': 'StudentID + CourseID', 'partial': 'StudentName depends only on StudentID', 'trans': 'TutorName depends on TutorID, which depends on StudentID',
     '3nf': 'STUDENT(StudentID, StudentName, TutorID); TUTOR(TutorID, TutorName); COURSE(CourseID, CourseName); ENROLMENT(StudentID, CourseID, Grade)'},
    {'un': 'LOAN(MemberID, MemberName, BookID, Title, AuthorID, AuthorName, LoanDate)', 'ctx': 'a library',
     'pk': 'MemberID + BookID + LoanDate', 'partial': 'Title depends only on BookID', 'trans': 'AuthorName depends on AuthorID, which depends on BookID',
     '3nf': 'MEMBER(MemberID, MemberName); BOOK(BookID, Title, AuthorID); AUTHOR(AuthorID, AuthorName); LOAN(MemberID, BookID, LoanDate)'},
    {'un': 'APPOINTMENT(PatientID, PatientName, DoctorID, DoctorName, Specialism, AppDate, AppTime, Room)', 'ctx': 'a medical centre',
     'pk': 'PatientID + DoctorID + AppDate + AppTime', 'partial': 'PatientName depends only on PatientID', 'trans': 'Specialism depends on DoctorID, which is not the whole key',
     '3nf': 'PATIENT(PatientID, PatientName); DOCTOR(DoctorID, DoctorName, Specialism); APPOINTMENT(PatientID, DoctorID, AppDate, AppTime, Room)'},
    {'un': 'MEMBERSHIP(MemberID, MemberName, TeamID, TeamName, CoachID, CoachName, JoinDate)', 'ctx': 'a sports club',
     'pk': 'MemberID + TeamID', 'partial': 'MemberName depends only on MemberID', 'trans': 'CoachName depends on CoachID, which depends on TeamID',
     '3nf': 'MEMBER(MemberID, MemberName); TEAM(TeamID, TeamName, CoachID); COACH(CoachID, CoachName); MEMBERSHIP(MemberID, TeamID, JoinDate)'},
    {'un': 'HIRE(HireID, CustomerID, CustomerName, CarReg, Make, Model, StartDate, Days)', 'ctx': 'a car hire company',
     'pk': 'HireID', 'partial': 'none, because the primary key is a single field (so the table is already in 2NF once in 1NF)', 'trans': 'CustomerName depends on CustomerID and Make/Model depend on CarReg, not directly on HireID',
     '3nf': 'CUSTOMER(CustomerID, CustomerName); CAR(CarReg, Make, Model); HIRE(HireID, CustomerID, CarReg, StartDate, Days)'},
]
t11_2 = topic('Entity-relationship modelling and normalisation to third normal form', 'entity-relationship modelling', 'normalisation', 'third normal form')
t11_2.fixed('C1', (1, 2, 3), [
    ('A table is in first normal form (1NF) when', 'it has no repeating groups of attributes and every field is atomic', '1NF: atomic values, no repeating groups, a primary key.', ['every non-key attribute depends on the whole key', 'there are no transitive dependencies', 'it has a foreign key']),
    ('A table in 1NF is also in second normal form (2NF) when', 'it has no partial dependencies', '2NF: every non-key attribute depends on the whole primary key.', ['it has no repeating groups', 'it has no transitive dependencies', 'it has at least two tables']),
    ('A table in 2NF is in third normal form (3NF) when', 'it has no non-key dependencies (transitive dependencies)', '3NF: non-key attributes depend only on the key.', ['all fields are numbers', 'it has a composite key', 'it has no foreign keys']),
    ('How is a many-to-many relationship implemented in a relational database?', 'By adding a link table with a one-to-many relationship to each original table', 'The link table has a composite key of the two foreign keys.', ['By putting both primary keys in one table', 'It cannot be implemented', 'By duplicating every record']),
    ('What is a composite key?', 'A primary key made of two or more fields', 'e.g. (StudentID, CourseID) in an ENROLMENT table.', ['A key made by joining two tables', 'A foreign key that is also encrypted', 'A field that contains text and numbers']),
    ('What is a partial dependency?', 'A non-key attribute that depends on only part of a composite primary key', 'Partial dependencies are removed to reach 2NF.', ['An attribute that depends on another non-key attribute', 'A key that is only partly unique', 'A missing field']),
])
t11_2.fixed('C2', (2, 3, 4), [
    ('Explain why a many-to-many relationship cannot be implemented directly in a relational database.', 'A foreign key field can hold only one value per record, so each side would need repeating groups; a link table is used to turn it into two one-to-many relationships.', '1 mark: one value per field/repeating groups; 1 mark: link table [2]'),
    ('Explain the benefits of normalising a database.', 'Reduces data redundancy, so less storage and fewer update anomalies; improves data integrity and consistency.', '1 mark per point, max 2 [2]'),
])


@t11_2.add('C3', (1, 2, 3, 4))
def t11_2_rel(r, D):
    a, c, rel, why = r.choice(ER)
    if D <= 2:
        return MCQ(r, f'What is the relationship between the entities {a} and {c}?', rel, [x for x in ['one-to-one', 'one-to-many', 'many-to-many', 'many-to-one'] if x != rel], f'{why[0].upper() + why[1:]}.')
    extra = f' Explain how this relationship would be implemented using tables and keys.' if D >= 3 else ''
    impl = {'one-to-many': f'the primary key of {a} is a foreign key in {c}', 'one-to-one': f'the primary key of one table is a foreign key in the other',
            'many-to-many': f'a link table (e.g. {a}_{c}) holding the primary keys of both tables as foreign keys, forming a composite key'}[rel]
    return Q(f'State the type of relationship between {a} and {c}, giving a reason.{extra}', f'{rel}: {why}' + (f'. Implementation: {impl}.' if extra else ''),
             f'1 mark: {rel}; 1 mark: reason' + ('; 1 mark: implementation [3]' if extra else ' [2]'), marks=3 if extra else 2)


@t11_2.add('C3', (2, 3, 4, 5))
def t11_2_norm(r, D):
    n = r.choice(NORM)
    k = r.choice(['pk', 'partial', 'trans', '3nf'] if D >= 3 else ['pk', 'partial'])
    q = {'pk': 'Identify a suitable primary key for this table in 1NF.', 'partial': 'Identify one partial dependency.', 'trans': 'Identify one non-key (transitive) dependency.',
         '3nf': 'Normalise the table to third normal form, giving each table with its key.'}[k]
    m = {'pk': 1, 'partial': 2, 'trans': 2, '3nf': 4}[k]
    return Q(f'A database for {n["ctx"]} uses the table {n["un"]}. {q}', n[k], f'{n[k]} [{m}]', marks=m)


@t11_2.add('C4', (3, 4, 5), 'multi_step')
def t11_2_full(r, D):
    n = r.choice(NORM)
    d = ctx(r)
    stem = (f'{d["p"]} is designing a database for {n["ctx"]} in {d["city"]}. All the data is currently held in one table: {n["un"]}. (a) Identify the primary key. (b) Explain why the table is not in 2NF or 3NF, giving an example. '
            f'(c) Produce a design in 3NF. (d) Explain one benefit of the new design.')
    return Q(stem, f'(a) {n["pk"]} (b) partial: {n["partial"]}; transitive: {n["trans"]} (c) {n["3nf"]} (d) less redundancy, fewer update anomalies',
             f'(a) [1] (b) partial dependency example [1]; non-key dependency example [1] (c) {n["3nf"]} [4] (d) [1]', marks=8, typ='multi_step')


@t11_2.add('C2', (2, 3, 4), 'explain')
def t11_2_anom(r, D):
    n = r.choice(NORM)
    kind = r.choice(['update', 'insert', 'delete'])
    expl = {'update': 'If a value such as a name is stored in many records, changing it means updating every copy; missing one leaves inconsistent data.',
            'insert': 'Data about one entity cannot be added until related data exists (e.g. a new item cannot be stored until it appears in a transaction).',
            'delete': 'Deleting the last record about one transaction also deletes the only copy of other data (e.g. the details of an item or person).'}[kind]
    return Q(f'Explain how the unnormalised table {n["un"]}, used by {n["ctx"]}, could lead to a {kind} anomaly.', expl, f'1 mark: describes the {kind} problem; 1 mark: linked to the table attributes [2]')


t11_3 = topic('Database management systems: data dictionary, logical schema, access rights and developer interface', 'database management systems', 'data dictionary', 'logical schema')
t11_3.fixed('C1', (1, 2), [
    ('What is a data dictionary?', 'A file that holds metadata about the database, such as table names, field names, types and validation rules', 'The data dictionary describes the structure of the data, not the data itself.', ['A list of all the data values', 'A spell-checker for SQL', 'A backup of the database']),
    ('What is a logical schema?', 'An overall model of the database structure independent of how it is physically stored', 'Logical schema: tables, attributes, relationships, keys.', ['The physical layout of data on disk', 'A user\'s view of a form', 'A list of passwords']),
    ('Which DBMS feature lets the administrator stop some users changing data?', 'Access rights', 'Access rights/permissions: read, write, delete for each user group.', ['Data dictionary', 'Query processor', 'Indexing']),
    ('What is the purpose of the query processor in a DBMS?', 'To process and optimise queries so data can be retrieved efficiently', 'Query processor interprets and executes queries (e.g. SQL).', ['To design forms', 'To back up the database', 'To encrypt passwords']),
    ('What does the developer interface of a DBMS allow?', 'Creation and manipulation of the database structure, forms, queries and reports', 'Developer interface: tools for building tables, forms and queries without writing everything in code.', ['Only data entry by end users', 'Only printing reports', 'Network configuration']),
])
t11_3.fixed('C2', (2, 3, 4), [
    ('Explain how a DBMS addresses the problems of a file-based system.', 'Stores data once in related tables (less redundancy and inconsistency); data dictionary describes data independently of programs (data independence); access rights and backup/recovery tools improve security and integrity.', '1 mark per point, max 3 [3]'),
    ('Explain why the data dictionary is important for a database developer.', 'It records names, types, sizes, keys and validation rules, so developers can build queries and programs correctly and the DBMS can enforce validation.', '1 mark each [2]'),
])
scen(t11_3, 'C3', (2, 3, 4), [
    '{org} in {city} uses a DBMS to manage its staff, stock and sales data.',
    '{p} is the database administrator for {org}.',
], [('Describe how access rights could be set for different groups of staff.', 'e.g. sales staff read/write orders but read-only stock prices; managers full access; HR only staff records.', '1 mark per sensible right, max 2 [2]'),
    ('State three items stored in the data dictionary for a field.', 'Field name, data type, field size/length, validation rule, whether it is a key, description.', '1 mark each [3]'),
    ('Explain the benefit of indexing a frequently searched field.', 'Searches and sorts on that field are faster because the index can be used rather than scanning every record.', '1 mark each [2]'),
    ('Describe two tools in the developer interface.', 'Table design view, query builder (QBE), form designer, report generator.', '1 mark each [2]'),
    ('Explain why regular back-ups of the database are needed.', 'Data can be recovered after corruption, deletion or hardware failure.', '1 mark [1]')], k=(2, 3))
essay(t11_3, [('the benefits to {org} of replacing its spreadsheets with a database management system', 'less redundancy and inconsistency; data independence; access rights; query processor; backup and recovery; multi-user access.',
               'cost of DBMS and training; need for a database administrator; migration effort; more complex than a spreadsheet for small tasks.', 'for a growing organisation the benefits outweigh the costs.')],
      ['{org} in {city} has grown and now has 30 staff using shared data.', '{p} is preparing a proposal for the directors of {org}.'])

t11_4 = topic('SQL: data definition language and data manipulation language queries', 'sql', 'data definition language', 'data manipulation language')
t11_4.fixed('C1', (1, 2), [
    ('Which SQL statement is part of the data definition language (DDL)?', 'CREATE TABLE', 'DDL: CREATE DATABASE, CREATE TABLE, ALTER TABLE, PRIMARY KEY, FOREIGN KEY.', ['SELECT', 'UPDATE', 'INSERT INTO']),
    ('Which SQL statement is used to change values in existing records?', 'UPDATE', 'UPDATE table SET field = value WHERE condition;', ['ALTER TABLE', 'INSERT INTO', 'CREATE TABLE']),
    ('Which SQL statement adds a new field to an existing table?', 'ALTER TABLE ... ADD', 'ALTER TABLE changes the structure (DDL).', ['UPDATE ... SET', 'INSERT INTO', 'SELECT ... FROM']),
    ('Which SQL clause sorts the results of a query?', 'ORDER BY', 'ORDER BY field ASC/DESC.', ['GROUP BY', 'SORT', 'WHERE']),
    ('Which SQL function returns the number of rows that match a query?', 'COUNT', 'COUNT(*) or COUNT(field).', ['SUM', 'AVG', 'TOTAL']),
    ('What does DELETE FROM STUDENT WHERE Age > 18; do?', 'Removes all records in STUDENT where Age is greater than 18', 'DELETE removes records (rows), not fields.', ['Removes the Age field', 'Deletes the whole STUDENT table structure', 'Sets Age to 18']),
    ('Which SQL keyword combines rows from two tables using a common field?', 'INNER JOIN', 'SELECT ... FROM A INNER JOIN B ON A.Key = B.Key.', ['GROUP BY', 'UNION ALL', 'MERGE']),
])
t11_4.fixed('C2', (2, 3, 4), [
    ('Explain the difference between DDL and DML.', 'DDL defines or changes the structure of the database (CREATE, ALTER); DML adds, changes, deletes and queries the data itself (SELECT, INSERT, UPDATE, DELETE).', '1 mark each with example [2]'),
    ('Explain why an UPDATE statement without a WHERE clause can be dangerous.', 'Every record in the table would be changed, not just the intended ones.', '1 mark each [2]'),
])


@t11_4.add('C3', (1, 2, 3, 4, 5))
def t11_4_write(r, D):
    name, rows, cols, conds, conj, order, sel, sql, fields = _query(r, D)
    words = f'Write an SQL query to display the {cols[0]} and {cols[1]} of every record in {name} where {cond_words(conds, conj.lower())}' + (f', sorted by {order[0]} in {"descending" if order[1] == "DESC" else "ascending"} order' if order else '') + '.'
    if D == 1:
        wrong = [sql.replace('SELECT', 'SELECT *,', 1), sql.replace(' WHERE ', ' AND ', 1), sql.replace(f'FROM {name} ', '', 1), sql.replace('>', '<') if '>' in sql else sql.replace('<', '>')]
        return MCQ(r, f'Which SQL query displays the {cols[0]} and {cols[1]} of every record in {name} where {cond_words(conds)}?', sql, wrong, sql)
    m = 3 + (1 if order else 0) + (1 if len(conds) > 1 else 0)
    return Q(f'A table {name} has the fields {", ".join(f for f, _ in fields)}. ' + words, sql,
             f'{sql} — 1 mark SELECT fields; 1 mark FROM {name}; 1 mark WHERE condition' + ('; 1 mark second condition with ' + conj if len(conds) > 1 else '') + ('; 1 mark ORDER BY' if order else '') + f' [{m}]', marks=m)


@t11_4.add('C3', (2, 3, 4, 5), 'numerical')
def t11_4_out(r, D):
    name, rows, cols, conds, conj, order, sel, sql, fields = _query(r, D)
    out = '; '.join(', '.join(f'{x[c]:.2f}' if isinstance(x[c], float) else str(x[c]) for c in cols) for x in sel) or 'no rows are returned'
    stem = f'{tbl_text(name, rows)}\nState the output of the SQL query: {sql}'
    return Q(stem, out, f'Rows meeting {cond_sql(conds, conj)}' + (f', ordered by {order[0]} {order[1]}' if order else '') + f': {out}. 1 mark per correct row, all correct and no extra rows for full marks [{max(1, min(4, len(sel)))}]', marks=max(1, min(4, len(sel))))


@t11_4.add('C3', (2, 3, 4, 5), 'numerical')
def t11_4_agg(r, D):
    name, gen, pk, fields, where = r.choice(SCHEMAS)
    rows = gen(r)
    nf = [f for f, _ in fields if f in NUMF]
    gf = [f for f, _ in fields if f not in NUMF and not f.endswith('ID') and f not in ('ProductName', 'FirstName', 'Name', 'Title')]
    fn = r.choice(['COUNT', 'SUM', 'AVG']) if D < 4 else 'GROUP'
    g = r.choice(gf)
    gv = r.choice([x[g] for x in rows])
    f = r.choice(nf)
    sub = [x for x in rows if x[g] == gv]
    if fn == 'COUNT':
        sql, v = f"SELECT COUNT(*) FROM {name} WHERE {g} = '{gv}';", str(len(sub))
    elif fn == 'SUM':
        s = sum(x[f] for x in sub)
        sql, v = f"SELECT SUM({f}) FROM {name} WHERE {g} = '{gv}';", (f'{s:.2f}' if isinstance(s, float) else str(s))
    elif fn == 'AVG':
        s = sum(x[f] for x in sub) / len(sub)
        sql, v = f"SELECT AVG({f}) FROM {name} WHERE {g} = '{gv}';", f'{s:.2f}'.rstrip('0').rstrip('.')
    else:
        groups = sorted({x[g] for x in rows})
        sql = f'SELECT {g}, COUNT(*) FROM {name} GROUP BY {g};'
        v = '; '.join(f'{k}, {sum(1 for x in rows if x[g] == k)}' for k in groups)
    stem = f'{tbl_text(name, rows)}\nState the result of the query: {sql}'
    if D >= 3 and fn != 'GROUP':
        stem += ' Then write a query that would display the same result for every value of ' + g + ' using GROUP BY.'
        return Q(stem, f'{v}; SELECT {g}, {fn}({"*" if fn == "COUNT" else f}) FROM {name} GROUP BY {g};', f'Result {v} [2]; GROUP BY query [2] [4]', marks=4)
    return Q(stem, v, f'{v} [2]', marks=2)


@t11_4.add('C3', (2, 3, 4, 5))
def t11_4_ddl(r, D):
    name, gen, pk, fields, where = r.choice(SCHEMAS)
    kind = r.choice(['create', 'alter', 'insert', 'update', 'delete'])
    rows = gen(r)
    x = r.choice(rows)
    if kind == 'create':
        sql = f'CREATE TABLE {name} (' + ', '.join(f'{f} {t}' for f, t in fields) + f', PRIMARY KEY ({pk}));'
        stem = f'{where.capitalize()} needs a table {name} with the fields ' + ', '.join(f'{f} ({t})' for f, t in fields) + f'. {pk} is the primary key. Write the SQL statement to create the table.'
        return Q(stem, sql, f'{sql} — 1 mark CREATE TABLE {name}; 1 mark all fields with types; 1 mark PRIMARY KEY [3]', marks=3)
    if kind == 'alter':
        nf = r.choice([('Email', 'VARCHAR(40)'), ('DateAdded', 'DATE'), ('Active', 'BOOLEAN'), ('Notes', 'VARCHAR(100)')])
        sql = f'ALTER TABLE {name} ADD {nf[0]} {nf[1]};'
        return Q(f'Write an SQL statement to add a field {nf[0]} of type {nf[1]} to the existing table {name}.', sql, f'{sql} — 1 mark ALTER TABLE {name}; 1 mark ADD {nf[0]} {nf[1]} [2]', marks=2)
    if kind == 'insert':
        newv = dict(x)
        newv[pk] = str(x[pk])[:-1] + ('9' if str(x[pk])[-1] != '9' else '8')
        sql = f'INSERT INTO {name} (' + ', '.join(newv) + ') VALUES (' + ', '.join(sqlv(v) for v in newv.values()) + ');'
        return Q(f'Write an SQL statement to add a new record to {name} with the values ' + ', '.join(f'{k} = {v}' for k, v in newv.items()) + '.', sql, f'{sql} — 1 mark INSERT INTO with field list; 1 mark VALUES in correct order and format [2]', marks=2)
    nf_ = [f for f, _ in fields if f in NUMF]
    f = r.choice(nf_)
    if kind == 'update':
        nv = x[f] + (1 if isinstance(x[f], int) else 0.5)
        nv = round(nv, 2)
        sql = f'UPDATE {name} SET {f} = {sqlv(nv)} WHERE {pk} = {sqlv(x[pk])};'
        return Q(f'Write an SQL statement to change the {f} of the record with {pk} {x[pk]} to {sqlv(nv)} in the table {name}.', sql, f'{sql} — 1 mark UPDATE {name} SET; 1 mark WHERE {pk} [2]', marks=2)
    v = sorted(y[f] for y in rows)[1]
    sql = f'DELETE FROM {name} WHERE {f} < {sqlv(v)};'
    n = sum(1 for y in rows if y[f] < v)
    return Q(f'{tbl_text(name, rows)}\nWrite an SQL statement to delete every record where {f} is less than {sqlv(v)}, and state how many records would be deleted.', f'{sql} {n} record{"s" if n != 1 else ""} deleted',
             f'{sql} [2]; {n} [1] [3]', marks=3)


def _join(r, D):
    custs = [{'CustomerID': f'C{i}', 'Name': n, 'Town': city(r)} for i, n in zip(r.sample(range(10, 60), 4), r.sample(FIRST, 4))]
    sales = []
    for k in range(6):
        c = r.choice(custs)
        sales.append({'SaleID': str(500 + k), 'CustomerID': c['CustomerID'], 'Total': r.randrange(20, 400)})
    lim = sorted(s['Total'] for s in sales)[2]
    return custs, sales, lim


@t11_4.add('C4', (3, 4, 5), 'multi_step')
def t11_4_join(r, D):
    custs, sales, lim = _join(r, D)
    names = {c['CustomerID']: c['Name'] for c in custs}
    res = [(names[s['CustomerID']], s['Total']) for s in sales if s['Total'] > lim]
    sql = f'SELECT CUSTOMER.Name, SALE.Total FROM CUSTOMER INNER JOIN SALE ON CUSTOMER.CustomerID = SALE.CustomerID WHERE SALE.Total > {lim};'
    stem = (f'{tbl_text("CUSTOMER", custs)}\n{tbl_text("SALE", sales)}\n(a) Identify the foreign key in SALE. (b) Write an SQL query to display the Name of the customer and the Total for every sale with a Total greater than {lim}. '
            f'(c) State the output of your query. (d) Explain why the relationship is one-to-many.')
    return Q(stem, f'(a) CustomerID (b) {sql} (c) ' + ('; '.join(f'{a}, {t}' for a, t in res) or 'no rows') + ' (d) one customer can have many sales, each sale belongs to one customer',
             f'(a) [1] (b) SELECT fields with table names [1]; INNER JOIN ... ON [1]; WHERE [1] (c) correct rows [2] (d) [1]', marks=7, typ='multi_step')


@t11_4.add('C2', (2, 3, 4), 'explain')
def t11_4_err(r, D):
    name, rows, cols, conds, conj, order, sel, sql, fields = _query(r, 2)
    kind = r.choice(['quote', 'from', 'order', 'where'])
    if kind == 'quote' and any(isinstance(v, str) for _, _, v in conds):
        bad = sql.replace("'", '')
        why = 'String (text) values in a condition must be enclosed in quotation marks.'
    elif kind == 'from':
        bad = sql.replace(f' FROM {name}', '')
        why = f'The FROM clause naming the table {name} is missing.'
    elif kind == 'order' and order:
        bad = sql.replace('ORDER BY', 'SORT BY')
        why = 'SQL uses ORDER BY, not SORT BY.'
    else:
        bad = sql.replace(' WHERE ', ' IF ')
        why = 'Conditions are introduced with WHERE, not IF.'
    d = ctx(r)
    return Q(f'{d["p"]} writes this SQL query: {bad} Identify the error and write the corrected query.', f'{why} Correct: {sql}', '1 mark: error identified; 1 mark: corrected query [2]')


CHAPTERS[11] = [t11_1, t11_2, t11_3, t11_4]

# =============================================================================== Pseudocode program generators (used in chapters 12-15)
IND = '    '


def pc_for_mod(r, D):
    tot, cnt = r.choice(['Total', 'Sum', 'Result']), r.choice(['Count', 'Index', 'Num'])
    a = r.randrange(1, 6)
    bb = a + r.randrange(5, 10 if D < 4 else 16)
    k = r.choice([2, 3, 4, 5])
    act = r.choice(['add', 'count'])
    lines = [f'{tot} ← 0', f'FOR {cnt} ← {a} TO {bb}', f'{IND}IF {cnt} MOD {k} = 0 THEN',
             f'{IND}{IND}{tot} ← {tot} + {cnt if act == "add" else 1}', f'{IND}ENDIF', f'NEXT {cnt}', f'OUTPUT {tot}']
    v = sum((i if act == 'add' else 1) for i in range(a, bb + 1) if i % k == 0)
    trace = [i for i in range(a, bb + 1) if i % k == 0]
    return lines, str(v), f'{cnt} values divisible by {k}: {", ".join(map(str, trace)) or "none"}; {tot} = {v}'


def pc_while(r, D):
    x, st = r.choice(['Value', 'X', 'Amount']), r.choice(['Steps', 'Count', 'Turns'])
    s = r.randrange(1, 6)
    m = r.choice([2, 3])
    lim = r.randrange(20, 200)
    add = r.choice([0, 1]) if D >= 3 else 0
    lines = [f'{x} ← {s}', f'{st} ← 0', f'WHILE {x} < {lim}', f'{IND}{x} ← {x} * {m}' + (f' + {add}' if add else ''), f'{IND}{st} ← {st} + 1', 'ENDWHILE', f'OUTPUT {x}, " ", {st}']
    v, n, seq = s, 0, [s]
    while v < lim:
        v = v * m + add
        n += 1
        seq.append(v)
    return lines, f'{v} {n}', f'{x} takes the values {", ".join(map(str, seq))}; loop runs {n} times'


def pc_repeat(r, D):
    nn, dg = r.choice(['Number', 'N', 'Temp']), r.choice(['Digits', 'Count', 'Total'])
    base = r.choice([10, 2]) if D >= 3 else 10
    n = r.randrange(10, 99999) if base == 10 else r.randrange(5, 300)
    mode = r.choice(['count', 'sum']) if base == 10 else 'count'
    lines = [f'{nn} ← {n}', f'{dg} ← 0', 'REPEAT']
    if mode == 'count':
        lines += [f'{IND}{nn} ← {nn} DIV {base}', f'{IND}{dg} ← {dg} + 1']
    else:
        lines += [f'{IND}{dg} ← {dg} + {nn} MOD 10', f'{IND}{nn} ← {nn} DIV 10']
    lines += [f'UNTIL {nn} = 0', f'OUTPUT {dg}']
    v, cnt, seq = n, 0, []
    while True:
        if mode == 'count':
            v //= base
            cnt += 1
        else:
            cnt += v % 10
            v //= 10
        seq.append(v)
        if v == 0:
            break
    return lines, str(cnt), f'{nn} becomes {", ".join(map(str, seq))}; {dg} = {cnt}'


def pc_case(r, D):
    vals = [r.randrange(1, 30) for _ in range(4 if D < 4 else 6)]
    k = 3
    lab = r.sample(['"Red"', '"Blue"', '"Green"', '"Gold"', '"Pink"'], 3)
    lines = [f'DECLARE Codes : ARRAY[1:{len(vals)}] OF INTEGER', '// Codes contains ' + ', '.join(map(str, vals)), f'FOR i ← 1 TO {len(vals)}', f'{IND}CASE OF Codes[i] MOD {k}',
             f'{IND}{IND}0 : OUTPUT {lab[0]}', f'{IND}{IND}1 : OUTPUT {lab[1]}', f'{IND}{IND}OTHERWISE OUTPUT {lab[2]}', f'{IND}ENDCASE', 'NEXT i']
    out = [lab[0] if v % k == 0 else (lab[1] if v % k == 1 else lab[2]) for v in vals]
    return lines, ' '.join(o.strip('"') for o in out), '; '.join(f'{v} MOD 3 = {v % 3} → {o.strip(chr(34))}' for v, o in zip(vals, out))


def pc_array(r, D):
    n = 6 if D < 4 else 8
    vals = [r.randrange(1, 60) for _ in range(n)]
    nm = r.choice(['Scores', 'Marks', 'Temps', 'Sales'])
    mode = r.choice(['max', 'count', 'min'])
    t = r.randrange(15, 45)
    if mode == 'max':
        lines = [f'// {nm} contains ' + ', '.join(map(str, vals)), f'Best ← {nm}[1]', 'Pos ← 1', f'FOR i ← 2 TO {n}', f'{IND}IF {nm}[i] > Best THEN', f'{IND}{IND}Best ← {nm}[i]', f'{IND}{IND}Pos ← i', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Best, " ", Pos']
        b_ = max(vals)
        return lines, f'{b_} {vals.index(b_) + 1}', f'largest value {b_} first found at position {vals.index(b_) + 1}'
    if mode == 'min':
        lines = [f'// {nm} contains ' + ', '.join(map(str, vals)), f'Low ← {nm}[1]', f'FOR i ← 2 TO {n}', f'{IND}IF {nm}[i] < Low THEN', f'{IND}{IND}Low ← {nm}[i]', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Low']
        return lines, str(min(vals)), f'smallest value {min(vals)}'
    lines = [f'// {nm} contains ' + ', '.join(map(str, vals)), 'Above ← 0', f'FOR i ← 1 TO {n}', f'{IND}IF {nm}[i] >= {t} THEN', f'{IND}{IND}Above ← Above + 1', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Above']
    c = sum(1 for v in vals if v >= t)
    return lines, str(c), f'values ≥ {t}: {", ".join(str(v) for v in vals if v >= t) or "none"}; count {c}'


WORDS = ['ALGORITHM', 'COMPUTER', 'PROCEDURE', 'VARIABLE', 'NETWORK', 'DATABASE', 'ITERATION', 'SELECTION', 'PROGRAM', 'INTERRUPT', 'REGISTER', 'COMPILER', 'KEYBOARD', 'ENCRYPTION']


def pc_string(r, D):
    w = r.choice(WORDS)
    mode = r.choice(['vowel', 'rev', 'skip'])
    if mode == 'vowel':
        lines = [f'Word ← "{w}"', 'V ← 0', 'FOR i ← 1 TO LENGTH(Word)', f'{IND}Ch ← MID(Word, i, 1)', f'{IND}IF Ch = "A" OR Ch = "E" OR Ch = "I" OR Ch = "O" OR Ch = "U" THEN', f'{IND}{IND}V ← V + 1', f'{IND}ENDIF', 'NEXT i', 'OUTPUT V']
        v = sum(1 for c in w if c in 'AEIOU')
        return lines, str(v), f'vowels in {w}: {v}'
    if mode == 'rev':
        lines = [f'Word ← "{w}"', 'NewWord ← ""', 'FOR i ← LENGTH(Word) TO 1 STEP -1', f'{IND}NewWord ← NewWord & MID(Word, i, 1)', 'NEXT i', 'OUTPUT NewWord']
        return lines, w[::-1], f'characters taken from the end: {w[::-1]}'
    s = r.choice([1, 2])
    lines = [f'Word ← "{w}"', 'Out ← ""', f'FOR i ← {s} TO LENGTH(Word) STEP 2', f'{IND}Out ← Out & MID(Word, i, 1)', 'NEXT i', 'OUTPUT Out']
    return lines, w[s - 1::2], f'characters at positions {s}, {s + 2}, ...: {w[s - 1::2]}'


def pc_nested(r, D):
    a, c = r.randrange(2, 5), r.randrange(2, 5)
    lines = ['Total ← 0', f'FOR Row ← 1 TO {a}', f'{IND}FOR Col ← 1 TO {c}', f'{IND}{IND}Total ← Total + Row * Col', f'{IND}NEXT Col', 'NEXT Row', 'OUTPUT Total']
    v = sum(i * j for i in range(1, a + 1) for j in range(1, c + 1))
    return lines, str(v), f'sum of Row × Col for Row 1–{a}, Col 1–{c} = {v}; inner statement runs {a * c} times'


PC_GENS = [pc_for_mod, pc_while, pc_repeat, pc_case, pc_array, pc_string, pc_nested]

# =============================================================================== Chapter 12 Algorithm design and problem-solving
t12_1 = topic('Computational thinking: abstraction and decomposition', 'computational thinking', 'abstraction', 'decomposition')
t12_1.fixed('C1', (1, 2), [
    ('What is abstraction?', 'Removing unnecessary details to focus on the essential features of a problem', 'Abstraction keeps only what is relevant (e.g. a metro map shows stations and lines, not distances).', ['Breaking a problem into smaller parts', 'Writing code in a high-level language', 'Testing every possible input']),
    ('What is decomposition?', 'Breaking a complex problem down into smaller, more manageable sub-problems', 'Each sub-problem can be solved (and coded as a module) separately.', ['Removing unnecessary details', 'Converting a program to machine code', 'Deleting unused variables']),
    ('Which is an example of abstraction?', 'A train map that shows stations and connections but not exact distances', 'Only the details needed by travellers are kept.', ['Dividing a game into modules for input, logic and display', 'Testing a program with boundary data', 'Writing comments in code']),
    ('What is pattern recognition in computational thinking?', 'Identifying similarities between problems so existing solutions can be reused', 'e.g. recognising that two reports both need sorting.', ['Removing details from a problem', 'Writing a flowchart', 'Running a program step by step']),
])
t12_1.fixed('C2', (2, 3, 4), [
    ('Explain two benefits of decomposition when developing a large program.', 'Each sub-problem is easier to understand and solve; modules can be written and tested by different programmers at the same time; modules can be reused.', '1 mark per benefit, max 2 [2]'),
    ('Explain why abstraction is useful when designing a computer model of a real system.', 'It removes irrelevant details so the model is simpler, faster to build and run, and focuses on the factors that affect the result.', '1 mark each [2]'),
])
scen(t12_1, 'C3', (2, 3, 4), [
    '{org} in {city} wants a program to manage online bookings.',
    '{p} is designing a mobile game in which a player moves through a city collecting coins.',
    'A school wants a program to produce student timetables.',
    '{org} needs a system to calculate monthly pay for its staff.',
], [('Decompose the problem into four sub-problems.', 'e.g. input data; validate data; process/calculate; store records; produce output/reports.', '1 mark per sensible sub-problem, max 4 [4]'),
    ('Give two details that could be removed through abstraction, and two that must be kept.', 'Removed: irrelevant features (colours, exact locations, unrelated personal details); kept: data needed for the processing.', '1 mark per detail [4]'),
    ('Explain how decomposition helps a team of programmers work on this project.', 'Sub-problems assigned to different programmers, developed and tested in parallel, then combined.', '1 mark each [2]'),
    ('Explain how one module from this project could be reused in another project.', 'e.g. a validation or login module can be used unchanged in a different program, saving time.', '1 mark each [2]')], k=(2, 3))
scen(t12_1, 'C4', (3, 4, 5), [
    '{org} in {city} is building a route-planning app for its delivery drivers.',
    '{p} is leading the design of a library management system for {org}.',
], [('Use abstraction to describe the data the system needs to store and what can be ignored.', 'Keep only the data needed for processing (e.g. locations, connections and times; or books, members and loans); ignore appearance and unrelated details.', '1 mark per point, max 3 [3]'),
    ('Decompose the system into modules and describe the purpose of each.', 'e.g. login, input orders/books, search, calculate route/due dates, output map/report.', '1 mark per module with purpose, max 4 [4]'),
    ('Explain how pattern recognition could save development time.', 'Identifying that tasks (e.g. searching lists) are similar means one routine can be written and reused.', '1 mark each [2]')], k=(2, 3))

t12_2 = topic('Writing algorithms in structured English, flowcharts and pseudocode; identifiers and identifier tables', 'writing algorithms', 'structured english', 'flowcharts', 'pseudocode', 'identifier tables')
t12_2.fixed('C1', (1, 2), [
    ('What is an algorithm?', 'A sequence of steps that can be carried out to perform a task', 'Algorithms can be shown in structured English, flowcharts or pseudocode.', ['A program written in machine code', 'A type of variable', 'A diagram of a network']),
    ('Which flowchart symbol is used for a decision?', 'A diamond', 'Decision: diamond with two exits (Yes/No); process: rectangle; input/output: parallelogram; start/stop: rounded rectangle.', ['A rectangle', 'A parallelogram', 'A rounded rectangle']),
    ('Which flowchart symbol represents input or output?', 'A parallelogram', 'Input/output: parallelogram.', ['A diamond', 'A rectangle', 'A circle']),
    ('In Cambridge pseudocode, which symbol is used for assignment?', '←', 'e.g. Total ← Total + 1.', ['=', ':=', '=='], ),
    ('What is an identifier table?', 'A table listing each identifier used, its data type and its purpose', 'Identifier tables document variables, constants and arrays.', ['A table of the program\'s output', 'A list of error messages', 'A test plan']),
    ('What is structured English?', 'A restricted form of English using keywords to describe the steps of an algorithm', 'e.g. "IF the mark is above 50 THEN output Pass".', ['A programming language', 'A type of flowchart', 'Text that cannot be read by people']),
])
t12_2.fixed('C2', (2, 3, 4), [
    ('Explain why pseudocode is used to design algorithms.', 'It is independent of any programming language so it can be understood by all programmers and easily converted to code; it focuses on logic, not syntax.', '1 mark each point, max 2 [2]'),
    ('Explain why meaningful identifier names should be used.', 'They make the algorithm/code easier to read, understand, debug and maintain, by the author and by others.', '1 mark each [2]'),
])


def _task(r, D):
    d = ctx(r)
    n = r.randrange(5, 31)
    thing = r.choice([('temperature', 'REAL', 'temperatures'), ('mark', 'INTEGER', 'marks'), ('price', 'REAL', 'prices'), ('height', 'REAL', 'heights'), ('score', 'INTEGER', 'scores'), ('age', 'INTEGER', 'ages')])
    t = r.randrange(10, 90)
    kind = r.choice(['avg', 'max', 'count', 'valid']) if D >= 3 else r.choice(['avg', 'count', 'max'])
    return d, n, thing, t, kind


@t12_2.add('C3', (2, 3, 4, 5))
def t12_2_write(r, D):
    d, n, (one, typ, many), t, kind = _task(r, D)
    if kind == 'avg':
        desc = f'input {n} {many} and output their average'
        code_ = ['DECLARE Total : REAL', f'DECLARE Value : {typ}', 'DECLARE Count : INTEGER', 'Total ← 0', f'FOR Count ← 1 TO {n}', f'{IND}INPUT Value', f'{IND}Total ← Total + Value', 'NEXT Count', f'OUTPUT Total / {n}']
        pts = ['initialise total', f'loop {n} times', 'input inside loop', 'add to total', f'output total / {n}']
    elif kind == 'max':
        desc = f'input {n} {many} and output the highest {one}'
        code_ = [f'DECLARE Value, Highest : {typ}', 'DECLARE Count : INTEGER', 'INPUT Value', 'Highest ← Value', f'FOR Count ← 2 TO {n}', f'{IND}INPUT Value', f'{IND}IF Value > Highest THEN', f'{IND}{IND}Highest ← Value', f'{IND}ENDIF', 'NEXT Count', 'OUTPUT Highest']
        pts = ['initialise highest from first value', 'loop for remaining values', 'compare with highest', 'update highest', 'output after loop']
    elif kind == 'count':
        desc = f'input {n} {many} and output how many are greater than {t}'
        code_ = [f'DECLARE Value : {typ}', 'DECLARE Count, Above : INTEGER', 'Above ← 0', f'FOR Count ← 1 TO {n}', f'{IND}INPUT Value', f'{IND}IF Value > {t} THEN', f'{IND}{IND}Above ← Above + 1', f'{IND}ENDIF', 'NEXT Count', 'OUTPUT Above']
        pts = ['initialise counter to 0', f'loop {n} times', 'input in loop', f'IF value > {t}', 'increment counter and output after loop']
    else:
        desc = f'input a {one} and keep asking until it is between 0 and {t} inclusive, then output it'
        code_ = [f'DECLARE Value : {typ}', 'REPEAT', f'{IND}OUTPUT "Enter a {one} between 0 and {t}"', f'{IND}INPUT Value', f'UNTIL Value >= 0 AND Value <= {t}', 'OUTPUT Value']
        pts = ['prompt', 'input', 'post-condition (or pre-condition) loop', f'correct condition 0..{t}', 'output after loop']
    m = min(5, D + 1)
    return Q(f'{d["p"]} needs an algorithm for {d["org"]} to {desc}. Write the algorithm in pseudocode, declaring all variables.', code(code_),
             'Mark points: ' + '; '.join(pts) + f'. 1 mark per point, max {m} [{m}]', marks=m)


@t12_2.add('C3', (1, 2, 3, 4))
def t12_2_trace(r, D):
    lines, out, why = r.choice(PC_GENS)(r, D)
    stem = 'Study the pseudocode algorithm.\n' + code(lines) + '\nState the output.'
    if D == 1:
        alts = []
        for o in [out + '0', out[::-1], str(len(out))]:
            alts.append(o)
        try:
            v = int(out)
            alts += [str(v + 1), str(v - 1), str(v * 2)]
        except ValueError:
            pass
        return MCQ(r, stem.replace('State the output.', 'What is output?'), out, alts, why + '.')
    return Q(stem, out, f'{why} [2]', marks=2)


IDENT = [('the number of tickets sold', 'TicketsSold', 'INTEGER'), ('the price of one ticket in dollars', 'TicketPrice', 'REAL'), ('whether a customer is a member', 'IsMember', 'BOOLEAN'),
         ('a customer\'s surname', 'Surname', 'STRING'), ('the date of the booking', 'BookingDate', 'DATE'), ('a single grade letter', 'Grade', 'CHAR'),
         ('the running total of money taken', 'TotalTaken', 'REAL'), ('a counter for the loop', 'Count', 'INTEGER'), ('the average temperature', 'AverageTemp', 'REAL'),
         ('a product code such as "P0193"', 'ProductCode', 'STRING'), ('whether the input is valid', 'ValidInput', 'BOOLEAN'), ('the menu choice entered as one key press', 'Choice', 'CHAR')]


@t12_2.add('C3', (2, 3, 4))
def t12_2_ident(r, D):
    ch = r.sample(IDENT, 3 if D < 4 else 4)
    d = ctx(r)
    stem = f'{d["p"]} is writing a program for {d["org"]}. Complete an identifier table giving a suitable identifier and data type for each of: ' + '; '.join(c[0] for c in ch) + '.'
    return Q(stem, '; '.join(f'{c[1]} : {c[2]}' for c in ch), '1 mark per row with meaningful identifier and correct data type: ' + '; '.join(f'{c[0]} → {c[1]} {c[2]}' for c in ch) + f' [{len(ch)}]', marks=len(ch))


@t12_2.add('C4', (2, 3, 4, 5), 'multi_step')
def t12_2_flow(r, D):
    lines, out, why = r.choice([pc_while, pc_for_mod, pc_repeat])(r, D)
    stem = ('An algorithm is shown in pseudocode.\n' + code(lines) + '\n(a) State the output. (b) Identify the type of loop used and explain why it is suitable. (c) Describe how the algorithm would be shown as a flowchart, naming the symbols used.')
    loop = 'count-controlled FOR loop: number of repetitions known' if any(l.startswith('FOR') for l in lines) else ('pre-condition WHILE loop: may run zero times, condition checked first' if any(l.startswith('WHILE') for l in lines) else 'post-condition REPEAT loop: runs at least once')
    return Q(stem, f'(a) {out} (b) {loop} (c) terminators for start/stop, rectangles for assignments, diamond for the loop condition with Yes/No branches, parallelogram for output, arrows showing the loop back',
             f'(a) {why} [2] (b) loop type [1]; reason [1] (c) correct symbols [2]', marks=6, typ='multi_step')


@t12_2.add('C2', (2, 3, 4), 'explain')
def t12_2_bug(r, D):
    d, n, (one, typ, many), t, kind = _task(r, 2)
    bug = r.choice(['init', 'bound', 'output'])
    if bug == 'init':
        lines = ['Total ← 0', f'FOR Count ← 1 TO {n}', f'{IND}Total ← 0', f'{IND}INPUT Value', f'{IND}Total ← Total + Value', 'NEXT Count', f'OUTPUT Total / {n}']
        fix = 'Line 3 sets Total to 0 inside the loop, so only the last value is kept; it should be removed (Total initialised once before the loop).'
    elif bug == 'bound':
        lines = ['Total ← 0', f'FOR Count ← 1 TO {n - 1}', f'{IND}INPUT Value', f'{IND}Total ← Total + Value', 'NEXT Count', f'OUTPUT Total / {n}']
        fix = f'The loop runs only {n - 1} times; line 2 should be FOR Count ← 1 TO {n}.'
    else:
        lines = ['Total ← 0', f'FOR Count ← 1 TO {n}', f'{IND}INPUT Value', f'{IND}Total ← Total + Value', f'{IND}OUTPUT Total / {n}', 'NEXT Count']
        fix = 'The OUTPUT is inside the loop so a value is output every time; it should be moved after NEXT Count.'
    return Q(f'This algorithm should input {n} {many} and output the average.\n' + code(lines) + '\nIdentify the error and explain how to correct it.', fix, '1 mark: error identified (line); 1 mark: correction [2]')


t12_3 = topic('Stepwise refinement of algorithms', 'stepwise refinement')
t12_3.fixed('C1', (1, 2), [
    ('What is stepwise refinement?', 'Breaking each step of an algorithm into smaller, more detailed steps until each can be coded directly', 'Top-down design: refine until each step is a single instruction or simple module.', ['Testing an algorithm with many inputs', 'Removing unnecessary steps from an algorithm', 'Converting a flowchart into a structure chart']),
    ('When should stepwise refinement stop?', 'When each step is detailed enough to be written directly as program code', 'Each final step corresponds to one or a few statements.', ['After exactly three levels', 'When the program compiles', 'When the algorithm has 10 steps']),
    ('Stepwise refinement is an example of which design approach?', 'Top-down design', 'Start with the whole problem and refine downwards.', ['Bottom-up testing', 'Black-box testing', 'Rapid application development']),
])
t12_3.fixed('C2', (2, 3, 4), [
    ('Explain the benefits of stepwise refinement.', 'Each step becomes simple to understand and code; errors are easier to find; the steps can become modules shared among a team.', '1 mark each point, max 2 [2]'),
])
REFINE = [('Process a customer order', ['Input order details', 'Validate the order', 'Calculate the total cost', 'Update stock levels', 'Output a receipt'],
           'Calculate the total cost', ['Set Total to 0', 'For each item, multiply quantity by price and add to Total', 'If Total > 100, apply 10% discount', 'Add delivery charge']),
          ('Produce a student report', ['Input student marks', 'Calculate the average', 'Assign a grade', 'Output the report'],
           'Assign a grade', ['IF average >= 70 THEN grade is A', 'ELSE IF average >= 55 THEN grade is B', 'ELSE IF average >= 40 THEN grade is C', 'ELSE grade is U']),
          ('Log in a user', ['Input username and password', 'Look up the stored password', 'Compare passwords', 'Allow or refuse access'],
           'Compare passwords', ['Hash the entered password', 'Compare with stored hash', 'If equal set Valid to TRUE', 'Otherwise add 1 to failed attempts and lock after 3']),
          ('Run a car park barrier', ['Detect car', 'Read ticket', 'Check payment', 'Open barrier', 'Close barrier'],
           'Check payment', ['Read ticket number', 'Look up entry time and amount paid', 'Calculate charge from time parked', 'If paid >= charge, set Allowed to TRUE'])]
scen(t12_3, 'C3', (2, 3, 4), [
    '{p} is designing a program for {org} in {city}.',
    'A team at {org} is refining an algorithm before coding it.',
], [lambda r, d: (lambda x: (f'The top-level task is "{x[0]}". Refine it into the main steps.', '; '.join(x[1]), f'1 mark per sensible step in logical order, max {min(4, len(x[1]))} [{min(4, len(x[1]))}]'))(r.choice(REFINE)),
    lambda r, d: (lambda x: (f'The step "{x[2]}" (part of "{x[0]}") needs further refinement. Write the refined steps.', '; '.join(x[3]), f'1 mark per refined step, max 4 [4]'))(r.choice(REFINE)),
    ('Explain how you know when refinement is complete.', 'Each step can be translated directly into one or a few program statements.', '1 mark [1]'),
    ('Explain how stepwise refinement helps the team to share the work.', 'Each refined step can become a module written and tested by a different person.', '1 mark each [2]')], k=(2, 3))


@t12_3.add('C4', (3, 4, 5), 'multi_step')
def t12_3_full(r, D):
    x = r.choice(REFINE)
    d = ctx(r)
    stem = (f'{d["org"]} in {d["city"]} needs a program to "{x[0].lower()}". (a) Use stepwise refinement to give the top-level steps. (b) Refine the step "{x[2]}" further. '
            f'(c) Write pseudocode for one of your refined steps. (d) Explain one advantage of designing the solution in this way.')
    return Q(stem, f'(a) {"; ".join(x[1])} (b) {"; ".join(x[3])} (c) e.g. pseudocode for {x[3][-1].lower()} (d) easier to code/test each step; modules can be shared',
             '(a) 1 mark per sensible step, max 3 [3] (b) 1 mark per refined step, max 3 [3] (c) correct pseudocode syntax and logic [2] (d) [1]', marks=9, typ='multi_step')


CHAPTERS[12] = [t12_1, t12_2, t12_3]

# =============================================================================== Chapter 13 Data types and structures
TYPES = [('a person\'s age in whole years', 'INTEGER'), ('the price of a meal, e.g. 12.50', 'REAL'), ('a single gender code such as "F"', 'CHAR'), ('a postcode such as "NA1 4PQ"', 'STRING'),
         ('whether a book is on loan', 'BOOLEAN'), ('a date of birth', 'DATE'), ('the number of students in a class', 'INTEGER'), ('a telephone number including the leading 0', 'STRING'),
         ('the average mark of a class', 'REAL'), ('whether a payment has been made', 'BOOLEAN'), ('a star rating of 1 to 5', 'INTEGER'), ('the distance of a race in kilometres, e.g. 21.1', 'REAL'),
         ('an employee\'s first name', 'STRING'), ('the date an order was dispatched', 'DATE'), ('a menu option chosen by a single key', 'CHAR')]
t13_1 = topic('Data types: INTEGER, REAL, CHAR, STRING, BOOLEAN, DATE; records', 'data types', 'integer, real, char, string, boolean, date', 'records')
t13_1.fixed('C1', (1, 2), [
    ('Which data type stores TRUE or FALSE?', 'BOOLEAN', 'BOOLEAN: two values only.', ['CHAR', 'INTEGER', 'STRING']),
    ('What is a record (composite) data type?', 'A data structure that groups together related items of different data types under one identifier', 'e.g. TYPE Student with Name : STRING, Age : INTEGER.', ['An array of the same data type', 'A single character', 'A text file']),
    ('Why is a telephone number usually stored as a STRING rather than an INTEGER?', 'It may start with 0 or contain spaces/+ signs and is never used in calculations', 'Leading zeros would be lost as an integer.', ['STRING uses less memory', 'INTEGER cannot store large numbers', 'STRING is faster to sort numerically']),
    ('In Cambridge pseudocode, how is a record type started?', 'TYPE <identifier>', 'TYPE TStudent ... ENDTYPE.', ['RECORD <identifier>', 'DECLARE TYPE', 'STRUCT <identifier>']),
    ('Which data type would store the value 3.75?', 'REAL', 'REAL holds numbers with a fractional part.', ['INTEGER', 'CHAR', 'BOOLEAN']),
])
t13_1.fixed('C2', (2, 3, 4), [
    ('Explain why a record is useful for storing data about a book in a library program.', 'All the fields about one book (title, author, ISBN, on loan) of different types are kept together under one identifier, so they can be passed, stored and processed as one item; an array of records can store many books.', '1 mark: groups related data of different types; 1 mark: processed/stored together or array of records [2]'),
    ('Explain the difference between CHAR and STRING.', 'CHAR holds exactly one character; STRING holds a sequence of zero or more characters.', '1 mark each [2]'),
])


@t13_1.add('C3', (1, 2, 3, 4))
def t13_1_type(r, D):
    if D <= 2:
        x = r.choice(TYPES)
        return MCQ(r, f'Which is the most suitable data type to store {x[0]}?', x[1], [t for t in ['INTEGER', 'REAL', 'CHAR', 'STRING', 'BOOLEAN', 'DATE'] if t != x[1]], f'{x[0]}: {x[1]}.')
    xs = r.sample(TYPES, 4)
    return Q('State the most suitable data type for each item and give a reason for one of them: ' + '; '.join(f'({i + 1}) {x[0]}' for i, x in enumerate(xs)) + '.',
             '; '.join(f'({i + 1}) {x[1]}' for i, x in enumerate(xs)), '1 mark per correct type: ' + '; '.join(x[1] for x in xs) + '; 1 mark reason [5]', marks=5)


RECS = [('TBook', [('Title', 'STRING'), ('Author', 'STRING'), ('YearPublished', 'INTEGER'), ('Price', 'REAL'), ('OnLoan', 'BOOLEAN')], 'a book in a library'),
        ('TPatient', [('PatientID', 'STRING'), ('Surname', 'STRING'), ('DateOfBirth', 'DATE'), ('Weight', 'REAL'), ('Insured', 'BOOLEAN')], 'a patient at a clinic'),
        ('TCar', [('Registration', 'STRING'), ('Make', 'STRING'), ('Seats', 'INTEGER'), ('DailyRate', 'REAL'), ('Available', 'BOOLEAN')], 'a car for hire'),
        ('TStudent', [('StudentID', 'STRING'), ('FirstName', 'STRING'), ('Form', 'STRING'), ('Grade', 'CHAR'), ('Average', 'REAL')], 'a student'),
        ('TFlight', [('FlightNumber', 'STRING'), ('Destination', 'STRING'), ('DepartureDate', 'DATE'), ('SeatsLeft', 'INTEGER'), ('Delayed', 'BOOLEAN')], 'a flight')]


@t13_1.add('C3', (2, 3, 4, 5))
def t13_1_rec(r, D):
    nm, fs, what = r.choice(RECS)
    d = ctx(r)
    lines = [f'TYPE {nm}'] + [f'{IND}DECLARE {f} : {t}' for f, t in fs] + ['ENDTYPE']
    n = r.choice([50, 100, 200, 500])
    stem = f'{d["org"]} stores data about {what}: ' + ', '.join(f'{f}' for f, _ in fs) + f'. Write pseudocode to declare a record type {nm} for this data' + (f', then declare an array of {n} records and assign {fs[2][0]} for the first record.' if D >= 4 else '.')
    ans = code(lines + ([f'DECLARE Items : ARRAY[1:{n}] OF {nm}', f'Items[1].{fs[2][0]} ← ...'] if D >= 4 else []))
    return Q(stem, ans, '1 mark TYPE/ENDTYPE; 1 mark per two fields with correct types' + ('; 1 mark array of records; 1 mark dot notation' if D >= 4 else '') + f' [{(5 if D >= 4 else 3)}]', marks=5 if D >= 4 else 3)


t13_2 = topic('1D and 2D arrays; linear search and bubble sort', '1d and 2d arrays', 'linear search', 'bubble sort')
t13_2.fixed('C1', (1, 2), [
    ('What is an array?', 'A data structure holding a fixed number of items of the same data type under one identifier, accessed by index', 'e.g. DECLARE Marks : ARRAY[1:30] OF INTEGER.', ['A collection of fields of different data types', 'A file stored on disk', 'A single variable that can change type']),
    ('In a bubble sort, what happens in each pass?', 'Adjacent items are compared and swapped if they are in the wrong order', 'After pass 1 the largest item is in its final position (ascending sort).', ['The smallest item is moved to the start in one step', 'The list is split in half', 'Each item is inserted into a new list']),
    ('In the worst case, how many comparisons does a linear search make on a list of 50 items?', '50', 'Every item may need checking (item last or not present).', ['25', '6', '1']),
    ('What is the lower bound of the array DECLARE Data : ARRAY[0:9] OF INTEGER?', '0', 'Bounds are [lower:upper]; this array has 10 elements.', ['1', '9', '10']),
    ('How many elements does DECLARE Grid : ARRAY[1:4, 1:6] OF CHAR have?', '24', '4 rows × 6 columns.', ['10', '20', '6']),
    ('Why might a bubble sort use a flag variable?', 'To stop early if a pass makes no swaps, because the list is already sorted', 'Improved bubble sort: if no swaps in a pass, finish.', ['To count the number of items', 'To mark the middle of the list', 'To reverse the list']),
])
t13_2.fixed('C2', (2, 3, 4), [
    ('Explain why a linear search can be used on an unsorted list but a binary search cannot.', 'Linear search checks each element in turn so order does not matter; binary search relies on the list being in order to discard half each time.', '1 mark each [2]'),
    ('Explain how the efficiency of a bubble sort can be improved.', 'Stop when a pass makes no swaps (flag); reduce the number of comparisons in each pass by one, since the end of the list is already sorted.', '1 mark each [2]'),
])


def bubble_pass(a):
    a = a[:]
    sw = 0
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
            sw += 1
    return a, sw


@t13_2.add('C3', (1, 2, 3, 4, 5))
def t13_2_bubble(r, D):
    n = 6 if D < 4 else 8
    a = r.sample(range(1, 99), n)
    p1, s1 = bubble_pass(a)
    if D == 1:
        return MCQ(r, f'The array {a} is sorted into ascending order using a bubble sort. What is the array after the first pass?', str(p1), [str(sorted(a)), str(a[::-1]), str(bubble_pass(p1)[0]) if bubble_pass(p1)[0] != p1 else str(a[1:] + a[:1])], f'Compare neighbours and swap: {p1} ({s1} swaps).')
    if D <= 3:
        return Q(f'The array {a} is sorted into ascending order using a bubble sort. Give the contents of the array after the first pass and state the number of swaps made.', f'{p1}; {s1} swaps', f'{p1} [2]; {s1} swaps [1] [3]', marks=3)
    passes, cur, tot = 0, a, 0
    while True:
        cur, s = bubble_pass(cur)
        passes += 1
        tot += s
        if s == 0:
            break
    p2 = bubble_pass(p1)[0]
    return Q(f'The array {a} is sorted into ascending order using a bubble sort that stops when a pass makes no swaps. Give the array after pass 2, the total number of swaps, and the number of passes made.',
             f'{p2}; {tot} swaps; {passes} passes', f'after pass 2: {p2} [2]; total swaps {tot} [1]; passes {passes} (including the final pass with no swaps) [1] [4]', marks=4)


@t13_2.add('C3', (1, 2, 3, 4))
def t13_2_search(r, D):
    n = r.randrange(7, 11)
    a = r.sample(range(1, 80), n)
    t = r.choice(a + [r.choice([x for x in range(1, 80) if x not in a])])
    found = t in a
    cmp = a.index(t) + 1 if found else n
    stem = f'A linear search is used to look for {t} in the array {a}. State how many comparisons are made and the result of the search.'
    ans = f'{cmp} comparisons; ' + (f'found at index {a.index(t) + 1}' if found else 'not found')
    if D == 1:
        return MCQ(r, f'A linear search is used to look for {t} in the array {a}. How many comparisons are made?', str(cmp), [str(cmp + 1), str(cmp - 1 if cmp > 1 else n + 1), str(n // 2), str(n - cmp + 1) if n - cmp + 1 != cmp else str(n + 2)], ans)
    return Q(stem, ans, f'{ans} (index counted from 1) [2]', marks=2)


@t13_2.add('C3', (2, 3, 4, 5))
def t13_2_2d(r, D):
    rows, cols = r.randrange(2, 4), r.randrange(3, 5)
    g = [[r.randrange(1, 20) for _ in range(cols)] for _ in range(rows)]
    i, j = r.randrange(rows), r.randrange(cols)
    k = r.randrange(rows)
    txt = '; '.join(f'row {x + 1}: ' + ', '.join(map(str, g[x])) for x in range(rows))
    stem = f'A 2D array Grid is declared as ARRAY[1:{rows}, 1:{cols}] OF INTEGER and contains {txt}. State the value of Grid[{i + 1}, {j + 1}] and the sum of row {k + 1}.'
    m = 2
    if D >= 4:
        stem += f' Then write pseudocode using nested loops to output the total of all elements.'
        m = 5
    ans = f'{g[i][j]}; {sum(g[k])}' + (f'; total {sum(map(sum, g))}: Total ← 0 / FOR R ← 1 TO {rows} / FOR C ← 1 TO {cols} / Total ← Total + Grid[R, C] / NEXT C / NEXT R / OUTPUT Total' if D >= 4 else '')
    return Q(stem, ans, f'Grid[{i + 1}, {j + 1}] = {g[i][j]} [1]; row sum {sum(g[k])} [1]' + ('; initialise total [1]; nested loops with correct bounds [1]; accumulate and output [1]' if D >= 4 else '') + f' [{m}]', marks=m)


@t13_2.add('C4', (3, 4, 5), 'multi_step')
def t13_2_write(r, D):
    nm = r.choice(['Scores', 'Prices', 'Codes', 'Times'])
    n = r.choice([10, 20, 50, 100])
    stem = (f'An array {nm} holds {n} integers. (a) Write pseudocode for a bubble sort that sorts {nm} into ascending order and stops early if no swaps are made in a pass. '
            f'(b) Explain why the number of comparisons in each pass can be reduced by one each time.')
    ans = code(['Boundary ← ' + str(n - 1), 'REPEAT', f'{IND}NoSwaps ← TRUE', f'{IND}FOR j ← 1 TO Boundary', f'{IND}{IND}IF {nm}[j] > {nm}[j + 1] THEN', f'{IND}{IND}{IND}Temp ← {nm}[j]',
                f'{IND}{IND}{IND}{nm}[j] ← {nm}[j + 1]', f'{IND}{IND}{IND}{nm}[j + 1] ← Temp', f'{IND}{IND}{IND}NoSwaps ← FALSE', f'{IND}{IND}ENDIF', f'{IND}NEXT j', f'{IND}Boundary ← Boundary - 1',
                'UNTIL NoSwaps = TRUE OR Boundary = 0']) + '\n(b) After each pass the largest remaining value is in its final place at the end, so it need not be compared again.'
    return Q(stem, ans, '(a) outer loop until no swaps [1]; flag reset/set [1]; inner loop with correct bound [1]; comparison of adjacent elements [1]; swap using temp [1]; boundary reduced [1] (b) [1]', marks=7, typ='multi_step')


@t13_2.add('C2', (2, 3, 4), 'explain')
def t13_2_err(r, D):
    n = r.randrange(6, 12)
    bug = r.choice(['bound', 'swap'])
    if bug == 'bound':
        lines = [f'FOR j ← 1 TO {n}', f'{IND}IF Data[j] > Data[j + 1] THEN', f'{IND}{IND}Temp ← Data[j]', f'{IND}{IND}Data[j] ← Data[j + 1]', f'{IND}{IND}Data[j + 1] ← Temp', f'{IND}ENDIF', 'NEXT j']
        fix = f'The loop runs to {n}, so Data[j + 1] refers to Data[{n + 1}], which is outside the array bounds [1:{n}]. Change line 1 to FOR j ← 1 TO {n - 1}.'
    else:
        lines = [f'FOR j ← 1 TO {n - 1}', f'{IND}IF Data[j] > Data[j + 1] THEN', f'{IND}{IND}Data[j] ← Data[j + 1]', f'{IND}{IND}Data[j + 1] ← Data[j]', f'{IND}ENDIF', 'NEXT j']
        fix = 'The swap overwrites Data[j] before it is saved, so both elements end up with the same value. Use a temporary variable: Temp ← Data[j]; Data[j] ← Data[j + 1]; Data[j + 1] ← Temp.'
    return Q(f'This pseudocode is one pass of a bubble sort on the array Data[1:{n}].\n' + code(lines) + '\nIdentify the error and explain how to correct it.', fix, '1 mark: error identified; 1 mark: correction [2]')


t13_3 = topic('Text files: reading, writing and appending', 'text files', 'reading, writing and appending')
t13_3.fixed('C1', (1, 2), [
    ('Which file mode adds new lines to the end of an existing text file?', 'APPEND', 'OPENFILE <name> FOR APPEND; WRITE overwrites/creates.', ['WRITE', 'READ', 'RANDOM']),
    ('What happens if a file is opened FOR WRITE and it already exists?', 'Its existing contents are replaced', 'WRITE creates a new file or overwrites the old one.', ['New data is added to the end', 'An error always occurs', 'The file is opened read-only']),
    ('Which function tests whether the end of a file has been reached?', 'EOF()', 'WHILE NOT EOF("Data.txt") ... ENDWHILE.', ['END()', 'LENGTH()', 'CLOSEFILE()']),
    ('Which statement reads one line from a text file into a variable?', 'READFILE "Data.txt", Line', 'READFILE <file>, <variable>.', ['INPUT "Data.txt", Line', 'GETRECORD "Data.txt", Line', 'OPENFILE Line FOR READ']),
    ('Why should a file be closed after use?', 'So that all data is written and the file is released for other programs', 'CLOSEFILE flushes buffers and frees the file.', ['To delete the file', 'To encrypt the file', 'To sort the file']),
    ('Why is data stored in a file rather than only in variables?', 'Variables are lost when the program ends; files keep data permanently', 'Files provide persistent storage between runs.', ['Files are faster than RAM', 'Variables cannot hold strings', 'Files cannot be changed']),
])
t13_3.fixed('C2', (2, 3, 4), [
    ('Explain the difference between opening a file for WRITE and for APPEND.', 'WRITE creates a new file (or overwrites an existing one) and writes from the start; APPEND keeps the existing contents and adds new data to the end.', '1 mark each [2]'),
])
FILELINES = [['Red', 'Blue', 'Green', 'Red', 'Yellow', 'Blue', 'Red'], ['Lima', 'Cairo', 'Doha', 'Lisbon', 'Lagos', 'Dubai'], ['45', '72', '18', '90', '63', '27', '51'],
             ['apple', 'banana', 'cherry', 'avocado', 'blueberry', 'apricot'], ['Tiger', 'Lion', 'Tapir', 'Llama', 'Toucan', 'Lemur']]


@t13_3.add('C3', (2, 3, 4, 5))
def t13_3_trace(r, D):
    lines_ = r.choice(FILELINES)[:]
    r.shuffle(lines_)
    fn = r.choice(['Data.txt', 'Words.txt', 'Items.txt', 'Log.txt'])
    if lines_[0].isdigit():
        t = r.randrange(30, 70)
        code_ = ['Count ← 0', f'OPENFILE "{fn}" FOR READ', f'WHILE NOT EOF("{fn}")', f'{IND}READFILE "{fn}", Line', f'{IND}IF STR_TO_NUM(Line) > {t} THEN', f'{IND}{IND}Count ← Count + 1', f'{IND}ENDIF', 'ENDWHILE', f'CLOSEFILE "{fn}"', 'OUTPUT Count']
        out = str(sum(1 for x in lines_ if int(x) > t))
    else:
        c0 = r.choice(sorted({x[0] for x in lines_}))
        code_ = ['Count ← 0', f'OPENFILE "{fn}" FOR READ', f'WHILE NOT EOF("{fn}")', f'{IND}READFILE "{fn}", Line', f'{IND}IF LEFT(Line, 1) = "{c0}" THEN', f'{IND}{IND}OUTPUT Line', f'{IND}{IND}Count ← Count + 1', f'{IND}ENDIF', 'ENDWHILE', f'CLOSEFILE "{fn}"', 'OUTPUT Count']
        sel = [x for x in lines_ if x[0] == c0]
        out = ' '.join(sel + [str(len(sel))])
    stem = f'The text file {fn} contains these lines, in order: {", ".join(lines_)}.\n' + code(code_) + '\nState the output.'
    return Q(stem, out, f'Each line read until EOF and tested: output {out} [2]', marks=2)


@t13_3.add('C3', (2, 3, 4, 5))
def t13_3_write(r, D):
    d = ctx(r)
    fn = r.choice(['Members.txt', 'Scores.txt', 'Orders.txt', 'Visitors.txt'])
    mode = r.choice(['append', 'copy', 'write'])
    if mode == 'append':
        task = f'input a name from the user and add it to the end of the existing file {fn}'
        ans = ['DECLARE Name : STRING', 'INPUT Name', f'OPENFILE "{fn}" FOR APPEND', f'WRITEFILE "{fn}", Name', f'CLOSEFILE "{fn}"']
        pts = 'input; OPENFILE ... FOR APPEND; WRITEFILE; CLOSEFILE'
        m = 4
    elif mode == 'write':
        n = r.randrange(3, 11)
        task = f'input {n} lines of text and store them in a new file {fn}'
        ans = [f'OPENFILE "{fn}" FOR WRITE', f'FOR i ← 1 TO {n}', f'{IND}INPUT Line', f'{IND}WRITEFILE "{fn}", Line', 'NEXT i', f'CLOSEFILE "{fn}"']
        pts = f'OPENFILE FOR WRITE; loop {n} times; input and WRITEFILE inside loop; CLOSEFILE'
        m = 4
    else:
        task = f'copy every line of {fn} that is not empty into a new file Backup.txt'
        ans = [f'OPENFILE "{fn}" FOR READ', 'OPENFILE "Backup.txt" FOR WRITE', f'WHILE NOT EOF("{fn}")', f'{IND}READFILE "{fn}", Line', f'{IND}IF Line <> "" THEN', f'{IND}{IND}WRITEFILE "Backup.txt", Line', f'{IND}ENDIF', 'ENDWHILE', f'CLOSEFILE "{fn}"', 'CLOSEFILE "Backup.txt"']
        pts = 'open both files in correct modes; loop until EOF; READFILE; test for empty line; WRITEFILE; close both files'
        m = 6
    return Q(f'{d["p"]} is writing a program for {d["org"]}. Write pseudocode to {task}.', code(ans), f'1 mark each: {pts} [{m}]', marks=m)


scen(t13_3, 'C4', (3, 4, 5), [
    '{org} in {city} records each visitor\'s name in a text file called Visitors.txt.',
    '{p} keeps a log of sensor readings in a text file called Readings.txt.',
], [('Explain why the program should open the file in APPEND mode when adding a new entry.', 'APPEND keeps the existing data and adds to the end; WRITE would erase all previous entries.', '1 mark each [2]'),
    ('Write pseudocode to output every line in the file.', 'OPENFILE ... FOR READ; WHILE NOT EOF(...); READFILE ..., Line; OUTPUT Line; ENDWHILE; CLOSEFILE ...', '1 mark open; 1 mark loop to EOF; 1 mark read and output; 1 mark close [4]'),
    ('Write pseudocode to count the number of lines in the file.', 'Count ← 0; OPENFILE FOR READ; WHILE NOT EOF; READFILE; Count ← Count + 1; ENDWHILE; CLOSEFILE; OUTPUT Count', '1 mark initialise; 1 mark loop/read; 1 mark increment; 1 mark output [4]'),
    ('Explain why the file must be closed after use.', 'Ensures buffered data is written and the file is available to other programs.', '1 mark each [2]')], k=(2, 3))


def stack_sim(r, D):
    size = 6
    ops, st, popped = [], [], []
    for _ in range(r.randrange(5, 8) if D < 4 else r.randrange(7, 11)):
        if st and (r.random() < 0.35 or len(st) == size):
            ops.append('POP')
            popped.append(st.pop())
        else:
            v = r.randrange(1, 50)
            ops.append(f'PUSH {v}')
            st.append(v)
    return ops, st, popped


def queue_sim(r, D):
    q, out, ops = [], [], []
    front, rear = 1, 0
    for _ in range(r.randrange(5, 8) if D < 4 else r.randrange(7, 10)):
        if q and r.random() < 0.35:
            ops.append('DEQUEUE')
            out.append(q.pop(0))
            front += 1
        elif rear < 8:
            v = r.randrange(1, 50)
            ops.append(f'ENQUEUE {v}')
            q.append(v)
            rear += 1
    return ops, q, out, front, rear


t13_4 = topic('Abstract data types: stack, queue and linked list', 'abstract data types', 'stack', 'queue', 'linked list')
t13_4.fixed('C1', (1, 2), [
    ('A stack is described as', 'last in, first out (LIFO)', 'Items are pushed onto and popped from the top.', ['first in, first out (FIFO)', 'sorted in ascending order', 'accessed by any index directly']),
    ('A queue is described as', 'first in, first out (FIFO)', 'Items join at the rear and leave from the front.', ['last in, first out (LIFO)', 'a structure with no order', 'a list accessed only from the middle']),
    ('What is an abstract data type (ADT)?', 'A collection of data together with the operations that can be performed on it, defined independently of its implementation', 'e.g. stack with push/pop.', ['A data type built into every language', 'A type of file', 'A variable that has not been declared']),
    ('In a linked list, what does each node contain?', 'Data and a pointer to the next node', 'The last node has a null pointer; a start pointer gives the first node.', ['Only data', 'Only a pointer', 'An index to every other node']),
    ('Which ADT would be used to store the order of web pages visited so the Back button works?', 'Stack', 'The most recently visited page is returned first: LIFO.', ['Queue', 'Linked list sorted alphabetically', 'Binary file']),
    ('Which ADT is used to hold print jobs waiting for a printer?', 'Queue', 'Jobs are printed in the order they arrive: FIFO.', ['Stack', 'Record', 'Two-dimensional array']),
    ('What is stack overflow?', 'Trying to push an item onto a stack that is already full', 'Underflow: popping from an empty stack.', ['Popping from an empty stack', 'A stack with exactly one item', 'Deleting the stack']),
])
t13_4.fixed('C2', (2, 3, 4), [
    ('Explain why a linked list can be more efficient than an array when items are frequently inserted in order.', 'Inserting in an array means moving many elements along to make space; in a linked list only pointers are changed.', '1 mark each [2]'),
    ('Explain the role of the null pointer in a linked list.', 'It marks the end of the list (the last node points to nothing), and an empty list has a null start pointer.', '1 mark each [2]'),
])


@t13_4.add('C3', (1, 2, 3, 4, 5))
def t13_4_stack(r, D):
    ops, st, popped = stack_sim(r, D)
    stem = f'An empty stack is implemented with an array Stack[1:6] and a pointer TopOfStack that is 0 when the stack is empty. The operations {", ".join(ops)} are performed in order. Give the contents of the stack (bottom to top), the value of TopOfStack and the values popped.'
    ans = f'Stack: {", ".join(map(str, st)) or "empty"}; TopOfStack = {len(st)}; popped: {", ".join(map(str, popped)) or "none"}'
    if D == 1:
        return MCQ(r, f'An empty stack has the operations {", ".join(ops)} performed in order. What is the value at the top of the stack afterwards?' if st else f'An empty stack has the operations {", ".join(ops)} performed. How many items remain?',
                   str(st[-1]) if st else '0', [str(x) for x in (st[:-1] + popped + [len(st) + 1, len(st) + 2])] if st else ['1', '2', '3'], ans)
    return Q(stem, ans, f'contents [1]; TopOfStack {len(st)} [1]; popped values in order [1] [3]', marks=3)


@t13_4.add('C3', (2, 3, 4, 5))
def t13_4_queue(r, D):
    ops, q, out, front, rear = queue_sim(r, D)
    stem = f'A linear queue uses an array Queue[1:8] with FrontPointer = 1 and RearPointer = 0 when empty. ENQUEUE adds 1 to RearPointer then stores the item; DEQUEUE removes the item at FrontPointer then adds 1 to FrontPointer. The operations {", ".join(ops)} are performed. Give the items in the queue (front to rear), FrontPointer, RearPointer and the items removed.'
    ans = f'Queue: {", ".join(map(str, q)) or "empty"}; FrontPointer = {front}; RearPointer = {rear}; removed: {", ".join(map(str, out)) or "none"}'
    return Q(stem, ans, f'items [1]; FrontPointer {front} [1]; RearPointer {rear} [1]; removed in order [1] [4]', marks=4)


@t13_4.add('C3', (2, 3, 4, 5))
def t13_4_list(r, D):
    words = r.sample(['Ant', 'Bee', 'Cat', 'Dog', 'Eel', 'Fox', 'Gnu', 'Hen', 'Owl', 'Yak'], 5 if D < 4 else 6)
    order = sorted(words)
    slots = list(range(1, len(words) + 1))
    r.shuffle(slots)
    pos = {w: s for w, s in zip(order, slots)}
    table = {s: (w, (pos[order[i + 1]] if i + 1 < len(order) else -1)) for i, (w, s) in enumerate(pos.items())}
    start = pos[order[0]]
    txt = '; '.join(f'[{s}] {table[s][0]} → {table[s][1]}' for s in sorted(table))
    stem = f'A linked list is stored in arrays of data and pointers (−1 is the null pointer). StartPointer = {start}. Nodes: {txt}. Give the data items in the order they are visited.'
    m = 2
    if D >= 4:
        new = r.choice([w for w in ['Ape', 'Bat', 'Cod', 'Elk', 'Gar', 'Jay', 'Koi'] if w not in words])
        merged = sorted(words + [new])
        i = merged.index(new)
        prev = merged[i - 1] if i > 0 else None
        nxt = merged[i + 1] if i + 1 < len(merged) else None
        stem += f' The item {new} is stored in a free node at index {len(words) + 1} to keep the list in alphabetical order. State which pointers change and their new values.'
        chg = (f'{prev}\'s pointer (node {pos[prev]}) becomes {len(words) + 1}' if prev else f'StartPointer becomes {len(words) + 1}') + f'; the new node\'s pointer becomes {pos[nxt] if nxt else -1}'
        return Q(stem, f'{", ".join(order)}; {chg}', f'order [2]; pointer changes: {chg} [2] [4]', marks=4)
    return Q(stem, ', '.join(order), f'Follow pointers from {start}: {", ".join(order)} [{m}]', marks=m)


scen(t13_4, 'C4', (3, 4, 5), [
    'A printer at {org} in {city} receives documents from 20 computers.',
    '{p} is writing a text editor that needs an "undo" feature.',
    'A ticket booking system at {org} must serve customers in the order they join an online waiting room.',
], [('Identify the most suitable ADT and justify your choice.', 'Queue for printing/waiting room (FIFO); stack for undo (LIFO).', '1 mark ADT; 1 mark justification [2]'),
    ('Describe how the ADT can be implemented using an array and pointers.', 'Array of fixed size; stack: TopOfStack pointer incremented on push, decremented on pop; queue: front and rear pointers.', '1 mark array; 1 mark pointers; 1 mark how they change [3]'),
    ('Explain what should happen if an item is added when the structure is full.', 'Report an error (overflow) and do not store the item / wait.', '1 mark [1]'),
    ('Write pseudocode for a procedure to add an item to the ADT you chose, implemented as an array.', 'Stack: IF TopOfStack = MaxSize THEN OUTPUT "Full" ELSE TopOfStack ← TopOfStack + 1; Stack[TopOfStack] ← Item ENDIF. Queue: IF RearPointer = MaxSize THEN OUTPUT "Full" ELSE RearPointer ← RearPointer + 1; Queue[RearPointer] ← Item ENDIF', '1 mark full check; 1 mark increment pointer; 1 mark store item [3]')], k=(2, 3))

ar(t13_1, [('A telephone number should be stored as a STRING.', 'It can begin with 0 and is not used in calculations.'),
           ('A record can store data of different types.', 'Each field of a record is declared with its own data type.'),
           ('The price of an item should be stored as REAL.', 'Prices can have a fractional part.'),
           ('A BOOLEAN variable is suitable for recording whether a member has paid.', 'BOOLEAN can only hold TRUE or FALSE.')],
   ['A CHAR variable can hold a whole word.', 'An array can store items of different data types.', 'INTEGER can store the value 4.5.', 'A DATE must be stored as a REAL number.'])
ar(t13_2, [('A binary search cannot be used on an unsorted array.', 'Binary search discards half of the items each time by comparing with the middle item, which depends on order.'),
           ('A bubble sort can stop early if a pass makes no swaps.', 'A pass with no swaps means every pair of adjacent items is in order.'),
           ('After the first pass of an ascending bubble sort, the largest item is at the end.', 'The largest item is swapped with each neighbour until it reaches the end.'),
           ('A linear search on 100 items may need 100 comparisons.', 'In the worst case the item is last or not present.')],
   ['A linear search only works on sorted arrays.', 'A bubble sort compares items that are far apart.', 'ARRAY[1:5, 1:4] has 9 elements.', 'A bubble sort always needs exactly one pass.'])
ar(t13_4, [('A stack is suitable for an undo feature.', 'A stack is last in, first out, so the most recent action is undone first.'),
           ('A queue is suitable for print jobs.', 'A queue is first in, first out, so jobs are printed in the order they arrive.'),
           ('Inserting into an ordered linked list does not require data to be moved.', 'Only the pointers need to be changed.'),
           ('Popping from an empty stack causes an error.', 'There is no item at the top of the stack to remove (underflow).')],
   ['A queue removes the most recently added item first.', 'A linked list must be stored in consecutive memory locations.', 'A stack has a front pointer and a rear pointer.', 'The null pointer marks the start of a linked list.'])


@t13_4.add('C2', (2, 3, 4), 'explain')
def t13_4_cmp(r, D):
    ops, st, popped = stack_sim(r, 2)
    d = ctx(r)
    first = next((o.split()[1] for o in ops if o.startswith('PUSH')), None)
    if not popped or first is None:
        return None
    return Q(f'{d["p"]} performs the operations {", ".join(ops)} on an empty stack and says the first value removed should be {first} because it was added first. Explain why {d["p"]} is wrong.',
             f'A stack is LIFO: POP removes the item at the top (the most recently pushed), so the first value removed is {popped[0]}.', f'1 mark: LIFO explained; 1 mark: correct value {popped[0]} [2]')


@t13_2.add('C2', (2, 3, 4), 'explain')
def t13_2_claim(r, D):
    a = r.sample(range(1, 99), 7)
    t = r.choice(a)
    d = ctx(r)
    return Q(f'{d["p"]} wants to use a binary search to find {t} in the array {a}. Explain why this will not work reliably and what should be done.',
             'The array is not sorted, so comparing with the middle item does not tell you which half contains the target. Either sort the array first or use a linear search.', '1 mark: array unsorted/binary search needs order; 1 mark: sort first or use linear search [2]')


@t13_1.add('C2', (2, 3, 4), 'explain')
def t13_1_claim(r, D):
    x = r.choice(TYPES)
    wrong = r.choice([t for t in ['INTEGER', 'REAL', 'CHAR', 'STRING', 'BOOLEAN', 'DATE'] if t != x[1]])
    d = ctx(r)
    return Q(f'{d["p"]} declares a variable to store {x[0]} using the data type {wrong}. Explain why this is not the best choice and state a better data type.', f'{x[1]} is better: {wrong} would not represent the value correctly or efficiently.',
             f'1 mark: reason {wrong} is unsuitable; 1 mark: {x[1]} [2]')


CHAPTERS[13] = [t13_1, t13_2, t13_3, t13_4]
scen(t13_1, 'C4', (3, 4, 5), [
    '{org} in {city} is writing a program to store details of its stock items.',
    '{p} is designing a program for a sports club to store details of its members.',
], [('Explain why a record type is more suitable than several separate arrays for this data.', 'All the data about one item is kept together, so there is no risk of the arrays getting out of step; easier to pass and store.', '1 mark each [2]'),
    lambda r, d: (lambda x: (f'Write pseudocode to declare a record type {x[0]} with the fields ' + ', '.join(f for f, _ in x[1]) + '.', code([f'TYPE {x[0]}'] + [f'{IND}DECLARE {f} : {t}' for f, t in x[1]] + ['ENDTYPE']),
                         '1 mark TYPE/ENDTYPE; 1 mark per two correct fields [3]'))(r.choice(RECS)),
    ('Justify the choice of data type for a field that stores money.', 'REAL, because amounts have a fractional (cents) part.', '1 mark type; 1 mark reason [2]'),
    ('Write a pseudocode statement to declare an array of 100 of these records.', 'DECLARE Items : ARRAY[1:100] OF <record type>', '1 mark bounds; 1 mark OF record type [2]'),
    ('Explain why a date of birth should be stored using the DATE type rather than STRING.', 'Dates can be compared, sorted and used in calculations (e.g. age) correctly; validation of real dates.', '1 mark each [2]')], k=(3, 4))

# =============================================================================== Chapter 14 Programming
def _fn_expr(r, D):
    w = r.choice(['Computer', 'Keyboard', 'Monitor', 'Network', 'Printer', 'Software', 'Hardware', 'Database', 'Internet', 'Password', 'Variable', 'Function'])
    n = len(w)
    opts = []
    x = r.randrange(1, n - 2)
    y = r.randrange(1, n - x + 1)
    opts.append((f'MID("{w}", {x}, {y})', w[x - 1:x - 1 + y], f'start at character {x}, take {y} characters'))
    k = r.randrange(1, n)
    opts.append((f'LEFT("{w}", {k})', w[:k], f'first {k} characters'))
    opts.append((f'RIGHT("{w}", {k})', w[-k:], f'last {k} characters'))
    opts.append((f'LENGTH("{w}")', str(n), 'number of characters'))
    opts.append((f'TO_UPPER(LEFT("{w}", {k}))', w[:k].upper(), f'first {k} characters in upper case'))
    a, c = r.randrange(10, 100), r.randrange(2, 9)
    opts.append((f'{a} MOD {c}', str(a % c), f'remainder of {a} ÷ {c}'))
    opts.append((f'{a} DIV {c}', str(a // c), f'integer quotient of {a} ÷ {c}'))
    f = r.randrange(10, 999) / 10
    opts.append((f'INT({f:g})', str(int(f)), 'whole number part'))
    if D >= 3:
        opts.append((f'LEFT("{w}", {k}) & RIGHT("{w}", 2)', w[:k] + w[-2:], 'concatenates the first characters and the last two'))
        opts.append((f'LENGTH("{w}") MOD {c}', str(n % c), f'length {n} MOD {c}'))
        opts.append((f'MID("{w}", LENGTH("{w}") - {min(3, n - 1)}, 2)', w[n - min(3, n - 1) - 1:n - min(3, n - 1) + 1], f'start at position {n - min(3, n - 1)}'))
        opts.append((f'NUM_TO_STR({a}) & NUM_TO_STR({c})', f'{a}{c}', 'numbers converted to strings and joined'))
        opts.append((f'STR_TO_NUM("{a}") + {c}', str(a + c), 'string converted to a number then added'))
        opts.append((f'ASC("{w[0]}")', str(ord(w[0])), 'ASCII value of the character'))
    return r.choice(opts)


t14_1 = topic('Programming basics: variables, constants, input, output, assignment and built-in functions (string and numeric)', 'programming basics', 'variables, constants', 'built-in functions')
t14_1.fixed('C1', (1, 2), [
    ('What is a constant?', 'A named value that cannot change while the program is running', 'CONSTANT VAT = 0.2; makes code easier to read and update.', ['A variable that is always 0', 'A value input by the user', 'A loop counter']),
    ('What is the purpose of DECLARE in Cambridge pseudocode?', 'To give a variable an identifier and a data type', 'e.g. DECLARE Count : INTEGER.', ['To output a value', 'To input a value', 'To create a constant']),
    ('Which operator joins two strings in Cambridge pseudocode?', '&', 'Concatenation: "Hello " & Name.', ['+', 'MOD', '//']),
    ('What does the function RAND(10) return?', 'A random REAL number in the range 0 to 10 (not including 10)', 'RAND(x) returns a real between 0 and x.', ['A random integer from 1 to 10', 'The number 10', 'A random string of 10 characters']),
    ('What is meant by assignment?', 'Giving a value to a variable', 'e.g. Total ← Total + Mark.', ['Comparing two values', 'Displaying a value on screen', 'Declaring a procedure']),
    ('Why is it good practice to use a constant for the VAT rate in a program?', 'If the rate changes it only has to be updated in one place', 'Constants improve readability and maintainability.', ['Constants run faster than variables', 'Variables cannot store decimals', 'It is a syntax rule']),
])
t14_1.fixed('C2', (2, 3, 4), [
    ('Explain the difference between a variable and a constant.', 'A variable\'s value can change while the program runs; a constant is given a value once and cannot be changed.', '1 mark each [2]'),
    ('Explain why a programmer should declare variables before use.', 'The translator knows each variable\'s data type and allocates memory; typing errors in identifiers are detected; the code is easier to understand.', '1 mark per point, max 2 [2]'),
])


@t14_1.add('C3', (1, 2, 3, 4, 5))
def t14_1_fn(r, D):
    e, v, why = _fn_expr(r, D)
    if D == 1:
        dis = [v[::-1], v + v[-1:], v[1:] or 'x', str(len(v))] if not v.isdigit() else [str(int(v) + 1), str(max(0, int(v) - 1)), str(int(v) * 2), v + '0']
        return MCQ(r, f'What value is returned by {e}?', v, dis, f'{e}: {why} → {v}.')
    if D >= 4:
        e2, v2, why2 = _fn_expr(r, D)
        if e2 == e:
            return None
        return Q(f'State the value returned by each expression: (i) {e} (ii) {e2}', f'(i) {v} (ii) {v2}', f'(i) {why}: {v} [1] (ii) {why2}: {v2} [1] [2]', marks=2)
    return Q(f'State the value returned by the expression {e}.', v, f'{why}: {v} [1]')


@t14_1.add('C3', (2, 3, 4, 5))
def t14_1_write(r, D):
    d = ctx(r)
    task = r.choice([
        ('input a full name such as "Ana Silva" and output the initials', ['INPUT FullName', 'Space ← 0', 'FOR i ← 1 TO LENGTH(FullName)', f'{IND}IF MID(FullName, i, 1) = " " THEN', f'{IND}{IND}Space ← i', f'{IND}ENDIF', 'NEXT i', 'OUTPUT LEFT(FullName, 1) & MID(FullName, Space + 1, 1)'], 'input; find space; first initial; second initial; output'),
        ('input a price and a quantity and output the total cost including tax, using a constant TaxRate of 0.15', ['CONSTANT TaxRate = 0.15', 'DECLARE Price : REAL', 'DECLARE Quantity : INTEGER', 'INPUT Price', 'INPUT Quantity', 'OUTPUT Price * Quantity * (1 + TaxRate)'], 'constant; declarations; inputs; calculation; output'),
        ('input a password and output "Valid" if it has at least 8 characters, otherwise "Too short"', ['DECLARE Password : STRING', 'INPUT Password', 'IF LENGTH(Password) >= 8 THEN', f'{IND}OUTPUT "Valid"', 'ELSE', f'{IND}OUTPUT "Too short"', 'ENDIF'], 'input; LENGTH; condition ≥ 8; both outputs'),
        ('input a number of seconds and output it as minutes and seconds', ['DECLARE Total, Minutes, Seconds : INTEGER', 'INPUT Total', 'Minutes ← Total DIV 60', 'Seconds ← Total MOD 60', 'OUTPUT Minutes, " minutes ", Seconds, " seconds"'], 'input; DIV 60; MOD 60; output'),
        ('input a word and output it with the first letter in upper case and the rest in lower case', ['INPUT Word', 'Result ← TO_UPPER(LEFT(Word, 1)) & TO_LOWER(RIGHT(Word, LENGTH(Word) - 1))', 'OUTPUT Result'], 'input; LEFT/TO_UPPER; RIGHT with LENGTH − 1/TO_LOWER; concatenation and output'),
        ('generate and output a random whole number between 1 and 6 to simulate a dice', ['Dice ← INT(RAND(6)) + 1', 'OUTPUT Dice'], 'RAND(6); INT; + 1; output'),
    ])
    m = len(task[2].split(';'))
    return Q(f'{d["p"]} is writing a program for {d["org"]}. Write pseudocode to {task[0]}.', code(task[1]), f'1 mark each: {task[2]} [{m}]', marks=m)


scen(t14_1, 'C4', (3, 4, 5), [
    '{org} in {city} needs a program to create usernames for new staff.',
    '{p} is writing a program for {org} in {city} that creates usernames for new staff members.',
], [('A username is the first three letters of the surname followed by the year of joining. Write pseudocode to input the surname and year and output the username.', 'INPUT Surname; INPUT Year; Username ← LEFT(Surname, 3) & NUM_TO_STR(Year); OUTPUT Username', '1 mark inputs; 1 mark LEFT; 1 mark NUM_TO_STR and &; 1 mark output [4]'),
    lambda r, d: (lambda e: (f'State the value of {e[0]}.', e[1], f'{e[2]} [1]'))(_fn_expr(r, 3)),
    ('Explain why a constant should be used for the maximum length of a code.', 'The value can be changed in one place and the code is easier to understand.', '1 mark each [2]'),
    ('Describe the difference between the DIV and MOD operators.', 'DIV gives the whole-number quotient; MOD gives the remainder.', '1 mark each [2]')], k=(2, 3))

t14_2 = topic('Constructs: selection (IF, CASE) and iteration (count-controlled, pre-condition and post-condition loops)', 'constructs', 'selection (if, case)', 'iteration', 'pre-condition and post-condition loops')
t14_2.fixed('C1', (1, 2), [
    ('Which type of loop always executes its body at least once?', 'Post-condition loop (REPEAT ... UNTIL)', 'The condition is checked at the end.', ['Pre-condition loop (WHILE ... ENDWHILE)', 'Count-controlled loop (FOR ... NEXT)', 'IF ... ENDIF']),
    ('Which loop is most suitable when the number of repetitions is known in advance?', 'Count-controlled loop (FOR ... NEXT)', 'FOR loops repeat a fixed number of times.', ['REPEAT ... UNTIL', 'WHILE ... ENDWHILE', 'CASE OF']),
    ('Which construct chooses between several alternatives based on the value of one variable?', 'CASE OF ... ENDCASE', 'CASE OF with OTHERWISE for unmatched values.', ['FOR ... NEXT', 'REPEAT ... UNTIL', 'WHILE ... ENDWHILE']),
    ('A WHILE loop condition is false the first time it is checked. How many times does the body run?', '0', 'Pre-condition: checked before the body.', ['1', 'It runs forever', '2']),
    ('Which statement ends an IF block in Cambridge pseudocode?', 'ENDIF', 'IF ... THEN ... ELSE ... ENDIF.', ['END IF THEN', 'NEXT', 'ENDCASE']),
    ('What is nesting?', 'Placing one construct inside another, such as a loop inside a loop', 'e.g. an IF inside a FOR loop.', ['Joining two strings', 'Declaring two variables on one line', 'Calling a function']),
])
t14_2.fixed('C2', (2, 3, 4), [
    ('Explain the difference between a pre-condition loop and a post-condition loop.', 'A pre-condition loop tests the condition before the body, so may run zero times; a post-condition loop tests after the body, so always runs at least once.', '1 mark each [2]'),
    ('Explain when a CASE statement is better than nested IF statements.', 'When one variable is compared with several possible values; CASE is clearer and easier to read and maintain than many nested IFs.', '1 mark each [2]'),
])


@t14_2.add('C3', (1, 2, 3, 4, 5))
def t14_2_trace(r, D):
    lines, out, why = r.choice(PC_GENS)(r, D)
    if D == 1:
        alts = [out[::-1], out + '1']
        try:
            v = int(out.split()[0])
            alts += [str(v + 1), str(v - 1) if v > 0 else str(v + 2), str(v * 2) if v else '2']
        except ValueError:
            alts += [out.lower(), out[1:] or 'x']
        return MCQ(r, 'What is output by this pseudocode?\n' + code(lines), out, alts, why + '.')
    if D >= 4:
        return Q('Study the pseudocode.\n' + code(lines) + '\n(a) Complete a trace and state the output. (b) Identify the type of each construct used.', f'(a) {out} (b) iteration (' + ('count-controlled' if any(l.startswith('FOR') for l in lines) else ('pre-condition' if any(l.startswith('WHILE') for l in lines) else 'post-condition')) + ')' + (' and selection' if any('IF' in l or 'CASE' in l for l in lines) else ''),
                 f'(a) {why}: {out} [3] (b) constructs named [1] [4]', marks=4)
    return Q('Study the pseudocode.\n' + code(lines) + '\nState the output.', out, f'{why} [2]', marks=2)


@t14_2.add('C3', (2, 3, 4, 5))
def t14_2_convert(r, D):
    a, c = r.randrange(1, 5), r.randrange(6, 15)
    st = r.choice([1, 2, 3])
    v = r.choice(['Count', 'i', 'Index'])
    kind = r.choice(['while', 'repeat'])
    lines = [f'FOR {v} ← {a} TO {c}' + (f' STEP {st}' if st > 1 else ''), f'{IND}OUTPUT {v} * {v}', f'NEXT {v}']
    out = ' '.join(str(i * i) for i in range(a, c + 1, st))
    if kind == 'while':
        ans = [f'{v} ← {a}', f'WHILE {v} <= {c}', f'{IND}OUTPUT {v} * {v}', f'{IND}{v} ← {v} + {st}', 'ENDWHILE']
    else:
        ans = [f'{v} ← {a}', 'REPEAT', f'{IND}OUTPUT {v} * {v}', f'{IND}{v} ← {v} + {st}', f'UNTIL {v} > {c}']
    return Q('Rewrite this pseudocode using a ' + ('pre-condition (WHILE)' if kind == 'while' else 'post-condition (REPEAT)') + ' loop that gives the same output, and state the output.\n' + code(lines),
             code(ans) + f'\nOutput: {out}', f'1 mark initialise {v}; 1 mark correct condition; 1 mark increment by {st}; 1 mark output {out} [4]', marks=4)


@t14_2.add('C3', (2, 3, 4))
def t14_2_select(r, D):
    bands = sorted(r.sample(range(30, 90, 5), 3), reverse=True)
    grades = ['A', 'B', 'C']
    lines = ['INPUT Mark', f'IF Mark >= {bands[0]} THEN', f'{IND}Grade ← "A"', 'ELSE', f'{IND}IF Mark >= {bands[1]} THEN', f'{IND}{IND}Grade ← "B"', f'{IND}ELSE', f'{IND}{IND}IF Mark >= {bands[2]} THEN',
             f'{IND}{IND}{IND}Grade ← "C"', f'{IND}{IND}ELSE', f'{IND}{IND}{IND}Grade ← "U"', f'{IND}{IND}ENDIF', f'{IND}ENDIF', 'ENDIF', 'OUTPUT Grade']
    tests = [bands[0], bands[1] - 1, bands[2], bands[2] - 1, r.randrange(bands[1], bands[0])]
    r.shuffle(tests)
    tests = tests[:3]

    def g(m):
        return 'A' if m >= bands[0] else ('B' if m >= bands[1] else ('C' if m >= bands[2] else 'U'))
    return Q('Study the pseudocode.\n' + code(lines) + f'\nState the output for the inputs {", ".join(map(str, tests))}.', ', '.join(g(m) for m in tests),
             '; '.join(f'{m} → {g(m)}' for m in tests) + ' [3]', marks=3)


@t14_2.add('C4', (3, 4, 5), 'multi_step')
def t14_2_task(r, D):
    d = ctx(r)
    lim = r.randrange(50, 200)
    stem = (f'{d["org"]} in {d["city"]} needs a program that repeatedly inputs the weight of a parcel in kg. Input stops when a weight of 0 is entered. Parcels over {lim // 10} kg cost $12, '
            f'parcels over 2 kg up to {lim // 10} kg cost $7 and other parcels cost $4. (a) Write pseudocode that outputs the cost of each parcel and the total cost at the end. (b) Justify your choice of loop.')
    ans = code(['Total ← 0', 'INPUT Weight', 'WHILE Weight <> 0', f'{IND}IF Weight > {lim // 10} THEN', f'{IND}{IND}Cost ← 12', f'{IND}ELSE', f'{IND}{IND}IF Weight > 2 THEN', f'{IND}{IND}{IND}Cost ← 7', f'{IND}{IND}ELSE',
                f'{IND}{IND}{IND}Cost ← 4', f'{IND}{IND}ENDIF', f'{IND}ENDIF', f'{IND}OUTPUT Cost', f'{IND}Total ← Total + Cost', f'{IND}INPUT Weight', 'ENDWHILE', 'OUTPUT Total']) + '\n(b) A pre-condition loop, because the number of parcels is not known and the first input may be 0.'
    return Q(stem, ans, '(a) initialise total [1]; input before loop and inside loop [1]; loop ends on 0 [1]; correct selection for three bands [2]; output cost and add to total [1]; output total after loop [1] (b) [1]', marks=8, typ='multi_step')


@t14_2.add('C2', (2, 3, 4), 'explain')
def t14_2_bug(r, D):
    lim = r.randrange(5, 20)
    kind = r.choice(['inf', 'off', 'cond'])
    if kind == 'inf':
        lines = ['Count ← 1', f'WHILE Count <= {lim}', f'{IND}OUTPUT Count', 'ENDWHILE']
        fix = 'Count is never changed inside the loop, so the condition is always true (infinite loop). Add Count ← Count + 1 before ENDWHILE.'
    elif kind == 'off':
        lines = ['Count ← 1', 'REPEAT', f'{IND}OUTPUT Count', f'{IND}Count ← Count + 1', f'UNTIL Count = {lim}']
        fix = f'The loop stops before outputting {lim}; the condition should be UNTIL Count > {lim}.'
    else:
        lines = ['INPUT Age', 'IF Age > 18 THEN', f'{IND}OUTPUT "Adult"', 'ELSE', f'{IND}OUTPUT "Child"', 'ENDIF']
        fix = 'An age of exactly 18 is treated as a child; the condition should be Age >= 18.'
    task = {'inf': f'output the numbers 1 to {lim}', 'off': f'output the numbers 1 to {lim}', 'cond': 'output "Adult" for anyone aged 18 or over'}[kind]
    return Q(f'This pseudocode should {task}.\n' + code(lines) + '\nIdentify the error and explain how to correct it.', fix, '1 mark: error; 1 mark: correction [2]')


def proc_prog(r, D):
    a, c = r.randrange(2, 10), r.randrange(2, 10)
    op1 = r.choice([('+', lambda x, y: x + y), ('*', lambda x, y: x * y), ('-', lambda x, y: x - y)])
    op2 = r.choice([('+ 1', lambda y: y + 1), ('* 2', lambda y: y * 2), ('- 1', lambda y: y - 1)])
    m1, m2 = r.choice([('BYREF', 'BYVAL'), ('BYVAL', 'BYREF'), ('BYREF', 'BYREF'), ('BYVAL', 'BYVAL')])
    lines = [f'PROCEDURE Change({m1} P : INTEGER, {m2} Q : INTEGER)', f'{IND}P ← P {op1[0]} Q', f'{IND}Q ← Q {op2[0]}', 'ENDPROCEDURE', '', f'X ← {a}', f'Y ← {c}', 'CALL Change(X, Y)', 'OUTPUT X, " ", Y']
    p = op1[1](a, c)
    q = op2[1](c)
    x = p if m1 == 'BYREF' else a
    y = q if m2 == 'BYREF' else c
    why = f'inside the procedure P = {p}, Q = {q}; X is passed {m1} so ' + ('changes' if m1 == 'BYREF' else 'is unchanged') + f'; Y is passed {m2} so ' + ('changes' if m2 == 'BYREF' else 'is unchanged')
    return lines, f'{x} {y}', why


t14_3 = topic('Structured programming: procedures, functions, parameters by value and by reference', 'structured programming', 'procedures, functions', 'parameters by value and by reference')
t14_3.fixed('C1', (1, 2), [
    ('What is the difference between a function and a procedure?', 'A function returns a value; a procedure does not have to', 'FUNCTION ... RETURNS <type>; procedures are called with CALL.', ['A procedure returns a value; a function does not', 'Functions cannot have parameters', 'There is no difference']),
    ('When a parameter is passed by reference, what is passed?', 'The address of the variable, so changes affect the original', 'BYREF: the subroutine works on the original variable.', ['A copy of the value', 'Nothing', 'The data type only']),
    ('When a parameter is passed by value, what is passed?', 'A copy of the value, so the original is not changed', 'BYVAL is the default in Cambridge pseudocode.', ['The memory address of the variable', 'The name of the variable', 'A pointer to the procedure']),
    ('What is a local variable?', 'A variable that can only be used within the subroutine in which it is declared', 'Local scope; global variables can be used anywhere.', ['A variable used everywhere in the program', 'A constant', 'A parameter passed by reference']),
    ('What is the header of a subroutine?', 'The first line, giving its identifier, parameters and (for a function) return type', 'e.g. FUNCTION Area(L : REAL, W : REAL) RETURNS REAL.', ['The comment at the top of the program', 'The last line of the subroutine', 'The call statement']),
    ('Which keyword is used to call a procedure in Cambridge pseudocode?', 'CALL', 'CALL ProcName(Params); functions are used in expressions.', ['RUN', 'RETURN', 'EXECUTE']),
])
t14_3.fixed('C2', (2, 3, 4), [
    ('Explain two benefits of using subroutines.', 'Code is written once and reused (shorter programs); each subroutine can be tested separately; easier to maintain; work shared among programmers; library routines.', '1 mark per benefit, max 2 [2]'),
    ('Explain why local variables are preferred to global variables.', 'They exist only while the subroutine runs, so they cannot be changed accidentally by other parts of the program; the same name can be reused; memory is freed.', '1 mark per point, max 2 [2]'),
])


@t14_3.add('C3', (1, 2, 3, 4, 5))
def t14_3_byref(r, D):
    lines, out, why = proc_prog(r, D)
    if D == 1:
        x, y = out.split()
        return MCQ(r, 'What is output by this pseudocode?\n' + code(lines), out, [f'{y} {x}', f'{lines[5][4:]} {lines[6][4:]}', f'{int(x) + 1} {y}', f'{x} {int(y) + 1}'], why + '.')
    return Q('Study the pseudocode.\n' + code(lines) + '\nState the output and explain your answer.', out, f'{why}: output {out} [3]', marks=3)


@t14_3.add('C3', (2, 3, 4, 5))
def t14_3_func(r, D):
    d = ctx(r)
    f = r.choice([
        ('Area', 'the area of a rectangle from its length and width', ['FUNCTION Area(Length : REAL, Width : REAL) RETURNS REAL', f'{IND}RETURN Length * Width', 'ENDFUNCTION'], 'header with two REAL parameters; RETURNS REAL; RETURN product; ENDFUNCTION'),
        ('IsEven', 'TRUE if an integer is even and FALSE otherwise', ['FUNCTION IsEven(N : INTEGER) RETURNS BOOLEAN', f'{IND}IF N MOD 2 = 0 THEN', f'{IND}{IND}RETURN TRUE', f'{IND}ELSE', f'{IND}{IND}RETURN FALSE', f'{IND}ENDIF', 'ENDFUNCTION'], 'header; RETURNS BOOLEAN; MOD 2 test; both RETURNs'),
        ('CountChar', 'the number of times a given character appears in a string', ['FUNCTION CountChar(S : STRING, C : CHAR) RETURNS INTEGER', f'{IND}DECLARE Total, i : INTEGER', f'{IND}Total ← 0', f'{IND}FOR i ← 1 TO LENGTH(S)', f'{IND}{IND}IF MID(S, i, 1) = C THEN', f'{IND}{IND}{IND}Total ← Total + 1', f'{IND}{IND}ENDIF', f'{IND}NEXT i', f'{IND}RETURN Total', 'ENDFUNCTION'], 'header with parameters; RETURNS INTEGER; loop over string; compare with MID; count; RETURN'),
        ('Max3', 'the largest of three integers', ['FUNCTION Max3(A : INTEGER, B : INTEGER, C : INTEGER) RETURNS INTEGER', f'{IND}Big ← A', f'{IND}IF B > Big THEN', f'{IND}{IND}Big ← B', f'{IND}ENDIF', f'{IND}IF C > Big THEN', f'{IND}{IND}Big ← C', f'{IND}ENDIF', f'{IND}RETURN Big', 'ENDFUNCTION'], 'header; RETURNS INTEGER; comparisons; RETURN'),
        ('Swap', 'swap the values of two integer variables (a procedure)', ['PROCEDURE Swap(BYREF A : INTEGER, BYREF B : INTEGER)', f'{IND}DECLARE Temp : INTEGER', f'{IND}Temp ← A', f'{IND}A ← B', f'{IND}B ← Temp', 'ENDPROCEDURE'], 'PROCEDURE header; BYREF for both; temp variable; correct swap'),
        ('CelsiusToF', 'convert a temperature in Celsius to Fahrenheit (F = C × 1.8 + 32)', ['FUNCTION CelsiusToF(C : REAL) RETURNS REAL', f'{IND}RETURN C * 1.8 + 32', 'ENDFUNCTION'], 'header; RETURNS REAL; formula; RETURN'),
    ])
    m = len(f[3].split(';'))
    return Q(f'{d["p"]} needs a subroutine {f[0]} for {d["org"]} that returns {f[1]}. Write the pseudocode for {f[0]}.', code(f[2]), f'1 mark each: {f[3]} [{m}]', marks=m)


@t14_3.add('C4', (3, 4, 5), 'multi_step')
def t14_3_full(r, D):
    lines, out, why = proc_prog(r, D)
    stem = ('Study the pseudocode.\n' + code(lines) + '\n(a) State the output. (b) Explain the difference between BYVAL and BYREF using this example. (c) Rewrite the header so that both X and Y are changed by the call, and state the new output.')
    p_q = why.split(';')[0].replace('inside the procedure ', '')
    pv, qv = [s.split('=')[1].strip() for s in p_q.split(',')]
    return Q(stem, f'(a) {out} (b) BYVAL passes a copy so the original is unchanged; BYREF passes the address so the original is changed (c) PROCEDURE Change(BYREF P : INTEGER, BYREF Q : INTEGER); output {pv} {qv}',
             f'(a) {why} [2] (b) [2] (c) header [1]; output {pv} {qv} [1]', marks=6, typ='multi_step')


@t14_3.add('C2', (2, 3, 4), 'explain')
def t14_3_err(r, D):
    kind = r.choice(['ret', 'byval', 'call'])
    if kind == 'ret':
        lines = ['FUNCTION Square(N : INTEGER) RETURNS INTEGER', f'{IND}Result ← N * N', 'ENDFUNCTION']
        fix = 'The function never returns a value; add RETURN Result (or RETURN N * N) before ENDFUNCTION.'
    elif kind == 'byval':
        lines = ['PROCEDURE AddBonus(Score : INTEGER)', f'{IND}Score ← Score + 10', 'ENDPROCEDURE', 'CALL AddBonus(PlayerScore)']
        fix = 'Score is passed by value (the default), so PlayerScore is not changed; the parameter should be BYREF Score : INTEGER.'
    else:
        lines = ['FUNCTION Double(N : INTEGER) RETURNS INTEGER', f'{IND}RETURN N * 2', 'ENDFUNCTION', 'CALL Double(5)']
        fix = 'A function is not called with CALL and its return value is lost; it should be used in an expression, e.g. Answer ← Double(5).'
    return Q('This pseudocode contains an error.\n' + code(lines) + '\nIdentify the error and explain how to correct it.', fix, '1 mark: error; 1 mark: correction [2]')


CHAPTERS[14] = [t14_1, t14_2, t14_3]

# =============================================================================== Chapter 15 Software development
t15_1 = topic('Program development life cycle: analysis, design, coding, testing and maintenance; waterfall, iterative and RAD', 'program development life cycle', 'waterfall', 'iterative', 'rad')
t15_1.fixed('C1', (1, 2), [
    ('In which stage of the program development life cycle are the requirements of the client identified?', 'Analysis', 'Analysis: investigate the problem, interview users, produce a requirements specification.', ['Design', 'Coding', 'Maintenance']),
    ('Which life cycle model completes each stage fully before the next begins?', 'Waterfall', 'Waterfall: linear sequence, each stage signed off.', ['Iterative', 'RAD', 'Agile prototyping']),
    ('What is a key feature of rapid application development (RAD)?', 'Prototypes are produced quickly and refined with frequent user feedback', 'RAD: modules developed in parallel as prototypes, little upfront planning.', ['All stages are completed once in strict order', 'The client is only involved at the end', 'No testing is carried out']),
    ('In the iterative model, what happens?', 'The program is developed in repeated cycles, each adding or improving features', 'Each iteration goes through design, code and test.', ['Each stage is done once only', 'Only the design stage is repeated', 'The program is written without any design']),
    ('During which stage are identifier tables, structure charts and pseudocode produced?', 'Design', 'Design: algorithms, data structures, interfaces, test plans.', ['Analysis', 'Maintenance', 'Testing']),
])
t15_1.fixed('C2', (2, 3, 4), [
    ('Give one advantage and one disadvantage of the waterfall model.', 'Advantage: simple to manage with clear stages and documentation. Disadvantage: the client sees the product late, and changes to requirements are difficult/expensive.', '1 mark each [2]'),
    ('Explain why RAD may be suitable for a project where the requirements are not clear.', 'Users see working prototypes early and give feedback, so requirements can be discovered and changed throughout development.', '1 mark each [2]'),
    ('Explain the purpose of the analysis stage.', 'To find out what the problem is and what the client needs, by investigating the current system and producing a requirements specification.', '1 mark each [2]'),
])
scen(t15_1, 'C3', (2, 3, 4), [
    '{org} in {city} needs a booking app quickly but is not sure what features it wants.',
    'A bank needs safety-critical software with fixed, well-understood requirements.',
    '{p} is leading a project to replace the stock control system at {org}.',
], [('Recommend a development model and justify your choice.', 'RAD/iterative if requirements unclear or speed important; waterfall if requirements fixed and documentation/safety important.', '1 mark model; 2 marks justification [3]'),
    ('Describe two activities in the analysis stage.', 'Interviews, questionnaires, observation, document review; producing the requirements specification.', '1 mark each [2]'),
    ('Describe what happens in the maintenance stage.', 'Program is corrected, adapted or improved after release.', '1 mark each point, max 2 [2]'),
    ('Explain one drawback of RAD for this project.', 'Less documentation; needs committed users; may not suit large or safety-critical systems.', '1 mark [1]')], k=(2, 3))
essay(t15_1, [('the choice of the waterfall model rather than rapid application development for the project at {org}', 'clear stages and documentation; easy to manage and budget; suits fixed, well-understood requirements and safety-critical systems.',
               'client sees product late; changes are costly; problems found late in testing; RAD gives early prototypes and feedback.', 'waterfall suits stable requirements; RAD suits changing requirements and tight deadlines.')],
      ['{org} in {city} is starting a new software project.', '{p} is the project manager at {org}.'])


def fsm(r, D):
    states = ['S1', 'S2', 'S3'] if D < 4 else ['S1', 'S2', 'S3', 'S4']
    inputs = ['a', 'b']
    tbl = {(s, i): r.choice(states) for s in states for i in inputs}
    seq = ''.join(r.choice(inputs) for _ in range(5 if D < 4 else 7))
    cur, path = 'S1', ['S1']
    for c in seq:
        cur = tbl[(cur, c)]
        path.append(cur)
    return states, tbl, seq, path


t15_2 = topic('Program design using structure charts and state-transition diagrams', 'structure charts', 'state-transition diagrams')
t15_2.fixed('C1', (1, 2), [
    ('What does a structure chart show?', 'The modules of a program, how they are related and the parameters passed between them', 'Structure charts show hierarchy and data flow between modules.', ['The order in which every instruction runs', 'The states of a system and transitions', 'The truth table of a circuit']),
    ('On a structure chart, what does a curved arrow around the lines to sub-modules show?', 'Iteration (the modules are repeated)', 'A diamond shows selection; a curved arrow shows repetition.', ['Selection', 'A parameter passed by reference', 'The end of the program']),
    ('On a structure chart, what does a diamond on a line show?', 'Selection (the module is called only under a condition)', 'Diamond = selection.', ['Iteration', 'Data flow', 'A state']),
    ('What does a state-transition diagram show?', 'The states a system can be in and the events that cause it to move between them', 'States as circles, transitions as labelled arrows, start state indicated.', ['The modules of a program', 'The data in a database', 'The hardware of a computer']),
    ('In a state-transition diagram, how is an accepting (final) state shown?', 'With a double circle', 'Single circle = state; double circle = accepting state; arrow from nowhere = start.', ['With a diamond', 'With a rectangle', 'With a dashed arrow']),
])
t15_2.fixed('C2', (2, 3, 4), [
    ('Explain how a structure chart helps a programmer design a program.', 'It shows how the problem is decomposed into modules, the hierarchy of calls and the parameters passed, so modules can be designed, coded and tested separately.', '1 mark per point, max 2 [2]'),
    ('Explain how a state-transition diagram can be used to design a vending machine program.', 'It identifies every state (waiting, coins inserted, dispensing), the inputs/events that change state and the outputs, so the program logic covers every case.', '1 mark each point, max 2 [2]'),
])


@t15_2.add('C3', (1, 2, 3, 4, 5))
def t15_2_fsm(r, D):
    states, tbl, seq, path = fsm(r, D)
    txt = '; '.join(f'{s} --{i}--> {tbl[(s, i)]}' for s in states for i in ['a', 'b'])
    stem = f'A state-transition table has the transitions {txt}. The start state is S1. State the final state after the input sequence {seq}' + (', and the sequence of states visited.' if D >= 3 else '.')
    if D == 1:
        return MCQ(r, stem.replace('State the final state', 'What is the final state').rstrip('.') + '?', path[-1], [s for s in states + ['S5'] if s != path[-1]], f'States: {" → ".join(path)}.')
    return Q(stem, path[-1] + (f'; {" → ".join(path)}' if D >= 3 else ''), f'{" → ".join(path)} [{2 if D >= 3 else 1}]', marks=2 if D >= 3 else 1)


SC = [('ProcessOrder', [('InputOrder', 'OrderDetails ↑'), ('CalculateTotal', 'OrderDetails ↓, Total ↑'), ('PrintReceipt', 'Total ↓')]),
      ('MarkExam', [('ReadAnswers', 'Answers ↑'), ('CompareWithKey', 'Answers ↓, Score ↑'), ('AssignGrade', 'Score ↓, Grade ↑'), ('OutputResult', 'Grade ↓')]),
      ('LoginUser', [('GetCredentials', 'Username ↑, Password ↑'), ('CheckPassword', 'Username ↓, Password ↓, Valid ↑'), ('ShowMenu', 'Valid ↓')]),
      ('PayStaff', [('ReadHours', 'Hours ↑'), ('CalculatePay', 'Hours ↓, Pay ↑'), ('DeductTax', 'Pay ↓, NetPay ↑'), ('PrintPayslip', 'NetPay ↓')])]
scen(t15_2, 'C3', (2, 3, 4), [
    '{p} has drawn a structure chart for a program used by {org}.',
    'A team at {org} in {city} is designing a program using a structure chart.',
], [lambda r, d: (lambda s: (f'The top module {s[0]} calls ' + ', '.join(m for m, _ in s[1]) + '. Describe the parameters passed between the modules (↑ returned to the parent, ↓ passed down).', '; '.join(f'{m}: {p}' for m, p in s[1]), f'1 mark per module with correct parameters, max {min(4, len(s[1]))} [{min(4, len(s[1]))}]'))(r.choice(SC)),
    ('Explain how iteration would be shown on the structure chart.', 'A curved arrow over the lines to the modules that are repeated.', '1 mark [1]'),
    ('Explain how selection would be shown on the structure chart.', 'A diamond on the line to the module that is only called if a condition is true.', '1 mark [1]'),
    ('Write the pseudocode header for one of the modules that returns a value.', 'e.g. FUNCTION CalculateTotal(OrderDetails : ...) RETURNS REAL', '1 mark identifier/parameters; 1 mark return type [2]')], k=(2, 3))


@t15_2.add('C4', (3, 4, 5), 'multi_step')
def t15_2_design(r, D):
    states, tbl, seq, path = fsm(r, D)
    acc = r.choice(states)
    txt = '; '.join(f'{s} --{i}--> {tbl[(s, i)]}' for s in states for i in ['a', 'b'])
    stem = (f'A door entry system is modelled by the transitions {txt}; S1 is the start state and {acc} is the accepting state (door opens). (a) Give the states visited for the input {seq}. '
            f'(b) State whether the door opens. (c) Describe how this would be drawn as a state-transition diagram. (d) Explain one benefit of designing the system this way.')
    return Q(stem, f'(a) {" → ".join(path)} (b) {"Yes" if path[-1] == acc else "No"} (c) circles for states, labelled arrows for each transition, arrow into S1, double circle for {acc} (d) every state/input combination is considered so the logic is complete',
             '(a) [2] (b) [1] (c) [2] (d) [1]', marks=6, typ='multi_step')


t15_3 = topic('Types of errors and testing methods: dry-run, walkthrough, white-box, black-box, alpha, beta, acceptance; test data', 'types of errors', 'testing methods', 'test data')
t15_3.fixed('C1', (1, 2), [
    ('What is a syntax error?', 'A statement that breaks the grammar rules of the programming language', 'Syntax errors are found by the translator; the program will not run.', ['An error in the logic of the program', 'An error that only occurs when the program runs', 'A spelling mistake in a comment']),
    ('What is a logic error?', 'An error that causes the program to give incorrect results even though it runs', 'e.g. using > instead of >=.', ['An error that stops the program from being translated', 'An error in the hardware', 'A missing semicolon']),
    ('What is a run-time error?', 'An error that causes the program to crash while it is running', 'e.g. division by zero, array index out of range.', ['An error found by the compiler', 'An error in the design documents', 'A spelling error in the output']),
    ('What is black-box testing?', 'Testing the inputs and outputs without considering the code', 'Black-box: based on the specification; white-box: tests every path through the code.', ['Testing every path through the code', 'Testing by the client in their own environment', 'Reading through the code with colleagues']),
    ('What is beta testing?', 'Testing by a group of real users outside the company before release', 'Alpha: in-house; beta: selected external users; acceptance: by the client against requirements.', ['Testing by the programmers in-house', 'Testing each module on its own', 'Testing with extreme data only']),
    ('What is a dry run?', 'Working through an algorithm by hand, recording values in a trace table', 'Dry runs find logic errors without running the program.', ['Running the program with no data', 'Compiling the program', 'Running a program without a monitor']),
    ('What is a walkthrough?', 'A formal review in which the programmer explains the code to colleagues', 'Colleagues look for errors and suggest improvements.', ['Running the program one line at a time', 'Testing with beta users', 'A type of black-box test']),
])
t15_3.fixed('C2', (2, 3, 4), [
    ('Explain the difference between white-box and black-box testing.', 'White-box testing uses knowledge of the code to test every path/branch; black-box testing checks outputs for given inputs against the specification without looking at the code.', '1 mark each [2]'),
    ('Explain why acceptance testing is carried out.', 'The client checks that the finished system meets the agreed requirements before formally accepting (and paying for) it.', '1 mark each [2]'),
    ('Explain why a program with no syntax errors may still contain errors.', 'Logic errors (wrong results) and run-time errors (crashes) are not detected by the translator.', '1 mark each [2]'),
])


@t15_3.add('C3', (1, 2, 3, 4, 5))
def t15_3_data(r, D):
    lo = r.randrange(1, 50)
    hi = lo + r.randrange(10, 80)
    d = ctx(r)
    field = r.choice(['age', 'number of tickets', 'test mark', 'quantity ordered', 'room temperature'])
    kinds = {'normal': r.randrange(lo + 1, hi), 'extreme': r.choice([lo, hi]), 'abnormal': r.choice([lo - r.randrange(1, 10), hi + r.randrange(1, 10), 'abc']), 'boundary': r.choice([lo - 1, hi + 1])}
    if D <= 2:
        k = r.choice(list(kinds))
        v = kinds[k]
        desc = {'normal': 'normal', 'extreme': 'extreme', 'abnormal': 'abnormal (erroneous)', 'boundary': 'boundary (just outside the range)'}
        return MCQ(r, f'A program accepts a {field} between {lo} and {hi} inclusive. Which type of test data is the value {v}?', desc[k],
                   [x for kk, x in desc.items() if kk != k] + ['abnormal (erroneous)' if k == 'boundary' else 'boundary (just outside the range)'],
                   f'Normal: within range; extreme: {lo} or {hi}; boundary: {lo - 1}/{lo} and {hi}/{hi + 1}; abnormal: outside range or wrong type.')
    stem = f'{d["p"]} is testing a program for {d["org"]} that accepts a {field} between {lo} and {hi} inclusive. Give one example each of normal, extreme, abnormal and boundary test data, with the expected outcome.'
    return Q(stem, f'Normal: {kinds["normal"]} (accepted); extreme: {lo} or {hi} (accepted); abnormal: e.g. {hi + 15} or "abc" (rejected); boundary: {lo - 1} rejected / {lo} accepted (or {hi} accepted / {hi + 1} rejected)',
             f'1 mark per correct type with expected outcome [4]', marks=4)


@t15_3.add('C3', (2, 3, 4))
def t15_3_err(r, D):
    ex = r.choice([('OUTPUT "Total is " Total', 'syntax', 'the & operator (or comma) is missing between the string and the variable'),
                   ('IF Mark > 50 THEN OUTPUT "Pass"  (pass mark is 50 or more)', 'logic', 'a mark of exactly 50 is treated as a fail; should be >='),
                   ('Average ← Total / Count  (when no values have been entered)', 'run-time', 'division by zero when Count is 0'),
                   ('FOR i ← 1 TO 10 ... Scores[i + 1] (Scores is ARRAY[1:10])', 'run-time', 'index 11 is out of range'),
                   ('WHILE Count < 10 (Count never changes in the loop)', 'logic', 'infinite loop'),
                   ('DECLARE Name : STRNG', 'syntax', 'misspelt keyword/data type'),
                   ('Area ← Length + Width  (for the area of a rectangle)', 'logic', 'should multiply, not add')])
    if D == 2:
        return MCQ(r, f'What type of error is shown by: {ex[0]}?', f'{ex[1]} error', [f'{x} error' for x in ['syntax', 'logic', 'run-time'] if x != ex[1]] + ['hardware error'], ex[2] + '.')
    return Q(f'Identify the type of error in the statement {ex[0]} and explain how it would be detected.', f'{ex[1].capitalize()} error: {ex[2]}.',
             '1 mark type; 1 mark explanation; 1 mark detection method (translator for syntax; testing/dry run/trace for logic; crash during execution for run-time) [3]', marks=3)


scen(t15_3, 'C4', (3, 4, 5), [
    '{org} in {city} has commissioned a new online booking system.',
    '{p} has finished coding a program that calculates staff overtime pay for {org}.',
], [('Describe the difference between alpha and beta testing for this system.', 'Alpha: in-house by the developers/testers; beta: by selected real users in their own environment before release.', '1 mark each [2]'),
    ('Explain how a dry run with a trace table could find a logic error.', 'Work through the algorithm by hand recording each variable; compare with expected values; find the line where they differ.', '1 mark per point, max 3 [3]'),
    ('Describe a test plan for the system.', 'Lists each test, its purpose, test data (normal, extreme, abnormal), expected outcome, actual outcome.', '1 mark per feature, max 3 [3]'),
    ('Explain the purpose of acceptance testing.', 'Client confirms the system meets the requirements specification.', '1 mark each [2]'),
    ('Explain why white-box testing is used by the developers.', 'Every path/branch in the code is tested so hidden logic errors are found.', '1 mark each [2]')], k=(3, 4))

t15_4 = topic('Maintenance: corrective, adaptive and perfective', 'maintenance', 'corrective, adaptive and perfective')
t15_4.fixed('C1', (1, 2), [
    ('What is corrective maintenance?', 'Fixing errors found after the program has been released', 'Corrective: bugs that were not found in testing.', ['Adding new features', 'Changing the program for a new operating system', 'Making the program run faster']),
    ('What is adaptive maintenance?', 'Changing a program to meet new requirements or a new environment', 'e.g. new law, new tax rate, new operating system or hardware.', ['Fixing bugs', 'Improving performance without new requirements', 'Writing documentation']),
    ('What is perfective maintenance?', 'Improving the performance or usability of a program that already works', 'e.g. faster processing, better interface.', ['Fixing bugs', 'Changing the program because of a new law', 'Testing the program']),
])
t15_4.fixed('C2', (2, 3, 4), [
    ('Explain why good documentation and meaningful identifiers make maintenance easier.', 'Programmers who did not write the code can understand what each part does, so they can find and change the right code quickly with fewer new errors.', '1 mark each [2]'),
])
MAINT = [('A tax rate changes because of a new law.', 'adaptive'), ('Users report the program crashes when a date in February is entered.', 'corrective'),
         ('The report screen is redesigned so it loads twice as fast.', 'perfective'), ('The app is updated to run on a new version of the operating system.', 'adaptive'),
         ('A rounding error in the invoice totals is fixed.', 'corrective'), ('A search feature is made easier to use after user feedback.', 'perfective'),
         ('The program is changed to accept a new currency.', 'adaptive'), ('A loop that occasionally never ends is corrected.', 'corrective'),
         ('The code is optimised to use less memory.', 'perfective')]


@t15_4.add('C3', (1, 2, 3, 4))
def t15_4_type(r, D):
    if D <= 2:
        x = r.choice(MAINT)
        d = ctx(r)
        return MCQ(r, f'Software used by {d["org"]} is changed. {x[0]} Which type of maintenance is this?', x[1], [m for m in ['corrective', 'adaptive', 'perfective', 'preventive testing'] if m != x[1]], f'{x[1]} maintenance.')
    xs = r.sample(MAINT, 3)
    return Q('Identify the type of maintenance in each case, giving a reason: ' + ' '.join(f'({i + 1}) {x[0]}' for i, x in enumerate(xs)), '; '.join(f'({i + 1}) {x[1]}' for i, x in enumerate(xs)), '1 mark per correct type with reason [3]', marks=3)


scen(t15_4, 'C4', (3, 4, 5), [
    'The payroll program at {org} in {city} was released two years ago.',
    '{p} has been asked to maintain a stock control program written by another programmer at {org}.',
], [('Describe one example each of corrective, adaptive and perfective maintenance for this program.', 'Corrective: fix a calculation bug; adaptive: new tax rules/OS; perfective: faster reports/better interface.', '1 mark each [3]'),
    ('Explain why maintenance can cost more than the original development.', 'Programs are used for many years; changes needed repeatedly; programmers must first understand old code; new errors may be introduced.', '1 mark per point, max 2 [2]'),
    ('Explain how the original programmer could have made maintenance easier.', 'Comments, meaningful identifiers, modular design, documentation, consistent indentation.', '1 mark per point, max 3 [3]')], k=(2, 3))

CHAPTERS[15] = [t15_1, t15_2, t15_3, t15_4]


# ----------------------------------------------------------------------------- extra C2 (explain / compare) items
scen(t7_1, 'C2', (2, 3, 4), [
    'A {otype} in {city} uses a computer system with sensors.', '{org} is installing an automatic system controlled by a microprocessor.', '{p} is studying how a burglar alarm at {org} works.',
], [('Explain why the sensor readings must be checked continuously.', 'Conditions change at any time; the system must respond quickly, so it loops, reading the sensors repeatedly.', '1 mark each [2]'),
    ('Explain the difference between the role of the sensor and the role of the actuator.', 'The sensor measures a physical quantity and sends data; the actuator performs an action when signalled by the processor.', '1 mark each [2]'),
    ('Explain why the microprocessor, not the sensor, decides when to act.', 'Only the processor compares the readings with stored values; the sensor only measures.', '1 mark each [2]'),
    ('Explain why a monitoring system may give a warning but not change anything.', 'It has no actuators; it only records readings and alerts a human when values are outside limits.', '1 mark each [2]'),
    ('Explain why an infrared sensor rather than a pressure sensor might be chosen to detect people.', 'It detects movement/body heat at a distance over a wide area; a pressure pad only detects someone standing on it.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t7_2, 'C2', (2, 3, 4), [
    'A {otype} in {city} uses a closed-loop control system.', '{p} is explaining an automatic heating system at {org}.', 'A fish tank at {org} keeps its water at a constant temperature.',
], [('Explain why the system is described as closed loop.', 'The output (actuator action) changes the environment, which is measured by the sensor and fed back into the next decision.', '1 mark each [2]'),
    ('Explain why an ADC is needed between the sensor and the processor.', 'The sensor gives a continuously varying (analogue) voltage; the processor can only process discrete binary (digital) values.', '1 mark each [2]'),
    ('Explain why a DAC may be needed between the processor and the actuator.', 'Some actuators, such as a variable-speed motor, need a varying analogue voltage, not a digital signal.', '1 mark each [2]'),
    ('Explain what would happen without feedback.', 'The actuator would be switched on or off without knowing the effect, so the value could overshoot or never be reached.', '1 mark each [2]'),
    ('Explain why the processor samples the sensor at regular time intervals.', 'So that changes are detected quickly without wasting processing time.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t12_1, 'C2', (2, 3, 4), [
    '{org} in {city} is planning a new computer system.', '{p} is designing a simulation of traffic in {city}.', 'A team at {org} is writing a game.',
], [('Explain how abstraction would simplify the design.', 'Only the details needed are kept (e.g. positions and speeds) and irrelevant details removed, so the model is simpler to build.', '1 mark each [2]'),
    ('Explain how decomposition would help the team.', 'The problem is split into smaller sub-problems that are easier to solve and can be shared among the team.', '1 mark each [2]'),
    ('Explain the difference between abstraction and decomposition.', 'Abstraction removes unnecessary detail; decomposition breaks a problem into smaller parts.', '1 mark each [2]'),
    ('Explain one risk of too much abstraction.', 'Important details may be removed, so the solution no longer represents the real problem accurately.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t12_3, 'C2', (2, 3, 4), [
    '{p} is using stepwise refinement to design a program for {org}.', 'A team at {org} in {city} is designing an algorithm top-down.',
], [('Explain why the top-level steps are not detailed enough to code.', 'Each top-level step represents a large task needing many statements; it must be broken down further.', '1 mark each [2]'),
    ('Explain how stepwise refinement makes testing easier.', 'Each small step/module can be tested separately before being combined, so errors are easier to locate.', '1 mark each [2]'),
    ('Explain how stepwise refinement relates to a structure chart.', 'Each level of refinement becomes a level of modules in the structure chart.', '1 mark each [2]'),
    ('Explain why refinement can stop at different depths for different steps.', 'Some steps are simple and can be coded at once; others need several levels.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t14_1, 'C2', (2, 3, 4), [
    '{p} is writing a program for {org}.', 'A student at {org} is learning Cambridge pseudocode.', '{org} in {city} is reviewing its programs for readability.',
], [('Explain why VAT should be stored as a constant rather than typed as 0.2 throughout the program.', 'Its meaning is clear and if the rate changes it is updated in one place, avoiding missed changes.', '1 mark each [2]'),
    ('Explain the difference between INPUT and READFILE.', 'INPUT takes data from the user (keyboard); READFILE reads a line from a text file.', '1 mark each [2]'),
    ('Explain why LENGTH(Name) is used rather than a fixed number in a loop that processes a name.', 'Names have different lengths; LENGTH gives the actual number of characters so the loop works for any name.', '1 mark each [2]'),
    ('Explain the difference between the = operator in a condition and the ← operator.', '← assigns a value to a variable; = compares two values and gives TRUE or FALSE.', '1 mark each [2]'),
    ('Explain why STR_TO_NUM may be needed when data is read from a text file.', 'Data read from a text file is a string; it must be converted before arithmetic can be done.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t8_4, 'C2', (2, 3, 4), [
    '{p} is using an IDE to write code for {org}.', 'A programming class at {org} has just started using an IDE.',
], [('Explain how context-sensitive prompts speed up coding.', 'The IDE suggests identifiers, keywords and parameters as you type, so less typing and fewer spelling errors.', '1 mark each [2]'),
    ('Explain how dynamic syntax checking reduces development time.', 'Errors are highlighted as code is typed, so they are fixed immediately instead of after translation.', '1 mark each [2]'),
    ('Explain the difference between a breakpoint and single stepping.', 'A breakpoint pauses execution at a chosen line; single stepping runs one statement at a time.', '1 mark each [2]'),
    ('Explain why a report (watch) window is useful.', 'It shows the values of variables as the program runs, so unexpected values reveal logic errors.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t6_4, 'C2', (2, 3, 4), [
    '{p} is writing assembly code for a device at {org}.', 'A student at {org} is learning bit manipulation.',
], [('Explain why a logical shift left by 1 place multiplies an unsigned number by 2.', 'Every bit moves to the next higher place value (twice as large), with 0 entering at the right, provided no 1 is lost from the left.', '1 mark each [2]'),
    ('Explain why an arithmetic shift is needed to divide a negative two\'s complement number by 2.', 'A logical shift would put 0 into the sign bit, making the number positive; arithmetic shift copies the sign bit.', '1 mark each [2]'),
    ('Explain why AND is used with a mask to test a single bit.', 'AND with 1 keeps the tested bit and AND with 0 clears all others, so the result is non-zero only if that bit is 1.', '1 mark each [2]'),
    ('Explain the difference between using OR and XOR with the same mask.', 'OR always sets the masked bits to 1; XOR flips them, setting 0s to 1 and 1s to 0.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t11_3, 'C2', (2, 3, 4), [
    '{org} in {city} is moving its data into a DBMS.', '{p} is the database administrator at {org}.',
], [('Explain how the DBMS provides data independence.', 'The structure is held in the data dictionary/schema, so programs do not depend on how data is physically stored; the structure can change without rewriting programs.', '1 mark each [2]'),
    ('Explain the difference between the logical schema and the data dictionary.', 'The logical schema models the whole database (tables, relationships); the data dictionary stores detailed metadata about each item (names, types, rules).', '1 mark each [2]'),
    ('Explain why different users may be given different views of the database.', 'Each user sees only the data they need, improving security and making the system simpler to use.', '1 mark each [2]'),
    ('Explain how the DBMS helps keep data consistent when many users edit it.', 'Record locking/concurrency control stops two users changing the same record at the same time; referential integrity is enforced.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t13_3, 'C2', (2, 3, 4), [
    '{p} is writing a program for {org} that stores data in text files.', 'A program at {org} reads a list of customers from a text file.',
], [('Explain why a WHILE NOT EOF loop is used rather than a FOR loop to read the file.', 'The number of lines is not known in advance; the loop stops when the end of the file is reached.', '1 mark each [2]'),
    ('Explain what would happen if the program tried to read past the end of the file.', 'A run-time error occurs because there is no more data to read.', '1 mark each [2]'),
    ('Explain why data is stored in a text file rather than only in an array.', 'Arrays are in RAM and lost when the program ends; files store data permanently.', '1 mark each [2]'),
    ('Explain why opening the file in WRITE mode by mistake would be a problem.', 'WRITE would replace the existing contents, losing all previous data.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t14_3, 'C2', (2, 3, 4), [
    '{p} is writing modular code for {org}.', 'A team at {org} in {city} is splitting a program into subroutines.',
], [('Explain why a function is more suitable than a procedure for calculating a discount.', 'A function returns a single value that can be used directly in an expression.', '1 mark each [2]'),
    ('Explain when a parameter should be passed by reference.', 'When the subroutine must change the original variable, or return more than one value.', '1 mark each [2]'),
    ('Explain why parameters are better than global variables for passing data.', 'The data each subroutine uses is clear from its header; subroutines are independent and reusable; fewer side effects.', '1 mark each [2]'),
    ('Explain how subroutines make testing easier.', 'Each subroutine can be tested on its own with known inputs before it is combined.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t15_2, 'C2', (2, 3, 4), [
    '{p} is designing a program for {org} using diagrams.', 'A team at {org} is planning a ticket machine.',
], [('Explain the difference between a structure chart and a flowchart.', 'A structure chart shows the modules and data passed between them (hierarchy); a flowchart shows the sequence of steps and decisions in an algorithm.', '1 mark each [2]'),
    ('Explain why parameters are shown on a structure chart.', 'They show what data each module needs and returns, helping define module interfaces.', '1 mark each [2]'),
    ('Explain why a state-transition diagram suits a ticket machine.', 'The machine moves between a fixed set of states (waiting, paid, printing) in response to events, which the diagram shows.', '1 mark each [2]'),
    ('Explain what an arrow labelled "coin inserted" between two states means.', 'When the event "coin inserted" happens in the first state, the system moves to the second state.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t6_3, 'C2', (2, 3, 4), [
    '{p} is testing an assembly language program for {org}.', 'A student at {org} is tracing an assembly language loop.',
], [('Explain why a CMP instruction is always followed by JPE or JPN in a loop.', 'CMP only sets a flag; the conditional jump uses the flag to decide whether to leave or repeat the loop.', '1 mark each [2]'),
    ('Explain the difference between JMP and JPE.', 'JMP always jumps; JPE only jumps if the last comparison was true.', '1 mark each [2]'),
    ('Explain why memory locations are used to hold loop counters in simple programs.', 'There is only one accumulator, so values must be stored and reloaded between steps.', '1 mark each [2]'),
    ('Explain how a trace table shows that a loop has finished.', 'The counter reaches the exit value, the conditional jump is taken and the END instruction is reached.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t15_4, 'C2', (2, 3, 4), [
    'The software used by {org} in {city} needs to be changed.', '{p} maintains a program written several years ago for {org}.',
], [('Explain the difference between corrective and perfective maintenance.', 'Corrective fixes errors; perfective improves a program that already works (speed, usability).', '1 mark each [2]'),
    ('Explain why adaptive maintenance may be needed even when the program has no errors.', 'The environment or requirements change (new law, hardware, OS), so the program must be changed to keep working.', '1 mark each [2]'),
    ('Explain why testing is needed after maintenance.', 'Changes may introduce new errors; regression testing checks that existing features still work.', '1 mark each [2]'),
    ('Explain why comments help a maintenance programmer.', 'They explain what the code does and why, so it can be changed safely.', '1 mark each [2]')], k=(1, 2), name='scen_c2')
scen(t15_3, 'C2', (2, 3, 4), [
    '{p} is testing a program for {org}.', 'A test team at {org} in {city} is planning tests for a booking system.',
], [('Explain why extreme test data is used.', 'It checks that values at the limits of the valid range are accepted, where off-by-one errors are common.', '1 mark each [2]'),
    ('Explain why abnormal test data is used.', 'It checks that invalid data is rejected rather than crashing the program or giving wrong results.', '1 mark each [2]'),
    ('Explain the difference between a logic error and a run-time error.', 'A logic error gives wrong results but the program runs; a run-time error causes the program to stop/crash.', '1 mark each [2]'),
    ('Explain why a walkthrough may find errors that testing misses.', 'Colleagues read the code and logic directly, so they can spot problems on paths that the test data does not exercise.', '1 mark each [2]')], k=(1, 2), name='scen_c2')


@t13_2.add('C4', (3, 4, 5), 'multi_step')
def t13_2_lsearch(r, D):
    n = r.randrange(8, 13)
    a = r.sample(range(1, 90), n)
    t = r.choice(a)
    p_, sw = bubble_pass(a)
    stem = (f'An array Values[1:{n}] contains {a}. (a) Write pseudocode for a linear search that outputs the index of a value input by the user, or "Not found". (b) State the number of comparisons needed to find {t}. '
            f'(c) Give the array after one pass of an ascending bubble sort.')
    ans = code(['INPUT Target', 'Index ← 0', 'i ← 1', f'WHILE i <= {n} AND Index = 0', f'{IND}IF Values[i] = Target THEN', f'{IND}{IND}Index ← i', f'{IND}ENDIF', f'{IND}i ← i + 1', 'ENDWHILE',
                'IF Index = 0 THEN', f'{IND}OUTPUT "Not found"', 'ELSE', f'{IND}OUTPUT Index', 'ENDIF']) + f'\n(b) {a.index(t) + 1} (c) {p_}'
    return Q(stem, ans, f'(a) input [1]; loop with correct bounds/stop condition [1]; comparison [1]; output index or Not found [1] (b) {a.index(t) + 1} [1] (c) {p_} [2]', marks=7, typ='multi_step')


finalize(CHAPTERS)
