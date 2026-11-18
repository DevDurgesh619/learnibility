"""CBSE class 12 Computer Science (083), chapters 1-2: Python revision, functions, exception handling.

Every output, exception name and possible-output answer is computed by running the snippet (kit.run / kit.exc).
"""
from __future__ import annotations

import itertools
import random

from qbank import F, mcq, ar
from g12_computer_science_kit import (ST, run, exc, run_or_err, out_item, uniq, VARS, FUNCS, WORDS, SENTS, NAMES,
                                      compiles, rows_mcq, rows_written, deck)

S = 'cbse-g12-computer-science-ch'


# ====================================================================== ch01 st1 revision
def expr_eval(r):
    t = r.randrange(6)
    a, b, c, d, e = (r.randint(2, 9) for _ in range(5))
    if t == 0:
        ex = f'{a} + {b} * {c} ** 2 // {d} - {e}'
        wr = [f'(({a} + {b}) * {c}) ** 2 // {d} - {e}', f'{a} + ({b} * {c}) ** 2 // {d} - {e}', f'{a} + {b} * {c} ** 2 / {d} - {e}']
    elif t == 1:
        ex = f'{a * 3 + 1} % {b} * {c} + {d * 5} // {e}'
        wr = [f'{a * 3 + 1} % ({b} * {c}) + {d * 5} // {e}', f'({a * 3 + 1} % {b} * {c} + {d * 5}) // {e}', f'{a * 3 + 1} % {b} * {c} + {d * 5} / {e}']
    elif t == 2:
        a, b, c = r.choice([2, 3]), r.choice([1, 2]), r.choice([2, 3])
        ex = f'{a} ** {b} ** {c}'
        wr = [f'({a} ** {b}) ** {c}', f'{a} * {b} * {c}', f'{a} ** ({b} * {c}) + 1']
    elif t == 3:
        ex = f'{a} > {b} and {c} < {d} or not {e} == {a}'
        wr = [f'not ({a} > {b} and {c} < {d} or not {e} == {a})']
        out = run(f'print({ex})')
        w = ['True' if out == 'False' else 'False', 'Error', str(int(out == 'True'))]
        return mcq(f'What will be the output of the following Python statement?\nprint({ex})', out, w,
                   f'not is evaluated first, then and, then or; the expression is {out}.', r)
    elif t == 4:
        x, y = r.randint(20, 99), r.randint(3, 9)
        ex = f'{x} // {y} * {y} + {x} % {y} - {x} // {y}'
        wr = [f'{x} // ({y} * {y}) + {x} % {y} - {x} // {y}', f'{x} / {y} * {y} + {x} % {y} - {x} // {y}', f'({x} // {y} * {y} + {x}) % {y} - {x} // {y}']
    else:
        x = r.randint(10, 60)
        ex = f'{x} - {a} * {b} / {c} + {d} // {e}'
        wr = [f'({x} - {a}) * {b} / {c} + {d} // {e}', f'{x} - {a} * {b} // {c} + {d} // {e}', f'({x} - {a} * {b}) / ({c} + {d}) // {e}']
    out = run(f'print({ex})')
    wrong = uniq([run_or_err(f'print({w})') for w in wr], [out])
    wrong = [w for w in wrong if not w.startswith('Error')]
    pad = [str(int(float(out)) + 1), str(int(float(out)) - 1), str(int(float(out)) + 2), str(float(out) + 0.5)]
    wrong = uniq(wrong + pad, [out])[:3]
    return mcq(f'What will be the output of the following Python statement?\nprint({ex})', out, wrong,
               f'Precedence: ** (right to left), then *, /, //, % (left to right), then + and −. Result: {out}.', r)


def slicing(r):
    s = r.choice(WORDS + SENTS)
    n = len(s)
    t = r.randrange(6)
    a, b = sorted(r.sample(range(0, n), 2))
    k = r.choice([2, 3])
    if t == 0:
        e, w = f's[{a}:{b}]', [f's[{a}:{b + 1}]', f's[{a + 1}:{b + 1}]', f's[{max(a - 1, 0)}:{b}]']
    elif t == 1:
        m = r.randint(2, min(6, n - 1))
        e, w = f's[-{m}:]', [f's[:-{m}]', f's[-{m}:-1]', f's[{m}:]']
    elif t == 2:
        e, w = f's[::{k}]', [f's[1::{k}]', f's[::-{k}]', f's[::{k + 1}]']
    elif t == 3:
        e, w = f's[{a}:{b}:{k}]', [f's[{a}:{b}:1]', f's[{a + 1}:{b}:{k}]', f's[{a}:{b + 1}:{k}]']
    elif t == 4:
        m = r.randint(2, 5)
        e, w = f's[::-1][:{m}]', [f's[:{m}][::-1]', f's[-{m}:]', f's[::-1][:{m + 1}]']
    else:
        m = r.randint(1, 4)
        e, w = f's[{a}:-{m}]', [f's[{a}:{m}]', f's[{a}:-{m + 1}]', f's[{a + 1}:-{m}]']
    code = f's = "{s}"\nprint({e})'
    ans = run(code)
    if not ans.strip():
        raise ValueError('empty')
    wrong = uniq([run(f's = "{s}"\nprint({x})') for x in w], [ans])
    wrong = [x for x in wrong if x.strip()]
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Write the output of the following Python code:\n{code}', 'answer': ans,
            'key': f'Indexing starts at 0; the stop index is excluded. Output: {ans}', 'distractors': wrong}


def str_methods(r):
    s = r.choice(SENTS)
    w = s.split()
    t = r.randrange(7)
    ch = r.choice([c for c in s.lower() if c.isalpha()])
    if t == 0:
        e, alts = f's.split("{ch}")', [f's.partition("{ch}")', f's.split()', f's.rsplit("{ch}", 1)']
    elif t == 1:
        e, alts = f's.count("{ch}")', [f's.find("{ch}")', f's.lower().count("{ch}") + 1', f's.index("{ch}") + 1']
    elif t == 2:
        e, alts = 's.title()', ['s.capitalize()', 's.upper()', 's.swapcase()']
    elif t == 3:
        e, alts = f's.find("{ch}")', [f's.find("{ch}") + 1', f's.rfind("{ch}")', f's.count("{ch}")']
    elif t == 4:
        old = r.choice(w)
        e, alts = f's.replace("{old}", "{old.upper()}")', ['s.upper()', f's.replace("{old}", "")', 's']
    elif t == 5:
        e, alts = '"-".join(s.split())', ['"-".join(s)', 's.replace(" ", "")', '"-".join(s.split()[::-1])']
    else:
        e, alts = 's.split()[-1].upper() + str(len(s.split()))', ['s.split()[0].upper() + str(len(s.split()))', 's.split()[-1].upper() + str(len(s))',
                                                                 's.split()[-1] + str(len(s.split()))']
    code = f's = "{s}"\nprint({e})'
    ans = run(code)
    wrong = uniq([run(f's = "{s}"\nprint({x})') for x in alts], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'What is the output of the following code?\n{code}', ans, wrong[:3], f'{e} gives {ans}.', r)


def list_ops(r):
    v = r.choice(VARS)
    L = r.sample(range(1, 60), r.randint(4, 6))
    ops = []
    pool = [f'{v}.append({r.randint(1, 40)})', f'{v}.insert({r.randint(0, 3)}, {r.randint(1, 40)})',
            f'{v}.extend([{r.randint(1, 9)}, {r.randint(10, 20)}])', f'{v}.pop({r.randint(0, 2)})', f'{v}.pop()',
            f'{v}.remove({L[r.randrange(len(L))]})', f'{v}.reverse()', f'{v}.sort()', f'{v}.sort(reverse=True)',
            f'{v} = {v}[1:] + {v}[:1]', f'{v}[{r.randint(0, 2)}] = {v}[-1]']
    ops = r.sample(pool, 4)
    if sum(1 for o in ops if 'sort' in o) > 1:
        raise ValueError('two sorts')
    lines = [f'{v} = {L}'] + ops + [f'print({v})']
    code = '\n'.join(lines)
    try:
        ans = run(code)
    except ValueError:
        raise
    except Exception:
        raise ValueError('bad')
    wrong = []
    for i in range(len(ops)):
        c = '\n'.join([lines[0]] + ops[:i] + ops[i + 1:] + [lines[-1]])
        wrong.append(run_or_err(c))
    wrong = [w for w in uniq(wrong, [ans]) if not w.startswith('Error')]
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': ans,
            'key': f'2 marks for the correct final list {ans} (1 mark if only one operation is traced wrongly).',
            'distractors': wrong, 'marks': 2}


