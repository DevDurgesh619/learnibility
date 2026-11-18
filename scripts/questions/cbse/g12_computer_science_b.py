"""CBSE class 12 Computer Science (083), chapters 3-4: file handling and the stack.

File outputs are computed by running the code in a temporary folder that holds the stated file (kit.run_files);
stack traces and postfix values are computed by simulating the stack.
"""
from __future__ import annotations

import random

from qbank import F, mcq, ar
from g12_computer_science_kit import (ST, run, run_files, run_files_or_err, uniq, NAMES, SENTS, WORDS, FUNCS, compiles)

S = 'cbse-g12-computer-science-ch'

LINES = ['The quick brown fox jumps', 'A stitch in time saves nine', 'Python is easy to learn', 'Delhi is the capital of India',
         'Every student must read daily', 'An apple a day keeps the doctor away', 'Trees give us oxygen', 'The sun rises in the east',
         'All that glitters is not gold', 'Honesty is the best policy', 'We love our country', 'Time and tide wait for none',
         'Arjun plays the flute', 'The Ganga flows through Varanasi', 'India won the match', 'Our school has a big library',
         'Today is a sunny day', 'Mumbai is a busy city', 'The exam starts at ten', 'Always wear a helmet']
FNAMES = ['STORY.TXT', 'NOTES.TXT', 'POEM.TXT', 'DIARY.TXT', 'MATTER.TXT', 'ESSAY.TXT', 'Report.txt', 'Data.txt', 'Lines.txt', 'Article.txt']


def content(r, n=None):
    ls = r.sample(LINES, n or r.randint(3, 5))
    return ls, '\n'.join(ls) + '\n'


def show_file(fn, ls):
    return f'The text file "{fn}" contains the following lines (each line ends with a newline character):\n' + '\n'.join(ls)


# ====================================================================== ch03 st1 modes
MODE_SCEN = [
    ('read an existing file of notes without changing it', 'r'), ('create a new file of results, erasing it if it already exists', 'w'),
    ('add new records at the end of an existing log file without erasing it', 'a'), ('read and also update an existing text file, keeping its contents', 'r+'),
    ('write to a file and then read it back, erasing any old contents first', 'w+'), ('read an existing image file byte by byte', 'rb'),
    ('store Python lists in a new binary file using pickle, replacing old data', 'wb'), ('append new pickled records to an existing binary file', 'ab'),
    ('read pickled records and also modify them in place in a binary file', 'rb+'), ('append text to a file and also be able to read it', 'a+'),
]
MODES = ['r', 'w', 'a', 'r+', 'w+', 'a+', 'rb', 'wb', 'ab', 'rb+']


def mode_pick(r):
    task, m = r.choice(MODE_SCEN)
    who = r.choice(NAMES)
    same_kind = [x for x in MODES if x != m and (('b' in x) == ('b' in m))]
    other = [x for x in MODES if x != m]
    wrong = r.sample(same_kind, min(3, len(same_kind)))
    while len(wrong) < 3:
        x = r.choice(other)
        if x not in wrong:
            wrong.append(x)
    return mcq(f'{who} wants to open a file to {task}. Which file mode should be used?', m, wrong, f'Mode "{m}" is used to {task}.', r)


def mode_effect(r):
    fn = r.choice(FNAMES)
    ls, txt = content(r, 3)
    m = r.choice(['w', 'a'])
    add = r.choice(LINES)
    code = f'f = open("{fn}", "{m}")\nf.write("{add}\\n")\nf.close()\nf = open("{fn}")\nprint(len(f.readlines()))\nf.close()'
    ans = run_files(code, {fn: txt})
    alt = run_files(code.replace(f'"{m}"', '"a"' if m == 'w' else '"w"', 1), {fn: txt})
    wrong = uniq([alt, str(len(ls)), str(len(ls) + 2), '0'], [ans])[:3]
    return mcq(f'{show_file(fn, ls)}\nWhat is the output of the following code?\n{code}', ans, wrong,
               f'Mode "{m}" ' + ('erases the old contents, so only one line remains.' if m == 'w' else 'adds the line at the end, so the file has one more line.'), r)


# ====================================================================== ch03 st2 text methods
def text_methods(r):
    fn = r.choice(FNAMES)
    ls, txt = content(r)
    v = r.choice(['f', 'fh', 'myfile', 'F', 'fobj'])
    t = r.randrange(7)
    n = r.randint(4, 14)
    if t == 0:
        body = f'print({v}.read({n}))'
        alts = [f'print({v}.read({n + 1}))', f'print({v}.readline())', f'print({v}.read({n - 1}))']
    elif t == 1:
        body = f'{v}.readline()\nprint({v}.readline().strip())'
        alts = [f'print({v}.readline().strip())', f'{v}.readline()\n{v}.readline()\nprint({v}.readline().strip())', f'print({v}.read(5))']
    elif t == 2:
        i = r.randint(0, len(ls) - 1)
        body = f'L = {v}.readlines()\nprint(len(L), L[{i}].split()[0])'
        alts = [f'L = {v}.readlines()\nprint(len(L) + 1, L[{i}].split()[0])', f'L = {v}.readlines()\nprint(len(L), L[{i}].split()[-1])',
                f'L = {v}.read()\nprint(len(L.split()), L.split()[0])']
    elif t == 3:
        body = f'x = {v}.read({n})\nprint({v}.tell())\n{v}.seek({n // 2})\nprint({v}.read(4))'
        alts = [f'x = {v}.read({n})\nprint({v}.tell() + 1)\n{v}.seek({n // 2})\nprint({v}.read(4))', f'x = {v}.read({n})\nprint({v}.tell())\n{v}.seek({n // 2 + 1})\nprint({v}.read(4))',
                f'x = {v}.read({n})\nprint({v}.tell())\nprint({v}.read(4))']
    elif t == 4:
        body = f'data = {v}.read()\nprint(len(data.split()), len(data.split("\\n")) - 1)'
        alts = [f'data = {v}.read()\nprint(len(data.split()) + 1, len(data.split("\\n")))', f'data = {v}.read()\nprint(len(data), len(data.split("\\n")) - 1)',
                f'data = {v}.readline()\nprint(len(data.split()), 1)']
    elif t == 5:
        body = f'for line in {v}:\n    if line[0] in "AaEeIiOoUu":\n        print(line.strip())'
        alts = [f'for line in {v}:\n    if line[0] not in "AaEeIiOoUu":\n        print(line.strip())', f'print({v}.readline().strip())', f'for line in {v}:\n    print(line.split()[0])']
    else:
        body = f'{v}.seek({n})\nprint({v}.readline().strip())'
        alts = [f'print({v}.readline().strip())', f'{v}.seek({n + 1})\nprint({v}.readline().strip())', f'{v}.seek({n - 1})\nprint({v}.readline().strip())']
    code = f'{v} = open("{fn}", "r")\n{body}\n{v}.close()'
    ans = run_files(code, {fn: txt})
    if not ans.strip():
        raise ValueError('empty')
    wrong = [w for w in uniq([run_files_or_err(f'{v} = open("{fn}", "r")\n{a}\n{v}.close()', {fn: txt}) for a in alts], [ans]) if w.strip() and not w.startswith('Error')]
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'{show_file(fn, ls)}\nWrite the output of the following code:\n{code}', 'answer': ans, 'distractors': wrong,
            'key': f'2 marks for the exact output (read(n) reads n characters, readline() one line, readlines() a list of lines; tell() gives the current position):\n{ans}', 'marks': 2}


def write_count(r):
    fn = r.choice(FNAMES)
    a, b, c = r.sample(LINES, 3)
    code = f'f = open("{fn}", "w")\nn1 = f.write("{a}\\n")\nf.writelines(["{b}\\n", "{c}\\n"])\nf.close()\nf = open("{fn}")\nprint(n1, len(f.read()))\nf.close()'
    ans = run_files(code)
    n1 = len(a) + 1
    tot = n1 + len(b) + len(c) + 2
    wrong = uniq([f'{n1 - 1} {tot}', f'{n1} {tot - 3}', f'None {tot}', f'{n1} {n1}'], [ans])[:3]
    return mcq(f'What is the output of the following code?\n{code}', ans, wrong,
               'write() returns the number of characters written (including \\n); writelines() writes each string of the list; read() returns everything.', r)


