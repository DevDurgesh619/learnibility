"""Computed families for the CBSE class 11 Informatics Practices (065) bank.

Every answer is computed: statistics with fractions and the statistics module, NumPy outputs by running the code
with NumPy, file-loading outputs by running the code on the shown file in a temporary folder, and SQL outputs by
running the query on an sqlite3 copy of the shown table (g12_computer_science_kit.DB). SQL items keep to the class 11
syllabus (no aggregate functions, GROUP BY or joins) and avoid division and fractional arithmetic, so sqlite and
MySQL print the same result. Python families of g11_computer_science_kit.py are reused through `only()`, which
regenerates a variant whose code uses a feature outside the IP class 11 syllabus.
"""
from __future__ import annotations

import math
import statistics
from fractions import Fraction

from qbank import mcq
from g12_computer_science_kit import run, run_or_err, uniq, NAMES, DB, show_table, run_files, run_files_or_err
import g11_computer_science_kit as K
import g12_computer_science_d as D


# ====================================================================== scope filter for reused Python families
def only(fn, bad):
    """Wrap a family so that variants whose stem contains any of `bad` are regenerated."""
    def g(r):
        for _ in range(60):
            v = fn(r)
            if not any(b in v['stem'] for b in bad):
                return v
        raise ValueError('scope')
    g.__name__ = getattr(fn, '__name__', 'only')
    return g


def ip_py_case(r):
    who = r.choice(NAMES)
    item = r.choice(['notebook', 'pen', 'geometry box', 'water bottle', 'school bag'])
    price = round(r.uniform(20, 400), 1)
    qty = r.randint(2, 9)
    disc = r.choice([5, 10, 12, 15])
    code = (f'item = "{item}"\nprice = {price}\nqty = {qty}\ndiscount = {disc}\npaid = qty >= 5\n'
            f'total = price * qty\nbill = total - total * discount / 100\nprint(item, qty * 2, round(bill, 2), paid)')
    out = run(code)
    types = run(f'print(type({price}).__name__, type({qty}).__name__, type({qty >= 5}).__name__)')
    return K._case(who, 'wrote this program to prepare a shop bill:', code,
                   [('Write the data types of price, qty and paid.', types.replace(' ', ', '), 1),
                    ('Which operator gives a float result even when both operands are integers? Name one relational operator used.', '/ (true division); >=', 1),
                    ('Write the exact output of the program.', out, 2)])


def ip_dict_case(r):
    who = r.choice(NAMES)
    items = r.sample(['pen', 'pencil', 'eraser', 'ruler', 'notebook', 'marker', 'stapler'], 4)
    qty = r.sample(range(5, 60), 4)
    d = dict(zip(items[:3], qty[:3]))
    code = (f'stock = {d}\nstock["{items[3]}"] = {qty[3]}\nstock["{items[0]}"] -= 5\n'
            f'print(len(stock), stock.get("{items[1]}", 0), stock.get("glue", 0))\nprint(list(stock.keys())[1:3], max(stock.values()))')
    lines = run(code).split('\n')
    return K._case(who, 'keeps the stock of a stationery shop in a dictionary:', code,
                   [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second print statement.', lines[1], 1),
                    ('Why is get() used for "glue" instead of stock["glue"]? Write a statement to remove the item "' + items[2] + '" from stock.',
                     f'get() returns the default 0 instead of raising KeyError for a missing key; del stock["{items[2]}"]', 2)])


def ip_loop_case(r):
    who = r.choice(NAMES)
    n = r.randint(10000, 999999)
    code = f'n = {n}\ns = 0\ncount = 0\nwhile n > 0:\n    d = n % 10\n    if d % 2 == 0:\n        s = s + d\n    count = count + 1\n    n = n // 10\nprint(count, s)'
    out = run(code)
    alt = run(code.replace('n = n // 10', 'n = n // 100'))
    return K._case(who, 'wrote the following code to work with the digits of a number:', code,
                   [('How many times does the loop run?', out.split()[0], 1),
                    ('Write the output of the code.', out, 1),
                    ('Write the output if n = n // 10 is changed to n = n // 100, and explain the change.', f'{alt}; the loop now drops two digits each time, '
                     'so it runs fewer times and checks only every second digit', 2)])


# ====================================================================== statistics (ch05)
def _fmt(x):
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    v = float(x)
    return f'{v:.2f}'.rstrip('0').rstrip('.') if abs(v * 100 - round(v * 100)) < 1e-9 else f'{v:.2f}'


def _data(r, n=None, lo=10, hi=60, mode=True):
    n = n or r.randint(6, 9)
    while True:
        xs = [r.randint(lo, hi) for _ in range(n - 1)]
        if mode:
            xs.append(r.choice(xs))
        else:
            xs.append(r.randint(lo, hi))
        modes = statistics.multimode(xs)
        if mode and len(modes) != 1:
            continue
        if (Fraction(sum(xs), n) * 100).denominator != 1:
            continue
        r.shuffle(xs)
        return xs


def stat_measures(xs):
    s = sorted(xs)
    n = len(s)
    mean = Fraction(sum(s), n)
    med = Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)
    modes = statistics.multimode(s)
    return {'mean': mean, 'median': med, 'mode': modes[0] if len(modes) == 1 else None, 'range': s[-1] - s[0], 'sorted': s}


