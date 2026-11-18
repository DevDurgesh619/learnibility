"""Shared helpers for the CBSE class 12 Computer Science (083) and Informatics Practices (065) banks.

* run(code)            executes a Python snippet and returns what it prints (answers are computed, never typed)
* exc(code)            name of the exception a snippet raises (or None)
* SQL helpers          sqlite3 database with MySQL-compatible functions (ROUND, MOD, POWER, MID, INSTR,
                       UCASE, MONTHNAME, DAYNAME ...), table rendering and result rendering
* fact tables          thin wrapper over g12_hum_engine (line-based fact tables -> families)
* assign_kinds         tags families with the mock kinds k2 / k3 / k4 / k5 from their marks
"""
from __future__ import annotations

import contextlib
import datetime as dt
import io
import random
import sqlite3
from decimal import Decimal, ROUND_HALF_UP

import g12_hum_engine as HE
from qbank import F, mcq, ar, onorm, GIRLS, BOYS, CITIES, TYPE_MARKS

NAMES = GIRLS + BOYS
SURN = ['Sharma', 'Verma', 'Iyer', 'Nair', 'Khan', 'Gill', 'Das', 'Reddy', 'Patel', 'Joshi', 'Mehta', 'Rao', 'Singh',
        'Bose', 'Kaur', 'Menon', 'Pillai', 'Ansari', 'Chopra', 'Kulkarni']


# ---------------------------------------------------------------- running Python

def run(code: str) -> str:
    buf = io.StringIO()
    g = {'__name__': '__main__'}
    with contextlib.redirect_stdout(buf):
        exec(compile(code, '<snippet>', 'exec'), g)
    return buf.getvalue().rstrip('\n')


def exc(code: str):
    """Return (output_before_error, exception class name or None)."""
    buf = io.StringIO()
    g = {'__name__': '__main__'}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, '<snippet>', 'exec'), g)
    except Exception as e:  # noqa: BLE001
        return buf.getvalue().rstrip('\n'), type(e).__name__
    return buf.getvalue().rstrip('\n'), None


def run_or_err(code: str) -> str:
    try:
        return run(code)
    except Exception as e:  # noqa: BLE001
        return f'Error ({type(e).__name__})'


def compiles(code: str) -> bool:
    try:
        compile(code, '<snippet>', 'exec')
        return True
    except SyntaxError:
        return False


def uniq(seq, exclude=()):
    seen = {onorm(x) for x in exclude}
    out = []
    for x in seq:
        k = onorm(x)
        if k and k not in seen:
            seen.add(k)
            out.append(x)
    return out


def out_item(r, code, wrong_codes=(), wrong_lits=(), head='Predict the output of the following Python code:',
             key='', marks=None, as_mcq=False, typ_note=''):
    """Output-prediction item: answer = what the code prints; distractors = outputs of plausible slips."""
    ans = run(code)
    if not ans.strip():
        raise ValueError('empty output')
    wrong = [run_or_err(c) for c in wrong_codes] + list(wrong_lits)
    wrong = [w for w in uniq(wrong, [ans]) if w.strip() and not w.startswith('Error')] + [w for w in wrong if w.startswith('Error')]
    wrong = uniq(wrong, [ans])
    stem = f'{head}\n{code}'
    k = key or f'The code prints {ans}.'
    d = {'stem': stem, 'answer': ans, 'key': k, 'distractors': wrong}
    if marks:
        d['marks'] = marks
    if as_mcq:
        if len(wrong) < 3:
            raise ValueError('few distractors')
        return mcq(stem, ans, r.sample(wrong[:6], 3) if len(wrong) > 3 else wrong, k, r)
    return d


def pick(r, seq, k=None):
    return r.choice(seq) if k is None else r.sample(seq, k)


VARS = ['L', 'A', 'nums', 'data', 'vals', 'marks', 'items', 'arr', 'lst', 'scores', 'P', 'Q', 'T', 'X', 'M']
FUNCS = ['change', 'update', 'modify', 'process', 'alter', 'calc', 'compute', 'work', 'show', 'fun', 'convert',
         'execute', 'shift', 'mix', 'test', 'check', 'display', 'transform']
WORDS = ['INDIA', 'Python', 'CBSE', 'Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bengaluru', 'Science', 'Computer',
         'Program', 'Keyboard', 'Monitor', 'Function', 'Variable', 'Exam2025', 'Board@12', 'NCERT', 'Learning',
         'Jaipur', 'Lucknow', 'Hyderabad', 'Network', 'Database', 'Holiday', 'Teacher', 'Cricket', 'Diwali']
SENTS = ['Python is fun', 'Learning never stops', 'Practice makes perfect', 'Work hard dream big', 'India is my country',
         'Health is wealth', 'Knowledge is power', 'Save water save life', 'Time and tide wait for none',
         'Unity in diversity', 'Honesty is the best policy', 'All that glitters is not gold', 'Read every day',
         'Code is poetry', 'Keep calm and code on', 'Clean India green India', 'Slow and steady wins the race']


