"""IB DP Computer Science (new guide, first assessment May 2027) – ib-g12-computer-science.

Year-2 content: A3 Databases, A4 Machine learning (Paper 1, Theme A), B3 Object-oriented programming,
B4 Abstract data types (Paper 2, Theme B), the pre-released case study and the IA computational solution.

Most numerical / tracing items are parametric and their answers are COMPUTED here:
  * SQL items build small tables in an in-memory sqlite3 database and execute the query,
  * code-tracing items generate a Python program and exec() it to capture the real output
    (Java versions are only emitted where the Java and Python semantics are identical),
  * ADT items (stacks, queues, linked lists, BSTs, sets, hash tables) are simulated,
  * ML items (confusion matrices, k-NN, regression, k-means, entropy, perceptrons...) are calculated.
"""
from __future__ import annotations

import contextlib
import re
import io
import itertools
import math
import sqlite3
from collections import Counter, OrderedDict, deque

from _common import F, Registry, T, mcq, name, two_names, fmt, CITIES
from engine import Slot

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

# HL papers: Paper 1 (Theme A + case study) 2 h, 80 marks = Section A 56 + case study 24 (4 challenge
# questions); Paper 2 (Theme B, Java or Python) 2 h, 80 marks. One mock = both papers, 22 questions, 160 marks.
MOCK = [
    dict(section='Paper 1 Section A – Theme A structured questions (databases, machine learning)', count=8,
         c=['C3', 'C4', 'C3', 'C4'], d=[3, 4, 3, 5], type='multi_step', marks=7, style='structured', chapters=[1, 2, 3, 4, 5, 6, 7, 8]),
    dict(section='Paper 1 Section B – Case study challenge questions', count=4,
         c=['C4'], d=[4, 5, 4], type='long', marks=6, style='case_study', chapters=[1, 2, 3, 4, 5, 6, 7, 8, 12]),
    dict(section='Paper 2 – Theme B structured programming questions (OOP and ADTs, Java/Python)', count=10,
         c=['C3', 'C4', 'C3'], d=[3, 4, 5, 3], type='multi_step', marks=8, style='structured', chapters=[9, 10, 11]),
]

STYLE = {'eval_marks': 6, 'essay_marks': 8,
         'markband': 'top band: well-balanced discussion with accurate, specific technical detail applied to the context and a justified conclusion; '
                     'middle band: some balance and correct terminology, conclusion only partly supported; '
                     'bottom band: descriptive, largely one-sided, little technical detail or application.'}

R = Registry()


def init(subject_id):
    pass


# =============================================================================================
# Generic helpers
# =============================================================================================
def run_py(code: str) -> str:
    """Execute generated Python and return what it prints (the real output)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {'__name__': '__qb__'})
    return buf.getvalue().rstrip('\n')


def lines(out: str) -> str:
    return ' / '.join(out.split('\n'))


def table(headers, rows) -> str:
    h = ' | '.join(str(x) for x in headers)
    body = '\n'.join(' | '.join('NULL' if v is None else str(v) for v in r) for r in rows)
    return f'{h}\n{body}'


def sql_run(setup: list, query: str):
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    for s in setup:
        if isinstance(s, tuple):
            cur.executemany(s[0], s[1])
        else:
            cur.execute(s)
    res = cur.execute(query).fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    con.close()
    return cols, res


def sql_seq(setup: list, stmts: list, final: str):
    con = sqlite3.connect(':memory:')
    con.isolation_level = None
    cur = con.cursor()
    for s in setup:
        if isinstance(s, tuple):
            cur.executemany(s[0], s[1])
        else:
            cur.execute(s)
    for s in stmts:
        cur.execute(s)
    res = cur.execute(final).fetchall()
    con.close()
    return res


def fmt_rows(res) -> str:
    if not res:
        return '(no rows returned)'
    def v(x):
        if isinstance(x, float):
            return f'{x:.2f}'.rstrip('0').rstrip('.')
        return 'NULL' if x is None else str(x)
    return '; '.join('(' + ', '.join(v(x) for x in r) + ')' for r in res)


def r2(x, nd=2):
    s = f'{x:.{nd}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.',
           'Both A and R are true, but R is not the correct explanation of A.',
           'A is true but R is false.',
           'A is false but R is true.']


def ar(key, items, d=(2, 4)):
    """Assertion-Reason MCQs: (assertion, reason, index of correct option 0-3, explanation)."""
    def fn(rng, slot):
        a, r_, k, why = rng.choice(items)
        stem = f'Assertion (A): {a}\nReason (R): {r_}\nWhich option is correct?'
        return dict(stem=stem, options=list(AR_OPTS), answer=AR_OPTS[k], markingKey=f'{"ABCD"[k]}. {why}', type='mcq')
    R.t.setdefault(key, []).append(T('C2', d, fn, 'mcq', None, 'ar'))


def scen(key, c, d, contexts, items, type='short'):
    """Context x question combiner: contexts are scenario sentences, items (stem, answer, marks)."""
    def fn(rng, slot):
        cx = rng.choice(contexts)
        st, ans, m = rng.choice(items)
        return dict(stem=f'{cx} {st}', answer=ans, markingKey=ans, type=type, marks=m)
    R.t.setdefault(key, []).append(T(c, d, fn, type, None, 'scen'))


def pick_mcq(key, c, d, items):
    """items: (stem, correct, [wrong x3], why) – shuffled MCQ."""
    R.mcqs(key, c, d, items)


# ---- multi-part structured and case-study templates (used by mocks and the wider bank) ----
CASE_ORGS = [
    'Sabana Health, a network of clinics in Bogotá, is moving patient records into a relational database and trialling a machine-learning triage tool; its booking app is written in an object-oriented language.',
    'MetroFlow, the public-transport authority in Kuala Lumpur, stores ticketing data in a data warehouse, predicts passenger demand with machine learning and runs route-planning software built from classes and graph structures.',
    'Harvest Link, an agricultural cooperative near Nairobi, records crop sales in a database, uses sensors and a model to predict yields, and gives farmers an app that queues orders and caches prices in a hash table.',
    'NordLib, a group of public libraries in Oslo, runs a loans database, recommends books with a clustering model and maintains a catalogue application written in Java.',
    'Pacific Ride, a ride-sharing start-up in Lima, matches drivers to passengers using location data, trains models to set prices and builds its back end from reusable classes.',
    'Lakeside International School in Geneva keeps student, course and grade data in a relational database, uses an ML model to flag students who may need support, and writes its timetabling tool in Python.',
    'Saigon Fresh, a supermarket chain in Hanoi, analyses loyalty-card transactions with association rules, forecasts stock with regression and runs an inventory system based on linked lists and stacks.',
    'Aurora Energy, a utility in Toronto, collects smart-meter readings in a distributed database, detects faults with anomaly detection and models its devices as objects in a simulation.',
    'Kente Market, an online craft marketplace in Accra, stores products as JSON documents, ranks listings with a neural network and processes orders through a queue-based service.',
    'Alpine Rescue in Vienna logs mountain incidents with GPS coordinates in a spatial database, predicts avalanche risk from weather features and coordinates teams with an OOP dispatch system.',
]


GENERIC_PARTS = ('define', 'why', 'contrast', 'misc', 'evaluate')


def _parts_for(base, st, slot, rng, plan, only=None):
    out = []
    used = set()
    for c, d in plan:
        pool = [t for t in base if t.type != 'mcq' and t.name not in ('structured', 'case_study')
                and c in (t.c if isinstance(t.c, tuple) else (t.c,)) and (only is None or t.name in only)]
        fresh = [t for t in pool if id(t.fn) not in used]
        pool = fresh or pool
        rng.shuffle(pool)
        for t in pool[:6]:
            try:
                o = t.fn(rng, Slot(st, slot.chapter, c, d))
            except IndexError:
                o = None
            if o and o.get('type') != 'mcq' and not o.get('options') and all(o['stem'] != p['stem'] for p in out):
                out.append(o)
                used.add(id(t.fn))
                break
    return out


def _split_marks(total, parts):
    raw = [max(1, int(p.get('marks') or 2)) for p in parts]
    s = sum(raw)
    floor = 2 if total >= 2 * len(parts) else 1
    ms = [max(floor, round(total * r / s)) for r in raw]
    while sum(ms) > total:
        i = ms.index(max(ms))
        if ms[i] <= floor:
            break
        ms[i] -= 1
    while sum(ms) < total:
        i = ms.index(max(ms))
        ms[i] += 1
    return ms


def _org_short(org):
    cuts = [org.find(x) for x in (',', ' keeps', ' logs') if org.find(x) > 0]
    return org[:min(cuts)] if cuts else 'the organisation'


def _clean_key(k):
    k = re.sub(r'\((\d+) marks: ', '(', k)
    k = re.sub(r'Markbands \(\d+ marks\)', 'Markbands', k)
    return k


def _compose(parts, total, intro=''):
    for p in parts:
        p['markingKey'] = _clean_key(p['markingKey'])
    ms = _split_marks(total, parts)
    letters = 'abcd'
    stem = (intro + '\n' if intro else '') + '\n'.join(f'({letters[i]}) {p["stem"]} [{ms[i]}]' for i, p in enumerate(parts))
    ans = ' '.join(f'({letters[i]}) {p["answer"]}' for i, p in enumerate(parts))
    key = ' '.join(f'({letters[i]}) [{ms[i]} marks] {p["markingKey"]}' for i, p in enumerate(parts))
    return stem, ans, key


def structured_t(base, st):
    def fn(rng, slot):
        if slot.c == 'C4':
            plan = [('C2', 2), ('C3', 3), ('C4', max(3, slot.d))]
        elif slot.d >= 4:
            plan = [('C1', 2), ('C3', 3), ('C3', 4)]
        else:
            plan = [('C1', 2), ('C2', 2), ('C3', 3)]
        parts = _parts_for(base, st, slot, rng, plan)
        if len(parts) < 2:
            return None
        total = slot.marks or sum(int(p.get('marks') or 2) for p in parts)
        stem, ans, key = _compose(parts, total)
        return dict(stem=stem, answer=ans, markingKey=key, type='multi_step', marks=total)
    return T(('C3', 'C4'), (3, 5), fn, 'multi_step', 'structured', 'structured')


def case_study_t(base, st):
    def fn(rng, slot):
        if st['id'][-8:] in ('ch12-st3', 'ch12-st4', 'ch12-st5'):
            client, need = rng.choice(_IA_CLIENTS)
            org = f'A student is developing an IA computational solution for {client}, which needs to {need}.'
            short = 'this IA project'
        else:
            org = rng.choice(CASE_ORGS)
            short = _org_short(org)
        plan = [('C2', 3), ('C4', max(3, slot.d))]
        parts = _parts_for(base, st, slot, rng, plan, GENERIC_PARTS)
        if len(parts) < 2:
            return None
        for p in parts:
            p['stem'] = p['stem'].rstrip() + f' Refer to {short} in your answer.'
        total = slot.marks or 6
        stem, ans, key = _compose(parts, total, ('Internal assessment context: ' if short == 'this IA project' else 'Case study context: ') + org)
        return dict(stem=stem, answer=ans, markingKey=key + ' Credit is given only for points applied to the stated organisation (not generic answers).', type='long', marks=total)
    return T('C4', (3, 5), fn, 'long', 'case_study', 'case_study')


_TPL_CACHE: dict = {}


def templates(st):
    # Cached so that template use-counts persist between items and the engine rotates fairly.
    if st['id'] not in _TPL_CACHE:
        base = [t for t in R.build(st, STYLE) if t.name != 'fact_short']
        _TPL_CACHE[st['id']] = base + [structured_t(base, st), case_study_t(base, st)]
    return _TPL_CACHE[st['id']]


PEOPLE = ['Amara', 'Lukas', 'Sofia', 'Kenji', 'Priya', 'Mateo', 'Chloe', 'Omar', 'Ingrid', 'Tomas', 'Aiko',
          'Nia', 'Yusuf', 'Elena', 'Kwame', 'Mei', 'Lars', 'Zara', 'Diego', 'Hana', 'Felix', 'Leila', 'Arjun',
          'Freya', 'Isabel', 'Jonas', 'Ana', 'Rafael', 'Sana', 'Noah', 'Alessia', 'Tariq', 'Maya']


# =============================================================================================
# ch01 A3.1 Database fundamentals
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('table (relation)', 'a two-dimensional structure of rows and columns that stores data about one entity type'),
           ('record (tuple)', 'one row of a table, holding all the data about a single instance of the entity'),
           ('field (attribute)', 'one column of a table, holding one item of data of a single data type for every record'),
           ('data type', 'the kind of value a field may hold, such as INTEGER, VARCHAR, DATE or BOOLEAN, which fixes the storage used and the operations allowed'),
           ('relational database', 'a collection of related tables, linked through keys, that is managed by a DBMS and queried with SQL'),
           ('flat-file database', 'a single table, often a text or spreadsheet file, with no links to other tables'),
           ('database', 'an organised, persistent collection of related data that can be searched, sorted and updated efficiently')],
    facts=[('Which of the following is the best data type for a telephone number such as +41 22 555 0199?', 'VARCHAR (text)', ['INTEGER', 'REAL', 'DATE'], 'Telephone numbers contain +, spaces and leading zeros and are never used in arithmetic, so they are stored as text.'),
           ('In a relational table, which of the following is TRUE?', 'Every value in one column has the same data type', ['Rows must be stored in alphabetical order', 'A table can hold only one field', 'Each record must have a different number of fields'], 'A column (field) holds values of one data type for all records.'),
           ('A table Students has 7 columns and 240 rows. How many records does it hold?', '240', ['7', '247', '1680'], 'Each row is one record; columns are fields.'),
           ('Which data type would most suitably store whether a library book is currently on loan?', 'BOOLEAN', ['VARCHAR(50)', 'DATE', 'REAL'], 'There are only two states, true or false.')],
    why=[('Explain why a relational database is preferred to a single flat file for a school storing students, courses and enrolments.', 'Data about each entity is stored once in its own table and linked by keys, so redundancy is reduced, updates happen in one place (no update anomalies), data stays consistent, and flexible queries can join the tables.'),
         ('Explain why choosing the correct data type for each field matters.', 'The data type restricts the values that can be entered (a form of validation), determines how much storage each value takes, and decides which operations are possible (e.g. arithmetic on INTEGER, date comparison on DATE, sorting order).'),
         ('Explain why a date of birth should be stored as DATE rather than as text.', 'A DATE field validates that the value is a real date, sorts chronologically rather than alphabetically, and allows date arithmetic such as calculating age; text such as "03/04/2008" is ambiguous and sorts incorrectly.'),
         ('Explain why each table in a relational database should describe a single entity.', 'Keeping one entity per table means each fact is stored once, avoids repeating groups, and makes it possible to link tables with keys without duplicating or contradicting data.')],
    contrast=[('a record', 'a field', 'A record is a complete row describing one instance of an entity; a field is a single column/attribute that holds one type of data for every record.'),
              ('a flat-file database', 'a relational database', 'A flat file stores all data in one table, causing redundancy and inconsistency; a relational database splits data into linked tables using primary and foreign keys, reducing redundancy.'),
              ('data', 'information', 'Data are raw values stored in fields; information is data that has been processed or given context (e.g. by a query) so that it is meaningful.'),
              ('CHAR(n)', 'VARCHAR(n)', 'CHAR(n) always reserves n characters (padding shorter values); VARCHAR(n) stores only the characters entered, up to n, so it saves space for values of varying length.')],
    misc=[('A relational table can have two rows that are completely identical because the DBMS stores them in order.', 'Each record must be uniquely identifiable by its primary key; duplicate rows break entity integrity and row order is not significant in the relational model.'),
          ('Postcodes should be stored as INTEGER because they are numbers.', 'Many postcodes contain letters or leading zeros (e.g. 01067, SW1A 1AA) and are never used in arithmetic, so they should be stored as text.'),
          ('Storing a customer\'s age is better than storing their date of birth.', 'Age changes every year so the stored value soon becomes wrong; storing date of birth lets age be calculated whenever it is needed.')],
    evaluate=[('A spreadsheet is an adequate replacement for a relational database in a small business.', ['easy to set up and familiar to staff', 'adequate for a small amount of data used by one person'], ['no enforced relationships or referential integrity', 'redundant data leads to inconsistencies', 'weak multi-user access control and concurrency', 'does not scale and lacks a query language such as SQL'], 'Adequate only for very small, single-user data; once data are related and shared, a relational DBMS is needed for integrity, security and concurrency.')],
    extended=[('A charity in Mumbai keeps volunteer details in a spreadsheet with columns VolunteerName, Phone, Event1, Event1Date, Event2, Event2Date. Describe three problems with this design and explain how a relational design would solve them.', 'Problems: repeating groups (Event1, Event2…) limit the number of events and waste space; event details are duplicated for every volunteer (redundancy) so changing an event date needs many edits (update anomaly) and can cause inconsistency; no unique identifier, so two volunteers with the same name cannot be told apart. Relational design: Volunteer(VolunteerID PK, Name, Phone), Event(EventID PK, Name, Date), Attendance(VolunteerID FK, EventID FK) with composite PK – each fact stored once and any number of events per volunteer.', 6)],
))

_DT_POOL = [
    ('ProductPrice', ['12.99', '7.50', '149.00'], 'DECIMAL(8,2) / REAL', 'it has a fractional part and is used in arithmetic'),
    ('Quantity', ['3', '12', '0'], 'INTEGER', 'it is a whole number used in arithmetic'),
    ('PhoneNumber', ['+254 20 555 0182', '0207 946 0011', '+65 6555 0199'], 'VARCHAR(20)', 'it contains +, spaces and leading zeros and is never calculated with'),
    ('DateOfBirth', ['2008-03-14', '2007-11-02', '2009-01-30'], 'DATE', 'it is a date that must be validated, sorted chronologically and used to compute age'),
    ('IsMember', ['TRUE', 'FALSE', 'TRUE'], 'BOOLEAN', 'it only ever has two possible values'),
    ('Email', ['li.wei@mail.sg', 'k.mensah@uni.gh', 'a.ruiz@correo.pe'], 'VARCHAR(100)', 'it is text of varying length'),
    ('CountryCode', ['KE', 'SG', 'PE'], 'CHAR(2)', 'it is always exactly two characters'),
    ('PostCode', ['01067', 'SW1A 1AA', '10115'], 'VARCHAR(10)', 'it may contain letters and leading zeros and is never used in arithmetic'),
    ('HeightCm', ['171.5', '158.0', '183.2'], 'REAL / DECIMAL(5,1)', 'it is a measurement with a decimal part'),
    ('LastLogin', ['2026-05-02 08:15:00', '2026-05-03 19:42:10', '2026-05-04 06:01:55'], 'DATETIME / TIMESTAMP', 'it records both a date and a time'),
    ('Grade', ['A', 'C', 'B'], 'CHAR(1)', 'it is a single character'),
    ('Rating', ['4', '5', '2'], 'INTEGER (with a CHECK 1-5)', 'it is a small whole number in a fixed range'),
]


@R.add('ch01-st1', 'C3', (1, 4), 'short')
def dt_choose(rng, slot):
    k = 2 if slot.d <= 2 else 3 if slot.d == 3 else 4
    fs = rng.sample(_DT_POOL, k)
    ent = rng.choice(['Customer', 'Order', 'Student', 'Patient', 'Member', 'Product', 'Booking', 'Athlete'])
    lst = '\n'.join(f'{f[0]}: e.g. {", ".join(f[1])}' for f in fs)
    ans = '; '.join(f'{f[0]} – {f[2]} because {f[3]}' for f in fs)
    return dict(stem=f'A {ent} table is being designed. For each field below, state the most appropriate data type and justify your choice.\n{lst}',
                answer=ans, markingKey=f'1 mark for each correct data type with a valid justification: {ans}.', marks=k, type='short')


@R.add('ch01-st1', 'C3', (2, 5), 'numerical')
def rec_size(rng, slot):
    ent = rng.choice(['Book', 'Patient', 'Vehicle', 'Flight', 'Employee', 'Sensor reading'])
    fields = [('ID', 'INTEGER', 4), ('Name', f'CHAR({rng.choice([20, 30, 40])})', None), ('Code', f'CHAR({rng.choice([2, 3, 6, 8])})', None),
              ('Date', 'DATE', 3), ('Flag', 'BOOLEAN', 1), ('Amount', 'DECIMAL', 8)]
    k = 4 if slot.d <= 3 else 6
    fs = fields[:k]
    sizes = []
    for f_, t_, s in fs:
        sizes.append(s if s else int(t_[5:-1]))
    rec = sum(sizes)
    n = rng.choice([500, 1200, 2500, 8000, 15000, 40000])
    total = rec * n
    over = rng.choice([0, 10, 20, 25]) if slot.d >= 4 else 0
    total2 = total * (100 + over) / 100
    lst = ', '.join(f'{f_} {t_}' for f_, t_, s in fs)
    note = ' (CHAR(n) uses n bytes, INTEGER 4 bytes, DATE 3 bytes, BOOLEAN 1 byte, DECIMAL 8 bytes)'
    extra = f' Allow an extra {over}% for indexes and overheads.' if over else ''
    ans = f'{rec} bytes per record; {r2(total2)} bytes ≈ {r2(total2 / 1024, 1)} KiB'
    return dict(stem=f'A {ent} table has the fields {lst}{note}. Estimate the storage needed for {n} records.{extra}',
                answer=ans, markingKey=f'Record size = {" + ".join(map(str, sizes))} = {rec} bytes (M1 A1); × {n} = {total} bytes (M1)' + (f'; × 1.{over:02d} = {r2(total2)} bytes' if over else '') + f'; ≈ {r2(total2 / 1024, 1)} KiB (A1).',
                marks=3 if slot.d <= 3 else 4)


@R.add('ch01-st1', 'C1', (1, 3), 'mcq')
def count_rf(rng, slot):
    cols = rng.sample(['MemberID', 'Surname', 'City', 'JoinDate', 'Tier', 'Points', 'Email'], rng.randint(3, 5))
    n = rng.randint(3, 6)
    rows = [[f'{c[:1]}{rng.randint(10, 99)}' for c in cols] for _ in range(n)]
    ask = rng.choice(['records', 'fields'])
    corr = n if ask == 'records' else len(cols)
    wrong = {n * len(cols), n + len(cols), (len(cols) if ask == 'records' else n), corr + 1, corr - 1}
    wrong.discard(corr)
    return mcq(rng, f'The table extract below is from a club database.\n{table(cols, rows)}\nHow many {ask} are shown?', str(corr),
               [str(w) for w in sorted(wrong)][:3], f'Rows are records ({n}); columns are fields ({len(cols)}).')


ar('ch01-st1', [
    ('A field storing a product price should use a DECIMAL data type.', 'DECIMAL values are stored exactly to a fixed number of decimal places, avoiding floating-point rounding errors in money calculations.', 0, 'Both true; exact fixed-point storage is the reason DECIMAL suits currency.'),
    ('In the relational model the order of rows in a table is significant.', 'Rows are retrieved with queries that can sort them in any order using ORDER BY.', 3, 'Row order has no meaning in a relation (A false); R is true.'),
    ('Every field in a table must have a data type.', 'The data type determines the storage, valid values and operations for a field.', 0, 'Both true and R explains why a type is required.'),
    ('A telephone number should be stored as INTEGER.', 'Leading zeros are lost when a value is stored as an integer.', 3, 'A is false: store as text; R is true and is precisely why.'),
])


R.facts('ch01-st2', F(
    terms=[('primary key', 'a field (or combination of fields) chosen to uniquely identify each record in a table; it cannot be NULL'),
           ('foreign key', 'a field in one table that refers to the primary key of another table, creating a relationship between them'),
           ('composite key', 'a primary key made up of two or more fields that together uniquely identify a record'),
           ('candidate key', 'any minimal field or set of fields that could uniquely identify every record and so could be chosen as the primary key'),
           ('secondary key', 'a non-unique field that is indexed so that records can be searched or sorted quickly by it'),
           ('surrogate key', 'an artificial identifier, such as an auto-incrementing integer, created only to be the primary key'),
           ('alternate key', 'a candidate key that was not chosen as the primary key')],
    facts=[('Which of the following fields is the most suitable primary key for a table of students?', 'StudentID', ['Surname', 'DateOfBirth', 'HomeCity'], 'Only StudentID is guaranteed unique and unchanging; the others can repeat.'),
           ('A table Enrolment(StudentID, CourseID, Grade) records which students take which courses. What is the most suitable primary key?', 'The composite key (StudentID, CourseID)', ['StudentID alone', 'CourseID alone', 'Grade'], 'A student takes many courses and a course has many students, so only the pair is unique.'),
           ('What type of relationship is created when a foreign key in Orders refers to the primary key of Customers?', 'One-to-many (one customer, many orders)', ['One-to-one', 'Many-to-many', 'No relationship'], 'Many order records can hold the same CustomerID.'),
           ('A many-to-many relationship between Authors and Books is implemented in a relational database by…', 'a link (junction) table containing the primary keys of both tables as foreign keys', ['adding a foreign key to both tables', 'merging the two tables', 'storing a list of book IDs in one field'], 'Relational tables cannot store lists in a field, so a junction table resolves M:N into two 1:M.')],
    why=[('Explain why a primary key value cannot be NULL.', 'The primary key must identify every record uniquely; a NULL is an unknown value, so a record with a NULL key could not be identified or referenced (entity integrity).'),
         ('Explain why a surrogate key is often used instead of a natural key such as an email address.', 'Natural keys can change (a person changes email) or contain errors, and are long text; a surrogate integer never changes, is short, fast to index and join, and is guaranteed unique.'),
         ('Explain how a foreign key enforces referential integrity.', 'The DBMS only allows a foreign key value that exists as a primary key value in the referenced table (or NULL), and blocks or cascades deletions of referenced records, so there are no orphan records.'),
         ('Explain why a many-to-many relationship cannot be implemented directly between two tables.', 'A field may hold only one atomic value, so neither table can store a list of keys from the other; a junction table with one row per pairing splits it into two one-to-many relationships.')],
    contrast=[('a primary key', 'a foreign key', 'A primary key uniquely identifies records in its own table; a foreign key is a field that refers to the primary key of another table to link the tables, and may repeat.'),
              ('a candidate key', 'a primary key', 'A candidate key is any minimal set of fields that could uniquely identify records; the primary key is the one candidate key chosen for that role.'),
              ('a composite key', 'a surrogate key', 'A composite key combines two or more existing fields to achieve uniqueness; a surrogate key is a single artificial field (e.g. auto-number) added just to be the key.'),
              ('a one-to-many relationship', 'a many-to-many relationship', 'In 1:M one record in table A links to many in B but each B links to one A (FK in B); in M:N records on both sides link to many on the other, requiring a junction table.')],
    misc=[('A foreign key must be unique in the table where it appears.', 'A foreign key usually repeats (many orders for one customer); it is the referenced primary key that must be unique.'),
          ('A composite key means the table has two primary keys.', 'A table has exactly one primary key; a composite key is one key made of several fields that only together are unique.'),
          ('Surname is a good primary key for an employee table because it is always filled in.', 'Being NOT NULL is not enough – surnames are not unique and can change, so they cannot identify records reliably.')],
    evaluate=[('Natural keys should always be preferred to surrogate keys.', ['natural keys carry meaning and avoid an extra column', 'they prevent duplicate entry of the same real-world item'], ['natural values can change, forcing cascading updates', 'they may be long text, slowing joins and indexes', 'uniqueness is not always guaranteed (e.g. names, emails reused)'], 'Not always: surrogate keys are usually safer as primary keys, while natural candidate keys can still be protected with UNIQUE constraints.')],
    extended=[('A hospital in Lisbon stores Doctor(DoctorID, Name, Specialism), Patient(PatientID, Name, DOB) and Appointment(…). Each appointment is for one patient with one doctor at a date and time. Design the Appointment table, identifying its primary key and foreign keys, and justify your choices.', 'Appointment(AppointmentID PK, PatientID FK → Patient, DoctorID FK → Doctor, AppDate, AppTime, Room). AppointmentID is a surrogate key because a patient may see the same doctor many times (so PatientID+DoctorID is not unique); alternatively a composite key (DoctorID, AppDate, AppTime) is a candidate key since a doctor cannot have two appointments at once. PatientID and DoctorID are foreign keys giving two 1:M relationships and enforcing referential integrity.', 6)],
))


def _cand_keys(cols, rows):
    out = []
    for k in range(1, len(cols) + 1):
        for combo in itertools.combinations(range(len(cols)), k):
            if any(set(c) <= set(combo) for c in out):
                continue
            vals = [tuple(r[i] for i in combo) for r in rows]
            if len(set(vals)) == len(vals):
                out.append(combo)
    return out


@R.add('ch01-st2', 'C3', (2, 5), 'short')
def which_unique(rng, slot):
    ctx = rng.choice([
        ('Loans at a library in Vienna', ['MemberID', 'BookID', 'LoanDate', 'Branch'],
         lambda: [rng.choice(['M01', 'M02', 'M03']), rng.choice(['B10', 'B11', 'B12']), rng.choice(['2026-03-01', '2026-03-02']), rng.choice(['Ost', 'West'])]),
        ('Race results in a Nairobi athletics league', ['RunnerID', 'RaceID', 'Position', 'Club'],
         lambda: [rng.choice(['R1', 'R2', 'R3']), rng.choice(['K5', 'H10', 'M42']), rng.randint(1, 4), rng.choice(['Simba', 'Tembo'])]),
        ('Class timetable at a school in Seoul', ['TeacherID', 'Period', 'Room', 'Subject'],
         lambda: [rng.choice(['T1', 'T2', 'T3']), rng.randint(1, 3), rng.choice(['A1', 'A2', 'B1']), rng.choice(['CS', 'Maths', 'Physics'])]),
    ])
    title, cols, mk = ctx
    n = 5 if slot.d <= 3 else 6
    for _ in range(60):
        rows = [mk() for _ in range(n)]
        if len(set(map(tuple, rows))) < n:
            continue
        cks = _cand_keys(cols, rows)
        if cks and all(len(c) <= 3 for c in cks) and len(cks[0]) >= 2:
            break
    else:
        return None
    singles = [cols[i] for i in range(len(cols)) if len(set(r[i] for r in rows)) == n]
    dup_col = next((i for i in range(len(cols)) if len(set(r[i] for r in rows)) < n), None)
    dv = Counter(r[dup_col] for r in rows).most_common(1)[0][0]
    ck_txt = ' or '.join('(' + ', '.join(cols[i] for i in c) + ')' for c in cks)
    if slot.d <= 3:
        stem = f'The table below records {title[0].lower() + title[1:]}.\n{table(cols, rows)}\nUsing only the data shown, explain why {cols[dup_col]} on its own cannot be the primary key, and identify the smallest combination of fields that is unique in this extract.'
    else:
        stem = f'The extract below shows {title.lower()}.\n{table(cols, rows)}\nIdentify every minimal combination of fields that uniquely identifies the records shown, and discuss whether the data alone proves that a combination is a suitable composite primary key.'
    ans = f'{cols[dup_col]} repeats (value {dv} appears more than once), so it is not unique. Minimal unique combinations in this extract: {ck_txt}.' + (' Single unique fields: ' + ', '.join(singles) + '.' if singles else '')
    key = ans + ' A sample can only DISprove uniqueness; whether a combination is a valid key depends on the business rules (e.g. could the same pair recur in future?).'
    return dict(stem=stem, answer=ans, markingKey=key, marks=3 if slot.d <= 3 else 4)


@R.add('ch01-st2', 'C3', (2, 4), 'short')
def fk_violation(rng, slot):
    par = rng.choice([('Customer', 'CustomerID', 'C'), ('Department', 'DeptID', 'D'), ('Course', 'CourseCode', 'CS'), ('Airport', 'IATA', '')])
    pname, pk, pre = par
    if pname == 'Airport':
        ids = rng.sample(['NBO', 'SIN', 'LIM', 'OSL', 'YYZ', 'LIS', 'DXB', 'MEL', 'ACC', 'HAN'], 4)
        allc = ['NBO', 'SIN', 'LIM', 'OSL', 'YYZ', 'LIS', 'DXB', 'MEL', 'ACC', 'HAN', 'BOG', 'VIE']
    else:
        nums = rng.sample(range(1, 9), 4)
        ids = [f'{pre}{x}' for x in nums]
        allc = [f'{pre}{x}' for x in range(1, 10)]
    child = rng.choice(['Orders', 'Staff', 'Enrolment', 'Flight'])
    rows = []
    for i in range(6):
        v = rng.choice(ids) if rng.random() < 0.7 else rng.choice([x for x in allc if x not in ids])
        rows.append([100 + i, v])
    bad = [r[0] for r in rows if r[1] not in ids]
    if not bad:
        rows[rng.randrange(6)][1] = rng.choice([x for x in allc if x not in ids])
        bad = [r[0] for r in rows if r[1] not in ids]
    ans = f'Rows with {child}ID ' + ', '.join(map(str, bad)) + f' violate referential integrity: their {pk} value does not exist in {pname}.'
    return dict(stem=f'Table {pname} contains these {pk} values: {", ".join(ids)}.\nTable {child} has a foreign key {pk} referencing {pname}:\n{table([child + "ID", pk], rows)}\nIdentify the records in {child} that break referential integrity and state what a DBMS would do if one of them were inserted.',
                answer=ans, markingKey=ans + ' The DBMS would reject the INSERT (foreign-key constraint violation). 1 mark per correct row, 1 for the DBMS response.', marks=len(bad) + 1)


@R.add('ch01-st2', 'C3', (2, 4), 'short')
def rel_type(rng, slot):
    A, B = rng.choice([('Teacher', 'Class'), ('Author', 'Book'), ('Player', 'Team'), ('Country', 'Capital'), ('Doctor', 'Patient'), ('Driver', 'Licence')])
    kind = rng.choice(['1:1', '1:M', 'M:N'])
    a_ids = [f'{A[0]}{i}' for i in range(1, 4)]
    b_ids = [f'{B[0].lower()}{i}' for i in range(1, 5)]
    if kind == '1:1':
        pairs = list(zip(a_ids, b_ids))
    elif kind == '1:M':
        pairs = [(rng.choice(a_ids), b) for b in b_ids]
        if len(set(a for a, _ in pairs)) == len(pairs):
            pairs[1] = (pairs[0][0], pairs[1][1])
    else:
        pairs = [('{}'.format(a_ids[0]), b_ids[0]), (a_ids[0], b_ids[1]), (a_ids[1], b_ids[0]), (a_ids[2], b_ids[2]), (a_ids[1], b_ids[3])]
    rng.shuffle(pairs)
    a_many = max(Counter(a for a, _ in pairs).values()) > 1
    b_many = max(Counter(b for _, b in pairs).values()) > 1
    comp = 'M:N' if a_many and b_many else '1:M' if a_many else 'M:1' if b_many else '1:1'
    impl = {'M:N': f'a junction table {A}{B}({A}ID, {B}ID) with a composite primary key, each part a foreign key',
            '1:M': f'{A}ID stored as a foreign key in the {B} table',
            'M:1': f'{B}ID stored as a foreign key in the {A} table',
            '1:1': f'a foreign key with a UNIQUE constraint in either table (or merge the tables)'}[comp]
    pl = ', '.join(f'{a}–{b}' for a, b in pairs)
    ans = f'{comp} ({A} to {B}); implement with {impl}.'
    return dict(stem=f'The sample links between {A} and {B} records are: {pl}. Assuming the sample is typical, identify the type of relationship between {A} and {B} and describe how it should be implemented in a relational database.',
                answer=ans, markingKey=f'{ans} 1 mark for the relationship type with reasoning from the data (an {A} appears {"more than once" if a_many else "once"}, a {B} appears {"more than once" if b_many else "once"}); 1-2 marks for the implementation.', marks=3)


ar('ch01-st2', [
    ('A foreign key value may appear many times in a table.', 'A foreign key represents the "many" side of a one-to-many relationship.', 0, 'Both true; repetition follows from the 1:M relationship.'),
    ('A composite primary key may contain NULL in one of its fields.', 'Every part of a primary key must have a value for entity integrity.', 3, 'A is false: no part of a PK may be NULL; R is true.'),
    ('An email address is a candidate key for a Users table.', 'Candidate keys must be numeric.', 2, 'If emails are unique, A is true; keys need not be numeric, so R is false.'),
    ('A primary key must contain a unique value for every record.', 'Most DBMSs automatically create an index on the primary key.', 1, 'Both true, but the index is an implementation detail; uniqueness is required so that each record can be identified.'),
])


R.facts('ch01-st3', F(
    terms=[('database management system (DBMS)', 'software that creates, maintains and controls access to a database, providing data storage, querying, security, integrity and concurrency control'),
           ('data integrity', 'the accuracy, consistency and completeness of data over its whole life cycle'),
           ('concurrency control', 'DBMS mechanisms, such as locking or timestamps, that let several users work on the same data at the same time without corrupting it'),
           ('record locking', 'preventing other transactions from changing (or reading) a record while one transaction is updating it'),
           ('deadlock', 'a situation where two transactions each wait for a lock held by the other, so neither can proceed'),
           ('data dictionary', 'metadata stored by the DBMS describing tables, fields, data types, constraints, relationships and users'),
           ('entity integrity', 'the rule that every table has a primary key whose values are unique and never NULL'),
           ('referential integrity', 'the rule that every foreign key value must match an existing primary key value in the referenced table (or be NULL)')],
    facts=[('Two clerks read the same stock level of 20, each sells items and writes back their own new total. What problem is this?', 'Lost update', ['Deadlock', 'Dirty read', 'Phantom read'], 'The second write overwrites the first, so one update is lost.'),
           ('Which DBMS feature lets different users see only the parts of a database they are allowed to?', 'User views and access privileges', ['Normalisation', 'Data types', 'Indexes'], 'Views and GRANTed privileges restrict what each user can see or change.'),
           ('Which of the following is an example of a domain (field-level) integrity constraint?', 'CHECK (Age BETWEEN 0 AND 120)', ['FOREIGN KEY (DeptID) REFERENCES Dept', 'PRIMARY KEY (StudentID)', 'CREATE INDEX idx ON Staff(Name)'], 'A CHECK restricts the values allowed in a field (its domain).'),
           ('A transaction T1 locks record A and waits for record B, while T2 locks B and waits for A. This is…', 'deadlock', ['a lost update', 'a rollback', 'a referential-integrity violation'], 'Each holds what the other needs.')],
    why=[('Explain why a DBMS needs concurrency control in a multi-user system.', 'Several users may read and update the same records at the same time; without locking or similar control, interleaved operations can cause lost updates, dirty reads or inconsistent results, corrupting the data.'),
         ('Explain how record locking prevents the lost update problem.', 'The first transaction to update a record obtains a lock; the second must wait until the first commits and releases it, then reads the updated value, so both changes are applied in sequence.'),
         ('Explain why a DBMS separates the logical view of data from its physical storage (data independence).', 'Applications access data by tables and fields, not file locations, so storage structures and indexes can change without rewriting programs, and different users can have different views.'),
         ('Explain why regular backups do not on their own guarantee data integrity.', 'Backups allow recovery after loss but do not stop incorrect, inconsistent or concurrent-update errors entering the data; validation, constraints and concurrency control are also needed.')],
    contrast=[('validation', 'verification', 'Validation checks that data is reasonable and obeys rules (range, type, format) when entered; verification checks that data has been copied or entered accurately, e.g. double entry or proof-reading against the source.'),
              ('entity integrity', 'referential integrity', 'Entity integrity requires a unique, non-NULL primary key in every table; referential integrity requires every foreign key to match an existing primary key in the referenced table.'),
              ('a shared (read) lock', 'an exclusive (write) lock', 'A shared lock lets many transactions read a record but none write it; an exclusive lock gives one transaction sole access to read and write it.'),
              ('data security', 'data integrity', 'Security protects data from unauthorised access or loss (passwords, encryption, privileges, backups); integrity is about the data being accurate and consistent.')],
    misc=[('Locking every table for the entire day is the best way to stop concurrency problems.', 'It would prevent concurrency problems but make the database unusable for other users; locks should be as fine-grained (record level) and short as possible.'),
          ('If data passes validation it must be correct.', 'Validation only checks data is reasonable (e.g. an age of 34 is in range); the true age might be 43. Verification is needed to check accuracy.'),
          ('Deadlock can be fixed by making both transactions wait longer.', 'Waiting longer never resolves a deadlock; the DBMS must detect it and roll back one transaction (or prevent it by ordering lock requests).')],
    evaluate=[('Optimistic concurrency control (checking for conflicts only at commit) is better than pessimistic locking for an online shop.', ['most transactions do not conflict, so no time is wasted waiting for locks', 'better throughput and no deadlocks'], ['when conflicts are frequent (e.g. last items in stock) many transactions must be restarted', 'users may lose work if their transaction is rejected at commit'], 'Optimistic control suits read-heavy workloads with rare conflicts; pessimistic locking is safer for high-contention records such as stock levels of popular items.')],
    extended=[('A ticket agency in Melbourne sells seats online from several servers. Explain, with reference to a specific sequence of events, how two customers could be sold the same seat, and describe two DBMS mechanisms that would prevent this.', 'Sequence: customer A reads seat 14C as free; customer B reads 14C as free; A writes "sold to A"; B writes "sold to B" (lost update – both receive tickets). Prevention: exclusive record lock on the seat when a transaction begins the purchase so B must wait and then sees it sold; a transaction with a UNIQUE constraint/condition (UPDATE … WHERE status = \'free\') executed atomically so only one succeeds; or optimistic control with version numbers that rejects the second commit.', 6)],
))


@R.add('ch01-st3', 'C3', (2, 5), 'numerical')
def lost_update(rng, slot):
    ctx = rng.choice([('a shared bank account in Accra', 'balance', '€'), ('the stock level of a phone model in a Dubai warehouse', 'stock', ''),
                      ('the number of free seats on a Lima–Bogotá flight', 'seats', ''), ('a café loyalty-points total in Toronto', 'points', '')])
    what, var, unit = ctx
    start = rng.randint(20, 90) if unit == '' else rng.randint(200, 900)
    a = rng.randint(2, 15) if unit == '' else rng.randint(20, 150)
    b = rng.randint(2, 15) if unit == '' else rng.randint(20, 150)
    op1 = rng.choice(['+', '-'])
    op2 = rng.choice(['+', '-'])
    f = lambda x, op, v: x + v if op == '+' else x - v
    sched = rng.choice(['R1 R2 W1 W2', 'R1 R2 W2 W1', 'R1 W1 R2 W2'])
    vals = {}
    db = start
    for step in sched.split():
        t = step[1]
        if step[0] == 'R':
            vals[t] = db
        else:
            db = f(vals[t], op1 if t == '1' else op2, a if t == '1' else b)
    correct = f(f(start, op1, a), op2, b)
    desc = {'R': 'reads', 'W': 'writes'}
    steps = '; '.join(f'T{s[1]} {desc[s[0]]}' for s in sched.split())
    o1 = ('adds' if op1 == '+' else 'subtracts') + f' {unit}{a}'
    o2 = ('adds' if op2 == '+' else 'subtracts') + f' {unit}{b}'
    lost = db != correct
    ans = f'Final value {unit}{db}; correct value {unit}{correct}.' + (' An update was lost.' if lost else ' No update was lost because the schedule is serial.')
    extra = ' Explain how an exclusive lock would change the outcome.' if slot.d >= 4 else ''
    return dict(stem=f'Transactions T1 and T2 both update {what} (the {var}), starting at {unit}{start}. T1 {o1}; T2 {o2}. Each transaction reads the {var}, computes the new value and writes it. The operations run in the order: {steps}. Determine the final stored {var} and state whether this is correct.{extra}',
                answer=ans, markingKey=ans + ' M1 trace of the values read by each transaction; A1 final value; R1 comparison with the serial result.' + (' Lock: T1 holds an exclusive lock until it commits, so T2 must read after W1, giving the correct value.' if slot.d >= 4 else ''),
                marks=3 if slot.d <= 3 else 5)


_INTEG = [
    ('a new Student record is inserted with StudentID NULL', 'entity integrity', 'the primary key must not be NULL'),
    ('an Order is inserted with CustomerID 908, but no customer 908 exists', 'referential integrity', 'a foreign key must match an existing primary key'),
    ('an exam mark of 134 is entered where marks must be 0–100', 'domain integrity', 'the value is outside the allowed domain (CHECK constraint)'),
    ('two Product records are given ProductID P17', 'entity integrity', 'primary key values must be unique'),
    ('a Department row is deleted while Staff rows still reference it', 'referential integrity', 'deleting a referenced parent leaves orphan child records'),
    ('a date of 31/02/2026 is stored in a booking', 'domain integrity', 'the value is not a valid DATE'),
    ('an Employee is given a Salary of −2000', 'domain integrity', 'the value breaks a CHECK (Salary > 0) rule'),
    ('a Loan row refers to BookID B999 that was never added', 'referential integrity', 'the foreign key has no matching parent'),
]


@R.add('ch01-st3', 'C3', (1, 3), 'short')
def integ_classify(rng, slot):
    k = 1 if slot.d <= 1 else 2 if slot.d == 2 else 3
    its = rng.sample(_INTEG, k)
    stem = 'For each event, identify the type of integrity rule that is broken and explain why.\n' + '\n'.join(f'{i + 1}. {e}' for i, (e, _, _) in enumerate(its)) if k > 1 else f'In a school database, {its[0][0]}. Identify the type of integrity rule that is broken and explain why.'
    ans = '; '.join(f'{i + 1}. {t} – {w}' for i, (_, t, w) in enumerate(its))
    return dict(stem=stem, answer=ans, markingKey=ans + ' 1 mark per correct type with reason.', marks=k + (1 if k == 1 else 0))


ar('ch01-st3', [
    ('A DBMS can enforce referential integrity automatically.', 'Foreign-key constraints are stored in the data dictionary and checked on every insert, update and delete.', 0, 'Both true; the stored constraints are why it can be automatic.'),
    ('Record-level locking allows more concurrency than table-level locking.', 'Other transactions can still update different records of the same table.', 0, 'Both true and R explains A.'),
    ('Validation guarantees that data is accurate.', 'Validation checks that data is sensible and obeys rules.', 3, 'A is false (data can be valid but wrong); R is true.'),
    ('Deadlock is resolved by the DBMS rolling back one of the transactions.', 'Rolling back releases that transaction\'s locks so the other can continue.', 0, 'Both true; releasing locks is why rollback resolves it.'),
])


R.facts('ch01-st4', F(
    terms=[('NoSQL database', 'a non-relational database that stores data as documents, key-value pairs, wide columns or graphs, usually with a flexible schema and horizontal scaling'),
           ('schema-on-write', 'the structure of the data is fixed before data is stored and every record must conform to it, as in a relational database'),
           ('schema-on-read', 'data is stored in its raw or flexible form and a structure is applied only when the data is read'),
           ('horizontal scaling', 'adding more servers (nodes) to share the data and workload, as many NoSQL systems do'),
           ('vertical scaling', 'increasing the power (CPU, memory, storage) of a single server'),
           ('BASE', 'basically available, soft state, eventually consistent – the looser consistency model of many NoSQL systems')],
    facts=[('Which situation is best suited to a relational database rather than a NoSQL store?', 'A banking system where transfers must be ACID-compliant', ['Storing millions of social-media posts with varying fields', 'Caching session data by session ID', 'Storing a social network of friendships'], 'Strong consistency and structured, related data favour relational DBMSs.'),
           ('Which is a typical advantage of NoSQL databases?', 'Flexible schemas and easy horizontal scaling', ['Guaranteed ACID transactions across all nodes', 'A standard query language used by every product', 'Stronger normalisation'], 'NoSQL trades strict consistency/standardisation for flexibility and scale.'),
           ('Which term describes a system that may briefly return old data after an update but will become consistent later?', 'Eventual consistency', ['Atomicity', 'Referential integrity', 'Normalisation'], 'Eventual consistency is part of the BASE model.')],
    why=[('Explain why relational databases can be difficult to scale horizontally.', 'Joins and ACID transactions need data from many tables to be consistent at once; splitting tables across many servers makes joins slow and coordinating transactions across nodes costly.'),
         ('Explain why a fixed relational schema can be a disadvantage for an application that stores product reviews with photos, videos and varying tags.', 'Each review may have different attributes; a fixed schema would need many NULL columns or extra tables and schema changes for every new attribute, whereas a document store can hold each review as a flexible document.'),
         ('Explain why many NoSQL systems accept eventual consistency.', 'By the CAP theorem a distributed system that must remain available during network partitions cannot also guarantee immediate consistency; accepting eventual consistency keeps the system available and fast across many nodes.')],
    contrast=[('a relational database', 'a document database', 'A relational database stores data in fixed-schema tables linked by keys and queried with SQL joins; a document database stores self-contained, flexible JSON-like documents that can nest related data, avoiding joins.'),
              ('ACID', 'BASE', 'ACID guarantees atomic, consistent, isolated and durable transactions; BASE favours availability and accepts soft state and eventual consistency.'),
              ('vertical scaling', 'horizontal scaling', 'Vertical scaling upgrades one server; horizontal scaling adds more servers and distributes the data and load between them.')],
    misc=[('NoSQL databases cannot be queried.', 'NoSQL databases have their own query APIs/languages (e.g. MongoDB queries, Cypher for graphs); "NoSQL" usually means "not only SQL".'),
          ('NoSQL databases have replaced relational databases.', 'Both are widely used; relational databases remain the best choice for structured data needing integrity and transactions, and many systems combine the two (polyglot persistence).'),
          ('Non-relational databases have no structure at all.', 'They have structure (documents, key-value pairs, column families, nodes and edges) – it is just more flexible and not enforced by a fixed table schema.')],
    apply=[('A streaming service in Seoul stores user profiles, watch histories of different lengths and recommendations. Suggest whether a relational or a document database is more suitable for the watch histories and justify your answer.', 'Document database: each user\'s history is a variable-length list naturally stored as an array inside the user document, read in one operation without joins; scales horizontally for millions of users; strict ACID transactions are not essential for viewing history.', 3),
           ('A university in Vienna must record exam results that feed into degree classifications. Recommend relational or NoSQL storage and justify.', 'Relational: data is highly structured and related (students, modules, results), integrity constraints and ACID transactions are essential, and complex SQL reports are needed.', 3),
           ('An online multiplayer game in Singapore needs to store each player\'s current session state and fetch it in under a millisecond. Recommend a database type and justify.', 'A key-value store (in memory): the session is looked up by a single key (session/player ID), no relationships or joins are needed, and key-value stores give very fast reads and writes and scale horizontally.', 3)],
    evaluate=[('Organisations should replace their relational databases with NoSQL databases to cope with big data.', ['NoSQL scales horizontally and handles semi-structured, high-velocity data', 'flexible schema speeds up development'], ['loses ACID guarantees and integrity constraints', 'staff skills and SQL tooling are built around relational systems', 'many workloads are structured and modest in size'], 'Replacement is rarely justified wholesale; use NoSQL where data variety/scale demand it and keep relational systems for transactional, structured data.'),
              ('Eventual consistency is acceptable for every web application.', ['improves availability and speed', 'users rarely notice short delays in, e.g., like counts'], ['financial balances, stock and bookings must be consistent immediately', 'stale reads can cause double bookings or overspending'], 'Acceptable only where short-lived stale data has low cost; not for transactions involving money or limited resources.')],
))

_DB_CHOICE = [
    ('A fitness-tracker company in Melbourne collects millions of heart-rate readings per minute from wearable devices.', 'non-relational (wide-column or time-series store)', 'very high write volume of simple time-stamped readings, needs horizontal scaling; few joins; slight delays in consistency are acceptable', 'readings are append-only, so the main relational advantage (complex transactions and integrity across tables) is not needed'),
    ('A news website in Mexico City stores articles whose fields differ by type (video, live blog, photo essay).', 'non-relational (document database)', 'each article type has different attributes, so flexible JSON documents avoid many NULL columns and schema changes', 'joins are rarely needed because each article is read as a whole document'),
    ('A national pension fund in Oslo records contributions and payouts for every citizen.', 'relational', 'highly structured, related financial data needing ACID transactions, referential integrity and auditable SQL reporting', 'eventual consistency would be unacceptable for money; volume is large but manageable for a relational DBMS'),
    ('A logistics firm in Dubai needs to find the shortest chain of partners connecting two warehouses.', 'non-relational (graph database)', 'the query is a traversal of relationships; edges are stored directly so multi-hop paths are fast', 'in SQL the same query needs repeated self-joins or recursive queries that slow down as depth grows'),
    ('A start-up in Hanoi is building a prototype app and expects its data model to change weekly.', 'non-relational (document database) for the prototype', 'a flexible schema lets developers add fields without migrations', 'once the model stabilises and integrity matters (payments, orders), parts may move to a relational design'),
    ('A university in Vienna must record exam results that feed into degree classifications.', 'relational', 'structured data (students, modules, results) with strict integrity constraints and complex SQL reports', 'ACID transactions prevent partial or inconsistent updates to official records'),
]


@R.add('ch01-st4', 'C3', (2, 5), 'short')
def db_choice(rng, slot):
    ctx, choice, why1, why2 = rng.choice(_DB_CHOICE)
    q = rng.choice([('Discuss whether a relational or a non-relational database would be more suitable.', 4),
                    ('Recommend a database model for this organisation, justifying your choice.', 3),
                    ('Identify one advantage and one disadvantage of using a NoSQL database here.', 2)])
    if q[1] == 2:
        ans = (f'Advantage: {why1 if "non-relational" in choice else "horizontal scaling / flexible schema"}. '
               f'Disadvantage: {"weaker consistency and no standard joins/SQL; integrity must be enforced in application code" if "non-relational" in choice else why1 + " – a NoSQL store would weaken these guarantees"}.')
    else:
        ans = f'Recommended: {choice}. Reasons: {why1}; {why2}.'
    return dict(stem=f'{ctx} {q[0]}', answer=ans, markingKey=ans + ' Marks for a justified choice explicitly linked to the scenario; a well-argued alternative choice may also be credited.', marks=q[1] + (1 if slot.d >= 4 else 0))


pick_mcq('ch01-st4', 'C2', (2, 3), [
    ('Which statement best explains why a graph database suits a social network?', 'Relationships are stored directly as edges, so traversing friends-of-friends does not require repeated joins', ['It stores all data in a single table', 'It enforces a fixed schema', 'It guarantees ACID transactions across nodes'], 'Graph databases store relationships as first-class edges.'),
    ('A relational database is said to use schema-on-write. This means…', 'data must match the table structure when it is stored', ['the structure is decided only when data is queried', 'any data can be written without checks', 'the schema is written in JSON'], 'Relational tables enforce their schema at insert time.'),
])


# =============================================================================================
# ch02 A3.2 Database design
# =============================================================================================
_ERD = {
    'a library network in Oslo': [
        ('Member', 'Loan', '1:M', 'A member can have many loans, but each loan is made by exactly one member.'),
        ('Copy', 'Loan', '1:M', 'A copy of a book can be lent many times over the years; each loan is of one copy.'),
        ('Book', 'Author', 'M:N', 'A book can have several authors and an author can write several books.'),
        ('Branch', 'Copy', '1:M', 'Each copy is held at one branch; a branch holds many copies.'),
        ('Member', 'LibraryCard', '1:1', 'Each member has exactly one library card and each card belongs to one member.')],
    'a secondary school in Singapore': [
        ('Teacher', 'Class', '1:M', 'A teacher teaches many classes; each class has one teacher.'),
        ('Student', 'Club', 'M:N', 'A student may join many clubs and each club has many students.'),
        ('Department', 'Teacher', '1:M', 'A department employs many teachers; each teacher belongs to one department.'),
        ('Student', 'Locker', '1:1', 'Each student is allocated one locker and each locker is allocated to one student.'),
        ('Student', 'Course', 'M:N', 'Students take several courses and each course is taken by many students.')],
    'a hospital in Nairobi': [
        ('Ward', 'Patient', '1:M', 'A ward holds many patients; an admitted patient is in one ward.'),
        ('Doctor', 'Patient', 'M:N', 'A doctor treats many patients and a patient can be treated by several doctors.'),
        ('Patient', 'Admission', '1:M', 'A patient may be admitted many times; each admission is for one patient.'),
        ('Doctor', 'Specialism', 'M:1', 'Each doctor has one main specialism; a specialism has many doctors.'),
        ('Drug', 'Prescription', 'M:N', 'A prescription can contain several drugs and a drug appears on many prescriptions.')],
    'an airline based in Dubai': [
        ('Aircraft', 'Flight', '1:M', 'An aircraft operates many flights; each flight uses one aircraft.'),
        ('Passenger', 'Flight', 'M:N', 'A passenger takes many flights and a flight carries many passengers.'),
        ('Airport', 'Flight', '1:M', 'An airport is the departure airport of many flights; each flight departs from one airport.'),
        ('Pilot', 'Licence', '1:1', 'Each pilot holds one current licence and each licence belongs to one pilot.'),
        ('CrewMember', 'Flight', 'M:N', 'Crew members work on many flights and each flight has several crew.')],
    'a football league in Lisbon': [
        ('Team', 'Player', '1:M', 'A team has many players; a player is registered with one team.'),
        ('Team', 'Match', 'M:N', 'A team plays many matches and each match involves two teams.'),
        ('Stadium', 'Team', '1:M', 'A stadium may be home to several teams; each team has one home stadium.'),
        ('Team', 'Coach', '1:1', 'Each team has one head coach who coaches only that team.'),
        ('Player', 'Sponsor', 'M:N', 'A player can have several sponsors and a sponsor can support several players.')],
}


def _impl(a, b, card):
    return {'1:M': f'put the primary key of {a} as a foreign key in {b}',
            'M:1': f'put the primary key of {b} as a foreign key in {a}',
            'M:N': f'create a link table {a}{b} containing {a}ID and {b}ID as foreign keys forming a composite primary key',
            '1:1': f'put the primary key of one table as a UNIQUE foreign key in the other (e.g. {a}ID in {b})'}[card]


_CARD_WORDS = {'1:M': 'one-to-many', 'M:1': 'many-to-one', 'M:N': 'many-to-many', '1:1': 'one-to-one'}


@R.add('ch02-st1', 'C3', (1, 4), 'short')
def erd_card(rng, slot):
    dom = rng.choice(list(_ERD))
    k = 1 if slot.d <= 2 else 2 if slot.d == 3 else 3
    rules = rng.sample(_ERD[dom], k)
    txt = ' '.join(r[3] for r in rules)
    ans = '; '.join(f'{a}–{b}: {_CARD_WORDS[c]} ({c}) – {_impl(a, b, c)}' for a, b, c, _ in rules)
    return dict(stem=f'The following business rules apply to {dom}. {txt} For each relationship, state its cardinality and describe how it would be implemented in a relational database.',
                answer=ans, markingKey=f'{ans}. 1 mark per correct cardinality, 1 mark per correct implementation.', marks=2 * k)


@R.add('ch02-st1', 'C3', (2, 5), 'short')
def erd_tables(rng, slot):
    dom = rng.choice(list(_ERD))
    rules = rng.sample(_ERD[dom], rng.randint(3, 4) if slot.d <= 3 else 5)
    ents = []
    for a, b, _, _ in rules:
        for e in (a, b):
            if e not in ents:
                ents.append(e)
    links = [f'{a}{b}' for a, b, c, _ in rules if c == 'M:N']
    n = len(ents) + len(links)
    txt = ' '.join(r[3] for r in rules)
    ans = f'{n} tables: {", ".join(ents)}' + (f' plus link table(s) {", ".join(links)}' if links else '') + '.'
    return dict(stem=f'A designer for {dom} records these rules. {txt} Determine the minimum number of tables needed in a normalised relational implementation, naming each table.',
                answer=ans, markingKey=f'One table per entity ({len(ents)}) (M1) plus one link table for each many-to-many relationship ({len(links)}) (M1); {ans} (A1).', marks=3)


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def erd_mcq(rng, slot):
    dom = rng.choice(list(_ERD))
    a, b, c, txt = rng.choice(_ERD[dom])
    corr = _CARD_WORDS[c]
    wr = [w for w in ['one-to-one', 'one-to-many', 'many-to-many', 'many-to-one'] if w != corr]
    if c == 'M:1':
        wr = [w for w in wr if w != 'one-to-many'] + ['none of these']
    return mcq(rng, f'In {dom}: "{txt}" What is the cardinality of the relationship from {a} to {b}?', corr, wr[:3],
               f'{txt} gives {corr} ({c}).')


R.facts('ch02-st1', F(
    terms=[('entity', 'a thing or object of interest about which data is stored, represented by a table'),
           ('entity-relationship diagram (ERD)', 'a diagram showing the entities in a system, their attributes and the relationships and cardinalities between them'),
           ('cardinality', 'the number of instances of one entity that can be associated with an instance of another (1:1, 1:M or M:N)'),
           ('attribute', 'a property or characteristic of an entity, implemented as a field'),
           ('link (junction) table', 'a table that resolves a many-to-many relationship into two one-to-many relationships by holding the keys of both entities'),
           ('optionality (participation)', 'whether an entity instance must take part in a relationship (mandatory) or may not (optional)')],
    why=[('Explain why many-to-many relationships are removed from a logical ERD before implementation.', 'Relational tables cannot hold a list of foreign keys in one field, so an M:N relationship must be resolved into a link entity with two 1:M relationships; the link table can also store attributes of the relationship (e.g. date enrolled).'),
         ('Explain why an ERD is produced before any tables are created.', 'It models the entities and rules agreed with the client at a high level, so design errors (missing entities, wrong cardinalities) are found cheaply before implementation; it also communicates the design to non-technical stakeholders.'),
         ('Explain how crow\'s-foot notation shows a one-to-many relationship.', 'A single line (or bar) at the "one" end and a three-pronged crow\'s foot at the "many" end of the line joining the two entities; circles/bars can add optional or mandatory participation.'),
         ('Explain why the foreign key is placed on the "many" side of a one-to-many relationship.', 'Each record on the many side relates to exactly one record on the one side, so it can store a single foreign key value; placing it on the one side would need a list of values.')],
    contrast=[('an entity', 'an attribute', 'An entity is an object about which data is stored (e.g. Patient), becoming a table; an attribute is a property of that entity (e.g. DateOfBirth), becoming a field.'),
              ('a mandatory relationship', 'an optional relationship', 'In a mandatory relationship every instance must participate (each Order must have a Customer); in an optional one an instance may have no related record (a Customer may have no Orders yet).'),
              ('a conceptual ERD', 'a logical ERD', 'A conceptual ERD shows entities and relationships only, possibly with M:N; a logical ERD adds attributes, keys and resolves M:N relationships ready for tables.')],
    misc=[('In a one-to-many relationship between Customer and Order, the OrderID should be stored in the Customer table.', 'The foreign key goes on the many side: CustomerID is stored in Order. Storing OrderIDs in Customer would need a list of values in one field.'),
          ('A many-to-many relationship can be implemented by putting a foreign key in each table.', 'Each table could then link to only one record of the other; a link table with a composite key is required.'),
          ('An ERD shows the data stored in each record.', 'An ERD shows the structure – entities, attributes and relationships – not actual data values.')],
    evaluate=[('An ERD is unnecessary for a small database with only three tables.', ['for very small systems the relationships may be obvious', 'saves design time'], ['even small designs can contain M:N relationships or wrong cardinalities', 'documentation helps future maintenance and communication with the client', 'small systems often grow'], 'A quick ERD is still worthwhile because it is cheap and prevents structural errors that are costly to fix after data is loaded.')],
    extended=[('A music-streaming service in Seoul stores Artists, Albums, Tracks and Playlists. An artist releases many albums; an album has many tracks; a track can appear on many playlists and a playlist contains many tracks; each playlist is created by one user and a user can create many playlists. Describe the ERD (entities, relationships and cardinalities) and list the tables with their primary and foreign keys.', 'Entities: Artist, Album, Track, Playlist, User, PlaylistTrack (link). Artist 1:M Album; Album 1:M Track; User 1:M Playlist; Track M:N Playlist resolved by PlaylistTrack. Tables: Artist(ArtistID PK, Name), Album(AlbumID PK, Title, ArtistID FK), Track(TrackID PK, Title, Duration, AlbumID FK), User(UserID PK, Name), Playlist(PlaylistID PK, Name, UserID FK), PlaylistTrack(PlaylistID FK, TrackID FK, Position; PK (PlaylistID, TrackID)).', 8)],
))
ar('ch02-st1', [
    ('A link table is needed to implement a many-to-many relationship.', 'A field in a relational table must contain a single atomic value.', 0, 'Both true; atomic fields are why a link table is needed.'),
    ('In a one-to-many relationship the foreign key is placed in the table on the "one" side.', 'The "one" side table holds the primary key that is referenced.', 3, 'A is false (FK goes on the many side); R is true.'),
    ('A one-to-one relationship can often be implemented by merging the two tables.', 'Each record in one table matches exactly one record in the other.', 0, 'Both true; the exact pairing is why merging is possible.'),
])


# ---- normalisation: functional-dependency engine ----
_SCHEMAS = [
    ('an online shop in Toronto', 'OrderLine',
     ['OrderID', 'ProductID', 'Quantity', 'ProductName', 'UnitPrice', 'OrderDate', 'CustomerID', 'CustomerName'],
     [({'OrderID', 'ProductID'}, {'Quantity'}), ({'ProductID'}, {'ProductName', 'UnitPrice'}), ({'OrderID'}, {'OrderDate', 'CustomerID'}), ({'CustomerID'}, {'CustomerName'})],
     ['OrderID', 'ProductID']),
    ('a school in Geneva', 'Enrolment',
     ['StudentID', 'CourseID', 'Grade', 'StudentName', 'CourseTitle', 'TeacherID', 'TeacherName'],
     [({'StudentID', 'CourseID'}, {'Grade'}), ({'StudentID'}, {'StudentName'}), ({'CourseID'}, {'CourseTitle', 'TeacherID'}), ({'TeacherID'}, {'TeacherName'})],
     ['StudentID', 'CourseID']),
    ('a hotel in Cape Town', 'Booking',
     ['BookingID', 'GuestID', 'GuestName', 'RoomNo', 'RoomType', 'NightlyRate', 'CheckIn'],
     [({'BookingID'}, {'GuestID', 'RoomNo', 'CheckIn'}), ({'GuestID'}, {'GuestName'}), ({'RoomNo'}, {'RoomType'}), ({'RoomType'}, {'NightlyRate'})],
     ['BookingID']),
    ('a football league in Bogotá', 'MatchPlayer',
     ['MatchID', 'PlayerID', 'Goals', 'PlayerName', 'TeamID', 'TeamName', 'MatchDate', 'Venue'],
     [({'MatchID', 'PlayerID'}, {'Goals'}), ({'PlayerID'}, {'PlayerName', 'TeamID'}), ({'TeamID'}, {'TeamName'}), ({'MatchID'}, {'MatchDate', 'Venue'})],
     ['MatchID', 'PlayerID']),
    ('a clinic in Kuala Lumpur', 'PrescriptionItem',
     ['PrescriptionID', 'DrugCode', 'Dose', 'PatientID', 'PatientName', 'DrugName', 'DoctorID', 'DoctorName'],
     [({'PrescriptionID', 'DrugCode'}, {'Dose'}), ({'PrescriptionID'}, {'PatientID', 'DoctorID'}), ({'PatientID'}, {'PatientName'}), ({'DrugCode'}, {'DrugName'}), ({'DoctorID'}, {'DoctorName'})],
     ['PrescriptionID', 'DrugCode']),
    ('a car-hire firm in Melbourne', 'Rental',
     ['RentalID', 'CarReg', 'Model', 'DailyRate', 'CustomerID', 'CustomerName', 'StartDate'],
     [({'RentalID'}, {'CarReg', 'CustomerID', 'StartDate'}), ({'CarReg'}, {'Model'}), ({'Model'}, {'DailyRate'}), ({'CustomerID'}, {'CustomerName'})],
     ['RentalID']),
]


def _closure(X, fds):
    X = set(X)
    ch = True
    while ch:
        ch = False
        for l, r in fds:
            if l <= X and not r <= X:
                X |= r
                ch = True
    return X


def _project(attrs, fds):
    S = set(attrs)
    out = []
    for k in range(1, len(attrs)):
        for X in itertools.combinations(attrs, k):
            X = set(X)
            cl = _closure(X, fds) & S
            for a in sorted(cl - X):
                if not any(l <= X and a in r for l, r in out if l < X or l == X):
                    if not any(_closure(set(Y), fds) >= {a} for j in range(1, len(X)) for Y in itertools.combinations(sorted(X), j)):
                        out.append((X, {a}))
    # remove redundant FDs
    cover = list(out)
    for f_ in list(cover):
        rest = [g for g in cover if g is not f_]
        if f_[1] <= _closure(f_[0], rest):
            cover = rest
    merged: dict = {}
    for l, r in cover:
        merged.setdefault(frozenset(l), set()).update(r)
    return [(set(l), r) for l, r in merged.items()]


def _keys(attrs, fds):
    S = set(attrs)
    ks = []
    for k in range(1, len(attrs) + 1):
        for X in itertools.combinations(attrs, k):
            if any(set(c) <= set(X) for c in ks):
                continue
            if _closure(X, fds) >= S:
                ks.append(X)
    return ks


def _nf(attrs, fds):
    ks = _keys(attrs, fds)
    prime = set(a for k in ks for a in k)
    partial, trans = [], []
    for k in ks:
        for j in range(1, len(k)):
            for Y in itertools.combinations(k, j):
                for a in sorted((_closure(set(Y), fds) & set(attrs)) - prime - set(Y)):
                    partial.append((Y, a))
    for l, r in fds:
        if not (_closure(l, fds) >= set(attrs)):
            for a in sorted(r - prime):
                if not any(set(Y) == l and a == b for Y, b in partial) and not any(set(Y) < set(k) and set(Y) == l for k in ks for Y, _ in partial):
                    trans.append((tuple(sorted(l)), a))
    nf = '1NF' if partial else '2NF' if trans else '3NF'
    return nf, ks, partial, trans


def _synth(attrs, fds, ks, rel):
    rels = []
    for l, r in fds:
        rels.append((sorted(l), sorted(r - l)))
    if not any(set(k) <= set(l) | set(r) for k in ks for l, r in rels):
        rels.append((list(ks[0]), []))
    rels = [x for x in rels if not any((set(x[0]) | set(x[1])) < (set(y[0]) | set(y[1])) for y in rels)]
    return rels


def _fd_txt(l, r):
    return ', '.join(sorted(l)) + ' → ' + ', '.join(sorted(r))


def _schema_draw(rng, slot):
    for _ in range(30):
        ctx, rel, attrs, fds, key = rng.choice(_SCHEMAS)
        keep = list(key) + [a for a in attrs if a not in key and rng.random() < (0.85 if slot.d >= 4 else 0.7)]
        keep = [a for a in attrs if a in keep]
        if len(keep) < 4:
            continue
        pf = _project(keep, fds)
        if not pf:
            continue
        return ctx, rel, keep, pf
    return None


def _rel_str(rels, ks=None):
    out = []
    for l, r in rels:
        out.append('(' + ', '.join([f'{a}*' for a in l] + list(r)) + ')')
    return '; '.join(out)


@R.add('ch02-st2', 'C3', (2, 4), 'short')
def nf_identify(rng, slot):
    d = _schema_draw(rng, slot)
    if not d:
        return None
    ctx, rel, keep, pf = d
    nf, ks, partial, trans = _nf(keep, pf)
    fdl = '\n'.join(_fd_txt(l, r) for l, r in pf)
    reason = []
    if partial:
        reason.append('partial dependencies: ' + '; '.join(f'{a} depends only on {", ".join(Y)}' for Y, a in partial[:4]))
    if trans:
        reason.append('transitive dependencies: ' + '; '.join(f'{a} depends on non-key {", ".join(l)}' for l, a in trans[:4]))
    why = ' and '.join(reason) if reason else 'every non-key attribute depends on the whole key and nothing but the key'
    kt = ' or '.join('(' + ', '.join(k) + ')' for k in ks)
    ans = f'Candidate key {kt}. Highest normal form: {nf}, because {why}.'
    return dict(stem=f'A table used by {ctx} is {rel}({", ".join(keep)}) with the functional dependencies:\n{fdl}\nIdentify the primary key and state the highest normal form the table is in, justifying your answer.',
                answer=ans, markingKey=f'{ans} 1 mark key; 1 mark normal form; 1-2 marks justification naming the specific dependencies.', marks=3 if slot.d <= 3 else 4)


@R.add('ch02-st2', 'C3', (3, 5), 'multi_step')
def nf_decompose(rng, slot):
    d = _schema_draw(rng, slot)
    if not d:
        return None
    ctx, rel, keep, pf = d
    nf, ks, partial, trans = _nf(keep, pf)
    if nf == '3NF':
        return None
    rels = _synth(keep, pf, ks, rel)
    fdl = '\n'.join(_fd_txt(l, r) for l, r in pf)
    ans = f'{len(rels)} tables (key fields marked *): {_rel_str(rels)}'
    return dict(stem=f'{ctx[0].upper() + ctx[1:]} stores {rel}({", ".join(keep)}). The functional dependencies are:\n{fdl}\nNormalise the table to third normal form. Show each resulting table with its primary key.',
                answer=ans, markingKey=f'Key {", ".join(ks[0])} identified (A1). Remove partial dependencies to reach 2NF (M1), remove transitive dependencies to reach 3NF (M1). Final: {ans} (A1 per correct table; foreign keys retained so the original data can be rejoined).',
                marks=5 if slot.d <= 4 else 6, gap='G5')


@R.add('ch02-st2', 'C3', (1, 3), 'short')
def unf_rows(rng, slot):
    ctx = rng.choice([('order', 'product', 'an online bookshop in Lisbon'), ('student', 'club', 'a school in Hanoi'), ('patient', 'vaccination', 'a clinic in Accra'), ('flight', 'passenger', 'an airline in Lima')])
    a, b, where = ctx
    n = rng.randint(3, 5)
    groups = {f'{a[0].upper()}{100 + i}': rng.randint(1, 4) for i in range(n)}
    rows = '\n'.join(f'{k}: ' + ', '.join(f'{b[0].upper()}{rng.randint(10, 99)}' for _ in range(v)) for k, v in groups.items())
    tot = sum(groups.values())
    ans = f'{tot} rows (one per {a}-{b} pair); the primary key becomes the composite ({a.capitalize()}ID, {b.capitalize()}ID).'
    return dict(stem=f'At {where}, an unnormalised table stores each {a} with a repeating group of {b}s:\n{rows}\nThe table is converted to first normal form by giving each {b} its own row. State how many rows the 1NF table will contain and identify its primary key.',
                answer=ans, markingKey=f'Count of repeating values {" + ".join(map(str, groups.values()))} = {tot} (A1); composite key (A1).', marks=2)


R.facts('ch02-st2', F(
    terms=[('normalisation', 'the process of organising tables to reduce data redundancy and remove insert, update and delete anomalies'),
           ('first normal form (1NF)', 'a table with a primary key in which every field holds a single atomic value and there are no repeating groups'),
           ('second normal form (2NF)', 'a 1NF table in which every non-key attribute depends on the whole primary key, so there are no partial dependencies'),
           ('third normal form (3NF)', 'a 2NF table in which no non-key attribute depends on another non-key attribute, so there are no transitive dependencies'),
           ('functional dependency', 'a relationship A → B meaning that each value of A determines exactly one value of B'),
           ('partial dependency', 'a non-key attribute that depends on only part of a composite primary key'),
           ('transitive dependency', 'a non-key attribute that depends on another non-key attribute rather than directly on the primary key'),
           ('update anomaly', 'an inconsistency caused when a fact stored in several rows is changed in some rows but not others')],
    why=[('Explain why a table with a single-field primary key that is in 1NF is automatically in 2NF.', 'A partial dependency needs a non-key attribute to depend on part of a composite key; with a single-field key there is no "part" of the key, so no partial dependencies can exist.'),
         ('Explain why normalisation reduces update anomalies.', 'Each fact is stored once, in the table whose key determines it, so a change (e.g. a product price) is made in one row and cannot leave other copies inconsistent.'),
         ('Explain why a fully normalised database may sometimes be deliberately denormalised.', 'Highly normalised designs need many joins, which can slow read-heavy reporting; storing some redundant data (e.g. in a data warehouse) speeds up queries at the cost of extra storage and controlled redundancy.'),
         ('Explain why foreign keys must be kept when a table is decomposed during normalisation.', 'The decomposed tables must be joinable to recreate the original data without loss; the foreign keys provide the links (lossless-join decomposition).')],
    contrast=[('a partial dependency', 'a transitive dependency', 'A partial dependency is on part of a composite key (removed for 2NF); a transitive dependency is a non-key attribute depending on another non-key attribute (removed for 3NF).'),
              ('an insertion anomaly', 'a deletion anomaly', 'An insertion anomaly is being unable to add a fact without unrelated data (a new course with no students); a deletion anomaly is losing a fact unintentionally when deleting other data (deleting the last student removes the course).'),
              ('2NF', '3NF', '2NF removes partial dependencies on part of a composite key; 3NF additionally removes transitive dependencies between non-key attributes.')],
    misc=[('A table is in 1NF as long as it has a primary key.', '1NF also requires atomic values and no repeating groups (e.g. no "Subjects: Maths, CS" in one field).'),
          ('Normalisation always makes queries faster.', 'Normalisation reduces redundancy and anomalies but often requires more joins, which can make some queries slower.'),
          ('In 3NF there is no redundancy at all.', '3NF removes redundancy caused by partial and transitive dependencies, but some redundancy (e.g. repeated foreign key values) is needed and some anomalies can remain until BCNF.')],
    evaluate=[('Databases should always be normalised to third normal form.', ['removes redundancy and update/insert/delete anomalies', 'keeps data consistent and saves storage'], ['more tables mean more joins, slowing read-heavy queries', 'data warehouses and analytics deliberately denormalise', 'design effort and complexity increase'], 'For transactional (OLTP) systems 3NF is the right default; for analytical or performance-critical read workloads controlled denormalisation can be justified.')],
))
ar('ch02-st2', [
    ('A table whose primary key is a single field cannot contain a partial dependency.', 'A partial dependency is a dependency on part of a composite key.', 0, 'Both true; the definition in R explains A.'),
    ('Moving to 3NF removes transitive dependencies.', 'In 3NF every non-key attribute depends on the key, the whole key and nothing but the key.', 0, 'Both true; R states the 3NF condition.'),
    ('Normalisation increases the number of update anomalies.', 'Normalisation splits tables so that each fact is stored once.', 3, 'A is false – normalisation reduces anomalies; R is true.'),
    ('A table in 2NF must also be in 3NF.', 'A table in 2NF has no partial dependencies.', 3, 'A is false (transitive dependencies may remain); R is true.'),
])


# ---- data types, constraints and validation ----
import re as _re


_RULES = [
    ('Age', 'range check: an integer from {lo} to {hi} inclusive', 'range'),
    ('Username', 'length check: 6 to 12 characters', 'length'),
    ('StudentCode', 'format check: two capital letters followed by four digits (e.g. GE2041)', 'format'),
    ('Email', 'format check: contains exactly one "@" with at least one "." after it', 'email'),
    ('Rating', 'lookup check: one of 1, 2, 3, 4, 5', 'lookup'),
]


def _valid(kind, v, lo=0, hi=0):
    if kind == 'range':
        try:
            x = int(v)
        except ValueError:
            return False
        return lo <= x <= hi and str(x) == v.strip()
    if kind == 'length':
        return 6 <= len(v) <= 12
    if kind == 'format':
        return bool(_re.fullmatch(r'[A-Z]{2}\d{4}', v))
    if kind == 'email':
        return v.count('@') == 1 and '.' in v.split('@')[1] and len(v.split('@')[0]) > 0 and not v.split('@')[1].startswith('.') and not v.endswith('.')
    if kind == 'lookup':
        return v in {'1', '2', '3', '4', '5'}


@R.add('ch02-st3', 'C3', (1, 4), 'short')
def validate_inputs(rng, slot):
    fld, rule, kind = rng.choice(_RULES)
    lo, hi = rng.choice([(11, 18), (16, 65), (0, 120), (13, 19)])
    rule = rule.format(lo=lo, hi=hi)
    pools = {
        'range': [str(lo), str(hi), str(lo - 1), str(hi + 1), str((lo + hi) // 2), 'twelve', str(lo) + '.5'],
        'length': ['kofi', 'amara_k', 'sofia2008', 'ingrid.larsen99', 'mei_li', 'tomas_ruiz_19', 'abcdef', 'abcdefghijkl'],
        'format': ['GE2041', 'ge2041', 'GE204', 'G12041', 'NB9932', 'SG12345', 'LIM203'],
        'email': ['li.wei@mail.sg', 'kwame.mensah@uni', 'ana@@correo.pe', 'freya@oslo.no', '@school.ch', 'omar@dubai.ae'],
        'lookup': ['3', '0', '5', '6', '1', 'five'],
    }
    k = 3 if slot.d <= 2 else 4 if slot.d == 3 else 5
    vals = rng.sample(pools[kind], min(k, len(pools[kind])))
    res = [(v, _valid(kind, v, lo, hi)) for v in vals]
    ans = '; '.join(f'"{v}" {"accepted" if ok else "rejected"}' for v, ok in res)
    return dict(stem=f'A form for a club in {rng.choice(CITIES)} validates the field {fld} with a {rule}. State whether each of the following inputs is accepted or rejected: ' + ', '.join(f'"{v}"' for v in vals) + '.',
                answer=ans, markingKey=ans + '. 1 mark for each two correct (round down); boundary values are inside the range for an inclusive check.', marks=max(2, k - 1))


@R.add('ch02-st3', 'C3', (2, 4), 'short')
def test_data(rng, slot):
    fld, lo, hi = rng.choice([('number of tickets per booking', 1, 8), ('exam mark', 0, 100), ('age of a junior swimmer', 8, 17), ('quantity ordered', 1, 50), ('room temperature setting (°C)', 16, 28)])
    mid = rng.randint(lo + 1, hi - 1)
    ans = f'Normal: {mid}; boundary (extreme): {lo} and {hi}; boundary rejected: {lo - 1} and {hi + 1}; erroneous: e.g. "abc" or {r2(mid + 0.5)} (not an integer).'
    return dict(stem=f'A program accepts the {fld} as a whole number from {lo} to {hi} inclusive. Construct a set of test data containing normal, boundary and erroneous values, with the expected outcome for each.',
                answer=ans, markingKey=ans + ' 1 mark each for normal, boundary (both ends, just inside and just outside) and erroneous data with expected outcomes.', marks=3)


@R.add('ch02-st3', 'C3', (2, 5), 'short')
def check_inserts(rng, slot):
    n = 4 if slot.d <= 3 else 5
    if rng.random() < 0.5:
        tname = 'Athlete'
        cols = "AthleteID INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INTEGER CHECK (Age BETWEEN 14 AND 40), Event TEXT CHECK (Event IN ('100m', '400m', 'Long jump'))"
        def mk(i, fault):
            nm = "'" + rng.choice(['Kip', 'Ruiz', 'Sato', 'Okafor', 'Berg']) + "'"
            age = rng.choice([14, 19, 22, 30, 40])
            ev = rng.choice(['100m', '400m', 'Long jump'])
            if fault == 1:
                nm = 'NULL'
            elif fault == 2:
                age = rng.choice([13, 41, 9, 45])
            elif fault == 3:
                ev = rng.choice(['200m', 'High jump', 'Marathon'])
            elif fault == 4:
                i = 1
            return f"({i}, {nm}, {age}, '{ev}')"
    else:
        tname = 'Product'
        cols = 'ProductID INTEGER PRIMARY KEY, Price REAL CHECK (Price > 0), Stock INTEGER CHECK (Stock >= 0), Name TEXT UNIQUE'
        names = rng.sample(['Mug', 'Lamp', 'Desk', 'Chair', 'Kettle', 'Rug'], 5)
        def mk(i, fault):
            price = rng.choice([4.5, 12.0, 19.99, 7.25])
            stock = rng.choice([0, 5, 20, 3])
            nm = names[i - 1]
            if fault == 1:
                price = rng.choice([0, -3, -0.5])
            elif fault == 2:
                stock = rng.choice([-1, -10])
            elif fault == 3:
                nm = names[0]
            elif fault == 4:
                i = 1
            return f"({i}, {price}, {stock}, '{nm}')"
    faults = [0] + [rng.choice([0, 1, 2, 3, 4]) for _ in range(n - 1)]
    stmts = [f'INSERT INTO {tname} VALUES {mk(i + 1, f_)};' for i, f_ in enumerate(faults)]
    con = sqlite3.connect(':memory:')
    con.execute(f'CREATE TABLE {tname} ({cols})')
    res = []
    for s_ in stmts:
        try:
            con.execute(s_)
            res.append('succeeds')
        except sqlite3.IntegrityError as e:
            msg = str(e)
            res.append('fails (' + ('NOT NULL' if 'NOT NULL' in msg else 'UNIQUE / primary key' if 'UNIQUE' in msg else 'CHECK') + ' constraint)')
    con.close()
    cnt = sum(1 for r_ in res if r_ == 'succeeds')
    ans = '; '.join(f'{i + 1}: {r_}' for i, r_ in enumerate(res)) + f'. Rows stored: {cnt}.'
    body = '\n'.join(f'{i + 1}. {s_}' for i, s_ in enumerate(stmts))
    return dict(stem=f'The table is created with:\nCREATE TABLE {tname} ({cols});\nThe following statements are executed in order (each on its own):\n{body}\nState which statements succeed and which fail, giving the reason for each failure.',
                answer=ans, markingKey=ans + ' 1 mark per correct outcome with reason.', marks=n)


R.facts('ch02-st3', F(
    terms=[('validation', 'automatic checking by a program or DBMS that input data is sensible and obeys defined rules before it is accepted'),
           ('range check', 'a validation rule that a value lies between a lower and an upper limit'),
           ('presence check', 'a validation rule that a required field is not left empty (NOT NULL)'),
           ('format check', 'a validation rule that data matches a required pattern, such as two letters followed by four digits'),
           ('constraint', 'a rule defined in the database schema, such as NOT NULL, UNIQUE, CHECK or FOREIGN KEY, that the DBMS enforces on every change'),
           ('lookup check', 'a validation rule that a value is one of a fixed list of allowed values')],
    why=[('Explain why validation rules should be enforced by the DBMS as well as by the user interface.', 'Data can reach the database through many routes (other apps, imports, SQL scripts); constraints in the schema guarantee every route obeys the rules, while UI checks give users fast feedback.'),
         ('Explain why boundary values must be included in test data for a range check.', 'Off-by-one errors (using < instead of ≤) are common; testing values at and just beyond each limit shows whether the boundaries are accepted and rejected correctly.'),
         ('Explain why a UNIQUE constraint might be added to a field that is not the primary key.', 'Some non-key attributes, such as email or passport number, must still not repeat (they are alternate keys); UNIQUE enforces this while a surrogate key remains the primary key.')],
    contrast=[('a CHECK constraint', 'a NOT NULL constraint', 'CHECK requires values to satisfy a condition (e.g. Price > 0); NOT NULL only requires that a value is present.'),
              ('normal test data', 'erroneous test data', 'Normal data are typical valid values that should be accepted; erroneous data are invalid values (wrong type or out of range) that should be rejected.'),
              ('a range check', 'a type check', 'A range check tests that a value lies between limits; a type check tests that the value is of the correct data type (e.g. an integer, not text).')],
    misc=[('A presence check makes sure that the data entered is correct.', 'A presence check only ensures something has been entered; the value could still be wrong or invalid.'),
          ('A value of 100 should be rejected by a range check of 0 to 100.', 'For an inclusive range 0–100 the boundary value 100 is valid and must be accepted.'),
          ('Constraints slow down a database so they should be removed.', 'Constraints have a small cost but prevent invalid data entering; removing them risks inconsistent data, which is far more costly.')],
    evaluate=[('Validation in the application is sufficient; database constraints are unnecessary.', ['application checks give immediate user feedback', 'fewer schema changes are needed'], ['other applications, scripts and imports bypass application checks', 'constraints are enforced centrally and consistently', 'they document the rules in the schema'], 'Both layers are needed: UI validation for usability and DBMS constraints as the final guarantee of integrity.')],
))
ar('ch02-st3', [
    ('A range check of 1 to 10 should accept 10.', 'An inclusive range includes its boundary values.', 0, 'Both true; inclusivity explains why 10 is accepted.'),
    ('A format check can be implemented with a regular expression.', 'A regular expression describes a pattern of characters.', 0, 'Both true; R explains A.'),
    ('Validation can detect a correctly formatted but wrong telephone number.', 'Verification compares the data with its source.', 3, 'A is false – only verification can catch this; R is true.'),
])


_SCHEMA_STMTS = [
    ('An ERD agreed with the client showing that a Customer places many Orders, with no data types.', 'conceptual'),
    ('A list of the main entities (Patient, Doctor, Appointment) and how they relate, produced in a meeting with users.', 'conceptual'),
    ('Identifying that the business needs to store data about suppliers and deliveries.', 'conceptual'),
    ('Customer(CustomerID PK, Name, Email) and Order(OrderID PK, CustomerID FK, OrderDate), normalised to 3NF.', 'logical'),
    ('Deciding that the many-to-many relationship between Student and Club is resolved by a Membership table.', 'logical'),
    ('Specifying all attributes, primary keys and foreign keys without reference to a particular DBMS product.', 'logical'),
    ('CustomerID INT AUTO_INCREMENT, Email VARCHAR(255) stored using the InnoDB engine in MySQL.', 'physical'),
    ('Creating an index on Order.OrderDate to speed up monthly reports.', 'physical'),
    ('Partitioning the Readings table by year and storing it on SSDs.', 'physical'),
    ('Choosing DECIMAL(10,2) for prices and setting the database\'s character encoding to UTF-8.', 'physical'),
]


@R.add('ch02-st4', 'C3', (1, 4), 'short')
def schema_classify(rng, slot):
    k = 2 if slot.d <= 2 else 3 if slot.d == 3 else 4
    its = rng.sample(_SCHEMA_STMTS, k)
    ans = '; '.join(f'{i + 1}: {lvl}' for i, (_, lvl) in enumerate(its))
    return dict(stem='Classify each design decision as belonging to the conceptual, logical or physical schema.\n' + '\n'.join(f'{i + 1}. {s}' for i, (s, _) in enumerate(its)),
                answer=ans, markingKey=ans + '. Conceptual = what data/entities and relationships; logical = tables, attributes and keys independent of DBMS; physical = DBMS-specific storage, types and indexes. 1 mark each.', marks=k)


@R.add('ch02-st4', 'C1', (1, 3), 'mcq')
def schema_mcq(rng, slot):
    s, lvl = rng.choice(_SCHEMA_STMTS)
    wr = [x for x in ['conceptual schema', 'logical schema', 'physical schema', 'external schema (user view)'] if x != f'{lvl} schema']
    return mcq(rng, f'"{s}" This decision belongs to which level of design?', f'{lvl} schema', wr, f'It is part of the {lvl} schema.')


R.facts('ch02-st4', F(
    terms=[('schema', 'the formal description of a database\'s structure: its tables, fields, data types, keys, relationships and constraints'),
           ('conceptual schema', 'a high-level model of the entities, attributes and relationships the organisation needs, independent of any technology'),
           ('logical schema', 'the detailed design of tables, attributes, keys and relationships in a particular data model (e.g. relational) but independent of a specific DBMS'),
           ('physical schema', 'how the data is actually stored by a specific DBMS: data types, indexes, files, partitions and storage devices'),
           ('external schema (view)', 'the part of the database seen by a particular user or application'),
           ('data independence', 'the ability to change one level of the schema without having to change the levels above it')],
    why=[('Explain why separating the logical and physical schemas is useful.', 'The physical storage (indexes, partitions, hardware) can be changed for performance without changing the tables that programs use (physical data independence), so applications do not need rewriting.'),
         ('Explain why the conceptual schema is developed with end users.', 'Users know the business rules (what data exists and how entities relate); agreeing the conceptual model with them before technical design ensures the database meets real requirements.'),
         ('Explain why a data dictionary is important when a team maintains a database.', 'It records the schema (field names, types, constraints, relationships, meanings), so developers use data consistently and can understand the effect of changes.')],
    contrast=[('the logical schema', 'the physical schema', 'The logical schema defines tables, attributes and keys independently of any DBMS; the physical schema specifies how a particular DBMS stores them (types, indexes, files).'),
              ('the conceptual schema', 'an external schema', 'The conceptual schema models the whole organisation\'s data; an external schema is one user group\'s view of part of it.'),
              ('a schema', 'an instance (state) of the database', 'The schema is the structure, which rarely changes; an instance is the actual data stored at a moment in time, which changes constantly.')],
    misc=[('The physical schema is designed first, because the hardware must be bought before anything else.', 'Design proceeds from conceptual to logical to physical; hardware and storage choices depend on the agreed data requirements.'),
          ('Adding an index changes the logical schema.', 'An index is a physical storage structure; the tables and attributes (logical schema) are unchanged.'),
          ('Each user of a database sees the whole conceptual schema.', 'Users normally see an external schema (view) restricted to what they need and are allowed to access.')],
    evaluate=[('A three-level schema architecture adds unnecessary complexity for small projects.', ['small teams may design and implement in one step', 'fewer documents to maintain'], ['data independence still makes later changes cheaper', 'views give security by restricting access', 'separating levels clarifies design decisions'], 'Even small projects benefit from at least a clear logical design and views; the full formality can be scaled to the project size.')],
    apply=[('A sports club in Vienna wants coaches to see only their own squad\'s training records. Explain which schema level provides this and how.', 'The external level: create a view (e.g. CREATE VIEW SquadA AS SELECT … WHERE Squad = \'A\') for each coach and grant access to the view rather than the base tables.', 3)],
))
ar('ch02-st4', [
    ('Creating an index on a column changes the physical schema.', 'An index alters how data is stored and accessed but not the logical tables.', 0, 'Both true; R explains A.'),
    ('The logical schema depends on the DBMS product chosen.', 'Data types such as VARCHAR(255) are DBMS-specific.', 3, 'A is false (logical is DBMS-independent); R is true, which is why types belong to the physical schema.'),
])


# =============================================================================================
# ch03 A3.3 Database programming (SQL)  – every result below is produced by sqlite3
# =============================================================================================
def _ds_students(rng, n):
    houses = rng.sample(['Rhine', 'Rhone', 'Aare', 'Inn'], 3)
    names = rng.sample(PEOPLE, n)
    rows = [(i + 1, names[i], rng.choice(houses), rng.choice([11, 12]), rng.randint(40, 99)) for i in range(n)]
    return dict(name='Student', ctx='an international school in Geneva', cols=['StudentID', 'Name', 'House', 'Year', 'Score'],
                types=['INTEGER PRIMARY KEY', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER'], rows=rows,
                num='Score', cat='House', txt='Name', key='StudentID', catvals=houses, noun='students')


def _ds_products(rng, n):
    cats = rng.sample(['Stationery', 'Electronics', 'Kitchen', 'Garden', 'Toys'], 3)
    items = rng.sample(['Pen', 'Lamp', 'Kettle', 'Hose', 'Kite', 'Ruler', 'Router', 'Wok', 'Shovel', 'Puzzle', 'Stapler', 'Charger'], n)
    rows = [(100 + i, items[i], rng.choice(cats), rng.choice([2, 4, 5, 8, 12, 15, 20, 25, 30, 45]), rng.randint(0, 60)) for i in range(n)]
    return dict(name='Product', ctx='a hardware store in Nairobi', cols=['ProductID', 'Name', 'Category', 'Price', 'Stock'],
                types=['INTEGER PRIMARY KEY', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER'], rows=rows,
                num='Price', cat='Category', txt='Name', key='ProductID', catvals=cats, noun='products')


def _ds_flights(rng, n):
    hubs = rng.sample(['SIN', 'DXB', 'LIS', 'NBO', 'LIM'], 3)
    dests = ['OSL', 'YYZ', 'MEL', 'ACC', 'HAN', 'BOG', 'VIE', 'SEL', 'MEX', 'GVA', 'KUL', 'CPT']
    rows = [(f'XY{200 + 7 * i}', rng.choice(hubs), rng.choice(dests), rng.randint(2, 14), rng.choice([120, 150, 180, 220, 300])) for i in range(n)]
    return dict(name='Flight', ctx='an airline', cols=['FlightNo', 'Origin', 'Dest', 'Hours', 'Seats'],
                types=['TEXT PRIMARY KEY', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER'], rows=rows,
                num='Hours', cat='Origin', txt='Dest', key='FlightNo', catvals=hubs, noun='flights')


def _ds_books(rng, n):
    genres = rng.sample(['Fantasy', 'History', 'Science', 'Poetry', 'Crime'], 3)
    titles = rng.sample(['Dune Sea', 'Atlas', 'Orbit', 'Ember', 'Fjord', 'Baobab', 'Monsoon', 'Quipu', 'Andes', 'Lagoon', 'Kilimanjaro', 'Aurora'], n)
    rows = [(i + 1, titles[i], rng.choice(genres), rng.randint(120, 640), rng.randint(1995, 2025)) for i in range(n)]
    return dict(name='Book', ctx='a public library in Oslo', cols=['BookID', 'Title', 'Genre', 'Pages', 'PubYear'],
                types=['INTEGER PRIMARY KEY', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER'], rows=rows,
                num='Pages', cat='Genre', txt='Title', key='BookID', catvals=genres, noun='books')


def _present(f):
    def g(rng, n):
        ds = f(rng, n)
        i = ds['cols'].index(ds['cat'])
        present = sorted({r[i] for r in ds['rows']})
        if len(present) < 2:
            ds['rows'][0] = tuple(v if j != i else next(c for c in ds['catvals'] if c != present[0]) for j, v in enumerate(ds['rows'][0]))
            present = sorted({r[i] for r in ds['rows']})
        ds['catvals'] = present
        return ds
    return g


_DS = [_present(f) for f in (_ds_students, _ds_products, _ds_flights, _ds_books)]


def _setup(ds):
    cols = ', '.join(f'{c} {t}' for c, t in zip(ds['cols'], ds['types']))
    ph = ', '.join('?' * len(ds['cols']))
    return [f'CREATE TABLE {ds["name"]} ({cols})', (f'INSERT INTO {ds["name"]} VALUES ({ph})', ds['rows'])]


def _q_templates(rng, ds):
    t, num, cat, txt, key = ds['name'], ds['num'], ds['cat'], ds['txt'], ds['key']
    vals = sorted(r[ds['cols'].index(num)] for r in ds['rows'])
    thr = vals[len(vals) // 2]
    cv = rng.choice(ds['catvals'])
    cv2 = rng.choice([c for c in ds['catvals'] if c != cv])
    k = rng.randint(2, 3)
    lo, hi = vals[1], vals[-2]
    letter = rng.choice([r[ds['cols'].index(txt)][0] for r in ds['rows']])
    n_ = ds['noun']
    return [
        (1, f"SELECT {txt}, {num} FROM {t} WHERE {num} > {thr} ORDER BY {num} DESC, {txt};", f'the {txt} and {num} of all {n_} with {num} greater than {thr}, highest {num} first (ties in alphabetical order of {txt})'),
        (1, f"SELECT {txt} FROM {t} WHERE {cat} = '{cv}' ORDER BY {txt};", f'the {txt} of every {n_[:-1]} whose {cat} is {cv}, in alphabetical order'),
        (2, f"SELECT COUNT(*) FROM {t} WHERE {cat} = '{cv}' AND {num} >= {thr};", f'how many {n_} have {cat} {cv} and {num} of at least {thr}'),
        (2, f"SELECT {txt}, {cat} FROM {t} WHERE {cat} = '{cv}' OR {num} < {lo + 1} ORDER BY {key};", f'the {txt} and {cat} of {n_} that either have {cat} {cv} or a {num} below {lo + 1}, in {key} order'),
        (2, f"SELECT MAX({num}), MIN({num}) FROM {t} WHERE {cat} <> '{cv}';", f'the largest and smallest {num} of {n_} whose {cat} is not {cv}'),
        (2, f"SELECT {txt} FROM {t} WHERE {num} BETWEEN {lo} AND {hi} AND {cat} IN ('{cv}', '{cv2}') ORDER BY {num}, {txt};", f'the {txt} of {n_} with {num} from {lo} to {hi} inclusive and {cat} {cv} or {cv2}, ordered by {num} then {txt}'),
        (2, f"SELECT {txt} FROM {t} WHERE {txt} LIKE '{letter}%' ORDER BY {txt};", f'the {txt} of every {n_[:-1]} whose {txt} starts with {letter}, alphabetically'),
        (3, f"SELECT {cat}, COUNT(*) FROM {t} GROUP BY {cat} ORDER BY {cat};", f'the number of {n_} in each {cat}, sorted by {cat}'),
        (3, f"SELECT {cat}, ROUND(AVG({num}), 1) FROM {t} GROUP BY {cat} ORDER BY {cat};", f'the average {num} (to 1 decimal place) for each {cat}, sorted by {cat}'),
        (3, f"SELECT {cat}, SUM({num}) FROM {t} GROUP BY {cat} HAVING COUNT(*) >= 2 ORDER BY SUM({num}) DESC, {cat};", f'the total {num} for each {cat} that contains at least two {n_}, largest total first'),
        (3, f"SELECT {txt}, {num} FROM {t} ORDER BY {num} DESC, {txt} ASC LIMIT {k};", f'the {txt} and {num} of the {k} {n_} with the highest {num} (ties broken alphabetically by {txt})'),
        (4, f"SELECT {txt} FROM {t} WHERE {num} > (SELECT AVG({num}) FROM {t}) ORDER BY {txt};", f'the {txt} of {n_} whose {num} is above the average {num} of all {n_}, alphabetically'),
        (4, f"SELECT {cat}, MAX({num}) - MIN({num}) FROM {t} GROUP BY {cat} HAVING MAX({num}) - MIN({num}) > 0 ORDER BY {cat};", f'for each {cat} with more than one distinct {num}, the range (max − min) of {num}, sorted by {cat}'),
        (4, f"SELECT COUNT(DISTINCT {cat}) FROM {t} WHERE {num} >= {thr};", f'how many different {cat} values occur among {n_} with {num} at least {thr}'),
    ]


def _sql_pick(rng, slot):
    ds = rng.choice(_DS)(rng, 6 if slot.d <= 2 else 7 if slot.d <= 3 else 8)
    qs = [q for q in _q_templates(rng, ds) if q[0] <= max(1, slot.d) and q[0] >= slot.d - 2]
    lvl, sql, eng = rng.choice(qs)
    cols, res = sql_run(_setup(ds), sql)
    return ds, sql, eng, cols, res


@R.add('ch03-st2', 'C3', (1, 5), 'short')
def sql_output(rng, slot):
    ds, sql, eng, cols, res = _sql_pick(rng, slot)
    tb = table(ds['cols'], ds['rows'])
    ans = fmt_rows(res)
    return dict(stem=f'The table {ds["name"]} at {ds["ctx"]} contains:\n{tb}\nState the result of the query:\n{sql}',
                answer=ans, markingKey=f'Result rows (in order): {ans}. A1 for correct rows, A1 for correct order/columns' + (' (aggregate correctly grouped).' if 'GROUP' in sql else '.'),
                marks=2 if slot.d <= 2 else 3)


@R.add('ch03-st2', 'C3', (2, 5), 'short')
def sql_write(rng, slot):
    ds, sql, eng, cols, res = _sql_pick(rng, slot)
    sch = f'{ds["name"]}(' + ', '.join(ds['cols']) + ')'
    tb = table(ds['cols'], ds['rows'])
    show = f' Sample data:\n{tb}\n' if slot.d >= 3 else ' '
    ans = f'{sql}  → returns {fmt_rows(res)}' if slot.d >= 3 else sql
    return dict(stem=f'A database for {ds["ctx"]} contains the table {sch}.{show}Write an SQL query to return {eng}.',
                answer=ans, markingKey=f'Model answer: {sql} (equivalent correct SQL accepted). On the sample data it returns {fmt_rows(res)}. Marks: correct SELECT list; correct FROM/WHERE condition; correct GROUP BY/HAVING/ORDER BY as required.',
                marks=2 if slot.d <= 2 else 3 if slot.d == 3 else 4)


def _ds_join(rng, slot):
    city = rng.sample(['Lima', 'Oslo', 'Hanoi', 'Accra', 'Lisbon', 'Seoul'], 3)
    names = rng.sample(PEOPLE, 5)
    cust = [(i + 1, names[i], rng.choice(city)) for i in range(5)]
    orders = []
    oid = 500
    for c in cust:
        for _ in range(rng.choice([0, 1, 1, 2, 3])):
            oid += 1
            orders.append((oid, c[0], rng.choice([15, 20, 35, 40, 60, 75, 90, 120])))
    if len(orders) < 3:
        return None
    setup = ['CREATE TABLE Customer (CustomerID INTEGER PRIMARY KEY, Name TEXT, City TEXT)',
             'CREATE TABLE Orders (OrderID INTEGER PRIMARY KEY, CustomerID INTEGER REFERENCES Customer(CustomerID), Amount INTEGER)',
             ('INSERT INTO Customer VALUES (?, ?, ?)', cust), ('INSERT INTO Orders VALUES (?, ?, ?)', orders)]
    c1 = rng.choice(city)
    a = rng.choice([30, 40, 50, 60])
    qs = [
        (2, f"SELECT Customer.Name, Orders.Amount FROM Customer INNER JOIN Orders ON Customer.CustomerID = Orders.CustomerID WHERE Orders.Amount > {a} ORDER BY Orders.Amount DESC, Customer.Name;", f'each order over {a} with the customer\'s name, largest first'),
        (3, f"SELECT Customer.Name, COUNT(Orders.OrderID) FROM Customer INNER JOIN Orders ON Customer.CustomerID = Orders.CustomerID GROUP BY Customer.CustomerID, Customer.Name ORDER BY Customer.Name;", 'the name of every customer who has placed an order, with their number of orders, alphabetically'),
        (3, f"SELECT Customer.City, SUM(Orders.Amount) FROM Customer INNER JOIN Orders ON Customer.CustomerID = Orders.CustomerID GROUP BY Customer.City ORDER BY SUM(Orders.Amount) DESC, Customer.City;", 'the total value of orders from each city, highest first'),
        (4, f"SELECT Customer.Name FROM Customer LEFT JOIN Orders ON Customer.CustomerID = Orders.CustomerID WHERE Orders.OrderID IS NULL ORDER BY Customer.Name;", 'the names of customers who have never placed an order'),
        (4, f"SELECT Customer.Name, SUM(Orders.Amount) FROM Customer INNER JOIN Orders ON Customer.CustomerID = Orders.CustomerID WHERE Customer.City = '{c1}' GROUP BY Customer.CustomerID, Customer.Name HAVING SUM(Orders.Amount) >= {a} ORDER BY Customer.Name;", f'the name and total spending of customers in {c1} whose orders total at least {a}'),
    ]
    qs = [q for q in qs if q[0] <= slot.d]
    lvl, sql, eng = rng.choice(qs)
    cols, res = sql_run(setup, sql)
    return cust, orders, sql, eng, res


@R.add('ch03-st2', 'C3', (2, 5), 'short')
def sql_join(rng, slot):
    j = _ds_join(rng, slot)
    if not j:
        return None
    cust, orders, sql, eng, res = j
    t1 = table(['CustomerID', 'Name', 'City'], cust)
    t2 = table(['OrderID', 'CustomerID', 'Amount'], orders)
    if rng.random() < 0.5:
        return dict(stem=f'An online marketplace stores:\nCustomer\n{t1}\nOrders\n{t2}\nState the output of:\n{sql}', answer=fmt_rows(res),
                    markingKey=f'Rows: {fmt_rows(res)}. M1 matching rows on CustomerID; A1 correct filtering/grouping; A1 order.', marks=3)
    return dict(stem=f'An online marketplace stores:\nCustomer\n{t1}\nOrders\n{t2}\nWrite an SQL query to list {eng}, and state the rows it returns.', answer=f'{sql} → {fmt_rows(res)}',
                markingKey=f'Model answer: {sql} (equivalent SQL accepted). Join condition (1), filter/grouping (1-2), ordering (1), correct result {fmt_rows(res)} (1).', marks=4 if slot.d >= 4 else 3)


_SQL_ERRORS = [
    ("SELECT Name, Score FROM Student WHERE AVG(Score) > 70;", 'An aggregate function cannot be used in WHERE; use GROUP BY with HAVING, or compare with a subquery: WHERE Score > (SELECT AVG(Score) FROM Student).'),
    ("SELECT House, COUNT(*) FROM Student;", 'House is selected alongside an aggregate without GROUP BY; add GROUP BY House.'),
    ("SELECT * FROM Product WHERE Category = Kitchen;", 'The text value must be in quotes: Category = \'Kitchen\'.'),
    ("SELECT Title FROM Book WHERE PubYear = NULL;", 'Comparison with NULL using = is never true; use PubYear IS NULL.'),
    ("SELECT Name, Price FROM Product ORDER Price DESC;", 'The clause is ORDER BY Price DESC; the keyword BY is missing.'),
    ("SELECT Name Price FROM Product;", 'A comma is missing between the column names (Name Price is read as Name aliased as Price).'),
    ("SELECT Dest FROM Flight WHERE Hours > 5 AND < 10;", 'Each condition needs its own column: Hours > 5 AND Hours < 10 (or Hours BETWEEN 6 AND 9).'),
    ("SELECT Customer.Name, Orders.Amount FROM Customer, Orders;", 'There is no join condition, so every customer is paired with every order (Cartesian product); add WHERE/ON Customer.CustomerID = Orders.CustomerID.'),
    ("SELECT Genre, COUNT(*) FROM Book GROUP BY Genre WHERE COUNT(*) > 2;", 'WHERE cannot follow GROUP BY or filter groups; use HAVING COUNT(*) > 2.'),
    ("UPDATE Product SET Price = Price * 1.1;", 'Not a syntax error but a logic error: without a WHERE clause every product\'s price is increased.'),
    ("DELETE Student WHERE Year = 12;", 'The syntax is DELETE FROM Student WHERE Year = 12; FROM is missing.'),
    ("INSERT INTO Student VALUES ('Hana', 12, 88);", 'The number of values does not match the table\'s five columns; list the columns: INSERT INTO Student (Name, Year, Score) VALUES (…) or supply all values.'),
]


@R.add('ch03-st2', 'C2', (2, 4), 'explain')
def sql_error(rng, slot):
    k = 1 if slot.d <= 3 else 2
    its = rng.sample(_SQL_ERRORS, k)
    if k == 1:
        q, fix = its[0]
        return dict(stem=f'A student writes the SQL statement below. Identify the error and write a corrected version.\n{q}', answer=fix,
                    markingKey=f'{fix} 1 mark for identifying the error, 1 mark for a correct corrected statement.', type='explain', marks=2, gap='G2')
    return dict(stem='Each SQL statement below contains an error. For each one, identify the error and correct it.\n' + '\n'.join(f'{i + 1}. {q}' for i, (q, _) in enumerate(its)),
                answer=' '.join(f'{i + 1}. {f_}' for i, (_, f_) in enumerate(its)), markingKey=' '.join(f'{i + 1}. {f_}' for i, (_, f_) in enumerate(its)) + ' 2 marks each.', type='explain', marks=4, gap='G2')


R.facts('ch03-st2', F(
    terms=[('query', 'a request for data from a database, written in SQL as a SELECT statement'),
           ('aggregate function', 'an SQL function such as COUNT, SUM, AVG, MIN or MAX that returns one value calculated from a set of rows'),
           ('inner join', 'a join that returns only the rows where the join condition matches in both tables'),
           ('left (outer) join', 'a join that returns every row of the left table, with NULLs where there is no matching row in the right table'),
           ('GROUP BY', 'the SQL clause that collects rows with the same value(s) so that aggregate functions are calculated per group'),
           ('HAVING', 'the SQL clause that filters groups after GROUP BY, using conditions on aggregates')],
    why=[('Explain why HAVING is needed in addition to WHERE.', 'WHERE filters individual rows before grouping and cannot use aggregates; HAVING filters the groups produced by GROUP BY using aggregate values such as COUNT(*) > 2.'),
         ('Explain why a join without a join condition produces too many rows.', 'Without a condition every row of one table is paired with every row of the other (a Cartesian product of m × n rows) instead of only related rows.'),
         ('Explain why NULL must be tested with IS NULL rather than = NULL.', 'NULL means unknown; any comparison with NULL using = gives unknown (not true), so no rows match; IS NULL is the specific test for missing values.'),
         ('Explain why COUNT(column) may give a different answer from COUNT(*).', 'COUNT(*) counts all rows; COUNT(column) counts only rows where that column is not NULL.')],
    contrast=[('WHERE', 'HAVING', 'WHERE filters rows before grouping and cannot contain aggregates; HAVING filters groups after GROUP BY and may use aggregates.'),
              ('an inner join', 'a left join', 'An inner join keeps only matching rows from both tables; a left join keeps every row of the left table, filling unmatched columns with NULL.'),
              ('ORDER BY', 'GROUP BY', 'ORDER BY only sorts the result rows; GROUP BY combines rows with equal values into one row per group for aggregation.')],
    misc=[('ORDER BY Score DESC LIMIT 1 and MAX(Score) always give the same output.', 'MAX(Score) returns only the highest value (one column); ORDER BY … LIMIT 1 returns a whole row and, with ties, only one of the tied rows.'),
          ('SELECT DISTINCT removes duplicate rows from the table.', 'DISTINCT removes duplicate rows only from the query result; the stored table is unchanged.'),
          ('AVG(Score) counts NULL scores as zero.', 'Aggregate functions ignore NULLs, so AVG divides by the number of non-NULL scores only.')],
    evaluate=[('Using SQL queries is always better than exporting data to a spreadsheet for analysis.', ['SQL works on the live, consistent data and scales to millions of rows', 'queries can be saved, repeated and secured'], ['spreadsheets are easier for non-specialists and good for charts', 'one-off small analyses may be faster in a spreadsheet'], 'For repeatable or large-scale analysis SQL is superior; spreadsheets suit small, ad-hoc exploration of exported summaries.')],
))
ar('ch03-st2', [
    ('SELECT COUNT(*) FROM Student; returns one row.', 'Without GROUP BY an aggregate summarises the whole table.', 0, 'Both true; R explains A.'),
    ('A LEFT JOIN can be used to find customers who have no orders.', 'Unmatched rows of the left table appear with NULLs in the right table\'s columns.', 0, 'Both true; testing Orders.OrderID IS NULL after a LEFT JOIN finds them.'),
    ('A condition such as COUNT(*) > 2 must be placed in HAVING, not in WHERE.', 'WHERE is applied to individual rows before any grouping takes place.', 0, 'Both true; because WHERE runs before grouping, group aggregates are not yet available, which explains A.'),
    ('ORDER BY must appear before WHERE in a SELECT statement.', 'ORDER BY sorts the final result set.', 3, 'A is false (ORDER BY comes last); R is true.'),
])


_DDL_SPECS = [
    ('Volunteer', 'a charity in Mumbai', [('VolunteerID', 'INTEGER', 'primary key'), ('FullName', 'VARCHAR(60)', 'must be present'), ('Email', 'VARCHAR(100)', 'unique'), ('BirthDate', 'DATE', None), ('Hours', 'INTEGER', 'zero or more')]),
    ('Room', 'a hotel in Cape Town', [('RoomNo', 'INTEGER', 'primary key'), ('RoomType', 'VARCHAR(10)', "one of 'single', 'double', 'suite'"), ('Rate', 'DECIMAL(6,2)', 'greater than 0'), ('Floor', 'INTEGER', 'between 0 and 20')]),
    ('Sensor', 'a smart farm near Nairobi', [('SensorID', 'CHAR(6)', 'primary key'), ('FieldName', 'VARCHAR(30)', 'must be present'), ('InstalledOn', 'DATE', None), ('BatteryPct', 'INTEGER', 'between 0 and 100')]),
    ('Athlete', 'a sports academy in Seoul', [('AthleteID', 'INTEGER', 'primary key'), ('Name', 'VARCHAR(50)', 'must be present'), ('Sport', 'VARCHAR(20)', None), ('Age', 'INTEGER', 'between 12 and 40'), ('Coach', 'INTEGER', 'foreign key to Coach(CoachID)')]),
    ('Loan', 'a library in Vienna', [('LoanID', 'INTEGER', 'primary key'), ('MemberID', 'INTEGER', 'foreign key to Member(MemberID)'), ('BookID', 'INTEGER', 'foreign key to Book(BookID)'), ('LoanDate', 'DATE', 'must be present'), ('Returned', 'BOOLEAN', None)]),
]


def _col_sql(c, t, rule):
    s = f'{c} {t}'
    if not rule:
        return s
    if rule == 'primary key':
        return s + ' PRIMARY KEY'
    if rule == 'must be present':
        return s + ' NOT NULL'
    if rule == 'unique':
        return s + ' UNIQUE'
    if rule == 'zero or more':
        return s + f' CHECK ({c} >= 0)'
    if rule == 'greater than 0':
        return s + f' CHECK ({c} > 0)'
    if rule.startswith('between'):
        a, b = rule.split()[1], rule.split()[3]
        return s + f' CHECK ({c} BETWEEN {a} AND {b})'
    if rule.startswith('one of'):
        return s + f' CHECK ({c} IN ({rule[7:]}))'
    if rule.startswith('foreign key'):
        return s + ' REFERENCES ' + rule.split('to ')[1]
    return s


@R.add('ch03-st1', 'C3', (2, 5), 'short')
def ddl_create(rng, slot):
    tname, ctx, cols = rng.choice(_DDL_SPECS)
    k = len(cols) if slot.d >= 4 else min(len(cols), 4)
    cols = cols[:k]
    spec = '; '.join(f'{c} ({t}' + (f', {r}' if r else '') + ')' for c, t, r in cols)
    sql = f'CREATE TABLE {tname} (\n  ' + ',\n  '.join(_col_sql(*c) for c in cols) + '\n);'
    con = sqlite3.connect(':memory:')
    con.execute('CREATE TABLE Coach (CoachID INTEGER PRIMARY KEY)')
    con.execute('CREATE TABLE Member (MemberID INTEGER PRIMARY KEY)')
    con.execute('CREATE TABLE Book (BookID INTEGER PRIMARY KEY)')
    con.execute(sql)
    con.close()
    return dict(stem=f'Write the SQL statement to create a table {tname} for {ctx} with these fields and rules: {spec}.',
                answer=sql, markingKey=f'Model answer:\n{sql}\n1 mark for CREATE TABLE with correct name and brackets; 1 mark for correct data types; 1 mark per correctly expressed constraint (PRIMARY KEY, NOT NULL, UNIQUE, CHECK, REFERENCES), max {k}.', marks=k)


@R.add('ch03-st1', 'C3', (2, 5), 'short')
def ddl_alter(rng, slot):
    tname, ctx, cols = rng.choice(_DDL_SPECS)
    con = sqlite3.connect(':memory:')
    for p_ in ('Coach (CoachID INTEGER PRIMARY KEY)', 'Member (MemberID INTEGER PRIMARY KEY)', 'Book (BookID INTEGER PRIMARY KEY)'):
        con.execute('CREATE TABLE ' + p_)
    con.execute(f'CREATE TABLE {tname} (' + ', '.join(f'{c} {t}' + (' PRIMARY KEY' if r == 'primary key' else '') for c, t, r in cols) + ')')
    current = [c for c, _, _ in cols]
    ops = []
    n_ops = 2 if slot.d <= 3 else 3
    adds = [('Notes', 'VARCHAR(200)'), ('Phone', 'VARCHAR(20)'), ('Rating', 'INTEGER'), ('UpdatedAt', 'DATETIME'), ('Country', 'CHAR(2)')]
    rng.shuffle(adds)
    for _ in range(n_ops):
        kind = rng.choice(['add', 'drop', 'rename'])
        non_pk = [c for c in current if c != cols[0][0]]
        if kind == 'add' or not non_pk:
            a, t = adds.pop()
            ops.append(f'ALTER TABLE {tname} ADD COLUMN {a} {t};')
            current.append(a)
        elif kind == 'drop':
            c = rng.choice(non_pk)
            ops.append(f'ALTER TABLE {tname} DROP COLUMN {c};')
            current.remove(c)
        else:
            c = rng.choice(non_pk)
            nn = c + rng.choice(['Old', '2', 'Txt'])
            ops.append(f'ALTER TABLE {tname} RENAME COLUMN {c} TO {nn};')
            current[current.index(c)] = nn
    for o in ops:
        con.execute(o)
    real = [r[1] for r in con.execute(f'PRAGMA table_info({tname})')]
    con.close()
    assert real == current, (real, current)
    ans = ', '.join(real)
    return dict(stem=f'The table {tname} has the columns {", ".join(c for c, _, _ in cols)}. The following statements are executed in order:\n' + '\n'.join(ops) + f'\nList the columns of {tname} afterwards, in order.',
                answer=ans, markingKey=f'Columns: {ans}. ADD COLUMN appends at the end; DROP removes; RENAME keeps the position. 1 mark per correctly applied statement.', marks=n_ops)


_DDL_ERR = [
    ('CREATE TABLE Pupil (PupilID INTEGER PRIMARY KEY, Name VARCHAR(40) NOT NULL Age INTEGER);', 'A comma is missing between the Name and Age column definitions.'),
    ('CREATE TABLE Order (OrderID INTEGER PRIMARY KEY, Total DECIMAL(8,2));', 'ORDER is a reserved word; rename the table (e.g. Orders) or quote the identifier.'),
    ('CREATE TABLE Booking (BookingID INTEGER PRIMARY KEY, RoomNo INTEGER REFERENCES Room, Nights INTEGER CHECK Nights > 0);', 'The CHECK condition must be in brackets: CHECK (Nights > 0).'),
    ('ALTER TABLE Staff ADD Salary;', 'The new column needs a data type, e.g. ALTER TABLE Staff ADD Salary DECIMAL(9,2);'),
    ('DROP Staff;', 'The statement must say what is dropped: DROP TABLE Staff;'),
    ('CREATE TABLE Match (MatchID INTEGER PRIMARY KEY, HomeTeam INTEGER FOREIGN KEY Team(TeamID));', 'Column-level foreign keys use REFERENCES: HomeTeam INTEGER REFERENCES Team(TeamID) (or a table-level FOREIGN KEY (HomeTeam) REFERENCES Team(TeamID)).'),
    ('CREATE TABLE Item (ItemID INTEGER PRIMARY KEY, Name VARCHAR(40) NOT NULL, Price DECIMAL(6,2) DEFAULT 0, PRIMARY KEY (Name));', 'A table can have only one primary key; ItemID is already declared PRIMARY KEY, so the second PRIMARY KEY clause is an error.'),
]


@R.add('ch03-st1', 'C2', (2, 4), 'explain')
def ddl_error(rng, slot):
    q, fix = rng.choice(_DDL_ERR)
    frame = rng.choice(['Identify the error in this SQL statement and correct it.', 'This statement is rejected by the DBMS. Explain why and give a corrected version.'])
    return dict(stem=f'{frame}\n{q}', answer=fix, markingKey=f'{fix} 1 mark for the error, 1 mark for a correct fix.', type='explain', marks=2, gap='G2')


R.facts('ch03-st1', F(
    terms=[('data definition language (DDL)', 'the part of SQL used to define and change the structure of a database, using CREATE, ALTER and DROP'),
           ('CREATE TABLE', 'the DDL statement that defines a new table with its columns, data types and constraints'),
           ('ALTER TABLE', 'the DDL statement that changes an existing table, for example adding, dropping or renaming a column or constraint'),
           ('DROP TABLE', 'the DDL statement that permanently removes a table, its structure and all its data'),
           ('data manipulation language (DML)', 'the part of SQL used to query and change the data in tables, using SELECT, INSERT, UPDATE and DELETE'),
           ('index', 'a separate data structure (often a B-tree) that lets the DBMS find rows by a column value without scanning the whole table')],
    facts=[('Which SQL statement permanently removes a table and all of its data?', 'DROP TABLE', ['DELETE FROM', 'ALTER TABLE … DROP COLUMN', 'TRUNCATE COLUMN'], 'DROP removes the structure and data.'),
           ('Which statement adds a column Phone to a table Staff?', 'ALTER TABLE Staff ADD Phone VARCHAR(20);', ['UPDATE Staff ADD Phone;', 'INSERT INTO Staff (Phone);', 'CREATE COLUMN Phone IN Staff;'], 'Changing the structure of a table is done with ALTER TABLE.'),
           ('Which of these is a DDL statement?', 'CREATE TABLE', ['SELECT', 'UPDATE', 'INSERT'], 'CREATE defines structure.')],
    why=[('Explain why DROP TABLE should be used with great care in a live database.', 'It removes the table definition and every row immediately and usually cannot be undone without a backup; other tables\' foreign keys and applications that use the table will also break.'),
         ('Explain why constraints are defined in the CREATE TABLE statement rather than checked later by programs.', 'The DBMS then enforces them automatically for every insert or update from any application, guaranteeing integrity centrally and documenting the rules in the schema.'),
         ('Explain why adding an index can speed up SELECT queries but slow down INSERT statements.', 'An index lets the DBMS locate matching rows quickly instead of scanning the table, but every INSERT/UPDATE must also update the index structure, adding work.')],
    contrast=[('DROP TABLE', 'DELETE FROM', 'DROP TABLE removes the table structure and all data; DELETE FROM removes rows (all, or those matching WHERE) but the table remains.'),
              ('DDL', 'DML', 'DDL defines or changes the structure (CREATE, ALTER, DROP); DML queries and changes the data in tables (SELECT, INSERT, UPDATE, DELETE).'),
              ('a column constraint', 'a table constraint', 'A column constraint is written after one column\'s definition (Age INTEGER CHECK (Age > 0)); a table constraint is written separately and can cover several columns (PRIMARY KEY (StudentID, CourseID)).')],
    misc=[('ALTER TABLE is used to change the value stored in a field.', 'ALTER TABLE changes structure; values are changed with UPDATE.'),
          ('A composite primary key is created by writing PRIMARY KEY after each of the two columns.', 'That would declare two primary keys (an error); a composite key is a table constraint: PRIMARY KEY (ColA, ColB).'),
          ('DELETE FROM Student; removes the Student table.', 'It deletes every row but the empty table and its structure remain; DROP TABLE removes the table.')],
    evaluate=[('Database structure changes (ALTER TABLE) should be made directly on the live database whenever a new requirement appears.', ['quick response to user needs', 'no separate test environment to maintain'], ['changes can break applications, queries and foreign keys', 'locks on large tables may stop the service', 'no rollback plan if data is lost'], 'Schema changes should be scripted, tested on a copy, version-controlled and applied in a planned window; direct live changes are only acceptable for trivial, reversible cases.')],
))
ar('ch03-st1', [
    ('CREATE, ALTER and DROP are data definition language statements.', 'They change the structure of the database rather than the data in it.', 0, 'Both true; R explains the classification.'),
    ('ALTER TABLE can add a CHECK constraint to an existing table.', 'ALTER TABLE changes the definition of an existing table.', 0, 'Both true and R explains A.'),
    ('DROP TABLE can be reversed with ROLLBACK in every DBMS.', 'Some DBMSs treat DDL as auto-committing.', 3, 'A is false (in many DBMSs DDL auto-commits); R is true.'),
])


# ---- DML ----
@R.add('ch03-st3', 'C3', (1, 5), 'short')
def dml_seq(rng, slot):
    ds = rng.choice(_DS)(rng, 5 if slot.d <= 2 else 6)
    t, num, cat, txt, key = ds['name'], ds['num'], ds['cat'], ds['txt'], ds['key']
    cv = rng.choice(ds['catvals'])
    vals = sorted(r[ds['cols'].index(num)] for r in ds['rows'])
    thr = vals[len(vals) // 2]
    kv = ds['rows'][rng.randrange(len(ds['rows']))][0]
    kv_s = f"'{kv}'" if isinstance(kv, str) else str(kv)
    newkey = "'XY999'" if isinstance(kv, str) else '999'
    newrow = {'Student': f"({newkey}, 'Ines', '{cv}', 12, 75)", 'Product': f"({newkey}, 'Fan', '{cv}', 18, 7)",
              'Flight': f"({newkey}, '{cv}', 'GVA', 6, 180)", 'Book': f"({newkey}, 'Tundra', '{cv}', 300, 2021)"}[t]
    pool = [
        f"UPDATE {t} SET {num} = {num} + {rng.randint(1, 5)} WHERE {cat} = '{cv}';",
        f"DELETE FROM {t} WHERE {num} < {thr};",
        f"INSERT INTO {t} VALUES {newrow};",
        f"UPDATE {t} SET {cat} = '{rng.choice(ds['catvals'])}' WHERE {key} = {kv_s};",
        f"DELETE FROM {t} WHERE {key} = {kv_s};",
        f"UPDATE {t} SET {num} = {num} * 2 WHERE {num} <= {vals[1]};",
    ]
    k = 1 if slot.d <= 1 else 2 if slot.d <= 3 else 3
    stmts = rng.sample(pool, k)
    final_q = rng.choice([f'SELECT COUNT(*), SUM({num}) FROM {t};', f'SELECT {key}, {num} FROM {t} ORDER BY {key};', f"SELECT {txt} FROM {t} WHERE {cat} = '{cv}' ORDER BY {txt};"])
    res = sql_seq(_setup(ds), stmts, final_q)
    ans = fmt_rows(res)
    return dict(stem=f'The table {t} for {ds["ctx"]} contains:\n{table(ds["cols"], ds["rows"])}\nThe following statements are executed in order:\n' + '\n'.join(stmts) + f'\nState the result of: {final_q}',
                answer=ans, markingKey=f'Apply each statement in turn (M1 per statement correctly applied), then the final query gives {ans} (A1).', marks=k + 1)


@R.add('ch03-st3', 'C3', (2, 4), 'short')
def dml_write(rng, slot):
    ds = rng.choice(_DS)(rng, 6)
    t, num, cat, txt, key = ds['name'], ds['num'], ds['cat'], ds['txt'], ds['key']
    cv = rng.choice(ds['catvals'])
    p = rng.choice([5, 10, 20])
    vals = sorted(r[ds['cols'].index(num)] for r in ds['rows'])
    thr = vals[2]
    tasks = [
        (f'increase the {num} of every {ds["noun"][:-1]} with {cat} {cv} by {p}', f"UPDATE {t} SET {num} = {num} + {p} WHERE {cat} = '{cv}';", f'SELECT COUNT(*) FROM {t} WHERE {cat} = \'{cv}\';', 'rows changed'),
        (f'remove every {ds["noun"][:-1]} whose {num} is below {thr}', f'DELETE FROM {t} WHERE {num} < {thr};', f'SELECT COUNT(*) FROM {t} WHERE {num} < {thr};', 'rows deleted'),
        (f'move every {ds["noun"][:-1]} with {cat} {cv} and {num} of at least {thr} into {cat} \'Archive\'', f"UPDATE {t} SET {cat} = 'Archive' WHERE {cat} = '{cv}' AND {num} >= {thr};", f"SELECT COUNT(*) FROM {t} WHERE {cat} = '{cv}' AND {num} >= {thr};", 'rows changed'),
    ]
    desc, sql, cnt_q, what = rng.choice(tasks)
    _, res = sql_run(_setup(ds), cnt_q)
    n = res[0][0]
    return dict(stem=f'The table {t} for {ds["ctx"]} contains:\n{table(ds["cols"], ds["rows"])}\nWrite one SQL statement to {desc}, and state how many rows it affects.',
                answer=f'{sql} – {n} {what}', markingKey=f'{sql} (1 mark statement type and table, 1 mark SET/condition correct); {n} {what} (1 mark).', marks=3)


R.facts('ch03-st3', F(
    terms=[('INSERT', 'the DML statement that adds one or more new rows to a table'),
           ('UPDATE', 'the DML statement that changes values in existing rows, normally limited by a WHERE clause'),
           ('DELETE', 'the DML statement that removes rows from a table, normally limited by a WHERE clause'),
           ('cascading delete', 'a foreign-key option (ON DELETE CASCADE) that automatically deletes child rows when the referenced parent row is deleted')],
    facts=[('Which statement changes the price of product 104 to 12?', 'UPDATE Product SET Price = 12 WHERE ProductID = 104;', ['ALTER TABLE Product SET Price = 12;', 'INSERT INTO Product (Price) VALUES (12);', 'UPDATE Product WHERE ProductID = 104 SET Price = 12;'], 'UPDATE … SET … WHERE is the correct order.'),
           ('What does DELETE FROM Loan; do?', 'Removes every row from Loan but keeps the table', ['Removes the Loan table entirely', 'Causes a syntax error', 'Removes only the first row'], 'Without WHERE, DELETE affects all rows.')],
    why=[('Explain why an UPDATE statement without a WHERE clause is dangerous.', 'It changes the chosen column in every row of the table, overwriting correct data; unless it is inside a transaction that can be rolled back, the old values are lost.'),
         ('Explain why listing column names in an INSERT statement is good practice.', 'It makes the statement independent of column order, allows default/NULL columns to be omitted, and keeps working if new columns are added to the table later.'),
         ('Explain what happens when you try to delete a parent row that is still referenced by a foreign key.', 'With the default (RESTRICT/NO ACTION) the DBMS rejects the delete to protect referential integrity; with ON DELETE CASCADE the child rows are deleted too; with SET NULL their foreign keys are set to NULL.')],
    contrast=[('UPDATE', 'ALTER TABLE', 'UPDATE changes data values in existing rows; ALTER TABLE changes the table structure (columns, constraints).'),
              ('DELETE', 'DROP', 'DELETE removes rows but keeps the table; DROP removes the table and its structure entirely.'),
              ('ON DELETE CASCADE', 'ON DELETE RESTRICT', 'CASCADE automatically deletes dependent child rows when a parent is deleted; RESTRICT prevents deleting a parent that still has children.')],
    misc=[('INSERT INTO Student VALUES (…) can be used to change an existing student\'s score.', 'INSERT adds a new row (and would fail on a duplicate key); an existing row is changed with UPDATE … SET … WHERE.'),
          ('UPDATE Product SET Price = Price * 1.1 WHERE Category = Garden; increases garden prices by 10%.', 'The text value needs quotes – WHERE Category = \'Garden\'; otherwise Garden is treated as a column name and an error occurs.'),
          ('DELETE FROM Orders WHERE OrderID = 7 deletes column OrderID.', 'DELETE removes whole rows (here the row whose OrderID is 7); columns are removed with ALTER TABLE … DROP COLUMN.')],
    evaluate=[('Using ON DELETE CASCADE on all foreign keys makes a database easier and safer to manage.', ['no orphan rows', 'simpler application code'], ['one accidental delete can wipe large amounts of related data (e.g. all orders of a customer)', 'historical/financial records may need to be kept by law', 'hides mistakes that RESTRICT would catch'], 'Cascade only where child rows have no meaning without the parent (e.g. order lines); use RESTRICT or soft deletes for important records.')],
))
ar('ch03-st3', [
    ('UPDATE without WHERE changes every row of the table.', 'The WHERE clause restricts which rows are affected.', 0, 'Both true; R explains A.'),
    ('DELETE FROM removes the table structure.', 'DELETE is a DML statement.', 3, 'A is false; R is true – DML acts on data, not structure.'),
    ('An INSERT can fail even when its syntax is correct.', 'Constraints such as PRIMARY KEY, NOT NULL and CHECK are tested on every insert.', 0, 'Both true; R explains A.'),
])


# ---- views, transactions and ACID ----
@R.add('ch03-st4', 'C3', (2, 5), 'short')
def txn_trace(rng, slot):
    names = rng.sample(PEOPLE, 3)
    bal = [rng.choice([100, 150, 200, 250, 300, 400]) for _ in names]
    setup = ['CREATE TABLE Account (AccID INTEGER PRIMARY KEY, Owner TEXT, Balance INTEGER CHECK (Balance >= 0))',
             ('INSERT INTO Account VALUES (?, ?, ?)', [(i + 1, n_, b) for i, (n_, b) in enumerate(zip(names, bal))])]
    a1, a2 = rng.sample([1, 2, 3], 2)
    amt = rng.choice([50, 80, 120, 175, 260, 450])
    end = rng.choice(['COMMIT', 'ROLLBACK'])
    stmts = ['BEGIN TRANSACTION;', f'UPDATE Account SET Balance = Balance - {amt} WHERE AccID = {a1};', f'UPDATE Account SET Balance = Balance + {amt} WHERE AccID = {a2};', f'{end};']
    con = sqlite3.connect(':memory:')
    con.isolation_level = None
    cur = con.cursor()
    for s_ in setup:
        cur.executemany(*s_) if isinstance(s_, tuple) else cur.execute(s_)
    failed = False
    cur.execute('BEGIN')
    try:
        cur.execute(stmts[1])
        cur.execute(stmts[2])
        cur.execute(end)
    except sqlite3.IntegrityError:
        failed = True
        cur.execute('ROLLBACK')
    res = cur.execute('SELECT AccID, Owner, Balance FROM Account ORDER BY AccID').fetchall()
    con.close()
    why = ('The first UPDATE breaks CHECK (Balance >= 0), so the application rolls the whole transaction back (atomicity): no balance changes.' if failed else
           'ROLLBACK undoes both updates, so balances are unchanged.' if end == 'ROLLBACK' else f'COMMIT makes both changes permanent: account {a1} −{amt}, account {a2} +{amt}.')
    ans = fmt_rows(res) + '. ' + why
    return dict(stem=f'The table Account(AccID, Owner, Balance) has the constraint CHECK (Balance >= 0) and contains:\n{table(["AccID", "Owner", "Balance"], [(i + 1, n_, b) for i, (n_, b) in enumerate(zip(names, bal))])}\nThe following transaction is run; if any statement fails, the application issues ROLLBACK.\n' + '\n'.join(stmts) + '\nState the contents of Account afterwards and explain, with reference to the ACID properties, why.',
                answer=ans, markingKey=f'{ans} A1 correct balances; R1 explanation referring to atomicity/durability as appropriate.', marks=3 if slot.d <= 3 else 4)


@R.add('ch03-st4', 'C3', (2, 4), 'short')
def view_trace(rng, slot):
    ds = rng.choice(_DS)(rng, 6)
    t, num, cat, txt, key = ds['name'], ds['num'], ds['cat'], ds['txt'], ds['key']
    vals = sorted(r[ds['cols'].index(num)] for r in ds['rows'])
    thr = vals[2]
    cv = rng.choice(ds['catvals'])
    view = f"CREATE VIEW Top{t} AS SELECT {txt}, {num} FROM {t} WHERE {num} >= {thr};"
    change = rng.choice([f"UPDATE {t} SET {num} = {num} + 100 WHERE {cat} = '{cv}';", f"DELETE FROM {t} WHERE {cat} = '{cv}';"])
    q = f'SELECT * FROM Top{t} ORDER BY {num} DESC, {txt};'
    res = sql_seq(_setup(ds), [view, change], q)
    ans = fmt_rows(res) + ' – a view is a stored query, so it reflects the change to the base table.'
    return dict(stem=f'The table {t} contains:\n{table(ds["cols"], ds["rows"])}\nThe statements below are run in order:\n{view}\n{change}\n{q}\nState the output of the final query and explain why the view shows this data.',
                answer=ans, markingKey=f'{ans} A1 rows; A1 order; R1 the view is virtual and re-evaluated on every query.', marks=3)


R.facts('ch03-st4', F(
    terms=[('view', 'a virtual table defined by a stored SELECT query; it holds no data of its own and is re-evaluated whenever it is used'),
           ('transaction', 'a sequence of database operations treated as a single logical unit of work that either completes entirely or has no effect'),
           ('atomicity', 'the ACID property that a transaction is all-or-nothing: if any part fails, every change is rolled back'),
           ('consistency', 'the ACID property that a transaction takes the database from one valid state to another, obeying all constraints'),
           ('isolation', 'the ACID property that concurrent transactions do not see each other\'s uncommitted changes, so the result is as if they ran one after another'),
           ('durability', 'the ACID property that once a transaction is committed its changes survive crashes and power failures'),
           ('COMMIT', 'the SQL command that ends a transaction and makes its changes permanent'),
           ('ROLLBACK', 'the SQL command that undoes all changes made since the start of the current transaction')],
    why=[('Explain why a bank transfer must be executed as a single transaction.', 'Debiting one account and crediting another must both happen or neither; if the system failed between them, money would disappear or be created. A transaction guarantees atomicity.'),
         ('Explain how a DBMS achieves durability.', 'Changes are written to a transaction log on non-volatile storage before the commit is confirmed; after a crash the log is replayed to restore committed transactions.'),
         ('Explain why views can improve security.', 'Users can be granted access to a view that shows only certain columns or rows, rather than to the base table, so sensitive data (e.g. salaries) stays hidden.'),
         ('Explain why isolation matters when two users book seats at the same time.', 'Without isolation each could read the seat as free before the other\'s booking is committed, so both book it; isolation (locking or serialisable execution) makes the second see the first\'s result.')],
    contrast=[('a view', 'a table', 'A table physically stores data; a view stores only a query and shows data derived from base tables when used.'),
              ('COMMIT', 'ROLLBACK', 'COMMIT makes all changes in the transaction permanent; ROLLBACK cancels them, returning the database to its state at the start of the transaction.'),
              ('atomicity', 'durability', 'Atomicity means all-or-nothing execution of a transaction; durability means committed results persist even after a failure.')],
    misc=[('A view stores a copy of the data, so it must be refreshed after the base table changes.', 'A standard view stores only the query and is re-evaluated each time, so it always reflects current data (only materialised views store copies).'),
          ('Once a transaction has updated a row the change is permanent.', 'Until COMMIT the change can be undone with ROLLBACK, and other transactions should not see it (isolation).'),
          ('ACID properties are only needed for banking systems.', 'Any system where partial updates or concurrent conflicts would corrupt data – bookings, stock, grades, medical records – needs ACID transactions.')],
    evaluate=[('Strict ACID compliance should be enforced in every database application.', ['guarantees correctness of concurrent and failed operations', 'essential for money, bookings and records'], ['locking and logging reduce throughput', 'distributed systems may need to relax consistency for availability (BASE)', 'analytics or social feeds tolerate slight staleness'], 'Strict ACID is essential where correctness is critical; for high-scale, low-risk data, relaxed consistency can be justified.')],
))
ar('ch03-st4', [
    ('A ROLLBACK after an error leaves the database as it was before the transaction began.', 'Atomicity requires a transaction to be all-or-nothing.', 0, 'Both true; R explains A.'),
    ('A view always uses extra disk space equal to the size of its result.', 'A view is defined by a SELECT statement.', 3, 'A is false (a normal view stores only the query); R is true.'),
    ('Durability means committed data survives a power failure.', 'The DBMS writes committed changes to a log on non-volatile storage.', 0, 'Both true; logging explains durability.'),
    ('Isolation allows a transaction to read another transaction\'s uncommitted changes.', 'Isolation keeps concurrent transactions apart.', 3, 'A is false (that would be a dirty read); R is true.'),
])


# =============================================================================================
# ch04 A3.4 Alternative databases and data warehouses (HL)
# =============================================================================================
@R.add('ch04-st1', 'C3', (1, 4), 'short')
def kv_trace(rng, slot):
    ctx = rng.choice(['a session cache for a game server in Singapore', 'a shopping-cart store for an online shop in Lima', 'a feature-flag store for an app in Oslo'])
    keys = rng.sample(['user:17', 'user:42', 'cart:9', 'cart:12', 'flag:dark', 'flag:beta', 'sess:a1', 'sess:b7'], 4)
    store = OrderedDict()
    ops = []
    n = 4 if slot.d <= 2 else 6 if slot.d == 3 else 8
    for _ in range(n):
        k = rng.choice(keys)
        kind = rng.choice(['PUT', 'PUT', 'GET', 'DELETE', 'INCR'])
        if kind == 'PUT':
            v = rng.randint(1, 20)
            store[k] = v
            ops.append(f'PUT {k} {v}')
        elif kind == 'INCR':
            store[k] = store.get(k, 0) + 1
            ops.append(f'INCR {k}')
        elif kind == 'DELETE':
            store.pop(k, None)
            ops.append(f'DELETE {k}')
        else:
            ops.append(f'GET {k}')
    q = rng.choice(keys)
    ops.append(f'GET {q}')
    gets = []
    st2 = {}
    for o in ops:
        p = o.split()
        if p[0] == 'PUT':
            st2[p[1]] = int(p[2])
        elif p[0] == 'INCR':
            st2[p[1]] = st2.get(p[1], 0) + 1
        elif p[0] == 'DELETE':
            st2.pop(p[1], None)
        else:
            gets.append(f'{p[1]} → {st2.get(p[1], "nil")}')
    final = ', '.join(f'{k}={v}' for k, v in sorted(st2.items())) or '(empty)'
    ans = f'GET results: {"; ".join(gets)}. Final store: {final}.'
    return dict(stem=f'A key-value database is used as {ctx}. It starts empty. PUT k v stores v under k (overwriting), INCR k adds 1 (treating a missing key as 0), DELETE k removes k, and GET k returns the value or nil. Trace these operations and give the value returned by each GET and the final contents:\n' + '\n'.join(ops),
                answer=ans, markingKey=ans + ' 1 mark per correct GET (max 3), 1 mark final store.', marks=min(4, len(gets) + 1))


def _docs(rng):
    cities = rng.sample(['Lima', 'Accra', 'Oslo', 'Hanoi', 'Seoul'], 3)
    docs = []
    for i in range(6):
        tags = rng.sample(['vegan', 'halal', 'spicy', 'budget', 'family'], rng.randint(0, 2))
        d = {'_id': i + 1, 'name': rng.choice(['Tika', 'Mesa', 'Fika', 'Pho Ga', 'Bibim', 'Jollof', 'Ceviche', 'Kimchi']) + f' {i + 1}',
             'city': rng.choice(cities), 'rating': rng.choice([3.5, 4.0, 4.2, 4.5, 4.8]), 'tags': tags}
        if rng.random() < 0.5:
            d['delivery'] = rng.choice([True, False])
        docs.append(d)
    return docs, cities


def _doc_txt(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, str):
            parts.append(f'"{k}": "{v}"')
        elif isinstance(v, bool):
            parts.append(f'"{k}": {"true" if v else "false"}')
        elif isinstance(v, list):
            parts.append(f'"{k}": [' + ', '.join(f'"{x}"' for x in v) + ']')
        else:
            parts.append(f'"{k}": {v}')
    return '{' + ', '.join(parts) + '}'


@R.add('ch04-st1', 'C3', (2, 5), 'short')
def doc_query(rng, slot):
    docs, cities = _docs(rng)
    c = rng.choice(cities)
    r = rng.choice([4.0, 4.2, 4.5])
    tag = rng.choice(['vegan', 'halal', 'spicy', 'budget', 'family'])
    qs = [
        (f'{{"city": "{c}"}}', lambda d: d['city'] == c),
        (f'{{"rating": {{"$gte": {r}}}}}', lambda d: d['rating'] >= r),
        (f'{{"tags": "{tag}"}}  (matches if the array contains the value)', lambda d: tag in d['tags']),
        (f'{{"delivery": {{"$exists": true}}}}', lambda d: 'delivery' in d),
        (f'{{"city": "{c}", "rating": {{"$gt": {r}}}}}', lambda d: d['city'] == c and d['rating'] > r),
    ]
    q, f_ = rng.choice(qs if slot.d >= 3 else qs[:3])
    hits = [d['_id'] for d in docs if f_(d)]
    ans = f'Documents with _id {", ".join(map(str, hits))} ({len(hits)} matches).' if hits else 'No documents match (0).'
    extra = ' Explain one advantage of storing the restaurants as documents rather than relational rows.' if slot.d >= 4 else ''
    return dict(stem='A document database for a food-delivery app stores these restaurant documents in a collection:\n' + '\n'.join(_doc_txt(d) for d in docs) + f'\nWhich documents are returned by the query find({q})?{extra}',
                answer=ans, markingKey=ans + (' Advantage: documents can have different fields (e.g. only some have "delivery") and hold arrays such as tags without extra tables or NULL columns.' if extra else ''), marks=2 if slot.d <= 3 else 4)


@R.add('ch04-st1', 'C3', (2, 5), 'short')
def graph_fof(rng, slot):
    people = rng.sample(PEOPLE, 7)
    edges = set()
    while len(edges) < 8:
        a, b = rng.sample(people, 2)
        edges.add(tuple(sorted((a, b))))
    adj = {p: set() for p in people}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    src = max(people, key=lambda p: (len(adj[p]), p))
    fof = sorted(set().union(*[adj[f] for f in adj[src]]) - adj[src] - {src}) if adj[src] else []
    # shortest path lengths
    dist = {src: 0}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
    tgt = max((p for p in people if p in dist), key=lambda p: (dist[p], p))
    e_txt = ', '.join(f'{a}–{b}' for a, b in sorted(edges))
    if slot.d <= 3:
        ans = ', '.join(fof) if fof else 'none'
        return dict(stem=f'A graph database for a social app stores FRIEND relationships (undirected): {e_txt}. List the friends-of-friends of {src} who are not already {src}\'s friends, and explain why a graph database answers this query efficiently.',
                    answer=f'{ans}. Graph databases store relationships as edges, so the query follows edges from {src} directly instead of performing repeated self-joins.',
                    markingKey=f'Direct friends of {src}: {", ".join(sorted(adj[src]))}. Friends-of-friends (excluding {src} and direct friends): {ans} (A2). Explanation: index-free adjacency / traversal vs joins (R1).', marks=3)
    return dict(stem=f'A graph database stores FRIEND relationships (undirected): {e_txt}. Find the length of the shortest chain of friendships from {src} to {tgt}, and outline how the equivalent query would be written in a relational database.',
                answer=f'{dist[tgt]} edge(s). In SQL a Friendship(PersonA, PersonB) table would need {dist[tgt]} self-joins (or a recursive CTE), which becomes slow as the chain grows.',
                markingKey=f'Breadth-first traversal from {src} gives distance {dist[tgt]} to {tgt} (A2). Relational version: link table plus repeated self-joins / recursive query (R1); comparison of efficiency (R1).', marks=4)


R.facts('ch04-st1', F(
    terms=[('document database', 'a NoSQL database that stores each record as a self-describing document (e.g. JSON) whose fields can differ between documents'),
           ('key-value store', 'a NoSQL database that stores values that are retrieved only by a unique key, like a large distributed hash table'),
           ('column-family (wide-column) database', 'a NoSQL database that stores data in rows grouped into column families, where each row can have different columns and data are stored and read by column'),
           ('graph database', 'a NoSQL database that stores entities as nodes and relationships as edges, both with properties, for efficient traversal of connections'),
           ('collection', 'a group of documents in a document database, comparable to a table'),
           ('node (graph)', 'an entity such as a person or place stored in a graph database'),
           ('edge (graph)', 'a stored, named relationship between two nodes in a graph database, such as FRIEND_OF')],
    facts=[('Which NoSQL model is best for storing user sessions retrieved by session ID?', 'Key-value store', ['Graph database', 'Column-family database', 'Data warehouse'], 'Access is purely by a single key.'),
           ('Which NoSQL model is best suited to fraud detection through chains of linked transactions?', 'Graph database', ['Key-value store', 'Document database', 'Flat file'], 'Following relationships is what graph databases are optimised for.'),
           ('Which model suits storing billions of time-stamped sensor readings that are analysed by column?', 'Column-family database', ['Key-value store', 'Graph database', 'Spreadsheet'], 'Wide-column stores handle huge, write-heavy, column-oriented data.'),
           ('Product catalogues where each product type has different attributes are best suited to…', 'a document database', ['a key-value store with no structure', 'a graph database', 'a single fixed relational table'], 'Documents allow flexible fields per product.')],
    why=[('Explain why a document database can avoid joins.', 'Related data (e.g. an order and its order lines) can be embedded in one document, so the whole object is read in a single operation instead of joining several tables.'),
         ('Explain why key-value stores are very fast.', 'Each value is located directly by hashing its key, with no query parsing, joins or schema checks; data is often held in memory and spread across nodes by key.'),
         ('Explain why graph databases outperform relational databases for deep relationship queries.', 'Edges are stored with each node (index-free adjacency), so each hop is a pointer traversal; a relational database needs a join per hop, whose cost grows with table size and depth.')],
    contrast=[('a document database', 'a key-value store', 'A document database understands the structure of its documents and can query or index fields inside them; a key-value store treats the value as opaque and can only look it up by key.'),
              ('a graph database', 'a relational database', 'A graph database stores relationships explicitly as edges and traverses them directly; a relational database represents relationships with foreign keys and reconstructs them with joins.'),
              ('a column-family database', 'a row-oriented relational database', 'A column-family store groups and stores data by column families with flexible columns per row, efficient for wide sparse data and column scans; a row store keeps each row\'s fixed fields together, efficient for whole-record transactions.')],
    misc=[('Embedding data in documents means data is never duplicated.', 'Embedding often duplicates data (e.g. customer address copied into each order document) which can become inconsistent; designers trade duplication for read speed.'),
          ('A key-value store can efficiently find all values greater than 100.', 'Values are opaque and indexed only by key, so such a query requires scanning every pair; secondary indexes or a different model are needed.'),
          ('Graph databases can only store social networks.', 'They suit any highly connected data: road networks, recommendation engines, fraud rings, knowledge graphs, supply chains.')],
    evaluate=[('A document database is the best choice for an e-commerce platform.', ['product data varies by category', 'orders can be stored as single documents', 'scales horizontally for traffic peaks'], ['payments and stock need strong consistency across documents', 'reporting across customers and products needs joins', 'duplicated embedded data may become inconsistent'], 'A document store suits the catalogue; payments and inventory are better kept in a relational, ACID-compliant database – a polyglot design.')],
))
ar('ch04-st1', [
    ('Documents in the same collection may have different fields.', 'Document databases are schema-flexible.', 0, 'Both true; R explains A.'),
    ('A graph database stores relationships as edges.', 'Edges can have properties such as a "since" date.', 1, 'Both true, but having properties is not why relationships are edges.'),
    ('Key-value stores support complex joins between values.', 'Key-value stores retrieve values by key only.', 3, 'A is false; R is true.'),
])


# ---- data warehouses, ETL, OLAP ----
def _fact(rng, n):
    regions = rng.sample(['North', 'South', 'East', 'West'], 3)
    prods = rng.sample(['Tea', 'Coffee', 'Cocoa', 'Rice', 'Maize'], 3)
    qs = rng.sample(['Q1', 'Q2', 'Q3'], 2)
    rows = []
    for _ in range(n):
        rows.append((rng.choice(regions), rng.choice(prods), rng.choice(qs), rng.choice([10, 20, 25, 30, 40, 50, 60])))
    return regions, prods, qs, rows


@R.add('ch04-st2', 'C3', (1, 5), 'numerical')
def olap(rng, slot):
    regions, prods, qs, rows = _fact(rng, 8 if slot.d <= 3 else 10)
    op = rng.choice(['rollup', 'slice', 'dice', 'drill'] if slot.d >= 3 else ['rollup', 'slice'])
    tb = table(['Region', 'Product', 'Quarter', 'Sales (k$)'], rows)
    if op == 'rollup':
        dim = rng.choice(['Region', 'Product'])
        i = 0 if dim == 'Region' else 1
        agg = Counter()
        for r in rows:
            agg[r[i]] += r[3]
        ans = '; '.join(f'{k}: {v}' for k, v in sorted(agg.items()))
        stem = f'A cooperative\'s data warehouse in Accra contains this sales fact table:\n{tb}\nPerform a roll-up to give total sales by {dim} (summing over the other dimensions).'
    elif op == 'slice':
        q = rng.choice(qs)
        agg = Counter()
        for r in rows:
            if r[2] == q:
                agg[r[1]] += r[3]
        ans = '; '.join(f'{k}: {v}' for k, v in sorted(agg.items())) or 'no sales'
        stem = f'A data warehouse holds this sales cube (Region × Product × Quarter):\n{tb}\nTake the slice Quarter = {q} and give total sales for each product within that slice.'
    elif op == 'dice':
        rr = rng.sample(regions, 2)
        p = rng.choice(prods)
        tot = sum(r[3] for r in rows if r[0] in rr and r[1] == p)
        ans = f'{tot}'
        stem = f'The sales fact table below is stored in a data warehouse.\n{tb}\nA dice operation selects Region ∈ {{{", ".join(rr)}}} and Product = {p}. Calculate the total sales in the resulting sub-cube.'
    else:
        reg = rng.choice(regions)
        agg = Counter()
        for r in rows:
            if r[0] == reg:
                agg[(r[1], r[2])] += r[3]
        ans = '; '.join(f'{a} {b}: {v}' for (a, b), v in sorted(agg.items())) or 'no sales'
        tot = sum(agg.values())
        ans = f'Total for {reg}: {tot}. Drill-down: {ans}'
        stem = f'A manager sees the total sales for the {reg} region and drills down by Product and Quarter. Using the fact table below, give the {reg} total and the drill-down figures.\n{tb}'
    return dict(stem=stem, answer=ans, markingKey=f'{ans}. M1 correct selection of cells; A1 correct sums.', marks=2 if slot.d <= 2 else 3)


@R.add('ch04-st2', 'C3', (2, 4), 'short')
def etl_transform(rng, slot):
    rates = {'EUR': 1.10, 'GBP': 1.25, 'KES': 0.0077, 'SGD': 0.74}
    recs = []
    for i in range(5):
        cur = rng.choice(list(rates))
        amt = rng.choice([100, 250, 400, 1000, 20000]) if cur == 'KES' else rng.choice([20, 45, 80, 120, 300])
        date = rng.choice(['2026-03-04', '04/03/2026', '2026-03-05', '05/03/2026'])
        recs.append((f'T{i + 1}', amt, cur, date))
    dup = rng.randrange(5)
    recs.append(recs[dup])
    out = []
    seen = set()
    for r in recs:
        if r in seen:
            continue
        seen.add(r)
        d = r[3] if '-' in r[3] else f'{r[3][6:]}-{r[3][3:5]}-{r[3][:2]}'
        out.append(f'{r[0]}: {r[1] * rates[r[2]]:.2f} USD, {d}')
    tot = sum(r[1] * rates[r[2]] for r in set(recs))
    ans = '; '.join(out) + f'. Total = {tot:.2f} USD (duplicate {recs[dup][0]} removed).'
    return dict(stem='During the transform stage of ETL, records from shops in four countries must be converted to USD (EUR × 1.10, GBP × 1.25, KES × 0.0077, SGD × 0.74), dates standardised to YYYY-MM-DD (DD/MM/YYYY sources) and exact duplicates removed.\n' + table(['TxID', 'Amount', 'Currency', 'Date'], recs) + '\nGive the transformed records and the total in USD.',
                answer=ans, markingKey=ans + ' 1 mark conversion, 1 mark date format, 1 mark duplicate removed, 1 mark total.', marks=4)


R.facts('ch04-st2', F(
    terms=[('data warehouse', 'a large, subject-oriented, integrated, time-variant and non-volatile store of historical data from many sources, used for analysis and decision-making'),
           ('ETL', 'extract, transform, load: copying data from source systems, cleaning and converting it, and loading it into a data warehouse'),
           ('OLAP', 'online analytical processing: interactive multidimensional analysis of data (roll-up, drill-down, slice, dice, pivot) for decision support'),
           ('OLTP', 'online transaction processing: systems that process many short, concurrent transactions such as sales and bookings'),
           ('data mart', 'a smaller, subject-specific subset of a data warehouse for one department'),
           ('fact table', 'the central table in a star schema holding numeric measures (e.g. sales) with foreign keys to dimension tables'),
           ('dimension table', 'a table in a star schema describing a perspective for analysis, such as time, product or region'),
           ('star schema', 'a warehouse design with one fact table linked directly to several denormalised dimension tables')],
    facts=[('Which OLAP operation moves from monthly to quarterly totals?', 'Roll-up', ['Drill-down', 'Slice', 'Pivot'], 'Aggregating to a coarser level is roll-up.'),
           ('Fixing one dimension (e.g. Year = 2025) to view a 2-D sub-cube is called…', 'a slice', ['a dice', 'a roll-up', 'a merge'], 'A slice fixes a single dimension value.'),
           ('Data in a warehouse is described as non-volatile. This means…', 'it is not changed once loaded; new data is added periodically', ['it is lost when power fails', 'it is updated by every sale in real time', 'it is stored only in RAM'], 'Warehouses keep a stable historical record.'),
           ('In ETL, removing duplicates and converting currencies happens in which stage?', 'Transform', ['Extract', 'Load', 'Query'], 'Cleaning and conversion are transformations.')],
    why=[('Explain why organisations keep a separate data warehouse instead of running analysis on the operational (OLTP) database.', 'Heavy analytical queries would slow the transactional system used by customers; the warehouse integrates data from many sources, keeps history, and is structured (star schema, denormalised) for fast aggregation.'),
         ('Explain why data warehouses are often denormalised.', 'Analysis reads large volumes and aggregates them; fewer joins (star schema) make queries faster, and because data is loaded in batches and not updated, the anomalies normalisation prevents are not a concern.'),
         ('Explain why the transform stage of ETL is important for data quality.', 'Source systems use different formats, units, codes and may contain errors or duplicates; transformation cleans, standardises and integrates them so analyses are consistent and trustworthy.')],
    contrast=[('OLTP', 'OLAP', 'OLTP handles many short, concurrent read/write transactions on current data (normalised); OLAP runs complex read-only analytical queries over large historical datasets (often denormalised).'),
              ('a data warehouse', 'a data mart', 'A data warehouse integrates data for the whole organisation; a data mart is a smaller subset focused on one subject or department.'),
              ('roll-up', 'drill-down', 'Roll-up aggregates data to a higher level (days → months); drill-down goes to more detail (year → quarter → month).'),
              ('slice', 'dice', 'A slice fixes one dimension to a single value; a dice selects ranges or sets of values on two or more dimensions, giving a sub-cube.')],
    misc=[('A data warehouse is updated every time a customer buys something.', 'Warehouses are usually loaded in periodic batches by ETL; the operational database records each sale.'),
          ('ETL just copies data from one database to another.', 'ETL also transforms data – cleaning, standardising, integrating and aggregating – before loading.'),
          ('OLAP cubes can only have three dimensions.', 'A "cube" can have any number of dimensions (hypercube); three is just easy to draw.')],
    evaluate=[('Building a data warehouse is worthwhile for a medium-sized retail chain.', ['integrated historical data supports trend analysis and forecasting', 'OLAP lets managers analyse by region/product/time', 'removes analytical load from the till system'], ['high cost of design, ETL development and storage', 'data is only as current as the last load', 'requires skilled staff and good data quality'], 'Usually worthwhile once data from several systems must be analysed regularly; cloud warehouses reduce cost, but benefits depend on data quality and clear business questions.')],
))
ar('ch04-st2', [
    ('A star schema has one fact table surrounded by dimension tables.', 'Dimension tables describe the context of the measures in the fact table.', 0, 'Both true; R explains the structure.'),
    ('Data warehouses are designed mainly for fast INSERT and UPDATE of individual records.', 'Warehouses are optimised for reading and aggregating large volumes of data.', 3, 'A is false; R is true.'),
    ('Drill-down shows data at a finer level of detail.', 'Drill-down is the reverse of roll-up.', 0, 'Both true; being the reverse of aggregation explains why it shows more detail.'),
])


# ---- distributed databases ----
@R.add('ch04-st3', 'C3', (1, 4), 'numerical')
def hash_partition(rng, slot):
    n = rng.choice([3, 4, 5])
    ids = rng.sample(range(1000, 9999), 6 if slot.d <= 2 else 8)
    place = {i: i % n for i in ids}
    ans = '; '.join(f'{i} → node {place[i]}' for i in ids)
    cnt = Counter(place.values())
    extra = ''
    if slot.d >= 3:
        m = n + 1
        moved = sum(1 for i in ids if i % m != i % n)
        extra = f' A node is then added (node = CustomerID mod {m}). How many of these records must move?'
        ans += f'. After adding a node, {moved} of {len(ids)} records move.'
    return dict(stem=f'A distributed database for a bank in {rng.choice(CITIES)} partitions customer records across {n} nodes (0–{n - 1}) using node = CustomerID mod {n}. State the node for each CustomerID: {", ".join(map(str, ids))}.{extra}',
                answer=ans, markingKey=ans + (' This shows why simple modulo hashing is costly to re-partition; consistent hashing moves far fewer keys.' if extra else '') + ' 1 mark per two correct placements.', marks=3 if slot.d <= 2 else 4)


@R.add('ch04-st3', 'C3', (2, 5), 'numerical')
def quorum(rng, slot):
    N = rng.choice([3, 5, 7])
    W = rng.randint(1, N)
    Rr = rng.randint(1, N)
    strong = Rr + W > N
    if slot.d <= 3:
        ans = f'R + W = {Rr + W} {">" if strong else "≤"} N = {N}, so reads are {"guaranteed to see the latest write (strong consistency)" if strong else "NOT guaranteed to see the latest write (eventual consistency)"}.'
        return dict(stem=f'A distributed key-value store replicates every item on N = {N} nodes. A write succeeds after W = {W} nodes confirm it and a read queries R = {Rr} nodes. Determine whether every read is guaranteed to return the most recent write.',
                    answer=ans, markingKey=ans + ' M1 quorum rule R + W > N; A1 conclusion; R1 overlap of read and write sets.', marks=3)
    p = rng.choice([0.9, 0.95, 0.99])
    k = N
    avail = 1 - (1 - p) ** k
    tol = N - W
    ans = f'Probability at least one replica is up = 1 − {r2(1 - p)}^{k} = {avail:.6f}. With W = {W} the system tolerates {tol} failed node(s) for writes; R + W = {Rr + W} {">" if strong else "≤"} {N} so consistency is {"strong" if strong else "eventual"}.'
    return dict(stem=f'Data in a distributed database is replicated on {N} independent nodes, each available with probability {p}. (a) Calculate the probability that at least one replica is available. (b) Writes require W = {W} acknowledgements and reads query R = {Rr} nodes: state how many node failures writes can tolerate and whether reads are strongly consistent.',
                answer=ans, markingKey=ans + ' M1 complement rule; A1 probability; A1 failures tolerated; R1 quorum argument.', marks=4)


R.facts('ch04-st3', F(
    terms=[('distributed database', 'a database whose data is stored across several physical sites or nodes connected by a network but presented to users as a single database'),
           ('replication', 'storing copies of the same data on more than one node to improve availability, fault tolerance and read performance'),
           ('partitioning (sharding)', 'splitting a database into parts (by rows or columns) stored on different nodes so that each node holds only part of the data'),
           ('horizontal partitioning', 'splitting a table by rows, for example customers A–M on one node and N–Z on another'),
           ('vertical partitioning', 'splitting a table by columns, keeping frequently used columns separate from rarely used ones'),
           ('CAP theorem', 'the principle that a distributed system cannot simultaneously guarantee consistency, availability and partition tolerance; during a network partition it must choose consistency or availability')],
    facts=[('Which technique mainly improves fault tolerance in a distributed database?', 'Replication', ['Vertical partitioning', 'Normalisation', 'Indexing'], 'Copies on other nodes keep data available if one fails.'),
           ('Splitting a Customers table so European customers are stored in Frankfurt and Asian customers in Singapore is…', 'horizontal partitioning (sharding)', ['vertical partitioning', 'replication', 'denormalisation'], 'Rows are divided between sites.'),
           ('According to the CAP theorem, during a network partition a system must choose between…', 'consistency and availability', ['atomicity and durability', 'speed and storage', 'replication and indexing'], 'Partition tolerance is required, so C or A must give way.')],
    why=[('Explain why replication can make updates slower.', 'Every replica must be updated; synchronous replication waits for all (or a quorum of) nodes to confirm, adding network delay, and conflicts between replicas must be resolved.'),
         ('Explain why a multinational company might partition customer data by region.', 'Queries are answered from a nearby node (lower latency), load is spread across servers, and data can be kept in the region required by local privacy laws (data sovereignty).'),
         ('Explain why distributed transactions need a protocol such as two-phase commit.', 'A transaction may update data on several nodes; two-phase commit makes all nodes first prepare and vote, then all commit or all abort, preserving atomicity across sites.')],
    contrast=[('replication', 'partitioning', 'Replication stores copies of the same data on several nodes (availability, read speed); partitioning stores different subsets of the data on different nodes (scalability).'),
              ('synchronous replication', 'asynchronous replication', 'Synchronous replication confirms a write only when all replicas are updated (consistent but slower); asynchronous confirms immediately and updates replicas later (faster but replicas may lag).'),
              ('horizontal partitioning', 'vertical partitioning', 'Horizontal partitioning divides rows between nodes; vertical partitioning divides columns.')],
    misc=[('Replicating data on more nodes always makes the database more consistent.', 'More replicas improve availability but make it harder to keep every copy identical; consistency needs synchronous or quorum writes.'),
          ('A distributed database means users must know where each piece of data is stored.', 'Distribution transparency hides location: users query one logical database and the DBMS routes the query.'),
          ('Sharding removes the need for backups.', 'Each shard holds unique data; losing a shard loses that data unless it is replicated and backed up.')],
    evaluate=[('A global e-commerce company should use a distributed rather than a centralised database.', ['lower latency for users worldwide', 'no single point of failure', 'scales by adding nodes', 'supports regional data-protection laws'], ['more complex to design and administer', 'consistency across sites is harder (CAP trade-offs)', 'distributed transactions are slower', 'higher network and security costs'], 'For a global company the availability and latency benefits usually outweigh the complexity, provided critical transactions use strong consistency.')],
))
ar('ch04-st3', [
    ('Replication improves the availability of a distributed database.', 'If one node fails, a copy of the data can be read from another node.', 0, 'Both true; R explains A.'),
    ('In the CAP theorem a system can always guarantee all three properties.', 'Network partitions can occur in any distributed system.', 3, 'A is false; R is true (and is why a trade-off is unavoidable).'),
])


# ---- spatial / temporal / data lakes ----
@R.add('ch04-st4', 'C3', (1, 5), 'numerical')
def spatial_q(rng, slot):
    kind = rng.choice(['ambulance stations', 'bike-share docks', 'mobile-phone masts', 'water pumps'])
    pts = {f'{kind[0].upper()}{i}': (rng.randint(0, 20), rng.randint(0, 20)) for i in range(1, 7)}
    q = (rng.randint(3, 17), rng.randint(3, 17))
    dist = {k: math.dist(v, q) for k, v in pts.items()}
    pt = '; '.join(f'{k} ({x}, {y})' for k, (x, y) in pts.items())
    mode = rng.choice(['nearest', 'radius', 'box'] if slot.d >= 3 else ['nearest', 'box'])
    if mode == 'nearest':
        best = min(dist, key=lambda k: (dist[k], k))
        ans = f'{best} at distance {dist[best]:.2f} km'
        stem = f'A spatial database stores the locations (in km on a city grid) of {kind}: {pt}. An incident occurs at ({q[0]}, {q[1]}). Using straight-line distance, which point is nearest and how far is it?'
    elif mode == 'radius':
        rad = rng.choice([5, 6, 8])
        hits = sorted(k for k in dist if dist[k] <= rad)
        ans = (', '.join(hits) if hits else 'none') + f' (distances: ' + ', '.join(f'{k} {dist[k]:.2f}' for k in sorted(dist)) + ')'
        stem = f'A spatial query must return all {kind} within {rad} km of ({q[0]}, {q[1]}). The stored points are: {pt}. List the points returned.'
    else:
        x1, x2 = sorted(rng.sample(range(0, 21), 2))
        y1, y2 = sorted(rng.sample(range(0, 21), 2))
        hits = sorted(k for k, (x, y) in pts.items() if x1 <= x <= x2 and y1 <= y <= y2)
        ans = ', '.join(hits) if hits else 'none'
        stem = f'A map app sends a bounding-box query for the visible screen area x from {x1} to {x2} and y from {y1} to {y2} (inclusive). The {kind} are stored at: {pt}. Which points are returned?'
    return dict(stem=stem, answer=ans, markingKey=f'{ans}. M1 correct distance/containment test; A1 correct points. Spatial indexes (R-trees) avoid testing every point.', marks=2 if slot.d <= 2 else 3)


@R.add('ch04-st4', 'C3', (2, 5), 'short')
def temporal_q(rng, slot):
    item = rng.choice(['the price of a 1 kg bag of rice in Hanoi', 'the exchange rate EUR→KES used by a remittance firm', 'the job title of an employee in Toronto', 'the monthly rent of flat 4B in Lisbon'])
    import datetime as _dt
    day = rng.randint(1, 20)
    months = [(2025, 1), (2025, rng.choice([3, 4, 5])), (2025, rng.choice([8, 9, 10])), (2026, rng.choice([1, 2, 3]))]
    starts = [_dt.date(y, m_, day) for y, m_ in months]
    vals = [rng.randint(10, 99) for _ in range(4)]
    rows = []
    for i in range(4):
        end = (starts[i + 1] - _dt.timedelta(days=1)).isoformat() if i < 3 else '9999-12-31'
        rows.append((vals[i], starts[i].isoformat(), end))
    qd_m = rng.choice(['2025-03', '2025-06', '2025-12', '2026-05', '2025-04'])
    qd = f'{qd_m}-{rng.randint(1, 28):02d}'
    hit = [r for r in rows if r[1] <= qd <= r[2]]
    ans = f'{hit[0][0]} (valid from {hit[0][1]} to {hit[0][2]})' if hit else 'no value was valid on that date'
    return dict(stem=f'A temporal database stores {item} with valid-time periods (ValidFrom, ValidTo inclusive):\n' + table(['Value', 'ValidFrom', 'ValidTo'], rows) + f'\nWhat value was valid on {qd}? Explain why storing ValidFrom/ValidTo is better than overwriting the value.',
                answer=f'{ans}. Overwriting would lose history; valid-time periods allow "as-of" queries, auditing and trend analysis.',
                markingKey=f'{ans} (A1); compare {qd} with each period (M1); history/audit/as-of queries (R1).', marks=3)


R.facts('ch04-st4', F(
    terms=[('spatial database', 'a database optimised to store and query data about objects in space – points, lines and polygons – using spatial data types, functions and indexes'),
           ('temporal database', 'a database that records time periods for which facts are valid (valid time) and/or when they were stored (transaction time), keeping history'),
           ('data lake', 'a central repository that stores large amounts of raw structured, semi-structured and unstructured data in its native format until it is needed (schema-on-read)'),
           ('valid time', 'the period during which a fact was true in the real world'),
           ('transaction time', 'the period during which a fact was recorded in the database'),
           ('R-tree', 'a spatial index that groups nearby objects in nested minimum bounding rectangles to speed up spatial queries'),
           ('GIS', 'geographic information system: software that captures, stores, analyses and displays spatial data on maps')],
    facts=[('Which query is typical of a spatial database?', 'Find all hospitals within 5 km of a given point', ['Find the average salary per department', 'List orders placed in March', 'Count students in each house'], 'Distance-based queries use spatial functions and indexes.'),
           ('A data lake typically stores data…', 'in raw, native formats, with structure applied when read', ['only after it has been normalised to 3NF', 'only as relational tables', 'only as images'], 'Schema-on-read is a defining feature.'),
           ('Recording that an employee\'s salary was 52 000 from 2024-01-01 to 2025-06-30 uses…', 'valid time in a temporal database', ['a spatial index', 'a key-value store', 'vertical partitioning'], 'The period of real-world truth is valid time.')],
    why=[('Explain why spatial indexes such as R-trees are needed.', 'Ordinary B-tree indexes sort values in one dimension, but spatial queries involve two or more dimensions; R-trees group nearby objects into bounding rectangles so most of the data can be skipped when searching an area.'),
         ('Explain why a data lake can turn into a "data swamp".', 'Because data is stored raw without enforced schema, poor metadata, cataloguing and governance make it hard to find, trust or understand the data, so it becomes unusable.'),
         ('Explain why a temporal database is useful for auditing.', 'It keeps every past version with its time period, so auditors can see what was true (and what the system recorded) at any moment and who changed it, rather than only the current value.')],
    contrast=[('a data lake', 'a data warehouse', 'A data lake stores raw data of any type with schema-on-read and is suited to data science/ML; a data warehouse stores cleaned, structured, integrated data with schema-on-write for reporting and OLAP.'),
              ('valid time', 'transaction time', 'Valid time records when a fact was true in the real world; transaction time records when the fact was stored in the database.'),
              ('raster spatial data', 'vector spatial data', 'Raster data is a grid of cells (pixels) such as satellite images; vector data uses points, lines and polygons such as roads and boundaries.')],
    misc=[('A data lake replaces the need for data cleaning.', 'Data still needs cleaning and transformation – it is just done when the data is read and used, not when it is stored.'),
          ('A spatial query can be answered efficiently by sorting points by their x-coordinate only.', 'Points close in x may be far apart in y; spatial indexes consider both dimensions together.'),
          ('Temporal databases simply add a timestamp column showing when a row was last changed.', 'They store periods of validity for every version, keeping full history, not only the last update time.')],
    evaluate=[('Organisations should store all their data in a data lake rather than a data warehouse.', ['cheap storage of any data type at scale', 'keeps raw data for future ML uses', 'fast ingestion with no up-front modelling'], ['without governance it becomes a data swamp', 'business users need clean, structured data for reports', 'query performance and data quality are lower'], 'Many organisations use both (or a "lakehouse"): the lake for raw and ML data, the warehouse for trusted reporting.')],
))
ar('ch04-st4', [
    ('A data lake uses schema-on-read.', 'Data is stored in its raw format and structured only when it is analysed.', 0, 'Both true; R explains A.'),
    ('Spatial databases can only store point data.', 'Spatial data types include points, lines and polygons.', 3, 'A is false; R is true.'),
])


# =============================================================================================
# ch05 A4.1 Machine learning fundamentals
# =============================================================================================
_ML_SCEN = [
    ('A bank in Singapore trains a model on 200 000 past loans, each labelled "repaid" or "defaulted", to predict whether new applicants will default.', 'supervised learning (classification)', 'the training data has known labels (repaid/defaulted) and the output is a category'),
    ('A supermarket in Hanoi groups its loyalty-card customers into segments based on what they buy, without any predefined groups.', 'unsupervised learning (clustering)', 'there are no labels; the algorithm discovers structure (groups) in the data'),
    ('A robot vacuum learns which cleaning routes save battery by receiving a reward each time it finishes a room with energy left.', 'reinforcement learning', 'an agent learns by trial and error from rewards/penalties for its actions in an environment'),
    ('An estate agency in Lisbon predicts the selling price of flats from their size, location and age using past sales.', 'supervised learning (regression)', 'labelled examples with a continuous numerical target (price)'),
    ('A credit-card company flags transactions that are very unlike a customer\'s usual spending, without labelled fraud examples.', 'unsupervised learning (anomaly detection)', 'it learns normal patterns from unlabelled data and flags outliers'),
    ('A program learns to play Go by playing millions of games against itself and being rewarded for wins.', 'reinforcement learning', 'learning a policy from the reward signal of winning or losing'),
    ('An email provider learns to sort messages into "spam" and "not spam" from messages users have marked.', 'supervised learning (classification)', 'the user-marked messages provide labels'),
    ('An online shop finds that customers who buy tents often also buy head torches.', 'unsupervised learning (association rule learning)', 'rules are mined from unlabelled transaction data'),
    ('A self-driving delivery robot in Tallinn improves its route choices using rewards for on-time deliveries and penalties for near-collisions.', 'reinforcement learning', 'actions are chosen to maximise cumulative reward'),
    ('A hospital in Nairobi predicts patients\' length of stay in days from admission data labelled with actual stays.', 'supervised learning (regression)', 'labelled data with a numerical output'),
    ('A music service compresses each song\'s 500 audio features into 10 features that capture most of the variation.', 'unsupervised learning (dimensionality reduction)', 'no labels; it finds a lower-dimensional representation'),
    ('A climate lab labels a few hundred satellite images as "flooded" and uses them together with a million unlabelled images to train a classifier.', 'semi-supervised learning', 'a small labelled set is combined with a large unlabelled set'),
]


@R.add('ch05-st1', 'C3', (1, 4), 'short')
def ml_type(rng, slot):
    sc, t, why = rng.choice(_ML_SCEN)
    frame = rng.choice(['Identify the type of machine learning used and justify your answer.', 'State which type of machine learning this is and explain how you can tell.', 'Classify this application as supervised, unsupervised, semi-supervised or reinforcement learning, giving a reason.'])
    return dict(stem=f'{sc} {frame}', answer=f'{t} – {why}', markingKey=f'{t} (1); justification: {why} (1).', marks=2)


@R.add('ch05-st1', 'C1', (1, 3), 'mcq')
def ml_type_mcq(rng, slot):
    sc, t, why = rng.choice(_ML_SCEN)
    main = t.split(' (')[0]
    wr = [x for x in ['supervised learning', 'unsupervised learning', 'reinforcement learning', 'semi-supervised learning'] if x != main]
    return mcq(rng, f'{sc} Which type of machine learning is this?', main, wr, f'{main}: {why}.')


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step')
def ml_compare(rng, slot):
    a, b = rng.sample(_ML_SCEN, 2)
    return dict(stem=f'Compare the machine-learning approaches needed for these two applications, referring to the data each requires and how each model is trained.\nApplication 1: {a[0]}\nApplication 2: {b[0]}',
                answer=f'1: {a[1]} – {a[2]}. 2: {b[1]} – {b[2]}.',
                markingKey=f'Application 1 is {a[1]} because {a[2]} (2). Application 2 is {b[1]} because {b[2]} (2). Comparison of data needed (labelled/unlabelled/reward signal) and training process (fit to labels / discover structure / trial-and-error with rewards) (2).', marks=6)


R.facts('ch05-st1', F(
    terms=[('machine learning', 'a branch of artificial intelligence in which systems improve at a task by learning patterns from data rather than following explicitly programmed rules'),
           ('supervised learning', 'learning a mapping from inputs to outputs using training data in which every example is labelled with the correct output'),
           ('unsupervised learning', 'learning patterns or structure, such as clusters or associations, from data that has no labels'),
           ('reinforcement learning', 'learning by an agent that takes actions in an environment and receives rewards or penalties, aiming to maximise cumulative reward'),
           ('label', 'the known correct output (target) attached to a training example in supervised learning'),
           ('feature', 'a measurable input property of the data used by a model, such as age or pixel brightness'),
           ('semi-supervised learning', 'learning from a small amount of labelled data together with a large amount of unlabelled data'),
           ('training data', 'the examples used to fit a model\'s parameters')],
    why=[('Explain why supervised learning needs labelled data.', 'The algorithm adjusts its parameters by comparing its predictions with the correct answers; without labels there is no target to measure error against.'),
         ('Explain why reinforcement learning suits game playing and robotics.', 'There is often no labelled "correct move" for every situation, but outcomes (win/lose, task completed) give a reward signal; the agent can learn a strategy through repeated trial and error.'),
         ('Explain why unsupervised learning is useful when labels are expensive.', 'Labelling large datasets needs human experts and time; unsupervised methods can still find useful structure (segments, anomalies, compressed features) in unlabelled data.'),
         ('Explain why classification and regression are both forms of supervised learning.', 'Both learn from labelled examples; they differ only in the type of output – a discrete class for classification, a continuous value for regression.')],
    contrast=[('supervised learning', 'unsupervised learning', 'Supervised learning trains on labelled data to predict known outputs; unsupervised learning finds structure in unlabelled data without target outputs.'),
              ('classification', 'regression', 'Classification predicts a discrete category (spam/not spam); regression predicts a continuous numerical value (price).'),
              ('reinforcement learning', 'supervised learning', 'Supervised learning is told the correct output for each example; reinforcement learning only receives a reward signal after actions and must discover good actions by exploration.')],
    misc=[('Unsupervised learning means no human is involved at all.', 'Humans still choose the data, features, algorithm and parameters (e.g. k in k-means) and interpret the clusters; only the labels are absent.'),
          ('Reinforcement learning is supervised learning with rewards as labels.', 'Rewards are delayed and evaluate sequences of actions, not correct answers for each input; the agent must balance exploration and exploitation.'),
          ('A machine-learning model follows rules written by its programmer.', 'The programmer writes the learning algorithm; the decision rules (parameters) are learned from data.')],
    evaluate=[('Supervised learning is always more accurate than unsupervised learning.', ['labels give a clear objective and measurable accuracy', 'well-suited to prediction tasks'], ['the two solve different problems so accuracy is not directly comparable', 'supervised models are limited by label quality and quantity', 'unsupervised learning can reveal unknown patterns'], 'The comparison is misplaced: the choice depends on the task and on whether reliable labels exist.')],
))
ar('ch05-st1', [
    ('Predicting house prices is a regression task.', 'The output is a continuous numerical value.', 0, 'Both true; R explains A.'),
    ('k-means clustering is a supervised learning algorithm.', 'k-means needs the number of clusters k to be chosen.', 3, 'A is false (unsupervised); R is true.'),
    ('A reinforcement-learning agent needs labelled examples of correct actions.', 'It learns from rewards received after actions.', 3, 'A is false; R is true.'),
    ('Spam filtering is usually supervised learning.', 'Users\' "mark as spam" actions provide labels.', 0, 'Both true; R explains A.'),
])


@R.add('ch05-st2', 'C3', (2, 5), 'numerical')
def model_memory(rng, slot):
    p = rng.choice([7, 13, 70, 175, 1.5, 3])  # billion parameters
    prec = rng.choice([('32-bit floating point', 4), ('16-bit floating point', 2), ('8-bit integers', 1)])
    gb = p * 1e9 * prec[1] / 1e9
    gpu = rng.choice([16, 24, 40, 80])
    n_gpu = math.ceil(gb / gpu)
    ans = f'{p} × 10⁹ × {prec[1]} B = {r2(gb)} GB; needs at least {n_gpu} GPU(s) with {gpu} GB each (weights only).'
    extra = ' Suggest two ways to run the model on a smaller device.' if slot.d >= 4 else ''
    return dict(stem=f'A language model has {p} billion parameters stored as {prec[0]} ({prec[1]} byte(s) each). Calculate the memory needed just to hold the parameters, and the minimum number of {gpu} GB GPUs required.{extra}',
                answer=ans, markingKey=ans + (' Ways: quantisation to fewer bits, pruning, knowledge distillation into a smaller model, offloading layers.' if extra else '') + ' M1 parameters × bytes; A1 GB; A1 number of GPUs (rounded up).', marks=3 if slot.d <= 3 else 5)


@R.add('ch05-st2', 'C3', (2, 5), 'numerical')
def train_time(rng, slot):
    flops = rng.choice([1e20, 5e20, 2e21, 6e21])
    per = rng.choice([(100e12, 'GPU'), (300e12, 'GPU'), (1000e12, 'accelerator')])
    n = rng.choice([8, 16, 64, 256])
    util = rng.choice([0.3, 0.4, 0.5])
    secs = flops / (n * per[0] * util)
    hours = secs / 3600
    ex = math.floor(math.log10(secs))
    ans = f'{secs / 10 ** ex:.2f} × 10^{ex} s ≈ {hours:.3g} hours ≈ {hours / 24:.3g} days'
    e = f'{flops:.0e}'.replace('e+', ' × 10^')
    return dict(stem=f'Training a model requires {e} floating-point operations. The team uses {n} {per[1]}s, each with a peak of {int(per[0] / 1e12)} TFLOP/s, running at {int(util * 100)}% utilisation. Estimate the training time.',
                answer=ans, markingKey=f'Effective rate = {n} × {int(per[0] / 1e12)} × 10¹² × {util} FLOP/s (M1); time = total ÷ rate (M1) = {ans} (A1).', marks=3)


R.facts('ch05-st2', F(
    terms=[('GPU', 'a graphics processing unit: a processor with thousands of simple cores that perform the same operation on many data items in parallel, ideal for the matrix operations in ML'),
           ('TPU', 'a tensor processing unit: an application-specific chip designed by Google to accelerate neural-network tensor operations'),
           ('edge computing', 'running processing, such as ML inference, on or near the device where data is produced rather than in a distant data centre'),
           ('inference', 'using a trained model to make predictions on new data'),
           ('training', 'the computationally intensive process of adjusting a model\'s parameters using data'),
           ('FPGA', 'a field-programmable gate array: reconfigurable hardware that can be programmed to implement a specific ML pipeline with low latency'),
           ('cloud computing (for ML)', 'renting remote, scalable compute and storage (e.g. GPU clusters) over the internet to train or serve models')],
    facts=[('Why are GPUs preferred to CPUs for training neural networks?', 'They perform many matrix multiplications in parallel', ['They have higher clock speeds', 'They use less memory', 'They can only run Python'], 'Massive parallelism suits matrix maths.'),
           ('Which application is the best example of ML at the edge?', 'Face unlock processed on a smartphone', ['Training a language model in a data centre', 'A bank\'s overnight batch credit scoring', 'Storing photos in cloud backup'], 'Inference runs on the device itself.'),
           ('Which ML application analyses medical scans to highlight possible tumours?', 'Computer vision (image classification/segmentation)', ['Association rule mining', 'Linear regression of prices', 'Reinforcement learning for games'], 'Image analysis is computer vision.')],
    why=[('Explain why many ML applications run inference on edge devices rather than in the cloud.', 'Lower latency (no network round trip), works offline, keeps personal data on the device (privacy), and reduces bandwidth and server cost; the trade-off is limited device memory and power.'),
         ('Explain why training a large model needs far more computing power than using it.', 'Training repeats forward and backward passes over the whole dataset many times (epochs) to adjust millions or billions of parameters, while inference is a single forward pass per input.'),
         ('Explain why cloud computing is attractive to a start-up developing ML products.', 'It can rent powerful GPUs/TPUs on demand without large capital expenditure, scale up for training and down afterwards, and use managed ML services.')],
    contrast=[('a CPU', 'a GPU', 'A CPU has a few powerful cores optimised for sequential, varied tasks; a GPU has thousands of simpler cores optimised for the same operation on many data items in parallel.'),
              ('training', 'inference', 'Training fits the model\'s parameters using large datasets and is compute-intensive; inference applies the trained model to new inputs and is relatively cheap.'),
              ('cloud ML', 'edge ML', 'Cloud ML runs on remote, powerful servers (scalable, needs connectivity); edge ML runs on local devices (low latency, private, limited resources).')],
    misc=[('Any ML model can run on a smartwatch if the code is efficient.', 'Large models need more memory and compute than a watch has; they must be compressed (quantised, pruned, distilled) or run in the cloud.'),
          ('More hardware always makes training proportionally faster.', 'Communication between devices, memory bandwidth and parts of the algorithm that cannot be parallelised limit speed-up (Amdahl\'s law).'),
          ('Machine learning is only used by technology companies.', 'It is used in healthcare (diagnosis), agriculture (yield prediction), finance (fraud detection), transport (demand forecasting), retail (recommendations) and many other sectors.')],
    evaluate=[('Specialised hardware such as TPUs will make general-purpose GPUs obsolete for machine learning.', ['TPUs give higher performance per watt for tensor operations', 'large providers deploy them at scale'], ['GPUs are flexible, widely available and supported by all ML frameworks', 'new model types may not suit fixed-function chips', 'cost and vendor lock-in'], 'Specialised chips will take an increasing share of large-scale workloads, but GPUs remain important because of flexibility and ecosystem support.')],
))
_ML_APPS = [
    ('A hospital in Bogotá wants to detect pneumonia on chest X-rays.', 'labelled chest X-ray images (pneumonia / normal)', 'a probability or class label for each new X-ray', 'supervised classification with a convolutional neural network', 'GPU cluster or cloud GPUs for training on large image sets; inference on hospital servers or radiology workstations'),
    ('A farming cooperative in Kenya wants to predict maize yields for each field.', 'historical yields with rainfall, temperature, soil and fertiliser data per field', 'a predicted yield in tonnes per hectare', 'supervised regression', 'modest: training on a cloud CPU/GPU; inference on a phone app, possibly offline at the edge'),
    ('A bank in Toronto wants to detect fraudulent card payments in real time.', 'transaction amount, location, time, merchant and customer history, with past fraud labels', 'a fraud score / flag for each transaction within milliseconds', 'supervised classification (plus unsupervised anomaly detection for new fraud types)', 'low-latency servers close to the payment system; GPUs or CPUs for periodic retraining'),
    ('A city council in Seoul wants to reduce traffic congestion at junctions.', 'live vehicle counts and queue lengths from cameras and road sensors', 'traffic-light timings chosen to minimise waiting time', 'reinforcement learning (agent rewarded for reducing delay), trained first in simulation', 'edge devices at junctions for real-time control; simulation training on cloud GPUs'),
    ('An online retailer in Dubai wants to recommend products to shoppers.', 'browsing and purchase histories, ratings and product attributes', 'a ranked list of products likely to interest each shopper', 'unsupervised/collaborative filtering or supervised ranking models', 'distributed cloud servers to train on large interaction data and serve recommendations at scale'),
    ('A wildlife charity in Nairobi wants to count elephants in drone footage.', 'drone images with elephants labelled by bounding boxes', 'the number and location of elephants in each image', 'supervised object detection (deep learning)', 'GPUs for training; on-drone edge accelerator or field laptop for inference with poor connectivity'),
]


@R.add('ch05-st2', 'C3', (2, 5), 'short')
def ml_app(rng, slot):
    ctx, inp, out, kind, hw = rng.choice(_ML_APPS)
    q = rng.choice([
        ('Describe how machine learning could be applied, stating the input data, the output of the model and the type of learning.', f'Input: {inp}. Output: {out}. Type: {kind}.', 3),
        ('Outline the hardware requirements for training and for deploying the model.', f'{hw}.', 3),
        ('Explain how a model for this application would be developed, from data to deployment, and the hardware it would need.', f'Collect and clean {inp}; train a {kind} model; evaluate on held-out data; deploy to produce {out}. Hardware: {hw}.', 5),
    ])
    return dict(stem=f'{ctx} {q[0]}', answer=q[1], markingKey=q[1] + ' Marks for each relevant, context-specific point.', marks=q[2] if slot.d <= 4 else q[2] + 1)


@R.add('ch05-st3', 'C3', (2, 5), 'numerical')
def mlp_params(rng, slot):
    k = 3 if slot.d <= 2 else 4 if slot.d <= 4 else 5
    sizes = [rng.choice([4, 8, 10, 16, 784, 64])] + [rng.choice([8, 16, 32, 64, 128]) for _ in range(k - 2)] + [rng.choice([1, 2, 3, 10])]
    parts = [sizes[i] * sizes[i + 1] + sizes[i + 1] for i in range(len(sizes) - 1)]
    tot = sum(parts)
    ans = f'{tot} parameters ({" + ".join(f"{sizes[i]}×{sizes[i + 1]} + {sizes[i + 1]}" for i in range(len(sizes) - 1))})'
    return dict(stem=f'A fully connected neural network has layer sizes {" → ".join(map(str, sizes))} (input → hidden → output). Every neuron after the input layer has a bias. Calculate the total number of trainable parameters.',
                answer=ans, markingKey=f'Weights between layers: in × out; biases: one per non-input neuron (M1). Totals per layer: {", ".join(map(str, parts))} (M1); total {tot} (A1).', marks=3)


@R.add('ch05-st3', 'C3', (3, 5), 'numerical')
def cnn_params(rng, slot):
    kk = rng.choice([3, 5])
    cin = rng.choice([1, 3])
    cout = rng.choice([8, 16, 32])
    H = rng.choice([28, 32, 64])
    conv = (kk * kk * cin + 1) * cout
    out = H - kk + 1
    dense_in = out * out * cout
    dense = dense_in * 10 + 10
    ans = f'Conv layer: ({kk}×{kk}×{cin} + 1) × {cout} = {conv}; output {out}×{out}×{cout}; dense layer to 10 classes: {dense_in}×10 + 10 = {dense}.'
    return dict(stem=f'A convolutional layer applies {cout} filters of size {kk}×{kk} (stride 1, no padding) to a {H}×{H}×{cin} image; each filter has one bias. Its output is flattened into a dense layer with 10 outputs. Calculate the number of parameters in the convolutional layer, the output size of the convolution, and the parameters in the dense layer. Comment on what this shows about convolution.',
                answer=ans + ' Convolution shares weights across the image, so it has far fewer parameters than a dense layer.',
                markingKey=ans + ' A1 each; R1 weight sharing / local connectivity.', marks=4)


R.facts('ch05-st3', F(
    terms=[('artificial intelligence (AI)', 'the broad field of building computer systems that perform tasks normally requiring human intelligence, such as reasoning, perception and language'),
           ('deep learning', 'a subset of machine learning that uses artificial neural networks with many hidden layers to learn hierarchical features directly from raw data'),
           ('artificial neural network', 'a model made of layers of connected artificial neurons, each computing a weighted sum of its inputs plus a bias passed through an activation function'),
           ('hidden layer', 'a layer of neurons between the input and output layers whose values are not directly observed'),
           ('convolutional neural network (CNN)', 'a deep network that uses convolutional filters with shared weights to detect local patterns, used mainly for images'),
           ('activation function', 'a non-linear function, such as ReLU or sigmoid, applied to a neuron\'s weighted sum so that the network can model non-linear relationships'),
           ('large language model (LLM)', 'a very large deep-learning model, usually a transformer, trained on vast text corpora to predict and generate language')],
    facts=[('Which statement correctly describes the relationship between AI, ML and DL?', 'DL ⊂ ML ⊂ AI', ['AI ⊂ ML ⊂ DL', 'ML ⊂ DL ⊂ AI', 'They are three unrelated fields'], 'Deep learning is a kind of ML, which is a kind of AI.'),
           ('Which feature distinguishes deep learning from classical machine learning?', 'It learns features automatically through many layers', ['It never needs data', 'It uses only decision trees', 'It cannot run on GPUs'], 'Feature learning across many layers is the key idea.'),
           ('A rule-based expert system for diagnosing faults in a car is an example of…', 'AI that is not machine learning', ['deep learning', 'unsupervised learning', 'a convolutional network'], 'Hand-written rules are AI but involve no learning from data.')],
    why=[('Explain why deep learning needs large datasets.', 'Deep networks have very many parameters; with little data they memorise the training set (overfit) instead of learning general features, so many examples are needed to constrain the parameters.'),
         ('Explain why activation functions must be non-linear.', 'A stack of linear layers is equivalent to one linear layer, so without non-linearity extra layers add no representational power; non-linear activations let the network model complex relationships.'),
         ('Explain why deep learning models are described as "black boxes".', 'Their decisions emerge from millions of learned weights across many layers, so it is hard to explain which features caused a particular output, unlike a decision tree\'s readable rules.')],
    contrast=[('machine learning', 'deep learning', 'Classical ML often relies on hand-engineered features and simpler models; deep learning uses many-layered neural networks that learn features automatically from raw data, needing more data and compute.'),
              ('artificial intelligence', 'machine learning', 'AI is the broad goal of making machines perform intelligent tasks (including rule-based systems); ML is the subset of AI in which behaviour is learned from data.'),
              ('a shallow neural network', 'a deep neural network', 'A shallow network has one (or very few) hidden layers; a deep network has many, allowing it to build hierarchical representations.')],
    misc=[('All artificial intelligence is machine learning.', 'Rule-based expert systems, search and planning algorithms are AI without learning from data.'),
          ('Adding more layers always makes a neural network better.', 'More layers increase capacity but also the risk of overfitting, training instability (vanishing gradients) and cost; depth must suit the data.'),
          ('Deep learning works like a human brain.', 'Artificial neurons are loosely inspired by biology but are simple mathematical functions; networks learn very differently from brains.')],
    evaluate=[('Deep learning is the best approach for every machine-learning problem.', ['state-of-the-art for images, speech and language', 'learns features automatically'], ['needs large labelled datasets and expensive hardware', 'hard to interpret – a problem in regulated areas', 'simpler models (regression, trees) perform as well on small tabular data'], 'No: deep learning excels on large unstructured data; for small or tabular datasets and where explanations are required, simpler models are often better.')],
))
ar('ch05-st3', [
    ('Deep learning is a subset of machine learning.', 'Deep-learning models learn their parameters from data.', 0, 'Both true; learning from data is what makes DL a form of ML.'),
    ('A neural network with only linear activations can model any non-linear function.', 'Composing linear functions gives another linear function.', 3, 'A is false; R is true and explains why.'),
    ('CNNs are well suited to image recognition.', 'Convolutional filters detect local patterns anywhere in the image using shared weights.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# ch06 A4.2 Data preprocessing (HL)
# =============================================================================================
def _quart(xs):
    s = sorted(xs)
    n = len(s)
    def med(a):
        m = len(a)
        return a[m // 2] if m % 2 else (a[m // 2 - 1] + a[m // 2]) / 2
    lower = s[: n // 2]
    upper = s[(n + 1) // 2:]
    return med(lower), med(s), med(upper)


@R.add('ch06-st1', 'C3', (1, 5), 'numerical')
def impute(rng, slot):
    feat = rng.choice([('daily temperature (°C) from a weather station in Oslo', 'temp'), ('household income (k$) in a survey in Lima', 'income'), ('resting heart rate (bpm) from a fitness app', 'hr'), ('exam score of students in Seoul', 'score')])
    n = 7 if slot.d <= 3 else 9
    vals = [rng.randint(10, 40) if feat[1] == 'temp' else rng.randint(20, 90) for _ in range(n)]
    oi = rng.randrange(n)
    if slot.d >= 3:
        vals[oi] = max(vals) * rng.choice([4, 5, 6])
    miss = rng.sample([i for i in range(n) if i != oi], 2)
    shown = ['?' if i in miss else str(v) for i, v in enumerate(vals)]
    known = [v for i, v in enumerate(vals) if i not in miss]
    mean = sum(known) / len(known)
    s = sorted(known)
    med = s[len(s) // 2] if len(s) % 2 else (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2
    which = 'median' if slot.d >= 3 else rng.choice(['mean', 'median'])
    ans = f'mean of known values = {r2(mean)}; median = {r2(med)}.'
    if slot.d >= 3:
        ans += f' The median ({r2(med)}) is the better choice because the outlier {max(known)} pulls the mean up.'
    return dict(stem=f'A dataset of {feat[0]} has missing values (?): {", ".join(shown)}. Calculate the mean and the median of the known values' + (' and justify which should be used to impute the missing values.' if slot.d >= 3 else f', and state the value that would replace each ? using {which} imputation.'),
                answer=ans + ('' if slot.d >= 3 else f' Each ? becomes {r2(mean) if which == "mean" else r2(med)}.'),
                markingKey=f'Known values: {", ".join(map(str, known))} (M1). {ans} A1 each; R1 justification (median is robust to outliers).', marks=3 if slot.d <= 3 else 4)


@R.add('ch06-st1', 'C3', (1, 4), 'numerical')
def minmax(rng, slot):
    vals = sorted(rng.sample(range(5, 200), 5))
    x = rng.choice(vals[1:-1])
    lo, hi = vals[0], vals[-1]
    mm = (x - lo) / (hi - lo)
    mu = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - mu) ** 2 for v in vals) / len(vals))
    z = (x - mu) / sd
    feat = rng.choice(['floor area (m²)', 'monthly data usage (GB)', 'distance to school (km × 10)', 'number of daily steps (hundreds)'])
    if slot.d <= 2:
        return dict(stem=f'The feature {feat} takes the values {", ".join(map(str, vals))}. Using min-max normalisation to the range [0, 1], calculate the normalised value of {x}.',
                    answer=r2(mm, 3), markingKey=f'(x − min)/(max − min) = ({x} − {lo})/({hi} − {lo}) = {r2(mm, 3)}. M1 A1.', marks=2)
    return dict(stem=f'The feature {feat} has values {", ".join(map(str, vals))}. (a) Min-max normalise {x}. (b) Standardise {x} as a z-score using the population standard deviation. (c) Explain why k-nearest neighbours needs features to be scaled.',
                answer=f'(a) {r2(mm, 3)} (b) mean {r2(mu)}, σ {r2(sd)}, z = {r2(z, 3)} (c) distance-based: features with large ranges would dominate the distance.',
                markingKey=f'(a) ({x} − {lo})/({hi} − {lo}) = {r2(mm, 3)} [2] (b) μ = {r2(mu)}, σ = {r2(sd)}, z = ({x} − μ)/σ = {r2(z, 3)} [2] (c) Euclidean distance is dominated by the feature with the largest scale [1].', marks=5)


@R.add('ch06-st1', 'C3', (2, 5), 'numerical')
def iqr_outliers(rng, slot):
    n = rng.choice([9, 11])
    vals = [rng.randint(30, 60) for _ in range(n - 2)] + [rng.randint(95, 140), rng.choice([rng.randint(0, 8), rng.randint(40, 50)])]
    rng.shuffle(vals)
    q1, q2, q3 = _quart(vals)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outs = sorted(v for v in vals if v < lo or v > hi)
    ctx = rng.choice(['delivery times (minutes) for a food app in Accra', 'sensor readings from a soil-moisture probe', 'ages entered on a sign-up form', 'response times (ms) of a web server'])
    ans = f'Q1 = {r2(q1)}, Q3 = {r2(q3)}, IQR = {r2(iqr)}; fences {r2(lo)} and {r2(hi)}; outliers: {", ".join(map(str, outs)) if outs else "none"}.'
    return dict(stem=f'The following {ctx} are being cleaned: {", ".join(map(str, vals))}. Using the 1.5 × IQR rule (quartiles found as medians of the lower and upper halves, excluding the median when n is odd), identify any outliers, and discuss whether they should be removed.',
                answer=ans, markingKey=ans + ' M1 sorted data/quartiles; A1 IQR and fences; A1 outliers. R1: remove only if errors (e.g. impossible values); genuine extreme values may carry information (e.g. real delays).', marks=4)


@R.add('ch06-st1', 'C3', (1, 3), 'short')
def dedupe(rng, slot):
    names = rng.sample(PEOPLE, 5)
    rows = []
    for nm in names:
        rows.append((nm, rng.choice(CITIES), rng.randint(18, 70)))
    k = rng.randint(1, 3)
    for _ in range(k):
        rows.append(rng.choice(rows[:5]))
    rng.shuffle(rows)
    uniq = len(set(rows))
    return dict(stem=f'A customer dataset contains these records (Name, City, Age):\n{table(["Name", "City", "Age"], rows)}\nHow many exact duplicate rows must be removed, and how many records remain? Explain why duplicates harm a model.',
                answer=f'{len(rows) - uniq} duplicates removed; {uniq} records remain. Duplicates over-weight some examples, bias the model and can leak between training and test sets.',
                markingKey=f'{len(rows) - uniq} duplicates (A1); {uniq} remain (A1); R1 bias/over-weighting/leakage.', marks=3)


R.facts('ch06-st1', F(
    terms=[('data cleaning', 'detecting and correcting or removing incorrect, incomplete, inconsistent, duplicated or irrelevant data before training a model'),
           ('imputation', 'replacing missing values with estimated values such as the mean, median, mode or a model prediction'),
           ('outlier', 'a data point that lies far from the other observations, which may be an error or a genuine extreme value'),
           ('normalisation (min-max scaling)', 'rescaling a feature to a fixed range, usually [0, 1], using (x − min)/(max − min)'),
           ('standardisation (z-score)', 'rescaling a feature to mean 0 and standard deviation 1 using (x − μ)/σ'),
           ('noise', 'random errors or irrelevant variation in data that do not represent the underlying pattern')],
    facts=[('Which method of filling missing values is least affected by outliers?', 'Median imputation', ['Mean imputation', 'Replacing with the maximum', 'Replacing with zero'], 'The median is robust to extreme values.'),
           ('Which value is the min-max normalised value of the minimum of a feature?', '0', ['1', '0.5', 'It depends on the mean'], '(min − min)/(max − min) = 0.'),
           ('Which is the most appropriate way to handle the category "Kenya" written as "kenya", "KENYA" and "Kenya " in a dataset?', 'Standardise case and trim whitespace so they become one category', ['Delete all three rows', 'Treat them as three different countries', 'Replace them with the mean'], 'Inconsistent formatting should be standardised.')],
    why=[('Explain why features should be scaled before training a k-nearest neighbours model.', 'k-NN uses distances; a feature with a large range (e.g. income in dollars) would dominate one with a small range (e.g. age), so scaling gives each feature comparable influence.'),
         ('Explain why simply deleting every row with a missing value can be a poor strategy.', 'It can discard a large share of the data and, if values are not missing at random, it biases the sample (e.g. removing all low-income respondents who skipped a question).'),
         ('Explain why the statistics used for scaling must be calculated on the training set only.', 'Using test data to compute means or min/max leaks information about the test set into training, giving over-optimistic evaluation results.'),
         ('Explain why outliers should not automatically be deleted.', 'Some outliers are genuine and informative (fraud, rare diseases); removing them hides important cases. Only errors (impossible values, typos) should be removed or corrected.')],
    contrast=[('normalisation', 'standardisation', 'Normalisation rescales values to a fixed range such as [0, 1] using min and max; standardisation transforms values to mean 0 and standard deviation 1, and is less affected by a single extreme value.'),
              ('mean imputation', 'median imputation', 'Mean imputation fills gaps with the average, which is pulled by outliers; median imputation uses the middle value, which is robust to outliers.'),
              ('an outlier', 'noise', 'An outlier is an individual point far from the rest; noise is general random variation spread through the data.')],
    misc=[('Normalising the data changes the relationships between the examples.', 'Linear rescaling preserves the order and relative spacing of values within a feature; it only changes the units/scale.'),
          ('Mean imputation has no effect on the model.', 'It reduces the variance of the feature and can weaken correlations, biasing the model; flagging missingness can help.'),
          ('Data cleaning is only needed for small datasets.', 'Large datasets usually contain more errors, duplicates and inconsistencies; "garbage in, garbage out" applies at any scale.')],
    evaluate=[('Data cleaning is the most important stage of a machine-learning project.', ['model quality is limited by data quality', 'practitioners report most time is spent on preparation', 'errors and bias in data propagate into predictions'], ['algorithm choice, features and evaluation also matter', 'over-cleaning can remove genuine signal', 'the importance depends on the data source'], 'It is among the most important stages because no algorithm can compensate for poor data, but it must be balanced with sound modelling and evaluation.')],
))
ar('ch06-st1', [
    ('Median imputation is preferred to mean imputation for skewed data.', 'The median is not pulled by extreme values.', 0, 'Both true; R explains A.'),
    ('Min-max normalisation always produces values between 0 and 1 for new data.', 'It uses the minimum and maximum of the training data.', 3, 'A is false – new values outside the training range map outside [0, 1]; R is true and explains why.'),
    ('Duplicate records should be removed before splitting data into training and test sets.', 'Otherwise the same example may appear in both sets, inflating test accuracy.', 0, 'Both true; R explains A.'),
])


def _pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)


@R.add('ch06-st2', 'C3', (2, 5), 'numerical')
def corr_select(rng, slot):
    n = 6
    y = [rng.randint(20, 90) for _ in range(n)]
    f1 = [round(v / 10 + rng.uniform(-1, 1), 1) for v in y]
    f2 = [rng.randint(1, 9) for _ in range(n)]
    f3 = [round(100 - v + rng.uniform(-8, 8)) for v in y]
    rs = {'StudyHours': _pearson(f1, y), 'ShoeSize': _pearson(f2, y), 'PhoneHours': _pearson(f3, y)}
    rows = [(f1[i], f2[i], f3[i], y[i]) for i in range(n)]
    keep = [k for k, v in rs.items() if abs(v) >= 0.5]
    ans = '; '.join(f'r({k}, Score) = {v:.3f}' for k, v in rs.items()) + f'. Keep: {", ".join(keep) if keep else "none"} (|r| ≥ 0.5).'
    if slot.d <= 3:
        stem = f'A school in Kuala Lumpur wants to predict exam Score. The data are:\n{table(["StudyHours", "ShoeSize", "PhoneHours", "Score"], rows)}\nThe Pearson correlation of each feature with Score is: ' + ', '.join(f'{k} {v:.3f}' for k, v in rs.items()) + '. Using a threshold of |r| ≥ 0.5, state which features should be selected and justify.'
    else:
        stem = f'A school in Kuala Lumpur wants to predict exam Score. The data are:\n{table(["StudyHours", "ShoeSize", "PhoneHours", "Score"], rows)}\nCalculate the Pearson correlation coefficient between ShoeSize and Score, and hence, using |r| ≥ 0.5 (given r = {rs["StudyHours"]:.3f} for StudyHours and {rs["PhoneHours"]:.3f} for PhoneHours), select features. Explain one limitation of correlation-based selection.'
    return dict(stem=stem, answer=ans, markingKey=ans + ' Limitation: correlation only captures linear, one-feature-at-a-time relationships; it misses interactions and non-linear effects, and correlation is not causation.', marks=3 if slot.d <= 3 else 5)


@R.add('ch06-st2', 'C3', (1, 4), 'short')
def one_hot(rng, slot):
    cats = rng.sample(['Lima', 'Oslo', 'Accra', 'Hanoi', 'Seoul', 'Lisbon'], rng.randint(3, 5))
    rows = [rng.choice(cats) for _ in range(5)]
    order = sorted(set(cats))
    enc = '; '.join(f'{r} → [' + ', '.join('1' if r == c else '0' for c in order) + ']' for r in rows)
    extra_feats = rng.randint(2, 6)
    tot = extra_feats + len(order)
    return dict(stem=f'A model uses the feature City with possible values {", ".join(cats)} plus {extra_feats} numerical features. Using one-hot encoding with columns in alphabetical order ({", ".join(order)}), encode the rows {", ".join(rows)}, and state how many input features the model will have. Explain why label encoding (Lima = 1, Oslo = 2, …) could mislead a linear model.',
                answer=f'{enc}. Total features = {extra_feats} + {len(order)} = {tot}. Label encoding implies an order/size between cities that does not exist.',
                markingKey=f'Encodings: {enc} (A2). Feature count {tot} (A1). R1 artificial ordering.', marks=4)


@R.add('ch06-st2', 'C3', (1, 4), 'numerical')
def feat_eng(rng, slot):
    kind = rng.choice(['bmi', 'speed', 'ratio', 'age'])
    if kind == 'bmi':
        m, h = rng.randint(45, 110), rng.choice([1.55, 1.62, 1.70, 1.78, 1.85])
        v = m / h ** 2
        return dict(stem=f'A health model in Mumbai has raw features mass = {m} kg and height = {h} m. Engineer the feature BMI = mass / height² for this patient and explain why an engineered feature can improve a model.',
                    answer=f'BMI = {m}/{h}² = {v:.1f}. It combines two raw features into one that is more directly related to the target, so simpler models can use it.',
                    markingKey=f'{m}/{h}² = {v:.1f} (M1 A1); R1 domain knowledge captures a relationship the model would otherwise need to learn.', marks=3)
    if kind == 'speed':
        d, t = rng.randint(3, 42), rng.randint(15, 240)
        v = d / (t / 60)
        return dict(stem=f'A running app records distance = {d} km and duration = {t} min. Create the engineered feature average speed (km/h) and suggest one further feature that could help predict injury risk.',
                    answer=f'{d}/({t}/60) = {v:.2f} km/h. Further feature: e.g. weekly distance change, pace variability.',
                    markingKey=f'Convert minutes to hours (M1); {v:.2f} km/h (A1); sensible additional engineered feature (R1).', marks=3)
    if kind == 'ratio':
        debt, inc = rng.randint(5, 80), rng.randint(20, 120)
        v = debt / inc
        return dict(stem=f'A lender\'s dataset has Debt = {debt} k$ and Income = {inc} k$ for an applicant. Engineer a debt-to-income ratio and explain why it may predict default better than either raw feature.',
                    answer=f'{debt}/{inc} = {v:.3f}. It measures affordability relative to income: the same debt is riskier for a lower income.',
                    markingKey=f'{v:.3f} (A1); R1 relative measure; R1 reduces dependence on scale.', marks=3)
    y = rng.randint(1950, 2010)
    return dict(stem=f'A dataset stores DateOfBirth (e.g. {y}-06-15) but a model needs numerical inputs. Describe how to engineer an Age feature on 2026-01-01 for this example and why raw dates are unsuitable inputs.',
                answer=f'Age = 2026 − {y} − 1 = {2026 - y - 1} (birthday not yet reached on 1 January). Raw date strings are not numerical and their format has no meaningful scale for the model.',
                markingKey=f'Age {2026 - y - 1} (A1) with birthday adjustment (M1); R1 explanation.', marks=3)


R.facts('ch06-st2', F(
    terms=[('feature selection', 'choosing the subset of available features that are most relevant to the target, discarding irrelevant or redundant ones'),
           ('feature engineering', 'creating new, more informative features from raw data using domain knowledge, such as ratios, counts or date parts'),
           ('one-hot encoding', 'representing a categorical feature with one binary column per category, set to 1 for the category present and 0 otherwise'),
           ('filter method', 'a feature-selection approach that ranks features by a statistic (e.g. correlation, chi-squared) independent of any model'),
           ('wrapper method', 'a feature-selection approach that evaluates subsets of features by training a model on each, e.g. forward selection or recursive feature elimination'),
           ('embedded method', 'a feature-selection approach where selection happens during model training, e.g. L1 (lasso) regularisation or tree feature importance')],
    why=[('Explain why removing irrelevant features can improve a model.', 'Irrelevant features add noise that the model may fit (overfitting), increase training time and memory, and make the model harder to interpret; fewer, relevant features generalise better.'),
         ('Explain why two highly correlated features may both not be needed.', 'They carry largely the same information (redundancy), so keeping both adds little predictive power, can destabilise some models (multicollinearity in regression) and increases dimensionality.'),
         ('Explain why wrapper methods are more computationally expensive than filter methods.', 'Wrapper methods train and evaluate a model for many candidate subsets of features, whereas filter methods compute a single statistic per feature.')],
    contrast=[('feature selection', 'feature engineering', 'Feature selection chooses among existing features; feature engineering creates new features from raw data.'),
              ('a filter method', 'a wrapper method', 'A filter method scores features independently of any model (fast); a wrapper method searches subsets using a model\'s performance (slower but accounts for interactions).'),
              ('one-hot encoding', 'label encoding', 'One-hot uses a binary column per category with no implied order; label encoding maps categories to integers, which implies an order and is suitable only for ordinal data.')],
    misc=[('A feature with zero correlation with the target is useless.', 'Pearson correlation only measures linear association; the feature may have a non-linear relationship or be useful in combination with others.'),
          ('More features always give a more accurate model.', 'Extra irrelevant or redundant features add noise and dimensionality, often causing overfitting and lower test accuracy.'),
          ('One-hot encoding is the best choice for a feature with 50 000 categories such as postcode.', 'It would create 50 000 sparse columns; alternatives such as grouping, target/frequency encoding or embeddings are more practical.')],
    evaluate=[('Domain experts should always be involved in feature engineering.', ['experts know which derived quantities matter (e.g. BMI, debt ratio)', 'helps avoid nonsensical or leaking features'], ['deep learning can learn features automatically from raw data', 'experts may carry biases or overlook unexpected patterns', 'cost and availability of experts'], 'Expert involvement is highly valuable, especially for tabular data and in sensitive domains, but should be combined with data-driven selection.')],
))
ar('ch06-st2', [
    ('One-hot encoding is suitable for nominal categories such as city names.', 'It does not impose an artificial order on the categories.', 0, 'Both true; R explains A.'),
    ('Filter methods consider interactions between features.', 'Filter methods evaluate each feature using a statistic independent of the model.', 3, 'A is false; R is true and explains why.'),
])


@R.add('ch06-st3', 'C3', (1, 5), 'numerical')
def curse_grid(rng, slot):
    bins = rng.choice([5, 10, 4])
    d1, d2 = rng.sample([1, 2, 3, 5, 8, 10], 2)
    d1, d2 = sorted((d1, d2))
    c1, c2 = bins ** d1, bins ** d2
    per = rng.choice([5, 10])
    ans = f'{bins}^{d1} = {c1} cells vs {bins}^{d2} = {c2} cells; for {per} samples per cell you need {per * c1} vs {per * c2} samples.'
    return dict(stem=f'Each feature is divided into {bins} intervals, so the feature space is split into cells. Compare the number of cells for {d1} feature(s) and {d2} features, and the number of training samples needed for about {per} samples per cell. Explain what this shows about the curse of dimensionality.',
                answer=ans + ' The data needed grows exponentially with dimensions, so data becomes sparse.',
                markingKey=ans + ' A1 each count; R1 exponential growth → sparsity, distances become less meaningful, more data or fewer dimensions needed.', marks=3 if slot.d <= 3 else 4)


@R.add('ch06-st3', 'C3', (2, 5), 'numerical')
def pca_var(rng, slot):
    k = rng.randint(4, 6)
    ev = sorted([round(rng.uniform(0.2, 9.0), 2) for _ in range(k)], reverse=True)
    tot = sum(ev)
    pct = [e / tot * 100 for e in ev]
    cum = list(itertools.accumulate(pct))
    th = rng.choice([80, 90, 95])
    need = next(i + 1 for i, c in enumerate(cum) if c >= th - 1e-9)
    ans = 'Explained variance: ' + ', '.join(f'PC{i + 1} {p:.1f}%' for i, p in enumerate(pct)) + f'; cumulative reaches {cum[need - 1]:.1f}% after {need} components, so keep {need}.'
    return dict(stem=f'Principal component analysis on a {k}-feature dataset gives eigenvalues (variances) {", ".join(map(str, ev))}. Calculate the percentage of variance explained by each component and the number of components needed to keep at least {th}% of the variance.',
                answer=ans, markingKey=f'Total variance {r2(tot)} (M1); each % = eigenvalue/total (A1); cumulative sums (M1); {need} components (A1).', marks=4)


R.facts('ch06-st3', F(
    terms=[('dimensionality', 'the number of features (input variables) used to describe each data point'),
           ('curse of dimensionality', 'the problems that arise as the number of features grows: data become sparse, distances lose meaning and the amount of data needed grows exponentially'),
           ('dimensionality reduction', 'reducing the number of features while keeping as much useful information as possible, by selection or by transformation (e.g. PCA)'),
           ('principal component analysis (PCA)', 'an unsupervised technique that transforms correlated features into a smaller set of uncorrelated principal components ordered by the variance they explain'),
           ('principal component', 'a new feature that is a linear combination of the original features, chosen to capture the maximum remaining variance'),
           ('t-SNE', 'a non-linear dimensionality-reduction technique used mainly to visualise high-dimensional data in two or three dimensions')],
    why=[('Explain why k-nearest neighbours performs poorly in very high-dimensional spaces.', 'As dimensions increase, the distances between all points become similar, so the "nearest" neighbours are hardly nearer than others and data become sparse; many irrelevant dimensions also add noise to the distance.'),
         ('Explain why dimensionality reduction can reduce overfitting.', 'With fewer features the model has fewer parameters to fit and less opportunity to learn noise, so it generalises better from a limited number of examples.'),
         ('Explain why the features should be standardised before PCA.', 'PCA finds directions of maximum variance; a feature measured on a large scale would dominate the components simply because of its units.')],
    contrast=[('feature selection', 'feature extraction (e.g. PCA)', 'Feature selection keeps a subset of the original features (still interpretable); feature extraction creates new combined features, which may be harder to interpret.'),
              ('PCA', 't-SNE', 'PCA is a linear method that preserves global variance and can transform new data; t-SNE is non-linear, preserves local neighbourhoods, and is used mainly for visualisation.')],
    misc=[('PCA selects the most important original features.', 'PCA creates new features (principal components) that are linear combinations of all the original features.'),
          ('Adding more features always helps a model distinguish between classes.', 'Beyond a point, extra features make the data sparse and increase overfitting (the curse of dimensionality / Hughes phenomenon).'),
          ('Dimensionality reduction never loses information.', 'Discarding low-variance components loses some information; the aim is to lose as little useful information as possible.')],
    evaluate=[('PCA should always be applied before training a model on high-dimensional data.', ['reduces dimensionality, training time and overfitting', 'removes correlated features', 'enables visualisation'], ['components are hard to interpret', 'variance is not the same as predictive relevance – useful low-variance features can be discarded', 'not suitable for non-linear structure'], 'PCA is a useful tool but not automatic: it should be evaluated against model performance and the need for interpretability.')],
))
ar('ch06-st3', [
    ('The first principal component explains the largest share of the variance.', 'PCA orders components by the variance they capture.', 0, 'Both true; R explains A.'),
    ('Increasing the number of features always reduces the amount of training data required.', 'The volume of the feature space grows exponentially with the number of dimensions.', 3, 'A is false; R is true and implies the opposite.'),
])


# =============================================================================================
# ch07 A4.3 Machine learning approaches
# =============================================================================================
_REG_CTX = [
    ('advertising spend (k$)', 'monthly sales (k$)', 'a sportswear shop in Toronto'),
    ('hours of revision', 'test score (%)', 'a school in Hanoi'),
    ('floor area (10 m²)', 'rent (100 €/month)', 'an estate agency in Lisbon'),
    ('daily temperature (°C)', 'ice creams sold (dozens)', 'a kiosk in Melbourne'),
    ('engine size (100 cc)', 'fuel use (L/100 km)', 'a car-review site in Seoul'),
    ('rainfall (cm)', 'maize yield (t/ha)', 'a farm near Nairobi'),
]


def _linreg(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    m = sxy / sxx
    c = my - m * mx
    return m, c, mx, my, sxy, sxx


@R.add('ch07-st1', 'C3', (1, 5), 'numerical')
def linreg_fit(rng, slot):
    xl, yl, ctx = rng.choice(_REG_CTX)
    n = 4 if slot.d <= 2 else 5 if slot.d <= 3 else 6
    xs = sorted(rng.sample(range(1, 15), n))
    a, b = rng.choice([1.5, 2, 2.5, 3, 4]), rng.randint(2, 20)
    ys = [round(a * x + b + rng.choice([-2, -1, 0, 1, 2])) for x in xs]
    m, c, mx, my, sxy, sxx = _linreg(xs, ys)
    x0 = rng.randint(xs[0], xs[-1] + 3)
    pred = m * x0 + c
    tb = table([xl, yl], list(zip(xs, ys)))
    if slot.d <= 2:
        return dict(stem=f'At {ctx}, a linear regression model y = {r2(m, 3)}x + {r2(c, 3)} was fitted, where x is {xl} and y is {yl}. Use the model to predict y when x = {x0}, and interpret the gradient.',
                    answer=f'y = {r2(m, 3)} × {x0} + {r2(c, 3)} = {r2(pred, 2)}. Each extra unit of x increases predicted y by {r2(m, 3)}.',
                    markingKey=f'Substitution (M1); {r2(pred, 2)} (A1); gradient interpreted in context (R1).', marks=3)
    resid = [y - (m * x + c) for x, y in zip(xs, ys)]
    mse = sum(e * e for e in resid) / n
    extra = f' Calculate the mean squared error of the model on these data.' if slot.d >= 4 else ''
    ans = f'm = Sxy/Sxx = {r2(sxy, 3)}/{r2(sxx, 3)} = {r2(m, 3)}; c = ȳ − m x̄ = {r2(my, 3)} − {r2(m, 3)} × {r2(mx, 3)} = {r2(c, 3)}; prediction at x = {x0}: {r2(pred, 2)}' + (f'; MSE = {r2(mse, 3)}' if extra else '')
    return dict(stem=f'At {ctx} the following data were collected:\n{tb}\nUsing least squares, find the regression line y = mx + c and predict y when x = {x0}.{extra}' + (' Comment on the reliability of this prediction.' if x0 > xs[-1] else ''),
                answer=ans, markingKey=ans + ('. R1: x is outside the data range, so this is extrapolation and less reliable.' if x0 > xs[-1] else '') + ' M1 means; M1 Sxy and Sxx; A1 m; A1 c; A1 prediction.', marks=4 if slot.d <= 3 else 6)


@R.add('ch07-st1', 'C3', (2, 4), 'numerical')
def residuals(rng, slot):
    xl, yl, ctx = rng.choice(_REG_CTX)
    m, c = rng.choice([1.5, 2, 2.5, 3]), rng.randint(1, 10)
    xs = rng.sample(range(1, 12), 4)
    ys = [round(m * x + c + rng.choice([-3, -2, -1, 1, 2, 3])) for x in xs]
    res = [y - (m * x + c) for x, y in zip(xs, ys)]
    mse = sum(e * e for e in res) / 4
    mae = sum(abs(e) for e in res) / 4
    return dict(stem=f'A model for {ctx} predicts {yl} as ŷ = {m}x + {c} where x is {xl}. For the data points ' + ', '.join(f'({x}, {y})' for x, y in zip(xs, ys)) + ' calculate the residuals, the mean absolute error and the mean squared error.',
                answer='Residuals ' + ', '.join(r2(e) for e in res) + f'; MAE = {r2(mae, 3)}; MSE = {r2(mse, 3)}',
                markingKey='Residual = y − ŷ (M1): ' + ', '.join(r2(e) for e in res) + f' (A1); MAE = {r2(mae, 3)} (A1); MSE = {r2(mse, 3)} (A1).', marks=4)


R.facts('ch07-st1', F(
    terms=[('linear regression', 'a supervised learning method that models a continuous target as a linear function of one or more features, y = mx + c'),
           ('least squares', 'the method of fitting a regression line by choosing parameters that minimise the sum of squared residuals'),
           ('residual', 'the difference between an observed value and the value predicted by the model, y − ŷ'),
           ('coefficient of determination (R²)', 'the proportion of the variation in the target that is explained by the model, from 0 to 1'),
           ('extrapolation', 'using a model to predict outside the range of the data it was trained on'),
           ('mean squared error (MSE)', 'the average of the squared residuals, used as the loss function for linear regression')],
    why=[('Explain why residuals are squared in least-squares regression.', 'Squaring makes all residuals positive so they do not cancel, penalises large errors more heavily, and gives a smooth function that can be minimised analytically or by gradient descent.'),
         ('Explain why extrapolation with a regression model is risky.', 'The linear relationship has only been observed within the data range; outside it the true relationship may change (saturation, limits), so predictions can be badly wrong.'),
         ('Explain why a high correlation does not prove that x causes y.', 'Both may be driven by a third (confounding) variable or the link may be coincidental; regression shows association, and causation needs controlled experiments or causal reasoning.')],
    contrast=[('linear regression', 'logistic regression', 'Linear regression predicts a continuous value; logistic regression predicts the probability of a class (classification) using a sigmoid function.'),
              ('interpolation', 'extrapolation', 'Interpolation predicts within the range of the training data (more reliable); extrapolation predicts outside it (less reliable).'),
              ('MAE', 'MSE', 'MAE averages absolute errors (same units as y, less sensitive to outliers); MSE averages squared errors (penalises large errors more).')],
    misc=[('An R² of 0.95 means the model is correct 95% of the time.', 'R² is the proportion of variance in y explained by the model; it says nothing about the percentage of correct predictions.'),
          ('A regression line must pass through the origin.', 'The intercept c is fitted from the data; the least-squares line passes through (x̄, ȳ), not necessarily (0, 0).'),
          ('If the residuals are large the gradient must be wrong.', 'Large residuals may come from noise or a non-linear relationship; the gradient can still be the best linear fit.')],
    evaluate=[('Linear regression is too simple to be useful in modern machine learning.', ['fast, interpretable, works with small data', 'a strong baseline and widely used in economics, science and business'], ['cannot model non-linear relationships without feature engineering', 'sensitive to outliers', 'assumes independent errors'], 'It remains very useful as an interpretable baseline and for approximately linear problems, but more flexible models are needed for complex non-linear data.')],
))
ar('ch07-st1', [
    ('The least-squares regression line passes through the point (x̄, ȳ).', 'The intercept is calculated as c = ȳ − m x̄.', 0, 'Both true; R explains A.'),
    ('Linear regression is an unsupervised learning method.', 'It is trained on examples that include the target value.', 3, 'A is false (supervised); R is true.'),
])


# ---- k-NN and decision trees ----
@R.add('ch07-st2', 'C3', (1, 5), 'numerical')
def knn(rng, slot):
    ctx = rng.choice([('fruit', 'mass (g)', 'sweetness', ['Apple', 'Orange']), ('patients', 'age', 'blood pressure index', ['Low risk', 'High risk']),
                      ('songs', 'tempo (×10 bpm)', 'energy', ['Pop', 'Jazz']), ('loan applicants', 'income (k$×10)', 'credit score/100', ['Approve', 'Decline'])])
    what, f1, f2, cls = ctx
    n = 6 if slot.d <= 2 else 8
    for _ in range(40):
        pts = [(rng.randint(1, 10), rng.randint(1, 10), rng.choice(cls)) for _ in range(n)]
        q = (rng.randint(2, 9), rng.randint(2, 9))
        d = sorted(((math.dist(p[:2], q), i) for i, p in enumerate(pts)))
        k = 3 if slot.d <= 3 else rng.choice([3, 5])
        if len({round(x[0], 6) for x in d[: k + 1]}) < k + 1:
            continue
        votes = Counter(pts[i][2] for _, i in d[:k])
        if len(votes) > 1 and votes.most_common(2)[0][1] == votes.most_common(2)[1][1]:
            continue
        if set(p[:2] for p in pts) and len(set(p[:2] for p in pts)) < n:
            continue
        break
    else:
        return None
    lab = votes.most_common(1)[0][0]
    tb = table(['Point', f1, f2, 'Class'], [(f'P{i + 1}', x, y, c) for i, (x, y, c) in enumerate(pts)])
    near = ', '.join(f'P{i + 1} ({dd:.2f}, {pts[i][2]})' for dd, i in d[:k])
    ans = f'Nearest {k}: {near}. Majority class: {lab}.'
    extra = ' Explain the effect of choosing a much larger k.' if slot.d >= 4 else ''
    return dict(stem=f'A k-nearest-neighbours classifier for {what} uses two features, {f1} and {f2}. Training data:\n{tb}\nUsing Euclidean distance and k = {k}, classify a new example at ({q[0]}, {q[1]}). Show the distances to the nearest neighbours.{extra}',
                answer=ans, markingKey=ans + ' M1 Euclidean distance formula; A1 correct nearest set; A1 class by majority vote.' + (' R1 large k smooths the decision boundary (less variance, more bias) and can be dominated by the majority class.' if extra else ''),
                marks=3 if slot.d <= 3 else 5)


def _entropy(counts):
    t = sum(counts)
    return -sum(c / t * math.log2(c / t) for c in counts if c)


def _gini(counts):
    t = sum(counts)
    return 1 - sum((c / t) ** 2 for c in counts)


@R.add('ch07-st2', 'C3', (2, 5), 'numerical')
def info_gain(rng, slot):
    ctx = rng.choice([('play outdoor football', 'Weather', ['Sunny', 'Rainy']), ('approve a loan', 'Employed', ['Yes', 'No']), ('a passenger buys travel insurance', 'Trip length', ['Short', 'Long']), ('a student passes', 'Did homework', ['Yes', 'No'])])
    target, attr, vals = ctx
    a_pos, a_neg = rng.randint(0, 6), rng.randint(0, 6)
    b_pos, b_neg = rng.randint(0, 6), rng.randint(0, 6)
    if min(a_pos + a_neg, b_pos + b_neg) == 0:
        return None
    P, N = a_pos + b_pos, a_neg + b_neg
    if P == 0 or N == 0:
        return None
    use_gini = slot.d >= 4 and rng.random() < 0.5
    f = _gini if use_gini else _entropy
    H = f([P, N])
    Ha, Hb = f([a_pos, a_neg]), f([b_pos, b_neg])
    tot = P + N
    w = (a_pos + a_neg) / tot * Ha + (b_pos + b_neg) / tot * Hb
    gain = H - w
    meas = 'Gini impurity' if use_gini else 'entropy'
    ans = f'Parent {meas} = {H:.3f}; {vals[0]}: {Ha:.3f}, {vals[1]}: {Hb:.3f}; weighted = {w:.3f}; {"decrease in impurity" if use_gini else "information gain"} = {gain:.3f}'
    return dict(stem=f'A decision tree is being built to predict whether {target}. Of {tot} training examples, {P} are Yes and {N} are No. Splitting on {attr}: {vals[0]} has {a_pos} Yes and {a_neg} No; {vals[1]} has {b_pos} Yes and {b_neg} No. Calculate the {"reduction in Gini impurity" if use_gini else "information gain (using log base 2)"} for this split.',
                answer=ans, markingKey=ans + f'. M1 parent {meas}; M1 child values; M1 weighting by proportion; A1 final value.', marks=4)


@R.add('ch07-st2', 'C3', (1, 3), 'short')
def tree_trace(rng, slot):
    t1, t2 = rng.randint(18, 30), rng.randint(40, 80)
    ex = [(rng.randint(10, 40), rng.randint(20, 100), rng.choice(['yes', 'no'])) for _ in range(3)]
    def cls(temp, hum, wind):
        if temp > t1:
            return 'Go to beach' if hum <= t2 else 'Stay in'
        return 'Go hiking' if wind == 'no' else 'Stay in'
    outs = [cls(*e) for e in ex]
    rule = f'IF Temperature > {t1} THEN (IF Humidity ≤ {t2} THEN "Go to beach" ELSE "Stay in") ELSE (IF Windy = no THEN "Go hiking" ELSE "Stay in")'
    return dict(stem=f'A trained decision tree is: {rule}. Classify these days (Temperature °C, Humidity %, Windy): ' + '; '.join(f'({a}, {b}, {c})' for a, b, c in ex) + '.',
                answer='; '.join(outs), markingKey='; '.join(f'({a}, {b}, {c}) → {o}' for (a, b, c), o in zip(ex, outs)) + ' 1 mark each.', marks=3)


R.facts('ch07-st2', F(
    terms=[('k-nearest neighbours (k-NN)', 'a supervised algorithm that classifies a new example by the majority class of the k closest training examples according to a distance measure'),
           ('decision tree', 'a supervised model that predicts by following a tree of tests on feature values from the root to a leaf that gives the class or value'),
           ('entropy', 'a measure of impurity (uncertainty) in a set of class labels, −Σ p log₂ p, which is 0 for a pure set'),
           ('information gain', 'the reduction in entropy achieved by splitting a dataset on a feature; the split with the highest gain is chosen'),
           ('Gini impurity', 'a measure of impurity, 1 − Σ p², equal to the probability of misclassifying a randomly chosen example'),
           ('pruning', 'removing branches of a decision tree that add little predictive power, to reduce overfitting'),
           ('lazy learner', 'an algorithm such as k-NN that does no training beyond storing the data and does its work at prediction time')],
    why=[('Explain why k is usually chosen to be odd in binary k-NN classification.', 'An odd k avoids tied votes between the two classes.'),
         ('Explain why k-NN is slow at prediction time for large datasets.', 'It stores all training examples and must compute the distance from the new example to every one of them (unless an index such as a k-d tree is used).'),
         ('Explain why an unpruned decision tree is likely to overfit.', 'It keeps splitting until leaves are pure, so it learns noise and individual examples, giving perfect training accuracy but poor generalisation.'),
         ('Explain why decision trees are considered interpretable.', 'Each prediction can be explained as a sequence of simple, human-readable if-then tests from root to leaf.')],
    contrast=[('k-NN', 'a decision tree', 'k-NN is a lazy, distance-based learner that stores the data and votes among neighbours; a decision tree is an eager learner that builds explicit rules by recursively splitting on features.'),
              ('entropy', 'Gini impurity', 'Both measure node impurity; entropy uses −Σ p log₂ p (range 0–1 for two classes), Gini uses 1 − Σ p² (range 0–0.5); they usually choose similar splits, Gini is cheaper to compute.'),
              ('a small k', 'a large k', 'A small k gives a flexible boundary that follows noise (high variance, overfitting); a large k gives a smoother boundary (higher bias) that may ignore local patterns.')],
    misc=[('k-NN learns a set of weights during training.', 'k-NN has no training phase; it simply stores the examples and computes distances at prediction time.'),
          ('A decision tree always chooses the feature with the most categories at the root.', 'It chooses the split with the greatest information gain (or impurity reduction); many-valued features can be favoured unfairly, which is why gain ratio exists.'),
          ('Setting k = 1 gives the most accurate k-NN model.', 'k = 1 fits the training data perfectly but is very sensitive to noise and outliers; the best k is chosen by validation.')],
    evaluate=[('Decision trees should be preferred to k-NN for medical diagnosis.', ['trees give explainable rules that doctors can check', 'fast predictions', 'handle mixed feature types'], ['single trees can be unstable and overfit', 'k-NN can be accurate with well-scaled features and needs no training', 'ensembles (random forests) may be needed, reducing interpretability'], 'Trees are often preferable where explanations are required, but the choice should be validated on data; accuracy and explainability must be balanced.')],
))
ar('ch07-st2', [
    ('Features should be scaled before applying k-NN.', 'k-NN uses distances, which are dominated by features with large ranges.', 0, 'Both true; R explains A.'),
    ('A pure node in a decision tree has entropy 1.', 'In a pure node all examples have the same class.', 3, 'A is false (entropy 0); R is true.'),
    ('k-NN is called a lazy learner.', 'It defers computation until a prediction is requested.', 0, 'Both true; R explains A.'),
])


# ---- model evaluation ----
@R.add('ch07-st3', 'C3', (1, 5), 'numerical')
def confusion(rng, slot):
    ctx = rng.choice([('a spam filter', 'spam'), ('a model screening X-rays for tuberculosis', 'tuberculosis'), ('a fraud detector at a bank in Dubai', 'fraud'), ('a model predicting which students in Lima need extra support', 'needs support'), ('a defect detector on a factory line in Seoul', 'defective')])
    tp, fn_, fp, tn = rng.randint(10, 90), rng.randint(2, 30), rng.randint(2, 30), rng.randint(50, 300)
    tot = tp + fn_ + fp + tn
    acc = (tp + tn) / tot
    prec = tp / (tp + fp)
    rec = tp / (tp + fn_)
    f1 = 2 * prec * rec / (prec + rec)
    spec = tn / (tn + fp)
    k = slot.d
    want = [('accuracy', acc), ('precision', prec), ('recall', rec)]
    if k >= 4:
        want += [('F1 score', f1), ('specificity', spec)]
    ans = '; '.join(f'{nm} = {v:.3f}' for nm, v in want)
    q = 'Calculate the accuracy, precision and recall' + (', F1 score and specificity' if k >= 4 else '') + ' of the model.'
    if k >= 3:
        q += f' Explain which metric matters most in this context.'
    return dict(stem=f'{ctx[0][0].upper() + ctx[0][1:]} was tested on {tot} cases, with "{ctx[1]}" as the positive class. True positives = {tp}, false negatives = {fn_}, false positives = {fp}, true negatives = {tn}. {q}',
                answer=ans, markingKey=f'Accuracy = (TP + TN)/total = {tp + tn}/{tot}; precision = TP/(TP + FP) = {tp}/{tp + fp}; recall = TP/(TP + FN) = {tp}/{tp + fn_}' + (f'; F1 = 2PR/(P + R); specificity = TN/(TN + FP) = {tn}/{tn + fp}' if k >= 4 else '') + f'. {ans}. A1 each.' + (' R1: when missing a positive is costly (disease, fraud) recall matters most; when false alarms are costly (spam hiding real mail) precision matters most.' if k >= 3 else ''),
                marks=3 if k <= 2 else 4 if k == 3 else 6)


@R.add('ch07-st3', 'C3', (2, 4), 'numerical')
def preds_to_cm(rng, slot):
    n = 10 if slot.d <= 3 else 12
    act = [rng.choice([0, 1]) for _ in range(n)]
    pred = [a if rng.random() < 0.7 else 1 - a for a in act]
    tp = sum(1 for a, p in zip(act, pred) if a == 1 and p == 1)
    tn = sum(1 for a, p in zip(act, pred) if a == 0 and p == 0)
    fp = sum(1 for a, p in zip(act, pred) if a == 0 and p == 1)
    fn_ = sum(1 for a, p in zip(act, pred) if a == 1 and p == 0)
    if tp + fp == 0 or tp + fn_ == 0:
        return None
    ans = f'TP = {tp}, FP = {fp}, FN = {fn_}, TN = {tn}; accuracy {(tp + tn) / n:.2f}, precision {tp / (tp + fp):.2f}, recall {tp / (tp + fn_):.2f}'
    return dict(stem=f'A classifier gave these results on a test set (1 = positive):\nActual:    {" ".join(map(str, act))}\nPredicted: {" ".join(map(str, pred))}\nConstruct the confusion matrix and calculate accuracy, precision and recall.',
                answer=ans, markingKey=ans + '. A1 matrix; A1 each metric.', marks=4)


@R.add('ch07-st3', 'C3', (1, 3), 'numerical')
def split_sizes(rng, slot):
    n = rng.choice([1200, 5000, 24000, 800, 15000])
    tr, va = rng.choice([(70, 15), (80, 10), (60, 20)])
    te = 100 - tr - va
    k = rng.choice([5, 10])
    ans = f'train {n * tr // 100}, validation {n * va // 100}, test {n * te // 100}; in {k}-fold cross-validation each fold has {n // k} examples, and each model trains on {n - n // k}.'
    return dict(stem=f'A dataset of {n} labelled images is split {tr}/{va}/{te} into training, validation and test sets. State the size of each set. If instead {k}-fold cross-validation is used on all {n} images, state the size of each fold and how many examples each model is trained on.',
                answer=ans, markingKey=ans + ' A1 each.', marks=3)


R.facts('ch07-st3', F(
    terms=[('training set', 'the portion of the data used to fit the model\'s parameters'),
           ('test set', 'held-out data, never used in training or tuning, used once to estimate how well the model generalises'),
           ('validation set', 'data held out from training and used to tune hyperparameters and choose between models'),
           ('overfitting', 'when a model learns the training data, including its noise, so well that it performs poorly on new data'),
           ('underfitting', 'when a model is too simple to capture the underlying pattern, so it performs poorly on both training and test data'),
           ('precision', 'the proportion of predicted positives that are actually positive, TP/(TP + FP)'),
           ('recall (sensitivity)', 'the proportion of actual positives that the model correctly identifies, TP/(TP + FN)'),
           ('accuracy', 'the proportion of all predictions that are correct, (TP + TN)/total'),
           ('k-fold cross-validation', 'splitting the data into k folds and training k models, each tested on a different fold, then averaging the results')],
    why=[('Explain why accuracy can be misleading on an imbalanced dataset.', 'If 99% of cases are negative, a model that always predicts negative scores 99% accuracy while detecting no positives; precision and recall reveal this.'),
         ('Explain why the test set must not be used to tune a model.', 'Tuning on the test set makes the chosen model fit that particular data, so its score no longer estimates performance on unseen data (information leakage).'),
         ('Explain how a large gap between training accuracy and test accuracy indicates overfitting.', 'High training accuracy shows the model fits the training data; much lower test accuracy shows it has memorised specifics/noise rather than general patterns.'),
         ('Explain why there is a trade-off between precision and recall.', 'Lowering the decision threshold labels more cases positive, catching more true positives (higher recall) but also more false positives (lower precision), and vice versa.')],
    contrast=[('precision', 'recall', 'Precision measures how many predicted positives are correct (penalises false positives); recall measures how many actual positives are found (penalises false negatives).'),
              ('overfitting', 'underfitting', 'Overfitting: model too complex, excellent on training data, poor on test data; underfitting: model too simple, poor on both.'),
              ('a validation set', 'a test set', 'A validation set is used repeatedly to tune hyperparameters and select models; a test set is used once at the end to estimate final performance.')],
    misc=[('A model with 100% training accuracy is the best possible model.', 'It may be overfitting; only performance on unseen (test) data shows how well it generalises.'),
          ('High precision means the model finds most of the positive cases.', 'That is recall; high precision means that when it predicts positive it is usually right, even if it misses many positives.'),
          ('Using more of the data for testing always gives a better model.', 'A larger test set gives a more reliable estimate, but less training data usually makes the model itself worse; a balance (or cross-validation) is needed.')],
    evaluate=[('Accuracy is the best single measure of a classifier\'s quality.', ['easy to understand and communicate', 'appropriate when classes are balanced and errors equally costly'], ['misleading for imbalanced data', 'ignores different costs of false positives and false negatives', 'precision, recall, F1 and ROC-AUC give a fuller picture'], 'Accuracy is only adequate for balanced problems with equal error costs; the metric should be chosen to reflect the consequences of each type of error.')],
))
ar('ch07-st3', [
    ('Recall is the most important metric for a cancer-screening model.', 'A false negative means a patient with cancer is not referred for further tests.', 0, 'Both true; the high cost of false negatives explains A.'),
    ('k-fold cross-validation uses every example for testing exactly once.', 'Each of the k folds is used once as the test fold.', 0, 'Both true; R explains A.'),
    ('An overfitted model performs badly on its training data.', 'Overfitting means fitting noise in the training data.', 3, 'A is false – it performs very well on training data; R is true.'),
])


# ---- clustering and association rules ----
@R.add('ch07-st4', 'C3', (2, 5), 'numerical')
def kmeans_iter(rng, slot):
    for _ in range(40):
        pts = [(rng.randint(0, 10), rng.randint(0, 10)) for _ in range(6 if slot.d <= 3 else 8)]
        if len(set(pts)) < len(pts):
            continue
        c = rng.sample(pts, 2)
        ok = True
        assign = []
        for p in pts:
            d0, d1 = math.dist(p, c[0]), math.dist(p, c[1])
            if abs(d0 - d1) < 1e-9:
                ok = False
            assign.append(0 if d0 < d1 else 1)
        if ok and 0 < sum(assign) < len(pts):
            break
    else:
        return None
    new = []
    for k in (0, 1):
        g = [p for p, a in zip(pts, assign) if a == k]
        new.append((sum(x for x, _ in g) / len(g), sum(y for _, y in g) / len(g)))
    ctx = rng.choice(['delivery addresses for two depots in Bogotá', 'customers plotted by visits per month and average spend', 'GPS positions of bike-share docks', 'students plotted by hours of sport and hours of music'])
    ans = 'Cluster 1: ' + ', '.join(f'({x}, {y})' for (x, y), a in zip(pts, assign) if a == 0) + f'; cluster 2: ' + ', '.join(f'({x}, {y})' for (x, y), a in zip(pts, assign) if a == 1) + f'. New centroids ({r2(new[0][0])}, {r2(new[0][1])}) and ({r2(new[1][0])}, {r2(new[1][1])}).'
    return dict(stem=f'k-means clustering (k = 2) is applied to {ctx}: ' + ', '.join(f'({x}, {y})' for x, y in pts) + f'. The initial centroids are C1 = {c[0]} and C2 = {c[1]}. Perform one iteration: assign each point to the nearest centroid (Euclidean distance) and calculate the updated centroids.',
                answer=ans, markingKey=ans + ' M1 distances; A1 assignments; A1 each new centroid (mean of assigned points).', marks=4)


@R.add('ch07-st4', 'C3', (1, 5), 'numerical')
def assoc(rng, slot):
    items = rng.sample(['bread', 'milk', 'eggs', 'rice', 'tea', 'mangoes', 'cheese', 'coffee'], 5)
    n = 8 if slot.d <= 3 else 10
    tx = [sorted(rng.sample(items, rng.randint(2, 4))) for _ in range(n)]
    a, b = rng.sample(items, 2)
    sa = sum(1 for t in tx if a in t)
    sb = sum(1 for t in tx if b in t)
    sab = sum(1 for t in tx if a in t and b in t)
    if sa == 0 or sb == 0:
        return None
    sup = sab / n
    conf = sab / sa
    lift = conf / (sb / n)
    tl = '\n'.join(f'T{i + 1}: {{{", ".join(t)}}}' for i, t in enumerate(tx))
    want = 'support and confidence' + (' and lift' if slot.d >= 3 else '')
    ans = f'support = {sab}/{n} = {sup:.3f}; confidence = {sab}/{sa} = {conf:.3f}' + (f'; lift = {conf:.3f}/({sb}/{n}) = {lift:.3f} ({"positive association" if lift > 1 else "negative association" if lift < 1 else "independent"})' if slot.d >= 3 else '')
    return dict(stem=f'A market in Accra recorded these transactions:\n{tl}\nFor the rule {{{a}}} → {{{b}}}, calculate the {want}.' + (' Interpret the lift.' if slot.d >= 3 else ''),
                answer=ans, markingKey=ans + '. M1 counts; A1 each measure.', marks=2 if slot.d <= 2 else 4)


R.facts('ch07-st4', F(
    terms=[('clustering', 'an unsupervised technique that groups data points so that points in the same cluster are more similar to each other than to points in other clusters'),
           ('k-means', 'a clustering algorithm that repeatedly assigns points to the nearest of k centroids and moves each centroid to the mean of its assigned points until assignments stop changing'),
           ('centroid', 'the centre (mean position) of the points in a cluster'),
           ('association rule learning', 'an unsupervised method that finds rules of the form {A} → {B} describing items that frequently occur together'),
           ('support', 'the proportion of all transactions that contain the itemset'),
           ('confidence', 'for a rule A → B, the proportion of transactions containing A that also contain B'),
           ('lift', 'confidence(A → B) divided by support(B); a value above 1 means A and B occur together more often than expected by chance'),
           ('elbow method', 'choosing k by plotting within-cluster variation against k and picking the point where improvements level off')],
    why=[('Explain why the result of k-means can depend on the initial centroids.', 'k-means converges to a local optimum; different starting centroids can lead to different final clusters, so it is run several times (or seeded with k-means++) and the best result kept.'),
         ('Explain why a rule with high confidence may still be uninteresting.', 'If the consequent B is bought in most transactions anyway, high confidence is expected; lift compares confidence with B\'s overall frequency and reveals whether the association is real.'),
         ('Explain why k-means requires the number of clusters to be chosen in advance.', 'The algorithm initialises and updates exactly k centroids; it has no mechanism to decide k itself, so methods such as the elbow method or silhouette score are used.')],
    contrast=[('clustering', 'classification', 'Clustering is unsupervised and discovers groups without labels; classification is supervised and assigns examples to predefined, labelled classes.'),
              ('support', 'confidence', 'Support is how often the itemset appears in all transactions; confidence is how often B appears in transactions that already contain A.'),
              ('k-means', 'k-NN', 'k-means is unsupervised clustering with k centroids; k-NN is supervised classification using the k nearest labelled neighbours.')],
    misc=[('k-means always finds the best possible clusters.', 'It converges to a local optimum that depends on the initial centroids; it may not find the global best.'),
          ('A confidence of 0.9 for {tea} → {milk} proves buying tea causes people to buy milk.', 'Association rules show co-occurrence, not causation.'),
          ('k-means works well for clusters of any shape.', 'It assumes roughly spherical, similar-sized clusters; elongated or nested clusters need other methods such as DBSCAN.')],
    evaluate=[('Supermarkets should rearrange their stores based on association rules.', ['placing associated items together can increase sales', 'rules are cheap to compute from till data'], ['rules may reflect coincidence or seasonal effects', 'separating items can increase browsing and impulse buys', 'privacy concerns over loyalty-card data'], 'Rules are a useful input but should be tested (e.g. A/B trials) and combined with business judgement before rearranging stores.')],
))
ar('ch07-st4', [
    ('A lift greater than 1 indicates a positive association between items.', 'Lift compares the observed co-occurrence with that expected if the items were independent.', 0, 'Both true; R explains A.'),
    ('k-means is a supervised learning algorithm.', 'k-means updates centroids to the mean of assigned points.', 3, 'A is false; R is true.'),
])


# ---- neural networks, RL, genetic algorithms ----
@R.add('ch07-st5', 'C3', (1, 5), 'numerical')
def perceptron(rng, slot):
    n = 2 if slot.d <= 2 else 3
    w = [rng.choice([-1.0, -0.5, 0.2, 0.5, 0.8, 1.0, 1.5]) for _ in range(n)]
    x = [rng.choice([0, 1, 2, 3]) for _ in range(n)]
    b = rng.choice([-1.5, -1.0, -0.5, 0.0, 0.5])
    z = sum(a * c for a, c in zip(w, x)) + b
    act = rng.choice(['step', 'sigmoid', 'relu']) if slot.d >= 3 else 'step'
    if act == 'step':
        out, f_ = (1 if z >= 0 else 0), 'step (output 1 if z ≥ 0, else 0)'
    elif act == 'sigmoid':
        out, f_ = 1 / (1 + math.exp(-z)), 'sigmoid σ(z) = 1/(1 + e^(−z))'
    else:
        out, f_ = max(0.0, z), 'ReLU max(0, z)'
    ans = f'z = {" + ".join(f"({a})({c})" for a, c in zip(w, x))} + ({b}) = {r2(z, 3)}; output = {r2(out, 3)}'
    return dict(stem=f'A neuron has weights {w}, bias {b} and inputs {x}. Using the {f_} activation function, calculate the weighted sum z and the neuron\'s output.',
                answer=ans, markingKey=ans + '. M1 weighted sum; A1 z; A1 activation applied.', marks=2 if slot.d <= 2 else 3)


@R.add('ch07-st5', 'C3', (3, 5), 'numerical')
def qlearn(rng, slot):
    q = rng.choice([0.0, 2.0, 4.5, 5.0])
    r_ = rng.choice([-1, 0, 5, 10])
    mx = rng.choice([3.0, 6.0, 8.0])
    a = rng.choice([0.1, 0.5, 0.2])
    g = rng.choice([0.9, 0.8])
    new = q + a * (r_ + g * mx - q)
    ans = f'Q_new = {q} + {a}({r_} + {g} × {mx} − {q}) = {r2(new, 3)}'
    return dict(stem=f'A reinforcement-learning agent in a warehouse robot uses Q-learning: Q(s, a) ← Q(s, a) + α[r + γ max Q(s′, a′) − Q(s, a)]. Currently Q(s, a) = {q}. After taking the action it receives reward r = {r_} and the best Q-value in the next state is {mx}. With learning rate α = {a} and discount factor γ = {g}, calculate the updated Q(s, a) and explain the role of γ.',
                answer=ans + '. γ weights future rewards: close to 1 values long-term reward, close to 0 makes the agent short-sighted.',
                markingKey=ans + ' M1 substitution; A1 value; R1 discount factor.', marks=4)


@R.add('ch07-st5', 'C3', (2, 5), 'short')
def ga_ops(rng, slot):
    L = 8
    p1 = ''.join(rng.choice('01') for _ in range(L))
    p2 = ''.join(rng.choice('01') for _ in range(L))
    cp = rng.randint(2, 6)
    c1, c2 = p1[:cp] + p2[cp:], p2[:cp] + p1[cp:]
    mpos = rng.randint(1, L)
    m = c1[:mpos - 1] + ('1' if c1[mpos - 1] == '0' else '0') + c1[mpos:]
    fit = lambda s: s.count('1')
    ans = f'Children: {c1} and {c2}; after mutation of bit {mpos}: {m}. Fitness (number of 1s): parents {fit(p1)}, {fit(p2)}; children {fit(c1)}, {fit(c2)}; mutated {fit(m)}.'
    return dict(stem=f'A genetic algorithm evolves 8-bit strings, with fitness = number of 1s. Parents are {p1} and {p2}. Apply single-point crossover after bit {cp}, then mutate bit {mpos} (counting from 1 on the left) of the first child. Give the children, the mutated child and all fitness values.',
                answer=ans, markingKey=ans + ' A1 each child; A1 mutation; A1 fitness values.', marks=4)


R.facts('ch07-st5', F(
    terms=[('artificial neuron (perceptron)', 'a unit that computes a weighted sum of its inputs plus a bias and passes it through an activation function to produce an output'),
           ('backpropagation', 'the algorithm that computes how much each weight contributed to the error and adjusts weights backwards through the network using gradient descent'),
           ('learning rate', 'a hyperparameter controlling how large each weight update is during training'),
           ('agent (RL)', 'the learner or decision-maker in reinforcement learning, which observes states, takes actions and receives rewards'),
           ('reward', 'the numerical feedback signal an RL agent receives after an action, which it tries to maximise over time'),
           ('exploration vs exploitation', 'the RL trade-off between trying new actions to discover their value and choosing the best-known action'),
           ('genetic algorithm', 'an optimisation method inspired by natural selection that evolves a population of candidate solutions using selection, crossover and mutation'),
           ('fitness function', 'the function that scores how good a candidate solution is in a genetic algorithm')],
    why=[('Explain why mutation is needed in a genetic algorithm.', 'Crossover only recombines existing genes; mutation introduces new genetic material, maintaining diversity and preventing the population converging prematurely on a local optimum.'),
         ('Explain why an RL agent must sometimes explore rather than always choose the best-known action.', 'Its value estimates are based on limited experience; without exploration it may never discover better actions and remain stuck with a sub-optimal policy.'),
         ('Explain why a learning rate that is too high can stop a neural network from training.', 'Weight updates overshoot the minimum of the loss function, making the loss oscillate or diverge instead of decreasing.'),
         ('Explain why neural networks need many training examples.', 'They have many weights to adjust; each example provides only a small amount of information, and too few examples lead to overfitting.')],
    contrast=[('a genetic algorithm', 'reinforcement learning', 'A GA evolves a population of complete solutions using a fitness function over generations; RL trains one agent that learns a policy from rewards for individual actions in an environment.'),
              ('crossover', 'mutation', 'Crossover combines parts of two parents to make offspring; mutation randomly changes genes in one individual.'),
              ('exploration', 'exploitation', 'Exploration tries less-known actions to gain information; exploitation chooses the action currently believed to be best.')],
    misc=[('A genetic algorithm is guaranteed to find the optimal solution.', 'GAs are heuristic; they usually find good solutions but may converge to a local optimum.'),
          ('In reinforcement learning the agent is told the correct action at each step.', 'It only receives a reward (often delayed) and must work out which actions led to it.'),
          ('A neural network\'s weights are set by the programmer.', 'Weights are initialised randomly and learned through backpropagation and gradient descent.')],
    evaluate=[('Reinforcement learning is the most suitable approach for training self-driving cars.', ['learns complex sequential decisions from rewards', 'can be trained safely in simulation'], ['real-world exploration is dangerous', 'reward functions are hard to design and can be gamed', 'supervised learning from human driving data and rule-based safety systems are also needed'], 'RL is valuable, mainly in simulation, but practical systems combine it with supervised learning and engineered safety constraints.')],
))
ar('ch07-st5', [
    ('Mutation helps a genetic algorithm escape local optima.', 'Mutation introduces new variation into the population.', 0, 'Both true; R explains A.'),
    ('A perceptron with a step activation can learn the XOR function.', 'A single perceptron can only separate classes with a straight line (linear boundary).', 3, 'A is false; R is true and explains why (XOR is not linearly separable).'),
    ('The discount factor γ in Q-learning is between 0 and 1.', 'Future rewards are usually worth less than immediate rewards.', 0, 'Both true; R explains why γ < 1.'),
])


# =============================================================================================
# ch08 A4.4 Ethical considerations
# =============================================================================================
@R.add('ch08-st1', 'C3', (2, 5), 'numerical')
def fairness(rng, slot):
    ctx = rng.choice([('a CV-screening model at a company in Toronto', 'shortlisted', 'gender', ('women', 'men')),
                      ('a loan-approval model in Nairobi', 'approved', 'region', ('rural applicants', 'urban applicants')),
                      ('a university admissions model in Seoul', 'offered a place', 'school type', ('state-school applicants', 'private-school applicants')),
                      ('a facial-verification system at an airport', 'correctly verified', 'skin tone', ('darker-skinned travellers', 'lighter-skinned travellers'))])
    what, out, attr, (g1, g2) = ctx
    n1, n2 = rng.choice([200, 400, 500, 800]), rng.choice([200, 400, 500, 800])
    s1, s2 = rng.randint(15, 45), rng.randint(35, 70)
    a1, a2 = n1 * s1 // 100, n2 * s2 // 100
    r1, r2_ = a1 / n1, a2 / n2
    di = min(r1, r2_) / max(r1, r2_)
    ans = f'{g1}: {a1}/{n1} = {r1:.3f}; {g2}: {a2}/{n2} = {r2_:.3f}; difference = {abs(r1 - r2_):.3f}; ratio = {di:.3f} – ' + ('below 0.8, so the four-fifths rule flags possible adverse impact.' if di < 0.8 else 'at least 0.8, so the four-fifths rule is satisfied.')
    extra = ' Suggest two possible causes of the disparity and one mitigation.' if slot.d >= 4 else ''
    return dict(stem=f'An audit of {what} found that {a1} of {n1} {g1} and {a2} of {n2} {g2} were {out}. Calculate the rate for each group, the difference in rates (demographic parity difference) and the ratio of the lower to the higher rate, and apply the "four-fifths rule".{extra}',
                answer=ans, markingKey=ans + (' Causes: historical bias in training labels; under-representation of a group; proxy features (postcode, school) correlated with the protected attribute. Mitigation: re-sample/re-weight data, remove proxies, fairness constraints, human review, ongoing audits.' if extra else '') + ' A1 each rate; A1 difference; A1 ratio and conclusion.', marks=4 if slot.d <= 3 else 6)


@R.add('ch08-st1', 'C3', (3, 5), 'numerical')
def eq_opp(rng, slot):
    g = rng.choice([('older patients', 'younger patients'), ('patients from clinic A', 'patients from clinic B'), ('female patients', 'male patients')])
    tp1, fn1 = rng.randint(30, 80), rng.randint(5, 40)
    tp2, fn2 = rng.randint(30, 80), rng.randint(5, 40)
    t1, t2 = tp1 / (tp1 + fn1), tp2 / (tp2 + fn2)
    ans = f'TPR {g[0]} = {tp1}/{tp1 + fn1} = {t1:.3f}; TPR {g[1]} = {tp2}/{tp2 + fn2} = {t2:.3f}; gap = {abs(t1 - t2):.3f}. The group with lower recall has more missed diagnoses, violating equal opportunity.'
    return dict(stem=f'A diagnostic model was tested on {g[0]} (TP = {tp1}, FN = {fn1}) and {g[1]} (TP = {tp2}, FN = {fn2}). Calculate the true-positive rate (recall) for each group and explain what the difference means for fairness ("equal opportunity").',
                answer=ans, markingKey=ans + ' A1 each TPR; A1 gap; R1 interpretation.', marks=4)


_BIAS_CASES = [
    ('a recruitment model trained on ten years of a technology firm\'s hiring decisions', 'historical bias: past decisions favoured one group, so the labels encode discrimination', 'audit outcomes by group, remove proxy features, re-weight or re-label training data, keep human review'),
    ('a face-recognition system trained mostly on images of light-skinned adults', 'representation (sampling) bias: some groups are under-represented, so error rates are higher for them', 'collect a more diverse, balanced dataset; report accuracy per demographic group'),
    ('a predictive-policing tool trained on past arrest records', 'feedback-loop / measurement bias: arrests reflect where police patrolled, so the tool sends more patrols to the same areas', 'use outcome data less dependent on patrol patterns, audit for feedback loops, limit use'),
    ('a speech assistant that struggles with Scottish, Nigerian and Indian English accents', 'representation bias in the audio training data', 'include diverse speakers in training and test sets; evaluate per accent'),
    ('a health-risk model that used past healthcare spending as a proxy for medical need', 'measurement (proxy) bias: groups with less access to care spent less, so their need was underestimated', 'choose a target variable that measures need directly; test outcomes across groups'),
    ('a credit-scoring model that does not use ethnicity but does use postcode', 'proxy discrimination: postcode correlates strongly with ethnicity and income', 'test for disparate impact, remove or transform proxy features, apply fairness constraints'),
]


@R.add('ch08-st1', 'C3', (1, 4), 'short')
def bias_case(rng, slot):
    case, typ, fix = rng.choice(_BIAS_CASES)
    frame = rng.choice(['Identify the type of bias most likely to arise and explain how it occurs.', 'Explain how bias could enter this system and suggest one way to reduce it.', 'Outline the likely source of unfairness and one mitigation the developers should apply.'])
    return dict(stem=f'Consider {case}. {frame}', answer=f'{typ}. Mitigation: {fix}.', markingKey=f'Type/source: {typ} (1-2); explanation of mechanism (1); mitigation: {fix} (1).', marks=3 if slot.d <= 3 else 4)


R.facts('ch08-st1', F(
    terms=[('algorithmic bias', 'systematic and unfair differences in a system\'s outputs for different groups of people'),
           ('historical bias', 'bias that exists in the world and is reflected in the data even if it is perfectly measured, e.g. past discriminatory decisions'),
           ('representation (sampling) bias', 'bias caused when some groups are under- or over-represented in the training data'),
           ('measurement bias', 'bias caused by choosing, collecting or labelling features and targets in ways that differ in accuracy between groups'),
           ('proxy variable', 'a feature that is not a protected characteristic but correlates strongly with one, such as postcode with ethnicity'),
           ('demographic parity', 'a fairness criterion requiring that the rate of positive outcomes is similar for all groups'),
           ('equal opportunity', 'a fairness criterion requiring that the true-positive rate is similar for all groups')],
    why=[('Explain why removing a protected attribute (e.g. gender) from the training data does not guarantee a fair model.', 'Other features can act as proxies (job titles, hobbies, postcode) and the labels themselves may reflect historical discrimination, so the model can still learn the same bias.'),
         ('Explain why a model can be biased even if the algorithm itself treats every input identically.', 'The model learns patterns from data; if the data under-represent a group or encode past discrimination, the learned rules reproduce those patterns.'),
         ('Explain why it is often impossible to satisfy all fairness definitions at once.', 'When base rates differ between groups, equalising positive rates (demographic parity) conflicts mathematically with equalising error rates and calibration; designers must choose which criterion fits the context.')],
    contrast=[('historical bias', 'representation bias', 'Historical bias exists in the real world and is captured accurately by the data; representation bias arises because the data sample does not reflect the population.'),
              ('demographic parity', 'equal opportunity', 'Demographic parity requires equal positive-outcome rates across groups; equal opportunity requires equal true-positive rates among those who truly qualify.')],
    misc=[('Algorithms are objective, so they cannot be biased.', 'Algorithms learn from human-generated data and design choices; they can reproduce and amplify existing biases at scale.'),
          ('Bias only matters if the developers intended to discriminate.', 'Unintended bias still causes real harm (denied loans, misdiagnoses); responsibility includes testing for and mitigating it.'),
          ('A larger dataset always removes bias.', 'More data reduces random error but not systematic bias; a large but unrepresentative or historically biased dataset stays biased.')],
    evaluate=[('Machine-learning models are fairer than human decision-makers.', ['apply the same rules consistently', 'can be audited and measured for bias', 'remove individual prejudices'], ['learn and amplify bias in historical data', 'scale errors to millions of decisions', 'lack of transparency makes challenge difficult'], 'Models can be fairer only if data, objectives and outcomes are actively audited and corrected; otherwise they automate existing unfairness.'),
              ('Companies should be legally required to audit ML systems for bias before deployment.', ['protects individuals from discriminatory outcomes', 'creates accountability and public trust'], ['compliance cost may burden small firms', 'no single agreed fairness metric', 'audits can become box-ticking'], 'Audits are justified for high-risk uses (hiring, credit, health, policing), as in the EU AI Act\'s risk-based approach, with proportionate requirements elsewhere.')],
))
ar('ch08-st1', [
    ('Removing gender from a dataset may not stop a model discriminating by gender.', 'Other features can act as proxies for gender.', 0, 'Both true; R explains A.'),
    ('Representation bias occurs when some groups are under-represented in training data.', 'Models are usually less accurate for groups with fewer training examples.', 0, 'Both true; R explains why under-representation matters.'),
    ('An accurate model overall is fair to every group.', 'Overall accuracy can hide large differences between groups.', 3, 'A is false; R is true.'),
])


@R.add('ch08-st2', 'C3', (2, 5), 'short')
def k_anon(rng, slot):
    ages = ['20–29', '30–39', '40–49']
    zips = ['101**', '102**', '103**']
    rows = []
    for _ in range(8 if slot.d <= 3 else 10):
        rows.append((rng.choice(ages), rng.choice(zips), rng.choice(['F', 'M']), rng.choice(['asthma', 'diabetes', 'flu', 'none'])))
    groups = Counter((a, z, s) for a, z, s, _ in rows)
    k = min(groups.values())
    small = [g for g, c in groups.items() if c == k]
    ans = f'k = {k} (smallest group: {", ".join("/".join(g) for g in small[:2])} with {k} record(s)).'
    return dict(stem=f'A hospital in Lisbon wants to release this dataset for ML research. AgeBand, Postcode and Sex are quasi-identifiers; Condition is sensitive.\n{table(["AgeBand", "Postcode", "Sex", "Condition"], rows)}\nDetermine the value of k for which the table is k-anonymous, and explain why a low k is a privacy risk.',
                answer=ans + ' With small groups an attacker who knows a person\'s age band, postcode and sex can identify their record and condition (re-identification).',
                markingKey=ans + ' M1 grouping by quasi-identifiers; A1 k; R1 re-identification risk; further generalisation or suppression increases k.', marks=3 if slot.d <= 3 else 4)


R.facts('ch08-st2', F(
    terms=[('informed consent', 'permission given freely by a person who understands what data will be collected, how it will be used and the risks involved'),
           ('anonymisation', 'irreversibly removing or altering identifying information so that individuals cannot be identified from a dataset'),
           ('pseudonymisation', 'replacing identifiers with artificial codes so that data can only be linked back to individuals with separately held additional information'),
           ('transparency (in ML)', 'openness about when an ML system is used, what data it uses and how it reaches decisions'),
           ('explainability', 'the ability to give human-understandable reasons for a model\'s individual decisions'),
           ('accountability', 'the principle that identifiable people or organisations are responsible for an ML system\'s outcomes and can be held to account'),
           ('data minimisation', 'collecting and keeping only the personal data that is necessary for a specified purpose'),
           ('differential privacy', 'a technique that adds carefully calibrated random noise to data or results so that the presence of any single individual cannot be inferred')],
    why=[('Explain why pseudonymised data is still considered personal data under laws such as the GDPR.', 'The codes can be linked back to individuals using the separately held key, or re-identified by combining with other data, so the risk to individuals remains.'),
         ('Explain why explainability is important when ML is used to make decisions about people.', 'People affected need to understand and challenge decisions (e.g. a refused loan); explanations reveal errors and bias, support accountability and are required by some regulations.'),
         ('Explain why consent obtained through long, complex terms and conditions may not be "informed".', 'Users rarely read or understand them, may have no real choice but to accept, and cannot foresee secondary uses such as training ML models, so the consent is not genuinely informed or freely given.'),
         ('Explain why accountability is difficult for complex ML systems.', 'Responsibility is spread across data providers, developers, deployers and users; opaque models make it hard to show why an error happened, so it is unclear who should answer for harms.')],
    contrast=[('anonymisation', 'pseudonymisation', 'Anonymisation irreversibly prevents identification; pseudonymisation replaces identifiers with codes that can be reversed with a separately held key.'),
              ('transparency', 'explainability', 'Transparency is openness about the system as a whole (that ML is used, what data, purpose); explainability is being able to give reasons for a specific decision.'),
              ('privacy', 'security', 'Privacy is about individuals\' control over how their personal data is collected and used; security is the technical protection of data from unauthorised access or loss.')],
    misc=[('Removing names from a dataset makes it anonymous.', 'Combinations of other attributes (birth date, postcode, sex) can re-identify most people; true anonymisation needs generalisation, suppression or noise.'),
          ('If data is publicly available online, it is ethical to use it for any ML purpose.', 'Public availability is not consent for every use; scraping personal data can breach privacy expectations, copyright and data-protection law.'),
          ('An ML model cannot leak training data because it only stores weights.', 'Models can memorise and reveal training examples (membership-inference and model-inversion attacks), especially large models.')],
    evaluate=[('Users should have a legal right to an explanation of any decision made about them by an ML system.', ['supports fairness, trust and the ability to contest decisions', 'forces developers to detect errors and bias'], ['some accurate models are hard to explain faithfully', 'explanations may reveal trade secrets or enable gaming', 'cost for low-impact decisions'], 'A right to meaningful explanation is justified for significant decisions (credit, jobs, health, justice), with lighter requirements for low-risk uses.')],
))
ar('ch08-st2', [
    ('Pseudonymised data can sometimes be linked back to individuals.', 'The key that maps codes to identities is kept separately but still exists.', 0, 'Both true; R explains A.'),
    ('Ticking "I agree" always constitutes informed consent.', 'Informed consent requires understanding how the data will be used.', 3, 'A is false; R is true.'),
])
scen('ch08-st2', 'C3', (2, 4), [
    'A school in Geneva wants to use an ML system that analyses webcam footage to detect whether students are paying attention in online lessons.',
    'A health-insurance company in Toronto plans to use fitness-tracker data to set individual premiums.',
    'A city council in Melbourne wants to use facial recognition on public CCTV to find missing persons.',
    'A supermarket chain in Hanoi wants to predict which customers are pregnant from their purchases to send targeted offers.',
    'A bank in Lima uses a complex neural network to decide which small businesses receive loans.',
], [
    ('Discuss two privacy issues raised by this proposal.', 'Points may include: collection of sensitive personal/biometric data; whether informed, freely given consent is possible; purpose limitation and data minimisation; storage, security and retention; inferences beyond what people disclosed; surveillance and chilling effects. Two well-developed, context-specific points.', 4),
    ('Explain how the organisation could make the system more transparent and accountable.', 'Inform people when ML is used and why; publish what data is used; provide explanations of individual decisions and a route to human review/appeal; document the model (model cards), audit it regularly, and assign a named responsible owner.', 4),
    ('Outline what informed consent would require in this situation.', 'Clear, plain-language explanation of what data is collected, for what purpose, by whom, how long it is kept and the risks; a genuine choice to refuse without penalty; ability to withdraw consent later.', 3),
])


@R.add('ch08-st3', 'C3', (2, 5), 'numerical')
def carbon(rng, slot):
    g = rng.choice([64, 128, 512, 1024])
    p = rng.choice([0.3, 0.4, 0.7])
    h = rng.choice([24, 72, 240, 720])
    pue = rng.choice([1.1, 1.2, 1.5])
    ci = rng.choice([(0.03, 'Norway (mostly hydro)'), (0.45, 'a mixed grid'), (0.7, 'a coal-heavy grid')])
    kwh = g * p * h * pue
    co2 = kwh * ci[0] / 1000
    alt = kwh * 0.03 / 1000
    ans = f'Energy = {g} × {p} kW × {h} h × {pue} = {r2(kwh, 1)} kWh; emissions = {r2(kwh, 1)} × {ci[0]} kg/kWh = {r2(co2, 2)} tonnes CO₂'
    extra = f' Compare with running the same job on a grid of 0.03 kg/kWh.' if slot.d >= 4 else ''
    return dict(stem=f'Training a model uses {g} GPUs drawing {p} kW each for {h} hours in a data centre with a power usage effectiveness (PUE) of {pue}, powered by {ci[1]} emitting {ci[0]} kg CO₂ per kWh. Estimate the energy used and the CO₂ emitted.{extra}',
                answer=ans + (f'; on a 0.03 kg/kWh grid: {r2(alt, 2)} t.' if extra else ''), markingKey=ans + '. M1 GPUs × power × time; M1 × PUE; A1 kWh; A1 tonnes.' + (' R1 location/energy source strongly affects footprint.' if extra else ''), marks=4 if slot.d <= 3 else 5)


R.facts('ch08-st3', F(
    terms=[('carbon footprint (of ML)', 'the greenhouse-gas emissions caused by the energy used to train, run and store ML models and their data, plus hardware manufacture'),
           ('deepfake', 'synthetic audio, image or video created with deep learning that realistically imitates a real person saying or doing something they did not'),
           ('misinformation', 'false or misleading information spread regardless of intent'),
           ('disinformation', 'false information created and spread deliberately to deceive'),
           ('filter bubble', 'a situation in which recommendation algorithms show users mainly content that matches their existing views, limiting exposure to other perspectives'),
           ('power usage effectiveness (PUE)', 'the ratio of a data centre\'s total energy use to the energy used by its computing equipment; 1.0 is ideal'),
           ('automation', 'the use of technology, including AI, to perform tasks previously done by people')],
    why=[('Explain why generative AI can make misinformation harder to detect.', 'It produces fluent text, realistic images, audio and video cheaply and at scale, so fake content looks authentic, can be personalised and overwhelms fact-checking.'),
         ('Explain why the location of a data centre affects the environmental impact of training a model.', 'Emissions depend on the carbon intensity of the local electricity grid and on cooling needs; the same training run can emit many times more CO₂ on a coal-heavy grid than on hydro or wind power.'),
         ('Explain how recommendation algorithms can contribute to polarisation.', 'They optimise for engagement, which favours emotive and extreme content and content similar to what users already like, creating filter bubbles and echo chambers.'),
         ('Explain why water use is an environmental concern for AI data centres.', 'Large data centres use evaporative cooling, consuming significant volumes of fresh water, which can stress local supplies, especially in dry regions.')],
    contrast=[('misinformation', 'disinformation', 'Misinformation is false information spread without necessarily intending harm; disinformation is deliberately created and spread to deceive.'),
              ('job displacement', 'job augmentation', 'Displacement is AI replacing tasks or jobs done by people; augmentation is AI assisting workers so they become more productive.'),
              ('training energy', 'inference energy', 'Training energy is a large one-off cost per model; inference energy is smaller per query but repeated billions of times, so over a model\'s life it can exceed training.')],
    misc=[('Once a model is trained it has no further environmental cost.', 'Serving predictions (inference) to millions of users consumes ongoing energy and water, and hardware has embodied emissions.'),
          ('Deepfakes are only a problem for celebrities.', 'They are used in fraud (voice-cloned phone scams), harassment of private individuals, election disinformation and can undermine trust in genuine evidence (the "liar\'s dividend").'),
          ('AI will only replace low-skilled jobs.', 'AI also automates tasks in skilled work such as translation, coding, legal research and radiology, while creating new roles.')],
    evaluate=[('The benefits of large AI models outweigh their environmental costs.', ['AI optimises energy grids, logistics and climate research', 'efficiency improvements per task', 'can accelerate scientific discovery'], ['training and inference consume large amounts of electricity and water', 'rebound effect: cheaper AI increases total use', 'benefits are unevenly distributed while environmental costs are global'], 'It depends on use and energy source: benefits can outweigh costs when models are used for high-value purposes, efficiently, on low-carbon energy and reported transparently.'),
              ('Social-media platforms should be legally responsible for AI-generated misinformation they host.', ['creates strong incentives to detect and label fake content', 'platforms profit from engagement'], ['risk of over-removal and censorship of legitimate speech', 'detection at scale is technically difficult', 'shifts responsibility from creators'], 'A balanced approach – duties to label synthetic media, act on reported harmful content and be transparent about algorithms – is more defensible than strict liability.')],
))
ar('ch08-st3', [
    ('The CO₂ emitted by training a model depends on where it is trained.', 'Electricity grids differ in carbon intensity.', 0, 'Both true; R explains A.'),
    ('Deepfakes can only be created by large organisations.', 'Open-source deep-learning tools can run on consumer GPUs.', 3, 'A is false; R is true and shows why.'),
])


# =============================================================================================
# ch09 B3.1 Fundamentals of OOP for a single class  – outputs come from exec() of the code shown
# =============================================================================================
def _code_q(code, lang='Python'):
    return f'Consider the following {lang} code.\n{code}\nState the exact output.'


def _gen_account(rng, slot):
    cls = rng.choice(['BankAccount', 'Wallet', 'TransitCard'])
    start = rng.choice([0, 20, 50, 100])
    owner = rng.choice(PEOPLE)
    ops = []
    for _ in range(3 if slot.d <= 2 else 5):
        if rng.random() < 0.5:
            ops.append(f'acc.deposit({rng.choice([10, 25, 40, 60])})')
        else:
            ops.append(f'acc.withdraw({rng.choice([15, 30, 70, 120])})')
    body = '\n'.join(ops)
    code = f'''class {cls}:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused", amount)
        else:
            self.balance = self.balance - amount

acc = {cls}("{owner}", {start})
{body}
print(acc.owner, acc.balance)'''
    return code


def _gen_thermo(rng, slot):
    lo, hi = rng.choice([(16, 26), (15, 28), (18, 24)])
    t0 = rng.randint(lo, hi)
    ops = [f't.adjust({rng.choice([-5, -3, -1, 2, 4, 6])})' for _ in range(3 if slot.d <= 2 else 5)]
    code = f'''class Thermostat:
    def __init__(self, target):
        self.target = target

    def adjust(self, change):
        new = self.target + change
        if new < {lo}:
            new = {lo}
        elif new > {hi}:
            new = {hi}
        self.target = new
        print("Target:", self.target)

t = Thermostat({t0})
''' + '\n'.join(ops)
    return code


def _gen_playlist(rng, slot):
    songs = rng.sample([('Fela', 245), ('Amapiano', 198), ('Fado', 210), ('K-pop', 185), ('Cumbia', 230), ('Samba', 175)], 4 if slot.d <= 3 else 5)
    adds = '\n'.join(f'p.add("{s}", {d})' for s, d in songs)
    rm = rng.choice(songs)[0]
    code = f'''class Playlist:
    def __init__(self, name):
        self.name = name
        self.titles = []
        self.seconds = 0

    def add(self, title, length):
        self.titles.append(title)
        self.seconds = self.seconds + length

    def remove(self, title, length):
        if title in self.titles:
            self.titles.remove(title)
            self.seconds = self.seconds - length

    def summary(self):
        return self.name + ": " + str(len(self.titles)) + " songs, " + str(self.seconds // 60) + " min " + str(self.seconds % 60) + " s"

p = Playlist("Road trip")
{adds}
p.remove("{rm}", {dict(songs)[rm]})
print(p.summary())'''
    return code


def _gen_grades(rng, slot):
    marks = [rng.randint(3, 7) for _ in range(rng.randint(3, 5))]
    adds = '\n'.join(f's.add_grade({m})' for m in marks)
    code = f'''class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, g):
        if 1 <= g <= 7:
            self.grades.append(g)

    def best(self):
        return max(self.grades)

    def mean(self):
        return round(sum(self.grades) / len(self.grades), 2)

s = Student("{rng.choice(PEOPLE)}")
{adds}
s.add_grade({rng.choice([0, 8, 9])})
print(s.name, len(s.grades), s.best(), s.mean())'''
    return code


def _gen_robot(rng, slot):
    moves = ''.join(rng.choice('NESW') for _ in range(5 if slot.d <= 3 else 8))
    code = f'''class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.steps = 0

    def move(self, d):
        if d == "N":
            self.y += 1
        elif d == "S":
            self.y -= 1
        elif d == "E":
            self.x += 1
        else:
            self.x -= 1
        self.steps += 1

    def distance(self):
        return abs(self.x) + abs(self.y)

r = Robot({rng.randint(-2, 2)}, {rng.randint(-2, 2)})
for d in "{moves}":
    r.move(d)
print(r.x, r.y, r.steps, r.distance())'''
    return code


_OOP1_GENS = [_gen_account, _gen_thermo, _gen_playlist, _gen_grades, _gen_robot]


@R.add('ch09-st1', 'C3', (1, 5), 'short')
def oop1_trace(rng, slot):
    code = rng.choice(_OOP1_GENS)(rng, slot)
    out = run_py(code)
    return dict(stem=_code_q(code), answer=out, markingKey=f'Output:\n{out}\nTrace each method call in order, updating the object\'s attributes (M1); A1 for each correct output line (max 3).', marks=2 if slot.d <= 2 else 3)


@R.add('ch09-st1', 'C3', (2, 5), 'short')
def oop1_java(rng, slot):
    cap = rng.choice([4, 5, 6])
    ops = [rng.choice(['board', 'board', 'leave']) for _ in range(6 if slot.d <= 3 else 9)]
    n = 0
    log = []
    for o in ops:
        if o == 'board':
            if n < cap:
                n += 1
            else:
                log.append('Full')
        else:
            if n > 0:
                n -= 1
    calls = '\n'.join(f'        lift.{o}();' for o in ops)
    code = f'''public class Lift {{
    private int people;
    private final int capacity;

    public Lift(int capacity) {{
        this.capacity = capacity;
        this.people = 0;
    }}

    public void board() {{
        if (people < capacity) {{
            people++;
        }} else {{
            System.out.println("Full");
        }}
    }}

    public void leave() {{
        if (people > 0) {{
            people--;
        }}
    }}

    public int getPeople() {{
        return people;
    }}

    public static void main(String[] args) {{
        Lift lift = new Lift({cap});
{calls}
        System.out.println("People: " + lift.getPeople());
    }}
}}'''
    out = '\n'.join(log + [f'People: {n}'])
    return dict(stem=_code_q(code, 'Java'), answer=out, markingKey=f'Output:\n{out}\nM1 trace of people after each call; A1 "Full" printed at the right times; A1 final count.', marks=3)


_CLASS_SPECS = [
    ('Drone', 'A delivery company in Nairobi tracks each drone\'s ID, battery level and current position, and needs to fly it to a location, recharge it and report whether it can complete a trip of a given distance.',
     ['droneID: String', 'battery: int', 'x: double', 'y: double'], ['flyTo(x, y)', 'recharge()', 'canComplete(distance): boolean']),
    ('Book', 'A library in Oslo stores each book\'s ISBN, title, author and whether it is on loan; books can be lent, returned and checked for availability.',
     ['isbn: String', 'title: String', 'author: String', 'onLoan: boolean'], ['lend()', 'giveBack()', 'isAvailable(): boolean']),
    ('Flight', 'An airline records a flight\'s number, origin, destination, capacity and seats sold; seats can be sold, cancelled and the number of free seats reported.',
     ['flightNo: String', 'origin: String', 'destination: String', 'capacity: int', 'sold: int'], ['sellSeat(): boolean', 'cancelSeat()', 'freeSeats(): int']),
    ('Plant', 'A smart greenhouse in Lisbon monitors each plant\'s species, soil moisture and days since watering, can water it and decides whether it needs water.',
     ['species: String', 'moisture: int', 'daysSinceWatered: int'], ['water()', 'nextDay()', 'needsWater(): boolean']),
    ('Ticket', 'A concert venue in Seoul sells tickets with a code, seat, price and a used flag; tickets can be scanned at the door and refunded if unused.',
     ['code: String', 'seat: String', 'price: double', 'used: boolean'], ['scan(): boolean', 'refund(): double', 'isUsed(): boolean']),
]


@R.add('ch09-st1', 'C3', (2, 4), 'short')
def identify_members(rng, slot):
    cname, desc, attrs, meths = rng.choice(_CLASS_SPECS)
    frame = rng.choice([f'Identify the attributes and methods of a class {cname} for this scenario, giving a data type for each attribute.',
                        f'Design the class {cname}: list suitable attributes (with types) and methods.',
                        f'Outline the state and behaviour that a {cname} object should have.'])
    ans = 'Attributes: ' + ', '.join(attrs) + '. Methods: ' + ', '.join(meths) + '.'
    return dict(stem=f'{desc} {frame}', answer=ans, markingKey=ans + ' 1 mark per two suitable attributes with types; 1 mark per two suitable methods; state = attributes, behaviour = methods.', marks=4)


R.facts('ch09-st1', F(
    terms=[('class', 'a template or blueprint that defines the attributes (data) and methods (behaviour) that its objects will have'),
           ('object', 'an instance of a class, with its own values for the attributes defined by the class'),
           ('attribute', 'a variable that belongs to an object or class and stores part of its state'),
           ('method', 'a function defined in a class that describes a behaviour of its objects and can access their attributes'),
           ('state', 'the values of all of an object\'s attributes at a particular time'),
           ('instantiation', 'creating a new object from a class'),
           ('object-oriented programming (OOP)', 'a programming paradigm in which programs are built from interacting objects that combine data and the methods that operate on it')],
    facts=[('In OOP, what is the relationship between a class and an object?', 'An object is an instance of a class', ['A class is an instance of an object', 'They are the same thing', 'An object contains many classes'], 'The class is the blueprint, the object is built from it.'),
           ('Which of these is most likely to be a method of a class Car?', 'accelerate(amount)', ['colour', 'registrationNumber', 'Car'], 'Methods are behaviours; the others are attributes or the class name.'),
           ('Two objects of the same class…', 'have the same attributes and methods but may hold different attribute values', ['must hold identical values', 'share a single copy of every instance attribute', 'cannot exist at the same time'], 'Each object has its own state.')],
    why=[('Explain why OOP can make large programs easier to maintain.', 'Code is organised into classes that bundle related data and behaviour; changes are localised inside a class, classes can be reused, and encapsulation hides implementation details from the rest of the program.'),
         ('Explain why a method is used to change an attribute rather than changing it directly from outside the class.', 'The method can validate the change and keep the object in a valid state, and the internal representation can later change without affecting code that uses the class.'),
         ('Explain the difference in memory between creating one class and creating three objects of that class.', 'The class definition (methods) exists once; each of the three objects has its own separate storage for its instance attributes.')],
    contrast=[('a class', 'an object', 'A class is a blueprint describing attributes and methods; an object is a specific instance created from it with its own attribute values.'),
              ('an attribute', 'a method', 'An attribute stores data (state) of an object; a method is code that defines what the object can do (behaviour).'),
              ('procedural programming', 'object-oriented programming', 'Procedural programming organises code as procedures operating on separate data; OOP bundles data and the methods that act on it into objects.')],
    misc=[('Every object of a class always has the same attribute values.', 'Objects share the attribute names and methods, but each has its own values (state).'),
          ('Creating a class automatically creates an object.', 'A class only defines the structure; an object exists only when it is instantiated (e.g. new Car() or Car()).'),
          ('A method can only read attributes, never change them.', 'Methods (mutators) can change attributes; others (accessors) only read them.')],
    evaluate=[('Object-oriented programming is always the best paradigm for a programming project.', ['models real-world entities naturally', 'encapsulation and reuse aid large team projects', 'supports inheritance and polymorphism'], ['adds overhead and boilerplate for small scripts', 'functional or procedural styles can be clearer for data pipelines and maths', 'poorly designed class hierarchies become complex'], 'OOP is well suited to large systems modelling interacting entities; for small or data-transformation tasks other paradigms may be simpler.')],
))
ar('ch09-st1', [
    ('Two objects of the same class can have different states.', 'Each object stores its own values for instance attributes.', 0, 'Both true; R explains A.'),
    ('A class is an instance of an object.', 'Objects are created from classes.', 3, 'A is false (the reverse); R is true.'),
    ('Methods define the behaviour of objects.', 'Methods are written inside the class definition.', 1, 'Both true, but where methods are written does not explain why they represent behaviour.'),
])


# ---- constructors ----
@R.add('ch09-st2', 'C3', (1, 5), 'short')
def ctor_defaults(rng, slot):
    cls = rng.choice(['Room', 'Order', 'Pet'])
    if cls == 'Room':
        code = f'''class Room:
    def __init__(self, number, beds=2, rate=80):
        self.number = number
        self.beds = beds
        self.rate = rate * beds

r1 = Room({rng.randint(100, 120)})
r2 = Room({rng.randint(200, 220)}, {rng.choice([1, 3])})
r3 = Room({rng.randint(300, 320)}, rate={rng.choice([60, 95])})
print(r1.number, r1.rate)
print(r2.number, r2.rate)
print(r3.number, r3.beds, r3.rate)'''
    elif cls == 'Order':
        code = f'''class Order:
    next_id = {rng.choice([1, 100, 500])}

    def __init__(self, item, qty=1):
        self.id = Order.next_id
        Order.next_id += 1
        self.item = item
        self.qty = qty

a = Order("{rng.choice(['tea', 'rice', 'mango'])}")
b = Order("{rng.choice(['pens', 'eggs', 'soap'])}", {rng.randint(2, 6)})
c = Order(qty={rng.randint(7, 9)}, item="{rng.choice(['kites', 'lamps'])}")
print(a.id, a.item, a.qty)
print(b.id, b.qty, c.id, c.item)'''
    else:
        code = f'''class Pet:
    def __init__(self, name, species="cat", age=0):
        self.name = name
        self.species = species
        self.age = age
        print("Created", self.name)

p = Pet("{rng.choice(['Simba', 'Luna', 'Kiko'])}", age={rng.randint(1, 9)})
q = Pet("{rng.choice(['Rex', 'Momo', 'Pip'])}", "{rng.choice(['dog', 'rabbit', 'parrot'])}")
q.age = p.age + {rng.randint(1, 3)}
print(p.species, p.age, q.species, q.age)'''
    out = run_py(code)
    return dict(stem=_code_q(code), answer=out, markingKey=f'Output:\n{out}\nM1 constructor defaults/keyword arguments applied correctly; A1 per correct line.', marks=3)


@R.add('ch09-st2', 'C3', (2, 5), 'short')
def ctor_alias(rng, slot):
    a, b = rng.randint(1, 9), rng.randint(10, 19)
    code = f'''class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point({a}, {b})
q = p
r = Point(p.x, p.y)
q.x = q.x + {rng.randint(2, 5)}
r.y = {rng.randint(20, 30)}
print(p.x, p.y)
print(q.x, q.y)
print(r.x, r.y)
print(p is q, p is r)'''
    out = run_py(code)
    return dict(stem=_code_q(code) + ' Explain why p and q are affected differently from r.',
                answer=out + '\nq = p copies the reference, so p and q refer to the same object; r is a separate object created by the constructor.',
                markingKey=f'Output:\n{out}\nA1 per line (max 3); R1 reference vs new object.', marks=4)


@R.add('ch09-st2', 'C3', (2, 5), 'short')
def ctor_java(rng, slot):
    w, h = rng.randint(2, 9), rng.randint(2, 9)
    s = rng.randint(2, 9)
    code = f'''public class Rect {{
    private int width;
    private int height;

    public Rect() {{
        this(1, 1);
    }}

    public Rect(int side) {{
        this(side, side);
    }}

    public Rect(int width, int height) {{
        this.width = width;
        this.height = height;
    }}

    public int area() {{
        return width * height;
    }}

    public static void main(String[] args) {{
        Rect a = new Rect();
        Rect b = new Rect({s});
        Rect c = new Rect({w}, {h});
        System.out.println(a.area() + " " + b.area() + " " + c.area());
        System.out.println(a.area() + b.area() + c.area());
    }}
}}'''
    out = f'1 {s * s} {w * h}\n{1 + s * s + w * h}'
    return dict(stem=_code_q(code, 'Java') + ' Identify which constructor is called for each object.',
                answer=out + '\na: no-argument constructor (which calls this(1, 1)); b: one-argument constructor (this(side, side)); c: two-argument constructor.',
                markingKey=f'Output:\n{out}\nA1 first line (string concatenation); A1 second line (integer addition before printing); R1 constructor overloading resolved by number of arguments.', marks=4)


R.facts('ch09-st2', F(
    terms=[('constructor', 'a special method that is called automatically when an object is created and initialises its attributes'),
           ('default constructor', 'a constructor that takes no parameters and gives attributes default values'),
           ('parameterised constructor', 'a constructor that takes arguments used to set the initial attribute values'),
           ('this / self', 'a reference to the current object, used inside methods and constructors to access its own attributes'),
           ('object reference', 'a value that refers to where an object is stored in memory; variables of class type hold references, not the objects themselves'),
           ('constructor overloading', 'defining several constructors with different parameter lists in the same class (e.g. in Java)')],
    facts=[('In Java, which statement creates a new object of class Student?', 'Student s = new Student("Mei", 12);', ['Student s = Student.create;', 'new s = Student("Mei", 12);', 'Student s;'], 'new calls the constructor and returns a reference.'),
           ('What does self (Python) / this (Java) refer to inside a constructor?', 'The object being created', ['The class itself', 'The previous object created', 'The main method'], 'It is the current instance.'),
           ('A constructor\'s name in Java must…', 'be the same as the class name and have no return type', ['start with "init"', 'return void', 'be static'], 'That is the Java rule.')],
    why=[('Explain why a constructor is used rather than setting each attribute after creating the object.', 'It guarantees that every object starts in a valid, fully initialised state in one step; required values cannot be forgotten and validation can be applied once.'),
         ('Explain why this.name = name is needed in a constructor whose parameter is also called name.', 'The parameter shadows the attribute; this.name refers to the object\'s attribute while name refers to the parameter, so the value is copied into the object.'),
         ('Explain why assigning one object variable to another does not copy the object.', 'Object variables hold references; the assignment copies the reference, so both variables refer to the same object and changes through one are seen through the other.')],
    contrast=[('a constructor', 'an ordinary method', 'A constructor runs once automatically when an object is created and initialises it (no return type); an ordinary method is called explicitly any number of times and may return a value.'),
              ('a default constructor', 'a parameterised constructor', 'A default constructor takes no arguments and sets default values; a parameterised constructor takes arguments to set initial values.'),
              ('copying a reference', 'creating a new object', 'Copying a reference makes two variables refer to the same object; creating a new object (calling the constructor) allocates a separate object with its own state.')],
    misc=[('A constructor must return the new object using a return statement.', 'Constructors have no return type; new (Java) or calling the class (Python) returns the reference automatically.'),
          ('If you write a constructor with parameters, Java still provides a no-argument constructor automatically.', 'Java only supplies a default constructor when no constructor is written; once one is defined, a no-argument constructor must be written explicitly if needed.'),
          ('b = a creates a copy of object a.', 'It copies the reference only; a and b now refer to the same object.')],
    evaluate=[('Constructors should validate all of their arguments and refuse to create invalid objects.', ['objects are always in a valid state', 'errors are detected early, close to their cause'], ['extra code and processing', 'some objects are legitimately built step by step (builders)', 'exceptions in constructors must be handled by callers'], 'Validating in constructors is good practice for invariants that must always hold; flexible construction patterns can be used where objects are assembled gradually.')],
))
ar('ch09-st2', [
    ('A constructor is called automatically when an object is instantiated.', 'A Java constructor has the same name as its class.', 1, 'Both true, but the naming rule does not explain why the constructor runs automatically.'),
    ('In Java a class can have more than one constructor.', 'Constructors can be overloaded with different parameter lists.', 0, 'Both true; R explains A.'),
    ('A Java constructor must have the return type void.', 'Constructors have the same name as the class.', 3, 'A is false (no return type at all); R is true.'),
])


# ---- encapsulation ----
@R.add('ch09-st3', 'C3', (1, 5), 'short')
def setter_trace(rng, slot):
    cls, attr, lo, hi = rng.choice([('Athlete', 'age', 12, 40), ('Sensor', 'level', 0, 100), ('Exam', 'mark', 0, 100), ('Speaker', 'volume', 0, 10)])
    start = rng.randint(lo, hi)
    tries = rng.sample([lo - 3, lo, (lo + hi) // 2, hi, hi + 5, rng.choice([lo + 1, hi - 1])], 3 if slot.d <= 2 else 5)
    calls = '\n'.join(f'print(o.set_{attr}({v}), o.get_{attr}())' for v in tries)
    code = f'''class {cls}:
    def __init__(self, {attr}):
        self.__{attr} = {attr}

    def get_{attr}(self):
        return self.__{attr}

    def set_{attr}(self, value):
        if {lo} <= value <= {hi}:
            self.__{attr} = value
            return True
        return False

o = {cls}({start})
{calls}'''
    out = run_py(code)
    return dict(stem=_code_q(code) + (' Explain how this design demonstrates encapsulation.' if slot.d >= 4 else ''),
                answer=out + ('\nThe attribute is private (name-mangled __' + attr + ') and can only be changed through the validating setter.' if slot.d >= 4 else ''),
                markingKey=f'Output:\n{out}\nA1 per correct pair of lines; invalid values return False and leave the attribute unchanged.' + (' R1 private attribute + controlled access via getter/setter.' if slot.d >= 4 else ''), marks=3 if slot.d <= 3 else 4)


_ENC_ERR = [
    ('''public class Card {
    private int pin;
    public Card(int pin) { this.pin = pin; }
}
class Main {
    public static void main(String[] args) {
        Card c = new Card(4321);
        System.out.println(c.pin);
    }
}''', 'c.pin in Main: pin is private, so it cannot be accessed outside Card (compile error). Provide a public method (e.g. checkPin(int)) rather than exposing the PIN.'),
    ('''public class Temperature {
    private double celsius;
    public double getCelsius() { return celsius; }
    public void setCelsius(double c) { c = celsius; }
}''', 'The setter assigns the wrong way round: c = celsius should be this.celsius = c, so the attribute is never updated.'),
    ('''public class Account {
    private double balance;
    public void setBalance(double b) { balance = b; }
    public double getBalance() { return balance; }
}''', 'Not a compile error but poor encapsulation: the public setter lets any code set any balance (even negative), bypassing deposit/withdraw rules. Replace it with validated deposit() and withdraw() methods.'),
    ('''public class Student {
    private String name;
    public String getName() { return name; }
    private void setName(String n) { name = n; }
}
// elsewhere:  s.setName("Kwame");''', 'setName is private, so s.setName("Kwame") outside Student does not compile; make the setter public (with validation) if names may be changed.'),
]


@R.add('ch09-st3', 'C2', (2, 4), 'explain')
def enc_error(rng, slot):
    code, fix = rng.choice(_ENC_ERR)
    frame = rng.choice(['Identify the problem with this Java code and explain how to correct it.', 'Explain why this code does not behave as intended with respect to encapsulation, and suggest a correction.'])
    return dict(stem=f'{frame}\n{code}', answer=fix, markingKey=f'{fix} 1 mark identification, 1-2 marks explanation/correction.', type='explain', marks=3, gap='G2')


R.facts('ch09-st3', F(
    terms=[('encapsulation', 'bundling an object\'s data with the methods that operate on it and restricting direct access to the data from outside the class'),
           ('access modifier', 'a keyword (public, private, protected) that controls where a class member can be accessed from'),
           ('private', 'an access modifier meaning the member can be accessed only from inside its own class'),
           ('public', 'an access modifier meaning the member can be accessed from any other class'),
           ('getter (accessor)', 'a method that returns the value of a private attribute'),
           ('setter (mutator)', 'a method that changes the value of a private attribute, usually after validating the new value'),
           ('information hiding', 'concealing the internal details of a class so that other code depends only on its public interface')],
    facts=[('Which access modifier should normally be used for attributes in a well-encapsulated Java class?', 'private', ['public', 'static', 'final'], 'Attributes are hidden and accessed through methods.'),
           ('In Python, how is an attribute conventionally marked as private?', 'By starting its name with underscores, e.g. self.__balance', ['With the keyword private', 'By writing it in capitals', 'By declaring it outside the class'], 'Python uses naming conventions (and name mangling for __).'),
           ('Which is the main benefit of a setter compared with a public attribute?', 'It can validate values before changing the attribute', ['It runs faster', 'It uses less memory', 'It makes the attribute static'], 'Validation keeps the object in a valid state.')],
    why=[('Explain why attributes are usually made private.', 'Other code cannot put the object into an invalid state or depend on its internal representation; all changes go through methods that can validate them, so the implementation can change without breaking other code.'),
         ('Explain why not every private attribute should have a public setter.', 'Some attributes must not change freely (an ID, a balance that changes only through deposits/withdrawals); providing a setter would bypass the class\'s rules and weaken encapsulation.'),
         ('Explain how encapsulation helps teams of programmers work on the same project.', 'Each class exposes a stable public interface; programmers using it do not need to know or depend on its internals, so classes can be developed, tested and changed independently.')],
    contrast=[('a getter', 'a setter', 'A getter returns the value of a private attribute without changing it; a setter changes the attribute, ideally after validation.'),
              ('private', 'protected', 'A private member is accessible only inside its own class; a protected member is also accessible in subclasses (and, in Java, the same package).'),
              ('encapsulation', 'abstraction', 'Encapsulation hides an object\'s data behind methods; abstraction hides complexity by exposing only the essential features of an object or operation.')],
    misc=[('Making attributes private means they can never be changed.', 'Private attributes can be changed by the class\'s own methods, including setters; private only restricts direct outside access.'),
          ('Encapsulation is just about adding a getter and setter for every attribute.', 'Automatic getters/setters for everything can expose internal state; encapsulation is about providing only the operations that keep objects valid.'),
          ('Python\'s double underscore makes an attribute completely inaccessible.', 'It triggers name mangling (_ClassName__attr), which discourages access but does not prevent it; privacy in Python is by convention.')],
    evaluate=[('Strict encapsulation makes programs harder to write without bringing real benefits.', ['more code (getters, setters, validation)', 'can slow down quick prototypes'], ['prevents invalid states and accidental misuse', 'allows internal changes without breaking other code', 'essential for maintainability in large systems'], 'The extra code is a small cost compared with the safety and maintainability benefits in anything beyond a small script.')],
))
ar('ch09-st3', [
    ('A setter can prevent an attribute being given an invalid value.', 'A setter can contain validation code before assigning the value.', 0, 'Both true; R explains A.'),
    ('Private attributes can be accessed directly from a subclass in Java.', 'Private members are visible only within the class that declares them.', 3, 'A is false; R is true and explains why.'),
])


# ---- static vs instance ----
@R.add('ch09-st4', 'C3', (1, 5), 'short')
def static_trace(rng, slot):
    n = rng.randint(2, 4)
    extra = rng.randint(1, 3)
    code = f'''class Visitor:
    count = 0

    def __init__(self, name):
        self.name = name
        self.visits = 0
        Visitor.count += 1

    def visit(self):
        self.visits += 1

people = []
for nm in {[rng.choice(PEOPLE) for _ in range(n)]}:
    people.append(Visitor(nm))
for i in range({extra}):
    people[0].visit()
people[-1].visit()
print(Visitor.count, people[0].visits, people[-1].visits)'''
    if slot.d >= 4:
        code += '''
people[1].count = 99
print(Visitor.count, people[1].count, people[0].count)'''
    out = run_py(code)
    return dict(stem=_code_q(code) + (' Explain the output of the last line.' if slot.d >= 4 else ''),
                answer=out + ('\npeople[1].count = 99 creates a new instance attribute on that object only, shadowing the class (static) attribute; Visitor.count is unchanged.' if slot.d >= 4 else ''),
                markingKey=f'Output:\n{out}\nM1 class attribute shared by all objects; A1 per line.' + (' R1 instance attribute shadows class attribute.' if slot.d >= 4 else ''), marks=3 if slot.d <= 3 else 4)


@R.add('ch09-st4', 'C3', (2, 5), 'short')
def static_java(rng, slot):
    n = rng.randint(2, 5)
    rate = rng.choice([2, 3, 5])
    newr = rng.choice([4, 6, 10])
    code = f'''public class Tax {{
    static int rate = {rate};
    int id;
    static int created = 0;

    Tax() {{
        created++;
        id = created;
    }}

    static int apply(int amount) {{
        return amount + amount * rate / 100;
    }}

    public static void main(String[] args) {{
        Tax last = null;
        for (int i = 0; i < {n}; i++) {{
            last = new Tax();
        }}
        System.out.println(Tax.created + " " + last.id);
        System.out.println(Tax.apply(200));
        Tax.rate = {newr};
        System.out.println(Tax.apply(200));
    }}
}}'''
    out = f'{n} {n}\n{200 + 200 * rate // 100}\n{200 + 200 * newr // 100}'
    return dict(stem=_code_q(code, 'Java') + ' Explain why apply can be called without creating an object.',
                answer=out + '\napply is static: it belongs to the class, uses only the static rate and no instance data, so it is called as Tax.apply(...).',
                markingKey=f'Output:\n{out}\nA1 per line; R1 static methods belong to the class.', marks=4)


R.facts('ch09-st4', F(
    terms=[('static (class) variable', 'a variable that belongs to the class itself, with a single copy shared by all objects of the class'),
           ('instance variable', 'a variable that belongs to an individual object, so each object has its own copy'),
           ('static method', 'a method that belongs to the class rather than an object, called using the class name and unable to access instance variables directly'),
           ('instance method', 'a method that is called on an object and can access that object\'s instance variables'),
           ('class constant', 'a static final (Java) / conventionally upper-case (Python) value shared by all objects and never changed, such as MAX_SPEED')],
    facts=[('A class Student keeps a count of how many Student objects have been created. This count should be…', 'a static variable', ['an instance variable', 'a local variable in the constructor', 'a parameter'], 'One shared counter for the whole class.'),
           ('Why can a static method not use this?', 'It is not called on any particular object', ['It is private', 'It must return void', 'It is always abstract'], 'There is no current instance.'),
           ('Math.sqrt(16) in Java is an example of…', 'calling a static method', ['creating an object', 'calling an instance method', 'accessing a private attribute'], 'It is called on the class name.')],
    why=[('Explain why a static method cannot directly access instance variables.', 'A static method is called on the class, not on an object, so there is no particular object whose instance variables it could use.'),
         ('Explain why a running total of all orders placed should be a static variable.', 'The total relates to the class as a whole, not to any single order; a static variable has one shared copy updated by every object, whereas instance variables would give each order its own separate total.'),
         ('Explain why utility functions such as unit conversions are often written as static methods.', 'They depend only on their parameters and not on any object\'s state, so creating an object to call them would be unnecessary.')],
    contrast=[('a static variable', 'an instance variable', 'A static variable has one copy shared by all objects of the class; an instance variable has a separate copy in each object.'),
              ('a static method', 'an instance method', 'A static method is called on the class and cannot use instance data; an instance method is called on an object and can use its attributes.')],
    misc=[('Changing a static variable through one object only affects that object.', 'In Java there is only one copy, so the change is seen by all objects (in Python, assigning via an instance creates a new instance attribute instead).'),
          ('Static methods can call instance methods directly without an object.', 'They need an object reference to call an instance method.'),
          ('Every variable in a class should be static to save memory.', 'Data that differs between objects must be instance variables; making it static would make all objects share one value.')],
    evaluate=[('Static variables should be avoided in object-oriented design.', ['shared mutable state makes testing and concurrency harder', 'hidden dependencies between objects'], ['appropriate for constants, counters and configuration', 'static utility methods are simple and efficient'], 'Static constants and stateless utility methods are good practice; shared mutable static state should be minimised and carefully controlled.')],
))
ar('ch09-st4', [
    ('A static variable is shared by all instances of a class.', 'Only one copy of a static variable exists, stored with the class.', 0, 'Both true; R explains A.'),
    ('A static method can use the keyword this.', 'Static methods are called on the class rather than on an object.', 3, 'A is false; R is true and explains why.'),
])


# ---- UML for one class ----
def _uml(cname, attrs, meths):
    return f'{cname}\n' + '\n'.join(attrs) + '\n' + '\n'.join(meths)


_UML_SPECS = [
    ('Locker', [('lockerNo', 'int', '-'), ('code', 'String', '-'), ('occupied', 'boolean', '-')], [('Locker', 'lockerNo: int', ''), ('open', 'attempt: String', 'boolean'), ('isOccupied', '', 'boolean'), ('getLockerNo', '', 'int')]),
    ('Vaccine', [('name', 'String', '-'), ('dosesInStock', 'int', '-'), ('totalCreated', 'int', '- static')], [('Vaccine', 'name: String, doses: int', ''), ('administer', '', 'boolean'), ('restock', 'n: int', 'void'), ('getTotalCreated', '', 'int static')]),
    ('Parcel', [('trackingID', 'String', '-'), ('weightKg', 'double', '-'), ('delivered', 'boolean', '-')], [('Parcel', 'id: String, w: double', ''), ('cost', '', 'double'), ('markDelivered', '', 'void'), ('isDelivered', '', 'boolean')]),
    ('Bus', [('route', 'String', '-'), ('capacity', 'int', '-'), ('passengers', 'int', '-')], [('Bus', 'route: String, capacity: int', ''), ('board', 'n: int', 'boolean'), ('alight', 'n: int', 'void'), ('getFreeSeats', '', 'int')]),
]


def _uml_lines(cname, attrs, meths):
    a = [f'{v[0]} {n}: {t}' + (' {static}' if 'static' in v else '') for n, t, v in attrs]
    m = []
    for nm, ps, ret in meths:
        if nm == cname:
            m.append(f'+ {nm}({ps})')
        else:
            static = ' {static}' if 'static' in ret else ''
            m.append(f'+ {nm}({ps}): {ret.replace(" static", "")}{static}')
    return a, m


@R.add('ch09-st5', 'C3', (1, 5), 'short')
def uml_read(rng, slot):
    cname, attrs, meths = rng.choice(_UML_SPECS)
    a, m = _uml_lines(cname, attrs, meths)
    box = f'+-----------------------------+\n| {cname}\n+-----------------------------+\n' + '\n'.join(f'| {x}' for x in a) + '\n+-----------------------------+\n' + '\n'.join(f'| {x}' for x in m) + '\n+-----------------------------+'
    q = rng.choice(['attrs', 'ctor', 'code'] if slot.d >= 3 else ['attrs', 'ctor'])
    if q == 'attrs':
        priv = [n for n, _, v in attrs if v.startswith('-')]
        ret = [f'{nm} returns {r.replace(" static", "")}' for nm, _, r in meths if nm != cname]
        ans = f'Private attributes: {", ".join(priv)}. ' + '; '.join(ret) + '. "-" means private, "+" means public.'
        stem = f'The UML class diagram below describes a class.\n{box}\nList the private attributes, state the return type of each method, and explain the meaning of the symbols - and +.'
        mk = 3
    elif q == 'ctor':
        ctor = next(x for x in meths if x[0] == cname)
        ans = f'Constructor {cname}({ctor[1]}); it has no return type and initialises the attributes ' + ', '.join(n for n, _, _ in attrs) + '.'
        stem = f'Study this UML class diagram.\n{box}\nIdentify the constructor, its parameters, and explain how you can tell it is a constructor.'
        mk = 2
    else:
        jt = {'int': 'int', 'String': 'String', 'boolean': 'boolean', 'double': 'double'}
        fields = '\n'.join(f'    private {"static " if "static" in v else ""}{jt[t]} {n};' for n, t, v in attrs)
        sigs = []
        for nm, ps, ret in meths:
            params = ', '.join(f'{p.split(": ")[1]} {p.split(": ")[0]}' for p in ps.split(', ')) if ps else ''
            if nm == cname:
                sigs.append(f'    public {nm}({params}) {{ ... }}')
            else:
                st_ = 'static ' if 'static' in ret else ''
                sigs.append(f'    public {st_}{ret.replace(" static", "")} {nm}({params}) {{ ... }}')
        ans = f'public class {cname} {{\n{fields}\n' + '\n'.join(sigs) + '\n}'
        stem = f'Write the Java class skeleton (attribute declarations and method headers, no method bodies) for the class shown in this UML diagram.\n{box}'
        mk = 4
    return dict(stem=stem, answer=ans, markingKey=ans + f' Award marks for correct visibility, types, static members and return types ({mk} marks).', marks=mk)


@R.add('ch09-st5', 'C3', (2, 5), 'short')
def uml_from_code(rng, slot):
    cname, attrs, meths = rng.choice(_UML_SPECS)
    py_t = {'int': 'int', 'String': 'str', 'boolean': 'bool', 'double': 'float'}
    ctor = next(x for x in meths if x[0] == cname)
    params = ', '.join(p.split(': ')[0] for p in ctor[1].split(', '))
    lines_ = [f'class {cname}:']
    for n, t, v in attrs:
        if 'static' in v:
            lines_.append(f'    __{n} = 0  # class attribute')
    lines_.append(f'    def __init__(self, {params}):')
    for n, t, v in attrs:
        if 'static' not in v:
            lines_.append(f'        self.__{n} = ...  # {py_t[t]}')
    for nm, ps, ret in meths:
        if nm == cname:
            continue
        pp = ', '.join(p.split(': ')[0] for p in ps.split(', ')) if ps else ''
        dec = '    @staticmethod\n' if 'static' in ret else ''
        lines_.append(f'{dec}    def {nm}({"self" if not dec else ""}{", " if pp and not dec else ""}{pp}) -> {py_t.get(ret.replace(" static", ""), "None")}:\n        ...')
    code = '\n'.join(lines_)
    a, m = _uml_lines(cname, attrs, meths)
    ans = f'{cname}\n' + '\n'.join(a) + '\n' + '\n'.join(m)
    return dict(stem=f'Draw (as text) the UML class diagram for this Python class, using - for private and + for public members and showing types.\n{code}',
                answer=ans, markingKey=f'Three compartments: name / attributes / methods (1). Attributes with visibility and types (1-2). Methods with parameters and return types, static marked (1-2). Model:\n{ans}', marks=4)


R.facts('ch09-st5', F(
    terms=[('UML (Unified Modelling Language)', 'a standard visual notation for modelling the structure and behaviour of software systems'),
           ('class diagram', 'a UML diagram showing a class as a box divided into name, attributes and methods compartments'),
           ('visibility', 'the accessibility of a class member, shown in UML by + (public), - (private) and # (protected)'),
           ('return type (UML)', 'the type written after a colon at the end of a method, e.g. + getAge(): int')],
    facts=[('In a UML class diagram, what does "- balance: double" mean?', 'A private attribute named balance of type double', ['A public method returning double', 'A static constant called balance', 'A protected attribute named double'], '"-" = private; type after the colon.'),
           ('In UML, which symbol shows a protected member?', '#', ['+', '-', '~'], '# = protected.'),
           ('How is a static member shown in a UML class diagram?', 'It is underlined (or marked {static})', ['It is written in capitals', 'It has a # symbol', 'It is placed in the name compartment'], 'Static members are underlined.')],
    why=[('Explain why UML class diagrams are produced before writing code.', 'They let designers agree the classes, attributes, methods and visibility independently of any language, spot design problems early and communicate the design to the whole team.'),
         ('Explain why a UML class diagram is language-independent.', 'It describes the structure (names, types, visibility, relationships) using standard notation that can be implemented in Java, Python or any OOP language.')],
    contrast=[('the attributes compartment', 'the methods compartment', 'The attributes compartment lists the data members with visibility and type; the methods compartment lists operations with parameters and return types.'),
              ('+ (public)', '- (private)', '+ marks a member accessible from outside the class; - marks a member accessible only inside the class.')],
    misc=[('In UML the return type of a method is written before the method name.', 'UML writes it after a colon at the end: + getName(): String (Java writes it before the name).'),
          ('A UML class diagram shows the values stored in each object.', 'It shows the structure of the class (attributes, types, methods); values belong to object diagrams or runtime state.')],
    evaluate=[('Detailed UML diagrams are unnecessary in agile software development.', ['agile values working software over documentation', 'diagrams quickly become outdated'], ['lightweight UML helps teams agree designs and onboard members', 'complex systems need a shared model', 'required for documentation in assessed work such as the IA'], 'Lightweight, up-to-date UML sketches remain valuable even in agile teams; exhaustive diagrams are rarely justified.')],
))
ar('ch09-st5', [
    ('In UML, - before an attribute means it is private.', 'UML class diagrams can be implemented in any object-oriented language.', 1, 'Both true, but language independence does not explain the meaning of the - symbol.'),
    ('A UML class box has three compartments.', 'They hold the class name, the attributes and the methods.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# ch10 B3.2 Features of OOP for multiple classes (HL)
# =============================================================================================
def _gen_inherit(rng, slot):
    kind = rng.choice(['vehicle', 'staff', 'account', 'media'])
    if kind == 'vehicle':
        w = rng.randint(2, 6)
        code = f'''class Vehicle:
    def __init__(self, reg, wheels):
        self.reg = reg
        self.wheels = wheels

    def describe(self):
        return self.reg + " has " + str(self.wheels) + " wheels"

    def toll(self):
        return self.wheels * {rng.choice([2, 3, 5])}

class Truck(Vehicle):
    def __init__(self, reg, wheels, tonnes):
        super().__init__(reg, wheels)
        self.tonnes = tonnes

    def toll(self):
        return super().toll() + self.tonnes * {rng.choice([4, 10, 12])}

v = Vehicle("KDA 123A", {rng.choice([2, 4])})
t = Truck("KBZ 9{rng.randint(10, 99)}T", {rng.choice([6, 8, 10])}, {rng.randint(3, 20)})
print(v.describe(), v.toll())
print(t.describe(), t.toll())
print(isinstance(t, Vehicle), isinstance(v, Truck))'''
    elif kind == 'staff':
        code = f'''class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def bonus(self):
        return self.salary // {rng.choice([10, 20])}

    def info(self):
        return self.name + " " + str(self.salary + self.bonus())

class Manager(Employee):
    def __init__(self, name, salary, team):
        super().__init__(name, salary)
        self.team = team

    def bonus(self):
        return super().bonus() + {rng.choice([100, 250, 500])} * self.team

e = Employee("{rng.choice(PEOPLE)}", {rng.choice([3000, 4000, 5200])})
m = Manager("{rng.choice(PEOPLE)}", {rng.choice([6000, 7000, 8400])}, {rng.randint(2, 6)})
for p in [e, m]:
    print(p.info())'''
    elif kind == 'account':
        code = f'''class Account:
    def __init__(self, balance):
        self.balance = balance

    def month_end(self):
        self.balance -= {rng.choice([1, 2, 5])}

class Savings(Account):
    def __init__(self, balance, rate):
        super().__init__(balance)
        self.rate = rate

    def month_end(self):
        self.balance += self.balance * self.rate // 100

a = Account({rng.choice([100, 200, 500])})
s = Savings({rng.choice([1000, 2000, 400])}, {rng.choice([1, 2, 5])})
for month in range({rng.randint(2, 3)}):
    a.month_end()
    s.month_end()
print(a.balance, s.balance)'''
    else:
        code = f'''class Media:
    count = 0

    def __init__(self, title):
        self.title = title
        Media.count += 1

    def play(self):
        return "Playing " + self.title

class Podcast(Media):
    def __init__(self, title, episode):
        super().__init__(title)
        self.episode = episode

    def play(self):
        return super().play() + " episode " + str(self.episode)

class Song(Media):
    pass

items = [Song("{rng.choice(['Pata Pata', 'Fado Triste', 'Bamboleo'])}"), Podcast("{rng.choice(['TechTalk', 'CS Daily', 'Data Bytes'])}", {rng.randint(1, 40)}), Song("{rng.choice(['Lambada', 'Gangnam', 'Despacito'])}")]
for it in items:
    print(it.play())
print(Media.count)'''
    return code


@R.add('ch10-st1', 'C3', (1, 5), 'short')
def inherit_trace(rng, slot):
    code = _gen_inherit(rng, slot)
    out = run_py(code)
    return dict(stem=_code_q(code), answer=out, markingKey=f'Output:\n{out}\nM1 subclass constructor calls super().__init__; M1 overridden method (and super() call) used for subclass objects; A1 per line.', marks=3 if slot.d <= 3 else 4)


@R.add('ch10-st1', 'C3', (2, 5), 'short')
def inherit_java(rng, slot):
    base_speed = rng.randint(10, 30)
    extra = rng.randint(5, 20)
    k = rng.randint(2, 4)
    code = f'''class Animal {{
    protected String name;
    protected int speed;

    public Animal(String name) {{
        this.name = name;
        this.speed = {base_speed};
        System.out.println("Animal " + name);
    }}

    public int run(int minutes) {{
        return speed * minutes;
    }}
}}

class Cheetah extends Animal {{
    public Cheetah(String name) {{
        super(name);
        speed = speed + {extra};
        System.out.println("Cheetah " + name);
    }}

    @Override
    public int run(int minutes) {{
        return super.run(minutes) * 2;
    }}
}}

public class Main {{
    public static void main(String[] args) {{
        Animal a = new Cheetah("Kasi");
        System.out.println(a.run({k}));
    }}
}}'''
    out = f'Animal Kasi\nCheetah Kasi\n{(base_speed + extra) * k * 2}'
    return dict(stem=_code_q(code, 'Java') + ' Explain the order of the first two lines.',
                answer=out + '\nThe Cheetah constructor calls super(name) first, so the Animal constructor runs (and prints) before the rest of the Cheetah constructor.',
                markingKey=f'Output:\n{out}\nA1 order of constructor output; A1 speed {base_speed} + {extra}; A1 overridden run uses super.run × 2; R1 explanation of constructor chaining.', marks=4)


R.facts('ch10-st1', F(
    terms=[('inheritance', 'a mechanism by which a subclass acquires the attributes and methods of a superclass and can add to or modify them'),
           ('superclass (parent class)', 'the more general class whose attributes and methods are inherited'),
           ('subclass (child class)', 'a more specialised class that inherits from a superclass and may add or override members'),
           ('super', 'a keyword used in a subclass to call the superclass\'s constructor or methods'),
           ('"is-a" relationship', 'the relationship modelled by inheritance: a subclass object is a kind of superclass object (a Truck is a Vehicle)'),
           ('protected', 'an access modifier allowing access from within the class and its subclasses')],
    facts=[('In Java, class Cat extends Animal means…', 'Cat is a subclass that inherits from Animal', ['Animal inherits from Cat', 'Cat and Animal are unrelated', 'Cat contains an Animal attribute'], 'extends declares inheritance.'),
           ('Which relationship is best modelled by inheritance?', 'A SavingsAccount is an Account', ['A Car has an Engine', 'A Library has Books', 'A Student uses a Locker'], '"is-a" relationships suit inheritance; "has-a" suits composition.'),
           ('In Python, which line calls the superclass constructor inside a subclass constructor?', 'super().__init__(name)', ['self.__init__(name)', 'parent(name)', 'Super.new(name)'], 'super() refers to the parent class.')],
    why=[('Explain how inheritance reduces code duplication.', 'Common attributes and methods are written once in the superclass and automatically available to every subclass, so changes are made in one place and subclasses only contain what is different.'),
         ('Explain why a subclass constructor usually calls the superclass constructor.', 'The superclass constructor initialises the inherited attributes (often private ones the subclass cannot set directly); calling it ensures the inherited part of the object is set up correctly.'),
         ('Explain why deep inheritance hierarchies can make programs harder to maintain.', 'Behaviour is spread across many levels, a change in a superclass can unexpectedly affect all descendants (fragile base class), and it becomes hard to understand where a method is defined.')],
    contrast=[('a superclass', 'a subclass', 'A superclass is the general class providing shared members; a subclass inherits them and adds or overrides members to specialise behaviour.'),
              ('inheritance', 'composition', 'Inheritance models an "is-a" relationship where a subclass reuses a superclass\'s members; composition models a "has-a" relationship where an object contains other objects.'),
              ('private members', 'protected members', 'Private members are not directly accessible in subclasses; protected members are accessible in subclasses.')],
    misc=[('A subclass can access all private attributes of its superclass directly.', 'Private members are inherited as part of the object but are not directly accessible; the subclass must use public/protected methods or protected attributes.'),
          ('Inheritance means the subclass gets a copy of the superclass\'s objects.', 'The subclass inherits the definition (attributes and methods); each subclass object has its own values.'),
          ('A class can only be a superclass if it has no methods.', 'Superclasses normally provide methods that subclasses inherit or override.')],
    evaluate=[('Composition should be preferred to inheritance.', ['looser coupling, easier to change at run time', 'avoids fragile base-class problems', 'models "has-a" relationships accurately'], ['inheritance gives natural polymorphism for true "is-a" relationships', 'less delegation code', 'clearer for simple hierarchies'], 'Prefer composition by default, but use inheritance for genuine "is-a" relationships with shared behaviour and stable hierarchies.')],
))
ar('ch10-st1', [
    ('A subclass inherits the public methods of its superclass.', 'Inheritance lets a subclass reuse the superclass\'s behaviour.', 0, 'Both true; R explains A.'),
    ('Java allows a class to extend two superclasses directly.', 'Java supports multiple inheritance of type through interfaces.', 3, 'A is false (single inheritance of classes); R is true.'),
    ('The superclass constructor runs before the rest of the subclass constructor.', 'super(...) must be the first statement in a Java subclass constructor.', 0, 'Both true; R explains A.'),
])


# ---- polymorphism ----
@R.add('ch10-st2', 'C3', (1, 5), 'short')
def poly_trace(rng, slot):
    shapes = [('Rect', rng.randint(2, 9), rng.randint(2, 9)), ('Square', rng.randint(2, 9)), ('Triangle', rng.randint(2, 10) * 2, rng.randint(2, 9))]
    rng.shuffle(shapes)
    objs = ', '.join(f'{s[0]}({", ".join(map(str, s[1:]))})' for s in shapes)
    code = f'''class Shape:
    def area(self):
        return 0

    def label(self):
        return type(self).__name__ + ": " + str(self.area())

class Rect(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

class Square(Rect):
    def __init__(self, s):
        super().__init__(s, s)

class Triangle(Shape):
    def __init__(self, b, h):
        self.b = b
        self.h = h

    def area(self):
        return self.b * self.h // 2

shapes = [{objs}, Shape()]
total = 0
for s in shapes:
    print(s.label())
    total += s.area()
print("Total", total)'''
    out = run_py(code)
    return dict(stem=_code_q(code) + (' Explain how this demonstrates polymorphism.' if slot.d >= 3 else ''),
                answer=out + ('\nThe same call s.area() (and label()) runs a different overridden method depending on the actual object type – dynamic binding.' if slot.d >= 3 else ''),
                markingKey=f'Output:\n{out}\nA1 per two lines; Square inherits Rect.area; Shape returns 0.' + (' R1 run-time polymorphism / overriding.' if slot.d >= 3 else ''), marks=3 if slot.d <= 2 else 4)


@R.add('ch10-st2', 'C3', (2, 5), 'short')
def overload_java(rng, slot):
    has_int = rng.random() < 0.6
    sigs = [('int', '"int "'), ('double', '"double "'), ('String', '"text "'), ('int, int', '"pair "')]
    if not has_int:
        sigs = sigs[1:]
    args = []
    for _ in range(4):
        args.append(rng.choice([str(rng.randint(1, 9)), f'{rng.randint(1, 9)}.5', f'"{rng.choice(["Oslo", "Lima"])}"', f'{rng.randint(1, 9)}, {rng.randint(1, 9)}']))
    meth = []
    for p, tag in sigs:
        if p == 'int, int':
            meth.append(f'    static String show(int a, int b) {{ return {tag} + (a + b); }}')
        else:
            meth.append(f'    static String show({p} x) {{ return {tag} + x; }}')
    calls = '\n'.join(f'        System.out.println(show({a}));' for a in args)
    code = 'public class Demo {\n' + '\n'.join(meth) + f'\n\n    public static void main(String[] args) {{\n{calls}\n    }}\n}}'
    outs = []
    for a in args:
        if ', ' in a:
            x, y = a.split(', ')
            outs.append(f'pair {int(x) + int(y)}')
        elif a.startswith('"'):
            outs.append(f'text {a.strip(chr(34))}')
        elif '.' in a:
            outs.append(f'double {a}')
        else:
            outs.append(f'int {a}' if has_int else f'double {a}.0')
    out = '\n'.join(outs)
    return dict(stem=_code_q(code, 'Java') + ' Explain how Java decides which version of show is called.',
                answer=out + '\nOverloading is resolved at compile time from the number and types of the arguments' + ('' if has_int else '; with no show(int), an int argument is widened to double') + '.',
                markingKey=f'Output:\n{out}\nA1 per two lines; R1 compile-time (static) resolution by parameter list' + ('' if has_int else '; R1 int widened to double (printed with .0)') + '.', marks=4)


R.facts('ch10-st2', F(
    terms=[('polymorphism', 'the ability of objects of different classes to respond to the same method call in their own way'),
           ('method overriding', 'a subclass providing its own implementation of a method with the same name and parameters as one in its superclass'),
           ('method overloading', 'defining several methods with the same name but different parameter lists in the same class'),
           ('dynamic (late) binding', 'deciding at run time which overridden method to execute, based on the actual type of the object'),
           ('static (early) binding', 'deciding at compile time which method to call, as with overloaded methods'),
           ('@Override', 'a Java annotation telling the compiler that a method is intended to override a superclass method, so mistakes in its signature are caught')],
    facts=[('A superclass reference Animal a = new Dog(); then a.speak() runs Dog\'s speak(). This is…', 'run-time polymorphism (overriding)', ['overloading', 'encapsulation', 'composition'], 'The object\'s actual type decides the method.'),
           ('Two methods area(int r) and area(int w, int h) in the same class are an example of…', 'overloading', ['overriding', 'inheritance', 'abstraction'], 'Same name, different parameter lists.'),
           ('Why does Python not support Java-style method overloading?', 'A later definition with the same name replaces the earlier one', ['Python has no methods', 'Python forbids default parameters', 'Python is compiled'], 'Python uses default/variable arguments instead.')],
    why=[('Explain how polymorphism makes it easy to add new types to a program.', 'Code written against the superclass (e.g. looping over Shape objects calling area()) works unchanged with a new subclass that overrides area(), so only the new class needs writing.'),
         ('Explain why the @Override annotation is useful.', 'If the method signature does not actually match a superclass method (e.g. a typo or wrong parameter type), the compiler reports an error instead of silently creating a new overloaded method.'),
         ('Explain why overloading is resolved at compile time but overriding at run time.', 'Overload choice depends only on the declared types of the arguments, known when compiling; overriding depends on the actual class of the object, which may only be known when the program runs.')],
    contrast=[('method overloading', 'method overriding', 'Overloading: same name, different parameters, usually in one class, chosen at compile time; overriding: same name and parameters in a subclass replacing the superclass version, chosen at run time.'),
              ('static binding', 'dynamic binding', 'Static binding fixes the method at compile time (overloads, static methods); dynamic binding chooses at run time from the object\'s actual class (overridden methods).')],
    misc=[('Overloading requires inheritance.', 'Overloaded methods are normally in the same class and need no inheritance; it is overriding that requires a subclass.'),
          ('Changing only the return type of a method is enough to overload it in Java.', 'Overloads must differ in parameter list; methods differing only in return type cause a compile error.'),
          ('If a variable is declared as Animal, a.speak() always runs Animal\'s version.', 'With overriding, the actual object\'s class decides; if a refers to a Dog, Dog.speak() runs.')],
    evaluate=[('Polymorphism is the most important feature of object-oriented programming.', ['enables extensible, loosely coupled code', 'supports design patterns and frameworks'], ['depends on inheritance/interfaces and encapsulation to be useful', 'can make control flow harder to trace', 'encapsulation arguably delivers more everyday benefit'], 'Polymorphism is central to flexible OOP design, but its value relies on the other features; "most important" depends on the problem.')],
))
ar('ch10-st2', [
    ('Overridden methods are selected at run time.', 'The method executed depends on the actual type of the object, not the declared type of the variable.', 0, 'Both true; R explains A.'),
    ('In Java, two methods can be overloaded by changing only their return types.', 'Overloaded methods must have different parameter lists.', 3, 'A is false; R is true and explains why.'),
])


# ---- abstraction ----
@R.add('ch10-st3', 'C3', (2, 5), 'short')
def abstract_trace(rng, slot):
    forget = rng.random() < 0.4
    p1, p2 = rng.randint(2, 9), rng.randint(10, 30)
    code = f'''from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def fee(self):
        pass

    def total(self):
        return self.amount + self.fee()

class Card(Payment):
    def fee(self):
        return self.amount * {p1} // 100

class Mobile(Payment):
    def {"charge" if forget else "fee"}(self):
        return {p2}

for p in [Card({rng.choice([100, 200, 400])}), Mobile({rng.choice([50, 80, 150])})]:
    print(type(p).__name__, p.total())'''
    try:
        out = run_py(code)
        err = None
    except TypeError as e:
        err = str(e)
        out = None
    if err:
        ans = 'Nothing is printed: Mobile does not implement the abstract method fee (it defines charge instead), so Mobile(...) raises TypeError "Can\'t instantiate abstract class Mobile" while the list is being built.'
    else:
        ans = out
    return dict(stem=f'Consider the following Python code.\n{code}\nState the output, or describe the error that occurs and why.',
                answer=ans, markingKey=ans + ' Marks: correct identification of abstract-method rule (R1) and output/error (A2).', marks=3)


_IFACE = [
    ('interface Chargeable { int chargeTime(); }\nclass Phone implements Chargeable { }', 'Phone does not implement chargeTime(); a class implementing an interface must implement all its abstract methods or be declared abstract (compile error).'),
    ('abstract class Sensor { abstract double read(); }\n...\nSensor s = new Sensor();', 'An abstract class cannot be instantiated; create an object of a concrete subclass, e.g. Sensor s = new TempSensor();'),
    ('interface Drawable { void draw(); }\nclass Logo implements Drawable { void draw() { ... } }', 'Interface methods are implicitly public; draw() in Logo has package (default) access, weaker than public, so it does not compile – declare it public void draw().'),
    ('abstract class Animal { abstract void speak() { System.out.println("..."); } }', 'An abstract method cannot have a body; either remove the body (abstract void speak();) or make it a concrete method.'),
    ('class Robot extends Machine, Toy { }', 'Java does not allow a class to extend two classes; make one (or both) an interface: class Robot extends Machine implements Toy.'),
]


@R.add('ch10-st3', 'C2', (2, 4), 'explain')
def iface_err(rng, slot):
    code, fix = rng.choice(_IFACE)
    return dict(stem=rng.choice(['Explain why the following Java code does not compile and how to fix it.\n', 'Identify the error in this Java code.\n']) + code,
                answer=fix, markingKey=f'{fix} 1 mark identification, 1 mark rule/fix.', type='explain', marks=2, gap='G2')


R.facts('ch10-st3', F(
    terms=[('abstraction', 'showing only the essential features of an object or operation and hiding unnecessary detail'),
           ('abstract class', 'a class that cannot be instantiated and may contain abstract methods (without bodies) as well as concrete methods and attributes'),
           ('abstract method', 'a method declared without an implementation that subclasses must override'),
           ('interface', 'a type that specifies a set of method signatures (a contract) that implementing classes must provide; in Java a class can implement many interfaces'),
           ('concrete class', 'a class that implements all of its methods and so can be instantiated')],
    facts=[('Which statement about abstract classes is TRUE?', 'They cannot be instantiated', ['They cannot have constructors', 'They cannot have any concrete methods', 'They must be final'], 'You instantiate concrete subclasses instead.'),
           ('In Java, a class can…', 'extend one class and implement several interfaces', ['extend several classes', 'implement only one interface', 'not use interfaces with inheritance'], 'Single class inheritance, multiple interfaces.'),
           ('Python supports abstract classes through the module…', 'abc (ABC and @abstractmethod)', ['math', 'random', 'interface'], 'abc = abstract base classes.')],
    why=[('Explain why an abstract class Shape with an abstract area() method is useful.', 'It guarantees every concrete shape provides area(), lets code treat all shapes uniformly (polymorphism), shares common code in Shape, and prevents meaningless generic Shape objects being created.'),
         ('Explain why interfaces are used when unrelated classes need a common behaviour.', 'Classes like Phone and ElectricCar are not related by "is-a", but both can implement Chargeable, so code can treat them uniformly without forcing an inheritance hierarchy.'),
         ('Explain how abstraction reduces complexity for programmers using a class.', 'They only need to know what the public methods do (the interface), not how they are implemented, so they can use complex components without understanding their internals.')],
    contrast=[('an abstract class', 'an interface', 'An abstract class can hold attributes, constructors and implemented methods, and a class extends only one; an interface defines a contract of methods (mainly without state) and a class can implement many.'),
              ('an abstract method', 'a concrete method', 'An abstract method has no body and must be overridden in a subclass; a concrete method has an implementation.'),
              ('abstraction', 'encapsulation', 'Abstraction decides which essential features to expose; encapsulation protects the data and implementation behind that interface.')],
    misc=[('An abstract class cannot have a constructor.', 'It can have constructors, which subclasses call with super(...) to initialise inherited attributes; it just cannot be instantiated directly.'),
          ('All methods in an abstract class must be abstract.', 'An abstract class can mix abstract and fully implemented methods.'),
          ('Implementing an interface gives a class inherited attributes.', 'An interface provides method signatures (and constants/default methods), not instance attributes.')],
    evaluate=[('Programmers should always design to interfaces rather than concrete classes.', ['loose coupling – implementations can be swapped (e.g. for testing)', 'supports polymorphism and multiple types'], ['extra layers add complexity to small programs', 'premature abstraction can make code harder to follow'], 'Programming to interfaces is valuable at module boundaries and where variation is expected; it should not be applied mechanically everywhere.')],
))
ar('ch10-st3', [
    ('An abstract class cannot be instantiated.', 'It may contain methods without implementations.', 0, 'Both true; R explains A (an object would have unimplemented methods).'),
    ('A Java class can implement more than one interface.', 'Interfaces define contracts rather than state, avoiding the problems of multiple inheritance.', 0, 'Both true; R explains why Java allows it.'),
])


# ---- composition / aggregation ----
@R.add('ch10-st4', 'C3', (1, 5), 'short')
def compose_trace(rng, slot):
    kind = rng.choice(['car', 'library'])
    if kind == 'car':
        code = f'''class Engine:
    def __init__(self, power):
        self.power = power
        self.running = False

    def start(self):
        self.running = True
        return "Engine " + str(self.power) + "kW on"

class Car:
    def __init__(self, model, power):
        self.model = model
        self.engine = Engine(power)

    def drive(self, km):
        if not self.engine.running:
            print(self.engine.start())
        return self.model + " drove " + str(km) + " km"

c = Car("{rng.choice(['Zoe', 'Leaf', 'Kona'])}", {rng.choice([50, 80, 110])})
print(c.drive({rng.randint(5, 30)}))
print(c.drive({rng.randint(31, 90)}))
print(c.engine.running)'''
    else:
        titles = rng.sample(['Things Fall Apart', 'Siddhartha', 'Kafka on the Shore', 'Ficciones', 'Sophie\'s World', 'The Alchemist'], 4)
        code = f'''class Book:
    def __init__(self, title):
        self.title = title

class Shelf:
    def __init__(self, label):
        self.label = label
        self.books = []

    def add(self, book):
        self.books.append(book)

b = [Book(t) for t in {titles}]
s1 = Shelf("A")
s2 = Shelf("B")
for i, book in enumerate(b):
    if i % 2 == 0:
        s1.add(book)
    else:
        s2.add(book)
s2.add(b[0])
del s1
print(len(s2.books), s2.books[-1].title)
print([x.title for x in s2.books[:2]])'''
    out = run_py(code)
    ex = ' Identify whether the relationship between the two classes is composition or aggregation, and justify.' if slot.d >= 3 else ''
    why = ('Composition: the Car creates and owns its Engine; the Engine does not exist independently of the Car.' if kind == 'car' else
           'Aggregation: Books are created independently and can belong to several shelves; deleting a Shelf does not destroy its Books.')
    return dict(stem=_code_q(code) + ex, answer=out + (f'\n{why}' if ex else ''),
                markingKey=f'Output:\n{out}\nA1 per line.' + (f' R1 {why}' if ex else ''), marks=3 if slot.d <= 2 else 4)


_MULT = [
    ('a Team has 11 to 25 Players and each Player belongs to exactly one Team', 'Team 1 ◇—— 11..25 Player (aggregation; hollow diamond at the Team end, 1 at Team, 11..25 at Player)'),
    ('a House is made of 1 or more Rooms that cannot exist without it', 'House 1 ◆—— 1..* Room (composition; filled diamond at House)'),
    ('a Course has 0 or more Students and a Student takes 1 to 6 Courses', 'Student —— Course as a plain association (many-to-many): 1..6 written at the Course end and 0..* at the Student end'),
    ('an Order contains 1 or more OrderLines that are deleted with the Order', 'Order 1 ◆—— 1..* OrderLine (composition)'),
    ('a Car has exactly 4 Wheels, which can be moved to another car', 'Car 0..1 ◇—— 4 Wheel (aggregation; wheel can exist without the car)'),
]


@R.add('ch10-st4', 'C3', (2, 4), 'short')
def multiplicity(rng, slot):
    k = 1 if slot.d <= 2 else 2
    its = rng.sample(_MULT, k)
    stem = 'Describe how each relationship would be drawn on a UML class diagram, including the type of association and the multiplicities.\n' + '\n'.join(f'{i + 1}. {d}' for i, (d, _) in enumerate(its))
    ans = ' '.join(f'{i + 1}. {a}' for i, (_, a) in enumerate(its))
    return dict(stem=stem, answer=ans, markingKey=ans + ' Per relationship: correct line/diamond type (1), correct multiplicities at both ends (1).', marks=2 * k)


R.facts('ch10-st4', F(
    terms=[('association', 'a general relationship between two classes in which objects of one class use or are linked to objects of the other'),
           ('aggregation', 'a "has-a" relationship in which the part can exist independently of the whole (shown with a hollow diamond)'),
           ('composition', 'a strong "has-a" relationship in which the part is owned by and cannot exist without the whole (shown with a filled diamond)'),
           ('multiplicity', 'the number of objects that can take part in a relationship, written on UML diagrams as 1, 0..1, *, 1..* or a range'),
           ('dependency', 'a weak relationship where one class temporarily uses another, e.g. as a method parameter (dashed arrow in UML)'),
           ('generalisation (UML)', 'the UML name for inheritance, drawn as a line with a hollow triangle pointing to the superclass')],
    facts=[('In UML, a filled (black) diamond represents…', 'composition', ['aggregation', 'inheritance', 'an interface'], 'Filled = composition; hollow = aggregation.'),
           ('Which is the best example of composition?', 'A Building and its Floors', ['A Teacher and her Students', 'A Playlist and its Songs', 'A Team and its Players'], 'Floors cannot exist without the building.'),
           ('A multiplicity of 0..* means…', 'zero or more', ['exactly one', 'one or more', 'at most one'], '* means many.')],
    why=[('Explain why a playlist and its songs is modelled as aggregation rather than composition.', 'Songs exist independently of any playlist and can appear on several playlists; deleting a playlist must not delete the songs.'),
         ('Explain why composition can be safer than inheritance for reusing behaviour.', 'The containing class uses only the part\'s public interface (loose coupling), parts can be replaced at run time, and changes to the part\'s internals do not ripple through a hierarchy.'),
         ('Explain why multiplicities are shown on UML association lines.', 'They express business rules (e.g. each order has at least one line) that must be enforced in code and help programmers choose data structures (single reference vs list).')],
    contrast=[('aggregation', 'composition', 'In aggregation the part can exist independently and may be shared (hollow diamond); in composition the part is owned exclusively and destroyed with the whole (filled diamond).'),
              ('association', 'dependency', 'An association is a lasting structural link (an attribute referencing another object); a dependency is temporary use, such as a parameter or local variable.'),
              ('"has-a"', '"is-a"', '"Has-a" relationships (association/aggregation/composition) mean an object contains or uses another; "is-a" (inheritance) means a subclass is a kind of superclass.')],
    misc=[('Aggregation and inheritance are the same thing.', 'Aggregation is a "has-a" relationship between separate objects; inheritance is an "is-a" relationship between classes.'),
          ('In composition the part can be shared between several wholes.', 'In composition the part belongs to exactly one whole; sharing indicates aggregation.'),
          ('A multiplicity of 1..* allows zero objects.', '1..* means at least one; 0..* allows zero.')],
    evaluate=[('Composition should replace inheritance in most object-oriented designs.', ['flexible: behaviour can be changed at run time', 'reduces coupling and fragile hierarchies', 'supports many design patterns (strategy, decorator)'], ['inheritance is natural for true "is-a" relationships', 'composition needs extra delegation methods', 'polymorphism via inheritance is simple'], 'Favour composition for reuse and flexibility, reserving inheritance for genuine, stable "is-a" hierarchies.')],
))
ar('ch10-st4', [
    ('Deleting a House object should delete its Room objects.', 'House and Room are related by composition.', 0, 'Both true; R explains A.'),
    ('A filled diamond in UML shows aggregation.', 'Aggregation parts can exist independently of the whole.', 3, 'A is false (filled = composition); R is true.'),
])


# ---- design patterns ----
@R.add('ch10-st5', 'C3', (1, 5), 'short')
def pattern_trace(rng, slot):
    kind = rng.choice(['singleton', 'factory', 'observer'])
    if kind == 'singleton':
        n = rng.randint(2, 4)
        code = f'''class Config:
    _instance = None
    created = 0

    def __init__(self):
        Config.created += 1
        self.theme = "light"

    @staticmethod
    def get():
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance

a = Config.get()
for i in range({n}):
    b = Config.get()
b.theme = "dark"
print(a.theme, a is b, Config.created)'''
    elif kind == 'factory':
        orders = [rng.choice(['bike', 'scooter', 'car', 'boat']) for _ in range(4)]
        code = f'''class Bike:
    def cost(self, km):
        return km * 1

class Scooter:
    def cost(self, km):
        return 2 + km * 2

class Car:
    def cost(self, km):
        return 5 + km * 3

def make(kind):
    if kind == "bike":
        return Bike()
    if kind == "scooter":
        return Scooter()
    if kind == "car":
        return Car()
    return None

for k in {orders}:
    v = make(k)
    if v is None:
        print(k, "unavailable")
    else:
        print(k, v.cost({rng.randint(2, 9)}))'''
    else:
        code = f'''class Station:
    def __init__(self):
        self.observers = []

    def subscribe(self, fn):
        self.observers.append(fn)

    def unsubscribe(self, fn):
        self.observers.remove(fn)

    def publish(self, temp):
        for fn in self.observers:
            fn(temp)

def phone(t):
    print("Phone:", t)

def sign(t):
    if t > {rng.choice([25, 28, 30])}:
        print("Sign: HEAT WARNING", t)

s = Station()
s.subscribe(phone)
s.subscribe(sign)
s.publish({rng.randint(20, 35)})
s.unsubscribe(phone)
s.publish({rng.randint(20, 35)})
s.subscribe(phone)
s.publish({rng.randint(20, 35)})'''
    out = run_py(code)
    names = {'singleton': 'singleton', 'factory': 'factory', 'observer': 'observer'}
    ex = ' Name the design pattern used and state one advantage of it.' if slot.d >= 3 else ''
    adv = {'singleton': 'guarantees a single shared instance (e.g. configuration) with a global access point',
           'factory': 'client code creates objects without knowing their concrete classes, so new types can be added in one place',
           'observer': 'the subject is loosely coupled to any number of observers that are notified automatically of changes'}[kind]
    return dict(stem=_code_q(code) + ex, answer=out + (f'\nPattern: {names[kind]} – {adv}.' if ex else ''),
                markingKey=f'Output:\n{out}\nA1 per line (max 3).' + (f' Pattern {names[kind]} (1); advantage: {adv} (1).' if ex else ''), marks=3 if slot.d <= 2 else 5)


R.facts('ch10-st5', F(
    terms=[('design pattern', 'a general, reusable solution to a commonly occurring problem in software design'),
           ('singleton pattern', 'a creational pattern that ensures a class has only one instance and provides a global point of access to it'),
           ('factory pattern', 'a creational pattern in which a method or class creates objects without the client specifying their exact concrete class'),
           ('observer pattern', 'a behavioural pattern in which a subject keeps a list of observers and notifies them automatically when its state changes'),
           ('creational pattern', 'a design pattern concerned with how objects are created'),
           ('behavioural pattern', 'a design pattern concerned with communication and responsibilities between objects')],
    facts=[('A weather app updates every open screen when new data arrives. Which pattern fits?', 'Observer', ['Singleton', 'Factory', 'Composition'], 'Subscribers are notified of changes.'),
           ('An application must have exactly one database-connection manager. Which pattern fits?', 'Singleton', ['Observer', 'Factory', 'Decorator'], 'Only one instance is allowed.'),
           ('A game creates Enemy objects of different types from a level file containing names such as "orc" and "troll". Which pattern fits?', 'Factory', ['Singleton', 'Observer', 'Iterator'], 'Object creation is delegated by type name.')],
    why=[('Explain why the singleton\'s constructor is usually made private.', 'So no other code can call new and create a second instance; the only way to get the object is through the static getInstance() method.'),
         ('Explain why the observer pattern reduces coupling.', 'The subject only knows that observers implement an update method; it does not depend on their concrete classes, so observers can be added or removed without changing the subject.'),
         ('Explain why singletons are sometimes considered an anti-pattern.', 'They introduce global shared state, hide dependencies, make unit testing hard (cannot easily substitute a fake) and can cause problems with concurrency.')],
    contrast=[('the singleton pattern', 'the factory pattern', 'Singleton restricts a class to one instance; factory centralises the creation of many objects of varying concrete types.'),
              ('a creational pattern', 'a behavioural pattern', 'Creational patterns deal with how objects are created (singleton, factory); behavioural patterns deal with how objects interact and communicate (observer).')],
    misc=[('A design pattern is a piece of library code that can be copied into a program.', 'A pattern is a reusable design idea/template; it must be implemented to fit each program.'),
          ('In the observer pattern, observers repeatedly ask the subject whether anything has changed.', 'That is polling; in the observer pattern the subject pushes notifications to registered observers when a change occurs.')],
    evaluate=[('Using design patterns always improves software quality.', ['proven solutions and shared vocabulary for teams', 'promote loose coupling and reuse'], ['over-engineering simple problems', 'misapplied patterns (e.g. singletons) add hidden dependencies', 'extra classes and indirection'], 'Patterns improve quality when they match a real recurring problem; applying them by default adds unnecessary complexity.')],
))
ar('ch10-st5', [
    ('The singleton pattern restricts a class to one instance.', 'Its constructor is private and access is through a static method.', 0, 'Both true; R explains how A is achieved.'),
    ('The observer pattern requires the subject to know the concrete class of each observer.', 'Observers register with the subject.', 3, 'A is false – the subject only relies on a common update interface; R is true.'),
])


# =============================================================================================
# ch11 B4.1 Fundamentals of abstract data types (HL)
# =============================================================================================
@R.add('ch11-st1', 'C3', (1, 5), 'short')
def stack_queue(rng, slot):
    kind = rng.choice(['stack', 'queue'])
    n = 6 if slot.d <= 2 else 9 if slot.d <= 3 else 12
    s = deque()
    ops, outs = [], []
    vals = iter(rng.sample(range(1, 60), n))
    for _ in range(n):
        if len(s) == 0 or rng.random() < 0.55:
            v = next(vals)
            s.append(v)
            ops.append(f'push({v})' if kind == 'stack' else f'enqueue({v})')
        else:
            r_ = rng.random()
            if r_ < 0.7:
                v = s.pop() if kind == 'stack' else s.popleft()
                ops.append('pop()' if kind == 'stack' else 'dequeue()')
                outs.append(str(v))
            else:
                ops.append('peek()' if kind == 'stack' else 'front()')
                outs.append(str(s[-1] if kind == 'stack' else s[0]))
    ops.append('size()')
    outs.append(str(len(s)))
    if not outs:
        return None
    final = (' (top on the right)' if kind == 'stack' else ' (front on the left)')
    ctx = rng.choice({'stack': ['the undo history of a text editor', 'a browser\'s back button', 'checking brackets in a compiler'],
                      'queue': ['print jobs in a school library', 'customers waiting for a ride-share driver', 'packets in a router buffer']}[kind])
    ans = f'Returned values: {", ".join(outs)}. Final {kind}: [{", ".join(map(str, s))}]{final}.'
    return dict(stem=f'A {kind} is used for {ctx}. Starting empty, the operations below are performed in order. State the value returned by each pop/dequeue/peek/front/size operation and the final contents of the {kind}.\n' + ', '.join(ops),
                answer=ans, markingKey=ans + f' {"LIFO" if kind == "stack" else "FIFO"} order (M1); A1 per two correct returned values; A1 final contents.', marks=3 if slot.d <= 2 else 4)


@R.add('ch11-st1', 'C3', (2, 5), 'short')
def bracket_check(rng, slot):
    pairs = {')': '(', ']': '[', '}': '{'}
    exprs = ['(a[1] + {b * 2})', '{[x + (y - 1)]}', '(a + b]', '[(x + y) * {z}', 'f(g[h(1)])', '{a + (b * [c - d)]}', '((x))[y]{z}', '(]', 'max(a[i], b[j]))']
    e = rng.choice(exprs)
    st = []
    result = None
    trace = []
    for i, ch in enumerate(e):
        if ch in '([{':
            st.append(ch)
            trace.append(f'push {ch}')
        elif ch in ')]}':
            if not st or st[-1] != pairs[ch]:
                result = f'unbalanced: "{ch}" at position {i} does not match ' + (f'"{st[-1]}"' if st else 'anything (stack empty)')
                break
            st.pop()
            trace.append(f'pop for {ch}')
    if result is None:
        result = 'balanced' if not st else f'unbalanced: {len(st)} unclosed bracket(s) left on the stack ({"".join(st)})'
    return dict(stem=f'A compiler uses a stack to check brackets: push every opening bracket; on a closing bracket, pop and check it matches; at the end the stack must be empty. Trace the algorithm on the expression {e} and state the result.',
                answer=result, markingKey=f'Trace: {"; ".join(trace)}. Result: {result}. M1 correct pushes/pops; A1 result with reason.', marks=3)


R.facts('ch11-st1', F(
    terms=[('abstract data type (ADT)', 'a data type defined by its values and the operations that can be performed on it, independently of how it is implemented'),
           ('stack', 'a last-in, first-out (LIFO) ADT with operations push, pop, peek and isEmpty'),
           ('queue', 'a first-in, first-out (FIFO) ADT with operations enqueue, dequeue, front and isEmpty'),
           ('priority queue', 'a queue in which each element has a priority and the element with the highest priority is removed first'),
           ('static data structure', 'a structure whose size is fixed when it is created, such as an array'),
           ('dynamic data structure', 'a structure that can grow and shrink at run time, such as a linked list'),
           ('circular queue', 'a queue implemented in a fixed-size array whose front and rear pointers wrap around to reuse freed space')],
    facts=[('Which ADT is used to implement the "undo" function in a word processor?', 'Stack', ['Queue', 'Set', 'Hash table'], 'The most recent action is undone first (LIFO).'),
           ('Which ADT is most suitable for jobs waiting for a single printer?', 'Queue', ['Stack', 'Binary search tree', 'Set'], 'First come, first served (FIFO).'),
           ('Method calls and their local variables are stored at run time on…', 'the call stack', ['a queue', 'a hash table', 'a set'], 'Each call is pushed and popped on return (LIFO).'),
           ('Which operation of a stack returns the top item without removing it?', 'peek', ['pop', 'push', 'dequeue'], 'peek (top) only reads.')],
    why=[('Explain why an ADT separates the interface from the implementation.', 'Users rely only on the defined operations and their behaviour, so the implementation (array, linked list) can be changed for efficiency without changing the code that uses the ADT.'),
         ('Explain why a circular queue is more efficient than a simple linear array queue.', 'In a linear array queue, dequeued slots at the front are wasted (or items must be shifted, O(n)); a circular queue wraps the pointers so freed slots are reused and enqueue/dequeue stay O(1).'),
         ('Explain why recursion relies on a stack.', 'Each recursive call\'s parameters, local variables and return address are pushed onto the call stack and popped when it returns, so calls finish in reverse order (LIFO).')],
    contrast=[('a stack', 'a queue', 'A stack is LIFO – items are added and removed at the same end (top); a queue is FIFO – items are added at the rear and removed from the front.'),
              ('a static data structure', 'a dynamic data structure', 'A static structure has a fixed size set at creation (fast indexed access, may waste or run out of space); a dynamic structure grows and shrinks as needed using extra memory for pointers.'),
              ('an ADT', 'a data structure', 'An ADT is a logical description of data and operations; a data structure is a concrete implementation of it in memory (e.g. a stack implemented with an array).')],
    misc=[('A queue removes the most recently added item first.', 'That is a stack (LIFO); a queue removes the oldest item first (FIFO).'),
          ('Popping from an empty stack returns 0.', 'It is an error (stack underflow); isEmpty() should be checked first or an exception handled.'),
          ('An ADT specifies exactly how the data must be stored in memory.', 'An ADT specifies operations and behaviour only; storage is left to the implementation.')],
    evaluate=[('Arrays are always a better way to implement a stack than a linked list.', ['contiguous memory, cache-friendly and fast', 'no pointer overhead'], ['fixed size can overflow or waste space', 'resizing is costly', 'linked list grows freely, O(1) push/pop with no capacity limit'], 'Arrays are better when the maximum size is known; linked lists suit unpredictable sizes. Dynamic arrays offer a common compromise.')],
))
ar('ch11-st1', [
    ('A stack is suitable for reversing a sequence of items.', 'The last item pushed is the first item popped.', 0, 'Both true; LIFO explains reversal.'),
    ('A queue is a LIFO data structure.', 'Items are removed from a queue in the order they arrived.', 3, 'A is false (FIFO); R is true.'),
    ('A stack can be implemented with either an array or a linked list.', 'An ADT defines operations independently of implementation.', 0, 'Both true; R explains A.'),
])


# ---- linked lists ----
@R.add('ch11-st2', 'C3', (1, 5), 'short')
def ll_ops(rng, slot):
    lst = rng.sample(range(10, 99), rng.randint(3, 5))
    start = list(lst)
    n = 2 if slot.d <= 2 else 3 if slot.d <= 3 else 5
    ops = []
    for _ in range(n):
        k = rng.choice(['head', 'tail', 'delete', 'after', 'deletehead'])
        if k == 'head':
            v = rng.randint(1, 9)
            lst.insert(0, v)
            ops.append(f'insertAtHead({v})')
        elif k == 'tail':
            v = rng.randint(100, 120)
            lst.append(v)
            ops.append(f'insertAtTail({v})')
        elif k == 'delete' and lst:
            v = rng.choice(lst + [0])
            if v in lst:
                lst.remove(v)
            ops.append(f'delete({v})' + ('' if v else '  # value not present'))
        elif k == 'after' and lst:
            a = rng.choice(lst)
            v = rng.randint(200, 220)
            lst.insert(lst.index(a) + 1, v)
            ops.append(f'insertAfter({a}, {v})')
        elif lst:
            lst.pop(0)
            ops.append('deleteHead()')
    chain = ' → '.join(map(str, lst)) + ' → null'
    ans = f'{chain}; head = {lst[0] if lst else "null"}, length {len(lst)}'
    return dict(stem=f'A singly linked list contains {" → ".join(map(str, start))} → null (head on the left). The following operations are performed in order: {", ".join(ops)}. (delete removes the first node holding that value.) Draw the final list and state the value at the head.',
                answer=ans, markingKey=ans + '. A1 per operation correctly applied; pointers updated so no node is lost.', marks=n + 1)


@R.add('ch11-st2', 'C3', (2, 5), 'short')
def ll_code(rng, slot):
    vals = rng.sample(range(1, 30), rng.randint(4, 6))
    t = rng.choice(['sum_even', 'count_gt', 'reverse', 'circular'])
    k = rng.randint(5, 20)
    if t == 'circular':
        steps = rng.randint(5, 12)
        code = f'''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

nodes = [Node(v) for v in {vals}]
for i in range(len(nodes)):
    nodes[i].next = nodes[(i + 1) % len(nodes)]   # circular
cur = nodes[{rng.randint(0, len(vals) - 1)}]
out = []
for i in range({steps}):
    out.append(cur.data)
    cur = cur.next
print(out[-3:], cur.data)'''
    else:
        body = {'sum_even': '''total = 0
cur = head
while cur is not None:
    if cur.data % 2 == 0:
        total += cur.data
    cur = cur.next
print(total)''',
                'count_gt': f'''count = 0
cur = head
while cur is not None:
    if cur.data > {k}:
        count += 1
    cur = cur.next
print(count, head.data)''',
                'reverse': '''prev = None
cur = head
while cur is not None:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
head = prev
cur = head
while cur is not None:
    print(cur.data, end=" ")
    cur = cur.next
print()'''}[t]
        code = f'''class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

head = None
for v in {vals}:
    head = Node(v, head)      # insert at head
{body}'''
    out = run_py(code).rstrip()
    return dict(stem=_code_q(code), answer=out, markingKey=f'Output: {out}. M1 list order after insertions/links; M1 traversal logic; A1 output.', marks=3)


R.facts('ch11-st2', F(
    terms=[('linked list', 'a dynamic linear data structure made of nodes, each holding data and a pointer (reference) to the next node'),
           ('node', 'an element of a linked structure containing data and one or more pointers to other nodes'),
           ('head pointer', 'the reference to the first node of a linked list; null when the list is empty'),
           ('null pointer', 'a pointer that refers to no node, used to mark the end of a singly linked list'),
           ('doubly linked list', 'a linked list in which each node has pointers to both the next and the previous node'),
           ('circular linked list', 'a linked list in which the last node points back to the first node instead of to null')],
    facts=[('What is the time complexity of accessing the k-th element of a singly linked list?', 'O(k) – it must be reached by following pointers from the head', ['O(1)', 'O(log k)', 'O(k²)'], 'No random access; traverse from the head.'),
           ('Which advantage does a doubly linked list have over a singly linked list?', 'It can be traversed backwards and a node can be deleted given only a reference to it', ['It uses less memory', 'It allows O(1) access by index', 'It never needs a head pointer'], 'Each node knows its predecessor.'),
           ('Inserting a new node at the head of a linked list takes…', 'O(1) time', ['O(n) time', 'O(log n) time', 'O(n²) time'], 'Only two pointer assignments are needed.')],
    why=[('Explain why inserting into the middle of a linked list can be faster than inserting into the middle of an array.', 'Once the position is found, a linked list only changes two pointers (O(1)), while an array must shift every later element along by one (O(n)).'),
         ('Explain why binary search is not efficient on a linked list.', 'Binary search needs O(1) access to the middle element; in a linked list reaching the middle requires traversing about n/2 nodes, so the advantage is lost.'),
         ('Explain why the order of pointer updates matters when inserting a node after node A.', 'The new node\'s next must be set to A.next before A.next is changed to the new node; otherwise the reference to the rest of the list is lost.'),
         ('Explain why a circular linked list is suitable for round-robin scheduling.', 'After the last process the pointer naturally returns to the first, so the scheduler can cycle through processes indefinitely without special end-of-list handling.')],
    contrast=[('a linked list', 'an array', 'An array stores elements contiguously with O(1) indexed access but fixed size and costly insertion; a linked list stores nodes anywhere linked by pointers, grows dynamically and inserts in O(1) at a known position but has O(n) access.'),
              ('a singly linked list', 'a doubly linked list', 'A singly linked list has one pointer per node (forward only); a doubly linked list has next and previous pointers, allowing traversal both ways at the cost of extra memory.'),
              ('a circular linked list', 'a linear linked list', 'In a circular list the last node points back to the first; in a linear list the last node points to null.')],
    misc=[('Deleting a node from a linked list requires shifting all the following nodes.', 'Only the previous node\'s pointer is changed to skip the deleted node; nothing is shifted.'),
          ('A linked list uses less memory than an array holding the same data.', 'Each node also stores at least one pointer, so a linked list usually uses more memory per element.'),
          ('In a circular linked list traversal ends when a null pointer is reached.', 'There is no null; traversal stops when it returns to the starting node.')],
    evaluate=[('Linked lists are obsolete because modern languages provide dynamic arrays.', ['dynamic arrays give O(1) indexed access and good cache performance', 'amortised O(1) append'], ['linked lists give O(1) insertion/deletion at known positions', 'basis of stacks, queues, hash-table chaining, adjacency lists', 'no costly resize copies'], 'Dynamic arrays are usually preferred for general lists, but linked structures remain essential where frequent insertions/deletions or linked ADTs are needed.')],
))
ar('ch11-st2', [
    ('A linked list can grow while the program is running.', 'Nodes are allocated individually and linked by pointers.', 0, 'Both true; R explains A.'),
    ('A doubly linked list can be traversed backwards from the tail.', 'Each node stores a pointer to its previous node as well as its next node.', 0, 'Both true; the previous pointers explain A.'),
    ('Accessing the last node of a singly linked list with only a head pointer takes O(1) time.', 'Each node stores a pointer to the next node.', 3, 'A is false (O(n) traversal unless a tail pointer is kept); R is true.'),
])


# ---- binary search trees ----
class _BST:
    def __init__(self):
        self.root = None

    def insert(self, v):
        if self.root is None:
            self.root = [v, None, None]
            return
        n = self.root
        while True:
            i = 1 if v < n[0] else 2
            if n[i] is None:
                n[i] = [v, None, None]
                return
            n = n[i]

    def order(self, kind):
        out = []
        def go(n):
            if n is None:
                return
            if kind == 'pre':
                out.append(n[0])
            go(n[1])
            if kind == 'in':
                out.append(n[0])
            go(n[2])
            if kind == 'post':
                out.append(n[0])
        go(self.root)
        return out

    def height(self, n='root'):
        n = self.root if n == 'root' else n
        if n is None:
            return -1
        return 1 + max(self.height(n[1]), self.height(n[2]))

    def path(self, v):
        n, p = self.root, []
        while n is not None:
            p.append(n[0])
            if v == n[0]:
                return p, True
            n = n[1] if v < n[0] else n[2]
        return p, False

    def delete(self, v):
        def rec(n, v):
            if n is None:
                return None
            if v < n[0]:
                n[1] = rec(n[1], v)
            elif v > n[0]:
                n[2] = rec(n[2], v)
            else:
                if n[1] is None:
                    return n[2]
                if n[2] is None:
                    return n[1]
                s = n[2]
                while s[1] is not None:
                    s = s[1]
                n[0] = s[0]
                n[2] = rec(n[2], s[0])
            return n
        self.root = rec(self.root, v)

    def leaves(self):
        out = []
        def go(n):
            if n is None:
                return
            if n[1] is None and n[2] is None:
                out.append(n[0])
            go(n[1])
            go(n[2])
        go(self.root)
        return out


@R.add('ch11-st3', 'C3', (1, 5), 'short')
def bst_trav(rng, slot):
    n = 6 if slot.d <= 2 else 8 if slot.d <= 3 else 10
    vals = rng.sample(range(10, 99), n)
    t = _BST()
    for v in vals:
        t.insert(v)
    kinds = rng.sample(['pre', 'in', 'post'], 1 if slot.d <= 2 else 2 if slot.d <= 3 else 3)
    nm = {'pre': 'pre-order', 'in': 'in-order', 'post': 'post-order'}
    ans = '; '.join(f'{nm[k]}: {", ".join(map(str, t.order(k)))}' for k in kinds) + f'; height {t.height()} (edges on the longest root-to-leaf path)'
    ctx = rng.choice(['product IDs in a warehouse system', 'student ID numbers', 'flight numbers in a booking system', 'sensor IDs'])
    return dict(stem=f'The following {ctx} are inserted, in this order, into an empty binary search tree: {", ".join(map(str, vals))}. Give the {" and ".join(nm[k] for k in kinds)} traversal(s) and state the height of the tree.',
                answer=ans, markingKey=ans + '. M1 correct tree built (smaller left, larger right); A1 per traversal; A1 height.', marks=len(kinds) + 2)


@R.add('ch11-st3', 'C3', (2, 5), 'short')
def bst_delete(rng, slot):
    vals = rng.sample(range(10, 99), 9)
    t = _BST()
    for v in vals:
        t.insert(v)
    # choose a node with two children if possible
    def nodes(n, acc):
        if n:
            acc.append(n)
            nodes(n[1], acc)
            nodes(n[2], acc)
        return acc
    ns = nodes(t.root, [])
    two = [x[0] for x in ns if x[1] and x[2]]
    leaf = [x[0] for x in ns if not x[1] and not x[2]]
    target = rng.choice(two) if two and slot.d >= 3 else rng.choice(leaf)
    case = 'two children: replaced by its in-order successor (smallest value in the right subtree)' if target in two else 'a leaf: simply removed'
    t.delete(target)
    ans = f'{target} has {case}. In-order after deletion: {", ".join(map(str, t.order("in")))}; pre-order: {", ".join(map(str, t.order("pre")))}'
    return dict(stem=f'A binary search tree is built by inserting {", ".join(map(str, vals))} in that order. The value {target} is then deleted using the in-order successor method. Describe how the deletion is performed and give the pre-order traversal of the resulting tree.',
                answer=ans, markingKey=ans + '. M1 identify case; M1 correct replacement; A1 pre-order traversal.', marks=4)


@R.add('ch11-st3', 'C3', (1, 4), 'short')
def bst_search(rng, slot):
    vals = rng.sample(range(1, 99), 8 if slot.d <= 2 else 11)
    t = _BST()
    for v in vals:
        t.insert(v)
    q = rng.choice(vals + [rng.randint(1, 99)])
    p, found = t.path(q)
    ans = f'Visits {", ".join(map(str, p))} – {len(p)} comparison(s); {"found" if found else "not found"}.'
    extra = f' Compare this with the worst case for a sorted linked list of the same {len(vals)} values.' if slot.d >= 3 else ''
    return dict(stem=f'Values are inserted into an empty BST in the order {", ".join(map(str, vals))}. List the nodes visited when searching for {q}, and state the number of comparisons.{extra}',
                answer=ans + (f' A sorted linked list could need up to {len(vals)} comparisons; a balanced BST needs about log₂ n.' if extra else ''),
                markingKey=ans + ' A1 path; A1 count.' + (' R1 comparison.' if extra else ''), marks=2 if slot.d <= 2 else 3)


R.facts('ch11-st3', F(
    terms=[('binary tree', 'a hierarchical data structure in which each node has at most two children, called left and right'),
           ('binary search tree (BST)', 'a binary tree in which every value in a node\'s left subtree is smaller than the node and every value in its right subtree is larger'),
           ('root', 'the top node of a tree, which has no parent'),
           ('leaf node', 'a node with no children'),
           ('in-order traversal', 'visiting the left subtree, then the node, then the right subtree; on a BST this gives the values in ascending order'),
           ('pre-order traversal', 'visiting the node, then its left subtree, then its right subtree; useful for copying a tree'),
           ('post-order traversal', 'visiting the left subtree, then the right subtree, then the node; useful for deleting a tree'),
           ('height of a tree', 'the number of edges on the longest path from the root to a leaf'),
           ('balanced tree', 'a tree whose left and right subtrees differ in height by at most a small amount at every node, giving O(log n) operations')],
    facts=[('Which traversal of a BST outputs its values in ascending order?', 'In-order', ['Pre-order', 'Post-order', 'Breadth-first'], 'Left, node, right.'),
           ('Inserting 10, 20, 30, 40, 50 in that order into an empty BST produces…', 'a tree that is effectively a linked list (height 4)', ['a perfectly balanced tree', 'a tree of height 1', 'an error'], 'Sorted input creates a degenerate tree.'),
           ('The average time to search a balanced BST of n nodes is…', 'O(log n)', ['O(1)', 'O(n)', 'O(n log n)'], 'Each comparison halves the remaining tree.')],
    why=[('Explain why inserting data in sorted order into a BST is a problem.', 'Each new value is larger than all previous ones, so it always goes right; the tree degenerates into a linked list of height n − 1 and search becomes O(n) instead of O(log n).'),
         ('Explain why the in-order successor is used when deleting a node with two children.', 'The successor (smallest value in the right subtree) is larger than everything on the left and smaller than everything else on the right, so it can replace the deleted value while keeping the BST property; it has at most one child, so it is easy to remove.'),
         ('Explain why searching a balanced BST is faster than searching an unsorted array.', 'Each comparison discards one subtree, about half the remaining nodes, giving O(log n) comparisons, while an unsorted array needs a linear O(n) search.')],
    contrast=[('a binary tree', 'a binary search tree', 'A binary tree only limits each node to two children; a BST also orders values so left < node < right, enabling efficient search.'),
              ('pre-order traversal', 'post-order traversal', 'Pre-order visits a node before its subtrees (used to copy/serialise a tree); post-order visits it after both subtrees (used to delete or evaluate expression trees).'),
              ('a balanced BST', 'a degenerate BST', 'A balanced BST has height about log₂ n and O(log n) operations; a degenerate BST has height n − 1, behaving like a linked list with O(n) operations.')],
    misc=[('The root of a BST is always the median value.', 'The root is the first value inserted; it is only the median if data happened to be inserted that way or the tree is rebalanced.'),
          ('A BST always gives O(log n) search time.', 'Only if it is balanced; a degenerate BST gives O(n).'),
          ('Deleting a node with two children means deleting its whole subtree.', 'Only the value is removed: it is replaced by its in-order successor (or predecessor) and the rest of the subtree stays.')],
    evaluate=[('A binary search tree is a better choice than a hash table for storing a dictionary of words.', ['in-order traversal lists words alphabetically', 'supports range queries and nearest matches (autocomplete)', 'guaranteed O(log n) if balanced'], ['hash table gives O(1) average look-up', 'unbalanced BSTs degrade to O(n)', 'BST needs balancing algorithms'], 'For pure look-up a hash table is faster; for ordered output, prefix/range searches a balanced BST is better.')],
))
ar('ch11-st3', [
    ('An in-order traversal of a BST gives values in ascending order.', 'In a BST, smaller values are in the left subtree and larger values in the right subtree.', 0, 'Both true; R explains A.'),
    ('Inserting values in random order usually gives a reasonably balanced BST.', 'Random insertion order makes a degenerate tree very unlikely.', 0, 'Both true; R explains A.'),
    ('A leaf node has exactly one child.', 'A leaf node is at the bottom of the tree.', 3, 'A is false (no children); R is true.'),
])


# ---- sets ----
@R.add('ch11-st4', 'C3', (1, 5), 'short')
def set_ops(rng, slot):
    ctx = rng.choice([('students in the robotics club', 'students in the chess club', PEOPLE), ('cities served by airline A', 'cities served by airline B', CITIES),
                      ('songs in Mei\'s playlist', 'songs in Omar\'s playlist', ['Fela', 'Fado', 'Samba', 'Cumbia', 'Raï', 'K-pop', 'Highlife', 'Tango', 'Bhangra'])])
    an, bn, pool = ctx
    A = set(rng.sample(pool, 5))
    B = set(rng.sample(pool, 5))
    ops = [('A ∪ B', A | B, 'union'), ('A ∩ B', A & B, 'intersection'), ('A − B', A - B, 'difference'), ('B − A', B - A, 'difference'), ('A △ B', A ^ B, 'symmetric difference')]
    k = 2 if slot.d <= 2 else 3 if slot.d <= 3 else 5
    pick = rng.sample(ops, k)
    f_ = lambda s: '{' + ', '.join(sorted(s)) + '}' if s else '∅ (empty set)'
    ans = '; '.join(f'{nm} = {f_(v)}' for nm, v, _ in pick)
    extra = f' Is A ∩ B a subset of A ∪ B? Justify.' if slot.d >= 4 else ''
    return dict(stem=f'Let A = {f_(A)} be the {an} and B = {f_(B)} the {bn}. Find ' + ', '.join(nm for nm, _, _ in pick) + f'.{extra}',
                answer=ans + (' Yes – every element in both sets is in at least one of them.' if extra else ''), markingKey=ans + ' A1 each (elements in any order, no duplicates).', marks=k)


@R.add('ch11-st4', 'C3', (2, 5), 'short')
def set_code(rng, slot):
    a = rng.sample(range(1, 15), 6)
    b = rng.sample(range(5, 20), 6)
    code = f'''a = set({a})
b = set({b})
c = a & b
d = a - b
a.add({rng.choice(b)})
a.discard({rng.choice(a + [99])})
print(sorted(c), sorted(d))
print(len(a | b), {rng.choice(a)} in a, c <= b)'''
    out = run_py(code)
    return dict(stem=_code_q(code), answer=out, markingKey=f'Output:\n{out}\nNote c and d are computed before a is changed. A1 per value.', marks=4)


R.facts('ch11-st4', F(
    terms=[('set', 'an ADT that stores an unordered collection of distinct elements and supports membership testing, union, intersection and difference'),
           ('union', 'the set of elements that are in A, in B, or in both (A ∪ B)'),
           ('intersection', 'the set of elements that are in both A and B (A ∩ B)'),
           ('difference', 'the set of elements in A that are not in B (A − B)'),
           ('subset', 'A is a subset of B if every element of A is also an element of B'),
           ('symmetric difference', 'the set of elements in exactly one of A or B (A △ B)')],
    facts=[('What is {2, 4, 6} ∩ {4, 6, 8}?', '{4, 6}', ['{2, 4, 6, 8}', '{2, 8}', '{2}'], 'Elements common to both.'),
           ('Which property distinguishes a set from a list?', 'A set contains no duplicate elements and has no defined order', ['A set can only hold numbers', 'A set has a fixed size', 'A set is always sorted'], 'Uniqueness and no ordering.'),
           ('Testing whether x is in a hash-based set takes, on average…', 'O(1) time', ['O(n) time', 'O(log n) time', 'O(n²) time'], 'Hashing gives constant-time membership tests.')],
    why=[('Explain why converting a list to a set is a quick way to remove duplicates.', 'A set can only hold distinct elements, so adding every list element to a set keeps one copy of each value automatically (O(n) with hashing).'),
         ('Explain why sets are usually implemented with hash tables.', 'Hashing gives average O(1) insertion, deletion and membership tests, which are the main set operations; ordering is not required.'),
         ('Explain why A − B is not the same as B − A in general.', 'A − B contains elements of A missing from B, while B − A contains elements of B missing from A; they are equal only when both are empty (A = B).')],
    contrast=[('union', 'intersection', 'The union contains every element in either set; the intersection contains only elements in both.'),
              ('a set', 'a list', 'A set is unordered with no duplicates and fast membership testing; a list is ordered, allows duplicates and has O(n) membership testing.'),
              ('difference', 'symmetric difference', 'A − B keeps elements only in A; A △ B keeps elements in exactly one of the two sets.')],
    misc=[('The union of two sets of sizes 5 and 4 always has 9 elements.', '|A ∪ B| = |A| + |B| − |A ∩ B|; common elements are counted once.'),
          ('Sets keep elements in the order they were added.', 'Mathematical sets (and Python sets) have no guaranteed order.'),
          ('The empty set is not a subset of any set.', 'The empty set is a subset of every set.')],
    evaluate=[('A set is always a better choice than a list for storing a collection of IDs.', ['O(1) membership tests', 'no duplicates enforced'], ['no order or indexing', 'cannot store repeated values when repetition matters (e.g. a log)', 'extra memory for hashing'], 'Use a set when uniqueness and fast look-up matter; use a list when order, duplicates or indexed access are needed.')],
))
ar('ch11-st4', [
    ('{3, 3, 5} and {5, 3} represent the same set.', 'Sets contain no duplicates and are unordered.', 0, 'Both true; R explains A.'),
    ('A ∩ B is always a subset of A.', 'Every element of A ∩ B is in both A and B.', 0, 'Both true; R explains A.'),
])


# ---- hash tables ----
@R.add('ch11-st5', 'C3', (1, 5), 'short')
def hash_place(rng, slot):
    m = rng.choice([7, 10, 11, 13])
    n = 5 if slot.d <= 2 else 7
    keys = rng.sample(range(10, 200), n)
    method = rng.choice(['linear', 'chain']) if slot.d >= 2 else 'linear'
    if method == 'linear':
        table_ = [None] * m
        probes = 0
        log = []
        for k in keys:
            h = k % m
            i = h
            c = 0
            while table_[i] is not None:
                i = (i + 1) % m
                c += 1
            table_[i] = k
            probes += c
            log.append(f'{k}: h = {h}' + (f' → collision, placed at {i}' if c else ''))
        ans = 'Table: ' + ', '.join(f'[{i}] {v if v is not None else "–"}' for i, v in enumerate(table_)) + f'. Total extra probes: {probes}; load factor {n}/{m} = {n / m:.2f}.'
        desc = 'linear probing (try the next slot, wrapping round)'
    else:
        ch = {i: [] for i in range(m)}
        log = []
        for k in keys:
            ch[k % m].append(k)
            log.append(f'{k}: h = {k % m}')
        longest = max(len(v) for v in ch.values())
        ans = 'Chains: ' + ', '.join(f'[{i}] ' + ('→'.join(map(str, v)) if v else '–') for i, v in ch.items()) + f'. Longest chain {longest}; load factor {n}/{m} = {n / m:.2f}.'
        desc = 'separate chaining (new keys added to the end of the slot\'s list)'
    return dict(stem=f'Keys are inserted in the order {", ".join(map(str, keys))} into a hash table with {m} slots (0–{m - 1}) using h(k) = k mod {m} and {desc}. Show the final table and state the load factor.',
                answer=ans, markingKey=f'{"; ".join(log)}. {ans} M1 hash values; A1 collisions resolved correctly; A1 load factor.', marks=3 if slot.d <= 2 else 4)


@R.add('ch11-st5', 'C3', (2, 5), 'short')
def str_hash(rng, slot):
    words = rng.sample(['CAT', 'ACT', 'DOG', 'LIMA', 'OSLO', 'MAIL', 'LIAM', 'RICE', 'BOOK', 'KOBE', 'TEA', 'EAT'], 4)
    m = rng.choice([11, 13, 17])
    hs = {w: sum(ord(c) for c in w) % m for w in words}
    coll = [w for w in words if list(hs.values()).count(hs[w]) > 1]
    ans = '; '.join(f'{w}: ({"+".join(str(ord(c)) for c in w)}) mod {m} = {hs[w]}' for w in words) + ('. Collisions: ' + ', '.join(coll) + '.' if coll else '. No collisions.')
    return dict(stem=f'A hash function adds the ASCII codes of the characters of a key (A = 65, …, Z = 90) and takes the result mod {m}. Calculate the hash of each key: {", ".join(words)}. Identify any collisions and explain one weakness of this hash function.',
                answer=ans + ' Weakness: anagrams (e.g. CAT/ACT) always collide because addition ignores character order; values cluster.',
                markingKey=ans + ' A1 per two hashes; A1 collisions; R1 weakness (order-insensitive / poor distribution).', marks=4)


R.facts('ch11-st5', F(
    terms=[('hash table', 'a data structure that stores key-value pairs in an array, using a hash function to compute the index (bucket) for each key'),
           ('hash function', 'a function that maps a key to an index in the hash table; it should be fast and spread keys evenly'),
           ('collision', 'when two different keys are mapped by the hash function to the same index'),
           ('linear probing', 'an open-addressing collision strategy that places a colliding key in the next free slot, wrapping round the table'),
           ('separate chaining', 'a collision strategy in which each slot holds a linked list of all the keys that hash to it'),
           ('load factor', 'the number of stored items divided by the number of slots in a hash table'),
           ('dictionary (map)', 'an ADT storing key-value pairs with operations to insert, look up and delete a value by its key, usually implemented with a hash table'),
           ('rehashing', 'creating a larger table and re-inserting every key when the load factor becomes too high')],
    facts=[('What is the average time complexity of looking up a key in a well-designed hash table?', 'O(1)', ['O(n)', 'O(log n)', 'O(n log n)'], 'The hash gives the position directly.'),
           ('Using h(k) = k mod 10, which keys collide: 23, 47, 53, 61?', '23 and 53', ['47 and 61', '23 and 47', 'None'], 'Both give remainder 3.'),
           ('Which problem is typical of linear probing?', 'Primary clustering of occupied slots', ['Keys can never be found', 'Chains grow without limit', 'The table cannot store integers'], 'Runs of filled slots form and grow.')],
    why=[('Explain why the table size in a modulo hash function is often a prime number.', 'A prime modulus spreads keys more evenly, especially when keys share common factors or patterns (e.g. multiples of 10), reducing collisions.'),
         ('Explain why performance degrades as the load factor approaches 1 with linear probing.', 'Free slots become rare, clusters grow, and each insertion or search must probe many occupied slots, so operations tend towards O(n).'),
         ('Explain why deleting from a linearly probed table needs a special "deleted" marker.', 'Emptying a slot could break the probe sequence for keys inserted after a collision, so later searches would stop early and wrongly report them as missing; a tombstone keeps the chain intact.'),
         ('Explain why hash tables do not support efficient sorted output.', 'Keys are scattered by the hash function with no relation to their order, so listing them in order requires sorting all keys (O(n log n)).')],
    contrast=[('linear probing', 'separate chaining', 'Linear probing stores colliding keys in other slots of the same array (no extra memory, but clustering); chaining stores them in a linked list at the same slot (handles load factor > 1, extra pointer memory).'),
              ('a hash table', 'a binary search tree', 'A hash table offers average O(1) look-up but no ordering; a balanced BST offers O(log n) look-up and keeps keys in order for traversal and range queries.'),
              ('a good hash function', 'a poor hash function', 'A good hash function is fast and distributes keys uniformly across slots; a poor one clusters keys into few slots, causing many collisions.')],
    misc=[('A hash table look-up is always O(1).', 'O(1) is the average; with many collisions or a poor hash function it can degrade to O(n).'),
          ('Collisions only happen when the table is full.', 'Collisions can occur at any load factor whenever two keys hash to the same index (birthday paradox).'),
          ('With chaining, the load factor can never exceed 1.', 'Each slot holds a list, so more items than slots (load factor > 1) are possible, though chains get longer.')],
    evaluate=[('Hash tables are the best data structure for implementing a dictionary.', ['average O(1) insert, delete and look-up', 'simple to use (built into most languages)'], ['no ordering or range queries', 'worst-case O(n) and need for resizing', 'memory overhead from empty slots'], 'For most key look-up tasks hash tables are best; where ordering or guaranteed worst-case performance matter, balanced trees are preferable.')],
))
ar('ch11-st5', [
    ('Two different keys can hash to the same index.', 'A hash function maps a large set of possible keys onto a smaller set of indices.', 0, 'Both true; R (pigeonhole principle) explains A.'),
    ('Increasing the table size usually reduces collisions.', 'With more slots, the load factor falls.', 0, 'Both true; R explains A.'),
    ('Separate chaining requires the table to have more slots than keys.', 'Each slot in chaining stores a list of keys.', 3, 'A is false; R is true and shows why many keys can share a slot.'),
])


# =============================================================================================
# ch12 Pre-released case study and Internal Assessment
# =============================================================================================
_CS_CHALLENGES = [
    ('ensuring patient data shared between clinics remains private', 'data privacy and security', 'encryption in transit and at rest, role-based access control, pseudonymisation, audit logs, compliance with data-protection law'),
    ('predicting demand when historical data is sparse or biased', 'data quality and ML bias', 'data augmentation, collecting more representative data, transfer learning, monitoring for drift, human oversight'),
    ('scaling the system to millions of users at peak times', 'scalability', 'horizontal scaling, load balancing, caching, distributed or NoSQL databases, cloud auto-scaling'),
    ('explaining automated decisions to the people affected', 'transparency and explainability', 'interpretable models or explanation tools (feature importance), clear user communication, human review and appeal routes'),
    ('keeping data consistent across offline mobile devices', 'concurrency and synchronisation', 'conflict-resolution rules, versioning/timestamps, eventual consistency with reconciliation, transactions on the server'),
    ('reducing the energy use of training and running models', 'environmental impact', 'smaller or distilled models, efficient hardware, scheduling training when renewable energy is available, choosing low-carbon data centres'),
]


@R.add('ch12-st1', 'C3', (1, 5), 'short')
def cs_challenge(rng, slot):
    org = rng.choice(CASE_ORGS)
    ch, area, sol = rng.choice(_CS_CHALLENGES)
    frame = rng.choice([f'One challenge identified in the case study is {ch}. Identify the area of computer science this challenge relates to and outline two possible approaches.',
                        f'Explain why {ch} is a challenge for this organisation and suggest how it could be addressed.',
                        f'The organisation\'s technical lead lists "{ch}" as a key challenge. Outline the computer-science concepts a student should research to understand this challenge.'])
    return dict(stem=f'{org} {frame}', answer=f'Area: {area}. Approaches: {sol}.',
                markingKey=f'Area/concept identified: {area} (1). Approaches/concepts: {sol} – 1 mark per relevant, context-specific point (max {3 if slot.d <= 3 else 4}).', marks=3 if slot.d <= 3 else 5)


_STAKE = [('patients', 'privacy, accurate and fair decisions, accessibility'), ('clinic managers', 'cost, efficiency, legal compliance'), ('software developers', 'maintainability, clear requirements, scalability'),
          ('drivers', 'fair pay and allocation, transparency of algorithms'), ('regulators', 'compliance with data-protection and AI law, accountability'), ('farmers', 'reliable predictions, low cost, offline access'),
          ('passengers', 'reliability, privacy of location data, fair pricing'), ('teachers', 'accurate data, workload, student privacy')]


@R.add('ch12-st1', 'C3', (2, 4), 'short')
def cs_stakeholders(rng, slot):
    org = rng.choice(CASE_ORGS)
    st = rng.sample(_STAKE, 2)
    ans = '; '.join(f'{a}: {b}' for a, b in st)
    return dict(stem=f'{org} Outline the interests of two stakeholder groups, such as {st[0][0]} and {st[1][0]}, in the proposed system, and identify one way in which their interests might conflict.',
                answer=ans + '. Conflict: e.g. efficiency/cost goals vs privacy, fairness or transparency for individuals.',
                markingKey=ans + ' 1 mark per stakeholder interest (with context), 1-2 marks for a plausible conflict.', marks=4)


R.facts('ch12-st1', F(
    terms=[('pre-released case study', 'a scenario issued by the IB before the examination that students research in depth and that forms the basis of the case-study questions in Paper 1'),
           ('stakeholder', 'a person or group affected by, or with an interest in, a computer system'),
           ('technical terminology (case study)', 'the specialist vocabulary listed in or implied by the case study that students must be able to define and apply'),
           ('challenge (case study)', 'a problem faced by the organisation in the case study that requires computer-science knowledge to analyse and address'),
           ('scenario', 'the fictional or real-world context described in the case study, including the organisation, its systems and its problems')],
    facts=[('What is the best first step when analysing a pre-released case study?', 'Read it carefully and list the key terms, systems, stakeholders and challenges', ['Memorise model answers from the internet', 'Write code for the system', 'Ignore the terminology section'], 'Systematic analysis comes first.'),
           ('Case-study questions in Paper 1 mainly reward…', 'applying computer-science knowledge to the specific scenario', ['repeating the case-study text', 'general opinions without technical detail', 'drawing diagrams only'], 'Answers must be technical and in context.')],
    why=[('Explain why students should research beyond the text of the case study.', 'Examination questions can ask about the underlying technologies, alternatives and ethical issues in more depth than the case study explains; additional research gives the technical knowledge needed to analyse and evaluate.'),
         ('Explain why answers to case-study questions should refer explicitly to the scenario.', 'The questions assess application; generic answers that could apply to any organisation do not show how the concept affects this particular situation and receive fewer marks.'),
         ('Explain why it is useful to build a glossary while studying the case study.', 'Questions often require precise definitions; a glossary of the technical terms with examples from the scenario helps answer "define" and "explain" questions accurately and consistently.')],
    contrast=[('a stakeholder', 'a user', 'A user directly interacts with the system; a stakeholder is anyone affected by or interested in it, including users, managers, developers, regulators and the public.'),
              ('a social/ethical issue', 'a technical issue', 'A technical issue concerns how a system works (performance, scalability, security mechanisms); a social or ethical issue concerns its impact on people (privacy, fairness, employment).')],
    misc=[('The case study only requires knowledge of the technologies named in it.', 'Questions may test related concepts, alternatives and their implications; research should cover the wider computer science the scenario relies on.'),
          ('Memorising the case study text is enough to answer the questions.', 'Questions require analysis, application and evaluation, which need understanding of the underlying computer science, not just recall of the text.')],
    evaluate=[('Studying a pre-released case study gives an unfair advantage to students with more time for research.', ['access to resources and time varies', 'some topics may be unfamiliar to some cultures'], ['all students receive it months in advance', 'questions reward understanding over volume of research', 'schools guide preparation'], 'The case study is designed to be accessible; fairness depends mostly on structured school preparation rather than extra private research.')],
))
ar('ch12-st1', [
    ('Case-study answers should refer to the scenario.', 'Marks are awarded for applying knowledge in context.', 0, 'Both true; R explains A.'),
    ('Students should only learn the terms defined in the case study.', 'Questions can test related concepts not defined in the text.', 3, 'A is false; R is true.'),
])


_CMD = [
    ('Define', 'Give the precise meaning of a word, phrase, concept or physical quantity.'),
    ('State', 'Give a specific name, value or other brief answer without explanation or calculation.'),
    ('Outline', 'Give a brief account or summary.'),
    ('Describe', 'Give a detailed account.'),
    ('Explain', 'Give a detailed account including reasons or causes.'),
    ('Distinguish', 'Make clear the differences between two or more concepts or items.'),
    ('Compare', 'Give an account of the similarities between two (or more) items or situations, referring to both throughout.'),
    ('Compare and contrast', 'Give an account of similarities and differences between two (or more) items or situations, referring to both throughout.'),
    ('Evaluate', 'Make an appraisal by weighing up the strengths and limitations.'),
    ('Discuss', 'Offer a considered and balanced review that includes a range of arguments, factors or hypotheses, with opinions or conclusions supported by appropriate evidence.'),
    ('To what extent', 'Consider the merits or otherwise of an argument or concept; opinions and conclusions should be presented clearly and supported with appropriate evidence and sound argument.'),
    ('Justify', 'Give valid reasons or evidence to support an answer or conclusion.'),
    ('Identify', 'Provide an answer from a number of possibilities.'),
    ('Construct', 'Display information in a diagrammatic or logical form.'),
    ('Trace', 'Follow and record the action of an algorithm.'),
]


@R.add('ch12-st2', 'C1', (1, 3), 'mcq')
def cmd_mcq(rng, slot):
    t, d = rng.choice(_CMD)
    wr = rng.sample([x for x in _CMD if x[0] != t], 3)
    if rng.random() < 0.5:
        return mcq(rng, f'In IB Computer Science examinations, which description matches the command term "{t}"?', d, [w[1] for w in wr], f'{t}: {d}')
    return mcq(rng, f'Which IB command term means: "{d}"', t, [w[0] for w in wr], f'{t}: {d}')


@R.add('ch12-st2', 'C3', (2, 5), 'short')
def cmd_plan(rng, slot):
    org = rng.choice(CASE_ORGS)
    ch, area, sol = rng.choice(_CS_CHALLENGES)
    t, m = rng.choice([('Evaluate', 6), ('Discuss', 6), ('To what extent', 8), ('Explain', 4), ('Compare and contrast', 6)])
    q = f'{t} {"the extent to which " if t == "To what extent" else ""}the organisation\'s approach to {ch}' if t != 'To what extent' else f'To what extent will the proposed system succeed in {ch}?'
    plan = {'Evaluate': 'state the approach; give 2–3 strengths and 2–3 limitations with technical detail in context; weigh them; reach a justified conclusion',
            'Discuss': 'present arguments/factors on more than one side with evidence from the scenario; consider alternatives; give a supported conclusion',
            'To what extent': 'set out arguments for and against with technical evidence, consider conditions/limitations, and conclude with a clear judgement of extent',
            'Explain': 'give a linked chain of reasons (cause → effect) using correct terminology and the scenario; no evaluation needed',
            'Compare and contrast': 'identify similarities and differences between the options point by point, referring to both throughout, applied to the scenario'}[t]
    return dict(stem=f'{org} A Paper 1 case-study question reads: "{q.rstrip('?') + '?' if q.endswith('?') else q + '.'}" [{m}] Describe how a student should structure a high-scoring answer, explaining what the command term requires.',
                answer=f'{t}: {plan}. Relevant content: {sol}.',
                markingKey=f'Command-term requirement: {plan} (2). Planned content relevant to {area}: {sol} (1-2). Allocation of time/points to the {m} marks and use of the scenario (1).', marks=4)


R.facts('ch12-st2', F(
    terms=[('command term', 'a word such as define, explain or evaluate that tells the candidate what kind of response a question requires'),
           ('markband', 'a level descriptor used to mark extended responses holistically, describing the quality of answer needed for each range of marks'),
           ('challenge question', 'a case-study question in Paper 1 that asks candidates to analyse or evaluate a challenge faced by the organisation using their research'),
           ('mark allocation', 'the number of marks shown for a question part, indicating how many distinct, developed points are expected')],
    why=[('Explain why the mark allocation should guide the length of an answer.', 'Each mark usually corresponds to one relevant point or step; the allocation shows how many developed points are expected, so candidates avoid writing too little or wasting time.'),
         ('Explain why an "evaluate" answer must reach a conclusion.', 'Evaluating means weighing strengths against limitations; without a judgement that follows from the weighing, the response is only descriptive and cannot reach the top markband.'),
         ('Explain why generic answers score poorly on case-study questions.', 'Markbands reward application to the scenario; a generic list of advantages shows knowledge but not analysis of how it applies to the organisation\'s specific situation.')],
    contrast=[('"explain"', '"evaluate"', '"Explain" requires reasons or causes for something; "evaluate" requires weighing strengths and limitations and making an appraisal/judgement.'),
              ('"outline"', '"describe"', '"Outline" asks for a brief account; "describe" asks for a detailed account.'),
              ('"discuss"', '"to what extent"', '"Discuss" asks for a balanced review of arguments with a supported conclusion; "to what extent" additionally requires a clear judgement about how far a claim is true.')],
    misc=[('A six-mark "discuss" question can be answered with a bullet list of six advantages.', 'It needs a balanced, developed argument with points on more than one side, applied to the scenario, and a conclusion.'),
          ('Using more technical terms always gains more marks.', 'Terms gain credit only when used accurately and applied to the question; misused jargon earns nothing.')],
    evaluate=[('Planning an answer before writing wastes time in a timed examination.', ['time is limited', 'some short questions need no plan'], ['for 6–8 mark questions a brief plan ensures balance and a conclusion', 'reduces repetition and irrelevance', 'helps meet the command term'], 'A short plan is worthwhile for extended-response questions and saves time overall; it is unnecessary for 1–2 mark items.')],
))
ar('ch12-st2', [
    ('An answer to an "evaluate" question should include a judgement.', 'Evaluate means making an appraisal by weighing strengths and limitations.', 0, 'Both true; R explains A.'),
    ('"State" questions require a detailed explanation.', '"State" asks for a specific name, value or brief answer.', 3, 'A is false; R is true.'),
])


# ---- IA problem specification and success criteria ----
_CRIT = [
    ('The system allows the club secretary to add, edit and delete member records.', True, 'specific, testable function'),
    ('A search by surname returns matching records in under 2 seconds for 5000 records.', True, 'measurable performance criterion'),
    ('The program is user-friendly.', False, 'vague: no measurable test – rewrite e.g. "a new user can book a lesson in under 5 clicks"'),
    ('The app looks nice.', False, 'subjective and untestable'),
    ('The system rejects a booking if the room is already booked for that time slot.', True, 'testable validation rule'),
    ('The program works well.', False, 'not specific or measurable'),
    ('The teacher can export a class\'s grades as a CSV file that opens in a spreadsheet.', True, 'specific and testable'),
    ('Passwords are stored as salted hashes, never in plain text.', True, 'testable by inspecting the database'),
    ('The system will be fast.', False, 'no measurable threshold'),
    ('The program will use object-oriented programming.', False, 'describes implementation, not a user requirement the product must meet'),
    ('An email reminder is sent to members 24 hours before each event.', True, 'specific and testable'),
    ('The client will be happy with the product.', False, 'not a measurable feature of the product'),
]


@R.add('ch12-st3', 'C3', (1, 5), 'short')
def crit_judge(rng, slot):
    k = 3 if slot.d <= 2 else 4 if slot.d <= 3 else 5
    its = rng.sample(_CRIT, k)
    ans = '; '.join(f'{i + 1}: {"suitable" if ok else "unsuitable"} – {why}' for i, (_, ok, why) in enumerate(its))
    return dict(stem='A student\'s IA proposes the following success criteria. For each one, state whether it is a suitable (specific and testable) success criterion and justify, rewriting any unsuitable criterion.\n' + '\n'.join(f'{i + 1}. {c}' for i, (c, _, _) in enumerate(its)),
                answer=ans, markingKey=ans + ' 1 mark per correct judgement with justification/rewrite.', marks=k)


_IA_CLIENTS = [('a badminton club in Kuala Lumpur', 'track court bookings and member fees'), ('a family bakery in Lisbon', 'record daily orders and stock of ingredients'),
               ('a school library in Accra', 'manage loans and overdue reminders'), ('a physiotherapy clinic in Toronto', 'schedule appointments and exercise plans'),
               ('a youth football league in Bogotá', 'store fixtures, results and league tables'), ('a community garden in Melbourne', 'allocate plots and log harvests')]


@R.add('ch12-st3', 'C3', (2, 5), 'short')
def ia_spec(rng, slot):
    client, need = rng.choice(_IA_CLIENTS)
    return dict(stem=f'An IA student is developing a computational solution for {client}, which needs to {need}. Write a problem specification outline: identify the client and problem, justify a computational solution, and propose three specific, testable success criteria.',
                answer=f'Client/problem: {client} currently handles the need to {need} manually (paper/spreadsheets), causing errors, lost data and wasted time. Justification: a database-backed application automates storage, validation, searching and reporting. Example criteria: 1) the user can add/edit/delete records with validation of each field; 2) a search returns matching records in under 2 s; 3) the system produces a specified report (e.g. overdue items) on demand.',
                markingKey='Client and problem clearly identified with evidence of consultation (1); computational solution justified (1); three specific, measurable, testable success criteria linked to the problem (1 each).', marks=5)


R.facts('ch12-st3', F(
    terms=[('internal assessment (IA)', 'the computational solution coursework in which a student develops a product to solve a problem, documents the process and demonstrates the product; it is internally marked and externally moderated'),
           ('client', 'the person or organisation for whom the IA product is developed, whose needs define the problem'),
           ('problem specification', 'a clear statement of the problem to be solved, its context and the requirements the solution must meet'),
           ('success criteria', 'specific, measurable statements of what the product must do, used to test and evaluate whether it solves the problem'),
           ('requirements gathering', 'collecting the client\'s needs through interviews, questionnaires, observation or analysing existing systems'),
           ('computational solution', 'a product, such as an application or system, built through programming to solve the identified problem')],
    why=[('Explain why success criteria must be specific and measurable.', 'They are used to test the product and to evaluate it; vague criteria ("easy to use") cannot be shown to be met or not met, while measurable ones ("books a slot in under 30 seconds") can be tested objectively.'),
         ('Explain why consultation with a client is important at the start of an IA.', 'It provides evidence of a genuine problem and real requirements, ensures the success criteria reflect what the client needs, and gives a basis for later feedback and evaluation.'),
         ('Explain why a student should justify why a computational solution is appropriate.', 'Not every problem needs software; justification shows that automation, data processing or validation would genuinely improve on the current method.')],
    contrast=[('a functional requirement', 'a non-functional requirement', 'A functional requirement states what the system must do (add a booking); a non-functional requirement states how well it must do it (response time, security, usability).'),
              ('success criteria', 'test plan', 'Success criteria state what the product must achieve; the test plan describes how each criterion (and each feature) will be tested, with data and expected results.')],
    misc=[('Success criteria should describe the programming techniques used.', 'They describe what the product must do for the client; techniques belong in design and development documentation.'),
          ('A problem specification can be written after the product is finished.', 'It should be developed first, from consultation, because it drives the design and testing.')],
    evaluate=[('A real client is essential for a successful IA.', ['provides authentic requirements and feedback', 'evaluation is more meaningful'], ['an adviser or the student acting as user may suffice for some problems', 'clients can be unavailable or change requirements'], 'A real client strengthens the problem definition and evaluation, though what matters most is a clearly specified, genuine problem with testable criteria.')],
))
ar('ch12-st3', [
    ('"The system is easy to use" is a weak success criterion.', 'It cannot be measured or tested objectively.', 0, 'Both true; R explains A.'),
    ('Success criteria should be agreed with the client.', 'The product is developed to solve the client\'s problem.', 0, 'Both true; R explains A.'),
])


# ---- IA planning, design, development and testing ----
@R.add('ch12-st4', 'C3', (2, 5), 'numerical')
def critical_path(rng, slot):
    tasks = OrderedDict()
    tasks['A Consult client'] = (rng.randint(2, 4), [])
    tasks['B Design database'] = (rng.randint(3, 6), ['A Consult client'])
    tasks['C Design interface'] = (rng.randint(2, 5), ['A Consult client'])
    tasks['D Code back end'] = (rng.randint(6, 12), ['B Design database'])
    tasks['E Code front end'] = (rng.randint(4, 9), ['C Design interface'])
    tasks['F Test and fix'] = (rng.randint(3, 6), ['D Code back end', 'E Code front end'])
    tasks['G Evaluate with client'] = (rng.randint(1, 3), ['F Test and fix'])
    ef = {}
    prev = {}
    for t, (d, deps) in tasks.items():
        st = max((ef[x] for x in deps), default=0)
        prev[t] = max(deps, key=lambda x: ef[x]) if deps else None
        ef[t] = st + d
    end = 'G Evaluate with client'
    path = []
    cur = end
    while cur:
        path.append(cur.split()[0])
        cur = prev[cur]
    path.reverse()
    lst = '\n'.join(f'{t}: {d} days, after {", ".join(x.split()[0] for x in deps) if deps else "—"}' for t, (d, deps) in tasks.items())
    ans = f'Minimum duration {ef[end]} days; critical path {" → ".join(path)}.'
    return dict(stem=f'An IA student plans these tasks:\n{lst}\nDetermine the minimum number of days to complete the project and the critical path. Explain why identifying the critical path helps planning.',
                answer=ans + ' Tasks on the critical path cannot slip without delaying the whole project, so they need closest monitoring; others have float.',
                markingKey=f'Earliest finish times: ' + ', '.join(f'{t.split()[0]} {v}' for t, v in ef.items()) + f' (M1 M1). {ans} (A1). R1 explanation.', marks=4)


@R.add('ch12-st4', 'C3', (1, 5), 'short')
def ia_testplan(rng, slot):
    field, lo, hi = rng.choice([('number of guests per booking', 1, 12), ('player age in a junior league', 8, 16), ('quantity of loaves ordered', 1, 200), ('plot size in m²', 5, 40)])
    mid = rng.randint(lo + 1, hi - 1)
    rows = [(mid, 'normal', 'accepted'), (lo, 'boundary', 'accepted'), (hi, 'boundary', 'accepted'), (lo - 1, 'boundary (just outside)', 'rejected with error message'),
            (hi + 1, 'boundary (just outside)', 'rejected with error message'), ('"ten"', 'erroneous (wrong type)', 'rejected with error message'), ('(blank)', 'erroneous (presence)', 'rejected with error message')]
    k = 4 if slot.d <= 2 else 6 if slot.d <= 3 else 7
    chosen = rows[:k]
    ans = '; '.join(f'{v} – {t} – {e}' for v, t, e in chosen)
    return dict(stem=f'Part of an IA test plan must test the validation of the {field}, which must be an integer from {lo} to {hi}. Construct {k} rows of the test plan giving the test data, the type of test and the expected result.',
                answer=ans, markingKey=ans + ' 1 mark per two correct rows (data, type, expected outcome); must include normal, both boundaries and erroneous data.', marks=max(3, k // 2 + 1))


R.facts('ch12-st4', F(
    terms=[('Gantt chart', 'a chart showing project tasks as bars against a timeline, including their order, duration and overlaps'),
           ('critical path', 'the longest sequence of dependent tasks in a project, which determines the minimum completion time'),
           ('prototype', 'an early working model of the product used to test ideas and gather client feedback'),
           ('iterative development', 'building a product through repeated cycles of design, development, testing and feedback'),
           ('test plan', 'a document listing each test, the data used, the expected result and how it links to the success criteria'),
           ('alpha testing', 'testing carried out by the developer (or in-house) before release'),
           ('beta testing', 'testing carried out by real users or the client in their own environment before final release'),
           ('trace table', 'a table used to record the values of variables step by step as an algorithm runs, to check its logic')],
    why=[('Explain why an IA should show evidence of iterative development.', 'Repeated cycles with testing and client feedback show how the product was refined to meet the success criteria and justify design changes, which is part of good development practice.'),
         ('Explain why test data should include boundary and erroneous values.', 'Most validation errors happen at the limits or with unexpected input; testing them shows the program accepts every valid value and rejects invalid ones without crashing.'),
         ('Explain why algorithms should be designed (e.g. as flowcharts or pseudocode) before coding.', 'Design clarifies the logic, data structures and inputs/outputs independently of syntax, makes errors cheaper to find, and documents the solution for others.'),
         ('Explain why complex techniques should be explained in the IA documentation.', 'The moderator needs to see why each technique was chosen and how it works to credit the student\'s understanding and the ingenuity of the solution.')],
    contrast=[('alpha testing', 'beta testing', 'Alpha testing is done by the developer in a controlled environment; beta testing is done by the client or real users in real conditions.'),
              ('white-box testing', 'black-box testing', 'White-box testing uses knowledge of the code to test paths and branches; black-box testing checks outputs for given inputs against the specification without looking at the code.'),
              ('a prototype', 'the final product', 'A prototype is an early, partial version used for feedback; the final product is the complete, tested solution.')],
    misc=[('Testing only needs to show that the program works with normal data.', 'Tests must also include boundary and erroneous data to show robust validation and error handling.'),
          ('A Gantt chart is only needed for teams, not for an individual IA.', 'It helps an individual schedule tasks, track progress against deadlines and identify dependencies.')],
    evaluate=[('Agile, iterative development is better than a linear (waterfall) approach for an IA.', ['frequent client feedback improves fit to needs', 'problems found early', 'flexible when requirements change'], ['harder to plan a fixed timeline', 'documentation of each iteration takes time', 'waterfall suits well-defined, stable requirements'], 'For most IAs an iterative approach with clear documentation works best, provided the overall plan and deadlines are kept under control.')],
))
ar('ch12-st4', [
    ('Delaying a task on the critical path delays the whole project.', 'The critical path has no slack (float).', 0, 'Both true; R explains A.'),
    ('Black-box testing requires reading the source code.', 'Black-box tests compare actual outputs with expected outputs for given inputs.', 3, 'A is false; R is true.'),
])


# ---- IA evaluation, documentation and video ----
@R.add('ch12-st5', 'C3', (1, 5), 'short')
def ia_eval(rng, slot):
    lim = rng.choice([1.0, 2.0, 3.0])
    times = [round(rng.uniform(0.3, lim * 1.4), 2) for _ in range(5)]
    met_time = all(t < lim for t in times)
    acc = rng.randint(85, 100)
    acc_lim = rng.choice([90, 95])
    clicks = rng.randint(3, 8)
    click_lim = 5
    res = [('search in under ' + r2(lim) + ' s', 'times ' + ', '.join(map(str, times)) + ' s', met_time),
           (f'at least {acc_lim}% of test bookings processed correctly', f'{acc}% correct', acc >= acc_lim),
           (f'a booking takes at most {click_lim} clicks', f'{clicks} clicks', clicks <= click_lim)]
    k = 2 if slot.d <= 2 else 3
    res = res[:k]
    ans = '; '.join(f'"{c}": {e} → {"met" if ok else "not met"}' for c, e, ok in res)
    return dict(stem='An IA student recorded these test results against the success criteria:\n' + '\n'.join(f'Criterion: {c}; evidence: {e}' for c, e, _ in res) + '\nState whether each criterion was met, and suggest one improvement for any criterion that was not met.',
                answer=ans + '. Improvements: e.g. add an index/optimise query for speed; fix validation logic for accuracy; simplify the booking form for clicks.',
                markingKey=ans + ' 1 mark per correct judgement referring to the evidence; 1 mark for a realistic improvement linked to an unmet criterion.', marks=k + 1)


R.facts('ch12-st5', F(
    terms=[('evaluation (IA)', 'judging how well the final product meets each success criterion, using evidence such as test results and client feedback, and recommending improvements'),
           ('client feedback', 'the client\'s documented response to the product, used as evidence in the evaluation'),
           ('video demonstration', 'a short recording showing the product working, used as evidence of its functionality and of the success criteria being met'),
           ('recommendations for improvement', 'realistic, specific suggestions for further development based on the evaluation'),
           ('documentation', 'the written record of the IA, covering the problem, planning, design, development and evaluation with appropriate evidence and references')],
    why=[('Explain why an IA evaluation must refer to each success criterion.', 'The success criteria define what the solution should achieve; evaluating against each one with evidence shows objectively how far the problem has been solved.'),
         ('Explain why client feedback strengthens an evaluation.', 'It provides independent evidence from the intended user on whether the product meets their needs, rather than only the developer\'s opinion.'),
         ('Explain why the video should demonstrate the product rather than explain the code.', 'Its purpose is to show the working functionality and evidence the success criteria are met; code explanation belongs in the development documentation.'),
         ('Explain why recommendations for improvement should be realistic.', 'Credible recommendations follow from evidence of what was not met or could be better and show understanding of feasible next steps; vague or unrealistic ideas show little reflection.')],
    contrast=[('evaluation', 'testing', 'Testing checks specific inputs against expected outputs; evaluation judges overall how well the product solves the problem and meets the criteria, using test results and feedback.'),
              ('a limitation of the product', 'a recommendation', 'A limitation is a weakness found in the product; a recommendation is a proposed future change to address it or extend the product.')],
    misc=[('If the product works, the evaluation can simply say "all criteria were met".', 'Each claim must be backed by specific evidence (test results, screenshots, client feedback) and limitations should be considered honestly.'),
          ('The video should be as long as possible to show everything.', 'It should be concise and focused on demonstrating that the product works and meets its success criteria.')],
    evaluate=[('Client feedback is more valuable than test results in an IA evaluation.', ['shows whether the product meets real needs', 'reveals usability issues tests may miss'], ['feedback can be subjective or polite', 'tests provide objective, repeatable evidence', 'both are needed to judge each criterion'], 'The strongest evaluations combine objective test evidence with client feedback for each success criterion.')],
))
ar('ch12-st5', [
    ('An IA evaluation should be based on the success criteria.', 'The success criteria state what the product must achieve.', 0, 'Both true; R explains A.'),
    ('The video demonstration is mainly for explaining the source code.', 'The video shows the product functioning.', 3, 'A is false; R is true.'),
])


# =============================================================================================
# Theme B programming tasks with model answers (every model answer is executed against tests at import)
# =============================================================================================
def code_tasks(key, items, c='C4', d=(3, 5)):
    for stem, model, test, marks in items:
        g = {}
        exec(model + '\n' + test, g)   # raises if the model answer is wrong
    def fn(rng, slot):
        stem, model, test, marks = rng.choice(items)
        return dict(stem=stem, answer=model, type='long',
                    markingKey=f'Model answer (Python; an equivalent Java solution is equally acceptable):\n{model}\nMarks: correct class/method headers and parameters; correct use of attributes (self/this); correct logic and validation; correct return values/output. Tested with:\n{test}',
                    marks=marks)
    R.t.setdefault(key, []).append(T(c, d, fn, 'long', None, 'code_task'))


code_tasks('ch09-st1', [
    ('A parking garage in Singapore needs a class CarPark. Write the class with attributes capacity and occupied (initially 0), and methods enter() (returns False if full, otherwise increments occupied and returns True), leave() (never lets occupied go below 0) and free_spaces().',
     '''class CarPark:
    def __init__(self, capacity):
        self.capacity = capacity
        self.occupied = 0

    def enter(self):
        if self.occupied >= self.capacity:
            return False
        self.occupied += 1
        return True

    def leave(self):
        if self.occupied > 0:
            self.occupied -= 1

    def free_spaces(self):
        return self.capacity - self.occupied''',
     'c = CarPark(2)\nassert c.enter() and c.enter() and not c.enter()\nc.leave(); c.leave(); c.leave()\nassert c.free_spaces() == 2', 6),
    ('Write a class Recipe for a cooking app in Lisbon. It stores a name and a dictionary of ingredients (name → grams). Methods: add(ingredient, grams) adds grams (accumulating if the ingredient already exists); total_mass() returns the total grams; scale(factor) returns a NEW dictionary with every quantity multiplied by factor, leaving the recipe unchanged.',
     '''class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = {}

    def add(self, ingredient, grams):
        self.ingredients[ingredient] = self.ingredients.get(ingredient, 0) + grams

    def total_mass(self):
        return sum(self.ingredients.values())

    def scale(self, factor):
        return {k: v * factor for k, v in self.ingredients.items()}''',
     'r = Recipe("Pastel")\nr.add("flour", 200); r.add("sugar", 50); r.add("flour", 100)\nassert r.total_mass() == 350\nassert r.scale(2)["flour"] == 600 and r.ingredients["flour"] == 300', 6),
    ('Write a class StepCounter with attributes owner and a list daily_steps. Include methods record(steps) (ignores negative values), best_day() returning the largest value (or 0 if empty) and goal_days(goal) returning how many days met or exceeded goal.',
     '''class StepCounter:
    def __init__(self, owner):
        self.owner = owner
        self.daily_steps = []

    def record(self, steps):
        if steps >= 0:
            self.daily_steps.append(steps)

    def best_day(self):
        if not self.daily_steps:
            return 0
        return max(self.daily_steps)

    def goal_days(self, goal):
        return sum(1 for s in self.daily_steps if s >= goal)''',
     's = StepCounter("Aiko")\nassert s.best_day() == 0\nfor v in [4000, -5, 12000, 8000]: s.record(v)\nassert s.best_day() == 12000 and s.goal_days(8000) == 2', 5),
])

code_tasks('ch09-st2', [
    ('Write a class Booking whose constructor takes guest, nights and an optional room_type (default "standard"). The constructor must raise ValueError if nights is less than 1, and set price_per_night to 90 for "standard" and 150 for "suite". Add a method total() returning nights × price_per_night.',
     '''class Booking:
    PRICES = {"standard": 90, "suite": 150}

    def __init__(self, guest, nights, room_type="standard"):
        if nights < 1:
            raise ValueError("nights must be at least 1")
        self.guest = guest
        self.nights = nights
        self.room_type = room_type
        self.price_per_night = Booking.PRICES[room_type]

    def total(self):
        return self.nights * self.price_per_night''',
     'b = Booking("Kwame", 3)\nassert b.total() == 270\nassert Booking("Mei", 2, "suite").total() == 300\ntry:\n    Booking("X", 0)\n    assert False\nexcept ValueError:\n    pass', 5),
    ('Write a class Fraction whose constructor takes a numerator and denominator (default 1), rejects a zero denominator with ValueError, and stores the fraction in lowest terms with a positive denominator. Add a method value() returning the decimal value.',
     '''from math import gcd

class Fraction:
    def __init__(self, num, den=1):
        if den == 0:
            raise ValueError("denominator cannot be zero")
        if den < 0:
            num, den = -num, -den
        g = gcd(num, den)
        self.num = num // g
        self.den = den // g

    def value(self):
        return self.num / self.den''',
     'f = Fraction(6, -8)\nassert (f.num, f.den) == (-3, 4)\nassert Fraction(5).value() == 5.0', 6),
])

code_tasks('ch09-st3', [
    ('Write an encapsulated class BankCard with a private PIN and a private balance. Provide check_pin(pin) returning True/False; withdraw(pin, amount) that only succeeds if the PIN is correct, the amount is positive and does not exceed the balance (return True/False); and get_balance(). After three consecutive wrong PINs the card is blocked and every later call to withdraw returns False.',
     '''class BankCard:
    def __init__(self, pin, balance):
        self.__pin = pin
        self.__balance = balance
        self.__fails = 0

    def check_pin(self, pin):
        return pin == self.__pin

    def withdraw(self, pin, amount):
        if self.__fails >= 3:
            return False
        if not self.check_pin(pin):
            self.__fails += 1
            return False
        self.__fails = 0
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def get_balance(self):
        return self.__balance''',
     'c = BankCard(1234, 100)\nassert c.withdraw(1234, 40) and c.get_balance() == 60\nfor _ in range(3): c.withdraw(1, 10)\nassert not c.withdraw(1234, 10) and c.get_balance() == 60', 7),
    ('Write a class Thermometer with a private attribute celsius. Provide get_celsius(), set_celsius(value) that rejects values below −273.15 (returning False), and a read-only computed accessor get_fahrenheit() (F = C × 9/5 + 32). Explain in a comment why there is no set_fahrenheit attribute.',
     '''class Thermometer:
    def __init__(self, celsius=0.0):
        self.__celsius = celsius

    def get_celsius(self):
        return self.__celsius

    def set_celsius(self, value):
        if value < -273.15:
            return False
        self.__celsius = value
        return True

    def get_fahrenheit(self):
        # derived from celsius, so it is never stored separately (avoids inconsistent data)
        return self.__celsius * 9 / 5 + 32''',
     't = Thermometer(100)\nassert t.get_fahrenheit() == 212\nassert not t.set_celsius(-300) and t.get_celsius() == 100', 5),
])

code_tasks('ch09-st4', [
    ('Write a class Ticket where each new ticket receives a unique, sequential number starting at 1001, using a class (static) variable. Add a static/class method issued() returning how many tickets have been created, and an instance method label() returning e.g. "T1003".',
     '''class Ticket:
    next_number = 1001
    count = 0

    def __init__(self):
        self.number = Ticket.next_number
        Ticket.next_number += 1
        Ticket.count += 1

    @staticmethod
    def issued():
        return Ticket.count

    def label(self):
        return "T" + str(self.number)''',
     'a = Ticket(); b = Ticket(); c = Ticket()\nassert c.label() == "T1003" and Ticket.issued() == 3', 5),
    ('Write a class Converter containing only static methods km_to_miles(km) (1 km = 0.621371 miles, rounded to 2 dp) and celsius_to_f(c), and explain in a comment why no object needs to be created.',
     '''class Converter:
    # stateless utility methods: they use only their parameters, so no object state is needed
    @staticmethod
    def km_to_miles(km):
        return round(km * 0.621371, 2)

    @staticmethod
    def celsius_to_f(c):
        return c * 9 / 5 + 32''',
     'assert Converter.km_to_miles(10) == 6.21 and Converter.celsius_to_f(0) == 32', 4),
])

code_tasks('ch09-st5', [
    ('A UML class diagram shows: Course | - code: String, - title: String, - students: List<String>, - capacity: int | + Course(code: String, title: String, capacity: int), + enrol(name: String): boolean, + withdraw(name: String): void, + size(): int. Implement the class. enrol must reject duplicates and enrolments beyond capacity.',
     '''class Course:
    def __init__(self, code, title, capacity):
        self.__code = code
        self.__title = title
        self.__students = []
        self.__capacity = capacity

    def enrol(self, name):
        if name in self.__students or len(self.__students) >= self.__capacity:
            return False
        self.__students.append(name)
        return True

    def withdraw(self, name):
        if name in self.__students:
            self.__students.remove(name)

    def size(self):
        return len(self.__students)''',
     'c = Course("CS1", "Databases", 2)\nassert c.enrol("Nia") and not c.enrol("Nia") and c.enrol("Lars") and not c.enrol("Ana")\nc.withdraw("Nia"); assert c.size() == 1', 6),
])

code_tasks('ch10-st1', [
    ('Write a superclass Employee (name, hourly_rate, method pay(hours) = hours × rate) and a subclass Contractor that adds an agency_fee percentage and overrides pay so that it returns the superclass pay plus the fee. Use super() rather than repeating code.',
     '''class Employee:
    def __init__(self, name, hourly_rate):
        self.name = name
        self.hourly_rate = hourly_rate

    def pay(self, hours):
        return hours * self.hourly_rate

class Contractor(Employee):
    def __init__(self, name, hourly_rate, agency_fee):
        super().__init__(name, hourly_rate)
        self.agency_fee = agency_fee

    def pay(self, hours):
        base = super().pay(hours)
        return base + base * self.agency_fee / 100''',
     'assert Employee("A", 20).pay(10) == 200\nassert Contractor("B", 20, 10).pay(10) == 220', 6),
    ('Write a class Account (owner, balance, withdraw(amount) refusing overdrafts) and a subclass StudentAccount that allows an overdraft down to −200 by overriding withdraw. Both withdraw methods return True on success.',
     '''class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

class StudentAccount(Account):
    LIMIT = -200

    def withdraw(self, amount):
        if self.balance - amount < StudentAccount.LIMIT:
            return False
        self.balance -= amount
        return True''',
     'a = Account("x", 50); assert not a.withdraw(60)\ns = StudentAccount("y", 50); assert s.withdraw(200) and s.balance == -150 and not s.withdraw(100)', 6),
])

code_tasks('ch10-st2', [
    ('Write classes Delivery (with method cost(km) returning 0), Bike (2 + 0.5 per km), Van (10 + 1.2 per km) and Drone (5 per delivery, but returns -1 meaning "not possible" if km > 15). Write a function cheapest(options, km) that uses polymorphism to return the name of the class of the cheapest possible option.',
     '''class Delivery:
    def cost(self, km):
        return 0

class Bike(Delivery):
    def cost(self, km):
        return 2 + 0.5 * km

class Van(Delivery):
    def cost(self, km):
        return 10 + 1.2 * km

class Drone(Delivery):
    def cost(self, km):
        return -1 if km > 15 else 5

def cheapest(options, km):
    best = None
    for o in options:
        c = o.cost(km)
        if c >= 0 and (best is None or c < best[0]):
            best = (c, type(o).__name__)
    return best[1] if best else None''',
     'opts = [Bike(), Van(), Drone()]\nassert cheapest(opts, 4) == "Bike" and cheapest(opts, 12) == "Drone" and cheapest(opts, 20) == "Bike"', 7),
])

code_tasks('ch10-st3', [
    ('Using Python\'s abc module, write an abstract class Sensor with an abstract method read() and a concrete method status() returning "ALERT" if read() exceeds a threshold attribute, else "OK". Write two concrete subclasses TempSensor (returns a stored temperature) and SmokeSensor (returns a stored ppm).',
     '''from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, threshold):
        self.threshold = threshold

    @abstractmethod
    def read(self):
        pass

    def status(self):
        return "ALERT" if self.read() > self.threshold else "OK"

class TempSensor(Sensor):
    def __init__(self, temp):
        super().__init__(40)
        self.temp = temp

    def read(self):
        return self.temp

class SmokeSensor(Sensor):
    def __init__(self, ppm):
        super().__init__(300)
        self.ppm = ppm

    def read(self):
        return self.ppm''',
     'assert TempSensor(45).status() == "ALERT" and SmokeSensor(100).status() == "OK"\ntry:\n    Sensor(1)\n    assert False\nexcept TypeError:\n    pass', 7),
])

code_tasks('ch10-st4', [
    ('Write classes OrderLine (product, unit_price, qty, method subtotal()) and Order, which is COMPOSED of order lines: Order creates its own OrderLine objects in add_line(product, price, qty) and provides total(). Explain in a comment why this is composition rather than aggregation.',
     '''class OrderLine:
    def __init__(self, product, unit_price, qty):
        self.product = product
        self.unit_price = unit_price
        self.qty = qty

    def subtotal(self):
        return self.unit_price * self.qty

class Order:
    # composition: the Order creates and owns its lines; they do not exist without the order
    def __init__(self, order_id):
        self.order_id = order_id
        self.lines = []

    def add_line(self, product, price, qty):
        self.lines.append(OrderLine(product, price, qty))

    def total(self):
        return sum(line.subtotal() for line in self.lines)''',
     'o = Order(1)\no.add_line("tea", 3, 4); o.add_line("rice", 10, 2)\nassert o.total() == 32', 6),
])

code_tasks('ch10-st5', [
    ('Implement the observer pattern for a stock-price feed: a class Stock with subscribe(observer), unsubscribe(observer) and set_price(p), which notifies every observer by calling observer.update(symbol, p) only when the price changes. Write an Observer class Alert that records messages "SYM above X" whenever the price exceeds its limit.',
     '''class Stock:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price
        self.observers = []

    def subscribe(self, o):
        self.observers.append(o)

    def unsubscribe(self, o):
        self.observers.remove(o)

    def set_price(self, p):
        if p != self.price:
            self.price = p
            for o in self.observers:
                o.update(self.symbol, p)

class Alert:
    def __init__(self, limit):
        self.limit = limit
        self.messages = []

    def update(self, symbol, price):
        if price > self.limit:
            self.messages.append(symbol + " above " + str(self.limit))''',
     's = Stock("KEN", 10)\na = Alert(12)\ns.subscribe(a)\ns.set_price(13); s.set_price(13); s.set_price(11)\ns.unsubscribe(a); s.set_price(20)\nassert a.messages == ["KEN above 12"]', 7),
    ('Implement a thread-unsafe singleton Logger in Python: Logger.get() always returns the same instance; the instance has a list entries and a method log(msg) that appends msg with a running number, e.g. "1: started".',
     '''class Logger:
    _instance = None

    def __init__(self):
        self.entries = []

    @staticmethod
    def get():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance

    def log(self, msg):
        self.entries.append(str(len(self.entries) + 1) + ": " + msg)''',
     'Logger.get().log("started"); Logger.get().log("saved")\nassert Logger.get() is Logger.get() and Logger.get().entries == ["1: started", "2: saved"]', 5),
])

code_tasks('ch11-st1', [
    ('Write a class Stack implemented with a Python list, with methods push(x), pop() (raising IndexError when empty), peek(), is_empty() and size(). Then write a function reverse_words(sentence) that uses your Stack to reverse the order of the words.',
     '''class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

def reverse_words(sentence):
    s = Stack()
    for w in sentence.split():
        s.push(w)
    out = []
    while not s.is_empty():
        out.append(s.pop())
    return " ".join(out)''',
     'assert reverse_words("data structures are fun") == "fun are structures data"', 6),
    ('Write a class CircularQueue of fixed capacity using a list and front/rear indices that wrap with modulo arithmetic. Provide enqueue(x) (returns False when full), dequeue() (returns None when empty) and is_full().',
     '''class CircularQueue:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.capacity = capacity
        self.front = 0
        self.count = 0

    def is_full(self):
        return self.count == self.capacity

    def enqueue(self, x):
        if self.is_full():
            return False
        rear = (self.front + self.count) % self.capacity
        self.data[rear] = x
        self.count += 1
        return True

    def dequeue(self):
        if self.count == 0:
            return None
        x = self.data[self.front]
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return x''',
     'q = CircularQueue(3)\nassert q.enqueue(1) and q.enqueue(2) and q.enqueue(3) and not q.enqueue(4)\nassert q.dequeue() == 1 and q.enqueue(4)\nassert [q.dequeue(), q.dequeue(), q.dequeue(), q.dequeue()] == [2, 3, 4, None]', 7),
])

code_tasks('ch11-st2', [
    ('Write a Node class and a LinkedList class with a head pointer. Implement insert_sorted(value), which inserts a value so the list stays in ascending order, and to_list(), which returns the values as a Python list.',
     '''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_sorted(self, value):
        node = Node(value)
        if self.head is None or value < self.head.data:
            node.next = self.head
            self.head = node
            return
        cur = self.head
        while cur.next is not None and cur.next.data <= value:
            cur = cur.next
        node.next = cur.next
        cur.next = node

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out''',
     'L = LinkedList()\nfor v in [30, 10, 20, 5, 40, 20]: L.insert_sorted(v)\nassert L.to_list() == [5, 10, 20, 20, 30, 40]', 7),
    ('Add a method delete(value) to a singly linked list (head pointer, nodes with data and next) that removes the first node containing value and returns True, or returns False if the value is absent. Handle deletion of the head.',
     '''class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self, values=()):
        self.head = None
        for v in reversed(values):
            self.head = Node(v, self.head)

    def delete(self, value):
        prev, cur = None, self.head
        while cur is not None:
            if cur.data == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev, cur = cur, cur.next
        return False''',
     'L = LinkedList([4, 8, 15])\nassert L.delete(4) and L.head.data == 8 and L.delete(15) and not L.delete(99) and L.head.next is None', 6),
])

code_tasks('ch11-st3', [
    ('Write a BST class with insert(value) and a recursive method in_order() that returns a list of values in ascending order, plus height() (edges on the longest path; −1 for an empty tree).',
     '''class TreeNode:
    def __init__(self, v):
        self.v = v
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, v):
        def rec(n):
            if n is None:
                return TreeNode(v)
            if v < n.v:
                n.left = rec(n.left)
            else:
                n.right = rec(n.right)
            return n
        self.root = rec(self.root)

    def in_order(self):
        out = []
        def rec(n):
            if n:
                rec(n.left)
                out.append(n.v)
                rec(n.right)
        rec(self.root)
        return out

    def height(self):
        def h(n):
            return -1 if n is None else 1 + max(h(n.left), h(n.right))
        return h(self.root)''',
     't = BST()\nfor v in [50, 30, 70, 20, 40, 80, 85]: t.insert(v)\nassert t.in_order() == [20, 30, 40, 50, 70, 80, 85] and t.height() == 3', 7),
    ('Write a function count_in_range(node, lo, hi) for a BST (nodes with v, left, right) that counts values between lo and hi inclusive, skipping subtrees that cannot contain values in range.',
     '''class TreeNode:
    def __init__(self, v, left=None, right=None):
        self.v = v
        self.left = left
        self.right = right

def count_in_range(node, lo, hi):
    if node is None:
        return 0
    if node.v < lo:
        return count_in_range(node.right, lo, hi)
    if node.v > hi:
        return count_in_range(node.left, lo, hi)
    return 1 + count_in_range(node.left, lo, hi) + count_in_range(node.right, lo, hi)''',
     'root = TreeNode(50, TreeNode(30, TreeNode(20), TreeNode(40)), TreeNode(70, None, TreeNode(80)))\nassert count_in_range(root, 25, 70) == 4', 6),
])

code_tasks('ch11-st4', [
    ('Without using Python\'s built-in set type, write a class IntSet storing distinct integers in a list, with add(x), contains(x), union(other) and intersection(other) (both returning new IntSet objects).',
     '''class IntSet:
    def __init__(self, items=()):
        self.items = []
        for x in items:
            self.add(x)

    def add(self, x):
        if not self.contains(x):
            self.items.append(x)

    def contains(self, x):
        return x in self.items

    def union(self, other):
        return IntSet(self.items + other.items)

    def intersection(self, other):
        return IntSet([x for x in self.items if other.contains(x)])''',
     'a = IntSet([1, 2, 3, 3]); b = IntSet([3, 4])\nassert sorted(a.union(b).items) == [1, 2, 3, 4] and a.intersection(b).items == [3] and len(a.items) == 3', 6),
])

code_tasks('ch11-st5', [
    ('Write a class HashTable of size m using separate chaining (a list of lists) to store key-value pairs with integer keys, h(k) = k mod m. Provide put(k, v) (updating an existing key), get(k) (returning None if absent) and load_factor().',
     '''class HashTable:
    def __init__(self, m):
        self.m = m
        self.buckets = [[] for _ in range(m)]
        self.n = 0

    def put(self, k, v):
        b = self.buckets[k % self.m]
        for pair in b:
            if pair[0] == k:
                pair[1] = v
                return
        b.append([k, v])
        self.n += 1

    def get(self, k):
        for key, val in self.buckets[k % self.m]:
            if key == k:
                return val
        return None

    def load_factor(self):
        return self.n / self.m''',
     'h = HashTable(5)\nh.put(3, "a"); h.put(8, "b"); h.put(3, "c")\nassert h.get(3) == "c" and h.get(8) == "b" and h.get(13) is None and h.load_factor() == 0.4', 6),
    ('Write a function first_repeat(words) that uses a dictionary (hash table) to return the first word that appears for a second time in the list, or None, in O(n) time. Explain in a comment why a dictionary is used.',
     '''def first_repeat(words):
    seen = {}   # hash table: O(1) average look-up, so the whole scan is O(n)
    for w in words:
        if w in seen:
            return w
        seen[w] = True
    return None''',
     'assert first_repeat(["lima", "oslo", "accra", "oslo", "lima"]) == "oslo" and first_repeat(["a", "b"]) is None', 4),
])