def dict_ops(r):
    ks = r.sample(NAMES, 4)
    vals = r.sample(range(40, 100), 4)
    d = dict(zip(ks[:3], vals[:3]))
    v = r.choice(['D', 'marks', 'result', 'score', 'stud'])
    t = r.randrange(4)
    if t == 0:
        code = f'{v} = {d}\n{v}["{ks[3]}"] = {vals[3]}\n{v}["{ks[0]}"] += 5\nprint(len({v}), {v}["{ks[0]}"])'
        alts = [code.replace('+= 5', '= 5'), code.replace(f'{v}["{ks[3]}"] = {vals[3]}\n', ''), code.replace('len(', 'max(')]
    elif t == 1:
        code = f'{v} = {d}\nprint({v}.get("{ks[3]}", 0), {v}.get("{ks[1]}"))'
        alts = [code.replace(', 0)', ')'), code.replace(f'{v}.get("{ks[1]}")', f'{v}.get("{ks[1]}", 0) + 1'), code.replace(f'"{ks[3]}", 0', f'"{ks[2]}", 0')]
    elif t == 2:
        code = f'{v} = {d}\nfor k in {v}:\n    if {v}[k] > {sorted(vals[:3])[1] - 1}:\n        print(k, end="#")'
        alts = [code.replace(' > ', ' < '), code.replace('print(k,', 'print(' + v + '[k],'), code.replace(f'{sorted(vals[:3])[1] - 1}', f'{sorted(vals[:3])[1]}')]
    else:
        code = f'{v} = {d}\nx = {v}.pop("{ks[1]}")\n{v}.update({{"{ks[3]}": {vals[3]}}})\nprint(x, list({v}.keys()))'
        alts = [code.replace(f'{v}.pop("{ks[1]}")', f'{v}["{ks[1]}"]').replace('x, list', 'x, list'),
                code.replace(f'.pop("{ks[1]}")', f'.pop("{ks[0]}")'), code.replace('list(' + v + '.keys())', 'list(' + v + '.values())')]
    ans = run(code)
    wrong = [w for w in uniq([run_or_err(a) for a in alts], [ans]) if w.strip() and not w.startswith('Error')]
    wrong = uniq(wrong + [ans.replace('#', ' '), ans + '#' if not ans.endswith('#') else ans[:-1]], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'Predict the output:\n{code}', ans, wrong[:3], f'Output: {ans}.', r)


def loop_out(r):
    t = r.randrange(5)
    if t == 0:
        a, b, c, k = r.randint(1, 5), r.randint(15, 30), r.choice([2, 3]), r.choice([3, 4, 5])
        code = f'for i in range({a}, {b}, {c}):\n    if i % {k} == 0:\n        print(i, end="#")'
        alts = [code.replace(f'range({a}, {b},', f'range({a}, {b + 1},'), code.replace('== 0', '!= 0'), code.replace(f'range({a},', f'range({a + 1},')]
    elif t == 1:
        s = r.choice(WORDS)
        code = (f'S = "{s}"\nR = ""\nfor ch in S:\n    if ch in "aeiouAEIOU":\n        R = R + "*"\n'
                f'    elif ch.isupper():\n        R = R + ch.lower()\n    else:\n        R = ch + R\nprint(R)')
        alts = [code.replace('R = ch + R', 'R = R + ch'), code.replace('ch.lower()', 'ch'), code.replace('"*"', '"#"')]
    elif t == 2:
        n = r.randint(1000, 99999)
        code = f'n = {n}\ns = 0\nwhile n > 0:\n    d = n % 10\n    if d % 2 == 0:\n        s = s + d\n    n = n // 10\nprint(s)'
        alts = [code.replace('d % 2 == 0', 'd % 2 == 1'), code.replace('s = s + d', 's = s * 10 + d'), code.replace('n // 10', 'n // 100')]
    elif t == 3:
        n = r.randint(3, 5)
        sym = r.choice(['*', '#', '@'])
        code = f'for i in range(1, {n + 1}):\n    for j in range(i):\n        print("{sym}", end="")\n    print(i)'
        alts = [code.replace('range(i)', 'range(i + 1)'), code.replace('print(i)', 'print()'), code.replace(f'range(1, {n + 1})', f'range(1, {n})')]
    else:
        L = r.sample(range(1, 30), 6)
        code = f'L = {L}\nfor i in range(len(L)):\n    if L[i] % 2 == 0:\n        L[i] = L[i] // 2\n    else:\n        L[i] = L[i] * 2\nprint(L)'
        alts = [code.replace('// 2', '* 2', 1).replace('L[i] * 2\n', 'L[i] // 2\n'), code.replace('% 2 == 0', '% 2 == 1'), code.replace('range(len(L))', 'range(1, len(L))')]
    ans = run(code)
    wrong = [w for w in uniq([run_or_err(a) for a in alts], [ans]) if w.strip() and not w.startswith('Error')]
    if len(wrong) < 3 or not ans.strip():
        raise ValueError('few')
    return {'stem': f'Write the output of the following Python code:\n{code}', 'answer': ans,
            'key': f'2 marks for the exact output (1 mark if partly correct):\n{ans}', 'distractors': wrong, 'marks': 2}


# error finding: (correct line, faulty line) templates; {v} {n} {f} filled per variant
ERR_PROGS = [
    ['{v} = int(input("Enter a number: "))', ('if {v} % 2 == 0:', 'if {v} % 2 = 0:'), ('    print({v}, "is even")', '    Print({v}, "is even")'),
     ('else:', 'else'), ('    print({v}, "is odd")', '    print({v}, "is odd)')],
    [('def {f}(n):', 'def {f}(n)'), '    s = 0', ('    for i in range(1, n + 1):', '    for i in range(1, n + 1)'), ('        s += i', '        s =+ i'),
     ('    return s', '    retrun s'), ('print({f}({n}))', 'print({f}({n})')],
    ['{v} = [{a}, {b}, {c}]', ('for x in {v}:', 'for x in {v}'), ('    if x > {n}:', '    if x => {n}:'), ('        print(x * 2)', '        print(x * 2'),
     ('    else:', '    elif:'), '        print(x)'],
    [('{v} = "{w}"', '{v} = "{w}'), 'count = 0', ('for ch in {v}:', 'for ch in {v}'), ('    if ch.isupper():', '    if ch.isupper:'),
     ('        count += 1', '        count + = 1'), ('print("Uppercase letters:", count)', 'print("Uppercase letters:" count)')],
    [('def {f}(a, b=10):', 'def {f}(a=10, b):'), ('    if a > b:', '    If a > b:'), '        return a', '    return b',
     ('x = {f}({n})', 'x == {f}({n})'), ('print(x)', 'print x')],
    ['total = 0', ('while True:', 'while True'), ('    m = int(input("Marks: "))', '    m = int(input("Marks: ")'), ('    if m < 0:', '    if m < 0'),
     '        break', ('    total = total + m', '    total = total + M'), 'print(total)'],
    [('D = {{"{k1}": {a}, "{k2}": {b}}}', 'D = {{"{k1}": {a}, "{k2}": {b}]'), ('for k in D:', 'for k in D'), ('    print(k, D[k])', '    print(k, D(k))'),
     ('if "{k1}" in D:', 'if "{k1}" in D'), ('    print("Found")', '    print("Found"))')],
    [('import math', 'import Math'), '{v} = {n}', ('if {v} >= 0:', 'if {v} >= 0'), ('    print(math.sqrt({v}))', '    print(math.sqrt{v})'),
     ('else:', 'else if:'), ('    print("Negative")', '    print("Negative)')],
]


def error_find(r):
    prog = r.choice(ERR_PROGS)
    v, f = r.choice(['num', 'x', 'val', 'N', 'a', 'value']), r.choice(FUNCS)
    w = r.choice(WORDS)
    k1, k2 = r.sample(NAMES, 2)
    fill = dict(v=v, f=f, n=r.randint(5, 30), a=r.randint(1, 20), b=r.randint(21, 40), c=r.randint(41, 60), w=w, k1=k1, k2=k2)
    errs = [i for i, ln in enumerate(prog) if isinstance(ln, tuple)]
    pickn = 4
    chosen = set(r.sample(errs, pickn))
    good, bad, fixes = [], [], []
    for i, ln in enumerate(prog):
        if isinstance(ln, tuple):
            g, b = ln[0].format(**fill), ln[1].format(**fill)
            good.append(g)
            bad.append(b if i in chosen else g)
            if i in chosen:
                fixes.append(f'{b.strip()}  →  {g.strip()}')
        else:
            good.append(ln.format(**fill))
            bad.append(ln.format(**fill))
    gcode = '\n'.join(good)
    assert compiles(gcode), gcode
    bcode = '\n'.join(bad)
    marks = 2
    return {'stem': (f'{r.choice(NAMES)} has written the following code, but it has errors. Rewrite the correct code and underline '
                     f'the corrections made.\n{bcode}'),
            'answer': 'Corrected code:\n' + gcode + '\nCorrections: ' + '; '.join(fixes),
            'key': '½ mark for each of the 4 corrections.', 'marks': marks}


ALIAS = [
    ('A = {L}\nB = A\nB.append({x})\nprint(A)', 'B refers to the same list object as A, so appending through B changes A.'),
    ('A = {L}\nB = A[:]\nB.append({x})\nprint(A, len(B))', 'A[:] makes a copy; A is unchanged.'),
    ('A = {L}\nB = A\nB = B + [{x}]\nprint(A)', 'B + [...] creates a new list; A is unchanged.'),
    ('A = {L}\nB = A\nB += [{x}]\nprint(A)', '+= on a list extends it in place, so A also changes.'),
    ('A = {T}\nB = A\nB = B + ({x},)\nprint(A, B)', 'Tuples are immutable; B + (...) creates a new tuple.'),
    ('A = {L}\nB = A * 2\nB[0] = {x}\nprint(A[0], B[0], len(B))', 'A * 2 builds a new list of repeated elements.'),
    ('S = "{w}"\nT = S\nT = T.upper()\nprint(S, T)', 'Strings are immutable; upper() returns a new string.'),
    ('A = {L}\nB = list(A)\nA.reverse()\nprint(A[0], B[0])', 'list(A) makes a copy before A is reversed.'),
]


