"""CBSE class 12 Computer Science (083), chapters 7-9: database concepts, SQL and the Python-MySQL interface.

Every query output is computed by running the query on an sqlite3 copy of the table (kit.DB) with MySQL-style
functions installed; rows are inserted in primary-key order and queries that list rows either use ORDER BY on a
column with distinct values or follow that order, so the output matches MySQL. AVG() of an INT column is shown
with four decimal places as MySQL does. Table generators are reused by Informatics Practices (065).
"""
from __future__ import annotations

import random

from qbank import F, mcq, CITIES
from g12_computer_science_kit import ST, DB, show_table, render, uniq, NAMES, SURN, deck

S = 'cbse-g12-computer-science-ch'

DEPTS = ['SALES', 'HR', 'FINANCE', 'IT', 'ADMIN']
STREAMS = ['Science', 'Commerce', 'Humanities']
PCATS = [('Stationery', ['Pen', 'Pencil', 'Notebook', 'Eraser', 'Marker']), ('Grocery', ['Rice', 'Sugar', 'Tea', 'Atta', 'Dal']),
         ('Electronics', ['Mouse', 'Keyboard', 'Speaker', 'Charger', 'Pendrive'])]


def emp_table(r, n=None, nulls=True):
    n = n or r.randint(6, 8)
    nm = r.sample(NAMES, n)
    ids = sorted(r.sample(range(101, 160), n))
    sal = r.sample(range(25, 99), n)
    depts = r.sample(DEPTS, 3)
    rows = []
    for i in range(n):
        d = depts[i % 3] if i < 3 else r.choice(depts)
        city = r.choice(CITIES[:6])
        doj = f'{r.randint(2012, 2024)}-{r.randint(1, 12):02d}-{r.randint(1, 28):02d}'
        bonus = r.choice([None, r.randint(2, 9) * 500]) if nulls else r.randint(2, 9) * 500
        rows.append([ids[i], nm[i], d, sal[i] * 1000, city, doj, bonus])
    if nulls and all(x[6] is not None for x in rows):
        rows[r.randrange(n)][6] = None
    return 'EMPLOYEE', ['EmpNo', 'Name', 'Dept', 'Salary', 'City', 'DOJ', 'Bonus'], rows


def stu_table(r, n=None, nulls=True):
    n = n or r.randint(6, 8)
    nm = r.sample(NAMES, n)
    ids = sorted(r.sample(range(1, 40), n))
    marks = r.sample(range(35, 99), n)
    rows = []
    for i in range(n):
        st = STREAMS[i % 3] if i < 3 else r.choice(STREAMS)
        fee = r.choice([2500, 3000, 3500, 4000, 4500])
        rows.append([ids[i], nm[i], r.choice(['XI', 'XII']), st, marks[i], r.choice(CITIES[:6]), fee])
    if nulls:
        rows[r.randrange(n)][4] = None
    return 'STUDENT', ['RollNo', 'Name', 'Class', 'Stream', 'Marks', 'City', 'Fee'], rows


def prod_table(r, n=None, nulls=False):
    n = n or r.randint(6, 8)
    items = [(c, it) for c, its in PCATS for it in its]
    pick = r.sample(items, n)
    for c, _ in PCATS:
        if not any(p[0] == c for p in pick):
            pick[r.randrange(n)] = (c, r.choice(dict(PCATS)[c]))
    if len({p[1] for p in pick}) < n:
        raise ValueError('dup item')
    codes = sorted(r.sample(range(1, 99), n))
    price = r.sample(range(10, 999), n)
    rows = [[f'P{codes[i]:02d}', pick[i][1], pick[i][0], price[i], r.randint(5, 150)] for i in range(n)]
    return 'PRODUCT', ['PCode', 'PName', 'Category', 'Price', 'Qty'], rows


TABLES = [emp_table, stu_table, prod_table]
# column roles per table: (num col, text group col, name col, city-like col or None)
ROLES = {'EMPLOYEE': ('Salary', 'Dept', 'Name', 'City', 'Bonus'), 'STUDENT': ('Marks', 'Stream', 'Name', 'City', 'Marks'),
         'PRODUCT': ('Price', 'Category', 'PName', None, None)}


def any_table(r, nulls=True):
    for _ in range(20):
        try:
            return r.choice(TABLES)(r, nulls=nulls)
        except ValueError:
            continue
    raise ValueError('table')


# ---------------------------------------------------------------- output-prediction queries

def query_pool(r, tname, cols, rows):
    numc, grp, namec, city, nullc = ROLES[tname]
    ni = cols.index(numc)
    vals = sorted(x[ni] for x in rows if x[ni] is not None)
    k = vals[r.randint(1, len(vals) - 3)]
    lo, hi = vals[1], vals[-2]
    gv = r.choice(sorted({x[cols.index(grp)] for x in rows}))
    letter = r.choice(sorted({x[cols.index(namec)][0] for x in rows}))
    second = r.choice(sorted({x[cols.index(namec)][1] for x in rows}))
    qs = [
        f'SELECT {namec}, {numc} FROM {tname} WHERE {numc} > {k} ORDER BY {numc} DESC;',
        f'SELECT COUNT(*), MAX({numc}) FROM {tname} WHERE {grp} = \'{gv}\';',
        f'SELECT {grp}, COUNT(*) FROM {tname} GROUP BY {grp} ORDER BY {grp};',
        f'SELECT {grp}, SUM({numc}) FROM {tname} GROUP BY {grp} HAVING COUNT(*) > 1 ORDER BY {grp};',
        f'SELECT DISTINCT {grp} FROM {tname} ORDER BY {grp} DESC;',
        f'SELECT {namec} FROM {tname} WHERE {namec} LIKE \'{letter}%\' OR {namec} LIKE \'_{second}%\' ORDER BY {namec};',
        f'SELECT {namec} FROM {tname} WHERE {numc} BETWEEN {lo} AND {k} ORDER BY {namec};',
        f'SELECT MIN({numc}), MAX({numc}), COUNT({numc}) FROM {tname};',
        f'SELECT {namec}, {numc} FROM {tname} WHERE {grp} IN (\'{gv}\') AND {numc} < {hi} ORDER BY {namec};',
    ]
    if nullc:
        qs += [f'SELECT COUNT(*), COUNT({nullc}) FROM {tname};', f'SELECT {namec} FROM {tname} WHERE {nullc} IS NULL;']
    if city:
        c = r.choice(sorted({x[cols.index(city)] for x in rows}))
        qs += [f'SELECT {namec}, {city} FROM {tname} WHERE {city} <> \'{c}\' AND {numc} >= {k} ORDER BY {numc};']
    if tname != 'PRODUCT':
        qs += [f'SELECT AVG({numc}) FROM {tname} WHERE {grp} = \'{gv}\';']
    return qs


def sql_out(r, n_q=1, marks=None):
    tname, cols, rows = any_table(r)
    db = DB([(tname, cols, rows)])
    qs = r.sample(query_pool(r, tname, cols, rows), n_q)
    outs = [db.result(q) for q in qs]
    tbl = show_table(tname, cols, rows)
    if n_q == 1:
        q, o = qs[0], outs[0]
        if o.startswith('Empty'):
            raise ValueError('empty')
        return {'stem': f'Consider the table given below.\n{tbl}\nWrite the output of the query:\n{q}', 'answer': o,
                'key': f'{marks or 1} mark(s) for the correct output (column headings and all rows):\n{o}', 'marks': marks or 1}
    lab = ['i', 'ii', 'iii', 'iv'][:n_q]
    body = '\n'.join(f'({l}) {q}' for l, q in zip(lab, qs))
    ans = '\n'.join(f'({l})\n{o}' for l, o in zip(lab, outs))
    return {'stem': f'Consider the table given below.\n{tbl}\nWrite the output of the following queries:\n{body}', 'answer': ans,
            'key': f'{marks} marks: {marks / n_q:g} for each correct output.', 'marks': marks}