# ====================================================================== ch03 st3 processing programs
COUNT_TASKS = [
    ('counts the lines that begin with the letter "{c}"', 'lines', lambda ls, c: sum(1 for l in ls if l[0].upper() == c),
     'def {f}():\n    count = 0\n    with open("{fn}") as F:\n        for line in F:\n            if line[0] in "{c}{cl}":\n                count += 1\n    print("Lines:", count)'),
    ('counts the words "the" (in any case) in the file', 'words', lambda ls, c: sum(1 for l in ls for w in l.split() if w.lower() == 'the'),
     'def {f}():\n    count = 0\n    with open("{fn}") as F:\n        for w in F.read().split():\n            if w.lower() == "the":\n                count += 1\n    print("Count:", count)'),
    ('counts the words that have more than {k} characters', 'words', None,
     'def {f}():\n    count = 0\n    with open("{fn}") as F:\n        for w in F.read().split():\n            if len(w) > {k}:\n                count += 1\n    print("Count:", count)'),
    ('counts the uppercase letters in the file', 'chars', lambda ls, c: sum(1 for l in ls for ch in l if ch.isupper()),
     'def {f}():\n    count = 0\n    with open("{fn}") as F:\n        for ch in F.read():\n            if ch.isupper():\n                count += 1\n    print("Uppercase:", count)'),
    ('counts the vowels in the file', 'chars', lambda ls, c: sum(1 for l in ls for ch in l if ch in 'aeiouAEIOU'),
     'def {f}():\n    count = 0\n    with open("{fn}") as F:\n        for ch in F.read():\n            if ch in "aeiouAEIOU":\n                count += 1\n    print("Vowels:", count)'),
    ('displays the lines that do not begin with "{c}" and counts them', 'lines', lambda ls, c: sum(1 for l in ls if l[0].upper() != c),
     'def {f}():\n    count = 0\n    with open("{fn}") as F:\n        for line in F:\n            if line[0] not in "{c}{cl}":\n                print(line, end="")\n                count += 1\n    print("Lines:", count)'),
    ('displays the words that end with the letter "{e}"', 'words', None,
     'def {f}():\n    with open("{fn}") as F:\n        for w in F.read().split():\n            if w[-1] in "{e}{eu}":\n                print(w, end=" ")'),
    ('displays each line with its words in reverse order', 'lines', None,
     'def {f}():\n    with open("{fn}") as F:\n        for line in F:\n            print(" ".join(line.split()[::-1]))'),
]


def count_out(r):
    fn = r.choice(FNAMES)
    ls, txt = content(r)
    i = r.randrange(len(COUNT_TASKS))
    desc, unit, _, sol = COUNT_TASKS[i]
    c = r.choice(sorted({l[0].upper() for l in ls}))
    e = r.choice(sorted({w[-1].lower() for l in ls for w in l.split()}))
    fill = dict(f=r.choice(['COUNT', 'DISPLAY', 'SHOW', 'COUNTLINES', 'COUNTWORDS', 'PROCESS']) + r.choice(['', '_T', 'IT', 'FILE']),
                fn=fn, c=c, cl=c.lower(), k=r.choice([3, 4, 5]), e=e, eu=e.upper())
    code = sol.format(**fill)
    ans = run_files(code + f'\n{fill["f"]}()', {fn: txt})
    return {'stem': f'{show_file(fn, ls)}\nWrite the output when the following function is called:\n{code}', 'answer': ans,
            'key': f'2 marks for the exact output:\n{ans}', 'marks': 2,
            'distractors': uniq([ans.replace(ans.split()[-1], str(int(ans.split()[-1]) + 1)) if ans.split()[-1].isdigit() else ans + ' ' + ls[0].split()[0],
                                 ans.replace(ans.split()[-1], str(max(0, int(ans.split()[-1]) - 1))) if ans.split()[-1].isdigit() else ls[-1],
                                 ans.replace(ans.split()[-1], str(int(ans.split()[-1]) + 2)) if ans.split()[-1].isdigit() else ls[0]], [ans])}


def count_write(r, marks=3):
    fn = r.choice(FNAMES)
    i = r.randrange(len(COUNT_TASKS))
    desc, _, _, sol = COUNT_TASKS[i]
    c = r.choice('TAESHWIDM')
    e = r.choice('eyst')
    nm = [['COUNTLINES', 'CountL', 'LINES'], ['COUNT_THE', 'CountThe', 'THECOUNT'], ['LONGWORDS', 'CountLong', 'BIGWORDS'], ['UPPERCOUNT', 'CountUpper', 'CAPS'],
          ['VOWELCOUNT', 'CountVowels', 'VOWELS'], ['SHOWLINES', 'NotStarting', 'DISPLAYLINES'], ['ENDWORDS', 'ShowEnd', 'WORDSEND'], ['REVERSE', 'RevWords', 'FLIP']][i]
    fill = dict(f=r.choice(nm) + r.choice(['', '_T', 'IT', 'FILE', '2']),
                fn=fn, c=c, cl=c.lower(), k=r.choice([3, 4, 5, 6]), e=e, eu=e.upper())
    code = sol.format(**fill)
    run_files(code + f'\n{fill["f"]}()', {fn: '\n'.join(LINES[:6]) + '\n'})
    return {'stem': f'Write a function {fill["f"]}() in Python that reads the text file "{fn}" and ' + desc.format(**fill) + '.',
            'answer': code, 'key': f'{marks} marks: opening the file correctly 1, reading/looping 1, correct condition and output {marks - 2}.', 'marks': marks}


def count_mcq(r):
    fn = r.choice(FNAMES)
    ls, txt = content(r)
    t = r.randrange(3)
    if t == 0:
        k = r.choice([3, 4, 5])
        code = f'count = 0\nwith open("{fn}") as f:\n    for w in f.read().split():\n        if len(w) <= {k}:\n            count += 1\nprint(count)'
        alts = [code.replace('<=', '<'), code.replace('<=', '>'), code.replace('f.read().split()', 'f.readline().split()')]
    elif t == 1:
        code = f'n = 0\nwith open("{fn}") as f:\n    for line in f:\n        n += len(line.strip())\nprint(n)'
        alts = [code.replace('.strip()', ''), code.replace('len(line.strip())', 'len(line.split())'), code.replace('n += len(line.strip())', 'n += 1')]
    else:
        ch = r.choice('aeiost')
        code = f'with open("{fn}") as f:\n    data = f.read()\nprint(data.count("{ch}"), data.count("\\n"))'
        alts = [code.replace(f'"{ch}"', f'"{ch.upper()}"'), code.replace('data.count("\\n")', 'len(data.split())'), code.replace(f'data.count("{ch}")', f'data.lower().count("{ch}") + 1')]
    ans = run_files(code, {fn: txt})
    wrong = [w for w in uniq([run_files_or_err(a, {fn: txt}) for a in alts], [ans]) if not w.startswith('Error')]
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'{show_file(fn, ls)}\nWhat is the output of the following code?\n{code}', ans, wrong[:3], f'Tracing the loop gives {ans}.', r)


# ====================================================================== ch03 st4 pickle
REC_KINDS = [
    ('STUDENT.DAT', '[RollNo, Name, Percentage]', lambda r: [[r.randint(1, 60), n, r.randint(40, 99)] for n in r.sample(NAMES, 5)], 2, 'Percentage'),
    ('ITEMS.DAT', '[ItemNo, ItemName, Price]', lambda r: [[r.randint(100, 999), n, r.randint(20, 900)] for n in r.sample(['Pen', 'Pencil', 'Notebook', 'Bag', 'Ruler', 'Eraser', 'Geometry box', 'Marker'], 5)], 2, 'Price'),
    ('EMP.DAT', '[EmpId, Name, Salary]', lambda r: [[r.randint(1, 99), n, r.randint(18, 95) * 1000] for n in r.sample(NAMES, 5)], 2, 'Salary'),
    ('BOOK.DAT', '[BookNo, Title, Pages]', lambda r: [[r.randint(1, 99), n, r.randint(80, 600)] for n in r.sample(['Godan', 'Gitanjali', 'Malgudi Days', 'Wings of Fire', 'Discovery of India', 'Panchatantra', 'Nirmala'], 5)], 2, 'Pages'),
]