def alias_out(r):
    tpl, why = r.choice(ALIAS)
    L = r.sample(range(1, 50), r.randint(3, 4))
    x = r.randint(51, 99)
    code = tpl.format(L=L, T=tuple(L), x=x, w=r.choice(WORDS))
    ans = run(code)
    alt = [code.replace('B = A[:]', 'B = A').replace('B = list(A)', 'B = A').replace('B = A\nB = B +', 'B = A\nB +=').replace('B = A\nB +=', 'B = A\nB = B +'),
           code.replace(f'{x}', str(x + 1)), code.replace('print(A', 'print(B', 1)]
    wrong = [w for w in uniq([run_or_err(a) for a in alt], [ans]) if not w.startswith('Error')]
    wrong = uniq(wrong + ['Error'], [ans])
    if len(wrong) < 3:
        wrong += [ans.replace(str(x), str(x + 1))]
    wrong = uniq(wrong, [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'What will be the output of the following code?\n{code}', ans, wrong[:3], f'{why} Output: {ans}.', r)


AR_REV = [
    ('A tuple cannot be changed after it is created.', 'Tuples are immutable sequences in Python.', 'a', 'Immutability is why a tuple cannot be changed.'),
    ('The expression 2 ** 3 ** 2 evaluates to 512.', 'The exponent operator ** is evaluated from right to left.', 'a', '3 ** 2 = 9 first, then 2 ** 9 = 512.'),
    ('Dictionary keys must be immutable.', 'A list can be used as a key in a dictionary.', 'c', 'A is true; R is false: a list is mutable and cannot be a key.'),
    ('The statement L = [1, 2] * 2 gives [2, 4].', 'The * operator replicates a list.', 'd', 'A is false: [1, 2] * 2 = [1, 2, 1, 2]; R is true.'),
    ('Strings in Python are immutable.', 'Each character of a string can be changed using indexing, as in s[0] = "A".', 'c', 'A is true; R is false: item assignment on a string gives TypeError.'),
    ('The loop for i in range(5): runs five times.', 'range(5) generates the numbers 0 to 4.', 'a', 'Five values 0–4, so five iterations.'),
    ('15 // 4 gives 3 and 15 % 4 gives 3.', 'The // operator gives the quotient and % gives the remainder.', 'a', 'Floor division and modulus explain both results.'),
    ('The expression not True or True evaluates to True.', 'The or operator has higher precedence than not.', 'c', 'A is true; R is false: not has higher precedence than or.'),
    ('A list can contain elements of different data types.', 'Lists in Python are heterogeneous sequences.', 'a', 'Lists can mix data types.'),
    ('The break statement skips only the current iteration of a loop.', 'The continue statement moves control to the next iteration of the loop.', 'd', 'A is false: break exits the loop; R is true.'),
]

CH01 = [ST(S + '01-st1', 'Python data types, operators and flow of control', """
T: mutable object | an object whose value can be changed in place after creation, such as a list or dictionary
T: immutable object | an object whose value cannot be changed in place after creation, such as an int, float, string or tuple
T: type casting | converting a value from one data type to another, as with int("25") or str(10)
T: slicing | extracting a part of a sequence using the [start:stop:step] notation
T: dictionary | an unordered collection of key-value pairs in which keys are unique and immutable
Q: Which of the following is a mutable data type in Python? | list | tuple | str | int
Q: Which operator has the highest precedence in Python? | ** (exponentiation) | * (multiplication) | not | and
Q: What is the data type of the value returned by 7 / 2 in Python 3? | float | int | str | complex
Q: Which method adds all elements of another list at the end of a list? | extend() | append() | insert() | add()
Q: Which of these is NOT a valid Python identifier? | 2total | total_2 | _total | Total2
Q: Which statement is used to skip the rest of the current iteration of a loop? | continue | break | pass | exit
Q: Which function returns the number of key-value pairs in a dictionary D? | len(D) | D.count() | D.size() | count(D)
Q: In Python, which of the following creates a tuple with one element? | (5,) | (5) | [5] | {5}
S+: Python uses indentation to mark a block of statements
S+: A string can be traversed with a for loop, one character at a time
S+: The keys of a dictionary must be of an immutable type
S+: The range(2, 10, 3) function generates the values 2, 5 and 8
S+: The in operator can be used to test membership in lists, tuples, strings and dictionary keys
S+: The sort() method changes the list in place and returns None
S-: A tuple can be modified using the append() method | Tuples are immutable and have no append() method
S-: The expression 10 // 3 gives 3.33 | 10 // 3 gives 3 because // is floor division
S-: Dictionary keys can be repeated | Keys of a dictionary are unique; a repeated key overwrites the old value
S-: The break statement takes control to the next iteration of the loop | break terminates the loop; continue goes to the next iteration
C: s[0] = "J" gives an error for the string s = "Python" | strings are immutable, so item assignment is not allowed
C: A list cannot be used as a key of a dictionary | a list is mutable and dictionary keys must be immutable
C: The loop for i in range(1, 10, 2) never prints 10 | the stop value of range() is excluded
X: C2 D2 2 | Differentiate between append() and extend() methods of a list with an example. | append() adds one element (even a list) at the end: L.append([4, 5]) gives [1, 2, 3, [4, 5]]; extend() adds each element of an iterable: L.extend([4, 5]) gives [1, 2, 3, 4, 5].
X: C2 D3 2 | Differentiate between a list and a tuple in Python. Give one example of each. | A list is mutable and written in square brackets, e.g. [10, 20]; a tuple is immutable and written in parentheses, e.g. (10, 20). Lists have methods like append(); tuples do not.
X: C3 D3 2 | What is the difference between the break and continue statements? Explain with a small loop. | break exits the loop at once; continue skips the rest of the current iteration and goes to the next one. In for i in range(5): if i == 2: break, only 0 1 print; with continue, 0 1 3 4 print.
"""), ST(S + '01-st2', 'functions in Python', """
T: function | a named group of statements that performs a specific task and runs only when it is called
T: built-in function | a function that is always available in Python without importing a module, such as len(), input() or int()
T: module | a Python file (.py) containing definitions of functions, variables and classes that can be imported
T: user-defined function | a function created by the programmer using the def keyword
T: function header | the first line of a function definition, beginning with def and ending with a colon
Q: Which keyword is used to define a function in Python? | def | function | define | fun
Q: Which of the following is a built-in function? | len() | sqrt() | randint() | mean()
Q: Which module provides the function randint()? | random | math | statistics | os
Q: What does a function return if it has no return statement? | None | 0 | an empty string | False
Q: Which statement imports only the sqrt() function from the math module? | from math import sqrt | import sqrt from math | import math.sqrt | using math.sqrt
Q: Which function of the statistics module returns the most frequent value? | mode() | mean() | median() | max()
Q: math.ceil(4.2) returns: | 5 | 4 | 4.0 | 4.2
Q: random.random() returns a value: | from 0.0 up to but not including 1.0 | from 0 to 1 including 1 | an integer from 0 to 10 | from 1 to 100
S+: A function must be defined before it is called in a Python program
S+: The statement import math as m lets the math module be used through the name m
S+: random.randint(a, b) can return both a and b
S+: The math.floor() function returns the largest integer less than or equal to its argument
S+: A function can be called many times, which avoids repeating code
S-: random.randint(1, 5) can never return 5 | randint(a, b) includes both end points, so it can return 5
S-: A function always needs a return statement | Without return a function returns None
S-: The len() function belongs to the math module | len() is a built-in function and needs no import
S-: math.sqrt(16) returns the integer 4 | math.sqrt() returns a float, 4.0
C: Functions make programs easier to read and maintain | a large program is divided into small, named blocks that can be reused and tested separately
C: The function call math.sqrt(25) fails unless math is imported | sqrt() is defined in the math module, which must be imported before use
C: random.randrange(1, 10) never returns 10 | the stop value of randrange() is excluded
X: C2 D2 2 | Differentiate between a built-in function and a user-defined function with one example each. | Built-in functions are always available, e.g. len(), max(); user-defined functions are written by the programmer using def, e.g. def area(r): return 3.14 * r * r.
X: C2 D3 2 | Write the two ways of importing the math module and calling its sqrt() function. | import math then math.sqrt(25); or from math import sqrt then sqrt(25) (also import math as m; m.sqrt(25)).
"""), ST(S + '01-st3', 'arguments and parameters', """
T: parameter | a variable written in the function header that receives a value when the function is called
T: argument | a value passed to a function in the function call
T: default parameter | a parameter that is given a value in the function header and used when no argument is passed for it
T: keyword argument | an argument passed in the form name=value, so that its position does not matter
T: positional argument | an argument matched to a parameter by its position in the call
Q: In def f(a, b=5):, the parameter b is a: | default parameter | keyword argument | global variable | required positional parameter
Q: Which function header is valid? | def f(a, b=2, c=3): | def f(a=1, b, c): | def f(a=1, b=2, c): | def f(a, b=2, c):
Q: When a function returns a, b, the values are returned as a: | tuple | list | dictionary | set
Q: In the call show(name="Asha", age=16), the arguments are: | keyword arguments | default arguments | positional arguments only | global arguments
Q: What happens if a positional argument follows a keyword argument in a call? | SyntaxError | TypeError at run time | the arguments are swapped silently | NameError
Q: The values written in a function call are called: | arguments (actual parameters) | formal parameters | defaults | keywords
S+: Default parameters must come after all non-default parameters in a function header
S+: Keyword arguments can be given in any order in a function call
S+: A function can return more than one value by separating the values with commas
S+: In a function call, positional arguments must come before keyword arguments
S-: Default parameters can be placed before non-default parameters | Non-default parameters must come first; def f(a=1, b) is a SyntaxError
S-: A function can return only one value | It can return several values as a tuple, e.g. return a, b
S-: Keyword arguments must be written in the same order as the parameters | Keyword arguments can be given in any order
C: def area(l, b=10): can be called as area(5) | b is a default parameter, so it takes 10 when no value is passed
C: The call f(b=2, 3) gives an error | a positional argument cannot follow a keyword argument
C: x, y = calc(4, 5) works when calc() has return a + b, a * b | the returned tuple is unpacked into x and y
X: C2 D2 2 | Differentiate between formal parameters and actual arguments with an example. | Formal parameters are the names in the function header, e.g. a and b in def add(a, b); actual arguments are values in the call, e.g. 3 and 4 in add(3, 4).
X: C3 D3 2 | Explain default and keyword arguments with an example of each. | Default: def interest(p, r=5): r takes 5 if omitted; keyword: interest(r=6, p=1000) matches by name in any order.
"""), ST(S + '01-st4', 'scope of variables', """
T: local variable | a variable created inside a function, which can be used only inside that function
T: global variable | a variable created outside all functions, which can be read anywhere in the program
T: global keyword | a statement inside a function that lets the function change a variable defined outside it
T: flow of execution | the order in which the statements of a program are executed, including jumps into and out of function calls
T: scope | the part of a program in which a variable name can be accessed
Q: A variable defined inside a function is called a: | local variable | global variable | built-in variable | parameter constant
Q: Which keyword lets a function modify a global variable? | global | nonlocal | extern | static
Q: If a function assigns to a variable x without declaring it global, x is: | local to that function | the global x | an error | a constant
Q: When a list is passed to a function and the function appends to it, the change: | is visible outside the function | is lost after the function ends | raises an error | creates a copy of the list
Q: Python looks up names in the order: | Local, Enclosing, Global, Built-in | Global, Local, Built-in, Enclosing | Built-in, Global, Local, Enclosing | Local, Global, Enclosing, Built-in
S+: A local variable is destroyed when the function finishes executing
S+: A global variable can be read inside a function without the global keyword
S+: A mutable object such as a list passed to a function can be changed inside the function
S+: Statements inside a function are executed only when the function is called
S-: A local variable can be used anywhere in the program | It can be used only inside the function where it is created
S-: Changing an integer parameter inside a function changes the caller's variable | Integers are immutable; rebinding the parameter does not affect the caller
S-: The global keyword is needed to read a global variable inside a function | It is needed only to assign to it
C: A function that does x = x + 1 without global x raises UnboundLocalError | assignment makes x local, and it is read before a value is given to it
C: Appending to a list parameter changes the original list | the parameter and the argument refer to the same list object
X: C2 D2 2 | Differentiate between local and global variables with a short example. | Local: created inside a function, used only there (def f(): y = 5); global: created outside all functions, readable everywhere (x = 10 at top level).
X: C3 D3 2 | Why does changing a list inside a function change it outside, while changing an integer does not? | A list is mutable; the parameter refers to the same object, so in-place changes are seen. An int is immutable; assignment makes the local name refer to a new object.
""")]


# ----------------------------------------------------------- ch01 st2 functions
def math_out(r):
    import math
    x = round(r.uniform(-9.9, 9.9), 1)
    if float(x).is_integer():
        x += 0.3
    y = r.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
    p, q = r.randint(2, 5), r.randint(2, 3)
    t = r.randrange(5)
    if t == 0:
        e, alts = f'math.ceil({x}) + math.floor({x})', [f'math.ceil({x}) + math.ceil({x})', f'math.floor({x}) + math.floor({x})', f'int({x}) + int({x})']
    elif t == 1:
        e, alts = f'math.sqrt({y}) + math.pow({p}, {q})', [f'int(math.sqrt({y})) + {p} ** {q}', f'math.sqrt({y}) * math.pow({p}, {q})', f'{y} / 2 + math.pow({p}, {q})']
    elif t == 2:
        e, alts = f'math.fabs({x}) + abs({-p})', [f'{x} + {p}', f'math.floor(math.fabs({x})) + {p}', f'math.ceil(math.fabs({x})) + {p}']
    elif t == 3:
        e, alts = f'math.floor({x}), math.ceil({x})', [f'math.ceil({x}), math.floor({x})', f'int({x}), int({x}) + 1', f'round({x}), round({x}) + 1']
    else:
        e, alts = f'math.gcd({p * 6}, {q * 8})', [f'{p * 6} * {q * 8} // math.gcd({p * 6}, {q * 8})', f'min({p * 6}, {q * 8})', f'math.gcd({p * 6}, {q * 8}) * 2']
    code = f'import math\nprint({e})'
    return out_item(r, code, [f'import math\nprint({a})' for a in alts], head='What is the output of the following code?', as_mcq=True,
                    key=f'Evaluate each math function: output {run(code)}.')


def stats_out(r):
    xs = [r.randint(1, 20) for _ in range(r.choice([5, 7]))]
    xs[1] = xs[3]
    import statistics as st
    try:
        st.mode(xs)
    except Exception:
        raise ValueError('mode')
    v = r.choice(['data', 'marks', 'runs', 'L'])
    f = r.choice(['mean', 'median', 'mode'])
    code = f'import statistics\n{v} = {xs}\nprint(statistics.{f}({v}))'
    alts = [code.replace(f'.{g}(', f'.{g}(') .replace(f'statistics.{f}', f'statistics.{g}') for g in ['mean', 'median', 'mode'] if g != f]
    alts.append(f'print(sorted({xs})[{len(xs) // 2 - 1}])')
    return out_item(r, code, alts, head='What is the output of the following code?', as_mcq=True,
                    key=f'statistics.{f}() of {xs} is {run(code)}.')


def rand_possible(r):
    t = r.randrange(3)
    v = r.choice(['AR', 'L', 'VAL', 'P', 'NUM'])
    data = r.sample(range(10, 99), 6) if t != 2 else r.sample(['RED', 'BLUE', 'PINK', 'GREEN', 'WHITE', 'BLACK', 'GREY'], 6)
    a1, a2 = r.randint(0, 2), r.randint(3, 4)
    b1, b2 = r.randint(2, 3), r.randint(4, 5)
    if t in (0, 2):
        code = (f'import random\n{v} = {data}\nFROM = random.randint({a1}, {a2 - 1})\nTO = random.randint({b1}, {b2})\n'
                f'for K in range(FROM, TO + 1):\n    print({v}[K], end="#")')
        poss = set()
        for fr in range(a1, a2):
            for to in range(b1, b2 + 1):
                poss.add(''.join(f'{data[k]}#' for k in range(fr, to + 1)))
        poss.discard('')
        cands = set()
        for fr in range(0, 6):
            for to in range(fr, 6):
                cands.add(''.join(f'{data[k]}#' for k in range(fr, to + 1)))
        imp = sorted(cands - poss)
    else:
        n = r.randint(2, 4)
        code = f'import random\n{v} = {data}\nfor i in range({n}):\n    x = random.randint(0, {n})\n    print({v}[x], end="-")'
        poss_idx = list(itertools.product(range(0, n + 1), repeat=n))
        poss = set(''.join(f'{data[k]}-' for k in p) for p in poss_idx)
        imp = []
        for _ in range(60):
            p = [r.randint(0, 5) for _ in range(n)]
            if max(p) > n:
                imp.append(''.join(f'{data[k]}-' for k in p))
        imp = sorted(set(imp))
    good = r.choice(sorted(poss))
    if len(imp) < 3:
        raise ValueError('few')
    wrong = r.sample(imp, 3)
    return mcq(f'What possible output(s) are expected to be displayed on the screen when the following code is executed? Choose the one that can occur.\n{code}',
               good, wrong, f'{good} is possible for some values of the random numbers; each other option needs an index outside the range the random calls can produce.', r)


def rand_range(r):
    a, b = r.randint(1, 5), r.randint(6, 12)
    c = r.randint(2, 5)
    v = r.choice(['N', 'X', 'num', 'P'])
    t = r.randrange(3)
    if t == 0:
        code = f'import random\n{v} = random.randint({a}, {b}) + {c}'
        lo, hi = a + c, b + c
    elif t == 1:
        code = f'import random\n{v} = random.randrange({a}, {b}) * {c}'
        lo, hi = a * c, (b - 1) * c
    else:
        code = f'import random\n{v} = int(random.random() * {b}) + {a}'
        lo, hi = a, b - 1 + a
    return {'stem': f'Consider the code:\n{code}\nWhat are the minimum and maximum values that {v} can take?',
            'answer': f'Minimum {lo}, maximum {hi}', 'key': f'1 mark each: minimum {lo}, maximum {hi}.',
            'distractors': [f'Minimum {lo}, maximum {hi + c}', f'Minimum {lo - c if lo - c > 0 else lo + 1}, maximum {hi}', f'Minimum {lo}, maximum {hi - 1}', f'Minimum {lo + 1}, maximum {hi + 1}'],
            'marks': 2}


def func_call_out(r):
    f = r.choice(FUNCS)
    a, b, k = r.randint(2, 9), r.randint(2, 9), r.randint(2, 5)
    t = r.randrange(4)
    if t == 0:
        code = f'def {f}(x):\n    return x * {k} - 1\n\nprint({f}({a}) + {f}({b}))'
        alts = [code.replace(f'x * {k} - 1', f'x * ({k} - 1)'), code.replace(f'{f}({a}) + {f}({b})', f'{f}({a} + {b})'), code.replace(' - 1', ' + 1')]
    elif t == 1:
        code = f'def {f}(n):\n    s = 0\n    for i in range(1, n + 1):\n        if i % {k} == 0:\n            s += i\n    return s\n\nprint({f}({a * 3 + 4}))'
        alts = [code.replace('range(1, n + 1)', 'range(1, n)'), code.replace('s += i', 's += 1'), code.replace('== 0', '!= 0')]
    elif t == 2:
        code = f'def {f}(s):\n    r = ""\n    for ch in s:\n        r = ch + r\n    return r.upper()\n\nprint({f}("{r.choice(WORDS).lower()}"))'
        alts = [code.replace('r = ch + r', 'r = r + ch'), code.replace('.upper()', ''), code.replace('.upper()', '.title()')]
    else:
        code = f'def {f}(a, b):\n    if a > b:\n        return a - b\n    return a + b\n\nprint({f}({a}, {b}), {f}({b}, {a}))'
        alts = [code.replace('a - b', 'b - a'), code.replace('a > b', 'a < b'), code.replace('    return a + b', '    return a * b')]
    return out_item(r, code, alts, head='Write the output of the following code:', marks=2,
                    key=f'2 marks for the correct output: {run(code)}.')


def returns_none(r):
    f = r.choice(FUNCS)
    w = r.choice(WORDS)
    n = r.randint(2, 5)
    code = f'def {f}(s):\n    print(s * {n})\n\nx = {f}("{w[:2]}")\nprint(x)'
    ans = run(code)
    return mcq(f'What will be the output of the following code?\n{code}', ans,
               [(w[:2] * n), (w[:2] * n) + '\n' + (w[:2] * n), 'Error'], 'The function prints the repeated string and returns None, so print(x) displays None.', r)


FN_TASKS = [
    ('Write a function {f}(L) that accepts a list L of integers and displays all the elements that are divisible by {k} but not by {m}.',
     'def {f}(L):\n    for x in L:\n        if x % {k} == 0 and x % {m} != 0:\n            print(x, end=" ")', '{f}([10, 15, 30, 45, 9])'),
    ('Write a function {f}(S) that accepts a string S and returns the number of words in it that begin with the letter "{c}" (upper or lower case).',
     'def {f}(S):\n    count = 0\n    for w in S.split():\n        if w[0] in "{c}{cl}":\n            count += 1\n    return count', 'print({f}("{s}"))'),
    ('Write a function {f}(L) that replaces every element of the list L that is greater than {k} by {k}, and leaves the others unchanged.',
     'def {f}(L):\n    for i in range(len(L)):\n        if L[i] > {k}:\n            L[i] = {k}', 'X = [3, 99, 7]\n{f}(X)\nprint(X)'),
    ('Write a function {f}(D) that accepts a dictionary D of student names and marks, and displays the names of students who scored more than {k}.',
     'def {f}(D):\n    for name in D:\n        if D[name] > {k}:\n            print(name)', '{f}({{"Asha": 90, "Ravi": 20}})'),
    ('Write a function {f}(T) that accepts a tuple T of numbers and returns the sum of the elements at even index positions.',
     'def {f}(T):\n    s = 0\n    for i in range(0, len(T), 2):\n        s += T[i]\n    return s', 'print({f}((1, 2, 3, 4)))'),
    ('Write a function {f}(S) that accepts a string S and returns a new string in which every vowel is replaced by "{sym}".',
     'def {f}(S):\n    R = ""\n    for ch in S:\n        if ch in "aeiouAEIOU":\n            R += "{sym}"\n        else:\n            R += ch\n    return R', 'print({f}("Education"))'),
    ('Write a function {f}(L) that shifts all the elements of the list L one position to the left; the first element moves to the end.',
     'def {f}(L):\n    first = L[0]\n    for i in range(len(L) - 1):\n        L[i] = L[i + 1]\n    L[-1] = first', 'X = [1, 2, 3]\n{f}(X)\nprint(X)'),
    ('Write a function {f}(n) that returns the sum of the digits of the positive integer n.',
     'def {f}(n):\n    s = 0\n    while n > 0:\n        s += n % 10\n        n //= 10\n    return s', 'print({f}(1234))'),
    ('Write a function {f}(L) that returns a list containing the squares of the odd numbers in the list L.',
     'def {f}(L):\n    R = []\n    for x in L:\n        if x % 2 != 0:\n            R.append(x * x)\n    return R', 'print({f}([1, 2, 3]))'),
    ('Write a function {f}(D) that accepts a dictionary D whose values are prices (in rupees) and returns the key of the costliest item.',
     'def {f}(D):\n    best = None\n    for k in D:\n        if best is None or D[k] > D[best]:\n            best = k\n    return best', 'print({f}({{"pen": 20, "bag": 500}}))'),
]


def fn_task(r, idx=None, marks=3):
    i = idx if idx is not None else r.randrange(len(FN_TASKS))
    stem, sol, test = FN_TASKS[i]
    k, m = r.choice([(3, 5), (5, 2), (7, 3), (4, 8), (6, 4), (3, 2), (5, 10)])
    c = r.choice('ATSDMPH')
    base = [['SHOW', 'Display', 'Div'], ['COUNT', 'Count', 'CountW'], ['Limit', 'Cap', 'Change'], ['Toppers', 'SHOW', 'Display'], ['SumEven', 'Calc', 'Add'],
            ['Replace', 'Mask', 'Change'], ['LShift', 'Shift', 'Rotate'], ['DigitSum', 'Sum', 'Calc'], ['OddSq', 'Squares', 'Make'], ['Costly', 'Find', 'MaxItem']][i]
    fill = dict(f=r.choice(base) + r.choice(['', 'IT', 'Val', '_L', 'Fn']),
                k=k * 10 if i in (2, 3) else k, m=m, c=c, cl=c.lower(), sym=r.choice(['*', '#', '@', '$']),
                s='A stitch in time saves nine')
    code = sol.format(**fill)
    run(code + '\n' + test.format(**fill))
    return {'stem': stem.format(**fill), 'answer': code,
            'key': f'{marks} marks: function header 1, correct loop/logic {marks - 2 if marks > 2 else 1}, correct output/return 1.', 'marks': marks}


def fn_task2(r):
    i, j = r.sample(range(len(FN_TASKS)), 2)
    a, b = fn_task(r, i, 2), fn_task(r, j, 3)
    return {'stem': f'(a) {a["stem"]} (2)\n(b) {b["stem"]} (3)', 'answer': f'(a)\n{a["answer"]}\n(b)\n{b["answer"]}',
            'key': '5 marks: (a) header 1, logic 1; (b) header 1, loop/condition 1, output/return 1.', 'marks': 5}


# ----------------------------------------------------------- ch01 st3 arguments
def header_valid(r):
    f = r.choice(FUNCS)
    ps = r.sample(['a', 'b', 'c', 'x', 'y', 'n', 'p', 'q', 'r', 's'], 3)
    vals = [r.randint(1, 9) for _ in range(3)]
    combos = []
    for mask in itertools.product([0, 1], repeat=3):
        parts = [f'{p}={v}' if d else p for p, v, d in zip(ps, vals, mask)]
        combos.append((f'def {f}({", ".join(parts)}):', compiles(f'def {f}({", ".join(parts)}):\n    pass')))
    want_valid = r.random() < 0.5
    good = [h for h, ok in combos if ok == want_valid]
    bad = [h for h, ok in combos if ok != want_valid]
    if len(bad) < 3:
        raise ValueError('few')
    g = r.choice(good)
    stem = 'Which of the following function headers is ' + ('valid' if want_valid else 'NOT valid') + ' in Python?'
    return mcq(stem, g, r.sample(bad, 3), f'{g} {"is valid" if want_valid else "is invalid"}: a parameter with a default value cannot be followed by one without a default.', r)


def call_valid(r):
    f = r.choice(FUNCS)
    p1, p2, p3 = r.sample(['a', 'b', 'c', 'x', 'y', 'n', 'p', 'q', 'r'], 3)
    d = r.randint(1, 9)
    head = f'def {f}({p1}, {p2}, {p3}={d}):\n    return {p1} + {p2} * {p3}'
    calls = [f'{f}(1, 2)', f'{f}(1, 2, 3)', f'{f}({p2}=4, {p1}=1)', f'{f}(1, {p3}=2, {p2}=5)', f'{f}(1, {p1}=2)', f'{f}({p1}=1, 2)',
             f'{f}(1)', f'{f}({p3}=3)', f'{f}(1, 2, 3, 4)', f'{f}(1, {p2}=2, {p2}=3)']
    res = []
    for c in calls:
        code = head + '\nprint(' + c + ')'
        if not compiles(code):
            res.append((c, False))
            continue
        _, e = exc(code)
        res.append((c, e is None))
    want = r.random() < 0.5
    good = [c for c, ok in res if ok == want]
    bad = [c for c, ok in res if ok != want]
    g = r.choice(good)
    return mcq(f'Consider the function:\n{head}\nWhich of the following function calls is ' + ('valid' if want else 'invalid') + '?', g, r.sample(bad, 3),
               f'{g} is {"valid" if want else "invalid"}. A call must give values for {p1} and {p2} exactly once and cannot put a positional argument after a keyword argument.', r)


def default_out(r):
    f = r.choice(FUNCS)
    a, b, c = r.randint(1, 9), r.randint(10, 20), r.randint(2, 5)
    t = r.randrange(3)
    if t == 0:
        code = f'def {f}(x, y={b}, z={c}):\n    print(x + y * z, end=" ")\n\n{f}({a})\n{f}({a}, {c})\n{f}({a}, z={a})'
        alts = [code.replace(f'{f}({a}, {c})', f'{f}({a}, y={b})'), code.replace('x + y * z', '(x + y) * z'), code.replace(f'z={a})', f'z={c})')]
    elif t == 1:
        code = f'def {f}(p, r={c}, t=1):\n    return p * r * t // 100\n\nprint({f}({b * 100}, t={c}), {f}({b * 100}, {a}))'
        alts = [code.replace(f't={c})', f'{c})'), code.replace('// 100', '// 10'), code.replace(f', {a}))', '))')]
    else:
        s = r.choice(WORDS)
        code = f'def {f}(s, n={c}, ch="*"):\n    return ch * n + s[:n]\n\nprint({f}("{s}"), {f}("{s}", ch="#"), {f}("{s}", 1))'
        alts = [code.replace('s[:n]', 's[n:]'), code.replace('ch * n + s[:n]', 's[:n] + ch * n'), code.replace(f'n={c}', f'n={c + 1}')]
    return out_item(r, code, alts, head='Write the output of the following code:', marks=2,
                    key=f'2 marks: values not passed take the defaults; keyword arguments match by name. Output: {run(code)}')


def multi_return(r):
    f = r.choice(FUNCS)
    a, b = r.randint(2, 15), r.randint(2, 15)
    t = r.randrange(3)
    if t == 0:
        code = f'def {f}(x, y):\n    return x + y, x * y, x - y\n\nres = {f}({a}, {b})\nprint(res)'
        alts = [code.replace('print(res)', 'print(list(res))'), code.replace('x - y', 'y - x'), code.replace('print(res)', 'print(res[0])')]
    elif t == 1:
        code = f'def {f}(L):\n    return min(L), max(L)\n\nlo, hi = {f}({r.sample(range(1, 90), 5)})\nprint(hi - lo, hi, lo)'
        alts = [code.replace('lo, hi =', 'hi, lo ='), code.replace('hi - lo, ', ''), code.replace('min(L), max(L)', 'max(L), min(L)').replace('lo, hi =', 'hi, lo =').replace('hi - lo', 'lo - hi')]
    else:
        code = f'def {f}(n):\n    return n // 10, n % 10\n\nq, r = {f}({a * 10 + b % 10})\nprint(r, q)\nprint({f}({b * 7}))'
        alts = [code.replace('print(r, q)', 'print(q, r)'), code.replace('n // 10, n % 10', 'n % 10, n // 10'), code.replace(f'print({f}({b * 7}))', f'print(list({f}({b * 7})))')]
    return out_item(r, code, alts, head='Predict the output of the following code:', marks=2,
                    key=f'2 marks: several returned values travel as a tuple. Output: {run(code)}')


# ----------------------------------------------------------- ch01 st4 scope
def scope_out(r):
    f = r.choice(FUNCS)
    v = r.choice(['x', 'a', 'num', 'val', 'count', 'total'])
    a, b, c = r.randint(1, 20), r.randint(1, 9), r.randint(2, 5)
    t = r.randrange(4)
    if t == 0:
        code = f'{v} = {a}\ndef {f}():\n    global {v}\n    {v} = {v} + {b}\n    print({v}, end=" ")\n\n{f}()\n{f}()\nprint({v})'
        alts = [code.replace(f'    global {v}\n', f'    {v} = {a}\n'), code.replace(f'{f}()\n{f}()', f'{f}()'), code.replace(f'+ {b}', f'* {b}')]
    elif t == 1:
        code = f'{v} = {a}\ndef {f}({v}):\n    {v} = {v} * {c}\n    print({v}, end=" ")\n\n{f}({v} + {b})\nprint({v})'
        alts = [code.replace(f'def {f}({v}):\n', f'def {f}({v}):\n    global_dummy = 0\n').replace(f'print({v})\n', 'print(0)\n'),
                code.replace(f'{f}({v} + {b})', f'{f}({v})'), code.replace(f'* {c}', f'+ {c}')]
        alts[0] = f'{v} = {a}\nprint({a * c}, end=" ")\nprint({(a + b) * c})'
    elif t == 2:
        code = (f'{v} = {a}\ndef {f}():\n    {v} = {b}\n    print("inside", {v}, end="; ")\n\nprint("before", {v}, end="; ")\n{f}()\nprint("after", {v})')
        alts = [code.replace(f'    {v} = {b}\n', f'    global {v}\n    {v} = {b}\n'), code.replace(f'"before", {v}', f'"before", {b}'), code.replace(f'"after", {v}', f'"after", {b}')]
    else:
        code = (f'def {f}(P, Q={c}):\n    global R\n    R = P + Q\n    P = P * Q\n    return P\n\nR = {a}\nS = {f}({b})\nprint(R, S)\nS = {f}(S, {b})\nprint(R, S)')
        alts = [code.replace('    global R\n', ''), code.replace('return P', 'return R'), code.replace(f'Q={c}', f'Q={c + 1}')]
    return out_item(r, code, alts, head='Write the output of the following code:', marks=2,
                    key=f'2 marks (1 per line of output). Output:\n{run(code)}')


def unbound(r):
    f = r.choice(FUNCS)
    v = r.choice(['x', 'count', 'total', 'n'])
    a = r.randint(1, 50)
    t = r.randrange(3)
    if t == 0:
        code = f'{v} = {a}\ndef {f}():\n    {v} = {v} + 1\n    print({v})\n\n{f}()'
    elif t == 1:
        code = f'{v} = {a}\ndef {f}():\n    print({v})\n    {v} = 5\n\n{f}()'
    else:
        code = f'{v} = {a}\ndef {f}():\n    global {v}\n    {v} = {v} + 1\n    print({v})\n\n{f}()'
    out, e = exc(code)
    ans = f'It raises UnboundLocalError' if e == 'UnboundLocalError' else f'It prints {out}'
    wrong = [f'It prints {a + 1}' if e else 'It raises UnboundLocalError', f'It prints {a}', 'It raises NameError', f'It prints {a + 1}', 'It prints 5']
    wrong = uniq(wrong, [ans])[:3]
    return mcq(f'What happens when the following code is executed?\n{code}', ans, wrong,
               ('Because the function assigns to ' + v + ', it is local throughout the function and is read before it has a value.' if e else
                'The global statement makes the function use the global variable.'), r)


def mutable_pass(r):
    f = r.choice(FUNCS)
    L = r.sample(range(1, 30), 3)
    n, k = r.randint(31, 60), r.randint(2, 4)
    t = r.randrange(3)
    if t == 0:
        code = f'def {f}(A, n):\n    A.append(n)\n    n = n * {k}\n    return n\n\nX = {L}\nm = {n}\ny = {f}(X, m)\nprint(X, m, y)'
    elif t == 1:
        code = f'def {f}(A):\n    A = A + [{n}]\n    A[0] = 0\n    return A\n\nX = {L}\nY = {f}(X)\nprint(X, Y)'
    else:
        code = f'def {f}(A):\n    for i in range(len(A)):\n        A[i] = A[i] * {k}\n    A = []\n\nX = {L}\n{f}(X)\nprint(X)'
    ans = run(code)
    alts = [code.replace('A.append(n)', 'A = A + [n]'), code.replace('A = A + [', 'A += ['), code.replace('    A = []\n', '    A.clear()\n'),
            code.replace(f'* {k}', f'+ {k}')]
    wrong = [w for w in uniq([run_or_err(a) for a in alts], [ans]) if not w.startswith('Error')]
    wrong = uniq(wrong + [ans.replace(str(n), str(n * k), 1), str(L)], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'What is the output of the following code?\n{code}', ans, wrong[:3],
               'In-place changes to a list parameter are seen by the caller; rebinding the parameter or changing an int is not. Output: ' + ans, r)


def scope_case(r):
    who = r.choice(NAMES)
    f = r.choice(FUNCS)
    a, b = r.randint(10, 50), r.randint(2, 9)
    code = (f'bonus = {a}\ndef {f}(salary, rate={b}):\n    global bonus\n    tax = salary * rate // 100\n    bonus = bonus + 5\n    return salary - tax + bonus\n\n'
            f'print({f}({b * 1000}))\nprint({f}({b * 1000}, {b + 1}))\nprint(bonus)')
    out = run(code).split('\n')
    return {'stem': (f'{who} wrote this program to compute take-home pay:\n{code}\n'
                     '(i) Name one local and one global variable in the program. (1)\n(ii) Which parameter is a default parameter? (1)\n'
                     '(iii) Write the output of the program. (2)'),
            'answer': f'(i) Local: tax (or salary, rate); global: bonus (ii) rate (iii) {out[0]} / {out[1]} / {out[2]}',
            'key': '1 + 1 + 2 marks (½ mark per correct output line, 2 marks for all three).', 'marks': 4}


def args_case(r):
    who = r.choice(NAMES)
    f = r.choice(['interest', 'bill', 'fare', 'fee', 'amount'])
    p, rate = r.choice([1000, 2000, 5000, 8000]), r.choice([5, 6, 8, 10])
    code = f'def {f}(p, r={rate}, t=2):\n    si = p * r * t / 100\n    return p + si, si\n\nA = {f}({p})\nB, C = {f}({p}, t=3)\nprint(A)\nprint(B, C)'
    out = run(code).split('\n')
    return {'stem': (f'{who} wrote the following function:\n{code}\n(i) Identify the default parameters. (1)\n(ii) Is the call {f}(r=5, {p}) valid? Why? (1)\n'
                     '(iii) Write the output. (2)'),
            'answer': f'(i) r and t (ii) No – a positional argument cannot follow a keyword argument (SyntaxError). (iii) {out[0]} / {out[1]}',
            'key': '1 + 1 + 2 marks.', 'marks': 4}


# ====================================================================== ch02 exceptions
EXC_SNIPS = [
    ('x = int("{w}")', 'ValueError'), ('print({a} / ({b} - {b}))', 'ZeroDivisionError'), ('L = [{a}, {b}]\nprint(L[{c}])', 'IndexError'),
    ('D = {{"{k}": {a}}}\nprint(D["{k2}"])', 'KeyError'), ('print("{w}" + {a})', 'TypeError'), ('print({v} + {a})', 'NameError'),
    ('T = ({a}, {b})\nT[0] = {c}', 'TypeError'), ('import {mod}', 'ModuleNotFoundError'), ('f = open("{fn}.txt")', 'FileNotFoundError'),
    ('x = float("{w}")', 'ValueError'), ('print({a} % 0)', 'ZeroDivisionError'), ('s = "{w}"\nprint(s[{c2}])', 'IndexError'),
    ('L = [{a}, {b}]\nL.remove({c})', 'ValueError'), ('print(len({a}))', 'TypeError'), ('import math\nprint(math.sqrt(-{a}))', 'ValueError'),
]
EXC_ALL = ['ValueError', 'ZeroDivisionError', 'IndexError', 'KeyError', 'TypeError', 'NameError', 'ModuleNotFoundError', 'FileNotFoundError']


def exc_identify(r):
    tpl, _ = r.choice(EXC_SNIPS)
    w = r.choice(WORDS)
    fill = dict(w=w, a=r.randint(2, 50), b=r.randint(2, 50), c=r.randint(60, 99), k=r.choice(NAMES), k2=r.choice(NAMES), v=r.choice(['total', 'Sum', 'marks', 'value', 'Count']),
                mod=r.choice(['maths', 'Random', 'statistic', 'pickel', 'csvfile']), fn=r.choice(['notes2', 'report_x', 'data99', 'old_marks']), c2=len(w) + r.randint(0, 5))
    if fill['k'] == fill['k2']:
        raise ValueError('same')
    code = tpl.format(**fill)
    _, e = exc(code)
    if e is None:
        raise ValueError('no exception')
    wrong = r.sample([x for x in EXC_ALL if x != e and not (e == 'ModuleNotFoundError' and x == 'FileNotFoundError')], 3)
    return mcq(f'Which built-in exception is raised when the following code is executed?\n{code}', e, wrong, f'{e} is raised.', r)


def exc_partial(r):
    a, b = r.randint(10, 99), r.randint(2, 9)
    L = r.sample(range(1, 40), 4)
    i = r.randint(4, 7)
    lines = [f'print({a} // {b}, end=" ")', f'L = {L}', f'print(L[{r.randint(0, 3)}], end=" ")', f'print(L[{i}])', 'print("Done")']
    if r.random() < 0.5:
        lines = [f'print({a} % {b}, end=" ")', f'x = {a} / {b - b}', 'print(x)', 'print("Done")']
    code = '\n'.join(lines)
    out, e = exc(code)
    ans = f'{out.strip()} is printed and then {e} is raised'
    wrong = [f'{out.strip()} Done is printed', f'Only {e} is raised; nothing is printed', f'{out.strip()} is printed and then a SyntaxError is reported']
    return mcq(f'What happens when the following code runs?\n{code}', ans, wrong,
               'Statements before the faulty line execute; the exception stops the program at that line. A syntax error would stop it before anything runs.', r)


def try_out(r):
    s = r.choice(['0', str(r.randint(2, 9)), 'abc', 'x' + str(r.randint(1, 9)), str(r.randint(10, 30))])
    a = r.randint(20, 99)
    L = r.sample(range(1, 50), 3)
    t = r.randrange(3)
    labels = r.sample(['A', 'B', 'C', 'D', 'E', 'P', 'Q', 'R', 'S', 'T'], 5)
    A, B, C, D, E = labels
    if t == 0:
        code = (f'try:\n    x = int("{s}")\n    y = {a} // x\n    print("{A}", y)\nexcept ZeroDivisionError:\n    print("{B}")\nexcept ValueError:\n'
                f'    print("{C}")\nelse:\n    print("{D}")\nfinally:\n    print("{E}")')
    elif t == 1:
        idx = r.choice([0, 1, 2, 3, 5])
        code = (f'L = {L}\ntry:\n    print(L[{idx}] * 2)\n    print(L[{idx}] / (L[0] - {L[0] if r.random() < 0.4 else L[0] + 1}))\nexcept IndexError:\n    print("{B}")\n'
                f'except ZeroDivisionError:\n    print("{C}")\nfinally:\n    print("{E}")')
    else:
        k = r.choice(['"x"', str(r.randint(1, 9)), '"5"'])
        code = (f'def safe(v):\n    try:\n        return {a} + v\n    except TypeError:\n        print("{B}", end=" ")\n        return 0\n    finally:\n        print("{E}", end=" ")\n\nprint(safe({k}))')
    ans = run(code)
    alt = [code.replace('finally:', 'except Exception:'), code.replace('else:', 'finally:').replace('finally:\n    print("' + E, 'else:\n    print("' + E) if 'else:' in code else code.replace('print("' + E + '"', 'print("' + D + '"'),
           code.replace('except ValueError', 'except TypeError').replace('except IndexError', 'except KeyError').replace('except TypeError:\n        print', 'except ValueError:\n        print')]
    wrong = [w for w in uniq([run_or_err(x) for x in alt], [ans]) if not w.startswith('Error')]
    wrong = uniq(wrong + [ans.replace(E, '').strip(), ans + '\n' + D, f'{ans.split(chr(10))[0]}'], [ans])
    wrong = [w for w in wrong if w.strip()]
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': ans, 'distractors': wrong[:5],
            'key': f'2 marks. The matching except block runs only if an exception occurs; else runs only if none occurs; finally always runs. Output:\n{ans}',
            'marks': 2}


