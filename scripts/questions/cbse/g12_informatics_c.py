"""CBSE class 12 Informatics Practices (065), chapters 4-6: plotting with Matplotlib, computer networks and the
Internet and web, societal impacts.

Chapter 4 answers are worked out from Matplotlib's documented rules (format strings, default x values, default
bar width, histogram bins that include the left edge and, for the last bin only, the right edge) using numpy;
the accuracy check re-runs every chart program and reads the drawn figure back with Matplotlib.
Chapter 5 reuses the network generators of the Computer Science bank (g12_computer_science_c).
"""
from __future__ import annotations

import copy

import numpy as np

from qbank import F, mcq, CITIES
from g12_computer_science_kit import ST, uniq, NAMES, deck
import g12_computer_science_c as CSC
from g12_hum_engine import Sub

S = 'cbse-g12-informatics-ch'


def STc(sid, topic, text):
    """ST with the corrected statement of each S- line starting with a capital letter."""
    out = []
    for line in text.strip().splitlines():
        if line.startswith('S-: ') and ' | ' in line:
            a, c = line.split(' | ', 1)
            w = c.split(' ', 1)[0]
            if w.isalpha():
                line = f'{a} | {c[0].upper()}{c[1:]}'
        out.append(line)
    return ST(sid, topic, '\n'.join(out))

# ====================================================================== ch04 matplotlib
COLORS = {'b': 'blue', 'g': 'green', 'r': 'red', 'c': 'cyan', 'm': 'magenta', 'y': 'yellow', 'k': 'black'}
MARKERS = {'o': 'circle', 's': 'square', '^': 'upward triangle', 'v': 'downward triangle', '*': 'star', '+': 'plus', 'x': 'cross (x)', 'D': 'diamond', 'p': 'pentagon'}
LINES = {'-': 'solid', '--': 'dashed', '-.': 'dash-dot', ':': 'dotted'}


def describe(c, ls, m):
    return f'{COLORS[c]} {LINES[ls]} line with {MARKERS[m]} markers'


def fmt_pick(r):
    c, ls, m = r.choice(list(COLORS)), r.choice(list(LINES)), r.choice(list(MARKERS))
    order = r.randrange(3)
    fmt = [c + ls + m, c + m + ls, m + ls + c][order]
    x = r.sample(range(1, 30), 4)
    ans = describe(c, ls, m)
    c2 = r.choice([k for k in COLORS if k != c])
    l2 = r.choice([k for k in LINES if k != ls])
    m2 = r.choice([k for k in MARKERS if k != m])
    wrong = [describe(c2, ls, m), describe(c, l2, m), describe(c, ls, m2), describe(c2, l2, m)]
    return mcq(f"How is the line drawn by plt.plot({sorted(x)}, {x}, '{fmt}') displayed?", ans, r.sample(wrong, 3),
               f"In the format string, '{c}' is the colour ({COLORS[c]}), '{ls}' the line style ({LINES[ls]}) and '{m}' the marker ({MARKERS[m]}).", r)


def fmt_write(r):
    c, ls, m = r.choice(list(COLORS)), r.choice(list(LINES)), r.choice(list(MARKERS))
    who = r.choice(NAMES)
    v = r.sample(range(10, 60), 5)
    return {'stem': f'{who} wants to plot the values {v} as a {describe(c, ls, m)}. Write the plt.plot() statement using a format string (x values 1 to 5).',
            'answer': f"plt.plot([1, 2, 3, 4, 5], {v}, '{c}{ls}{m}')  (or color='{COLORS[c]}', linestyle='{ls}', marker='{m}')",
            'key': f"1 mark: x and y lists; format string has colour '{c}', line style '{ls}' and marker '{m}' in any order.", 'marks': 1}


def xdefault(r):
    n = r.randint(4, 7)
    y = r.sample(range(5, 99), n)
    ans = ', '.join(str(i) for i in range(n))
    wrong = [', '.join(str(i) for i in range(1, n + 1)), ', '.join(str(v) for v in y), ', '.join(str(i) for i in range(0, 2 * n, 2))]
    return mcq(f'plt.plot({y}) is called with only one list. What are the x-coordinates of the plotted points?', ans, wrong,
               'With a single list, the values are taken as y and the x values are the indices 0, 1, 2, …', r)


FUNC_SCEN = [('give the chart a heading', 'plt.title()'), ('label the horizontal axis', 'plt.xlabel()'), ('label the vertical axis', 'plt.ylabel()'),
             ('show which line stands for which data series', 'plt.legend()'), ('draw grid lines on the plot area', 'plt.grid()'),
             ('save the chart as an image file', 'plt.savefig()'), ('display the chart on screen', 'plt.show()'),
             ('set the positions and labels of the ticks on the x-axis', 'plt.xticks()'), ('draw a horizontal bar chart', 'plt.barh()'),
             ('draw a frequency distribution of continuous data', 'plt.hist()'), ('draw vertical bars for categories', 'plt.bar()'),
             ('draw a line chart', 'plt.plot()')]
FUNCS = [f for _, f in FUNC_SCEN]


def func_pick(r):
    d, f = r.choice(FUNC_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} wants to {d} using pyplot. Which function should be used?', f, r.sample([x for x in FUNCS if x != f], 3), f'{f} is used to {d}.', r)


DATASETS = [
    ('monthly rainfall (mm) of {city}', 'Month', ['Jun', 'Jul', 'Aug', 'Sep', 'Oct'], 'Rainfall (mm)', (40, 400)),
    ('runs scored by {name} in five matches', 'Match', ['M1', 'M2', 'M3', 'M4', 'M5'], 'Runs', (5, 120)),
    ('daily maximum temperature (°C) of {city} in a week', 'Day', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], 'Temperature (°C)', (24, 46)),
    ('quarterly sales (₹ lakh) of a shop in {city}', 'Quarter', ['Q1', 'Q2', 'Q3', 'Q4'], 'Sales (₹ lakh)', (10, 90)),
    ('number of visitors to a museum in {city} by year', 'Year', ['2021', '2022', '2023', '2024', '2025'], 'Visitors (thousand)', (20, 150)),
    ('marks of {name} in five unit tests', 'Test', ['UT1', 'UT2', 'UT3', 'UT4', 'UT5'], 'Marks', (35, 100)),
]


def dataset(r):
    t, xl, xs, yl, (lo, hi) = r.choice(DATASETS)
    t = t.format(city=r.choice(CITIES), name=r.choice(NAMES))
    ys = [r.randint(lo, hi) for _ in xs]
    return t, xl, xs, yl, ys


def line_program(r, marks=3):
    t, xl, xs, yl, ys = dataset(r)
    c, ls, m = r.choice(list(COLORS)), r.choice(list(LINES)), r.choice(list(MARKERS))
    title = t[0].upper() + t[1:]
    steps = [f'plot {yl} against {xl} as a {COLORS[c]} {LINES[ls]} line with {MARKERS[m]} markers', f'give the title "{title}"', 'label both axes']
    code = ['import matplotlib.pyplot as plt', f'x = {xs}', f'y = {ys}', f"plt.plot(x, y, color='{COLORS[c]}', linestyle='{ls}', marker='{m}')",
            f"plt.title('{title}')", f"plt.xlabel('{xl}')", f"plt.ylabel('{yl}')"]
    if marks >= 4:
        steps.append('show grid lines')
        code.append('plt.grid(True)')
    if marks >= 5:
        f = r.choice(['chart.png', 'report.pdf', 'trend.jpg'])
        steps.append(f'save the chart as {f}')
        code.append(f"plt.savefig('{f}')")
    code.append('plt.show()')
    stem = f'The {t} is: ' + ', '.join(f'{a}: {b}' for a, b in zip(xs, ys)) + '.\nWrite a Python program using pyplot to ' + '; '.join(steps) + '; and display the chart.'
    return {'stem': stem, 'answer': '\n'.join(code), 'key': f'{marks} marks: import and data ½–1, plot() with the required style 1, title/labels 1' +
            (', grid ½–1' if marks >= 4 else '') + (', savefig 1' if marks >= 5 else '') + '; any equivalent code (format string or keyword arguments) earns full marks.', 'marks': marks}


def two_line_program(r, marks=5):
    city1, city2 = r.sample(CITIES, 2)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    a = [r.randint(25, 45) for _ in days]
    b = [r.randint(25, 45) for _ in days]
    c1, c2 = r.sample(list(COLORS), 2)
    m1, m2 = r.sample(list(MARKERS), 2)
    stem = (f'The maximum temperatures (°C) of {city1} and {city2} from Monday to Friday are {a} and {b}. Write a program to plot both on the same chart: '
            f'{city1} as a {COLORS[c1]} line with {MARKERS[m1]} markers and {city2} as a {COLORS[c2]} dashed line with {MARKERS[m2]} markers; add the title '
            f'"Temperature Comparison", axis labels "Day" and "Temperature", a legend, and save the chart as temp.png.')
    code = ['import matplotlib.pyplot as plt', f'days = {days}', f"plt.plot(days, {a}, color='{COLORS[c1]}', marker='{m1}', label='{city1}')",
            f"plt.plot(days, {b}, color='{COLORS[c2]}', linestyle='--', marker='{m2}', label='{city2}')", "plt.title('Temperature Comparison')",
            "plt.xlabel('Day')", "plt.ylabel('Temperature')", 'plt.legend()', "plt.savefig('temp.png')", 'plt.show()']
    return {'stem': stem, 'answer': '\n'.join(code), 'key': '5 marks: import and data 1, two plot() calls with styles and labels 2, title and axis labels 1, legend and savefig 1.', 'marks': marks}