def pickle_out(r):
    fn, struct, mk, idx, fld = r.choice(REC_KINDS)
    recs = mk(r)
    k = sorted(x[idx] for x in recs)[r.randint(1, 3)]
    setup = f'import pickle\nf = open("{fn}", "wb")\nfor rec in {recs}:\n    pickle.dump(rec, f)\nf.close()'
    t = r.randrange(2)
    if t == 0:
        code = (f'import pickle\nc = 0\nwith open("{fn}", "rb") as f:\n    try:\n        while True:\n            rec = pickle.load(f)\n            if rec[{idx}] > {k}:\n'
                f'                print(rec[1], end=", ")\n                c += 1\n    except EOFError:\n        print("Total:", c)')
    else:
        code = (f'import pickle\nwith open("{fn}", "rb") as f:\n    rec = pickle.load(f)\n    rec = pickle.load(f)\n    print(rec)')
    ans = run_files(code, setup=setup)
    alts = [code.replace(' > ', ' >= '), code.replace(' > ', ' < '), code.replace('    rec = pickle.load(f)\n    rec = pickle.load(f)', '    rec = pickle.load(f)')]
    wrong = [w for w in uniq([run_files_or_err(a, setup=setup) for a in alts], [ans]) if not w.startswith('Error')]
    wrong = uniq(wrong + [str(recs[0]), str(recs[-1]), 'EOFError'], [ans])
    recs_txt = '\n'.join(str(x) for x in recs)
    return {'stem': f'A binary file "{fn}" has records of the form {struct}, written one after another with pickle.dump(). It contains:\n{recs_txt}\nWrite the output of:\n{code}',
            'answer': ans, 'key': f'2 marks for the exact output:\n{ans}', 'distractors': wrong[:5], 'marks': 2}


PK_TASKS = [
    ('Write a function {f}() that reads the binary file "{fn}" (records {struct}) and displays the records in which {fld} is more than {k}. '
     'Also display the number of such records.',
     'import pickle\ndef {f}():\n    count = 0\n    with open("{fn}", "rb") as F:\n        try:\n            while True:\n                rec = pickle.load(F)\n'
     '                if rec[2] > {k}:\n                    print(rec)\n                    count += 1\n        except EOFError:\n            pass\n    print("Records:", count)'),
    ('Write a function {f}() that accepts a record {struct} from the user and appends it to the binary file "{fn}" using pickle.',
     'import pickle\ndef {f}():\n    a = int(input("Number: "))\n    b = input("Name: ")\n    c = int(input("{fld}: "))\n    with open("{fn}", "ab") as F:\n        pickle.dump([a, b, c], F)'),
    ('Write a function {f}(n) that searches the binary file "{fn}" (records {struct}) for the record whose first field is n and displays it, '
     'or displays "Not found".',
     'import pickle\ndef {f}(n):\n    found = False\n    with open("{fn}", "rb") as F:\n        try:\n            while True:\n                rec = pickle.load(F)\n'
     '                if rec[0] == n:\n                    print(rec)\n                    found = True\n        except EOFError:\n            pass\n    if not found:\n        print("Not found")'),
    ('Write a function {f}() that increases {fld} by {p}% in every record of the binary file "{fn}" (records {struct}). '
     'Read all records into a list, update them and write them back.',
     'import pickle\ndef {f}():\n    recs = []\n    with open("{fn}", "rb") as F:\n        try:\n            while True:\n                recs.append(pickle.load(F))\n'
     '        except EOFError:\n            pass\n    for rec in recs:\n        rec[2] = rec[2] + rec[2] * {p} / 100\n    with open("{fn}", "wb") as F:\n        for rec in recs:\n            pickle.dump(rec, F)'),
    ('Write a function {f}() that copies the records of "{fn}" (records {struct}) whose {fld} is less than {k} into a new binary file "LOW.DAT", '
     'and returns the number of records copied.',
     'import pickle\ndef {f}():\n    n = 0\n    with open("{fn}", "rb") as F, open("LOW.DAT", "wb") as G:\n        try:\n            while True:\n                rec = pickle.load(F)\n'
     '                if rec[2] < {k}:\n                    pickle.dump(rec, G)\n                    n += 1\n        except EOFError:\n            pass\n    return n'),
]


def pickle_task(r, marks=5, which=None):
    fn, struct, mk, idx, fld = r.choice(REC_KINDS)
    i = which if which is not None else r.randrange(len(PK_TASKS))
    stem, sol = PK_TASKS[i]
    recs = mk(r)
    k = sorted(x[2] for x in recs)[2]
    fill = dict(f=r.choice(['SHOW', 'DISPLAY', 'ADDREC', 'SEARCH', 'UPDATE', 'COPYREC', 'countrec', 'Search', 'Update', 'Display']) + r.choice(['', 'REC', 'DATA', '_BIN']),
                fn=fn, struct=struct, fld=fld, k=k, p=r.choice([5, 10, 15, 20]))
    code = sol.format(**fill)
    setup = f'import pickle\nf = open("{fn}", "wb")\nfor rec in {recs}:\n    pickle.dump(rec, f)\nf.close()'
    if i != 1:
        run_files(code + f'\n{fill["f"]}(' + (str(recs[0][0]) if i == 2 else '') + ')', setup=setup)
    else:
        assert compiles(code)
    lead = (f'A binary file "{fn}" stores records of the form {struct}.\n(a) Differentiate between pickle.dump() and pickle.load(). (2)\n(b) ' if marks == 5 else '')
    ans = ('(a) dump() writes (serialises) a Python object to a binary file opened in wb/ab mode; load() reads (deserialises) one object from a file opened in rb mode and raises EOFError at the end.\n(b) '
           if marks == 5 else '') + code
    return {'stem': lead + stem.format(**fill) + (' (3)' if marks == 5 else ''), 'answer': ans,
            'key': (f'{marks} marks: ' + ('(a) 2 marks; (b) ' if marks == 5 else '') + 'import and correct file mode 1, load/dump loop with EOFError 1, condition/update and output 1.'),
            'marks': marks}


# ====================================================================== ch03 st5 csv
CSV_KINDS = [
    ('student.csv', ['Roll', 'Name', 'Marks'], lambda r: [[str(r.randint(1, 50)), n, str(r.randint(30, 99))] for n in r.sample(NAMES, 4)]),
    ('product.csv', ['PID', 'PName', 'Price'], lambda r: [[f'P{r.randint(10, 99)}', n, str(r.randint(50, 999))] for n in r.sample(['Soap', 'Shampoo', 'Toothpaste', 'Oil', 'Biscuit', 'Tea'], 4)]),
    ('furniture.csv', ['FID', 'Item', 'Price'], lambda r: [[str(r.randint(100, 999)), n, str(r.randint(2000, 30000))] for n in r.sample(['Chair', 'Table', 'Sofa', 'Bed', 'Almirah', 'Desk'], 4)]),
    ('books.csv', ['BID', 'Title', 'Price'], lambda r: [[str(r.randint(1, 99)), n, str(r.randint(100, 900))] for n in r.sample(['Godan', 'Gitanjali', 'Malgudi Days', 'Wings of Fire', 'Panchatantra'], 4)]),
]


