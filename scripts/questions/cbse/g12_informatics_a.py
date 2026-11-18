"""CBSE class 12 Informatics Practices (065), chapter 1: Querying and SQL functions.

Function outputs are computed with MySQL semantics (kit.my_round: half away from zero on exact values; MOD takes the
sign of the dividend; INSTR is case-insensitive and 1-based; MID/SUBSTRING are 1-based) and table queries are run
on sqlite3 with those functions installed (kit.DB). Only INT columns and exact literals are rounded, so MySQL's
exact-value rounding rule applies.
"""
from __future__ import annotations

import datetime as dt
import random

from qbank import F, mcq, CITIES
from g12_computer_science_kit import (ST, DB, show_table, uniq, NAMES, my_round, my_mod, my_power, my_mid, my_instr, fmt_val)
import g12_computer_science_d as CSD

S = 'cbse-g12-informatics-ch'


def fv(v):
    return fmt_val(v)


# ---------------------------------------------------------------- st1 math functions
def math_fn(r):
    t = r.randrange(6)
    if t == 0:
        x = round(r.uniform(10, 999), 3)
        d = r.choice([0, 1, 2])
        e = f'ROUND({x}, {d})'
        a = my_round(x, d)
        w = [my_round(x, d + 1), int(x) if d == 0 else round(int(x * 10 ** d) / 10 ** d, d), my_round(x, max(d - 1, 0)) if d else my_round(x, 1)]
        why = f'ROUND(x, {d}) rounds to {d} decimal place(s); 5 and above rounds up.'
    elif t == 1:
        x = r.randint(1000, 99999) + r.choice([0, 0.5, 0.25, 0.75])
        d = r.choice([-1, -2, -3])
        e = f'ROUND({fv(x)}, {d})'
        a = my_round(x, d)
        w = [my_round(x, d + 1), my_round(x, d - 1) if d > -3 else my_round(x, 0), int(x // 10 ** (-d)) * 10 ** (-d) + 10 ** (-d) if a == int(x // 10 ** (-d)) * 10 ** (-d) else int(x // 10 ** (-d)) * 10 ** (-d)]
        why = f'A negative second argument rounds to the left of the decimal point (to the nearest {10 ** (-d)}).'
    elif t == 2:
        a_, b_ = r.randint(10, 99), r.randint(3, 9)
        if a_ % b_ == 0:
            a_ += 1
        sgn = r.choice([1, -1])
        e = f'MOD({sgn * a_}, {b_})'
        a = my_mod(sgn * a_, b_)
        w = [a_ // b_, (sgn * a_) % b_ if (sgn * a_) % b_ != a else -a, a + 1]
        why = 'MOD() gives the remainder; its sign is that of the dividend.'
    elif t == 3:
        b_, p = r.choice([2, 3, 4, 5, 1.5, 2.5]), r.choice([2, 3, -1, 0])
        e = f'POWER({b_}, {p})'
        a = my_power(b_, p)
        w = [my_power(p, b_) if b_ * p else 0, b_ * p, my_power(b_, p + 1)]
        why = 'POWER(m, n) gives m raised to the power n.'
    elif t == 4:
        x = round(r.uniform(1, 99), 2)
        k = r.randint(2, 4)
        e = f'POWER(ROUND({x}, 0), 2) + MOD({k * 7 + 1}, {k})'
        a = my_power(my_round(x, 0), 2) + my_mod(k * 7 + 1, k)
        w = [my_power(int(x), 2) + my_mod(k * 7 + 1, k) if int(x) != my_round(x, 0) else a + 1, my_power(my_round(x, 0), 2), a + k]
        why = 'Evaluate inner functions first.'
    else:
        a1, b1 = r.randint(100, 999), r.randint(6, 9)
        e = f'ROUND({a1} / {b1}, 2)'
        a = my_round(a1 / b1, 2)
        import math
        w = [math.floor(a1 / b1 * 100) / 100, round(a1 / b1, 1), a1 // b1]
        why = 'The division is evaluated first, then rounded to 2 decimal places.'
    ans = fv(a)
    w = [x for x in w if not isinstance(x, complex)]
    wrong = uniq([fv(x) for x in w] + [fv(a + 1), fv(a - 1) if isinstance(a, int) else fv(round(a + 0.1, 3))], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Write the output of the SQL query: SELECT {e};', 'answer': ans, 'key': f'{why} Output: {ans}', 'distractors': wrong}


def math_mcq(r):
    v = math_fn(r)
    return mcq(f'What is the output of SELECT {v["stem"].split("SELECT ", 1)[1][:-1]}?', v['answer'], v['distractors'][:3], v['key'], r)


# ---------------------------------------------------------------- st2 text functions
TWORDS = ['Informatics', 'Practices', 'Database', 'Computer', 'Pandas', 'Matplotlib', 'Learning', 'Network', 'Kolkata', 'Bengaluru', 'Hyderabad',
          'Thiruvananthapuram', 'Chandigarh', 'Ahmedabad', 'Visakhapatnam', 'Gandhinagar', 'Puducherry']


def text_fn(r):
    w = r.choice(TWORDS)
    w2 = r.choice(['INDIA', 'Bharat', 'Yoga Day', 'Digital India', 'Make in India', 'Swachh Bharat', 'Board Exam'])
    t = r.randrange(8)
    n = len(w)
    p, k = r.randint(2, max(2, n - 4)), r.randint(2, 4)
    if t == 0:
        e, a = f"MID('{w}', {p}, {k})", my_mid(w, p, k)
        alts = [my_mid(w, p + 1, k), my_mid(w, p - 1, k), my_mid(w, p, k + 1)]
    elif t == 1:
        e, a = f"SUBSTRING('{w}', -{k + 1}, {k})", my_mid(w, -(k + 1), k)
        alts = [w[-k:], my_mid(w, k + 1, k), w[-(k + 1):], my_mid(w, -k, k), my_mid(w, -(k + 2), k)]
    elif t == 2:
        e, a = f"LEFT('{w}', {k}), RIGHT('{w}', {k})", f'{w[:k]} | {w[-k:]}'
        alts = [f'{w[-k:]} | {w[:k]}', f'{w[:k + 1]} | {w[-k - 1:]}', f'{w[:k - 1]} | {w[-k + 1:]}']
    elif t == 3:
        sub = w[p - 1:p + 1]
        e, a = f"INSTR('{w}', '{sub}')", my_instr(w, sub)
        alts = [p - 1, p + 1, p + 2, n, p - 2]
    elif t == 4:
        sp = ' ' * r.randint(1, 3)
        sp2 = ' ' * r.randint(1, 3)
        f_ = r.choice(['LTRIM', 'RTRIM', 'TRIM'])
        s = sp + w2 + sp2
        res = {'LTRIM': s.lstrip(' '), 'RTRIM': s.rstrip(' '), 'TRIM': s.strip(' ')}[f_]
        e, a = f"LENGTH({f_}('{s}'))", len(res)
        alts = [len(s), len(w2), len(s.lstrip(' ')) if f_ != 'LTRIM' else len(s.rstrip(' ')), len(res) + 1, len(res) - 1]
    elif t == 5:
        e, a = f"UCASE(MID('{w2}', 1, {k}))", my_mid(w2, 1, k).upper()
        alts = [my_mid(w2, 2, k).upper(), w2[:k + 1].upper(), w2[:k - 1].upper(), w2[-k:].upper()]
    elif t == 6:
        e, a = f"LCASE(LEFT('{w}', {k})) , LENGTH('{w}')", f'{w[:k].lower()} | {n}'
        alts = [f'{w[:k].lower()} | {n - 1}', f'{w[-k:].lower()} | {n}', f'{w[:k + 1].lower()} | {n}', f'{w[:k].lower()} | {n + 1}']
    else:
        e, a = f"CONCAT(LEFT('{w}', {k}), RIGHT('{w2}', {k}))", w[:k] + w2[-k:]
        alts = [w[:k] + w2[:k], w[-k:] + w2[-k:], w2[-k:] + w[:k]]
    ans = str(a)
    wrong = uniq([str(x) for x in alts], [ans])
    if len(wrong) < 3 or not ans.strip():
        raise ValueError('few')
    return {'stem': f'Write the output of the SQL query: SELECT {e};', 'answer': ans,
            'key': f'Positions in MySQL string functions start at 1. Output: {ans}' + (' (two columns shown as "a | b")' if ' | ' in ans else ''), 'distractors': wrong}


def text_mcq(r):
    v = text_fn(r)
    return mcq(f'What is the output of SELECT {v["stem"].split("SELECT ", 1)[1][:-1]}?', v['answer'], v['distractors'][:3], v['key'], r)


# ---------------------------------------------------------------- st3 date functions
def date_fn(r):
    d = dt.date(r.randint(2000, 2026), r.randint(1, 12), r.randint(1, 28))
    ds = d.isoformat()
    t = r.randrange(6)
    if t == 0:
        e, a = f"MONTHNAME('{ds}')", d.strftime('%B')
        alts = [(d.replace(month=d.month % 12 + 1)).strftime('%B'), str(d.month), d.strftime('%b')]
    elif t == 1:
        e, a = f"DAYNAME('{ds}')", d.strftime('%A')
        alts = [(d + dt.timedelta(days=1)).strftime('%A'), (d - dt.timedelta(days=1)).strftime('%A'), str(d.day)]
    elif t == 2:
        e, a = f"MONTH('{ds}') + DAY('{ds}')", d.month + d.day
        alts = [d.month * d.day, d.year + d.day, d.month + d.day + 1, d.month + d.day - 1, d.day]
    elif t == 3:
        e, a = f"YEAR('{ds}') - {d.year - r.randint(5, 20)}", None
        k = int(e.split('- ')[1])
        a = d.year - k
        alts = [a + 1, d.year, a - 1]
    elif t == 4:
        hh = r.randint(0, 23)
        e, a = f"DATE('{ds} {hh:02d}:{r.randint(0, 59):02d}:00')", ds
        alts = [f'{ds} {hh:02d}:00:00', f'{d.day:02d}-{d.month:02d}-{d.year}', str(d.year)]
    else:
        e, a = f"CONCAT(DAY('{ds}'), '-', MONTHNAME('{ds}'))", f'{d.day}-{d.strftime("%B")}'
        alts = [f'{d.month}-{d.strftime("%B")}', f'{d.day}-{d.strftime("%b")}', f'{d.day}-{d.month}']
    ans = str(a)
    wrong = uniq([str(x) for x in alts], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Write the output of the SQL query: SELECT {e};', 'answer': ans, 'key': f'Output: {ans}.', 'distractors': wrong}


def date_mcq(r):
    v = date_fn(r)
    return mcq(f'What is the output of SELECT {v["stem"].split("SELECT ", 1)[1][:-1]}?', v['answer'], v['distractors'][:3], v['key'], r)


# ---------------------------------------------------------------- table queries with functions
def fn_table(r):
    n = r.randint(5, 7)
    nm = r.sample(NAMES, n)
    ids = sorted(r.sample(range(1, 60), n))
    rows = []
    for i in range(n):
        d = dt.date(r.randint(2015, 2024), r.randint(1, 12), r.randint(1, 28))
        rows.append([ids[i], f'{nm[i]} {r.choice(["Sharma", "Iyer", "Khan", "Gill", "Das", "Nair", "Rao", "Mehta"])}', r.choice(CITIES[:8]), float(r.randint(18, 95) * 1000 + r.choice([0, 250, 500, 750])), d.isoformat()])   # float: '/' must not be integer division in sqlite
    return 'STAFF', ['SNo', 'SName', 'City', 'Salary', 'DOJ'], rows


FN_Q = [
    'SELECT UCASE(LEFT(SName, 3)), LENGTH(City) FROM STAFF WHERE SNo < {k} ORDER BY SNo;',
    'SELECT SName, MONTHNAME(DOJ) FROM STAFF WHERE YEAR(DOJ) >= {y} ORDER BY SNo;',
    'SELECT ROUND(Salary / 12, 1) FROM STAFF WHERE City = \'{c}\' ORDER BY SNo;',
    'SELECT MID(SName, 2, 3), DAY(DOJ) FROM STAFF ORDER BY SNo;',
    'SELECT SName FROM STAFF WHERE INSTR(SName, \'a\') = 2 ORDER BY SNo;',
    'SELECT MOD(Salary, 7), ROUND(Salary, -4) FROM STAFF WHERE SNo > {k} ORDER BY SNo;',
    'SELECT LCASE(City), DAYNAME(DOJ) FROM STAFF WHERE MONTH(DOJ) > 6 ORDER BY SNo;',
]


def fn_table_out(r, n_q=1, marks=1):
    tname, cols, rows = fn_table(r)
    db = DB([(tname, cols, rows)])
    k = rows[len(rows) // 2][0]
    y = sorted(int(x[4][:4]) for x in rows)[len(rows) // 2]
    c = r.choice([x[2] for x in rows])
    qs = [q.format(k=k, y=y, c=c) for q in r.sample(FN_Q, n_q)]
    outs = [db.result(q) for q in qs]
    if any(o.startswith('Empty') for o in outs):
        raise ValueError('empty')
    tbl = show_table(tname, cols, rows)
    if n_q == 1:
        return {'stem': f'Consider the table:\n{tbl}\nWrite the output of the query:\n{qs[0]}', 'answer': outs[0], 'key': f'{marks} mark(s) for the correct output:\n{outs[0]}', 'marks': marks}
    lab = ['i', 'ii', 'iii'][:n_q]
    return {'stem': f'Consider the table:\n{tbl}\nWrite the output of:\n' + '\n'.join(f'({l}) {q}' for l, q in zip(lab, qs)),
            'answer': '\n'.join(f'({l})\n{o}' for l, o in zip(lab, outs)), 'key': f'{marks} marks: {marks / n_q:g} for each output.', 'marks': marks}


FN_TASKS = [
    ('Display the first three characters of every SName in capital letters.', 'SELECT UCASE(LEFT(SName, 3)) FROM STAFF;'),
    ('Display SName and the month name of DOJ.', 'SELECT SName, MONTHNAME(DOJ) FROM STAFF;'),
    ('Display the monthly salary (Salary / 12) rounded to 2 decimal places.', 'SELECT ROUND(Salary / 12, 2) FROM STAFF;'),
    ('Display the names of staff who joined on a Monday.', "SELECT SName FROM STAFF WHERE DAYNAME(DOJ) = 'Monday';"),
    ('Display the number of characters in each City.', 'SELECT City, LENGTH(City) FROM STAFF;'),
    ('Display SName of staff who joined in the year {y}.', 'SELECT SName FROM STAFF WHERE YEAR(DOJ) = {y};'),
    ('Display the position of the first "a" in each SName.', "SELECT SName, INSTR(SName, 'a') FROM STAFF;"),
    ('Display the last four characters of each City in lower case.', 'SELECT LCASE(RIGHT(City, 4)) FROM STAFF;'),
    ('Display the remainder when Salary is divided by 1000.', 'SELECT MOD(Salary, 1000) FROM STAFF;'),
    ('Display the day of the month on which each staff member joined.', 'SELECT SName, DAY(DOJ) FROM STAFF;'),
]


def fn_write(r, n=4, marks=4):
    tname, cols, rows = fn_table(r)
    y = int(rows[0][4][:4])
    pick = r.sample(FN_TASKS, n)
    db = DB([(tname, cols, rows)])
    for _, q in pick:
        db.q(q.format(y=y))
    lab = ['i', 'ii', 'iii', 'iv', 'v'][:n]
    return {'stem': f'Consider the table STAFF:\n{show_table(tname, cols, rows)}\nWrite SQL queries to:\n' + '\n'.join(f'({l}) {t.format(y=y)}' for l, (t, _) in zip(lab, pick)),
            'answer': '\n'.join(f'({l}) {q.format(y=y)}' for l, (_, q) in zip(lab, pick)), 'key': f'{marks} marks: {marks / n:g} for each correct query.', 'marks': marks}


def fn_write1(r):
    t, q = r.choice(FN_TASKS)
    y = r.randint(2015, 2024)
    return {'stem': f'Table STAFF has the columns SNo, SName, City, Salary, DOJ (date of joining). Write an SQL query to: {t.format(y=y)[0].lower() + t.format(y=y)[1:]}',
            'answer': q.format(y=y), 'key': f'1 mark: {q.format(y=y)}', 'marks': 1}


def fn_case(r):
    who = r.choice(NAMES)
    tname, cols, rows = fn_table(r)
    db = DB([(tname, cols, rows)])
    q1 = 'SELECT COUNT(*) FROM STAFF WHERE MONTH(DOJ) BETWEEN 4 AND 9;'
    q2 = 'SELECT MAX(LENGTH(City)) FROM STAFF;'
    a1, a2 = db.q(q1)[1][0][0], db.q(q2)[1][0][0]
    return {'stem': (f'{who} manages the STAFF table of a coaching centre:\n{show_table(tname, cols, rows)}\n(i) Write the output of: {q1} (1)\n(ii) Write the output of: {q2} (1)\n'
                     '(iii) Write a query to display SName and the year of joining of all staff from Delhi. (1)\n(iv) Which function returns the current date and time? (1)'),
            'answer': f"(i) {a1} (ii) {a2} (iii) SELECT SName, YEAR(DOJ) FROM STAFF WHERE City = 'Delhi'; (iv) NOW()", 'key': '1 mark each.', 'marks': 4}


# ---------------------------------------------------------------- st5 set operations
def set_ops(r):
    pool = r.sample(NAMES, 9)
    a = sorted(r.sample(pool, 5))
    b = sorted(r.sample(pool, 4))
    if not set(a) & set(b) or set(b) <= set(a):
        raise ValueError('overlap')
    t1, t2 = r.choice([('DANCE', 'MUSIC'), ('CRICKET', 'CHESS'), ('SCIENCE_CLUB', 'MATHS_CLUB'), ('NCC', 'NSS'), ('ECO_CLUB', 'QUIZ_CLUB')])
    op = r.choice(['UNION', 'INTERSECT', 'MINUS'])
    res = {'UNION': sorted(set(a) | set(b)), 'INTERSECT': sorted(set(a) & set(b)), 'MINUS': sorted(set(a) - set(b))}[op]
    alt = {'UNION': [sorted(a + b), sorted(set(a) & set(b)), sorted(set(a) - set(b))],
           'INTERSECT': [sorted(set(a) | set(b)), sorted(set(a) - set(b)), sorted(set(b) - set(a))],
           'MINUS': [sorted(set(b) - set(a)), sorted(set(a) & set(b)), sorted(set(a) | set(b))]}[op]
    fmt = lambda L: ', '.join(L) if L else 'no rows'
    ans = fmt(res)
    wrong = uniq([fmt(x) for x in alt] + [fmt(sorted(set(a) ^ set(b)))], [ans])
    return mcq(f'Table {t1} has one column Name with the values: {", ".join(a)}. Table {t2} has one column Name with the values: {", ".join(b)}. '
               f'Which names are in {t1} {op} {t2}? (Names listed in alphabetical order.)', ans, wrong[:3],
               {'UNION': 'UNION gives rows in either table, without duplicates.', 'INTERSECT': 'INTERSECT gives rows common to both tables.',
                'MINUS': f'MINUS gives rows of {t1} that are not in {t2}.'}[op], r)


def set_count(r):
    a, b = r.randint(4, 9), r.randint(3, 8)
    c = r.randint(1, min(a, b) - 1)
    t = r.randrange(3)
    q, ans = [(f'UNION', a + b - c), ('INTERSECT', c), ('MINUS (first table minus second)', a - c)][t]
    return {'stem': f'Two union-compatible tables have {a} and {b} distinct rows, and {c} rows appear in both. How many rows are there in their {q}?', 'answer': str(ans),
            'key': f'UNION = {a} + {b} − {c}; INTERSECT = {c}; MINUS = {a} − {c}. Answer: {ans}.', 'distractors': uniq([str(a + b), str(a * b), str(c), str(a - c), str(a + b - c)], [str(ans)]),
            'marks': 2}


CH01 = [ST(S + '01-st1', 'math functions in SQL', """
T: single row function | a function that works on one row at a time and returns one value for each row, such as ROUND() or UCASE()
T: POWER() | the function that returns a number raised to a power, as in POWER(2, 3) = 8
T: ROUND() | the function that rounds a number to a given number of decimal places
T: MOD() | the function that returns the remainder of one number divided by another
Q: SELECT POWER(3, 2); gives: | 9 | 6 | 8 | 5
Q: SELECT MOD(17, 5); gives: | 2 | 3 | 3.4 | 12
Q: SELECT ROUND(45.678, 1); gives: | 45.7 | 45.6 | 46 | 45.68
Q: SELECT ROUND(1576.4, -2); gives: | 1600 | 1500 | 1576 | 1580
Q: Which function is a single row function? | ROUND() | SUM() | COUNT() | AVG()
Q: SELECT POWER(2, -1); gives: | 0.5 | -2 | 2 | -0.5
S+: ROUND(x) without a second argument rounds to the nearest integer
S+: A negative second argument of ROUND() rounds digits to the left of the decimal point
S+: Single row functions return one value for every row of the table
S+: MOD(10, 2) returns 0 because 10 is divisible by 2
S-: MOD(17, 5) returns 3 | MOD gives the remainder 2; 17 = 5 × 3 + 2
S-: ROUND(45.65, 1) returns 45.6 | It returns 45.7, since the digit 5 rounds up
S-: POWER(2, 3) returns 6 | It returns 8, since 2 × 2 × 2 = 8
C: ROUND(678.9, -1) returns 680 | the second argument -1 rounds to the nearest ten
C: MOD() can be used to find even values | MOD(n, 2) = 0 only for even numbers
X: C2 D2 2 | Differentiate between single row functions and aggregate functions with one example each. | Single row: works on each row and returns a value per row, e.g. ROUND(Salary); aggregate: works on a group of rows and returns one value, e.g. SUM(Salary).
"""), ST(S + '01-st2', 'text functions in SQL', """
T: UCASE() | the function that converts a string to upper case (also UPPER())
T: LCASE() | the function that converts a string to lower case (also LOWER())
T: MID() | the function that extracts a substring from a given position for a given number of characters (same as SUBSTRING())
T: LENGTH() | the function that returns the number of characters in a string
T: INSTR() | the function that returns the position of the first occurrence of a substring in a string, or 0 if it is not found
T: TRIM() | the function that removes leading and trailing spaces from a string
Q: SELECT LENGTH('INDIA'); gives: | 5 | 4 | 6 | INDIA
Q: SELECT INSTR('COMPUTER', 'PUT'); gives: | 4 | 3 | 5 | 0
Q: SELECT LEFT('Informatics', 4); gives: | Info | tics | Inf | form
Q: SELECT RIGHT('Practices', 3); gives: | ces | Pra | ice | tices
Q: Which function removes spaces only from the left side of a string? | LTRIM() | RTRIM() | TRIM() | LEFT()
Q: SELECT MID('Database', 3, 4); gives: | taba | atab | Data | base
Q: INSTR('PYTHON', 'Z') returns: | 0 | -1 | NULL | 1
S+: In MySQL string functions, the first character is at position 1
S+: SUBSTRING() and MID() work in the same way
S+: LENGTH() counts spaces as characters
S+: A negative position in SUBSTRING() counts from the end of the string
S-: INSTR() returns -1 when the substring is not found | It returns 0
S-: MID('Python', 0, 2) returns "Py" | Positions start at 1; MID('Python', 1, 2) returns "Py"
S-: TRIM() removes all the spaces inside a string | TRIM() removes only leading and trailing spaces
C: LENGTH(TRIM(' Hi ')) returns 2 | TRIM() removes the leading and trailing spaces before LENGTH() counts
C: UCASE(Name) helps compare names typed in mixed case | it converts all letters to the same (upper) case
X: C2 D3 2 | Write the output: (i) SELECT UCASE(MID('informatics', 3, 4)); (ii) SELECT INSTR('practices', 'c'); | (i) FORM (ii) 4
"""), ST(S + '01-st3', 'date functions in SQL', """
T: NOW() | the function that returns the current date and time
T: DATE() | the function that extracts the date part from a date-time value
T: MONTHNAME() | the function that returns the name of the month of a date, such as August
T: DAYNAME() | the function that returns the name of the weekday of a date, such as Monday
T: YEAR() | the function that returns the year part of a date
Q: SELECT MONTH('2024-08-15'); gives: | 8 | 15 | August | 2024
Q: SELECT MONTHNAME('2024-01-26'); gives: | January | 1 | Jan | 26
Q: SELECT DAY('2023-12-25'); gives: | 25 | 12 | Monday | 2023
Q: Which function returns the current date and time? | NOW() | DATE() | DAY() | TODAY()
Q: SELECT YEAR('2025-03-08'); gives: | 2025 | 3 | 8 | 25
Q: SELECT DATE('2024-08-15 10:30:00'); gives: | 2024-08-15 | 10:30:00 | 15 | 2024
S+: In MySQL, dates are written in the format 'YYYY-MM-DD'
S+: DAYNAME() returns the name of the weekday, while DAY() returns the day of the month
S+: NOW() returns both the date and the time
S-: DAY('2024-08-15') returns Thursday | DAY() returns 15; DAYNAME() returns the weekday
S-: MONTH('2024-08-15') returns August | MONTH() returns 8; MONTHNAME() returns August
C: NOW() gives a different value each time it is run | it returns the current date and time of the system
X: C2 D2 2 | Differentiate between DAY() and DAYNAME() with an example. | DAY('2024-08-15') returns 15 (day of the month); DAYNAME('2024-08-15') returns Thursday (name of the weekday).
"""), ST(S + '01-st4', 'aggregate functions and GROUP BY', """
T: aggregate function | a multiple row function that works on a set of rows and returns a single value, such as MAX, MIN, AVG, SUM and COUNT
T: GROUP BY | the clause that groups rows with the same value in a column so that aggregate functions can be applied to each group
T: HAVING | the clause used to apply conditions to groups formed with GROUP BY
T: ORDER BY | the clause used to sort the rows of the result in ascending or descending order
Q: Which function counts all rows including NULLs? | COUNT(*) | COUNT(column) | SUM(*) | MAX(*)
Q: Conditions on groups are given with: | HAVING | WHERE | ORDER BY | DISTINCT
Q: Aggregate functions are also called: | multiple row functions | single row functions | text functions | date functions
Q: Which clause sorts the output in descending order? | ORDER BY ... DESC | GROUP BY ... DESC | SORT DESC | HAVING DESC
S+: Aggregate functions except COUNT(*) ignore NULL values
S+: WHERE filters rows before grouping; HAVING filters groups after grouping
S+: GROUP BY can be combined with ORDER BY in the same query
S-: HAVING can be used without aggregate conditions only | HAVING is mainly used with aggregate conditions on groups
S-: AVG() counts NULLs as zero | AVG() ignores NULL values
C: COUNT(*) and COUNT(Marks) may differ | COUNT(Marks) does not count rows where Marks is NULL
X: C2 D3 2 | Differentiate between WHERE and HAVING. | WHERE applies to individual rows before grouping and cannot contain aggregate functions; HAVING applies to groups after GROUP BY and can.
"""), ST(S + '01-st5', 'operations on relations and joins', """
T: UNION | the operation that combines the rows of two union-compatible tables, removing duplicate rows
T: INTERSECT | the operation that gives the rows common to two tables
T: MINUS | the operation that gives the rows of the first table that are not in the second (also called set difference)
T: Cartesian product | the operation that combines every row of one table with every row of another
T: union-compatible | the property of two tables that have the same number of columns with matching domains, needed for UNION, INTERSECT and MINUS
Q: Which operation removes duplicate rows while combining two tables? | UNION | Cartesian product | JOIN | MINUS
Q: A has 3 rows and B has 4 rows; the Cartesian product has: | 12 rows | 7 rows | 4 rows | 1 row
Q: Rows present in table A but not in table B are given by: | A MINUS B | A UNION B | A INTERSECT B | B MINUS A
Q: For UNION, the two tables must have: | the same number of columns with compatible domains | the same number of rows | the same primary key | no common rows
S+: UNION removes duplicate rows from the result
S+: A MINUS B and B MINUS A may give different results
S+: The degree of a Cartesian product is the sum of the degrees of the two tables
S-: INTERSECT gives all rows of both tables | INTERSECT gives only the common rows; UNION gives all rows
S-: The cardinality of a Cartesian product is the sum of the two cardinalities | It is the product of the two cardinalities
C: UNION needs union-compatible tables | the rows of both tables must have the same structure to be combined
X: C2 D3 2 | Differentiate between UNION and Cartesian product. | UNION combines rows of two union-compatible tables (rows added, duplicates removed); Cartesian product pairs every row of one table with every row of the other (degree adds, cardinality multiplies).
""")]


def fams_ch01():
    E = {}
    E[S + '01-st1'] = [F('C2', 'D2', 'short', math_fn, marks=1), F('C3', 'D3', 'mcq', math_mcq), F('C2', 'D3', 'mcq', math_mcq), F('C3', 'D4', 'short', math_fn, marks=1, gap='G5'),
                       F('C4', 'D3', 'explain', lambda r: fn_table_out(r, 2, 2), marks=2), F('C4', 'D4', 'case', fn_case, marks=4, gap='G7'), F('C1', 'D1', 'mcq', math_mcq)]
    E[S + '01-st2'] = [F('C2', 'D2', 'short', text_fn, marks=1), F('C3', 'D3', 'mcq', text_mcq), F('C2', 'D3', 'mcq', text_mcq), F('C3', 'D4', 'short', text_fn, marks=1, gap='G5'),
                       F('C3', 'D3', 'short', lambda r: fn_table_out(r), marks=1), F('C4', 'D4', 'explain', lambda r: fn_write(r, 4, 4), marks=4), F('C2', 'D2', 'short', fn_write1, marks=1),
                       F('C4', 'D3', 'explain', lambda r: fn_table_out(r, 3, 3), marks=3)]
    E[S + '01-st3'] = [F('C2', 'D2', 'short', date_fn, marks=1), F('C3', 'D3', 'mcq', date_mcq), F('C3', 'D4', 'mcq', date_mcq, gap='G5'), F('C4', 'D4', 'case', fn_case, marks=4, gap='G7'),
                       F('C1', 'D1', 'mcq', date_mcq)]
    E[S + '01-st4'] = [F('C3', 'D3', 'short', lambda r: CSD.sql_out(r), marks=1), F('C3', 'D2', 'mcq', CSD.null_count), F('C3', 'D4', 'mcq', CSD.sql_out_mcq, gap='G5'),
                       F('C4', 'D4', 'explain', lambda r: CSD.sql_write(r, 4, 4), marks=4), F('C4', 'D3', 'explain', lambda r: CSD.sql_out(r, 2, 2), marks=2),
                       F('C4', 'D4', 'long', lambda r: CSD.sql_write(r, 5, 5), marks=5), F('C4', 'D5', 'explain', lambda r: CSD.sql_out(r, 3, 3), marks=3), F('C2', 'D2', 'mcq', CSD.sql_out_mcq),
                       F('C2', 'D2', 'short', CSD.sql_write1, marks=1), F('C4', 'D3', 'long', lambda r: CSD.sql_write(r, 5, 5), marks=5)]
    E[S + '01-st5'] = [F('C2', 'D2', 'mcq', set_ops), F('C3', 'D3', 'mcq', set_ops), F('C3', 'D3', 'numerical', set_count, marks=2), F('C2', 'D3', 'mcq', CSD.cartesian),
                       F('C3', 'D4', 'explain', CSD.join_out, marks=2, gap='G5'), F('C4', 'D4', 'multi_step', CSD.join_write, marks=3)]
    return [CH01], E
