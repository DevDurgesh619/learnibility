"""CBSE class 12 Informatics Practices (065), chapters 2-3: data handling using Pandas I and II.

Every output is produced by running the code with pandas (kit.run); the dtype line of string Series is shown as
"dtype: object", as printed by the pandas versions used in schools (newer pandas prints "dtype: str").
"""
from __future__ import annotations

import random

from qbank import F, mcq, CITIES
from g12_computer_science_kit import ST, run as _run, uniq, NAMES

S = 'cbse-g12-informatics-ch'


def run(code):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return _run(code).replace('dtype: str', 'dtype: object')


def run_or_err(code):
    try:
        return run(code)
    except Exception as e:  # noqa
        return f'Error ({type(e).__name__})'


def out_written(r, code, alts, marks=2, head='Write the output of the following code:'):
    ans = run(code)
    wrong = [w for w in uniq([run_or_err(a) for a in alts], [ans]) if not w.startswith('Error')]
    d = {'stem': f'{head}\n{code}', 'answer': ans, 'key': f'{marks} mark(s) for the exact output:\n{ans}', 'marks': marks}
    if len(wrong) >= 3:
        d['distractors'] = wrong
    return d


def out_mcq(r, code, alts, key='', head='What will be the output of the following code?'):
    ans = run(code)
    wrong = [w for w in uniq([run_or_err(a) for a in alts], [ans]) if not w.startswith('Error')]
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'{head}\n{code}', ans, wrong[:3], key or f'Output: {ans}', r)


LBL = [list('abcdef'), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'],
       ['Delhi', 'Mumbai', 'Pune', 'Agra', 'Patna', 'Surat'], ['P', 'Q', 'R', 'S', 'T', 'U']]
SV = ['S', 's1', 'marks', 'runs', 'sales', 'temp', 'stock', 'price']


# ====================================================================== ch02 st2 Series
def series_create(r):
    n = r.randint(3, 5)
    lb = r.choice(LBL)[:n]
    v = r.choice(SV)
    vals = r.sample(range(5, 99), n)
    t = r.randrange(4)
    if t == 0:
        code = f'import pandas as pd\n{v} = pd.Series({vals}, index={lb})\nprint({v})'
        alts = [f'import pandas as pd\n{v} = pd.Series({vals})\nprint({v})', f'import pandas as pd\n{v} = pd.Series({lb}, index={vals})\nprint({v})',
                f'import pandas as pd\n{v} = pd.Series({vals[::-1]}, index={lb})\nprint({v})']
    elif t == 1:
        d = dict(zip(lb, vals))
        code = f'import pandas as pd\nD = {d}\n{v} = pd.Series(D)\nprint({v})'
        alts = [f'import pandas as pd\n{v} = pd.Series({vals})\nprint({v})', f'import pandas as pd\n{v} = pd.Series({lb})\nprint({v})',
                f'import pandas as pd\n{v} = pd.Series({dict(zip(lb, vals[::-1]))})\nprint({v})']
    elif t == 2:
        k = r.randint(1, 99)
        code = f'import pandas as pd\n{v} = pd.Series({k}, index={lb})\nprint({v})'
        alts = [f'import pandas as pd\n{v} = pd.Series([{k}])\nprint({v})', f'import pandas as pd\n{v} = pd.Series({k}, index={lb[:-1]})\nprint({v})',
                f'import pandas as pd\n{v} = pd.Series({lb})\nprint({v})']
    else:
        a, b, c = r.randint(1, 10), r.randint(20, 40), r.choice([3, 4, 5])
        code = f'import pandas as pd\nimport numpy as np\n{v} = pd.Series(np.arange({a}, {b}, {c}))\nprint({v}.tail(3))'
        alts = [code.replace('tail(3)', 'head(3)'), code.replace(f'{b}, {c}', f'{b + c}, {c}'), code.replace('tail(3)', 'tail(2)')]
    return out_written(r, code, alts, marks=2)


def series_index(r):
    n = 5
    lb = r.choice(LBL)[:n]
    v = r.choice(SV)
    vals = r.sample(range(5, 99), n)
    i, j = sorted(r.sample(range(n), 2))
    if j - i < 2:
        j = min(n - 1, i + 2)
    t = r.randrange(5)
    base = f'import pandas as pd\n{v} = pd.Series({vals}, index={lb})\n'
    if t == 0:
        e, alts = f"{v}['{lb[i]}':'{lb[j]}']", [f'{v}.iloc[{i}:{j}]', f"{v}['{lb[i]}':'{lb[j - 1]}']", f'{v}.iloc[{i + 1}:{j + 1}]']
    elif t == 1:
        e, alts = f'{v}.iloc[{i}:{j}]', [f"{v}['{lb[i]}':'{lb[j]}']", f'{v}.iloc[{i}:{j + 1}]', f'{v}.iloc[{i + 1}:{j}]']
    elif t == 2:
        k = sorted(vals)[2]
        e, alts = f'{v}[{v} > {k}]', [f'{v}[{v} >= {k}]', f'{v}[{v} < {k}]', f'{v} > {k}']
    elif t == 3:
        e, alts = f'{v}.head(2) * 2', [f'{v}.head(2)', f'{v}.tail(2) * 2', f'{v}.head(3) * 2']
    else:
        e, alts = f'{v}[[\'{lb[i]}\', \'{lb[j]}\']]', [f"{v}['{lb[i]}':'{lb[j]}']", f'{v}.iloc[[{i + 1}, {j}]]' if j + 1 <= n else f'{v}.iloc[[{i}]]', f"{v}[['{lb[j]}', '{lb[i]}']]"]
    code = base + f'print({e})'
    return out_written(r, code, [base + f'print({a})' for a in alts], marks=2)