ERRS = [("plt.xlabel('{xl}')", "plt.xlable('{xl}')", 'xlable() should be xlabel()'),
        ("plt.title('{t}')", "plt.titel('{t}')", 'titel() should be title()'),
        ('plt.show()', 'plt.Show()', 'Show() should be show() (Python is case-sensitive)'),
        ("plt.plot(x, y, color='red', label='{yl}')", "plt.plot(x, y, colour='red', label='{yl}')", "the keyword is color, not colour"),
        ('plt.legend()', 'plt.legends()', 'legends() should be legend()'),
        ("plt.ylabel('{yl}')", "plt.ylabel = '{yl}'", "ylabel is a function: plt.ylabel('…')")]


def cap1(x):
    return x[0].upper() + x[1:]


def plot_errors(r):
    t, xl, xs, yl, ys = dataset(r)
    good = ['import matplotlib.pyplot as plt', f'x = {xs}', f'y = {ys}', "plt.plot(x, y, color='red', label='{yl}')", "plt.title('{t}')", "plt.xlabel('{xl}')",
            "plt.ylabel('{yl}')", 'plt.legend()', 'plt.show()']
    good = [g.format(t=cap1(t.split(' of ')[0]), xl=xl, yl=yl) for g in good]
    pick = r.sample(ERRS, 2)
    bad = good[:]
    notes = []
    for g, b, why in pick:
        gg = g.format(t=cap1(t.split(' of ')[0]), xl=xl, yl=yl)
        bb = b.format(t=cap1(t.split(' of ')[0]), xl=xl, yl=yl)
        i = bad.index(gg)
        bad[i] = bb
        notes.append((bb, gg, why))
    stem = 'The following code has two errors. Rewrite the incorrect statements correctly:\n' + '\n'.join(bad)
    ans = '\n'.join(f'{b}  →  {g}   ({why})' for b, g, why in notes)
    return {'stem': stem, 'answer': ans, 'key': '1 mark for each corrected statement.', 'marks': 2, '_good': '\n'.join(good), '_bad': '\n'.join(bad)}


# ---------------------------------------------------------------- st2 bar and histogram
def hist_counts(data, bins):
    n, _ = np.histogram(data, bins=bins)
    return [int(v) for v in n]


def hist_data(r):
    kind = r.choice([('marks of {n} students in a test', 30, 100), ('ages of {n} members of a club', 10, 70), ('heights (cm) of {n} plants', 20, 80),
                     ('weights (kg) of {n} students', 35, 75)])
    n = r.randint(12, 16)
    lo, hi = kind[1], kind[2]
    w = r.choice([10, 10, 5]) if hi - lo <= 40 else 10
    start = lo - lo % w
    edges = list(range(start, hi + w, w))
    if len(edges) > 8:
        edges = edges[:8]
    data = [r.randint(edges[0], edges[-1]) for _ in range(n)]
    return kind[0].format(n=n), data, edges


def hist_bin(r):
    what, data, edges = hist_data(r)
    cnt = hist_counts(data, edges)
    i = r.randrange(len(cnt))
    lo, hi = edges[i], edges[i + 1]
    ans = str(cnt[i])
    last = i == len(cnt) - 1
    naive = sum(lo <= v <= hi for v in data)
    excl = sum(lo < v <= hi for v in data)
    wrong = uniq([str(naive), str(excl), str(cnt[i] + 1), str(max(cnt[i] - 1, 0)), str(len(edges) - 1), str(cnt[i] + 2)], [ans])
    rule = ('the last bin includes both edges' if last else f'a bin includes its left edge and excludes its right edge, so {hi} goes to the next bin')
    return mcq(f'The {what} are {data}.\nplt.hist(data, bins={edges}) is used. What is the height of the bar for the bin {lo}–{hi}?', ans, wrong[:3],
               f'Count values v with {lo} ≤ v {"≤" if last else "<"} {hi}: {cnt[i]} ({rule}).', r)


def hist_freq(r, marks=2):
    what, data, edges = hist_data(r)
    cnt = hist_counts(data, edges)
    cum = r.random() < 0.3
    if cum:
        cnt = list(np.cumsum(cnt))
        cnt = [int(v) for v in cnt]
    rows = '\n'.join(f'{edges[i]}–{edges[i + 1]}: {c}' for i, c in enumerate(cnt))
    stem = (f'The {what} are {data}.\nThe statement plt.hist(data, bins={edges}' + (', cumulative=True' if cum else '') +
            ') draws a histogram. How many bars are drawn, and what is the height of each bar?')
    return {'stem': stem, 'answer': f'{len(cnt)} bars. Heights:\n{rows}',
            'key': f'{marks} marks: number of bars ½, heights 1½. Each bin includes its left edge; only the last bin also includes its right edge' +
            ('; with cumulative=True each bar shows the running total.' if cum else '.'), 'marks': marks}


def bar_count(r):
    t = r.randrange(3)
    n = r.randint(4, 7)
    xs = r.sample(['Delhi', 'Pune', 'Agra', 'Goa', 'Surat', 'Patna', 'Ranchi', 'Shimla', 'Indore', 'Kochi'], n)
    ys = r.sample(range(10, 99), n)
    if t == 0:
        return mcq(f'How many bars are drawn by plt.bar({xs}, {ys})?', str(n), [str(n - 1), str(n + 1), str(2 * n)], f'One bar for each of the {n} categories.', r)
    if t == 1:
        return mcq(f'What is the width of each bar drawn by plt.bar({xs}, {ys}) when no width is given?', '0.8', ['1.0', '0.5', '0.25'], 'The default width of bar() is 0.8.', r)
    i = r.randrange(n)
    return mcq(f'In plt.barh({xs}, {ys}), how long is the bar for {xs[i]}, and in which direction does it extend?', f'{ys[i]} units, horizontally',
               [f'{ys[i]} units, vertically', f'{i} units, horizontally', f'{sum(ys)} units, horizontally'], 'barh() draws horizontal bars whose lengths are the values.', r)


BAR_SETS = [('medals won by states in a sports meet', 'State', ['Haryana', 'Punjab', 'Kerala', 'Manipur', 'Odisha'], 'Medals', (5, 60)),
            ('books issued from a school library by class', 'Class', ['VIII', 'IX', 'X', 'XI', 'XII'], 'Books issued', (40, 200)),
            ('trees planted by eco-clubs of {city} schools', 'School', ['KV-1', 'KV-2', 'DPS', 'JNV', 'GHSS'], 'Trees', (20, 150)),
            ('votes received by candidates in a class election', 'Candidate', ['Aarav', 'Diya', 'Kabir', 'Meera'], 'Votes', (5, 40)),
            ('mobile phones sold by a shop in {city} by brand', 'Brand', ['A', 'B', 'C', 'D', 'E'], 'Units sold', (10, 80))]


def bar_program(r, marks=3):
    t, xl, xs, yl, (lo, hi) = r.choice(BAR_SETS)
    t = t.format(city=r.choice(CITIES))
    ys = [r.randint(lo, hi) for _ in xs]
    col = r.choice(['green', 'orange', 'purple', 'skyblue', 'brown'])
    horiz = r.random() < 0.3
    fn = 'barh' if horiz else 'bar'
    code = ['import matplotlib.pyplot as plt', f'x = {xs}', f'y = {ys}', f"plt.{fn}(x, y, color='{col}')", f"plt.title('{t[0].upper() + t[1:]}')",
            f"plt.xlabel('{yl if horiz else xl}')", f"plt.ylabel('{xl if horiz else yl}')"]
    steps = [f'draw a {"horizontal " if horiz else ""}bar chart in {col} colour', 'add a suitable title and axis labels']
    if marks >= 4:
        w = r.choice([0.4, 0.5, 0.6])
        code[3] = f"plt.{fn}(x, y, color='{col}', {'height' if horiz else 'width'}={w})"
        steps[0] += f' with bar {"height" if horiz else "width"} {w}'
        steps.append('save it as bars.png')
        code.append("plt.savefig('bars.png')")
    code.append('plt.show()')
    stem = f'The {t} are: ' + ', '.join(f'{a} {b}' for a, b in zip(xs, ys)) + '.\nWrite a Python program to ' + '; '.join(steps) + '.'
    return {'stem': stem, 'answer': '\n'.join(code), 'key': f'{marks} marks: import and lists 1, {fn}() with colour 1, title and labels 1' + (', width/height and savefig 1' if marks >= 4 else '') + '.', 'marks': marks}


def hist_program(r, marks=3):
    what, data, edges = hist_data(r)
    col = r.choice(['yellow', 'pink', 'cyan', 'orange'])
    ec = r.choice(['black', 'red', 'blue'])
    step = r.random() < 0.4
    code = ['import matplotlib.pyplot as plt', f'data = {data}', f"plt.hist(data, bins={edges}, color='{col}', edgecolor='{ec}'" + (", histtype='step'" if step else '') + ')',
            f"plt.title('Histogram of {what.split(' of ')[0]}')", "plt.xlabel('Range')", "plt.ylabel('Frequency')", 'plt.show()']
    stem = (f'The {what} are {data}. Write a program to draw a histogram with the bins {edges}, ' +
            (f'drawn as an unfilled step outline in {col}, ' if step else f'bars in {col} with {ec} edges, ') + 'a title, and the axis labels "Range" and "Frequency".')
    if step:
        code[2] = f"plt.hist(data, bins={edges}, color='{col}', histtype='step')"
    return {'stem': stem, 'answer': '\n'.join(code), 'key': f'{marks} marks: import and data 1, hist() with bins and style 1, title and labels 1.', 'marks': marks}