def sql_out_mcq(r):
    tname, cols, rows = any_table(r)
    db = DB([(tname, cols, rows)])
    numc, grp, namec, city, nullc = ROLES[tname]
    ni = cols.index(numc)
    vals = sorted(x[ni] for x in rows if x[ni] is not None)
    k = vals[r.randint(1, len(vals) - 3)]
    gv = r.choice(sorted({x[cols.index(grp)] for x in rows}))
    t = r.randrange(4)
    if t == 0:
        q = f'SELECT COUNT(*) FROM {tname} WHERE {numc} > {k};'
        alts = [q.replace('>', '>='), q.replace('>', '<'), f'SELECT COUNT(*) FROM {tname};']
    elif t == 1:
        q = f'SELECT MAX({numc}) - MIN({numc}) FROM {tname} WHERE {grp} = \'{gv}\';'
        alts = [f'SELECT MAX({numc}) - MIN({numc}) FROM {tname};', f'SELECT MAX({numc}) FROM {tname} WHERE {grp} = \'{gv}\';', f'SELECT MIN({numc}) FROM {tname} WHERE {grp} = \'{gv}\';']
    elif t == 2:
        q = f'SELECT COUNT(DISTINCT {grp}) FROM {tname};'
        alts = [f'SELECT COUNT({grp}) FROM {tname};', f'SELECT COUNT(*) - 1 FROM {tname};', f'SELECT COUNT(DISTINCT {grp}) + 1 FROM {tname};']
    else:
        q = f'SELECT SUM({numc}) FROM {tname} WHERE {numc} < {k};'
        alts = [q.replace('<', '<='), q.replace('<', '>'), f'SELECT SUM({numc}) FROM {tname};']
    a = db.q(q)[1][0][0]
    wrong = []
    for x in alts:
        wrong.append(str(db.q(x)[1][0][0]))
    wrong = uniq(wrong + [str(a + 1) if isinstance(a, int) else '0'], [str(a)])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'Consider the table:\n{show_table(tname, cols, rows)}\nWhat is the output of the query?\n{q}', str(a), wrong[:3], f'The query returns {a}.', r)


def null_count(r):
    tname, cols, rows = r.choice([emp_table, stu_table])(r)
    nullc = ROLES[tname][4]
    db = DB([(tname, cols, rows)])
    q = f'SELECT COUNT(*), COUNT({nullc}) FROM {tname};'
    a = db.q(q)[1][0]
    ans = f'{a[0]} and {a[1]}'
    wrong = uniq([f'{a[0]} and {a[0]}', f'{a[1]} and {a[1]}', f'{a[1]} and {a[0]}', f'{a[0]} and {a[1] - 1}'], [ans])
    return mcq(f'Consider the table:\n{show_table(tname, cols, rows)}\nWhat does the query return?\n{q}', ans, wrong[:3],
               f'COUNT(*) counts all rows ({a[0]}); COUNT({nullc}) ignores NULL values ({a[1]}).', r)


# ---------------------------------------------------------------- write-the-query tasks