def series_value(r):
    n = 5
    lb = r.choice(LBL)[:n]
    v = r.choice(SV)
    vals = r.sample(range(5, 99), n)
    base = f'import pandas as pd\n{v} = pd.Series({vals}, index={lb})\n'
    t = r.randrange(5)
    i = r.randrange(n)
    if t == 0:
        e, alts = f"{v}['{lb[i]}'] + {v}.iloc[{(i + 2) % n}]", [f'{v}.iloc[{i}] + {v}.iloc[{(i + 1) % n}]', f"{v}['{lb[i]}']", f'{v}.iloc[{(i + 2) % n}] * 2']
    elif t == 1:
        e, alts = f'{v}.size, {v}.sum()', [f'{v}.size - 1, {v}.sum()', f'{v}.size, {v}.max()', f'{v}.size, {v}.sum() - {v}.iloc[0]']
    elif t == 2:
        e, alts = f'{v}.max() - {v}.min()', [f'{v}.max()', f'{v}.iloc[-1] - {v}.iloc[0]', f'{v}.max() + {v}.min()']
    elif t == 3:
        e, alts = f"{v}.index[{i}], {v}.values[{i}]", [f"{v}.index[{(i + 1) % n}], {v}.values[{i}]", f"{v}.index[{i}], {v}.values[{(i + 1) % n}]", f"{v}.index[{(i + 1) % n}], {v}.values[{(i + 1) % n}]"]
    else:
        e, alts = f'len({v}[{v} % 2 == 0])', [f'len({v}[{v} % 2 == 1])', f'len({v})', f'len({v}[{v} > 50])']
    code = base + f'print({e})'
    return out_mcq(r, code, [base + f'print({a})' for a in alts])


def series_math(r):
    lb = r.choice(LBL)
    a_idx = lb[:4]
    b_idx = r.sample(lb[1:6], 4)
    va, vb = r.sample(range(1, 50), 4), r.sample(range(1, 50), 4)
    t = r.randrange(3)
    if t == 0:
        code = f'import pandas as pd\nA = pd.Series({va}, index={a_idx})\nB = pd.Series({vb}, index={b_idx})\nprint(A + B)'
        alts = [code.replace('A + B', 'A.add(B, fill_value=0)'), code.replace('A + B', 'A - B'), code.replace(f'index={b_idx}', f'index={a_idx}')]
    elif t == 1:
        code = f'import pandas as pd\nA = pd.Series({va}, index={a_idx})\nB = pd.Series({vb}, index={b_idx})\nprint(A.add(B, fill_value=0))'
        alts = [code.replace('A.add(B, fill_value=0)', 'A + B'), code.replace('A.add(B, fill_value=0)', 'A.sub(B, fill_value=0)'), code.replace(f'index={b_idx}', f'index={a_idx}')]
    else:
        k = r.randint(2, 5)
        code = f'import pandas as pd\nA = pd.Series({va}, index={a_idx})\nprint(A * {k} - 1)'
        alts = [code.replace(f'A * {k} - 1', f'A * ({k} - 1)'), code.replace(f'* {k}', f'+ {k}'), code.replace('- 1', '+ 1')]
    return out_written(r, code, alts, marks=3 if t < 2 else 2)


# ====================================================================== ch02 st3/4/5 DataFrames
def df_data(r, n=None):
    n = n or r.randint(4, 5)
    names = r.sample(NAMES, n)
    cities = r.sample(CITIES[:6], 3)
    return {'Name': names, 'City': [r.choice(cities) for _ in range(n)], 'Maths': r.sample(range(40, 100), n), 'Science': r.sample(range(40, 100), n)}


def df_lit(d):
    return '{' + ', '.join(f"'{k}': {v}" for k, v in d.items()) + '}'


def df_create(r):
    d = df_data(r)
    t = r.randrange(4)
    if t == 0:
        code = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\nprint(df.shape, df.size)'
        alts = [code.replace('df.shape, df.size', 'df.shape[::-1], df.size'), code.replace('df.size', 'len(df)'), code.replace('df.shape, df.size', 'df.shape, df.size - len(df)')]
        return out_mcq(r, code, alts)
    if t == 1:
        L = [{'Name': d['Name'][i], 'Maths': d['Maths'][i]} if i % 2 == 0 else {'Name': d['Name'][i], 'Science': d['Science'][i]} for i in range(3)]
        code = f'import pandas as pd\nL = {L}\ndf = pd.DataFrame(L)\nprint(df)'
        alts = [code.replace('print(df)', 'print(df.fillna(0))'), code.replace('print(df)', 'print(df.T)'), code.replace('print(df)', 'print(df.dropna())')]
        return out_written(r, code, alts, marks=2)
    if t == 2:
        lb = r.choice(LBL)[:3]
        code = (f'import pandas as pd\nA = pd.Series({d["Maths"][:3]}, index={lb})\nB = pd.Series({d["Science"][:2]}, index={lb[:2]})\n'
                f'df = pd.DataFrame({{"Maths": A, "Science": B}})\nprint(df)')
        alts = [code.replace('index={}'.format(lb[:2]), 'index={}'.format(lb[1:])), code.replace('print(df)', 'print(df.fillna(0))'), code.replace('print(df)', 'print(df.T)')]
        return out_written(r, code, alts, marks=2)
    code = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)}, index={["S" + str(i + 1) for i in range(len(d["Name"]))]})\nprint(df.columns.tolist(), df.index.tolist()[-1])'
    alts = [code.replace('df.index.tolist()[-1]', 'df.index.tolist()[0]'), code.replace('df.columns.tolist()', 'df.columns.tolist()[1:]'), code.replace('[-1])', '[-2])')]
    return out_mcq(r, code, alts)


def df_ops(r):
    d = df_data(r)
    base = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\n'
    t = r.randrange(5)
    if t == 0:
        body = "df['Total'] = df['Maths'] + df['Science']\nprint(df[['Name', 'Total']])"
        alts = ["df['Total'] = df['Maths'] - df['Science']\nprint(df[['Name', 'Total']])", "df['Total'] = df['Maths']\nprint(df[['Name', 'Total']])",
                "df['Total'] = df['Maths'] + df['Science']\nprint(df[['Name', 'Total']].head(2))"]
    elif t == 1:
        body = "df = df.drop('City', axis=1)\nprint(df.shape)"
        alts = ["df = df.drop(0)\nprint(df.shape)", "print(df.shape)", "df = df.drop(['City', 'Maths'], axis=1)\nprint(df.shape)"]
    elif t == 2:
        body = "df = df.rename(columns={'Maths': 'Mat', 'Science': 'Sci'})\nprint(df.columns.tolist())"
        alts = ["print(df.columns.tolist())", "df = df.rename(columns={'Maths': 'Mat'})\nprint(df.columns.tolist())", "df = df.rename(index={0: 'A'})\nprint(df.columns.tolist())"]
    elif t == 3:
        body = "for i, row in df.iterrows():\n    if row['Maths'] > row['Science']:\n        print(row['Name'], end=' ')"
        alts = [body.replace('>', '<'), body.replace("row['Name']", "row['City']"), body.replace("row['Maths'] > row['Science']", "row['Maths'] > 60")]
        alts = [a for a in alts]
    else:
        n = r.randint(1, 3)
        body = f"print(df.tail({n})['Name'].tolist())"
        alts = [f"print(df.head({n})['Name'].tolist())", f"print(df.tail({n + 1})['Name'].tolist())", f"print(df.tail({n})['City'].tolist())"]
    code = base + body
    if not run(code).strip():
        raise ValueError('empty')
    return out_written(r, code, [base + a for a in alts], marks=2)