# ---------------------------------------------------------------- st3 plotting from a DataFrame, saving
def df_plot_count(r):
    n = r.randint(3, 5)
    names = r.sample(NAMES, n)
    cols = r.sample(['Eng', 'Maths', 'Science', 'IP', 'Hindi'], r.randint(2, 4))
    data = {'Name': names}
    for c in cols:
        data[c] = r.sample(range(40, 100), n)
    lit = '{' + ', '.join(f"'{k}': {v}" for k, v in data.items()) + '}'
    t = r.randrange(4)
    m = len(cols)
    if t == 0:
        q, a, w = "df.plot(kind='bar', x='Name')", n * m, [n, m, n + m]
        why = f'{n} groups (one per row) of {m} bars (one per numeric column) = {n * m} bars.'
        what = 'How many bars are drawn'
    elif t == 1:
        y = r.choice(cols)
        q, a, w = f"df.plot(kind='barh', x='Name', y='{y}')", n, [m, n * m, 1]
        why = f'Only the column {y} is plotted: one bar per row = {n}.'
        what = 'How many bars are drawn'
    elif t == 2:
        q, a, w = "df.plot(kind='line', x='Name')", m, [n, n * m, 1]
        why = f'One line for each numeric column other than x: {m}.'
        what = 'How many lines are drawn'
    else:
        y = r.sample(cols, min(2, m))
        q, a, w = f"df.plot(kind='bar', x='Name', y={y})", n * len(y), [n, len(y), n * m]
        why = f'{n} rows × {len(y)} chosen columns = {n * len(y)} bars.'
        what = 'How many bars are drawn'
    wrong = uniq([str(x) for x in w] + [str(a + 1), str(a + 2)], [str(a)])
    return mcq(f'import pandas as pd\nimport matplotlib.pyplot as plt\ndf = pd.DataFrame({lit})\n{q}\nplt.show()\n{what}?', str(a), wrong[:3], why, r)


SAVE_SCEN = [("plt.savefig('sales.pdf')", 'a PDF file named sales.pdf'), ("plt.savefig('sales.png')", 'a PNG image named sales.png'),
             ("plt.savefig('sales.jpg')", 'a JPEG image named sales.jpg'), ("plt.savefig('sales.svg')", 'an SVG (vector) file named sales.svg'),
             ("plt.savefig('sales')", 'a PNG image named sales.png (PNG is the default format)')]


def save_pick(r):
    s, a = r.choice(SAVE_SCEN)
    folder = r.choice(['', 'D:/charts/', 'C:/IP/'])
    s2 = s.replace("('", f"('{folder}")
    a2 = a.replace('named ', f'named {folder}') if folder else a
    wrong = [x.replace('named ', f'named {folder}') if folder else x for _, x in SAVE_SCEN if x != a]
    return mcq(f'What does {s2} create?', a2, r.sample(wrong, 3), 'savefig() takes the format from the file extension; without an extension it saves a PNG.', r)


KIND_SCEN = [('compare the sales of five products', 'bar'), ('show the trend of monthly temperature over a year', 'line'),
             ('show how the marks of 60 students are distributed over ranges', 'hist'), ('compare category totals with horizontal bars', 'barh'),
             ('show the share of each expense head in the total budget', 'pie'), ('show the relation between hours studied and marks of each student', 'scatter'),
             ('show the median and quartiles of the marks of a class', 'box')]
KINDS = ['bar', 'line', 'hist', 'barh', 'pie', 'scatter', 'box']


def kind_pick(r):
    d, k = r.choice(KIND_SCEN)
    who = r.choice(NAMES)
    return mcq(f"{who} wants to {d} from a DataFrame df using df.plot(kind=…). Which kind should be used?", f"'{k}'", [f"'{x}'" for x in r.sample([x for x in KINDS if x != k], 3)],
               f"kind='{k}' suits this data.", r)


def df_plot_program(r, marks=3):
    n = 4
    months = r.choice([['Jan', 'Feb', 'Mar', 'Apr'], ['Q1', 'Q2', 'Q3', 'Q4'], ['2022', '2023', '2024', '2025']])
    shops = r.sample(['Kirana', 'Pharmacy', 'Bakery', 'Stationery', 'Dairy', 'Footwear'], 2)
    a = [r.randint(20, 90) * 1000 for _ in range(n)]
    b = [r.randint(20, 90) * 1000 for _ in range(n)]
    kind = r.choice(['bar', 'line'])
    f = r.choice(['sales.png', 'shops.pdf', 'compare.jpg'])
    stem = (f'The sales (₹) of a {shops[0]} shop and a {shops[1]} shop in {", ".join(months)} are {a} and {b}. Write a program to store them in a DataFrame with '
            f'columns Period, {shops[0]} and {shops[1]}, plot a {kind} chart of both shops against Period directly from the DataFrame with a title and axis labels, '
            f'and save it as {f}.')
    code = ['import pandas as pd', 'import matplotlib.pyplot as plt', f"df = pd.DataFrame({{'Period': {months}, '{shops[0]}': {a}, '{shops[1]}': {b}}})",
            f"df.plot(kind='{kind}', x='Period', title='Sales Comparison')", "plt.xlabel('Period')", "plt.ylabel('Sales (Rs)')", f"plt.savefig('{f}')", 'plt.show()']
    return {'stem': stem, 'answer': '\n'.join(code), 'key': f'{marks} marks: DataFrame 1, df.plot() with kind and x 1, labels/title and savefig 1' +
            ('; 2 more marks for correct imports, title and showing the chart' if marks == 5 else '') + '.', 'marks': marks}


FILL = [('import matplotlib.pyplot as ____', 'plt', 'import'), ('plt.____(x, y)', 'plot', 'line chart'), ('plt.____(x, y)', 'bar', 'bar chart'),
        ("plt.____(data, bins=5)", 'hist', 'histogram'), ("plt.____('{title}')", 'title', 'title'), ("plt.____('{xl}')", 'xlabel', 'x-axis label'),
        ("plt.____('{yl}')", 'ylabel', 'y-axis label'), ("plt.____('{file}')", 'savefig', 'save'), ('plt.____()', 'legend', 'legend'), ('plt.____()', 'show', 'show')]


def fill_case(r):
    t, xl, xs, yl, ys = dataset(r)
    who = r.choice(NAMES)
    kind = r.choice(['line', 'bar'])
    f = r.choice(['chart.png', 'result.pdf', 'graph.jpg'])
    title = t[0].upper() + t[1:]
    lines = ['import matplotlib.pyplot as ____   # (i)', f'x = {xs}', f'y = {ys}', f"plt.____(x, y, color='green')   # (ii) {kind} chart",
             f"plt.____('{title}')   # (iii) heading", f"plt.xlabel('{xl}')", f"plt.ylabel('{yl}')", f"plt.____('{f}')   # (iv) store the chart in a file", 'plt.show()']
    ans = f'(i) plt (ii) {"plot" if kind == "line" else "bar"} (iii) title (iv) savefig'
    return {'stem': f'{who} wrote a program to draw a {kind} chart of the {t}. Fill in the blanks (1 mark each):\n' + '\n'.join(lines), 'answer': ans,
            'key': '1 mark for each blank.', 'marks': 4}