# ---------------------------------------------------------------- MySQL-compatible SQL on sqlite

def _dec(x):
    return Decimal(repr(x)) if isinstance(x, float) else Decimal(x)


def my_round(x, d=0):
    if x is None:
        return None
    d = int(d)
    q = Decimal(1).scaleb(-d)
    v = _dec(x).quantize(q, rounding=ROUND_HALF_UP) if d >= 0 else (_dec(x) / Decimal(10) ** (-d)).quantize(Decimal(1), rounding=ROUND_HALF_UP) * Decimal(10) ** (-d)
    if isinstance(x, int) and d >= 0:
        return int(v)
    if d <= 0:
        return int(v)
    return float(v)


def my_mod(a, b):
    if a is None or b is None or b == 0:
        return None
    if isinstance(a, int) and isinstance(b, int):
        m = abs(a) % abs(b)
        return -m if a < 0 else m
    m = _dec(abs(a)) % _dec(abs(b))
    m = -m if a < 0 else m
    return float(m)


def my_power(a, b):
    v = float(a) ** float(b)
    return int(v) if v.is_integer() and abs(v) < 1e15 else v


def my_mid(s, p, n=None):
    if s is None:
        return None
    p = int(p)
    if p == 0:
        return ''
    start = p - 1 if p > 0 else len(s) + p
    if start < 0:
        return ''
    return s[start:] if n is None else s[start:start + int(n)]


def my_instr(s, sub):
    if s is None or sub is None:
        return None
    return s.lower().find(sub.lower()) + 1


def _d(s):
    return dt.date.fromisoformat(str(s)[:10])


def install_mysql(con: sqlite3.Connection):
    con.create_function('ROUND', 1, my_round)
    con.create_function('ROUND', 2, my_round)
    con.create_function('MOD', 2, my_mod)
    con.create_function('POWER', 2, my_power)
    con.create_function('POW', 2, my_power)
    con.create_function('UCASE', 1, lambda s: None if s is None else s.upper())
    con.create_function('LCASE', 1, lambda s: None if s is None else s.lower())
    con.create_function('MID', 3, my_mid)
    con.create_function('MID', 2, my_mid)
    con.create_function('SUBSTRING', 3, my_mid)
    con.create_function('SUBSTRING', 2, my_mid)
    con.create_function('SUBSTR', 3, my_mid)
    con.create_function('LEFT', 2, lambda s, n: None if s is None else s[:max(0, int(n))])
    con.create_function('RIGHT', 2, lambda s, n: None if s is None else (s[-int(n):] if int(n) > 0 else ''))
    con.create_function('INSTR', 2, my_instr)
    con.create_function('MONTH', 1, lambda s: _d(s).month)
    con.create_function('YEAR', 1, lambda s: _d(s).year)
    con.create_function('DAY', 1, lambda s: _d(s).day)
    con.create_function('DAYOFMONTH', 1, lambda s: _d(s).day)
    con.create_function('MONTHNAME', 1, lambda s: _d(s).strftime('%B'))
    con.create_function('DAYNAME', 1, lambda s: _d(s).strftime('%A'))
    con.create_function('DATE', 1, lambda s: str(s)[:10])


def fmt_val(v, avg=False):
    if v is None:
        return 'NULL'
    if avg:
        return f'{Decimal(repr(float(v))).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)}'
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() and abs(v) < 1e15 else f'{v:.10g}'
    return str(v)


class DB:
    """A small sqlite database built from (name, columns, rows) tables; MySQL functions installed."""

    def __init__(self, tables):
        self.con = sqlite3.connect(':memory:')
        install_mysql(self.con)
        self.tables = {}
        for tname, cols, rows in tables:
            self.add(tname, cols, rows)

    def add(self, tname, cols, rows):
        cl = ', '.join(cols)
        self.con.execute(f'CREATE TABLE {tname} ({cl})')
        self.con.executemany(f'INSERT INTO {tname} VALUES ({", ".join("?" * len(cols))})', rows)
        self.tables[tname] = (cols, rows)

    def q(self, sql):
        cur = self.con.execute(sql)
        head = [d[0] for d in cur.description]
        return head, cur.fetchall()

    def result(self, sql):
        head, rows = self.q(sql)
        avg = [h.upper().startswith('AVG(') for h in head]
        return render(head, [[fmt_val(v, a) for v, a in zip(rw, avg)] for rw in rows])


def render(head, rows):
    if not rows:
        return 'Empty set (no rows)'
    out = [' | '.join(str(h) for h in head)]
    for rw in rows:
        out.append(' | '.join(fmt_val(x) if not isinstance(x, str) else x for x in rw))
    return '\n'.join(out)