def csv_out(r):
    fn, head, mk = r.choice(CSV_KINDS)
    rows = mk(r)
    txt = ','.join(head) + '\n' + '\n'.join(','.join(x) for x in rows) + '\n'
    k = sorted(int(x[2]) for x in rows)[r.randint(0, 2)]
    t = r.randrange(3)
    if t == 0:
        code = f'import csv\nwith open("{fn}") as f:\n    R = csv.reader(f)\n    next(R)\n    for row in R:\n        if int(row[2]) > {k}:\n            print(row[1], end=" ")'
        alts = [code.replace('    next(R)\n', ''), code.replace(' > ', ' < '), code.replace('row[1]', 'row[0]')]
    elif t == 1:
        code = f'import csv\nwith open("{fn}") as f:\n    data = list(csv.reader(f))\nprint(len(data), data[1])'
        alts = [code.replace('len(data)', 'len(data) - 1'), code.replace('data[1]', 'data[0]'), code.replace('data[1]', 'data[-1]')]
    else:
        code = f'import csv\ntotal = 0\nwith open("{fn}") as f:\n    R = csv.reader(f)\n    next(R)\n    for row in R:\n        total += int(row[2])\nprint(total)'
        alts = [code.replace('total += int(row[2])', 'total += 1'), code.replace('total = 0', f'total = {rows[0][2]}'), code.replace('total += int(row[2])', 'total = int(row[2])')]
    ans = run_files(code, {fn: txt})
    wrong = [w for w in uniq([run_files_or_err(a, {fn: txt}) for a in alts], [ans]) if w.strip() and not w.startswith('Error')]
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'The CSV file "{fn}" contains:\n{txt.strip()}\nWrite the output of:\n{code}', 'answer': ans, 'distractors': wrong,
            'key': f'2 marks for the exact output:\n{ans}', 'marks': 2}


def csv_written(r):
    fn, head, mk = r.choice(CSV_KINDS)
    rows = mk(r)[:2]
    d = r.choice([',', ';', '|', '#'])
    code = f'import csv\nf = open("{fn}", "w", newline="")\nw = csv.writer(f, delimiter="{d}")\nw.writerow({head})\nw.writerows({rows})\nf.close()'
    from g12_computer_science_kit import run_files as rf
    ans = rf(code + f'\nprint(open("{fn}").read().strip())')
    wrong = [ans.replace(d, ','), ans.replace(d, ' '), '\n'.join(str(x) for x in [head] + rows)]
    if d == ',':
        wrong[0] = ans.replace(',', ';')
    wrong = uniq(wrong, [ans])
    ans1 = ans.replace('\n', ' / ')
    return mcq(f'What will the file "{fn}" contain after the following code runs? (Lines are separated by " / ".)\n{code}', ans1, [w.replace('\n', ' / ') for w in wrong][:3],
               f'writerow() writes one record, writerows() several, each field separated by "{d}".', r)


CSV_TASKS = [
    ('Write a function ADD() to accept a record [{h0}, {h1}, {h2}] from the user and append it to the CSV file "{fn}", and a function COUNTR() '
     'that counts and returns the number of records in the file whose {h2} is more than {k}.',
     'import csv\ndef ADD():\n    a = input("{h0}: ")\n    b = input("{h1}: ")\n    c = input("{h2}: ")\n    with open("{fn}", "a", newline="") as f:\n'
     '        csv.writer(f).writerow([a, b, c])\n\ndef COUNTR():\n    n = 0\n    with open("{fn}") as f:\n        for row in csv.reader(f):\n'
     '            if int(row[2]) > {k}:\n                n += 1\n    return n'),
    ('Write a function SEARCH() that reads the CSV file "{fn}" (fields {h0}, {h1}, {h2}; first line is the header) and displays the {h1} of every record whose '
     '{h2} is between {k} and {k2} (both inclusive), and a function TOTAL() that returns the sum of {h2} of all records.',
     'import csv\ndef SEARCH():\n    with open("{fn}") as f:\n        R = csv.reader(f)\n        next(R)\n        for row in R:\n            if {k} <= int(row[2]) <= {k2}:\n'
     '                print(row[1])\n\ndef TOTAL():\n    s = 0\n    with open("{fn}") as f:\n        R = csv.reader(f)\n        next(R)\n        for row in R:\n            s += int(row[2])\n    return s'),
    ('Write a function CREATE() that writes the header [{h0}, {h1}, {h2}] and three records entered by the user into a new CSV file "{fn}", '
     'and a function SHOW() that displays all records of the file.',
     'import csv\ndef CREATE():\n    with open("{fn}", "w", newline="") as f:\n        w = csv.writer(f)\n        w.writerow(["{h0}", "{h1}", "{h2}"])\n'
     '        for i in range(3):\n            w.writerow([input("{h0}: "), input("{h1}: "), input("{h2}: ")])\n\ndef SHOW():\n    with open("{fn}") as f:\n'
     '        for row in csv.reader(f):\n            print(row)'),
]


def csv_task(r):
    fn, head, mk = r.choice(CSV_KINDS)
    i = r.randrange(len(CSV_TASKS))
    stem, sol = CSV_TASKS[i]
    k = r.choice([50, 100, 200, 500, 60, 75])
    fill = dict(fn=fn, h0=head[0], h1=head[1], h2=head[2], k=k, k2=k * r.choice([2, 3, 4]))
    code = sol.format(**fill)
    assert compiles(code)
    return {'stem': stem.format(**fill), 'answer': code,
            'key': '4 marks: 2 marks for each function (correct mode/newline, writer or reader object, loop and condition).', 'marks': 4}


def csv_case(r):
    who = r.choice(NAMES)
    fn, head, mk = r.choice(CSV_KINDS)
    blanks = ['import csv', f'open("{fn}", "a", newline="")', 'csv.writer(f)', 'w.writerow(rec)']
    code = ('_____ # Statement 1\ndef addrec(rec):\n    f = _____ # Statement 2: open in append mode\n    w = _____ # Statement 3: writer object\n'
            '    _____ # Statement 4: write rec\n    f.close()')
    return {'stem': (f'{who} is writing a program to add records {head} to the CSV file "{fn}". Help by completing the missing statements:\n{code}\n'
                     '(i) Statement 1 (ii) Statement 2 (iii) Statement 3 (iv) Statement 4'),
            'answer': ' '.join(f'({x}) {y}' for x, y in zip(['i', 'ii', 'iii', 'iv'], blanks)), 'key': '1 mark for each statement.', 'marks': 4}