CH04 = [STc(S + '04-st1', 'line plots with pyplot', """
T: Matplotlib | a Python library for creating static, animated and interactive 2D plots
T: pyplot | the module of Matplotlib that provides functions such as plot(), bar() and hist() for drawing charts
T: figure | the overall window or page on which everything (axes, title, legend) is drawn
T: legend | a box on the chart that tells which colour or line style stands for which data series
T: marker | a symbol such as a circle or square drawn at each data point of a line chart
T: linestyle | the pattern of a line, such as solid, dashed, dash-dot or dotted
Q: The standard way to import pyplot is: | import matplotlib.pyplot as plt | import pyplot.matplotlib as plt | import matplotlib as pyplot | from pyplot import matplotlib
Q: Which function displays the chart on the screen? | show() | display() | plot() | draw_chart()
Q: Which function draws a line chart? | plot() | line() | bar() | hist()
Q: Which argument of plot() sets the thickness of the line? | linewidth | linestyle | marker | width
Q: Which argument of plot() sets the size of the markers? | markersize | marker | linewidth | size_marker
Q: For legend() to show names, each plot() call should have the argument: | label | title | name | legend
Q: In the format string 'b--', the colour code b stands for: | blue | black | brown | bold
Q: Which colour code stands for black in a format string? | k | b | bl | c
Q: Which linestyle string draws a dotted line? | ':' | '--' | '-.' | '-'
Q: Which function adds grid lines to a plot? | grid() | lines() | axis() | mesh()
S+: Matplotlib is installed with the command pip install matplotlib
S+: The title(), xlabel() and ylabel() functions add text to a chart
S+: Several plot() calls before show() draw several lines on the same chart
S+: A format string can combine colour, marker and line style, as in 'r--o'
S+: When plot() gets only one list, the list values are used as the y-coordinates
S-: plt.show() saves the chart as an image file | show() displays the chart; savefig() saves it
S-: The marker argument sets the colour of a line | marker sets the symbol at each point; color sets the colour
S-: legend() works even when no plot has a label | legend() needs label= in the plot() calls to show names
S-: In a format string, '--' draws a dotted line | '--' is dashed; ':' is dotted
C: A legend is needed when two lines are drawn on one chart | it tells the reader which line belongs to which data series
C: Markers are useful on a line chart with few points | they show the exact data points joined by the line
X: C2 D2 2 | Write two differences between the color and marker arguments of plot(). | color sets the colour of the line (e.g. 'red'); marker sets the symbol drawn at each data point (e.g. 'o' for circle). Both are optional keyword arguments.
X: C3 D3 2 | Name any four functions of pyplot used to customise a chart and state the use of each. | title() – heading; xlabel()/ylabel() – axis labels; legend() – identifies series; grid() – grid lines; xticks()/yticks() – tick positions and labels (any four).
"""), STc(S + '04-st2', 'bar graphs and histograms', """
T: bar chart | a chart that shows categorical data as rectangular bars whose lengths are proportional to the values
T: histogram | a chart that shows the frequency distribution of continuous data using adjacent bars over ranges called bins
T: bins | the intervals into which the range of data is divided in a histogram
T: barh() | the pyplot function that draws a horizontal bar chart
T: histtype | the argument of hist() that sets the bar style, such as 'bar', 'step' or 'stepfilled'
T: cumulative | the argument of hist() which, when True, makes each bar show the total of all bins up to it
Q: The default number of bins used by plt.hist() is: | 10 | 5 | 20 | 8
Q: Which argument of plt.bar() changes the thickness of vertical bars? | width | height | size | linewidth
Q: Which argument of plt.hist() draws an unfilled outline only? | histtype='step' | histtype='bar' | fill='outline' | kind='step'
Q: In a histogram the bars are: | adjacent, with no gaps between them | separated by equal gaps | always horizontal | drawn for categories
Q: Which chart is best to compare the populations of five states? | Bar chart | Histogram | Line chart | Scatter chart
Q: Which chart is used to show how the heights of 100 students are distributed? | Histogram | Bar chart | Pie chart | Line chart
Q: Which argument of plt.hist() sets the colour of the bar borders? | edgecolor | linecolor | border | facecolor
Q: plt.barh(x, y) draws: | horizontal bars | vertical bars | a histogram | a line chart
S+: A histogram is used for continuous numeric data while a bar chart is used for categories
S+: In plt.hist() the bins can be given as a number or as a list of bin edges
S+: Each bin of a histogram includes its left edge, and the last bin also includes its right edge
S+: plt.bar() and plt.barh() take the categories and their values as the first two arguments
S-: The bars of a histogram have gaps between them | Histogram bars are adjacent; bar charts have gaps
S-: plt.hist() needs a list of categories and a list of heights | hist() takes the raw data and bins and counts frequencies itself
S-: A bar chart is best for showing a frequency distribution of continuous data | A histogram shows frequency distributions; bar charts compare categories
C: A histogram has no gaps between its bars | the bins are continuous intervals that touch one another
C: A cumulative histogram never has a bar lower than the one before it | each bar adds the next bin's frequency to the running total
X: C2 D2 2 | Differentiate between a bar chart and a histogram. | Bar chart: compares categories; bars are separate; the user gives heights. Histogram: shows distribution of continuous data; bars are adjacent bins; frequencies are counted from raw data.
"""), STc(S + '04-st3', 'plotting from a DataFrame and saving plots', """
T: DataFrame.plot() | the pandas method that draws a chart of a DataFrame using Matplotlib
T: kind | the argument of DataFrame.plot() that chooses the chart type, such as 'line', 'bar', 'barh', 'hist', 'box', 'area', 'pie' or 'scatter'
T: savefig() | the pyplot function that saves the current figure to a file
Q: The default kind of chart drawn by df.plot() is: | line | bar | hist | pie
Q: By default, df.plot() takes the x-axis values from the: | index of the DataFrame | first column | last column | column with the largest values
Q: Which argument of df.plot() chooses the column to be used on the x-axis? | x | index | axis | xlabel
Q: Which function saves a chart to a file? | plt.savefig() | plt.save() | plt.store() | plt.export()
Q: If no file extension is given to savefig(), the chart is saved as a: | PNG file | PDF file | JPEG file | text file
Q: Which call draws a horizontal bar chart from a DataFrame df? | df.plot(kind='barh') | df.plot(kind='hbar') | df.barh(kind='plot') | df.plot(horizontal=True)
Q: Which kind value draws a scatter chart from a DataFrame? | 'scatter' | 'dots' | 'point' | 'spread'
S+: df.plot() plots every numeric column as a separate series
S+: savefig() must be called before show() to save the figure correctly
S+: The format of the saved file is decided by the file extension in savefig()
S+: The title argument of df.plot() sets the chart title
S-: df.plot() can only draw line charts | its kind argument draws bar, barh, hist, box, area, pie and scatter charts too
S-: plt.show() saves the chart as chart.png | show() only displays it; savefig() saves it
S-: Non-numeric columns are drawn as separate lines by df.plot(kind='line') | only numeric columns are plotted
C: A chart saved after plt.show() may come out blank | show() displays and then clears the current figure
C: df.plot(kind='bar', x='Name') draws a group of bars for each row | each numeric column of the row is drawn as one bar of the group
X: C3 D3 2 | Write the statement to save the current chart as result.pdf in the folder D:/IP, and explain why it is written before plt.show(). | plt.savefig('D:/IP/result.pdf'); show() clears the figure after displaying it, so saving afterwards may give an empty file.
""")]


# ====================================================================== ch05 networks, Internet and web
def merged(sid, topic, subs, text=''):
    out = ST(sid, topic, text) if text.strip() else Sub(sid, topic, '')
    for s in subs:
        for a in ('T', 'Q', 'Y', 'P', 'M', 'Sp', 'Sm', 'C', 'X', 'L'):
            getattr(out, a).extend(copy.deepcopy(getattr(s, a)))
    return out


_CS05 = {s.sid.rsplit('-', 1)[1]: s for s in CSC.CH05}

WEB_SCEN = [('a small program that adds a feature such as an ad blocker or a dictionary to the browser itself', 'Add-on (extension)'),
            ('a complete program that lets the browser show special content, such as a PDF reader or a media player inside the page', 'Plug-in'),
            ('a small text file that a website stores on the user\'s computer to remember login details or items in the cart', 'Cookie'),
            ('a computer that stores the pages of a website and sends them when a browser requests them', 'Web server'),
            ('software such as Chrome, Firefox or Edge used to open and display web pages', 'Web browser'),
            ('the service of keeping a website on a server so that it can be reached over the Internet', 'Web hosting'),
            ('the human-readable name of a website, such as ncert.nic.in, that is translated into an IP address', 'Domain name'),
            ('the complete address of a page, such as https://www.cbse.gov.in/index.html', 'URL')]
WEBS = [w for _, w in WEB_SCEN]


def web_pick(r):
    d, t = r.choice(WEB_SCEN)
    return mcq(f'Identify the term: {d}.', t, r.sample([x for x in WEBS if x != t], 3), f'{t}: {d}.', r)


PAGE_SCEN = [('The page of the school history shows the same text and pictures to every visitor.', 'Static web page'),
             ('A railway enquiry page shows the running status of the train number that the user types.', 'Dynamic web page'),
             ('An online shop shows each user the items in their own cart.', 'Dynamic web page'),
             ('A page written only in HTML that shows the address of a shop.', 'Static web page'),
             ('A results page shows the marks of the roll number entered by the student.', 'Dynamic web page'),
             ('A page with the fixed holiday list of a company, changed only when the developer edits the file.', 'Static web page')]


def page_pick(r):
    d, t = r.choice(PAGE_SCEN)
    return mcq(f'{d} Which type of web page is this?', t, [x for x in ['Static web page', 'Dynamic web page', 'Plug-in', 'Cookie'] if x != t], f'A {t.lower()} ' +
               ('shows the same content to everyone.' if t.startswith('Static') else 'creates its content when it is requested, often from a database.'), r)


APP_SCEN = [('talk to a relative abroad over a broadband connection using an app, without a telephone line', 'VoIP'),
            ('send a letter with a PDF attachment to the school principal', 'E-mail'),
            ('exchange short typed messages with friends in real time', 'Chat'),
            ('read the news on a website using a browser', 'World Wide Web'),
            ('hold an audio call through WhatsApp or Google Meet', 'VoIP'),
            ('send the same circular to all parents at their mailboxes, to be read later', 'E-mail')]


def app_pick(r):
    d, t = r.choice(APP_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} wants to {d}. Which Internet application is used?', t, [x for x in ['VoIP', 'E-mail', 'Chat', 'World Wide Web'] if x != t], f'{t} is used to {d}.', r)