def raise_out(r):
    f = r.choice(FUNCS)
    lim = r.randint(10, 60)
    v1, v2 = r.randint(1, lim - 1), r.randint(lim + 1, lim + 40)
    t = r.randrange(3)
    order = r.sample([v1, v2, -v1], 3)
    if t == 0:
        body = f'def {f}(n):\n    if n < 0:\n        raise ValueError("negative")\n    if n > {lim}:\n        raise OverflowError("too big")\n    return n * 2\n\n'
        calls = ''.join(f'try:\n    print({f}({x}))\nexcept ValueError as e:\n    print("V:", e)\nexcept OverflowError as e:\n    print("O:", e)\n' for x in order)
    elif t == 1:
        body = f'def {f}(marks):\n    assert 0 <= marks <= {lim}, "invalid marks"\n    return marks\n\n'
        calls = ''.join(f'try:\n    print({f}({x}))\nexcept AssertionError as e:\n    print("Error:", e)\n' for x in order)
    else:
        body = f'def {f}(age):\n    if age < {lim}:\n        raise Exception("Not eligible")\n    print("Eligible", end=" ")\n\n'
        calls = ''.join(f'try:\n    {f}({x})\nexcept Exception as e:\n    print(e, end=" ")\nfinally:\n    print("|", end=" ")\n' for x in order)
    code = body + calls
    ans = run(code)
    alts = [code.replace('n < 0', 'n <= 0').replace(f'n > {lim}', f'n >= {v2}'), code.replace(f'{lim}', f'{lim + 50}'), code.replace(f'age < {lim}', f'age > {lim}')]
    wrong = [w for w in uniq([run_or_err(x) for x in alts], [ans]) if not w.startswith('Error')]
    wrong = uniq(wrong + [' '.join(reversed(ans.split(' '))), ans.replace('Error: ', '').replace('V: ', '').replace('O: ', '')], [ans])
    if len(wrong) < 3:
        raise ValueError('few')
    return {'stem': f'Write the output of the following code:\n{code}', 'answer': ans, 'distractors': wrong[:5],
            'key': f'2 marks. A raise or failed assert jumps to the matching except block. Output:\n{ans}', 'marks': 2}