CH03 = [ST(S + '03-st1', 'files, file modes and the with clause', """
T: text file | a file that stores data as human-readable characters, each line ending with an end-of-line (EOL) character
T: binary file | a file that stores data as a stream of bytes in the same format as in memory, not directly human-readable
T: file mode | the string given to open() that tells whether the file is opened for reading, writing or appending, in text or binary form
T: absolute path | the full location of a file starting from the root folder or drive, such as C:\\Users\\Riya\\notes.txt
T: relative path | the location of a file given with respect to the current working folder
T: file object | the object returned by open() through which a program reads or writes a file (also called a file handle)
Q: Which is the default mode of open()? | "r" (read, text) | "w" | "a" | "rb"
Q: Which mode creates a new file and also erases an existing file's contents? | "w" | "a" | "r" | "r+"
Q: Which mode opens a file for appending in binary form? | "ab" | "a" | "wb" | "rb+"
Q: What happens if a file that does not exist is opened in "r" mode? | FileNotFoundError is raised | an empty file is created | the program waits | nothing happens
Q: The with statement for files: | closes the file automatically when the block ends | keeps the file open after the block | works only for binary files | opens two files at once
Q: Which attribute tells whether a file object f has been closed? | f.closed | f.close | f.isclosed() | f.mode
Q: Which of these is an example of a binary file? | an image (.jpg) file | a .txt file | a .csv file | a .py file
S+: The "a" mode places the file pointer at the end of the file
S+: Opening a file in "w" mode erases its existing contents
S+: The close() method frees the resources linked to a file
S+: The "r+" mode opens an existing file for both reading and writing
S+: A CSV file is a text file
S-: The "a" mode raises an error if the file does not exist | "a" creates the file if it does not exist
S-: Binary files can be read easily in a text editor | Binary files store bytes and are not human-readable
S-: The "w" mode adds data at the end of the existing contents | "w" overwrites; "a" appends at the end
C: Data written to a file opened in "w" mode replaces the old data | "w" mode truncates the file to zero length when it is opened
C: Files should be closed after use | closing writes pending (buffered) data to the disk and releases the file
C: A file opened using the with clause need not be closed explicitly | the with clause closes the file automatically when control leaves the block
M:mode: r | open for reading; the file must exist
M:mode: w | open for writing; old contents are erased
M:mode: a | open for appending at the end of the file
M:mode: rb | open a binary file for reading
M:mode: wb | open a binary file for writing
M:mode: r+ | open for reading and writing without erasing
X: C2 D2 2 | Differentiate between text files and binary files. | Text files store characters, are human-readable and lines end with EOL; binary files store bytes as in memory, are not human-readable and have no EOL translation; binary files are faster for records.
X: C2 D3 2 | Differentiate between "w" and "a" modes with an example. | "w" erases the contents (or creates the file) and writes from the start; "a" keeps the contents and writes at the end, e.g. open("log.txt", "a") to add entries.
"""), ST(S + '03-st2', 'reading and writing text files', """
T: read() | a method that reads the whole file, or n characters with read(n), and returns a string
T: readline() | a method that reads one line from the file, including the newline character at its end
T: readlines() | a method that reads all lines of the file and returns them as a list of strings
T: seek() | a method that moves the file pointer to a given byte position, as in f.seek(0)
T: tell() | a method that returns the current position of the file pointer in bytes
Q: Which method returns all lines of a file as a list? | readlines() | readline() | read() | lines()
Q: f.read(5) returns: | the next 5 characters as a string | the first 5 lines | a list of 5 words | 5 bytes as a list
Q: Which method writes a list of strings to a file? | writelines() | write() | dump() | writerow()
Q: f.seek(0) moves the file pointer to: | the beginning of the file | the end of the file | the next line | position 1
Q: write() returns: | the number of characters written | None | True | the written string
Q: readline() returns an empty string when: | the end of the file is reached | the line is blank | the file is closed | the file is in "w" mode
S+: readline() keeps the newline character at the end of the line it returns
S+: write() does not add a newline automatically; "\\n" must be written explicitly
S+: A for loop over a file object reads the file one line at a time
S+: tell() gives the position of the file pointer measured from the beginning of the file
S-: writelines() adds a newline after every string | writelines() writes the strings as they are, with no newline added
S-: read() returns a list of lines | read() returns a string; readlines() returns a list
S-: seek() returns the number of lines read | seek() moves the pointer; tell() reports the position
C: Calling readline() twice returns two different lines | the file pointer moves forward after each read
C: f.write(25) gives TypeError for a text file | write() accepts only a string in text mode
X: C2 D2 2 | Differentiate between readline() and readlines() with an example. | readline() reads one line and returns a string, e.g. "Hello\\n"; readlines() reads all lines and returns a list, e.g. ["Hello\\n", "World\\n"].
X: C2 D3 2 | Differentiate between write() and writelines(). | write(s) writes one string and returns the number of characters; writelines(L) writes every string of a list (or iterable) and returns None; neither adds newlines.
"""), ST(S + '03-st3', 'text file processing', """
T: split() | a string method that breaks a line into a list of words at whitespace
T: strip() | a string method that removes leading and trailing whitespace, including the newline character
T: EOL character | the end-of-line character "\\n" that marks the end of each line in a text file
Q: To count the words in a text file, the content is usually: | read and split into a list of words | read with seek() | read with tell() | dumped with pickle
Q: Which statement counts the lines of a text file f? | len(f.readlines()) | len(f.read()) | f.count() | len(f.readline())
Q: To check whether a line starts with "T" or "t", one can test: | line[0] in "Tt" | line[-1] == "T" | line.endswith("t") | line.find("T") == -1
Q: len(f.read()) gives the number of: | characters in the file | words in the file | lines in the file | bytes of the program
S+: The newline character is counted as a character when the length of a line is found
S+: Words separated by spaces can be obtained using the split() method
S+: line.strip() removes the newline character at the end of the line
S-: len(f.read()) gives the number of words in a file | It gives the number of characters; split() is needed to count words
S-: split() returns a string | split() returns a list of words
C: Counting characters with len(line) gives one more than the visible letters of each line | the newline character at the end is also counted
X: C3 D3 3 | Write a function COUNT_ME() that counts and displays how many times the words "Me" and "My" (any case) occur in "STORY.TXT". | Open STORY.TXT in read mode (with clause), read the whole text, convert it to lower case and split it into words; display words.count("me") and words.count("my") with labels.
"""), ST(S + '03-st4', 'binary files and pickle', """
T: pickling | converting a Python object into a byte stream so that it can be written to a binary file (serialisation)
T: unpickling | converting a byte stream read from a binary file back into a Python object (de-serialisation)
T: pickle.dump() | the function that writes a Python object to a binary file opened in write or append mode
T: pickle.load() | the function that reads one Python object from a binary file opened in read mode
Q: Which module is used to store Python objects in a binary file? | pickle | csv | os | binary
Q: pickle.load() raises which exception when the end of the file is reached? | EOFError | IndexError | KeyError | StopIteration
Q: In which mode should a binary file be opened before using pickle.dump() to add records at the end? | "ab" | "rb" | "r" | "a+"
Q: The correct syntax to write an object L to file object F is: | pickle.dump(L, F) | pickle.dump(F, L) | F.dump(L) | pickle.write(L, F)
Q: To update a record in a binary file, a program usually: | reads the records, changes the required one and writes them back | uses writerow() | uses seek(-1) only | deletes the file
S+: pickle can store lists, tuples and dictionaries in a binary file
S+: Each call to pickle.load() reads the next object from the file
S+: A while True loop with try…except EOFError is used to read all records of a binary file
S+: The first argument of pickle.dump() is the object and the second is the file object
S-: pickle.load() reads all records of the file at once | Each call reads only one object
S-: pickle.dump() needs the file to be opened in "r" mode | It needs "wb" or "ab" mode
S-: Binary files written with pickle can be read with readlines() | They must be read with pickle.load()
C: A loop reading a pickled file must handle EOFError | load() raises EOFError when no more objects are left
C: A binary file is opened in "rb+" mode for updating records in place | it allows both reading and writing without erasing the file
X: C2 D2 2 | What is pickling and unpickling? Name the functions used for each. | Pickling: object → byte stream, pickle.dump(); unpickling: byte stream → object, pickle.load().
"""), ST(S + '03-st5', 'CSV files', """
T: CSV file | a comma-separated values file, a text file in which each line is a record and fields are separated by a delimiter such as a comma
T: delimiter | the character that separates the fields of a record in a CSV file
T: csv.writer() | the function that returns a writer object for writing records to a CSV file
T: csv.reader() | the function that returns a reader object that gives each record of a CSV file as a list of strings
T: writerows() | the writer method that writes several records (a list of lists) at once
Q: Which method writes one record to a CSV file? | writerow() | writerows() | write() | dump()
Q: Each row returned by csv.reader() is a: | list of strings | tuple of integers | dictionary | single string
Q: Why is newline="" used when opening a CSV file for writing? | to avoid extra blank lines between records | to add a header | to make the file binary | to separate fields
Q: The default delimiter of the csv module is: | comma (,) | semicolon (;) | tab | space
Q: Which statement creates a writer object w for file f with delimiter ";"? | w = csv.writer(f, delimiter=";") | w = csv.write(f, ";") | w = f.writer(";") | w = csv.writer(";", f)
S+: CSV files can be opened in spreadsheet software such as a spreadsheet program
S+: Numbers read with csv.reader() are strings and must be converted with int() or float()
S+: A CSV file is a text file and can be opened in a text editor
S+: The first row of a CSV file is often a header that names the fields
S-: csv.reader() returns each value as an integer | Every field is returned as a string
S-: writerow() can write only one field | writerow() writes one record with all its fields
S-: A CSV file must be opened in binary mode | It is a text file, opened in text mode with newline=""
C: int(row[2]) is used while summing marks read from a CSV file | csv.reader() returns every field as a string
C: next(reader) is called before the loop in many CSV programs | it skips the header row
X: C2 D2 2 | Differentiate between writerow() and writerows(). | writerow(rec) writes one record (a list); writerows(recs) writes many records (a list of lists) in one call.
""")]