def stat_mcq(r):
    xs = _data(r)
    m = stat_measures(xs)
    what = r.choice(['mean', 'median', 'mode', 'range'])
    ans = _fmt(m[what])
    n = len(xs)
    cand = [_fmt(m[k]) for k in ('mean', 'median', 'mode', 'range') if k != what]
    cand += [str(xs[n // 2]), _fmt(Fraction(sum(xs), n - 1)), str(max(xs)), str(m['sorted'][n // 2]), _fmt(m[what] + 1)]
    wrong = uniq(cand, [ans])
    wrong = K.fill(wrong, ans)
    why = {'mean': f'Mean = sum / n = {sum(xs)} / {n} = {ans}',
           'median': f'Sorted: {", ".join(map(str, m["sorted"]))}; ' + ('the middle value' if n % 2 else 'the average of the two middle values') + f' is {ans}',
           'mode': f'{ans} occurs most often', 'range': f'Range = largest − smallest = {m["sorted"][-1]} − {m["sorted"][0]} = {ans}'}[what]
    return mcq(f'The marks of {n} students are: {", ".join(map(str, xs))}. What is the {what} of the marks?', ans, wrong[:3], why + '.', r)


def stat_written(r):
    xs = _data(r)
    m = stat_measures(xs)
    n = len(xs)
    ctx = r.choice(['daily sales (in units) of a shop', 'runs scored by a batsman in matches', 'heights gained by plants (in mm)', 'temperatures (in °C) recorded at noon'])
    mid = ('the middle (' + str(n // 2 + 1) + 'th) value') if n % 2 else f'the average of the {n // 2}th and {n // 2 + 1}th values'
    ans = (f'Sorted: {", ".join(map(str, m["sorted"]))}. Mean = {sum(xs)} / {n} = {_fmt(m["mean"])}; median = {mid} = {_fmt(m["median"])}; '
           f'mode = {m["mode"]} (occurs most often).')
    return {'stem': f'The {ctx} are: {", ".join(map(str, xs))}. Find the mean, median and mode.', 'answer': ans,
            'key': '3 marks: 1 each for the correct mean, median and mode with working.', 'marks': 3}


def _sd_data(r, n=None):
    n = n or r.randint(5, 6)
    for _ in range(200):
        xs = [r.randint(2, 20) for _ in range(n)]
        if sum(xs) % n == 0 and len(set(xs)) > 2:
            return xs
    raise ValueError('sd data')


def sd_parts(xs):
    n = len(xs)
    mu = sum(xs) // n
    dev = [x - mu for x in xs]
    sq = [d * d for d in dev]
    var = Fraction(sum(sq), n)
    sd = math.sqrt(var)
    return mu, dev, sq, var, sd


def sd_written(r, marks=3):
    xs = _sd_data(r)
    mu, dev, sq, var, sd = sd_parts(xs)
    n = len(xs)
    ans = (f'Mean = {sum(xs)} / {n} = {mu}. Deviations (x − mean): {", ".join(map(str, dev))}. Squares: {", ".join(map(str, sq))}; sum = {sum(sq)}. '
           f'Variance = {sum(sq)} / {n} = {_fmt(var)}. Standard deviation = √{_fmt(var)} ≈ {sd:.2f}.')
    return {'stem': f'Find the variance and standard deviation of the data: {", ".join(map(str, xs))}. (Use σ = √(Σ(x − x̄)² / n).)', 'answer': ans,
            'key': f'{marks} marks: mean 1, squared deviations and variance {marks - 2}, standard deviation 1.', 'marks': marks}


def sd_mcq(r):
    xs = _sd_data(r)
    mu, dev, sq, var, sd = sd_parts(xs)
    n = len(xs)
    t = r.randrange(2)
    if t == 0:
        ans = _fmt(var)
        wrong = uniq([f'{sd:.2f}', _fmt(Fraction(sum(sq), n - 1)), str(sum(sq)), _fmt(var + 1)], [ans])
        return mcq(f'What is the variance of the data {", ".join(map(str, xs))}? (Divide by n.)', ans, K.fill(wrong, ans)[:3],
                   f'Mean {mu}; Σ(x − mean)² = {sum(sq)}; variance = {sum(sq)} / {n} = {ans}.', r)
    ans = f'{sd:.2f}'
    wrong = uniq([_fmt(var), f'{math.sqrt(sum(sq) / (n - 1)):.2f}', f'{math.sqrt(sum(sq)):.2f}', f'{sd + 1:.2f}'], [ans])
    return mcq(f'What is the standard deviation of the data {", ".join(map(str, xs))}? (Use σ = √(Σ(x − x̄)² / n), rounded to 2 decimal places.)', ans,
               K.fill(wrong, ans)[:3], f'Mean {mu}; Σ(x − mean)² = {sum(sq)}; σ = √({sum(sq)} / {n}) ≈ {ans}.', r)


def median_even(r):
    xs = _data(r, n=r.choice([6, 8]))
    m = stat_measures(xs)
    ans = _fmt(m['median'])
    s = m['sorted']
    n = len(s)
    wrong = uniq([str(s[n // 2]), str(s[n // 2 - 1]), _fmt(Fraction(xs[n // 2 - 1] + xs[n // 2], 2)), _fmt(m['mean'])], [ans])
    return mcq(f'What is the median of {", ".join(map(str, xs))}?', ans, K.fill(wrong, ans)[:3],
               f'Sort first: {", ".join(map(str, s))}; with an even count the median is ({s[n // 2 - 1]} + {s[n // 2]}) / 2 = {ans}.', r)


def stat_case(r):
    who = r.choice(NAMES)
    while True:
        a, b = _sd_data(r, 5), _sd_data(r, 5)
        ma, _, sqa, va, sa = sd_parts(a)
        mb, _, sqb, vb, sb = sd_parts(b)
        if ma == mb and abs(sa - sb) > 0.5:
            break
        b = [x + (ma - mb) for x in b]
        mb, _, sqb, vb, sb = sd_parts(b)
        if min(b) > 0 and abs(sa - sb) > 0.5:
            break
    more = 'A' if sa < sb else 'B'
    ra, rb = max(a) - min(a), max(b) - min(b)
    stem = (f'{who} recorded the scores of two players over five matches.\nPlayer A: {", ".join(map(str, a))}\nPlayer B: {", ".join(map(str, b))}\n'
            f'(i) Find the mean score of each player. (1)\n(ii) Find the range of each player\'s scores. (1)\n'
            f'(iii) Find the standard deviation of each player\'s scores (divide by n) and state which player is more consistent. (2)')
    ans = (f'(i) A: {sum(a)} / 5 = {ma}; B: {sum(b)} / 5 = {mb} (ii) A: {max(a)} − {min(a)} = {ra}; B: {max(b)} − {min(b)} = {rb} '
           f'(iii) σA = √({sum(sqa)} / 5) ≈ {sa:.2f}; σB = √({sum(sqb)} / 5) ≈ {sb:.2f}; player {more} is more consistent (smaller standard deviation).')
    return {'stem': stem, 'answer': ans, 'key': '1 + 1 + 2 marks: ' + ans, 'marks': 4}


# ====================================================================== NumPy (ch06)
NP = 'import numpy as np\n'


def _np(code):
    return run(NP + code)


def _np_or_err(code):
    return run_or_err(NP + code)


def np_fill(wrong, out, n=3):
    """Top up distractors for a printed array: same layout, numbers changed (reversed order, last one off by one,
    first one doubled)."""
    import re as _re
    nums = _re.findall(r'-?\d+\.?\d*', out)
    extra = []
    if nums and '\n' not in out:
        it = iter(nums[::-1])
        extra.append(_re.sub(r'-?\d+\.?\d*', lambda m: next(it), out))
    if nums:
        last = nums[-1]
        try:
            bump = str(int(last) + 1)
        except ValueError:
            bump = str(float(last) + 1)
        k = out.rfind(last)
        extra.append(out[:k] + bump + out[k + len(last):])
        f = nums[0]
        k = out.find(f)
        try:
            dbl = str(int(f) * 2)
        except ValueError:
            dbl = str(float(f) * 2)
        extra.append(out[:k] + dbl + out[k + len(f):])
    w = uniq(list(wrong) + extra, [out])
    if len(w) < n:
        raise ValueError('few')
    return w


def _np_mcq(r, code, alts, why, head='What is the output of the following code?'):
    out = _np(code)
    wrong = [w for w in uniq([_np_or_err(c) for c in alts], [out]) if w.strip() and not w.startswith('Error')]
    wrong = np_fill(wrong, out)
    return mcq(f'{head}\n{NP}{code}', out, wrong[:3], f'{why} Output: {out}', r)


def _np_short(code, marks, why=''):
    out = _np(code)
    return {'stem': f'Write the output of the following code:\n{NP}{code}', 'answer': out,
            'key': f'{marks} mark{"s" if marks > 1 else ""} for the exact output{(" (" + why + ")") if why else ""}: {out}', 'marks': marks}


def np_attr(r):
    t = r.randrange(5)
    rows, cols = r.randint(2, 4), r.randint(2, 5)
    if t == 0:
        data = [[r.randint(1, 9) for _ in range(cols)] for _ in range(rows)]
        code = f'a = np.array({data})\nprint(a.ndim, a.shape, a.size)'
    elif t == 1:
        code = f'a = np.zeros(({rows}, {cols}))\nprint(a.ndim, a.shape, a.size)'
    elif t == 2:
        s, e, st = r.randint(0, 5), r.randint(15, 30), r.choice([2, 3, 4])
        code = f'a = np.arange({s}, {e}, {st})\nprint(a.ndim, a.shape, a.size)'
    elif t == 3:
        code = f'a = np.ones(({rows}, {cols}))\nb = a.reshape({cols}, {rows})\nprint(b.ndim, b.shape, b.size)'
    else:
        n = r.randint(4, 9)
        code = f'a = np.linspace(0, {r.randint(1, 5) * 10}, {n})\nprint(a.ndim, a.shape, a.size)'
    out = _np(code)
    p = out.split(' ', 1)
    sh = out[out.index('('):out.index(')') + 1]
    rest = out.split(')')[-1].strip()
    wrong = []
    try:
        dims = eval(sh)
        if len(dims) == 2:
            wrong += [f'{p[0]} ({dims[1]}, {dims[0]}) {rest}', f'{p[0]} {sh} {dims[0] + dims[1]}', f'{int(p[0]) + 1} {sh} {rest}']
        else:
            wrong += [f'2 ({dims[0]}, 1) {rest}', f'{p[0]} ({int(rest) + 1},) {int(rest) + 1}', f'{p[0]} {sh} {int(rest) - 1}']
    except Exception:
        pass
    wrong = np_fill(uniq(wrong, [out]), out)
    return mcq(f'What is the output of the following code?\n{NP}{code}', out, wrong[:3],
               f'ndim is the number of axes, shape gives the size along each axis, and size is the total number of elements. Output: {out}', r)


def np_create(r):
    t = r.randrange(5)
    if t == 0:
        s, e, st = r.randint(1, 6), r.randint(14, 25), r.choice([2, 3, 4, 5])
        code = f'a = np.arange({s}, {e}, {st})\nprint(a)'
        alts = [code.replace(f', {e},', f', {e + st},'), code.replace(f'({s},', f'({s + 1},'), code.replace(f', {st})', ')')]
        why = 'arange(start, stop, step) stops before stop.'
    elif t == 1:
        e, n = r.choice([(10, 5), (20, 5), (12, 4), (1, 5), (30, 4), (2, 5), (100, 5)])
        code = f'a = np.linspace(0, {e}, {n})\nprint(a)'
        alts = [f'a = np.linspace(0, {e}, {n}, endpoint=False)\nprint(a)', f'a = np.arange(0, {e}, {max(1, e // n)})\nprint(a)', f'a = np.linspace(0, {e}, {n + 1})\nprint(a)']
        why = 'linspace(start, stop, num) gives num equally spaced values including stop.'
    elif t == 2:
        rr, cc = r.randint(2, 3), r.randint(2, 4)
        code = f'a = np.ones(({rr}, {cc}), dtype=int)\nprint(a * {r.randint(2, 9)})'
        alts = [code.replace(f'({rr}, {cc})', f'({cc}, {rr})'), code.replace('ones', 'zeros'), code.replace(', dtype=int', '')]
        why = 'ones() fills the array with 1; the multiplication is element-wise.'
    elif t == 3:
        L = r.sample(range(1, 10), 4)
        k = r.randint(2, 3)
        code = f'L = {L}\nA = np.array(L)\nprint(L * {k})\nprint(A * {k})'
        alts = [code.replace(f'L * {k}', f'A * {k}'), code.replace(f'A * {k}', f'L * {k}'), code.replace(f'A * {k}', f'A + {k}')]
        why = '* on a list repeats it; * on an array multiplies each element.'
    else:
        L = r.sample(range(1, 10), 3)
        f = round(r.uniform(1, 9), 1)
        code = f'a = np.array({L + [f]})\nprint(a)\nprint(a.dtype)'
        alts = [f'a = np.array({L})\nprint(a)\nprint(a.dtype)', code.replace('print(a)\n', 'print(a.size)\n'), code.replace(str(f), str(int(f)))]
        why = 'All elements of a NumPy array have the same type, so the integers are converted to float.'
    return _np_mcq(r, code, alts, why)


def np_index(r):
    rows, cols = 3, 4
    data = [r.sample(range(10, 99), cols) for _ in range(rows)]
    i, j = r.randint(0, 2), r.randint(0, 3)
    t = r.randrange(6)
    if t == 0:
        e = f'a[{i}, {j}]'
    elif t == 1:
        e = f'a[{i}]'
    elif t == 2:
        e = f'a[:, {j}]'
    elif t == 3:
        e = f'a[0:2, 1:3]'
    elif t == 4:
        e = f'a[-1, ::-1]'
    else:
        e = f'a[{i}, {r.randint(0, 1)}:{r.randint(2, 4)}]'
    code = f'a = np.array({data})\nprint({e})'
    alts = [code.replace(f'a[{i}, {j}]', f'a[{j % 3}, {i}]'), code.replace(f'a[{i}]', f'a[:, {i}]'), code.replace(f'a[:, {j}]', f'a[{j % 3}]'),
            code.replace('a[0:2, 1:3]', 'a[1:3, 0:2]'), code.replace('a[-1, ::-1]', 'a[-1]'), code.replace('a[0:2, 1:3]', 'a[0:3, 1:2]'),
            code.replace('::-1', '::-2'), code.replace(f'a[{i},', f'a[{(i + 1) % 3},')]
    return _np_mcq(r, code, alts, 'Index a 2-D array as a[row, column]; a slice keeps the stop index out.')


def np_index_short(r):
    data = [r.sample(range(1, 50), 4) for _ in range(3)]
    i = r.randint(0, 2)
    code = f'a = np.array({data})\nprint(a[{i}, 1:3])\nprint(a[:, -1])\nprint(a[::2, 0])'
    return _np_short(code, 2, 'first line 1 mark, other two lines 1 mark')


def np_ops(r):
    a = r.sample(range(1, 20), 4)
    b = r.sample(range(1, 10), 4)
    k = r.randint(2, 5)
    t = r.randrange(7)
    exprs = {0: 'a + b', 1: 'a * b', 2: f'a ** 2 - b', 3: f'a // {k}', 4: f'a % {k}', 5: f'a > {sorted(a)[1]}', 6: 'b - a'}
    e = exprs[t]
    code = f'a = np.array({a})\nb = np.array({b})\nprint({e})'
    alts = [code.replace(e, x) for x in [exprs[(t + 1) % 7], exprs[(t + 3) % 7], e.replace('a', 'b', 1)]] + [code.replace('//', '/'), code.replace('% ', '// ')]
    return _np_mcq(r, code, alts, 'Arithmetic and comparison operators work element by element on arrays of the same shape.')


def np_2d_ops(r):
    data = [r.sample(range(1, 30), 3) for _ in range(2)]
    t = r.randrange(5)
    code = f'a = np.array({data})\n' + ['print(a.transpose())', 'print(np.sort(a))', 'print(np.sort(a, axis=0))', 'print(a * 2 + 1)', 'b = a.T\nprint(b.shape, b[0])'][t]
    alts = [code.replace('a.transpose()', 'a'), code.replace('np.sort(a)', 'np.sort(a, axis=0)'), code.replace(', axis=0', ''), code.replace('* 2 + 1', '* (2 + 1)'),
            code.replace('b[0]', 'a[0]'), code.replace('np.sort(a, axis=0)', 'np.sort(a.T)')]
    return _np_mcq(r, code, alts, 'transpose() turns rows into columns; np.sort() sorts along the last axis (each row) unless axis=0 is given.')


def np_reshape(r):
    n = r.choice([6, 8, 12])
    s = r.randint(1, 9)
    shapes = {6: [(2, 3), (3, 2)], 8: [(2, 4), (4, 2)], 12: [(3, 4), (4, 3), (2, 6), (6, 2)]}[n]
    p, q = r.choice(shapes)
    t = r.randrange(4)
    base = f'a = np.arange({s}, {s + n})\nb = a.reshape({p}, {q})\n'
    if t == 0:
        code = base + 'print(b)'
        alts = [base.replace(f'({p}, {q})', f'({q}, {p})') + 'print(b)', base + 'print(b.T)', base + 'print(a)']
    elif t == 1:
        code = base + f'print(b[{r.randint(0, p - 1)}], b.shape)'
        alts = [code.replace(f'reshape({p}, {q})', f'reshape({q}, {p})'), code.replace('b.shape', 'a.shape'), code.replace('print(b[', 'print(a[')]
    elif t == 2:
        code = base + 'print(b[:, 0])'
        alts = [base + 'print(b[0])', base + 'print(b[:, -1])', base.replace(f'({p}, {q})', f'({q}, {p})') + 'print(b[:, 0])']
    else:
        code = f'a = np.arange({s}, {s + n})\nb = a.reshape({p + 1}, {q})\nprint(b)'
        out = _np_or_err(code)
        assert out.startswith('Error (ValueError')
        return mcq(f'What happens when the following code is run?\n{NP}{code}', 'A ValueError, because the array of ' + str(n) + f' elements cannot be reshaped into {p + 1} × {q}',
                   [f'An array of {p + 1} rows and {q} columns is printed, with the missing places filled with 0', f'The array is printed with {p} rows only',
                    f'The array is printed in {q} rows of {p + 1} columns'], f'reshape() needs the same total number of elements: {p + 1} × {q} = {(p + 1) * q} ≠ {n}.', r)
    return _np_mcq(r, code, alts, 'reshape() keeps the elements in order and fills the new shape row by row.')


def np_concat(r):
    a = [r.sample(range(1, 20), 2) for _ in range(2)]
    b = [r.sample(range(20, 40), 2) for _ in range(2)]
    t = r.randrange(4)
    if t == 0:
        code = f'a = np.array({a})\nb = np.array({b})\nprint(np.concatenate((a, b), axis=0))'
        alts = [code.replace('axis=0', 'axis=1'), code.replace('(a, b)', '(b, a)'), code.replace('np.concatenate((a, b), axis=0)', 'a + b')]
    elif t == 1:
        code = f'a = np.array({a})\nb = np.array({b})\nprint(np.concatenate((a, b), axis=1))'
        alts = [code.replace('axis=1', 'axis=0'), code.replace('(a, b)', '(b, a)'), code.replace('np.concatenate((a, b), axis=1)', 'a * b')]
    elif t == 2:
        L = r.sample(range(1, 60), 6)
        k = r.choice([2, 3])
        code = f'a = np.array({L})\nx = np.split(a, {k})\nprint(x[1])'
        alts = [code.replace(f'split(a, {k})', f'split(a, {5 - k})'), code.replace('x[1]', 'x[0]'), code.replace('x[1]', 'x[-1]')]
    else:
        L = r.sample(range(1, 60), 7)
        i, j = r.choice([(2, 5), (1, 4), (3, 5), (2, 4)])
        code = f'a = np.array({L})\nx, y, z = np.split(a, [{i}, {j}])\nprint(y)'
        alts = [code.replace(f'[{i}, {j}]', f'[{i + 1}, {j + 1}]'), code.replace('print(y)', 'print(x)'), code.replace('print(y)', 'print(z)')]
    return _np_mcq(r, code, alts, 'concatenate() joins arrays along the given axis (0 = rows, 1 = columns); split() divides an array into equal parts or at the given indices.')


def np_concat_short(r):
    L = r.sample(range(1, 40), 6)
    p, q = r.choice([(2, 3), (3, 2)])
    code = f'a = np.array({L})\nb = a.reshape({p}, {q})\nc = np.concatenate((b, b * 2), axis={r.randint(0, 1)})\nprint(c.shape)\nprint(c)'
    return _np_short(code, 3, 'shape 1 mark, array 2 marks')


def np_stats(r):
    data = [r.sample(range(20, 99), 3) for _ in range(3)]
    t = r.randrange(6)
    code = f'm = np.array({data})\n' + ['print(m.max(), m.min())', 'print(m.sum(axis=0))', 'print(m.sum(axis=1))', 'print(m.max(axis=1))',
                                         'print(m.min(axis=0))', 'print(np.mean(m[0]))'][t]
    alts = [code.replace('axis=0', 'axis=1'), code.replace('axis=1', 'axis=0'), code.replace('m.max(), m.min()', 'm.max(axis=0), m.min(axis=0)'),
            code.replace('max', 'min'), code.replace('m[0]', 'm[:, 0]'), code.replace('sum', 'max')]
    return _np_mcq(r, code, alts, 'Without axis the whole array is used; axis=0 works down each column and axis=1 along each row.')


def np_stats_short(r):
    data = [r.sample(range(30, 99), 4) for _ in range(3)]
    code = f'm = np.array({data})\nprint(m.sum(axis=1))\nprint(m.max(axis=0))\nprint(np.mean(m[:, 0]))'
    return _np_short(code, 3, '1 mark per line')


def np_std(r):
    xs = _sd_data(r)
    mu, dev, sq, var, sd = sd_parts(xs)
    code = f'a = np.array({xs})\nprint(np.mean(a), np.var(a))\nprint(round(np.std(a), 2))'
    out = _np(code)
    assert out.split('\n')[1] == f'{round(sd, 2)}', (out, sd)
    return {'stem': f'Write the output of the following code:\n{NP}{code}', 'answer': out,
            'key': f'2 marks: mean {mu}, variance {sum(sq)} / {len(xs)} (1); standard deviation √variance (1). Output: {out.replace(chr(10), " / ")}', 'marks': 2}


FILES = [
    ('marks.csv', 'Roll,Eng,Maths,IP\n1,{a},{b},{c}\n2,{d},{e},{f}\n3,{g},{h},{i}\n'),
    ('sales.csv', 'Month,North,South,East\n1,{a},{b},{c}\n2,{d},{e},{f}\n3,{g},{h},{i}\n'),
]


def np_file(r):
    name, tpl = r.choice(FILES)
    v = {k: r.randint(40, 99) for k in 'abcdefghi'}
    content = tpl.format(**v)
    t = r.randrange(4)
    load = f'data = np.loadtxt("{name}", skiprows=1, delimiter=",", dtype=int)\n'
    code = load + ['print(data[:, 1:])', 'print(data[1])', 'print(data[:, 2].max(), data.shape)', 'print(data[:, 1:].sum(axis=1))'][t]
    out = run_files(NP + code, {name: content})
    alts = [code.replace('skiprows=1, ', ''), code.replace('data[:, 1:]', 'data'), code.replace('data[1]', 'data[0]'), code.replace('axis=1', 'axis=0'),
            code.replace('data[:, 2]', 'data[2]'), code.replace('data.shape', 'data.size')]
    wrong = [w for w in uniq([run_files_or_err(NP + c, {name: content}) for c in alts], [out]) if w.strip() and not w.startswith('Error')]
    wrong = np_fill(wrong, out)
    return mcq(f'The file {name} contains:\n{content.strip()}\nWhat is the output of the following code?\n{NP}{code}', out, wrong[:3],
               f'skiprows=1 skips the heading line and delimiter="," splits the columns. Output: {out}', r)


def np_genfromtxt(r):
    v = [r.randint(10, 90) for _ in range(6)]
    miss = r.randrange(6)
    cells = [str(x) if i != miss else '' for i, x in enumerate(v)]
    content = f'{cells[0]},{cells[1]},{cells[2]}\n{cells[3]},{cells[4]},{cells[5]}\n'
    fv = r.choice([-1, 0, -999])
    code = f'data = np.genfromtxt("scores.csv", delimiter=",", dtype=int, filling_values={fv})\nprint(data)'
    out = run_files(NP + code, {'scores.csv': content})
    return {'stem': f'The file scores.csv contains (one value is missing):\n{content.strip()}\nWrite the output of the following code and explain why genfromtxt() is used here instead of loadtxt().\n{NP}{code}',
            'answer': f'{out}\ngenfromtxt() handles the missing value by putting the filling value {fv} in its place; loadtxt() would raise an error for the missing value.',
            'key': '2 marks: output 1, reason 1.', 'marks': 2}


def np_case_create(r):
    who = r.choice(NAMES)
    s, e, st = r.randint(1, 5), r.randint(20, 30), r.choice([3, 4, 5])
    n = r.choice([4, 5, 6])
    code = f'import numpy as np\na = np.arange({s}, {e}, {st})\nb = np.linspace(0, {n - 1}, {n})\nc = np.zeros((2, 3), dtype=int)\nprint(a, a.size)\nprint(b)\nprint(c.shape, c.ndim)'
    lines = run(code).split('\n')
    return K._case(who, 'is learning how to create NumPy arrays:', code,
                   [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second and third print statements.', lines[1] + ' / ' + lines[2], 1),
                    ('Give two differences between the list [1, 2, 3] and np.array([1, 2, 3]).', 'A list can hold elements of different types, an array holds one type; '
                     'list * 2 repeats the list, array * 2 multiplies each element (arrays support element-wise arithmetic and use less memory)', 2)])


def np_case_ops(r):
    who = r.choice(NAMES)
    data = [r.sample(range(40, 99), 3) for _ in range(3)]
    code = f'import numpy as np\nm = np.array({data})\nprint(m[1], m[:, 2])\nprint(m + 5)\nprint(np.sort(m[0]), m.T[0])'
    lines = run(code).split('\n')
    p2 = '\n'.join(lines[1:-1])
    return K._case(who, 'stores the marks of three students (rows) in three subjects (columns):', code,
                   [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second print statement.', p2.replace('\n', ' '), 1),
                    ('Write the output of the last print statement and explain what m.T does.', lines[-1] + '; m.T is the transpose, so its first row is the first column of m', 2)])


def np_case_reshape(r):
    who = r.choice(NAMES)
    L = r.sample(range(10, 99), 12)
    code = f'import numpy as np\na = np.array({L})\nb = a.reshape(3, 4)\nx, y = np.split(b, 2, axis=1)\nprint(b[2])\nprint(x.shape, y[0])\nprint(np.concatenate((x, y), axis=0).shape)'
    lines = run(code).split('\n')
    return K._case(who, 'arranges the monthly readings of a year in an array:', code,
                   [('Write the output of the first print statement.', lines[0], 1), ('Write the output of the second print statement.', lines[1], 1),
                    ('Write the output of the third print statement. What would happen with b = a.reshape(5, 3)?', lines[2] + '; ValueError, because 12 elements cannot fill a 5 × 3 array', 2)])


def np_case_stats(r):
    who = r.choice(NAMES)
    data = [r.sample(range(35, 99), 4) for _ in range(3)]
    code = f'import numpy as np\nm = np.array({data})\nprint(m.sum(axis=1))\nprint(m.max(axis=0))\nprint(np.mean(m), m.min())'
    lines = run(code).split('\n')
    return K._case(who, 'analyses the marks of three students (rows) in four tests (columns):', code,
                   [('Write the output of the first print statement. What does it represent?', lines[0] + '; the total marks of each student', 1),
                    ('Write the output of the second print statement. What does it represent?', lines[1] + '; the highest mark in each test', 1),
                    ('Write the output of the third print statement and a statement to find the standard deviation of all the marks.', lines[2] + '; print(np.std(m))', 2)])


# ====================================================================== SQL (ch07, ch08)
def _tbl(r, nulls=True):
    return D.any_table(r, nulls=nulls)


def query_pool11(r, tname, cols, rows):
    """Class 11 single-table SELECT queries (no aggregates); every query fixes the row order with ORDER BY on a
    column with distinct values, or returns rows in primary-key (insertion) order."""
    numc, grp, namec, city, nullc = D.ROLES[tname]
    ni = cols.index(numc)
    vals = sorted(x[ni] for x in rows if x[ni] is not None)
    k = vals[r.randint(1, len(vals) - 3)]
    lo = vals[1]
    gvs = sorted({x[cols.index(grp)] for x in rows})
    gv = r.choice(gvs)
    letter = r.choice(sorted({x[cols.index(namec)][0] for x in rows}))
    second = r.choice(sorted({x[cols.index(namec)][1] for x in rows}))
    last = r.choice(sorted({x[cols.index(namec)][-1] for x in rows}))
    key = cols[0]
    qs = [
        f'SELECT {namec}, {numc} FROM {tname} WHERE {numc} > {k} ORDER BY {numc} DESC;',
        f'SELECT DISTINCT {grp} FROM {tname} ORDER BY {grp};',
        f'SELECT {namec} FROM {tname} WHERE {namec} LIKE \'{letter}%\' OR {namec} LIKE \'_{second}%\' ORDER BY {namec};',
        f'SELECT {namec} FROM {tname} WHERE {namec} LIKE \'%{last}\' ORDER BY {namec};',
        f'SELECT {namec}, {numc} FROM {tname} WHERE {numc} BETWEEN {lo} AND {k} ORDER BY {namec};',
        f'SELECT {key}, {namec} FROM {tname} WHERE {grp} IN (\'{gv}\', \'{r.choice(gvs)}\') ORDER BY {key};',
        f'SELECT {key}, {namec} FROM {tname} WHERE {grp} NOT IN (\'{gv}\') AND {numc} < {vals[-2]} ORDER BY {key};',
        f'SELECT {namec}, {grp} FROM {tname} WHERE {grp} <> \'{gv}\' ORDER BY {grp}, {namec};',
        f'SELECT {namec}, {numc} FROM {tname} ORDER BY {grp} DESC, {numc};',
    ]
    if tname == 'EMPLOYEE':
        qs += [f'SELECT Name, Salary * 12 AS Annual FROM EMPLOYEE WHERE Dept = \'{gv}\' ORDER BY Name;',
               f'SELECT Name, Salary + Bonus FROM EMPLOYEE WHERE Salary > {k} ORDER BY Name;']
    elif tname == 'STUDENT':
        qs += [f'SELECT Name, Marks + 5 AS NewMarks FROM STUDENT WHERE Stream = \'{gv}\' ORDER BY Name;',
               f'SELECT Name, Fee * 12 FROM STUDENT WHERE Class = \'XII\' ORDER BY RollNo;']
    else:
        qs += [f'SELECT PName, Price * Qty AS Amount FROM PRODUCT WHERE Category = \'{gv}\' ORDER BY PName;',
               f'SELECT PCode, Price - 5 FROM PRODUCT WHERE Qty < {sorted(x[4] for x in rows)[-2]} ORDER BY PCode;']
    if nullc:
        qs += [f'SELECT {namec} FROM {tname} WHERE {nullc} IS NULL ORDER BY {namec};', f'SELECT {key}, {nullc} FROM {tname} WHERE {nullc} IS NOT NULL ORDER BY {key};']
    if city:
        c = r.choice(sorted({x[cols.index(city)] for x in rows}))
        qs += [f'SELECT {namec}, {city} FROM {tname} WHERE {city} = \'{c}\' OR {numc} >= {k} ORDER BY {namec};']
    return qs


def _outcheck(db, q):
    o = db.result(q)
    if o.startswith('Empty'):
        raise ValueError('empty')
    return o


def sql_out11(r, n_q=1, marks=1):
    tname, cols, rows = _tbl(r)
    db = DB([(tname, cols, rows)])
    qs = r.sample(query_pool11(r, tname, cols, rows), n_q)
    outs = [_outcheck(db, q) for q in qs]
    tbl = show_table(tname, cols, rows)
    if n_q == 1:
        return {'stem': f'Consider the table given below.\n{tbl}\nWrite the output of the query:\n{qs[0]}', 'answer': outs[0],
                'key': f'{marks} mark{"s" if marks > 1 else ""} for the correct output (column headings and all rows):\n{outs[0]}', 'marks': marks}
    lab = ['i', 'ii', 'iii', 'iv'][:n_q]
    body = '\n'.join(f'({l}) {q}' for l, q in zip(lab, qs))
    ans = '\n'.join(f'({l})\n{o}' for l, o in zip(lab, outs))
    return {'stem': f'Consider the table given below.\n{tbl}\nWrite the output of the following queries:\n{body}', 'answer': ans,
            'key': f'{marks} marks: {marks / n_q:g} for each correct output.', 'marks': marks}


def sql_out11_mcq(r):
    tname, cols, rows = _tbl(r)
    db = DB([(tname, cols, rows)])
    pool = query_pool11(r, tname, cols, rows)
    q = r.choice(pool)
    out = _outcheck(db, q)
    alts = [q.replace(' > ', ' >= '), q.replace(' DESC', ''), q.replace('ORDER BY', 'ORDER BY 1 DESC,') if 'ORDER BY' in q else q, q.replace(' OR ', ' AND '),
            q.replace('NOT IN', 'IN'), q.replace(' <> ', ' = '), q.replace('IS NULL', 'IS NOT NULL'), q.replace('IS NOT NULL', 'IS NULL'),
            q.replace('BETWEEN', 'NOT BETWEEN'), q.replace("LIKE '%", "LIKE '"), q.replace('DISTINCT ', '')]
    wrong = []
    for a in alts:
        if a == q:
            continue
        try:
            o = db.result(a)
        except Exception:
            continue
        wrong.append(o)
    import re as _re
    nowhere = _re.sub(r' WHERE .*? ORDER BY', ' ORDER BY', q)
    flip = q.replace(' DESC', '') if ' DESC' in q else q.replace(';', ' DESC;')
    for a in (nowhere, flip):
        if a != q:
            try:
                wrong.append(db.result(a))
            except Exception:
                pass
    lines = out.split('\n')
    if len(lines) > 2:
        wrong += ['\n'.join(lines[:-1]), '\n'.join(lines[:1] + lines[2:])]
    wrong = uniq(wrong, [out])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'Consider the table given below.\n{show_table(tname, cols, rows)}\nWhich of the following is the output of the query:\n{q}', out, r.sample(wrong, 3),
               f'Apply the WHERE condition to each row, then sort as ORDER BY says. Output:\n{out}', r)


def tasks11(r, tname, cols, rows):
    numc, grp, namec, city, nullc = D.ROLES[tname]
    ni = cols.index(numc)
    vals = sorted(x[ni] for x in rows if x[ni] is not None)
    k = vals[len(vals) // 2]
    gvs = sorted({x[cols.index(grp)] for x in rows})
    gv = r.choice(gvs)
    letter = r.choice(sorted({x[cols.index(namec)][0] for x in rows}))
    T = [
        (f'Display all details of records whose {grp} is {gv}.', f"SELECT * FROM {tname} WHERE {grp} = '{gv}';"),
        (f'Display {namec} and {numc} in descending order of {numc}.', f'SELECT {namec}, {numc} FROM {tname} ORDER BY {numc} DESC;'),
        (f'Display the {namec} of records whose {namec} starts with "{letter}".', f"SELECT {namec} FROM {tname} WHERE {namec} LIKE '{letter}%';"),
        (f'Display the {namec} of records whose {namec} has "a" as the second letter.', f"SELECT {namec} FROM {tname} WHERE {namec} LIKE '_a%';"),
        (f'Display {namec} of records with {numc} between {vals[1]} and {k} (both inclusive).', f'SELECT {namec} FROM {tname} WHERE {numc} BETWEEN {vals[1]} AND {k};'),
        (f'Display the distinct values of {grp}.', f'SELECT DISTINCT {grp} FROM {tname};'),
        (f'Display {namec} and {grp} of records whose {grp} is either {gvs[0]} or {gvs[-1]}.', f"SELECT {namec}, {grp} FROM {tname} WHERE {grp} IN ('{gvs[0]}', '{gvs[-1]}');"),
        (f'Display all details of records whose {numc} is more than {k}, in alphabetical order of {namec}.', f'SELECT * FROM {tname} WHERE {numc} > {k} ORDER BY {namec};'),
        (f'Increase the {numc} of all records of {grp} {gv} by 10%.', f"UPDATE {tname} SET {numc} = {numc} * 1.10 WHERE {grp} = '{gv}';"),
        (f'Delete the records whose {numc} is less than {vals[0] + 1}.', f'DELETE FROM {tname} WHERE {numc} < {vals[0] + 1};'),
    ]
    if tname == 'EMPLOYEE':
        T += [('Display Name and annual salary (Salary * 12) with the column heading Annual.', 'SELECT Name, Salary * 12 AS Annual FROM EMPLOYEE;'),
              ('Display Name of employees who have not been given a bonus.', 'SELECT Name FROM EMPLOYEE WHERE Bonus IS NULL;'),
              ('Add a column Phone of type CHAR(10) to the table.', 'ALTER TABLE EMPLOYEE ADD Phone CHAR(10);')]
    elif tname == 'STUDENT':
        T += [('Display Name and Marks of students of class XII in descending order of Marks.', "SELECT Name, Marks FROM STUDENT WHERE Class = 'XII' ORDER BY Marks DESC;"),
              ('Display Name of students whose Marks are not entered.', 'SELECT Name FROM STUDENT WHERE Marks IS NULL;'),
              ('Display Name and Fee of students whose City is not Delhi.', "SELECT Name, Fee FROM STUDENT WHERE City <> 'Delhi';")]
    else:
        T += [('Display PName and the amount (Price * Qty) with the heading Amount.', 'SELECT PName, Price * Qty AS Amount FROM PRODUCT;'),
              ('Display PName and Price of products whose Qty is less than 20.', 'SELECT PName, Price FROM PRODUCT WHERE Qty < 20;'),
              ('Change the price of product P%02d to 100.' % int(rows[0][0][1:]), f"UPDATE PRODUCT SET Price = 100 WHERE PCode = '{rows[0][0]}';")]
    return T


def _check(db, q):
    if q.startswith('ALTER'):
        return
    if q.startswith('SELECT'):
        db.q(q)
    else:
        db.con.execute(q)


def sql_write11(r, n=4, marks=4):
    tname, cols, rows = _tbl(r)
    db = DB([(tname, cols, rows)])
    T = r.sample(tasks11(r, tname, cols, rows), n)
    for _, q in T:
        _check(db, q)
    lab = ['i', 'ii', 'iii', 'iv', 'v'][:n]
    return {'stem': f'Consider the table {tname} given below.\n{show_table(tname, cols, rows)}\nWrite SQL queries for the following:\n' +
                    '\n'.join(f'({l}) {t}' for l, (t, _) in zip(lab, T)),
            'answer': '\n'.join(f'({l}) {q}' for l, (_, q) in zip(lab, T)),
            'key': f'{marks} marks: {marks / n:g} for each correct query (½ for the correct clause, ½ for the correct condition).', 'marks': marks}


def sql_write11_1(r):
    tname, cols, rows = _tbl(r)
    t, q = r.choice([x for x in tasks11(r, tname, cols, rows) if x[1].startswith('SELECT')])
    _check(DB([(tname, cols, rows)]), q)
    return {'stem': f'Table {tname} has the columns {", ".join(cols)}. Write an SQL query to: {t[0].lower() + t[1:]}', 'answer': q, 'key': f'1 mark: {q}', 'marks': 1}


def _sqlval(v):
    if v is None:
        return 'NULL'
    return f"'{v}'" if isinstance(v, str) else str(v)


def insert_write(r):
    tname, cols, rows = _tbl(r, nulls=False)
    db = DB([(tname, cols, rows)])
    new = list(rows[-1])
    if isinstance(new[0], int):
        new[0] = new[0] + r.randint(1, 5)
    else:
        new[0] = f'P{int(new[0][1:]) + r.randint(1, 5):02d}'
    new[1] = r.choice([x for x in NAMES if x not in {row[1] for row in rows}]) if tname != 'PRODUCT' else r.choice(['Stapler', 'Glue', 'Scale', 'Crayon'])
    q = f'INSERT INTO {tname} VALUES ({", ".join(_sqlval(v) for v in new)});'
    db.con.execute(q)
    n = len(db.q(f'SELECT * FROM {tname}')[1])
    spec = ', '.join(f'{c} = {v}' for c, v in zip(cols, new))
    return {'stem': f'Consider the table {tname} given below.\n{show_table(tname, cols, rows)}\nWrite an SQL command to add the row: {spec}. What will be the cardinality of the table after this?',
            'answer': f'{q}\nCardinality after insertion: {n}', 'key': '2 marks: correct INSERT command 1 (text and date values in quotes), cardinality 1.', 'marks': 2}


def dml_effect(r):
    tname, cols, rows = _tbl(r, nulls=False)
    numc, grp, namec, city, nullc = D.ROLES[tname]
    vals = sorted(x[cols.index(numc)] for x in rows)
    k = vals[r.randint(1, len(vals) - 2)]
    db = DB([(tname, cols, rows)])
    gv = r.choice(sorted({x[cols.index(grp)] for x in rows}))
    t = r.randrange(3)
    if t == 0:
        cmd = f'DELETE FROM {tname} WHERE {numc} < {k};'
        db.con.execute(cmd)
        n = len(db.q(f'SELECT * FROM {tname}')[1])
        return mcq(f'{show_table(tname, cols, rows)}\nHow many rows will the table {tname} have after the command:\n{cmd}', str(n),
                   uniq([str(len(rows)), str(len(rows) - n), str(n - 1), '0', str(n + 1)], [str(n)])[:3], f'{len(rows) - n} row(s) with {numc} below {k} are deleted; {n} remain.', r)
    if t == 1:
        cmd = f'UPDATE {tname} SET {numc} = {numc} + 10 WHERE {grp} = \'{gv}\';'
        n = db.con.execute(cmd).rowcount
        return mcq(f'{show_table(tname, cols, rows)}\nHow many rows are changed by the command:\n{cmd}', str(n),
                   uniq([str(len(rows)), str(len(rows) - n), str(n + 1), str(max(n - 1, 0)), '0'], [str(n)])[:3], f'{n} row(s) have {grp} = {gv}.', r)
    cmd = f'UPDATE {tname} SET {numc} = {numc} + 10 WHERE {numc} >= {k};'
    db.con.execute(cmd)
    q = f'SELECT {namec}, {numc} FROM {tname} WHERE {numc} >= {k + 10} ORDER BY {numc};'
    out = _outcheck(db, q)
    db2 = DB([(tname, cols, rows)])
    w = [db2.result(q), db2.result(q.replace(f'>= {k + 10}', f'>= {k}'))]
    db3 = DB([(tname, cols, rows)])
    db3.con.execute(cmd.replace('>=', '>'))
    w.append(db3.result(q))
    db4 = DB([(tname, cols, rows)])
    db4.con.execute(cmd.replace('+ 10', '+ 20'))
    w.append(db4.result(q))
    wrong = uniq(w, [out])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'{show_table(tname, cols, rows)}\nThe following commands are run one after the other:\n{cmd}\n{q}\nWhat is the output of the SELECT query?', out, wrong[:3],
               f'Rows with {numc} ≥ {k} get 10 more; then those with {numc} ≥ {k + 10} are listed.\n{out}', r)


def dml_case(r):
    who = r.choice(NAMES)
    tname, cols, rows = _tbl(r, nulls=False)
    numc, grp, namec, city, nullc = D.ROLES[tname]
    db = DB([(tname, cols, rows)])
    vals = sorted(x[cols.index(numc)] for x in rows)
    k = vals[1]
    gv = r.choice(sorted({x[cols.index(grp)] for x in rows}))
    inc = {'Salary': 1000, 'Marks': 5, 'Price': 10}[numc]
    up = f"UPDATE {tname} SET {numc} = {numc} + {inc} WHERE {grp} = '{gv}';"
    de = f'DELETE FROM {tname} WHERE {numc} <= {k};'
    n_up = db.con.execute(up).rowcount
    n_de = db.con.execute(de).rowcount
    q = f'SELECT {namec}, {numc} FROM {tname} WHERE {grp} = \'{gv}\' ORDER BY {namec};'
    out = db.result(q)
    left = len(db.q(f'SELECT * FROM {tname}')[1])
    return {'stem': (f'{who} manages the table {tname} given below.\n{show_table(tname, cols, rows)}\n'
                     f'(i) Write a command to increase the {numc} of every record of {grp} {gv} by {inc}. How many rows will change? (1)\n'
                     f'(ii) Write a command to delete the records whose {numc} is {k} or less. (1)\n'
                     f'(iii) After the commands of (i) and (ii) are run, write the output of:\n{q} (1)\n'
                     f'(iv) How many rows are left in the table? Name the category (DDL or DML) of the commands used. (1)'),
            'answer': f'(i) {up} – {n_up} row(s) (ii) {de} (iii)\n{out}\n(iv) {left} rows; UPDATE and DELETE are DML commands.',
            'key': '1 mark each.', 'marks': 4}


def ddl_case(r):
    who = r.choice(NAMES)
    name, cols = r.choice([('BOOK', [('BookNo', 'INT', 'PRIMARY KEY'), ('Title', 'VARCHAR(40)', 'NOT NULL'), ('Author', 'VARCHAR(30)', ''), ('Price', 'FLOAT', '')]),
                           ('CUSTOMER', [('CustId', 'INT', 'PRIMARY KEY'), ('CName', 'VARCHAR(30)', 'NOT NULL'), ('Phone', 'CHAR(10)', 'UNIQUE'), ('City', 'VARCHAR(20)', '')]),
                           ('VEHICLE', [('RegNo', 'CHAR(10)', 'PRIMARY KEY'), ('Owner', 'VARCHAR(30)', 'NOT NULL'), ('Model', 'VARCHAR(20)', ''), ('RegDate', 'DATE', '')])])
    db = r.choice(['SCHOOL', 'SHOPDB', 'CITYDB', 'RECORDS'])
    create = f'CREATE TABLE {name} (' + ', '.join(f'{c} {d}' + (f' {k}' if k else '') for c, d, k in cols) + ');'
    import sqlite3
    sqlite3.connect(':memory:').execute(create)
    spec = '; '.join(f'{c} {d}' + (f' ({k})' if k else '') for c, d, k in cols)
    return {'stem': (f'{who} wants to store data in MySQL.\n(i) Write commands to create a database {db} and open it for use. (1)\n'
                     f'(ii) Write a command to create the table {name} with the columns {spec}. (1)\n'
                     f'(iii) Write a command to view the structure of the table. (1)\n(iv) Write commands to add a column Remarks VARCHAR(50) and then remove the column {cols[2][0]}. (1)'),
            'answer': f'(i) CREATE DATABASE {db}; USE {db}; (ii) {create} (iii) DESCRIBE {name}; (or DESC {name};) (iv) ALTER TABLE {name} ADD Remarks VARCHAR(50); ALTER TABLE {name} DROP {cols[2][0]};',
            'key': '1 mark each.', 'marks': 4}


def constr_case(r):
    who = r.choice(NAMES)
    t = r.choice([
        ('HOSPITAL patients', 'PID', 'PName', 'Phone', 'Ward', 'General'),
        ('LIBRARY members', 'MemberId', 'MName', 'Email', 'MemberType', 'Student'),
        ('SPORTS club players', 'PlayerId', 'PlayerName', 'Phone', 'Sport', 'Cricket')])
    what, pk, nm, uq, dc, dv = t
    return {'stem': (f'{who} is designing a table to store {what} with the columns {pk}, {nm}, {uq}, {dc} and JoinDate.\n'
                     f'(i) Which constraint should be applied to {pk}, and why? (1)\n(ii) {nm} must always be filled in. Which constraint is needed? (1)\n'
                     f'(iii) No two rows may share a {uq}, but it may be left blank. Which constraint is needed? (1)\n'
                     f'(iv) If {dc} is not given it should be stored as \'{dv}\'. Write the column definition, and suggest a data type for JoinDate. (1)'),
            'answer': (f'(i) PRIMARY KEY – it identifies each row uniquely and cannot be NULL (ii) NOT NULL (iii) UNIQUE (iv) {dc} VARCHAR(20) DEFAULT \'{dv}\'; '
                       f'JoinDate DATE'),
            'key': '1 mark each.', 'marks': 4}


def null_q(r):
    tname, cols, rows = D.emp_table(r) if r.random() < 0.5 else D.stu_table(r)
    numc, grp, namec, city, nullc = D.ROLES[tname]
    db = DB([(tname, cols, rows)])
    t = r.randrange(2)
    q = f'SELECT {namec} FROM {tname} WHERE {nullc} IS NULL ORDER BY {namec};' if t == 0 else f'SELECT {namec} FROM {tname} WHERE {nullc} IS NOT NULL ORDER BY {namec};'
    out = _outcheck(db, q)
    w = [db.result(q.replace('IS NOT NULL', 'IS NULL') if t else q.replace('IS NULL', 'IS NOT NULL')), db.result(f'SELECT {namec} FROM {tname} ORDER BY {namec};'),
         'Empty set (no rows)']
    wrong = uniq(w, [out])
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'{show_table(tname, cols, rows)}\nWhat is the output of the query:\n{q}', out, wrong[:3],
               f'NULL means a missing value; it is tested with IS NULL / IS NOT NULL, not with = NULL.\n{out}', r)