def exc_program(r):
    who = r.choice(NAMES)
    t = r.randrange(3)
    if t == 0:
        stem = (f'Write a Python program for {who}\'s billing counter that inputs the total amount and the number of customers, and prints the share of each customer. '
                'Use try…except to handle ValueError (non-numeric input) and ZeroDivisionError, an else block to print the share, and a finally block that prints "Thank you".')
        ans = ('try:\n    amt = float(input("Total amount: "))\n    n = int(input("Customers: "))\n    share = amt / n\nexcept ValueError:\n    print("Enter numbers only")\n'
               'except ZeroDivisionError:\n    print("Customers cannot be zero")\nelse:\n    print("Share =", share)\nfinally:\n    print("Thank you")')
    elif t == 1:
        lim = r.choice([100, 50, 80])
        stem = (f'Write a function READMARKS() that keeps asking the user to enter marks until a valid integer between 0 and {lim} is entered. '
                'Raise a ValueError with a suitable message when the number is out of range, and handle both non-numeric input and the raised error.')
        ans = (f'def READMARKS():\n    while True:\n        try:\n            m = int(input("Marks: "))\n            if m < 0 or m > {lim}:\n                raise ValueError("Marks out of range")\n'
               '            return m\n        except ValueError as e:\n            print("Invalid:", e)')
    else:
        stem = ('Write a function SAFE_DIVIDE(L, i, j) that returns L[i] / L[j] for a list L. It should return None and print a suitable message '
                'if either index is out of range (IndexError) or L[j] is zero (ZeroDivisionError).')
        ans = ('def SAFE_DIVIDE(L, i, j):\n    try:\n        return L[i] / L[j]\n    except IndexError:\n        print("Index out of range")\n'
               '    except ZeroDivisionError:\n        print("Division by zero")\n    return None')
    compile(ans, 'x', 'exec')
    return {'stem': stem, 'answer': ans, 'key': '3 marks: try block 1, correct except clauses 1, else/finally or return logic 1.', 'marks': 3}