# ====================================================================== ch04 stack
def push_pop(r):
    v = r.choice(['stack', 'S', 'stk', 'St', 'books', 'plates'])
    ops = []
    st = []
    out = []
    vals = r.sample(range(1, 99), 8)
    vi = 0
    for _ in range(r.randint(6, 8)):
        if st and r.random() < 0.4:
            ops.append(f'print({v}.pop(), end=" ")')
            out.append(str(st.pop()))
        else:
            ops.append(f'{v}.append({vals[vi]})')
            st.append(vals[vi])
            vi += 1
    if not out:
        raise ValueError('no pop')
    code = f'{v} = []\n' + '\n'.join(ops) + f'\nprint({v})'
    ans = run(code)
    q = [x for x in ops if 'append' in x]
    wrong = [' '.join(out) + ' ' + str(list(reversed(st))), ' '.join(reversed(out)) + ' ' + str(st)]
    fifo = []
    fo = []
    for o in ops:
        if 'append' in o:
            fifo.append(int(o.split('(')[1].rstrip(')')))
        else:
            fo.append(str(fifo.pop(0)))
    wrong.append(' '.join(fo) + ' ' + str(fifo))
    wrong.append(' '.join(out[:-1]) + ' ' + str(st + [int(out[-1])]))
    wrong = uniq(wrong, [ans.replace('\n', ' ')])
    return {'stem': f'A stack is implemented using a Python list (top = end of the list). Write the output of:\n{code}', 'answer': ans,
            'key': f'2 marks: pop() removes the most recently pushed element (LIFO). Output: {ans}', 'distractors': wrong, 'marks': 2}


def stack_trace(r):
    vals = r.sample(range(10, 99), 6)
    ops = []
    st = []
    for x in vals:
        st.append(x)
        ops.append(f'PUSH({x})')
        if r.random() < 0.35 and st:
            st.pop()
            ops.append('POP()')
    ops += ['POP()'] * r.randint(0, 2)
    st2 = []
    popped = []
    for o in ops:
        if o.startswith('PUSH'):
            st2.append(int(o[5:-1]))
        else:
            if not st2:
                raise ValueError('underflow')
            popped.append(st2.pop())
    top = st2[-1] if st2 else None
    ans = f'{st2} (top = {top})' if st2 else 'Empty stack'
    wrong = uniq([f'{st2[::-1]} (top = {st2[0] if st2 else None})', f'{sorted(st2)} (top = {max(st2) if st2 else None})',
                  f'{(st2 + popped[-1:])} (top = {popped[-1] if popped else None})', f'{vals} (top = {vals[-1]})'], [ans])
    return mcq(f'An empty stack undergoes the operations: {", ".join(ops)}. What does the stack contain at the end (bottom → top)?', ans, wrong[:3],
               f'Each POP removes the element pushed most recently. Final stack: {ans}.', r)


def under_over(r):
    n = r.randint(3, 5)
    pushes = r.randint(1, n + 2)
    pops = r.randint(0, n + 2)
    lines = [f'PUSH({x})' for x in r.sample(range(1, 50), pushes)]
    res = 'no error'
    size = 0
    seq = []
    for i in range(max(pushes, 1)):
        seq.append(lines[i])
    seq += ['POP()'] * pops
    for o in seq:
        if o.startswith('PUSH'):
            if size == n:
                res = 'Overflow'
                break
            size += 1
        else:
            if size == 0:
                res = 'Underflow'
                break
            size -= 1
    opts = ['Overflow', 'Underflow', 'no error']
    ans = {'Overflow': 'Overflow occurs', 'Underflow': 'Underflow occurs', 'no error': 'No overflow or underflow occurs'}[res]
    wrong = [x for x in ['Overflow occurs', 'Underflow occurs', 'No overflow or underflow occurs', 'Both overflow and underflow occur'] if x != ans]
    return mcq(f'A stack can hold at most {n} elements and is initially empty. The operations {", ".join(seq)} are performed in this order. Which statement is correct?',
               ans, wrong, f'Tracking the size (max {n}): {ans.lower()}.', r)


STK_TASKS = [
    ('Write a function PUSH_{nm}(Arr, Stk) that pushes all the numbers of the list Arr that are divisible by {k} onto the stack Stk, and a function POP_{nm}(Stk) '
     'that pops and returns the top element, or displays "Stack Empty" and returns None when the stack is empty.',
     'def PUSH_{nm}(Arr, Stk):\n    for x in Arr:\n        if x % {k} == 0:\n            Stk.append(x)\n\ndef POP_{nm}(Stk):\n    if len(Stk) == 0:\n        print("Stack Empty")\n        return None\n    return Stk.pop()',
     'S = []\nPUSH_{nm}([10, 15, 21, 30], S)\nprint(POP_{nm}(S))'),
    ('A dictionary D stores names of {who} and their {what}. Write a function PUSH(D, Stk) that pushes onto the stack Stk the names whose {what} is more than {k}, '
     'and a function POPALL(Stk) that pops and displays all names, then displays "Stack Empty".',
     'def PUSH(D, Stk):\n    for name in D:\n        if D[name] > {k}:\n            Stk.append(name)\n\ndef POPALL(Stk):\n    while Stk:\n        print(Stk.pop(), end=" ")\n    print("Stack Empty")',
     'S = []\nPUSH({{"A": 1, "B": 999999}}, S)\nPOPALL(S)'),
    ('Each record of a list is [{f1}, {f2}]. Write functions Push_rec(L, Stk) that pushes [{f1}] of records with {f2} less than {k} onto Stk, '
     'Pop_rec(Stk) that pops and displays the records until the stack is empty, and Peek(Stk) that displays the top record without removing it.',
     'def Push_rec(L, Stk):\n    for rec in L:\n        if rec[1] < {k}:\n            Stk.append([rec[0]])\n\ndef Pop_rec(Stk):\n    while len(Stk) > 0:\n        print(Stk.pop())\n    print("Stack Empty")\n\n'
     'def Peek(Stk):\n    if Stk:\n        print(Stk[-1])\n    else:\n        print("Stack Empty")',
     'S = []\nPush_rec([["X", 1]], S)\nPeek(S)\nPop_rec(S)'),
]


def stack_task(r, marks=3):
    i = r.randrange(len(STK_TASKS))
    stem, sol, test = STK_TASKS[i]
    who, what = r.choice([('students', 'marks'), ('employees', 'salary'), ('players', 'runs'), ('cities', 'population (in lakh)'), ('items', 'price')])
    f1, f2 = r.choice([('Name', 'Price'), ('City', 'Rainfall'), ('Book', 'Pages'), ('Player', 'Age'), ('Item', 'Stock')])
    fill = dict(nm=r.choice(['ODD', 'EVEN', 'NUM', 'Div', 'MUL', 'SEL']), k=r.choice([3, 5, 7, 75, 50, 90, 25]), who=who, what=what, f1=f1, f2=f2)
    code = sol.format(**fill)
    run(code + '\n' + test.format(**fill))
    return {'stem': stem.format(**fill), 'answer': code, 'key': f'{marks} marks: push function {marks // 2 + marks % 2}, pop/peek function with empty check {marks // 2}.', 'marks': marks}


# postfix / infix
PREC = {'+': 1, '-': 1, '*': 2, '/': 2}


def to_postfix(tokens):
    out, st = [], []
    for t in tokens:
        if t.isalnum():
            out.append(t)
        elif t == '(':
            st.append(t)
        elif t == ')':
            while st[-1] != '(':
                out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and PREC[st[-1]] >= PREC[t]:
                out.append(st.pop())
            st.append(t)
    while st:
        out.append(st.pop())
    return out


def rand_infix(r, n_ops):
    letters = r.sample('ABCDEFGHJKMNPQRSTUVWXYZ', n_ops + 1)
    toks = [letters[0]]
    for i in range(n_ops):
        toks += [r.choice('+-*/'), letters[i + 1]]
    if r.random() < 0.7:
        i = r.randrange(0, n_ops) * 2
        j = r.randrange(i + 2, len(toks), 2)
        toks = toks[:i] + ['('] + toks[i:j + 1] + [')'] + toks[j + 1:]
    return toks


def infix_postfix(r):
    toks = rand_infix(r, r.randint(3, 4))
    good = ' '.join(to_postfix(toks))
    plain = [t for t in toks if t not in '()']
    lr = []
    opr = []
    for t in plain:
        if t.isalnum():
            lr.append(t)
        else:
            opr.append(t)
    wrong = [' '.join(lr + opr), ' '.join(lr + opr[::-1]), ' '.join(to_postfix(plain))]
    sw = to_postfix(toks)
    ops_i = [i for i, t in enumerate(sw) if not t.isalnum()]
    if len(ops_i) >= 2:
        a, b = ops_i[0], ops_i[-1]
        sw2 = sw[:]
        sw2[a], sw2[b] = sw2[b], sw2[a]
        wrong.append(' '.join(sw2))
    wrong = uniq(wrong, [good])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'Convert the infix expression {"".join(toks)} into postfix form using a stack.', good, wrong[:3],
               '* and / have higher precedence than + and −; operators of equal precedence are applied left to right; brackets first. Postfix: ' + good, r)