def df_loc(r):
    d = df_data(r, 5)
    idx = ['R' + str(i + 1) for i in range(5)]
    base = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)}, index={idx})\n'
    k = sorted(d['Maths'])[2]
    t = r.randrange(6)
    if t == 0:
        e, alts = "df.loc['R2':'R4', 'Name']", ["df.iloc[1:3, 0]", "df.loc['R2':'R3', 'Name']", "df.iloc[2:5, 0]"]
    elif t == 1:
        e, alts = 'df.iloc[1:3, 2:4]', ["df.loc['R2':'R3', 'Maths':'Science'].iloc[:1]", 'df.iloc[1:4, 2:4]', 'df.iloc[0:2, 2:4]']
    elif t == 2:
        e, alts = f"df[df['Maths'] > {k}]['Name']", [f"df[df['Maths'] >= {k}]['Name']", f"df[df['Maths'] < {k}]['Name']", f"df[df['Science'] > {k}]['Name']"]
    elif t == 3:
        e, alts = "df.at['R3', 'Science']", ["df.at['R3', 'Maths']", "df.iat[3, 3]", "df.at['R2', 'Science']"]
    elif t == 4:
        e, alts = f"df.loc[df['Science'] < {sorted(d['Science'])[3]}, ['Name', 'Science']]", [f"df.loc[df['Science'] <= {sorted(d['Science'])[3]}, ['Name', 'Science']]",
                                                                                         f"df.loc[df['Science'] > {sorted(d['Science'])[3]}, ['Name', 'Science']]", "df[['Name', 'Science']].head(3)"]
    else:
        e, alts = "df.iloc[-1, 0], df.iloc[0, -1]", ["df.iloc[0, 0], df.iloc[-1, -1]", "df.iloc[-1, 1], df.iloc[0, -1]", "df.iloc[-2, 0], df.iloc[0, -1]"]
    code = base + f'print({e})'
    if t in (3, 5):
        return out_mcq(r, code, [base + f'print({a})' for a in alts])
    return out_written(r, code, [base + f'print({a})' for a in alts], marks=2)


def csv_io(r):
    fn = r.choice(['marks.csv', 'sales.csv', 'stock.csv', 'result.csv', 'emp.csv'])
    t = r.randrange(5)
    rows = [
        (f'Which statement reads "{fn}" into a DataFrame df?', f'df = pd.read_csv("{fn}")', [f'df = pd.load_csv("{fn}")', f'df = pd.DataFrame.read("{fn}")', f'df = pd.open_csv("{fn}")']),
        (f'Which statement writes df to "{fn}" without the row labels (index)?', f'df.to_csv("{fn}", index=False)', [f'df.to_csv("{fn}", header=False)', f'df.write_csv("{fn}")', f'pd.to_csv(df, "{fn}")']),
        (f'Which statement reads "{fn}", whose values are separated by semicolons, into df?', f'df = pd.read_csv("{fn}", sep=";")', [f'df = pd.read_csv("{fn}", index=";")', f'df = pd.read_csv("{fn}", header=";")', f'df = pd.read_csv("{fn}", names=";")']),
        (f'"{fn}" has no header row. Which statement reads it and names the columns Roll, Name and Marks?', f'df = pd.read_csv("{fn}", header=None, names=["Roll", "Name", "Marks"])',
         [f'df = pd.read_csv("{fn}", header=["Roll", "Name", "Marks"])', f'df = pd.read_csv("{fn}", index=["Roll", "Name", "Marks"])', f'df = pd.read_csv("{fn}", columns="Roll, Name, Marks")']),
        (f'Which statement saves df to "{fn}" writing "NA" in place of missing values?', f'df.to_csv("{fn}", na_rep="NA")', [f'df.to_csv("{fn}", NaN="NA")', f'df.to_csv("{fn}", fillna="NA")', f'df.to_csv("{fn}", missing="NA")']),
    ]
    q, a, w = rows[t]
    return mcq(q, a, w, f'{a}.', r)


def df_program(r, marks=3):
    d = df_data(r)
    t = r.randrange(3)
    if t == 0:
        stem = (f'Write a Python program to create a DataFrame df from the dictionary {df_lit(d)}, add a column Total (= Maths + Science), '
                'and display the names of students whose Total is more than 150.')
        ans = f"import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\ndf['Total'] = df['Maths'] + df['Science']\nprint(df[df['Total'] > 150]['Name'])"
    elif t == 1:
        stem = (f'Write a Python program to create a DataFrame from the dictionary {df_lit(d)} with row labels S1, S2, …, then (i) display the rows S2 to S3 using loc, '
                '(ii) delete the column City, and (iii) display the first two rows.')
        idx = ['S' + str(i + 1) for i in range(len(d['Name']))]
        ans = f"import pandas as pd\ndf = pd.DataFrame({df_lit(d)}, index={idx})\nprint(df.loc['S2':'S3'])\ndf = df.drop('City', axis=1)\nprint(df.head(2))"
    else:
        stem = (f'Write a Python program that creates a DataFrame from the dictionary {df_lit(d)}, writes it to "class.csv" without the index, '
                'reads the file back into a new DataFrame and prints its shape.')
        ans = f"import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\ndf.to_csv('class.csv', index=False)\ndf2 = pd.read_csv('class.csv')\nprint(df2.shape)"
    from g12_computer_science_kit import run_files
    run_files(ans.replace('print(', 'str(')) if t == 2 else run(ans)
    return {'stem': stem, 'answer': ans, 'key': f'{marks} marks: creating the DataFrame 1, each required operation {"1" if marks == 3 else "1–2"}.', 'marks': marks}


# ====================================================================== ch03 pandas II
def sales_df(r, n=6):
    zones = r.sample(['North', 'South', 'East', 'West'], 3)
    items = r.sample(['Laptop', 'Mobile', 'Tablet', 'Printer', 'Camera'], 2)
    rows = [(zones[i % 3] if i < 3 else r.choice(zones), r.choice(items), r.randint(10, 99) * 100) for i in range(n)]
    return {'Zone': [x[0] for x in rows], 'Item': [x[1] for x in rows], 'Sales': [x[2] for x in rows]}