def show_table(tname, cols, rows):
    return f'Table: {tname}\n' + render(cols, [[fmt_val(x) for x in rw] for rw in rows])


# ---------------------------------------------------------------- fact tables (g12_hum_engine)

import re as _re

_CODEY = _re.compile(r'^(?:[a-z_][\w.]*\s*[\(\[.=]|[a-z]\b|(?:raise|assert|pickle|def|import)\b)')


def _py(x: str) -> str:
    """Statements that start with lower-case code (len(), s[0], pickle ...) get "In Python, " so that the engine's
    capitalisation never turns them into Len(), S[0] or Pickle."""
    return 'In Python, ' + x if _CODEY.match(x) else x


def ST(sid, topic, text):
    out = []
    for line in text.strip().splitlines():
        tag, sep, rest = line.partition(': ')
        if tag in ('S+', 'S-', 'C') and sep:
            parts = rest.split(' | ')
            parts[0] = _py(parts[0])
            if tag == 'C' and len(parts) > 1:
                parts[1] = _py(parts[1])
            line = f'{tag}: ' + ' | '.join(parts)
        out.append(line)
    return HE.ST(sid, topic, '\n'.join(out))


CODE_KEEP = {'recall', 'what_is', 'three', 'not_correct', 'ar_item', 'fix', 'gen'}


def fact_families(chapters, extra=None, drop_case=(), long_marks=5, code=(), code_weight=2):
    """chapters: list of lists of Sub. Returns {sid: [Family]} (engine families + extra).

    For code subtopics (`code`) only a few engine fact families are kept (recall, statements, A-R, correction,
    hand-written items) and every code family is entered `code_weight` times, so that output-prediction,
    error-finding and coding tasks make up most of those subtopics' items."""
    import dataclasses
    cfgs = [{'long_marks': long_marks, 'case_marks': (1, 1, 2), 'chapter_topic': ''} for _ in chapters]
    fams = HE.families(chapters, cfgs, None)
    for sid in fams:
        if sid in drop_case or drop_case == 'all':
            fams[sid] = [f for f in fams[sid] if f.type != 'case']
        ex = list((extra or {}).get(sid, []))
        if sid in code:
            fams[sid] = [f for f in fams[sid] if f.gen.__name__ in CODE_KEEP]
            ex = [dataclasses.replace(f) for f in ex for _ in range(code_weight)]
        fams[sid] += ex
    return fams


# ---------------------------------------------------------------- mock kinds

def assign_kinds(fams: dict):
    """k2 / k3 / k4 / k5 mock kinds from each written family's marks (MCQ and A-R families serve 'mcq' / 'ar')."""
    for fs in fams.values():
        for f in fs:
            if f.type == 'mcq':
                continue
            m = f.marks or TYPE_MARKS[f.type][0]
            k = {2: 'k2', 3: 'k3', 4: 'k4', 5: 'k5'}.get(int(m)) if float(m).is_integer() else None
            if k and k not in f.kinds and f.C != 'C1':
                f.kinds = tuple(f.kinds) + (k,)
    return fams


def deck(items, recycle=True):
    return HE.deck(items, recycle=recycle)


def rows_mcq(C, D, rows, **kw):
    """MCQ family over rows (stem, correct, wrong1, wrong2, wrong3[, key])."""
    d = deck(rows)

    def gen(r):
        row = d(r)
        stem, a, w1, w2, w3 = row[:5]
        key = row[5] if len(row) > 5 else a + '.'
        return mcq(stem, a, [w1, w2, w3], key, r)
    return F(C, D, 'mcq', gen, **kw)


def rows_written(C, D, typ, rows, marks, **kw):
    """Written family over rows (stem, answer[, key])."""
    d = deck(rows)

    def gen(r):
        row = d(r)
        key = row[2] if len(row) > 2 else f'{marks} marks: ' + row[1]
        return {'stem': row[0], 'answer': row[1], 'key': key, 'marks': marks}
    return F(C, D, typ, gen, marks=marks, **kw)


def names_pick(r, n):
    return r.sample(NAMES, n)


# ---------------------------------------------------------------- running code that uses files

def run_files(code: str, files: dict | None = None, setup: str = '') -> str:
    """Run code inside a fresh temporary folder holding the given text files (name -> content); setup code runs first, silently."""
    import os
    import tempfile
    old = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        try:
            for n, c in (files or {}).items():
                with open(n, 'w', newline='\n') as fh:
                    fh.write(c)
            if setup:
                run(setup)
            return run(code)
        finally:
            os.chdir(old)


def run_files_or_err(code, files=None, setup=''):
    try:
        return run_files(code, files, setup)
    except Exception as e:  # noqa: BLE001
        return f'Error ({type(e).__name__})'