def exc_case(r):
    who = r.choice(NAMES)
    a = r.randint(100, 999)
    code = (f'def average(total, n):\n    try:\n        avg = total / n\n    except ZeroDivisionError:\n        print("No students")\n        avg = 0\n    else:\n        print("Average computed")\n'
            f'    finally:\n        print("Done")\n    return avg\n\nprint(average({a}, 0))\nprint(average({a * 4}, 4))')
    out = run(code)
    return {'stem': (f'{who} wrote the following code to find the class average:\n{code}\n(i) Is ZeroDivisionError a syntax error or an exception? (1)\n'
                     '(ii) When does the else block run? (1)\n(iii) Write the complete output. (2)'),
            'answer': f'(i) An exception (run-time error) (ii) Only when no exception occurs in the try block (iii)\n{out}',
            'key': '1 + 1 + 2 marks (½ mark per output line).', 'marks': 4}


CH02 = [ST(S + '02-st1', 'errors and built-in exceptions', """
T: syntax error | an error in the grammar of a Python statement, detected before the program starts running
T: exception | an error that occurs while a program is running and disturbs its normal flow
T: ZeroDivisionError | the exception raised when a number is divided by zero
T: ValueError | the exception raised when a function gets an argument of the right type but an inappropriate value, as in int("abc")
T: NameError | the exception raised when a name that has not been defined is used
T: IndexError | the exception raised when a sequence index is out of range
Q: Which exception is raised by int("12a")? | ValueError | TypeError | NameError | SyntaxError
Q: Which exception is raised when a key is not found in a dictionary? | KeyError | IndexError | NameError | LookupKeyError
Q: Which exception is raised by "5" + 5? | TypeError | ValueError | SyntaxError | ArithmeticError
Q: Which exception is raised when import fails because the module is not found? | ModuleNotFoundError (an ImportError) | FileNotFoundError | NameError | EOFError
Q: An error caused by a missing colon after an if condition is a: | syntax error | ValueError | logical error that Python reports as an exception | ZeroDivisionError
Q: Which exception is raised when input() reaches the end of file without reading data? | EOFError | IOError | IndexError | KeyError
Q: Which of these is detected before a Python program begins to run? | SyntaxError | ZeroDivisionError | ValueError | IndexError
S+: A syntax error is also called a parsing error
S+: Exceptions are raised at run time and can be handled by the program
S+: Every exception in Python is an object of a class derived from the class Exception (BaseException)
S+: NameError is raised when a variable is used before it is defined
S+: A program with a syntax error does not run at all
S-: Syntax errors can be handled with try and except | Syntax errors are found before execution, so they cannot be caught by the same program
S-: TypeError is raised when an index is out of range | IndexError is raised for an index out of range
S-: Dividing by zero gives a ValueError | It raises ZeroDivisionError
C: A program with a missing closing bracket shows no output at all | syntax errors are detected while parsing, before execution starts
C: int("seven") raises ValueError | the argument is a string (right type) but it cannot be converted to an integer (wrong value)
X: C2 D2 2 | Differentiate between a syntax error and an exception, with an example of each. | Syntax error: wrong grammar, found before running, e.g. if x > 5 without colon; exception: run-time error, e.g. 10/0 raises ZeroDivisionError.
X: C3 D3 2 | Name the exceptions raised by: (i) L = [1, 2]; L[5] (ii) print(x) when x is undefined. | (i) IndexError (ii) NameError.
"""), ST(S + '02-st2', 'handling exceptions', """
T: try block | the block containing statements that may raise an exception
T: except block | the block that handles a particular exception raised in the try block
T: else clause | the block that runs only when no exception is raised in the try block
T: finally clause | the block that always runs, whether or not an exception occurred
T: exception handler | the code that is executed when a particular exception is raised
Q: Which block is always executed in exception handling? | finally | else | except | try
Q: The else block of a try statement runs when: | no exception occurs in the try block | an exception occurs | the finally block fails | always
Q: What is the correct order of clauses? | try, except, else, finally | try, else, except, finally | try, finally, except, else | except, try, else, finally
Q: An except clause written without an exception name: | catches any exception | catches only syntax errors | is a syntax error | catches nothing
Q: The process of finding a suitable handler for a raised exception is called: | catching the exception | throwing the exception | raising the exception | compiling the exception
Q: If no handler is found for an exception, the program: | stops and Python displays the error | continues silently | restarts | ignores the statement
S+: A single try block can have several except blocks
S+: Once an exception occurs in a try block, the remaining statements of the try block are skipped
S+: The finally block is generally used to release resources such as closing a file
S+: An except clause can handle more than one exception by naming them in a tuple
S-: The else block runs when an exception occurs | else runs only when the try block raises no exception
S-: The finally block runs only if an exception occurs | finally runs in every case
S-: A try block can be written without any except or finally clause | A try must have at least one except or a finally clause
C: The statement after the failing line in a try block is not executed | control jumps to the matching except block as soon as the exception is raised
C: Closing a file is written in the finally block | finally runs whether or not an exception occurs
X: C2 D3 2 | What is the use of the finally clause? Give an example. | It runs in all cases and is used for clean-up: try: f = open("a.txt") ... finally: f.close().
X: C3 D3 3 | Explain the flow of control in a try…except…else…finally statement. | try runs first; on an exception the rest of try is skipped and the matching except runs; if no exception the else runs; finally runs in both cases; an unmatched exception propagates after finally.
"""), ST(S + '02-st3', 'raise and assert statements', """
T: raise statement | a statement used to raise an exception deliberately, as in raise ValueError("Invalid")
T: assert statement | a statement that tests a condition and raises AssertionError if the condition is false
T: AssertionError | the exception raised when the condition in an assert statement is false
Q: Which exception does a failing assert raise? | AssertionError | ValueError | AssertError | RuntimeError
Q: Which statement raises an exception deliberately? | raise | throw | except | error
Q: In assert x > 0, "Negative", the string "Negative" is: | the message shown with AssertionError | a variable name | the exception class | ignored by Python
Q: After a raise statement executes, the statements after it in the same block: | are not executed | run normally | run only once | run before the raise
S+: raise can be used with built-in exceptions such as ValueError and TypeError
S+: assert is used to check an assumption during testing and debugging
S+: A raised exception can be caught by an except block like any other exception
S-: assert raises ValueError when the condition is false | It raises AssertionError
S-: The raise statement can only be used inside an except block | raise can be used anywhere to signal an error
C: assert age >= 18 stops a program when age is 15 | the condition is false, so AssertionError is raised
C: A function can raise ValueError for a negative price | raise lets the programmer signal invalid data even when Python itself sees no error
X: C2 D2 2 | Write the syntax of the raise and assert statements with an example of each. | raise ExceptionName("message"), e.g. raise ValueError("Negative"); assert condition, "message", e.g. assert n > 0, "n must be positive".
"""),]