def stats_out(r):
    xs = [r.randint(20, 99) for _ in range(r.choice([5, 6, 7]))]
    xs[1] = xs[r.randint(2, len(xs) - 1)]
    v = r.choice(['marks', 'runs', 'temp', 'rain', 'S'])
    t = r.randrange(6)
    base = f'import pandas as pd\n{v} = pd.Series({xs})\n'
    if t == 0:
        e, alts = f'{v}.median()', [f'{v}.mean()', f'{v}.iloc[{len(xs) // 2}]', f'{v}.mode()[0]']
    elif t == 1:
        e, alts = f'{v}.mode()[0]', [f'{v}.median()', f'{v}.max()', f'{v}.min()']
    elif t == 2:
        e, alts = f'round({v}.mean(), 2)', [f'{v}.median()', f'round({v}.sum() / ({v}.count() - 1), 2)', f'round({v}.mean(), 1) + 1']
    elif t == 3:
        e, alts = f'{v}.quantile(0.5), {v}.max() - {v}.min()', [f'{v}.mean(), {v}.max() - {v}.min()', f'{v}.quantile(0.5), {v}.max()', f'{v}.quantile(0.25), {v}.max() - {v}.min()']
    elif t == 4:
        e, alts = f'round({v}.var(), 2)', [f'round({v}.std(), 2)', f'round({v}.var(ddof=0), 2)', f'round({v}.mean(), 2)']
    else:
        e, alts = f'{v}.count(), {v}.sum()', [f'{v}.count() + 1, {v}.sum()', f'{v}.count(), {v}.max()', f'{v}.nunique(), {v}.sum()']
    code = base + f'print({e})'
    return out_mcq(r, code, [base + f'print({a})' for a in alts])


def stats_df(r):
    d = df_data(r)
    base = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\n'
    t = r.randrange(3)
    if t == 0:
        body = "print(df[['Maths', 'Science']].max())"
        alts = ["print(df[['Maths', 'Science']].min())", "print(df[['Maths', 'Science']].max(axis=1))", "print(df[['Maths', 'Science']].sum())"]
    elif t == 1:
        body = "print(df[['Maths', 'Science']].mean(axis=1))"
        alts = ["print(df[['Maths', 'Science']].mean())", "print(df[['Maths', 'Science']].sum(axis=1))", "print(df[['Maths', 'Science']].max(axis=1))"]
    else:
        body = "print(df['Maths'].quantile([0.25, 0.75]))"
        alts = ["print(df['Maths'].quantile([0.25, 0.5]))", "print(df['Science'].quantile([0.25, 0.75]))", "print(df['Maths'].quantile([0.5, 0.75]))"]
    return out_written(r, base + body, [base + a for a in alts], marks=2)


def group_out(r):
    d = sales_df(r)
    base = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\n'
    t = r.randrange(4)
    if t == 0:
        body = "print(df.groupby('Zone')['Sales'].sum())"
        alts = ["print(df.groupby('Zone')['Sales'].max())", "print(df.groupby('Item')['Sales'].sum())", "print(df.groupby('Zone')['Sales'].count())"]
    elif t == 1:
        body = "print(df.groupby('Item')['Sales'].count())"
        alts = ["print(df.groupby('Item')['Sales'].sum())", "print(df.groupby('Zone')['Sales'].count())", "print(df.groupby('Item')['Sales'].max())"]
    elif t == 2:
        body = "print(df.sort_values('Sales', ascending=False).head(3)[['Zone', 'Sales']])"
        alts = [body.replace('ascending=False', 'ascending=True'), body.replace('head(3)', 'head(2)'), body.replace('head(3)', 'tail(3)')]
    else:
        body = "print(df.groupby('Zone')['Sales'].agg(['min', 'max']))"
        alts = [body.replace("['min', 'max']", "['sum', 'max']"), body.replace("'Zone'", "'Item'"), body.replace("['min', 'max']", "['count', 'max']")]
    return out_written(r, base + body, [base + a for a in alts], marks=3)


def pivot_out(r):
    d = sales_df(r)
    base = f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\n'
    t = r.randrange(3)
    if t == 0:
        body = "print(df.pivot_table(index='Zone', columns='Item', values='Sales', aggfunc='sum'))"
        alts = [body.replace("'sum'", "'max'"), body.replace("index='Zone', columns='Item'", "index='Item', columns='Zone'"), body.replace("'sum'", "'count'")]
    elif t == 1:
        body = "print(df.pivot_table(index='Item', values='Sales', aggfunc='mean'))"
        alts = [body.replace("'mean'", "'sum'"), body.replace("index='Item'", "index='Zone'"), body.replace("'mean'", "'max'")]
    else:
        body = "df2 = df.set_index('Zone')\nprint(df2.index.tolist()[:3], df2.shape)"
        alts = ["df2 = df.set_index('Item')\nprint(df2.index.tolist()[:3], df2.shape)", "df2 = df.reset_index()\nprint(df2.index.tolist()[:3], df2.shape)",
                "df2 = df\nprint(df2.index.tolist()[:3], df2.shape)"]
    return out_written(r, base + body, [base + a for a in alts], marks=3)


def missing_out(r):
    n = 5
    import math
    a = [r.choice([r.randint(10, 99), None]) for _ in range(n)]
    b = [r.choice([r.randint(10, 99), None]) for _ in range(n)]
    if a.count(None) == 0:
        a[r.randrange(n)] = None
    if b.count(None) == 0:
        b[r.randrange(n)] = None
    if all(x is None for x in a) or all(x is None for x in b):
        raise ValueError('all nan')
    A = str(a).replace('None', 'np.nan')
    B = str(b).replace('None', 'np.nan')
    base = f"import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({{'Eng': {A}, 'Hindi': {B}}})\n"
    t = r.randrange(5)
    if t == 0:
        e, alts = 'df.isnull().sum().sum()', ['df.isnull().sum().max()', 'df.notnull().sum().sum()', 'len(df.dropna())', 'df.isnull().sum().min()', 'df.size']
    elif t == 1:
        e, alts = 'df.dropna().shape', ["df.dropna(how='all').shape", 'df.shape', 'df.fillna(0).shape[::-1]', 'df.dropna(axis=1).shape', 'df.dropna().shape[::-1]']
    elif t == 2:
        e, alts = "df.fillna(0)['Eng'].sum()", ["df['Eng'].count()", "df.fillna(1)['Eng'].sum()", "df.fillna(0)['Hindi'].sum()", "df.fillna(10)['Eng'].sum()", "df.fillna(0)['Eng'].max()"]
    elif t == 3:
        e, alts = "len(df.dropna(how='all'))", ['len(df.dropna())', 'len(df)', "df['Eng'].count()", "df['Hindi'].count()", 'df.isnull().sum().sum()', 'len(df.columns)']
    else:
        e, alts = "df['Hindi'].count(), df['Hindi'].isnull().sum()", ["df['Hindi'].count(), df['Eng'].isnull().sum()", "len(df), df['Hindi'].isnull().sum()", "df['Eng'].count(), df['Hindi'].isnull().sum()", "df['Hindi'].isnull().sum(), df['Hindi'].count()", "df['Eng'].count(), df['Eng'].isnull().sum()"]
    code = base + f'print({e})'
    return out_mcq(r, code, [base + f'print({x})' for x in alts])