WEB_ROWS = [('Differentiate between a website and a web page.', 'A web page is a single document on the web; a website is a collection of related web pages under one domain name, with a home page.'),
            ('Differentiate between a static and a dynamic web page.', 'Static: fixed content, same for every user, written in HTML. Dynamic: content generated at request time (e.g. from a database), may differ for each user.'),
            ('Differentiate between a web browser and a web server.', 'A browser is client software that requests and displays web pages (e.g. Chrome); a web server stores websites and sends pages on request (e.g. Apache).'),
            ('Differentiate between an add-on and a plug-in.', 'An add-on (extension) adds a feature to the browser itself, e.g. an ad blocker; a plug-in is a separate program that lets the browser show special content, e.g. a PDF or media plug-in.'),
            ('What are cookies? Give one use and one risk.', 'Small text files stored by a website on the user\'s computer. Use: remember login or cart items. Risk: third-party cookies can track browsing and threaten privacy.'),
            ('Differentiate between the Internet and the World Wide Web.', 'The Internet is the global network of networks (hardware and protocols); the WWW is a service on the Internet made of interlinked web pages accessed through browsers.'),
            ('What is web hosting? Name two things needed to host a website.', 'Keeping a website on a web server connected to the Internet so that others can reach it. Needs: a registered domain name and space on a web server (hosting service).'),
            ('What is VoIP? Give one advantage.', 'Voice over Internet Protocol: voice calls over the Internet as data packets. Advantage: cheap or free long-distance calls; no separate telephone line needed.'),
            ('Write the parts of the URL https://www.ncert.nic.in/textbook.php.', 'Protocol: https; domain name: www.ncert.nic.in (top-level domain .in); path/file: textbook.php.'),
            ('What is an e-mail address? Write its two parts with an example.', 'The address of a mailbox: username@domain, e.g. ananya.rao@gmail.com – user name ananya.rao, domain name gmail.com.')]


def web_compare(r):
    d = deck(WEB_ROWS)

    def gen(rr):
        q, a = d(rr)
        return {'stem': q, 'answer': a, 'key': '2 marks: 1 mark for each correct point.', 'marks': 2}
    return gen


def web_case(r):
    who = r.choice(NAMES)
    org = r.choice(['bakery', 'coaching centre', 'handloom co-operative', 'dental clinic', 'travel agency'])
    city = r.choice(CITIES)
    site = r.choice(['swaad', 'gyanpath', 'bunkar', 'muskaan', 'yatra'])
    stem = (f'{who} wants to start a website for a {org} in {city}. The site will show a fixed page about the {org} and a page where customers check the status of '
            f'their orders by entering an order number.\n(i) Which type of web page is the order-status page: static or dynamic? (1)\n(ii) What must {who} register and '
            f'buy so that people can reach the site as www.{site}.in? (1)\n(iii) Customers see a message that the site uses cookies. What are cookies? (1)\n'
            f'(iv) Name any two web browsers customers might use to open the site. (1)')
    ans = ('(i) Dynamic – its content is generated for each order number.\n(ii) A domain name (www.' + site + '.in) and web hosting space on a web server.\n'
           '(iii) Small text files that a website stores on the visitor\'s computer to remember information such as login or preferences.\n(iv) Google Chrome, Mozilla Firefox (also Microsoft Edge, Safari, Opera).')
    return {'stem': stem, 'answer': ans, 'key': '1 mark for each part.', 'marks': 4}


CH05 = [merged(S + '05-st1', 'types of networks and network devices', [_CS05['st1'], _CS05['st2']]),
        merged(S + '05-st2', 'network topologies', [_CS05['st3']]),
        STc(S + '05-st3', 'Internet, URL, WWW and its applications', """
T: Internet | the global network of networks that connects millions of computers using TCP/IP
T: World Wide Web | an information system of interlinked web pages and resources that are accessed over the Internet through browsers
T: URL | Uniform Resource Locator, the complete address of a resource on the web, made of the protocol, domain name and path
T: e-mail | a service for sending and receiving messages and attachments through mailboxes on the Internet
T: chat | real-time exchange of typed messages between people over the Internet
T: VoIP | Voice over Internet Protocol, a technology that carries voice calls over the Internet as data packets
T: DNS | Domain Name System, the service that translates domain names into IP addresses
T: HTML | HyperText Markup Language, used to create web pages with predefined tags
Q: The World Wide Web was invented by: | Tim Berners-Lee | Vint Cerf | Ray Tomlinson | Charles Babbage
Q: The WWW was developed in 1989-90 at: | CERN | ISRO | NASA | MIT
Q: Which part of the URL https://www.cbse.gov.in/results.html is the protocol? | https | www.cbse.gov.in | results.html | gov.in
Q: The two parts of an e-mail address are separated by: | @ | # | / | .com
Q: Which system translates www.ncert.nic.in into an IP address? | DNS | URL | HTML | VoIP
Q: Which of these is an example of a VoIP application? | Skype call | Notepad | Excel | MySQL
Q: Hyperlinks on web pages are created using: | HTML | SQL | Python | CSV
S+: The WWW is a service that runs on the Internet
S+: An e-mail can be sent to many recipients at the same time
S+: VoIP calls need an Internet connection rather than a separate telephone line
S+: A URL tells the browser the protocol to use and the location of the resource
S+: Chat is synchronous communication while e-mail is asynchronous
S-: The Internet and the World Wide Web are the same thing | the WWW is one service that runs on the Internet
S-: An e-mail can be received only if the receiver is online when it is sent | The e-mail is stored in the mailbox and read later
S-: VoIP sends voice as analog signals over telephone lines | VoIP sends voice as digital packets over the Internet
S-: HTML tags are defined by the user | HTML has predefined tags; XML tags are user-defined
C: Users can type names instead of IP addresses to open websites | DNS translates domain names into IP addresses
C: VoIP calls to other countries are cheap | the voice travels as data over the Internet instead of long-distance telephone lines
X: C2 D2 2 | Give two differences between e-mail and chat. | E-mail is asynchronous (read later) and suits formal messages with attachments; chat is real-time (synchronous) and suits short informal messages.
"""), STc(S + '05-st4', 'websites, web servers, hosting and browsers', """
T: web page | a single document on the World Wide Web, written in HTML and displayed by a browser
T: website | a collection of related web pages under one domain name, usually starting from a home page
T: static web page | a web page whose content is fixed and is the same for every visitor
T: dynamic web page | a web page whose content is generated when it is requested and can differ for each visitor
T: web server | a computer or program that stores websites and sends web pages to browsers on request
T: web hosting | a service that stores a website on a web server connected to the Internet so that it can be accessed by everyone
T: web browser | a client program used to access and display web pages, such as Chrome, Firefox, Edge or Safari
T: add-on | a small program (extension) that adds a new feature to the browser itself
T: plug-in | a complete program that lets a browser display special content such as video or PDF files
T: cookie | a small text file stored on the user's computer by a website to remember information about the user
Q: Which of these is a web browser? | Mozilla Firefox | Apache | MySQL | Python
Q: Which of these is web server software? | Apache | Google Chrome | Safari | Opera
Q: The first page of a website is called its: | home page | front end | index server | cover page
Q: Cookies are stored on the: | user's computer | web server only | DNS server | router
Q: An ad blocker added to a browser is an example of: | an add-on | a plug-in | a cookie | a web server
Q: Which kind of web page is generated from a database when it is requested? | Dynamic | Static | Home | Blank
Q: The first web browser, created by Tim Berners-Lee, was called: | WorldWideWeb | Mosaic | Netscape | Internet Explorer
S+: Every website is hosted on a web server
S+: Cookies help websites remember the user's preferences and login status
S+: Third-party cookies can be used to track a user's browsing across websites
S+: A browser's settings let the user clear history and cookies
S+: A dynamic web page can show different content to different users
S-: A web browser stores websites for others to access | a web server stores websites; a browser requests and displays them
S-: Cookies are programs that can run on the user's computer | cookies are small text files, not programs
S-: A plug-in and an add-on are exactly the same | an add-on changes the browser itself; a plug-in is a separate program that handles special content
S-: A static web page changes its content for each visitor | a dynamic page changes; a static page is the same for everyone
C: A website needs web hosting to be reachable by others | its files must be on a server that is always connected to the Internet
C: Deleting cookies may log a user out of websites | cookies store the session and login information
X: C2 D2 2 | Name any two web browsers and any two add-ons or plug-ins. | Browsers: Google Chrome, Mozilla Firefox, Microsoft Edge, Safari, Opera. Add-ons/plug-ins: ad blocker, password manager, dictionary/translator extension, PDF viewer plug-in (any two each).
""")]


# ====================================================================== ch06 societal impacts
CRIME_SCEN = [('received an e-mail that looked like it came from her bank, asking her to click a link and enter her net-banking password', 'Phishing'),
              ('found that all the files on his laptop were encrypted and a message demanded payment in cryptocurrency to unlock them', 'Ransomware'),
              ('discovered that someone had gained unauthorised access to the school server and changed marks', 'Hacking'),
              ('kept receiving insulting and threatening comments on her posts from a group of classmates', 'Cyber bullying'),
              ('learnt that someone was secretly listening in to the data on an unsecured public Wi-Fi network and reading her messages', 'Eavesdropping'),
              ('found that someone had opened a social media account using his name and photos and was asking his friends for money', 'Identity theft'),
              ('saw a person post provocative, upsetting comments on a forum just to get angry reactions from others', 'Cyber trolling')]