def fams_ch01_02():
    E = {}
    st = S + '01-st1'
    E[st] = [F('C1', 'D2', 'mcq', expr_eval), F('C2', 'D2', 'short', slicing, marks=1), F('C2', 'D3', 'mcq', str_methods),
             F('C2', 'D3', 'short', list_ops, marks=2), F('C3', 'D2', 'mcq', dict_ops), F('C3', 'D3', 'short', loop_out, marks=2),
             F('C3', 'D4', 'explain', error_find, marks=2, gap='G5'), F('C4', 'D4', 'mcq', alias_out, gap='G5'),
             F('C3', 'D3', 'mcq', lambda r: ar(*r.choice(AR_REV)), kinds=('ar',)),
             F('C4', 'D3', 'multi_step', lambda r: fn_task(r, marks=3), marks=3)]
    st = S + '01-st2'
    E[st] = [F('C2', 'D2', 'mcq', math_out), F('C2', 'D2', 'mcq', stats_out), F('C3', 'D4', 'mcq', rand_possible, gap='G5'),
             F('C3', 'D3', 'short', rand_range, marks=2), F('C2', 'D3', 'short', func_call_out, marks=2), F('C3', 'D3', 'mcq', returns_none),
             F('C4', 'D3', 'multi_step', lambda r: fn_task(r, marks=3), marks=3), F('C4', 'D5', 'long', fn_task2, marks=5)]
    st = S + '01-st3'
    E[st] = [F('C2', 'D2', 'mcq', header_valid), F('C3', 'D3', 'mcq', call_valid), F('C2', 'D3', 'short', default_out, marks=2),
             F('C3', 'D3', 'short', multi_return, marks=2), F('C4', 'D4', 'case', args_case, marks=4, gap='G7'), F('C3', 'D4', 'mcq', call_valid, gap='G5')]
    st = S + '01-st4'
    E[st] = [F('C3', 'D3', 'short', scope_out, marks=2), F('C3', 'D4', 'mcq', unbound, gap='G5'), F('C4', 'D4', 'mcq', mutable_pass, gap='G5'),
             F('C4', 'D4', 'case', scope_case, marks=4, gap='G7'), F('C2', 'D3', 'short', scope_out, marks=2)]
    st = S + '02-st1'
    E[st] = [F('C2', 'D2', 'mcq', exc_identify), F('C3', 'D3', 'mcq', exc_partial), F('C1', 'D1', 'mcq', exc_identify),
             F('C3', 'D4', 'explain', error_find, marks=2, gap='G5'), F('C4', 'D4', 'mcq', exc_partial, gap='G5'), F('C4', 'D3', 'multi_step', exc_program, marks=3)]
    st = S + '02-st2'
    E[st] = [F('C3', 'D3', 'short', try_out, marks=2), F('C3', 'D4', 'short', try_out, marks=2, gap='G5'), F('C4', 'D4', 'case', exc_case, marks=4, gap='G7'),
             F('C4', 'D3', 'multi_step', exc_program, marks=3), F('C2', 'D3', 'mcq', exc_identify)]
    st = S + '02-st3'
    E[st] = [F('C3', 'D3', 'short', raise_out, marks=2), F('C4', 'D4', 'short', raise_out, marks=2), F('C4', 'D3', 'multi_step', exc_program, marks=3)]
    return [CH01, CH02], E
