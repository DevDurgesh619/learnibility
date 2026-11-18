"""Cambridge International A Level Computer Science 9618 (syllabus sections 13-20), grade 12.

Paper 3 (Advanced Theory) and Paper 4 (Practical) style items: user-defined types and file organisation,
floating-point representation, communication protocols, RISC/CISC and parallel processing, Boolean algebra
and Karnaugh maps, flip-flops, operating systems and scheduling, translation (BNF, RPN), encryption and
certificates, AI graph search and machine learning, ADTs (circular queues, linked lists, binary trees),
searching/sorting and Big O, recursion, programming paradigms, OOP and exception handling.
Pseudocode follows the Cambridge 9618 guide. Every computed answer is produced by the code that builds the stem.
"""
import contextlib
import heapq
import io
import itertools
import math
import re
from fractions import Fraction

from ._lib import topic, mcq, compose, person, city  # noqa: F401
from .g11_computer_science import (ctx, fill, Q, MCQ, code, items, scen, essay, ar, finalize, b, hx, tc, from_tc, Asm, asm_text, mem_text,
                                   _addr_setup, IND, lg_eval, lg_str, lg_table, lg_rand, GATES)

def art(n):
    return 'an' if str(n)[0] == '8' or n in (11, 18) else 'a'


PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# =============================================================================== Chapter 1 User-defined data types and file organisation
t1_1 = topic('User-defined data types: non-composite (enumerated, pointer) and composite (record, set, class)', 'user-defined data types', 'non-composite', 'composite')
t1_1.fixed('C1', (1, 2), [
    ('What is a user-defined data type?', 'A data type designed by the programmer, built from existing data types', 'e.g. enumerated, pointer, record, set, class.', ['A data type built into the language such as INTEGER', 'A variable entered by the user', 'A type of file']),
    ('Which of these is a non-composite data type?', 'Enumerated', 'Non-composite: defined without reference to other user types (enumerated, pointer). Composite: record, set, class.', ['Record', 'Class', 'Set']),
    ('What does an enumerated data type contain?', 'An ordered list of all the possible values', 'e.g. TYPE Season = (Spring, Summer, Autumn, Winter).', ['The memory address of a variable', 'Fields of different data types', 'Methods and attributes']),
    ('What does a pointer variable store?', 'The memory address of another variable or data item', 'TYPE TIntPtr = ^INTEGER; MyPtr ← @Count.', ['A copy of the value of another variable', 'A list of possible values', 'A string of characters']),
    ('Which is a composite data type?', 'Record', 'Composite types refer to other data types: record, set, class.', ['Enumerated', 'Pointer', 'INTEGER']),
    ('What is a set data type?', 'An unordered collection of unique values of the same type that supports set operations', 'Sets support union, intersection, difference, membership.', ['An ordered list of values in an array', 'A pointer to a list', 'A record with one field']),
    ('In Cambridge pseudocode, what does MyPointer^ refer to?', 'The value stored at the address held in MyPointer', '^ after the pointer dereferences it; @ gives the address of a variable.', ['The address of MyPointer itself', 'The next pointer in a list', 'The data type of MyPointer']),
])
t1_1.fixed('C2', (2, 3, 4), [
    ('Explain why a programmer might use an enumerated data type instead of an integer code.', 'Values have meaningful names, making code easier to read and maintain; only the listed values are allowed, which reduces errors; values are ordered so can be compared.', '1 mark per point, max 2 [2]'),
    ('Explain the difference between a non-composite and a composite data type.', 'A non-composite type is defined without reference to other data types (e.g. enumerated, pointer); a composite type is built from other data types (e.g. record, set, class).', '1 mark each [2]'),
    ('Explain why pointers are needed to implement dynamic data structures such as linked lists.', 'Nodes can be stored anywhere in memory and created at run time; each node holds a pointer to the address of the next node, linking them.', '1 mark each [2]'),
])
ENUMS = [('TSeason', ['Spring', 'Summer', 'Autumn', 'Winter']), ('TDay', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
         ('TLight', ['Red', 'Amber', 'Green']), ('TSize', ['Small', 'Medium', 'Large', 'ExtraLarge']), ('TDirection', ['North', 'East', 'South', 'West'])]


@t1_1.add('C3', (1, 2, 3, 4, 5))
def t1_1_ptr(r, D):
    a, inc = r.randrange(5, 50), r.randrange(2, 12)
    v = r.choice(['Count', 'Score', 'Total', 'Level'])
    k = r.choice(['add', 'mul', 'two'])
    lines = ['TYPE TIntPointer = ^INTEGER', f'DECLARE {v}, Other : INTEGER', 'DECLARE MyPointer : TIntPointer', f'{v} ← {a}', f'MyPointer ← @{v}']
    if k == 'add':
        lines += [f'MyPointer^ ← MyPointer^ + {inc}', f'OUTPUT {v}']
        out = str(a + inc)
        why = f'MyPointer points to {v}, so changing MyPointer^ changes {v}: {a} + {inc} = {a + inc}'
    elif k == 'mul':
        lines += [f'Other ← MyPointer^ * {inc}', f'OUTPUT Other, " ", {v}']
        out = f'{a * inc} {a}'
        why = f'Other gets the value pointed to ({a}) × {inc}; {v} is unchanged'
    else:
        lines += [f'Other ← {inc}', 'MyPointer ← @Other', f'MyPointer^ ← MyPointer^ + {v}', f'OUTPUT {v}, " ", Other']
        out = f'{a} {inc + a}'
        why = f'MyPointer is moved to point at Other, so only Other changes: {inc} + {a} = {inc + a}'
    stem = 'Study the pseudocode.\n' + code(lines) + '\nState the output.'
    if D == 1:
        return MCQ(r, stem.replace('State the output.', 'What is output?'), out, [str(a), str(inc), f'{a} {a}', str(a * inc + 1), out + '0'], why + '.')
    return Q(stem, out, f'{why} [2]', marks=2)


@t1_1.add('C3', (2, 3, 4, 5))
def t1_1_decl(r, D):
    d = ctx(r)
    kind = r.choice(['enum', 'ptr', 'set', 'rec'])
    if kind == 'enum':
        nm, vals = r.choice(ENUMS)
        stem = f'{d["p"]} needs a data type {nm} whose only values are ' + ', '.join(vals) + '. Write the pseudocode to declare the type and a variable of that type, and assign it the value ' + vals[1] + '.'
        ans = code([f'TYPE {nm} = (' + ', '.join(vals) + ')', f'DECLARE Current : {nm}', f'Current ← {vals[1]}'])
        return Q(stem, ans, '1 mark TYPE with list in brackets; 1 mark DECLARE variable of the type; 1 mark assignment [3]', marks=3)
    if kind == 'ptr':
        base = r.choice(['INTEGER', 'REAL', 'STRING', 'CHAR'])
        nm = 'T' + base.capitalize() + 'Pointer'
        stem = f'Write pseudocode to declare a pointer type {nm} that points to a {base}, declare a variable of type {base} and a pointer, and make the pointer point to the variable.'
        ans = code([f'TYPE {nm} = ^{base}', f'DECLARE Item : {base}', f'DECLARE ItemPtr : {nm}', 'ItemPtr ← @Item'])
        return Q(stem, ans, '1 mark TYPE ... = ^type; 1 mark both declarations; 1 mark ← @ variable [3]', marks=3)
    if kind == 'set':
        nm, vals = r.choice(ENUMS)
        stem = f'A set type is needed to store a group of values chosen from ' + ', '.join(vals) + f'. Write pseudocode to define the set type and a set containing {vals[0]} and {vals[-1]}, and describe one operation that can be performed on a set.'
        ans = code([f'TYPE {nm}Set = SET OF STRING', f'DEFINE Chosen ("{vals[0]}", "{vals[-1]}") : {nm}Set']) + '\nOperations: union, intersection, difference, membership test (IN), adding/removing values.'
        return Q(stem, ans, '1 mark TYPE ... SET OF; 1 mark DEFINE with values; 1 mark operation [3]', marks=3)
    fs = r.choice([('TEmployee', [('Name', 'STRING'), ('StartDate', 'DATE'), ('Salary', 'REAL'), ('Grade', 'CHAR')]), ('TSensor', [('SensorID', 'INTEGER'), ('Location', 'STRING'), ('LastReading', 'REAL'), ('Active', 'BOOLEAN')]),
                   ('TOrder', [('OrderNo', 'INTEGER'), ('OrderDate', 'DATE'), ('Total', 'REAL'), ('Paid', 'BOOLEAN')])])
    stem = f'{d["org"]} needs a record type {fs[0]} with the fields ' + ', '.join(f for f, _ in fs[1]) + '. Write the pseudocode to declare it, then declare a pointer type to the record.'
    ans = code([f'TYPE {fs[0]}'] + [f'{IND}DECLARE {f} : {t}' for f, t in fs[1]] + ['ENDTYPE', f'TYPE {fs[0]}Pointer = ^{fs[0]}'])
    return Q(stem, ans, '1 mark TYPE/ENDTYPE; 1 mark fields with suitable types; 1 mark pointer type [3]', marks=3)


@t1_1.add('C3', (2, 3, 4))
def t1_1_enum(r, D):
    nm, vals = r.choice(ENUMS)
    i, j = r.sample(range(len(vals)), 2)
    return Q(f'The enumerated type {nm} = (' + ', '.join(vals) + f') is declared. State whether the condition {vals[i]} < {vals[j]} is TRUE or FALSE and explain why.',
             f'{"TRUE" if i < j else "FALSE"}: enumerated values are ordered by their position in the list ({vals[i]} is position {i + 1}, {vals[j]} is position {j + 1}).', '1 mark value; 1 mark reason (ordinal position) [2]', marks=2)


scen(t1_1, 'C4', (3, 4, 5), [
    '{p} is writing a program for {org} in {city} that manages staff rotas.',
    '{org} is developing a booking system and wants to use user-defined data types.',
], [lambda r, d: (lambda e: (f'Declare an enumerated type {e[0]} for the values ' + ', '.join(e[1]) + '.', f'TYPE {e[0]} = (' + ', '.join(e[1]) + ')', '1 mark TYPE; 1 mark values [2]'))(r.choice(ENUMS)),
    ('Explain why a record type would be used for the staff details.', 'Groups related fields of different data types under one identifier; an array of records holds all staff.', '1 mark each [2]'),
    ('Explain what is meant by a pointer and how it could link records together.', 'A pointer holds a memory address; each record can hold a pointer to the next record, forming a linked list.', '1 mark each [2]'),
    ('Explain how a class differs from a record.', 'A class contains methods (procedures/functions) as well as attributes, and supports encapsulation; a record has data fields only.', '1 mark each [2]'),
    ('Describe a situation in which a set type would be useful.', 'e.g. storing the days on which a member is available and testing membership or finding common days with intersection.', '1 mark situation; 1 mark operation [2]')], k=(3, 4))

FILEORG = [('serial', 'records are stored one after another in the order they were added (chronological), with no key order', 'a log of transactions or sensor readings recorded as they happen'),
           ('sequential', 'records are stored in order of a key field', 'a payroll master file processed in order of employee number in a batch run'),
           ('random (direct)', 'records are stored at an address calculated from the key using a hashing algorithm', 'a bank customer file where any account must be found quickly')]
t1_2 = topic('File organisation: serial, sequential and random files', 'file organisation', 'serial, sequential and random files')
t1_2.fixed('C1', (1, 2), [(f'In {n} file organisation, how are records stored?', d[0].upper() + d[1:], f'{n}: {d}.', [x[1][0].upper() + x[1][1:] for x in FILEORG if x[0] != n] + ['Records are stored in a different file for each field']) for n, d, _ in FILEORG] + [
    ('In a serial file, where is a new record added?', 'At the end of the file', 'Serial files append records in arrival order.', ['In key order', 'At an address calculated by hashing', 'At the start of the file']),
    ('Why must a new file usually be created when a record is inserted into a sequential file?', 'Records after the insertion point must be moved to keep key order', 'Copy records up to the insertion point, write the new record, copy the rest.', ['Sequential files cannot be read', 'The hash table is full', 'Sequential files have no key field']),
])
t1_2.fixed('C2', (2, 3, 4), [
    ('Explain why a random file is suitable for a system where individual records must be found very quickly.', 'The address of a record is calculated from its key by a hashing algorithm, so the record can be accessed directly without reading other records.', '1 mark each [2]'),
    ('Explain how a record is inserted into a sequential file.', 'A new file is created: records from the old file are copied until the correct key position is found, the new record is written, then the remaining records are copied.', '1 mark per step, max 3 [3]'),
])


@t1_2.add('C3', (1, 2, 3, 4))
def t1_2_pick(r, D):
    uses = [('a log of all the readings taken by a weather station', 'serial'), ('a file of employee records processed in ID order once a month to produce payslips', 'sequential'),
            ('a file of customer accounts that must be accessed instantly at a cash machine', 'random'), ('a file of transactions recorded during a day before sorting', 'serial'),
            ('a master file of student records updated in a weekly batch run in student number order', 'sequential'), ('a file of airline seat bookings checked immediately when a customer chooses a seat', 'random'),
            ('a file of goods received at a warehouse, written as each delivery arrives', 'serial'), ('a library catalogue where any book record must be found instantly by its ISBN', 'random')]
    u, o = r.choice(uses)
    if D <= 2:
        return MCQ(r, f'Which file organisation is most suitable for {u}?', o, [x for x in ['serial', 'sequential', 'random', 'indexed sequential'] if x != o], f'{o} organisation suits {u}.')
    reason = {'serial': 'records are simply appended in the order they occur and later processed in that order', 'sequential': 'all records are processed in key order in a batch, so key order makes processing efficient',
              'random': 'any record can be accessed directly by hashing its key, so access is fast'}[o]
    return Q(f'State the most suitable file organisation for {u} and justify your choice.', f'{o}: {reason}.', '1 mark organisation; 2 marks justification [3]', marks=3)


scen(t1_2, 'C4', (3, 4, 5), [
    '{org} in {city} keeps a file of 50 000 customer records and a daily file of transactions.',
    '{p} is designing the files for a hospital patient system at {org}.',
], [('Recommend an organisation for the daily transaction file and justify it.', 'Serial: transactions appended as they occur; later sorted for batch processing.', '1 mark choice; 1 mark reason [2]'),
    ('Recommend an organisation for the main record file and justify it.', 'Random (direct) for fast access to any record; or sequential if only batch processed.', '1 mark choice; 2 marks reason [3]'),
    ('Describe how records are added to a sequential file.', 'Copy records before the insertion point to a new file; write new record; copy remainder.', '1 mark per step [3]'),
    ('Explain one disadvantage of random file organisation.', 'Collisions must be handled; processing all records in key order is slow; space may be wasted.', '1 mark each [2]')], k=(2, 3))


def hash_insert(keys, n, method='linear'):
    table = [None] * n
    log = []
    for k in keys:
        h = k % n
        pos = h
        steps = 0
        while table[pos] is not None and steps < n:
            pos = (pos + 1) % n
            steps += 1
        if table[pos] is None:
            table[pos] = k
        log.append((k, h, pos))
    return table, log


t1_3 = topic('File access methods: sequential and direct access; hashing algorithms', 'file access methods', 'sequential and direct access', 'hashing algorithms')
t1_3.fixed('C1', (1, 2, 3), [
    ('What is a hashing algorithm used for in random files?', 'To calculate the address of a record from its key', 'e.g. address = key MOD number of locations.', ['To encrypt the records', 'To sort the records into order', 'To compress the file']),
    ('What is a collision in hashing?', 'When two different keys produce the same address', 'Collisions are resolved by open addressing (next free location) or an overflow area/chaining.', ['When a record is deleted', 'When the file is full', 'When a key is not found']),
    ('Which access method reads records one after another from the start of the file?', 'Sequential access', 'Sequential access can be used on serial or sequential files.', ['Direct access', 'Hashing', 'Indexed binary access']),
    ('Which access method goes straight to a record without reading the others?', 'Direct access', 'Direct (random) access uses the address calculated by hashing or an index.', ['Sequential access', 'Serial access', 'Linear search']),
    ('Using address = key MOD 7, what is the address for key 45?', '3', '45 MOD 7 = 3 (7 × 6 = 42).', ['6', '4', '5']),
])
t1_3.fixed('C2', (2, 3, 4), [
    ('Describe two methods of handling collisions in a random file.', 'Open addressing: store the record in the next free location; overflow area: store it in a separate overflow area (or chain records from the home address).', '1 mark each with description [2]'),
    ('Explain why searching for a record in a random file may need more than one read after collisions.', 'The record may not be at its home address; the program must check the next locations (or overflow area) until it finds the key or an empty slot.', '1 mark each [2]'),
])


@t1_3.add('C3', (1, 2, 3, 4, 5))
def t1_3_hash(r, D):
    n = r.choice([7, 11, 13]) if D >= 3 else r.choice([7, 10, 11])
    cnt = 5 if D <= 3 else 7
    keys = r.sample(range(100, 999), cnt)
    # force at least one collision
    keys[-1] = keys[0] + n * r.randrange(1, 5)
    table, log = hash_insert(keys, n)
    if D == 1:
        k = keys[0]
        return MCQ(r, f'Records are stored using the hashing algorithm address = key MOD {n}. What is the home address for key {k}?', str(k % n), [str(k // n), str((k % n) + 1), str(n - k % n), str(k % (n + 1))], f'{k} MOD {n} = {k % n}.')
    stem = f'Records are stored in a random file with {n} locations (0 to {n - 1}) using address = key MOD {n}. A collision is resolved by storing the record in the next free location (wrapping to 0). The keys {", ".join(map(str, keys))} are inserted in order. Give the address where each key is stored.'
    ans = ', '.join(f'{k} → {p}' for k, h, p in log)
    key = '; '.join(f'{k} MOD {n} = {h}' + (f', collision, stored at {p}' if h != p else '') for k, h, p in log)
    m = 3 if D <= 3 else 4
    return Q(stem, ans, f'{key}. Award {m} for all correct, deduct 1 per error [{m}]', marks=m)


@t1_3.add('C3', (2, 3, 4, 5))
def t1_3_search(r, D):
    n = r.choice([7, 11])
    keys = r.sample(range(100, 999), 5)
    keys[2] = keys[0] + n
    keys[3] = keys[0] + 2 * n
    table, log = hash_insert(keys, n)
    target = keys[3]
    h = target % n
    reads = 1
    pos = h
    while table[pos] != target:
        pos = (pos + 1) % n
        reads += 1
    tbl = ', '.join(f'[{i}] {v if v is not None else "empty"}' for i, v in enumerate(table))
    return Q(f'A random file uses address = key MOD {n} with collisions placed in the next free location. Its contents are: {tbl}. Describe how the record with key {target} is found and state the number of locations read.',
             f'Hash {target} MOD {n} = {h}; read location {h}' + (', not the key, so read the following locations until it is found' if reads > 1 else ', key matches') + f' at {pos}. {reads} reads.',
             f'1 mark hash calculation {h}; 1 mark linear probing explained; 1 mark {reads} reads [3]', marks=3)


@t1_3.add('C4', (3, 4, 5), 'multi_step')
def t1_3_code(r, D):
    n = r.choice([100, 200, 500, 1000])
    d = ctx(r)
    stem = (f'{d["org"]} stores {n // 2} customer records in a random file with {n} locations. The key is a 6-digit customer number. (a) Write a pseudocode function Hash(Key : INTEGER) RETURNS INTEGER using the MOD operator. '
            f'(b) Write pseudocode that uses Hash to find the record for a key input by the user, using the next free location for collisions; use SEEK and GETRECORD. (c) Explain why the file has more locations than records.')
    ans = code(['FUNCTION Hash(Key : INTEGER) RETURNS INTEGER', f'{IND}RETURN Key MOD {n}', 'ENDFUNCTION', '', 'INPUT SearchKey', 'Address ← Hash(SearchKey)', 'OPENFILE "Customers.dat" FOR RANDOM', 'Found ← FALSE', 'Count ← 0',
                'WHILE NOT Found AND Count < ' + str(n), f'{IND}SEEK "Customers.dat", Address', f'{IND}GETRECORD "Customers.dat", Customer', f'{IND}IF Customer.Key = SearchKey THEN', f'{IND}{IND}Found ← TRUE', f'{IND}ELSE',
                f'{IND}{IND}Address ← (Address + 1) MOD {n}', f'{IND}{IND}Count ← Count + 1', f'{IND}ENDIF', 'ENDWHILE', 'CLOSEFILE "Customers.dat"']) + '\n(c) Spare locations reduce the number of collisions and the length of probe sequences.'
    return Q(stem, ans, '(a) header and RETURN Key MOD n [2] (b) open RANDOM [1]; SEEK and GETRECORD [1]; compare key [1]; move to next location with wrap [1]; loop termination [1] (c) [1]', marks=8, typ='multi_step')


CHAPTERS[1] = [t1_1, t1_2, t1_3]

# =============================================================================== Chapter 2 Floating-point numbers
def fp_val(m, e):
    """m, e: bit strings, two's complement; binary point after the first mantissa bit."""
    M = from_tc(m)
    E = from_tc(e)
    return Fraction(M, 1 << (len(m) - 1)) * (Fraction(2) ** E)


def fdec(x):
    """Exact decimal string for a dyadic fraction."""
    if x.denominator == 1:
        return str(x.numerator)
    sign = '-' if x < 0 else ''
    x = abs(x)
    ip = x.numerator // x.denominator
    fr = x - ip
    digits = ''
    while fr and len(digits) < 20:
        fr *= 10
        dg = fr.numerator // fr.denominator
        digits += str(dg)
        fr -= dg
    return f'{sign}{ip}.{digits}'


def fp_rand_norm(r, mb, eb, neg=None):
    neg = r.random() < 0.4 if neg is None else neg
    body = ''.join(r.choice('01') for _ in range(mb - 2))
    m = ('10' if neg else '01') + body
    emax = (1 << (eb - 1)) - 1
    E = r.randrange(-3, min(emax, 7) + 1)
    return m, tc(E, eb)


def is_norm(m):
    return m[0] != m[1]


def normalise(m, e):
    M = from_tc(m)
    E = from_tc(e)
    mb = len(m)
    if M == 0:
        return m, e, 0
    shifts = 0
    while True:
        s = tc(M, mb)
        if s[0] != s[1]:
            break
        M *= 2
        E -= 1
        shifts += 1
    return tc(M, mb), tc(E, len(e)), shifts


t2_1 = topic('Floating-point representation: mantissa and exponent in two\'s complement', 'floating-point representation', 'mantissa and exponent')
t2_1.fixed('C1', (1, 2, 3), [
    ('In floating-point representation, what does the exponent determine?', 'The position of the binary point (how far it moves)', 'Value = mantissa × 2^exponent.', ['The sign of the number only', 'The number of significant bits', 'The number of bytes used']),
    ('In a two\'s complement mantissa with the binary point after the first bit, what is the place value of the first bit?', '−1', 'The sign bit has weight −1; then 1/2, 1/4, 1/8, ...', ['1', '−128', '1/2']),
    ('What is the value of the exponent 1101 in 4-bit two\'s complement?', '−3', '−8 + 4 + 1 = −3.', ['13', '3', '−5']),
    ('Why is floating-point representation used for real numbers?', 'It can represent a very wide range of values, both very large and very small', 'Fixed point has limited range for the same number of bits.', ['It is always exact', 'It uses fewer bits than integers', 'It cannot represent negative numbers']),
    ('What does the mantissa hold in floating-point representation?', 'The significant digits of the number', 'Mantissa: the precision; exponent: the range/scale.', ['The position of the binary point', 'Only the sign of the number', 'The number of bits used']),
])
t2_1.fixed('C2', (2, 3, 4), [
    ('Explain why both the mantissa and the exponent are stored in two\'s complement.', 'The mantissa must represent negative numbers and the exponent must represent negative powers of 2 (small fractions), so both need to be signed.', '1 mark each [2]'),
    ('Explain the effect of a negative exponent on the value of a floating-point number.', 'The binary point moves to the left, making the magnitude smaller (a fraction).', '1 mark each [2]'),
])


@t2_1.add('C3', (1, 2, 3, 4, 5))
def t2_1_val(r, D):
    mb, eb = (8, 4) if D <= 3 else r.choice([(10, 6), (12, 4), (8, 8)])
    m, e = fp_rand_norm(r, mb, eb, neg=(r.random() < 0.5) if D >= 3 else False)
    v = fp_val(m, e)
    E = from_tc(e)
    stem = f'A floating-point number uses {art(mb)} {mb}-bit mantissa and {art(eb)} {eb}-bit exponent, both in two\'s complement. Calculate the denary value of mantissa {m}, exponent {e}.'
    key = f'Exponent {e} = {E} [1]; move the binary point {abs(E)} place{"s" if abs(E) != 1 else ""} {"right" if E >= 0 else "left"} (mantissa {fdec(Fraction(from_tc(m), 1 << (mb - 1)))} × 2^{E}) [1]; value {fdec(v)} [1] [3]'
    if D == 1:
        return MCQ(r, stem.replace('Calculate the denary value', 'What is the denary value').rstrip('.') + '?', fdec(v), [fdec(v * 2), fdec(v / 2), fdec(-v), fdec(fp_val(m, tc(-E, eb)))], key.replace(' [1]', '').replace(' [3]', ''))
    return Q(stem, fdec(v), key, marks=3)


@t2_1.add('C3', (2, 3, 4, 5), 'numerical')
def t2_1_to(r, D):
    mb, eb = (8, 4) if D <= 3 else (10, 4)
    m, e = fp_rand_norm(r, mb, eb, neg=(r.random() < 0.5) if D >= 3 else False)
    v = fp_val(m, e)
    stem = f'Convert the denary number {fdec(v)} into a normalised floating-point number with {art(mb)} {mb}-bit mantissa and {art(eb)} {eb}-bit exponent, both in two\'s complement.'
    key = (f'{fdec(v)} in binary, normalised so the mantissa starts {"01" if v > 0 else "10"} [1]; mantissa {m} [1]; exponent {e} (= {from_tc(e)}) [1] [3]')
    return Q(stem, f'Mantissa {m}, exponent {e}', key, marks=3)


@t2_1.add('C4', (3, 4, 5), 'multi_step')
def t2_1_compare(r, D):
    m1, e1 = fp_rand_norm(r, 8, 4, neg=False)
    m2, e2 = fp_rand_norm(r, 8, 4, neg=True)
    v1, v2 = fp_val(m1, e1), fp_val(m2, e2)
    stem = (f'Two floating-point numbers use an 8-bit mantissa and a 4-bit exponent in two\'s complement. P: mantissa {m1}, exponent {e1}. Q: mantissa {m2}, exponent {e2}. '
            f'(a) Calculate the denary value of P. (b) Calculate the denary value of Q. (c) Calculate P + Q in denary. (d) State, with a reason, whether both numbers are normalised.')
    s = v1 + v2
    return Q(stem, f'(a) {fdec(v1)} (b) {fdec(v2)} (c) {fdec(s)} (d) yes: P starts 01 (positive) and Q starts 10 (negative)',
             f'(a) exponent {from_tc(e1)}; {fdec(v1)} [2] (b) exponent {from_tc(e2)}; {fdec(v2)} [2] (c) {fdec(s)} [1] (d) first two mantissa bits differ in both [1]', marks=6, typ='multi_step')


t2_2 = topic('Normalisation of floating-point numbers and converting between denary and floating-point', 'normalisation of floating-point numbers', 'converting between denary and floating-point')
t2_2.fixed('C1', (1, 2, 3), [
    ('A positive normalised floating-point mantissa always starts with which two bits?', '01', 'Positive normalised: 0 then 1; negative normalised: 1 then 0.', ['10', '00', '11']),
    ('A negative normalised floating-point mantissa always starts with which two bits?', '10', 'The first two bits of a normalised mantissa are different.', ['01', '11', '00']),
    ('Why are floating-point numbers normalised?', 'To give the maximum precision for the number of bits and a unique representation', 'Leading redundant sign bits are removed, so more significant bits are kept.', ['To increase the range of the exponent', 'To make all numbers positive', 'To convert them into integers']),
    ('When a mantissa is shifted one place left during normalisation, what happens to the exponent?', 'It is decreased by 1', 'Shifting the mantissa left doubles it, so the exponent decreases by 1 to keep the value the same.', ['It is increased by 1', 'It is unchanged', 'It is doubled']),
])
t2_2.fixed('C2', (2, 3, 4), [
    ('Explain how to normalise a positive floating-point number whose mantissa begins 0001.', 'Shift the mantissa left until it begins 01 (two places), filling with zeros on the right, and subtract the number of places shifted (2) from the exponent.', '1 mark shift left until 01; 1 mark subtract shifts from exponent [2]'),
    ('Explain why a normalised representation gives the best precision.', 'Redundant leading sign bits are removed so all the mantissa bits are used for significant digits.', '1 mark each [2]'),
])


@t2_2.add('C3', (1, 2, 3, 4, 5))
def t2_2_norm(r, D):
    mb, eb = 8, 4
    for _ in range(30):
        m, e = fp_rand_norm(r, mb, eb, neg=(r.random() < 0.5) if D >= 2 else False)
        M, E = from_tc(m), from_tc(e)
        k = r.randrange(1, 4)
        if (M % (1 << k)) != 0 or not (-8 <= E + k <= 7):
            continue
        dm, de = tc(M >> k, mb), tc(E + k, eb)
        if is_norm(dm):
            continue
        nm, ne, sh = normalise(dm, de)
        break
    else:
        return None
    stem = f'The floating-point number with mantissa {dm} and exponent {de} (8-bit mantissa, 4-bit exponent, two\'s complement) is not normalised. Normalise it, giving the new mantissa and exponent.'
    key = f'Shift the mantissa {sh} place{"s" if sh > 1 else ""} left so the first two bits differ: {nm} [1]; exponent {from_tc(de)} − {sh} = {from_tc(ne)} = {ne} [1] [2]'
    if D == 1:
        return MCQ(r, stem.replace('Normalise it, giving the new mantissa and exponent.', 'Which is its normalised form?'), f'mantissa {nm}, exponent {ne}',
                   [f'mantissa {nm}, exponent {tc(from_tc(de) + sh, eb)}', f'mantissa {dm}, exponent {ne}', f'mantissa {tc(from_tc(nm) // 2 if sh else from_tc(nm), mb)}, exponent {de}'], key.replace(' [1]', '').replace(' [2]', ''))
    if D >= 4:
        stem += ' Then give the denary value and explain why the value is unchanged.'
        return Q(stem, f'Mantissa {nm}, exponent {ne}; value {fdec(fp_val(nm, ne))}', key.replace(' [2]', '') + f'; value {fdec(fp_val(nm, ne))} [1]; mantissa doubled for each shift and exponent reduced by 1, so value same [1] [4]', marks=4)
    return Q(stem, f'Mantissa {nm}, exponent {ne}', key, marks=2)


@t2_2.add('C3', (2, 3, 4, 5))
def t2_2_conv(r, D):
    m, e = fp_rand_norm(r, 8, 4, neg=r.random() < 0.5)
    v = fp_val(m, e)
    if r.random() < 0.5:
        return Q(f'Show how the denary number {fdec(v)} is represented as a normalised floating-point number with an 8-bit mantissa and 4-bit exponent in two\'s complement. Show your working.',
                 f'Mantissa {m}, exponent {e}', f'binary form of {fdec(abs(v))} [1]' + ('; two\'s complement for the negative value [1]' if v < 0 else '; [1] for placing the point') + f'; normalised mantissa {m} [1]; exponent {e} [1] [4]', marks=4)
    return Q(f'A normalised floating-point number has mantissa {m} and exponent {e} (8-bit mantissa, 4-bit exponent, two\'s complement). Convert it to denary, showing your working.',
             fdec(v), f'exponent {from_tc(e)} [1]; binary point moved [1]; {fdec(v)} [1] [3]', marks=3)


scen(t2_2, 'C4', (3, 4, 5), [
    'A scientific instrument at {org} stores readings as 8-bit mantissa, 4-bit exponent floating-point numbers.',
    '{p} is writing an emulator that shows how a processor stores real numbers in floating-point form.',
], [lambda r, d: (lambda me: (f'Convert mantissa {me[0]}, exponent {me[1]} to denary.', fdec(fp_val(*me)), f'exponent {from_tc(me[1])}; value {fdec(fp_val(*me))} [2]'))(fp_rand_norm(r, 8, 4)),
    lambda r, d: (lambda me: (f'Convert {fdec(fp_val(*me))} into normalised floating-point form.', f'mantissa {me[0]}, exponent {me[1]}', '1 mark mantissa; 1 mark exponent [2]'))(fp_rand_norm(r, 8, 4)),
    ('Explain why the readings should be stored in normalised form.', 'Maximum precision for the bits available and a unique representation of each value.', '1 mark each [2]'),
    ('State how you can tell whether a negative mantissa is normalised.', 'Its first two bits are 10.', '1 mark [1]')], k=(3, 4))

t2_3 = topic('Trade-off between range and precision; rounding errors, overflow and underflow', 'range and precision', 'rounding errors', 'overflow and underflow')
t2_3.fixed('C1', (1, 2, 3), [
    ('If more bits are given to the exponent and fewer to the mantissa (same total), what happens?', 'The range increases but the precision decreases', 'Exponent → range; mantissa → precision.', ['The range and precision both increase', 'The precision increases but the range decreases', 'Neither changes']),
    ('What is underflow in floating-point arithmetic?', 'A result is too close to zero to be represented', 'Underflow: magnitude smaller than the smallest representable value (exponent too negative).', ['A result is too large to be represented', 'A rounding error in the last bit', 'A negative mantissa']),
    ('What is overflow in floating-point arithmetic?', 'A result is too large in magnitude to be represented', 'The exponent needed exceeds its maximum.', ['A result is too close to zero', 'The mantissa is not normalised', 'Two numbers are subtracted']),
    ('Why can 0.1 not be stored exactly in binary floating-point?', 'Its binary form is a recurring fraction that would need infinitely many bits', '0.1 = 0.000110011... in binary, so it is rounded.', ['It is too large', 'It is negative', 'It needs a negative exponent']),
])
t2_3.fixed('C2', (2, 3, 4), [
    ('Explain why rounding errors can build up in a program that adds 0.1 many times.', '0.1 cannot be stored exactly, so each addition includes a small error; repeated additions accumulate the errors so the final total differs from the true value.', '1 mark: 0.1 not exact; 1 mark: errors accumulate [2]'),
    ('Explain why a programmer should not test two real numbers for exact equality.', 'Rounding errors mean values that should be equal may differ slightly; test whether the difference is less than a small tolerance instead.', '1 mark each [2]'),
])


@t2_3.add('C3', (2, 3, 4, 5), 'numerical')
def t2_3_range(r, D):
    mb, eb = r.choice([(8, 4), (10, 6), (12, 4), (8, 8), (6, 4)])
    emax = (1 << (eb - 1)) - 1
    emin = -(1 << (eb - 1))
    big = Fraction((1 << (mb - 1)) - 1, 1 << (mb - 1)) * Fraction(2) ** emax
    small = Fraction(1, 2) * Fraction(2) ** emin
    neg = Fraction(-1) * Fraction(2) ** emax
    kind = r.choice(['big', 'small', 'neg'])
    if kind == 'big':
        q, m, e, v = 'largest positive value', '0' + '1' * (mb - 1), '0' + '1' * (eb - 1), big
    elif kind == 'small':
        q, m, e, v = 'smallest positive normalised value', '01' + '0' * (mb - 2), '1' + '0' * (eb - 1), small
    else:
        q, m, e, v = 'most negative value', '1' + '0' * (mb - 1), '0' + '1' * (eb - 1), neg
    vs = fdec(v) if abs(v) >= Fraction(1, 1 << 12) and len(fdec(v)) < 22 else f'{float(v):.6g}'
    stem = f'A floating-point system uses {art(mb)} {mb}-bit mantissa and {art(eb)} {eb}-bit exponent, both in two\'s complement. Give the mantissa and exponent of the {q} that can be represented, and its denary value.'
    return Q(stem, f'Mantissa {m}, exponent {e}; {vs}' + (f' (2^{emin - 1})' if kind == 'small' else ''), f'mantissa {m} [1]; exponent {e} = {from_tc(e)} [1]; value {vs} [1] [3]', marks=3)


@t2_3.add('C3', (1, 2, 3, 4))
def t2_3_tradeoff(r, D):
    tot = r.choice([12, 16, 20, 24])
    a = r.randrange(tot // 2, tot - 3)
    c = r.choice([x for x in range(tot // 2, tot - 2) if x != a])
    more_m = max(a, c)
    stem = f'A system can split {tot} bits between mantissa and exponent as either {a}/{tot - a} or {c}/{tot - c} (mantissa/exponent). Which split gives the greater precision?'
    ans = f'{more_m}/{tot - more_m}'
    key = f'More mantissa bits give more precision; {more_m}/{tot - more_m} has the longer mantissa (but a smaller range).'
    if D <= 2:
        return MCQ(r, stem, ans, [f'{min(a, c)}/{tot - min(a, c)}', 'Both give the same precision', 'Precision depends only on the exponent'], key)
    return Q(stem.replace('Which split gives the greater precision?', 'State which split gives the greater precision and which gives the greater range, explaining why.'),
             f'Precision: {more_m}/{tot - more_m}; range: {min(a, c)}/{tot - min(a, c)}', '1 mark precision choice; 1 mark range choice; 1 mark explanation (mantissa → precision, exponent → range) [3]', marks=3)


@t2_3.add('C4', (3, 4, 5), 'multi_step')
def t2_3_err(r, D):
    n = r.choice([10, 100, 1000])
    d = ctx(r)
    stem = (f'{d["p"]} writes a program for {d["org"]} that adds 0.1 to a REAL variable Total, starting from 0, {n} times, then tests IF Total = {n / 10:g} THEN OUTPUT "Correct". '
            f'(a) Explain why "Correct" may not be output. (b) Suggest how the test should be rewritten. (c) Explain how increasing the number of bits in the mantissa would affect the problem.')
    return Q(stem, f'(a) 0.1 cannot be stored exactly in binary, so each addition adds a small rounding error; after {n} additions Total is not exactly {n / 10:g} (b) IF ABS(Total − {n / 10:g}) < 0.0001 THEN ... (c) more mantissa bits give greater precision so the error is smaller, but it is not removed',
             '(a) 0.1 not exact [1]; rounding errors accumulate [1] (b) compare with a tolerance [2] (c) smaller error but still present [2]', marks=6, typ='multi_step')


ar(t2_3, [('Increasing the number of bits in the mantissa increases precision.', 'More significant bits can be stored, so the number can be represented more accurately.'),
          ('Increasing the number of bits in the exponent increases the range.', 'The binary point can be moved further left or right, giving larger and smaller magnitudes.'),
          ('Underflow can occur when two very small numbers are multiplied.', 'The result may need an exponent more negative than the smallest exponent available.'),
          ('The denary value 0.1 cannot be stored exactly in binary floating-point.', 'Its binary representation is a recurring fraction.')],
   ['Increasing exponent bits increases precision.', 'Floating-point numbers never have rounding errors.', 'Overflow occurs when a result is too close to zero.', 'A normalised positive mantissa starts with 10.'])

CHAPTERS[2] = [t2_1, t2_2, t2_3]

# =============================================================================== Chapter 3 Communication and internet technologies
LAYERS = [('application', 'provides the protocols used by applications, e.g. HTTP, FTP, SMTP, POP3, IMAP', ['HTTP', 'FTP', 'SMTP', 'POP3', 'IMAP', 'DNS']),
          ('transport', 'splits data into segments/packets, adds port numbers and sequence numbers, and ensures reliable delivery (TCP) or fast delivery (UDP)', ['TCP', 'UDP']),
          ('internet (network)', 'adds source and destination IP addresses and routes packets between networks', ['IP']),
          ('link', 'transmits frames over the physical network, using MAC addresses', ['Ethernet', 'Wi-Fi'])]
PROTOS = [('HTTP', 'transfers web pages from a web server to a browser'), ('HTTPS', 'transfers web pages securely using encryption (TLS)'),
          ('FTP', 'transfers files between a client and a server'), ('SMTP', 'sends (pushes) email from a client to a server and between mail servers'),
          ('POP3', 'downloads email from a server to a single client, usually deleting it from the server'),
          ('IMAP', 'accesses email kept on the server so it can be synchronised across several devices'), ('TCP', 'provides reliable, ordered delivery of segments with acknowledgements and retransmission'),
          ('IP', 'addresses and routes packets across networks')]
t3_1 = topic('Protocols and the TCP/IP four-layer stack; HTTP, FTP, POP3, IMAP and SMTP', 'protocols', 'tcp/ip', 'http, ftp, pop3, imap and smtp')
t3_1.fixed('C1', (1, 2), [(f'What is the purpose of {p}?', d[0].upper() + d[1:], f'{p} {d}.', [x[1][0].upper() + x[1][1:] for x in PROTOS if x[0] != p][:5]) for p, d in PROTOS] + [
    ('What is a protocol?', 'A set of rules that govern how data is transmitted between devices', 'Protocols allow devices from different manufacturers to communicate.', ['A type of network cable', 'A program that removes viruses', 'A hardware device that connects networks']),
    ('Why is a protocol stack divided into layers?', 'Each layer has a specific job and can be changed without affecting the others', 'Layering simplifies design, allows standardisation and independent development.', ['To make the data larger', 'So that only one protocol is used', 'To encrypt data at every layer']),
    ('Which layer of the TCP/IP stack adds the destination IP address?', 'Internet (network) layer', 'IP addressing and routing are at the internet layer.', ['Application layer', 'Transport layer', 'Link layer']),
])
t3_1.fixed('C2', (2, 3, 4), [
    ('Explain the difference between POP3 and IMAP.', 'POP3 downloads emails to one device and usually deletes them from the server; IMAP keeps emails on the server and synchronises them across several devices.', '1 mark each [2]'),
    ('Describe the role of the transport layer when a web page is sent.', 'Splits the data into segments, adds port numbers and sequence numbers; TCP checks for errors, acknowledges receipt and resends lost segments; reassembles in order at the destination.', '1 mark per point, max 3 [3]'),
    ('Explain why a layered protocol stack is used.', 'Each layer deals with one part of communication, so layers can be developed, changed or replaced independently; different hardware/software can interoperate through standard interfaces.', '1 mark per point, max 2 [2]'),
])


@t3_1.add('C3', (1, 2, 3, 4))
def t3_1_layer(r, D):
    L = r.choice(LAYERS)
    pr = r.choice(L[2])
    if D <= 2:
        return MCQ(r, f'At which layer of the TCP/IP stack does {pr} operate?', L[0] + ' layer', [x[0] + ' layer' for x in LAYERS if x[0] != L[0]], f'{pr}: {L[0]} layer, which {L[1]}.')
    d = ctx(r)
    task = r.choice(['downloads a web page', 'sends an email with an attachment', 'uploads a file to a server', 'reads email on a phone and a laptop'])
    proto = {'downloads a web page': 'HTTP/HTTPS', 'sends an email with an attachment': 'SMTP', 'uploads a file to a server': 'FTP', 'reads email on a phone and a laptop': 'IMAP'}[task]
    return Q(f'{d["p"]} {task}. Name the application layer protocol used and describe what happens to the data at each of the four layers of the TCP/IP stack as it is sent.',
             f'{proto}. Application: {proto} formats the request/data; transport: TCP splits into segments with port and sequence numbers; internet: IP adds source/destination IP addresses and routes packets; link: frames sent over the physical network using MAC addresses.',
             '1 mark protocol; 1 mark per layer described [5]', marks=5)


scen(t3_1, 'C4', (3, 4, 5), [
    '{org} in {city} runs a web server, a file server and an email server.',
    '{p} uses a laptop and a phone to access email and the company website of {org}.',
], [('Explain why IMAP is more suitable than POP3 for staff who use several devices.', 'IMAP keeps mail on the server and synchronises all devices; POP3 downloads to one device and may delete from the server.', '1 mark each [2]'),
    ('Describe the role of SMTP.', 'Sends email from the client to the mail server and between servers.', '1 mark each [2]'),
    ('Explain how TCP ensures a large file arrives correctly.', 'Sequence numbers to reorder; acknowledgements; retransmission of lost/corrupt segments; checksums.', '1 mark per point, max 3 [3]'),
    ('Explain why HTTPS should be used for the login page.', 'Data is encrypted with TLS so passwords cannot be read if intercepted; server identity verified by certificate.', '1 mark each [2]'),
    ('State the purpose of FTP and one situation in which staff would use it.', 'Transfers files between client and server; e.g. uploading web pages to the web server.', '1 mark each [2]')], k=(3, 4))

t3_2 = topic('Circuit switching and packet switching; role of routers', 'circuit switching', 'packet switching', 'role of routers')
t3_2.fixed('C1', (1, 2), [
    ('In circuit switching, what happens before data is sent?', 'A dedicated path is set up between sender and receiver for the whole communication', 'Circuit switching: the route is reserved; all data follows it in order.', ['The data is split into packets that take different routes', 'The data is encrypted', 'Routers decide a new route for each packet']),
    ('In packet switching, which statement is true?', 'Packets may take different routes and arrive out of order', 'Each packet is routed independently and reassembled at the destination using sequence numbers.', ['All packets must follow the same reserved path', 'No routers are needed', 'Packets are never lost']),
    ('What is the role of a router in packet switching?', 'To forward each packet towards its destination using its IP address and a routing table', 'Routers choose the next hop for each packet.', ['To reserve a circuit for each call', 'To assign MAC addresses', 'To reassemble the whole message']),
    ('What does a packet header contain?', 'Source and destination addresses and the packet sequence number', 'Header also includes protocol, length and hop count (TTL); the trailer may hold a checksum.', ['Only the data being sent', 'The password of the user', 'The whole routing table']),
    ('Why does each packet have a hop limit (time to live)?', 'To stop lost packets circulating the network forever', 'TTL is reduced at each router; the packet is discarded at zero.', ['To encrypt the packet', 'To set the speed of the packet', 'To reserve bandwidth']),
])
t3_2.fixed('C2', (2, 3, 4), [
    ('Explain why packet switching makes better use of a network than circuit switching.', 'Links are shared by packets from many users and are only used when data is sent; in circuit switching the reserved path is unavailable to others even when idle.', '1 mark each [2]'),
    ('Explain why circuit switching may be preferred for a live video call.', 'The dedicated path gives a constant bandwidth and data arrives in order with little delay or jitter.', '1 mark each [2]'),
    ('Describe how a message is sent using packet switching.', 'The message is split into packets with headers; each packet is sent independently; routers forward packets on the best available route; packets are reassembled in order at the destination and missing ones requested again.', '1 mark per point, max 3 [3]'),
])


@t3_2.add('C3', (2, 3, 4, 5), 'numerical')
def t3_2_pk(r, D):
    size = r.choice([2000, 4000, 6000, 10000, 12000, 24000])
    payload = r.choice([500, 1000, 1500, 2000])
    hdr = r.choice([20, 40, 60])
    n = math.ceil(size / payload)
    tot = size + n * hdr
    stem = f'A message of {size:,} bytes is sent using packet switching. Each packet carries at most {payload} bytes of data and a header of {hdr} bytes. Calculate the number of packets and the total number of bytes transmitted.'
    return Q(stem, f'{n} packets; {tot:,} bytes', f'{size:,} ÷ {payload} = {n} packets (rounded up) [1]; {size:,} + {n} × {hdr} = {tot:,} bytes [1] [2]', marks=2)


scen(t3_2, 'C2', (2, 3, 4), [
    '{org} in {city} sends large files to a branch office over the internet.', '{p} makes a voice call and downloads a film at the same time.',
], [('State whether packet switching or circuit switching is used on the internet, giving a reason.', 'Packet switching: links shared, no reserved path, resilient routing.', '1 mark each [2]'),
    ('Explain what happens if one router on the route fails.', 'Packets are re-routed by other routers along alternative paths; lost packets are re-sent.', '1 mark each [2]'),
    ('Explain why packets may arrive out of order and how this is dealt with.', 'Different routes with different delays; sequence numbers used to reassemble in order.', '1 mark each [2]'),
    ('Describe two items in a packet header.', 'Source IP, destination IP, sequence number, protocol, TTL/hop count, packet length.', '1 mark each [2]')], k=(2, 3))
essay(t3_2, [('the use of packet switching rather than circuit switching for real-time communication such as video calls', 'efficient sharing of links; resilience as packets can be re-routed; cheaper; works well with buffering and QoS.',
              'variable delay (latency, jitter) and packets arriving out of order or lost can disrupt real-time audio and video; circuit switching gives a guaranteed constant connection.', 'packet switching is now used for most calls because of efficiency, with protocols to reduce jitter.')],
      ['{org} in {city} is choosing a network service for its video conferencing.', '{p} is writing a report on network technologies.'])

t3_3 = topic('Peer-to-peer file sharing with BitTorrent: swarms, seeds, leeches and trackers', 'peer-to-peer file sharing', 'bittorrent', 'swarms, seeds, leeches')
BT = [('swarm', 'all the peers sharing (uploading or downloading) a particular file'), ('seed', 'a peer that has the complete file and uploads it to others'),
      ('leech', 'a peer that downloads but uploads little or nothing'), ('tracker', 'a server that keeps a record of the peers in a swarm and helps peers find each other'),
      ('torrent file', 'a small file containing metadata about the shared file and the address of the tracker'), ('peer', 'any computer taking part in sharing the file')]
t3_3.fixed('C1', (1, 2), [(f'In BitTorrent, what is a {n}?', d[0].upper() + d[1:], f'{n}: {d}.', [x[1][0].upper() + x[1][1:] for x in BT if x[0] != n][:4]) for n, d in BT])
t3_3.fixed('C2', (2, 3, 4), [
    ('Explain why BitTorrent downloads can be faster than downloading from a single server.', 'The file is split into pieces downloaded from many peers at once, so the load is shared and total bandwidth is greater than one server can provide.', '1 mark each [2]'),
    ('Explain why leeches reduce the performance of a swarm.', 'They take pieces without uploading, so fewer sources are available and the load falls on seeds.', '1 mark each [2]'),
])
scen(t3_3, 'C2', (2, 3, 4), [
    '{org} in {city} wants to distribute a large software update to thousands of users.', '{p} downloads a large open-source file using BitTorrent.',
], [('Describe how the file is downloaded using BitTorrent.', 'Torrent file obtained; client contacts tracker for peers in swarm; pieces downloaded from many peers simultaneously; pieces uploaded to others; file reassembled and checked with hashes.', '1 mark per point, max 4 [4]'),
    ('Explain the role of the tracker.', 'It records which peers are in the swarm and tells new peers who to connect to.', '1 mark each [2]'),
    ('Give one benefit and one drawback of using BitTorrent for this purpose.', 'Benefit: reduces load on the company\'s servers/fast; drawback: depends on peers being online; may be blocked or associated with illegal sharing.', '1 mark each [2]')], k=(1, 2, 3))
essay(t3_3, [('the use of peer-to-peer file sharing with BitTorrent by {org} to distribute its files', 'load spread across peers so less server bandwidth; scales well with many users; resilient if one source fails; pieces verified by hashes.',
              'needs enough seeds; users\' upload bandwidth is used; some networks block BitTorrent; reputation linked to illegal sharing of copyrighted material.', 'suitable for large, legal, popular files such as software updates.')],
      ['{org} in {city} distributes large files to its customers.', '{p} is advising {org} on file distribution.'])

CHAPTERS[3] = [t3_1, t3_2, t3_3]

# =============================================================================== Chapter 4 Hardware and virtual machines
t4_1 = topic('RISC and CISC processors; pipelining and registers', 'risc and cisc', 'pipelining')
t4_1.fixed('C1', (1, 2), [
    ('Which is a feature of RISC processors?', 'A small set of simple instructions, most taking one clock cycle', 'RISC: fixed-length instructions, many registers, load/store architecture, easy pipelining.', ['Many complex instructions of variable length', 'Few registers', 'Instructions that operate directly on memory in many modes']),
    ('Which is a feature of CISC processors?', 'Many complex instructions, some taking several clock cycles', 'CISC: variable-length instructions, many addressing modes, fewer instructions per program.', ['Only fixed-length instructions', 'Instructions all complete in one cycle', 'No microcode']),
    ('What is pipelining?', 'Overlapping the stages of several instructions so a new one starts before the previous one finishes', 'e.g. fetch, decode, execute, memory access, write back stages run in parallel on different instructions.', ['Running two programs on two cores', 'Storing data in a cache', 'Executing one instruction at a time from start to finish']),
    ('Why does RISC suit pipelining better than CISC?', 'Instructions are of fixed length and take similar times', 'Uniform instructions keep each stage the same length.', ['RISC has more complex instructions', 'RISC uses microprogramming', 'RISC has fewer registers']),
    ('What problem can a conditional branch cause in a pipeline?', 'Instructions already fetched may be the wrong ones and must be flushed', 'Branch hazard: pipeline flushed and refilled, losing cycles.', ['The cache becomes full', 'The clock stops', 'The registers are cleared']),
])
t4_1.fixed('C2', (2, 3, 4), [
    ('Explain why RISC processors have more general-purpose registers than CISC processors.', 'RISC uses a load/store architecture: only load and store instructions access memory, so operands are kept in registers; more registers reduce slow memory accesses.', '1 mark each [2]'),
    ('Explain how interrupts are handled in a pipelined processor.', 'Instructions in the pipeline may be allowed to complete or are flushed; register contents are saved; the ISR is loaded into the pipeline; after the ISR the pipeline restarts from the saved PC.', '1 mark per point, max 3 [3]'),
])


@t4_1.add('C3', (1, 2, 3, 4, 5))
def t4_1_pipe(r, D):
    k = r.choice([3, 4, 5, 6])
    n = r.choice([4, 5, 6, 8, 10, 12, 20, 50, 100])
    ns = r.choice([1, 2, 5])
    seq = n * k
    pipe = k + n - 1
    if D == 1:
        return MCQ(r, f'A {k}-stage pipeline executes {n} instructions, with each stage taking one clock cycle and no hazards. How many clock cycles are needed?', str(pipe), [str(seq), str(n), str(k * (n - 1)), str(pipe + 1)], f'k + n − 1 = {k} + {n} − 1 = {pipe}.')
    stem = f'A processor has a {k}-stage pipeline; each stage takes {ns} ns. Calculate the time to execute {n} instructions without pipelining and with pipelining (no hazards).'
    m = 3
    key = f'Without: {n} × {k} × {ns} = {seq * ns} ns [1]; with: ({k} + {n} − 1) × {ns} = {pipe * ns} ns [2] [3]'
    ans = f'{seq * ns} ns; {pipe * ns} ns'
    if D >= 4:
        stem += ' Then calculate the speed-up.'
        ans += f'; speed-up {seq / pipe:.2f}'
        key = key.replace(' [3]', f'; speed-up {seq * ns} ÷ {pipe * ns} = {seq / pipe:.2f} [1] [4]')
        m = 4
    return Q(stem, ans, key, marks=m)


@t4_1.add('C3', (2, 3, 4))
def t4_1_table(r, D):
    stages = ['IF', 'ID', 'EX', 'MA', 'WB'][:r.choice([3, 4, 5])]
    n = r.randrange(3, 6)
    c = r.randrange(1, len(stages) + n - 1)
    active = [(i + 1, stages[c - 1 - i]) for i in range(n) if 0 <= c - 1 - i < len(stages)]
    stem = f'A pipeline has the stages {", ".join(stages)} and executes instructions 1 to {n}, one new instruction entering each clock cycle. State which instruction is in each stage during clock cycle {c}.'
    ans = '; '.join(f'{s}: instruction {i}' for i, s in active)
    return Q(stem, ans, f'In cycle {c}, instruction i is in stage number {c} − i + 1: {ans} [{len(active)}]', marks=len(active))


scen(t4_1, 'C4', (3, 4, 5), [
    '{p} works for a company in {city} that designs processors for smartphones.', '{p} is comparing a RISC processor with a CISC processor for a laptop developed in {city}.',
], [('Compare RISC and CISC in terms of instruction set and clock cycles per instruction.', 'RISC: few simple fixed-length instructions, ~1 cycle each; CISC: many complex variable-length instructions, several cycles.', '1 mark each comparison, max 3 [3]'),
    ('Explain why RISC processors are often used in smartphones.', 'Simpler circuits use less power and generate less heat; good performance per watt.', '1 mark each [2]'),
    ('Explain how pipelining improves performance.', 'Different stages of several instructions run at once, so one instruction completes per cycle once the pipeline is full.', '1 mark each [2]'),
    ('Explain why a CISC program may need fewer instructions than a RISC program for the same task.', 'Each CISC instruction can do more work (e.g. memory operands, complex operations).', '1 mark each [2]')], k=(3, 4))

t4_2 = topic('Parallel processing: SISD, SIMD, MISD and MIMD; massively parallel computers', 'parallel processing', 'sisd, simd, misd and mimd', 'massively parallel')
FLYNN = [('SISD', 'one processor executes a single stream of instructions on a single stream of data', 'an early single-core personal computer'),
         ('SIMD', 'many processors execute the same instruction on different data at the same time', 'a graphics card changing the brightness of every pixel'),
         ('MISD', 'several processors execute different instructions on the same data', 'fault-tolerant systems such as flight control, where results are compared'),
         ('MIMD', 'several processors execute different instructions on different data independently', 'a modern multi-core processor running several programs')]
t4_2.fixed('C1', (1, 2), [(f'Which describes {n}?', d[0].upper() + d[1:], f'{n}: {d}; e.g. {e}.', [x[1][0].upper() + x[1][1:] for x in FLYNN if x[0] != n]) for n, d, e in FLYNN] + [
    ('What is a massively parallel computer?', 'A computer with a very large number of processors working together on one task, linked by a network', 'e.g. supercomputers with thousands of nodes.', ['A computer with a very fast single processor', 'A computer with a very large hard disk', 'A computer used by many users at once']),
])
t4_2.fixed('C2', (2, 3, 4), [
    ('Explain why software must be specially written to benefit from parallel processing.', 'The task must be split into parts that can run at the same time, and the results combined; sequential code runs on one processor only.', '1 mark each [2]'),
    ('Explain why SIMD is suitable for processing images.', 'The same operation is applied to every pixel; many pixels are processed at once by different processing units.', '1 mark each [2]'),
])


@t4_2.add('C3', (1, 2, 3, 4))
def t4_2_pick(r, D):
    n, dsc, ex = r.choice(FLYNN)
    if D <= 2:
        return MCQ(r, f'Which classification best describes {ex}?', n, [x[0] for x in FLYNN if x[0] != n], f'{n}: {dsc}.')
    return Q(f'Identify the Flynn classification of {ex} and explain your answer.', f'{n}: {dsc}.', '1 mark classification; 1 mark explanation [2]', marks=2)


@t4_2.add('C3', (2, 3, 4, 5), 'numerical')
def t4_2_speed(r, D):
    t = r.choice([60, 120, 240, 600, 1200])
    p = r.choice([2, 4, 8, 10, 20])
    s = r.choice([10, 20, 25, 50])
    seq = t * s / 100
    par = t * (100 - s) / 100 / p
    tot = seq + par
    return Q(f'A task takes {t} s on one processor. {s}% of the task must run sequentially and the rest can be shared equally between {p} processors. Calculate the time taken on {p} processors and the speed-up.',
             f'{tot:g} s; speed-up {t / tot:.2f}', f'sequential part {seq:g} s [1]; parallel part {t * (100 - s) / 100:g} ÷ {p} = {par:g} s [1]; total {tot:g} s, speed-up {t} ÷ {tot:g} = {t / tot:.2f} [1] [3]', marks=3)


scen(t4_2, 'C4', (3, 4, 5), [
    'A weather forecasting centre in {city} uses a massively parallel computer.', '{org} is choosing hardware for rendering animated films.',
], [('Explain why a massively parallel computer is suitable for this task.', 'The task can be split into many independent parts (grid cells/frames) processed simultaneously, reducing time.', '1 mark each [2]'),
    ('Describe two problems in using massively parallel systems.', 'Software must be written to divide the task; communication between processors; cost; power/cooling.', '1 mark each [2]'),
    ('Identify the classification of a GPU and explain it.', 'SIMD: same instruction on many data items at once.', '1 mark each [2]'),
    ('Explain why adding more processors gives diminishing returns.', 'Sequential parts cannot be parallelised and communication overhead increases.', '1 mark each [2]')], k=(2, 3))

t4_3 = topic('Virtual machines: concept, examples and benefits and limitations', 'virtual machines')
t4_3.fixed('C1', (1, 2), [
    ('What is a virtual machine?', 'Software that emulates a complete computer system, allowing one operating system to run inside another', 'The host OS runs a hypervisor; guest OSs run in VMs.', ['A computer with no hardware', 'A computer with two processors', 'A program that removes viruses']),
    ('Which is an example of a process virtual machine?', 'The Java Virtual Machine running bytecode', 'Process VMs run a single program (e.g. JVM); system VMs run a full OS.', ['A USB flash drive', 'A web browser cache', 'A RAID array']),
    ('What is the guest operating system?', 'The operating system running inside the virtual machine', 'The host OS runs on the real hardware.', ['The OS on the physical hardware', 'The hypervisor', 'The BIOS']),
    ('What is the role of a hypervisor?', 'To create and manage virtual machines and allocate hardware resources to them', 'Hypervisor (virtual machine monitor).', ['To compile programs', 'To encrypt network traffic', 'To act as a firewall']),
])
t4_3.fixed('C2', (2, 3, 4), [
    ('Explain two benefits of using virtual machines.', 'Several OSs on one computer; legacy software can be run; testing in isolation without risk to the host; easy back-up/cloning of whole systems; better use of server hardware.', '1 mark per benefit, max 2 [2]'),
    ('Explain two limitations of virtual machines.', 'Slower than running on real hardware because of emulation overhead; need significant memory/processing; some hardware cannot be emulated fully.', '1 mark per limitation, max 2 [2]'),
])
scen(t4_3, 'C2', (2, 3, 4), [
    '{org} in {city} needs to keep running an old accounting program that only works on an obsolete operating system.', '{p} is a software tester at {org} who must test an app on several operating systems.',
    '{org} has ten lightly used servers and wants to reduce costs.',
], [('Explain how a virtual machine would help in this situation.', 'A VM can run the required (guest) OS on current hardware, isolated from the host.', '1 mark each [2]'),
    ('Describe one limitation of using a virtual machine here.', 'Performance overhead; needs more RAM/CPU; possible hardware compatibility issues.', '1 mark each [2]'),
    ('Explain the roles of the host OS and the guest OS.', 'Host OS runs on the real hardware and runs the hypervisor; guest OS runs inside the VM using virtual hardware.', '1 mark each [2]'),
    ('Explain why VMs are useful for testing software that may contain malware.', 'The VM is isolated, so any damage is contained and the VM can be reset.', '1 mark each [2]')], k=(2, 3))
essay(t4_3, [('the use of virtual machines by {org} to replace several physical servers', 'better use of hardware; lower power, space and cost; easy backups and migration; isolation between services.',
              'single physical failure affects many VMs; performance overhead; licensing and expertise costs; resource contention.', 'virtualisation is usually beneficial with redundancy and monitoring in place.')],
      ['{org} in {city} is reviewing its data centre.', '{p} is the IT manager at {org}.'])

CHAPTERS[4] = [t4_1, t4_2, t4_3]

# =============================================================================== Chapter 5 Boolean algebra and logic circuits
BAR = '̅'


def lit(v, val):
    return v if val else v + BAR


def minterms_of(outs):
    return [i for i, o in enumerate(outs) if o]


def prime_implicants(mins, n):
    terms = {tuple((m >> (n - 1 - k)) & 1 for k in range(n)) for m in mins}
    primes = set()
    cur = set(terms)
    while cur:
        nxt, used = set(), set()
        cl = list(cur)
        for a, c in itertools.combinations(cl, 2):
            diff = [i for i in range(n) if a[i] != c[i]]
            if len(diff) == 1 and a[diff[0]] != '-' and c[diff[0]] != '-':
                t = list(a)
                t[diff[0]] = '-'
                nxt.add(tuple(t))
                used.add(a)
                used.add(c)
        primes |= (cur - used)
        cur = nxt
    return primes


def covers(t, m, n):
    bits = tuple((m >> (n - 1 - k)) & 1 for k in range(n))
    return all(x == '-' or x == y for x, y in zip(t, bits))


def min_sop(outs, vs):
    n = len(vs)
    mins = minterms_of(outs)
    if not mins:
        return '0', []
    if len(mins) == 1 << n:
        return '1', []
    pis = list(prime_implicants(mins, n))
    best = None
    for k in range(1, len(pis) + 1):
        for combo in itertools.combinations(pis, k):
            if all(any(covers(t, m, n) for t in combo) for m in mins):
                cost = sum(sum(1 for x in t if x != '-') for t in combo)
                if best is None or cost < best[0]:
                    best = (cost, combo)
        if best:
            break
    terms = sorted(best[1], key=lambda t: [('0', '1', '-').index(str(x)) if x != '-' else 2 for x in t])
    return ' + '.join(term_str(t, vs) for t in terms), terms


def term_str(t, vs):
    parts = [lit(v, x) for v, x in zip(vs, t) if x != '-']
    return '.'.join(parts) if parts else '1'


def canon_sop(outs, vs):
    n = len(vs)
    return ' + '.join('.'.join(lit(v, (m >> (n - 1 - k)) & 1) for k, v in enumerate(vs)) for m in minterms_of(outs))


def alg_str(e):
    """Boolean algebra notation: . for AND, + for OR, overbar for NOT of a variable."""
    if e[0] == 'V':
        return e[1]
    if e[0] == 'NOT':
        if e[1][0] == 'V':
            return e[1][1] + BAR
        return 'NOT(' + alg_str(e[1]) + ')'
    op = {'AND': '.', 'OR': ' + '}.get(e[0])
    a, c = alg_str(e[1]), alg_str(e[2])
    if op is None:
        return f'({a}) {e[0]} ({c})'
    if e[0] == 'AND':
        a = f'({a})' if e[1][0] == 'OR' else a
        c = f'({c})' if e[2][0] == 'OR' else c
    return a + op + c


LAWS = [('{A} + {A}.{B}', '{A}', 'absorption: A + A.B = A(1 + B) = A'), ('{A}.({A} + {B})', '{A}', 'absorption: A.(A + B) = A'),
        ('{A} + {Ab}.{B}', '{A} + {B}', 'A + A̅.B = (A + A̅).(A + B) = A + B'), ('{A}.{B} + {A}.{Bb}', '{A}', 'A.(B + B̅) = A.1 = A'),
        ('({A} + {B}).({A} + {Bb})', '{A}', 'A + B.B̅ = A + 0 = A'), ('{A}.{Ab} + {B}', '{B}', 'A.A̅ = 0, so 0 + B = B'),
        ('{A}.{B} + {A}.{B}.{C}', '{A}.{B}', 'absorption: A.B(1 + C) = A.B'), ('{Ab}.{Bb} + {Ab}.{B}', '{Ab}', 'A̅.(B̅ + B) = A̅'),
        ('{A}.{B} + {Ab}.{C} + {B}.{C}', '{A}.{B} + {Ab}.{C}', 'consensus theorem: the B.C term is redundant'), ('({A} + {B}).({Ab} + {B})', '{B}', 'B + A.A̅ = B'),
        ('{A} + {A}', '{A}', 'idempotent law'), ('{A}.1 + {B}.0', '{A}', 'identity and null laws'),
        ('NOT({A}.{B})', '{Ab} + {Bb}', "De Morgan's law"), ('NOT({A} + {B})', '{Ab}.{Bb}', "De Morgan's law"),
        ('NOT({Ab} + {Bb})', '{A}.{B}', "De Morgan's law then double negation"), ('NOT({Ab}.{Bb})', '{A} + {B}', "De Morgan's law then double negation")]


def law_item(r):
    v = r.sample(['A', 'B', 'C', 'P', 'Q', 'R', 'X', 'Y'], 3)
    lhs, rhs, why = r.choice(LAWS)
    sub = {'A': v[0], 'B': v[1], 'C': v[2], 'Ab': v[0] + BAR, 'Bb': v[1] + BAR}
    return fill(lhs, sub), fill(rhs, sub), why


t5_1 = topic("Boolean algebra: De Morgan's laws and simplifying expressions", 'boolean algebra', "de morgan's laws", 'simplifying expressions')
t5_1.fixed('C1', (1, 2, 3), [
    ("Which expression is equivalent to NOT(A.B) by De Morgan's law?", 'A̅ + B̅', 'Break the bar and change the operator: NOT(A.B) = A̅ + B̅.', ['A̅.B̅', 'A + B', 'A.B']),
    ("Which expression is equivalent to NOT(A + B) by De Morgan's law?", 'A̅.B̅', 'NOT(A + B) = A̅.B̅.', ['A̅ + B̅', 'A.B', 'A + B']),
    ('What is A + 1 equal to?', '1', 'Null (annulment) law for OR.', ['A', '0', 'A̅']),
    ('What is A.A̅ equal to?', '0', 'Complement law: A AND NOT A is always 0.', ['1', 'A', 'A̅']),
    ('What is A + A̅ equal to?', '1', 'Complement law: A OR NOT A is always 1.', ['0', 'A', 'A̅']),
    ('What is A + A.B equal to?', 'A', 'Absorption: A(1 + B) = A.', ['A.B', 'B', 'A + B']),
    ('What is the double complement of A equal to?', 'A', 'Double negation: NOT(NOT A) = A.', ['A̅', '0', '1']),
])
t5_1.fixed('C2', (2, 3, 4), [
    ('Explain why simplifying a Boolean expression is useful when designing a circuit.', 'A simpler expression needs fewer gates, so the circuit is cheaper, uses less power, produces less heat and is faster.', '1 mark per point, max 2 [2]'),
    ("Explain how De Morgan's laws allow a circuit to be built using only NAND gates.", "De Morgan's laws convert ORs into NAND form (A + B = NOT(A̅.B̅)), so any sum-of-products can be written as NANDs of NANDs.", '1 mark each [2]'),
])


@t5_1.add('C3', (1, 2, 3, 4, 5))
def t5_1_law(r, D):
    lhs, rhs, why = law_item(r)
    if D <= 2:
        a, c = rhs.split(' + ')[0] if ' + ' in rhs else rhs, 'x'
        wrong = [lhs.replace('.', ' + ', 1) if '.' in lhs else lhs + '.1', '0', '1', rhs + BAR if len(rhs) == 1 else rhs.replace(' + ', '.')]
        return MCQ(r, f'Which expression is equivalent to {lhs}?', rhs, wrong, f'{why}.')
    return Q(f'Simplify the Boolean expression {lhs}, stating the law(s) used.', rhs, f'{why} [1]; answer {rhs} [1] [2]', marks=2)


@t5_1.add('C3', (3, 4, 5), 'numerical')
def t5_1_simplify(r, D):
    vs = ['A', 'B', 'C']
    for _ in range(30):
        e = lg_rand(r, vs, 3 if D <= 3 else 4, ops=('AND', 'OR'))
        outs = lg_table(e, vs)
        s, terms = min_sop(outs, vs)
        if s not in ('0', '1') and len(alg_str(e)) > len(s) + 2:
            break
    else:
        return None
    return Q(f'Simplify the Boolean expression {alg_str(e)} as far as possible, showing your working.', s,
             f'Truth table outputs {"".join(map(str, outs))}; laws such as absorption, distribution and complement give {s}. 1 mark per correct simplification step, 1 mark final answer [3]', marks=3)


@t5_1.add('C4', (3, 4, 5), 'multi_step')
def t5_1_prove(r, D):
    lhs, rhs, why = law_item(r)
    vs = sorted(set(re.findall(r'[A-Z]', lhs)))
    d = ctx(r)
    stem = (f'{d["p"]} claims that the expression {lhs} can be replaced by {rhs} in a circuit for {d["org"]}. (a) Use Boolean algebra to show whether this is correct. (b) Verify your answer with a truth table for the inputs {", ".join(vs)}. '
            f'(c) State how many gates are saved, counting each AND, OR and NOT as one gate.')
    g1 = lhs.count('.') + lhs.count('+') + lhs.count(BAR) + lhs.count('NOT')
    g2 = rhs.count('.') + rhs.count('+') + rhs.count(BAR) + rhs.count('NOT')
    return Q(stem, f'(a) Correct: {why} (b) both expressions give the same output in every row (c) {g1} − {g2} = {g1 - g2} gates saved',
             f'(a) law applied [2] (b) table with all rows [2] (c) {g1 - g2} [1]', marks=5, typ='multi_step')


@t5_1.add('C2', (2, 3, 4), 'explain')
def t5_1_err(r, D):
    v = r.sample(['A', 'B', 'P', 'Q', 'X', 'Y'], 2)
    kind = r.choice(['and', 'or'])
    d = ctx(r)
    if kind == 'and':
        wrong, right = f'{v[0]}{BAR}.{v[1]}{BAR}', f'{v[0]}{BAR} + {v[1]}{BAR}'
        lhs = f'NOT({v[0]}.{v[1]})'
    else:
        wrong, right = f'{v[0]}{BAR} + {v[1]}{BAR}', f'{v[0]}{BAR}.{v[1]}{BAR}'
        lhs = f'NOT({v[0]} + {v[1]})'
    return Q(f"{d['p']} applies De Morgan's law and writes {lhs} = {wrong}. Explain the error and give the correct result.",
             f"When the bar is broken the operator must also change ({'AND to OR' if kind == 'and' else 'OR to AND'}): {lhs} = {right}.", '1 mark: operator must change; 1 mark: correct expression [2]')


t5_2 = topic('Karnaugh maps: sum-of-products form and simplification', 'karnaugh maps', 'sum-of-products')
t5_2.fixed('C1', (1, 2, 3), [
    ('In a Karnaugh map, why are the rows and columns labelled in Gray code order (00, 01, 11, 10)?', 'So that adjacent cells differ by only one variable', 'This allows neighbouring 1s to be grouped and a variable eliminated.', ['To make the map symmetrical', 'Because binary order is not allowed', 'To reduce the number of cells']),
    ('Which group sizes are allowed in a Karnaugh map?', 'Powers of 2: 1, 2, 4, 8, ...', 'Groups must be rectangles of 1, 2, 4, 8 or 16 cells.', ['Any number of cells', 'Only pairs', 'Multiples of 3']),
    ('A group of four 1s in a 3-variable K-map eliminates how many variables?', '2', 'A group of 2ⁿ cells eliminates n variables.', ['1', '3', '4']),
    ('What is a minterm?', 'A product (AND) term containing every input variable, for which the output is 1', 'Sum-of-products is an OR of minterms.', ['A sum term containing every variable', 'A group of 1s in a K-map', 'The smallest gate in a circuit']),
    ('Can a K-map group wrap around the edges of the map?', 'Yes, the edges are adjacent', 'The map is treated as wrapping left-right and top-bottom.', ['No, never', 'Only for 2-variable maps', 'Only diagonally']),
])
t5_2.fixed('C2', (2, 3, 4), [
    ('Explain why groups in a K-map should be as large as possible.', 'Each larger group eliminates more variables, giving shorter product terms and a simpler expression.', '1 mark each [2]'),
    ('Explain why a cell may be included in more than one group.', 'Overlapping lets each group be as large as possible, which simplifies the expression; every 1 must be covered at least once.', '1 mark each [2]'),
])


def _kfunc(r, D):
    vs = ['A', 'B', 'C'] if D <= 3 else ['A', 'B', 'C', 'D']
    n = len(vs)
    for _ in range(40):
        k = r.randrange(2, (1 << n) - 2)
        mins = sorted(r.sample(range(1 << n), k))
        outs = [1 if i in mins else 0 for i in range(1 << n)]
        s, terms = min_sop(outs, vs)
        if s not in ('0', '1') and len(terms) <= 4:
            return vs, outs, s, terms
    return None


@t5_2.add('C3', (1, 2, 3, 4, 5))
def t5_2_kmap(r, D):
    x = _kfunc(r, D)
    if not x:
        return None
    vs, outs, s, terms = x
    rows = ', '.join(f'{format(i, "0" + str(len(vs)) + "b")}→{o}' for i, o in enumerate(outs))
    if D == 1:
        return MCQ(r, f'A function of {", ".join(vs)} has the truth table {rows}. How many 1s must be placed in its Karnaugh map?', str(sum(outs)), [str(sum(outs) + 1), str(len(outs) - sum(outs)), str(len(terms))], f'One 1 per row with output 1: {sum(outs)}.')
    stem = f'A logic function of {", ".join(vs)} has the truth table ({"".join(vs)}→X): {rows}. Use a Karnaugh map to find the simplified sum-of-products expression.'
    m = 3 if len(vs) == 3 else 4
    return Q(stem, f'X = {s}', f'K-map filled correctly [1]; groups: {"; ".join(term_str(t, vs) for t in terms)} [{m - 2}]; X = {s} [1] [{m}]', marks=m)


@t5_2.add('C3', (2, 3, 4), 'numerical')
def t5_2_canon(r, D):
    x = _kfunc(r, 3)
    if not x:
        return None
    vs, outs, s, terms = x
    rows = ', '.join(f'{format(i, "03b")}→{o}' for i, o in enumerate(outs))
    return Q(f'Write the sum-of-products expression for the truth table ({"".join(vs)}→X): {rows}.', f'X = {canon_sop(outs, vs)}', f'one minterm per row with X = 1 [{min(3, sum(outs))}]', marks=min(3, sum(outs)))


@t5_2.add('C4', (3, 4, 5), 'multi_step')
def t5_2_full(r, D):
    vs = ['A', 'B', 'C'] if D <= 3 else ['A', 'B', 'C', 'D']
    for _ in range(30):
        e = lg_rand(r, vs, len(vs) + 1, ops=('AND', 'OR', 'XOR', 'NAND', 'NOR'))
        outs = lg_table(e, vs)
        s, terms = min_sop(outs, vs)
        if s not in ('0', '1') and ('.' in s or '+' in s):
            break
    else:
        return None
    d = ctx(r)
    stem = (f'A control circuit at {d["org"]} has output X = {lg_str(e)}. (a) Complete the truth table for {"".join(vs)} = 0…0 to 1…1. (b) Write the sum-of-products expression. '
            f'(c) Use a Karnaugh map to simplify the expression. (d) State the number of 2-input AND/OR gates and NOT gates needed for your simplified expression.')
    nots = len({v for t in terms for v, x in zip(vs, t) if x == 0})
    ands = sum(max(0, sum(1 for x_ in t if x_ != '-') - 1) for t in terms)
    ors = len(terms) - 1
    return Q(stem, f'(a) {"".join(map(str, outs))} (b) X = {canon_sop(outs, vs)} (c) X = {s} (d) {ands} AND, {ors} OR, {nots} NOT',
             f'(a) [2] (b) [1] (c) correct groups [2]; X = {s} [1] (d) [1]', marks=7, typ='multi_step')


t5_3 = topic('Half adder, full adder and SR and JK flip-flops', 'half adder', 'full adder', 'flip-flops')
t5_3.fixed('C1', (1, 2), [
    ('Which gates make a half adder?', 'An XOR gate for the sum and an AND gate for the carry', 'S = A XOR B; C = A AND B.', ['Two OR gates', 'A NAND and a NOR gate', 'An AND gate for the sum and an XOR gate for the carry']),
    ('How many inputs does a full adder have?', '3', 'A, B and carry-in; outputs sum and carry-out.', ['2', '4', '1']),
    ('What is a flip-flop used for?', 'To store one bit of data', 'Flip-flops are bistable circuits used in registers and memory (SRAM).', ['To add two bits', 'To convert analogue to digital', 'To amplify a signal']),
    ('In an SR flip-flop built from NOR gates, which input combination is invalid?', 'S = 1, R = 1', 'Both outputs would be forced to 0, so Q and Q̅ are not complementary.', ['S = 0, R = 0', 'S = 1, R = 0', 'S = 0, R = 1']),
    ('In a JK flip-flop, what happens when J = 1 and K = 1 on a clock pulse?', 'The output toggles', 'JK: 00 hold, 01 reset, 10 set, 11 toggle.', ['The output is invalid', 'The output is reset to 0', 'The output is set to 1']),
    ('Why is the JK flip-flop an improvement on the SR flip-flop?', 'It has no invalid input state and is clocked', 'J = K = 1 toggles instead of being invalid; the clock synchronises changes.', ['It stores two bits', 'It needs no power', 'It has only one input']),
])
t5_3.fixed('C2', (2, 3, 4), [
    ('Explain how full adders can be combined to add two 4-bit numbers.', 'Four full adders are connected in series; the carry-out of each is the carry-in of the next more significant bit (ripple carry adder).', '1 mark each [2]'),
    ('Explain why a flip-flop is described as bistable.', 'It has two stable states (Q = 0 or Q = 1) and stays in one until an input changes it, so it stores a bit.', '1 mark each [2]'),
])


@t5_3.add('C3', (1, 2, 3, 4, 5))
def t5_3_adder(r, D):
    if D <= 2:
        a, c = r.randrange(2), r.randrange(2)
        s, cy = a ^ c, a & c
        if D == 1:
            return MCQ(r, f'A half adder has inputs A = {a} and B = {c}. What are the sum S and carry C?', f'S = {s}, C = {cy}', [f'S = {1 - s}, C = {cy}', f'S = {s}, C = {1 - cy}', f'S = {cy}, C = {s}' if s != cy else f'S = {1 - s}, C = {1 - cy}'], f'S = A XOR B = {s}; C = A AND B = {cy}.')
        return Q(f'A half adder has inputs A = {a} and B = {c}. State the sum S and carry C, and the gates that produce them.', f'S = {s}, C = {cy}; XOR for S, AND for C', f'S = {s} [1]; C = {cy} [1] [2]', marks=2)
    n = 4 if D < 5 else 8
    x, y = r.randrange(1 << (n - 1), 1 << n), r.randrange(1 << (n - 1))
    tot = x + y
    carries = []
    cin = 0
    for i in range(n):
        xb, yb = (x >> i) & 1, (y >> i) & 1
        cout = (xb & yb) | (cin & (xb ^ yb))
        carries.append(cout)
        cin = cout
    stem = f'A {n}-bit ripple carry adder made from full adders adds {b(x, n)} and {b(y, n)}. Give the {n}-bit sum, the final carry-out, and the carry-out of each full adder from the least significant bit.'
    return Q(stem, f'Sum {b(tot % (1 << n), n)}; carry-out {tot >> n}; carries (LSB first) {"".join(map(str, carries))}', f'sum [1]; final carry [1]; carry chain [1] [3]', marks=3)


def sr_seq(r, n):
    q = r.randrange(2)
    seq = []
    out = []
    for _ in range(n):
        s, rr = r.choice([(0, 0), (1, 0), (0, 1)])
        seq.append((s, rr))
        if s == 1:
            q = 1
        elif rr == 1:
            q = 0
        out.append(q)
    return seq, out


def jk_seq(r, n):
    q = r.randrange(2)
    q0 = q
    seq, out = [], []
    for _ in range(n):
        j, k = r.choice([(0, 0), (0, 1), (1, 0), (1, 1)])
        seq.append((j, k))
        if j and k:
            q = 1 - q
        elif j:
            q = 1
        elif k:
            q = 0
        out.append(q)
    return q0, seq, out


@t5_3.add('C3', (2, 3, 4, 5), 'numerical')
def t5_3_ff(r, D):
    n = 4 if D <= 3 else 6
    if r.random() < 0.5:
        seq, out = sr_seq(r, n)
        q0 = 'unknown'
        stem = f'An SR flip-flop (built from NOR gates) receives the inputs (S, R): {", ".join(f"({s}, {x})" for s, x in seq)} in order. Give the value of Q after each input, writing "unchanged" where the input holds the previous state.'
        if seq[0] == (0, 0):
            seq[0] = (1, 0)
            out[0] = 1
            q = 1
            for i in range(1, n):
                s, x = seq[i]
                q = 1 if s else (0 if x else q)
                out[i] = q
            stem = f'An SR flip-flop (built from NOR gates) receives the inputs (S, R): {", ".join(f"({s}, {x})" for s, x in seq)} in order. Give the value of Q after each input.'
        return Q(stem, ', '.join(map(str, out)), 'S = 1 sets Q to 1, R = 1 resets Q to 0, S = R = 0 holds: ' + ', '.join(map(str, out)) + f' [{(n + 1) // 2}]', marks=(n + 1) // 2)
    q0, seq, out = jk_seq(r, n)
    stem = f'A JK flip-flop has Q = {q0}. On successive clock pulses its inputs (J, K) are {", ".join(f"({j}, {k})" for j, k in seq)}. Give Q after each clock pulse.'
    return Q(stem, ', '.join(map(str, out)), 'JK: 00 hold, 01 reset, 10 set, 11 toggle: ' + ', '.join(map(str, out)) + f' [{(n + 1) // 2}]', marks=(n + 1) // 2)


scen(t5_3, 'C4', (3, 4, 5), [
    '{org} is designing an arithmetic unit and a register for a simple processor.', '{p} is building digital circuits for a student project at {org}.',
], [('Draw (describe) a half adder and give its truth table.', 'XOR gate gives S, AND gate gives C; truth table AB 00→S0 C0, 01→1 0, 10→1 0, 11→0 1.', '1 mark gates; 1 mark truth table [2]'),
    ('Explain how a full adder can be built from two half adders.', 'First half adder adds A and B; second adds the sum to carry-in; the two carries are ORed to give carry-out.', '1 mark per point [3]'),
    ('Explain why flip-flops are used to build registers.', 'Each flip-flop stores one bit; n flip-flops clocked together store an n-bit value.', '1 mark each [2]'),
    lambda r, d: (lambda x: (f'A JK flip-flop has Q = {x[0]}; the inputs on three clock pulses are ' + ', '.join(f'J = {j}, K = {k}' for j, k in x[1]) + '. Give Q after each pulse.', ', '.join(map(str, x[2])), '1 mark per correct value [3]'))(jk_seq(r, 3))], k=(3, 4))

CHAPTERS[5] = [t5_1, t5_2, t5_3]

# =============================================================================== Chapter 6 System software
PNAMES = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']


def sched(alg, procs, q=2):
    """procs: list of (name, arrival, burst). Returns (gantt [(name, start, end)], completion {name: t})."""
    gantt, comp = [], {}
    if alg == 'FCFS':
        t = 0
        for n, a, bt in sorted(procs, key=lambda x: (x[1], PNAMES.index(x[0]))):
            t = max(t, a)
            gantt.append((n, t, t + bt))
            t += bt
            comp[n] = t
    elif alg == 'SJF':
        t, left = 0, list(procs)
        while left:
            ready = [p for p in left if p[1] <= t] or [min(left, key=lambda x: x[1])]
            t = max(t, min(p[1] for p in ready))
            ready = [p for p in left if p[1] <= t]
            p = min(ready, key=lambda x: (x[2], x[1], PNAMES.index(x[0])))
            gantt.append((p[0], t, t + p[2]))
            t += p[2]
            comp[p[0]] = t
            left.remove(p)
    elif alg == 'RR':
        rem = {n: bt for n, _, bt in procs}
        queue = [n for n, _, _ in procs]
        t = 0
        while queue:
            n = queue.pop(0)
            run = min(q, rem[n])
            if gantt and gantt[-1][0] == n:
                gantt[-1] = (n, gantt[-1][1], t + run)
            else:
                gantt.append((n, t, t + run))
            t += run
            rem[n] -= run
            if rem[n]:
                queue.append(n)
            else:
                comp[n] = t
    elif alg == 'SRTF':
        rem = {n: bt for n, _, bt in procs}
        arr = {n: a for n, a, _ in procs}
        t = 0
        while rem:
            ready = [n for n in rem if arr[n] <= t]
            if not ready:
                t += 1
                continue
            n = min(ready, key=lambda x: (rem[x], arr[x], PNAMES.index(x)))
            if gantt and gantt[-1][0] == n and gantt[-1][2] == t:
                gantt[-1] = (n, gantt[-1][1], t + 1)
            else:
                gantt.append((n, t, t + 1))
            rem[n] -= 1
            t += 1
            if not rem[n]:
                del rem[n]
                comp[n] = t
    return gantt, comp


def gantt_str(g):
    return ' | '.join(f'{n} {s}–{e}' for n, s, e in g)


ALG_NAME = {'FCFS': 'first come first served (FCFS)', 'SJF': 'shortest job first (SJF, non-pre-emptive)', 'RR': 'round robin', 'SRTF': 'shortest remaining time first (SRTF, pre-emptive)'}

t6_1 = topic('Operating system: maximising resource use, user interface; process states and scheduling algorithms', 'operating system', 'process states', 'scheduling algorithms')
t6_1.fixed('C1', (1, 2), [
    ('A running process requests data from a disk. To which state does it move?', 'Blocked', 'Running → blocked while waiting for an I/O event; blocked → ready when the event completes.', ['Ready', 'Running', 'Terminated']),
    ('A running process uses up its time slice. To which state does it move?', 'Ready', 'Running → ready when interrupted by the scheduler (time slice ends).', ['Blocked', 'Terminated', 'Suspended on disk']),
    ('A blocked process has its I/O operation completed. To which state does it move?', 'Ready', 'Blocked → ready: it cannot go straight to running; it waits to be scheduled.', ['Running', 'Blocked', 'Terminated']),
    ('Which scheduling algorithm can cause starvation of long processes?', 'Shortest job first', 'Short jobs keep being chosen first, so a long job may wait indefinitely.', ['First come first served', 'Round robin', 'None of them']),
    ('Which scheduling algorithm gives each process a fixed time slice in turn?', 'Round robin', 'Each ready process gets a time quantum, then goes to the back of the ready queue.', ['First come first served', 'Shortest job first', 'Shortest remaining time first']),
    ('What is the role of the low-level scheduler?', 'To decide which ready process is given the processor next', 'The high-level scheduler decides which jobs are loaded into memory.', ['To decide which jobs are loaded from backing store into memory', 'To manage the files on a disk', 'To provide the user interface']),
    ('What is an interrupt?', 'A signal to the processor that an event needs attention', 'The current process is suspended, its state saved, and an interrupt service routine runs.', ['A process that has finished', 'A type of scheduling algorithm', 'An error in a program that stops compilation']),
    ('Which is a pre-emptive scheduling algorithm?', 'Round robin', 'Pre-emptive: the OS can take the processor away from a running process (RR, SRTF).', ['First come first served', 'Shortest job first (non-pre-emptive)', 'Batch processing']),
])
t6_1.fixed('C2', (2, 3, 4), [
    ('Explain why a process cannot move directly from the blocked state to the running state.', 'When its I/O completes it must join the ready queue; only the scheduler can move a ready process to running, according to the scheduling algorithm.', '1 mark each [2]'),
    ('Explain how an operating system maximises the use of the processor.', 'Multitasking: while one process waits for I/O (blocked) another ready process is scheduled, so the CPU is rarely idle; interrupts let I/O run without the CPU waiting.', '1 mark per point, max 3 [3]'),
    ('Explain the difference between pre-emptive and non-pre-emptive scheduling.', 'Pre-emptive: the OS can interrupt a running process (time slice/higher priority); non-pre-emptive: a process keeps the CPU until it finishes or blocks.', '1 mark each [2]'),
    ('Explain why a graphical user interface hides the complexity of the hardware from the user.', 'The OS provides icons/windows that the user interacts with; the OS translates these into low-level operations on hardware via drivers, so the user does not need to know how the hardware works.', '1 mark each [2]'),
])
ar(t6_1, [('Round robin scheduling is fair to all processes.', 'Each process receives an equal time slice in turn.'),
          ('Shortest job first gives the lowest average waiting time when all jobs arrive together.', 'Running short jobs first reduces the time that the other jobs spend waiting.'),
          ('A process in the blocked state cannot use the processor.', 'It is waiting for an event such as the completion of an I/O operation.'),
          ('Interrupts allow the processor to do other work during input/output.', 'The device signals the processor only when it needs attention.'),
          ('Shortest job first can lead to starvation.', 'Long jobs may be overtaken repeatedly by newly arriving short jobs.')],
   ['Round robin is a non-pre-emptive algorithm.', 'A process moves from blocked straight to running when its I/O completes.', 'First come first served always gives the shortest average waiting time.',
    'The high-level scheduler decides which ready process uses the processor next.'])


def _procs(r, D, arrivals):
    n = 3 if D <= 2 else (4 if D <= 4 else 5)
    bursts = r.sample(range(2, 13), n)
    arr = [0] * n
    if arrivals:
        arr = sorted([0] + r.sample(range(1, 9), n - 1))
    return [(PNAMES[i], arr[i], bursts[i]) for i in range(n)]


def _ptable(procs, arrivals):
    if arrivals:
        return '; '.join(f'{n}: arrival time {a}, burst time {bt} ms' for n, a, bt in procs)
    return '; '.join(f'{n}: {bt} ms' for n, _, bt in procs)


@t6_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_1_sched(r, D):
    alg = r.choice(['FCFS', 'SJF', 'RR'] + (['SRTF'] if D >= 4 else []))
    arrivals = D >= 4 and alg != 'RR'
    procs = _procs(r, D, arrivals)
    q = r.choice([2, 3, 4])
    g, comp = sched(alg, procs, q)
    wait = {n: comp[n] - a - bt for n, a, bt in procs}
    avg = sum(wait.values()) / len(procs)
    avs = f'{avg:.2f}'.rstrip('0').rstrip('.')
    qs = f' with a time quantum of {q} ms' if alg == 'RR' else ''
    intro = ('The processes below are in the ready queue in the order shown, all arriving at time 0' if not arrivals else 'The processes below arrive at the times shown') + f': {_ptable(procs, arrivals)}.'
    if D == 1:
        return MCQ(r, f'{intro} They are scheduled using {ALG_NAME[alg]}{qs}. What is the average waiting time?', f'{avs} ms',
                   [f'{x:.2f}'.rstrip('0').rstrip('.') + ' ms' for x in (sum(comp.values()) / len(procs), avg + 1, max(avg - 1.5, 0.5), sum(bt for _, _, bt in procs) / len(procs))],
                   'Waiting time = completion − arrival − burst: ' + ', '.join(f'{n} {w}' for n, w in wait.items()) + f'; average {avs} ms.')
    stem = f'{intro} The operating system uses {ALG_NAME[alg]}{qs}. Draw (write) the order in which the processes use the processor with start and end times, and calculate the average waiting time.'
    ans = f'{gantt_str(g)}; waiting times ' + ', '.join(f'{n} = {w}' for n, w in wait.items()) + f'; average = {avs} ms'
    return Q(stem, ans, f'order/timeline correct [2]; waiting time = completion − arrival − burst for each process [1]; average {sum(wait.values())} ÷ {len(procs)} = {avs} ms [1] [4]', marks=4)


@t6_1.add('C3', (2, 3, 4, 5), 'numerical')
def t6_1_compare(r, D):
    procs = _procs(r, max(D, 3), False)
    res = {}
    for alg in ('FCFS', 'SJF'):
        g, comp = sched(alg, procs)
        res[alg] = sum(comp[n] - bt for n, _, bt in procs) / len(procs)
    f = lambda x: f'{x:.2f}'.rstrip('0').rstrip('.')
    return Q(f'Four jobs arrive together in the order {_ptable(procs, False)}. Calculate the average waiting time using FCFS and using SJF, and state which algorithm gives the lower value.'.replace('Four', {3: 'Three', 4: 'Four', 5: 'Five'}[len(procs)]),
             f'FCFS {f(res["FCFS"])} ms; SJF {f(res["SJF"])} ms; ' + ('SJF is lower' if res['SJF'] < res['FCFS'] else 'they are equal (the jobs are already in shortest-first order)'),
             f'FCFS average [1]; SJF average [1]; conclusion [1] [3]', marks=3)


@t6_1.add('C3', (1, 2, 3))
def t6_1_state(r, D):
    ev = [('the process is chosen by the low-level scheduler', 'ready', 'running'), ('the process requests input from the keyboard', 'running', 'blocked'),
          ('the time slice of the process ends', 'running', 'ready'), ('the printer finishes printing data sent by the process', 'blocked', 'ready'),
          ('the process waits for a file to be read from disk', 'running', 'blocked'), ('a higher-priority process becomes ready and pre-empts it', 'running', 'ready'),
          ('the data the process was waiting for arrives from the network', 'blocked', 'ready'), ('the process is dispatched to the processor', 'ready', 'running')]
    e, a, c = r.choice(ev)
    if D <= 2:
        return MCQ(r, f'A process is in the {a} state. Which state does it move to when {e}?', c.capitalize(), [x.capitalize() for x in ['ready', 'running', 'blocked', 'terminated'] if x != c], f'{a} → {c} when {e}.')
    return Q(f'A process is currently {a}. State the new state of the process when {e}, and explain why.', f'{c}: ' + {'running': 'the scheduler has given it the processor', 'blocked': 'it cannot continue until the I/O event happens',
                                                                                                                         'ready': 'it can run again but must wait for the scheduler to allocate the processor'}[c] + '.', '1 mark state; 1 mark reason [2]', marks=2)


scen(t6_1, 'C4', (3, 4, 5), [
    'A multi-user server at {org} in {city} runs many processes at the same time.', '{p} is writing a report on how the operating system on a laptop shares the processor.',
], [('Describe the three main process states.', 'Ready: waiting for the processor; running: being executed; blocked: waiting for an event such as I/O.', '1 mark per state [3]'),
    ('Explain how interrupts are used when a process requests data from a disk.', 'Process is blocked while disk transfers; disk controller sends an interrupt when done; ISR runs; process moves to ready.', '1 mark per point, max 3 [3]'),
    lambda r, d: (lambda pr: (f'Four processes arrive at time 0 with burst times ' + ', '.join(f'{n} {bt} ms' for n, _, bt in pr) + '. Calculate the average waiting time using round robin with a 3 ms time slice.',
                              (lambda g, c: f'{gantt_str(g)}; average waiting = {sum(c[n] - bt for n, _, bt in pr) / 4:g} ms')(*sched('RR', pr, 3)), 'timeline [1]; waiting times [1]; average [1] [3]'))(
        [(PNAMES[i], 0, x) for i, x in enumerate(r.sample(range(2, 11), 4))]),
    ('Explain why round robin is suitable for an interactive multi-user system.', 'Every user process gets the CPU regularly, so response times are short and no process is starved.', '1 mark each [2]'),
    ('Describe two ways the operating system maximises the use of resources other than the processor.', 'Memory management allocates/frees memory and uses virtual memory; spooling/buffering for printers; device drivers and I/O scheduling.', '1 mark each [2]')], k=(3, 4))
essay(t6_1, [('the choice of scheduling algorithm for {org}\'s server, comparing round robin, shortest job first and first come first served', 'RR gives fair, quick response for interactive users; SJF minimises average waiting time; FCFS simple with low overhead.',
              'RR has context-switch overhead and depends on quantum size; SJF needs burst times known and may starve long jobs; FCFS gives long waits behind long jobs (convoy effect).', 'a pre-emptive algorithm such as RR (or multilevel feedback) suits mixed interactive workloads.')],
      ['{org} in {city} runs a shared server used by staff and by overnight batch jobs.', '{p} is advising {org} on operating system configuration.'])

t6_2 = topic('Memory management: paging, segmentation, virtual memory and disk thrashing', 'memory management', 'paging', 'segmentation', 'virtual memory', 'disk thrashing')
t6_2.fixed('C1', (1, 2), [
    ('In paging, how is memory divided?', 'Into fixed-size blocks: pages in logical memory and page frames in physical memory', 'Pages are all the same size; segments vary.', ['Into variable-size blocks based on program modules', 'Into one block per user', 'Into sectors and tracks']),
    ('How is memory divided in segmentation?', 'Into variable-size blocks that match logical parts of a program', 'e.g. a segment for code, data, stack.', ['Into fixed-size blocks', 'Into equal frames', 'Into tracks on a disk']),
    ('What is virtual memory?', 'Using part of secondary storage as if it were main memory', 'Pages not in use are swapped out to disk; only needed pages are kept in RAM.', ['Memory inside the CPU', 'Memory that is not used', 'A type of ROM']),
    ('What is disk thrashing?', 'When pages are swapped between RAM and disk so often that little useful processing is done', 'Caused by too many processes/too little RAM; constant page faults.', ['When a hard disk is physically damaged', 'When a disk is defragmented', 'When files are deleted']),
    ('What does a page table store?', 'Which page frame in physical memory holds each page of a process', 'Also flags such as present/absent and dirty bits.', ['The size of every file', 'The process states', 'The list of users']),
    ('What is a page fault?', 'An attempt to access a page that is not currently in main memory', 'The OS must load the page from disk, possibly replacing another page.', ['A hardware failure in RAM', 'A page that contains an error', 'A page that is too large']),
])
t6_2.fixed('C2', (2, 3, 4), [
    ('Explain the difference between paging and segmentation.', 'Pages are fixed-size physical divisions; segments are variable-size logical divisions of the program (e.g. procedures); paging can cause internal fragmentation, segmentation external fragmentation.', '1 mark per point, max 3 [3]'),
    ('Explain how virtual memory allows a program larger than RAM to run.', 'Only the pages currently needed are loaded into RAM; others are kept on disk and swapped in when required (on a page fault).', '1 mark each [2]'),
    ('Explain how disk thrashing can be reduced.', 'Install more RAM; run fewer programs at once; use a better page replacement algorithm; reduce paging by increasing frame allocation.', '1 mark per point, max 2 [2]'),
])
ar(t6_2, [('Virtual memory lets a computer run programs bigger than its RAM.', 'Pages not currently in use are stored on secondary storage.'),
          ('Paging can waste some memory in the last page of a process.', 'Pages are of fixed size, so the final page is rarely full.'),
          ('Disk thrashing slows a computer down.', 'Accessing secondary storage is much slower than accessing RAM.'),
          ('Segmentation divides a program into logical units.', 'Segments are variable in size and match parts such as procedures or data areas.')],
   ['Pages are of variable size.', 'Virtual memory is faster than RAM.', 'A page fault means that the RAM is faulty.', 'Segments must all be the same size.'])


@t6_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_2_addr(r, D):
    ps = r.choice([256, 512, 1024, 2048, 4096])
    npages = r.randrange(4, 8)
    frames = r.sample(range(2, 20), npages)
    p = r.randrange(npages)
    off = r.randrange(ps)
    la = p * ps + off
    pa = frames[p] * ps + off
    table = ', '.join(f'page {i} → frame {f}' for i, f in enumerate(frames))
    if D == 1:
        return MCQ(r, f'A system uses pages of {ps} bytes. What is the page number of logical address {la}?', str(p), [str(p + 1), str(off), str(max(p - 1, frames[p])), str(la % 10)], f'Page = {la} DIV {ps} = {p}; offset = {la} MOD {ps} = {off}.')
    if D == 2:
        return Q(f'A system uses pages of {ps} bytes. Calculate the page number and the offset of logical address {la}.', f'page {p}, offset {off}', f'page = {la} DIV {ps} = {p} [1]; offset = {la} MOD {ps} = {off} [1] [2]', marks=2)
    return Q(f'A process uses pages of {ps} bytes. Its page table is: {table}. Calculate the physical address of logical address {la}, showing your working.', str(pa),
             f'page = {la} DIV {ps} = {p}, offset = {off} [1]; frame {frames[p]} [1]; physical = {frames[p]} × {ps} + {off} = {pa} [1] [3]', marks=3)


@t6_2.add('C3', (2, 3, 4, 5), 'numerical')
def t6_2_frag(r, D):
    ps = r.choice([1024, 2048, 4096])
    size = r.randrange(3 * ps + 1, 12 * ps)
    if size % ps == 0:
        size += 37
    n = -(-size // ps)
    waste = n * ps - size
    unit = 'bytes'
    return Q(f'A program of {size} {unit} is loaded into memory that uses pages of {ps} bytes. Calculate the number of pages needed and the internal fragmentation.', f'{n} pages; {waste} bytes unused',
             f'{size} ÷ {ps} = {size / ps:.2f} → {n} pages (round up) [1]; {n} × {ps} − {size} = {waste} bytes [1] [2]', marks=2)


def page_faults(refs, nf, alg):
    mem, faults, hist = [], 0, []
    last = {}
    for i, p in enumerate(refs):
        if p in mem:
            last[p] = i
            hist.append(None)
            continue
        faults += 1
        if len(mem) < nf:
            mem.append(p)
            hist.append(None)
        else:
            if alg == 'FIFO':
                v = mem.pop(0)
            else:
                v = min(mem, key=lambda x: last[x])
                mem.remove(v)
            mem.append(p)
            hist.append(v)
        last[p] = i
    return faults, hist


@t6_2.add('C3', (3, 4, 5), 'numerical')
def t6_2_replace(r, D):
    n = 10 if D == 3 else 12
    refs = [r.randrange(1, 6) for _ in range(n)]
    for i in range(1, n):
        if refs[i] == refs[i - 1]:
            refs[i] = refs[i] % 5 + 1
    nf = 3
    alg = r.choice(['FIFO', 'LRU'])
    f, hist = page_faults(refs, nf, alg)
    other = page_faults(refs, nf, 'LRU' if alg == 'FIFO' else 'FIFO')[0]
    nm = {'FIFO': 'first in first out (FIFO)', 'LRU': 'least recently used (LRU)'}[alg]
    ev = [f'{p} replaces {v}' for p, v in zip(refs, hist) if v is not None]
    stem = f'A process has 3 page frames, initially empty. It accesses pages in the order {", ".join(map(str, refs))}. Using the {nm} page replacement algorithm, state the number of page faults.'
    if D == 5:
        stem += f' Compare your answer with the {"LRU" if alg == "FIFO" else "FIFO"} algorithm.'
        return Q(stem, f'{alg}: {f} page faults; {"LRU" if alg == "FIFO" else "FIFO"}: {other}', f'replacements: {"; ".join(ev)} [2]; {f} faults [1]; other algorithm {other} [1] [4]', marks=4)
    return Q(stem, f'{f} page faults', f'first 3 distinct pages fault; replacements: {"; ".join(ev) or "none"} [2]; total {f} [1] [3]', marks=3)


scen(t6_2, 'C2', (2, 3, 4), [
    '{p} notices that a laptop with 4 GiB of RAM becomes very slow when many browser tabs are open.', 'A server at {org} in {city} uses virtual memory.',
], [('Explain what is meant by virtual memory.', 'Secondary storage used to extend RAM; pages swapped between RAM and disk as needed.', '1 mark each [2]'),
    ('Explain why the computer slows down in this situation.', 'Too little RAM so pages are continually swapped in and out (disk thrashing); disk access is much slower than RAM.', '1 mark each [2]'),
    ('Suggest how the problem could be reduced.', 'Add RAM; close programs; reduce number of processes; use an SSD for the swap area.', '1 mark per point, max 2 [2]')], k=(2, 3))
scen(t6_2, 'C4', (3, 4, 5), [
    'The operating system of a computer at {org} uses paged virtual memory.', '{p} is studying how a games console manages memory when several games are suspended.',
], [lambda r, d: (lambda ps, la: (f'Pages are {ps} bytes. Calculate the page number and offset for logical address {la}.', f'page {la // ps}, offset {la % ps}', '1 mark each [2]'))(
    r.choice([512, 1024, 4096]), r.randrange(5000, 30000)),
    ('Explain the purpose of the page table.', 'Maps each page of the process to the frame in RAM holding it, with a flag to show whether the page is present.', '1 mark each [2]'),
    ('Describe what happens when a page fault occurs.', 'Interrupt; OS finds the page on disk; chooses a frame (replacing a page using an algorithm, writing it back if changed); loads page; updates page table; process restarts.', '1 mark per point, max 3 [3]'),
    ('Compare paging with segmentation.', 'Paging: fixed-size, physical division, internal fragmentation; segmentation: variable-size, logical division, external fragmentation.', '1 mark per point, max 3 [3]')], k=(3, 4))

t6_3 = topic('Translation software: stages of compilation (lexical, syntax analysis, code generation, optimisation)', 'translation software', 'stages of compilation', 'lexical', 'syntax analysis', 'code generation', 'optimisation')
STAGES = [('lexical analysis', 'removes white space and comments and converts the source code into tokens, adding identifiers to the symbol table'),
          ('syntax analysis', 'checks that the sequence of tokens obeys the grammar rules of the language, producing a parse tree and syntax errors'),
          ('code generation', 'produces the object code (machine code) from the parse tree'),
          ('optimisation', 'changes the code so it runs faster or uses less memory without changing what it does')]
t6_3.fixed('C1', (1, 2), [(f'Which stage of compilation {d}?', n.capitalize(), f'{n}: {d}.', [x[0].capitalize() for x in STAGES if x[0] != n]) for n, d in STAGES] + [
    ('In which order are the stages of compilation carried out?', 'Lexical analysis, syntax analysis, code generation, optimisation', 'Optimisation can also happen during code generation.', ['Syntax analysis, lexical analysis, optimisation, code generation', 'Code generation, lexical analysis, syntax analysis, optimisation', 'Optimisation, code generation, syntax analysis, lexical analysis']),
    ('What is a token?', 'A string of characters with a meaning in the language, such as a keyword, identifier or operator', 'Lexical analysis produces a token stream.', ['A memory address', 'A comment in the program', 'A line of machine code']),
    ('What is held in the symbol table?', 'Identifiers with information such as their data type and memory location', 'Built during lexical analysis and used in later stages.', ['The list of keywords of the language', 'The machine code output', 'The error messages']),
])
t6_3.fixed('C2', (2, 3, 4), [
    ('Explain why code optimisation is carried out.', 'To make the object code run faster and/or use less memory, e.g. by removing redundant code or reusing results, without changing the program\'s result.', '1 mark each [2]'),
    ('Explain the difference between the errors found in lexical analysis and syntax analysis.', 'Lexical: invalid tokens/characters or identifiers (e.g. illegal symbol); syntax: tokens in an order that breaks grammar rules (e.g. missing bracket, IF without THEN).', '1 mark each [2]'),
])
ar(t6_3, [('Comments do not appear in the object code.', 'Lexical analysis removes comments and white space.'),
          ('A syntax error can be reported before any object code is produced.', 'Syntax analysis happens before code generation.'),
          ('Optimised code can run faster.', 'Optimisation removes redundant instructions or reuses computed values.'),
          ('The symbol table is used during code generation.', 'It holds the data type and address of each identifier.')],
   ['Lexical analysis checks that statements obey the grammar.', 'Code generation happens before syntax analysis.', 'Optimisation changes the output of the program.', 'Tokens are produced during code generation.'])

VARS = ['Total', 'Price', 'Count', 'Rate', 'Tax', 'Score', 'Width', 'Height', 'Speed', 'Bonus', 'Index', 'Cost']


@t6_3.add('C3', (1, 2, 3, 4, 5))
def t6_3_tokens(r, D):
    n = 2 if D <= 2 else (3 if D <= 4 else 4)
    vs = r.sample(VARS, n + 1)
    toks = [vs[0], '←']
    terms = []
    for i in range(n):
        if i:
            toks.append(r.choice(['+', '-', '*', '/']))
        if r.random() < 0.4:
            toks.append(str(r.randrange(2, 20)))
        else:
            toks.append(vs[i + 1])
    if D >= 4:
        toks.insert(2, '(')
        toks.insert(6, ')') if len(toks) > 6 else toks.append(')')
        if toks[-1] == ')' and toks.count('(') == 1 and toks.index('(') == 2 and len(toks) < 6:
            pass
    stmt = ' '.join(toks)
    ids = []
    for t in toks:
        if t[0].isalpha() and t not in ids:
            ids.append(t)
    if D <= 2:
        return MCQ(r, f'How many tokens are produced by lexical analysis of the statement {stmt}?', str(len(toks)), [str(len(toks) - 1), str(len(toks) + 1), str(len(ids)), str(len(toks) + 2)], 'Tokens: ' + ', '.join(toks) + f' = {len(toks)}.')
    return Q(f'During lexical analysis the statement {stmt} is processed. List the tokens produced and identify which tokens are entered into the symbol table.', 'Tokens: ' + ', '.join(toks) + f' ({len(toks)}); symbol table: ' + ', '.join(ids),
             f'all {len(toks)} tokens [2]; identifiers {", ".join(ids)} [1] [3]', marks=3)


@t6_3.add('C3', (2, 3, 4, 5))
def t6_3_opt(r, D):
    a, c, e, x, y = r.sample(VARS, 5)
    k1, k2 = r.randrange(2, 10), r.randrange(2, 10)
    kind = r.choice(['cse', 'fold', 'loop', 'dead'])
    if kind == 'cse':
        orig = [f'{x} ← {a} * {c} + {k1}', f'{y} ← {a} * {c} - {e}']
        opt = [f'Temp ← {a} * {c}', f'{x} ← Temp + {k1}', f'{y} ← Temp - {e}']
        why = f'{a} * {c} is calculated twice (common subexpression), so it is calculated once and reused'
    elif kind == 'fold':
        orig = [f'{x} ← {k1} * {k2} * {a}']
        opt = [f'{x} ← {k1 * k2} * {a}']
        why = f'the constant expression {k1} * {k2} is evaluated at compile time ({k1 * k2}) (constant folding)'
    elif kind == 'loop':
        orig = [f'FOR I ← 1 TO {k1 * 10}', f'{IND}{x} ← {a} * {k2}', f'{IND}{y}[I] ← {y}[I] + {x}', 'NEXT I']
        opt = [f'{x} ← {a} * {k2}', f'FOR I ← 1 TO {k1 * 10}', f'{IND}{y}[I] ← {y}[I] + {x}', 'NEXT I']
        why = f'{x} ← {a} * {k2} gives the same value every iteration, so it is moved out of the loop and executed once instead of {k1 * 10} times'
    else:
        orig = [f'{x} ← {a} + {k1}', f'{x} ← {c} * {k2}', f'OUTPUT {x}']
        opt = [f'{x} ← {c} * {k2}', f'OUTPUT {x}']
        why = f'the first value assigned to {x} is never used before it is overwritten, so that statement is redundant'
    return Q('A compiler optimises the code:\n' + code(orig) + '\nWrite an optimised version and explain the optimisation made.', code(opt) + '\n' + why[0].upper() + why[1:] + '.', '1 mark optimised code; 1 mark explanation [2]', marks=2)


scen(t6_3, 'C2', (2, 3, 4), [
    '{p} is compiling a program written for {org}.', 'A compiler at {org} reports an error in the statement IF Total > 100 Discount ← 5 ENDIF.',
], [('Identify the stage of compilation that would find a missing THEN and explain why.', 'Syntax analysis: the token sequence breaks the grammar rule for IF ... THEN ... ENDIF.', '1 mark stage; 1 mark reason [2]'),
    ('Explain what happens to comments and spaces during compilation.', 'Removed in lexical analysis, since they are not needed to produce object code.', '1 mark each [2]'),
    ('Explain the role of the symbol table in code generation.', 'Gives the data type and memory address of each identifier so instructions can refer to the correct locations.', '1 mark each [2]')], k=(2, 3))
scen(t6_3, 'C4', (3, 4, 5), [
    '{org} uses a compiler to translate its stock control program into machine code.', '{p} is writing a simple compiler for a teaching language at {org}.',
], [('Describe the tasks carried out during lexical analysis.', 'Remove white space/comments; identify tokens; replace keywords/operators with tokens; add identifiers to the symbol table; report invalid tokens.', '1 mark per point, max 3 [3]'),
    ('Describe what happens during syntax analysis.', 'Tokens are parsed against the grammar (e.g. BNF); a parse tree is built; syntax errors are reported.', '1 mark per point, max 2 [2]'),
    lambda r, d: (lambda q: (q['stem'].replace('A compiler optimises the code:', 'The compiler is given the code:'), q['answer'], q['key']))(t6_3_opt(r, 4)),
    ('Explain why a compiled program runs faster than the same program run by an interpreter.', 'Translation happens once before execution; an interpreter translates each statement every time it is run.', '1 mark each [2]')], k=(3, 4))

t6_4 = topic('Backus–Naur form, syntax diagrams and Reverse Polish Notation', 'backus–naur form', 'syntax diagrams', 'reverse polish notation')
t6_4.fixed('C1', (1, 2), [
    ('What is Backus–Naur form (BNF) used for?', 'Describing the syntax rules of a language', 'Meta-language with ::= and | to define grammar.', ['Converting infix to postfix', 'Storing data in a database', 'Compressing source code']),
    ('In BNF, what does the symbol | mean?', 'OR: a choice between alternatives', '::= means "is defined as"; <...> encloses a non-terminal.', ['AND', 'is defined as', 'end of the rule']),
    ('In BNF, what does ::= mean?', 'Is defined as', 'e.g. <digit> ::= 0|1|2.', ['Is equal to in value', 'OR', 'Is not defined']),
    ('What is a recursive BNF definition?', 'A rule that refers to itself, e.g. <number> ::= <digit> | <digit><number>', 'Recursion allows items of unlimited length.', ['A rule with no alternatives', 'A rule containing only terminals', 'A rule that cannot be parsed']),
    ('Reverse Polish Notation places operators where?', 'After their operands (postfix)', 'e.g. A + B becomes A B +.', ['Before their operands', 'Between their operands', 'Only at the start of the expression']),
    ('Why do compilers use Reverse Polish Notation?', 'It needs no brackets and can be evaluated using a stack in one left-to-right pass', 'Operator precedence is built into the order.', ['It is easier for humans to read', 'It uses less memory than machine code', 'It removes all variables']),
    ('Which data structure is used to evaluate an RPN expression?', 'A stack', 'Push operands; on an operator pop two, apply, push the result.', ['A queue', 'A binary search tree', 'A hash table']),
])
t6_4.fixed('C2', (2, 3, 4), [
    ('Explain how a stack is used to evaluate an expression in Reverse Polish Notation.', 'Read tokens left to right; push each operand; when an operator is read, pop the top two values, apply the operator (second popped op first popped) and push the result; the final value on the stack is the answer.', '1 mark per point, max 3 [3]'),
    ('Explain why a syntax diagram and a BNF definition can describe the same rule.', 'Both are meta-languages defining the valid sequences of symbols; the diagram shows the alternatives and repetitions as paths/loops, BNF uses | and recursion.', '1 mark each [2]'),
])
ar(t6_4, [('Reverse Polish Notation needs no brackets.', 'The order of operators and operands determines the order of evaluation.'),
          ('BNF can define identifiers of any length.', 'A rule can be defined recursively in terms of itself.'),
          ('A stack is suitable for evaluating RPN.', 'The most recent two operands are the ones needed by the next operator.')],
   ['In RPN the operator comes before its operands.', 'BNF cannot express a choice between alternatives.', 'A queue is used to evaluate RPN.'])

OPS = {'+': (1, lambda a, c: a + c), '-': (1, lambda a, c: a - c), '*': (2, lambda a, c: a * c), '/': (2, lambda a, c: a // c if c and a % c == 0 else None)}


def rpn_tree(r, n, leaves):
    """Random expression tree with n operators; leaves from list."""
    if n == 0:
        return ('L', r.choice(leaves))
    k = r.randrange(n)
    op = r.choice(['+', '-', '*', '*', '+', '-', '/'])
    return (op, rpn_tree(r, k, leaves), rpn_tree(r, n - 1 - k, leaves))


def infix(t, parent=None, right=False):
    if t[0] == 'L':
        return str(t[1])
    s = infix(t[1], t[0]) + f' {t[0]} ' + infix(t[2], t[0], True)
    if parent:
        pp, mp = OPS[parent][0], OPS[t[0]][0]
        if mp < pp or (mp == pp and right and parent in '-/') or (mp == pp and right and t[0] in '-/' and parent in '+*' and False):
            s = '(' + s + ')'
        elif mp == pp and right and parent in '*' and t[0] == '/':
            s = '(' + s + ')'
    return s


def rpn(t):
    return str(t[1]) if t[0] == 'L' else rpn(t[1]) + ' ' + rpn(t[2]) + ' ' + t[0]


def tev(t, env):
    if t[0] == 'L':
        return env.get(t[1], t[1]) if isinstance(t[1], str) else t[1]
    a, c = tev(t[1], env), tev(t[2], env)
    if a is None or c is None:
        return None
    return OPS[t[0]][1](a, c)


def rpn_stack(s, env):
    st, frames = [], []
    for tok in s.split():
        if tok in OPS:
            c, a = st.pop(), st.pop()
            st.append(OPS[tok][1](a, c))
        else:
            st.append(env.get(tok, int(tok) if tok.isdigit() else 0))
        frames.append(list(st))
    return st[-1], frames


def _rpn_item(r, D, use_vars):
    for _ in range(50):
        n = 2 if D <= 2 else (3 if D <= 4 else 4)
        leaves = r.sample(['A', 'B', 'C', 'D', 'E', 'X', 'Y'], n + 1) if use_vars else list(range(2, 13))
        t = rpn_tree(r, n, leaves)
        env = {v: r.randrange(1, 13) for v in leaves} if use_vars else {}
        v = tev(t, env)
        if v is not None and v >= 0 and infix(t).count('(') <= 2:
            # check infix with Python evaluation matches tree value (bracket correctness)
            expr = infix(t)
            py = expr.replace('/', '//')
            for k_, x in env.items():
                py = re.sub(rf'\b{k_}\b', str(x), py)
            try:
                if eval(py) != v:
                    continue
            except Exception:
                continue
            return t, env, v
    return None


@t6_4.add('C3', (1, 2, 3, 4, 5))
def t6_4_convert(r, D):
    x = _rpn_item(r, D, True)
    if not x:
        return None
    t, env, v = x
    inf, post = infix(t), rpn(t)
    if r.random() < 0.5:
        if D <= 2:
            wrong = [inf.replace('(', '').replace(')', '').replace(' ', ' ').split(' ')[0] + ' ' + ' '.join(reversed(post.split()[1:])), ' '.join(reversed(post.split())),
                     ' '.join([tok for tok in post.split() if tok not in OPS] + [tok for tok in post.split() if tok in OPS][::-1]), inf.replace('(', '').replace(')', '')]
            return MCQ(r, f'Which is the Reverse Polish Notation for the infix expression {inf}?', post, wrong, f'Operators follow their operands in evaluation order: {post}.')
        return Q(f'Convert the infix expression {inf} into Reverse Polish Notation.', post, f'operands in correct order [1]; operators in correct positions [1] [2]', marks=2)
    return Q(f'Convert the Reverse Polish Notation expression {post} into infix form, using brackets only where needed.', inf, f'correct operators and operands [1]; brackets/precedence correct [1] [2]', marks=2)


@t6_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_4_eval(r, D):
    use_vars = D >= 3
    x = _rpn_item(r, D, use_vars)
    if not x:
        return None
    t, env, v = x
    post = rpn(t)
    val, frames = rpn_stack(post, env)
    if val != v:
        return None
    given = (' where ' + ', '.join(f'{k} = {env[k]}' for k in sorted(env))) if use_vars else ''
    if D == 1:
        return MCQ(r, f'What is the value of the Reverse Polish Notation expression {post}?', str(v), [str(v + 1), str(v * 2), str(abs(v - 3)), str(v + 10)], f'Using a stack: {" → ".join(str(f) for f in frames)}.')
    stem = f'Evaluate the Reverse Polish Notation expression {post}{given}. Show the contents of the stack after each operator is processed.'
    ops_frames = [f for tok, f in zip(post.split(), frames) if tok in OPS]
    return Q(stem, f'{v}', 'stack after each operator: ' + '; '.join(str(f) for f in ops_frames) + f' [{len(ops_frames)}]; final value {v} [1] [{len(ops_frames) + 1}]', marks=len(ops_frames) + 1)


GRAMMARS = [
    ('<code> ::= <letter><letter><digit> | <letter><digit><digit>\n<letter> ::= A | B | C | D\n<digit> ::= 1 | 2 | 3', r'[A-D]([A-D]|[1-3])[1-3]', 'ABCD123XY09', '<code>', 3),
    ('<signed> ::= <sign><number>\n<number> ::= <digit> | <digit><number>\n<sign> ::= + | -\n<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9', r'[+-][0-9]+', '+-0123456789A', '<signed>', 4),
    ('<identifier> ::= <letter> | <identifier><letter> | <identifier><digit>\n<letter> ::= a | b | c | x | y\n<digit> ::= 0 | 1 | 2', r'[abcxy][abcxy012]*', 'abcxy012dz9', '<identifier>', 4),
    ('<assignment> ::= <variable>=<variable><operator><variable>\n<variable> ::= <letter><digit>\n<letter> ::= P | Q | R\n<digit> ::= 1 | 2\n<operator> ::= + | -', r'[PQR][12]=[PQR][12][+-][PQR][12]', 'PQR12=+-*S', '<assignment>', 8),
    ('<hex> ::= #<hexdigit><hexdigit>\n<hexdigit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F', r'#[0-9A-F]{2}', '#0123456789ABCDEFG', '<hex>', 3),
    ('<binary> ::= <bit> | <bit><binary>\n<bit> ::= 0 | 1\n<byte> ::= B<binary>', r'B[01]+', 'B0123', '<byte>', 5),
]


def _gram_valid(r, g):
    pat, alpha = g[1], g[2]
    for _ in range(200):
        s = ''.join(r.choice(alpha) for _ in range(r.randrange(2, g[4] + 2)))
        if re.fullmatch(pat, s):
            return s
    # construct by hand
    return {0: 'AB2', 1: '+' + str(r.randrange(10, 999)), 2: 'x1b', 3: 'P1=Q2+R1', 4: '#' + format(r.randrange(256), '02X'), 5: 'B' + format(r.randrange(2, 64), 'b')}[GRAMMARS.index(g)]


def _gram_mutate(r, s, g):
    for _ in range(50):
        k = r.randrange(3)
        lst = list(s)
        if k == 0 and len(lst) > 1:
            i = r.randrange(len(lst))
            lst[i] = r.choice(g[2])
        elif k == 1:
            lst.insert(r.randrange(len(lst) + 1), r.choice(g[2]))
        elif len(lst) > 1:
            del lst[r.randrange(len(lst))]
        t = ''.join(lst)
        if t != s and not re.fullmatch(g[1], t):
            return t
    return None


@t6_4.add('C3', (2, 3, 4, 5))
def t6_4_bnf(r, D):
    g = r.choice(GRAMMARS)
    n = 3 if D <= 3 else 4
    cands = []
    for _ in range(n * 5):
        v = _gram_valid(r, g)
        s = v if r.random() < 0.5 else _gram_mutate(r, v, g)
        if s and s not in cands:
            cands.append(s)
        if len(cands) == n:
            break
    if len(cands) < n:
        return None
    res = [(s, bool(re.fullmatch(g[1], s))) for s in cands]
    stem = f'A language is defined by these BNF rules:\n{g[0]}\nState whether each of these is a valid {g[3]}: ' + ', '.join(s for s, _ in res) + '.'
    return Q(stem, '; '.join(f'{s} {"valid" if ok else "invalid"}' for s, ok in res), f'1 mark per correct decision [{n}]', marks=n)


scen(t6_4, 'C4', (3, 4, 5), [
    '{p} is writing an interpreter for a calculator app developed in {city}.', 'A compiler being developed at {org} in {city} converts expressions to Reverse Polish Notation.',
], [lambda r, d: (lambda x: (f'Convert {infix(x[0])} to Reverse Polish Notation.', rpn(x[0]), '1 mark operands; 1 mark operators [2]') if x else None)(_rpn_item(r, 3, True)),
    lambda r, d: (lambda x: (f'Evaluate the RPN expression {rpn(x[0])}, showing the stack after each operator.', str(x[2]), '1 mark per stack state; 1 mark answer [3]') if x else None)(_rpn_item(r, 3, False)),
    ('Explain why RPN is used by the interpreter.', 'No brackets or precedence rules needed; evaluated left to right in one pass using a stack.', '1 mark each [2]'),
    ('Write a BNF definition for an unsigned integer made of one or more digits.', '<digit> ::= 0|1|2|3|4|5|6|7|8|9\n<integer> ::= <digit> | <digit><integer>', '1 mark digit rule; 1 mark recursive rule [2]')], k=(3, 4))

CHAPTERS[6] = [t6_1, t6_2, t6_3, t6_4]

# =============================================================================== Chapter 7 Security
t7_1 = topic('Symmetric and asymmetric encryption; public and private keys', 'symmetric and asymmetric encryption', 'public and private keys')
t7_1.fixed('C1', (1, 2), [
    ('What is symmetric encryption?', 'Encryption in which the same secret key is used to encrypt and decrypt', 'Both parties must share the key securely.', ['Encryption using a public key and a private key', 'Encryption that cannot be decrypted', 'Encryption that uses no key']),
    ('What is asymmetric encryption?', 'Encryption that uses a matching pair of keys: a public key and a private key', 'Data encrypted with one key of the pair can only be decrypted with the other.', ['Encryption using one shared secret key', 'Encryption of only half the data', 'Encryption using a hash function']),
    ('Which key must be kept secret by its owner?', 'The private key', 'The public key can be given to anyone.', ['The public key', 'Both keys', 'Neither key']),
    ('What is plaintext?', 'The original readable data before encryption', 'Ciphertext is the encrypted, unreadable form.', ['Encrypted data', 'The encryption key', 'Data that has been hashed']),
    ('What is the main problem with symmetric encryption?', 'Securely distributing the shared key to the recipient', 'If the key is intercepted, all messages can be read.', ['It is too slow for large files', 'It cannot be used on networks', 'The keys are too short to be secure']),
    ('Why is a longer encryption key more secure?', 'There are more possible keys, so a brute-force attack takes longer', 'An n-bit key gives 2ⁿ possible keys.', ['It makes the ciphertext shorter', 'It makes encryption faster', 'It removes the need for a private key']),
])
t7_1.fixed('C2', (2, 3, 4), [
    ('Explain why asymmetric encryption solves the key distribution problem of symmetric encryption.', 'The public key can be shared openly because only the matching private key (never transmitted) can decrypt the message.', '1 mark each [2]'),
    ('Explain why symmetric encryption is often used for the bulk of the data even when asymmetric encryption is available.', 'Symmetric encryption is much faster/less processor-intensive; asymmetric encryption is used only to exchange the symmetric session key.', '1 mark each [2]'),
])
ar(t7_1, [('A public key can be published openly.', 'Data encrypted with it can only be decrypted using the matching private key.'),
          ('Symmetric encryption requires a secure way to share the key.', 'The same key is used for both encryption and decryption.'),
          ('A 128-bit key is harder to brute-force than a 64-bit key.', 'Each extra bit doubles the number of possible keys.'),
          ('Asymmetric encryption is slower than symmetric encryption.', 'It uses more complex mathematical operations with larger keys.')],
   ['The private key is shared with everyone who sends you messages.', 'Symmetric encryption uses two different keys.', 'Ciphertext can be read without the key.', 'Public keys must be kept secret.'])


@t7_1.add('C3', (1, 2, 3, 4))
def t7_1_which(r, D):
    a, c = r.sample(['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Priya', 'Omar', 'Hana'], 2)
    kind = r.choice(['enc', 'dec', 'sign', 'verify'])
    if kind == 'enc':
        q, ans, why = f'{a} wants to send a confidential message to {c} using asymmetric encryption. Which key should {a} use to encrypt the message?', f"{c}'s public key", f'Only {c} has the matching private key, so only {c} can decrypt it.'
    elif kind == 'dec':
        q, ans, why = f'{a} has sent {c} a message encrypted with {c}\'s public key. Which key does {c} use to decrypt it?', f"{c}'s private key", 'Data encrypted with a public key can only be decrypted with the matching private key.'
    elif kind == 'sign':
        q, ans, why = f'{a} wants to digitally sign a document sent to {c}. Which key does {a} use to encrypt the hash (digest) of the document?', f"{a}'s private key", f'Only {a} has this key, so the signature proves the sender.'
    else:
        q, ans, why = f'{c} receives a document digitally signed by {a}. Which key does {c} use to decrypt the digital signature?', f"{a}'s public key", f"The signature was made with {a}'s private key, so only {a}'s public key can decrypt it, proving it came from {a}."
    opts = [f"{a}'s public key", f"{a}'s private key", f"{c}'s public key", f"{c}'s private key"]
    if D <= 2:
        return MCQ(r, q, ans, [o for o in opts if o != ans], why)
    q2 = re.sub(r'Which key (does|should) (\w+) use to (.*)\?', lambda m: f'Identify the key that {m.group(2)} {"should use" if m.group(1) == "should" else "uses"} to {m.group(3)}, and explain your choice.', q)
    return Q(q2, f'{ans}: {why}', '1 mark key; 1 mark explanation [2]', marks=2)


@t7_1.add('C3', (2, 3, 4, 5), 'numerical')
def t7_1_keys(r, D):
    if D <= 3 or r.random() < 0.4:
        n = r.choice([5, 8, 10, 12, 20, 25, 50, 100])
        sym = n * (n - 1) // 2
        return Q(f'A group of {n} people each want to be able to communicate privately with every other member of the group. Calculate the number of keys needed using symmetric encryption and using asymmetric encryption.',
                 f'symmetric {sym} keys; asymmetric {n} key pairs ({2 * n} keys)', f'symmetric: one key per pair = {n} × {n - 1} ÷ 2 = {sym} [1]; asymmetric: one public/private pair each = {2 * n} keys [1] [2]', marks=2)
    bits = r.choice([40, 48, 56, 64])
    rate = r.choice([10 ** 9, 10 ** 10, 10 ** 12])
    keys = 2 ** bits
    avg = keys / 2 / rate
    def tstr(s):
        for u, v in (('years', 365 * 24 * 3600), ('days', 86400), ('hours', 3600), ('minutes', 60)):
            if s >= v:
                return f'{s / v:.3g} {u}'
        return f'{s:.3g} seconds'
    return Q(f'An encryption algorithm uses a {bits}-bit key. A computer can test {rate:.0e} keys per second. Calculate the number of possible keys and the average time to find the key by brute force (testing half of the keys).'.replace('e+', ' × 10^'),
             f'2^{bits} = {keys:,} keys; average time ≈ {tstr(avg)}', f'2^{bits} keys [1]; ÷ 2 ÷ rate = {avg:,.0f} s [1]; ≈ {tstr(avg)} [1] [3]', marks=3)


@t7_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t7_1_xor(r, D):
    key = r.randrange(1, 256)
    if D <= 2:
        p = r.randrange(1, 256)
        c = p ^ key
        if D == 1:
            return MCQ(r, f'A simple symmetric cipher XORs each byte with the key {b(key)}. What is the ciphertext for the plaintext byte {b(p)}?', b(c), [b(p & key), b(p | key), b(~c & 255), b(p ^ 255)], f'{b(p)} XOR {b(key)} = {b(c)}.')
        return Q(f'A simple symmetric cipher XORs each byte with the key {b(key)}. Encrypt the byte {b(p)}, then show that applying the same key again gives back the plaintext.', f'{b(c)}; {b(c)} XOR {b(key)} = {b(p)}',
                 f'ciphertext {b(c)} [1]; decrypted {b(p)} [1] [2]', marks=2)
    word = r.choice(['KEY', 'CAT', 'MAP', 'SUN', 'DOG', 'BOX', 'HI', 'OK', 'LAB', 'NET'])[:2 if D == 3 else 3]
    cs = [ord(ch) ^ key for ch in word]
    return Q(f'A symmetric cipher encrypts each ASCII character code by XOR with the 8-bit key {b(key)}. Give the ciphertext, in binary, for the plaintext "{word}" (ASCII: ' + ', '.join(f'{ch} = {ord(ch)}' for ch in word) + '), and explain why the same key decrypts it.',
             '; '.join(b(x) for x in cs) + '; XOR with the same key twice returns the original value (A XOR K XOR K = A)', '; '.join(f'{ch}: {b(ord(ch))} XOR {b(key)} = {b(x)}' for ch, x in zip(word, cs)) + f' [{len(word)}]; explanation [1] [{len(word) + 1}]', marks=len(word) + 1)


scen(t7_1, 'C4', (3, 4, 5), [
    '{org} in {city} sends confidential reports to its partners over the internet.', '{p} and {q} work for {org} and exchange sensitive files by email.',
], [('Explain how asymmetric encryption keeps the reports confidential.', 'Sender encrypts with the recipient\'s public key; only the recipient\'s private key can decrypt; the private key is never sent.', '1 mark per point, max 3 [3]'),
    ('Explain why symmetric encryption alone would be a risk.', 'The single shared key must be sent to the partner and could be intercepted, allowing all messages to be decrypted.', '1 mark each [2]'),
    lambda r, d: (lambda n: (f'{org_n(d)} has {n} partners who must each communicate privately with every other partner. Calculate the number of symmetric keys needed.', str(n * (n - 1) // 2), f'{n} × {n - 1} ÷ 2 [1]; = {n * (n - 1) // 2} [1] [2]'))(r.choice([6, 8, 12, 15])),
    ('Explain why a session key is often used.', 'Asymmetric encryption is used once to exchange a symmetric session key, then faster symmetric encryption is used for the data.', '1 mark each [2]')], k=(3, 4))


def org_n(d):
    return d['org']


t7_2 = topic('Secure Socket Layer (SSL) and Transport Layer Security (TLS)', 'secure socket layer', 'transport layer security', 'ssl', 'tls')
HANDSHAKE = ['The client sends a "client hello" listing the TLS versions and cipher suites it supports',
             'The server replies with a "server hello" choosing the cipher suite, and sends its digital certificate',
             'The client checks the server\'s certificate using the public key of the certificate authority',
             'The client creates the session key material, encrypts it with the server\'s public key and sends it',
             'The server decrypts this with its private key and both sides generate the same symmetric session key',
             'Data is exchanged, encrypted with the symmetric session key']
t7_2.fixed('C1', (1, 2), [
    ('What is the purpose of SSL/TLS?', 'To provide secure, encrypted and authenticated communication between a client and a server', 'Used for HTTPS, secure email etc.', ['To compress web pages', 'To assign IP addresses', 'To route packets across the internet']),
    ('Which protocol has replaced SSL?', 'TLS', 'TLS is the successor to SSL.', ['HTTP', 'FTP', 'POP3']),
    ('What are the two main layers of TLS?', 'The record protocol and the handshake protocol', 'Handshake: authentication and key exchange; record: encrypts/transfers the data.', ['The physical layer and the link layer', 'The client layer and the server layer', 'The hash layer and the key layer']),
    ('What does the "S" in HTTPS indicate?', 'The HTTP data is sent over a secure TLS/SSL connection', 'Browsers display a padlock.', ['The site is small', 'The data is sent faster', 'The server is in a safe country']),
    ('During the TLS handshake, what does the server send to prove its identity?', 'Its digital certificate', 'The client verifies it using the CA\'s public key.', ['Its private key', 'The session key in plaintext', 'Its IP address only']),
    ('What type of encryption is used for the data once a TLS session is established?', 'Symmetric encryption using a session key', 'Asymmetric encryption is used only during the handshake.', ['Asymmetric encryption for all data', 'No encryption', 'Hashing only']),
])
t7_2.fixed('C2', (2, 3, 4), [
    ('Explain why TLS uses both asymmetric and symmetric encryption.', 'Asymmetric encryption securely exchanges the session key without sharing a secret in advance; symmetric encryption is then used for the data because it is faster.', '1 mark each [2]'),
    ('Explain how TLS protects a user against a fake website.', 'The server must present a digital certificate signed by a trusted CA; the browser verifies it, so an impostor without a valid certificate is detected and the user warned.', '1 mark each [2]'),
])
ar(t7_2, [('A browser shows a warning if a website\'s certificate is not valid.', 'TLS checks the certificate against trusted certificate authorities.'),
          ('TLS uses a session key for most of the data.', 'Symmetric encryption is faster than asymmetric encryption.'),
          ('HTTPS protects passwords sent to a website.', 'The data is encrypted using TLS before it is transmitted.')],
   ['TLS sends the session key as plaintext.', 'SSL is newer and more secure than TLS.', 'The server sends its private key to the client during the handshake.'])


@t7_2.add('C3', (2, 3, 4, 5))
def t7_2_order(r, D):
    n = 4 if D <= 3 else 6
    steps = HANDSHAKE[:n] if n == 6 else [HANDSHAKE[0], HANDSHAKE[1], HANDSHAKE[2], HANDSHAKE[5]]
    shuf = steps[:]
    while shuf == steps:
        r.shuffle(shuf)
    letters = 'ABCDEF'
    lab = {s: letters[i] for i, s in enumerate(shuf)}
    stem = 'The statements describe stages of setting up and using a TLS connection between a browser and a web server. ' + ' '.join(f'{letters[i]}: {s}.' for i, s in enumerate(shuf)) + ' Write the letters in the correct order.'
    ans = ', '.join(lab[s] for s in steps)
    return Q(stem, ans, f'Correct order {ans}. 1 mark for each correctly placed pair of stages [{n // 2}]', marks=n // 2)


@t7_2.add('C3', (1, 2, 3))
def t7_2_where(r, D):
    uses = [('a customer entering card details on an online shop', 'the card details are encrypted and the shop\'s identity is verified'),
            ('a student logging in to a school\'s virtual learning environment', 'the username and password are encrypted in transit'),
            ('a doctor viewing patient records through a web portal', 'confidential medical data cannot be read if intercepted'),

            ('a customer using online banking', 'the bank\'s certificate is verified and all transactions are encrypted'),
            ('an employee connecting to a company intranet from home', 'data crossing the public internet is encrypted')]
    u, why = r.choice(uses)
    if D == 1:
        return MCQ(r, f'Why should TLS be used for {u}?', why[0].upper() + why[1:], ['It makes the web page load faster', 'It compresses the data to save bandwidth', 'It gives the user a static IP address', 'It removes the need for a password'], f'TLS: {why}.')
    return Q(f'Explain why TLS should be used for {u}, and describe how the user can tell that it is being used.', f'{why[0].upper() + why[1:]}; the web address begins with https and the browser shows a padlock.', '1 mark reason; 1 mark explanation; 1 mark identification [3]', marks=3)


scen(t7_2, 'C2', (2, 3, 4), [
    '{org} in {city} has launched an online booking website.', '{p} is buying tickets from the website of {org}.',
], [('Explain the purpose of the server\'s digital certificate in the TLS handshake.', 'Proves the server\'s identity and supplies its public key; signed by a CA so the browser can verify it.', '1 mark each [2]'),
    ('Explain why the session key is not used for long.', 'A new key for each session limits the data exposed if a key is compromised.', '1 mark each [2]'),
    ('Explain what the browser does if the certificate has expired.', 'Displays a warning that the connection may not be secure; user may choose not to proceed.', '1 mark each [2]')], k=(2, 3))
scen(t7_2, 'C4', (3, 4, 5), [
    '{org} in {city} is setting up an online shop.', '{p} is the web developer for {org}, whose customers log in to view their accounts.',
], [('Describe the stages of the TLS handshake.', 'Client hello; server hello + certificate; client verifies certificate with CA; key exchange (session key encrypted with server public key); both derive symmetric session key.', '1 mark per stage, max 4 [4]'),
    ('Explain why the shop must obtain a certificate from a certificate authority.', 'Browsers trust certificates signed by a CA; a self-signed certificate would trigger warnings and could not prove identity.', '1 mark each [2]'),
    ('Explain the difference between the handshake protocol and the record protocol.', 'Handshake: authenticates and agrees keys/cipher suite; record: uses the agreed keys to encrypt, (compress) and transfer data.', '1 mark each [2]'),
    ('State two other protocols that can be secured using TLS.', 'e.g. SMTP/IMAP/POP3 (email), FTP (FTPS), VoIP.', '1 mark each [2]')], k=(3, 4))

t7_3 = topic('Digital certificates and digital signatures; quantum cryptography', 'digital certificates', 'digital signatures', 'quantum cryptography')
t7_3.fixed('C1', (1, 2), [
    ('Who issues a digital certificate?', 'A certificate authority (CA)', 'The CA verifies the identity of the applicant and signs the certificate.', ['The web browser', 'The user\'s ISP', 'The operating system']),
    ('Which of these is contained in a digital certificate?', 'The owner\'s public key', 'Also: owner identity, serial number, validity dates, CA name and the CA\'s digital signature.', ['The owner\'s private key', 'The session key', 'The owner\'s password']),
    ('A digital signature is created by encrypting the message digest with', 'the sender\'s private key', 'The recipient decrypts it with the sender\'s public key.', ['the recipient\'s public key', 'the recipient\'s private key', 'the session key']),
    ('What is a message digest?', 'A fixed-length value produced by applying a hashing algorithm to a message', 'Any change to the message gives a different digest.', ['The message encrypted with a public key', 'A summary written by the sender', 'The first line of the message']),
    ('What does quantum cryptography use to transmit a key securely?', 'The polarisation of photons sent through a fibre-optic cable', 'Quantum key distribution (QKD): observing a photon changes its state, so eavesdropping is detected.', ['Very long prime numbers', 'Radio waves', 'Hash functions']),
    ('Why can eavesdropping be detected in quantum key distribution?', 'Measuring a photon changes its state, causing errors that the sender and receiver can detect', 'Heisenberg uncertainty principle.', ['The photons are too fast to intercept', 'The key is too long to copy', 'The photons are encrypted with a password']),
])
t7_3.fixed('C2', (2, 3, 4), [
    ('Explain how a digital signature shows that a message has not been altered.', 'The receiver hashes the received message and compares it with the digest obtained by decrypting the signature with the sender\'s public key; if they match, the message is unaltered.', '1 mark per point, max 3 [3]'),
    ('Explain one benefit and one drawback of quantum cryptography.', 'Benefit: interception of the key can be detected, so key exchange is very secure (and long keys possible). Drawback: needs dedicated fibre/expensive equipment and has limited range; photons can be lost.', '1 mark each [2]'),
])
ar(t7_3, [('A digital signature proves who sent a message.', 'Only the sender has the private key used to encrypt the digest.'),
          ('A changed message will fail the signature check.', 'Any change to the message changes its hash.'),
          ('Browsers trust certificates signed by a CA.', 'The CA\'s public key is used to verify its signature on the certificate.'),
          ('Quantum key distribution can reveal an eavesdropper.', 'Observing a photon alters its polarisation.')],
   ['A digital certificate contains the owner\'s private key.', 'A digital signature encrypts the whole message with the receiver\'s private key.', 'Hashing can be reversed to obtain the original message.', 'Quantum cryptography uses radio waves.'])


def toy_hash(s, m):
    return sum(ord(c) for c in s) % m


@t7_3.add('C3', (2, 3, 4, 5), 'numerical')
def t7_3_verify(r, D):
    m = r.choice([97, 100, 101, 128])
    msg = r.choice(['PAY 500', 'SHIP 20', 'SEND 75', 'BUY 300', 'LOAN 90', 'MEET 10', 'OPEN 42', 'HOLD 15'])
    d = toy_hash(msg, m)
    tam = r.random() < 0.5
    rec = msg
    if tam:
        digits = [i for i, c in enumerate(msg) if c.isdigit()]
        i = r.choice(digits)
        rec = msg[:i] + str((int(msg[i]) + r.randrange(1, 9)) % 10) + msg[i + 1:]
    d2 = toy_hash(rec, m)
    if d2 == d:
        tam = False
        rec = msg
    codes = ' + '.join(str(ord(c)) for c in rec)
    stem = (f'A (simplified) hashing algorithm adds the ASCII codes of all characters in a message and takes the result MOD {m}. A message is received as "{rec}". Decrypting the attached digital signature with the sender\'s public key gives the digest {d}. '
            f'Calculate the hash of the received message (ASCII codes: {", ".join(f"{c!r} = {ord(c)}" for c in rec)}) and state what the receiver concludes.')
    s = sum(ord(c) for c in rec)
    concl = 'the digests match, so the message is authentic and unaltered' if not tam else 'the digests differ, so the message has been altered (or was not signed by the sender)'
    return Q(stem, f'{s} MOD {m} = {d2}; {concl}', f'sum {s} [1]; hash {d2} [1]; conclusion [1] [3]', marks=3)


@t7_3.add('C3', (1, 2, 3, 4))
def t7_3_steps(r, D):
    steps = ['The sender hashes the message to produce a digest', 'The sender encrypts the digest with the sender\'s private key to form the signature',
             'The message and the signature are sent', 'The receiver decrypts the signature using the sender\'s public key',
             'The receiver hashes the received message', 'The receiver compares the two digests']
    if D == 1:
        i = r.randrange(len(steps) - 1)
        return MCQ(r, f'In the digital signature process, which step comes immediately after: "{steps[i]}"?', steps[i + 1], [s for j, s in enumerate(steps) if j not in (i, i + 1)][:4], 'Order: ' + ' → '.join(steps) + '.')
    k = 4 if D <= 2 else 6
    sel = steps[:k] if k == 6 else [steps[0], steps[1], steps[3], steps[5]]
    shuf = sel[:]
    while shuf == sel:
        r.shuffle(shuf)
    lab = {s: 'ABCDEF'[i] for i, s in enumerate(shuf)}
    ans = ', '.join(lab[s] for s in sel)
    return Q('The statements describe how a digital signature is created and checked. ' + ' '.join(f'{"ABCDEF"[i]}: {s}.' for i, s in enumerate(shuf)) + ' Put them in the correct order.', ans, f'{ans} [{k // 2}]', marks=k // 2)


@t7_3.add('C3', (1, 2, 3))
def t7_3_cert(r, D):
    inc = ['the name of the certificate owner', 'the owner\'s public key', 'the serial number of the certificate', 'the dates between which the certificate is valid', 'the name of the certificate authority', 'the CA\'s digital signature']
    exc = ['the owner\'s private key', 'the session key', 'the user\'s password', 'the owner\'s credit card number', 'the CA\'s private key']
    d = ctx(r)
    if D == 1:
        x = r.choice(exc)
        return MCQ(r, f'{d["org"]} obtains a digital certificate. Which item would NOT be included in it?', x[0].upper() + x[1:], [s[0].upper() + s[1:] for s in r.sample(inc, 3)], f'A certificate never contains {x}; it contains public information such as {", ".join(inc[:3])}.')
    return Q(f'{d["org"]} in {d["city"]} applies for a digital certificate for its website. Describe how the certificate is obtained and identify three items it contains.',
             'The organisation sends its public key and proof of identity to a CA; the CA checks the identity, creates the certificate and signs it with the CA\'s private key. Contents: ' + '; '.join(r.sample(inc, 3)) + '.',
             '1 mark apply to CA with public key; 1 mark CA verifies and signs; 1 mark three items [3]', marks=3)


scen(t7_3, 'C4', (3, 4, 5), [
    '{org} in {city} sends contracts electronically to its suppliers.', '{p} must prove that software updates released by {org} are genuine.',
], [('Describe how a digital signature is produced for the document.', 'Hash the document to give a digest; encrypt the digest with the sender\'s private key; attach to the document.', '1 mark per point [3]'),
    ('Describe how the recipient checks the digital signature.', 'Decrypt the signature with the sender\'s public key; hash the received document; compare digests; match = authentic and unaltered.', '1 mark per point, max 3 [3]'),
    ('Explain why the recipient needs the sender\'s digital certificate.', 'To obtain the sender\'s public key and be sure it really belongs to the sender (vouched for by a CA).', '1 mark each [2]'),
    ('Explain how quantum cryptography could improve the security of key exchange.', 'Key sent as polarised photons; any eavesdropping changes the photons and is detected, so a secure key can be guaranteed.', '1 mark each [2]')], k=(3, 4))
essay(t7_3, [('whether {org} should invest in quantum cryptography to protect the transfer of encryption keys', 'eavesdropping is detectable; theoretically unbreakable key exchange; protects against future quantum computers breaking public-key methods.',
              'very expensive; needs dedicated fibre and limited distance; technology still developing; current TLS is adequate for most data.', 'worthwhile only for highly sensitive, long-lived data; otherwise strong conventional cryptography suffices.')],
      ['{org} in {city} handles very sensitive financial data.', '{p} is the security manager at {org}.'])

CHAPTERS[7] = [t7_1, t7_2, t7_3]

# =============================================================================== Chapter 8 Artificial intelligence
NODES = 'ABCDEFG'


def rand_graph(r, n):
    nodes = list(NODES[:n])
    for _ in range(100):
        edges = {}
        order = nodes[:]
        for i in range(1, n):
            j = r.randrange(i)
            edges[tuple(sorted((order[i], order[j])))] = r.randrange(2, 13)
        extra = r.randrange(n - 1, n + 2)
        for _ in range(extra):
            a, c = r.sample(nodes, 2)
            edges.setdefault(tuple(sorted((a, c))), r.randrange(2, 13))
        if ('A', nodes[-1]) in edges:
            del edges[('A', nodes[-1])]
        dist, prev, cnt = dijkstra(nodes, edges, 'A')
        if dist[nodes[-1]] < 10 ** 9 and all(cnt[x] == 1 for x in nodes) and len(path_to(prev, nodes[-1])) >= 3:
            return nodes, edges
    return None


def adj(edges):
    g = {}
    for (a, c), w in edges.items():
        g.setdefault(a, []).append((c, w))
        g.setdefault(c, []).append((a, w))
    return g


def dijkstra(nodes, edges, s):
    g = adj(edges)
    dist = {x: 10 ** 9 for x in nodes}
    cnt = {x: 0 for x in nodes}
    prev = {}
    dist[s], cnt[s] = 0, 1
    pq = [(0, s)]
    done = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for v, w in g.get(u, []):
            if d + w < dist[v]:
                dist[v], prev[v], cnt[v] = d + w, u, cnt[u]
                heapq.heappush(pq, (dist[v], v))
            elif d + w == dist[v]:
                cnt[v] += cnt[u]
    return dist, prev, cnt


def path_to(prev, t):
    p = [t]
    while p[-1] in prev:
        p.append(prev[p[-1]])
    return p[::-1]


def edges_text(edges):
    return ', '.join(f'{a}–{c} {w}' for (a, c), w in sorted(edges.items()))


t8_1 = topic("Graphs as a data structure for AI; Dijkstra's and A* search algorithms", 'graphs as a data structure for ai', "dijkstra's and a* search algorithms")
t8_1.fixed('C1', (1, 2), [
    ('What does a weighted graph consist of?', 'Nodes (vertices) joined by edges that have a value (weight) such as distance or cost', 'Used in AI to model maps, networks and states.', ['A list of values in order', 'A tree with a single root only', 'A table of records']),
    ("What does Dijkstra's algorithm find?", 'The shortest path from a start node to every other node in a weighted graph', 'It repeatedly visits the unvisited node with the smallest known distance.', ['The longest path', 'A path that visits every node once', 'The minimum number of edges']),
    ('How does A* differ from Dijkstra\'s algorithm?', 'It adds a heuristic estimate of the remaining distance to the goal to choose which node to explore', 'f(n) = g(n) + h(n).', ['It ignores the edge weights', 'It always explores every node', 'It only works on unweighted graphs']),
    ('In A*, what does g(n) represent?', 'The actual cost of the path from the start node to node n', 'h(n) is the heuristic estimate from n to the goal.', ['The estimated cost from n to the goal', 'The number of edges from n', 'The total number of nodes']),
    ('What is a heuristic?', 'A rule of thumb that gives an estimate to guide a search', 'e.g. straight-line distance to the goal.', ['An exact calculation of the shortest path', 'A type of graph', 'A sorting algorithm']),
    ('Why is a graph a suitable data structure for AI route planning?', 'Locations can be nodes and routes edges with weights for distance or time', 'Search algorithms can then find optimal routes.', ['Graphs store data in sorted order', 'Graphs use less memory than arrays', 'Graphs cannot contain cycles']),
])
t8_1.fixed('C2', (2, 3, 4), [
    ('Explain why A* usually explores fewer nodes than Dijkstra\'s algorithm.', 'The heuristic guides the search towards the goal, so nodes that lead away from the goal are less likely to be expanded.', '1 mark each [2]'),
    ('Explain why the heuristic used by A* must not overestimate the remaining distance.', 'If it overestimates, a shorter path may be ignored, so A* may not return the optimal (shortest) path.', '1 mark each [2]'),
])
ar(t8_1, [("Dijkstra's algorithm finds the shortest path when all weights are non-negative.", 'Once a node has the smallest tentative distance it cannot be reached more cheaply.'),
          ('A* can find a route faster than Dijkstra\'s algorithm.', 'A heuristic directs the search towards the goal.'),
          ('A sat-nav can use a graph to plan journeys.', 'Junctions are represented as nodes and roads as weighted edges.')],
   ["Dijkstra's algorithm always visits the node with the largest distance next.", 'A* does not use edge weights.', 'A heuristic always gives the exact remaining distance.'])


@t8_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_1_dijk(r, D):
    n = 5 if D <= 3 else (6 if D == 4 else 7)
    g = rand_graph(r, n)
    if not g:
        return None
    nodes, edges = g
    dist, prev, _ = dijkstra(nodes, edges, 'A')
    t = nodes[-1]
    p = path_to(prev, t)
    d = ctx(r)
    stem = f'A delivery robot at {d["org"]} moves between locations A to {t}. The graph has the edges (with times in seconds): {edges_text(edges)}. '
    if D == 1:
        return MCQ(r, stem + f'What is the length of the shortest path from A to {t}?', str(dist[t]), [str(dist[t] + 1), str(dist[t] + 3), str(sum(edges.values()) // 2), str(max(dist[t] - 2, 1))], f'Shortest path {"-".join(p)} = {dist[t]}.')
    if D <= 3:
        return Q(stem + f"Use Dijkstra's algorithm to find the shortest path from A to {t} and its length.", f'{"–".join(p)}, {dist[t]} s', f'path {"–".join(p)} [1]; length {dist[t]} [1]; working shown [1] [3]', marks=3)
    tab = ', '.join(f'{x} = {dist[x]}' for x in nodes)
    return Q(stem + f"Use Dijkstra's algorithm to find the shortest distance from A to every node, and state the shortest path from A to {t}.", f'{tab}; path {"–".join(p)}',
             f'final distances {tab} [{n - 2}]; path [1] [{n - 1}]', marks=n - 1)


@t8_1.add('C3', (3, 4, 5), 'numerical')
def t8_1_astar(r, D):
    n = 5 if D == 3 else 6
    g = rand_graph(r, n)
    if not g:
        return None
    nodes, edges = g
    t = nodes[-1]
    dt, _, _ = dijkstra(nodes, edges, t)
    h = {x: int(dt[x] * r.uniform(0.6, 1.0)) for x in nodes}
    h[t] = 0
    gA = adj(edges)
    nb = sorted(gA['A'])
    fvals = ', '.join(f'{v}: g = {w}, h = {h[v]}, f = {w + h[v]}' for v, w in nb)
    best = min(nb, key=lambda x: (x[1] + h[x[0]], x[0]))
    ties = [v for v, w in nb if w + h[v] == best[1] + h[best[0]]]
    if len(ties) > 1:
        return None
    dist, prev, _ = dijkstra(nodes, edges, 'A')
    p = path_to(prev, t)
    stem = (f'A* search is used to find the shortest route from A to {t} in a graph with edges {edges_text(edges)}. The heuristic values h(n) are ' + ', '.join(f'{x} = {h[x]}' for x in nodes) +
            f'. (a) Calculate f(n) for each neighbour of A. (b) State which node is expanded next. (c) Give the shortest path from A to {t} and its cost.')
    return Q(stem, f'(a) {fvals} (b) {best[0]} (c) {"–".join(p)}, cost {dist[t]}', f'(a) f = g + h for each neighbour [2] (b) lowest f: {best[0]} [1] (c) path and cost [2] [5]', marks=5, typ='multi_step')


scen(t8_1, 'C4', (3, 4, 5), [
    'A navigation app developed in {city} plans routes between landmarks.', '{p} is programming a game character that must find its way around a map for {org}.',
], [lambda r, d: (lambda g: (f'The map is a graph with edges {edges_text(g[1])}. Use Dijkstra\'s algorithm to find the shortest path from A to {g[0][-1]}.',
                             (lambda dd: f'{"–".join(path_to(dd[1], g[0][-1]))}, {dd[0][g[0][-1]]}')(dijkstra(g[0], g[1], 'A')), '1 mark path; 1 mark length; 1 mark working [3]') if g else None)(rand_graph(r, 5)),
    ('Explain how A* uses a heuristic to improve the search.', 'Chooses node with lowest f = g + h; h estimates distance to goal (e.g. straight line), so search heads towards goal, expanding fewer nodes.', '1 mark per point, max 3 [3]'),
    ('Explain why a graph is a suitable way to represent the map.', 'Locations as nodes, paths as edges with weights (distance/time); algorithms can then compute optimal routes.', '1 mark each [2]'),
    ('Suggest a suitable heuristic and explain why it is admissible.', 'Straight-line (Euclidean) distance: a path along edges can never be shorter than a straight line, so it never overestimates.', '1 mark heuristic; 1 mark reason [2]')], k=(3, 4))

ML = [('a bank trains a model on past transactions labelled "fraud" or "genuine" to flag new fraudulent payments', 'supervised'),
      ('an email service learns to classify messages as spam using thousands of emails already marked as spam or not spam', 'supervised'),
      ('a shop groups its customers into segments by purchasing behaviour without any predefined categories', 'unsupervised'),
      ('a robot learns to walk by receiving a reward each time it moves forward without falling', 'reinforcement'),
      ('a program predicts house prices from the sizes and locations of houses whose sale prices are known', 'supervised'),
      ('a streaming service finds clusters of films that are watched by similar viewers', 'unsupervised'),
      ('a game-playing AI improves by playing millions of games against itself and being rewarded for wins', 'reinforcement'),
      ('a hospital system learns to recognise tumours from X-ray images labelled by doctors', 'supervised'),
      ('a network monitor detects unusual traffic patterns without being told what an attack looks like', 'unsupervised'),
      ('a self-driving car simulator rewards the car for staying in lane and penalises collisions', 'reinforcement'),
      ('a translation system is trained on millions of sentence pairs in two languages', 'supervised'),
      ('a warehouse robot learns the quickest route to pick items through trial and error with a score for speed', 'reinforcement')]
t8_2 = topic('Machine learning: supervised, unsupervised and reinforcement learning', 'machine learning', 'supervised, unsupervised and reinforcement learning')
t8_2.fixed('C1', (1, 2), [
    ('What is machine learning?', 'A branch of AI in which a system learns from data and improves its performance without being explicitly programmed for every case', 'Models are trained on data.', ['Programming every rule by hand', 'A type of computer hardware', 'Storing large amounts of data']),
    ('Supervised learning uses which kind of training data?', 'Labelled data, where the correct output is known for each input', 'The model learns to map inputs to the given labels.', ['Unlabelled data', 'Rewards and penalties only', 'No data at all']),
    ('Unsupervised learning is used to', 'find patterns or groups (clusters) in unlabelled data', 'e.g. customer segmentation.', ['predict labels from labelled data', 'maximise a reward', 'sort data into alphabetical order']),
    ('In reinforcement learning, how does the agent learn?', 'By trial and error, receiving rewards or penalties for its actions', 'It learns a policy that maximises total reward.', ['From labelled examples', 'By clustering data', 'From rules written by an expert']),
    ('Which is an example of supervised learning?', 'Training a model with images labelled "cat" or "dog"', 'Labels are supplied with the training data.', ['Grouping news articles by topic with no labels', 'A robot learning to balance through rewards', 'Sorting a list into order']),
])
t8_2.fixed('C2', (2, 3, 4), [
    ('Explain the difference between supervised and unsupervised learning.', 'Supervised learning is trained on labelled data with known outputs to predict labels; unsupervised learning finds patterns/clusters in unlabelled data.', '1 mark each [2]'),
    ('Explain why a large amount of training data is needed in machine learning.', 'More (representative) examples let the model generalise to new data and reduce errors/overfitting.', '1 mark each [2]'),
])
ar(t8_2, [('Supervised learning needs labelled data.', 'The model is told the correct output for each training example.'),
          ('Reinforcement learning suits game-playing AI.', 'The agent can be rewarded for winning and learn from trial and error.'),
          ('Unsupervised learning can discover groups of similar customers.', 'It looks for patterns in data without labels.')],
   ['Unsupervised learning requires every example to be labelled.', 'Reinforcement learning uses no feedback.', 'Machine learning systems never make mistakes.'])


@t8_2.add('C3', (1, 2, 3, 4))
def t8_2_type(r, D):
    s, t = r.choice(ML)
    if D <= 2:
        return MCQ(r, f'Which type of machine learning is used when {s}?', t.capitalize() + ' learning', ['Supervised learning', 'Unsupervised learning', 'Reinforcement learning', 'Rule-based expert system'], f'{t}: ' + {'supervised': 'labelled training data', 'unsupervised': 'no labels, finds patterns', 'reinforcement': 'rewards and penalties'}[t] + '.')
    why = {'supervised': 'the training data is labelled with the correct output', 'unsupervised': 'there are no labels; the system finds patterns/clusters itself', 'reinforcement': 'the system learns by trial and error from rewards and penalties'}[t]
    return Q(f'Identify the type of machine learning used when {s}. Justify your answer.', f'{t.capitalize()} learning: {why}.', '1 mark type; 1 mark justification [2]', marks=2)


@t8_2.add('C3', (3, 4, 5), 'numerical')
def t8_2_acc(r, D):
    tp, fn, fp, tn = r.randrange(30, 90), r.randrange(2, 20), r.randrange(2, 20), r.randrange(50, 200)
    tot = tp + fn + fp + tn
    acc = (tp + tn) / tot * 100
    d = ctx(r)
    return Q(f'{d["org"]} tests a supervised learning model on {tot} labelled examples. It correctly identifies {tp} positive and {tn} negative cases; it misses {fn} positive cases and wrongly flags {fp} negative cases as positive. Calculate the accuracy as a percentage and explain why more training data might improve it.',
             f'{tp + tn} ÷ {tot} × 100 = {acc:.1f}%; more varied labelled data helps the model generalise to new cases.', f'correct = {tp + tn} [1]; accuracy {acc:.1f}% [1]; explanation [1] [3]', marks=3)


scen(t8_2, 'C4', (3, 4, 5), [
    '{org} in {city} wants to use machine learning to improve its services.', '{p} is a data scientist at {org}.',
], [lambda r, d: (lambda x: (f'Identify the type of machine learning used if {x[0]}, and justify it.', x[1].capitalize() + ' learning', '1 mark type; 1 mark justification [2]'))(r.choice(ML)),
    ('Describe how a supervised learning model is trained and tested.', 'Labelled data split into training and test sets; model learns from training data; accuracy measured on unseen test data; adjust and repeat.', '1 mark per point, max 3 [3]'),
    ('Explain one ethical issue of using machine learning in this way.', 'Bias in training data may lead to unfair decisions; lack of transparency about how decisions are made; privacy of personal data.', '1 mark issue; 1 mark explanation [2]'),
    ('Compare reinforcement learning with supervised learning.', 'Reinforcement: no labelled data, learns from rewards through trial and error; supervised: learns from labelled examples.', '1 mark each [2]')], k=(3, 4))
essay(t8_2, [('the use of machine learning by {org} to make decisions about its customers', 'fast, consistent decisions on large data; can find patterns humans miss; improves over time.',
              'bias in training data; decisions hard to explain; privacy concerns; need for large labelled data sets; errors may harm individuals.', 'use with human oversight, transparent models and audited data.')],
      ['{org} in {city} wants to automate some decisions.', '{p} is advising {org} on AI.'])

t8_3 = topic('Deep learning and artificial neural networks; back propagation and regression', 'deep learning', 'artificial neural networks', 'back propagation', 'regression')
t8_3.fixed('C1', (1, 2), [
    ('What is an artificial neural network?', 'A network of connected nodes (neurons) in layers, with weighted connections, modelled on the brain', 'Input layer, hidden layer(s), output layer.', ['A network of computers in a LAN', 'A database of facts', 'A type of search algorithm']),
    ('What makes a neural network "deep"?', 'It has many hidden layers', 'Deep learning uses many hidden layers to learn complex features.', ['It uses very large weights', 'It has only one output', 'It is trained without data']),
    ('What is back propagation?', 'Sending the error at the output back through the network to adjust the weights', 'Weights are adjusted to reduce the error between predicted and actual outputs.', ['Passing inputs forward through the network', 'Removing hidden layers', 'Sorting the training data']),
    ('What is regression in machine learning?', 'Predicting a continuous numerical value from input data', 'e.g. predicting a house price; the line/curve of best fit.', ['Sorting items into categories', 'Removing errors from data', 'Reversing a calculation']),
    ('In a neural network, what is a weight?', 'A value that sets the strength of the connection between two neurons', 'Training adjusts the weights.', ['The number of neurons', 'The output value', 'The size of the data set']),
])
t8_3.fixed('C2', (2, 3, 4), [
    ('Explain how a neural network learns using back propagation.', 'Inputs pass forward to give an output; the error (actual − expected) is calculated; the error is propagated back and weights adjusted to reduce it; repeated over many examples.', '1 mark per point, max 3 [3]'),
    ('Explain why deep learning needs large amounts of data and processing power.', 'Many layers and weights must be adjusted; many examples are needed to learn features without overfitting; training uses many calculations (GPUs).', '1 mark each [2]'),
])
ar(t8_3, [('Back propagation reduces the error of a neural network.', 'The weights are adjusted in proportion to their contribution to the error.'),
          ('Deep learning can recognise complex patterns such as faces.', 'Its many hidden layers learn increasingly abstract features.'),
          ('Regression can predict a price.', 'It models the relationship between inputs and a continuous output value.')],
   ['A neural network with no hidden layers is a deep network.', 'Back propagation passes the inputs forward through the network.', 'Regression only outputs categories.'])


@t8_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_3_neuron(r, D):
    n = 2 if D <= 2 else 3
    xs = [r.randrange(0, 2) if D <= 3 else round(r.uniform(0, 1), 1) for _ in range(n)]
    ws = [round(r.choice([-1, 1]) * r.uniform(0.1, 0.9), 1) for _ in range(n)]
    bias = round(r.uniform(-0.5, 0.5), 1)
    th = 0
    s = sum(x * w for x, w in zip(xs, ws)) + bias
    s = round(s, 2)
    if abs(s) < 0.005:
        return None
    out = 1 if s >= th else 0
    terms = ' + '.join(f'({x} × {w})' for x, w in zip(xs, ws)) + f' + ({bias})'
    stem = f'A neuron has inputs {", ".join(f"x{i + 1} = {x}" for i, x in enumerate(xs))}, weights {", ".join(f"w{i + 1} = {w}" for i, w in enumerate(ws))} and bias {bias}. It uses a step activation function: output 1 if the weighted sum is at least 0, otherwise 0.'
    if D == 1:
        return MCQ(r, stem + ' What is the weighted sum (including the bias)?', f'{s:g}', [f'{round(s - bias, 2):g}', f'{round(-s, 2):g}', f'{round(s + 1, 2):g}', f'{round(sum(ws), 2):g}'], f'{terms} = {s:g}.')
    return Q(stem + ' Calculate the weighted sum and the output of the neuron.', f'sum = {s:g}; output = {out}', f'{terms} = {s:g} [1]; output {out} [1] [2]', marks=2)


@t8_3.add('C3', (3, 4, 5), 'numerical')
def t8_3_update(r, D):
    lr = r.choice([0.1, 0.2, 0.5])
    x = [r.randrange(0, 2) for _ in range(2)]
    if not any(x):
        x[0] = 1
    w = [round(r.uniform(-0.8, 0.8), 1) for _ in range(2)]
    s = round(sum(a * c for a, c in zip(x, w)), 2)
    out = 1 if s >= 0 else 0
    target = 1 - out
    err = target - out
    nw = [round(c + lr * err * a, 2) for a, c in zip(x, w)]
    stem = (f'A perceptron with no bias has inputs x1 = {x[0]}, x2 = {x[1]} and weights w1 = {w[0]}, w2 = {w[1]}; output 1 if the weighted sum ≥ 0, else 0. The target output is {target}. '
            f'Using the rule w ← w + η × (target − output) × x with learning rate η = {lr}, calculate the output, the error and the new weights.')
    return Q(stem, f'sum {s:g} → output {out}; error {err}; new w1 = {nw[0]:g}, w2 = {nw[1]:g}', f'output {out} [1]; error {target} − {out} = {err} [1]; new weights {nw[0]:g}, {nw[1]:g} [2] [4]', marks=4)


@t8_3.add('C3', (3, 4, 5), 'numerical')
def t8_3_reg(r, D):
    for _ in range(30):
        m = r.choice([2, 3, 4, 5, 0.5, 1.5])
        c = r.randrange(1, 20)
        xs = sorted(r.sample(range(1, 11), 4 if D < 5 else 5))
        ys = [round(m * x + c + r.choice([-1, 0, 1])) for x in xs]
        n = len(xs)
        mx, my = Fraction(sum(xs), n), Fraction(sum(ys), n)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs)
        if sxx == 0:
            continue
        slope = sxy / sxx
        icpt = my - slope * mx
        px = r.randrange(11, 16)
        pred = slope * px + icpt
        d = ctx(r)
        stem = (f'{d["org"]} records advertising spend x (thousands) and sales y (hundreds): ' + ', '.join(f'({x}, {y})' for x, y in zip(xs, ys)) +
                f'. Linear regression gives the line of best fit y = mx + c with m = Σ(x − x̄)(y − ȳ) ÷ Σ(x − x̄)² and c = ȳ − m·x̄. Calculate m and c to 2 decimal places and predict y when x = {px}.')
        return Q(stem, f'm = {float(slope):.2f}, c = {float(icpt):.2f}; prediction {float(pred):.2f}', f'x̄ = {float(mx):.2f}, ȳ = {float(my):.2f} [1]; m = {float(sxy):.2f} ÷ {float(sxx):.2f} = {float(slope):.2f} [1]; c = {float(icpt):.2f} [1]; y = {float(pred):.2f} [1] [4]', marks=4)
    return None


scen(t8_3, 'C4', (3, 4, 5), [
    '{org} in {city} is developing a deep learning system to recognise products from photographs.', '{p} is training an artificial neural network at {org} to predict energy demand.',
], [('Describe the structure of an artificial neural network.', 'Input layer, one or more hidden layers, output layer; neurons connected by weighted links; activation functions.', '1 mark per point, max 3 [3]'),
    ('Explain how back propagation is used during training.', 'Output compared with expected value; error fed backwards through the layers; weights adjusted (gradient descent) to reduce error; repeated.', '1 mark per point, max 3 [3]'),
    lambda r, d: (lambda q: (q['stem'].split(' It uses')[0] + '. Using a step function (output 1 if sum ≥ 0), calculate the output.', q['answer'], q['key']) if q else None)(t8_3_neuron(r, 3)),
    ('Explain why this task is suitable for deep learning rather than a rule-based program.', 'Patterns are too complex to write as rules; deep networks learn features from large amounts of example data.', '1 mark each [2]')], k=(3, 4))

CHAPTERS[8] = [t8_1, t8_2, t8_3]

# =============================================================================== Chapter 9 Abstract data types
t9_1 = topic('Implementing stacks and queues (including circular queues) using arrays', 'implementing stacks and queues', 'circular queues', 'using arrays')
t9_1.fixed('C1', (1, 2), [
    ('In an array implementation of a stack, what does the top of stack pointer hold?', 'The index of the item most recently pushed', 'Push: increment pointer then store; pop: read then decrement.', ['The index of the first item pushed', 'The number of free spaces', 'The value of the top item']),
    ('Why is a circular queue used instead of a linear queue in an array?', 'Spaces freed at the front can be reused when the rear pointer wraps around', 'Rear ← (Rear + 1) MOD Size.', ['It allows items to be removed from the rear', 'It keeps the items sorted', 'It needs no pointers']),
    ('What error occurs when an item is pushed onto a full stack?', 'Stack overflow', 'Popping from an empty stack is stack underflow.', ['Stack underflow', 'Queue full', 'Null pointer']),
    ('In a circular queue of size 8 (indices 0 to 7), the rear pointer is 7. Where is the next item added?', 'Index 0', '(7 + 1) MOD 8 = 0, if the queue is not full.', ['Index 8', 'Index 7', 'Index 1']),
    ('Which variable makes it easy to tell whether a circular queue is full or empty?', 'A count of the number of items in the queue', 'Full when NumberOfItems = Size; empty when 0.', ['The value of the front item', 'The size of each item', 'A flag set when the program starts']),
    ('Items are removed from a queue at the', 'front', 'Queue: FIFO; added at rear, removed at front.', ['rear', 'middle', 'top']),
])
t9_1.fixed('C2', (2, 3, 4), [
    ('Explain why a linear queue implemented in an array can report that it is full even when it has empty spaces.', 'Dequeued items leave spaces at the front, but the rear pointer has reached the end of the array, so no more items can be added unless the queue wraps around (circular) or items are shuffled.', '1 mark each [2]'),
    ('Explain the purpose of the MOD operator when updating the pointers of a circular queue.', 'When a pointer reaches the last index, (Pointer + 1) MOD Size returns it to index 0, so the array is used circularly.', '1 mark each [2]'),
])
ar(t9_1, [('A circular queue makes better use of its array than a linear queue.', 'Positions freed at the front of the array can be reused.'),
          ('Popping from an empty stack must be prevented.', 'There is no item at the top to return (stack underflow).'),
          ('A stack is suitable for reversing the order of items.', 'The last item pushed is the first item popped.')],
   ['Items are removed from the rear of a queue.', 'A stack is first in, first out.', 'A circular queue never becomes full.'])


def cq_sim(r, size, D):
    arr = [None] * size
    front, rear, n = 0, -1, 0
    ops, log = [], []
    k = 6 if D <= 3 else 9
    pre = r.randrange(1, size)
    for _ in range(pre):
        v = r.randrange(10, 99)
        rear = (rear + 1) % size
        arr[rear] = v
        n += 1
    for _ in range(r.randrange(pre)):
        front = (front + 1) % size
        n -= 1
    start = (front, rear, n, [arr[(front + i) % size] for i in range(n)], arr[:])
    for _ in range(k):
        if r.random() < 0.55:
            v = r.randrange(10, 99)
            ops.append(f'Enqueue({v})')
            if n == size:
                log.append('queue full')
            else:
                rear = (rear + 1) % size
                arr[rear] = v
                n += 1
        else:
            ops.append('Dequeue()')
            if n == 0:
                log.append('queue empty')
            else:
                log.append(str(arr[front]))
                front = (front + 1) % size
                n -= 1
    return start, ops, log, (front, rear, n, [arr[(front + i) % size] for i in range(n)])


@t9_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_1_cq(r, D):
    size = 5 if D <= 3 else 6
    start, ops, log, end = cq_sim(r, size, D)
    f0, r0, n0, items0, arr0 = start
    state = ', '.join(f'[{i}] {"" if v is None else v}'.rstrip() for i, v in enumerate(arr0))
    stem = (f'A circular queue is stored in a 1D array Queue of {size} elements (indices 0 to {size - 1}). Currently FrontPointer = {f0}, RearPointer = {r0} and NumberOfItems = {n0}; the array holds {state}. '
            f'Enqueue adds at (RearPointer + 1) MOD {size} if the queue is not full; Dequeue returns the item at FrontPointer and then FrontPointer ← (FrontPointer + 1) MOD {size}. ')
    if D == 1:
        ops, log, end = ops[:3], None, None
        f, rr, n = f0, r0, n0
        for op in ops:
            if op.startswith('Enq') and n < size:
                rr, n = (rr + 1) % size, n + 1
            elif op.startswith('Deq') and n:
                f, n = (f + 1) % size, n - 1
        return MCQ(r, stem + f'The operations {", ".join(ops)} are carried out. What is the value of RearPointer afterwards?', str(rr), [str((rr + 1) % size), str(rr + 1), str(f), str((rr - 1) % size)], f'Each successful enqueue moves RearPointer on by 1 MOD {size}: RearPointer = {rr}.')
    stem += f'The operations {", ".join(ops)} are carried out in order. State the output of each Dequeue (or error message), and the final values of FrontPointer, RearPointer and NumberOfItems.'
    outs = [x for x in log]
    ans = f'outputs/messages: {", ".join(outs) or "none"}; FrontPointer = {end[0]}, RearPointer = {end[1]}, NumberOfItems = {end[2]} (queue front to rear: {", ".join(map(str, end[3])) or "empty"})'
    m = 4 if D <= 3 else 5
    return Q(stem, ans, f'dequeued values/messages [{m - 3}]; FrontPointer [1]; RearPointer [1]; NumberOfItems [1] [{m}]', marks=m)


@t9_1.add('C3', (2, 3, 4, 5), 'numerical')
def t9_1_stack(r, D):
    size = r.choice([5, 6, 8])
    st, ops, outs = [], [], []
    for _ in range(r.randrange(6, 9) if D <= 3 else r.randrange(9, 12)):
        if r.random() < 0.4:
            ops.append('Pop()')
            outs.append(str(st.pop()) if st else 'underflow')
        else:
            v = r.choice(['"' + x + '"' for x in ['Red', 'Blue', 'Gold', 'Pink', 'Grey', 'Teal', 'Lime', 'Navy']]) if D == 5 else str(r.randrange(1, 60))
            ops.append(f'Push({v})')
            if len(st) == size:
                outs.append('overflow')
            else:
                st.append(v)
    top = len(st) - 1
    return Q(f'A stack is implemented with an array Stack[0:{size - 1}] and a pointer TopOfStack initialised to −1. Push increments TopOfStack then stores the item; Pop returns Stack[TopOfStack] then decrements TopOfStack. Errors are reported as "overflow" or "underflow". '
             f'The operations {", ".join(ops)} are carried out. State the values returned by Pop (and any errors), the final value of TopOfStack and the final contents of the stack from bottom to top.',
             f'returned: {", ".join(outs) or "none"}; TopOfStack = {top}; stack: {", ".join(st) or "empty"}', f'popped values [2]; TopOfStack {top} [1]; contents [1] [4]', marks=4)


ERRS_Q = [
    (['PROCEDURE Enqueue(Item : INTEGER)', f'{IND}IF NumberOfItems = QueueSize THEN', f'{IND}{IND}OUTPUT "Queue full"', f'{IND}ELSE', f'{IND}{IND}RearPointer ← RearPointer + 1', f'{IND}{IND}Queue[RearPointer] ← Item', f'{IND}{IND}NumberOfItems ← NumberOfItems + 1', f'{IND}ENDIF', 'ENDPROCEDURE'],
     'RearPointer ← RearPointer + 1 does not wrap round: it should be RearPointer ← (RearPointer + 1) MOD QueueSize', 'RearPointer goes beyond the last index (array out of bounds) instead of returning to 0'),
    (['FUNCTION Pop() RETURNS INTEGER', f'{IND}DECLARE Item : INTEGER', f'{IND}TopOfStack ← TopOfStack - 1', f'{IND}Item ← Stack[TopOfStack]', f'{IND}RETURN Item', 'ENDFUNCTION'],
     'TopOfStack is decremented before the item is read, so the wrong item is returned (and no underflow check); read Stack[TopOfStack] first, then decrement', 'The item below the top is returned and the top item is lost'),
    (['PROCEDURE Push(Item : INTEGER)', f'{IND}IF TopOfStack = 0 THEN', f'{IND}{IND}OUTPUT "Stack full"', f'{IND}ELSE', f'{IND}{IND}TopOfStack ← TopOfStack + 1', f'{IND}{IND}Stack[TopOfStack] ← Item', f'{IND}ENDIF', 'ENDPROCEDURE'],
     'The full test is wrong: it should be IF TopOfStack = MaxIndex (the last index of the array)', 'The stack would report full when it holds one item, and would overflow the array when full'),
    (['FUNCTION Dequeue() RETURNS INTEGER', f'{IND}DECLARE Item : INTEGER', f'{IND}Item ← Queue[FrontPointer]', f'{IND}FrontPointer ← (FrontPointer + 1) MOD QueueSize', f'{IND}RETURN Item', 'ENDFUNCTION'],
     'NumberOfItems is not decremented (and there is no check for an empty queue): add IF NumberOfItems = 0 ... and NumberOfItems ← NumberOfItems - 1', 'The queue would appear to hold more items than it does and could return items that were already removed'),
]


@t9_1.add('C2', (2, 3, 4), 'explain')
def t9_1_err(r, D):
    lines, fix, eff = r.choice(ERRS_Q)
    d = ctx(r)
    return Q(f'{d["p"]} has written this subroutine for an array-based ADT:\n' + code(lines) + '\nIdentify the error, explain its effect and give the correction.', f'{fix}. Effect: {eff}.', '1 mark error; 1 mark effect; 1 mark correction [3]', marks=3)


scen(t9_1, 'C4', (3, 4, 5), [
    'A print server at {org} in {city} stores print jobs in a circular queue.', '{p} is writing an undo feature for a drawing app developed in {city}, using a stack stored in an array.',
], [('Write pseudocode for a procedure Enqueue that adds an item to a circular queue of size 10, reporting when it is full.',
     code(['PROCEDURE Enqueue(Item : STRING)', f'{IND}IF NumberOfItems = 10 THEN', f'{IND}{IND}OUTPUT "Queue full"', f'{IND}ELSE', f'{IND}{IND}RearPointer ← (RearPointer + 1) MOD 10', f'{IND}{IND}Queue[RearPointer] ← Item', f'{IND}{IND}NumberOfItems ← NumberOfItems + 1', f'{IND}ENDIF', 'ENDPROCEDURE']),
     '1 mark full check; 1 mark pointer update with MOD; 1 mark store item; 1 mark increment count [4]'),
    ('Write pseudocode for a function Pop that returns the top item of a stack, or −1 if the stack is empty.',
     code(['FUNCTION Pop() RETURNS INTEGER', f'{IND}DECLARE Item : INTEGER', f'{IND}IF TopOfStack = -1 THEN', f'{IND}{IND}RETURN -1', f'{IND}ELSE', f'{IND}{IND}Item ← Stack[TopOfStack]', f'{IND}{IND}TopOfStack ← TopOfStack - 1', f'{IND}{IND}RETURN Item', f'{IND}ENDIF', 'ENDFUNCTION']),
     '1 mark empty check; 1 mark read item; 1 mark decrement; 1 mark return [4]'),
    ('Explain why a queue rather than a stack is suitable for print jobs.', 'Jobs should be printed in the order they arrive (FIFO); a stack would print the newest job first.', '1 mark each [2]'),
    ('Explain why a stack is suitable for an undo feature.', 'The most recent action must be undone first (LIFO).', '1 mark each [2]')], k=(2, 3))

t9_2 = topic('Linked lists: insertion, deletion and searching using pointers', 'linked lists', 'insertion, deletion and searching', 'using pointers')
t9_2.fixed('C1', (1, 2), [
    ('What does the start pointer of a linked list hold?', 'The index (address) of the first node in the list', 'A value of −1 (null) means the list is empty.', ['The number of nodes', 'The data in the last node', 'The next free node']),
    ('What is the purpose of the free list in an array-based linked list?', 'To link together the unused nodes so they can be allocated when inserting', 'The free pointer gives the first free node.', ['To store deleted data permanently', 'To keep the list sorted', 'To count the items']),
    ('How is the end of a linked list shown?', 'The last node has a null pointer', 'Often −1 or 0 in an array implementation.', ['The last node points to the first', 'The last node has no data', 'The start pointer is set to null']),
    ('Why does inserting into an ordered linked list not require existing items to be moved?', 'Only the pointers need to be changed', 'The new node can be stored in any free position.', ['Because the list is unordered', 'Because the array is always large enough', 'Because nodes are stored in order in memory']),
    ('When a node is deleted from an array-based linked list, what happens to it?', 'It is returned to the free list', 'The previous node\'s pointer is changed to skip it.', ['It is moved to the end of the list', 'The whole array is shifted', 'It is set to zero and left unused']),
])
t9_2.fixed('C2', (2, 3, 4), [
    ('Explain the advantage of a linked list over an array for a list that changes often.', 'Items can be inserted and deleted by changing pointers only, without moving other items; the list can grow/shrink dynamically.', '1 mark each [2]'),
    ('Explain why a linked list cannot be searched with a binary search.', 'Nodes can only be accessed by following pointers from the start; there is no direct access to the middle item.', '1 mark each [2]'),
])
ar(t9_2, [('Deleting from a linked list does not require items to be moved.', 'The pointer of the previous node is changed to bypass the deleted node.'),
          ('Searching a linked list is a linear process.', 'Each node can only be reached from the node before it.'),
          ('An array-based linked list needs a free list.', 'Unused nodes must be tracked so they can be allocated to new items.')],
   ['A linked list allows direct access to the middle node.', 'Inserting into a linked list always requires every item to be moved.', 'The last node of a linked list points to the start pointer.'])

LL_WORDS = ['Ant', 'Bee', 'Cat', 'Dog', 'Eel', 'Fox', 'Gnu', 'Hen', 'Ibis', 'Jay', 'Kiwi', 'Lynx', 'Mole', 'Newt', 'Owl', 'Puma', 'Quail', 'Rat', 'Seal', 'Toad', 'Vole', 'Wren', 'Yak', 'Zebu']


def ll_build(r, size, n):
    words = sorted(r.sample(LL_WORDS, n))
    slots = r.sample(range(size), size)
    used, free = slots[:n], slots[n:]
    data = [''] * size
    ptr = [-1] * size
    for i, w in enumerate(words):
        data[used[i]] = w
        ptr[used[i]] = used[i + 1] if i + 1 < n else -1
    for i, f in enumerate(free):
        ptr[f] = free[i + 1] if i + 1 < len(free) else -1
    return data, ptr, used[0] if n else -1, free[0] if free else -1


def ll_list(data, ptr, start):
    out, p = [], start
    while p != -1:
        out.append(data[p])
        p = ptr[p]
    return out


def ll_insert(data, ptr, start, free, w):
    if free == -1:
        return start, free, False
    new = free
    free = ptr[free]
    data[new] = w
    prev, cur = -1, start
    while cur != -1 and data[cur] < w:
        prev, cur = cur, ptr[cur]
    ptr[new] = cur
    if prev == -1:
        start = new
    else:
        ptr[prev] = new
    return start, free, True


def ll_delete(data, ptr, start, free, w):
    prev, cur = -1, start
    while cur != -1 and data[cur] != w:
        prev, cur = cur, ptr[cur]
    if cur == -1:
        return start, free, False
    if prev == -1:
        start = ptr[cur]
    else:
        ptr[prev] = ptr[cur]
    ptr[cur] = free
    free = cur
    return start, free, True


def ll_table(data, ptr):
    return '; '.join(f'[{i}] {data[i] or "—"}, {ptr[i]}' for i in range(len(data)))


@t9_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_2_ll(r, D):
    size = 7 if D <= 3 else 8
    n = r.randrange(3, 5)
    data, ptr, start, free = ll_build(r, size, n)
    words = ll_list(data, ptr, start)
    base = (f'An ordered linked list is stored in the arrays Data and Pointer (indices 0 to {size - 1}); −1 is the null pointer. StartPointer = {start}, FreePointer = {free}. '
            f'Each entry is [index] Data, Pointer: {ll_table(data, ptr)}. ')
    if D == 1:
        return MCQ(r, base + 'Which item is the second item in the list?', words[1], [w for w in words if w != words[1]] + r.sample([w for w in LL_WORDS if w not in words], 2), f'Start at {start} ({words[0]}), follow its pointer to {ptr[start]} ({words[1]}).')
    if D == 2:
        return Q(base + 'Write the items in the order they are stored in the list and state the index of the node that will be used for the next item inserted.', f'{", ".join(words)}; index {free}',
                 f'order {", ".join(words)} [1]; next node is FreePointer = {free} [1] [2]', marks=2)
    ops = []
    d2, p2, s2, f2 = data[:], ptr[:], start, free
    k = 2 if D <= 4 else 3
    for _ in range(k):
        cur = ll_list(d2, p2, s2)
        if r.random() < 0.6 or len(cur) < 2:
            w = r.choice([x for x in LL_WORDS if x not in cur])
            s2, f2, ok = ll_insert(d2, p2, s2, f2, w)
            ops.append(f'insert {w}')
        else:
            w = r.choice(cur)
            s2, f2, ok = ll_delete(d2, p2, s2, f2, w)
            ops.append(f'delete {w}')
    stem = base + f'The operations {", ".join(ops)} are carried out, taking new nodes from the front of the free list and returning deleted nodes to the front of the free list. Give the final StartPointer, FreePointer and Pointer array, and the items in list order.'
    return Q(stem, f'StartPointer = {s2}; FreePointer = {f2}; Pointer = {p2}; list: {", ".join(ll_list(d2, p2, s2))}', f'StartPointer [1]; FreePointer [1]; pointers changed correctly [{k}]; list order [1] [{k + 3}]', marks=k + 3)


@t9_2.add('C3', (2, 3, 4), 'numerical')
def t9_2_search(r, D):
    data, ptr, start, free = ll_build(r, 8, r.randrange(4, 7))
    words = ll_list(data, ptr, start)
    if r.random() < 0.6:
        w = r.choice(words)
        ans = f'{words.index(w) + 1} nodes visited; found at index {data.index(w)}'
    else:
        w = r.choice([x for x in LL_WORDS if x not in words])
        before = sum(1 for x in words if x < w)
        stop = before + 1 if before < len(words) else len(words)
        ans = f'not found after {stop} nodes visited (search stops when ' + ('a later item is reached, since the list is ordered)' if before < len(words) else 'the null pointer is reached)')
    return Q(f'An ordered linked list has StartPointer = {start} and nodes ([index] Data, Pointer; −1 = null): {ll_table(data, ptr)}. A search for "{w}" follows the pointers from the start and stops early once an item greater than the search item is reached. State the number of nodes visited and the outcome.',
             ans, '1 mark count; 1 mark outcome [2]', marks=2)


scen(t9_2, 'C4', (3, 4, 5), [
    '{org} stores its waiting list of customers as an ordered linked list in two arrays.', '{p} is writing a program for {org} that keeps a sorted list of usernames in a linked list.',
], [('Describe how a new item is inserted into the ordered linked list.', 'Take node from free list (FreePointer updated); store data; traverse to find position; set new node pointer to next node; set previous pointer (or StartPointer) to new node.', '1 mark per step, max 4 [4]'),
    ('Describe how an item is deleted.', 'Search for the item keeping track of previous node; set previous pointer (or StartPointer) to the deleted node\'s pointer; return node to free list.', '1 mark per step, max 3 [3]'),
    ('Explain why a linked list was chosen rather than a sorted array.', 'Insertion/deletion only change pointers, no shifting of items.', '1 mark each [2]'),
    lambda r, d: (lambda q: (q['stem'].split(' Each entry is')[0] + '. Explain what StartPointer = −1 would mean.', 'The list is empty.', '1 mark [1]'))(t9_2_ll(r, 2))], k=(3, 4))

t9_3 = topic('Binary trees: insertion and traversal (in-order, pre-order, post-order)', 'binary trees', 'insertion and traversal', 'in-order, pre-order, post-order')
t9_3.fixed('C1', (1, 2), [
    ('In a binary search tree, where is a value less than the current node placed?', 'In the left subtree', 'Greater (or equal) values go to the right.', ['In the right subtree', 'At the root', 'At the end of the tree']),
    ('Which traversal of a binary search tree outputs the values in ascending order?', 'In-order', 'Left, root, right.', ['Pre-order', 'Post-order', 'Breadth-first only']),
    ('In a pre-order traversal, when is the root visited?', 'Before its left and right subtrees', 'Pre-order: root, left, right.', ['After both subtrees', 'Between the two subtrees', 'Never']),
    ('In a post-order traversal, when is the root visited?', 'After its left and right subtrees', 'Post-order: left, right, root.', ['Before both subtrees', 'Between the two subtrees', 'First']),
    ('What is a leaf node?', 'A node with no children', 'Both its left and right pointers are null.', ['The root node', 'A node with two children', 'A node with one child']),
    ('How many children can each node in a binary tree have?', 'At most two', 'Left child and right child.', ['Exactly two', 'Any number', 'Exactly one']),
])
t9_3.fixed('C2', (2, 3, 4), [
    ('Explain why searching a balanced binary search tree is faster than searching an unordered list.', 'Each comparison discards half of the remaining tree, so about log₂ n comparisons are needed instead of up to n.', '1 mark each [2]'),
    ('Explain why the order in which values are inserted affects the shape of a binary search tree.', 'Each value is placed by comparison with existing nodes; inserting sorted data creates a tall, unbalanced tree like a linked list, which is slow to search.', '1 mark each [2]'),
])
ar(t9_3, [('An in-order traversal of a binary search tree gives sorted output.', 'All values in the left subtree are smaller than the root and all values in the right subtree are larger.'),
          ('Inserting values already in order produces an unbalanced tree.', 'Each new value is greater than every existing value, so it always goes to the right.'),
          ('A binary tree can be stored using arrays of pointers.', 'Each node can hold the indices of its left and right children.')],
   ['Pre-order traversal visits the root last.', 'A leaf node has two children.', 'Values greater than the root are placed in the left subtree.'])


def bst_build(vals):
    left, right = {}, {}
    root = vals[0]
    for v in vals[1:]:
        cur = root
        while True:
            if v < cur:
                if cur in left:
                    cur = left[cur]
                else:
                    left[cur] = v
                    break
            else:
                if cur in right:
                    cur = right[cur]
                else:
                    right[cur] = v
                    break
    return root, left, right


def trav(n, left, right, kind):
    if n is None:
        return []
    l, rr = trav(left.get(n), left, right, kind), trav(right.get(n), left, right, kind)
    return {'pre': [n] + l + rr, 'in': l + [n] + rr, 'post': l + rr + [n]}[kind]


def height(n, left, right):
    return 0 if n is None else 1 + max(height(left.get(n), left, right), height(right.get(n), left, right))


TNAME = {'pre': 'pre-order', 'in': 'in-order', 'post': 'post-order'}


@t9_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_3_trav(r, D):
    n = 6 if D <= 2 else (8 if D <= 4 else 10)
    if r.random() < 0.3:
        vals = r.sample(LL_WORDS, n)
    else:
        vals = r.sample(range(10, 99), n)
    root, left, right = bst_build(vals)
    vs = ', '.join(map(str, vals))
    kinds = ['pre', 'post'] if D <= 3 else ['pre', 'in', 'post']
    if D == 1:
        k = r.choice(['pre', 'post'])
        ans = ', '.join(map(str, trav(root, left, right, k)))
        return MCQ(r, f'The values {vs} are inserted in this order into an empty binary search tree. What is the {TNAME[k]} traversal?', ans,
                   [', '.join(map(str, trav(root, left, right, x))) for x in ('pre', 'in', 'post') if x != k] + [', '.join(map(str, vals))], f'{TNAME[k]}: {ans}.')
    res = '; '.join(f'{TNAME[k]}: ' + ', '.join(map(str, trav(root, left, right, k))) for k in kinds)
    lc = ', '.join(f'{p}→L {c}' for p, c in left.items())
    rc = ', '.join(f'{p}→R {c}' for p, c in right.items())
    return Q(f'The values {vs} are inserted, in this order, into an empty binary search tree. Draw (describe) the tree and write down its ' + ' and '.join(TNAME[k] for k in kinds) + ' traversals.',
             f'root {root}; links {lc}; {rc}; {res}', f'tree correct [1]; each traversal [{len(kinds)}] [{len(kinds) + 1}]', marks=len(kinds) + 1)


@t9_3.add('C3', (2, 3, 4, 5), 'numerical')
def t9_3_array(r, D):
    n = 6 if D <= 3 else 8
    vals = r.sample(range(10, 99), n)
    root, left, right = bst_build(vals)
    idx = {v: i for i, v in enumerate(vals)}
    L = [idx[left[v]] if v in left else -1 for v in vals]
    R = [idx[right[v]] if v in right else -1 for v in vals]
    tgt = r.choice(vals[1:]) if r.random() < 0.6 else r.choice([x for x in range(10, 99) if x not in vals])
    path, cur = [], root
    while cur is not None:
        path.append(cur)
        if tgt == cur:
            break
        cur = left.get(cur) if tgt < cur else right.get(cur)
    found = path[-1] == tgt
    return Q(f'A binary search tree is stored in arrays: index 0 is the root and nodes are stored in the order inserted. Data = {vals}; LeftPointer and RightPointer give child indices (−1 = null). '
             f'(a) Complete the LeftPointer and RightPointer arrays. (b) State the values compared when searching for {tgt}, and the result.',
             f'(a) LeftPointer = {L}; RightPointer = {R} (b) {", ".join(map(str, path))}; ' + ('found' if found else 'not found (null pointer reached)'),
             f'(a) LeftPointer [1]; RightPointer [1] (b) path [1]; result [1] [4]', marks=4)


scen(t9_3, 'C4', (3, 4, 5), [
    '{org} in {city} stores product codes in a binary search tree.', '{p} is writing a program for {org} that stores member names in a binary tree.',
], [lambda r, d: (lambda v: (f'The values {", ".join(map(str, v))} are inserted in order. Give the in-order and post-order traversals.',
                             (lambda t: 'in-order ' + ', '.join(map(str, trav(t[0], t[1], t[2], 'in'))) + '; post-order ' + ', '.join(map(str, trav(t[0], t[1], t[2], 'post'))))(bst_build(v)), '1 mark each [2]'))(r.sample(range(10, 99), 7)),
    ('Write a recursive pseudocode procedure InOrder(Node) that outputs the tree in order, using arrays LeftPointer, RightPointer and Data.',
     code(['PROCEDURE InOrder(Node : INTEGER)', f'{IND}IF Node <> -1 THEN', f'{IND}{IND}CALL InOrder(LeftPointer[Node])', f'{IND}{IND}OUTPUT Data[Node]', f'{IND}{IND}CALL InOrder(RightPointer[Node])', f'{IND}ENDIF', 'ENDPROCEDURE']),
     '1 mark base case check; 1 mark left call; 1 mark output; 1 mark right call [4]'),
    ('Explain why the tree may become slow to search over time.', 'If data is added in (nearly) sorted order the tree becomes unbalanced/tall, so searching approaches linear time.', '1 mark each [2]'),
    ('Describe how a new value is inserted into the tree.', 'Start at root; compare; go left if smaller, right if larger; repeat until a null pointer; add the new node there and set the parent\'s pointer.', '1 mark per point, max 3 [3]')], k=(3, 4))

t9_4 = topic('Graphs and dictionaries as ADTs', 'graphs and dictionaries')
t9_4.fixed('C1', (1, 2), [
    ('What is a dictionary ADT?', 'A collection of key–value pairs in which each value is accessed by its unique key', 'e.g. {"KE": "Kenya"}.', ['A sorted list of words', 'A stack of strings', 'A binary tree of numbers']),
    ('What is a directed graph?', 'A graph in which each edge has a direction from one node to another', 'Shown with arrows; an undirected edge works both ways.', ['A graph with weights on the edges', 'A graph with no cycles', 'A graph with only one node']),
    ('What is an adjacency matrix?', 'A 2D table in which entry [i, j] shows whether (or with what weight) node i is connected to node j', 'Adjacency lists store each node\'s neighbours instead.', ['A list of all nodes in order', 'A table of keys and values', 'A tree drawn as a table']),
    ('Which data structure is often used to implement a dictionary for fast look-up?', 'A hash table', 'The key is hashed to find the location.', ['A linked list', 'A stack', 'A queue']),
    ('Why are duplicate keys not allowed in a dictionary?', 'Each key must identify exactly one value', 'Adding an existing key replaces its value.', ['Keys must be numbers', 'It would use too much memory', 'Dictionaries are sorted by value']),
])
t9_4.fixed('C2', (2, 3, 4), [
    ('Explain when an adjacency list is better than an adjacency matrix.', 'For a sparse graph (few edges) an adjacency list uses less memory because only existing edges are stored; a matrix stores n² entries.', '1 mark each [2]'),
    ('Explain why a graph is a suitable ADT to represent a social network.', 'People are nodes and friendships/follows are edges (directed for follows); algorithms can find connections and shortest links.', '1 mark each [2]'),
])
ar(t9_4, [('A dictionary gives fast access to a value when the key is known.', 'The key can be hashed to find the location of the value directly.'),
          ('An adjacency matrix for an undirected graph is symmetrical.', 'Every edge between A and B is also an edge between B and A.'),
          ('An adjacency list saves memory for sparse graphs.', 'Only the edges that exist are stored.')],
   ['A dictionary can store two different values with the same key.', 'An adjacency matrix only works for trees.', 'A directed graph has no arrows.'])


@t9_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_4_matrix(r, D):
    n = 4 if D <= 3 else 5
    nodes = list(NODES[:n])
    directed = D >= 3 and r.random() < 0.5
    edges = set()
    while len(edges) < n + (0 if D <= 2 else 2):
        a, c = r.sample(nodes, 2)
        edges.add((a, c) if directed else tuple(sorted((a, c))))
    M = [[0] * n for _ in range(n)]
    for a, c in edges:
        M[nodes.index(a)][nodes.index(c)] = 1
        if not directed:
            M[nodes.index(c)][nodes.index(a)] = 1
    et = ', '.join(f'{a}{"→" if directed else "–"}{c}' for a, c in sorted(edges))
    rows = '; '.join(f'{nodes[i]}: ' + ' '.join(map(str, M[i])) for i in range(n))
    deg = {x: sum(M[nodes.index(x)]) for x in nodes}
    x = max(nodes, key=lambda k: (deg[k], k))
    if D == 1:
        y = r.choice(nodes)
        return MCQ(r, f'An undirected graph has the edges {et}. How many edges are connected to node {y}?', str(deg[y]), [str(deg[y] + 1), str(max(deg[y] - 1, 0) if deg[y] > 1 else deg[y] + 2), str(len(edges)), str(n)], f'Neighbours of {y}: {deg[y]}.')
    kind = 'directed' if directed else 'undirected'
    return Q(f'{"An" if kind[0] == "u" else "A"} {kind} graph has nodes {", ".join(nodes)} and edges {et}. Write its adjacency matrix (rows and columns in the order {", ".join(nodes)}) and state which node has the most ' + ('outgoing edges.' if directed else 'neighbours.'),
             f'{rows}; {x} ({deg[x]})', f'matrix correct [2]; {x} [1] [3]', marks=3)


@t9_4.add('C3', (2, 3, 4, 5), 'numerical')
def t9_4_dict(r, D):
    pool = [('KE', 'Kenya'), ('PE', 'Peru'), ('SG', 'Singapore'), ('AE', 'UAE'), ('PT', 'Portugal'), ('VN', 'Vietnam'), ('EG', 'Egypt'), ('NG', 'Nigeria'), ('QA', 'Qatar'), ('CL', 'Chile'), ('GH', 'Ghana'), ('NP', 'Nepal')]
    start = r.sample(pool, 3)
    dct = dict(start)
    ops, outs = [], []
    for _ in range(4 if D <= 3 else 6):
        k = r.choice(['add', 'get', 'del', 'upd'])
        if k == 'add':
            kk, vv = r.choice(pool)
            ops.append(f'Add("{kk}", "{vv}")')
            if kk in dct:
                outs.append(f'"{kk}" already exists')
            else:
                dct[kk] = vv
        elif k == 'get':
            kk = r.choice(list(dct) + [r.choice(pool)[0]])
            ops.append(f'OUTPUT Lookup("{kk}")')
            outs.append(dct.get(kk, 'NOT FOUND'))
        elif k == 'del' and dct:
            kk = r.choice(list(dct))
            ops.append(f'Delete("{kk}")')
            del dct[kk]
        elif dct:
            kk = r.choice(list(dct))
            vv = dct[kk].upper()
            ops.append(f'Update("{kk}", "{vv}")')
            dct[kk] = vv
    return Q('A dictionary ADT holds country codes and names: ' + ', '.join(f'"{k}": "{v}"' for k, v in start) + '. Add reports an error if the key already exists; Lookup returns "NOT FOUND" for a missing key. The operations ' + '; '.join(ops) +
             ' are carried out. State the outputs and errors, and the final contents of the dictionary.', f'outputs/errors: {", ".join(outs) or "none"}; final: ' + ', '.join(f'"{k}": "{v}"' for k, v in dct.items()),
             '1 mark outputs; 1 mark errors; 1 mark final contents [3]', marks=3)


scen(t9_4, 'C4', (3, 4, 5), [
    'An airline at {city} represents its routes as a graph and stores airport codes in a dictionary.', '{org} models its delivery network as a graph.',
], [('Compare an adjacency matrix and an adjacency list for storing the network.', 'Matrix: n² space, O(1) edge test; list: space proportional to edges, better for sparse graphs, slower edge test.', '1 mark per point, max 3 [3]'),
    ('Explain how a dictionary would be used to look up the full name of a location from its code.', 'Code is the key, name is the value; lookup by key (hashed) gives the name directly.', '1 mark each [2]'),
    ('Explain why some edges might be directed.', 'Some routes run only one way (e.g. one-way flights/roads).', '1 mark each [2]'),
    ('Describe the operations that a dictionary ADT should provide.', 'Add key–value pair; look up value by key; delete a key; update value; check if key exists.', '1 mark per operation, max 3 [3]')], k=(3, 4))

CHAPTERS[9] = [t9_1, t9_2, t9_3, t9_4]

# =============================================================================== Chapter 10 Algorithms
t10_1 = topic('Linear and binary search algorithms and their conditions', 'linear and binary search')
t10_1.fixed('C1', (1, 2), [
    ('What condition must be met before a binary search can be used?', 'The data must be sorted', 'Binary search compares with the middle item and discards half.', ['The data must be unsorted', 'The data must be in a linked list', 'There must be fewer than 100 items']),
    ('What is the maximum number of comparisons a linear search needs for n items?', 'n', 'Each item may need to be checked.', ['log₂ n', 'n²', '1']),
    ('What is the maximum number of comparisons for a binary search of 1000 sorted items?', '10', '2¹⁰ = 1024 ≥ 1000.', ['500', '1000', '100']),
    ('In a binary search, which item is compared first?', 'The middle item', 'Then the half that cannot contain the item is discarded.', ['The first item', 'The last item', 'A random item']),
    ('Which search can be used on unsorted data?', 'Linear search', 'Binary search requires sorted data.', ['Binary search', 'Both', 'Neither']),
])
t10_1.fixed('C2', (2, 3, 4), [
    ('Explain why a binary search is faster than a linear search for large sorted lists.', 'Each comparison halves the number of remaining items, so about log₂ n comparisons are needed instead of up to n.', '1 mark each [2]'),
    ('Explain when a linear search might be the better choice.', 'For small or unsorted lists, or when the list changes often, because sorting first would take extra time.', '1 mark each [2]'),
])
ar(t10_1, [('A binary search can only be used on a sorted array.', 'It relies on knowing whether the target is before or after the middle item.'),
           ('Doubling the size of a sorted list adds only one extra comparison to a binary search.', 'Each comparison halves the remaining list.'),
           ('A linear search works on unsorted data.', 'It checks every item in turn until the target is found.')],
    ['Binary search checks every item in order.', 'Linear search needs the data to be sorted.', 'Binary search always needs n comparisons.'])


def bsearch(a, t):
    lo, hi = 0, len(a) - 1
    mids = []
    while lo <= hi:
        m = (lo + hi) // 2
        mids.append(m)
        if a[m] == t:
            return mids, True
        if a[m] < t:
            lo = m + 1
        else:
            hi = m - 1
    return mids, False


@t10_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_1_bin(r, D):
    n = r.choice([7, 9, 10]) if D <= 2 else r.choice([11, 13, 15, 16])
    a = sorted(r.sample(range(5, 99), n))
    t = r.choice(a) if r.random() < 0.65 else r.choice([x for x in range(5, 99) if x not in a])
    mids, found = bsearch(a, t)
    seq = ', '.join(f'Mid = {m} (value {a[m]})' for m in mids)
    stem = f'The array Values[0:{n - 1}] holds {a}. A binary search for {t} uses Low = 0, High = {n - 1} and Mid ← INT((Low + High) / 2), then Low ← Mid + 1 or High ← Mid − 1.'
    if D == 1:
        return MCQ(r, stem + ' What is the first value compared with the target?', str(a[mids[0]]), [str(a[0]), str(a[-1]), str(a[min(mids[0] + 1, n - 1)]), str(a[max(mids[0] - 1, 0)])], f'Mid = INT((0 + {n - 1}) / 2) = {mids[0]}; Values[{mids[0]}] = {a[mids[0]]}.')
    return Q(stem + ' State each value of Mid and the value compared, the number of comparisons, and whether the item is found.', f'{seq}; {len(mids)} comparison{"" if len(mids) == 1 else "s"}; ' + ('found' if found else 'not found (Low > High)'),
             f'each Mid value [{min(len(mids), 3)}]; outcome [1] [{min(len(mids), 3) + 1}]', marks=min(len(mids), 3) + 1)


@t10_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_1_count(r, D):
    n = r.choice([50, 100, 200, 500, 1000, 4000, 10000, 65000, 100000, 1000000])
    mx = math.floor(math.log2(n)) + 1
    if D <= 2:
        return MCQ(r, f'What is the maximum number of comparisons needed by a binary search of {n:,} sorted items?', str(mx), [str(n), str(n // 2), str(mx + 3), str(max(mx - 2, 1))], f'⌊log₂ {n:,}⌋ + 1 = {mx}.')
    return Q(f'A sorted list contains {n:,} items. Calculate the maximum number of comparisons for a linear search and for a binary search, and the average for a linear search when the item is present.',
             f'linear max {n:,}; binary max {mx}; linear average ≈ {(n + 1) / 2:,.1f}', f'linear {n:,} [1]; binary ⌊log₂ n⌋ + 1 = {mx} [1]; average (n + 1)/2 [1] [3]', marks=3)


@t10_1.add('C3', (2, 3, 4, 5))
def t10_1_code(r, D):
    nm = r.choice(['Scores', 'Codes', 'Ages', 'Prices'])
    n = r.choice([50, 100, 200])
    lines = [f'FUNCTION BinarySearch(Target : INTEGER) RETURNS INTEGER', f'{IND}DECLARE Low, High, Mid : INTEGER', f'{IND}Low ← 0', f'{IND}High ← {n - 1}',
             f'{IND}WHILE Low <= High', f'{IND}{IND}Mid ← INT((Low + High) / 2)', f'{IND}{IND}IF {nm}[Mid] = Target THEN', f'{IND}{IND}{IND}RETURN Mid', f'{IND}{IND}ELSE', f'{IND}{IND}{IND}IF {nm}[Mid] < Target THEN',
             f'{IND}{IND}{IND}{IND}Low ← Mid + 1', f'{IND}{IND}{IND}ELSE', f'{IND}{IND}{IND}{IND}High ← Mid - 1', f'{IND}{IND}{IND}ENDIF', f'{IND}{IND}ENDIF', f'{IND}ENDWHILE', f'{IND}RETURN -1', 'ENDFUNCTION']
    errs = [(f'{IND}{IND}{IND}{IND}Low ← Mid + 1', f'{IND}{IND}{IND}{IND}Low ← Mid', 'Low ← Mid should be Low ← Mid + 1; otherwise the loop may never end when Low and High are adjacent'),
            (f'{IND}WHILE Low <= High', f'{IND}WHILE Low < High', 'WHILE Low < High should be WHILE Low <= High; otherwise the last remaining item is never checked'),
            (f'{IND}{IND}{IND}IF {nm}[Mid] < Target THEN', f'{IND}{IND}{IND}IF {nm}[Mid] > Target THEN', f'the comparison is reversed: it should be IF {nm}[Mid] < Target, so the search moves to the correct half'),
            (f'{IND}RETURN -1', f'{IND}RETURN Mid', 'RETURN Mid at the end should be RETURN -1 so that "not found" can be detected')]
    good, bad, why = r.choice(errs)
    lines = [bad if l == good else l for l in lines]
    return Q(f'The function searches the sorted array {nm}[0:{n - 1}]. It contains one error.\n' + code(lines) + '\nIdentify the error and write the corrected line.', why[0].upper() + why[1:] + '.', '1 mark error identified; 1 mark corrected line [2]', marks=2)


scen(t10_1, 'C4', (3, 4, 5), [
    'A library system at {org} in {city} must look up books by ISBN.', '{p} is choosing a search algorithm for a list of customer IDs at {org}.',
], [('Compare linear and binary search for this application.', 'Binary search much faster for large lists (log n vs n) but needs sorted data; linear works on unsorted data and is simpler.', '1 mark per point, max 3 [3]'),
    lambda r, d: (lambda n: (f'The list holds {n:,} sorted IDs. Calculate the maximum number of comparisons for each search.', f'linear {n:,}; binary {math.floor(math.log2(n)) + 1}', '1 mark each [2]'))(r.choice([2000, 5000, 30000, 250000])),
    ('Write pseudocode for a linear search that returns the index of Target in the array IDs[1:N], or −1 if absent.',
     code(['FUNCTION LinearSearch(Target : INTEGER) RETURNS INTEGER', f'{IND}DECLARE i : INTEGER', f'{IND}FOR i ← 1 TO N', f'{IND}{IND}IF IDs[i] = Target THEN', f'{IND}{IND}{IND}RETURN i', f'{IND}{IND}ENDIF', f'{IND}NEXT i', f'{IND}RETURN -1', 'ENDFUNCTION']),
     '1 mark loop; 1 mark comparison; 1 mark return index; 1 mark return −1 [4]'),
    ('Explain what must be done if new IDs are added frequently and binary search is to be used.', 'The list must be kept sorted (insert in order or re-sort), which takes extra time.', '1 mark each [2]')], k=(3, 4))

t10_2 = topic('Insertion sort and bubble sort; comparing performance', 'insertion sort and bubble sort', 'comparing performance')
t10_2.fixed('C1', (1, 2), [
    ('How does an insertion sort work?', 'Each item in turn is inserted into its correct place in the sorted part of the list', 'Items in the sorted part are shifted to make space.', ['Neighbouring items are repeatedly swapped', 'The list is split in half repeatedly', 'The smallest item is swapped to the front']),
    ('How does a bubble sort work?', 'Adjacent items are compared and swapped if out of order, in repeated passes', 'After each pass the largest unsorted item is in place.', ['Each item is inserted into a sorted sub-list', 'The list is divided into halves', 'Items are placed in a tree']),
    ('When can an improved bubble sort stop early?', 'When a complete pass makes no swaps', 'A flag records whether any swap happened.', ['After the first pass', 'When the first item is the smallest', 'Never']),
    ('What is the worst-case time complexity of insertion sort?', 'O(n²)', 'Best case (already sorted) is O(n).', ['O(n)', 'O(log n)', 'O(n log n)']),
    ('For which data does insertion sort perform best?', 'Data that is already nearly sorted', 'Few shifts are needed, close to O(n).', ['Data in reverse order', 'Random data', 'Data with many duplicates only']),
])
t10_2.fixed('C2', (2, 3, 4), [
    ('Explain why insertion sort is usually faster than bubble sort on nearly sorted data.', 'Each item needs to move only a short distance, so few comparisons/shifts are made; bubble sort still makes full passes of comparisons.', '1 mark each [2]'),
    ('Explain how the performance of bubble sort can be improved.', 'Stop when a pass makes no swaps (flag); reduce the range of each pass by one because the last items are already in place.', '1 mark each [2]'),
])
ar(t10_2, [('Bubble sort with a swap flag can finish after one pass on sorted data.', 'No swaps are made, which shows the data is already in order.'),
           ('Insertion sort is efficient for small or nearly sorted lists.', 'Items only move a few places to reach their correct position.'),
           ('Both bubble sort and insertion sort are O(n²) in the worst case.', 'They may compare every item with every other item.')],
    ['Bubble sort is O(log n).', 'Insertion sort needs the data to be sorted first.', 'Bubble sort compares items that are far apart.'])


def ins_passes(a):
    a = a[:]
    out, shifts = [], 0
    for i in range(1, len(a)):
        k, j = a[i], i - 1
        while j >= 0 and a[j] > k:
            a[j + 1] = a[j]
            j -= 1
            shifts += 1
        a[j + 1] = k
        out.append(a[:])
    return out, shifts


def bub_all(a):
    a = a[:]
    passes, comps, swaps = [], 0, 0
    n = len(a)
    while True:
        sw = False
        for i in range(n - 1):
            comps += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swaps += 1
                sw = True
        passes.append(a[:])
        n -= 1
        if not sw or n <= 1:
            break
    return passes, comps, swaps


@t10_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_2_ins(r, D):
    n = 5 if D <= 2 else (6 if D <= 4 else 7)
    a = r.sample(range(1, 60), n)
    ps, shifts = ins_passes(a)
    if D == 1:
        return MCQ(r, f'An insertion sort puts {a} into ascending order. What is the list after the second item has been inserted (after the first pass)?', str(ps[0]), [str(ps[1]), str(sorted(a)), str(a[::-1]), str(bub_all(a)[0][0])], f'Insert {a[1]} into the sorted part [{a[0]}]: {ps[0]}.')
    k = min(3, len(ps)) if D <= 3 else len(ps)
    return Q(f'The list {a} is sorted into ascending order using an insertion sort. Show the list after each of the first {k} passes' + (' and state the total number of shifts.' if D >= 4 else '.'),
             '; '.join(f'pass {i + 1}: {p}' for i, p in enumerate(ps[:k])) + (f'; {shifts} shifts' if D >= 4 else ''), (f'1 mark per correct pass [{k}]; shifts [1] [{k + 1}]' if D >= 4 else f'1 mark per correct pass [{k}]'), marks=k + (1 if D >= 4 else 0))


@t10_2.add('C3', (2, 3, 4, 5), 'numerical')
def t10_2_bub(r, D):
    n = 6 if D <= 3 else 8
    a = r.sample(range(1, 60), n)
    if D >= 4 and r.random() < 0.5:
        a = sorted(a)
        i = r.randrange(n - 1)
        a[i], a[i + 1] = a[i + 1], a[i]
    ps, comps, swaps = bub_all(a)
    return Q(f'An improved bubble sort (it stops after a pass with no swaps and makes each pass one comparison shorter) sorts {a} into ascending order. State the list after the first pass, the number of passes made, and the total number of comparisons.',
             f'after pass 1: {ps[0]}; {len(ps)} passes; {comps} comparisons; {swaps} swap{"" if swaps == 1 else "s"}', f'first pass [1]; passes {len(ps)} [1]; comparisons {comps} [1] [3]', marks=3)


scen(t10_2, 'C2', (2, 3, 4), [
    '{p} needs to sort a list of 20 exam scores that is already almost in order.', '{org} sorts its daily list of 5000 orders by order number.',
], [('Explain why an insertion sort may be a good choice.', 'Efficient for nearly sorted/small lists: items move only a short distance, close to O(n).', '1 mark each [2]'),
    ('Explain one way to improve the efficiency of a bubble sort.', 'Use a flag to stop when no swaps are made; shorten each pass by one.', '1 mark each [2]'),
    ('Compare the worst-case performance of insertion sort and bubble sort.', 'Both O(n²) comparisons in the worst case (reverse order); insertion sort shifts instead of swaps, so is usually faster in practice.', '1 mark each [2]')], k=(2, 3))
scen(t10_2, 'C4', (3, 4, 5), [
    'A scoreboard app developed in {city} keeps a list of high scores in order.', '{p} is comparing sorting algorithms for {org}\'s stock list.',
], [('Write pseudocode for an insertion sort on the array Scores[0:N-1].',
     code(['FOR i ← 1 TO N - 1', f'{IND}Item ← Scores[i]', f'{IND}j ← i - 1', f'{IND}WHILE j >= 0 AND Scores[j] > Item', f'{IND}{IND}Scores[j + 1] ← Scores[j]', f'{IND}{IND}j ← j - 1', f'{IND}ENDWHILE', f'{IND}Scores[j + 1] ← Item', 'NEXT i']),
     '1 mark outer loop; 1 mark store item; 1 mark while with both conditions; 1 mark shift; 1 mark insert [5]'),
    lambda r, d: (lambda a: (f'Show the list {a} after each pass of a bubble sort until it is sorted.', '; '.join(map(str, bub_all(a)[0])), '1 mark per pass, max 3 [3]'))(r.sample(range(1, 50), 5)),
    ('Explain which algorithm is better when one new score is added to an already sorted list.', 'Insertion sort: the new item is moved into place in one pass (O(n)); bubble sort needs at least one full pass and may need more.', '1 mark each [2]')], k=(2, 3))

t10_3 = topic('Big O notation for time and space complexity', 'big o notation', 'time and space complexity')
t10_3.fixed('C1', (1, 2), [
    ('What does Big O notation describe?', 'How the time or memory needed by an algorithm grows as the size of the input grows', 'Usually the worst case; constants are ignored.', ['The exact running time in seconds', 'The number of lines of code', 'The size of the program file']),
    ('What is the time complexity of a binary search?', 'O(log n)', 'Each step halves the problem.', ['O(n)', 'O(n²)', 'O(1)']),
    ('What is the time complexity of accessing an array element by its index?', 'O(1)', 'Constant time regardless of size.', ['O(n)', 'O(log n)', 'O(n²)']),
    ('Which order of growth is the slowest growing?', 'O(log n)', 'O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ).', ['O(n)', 'O(n²)', 'O(2ⁿ)']),
    ('What is the time complexity of a linear search?', 'O(n)', 'Worst case checks every item.', ['O(log n)', 'O(1)', 'O(n²)']),
    ('What does space complexity measure?', 'How the amount of memory needed grows with the input size', 'e.g. an in-place sort is O(1) extra space.', ['How fast the program runs', 'The size of the hard disk', 'The number of variables declared']),
])
t10_3.fixed('C2', (2, 3, 4), [
    ('Explain why constants are ignored in Big O notation.', 'Big O describes growth for large n; a constant factor does not change how the time grows (e.g. 3n and n are both linear).', '1 mark each [2]'),
    ('Explain why an O(2ⁿ) algorithm is impractical for large inputs.', 'Each extra item doubles the time, so time becomes enormous even for moderate n (e.g. n = 60).', '1 mark each [2]'),
])
ar(t10_3, [('A binary search is O(log n).', 'The number of items to check halves at every step.'),
           ('Nested loops over the same data are often O(n²).', 'The inner loop runs n times for each of the n outer iterations.'),
           ('Bubble sort has O(1) space complexity.', 'It sorts the array in place using only a few extra variables.')],
    ['Linear search is O(1).', 'O(n²) grows more slowly than O(n).', 'Big O gives the exact time in seconds.'])

BIGO = [('O(1)', lambda n: 1), ('O(log n)', lambda n: math.log2(n)), ('O(n)', lambda n: n), ('O(n log n)', lambda n: n * math.log2(n)), ('O(n²)', lambda n: n * n), ('O(n³)', lambda n: n ** 3), ('O(2ⁿ)', lambda n: 2 ** n)]


def bigo_code(r, kind):
    v = r.choice(['Data', 'List', 'Values', 'Items'])
    if kind == 'O(1)':
        return [f'Result ← {v}[1] + {v}[N]', 'OUTPUT Result']
    if kind == 'O(n)':
        return ['Total ← 0', 'FOR i ← 1 TO N', f'{IND}Total ← Total + {v}[i]', 'NEXT i']
    if kind == 'O(n²)':
        return ['Count ← 0', 'FOR i ← 1 TO N', f'{IND}FOR j ← 1 TO N', f'{IND}{IND}IF {v}[i] = {v}[j] THEN', f'{IND}{IND}{IND}Count ← Count + 1', f'{IND}{IND}ENDIF', f'{IND}NEXT j', 'NEXT i']
    if kind == 'O(log n)':
        return ['Steps ← 0', 'WHILE N > 1', f'{IND}N ← INT(N / 2)', f'{IND}Steps ← Steps + 1', 'ENDWHILE']
    if kind == 'O(n log n)':
        return ['FOR i ← 1 TO N', f'{IND}k ← N', f'{IND}WHILE k > 1', f'{IND}{IND}k ← INT(k / 2)', f'{IND}{IND}Total ← Total + {v}[i]', f'{IND}ENDWHILE', 'NEXT i']
    return ['FOR i ← 1 TO N', f'{IND}FOR j ← 1 TO N', f'{IND}{IND}FOR k ← 1 TO N', f'{IND}{IND}{IND}Total ← Total + {v}[i] * {v}[j] * {v}[k]', f'{IND}{IND}NEXT k', f'{IND}NEXT j', 'NEXT i']


@t10_3.add('C3', (1, 2, 3, 4))
def t10_3_code(r, D):
    kind = r.choice(['O(1)', 'O(n)', 'O(n²)', 'O(log n)', 'O(n log n)', 'O(n³)'])
    lines = bigo_code(r, kind)
    why = {'O(1)': 'a fixed number of steps whatever the size of N', 'O(n)': 'one loop that runs N times', 'O(n²)': 'a loop of N nested inside a loop of N, so N × N steps',
           'O(log n)': 'N is halved each time round the loop', 'O(n log n)': 'a halving loop (log N) inside a loop that runs N times', 'O(n³)': 'three nested loops of N'}[kind]
    if D <= 2:
        return MCQ(r, 'What is the time complexity of this algorithm?\n' + code(lines), kind, [k for k, _ in BIGO if k != kind], f'{kind}: {why}.')
    return Q('State the time complexity of this algorithm in Big O notation and justify your answer.\n' + code(lines), f'{kind}: {why}.', '1 mark complexity; 1 mark justification [2]', marks=2)


@t10_3.add('C3', (2, 3, 4, 5), 'numerical')
def t10_3_scale(r, D):
    kind = r.choice(['O(n)', 'O(n²)', 'O(n log n)', 'O(n³)', 'O(log n)'] + (['O(2ⁿ)'] if D >= 4 else []))
    f = dict(BIGO)[kind]
    if kind == 'O(2ⁿ)':
        n1 = r.randrange(20, 31)
        n2 = n1 + r.randrange(2, 6)
    elif kind in ('O(n log n)', 'O(log n)'):
        n1 = r.choice([256, 1024, 4096])
        n2 = n1 * r.choice([4, 16, 64])
    else:
        n1 = r.choice([100, 500, 1000, 2000])
        n2 = n1 * r.choice([2, 3, 4, 10])
    t1 = r.choice([0.5, 1, 2, 3, 4, 5, 8])
    t2 = t1 * f(n2) / f(n1)
    t2s = f'{t2:.3g}' if t2 < 1000 else f'{t2:,.0f}'
    return Q(f'An algorithm with time complexity {kind} takes {t1:g} seconds to process {n1:,} items. Estimate the time to process {n2:,} items, showing your working.', f'{t2s} s',
             f'time ∝ f(n): {t1:g} × f({n2:,}) ÷ f({n1:,}) [1]; = {t2s} s [1] [2]', marks=2)


scen(t10_3, 'C4', (3, 4, 5), [
    '{org} in {city} must choose an algorithm to process a database that grows by 10 000 records a month.', '{p} is comparing two programs that check a list of usernames for duplicates at {org}.',
], [lambda r, d: (lambda k: (f'State the time complexity of this code and justify it:\n' + code(bigo_code(r, k)), k, '1 mark complexity; 1 mark reason [2]'))(r.choice(['O(n)', 'O(n²)', 'O(log n)'])),
    ('Explain why an O(n log n) algorithm is preferred to an O(n²) algorithm for large data sets.', 'n log n grows much more slowly; e.g. for n = 1 000 000, ≈ 2 × 10⁷ vs 10¹² steps.', '1 mark each [2]'),
    ('Explain what is meant by space complexity and why it matters here.', 'How memory use grows with n; large data sets may not fit in memory if extra space grows quickly.', '1 mark each [2]'),
    lambda r, d: (lambda n: (f'An O(n²) program takes 2 s for {n:,} records. Estimate the time for {4 * n:,} records.', '32 s', '× 4² = × 16 [1]; 32 s [1] [2]'))(r.choice([1000, 5000, 20000]))], k=(3, 4))

CHAPTERS[10] = [t10_1, t10_2, t10_3]

# =============================================================================== Chapter 11 Recursion
def _calls(f, *a):
    """Run a Python recursive function f(rec, *a) counting calls and max depth."""
    st = {'calls': 0, 'depth': 0, 'max': 0}

    def rec(*x):
        st['calls'] += 1
        st['depth'] += 1
        st['max'] = max(st['max'], st['depth'])
        v = f(rec, *x)
        st['depth'] -= 1
        return v
    v = rec(*a)
    return v, st['calls'], st['max']


REC_NAMES = {'Factorial': (['Factorial', 'Fact', 'CalcFactorial', 'Product'], [('N',), ('Num',), ('X',), ('Value',), ('K',)]),
             'Power': (['Power', 'Raise', 'PowerOf', 'Exp'], [('B', 'E'), ('Base', 'Exponent'), ('X', 'N'), ('Num', 'Times')]),
             'SumDigits': (['SumDigits', 'DigitTotal', 'AddDigits'], [('N',), ('Num',), ('Value',), ('X',)]),
             'SumTo': (['SumTo', 'Triangle', 'AddUp', 'SumOf'], [('N',), ('Num',), ('K',), ('Count',)]),
             'GCD': (['GCD', 'HCF', 'Highest'], [('A', 'B'), ('X', 'Y'), ('M', 'N'), ('First', 'Second')]),
             'Mystery': (['Mystery', 'Remainder', 'Reduce', 'Calc'], [('X', 'Y'), ('A', 'B'), ('P', 'Q'), ('Num', 'Step')]),
             'Fib': (['Fib', 'Fibonacci', 'Seq'], [('N',), ('Num',), ('Term',)])}


def _rename(r, f):
    old = f['lines'][0].split()[1].split('(')[0]
    names, params = REC_NAMES[old]
    oldp = params[0]
    newn, newp = r.choice(names), r.choice(params)
    mp = {old: newn}
    mp.update({a: c for a, c in zip(oldp, newp)})
    rx = re.compile(r'\b(' + '|'.join(map(re.escape, mp)) + r')\b')
    sub = lambda t: rx.sub(lambda m: mp[m.group(1)], t)
    g = dict(f)
    for k in ('call', 'base', 'gen', 'unwind'):
        g[k] = sub(f[k])
    for k in ('lines', 'it'):
        g[k] = [sub(x) for x in f[k]]
    return g


def recfun(r, D, kind=None):
    return _rename(r, _recfun(r, D, kind))


def _recfun(r, D, kind=None):
    kind = kind or r.choice(['fact', 'power', 'digits', 'sum', 'gcd', 'mod', 'fib'] if D >= 3 else ['fact', 'power', 'sum', 'digits', 'mod'])
    if kind == 'fact':
        n = r.randrange(3, 6 if D <= 2 else 8)
        lines = ['FUNCTION Factorial(N : INTEGER) RETURNS INTEGER', f'{IND}IF N <= 1 THEN', f'{IND}{IND}RETURN 1', f'{IND}ELSE', f'{IND}{IND}RETURN N * Factorial(N - 1)', f'{IND}ENDIF', 'ENDFUNCTION']
        v, c, dp = _calls(lambda rec, x: 1 if x <= 1 else x * rec(x - 1), n)
        it = ['Result ← 1', 'FOR i ← 2 TO N', f'{IND}Result ← Result * i', 'NEXT i', 'RETURN Result']
        return dict(lines=lines, call=f'Factorial({n})', v=v, calls=c, depth=dp, base='IF N <= 1 THEN RETURN 1', gen='RETURN N * Factorial(N - 1)', it=it,
                    unwind=' → '.join(f'Factorial({k}) = {math.factorial(k)}' for k in range(1, n + 1)))
    if kind == 'power':
        bb, e = r.randrange(2, 6), r.randrange(3, 6 if D <= 2 else 8)
        lines = ['FUNCTION Power(B : INTEGER, E : INTEGER) RETURNS INTEGER', f'{IND}IF E = 0 THEN', f'{IND}{IND}RETURN 1', f'{IND}ELSE', f'{IND}{IND}RETURN B * Power(B, E - 1)', f'{IND}ENDIF', 'ENDFUNCTION']
        v, c, dp = _calls(lambda rec, x, y: 1 if y == 0 else x * rec(x, y - 1), bb, e)
        it = ['Result ← 1', 'FOR i ← 1 TO E', f'{IND}Result ← Result * B', 'NEXT i', 'RETURN Result']
        return dict(lines=lines, call=f'Power({bb}, {e})', v=v, calls=c, depth=dp, base='IF E = 0 THEN RETURN 1', gen='RETURN B * Power(B, E - 1)', it=it,
                    unwind=' → '.join(f'Power({bb}, {k}) = {bb ** k}' for k in range(0, e + 1)))
    if kind == 'digits':
        n = r.randrange(100, 1000 if D <= 3 else 100000)
        lines = ['FUNCTION SumDigits(N : INTEGER) RETURNS INTEGER', f'{IND}IF N < 10 THEN', f'{IND}{IND}RETURN N', f'{IND}ELSE', f'{IND}{IND}RETURN (N MOD 10) + SumDigits(N DIV 10)', f'{IND}ENDIF', 'ENDFUNCTION']
        v, c, dp = _calls(lambda rec, x: x if x < 10 else x % 10 + rec(x // 10), n)
        it = ['Total ← 0', 'WHILE N > 0', f'{IND}Total ← Total + (N MOD 10)', f'{IND}N ← N DIV 10', 'ENDWHILE', 'RETURN Total']
        ks, x = [], n
        while x >= 10:
            ks.append(x)
            x //= 10
        ks.append(x)
        return dict(lines=lines, call=f'SumDigits({n})', v=v, calls=c, depth=dp, base='IF N < 10 THEN RETURN N', gen='RETURN (N MOD 10) + SumDigits(N DIV 10)', it=it,
                    unwind=' → '.join(f'SumDigits({k}) = {sum(map(int, str(k)))}' for k in reversed(ks)))
    if kind == 'sum':
        n = r.randrange(4, 9 if D <= 3 else 13)
        lines = ['FUNCTION SumTo(N : INTEGER) RETURNS INTEGER', f'{IND}IF N = 0 THEN', f'{IND}{IND}RETURN 0', f'{IND}ELSE', f'{IND}{IND}RETURN N + SumTo(N - 1)', f'{IND}ENDIF', 'ENDFUNCTION']
        v, c, dp = _calls(lambda rec, x: 0 if x == 0 else x + rec(x - 1), n)
        it = ['Total ← 0', 'FOR i ← 1 TO N', f'{IND}Total ← Total + i', 'NEXT i', 'RETURN Total']
        return dict(lines=lines, call=f'SumTo({n})', v=v, calls=c, depth=dp, base='IF N = 0 THEN RETURN 0', gen='RETURN N + SumTo(N - 1)', it=it,
                    unwind=' → '.join(f'SumTo({k}) = {k * (k + 1) // 2}' for k in range(0, n + 1)))
    if kind == 'gcd':
        a, c0 = r.randrange(20, 200), r.randrange(6, 90)
        lines = ['FUNCTION GCD(A : INTEGER, B : INTEGER) RETURNS INTEGER', f'{IND}IF B = 0 THEN', f'{IND}{IND}RETURN A', f'{IND}ELSE', f'{IND}{IND}RETURN GCD(B, A MOD B)', f'{IND}ENDIF', 'ENDFUNCTION']
        v, c, dp = _calls(lambda rec, x, y: x if y == 0 else rec(y, x % y), a, c0)
        seq, x, y = [], a, c0
        while True:
            seq.append(f'GCD({x}, {y})')
            if y == 0:
                break
            x, y = y, x % y
        it = ['WHILE B <> 0', f'{IND}Temp ← B', f'{IND}B ← A MOD B', f'{IND}A ← Temp', 'ENDWHILE', 'RETURN A']
        return dict(lines=lines, call=f'GCD({a}, {c0})', v=v, calls=c, depth=dp, base='IF B = 0 THEN RETURN A', gen='RETURN GCD(B, A MOD B)', it=it, unwind=' → '.join(seq) + f' = {v}')
    if kind == 'mod':
        a, c0 = r.randrange(20, 60), r.randrange(3, 9)
        lines = ['FUNCTION Mystery(X : INTEGER, Y : INTEGER) RETURNS INTEGER', f'{IND}IF X < Y THEN', f'{IND}{IND}RETURN X', f'{IND}ELSE', f'{IND}{IND}RETURN Mystery(X - Y, Y)', f'{IND}ENDIF', 'ENDFUNCTION']
        v, c, dp = _calls(lambda rec, x, y: x if x < y else rec(x - y, y), a, c0)
        it = ['WHILE X >= Y', f'{IND}X ← X - Y', 'ENDWHILE', 'RETURN X']
        return dict(lines=lines, call=f'Mystery({a}, {c0})', v=v, calls=c, depth=dp, base='IF X < Y THEN RETURN X', gen='RETURN Mystery(X - Y, Y)', it=it,
                    unwind=' → '.join(f'Mystery({a - k * c0}, {c0})' for k in range(c)) + f' = {v} (the remainder of {a} ÷ {c0})')
    n = r.randrange(4, 8)
    lines = ['FUNCTION Fib(N : INTEGER) RETURNS INTEGER', f'{IND}IF N <= 1 THEN', f'{IND}{IND}RETURN N', f'{IND}ELSE', f'{IND}{IND}RETURN Fib(N - 1) + Fib(N - 2)', f'{IND}ENDIF', 'ENDFUNCTION']
    v, c, dp = _calls(lambda rec, x: x if x <= 1 else rec(x - 1) + rec(x - 2), n)
    it = ['A ← 0', 'B ← 1', 'FOR i ← 1 TO N', f'{IND}Temp ← A + B', f'{IND}A ← B', f'{IND}B ← Temp', 'NEXT i', 'RETURN A']
    fs = [0, 1]
    while len(fs) <= n:
        fs.append(fs[-1] + fs[-2])
    return dict(lines=lines, call=f'Fib({n})', v=v, calls=c, depth=dp, base='IF N <= 1 THEN RETURN N', gen='RETURN Fib(N - 1) + Fib(N - 2)', it=it,
                unwind=', '.join(f'Fib({k}) = {fs[k]}' for k in range(n + 1)))


def recproc(r, D):
    kind = r.choice(['pre', 'post', 'bin', 'both'])
    step = r.choice([1, 2, 3])
    n = r.randrange(5, 12)
    if kind == 'bin':
        n = r.randrange(5, 64 if D <= 3 else 256)
        lines = ['PROCEDURE ToBinary(N : INTEGER)', f'{IND}IF N > 1 THEN', f'{IND}{IND}CALL ToBinary(N DIV 2)', f'{IND}ENDIF', f'{IND}OUTPUT N MOD 2', 'ENDPROCEDURE']
        pn, vn = r.choice(['ToBinary', 'ShowBinary', 'Convert', 'OutBits']), r.choice(['N', 'Num', 'X', 'Value'])
        lines = [re.sub(r'\bN\b', vn, l).replace('ToBinary', pn) for l in lines]
        return lines, f'CALL {pn}({n})', ' '.join(format(n, 'b')), 'each call outputs N MOD 2 after the recursive call returns, so the remainders are output in reverse order of calculation, giving the binary form of ' + str(n)
    outs = []
    def go(x):
        if x > 0:
            if kind in ('pre', 'both'):
                outs.append(x)
            go(x - step)
            if kind in ('post', 'both'):
                outs.append(x)
    go(n)
    body = []
    if kind in ('pre', 'both'):
        body.append(f'{IND}{IND}OUTPUT N')
    body.append(f'{IND}{IND}CALL Show(N - {step})')
    if kind in ('post', 'both'):
        body.append(f'{IND}{IND}OUTPUT N')
    lines = ['PROCEDURE Show(N : INTEGER)', f'{IND}IF N > 0 THEN'] + body + [f'{IND}ENDIF', 'ENDPROCEDURE']
    pn, vn = r.choice(['Show', 'Display', 'Count', 'PrintDown', 'Trace']), r.choice(['N', 'Num', 'X', 'Value'])
    lines = [re.sub(r'\bN\b', vn, l).replace('Show', pn) for l in lines]
    why = {'pre': 'each value is output before the recursive call', 'post': 'each value is output after the recursive call returns, so in reverse order', 'both': 'each value is output on the way down and again as the calls unwind'}[kind]
    return lines, f'CALL {pn}({n})', ' '.join(map(str, outs)), why


t11_1 = topic('Essential features of recursion: base case, general case and stack frames', 'essential features of recursion', 'base case, general case', 'stack frames')
t11_1.fixed('C1', (1, 2), [
    ('What is recursion?', 'When a subroutine calls itself', 'It must have a base case and a general case that moves towards it.', ['When a loop runs forever', 'When two programs share data', 'When a function returns two values']),
    ('What is the base case of a recursive subroutine?', 'The condition under which the subroutine returns without calling itself', 'It stops the recursion.', ['The first line of the subroutine', 'The recursive call', 'The largest possible input']),
    ('What is the general case of a recursive subroutine?', 'The part where the subroutine calls itself with a value closer to the base case', 'e.g. RETURN N * Factorial(N - 1).', ['The part that stops the recursion', 'The parameter list', 'The return type']),
    ('What happens if a recursive subroutine never reaches its base case?', 'The call stack fills up and a stack overflow error occurs', 'Each call uses a new stack frame.', ['It returns 0', 'It runs as a loop with no memory use', 'The compiler fixes it']),
    ('What is stored in a stack frame for a subroutine call?', 'The return address, parameters and local variables', 'One frame is pushed per call and popped on return.', ['The source code of the subroutine', 'Only the result', 'The whole program']),
])
t11_1.fixed('C2', (2, 3, 4), [
    ('Explain why a recursive subroutine must have a base case.', 'Without it the subroutine keeps calling itself; each call adds a stack frame, so memory runs out (stack overflow) and the program crashes.', '1 mark each [2]'),
    ('Explain why recursion can use more memory than iteration.', 'Every recursive call pushes a new stack frame (return address, parameters, locals) that remains until the call returns; a loop reuses the same variables.', '1 mark each [2]'),
])
ar(t11_1, [('A recursive function needs a base case.', 'The base case stops further recursive calls.'),
           ('Deep recursion can cause a stack overflow.', 'Each call adds a frame to the call stack.'),
           ('The general case must move towards the base case.', 'Otherwise the base case would never be reached.')],
    ['A recursive function cannot have parameters.', 'Stack frames are stored in a queue.', 'The base case calls the function again.'])


@t11_1.add('C3', (1, 2, 3, 4, 5))
def t11_1_identify(r, D):
    f = recfun(r, D)
    if D == 1:
        return MCQ(r, 'Which line is the base case of this function?\n' + code(f['lines']), f['base'], [f['gen'], f['lines'][0], 'ENDFUNCTION', 'RETURN ' + f['call']], f'The base case returns without a recursive call: {f["base"]}.')
    if D <= 3:
        return Q('Study the recursive function:\n' + code(f['lines']) + f'\nIdentify the base case and the general case, and state how many times the function is called (including the first call) when {f["call"]} is evaluated.',
                 f'Base case: {f["base"]}; general case: {f["gen"]}; {f["calls"]} calls', f'base case [1]; general case [1]; {f["calls"]} calls [1] [3]', marks=3)
    return Q('Study the recursive function:\n' + code(f['lines']) + f'\n{f["call"]} is evaluated. State the value returned, the total number of calls, and the maximum number of stack frames for this function on the call stack at one time.',
             f'{f["v"]}; {f["calls"]} calls; maximum depth {f["depth"]}', f'value {f["v"]} [1]; calls {f["calls"]} [1]; depth {f["depth"]} [1] [3]', marks=3)


@t11_1.add('C3', (2, 3, 4, 5))
def t11_1_bug(r, D):
    kinds = [(['FUNCTION Countdown(N : INTEGER) RETURNS INTEGER', f'{IND}IF N = 0 THEN', f'{IND}{IND}RETURN 0', f'{IND}ELSE', f'{IND}{IND}RETURN N + Countdown(N - 2)', f'{IND}ENDIF', 'ENDFUNCTION'],
              lambda n: n % 2 == 1, 'N decreases by 2, so for an odd starting value N skips 0 and becomes negative; the base case is never reached and the stack overflows. Fix: IF N <= 0 THEN'),
             (['FUNCTION Total(N : INTEGER) RETURNS INTEGER', f'{IND}IF N = 1 THEN', f'{IND}{IND}RETURN 1', f'{IND}ELSE', f'{IND}{IND}RETURN N + Total(N)', f'{IND}ENDIF', 'ENDFUNCTION'],
              lambda n: n != 1, 'The general case calls Total(N) with the same value, so it never moves towards the base case; infinite recursion causes stack overflow. Fix: RETURN N + Total(N - 1)'),
             (['FUNCTION Fact(N : INTEGER) RETURNS INTEGER', f'{IND}IF N = 1 THEN', f'{IND}{IND}RETURN 1', f'{IND}ELSE', f'{IND}{IND}RETURN N * Fact(N - 1)', f'{IND}ENDIF', 'ENDFUNCTION'],
              lambda n: n <= 0, 'For N = 0 or a negative value, N − 1 never equals 1, so the base case is never reached and the stack overflows. Fix: IF N <= 1 THEN'),
             (['FUNCTION Half(N : INTEGER) RETURNS INTEGER', f'{IND}IF N = 1 THEN', f'{IND}{IND}RETURN 0', f'{IND}ELSE', f'{IND}{IND}RETURN 1 + Half(N DIV 2)', f'{IND}ENDIF', 'ENDFUNCTION'],
              lambda n: n <= 0, 'For N = 0, N DIV 2 stays 0 for ever, so the base case is never reached; stack overflow. Fix: IF N <= 1 THEN')]
    lines, bad, why = r.choice(kinds)
    cands = [x for x in range(-3, 15) if bad(x)]
    n = r.choice(cands)
    nm = lines[0].split()[1].split('(')[0]
    return Q(f'The recursive function is called with {nm}({n}).\n' + code(lines) + '\nExplain what happens and suggest a correction.', why + '.', '1 mark base case never reached; 1 mark stack overflow; 1 mark correction [3]', marks=3)


scen(t11_1, 'C4', (3, 4, 5), [
    '{p} is learning about recursion while writing utilities for {org}.', 'A programmer at {org} in {city} has written several recursive functions.',
], [lambda r, d: (lambda f: ('Study the function:\n' + code(f['lines']) + f'\nState the value returned by {f["call"]}.', str(f['v']), f'{f["unwind"]} [2]'))(recfun(r, 3)),
    ('Describe the features that every recursive subroutine must have.', 'A base case that stops the recursion; a general case that calls itself; each call moves closer to the base case.', '1 mark per point [3]'),
    ('Explain what is stored on the stack when a recursive call is made.', 'A stack frame containing the return address, parameter values and local variables; popped when the call returns.', '1 mark per point, max 2 [2]'),
    ('Give one advantage and one disadvantage of recursion compared with iteration.', 'Advantage: shorter, clearer code for naturally recursive problems (trees). Disadvantage: more memory; risk of stack overflow; slower due to call overheads.', '1 mark each [2]')], k=(3, 4))

t11_2 = topic('Tracing recursive algorithms and comparing with iterative solutions', 'tracing recursive algorithms', 'iterative solutions')
t11_2.fixed('C1', (1, 2), [
    ('When a recursive function returns, where does execution continue?', 'At the instruction after the call, in the calling instance of the function', 'The return address is taken from the stack frame.', ['At the start of the program', 'At the base case', 'At the end of the program']),
    ('Which structure can always replace recursion?', 'Iteration (a loop), possibly with an explicit stack', 'Any recursive algorithm can be rewritten iteratively.', ['A selection statement only', 'A constant', 'A single assignment']),
    ('In a recursive procedure, statements written after the recursive call are executed', 'as the calls unwind, in reverse order of the calls', 'This is why output after the call appears reversed.', ['before the recursive call', 'only in the base case', 'never']),
    ('Which problem is naturally recursive?', 'Traversing a binary tree', 'Each subtree is itself a tree.', ['Adding two numbers', 'Reading one input', 'Swapping two variables']),
    ('Why can a recursive solution be slower than an iterative one?', 'Each call has the overhead of creating and removing a stack frame', 'Some recursive algorithms (e.g. naive Fibonacci) also repeat work.', ['Recursive code is compiled twice', 'Recursion cannot use variables', 'Recursion always uses a queue']),
])
t11_2.fixed('C2', (2, 3, 4), [
    ('Explain why the naive recursive Fibonacci function is inefficient.', 'Each call makes two further calls, so the same values (e.g. Fib(2)) are recalculated many times; the number of calls grows exponentially.', '1 mark each [2]'),
    ('Explain why a programmer might choose recursion even though it uses more memory.', 'The code is shorter and closer to the mathematical definition, making it easier to write and check, especially for recursive structures such as trees.', '1 mark each [2]'),
])
ar(t11_2, [('Output placed after a recursive call appears in reverse order.', 'It is executed as each call returns, starting with the deepest call.'),
           ('Naive recursive Fibonacci makes many repeated calls.', 'Each call branches into two further calls.'),
           ('Every recursive algorithm can be written iteratively.', 'A loop with an explicit stack can do the same work.')],
    ['Recursion always uses less memory than iteration.', 'A recursive function can only be called once.', 'The base case is executed first in every call.'])


@t11_2.add('C3', (1, 2, 3, 4, 5))
def t11_2_trace(r, D):
    if r.random() < 0.5:
        lines, call, out, why = recproc(r, D)
        stem = 'Study the recursive procedure:\n' + code(lines) + f'\nState the output when {call} is executed.'
        if D == 1:
            rev = ' '.join(reversed(out.split()))
            return MCQ(r, stem.replace('State the output', 'What is the output'), out, [rev if rev != out else out + ' 0', ' '.join(out.split()[:-1]) or '0', out + ' ' + out.split()[0], '0 ' + out], why[0].upper() + why[1:] + '.')
        return Q(stem, out, f'{why[0].upper() + why[1:]} [2]', marks=2)
    f = recfun(r, D)
    stem = 'Study the recursive function:\n' + code(f['lines']) + f'\nTrace the call {f["call"]}, showing the value returned by each call, and state the final result.'
    if D == 1:
        return MCQ(r, 'Study the recursive function:\n' + code(f['lines']) + f'\nWhat value is returned by {f["call"]}?', str(f['v']), [str(f['v'] + 1), str(f['v'] * 2), str(max(f['v'] - 1, 0)) if f['v'] > 1 else '2', str(f['calls'])], f['unwind'] + '.')
    return Q(stem, f'{f["unwind"]}; result {f["v"]}', f'calls/returns traced [2]; final value {f["v"]} [1] [3]', marks=3)


@t11_2.add('C3', (2, 3, 4, 5))
def t11_2_iter(r, D):
    f = recfun(r, D)
    hdr = f['lines'][0]
    return Q('Rewrite this recursive function as an iterative function that gives the same result.\n' + code(f['lines']), code([hdr] + [IND + l for l in f['it']] + ['ENDFUNCTION']),
             '1 mark loop structure; 1 mark correct initialisation; 1 mark correct update; 1 mark return [4]', marks=4)


scen(t11_2, 'C4', (3, 4, 5), [
    '{p} is comparing recursive and iterative solutions for {org}.', 'A teacher at {org} gives students recursive code to trace.',
], [lambda r, d: (lambda f: ('Study:\n' + code(f['lines']) + f'\nTrace {f["call"]} and give the result.', f'{f["unwind"]}; {f["v"]}', '1 mark trace; 1 mark result [2]'))(recfun(r, 3)),
    lambda r, d: (lambda p: ('Study:\n' + code(p[0]) + f'\nState the output of {p[1]}.', p[2], '1 mark per correct half of output [2]'))(recproc(r, 3)),
    ('Compare the recursive and iterative solutions in terms of memory use and readability.', 'Recursive uses a stack frame per call so more memory; iterative uses fixed memory; recursive often shorter/clearer.', '1 mark per point, max 3 [3]'),
    lambda r, d: (lambda f: ('Write an iterative version of:\n' + code(f['lines']), code([f['lines'][0]] + [IND + l for l in f['it']] + ['ENDFUNCTION']), '1 mark loop; 1 mark update; 1 mark return [3]'))(recfun(r, 2))], k=(3, 4))

t11_3 = topic('How compilers implement recursion using a call stack', 'compilers implement recursion', 'call stack')
t11_3.fixed('C1', (1, 2), [
    ('What does the compiler generate for each subroutine call?', 'Code to push a stack frame (return address, parameters, locals) onto the call stack and jump to the subroutine', 'On return the frame is popped and execution resumes at the return address.', ['Code to copy the whole program', 'A new compiler for each call', 'A queue of instructions']),
    ('Why is a stack used for subroutine calls?', 'The most recent call must return first (LIFO)', 'Nested and recursive calls return in reverse order.', ['Because it is sorted', 'Because it is a FIFO structure', 'Because it uses the least disk space']),
    ('What is the return address?', 'The address of the instruction to continue from after the subroutine finishes', 'Stored in the stack frame when the call is made.', ['The address of the subroutine', 'The address of the stack', 'The value returned by the function']),
    ('What happens to a stack frame when a call returns?', 'It is popped (removed) from the call stack', 'Local variables of that call are lost.', ['It is moved to a queue', 'It stays on the stack for ever', 'It is written to a file']),
    ('What causes a stack overflow error?', 'Too many frames are pushed onto the call stack, exceeding its size', 'Usually from recursion that is too deep or has no base case.', ['A division by zero', 'A missing semicolon', 'A file that is not found']),
])
t11_3.fixed('C2', (2, 3, 4), [
    ('Explain how the call stack allows each recursive call to have its own copy of local variables.', 'A new stack frame is created for every call, holding its own parameters and local variables; frames for earlier calls remain unchanged below it.', '1 mark each [2]'),
    ('Explain how the value returned by a recursive call is used by the calling instance.', 'When the call returns, its frame is popped; the return value is passed back (e.g. in a register/on the stack) and execution resumes at the return address in the caller, which uses it in its expression.', '1 mark per point, max 2 [2]'),
])
ar(t11_3, [('Each recursive call has its own local variables.', 'A new stack frame is pushed for every call.'),
           ('Recursive calls return in the reverse order to which they were made.', 'The call stack is a last in, first out structure.')],
    ['The call stack is a first in, first out structure.', 'Local variables are shared by all recursive calls.', 'Return addresses are stored in the symbol table.'])


@t11_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_3_frames(r, D):
    kind = r.choice(['fact', 'sum', 'power', 'digits'])
    f = recfun(r, D, kind)
    call = f['call']
    nm = call.split('(')[0]
    args = [int(x) for x in call.split('(')[1][:-1].split(', ')]
    if kind == 'power':
        bb, e = args
        frames = [f'{nm}({bb}, {e - k})' for k in range(e + 1)]
    elif kind == 'digits':
        frames, x = [], args[0]
        while True:
            frames.append(f'{nm}({x})')
            if x < 10:
                break
            x //= 10
    else:
        n = args[0]
        lo = 1 if kind == 'fact' else 0
        frames = [f'{nm}({k})' for k in range(n, lo - 1, -1)]
    if D == 1:
        return MCQ(r, 'Study the function:\n' + code(f['lines']) + f'\nWhen {call} is evaluated, what is the maximum number of frames for this function on the call stack at the same time?', str(f['depth']),
                   [str(f['depth'] + 1), str(f['depth'] - 1), str(f['v']), str(f['depth'] * 2)], f'Frames: {", ".join(frames)} = {f["depth"]}.')
    return Q('Study the function:\n' + code(f['lines']) + f'\n{call} is evaluated. Describe the contents of the call stack when the base case is reached (top of stack last), and explain how the final result is produced.',
             f'Frames (bottom to top): {", ".join(frames)}; each holds return address, parameter(s) and space for local values. The base case returns, then each frame is popped in turn and its return value used by the caller: {f["unwind"]}; result {f["v"]}.',
             f'frames listed in order [2]; contents of a frame [1]; unwinding/result [1] [4]', marks=4)


scen(t11_3, 'C2', (2, 3, 4), [
    '{p} is investigating why a recursive program written for {org} crashes with very large inputs.', 'A recursive function at {org} works for small values but fails for large ones.',
], [('Explain why the program fails for large inputs.', 'Each recursive call adds a stack frame; for very large inputs the call stack runs out of memory (stack overflow).', '1 mark each [2]'),
    ('Describe what is stored in each stack frame.', 'Return address, parameters, local variables (and the return value).', '1 mark per item, max 2 [2]'),
    ('Suggest how the problem could be solved.', 'Rewrite iteratively; increase stack size; use tail recursion optimisation or memoisation.', '1 mark each [2]')], k=(2, 3))
scen(t11_3, 'C4', (3, 4, 5), [
    '{p} is writing a compiler for a language that supports recursion at {org}.', 'A computer science student at {org} is explaining recursion to a class.',
], [('Describe how the compiled code uses the call stack when a subroutine is called and when it returns.', 'Call: push return address, parameters and local variables (frame), jump to subroutine. Return: pop frame, pass back result, jump to return address.', '1 mark per point, max 4 [4]'),
    lambda r, d: (lambda f: ('Study:\n' + code(f['lines']) + f'\nState the maximum number of frames for this function on the call stack when {f["call"]} is evaluated, and the value returned.', f'{f["depth"]} frames; returns {f["v"]}', '1 mark each [2]'))(recfun(r, 3, r.choice(['fact', 'sum', 'power']))),
    ('Explain why recursion would not be possible without a stack.', 'Each active call needs its own return address and variables; a single fixed storage area would be overwritten by the next call.', '1 mark each [2]'),
    ('Explain why recursive programs may run slower than iterative ones.', 'Overhead of pushing/popping frames and jumping for every call.', '1 mark each [2]')], k=(2, 3))

CHAPTERS[11] = [t11_1, t11_2, t11_3]

# =============================================================================== Chapter 12 Programming paradigms
t12_1 = topic('Low-level programming: addressing modes revisited', 'low-level programming', 'addressing modes')
MODES = [('immediate', 'the operand is the value to be used', 'LDM #25'), ('direct', 'the operand is the address of the value', 'LDD 200'),
         ('indirect', 'the operand is an address that holds the address of the value', 'LDI 200'), ('indexed', 'the address of the value is the operand plus the contents of the index register', 'LDX 200'),
         ('relative', 'the address of the value is calculated relative to the address of the current instruction (or a base address)', 'JMP +4')]
t12_1.fixed('C1', (1, 2), [(f'Which addressing mode is described as: {d}?', n.capitalize(), f'{n}: {d}; e.g. {e}.', [x[0].capitalize() for x in MODES if x[0] != n][:4]) for n, d, e in MODES] + [
    ('Which addressing mode is most useful for accessing consecutive elements of an array?', 'Indexed', 'Incrementing IX moves to the next element.', ['Immediate', 'Direct', 'Relative']),
    ('Why does relative addressing make code relocatable?', 'Addresses are offsets from the current instruction, so the program works wherever it is loaded', 'No absolute addresses need changing.', ['It uses fewer registers', 'It stores data in the instruction', 'It always uses address 0']),
])
t12_1.fixed('C2', (2, 3, 4), [
    ('Explain why indirect addressing is useful.', 'The address held in memory can be changed at run time, so the same instruction can access different locations (like a pointer); it also allows access to a larger address range.', '1 mark each [2]'),
    ('Explain the difference between direct and indexed addressing.', 'Direct uses the operand as the address; indexed adds the index register to the operand to form the address, so the same instruction can access a sequence of locations.', '1 mark each [2]'),
])
ar(t12_1, [('Indexed addressing suits processing arrays.', 'The index register can be incremented to move to the next element.'),
           ('Immediate addressing needs no extra memory access to fetch the data.', 'The value is part of the instruction itself.'),
           ('Relative addressing allows code to be loaded anywhere in memory.', 'Addresses are calculated as offsets rather than fixed locations.')],
    ['Direct addressing adds the index register to the operand.', 'Immediate addressing uses the operand as an address.', 'Indirect addressing never needs memory access.'])


@t12_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_1_prog(r, D):
    base, mem, ix = _addr_setup(r)
    out = base + 10
    steps = r.sample(['LDD', 'LDI', 'LDX', 'LDM'], 1 if D <= 2 else 2)
    prog, a = {}, 50
    prog[a] = ('LDR', f'#{ix}')
    a += 1
    first = True
    for m in steps:
        loc = base + (1 if m == 'LDI' else r.randrange(0, 3))
        if first:
            prog[a] = (m, f'#{r.randrange(5, 40)}' if m == 'LDM' else str(loc))
            first = False
        else:
            prog[a] = ('ADD', f'#{r.randrange(2, 20)}' if m == 'LDM' else str(base + r.randrange(0, 6)))
        a += 1
    if D >= 3:
        prog[a] = ('ADD', f'#{r.randrange(1, 9)}')
        a += 1
    prog[a] = ('STO', str(out))
    prog[a + 1] = ('END', '')
    sim = Asm(prog, mem)
    if not sim.run(50):
        return None
    stem = f'The memory contains {mem_text(mem)}. The program below runs, starting at address 50.\n' + asm_text(prog) + f'\nState the value in the accumulator when the program ends and the value stored in address {out}.'
    tr = '; '.join(f'{op} {o}'.strip() + f' → ACC {acc}, IX {x}' for _, op, o, acc, x in sim.trace if op not in ('END',))
    if D == 1:
        return MCQ(r, stem.replace('State the value in the accumulator when the program ends and the value stored in address', 'What value is stored in address').rstrip('.') + '?', str(sim.acc),
                   [str(x) for x in (sim.acc + ix, sim.acc - ix, mem[base], mem[base + 1], sim.acc + 1)], tr + '.')
    return Q(stem, f'ACC = {sim.acc}; [{out}] = {sim.m[out]}', f'{tr} [{len(sim.trace) - 2}]; final value [1] [{len(sim.trace) - 1}]', marks=min(len(sim.trace) - 1, 6))


@t12_1.add('C3', (2, 3, 4, 5), 'numerical')
def t12_1_rel(r, D):
    cur = r.randrange(100, 400)
    off = r.choice([-6, -4, -3, 2, 3, 4, 5, 7, 9])
    base = r.randrange(500, 900)
    k = r.randrange(0, 12)
    return Q(f'(a) An instruction stored at address {cur} uses relative addressing with operand {off:+d}, where the address is the address of the current instruction plus the operand. State the address accessed. '
             f'(b) A program is loaded with its base address in a register holding {base}. An instruction uses base-relative addressing with offset {k}. State the address accessed, and explain why this helps when the program is moved in memory.',
             f'(a) {cur + off} (b) {base + k}; only the base register changes when the program is moved, so the instructions need no changes (relocatable code).', f'(a) {cur} {off:+d} = {cur + off} [1] (b) {base} + {k} = {base + k} [1]; explanation [1] [3]', marks=3)


scen(t12_1, 'C4', (3, 4, 5), [
    '{p} is writing assembly code for a microcontroller used by {org}.', 'An embedded system at {org} in {city} processes a table of sensor readings in assembly language.',
], [lambda r, d: (lambda q: (q['stem'], q['answer'], q['key']) if q else None)(t12_1_prog(r, 3)),
    ('Explain why indexed addressing is suitable for processing the table of readings.', 'IX is incremented each pass of a loop, so the same LDX instruction reads successive elements.', '1 mark each [2]'),
    ('Describe the difference between immediate and indirect addressing.', 'Immediate: operand is the value. Indirect: operand is an address whose contents is the address of the value.', '1 mark each [2]'),
    ('Explain one reason why relative addressing is used for jumps.', 'Code is relocatable; branch targets stay correct wherever the program is loaded.', '1 mark each [2]')], k=(3, 4))

t12_2 = topic('Imperative (procedural) programming', 'imperative', 'procedural programming')
t12_2.fixed('C1', (1, 2), [
    ('What is the main feature of imperative programming?', 'The program is a sequence of statements that change the program state (values of variables)', 'It describes how to solve a problem step by step.', ['The program states facts and rules', 'The program is a set of objects only', 'The program has no variables']),
    ('Procedural programming is imperative programming that', 'is structured into procedures and functions', 'e.g. Python, Pascal, C, Cambridge pseudocode.', ['uses only facts and rules', 'cannot use loops', 'only uses machine code']),
    ('Which language is mainly procedural?', 'C', 'Prolog is declarative; Java is mainly object-oriented.', ['Prolog', 'SQL', 'HTML']),
    ('What is a global variable?', 'A variable that can be accessed anywhere in the program', 'Local variables are accessible only within their subroutine.', ['A variable inside one procedure only', 'A constant', 'A parameter']),
    ('Which programming constructs are used in imperative programming?', 'Sequence, selection and iteration', 'These control the order of statement execution.', ['Facts, rules and goals', 'Classes and objects only', 'Opcodes and operands only']),
])
t12_2.fixed('C2', (2, 3, 4), [
    ('Explain the difference between imperative and declarative programming.', 'Imperative: the programmer gives the steps (how) that change state; declarative: the programmer states facts/rules (what) and the system works out how to find the answer.', '1 mark each [2]'),
    ('Explain why using local variables rather than global variables is good practice in procedural programming.', 'Subroutines are self-contained, so they can be tested and reused independently; there is less risk of accidentally changing a value used elsewhere.', '1 mark each [2]'),
])
ar(t12_2, [('Procedural programs are made of subroutines.', 'Procedural programming structures an imperative program into procedures and functions.'),
           ('A local variable with the same name as a global variable hides the global one.', 'Inside the subroutine the local declaration is used.')],
    ['Imperative programs only contain facts and rules.', 'Global variables can only be used in one procedure.', 'Procedural languages cannot use loops.'])


@t12_2.add('C3', (1, 2, 3, 4, 5))
def t12_2_scope(r, D):
    g0, l0, k = r.randrange(1, 20), r.randrange(20, 50), r.randrange(2, 6)
    vn = r.choice(['Count', 'Total', 'Score', 'Level'])
    variant = r.choice(['shadow', 'global', 'param'])
    if variant == 'shadow':
        lines = [f'DECLARE {vn} : INTEGER', f'{vn} ← {g0}', 'PROCEDURE Update()', f'{IND}DECLARE {vn} : INTEGER', f'{IND}{vn} ← {l0}', f'{IND}OUTPUT {vn}', 'ENDPROCEDURE', 'CALL Update()', f'OUTPUT {vn}']
        out, why = f'{l0} {g0}', f'the procedure declares a local {vn} that hides the global one; the global {vn} is unchanged'
    elif variant == 'global':
        lines = [f'DECLARE {vn} : INTEGER', f'{vn} ← {g0}', 'PROCEDURE Update()', f'{IND}{vn} ← {vn} * {k}', f'{IND}OUTPUT {vn}', 'ENDPROCEDURE', 'CALL Update()', 'CALL Update()', f'OUTPUT {vn}']
        out, why = f'{g0 * k} {g0 * k * k} {g0 * k * k}', f'no local declaration, so the procedure changes the global {vn} each call'
    else:
        lines = [f'DECLARE {vn} : INTEGER', f'{vn} ← {g0}', f'PROCEDURE Update(BYVAL X : INTEGER)', f'{IND}X ← X + {l0}', f'{IND}{vn} ← {vn} + {k}', f'{IND}OUTPUT X', 'ENDPROCEDURE', f'CALL Update({vn})', f'OUTPUT {vn}']
        out, why = f'{g0 + l0} {g0 + k}', f'X is a copy of {vn} ({g0}) so X = {g0 + l0}; the global {vn} is changed directly to {g0 + k}'
    stem = 'Study the procedural program:\n' + code(lines) + '\nState the output.'
    if D <= 2:
        return MCQ(r, stem.replace('State the output.', 'What is output?'), out, [f'{g0} {g0}', f'{l0} {l0}', f'{g0 * k} {g0}', f'{g0 + l0} {g0}', f'{g0} {g0 + k}'], why[0].upper() + why[1:] + '.')
    return Q(stem + ' Explain your answer with reference to the scope of the variables.', out, f'output {out} [1]; {why} [1] [2]', marks=2)


@t12_2.add('C3', (1, 2, 3, 4))
def t12_2_classify(r, D):
    snips = [(['grandparent(X, Z) :- parent(X, Y), parent(Y, Z).'], 'declarative', 'it states a rule; the system searches for solutions'),
             (['FOR i ← 1 TO 10', f'{IND}Total ← Total + i', 'NEXT i'], 'imperative (procedural)', 'it gives a sequence of steps that change variables'),
             (['LDD 200', 'ADD #5', 'STO 201'], 'low-level', 'it uses assembly mnemonics and memory addresses'),
             (['CLASS Car', f'{IND}PRIVATE Speed : INTEGER', f'{IND}PUBLIC PROCEDURE Accelerate()', f'{IND}{IND}Speed ← Speed + 10', f'{IND}ENDPROCEDURE', 'ENDCLASS'], 'object-oriented', 'it defines a class with private attributes and methods'),
             (['SELECT Name FROM Student WHERE Age > 16;'], 'declarative', 'it states what data is wanted, not how to find it'),
             (['likes(amara, pizza).', 'likes(kenji, sushi).'], 'declarative', 'these are facts in a knowledge base'),
             (['PROCEDURE Swap(BYREF A : INTEGER, BYREF B : INTEGER)', f'{IND}Temp ← A', f'{IND}A ← B', f'{IND}B ← Temp', 'ENDPROCEDURE'], 'imperative (procedural)', 'a procedure made of statements that change state'),
             (['LDX 300', 'INC IX', 'CMP #0', 'JPE 120'], 'low-level', 'assembly instructions using indexed addressing and jumps')]
    lines, par, why = r.choice(snips)
    if D <= 2:
        return MCQ(r, 'Which programming paradigm is shown by this code?\n' + code(lines), par.split(' (')[0].capitalize(), ['Declarative', 'Imperative', 'Low-level', 'Object-oriented'], f'{par}: {why}.')
    return Q('Identify the programming paradigm shown by this code and give a reason.\n' + code(lines), f'{par}: {why}.', '1 mark paradigm; 1 mark reason [2]', marks=2)


scen(t12_2, 'C4', (3, 4, 5), [
    '{org} in {city} is choosing a paradigm for a new payroll program.', '{p} has written a procedural program for {org} and a colleague suggests an object-oriented version.',
], [('Describe the features of procedural programming.', 'Sequence of instructions; procedures/functions with parameters; local and global variables; selection and iteration; state changed by assignment.', '1 mark per point, max 3 [3]'),
    lambda r, d: (lambda q: (q['stem'].replace('Study the procedural program:', 'Part of the program is shown:'), q['answer'], q['key']))(t12_2_scope(r, 3)),
    ('Compare procedural and object-oriented programming for a large project.', 'OOP: encapsulation, reuse through inheritance, easier maintenance by teams; procedural: simpler, efficient for smaller tasks, data and functions separate.', '1 mark per point, max 3 [3]'),
    ('Explain why parameters are preferred to global variables.', 'Makes subroutines independent and reusable; reduces side effects; easier testing.', '1 mark each [2]')], k=(3, 4))

FAM = ['amara', 'lucas', 'sofia', 'kenji', 'zara', 'mateo', 'aisha', 'noah', 'leila', 'omar', 'priya', 'ravi', 'hana', 'jonas', 'ines', 'kwame']


def family(r):
    g = r.sample(FAM, 10)
    a, kids, gk = g[0], g[1:4], g[4:10]
    facts = [(a, k) for k in kids]
    rest = gk[:]
    for k in kids[:2]:
        n = r.randrange(1, 4)
        for _ in range(n):
            if rest:
                facts.append((k, rest.pop(0)))
    return facts


t12_3 = topic('Declarative programming: facts, rules and goals (Prolog-style)', 'declarative programming', 'facts, rules and goals', 'prolog')
t12_3.fixed('C1', (1, 2), [
    ('In declarative programming, the programmer writes', 'facts and rules, and the system finds answers to goals (queries)', 'The programmer states what, not how.', ['a step-by-step algorithm', 'machine code', 'classes and objects only']),
    ('In Prolog, how is a variable distinguished from a constant (atom)?', 'Variables start with an upper-case letter; constants start with a lower-case letter', 'e.g. parent(X, amara).', ['Variables are in quotation marks', 'Variables are numbers', 'There is no difference']),
    ('What is a goal in Prolog?', 'A query that the system tries to satisfy using the facts and rules', 'e.g. ?- parent(X, sofia).', ['A fact in the knowledge base', 'A comment', 'A loop']),
    ('What does the symbol :- mean in a Prolog rule?', 'IF', 'head :- body means the head is true if the body is true.', ['AND', 'OR', 'NOT']),
    ('In a Prolog rule, what does a comma between conditions mean?', 'AND', 'All conditions must be true.', ['OR', 'IF', 'NOT']),
    ('How does Prolog find answers to a goal?', 'By searching the facts and rules in order, matching (unifying) and backtracking', 'Backtracking tries alternatives when a match fails.', ['By executing statements in sequence', 'By sorting the facts', 'By random guessing']),
])
t12_3.fixed('C2', (2, 3, 4), [
    ('Explain what is meant by backtracking in declarative programming.', 'When a goal fails (or more solutions are wanted) the system goes back to the most recent choice point and tries the next matching fact or rule.', '1 mark each [2]'),
    ('Explain why declarative languages are suited to expert systems.', 'Knowledge is naturally expressed as facts and rules; the inference engine searches them to answer queries, so new knowledge can be added easily without rewriting algorithms.', '1 mark each [2]'),
])
ar(t12_3, [('Prolog can give more than one answer to a goal.', 'It backtracks to find further matches in the knowledge base.'),
           ('In Prolog, Parent is a variable but parent is not.', 'Variables begin with an upper-case letter.'),
           ('A Prolog rule can use other rules.', 'The body of a rule can contain any goals, including rule heads.')],
    ['Prolog programs are a sequence of assignment statements.', 'In Prolog a comma means OR.', 'Facts in Prolog must contain variables.'])


@t12_3.add('C3', (1, 2, 3, 4, 5))
def t12_3_family(r, D):
    facts = family(r)
    fx = ' '.join(f'parent({a}, {c}).' for a, c in facts)
    rule = 'grandparent(X, Z) :- parent(X, Y), parent(Y, Z).'
    people = sorted({x for f in facts for x in f})
    kind = r.choice(['children', 'parent'] if D <= 2 else ['children', 'grand', 'grandof', 'sib'])
    if kind == 'children':
        p = r.choice([a for a, _ in facts])
        res = [c for a, c in facts if a == p]
        goal = f'parent({p}, C)'
    elif kind == 'parent':
        c0 = r.choice([c for _, c in facts])
        res = [a for a, c in facts if c == c0]
        goal = f'parent(P, {c0})'
    elif kind == 'grand':
        g = facts[0][0]
        res = [z for a, y in facts if a == g for a2, z in facts if a2 == y]
        goal = f'grandparent({g}, G)'
    elif kind == 'grandof':
        z0 = r.choice([z for a, y in facts if a == facts[0][0] for a2, z in facts if a2 == y])
        res = [x for x, y in facts for y2, z in facts if y2 == y and z == z0]
        goal = f'grandparent(X, {z0})'
    else:
        rule = 'sibling(A, B) :- parent(P, A), parent(P, B), A \\= B.'
        a0 = r.choice([c for _, c in facts])
        res = [b for p, a in facts if a == a0 for p2, b in facts if p2 == p and b != a0]
        goal = f'sibling({a0}, S)'
    var = re.findall(r'[A-Z]\w*', goal)[0]
    ansl = ', '.join(f'{var} = {x}' for x in res) if res else 'false (no solutions)'
    stem = f'A knowledge base contains the facts: {fx} and the rule {rule} State the result(s) of the goal {goal}.'
    if D == 1:
        if not res:
            return None
        wrong = [', '.join(r.sample(people, len(res))) for _ in range(5)]
        return MCQ(r, f'A knowledge base contains the facts: {fx} What is returned for the goal {goal}?', ', '.join(res), [w for w in wrong if w != ', '.join(res)] + ['false'], f'{ansl}.')
    return Q(stem, ansl, f'each correct result, in knowledge-base order [{max(1, min(len(res), 3))}]', marks=max(1, min(len(res), 3)) + (1 if D >= 4 else 0)) if D < 4 else \
        Q(stem + ' Explain how backtracking is used to find all the results.', ansl + '. After each match the system backtracks to the last choice point and tries the next fact.', f'results [{max(1, min(len(res), 3))}]; backtracking explained [1] [{max(1, min(len(res), 3)) + 1}]', marks=max(1, min(len(res), 3)) + 1)


@t12_3.add('C3', (2, 3, 4, 5))
def t12_3_flights(r, D):
    cs = r.sample(['nairobi', 'lima', 'dubai', 'lisbon', 'cairo', 'hanoi', 'doha', 'accra', 'madrid', 'seoul'], 5)
    fl = []
    for _ in range(7):
        a, c = r.sample(cs, 2)
        if (a, c) not in [(x, y) for x, y, _ in fl]:
            fl.append((a, c, r.randrange(80, 600, 10)))
    src = r.choice([a for a, _, _ in fl])
    lim = r.choice([200, 250, 300, 350, 400])
    q = r.choice(['cheap', 'to', 'two'] if D >= 4 else ['cheap', 'to'])
    fx = ' '.join(f'flight({a}, {c}, {p}).' for a, c, p in fl)
    if q == 'cheap':
        res = [f'D = {c}, C = {p}' for a, c, p in fl if a == src and p < lim]
        goal = f'flight({src}, D, C), C < {lim}'
        rule = ''
    elif q == 'to':
        dst = r.choice([c for _, c, _ in fl])
        res = [f'S = {a}' for a, c, _ in fl if c == dst]
        goal = f'flight(S, {dst}, _)'
        rule = ''
    else:
        rule = ' The rule route(A, B, T) :- flight(A, X, P1), flight(X, B, P2), T is P1 + P2. is added.'
        res = [f'B = {c2}, T = {p1 + p2}' for a, x, p1 in fl if a == src for x2, c2, p2 in fl if x2 == x]
        goal = f'route({src}, B, T)'
    if not res:
        return None
    ansl = '; '.join(res)
    n = max(1, min(len(res), 3))
    return Q(f'Facts flight(From, To, Price) are stored: {fx}{rule} State all the results returned for the goal {goal}.', ansl, f'1 mark per correct result, in order [{n}]', marks=n)


@t12_3.add('C3', (2, 3, 4))
def t12_3_write(r, D):
    tasks = [('a rule ancestor(A, D) that is true if A is a parent of D, or a parent of an ancestor of D', 'ancestor(A, D) :- parent(A, D).\nancestor(A, D) :- parent(A, X), ancestor(X, D).', '1 mark base clause; 1 mark recursive clause [2]'),
             ('a rule cousin(A, B) using parent/2 and a sibling/2 rule', 'cousin(A, B) :- parent(P, A), parent(Q, B), sibling(P, Q).', '1 mark parents; 1 mark sibling condition [2]'),
             ('a goal to find every film F that is longer than 120 minutes, given facts film(Title, Minutes)', 'film(F, M), M > 120.', '1 mark goal; 1 mark condition [2]'),
             ('a rule cheap(Item) that is true if the price of Item is less than 10, given facts price(Item, P)', 'cheap(Item) :- price(Item, P), P < 10.', '1 mark head; 1 mark body [2]'),
             ('a rule can_vote(X) that is true if X is aged 18 or over, given facts age(Name, Years)', 'can_vote(X) :- age(X, A), A >= 18.', '1 mark head; 1 mark body [2]'),
             ('a rule same_team(A, B) that is true if A and B play for the same team and are different people, given facts plays_for(Player, Team)', 'same_team(A, B) :- plays_for(A, T), plays_for(B, T), A \\= B.', '1 mark shared T; 1 mark A \\= B [2]')]
    t, a, k = r.choice(tasks)
    d = ctx(r)
    return Q(f'{d["p"]} is building a knowledge base for {d["org"]}. Write {t}.', a, k, marks=2)


scen(t12_3, 'C4', (3, 4, 5), [
    '{org} in {city} is developing an expert system using a declarative language.', '{p} is writing a Prolog knowledge base about family relationships for a genealogy app developed in {city}.',
], [lambda r, d: (lambda q: (q['stem'], q['answer'], q['key']))(t12_3_family(r, 3)),
    ('Explain the difference between a fact and a rule.', 'A fact is unconditionally true (e.g. parent(a, b).); a rule is true if its conditions are satisfied (head :- body).', '1 mark each [2]'),
    ('Describe how the system answers a goal.', 'Searches facts and rules in order; unifies variables with matching values; uses backtracking to find alternative solutions.', '1 mark per point [3]'),
    ('Explain one advantage and one disadvantage of a declarative language for this application.', 'Advantage: knowledge expressed directly as facts/rules, easy to add more. Disadvantage: harder to control efficiency/order; less suited to general-purpose tasks or I/O.', '1 mark each [2]')], k=(3, 4))

CHAPTERS[12] = [t12_1, t12_2, t12_3]

# =============================================================================== Chapter 13 Object-oriented programming
ACCT = [('Account', 'Balance'), ('Wallet', 'Funds'), ('PrepaidCard', 'Credit'), ('SavingsPot', 'Saved')]


def acct_prog(r, D):
    cls, att = r.choice(ACCT)
    obj = r.choice(['MyAccount', 'Card1', 'Pot', 'UserWallet', 'Acc'])
    start = r.randrange(5, 30) * 10
    lines = [f'CLASS {cls}', f'{IND}PRIVATE {att} : INTEGER', f'{IND}PUBLIC PROCEDURE NEW(Start : INTEGER)', f'{IND}{IND}{att} ← Start', f'{IND}ENDPROCEDURE',
             f'{IND}PUBLIC PROCEDURE Deposit(Amount : INTEGER)', f'{IND}{IND}{att} ← {att} + Amount', f'{IND}ENDPROCEDURE',
             f'{IND}PUBLIC FUNCTION Withdraw(Amount : INTEGER) RETURNS BOOLEAN', f'{IND}{IND}IF Amount <= {att} THEN', f'{IND}{IND}{IND}{att} ← {att} - Amount', f'{IND}{IND}{IND}RETURN TRUE',
             f'{IND}{IND}ELSE', f'{IND}{IND}{IND}RETURN FALSE', f'{IND}{IND}ENDIF', f'{IND}ENDFUNCTION', f'{IND}PUBLIC FUNCTION Get{att}() RETURNS INTEGER', f'{IND}{IND}RETURN {att}', f'{IND}ENDFUNCTION', 'ENDCLASS']
    main = [f'{obj} ← NEW {cls}({start})']
    bal, outs = start, []
    for _ in range(3 if D <= 2 else 5):
        k = r.choice(['dep', 'wd', 'wd', 'get'])
        v = r.randrange(2, 30) * 10
        if k == 'dep':
            main.append(f'CALL {obj}.Deposit({v})')
            bal += v
        elif k == 'wd':
            main.append(f'OUTPUT {obj}.Withdraw({v})')
            ok = v <= bal
            outs.append('TRUE' if ok else 'FALSE')
            if ok:
                bal -= v
        else:
            main.append(f'OUTPUT {obj}.Get{att}()')
            outs.append(str(bal))
    main.append(f'OUTPUT {obj}.Get{att}()')
    outs.append(str(bal))
    return lines, main, outs, bal, cls, att, obj


t13_1 = topic('Classes, objects, attributes, methods and encapsulation', 'classes, objects, attributes, methods', 'encapsulation')
t13_1.fixed('C1', (1, 2), [
    ('What is a class?', 'A template (blueprint) that defines the attributes and methods of a type of object', 'Objects are instances of a class.', ['A single instance of an object', 'A variable that holds a number', 'A subroutine that returns a value']),
    ('What is an object?', 'An instance of a class', 'Created with NEW; has its own attribute values.', ['A template for creating classes', 'A data type such as INTEGER', 'A method of a class']),
    ('What is encapsulation?', 'Combining data and the methods that act on it in one class, and hiding the data from outside access', 'Attributes are PRIVATE; access is through PUBLIC methods.', ['Creating a new class from an existing class', 'Using one method name for different actions', 'Storing objects in a file']),
    ('What is a method?', 'A procedure or function defined in a class', 'Methods define the behaviour of objects.', ['An attribute of a class', 'A type of loop', 'A class with no attributes']),
    ('What is an attribute?', 'A data item (property) stored by an object', 'e.g. Balance in an Account class.', ['A procedure in a class', 'The name of a class', 'A parameter of the constructor only']),
    ('Why are attributes usually declared PRIVATE?', 'So they can only be changed through the class\'s methods, which can validate changes', 'This is information hiding / encapsulation.', ['To make the program run faster', 'So they can be accessed from anywhere', 'Because PUBLIC attributes are not allowed']),
])
t13_1.fixed('C2', (2, 3, 4), [
    ('Explain how encapsulation helps to keep an object\'s data valid.', 'Attributes are private, so the only way to change them is through public methods, which can check (validate) new values before changing the data.', '1 mark each [2]'),
    ('Explain the difference between a class and an object.', 'A class is the definition/template of attributes and methods; an object is a particular instance created from the class with its own attribute values.', '1 mark each [2]'),
])
ar(t13_1, [('Several objects can be created from one class.', 'A class is a template that defines attributes and methods.'),
           ('Private attributes cannot be changed directly from the main program.', 'Encapsulation restricts access to the methods of the class.'),
           ('Each object has its own copy of its instance attributes.', 'Attribute values belong to the instance, not to the class definition.')],
    ['An object is a template for a class.', 'Methods are the data stored by an object.', 'Private attributes can be accessed from anywhere in the program.'])


@t13_1.add('C3', (1, 2, 3, 4, 5))
def t13_1_trace(r, D):
    lines, main, outs, bal, cls, att, obj = acct_prog(r, D)
    stem = 'The class is defined:\n' + code(lines) + '\nThe main program is:\n' + code(main) + '\n'
    if D == 1:
        return MCQ(r, stem + 'What is the final value output?', str(bal), [str(bal + 10), str(int(main[0].split('(')[1][:-1])), str(abs(bal - 50)), str(bal * 2) if bal else '10'], f'Final {att} = {bal}.')
    return Q(stem + 'State the output of the main program.', ' '.join(outs), f'Withdraw returns FALSE and leaves {att} unchanged if Amount > {att}; outputs ' + ', '.join(outs) + f' [{min(len(outs), 4)}]', marks=min(len(outs), 4))


SPECS = [('Book', [('Title', 'STRING'), ('Author', 'STRING'), ('Pages', 'INTEGER')], ['GetTitle', 'SetPages']),
         ('Car', [('Registration', 'STRING'), ('Mileage', 'INTEGER'), ('Price', 'REAL')], ['GetMileage', 'SetPrice']),
         ('Sensor', [('SensorID', 'STRING'), ('Reading', 'REAL'), ('Active', 'BOOLEAN')], ['GetReading', 'SetActive']),
         ('Player', [('Name', 'STRING'), ('Score', 'INTEGER'), ('Level', 'INTEGER')], ['GetScore', 'SetLevel']),
         ('Room', [('RoomNumber', 'INTEGER'), ('Capacity', 'INTEGER'), ('Booked', 'BOOLEAN')], ['GetCapacity', 'SetBooked']),
         ('Product', [('Code', 'STRING'), ('Description', 'STRING'), ('Stock', 'INTEGER')], ['GetStock', 'SetDescription'])]


@t13_1.add('C3', (2, 3, 4, 5))
def t13_1_diagram(r, D):
    nm, atts, meths = r.choice(SPECS)
    d = ctx(r)
    att_s = ', '.join(f'{a} ({t})' for a, t in atts)
    ans = code([nm, '-' * 20] + [f'- {a} : {t}' for a, t in atts] + ['-' * 20, f'+ Constructor({", ".join(a for a, _ in atts)})'] + [f'+ {m}()' for m in meths])
    return Q(f'{d["org"]} in {d["city"]} needs a class {nm} with the private attributes {att_s}, a constructor, and the public methods {meths[0]} and {meths[1]}. Draw (write out) the class diagram, showing which members are private (−) and public (+).',
             ans, '1 mark class name; 1 mark private attributes with types; 1 mark public methods [3]', marks=3)


scen(t13_1, 'C4', (3, 4, 5), [
    '{org} in {city} is writing an object-oriented system to manage customer accounts.', '{p} is designing classes for a library system at {org}.',
], [lambda r, d: (lambda x: ('The class and program are:\n' + code(x[0]) + '\n' + code(x[1]) + '\nState the output.', ' '.join(x[2]), '1 mark per correct output, max 3 [3]'))(acct_prog(r, 2)),
    ('Explain why the attribute is declared PRIVATE.', 'So it can only be changed through the methods (e.g. Withdraw checks the amount), protecting data integrity.', '1 mark each [2]'),
    ('Explain the difference between a class and an object in this system.', 'Class: the template for all accounts; object: one particular account with its own balance.', '1 mark each [2]'),
    ('Describe two benefits of using OOP for this system.', 'Encapsulation protects data; classes can be reused/inherited; easier maintenance; models real-world entities.', '1 mark each [2]')], k=(3, 4))

t13_2 = topic('Constructors, getters and setters; instance and private attributes', 'constructors', 'getters and setters', 'instance and private attributes')
t13_2.fixed('C1', (1, 2), [
    ('What is a constructor?', 'A method that is called when an object is created, to initialise its attributes', 'In Cambridge pseudocode it is PROCEDURE NEW(...).', ['A method that deletes an object', 'A method that returns an attribute', 'A class with no methods']),
    ('What is a getter?', 'A method that returns the value of a private attribute', 'e.g. FUNCTION GetName() RETURNS STRING.', ['A method that changes an attribute', 'A method that creates an object', 'A public attribute']),
    ('What is a setter?', 'A method that changes the value of a private attribute, often after validation', 'e.g. PROCEDURE SetAge(NewAge : INTEGER).', ['A method that returns an attribute', 'A constructor', 'A private attribute']),
    ('What is an instance attribute?', 'An attribute whose value belongs to a particular object', 'Each object has its own copy.', ['An attribute shared by all objects of a class', 'A method of a class', 'A local variable in the main program']),
    ('In Cambridge pseudocode, how is an object created?', 'Obj ← NEW ClassName(parameters)', 'NEW calls the constructor.', ['DECLARE Obj : NEW', 'CALL ClassName(parameters)', 'Obj ← ClassName.CREATE()']),
])
t13_2.fixed('C2', (2, 3, 4), [
    ('Explain why setters are used instead of making attributes public.', 'A setter can validate the new value before changing the private attribute, so invalid data cannot be stored; the internal representation can change without affecting other code.', '1 mark each [2]'),
    ('Explain why a constructor is needed.', 'It makes sure every new object starts in a valid state with all attributes initialised (possibly from parameters).', '1 mark each [2]'),
])
ar(t13_2, [('A setter can reject invalid values.', 'It can check the value before it updates the private attribute.'),
           ('The constructor runs automatically when an object is created.', 'NEW calls the constructor to initialise the attributes.'),
           ('Two objects of the same class can hold different values.', 'Instance attributes belong to each object separately.')],
    ['A getter changes the value of an attribute.', 'A constructor is called when an object is deleted.', 'Private attributes can be read directly by the main program.'])


@t13_2.add('C3', (2, 3, 4, 5))
def t13_2_write(r, D):
    nm, atts, meths = r.choice(SPECS)
    lo, hi = r.choice([(0, 100), (1, 500), (0, 1000), (1, 50)])
    num = [a for a, t in atts if t in ('INTEGER', 'REAL')]
    va = num[-1] if num else atts[-1][0]
    vt = dict(atts)[va]
    params = ', '.join(f'p{a} : {t}' for a, t in atts)
    lines = [f'CLASS {nm}'] + [f'{IND}PRIVATE {a} : {t}' for a, t in atts] + [f'{IND}PUBLIC PROCEDURE NEW({params})'] + [f'{IND}{IND}{a} ← p{a}' for a, _ in atts] + [f'{IND}ENDPROCEDURE',
             f'{IND}PUBLIC FUNCTION Get{atts[0][0]}() RETURNS {atts[0][1]}', f'{IND}{IND}RETURN {atts[0][0]}', f'{IND}ENDFUNCTION']
    if vt in ('INTEGER', 'REAL'):
        lines += [f'{IND}PUBLIC FUNCTION Set{va}(New{va} : {vt}) RETURNS BOOLEAN', f'{IND}{IND}IF New{va} >= {lo} AND New{va} <= {hi} THEN', f'{IND}{IND}{IND}{va} ← New{va}', f'{IND}{IND}{IND}RETURN TRUE',
                  f'{IND}{IND}ELSE', f'{IND}{IND}{IND}RETURN FALSE', f'{IND}{IND}ENDIF', f'{IND}ENDFUNCTION']
        rule = f' The setter for {va} must only accept values from {lo} to {hi} and return TRUE or FALSE.'
    else:
        lines += [f'{IND}PUBLIC PROCEDURE Set{va}(New{va} : {vt})', f'{IND}{IND}{va} ← New{va}', f'{IND}ENDPROCEDURE']
        rule = ''
    lines.append('ENDCLASS')
    d = ctx(r)
    return Q(f'Write pseudocode for a class {nm} for {d["org"]} with the private attributes ' + ', '.join(f'{a} : {t}' for a, t in atts) + f', a constructor that sets all the attributes from parameters, a getter for {atts[0][0]} and a setter for {va}.{rule}',
             code(lines), '1 mark CLASS/ENDCLASS with PRIVATE attributes; 1 mark constructor NEW with parameters; 1 mark assignments; 1 mark getter; 1 mark setter' + (' with validation and return' if rule else '') + ' [5]', marks=5)


@t13_2.add('C3', (1, 2, 3, 4, 5))
def t13_2_setter(r, D):
    cls, att = r.choice([('Thermostat', 'Target'), ('Speaker', 'Volume'), ('Lift', 'Floor'), ('Heater', 'Power')])
    lo, hi = r.choice([(10, 30), (0, 20), (0, 12), (1, 9)])
    init = r.randrange(lo, hi + 1)
    obj = cls[0] + r.choice(['1', 'A', 'Main'])
    main = [f'{obj} ← NEW {cls}({init})']
    cur, outs = init, []
    for _ in range(3 if D <= 2 else 5):
        v = r.randrange(lo - 5, hi + 6)
        if r.random() < 0.7:
            main.append(f'OUTPUT {obj}.Set{att}({v})')
            ok = lo <= v <= hi
            outs.append('TRUE' if ok else 'FALSE')
            if ok:
                cur = v
        else:
            main.append(f'OUTPUT {obj}.Get{att}()')
            outs.append(str(cur))
    main.append(f'OUTPUT {obj}.Get{att}()')
    outs.append(str(cur))
    cl = [f'CLASS {cls}', f'{IND}PRIVATE {att} : INTEGER', f'{IND}PUBLIC PROCEDURE NEW(Start : INTEGER)', f'{IND}{IND}{att} ← Start', f'{IND}ENDPROCEDURE',
          f'{IND}PUBLIC FUNCTION Set{att}(NewValue : INTEGER) RETURNS BOOLEAN', f'{IND}{IND}IF NewValue < {lo} OR NewValue > {hi} THEN', f'{IND}{IND}{IND}RETURN FALSE', f'{IND}{IND}ENDIF',
          f'{IND}{IND}{att} ← NewValue', f'{IND}{IND}RETURN TRUE', f'{IND}ENDFUNCTION', f'{IND}PUBLIC FUNCTION Get{att}() RETURNS INTEGER', f'{IND}{IND}RETURN {att}', f'{IND}ENDFUNCTION', 'ENDCLASS']
    stem = 'Study the class and main program:\n' + code(cl) + '\n' + code(main) + '\n'
    if D == 1:
        return MCQ(r, stem + 'What is the final value output?', str(cur), [str(x) for x in {init, lo, hi, cur + 1, hi + 1} if x != cur], f'Only values from {lo} to {hi} are accepted; final {att} = {cur}.')
    return Q(stem + 'State the output.', ' '.join(outs), f'setter rejects values outside {lo}–{hi}; outputs ' + ', '.join(outs) + f' [{min(len(outs), 4)}]', marks=min(len(outs), 4))


scen(t13_2, 'C2', (2, 3, 4), [
    '{p} is writing a class to represent a student at {org}.', 'A class Booking at {org} has private attributes and public methods.',
], [('Explain why the attributes are private and accessed by getters and setters.', 'Prevents direct changes; setters validate data; encapsulation hides implementation.', '1 mark each [2]'),
    ('Explain the purpose of the constructor.', 'Called by NEW to initialise the attributes of each new object (from parameters).', '1 mark each [2]'),
    ('Explain what is meant by an instance attribute.', 'Each object has its own value for the attribute, e.g. each student has their own name.', '1 mark each [2]')], k=(2, 3))
scen(t13_2, 'C4', (3, 4, 5), [
    '{org} in {city} is building a booking system using classes.', '{p} is writing an object-oriented game for {org}.',
], [lambda r, d: (lambda q: (q['stem'].replace(f'Write pseudocode for a class', 'Write a class'), q['answer'], q['key']))(t13_2_write(r, 3)),
    lambda r, d: (lambda q: (q['stem'] + ' State the output.' if not q['stem'].endswith('State the output.') else q['stem'], q['answer'], q['key']))(t13_2_setter(r, 2)),
    ('Explain how the setter protects the object\'s data.', 'It checks that the new value is in range before changing the private attribute; invalid values are rejected.', '1 mark each [2]')], k=(2, 3))

t13_3 = topic('Inheritance, polymorphism, overloading and containment (aggregation)', 'inheritance', 'polymorphism', 'overloading', 'containment')
t13_3.fixed('C1', (1, 2), [
    ('What is inheritance?', 'Creating a new (derived) class that takes on the attributes and methods of an existing (base) class', 'CLASS Car INHERITS Vehicle.', ['Hiding data inside a class', 'Using the same name for different methods in one class', 'Storing one object inside another']),
    ('What is polymorphism?', 'A method inherited from a base class is redefined in a derived class, so the same call behaves differently for different classes', 'e.g. Area() in Circle and Rectangle.', ['Creating many objects from one class', 'Making attributes private', 'Copying a class']),
    ('What is overloading?', 'Defining several methods with the same name but different parameters in the same class', 'The version called depends on the arguments.', ['Redefining a method in a subclass', 'Creating too many objects', 'Giving a class two constructors in different files']),
    ('What is containment (aggregation)?', 'A class containing objects of another class as attributes', '"has a" relationship, e.g. a Library has Books.', ['A class inheriting from two classes', 'A method calling itself', 'Hiding data in a class']),
    ('Which relationship is shown by "a Car is a Vehicle"?', 'Inheritance', '"is a" suggests inheritance; "has a" suggests containment.', ['Containment', 'Overloading', 'Encapsulation']),
    ('In Cambridge pseudocode, how does a derived class call the constructor of its base class?', 'SUPER.NEW(...)', 'SUPER refers to the parent class.', ['BASE.CREATE(...)', 'NEW PARENT(...)', 'CALL Constructor()']),
])
t13_3.fixed('C2', (2, 3, 4), [
    ('Explain how inheritance reduces the amount of code a programmer writes.', 'Common attributes and methods are written once in the base class and reused by every derived class, which only adds or overrides what is different.', '1 mark each [2]'),
    ('Explain the difference between polymorphism and overloading.', 'Polymorphism: a derived class redefines (overrides) an inherited method with the same signature; overloading: several methods in one class share a name but have different parameters.', '1 mark each [2]'),
])
ar(t13_3, [('A derived class can use the methods of its base class.', 'Inheritance passes attributes and methods to the derived class.'),
           ('The same method call can produce different results for different objects.', 'Derived classes can override inherited methods (polymorphism).'),
           ('A Library class can contain Book objects.', 'Containment means a class has objects of another class as attributes.')],
    ['A base class inherits from its derived classes.', 'Overloading means a subclass replaces a method of its base class.', 'Containment is an "is a" relationship.'])

PI = 3.142


@t13_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_3_shapes(r, D):
    objs = []
    for i in range(2 if D <= 2 else 3):
        k = r.choice(['Rectangle', 'Circle', 'Triangle'])
        if k == 'Rectangle':
            w, h = r.randrange(2, 15), r.randrange(2, 15)
            objs.append((f'Shape{i + 1} ← NEW Rectangle({w}, {h})', w * h, f'{w} × {h} = {w * h}'))
        elif k == 'Circle':
            rr = r.randrange(1, 10)
            a = round(PI * rr * rr, 3)
            objs.append((f'Shape{i + 1} ← NEW Circle({rr})', a, f'3.142 × {rr}² = {a:g}'))
        else:
            bb, h = r.randrange(2, 15), r.randrange(2, 15)
            objs.append((f'Shape{i + 1} ← NEW Triangle({bb}, {h})', bb * h / 2, f'0.5 × {bb} × {h} = {bb * h / 2:g}'))
    cls = code(['CLASS Shape', f'{IND}PUBLIC FUNCTION Area() RETURNS REAL', f'{IND}{IND}RETURN 0', f'{IND}ENDFUNCTION', 'ENDCLASS',
                'CLASS Rectangle INHERITS Shape  // NEW(W, H); Area() RETURNS W * H', 'CLASS Circle INHERITS Shape  // NEW(R); Area() RETURNS 3.142 * R * R',
                'CLASS Triangle INHERITS Shape  // NEW(B, H); Area() RETURNS 0.5 * B * H'])
    main = [o[0] for o in objs] + [f'OUTPUT Shape{i + 1}.Area()' for i in range(len(objs))]
    outs = [f'{o[1]:g}' for o in objs]
    stem = 'A base class Shape has a method Area() that is overridden in each derived class:\n' + cls + '\nThe main program is:\n' + code(main) + '\n'
    if D == 1:
        return MCQ(r, stem + 'What is the first value output?', outs[0], ['0', f'{objs[0][1] * 2:g}', f'{objs[0][1] + 1:g}', f'{objs[1][1]:g}' if objs[1][1] != objs[0][1] else '1'], f'Polymorphism: the overridden Area() is used: {objs[0][2]}.')
    return Q(stem + 'State the output and explain why Shape.Area() is not used.', ' '.join(outs) + '; each derived class overrides Area() (polymorphism), so the version for the object\'s own class runs.',
             '; '.join(o[2] for o in objs) + f' [{len(objs)}]; polymorphism explained [1] [{len(objs) + 1}]', marks=len(objs) + 1)


@t13_3.add('C3', (2, 3, 4, 5), 'numerical')
def t13_3_staff(r, D):
    rate, hrs = r.randrange(10, 30), r.randrange(20, 45)
    bonus = r.randrange(5, 30) * 10
    rate2, hrs2 = r.randrange(10, 30), r.randrange(20, 45)
    names = r.sample(['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah'], 2)
    lines = ['CLASS Employee', f'{IND}PROTECTED Rate : INTEGER', f'{IND}PROTECTED Hours : INTEGER', f'{IND}PUBLIC PROCEDURE NEW(R : INTEGER, H : INTEGER)', f'{IND}{IND}Rate ← R', f'{IND}{IND}Hours ← H', f'{IND}ENDPROCEDURE',
             f'{IND}PUBLIC FUNCTION Pay() RETURNS INTEGER', f'{IND}{IND}RETURN Rate * Hours', f'{IND}ENDFUNCTION', 'ENDCLASS', 'CLASS Manager INHERITS Employee', f'{IND}PRIVATE Bonus : INTEGER',
             f'{IND}PUBLIC PROCEDURE NEW(R : INTEGER, H : INTEGER, B : INTEGER)', f'{IND}{IND}SUPER.NEW(R, H)', f'{IND}{IND}Bonus ← B', f'{IND}ENDPROCEDURE',
             f'{IND}PUBLIC FUNCTION Pay() RETURNS INTEGER', f'{IND}{IND}RETURN SUPER.Pay() + Bonus', f'{IND}ENDFUNCTION', 'ENDCLASS']
    main = [f'{names[0]} ← NEW Employee({rate}, {hrs})', f'{names[1]} ← NEW Manager({rate2}, {hrs2}, {bonus})', f'OUTPUT {names[0]}.Pay()', f'OUTPUT {names[1]}.Pay()']
    p1, p2 = rate * hrs, rate2 * hrs2 + bonus
    return Q('Study the classes and main program:\n' + code(lines) + '\n' + code(main) + '\nState the output and identify where inheritance and polymorphism are used.',
             f'{p1} {p2}; Manager INHERITS Employee (inheritance); Pay() is overridden in Manager (polymorphism), which calls SUPER.Pay().',
             f'{rate} × {hrs} = {p1} [1]; {rate2} × {hrs2} + {bonus} = {p2} [1]; inheritance [1]; polymorphism [1] [4]', marks=4)


scen(t13_3, 'C4', (3, 4, 5), [
    '{org} in {city} is designing classes for its vehicle fleet: cars, vans and buses.', '{p} is designing a class hierarchy for a zoo management system at {org}.',
], [('Explain how inheritance could be used in this design.', 'A base class (e.g. Vehicle/Animal) holds common attributes and methods; derived classes inherit them and add specific ones.', '1 mark each [2]'),
    ('Explain, with an example, how polymorphism could be used.', 'Each derived class overrides a method such as Describe() or DailyCost(); calling it on any object gives the right behaviour for that class.', '1 mark explanation; 1 mark example [2]'),
    ('Explain what is meant by containment, giving an example from this system.', 'A class has objects of another class as attributes, e.g. a Depot contains an array of Vehicle objects / an Enclosure contains Animals.', '1 mark each [2]'),
    ('Write the header and constructor for a derived class that calls the base-class constructor.', code(['CLASS Van INHERITS Vehicle', f'{IND}PRIVATE MaxLoad : REAL', f'{IND}PUBLIC PROCEDURE NEW(Reg : STRING, Load : REAL)', f'{IND}{IND}SUPER.NEW(Reg)', f'{IND}{IND}MaxLoad ← Load', f'{IND}ENDPROCEDURE', 'ENDCLASS']),
     '1 mark INHERITS; 1 mark SUPER.NEW; 1 mark own attribute set [3]')], k=(3, 4))
scen(t13_3, 'C4', (3, 4, 5), [
    '{org} in {city} is writing a payroll system using classes for employees and managers.', '{p} is designing the staff records program for {org}, in which managers receive a bonus.',
], [lambda r, d: (lambda q: (q['stem'], q['answer'], q['key']))(t13_3_staff(r, 3)),
    ('Explain why Manager is declared as a subclass of Employee rather than as a separate class.', 'A manager is an employee: it inherits Rate, Hours and Pay(), so common code is written once; only Bonus and the new Pay() are added.', '1 mark each [2]'),
    ('Explain why Rate and Hours are declared PROTECTED rather than PRIVATE.', 'Protected attributes can be accessed by subclasses such as Manager but are still hidden from the rest of the program.', '1 mark each [2]'),
    ('A Department class holds an array of Employee objects. Identify this relationship and explain one benefit.', 'Containment/aggregation ("has a"): the department can process all its staff together (e.g. total pay) while each Employee remains a separate object.', '1 mark relationship; 1 mark benefit [2]')], k=(2, 3))
essay(t13_3, [('the use of object-oriented programming, including inheritance and containment, for {org}\'s new software', 'models real-world entities; inheritance reuses code; encapsulation protects data; teams can work on separate classes; easier maintenance and extension.',
               'design takes longer; deep hierarchies can be complex; may be less efficient; not ideal for small or purely computational tasks.', 'OOP is suitable for large, evolving systems with many related entities.')],
      ['{org} in {city} is planning a large new booking system.', '{p} leads the software team at {org}.'])

CHAPTERS[13] = [t13_1, t13_2, t13_3]

# =============================================================================== Chapter 14 File processing and exception handling


def run_py(src, files=None):
    """Execute a small generated Python program with an in-memory file system; return (stdout, files)."""
    files = dict(files or {})

    class F(io.StringIO):
        def __init__(self, name, mode):
            self.name_, self.mode_ = name, mode
            init = files.get(name, '') if mode in ('r', 'a') else ''
            if mode == 'r' and name not in files:
                raise FileNotFoundError(name)
            super().__init__(init)
            if mode == 'a':
                self.seek(0, 2)

        def close(self):
            if self.mode_ in ('w', 'a'):
                files[self.name_] = self.getvalue()
            super().close()

        def __exit__(self, *a):
            self.close()

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(src, {'open': lambda n, m='r': F(n, m), '__builtins__': __builtins__})
    return buf.getvalue(), files


FILES = [('Scores.txt', 'score', [str(x) for x in range(30, 100)]), ('Temps.txt', 'temperature', [str(x) for x in range(12, 41)]),
         ('Sales.txt', 'sales figure', [str(x) for x in range(100, 900, 25)]), ('Ages.txt', 'age', [str(x) for x in range(11, 70)])]


t14_1 = topic('Writing, reading and appending records to serial, sequential and random files', 'writing, reading and appending records', 'serial, sequential and random files')
t14_1.fixed('C1', (1, 2), [
    ('Which file mode is used to add records to the end of an existing text file without deleting its contents?', 'APPEND', 'WRITE creates a new file (overwriting any existing one).', ['WRITE', 'READ', 'RANDOM']),
    ('What does the EOF() function return?', 'TRUE when the end of the file has been reached', 'Used to control a loop that reads every line.', ['The number of lines in the file', 'The last line of the file', 'TRUE when the file is open']),
    ('Which statement moves the file pointer to a given record position in a random file?', 'SEEK', 'Then GETRECORD or PUTRECORD reads or writes the record.', ['READFILE', 'OPENFILE', 'APPEND']),
    ('Which pair of statements reads and writes whole records in a random file in Cambridge pseudocode?', 'GETRECORD and PUTRECORD', 'Text files use READFILE and WRITEFILE.', ['READFILE and WRITEFILE', 'INPUT and OUTPUT', 'OPEN and CLOSE']),
    ('Why must a file be closed after use?', 'To make sure all data is written to the file and the file is released for other programs', 'CLOSEFILE flushes buffers.', ['To delete the file', 'To sort the file', 'To encrypt the file']),
    ('What happens when a file is opened FOR WRITE?', 'A new file is created; any existing file with the same name is overwritten', 'Use APPEND to keep the existing contents.', ['Data is added to the end', 'The file is opened read-only', 'An error always occurs']),
])
t14_1.fixed('C2', (2, 3, 4), [
    ('Explain why a record cannot be inserted into the middle of a sequential file without creating a new file.', 'Records are stored in key order one after another; to insert, all later records would have to move, so the file is copied to a new file with the record written at the correct point.', '1 mark each [2]'),
    ('Explain how a record is found in a random file.', 'The key is hashed to give the record address; SEEK moves to that address and GETRECORD reads it; if it is not the right record (collision), the next positions are checked.', '1 mark per point, max 3 [3]'),
])
ar(t14_1, [('Opening a file FOR WRITE can lose data.', 'Any existing file with the same name is overwritten.'),
           ('A random file gives fast access to individual records.', 'The record position is calculated from the key using a hash.'),
           ('A loop reading a text file usually tests EOF() first.', 'Reading past the end of the file would cause an error.')],
    ['APPEND deletes the existing contents of a file.', 'GETRECORD writes a record to a file.', 'EOF() returns the number of records in the file.'])


@t14_1.add('C3', (1, 2, 3, 4, 5))
def t14_1_trace(r, D):
    fn, what, pool = r.choice(FILES)
    lines_ = r.sample(pool, 5 if D <= 3 else 7)
    th = int(r.choice(pool[len(pool) // 4: 3 * len(pool) // 4]))
    out = fn.replace('.txt', 'Selected.txt')
    cmp_ = r.choice(['>=', '>', '<'])
    sel = [x for x in lines_ if eval(f'{int(x)} {cmp_} {th}')]
    tot = sum(int(x) for x in sel)
    prog = [f'DECLARE Line : STRING', 'DECLARE Count, Total : INTEGER', 'Count ← 0', 'Total ← 0', f'OPENFILE "{fn}" FOR READ', f'OPENFILE "{out}" FOR WRITE', f'WHILE NOT EOF("{fn}")',
            f'{IND}READFILE "{fn}", Line', f'{IND}IF STR_TO_NUM(Line) {cmp_} {th} THEN', f'{IND}{IND}Count ← Count + 1', f'{IND}{IND}Total ← Total + STR_TO_NUM(Line)', f'{IND}{IND}WRITEFILE "{out}", Line', f'{IND}ENDIF',
            'ENDWHILE', f'CLOSEFILE "{fn}"', f'CLOSEFILE "{out}"', 'OUTPUT Count, " ", Total']
    stem = f'The text file {fn} contains one {what} per line: ' + ', '.join(lines_) + '.\n' + code(prog) + '\n'
    if D == 1:
        return MCQ(r, stem + 'What is the value of Count that is output?', str(len(sel)), [str(len(lines_)), str(len(lines_) - len(sel)), str(len(sel) + 1), str(max(len(sel) - 1, 0)) if len(sel) else '2'], f'Lines with value {cmp_} {th}: {", ".join(sel) or "none"}.')
    return Q(stem + f'State the output and the contents of {out} after the program has run.', f'{len(sel)} {tot}; {out} contains ' + (', '.join(sel) or 'nothing (empty file)'),
             f'Count {len(sel)} [1]; Total {tot} [1]; file contents {", ".join(sel) or "empty"} [1] [3]', marks=3)


@t14_1.add('C3', (2, 3, 4, 5))
def t14_1_append(r, D):
    nm = r.choice(['Log.txt', 'Visitors.txt', 'Orders.txt', 'Members.txt'])
    old = r.sample(['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Priya'], 3)
    new = r.sample([x for x in ['Omar', 'Hana', 'Jonas', 'Ines', 'Kwame', 'Ravi', 'Elena', 'Diego'] if x not in old], 2)
    mode = r.choice(['APPEND', 'WRITE'])
    prog = [f'OPENFILE "{nm}" FOR {mode}'] + [f'WRITEFILE "{nm}", "{x}"' for x in new] + [f'CLOSEFILE "{nm}"', f'OPENFILE "{nm}" FOR READ', 'Count ← 0', f'WHILE NOT EOF("{nm}")', f'{IND}READFILE "{nm}", Name', f'{IND}Count ← Count + 1', 'ENDWHILE', f'CLOSEFILE "{nm}"', 'OUTPUT Count, " ", Name']
    final = (old + new) if mode == 'APPEND' else new
    return Q(f'The text file {nm} contains the lines {", ".join(old)}. This program is run:\n' + code(prog) + f'\nState the final contents of {nm} and the output. Explain the effect of the file mode used.',
             f'{nm}: {", ".join(final)}; output {len(final)} {final[-1]}; ' + ('APPEND adds lines to the end, keeping existing data.' if mode == 'APPEND' else 'WRITE creates a new file, so the original lines are lost.'),
             '1 mark contents; 1 mark output; 1 mark explanation [3]', marks=3)


@t14_1.add('C3', (2, 3, 4, 5), 'numerical')
def t14_1_random(r, D):
    size = r.choice([32, 50, 64, 100, 128])
    n = r.choice([100, 200, 500, 1000])
    key = r.randrange(10000, 99999)
    pos = key % n + 1
    off = (pos - 1) * size
    return Q(f'A random file stores {n} records of {size} bytes each, numbered from 1. The record position is calculated as (Key MOD {n}) + 1. (a) Calculate the position for the key {key}. (b) Calculate the byte offset of the start of that record from the start of the file. '
             '(c) Write the pseudocode to read this record into the variable CustRecord from the file "Customers.dat" and close the file.',
             f'(a) {key} MOD {n} + 1 = {pos} (b) ({pos} − 1) × {size} = {off} bytes (c) ' + code(['OPENFILE "Customers.dat" FOR RANDOM', f'SEEK "Customers.dat", {pos}', 'GETRECORD "Customers.dat", CustRecord', 'CLOSEFILE "Customers.dat"']),
             f'(a) {pos} [1] (b) {off} [1] (c) OPENFILE FOR RANDOM [1]; SEEK [1]; GETRECORD and CLOSEFILE [1] [5]', marks=5, typ='multi_step')


scen(t14_1, 'C4', (3, 4, 5), [
    '{org} in {city} stores member records in files.', '{p} is writing a program for {org} that logs every sale to a text file and stores customer details in a random file.',
], [('Write pseudocode to append a new line, held in the variable NewLine, to the text file "Log.txt".', code(['OPENFILE "Log.txt" FOR APPEND', 'WRITEFILE "Log.txt", NewLine', 'CLOSEFILE "Log.txt"']), '1 mark APPEND; 1 mark WRITEFILE; 1 mark CLOSEFILE [3]'),
    ('Write pseudocode to output every line of "Log.txt".', code(['OPENFILE "Log.txt" FOR READ', 'WHILE NOT EOF("Log.txt")', f'{IND}READFILE "Log.txt", Line', f'{IND}OUTPUT Line', 'ENDWHILE', 'CLOSEFILE "Log.txt"']), '1 mark open for read; 1 mark loop with EOF; 1 mark read and output; 1 mark close [4]'),
    ('Explain why the customer details are stored in a random file.', 'Each record can be accessed directly by hashing its key, without reading the records before it.', '1 mark each [2]'),
    lambda r, d: (lambda q: (q['stem'], q['answer'], q['key']))(t14_1_random(r, 3))], k=(2, 3))

t14_2 = topic('Exception handling: try, except and finally; robust programs', 'exception handling', 'try, except and finally', 'robust programs')
t14_2.fixed('C1', (1, 2), [
    ('What is an exception?', 'An unexpected event during program execution that disrupts the normal flow, such as division by zero', 'It can be handled so the program does not crash.', ['A syntax error found by the compiler', 'A comment in the code', 'A type of loop']),
    ('What is the purpose of the except (catch) block?', 'To contain the code that handles the exception', 'The program can recover or report the error.', ['To contain code that might cause an error', 'To run code that must always run', 'To stop the program']),
    ('When does the code in a finally block run?', 'Always, whether or not an exception occurred', 'Often used to close files or release resources.', ['Only when there is an exception', 'Only when there is no exception', 'Never']),
    ('Which of these is likely to raise an exception at run time?', 'Opening a file that does not exist', 'Others: division by zero, converting "abc" to a number, index out of range.', ['A comment line', 'Declaring a variable', 'Using a FOR loop correctly']),
    ('What is a robust program?', 'A program that can cope with unexpected inputs and errors without crashing', 'Achieved by validation and exception handling.', ['A program that runs very fast', 'A program with no comments', 'A program that uses little memory']),
])
t14_2.fixed('C2', (2, 3, 4), [
    ('Explain why exception handling makes a program more robust.', 'Run-time errors are caught and handled (e.g. a message and a retry) instead of the program crashing and losing data.', '1 mark each [2]'),
    ('Explain why a file should be closed in a finally block.', 'The finally block runs whether or not an exception occurs, so the file is always closed and data/resources are not lost.', '1 mark each [2]'),
])
ar(t14_2, [('Code in a finally block always runs.', 'It is executed whether or not an exception was raised.'),
           ('Exception handling stops a program crashing on invalid input.', 'The error is caught and handled by the except block.'),
           ('Converting the string "ten" to an integer raises an exception.', 'The string does not represent a valid number.')],
    ['The except block runs when no exception occurs.', 'Exceptions are only found by the compiler.', 'A finally block runs only if there is an error.'])


def _exc_prog(r, D):
    vals = []
    for _ in range(4 if D <= 3 else 6):
        k = r.random()
        vals.append(r.choice(['"abc"', '"x7"', '"ten"', '""']) if k < 0.25 else ('"0"' if k < 0.4 else f'"{r.randrange(1, 13)}"'))
    if all(v not in ('"0"',) for v in vals):
        vals[r.randrange(len(vals))] = '"0"'
    if all(v[1:-1].isdigit() for v in vals):
        vals[r.randrange(len(vals))] = '"abc"'
    tot = r.choice([60, 100, 120, 240])
    fin = D >= 3
    src = ['data = [' + ', '.join(vals) + ']'] + (['count = 0'] if fin else []) + ['for item in data:', '    try:', '        n = int(item)', f'        print({tot} // n)', '    except ValueError:', '        print("Not a number")',
           '    except ZeroDivisionError:', '        print("Cannot divide by zero")']
    if fin:
        src += ['    finally:', '        count = count + 1']
    src += ['print("Done", count)'] if fin else ['print("Done")']
    out, _ = run_py('\n'.join(src))
    return src, out.strip().split('\n')


@t14_2.add('C3', (1, 2, 3, 4, 5))
def t14_2_trace(r, D):
    src, outs = _exc_prog(r, D)
    stem = 'Study the Python program:\n' + code(src) + '\n'
    if D == 1:
        k = r.randrange(len(outs) - 1)
        return MCQ(r, stem + f'What is output line {k + 1}?', outs[k], list({'Not a number', 'Cannot divide by zero', '0', 'Done', outs[(k + 1) % len(outs)]} - {outs[k]}), f'Outputs: {"; ".join(outs)}.')
    return Q(stem + 'State the output.', ' / '.join(outs), 'int() raises ValueError for non-numeric strings; // by zero raises ZeroDivisionError' + ('; finally runs for every item' if 'finally' in ' '.join(src) else '') + f'. Output: {" / ".join(outs)} [{min(len(outs) - 1, 4)}]',
             marks=min(len(outs) - 1, 4))


@t14_2.add('C3', (2, 3, 4, 5))
def t14_2_write(r, D):
    what, lo, hi = r.choice([('an integer mark', 0, 100), ('a month number', 1, 12), ('a quantity', 1, 50), ('an age', 18, 65), ('a rating', 1, 10), ('a floor number', 0, 20)])
    ans = code(['valid = False', 'while not valid:', '    try:', f'        value = int(input("Enter {what[3:] if what.startswith("an ") else what[2:]}: "))', f'        if {lo} <= value <= {hi}:', '            valid = True', '        else:',
                f'            print("Must be between {lo} and {hi}")', '    except ValueError:', '        print("Please enter a whole number")'])
    return Q(f'Write a Python program fragment that repeatedly asks the user for {what} until a valid whole number from {lo} to {hi} is entered. It must use exception handling so that the program does not crash if letters are entered.',
             ans, '1 mark loop until valid; 1 mark try with int(input()); 1 mark range check; 1 mark except ValueError with message [4]', marks=4)


scen(t14_2, 'C4', (3, 4, 5), [
    '{org} in {city} has a program that crashes when users enter unexpected data.', '{p} is making a file-processing program at {org} more robust.',
], [('Explain what is meant by an exception and give two examples.', 'A run-time error that interrupts normal flow, e.g. file not found, division by zero, invalid type conversion, index out of range.', '1 mark definition; 1 mark examples [2]'),
    lambda r, d: (lambda x: ('The program contains:\n' + code(x[0]) + '\nState the output.', ' / '.join(x[1]), '1 mark per correct output line, max 3 [3]'))(_exc_prog(r, 3)),
    ('Describe how try, except and finally would be used when reading data from a file.', 'try: open and read the file; except FileNotFoundError/IOError: display message/handle; finally: close the file (always runs).', '1 mark each [3]'),
    ('Explain the difference between validation and exception handling.', 'Validation checks data before it is used (e.g. range check); exception handling deals with errors that occur during execution.', '1 mark each [2]')], k=(3, 4))

t14_3 = topic('Implementing file-based programs in Python, Java or VB.NET', 'implementing file-based programs', 'python, java or vb.net')
t14_3.fixed('C1', (1, 2), [
    ('In Python, which statement opens "data.txt" so that new lines are added to the end?', 'f = open("data.txt", "a")', '"r" reads, "w" writes (overwrites), "a" appends.', ['f = open("data.txt", "w")', 'f = open("data.txt", "r")', 'f = open("data.txt")']),
    ('In Python, what does line.strip() do when reading a line from a file?', 'Removes leading and trailing whitespace, including the newline character', 'Otherwise "\\n" stays at the end of each line.', ['Deletes the line from the file', 'Converts the line to a number', 'Splits the line into words']),
    ('Which Java class is commonly used to read a text file line by line?', 'BufferedReader (with FileReader)', 'readLine() returns null at the end of the file.', ['Scanner(System.in) only', 'ArrayList', 'StringBuilder']),
    ('In VB.NET, which object is used to write lines to a text file?', 'StreamWriter', 'StreamReader is used to read.', ['StreamReader', 'Console', 'ListBox']),
    ('In Python, why is the with statement used when opening a file?', 'It closes the file automatically, even if an exception occurs', 'with open("f.txt") as f: ...', ['It makes the file read-only', 'It encrypts the file', 'It sorts the file']),
    ('In Python, what does line.split(",") return?', 'A list of the parts of the line separated by commas', 'Used to separate fields in a CSV record.', ['The number of commas', 'The line with commas removed', 'A single string']),
])
t14_3.fixed('C2', (2, 3, 4), [
    ('Explain why data read from a text file usually needs to be converted before calculations are done.', 'Text files store data as strings; the values must be converted (e.g. int(), float(), Integer.parseInt) to numbers before arithmetic.', '1 mark each [2]'),
    ('Explain why a program that writes to a file should handle exceptions.', 'The file may not be accessible (disk full, no permission, path not found); handling the exception lets the program report the problem instead of crashing and losing data.', '1 mark each [2]'),
])
ar(t14_3, [('Python\'s with statement helps prevent files being left open.', 'The file is closed automatically when the block ends.'),
           ('Values read from a text file must be converted before adding them.', 'Each line is read as a string.'),
           ('Opening a file with mode "w" can destroy existing data.', 'Mode "w" creates a new empty file in place of any existing file.')],
    ['Mode "a" in Python deletes the existing contents of a file.', 'readline() returns integers.', 'Java cannot read text files.'])

CSV = [('Ana', 'Lima'), ('Kenji', 'Seoul'), ('Zara', 'Doha'), ('Omar', 'Cairo'), ('Ines', 'Lisbon'), ('Kwame', 'Accra'), ('Mei', 'Hanoi'), ('Diego', 'Madrid'), ('Priya', 'Mumbai')]


@t14_3.add('C3', (1, 2, 3, 4, 5))
def t14_3_py(r, D):
    rows = r.sample(CSV, 4 if D <= 3 else 6)
    data = [(n, c, r.randrange(20, 100)) for n, c in rows]
    content = ''.join(f'{n},{c},{s}\n' for n, c, s in data)
    th = r.choice([40, 50, 60, 70])
    kind = r.choice(['max', 'count', 'write'])
    if kind == 'max':
        src = ['best = ""', 'top = -1', 'with open("results.csv", "r") as f:', '    for line in f:', '        parts = line.strip().split(",")', '        score = int(parts[2])', '        if score > top:',
               '            top = score', '            best = parts[0]', 'print(best, top)']
    elif kind == 'count':
        src = ['count = 0', 'total = 0', 'with open("results.csv", "r") as f:', '    for line in f:', '        name, city, score = line.strip().split(",")', f'        if int(score) >= {th}:', '            count += 1', '            total += int(score)',
               'print(count, total)']
    else:
        src = ['out = open("below.txt", "w")', 'with open("results.csv", "r") as f:', '    for line in f:', '        fields = line.strip().split(",")', f'        if int(fields[2]) < {th}:', '            out.write(fields[0] + " " + fields[1] + "\\n")', 'out.close()',
               'print(open("below.txt").read().count("\\n"))']
    out, files = run_py('\n'.join(src), {'results.csv': content})
    out = out.strip()
    stem = 'The file results.csv contains the lines: ' + ' | '.join(f'{n},{c},{s}' for n, c, s in data) + '.\nStudy the Python program:\n' + code(src) + '\n'
    if D == 1:
        return MCQ(r, stem + 'What is output?', out, [out + '0', ' '.join(out.split()[::-1]), '0', data[0][0] + ' ' + str(data[0][2])], f'Output: {out}.')
    extra = ' and the contents of below.txt' if kind == 'write' else ''
    ans = out + (f'; below.txt: {files.get("below.txt", "").strip().replace(chr(10), " | ") or "empty"}' if kind == 'write' else '')
    return Q(stem + f'State the output{extra}.', ans, f'{ans} [2]', marks=2)


@t14_3.add('C3', (2, 3, 4, 5))
def t14_3_translate(r, D):
    fn = r.choice(['Stock.txt', 'Names.txt', 'Readings.txt', 'Words.txt'])
    lang = r.choice(['Python', 'Java', 'VB.NET'])
    task = r.choice(['count', 'longest'])
    pc = [f'OPENFILE "{fn}" FOR READ', 'Count ← 0', f'WHILE NOT EOF("{fn}")', f'{IND}READFILE "{fn}", Line'] + ([f'{IND}Count ← Count + 1'] if task == 'count' else [f'{IND}IF LENGTH(Line) > Count THEN', f'{IND}{IND}Count ← LENGTH(Line)', f'{IND}ENDIF']) + ['ENDWHILE', f'CLOSEFILE "{fn}"', 'OUTPUT Count']
    if lang == 'Python':
        a = ['count = 0', f'with open("{fn}", "r") as f:', '    for line in f:'] + (['        count += 1'] if task == 'count' else ['        line = line.rstrip("\\n")', '        if len(line) > count:', '            count = len(line)']) + ['print(count)']
    elif lang == 'Java':
        a = ['int count = 0;', f'try (BufferedReader br = new BufferedReader(new FileReader("{fn}"))) {{', '    String line;', '    while ((line = br.readLine()) != null) {'] + (['        count++;'] if task == 'count' else ['        if (line.length() > count) {', '            count = line.length();', '        }']) + ['    }', '} catch (IOException e) {', '    System.out.println("File error");', '}', 'System.out.println(count);']
    else:
        a = ['Dim count As Integer = 0', 'Dim line As String', f'Dim reader As New IO.StreamReader("{fn}")', 'Do Until reader.EndOfStream', '    line = reader.ReadLine()'] + (['    count = count + 1'] if task == 'count' else ['    If line.Length > count Then', '        count = line.Length', '    End If']) + ['Loop', 'reader.Close()', 'Console.WriteLine(count)']
    return Q(f'Write this pseudocode in {lang}:\n' + code(pc), code(a), '1 mark open file; 1 mark loop until end of file; 1 mark read line and ' + ('count' if task == 'count' else 'compare lengths') + '; 1 mark close/output [4]', marks=4)


scen(t14_3, 'C4', (3, 4, 5), [
    '{org} in {city} keeps its stock data in a CSV text file.', '{p} is writing a program for {org} that reads and updates a file of exam results.',
], [lambda r, d: (lambda q: (q['stem'], q['answer'], q['key']))(t14_3_py(r, 3)),
    ('Write Python code to append the line "Ravi,Mumbai,77" to results.csv.', 'with open("results.csv", "a") as f:\n    f.write("Ravi,Mumbai,77\\n")', '1 mark mode "a"; 1 mark write with newline [2]'),
    ('Explain how exception handling should be added to the program.', 'Wrap file operations in try; except FileNotFoundError/IOError to report errors; except ValueError for bad numbers; finally/with to close the file.', '1 mark per point, max 3 [3]'),
    ('Explain why the data is converted with int() before comparison.', 'Fields read from a text file are strings; comparing strings would compare characters, not numeric values.', '1 mark each [2]')], k=(3, 4))

CHAPTERS[14] = [t14_1, t14_2, t14_3]

# ------------------------------------------------------------------------------- extra C2 (explain / assertion-reason) for chapters 1, 4 and 5
ar(t1_1, [('An enumerated type makes code easier to read.', 'Each possible value is given a meaningful name.'),
          ('A pointer variable can be used to build a linked list.', 'It stores the memory address of another data item.'),
          ('A record is a composite data type.', 'It is made up of fields of other data types.'),
          ('A set type can test whether a value is a member.', 'Sets support operations such as membership, union and intersection.')],
   ['An enumerated type stores the address of a variable.', 'A pointer is a composite data type.', 'A set must contain duplicate values.', 'A record can only contain fields of one data type.'])
ar(t1_2, [('A serial file is suitable for a transaction log.', 'Records are added to the end in the order they occur.'),
          ('Adding a record to a sequential file usually requires a new file.', 'Records must stay in key order, so later records have to move.'),
          ('A random file allows direct access to a record.', 'The address is calculated from the key using a hashing algorithm.')],
   ['Serial files store records in key order.', 'Random files must be read from the beginning to find a record.', 'Sequential files store records at hashed addresses.'])
ar(t1_3, [('Collisions can occur in a hashed file.', 'Two different keys can produce the same hash address.'),
          ('Direct access is faster than sequential access for finding one record.', 'The record can be located without reading the records before it.'),
          ('An overflow area can be used to handle collisions.', 'Records that cannot be stored at their home address are placed elsewhere.')],
   ['A hashing algorithm always produces a different address for every key.', 'Sequential access reads records in random order.', 'Direct access requires every record to be read.'])
ar(t4_1, [('RISC processors are well suited to pipelining.', 'Their instructions are simple and of fixed length, taking one clock cycle each.'),
          ('CISC programs can be shorter than RISC programs.', 'One CISC instruction can carry out several low-level operations.'),
          ('RISC processors use many general-purpose registers.', 'Operations work on registers, reducing slow memory accesses.'),
          ('A branch instruction can reduce the efficiency of a pipeline.', 'Instructions already fetched after the branch may have to be discarded.'),
          ('Interrupts must be handled carefully in a pipelined processor.', 'Several partly executed instructions are in the pipeline at the same time.')],
   ['CISC instructions all take exactly one clock cycle.', 'RISC processors have more instructions than CISC processors.', 'Pipelining executes one instruction at a time from start to finish.', 'RISC instructions are of variable length.'])
ar(t4_2, [('SIMD is efficient for processing graphics.', 'The same instruction is applied to many pixels at the same time.'),
          ('A multi-core processor is an example of MIMD.', 'Each core can run different instructions on different data.'),
          ('Massively parallel computers need specially written software.', 'The problem must be split into parts that can be processed at the same time.'),
          ('Adding processors does not always give a proportional speed-up.', 'Some parts of a task must run sequentially, and processors must communicate.')],
   ['SISD uses many processors on one data stream.', 'Any program runs faster on a massively parallel computer without changes.', 'MIMD processors must all run the same instruction.', 'A GPU is an example of SISD.'])
ar(t4_3, [('A virtual machine can run an operating system that is different from the host.', 'The hypervisor emulates the hardware for the guest operating system.'),
          ('Programs usually run more slowly in a virtual machine.', 'Instructions and hardware access pass through an extra layer of emulation.'),
          ('Virtual machines are useful for testing software safely.', 'The guest system is isolated from the host and can be reset.'),
          ('The JVM allows Java programs to run on different platforms.', 'Java bytecode is executed by a process virtual machine on each platform.')],
   ['A virtual machine needs no host hardware.', 'A guest operating system runs directly on the physical hardware.', 'Virtual machines always run faster than real hardware.', 'A hypervisor is a type of compiler.'])
scen(t4_1, 'C2', (2, 3, 4), [
    '{org} is choosing between a RISC and a CISC processor for a new device.', '{p} is explaining pipelining to colleagues at {org} in {city}.',
], [('Explain why RISC instructions are easier to pipeline than CISC instructions.', 'Fixed-length, simple instructions take the same time in each stage, so stages stay in step.', '1 mark each [2]'),
    ('Explain why a branch instruction can cause a problem in a pipeline.', 'Instructions after the branch may already be in the pipeline and must be flushed if the branch is taken.', '1 mark each [2]'),
    ('Explain why RISC processors need more RAM for programs.', 'More, simpler instructions are needed for the same task, so programs are longer.', '1 mark each [2]'),
    ('Explain the role of registers in a RISC processor.', 'Many general-purpose registers hold operands so that most instructions work on registers, not memory, which is faster.', '1 mark each [2]')], k=(2, 3))
scen(t4_2, 'C2', (2, 3, 4), [
    '{org} in {city} uses a computer with a multi-core processor and a GPU.', '{p} is comparing computer architectures for {org}.',
], [('Explain why the GPU is described as SIMD.', 'Many processing units execute the same instruction on different data (pixels) simultaneously.', '1 mark each [2]'),
    ('Explain why the multi-core processor is described as MIMD.', 'Each core can execute a different instruction stream on different data at the same time.', '1 mark each [2]'),
    ('Explain why not all programs benefit from extra cores.', 'Sequential code cannot be split; overheads of communication/synchronisation.', '1 mark each [2]')], k=(2, 3))
scen(t4_3, 'C2', (2, 3, 4), [
    '{org} runs several virtual servers on one physical server in {city}.', '{p} uses a virtual machine at {org} to run old software.',
], [('Explain the role of the hypervisor.', 'Creates and manages the VMs and shares the physical hardware between them.', '1 mark each [2]'),
    ('Explain why a fault in one virtual machine does not affect the others.', 'Each VM is isolated with its own guest OS and virtual hardware.', '1 mark each [2]'),
    ('Explain why the software may run more slowly in the virtual machine.', 'Instructions and hardware access go through the emulation layer, adding overhead.', '1 mark each [2]')], k=(2, 3))
ar(t5_1, [("De Morgan's laws allow an AND gate to be replaced by OR and NOT gates.", 'NOT(A.B) = A̅ + B̅, so A.B = NOT(A̅ + B̅).'),
          ('A + A.B simplifies to A.', 'A + A.B = A(1 + B) and 1 + B = 1.'),
          ('Simplifying a Boolean expression can reduce the cost of a circuit.', 'A simpler expression needs fewer logic gates.')],
   ['NOT(A + B) = A̅ + B̅.', 'A.A̅ = 1.', 'A + 1 = A.'])
ar(t5_2, [('A Karnaugh map uses Gray code ordering.', 'Adjacent cells must differ in only one variable.'),
          ('A group of four 1s removes two variables.', 'The two variables that change within the group cancel out.'),
          ('Groups may wrap around the edges of a Karnaugh map.', 'Cells on opposite edges differ in only one variable.')],
   ['K-map groups can contain three cells.', 'Each 1 in a K-map can only belong to one group.', 'A Karnaugh map uses ordinary binary ordering for rows.'])
ar(t5_3, [('A full adder has a carry-in input.', 'It must add the carry from the previous, less significant bit.'),
          ('The JK flip-flop has no invalid state.', 'When J = K = 1 the output toggles.'),
          ('Flip-flops are used in registers.', 'Each flip-flop can store one bit.')],
   ['A half adder has three inputs.', 'S = 1, R = 1 is the normal way to store a 1 in an SR flip-flop.', 'A flip-flop can store a whole byte.'])
scen(t5_3, 'C2', (2, 3, 4), [
    '{p} is designing a 4-bit adder for a teaching kit developed in {city}.', 'A memory circuit at {org} is built from flip-flops.',
], [('Explain why a half adder cannot be used for every bit of a multi-bit adder.', 'It has no carry-in input, so it cannot add the carry from the previous bit; full adders are needed.', '1 mark each [2]'),
    ('Explain why the SR flip-flop input S = 1, R = 1 must be avoided.', 'Both outputs are forced to the same value, so Q and Q̅ are not complements; the next state is unpredictable.', '1 mark each [2]'),
    ('Explain the purpose of the clock input of a JK flip-flop.', 'Synchronises changes so the output only changes on a clock pulse, keeping circuits in step.', '1 mark each [2]')], k=(2, 3))

# ------------------------------------------------------------------------------- extra items for chapters 1-3 and 11
@t2_1.add('C2', (2, 3, 4, 5), 'explain')
def t2_1_err(r, D):
    mb, eb = (8, 4) if D <= 3 else (10, 6)
    m, e = fp_rand_norm(r, mb, eb, neg=True if r.random() < 0.6 else None)
    v = fp_val(m, e)
    kind = r.choice(['mant', 'exp'] if m[0] == '1' else ['exp'])
    if kind == 'mant':
        wrong = Fraction(int(m, 2), 1 << (mb - 1)) * Fraction(2) ** from_tc(e)
        why = 'treated the mantissa as unsigned; its first bit has place value −1, so the mantissa is negative'
    else:
        if e[0] == '0':
            e = '1' + e[1:]
            v = fp_val(m, e)
        wrong = Fraction(from_tc(m), 1 << (mb - 1)) * Fraction(2) ** int(e, 2)
        why = f'treated the exponent {e} as unsigned ({int(e, 2)}); in two\'s complement it is {from_tc(e)}'
    if wrong == v:
        return None
    d = ctx(r)
    return Q(f'A floating-point number has {art(mb)} {mb}-bit two\'s complement mantissa {m} and {art(eb)} {eb}-bit two\'s complement exponent {e}. {d["p"]} calculates its denary value as {fdec(wrong)}. Explain the error and give the correct value.',
             f'{d["p"]} {why}. Correct value: {fdec(Fraction(from_tc(m), 1 << (mb - 1)))} × 2^{from_tc(e)} = {fdec(v)}.', '1 mark error identified; 1 mark correct mantissa/exponent; 1 mark correct value [3]', marks=3)


ar(t2_1, [('A floating-point number with a mantissa beginning 1 is negative.', 'The first bit of a two\'s complement mantissa has a negative place value.'),
          ('A negative exponent gives a value smaller in magnitude than the mantissa.', 'The binary point moves to the left.'),
          ('Floating point can represent very large and very small numbers.', 'The exponent scales the mantissa by a power of two.')],
   ['The exponent stores the significant digits of the number.', 'Floating-point values are always exact.', 'The mantissa cannot be negative.'])


@t2_2.add('C2', (2, 3, 4, 5), 'explain')
def t2_2_why(r, D):
    mb, eb = (8, 4) if D <= 3 else (10, 5)
    for _ in range(40):
        neg = r.random() < 0.5
        k = r.randrange(1, 4)
        body = ''.join(r.choice('01') for _ in range(mb - 1 - k))
        m = ('1' * (k + 1) if neg else '0' * (k + 1)) + body
        m = m[:mb]
        if m[1:].strip(m[0]) == '':
            continue
        E = r.randrange(-2, 4)
        e = tc(E, eb)
        nm, ne, sh = normalise(m, e)
        if sh and E - sh >= -(1 << (eb - 1)):
            break
    else:
        return None
    return Q(f'The floating-point number with mantissa {m} and exponent {e} ({mb}-bit and {eb}-bit two\'s complement) is not normalised. Explain how you can tell, and normalise it.',
             f'A normalised mantissa must start 01 (positive) or 10 (negative); this one starts {m[:2]}. Shift the mantissa left {sh} place(s) and subtract {sh} from the exponent: mantissa {nm}, exponent {ne} (value unchanged: {fdec(fp_val(m, e))}).',
             '1 mark reason; 1 mark mantissa; 1 mark exponent [3]', marks=3)


ar(t2_2, [('Normalisation gives the greatest precision for a given mantissa size.', 'Redundant leading bits are removed so more significant bits can be stored.'),
          ('Each number has only one normalised representation.', 'The first two bits of a normalised mantissa must differ.'),
          ('Shifting the mantissa left requires the exponent to be decreased.', 'The value must stay the same, so the scale factor is reduced.')],
   ['A normalised positive mantissa starts with 00.', 'Normalisation changes the value of the number.', 'Shifting the mantissa left increases the exponent.'])

PROTO_TASKS = [('downloading a web page from a server', 'HTTP (or HTTPS)', 'application'), ('uploading website files to a web server', 'FTP', 'application'),
               ('sending an email from a phone to a mail server', 'SMTP', 'application'), ('reading the same mailbox on a laptop and a phone, kept in sync', 'IMAP', 'application'),
               ('downloading emails to one computer and removing them from the server', 'POP3', 'application'), ('making sure that all segments of a file arrive in the right order', 'TCP', 'transport'),
               ('routing packets between networks using IP addresses', 'IP', 'internet (network)'), ('sending frames across a local Ethernet network using MAC addresses', 'Ethernet', 'link'),
               ('streaming live video where speed matters more than every packet arriving', 'UDP', 'transport'), ('logging in to online banking securely', 'HTTPS', 'application')]


@t3_1.add('C3', (1, 2, 3, 4))
def t3_1_task(r, D):
    t, p_, l = r.choice(PROTO_TASKS)
    d = ctx(r)
    if D <= 2:
        return MCQ(r, f'{d["p"]} at {d["org"]} is {t}. Which protocol is used?', p_, [x[1] for x in PROTO_TASKS if x[1] != p_ and x[1].split()[0] != p_.split()[0]][:6], f'{p_} ({l} layer).')
    role = dict(PROTOS).get(p_.split()[0], {'UDP': 'sends datagrams quickly without acknowledgements or retransmission', 'Ethernet': 'transmits frames between devices on a LAN using MAC addresses'}.get(p_, ''))
    return Q(f'{d["p"]} at {d["org"]} in {d["city"]} is {t}. Identify the protocol used and the layer of the TCP/IP stack at which it operates, and describe its role.', f'{p_}; {l} layer; it {role}.', '1 mark protocol; 1 mark layer; 1 mark role [3]', marks=3)


ar(t3_3, [('BitTorrent reduces the load on the original server.', 'Peers download pieces from each other as well as from the seed.'),
          ('A tracker helps a new peer join a swarm.', 'It keeps a record of the peers sharing the file.'),
          ('Leeching can slow down a swarm.', 'Leeches download pieces but upload little in return.')],
   ['A seed has only part of the file.', 'BitTorrent needs a single central server to send the whole file to every user.', 'A torrent file contains the complete shared file.'])
scen(t3_3, 'C2', (2, 3, 4), [
    '{org} in {city} distributes a large software update to thousands of users using BitTorrent.', '{p} downloads an open-source operating system from a BitTorrent swarm.',
], [('Explain why downloads can become faster as more peers join the swarm.', 'More peers hold pieces and upload them, so pieces are downloaded from many sources at once.', '1 mark each [2]'),
    ('Explain the role of the tracker.', 'It records which peers are in the swarm and gives new peers a list to connect to.', '1 mark each [2]'),
    ('Explain why the file is split into pieces.', 'Pieces can be downloaded from different peers simultaneously and checked individually with hashes.', '1 mark each [2]')], k=(2, 3))
scen(t1_3, 'C4', (3, 4, 5), [
    '{org} in {city} stores customer records in a random file of 11 locations (0 to 10), using the hash Key MOD 11 and linear probing.', '{p} is designing a hashed file for {org} with 11 locations (0 to 10); the hash is Key MOD 11 and a collision uses the next free location.',
], [lambda r, d: (lambda ks: (f'Insert the keys {", ".join(map(str, ks))} in this order and give the location of each key.',
                              '; '.join(f'{k} → {pos}' for k, h, pos in hash_insert(ks, 11)[1]), '1 mark per correct location, max 4 [4]'))(r.sample(range(100, 999), 5)),
    ('Explain what is meant by a collision and how linear probing deals with it.', 'Two keys hash to the same address; the record is placed in the next free location (wrapping round).', '1 mark each [2]'),
    ('Describe how a record is searched for in this file.', 'Hash the key; read that location; if it is not the record, check the next locations until found or an empty location is reached.', '1 mark per point, max 3 [3]'),
    ('Explain why the file should not be allowed to become nearly full.', 'More collisions occur, clusters form and searches take longer, approaching a linear search.', '1 mark each [2]')], k=(3, 4))
essay(t1_3, [('whether {org} should use sequential or direct (random) access for its customer file', 'direct access finds individual records quickly for online enquiries; sequential access is efficient for batch processing of every record (e.g. monthly bills).',
              'random files need a hashing algorithm and collision handling, and waste space; sequential files are slow for single-record look-ups.', 'direct access suits interactive use; sequential suits batch runs; an indexed sequential file can give both.')],
      ['{org} in {city} processes customer accounts online and in a monthly batch run.', '{p} is the systems analyst for {org}.'])
scen(t11_1, 'C2', (2, 3, 4), [
    '{p} has written a recursive function for {org} that sometimes crashes.', 'A student at {org} is learning the essential features of recursion.',
], [('Explain the role of the base case.', 'It returns a value without a further recursive call, so the recursion stops and the calls can unwind.', '1 mark each [2]'),
    ('Explain why each recursive call must move towards the base case.', 'Otherwise the base case is never reached, causing infinite recursion and stack overflow.', '1 mark each [2]'),
    ('Explain what a stack frame contains and when it is removed.', 'Return address, parameters and local variables; popped when that call returns.', '1 mark each [2]')], k=(2, 3))

@t3_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t3_2_ttl(r, D):
    ttl = r.choice([4, 5, 6, 8, 10, 16])
    hops = r.randrange(2, ttl + 4)
    arrives = hops < ttl
    left = ttl - hops
    d = ctx(r)
    if D <= 2:
        return MCQ(r, f'A packet leaves {d["city"]} with a time-to-live (TTL) of {ttl}. Each router decreases the TTL by 1 and discards the packet if it reaches 0. The route to the destination passes through {hops} routers. What happens to the packet?',
                   'It arrives with TTL ' + str(left) if arrives else f'It is discarded at router {ttl}', [f'It arrives with TTL {ttl}', f'It is discarded at router {max(1, ttl - 1)}' if arrives else f'It arrives with TTL {abs(left) + 1}', 'It is sent back to the sender with TTL ' + str(ttl), f'It arrives with TTL {hops}'],
                   f'TTL after {hops} routers would be {ttl} − {hops} = {left}; ' + ('it arrives.' if arrives else f'it reaches 0 at router {ttl} and is discarded.'))
    return Q(f'A packet sent from {d["org"]} in {d["city"]} has a TTL (hop limit) of {ttl}; each router decrements it by 1 and discards the packet when it reaches 0. The best route passes through {hops} routers. State whether the packet reaches its destination and explain why routers use a TTL.',
             ('Yes: it arrives with TTL ' + str(left) if arrives else f'No: the TTL reaches 0 at router {ttl}, so the packet is discarded') + '. The TTL stops packets circulating for ever in routing loops.',
             f'{ttl} − {hops} [1]; conclusion [1]; reason for TTL [1] [3]', marks=3)


@t3_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t3_3_time(r, D):
    size = r.choice([700, 1400, 2000, 4500, 8000])
    piece = r.choice([256, 512, 1024, 2048])
    pieces = math.ceil(size * 1024 / piece)
    server = r.choice([2, 4, 5, 10])
    peers = r.randrange(5, 30)
    up = r.choice([0.5, 1, 2])
    cap = r.choice([20, 30, 50, 100])
    rate = min(cap, peers * up + server)
    t1 = size * 8 / server
    t2 = size * 8 / rate
    if D <= 2:
        return Q(f'A {size} MiB file is shared using BitTorrent in pieces of {piece} KiB. Calculate the number of pieces.', f'{pieces} pieces', f'{size} × 1024 ÷ {piece} = {size * 1024 / piece:g} → {pieces} [2]', marks=2)
    return Q(f'A {size} MB file is downloaded by a user whose connection can receive at most {cap} Mbps. Downloading from the company server alone gives {server} Mbps. Using BitTorrent, the user also receives {up:g} Mbps from each of {peers} peers. '
             'Calculate the download time in seconds for each method and explain the difference.', f'server only: {t1:.0f} s; BitTorrent: rate = min({cap}, {peers} × {up:g} + {server}) = {rate:g} Mbps, time {t2:.0f} s; pieces come from many peers at once.',
             f'{size} × 8 ÷ {server} = {t1:.0f} s [1]; combined rate {rate:g} Mbps (limited by connection) [1]; {t2:.0f} s [1]; explanation [1] [4]', marks=4)


@t4_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4_3_alloc(r, D):
    ram = r.choice([32, 64, 128, 256])
    hyp = r.choice([2, 4, 8])
    vm = r.choice([4, 6, 8, 12, 16])
    cores = r.choice([8, 16, 32])
    vc = r.choice([2, 4])
    n = min((ram - hyp) // vm, cores // vc)
    lim = 'memory' if (ram - hyp) // vm <= cores // vc else 'processor cores'
    d = ctx(r)
    if D <= 2:
        k = r.choice(['jvm', 'old', 'test'])
        ex = {'jvm': ('running Java bytecode on any platform', 'Process virtual machine'), 'old': ('running an old operating system on new hardware', 'System virtual machine'),
              'test': ('testing several operating systems on one computer', 'System virtual machine')}[k]
        return MCQ(r, f'{d["org"]} uses a virtual machine for {ex[0]}. Which type of virtual machine is this?', ex[1], ['Process virtual machine' if ex[1].startswith('System') else 'System virtual machine', 'Physical machine', 'Network virtual machine', 'Hardware emulator chip'],
                   'System VMs run a whole guest OS; process VMs (e.g. JVM) run a single program.')
    return Q(f'{d["org"]} in {d["city"]} has a server with {ram} GiB of RAM and {cores} processor cores. The hypervisor needs {hyp} GiB. Each virtual machine needs {vm} GiB of RAM and {vc} cores. Calculate the maximum number of virtual machines that can run at once and state the limiting resource.',
             f'{n} virtual machines; limited by {lim}', f'memory: ({ram} − {hyp}) ÷ {vm} = {(ram - hyp) // vm} [1]; cores: {cores} ÷ {vc} = {cores // vc} [1]; {n}, limited by {lim} [1] [3]', marks=3)

finalize(CHAPTERS)


def tidy_keys(chapters):
    """Single-part items: keep only the trailing [n] as a bracketed mark; inner mark points become (n)."""
    inner = re.compile(r'\[(\d+)\](?!\s*$)')
    for tps in chapters.values():
        for tp in tps:
            for tpl in tp.templates:
                if getattr(tpl, '_tk', False):
                    continue
                tpl._tk = True
                f = tpl.fn

                def g(r, D, f=f):
                    q = f(r, D)
                    if q and not q.get('options') and '(a)' not in q['stem'] and re.search(r'\[\d+\]\s*$', q['key']):
                        q['key'] = inner.sub(r'(\1)', q['key'])
                    return q
                tpl.fn = g


tidy_keys(CHAPTERS)