def missing_written(r):
    v = missing_out(r)
    return {'stem': v['stem'].replace('What will be the output of the following code?', 'Write the output of the following code:'),
            'answer': v['answer'], 'key': '2 marks: ' + v['key'], 'marks': 2, 'distractors': [o for o in v['options'] if o != v['answer']]}


SQLX = [
    ('Which library function creates the connection used by df.to_sql() and pd.read_sql()?', 'create_engine() from sqlalchemy', ['connect() from csv', 'open() from os', 'cursor() from pandas'],
     'sqlalchemy.create_engine() builds the engine (for example with the pymysql driver).'),
    ('Which statement reads the MySQL table STUDENT into a DataFrame df using engine?', 'df = pd.read_sql("SELECT * FROM STUDENT", engine)', ['df = pd.read_csv("STUDENT", engine)',
     'df = engine.read("STUDENT")', 'df = pd.to_sql("STUDENT", engine)'], 'read_sql() runs the query and returns a DataFrame.'),
    ('Which argument of to_sql() adds rows to an existing table instead of replacing it?', 'if_exists="append"', ['if_exists="replace"', 'mode="a"', 'append=True'],
     'if_exists can be "fail", "replace" or "append".'),
    ('Which statement writes df to a new MySQL table RESULT, replacing it if it exists, without the index?', 'df.to_sql("RESULT", engine, if_exists="replace", index=False)',
     ['df.to_csv("RESULT", engine)', 'pd.read_sql("RESULT", engine, index=False)', 'df.to_sql(engine, "RESULT", mode="w")'], 'to_sql(name, con, if_exists, index).'),
    ('Which Python package is commonly used as the MySQL driver with sqlalchemy in the NCERT examples?', 'pymysql', ['matplotlib', 'numpy', 'csv'], 'The URL is "mysql+pymysql://user:password@host/database".'),
    ('In create_engine("mysql+pymysql://root:tiger@localhost/school"), "school" is the:', 'database name', ['password', 'user name', 'table name'],
     'The URL format is dialect+driver://user:password@host/database.'),
    ('Which method of a DataFrame stores its rows in a MySQL table?', 'to_sql()', ['read_sql()', 'to_csv()', 'execute()'], 'df.to_sql(table_name, engine, ...) writes the DataFrame to MySQL.'),
    ('What does pd.read_sql() return?', 'A DataFrame', ['A cursor object', 'A list of tuples', 'A CSV file'], 'read_sql() returns the query result as a DataFrame.'),
    ('In create_engine("mysql+pymysql://root:tiger@localhost/school"), "tiger" is the:', 'password', ['user name', 'database name', 'host name'],
     'The URL format is dialect+driver://user:password@host/database.'),
    ('In create_engine("mysql+pymysql://root:tiger@localhost/school"), "localhost" is the:', 'host on which the MySQL server runs', ['database name', 'driver', 'table name'],
     'localhost means the MySQL server runs on the same computer.'),
    ('Which command installs the MySQL driver used with sqlalchemy?', 'pip install pymysql', ['import pymysql', 'pip install csv', 'mysql install pandas'],
     'Packages are installed with pip; import only loads an installed package.'),
    ('What happens if df.to_sql("RESULT", engine) is run (default if_exists) when table RESULT already exists?', 'An error (ValueError) is raised', ['The rows are appended',
     'The table is replaced', 'Nothing happens'], 'The default if_exists="fail" raises an error if the table exists.'),
]


def sqlx(r):
    q, a, w, k = r.choice(SQLX)
    return mcq(q, a, w, k, r)


def sqlx_case(r):
    who = r.choice(NAMES)
    tb = r.choice(['RESULT', 'SALES', 'STOCK', 'MARKS'])
    return {'stem': (f'{who} has a DataFrame df to be stored in the MySQL database school (user root, password tiger) as table {tb}. Complete the code:\n'
                     'import pandas as pd\nfrom sqlalchemy import _____          # (i)\nengine = _____("mysql+pymysql://root:tiger@localhost/school")   # (ii)\n'
                     f'df._____("{tb}", engine, if_exists="replace", index=False)   # (iii)\ndf2 = pd._____("SELECT * FROM {tb}", engine)   # (iv)'),
            'answer': '(i) create_engine (ii) create_engine (iii) to_sql (iv) read_sql', 'key': '1 mark each.', 'marks': 4}


def stats_program(r, marks=5):
    d = sales_df(r)
    stem = (f'A DataFrame df is created from {df_lit(d)}. Write Python statements to: (i) display the total Sales of each Zone (ii) display the maximum Sales of each Item '
            '(iii) display the rows sorted in descending order of Sales (iv) display the average Sales rounded to 2 decimal places (v) add a column Bonus equal to 5% of Sales.')
    ans = ("(i) print(df.groupby('Zone')['Sales'].sum())\n(ii) print(df.groupby('Item')['Sales'].max())\n(iii) print(df.sort_values('Sales', ascending=False))\n"
           "(iv) print(round(df['Sales'].mean(), 2))\n(v) df['Bonus'] = df['Sales'] * 0.05")
    run(f'import pandas as pd\ndf = pd.DataFrame({df_lit(d)})\n' + '\n'.join(l.split(') ', 1)[1] for l in ans.split('\n')))
    return {'stem': stem, 'answer': ans, 'key': f'{marks} marks: 1 for each statement.', 'marks': marks}