def tasks_for(r, tname, cols, rows):
    numc, grp, namec, city, nullc = ROLES[tname]
    ni = cols.index(numc)
    vals = sorted(x[ni] for x in rows if x[ni] is not None)
    k = vals[len(vals) // 2]
    gv = r.choice(sorted({x[cols.index(grp)] for x in rows}))
    letter = r.choice('ASKRMPN')
    T = [
        (f'Display all details of records whose {grp} is {gv}.', f"SELECT * FROM {tname} WHERE {grp} = '{gv}';"),
        (f'Display {namec} and {numc} in descending order of {numc}.', f'SELECT {namec}, {numc} FROM {tname} ORDER BY {numc} DESC;'),
        (f'Display the number of records in each {grp}.', f'SELECT {grp}, COUNT(*) FROM {tname} GROUP BY {grp};'),
        (f'Display the {namec} of records whose {namec} starts with "{letter}".', f"SELECT {namec} FROM {tname} WHERE {namec} LIKE '{letter}%';"),
        (f'Display the maximum and minimum {numc}.', f'SELECT MAX({numc}), MIN({numc}) FROM {tname};'),
        (f'Display {namec} of records with {numc} between {vals[1]} and {k}.', f'SELECT {namec} FROM {tname} WHERE {numc} BETWEEN {vals[1]} AND {k};'),
        (f'Display each {grp} and the average {numc}, only for groups having more than one record.', f'SELECT {grp}, AVG({numc}) FROM {tname} GROUP BY {grp} HAVING COUNT(*) > 1;'),
        (f'Increase the {numc} of all records of {grp} {gv} by 10%.', f"UPDATE {tname} SET {numc} = {numc} * 1.10 WHERE {grp} = '{gv}';"),
        (f'Delete the records whose {numc} is less than {vals[0] + 1}.', f'DELETE FROM {tname} WHERE {numc} < {vals[0] + 1};'),
        (f'Display the distinct values of {grp}.', f'SELECT DISTINCT {grp} FROM {tname};'),
    ]
    if nullc:
        T.append((f'Display {namec} of records in which {nullc} is not given (NULL).', f'SELECT {namec} FROM {tname} WHERE {nullc} IS NULL;'))
    if city:
        T.append((f'Display {namec} of records from {city} other than {r.choice(CITIES[:6])}, in alphabetical order of {namec}.',
                  f"SELECT {namec} FROM {tname} WHERE {city} <> '{r.choice(CITIES[:6])}' ORDER BY {namec};"))
    if tname == 'EMPLOYEE':
        T.append(('Add a column Phone of type CHAR(10) to the table.', 'ALTER TABLE EMPLOYEE ADD Phone CHAR(10);'))
    return T


def sql_write(r, n=4, marks=4):
    tname, cols, rows = any_table(r)
    db = DB([(tname, cols, rows)])
    T = r.sample(tasks_for(r, tname, cols, rows), n)
    for _, q in T:
        if not q.startswith('ALTER'):
            db.q(q) if q.startswith('SELECT') else db.con.execute(q)
    lab = ['i', 'ii', 'iii', 'iv', 'v'][:n]
    return {'stem': f'Consider the table {tname} given below.\n{show_table(tname, cols, rows)}\nWrite SQL queries for the following:\n' +
                    '\n'.join(f'({l}) {t}' for l, (t, _) in zip(lab, T)),
            'answer': '\n'.join(f'({l}) {q}' for l, (_, q) in zip(lab, T)),
            'key': f'{marks} marks: {marks / n:g} for each correct query (½ for correct clause, ½ for correct condition).', 'marks': marks}


def sql_write1(r):
    tname, cols, rows = any_table(r)
    t, q = r.choice(tasks_for(r, tname, cols, rows))
    db = DB([(tname, cols, rows)])
    if q.startswith('SELECT'):
        db.q(q)
    return {'stem': f'Table {tname} has the columns {", ".join(cols)}. Write an SQL query to: {t[0].lower() + t[1:]}', 'answer': q,
            'key': f'1 mark: {q}', 'marks': 1}


# ---------------------------------------------------------------- joins

def two_tables(r):
    depts = r.sample(DEPTS, 4)
    dids = sorted(r.sample(range(10, 60), 4))
    loc = r.sample(CITIES, 4)
    dept = [[dids[i], depts[i], loc[i]] for i in range(4)]
    n = r.randint(4, 6)
    nm = r.sample(NAMES, n)
    ids = sorted(r.sample(range(1, 30), n))
    used = r.sample(dids, 3)
    emp = [[ids[i], nm[i], r.choice(used), r.randint(20, 90) * 1000] for i in range(n)]
    return ('DEPT', ['DeptId', 'DName', 'Location'], dept), ('EMP', ['EId', 'EName', 'DeptId', 'Salary'], emp)


def join_out(r, marks=2):
    (t1, c1, r1), (t2, c2, r2) = two_tables(r)
    db = DB([(t1, c1, r1), (t2, c2, r2)])
    k = sorted(x[3] for x in r2)[1]
    t = r.randrange(3)
    if t == 0:
        q = f'SELECT EName, DName FROM EMP, DEPT WHERE EMP.DeptId = DEPT.DeptId AND Salary > {k} ORDER BY EName;'
    elif t == 1:
        q = f'SELECT DName, COUNT(*) FROM EMP, DEPT WHERE EMP.DeptId = DEPT.DeptId GROUP BY DName ORDER BY DName;'
    else:
        q = f'SELECT EName, Location FROM EMP NATURAL JOIN DEPT WHERE Salary <= {k * 2} ORDER BY EName;'
    o = db.result(q)
    if o.startswith('Empty'):
        raise ValueError('empty')
    return {'stem': f'Consider the tables:\n{show_table(t1, c1, r1)}\n{show_table(t2, c2, r2)}\nWrite the output of:\n{q}', 'answer': o,
            'key': f'{marks} marks for the correct output:\n{o}', 'marks': marks}


def cartesian(r):
    a, b = r.randint(3, 8), r.randint(2, 6)
    da, db_ = r.randint(2, 6), r.randint(2, 5)
    t1, t2 = r.sample(['STUDENT', 'TEACHER', 'CLUB', 'SUBJECT', 'BOOK', 'ISSUE', 'CUSTOMER', 'ORDERS', 'EMP', 'DEPT'], 2)
    t = r.randrange(2)
    if t == 0:
        ans = f'Degree {da + db_}, cardinality {a * b}'
        return mcq(f'Table {t1} has {da} columns and {a} rows; table {t2} has {db_} columns and {b} rows. What are the degree and cardinality of their Cartesian product?',
                   ans, [f'Degree {da * db_}, cardinality {a + b}', f'Degree {da + db_}, cardinality {a + b}', f'Degree {da * db_}, cardinality {a * b}'],
                   'Degree adds (columns), cardinality multiplies (rows).', r)
    ans = f'Degree {da + db_ - 1}, at most {a} rows'
    return {'stem': f'{t1}({da} columns, {a} rows) and {t2}({db_} columns, {b} rows) share exactly one common column, which is the primary key of {t2} and a foreign key in {t1}. '
                    f'What is the degree of their natural join, and at most how many rows can it have?',
            'answer': ans, 'key': f'Natural join shows the common column once: {da} + {db_} − 1 = {da + db_ - 1}; each {t1} row matches at most one {t2} row, so at most {a} rows.',
            'distractors': [f'Degree {da + db_}, at most {a * b} rows', f'Degree {da + db_ - 1}, at most {a * b} rows', f'Degree {da * db_}, at most {a} rows'], 'marks': 2}


def join_write(r):
    (t1, c1, r1), (t2, c2, r2) = two_tables(r)
    loc = r.choice([x[2] for x in r1])
    T = [('Display EName and DName of all employees.', 'SELECT EName, DName FROM EMP, DEPT WHERE EMP.DeptId = DEPT.DeptId;'),
         (f'Display the names of employees who work in {loc}.', f"SELECT EName FROM EMP, DEPT WHERE EMP.DeptId = DEPT.DeptId AND Location = '{loc}';"),
         ('Display DName and the total salary of each department.', 'SELECT DName, SUM(Salary) FROM EMP, DEPT WHERE EMP.DeptId = DEPT.DeptId GROUP BY DName;'),
         ('Display the Cartesian product of the two tables.', 'SELECT * FROM EMP, DEPT;'),
         ('Display EName and Location using a natural join.', 'SELECT EName, Location FROM EMP NATURAL JOIN DEPT;')]
    pick = r.sample(T, 3)
    db = DB([(t1, c1, r1), (t2, c2, r2)])
    for _, q in pick:
        db.q(q)
    return {'stem': f'Consider the tables:\n{show_table(t1, c1, r1)}\n{show_table(t2, c2, r2)}\nWrite SQL queries to:\n' + '\n'.join(f'({l}) {t}' for l, (t, _) in zip('i ii iii'.split(), pick)),
            'answer': '\n'.join(f'({l}) {q}' for l, (_, q) in zip('i ii iii'.split(), pick)), 'key': '3 marks: 1 for each query with a correct join condition.', 'marks': 3}


# ---------------------------------------------------------------- ch07 relational model
def degree_card(r):
    tname, cols, rows = any_table(r, nulls=False)
    t = r.randrange(3)
    tbl = show_table(tname, cols, rows)
    d, c = len(cols), len(rows)
    if t == 0:
        ans = f'Degree {d}, cardinality {c}'
        return mcq(f'{tbl}\nWhat are the degree and cardinality of the table {tname}?', ans,
                   [f'Degree {c}, cardinality {d}', f'Degree {d}, cardinality {c + 1}', f'Degree {d - 1}, cardinality {c}'], 'Degree = number of attributes (columns); cardinality = number of tuples (rows).', r)
    a, dl, ac = r.randint(1, 4), r.randint(1, 2), r.randint(1, 2)
    ans = f'Degree {d + ac}, cardinality {c + a - dl}'
    return mcq(f'{tbl}\nIn the table {tname}, {a} new row{"s" if a > 1 else ""} {"are" if a > 1 else "is"} inserted, {dl} row{"s" if dl > 1 else ""} {"are" if dl > 1 else "is"} deleted and {ac} new column{"s are" if ac > 1 else " is"} added. What are the new degree and cardinality?',
               ans, uniq([f'Degree {d + ac}, cardinality {c + a}', f'Degree {d}, cardinality {c + a - dl}', f'Degree {c + a - dl}, cardinality {d + ac}', f'Degree {d + ac + a}, cardinality {c - dl}'], [ans])[:3],
               f'Columns: {d} + {ac} = {d + ac}; rows: {c} + {a} − {dl} = {c + a - dl}.', r)


def key_table(r):
    n = r.randint(5, 7)
    nm = r.sample(NAMES, n - 1)
    nm.append(nm[0])
    r.shuffle(nm)
    adm = sorted(r.sample(range(1001, 1999), n))
    email = [f'{x.lower()}{a % 100}@mail.in' for x, a in zip(nm, adm)]
    cls = [r.choice(['XI-A', 'XII-A', 'XII-B']) for _ in range(n)]
    city = [r.choice(CITIES[:3]) for _ in range(n)]
    rows = [[adm[i], nm[i], cls[i], email[i], city[i]] for i in range(n)]
    return 'MEMBER', ['AdmNo', 'Name', 'Class', 'Email', 'City'], rows


def keys_q(r):
    tname, cols, rows = key_table(r)
    tbl = show_table(tname, cols, rows)
    t = r.randrange(3)
    if t == 0:
        return mcq(f'{tbl}\nWhich columns of {tname} can be candidate keys?', 'AdmNo and Email', ['Name and Email', 'Class and City', 'AdmNo and Name'],
                   'AdmNo and Email are unique for every member; Name repeats and Class/City repeat.', r)
    if t == 1:
        return mcq(f'{tbl}\nIf AdmNo is chosen as the primary key of {tname}, what is the alternate key?', 'Email', ['Name', 'Class', 'City'],
                   'The candidate keys are AdmNo and Email; the one not chosen (Email) is the alternate key.', r)
    return mcq(f'{tbl}\nWhy can Name not be the primary key of {tname}?', 'Two members have the same name, so it does not identify a row uniquely',
               ['Name is a text column', 'Name can never be NULL', 'Name is not the first column'], 'A primary key must be unique (and not NULL) for every row.', r)


def fk_q(r):
    (t1, c1, r1), (t2, c2, r2) = two_tables(r)
    return {'stem': f'Consider the tables:\n{show_table(t1, c1, r1)}\n{show_table(t2, c2, r2)}\n(i) Identify the primary key of each table. (ii) Identify the foreign key and the table it refers to.',
            'answer': '(i) DEPT: DeptId; EMP: EId (ii) DeptId in EMP is a foreign key referring to DeptId of DEPT.', 'key': '1 mark for (i), 1 mark for (ii).', 'marks': 2,
            'distractors': ['EId in DEPT', 'Salary in EMP', 'DName in EMP']}


def db_case(r):
    who = r.choice(NAMES)
    tname, cols, rows = key_table(r)
    return {'stem': (f'{who} maintains the following table for the school library club:\n{show_table(tname, cols, rows)}\n'
                     f'(i) What is the degree and cardinality of the table? (1)\n(ii) Name the candidate keys. (1)\n'
                     f'(iii) If AdmNo is the primary key, name the alternate key. (1)\n(iv) Which column(s) cannot be a key and why? (1)'),
            'answer': f'(i) Degree {len(cols)}, cardinality {len(rows)} (ii) AdmNo, Email (iii) Email (iv) Name, Class and City – their values repeat.',
            'key': '1 mark each.', 'marks': 4}


# ---------------------------------------------------------------- ch08 st1/st2 DDL
CONSTR = [('ensure that a column never stores a missing value', 'NOT NULL'), ('ensure that no two rows have the same value in a column (NULLs allowed)', 'UNIQUE'),
          ('identify each row uniquely and disallow NULL', 'PRIMARY KEY'), ('give a column a value automatically when none is supplied', 'DEFAULT'),
          ('make a column refer to the primary key of another table', 'FOREIGN KEY')]
DTYPE = [('store a 6-digit PIN code that is used only as text', 'CHAR(6)'), ('store names of different lengths up to 30 characters', 'VARCHAR(30)'),
         ('store the date of joining', 'DATE'), ('store the number of students in a class', 'INT'), ('store a price such as 249.50', 'FLOAT')]


def constr_pick(r):
    d, c = r.choice(CONSTR)
    return mcq(f'Which constraint is used to {d}?', c, [x for _, x in CONSTR if x != c][:3] if r.random() < 0.5 else r.sample([x for _, x in CONSTR if x != c], 3), f'{c}.', r)


def dtype_pick(r):
    d, c = r.choice(DTYPE)
    return mcq(f'Which MySQL data type is most suitable to {d}?', c, r.sample([x for _, x in DTYPE if x != c], 3), f'{c}.', r)


def ddl_write(r):
    t = r.choice([('SHOP', [('ItemNo', 'INT', 'PRIMARY KEY'), ('IName', 'VARCHAR(25)', 'NOT NULL'), ('Price', 'FLOAT', ''), ('MfgDate', 'DATE', '')]),
                  ('PATIENT', [('PID', 'CHAR(5)', 'PRIMARY KEY'), ('PName', 'VARCHAR(30)', 'NOT NULL'), ('Age', 'INT', ''), ('AdmitDate', 'DATE', '')]),
                  ('TRAIN', [('TNo', 'INT', 'PRIMARY KEY'), ('TName', 'VARCHAR(40)', 'NOT NULL'), ('Source', 'VARCHAR(20)', ''), ('Fare', 'FLOAT', '')]),
                  ('MEMBER', [('MId', 'INT', 'PRIMARY KEY'), ('MName', 'VARCHAR(30)', 'NOT NULL'), ('Email', 'VARCHAR(40)', 'UNIQUE'), ('JoinDate', 'DATE', '')])])
    name, cols = t
    newc = r.choice(['Phone CHAR(10)', 'City VARCHAR(20)', 'Remarks VARCHAR(50)'])
    spec = '; '.join(f'{c} {d}' + (f' ({k})' if k else '') for c, d, k in cols)
    ans = (f'(i) CREATE TABLE {name} (' + ', '.join(f'{c} {d}' + (f' {k}' if k else '') for c, d, k in cols) + ');\n'
           f'(ii) ALTER TABLE {name} ADD {newc};\n(iii) ALTER TABLE {name} DROP {cols[2][0]};')
    return {'stem': f'Write SQL commands to: (i) create the table {name} with the columns {spec}; (ii) add a column {newc}; (iii) remove the column {cols[2][0]}.',
            'answer': ans, 'key': '3 marks: 1 for each correct command.', 'marks': 3}


DDL_DML = [('CREATE TABLE', 'DDL'), ('ALTER TABLE', 'DDL'), ('DROP TABLE', 'DDL'), ('CREATE DATABASE', 'DDL'),
           ('INSERT INTO', 'DML'), ('UPDATE', 'DML'), ('DELETE FROM', 'DML'), ('SELECT', 'DML (query)')]


def ddl_dml(r):
    c, k = r.choice(DDL_DML)
    if k == 'DDL':
        wrong = r.sample([x for x, y in DDL_DML if y != 'DDL'], 3)
        return mcq('Which of the following is a DDL command?', c, wrong, f'{c} changes the structure (schema), so it is DDL.', r)
    wrong = r.sample([x for x, y in DDL_DML if y == 'DDL'], 3)
    return mcq('Which of the following is a DML command?', c, wrong, f'{c} works on the data (rows), so it is DML.', r)


def delete_vs_drop(r):
    tname, cols, rows = any_table(r, nulls=False)
    numc = ROLES[tname][0]
    vals = sorted(x[cols.index(numc)] for x in rows)
    k = vals[r.randint(1, len(vals) - 2)]
    db = DB([(tname, cols, rows)])
    t = r.randrange(2)
    if t == 0:
        db.con.execute(f'DELETE FROM {tname} WHERE {numc} < {k}')
        n = db.q(f'SELECT COUNT(*) FROM {tname}')[1][0][0]
        return mcq(f'{show_table(tname, cols, rows)}\nAfter the command DELETE FROM {tname} WHERE {numc} < {k}; what will SELECT COUNT(*) FROM {tname}; return?', str(n),
                   uniq([str(len(rows)), str(len(rows) - n), str(n - 1), '0'], [str(n)])[:3], f'{len(rows) - n} row(s) with {numc} below {k} are deleted; {n} remain.', r)
    cur = db.con.execute(f'UPDATE {tname} SET {numc} = {numc} + 10 WHERE {numc} >= {k}')
    n = cur.rowcount
    return mcq(f'{show_table(tname, cols, rows)}\nHow many rows are changed by UPDATE {tname} SET {numc} = {numc} + 10 WHERE {numc} >= {k};?', str(n),
               uniq([str(len(rows)), str(len(rows) - n), str(n - 1), str(n + 1)], [str(n)])[:3], f'{n} rows have {numc} ≥ {k}.', r)


# ---------------------------------------------------------------- ch09 Python-MySQL
def fetch_out(r):
    tname, cols, rows = any_table(r, nulls=False)
    numc = ROLES[tname][0]
    namec = ROLES[tname][2]
    db = DB([(tname, cols, rows)])
    vals = sorted(x[cols.index(numc)] for x in rows)
    k = vals[r.randint(0, 2)]
    q = f'SELECT {namec}, {numc} FROM {tname} WHERE {numc} > {k} ORDER BY {numc}'
    cur = db.con.execute(q)
    t = r.randrange(3)
    if t == 0:
        a = cur.fetchone()
        b = cur.fetchmany(2)
        out = f'{a}\n{b}'
        code = f'cur.execute("{q}")\nr1 = cur.fetchone()\nr2 = cur.fetchmany(2)\nprint(r1)\nprint(r2)'
    elif t == 1:
        allr = cur.fetchall()
        out = f'{len(allr)}\n{allr[-1]}'
        code = f'cur.execute("{q}")\ndata = cur.fetchall()\nprint(len(data))\nprint(data[-1])'
    else:
        cur.fetchone()
        b = cur.fetchone()
        out = f'{b[0]}'
        code = f'cur.execute("{q}")\ncur.fetchone()\nrow = cur.fetchone()\nprint(row[0])'
    return {'stem': (f'The table {tname} in MySQL database SCHOOL contains:\n{show_table(tname, cols, rows)}\nA connection con and a cursor cur = con.cursor() have been created. '
                     f'Write the output of:\n{code}'), 'answer': out, 'key': f'2 marks: fetchone() returns one row as a tuple; fetchmany(n) and fetchall() return a list of tuples. Output:\n{out}', 'marks': 2}


def fmt_query(r):
    tname, cols, rows = any_table(r, nulls=False)
    numc = ROLES[tname][0]
    grp = ROLES[tname][1]
    gv = rows[0][cols.index(grp)]
    k = r.randint(10, 90) * 100
    t = r.randrange(3)
    if t == 0:
        code = f'x = {k}\ng = "{gv}"\nq = "SELECT * FROM {tname} WHERE {numc} > {{}} AND {grp} = \'{{}}\'".format(x, g)\nprint(q)'
    elif t == 1:
        code = f'x = {k}\nq = "SELECT * FROM {tname} WHERE {numc} > %s" % (x,)\nprint(q)'
    else:
        code = f'g = "{gv}"\nq = "DELETE FROM {tname} WHERE {grp} = \'{{}}\'".format(g)\nprint(q)'
    from g12_computer_science_kit import run
    ans = run(code)
    wrong = [ans.replace("'", ''), ans.replace(str(k), 'x') if str(k) in ans else ans.replace(gv, 'g'), ans.replace(' = ', ' == ') if ' = ' in ans else ans + ';']
    return mcq(f'What is printed by the following code?\n{code}', ans, uniq(wrong, [ans])[:3], 'format() and % substitute the values into the query string.', r)


CONN_BLANKS = [
    ('import mysql.connector as sqltor', 'import the connector module'), ('con = sqltor.connect(host="localhost", user="root", passwd="tiger", database="SCHOOL")', 'connect to the database SCHOOL'),
    ('cur = con.cursor()', 'create a cursor object'), ('cur.execute(query)', 'run the query'), ('con.commit()', 'make the changes permanent'),
    ('data = cur.fetchall()', 'fetch all the rows of the result'), ('con.close()', 'close the connection'),
]


def conn_case(r, marks=4):
    who = r.choice(NAMES)
    tname, cols, rows = any_table(r, nulls=False)
    numc = ROLES[tname][0]
    t = r.randrange(2)
    if t == 0:
        steps = [CONN_BLANKS[0], CONN_BLANKS[1], CONN_BLANKS[2], ('cur.execute(q)', 'execute the INSERT query'), CONN_BLANKS[4]]
        code = ('_____ # Statement 1: import the connector as sqltor\ncon = _____ # Statement 2: connect to database SCHOOL (user root, password tiger)\ncur = _____ # Statement 3\n'
                f'q = "INSERT INTO {tname} VALUES ({{}}, \'{{}}\', ...)".format(...)\n_____ # Statement 4: execute q\n_____ # Statement 5: save the changes')
        pick = [0, 1, 3, 4]
        lab = ['1', '2', '4', '5']
    else:
        steps = [CONN_BLANKS[0], CONN_BLANKS[1], CONN_BLANKS[2], ('cur.execute(f"SELECT * FROM %s WHERE %s > %%s" % ("' + tname + '", "' + numc + '"), (50,))', ''), CONN_BLANKS[5]]
        code = ('import mysql.connector as sqltor\ncon = sqltor.connect(host="localhost", user="root", passwd="tiger", database="SCHOOL")\ncur = _____ # Statement 1\n'
                f'cur.execute("SELECT * FROM {tname} WHERE {numc} > %s", (50,))\ndata = _____ # Statement 2: fetch all rows\nfor row in data:\n    print(row)\n'
                'print(_____) # Statement 3: number of rows fetched\n_____ # Statement 4: close the connection')
        steps = [CONN_BLANKS[2], CONN_BLANKS[5], ('cur.rowcount', ''), CONN_BLANKS[6]]
        pick = [0, 1, 2, 3]
        lab = ['1', '2', '3', '4']
    ans = ' '.join(f'Statement {l}: {steps[i][0]}' for l, i in zip(lab, pick))
    return {'stem': f'{who} is writing a Python program to work with the MySQL table {tname}. Complete the missing statements:\n{code}\nWrite Statement ' + ', '.join(lab) + '.',
            'answer': ans, 'key': f'{marks} marks: 1 for each statement.', 'marks': marks}


def db_program(r, marks=5):
    tname, cols, rows = any_table(r, nulls=False)
    numc, grp, namec = ROLES[tname][:3]
    t = r.randrange(3)
    if t == 0:
        stem = (f'Write a Python program that connects to the MySQL database SCHOOL (user "root", password "tiger") and inserts a record into the table {tname}({", ".join(cols)}) '
                'with values entered by the user. Commit the change and display "Record added". Use a parameterised query with %s.')
        ans = ('import mysql.connector as sqltor\ncon = sqltor.connect(host="localhost", user="root", passwd="tiger", database="SCHOOL")\ncur = con.cursor()\n'
               + '\n'.join(f'v{i} = input("{c}: ")' for i, c in enumerate(cols)) +
               f'\nq = "INSERT INTO {tname} VALUES (' + ', '.join(['%s'] * len(cols)) + ')"\ncur.execute(q, (' + ', '.join(f'v{i}' for i in range(len(cols))) + '))\ncon.commit()\nprint("Record added")\ncon.close()')
    elif t == 1:
        stem = (f'Write a Python function SHOW_{grp.upper()}(g) that connects to the MySQL database SCHOOL and displays all records of {tname} whose {grp} is g, '
                f'followed by the number of such records.')
        ans = (f'import mysql.connector as sqltor\ndef SHOW_{grp.upper()}(g):\n    con = sqltor.connect(host="localhost", user="root", passwd="tiger", database="SCHOOL")\n    cur = con.cursor()\n'
               f'    cur.execute("SELECT * FROM {tname} WHERE {grp} = %s", (g,))\n    rows = cur.fetchall()\n    for row in rows:\n        print(row)\n    print("Records:", cur.rowcount)\n    con.close()')
    else:
        stem = (f'Write a menu-driven Python program for the MySQL table {tname} with options 1. Display all records 2. Increase {numc} by a given percentage for a given {grp} '
                '3. Exit. Use parameterised queries and commit after changes.')
        ans = ('import mysql.connector as sqltor\ncon = sqltor.connect(host="localhost", user="root", passwd="tiger", database="SCHOOL")\ncur = con.cursor()\nwhile True:\n'
               '    ch = int(input("1.Display 2.Increase 3.Exit: "))\n    if ch == 1:\n'
               f'        cur.execute("SELECT * FROM {tname}")\n        for row in cur.fetchall():\n            print(row)\n    elif ch == 2:\n        p = float(input("Percent: "))\n'
               f'        g = input("{grp}: ")\n        cur.execute("UPDATE {tname} SET {numc} = {numc} + {numc} * %s / 100 WHERE {grp} = %s", (p, g))\n        con.commit()\n'
               '        print(cur.rowcount, "rows updated")\n    else:\n        break\ncon.close()')
    compile(ans, 'x', 'exec')
    return {'stem': stem, 'answer': ans, 'key': f'{marks} marks: connect and cursor 1, query with parameters {2 if marks == 5 else 1}, execute/fetch or commit 1, output/loop 1.', 'marks': marks}


CH07 = [ST(S + '07-st1', 'need for a database', """
T: database | an organised collection of logically related data stored so that it can be accessed, managed and updated easily
T: DBMS | Database Management System, software used to create, store, manage and retrieve data in a database, such as MySQL
T: data redundancy | the unnecessary repetition of the same data in more than one place
T: data inconsistency | a situation in which different copies of the same data do not match
T: data isolation | the situation when data is scattered in different files of different formats, making it hard to retrieve together
T: data dependence | the situation in which the structure of a data file is tied to the programs that use it, so a change in one requires changes in the other
Q: Which of these is a DBMS? | MySQL | Python | HTML | Linux
Q: Storing a student's address in both the fees file and the library file is an example of: | data redundancy | data security | data independence | normalisation
Q: When a student's phone number is updated in one file but not in another, it leads to: | data inconsistency | data isolation | data integrity | data abstraction
Q: Which is NOT a limitation of the file system? | controlled data sharing | data redundancy | data inconsistency | data isolation
Q: A DBMS reduces data redundancy by: | storing data centrally and sharing it among applications | storing every record many times | keeping data in separate files for each program | avoiding keys
S+: A DBMS allows many users to share data in a controlled manner
S+: Data redundancy can lead to data inconsistency
S+: A DBMS provides security by restricting access to authorised users
S+: In a file system each application program usually keeps its own data files
S-: A file system automatically removes data redundancy | Redundancy is a problem of file systems; a DBMS reduces it
S-: Python is an example of a DBMS | MySQL, Oracle and PostgreSQL are DBMSs; Python is a programming language
S-: Data inconsistency means the same data is stored in several places | That is redundancy; inconsistency is when copies do not match
C: Data inconsistency arises in file systems | the same data kept in several files may be updated in one file and not in others
C: Retrieving data from many files of a file system is difficult | the files may have different formats and structures (data isolation)
X: C2 D2 2 | Give any two limitations of a file system that a DBMS overcomes. | Data redundancy, data inconsistency, data isolation, data dependence, difficulty in access, poor controlled sharing/security (any two, explained).
"""), ST(S + '07-st2', 'the relational data model', """
T: relation | a table in a relational database, made of rows and columns
T: attribute | a column of a relation, representing a property of the entity
T: tuple | a row of a relation, representing one record
T: domain | the set of all possible values that an attribute can take
T: degree | the number of attributes (columns) in a relation
T: cardinality | the number of tuples (rows) in a relation
Q: A row of a relation is called a: | tuple | attribute | domain | degree
Q: The number of columns in a relation is its: | degree | cardinality | domain | key
Q: The set of values from which an attribute takes its values is its: | domain | degree | tuple | relation schema
Q: A relation with 5 columns and 12 rows has cardinality: | 12 | 5 | 17 | 60
Q: In the relational model, a relation is a: | table | file of programs | single value | query
S+: In a relation, the order of tuples does not matter
S+: All values in a column of a relation belong to the same domain
S+: Each value in a relation is atomic (cannot be divided further)
S+: No two tuples of a relation can be identical
S-: Degree is the number of rows of a relation | Degree is the number of columns; cardinality is the number of rows
S-: Two tuples of a relation can be exactly the same | Each tuple of a relation is distinct
C: Adding a new record changes the cardinality but not the degree of a relation | a record is a new row; the number of columns stays the same
X: C2 D2 2 | Define degree and cardinality with an example. | Degree: number of attributes; cardinality: number of tuples. A table with 4 columns and 10 rows has degree 4 and cardinality 10.
"""), ST(S + '07-st3', 'keys in a relational database', """
T: candidate key | an attribute or set of attributes that can uniquely identify each tuple of a relation
T: primary key | the candidate key chosen by the designer to uniquely identify the tuples of a relation; it cannot be NULL
T: alternate key | a candidate key that is not chosen as the primary key
T: foreign key | an attribute of one relation that refers to the primary key of another relation, linking the two
T: composite primary key | a primary key made of two or more attributes together
Q: A candidate key not chosen as the primary key is called: | an alternate key | a foreign key | a composite key | a super domain
Q: Which key is used to link two tables? | Foreign key | Alternate key | Candidate key | Primary key of the same table
Q: A primary key column can contain: | only unique and non-NULL values | NULL values | repeated values | only text values
Q: How many primary keys can a table have? | One (possibly made of several columns) | Two | Any number | None
Q: A foreign key value must match: | a primary key value in the referenced table, or be NULL | any value in any table | an alternate key in the same table | the row number
S+: A table can have more than one candidate key
S+: A foreign key can have repeated values
S+: The primary key helps in searching and linking records
S+: A combination of columns can act as a primary key
S-: A table can have two primary keys | A table has only one primary key, though it may be composite
S-: A primary key can contain NULL values | A primary key must be unique and not NULL
S-: A foreign key must be unique in its table | A foreign key can repeat; it refers to a unique primary key elsewhere
C: Name is usually not chosen as a primary key | two people can have the same name, so it does not uniquely identify a record
C: A foreign key helps maintain referential integrity | it allows only values that exist in the primary key of the referenced table
X: C2 D3 2 | Differentiate between a primary key and a foreign key. | Primary key: uniquely identifies rows of its own table, unique and not NULL; foreign key: refers to the primary key of another table, may repeat, links tables.
""")]

CH08 = [ST(S + '08-st1', 'SQL data types and constraints', """
T: SQL | Structured Query Language, the standard language for creating, managing and querying relational databases
T: DDL | Data Definition Language, SQL commands that define or change the structure of database objects, such as CREATE, ALTER and DROP
T: DML | Data Manipulation Language, SQL commands that insert, delete, update and retrieve data, such as INSERT, UPDATE, DELETE and SELECT
T: constraint | a rule applied to a column to restrict the values it can hold, such as NOT NULL, UNIQUE, DEFAULT or PRIMARY KEY
T: CHAR(n) | a fixed-length string data type; shorter values are padded with spaces to n characters
T: VARCHAR(n) | a variable-length string data type that uses only as much space as the value needs, up to n characters
Q: Which data type is fixed-length? | CHAR | VARCHAR | TEXT of variable size | INT
Q: In MySQL, the default format of a DATE value is: | YYYY-MM-DD | DD-MM-YYYY | MM/DD/YYYY | YYYY/DD/MM
Q: Which constraint allows NULLs but not repeated values? | UNIQUE | PRIMARY KEY | NOT NULL | DEFAULT
Q: Which command is a DDL command? | ALTER | UPDATE | INSERT | SELECT
Q: Which command is a DML command? | DELETE | DROP | CREATE | ALTER
Q: SQL keywords in MySQL are: | not case-sensitive | always lower case | always upper case | case-sensitive
S+: VARCHAR saves space when values have different lengths
S+: A PRIMARY KEY constraint combines NOT NULL and UNIQUE
S+: Text and date values are written in quotes in SQL statements
S+: Each SQL statement in MySQL ends with a semicolon
S-: CHAR(10) stores "Ram" using only 3 characters of space | CHAR is fixed-length and uses all 10; VARCHAR uses only what is needed
S-: UPDATE is a DDL command | UPDATE is DML; it changes data, not structure
S-: The UNIQUE constraint does not allow NULL values | UNIQUE allows NULLs; PRIMARY KEY does not
C: CHAR is preferred for PIN codes and VARCHAR for names | PIN codes always have the same length while names vary in length
X: C2 D2 2 | Differentiate between CHAR and VARCHAR with an example. | CHAR(n) is fixed length (CHAR(10) always uses 10 characters); VARCHAR(n) is variable length (VARCHAR(10) stores "Ram" in 3 characters).
"""), ST(S + '08-st2', 'DDL commands', """
T: CREATE DATABASE | the command that creates a new database, as in CREATE DATABASE SCHOOL;
T: CREATE TABLE | the command that creates a new table with its columns, data types and constraints
T: ALTER TABLE | the command that changes the structure of an existing table, such as adding or removing a column or a primary key
T: DROP TABLE | the command that removes a table together with its structure and data
T: USE | the command that selects a database to work with, as in USE SCHOOL;
T: DESCRIBE | the command that shows the structure of a table, as in DESC STUDENT;
Q: Which command shows the structure of a table? | DESC STUDENT; | SHOW STUDENT; | SELECT STUDENT; | DISPLAY STUDENT;
Q: Which command adds a column Phone to STUDENT? | ALTER TABLE STUDENT ADD Phone CHAR(10); | UPDATE STUDENT ADD Phone CHAR(10); | INSERT INTO STUDENT Phone; | ALTER STUDENT INSERT Phone;
Q: Which command removes the primary key from STUDENT? | ALTER TABLE STUDENT DROP PRIMARY KEY; | DROP PRIMARY KEY STUDENT; | DELETE PRIMARY KEY FROM STUDENT; | ALTER STUDENT REMOVE KEY;
Q: Which command lists all tables of the current database? | SHOW TABLES; | DESC TABLES; | SELECT TABLES; | LIST TABLES;
Q: Which command deletes a table along with its structure? | DROP TABLE | DELETE FROM | ALTER TABLE ... DROP | TRUNCATE ROW
S+: ALTER TABLE ... DROP column_name removes a column from a table
S+: DROP TABLE removes both the data and the structure of a table
S+: A primary key can be added to an existing table using ALTER TABLE ... ADD PRIMARY KEY
S-: DELETE FROM STUDENT; removes the table structure | DELETE removes rows only; DROP TABLE removes the structure
S-: ALTER TABLE is used to change data values | ALTER changes structure; UPDATE changes data
C: After DELETE FROM STUDENT; the table still exists | DELETE removes only the rows, not the structure
X: C2 D3 2 | Differentiate between DELETE and DROP commands. | DELETE (DML) removes rows, possibly with WHERE, structure remains; DROP (DDL) removes the whole table including its structure.
"""), ST(S + '08-st3', 'SQL queries', """
T: SELECT | the SQL command used to retrieve data from one or more tables
T: WHERE clause | the clause that selects only the rows satisfying a condition
T: DISTINCT | the keyword that removes duplicate values from the result of a query
T: ORDER BY | the clause that sorts the result in ascending (ASC, default) or descending (DESC) order
T: LIKE | the operator for pattern matching, with % for any number of characters and _ for exactly one character
T: BETWEEN | the operator that selects values within a range, including both end values
T: IS NULL | the condition that tests whether a column has no value
Q: Which wildcard matches exactly one character in LIKE? | _ (underscore) | % | * | ?
Q: The default sort order of ORDER BY is: | ascending | descending | random | insertion order only
Q: Which condition finds rows where Phone has no value? | Phone IS NULL | Phone = NULL | Phone == NULL | Phone = ''
Q: BETWEEN 10 AND 20 includes: | both 10 and 20 | neither 10 nor 20 | only 10 | only 20
Q: Which pattern finds names ending with "a"? | LIKE '%a' | LIKE 'a%' | LIKE '_a' | LIKE '%a%'
Q: Which keyword removes duplicates from the output? | DISTINCT | UNIQUE | GROUP | ONLY
S+: The IN operator checks whether a value matches any value in a list
S+: A condition comparing a column with NULL using = is never true; IS NULL must be used
S+: ORDER BY can sort on more than one column
S+: UPDATE without a WHERE clause changes every row of the table
S-: LIKE 'A_' matches any name starting with A | 'A_' matches only two-character values starting with A; 'A%' matches any length
S-: BETWEEN excludes its end values | BETWEEN includes both end values
S-: DELETE FROM STUDENT WHERE Marks = NULL; deletes rows with no marks | = NULL is never true; IS NULL must be used
C: WHERE Marks = NULL returns no rows | NULL means an unknown value, so comparisons with = give unknown, not true
C: SELECT DISTINCT City FROM STUDENT; may return fewer rows than the table has | duplicate city values appear only once
X: C2 D2 2 | Differentiate between the % and _ wildcards with an example. | % matches any number of characters (LIKE 'S%' – names starting with S); _ matches exactly one character (LIKE '_a%' – second letter a).
"""), ST(S + '08-st4', 'aggregate functions and grouping', """
T: aggregate function | a function that works on a set of rows and returns a single value, such as SUM, AVG, MAX, MIN or COUNT
T: GROUP BY | the clause that groups rows having the same value in a column so that aggregate functions can be applied to each group
T: HAVING | the clause that applies a condition to groups formed by GROUP BY
T: COUNT(*) | the function that counts all rows, including rows with NULL values
Q: Which function ignores NULL values when counting? | COUNT(column) | COUNT(*) | COUNT(ALL *) | SUM(*)
Q: Conditions on groups are written using: | HAVING | WHERE | ORDER BY | DISTINCT
Q: Which clause cannot use an aggregate function in its condition? | WHERE | HAVING | SELECT list | ORDER BY
Q: AVG() can be applied to: | numeric columns | only text columns | only dates | only primary keys
Q: The output of SELECT MAX(Marks) FROM STUDENT; has: | one row | as many rows as the table | no rows | two rows
S+: Aggregate functions other than COUNT(*) ignore NULL values
S+: WHERE filters rows before grouping while HAVING filters groups after grouping
S+: GROUP BY with COUNT(*) gives the number of rows in each group
S-: HAVING is used to filter individual rows before grouping | WHERE filters rows; HAVING filters groups
S-: COUNT(Marks) counts rows with NULL marks too | COUNT(column) ignores NULLs; COUNT(*) counts all rows
S-: An aggregate function can be used in the WHERE clause | Aggregates are used in SELECT and HAVING, not in WHERE
C: SELECT Stream, COUNT(*) FROM STUDENT GROUP BY Stream; gives one row per stream | GROUP BY forms one group for each distinct stream
C: COUNT(*) and COUNT(Marks) can give different results | COUNT(Marks) skips rows in which Marks is NULL
X: C2 D3 2 | Differentiate between WHERE and HAVING clauses. | WHERE applies conditions to individual rows before grouping and cannot use aggregates; HAVING applies conditions to groups after GROUP BY and can use aggregates.
"""), ST(S + '08-st5', 'joins', """
T: Cartesian product | the combination of every row of one table with every row of another table
T: equi-join | a join in which rows of two tables are combined when the values of the common column are equal
T: natural join | an equi-join in which the common column appears only once in the result
Q: If table A has 4 rows and B has 5 rows, their Cartesian product has: | 20 rows | 9 rows | 5 rows | 4 rows
Q: If table A has 3 columns and B has 4 columns, the degree of their Cartesian product is: | 7 | 12 | 4 | 3
Q: In a natural join, the common column appears: | once | twice | not at all | as many times as rows
Q: Which condition makes a Cartesian product an equi-join of EMP and DEPT? | WHERE EMP.DeptId = DEPT.DeptId | WHERE EMP.DeptId <> DEPT.DeptId | ORDER BY DeptId | GROUP BY DeptId
S+: A join without a condition gives the Cartesian product
S+: Table names are used as prefixes (such as EMP.DeptId) when the same column name appears in both tables
S+: The degree of a Cartesian product is the sum of the degrees of the two tables
S-: The cardinality of a Cartesian product is the sum of the cardinalities | It is the product of the cardinalities
S-: A natural join shows the common column twice | It shows the common column once; an equi-join shows it twice
C: Joining two tables needs a common column | rows are matched on the values of that common column
X: C2 D3 2 | Differentiate between an equi-join and a natural join. | Equi-join: joins on equality of a common column and shows it from both tables; natural join: joins on common columns automatically and shows the common column only once.
""")]

CH09 = [ST(S + '09-st1', 'connecting Python with MySQL', """
T: mysql.connector | the Python module (package mysql-connector-python) used to connect a Python program to a MySQL database
T: connection object | the object returned by connect() that represents the link between the Python program and the MySQL server
T: cursor | the object created with con.cursor() that executes SQL queries and holds their results
T: is_connected() | a method of the connection object that returns True if the connection to MySQL is established
Q: Which module is imported to connect Python with MySQL? | mysql.connector | pymysql.sql | sqlite | mysql.python
Q: Which method creates a cursor object? | con.cursor() | con.execute() | cursor.create() | mysql.cursor()
Q: Which arguments are commonly passed to connect()? | host, user, passwd, database | file, mode | table, column | query, result
Q: Which method checks whether the connection is successful? | is_connected() | connected() | check() | status()
Q: Which method closes the connection? | close() | end() | stop() | quit()
S+: A connection must be established before any query can be executed
S+: The cursor object is used to execute queries and fetch their results
S+: The database argument of connect() selects the database to work with
S-: A cursor is created using mysql.connector.cursor() | It is created from the connection: cur = con.cursor()
S-: The connect() function returns a cursor | It returns a connection object; cursor() returns a cursor
C: A program must call con.cursor() before executing a query | queries are executed through the cursor object
X: C2 D2 2 | Write the statements to connect to the MySQL database SCHOOL on localhost (user root, password admin) and create a cursor. | import mysql.connector as m; con = m.connect(host="localhost", user="root", passwd="admin", database="SCHOOL"); cur = con.cursor()
"""), ST(S + '09-st2', 'executing queries and fetching results', """
T: execute() | the cursor method that runs an SQL query given as a string
T: commit() | the connection method that saves the changes made by INSERT, UPDATE or DELETE permanently in the database
T: fetchone() | the cursor method that returns the next row of the result as a tuple, or None when no rows are left
T: fetchall() | the cursor method that returns all remaining rows of the result as a list of tuples
T: fetchmany(n) | the cursor method that returns the next n rows of the result as a list of tuples
T: rowcount | the cursor attribute that gives the number of rows fetched so far or affected by the last query
Q: Which method makes the changes of an UPDATE query permanent? | commit() | execute() | fetchall() | save()
Q: fetchone() returns: | one row as a tuple | all rows as a list | the number of rows | a dictionary of rows
Q: fetchall() returns: | a list of tuples | one tuple | an integer | a string
Q: After an UPDATE query, cur.rowcount gives: | the number of rows affected | the number of columns | always 1 | the table name
Q: fetchone() returns None when: | no more rows are left in the result | the table is empty only | the query is an INSERT | commit() is called
S+: Without commit(), changes made by INSERT, UPDATE or DELETE are not saved permanently
S+: fetchmany(3) returns at most three rows
S+: Each row returned by fetchall() is a tuple
S-: commit() is needed after a SELECT query | commit() is needed after queries that change data, not after SELECT
S-: fetchall() returns only the first row | fetchall() returns all remaining rows as a list
C: An INSERT done through Python is lost if commit() is not called | the transaction is not saved permanently without commit()
X: C2 D3 2 | Differentiate between fetchone() and fetchall(). | fetchone() returns the next single row as a tuple (or None); fetchall() returns all remaining rows as a list of tuples.
"""), ST(S + '09-st3', 'parameterised queries and database programs', """
T: parameterised query | a query in which values are passed separately using placeholders such as %s instead of being typed into the query
T: placeholder | a marker such as %s or {} in a query string that is replaced by an actual value
T: format() | the string method that substitutes values into {} placeholders, used to build query strings
Q: Which placeholder is used with cur.execute(query, values) in mysql.connector? | %s | ? | $1 | #
Q: The second argument of cur.execute("... WHERE id = %s", (5,)) must be a: | tuple (or list) of values | single string only | dictionary only | cursor
Q: "SELECT * FROM T WHERE M > {}".format(50) gives: | SELECT * FROM T WHERE M > 50 | SELECT * FROM T WHERE M > {} | an error | SELECT * FROM T WHERE M > {50}
Q: A menu-driven database program usually repeats its menu using a: | while loop | single if statement | return statement | commit() call
S+: Parameterised queries help prevent SQL injection
S+: String values substituted with format() must be enclosed in quotes inside the query
S+: The same parameterised query can be executed with different values
S-: %s placeholders can be used only for string values | %s is used for values of any type in mysql.connector
S-: A tuple with one value can be written as (5) | A one-value tuple needs a comma: (5,)
C: cur.execute(q, (roll,)) is safer than building the query by joining strings | the connector passes the value separately, so input cannot change the SQL command
X: C3 D3 3 | Write Python statements to delete the record of a student whose roll number is entered by the user from table STUDENT, and display how many rows were deleted. | r = int(input("Roll: ")); cur.execute("DELETE FROM STUDENT WHERE RollNo = %s", (r,)); con.commit(); print(cur.rowcount, "row(s) deleted")
""")]


def fams_ch07_09():
    E = {}
    E[S + '07-st1'] = [F('C4', 'D4', 'case', db_case, marks=4, gap='G7')]
    E[S + '07-st2'] = [F('C2', 'D2', 'mcq', degree_card), F('C3', 'D3', 'mcq', degree_card), F('C3', 'D4', 'mcq', cartesian, gap='G5'), F('C4', 'D4', 'case', db_case, marks=4, gap='G7'),
                       F('C1', 'D1', 'mcq', degree_card)]
    E[S + '07-st3'] = [F('C2', 'D2', 'mcq', keys_q), F('C3', 'D3', 'mcq', keys_q), F('C3', 'D3', 'explain', fk_q, marks=2), F('C4', 'D4', 'case', db_case, marks=4, gap='G7'),
                       F('C3', 'D4', 'mcq', keys_q, gap='G5')]
    E[S + '08-st1'] = [F('C2', 'D2', 'mcq', constr_pick), F('C2', 'D3', 'mcq', dtype_pick), F('C1', 'D1', 'mcq', ddl_dml), F('C3', 'D3', 'mcq', constr_pick), F('C4', 'D3', 'multi_step', ddl_write, marks=3)]
    E[S + '08-st2'] = [F('C3', 'D3', 'multi_step', ddl_write, marks=3), F('C2', 'D2', 'mcq', ddl_dml), F('C3', 'D4', 'mcq', delete_vs_drop, gap='G5'), F('C4', 'D4', 'multi_step', ddl_write, marks=3)]
    E[S + '08-st3'] = [F('C3', 'D3', 'short', lambda r: sql_out(r), marks=1), F('C2', 'D2', 'short', sql_write1, marks=1), F('C3', 'D2', 'mcq', sql_out_mcq), F('C3', 'D4', 'mcq', delete_vs_drop, gap='G5'),
                       F('C4', 'D4', 'explain', lambda r: sql_write(r, 4, 4), marks=4), F('C4', 'D3', 'explain', lambda r: sql_out(r, 2, 2), marks=2),
                       F('C4', 'D5', 'explain', lambda r: sql_out(r, 3, 3), marks=3), F('C2', 'D3', 'mcq', sql_out_mcq)]
    E[S + '08-st4'] = [F('C3', 'D3', 'short', lambda r: sql_out(r), marks=1), F('C3', 'D2', 'mcq', null_count), F('C3', 'D4', 'mcq', sql_out_mcq, gap='G5'),
                       F('C4', 'D4', 'explain', lambda r: sql_write(r, 4, 4), marks=4), F('C4', 'D3', 'explain', lambda r: sql_out(r, 2, 2), marks=2),
                       F('C4', 'D4', 'long', lambda r: dict(sql_write(r, 5, 5)), marks=5), F('C2', 'D2', 'mcq', null_count)]
    E[S + '08-st5'] = [F('C2', 'D2', 'mcq', cartesian), F('C3', 'D3', 'explain', join_out, marks=2), F('C4', 'D4', 'multi_step', join_write, marks=3), F('C3', 'D4', 'explain', join_out, marks=2, gap='G5'),
                       F('C2', 'D3', 'numerical', cartesian, marks=2)]
    E[S + '09-st1'] = [F('C3', 'D3', 'case', conn_case, marks=4, gap='G7'), F('C4', 'D4', 'case', conn_case, marks=4, gap='G7')]
    E[S + '09-st2'] = [F('C3', 'D3', 'short', fetch_out, marks=2), F('C3', 'D4', 'short', fetch_out, marks=2, gap='G5'), F('C4', 'D4', 'case', conn_case, marks=4, gap='G7')]
    E[S + '09-st3'] = [F('C2', 'D3', 'mcq', fmt_query), F('C3', 'D3', 'mcq', fmt_query), F('C4', 'D4', 'long', db_program, marks=5), F('C4', 'D3', 'multi_step', lambda r: db_program(r, 3), marks=3),
                       F('C4', 'D5', 'long', db_program, marks=5)]
    return [CH07, CH08, CH09], E