CRIMES = sorted({c for _, c in CRIME_SCEN})
SAFE = {'Phishing': 'do not click links in such e-mails; check the sender and the https address; never share passwords or OTPs',
        'Ransomware': 'keep regular offline backups; update the operating system and antivirus; do not open unknown attachments',
        'Hacking': 'use strong passwords and two-factor authentication; install a firewall; keep software updated',
        'Cyber bullying': 'do not respond; block and report the bullies; keep evidence and tell a trusted adult or the cyber cell',
        'Eavesdropping': 'avoid sensitive work on public Wi-Fi; use HTTPS/encrypted apps or a VPN',
        'Identity theft': 'report the fake profile to the platform and the cyber cell; keep personal details and photos private',
        'Cyber trolling': 'do not feed the troll (ignore it); report or block the account'}


def crime_pick(r):
    d, c = r.choice(CRIME_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} {d}. Which cyber crime is this?', c, r.sample([x for x in CRIMES if x != c], 3), f'This is {c.lower()}.', r)


def crime_case(r):
    d, c = r.choice(CRIME_SCEN)
    who = r.choice(NAMES)
    stem = (f'{who} {d}.\n(i) Identify the cyber crime. (1)\n(ii) Suggest two ways to protect oneself from it. (2)\n'
            f'(iii) Name the Indian law that deals with cyber crimes. (1)')
    ans = f'(i) {c}.\n(ii) {SAFE[c][0].upper() + SAFE[c][1:]}.\n(iii) The Information Technology Act, 2000 (IT Act), amended in 2008.'
    return {'stem': stem, 'answer': ans, 'key': '4 marks: (i) 1, (ii) 1 each for two measures, (iii) 1.', 'marks': 4}


IPR_SCEN = [('A company registers the shape of its logo so that no other company can use a similar logo on its products.', 'Trademark'),
            ('An inventor gets exclusive rights for 20 years over a new water-purifying device she designed.', 'Patent'),
            ('A singer gets the exclusive right to copy, distribute and perform the songs she wrote and recorded.', 'Copyright'),
            ('A programmer\'s source code is protected from being copied and sold by others without permission.', 'Copyright'),
            ('A firm protects the brand name of its tea so that others cannot sell tea under a confusingly similar name.', 'Trademark'),
            ('A scientist gets exclusive rights to make and sell a new process for producing a medicine.', 'Patent')]


def ipr_pick(r):
    d, c = r.choice(IPR_SCEN)
    return mcq(f'{d} Which intellectual property right is this?', c, [x for x in ['Copyright', 'Patent', 'Trademark', 'Trade licence'] if x != c],
               f'{c} protects this.', r)


VIOL_SCEN = [('submitted an essay copied from a website as her own work without giving credit', 'Plagiarism'),
             ('downloaded a paid film from a pirate site and shared copies with friends', 'Copyright infringement'),
             ('started selling shoes with a logo almost identical to that of a famous brand', 'Trademark infringement'),
             ('used a photographer\'s picture in a school magazine without permission or credit', 'Copyright infringement'),
             ('presented a classmate\'s project code as his own in the practical exam', 'Plagiarism')]


def viol_pick(r):
    d, c = r.choice(VIOL_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} {d}. Which violation of intellectual property is this?', c, [x for x in ['Plagiarism', 'Copyright infringement', 'Trademark infringement', 'Patent filing'] if x != c],
               f'This is {c.lower()}.', r)


LIC_SCEN = [('lets anyone use, modify and share the work, even commercially, as long as the creator is credited', 'CC BY'),
            ('lets others share and adapt the work with credit, but only if they release their version under the same licence', 'CC BY-SA'),
            ('lets others share and adapt the work with credit, but not for commercial purposes', 'CC BY-NC'),
            ('lets others share the work with credit, but not change it', 'CC BY-ND'),
            ('is a software licence that requires any modified version that is distributed to be released with its source code under the same licence (copyleft)', 'GPL'),
            ('is a permissive software licence that lets users modify the code and release it under other terms, provided the licence and notices are kept', 'Apache License')]
LICS = [c for _, c in LIC_SCEN]


def lic_pick(r):
    d, c = r.choice(LIC_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} wants a licence for her work that {d}. Which licence fits?', c, r.sample([x for x in LICS if x != c], 3), f'{c} {d}.', r)


FP_SCEN = [('posting photos on a social media account', 'Active'), ('websites recording the user\'s IP address and pages visited', 'Passive'),
           ('writing a comment on a blog', 'Active'), ('an app recording the user\'s location in the background', 'Passive'),
           ('filling an online form with one\'s e-mail address', 'Active'), ('cookies storing the items a user looked at on a shopping site', 'Passive'),
           ('sending an e-mail', 'Active'), ('search engines keeping the history of a user\'s searches', 'Passive')]


def fp_pick(r):
    d, c = r.choice(FP_SCEN)
    return mcq(f'What kind of digital footprint is created by {d}?', f'{c} digital footprint', [f'{"Passive" if c == "Active" else "Active"} digital footprint',
               'No digital footprint', 'Temporary footprint that is erased on logout'], f'{"Data shared intentionally by the user" if c == "Active" else "Data collected without the user knowing or acting"}: {c.lower()} footprint.', r)


ETQ_SCEN = [('typing a whole e-mail in capital letters', 'Poor etiquette: capitals read as shouting'),
            ('replying to a group mail with a short, polite message to only the person concerned', 'Good etiquette: precise and polite communication'),
            ('sharing a friend\'s photo online without asking', 'Poor etiquette: it does not respect the friend\'s privacy'),
            ('ignoring a troll instead of replying angrily', 'Good etiquette: do not feed the troll'),
            ('forwarding an unverified news message to all groups', 'Poor etiquette: it spreads fake information'),
            ('giving credit to the source when sharing someone\'s article', 'Good etiquette: being ethical and respecting copyright')]


def etq_pick(r):
    d, a = r.choice(ETQ_SCEN)
    who = r.choice(NAMES)
    wrong = [x for _, x in ETQ_SCEN if x != a and x.split(':')[0] != a.split(':')[0]][:1] + [x for _, x in ETQ_SCEN if x != a and x.split(':')[0] == a.split(':')[0]][:2]
    return mcq(f'{who} is {d}. How should this be judged?', a, wrong, a + '.', r)


EW_SCEN = [('donating a working old laptop to a school', 'Reuse'), ('buying a new phone only when the old one cannot be repaired', 'Reduce'),
           ('giving old circuit boards to an authorised e-waste recycler to recover metals', 'Recycle'), ('repairing a monitor instead of replacing it', 'Reuse'),
           ('selling an old working printer to someone who needs it', 'Reuse'), ('avoiding buying gadgets that are not really needed', 'Reduce'),
           ('dropping dead batteries at a collection centre for processing', 'Recycle')]


def ew_pick(r):
    d, c = r.choice(EW_SCEN)
    return mcq(f'Which principle of e-waste management is followed by {d}?', c, [x for x in ['Reduce', 'Reuse', 'Recycle', 'Refuse to dispose'] if x != c], f'This is {c.lower()}.', r)


HEALTH_SCEN = [('eyes feel dry and tired after long hours of looking at the screen', 'Eye strain: follow the 20-20-20 rule and blink often'),
               ('pain in the neck and back from slouching at the desk', 'Poor posture: sit upright with back support and the screen at eye level'),
               ('pain in the wrists from long periods of typing', 'Repetitive strain: keep wrists straight and take breaks'),
               ('feeling restless and anxious when away from the phone and games', 'Internet addiction: limit screen time and take up offline activities'),
               ('difficulty in sleeping after using the phone late at night', 'Disturbed sleep: avoid screens before bedtime')]


def health_pick(r):
    d, a = r.choice(HEALTH_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} complains of {d}. Which problem is this, and what helps?', a, r.sample([x for _, x in HEALTH_SCEN if x != a], 3), a + '.', r)