CH02 = [ST(S + '02-st1', 'Python libraries for data handling', """
T: Pandas | a Python library (PANel DAta) used for data manipulation and analysis with Series and DataFrame structures
T: NumPy | a Python library (Numerical Python) for fast numerical computation with arrays
T: Matplotlib | a Python library used to draw plots and charts
T: Series | a one-dimensional labelled array that can hold data of any type
T: DataFrame | a two-dimensional labelled data structure with rows and columns, like a table
Q: Which command installs Pandas? | pip install pandas | python install pandas | import pandas | pandas install
Q: Which statement imports Pandas with the usual alias? | import pandas as pd | import pd as pandas | from pandas import pd | include pandas
Q: A Pandas Series is: | one-dimensional | two-dimensional | three-dimensional | zero-dimensional
Q: Which library is used for plotting in Python? | Matplotlib | Pandas only | MySQL | csv
Q: A DataFrame is: | two-dimensional | one-dimensional | a single value | a text file
Q: In a Series, the values are labelled by its: | index | header | column name only | key file
S+: Pandas is built on top of NumPy
S+: A DataFrame can hold columns of different data types
S+: The size of a Series cannot be changed once it is created, but its values can be changed
S+: The values and the size of a DataFrame can both be changed
S-: A Series is two-dimensional | A Series is one-dimensional; a DataFrame is two-dimensional
S-: Pandas is used only for plotting graphs | Pandas is for data analysis; Matplotlib is for plotting
S-: A DataFrame can store only one data type | Different columns can have different data types
C: Pandas is preferred over plain lists for data analysis | it provides labelled data, fast operations, handling of missing data and easy reading of CSV files
X: C2 D2 2 | Differentiate between a Series and a DataFrame. | Series: one-dimensional labelled array, size immutable; DataFrame: two-dimensional with rows and columns (like a table), size mutable, columns can have different types.
"""), ST(S + '02-st2', 'Pandas Series', """
T: index | the labels attached to the values of a Series, by default 0, 1, 2 …
T: head() | the method that returns the first n elements of a Series (5 by default)
T: tail() | the method that returns the last n elements of a Series (5 by default)
T: vectorised operation | an operation applied to every element of a Series at once, such as S * 2
Q: s.head() returns by default the first: | 5 elements | 3 elements | 10 elements | 1 element
Q: When two Series with different indexes are added, unmatched labels get: | NaN | 0 | an error | the value of the first Series
Q: Slicing a Series with labels, as in s['b':'d'], includes: | both 'b' and 'd' | 'b' but not 'd' | neither end | only 'd'
Q: pd.Series(7, index=['a', 'b', 'c']) creates a Series with: | 7 in all three positions | one element 7 | an error | 7 only at 'a'
Q: Which attribute gives the number of elements in a Series s? | s.size | s.shape[1] | s.length | s.count
Q: Which attribute gives the labels of a Series s? | s.index | s.values | s.name | s.keys
S+: A Series can be created from a list, a NumPy array, a dictionary or a scalar value
S+: When a Series is created from a dictionary, the keys become the index
S+: Positional slicing with iloc excludes the end position
S+: Arithmetic between two Series is done on matching index labels
S-: Label slicing excludes the end label | Label slicing includes the end label; positional slicing excludes it
S-: Adding two Series with different indexes gives an error | Unmatched labels give NaN
S-: s.tail() returns the last 3 elements by default | It returns the last 5 elements
C: s1 + s2 gives NaN for some labels | those labels are present in only one of the two Series
C: s * 2 doubles every element of s | arithmetic operations on a Series are vectorised
X: C2 D3 2 | Write two ways of creating the Series s with values 10, 20, 30 and index 'a', 'b', 'c'. | pd.Series([10, 20, 30], index=['a', 'b', 'c']); pd.Series({'a': 10, 'b': 20, 'c': 30}).
"""), ST(S + '02-st3', 'creating DataFrames', """
T: dictionary of lists | a way of creating a DataFrame in which each key becomes a column name and its list gives the column values
T: list of dictionaries | a way of creating a DataFrame in which each dictionary becomes a row and missing keys give NaN
T: shape | the attribute giving the number of rows and columns of a DataFrame as a tuple
T: read_csv() | the Pandas function that reads a CSV file into a DataFrame
Q: df.shape for a DataFrame with 4 rows and 3 columns is: | (4, 3) | (3, 4) | 12 | 7
Q: When a DataFrame is created from a list of dictionaries, a missing key gives: | NaN | 0 | an error | an empty string
Q: In a DataFrame made from a dictionary of lists, the keys become: | column labels | row labels | values | data types
Q: Which attribute gives the total number of values in a DataFrame df? | df.size | df.shape | df.count | len(df.columns)
Q: Which function creates a DataFrame from a CSV file? | pd.read_csv() | pd.to_csv() | pd.DataFrame.csv() | pd.load()
S+: A DataFrame can be created from a dictionary of Series; the index labels are aligned
S+: len(df) gives the number of rows of a DataFrame
S+: A DataFrame can be created from a two-dimensional NumPy array
S-: df.shape returns (columns, rows) | It returns (rows, columns)
S-: All lists in a dictionary of lists may have different lengths | They must have the same length, or an error is raised
C: A DataFrame made from a dictionary of Series may contain NaN | a label present in one Series but not another has no value in that column
X: C2 D2 2 | Write code to create a DataFrame from a list of two dictionaries and say what happens to a missing key. | pd.DataFrame([{'A': 1, 'B': 2}, {'A': 3}]) – the missing B in row 1 becomes NaN.
"""), ST(S + '02-st4', 'DataFrame operations', """
T: drop() | the method that removes rows (axis=0) or columns (axis=1) from a DataFrame
T: rename() | the method that changes row or column labels using a dictionary
T: iterrows() | the method that iterates over a DataFrame row by row, giving the index and the row as a Series
T: iteritems / items() | the method that iterates over a DataFrame column by column
Q: Which statement deletes the column City from df? | df.drop('City', axis=1) | df.drop('City', axis=0) | df.remove('City') | df.delete('City')
Q: Which statement adds a column Total to df? | df['Total'] = df['A'] + df['B'] | df.add('Total') | df.insert_row('Total') | df.Total() = 0
Q: df.T gives: | the transpose (rows become columns) | the top rows | the total of each column | the data types
Q: Which statement renames column 'Maths' to 'Mat'? | df.rename(columns={'Maths': 'Mat'}) | df.rename(index={'Maths': 'Mat'}) | df.columns('Mat') | df.change('Maths', 'Mat')
Q: iterrows() returns each row as: | a pair of index and Series | a list | a dictionary of columns | a NumPy array only
S+: drop() returns a new DataFrame unless inplace=True is given
S+: A new row with label 'R9' can be added with df.loc['R9'] = [ … ]
S+: del df['col'] deletes a column permanently
S-: axis=0 in drop() refers to columns | axis=0 refers to rows; axis=1 refers to columns
S-: df.head() shows the last five rows | head() shows the first five rows; tail() shows the last five
C: df.drop('City', axis=1) does not change df unless it is assigned back | drop() returns a new DataFrame by default
X: C2 D3 2 | Write statements to (i) delete the row with label 'R2' from df (ii) rename column 'Sci' to 'Science'. | (i) df = df.drop('R2') (ii) df = df.rename(columns={'Sci': 'Science'})
"""), ST(S + '02-st5', 'indexing DataFrames and CSV files', """
T: loc | the label-based indexer of a DataFrame, as in df.loc['R1':'R3', 'Name']
T: iloc | the position-based indexer of a DataFrame, as in df.iloc[0:2, 1]
T: at | the accessor used to get or set a single value by row and column label
T: Boolean indexing | selecting rows using a condition, as in df[df['Marks'] > 60]
T: to_csv() | the DataFrame method that writes data to a CSV file
Q: df.loc['R1':'R3'] includes the row: | R3 | only R1 and R2 | none | R4
Q: df.iloc[0:2] selects the rows at positions: | 0 and 1 | 0, 1 and 2 | 1 and 2 | 2 only
Q: Which accessor gets a single value using labels? | at | iat | iloc | ix
Q: Which parameter of to_csv() stops the index from being written? | index=False | header=False | sep=None | na_rep
Q: Which parameter of read_csv() names the separator of the values? | sep | header | index_col | names
S+: Label slices with loc include the end label
S+: Position slices with iloc exclude the end position
S+: A condition such as df['Marks'] > 60 gives a Boolean Series
S+: read_csv() uses the first line of the file as the column names by default
S-: iloc uses labels to select data | iloc uses integer positions; loc uses labels
S-: to_csv() reads data from a CSV file | to_csv() writes; read_csv() reads
C: df[df['City'] == 'Pune'] shows only some rows | the Boolean condition keeps the rows where it is True
X: C2 D3 2 | Differentiate between loc and iloc with an example. | loc selects by labels and includes the end label (df.loc['R1':'R3']); iloc selects by integer positions and excludes the end (df.iloc[0:3]).
""")]