def infix_trace(r):
    toks = rand_infix(r, r.randint(3, 5))
    out, st, steps = [], [], []
    for t in toks:
        if t.isalnum():
            out.append(t)
        elif t == '(':
            st.append(t)
        elif t == ')':
            while st[-1] != '(':
                out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and PREC[st[-1]] >= PREC[t]:
                out.append(st.pop())
            st.append(t)
        steps.append(f'{t}: stack [{" ".join(st)}], postfix {"".join(out)}')
    while st:
        out.append(st.pop())
    steps.append(f'end: pop remaining, postfix {"".join(out)}')
    return {'stem': f'Convert the infix expression {"".join(toks)} to postfix, showing the stack status after each symbol is scanned.',
            'answer': '\n'.join(steps) + f'\nPostfix: {" ".join(out)}',
            'key': '3 marks: 2 marks for the stack status table, 1 mark for the final postfix expression ' + ' '.join(out) + '.', 'marks': 3}


def rand_postfix(r, n_ops):
    """Random integer postfix expression whose evaluation (with / exact) stays integral."""
    for _ in range(200):
        stack = []
        toks = []
        nums_left = n_ops + 1
        ops_left = n_ops
        while nums_left or ops_left:
            if nums_left and (len(stack) < 2 or (ops_left and r.random() < 0.45) or not ops_left):
                if not nums_left:
                    break
                v = r.randint(2, 9)
                stack.append(v)
                toks.append(str(v))
                nums_left -= 1
            else:
                b, a = stack.pop(), stack.pop()
                op = r.choice('+-*/')
                if op == '/' and (b == 0 or a % b):
                    op = r.choice('+*-')
                v = {'+': a + b, '-': a - b, '*': a * b, '/': a // b if b else 0}[op]
                stack.append(v)
                toks.append(op)
                ops_left -= 1
        if len(stack) == 1 and len(toks) == 2 * n_ops + 1:
            return toks, stack[0]
    raise ValueError('postfix')


def eval_trace(toks):
    st, steps = [], []
    for t in toks:
        if t.isdigit():
            st.append(int(t))
        else:
            b, a = st.pop(), st.pop()
            st.append({'+': a + b, '-': a - b, '*': a * b, '/': a // b}[t])
        steps.append(f'{t}: {st}')
    return st[0], steps


def postfix_eval(r):
    toks, val = rand_postfix(r, r.randint(3, 4))
    v, _ = eval_trace(toks)
    assert v == val
    st = []
    for t in toks:
        if t.isdigit():
            st.append(int(t))
        else:
            b, a = st.pop(), st.pop()
            st.append({'+': b + a, '-': b - a, '*': b * a, '/': b // a if a else 0}[t])
    wrong = uniq([str(st[0]), str(val + r.randint(1, 5)), str(val - r.randint(1, 5)), str(-val) if val else '1'], [str(val)])
    return mcq(f'Evaluate the postfix expression using a stack: {" ".join(toks)}', str(val), wrong[:3],
               f'Push operands; for each operator pop two values (second popped is the left operand). Result: {val}.', r)


def postfix_trace(r):
    toks, val = rand_postfix(r, r.randint(4, 5))
    _, steps = eval_trace(toks)
    return {'stem': f'Evaluate the following postfix expression using a stack, showing the stack contents after each symbol is scanned: {" ".join(toks)}',
            'answer': '\n'.join(steps) + f'\nResult = {val}', 'key': f'3 marks: 2 marks for the correct stack trace, 1 mark for the result {val}.', 'marks': 3}


def balanced(r):
    def rnd(depth=0):
        s = ''
        for _ in range(r.randint(1, 2)):
            o, c = r.choice([('(', ')'), ('[', ']'), ('{', '}')])
            inner = rnd(depth + 1) if depth < 2 and r.random() < 0.6 else r.choice(['a', 'b+c', 'x*y', '2'])
            s += o + inner + c
        return s
    good = rnd()

    def is_bal(s):
        st = []
        pairs = {')': '(', ']': '[', '}': '{'}
        for ch in s:
            if ch in '([{':
                st.append(ch)
            elif ch in pairs:
                if not st or st.pop() != pairs[ch]:
                    return False
        return not st
    bads = set()
    br = [i for i, ch in enumerate(good) if ch in '()[]{}']
    for _ in range(40):
        s = list(good)
        k = r.randrange(3)
        i = r.choice(br)
        if k == 0:
            s[i] = {'(': '[', '[': '{', '{': '(', ')': ']', ']': '}', '}': ')'}[s[i]]
        elif k == 1:
            del s[i]
        else:
            j = r.choice(br)
            s[i], s[j] = s[j], s[i]
        s = ''.join(s)
        if not is_bal(s):
            bads.add(s)
    if len(bads) < 3 or not is_bal(good):
        raise ValueError('few')
    want_bal = r.random() < 0.5
    if want_bal:
        return mcq('Using a stack to match brackets, which of the following expressions has balanced brackets?', good, r.sample(sorted(bads), 3),
                   f'{good}: every closing bracket matches the bracket on top of the stack and the stack is empty at the end.', r)
    goods = {good}
    for _ in range(20):
        goods.add(rnd())
    goods = [g for g in goods if g != good][:2] + [good]
    bad = r.choice(sorted(bads))
    if len(set(goods)) < 3:
        raise ValueError('few')
    return mcq('Using a stack to match brackets, which of the following expressions does NOT have balanced brackets?', bad, goods,
               f'{bad}: a closing bracket does not match the top of the stack, or brackets are left over.', r)


def reverse_stack(r):
    w = r.choice(WORDS + [s.split()[0] for s in SENTS])
    f = r.choice(FUNCS)
    t = r.randrange(2)
    if t == 0:
        code = f'def {f}(s):\n    stk = []\n    for ch in s:\n        stk.append(ch)\n    r = ""\n    while stk:\n        r += stk.pop()\n    return r\n\nprint({f}("{w}"))'
    else:
        code = (f'def {f}(s):\n    stk = []\n    for word in s.split():\n        stk.append(word)\n    r = []\n    while stk:\n        r.append(stk.pop())\n    return " ".join(r)\n\n'
                f'print({f}("{r.choice(SENTS)}"))')
    ans = run(code)
    alt = [code.replace('stk.pop()', 'stk.pop(0)'), code.replace('r += stk.pop()', 'r = stk.pop() + r')]
    from g12_computer_science_kit import run_or_err
    wrong = uniq([run_or_err(a) for a in alt] + [ans.upper(), ans.lower(), ans[1:] + ans[0]], [ans])
    return {'stem': f'Write the output of the following code that uses a stack:\n{code}', 'answer': ans,
            'key': f'1 mark: the stack reverses the order. Output: {ans}', 'distractors': wrong, 'marks': 1}


def stack_case(r):
    who = r.choice(NAMES)
    toks, val = rand_postfix(r, 3)
    _, steps = eval_trace(toks)
    return {'stem': (f'{who}\'s teacher asks her to evaluate the postfix expression {" ".join(toks)} using a stack implemented as a Python list.\n'
                     '(i) Which list methods implement push and pop? (1)\n(ii) Which data structure principle does the stack follow? (1)\n'
                     '(iii) Show the stack after each symbol and give the final value. (2)'),
            'answer': '(i) append() for push, pop() for pop (ii) LIFO – last in, first out (iii) ' + '; '.join(steps) + f'; value = {val}',
            'key': '1 + 1 + 2 marks.', 'marks': 4}


CH04 = [ST(S + '04-st1', 'the stack data structure', """
T: stack | a linear data structure in which elements are added and removed only at one end, called the top
T: LIFO | last in, first out: the element inserted last is the first to be removed
T: top | the end of a stack at which insertion and deletion take place
T: data structure | a way of storing and organising data in memory so that it can be used efficiently
Q: A stack follows the principle: | LIFO | FIFO | FILO-by-index | random access
Q: Which of these is an application of a stack? | the undo operation in a text editor | a ticket queue at a counter | printing jobs in order of arrival | a list of students in roll number order
Q: The end of a stack where elements are inserted and deleted is called the: | top | front | rear | base
Q: Which of these is a real-life example of a stack? | a pile of plates in a canteen | people waiting at a bus stop | cars at a toll plaza | a playlist played from the start
Q: In a web browser, the Back button behaves like a: | stack | queue | tree | dictionary
Q: Which of these is a linear data structure? | stack | tree | graph | network
S+: In a stack, insertion and deletion happen at the same end
S+: Function calls in a program are managed using a stack
S+: A stack is used to reverse a string
S+: A stack is used to check whether the brackets of an expression are balanced
S-: A stack follows the FIFO principle | A stack follows LIFO; a queue follows FIFO
S-: In a stack, elements can be removed from both ends | Elements are removed only from the top
S-: The element inserted first is removed first from a stack | The element inserted last is removed first
C: The undo feature of an editor can be implemented with a stack | the most recent action has to be undone first
C: A stack is useful for reversing a sequence | the last element pushed is the first one popped
X: C2 D2 2 | Give two real-life and two computer applications of a stack. | Real life: pile of plates, stack of books; computer: undo/redo, browser back button, function calls, expression evaluation, bracket matching (any two each).
"""), ST(S + '04-st2', 'push and pop operations', """
T: PUSH | the operation that inserts a new element at the top of a stack
T: POP | the operation that removes and returns the element at the top of a stack
T: overflow | the situation when an element is pushed onto a stack that is already full
T: underflow | the situation when a pop is attempted on an empty stack
T: peek | the operation that returns the top element of a stack without removing it
Q: In a Python list used as a stack, the PUSH operation is done with: | append() | insert(0, x) | pop(0) | extend()
Q: Popping from an empty Python list gives: | IndexError | ValueError | None | 0
Q: Which statement returns the top element of stack S (a non-empty list) without removing it? | S[-1] | S.pop() | S[0] | S.pop(0)
Q: Trying to delete from an empty stack is called: | underflow | overflow | peek | traversal
Q: Overflow in a stack occurs when: | an element is pushed onto a full stack | an element is popped from an empty stack | the stack has one element | the top is 0
S+: An empty stack must be checked for before a pop operation
S+: len(S) == 0 can be used to check whether a list S used as a stack is empty
S+: A Python list grows dynamically, so overflow rarely occurs in a list-based stack
S-: pop(0) removes the top element of a list-based stack whose top is the end of the list | pop() (last element) removes the top; pop(0) removes the bottom
S-: Overflow occurs when popping from an empty stack | That is underflow; overflow is pushing onto a full stack
C: The function that pops must first check whether the stack is empty | popping an empty list raises IndexError (underflow)
C: S.append(x) is used for PUSH when the end of the list is the top | append() adds x at the end of the list
X: C2 D3 2 | Differentiate between overflow and underflow in a stack. | Overflow: PUSH on a full stack; underflow: POP (or PEEK) on an empty stack.
"""), ST(S + '04-st3', 'applications of the stack', """
T: infix expression | an expression in which the operator is written between its operands, such as A + B
T: postfix expression | an expression in which the operator is written after its operands, such as A B +; also called reverse Polish notation
T: prefix expression | an expression in which the operator is written before its operands, such as + A B
Q: The postfix form of A + B * C is: | A B C * + | A B + C * | A + B C * | + A * B C
Q: While evaluating a postfix expression, when an operator is scanned the stack: | pops two operands, applies the operator and pushes the result | pushes the operator | pops one operand | is emptied
Q: Postfix expressions do not need: | brackets | operands | operators | a stack for evaluation
Q: While converting infix to postfix, operands are: | sent directly to the output | pushed on the stack | discarded | reversed
S+: In postfix notation the order of operations is fixed by the position of operators, so brackets are not needed
S+: When converting infix to postfix, a left bracket is pushed onto the stack
S+: Bracket matching uses a stack: an opening bracket is pushed and a closing bracket pops the matching one
S-: Postfix expressions need brackets to show precedence | Postfix needs no brackets
S-: While evaluating postfix, operands are written to the output and operators are pushed | Operands are pushed; an operator pops two operands
C: Compilers convert infix expressions to postfix | postfix expressions can be evaluated in one left-to-right scan using a stack, without brackets
X: C3 D3 3 | Write an algorithm to evaluate a postfix expression using a stack. | Scan left to right; push operands; on an operator pop two values (B then A), compute A op B and push; at the end the single value on the stack is the result.
""")]


def fams_ch03_04():
    E = {}
    E[S + '03-st1'] = [F('C2', 'D2', 'mcq', mode_pick), F('C3', 'D3', 'mcq', mode_effect), F('C1', 'D1', 'mcq', mode_pick), F('C3', 'D4', 'mcq', mode_effect, gap='G5'),
                       F('C4', 'D4', 'case', csv_case, marks=4, gap='G7')]
    E[S + '03-st2'] = [F('C2', 'D3', 'short', text_methods, marks=2), F('C3', 'D3', 'short', text_methods, marks=2), F('C3', 'D4', 'short', text_methods, marks=2, gap='G5'),
                       F('C2', 'D2', 'mcq', write_count), F('C4', 'D3', 'multi_step', lambda r: count_write(r, 3), marks=3)]
    E[S + '03-st3'] = [F('C3', 'D3', 'short', count_out, marks=2), F('C3', 'D2', 'mcq', count_mcq), F('C4', 'D3', 'multi_step', lambda r: count_write(r, 3), marks=3),
                       F('C4', 'D4', 'multi_step', lambda r: count_write(r, 3), marks=3), F('C3', 'D4', 'mcq', count_mcq, gap='G5'), F('C2', 'D3', 'short', count_out, marks=2)]
    E[S + '03-st4'] = [F('C3', 'D3', 'short', pickle_out, marks=2), F('C4', 'D4', 'long', lambda r: pickle_task(r, 5), marks=5), F('C4', 'D3', 'multi_step', lambda r: pickle_task(r, 3), marks=3),
                       F('C4', 'D5', 'long', lambda r: pickle_task(r, 5, which=3), marks=5), F('C3', 'D4', 'short', pickle_out, marks=2, gap='G5')]
    E[S + '03-st5'] = [F('C3', 'D3', 'short', csv_out, marks=2), F('C2', 'D3', 'mcq', csv_written), F('C4', 'D4', 'explain', csv_task, marks=4),
                       F('C4', 'D3', 'case', csv_case, marks=4, gap='G7'), F('C3', 'D4', 'short', csv_out, marks=2, gap='G5')]
    E[S + '04-st1'] = []
    E[S + '04-st2'] = [F('C2', 'D3', 'short', push_pop, marks=2), F('C3', 'D2', 'mcq', stack_trace), F('C3', 'D3', 'mcq', under_over),
                       F('C4', 'D3', 'multi_step', lambda r: stack_task(r, 3), marks=3), F('C4', 'D4', 'multi_step', lambda r: stack_task(r, 3), marks=3), F('C3', 'D4', 'mcq', stack_trace, gap='G5'),
                       F('C1', 'D1', 'mcq', under_over)]
    E[S + '04-st3'] = [F('C2', 'D2', 'mcq', infix_postfix), F('C3', 'D3', 'mcq', postfix_eval), F('C3', 'D4', 'multi_step', infix_trace, marks=3, gap='G5'),
                       F('C4', 'D3', 'multi_step', postfix_trace, marks=3), F('C3', 'D3', 'mcq', balanced), F('C2', 'D3', 'short', reverse_stack, marks=1),
                       F('C4', 'D4', 'case', stack_case, marks=4, gap='G7'), F('C4', 'D5', 'multi_step', infix_trace, marks=3)]
    E[S + '04-st1'] = [F('C3', 'D3', 'mcq', stack_trace), F('C2', 'D2', 'short', reverse_stack, marks=1), F('C4', 'D4', 'case', stack_case, marks=4, gap='G7'),
                       F('C3', 'D4', 'mcq', balanced, gap='G5')]
    return [CH03, CH04], E