SOC_ROWS = {
    'st1': [('What is a digital footprint? Differentiate between active and passive digital footprints.', 'The trail of data a person leaves while using the Internet. Active: data shared intentionally (posts, e-mails, forms). Passive: data collected without the user\'s knowledge (IP address, browsing history, cookies).'),
            ('Write any two net etiquettes and two social media etiquettes.', 'Net: be ethical (respect copyright, share expertise), be respectful (respect privacy and diversity), be responsible (avoid cyber bullying, do not feed trolls). Social media: be secure (strong passwords, know whom you befriend, beware of fake information), be reliable (think before uploading).'),
            ('Who is a netizen? Give two ways to be a responsible netizen.', 'A person who uses the Internet (digital citizen). Be polite and respectful, verify information before sharing, protect privacy, give credit to sources.')],
    'st2': [('Differentiate between copyright and patent.', 'Copyright protects creative expression (books, music, software code) automatically; a patent protects an invention, is granted on application and lasts 20 years, and gives exclusive rights to make, use and sell it.'),
            ('What is plagiarism? How can it be avoided?', 'Presenting someone else\'s work or ideas as one\'s own without credit. Avoid by citing/crediting the source, quoting properly, and writing in one\'s own words.'),
            ('Differentiate between GPL and Apache licences.', 'GPL is copyleft: distributed modified versions must be released under GPL with source code. Apache is permissive: modified versions may be released under other terms if the licence and notices are kept.'),
            ('What is Creative Commons? Name any two CC licences.', 'A non-profit that provides free licences for creative works, letting creators allow sharing on their terms. E.g. CC BY, CC BY-SA, CC BY-NC, CC BY-ND, CC0.')],
    'st3': [('What is FOSS? Give two examples.', 'Free and Open Source Software: software whose source code is freely available to use, modify and share. Examples: Linux, LibreOffice, Mozilla Firefox, Python, GIMP.'),
            ('Differentiate between ethical hacking and non-ethical hacking.', 'Ethical (white-hat) hacking is authorised testing to find and fix security weaknesses; non-ethical (black-hat) hacking is unauthorised access to steal, damage or misuse data.'),
            ('What is the IT Act, 2000? Give two of its provisions.', 'The Indian law on electronic transactions and cyber crime (amended 2008). It gives legal recognition to e-documents and digital signatures, defines cyber crimes and penalties, and set up the Cyber Appellate Tribunal.'),
            ('What is ransomware? Give one way to protect against it.', 'Malware that encrypts or locks a victim\'s data and demands a ransom to restore it. Protect by regular offline backups, updated antivirus/OS, and not opening unknown attachments.')],
    'st4': [('What is e-waste? Give two of its harmful effects.', 'Discarded electronic devices such as phones, computers and batteries. Effects: toxic metals (lead, mercury, cadmium) pollute soil and water; burning releases harmful fumes; health problems for workers.'),
            ('Explain the 3 Rs of e-waste management.', 'Reduce – buy only what is needed; Reuse – repair, donate or resell working devices; Recycle – send devices to authorised recyclers to recover materials safely.'),
            ('Give any two health problems caused by excessive use of technology and their remedies.', 'Eye strain – 20-20-20 rule, proper lighting; back/neck pain – correct posture and ergonomic chair; Internet addiction – limit screen time (any two).'),
            ('What is ergonomics? Give one example of its use with computers.', 'The science of designing furniture, devices and the workplace to fit the user and reduce strain. E.g. an adjustable chair with back support and the monitor at eye level.')]}


def soc_written(rows):
    d = deck(rows)

    def gen(r):
        q, a = d(r)
        return {'stem': q, 'answer': a, 'key': '2 marks: 1 mark for each correct point.', 'marks': 2}
    return gen


def ewaste_case(r):
    who = r.choice(NAMES)
    n = r.randint(20, 60)
    stem = (f'{who}\'s school is replacing {n} old computers, printers and UPS batteries.\n(i) What is this discarded equipment called? (1)\n'
            f'(ii) Give one harmful effect of throwing it in a landfill. (1)\n(iii) Suggest two ways the school can manage it responsibly. (2)')
    ans = ('(i) E-waste (electronic waste).\n(ii) Toxic substances such as lead, mercury and cadmium leak into soil and groundwater (or burning releases toxic fumes).\n'
           '(iii) Donate working computers (reuse); give the rest to an authorised e-waste recycler (recycle); return batteries through take-back schemes.')
    return {'stem': stem, 'answer': ans, 'key': '4 marks: (i) 1, (ii) 1, (iii) 1 each for two ways.', 'marks': 4}


def ipr_case(r):
    who, frnd = r.sample(NAMES, 2)
    work = r.choice(['photographs of birds', 'short film', 'poems', 'Python game'])
    stem = (f'{who} posted her {work} online. {frnd} downloaded them and used them in a project without giving any credit.\n(i) Which IPR protects {who}\'s {work}? (1)\n'
            f'(ii) Name the wrong committed by {frnd}. (1)\n(iii) {who} wants others to share and adapt her work, but only with credit and not for commercial use. Which licence should she choose? (1)\n'
            f'(iv) How could {frnd} have used the work properly? (1)')
    ans = (f'(i) Copyright.\n(ii) Plagiarism (and copyright infringement, using the work without permission).\n(iii) Creative Commons CC BY-NC.\n'
           f'(iv) By taking permission (or using it under its licence) and giving credit to {who} as the creator.')
    return {'stem': stem, 'answer': ans, 'key': '1 mark for each part.', 'marks': 4}


CH06 = [STc(S + '06-st1', 'digital footprints and etiquettes', """
T: digital footprint | the trail of data that a person leaves behind while using the Internet
T: active digital footprint | data that a user shares intentionally, such as posts, e-mails and online forms
T: passive digital footprint | data collected about a user without their knowledge, such as IP address, browsing history and location
T: netizen | a person who uses the Internet, also called a digital citizen
T: net etiquette | the code of good behaviour to be followed while using the Internet
T: cyber troll | a person who posts provocative or offensive comments online to upset others
Q: Which of these creates a passive digital footprint? | A website recording your IP address | Posting a photo | Writing a blog | Sending an e-mail
Q: Typing a message in all capital letters is considered: | shouting | polite | secure | formal
Q: The advice 'Do not feed the troll' means: | ignore provocative posts instead of replying | report every post | share the troll's posts | argue with the troll
Q: Net etiquettes ask a netizen to be ethical, respectful and: | responsible | anonymous | famous | quick
Q: A digital footprint is usually: | permanent and hard to delete | erased on logout | stored only on one's own phone | visible only to friends
Q: Which is a good social media practice? | Thinking before uploading a post | Sharing passwords with friends | Accepting requests from strangers | Forwarding unverified news
S+: A digital footprint can be used to trace a person's online activities
S+: Communication etiquette asks us to be precise, polite and credible
S+: Respecting others' privacy and diversity is part of net etiquette
S+: Before sharing information, a responsible netizen checks that it is genuine
S-: Deleting a post removes every copy of it from the Internet | copies may remain with others and on servers, so footprints are hard to erase
S-: Only data posted by a user forms the digital footprint | passive data such as IP address and browsing history also form it
S-: Replying angrily to trolls makes them stop | trolls want attention, so they should be ignored
C: One should think before posting on social media | the post becomes part of a permanent digital footprint that others can see later
C: Strong passwords must be kept on social media accounts | weak passwords let others take over the account and misuse it
X: C2 D2 2 | Give two examples each of active and passive digital footprints. | Active: social media posts, comments, e-mails, filling online forms. Passive: IP address, browsing history, cookies, location tracking by apps.
"""), STc(S + '06-st2', 'data protection, intellectual property rights and licensing', """
T: intellectual property | creations of the mind, such as inventions, literary and artistic works, designs, symbols and names
T: copyright | the legal right of creators over their literary, artistic, musical and software works
T: patent | an exclusive right granted for an invention, usually for 20 years
T: trademark | a word, symbol, logo or design that identifies a company's goods and distinguishes them from others
T: plagiarism | presenting someone else's work or ideas as one's own without giving credit
T: copyleft | a licensing method that requires modified versions to be shared under the same free terms
T: Creative Commons | a set of public licences that let creators allow others to share and use their work on stated conditions
T: GPL | General Public License, a free software licence that keeps derived works free and open (copyleft)
Q: Which IPR protects a company's logo? | Trademark | Patent | Copyright | Licence
Q: Which IPR protects a new invention? | Patent | Copyright | Trademark | Licence
Q: A patent is usually granted for: | 20 years | 5 years | 60 years | the creator's lifetime
Q: Which licence is commonly used for creative works such as photos and articles? | Creative Commons | GPL | Apache | Shareware
Q: In CC BY-SA, SA stands for: | Share Alike | Save All | Same Attribution | Software Application
Q: Copying someone's code and submitting it as your own is: | plagiarism | a patent | a trademark | fair licensing
Q: Which licence lets modified versions be released under other terms if notices are kept? | Apache | GPL | CC BY-SA | CC BY-ND
S+: Data protection means keeping personal and sensitive data safe from misuse
S+: Copyright exists automatically once a work is created
S+: Using copyrighted material without permission is copyright infringement
S+: The GPL requires source code to be made available when the software is distributed
S-: A patent protects the logo of a company | a trademark protects a logo; a patent protects an invention
S-: Everything available on the Internet is free to copy and use | most online content is protected by copyright unless its licence allows reuse
S-: Giving credit makes copying a whole copyrighted work legal | credit avoids plagiarism but permission or a suitable licence is still needed
C: Giving credit to the source avoids plagiarism | plagiarism is presenting another's work as one's own
C: Creators release work under Creative Commons licences | they want others to share and use it while keeping some rights
X: C2 D2 2 | Differentiate between copyright and trademark. | Copyright protects creative works such as books, music and software code; a trademark protects names, logos and symbols that identify a company's products.
"""), STc(S + '06-st3', 'open source software, cyber crimes and cyber laws', """
T: FOSS | Free and Open Source Software, software whose source code is freely available to use, study, modify and share
T: proprietary software | software owned by a company whose source code is not shared and which is used under a paid licence
T: hacking | gaining unauthorised access to a computer or network
T: ethical hacking | authorised testing of a system by a white-hat hacker to find and fix security weaknesses
T: phishing | tricking people through fake e-mails or websites into revealing passwords, card numbers or OTPs
T: ransomware | malware that locks or encrypts a victim's data and demands payment to restore it
T: eavesdropping | secretly listening to or intercepting private communication on a network
T: cyber bullying | using the Internet to harass, threaten or humiliate someone
T: IT Act | the Information Technology Act, 2000 of India, amended in 2008, which deals with cyber crime and electronic commerce
Q: Which of these is open source software? | LibreOffice | Microsoft Word | Adobe Photoshop | Windows 11
Q: The Indian law that deals with cyber crime is the: | IT Act, 2000 | Copyright Act, 1957 | Environment Protection Act, 1986 | Consumer Protection Act, 2019
Q: A white-hat hacker is also called: | an ethical hacker | a cracker | a troll | a phisher
Q: The 2017 WannaCry attack, which locked files and demanded bitcoins, was an example of: | ransomware | phishing | eavesdropping | trolling
Q: Fake e-mails that pretend to be from a bank to steal passwords are called: | phishing | spamming | hacking | trolling
Q: The IT Act, 2000 was amended in: | 2008 | 2005 | 2012 | 2019
Q: Which body hears appeals under the IT Act? | Cyber Appellate Tribunal | Lok Adalat | Election Commission | Press Council
S+: FOSS can be modified and redistributed by users
S+: Linux, Python and Mozilla Firefox are examples of open source software
S+: The IT Act gives legal recognition to electronic records and digital signatures
S+: Using strong passwords and two-factor authentication reduces the risk of hacking
S+: Ransomware often spreads through e-mail attachments and infected downloads
S-: Free software always means software with no cost and no source code | free refers to freedom to use, study, modify and share the source code
S-: Ethical hacking is a crime | ethical hacking is authorised testing to improve security
S-: Phishing attacks always come through phone calls | phishing mainly uses fake e-mails and websites
C: Regular offline backups reduce the damage done by ransomware | data can be restored without paying the ransom
C: Public Wi-Fi is risky for online banking | data on unsecured networks can be intercepted by eavesdroppers
X: C2 D2 2 | Differentiate between FOSS and proprietary software with one example each. | FOSS: source code available, free to modify and share (Linux, LibreOffice). Proprietary: source code closed, used under a paid licence (Windows, MS Office).
"""), STc(S + '06-st4', 'e-waste management and health concerns', """
T: e-waste | discarded electrical and electronic devices such as computers, phones, printers and batteries
T: ergonomics | the science of designing the workplace, furniture and devices to fit the user and reduce strain
T: Internet addiction | an excessive, uncontrolled use of the Internet that harms daily life and health
T: 3R principle | reduce, reuse and recycle, the basic approach to managing waste including e-waste
Q: Which toxic metal is commonly found in e-waste? | Lead | Gold | Aluminium foil | Copper wire insulation
Q: Repairing an old monitor instead of buying a new one is an example of: | reuse | recycle | reduce | refuse
Q: The 20-20-20 rule is advised to reduce: | eye strain | back pain | hearing loss | Internet addiction
Q: E-waste should be given to: | an authorised e-waste recycler | the municipal garbage bin | a scrap dealer who burns it | a landfill
Q: Ergonomics advises that the top of the monitor should be at about: | eye level | knee level | waist level | ceiling level
Q: The 'polluter pays' principle for waste in India comes from the: | Environment Protection Act, 1986 | IT Act, 2000 | Copyright Act, 1957 | Right to Information Act, 2005
S+: Burning e-waste in the open releases toxic fumes
S+: Recycling e-waste can recover valuable metals such as copper and gold
S+: Sitting with proper back support reduces neck and back pain
S+: Taking regular breaks while working on a computer reduces strain on eyes and wrists
S-: E-waste is harmless and can be thrown with household garbage | it contains toxic metals that pollute soil and water
S-: Recycling means buying fewer gadgets | that is reducing; recycling recovers materials from old devices
S-: Using a phone in bed late at night improves sleep | screen use before bed disturbs sleep
C: E-waste must be handled by authorised recyclers | it contains hazardous substances that harm health and the environment if dumped
C: Long hours of typing can cause wrist pain | repeated movements strain the muscles and tendons of the wrist
X: C2 D2 2 | Give two health hazards of using computers for long hours and one remedy for each. | Eye strain – 20-20-20 rule; back/neck pain – correct posture and ergonomic chair; wrist pain – breaks and wrist support (any two).
""")]