CH03 = [ST(S + '03-st1', 'descriptive statistics', """
T: mean() | the method that returns the arithmetic average of the values
T: median() | the method that returns the middle value of the sorted data
T: mode() | the method that returns the most frequent value(s)
T: quantile() | the method that returns the value below which a given fraction of the data lies, such as quantile(0.25)
T: std() | the method that returns the standard deviation of the values
T: var() | the method that returns the variance of the values
Q: quantile(0.5) is the same as the: | median | mean | mode | maximum
Q: Which method gives the most frequent value? | mode() | median() | mean() | count()
Q: df.max(axis=1) gives the maximum of each: | row | column | data type | index label
Q: count() counts: | non-missing values | all values including NaN | only NaN values | columns
Q: Variance is the square of the: | standard deviation | mean | median | range
S+: By default the statistical methods of a DataFrame work column-wise
S+: count() ignores missing (NaN) values
S+: The first quartile is quantile(0.25) and the third quartile is quantile(0.75)
S-: mean() includes NaN values as zero | NaN values are skipped
S-: median() returns the most frequent value | median() returns the middle value; mode() returns the most frequent
C: The median is less affected by extreme values than the mean | it depends only on the middle position of the sorted data
X: C2 D2 2 | Differentiate between mean() and median() with an example. | mean = sum/count (for 2, 4, 9 it is 5); median = middle value of sorted data (4); the median is not affected by extreme values.
"""), ST(S + '03-st2', 'aggregation, sorting and grouping', """
T: groupby() | the method that splits a DataFrame into groups based on a column so that aggregate functions can be applied to each group
T: sort_values() | the method that sorts a DataFrame by the values of one or more columns
T: agg() | the method that applies one or more aggregate functions at once, as in agg(['min', 'max'])
Q: df.sort_values('Sales', ascending=False) sorts in: | descending order of Sales | ascending order of Sales | order of index | order of columns
Q: df.groupby('Zone')['Sales'].sum() gives: | total Sales of each Zone | total of all columns | the number of zones | the first row of each zone
Q: Which method applies several aggregate functions together? | agg() | apply_all() | groupall() | sum_all()
Q: df.sort_index() sorts by: | the row labels | the first column | the values | the column names only
S+: groupby() is usually followed by an aggregate function such as sum(), count() or max()
S+: The groups of groupby() appear in sorted order of the group keys by default
S+: sort_values() can sort on more than one column by passing a list
S-: sort_values() sorts in descending order by default | It sorts in ascending order by default
S-: groupby() changes the original DataFrame | It returns a grouped object; df is unchanged
C: df.groupby('City')['Sales'].count() shows how many rows each city has | count() is applied to each group separately
X: C2 D3 2 | Write statements to (i) display the total Sales of each Zone (ii) sort df in descending order of Sales. | (i) df.groupby('Zone')['Sales'].sum() (ii) df.sort_values('Sales', ascending=False)
"""), ST(S + '03-st3', 'altering the index and pivoting', """
T: set_index() | the method that makes a column the index (row labels) of a DataFrame
T: reset_index() | the method that moves the index back into a column and gives the default 0, 1, 2 … index
T: pivot_table() | the method that reshapes a DataFrame into a summary table, aggregating values for each index-column combination
T: pivoting | reshaping data so that values of one column become new columns
Q: Which method makes the column Name the index of df? | df.set_index('Name') | df.reset_index('Name') | df.index('Name') | df.pivot('Name')
Q: The default aggregate function of pivot_table() is: | mean | sum | count | max
Q: Which method restores the default integer index? | reset_index() | set_index() | sort_index() | reindex_like()
Q: In pivot_table(index='Zone', columns='Item', values='Sales'), the column labels of the result are the values of: | Item | Zone | Sales | the index
S+: pivot_table() can aggregate duplicate entries with a function such as sum
S+: After set_index('Name'), Name is no longer an ordinary column
S-: pivot() can handle duplicate index-column pairs by summing them | pivot() raises an error for duplicates; pivot_table() aggregates them
S-: reset_index() deletes the old index permanently | It moves the old index into a column
C: pivot_table() is used for summary reports | it groups the data by rows and columns and aggregates the values
X: C2 D3 2 | Differentiate between pivot() and pivot_table(). | pivot() only reshapes and fails on duplicate index/column pairs; pivot_table() reshapes and aggregates duplicates using aggfunc (mean by default).
"""), ST(S + '03-st4', 'handling missing values', """
T: missing value | a value that is not available, shown as NaN in Pandas
T: isnull() | the method that returns True for each missing value
T: dropna() | the method that removes rows (or columns) containing missing values
T: fillna() | the method that replaces missing values with a given value
Q: df.dropna() by default removes: | every row that has at least one NaN | only rows with all NaN | every column | nothing
Q: df.fillna(0) replaces: | NaN values with 0 | 0 with NaN | all values with 0 | the first row with 0
Q: df.isnull().sum() gives: | the number of missing values in each column | the total of each column | the number of rows | the number of columns
Q: Which option of dropna() removes only rows in which all values are missing? | how='all' | how='any' | axis=1 | thresh=0
S+: NaN stands for Not a Number
S+: dropna(how='all') keeps rows that have at least one value
S+: Missing values can be estimated, for example by filling them with the column mean
S-: dropna() replaces missing values with 0 | dropna() removes them; fillna() replaces them
S-: isnull() removes missing values | isnull() only detects them by returning True/False
C: Dropping rows with NaN can reduce the data a lot | every row with even one missing value is removed
X: C2 D3 2 | Differentiate between dropna() and fillna(). | dropna() removes rows/columns with missing values; fillna(v) keeps the rows and replaces missing values with v.
"""), ST(S + '03-st5', 'Pandas and MySQL', """
T: sqlalchemy | a Python library whose create_engine() function creates the connection used by Pandas to work with MySQL
T: to_sql() | the DataFrame method that writes a DataFrame into a database table
T: read_sql() | the Pandas function that runs an SQL query and returns the result as a DataFrame
T: pymysql | a Python MySQL driver used in the connection string mysql+pymysql://user:password@host/database
Q: Which method writes a DataFrame to a MySQL table? | to_sql() | to_csv() | read_sql() | write_sql()
Q: Which function reads the result of a query into a DataFrame? | pd.read_sql() | pd.read_csv() | df.to_sql() | pd.query()
Q: The option if_exists="replace" in to_sql(): | drops the existing table and creates it again | adds rows | raises an error | does nothing
Q: The default value of if_exists in to_sql() is: | "fail" | "replace" | "append" | "ignore"
S+: to_sql() needs a table name and a connection (engine)
S+: index=False stops the DataFrame index from being written as a column
S+: read_sql() can be given any SELECT query
S-: read_sql() writes a DataFrame into MySQL | read_sql() reads; to_sql() writes
S-: if_exists="append" deletes the old table | "append" adds rows; "replace" drops and recreates
C: An engine must be created before using to_sql() | to_sql() needs a connection object to know which database to write to
X: C2 D2 2 | Write statements to store df in MySQL table MARKS (database school, user root, password tiger). | from sqlalchemy import create_engine; engine = create_engine("mysql+pymysql://root:tiger@localhost/school"); df.to_sql("MARKS", engine, if_exists="replace", index=False)
""")]