def fams_ch04_06():
    E = {}
    E[S + '04-st1'] = [F('C2', 'D2', 'mcq', fmt_pick), F('C3', 'D3', 'mcq', fmt_pick), F('C1', 'D1', 'mcq', func_pick), F('C2', 'D3', 'mcq', xdefault),
                       F('C3', 'D2', 'short', fmt_write, marks=1), F('C4', 'D4', 'multi_step', line_program, marks=3), F('C4', 'D4', 'long', lambda r: line_program(r, 4), marks=4),
                       F('C4', 'D5', 'long', two_line_program, marks=5), F('C3', 'D4', 'short', plot_errors, marks=2, gap='G5'), F('C4', 'D4', 'case', fill_case, marks=4, gap='G7')]
    E[S + '04-st2'] = [F('C3', 'D3', 'mcq', hist_bin), F('C3', 'D4', 'mcq', hist_bin, gap='G5'), F('C3', 'D3', 'numerical', hist_freq, marks=2), F('C2', 'D2', 'mcq', bar_count),
                       F('C1', 'D1', 'mcq', bar_count), F('C4', 'D4', 'multi_step', bar_program, marks=3), F('C4', 'D4', 'long', lambda r: bar_program(r, 4), marks=4),
                       F('C4', 'D3', 'multi_step', hist_program, marks=3), F('C2', 'D2', 'mcq', func_pick)]
    E[S + '04-st3'] = [F('C3', 'D3', 'mcq', df_plot_count), F('C2', 'D2', 'mcq', save_pick), F('C2', 'D3', 'mcq', kind_pick), F('C3', 'D4', 'mcq', df_plot_count, gap='G5'),
                       F('C4', 'D4', 'multi_step', df_plot_program, marks=3), F('C4', 'D5', 'long', lambda r: df_plot_program(r, 5), marks=5), F('C1', 'D1', 'mcq', save_pick)]
    cmp_ = CSC.net_compare(None)
    E[S + '05-st1'] = [F('C2', 'D2', 'mcq', CSC.net_pick), F('C3', 'D3', 'mcq', CSC.net_pick), F('C2', 'D2', 'mcq', CSC.dev_pick), F('C3', 'D3', 'mcq', CSC.repeater_pick),
                       F('C3', 'D2', 'mcq', CSC.server_pick), F('C4', 'D4', 'long', CSC.campus_case, marks=5, gap='G7'), F('C2', 'D3', 'explain', cmp_, marks=2), F('C1', 'D1', 'mcq', CSC.dev_pick)]
    E[S + '05-st2'] = [F('C2', 'D2', 'mcq', CSC.topo_pick), F('C3', 'D3', 'short', CSC.mesh_count), F('C3', 'D4', 'mcq', CSC.topo_pick, gap='G5'),
                       F('C4', 'D4', 'long', CSC.campus_case, marks=5, gap='G7'), F('C1', 'D1', 'short', CSC.mesh_count)]
    wc = web_compare(None)
    E[S + '05-st3'] = [F('C2', 'D2', 'mcq', CSC.url_parts), F('C3', 'D3', 'mcq', CSC.url_parts), F('C2', 'D2', 'mcq', app_pick), F('C3', 'D3', 'mcq', app_pick),
                       F('C2', 'D3', 'explain', wc, marks=2), F('C1', 'D1', 'mcq', app_pick)]
    E[S + '05-st4'] = [F('C2', 'D2', 'mcq', web_pick), F('C3', 'D3', 'mcq', page_pick), F('C1', 'D1', 'mcq', web_pick), F('C3', 'D4', 'explain', wc, marks=2, gap='G5'),
                       F('C4', 'D4', 'case', web_case, marks=4, gap='G7'), F('C2', 'D3', 'mcq', page_pick)]
    E[S + '06-st1'] = [F('C2', 'D2', 'mcq', fp_pick), F('C3', 'D3', 'mcq', etq_pick), F('C1', 'D1', 'mcq', fp_pick), F('C3', 'D4', 'explain', soc_written(SOC_ROWS['st1']), marks=2, gap='G5'),
                       F('C2', 'D3', 'mcq', etq_pick)]
    E[S + '06-st2'] = [F('C2', 'D2', 'mcq', ipr_pick), F('C3', 'D3', 'mcq', viol_pick), F('C3', 'D3', 'mcq', lic_pick), F('C1', 'D1', 'mcq', ipr_pick),
                       F('C2', 'D3', 'explain', soc_written(SOC_ROWS['st2']), marks=2), F('C4', 'D4', 'case', ipr_case, marks=4, gap='G7'), F('C3', 'D4', 'mcq', lic_pick, gap='G5')]
    E[S + '06-st3'] = [F('C2', 'D2', 'mcq', crime_pick), F('C3', 'D3', 'mcq', crime_pick), F('C1', 'D1', 'mcq', crime_pick), F('C4', 'D4', 'case', crime_case, marks=4, gap='G7'),
                       F('C2', 'D3', 'explain', soc_written(SOC_ROWS['st3']), marks=2), F('C3', 'D4', 'mcq', crime_pick, gap='G5')]
    E[S + '06-st4'] = [F('C2', 'D2', 'mcq', ew_pick), F('C3', 'D3', 'mcq', health_pick), F('C1', 'D1', 'mcq', ew_pick), F('C4', 'D4', 'case', ewaste_case, marks=4, gap='G7'),
                       F('C2', 'D3', 'explain', soc_written(SOC_ROWS['st4']), marks=2)]
    return [CH04, CH05, CH06], E