def fams_ch02_03():
    E = {}
    E[S + '02-st1'] = [F('C2', 'D2', 'short', series_create, marks=2), F('C3', 'D3', 'mcq', series_value), F('C4', 'D4', 'multi_step', df_program, marks=3)]
    E[S + '02-st2'] = [F('C2', 'D2', 'short', series_create, marks=2), F('C3', 'D3', 'short', series_index, marks=2), F('C2', 'D3', 'mcq', series_value), F('C3', 'D2', 'mcq', series_value),
                       F('C3', 'D4', 'multi_step', series_math, marks=3, gap='G5'), F('C4', 'D3', 'short', series_index, marks=2), F('C4', 'D4', 'multi_step', series_math, marks=3),
                       F('C1', 'D1', 'mcq', series_value)]
    E[S + '02-st3'] = [F('C2', 'D2', 'short', df_create, marks=2), F('C3', 'D3', 'short', df_create, marks=2), F('C4', 'D4', 'multi_step', df_program, marks=3), F('C3', 'D4', 'short', df_create, marks=2, gap='G5')]
    E[S + '02-st4'] = [F('C2', 'D3', 'short', df_ops, marks=2), F('C3', 'D3', 'short', df_ops, marks=2), F('C4', 'D4', 'multi_step', df_program, marks=3), F('C3', 'D4', 'short', df_ops, marks=2, gap='G5'),
                       F('C4', 'D5', 'long', lambda r: df_program(r, 5), marks=5)]
    E[S + '02-st5'] = [F('C2', 'D2', 'mcq', csv_io), F('C3', 'D3', 'short', df_loc, marks=2), F('C3', 'D4', 'short', df_loc, marks=2, gap='G5'), F('C4', 'D3', 'short', df_loc, marks=2),
                       F('C4', 'D4', 'multi_step', df_program, marks=3), F('C1', 'D1', 'mcq', csv_io)]
    E[S + '03-st1'] = [F('C2', 'D2', 'mcq', stats_out), F('C3', 'D3', 'mcq', stats_out), F('C3', 'D4', 'short', stats_df, marks=2, gap='G5'), F('C4', 'D3', 'short', stats_df, marks=2),
                       F('C4', 'D4', 'long', stats_program, marks=5), F('C1', 'D1', 'mcq', stats_out)]
    E[S + '03-st2'] = [F('C3', 'D3', 'multi_step', group_out, marks=3), F('C3', 'D4', 'multi_step', group_out, marks=3, gap='G5'), F('C4', 'D4', 'long', stats_program, marks=5),
                       F('C2', 'D3', 'multi_step', group_out, marks=3)]
    E[S + '03-st3'] = [F('C3', 'D3', 'multi_step', pivot_out, marks=3), F('C3', 'D4', 'multi_step', pivot_out, marks=3, gap='G5'), F('C4', 'D4', 'multi_step', pivot_out, marks=3)]
    E[S + '03-st4'] = [F('C2', 'D2', 'mcq', missing_out), F('C3', 'D3', 'mcq', missing_out), F('C3', 'D4', 'short', missing_written, marks=2, gap='G5'), F('C4', 'D3', 'short', missing_written, marks=2),
                       F('C4', 'D4', 'mcq', missing_out, gap='G5')]
    E[S + '03-st5'] = [F('C2', 'D2', 'mcq', sqlx), F('C3', 'D3', 'mcq', sqlx), F('C4', 'D4', 'case', sqlx_case, marks=4, gap='G7'), F('C1', 'D1', 'mcq', sqlx)]
    return [CH02, CH03], E
