"""Cambridge International AS Level Accounting 9706, AS content (grade 11), 27 chapters.

Paper 1 (Multiple Choice) and Paper 2 (Fundamentals of Accounting, structured questions) style items:
double entry and books of prime entry, the trial balance, accounting concepts, sole-trader statements,
accruals and prepayments, irrecoverable debts, depreciation, inventory, bank reconciliation, control
accounts, correction of errors, incomplete records, partnerships, clubs, manufacturing accounts, limited
companies, ratio analysis and AS cost accounting (absorption and marginal costing).

Each calculation topic registers a scenario "spec" (setup + structured parts with computed answers and
[n] mark points). One spec feeds four templates: a C3 structured/numeric item (MCQ at D1), a C2
spot-the-error item, and a C4 multi-part problem that adds evaluative parts from the topic's `disc` list.
"""
import re

from ._lib import topic, mcq, compose, PEOPLE, CTX
from .g12_accountancy import m as _m, m2 as _m2, pc, firm, co, ye, step, fixed, rs, FIRMS


def cap1(s):
    return s[:1].upper() + s[1:]


def m(x):
    return _m(x).replace('-$', '−$')


def m2(x):
    return _m2(x).replace('-$', '−$')

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

ROM = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii']
WHO = ['A trainee accountant', 'A student', 'The bookkeeper', 'A junior clerk', 'An accounts assistant', 'The owner']


def pp(r, k=1):
    return r.sample(PEOPLE, k) if k > 1 else r.choice(PEOPLE)


def lst(items):
    return ' '.join(f'({ROM[i]}) {x.rstrip(".")}' for i, x in enumerate(items))


def dp1(x):
    return f'{x:.1f}'


def dp2(x):
    return f'{x:.2f}'


def ratio_s(x, dp=2):
    return f'{x:.{dp}f}:1'


def days(x):
    return f'{x:.0f} days' if abs(x - round(x)) < 0.05 else f'{x:.1f} days'


def num_opts(f, correct, vals):
    """(correct_str, distractor_strs): the explicit wrong values first, padded to at least 3."""
    c = f(correct)
    ex = []
    for v in vals:
        s = f(v)
        if s != c and s not in ex:
            ex.append(s)
    if len(ex) >= 3:
        return c, ex[:5]
    for v in (correct * 1.1, correct * 0.9, correct * 1.25, correct * 0.8, correct * 2, correct * 0.5, correct + 100, correct - 100):
        s = f(v)
        if s != c and s not in ex:
            ex.append(s)
        if len(ex) >= 3:
            break
    return c, ex


def P(parts):
    return [(lambda r, p=p: p) for p in parts if p]


TOPS = []


def A(ch, name, keys, mcqs=(), exps=(), disc=()):
    """Topic with fixed C1 MCQs (stem, answer, [distractors], why) and C2 explain items (stem, answer, key[n])."""
    t = topic(name, *keys)
    t.disc = list(disc)
    if mcqs:
        fixed(t, 'C1', (1, 2, 3), [(s, a, f'{a}. {w} [1]', ds) for s, a, ds, w in mcqs])
    if exps:
        fixed(t, 'C2', (1, 2, 3, 4), list(exps))
    CHAPTERS.setdefault(ch, []).append(t)
    TOPS.append(t)
    return t


class _Ctx(dict):
    def __missing__(self, k):
        return {'f': 'the business', 'p': 'the owner', 'who': 'the users'}.get(k, k)


_MK = re.compile(r'\[(\d+)\]\s*$')


def _pm(key):
    x = _MK.search(key)
    return int(x.group(1)) if x else 1


def build(r, intro, parts, want, min_parts=1, type_=None):
    """Structured item that always keeps part 1 (the core task) and adds later parts while marks fit `want`."""
    parts = [p for p in parts if p]
    if not parts:
        return None
    chosen = [0]
    tot = _pm(parts[0][2])
    rest = list(range(1, len(parts)))
    r.shuffle(rest)
    for i in rest:
        mk = _pm(parts[i][2])
        if tot + mk <= max(want, tot) or len(chosen) < min_parts:
            chosen.append(i)
            tot += mk
    chosen.sort()
    got = [parts[i] for i in chosen]
    if len(got) < min_parts:
        return None
    if len(got) == 1:
        q = {'stem': intro.strip() + ' ' + got[0][0], 'answer': got[0][1], 'key': got[0][2]}
    else:
        L = 'abcdefgh'
        q = {'stem': intro.strip() + ' ' + ' '.join(f'({L[j]}) {x[0]}' for j, x in enumerate(got)),
             'answer': ' '.join(f'({L[j]}) {x[1]}' for j, x in enumerate(got)),
             'key': ' '.join(f'({L[j]}) {x[2]}' for j, x in enumerate(got))}
    q['marks'] = max(1, min(20, tot))
    q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
    if type_:
        q['type'] = type_
    return q


def _disc(t, r, s):
    out = []
    ctx = _Ctx(s.get('ctx', {}))
    for d in t.disc:
        x = d(r, s) if callable(d) else tuple(y.format_map(ctx) if isinstance(y, str) and '{' in y else y for y in d)
        if x:
            out.append(x)
    return out


def spec(t, D=(1, 2, 3, 4, 5), typ='numerical', err=True, c4=True, c3=True):
    """Register a scenario spec fn(r, D) -> dict(setup, parts=[(ask, ans, key[n])], mcq=(q, correct, [ds], key) | None,
    err=(claim, why, right, work, noun) | None, ctx={...})."""
    def deco(fn):
        nm_ = fn.__name__
        if c3:
            def c3f(r, D):
                s = fn(r, D)
                if not s:
                    return None
                if D == 1 and s.get('mcq'):
                    q, c, ds, key = s['mcq']
                    try:
                        opts, ans = mcq(r, c, ds)
                    except ValueError:
                        return None
                    return {'stem': s['setup'] + ' ' + q, 'options': opts, 'answer': ans, 'key': key + ' [1]', 'marks': 1}
                want = CTX.get('want_marks') or {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}[D]
                return build(r, s['setup'], s['parts'], want, type_=typ if D < 4 else ('multi_step' if typ == 'numerical' else typ))
            c3f.__name__ = nm_
            t.add('C3', D, typ)(c3f)
        if err:
            def c2f(r, D):
                s = fn(r, max(2, D))
                if not s or not s.get('err'):
                    return None
                claim, why, right, work, noun = s['err']
                who = r.choice(WHO)
                if D <= 2:
                    ask = r.choice([f'Identify the error and state the correct {noun}.', f'State the mistake made and give the correct {noun}.'])
                    key = f'Error: {why} [1]; correct {noun}: {right} [1] [2]'
                    mk = 2
                else:
                    ask = r.choice([f'Explain the error and calculate the correct {noun}, showing your working.',
                                    f'Explain why this is wrong and determine the correct {noun}.'])
                    key = f'Error explained: {why} [1]; working: {work} [1]; correct {noun}: {right} [1] [3]'
                    mk = 3
                return {'stem': f'{s["setup"]} {who} {claim}. {ask}', 'answer': f'{why[0].upper() + why[1:]}. Correct {noun}: {right}.',
                        'key': key, 'marks': mk, 'type': 'explain'}
            c2f.__name__ = nm_ + '_err'
            t.add('C2', (2, 3, 4), 'explain')(c2f)
        if c4:
            def c4f(r, D):
                s = fn(r, min(5, D + 1))
                if not s:
                    return None
                parts = list(s['parts']) + _disc(t, r, s)
                want = CTX.get('want_marks') or {2: 3, 3: 4, 4: 5, 5: 6}[D]
                return build(r, s['setup'], parts, max(want, 3), min_parts=2, type_='multi_step')
            c4f.__name__ = nm_ + '_c4'
            t.add('C4', (2, 3, 4, 5), 'multi_step')(c4f)
        return fn
    return deco


# ===================================================================== 1 The accounting system and double entry
USERS = [
    ('the owner', 'the profit for the year and the value of the business', 'to judge whether the business is worth continuing and how much can be withdrawn as drawings'),
    ('the bank manager', 'liquidity and the ability to repay loans with interest', 'to decide whether to lend or extend an overdraft'),
    ('a trade supplier', 'liquidity (working capital) and the record of paying on time', 'to decide whether to give credit and how much'),
    ('an employee', 'profitability and the stability of the business', 'to judge job security and the chance of pay rises'),
    ('the tax authorities', 'the profit for the year', 'to assess the tax payable'),
    ('a prospective partner', 'profitability, ROCE and the value of net assets', 'to decide whether to invest capital in the business'),
    ('a major customer', 'the long-term survival of the business', 'to be sure of continued supplies and after-sales service'),
]

t1_1 = A(1, 'Purpose of accounting and users of financial information', ['purpose of accounting and users of financial information', 'users of financial information', 'purpose of accounting'],
         mcqs=[('What is the main purpose of accounting?', 'To provide financial information that helps users make economic decisions',
                ['To calculate the tax a business must pay', 'To record only cash transactions', 'To prepare documents for the bank'], 'Accounting records, summarises and communicates financial information for decision making'),
               ('Which user of financial statements is most interested in the short-term liquidity of a business?', 'A trade supplier',
                ['The owner\'s family', 'A potential long-term shareholder', 'The government statistics office'], 'Suppliers want to know if they will be paid within the credit period'),
               ('Which activity is book-keeping rather than accounting?', 'Recording sales invoices in the sales journal',
                ['Interpreting the profit margin', 'Advising the owner on whether to expand', 'Preparing a budget for next year'], 'Book-keeping is the routine recording of transactions; accounting summarises, interprets and communicates'),
               ('Which is an internal user of the financial statements of a sole trader?', 'The owner',
                ['The bank', 'The tax authorities', 'A trade supplier'], 'The owner/manager is inside the business'),
               ('A bank is considering a loan to a business. Which information would it find MOST useful?', 'Profit and cash flow available to cover interest and repayments, and assets available as security',
                ['The names of the business\'s customers', 'The number of employees', 'The owner\'s personal hobbies'], 'Lenders assess ability to pay interest and repay capital')],
         exps=[('Explain the difference between book-keeping and accounting.', 'Book-keeping is the detailed recording of transactions in books of prime entry and ledgers; accounting uses those records to prepare, analyse and interpret financial statements for users.',
                'Book-keeping: recording of transactions [1]; accounting: summarising/interpreting/communicating information [1] [2]'),
               ('Explain why a trade supplier and a bank may be interested in different parts of a business\'s financial statements.', 'A supplier is concerned with short-term liquidity (current assets against current liabilities) because credit is short term; a bank lending long term looks at profitability, gearing and security over several years.',
                'Supplier – short-term liquidity [1]; bank – ability to repay over longer period/security [1]; reason linked to time horizon [1] [3]'),
               ('State two reasons why a sole trader should keep accurate accounting records.', 'To know the profit or loss made and the amounts owed to and by the business; to provide evidence for the tax authorities and for a bank loan application.',
                'Any two reasons, e.g. calculate profit, control receivables/payables, tax, obtain finance, plan [1 each] [2]'),
               ('Explain one limitation of financial statements for a user making decisions about the future.', 'They are based on past (historical) transactions and do not show future performance or non-monetary factors such as staff skills.',
                'Historical / non-monetary information omitted [1]; explanation linked to decision [1] [2]')],
         disc=[('Discuss whether the published profit figure is the most useful information for {who}.', 'Profit shows performance, but {who} may need cash flow, liquidity or security information too; profit can be affected by accounting policies.',
                'Profit useful – performance/ability to pay [1]; other information needed (liquidity, cash, security) [1]; judgement [1] [3]')])


@spec(t1_1, D=(1, 2, 3, 4, 5), typ='short', err=False)
def t11_user(r, D):
    u = r.sample(USERS, 2)
    f = firm(r)
    who = u[0][0]
    setup = r.choice([f'{f} is a sole-trader business. Its financial statements are read by several groups, including {u[0][0]} and {u[1][0]}.',
                      f'The owner of {f} has been asked to send copies of the business\'s latest income statement and statement of financial position to {u[0][0]} and to {u[1][0]}.',
                      f'{pp(r)} owns {f}. Copies of the annual financial statements are given to {u[0][0]} and {u[1][0]}.'])
    parts = [(f'State the information {u[0][0]} would be most interested in and explain why.', f'{cap1(u[0][1])}, {u[0][2]}.', f'Information: {u[0][1]} [1]; reason: {u[0][2]} [1] [2]'),
             (f'Explain why {u[1][0]} would use the financial statements.', f'{cap1(u[1][0])} would use them to look at {u[1][1]}, {u[1][2]}.', f'Information: {u[1][1]} [1]; reason: {u[1][2]} [1] [2]')]
    if D >= 3:
        parts.append((f'Explain why {u[0][0]} and {u[1][0]} might reach different conclusions from the same financial statements.', 'Their decisions differ: one focuses on ' + u[0][1] + ', the other on ' + u[1][1] + ', over different time horizons.',
                      'Different decisions/interests [1]; different time horizon or information focus [1] [2]'))
    return {'setup': setup, 'parts': parts, 'ctx': {'who': who, 'f': f},
            'mcq': (f'Which information would {u[0][0]} find most useful?', cap1(u[0][1]), [cap1(x[1]) for x in USERS if x[1] != u[0][1]][:4], f'{u[0][0]} needs {u[0][1]} {u[0][2]}')}


# accounting equation ------------------------------------------------------------
def _eq_txn(r, kind):
    x = step(r, 500, 9000, 100)
    if kind == 0:
        return f'bought inventory on credit for {m(x)}', (x, x, 0), 'assets (inventory) and liabilities (payables) both increase'
    if kind == 1:
        return f'paid a trade payable {m(x)} by bank transfer', (-x, -x, 0), 'assets (bank) and liabilities (payables) both decrease'
    if kind == 2:
        return f'paid an extra {m(x)} of capital into the business bank account', (x, 0, x), 'assets (bank) and capital both increase'
    if kind == 3:
        return f'withdrew {m(x)} from the business bank account for personal use', (-x, 0, -x), 'assets fall and capital falls (drawings)'
    if kind == 4:
        return f'bought office equipment for {m(x)}, paying by bank transfer', (0, 0, 0), 'one asset (equipment) increases and another (bank) decreases'
    if kind == 5:
        return f'received a bank loan of {m(x)}', (x, x, 0), 'assets (bank) and liabilities (loan) both increase'
    if kind == 6:
        c = step(r, 400, max(500, x - 200), 100)
        if c >= x:
            c = x - 200
        return f'sold goods costing {m(c)} for {m(x)} cash', (x - c, 0, x - c), f'cash up {m(x)}, inventory down {m(c)}; the profit of {m(x - c)} increases capital'
    if kind == 7:
        return f'received {m(x)} from a credit customer', (0, 0, 0), 'one asset (bank) increases and another (receivables) decreases'
    if kind == 8:
        return f'paid rent of {m(x)} from the bank account', (-x, 0, -x), 'assets fall and capital falls because the expense reduces profit'
    return f'repaid {m(x)} of the bank loan', (-x, -x, 0), 'assets (bank) and liabilities (loan) both decrease'


t1_2 = A(1, 'The accounting equation: assets, liabilities and capital', ['the accounting equation: assets, liabilities and capital', 'accounting equation', 'assets liabilities capital'],
         mcqs=[('Which is the accounting equation?', 'Assets = Capital + Liabilities', ['Assets + Liabilities = Capital', 'Capital = Assets + Liabilities', 'Liabilities = Assets + Capital'], 'Resources (assets) are financed by the owner (capital) and outsiders (liabilities)'),
               ('A business has assets of $85,000 and liabilities of $23,000. What is the capital?', '$62,000', ['$108,000', '$23,000', '$85,000'], 'Capital = 85,000 − 23,000'),
               ('Which transaction increases both assets and liabilities?', 'Buying inventory on credit', ['Paying a supplier by cheque', 'The owner withdrawing cash', 'Receiving cash from a credit customer'], 'Inventory (asset) and trade payables (liability) both rise'),
               ('Which transaction leaves total assets unchanged?', 'Buying a computer and paying by bank transfer', ['Paying wages from the bank', 'Taking out a bank loan', 'Buying goods on credit'], 'One asset increases and another decreases by the same amount'),
               ('Which item is a liability?', 'Bank overdraft', ['Trade receivables', 'Inventory', 'Prepaid insurance'], 'An overdraft is an amount owed to the bank'),
               ('The owner takes $500 from the business bank account for personal use. What is the effect?', 'Assets decrease by $500 and capital decreases by $500', ['Assets increase by $500 and capital increases by $500', 'Assets decrease by $500 and liabilities decrease by $500', 'No effect on the accounting equation'], 'Drawings reduce both the bank balance and the owner\'s capital')],
         exps=[('Explain why the accounting equation always balances.', 'Every asset of the business has been financed either by the owner (capital) or by outsiders (liabilities); each transaction has two equal effects, so the equation stays in balance.',
                'Assets financed by capital or liabilities [1]; dual effect of every transaction [1] [2]'),
               ('Explain why profit increases the capital of a sole trader.', 'Profit belongs to the owner; it increases net assets of the business, so the amount the business owes the owner (capital) increases by the same amount.',
                'Profit belongs to owner [1]; net assets and capital rise equally [1] [2]'),
               ('Distinguish between a current liability and a non-current liability, giving an example of each.', 'A current liability is due for payment within 12 months, e.g. trade payables or an overdraft; a non-current liability is due after more than 12 months, e.g. a five-year bank loan.',
                'Current: due within 12 months + example [1]; non-current: due after 12 months + example [1] [2]')],
         disc=[('Explain why the capital figure in the accounting equation does not tell {p} how much the business could be sold for.', 'Capital is a book value based on historical cost; the sale price depends on market values of assets and goodwill.',
                'Book value at historical cost [1]; market value/goodwill differs [1] [2]')])


@spec(t1_2)
def t12_eq(r, D):
    f, p = firm(r), pp(r)
    Aa = step(r, 30000, 150000, 500)
    L = step(r, 5000, int(Aa * 0.5), 500)
    k = {1: 2, 2: 2, 3: 3, 4: 4, 5: 5}[D]
    kinds = r.sample(range(10), k)
    tx = [_eq_txn(r, kd) for kd in kinds]
    dA = sum(t[1][0] for t in tx)
    dL = sum(t[1][1] for t in tx)
    dC = sum(t[1][2] for t in tx)
    A2, L2 = Aa + dA, L + dL
    C1, C2 = Aa - L, A2 - L2
    setup = r.choice([f'On 1 January {p} had business assets of {m(Aa)} and liabilities of {m(L)}. During January the business: {lst([t[0] for t in tx])}.',
                      f'{f}, owned by {p}, started the month with total assets of {m(Aa)} and total liabilities of {m(L)}. The following then took place: {lst([t[0] for t in tx])}.'])
    parts = [('Calculate the owner\'s capital at the start of the month.', m(C1), f'{m(Aa)} − {m(L)} = {m(C1)} [1]'),
             ('Calculate total assets, total liabilities and capital at the end of the month.', f'Assets {m(A2)}; liabilities {m(L2)}; capital {m(C2)}',
              f'Assets {m(Aa)} {"+" if dA >= 0 else "−"} {m(abs(dA))} = {m(A2)} [1]; liabilities {m(L2)} [1]; capital = {m(A2)} − {m(L2)} = {m(C2)} [1] [3]')]
    j = r.randrange(k)
    parts.append((f'State the effect of transaction ({ROM[j]}) on the accounting equation.', cap1(tx[j][2]) + '.', f'{tx[j][2]} [2]'))
    neg = [t for t in tx if t[1][2] < 0]
    if neg and r.random() < 0.6:
        wrong, why = C2 + 2 * sum(-t[1][2] for t in neg), 'the decrease in capital from drawings/expenses was added to capital instead of being deducted'
    else:
        wrong, why = A2 + L2, 'liabilities were added to assets instead of being deducted (capital = assets − liabilities)'
    c, ds = num_opts(m, C2, [A2 + L2, C1, C2 - dC * 2 if dC else C2 + L2 // 2, A2])
    return {'setup': setup, 'parts': parts, 'ctx': {'p': p, 'f': f},
            'mcq': ('What is the owner\'s capital at the end of the month?', c, ds, f'Closing assets {m(A2)} − liabilities {m(L2)} = {m(C2)}'),
            'err': (f'calculated the closing capital as {m(wrong)}', why, m(C2), f'{m(A2)} − {m(L2)}', 'closing capital')}


# double entry -------------------------------------------------------------------
def _de_bank(r):
    c, s = r.sample(PEOPLE, 2)
    g = r.choice(['Apex', 'Delta', 'Summit', 'Coastal', 'Metro', 'Unity'])
    xs = [step(r, 150, 6000, 50) for _ in range(14)]
    out = [
        (f'bought goods for resale on credit from {s}, {m(xs[0])}', 'Purchases', s, 'purchases (expense) increase – debit; amount owed to supplier (liability) increases – credit'),
        (f'sold goods on credit to {c}, {m(xs[1])}', c, 'Sales', 'the customer becomes a receivable (asset) – debit; income from sales – credit'),
        (f'paid wages of {m(xs[2])} by bank transfer', 'Wages', 'Bank', 'expense increases – debit; bank (asset) decreases – credit'),
        (f'received a cheque for {m(xs[3])} from {c}', 'Bank', c, 'bank (asset) increases – debit; receivable decreases – credit'),
        (f'returned goods costing {m(xs[4])} to {s}', s, 'Purchases returns', 'liability to supplier decreases – debit; purchases returns (reduction of expense) – credit'),
        (f'{c} returned goods sold for {m(xs[5])}', 'Sales returns', c, 'sales returns reduce income – debit; receivable decreases – credit'),
        (f'the owner took goods costing {m(xs[6])} for personal use', 'Drawings', 'Purchases', 'drawings reduce capital – debit; goods no longer available for resale reduce purchases – credit'),
        (f'bought a delivery van for {m(xs[7] * 4)} on credit from {g} Motors', 'Motor vehicles', f'{g} Motors', 'non-current asset increases – debit; liability (other payable, not a trade payable) – credit'),
        (f'the owner paid {m(xs[8])} of personal savings into the business bank account', 'Bank', 'Capital', 'bank (asset) increases – debit; capital owed to owner increases – credit'),
        (f'paid rent of {m(xs[9])} in cash', 'Rent', 'Cash', 'expense increases – debit; cash (asset) decreases – credit'),
        (f'received commission of {m(xs[10])} by bank transfer', 'Bank', 'Commission received', 'bank increases – debit; income – credit'),
        (f'withdrew {m(xs[11])} cash from the bank for office use', 'Cash', 'Bank', 'cash increases – debit; bank decreases – credit'),
        (f'paid {s} {m(xs[12])} by cheque', s, 'Bank', 'liability decreases – debit; bank decreases – credit'),
        (f'bought office furniture for {m(xs[13])}, paying by bank transfer', 'Office furniture', 'Bank', 'non-current asset increases – debit; bank decreases – credit'),
    ]
    return out


t1_3 = A(1, 'Double-entry rules: debits and credits in the ledger', ['double-entry rules: debits and credits in the ledger', 'double-entry rules', 'debits and credits'],
         mcqs=[('An increase in an asset is recorded as a', 'debit entry in the asset account', ['credit entry in the asset account', 'debit entry in the capital account', 'credit entry in the bank account only'], 'Assets and expenses increase on the debit side'),
               ('Which pair of accounts both normally have credit balances?', 'Capital and trade payables', ['Drawings and capital', 'Purchases and sales', 'Bank and trade payables'], 'Capital, liabilities and income have credit balances'),
               ('Goods are bought on credit from Kofi. Which entries are made?', 'Debit purchases, credit Kofi', ['Debit Kofi, credit purchases', 'Debit purchases, credit bank', 'Debit inventory, credit sales'], 'Purchases (expense) debited; supplier (liability) credited'),
               ('Which account is debited when the owner withdraws cash for personal use?', 'Drawings', ['Capital', 'Cash', 'Wages'], 'Drawings are debited; cash is credited'),
               ('Which of these has a debit balance?', 'Carriage inwards', ['Discounts received', 'Commission received', 'Purchases returns'], 'Carriage inwards is an expense'),
               ('A credit customer returns goods. Which account is credited?', 'The customer\'s (trade receivable) account', ['Sales returns', 'Sales', 'Purchases returns'], 'Dr sales returns, Cr customer')],
         exps=[('Explain the principle of double entry.', 'Every transaction has two aspects of equal value; one account is debited and another is credited with the same amount, so total debits always equal total credits.',
                'Two aspects/dual effect [1]; equal debit and credit entries [1] [2]'),
               ('Explain why drawings are debited to a drawings account rather than to the capital account directly.', 'A separate drawings account collects all withdrawals during the year so their total is visible; it is transferred to capital at the year end, keeping the capital account uncluttered.',
                'Collects withdrawals in one place/shows total [1]; transferred to capital at year end [1] [2]'),
               ('Explain why expenses and assets are both recorded on the debit side.', 'Both represent uses of the business\'s resources; an expense reduces capital (which has a credit balance), so it is a debit, and an asset is a resource held, also a debit.',
                'Expenses reduce capital – debit [1]; assets are resources owned – debit [1] [2]')],
         disc=[('Explain why a trial balance that agrees does not prove that every transaction has been posted to the correct account.', 'Errors such as commission, principle, omission and complete reversal keep debits equal to credits.',
                'Equal debits and credits still possible [1]; any named example of error not revealed [1] [2]')])


@spec(t1_3)
def t13_de(r, D):
    bank = _de_bank(r)
    k = {1: 2, 2: 2, 3: 3, 4: 4, 5: 5}[D]
    tx = r.sample(bank, k)
    f = firm(r)
    setup = r.choice([f'The following transactions took place at {f} during March: {lst([x[0] for x in tx])}.',
                      f'{pp(r)} owns {f}. In one week the business {"; ".join(x[0] for x in tx[:-1])} and {tx[-1][0]}.',
                      f'Transactions of {f} for the week ending 14 June: {lst([x[0] for x in tx])}.'])
    parts = [('For each transaction, state the account to be debited and the account to be credited.', '; '.join(f'({ROM[i]}) Dr {x[1]}, Cr {x[2]}' for i, x in enumerate(tx)),
              '; '.join(f'({ROM[i]}) Dr {x[1]}, Cr {x[2]} [1]' for i, x in enumerate(tx)) + f' [{k}]')]
    j = r.randrange(k)
    parts.append((f'Explain why transaction ({ROM[j]}) is recorded in this way.', cap1(tx[j][3]) + '.', f'{tx[j][3]} [2]'))
    o = r.choice(bank)
    wrong = [x for x in bank if (x[1], x[2]) != (o[1], o[2])]
    ds = [f'Debit {o[2]}, credit {o[1]}'] + [f'Debit {x[1]}, credit {x[2]}' for x in r.sample(wrong, 3)]
    e = tx[j]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'Which entries record the following: the business {o[0]}?', f'Debit {o[1]}, credit {o[2]}', ds, f'{o[3]}'),
            'err': (f'recorded transaction ({ROM[j]}) by debiting {e[2]} and crediting {e[1]}', f'the entries were reversed (complete reversal); {e[3]}', f'debit {e[1]}, credit {e[2]}', 'correct accounts named on each side', 'double entry')}


# ledger accounts ----------------------------------------------------------------
t1_4 = A(1, 'Recording cash and credit transactions in ledger accounts', ['recording cash and credit transactions in ledger accounts', 'ledger accounts', 'credit transactions'],
         mcqs=[('In which ledger is the personal account of a credit customer kept?', 'Sales ledger', ['Purchases ledger', 'General (nominal) ledger', 'Cash book'], 'Trade receivables\' accounts are in the sales (receivables) ledger'),
               ('A cash sale is recorded by', 'debiting cash and crediting sales', ['debiting sales and crediting cash', 'debiting the customer and crediting sales', 'debiting cash and crediting the customer'], 'No receivable arises for a cash sale'),
               ('On which side of a customer\'s account is a credit sale to that customer entered?', 'Debit', ['Credit', 'Either side', 'Neither – only in the sales account'], 'The customer owes the business: debit'),
               ('Which document is the source for recording a credit purchase?', 'Purchase invoice received from the supplier', ['Receipt issued to a customer', 'Bank statement', 'Credit note sent to a customer'], 'Credit purchases are recorded from suppliers\' invoices'),
               ('A business pays a supplier by bank transfer. Which side of the supplier\'s account is the payment entered on?', 'Debit', ['Credit', 'Both sides', 'It is entered only in the bank account'], 'Payment reduces the liability: debit supplier')],
         exps=[('Explain the difference between a cash transaction and a credit transaction.', 'In a cash transaction payment is made at the time of the sale or purchase; in a credit transaction payment is made later, so a receivable or payable is created.',
                'Cash – immediate payment [1]; credit – payment later, creates receivable/payable [1] [2]'),
               ('Explain why a business keeps a separate ledger account for each credit customer.', 'So that the amount owed by each customer is known, statements can be sent and overdue debts chased.',
                'Know amount owed by each customer [1]; credit control/statements [1] [2]'),
               ('Explain what a debit balance on a supplier\'s account would mean.', 'The business has paid the supplier more than it owes (e.g. overpayment or returns after payment), so the supplier owes the business – it is an asset.',
                'Supplier owes the business/overpayment [1]; treated as an asset/receivable [1] [2]')],
         disc=[('Explain one reason why {f} should check customers\' account balances regularly.', 'To identify overdue debts early, chase payment and reduce the risk of irrecoverable debts; and to set credit limits.',
                'Identify overdue/late payers [1]; consequence – reduce irrecoverable debts/protect cash flow [1] [2]')])


@spec(t1_4)
def t14_ledger(r, D):
    f = firm(r)
    cu = pp(r)
    ob = step(r, 400, 5000, 10)
    s1 = step(r, 800, 6000, 10)
    s2 = step(r, 500, 4000, 10) if D >= 3 else 0
    ret = step(r, 50, min(600, s1 // 3), 10)
    disc = step(r, 10, 120, 5) if D >= 2 else 0
    paid = step(r, 200, ob - disc, 10) if ob - disc > 300 else ob - disc
    cb = ob + s1 + s2 - ret - paid - disc
    if cb <= 0:
        s1 += -cb + 500
        cb = ob + s1 + s2 - ret - paid - disc
    items = [f'1 May balance owed by {cu} {m(ob)}', f'6 May credit sale to {cu} {m(s1)}', f'11 May {cu} returned goods {m(ret)}',
             f'20 May {cu} paid {m(paid)} by bank transfer' + (f' and was allowed {m(disc)} cash discount' if disc else '')]
    if s2:
        items.append(f'28 May credit sale to {cu} {m(s2)}')
    setup = r.choice([f'{f} sells goods on credit. The following relate to the account of {cu} in the sales ledger for May: {lst(items)}.',
                      f'Information about the customer {cu} in the books of {f}: {lst(items)}.'])
    dr = ob + s1 + s2
    parts = [(f'Prepare the account of {cu} for May, balancing it at 31 May.', f'Debit side: balance b/d {m(ob)}, sales {m(s1)}' + (f', sales {m(s2)}' if s2 else '') + f'; credit side: sales returns {m(ret)}, bank {m(paid)}' + (f', discount allowed {m(disc)}' if disc else '') + f', balance c/d {m(cb)}; balance b/d 1 June {m(cb)} (debit)',
              f'Debit entries (b/d, sales) [1]; credit entries (returns, bank' + (', discount' if disc else '') + f') [1]; balance c/d {m(cb)} [1]; b/d on debit side [1] [4]'),
             (f'State what the balance on {cu}\'s account on 1 June represents.', f'{cu} owes {f} {m(cb)}; it is a trade receivable (current asset).', 'Amount owed by customer [1]; trade receivable/current asset [1] [2]')]
    if disc:
        parts.append(('Name the account in the general ledger to which the discount is debited.', 'Discounts allowed account (an expense).', 'Discounts allowed [1]'))
    c, ds = num_opts(m, cb, [cb + 2 * ret, cb + 2 * disc if disc else cb + paid, dr, cb - s2 if s2 else cb + ret])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is the balance on {cu}\'s account at 31 May?', c, ds, f'{m(dr)} − {m(ret)} − {m(paid)}' + (f' − {m(disc)}' if disc else '') + f' = {m(cb)} debit'),
            'err': (f'calculated the balance owed by {cu} at 31 May as {m(cb + 2 * ret)}', 'sales returns were added to the account instead of being credited (deducted)', m(cb),
                    f'{m(dr)} − {m(ret)} − {m(paid)}' + (f' − {m(disc)}' if disc else ''), 'closing balance')}


CHAPTERS[1] = [t1_1, t1_2, t1_3, t1_4]


# ===================================================================== 2 Books of prime entry
t2_1 = A(2, 'Sales and purchases journals and returns journals', ['sales and purchases journals and returns journals', 'sales journal', 'purchases journal', 'returns journals'],
         mcqs=[('What is the source document for an entry in the sales returns journal?', 'A credit note sent to the customer', ['An invoice sent to the customer', 'A credit note received from a supplier', 'A cheque counterfoil'], 'Returns inwards are recorded from copies of credit notes issued'),
               ('Goods with a list price of $2,000 are sold on credit with 20% trade discount. What amount is entered in the sales journal?', '$1,600', ['$2,000', '$400', '$2,400'], 'Trade discount is deducted before recording: 2,000 × 80%'),
               ('The total of the purchases journal is posted to the', 'debit of the purchases account', ['credit of the purchases account', 'debit of each supplier\'s account', 'credit of the bank account'], 'Individual suppliers are credited; the total is debited to purchases'),
               ('Which transaction is recorded in the purchases journal?', 'Goods for resale bought on credit', ['Goods for resale bought for cash', 'A machine bought on credit', 'Goods returned to a supplier'], 'Only credit purchases of goods for resale'),
               ('Why is trade discount not recorded in the ledger accounts?', 'It is a reduction in the list price given before the sale is made, not a separate transaction', ['It is recorded in the cash book instead', 'It is an expense of the seller', 'It is only given to cash customers'], 'Only the net invoice value is recorded')],
         exps=[('Explain the difference between trade discount and cash discount.', 'Trade discount is a reduction in list price given to trade customers, usually for bulk buying, and is not recorded in the accounts; cash discount is an allowance for prompt payment, recorded as discount allowed/received.',
                'Trade discount – reduction in list price, not recorded [1]; cash discount – prompt payment, recorded [1] [2]'),
               ('Explain two advantages of using books of prime entry instead of posting every transaction directly to the ledger.', 'Transactions of the same type are listed together so only totals are posted to the general ledger, reducing work and errors; they provide a chronological record and make it easier to divide the work among staff.',
                'Fewer postings/totals only [1]; reduce errors or division of work or chronological record [1] [2]'),
               ('State the double entry made when the sales returns journal total is posted.', 'Debit the sales returns account with the total; credit each customer\'s account in the sales ledger with the individual amounts.',
                'Dr sales returns (total) [1]; Cr individual customers [1] [2]')],
         disc=[('Explain why trade discount is not recorded in the ledger accounts of {f}.', 'Trade discount is a reduction in the list price given to trade customers before the invoice is issued; it is not a separate transaction, so only the net invoice value is recorded.', 'Reduction from list price at the time of sale [1]; only net invoice value recorded [1] [2]')])


@spec(t2_1)
def t21_journal(r, D):
    f = firm(r)
    sales = r.random() < 0.55
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    names = pp(r, k)
    rows = []
    for n in names:
        lp = step(r, 400, 6000, 100)
        td = r.choice([0, 10, 15, 20, 25]) if D >= 2 else r.choice([10, 20])
        rows.append((n, lp, td, lp * (100 - td) // 100))
    tot = sum(x[3] for x in rows)
    gross = sum(x[1] for x in rows)
    verb = 'sold goods on credit to' if sales else 'bought goods on credit from'
    desc = '; '.join(f'{verb} {n}, list price {m(lp)}' + (f', less {td}% trade discount' if td else ', no trade discount') for n, lp, td, _ in rows)
    jn = 'sales journal' if sales else 'purchases journal'
    setup = r.choice([f'During April {f} {desc}.', f'The following credit transactions of {f} took place in July: {desc}.'])
    if sales:
        post = f'Debit each customer\'s account in the sales ledger (' + ', '.join(f'{n} {m(v)}' for n, _, _, v in rows) + f'); credit sales account with the total {m(tot)}'
    else:
        post = f'Credit each supplier\'s account in the purchases ledger (' + ', '.join(f'{n} {m(v)}' for n, _, _, v in rows) + f'); debit purchases account with the total {m(tot)}'
    parts = [(f'Calculate the amount entered in the {jn} for each transaction and the total of the journal.', '; '.join(f'{n} {m(v)}' for n, _, _, v in rows) + f'; total {m(tot)}',
              '; '.join(f'{n} {m(lp)} × {100 - td}% = {m(v)}' for n, lp, td, v in rows) + f' [{k - 1}]; total {m(tot)} [1] [{k}]'),
             (f'Describe how the {jn} is posted to the ledgers.', post + '.', f'Individual personal accounts [1]; total to {"sales" if sales else "purchases"} account on correct side [1] [2]')]
    if D >= 3:
        n0, _, _, v0 = rows[0]
        rt = step(r, 50, max(60, v0 // 4), 10)
        parts.append((f'Later, goods invoiced at {m(rt)} were returned {"by" if sales else "to"} {n0}. Name the book of prime entry and state the double entry.',
                      f'{"Sales returns journal: Dr sales returns, Cr " + n0 if sales else "Purchases returns journal: Dr " + n0 + ", Cr purchases returns"} {m(rt)}.',
                      f'{"Sales returns (returns inwards)" if sales else "Purchases returns (returns outwards)"} journal [1]; correct double entry {m(rt)} [1] [2]'))
    c, ds = num_opts(m, tot, [gross, gross - tot, tot + rows[0][1] - rows[0][3] if rows[0][2] else tot + 500])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is the total of the {jn} for these transactions?', c, ds, f'Trade discount deducted: {" + ".join(m(x[3]) for x in rows)} = {m(tot)}'),
            'err': (f'entered a total of {m(gross)} in the {jn}', 'the list prices were recorded without deducting trade discount; only the net invoice value is recorded', m(tot), ' + '.join(m(x[3]) for x in rows), 'journal total') if gross != tot else None}


t2_2 = A(2, 'Three-column cash book with discounts', ['three-column cash book with discounts', 'three-column cash book', 'cash book', 'discounts'],
         mcqs=[('In a three-column cash book, the discount column on the debit side records', 'discounts allowed to customers', ['discounts received from suppliers', 'trade discounts given', 'bank charges'], 'Debit side = receipts, so discount allowed to those paying'),
               ('The total of the discount allowed column is posted to the', 'debit of the discount allowed account', ['credit of the discount allowed account', 'debit of the bank account', 'credit of the sales account'], 'Discount allowed is an expense'),
               ('A contra entry in the cash book records', 'cash paid into the bank or cash withdrawn from the bank for office use', ['a cheque received from a customer', 'a payment made to a supplier', 'bank charges'], 'Both sides of the entry are in the cash book'),
               ('A credit balance in the bank column of the cash book means that', 'the business has an overdraft', ['the business has money in the bank', 'the cash book has been wrongly totalled', 'a customer owes money'], 'Payments exceed receipts: amount owed to the bank'),
               ('A customer owing $800 pays by bank transfer and is allowed 2.5% cash discount. How much is entered in the bank column?', '$780', ['$800', '$20', '$820'], '800 − 2.5% × 800 = 780')],
         exps=[('Explain why the discount columns in a three-column cash book are memorandum columns.', 'They are not part of the double entry in the cash book; their totals are posted to the discount allowed and discount received accounts in the general ledger.',
                'Not part of cash/bank double entry [1]; totals posted to discount accounts in general ledger [1] [2]'),
               ('Explain why a business offers cash discount to its credit customers.', 'To encourage customers to pay early, improving cash flow and reducing the risk of irrecoverable debts.', 'Encourage prompt payment [1]; improves liquidity/reduces bad debts [1] [2]'),
               ('Explain why the cash column of a cash book can never have a credit balance.', 'A business cannot pay out more cash than it holds, so total cash payments can never exceed cash receipts plus the opening balance.', 'Cannot spend more cash than held [1]; payments ≤ receipts + balance [1] [2]')],
         disc=[('Evaluate whether {f} should increase the cash discount it offers from 2% to 5%.', 'Higher discount may speed up receipts and cut irrecoverable debts, but it reduces profit on every sale; the cost may exceed the benefit unless liquidity is a serious problem.',
                'Benefit: faster cash/less bad debt [1]; cost: lower profit margin [1]; judgement linked to liquidity/cost of overdraft [1] [3]')])


@spec(t2_2)
def t22_cb(r, D):
    f = firm(r)
    ob = step(r, 500, 9000, 10) * (1 if r.random() < 0.75 or D < 3 else -1)
    c1, c2, s1 = pp(r, 3)
    d1 = r.choice([2, 2.5, 4, 5])
    x1 = step(r, 800, 6000, 40)
    a1 = x1 - x1 * d1 / 100
    x2 = step(r, 500, 4000, 40) if D >= 3 else 0
    a2 = x2 - x2 * d1 / 100
    d2 = r.choice([2, 3, 5])
    y1 = step(r, 600, 5000, 100)
    b1 = y1 - y1 * d2 / 100
    cs = step(r, 200, 3000, 10)
    wages = step(r, 300, 2500, 10)
    rec = [f'{c1} settled a debt of {m(x1)} by bank transfer, less {d1}% cash discount']
    if x2:
        rec.append(f'{c2} paid a balance of {m(x2)} less {d1}% cash discount')
    rec.append(f'cash sales of {m(cs)} were paid directly into the bank')
    pay = [f'{s1} was paid the {m(y1)} owed, less {d2}% cash discount, by bank transfer', f'wages of {m(wages)} were paid from the bank']
    cl = ob + a1 + a2 + cs - b1 - wages
    da = x1 * d1 / 100 + x2 * d1 / 100
    dr = y1 * d2 / 100
    obs = f'a bank balance of {m(ob)}' if ob > 0 else f'a bank overdraft of {m(-ob)}'
    setup = f'On 1 October {f} had {obs}. During October: {lst(rec + pay)}.'
    money = m2 if any(v != int(v) for v in (a1, a2, b1, da, dr)) else m
    parts = [(f'Calculate the amount received from {c1} and the discount allowed.', f'Received {money(a1)}; discount allowed {money(x1 * d1 / 100)}', f'{d1}% × {m(x1)} = {money(x1 * d1 / 100)} [1]; received {money(a1)} [1] [2]'),
             ('Calculate the bank balance at 31 October, stating whether it is a balance or an overdraft.', f'{money(abs(cl))} {"balance (debit)" if cl >= 0 else "overdraft (credit)"}',
              f'{m(ob)} + {money(a1)}' + (f' + {money(a2)}' if x2 else '') + f' + {m(cs)} − {money(b1)} − {m(wages)} [1]; = {money(cl)} [1]; {"debit balance" if cl >= 0 else "overdraft"} [1] [3]'),
             ('State the totals of the discount columns and the accounts to which they are posted.', f'Discount allowed {money(da)} – debit discount allowed account; discount received {money(dr)} – credit discount received account',
              f'Discount allowed {money(da)} Dr discount allowed [1]; discount received {money(dr)} Cr discount received [1] [2]')]
    c, ds = num_opts(money, cl, [cl + da, cl - dr, cl + da - dr, ob + x1 + x2 + cs - y1 - wages + 2 * dr])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the bank balance at 31 October?', c, ds, f'{m(ob)} + {money(a1 + a2 + cs)} − {money(b1 + wages)} = {money(cl)}'),
            'err': (f'calculated the closing bank balance as {money(cl + da - dr)}', 'the discounts were treated as if they were cash received or paid; discount columns are memorandum only – only the net amounts pass through the bank column', money(cl),
                    f'{m(ob)} + {money(a1 + a2 + cs)} − {money(b1 + wages)}', 'bank balance') if abs(da - dr) > 0.5 else None}


t2_3 = A(2, 'Petty cash book and the imprest system', ['petty cash book and the imprest system', 'petty cash book', 'imprest system'],
         mcqs=[('Under the imprest system, the amount given to the petty cashier at the end of each period equals', 'the amount spent during the period', ['the original float', 'the balance remaining', 'a fixed amount decided each period'], 'Reimbursement restores the float'),
               ('Which document supports each payment in the petty cash book?', 'A petty cash voucher', ['A credit note', 'A sales invoice', 'A bank statement'], 'Vouchers are signed and authorised for each payment'),
               ('Which expense would normally be paid out of petty cash?', 'Postage stamps', ['Monthly rent', 'Purchase of a computer', 'Wages of the sales team'], 'Small, regular expenses'),
               ('The imprest is $250 and $187 was spent. How much cash is left in the petty cash box before reimbursement?', '$63', ['$187', '$250', '$437'], '250 − 187'),
               ('The analysis column totals of the petty cash book are posted to the', 'debit side of the relevant expense accounts', ['credit side of the expense accounts', 'debit of the bank account', 'credit of the capital account'], 'Expenses are debited')],
         exps=[('Explain two advantages of the imprest system of petty cash.', 'The cashier can only spend the float, so overspending and fraud are limited and cash can be checked at any time (cash + vouchers = imprest); the main cashier is not troubled with small payments.',
                'Control – cash + vouchers = imprest, limits fraud [1]; saves the main cashier\'s time/delegation [1] [2]'),
               ('Explain why analysis columns are used in a petty cash book.', 'They group payments of the same type so only column totals are posted to each expense account, reducing postings in the general ledger.', 'Group similar expenses [1]; totals posted, fewer entries [1] [2]')],
         disc=[('Explain one control the owner of {f} could use to prevent misuse of petty cash.', 'Spot checks that cash plus vouchers equal the imprest; vouchers signed by an authorising manager; receipts attached.', 'Named control [1]; how it prevents misuse [1] [2]')])


PETTY = ['postage', 'cleaning materials', 'travel expenses', 'stationery', 'refreshments for visitors', 'window cleaning', 'taxi fare', 'printer ink']


@spec(t2_3)
def t23_petty(r, D):
    f = firm(r)
    F = r.choice([100, 150, 200, 250, 300, 400, 500])
    k = 3 if D <= 2 else 5
    its = r.sample(PETTY, k)
    amts = [step(r, 400, int(F * 100 / (k + 1)), 5) / 100 for _ in its]
    spent = round(sum(amts), 2)
    bal = round(F - spent, 2)
    setup = f'{f} keeps a petty cash book on the imprest system with a float of {m(F)}. During the week the petty cashier paid: ' + ', '.join(f'{a} {m2(x)}' for a, x in zip(its, amts)) + '.'
    F2 = F + r.choice([50, 100]) if D >= 4 else F
    parts = [('Calculate the total spent and the balance of petty cash at the end of the week.', f'Spent {m2(spent)}; balance {m2(bal)}', f'Total {m2(spent)} [1]; {m(F)} − {m2(spent)} = {m2(bal)} [1] [2]')]
    if F2 == F:
        parts.append(('State the amount the main cashier must give the petty cashier to restore the imprest.', m2(spent), f'Reimbursement = amount spent {m2(spent)} [1]'))
    else:
        parts.append((f'The owner decides to increase the float to {m(F2)}. Calculate the amount the main cashier must now give the petty cashier.', m2(F2 - bal), f'{m(F2)} − {m2(bal)} = {m2(F2 - bal)} (spent {m2(spent)} + increase {m(F2 - F)}) [2]'))
    parts.append(('State the double entry for the reimbursement.', 'Debit petty cash book (cash), credit bank (cash book).', 'Dr petty cash [1]; Cr bank [1] [2]'))
    c, ds = num_opts(m2, spent, [bal, F, F + spent])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('How much must be reimbursed to restore the imprest?', c, ds, f'Reimburse the amount spent = {m2(spent)}'),
            'err': (f'said the petty cashier should be reimbursed {m2(bal)}', 'the balance in hand was used instead of the amount spent; the imprest is restored by reimbursing what was spent', m2(spent), f'{" + ".join(m2(x) for x in amts)}', 'reimbursement')}


t2_4 = A(2, 'The general journal: opening entries, non-routine items', ['the general journal: opening entries, non-routine items', 'general journal', 'opening entries', 'journal entries'],
         mcqs=[('Which transaction would be recorded in the general journal?', 'The purchase of a machine on credit', ['A credit sale of goods', 'A cash payment of wages', 'A credit purchase of goods for resale'], 'Non-routine items with no other book of prime entry'),
               ('In an opening journal entry, capital is', 'credited with assets less liabilities', ['debited with total assets', 'credited with total assets', 'debited with liabilities'], 'Capital = net assets, a credit balance'),
               ('Why is a narrative written under each journal entry?', 'To explain the reason for the entry', ['To show the balance of the account', 'To record the date of payment', 'Because it replaces the ledger posting'], 'Narratives explain the transaction'),
               ('The owner takes goods costing $350 for personal use. The journal entry is', 'Dr Drawings $350, Cr Purchases $350', ['Dr Purchases $350, Cr Drawings $350', 'Dr Drawings $350, Cr Sales $350', 'Dr Capital $350, Cr Inventory $350'], 'Goods withdrawn reduce purchases'),
               ('Which item is NOT normally recorded in the general journal?', 'Cash received from a customer', ['Writing off an irrecoverable debt', 'Correction of an error', 'Transfer of a balance to the income statement'], 'Cash received is recorded in the cash book')],
         exps=[('Explain why the general journal is used for the purchase of non-current assets on credit.', 'No other book of prime entry deals with it (the purchases journal is only for goods for resale), and the journal provides a record and explanation of an infrequent, high-value transaction.',
                'Not goods for resale – no other book [1]; record/narrative for unusual item [1] [2]'),
               ('State two uses of the general journal.', 'Opening entries; purchase/sale of non-current assets on credit; correction of errors; writing off irrecoverable debts; year-end transfers.', 'Any two [1 each] [2]')],
         disc=[('Explain why {p} should keep a written record (journal) of non-routine transactions.', 'It provides an audit trail and an explanation for unusual entries, reduces errors and helps prevent fraud.', 'Audit trail/explanation [1]; control/fraud prevention [1] [2]')])


@spec(t2_4)
def t24_open(r, D):
    p = pp(r)
    f = firm(r)
    assets = [('Premises', step(r, 60000, 200000, 1000)), ('Equipment', step(r, 5000, 40000, 500)), ('Inventory', step(r, 3000, 20000, 100)),
              ('Trade receivables', step(r, 1000, 12000, 100)), ('Bank', step(r, 500, 8000, 10))]
    liabs = [('Trade payables', step(r, 1000, 9000, 100))]
    if D >= 3:
        liabs.append(('Bank loan (5 years)', step(r, 10000, 50000, 1000)))
        assets.insert(2, ('Motor vehicle', step(r, 6000, 25000, 500)))
    if D <= 2:
        assets = [a for a in assets if a[0] != 'Premises']
    ta, tl = sum(v for _, v in assets), sum(v for _, v in liabs)
    cap = ta - tl
    items = ', '.join(f'{a} {m(v)}' for a, v in assets + liabs)
    setup = r.choice([f'{p} started keeping a full set of double-entry records for {f} on 1 January. At that date the business had: {items}.',
                      f'On 1 July {p} took over the records of {f}. The balances at that date were: {items}.'])
    parts = [('Calculate the capital of the business.', m(cap), f'Assets {m(ta)} − liabilities {m(tl)} [1]; capital {m(cap)} [1] [2]'),
             ('Prepare the opening journal entry (a narrative is required).', 'Dr ' + ', '.join(f'{a} {m(v)}' for a, v in assets) + '; Cr ' + ', '.join(f'{a} {m(v)}' for a, v in liabs) + f', Capital {m(cap)}. Narrative: assets, liabilities and capital at the start of the year.',
              f'All assets debited [1]; liabilities credited [1]; capital credited {m(cap)} [1]; totals {m(ta)} each side and narrative [1] [4]')]
    if D >= 3:
        x = step(r, 2000, 12000, 100)
        g = r.choice(['Apex', 'Delta', 'Summit'])
        parts.append((f'On 5 January the business bought a machine costing {m(x)} on credit from {g} Ltd. Prepare the journal entry.', f'Dr Machinery {m(x)}, Cr {g} Ltd {m(x)}; narrative: purchase of machine on credit.',
                      f'Dr Machinery [1]; Cr {g} Ltd (other payable) [1] [2]'))
    c, ds = num_opts(m, cap, [ta, ta + tl, cap - assets[-1][1]])
    return {'setup': setup, 'parts': parts, 'ctx': {'p': p, 'f': f},
            'mcq': ('What amount is credited to capital in the opening journal entry?', c, ds, f'{m(ta)} − {m(tl)} = {m(cap)}'),
            'err': (f'credited capital with {m(ta)} in the opening journal', 'total assets were used; capital is assets less liabilities, otherwise the journal does not balance', m(cap), f'{m(ta)} − {m(tl)}', 'capital figure')}


JNL = [
    ('the owner took goods costing {x} for personal use', 'Drawings', 'Purchases', 'goods withdrawn reduce purchases and increase drawings'),
    ('a debt of {x} owed by {c} was written off as irrecoverable', 'Irrecoverable debts', '{c}', 'the receivable is removed and the loss is an expense'),
    ('office equipment costing {x} was bought on credit from {s} Ltd', 'Office equipment', '{s} Ltd', 'non-current asset acquired; a non-trade payable created'),
    ('the owner brought a private car valued at {x} into the business', 'Motor vehicles', 'Capital', 'a new asset financed by the owner'),
    ('an old computer with a book value of {x} was sold on credit to {c}', '{c}', 'Disposal of computer (equipment)', 'a receivable replaces the asset'),
    ('the owner paid a business supplier, {s}, {x} from private funds', '{s}', 'Capital', 'the liability falls and the owner has invested extra capital'),
]


@spec(t2_4, D=(2, 3, 4, 5))
def t24_nonroutine(r, D):
    f = firm(r)
    c, s = pp(r, 2)
    k = 2 if D <= 3 else 3
    its = r.sample(JNL, k)
    xs = [step(r, 200, 8000, 50) for _ in its]
    rows = [(d.format(x=m(x), c=c, s=s), dr.format(c=c, s=s), cr.format(c=c, s=s), w, x) for (d, dr, cr, w), x in zip(its, xs)]
    setup = f'The following non-routine transactions of {f} occurred in May: {lst([x[0] for x in rows])}.'
    parts = [('Prepare the journal entries to record these transactions. Narratives are not required.', '; '.join(f'({ROM[i]}) Dr {dr} {m(x)}, Cr {cr} {m(x)}' for i, (_, dr, cr, _, x) in enumerate(rows)),
              '; '.join(f'({ROM[i]}) Dr {dr}, Cr {cr} {m(x)} [2]' for i, (_, dr, cr, _, x) in enumerate(rows)) + f' [{2 * k}]'),
             (f'Explain the reason for entry ({ROM[0]}).', cap1(rows[0][3]) + '.', f'{rows[0][3]} [2]')]
    d0 = rows[0]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'err': (f'recorded transaction ({ROM[0]}) as Dr {d0[2]}, Cr {d0[1]}', f'the debit and credit were reversed; {d0[3]}', f'Dr {d0[1]} {m(d0[4])}, Cr {d0[2]} {m(d0[4])}', 'apply double-entry rules to each account', 'journal entry')}


CHAPTERS[2] = [t2_1, t2_2, t2_3, t2_4]


# ===================================================================== 3 Balancing accounts and the trial balance
t3_1 = A(3, 'Balancing off ledger accounts', ['balancing off ledger accounts', 'balancing off', 'balance c/d'],
         mcqs=[('When an account is balanced, the balance carried down (c/d) is entered on', 'the side with the smaller total, then brought down on the opposite side', ['the side with the larger total', 'the debit side only', 'the credit side only'], 'Balance c/d makes both sides equal; b/d goes to the larger side'),
               ('A trade payable account has credits of $5,400 and debits of $3,900. The balance brought down is', '$1,500 credit', ['$1,500 debit', '$9,300 credit', '$3,900 debit'], 'Credit side larger by 1,500'),
               ('An expense account usually has a balance on the', 'debit side', ['credit side', 'either side', 'neither side because it is closed'], 'Expenses are debits'),
               ('Why are accounts balanced at the end of a period?', 'To find the net amount on each account for the trial balance and financial statements', ['To close every account permanently', 'To correct errors of principle', 'To calculate trade discount'], 'Balances are needed for the TB')],
         exps=[('Explain what a credit balance on the bank account in the ledger means.', 'Payments out have exceeded receipts, so the business owes the bank money – it has an overdraft, a current liability.', 'Payments > receipts [1]; overdraft/current liability [1] [2]'),
               ('Explain why balance c/d and balance b/d are entered on opposite sides of an account.', 'The c/d figure is inserted on the smaller side to make the totals agree; it is then brought down on the other side to show the true balance at the start of the next period.', 'c/d equalises totals [1]; b/d shows opening balance on correct side [1] [2]')],
         disc=[('Explain how balancing the personal accounts of credit customers and suppliers helps {f} control its credit.', 'It shows the amount owed by each customer and to each supplier at a date; customer balances can be compared with credit limits and overdue debts chased, and supplier balances show what must be paid and when.', 'Shows amounts owed at a date [1]; credit limits/chasing debts or planning payments [1] [2]')])


@spec(t3_1)
def t31_bal(r, D):
    f = firm(r)
    kind = r.choice(['bank', 'supplier', 'customer'])
    s = pp(r)
    if kind == 'bank':
        drs = [('Balance b/d', step(r, 500, 6000, 10)), ('Sales', step(r, 1000, 8000, 10)), (r.choice(PEOPLE), step(r, 300, 4000, 10))]
        crs = [('Rent', step(r, 400, 3000, 10)), ('Wages', step(r, 800, 5000, 10)), (s, step(r, 500, 6000, 10))]
        title = 'bank account'
    elif kind == 'supplier':
        drs = [('Bank', step(r, 500, 5000, 10)), ('Purchases returns', step(r, 50, 600, 10))]
        crs = [('Balance b/d', step(r, 600, 4000, 10)), ('Purchases', step(r, 800, 6000, 10)), ('Purchases', step(r, 400, 3000, 10))]
        title = f'account of {s}, a trade payable,'
    else:
        drs = [('Balance b/d', step(r, 600, 4000, 10)), ('Sales', step(r, 800, 6000, 10)), ('Sales', step(r, 400, 3000, 10))]
        crs = [('Bank', step(r, 500, 5000, 10)), ('Sales returns', step(r, 50, 600, 10))]
        title = f'account of {s}, a trade receivable,'
    if D <= 2:
        drs, crs = drs[:2], crs[:2]
    td, tc = sum(v for _, v in drs), sum(v for _, v in crs)
    if td == tc:
        drs.append(('Cash', 120)); td += 120
    bal = td - tc
    side = 'debit' if bal > 0 else 'credit'
    setup = f'The {title} in the books of {f} for June contains — debit entries: ' + ', '.join(f'{a} {m(v)}' for a, v in drs) + '; credit entries: ' + ', '.join(f'{a} {m(v)}' for a, v in crs) + '.'
    meaning = {'bank': 'money in the bank (current asset)' if bal > 0 else 'a bank overdraft (current liability)',
               'supplier': 'an amount owed to the supplier (trade payable)' if bal < 0 else 'an overpayment – the supplier owes the business',
               'customer': 'an amount owed by the customer (trade receivable)' if bal > 0 else 'an overpayment – the business owes the customer'}[kind]
    parts = [('Balance the account at 30 June, showing the balance carried down and brought down.', f'Balance c/d {m(abs(bal))} on the {"credit" if bal > 0 else "debit"} side; totals {m(max(td, tc))}; balance b/d {m(abs(bal))} {side}',
              f'Totals {m(max(td, tc))} [1]; c/d {m(abs(bal))} on smaller side [1]; b/d on {side} side [1] [3]'),
             ('State what the balance brought down represents.', cap1(meaning) + '.', f'{meaning} [1]')]
    c, ds = num_opts(m, abs(bal), [td + tc, td, tc])
    opp = 'credit' if side == 'debit' else 'debit'
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the balance brought down on 1 July?', f'{c} {side}', [f'{c} {opp}'] + [f'{d} {side}' for d in ds[:3]], f'{m(td)} − {m(tc)} = {m(bal)}'),
            'err': (f'brought down the balance of {m(abs(bal))} on the {opp} side', 'the balance b/d must go on the side with the larger total; the c/d figure goes on the smaller side', f'{m(abs(bal))} {side}', f'debits {m(td)} − credits {m(tc)}', 'balance b/d')}


TB_ITEMS = [('Sales', 'Cr', 60000, 200000), ('Purchases', 'Dr', 30000, 120000), ('Sales returns', 'Dr', 500, 3000), ('Purchases returns', 'Cr', 300, 2500),
            ('Wages', 'Dr', 8000, 30000), ('Rent', 'Dr', 3000, 12000), ('Inventory at 1 January', 'Dr', 4000, 15000), ('Trade receivables', 'Dr', 3000, 15000),
            ('Trade payables', 'Cr', 2000, 12000), ('Equipment', 'Dr', 8000, 40000), ('Drawings', 'Dr', 5000, 20000), ('Bank loan', 'Cr', 5000, 30000),
            ('Discounts received', 'Cr', 100, 1200), ('Discounts allowed', 'Dr', 100, 1200), ('Carriage inwards', 'Dr', 200, 1500), ('Commission received', 'Cr', 300, 3000),
            ('Bank overdraft', 'Cr', 500, 5000), ('Motor vehicles', 'Dr', 6000, 30000)]


t3_2 = A(3, 'Preparing a trial balance', ['preparing a trial balance', 'trial balance'],
         mcqs=[('A trial balance is', 'a list of the balances on the ledger accounts at a date, in debit and credit columns', ['a financial statement showing profit', 'an account in the general ledger', 'a statement of the bank balance'], 'It is a list, not an account'),
               ('Which balance appears in the credit column of a trial balance?', 'Discounts received', ['Drawings', 'Carriage outwards', 'Sales returns'], 'Discounts received is income'),
               ('In which column of the trial balance would the bank overdraft appear?', 'Credit', ['Debit', 'Either column', 'It is not included'], 'An overdraft is a liability'),
               ('Which of the following appears in the debit column of a trial balance?', 'Purchases', ['Capital', 'Trade payables', 'Sales'], 'Purchases is an expense'),
               ('The closing inventory is usually NOT included in a trial balance because', 'it is counted after the trial balance is extracted and recorded at the year end', ['it is a liability', 'it is included in purchases', 'it is always zero'], 'Opening inventory is in the TB; closing inventory is a year-end adjustment')],
         exps=[('State two purposes of preparing a trial balance.', 'To check the arithmetical accuracy of the double entry (total debits = total credits); to provide a summary of balances from which financial statements are prepared.', 'Arithmetical check [1]; basis for financial statements [1] [2]'),
               ('Explain why drawings appear in the debit column of a trial balance.', 'Drawings reduce the owner\'s capital (a credit balance), so the drawings account has a debit balance.', 'Reduce capital [1]; therefore debit balance [1] [2]')],
         disc=[('Explain why a trial balance whose totals agree may still contain errors.', 'Some errors (omission, commission, principle, original entry, reversal, compensating) do not affect the equality of debits and credits.', 'Debits still equal credits [1]; named example [1] [2]')])


@spec(t3_2)
def t32_tb(r, D):
    p = pp(r)
    f = firm(r)
    k = {1: 5, 2: 6, 3: 8, 4: 10, 5: 12}[D]
    its = r.sample(TB_ITEMS, k)
    rows = [(n, s, step(r, lo, hi, 100)) for n, s, lo, hi in its]
    dr = sum(v for _, s, v in rows if s == 'Dr')
    cr = sum(v for _, s, v in rows if s == 'Cr')
    if dr <= cr:
        rows.append(('Premises', 'Dr', step(r, cr - dr + 20000, cr - dr + 80000, 1000)))
        dr = sum(v for _, s, v in rows if s == 'Dr')
    cap = dr - cr
    setup = r.choice([f'The following balances were extracted from the books of {p}, owner of {f}, at 31 December: ' + ', '.join(f'{n} {m(v)}' for n, _, v in rows) + '. The capital balance is missing.',
                      f'{f} had the following ledger balances at 31 March: ' + ', '.join(f'{n} {m(v)}' for n, _, v in rows) + '. The owner\'s capital account balance has not been recorded.'])
    parts = [('Prepare the trial balance, inserting capital as the balancing figure.', 'Debit: ' + ', '.join(f'{n}' for n, s, _ in rows if s == 'Dr') + f' = {m(dr)}; Credit: ' + ', '.join(f'{n}' for n, s, _ in rows if s == 'Cr') + f' + Capital {m(cap)} = {m(dr)}',
              f'Debit items correct [1]; credit items correct [1]; capital {m(cap)} [1]; totals {m(dr)} [1] [4]'),
             ('Calculate the capital at that date.', m(cap), f'Debits {m(dr)} − other credits {m(cr)} = {m(cap)} [2]')]
    wrong_item = r.choice([x for x in rows if x[0] in ('Drawings', 'Discounts received', 'Discounts allowed', 'Bank overdraft', 'Sales returns', 'Purchases returns', 'Commission received', 'Carriage inwards', 'Trade payables', 'Bank loan')] or rows)
    n0, s0, v0 = wrong_item
    wcap = cap - 2 * v0 if s0 == 'Dr' else cap + 2 * v0
    c, ds = num_opts(m, cap, [wcap, dr, cap + cr // 2])
    return {'setup': setup, 'parts': parts, 'ctx': {'p': p, 'f': f},
            'mcq': ('What is the capital balance?', c, ds, f'Total debits {m(dr)} − total credits {m(cr)} = {m(cap)}'),
            'err': (f'placed {n0} in the {"credit" if s0 == "Dr" else "debit"} column and so calculated capital as {m(wcap)}', f'{n0} has a {"debit" if s0 == "Dr" else "credit"} balance', m(cap), f'{m(dr)} − {m(cr)}', 'capital') if wcap > 0 else None}


ERRS = [
    ('omission', False, 'A credit sale of {x} to {c} was not recorded at all.', 'Dr {c}, Cr Sales {x}'),
    ('commission', False, 'A payment of {x} received from {c} was credited to the account of {d}.', 'Dr {d}, Cr {c} {x}'),
    ('principle', False, 'The purchase of office furniture for {x} was debited to the purchases account.', 'Dr Office furniture, Cr Purchases {x}'),
    ('original entry', False, 'A purchase invoice for {x} was entered in the purchases journal as {y}.', 'Dr Purchases, Cr supplier {z} (difference)'),
    ('complete reversal', False, 'Cash sales of {x} were debited to the sales account and credited to the cash account.', 'Dr Cash, Cr Sales {x2}'),
    ('compensating', False, 'The sales account was overcast by {x} and the wages account was also overcast by {x}.', 'Dr Sales, Cr Wages {x}'),
    ('single-sided entry', True, 'Rent paid of {x} was entered in the cash book but not posted to the rent account.', 'Dr Rent {x}, Cr Suspense {x}'),
    ('transposition (one side)', True, 'Wages paid of {x} were correctly entered in the cash book but debited to the wages account as {t}.', 'adjust wages and suspense by the difference {tz}'),
    ('casting error', True, 'The sales journal was undercast by {x}.', 'Dr Suspense, Cr Sales {x}'),
    ('two debits', True, 'Discount allowed of {x} was debited to the customer\'s account as well as to the discount allowed account.', 'Dr Suspense, Cr customer {x2}'),
]


def _err_text(r, e):
    c, d = r.sample(PEOPLE, 2)
    x = step(r, 100, 4000, 10)
    s = str(x)
    t = int(s[:-2] + s[-1] + s[-2]) if s[-1] != s[-2] else x + 90
    y = x + r.choice([90, 900, -90]) if x > 900 else x + 90
    return e[2].format(x=m(x), c=c, d=d, y=m(y), t=m(t)), e[3].format(x=m(x), c=c, d=d, z=m(abs(x - y)), x2=m(2 * x), tz=m(abs(t - x)))


t3_3 = A(3, 'Limitations of the trial balance', ['limitations of the trial balance', 'limitations of trial balance'],
         mcqs=[('Which error would NOT be revealed by a trial balance?', 'Goods sold on credit to Ali were debited to Alia\'s account', ['A payment was entered on the debit side of both accounts', 'The sales journal was overcast', 'An expense was posted to only one account'], 'Error of commission – debits still equal credits'),
               ('An error of principle occurs when', 'an entry is made in the wrong class of account', ['a transaction is completely omitted', 'two errors cancel each other out', 'the wrong amount is used in both accounts'], 'e.g. capital expenditure treated as revenue'),
               ('An error of original entry means that', 'the wrong amount was recorded in the book of prime entry, so both ledger entries are wrong by the same amount', ['the entry was made on the wrong side', 'the entry was made in the wrong person\'s account', 'only one side of the entry was made'], 'Both sides use the same wrong figure'),
               ('Which error causes the trial balance totals to disagree?', 'A transposition of figures in one account only', ['An error of complete reversal', 'An error of omission', 'A compensating error'], 'Only one side is affected'),
               ('Which of the following is a compensating error?', 'Two separate errors of the same amount on opposite sides that cancel out', ['An error that is corrected in the next period', 'An entry posted to the wrong side', 'A missing narrative'], 'Compensating errors cancel each other')],
         exps=[('Explain why an error of commission is not revealed by the trial balance.', 'The correct amount is debited and credited, but to the wrong account of the same class, so total debits still equal total credits.', 'Correct amounts on both sides [1]; wrong account of same type, totals unaffected [1] [2]'),
               ('Distinguish between an error of principle and an error of commission.', 'Principle: posted to the wrong class of account (e.g. asset as expense); commission: posted to the wrong account of the correct class (e.g. wrong customer).', 'Principle – wrong class [1]; commission – right class, wrong account [1] [2]'),
               ('State three types of error not revealed by a trial balance.', 'Omission, commission, principle, original entry, complete reversal, compensating errors.', 'Any three [1 each] [3]')],
         disc=[('Discuss how far a trial balance can be relied on as a check on the accuracy of the books of {f}.', 'It proves arithmetic equality of debits and credits and detects one-sided errors, but six types of error leave it balancing, so it is only a partial check.',
                'Detects one-sided/casting errors [1]; misses six types of error [1]; judgement – limited check [1] [3]')])


@spec(t3_3, typ='short')
def t33_lim(r, D):
    f = firm(r)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    es = r.sample(ERRS, k)
    txt = [_err_text(r, e)[0] for e in es]
    setup = f'The bookkeeper of {f} extracted a trial balance. The following errors were later found: {lst(txt)}.'
    parts = [('For each error, state whether it would cause the trial balance totals to disagree.', '; '.join(f'({ROM[i]}) {"yes – totals disagree" if e[1] else "no – totals still agree"}' for i, e in enumerate(es)),
              '; '.join(f'({ROM[i]}) {"disagree" if e[1] else "agree"} [1]' for i, e in enumerate(es)) + f' [{k}]')]
    nr = [(i, e) for i, e in enumerate(es) if not e[1]]
    if nr:
        i, e = nr[0]
        parts.append((f'Name the type of error in ({ROM[i]}).', f'Error of {e[0]}.', f'Error of {e[0]} [1]'))
    parts.append(('Explain why a trial balance cannot be relied upon to detect all errors.', 'Several types of error keep total debits equal to total credits, e.g. omission, commission, principle.', 'Debits = credits still [1]; example [1] [2]'))
    e0 = r.choice([e for e in ERRS if not e[1]])
    t0 = _err_text(r, e0)[0]
    others = [f'Error of {x[0]}' for x in ERRS if not x[1] and x[0] != e0[0]]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'Which type of error is this: "{t0}"', f'Error of {e0[0]}', r.sample(others, 3), f'This is an error of {e0[0]}; the trial balance still agrees'),
            'err': (f'said that error ({ROM[0]}) {"would not" if es[0][1] else "would"} be revealed by the trial balance', f'this is {"a one-sided error – debits no longer equal credits, so it is revealed" if es[0][1] else "an error of " + es[0][0] + " – debits still equal credits, so it is NOT revealed"}',
                    'revealed' if es[0][1] else 'not revealed', 'check whether both debit and credit entries are equal', 'answer')}


CHAPTERS[3] = [t3_1, t3_2, t3_3]


# ===================================================================== 4 Accounting principles and concepts
CONCEPTS = {
    'going concern': 'the business is assumed to continue trading for the foreseeable future, so assets are valued at cost less depreciation, not at break-up value',
    'consistency': 'once a method is chosen it should be used from year to year so that results can be compared',
    'prudence': 'profits and assets should not be overstated and losses and liabilities should not be understated',
    'accruals (matching)': 'income and expenses are recognised in the period in which they are earned or incurred, not when cash is received or paid',
    'business entity': 'the business is treated as separate from its owner; only business transactions are recorded',
    'duality': 'every transaction has two aspects, recorded by a debit and a credit of equal value',
    'money measurement': 'only items that can be measured in money terms are recorded',
    'historical cost': 'assets are recorded at their original cost to the business',
    'materiality': 'items too small to influence users\' decisions need not be treated strictly; they may be expensed',
    'realisation': 'revenue is recognised when goods or services pass to the customer and the customer is liable to pay, not when cash is received',
    'substance over form': 'transactions are recorded according to their economic reality rather than their legal form',
    'relevance': 'information is relevant when it can influence users\' economic decisions (predictive or confirmatory value)',
    'faithful representation': 'information is complete, neutral and free from error so that it represents what it claims to',
    'comparability': 'users can compare information over time and with other businesses',
    'understandability': 'information is presented clearly so that users with reasonable knowledge can understand it',
}

CSCEN = [
    ('going concern', '{f} values its machinery at cost less depreciation of {x} rather than at the {y} it would fetch if sold today.'),
    ('going concern', 'The auditors of {f} were concerned that a major customer owing {x} had collapsed and that the business might have to close; they questioned whether assets should be valued at break-up values.'),
    ('consistency', '{p} has always used the straight-line method to depreciate equipment and does not switch to the reducing-balance method this year, even though it would increase profit by {x}.'),
    ('consistency', '{f} continues to value inventory using FIFO, as in previous years, so that this year\'s gross profit can be compared with last year\'s.'),
    ('prudence', '{f} values its closing inventory at its net realisable value of {x}, which is below its cost of {y}.'),
    ('prudence', '{p} creates an allowance for doubtful debts of {x} because some customers are paying late, but does not record an expected gain of {y} from a lawsuit.'),
    ('accruals (matching)', 'The electricity bill for December of {x} will not be paid until January, but {f} includes it as an expense in the year ended 31 December.'),
    ('accruals (matching)', '{f} paid insurance of {y} on 1 October covering twelve months; only three months\' cost is charged in the year ended 31 December.'),
    ('business entity', '{p} paid {x} for a family holiday from the business bank account; this is recorded as drawings, not as an expense of {f}.'),
    ('business entity', 'The private house and car of {p} are not shown in the statement of financial position of {f}.'),
    ('duality', 'When {f} bought inventory on credit for {x}, the purchases account was debited and the supplier\'s account credited with {x}.'),
    ('money measurement', '{f} has a highly skilled and loyal workforce, but this is not shown as an asset in its statement of financial position.'),
    ('money measurement', 'The excellent reputation of {p} for customer service is not recorded in the accounts of {f}.'),
    ('historical cost', '{f} bought land for {x} ten years ago. Similar land is now worth {y}, but the land is shown at {x}.'),
    ('historical cost', 'A machine bought by {f} for {x} is recorded at {x}, even though the seller\'s list price was higher.'),
    ('materiality', '{f} bought a stapler for {s}; it is charged as office expenses rather than being capitalised and depreciated.'),
    ('materiality', 'A waste bin costing {s} that will last five years is written off as an expense by {f} in the year of purchase.'),
    ('realisation', '{f} delivered goods worth {x} to a customer on 28 December, with payment due in February; the sale is included in December revenue.'),
    ('realisation', 'A customer paid {f} a deposit of {x} in December for goods to be delivered in March; it is not included in December sales.'),
    ('substance over form', '{f} uses a delivery van under a five-year lease and records it as a non-current asset, although it does not legally own the van.'),
    ('substance over form', 'Machinery bought by {f} on hire purchase is shown as an asset even though legal ownership passes only after the final instalment of {x}.'),
    ('relevance', 'The bank asked {f} for the latest monthly figures, because last year\'s statements are now too old to help it decide on a loan of {x}.'),
    ('faithful representation', '{f} includes all liabilities, including a disputed bill of {x}, and presents the figures without bias in favour of the owner.'),
    ('comparability', '{f} shows last year\'s figures alongside this year\'s in its income statement so users can see the change in profit of {x}.'),
    ('understandability', '{f} groups expenses into clear headings and explains unusual items in notes so that a non-accountant can follow its statements.'),
]


def _cs(r, s):
    f, p = firm(r), pp(r)
    x = step(r, 1000, 40000, 100)
    y = x + step(r, 500, 20000, 100)
    return s.format(f=f, p=p, x=m(x), y=m(y), s=m2(step(r, 300, 2500, 5) / 100))


def concept_topic(name, keys, cons, mcqs, exps):
    t = A(4, name, keys, mcqs=mcqs, exps=exps,
          disc=[(lambda r, s: (f'Explain why the owner of {s["ctx"]["f"]} might prefer NOT to apply the {s["ctx"]["c"]} concept, and why it should still be applied.', f'Applying {s["ctx"]["c"]} may reduce reported profit or take extra work, but it gives users reliable, comparable information.',
                                'Owner\'s motive (e.g. higher profit/less work) [1]; benefit to users – reliable/comparable [1]; reference to concept [1] [3]')),
                (lambda r, s: (f'Explain how ignoring the {s["ctx"]["c"]} concept would affect users of the financial statements.', f'The statements would not show a true and fair view: {CONCEPTS[s["ctx"]["c"]]}.', 'Statements misleading [1]; link to concept meaning [1] [2]'))])

    @spec(t, typ='short')
    def concept_app(r, D):
        own = [x for x in CSCEN if x[0] in cons]
        k = 1 if D <= 2 else (2 if D <= 4 else 3)
        pick = r.sample(own, min(k, len(own)))
        if D >= 4:
            pick += r.sample([x for x in CSCEN if x[0] not in cons], 1)
        txt = [_cs(r, s) for _, s in pick]
        f = firm(r)
        setup = f'Read the following situations: {lst(txt)}.' if len(pick) > 1 else txt[0]
        if len(pick) > 1:
            parts = [('Identify the accounting concept applied in each situation.', '; '.join(f'({ROM[i]}) {c}' for i, (c, _) in enumerate(pick)), '; '.join(f'({ROM[i]}) {c} [1]' for i, (c, _) in enumerate(pick)) + f' [{len(pick)}]')]
        else:
            parts = [('Identify the accounting concept applied.', cap1(pick[0][0]) + '.', f'{pick[0][0]} [1]')]
        c0 = pick[0][0]
        parts.append((f'Explain the {c0} concept.', cap1(CONCEPTS[c0]) + '.', f'{CONCEPTS[c0]} [2]'))
        parts.append((f'Explain why it is appropriate to apply this concept in situation {"(i)" if len(pick) > 1 else "described"}.', f'Applying {c0} gives users a true and fair view: {CONCEPTS[c0]}.', 'Applied to the situation [1]; effect on profit/assets or reliability [1] [2]'))
        wrong = r.choice([c for c in CONCEPTS if c != c0 and c not in ('relevance', 'understandability')])
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'c': c0},
                'mcq': ('Which accounting concept is being applied?' if len(pick) == 1 else f'Which accounting concept is applied in situation (i)?', cap1(c0), [cap1(c) for c in r.sample([c for c in CONCEPTS if c != c0], 3)], f'{c0}: {CONCEPTS[c0]}'),
                'err': (f'stated that situation {"(i)" if len(pick) > 1 else "above"} is an example of the {wrong} concept', f'the situation shows {c0}: {CONCEPTS[c0]}; {wrong} means {CONCEPTS[wrong]}', c0, 'match the situation to the definition', 'concept')}
    return t


t4_1 = concept_topic('Going concern, consistency, prudence and accruals (matching)', ['going concern, consistency, prudence and accruals (matching)', 'going concern', 'prudence', 'consistency', 'accruals'],
                     ('going concern', 'consistency', 'prudence', 'accruals (matching)'),
                     [('Inventory is valued at the lower of cost and net realisable value. Which concept is applied?', 'Prudence', ['Consistency', 'Going concern', 'Business entity'], 'Losses are anticipated, gains are not'),
                      ('Which concept requires expenses to be matched with the revenue of the period to which they relate?', 'Accruals', ['Realisation', 'Prudence', 'Materiality'], 'Expenses recognised when incurred'),
                      ('Which concept would be abandoned if a business were about to close down?', 'Going concern', ['Duality', 'Money measurement', 'Business entity'], 'Assets would be valued at break-up value'),
                      ('A business changes its depreciation method every year to show the highest possible profit. Which concept is broken?', 'Consistency', ['Prudence', 'Accruals', 'Historical cost'], 'Methods should be applied consistently'),
                      ('Rent owing at the year end is recorded as an expense of the year. Which concept is applied?', 'Accruals', ['Going concern', 'Consistency', 'Business entity'], 'Expense incurred in the year')],
                     [('Explain the prudence concept, using an example.', 'Profits and assets are not overstated, liabilities and losses not understated, e.g. inventory at lower of cost and NRV, allowance for doubtful debts.', 'Meaning [1]; example [1] [2]'),
                      ('Explain why the consistency concept is important to users of financial statements.', 'If the same methods are used each year, changes in profit reflect real performance rather than changes in accounting policy, so results can be compared over time.', 'Comparison over time [1]; changes reflect performance not method [1] [2]'),
                      ('Explain how the going concern concept affects the valuation of non-current assets.', 'Because the business is expected to continue, assets are valued at cost less depreciation over their useful lives, not at the lower amount they would fetch in a forced sale.', 'Continue trading assumed [1]; cost less depreciation not break-up value [1] [2]')])
t4_2 = concept_topic('Business entity, duality, money measurement, historical cost', ['business entity, duality, money measurement, historical cost', 'business entity', 'money measurement', 'historical cost', 'duality'],
                     ('business entity', 'duality', 'money measurement', 'historical cost'),
                     [('The owner\'s private car is not shown in the business statement of financial position. Which concept is applied?', 'Business entity', ['Money measurement', 'Going concern', 'Prudence'], 'Business and owner are separate'),
                      ('Why are staff skills not shown as an asset?', 'Because of the money measurement concept', ['Because of the prudence concept', 'Because of the duality concept', 'Because of the realisation concept'], 'They cannot be measured reliably in money'),
                      ('Land is shown at the price paid for it many years ago. Which concept is applied?', 'Historical cost', ['Going concern', 'Consistency', 'Materiality'], 'Assets at original cost'),
                      ('Which concept is the basis of double-entry book-keeping?', 'Duality', ['Business entity', 'Accruals', 'Realisation'], 'Two aspects to every transaction'),
                      ('A disadvantage of the historical cost concept is that', 'asset values may be out of date when prices change', ['figures cannot be checked against invoices', 'it is not objective', 'it makes double entry impossible'], 'Historical cost ignores inflation')],
                     [('Explain the business entity concept and why it is applied even to a sole trader.', 'The business is treated as separate from its owner so only business transactions are recorded; this shows the true performance and position of the business, even though the law does not separate a sole trader from the business.', 'Separate from owner [1]; shows business performance even though not legally separate [1] [2]'),
                      ('Explain one advantage and one disadvantage of the historical cost concept.', 'Advantage: objective and verifiable from invoices. Disadvantage: values become out of date in times of inflation, understating assets.', 'Advantage – objective/verifiable [1]; disadvantage – outdated values [1] [2]')])
t4_3 = concept_topic('Materiality, realisation and substance over form', ['materiality, realisation and substance over form', 'materiality', 'realisation', 'substance over form'],
                     ('materiality', 'realisation', 'substance over form'),
                     [('Revenue from a credit sale is recognised when', 'the goods are delivered and the customer accepts liability to pay', ['the customer pays', 'the order is received', 'the goods are manufactured'], 'Realisation concept'),
                      ('A business writes off a $15 calculator as an expense rather than depreciating it. Which concept is applied?', 'Materiality', ['Prudence', 'Historical cost', 'Business entity'], 'The amount is too small to matter'),
                      ('A machine on hire purchase is recorded as a non-current asset before legal ownership passes. Which concept is applied?', 'Substance over form', ['Realisation', 'Historical cost', 'Duality'], 'Economic reality: the business controls and uses it'),
                      ('Whether an item is material depends mainly on', 'its size and nature in relation to the business', ['whether it was paid in cash', 'the date it was bought', 'whether it is an asset or a liability'], 'Materiality is relative'),
                      ('A deposit received for goods not yet delivered should be treated as', 'a liability (deferred income), not revenue', ['revenue of the year', 'capital', 'a reduction in purchases'], 'Revenue is not yet realised')],
                     [('Explain why the same item might be material for one business but not for another.', 'Materiality depends on size relative to the business: $5,000 may affect decisions about a small shop but be insignificant for a large company.', 'Relative size [1]; example [1] [2]'),
                      ('Explain the realisation concept.', 'Revenue is recognised when the goods or services have passed to the customer and the customer has accepted liability to pay, not when the cash is received.', 'Recognised when goods/services transferred [1]; not on receipt of cash [1] [2]')])
t4_4 = concept_topic('Qualitative characteristics: relevance and faithful representation', ['qualitative characteristics: relevance and faithful representation', 'qualitative characteristics', 'relevance', 'faithful representation'],
                     ('relevance', 'faithful representation', 'comparability', 'understandability'),
                     [('Information that is complete, neutral and free from error is said to be', 'a faithful representation', ['relevant', 'material', 'timely'], 'Faithful representation'),
                      ('Information has predictive or confirmatory value. This makes it', 'relevant', ['comparable', 'understandable', 'verifiable'], 'Relevance'),
                      ('Which is a fundamental (rather than enhancing) qualitative characteristic?', 'Relevance', ['Comparability', 'Timeliness', 'Understandability'], 'Fundamental: relevance and faithful representation'),
                      ('Showing last year\'s figures next to this year\'s improves', 'comparability', ['materiality', 'neutrality', 'prudence'], 'Enhancing characteristic'),
                      ('Information provided late to a bank making a lending decision lacks', 'timeliness, which reduces its relevance', ['duality', 'consistency', 'money measurement'], 'Old information cannot influence the decision')],
                     [('Distinguish between relevance and faithful representation.', 'Relevant information is capable of influencing users\' decisions; faithful representation means the information is complete, neutral and free from material error.', 'Relevance – influences decisions [1]; faithful representation – complete, neutral, error-free [1] [2]'),
                      ('Explain why there may be a conflict between relevance and faithful representation.', 'Up-to-date (relevant) information such as current values may need estimates that are less reliable, while verifiable historical cost may be less relevant.', 'Current/estimated values more relevant but less reliable [1]; historical cost reliable but less relevant [1] [2]')])

CHAPTERS[4] = [t4_1, t4_2, t4_3, t4_4]


# ===================================================================== 5 Introduction to financial statements
CAPREV = [
    ('purchase of a new delivery van', 'capital', 'expenditure'), ('cost of installing a new machine', 'capital', 'expenditure'),
    ('legal fees on the purchase of premises', 'capital', 'expenditure'), ('building an extension to the warehouse', 'capital', 'expenditure'),
    ('delivery charge on new office equipment', 'capital', 'expenditure'), ('purchase of a computer system for the office', 'capital', 'expenditure'),
    ('repairs to the delivery van', 'revenue', 'expenditure'), ('fuel for the delivery van', 'revenue', 'expenditure'),
    ('wages of sales staff', 'revenue', 'expenditure'), ('insurance of the premises', 'revenue', 'expenditure'),
    ('redecorating the showroom', 'revenue', 'expenditure'), ('annual servicing of machinery', 'revenue', 'expenditure'),
    ('road tax for the delivery van', 'revenue', 'expenditure'), ('electricity for the shop', 'revenue', 'expenditure'),
]
CAPREC = [('proceeds from the sale of an old machine', 'capital'), ('a five-year bank loan received', 'capital'), ('additional capital paid in by the owner', 'capital'),
          ('cash sales', 'revenue'), ('rent received from sub-letting part of the premises', 'revenue'), ('commission received', 'revenue'), ('discounts received', 'revenue')]

t5_1 = A(5, 'Capital and revenue expenditure and receipts', ['capital and revenue expenditure and receipts', 'capital expenditure', 'revenue expenditure'],
         mcqs=[('Which is capital expenditure?', 'The cost of installing a new machine', ['Repairs to an existing machine', 'Wages of machine operators', 'Electricity used by the machine'], 'Installation is part of the cost of bringing the asset into use'),
               ('Which is a revenue receipt?', 'Rent received from a tenant', ['A bank loan received', 'Proceeds from the sale of a van', 'Capital introduced by the owner'], 'Revenue receipts arise from normal trading activities'),
               ('Revenue expenditure is recorded in', 'the income statement', ['the statement of financial position as a non-current asset', 'the capital account', 'the general journal only'], 'Revenue expenditure is charged against profit'),
               ('If capital expenditure is wrongly treated as revenue expenditure, profit for the year will be', 'understated', ['overstated', 'unaffected', 'overstated and assets overstated'], 'An extra expense is charged'),
               ('Which item is revenue expenditure?', 'Painting the office', ['Building a new office', 'Legal fees on buying premises', 'Buying a delivery van'], 'Maintenance is revenue expenditure')],
         exps=[('Distinguish between capital expenditure and revenue expenditure.', 'Capital expenditure is spending on acquiring or improving non-current assets that benefit several years; revenue expenditure is spending on running the business or maintaining assets, which benefits only the current period.',
                'Capital – acquire/improve NCA, long-term benefit [1]; revenue – running costs/maintenance, current period [1] [2]'),
               ('Explain why it is important to distinguish between capital and revenue expenditure.', 'Misclassification misstates profit and the value of non-current assets: capital expenditure written off understates profit and assets; revenue expenditure capitalised overstates both.',
                'Effect on profit [1]; effect on SFP/assets [1] [2]')],
         disc=[('Discuss why the owner of {f} might be tempted to treat repairs as capital expenditure.', 'It would raise reported profit (e.g. to impress a bank) but breaks the accruals/prudence concepts and overstates assets.', 'Higher profit/assets [1]; misleading – breaks concepts [1]; judgement [1] [3]')])


@spec(t5_1)
def t51_caprev(r, D):
    f = firm(r)
    k = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7}[D]
    its = r.sample([x for x in CAPREV if x[1] == 'capital'], max(1, k // 2)) + r.sample([x for x in CAPREV if x[1] == 'revenue'], k - max(1, k // 2))
    r.shuffle(its)
    vals = [step(r, 300, 20000 if c == 'capital' else 4000, 50) for _, c, _ in its]
    cap = sum(v for v, (_, c, _) in zip(vals, its) if c == 'capital')
    rev = sum(v for v, (_, c, _) in zip(vals, its) if c == 'revenue')
    setup = f'During the year {f} spent the following amounts: ' + ', '.join(f'{d} {m(v)}' for (d, _, _), v in zip(its, vals)) + '.'
    parts = [('Calculate the total capital expenditure and the total revenue expenditure.', f'Capital {m(cap)}; revenue {m(rev)}',
              '; '.join(f'{d}: {c}' for d, c, _ in its) + f' [{k - 1}]; totals capital {m(cap)}, revenue {m(rev)} [1] [{k}]')]
    ci = [(d, v) for (d, c, _), v in zip(its, vals) if c == 'capital'][0]
    parts.append((f'The {ci[0]} was debited to an expense account. State the effect of this error on profit for the year and on non-current assets.', f'Profit understated by {m(ci[1])}; non-current assets understated by {m(ci[1])} (ignoring depreciation).',
                  f'Profit understated {m(ci[1])} [1]; non-current assets understated [1] [2]'))
    if D >= 3:
        rc = r.sample(CAPREC, 2)
        parts.append((f'Classify the following receipts as capital or revenue: {rc[0][0]}; {rc[1][0]}.', f'{cap1(rc[0][0])}: {rc[0][1]}; {rc[1][0]}: {rc[1][1]}.', f'{rc[0][1]} [1]; {rc[1][1]} [1] [2]'))
    ri = [(d, v) for (d, c, _), v in zip(its, vals) if c == 'revenue'][0]
    c, ds = num_opts(m, cap, [cap + ri[1], rev, cap + rev, cap - ci[1] if cap != ci[1] else cap + rev // 2])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the total capital expenditure?', c, ds, f'Capital items: {", ".join(d for d, cc, _ in its if cc == "capital")} = {m(cap)}'),
            'err': (f'included the {ri[0]} ({m(ri[1])}) in capital expenditure, giving {m(cap + ri[1])}', f'the {ri[0]} is revenue expenditure – it maintains or runs the business and benefits only this period', m(cap), ' + '.join(m(v) for v, (_, cc, _) in zip(vals, its) if cc == 'capital'), 'total capital expenditure')}


def _is_data(r, D):
    d = {}
    d['rev'] = step(r, 80000, 300000, 100)
    d['sr'] = step(r, 500, 4000, 10) if D >= 2 else 0
    d['oi'] = step(r, 5000, 25000, 10)
    d['pur'] = step(r, int(d['rev'] * 0.45), int(d['rev'] * 0.6), 10)
    d['pr'] = step(r, 300, 3000, 10) if D >= 3 else 0
    d['ci'] = step(r, 200, 2500, 10) if D >= 3 else 0
    d['ci_'] = step(r, 4000, 30000, 10)
    d['cos'] = d['oi'] + d['pur'] - d['pr'] + d['ci'] - d['ci_']
    d['nr'] = d['rev'] - d['sr']
    d['gp'] = d['nr'] - d['cos']
    ex = [('Wages', step(r, 8000, 40000, 10)), ('Rent and rates', step(r, 3000, 15000, 10)), ('Carriage outwards', step(r, 300, 3000, 10))]
    if D >= 2:
        ex.append(('Discounts allowed', step(r, 100, 1500, 10)))
    if D >= 4:
        ex.append(('General expenses', step(r, 1000, 6000, 10)))
    inc = [('Discounts received', step(r, 100, 1500, 10))] if D >= 3 else []
    if D >= 4:
        inc.append(('Rent received', step(r, 1000, 6000, 10)))
    d['ex'], d['inc'] = ex, inc
    d['np'] = d['gp'] + sum(v for _, v in inc) - sum(v for _, v in ex)
    return d


t5_2 = A(5, 'Income statement: gross profit and profit for the year', ['income statement: gross profit and profit for the year', 'income statement', 'gross profit', 'profit for the year'],
         mcqs=[('Cost of sales is calculated as', 'opening inventory + purchases (net of returns) + carriage inwards − closing inventory', ['opening inventory + purchases − carriage outwards + closing inventory', 'sales − gross profit + expenses', 'purchases − closing inventory − carriage inwards'], 'Carriage inwards is part of the cost of goods'),
               ('Where is carriage outwards shown in the income statement?', 'As an expense deducted from gross profit', ['In the cost of sales', 'Deducted from revenue', 'Added to purchases'], 'Carriage outwards is a selling/distribution expense'),
               ('Revenue $90,000, cost of sales $54,000, expenses $21,000. What is the profit for the year?', '$15,000', ['$36,000', '$69,000', '$33,000'], 'GP 36,000 − 21,000'),
               ('Discount received is shown in the income statement as', 'other income added to gross profit', ['an expense', 'a deduction from purchases in cost of sales', 'part of revenue'], 'Discount received is income'),
               ('Sales returns are', 'deducted from sales to give revenue', ['added to purchases', 'shown as an expense', 'deducted from purchases'], 'Revenue = sales − sales returns')],
         exps=[('Explain the difference between gross profit and profit for the year.', 'Gross profit is revenue less cost of sales (profit on trading); profit for the year is gross profit plus other income less all expenses.', 'GP = revenue − cost of sales [1]; profit for the year after expenses and other income [1] [2]'),
               ('Explain why carriage inwards is included in cost of sales but carriage outwards is not.', 'Carriage inwards is part of the cost of getting goods into the business ready for sale; carriage outwards is a cost of delivering goods to customers, a distribution expense.', 'Inwards – cost of acquiring goods [1]; outwards – selling/distribution expense [1] [2]'),
               ('Explain why closing inventory is deducted in calculating cost of sales.', 'Goods still unsold at the year end have not been sold, so their cost is carried forward to match against next year\'s revenue (accruals concept).', 'Unsold goods not part of cost of sales [1]; matched with later revenue [1] [2]')],
         disc=[('Suggest two ways in which {f} could improve its gross profit next year.', 'Raise selling prices; buy more cheaply (bulk/trade discounts, new supplier); reduce theft and wastage of inventory; change sales mix to higher-margin goods.', 'Any two valid methods [1 each] [2]')])


@spec(t5_2)
def t52_is(r, D):
    f, p = firm(r), pp(r)
    d = _is_data(r, D)
    items = [f'sales {m(d["rev"])}'] + ([f'sales returns {m(d["sr"])}'] if d['sr'] else []) + [f'inventory at 1 January {m(d["oi"])}', f'purchases {m(d["pur"])}'] + \
        ([f'purchases returns {m(d["pr"])}'] if d['pr'] else []) + ([f'carriage inwards {m(d["ci"])}'] if d['ci'] else []) + \
        [f'{n.lower()} {m(v)}' for n, v in d['ex'] + d['inc']]
    setup = r.choice([f'{p} owns {f}. For the year ended 31 December the following figures are available: ' + ', '.join(items) + f'. Inventory at 31 December was valued at {m(d["ci_"])}.',
                      f'The following balances were taken from the books of {f} for the year ended 30 June: ' + ', '.join(items) + f'. Closing inventory was {m(d["ci_"])}.'])
    cosw = f'{m(d["oi"])} + {m(d["pur"])}' + (f' − {m(d["pr"])}' if d['pr'] else '') + (f' + {m(d["ci"])}' if d['ci'] else '') + f' − {m(d["ci_"])} = {m(d["cos"])}'
    parts = [('Calculate the gross profit.', m(d['gp']), (f'Revenue {m(d["rev"])} − {m(d["sr"])} = {m(d["nr"])} [1]; ' if d['sr'] else '') + f'cost of sales {cosw} [1]; gross profit {m(d["gp"])} [1] [{3 if d["sr"] else 2}]'),
             ('Calculate the profit for the year.', m(d['np']), f'{m(d["gp"])}' + ''.join(f' + {m(v)}' for _, v in d['inc']) + ''.join(f' − {m(v)}' for _, v in d['ex']) + f' = {m(d["np"])} [1]; expenses and income correctly treated [1] [2]')]
    if D >= 3:
        parts.append(('Calculate the gross margin, to one decimal place.', pc(d['gp'] / d['nr'] * 100), f'{m(d["gp"])} ÷ {m(d["nr"])} × 100 = {pc(d["gp"] / d["nr"] * 100)} [1]'))
    wrong = d['gp'] + 2 * d['ci'] if d['ci'] else d['gp'] + 2 * d['ci_']
    why = 'carriage inwards was deducted below gross profit instead of in cost of sales' if d['ci'] else 'closing inventory was added to cost of sales instead of being deducted'
    if d['ci']:
        wrong = d['gp'] + d['ci']
    c, ds = num_opts(m, d['gp'], [d['gp'] + 2 * d['ci_'] if not d['ci'] else d['gp'] + d['ci'], d['np'], d['nr'] - d['pur'], d['gp'] + d['sr'] if d['sr'] else d['gp'] - d['oi']])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What is the gross profit?', c, ds, cosw),
            'err': (f'calculated the gross profit as {m(wrong)}', why, m(d['gp']), cosw, 'gross profit')}


SFP_ITEMS = [('Premises', 'NCA'), ('Fixtures and fittings (carrying amount)', 'NCA'), ('Motor vehicles (carrying amount)', 'NCA'), ('Inventory', 'CA'), ('Trade receivables', 'CA'),
             ('Cash in hand', 'CA'), ('Prepaid insurance', 'CA'), ('Trade payables', 'CL'), ('Accrued wages', 'CL'), ('Bank overdraft', 'CL'), ('Bank loan repayable in 2032', 'NCL')]
LIM = {'NCA': (5000, 120000), 'CA': (500, 20000), 'CL': (500, 15000), 'NCL': (10000, 50000)}

t5_3 = A(5, 'Statement of financial position: current and non-current items', ['statement of financial position: current and non-current items', 'statement of financial position', 'current and non-current'],
         mcqs=[('Which is a current asset?', 'Prepaid insurance', ['Delivery van', 'Bank overdraft', 'Accrued rent'], 'Prepayments are amounts paid in advance – current assets'),
               ('A bank loan repayable in six years is shown as', 'a non-current liability', ['a current liability', 'a current asset', 'part of capital'], 'Due after more than 12 months'),
               ('Working capital is', 'current assets minus current liabilities', ['non-current assets minus non-current liabilities', 'capital plus profit', 'total assets minus total liabilities'], 'Also called net current assets'),
               ('Current assets are usually listed in order of', 'increasing liquidity: inventory, receivables, bank, cash', ['size, largest first', 'the date they were acquired', 'alphabetical order'], 'Least liquid first in the IFRS-style format'),
               ('Which item appears in the capital section of a sole trader\'s statement of financial position?', 'Drawings', ['Trade payables', 'Inventory', 'Bank loan'], 'Capital + profit − drawings')],
         exps=[('Distinguish between non-current assets and current assets.', 'Non-current assets are held for use in the business for more than one year (e.g. premises); current assets are held for less than a year and change constantly (e.g. inventory, receivables, cash).', 'NCA – long-term use [1]; CA – short-term, circulating [1] [2]'),
               ('Explain why it is important for a business to have sufficient working capital.', 'To pay its current liabilities as they fall due and to finance day-to-day operations; too little may lead to inability to pay suppliers and loss of credit.', 'Pay short-term debts [1]; consequence of shortage [1] [2]')],
         disc=[('Assess whether {f} has a satisfactory level of working capital.', 'Compare current assets with current liabilities: a ratio around 1.5–2:1 is usually comfortable; too much may mean idle resources, too little risks paying debts.', 'Uses the figures [1]; risk of too little/too much [1]; judgement [1] [3]')])


@spec(t5_3)
def t53_sfp(r, D):
    f, p = firm(r), pp(r)
    k = {1: 5, 2: 6, 3: 8, 4: 9, 5: 11}[D]
    its = [SFP_ITEMS[0], SFP_ITEMS[3], SFP_ITEMS[7]] + r.sample([x for i, x in enumerate(SFP_ITEMS) if i not in (0, 3, 7)], k - 3)
    rows = [(n, c, step(r, *({'Premises': (40000, 150000), 'Cash in hand': (200, 2000), 'Prepaid insurance': (200, 2500), 'Accrued wages': (200, 3000)}.get(n) or LIM[c]), 100)) for n, c in its]
    tot = {c: sum(v for _, cc, v in rows if cc == c) for c in LIM}
    wc = tot['CA'] - tot['CL']
    na = tot['NCA'] + tot['CA'] - tot['CL'] - tot['NCL']
    r.shuffle(rows)
    setup = r.choice([f'The following balances relate to {f} at 31 December: ' + ', '.join(f'{n} {m(v)}' for n, _, v in rows) + '.',
                      f'{p} owns {f}. At the year end the business had: ' + ', '.join(f'{n.lower()} {m(v)}' for n, _, v in rows) + '.'])
    parts = [('Calculate the total of the current assets and the total of the current liabilities.', f'Current assets {m(tot["CA"])}; current liabilities {m(tot["CL"])}',
              f'CA: {", ".join(n for n, c, _ in rows if c == "CA")} = {m(tot["CA"])} [1]; CL: {", ".join(n for n, c, _ in rows if c == "CL")} = {m(tot["CL"])} [1] [2]'),
             ('Calculate the working capital.', m(wc), f'{m(tot["CA"])} − {m(tot["CL"])} = {m(wc)} [1]'),
             ('Calculate the owner\'s capital (net assets) at the year end.', m(na), f'NCA {m(tot["NCA"])} + CA {m(tot["CA"])} − CL {m(tot["CL"])}' + (f' − NCL {m(tot["NCL"])}' if tot['NCL'] else '') + f' = {m(na)} [2]')]
    od = [v for n, c, v in rows if n == 'Bank overdraft']
    wv = wc + 2 * od[0] if od else wc + 2 * tot['CL']
    why = 'the bank overdraft was treated as a current asset; it is a current liability' if od else 'current liabilities were added to current assets instead of being deducted'
    c, ds = num_opts(m, wc, [wv, tot['CA'], tot['CA'] + tot['CL'], na])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What is the working capital?', c, ds, f'{m(tot["CA"])} − {m(tot["CL"])} = {m(wc)}'),
            'err': (f'calculated working capital as {m(wv)}', why, m(wc), f'{m(tot["CA"])} − {m(tot["CL"])}', 'working capital')}


t5_4 = A(5, 'Drawings and the capital account', ['drawings and the capital account', 'drawings', 'capital account'],
         mcqs=[('Goods taken by the owner for personal use are recorded by', 'debiting drawings and crediting purchases', ['debiting purchases and crediting drawings', 'debiting drawings and crediting sales', 'debiting capital and crediting inventory'], 'At cost, reducing purchases'),
               ('Closing capital is', 'opening capital + capital introduced + profit − drawings', ['opening capital + drawings − profit', 'opening capital + profit + drawings', 'total assets + total liabilities'], 'Capital account movements'),
               ('A loss for the year will', 'decrease capital', ['increase capital', 'increase drawings', 'not affect capital'], 'Losses reduce the owner\'s claim'),
               ('Opening capital $40,000, profit $12,000, drawings $9,000. What is closing capital?', '$43,000', ['$61,000', '$37,000', '$31,000'], '40,000 + 12,000 − 9,000'),
               ('The owner pays a private electricity bill from the business bank account. The entry is', 'Dr Drawings, Cr Bank', ['Dr Electricity, Cr Bank', 'Dr Bank, Cr Drawings', 'Dr Capital, Cr Electricity'], 'Business entity concept: private expense = drawings')],
         exps=[('Explain why drawings are not an expense of the business.', 'Drawings are withdrawals of resources by the owner for private use; they do not help to earn revenue, so they reduce capital, not profit.', 'Private use – not to earn revenue [1]; reduce capital not profit [1] [2]'),
               ('Explain why goods taken for own use are credited to purchases rather than sales.', 'The goods are taken at cost and were never sold, so purchases are reduced to show the cost of goods actually available for sale.', 'Not a sale/at cost [1]; reduces cost of goods for resale [1] [2]')],
         disc=[('Discuss whether {p} is withdrawing too much from the business.', 'Compare drawings with profit: drawings above profit reduce capital and the funds available for growth or to repay debts; but some drawings are needed for living costs.', 'Compare with profit [1]; consequence for capital/liquidity [1]; judgement [1] [3]')])


@spec(t5_4)
def t54_cap(r, D):
    f, p = firm(r), pp(r)
    oc = step(r, 20000, 120000, 100)
    ci = step(r, 2000, 15000, 100) if D >= 3 else 0
    prof = step(r, 8000, 45000, 10) * (-1 if D >= 4 and r.random() < 0.25 else 1)
    dc = step(r, 4000, 25000, 10)
    dg = step(r, 200, 2000, 10) if D >= 2 else 0
    cc = oc + ci + prof - dc - dg
    word = 'profit' if prof > 0 else 'loss'
    setup = f'{p}, the owner of {f}, had capital of {m(oc)} on 1 January. During the year' + (f' {p} paid in additional capital of {m(ci)},' if ci else '') + f' withdrew {m(dc)} in cash' + (f' and took goods costing {m(dg)} for personal use' if dg else '') + f'. The business made a {word} of {m(abs(prof))} for the year.'
    parts = [('Prepare the capital account (or calculate the closing capital) at 31 December.', m(cc), f'{m(oc)}' + (f' + {m(ci)}' if ci else '') + f' {"+" if prof > 0 else "−"} {m(abs(prof))} − drawings {m(dc + dg)} [1]; closing capital {m(cc)} [1] [2]')]
    if dg:
        parts.append(('State the double entry for the goods taken for personal use.', f'Dr Drawings {m(dg)}, Cr Purchases {m(dg)}.', 'Dr drawings [1]; Cr purchases [1] [2]'))
    parts.append(('Explain why the drawings are deducted from capital rather than charged as an expense.', 'Drawings are for the owner\'s private use and do not help earn revenue (business entity concept).', 'Private use [1]; business entity [1] [2]'))
    wrong = oc + ci + prof - dc + dg if dg else oc + ci + prof + dc
    c, ds = num_opts(m, cc, [wrong, oc + ci + prof - dc, oc + prof - dc - dg - ci if ci else cc + 2 * dc, oc + ci - prof - dc - dg])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What is the capital at 31 December?', c, ds, f'{m(oc)} + {m(ci)} {"+" if prof > 0 else "−"} {m(abs(prof))} − {m(dc + dg)} = {m(cc)}'),
            'err': (f'calculated closing capital as {m(wrong)}', 'the goods taken for own use were added to capital instead of being treated as drawings' if dg else 'drawings were added to capital instead of being deducted', m(cc),
                    f'{m(oc)} + {m(ci)} {"+" if prof > 0 else "−"} {m(abs(prof))} − {m(dc + dg)}', 'closing capital')}


CHAPTERS[5] = [t5_1, t5_2, t5_3, t5_4]


# ===================================================================== 6 Accruals and prepayments
EXPS = ['rent', 'insurance', 'electricity', 'business rates', 'telephone', 'wages', 'heating and lighting']


def _exp_case(r, D):
    nm_ = r.choice(EXPS)
    paid = step(r, 3000, 30000, 10)
    o_acc = o_pre = c_acc = c_pre = 0
    kinds = r.sample(['oa', 'op', 'ca', 'cp'], 1 if D <= 2 else 2)
    if 'oa' in kinds:
        o_acc = step(r, 200, 2500, 10)
    if 'op' in kinds and not o_acc:
        o_pre = step(r, 200, 2500, 10)
    if 'ca' in kinds:
        c_acc = step(r, 200, 2500, 10)
    if 'cp' in kinds and not c_acc:
        c_pre = step(r, 200, 2500, 10)
    if not (o_acc or o_pre or c_acc or c_pre):
        c_acc = step(r, 200, 2500, 10)
    charge = paid - o_acc + c_acc + o_pre - c_pre
    return nm_, paid, o_acc, o_pre, c_acc, c_pre, charge


def _bal_txt(o_acc, o_pre, c_acc, c_pre, s='1 January', e='31 December'):
    b = []
    if o_acc:
        b.append(f'{m(o_acc)} was owing at {s}')
    if o_pre:
        b.append(f'{m(o_pre)} had been paid in advance at {s}')
    if c_acc:
        b.append(f'{m(c_acc)} was owing at {e}')
    if c_pre:
        b.append(f'{m(c_pre)} had been paid in advance for next year at {e}')
    return '; '.join(b)


t6_1 = A(6, 'Accrued and prepaid expenses in ledger accounts', ['accrued and prepaid expenses in ledger accounts', 'accrued expenses', 'prepaid expenses', 'accruals', 'prepayments'],
         mcqs=[('An accrued expense is', 'an expense incurred in the period but not yet paid', ['an expense paid in advance', 'income received in advance', 'an expense of a future period'], 'Accruals concept'),
               ('A prepaid expense is shown in the statement of financial position as', 'a current asset', ['a current liability', 'a non-current asset', 'a deduction from capital'], 'The business is owed the benefit'),
               ('Rent paid during the year $9,600; rent owing at the year end $800. The income statement charge is', '$10,400', ['$8,800', '$9,600', '$800'], '9,600 + 800'),
               ('In the expense account, an accrual at the year end is shown as a balance carried down on the', 'debit side, brought down as a credit balance', ['credit side, brought down as a debit balance', 'debit side only', 'credit side only'], 'Accrual c/d on debit side; b/d credit = liability'),
               ('Insurance of $2,400 for the year to 31 March 2026 was paid on 1 April 2025. For the year ended 31 December 2025, the prepayment is', '$600', ['$1,800', '$2,400', '$200'], '3 months unexpired: 2,400 × 3/12')],
         exps=[('Explain why an accrued expense is added to the amount paid when calculating the income statement charge.', 'The expense has been incurred in the year even though it is unpaid; the accruals concept requires all expenses incurred in the period to be matched against its revenue.', 'Incurred in period [1]; accruals/matching concept [1] [2]'),
               ('Explain the effect on profit and on the statement of financial position of failing to record a prepaid expense.', 'Expenses are overstated, so profit is understated; current assets are understated by the amount of the prepayment.', 'Profit understated [1]; current assets understated [1] [2]')],
         disc=[('Explain which accounting concept requires {f} to make this adjustment and why it matters to users.', 'The accruals (matching) concept: expenses incurred in the period are matched with that period\'s revenue, so profit is not distorted by the timing of payments.', 'Accruals concept named [1]; profit not distorted by payment timing [1] [2]')])


@spec(t6_1)
def t61_exp(r, D):
    f = firm(r)
    if D >= 4 and r.random() < 0.5:
        nm_ = r.choice(['insurance', 'rent', 'business rates'])
        mo = r.choice([3, 4, 6, 9])
        annual = step(r, 1200, 24000, 120)
        prior = annual * r.choice([1, 0.9]) // 12 * 12
        prior = int(prior)
        start = ['1 October', '1 September', '1 July', '1 April'][[3, 4, 6, 9].index(mo)]
        pre_months = 12 - mo
        cp = annual * pre_months // 12
        op = prior * (12 - mo) // 12
        charge = op + annual - cp
        setup = (f'{f} pays {nm_} annually in advance on {start}. On {start} last year it paid {m(prior)} for twelve months, and on {start} this year it paid {m(annual)} for the next twelve months. '
                 f'The financial year ends on 31 December.')
        parts = [(f'Calculate the {nm_} prepaid at 31 December.', m(cp), f'{pre_months}/12 × {m(annual)} = {m(cp)} [2]'),
                 (f'Calculate the {nm_} expense for the year ended 31 December.', m(charge), f'Prepaid b/d {m(op)} + paid {m(annual)} − prepaid c/d {m(cp)} = {m(charge)} [2]'),
                 ('State how the year-end balance is shown in the statement of financial position.', f'Prepayment {m(cp)} as a current asset (other receivables).', 'Current asset [1]')]
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
                'mcq': None,
                'err': (f'charged {m(annual)} as the {nm_} expense for the year', 'the amount paid was used; the part relating to next year must be carried forward as a prepayment and last year\'s prepayment brought in', m(charge), f'{m(op)} + {m(annual)} − {m(cp)}', f'{nm_} expense')}
    nm_, paid, oa, op, ca, cp, ch = _exp_case(r, D)
    setup = r.choice([f'{f} paid {m(paid)} for {nm_} during the year ended 31 December. {cap1(_bal_txt(oa, op, ca, cp))}.',
                      f'During the year ended 31 December, payments for {nm_} by {f} totalled {m(paid)}. You are told that {_bal_txt(oa, op, ca, cp)}.'])
    w = f'Paid {m(paid)}' + (f' − opening accrual {m(oa)}' if oa else '') + (f' + opening prepayment {m(op)}' if op else '') + (f' + closing accrual {m(ca)}' if ca else '') + (f' − closing prepayment {m(cp)}' if cp else '') + f' = {m(ch)}'
    parts = [(f'Calculate the amount for {nm_} to be charged in the income statement for the year.', m(ch), f'{w} [1 per adjustment]; answer {m(ch)} [1] [{1 + bool(oa or op) + bool(ca or cp)}]')]
    if ca or cp:
        parts.append(('State how the closing balance is shown in the statement of financial position.', f'{"Accrued expense " + m(ca) + " under current liabilities" if ca else "Prepayment " + m(cp) + " under current assets"}.', f'{"Current liability" if ca else "Current asset"} [1]'))
    if D >= 3:
        parts.append((f'Prepare the {nm_} account for the year, showing the transfer to the income statement and the balances.', w.replace(' = ', '; transfer to income statement '), f'Balances b/d and c/d on correct sides [1]; bank {m(paid)} [1]; transfer to IS {m(ch)} [1] [3]'))
    wrong = paid + oa - ca - op + cp
    c, ds = num_opts(m, ch, [paid, wrong, paid + oa + ca + op + cp])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is the {nm_} expense for the year?', c, ds, w),
            'err': (f'calculated the {nm_} expense as {m(wrong)}', 'the adjustments were made the wrong way round: closing accruals are added, closing prepayments deducted, opening accruals deducted and opening prepayments added', m(ch), w.split(' = ')[0], f'{nm_} expense') if wrong != ch else None}


t6_2 = A(6, 'Accrued and prepaid income', ['accrued and prepaid income', 'accrued income', 'income received in advance'],
         mcqs=[('Rent receivable owing to the business at the year end is shown as', 'a current asset', ['a current liability', 'a deduction from rent receivable', 'a non-current asset'], 'Accrued income is a receivable'),
               ('Commission received in advance at the year end is', 'a current liability', ['a current asset', 'income of the year', 'part of capital'], 'The business owes the service'),
               ('Rent received in the year $6,000; $500 was owed by the tenant at the year end. The income for the year is', '$6,500', ['$5,500', '$6,000', '$500'], 'Earned = received + accrued'),
               ('Income received in advance at the start of the year is', 'added to the amount received to find this year\'s income', ['deducted from the amount received', 'ignored', 'shown as an expense'], 'It was earned this year'),
               ('Which of these is accrued income?', 'Interest earned on a deposit but not yet received', ['Rent paid in advance', 'Wages owing', 'A customer\'s deposit for future goods'], 'Earned but not received')],
         exps=[('Explain the difference between accrued income and income received in advance.', 'Accrued income is earned in the period but not yet received (a current asset); income received in advance is received but relates to a later period (a current liability).', 'Accrued – earned not received, asset [1]; in advance – received not earned, liability [1] [2]'),
               ('Explain why income received in advance is treated as a liability.', 'The business still owes the goods or service to the payer; until it is earned it is an obligation, and it will become income in the next period.', 'Obligation to provide service [1]; becomes income later [1] [2]')],
         disc=[('Explain why {f} should not include all cash received from its tenant as income of the year.', 'The realisation and accruals concepts require income to be recognised when earned, not when cash is received.', 'Concept named [1]; earned vs received [1] [2]')])


@spec(t6_2)
def t62_inc(r, D):
    f = firm(r)
    nm_ = r.choice(['rent receivable', 'commission receivable', 'interest receivable'])
    rec = step(r, 2000, 20000, 10)
    oa = step(r, 200, 2000, 10) if r.random() < 0.5 else 0
    oadv = 0 if oa else step(r, 200, 2000, 10)
    ca = step(r, 200, 2000, 10) if r.random() < 0.5 else 0
    cadv = 0 if ca else step(r, 200, 2000, 10)
    if D <= 2:
        oa = oadv = 0
    inc = rec - oa + ca + oadv - cadv
    b = []
    if oa:
        b.append(f'{m(oa)} was owed to the business at 1 January')
    if oadv:
        b.append(f'{m(oadv)} had been received in advance at 1 January')
    b.append(f'{m(ca)} was owed to the business at 31 December' if ca else f'{m(cadv)} had been received in advance for next year at 31 December')
    setup = f'{f} received {m(rec)} of {nm_} during the year ended 31 December. ' + cap1('; '.join(b)) + '.'
    w = f'Received {m(rec)}' + (f' − {m(oa)}' if oa else '') + (f' + {m(oadv)}' if oadv else '') + (f' + {m(ca)}' if ca else f' − {m(cadv)}') + f' = {m(inc)}'
    parts = [(f'Calculate the {nm_} to be credited to the income statement.', m(inc), f'{w} [2]'),
             ('State how the balance at 31 December appears in the statement of financial position.', f'{"Accrued income " + m(ca) + " – current asset" if ca else "Income received in advance " + m(cadv) + " – current liability"}.', f'{"Current asset" if ca else "Current liability"} [1]')]
    if D >= 3:
        parts.append((f'Prepare the {nm_} account for the year.', w, f'Opening balance on correct side [1]; bank {m(rec)} [1]; transfer to IS {m(inc)} [1]; closing balance c/d [1] [4]'))
    wrong = rec + (oa if oa else -oadv) - (ca if ca else -cadv)
    c, ds = num_opts(m, inc, [rec, wrong, rec + ca + cadv])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What amount of {nm_} is credited to the income statement?', c, ds, w),
            'err': (f'credited {m(wrong)} to the income statement', 'the adjustments were reversed: income owed at the year end is added and income received in advance at the year end is deducted', m(inc), w.split(' = ')[0], 'income figure') if wrong != inc else None}


ADJ = [('accrued expense', 'wages owing of {x} had not been recorded', -1, 'CL'), ('prepaid expense', 'insurance of {x} paid in advance had been charged in full as an expense', 1, 'CA'),
       ('accrued income', 'rent receivable of {x} due from a tenant had not been recorded', 1, 'CA'), ('income in advance', 'commission of {x} received for next year had been included in income', -1, 'CL')]

t6_3 = A(6, 'Adjusting the financial statements for accruals and prepayments', ['adjusting the financial statements for accruals and prepayments', 'adjusting the financial statements', 'year-end adjustments'],
         mcqs=[('Failing to record an accrued expense will', 'overstate profit and understate current liabilities', ['understate profit and overstate current assets', 'overstate profit and overstate current assets', 'have no effect on profit'], 'Expense missing'),
               ('Draft profit $24,000. A prepayment of $1,000 was omitted. The corrected profit is', '$25,000', ['$23,000', '$24,000', '$26,000'], 'Expense reduced'),
               ('Accrued income is shown in the statement of financial position under', 'current assets', ['current liabilities', 'non-current liabilities', 'capital'], 'Amount receivable'),
               ('Which adjustment reduces profit?', 'Recording income received in advance', ['Recording a prepaid expense', 'Recording accrued income', 'Reducing an accrued expense'], 'Income is reduced'),
               ('Accruals and prepayments are necessary because of the', 'accruals (matching) concept', ['money measurement concept', 'business entity concept', 'historical cost concept'], 'Match income and expenses with the period')],
         exps=[('Explain how recording accrued income affects the financial statements.', 'Income in the income statement increases, so profit increases; current assets increase by the same amount.', 'Profit up [1]; current assets up [1] [2]'),
               ('Explain why the adjustments for accruals and prepayments do not affect the bank balance.', 'They are book entries that recognise income and expenses in the correct period; no cash is received or paid when the adjustments are made.', 'Non-cash adjustments [1]; timing/period recognition [1] [2]')],
         disc=[('Discuss why the owner of {f} should not ignore small accruals and prepayments.', 'Individually small items may be immaterial, but together they can distort profit and working capital; consistency and the accruals concept require them.', 'Materiality point [1]; cumulative distortion [1]; judgement [1] [3]')])


@spec(t6_3)
def t63_adj(r, D):
    f, p = firm(r), pp(r)
    dp_ = step(r, 15000, 70000, 10)
    k = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}[D]
    its = r.sample(ADJ, k)
    xs = [step(r, 200, 3000, 10) for _ in its]
    cp_ = dp_ + sum(s * x for (_, _, s, _), x in zip(its, xs))
    ca = sum(x for (_, _, _, c), x in zip(its, xs) if c == 'CA')
    cl = sum(x for (_, _, _, c), x in zip(its, xs) if c == 'CL')
    setup = f'{p} calculated a draft profit of {m(dp_)} for {f} for the year ended 31 December. It was then found that: {lst([d.format(x=m(x)) for (_, d, _, _), x in zip(its, xs)])}.'
    parts = [('Calculate the corrected profit for the year.', m(cp_), f'{m(dp_)}' + ''.join(f' {"+" if s > 0 else "−"} {m(x)} ({n})' for (n, _, s, _), x in zip(its, xs)) + f' [1 per item]; corrected profit {m(cp_)} [1] [{k + 1}]'),
             ('State the effect of the adjustments on current assets and on current liabilities.', f'Current assets increase by {m(ca)}; current liabilities increase by {m(cl)}.', f'CA +{m(ca)} [1]; CL +{m(cl)} [1] [2]')]
    wrong = dp_ - sum(s * x for (_, _, s, _), x in zip(its, xs))
    c, ds = num_opts(m, cp_, [wrong, dp_, dp_ + sum(xs)])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What is the corrected profit?', c, ds, f'{m(dp_)} adjusted = {m(cp_)}'),
            'err': (f'calculated the corrected profit as {m(wrong)}', 'each adjustment was applied in the wrong direction: unrecorded expenses and income received in advance reduce profit; prepaid expenses and accrued income increase it', m(cp_),
                    f'{m(dp_)}' + ''.join(f' {"+" if s > 0 else "−"} {m(x)}' for (_, _, s, _), x in zip(its, xs)), 'profit') if wrong != cp_ else None}


CHAPTERS[6] = [t6_1, t6_2, t6_3]


# ===================================================================== 7 Irrecoverable debts and allowance for doubtful debts
t7_1 = A(7, 'Writing off irrecoverable debts and recoveries', ['writing off irrecoverable debts and recoveries', 'irrecoverable debts', 'recoveries'],
         mcqs=[('An irrecoverable debt is written off by', 'debiting irrecoverable debts and crediting the customer\'s account', ['debiting the customer and crediting irrecoverable debts', 'debiting sales and crediting the customer', 'debiting irrecoverable debts and crediting bank'], 'The receivable is removed and the expense recorded'),
               ('A debt of $400 written off last year is recovered in full. The first entry is', 'Dr customer, Cr irrecoverable debts recovered $400', ['Dr bank, Cr sales $400', 'Dr irrecoverable debts, Cr customer $400', 'Dr bank, Cr capital $400'], 'Reinstate the debt first, then record the cash'),
               ('Why is a debt reinstated in the customer\'s account before the cash is recorded on recovery?', 'So the customer\'s account shows a full record of the debt and its payment, useful for future credit decisions', ['To increase sales', 'Because the trial balance requires it', 'To reduce the allowance for doubtful debts'], 'Complete credit history'),
               ('Writing off an irrecoverable debt reduces', 'profit and trade receivables', ['profit and trade payables', 'sales and bank', 'capital and bank'], 'Expense and asset reduction'),
               ('Irrecoverable debts recovered is shown in the income statement as', 'other income', ['an expense', 'part of revenue', 'a deduction from purchases'], 'Recovery is a gain')],
         exps=[('Explain why irrecoverable debts are written off rather than left in trade receivables.', 'The amount will never be received, so leaving it would overstate assets and profit; the prudence concept requires the loss to be recognised.', 'Will not be received – overstates assets [1]; prudence [1] [2]'),
               ('State two reasons why a debt may become irrecoverable.', 'The customer has become bankrupt or gone into liquidation; the customer has disappeared or disputes the debt and legal action is not worthwhile.', 'Any two [1 each] [2]')],
         disc=[('Suggest two ways in which {f} could reduce its irrecoverable debts in future.', 'Credit checks/references before giving credit; set credit limits; offer cash discounts for prompt payment; chase overdue accounts promptly.', 'Two valid methods [1 each] [2]')])


@spec(t7_1)
def t71_wo(r, D):
    f = firm(r)
    a, b = pp(r, 2)
    x1 = step(r, 200, 3000, 10)
    x2 = step(r, 200, 2500, 10) if D >= 3 else 0
    rec = step(r, 100, 1500, 10) if D >= 2 else 0
    dp_ = step(r, 20000, 60000, 10)
    setup = f'{f} prepared draft profit of {m(dp_)}. Before finalising the accounts: {a} has been declared bankrupt owing {m(x1)}' + (f'; {b}, who owes {m(x2)}, has left the country and cannot be traced' if x2 else '') + \
        (f'; and a debt of {m(rec)} written off two years ago was unexpectedly received in full by bank transfer' if rec else '') + '. These items have not been recorded.'
    cp_ = dp_ - x1 - x2 + rec
    parts = [('Calculate the corrected profit for the year.', m(cp_), f'{m(dp_)} − {m(x1 + x2)} irrecoverable debts' + (f' + {m(rec)} recovered' if rec else '') + f' = {m(cp_)} [2]'),
             (f'State the journal entry to write off the debt of {a}.', f'Dr Irrecoverable debts {m(x1)}, Cr {a} {m(x1)}.', 'Dr irrecoverable debts [1]; Cr customer [1] [2]')]
    if rec:
        parts.append(('State the entries needed to record the recovered debt.', f'Dr customer, Cr irrecoverable debts recovered {m(rec)}; then Dr bank, Cr customer {m(rec)}.', 'Reinstate debt [1]; record receipt [1] [2]'))
    wrong = dp_ - x1 - x2 - rec
    c, ds = num_opts(m, cp_, [wrong, dp_ - x1, dp_ + x1 + x2])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the corrected profit?', c, ds, f'{m(dp_)} − {m(x1 + x2)} + {m(rec)} = {m(cp_)}'),
            'err': (f'calculated the corrected profit as {m(wrong)}', 'the recovered debt was treated as a further loss; a recovery is income and increases profit', m(cp_), f'{m(dp_)} − {m(x1 + x2)} + {m(rec)}', 'profit') if rec else None}


def _allow(r, D):
    tr = step(r, 20000, 90000, 100)
    wo = step(r, 300, 3000, 100) if D >= 2 else 0
    pct_ = r.choice([2, 2.5, 3, 4, 5])
    old = step(r, 300, 3000, 10)
    new = (tr - wo) * pct_ / 100
    if abs(new - old) < 1:
        old += 150
    return tr, wo, pct_, old, new


t7_2 = A(7, 'Creating and adjusting an allowance for doubtful debts', ['creating and adjusting an allowance for doubtful debts', 'allowance for doubtful debts', 'doubtful debts'],
         mcqs=[('An increase in the allowance for doubtful debts is', 'debited to the income statement as an expense', ['credited to the income statement', 'added to trade receivables', 'debited to the allowance account'], 'Only the change is charged'),
               ('Trade receivables $40,000; allowance to be 5%; existing allowance $1,500. The income statement charge is', '$500', ['$2,000', '$1,500', '$3,500'], '2,000 − 1,500'),
               ('Which concept justifies creating an allowance for doubtful debts?', 'Prudence', ['Business entity', 'Money measurement', 'Duality'], 'Anticipate likely losses'),
               ('A decrease in the allowance for doubtful debts will', 'increase profit', ['reduce profit', 'reduce trade receivables', 'increase irrecoverable debts'], 'Credited to the income statement'),
               ('The allowance for doubtful debts account normally has', 'a credit balance', ['a debit balance', 'no balance', 'a balance that equals trade receivables'], 'It reduces an asset')],
         exps=[('Distinguish between an irrecoverable debt and a doubtful debt.', 'An irrecoverable debt is known to be uncollectable and is written off; a doubtful debt may not be collected, so an allowance is made but the debt stays in the receivables ledger.', 'Irrecoverable – certain, written off [1]; doubtful – uncertain, allowance only [1] [2]'),
               ('Explain why only the change in the allowance is recorded in the income statement each year.', 'The existing allowance was charged in earlier years; charging the full amount again would double-count the expense.', 'Earlier allowance already charged [1]; avoid double counting [1] [2]')],
         disc=[('Evaluate whether {f} should base its allowance on a fixed percentage of receivables or on an aged analysis.', 'A fixed percentage is simple and consistent; an aged analysis reflects the higher risk of older debts and is more accurate, but takes more work.', 'Fixed % – simple [1]; aged – more accurate [1]; judgement [1] [3]')])


@spec(t7_2)
def t72_allow(r, D):
    f = firm(r)
    tr, wo, pct_, old, new = _allow(r, D)
    ch = new - old
    setup = f'At 31 December the trade receivables of {f} were {m(tr)}' + (f', before writing off irrecoverable debts of {m(wo)}' if wo else '') + f'. The allowance for doubtful debts brought forward was {m(old)}. The allowance is to be maintained at {pct_}% of trade receivables.'
    money = m2 if abs(new - round(new)) > 0.001 else m
    parts = [('Calculate the new allowance for doubtful debts.', money(new), f'({m(tr)}' + (f' − {m(wo)}' if wo else '') + f') × {pct_}% = {money(new)} [2]'),
             ('Calculate the amount charged or credited to the income statement for the change in the allowance.', f'{"Increase – charge" if ch > 0 else "Decrease – credit"} {money(abs(ch))}', f'{money(new)} − {m(old)} = {money(ch)} [1]; {"expense (debit)" if ch > 0 else "income (credit)"} [1] [2]')]
    if wo:
        parts.append(('Calculate the total effect on profit of the irrecoverable debts and the allowance adjustment.', f'Profit {"reduced" if wo + ch > 0 else "increased"} by {money(abs(wo + ch))}', f'Write-off {m(wo)} {"+" if ch > 0 else "−"} {money(abs(ch))} = {money(wo + ch)} [1]'))
    if D >= 3:
        parts.append(('Show how trade receivables appear in the statement of financial position.', f'Trade receivables {m(tr - wo)} less allowance {money(new)} = {money(tr - wo - new)}', f'{m(tr - wo)} − {money(new)} = {money(tr - wo - new)} under current assets [2]'))
    wrong = new
    c, ds = num_opts(money, abs(ch), [new, old, tr * pct_ / 100 - old if wo else new + old])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What amount is charged (or credited) in the income statement for the change in the allowance?', c, ds, f'{money(new)} − {m(old)} = {money(ch)}'),
            'err': (f'charged the whole new allowance of {money(wrong)} to the income statement', 'only the increase (or decrease) in the allowance is charged; the opening allowance was charged in earlier years', f'{"charge" if ch > 0 else "credit"} {money(abs(ch))}', f'{money(new)} − {m(old)}', 'income statement entry')}


t7_3 = A(7, 'Presenting receivables net of allowance in financial statements', ['presenting receivables net of allowance in financial statements', 'receivables net of allowance', 'presenting receivables'],
         mcqs=[('In the statement of financial position, the allowance for doubtful debts is', 'deducted from trade receivables under current assets', ['shown as a current liability', 'added to trade receivables', 'shown in the capital section'], 'Net realisable amount of receivables'),
               ('Trade receivables $25,000, allowance $750. The amount shown as net receivables is', '$24,250', ['$25,750', '$25,000', '$750'], '25,000 − 750'),
               ('Showing receivables net of an allowance gives', 'a more realistic value of the amount likely to be collected', ['a higher value of current assets', 'a lower bank balance', 'a higher profit'], 'Prudence'),
               ('Irrecoverable debts written off are', 'removed from trade receivables before the allowance is calculated', ['added to the allowance', 'shown as a current liability', 'ignored in the statements'], 'Write off first, then calculate the allowance'),
               ('Which item does NOT affect the net trade receivables figure?', 'Discounts received', ['Irrecoverable debts written off', 'The allowance for doubtful debts', 'Credit sales'], 'Discounts received relate to payables')],
         exps=[('Explain why trade receivables are shown net of the allowance for doubtful debts.', 'It shows the amount the business realistically expects to collect, so current assets are not overstated (prudence).', 'Realistic/collectable amount [1]; prudence – not overstated [1] [2]'),
               ('Explain how an increase in the allowance affects working capital.', 'Net receivables fall, so current assets and working capital fall by the amount of the increase, although no cash is involved.', 'Net receivables/CA fall [1]; working capital falls, non-cash [1] [2]')],
         disc=[('Discuss whether a high allowance for doubtful debts is a sign that {f} manages credit badly.', 'A high allowance may show poor credit control, but it may also reflect prudence or difficult trading conditions for customers.', 'Poor credit control possible [1]; prudence/economic conditions [1]; judgement [1] [3]')])


@spec(t7_3)
def t73_pres(r, D):
    f = firm(r)
    tr, wo, pct_, old, new = _allow(r, max(2, D))
    ca_other = step(r, 3000, 20000, 100)
    cl = step(r, 5000, 30000, 100)
    money = m2 if abs(new - round(new)) > 0.001 else m
    net = tr - wo - new
    setup = f'{f} has trade receivables of {m(tr)} at its year end, before irrecoverable debts of {m(wo)} are written off. An allowance for doubtful debts of {pct_}% of the remaining receivables is required (previous allowance {m(old)}). Other current assets total {m(ca_other)} and current liabilities are {m(cl)}.'
    parts = [('Calculate the net trade receivables shown in the statement of financial position.', money(net), f'{m(tr)} − {m(wo)} = {m(tr - wo)} [1]; allowance {pct_}% = {money(new)} [1]; net {money(net)} [1] [3]'),
             ('Calculate the working capital.', money(net + ca_other - cl), f'{money(net)} + {m(ca_other)} − {m(cl)} = {money(net + ca_other - cl)} [1]'),
             ('State the amount shown in the income statement for the change in the allowance.', f'{"Increase" if new > old else "Decrease"} {money(abs(new - old))}', f'{money(new)} − {m(old)} [1]')]
    c, ds = num_opts(money, net, [tr - new, tr - wo, tr - wo - (new - old), tr - wo + new])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the net trade receivables figure?', c, ds, f'({m(tr)} − {m(wo)}) − {money(new)} = {money(net)}'),
            'err': (f'showed net trade receivables of {money(tr - wo - (new - old))}', 'only the change in the allowance was deducted; the full closing allowance must be deducted from receivables', money(net), f'{m(tr - wo)} − {money(new)}', 'net receivables')}


CHAPTERS[7] = [t7_1, t7_2, t7_3]


# ===================================================================== 8 Non-current assets and depreciation
ASSETS = ['machine', 'delivery van', 'computer system', 'printing press', 'refrigeration unit', 'forklift truck', 'coffee roaster', 'packaging machine']
MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

t8_1 = A(8, 'Causes of depreciation and the straight-line method', ['causes of depreciation and the straight-line method', 'straight-line method', 'causes of depreciation', 'depreciation'],
         mcqs=[('Which is NOT a cause of depreciation?', 'An increase in the market value of the asset', ['Wear and tear', 'Obsolescence', 'Passage of time'], 'Depreciation reflects consumption of the asset'),
               ('A machine costs $24,000, has a residual value of $4,000 and a useful life of 5 years. Straight-line depreciation per year is', '$4,000', ['$4,800', '$5,600', '$2,000'], '(24,000 − 4,000) ÷ 5'),
               ('Depreciation is an example of the', 'accruals (matching) concept', ['business entity concept', 'realisation concept', 'money measurement concept'], 'Cost spread over the years that benefit'),
               ('The straight-line method is most suitable for assets that', 'give equal benefit in each year of their life', ['lose most value in the first year', 'are bought and sold frequently', 'have no residual value'], 'Equal annual charge'),
               ('Obsolescence means that an asset', 'is out of date because of new technology or changes in demand', ['has been worn out by use', 'has reached the end of its lease', 'has been stolen'], 'Technological/market change')],
         exps=[('Explain why non-current assets are depreciated.', 'Their cost is spread over the years that benefit from their use (matching concept), so profit in each year bears a fair share and the carrying amount reflects consumption of the asset.', 'Spread cost over useful life [1]; matching/fair profit [1] [2]'),
               ('State two causes of depreciation.', 'Wear and tear; obsolescence; passage of time (e.g. a lease); depletion (e.g. a mine).', 'Any two [1 each] [2]'),
               ('Explain why depreciation is a non-cash expense.', 'It allocates cost already paid when the asset was bought; no cash leaves the business when depreciation is charged.', 'Allocation of past cost [1]; no cash outflow [1] [2]')],
         disc=[('Explain why the carrying amount of the {a} is unlikely to equal its market value.', 'Depreciation allocates cost over useful life using estimates; it does not try to measure the asset\'s current market value.', 'Allocation not valuation [1]; estimates [1] [2]')])


@spec(t8_1)
def t81_sl(r, D):
    f = firm(r)
    a = r.choice(ASSETS)
    life = r.choice([4, 5, 8, 10])
    res = step(r, 0, 6000, 500) if D >= 2 else 0
    cost = res + step(r, 8000, 60000, life * 100)
    dep = (cost - res) // life
    mi = r.randrange(1, 12) if D >= 3 else 0
    setup = f'{f} bought a {a} for {m(cost)} on 1 {MON[mi]} 2024. It is expected to have a useful life of {life} years' + (f' and a residual value of {m(res)}' if res else ' with no residual value') + \
        '. Depreciation is charged using the straight-line method' + (' on a monthly basis (time apportioned).' if mi else '.') + ' The financial year ends on 31 December.'
    y1 = dep * (12 - mi) / 12
    ca2 = cost - y1 - dep
    parts = [('Calculate the annual depreciation charge.', m(dep), f'({m(cost)} − {m(res)}) ÷ {life} = {m(dep)} [2]')]
    if mi:
        parts.append(('Calculate the depreciation for the year ended 31 December 2024.', m(y1), f'{m(dep)} × {12 - mi}/12 = {m(y1)} [1]'))
    parts.append(('Calculate the carrying amount of the asset at 31 December 2025.', m(ca2), f'{m(cost)} − ({m(y1)} + {m(dep)}) = {m(ca2)} [2]'))
    c, ds = num_opts(m, dep, [cost // life, (cost + res) // life, dep * 2, cost - dep])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'a': a},
            'mcq': ('What is the annual depreciation charge?', c, ds, f'({m(cost)} − {m(res)}) ÷ {life}'),
            'err': (f'calculated annual depreciation as {m(cost // life)}', 'the residual value was not deducted from cost before dividing by the useful life', m(dep), f'({m(cost)} − {m(res)}) ÷ {life}', 'annual depreciation') if res else
            (f'calculated the carrying amount at 31 December 2025 as {m(cost - dep)}', 'only one year of depreciation was deducted; the carrying amount is cost less accumulated depreciation for both years', m(ca2), f'{m(cost)} − {m(y1 + dep)}', 'carrying amount')}


t8_2 = A(8, 'Reducing-balance and revaluation methods', ['reducing-balance and revaluation methods', 'reducing-balance', 'revaluation method'],
         mcqs=[('Under the reducing-balance method, the depreciation charge', 'falls each year', ['is the same each year', 'rises each year', 'is based on the original cost each year'], 'A fixed % of a falling carrying amount'),
               ('A van cost $20,000 and is depreciated at 25% reducing balance. Depreciation in year 2 is', '$3,750', ['$5,000', '$2,500', '$15,000'], 'Year 1 5,000; CA 15,000 × 25%'),
               ('The revaluation method is most suitable for', 'loose tools and small items such as crockery', ['premises', 'delivery vehicles', 'computer systems'], 'Many small, low-value items'),
               ('Loose tools: opening value $1,200, bought $500, closing valuation $1,100. Depreciation is', '$600', ['$100', '$500', '$1,600'], '1,200 + 500 − 1,100'),
               ('Reducing-balance depreciation is most appropriate for', 'motor vehicles, which lose most value early and need more repairs later', ['land', 'buildings with a long life', 'loose tools'], 'Matches falling benefit and rising repairs')],
         exps=[('Explain one advantage of the reducing-balance method over the straight-line method.', 'Higher charges in early years when the asset loses most value; total cost (depreciation + repairs) is more even over the asset\'s life.', 'Early high charge matches value loss [1]; evens out depreciation + repairs [1] [2]'),
               ('Explain how the revaluation method of depreciation works.', 'The items are valued at the end of each year; depreciation = opening value + purchases − closing valuation (less any disposal proceeds).', 'Valued each year [1]; formula [1] [2]')],
         disc=[('Evaluate whether {f} should change from the straight-line to the reducing-balance method.', 'RB better matches vans/computers, but changing method breaks consistency and must be justified; profit will change this year.', 'RB suitability [1]; consistency concept [1]; judgement [1] [3]')])


@spec(t8_2)
def t82_rb(r, D):
    f = firm(r)
    if D >= 4 and r.random() < 0.4:
        ov = step(r, 800, 6000, 10)
        bought = step(r, 200, 3000, 10)
        cv = step(r, int((ov + bought) * 0.6), int((ov + bought) * 0.9), 10)
        dep = ov + bought - cv
        setup = f'{f} uses the revaluation method for its loose tools. At 1 January they were valued at {m(ov)}. During the year tools costing {m(bought)} were bought. At 31 December the tools were valued at {m(cv)}.'
        parts = [('Calculate the depreciation of loose tools for the year.', m(dep), f'{m(ov)} + {m(bought)} − {m(cv)} = {m(dep)} [2]'),
                 ('Explain why the revaluation method is suitable for loose tools.', 'They are numerous, low-value items with different lives; recording each separately would be impractical.', 'Many small items [1]; impractical to depreciate individually [1] [2]')]
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f}, 'mcq': ('What is the depreciation for the year?', *num_opts(m, dep, [ov - cv, bought, ov + bought + cv]), f'{m(ov)} + {m(bought)} − {m(cv)}'),
                'err': (f'calculated depreciation as {m(ov - cv)}', 'the tools bought during the year were ignored', m(dep), f'{m(ov)} + {m(bought)} − {m(cv)}', 'depreciation')}
    a = r.choice(ASSETS)
    cost = step(r, 10000, 80000, 1000)
    rate = r.choice([10, 20, 25, 30, 40])
    n = 2 if D <= 2 else (3 if D == 3 else 4)
    ca, ch = cost, []
    for _ in range(n):
        d = ca * rate / 100
        ch.append(d)
        ca -= d
    money = m2 if any(abs(x - round(x)) > 0.001 for x in ch) else m
    setup = f'{f} bought a {a} for {m(cost)} at the start of year 1. It is depreciated at {rate}% per annum using the reducing-balance method.'
    parts = [(f'Calculate the depreciation charge for each of years 1 to {n}.', '; '.join(f'year {i + 1} {money(x)}' for i, x in enumerate(ch)), '; '.join(f'year {i + 1}: {money(x)}' for i, x in enumerate(ch)) + f' [{n}]'),
             (f'Calculate the carrying amount at the end of year {n}.', money(ca), f'{m(cost)} − {money(sum(ch))} = {money(ca)} [1]')]
    sl = cost * rate / 100
    if rate * n < 100:
        parts.append((f'Calculate the difference in total depreciation over {n} years if {rate}% straight-line on cost had been used.', money(sl * n - sum(ch)), f'SL {money(sl)} × {n} = {money(sl * n)}; difference {money(sl * n - sum(ch))} [2]'))
    c, ds = num_opts(money, ch[1], [sl, ch[0], ch[1] * 2, cost - ch[1]])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'a': a},
            'mcq': ('What is the depreciation charge for year 2?', c, ds, f'({m(cost)} − {money(ch[0])}) × {rate}% = {money(ch[1])}'),
            'err': (f'calculated year {n} depreciation as {money(sl)}', f'{rate}% was applied to the original cost (straight-line), not to the carrying amount brought forward', money(ch[-1]), f'{money(ca + ch[-1])} × {rate}%', f'year {n} depreciation')}


t8_3 = A(8, 'Ledger accounts for provision for depreciation', ['ledger accounts for provision for depreciation', 'provision for depreciation', 'accumulated depreciation'],
         mcqs=[('The annual depreciation charge is recorded by', 'debiting depreciation (income statement) and crediting provision for depreciation', ['debiting the asset account and crediting depreciation', 'debiting provision for depreciation and crediting bank', 'debiting bank and crediting the asset'], 'The asset stays at cost'),
               ('The provision for depreciation account normally has', 'a credit balance', ['a debit balance', 'no balance', 'a balance equal to the asset cost'], 'It reduces the asset'),
               ('In the statement of financial position, a non-current asset is shown at', 'cost less accumulated depreciation (carrying amount)', ['cost only', 'market value', 'cost plus depreciation'], 'Carrying amount'),
               ('Why is the asset account kept at cost?', 'So the original cost and the accumulated depreciation can both be seen', ['Because depreciation is never recorded', 'Because the asset never loses value', 'To increase profit'], 'Separate records'),
               ('A business charges a full year\'s depreciation in the year of purchase. An asset bought in November will receive', 'a full year\'s charge in that year', ['one month\'s charge', 'no charge in that year', 'two months\' charge'], 'Policy determines the charge')],
         exps=[('Explain why depreciation is credited to a provision account rather than to the asset account.', 'The asset account then shows the original cost while the provision shows accumulated depreciation; both are needed for the statement of financial position and for calculating disposals.', 'Cost retained [1]; accumulated depreciation visible/disposals [1] [2]'),
               ('Explain why accumulated depreciation is not a fund of cash.', 'It is a book entry allocating cost; no money is set aside, so it cannot be used to buy replacement assets.', 'Book entry only [1]; no cash set aside [1] [2]')],
         disc=[('Discuss whether {f} should charge depreciation on a monthly basis rather than a full year in the year of purchase.', 'Monthly charging matches cost to use more accurately; full-year is simpler; the difference is small if purchases are regular, and consistency matters.', 'Monthly – accurate [1]; full-year – simple [1]; judgement [1] [3]')])


@spec(t8_3)
def t83_prov(r, D):
    f = firm(r)
    rate = r.choice([10, 20, 25])
    c1 = step(r, 10000, 50000, 1000)
    c2 = step(r, 5000, 30000, 1000) if D >= 2 else 0
    rb = D >= 4
    pol = 'a full year\'s depreciation in the year of purchase and none in the year of disposal'
    yrs = 3
    acc, rows = 0, []
    cost_tot = 0
    for y in range(1, yrs + 1):
        cost_tot = c1 + (c2 if y >= 2 else 0)
        base = cost_tot - acc if rb else cost_tot
        d = base * rate / 100
        acc += d
        rows.append((2023 + y, d, acc))
    money = m2 if any(abs(x[1] - round(x[1])) > 0.001 for x in rows) else m
    meth = 'reducing balance' if rb else 'straight-line on cost'
    setup = f'{f} bought equipment for {m(c1)} on 1 March 2024' + (f' and further equipment for {m(c2)} on 1 August 2025' if c2 else '') + f'. Depreciation is charged at {rate}% per annum, {meth}, with {pol}. The year end is 31 December.'
    parts = [('Calculate the depreciation charge for each of the years 2024, 2025 and 2026.', '; '.join(f'{y}: {money(d)}' for y, d, _ in rows), '; '.join(f'{y} {money(d)}' for y, d, _ in rows) + ' [3]'),
             ('Prepare the provision for depreciation account for 2026, showing the balance carried down.', f'Balance b/d {money(rows[1][2])}; income statement {money(rows[2][1])}; balance c/d {money(rows[2][2])}', f'Balance b/d {money(rows[1][2])} [1]; IS {money(rows[2][1])} [1]; c/d {money(rows[2][2])} [1] [3]'),
             ('Calculate the carrying amount of the equipment at 31 December 2026.', money(cost_tot - acc), f'{m(cost_tot)} − {money(acc)} = {money(cost_tot - acc)} [1]')]
    c, ds = num_opts(money, rows[2][2], [rows[2][1], rows[1][2], cost_tot * rate / 100 * 3, rows[2][2] + rows[2][1]])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the balance on the provision for depreciation account at 31 December 2026?', c, ds, ' + '.join(money(d) for _, d, _ in rows) + f' = {money(rows[2][2])}'),
            'err': (f'charged depreciation of {money(c1 * rate / 100)} in 2025', 'the additional equipment bought in 2025 was ignored; the policy gives a full year\'s charge in the year of purchase', money(rows[1][1]), f'{rate}% × ' + (f'({m(c1)} + {m(c2)})' if not rb else f'({m(c1 + c2)} − {money(rows[0][2])})'), '2025 depreciation') if c2 else None}


t8_4 = A(8, 'Disposal of non-current assets: profit or loss on disposal', ['disposal of non-current assets: profit or loss on disposal', 'disposal of non-current assets', 'profit or loss on disposal', 'disposal'],
         mcqs=[('On disposal, the cost of the asset is transferred by', 'debiting the disposal account and crediting the asset account', ['debiting the asset account and crediting disposal', 'debiting bank and crediting the asset', 'debiting depreciation and crediting disposal'], 'Remove the asset at cost'),
               ('A machine cost $12,000, accumulated depreciation $7,500, sold for $3,800. The result is', 'a loss of $700', ['a profit of $700', 'a loss of $8,200', 'a profit of $3,800'], 'CA 4,500 − 3,800'),
               ('A loss on disposal is', 'an expense in the income statement', ['deducted from capital', 'added to the asset account', 'a current liability'], 'Under-depreciation adjustment'),
               ('In a part-exchange, the trade-in allowance is', 'credited to the disposal account', ['debited to the disposal account', 'credited to bank', 'debited to provision for depreciation'], 'It is the "proceeds" of the old asset'),
               ('A profit on disposal suggests that', 'too much depreciation was charged while the asset was owned', ['too little depreciation was charged', 'the asset was revalued', 'the asset was stolen'], 'Over-depreciation corrected')],
         exps=[('Explain why a profit on disposal does not necessarily mean the asset was a good investment.', 'It only shows that the depreciation charged was more than the actual fall in value; it adjusts past estimates rather than measuring the asset\'s return.', 'Adjustment of past depreciation estimates [1]; not a measure of return [1] [2]'),
               ('State the entries in the disposal account when an asset is sold for cash.', 'Dr disposal with cost (Cr asset); Cr disposal with accumulated depreciation (Dr provision); Cr disposal with proceeds (Dr bank); balance = profit or loss to IS.', 'Cost [1]; depreciation and proceeds [1] [2]')],
         disc=[('Discuss whether {f} should replace the {a} now or keep it for longer.', 'Replacement brings efficiency and lower repairs but costs cash and may need finance; keeping it saves cash but repair costs and breakdown risk rise.', 'Benefit of replacement [1]; cost/finance [1]; judgement [1] [3]')])


@spec(t8_4)
def t84_disp(r, D):
    f = firm(r)
    a = r.choice(ASSETS)
    cost = step(r, 10000, 60000, 1000)
    rate = r.choice([10, 20, 25])
    rb = D >= 4 and r.random() < 0.5
    yrs = r.choice([2, 3]) if D <= 3 else r.choice([3, 4])
    acc, ca = 0, cost
    for _ in range(yrs):
        d = (ca if rb else cost) * rate / 100
        acc += d
        ca -= d
    pe = D >= 3 and r.random() < 0.5
    proceeds = step(r, int(ca * 0.6), int(ca * 1.3) + 100, 50)
    if abs(proceeds - ca) < 1:
        proceeds += 150
    res = proceeds - ca
    money = m2 if abs(acc - round(acc)) > 0.001 else m
    how = (f'was given in part-exchange for a new {a} costing {m(cost + step(r, 2000, 20000, 1000))}; the supplier allowed {m(proceeds)} for the old one' if pe else f'was sold for {m(proceeds)} by bank transfer')
    setup = f'{f} bought a {a} for {m(cost)}. Depreciation was charged at {rate}% per annum {"reducing balance" if rb else "straight-line on cost"}, a full year in the year of purchase and none in the year of disposal. After {yrs} full years the {a} {how}.'
    parts = [('Calculate the accumulated depreciation at the date of disposal.', money(acc), f'{" + ".join(money((cost * (1 - rate / 100) ** i if rb else cost) * rate / 100) for i in range(yrs))} = {money(acc)} [2]'),
             ('Calculate the profit or loss on disposal.', f'{"Profit" if res > 0 else "Loss"} {money(abs(res))}', f'Carrying amount {m(cost)} − {money(acc)} = {money(ca)} [1]; {m(proceeds)} − {money(ca)} = {"profit" if res > 0 else "loss"} {money(abs(res))} [1] [2]'),
             ('Prepare the disposal account.', f'Dr asset {m(cost)}; Cr provision for depreciation {money(acc)}; Cr {"new asset supplier (part-exchange)" if pe else "bank"} {m(proceeds)}; {"profit to IS (Dr)" if res > 0 else "loss to IS (Cr)"} {money(abs(res))}',
              f'Cost [1]; depreciation [1]; proceeds/trade-in [1]; {"profit" if res > 0 else "loss"} to IS [1] [4]')]
    wrong = proceeds - cost
    c, ds = num_opts(money, abs(res), [abs(wrong), acc, proceeds, abs(res) * 2])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'a': a},
            'mcq': (f'What is the {"profit" if res > 0 else "loss"} on disposal?', c, ds, f'CA {money(ca)}; proceeds {m(proceeds)}'),
            'err': (f'calculated a loss on disposal of {money(abs(wrong))}', 'the proceeds were compared with the original cost; they must be compared with the carrying amount (cost less accumulated depreciation)', f'{"profit" if res > 0 else "loss"} {money(abs(res))}', f'{m(proceeds)} − ({m(cost)} − {money(acc)})', 'profit or loss on disposal')}


t8_5 = A(8, 'Non-current asset register and IAS 16 basics', ['non-current asset register and ias 16 basics', 'non-current asset register', 'ias 16'],
         mcqs=[('Under IAS 16, which cost should be included in the cost of a new machine?', 'Installation and testing costs', ['Staff training on the new machine', 'The first year\'s maintenance contract', 'Advertising the products it will make'], 'Costs to bring the asset to working condition'),
               ('A non-current asset register records', 'details of each asset such as cost, date of purchase, location, depreciation and carrying amount', ['the daily cash receipts', 'the balances of all customers', 'the inventory held in the warehouse'], 'Control over assets'),
               ('Under IAS 16, the residual value and useful life of an asset should be', 'reviewed at least at each financial year end', ['fixed for the whole life of the asset', 'ignored', 'set equal to zero'], 'Estimates are reviewed annually'),
               ('Which item is property, plant and equipment?', 'Delivery vehicles used by the business', ['Goods held for resale', 'Trade receivables', 'Patents'], 'Tangible assets used for more than one period'),
               ('Which is a benefit of keeping a non-current asset register?', 'Assets can be checked physically against the records to detect loss or theft', ['It replaces the need for depreciation', 'It increases profit', 'It records credit sales'], 'Control')],
         exps=[('Explain two benefits to a business of keeping a non-current asset register.', 'Physical checks can detect theft or loss; depreciation and disposal calculations are easier; insurance and maintenance can be planned; the register can be reconciled with the ledger.', 'Any two benefits [1 each] [2]'),
               ('Explain why training costs are not capitalised as part of the cost of a machine.', 'They do not bring the asset itself to working condition; the benefit belongs to the staff, who may leave, so the cost is an expense (IAS 16).', 'Not directly attributable to asset [1]; expense [1] [2]')],
         disc=[('Explain how the asset register could help {f} control its non-current assets.', 'Regular physical checks against the register reveal missing or idle assets; responsibility can be assigned by location.', 'Physical check [1]; control/responsibility [1] [2]')])


@spec(t8_5)
def t85_cost(r, D):
    f = firm(r)
    a = r.choice(ASSETS)
    lp = step(r, 20000, 90000, 1000)
    td = r.choice([0, 5, 10]) if D >= 2 else 0
    inc = [('delivery', step(r, 200, 1500, 50), True), ('installation', step(r, 500, 3000, 50), True), ('testing', step(r, 200, 1200, 50), True),
           ('a one-year maintenance contract', step(r, 500, 2500, 50), False), ('training of operators', step(r, 300, 2000, 50), False), ('insurance for the first year', step(r, 200, 1500, 50), False)]
    k = 3 if D <= 2 else (4 if D == 3 else 6)
    its = [inc[0], inc[3]] + r.sample([inc[1], inc[2], inc[4], inc[5]], k - 2)
    r.shuffle(its)
    net = lp * (100 - td) // 100
    cap = net + sum(v for _, v, c in its if c)
    exp = sum(v for _, v, c in its if not c)
    setup = f'{f} bought a new {a} with a list price of {m(lp)}' + (f', less {td}% trade discount' if td else '') + '. The following were also paid: ' + ', '.join(f'{d} {m(v)}' for d, v, _ in its) + '.'
    parts = [(f'Calculate the cost of the {a} to be capitalised under IAS 16.', m(cap), (f'{m(lp)} × {100 - td}% = {m(net)} [1]; ' if td else '') + 'add ' + ', '.join(d for d, _, c in its if c) + f' [1]; exclude ' + ', '.join(d for d, _, c in its if not c) + f' [1]; = {m(cap)} [1] [{4 if td else 3}]'),
             ('State the amount to be charged as an expense in the income statement.', m(exp), f'{" + ".join(d for d, _, c in its if not c)} = {m(exp)} [1]'),
             ('State two details that would be recorded in the non-current asset register for this asset.', 'Date of purchase, cost, supplier, location, serial number, depreciation method and rate, carrying amount.', 'Any two [1 each] [2]')]
    c, ds = num_opts(m, cap, [cap + exp, lp + sum(v for _, v, c in its if c), net, cap - its[0][1]])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'a': a},
            'mcq': (f'What is the cost of the {a} under IAS 16?', c, ds, f'Directly attributable costs only = {m(cap)}'),
            'err': (f'capitalised {m(cap + exp)} as the cost of the {a}', 'costs such as maintenance, insurance or training are not directly attributable to bringing the asset into working condition and must be expensed', m(cap), f'{m(net)} + ' + ' + '.join(m(v) for _, v, c in its if c), 'cost')}


CHAPTERS[8] = [t8_1, t8_2, t8_3, t8_4, t8_5]


# ===================================================================== 9 Inventory valuation
GOODS = ['jackets', 'kettles', 'lamps', 'printers', 'rugs', 'speakers', 'bicycles', 'tablets', 'mirrors', 'tents']

t9_1 = A(9, 'Lower of cost and net realisable value', ['lower of cost and net realisable value', 'net realisable value', 'lower of cost'],
         mcqs=[('Net realisable value is', 'the expected selling price less the costs of completing and selling the item', ['the cost of the item plus profit', 'the replacement cost of the item', 'the original cost less depreciation'], 'IAS 2 definition'),
               ('An item cost $80. It can be sold for $95 after repairs costing $25. At what value is it included in inventory?', '$70', ['$80', '$95', '$55'], 'NRV 95 − 25 = 70 < cost 80'),
               ('Valuing inventory at the lower of cost and NRV applies the', 'prudence concept', ['business entity concept', 'duality concept', 'realisation concept'], 'Losses are recognised, unrealised gains are not'),
               ('Inventory should be valued item by item (or by groups of similar items) because', 'gains on some items should not hide losses on others', ['it is quicker', 'it increases profit', 'total NRV is always lower'], 'Prevents offsetting'),
               ('Which cost is NOT included in the cost of inventory under IAS 2?', 'Selling and distribution costs', ['Purchase price', 'Carriage inwards', 'Import duties'], 'Only costs of bringing inventory to its present location and condition')],
         exps=[('Explain why inventory is valued at the lower of cost and net realisable value.', 'Applying prudence: if goods can only be sold for less than they cost, the loss is recognised now; unrealised profits are not recognised until the goods are sold.', 'Prudence [1]; losses recognised, gains not [1] [2]'),
               ('State two reasons why the net realisable value of inventory may fall below cost.', 'Goods are damaged or obsolete; fashion has changed; selling prices have fallen; costs to complete/sell have risen.', 'Any two [1 each] [2]')],
         disc=[('Discuss whether {f} should sell its damaged items at a reduced price or scrap them.', 'Selling recovers some cash (NRV above zero) and frees space, but may harm the brand; scrapping avoids reputation damage but loses the value.', 'Cash recovered [1]; reputation/space [1]; judgement [1] [3]')])


@spec(t9_1)
def t91_nrv(r, D):
    f = firm(r)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    gs = r.sample(GOODS, k)
    rows = []
    for g in gs:
        n = r.choice([10, 20, 25, 40, 50])
        c = step(r, 20, 300, 5)
        if r.random() < 0.5:
            sp, extra = c + step(r, 10, 120, 5), 0
        else:
            sp = c + step(r, -40, 40, 5) if c > 50 else c + 20
            extra = step(r, 10, 60, 5)
        nrv = sp - extra
        rows.append((g, n, c, sp, extra, min(c, nrv)))
    tot = sum(n * v for _, n, _, _, _, v in rows)
    cost = sum(n * c for _, n, c, _, _, _ in rows)
    desc = '; '.join(f'{n} {g}: cost {m(c)} each, selling price {m(sp)} each' + (f', but each needs repairs costing {m(e)} before sale' if e else '') for g, n, c, sp, e, _ in rows)
    setup = f'At its year end {f} held the following inventory: {desc}.'
    parts = [('Calculate the value of closing inventory using the lower of cost and net realisable value.', m(tot), '; '.join(f'{g}: {n} × {m(v)} = {m(n * v)}' for g, n, _, _, _, v in rows) + f' [{k}]; total {m(tot)} [1] [{k + 1}]'),
             ('Calculate the effect on gross profit of using this valuation instead of cost.', f'Gross profit is {m(cost - tot)} lower' if cost > tot else 'No effect – every item is valued at cost', f'Cost {m(cost)} − {m(tot)} = {m(cost - tot)} [1]')]
    c, ds = num_opts(m, tot, [cost, sum(n * min(c, sp) for _, n, c, sp, _, _ in rows), sum(n * sp for _, n, _, sp, _, _ in rows)])
    w = sum(n * min(c, sp) for _, n, c, sp, _, _ in rows)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the value of closing inventory?', c, ds, f'Lower of cost and NRV for each item = {m(tot)}'),
            'err': (f'valued the inventory at {m(w)}', 'the costs of repair were not deducted from selling price to find net realisable value', m(tot), ' + '.join(m(n * v) for _, n, _, _, _, v in rows), 'inventory value') if w != tot else
            (f'valued the inventory at {m(cost)}', 'cost was used for every item, even where NRV is lower', m(tot), ' + '.join(m(n * v) for _, n, _, _, _, v in rows), 'inventory value') if cost != tot else None}


def _stores(r, D):
    ou = r.choice([0, 100, 200, 50]) if D >= 2 else 0
    op_ = step(r, 200, 800, 5) / 100
    tx = []
    pr = op_
    for _ in range(2 if D <= 3 else 3):
        q = r.choice([100, 150, 200, 250, 300, 400])
        pr = round(pr + step(r, 5, 60, 5) / 100, 2)
        tx.append(('in', q, pr))
        tx.append(('out', None, None))
    lots = [[ou, op_]] if ou else []
    av_q, av_v = ou, ou * op_
    rows = []
    for t in tx:
        if t[0] == 'in':
            lots.append([t[1], t[2]])
            av_q += t[1]
            av_v += t[1] * t[2]
            rows.append(t)
        else:
            have = sum(x[0] for x in lots)
            q = r.choice([x for x in (50, 100, 150, 200, 250, 300) if x <= have * 0.8] or [have // 2])
            rem = q
            while rem:
                take = min(rem, lots[0][0])
                lots[0][0] -= take
                rem -= take
                if lots[0][0] == 0:
                    lots.pop(0)
            av_v -= q * (av_v / av_q)
            av_q -= q
            rows.append(('out', q, None))
    fifo = sum(a * b for a, b in lots)
    return ou, op_, rows, fifo, av_v, av_q


t9_2 = A(9, 'FIFO and AVCO methods of inventory valuation', ['fifo and avco methods of inventory valuation', 'fifo', 'avco'],
         mcqs=[('Under FIFO, closing inventory is valued at', 'the most recent purchase prices', ['the earliest purchase prices', 'an average of all prices', 'the selling price'], 'Oldest goods are issued first'),
               ('In a period of rising prices, which method gives the higher closing inventory value?', 'FIFO', ['AVCO', 'Both give the same', 'It depends on the selling price'], 'FIFO leaves the latest (dearer) goods'),
               ('Under AVCO (perpetual), the average cost is recalculated', 'after each receipt of goods', ['after each issue', 'only at the year end', 'only when prices fall'], 'Weighted average updated on each purchase'),
               ('Which method is NOT allowed under IAS 2?', 'LIFO', ['FIFO', 'AVCO', 'Specific identification for unique items'], 'LIFO is prohibited'),
               ('In rising prices, using FIFO rather than AVCO will', 'increase gross profit', ['reduce gross profit', 'not affect gross profit', 'increase cost of sales'], 'Higher closing inventory → lower cost of sales')],
         exps=[('Explain why FIFO gives a higher profit than AVCO when prices are rising.', 'FIFO charges the older, cheaper costs to cost of sales and leaves newer, dearer goods in closing inventory, so cost of sales is lower and profit higher.', 'Older cheaper costs in COS [1]; higher closing inventory → higher profit [1] [2]'),
               ('State one advantage and one disadvantage of AVCO.', 'Advantage: smooths out price fluctuations / acceptable under IAS 2. Disadvantage: average must be recalculated after every receipt; values do not match actual prices paid.', 'Advantage [1]; disadvantage [1] [2]')],
         disc=[('Advise {f} whether to use FIFO or AVCO, given that prices are rising.', 'FIFO gives a higher, more up-to-date inventory value and higher profit; AVCO smooths results; whichever is chosen must be applied consistently.', 'FIFO effect [1]; AVCO effect [1]; consistency/recommendation [1] [3]')])


@spec(t9_2)
def t92_fifo(r, D):
    f = firm(r)
    g = r.choice(GOODS)
    ou, op_, rows, fifo, av, avq = _stores(r, D)
    days_ = [3, 8, 14, 19, 24, 28]
    lines = ([f'1 June: opening inventory {ou} units at {m2(op_)}'] if ou else []) + [f'{days_[i]} June: ' + (f'bought {q} units at {m2(p)} each' if k == 'in' else f'sold {q} units') for i, (k, q, p) in enumerate(rows)]
    setup = f'{f} sells {g}. Its inventory records for June show: ' + '; '.join(lines) + '.'
    parts = [('Calculate the value of closing inventory at 30 June using FIFO.', m2(fifo), f'Closing {avq} units at latest prices = {m2(fifo)} [2]')]
    if D >= 3:
        parts.append(('Calculate the value of closing inventory at 30 June using AVCO (perpetual).', m2(av), f'Weighted average recalculated after each purchase; {avq} units = {m2(av)} [3]'))
        parts.append(('State, with a reason, which method gives the higher gross profit.', f'{"FIFO" if fifo > av else "AVCO"}, because it gives the higher closing inventory and so the lower cost of sales.', 'Correct method [1]; reason – higher closing inventory → lower COS [1] [2]'))
    c, ds = num_opts(m2, fifo, [av, avq * op_ if ou else avq * rows[0][2], avq * rows[-2][2] * 1.1])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the value of closing inventory using FIFO?', c, ds, f'{avq} units remain, valued at the latest purchase prices = {m2(fifo)}'),
            'err': (f'valued closing inventory under FIFO at {m2(avq * (op_ if ou else rows[0][2]))}', 'the earliest prices were used; under FIFO the earliest units are issued first so closing inventory is at the latest prices', m2(fifo), f'{avq} units at latest purchase prices', 'FIFO value') if abs(avq * (op_ if ou else rows[0][2]) - fifo) > 0.5 else None}


t9_3 = A(9, 'Effect of inventory valuation on profit', ['effect of inventory valuation on profit', 'inventory valuation on profit'],
         mcqs=[('Closing inventory is overstated by $2,000. The effect on profit for the year is', 'profit overstated by $2,000', ['profit understated by $2,000', 'no effect', 'profit overstated by $4,000'], 'Cost of sales is understated'),
               ('Closing inventory of this year was overstated by $1,500. Next year\'s profit will be', 'understated by $1,500', ['overstated by $1,500', 'unaffected', 'understated by $3,000'], 'It becomes next year\'s opening inventory'),
               ('Opening inventory is understated. Profit for the year will be', 'overstated', ['understated', 'unaffected', 'understated by twice the error'], 'Cost of sales understated'),
               ('Over the whole life of a business, the choice of inventory method affects', 'only the timing of profit, not the total profit', ['the total profit earned', 'the cash received', 'the total sales'], 'Differences reverse'),
               ('If closing inventory is overstated, the statement of financial position shows', 'current assets and capital both overstated', ['current liabilities overstated', 'non-current assets overstated', 'no error'], 'Inventory and profit both too high')],
         exps=[('Explain why an error in closing inventory affects the profit of two years.', 'Closing inventory of one year is the opening inventory of the next; an overstatement raises this year\'s profit and reduces next year\'s by the same amount.', 'Closing becomes opening [1]; reverses next year [1] [2]'),
               ('Explain how an overstatement of closing inventory affects the statement of financial position.', 'Current assets are overstated, and because profit is overstated, capital is overstated by the same amount.', 'Current assets overstated [1]; capital overstated [1] [2]')],
         disc=[('Discuss why the owner of {f} might be tempted to overvalue closing inventory, and why this does not help in the long run.', 'It increases reported profit this year (e.g. for a loan), but next year\'s profit falls by the same amount; it breaks prudence and misleads users.', 'Motive [1]; reversal next year [1]; ethics/prudence [1] [3]')])


@spec(t9_3)
def t93_eff(r, D):
    f = firm(r)
    dp_ = step(r, 20000, 80000, 100)
    e = step(r, 500, 6000, 100)
    over = r.random() < 0.5
    which = r.choice(['closing', 'opening']) if D >= 3 else 'closing'
    sign = (-1 if over else 1) * (1 if which == 'closing' else -1)
    cp_ = dp_ + sign * e
    setup = f'{f} calculated a draft profit of {m(dp_)} for the year. It was then discovered that {which} inventory had been {"overstated" if over else "understated"} by {m(e)}, because some items were {"counted twice" if over else "omitted from the count"}.'
    parts = [('Calculate the corrected profit for the year.', m(cp_), f'{which} inventory {"over" if over else "under"}stated → cost of sales {"under" if (over == (which == "closing")) else "over"}stated [1]; {m(dp_)} {"+" if sign > 0 else "−"} {m(e)} = {m(cp_)} [1] [2]')]
    if which == 'closing':
        parts.append(('State the effect of the error on next year\'s profit if it were not corrected.', f'Next year\'s profit would be {"understated" if over else "overstated"} by {m(e)}.', f'{"Understated" if over else "Overstated"} [1]; by {m(e)} [1] [2]'))
    if which == 'closing':
        parts.append(('State the effect of the error on the statement of financial position at the year end.', f'Inventory (current assets) and capital {"overstated" if over else "understated"} by {m(e)}.', 'Current assets and capital [1]; direction and amount [1] [2]'))
    else:
        parts.append(('Explain why the closing capital at the end of this year is not affected by the error.', 'The opening inventory error came from last year\'s closing inventory; last year\'s profit was misstated in the opposite direction, so the two errors cancel in closing capital.', 'Last year\'s profit misstated oppositely [1]; cancel in capital [1] [2]'))
    c, ds = num_opts(m, cp_, [dp_ - sign * e, dp_, dp_ + 2 * sign * e])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the corrected profit?', c, ds, f'{m(dp_)} {"+" if sign > 0 else "−"} {m(e)} = {m(cp_)}'),
            'err': (f'calculated the corrected profit as {m(dp_ - sign * e)}', f'the adjustment was made in the wrong direction: {"over" if over else "under"}stated {which} inventory {"increases" if sign < 0 else "decreases"} profit, so the correction must {"reduce" if sign < 0 else "increase"} it', m(cp_), f'{m(dp_)} {"+" if sign > 0 else "−"} {m(e)}', 'profit')}


CHAPTERS[9] = [t9_1, t9_2, t9_3]


# ===================================================================== 10 Bank reconciliation statements
BRITEMS = [('bank charges of {x} shown on the bank statement', 'cash book', -1), ('a credit transfer of {x} received from a customer', 'cash book', 1), ('a cheque for {x} from a customer was dishonoured', 'cash book', -1),
           ('a standing order of {x} for insurance', 'cash book', -1), ('interest received of {x}', 'cash book', 1), ('a direct debit of {x} for electricity', 'cash book', -1),
           ('cheques paid to suppliers of {x} not yet presented for payment', 'statement', 0), ('takings of {x} paid in on the last day of the month not yet credited by the bank', 'statement', 0)]

t10_1 = A(10, 'Reasons for differences between cash book and bank statement', ['reasons for differences between cash book and bank statement', 'differences between cash book and bank statement', 'reasons for differences'],
          mcqs=[('An unpresented cheque is', 'a cheque paid to a supplier and entered in the cash book but not yet shown on the bank statement', ['a cheque received but not yet banked', 'a cheque returned unpaid by the bank', 'a cheque that has been cancelled'], 'Timing difference on payments'),
                ('Which item is a timing difference?', 'An outstanding lodgement', ['Bank charges', 'A dishonoured cheque', 'A credit transfer'], 'It will appear on the next bank statement'),
                ('Which item requires the cash book to be updated?', 'Bank interest charged', ['An unpresented cheque', 'An outstanding lodgement', 'A bank error'], 'The business learns of it from the statement'),
                ('A bank statement shows a credit balance. From the business\'s point of view this means', 'the business has money in the bank', ['the business is overdrawn', 'the bank owes nothing', 'the cash book is wrong'], 'The bank owes the customer'),
                ('Which item would appear in the bank statement but not yet in the cash book?', 'A standing order payment', ['A cheque paid to a supplier last week', 'Takings banked late on the last day', 'Cash sales kept in the till'], 'Automatic payment')],
          exps=[('Explain why the balance in the cash book may differ from the balance on the bank statement.', 'Timing differences (unpresented cheques, outstanding lodgements); items the business does not know about until it receives the statement (charges, standing orders, credit transfers, dishonoured cheques); errors by the business or the bank.', 'Timing differences [1]; items not yet in cash book [1]; errors [1] [3]'),
                ('Explain why a bank statement shows a positive bank balance as a credit.', 'The statement is prepared from the bank\'s point of view: money deposited is owed by the bank to the customer, a liability of the bank.', 'Bank\'s viewpoint [1]; liability of the bank [1] [2]')],
          disc=[('Explain why {f} should prepare a bank reconciliation every month.', 'To detect errors and fraud quickly, update the cash book for unrecorded items and know the true bank balance for decisions.', 'Detect errors/fraud [1]; accurate balance [1] [2]')])


@spec(t10_1, typ='short')
def t101_class(r, D):
    f = firm(r)
    k = 3 if D <= 2 else (4 if D == 3 else 6)
    its = r.sample(BRITEMS, k)
    txt = [d.format(x=m(step(r, 50, 3000, 10))) for d, _, _ in its]
    setup = f'When {f} compared its cash book with the bank statement for March, it found: {lst(txt)}.'
    parts = [('For each item, state whether it should be entered in the cash book or shown in the bank reconciliation statement.', '; '.join(f'({ROM[i]}) {"update cash book" if w == "cash book" else "bank reconciliation statement"}' for i, (_, w, _) in enumerate(its)),
              '; '.join(f'({ROM[i]}) {"cash book" if w == "cash book" else "BRS"} [1]' for i, (_, w, _) in enumerate(its)) + f' [{k}]'),
             ('Explain why some items appear only in the bank reconciliation statement.', 'They are timing differences: already correctly entered in the cash book but not yet processed by the bank.', 'Timing difference [1]; already in cash book [1] [2]')]
    d0, w0, _ = its[0]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'How should item (i) be dealt with?', 'Enter it in the cash book' if w0 == 'cash book' else 'Show it in the bank reconciliation statement', ['Enter it in the cash book' if w0 != 'cash book' else 'Show it in the bank reconciliation statement', 'Ignore it until next month', 'Ask the bank to reverse it'], 'Items the business did not know about go in the cash book; timing differences go in the BRS'),
            'err': (f'said that item (i) only needs to be shown in the bank reconciliation statement' if w0 == 'cash book' else 'entered item (i) in the cash book', 'items such as charges, standing orders, credit transfers, interest and dishonoured cheques must update the cash book' if w0 == 'cash book' else 'it is a timing difference already recorded in the cash book; entering it again would double count it',
                    'update the cash book' if w0 == 'cash book' else 'show it in the BRS only', 'classify as unrecorded item or timing difference', 'treatment')}


def _cb_update(r, D):
    cb = step(r, 1500, 9000, 10)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    its = r.sample([x for x in BRITEMS if x[1] == 'cash book'], k)
    xs = [step(r, 30, 1800, 5) for _ in its]
    upd = cb + sum(s * x for (_, _, s), x in zip(its, xs))
    return cb, its, xs, upd


t10_2 = A(10, 'Updating the cash book for bank charges, credit transfers and dishonoured cheques', ['updating the cash book for bank charges, credit transfers and dishonoured cheques', 'updating the cash book', 'dishonoured cheques', 'credit transfers'],
          mcqs=[('A customer\'s cheque is dishonoured. The entry in the cash book is on the', 'credit side, and the customer is debited again', ['debit side, and the customer is credited', 'credit side, and sales is debited', 'debit side only'], 'The receipt is reversed'),
                ('A credit transfer received from a customer is entered', 'on the debit side of the cash book', ['on the credit side of the cash book', 'only in the bank reconciliation statement', 'in the sales journal'], 'Money received'),
                ('Cash book debit balance $3,200; bank charges $45 and a credit transfer of $300 appear only on the statement. The updated cash book balance is', '$3,455', ['$2,945', '$3,545', '$3,155'], '3,200 − 45 + 300'),
                ('Bank charges not yet in the cash book are recorded by', 'Dr bank charges, Cr bank (cash book)', ['Dr bank, Cr bank charges', 'Dr bank charges, Cr capital', 'Only in the bank reconciliation'], 'Expense paid from the bank'),
                ('The updated cash book balance is the figure shown', 'in the statement of financial position', ['on the next bank statement', 'in the income statement', 'only in the bank reconciliation'], 'It is the correct balance')],
          exps=[('Explain why the cash book must be updated before the bank reconciliation statement is prepared.', 'So the cash book shows the correct balance for the financial statements; the reconciliation then only needs to explain timing differences.', 'Correct balance for SFP [1]; BRS for timing only [1] [2]'),
                ('Explain what a dishonoured cheque means for the business.', 'The customer\'s bank refused to pay, so the money has not been received; the customer again owes the debt and the bank balance is lower.', 'Not paid by customer\'s bank [1]; debt reinstated, bank reduced [1] [2]')],
          disc=[('Suggest how {f} could reduce the number of dishonoured cheques it receives.', 'Ask for payment by bank transfer or card; credit checks; wait for cheques to clear before releasing goods.', 'Two measures [1 each] [2]')])


@spec(t10_2)
def t102_cb(r, D):
    f = firm(r)
    cb, its, xs, upd = _cb_update(r, D)
    txt = [d.format(x=m(x)) for (d, _, _), x in zip(its, xs)]
    setup = f'The cash book of {f} showed a debit balance of {m(cb)} at 31 May. The bank statement showed: {lst(txt)}. None of these had been entered in the cash book.'
    w = f'{m(cb)}' + ''.join(f' {"+" if s > 0 else "−"} {m(x)}' for (_, _, s), x in zip(its, xs)) + f' = {m(upd)}'
    parts = [('Calculate the updated cash book balance at 31 May.', f'{m(abs(upd))} {"debit (in bank)" if upd >= 0 else "credit (overdraft)"}', f'Receipts added, payments deducted [1 per item]; {w} [1] [{len(its) + 1}]')]
    di = [i for i, (d, _, _) in enumerate(its) if 'dishonoured' in d]
    if di:
        parts.append(('State the double entry for the dishonoured cheque.', f'Dr the customer\'s account, Cr bank (cash book) {m(xs[di[0]])}.', 'Dr customer [1]; Cr bank [1] [2]'))
    else:
        parts.append(('State the double entry for the first item.', f'{"Dr bank, Cr " + ("the customer" if "transfer" in its[0][0] else "interest received") if its[0][2] > 0 else "Dr " + ("bank charges" if "charges" in its[0][0] else "insurance" if "insurance" in its[0][0] else "electricity") + ", Cr bank"} {m(xs[0])}.', 'Correct debit [1]; correct credit [1] [2]'))
    wrong = cb - sum(s * x for (_, _, s), x in zip(its, xs))
    c, ds = num_opts(m, upd, [wrong, cb, cb + sum(xs)])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the updated cash book balance?', c, ds, w),
            'err': (f'calculated the updated balance as {m(wrong)}', 'receipts on the statement were deducted and payments added – the opposite of the correct treatment', m(upd), w.split(' = ')[0], 'updated balance')}


t10_3 = A(10, 'Preparing a bank reconciliation statement', ['preparing a bank reconciliation statement', 'bank reconciliation statement', 'bank reconciliation'],
          mcqs=[('Starting with the updated cash book balance, unpresented cheques are', 'added', ['deducted', 'ignored', 'added to the cash book'], 'They have not yet reduced the bank balance'),
                ('Starting with the updated cash book balance, outstanding lodgements are', 'deducted', ['added', 'ignored', 'debited in the cash book'], 'They have not yet increased the bank balance'),
                ('Updated cash book $4,500; unpresented cheques $1,200; outstanding lodgements $800. The bank statement balance is', '$4,900', ['$4,100', '$6,500', '$2,500'], '4,500 + 1,200 − 800'),
                ('A bank reconciliation statement is', 'a statement explaining the difference between the cash book balance and the bank statement balance', ['a ledger account', 'a statement sent by the bank', 'part of the double entry'], 'Not part of the double-entry system'),
                ('Which balance appears in the statement of financial position?', 'The updated cash book balance', ['The bank statement balance', 'The average of the two', 'The balance before updating'], 'The cash book records all transactions')],
          exps=[('Explain why unpresented cheques are added to the cash book balance in a bank reconciliation statement.', 'They have reduced the cash book balance but not yet the bank\'s balance, so adding them back gives the balance shown by the bank.', 'Deducted in cash book, not yet by bank [1]; add back to reach bank figure [1] [2]'),
                ('State two benefits of preparing a bank reconciliation statement.', 'Detects errors in the cash book or by the bank; identifies unrecorded items; helps detect fraud; confirms the correct bank balance.', 'Any two [1 each] [2]')],
          disc=[('Discuss whether {f} needs to prepare bank reconciliations now that it can view its bank account online every day.', 'Online access helps update the cash book quickly, but a formal reconciliation is still needed to detect errors, fraud and timing differences at the year end.', 'Online benefit [1]; reconciliation still needed [1]; judgement [1] [3]')])


@spec(t10_3)
def t103_brs(r, D):
    f = firm(r)
    cb, its, xs, upd = _cb_update(r, max(2, D - 1))
    up = step(r, 300, 3000, 10)
    ol = step(r, 200, 2500, 10)
    bs = upd + up - ol
    txt = [d.format(x=m(x)) for (d, _, _), x in zip(its, xs)]
    if D <= 2:
        setup = f'The updated cash book of {f} shows a bank balance of {m(upd)} at 30 June. Cheques of {m(up)} sent to suppliers have not yet been presented, and takings of {m(ol)} paid in on 30 June have not yet been credited by the bank.'
        parts = [('Prepare a bank reconciliation statement and calculate the balance shown on the bank statement.', f'{m(bs)}', f'{m(upd)} + {m(up)} − {m(ol)} = {m(bs)} [1 each adjustment]; {m(bs)} [1] [3]')]
    else:
        setup = (f'At 30 June the cash book of {f} showed a debit balance of {m(cb)}. Comparison with the bank statement revealed: {lst(txt)}. In addition, cheques of {m(up)} sent to suppliers had not yet been presented, and takings of {m(ol)} paid in on 30 June did not appear on the statement.')
        parts = [('Calculate the updated cash book balance.', m(upd), f'{m(cb)}' + ''.join(f' {"+" if s > 0 else "−"} {m(x)}' for (_, _, s), x in zip(its, xs)) + f' = {m(upd)} [2]'),
                 ('Prepare a bank reconciliation statement to find the balance on the bank statement.', m(bs), f'{m(upd)} + unpresented {m(up)} [1] − lodgements {m(ol)} [1] = {m(bs)} [1] [3]')]
    parts.append(('State the bank balance to be shown in the statement of financial position.', f'{m(upd)} (the updated cash book balance)', f'{m(upd)} [1]'))
    wrong = upd - up + ol
    c, ds = num_opts(m, bs, [wrong, upd, upd + up + ol])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What balance should the bank statement show?', c, ds, f'{m(upd)} + {m(up)} − {m(ol)} = {m(bs)}'),
            'err': (f'calculated the bank statement balance as {m(wrong)}', 'unpresented cheques were deducted and outstanding lodgements added; starting from the cash book, unpresented cheques are added back and lodgements deducted', m(bs), f'{m(upd)} + {m(up)} − {m(ol)}', 'bank statement balance')}


CHAPTERS[10] = [t10_1, t10_2, t10_3]


# ===================================================================== 11 Control accounts
CTRL_CLASS = [('credit sales', 'sales ledger control account – debit'), ('cash received from credit customers', 'sales ledger control account – credit'), ('discounts allowed', 'sales ledger control account – credit'),
              ('sales returns', 'sales ledger control account – credit'), ('irrecoverable debts written off', 'sales ledger control account – credit'), ('dishonoured cheques', 'sales ledger control account – debit'),
              ('credit purchases', 'purchases ledger control account – credit'), ('payments to suppliers', 'purchases ledger control account – debit'), ('discounts received', 'purchases ledger control account – debit'),
              ('purchases returns', 'purchases ledger control account – debit'), ('cash sales', 'neither control account'), ('trade discount', 'neither control account'),
              ('the allowance for doubtful debts', 'neither control account'), ('a contra (set-off) between ledgers', 'debit purchases ledger control, credit sales ledger control')]

t11_1 = A(11, 'Purpose of sales and purchases ledger control accounts', ['purpose of sales and purchases ledger control accounts', 'purpose of control accounts', 'sales ledger control'],
          mcqs=[('The main purpose of a control account is to', 'check the arithmetical accuracy of a ledger', ['record cash transactions', 'replace the personal ledgers', 'calculate profit'], 'Total of individual balances should equal the control balance'),
                ('Which item appears on the credit side of a sales ledger control account?', 'Discounts allowed', ['Credit sales', 'Dishonoured cheques', 'Interest charged on overdue accounts'], 'Reduces amounts owed by customers'),
                ('Which item does NOT appear in a sales ledger control account?', 'Cash sales', ['Sales returns', 'Irrecoverable debts', 'Cash received from credit customers'], 'No receivable arises'),
                ('Which item appears on the debit side of a purchases ledger control account?', 'Discounts received', ['Credit purchases', 'Interest charged by suppliers', 'Refunds from suppliers'], 'Reduces amounts owed to suppliers'),
                ('Control accounts can help to', 'locate errors in a particular ledger and deter fraud', ['prevent all errors', 'calculate depreciation', 'value inventory'], 'Narrow down where an error is')],
          exps=[('Explain two benefits of keeping control accounts.', 'They check the accuracy of each ledger so errors are located quickly; totals of receivables and payables are available quickly for the trial balance; they act as a check against fraud if kept by a different person.', 'Any two benefits with explanation [1 each] [2]'),
                ('Explain why the allowance for doubtful debts is not entered in the sales ledger control account.', 'It is an estimate that does not relate to any individual customer\'s account, so it is not in the sales ledger; the control account must agree with the ledger total.', 'Not in individual accounts [1]; control must agree with ledger [1] [2]')],
          disc=[('Discuss whether a small business such as {f} needs control accounts if it uses accounting software.', 'Software posts both sides automatically, reducing arithmetic errors, but control accounts still summarise receivables/payables and help detect fraud or input errors.', 'Software reduces errors [1]; still useful summary/fraud check [1]; judgement [1] [3]')])


@spec(t11_1, typ='short')
def t111_class(r, D):
    f = firm(r)
    k = 3 if D <= 2 else (4 if D == 3 else 6)
    its = r.sample(CTRL_CLASS, k)
    setup = f'The bookkeeper of {f} is preparing control accounts. The following items appear in the books: {lst([x[0] for x in its])}.'
    parts = [('State the control account (and side) in which each item is entered, or "neither".', '; '.join(f'({ROM[i]}) {w}' for i, (_, w) in enumerate(its)), '; '.join(f'({ROM[i]}) {w} [1]' for i, (_, w) in enumerate(its)) + f' [{k}]'),
             ('Explain the purpose of a sales ledger control account.', 'It summarises all transactions with credit customers so its balance can be checked against the total of the individual customer balances, locating errors and deterring fraud.', 'Summary/total of receivables [1]; check against ledger/locate errors [1] [2]')]
    o = r.choice(CTRL_CLASS)
    others = list({w for _, w in CTRL_CLASS if w != o[1]})
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'Where is the item "{o[0]}" recorded?', cap1(o[1]), [cap1(x) for x in r.sample(others, 3)], f'{o[0]}: {o[1]}'),
            'err': None}


def _slca(r, D):
    d = {'ob': step(r, 5000, 30000, 10), 'cs': step(r, 30000, 120000, 10), 'cr': 0, 'da': step(r, 200, 1500, 10), 'sr': step(r, 500, 4000, 10)}
    d['bd'] = step(r, 200, 2000, 10) if D >= 2 else 0
    d['dc'] = step(r, 200, 1500, 10) if D >= 3 else 0
    d['ct'] = step(r, 200, 1500, 10) if D >= 4 else 0
    d['cr'] = step(r, int(d['cs'] * 0.75), int(d['cs'] * 0.95), 10)
    d['cb'] = d['ob'] + d['cs'] + d['dc'] - d['cr'] - d['da'] - d['sr'] - d['bd'] - d['ct']
    return d


t11_2 = A(11, 'Preparing control accounts from given information', ['preparing control accounts from given information', 'preparing control accounts', 'purchases ledger control'],
          mcqs=[('Opening receivables $8,000, credit sales $40,000, cash received $36,000, discounts allowed $500. Closing receivables are', '$11,500', ['$12,500', '$12,000', '$4,500'], '8,000 + 40,000 − 36,000 − 500'),
                ('A dishonoured cheque from a customer is entered in the sales ledger control account on the', 'debit side', ['credit side', 'it is not entered', 'either side'], 'Debt reinstated'),
                ('The source of the credit sales figure in the sales ledger control account is the', 'sales journal total', ['cash book', 'sales returns journal', 'general journal'], 'Totals from books of prime entry'),
                ('Payments to suppliers are entered in the purchases ledger control account on the', 'debit side', ['credit side', 'they are not entered', 'either side'], 'Reduce the liability'),
                ('A credit balance on a sales ledger control account may arise because', 'a customer has overpaid', ['a customer owes money', 'goods were sold for cash', 'discount was received'], 'The business owes the customer')],
          exps=[('Explain why the closing balance of the sales ledger control account may not agree with the total of the sales ledger balances.', 'Errors in posting individual accounts, casting errors in the books of prime entry used for the control account, or items such as contras omitted from one record.', 'Individual posting errors [1]; casting/omission errors [1] [2]'),
                ('State the source of the figures for cash received and discounts allowed in a sales ledger control account.', 'The cash book: the bank/cash column total of receipts from customers and the discount allowed column total.', 'Cash book [1]; discount column [1] [2]')],
          disc=[('Assess the credit control of {f} by comparing cash received with credit sales.', 'If cash received is a high proportion of credit sales and closing receivables are stable, credit control is good; rising receivables suggest slow payers.', 'Uses the figures [1]; interprets trend [1]; judgement [1] [3]')])


@spec(t11_2)
def t112_slca(r, D):
    f = firm(r)
    if r.random() < 0.5:
        d = _slca(r, D)
        its = [f'balance at 1 April {m(d["ob"])}', f'credit sales {m(d["cs"])}', f'cash and cheques received from customers {m(d["cr"])}', f'discounts allowed {m(d["da"])}', f'sales returns {m(d["sr"])}'] + \
            ([f'irrecoverable debts written off {m(d["bd"])}'] if d['bd'] else []) + ([f'dishonoured cheques {m(d["dc"])}'] if d['dc'] else []) + ([f'contra entries with the purchases ledger {m(d["ct"])}'] if d['ct'] else [])
        if D >= 3:
            its.append(f'cash sales {m(step(r, 2000, 9000, 10))}')
        setup = f'The following information relates to the sales ledger of {f} for the year ended 31 March: ' + '; '.join(its) + '.'
        w = f'{m(d["ob"])} + {m(d["cs"])}' + (f' + {m(d["dc"])}' if d['dc'] else '') + f' − {m(d["cr"])} − {m(d["da"])} − {m(d["sr"])}' + (f' − {m(d["bd"])}' if d['bd'] else '') + (f' − {m(d["ct"])}' if d['ct'] else '') + f' = {m(d["cb"])}'
        parts = [('Prepare the sales ledger control account and find the closing balance.', f'{m(d["cb"])} debit', f'Debit: b/d, credit sales' + (', dishonoured cheques' if d['dc'] else '') + ' [1]; credit: receipts, discounts, returns' + (', irrecoverable debts' if d['bd'] else '') + (', contra' if d['ct'] else '') + f' [1]; {w} [1]; balance c/d [1] [4]')]
        if D >= 3:
            parts.append(('State why the cash sales are not entered in the control account.', 'Cash sales create no trade receivable, so they do not appear in the sales ledger.', 'No receivable [1]'))
        wrong = d['cb'] + 2 * d['da']
        c, ds = num_opts(m, d['cb'], [wrong, d['cb'] + 2 * d['sr'], d['ob'] + d['cs'] - d['cr']])
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
                'mcq': ('What is the closing balance on the sales ledger control account?', c, ds, w),
                'err': (f'calculated the closing balance as {m(wrong)}', 'discounts allowed were debited instead of credited; they reduce the amounts owed by customers', m(d['cb']), w.split(' = ')[0], 'closing balance')}
    ob, cp = step(r, 4000, 25000, 10), step(r, 25000, 100000, 10)
    pay = step(r, int(cp * 0.75), int(cp * 0.95), 10)
    dr_, pr = step(r, 200, 1500, 10), step(r, 300, 3000, 10)
    ct = step(r, 200, 1500, 10) if D >= 3 else 0
    cb = ob + cp - pay - dr_ - pr - ct
    setup = f'Information for the purchases ledger of {f} for the year ended 30 September: balance at 1 October {m(ob)} (credit); credit purchases {m(cp)}; payments to suppliers {m(pay)}; discounts received {m(dr_)}; purchases returns {m(pr)}' + (f'; contra entries with the sales ledger {m(ct)}' if ct else '') + '.'
    w = f'{m(ob)} + {m(cp)} − {m(pay)} − {m(dr_)} − {m(pr)}' + (f' − {m(ct)}' if ct else '') + f' = {m(cb)}'
    parts = [('Prepare the purchases ledger control account and find the closing balance.', f'{m(cb)} credit', f'Credit: b/d, purchases [1]; debit: payments, discounts, returns' + (', contra' if ct else '') + f' [1]; {w} [1] [3]'),
             ('State where the closing balance appears in the statement of financial position.', 'Current liabilities (trade payables).', 'Current liability [1]')]
    wrong = cb + 2 * dr_
    c, ds = num_opts(m, cb, [wrong, cb + 2 * pr, ob + cp - pay])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the closing balance on the purchases ledger control account?', c, ds, w),
            'err': (f'calculated the closing balance as {m(wrong)}', 'discounts received were credited (added) instead of debited; they reduce the amounts owed to suppliers', m(cb), w.split(' = ')[0], 'closing balance')}


t11_3 = A(11, 'Contra entries and reconciling control accounts with ledgers', ['contra entries and reconciling control accounts with ledgers', 'contra entries', 'reconciling control accounts'],
          mcqs=[('A contra entry between the sales and purchases ledgers is recorded by', 'debiting the purchases ledger control account and crediting the sales ledger control account', ['debiting the sales ledger control and crediting purchases ledger control', 'debiting bank and crediting sales', 'debiting both control accounts'], 'Set-off reduces both the receivable and the payable'),
                ('A contra arises when', 'a business both buys from and sells to the same person', ['a customer pays by cheque', 'goods are returned', 'a debt is written off'], 'Amounts are set off'),
                ('The sales journal was undercast by $300. To reconcile, the', 'control account balance is increased by $300', ['list of ledger balances is increased by $300', 'list of balances is reduced by $300', 'control account is reduced by $300'], 'The journal total feeds the control account'),
                ('A credit sale of $250 was posted to the customer\'s account as $520. The correction affects', 'only the list of sales ledger balances', ['only the control account', 'both the control account and the list', 'neither'], 'Individual posting error'),
                ('A contra of $400 was omitted from both the control accounts. The sales ledger control balance must be', 'reduced by $400', ['increased by $400', 'left unchanged', 'increased by $800'], 'Credit SLCA')],
          exps=[('Explain why a contra entry is made.', 'When a business owes a supplier who is also its customer, the amounts are set off so that only the net amount is paid, saving cash transfers.', 'Same person customer and supplier [1]; net settlement [1] [2]'),
                ('Explain why errors in the books of prime entry affect the control account but not the individual ledger accounts.', 'Control accounts are written up from the totals of the books of prime entry, while individual accounts are posted from each line; a casting error affects only the total.', 'Control from totals [1]; ledger from individual entries [1] [2]')],
          disc=[('Explain why reconciling the control account with the ledger is a useful check for {f}.', 'It locates errors and can reveal fraud such as fictitious accounts, giving confidence in the receivables/payables figures.', 'Locate errors [1]; fraud/confidence [1] [2]')])


@spec(t11_3)
def t113_rec(r, D):
    f = firm(r)
    cbal = step(r, 15000, 60000, 10)
    lbal = cbal + step(r, -2000, 2000, 10)
    a, b = pp(r, 2)
    pool = [('The sales journal was undercast by {x}.', 'C', 1), ('A contra entry of {x} had not been entered in the control account.', 'C', -1),
            ('Discounts allowed of {x} were entered on the debit side of the control account.', 'C', '-2'), ('An irrecoverable debt of {x} had been written off in the customer\'s account but not in the control account.', 'C', -1),
            (f'A balance of {{x}} owed by {a} had been omitted from the list of balances.', 'L', 1), (f'A credit sale of {{y}} to {b} was posted to the customer\'s account as {{x}}.', 'L', 'yx'),
            ('A customer\'s debit balance of {x} had been listed as a credit balance.', 'L', '2')]
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    its = r.sample(pool, k)
    cadj = ladj = 0
    txt, keys = [], []
    for t, w, s in its:
        x = step(r, 100, 1500, 10)
        sx = str(x)
        y = int(sx[:-2] + sx[-1] + sx[-2]) if sx[-1] != sx[-2] else x + 90
        txt.append(t.format(x=m(x), y=m(y)))
        if s == 'yx':
            v = y - x
        elif s == '-2':
            v = -2 * x
        elif s == '2':
            v = 2 * x
        else:
            v = s * x
        if w == 'C':
            cadj += v
        else:
            ladj += v
        keys.append(f'{"control" if w == "C" else "list"} {"+" if v >= 0 else "−"}{m(abs(v))}')
    cc, lc = cbal + cadj, lbal + ladj
    if cc != lc:
        lbal += cc - lc
        lc = cc
    setup = f'The sales ledger control account of {f} showed a debit balance of {m(cbal)} at 31 December, but the total of the balances in the sales ledger was {m(lbal)}. The following errors were found: {lst(txt)}.'
    parts = [('Calculate the corrected sales ledger control account balance.', m(cc), f'{m(cbal)} adjusted: ' + '; '.join(k_ for k_ in keys if k_.startswith('control')) + f' [1 per item]; = {m(cc)} [1] [{1 + sum(1 for k_ in keys if k_.startswith("control"))}]'),
             ('Calculate the corrected total of the sales ledger balances.', m(lc), f'{m(lbal)} adjusted: ' + '; '.join(k_ for k_ in keys if k_.startswith('list')) + f' [1 per item]; = {m(lc)} [1] [{1 + sum(1 for k_ in keys if k_.startswith("list"))}]'),
             ('State which error affects the control account but not the individual customer accounts, and explain why.', 'Errors in book-of-prime-entry totals or omitted from the control account only, because the control account is written up from totals.', 'Correct error identified [1]; reason – totals [1] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the corrected control account balance?', *num_opts(m, cc, [cbal - cadj, cbal, lbal]), f'{m(cbal)} adjusted by {m(cadj)} = {m(cc)}'),
            'err': (f'corrected the control account balance to {m(cbal - cadj)}', 'the control account adjustments were made in the wrong direction', m(cc), f'{m(cbal)} {"+" if cadj >= 0 else "−"} {m(abs(cadj))}', 'control account balance') if cadj else None}


CHAPTERS[11] = [t11_1, t11_2, t11_3]


# ===================================================================== 12 Correction of errors and suspense accounts
def _errs(r, susp_only=False, none_susp=False):
    a, b = pp(r, 2)

    def amt():
        x = step(r, 100, 3000, 10)
        y = x + r.choice([90, 900, 180, 270]) if r.random() < 0.5 else max(10, x - r.choice([90, 180, 270]))
        return x, min(x, y), max(x, y)
    F = [
        lambda x, lo, hi: (f'Office equipment costing {m(x)} was debited to the purchases account.', 'principle', f'Dr Office equipment, Cr Purchases {m(x)}', 0, x),
        lambda x, lo, hi: (f'Rent received of {m(x)} was credited to the commission received account.', 'commission', f'Dr Commission received, Cr Rent received {m(x)}', 0, 0),
        lambda x, lo, hi: (f'A credit sale of {m(x)} to {a} was debited to the account of {b}.', 'commission', f'Dr {a}, Cr {b} {m(x)}', 0, 0),
        lambda x, lo, hi: (f'Repairs to a van costing {m(x)} were debited to the motor vehicles account.', 'principle', f'Dr Motor vehicle repairs, Cr Motor vehicles {m(x)}', 0, -x),
        lambda x, lo, hi: (f'The owner\'s private cash withdrawal of {m(x)} was debited to the wages account.', 'principle', f'Dr Drawings, Cr Wages {m(x)}', 0, x),
        lambda x, lo, hi: (f'Interest received of {m(x)} was not recorded in the books.', 'omission', f'Dr Bank, Cr Interest received {m(x)}', 0, x),
        lambda x, lo, hi: (f'A purchase invoice for {m(hi)} was entered in the purchases journal as {m(lo)}.', 'original entry', f'Dr Purchases, Cr supplier {m(hi - lo)}', 0, -(hi - lo)),
        lambda x, lo, hi: (f'Cash sales of {m(x)} were debited to sales and credited to cash.', 'complete reversal', f'Dr Cash, Cr Sales {m(2 * x)}', 0, 2 * x),
        lambda x, lo, hi: (f'The sales journal was undercast by {m(x)}.', 'casting', f'Dr Suspense, Cr Sales {m(x)}', x, x),
        lambda x, lo, hi: (f'Wages of {m(lo)} were correctly entered in the cash book but debited to the wages account as {m(hi)}.', 'transposition / wrong amount on one side', f'Dr Suspense, Cr Wages {m(hi - lo)}', hi - lo, hi - lo),
        lambda x, lo, hi: (f'Discounts allowed of {m(x)} were not posted to the discounts allowed account.', 'single-sided omission', f'Dr Discounts allowed, Cr Suspense {m(x)}', -x, -x),
        lambda x, lo, hi: (f'Rent paid of {m(x)} was entered on the credit side of the rent account.', 'wrong side (two credits)', f'Dr Rent, Cr Suspense {m(2 * x)}', -2 * x, -2 * x),
        lambda x, lo, hi: (f'Purchases returns of {m(x)} were debited to the purchases returns account.', 'wrong side (two debits)', f'Dr Suspense, Cr Purchases returns {m(2 * x)}', 2 * x, 2 * x),
        lambda x, lo, hi: (f'A payment of {m(x)} to the supplier {a} was not posted to {a}\'s account.', 'single-sided omission', f'Dr {a}, Cr Suspense {m(x)}', -x, 0),
    ]
    E = [g(*amt()) for g in F]
    if susp_only:
        E = [e for e in E if e[3]]
    if none_susp:
        E = [e for e in E if not e[3]]
    return E


t12_1 = A(12, 'Errors not revealed by the trial balance', ['errors not revealed by the trial balance', 'errors not revealed', 'types of error'],
          mcqs=[('Wages paid were debited to the drawings account. This is an error of', 'principle', ['commission', 'omission', 'original entry'], 'Expense recorded as drawings – wrong class'),
                ('A sales invoice of $380 was recorded in the sales journal as $830. This is an error of', 'original entry', ['transposition in one account', 'commission', 'compensating'], 'Wrong figure in the book of prime entry'),
                ('Which error would cause a suspense account to be opened?', 'An expense posted to the expense account only', ['A complete reversal of entries', 'A transaction omitted completely', 'An error of principle'], 'One-sided entry'),
                ('An invoice was not entered in the books at all. This is an error of', 'omission', ['commission', 'principle', 'reversal'], 'Both sides missing'),
                ('Purchases were overcast by $100 and sales were also overcast by $100. This is', 'a compensating error', ['an error of commission', 'an error of original entry', 'a casting error that is revealed'], 'They cancel out')],
          exps=[('Explain the difference between an error of omission and an error of original entry.', 'Omission: the transaction is not recorded at all; original entry: it is recorded in both accounts but with the wrong amount (from the book of prime entry).', 'Omission – not recorded [1]; original entry – wrong amount both sides [1] [2]'),
                ('Explain why errors not revealed by the trial balance may still affect profit.', 'Errors such as principle (capital treated as revenue) or omission of income/expenses change the income statement figures even though debits equal credits.', 'Example of profit-affecting error [1]; explanation [1] [2]')],
          disc=[('Suggest two controls {f} could use to reduce the risk of undetected errors.', 'Control accounts and bank reconciliations; division of duties; checking invoices against orders; regular review by a supervisor.', 'Two controls [1 each] [2]')])


@spec(t12_1, typ='short')
def t121_types(r, D):
    f = firm(r)
    E = _errs(r, none_susp=True)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    es = r.sample(E, k)
    setup = f'After the trial balance of {f} agreed, the following errors were discovered: {lst([e[0] for e in es])}.'
    parts = [('Name the type of error in each case.', '; '.join(f'({ROM[i]}) error of {e[1]}' for i, e in enumerate(es)), '; '.join(f'({ROM[i]}) {e[1]} [1]' for i, e in enumerate(es)) + f' [{k}]'),
             ('Prepare journal entries to correct the errors. Narratives are not required.', '; '.join(f'({ROM[i]}) {e[2]}' for i, e in enumerate(es)), '; '.join(f'({ROM[i]}) {e[2]} [1]' for i, e in enumerate(es)) + f' [{k}]'),
             ('Explain why none of these errors caused the trial balance to disagree.', 'In each case the debit entries still equal the credit entries.', 'Equal debits and credits [1]')]
    e0 = es[0]
    types = ['principle', 'commission', 'omission', 'original entry', 'complete reversal', 'compensating']
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What type of error is (i)?', f'Error of {e0[1]}', [f'Error of {t}' for t in types if t != e0[1]][:4], f'{e0[0]} → error of {e0[1]}'),
            'err': (f'described error (i) as an error of {"commission" if e0[1] != "commission" else "principle"}', f'it is an error of {e0[1]}', f'error of {e0[1]}; correction {e0[2]}', 'consider whether the account is the wrong class, the wrong account of the right class, or missing', 'classification')}


t12_2 = A(12, 'Journal entries to correct errors', ['journal entries to correct errors', 'correcting errors', 'journal entries to correct'],
          mcqs=[('Office furniture of $900 was debited to office expenses. The correcting entry is', 'Dr Office furniture $900, Cr Office expenses $900', ['Dr Office expenses $900, Cr Office furniture $900', 'Dr Office furniture $900, Cr Suspense $900', 'Dr Suspense $900, Cr Office expenses $900'], 'Move the debit to the correct account'),
                ('Cash sales of $200 were debited to sales and credited to cash. The correction is', 'Dr Cash $400, Cr Sales $400', ['Dr Cash $200, Cr Sales $200', 'Dr Sales $400, Cr Cash $400', 'Dr Suspense $400, Cr Sales $400'], 'Twice the amount to reverse and re-record'),
                ('A payment to Lee of $150 was debited to Leigh\'s account. The correction is', 'Dr Lee, Cr Leigh $150', ['Dr Leigh, Cr Lee $150', 'Dr Lee, Cr Bank $150', 'Dr Suspense, Cr Leigh $150'], 'Error of commission'),
                ('Why is a narrative included with a correcting journal entry?', 'To explain the error being corrected for audit purposes', ['To show the date of the trial balance', 'Because it changes the amount', 'It is not needed'], 'Audit trail'),
                ('A purchase of $480 was recorded throughout as $840. The correction is', 'Dr Supplier $360, Cr Purchases $360', ['Dr Purchases $360, Cr Supplier $360', 'Dr Supplier $840, Cr Purchases $840', 'Dr Suspense $360, Cr Purchases $360'], 'Reduce both sides by 360')],
          exps=[('Explain why errors are corrected through the general journal rather than by altering the original entries.', 'The journal gives a permanent, authorised record of each correction with a narrative, keeping an audit trail; crossing out entries could hide fraud.', 'Audit trail/authorisation [1]; altering records hides errors/fraud [1] [2]'),
                ('Explain why an error of complete reversal is corrected using twice the original amount.', 'The first amount cancels the wrong entries and the second records the correct entries.', 'Cancel wrong entry [1]; record correct entry [1] [2]')],
          disc=[('Explain the effect on the statement of financial position of the first error if it is not corrected.', 'Depends on the accounts involved: e.g. capital expenditure treated as revenue understates non-current assets and capital.', 'Identify accounts affected [1]; direction of misstatement [1] [2]')])


@spec(t12_2)
def t122_jnl(r, D):
    f = firm(r)
    E = _errs(r, none_susp=D <= 2)
    k = 2 if D <= 3 else 3
    es = r.sample(E, k)
    setup = f'The following errors were found in the books of {f}: {lst([e[0] for e in es])}.' + (' A suspense account was opened for the trial balance difference.' if any(e[3] for e in es) else '')
    parts = [('Prepare the journal entries to correct these errors. Narratives are not required.', '; '.join(f'({ROM[i]}) {e[2]}' for i, e in enumerate(es)), '; '.join(f'({ROM[i]}) {e[2]} [2]' for i, e in enumerate(es)) + f' [{2 * k}]'),
             ('State the effect on profit of correcting error (i).', 'No effect on profit' if not es[0][4] else f'Profit {"increases" if es[0][4] > 0 else "decreases"} by {m(abs(es[0][4]))}', '1 mark for direction and amount [1]')]
    e0 = es[0]
    dr_acc, rest = e0[2][3:].split(', Cr ')
    cr_acc, amt = rest.rsplit(' ', 1)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'err': (f'corrected error (i) with the entry Dr {cr_acc}, Cr {dr_acc} {amt}', 'the debit and credit were reversed, which doubles the error instead of correcting it', e0[2], 'debit the account that is understated (or should have been debited); credit the account wrongly debited', 'correcting entry')}


t12_3 = A(12, 'Suspense accounts and their clearance', ['suspense accounts and their clearance', 'suspense account', 'suspense'],
          mcqs=[('A suspense account is opened when', 'the trial balance totals do not agree', ['a customer\'s debt is doubtful', 'the bank statement differs from the cash book', 'goods are returned'], 'Temporary account for the difference'),
                ('The trial balance debit total is $250 more than the credit total. The suspense account will have', 'a credit balance of $250', ['a debit balance of $250', 'a credit balance of $500', 'no balance'], 'The suspense balance is entered on the shorter side'),
                ('Discounts allowed of $60 were not posted to the discounts allowed account. The correction is', 'Dr Discounts allowed $60, Cr Suspense $60', ['Dr Suspense $60, Cr Discounts allowed $60', 'Dr Discounts allowed $120, Cr Suspense $120', 'Dr Customer $60, Cr Suspense $60'], 'One-sided omission'),
                ('Which error would NOT be corrected through the suspense account?', 'An error of commission', ['A casting error in the sales journal', 'A posting to only one account', 'Two debit entries'], 'Commission does not affect TB balance'),
                ('After all errors are corrected, the suspense account should', 'have a nil balance', ['equal the trial balance difference', 'be transferred to capital', 'show a debit balance'], 'It is a temporary account')],
          exps=[('Explain why a suspense account should not appear in the final statement of financial position.', 'It is a temporary account for unidentified errors; the errors should be found and corrected so the balance is cleared before final statements are prepared.', 'Temporary/unidentified errors [1]; should be cleared [1] [2]'),
                ('Explain how an error where an amount is entered on the wrong side of an account affects the suspense account.', 'Both entries are on the same side, so the TB is out by twice the amount; the correction posts twice the amount through suspense.', 'Two entries same side [1]; twice the amount [1] [2]')],
          disc=[('Discuss whether {f} should prepare its financial statements while a balance remains on the suspense account.', 'Small unexplained balances may be immaterial, but they may hide significant compensating errors or fraud; the errors should be investigated first.', 'Materiality [1]; risk of hidden errors [1]; judgement [1] [3]')])


@spec(t12_3)
def t123_susp(r, D):
    f = firm(r)
    E = _errs(r, susp_only=True)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    es = r.sample(E, min(k, len(E)))
    if D >= 4:
        es = es[:3] + r.sample(_errs(r, none_susp=True), 1)
    net = sum(e[3] for e in es)
    if net == 0:
        return None
    side = 'credit' if net > 0 else 'debit'
    tb = 'debit' if net > 0 else 'credit'
    setup = f'The trial balance of {f} did not agree: the {tb} column exceeded the other by {m(abs(net))}, and the difference was entered in a suspense account. The following errors were then found: {lst([e[0] for e in es])}.'
    parts = [('Prepare journal entries to correct the errors.', '; '.join(f'({ROM[i]}) {e[2]}' for i, e in enumerate(es)), '; '.join(f'({ROM[i]}) {e[2]} [1]' for i, e in enumerate(es)) + f' [{len(es)}]'),
             ('Prepare the suspense account, showing the opening balance and the corrections.', f'Opening {side} balance {m(abs(net))}; corrections: ' + '; '.join(f'({ROM[i]}) {"Dr" if e[3] > 0 else "Cr"} {m(abs(e[3]))}' for i, e in enumerate(es) if e[3]) + '; account closes with nil balance',
              f'Opening balance {m(abs(net))} {side} [1]; entries on correct sides [1 each]; nil balance [1] [{2 + sum(1 for e in es if e[3])}]')]
    c, ds = num_opts(m, abs(net), [sum(abs(e[3]) for e in es), abs(net) * 2, abs(net) + es[0][3]])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What was the opening balance on the suspense account?', f'{c} {side}', [f'{c} {"debit" if side == "credit" else "credit"}'] + [f'{d} {side}' for d in ds[:3]], f'Sum of suspense corrections = {m(net)}; opening balance {side}'),
            'err': (f'entered the opening suspense balance of {m(abs(net))} on the {"debit" if side == "credit" else "credit"} side', f'the suspense balance is entered on the side that makes the trial balance agree – the {tb} column was larger, so suspense is a {side} balance', f'{m(abs(net))} {side}', 'suspense corrections must clear the balance to nil', 'suspense balance')}


t12_4 = A(12, 'Effect of corrections on profit and the statement of financial position', ['effect of corrections on profit and the statement of financial position', 'effect of corrections on profit', 'corrected profit'],
          mcqs=[('Draft profit $30,000. Equipment of $2,000 was debited to purchases. Corrected profit is', '$32,000', ['$28,000', '$30,000', '$34,000'], 'Purchases overstated → profit understated'),
                ('Which correction does NOT change profit?', 'Correcting a payment posted to the wrong supplier\'s account', ['Correcting an undercast sales journal', 'Recording omitted interest received', 'Reclassifying drawings charged to wages'], 'Both accounts are in the SFP'),
                ('Rent paid of $500 was entered on the credit side of the rent account. Correcting it will', 'reduce profit by $1,000', ['increase profit by $1,000', 'reduce profit by $500', 'not affect profit'], 'Rent expense increases by 2 × 500'),
                ('Drawings of $700 were debited to wages. The correction will', 'increase profit by $700 and reduce capital by drawings $700', ['reduce profit by $700', 'not affect profit', 'increase both profit and capital by $1,400'], 'Wages fall; drawings rise'),
                ('A casting error in the sales journal undercast sales by $150. Correcting it will', 'increase profit by $150', ['reduce profit by $150', 'not affect profit', 'increase trade receivables only'], 'Sales increase')],
          exps=[('Explain why some corrections of errors affect profit and others do not.', 'Only corrections involving income or expense accounts change profit; corrections between asset, liability or capital accounts affect only the statement of financial position.', 'Income/expense accounts affect profit [1]; SFP-only corrections do not [1] [2]'),
                ('Explain how correcting an error of principle (capital expenditure treated as revenue) affects the financial statements.', 'Expenses fall so profit rises; non-current assets rise; depreciation may then need to be charged.', 'Profit up [1]; NCA up/depreciation [1] [2]')],
          disc=[('Discuss why it matters to {f}\'s bank that errors are corrected before the accounts are submitted.', 'Profit and asset figures affect lending decisions and loan covenants; uncorrected errors make the statements unreliable.', 'Bank relies on figures [1]; reliability/covenants [1] [2]')])


@spec(t12_4)
def t124_prof(r, D):
    f = firm(r)
    dp_ = step(r, 15000, 60000, 10)
    E = _errs(r)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    es = r.sample(E, k)
    cp_ = dp_ + sum(e[4] for e in es)
    setup = f'{f} calculated a draft profit of {m(dp_)} for the year. The following errors were then discovered: {lst([e[0] for e in es])}.'
    parts = [('Prepare a statement of corrected profit for the year.', m(cp_), f'{m(dp_)}' + ''.join(f'; ({ROM[i]}) {"no effect" if not e[4] else ("+" if e[4] > 0 else "−") + m(abs(e[4]))}' for i, e in enumerate(es)) + f' [1 per error]; corrected profit {m(cp_)} [1] [{k + 1}]'),
             ('Prepare journal entries to correct errors (i) and (ii).', f'(i) {es[0][2]}; (ii) {es[1][2]}', f'(i) {es[0][2]} [1]; (ii) {es[1][2]} [1] [2]')]
    wrong = dp_ - sum(e[4] for e in es)
    c, ds = num_opts(m, cp_, [wrong, dp_, dp_ + sum(abs(e[4]) for e in es)])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the corrected profit?', c, ds, f'{m(dp_)} adjusted = {m(cp_)}'),
            'err': (f'calculated the corrected profit as {m(wrong)}', 'each adjustment was made in the wrong direction (e.g. reducing profit when an expense had been overstated)', m(cp_),
                    f'{m(dp_)}' + ''.join(f' {"+" if e[4] > 0 else "−"} {m(abs(e[4]))}' for e in es if e[4]), 'profit') if wrong != cp_ else None}


CHAPTERS[12] = [t12_1, t12_2, t12_3, t12_4]


# ===================================================================== 13 Incomplete records
t13_1 = A(13, 'Statement of affairs and profit from change in capital', ['statement of affairs and profit from change in capital', 'statement of affairs', 'change in capital'],
          mcqs=[('A statement of affairs is', 'a statement of assets and liabilities used to calculate capital when records are incomplete', ['a list of ledger balances', 'a bank reconciliation', 'an income statement for a club'], 'Capital = assets − liabilities'),
                ('Opening capital $30,000; closing capital $38,000; drawings $12,000; no capital introduced. Profit is', '$20,000', ['$8,000', '$4,000', '$50,000'], '38,000 − 30,000 + 12,000'),
                ('Capital introduced during the year is', 'deducted from the increase in capital to find profit', ['added to the increase in capital', 'ignored', 'treated as profit'], 'It is not earned'),
                ('A loss is indicated when', 'closing capital + drawings − capital introduced is less than opening capital', ['closing capital exceeds opening capital', 'drawings are high', 'there are no liabilities'], 'Net assets fell after adjusting'),
                ('Which is a limitation of calculating profit from the change in capital?', 'It does not show how the profit was made (no detail of sales and expenses)', ['It cannot be used by sole traders', 'It always overstates profit', 'It requires a full set of double-entry records'], 'Only the total is found')],
          exps=[('Explain why drawings are added to the change in capital when calculating profit.', 'Drawings reduced closing capital but were taken out of profit; adding them back gives the profit actually earned.', 'Drawings reduced capital [1]; added back to find profit earned [1] [2]'),
                ('Explain two disadvantages to a sole trader of not keeping full double-entry records.', 'Profit cannot be analysed by source; errors and fraud are harder to detect; the bank or tax authorities may not accept the figures; control of receivables and payables is difficult.', 'Any two [1 each] [2]')],
          disc=[('Advise {p} whether to start keeping full double-entry records.', 'Full records give detailed information, control and credibility with lenders, but cost time or bookkeeping fees; for a growing business the benefits usually outweigh the costs.', 'Benefits [1]; costs [1]; recommendation [1] [3]')])


@spec(t13_1)
def t131_soa(r, D):
    f, p = firm(r), pp(r)
    a1 = [('premises', step(r, 40000, 120000, 1000) if D >= 3 else 0), ('equipment', step(r, 5000, 30000, 100)), ('inventory', step(r, 3000, 15000, 100)),
          ('trade receivables', step(r, 1000, 9000, 100)), ('bank', step(r, 500, 6000, 10))]
    a2 = [(n, v if n == 'premises' else (v * 9 // 10 if n == 'equipment' else step(r, max(100, v // 2), v * 3 // 2, 10))) for n, v in a1]
    a1, a2 = [x for x in a1 if x[1]], [x for x in a2 if x[1]]
    l1 = [('trade payables', step(r, 1000, 8000, 100))] + ([('loan', step(r, 10000, 20000, 1000))] if D >= 4 else [])
    l2 = [(n, step(r, 1000, 8000, 100) if n == 'trade payables' else v - 2000) for n, v in l1]
    oc = sum(v for _, v in a1) - sum(v for _, v in l1)
    cc = sum(v for _, v in a2) - sum(v for _, v in l2)
    dr_ = step(r, 5000, 20000, 100)
    ci = step(r, 2000, 10000, 100) if D >= 3 else 0
    pr = cc - oc + dr_ - ci
    setup = (f'{p} does not keep full accounting records for {f}. At 1 January the business had ' + ', '.join(f'{n} {m(v)}' for n, v in a1 + l1) +
             f'. At 31 December it had ' + ', '.join(f'{n} {m(v)}' for n, v in a2 + l2) + f'. During the year {p} took drawings of {m(dr_)}' + (f' and paid in additional capital of {m(ci)}' if ci else '') + '.')
    parts = [('Calculate the capital at 1 January and at 31 December.', f'Opening {m(oc)}; closing {m(cc)}', f'Opening {m(oc)} [1]; closing {m(cc)} [1] [2]'),
             ('Calculate the profit or loss for the year.', f'{"Profit" if pr >= 0 else "Loss"} {m(abs(pr))}', f'{m(cc)} − {m(oc)} + drawings {m(dr_)}' + (f' − capital introduced {m(ci)}' if ci else '') + f' = {m(pr)} [2]')]
    wrong = cc - oc - dr_ + ci
    c, ds = num_opts(m, pr, [wrong, cc - oc, cc - oc + dr_ + ci])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What is the profit for the year?', c, ds, f'{m(cc)} − {m(oc)} + {m(dr_)} − {m(ci)} = {m(pr)}'),
            'err': (f'calculated the profit as {m(wrong)}', 'drawings were deducted and capital introduced added; drawings must be added back and capital introduced deducted', m(pr), f'{m(cc)} − {m(oc)} + {m(dr_)}' + (f' − {m(ci)}' if ci else ''), 'profit')}


t13_2 = A(13, 'Reconstructing accounts: receivables, payables and cash', ['reconstructing accounts: receivables, payables and cash', 'reconstructing accounts', 'credit sales', 'credit purchases'],
          mcqs=[('Opening receivables $4,000, closing receivables $5,500, cash received from customers $38,000. Credit sales are', '$39,500', ['$36,500', '$38,000', '$47,500'], '38,000 + 5,500 − 4,000'),
                ('Opening payables $3,000, closing payables $2,200, payments to suppliers $26,000. Credit purchases are', '$25,200', ['$26,800', '$26,000', '$31,200'], '26,000 + 2,200 − 3,000'),
                ('Total sales are found by', 'adding cash sales to credit sales', ['deducting cash sales from credit sales', 'adding receivables to cash received', 'adding purchases to gross profit'], 'Both types of sale'),
                ('Discounts allowed of $300 were given. In reconstructing the receivables account, this is', 'added to cash received to find credit sales', ['deducted from cash received', 'ignored', 'added to closing receivables twice'], 'Credit side item'),
                ('Takings are banked after paying wages of $200 a week in cash. To find total cash takings you must', 'add the cash payments to the amounts banked', ['deduct the payments from the amounts banked', 'ignore the payments', 'use only the bank statement'], 'Cash used before banking')],
          exps=[('Explain how a total trade receivables account is used to find credit sales.', 'Credit sales are the missing figure: closing receivables + cash received + discounts allowed + irrecoverable debts − opening receivables.', 'Missing figure in account [1]; correct formula [1] [2]'),
                ('Explain why cash taken from the till before banking must be added back to find total sales.', 'Payments made out of takings never reached the bank, so banked amounts understate the cash actually received from customers.', 'Takings used before banking [1]; bank understates sales [1] [2]')],
          disc=[('Discuss the risks to {f} of paying expenses out of the till before banking takings.', 'Payments may not be recorded, making sales understated and fraud easier; it weakens control over cash.', 'Unrecorded payments/sales understated [1]; fraud risk [1]; control point [1] [3]')])


@spec(t13_2)
def t132_rec(r, D):
    f, p = firm(r), pp(r)
    ob, cb = step(r, 2000, 9000, 10), step(r, 2000, 9000, 10)
    cr = step(r, 30000, 90000, 10)
    da = step(r, 100, 1200, 10) if D >= 2 else 0
    bd = step(r, 100, 1000, 10) if D >= 3 else 0
    cs_ = cr + da + bd + cb - ob
    cash = step(r, 5000, 20000, 10) if D >= 3 else 0
    op_, cp_ = step(r, 2000, 8000, 10), step(r, 2000, 8000, 10)
    pay = step(r, 20000, 60000, 10)
    drc = step(r, 100, 900, 10) if D >= 4 else 0
    pur = pay + drc + cp_ - op_
    setup = (f'{p} keeps only a cash book for {f}. For the year: trade receivables were {m(ob)} at the start and {m(cb)} at the end; {m(cr)} was received from credit customers' + (f' after allowing discounts of {m(da)}' if da else '') +
             (f'; irrecoverable debts of {m(bd)} were written off' if bd else '') + (f'; cash sales were {m(cash)}' if cash else '') +
             f'. Trade payables were {m(op_)} at the start and {m(cp_)} at the end; {m(pay)} was paid to suppliers' + (f' after deducting discounts received of {m(drc)}' if drc else '') + '.')
    parts = [('Calculate the credit sales for the year.', m(cs_), f'{m(cr)}' + (f' + {m(da)}' if da else '') + (f' + {m(bd)}' if bd else '') + f' + {m(cb)} − {m(ob)} = {m(cs_)} [2]'),
             ('Calculate the credit purchases for the year.', m(pur), f'{m(pay)}' + (f' + {m(drc)}' if drc else '') + f' + {m(cp_)} − {m(op_)} = {m(pur)} [2]')]
    if cash:
        parts.append(('Calculate the total revenue for the year.', m(cs_ + cash), f'{m(cs_)} + {m(cash)} = {m(cs_ + cash)} [1]'))
    wrong = cr + ob - cb + da + bd
    c, ds = num_opts(m, cs_, [wrong, cr, cr + cb])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What are the credit sales for the year?', c, ds, f'{m(cr)} + {m(da + bd)} + {m(cb)} − {m(ob)} = {m(cs_)}'),
            'err': (f'calculated credit sales as {m(wrong)}', 'the opening and closing receivables were used the wrong way round: closing receivables are added and opening receivables deducted', m(cs_), f'{m(cr + da + bd)} + {m(cb)} − {m(ob)}', 'credit sales') if wrong != cs_ else None}


t13_3 = A(13, 'Mark-up and margin to find missing figures', ['mark-up and margin to find missing figures', 'mark-up and margin', 'margin', 'mark-up'],
          mcqs=[('Goods costing $80 are sold for $100. The mark-up is', '25%', ['20%', '80%', '125%'], '20/80'),
                ('Goods costing $80 are sold for $100. The margin is', '20%', ['25%', '80%', '100%'], '20/100'),
                ('A mark-up of 50% is equivalent to a margin of', '33⅓%', ['50%', '25%', '66⅔%'], '50/150'),
                ('Revenue $60,000 at a margin of 25%. Cost of sales is', '$45,000', ['$48,000', '$15,000', '$75,000'], '60,000 × 75%'),
                ('Cost of sales $36,000 and mark-up 25%. Revenue is', '$45,000', ['$48,000', '$27,000', '$9,000'], '36,000 × 125%')],
          exps=[('Distinguish between mark-up and margin.', 'Mark-up is gross profit as a percentage of cost; margin is gross profit as a percentage of selling price (revenue).', 'Mark-up – on cost [1]; margin – on selling price [1] [2]'),
                ('Explain how mark-up can be used to estimate the value of inventory lost in a fire.', 'Using the normal mark-up, cost of sales is found from sales; cost of goods available less cost of sales gives the inventory that should have been held; less inventory saved = loss.', 'COS from sales via mark-up [1]; expected inventory − saved = loss [1] [2]')],
          disc=[('Explain why the actual margin of {f} might differ from its normal margin.', 'Price reductions/sales, theft or wastage, changes in purchase prices, or errors in inventory counts.', 'Two valid reasons [1 each] [2]')])


@spec(t13_3)
def t133_mm(r, D):
    f = firm(r)
    mu = r.choice([20, 25, 33.33, 50, 60, 100])
    mg = {20: 100 / 6, 25: 20, 33.33: 25, 50: 100 / 3, 60: 37.5, 100: 50}[mu]
    mus = '33⅓%' if mu == 33.33 else f'{mu:g}%'
    mgs = {20: '16⅔%', 25: '20%', 33.33: '25%', 50: '33⅓%', 60: '37.5%', 100: '50%'}[mu]
    oi, ci = step(r, 4000, 15000, 100), step(r, 3000, 12000, 100)
    rev = step(r, 40000, 150000, 1200)
    cos = rev * 100 / (100 + (100 / 3 if mu == 33.33 else mu))
    cos = round(cos)
    gp = rev - cos
    pur = cos - oi + ci
    if D >= 4:
        saved = step(r, 500, max(600, ci // 2), 100)
        setup = (f'A fire destroyed most of the inventory of {f} on 30 April. Inventory at 1 January was {m(oi)}; purchases from 1 January to 30 April were {m(pur - ci + ci)}; sales for the same period were {m(rev)}. '
                 f'{f} sells all goods at a mark-up of {mus}. Inventory costing {m(saved)} was saved.')
        exp_inv = oi + pur - cos
        parts = [('Calculate the cost of sales for the period.', m(cos), f'{m(rev)} × 100/{100 + (100 / 3 if mu == 33.33 else mu):g} = {m(cos)} [2]'),
                 ('Calculate the cost of the inventory destroyed by the fire.', m(exp_inv - saved), f'{m(oi)} + {m(pur)} − {m(cos)} = {m(exp_inv)} expected [1]; − {m(saved)} saved = {m(exp_inv - saved)} [1] [2]'),
                 ('State the equivalent gross margin.', mgs, f'{mus} mark-up = {mgs} margin [1]')]
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f}, 'mcq': None,
                'err': (f'calculated cost of sales as {m(rev * (100 - (100 / 3 if mu == 33.33 else mu)) / 100)}', 'the mark-up percentage was applied to selling price as if it were a margin', m(cos), f'{m(rev)} × 100/{100 + (100 / 3 if mu == 33.33 else mu):g}', 'cost of sales') if mu < 100 else None}
    setup = f'{f} sells goods at a mark-up of {mus} on cost. Revenue for the year was {m(rev)}; inventory was {m(oi)} at the start and {m(ci)} at the end of the year.'
    parts = [('Calculate the gross profit and the cost of sales.', f'Gross profit {m(gp)}; cost of sales {m(cos)}', f'Margin {mgs}: GP = {m(rev)} × {mgs} = {m(gp)} [1]; COS {m(cos)} [1] [2]'),
             ('Calculate the purchases for the year.', m(pur), f'{m(cos)} − {m(oi)} + {m(ci)} = {m(pur)} [2]'),
             ('Convert the mark-up to a gross margin.', mgs, f'{mus} ÷ (100% + {mus}) = {mgs} [1]')]
    wrong = rev * (mu if mu != 33.33 else 100 / 3) / 100
    c, ds = num_opts(m, gp, [wrong, rev - cos * 1.1, cos])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the gross profit?', c, ds, f'{m(rev)} × {mgs} = {m(gp)}'),
            'err': (f'calculated gross profit as {m(wrong)}', 'the mark-up (a percentage of cost) was applied to revenue; revenue must be multiplied by the margin', m(gp), f'{m(rev)} × {mgs}', 'gross profit') if mu < 100 else None}


t13_4 = A(13, 'Preparing financial statements from incomplete records', ['preparing financial statements from incomplete records', 'financial statements from incomplete records', 'incomplete records'],
          mcqs=[('When preparing an income statement from incomplete records, the purchases figure is usually found from', 'a reconstructed trade payables account', ['the bank statement only', 'the capital account', 'the statement of affairs'], 'Payments + closing − opening payables'),
                ('Expenses paid $5,000; expenses owing at start $400, at end $600. The income statement charge is', '$5,200', ['$4,800', '$5,000', '$6,000'], '5,000 − 400 + 600'),
                ('The opening capital for incomplete records is found from', 'the opening statement of affairs', ['the closing bank balance', 'the sales figure', 'the drawings'], 'Assets − liabilities'),
                ('Which figure is most likely to be a balancing figure in a reconstructed cash account?', 'Drawings', ['Opening bank balance', 'Closing receivables', 'Depreciation'], 'Unexplained cash withdrawals'),
                ('Depreciation for incomplete records is', 'calculated as usual from the non-current asset values', ['ignored', 'equal to drawings', 'found from the bank statement'], 'Normal accounting policies apply')],
          exps=[('Explain why the opening statement of affairs is needed when preparing financial statements from incomplete records.', 'It gives opening capital and opening balances of receivables, payables, inventory and accruals needed to reconstruct the year\'s figures.', 'Opening capital [1]; opening balances for reconstruction [1] [2]'),
                ('Explain how missing drawings can be found.', 'From the cash/bank account: all known receipts and payments are entered, and the balancing figure needed to reach the closing balance is taken to be drawings.', 'Reconstruct cash account [1]; balancing figure [1] [2]')],
          disc=[('Discuss the reliability of financial statements prepared from incomplete records for {f}.', 'Figures depend on estimates and balancing figures; errors and fraud may be hidden; but with careful reconstruction they give a reasonable view.', 'Estimates/balancing figures [1]; undetected errors [1]; judgement [1] [3]')])


@spec(t13_4)
def t134_fs(r, D):
    f, p = firm(r), pp(r)
    ob, cb = step(r, 2000, 8000, 10), step(r, 2000, 8000, 10)
    cr = step(r, 50000, 120000, 10)
    sales = cr + cb - ob
    op_, cp_ = step(r, 2000, 7000, 10), step(r, 2000, 7000, 10)
    pay = step(r, int(sales * 0.45), int(sales * 0.6), 10)
    pur = pay + cp_ - op_
    oi, ci = step(r, 3000, 10000, 100), step(r, 3000, 10000, 100)
    gp = sales - (oi + pur - ci)
    expd = step(r, 8000, 25000, 10)
    oa, ca = step(r, 100, 800, 10), step(r, 100, 800, 10)
    exp_ = expd - oa + ca
    dep = step(r, 500, 3000, 50) if D >= 3 else 0
    np_ = gp - exp_ - dep
    setup = (f'{p} owns {f} and keeps limited records. Receipts from customers {m(cr)}; payments to suppliers {m(pay)}; general expenses paid {m(expd)}. Opening and closing balances: trade receivables {m(ob)} and {m(cb)}; trade payables {m(op_)} and {m(cp_)}; '
             f'inventory {m(oi)} and {m(ci)}; general expenses owing {m(oa)} and {m(ca)}.' + (f' Depreciation of equipment for the year is {m(dep)}.' if dep else '') + ' All sales and purchases are on credit.')
    parts = [('Calculate revenue and purchases for the year.', f'Revenue {m(sales)}; purchases {m(pur)}', f'Revenue {m(cr)} + {m(cb)} − {m(ob)} = {m(sales)} [1]; purchases {m(pay)} + {m(cp_)} − {m(op_)} = {m(pur)} [1] [2]'),
             ('Calculate the gross profit.', m(gp), f'COS {m(oi)} + {m(pur)} − {m(ci)} = {m(oi + pur - ci)} [1]; GP {m(gp)} [1] [2]'),
             ('Calculate the profit for the year.', m(np_), f'Expenses {m(expd)} − {m(oa)} + {m(ca)} = {m(exp_)} [1]' + (f'; depreciation {m(dep)}' if dep else '') + f'; profit {m(np_)} [1] [2]')]
    wrong = gp - expd - dep
    c, ds = num_opts(m, np_, [wrong, gp, cr - pay - expd])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f, 'p': p},
            'mcq': ('What is the profit for the year?', c, ds, f'GP {m(gp)} − expenses {m(exp_)} − depreciation {m(dep)} = {m(np_)}'),
            'err': (f'calculated profit for the year as {m(wrong)}', 'expenses paid were used without adjusting for the opening and closing accruals', m(np_), f'{m(gp)} − ({m(expd)} − {m(oa)} + {m(ca)})' + (f' − {m(dep)}' if dep else ''), 'profit') if wrong != np_ else None}


CHAPTERS[13] = [t13_1, t13_2, t13_3, t13_4]


# ===================================================================== 14 Financial statements of sole traders with adjustments
def _st(r, D):
    d = {}
    d['sales'] = step(r, 120000, 300000, 100)
    d['pur'] = step(r, int(d['sales'] * 0.45), int(d['sales'] * 0.6), 100)
    d['oi'], d['ci'] = step(r, 5000, 20000, 100), step(r, 5000, 20000, 100)
    d['wages'] = step(r, 15000, 45000, 100)
    d['rent'] = step(r, 6000, 18000, 120)
    d['gen'] = step(r, 2000, 8000, 10)
    d['eq'] = step(r, 20000, 80000, 1000)
    d['ad'] = step(r, 4000, d['eq'] // 2, 100)
    d['tr'] = step(r, 8000, 25000, 100)
    d['bank'] = step(r, 1000, 9000, 10)
    d['tp'] = step(r, 5000, 18000, 100)
    d['draw'] = step(r, 10000, 25000, 100)
    d['acc'] = step(r, 300, 2000, 10)
    d['pre'] = d['rent'] // 12 * r.choice([1, 2, 3])
    d['rate'] = r.choice([10, 20, 25])
    d['rb'] = D >= 4 and r.random() < 0.5
    d['dep'] = (d['eq'] - d['ad']) * d['rate'] / 100 if d['rb'] else d['eq'] * d['rate'] / 100
    d['all_old'] = step(r, 200, 800, 10)
    d['all_pct'] = r.choice([2, 3, 4, 5])
    d['bd'] = step(r, 200, 1500, 100) if D >= 3 else 0
    d['all_new'] = (d['tr'] - d['bd']) * d['all_pct'] / 100
    dr = d['pur'] + d['oi'] + d['wages'] + d['rent'] + d['gen'] + d['eq'] + d['tr'] + d['bank'] + d['draw']
    cr = d['sales'] + d['ad'] + d['tp'] + d['all_old']
    d['cap'] = dr - cr
    if d['cap'] < 15000:
        bump = (15000 - d['cap']) // 1000 * 1000 + step(r, 1000, 20000, 1000)
        d['eq'] += bump
        d['cap'] += bump
        d['dep'] = (d['eq'] - d['ad']) * d['rate'] / 100 if d['rb'] else d['eq'] * d['rate'] / 100
    d['cos'] = d['oi'] + d['pur'] - d['ci']
    d['gp'] = d['sales'] - d['cos']
    d['wages_c'] = d['wages'] + d['acc']
    d['rent_c'] = d['rent'] - d['pre']
    d['all_ch'] = d['all_new'] - d['all_old']
    d['np'] = d['gp'] - d['wages_c'] - d['rent_c'] - d['gen'] - d['dep'] - d['bd'] - d['all_ch']
    d['nca'] = d['eq'] - d['ad'] - d['dep']
    d['ca'] = d['ci'] + d['tr'] - d['bd'] - d['all_new'] + d['pre'] + d['bank']
    d['cl'] = d['tp'] + d['acc']
    d['ccap'] = d['cap'] + d['np'] - d['draw']
    return d


def _st_text(r, d, full=True):
    tb = (f'sales {m(d["sales"])}; purchases {m(d["pur"])}; inventory at 1 January {m(d["oi"])}; wages {m(d["wages"])}; rent {m(d["rent"])}; general expenses {m(d["gen"])}; '
          f'equipment at cost {m(d["eq"])}; provision for depreciation of equipment {m(d["ad"])}; trade receivables {m(d["tr"])}; allowance for doubtful debts {m(d["all_old"])}; bank {m(d["bank"])}; '
          f'trade payables {m(d["tp"])}; drawings {m(d["draw"])}; capital {m(d["cap"])}')
    adj = [f'inventory at 31 December was {m(d["ci"])}', f'wages owing at the year end were {m(d["acc"])}', f'rent prepaid at the year end was {m(d["pre"])}',
           f'equipment is depreciated at {d["rate"]}% per annum on the {"reducing-balance" if d["rb"] else "straight-line"} basis']
    if d['bd']:
        adj.append(f'an irrecoverable debt of {m(d["bd"])} is to be written off')
    adj.append(f'the allowance for doubtful debts is to be {d["all_pct"]}% of trade receivables')
    return tb, adj


t14_1 = A(14, 'Year-end adjustments from a trial balance', ['year-end adjustments from a trial balance', 'year-end adjustments', 'adjustments from a trial balance'],
          mcqs=[('Closing inventory given as a note below the trial balance is entered', 'in cost of sales and as a current asset', ['only in cost of sales', 'only as a current asset', 'as a current liability'], 'Notes below a TB are recorded twice'),
                ('Wages in the trial balance $20,000; wages owing $700. The income statement shows', '$20,700', ['$19,300', '$20,000', '$700'], 'Add the accrual'),
                ('The provision for depreciation in the trial balance is the', 'balance before this year\'s charge', ['balance after this year\'s charge', 'charge for this year', 'cost of the asset'], 'This year\'s charge is an adjustment'),
                ('A note says insurance of $600 is prepaid. The adjustment is', 'reduce the insurance expense and show a current asset', ['increase the insurance expense and show a liability', 'reduce capital', 'increase bank'], 'Prepayment'),
                ('Which item is NOT normally an adjustment after the trial balance?', 'Sales for the year', ['Closing inventory', 'Depreciation', 'Accrued expenses'], 'Sales is already in the TB')],
          exps=[('Explain why each adjustment listed below a trial balance affects two items in the financial statements.', 'Each adjustment is a double entry: one effect is in the income statement (income or expense) and the other in the statement of financial position (asset or liability).', 'Double entry [1]; IS + SFP [1] [2]'),
                ('Explain why the depreciation charge is not shown in the trial balance.', 'It is calculated at the year end after the trial balance is extracted, from the asset cost or carrying amount and the policy.', 'Calculated at year end [1]; after TB [1] [2]')],
          disc=[('Explain why {p} should not simply use the trial balance figures without adjustments.', 'Unadjusted figures ignore accruals, prepayments, depreciation and inventory, so profit and assets would be misstated (accruals and prudence concepts).', 'Misstated profit/assets [1]; concepts [1] [2]')])


@spec(t14_1)
def t141_adj(r, D):
    p, f = pp(r), firm(r)
    d = _st(r, D)
    tb, adj = _st_text(r, d)
    money = m2 if abs(d['all_new'] - round(d['all_new'])) > 0.001 or abs(d['dep'] - round(d['dep'])) > 0.001 else m
    setup = f'{p} owns {f}. The trial balance at 31 December included: {tb}. Additional information: {lst(adj)}.'
    parts = [('Calculate the amounts for wages and rent to be shown in the income statement.', f'Wages {m(d["wages_c"])}; rent {m(d["rent_c"])}', f'Wages {m(d["wages"])} + {m(d["acc"])} = {m(d["wages_c"])} [1]; rent {m(d["rent"])} − {m(d["pre"])} = {m(d["rent_c"])} [1] [2]'),
             ('Calculate the depreciation charge for the year.', money(d['dep']), f'{d["rate"]}% × {m(d["eq"] - d["ad"]) if d["rb"] else m(d["eq"])} = {money(d["dep"])} [1]'),
             ('Calculate the change in the allowance for doubtful debts.', f'{"Increase" if d["all_ch"] > 0 else "Decrease"} {money(abs(d["all_ch"]))}', f'({m(d["tr"])} − {m(d["bd"])}) × {d["all_pct"]}% = {money(d["all_new"])} [1]; − {m(d["all_old"])} = {money(d["all_ch"])} [1] [2]'),
             ('Calculate the cost of sales.', m(d['cos']), f'{m(d["oi"])} + {m(d["pur"])} − {m(d["ci"])} = {m(d["cos"])} [1]')]
    wrong = d['wages'] - d['acc']
    return {'setup': setup, 'parts': parts, 'ctx': {'p': p, 'f': f},
            'mcq': ('What amount for wages is shown in the income statement?', *num_opts(m, d['wages_c'], [wrong, d['wages'], d['acc']]), f'{m(d["wages"])} + {m(d["acc"])}'),
            'err': (f'showed rent of {m(d["rent"] + d["pre"])} in the income statement', 'the prepayment was added instead of deducted; rent paid in advance belongs to next year', m(d['rent_c']), f'{m(d["rent"])} − {m(d["pre"])}', 'rent expense')}


t14_2 = A(14, 'Full income statement and statement of financial position', ['full income statement and statement of financial position', 'income statement and statement of financial position', 'final accounts'],
          mcqs=[('Profit for the year is added to opening capital in the', 'statement of financial position', ['income statement', 'trial balance', 'cash book'], 'Capital section'),
                ('Net current assets are', 'current assets minus current liabilities', ['non-current assets minus current liabilities', 'total assets minus capital', 'capital minus drawings'], 'Working capital'),
                ('The allowance for doubtful debts is shown', 'as a deduction from trade receivables', ['as a current liability', 'as an expense in full each year', 'in the capital section'], 'Net receivables'),
                ('Accumulated depreciation in the statement of financial position is', 'deducted from the cost of non-current assets', ['added to current assets', 'shown under current liabilities', 'shown as income'], 'Carrying amount'),
                ('If the statement of financial position does not balance, the most likely cause is', 'an adjustment recorded only once', ['too many expenses', 'a high profit', 'drawings exceeding profit'], 'Every adjustment has two effects')],
          exps=[('Explain why the closing capital in the statement of financial position must equal net assets.', 'By the accounting equation, assets − liabilities = capital; profit increases net assets and capital equally, drawings reduce both.', 'Accounting equation [1]; profit/drawings affect both [1] [2]'),
                ('Explain why both the income statement and the statement of financial position are needed by users.', 'The income statement shows performance over the year; the SFP shows the financial position (assets, liabilities, capital) at a point in time.', 'IS – performance over period [1]; SFP – position at a date [1] [2]')],
          disc=[('Comment on whether {p}\'s drawings are sustainable given the profit for the year.', 'If drawings exceed profit, capital falls and the business weakens; if below, capital grows and supports expansion.', 'Compare drawings and profit [1]; effect on capital [1]; judgement [1] [3]')])


@spec(t14_2, D=(2, 3, 4, 5))
def t142_full(r, D):
    p, f = pp(r), firm(r)
    d = _st(r, D)
    tb, adj = _st_text(r, d)
    money = m2 if any(abs(d[k] - round(d[k])) > 0.001 for k in ('all_new', 'dep')) else m
    setup = f'The following balances were extracted from the books of {f}, owned by {p}, at 31 December: {tb}. Notes: {lst(adj)}.'
    parts = [('Calculate the gross profit.', m(d['gp']), f'COS {m(d["oi"])} + {m(d["pur"])} − {m(d["ci"])} = {m(d["cos"])} [1]; GP {m(d["sales"])} − {m(d["cos"])} = {m(d["gp"])} [1] [2]'),
             ('Calculate the profit for the year.', money(d['np']), f'{m(d["gp"])} − wages {m(d["wages_c"])} − rent {m(d["rent_c"])} − general {m(d["gen"])} − depreciation {money(d["dep"])}' + (f' − irrecoverable debt {m(d["bd"])}' if d['bd'] else '') + f' {"−" if d["all_ch"] >= 0 else "+"} allowance change {money(abs(d["all_ch"]))} [3]; = {money(d["np"])} [1] [4]'),
             ('Calculate the totals of current assets and current liabilities.', f'CA {money(d["ca"])}; CL {m(d["cl"])}', f'CA: inventory {m(d["ci"])} + net receivables {money(d["tr"] - d["bd"] - d["all_new"])} + prepayment {m(d["pre"])} + bank {m(d["bank"])} = {money(d["ca"])} [2]; CL {m(d["tp"])} + {m(d["acc"])} = {m(d["cl"])} [1] [3]'),
             ('Calculate the closing capital and show that it equals net assets.', f'{money(d["ccap"])}', f'{m(d["cap"])} + {money(d["np"])} − {m(d["draw"])} = {money(d["ccap"])} [1]; NCA {money(d["nca"])} + CA {money(d["ca"])} − CL {m(d["cl"])} = {money(d["nca"] + d["ca"] - d["cl"])} [1] [2]')]
    wrong = d['gp'] - d['wages'] - d['rent'] - d['gen'] - d['dep'] - d['bd'] - d['all_ch']
    return {'setup': setup, 'parts': parts, 'ctx': {'p': p, 'f': f},
            'err': (f'calculated the profit for the year as {money(wrong)}', 'the wages accrual and the rent prepayment were ignored; expenses must be adjusted to the amounts incurred in the year', money(d['np']), f'wages {m(d["wages_c"])}, rent {m(d["rent_c"])} used', 'profit for the year') if abs(wrong - d['np']) > 0.5 else None}


t14_3 = A(14, 'Calculating and interpreting profit and working capital', ['calculating and interpreting profit and working capital', 'interpreting profit and working capital', 'working capital'],
          mcqs=[('A business has current assets of $24,000 and current liabilities of $16,000. Its current ratio is', '1.5:1', ['0.67:1', '8,000:1', '2.5:1'], '24,000 ÷ 16,000'),
                ('Which change would increase working capital?', 'Receiving a long-term loan into the bank', ['Paying a supplier from the bank', 'Buying inventory on credit', 'Buying a machine for cash'], 'CA rise, CL unchanged'),
                ('A sole trader makes a profit but has a bank overdraft. The most likely reason is', 'cash has been used to buy non-current assets or for drawings', ['profit was overstated by depreciation', 'sales were too high', 'expenses were too low'], 'Profit is not cash'),
                ('Too much working capital may indicate', 'idle cash or excessive inventory that could be used more profitably', ['a risk of being unable to pay debts', 'high profitability', 'no trade receivables'], 'Resources tied up'),
                ('Profit for the year as a percentage of revenue is the', 'profit margin', ['gross margin', 'mark-up', 'current ratio'], 'Net/operating margin')],
          exps=[('Explain why a profitable business can run short of cash.', 'Profit includes credit sales not yet received and non-cash expenses; cash may be spent on non-current assets, loan repayments, inventory or drawings that do not appear as expenses.', 'Timing/credit sales [1]; capital spending/drawings not expenses [1] [2]'),
                ('Explain two ways a sole trader could improve working capital.', 'Introduce more capital; take a long-term loan; sell surplus non-current assets; reduce drawings; collect receivables faster; reduce inventory.', 'Two methods with explanation [1 each] [2]')],
          disc=[('Advise {p} whether the working capital position of {f} is satisfactory.', 'Compare the current ratio with a benchmark (about 1.5–2:1) and the business type; consider the composition (inventory vs cash) and trend.', 'Uses ratio [1]; composition/benchmark [1]; advice [1] [3]')])


@spec(t14_3)
def t143_wc(r, D):
    p, f = pp(r), firm(r)
    inv, tr, bank = step(r, 4000, 20000, 100), step(r, 3000, 15000, 100), step(r, -4000, 6000, 100)
    tp, acc = step(r, 4000, 15000, 100), step(r, 200, 1500, 100)
    od = -bank if bank < 0 else 0
    ca = inv + tr + max(bank, 0)
    cl = tp + acc + od
    wc = ca - cl
    cr_ = ca / cl
    rev = step(r, 80000, 250000, 1000)
    np_ = step(r, int(rev * 0.05), int(rev * 0.2), 100)
    setup = f'{p} owns {f}. At the year end: inventory {m(inv)}, trade receivables {m(tr)}, ' + (f'bank {m(bank)}' if bank >= 0 else f'bank overdraft {m(od)}') + f', trade payables {m(tp)}, accrued expenses {m(acc)}. Revenue for the year was {m(rev)} and profit for the year {m(np_)}.'
    parts = [('Calculate the working capital and the current ratio (to two decimal places).', f'{m(wc)}; {ratio_s(cr_)}', f'CA {m(ca)} − CL {m(cl)} = {m(wc)} [1]; {m(ca)} ÷ {m(cl)} = {ratio_s(cr_)} [1] [2]'),
             ('Calculate the profit margin.', pc(np_ / rev * 100), f'{m(np_)} ÷ {m(rev)} × 100 = {pc(np_ / rev * 100)} [1]'),
             ('Comment on the liquidity of the business.', ('Current ratio below 1:1 – the business may struggle to pay current liabilities' if cr_ < 1 else ('Current ratio is comfortable' if cr_ <= 2.5 else 'Current ratio is high – resources may be tied up in idle inventory or receivables')) + (', and it relies on an overdraft' if od else '') + '.',
              'Comment linked to ratio value [1]; composition/overdraft/inventory point [1] [2]')]
    wrong = ca + cl
    return {'setup': setup, 'parts': parts, 'ctx': {'p': p, 'f': f},
            'mcq': ('What is the working capital?', *num_opts(m, wc, [wrong if not od else wc + 2 * od, ca, cl - ca]), f'{m(ca)} − {m(cl)}'),
            'err': (f'calculated working capital as {m(wc + 2 * od)}', 'the bank overdraft was treated as a current asset; it is a current liability', m(wc), f'{m(ca)} − {m(cl)}', 'working capital') if od else
            (f'calculated the current ratio as {ratio_s(cl / ca)}', 'the ratio was inverted; current ratio = current assets ÷ current liabilities', ratio_s(cr_), f'{m(ca)} ÷ {m(cl)}', 'current ratio')}


CHAPTERS[14] = [t14_1, t14_2, t14_3]


# ===================================================================== 15 Partnership accounts
t15_1 = A(15, 'Partnership agreement and the Partnership Act 1890 provisions', ['partnership agreement and the partnership act 1890 provisions', 'partnership act 1890', 'partnership agreement'],
          mcqs=[('In the absence of a partnership agreement, profits and losses are shared', 'equally', ['in the ratio of capitals', 'in proportion to hours worked', 'according to drawings'], 'Partnership Act 1890'),
                ('Under the Partnership Act 1890, a partner\'s loan to the firm earns interest at', '5% per annum', ['10% per annum', 'the bank base rate', 'nothing'], 'Section 24'),
                ('Without an agreement, partners are entitled to', 'no salaries and no interest on capital', ['salaries but no interest on capital', 'interest on capital at 5%', 'interest on drawings'], 'Act default rules'),
                ('Interest on a partner\'s loan is', 'an expense charged before profit is appropriated', ['an appropriation of profit', 'added to the partner\'s capital account', 'deducted from drawings'], 'It is a charge against profit'),
                ('Which item is usually included in a partnership agreement?', 'The profit-sharing ratio', ['The names of customers', 'The selling prices of goods', 'The amount of inventory to hold'], 'Agreement covers capital, profit sharing, interest, salaries, drawings')],
          exps=[('State three provisions of the Partnership Act 1890 that apply when there is no agreement.', 'Profits and losses shared equally; no interest on capital; no partners\' salaries; no interest on drawings; 5% interest on partners\' loans.', 'Any three [1 each] [3]'),
                ('Explain why partners should have a written partnership agreement.', 'It avoids disputes by setting out capital, profit sharing, salaries, interest and drawings; otherwise the Act\'s rules apply, which may be unfair to a partner who works more or invests more.', 'Avoids disputes/clear rules [1]; Act may be unfair [1] [2]')],
          disc=[('Discuss whether the partner who invested most capital in {f} is treated fairly if there is no agreement.', 'Under the Act they get no interest on capital and only an equal share, so their extra investment is not rewarded; an agreement could give interest on capital.', 'Equal share/no interest [1]; unfair to larger investor [1]; solution [1] [3]')])


@spec(t15_1)
def t151_act(r, D):
    f = firm(r)
    n = 2 if D <= 3 else 3
    ps = pp(r, n)
    caps = [step(r, 20000, 90000, 1000) for _ in ps]
    loan = step(r, 5000, 30000, 1000) if D >= 2 else 0
    prof = step(r, 30000, 120000, 300)
    li = loan * 5 // 100
    np_ = prof - li
    share = np_ / n
    setup = f'{", ".join(ps[:-1])} and {ps[-1]} are partners in {f} with capitals of {", ".join(m(c) for c in caps)} respectively. There is no partnership agreement.' + (f' {ps[0]} has also lent the firm {m(loan)}.' if loan else '') + f' The profit for the year before any interest on the loan was {m(prof)}.'
    money = m2 if abs(share - round(share)) > 0.001 else m
    parts = [('Calculate each partner\'s share of the profit.', f'{money(share)} each', (f'Loan interest 5% × {m(loan)} = {m(li)} [1]; ' if loan else '') + f'profit {m(np_)} ÷ {n} = {money(share)} each [1] [{2 if loan else 1}]'),
             ('State two other rules of the Partnership Act 1890 that apply to this partnership.', 'No interest on capital; no salaries; no interest on drawings; profits shared equally.', 'Two rules [1 each] [2]')]
    if loan:
        parts.append((f'State the total amount credited to {ps[0]} for the year.', money(share + li), f'Share {money(share)} + loan interest {m(li)} = {money(share + li)} [1]'))
    wrong = prof * caps[0] / sum(caps)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is each partner\'s share of the profit?', *num_opts(money, share, [prof / n, wrong, np_]), f'({m(prof)} − {m(li)}) ÷ {n}'),
            'err': (f'shared the profit in the ratio of the partners\' capitals, giving {ps[0]} {money(wrong)}', 'without an agreement the Partnership Act 1890 requires profits to be shared equally' + (' after charging 5% loan interest' if loan else ''), money(share), f'({m(prof)} − {m(li)}) ÷ {n}', f'share for {ps[0]}')}


def _appr(r, D):
    n = 2 if D <= 3 else 3
    ps = pp(r, n)
    ratio = r.choice([(3, 2), (2, 1), (1, 1), (3, 1)]) if n == 2 else r.choice([(3, 2, 1), (2, 2, 1), (4, 3, 1), (1, 1, 1)])
    s = sum(ratio)
    caps = [step(r, 20000, 100000, 1000) for _ in ps]
    ioc = r.choice([4, 5, 6, 8, 10])
    sal = [step(r, 6000, 20000, 1000) if i == 0 else 0 for i in range(n)]
    if D >= 3 and n == 3:
        sal[1] = step(r, 4000, 12000, 1000)
    iod = [step(r, 100, 900, 10) for _ in ps] if D >= 3 else [0] * n
    prof = step(r, 50000, 150000, 100 * s)
    ic = [c * ioc / 100 for c in caps]
    resid = prof + sum(iod) - sum(ic) - sum(sal)
    sh = [resid * x / s for x in ratio]
    return ps, ratio, caps, ioc, sal, iod, prof, ic, resid, sh


def _appr_text(ps, ratio, caps, ioc, sal, iod, prof):
    t = f'{" and ".join([", ".join(ps[:-1]), ps[-1]]) if len(ps) > 2 else " and ".join(ps)} are partners sharing profits and losses {rs(ratio)}. Capitals are ' + ', '.join(f'{p} {m(c)}' for p, c in zip(ps, caps)) + f'. The agreement provides for interest on capital at {ioc}% per annum'
    sals = [f'{p} {m(s)}' for p, s in zip(ps, sal) if s]
    t += f' and annual salaries: {", ".join(sals)}.' if sals else '.'
    if any(iod):
        t += ' Interest on drawings has been calculated as ' + ', '.join(f'{p} {m(x)}' for p, x in zip(ps, iod)) + '.'
    return t + f' Profit for the year was {m(prof)}.'


t15_2 = A(15, 'Appropriation account: interest on capital and drawings, salaries, profit share', ['appropriation account: interest on capital and drawings, salaries, profit share', 'appropriation account', 'interest on capital', 'interest on drawings'],
          mcqs=[('Interest on drawings is', 'added to profit in the appropriation account and debited to the partner\'s current account', ['deducted from profit and credited to the partner', 'an expense in the income statement', 'ignored'], 'It is a charge on the partner'),
                ('A partner\'s salary is', 'an appropriation of profit, not an expense', ['an expense in the income statement', 'a liability of the firm', 'deducted from capital'], 'Partners are owners'),
                ('Profit $60,000; interest on capital $8,000; salaries $12,000; interest on drawings $1,000. The residual profit to share is', '$41,000', ['$39,000', '$40,000', '$81,000'], '60,000 + 1,000 − 8,000 − 12,000'),
                ('Why is interest on capital given to partners?', 'To reward partners who invest more capital in the firm', ['Because it is required by law', 'To reduce tax', 'To reduce drawings'], 'Compensates for capital contributed'),
                ('Why do partnership agreements often charge interest on drawings?', 'To discourage partners from taking drawings early in the year', ['To increase the firm\'s expenses', 'Because the bank requires it', 'To reward large drawings'], 'Penalises early withdrawals')],
          exps=[('Explain why a partner\'s salary is shown in the appropriation account and not as an expense.', 'Partners are owners, not employees; their salary is a way of sharing profit to reward work, so it is an appropriation of profit.', 'Partners are owners [1]; reward/share of profit [1] [2]'),
                ('Explain the purpose of charging interest on drawings.', 'It discourages early or excessive withdrawals and compensates partners who leave money in the business.', 'Discourage drawings [1]; fairness [1] [2]')],
          disc=[('Evaluate whether the profit-sharing arrangements of {f} are fair to all partners.', 'Interest on capital rewards investment, salaries reward work and the ratio shares the rest; fairness depends on each partner\'s capital, time and skills.', 'Interest/salary rationale [1]; ratio vs contribution [1]; judgement [1] [3]')])


@spec(t15_2)
def t152_appr(r, D):
    f = firm(r)
    ps, ratio, caps, ioc, sal, iod, prof, ic, resid, sh = _appr(r, D)
    money = m2 if any(abs(x - round(x)) > 0.001 for x in ic + sh) else m
    setup = _appr_text(ps, ratio, caps, ioc, sal, iod, prof)
    parts = [('Calculate the residual profit to be shared in the profit-sharing ratio.', money(resid), f'{m(prof)}' + (f' + IoD {m(sum(iod))}' if any(iod) else '') + f' − IoC {money(sum(ic))} − salaries {m(sum(sal))} = {money(resid)} [2]'),
             ('Prepare the appropriation account, showing each partner\'s share of the residual profit.', '; '.join(f'{p}: IoC {money(i)}, share {money(s_)}' for p, i, s_ in zip(ps, ic, sh)),
              '; '.join(f'{p} IoC {money(i)}' for p, i in zip(ps, ic)) + ' [1]; salaries [1]; ' + '; '.join(f'{p} {money(s_)}' for p, s_ in zip(ps, sh)) + ' [2] [4]'),
             (f'Calculate the total profit credited to {ps[0]}.', money(ic[0] + sal[0] + sh[0] - iod[0]), f'{money(ic[0])} + {m(sal[0])} + {money(sh[0])}' + (f' − IoD {m(iod[0])}' if iod[0] else '') + f' = {money(ic[0] + sal[0] + sh[0] - iod[0])} [2]')]
    wrong = prof - sum(iod) - sum(ic) - sum(sal)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the residual profit shared in the profit-sharing ratio?', *num_opts(money, resid, [prof - sum(ic), prof - sum(sal), wrong if any(iod) else prof + sum(ic)]), f'{m(prof)} + {m(sum(iod))} − {money(sum(ic))} − {m(sum(sal))}'),
            'err': (f'calculated the residual profit as {money(wrong)}', 'interest on drawings was deducted; it is charged to the partners and so is added to the profit available', money(resid), f'{m(prof)} + {m(sum(iod))} − {money(sum(ic))} − {m(sum(sal))}', 'residual profit') if any(iod) else
            (f'deducted partners\' salaries as an expense to find profit, then deducted them again in the appropriation account, giving residual profit of {money(resid - sum(sal))}', 'salaries are appropriations of profit only – they must be deducted once, in the appropriation account', money(resid), f'{m(prof)} − {money(sum(ic))} − {m(sum(sal))}', 'residual profit')}


t15_3 = A(15, 'Capital and current accounts of partners', ['capital and current accounts of partners', 'current accounts', 'capital accounts of partners'],
          mcqs=[('Under the fixed capital method, a partner\'s share of profit is credited to', 'the current account', ['the capital account', 'the appropriation account only', 'the bank account'], 'Capital stays fixed'),
                ('A debit balance on a partner\'s current account means that', 'the partner has withdrawn more than their share of profits', ['the partner has invested extra capital', 'the firm owes the partner money', 'the partner has a loan to the firm'], 'Drawings exceed entitlements'),
                ('Drawings are entered in the partner\'s current account on the', 'debit side', ['credit side', 'they are entered in the capital account', 'either side'], 'They reduce what is owed to the partner'),
                ('Opening current account credit $2,000; share of profit $18,000; IoC $1,500; drawings $16,000. The closing balance is', '$5,500 credit', ['$5,500 debit', '$37,500 credit', '$1,500 credit'], '2,000 + 18,000 + 1,500 − 16,000'),
                ('Which item is credited to a partner\'s current account?', 'Interest on capital', ['Interest on drawings', 'Drawings', 'A share of a loss'], 'Entitlement of the partner')],
          exps=[('Explain why partners usually keep fixed capital accounts with separate current accounts.', 'Capital accounts show the agreed long-term investment, which is the basis for interest on capital; all changes from profits and drawings go through current accounts.', 'Fixed agreed capital/basis for IoC [1]; current account records profits & drawings [1] [2]'),
                ('Explain what a debit balance on a partner\'s current account indicates and why it may be a concern.', 'The partner has taken out more than their profit entitlement, so they owe the firm; persistent debit balances reduce the firm\'s capital and liquidity.', 'Over-withdrawal/owes firm [1]; liquidity/capital concern [1] [2]')],
          disc=[('Suggest how the partners of {f} could prevent a current account going into debit.', 'Set drawings limits in the agreement; charge interest on drawings; review drawings monthly against expected profit.', 'Two measures [1 each] [2]')])


@spec(t15_3)
def t153_cur(r, D):
    f = firm(r)
    ps, ratio, caps, ioc, sal, iod, prof, ic, resid, sh = _appr(r, D)
    ob = [step(r, -3000, 6000, 100) for _ in ps]
    dr_ = [step(r, 10000, 40000, 100) for _ in ps]
    cl = [o + i + s + h - d - x for o, i, s, h, d, x in zip(ob, ic, sal, sh, dr_, iod)]
    money = m2 if any(abs(x - round(x)) > 0.001 for x in ic + sh) else m
    setup = _appr_text(ps, ratio, caps, ioc, sal, iod, prof) + ' Current account balances at the start of the year were ' + ', '.join(f'{p} {m(abs(o))} {"credit" if o >= 0 else "debit"}' for p, o in zip(ps, ob)) + '; drawings for the year were ' + ', '.join(f'{p} {m(d)}' for p, d in zip(ps, dr_)) + '.'
    parts = [('Calculate the closing balance on each partner\'s current account.', '; '.join(f'{p} {money(abs(c))} {"credit" if c >= 0 else "debit"}' for p, c in zip(ps, cl)),
              f'Residual profit {money(resid)} shared {rs(ratio)} [1]; ' + '; '.join(f'{p}: {m(o)} + {money(i)} + {m(s)} + {money(h)} − {m(d)}' + (f' − {m(x)}' if x else '') + f' = {money(c)}' for p, o, i, s, h, d, x, c in zip(ps, ob, ic, sal, sh, dr_, iod, cl)) + f' [{len(ps)}] [{len(ps) + 1}]'),
             ('State where the current account balances appear in the statement of financial position.', 'In the capital (equity) section, below the capital accounts; a debit balance is deducted.', 'Capital section [1]; debit deducted [1] [2]')]
    neg = [i for i, c in enumerate(cl) if c < 0]
    if neg:
        parts.append((f'Explain the significance of the balance on {ps[neg[0]]}\'s current account.', f'{ps[neg[0]]} has withdrawn more than their entitlement and owes the firm {money(-cl[neg[0]])}.', 'Over-withdrawal [1]; owes firm [1] [2]'))
    w = ob[0] + ic[0] + sal[0] + sh[0] + dr_[0] - iod[0]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is the closing balance on {ps[0]}\'s current account?', f'{money(abs(cl[0]))} {"credit" if cl[0] >= 0 else "debit"}',
                    [f'{money(abs(cl[0]))} {"debit" if cl[0] >= 0 else "credit"}', f'{money(abs(w))} credit', f'{money(abs(cl[0] + 2 * ob[0]))} {"credit" if cl[0] + 2 * ob[0] >= 0 else "debit"}', f'{money(abs(cl[0] + sal[0] + 1000))} credit'], f'{ps[0]}: entitlements − drawings = {money(cl[0])}'),
            'err': (f'calculated the closing balance on {ps[0]}\'s current account as {money(w)}', 'drawings were credited (added) instead of debited', money(cl[0]), f'{m(ob[0])} + {money(ic[0])} + {m(sal[0])} + {money(sh[0])} − {m(dr_[0])}' + (f' − {m(iod[0])}' if iod[0] else ''), 'balance')}


t15_4 = A(15, 'Partnership statement of financial position', ['partnership statement of financial position', 'partnership statement'],
          mcqs=[('In a partnership statement of financial position, the capital section shows', 'each partner\'s capital and current account balances', ['only the total capital', 'the appropriation account', 'the drawings of each partner only'], 'Equity of each partner'),
                ('A loan from a partner repayable in five years is shown as', 'a non-current liability', ['part of that partner\'s capital', 'a current asset', 'a current liability'], 'It is a loan, not capital'),
                ('Capitals $80,000; current accounts $6,000 credit and $1,500 debit. Total partners\' funds are', '$84,500', ['$87,500', '$80,000', '$86,000'], '80,000 + 6,000 − 1,500'),
                ('Which item appears in a partnership SFP but not in a sole trader\'s?', 'Partners\' current accounts', ['Trade payables', 'Inventory', 'Bank overdraft'], 'Separate current accounts'),
                ('The net assets of a partnership equal', 'the total of the partners\' capital and current account balances', ['the profit for the year', 'the total capital only', 'total assets'], 'Accounting equation')],
          exps=[('Explain why a partner\'s loan is not included in the partners\' capital section.', 'It is a liability with interest and repayment terms, separate from the capital the partner has invested as an owner.', 'Liability with terms [1]; distinct from capital [1] [2]'),
                ('Explain how the statement of financial position of a partnership differs from that of a sole trader.', 'The capital section shows a capital and current account for each partner rather than one capital account with profit and drawings.', 'Separate accounts per partner [1]; current accounts [1] [2]')],
          disc=[('Discuss whether the partners of {f} should convert part of their current account credit balances into capital.', 'Converting increases permanent capital and may earn more interest on capital, but reduces flexibility to withdraw; it signals commitment to lenders.', 'Benefit [1]; drawback [1]; judgement [1] [3]')])


@spec(t15_4)
def t154_sfp(r, D):
    f = firm(r)
    ps = pp(r, 2 if D <= 3 else 3)
    caps = [step(r, 20000, 90000, 1000) for _ in ps]
    curs = [step(r, -3000, 9000, 100) for _ in ps]
    loan = step(r, 5000, 20000, 1000) if D >= 3 else 0
    funds = sum(caps) + sum(curs)
    cl = step(r, 5000, 20000, 100)
    nca = step(r, int(funds * 0.6), int(funds * 0.9), 100)
    ca = funds + loan + cl - nca
    setup = f'{" and ".join(ps)} are partners in {f}. At 31 December: non-current assets {m(nca)}; current assets {m(ca)}; current liabilities {m(cl)}' + (f'; a loan from {ps[0]} of {m(loan)} repayable in 2031' if loan else '') + '. Capital accounts: ' + ', '.join(f'{p} {m(c)}' for p, c in zip(ps, caps)) + '; current accounts: ' + ', '.join(f'{p} {m(abs(c))} {"credit" if c >= 0 else "debit"}' for p, c in zip(ps, curs)) + '.'
    parts = [('Calculate the total of the partners\' capital and current accounts.', m(funds), f'Capitals {m(sum(caps))} + current accounts net {m(sum(curs))} = {m(funds)} [2]'),
             ('Calculate the net assets and show that they equal the partners\' funds.', m(funds), f'{m(nca)} + {m(ca)} − {m(cl)}' + (f' − loan {m(loan)}' if loan else '') + f' = {m(funds)} [2]')]
    if loan:
        parts.append((f'State how the loan from {ps[0]} is shown and the interest it earns if there is no agreement.', f'Non-current liability; 5% × {m(loan)} = {m(loan * 5 // 100)} a year.', f'Non-current liability [1]; {m(loan * 5 // 100)} [1] [2]'))
    neg = [c for c in curs if c < 0]
    wrong = sum(caps) + sum(abs(c) for c in curs)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the total of the partners\' funds?', *num_opts(m, funds, [wrong, sum(caps), funds + loan]), f'{m(sum(caps))} + {m(sum(curs))}'),
            'err': (f'calculated partners\' funds as {m(wrong)}', 'the debit current account balance was added; a debit balance is deducted', m(funds), f'{m(sum(caps))} + {m(sum(curs))}', 'partners\' funds') if neg else
            ((f'included the loan from {ps[0]} in partners\' funds, giving {m(funds + loan)}', 'a partner\'s loan is a liability, not part of capital', m(funds), f'{m(sum(caps))} + {m(sum(curs))}', 'partners\' funds') if loan else None)}


CHAPTERS[15] = [t15_1, t15_2, t15_3, t15_4]


# ===================================================================== 16 Clubs and societies
CLUBS = ['Riverside Tennis Club', 'Harbour Chess Society', 'Hilltop Golf Club', 'Lakeside Rowing Club', 'Sunrise Drama Society', 'Greenfield Cricket Club', 'Coral Reef Diving Club', 'Old Town Photography Society']

t16_1 = A(16, 'Receipts and payments account', ['receipts and payments account', 'receipts and payments'],
          mcqs=[('A receipts and payments account is', 'a summary of the cash book of a club', ['the club\'s income statement', 'a statement of the accumulated fund', 'a list of members'], 'Cash summary'),
                ('Which item appears in a receipts and payments account but NOT in an income and expenditure account?', 'Purchase of new equipment', ['Depreciation', 'Subscriptions owing', 'Accrued expenses'], 'Capital payments are cash items'),
                ('The closing balance of a receipts and payments account shows', 'the cash and bank balance at the end of the year', ['the surplus for the year', 'the accumulated fund', 'subscriptions in arrears'], 'Cash only'),
                ('Opening bank $1,200; receipts $9,800; payments $8,400. Closing bank is', '$2,600', ['$200', '$19,400', '$600'], '1,200 + 9,800 − 8,400'),
                ('A limitation of a receipts and payments account is that it', 'ignores accruals, prepayments and depreciation', ['shows too much detail', 'cannot show cash', 'is not used by clubs'], 'Not on accruals basis')],
          exps=[('Distinguish between a receipts and payments account and an income and expenditure account.', 'R&P summarises actual cash received and paid (capital and revenue); I&E records income and expenditure of the period on the accruals basis, showing a surplus or deficit.', 'R&P – cash, all items [1]; I&E – accruals, revenue items, surplus [1] [2]'),
                ('Explain why members of a club need an income and expenditure account as well as a receipts and payments account.', 'The R&P account does not show whether the club covered its running costs in the year; the I&E shows the true surplus or deficit after accruals and depreciation.', 'R&P shows only cash [1]; I&E shows surplus/deficit [1] [2]')],
          disc=[('Discuss whether the treasurer of {c} should be allowed to report to members using only a receipts and payments account.', 'It is simple and shows cash, but omits amounts owing, depreciation and assets, so members cannot judge whether the club is viable.', 'Simple/cash [1]; omissions [1]; judgement [1] [3]')])


@spec(t16_1)
def t161_rp(r, D):
    c = r.choice(CLUBS)
    ob = step(r, 300, 5000, 10)
    rec = [('subscriptions', step(r, 4000, 20000, 10)), ('competition entry fees', step(r, 500, 3000, 10)), ('bar sales', step(r, 3000, 15000, 10))][:2 + (D >= 3)]
    pay = [('rent of clubhouse', step(r, 2000, 9000, 10)), ('coaching fees', step(r, 1000, 6000, 10)), ('new equipment', step(r, 1000, 7000, 10))] + ([('bar purchases', step(r, 2000, 9000, 10))] if D >= 3 else [])
    cb = ob + sum(v for _, v in rec) - sum(v for _, v in pay)
    setup = f'The treasurer of {c} provides the following information for the year: bank balance at 1 January {m(ob)}; receipts – ' + ', '.join(f'{n} {m(v)}' for n, v in rec) + '; payments – ' + ', '.join(f'{n} {m(v)}' for n, v in pay) + '.'
    parts = [('Prepare the receipts and payments account and find the closing balance.', f'{m(abs(cb))} {"in the bank" if cb >= 0 else "overdrawn"}', f'{m(ob)} + {m(sum(v for _, v in rec))} − {m(sum(v for _, v in pay))} = {m(cb)} [2]'),
             ('Identify the payment that would not appear in the income and expenditure account and explain why.', 'New equipment – it is capital expenditure; only its depreciation appears in the I&E account.', 'New equipment [1]; capital/depreciation [1] [2]')]
    wrong = ob + sum(v for _, v in rec) - sum(v for n, v in pay if n != 'new equipment')
    return {'setup': setup, 'parts': parts, 'ctx': {'c': c},
            'mcq': ('What is the bank balance at 31 December?', *num_opts(m, cb, [wrong, cb - ob, cb + 2 * ob]), f'{m(ob)} + receipts − payments'),
            'err': (f'calculated the closing bank balance as {m(wrong)}', 'the payment for new equipment was left out because it is capital; the receipts and payments account includes ALL cash paid', m(cb), f'{m(ob)} + {m(sum(v for _, v in rec))} − {m(sum(v for _, v in pay))}', 'closing balance')}


t16_2 = A(16, 'Subscriptions accounts with arrears and advances', ['subscriptions accounts with arrears and advances', 'subscriptions', 'arrears and advances'],
          mcqs=[('Subscriptions received in advance at the year end are shown as', 'a current liability', ['a current asset', 'income of the year', 'part of the accumulated fund'], 'Owed to members'),
                ('Subscriptions in arrears at the year end are', 'a current asset (if expected to be received)', ['a current liability', 'an expense', 'ignored'], 'Amounts owed by members'),
                ('Received $8,000; arrears at start $300 (all received); in advance at end $500. Subscriptions income is', '$7,200', ['$8,200', '$8,800', '$7,800'], '8,000 − 300 − 500'),
                ('A prudent club may decide to', 'treat subscriptions in arrears as income only when received', ['include all arrears as income', 'treat advances as income', 'ignore all subscriptions'], 'Prudence'),
                ('Life membership fees are often', 'credited to a deferred income account and released over several years', ['treated as income in the year received', 'added to the accumulated fund directly', 'shown as a current asset'], 'Matching')],
          exps=[('Explain why subscriptions received in advance are not income of the current year.', 'They relate to membership of a future year; under the accruals concept they become income in the year they cover, so they are a liability now.', 'Relate to future year [1]; accruals/liability [1] [2]'),
                ('Explain why a club might not include subscriptions in arrears in its income.', 'Members who have not paid may have left and never pay; prudence suggests recognising them only when received.', 'Uncertain collection [1]; prudence [1] [2]')],
          disc=[('Suggest how {c} could reduce subscriptions in arrears.', 'Payment by direct debit; reminders; suspend membership rights for non-payment; discount for early payment.', 'Two methods [1 each] [2]')])


@spec(t16_2)
def t162_sub(r, D):
    c = r.choice(CLUBS)
    rec = step(r, 5000, 25000, 10)
    oa, oadv = step(r, 100, 1500, 10), (step(r, 100, 1500, 10) if D >= 3 else 0)
    ca, cadv = (step(r, 100, 1500, 10) if D >= 2 else 0), step(r, 100, 1500, 10)
    inc = rec - oa + ca + oadv - cadv
    setup = f'{c} received subscriptions of {m(rec)} during the year ended 31 December. At 1 January subscriptions in arrears were {m(oa)}' + (f' and subscriptions in advance were {m(oadv)}' if oadv else '') + \
        f'. At 31 December subscriptions in arrears were {m(ca)} and subscriptions in advance were {m(cadv)}.'
    w = f'{m(rec)} − {m(oa)}' + (f' + {m(oadv)}' if oadv else '') + f' + {m(ca)} − {m(cadv)} = {m(inc)}'
    parts = [('Calculate the subscriptions income for the year.', m(inc), f'{w} [3]'),
             ('Prepare the subscriptions account for the year.', w, f'Opening arrears Dr, advances Cr [1]; bank {m(rec)} Cr [1]; income to I&E Dr {m(inc)} [1]; closing balances c/d [1] [4]'),
             ('State how the closing balances appear in the statement of financial position.', f'Arrears {m(ca)} – current asset; advances {m(cadv)} – current liability.', 'Arrears CA [1]; advances CL [1] [2]')]
    wrong = rec + oa - ca - oadv + cadv
    return {'setup': setup, 'parts': parts, 'ctx': {'c': c},
            'mcq': ('What is the subscriptions income for the year?', *num_opts(m, inc, [wrong, rec, rec + cadv]), w),
            'err': (f'calculated subscriptions income as {m(wrong)}', 'every adjustment was reversed: opening arrears are deducted, closing arrears added, opening advances added and closing advances deducted', m(inc), w.split(' = ')[0], 'subscriptions income') if wrong != inc else None}


t16_3 = A(16, 'Income and expenditure account and accumulated fund', ['income and expenditure account and accumulated fund', 'income and expenditure account', 'accumulated fund'],
          mcqs=[('The accumulated fund of a club is equivalent to', 'the capital of a business', ['the profit of a business', 'the bank balance', 'the drawings of a business'], 'Net assets'),
                ('An excess of income over expenditure is called', 'a surplus', ['a profit', 'a gain on disposal', 'working capital'], 'Not-for-profit terminology'),
                ('Opening assets of a club $45,000, liabilities $3,000. The accumulated fund is', '$42,000', ['$48,000', '$45,000', '$3,000'], 'Assets − liabilities'),
                ('Which item appears in the income and expenditure account?', 'Depreciation of equipment', ['Purchase of equipment', 'Opening bank balance', 'Loan received'], 'Accruals-based expense'),
                ('A deficit for the year is', 'deducted from the accumulated fund', ['added to the accumulated fund', 'shown as a current liability', 'ignored'], 'Reduces net assets')],
          exps=[('Explain why a club uses the terms surplus and deficit instead of profit and loss.', 'A club exists to provide facilities for members, not to make a profit; a surplus simply means income exceeded expenditure.', 'Not-for-profit purpose [1]; meaning of surplus [1] [2]'),
                ('Explain how the accumulated fund at the start of the year is calculated.', 'From the opening statement of affairs: total assets (equipment, inventory, bank, arrears, prepayments) less liabilities (payables, accruals, advances).', 'Assets − liabilities [1]; examples [1] [2]')],
          disc=[('Evaluate whether {c} should raise its annual subscription.', 'A deficit or planned equipment purchases suggest raising it, but members may leave; alternatives include fundraising events or cutting costs.', 'Reason to raise [1]; risk [1]; judgement/alternative [1] [3]')])


@spec(t16_3)
def t163_ie(r, D):
    c = r.choice(CLUBS)
    eq, bank, arr = step(r, 10000, 50000, 100), step(r, 500, 6000, 10), step(r, 100, 1000, 10)
    acc_ = step(r, 100, 1000, 10)
    af = eq + bank + arr - acc_
    subs = step(r, 8000, 25000, 10)
    other = [('competition fees', step(r, 500, 3000, 10))] + ([('bar profit', step(r, 500, 4000, 10))] if D >= 3 else [])
    exps = [('rent', step(r, 2000, 8000, 10)), ('coaching', step(r, 1000, 6000, 10)), ('general expenses', step(r, 500, 3000, 10))]
    dep = eq * r.choice([10, 20]) // 100
    surplus = subs + sum(v for _, v in other) - sum(v for _, v in exps) - dep
    setup = (f'At 1 January {c} had equipment {m(eq)}, bank {m(bank)}, subscriptions in arrears {m(arr)} and expenses owing {m(acc_)}. For the year its income was: subscriptions {m(subs)}, ' + ', '.join(f'{n} {m(v)}' for n, v in other) +
             '; expenditure was: ' + ', '.join(f'{n} {m(v)}' for n, v in exps) + f'; depreciation of equipment was {m(dep)}.')
    parts = [('Calculate the accumulated fund at 1 January.', m(af), f'{m(eq)} + {m(bank)} + {m(arr)} − {m(acc_)} = {m(af)} [2]'),
             ('Calculate the surplus or deficit for the year.', f'{"Surplus" if surplus >= 0 else "Deficit"} {m(abs(surplus))}', f'Income {m(subs + sum(v for _, v in other))} − expenditure {m(sum(v for _, v in exps) + dep)} = {m(surplus)} [2]'),
             ('Calculate the accumulated fund at 31 December.', m(af + surplus), f'{m(af)} {"+" if surplus >= 0 else "−"} {m(abs(surplus))} = {m(af + surplus)} [1]')]
    wrong = eq + bank + arr + acc_
    return {'setup': setup, 'parts': parts, 'ctx': {'c': c},
            'mcq': ('What is the accumulated fund at 1 January?', *num_opts(m, af, [wrong, eq + bank, af + arr]), f'Assets − liabilities = {m(af)}'),
            'err': (f'calculated the opening accumulated fund as {m(wrong)}', 'expenses owing (a liability) were added instead of deducted', m(af), f'{m(eq + bank + arr)} − {m(acc_)}', 'accumulated fund')}


t16_4 = A(16, 'Trading activities of clubs (bar or café profit)', ['trading activities of clubs (bar or café profit)', 'bar profit', 'trading activities of clubs'],
          mcqs=[('Bar profit of a club is shown', 'as income in the income and expenditure account', ['in the receipts and payments account only', 'as part of the accumulated fund', 'as an expense'], 'Net result of trading'),
                ('Bar sales $12,000; cost of bar sales $7,500; bar wages $2,000. Bar profit is', '$2,500', ['$4,500', '$9,500', '$5,500'], '12,000 − 7,500 − 2,000'),
                ('Bar purchases are found by', 'payments to bar suppliers + closing bar payables − opening bar payables', ['payments − closing payables', 'bar sales − bar profit', 'opening inventory + closing inventory'], 'Reconstruct the payables account'),
                ('Why does a club prepare a separate bar trading account?', 'To show whether the bar is making a profit or loss', ['Because it is required by law', 'To calculate subscriptions', 'To find the accumulated fund'], 'Assess the trading activity'),
                ('Which cost is normally deducted in the bar trading account?', 'Wages of bar staff', ['Rent of the whole clubhouse', 'Coaching fees', 'Depreciation of sports equipment'], 'Direct bar costs')],
          exps=[('Explain why a club calculates the profit of its bar separately.', 'Trading is not the club\'s main purpose, so members want to know whether the bar adds to or drains the club\'s funds and whether prices are set correctly.', 'Assess bar performance [1]; decisions on prices/continuation [1] [2]'),
                ('Explain why bar purchases are not the same as payments to bar suppliers.', 'Payments include amounts owed from last year and exclude amounts still owing at the year end; purchases are adjusted for opening and closing payables.', 'Payables adjustment [1]; accruals concept [1] [2]')],
          disc=[('Discuss whether {c} should close its bar if it makes a small loss.', 'The bar may attract members and visitors, increasing subscriptions; prices or costs could be changed instead; but a continuing loss uses members\' funds.', 'Non-financial benefit [1]; alternatives [1]; judgement [1] [3]')])


@spec(t16_4)
def t164_bar(r, D):
    c = r.choice(CLUBS)
    bs = step(r, 8000, 30000, 10)
    oi, ci = step(r, 500, 3000, 10), step(r, 500, 3000, 10)
    pay = step(r, int(bs * 0.4), int(bs * 0.6), 10)
    op_, cp_ = (step(r, 200, 1500, 10), step(r, 200, 1500, 10)) if D >= 2 else (0, 0)
    pur = pay + cp_ - op_
    cos = oi + pur - ci
    wg = step(r, 1000, 5000, 10) if D >= 3 else 0
    bp = bs - cos - wg
    setup = f'{c} runs a bar. For the year: bar sales {m(bs)}; payments to bar suppliers {m(pay)}; bar inventory {m(oi)} at the start and {m(ci)} at the end' + (f'; amounts owing to bar suppliers {m(op_)} at the start and {m(cp_)} at the end' if op_ else '') + (f'; bar wages {m(wg)}' if wg else '') + '.'
    parts = [('Calculate the bar purchases for the year.', m(pur), f'{m(pay)} + {m(cp_)} − {m(op_)} = {m(pur)} [1]' if op_ else f'Payments = purchases {m(pur)} [1]'),
             ('Calculate the bar profit or loss.', f'{"Profit" if bp >= 0 else "Loss"} {m(abs(bp))}', f'COS {m(oi)} + {m(pur)} − {m(ci)} = {m(cos)} [1]; {m(bs)} − {m(cos)}' + (f' − {m(wg)}' if wg else '') + f' = {m(bp)} [1] [2]'),
             ('State where the bar profit is shown in the club\'s financial statements.', 'As income (or as a deduction if a loss) in the income and expenditure account.', 'I&E account [1]')]
    wrong = bs - (oi + pay - ci) - wg
    return {'setup': setup, 'parts': parts, 'ctx': {'c': c},
            'mcq': ('What is the bar profit (loss)?', *num_opts(m, bp, [wrong, bs - pur, bs - cos]), f'{m(bs)} − {m(cos)} − {m(wg)}'),
            'err': (f'calculated the bar profit as {m(wrong)}', 'payments to suppliers were used as purchases without adjusting for the amounts owing at the start and end of the year', f'{m(bp)}', f'{m(bs)} − ({m(oi)} + {m(pur)} − {m(ci)})' + (f' − {m(wg)}' if wg else ''), 'bar profit') if wrong != bp else None}


CHAPTERS[16] = [t16_1, t16_2, t16_3, t16_4]


# ===================================================================== 17 Manufacturing accounts
def _mfg(r, D):
    d = {'orm': step(r, 3000, 15000, 100), 'prm': step(r, 40000, 120000, 100), 'cin': step(r, 500, 3000, 10) if D >= 2 else 0, 'crm': step(r, 3000, 15000, 100),
         'dl': step(r, 30000, 90000, 100), 'roy': step(r, 1000, 6000, 100) if D >= 3 else 0,
         'il': step(r, 8000, 25000, 100), 'frent': step(r, 5000, 15000, 100), 'fdep': step(r, 3000, 12000, 100), 'fpow': step(r, 2000, 9000, 100),
         'owip': step(r, 2000, 10000, 100) if D >= 3 else 0, 'cwip': step(r, 2000, 10000, 100) if D >= 3 else 0}
    d['dm'] = d['orm'] + d['prm'] + d['cin'] - d['crm']
    d['pc'] = d['dm'] + d['dl'] + d['roy']
    d['foh'] = d['il'] + d['frent'] + d['fdep'] + d['fpow']
    d['cop'] = d['pc'] + d['foh'] + d['owip'] - d['cwip']
    return d


def _mfg_text(d):
    s = f'raw materials inventory {m(d["orm"])} at the start and {m(d["crm"])} at the end of the year; purchases of raw materials {m(d["prm"])}' + (f'; carriage inwards on raw materials {m(d["cin"])}' if d['cin'] else '')
    s += f'; direct wages {m(d["dl"])}' + (f'; royalties paid per unit produced {m(d["roy"])}' if d['roy'] else '')
    s += f'; indirect factory wages {m(d["il"])}; factory rent {m(d["frent"])}; depreciation of factory machinery {m(d["fdep"])}; factory power {m(d["fpow"])}'
    if d['owip'] or d['cwip']:
        s += f'; work in progress {m(d["owip"])} at the start and {m(d["cwip"])} at the end'
    return s


t17_1 = A(17, 'Prime cost, factory overheads and cost of production', ['prime cost, factory overheads and cost of production', 'prime cost', 'factory overheads', 'cost of production'],
          mcqs=[('Prime cost is', 'direct materials + direct labour + direct expenses', ['direct materials + factory overheads', 'total factory cost − direct labour', 'cost of production + work in progress'], 'All direct costs'),
                ('Which is a factory overhead?', 'Wages of factory supervisors', ['Wages of machine operators', 'Raw materials used', 'Royalties per unit'], 'Indirect labour'),
                ('Royalties paid for each unit manufactured are', 'a direct expense, part of prime cost', ['a factory overhead', 'an administration expense', 'a selling expense'], 'They vary directly with output'),
                ('Carriage inwards on raw materials is included in', 'the cost of raw materials consumed', ['factory overheads', 'administration expenses', 'distribution costs'], 'Cost of getting materials into the factory'),
                ('Office salaries are shown in', 'the income statement, not the manufacturing account', ['prime cost', 'factory overheads', 'cost of raw materials'], 'Non-factory cost')],
          exps=[('Distinguish between direct costs and indirect costs in a manufacturing business.', 'Direct costs can be traced to each unit produced (materials, production wages, royalties); indirect costs are factory costs that cannot be traced to units (supervisors, factory rent, power).', 'Direct – traceable to units [1]; indirect – cannot be traced [1] [2]'),
                ('Explain why the manufacturing account is prepared separately from the income statement.', 'It shows the cost of producing the goods in the factory, separating production costs from selling and administration costs, so management can control factory costs.', 'Shows cost of production [1]; control of factory costs [1] [2]')],
          disc=[('Suggest two ways {f} could reduce its cost of production.', 'Buy materials in bulk/cheaper suppliers; reduce wastage; improve labour productivity/automation; reduce factory overheads such as power.', 'Two valid ways [1 each] [2]')])


@spec(t17_1)
def t171_pc(r, D):
    f = firm(r)
    d = _mfg(r, D)
    setup = f'{f} manufactures furniture. For the year ended 31 December: {_mfg_text(d)}.'
    parts = [('Calculate the cost of raw materials consumed.', m(d['dm']), f'{m(d["orm"])} + {m(d["prm"])}' + (f' + {m(d["cin"])}' if d['cin'] else '') + f' − {m(d["crm"])} = {m(d["dm"])} [2]'),
             ('Calculate the prime cost.', m(d['pc']), f'{m(d["dm"])} + {m(d["dl"])}' + (f' + {m(d["roy"])}' if d['roy'] else '') + f' = {m(d["pc"])} [1]'),
             ('Calculate the total factory overheads and the cost of production.', f'Overheads {m(d["foh"])}; cost of production {m(d["cop"])}', f'Overheads {m(d["foh"])} [1]; {m(d["pc"])} + {m(d["foh"])}' + (f' + {m(d["owip"])} − {m(d["cwip"])}' if d['owip'] else '') + f' = {m(d["cop"])} [1] [2]')]
    wrong = d['pc'] + d['il']
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the prime cost?', *num_opts(m, d['pc'], [wrong, d['dm'], d['pc'] + d['foh']]), f'{m(d["dm"])} + {m(d["dl"])} + {m(d["roy"])}'),
            'err': (f'calculated prime cost as {m(wrong)}', 'indirect factory wages were included; they are a factory overhead, not a direct cost', m(d['pc']), f'{m(d["dm"])} + {m(d["dl"])}' + (f' + {m(d["roy"])}' if d['roy'] else ''), 'prime cost')}


t17_2 = A(17, 'Inventories of raw materials, work in progress and finished goods', ['inventories of raw materials, work in progress and finished goods', 'work in progress', 'finished goods', 'raw materials'],
          mcqs=[('Work in progress is', 'partly completed goods at the end of the period', ['raw materials not yet used', 'finished goods awaiting sale', 'goods returned by customers'], 'Partly manufactured'),
                ('Closing work in progress is', 'deducted in the manufacturing account to find the cost of production', ['added to prime cost', 'shown in the income statement', 'deducted from sales'], 'Not yet completed'),
                ('Finished goods inventory is used in calculating', 'cost of sales in the income statement', ['prime cost', 'factory overheads', 'raw materials consumed'], 'Opening FG + cost of production − closing FG'),
                ('How many types of inventory may a manufacturer show in its statement of financial position?', 'Three: raw materials, work in progress and finished goods', ['One: finished goods', 'Two: raw materials and finished goods', 'Four, including factory overheads'], 'All are current assets'),
                ('Cost of production $150,000; opening finished goods $12,000; closing finished goods $15,000. Cost of sales is', '$147,000', ['$153,000', '$150,000', '$177,000'], '12,000 + 150,000 − 15,000')],
          exps=[('Explain where each of the three types of inventory is used in the financial statements of a manufacturer.', 'Raw materials: manufacturing account (materials consumed); work in progress: manufacturing account (adjusting total factory cost); finished goods: income statement (cost of sales); all three closing inventories are current assets.', 'RM and WIP – manufacturing account [1]; FG – income statement [1]; all CA [1] [3]'),
                ('Explain why work in progress is valued at factory cost.', 'Partly finished goods have absorbed materials, labour and overheads; valuing them at factory cost matches costs to the goods completed in each period.', 'Includes production costs [1]; matching [1] [2]')],
          disc=[('Discuss the problems {f} may face in valuing work in progress.', 'It is hard to measure the stage of completion and the share of overheads; errors affect cost of production and profit.', 'Stage of completion [1]; overhead share [1]; effect on profit [1] [3]')])


@spec(t17_2)
def t172_inv(r, D):
    f = firm(r)
    d = _mfg(r, max(3, D))
    ofg, cfg = step(r, 5000, 20000, 100), step(r, 5000, 20000, 100)
    cos = ofg + d['cop'] - cfg
    sales = step(r, int(cos * 1.2), int(cos * 1.6), 100)
    setup = f'{f} manufactures bicycles. For the year: {_mfg_text(d)}. Finished goods inventory was {m(ofg)} at the start and {m(cfg)} at the end of the year; revenue was {m(sales)}.'
    parts = [('Calculate the cost of production.', m(d['cop']), f'Prime cost {m(d["pc"])} + overheads {m(d["foh"])} + {m(d["owip"])} − {m(d["cwip"])} = {m(d["cop"])} [3]'),
             ('Calculate the cost of sales and gross profit.', f'Cost of sales {m(cos)}; gross profit {m(sales - cos)}', f'{m(ofg)} + {m(d["cop"])} − {m(cfg)} = {m(cos)} [1]; GP {m(sales - cos)} [1] [2]'),
             ('State the total value of inventories shown in the statement of financial position.', m(d['crm'] + d['cwip'] + cfg), f'{m(d["crm"])} + {m(d["cwip"])} + {m(cfg)} = {m(d["crm"] + d["cwip"] + cfg)} [1]')]
    wrong = d['pc'] + d['foh'] - d['owip'] + d['cwip']
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the cost of production?', *num_opts(m, d['cop'], [wrong, d['pc'] + d['foh'], d['pc']]), f'{m(d["pc"] + d["foh"])} + {m(d["owip"])} − {m(d["cwip"])}'),
            'err': (f'calculated the cost of production as {m(wrong)}', 'the work-in-progress adjustment was reversed: opening WIP is added and closing WIP deducted', m(d['cop']), f'{m(d["pc"] + d["foh"])} + {m(d["owip"])} − {m(d["cwip"])}', 'cost of production') if d['owip'] != d['cwip'] else None}


t17_3 = A(17, 'Manufacturing profit and unrealised profit on inventory', ['manufacturing profit and unrealised profit on inventory', 'manufacturing profit', 'unrealised profit'],
          mcqs=[('Goods are transferred from the factory at cost plus 25%. Closing finished goods at transfer price are $20,000. The unrealised profit is', '$4,000', ['$5,000', '$16,000', '$25,000'], '20,000 × 25/125'),
                ('An increase in the provision for unrealised profit is', 'deducted from the manufacturing profit in the income statement', ['added to gross profit', 'shown as a current liability', 'added to finished goods'], 'Reduces profit'),
                ('Why do some manufacturers transfer goods at a price above cost?', 'To measure the efficiency of the factory compared with buying the goods in', ['To increase total profit', 'To reduce tax', 'To increase inventory values'], 'Factory treated as a profit centre'),
                ('In the statement of financial position, finished goods are shown at', 'transfer price less the provision for unrealised profit (i.e. cost)', ['transfer price', 'selling price', 'transfer price plus manufacturing profit'], 'Prudence/realisation'),
                ('Manufacturing profit is', 'the market value (transfer price) of goods produced less the cost of production', ['revenue less cost of sales', 'gross profit less expenses', 'prime cost less overheads'], 'Factory profit')],
          exps=[('Explain why a provision for unrealised profit is needed when goods are transferred at a profit.', 'The factory profit on goods still unsold has not been realised by a sale to an outside customer; the provision removes it so inventory is at cost and profit is not overstated.', 'Profit not realised by external sale [1]; inventory at cost/profit not overstated [1] [2]'),
                ('Explain why only the change in the provision for unrealised profit is charged in the income statement.', 'The opening provision was charged in an earlier year; only the increase (or decrease) relates to the current year.', 'Opening already charged [1]; change only [1] [2]')],
          disc=[('Evaluate whether {f} should use a factory transfer price above cost.', 'It helps judge factory efficiency against outside suppliers and can motivate managers, but it adds complexity and the unrealised-profit adjustment; total profit is unchanged.', 'Benefit [1]; complexity/no change in total profit [1]; judgement [1] [3]')])


@spec(t17_3)
def t173_up(r, D):
    f = firm(r)
    mu = r.choice([10, 20, 25, 50])
    cop = step(r, 100000, 300000, 1000)
    tp = cop * (100 + mu) / 100
    mp = tp - cop
    k = (100 + mu)
    ofg_tp = step(r, 5000, 30000, k * 10)
    cfg_tp = step(r, 5000, 30000, k * 10)
    if cfg_tp == ofg_tp:
        cfg_tp += k * 10
    op_up, cl_up = ofg_tp * mu / k, cfg_tp * mu / k
    ch = cl_up - op_up
    setup = f'{f} transfers goods from its factory to its warehouse at cost plus {mu}%. The cost of production for the year was {m(cop)}. Finished goods inventory, valued at transfer price, was {m(ofg_tp)} at the start and {m(cfg_tp)} at the end of the year.'
    parts = [('Calculate the manufacturing profit for the year.', m(mp), f'{m(cop)} × {mu}% = {m(mp)} [1]'),
             ('Calculate the provision for unrealised profit at the end of the year and the change in the provision.', f'Closing provision {m(cl_up)}; {"increase" if ch > 0 else "decrease"} {m(abs(ch))}', f'{m(cfg_tp)} × {mu}/{k} = {m(cl_up)} [1]; opening {m(ofg_tp)} × {mu}/{k} = {m(op_up)} [1]; change {m(ch)} [1] [3]'),
             ('State the value of closing finished goods in the statement of financial position.', m(cfg_tp - cl_up), f'{m(cfg_tp)} − {m(cl_up)} = {m(cfg_tp - cl_up)} [1]')]
    wrong = cfg_tp * mu / 100
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the provision for unrealised profit on closing finished goods?', *num_opts(m, cl_up, [wrong, ch, cfg_tp - cl_up]), f'{m(cfg_tp)} × {mu}/{k}'),
            'err': (f'calculated the closing provision for unrealised profit as {m(wrong)}', f'{mu}% was applied to the transfer price; the profit element is {mu}/{k} of the transfer price because the mark-up is on cost', m(cl_up), f'{m(cfg_tp)} × {mu}/{k}', 'provision')}


CHAPTERS[17] = [t17_1, t17_2, t17_3]


# ===================================================================== 18 Limited company accounts
NOMS = [0.25, 0.5, 1.0]


def nom(x):
    return f'${x:.2f}'


t18_1 = A(18, 'Features of limited companies: limited liability, shares and debentures', ['features of limited companies: limited liability, shares and debentures', 'limited liability', 'debentures', 'features of limited companies'],
          mcqs=[('Limited liability means that shareholders', 'can lose no more than the amount they have paid or agreed to pay for their shares', ['are never liable for any company debts', 'are personally liable for all company debts', 'cannot lose their investment'], 'Liability limited to share capital'),
                ('Debenture interest is', 'an expense (finance cost) that must be paid whether or not a profit is made', ['an appropriation of profit', 'paid only if the directors decide', 'a dividend to shareholders'], 'Debenture holders are lenders'),
                ('Which is a feature of a public limited company (plc)?', 'Its shares can be offered to the general public', ['It has unlimited liability', 'It must have only one shareholder', 'It cannot issue debentures'], 'Shares traded publicly'),
                ('Debenture holders are', 'lenders to the company', ['owners of the company', 'directors of the company', 'preference shareholders'], 'A debenture is a long-term loan'),
                ('A company is a separate legal entity. This means it', 'can own assets, sue and be sued in its own name', ['must be run by its shareholders', 'has no liability for its debts', 'cannot borrow money'], 'Separate legal personality')],
          exps=[('Distinguish between a shareholder and a debenture holder.', 'A shareholder is an owner who receives dividends at the directors\' discretion and has voting rights (ordinary shares); a debenture holder is a lender who receives fixed interest, which must be paid, and is repaid before shareholders on liquidation.', 'Owner vs lender [1]; dividend vs fixed interest/priority [1] [2]'),
                ('Explain two advantages to a sole trader of converting the business into a private limited company.', 'Limited liability protects personal assets; easier to raise capital by selling shares; separate legal entity gives continuity.', 'Two advantages explained [1 each] [2]')],
          disc=[('Evaluate whether {co} should raise new finance by issuing debentures rather than ordinary shares.', 'Debentures: interest is a fixed cost and raises gearing but does not dilute control; shares: no compulsory return but dilute ownership and cost more to issue.', 'Debenture point [1]; share point [1]; judgement [1] [3]')])


@spec(t18_1)
def t181_feat(r, D):
    c = co(r)
    p = pp(r)
    n = step(r, 1000, 20000, 500)
    nm_ = r.choice(NOMS)
    paid = nm_ + step(r, 10, 200, 10) / 100
    deb = step(r, 50000, 400000, 10000)
    rate = r.choice([4, 5, 6, 7, 8])
    pfo = step(r, -20000, 80000, 1000) if D >= 3 else step(r, 30000, 80000, 1000)
    di = deb * rate // 100
    setup = f'{p} bought {n:,} ordinary shares of {nom(nm_)} each in {c}, paying {m2(paid)} per share. The company also has {m(deb)} of {rate}% debentures. This year it made a profit from operations of {m(pfo)}' + (' (a loss)' if pfo < 0 else '') + '.'
    parts = [(f'Calculate the maximum amount {p} could lose if {c} went into liquidation.', m2(n * paid), f'{n:,} × {m2(paid)} = {m2(n * paid)} [1]; limited liability – no further personal liability [1] [2]'),
             ('Calculate the debenture interest for the year and state how it is treated.', f'{m(di)}; a finance cost in the income statement, payable even if there is a loss', f'{rate}% × {m(deb)} = {m(di)} [1]; finance cost/expense [1] [2]'),
             (f'Explain whether {p} is guaranteed to receive a dividend this year.', 'No – ordinary dividends are paid only if the directors declare them out of distributable profits; debenture interest must be paid first.', 'Directors\' discretion [1]; priority of debenture interest [1] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('What is the annual debenture interest?', *num_opts(m, di, [deb * rate / 10, di * 2, n * nm_ * rate / 100]), f'{rate}% × {m(deb)}'),
            'err': (f'said that {p} could lose {m2(n * nm_)}', 'the nominal value was used; the shareholder\'s risk is the amount actually paid for the shares', m2(n * paid), f'{n:,} × {m2(paid)}', 'maximum loss')}


t18_2 = A(18, 'Equity: ordinary and preference shares, reserves', ['equity: ordinary and preference shares, reserves', 'preference shares', 'ordinary shares', 'equity'],
          mcqs=[('Preference shareholders usually receive', 'a fixed rate of dividend before ordinary shareholders', ['a variable dividend after ordinary shareholders', 'interest that must be paid by law', 'voting control of the company'], 'Priority, fixed rate'),
                ('Ordinary shareholders normally have', 'voting rights and the right to the residual profits', ['a fixed dividend', 'priority on liquidation over all others', 'no risk'], 'Owners of the company'),
                ('Equity in a company consists of', 'share capital plus reserves', ['share capital plus debentures', 'reserves plus current liabilities', 'total assets'], 'Shareholders\' funds'),
                ('6% preference shares of $200,000 entitle holders to an annual dividend of', '$12,000', ['$6,000', '$1,200', '$120,000'], '6% × 200,000'),
                ('The issued share capital of a company is', 'the nominal value of shares actually issued to shareholders', ['the maximum the company may issue', 'the market value of the shares', 'share capital plus share premium'], 'Issued at nominal value')],
          exps=[('Distinguish between ordinary shares and preference shares.', 'Ordinary shares carry votes and a variable dividend paid after preference dividends; preference shares have a fixed dividend paid first and priority for repayment, but usually no votes.', 'Ordinary – votes, variable, last [1]; preference – fixed, priority, no votes [1] [2]'),
                ('Explain why a company keeps retained earnings rather than paying them all as dividends.', 'To finance growth and replacement of assets without borrowing, to keep a buffer for poor years and to maintain liquidity.', 'Internal finance for growth [1]; buffer/liquidity [1] [2]')],
          disc=[('Discuss whether an investor should buy preference shares or ordinary shares in {co}.', 'Preference: lower risk, fixed income, no votes; ordinary: higher risk, higher potential return and capital growth, control; depends on the investor\'s attitude to risk.', 'Preference features [1]; ordinary features [1]; judgement [1] [3]')])


@spec(t18_2)
def t182_div(r, D):
    c = co(r)
    nm_ = r.choice(NOMS)
    ns = step(r, 100000, 800000, 50000)
    oc = ns * nm_
    pref = step(r, 50000, 200000, 10000) if D >= 2 else 0
    prate = r.choice([5, 6, 7, 8])
    dps = r.choice([4, 5, 6, 8, 10, 12, 15]) / 100
    pd = pref * prate / 100
    od = ns * dps
    pfy = step(r, int(pd + od + 10000), int(pd + od + 120000), 1000)
    setup = f'{c} has issued {ns:,} ordinary shares of {nom(nm_)} each' + (f' and {m(pref)} of {prate}% preference shares of $1 each' if pref else '') + f'. Profit for the year was {m(pfy)}. The directors paid the preference dividend and an ordinary dividend of {int(dps * 100)} cents per share.' if pref else \
        f'{c} has issued {ns:,} ordinary shares of {nom(nm_)} each. Profit for the year was {m(pfy)}. The directors paid an ordinary dividend of {int(dps * 100)} cents per share.'
    parts = [('Calculate the total ordinary dividend paid.', m(od), f'{ns:,} shares × {m2(dps)} = {m(od)} [2]')]
    if pref:
        parts.append(('Calculate the preference dividend.', m(pd), f'{prate}% × {m(pref)} = {m(pd)} [1]'))
    parts.append(('Calculate the profit retained for the year.', m(pfy - pd - od), f'{m(pfy)} − {m(pd)} − {m(od)} = {m(pfy - pd - od)} [1]'))
    parts.append(('State the value of the ordinary share capital in the statement of financial position.', m(oc), f'{ns:,} × {nom(nm_)} = {m(oc)} [1]'))
    wrong = oc * dps
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('What is the total ordinary dividend?', *num_opts(m, od, [wrong, od * nm_ if nm_ != 1 else od / 2, ns * dps * 2]), f'{ns:,} × {m2(dps)}'),
            'err': (f'calculated the ordinary dividend as {m(wrong)}', 'the dividend per share was applied to the nominal value of share capital instead of to the number of shares', m(od), f'{ns:,} × {m2(dps)}', 'ordinary dividend') if abs(wrong - od) > 0.5 else None}


t18_3 = A(18, 'Income statement and statement of financial position of a limited company', ['income statement and statement of financial position of a limited company', 'limited company income statement', 'statement of financial position of a limited company'],
          mcqs=[('In a company income statement, debenture interest is shown as', 'a finance cost deducted after profit from operations', ['an appropriation of profit', 'part of cost of sales', 'a deduction from share capital'], 'Finance costs'),
                ('Directors\' fees are', 'an expense of the company', ['a dividend', 'an appropriation of profit', 'part of share capital'], 'Directors are employees/officers'),
                ('Tax on company profits is shown', 'in the income statement, with any unpaid tax as a current liability', ['only as a current liability', 'as part of equity', 'as a non-current asset'], 'Income tax expense'),
                ('Dividends paid are shown in', 'the statement of changes in equity, not the income statement', ['the income statement as an expense', 'current liabilities always', 'non-current liabilities'], 'Distributions to owners'),
                ('Debentures repayable in 2035 are shown as', 'non-current liabilities', ['equity', 'current liabilities', 'current assets'], 'Long-term loan')],
          exps=[('Explain why debenture interest is deducted in the income statement but dividends are not.', 'Debenture interest is a cost of borrowing (an expense) that must be paid; dividends are distributions of profit to owners and are shown in the statement of changes in equity.', 'Interest – expense of borrowing [1]; dividends – distribution to owners/SOCE [1] [2]'),
                ('Explain why a company\'s income statement shows a tax charge but a sole trader\'s does not.', 'A company is a separate legal entity taxed on its profits; a sole trader\'s profit is taxed as the owner\'s personal income.', 'Company taxed separately [1]; sole trader – personal tax [1] [2]')],
          disc=[('Assess whether {co} has made enough profit to justify paying a larger dividend.', 'Compare profit for the year with dividends; consider retained earnings needed for investment, liquidity and debenture repayments.', 'Uses profit/dividend figures [1]; need for retained earnings/liquidity [1]; judgement [1] [3]')])


@spec(t18_3)
def t183_is(r, D):
    c = co(r)
    rev = step(r, 400000, 1500000, 1000)
    cos = step(r, int(rev * 0.45), int(rev * 0.65), 1000)
    dist, admin = step(r, 20000, int(rev * 0.1), 1000), step(r, 30000, int(rev * 0.12), 1000)
    pfo = rev - cos - dist - admin
    deb = step(r, 50000, 300000, 10000)
    rate = r.choice([5, 6, 8])
    fc = deb * rate // 100
    tax = step(r, 5000, max(6000, int((pfo - fc) * 0.3)), 500) if pfo - fc > 10000 else 0
    pfy = pfo - fc - tax
    sc, spm, gr, re0 = step(r, 200000, 800000, 50000), step(r, 0, 150000, 10000), step(r, 0, 100000, 10000), step(r, 20000, 200000, 1000)
    div = step(r, 5000, max(6000, int(pfy * 0.6)), 1000) if pfy > 10000 else 0
    re1 = re0 + pfy - div
    eq = sc + spm + gr + re1
    setup = (f'Extracts from the records of {c} for the year ended {ye(r)}: revenue {m(rev)}; cost of sales {m(cos)}; distribution costs {m(dist)}; administrative expenses {m(admin)}; {rate}% debentures {m(deb)} (interest for the full year is to be charged); '
             f'tax on profit for the year {m(tax)}. Equity at the start of the year: ordinary share capital {m(sc)}' + (f', share premium {m(spm)}' if spm else '') + (f', general reserve {m(gr)}' if gr else '') + f', retained earnings {m(re0)}. Dividends paid during the year were {m(div)}.')
    parts = [('Calculate the profit from operations.', m(pfo), f'{m(rev)} − {m(cos)} − {m(dist)} − {m(admin)} = {m(pfo)} [2]'),
             ('Calculate the profit for the year.', m(pfy), f'{m(pfo)} − finance costs {m(fc)} − tax {m(tax)} = {m(pfy)} [2]'),
             ('Calculate total equity at the end of the year.', m(eq), f'Retained earnings {m(re0)} + {m(pfy)} − {m(div)} = {m(re1)} [1]; equity {m(sc)} + {m(spm)} + {m(gr)} + {m(re1)} = {m(eq)} [1] [2]')]
    wrong = pfo - fc - tax - div
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('What is the profit for the year?', *num_opts(m, pfy, [wrong, pfo - tax, pfo]), f'{m(pfo)} − {m(fc)} − {m(tax)}'),
            'err': (f'calculated profit for the year as {m(wrong)}', 'dividends were deducted in the income statement; they are appropriations shown in the statement of changes in equity', m(pfy), f'{m(pfo)} − {m(fc)} − {m(tax)}', 'profit for the year') if div else None}


t18_4 = A(18, 'Statement of changes in equity and dividends', ['statement of changes in equity and dividends', 'statement of changes in equity', 'dividends'],
          mcqs=[('Which item appears in the statement of changes in equity?', 'Dividends paid', ['Debenture interest', 'Tax paid', 'Directors\' fees'], 'Movements in equity'),
                ('A transfer to the general reserve', 'reduces retained earnings and increases the general reserve, leaving total equity unchanged', ['increases total equity', 'reduces total equity', 'is an expense'], 'Movement between reserves'),
                ('Retained earnings at start $80,000; profit $45,000; dividends paid $20,000; transfer to general reserve $10,000. Closing retained earnings are', '$95,000', ['$105,000', '$125,000', '$85,000'], '80,000 + 45,000 − 20,000 − 10,000'),
                ('Proposed final dividends at the year end are', 'disclosed in a note, not recorded as a liability (IAS 10)', ['shown as a current liability', 'deducted from profit', 'added to retained earnings'], 'Not yet approved'),
                ('An issue of shares at a premium increases', 'share capital and share premium in the statement of changes in equity', ['retained earnings', 'the general reserve', 'profit for the year'], 'Capital receipts')],
          exps=[('Explain the purpose of the statement of changes in equity.', 'It shows how each component of equity (share capital, premium, reserves, retained earnings) changed during the year: profit, dividends, share issues and transfers.', 'Reconciles opening to closing equity [1]; examples of movements [1] [2]'),
                ('Explain why directors may transfer profits to a general reserve.', 'To show that profits are retained for future use (e.g. expansion or replacement) and to restrict the amount seen as available for dividends.', 'Retain for future use [1]; signal/restrict dividends [1] [2]')],
          disc=[('Evaluate the dividend policy of {co}.', 'Compare dividends with profit for the year: a high payout pleases shareholders but leaves less for growth; a low payout may disappoint investors but strengthens the company.', 'Payout vs profit [1]; shareholders vs growth [1]; judgement [1] [3]')])


@spec(t18_4)
def t184_soce(r, D):
    c = co(r)
    re0 = step(r, 30000, 300000, 1000)
    pfy = step(r, 20000, 150000, 1000)
    div = step(r, 5000, int(pfy * 0.7), 1000)
    tr = step(r, 5000, 40000, 5000) if D >= 2 else 0
    gr0 = step(r, 10000, 100000, 5000)
    iss = step(r, 50000, 200000, 10000) if D >= 3 else 0
    prem = iss // 2 if iss else 0
    sc0 = step(r, 200000, 600000, 50000)
    re1 = re0 + pfy - div - tr
    tot0, tot1 = sc0 + gr0 + re0, sc0 + iss + prem + gr0 + tr + re1
    setup = (f'At the start of the year {c} had ordinary share capital {m(sc0)}, general reserve {m(gr0)} and retained earnings {m(re0)}. During the year: profit for the year {m(pfy)}; dividends paid {m(div)}' +
             (f'; transfer to general reserve {m(tr)}' if tr else '') + (f'; an issue of shares raised {m(iss + prem)}, of which {m(prem)} was share premium' if iss else '') + '.')
    parts = [('Calculate the retained earnings at the end of the year.', m(re1), f'{m(re0)} + {m(pfy)} − {m(div)}' + (f' − {m(tr)}' if tr else '') + f' = {m(re1)} [2]'),
             ('Calculate total equity at the end of the year.', m(tot1), f'{m(sc0 + iss)} + premium {m(prem)} + reserve {m(gr0 + tr)} + RE {m(re1)} = {m(tot1)} [2]')]
    if tr:
        parts.append(('Explain why the transfer to the general reserve does not change total equity.', 'It moves profit from retained earnings to another reserve; both are part of equity.', 'Movement within equity [1]'))
    wrong = re0 + pfy - div + tr if tr else re0 + pfy + div
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('What are the retained earnings at the end of the year?', *num_opts(m, re1, [wrong, re0 + pfy, re0 + pfy - div]), f'{m(re0)} + {m(pfy)} − {m(div)} − {m(tr)}'),
            'err': (f'calculated closing retained earnings as {m(wrong)}', 'the transfer to the general reserve was added; it is deducted from retained earnings' if tr else 'dividends were added instead of deducted', m(re1), f'{m(re0)} + {m(pfy)} − {m(div)} − {m(tr)}', 'retained earnings')}


CHAPTERS[18] = [t18_1, t18_2, t18_3, t18_4]


# ===================================================================== 19 Share issues and capital reserves
t19_1 = A(19, 'Issue of shares at par and at a premium', ['issue of shares at par and at a premium', 'issue of shares', 'share premium'],
          mcqs=[('100,000 ordinary shares of $1 are issued at $1.60. The share premium is', '$60,000', ['$160,000', '$100,000', '$1,600'], '100,000 × $0.60'),
                ('Shares issued at par are issued at', 'their nominal value', ['a price above nominal value', 'market value', 'a discount'], 'Par = nominal'),
                ('The share premium account is', 'a capital reserve', ['a revenue reserve', 'a current liability', 'income of the year'], 'Not distributable as cash dividends'),
                ('On an issue at a premium, the bank account is debited with', 'the full issue price', ['the nominal value only', 'the premium only', 'nothing'], 'Cash received'),
                ('Why can an established company issue shares at a premium?', 'Its shares are worth more than their nominal value because of past profits and reputation', ['Because the law requires it', 'To reduce share capital', 'Because debentures are cheaper'], 'Market value > nominal')],
          exps=[('Explain why share premium cannot be used to pay cash dividends.', 'It is a capital reserve created from capital contributed by shareholders; company law protects it to maintain capital for creditors.', 'Capital reserve [1]; creditor protection/not distributable [1] [2]'),
                ('State the double entry for an issue of shares at a premium, received in full by bank transfer.', 'Dr Bank (issue price × number); Cr Ordinary share capital (nominal value); Cr Share premium (excess over nominal).', 'Dr bank [1]; Cr share capital and share premium [1] [2]')],
          disc=[('Discuss whether {co} should issue shares or take a bank loan to finance its expansion.', 'Shares: no interest or repayment, but dilute control and dividends expected; loan: interest is tax-deductible and control kept, but raises gearing and risk.', 'Shares point [1]; loan point [1]; judgement [1] [3]')])


@spec(t19_1)
def t191_issue(r, D):
    c = co(r)
    n = step(r, 50000, 500000, 10000)
    nm_ = r.choice(NOMS)
    pr = nm_ + (step(r, 10, 150, 5) / 100 if D >= 2 else 0)
    cash = n * pr
    sc, prem = n * nm_, n * (pr - nm_)
    setup = f'{c} issued {n:,} ordinary shares of {nom(nm_)} each at {m2(pr)} per share. All the money was received by bank transfer.'
    parts = [('Calculate the amounts credited to the share capital and share premium accounts.', f'Share capital {m(sc)}; share premium {m(prem)}', f'{n:,} × {nom(nm_)} = {m(sc)} [1]; {n:,} × {m2(pr - nm_)} = {m(prem)} [1] [2]'),
             ('Prepare the journal entry for the issue.', f'Dr Bank {m(cash)}; Cr Ordinary share capital {m(sc)}; Cr Share premium {m(prem)}', f'Dr bank {m(cash)} [1]; Cr share capital and premium [1] [2]'),
             ('Explain the effect of the issue on the statement of financial position.', f'Bank (current assets) increases by {m(cash)}; equity increases by the same amount.', 'Assets up [1]; equity up [1] [2]')]
    wrong = n * pr
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('What amount is credited to the ordinary share capital account?', *num_opts(m, sc, [cash, prem, sc * 2]), f'{n:,} × {nom(nm_)}'),
            'err': (f'credited the full {m(wrong)} to the ordinary share capital account', 'share capital is recorded at nominal value only; the excess over nominal value is credited to share premium', f'share capital {m(sc)}, share premium {m(prem)}', f'{n:,} × {nom(nm_)}', 'entries') if prem else None}


t19_2 = A(19, 'Rights issues and bonus issues', ['rights issues and bonus issues', 'rights issue', 'bonus issue'],
          mcqs=[('A bonus issue', 'gives existing shareholders free shares, financed from reserves', ['raises new cash for the company', 'is offered to the public at a premium', 'repays debentures'], 'Capitalisation of reserves'),
                ('A rights issue', 'offers new shares to existing shareholders, usually below market price, for cash', ['gives free shares', 'is offered only to new investors', 'reduces share capital'], 'Raises cash'),
                ('A company with 400,000 shares makes a 1 for 4 bonus issue. The number of shares after the issue is', '500,000', ['1,600,000', '400,000', '100,000'], '400,000 + 100,000'),
                ('A bonus issue changes total equity by', 'nothing – it moves reserves into share capital', ['the value of the new shares', 'the cash received', 'the dividend paid'], 'No cash involved'),
                ('Which reserve is most often used to fund a bonus issue?', 'Share premium', ['Trade payables', 'Debentures', 'Provision for depreciation'], 'Capital reserves first')],
          exps=[('Distinguish between a rights issue and a bonus issue.', 'A rights issue raises new cash by selling shares to existing shareholders in proportion to their holdings; a bonus issue gives free shares by converting reserves into share capital, raising no cash.', 'Rights – cash raised [1]; bonus – free, from reserves [1] [2]'),
                ('Explain why a company might make a bonus issue.', 'To bring the share capital more in line with the assets employed, to reduce the market price per share and make shares more marketable, or as a reward without paying cash.', 'Any valid reason with explanation [2]')],
          disc=[lambda r, s: (f"Advise a shareholder in {s['ctx']['co']} whether to take up the rights offer.", 'Taking up keeps their percentage holding and buys at a discount, but needs cash; selling the rights gives cash but dilutes their holding.', 'Take up – keep control/discount [1]; not – cash/dilution [1]; advice [1] [3]') if 'rights issue' in s['setup'] else
                (f"Discuss whether a bonus issue makes the shareholders of {s['ctx']['co']} better off.", 'Each shareholder has more shares but the same percentage holding and total equity is unchanged, so the share price should fall proportionately; it may signal confidence and improve marketability.', 'No change in value/percentage [1]; price adjusts/signal or marketability [1]; judgement [1] [3]')])


@spec(t19_2)
def t192_rb(r, D):
    c = co(r)
    nm_ = r.choice(NOMS)
    ns = step(r, 200000, 1000000, 40000)
    k = r.choice([2, 4, 5, 8, 10])
    new = ns // k
    bonus = r.random() < 0.5
    spm = step(r, 10000, 200000, 5000)
    re0 = step(r, 50000, 300000, 5000)
    if bonus:
        val = new * nm_
        from_prem = min(spm, val)
        from_re = val - from_prem
        setup = f'{c} has {ns:,} ordinary shares of {nom(nm_)} each, share premium of {m(spm)} and retained earnings of {m(re0)}. It makes a bonus issue of 1 share for every {k} held, using the share premium account as far as possible.'
        parts = [('Calculate the number of shares in issue after the bonus issue.', f'{ns + new:,}', f'{ns:,} ÷ {k} = {new:,} new [1]; total {ns + new:,} [1] [2]'),
                 ('Calculate the balances on share premium and retained earnings after the issue.', f'Share premium {m(spm - from_prem)}; retained earnings {m(re0 - from_re)}', f'Bonus value {new:,} × {nom(nm_)} = {m(val)} [1]; from premium {m(from_prem)}, retained earnings {m(from_re)} [1] [2]'),
                 ('Explain the effect of the bonus issue on total equity and on the bank balance.', 'No change to either – reserves are converted into share capital and no cash is received.', 'Equity unchanged [1]; no cash [1] [2]')]
        return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
                'mcq': ('How many shares are in issue after the bonus issue?', *num_opts(lambda x: f'{int(x):,}', ns + new, [ns * k, new, ns + ns // (k + 1)]), f'{ns:,} + {new:,}'),
                'err': (f'recorded the bonus issue as increasing the bank balance by {m(val)}', 'a bonus issue raises no cash; it is a transfer from reserves to share capital', 'no change to bank; Dr reserves, Cr share capital ' + m(val), f'{new:,} × {nom(nm_)}', 'treatment')}
    pr = nm_ + step(r, 5, 80, 5) / 100
    cash = new * pr
    setup = f'{c} has {ns:,} ordinary shares of {nom(nm_)} each, with a market price of {m2(pr + step(r, 10, 60, 5) / 100)}. It makes a rights issue of 1 share for every {k} held at {m2(pr)} per share; all rights are taken up.'
    parts = [('Calculate the cash raised by the rights issue.', m(cash), f'{ns:,} ÷ {k} = {new:,} shares [1]; × {m2(pr)} = {m(cash)} [1] [2]'),
             ('Calculate the increases in share capital and share premium.', f'Share capital {m(new * nm_)}; share premium {m(new * (pr - nm_))}', f'{new:,} × {nom(nm_)} = {m(new * nm_)} [1]; premium {m(new * (pr - nm_))} [1] [2]'),
             ('Explain one reason why the rights price is set below the market price.', 'To encourage existing shareholders to take up the shares so that the issue is fully subscribed.', 'Encourage take-up [1]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('How much cash is raised by the rights issue?', *num_opts(m, cash, [ns * pr, new * nm_, cash * k]), f'{new:,} × {m2(pr)}'),
            'err': (f'calculated the cash raised as {m(new * nm_)}', 'the nominal value was used; cash raised is the number of new shares × the rights price', m(cash), f'{new:,} × {m2(pr)}', 'cash raised')}


t19_3 = A(19, 'Capital and revenue reserves; uses of share premium', ['capital and revenue reserves; uses of share premium', 'capital reserves', 'revenue reserves', 'uses of share premium'],
          mcqs=[('Which is a revenue reserve?', 'Retained earnings', ['Share premium', 'Revaluation reserve', 'Capital redemption reserve'], 'Created from profits, distributable'),
                ('A revaluation reserve is created when', 'non-current assets are revalued upwards', ['shares are issued at par', 'profits are retained', 'debentures are issued'], 'Unrealised gain'),
                ('Share premium may be used to', 'issue fully paid bonus shares', ['pay cash dividends', 'pay debenture interest', 'buy inventory'], 'Permitted uses'),
                ('Revenue reserves can be', 'used to pay dividends', ['never distributed', 'used only for bonus issues', 'shown as liabilities'], 'Distributable'),
                ('A general reserve is', 'a revenue reserve', ['a capital reserve', 'a liability', 'a non-current asset'], 'Transferred from retained earnings')],
          exps=[('Distinguish between capital reserves and revenue reserves.', 'Capital reserves arise from capital transactions (share premium, revaluation) and cannot be distributed as dividends; revenue reserves come from profits (retained earnings, general reserve) and can be distributed.', 'Capital – not distributable, examples [1]; revenue – from profits, distributable [1] [2]'),
                ('State two uses of the share premium account.', 'Issuing fully paid bonus shares; writing off share issue expenses (and preliminary expenses).', 'Two uses [1 each] [2]')],
          disc=[('Explain why creditors of {co} benefit from the rules restricting capital reserves.', 'Capital is kept in the company as a buffer; it cannot be paid out to shareholders, protecting lenders if the company fails.', 'Capital maintained [1]; creditor protection [1] [2]')])


@spec(t19_3)
def t193_res(r, D):
    c = co(r)
    items = [('share premium', 'capital', step(r, 10000, 150000, 5000)), ('revaluation reserve', 'capital', step(r, 10000, 200000, 5000)),
             ('general reserve', 'revenue', step(r, 10000, 100000, 5000)), ('retained earnings', 'revenue', step(r, 20000, 300000, 1000))]
    k = 3 if D <= 2 else 4
    its = r.sample(items, k)
    capr = sum(v for _, t, v in its if t == 'capital')
    revr = sum(v for _, t, v in its if t == 'revenue')
    sc = step(r, 100000, 800000, 50000)
    setup = f'The equity of {c} at the year end consisted of ordinary share capital {m(sc)} and the following reserves: ' + ', '.join(f'{n} {m(v)}' for n, _, v in its) + '.'
    parts = [('Classify each reserve as a capital reserve or a revenue reserve and calculate the total of each.', f'Capital {m(capr)}; revenue {m(revr)}', '; '.join(f'{n}: {t}' for n, t, _ in its) + f' [{k - 1}]; totals [1] [{k}]'),
             ('State the maximum amount available for the payment of dividends.', m(revr), f'Revenue reserves {m(revr)} [1]'),
             ('Calculate total equity.', m(sc + capr + revr), f'{m(sc)} + {m(capr)} + {m(revr)} = {m(sc + capr + revr)} [1]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'co': c},
            'mcq': ('What is the maximum amount available for dividends?', *num_opts(m, revr, [capr + revr, capr, revr + sc]), 'Only revenue reserves are distributable'),
            'err': (f'stated that {m(capr + revr)} was available for dividends', 'capital reserves (share premium, revaluation reserve) cannot be distributed as dividends', m(revr), ' + '.join(m(v) for _, t, v in its if t == 'revenue'), 'amount available') if capr else None}


CHAPTERS[19] = [t19_1, t19_2, t19_3]


# ===================================================================== 20-22 Ratio analysis
def _fin(r):
    d = {}
    d['rev'] = step(r, 200000, 900000, 1000)
    d['cos'] = step(r, int(d['rev'] * 0.5), int(d['rev'] * 0.72), 1000)
    d['gp'] = d['rev'] - d['cos']
    d['exp'] = step(r, int(d['gp'] * 0.4), int(d['gp'] * 0.8), 1000)
    d['pfo'] = d['gp'] - d['exp']
    d['oi'], d['ci'] = step(r, d['cos'] * 20 // 365, d['cos'] * 90 // 365, 1000), step(r, d['cos'] * 20 // 365, d['cos'] * 90 // 365, 1000)
    d['tr'] = step(r, d['rev'] * 20 // 365, d['rev'] * 75 // 365, 1000)
    d['bank'] = step(r, 2000, 40000, 1000)
    _ca = d['ci'] + d['tr'] + d['bank']
    _cl = max(10000, round(_ca / r.uniform(0.8, 2.8) / 1000) * 1000)
    d['cl'] = _cl
    d['tp'] = _cl - step(r, 1000, max(1000, min(20000, _cl // 3)), 1000)
    d['nca'] = step(r, 150000, 700000, 5000)
    d['ncl'] = step(r, 0, 300000, 10000)
    d['ca'] = d['ci'] + d['tr'] + d['bank']
    d['eq'] = d['nca'] + d['ca'] - d['cl'] - d['ncl']
    if d['eq'] < 50000:
        d['nca'] += 100000
        d['eq'] += 100000
    d['ce'] = d['eq'] + d['ncl']
    d['pur'] = d['cos'] + d['ci'] - d['oi']
    return d


t20_1 = A(20, 'Gross margin, profit margin and mark-up', ['gross margin, profit margin and mark-up', 'gross margin', 'profit margin', 'mark-up'],
          mcqs=[('Gross margin is calculated as', 'gross profit ÷ revenue × 100', ['gross profit ÷ cost of sales × 100', 'profit for the year ÷ revenue × 100', 'revenue ÷ gross profit × 100'], 'On selling price'),
                ('Revenue $200,000, gross profit $70,000. The mark-up is', '53.8%', ['35.0%', '65.0%', '28.6%'], '70,000 ÷ 130,000'),
                ('Which change would reduce the gross margin?', 'Suppliers increase their prices and selling prices stay the same', ['Selling prices rise with costs unchanged', 'Expenses fall', 'Rent increases'], 'Cost of sales up'),
                ('A fall in the profit margin with an unchanged gross margin suggests', 'expenses have risen relative to revenue', ['selling prices have fallen', 'purchase prices have risen', 'inventory has been stolen'], 'Gap between gross and net'),
                ('Profit margin is also called', 'the net profit margin (profit for the year / operating profit as a % of revenue)', ['the mark-up', 'the gross margin', 'the current ratio'], 'Definition')],
          exps=[('Explain two reasons why a business\'s gross margin might fall.', 'Selling prices cut to meet competition; purchase costs rose but could not be passed on; change in sales mix toward lower-margin goods; theft or wastage of inventory.', 'Two reasons [1 each] [2]'),
                ('Explain the difference between the gross margin and the profit margin.', 'Gross margin compares gross profit (after cost of sales) with revenue; profit margin compares profit after all expenses with revenue, showing control of overheads too.', 'Gross – after COS [1]; profit margin – after expenses [1] [2]')],
          disc=[('Evaluate the profitability of {f}.', 'Compare margins with the previous year and the industry; explain causes (pricing, costs, expenses); consider whether the trend is sustainable.', 'Use of ratios [1]; causes [1]; judgement [1] [3]')])


@spec(t20_1)
def t201_gm(r, D):
    f = firm(r)
    d = _fin(r)
    setup = f'{f} reports for the year: revenue {m(d["rev"])}; cost of sales {m(d["cos"])}; ' + ('expenses ' + m(d['exp']) + '.' if D >= 2 else '.')
    gm, mu, pm = d['gp'] / d['rev'] * 100, d['gp'] / d['cos'] * 100, d['pfo'] / d['rev'] * 100
    parts = [('Calculate the gross margin.', pc(gm), f'GP {m(d["gp"])} ÷ {m(d["rev"])} × 100 = {pc(gm)} [2]'),
             ('Calculate the mark-up.', pc(mu), f'{m(d["gp"])} ÷ {m(d["cos"])} × 100 = {pc(mu)} [1]')]
    if D >= 2:
        parts.append(('Calculate the profit margin.', pc(pm), f'({m(d["gp"])} − {m(d["exp"])}) ÷ {m(d["rev"])} × 100 = {pc(pm)} [2]'))
    if D >= 4:
        ly = gm + r.choice([-6, -4, 3, 5])
        parts.append((f'Last year the gross margin was {pc(ly)}. Suggest two reasons for the change.', ('Higher selling prices; cheaper suppliers/bulk discounts; better sales mix' if gm > ly else 'Price cuts to meet competition; higher purchase costs not passed on; theft or wastage of inventory') + '.', 'Two reasons consistent with direction [1 each] [2]'))
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the gross margin?', *num_opts(pc, gm, [mu, pm, d['cos'] / d['rev'] * 100]), f'{m(d["gp"])} ÷ {m(d["rev"])} × 100'),
            'err': (f'calculated the gross margin as {pc(mu)}', 'gross profit was divided by cost of sales (that gives the mark-up); margin uses revenue', pc(gm), f'{m(d["gp"])} ÷ {m(d["rev"])} × 100', 'gross margin')}


t20_2 = A(20, 'Return on capital employed (ROCE)', ['return on capital employed (roce)', 'return on capital employed', 'roce'],
          mcqs=[('ROCE is calculated as', 'profit from operations ÷ capital employed × 100', ['profit for the year ÷ revenue × 100', 'revenue ÷ capital employed', 'gross profit ÷ equity × 100'], 'Profit before interest and tax'),
                ('Capital employed is', 'equity plus non-current liabilities', ['current assets minus current liabilities', 'total assets', 'share capital only'], 'Long-term funds'),
                ('Profit from operations $60,000; equity $300,000; non-current liabilities $100,000. ROCE is', '15.0%', ['20.0%', '12.0%', '25.0%'], '60,000 ÷ 400,000'),
                ('A rising ROCE indicates', 'more profit is being generated from the capital invested', ['liquidity has improved', 'gearing has fallen', 'the business is smaller'], 'Efficiency of capital use'),
                ('ROCE should be compared with', 'the return available from alternative investments, e.g. bank deposit rates', ['the current ratio', 'the number of employees', 'the gearing of other firms only'], 'Opportunity cost')],
          exps=[('Explain why ROCE is regarded as a key measure of performance.', 'It relates the profit made to all the long-term capital used to make it, so businesses of different sizes can be compared and the return compared with alternatives.', 'Profit relative to capital [1]; comparability/alternative returns [1] [2]'),
                ('Explain one limitation of ROCE.', 'Capital employed is based on book values (historical cost, depreciation), so older assets give a higher ROCE; year-end figures may not be representative.', 'Limitation [1]; explanation [1] [2]')],
          disc=[('Advise the owners of {f} whether the business is a good use of their capital.', 'Compare ROCE with the bank deposit rate and competitors; consider risk and non-financial factors.', 'Comparison with alternatives [1]; risk [1]; advice [1] [3]')])


@spec(t20_2)
def t202_roce(r, D):
    f = firm(r)
    d = _fin(r)
    roce = d['pfo'] / d['ce'] * 100
    setup = f'{f}: revenue {m(d["rev"])}; profit from operations {m(d["pfo"])}; equity {m(d["eq"])}' + (f'; non-current liabilities (loan) {m(d["ncl"])}' if d['ncl'] else '') + '.'
    parts = [('Calculate capital employed and the return on capital employed.', f'Capital employed {m(d["ce"])}; ROCE {pc(roce)}', f'CE {m(d["eq"])} + {m(d["ncl"])} = {m(d["ce"])} [1]; {m(d["pfo"])} ÷ {m(d["ce"])} × 100 = {pc(roce)} [1] [2]')]
    if D >= 3:
        bank = r.choice([3, 4, 5, 6])
        parts.append((f'The owners could earn {bank}% by placing their capital on deposit. Comment on the ROCE.', f'ROCE {pc(roce)} is {"above" if roce > bank else "below"} the {bank}% risk-free return; ' + ('the extra return rewards the risk of running the business.' if roce > bank else 'the business is not earning enough to justify the risk.'), 'Comparison [1]; risk point [1] [2]'))
    if D >= 2:
        parts.append(('Calculate the asset turnover (revenue ÷ capital employed).', f'{d["rev"] / d["ce"]:.2f} times', f'{m(d["rev"])} ÷ {m(d["ce"])} = {d["rev"] / d["ce"]:.2f} [1]'))
    wrong = d['pfo'] / d['eq'] * 100
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the ROCE?', *num_opts(pc, roce, [wrong, d['pfo'] / d['rev'] * 100, roce * 1.5]), f'{m(d["pfo"])} ÷ {m(d["ce"])} × 100'),
            'err': (f'calculated ROCE as {pc(wrong)}', 'non-current liabilities were left out of capital employed', pc(roce), f'{m(d["pfo"])} ÷ ({m(d["eq"])} + {m(d["ncl"])}) × 100', 'ROCE') if d['ncl'] else None}


EXPN = ['wages and salaries', 'rent', 'advertising', 'delivery costs', 'administration']

t20_3 = A(20, 'Expenses to revenue and other profitability ratios', ['expenses to revenue and other profitability ratios', 'expenses to revenue', 'profitability ratios'],
          mcqs=[('An expense-to-revenue ratio shows', 'each expense as a percentage of revenue', ['each expense as a percentage of profit', 'revenue per employee', 'the gross margin'], 'Cost control'),
                ('Revenue $400,000; wages $60,000. Wages to revenue is', '15.0%', ['6.7%', '66.7%', '1.5%'], '60,000 ÷ 400,000'),
                ('If wages rise from 12% to 15% of revenue, profit margin will', 'fall by 3 percentage points if other ratios are unchanged', ['rise by 3 percentage points', 'not change', 'fall by 15 percentage points'], 'Expense up relative to revenue'),
                ('Gross margin 40%, expenses 28% of revenue. The profit margin is', '12%', ['68%', '40%', '28%'], '40 − 28'),
                ('Which is a profitability ratio?', 'Return on capital employed', ['Current ratio', 'Trade receivables turnover', 'Gearing'], 'Profitability ratios')],
          exps=[('Explain why expense-to-revenue ratios are more useful than the money amounts of expenses.', 'They allow comparison over time and with other firms of different sizes, showing whether costs are controlled relative to activity.', 'Comparison/size [1]; cost control [1] [2]'),
                ('Explain how gross margin, expenses to revenue and profit margin are linked.', 'Profit margin = gross margin − total expenses as a % of revenue, so any change in profit margin is explained by the other two.', 'Relationship [1]; use in analysis [1] [2]')],
          disc=[('Recommend how {f} could improve its profit margin.', 'Control the expense with the largest rise (e.g. renegotiate rent, improve staff productivity), or raise gross margin; consider effects on sales and quality.', 'Target specific expense [1]; method [1]; risk/judgement [1] [3]')])


@spec(t20_3)
def t203_exp(r, D):
    f = firm(r)
    rev = step(r, 200000, 800000, 1000)
    gm = r.choice([30, 35, 40, 45, 50])
    k = 3 if D <= 3 else 4
    names = r.sample(EXPN, k)
    ex = [step(r, int(rev * 0.02), int(rev * 0.09), 500) for _ in names]
    gp = rev * gm // 100
    pfo = gp - sum(ex)
    setup = f'{f} had revenue of {m(rev)} and a gross margin of {gm}%. Its expenses were: ' + ', '.join(f'{n} {m(v)}' for n, v in zip(names, ex)) + '.'
    pcts = [v / rev * 100 for v in ex]
    parts = [('Calculate each expense as a percentage of revenue.', '; '.join(f'{n} {pc(p_)}' for n, p_ in zip(names, pcts)), '; '.join(f'{n} {m(v)} ÷ {m(rev)} = {pc(p_)}' for n, v, p_ in zip(names, ex, pcts)) + f' [{k}]'),
             ('Calculate the profit margin.', pc(pfo / rev * 100), f'{gm}% − {pc(sum(pcts))} = {pc(pfo / rev * 100)} [2]')]
    if D >= 3:
        parts.append(('Identify which expense the business should investigate first and explain why.', f'{cap1(names[pcts.index(max(pcts))])} – it is the largest proportion of revenue, so a small saving has the biggest effect on profit.', 'Largest expense identified [1]; reason [1] [2]'))
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is {names[0]} as a percentage of revenue?', *num_opts(pc, pcts[0], [ex[0] / gp * 100, ex[0] / max(pfo, 1) * 100 if pfo > 0 else pcts[0] * 3, pcts[0] * 10]), f'{m(ex[0])} ÷ {m(rev)} × 100'),
            'err': (f'calculated {names[0]} as {pc(ex[0] / gp * 100)} of revenue', 'the expense was divided by gross profit instead of revenue', pc(pcts[0]), f'{m(ex[0])} ÷ {m(rev)} × 100', 'percentage')}


CHAPTERS[20] = [t20_1, t20_2, t20_3]


t21_1 = A(21, 'Current ratio and liquid (acid test) ratio', ['current ratio and liquid (acid test) ratio', 'current ratio', 'acid test', 'liquid ratio'],
          mcqs=[('The liquid (acid test) ratio excludes', 'inventory', ['trade receivables', 'bank', 'trade payables'], 'Inventory is least liquid'),
                ('Current assets $90,000 including inventory $40,000; current liabilities $50,000. The acid test ratio is', '1.00:1', ['1.80:1', '0.80:1', '0.44:1'], '(90,000 − 40,000) ÷ 50,000'),
                ('A current ratio well above the norm may indicate', 'too much money tied up in inventory or receivables', ['a high risk of insolvency', 'too little inventory', 'a high gearing'], 'Inefficient use of resources'),
                ('Paying a trade payable from the bank when the current ratio is 2:1 will', 'increase the current ratio', ['reduce the current ratio', 'leave it unchanged', 'reduce working capital'], 'Equal reduction from a larger base'),
                ('An acid test ratio below 1:1 suggests that', 'the business may not be able to pay current liabilities without selling inventory', ['the business has excess cash', 'profit is too low', 'inventory turnover is fast'], 'Liquidity warning')],
          exps=[('Explain why the acid test ratio is a stricter test of liquidity than the current ratio.', 'Inventory is excluded because it may take time to sell and may not realise its book value; the ratio shows ability to pay immediate debts.', 'Excludes inventory [1]; reason – not quickly converted [1] [2]'),
                ('Explain why a supermarket can operate with a low current ratio.', 'It sells for cash so has few receivables, inventory turns over quickly, and it receives credit from suppliers.', 'Cash sales/fast inventory [1]; supplier credit [1] [2]')],
          disc=[('Evaluate the liquidity position of {f} and suggest how it could be improved.', 'Compare ratios with norms/industry; if low: inject capital, long-term loan, sell surplus assets, reduce inventory; if high: invest idle funds.', 'Interpret ratios [1]; suitable action [1]; judgement [1] [3]')])


@spec(t21_1)
def t211_liq(r, D):
    f = firm(r)
    d = _fin(r)
    cr_ = d['ca'] / d['cl']
    qr = (d['ca'] - d['ci']) / d['cl']
    setup = f'At the year end {f} had: inventory {m(d["ci"])}; trade receivables {m(d["tr"])}; bank {m(d["bank"])}; trade payables {m(d["tp"])}; other current liabilities {m(d["cl"] - d["tp"])}.'
    parts = [('Calculate the current ratio.', ratio_s(cr_), f'{m(d["ca"])} ÷ {m(d["cl"])} = {ratio_s(cr_)} [2]'),
             ('Calculate the liquid (acid test) ratio.', ratio_s(qr), f'({m(d["ca"])} − {m(d["ci"])}) ÷ {m(d["cl"])} = {ratio_s(qr)} [2]'),
             ('Comment on the liquidity of the business.', ('Liquid ratio below 1:1 – relies on selling inventory to pay debts' if qr < 1 else 'Liquid ratio at or above 1:1 – can meet current liabilities without selling inventory') + (f'; current ratio {ratio_s(cr_)} is ' + ('low' if cr_ < 1.5 else 'satisfactory' if cr_ <= 2.5 else 'high – possible idle resources')) + '.', 'Interpretation of acid test [1]; of current ratio [1] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the liquid (acid test) ratio?', *num_opts(ratio_s, qr, [cr_, d['ci'] / d['cl'], d['cl'] / (d['ca'] - d['ci'])]), f'({m(d["ca"])} − {m(d["ci"])}) ÷ {m(d["cl"])}'),
            'err': (f'calculated the acid test ratio as {ratio_s(cr_)}', 'inventory was not excluded from current assets', ratio_s(qr), f'({m(d["ca"])} − {m(d["ci"])}) ÷ {m(d["cl"])}', 'acid test ratio')}


t21_2 = A(21, 'Trade receivables and trade payables turnover in days', ['trade receivables and trade payables turnover in days', 'trade receivables turnover', 'trade payables turnover', 'collection period'],
          mcqs=[('Trade receivables turnover (days) is', 'trade receivables ÷ credit sales × 365', ['credit sales ÷ trade receivables × 365', 'trade receivables ÷ cost of sales × 365', 'trade payables ÷ credit purchases × 365'], 'Average collection period'),
                ('Trade receivables $30,000; credit sales $365,000. The collection period is', '30 days', ['12 days', '45 days', '73 days'], '30,000 ÷ 365,000 × 365'),
                ('If customers are allowed 30 days\' credit and the collection period is 52 days,', 'credit control needs to improve', ['credit control is excellent', 'payables days are too long', 'inventory is too high'], 'Customers pay late'),
                ('A long trade payables period may', 'help cash flow but damage relations with suppliers', ['always reduce costs', 'improve the acid test ratio directly', 'mean that receivables are paying faster'], 'Trade-off'),
                ('Trade payables turnover uses', 'credit purchases', ['revenue', 'cost of sales always', 'credit sales'], 'Relates payables to purchases')],
          exps=[('Explain why a business would like its trade receivables days to be lower than its trade payables days.', 'It collects cash from customers before it has to pay suppliers, so suppliers effectively finance its working capital and liquidity improves.', 'Collect before paying [1]; liquidity/financing [1] [2]'),
                ('State two ways a business could reduce its trade receivables days.', 'Offer cash discounts for prompt payment; credit checks and limits; chase overdue accounts; use factoring; invoice promptly.', 'Two ways [1 each] [2]')],
          disc=[('Discuss whether {f} should take longer to pay its suppliers.', 'It improves cash flow, but risks losing cash discounts, supplier goodwill and credit; it may breach agreed terms.', 'Cash benefit [1]; risks [1]; judgement [1] [3]')])


@spec(t21_2)
def t212_days(r, D):
    f = firm(r)
    d = _fin(r)
    cs_pct = r.choice([60, 75, 80, 100])
    cs = d['rev'] * cs_pct // 100
    rd = d['tr'] / cs * 365
    pdays = d['tp'] / d['pur'] * 365
    setup = f'{f} had revenue of {m(d["rev"])}' + (f', of which {cs_pct}% was on credit' if cs_pct < 100 else ', all on credit') + f', and credit purchases of {m(d["pur"])}. At the year end trade receivables were {m(d["tr"])} and trade payables were {m(d["tp"])}. The business allows customers 30 days\' credit.'
    parts = [('Calculate the trade receivables turnover in days.', days(rd), f'{m(d["tr"])} ÷ {m(cs)} × 365 = {days(rd)} [2]'),
             ('Calculate the trade payables turnover in days.', days(pdays), f'{m(d["tp"])} ÷ {m(d["pur"])} × 365 = {days(pdays)} [2]'),
             ('Comment on the results.', ('Customers take longer than the 30 days allowed – credit control should improve' if rd > 30 else 'Customers pay within the 30 days allowed') + ('; the business pays suppliers more slowly than it collects from customers, which helps cash flow.' if pdays > rd else '; it pays suppliers faster than it collects, which puts pressure on cash.'),
              'Receivables vs terms [1]; comparison with payables days [1] [2]')]
    wrong = d['tr'] / d['rev'] * 365
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the trade receivables turnover in days?', *num_opts(days, rd, [wrong if cs_pct < 100 else rd * 1.3, d['tr'] / d['cos'] * 365, pdays]), f'{m(d["tr"])} ÷ {m(cs)} × 365'),
            'err': (f'calculated trade receivables days as {days(wrong)}', 'total revenue was used; only credit sales create receivables', days(rd), f'{m(d["tr"])} ÷ {m(cs)} × 365', 'trade receivables days') if cs_pct < 100 else
            (f'calculated trade receivables days as {days(cs / d["tr"] * 365 / 365)}', 'the ratio was inverted, giving a number of times rather than days', days(rd), f'{m(d["tr"])} ÷ {m(cs)} × 365', 'trade receivables days')}


t21_3 = A(21, 'Inventory turnover and non-current asset turnover', ['inventory turnover and non-current asset turnover', 'inventory turnover', 'non-current asset turnover'],
          mcqs=[('Inventory turnover (times) is', 'cost of sales ÷ average inventory', ['revenue ÷ closing inventory', 'average inventory ÷ cost of sales', 'gross profit ÷ inventory'], 'Rate of turnover'),
                ('Opening inventory $20,000, closing $30,000, cost of sales $200,000. Inventory turnover is', '8 times', ['10 times', '6.7 times', '4 times'], 'Average 25,000'),
                ('A fall in inventory turnover may indicate', 'slow-moving or obsolete inventory', ['improved efficiency', 'higher gross margin', 'better credit control'], 'Goods take longer to sell'),
                ('Non-current asset turnover is', 'revenue ÷ net book value of non-current assets', ['non-current assets ÷ revenue', 'profit ÷ non-current assets', 'cost of sales ÷ non-current assets'], 'Use of NCA to generate revenue'),
                ('Which business would expect the highest inventory turnover?', 'A bakery', ['A jeweller', 'A furniture store', 'A car dealer'], 'Perishable goods')],
          exps=[('Explain why inventory turnover is important to a retailer.', 'Faster turnover means less money tied up in inventory, lower storage costs and less risk of obsolescence, and profit is earned more often.', 'Less capital tied up/costs [1]; profit earned more frequently [1] [2]'),
                ('Explain why non-current asset turnover may fall after a business buys new premises.', 'Non-current assets increase immediately, but revenue from the extra capacity may take time to grow.', 'NCA rise [1]; revenue lag [1] [2]')],
          disc=[('Evaluate how {f} could improve its inventory turnover.', 'Reduce order sizes/just-in-time, clear slow-moving lines, better forecasting; but risk of stock-outs and lost bulk discounts.', 'Methods [1]; risks [1]; judgement [1] [3]')])


@spec(t21_3)
def t213_inv(r, D):
    f = firm(r)
    d = _fin(r)
    avg = (d['oi'] + d['ci']) / 2
    it = d['cos'] / avg
    idays = avg / d['cos'] * 365
    nt = d['rev'] / d['nca']
    setup = f'{f}: revenue {m(d["rev"])}; cost of sales {m(d["cos"])}; inventory {m(d["oi"])} at the start and {m(d["ci"])} at the end of the year; non-current assets (carrying amount) {m(d["nca"])}.'
    parts = [('Calculate the rate of inventory turnover in times and in days.', f'{it:.2f} times; {days(idays)}', f'Average inventory {m(avg)} [1]; {m(d["cos"])} ÷ {m(avg)} = {it:.2f} times [1]; {days(idays)} [1] [3]'),
             ('Calculate the non-current asset turnover.', f'{nt:.2f} times', f'{m(d["rev"])} ÷ {m(d["nca"])} = {nt:.2f} [1]')]
    if D >= 3:
        parts.append(('Explain one reason why the inventory turnover might have fallen compared with last year.', 'Higher inventory held (bulk buying, slow-moving lines) or lower sales volume.', 'Valid reason [1]; explanation [1] [2]'))
    wrong = d['cos'] / d['ci']
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the rate of inventory turnover?', *num_opts(lambda x: f'{x:.2f} times', it, [wrong, d['rev'] / avg, avg / d['cos'] * 10]), f'{m(d["cos"])} ÷ {m(avg)}'),
            'err': (f'calculated inventory turnover as {d["rev"] / avg:.2f} times', 'revenue was used; inventory is at cost, so cost of sales must be used', f'{it:.2f} times', f'{m(d["cos"])} ÷ {m(avg)}', 'inventory turnover')}


t21_4 = A(21, 'Gearing ratio at AS level', ['gearing ratio at as level', 'gearing ratio', 'gearing'],
          mcqs=[('The gearing ratio compares', 'long-term borrowing with total capital employed', ['current assets with current liabilities', 'profit with revenue', 'inventory with cost of sales'], 'Financial risk'),
                ('Non-current liabilities $150,000; equity $350,000. Gearing is', '30.0%', ['42.9%', '70.0%', '23.1%'], '150,000 ÷ 500,000'),
                ('A highly geared business', 'has a high proportion of capital from borrowing', ['has no loans', 'has high liquidity', 'has low interest costs'], 'Above about 50%'),
                ('Rising interest rates are most risky for a business that', 'is highly geared with variable-rate loans', ['has no borrowing', 'is low geared', 'has high inventory turnover'], 'Interest cost increases'),
                ('Issuing new ordinary shares to repay a loan will', 'reduce gearing', ['increase gearing', 'leave gearing unchanged', 'reduce equity'], 'Less debt, more equity')],
          exps=[('Explain why a lender is interested in a business\'s gearing ratio.', 'High gearing means heavy interest commitments and greater risk that interest and repayments cannot be met, so further lending is riskier.', 'Interest burden/risk [1]; lending decision [1] [2]'),
                ('Explain one advantage of high gearing for the owners when profits are rising.', 'Interest is fixed, so extra profit goes to the owners, increasing their return without diluting ownership.', 'Fixed interest [1]; higher return to owners [1] [2]')],
          disc=[('Discuss whether {f} should borrow further to finance expansion.', 'Consider current gearing, interest cover, stability of profits and interest-rate risk; alternatives are equity or retained profits.', 'Gearing level [1]; risk/interest [1]; judgement [1] [3]')])


@spec(t21_4)
def t214_gear(r, D):
    f = firm(r)
    eq = step(r, 100000, 600000, 5000)
    ncl = step(r, 20000, 500000, 5000)
    g = ncl / (eq + ncl) * 100
    setup = f'{f} has equity of {m(eq)} and a long-term bank loan of {m(ncl)}.'
    parts = [('Calculate the gearing ratio.', pc(g), f'{m(ncl)} ÷ ({m(eq)} + {m(ncl)}) × 100 = {pc(g)} [2]'),
             ('State whether the business is high or low geared and explain one implication.', f'{"Highly geared (over 50%)" if g > 50 else "Low geared (under 50%)"}: ' + ('large interest commitments increase risk and make further borrowing difficult.' if g > 50 else 'it should find it easier to borrow more and interest commitments are manageable.'), 'Classification [1]; implication [1] [2]')]
    if D >= 3:
        x = step(r, 20000, 150000, 5000)
        g2 = (ncl + x) / (eq + ncl + x) * 100
        parts.append((f'Calculate the gearing ratio if a further loan of {m(x)} is taken.', pc(g2), f'{m(ncl + x)} ÷ {m(eq + ncl + x)} × 100 = {pc(g2)} [2]'))
    wrong = ncl / eq * 100
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the gearing ratio?', *num_opts(pc, g, [wrong, eq / (eq + ncl) * 100, g * 0.5]), f'{m(ncl)} ÷ {m(eq + ncl)} × 100'),
            'err': (f'calculated gearing as {pc(wrong)}', 'the loan was divided by equity only; at AS level gearing = non-current liabilities ÷ (equity + non-current liabilities)', pc(g), f'{m(ncl)} ÷ {m(eq + ncl)} × 100', 'gearing ratio')}


CHAPTERS[21] = [t21_1, t21_2, t21_3, t21_4]


def _ratios(d):
    return {'gross margin': d['gp'] / d['rev'] * 100, 'profit margin': d['pfo'] / d['rev'] * 100, 'ROCE': d['pfo'] / d['ce'] * 100,
            'current ratio': d['ca'] / d['cl'], 'acid test ratio': (d['ca'] - d['ci']) / d['cl'], 'trade receivables days': d['tr'] / d['rev'] * 365}


def _rf(k, v):
    return pc(v) if k in ('gross margin', 'profit margin', 'ROCE') else (days(v) if 'days' in k else ratio_s(v))


t22_1 = A(22, 'Interpreting ratios and comparing with previous years or competitors', ['interpreting ratios and comparing with previous years or competitors', 'interpreting ratios', 'comparing with competitors'],
          mcqs=[('Ratios are most useful when', 'compared with previous years, competitors or industry averages', ['looked at in isolation', 'calculated once only', 'used without the financial statements'], 'Comparison gives meaning'),
                ('Business A has a higher gross margin but a lower profit margin than Business B. This suggests A has', 'higher expenses relative to revenue', ['lower selling prices', 'higher cost of sales', 'better cost control'], 'Gap between margins'),
                ('A fall in the current ratio from 2.1:1 to 1.4:1 shows that', 'liquidity has worsened', ['profitability has improved', 'gearing has fallen', 'inventory turnover has risen'], 'Liquidity ratio'),
                ('An increase in ROCE with an unchanged profit margin must be due to', 'more revenue generated from capital employed (higher asset turnover)', ['higher gearing only', 'a fall in revenue', 'a fall in cost of sales'], 'ROCE = margin × asset turnover'),
                ('Which ratio would a supplier be most interested in?', 'Acid test ratio', ['ROCE', 'Gross margin', 'Non-current asset turnover'], 'Ability to pay')],
          exps=[('Explain why comparing ratios with a competitor may be misleading.', 'The competitor may use different accounting policies (depreciation, inventory), have a different year end, size or business mix, so differences may not reflect performance.', 'Different policies/size/mix [1]; explanation [1] [2]'),
                ('Explain why a business can have a high profit margin but a low ROCE.', 'It may use a large amount of capital relative to its revenue (low asset turnover), so each dollar of capital earns little even if each sale is profitable.', 'Low asset turnover/large capital [1]; explanation [1] [2]')],
          disc=[('Using the ratios, recommend which business a bank should lend to.', 'Weigh profitability (ROCE, margins) against liquidity (current and acid test) and collection period; lenders prioritise ability to repay.', 'Profitability comparison [1]; liquidity comparison [1]; recommendation [1] [3]')])


@spec(t22_1, D=(2, 3, 4, 5))
def t221_cmp(r, D):
    a, b = r.sample(FIRMS, 2)
    da, db = _fin(r), _fin(r)
    ra, rb = _ratios(da), _ratios(db)
    keys = r.sample(list(ra), 3 if D <= 3 else 4)
    setup = f'The following ratios have been calculated for two businesses in the same industry: ' + '; '.join(f'{k}: {a} {_rf(k, ra[k])}, {b} {_rf(k, rb[k])}' for k in keys) + '.'
    better = []
    for k in keys:
        hi_good = k != 'trade receivables days'
        w = a if (ra[k] > rb[k]) == hi_good else b
        better.append(f'{k}: {w} {"better" if k not in ("current ratio",) else "higher (better liquidity if not excessive)"}')
    parts = [('Compare the performance of the two businesses using these ratios.', '; '.join(better) + '.', '; '.join(f'{x} [1]' for x in better) + f' [{len(keys)}]'),
             ('Suggest one reason for the difference in the first ratio.', 'E.g. different pricing policy, purchasing costs, cost control, credit policy or capital structure, depending on the ratio.', 'Plausible reason linked to ratio [1]; explanation [1] [2]'),
             ('State one limitation of comparing the two businesses in this way.', 'Different accounting policies, year ends or business size; ratios are historical.', 'Valid limitation [1]')]
    k0 = keys[0]
    hi0 = k0 != 'trade receivables days'
    win = a if (ra[k0] > rb[k0]) == hi0 else b
    lose = b if win == a else a
    why = (f'a higher {k0} is better' if hi0 else 'a lower trade receivables days figure is better, because cash is collected more quickly')
    err = (f'concludes that {lose} performs better on {k0}', why, f'{win} performs better on {k0}',
           f'{a} {_rf(k0, ra[k0])} compared with {b} {_rf(k0, rb[k0])}', 'conclusion')
    return {'setup': setup, 'parts': parts, 'ctx': {'f': a}, 'err': err}


t22_2 = A(22, 'Stakeholders\' interests in financial information', ["stakeholders' interests in financial information", 'stakeholders', 'stakeholders interests'],
          mcqs=[('Which stakeholder is most interested in the gearing ratio?', 'A potential lender', ['A customer', 'An employee', 'A competitor'], 'Risk of lending'),
                ('Shareholders in a company are most interested in', 'profitability and dividends', ['the current ratio only', 'the trade payables days', 'the number of suppliers'], 'Return on investment'),
                ('Employees are likely to use financial statements to assess', 'job security and the ability to pay wage increases', ['the gearing ratio of competitors', 'the dividend policy', 'the share price only'], 'Profitability and stability'),
                ('Which stakeholder would be most interested in the trade payables payment period?', 'A trade supplier', ['A shareholder', 'The tax authority', 'A customer'], 'How quickly it will be paid'),
                ('The government uses company financial statements mainly to', 'assess tax and collect economic statistics', ['decide the gross margin', 'set dividends', 'choose suppliers'], 'Tax and statistics')],
          exps=[('Explain why different stakeholders focus on different ratios.', 'Each has different decisions: lenders focus on liquidity and gearing (repayment risk); shareholders on profitability and dividends; suppliers on short-term liquidity.', 'Different decisions/interests [1]; two examples [1] [2]'),
                ('Explain why a customer might be interested in the financial statements of a supplier.', 'To be sure the supplier will survive to provide continued supplies, warranties and after-sales service.', 'Continuity of supply [1]; after-sales/warranty [1] [2]')],
          disc=[('Discuss whether the published financial statements of {f} give stakeholders all the information they need.', 'They give audited financial data, but are historical, exclude non-financial information (staff, environment) and may be too summarised.', 'Useful content [1]; limitations [1]; judgement [1] [3]')])


STAKE = [('a bank considering a loan', ['gearing ratio', 'interest cover', 'current ratio'], 'the ability to pay interest and repay the loan'),
         ('a trade supplier', ['acid test ratio', 'trade payables days', 'current ratio'], 'whether it will be paid on time'),
         ('a potential shareholder', ['ROCE', 'profit margin', 'dividend per share'], 'the return on the investment'),
         ('the employees', ['profit margin', 'ROCE', 'current ratio'], 'job security and pay prospects'),
         ('the owner', ['ROCE', 'gross margin', 'expenses to revenue'], 'whether the business is worth continuing and how to improve it')]


@spec(t22_2, typ='short')
def t222_stake(r, D):
    f = firm(r)
    s1, s2 = r.sample(STAKE, 2)
    setup = f'{f} has sent its latest financial statements to {s1[0]} and to {s2[0]}.'
    parts = [(f'Identify two ratios that {s1[0]} would be most interested in and explain why.', f'{s1[1][0]} and {s1[1][1]}, because they show {s1[2]}.', f'Two relevant ratios [1 each]; reason – {s1[2]} [1] [3]'),
             (f'Explain why {s2[0]} might reach a different view of the business from {s1[0]}.', f'{cap1(s2[0])} is concerned with {s2[2]}, a different decision from {s1[2]}.', 'Different interests [1]; explanation [1] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'Which ratio is {s1[0]} most likely to examine?', s1[1][0], [x for x in ['gross margin', 'inventory turnover', 'non-current asset turnover', 'expenses to revenue', 'mark-up'] if x not in s1[1]][:4], f'{s1[0]} is interested in {s1[2]}'),
            'err': (f'says that {s1[0]} will mainly look at the inventory turnover', f'{s1[0]} is concerned with {s1[2]}, which inventory turnover does not show',
                    f'{s1[1][0]} and {s1[1][1]}', f'link the ratios to {s1[2]}', 'ratios')}


t22_3 = A(22, 'Limitations of ratio analysis and financial statements', ['limitations of ratio analysis and financial statements', 'limitations of ratio analysis'],
          mcqs=[('Which is a limitation of ratio analysis?', 'Ratios are based on historical information', ['Ratios allow comparison between years', 'Ratios summarise large amounts of data', 'Ratios highlight trends'], 'Past, not future'),
                ('Inflation can distort ratios because', 'non-current assets are shown at historical cost while revenue is at current prices', ['it increases the number of transactions', 'it reduces the gross margin always', 'ratios cannot use money values'], 'Mismatch of values'),
                ('The statement of financial position may not be typical of the year because', 'it shows the position at one date only', ['it covers twelve months', 'it includes all transactions', 'it is audited'], 'Seasonal effects'),
                ('Window dressing means', 'arranging transactions near the year end to make the statements look better', ['cleaning the shop windows', 'revaluing assets annually', 'preparing a cash budget'], 'Manipulating year-end figures'),
                ('Financial statements do not show', 'the skills and morale of the workforce', ['profit for the year', 'non-current assets', 'trade payables'], 'Non-monetary factors')],
          exps=[('Explain two limitations of using ratios to compare two businesses.', 'Different accounting policies (depreciation, inventory valuation); different sizes, locations or year ends; ratios are historical and ignore non-financial factors.', 'Two limitations explained [1 each] [2]'),
                ('Explain how the timing of the year end can affect liquidity ratios.', 'A seasonal business may have high inventory before its busy season or high cash after it, so ratios at one date may not represent the year.', 'Seasonal fluctuations [1]; one date not representative [1] [2]')],
          disc=[('Discuss how far ratio analysis can be relied on when deciding whether to invest in {f}.', 'Ratios give useful comparisons, but they are historical, depend on policies and ignore qualitative factors such as management quality and market prospects.', 'Usefulness [1]; limitations [1]; judgement [1] [3]')])


LIMS = [('changed its depreciation method from reducing balance to straight line this year', 'profit and ROCE are not comparable with last year because of the change in accounting policy'),
        ('collected a large overdue debt and delayed paying suppliers just before the year end', 'year-end liquidity ratios are flattered (window dressing) and not typical'),
        ('has premises bought twenty years ago at historical cost', 'capital employed is understated, so ROCE looks high compared with a newer competitor'),
        ('sells mainly at Christmas, and its year end is 31 January', 'inventory and cash at the year end are not typical of the year'),
        ('is three times the size of the competitor it is compared with', 'ratios may differ because of economies of scale, not better management'),
        ('has just lost its most experienced manager', 'this non-financial factor is not shown in the statements but will affect future performance')]


@spec(t22_3, typ='short')
def t223_lim(r, D):
    f = firm(r)
    k = 1 if D <= 2 else 2
    its = r.sample(LIMS, k)
    setup = f'An analyst is using ratios to assess {f}. She learns that the business ' + ' and '.join(x[0] for x in its) + '.'
    parts = [('Explain how this information limits the usefulness of the ratios.', cap1('; '.join(x[1] for x in its)) + '.', '; '.join(f'{x[1]} [2]' for x in its) + f' [{2 * k}]'),
             ('State two other limitations of ratio analysis.', 'Historical data; inflation; different accounting policies; non-financial factors ignored; year-end figures only.', 'Two limitations [1 each] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f}, 'mcq': None,
            'err': ('says that the ratios can be relied on without adjustment', its[0][1], 'the ratios should be interpreted with caution, adjusting for this factor or using other information',
                    'identify the factor and its effect on the ratios', 'conclusion')}


CHAPTERS[22] = [t22_1, t22_2, t22_3]


# ===================================================================== 23 Costing: materials and labour
COSTS = [('timber used to make tables', 'direct material', 'variable'), ('wages of machine operators paid per unit', 'direct labour', 'variable'), ('royalty paid for each unit made', 'direct expense', 'variable'),
         ('factory rent', 'indirect (overhead)', 'fixed'), ('salary of the factory supervisor', 'indirect (overhead)', 'fixed'), ('lubricating oil for machines', 'indirect (overhead)', 'variable'),
         ('depreciation of factory machinery (straight line)', 'indirect (overhead)', 'fixed'), ('insurance of the factory', 'indirect (overhead)', 'fixed'), ('glue and screws used in assembly', 'indirect (overhead)', 'variable'),
         ('fabric used to cover sofas', 'direct material', 'variable'), ('factory cleaners\' wages', 'indirect (overhead)', 'fixed')]

t23_1 = A(23, 'Classification of costs: direct, indirect, fixed, variable', ['classification of costs: direct, indirect, fixed, variable', 'classification of costs', 'fixed and variable costs', 'direct and indirect'],
          mcqs=[('A direct cost is one that', 'can be traced directly to a unit of output', ['does not change with output', 'is shared between departments', 'is incurred in the office'], 'Traceable'),
                ('A fixed cost', 'stays the same in total when output changes within the relevant range', ['rises in proportion to output', 'is always a direct cost', 'is the same per unit at every output'], 'Total fixed'),
                ('As output increases, fixed cost per unit', 'falls', ['rises', 'stays the same', 'becomes zero'], 'Spread over more units'),
                ('A semi-variable cost', 'has a fixed element and a variable element', ['is always direct', 'is fixed per unit', 'changes only in the long run'], 'e.g. telephone: rental + calls'),
                ('Which is an indirect cost for a furniture maker?', 'Factory supervisor\'s salary', ['Wood used in chairs', 'Wages of carpenters paid per chair', 'Royalty per chair'], 'Cannot be traced to a unit')],
          exps=[('Explain why it is important for a business to classify costs as fixed or variable.', 'It allows marginal costing, break-even analysis and decision making (e.g. special orders), because only variable costs change with output.', 'Behaviour with output [1]; use in decisions/break-even [1] [2]'),
                ('Distinguish between direct costs and indirect costs, giving an example of each.', 'Direct costs can be identified with a unit (e.g. raw materials); indirect costs cannot and are shared (e.g. factory rent).', 'Direct + example [1]; indirect + example [1] [2]')],
          disc=[('Explain why a cost may be fixed in the short run but variable in the long run for {f}.', 'Factory rent is fixed until output exceeds capacity; then new premises are needed, so costs step up (stepped fixed cost).', 'Relevant range/capacity [1]; step/long-run change [1] [2]')])


@spec(t23_1)
def t231_class(r, D):
    f = firm(r)
    k = 4 if D <= 2 else (5 if D == 3 else 6)
    its = r.sample(COSTS, k)
    vals = [step(r, 2000, 40000, 100) for _ in its]
    pc_ = sum(v for (_, c, _), v in zip(its, vals) if c.startswith('direct'))
    oh = sum(v for (_, c, _), v in zip(its, vals) if c.startswith('indirect'))
    setup = f'{f} manufactures furniture. Costs for May included: ' + '; '.join(f'{n} {m(v)}' for (n, _, _), v in zip(its, vals)) + '.'
    parts = [('Classify each cost as direct or indirect, and as fixed or variable.', '; '.join(f'{n}: {c}, {b}' for n, c, b in its), '; '.join(f'{n}: {c}/{b}' for n, c, b in its) + f' [{k}]'),
             ('Calculate the prime cost and the total production overheads.', f'Prime cost {m(pc_)}; overheads {m(oh)}', f'Direct costs {m(pc_)} [1]; indirect costs {m(oh)} [1] [2]')]
    if D >= 3:
        u1, u2 = r.choice([(2000, 3000), (4000, 6000), (5000, 8000)])
        fc = step(r, 2000, 8000, 100)
        vc = r.choice([0.5, 0.8, 1.2, 1.5, 2])
        c1, c2 = fc + vc * u1, fc + vc * u2
        parts.append((f'Factory power cost {m(c1)} when {u1:,} units were made and {m(c2)} when {u2:,} units were made. Use the high-low method to find the variable cost per unit and the fixed cost.', f'Variable {m2(vc)} per unit; fixed {m(fc)}',
                      f'({m(c2)} − {m(c1)}) ÷ ({u2:,} − {u1:,}) = {m2(vc)} [1]; fixed {m(c2)} − {u2:,} × {m2(vc)} = {m(fc)} [1] [2]'))
    oi = [(n, v) for (n, c, _), v in zip(its, vals) if c.startswith('indirect')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the prime cost?', *num_opts(m, pc_, [pc_ + oh, oh, pc_ + (oi[0][1] if oi else 500)]), 'Total of direct costs'),
            'err': (f'included {oi[0][0]} in prime cost, giving {m(pc_ + oi[0][1])}', f'{oi[0][0]} cannot be traced to a unit of output; it is an overhead, not a direct cost', m(pc_), ' + '.join(m(v) for (_, c, _), v in zip(its, vals) if c.startswith('direct')), 'prime cost') if oi else None}


t23_2 = A(23, 'Valuing material issues: FIFO and AVCO stores ledger', ['valuing material issues: fifo and avco stores ledger', 'stores ledger', 'material issues'],
          mcqs=[('In a stores ledger card using FIFO, issues are priced at', 'the cost of the earliest receipts still in stock', ['the latest purchase price', 'the average of all purchases', 'the selling price'], 'First in, first out'),
                ('When prices are falling, FIFO charges production with', 'higher (older) costs than AVCO', ['lower costs than AVCO', 'the same costs as AVCO', 'replacement cost'], 'Older prices are higher'),
                ('Under AVCO, after a receipt of 200 kg at $5 into a balance of 300 kg at $4, the new average cost is', '$4.40 per kg', ['$4.50 per kg', '$5.00 per kg', '$4.00 per kg'], '(1,200 + 1,000) ÷ 500'),
                ('A stores ledger card records', 'receipts, issues and balance of each material', ['only the purchases of materials', 'the wages of storekeepers', 'sales of finished goods'], 'Perpetual inventory'),
                ('Which material valuation method best reflects current costs in issues to production when prices are rising?', 'AVCO (compared with FIFO)', ['FIFO', 'Both equally', 'Neither'], 'Average includes more recent prices')],
          exps=[('Explain why the method used to price material issues affects both product cost and closing inventory.', 'The same total cost is split between issues (charged to production) and the balance (closing inventory); a method that charges more to issues leaves less in inventory.', 'Total cost divided [1]; trade-off between issues and inventory [1] [2]'),
                ('Explain one advantage of FIFO for valuing material issues.', 'It is logical (oldest materials used first), easy to apply, and closing inventory is at recent prices; it is acceptable under IAS 2.', 'Advantage explained [2]')],
          disc=[('Discuss which method {f} should use if material prices are rising quickly.', 'AVCO charges production nearer current cost, giving more realistic prices for quotes; FIFO gives higher profit and inventory values; consistency is required.', 'AVCO point [1]; FIFO point [1]; recommendation [1] [3]')])


@spec(t23_2)
def t232_stores(r, D):
    f = firm(r)
    mat = r.choice(['steel sheet', 'resin', 'cotton yarn', 'aluminium bar', 'paint base'])
    ou, op_, rows, fifo, av, avq = _stores(r, D)
    total_in = (ou * op_ if ou else 0) + sum(q * p for k, q, p in rows if k == 'in')
    issues_fifo = total_in - fifo
    issues_av = total_in - av
    days_ = [2, 7, 12, 18, 23, 27]
    lines = ([f'1 March: balance {ou} kg at {m2(op_)} per kg'] if ou else []) + [f'{days_[i]} March: ' + (f'received {q} kg at {m2(p)}' if k == 'in' else f'issued {q} kg to production') for i, (k, q, p) in enumerate(rows)]
    setup = f'{f} uses {mat} in production. Its stores ledger card for March shows: ' + '; '.join(lines) + '.'
    parts = [('Using FIFO, calculate the total cost of materials issued to production and the closing inventory value.', f'Issues {m2(issues_fifo)}; closing inventory {m2(fifo)}', f'Closing {avq} kg at latest prices = {m2(fifo)} [2]; issues = total {m2(total_in)} − {m2(fifo)} = {m2(issues_fifo)} [1] [3]')]
    if D >= 3:
        parts.append(('Using AVCO (perpetual), calculate the closing inventory value and the cost of issues.', f'Closing {m2(av)}; issues {m2(issues_av)}', f'Average recalculated after each receipt [1]; closing {m2(av)} [1]; issues {m2(issues_av)} [1] [3]'))
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the closing inventory value using FIFO?', *num_opts(m2, fifo, [av, issues_fifo, avq * (op_ if ou else rows[0][2])]), f'{avq} kg at latest prices'),
            'err': (f'valued the issues using FIFO at {m2(issues_av)}', 'the AVCO figures were used; under FIFO each issue is priced at the earliest remaining receipts', m2(issues_fifo), f'{m2(total_in)} − {m2(fifo)}', 'cost of issues (FIFO)') if abs(issues_av - issues_fifo) > 0.5 else None}


t23_3 = A(23, 'Labour remuneration: time rates, piece rates and bonus schemes', ['labour remuneration: time rates, piece rates and bonus schemes', 'time rates', 'piece rates', 'bonus schemes'],
          mcqs=[('A worker paid by time rate is paid', 'for the hours worked, regardless of output', ['for each unit produced', 'a share of profit', 'only when targets are met'], 'Hourly pay'),
                ('A worker is paid $12 per hour and overtime at time and a half. For 42 hours with 2 hours of overtime, gross pay is', '$516', ['$504', '$756', '$480'], '40 × 12 + 2 × 18'),
                ('A piece-rate worker produced 380 units at $1.50 per unit, with a guaranteed minimum of $600 a week. Pay is', '$600', ['$570', '$1,170', '$380'], '570 < 600, minimum applies'),
                ('A disadvantage of piece rates is that', 'quality may suffer as workers rush to increase output', ['workers have no incentive to work faster', 'pay is hard to calculate', 'they are illegal'], 'Quantity over quality'),
                ('Overtime premium is usually treated as', 'an indirect cost (overhead) unless caused by a specific job', ['a direct material cost', 'a selling expense', 'part of the selling price'], 'Spread across production')],
          exps=[('Explain one advantage and one disadvantage of paying workers by time rate.', 'Advantage: simple, encourages quality, stable pay. Disadvantage: no incentive to work faster; needs supervision.', 'Advantage [1]; disadvantage [1] [2]'),
                ('Explain why a guaranteed minimum wage is often included in a piece-rate scheme.', 'It protects workers when output is low for reasons beyond their control (machine breakdowns, material shortages), and may be legally required.', 'Protect earnings [1]; reason outside control/legal [1] [2]')],
          disc=[('Evaluate whether {f} should change from time rates to piece rates.', 'Piece rates can raise output and link pay to productivity but may reduce quality and create conflict; suitable where output is measurable.', 'Benefit [1]; drawback [1]; judgement [1] [3]')])


@spec(t23_3)
def t233_lab(r, D):
    f = firm(r)
    a = pp(r)
    kind = r.choice(['time', 'piece', 'bonus']) if D >= 2 else r.choice(['time', 'piece'])
    rate = step(r, 900, 2500, 50) / 100
    if kind == 'time':
        std = r.choice([35, 37, 38, 40])
        hrs = std + r.choice([2, 3, 4, 5, 6])
        ot = r.choice([1.25, 1.5, 2])
        basic = std * rate
        otp = (hrs - std) * rate * ot
        pay = basic + otp
        setup = f'{a} works in the factory of {f} and is paid {m2(rate)} per hour for a {std}-hour week, with overtime at {ot:g} times the basic rate. Last week {a} worked {hrs} hours.'
        parts = [(f'Calculate {a}\'s gross pay for the week.', m2(pay), f'Basic {std} × {m2(rate)} = {m2(basic)} [1]; overtime {hrs - std} × {m2(rate * ot)} = {m2(otp)} [1]; total {m2(pay)} [1] [3]'),
                 ('Calculate the overtime premium.', m2((hrs - std) * rate * (ot - 1)), f'{hrs - std} × {m2(rate)} × {ot - 1:g} = {m2((hrs - std) * rate * (ot - 1))} [1]')]
        wrong = hrs * rate * ot
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
                'mcq': ('What is the gross pay for the week?', *num_opts(m2, pay, [hrs * rate, wrong, basic + (hrs - std) * rate]), f'{m2(basic)} + {m2(otp)}'),
                'err': (f'calculated the gross pay as {m2(wrong)}', 'all hours were paid at the overtime rate; only hours beyond the standard week earn overtime', m2(pay), f'{std} × {m2(rate)} + {hrs - std} × {m2(rate * ot)}', 'gross pay')}
    if kind == 'piece':
        pr = step(r, 40, 300, 5) / 100
        mn = step(r, 300, 700, 10)
        u = r.randint(int(mn / pr * 0.7), int(mn / pr * 1.4))
        earn = u * pr
        pay = max(earn, mn)
        setup = f'{a} is paid {m2(pr)} for each unit produced at {f}, with a guaranteed minimum weekly wage of {m(mn)}. Last week {a} produced {u:,} units.'
        parts = [(f'Calculate {a}\'s pay for the week.', m2(pay), f'{u:,} × {m2(pr)} = {m2(earn)} [1]; {"above" if earn >= mn else "below"} minimum, so pay {m2(pay)} [1] [2]'),
                 (f'Calculate the number of units {a} must produce to earn more than the guaranteed minimum.', f'{int(mn / pr) + 1:,} units', f'{m(mn)} ÷ {m2(pr)} = {mn / pr:.1f} → {int(mn / pr) + 1:,} units [1]')]
        return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
                'mcq': ('What is the pay for the week?', *num_opts(m2, pay, [earn if earn != pay else mn, earn + mn, u * pr * 1.5]), f'max({m2(earn)}, {m(mn)})'),
                'err': (f'paid {a} {m2(earn)}', 'the guaranteed minimum was ignored; when piece-rate earnings fall below it, the minimum is paid', m2(pay), f'max({m2(earn)}, {m(mn)})', 'pay') if earn < mn else None}
    std_h = r.choice([4, 5, 6])
    jobs = r.choice([8, 10, 12])
    act = std_h * jobs - r.choice([4, 6, 8, 10])
    saved = std_h * jobs - act
    share = r.choice([50, 40, 33])
    bonus = saved * rate * share / 100
    pay = act * rate + bonus
    setup = f'At {f} each job has a standard time of {std_h} hours. {a} is paid {m2(rate)} per hour plus a bonus of {share}% of the time saved at the hourly rate. Last week {a} completed {jobs} jobs in {act} hours.'
    parts = [('Calculate the time saved and the bonus.', f'{saved} hours saved; bonus {m2(bonus)}', f'Standard {std_h} × {jobs} = {std_h * jobs} hours [1]; saved {saved} hours [1]; bonus {saved} × {m2(rate)} × {share}% = {m2(bonus)} [1] [3]'),
             (f'Calculate {a}\'s total pay.', m2(pay), f'{act} × {m2(rate)} + {m2(bonus)} = {m2(pay)} [1]')]
    wrong = act * rate + saved * rate
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the bonus earned?', *num_opts(m2, bonus, [saved * rate, std_h * jobs * rate * share / 100, bonus * 2]), f'{saved} × {m2(rate)} × {share}%'),
            'err': (f'calculated total pay as {m2(wrong)}', f'the whole of the time saved was paid; the scheme pays only {share}% of the time saved', m2(pay), f'{act} × {m2(rate)} + {m2(bonus)}', 'total pay')}


CHAPTERS[23] = [t23_1, t23_2, t23_3]


# ===================================================================== 24 Absorption costing
OH_BASES = [('factory rent', 'floor area (m²)'), ('machine power', 'machine hours'), ('supervision', 'number of employees'), ('depreciation of machinery', 'value of machinery'), ('factory insurance', 'floor area (m²)'), ('canteen costs', 'number of employees')]
DEPTS = [('Machining', 'Assembly'), ('Cutting', 'Finishing'), ('Moulding', 'Packing'), ('Pressing', 'Painting')]


def _apport(r, D):
    da, db = r.choice(DEPTS)
    k = 2 if D <= 2 else (3 if D == 3 else 4)
    its = r.sample(OH_BASES, k)
    bases = {}
    rows = []
    for nm_, b in its:
        if b not in bases:
            if b == 'floor area (m²)':
                x, y = step(r, 200, 1500, 50), step(r, 200, 1500, 50)
            elif b == 'machine hours':
                x, y = step(r, 1000, 9000, 100), step(r, 500, 6000, 100)
            elif b == 'number of employees':
                x, y = r.randint(5, 40), r.randint(5, 40)
            else:
                x, y = step(r, 20000, 150000, 5000), step(r, 10000, 100000, 5000)
            bases[b] = (x, y)
        x, y = bases[b]
        tot = step(r, 2000, 40000, 100)
        _a = round(tot * x / (x + y))
        rows.append((nm_, b, tot, _a, tot - _a))
    alloc = (step(r, 5000, 30000, 100), step(r, 5000, 30000, 100))
    ta = alloc[0] + sum(x[3] for x in rows)
    tb = alloc[1] + sum(x[4] for x in rows)
    return da, db, bases, rows, alloc, ta, tb


t24_1 = A(24, 'Allocation and apportionment of overheads to cost centres', ['allocation and apportionment of overheads to cost centres', 'allocation and apportionment', 'cost centres'],
          mcqs=[('Allocation of overheads means', 'charging an overhead in full to the one cost centre that caused it', ['sharing an overhead between cost centres on a fair basis', 'charging overheads to units of output', 'writing off overheads to profit'], 'Wholly incurred by one centre'),
                ('The most suitable basis for apportioning factory rent is', 'floor area', ['number of employees', 'machine hours', 'direct labour hours'], 'Space occupied'),
                ('Canteen costs are best apportioned on the basis of', 'number of employees', ['floor area', 'value of machinery', 'units produced'], 'Usage by staff'),
                ('Rent $24,000; floor areas: A 600 m², B 400 m². Rent apportioned to A is', '$14,400', ['$9,600', '$12,000', '$24,000'], '24,000 × 600/1,000'),
                ('A cost centre is', 'a location, function or item of equipment for which costs are collected', ['a product sold to customers', 'a type of profit', 'a book of prime entry'], 'Collecting point for costs')],
          exps=[('Distinguish between allocation and apportionment of overheads.', 'Allocation charges a whole overhead to one cost centre that incurred it; apportionment shares an overhead that benefits several centres using a fair basis.', 'Allocation – one centre [1]; apportionment – shared on a basis [1] [2]'),
                ('Explain why the basis chosen for apportionment should reflect the benefit each cost centre receives.', 'So that each department bears a fair share of overheads, giving more accurate product costs and prices.', 'Fair share/causal link [1]; accurate product cost [1] [2]')],
          disc=[('Discuss whether the overhead analysis of {f} gives an accurate cost for its products.', 'Apportionment bases are approximations; budgeted figures may differ from actual; but it gives a reasonable full cost for pricing.', 'Approximation [1]; budget vs actual [1]; judgement [1] [3]')])


@spec(t24_1)
def t241_app(r, D):
    f = firm(r)
    da, db, bases, rows, alloc, ta, tb = _apport(r, D)
    bt = '; '.join(f'{b}: {da} {x:,}, {db} {y:,}' for b, (x, y) in bases.items())
    setup = f'{f} has two production departments, {da} and {db}. Overheads allocated directly: {da} {m(alloc[0])}, {db} {m(alloc[1])}. Overheads to be apportioned: ' + ', '.join(f'{n} {m(t)} (on {b})' for n, b, t, _, _ in rows) + f'. Data: {bt}.'
    parts = [('Apportion the overheads and calculate the total overheads of each department.', f'{da} {m(ta)}; {db} {m(tb)}', '; '.join(f'{n}: {da} {m(a)}, {db} {m(b_)}' for n, _, _, a, b_ in rows) + f' [{len(rows)}]; totals {da} {m(ta)}, {db} {m(tb)} [1] [{len(rows) + 1}]'),
             ('Explain why the basis used for the first overhead is appropriate.', f'{cap1(rows[0][0])} is related to {rows[0][1]}, so departments using more of it bear a larger share.', 'Link between cost and basis [1]')]
    n0, b0, t0, a0, b0v = rows[0]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'How much {n0} is apportioned to {da}?', *num_opts(m, a0, [t0 / 2, b0v, t0]), f'{m(t0)} × {bases[b0][0]:,}/{sum(bases[b0]):,}'),
            'err': (f'apportioned {n0} equally, giving each department {m(t0 / 2)}', f'{n0} should be shared on the basis of {b0}', f'{da} {m(a0)}, {db} {m(b0v)}', f'{m(t0)} × {bases[b0][0]:,}/{sum(bases[b0]):,}', 'apportionment') if abs(a0 - t0 / 2) > 0.5 else None}


t24_2 = A(24, 'Reapportionment of service department costs', ['reapportionment of service department costs', 'service department', 'reapportionment'],
          mcqs=[('Service department costs are reapportioned to production departments because', 'overhead absorption rates are calculated only for production departments', ['service departments make products', 'they are fixed costs', 'they are direct costs'], 'Units pass through production centres'),
                ('Maintenance department costs $30,000 are shared Machining 60%, Assembly 40%. Machining receives', '$18,000', ['$12,000', '$30,000', '$15,000'], '60% × 30,000'),
                ('Which is an example of a service department?', 'Stores', ['Assembly', 'Machining', 'Finishing'], 'Supports production'),
                ('The direct method of reapportionment', 'ignores services that service departments provide to each other', ['includes all inter-service work', 'apportions costs equally', 'charges service costs to selling expenses'], 'Simplest method'),
                ('A suitable basis for reapportioning the stores department is', 'number of material requisitions', ['floor area of the office', 'sales revenue', 'number of customers'], 'Usage')],
          exps=[('Explain why service department costs must be included in product costs.', 'Services such as maintenance and stores are needed to make the products; excluding their costs would understate product cost and lead to under-pricing.', 'Needed for production [1]; avoids understated cost [1] [2]'),
                ('Explain one limitation of the direct method of reapportionment.', 'It ignores work that service departments do for each other, so production department totals may be inaccurate.', 'Ignores inter-service work [1]; less accurate [1] [2]')],
          disc=[('Discuss whether {f} should outsource its maintenance department.', 'Outsourcing may cut cost and give specialist skills, but loses control and quick response; compare outside price with avoidable costs.', 'Cost point [1]; control/quality point [1]; judgement [1] [3]')])


@spec(t24_2)
def t242_re(r, D):
    f = firm(r)
    da, db = r.choice(DEPTS)
    sv = r.choice(['Maintenance', 'Stores', 'Canteen'])
    pa, pb = step(r, 20000, 90000, 100), step(r, 20000, 90000, 100)
    s = step(r, 5000, 30000, 100)
    pct = r.choice([40, 50, 55, 60, 65, 70, 75])
    sa, sb = s * pct / 100, s * (100 - pct) / 100
    setup = f'{f} has production departments {da} and {db} and a service department, {sv}. After apportionment, overheads are: {da} {m(pa)}, {db} {m(pb)}, {sv} {m(s)}. {sv} provides {pct}% of its services to {da} and the rest to {db}.'
    parts = [(f'Reapportion the {sv} costs and calculate the total overheads of each production department.', f'{da} {m(pa + sa)}; {db} {m(pb + sb)}', f'{sv} to {da} {pct}% = {m(sa)}, to {db} {m(sb)} [1]; totals {da} {m(pa + sa)}, {db} {m(pb + sb)} [1] [2]'),
             ('Check that total overheads are unchanged.', m(pa + pb + s), f'{m(pa + sa)} + {m(pb + sb)} = {m(pa + pb + s)} [1]')]
    if D >= 3:
        h = step(r, 2000, 10000, 100)
        parts.append((f'{da} works {h:,} machine hours. Calculate its overhead absorption rate per machine hour.', m2((pa + sa) / h), f'{m(pa + sa)} ÷ {h:,} = {m2((pa + sa) / h)} [1]'))
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What are the total overheads of {da} after reapportionment?', *num_opts(m, pa + sa, [pa, pa + sb, pa + s]), f'{m(pa)} + {pct}% × {m(s)}'),
            'err': (f'added the whole {sv} cost of {m(s)} to {da}', f'only {pct}% of the {sv} services are used by {da}', m(pa + sa), f'{m(pa)} + {m(sa)}', f'{da} total') if pct != 100 else None}


t24_3 = A(24, 'Overhead absorption rates: labour-hour and machine-hour', ['overhead absorption rates: labour-hour and machine-hour', 'overhead absorption rate', 'machine-hour', 'labour-hour'],
          mcqs=[('An overhead absorption rate (OAR) is calculated as', 'budgeted overheads ÷ budgeted activity', ['actual overheads ÷ actual activity', 'budgeted overheads × budgeted hours', 'direct costs ÷ units'], 'Predetermined rate'),
                ('A machine-hour rate is most appropriate for a department that is', 'highly automated', ['labour intensive', 'a service department', 'an office'], 'Machines drive overheads'),
                ('Budgeted overheads $90,000; budgeted labour hours 15,000. The OAR is', '$6.00 per labour hour', ['$0.17 per labour hour', '$6.67 per labour hour', '$15.00 per labour hour'], '90,000 ÷ 15,000'),
                ('Why are budgeted figures used to calculate absorption rates?', 'So product costs can be calculated during the year, e.g. to set prices', ['Because actual figures are always wrong', 'To increase profit', 'Because the law requires it'], 'Timeliness'),
                ('A job takes 4 machine hours in a department with an OAR of $15 per machine hour. The overhead absorbed is', '$60', ['$19', '$3.75', '$15'], '4 × 15')],
          exps=[('Explain why a labour-hour rate may be preferred in a labour-intensive department.', 'Most overheads (supervision, canteen) relate to labour time, so jobs using more labour hours should absorb more overheads.', 'Overheads linked to labour [1]; fair absorption [1] [2]'),
                ('Explain why a business uses predetermined (budgeted) absorption rates.', 'Actual overheads and activity are not known until the year end; a predetermined rate allows product costs and prices to be calculated as jobs are done.', 'Actual not known [1]; costs/prices during year [1] [2]')],
          disc=[('Evaluate whether {f} should use a single factory-wide absorption rate instead of departmental rates.', 'A single rate is simpler but may misallocate overheads when departments differ (machine v labour intensive); departmental rates are more accurate.', 'Simplicity [1]; accuracy [1]; judgement [1] [3]')])


@spec(t24_3)
def t243_oar(r, D):
    f = firm(r)
    da, db = r.choice(DEPTS)
    oa, ob = step(r, 40000, 200000, 1000), step(r, 30000, 150000, 1000)
    mh = step(r, 4000, 20000, 500)
    lh = step(r, 4000, 20000, 500)
    ra, rb = oa / mh, ob / lh
    jm, jl = r.randint(2, 12), r.randint(3, 15)
    dm, dl = step(r, 100, 800, 5), step(r, 80, 600, 5)
    oh = jm * ra + jl * rb
    tc = dm + dl + oh
    setup = f'{f} has two production departments. {da} is machine intensive: budgeted overheads {m(oa)}, budgeted machine hours {mh:,}. {db} is labour intensive: budgeted overheads {m(ob)}, budgeted direct labour hours {lh:,}.'
    parts = [('Calculate a suitable overhead absorption rate for each department.', f'{da} {m2(ra)} per machine hour; {db} {m2(rb)} per labour hour', f'{m(oa)} ÷ {mh:,} = {m2(ra)} [1]; {m(ob)} ÷ {lh:,} = {m2(rb)} [1] [2]')]
    if D >= 2:
        parts.append((f'Job J{r.randint(100, 999)} uses direct materials {m(dm)}, direct labour {m(dl)}, {jm} machine hours in {da} and {jl} labour hours in {db}. Calculate the total cost of the job.', m2(tc),
                      f'Overheads {jm} × {m2(ra)} + {jl} × {m2(rb)} = {m2(oh)} [1]; total {m(dm)} + {m(dl)} + {m2(oh)} = {m2(tc)} [1] [2]'))
    parts.append(('Explain why different bases are used for the two departments.', f'Overheads in {da} are driven by machine use; in {db} by labour time, so each rate reflects the main cause of overheads.', 'Machine v labour driven [1]; fairness/accuracy [1] [2]'))
    wrong = oa / lh
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is the overhead absorption rate for {da}?', *num_opts(m2, ra, [wrong, mh / oa * 100, (oa + ob) / (mh + lh)]), f'{m(oa)} ÷ {mh:,}'),
            'err': (f'calculated the {da} absorption rate as {m2((oa + ob) / (mh + lh))} per hour', 'a single blanket rate was used for both departments; each department needs its own rate based on its main activity', f'{m2(ra)} per machine hour', f'{m(oa)} ÷ {mh:,}', 'absorption rate')}


t24_4 = A(24, 'Under- and over-absorption of overheads', ['under- and over-absorption of overheads', 'under-absorption', 'over-absorption'],
          mcqs=[('Overheads are under-absorbed when', 'overheads absorbed are less than actual overheads', ['absorbed overheads exceed actual overheads', 'budgeted hours are exceeded', 'the OAR is too high'], 'Absorbed < incurred'),
                ('OAR $8 per hour; actual hours 9,500; actual overheads $80,000. The result is', '$4,000 under-absorbed', ['$4,000 over-absorbed', '$76,000 absorbed exactly', '$84,000 under-absorbed'], 'Absorbed 76,000 < 80,000'),
                ('Under-absorbed overheads are', 'added to cost of sales (reducing profit) at the period end', ['added to closing inventory', 'carried forward as an asset', 'ignored'], 'Charged to IS'),
                ('Over-absorption can be caused by', 'actual activity being higher than budgeted', ['actual overheads higher than budgeted', 'actual hours lower than budget', 'a lower OAR'], 'More hours × rate'),
                ('An over-absorption of overheads', 'increases profit when adjusted', ['reduces profit', 'has no effect on profit', 'increases cost of sales'], 'Too much was charged')],
          exps=[('Explain two causes of under-absorption of overheads.', 'Actual overheads were higher than budgeted; actual activity (hours) was lower than budgeted; or both.', 'Overheads higher [1]; activity lower [1] [2]'),
                ('Explain how an over-absorption is treated in the financial statements.', 'Too much overhead was charged to production, so the excess is credited to the income statement (reducing cost of sales), increasing profit.', 'Excess charged [1]; credited to IS/profit up [1] [2]')],
          disc=[('Suggest how {f} could reduce the size of its under- or over-absorption next year.', 'Improve budgeting of overheads and activity; revise the rate during the year; control overhead spending.', 'Two suggestions [1 each] [2]')])


@spec(t24_4)
def t244_ua(r, D):
    f = firm(r)
    bo = step(r, 60000, 300000, 1000)
    bh = step(r, 5000, 30000, 500)
    oar = bo / bh
    ah = bh + step(r, -3000, 3000, 100)
    ao = bo + step(r, -15000, 15000, 500)
    ab = ah * oar
    diff = ab - ao
    if abs(diff) < 1:
        ao += 1500
        diff = ab - ao
    word = 'over-absorbed' if diff > 0 else 'under-absorbed'
    setup = f'{f} budgeted overheads of {m(bo)} and {bh:,} machine hours for the year. Actual overheads were {m(ao)} and actual machine hours were {ah:,}.'
    parts = [('Calculate the overhead absorption rate.', m2(oar), f'{m(bo)} ÷ {bh:,} = {m2(oar)} [1]'),
             ('Calculate the overheads absorbed and the under- or over-absorption.', f'Absorbed {m(ab)}; {word} {m(abs(diff))}', f'{ah:,} × {m2(oar)} = {m(ab)} [1]; {m(ab)} − {m(ao)} = {m(diff)} [1]; {word} [1] [3]'),
             ('State the effect on profit of adjusting for this.', f'Profit {"increases" if diff > 0 else "decreases"} by {m(abs(diff))}.', 'Direction and amount [1]')]
    wrong = bh * oar - ao
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'What is the amount {word}?', *num_opts(m, abs(diff), [abs(bo - ao), abs(ah - bh) * oar, abs(diff) * 2]), f'{m(ab)} − {m(ao)}'),
            'err': (f'calculated the under/over-absorption as {m(abs(bo - ao))}', 'budgeted overheads were compared with actual overheads; absorbed overheads (actual hours × OAR) must be compared with actual overheads', f'{word} {m(abs(diff))}', f'{ah:,} × {m2(oar)} − {m(ao)}', 'under/over-absorption') if abs(abs(bo - ao) - abs(diff)) > 1 else None}


t24_5 = A(24, 'Pricing using absorption cost-plus', ['pricing using absorption cost-plus', 'cost-plus pricing', 'absorption cost-plus'],
          mcqs=[('Cost-plus pricing sets the selling price by', 'adding a percentage mark-up to the full cost per unit', ['matching competitors\' prices', 'charging what customers will pay', 'deducting a margin from cost'], 'Full cost + mark-up'),
                ('Full cost per unit $40; mark-up 25%. The selling price is', '$50', ['$53.33', '$65', '$30'], '40 × 1.25'),
                ('Full cost $60; required margin 20% on selling price. The price is', '$75', ['$72', '$80', '$48'], '60 ÷ 0.8'),
                ('A limitation of cost-plus pricing is that it', 'ignores demand and competitors\' prices', ['always gives a loss', 'is hard to calculate', 'ignores costs'], 'Market factors'),
                ('An advantage of absorption cost-plus pricing is that', 'all costs are covered if budgeted output is sold', ['it maximises sales', 'it ignores fixed costs', 'it reacts to competitors'], 'Full cost recovery')],
          exps=[('Explain one advantage and one disadvantage of absorption cost-plus pricing.', 'Advantage: simple and ensures all costs are covered at budgeted volume. Disadvantage: ignores demand/competition; if volume falls, fixed cost per unit rises and price may become uncompetitive.', 'Advantage [1]; disadvantage [1] [2]'),
                ('Explain why the absorbed cost per unit depends on the budgeted level of output.', 'Fixed overheads are spread over budgeted units, so lower budgeted output means a higher overhead per unit.', 'Fixed overheads spread [1]; inverse relation [1] [2]')],
          disc=[('Evaluate whether {f} should use cost-plus pricing for a new product in a competitive market.', 'It covers costs but may set a price above competitors; market-based or penetration pricing may be better; consider the brand.', 'Cost-plus point [1]; market factors [1]; judgement [1] [3]')])


@spec(t24_5)
def t245_cp(r, D):
    f = firm(r)
    dm, dl = step(r, 500, 4000, 25) / 100, step(r, 400, 3000, 25) / 100
    h = r.choice([0.5, 1, 1.5, 2, 3])
    oar = step(r, 400, 2000, 25) / 100
    oh = h * oar
    fc = dm + dl + oh
    mu = r.choice([20, 25, 30, 40, 50])
    pr = fc * (100 + mu) / 100
    setup = f'{f} makes a product with direct materials {m2(dm)} and direct labour {m2(dl)} per unit. Each unit takes {h:g} machine hours and the overhead absorption rate is {m2(oar)} per machine hour. The business adds a mark-up of {mu}% to full cost.'
    parts = [('Calculate the full (absorption) cost per unit.', m2(fc), f'{m2(dm)} + {m2(dl)} + {h:g} × {m2(oar)} = {m2(fc)} [2]'),
             ('Calculate the selling price.', m2(pr), f'{m2(fc)} × {100 + mu}% = {m2(pr)} [1]')]
    if D >= 3:
        mg = r.choice([20, 25, 30])
        parts.append((f'Calculate the selling price if instead a margin of {mg}% on selling price were required.', m2(fc / (1 - mg / 100)), f'{m2(fc)} ÷ {1 - mg / 100:.2f} = {m2(fc / (1 - mg / 100))} [1]'))
    wrong = (dm + dl) * (100 + mu) / 100
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the selling price?', *num_opts(m2, pr, [wrong, fc, fc / (1 - mu / 100)]), f'{m2(fc)} × {100 + mu}%'),
            'err': (f'set the selling price at {m2(wrong)}', 'overheads were not included; absorption cost-plus adds the mark-up to full cost including absorbed overheads', m2(pr), f'{m2(fc)} × {100 + mu}%', 'selling price')}


CHAPTERS[24] = [t24_1, t24_2, t24_3, t24_4, t24_5]


# ===================================================================== 25 Marginal costing and break-even
def _cvp(r):
    sp = step(r, 1000, 9000, 50) / 100
    vc = round(sp * r.choice([0.4, 0.5, 0.55, 0.6, 0.65, 0.7]), 2)
    cpu = round(sp - vc, 2)
    fc = round(cpu * step(r, 1000, 20000, 100))
    cap = int(fc / cpu * r.choice([1.3, 1.5, 1.8, 2.0]))
    cap = cap // 100 * 100
    return sp, vc, cpu, fc, cap


t25_1 = A(25, 'Contribution and contribution per unit', ['contribution and contribution per unit', 'contribution per unit', 'contribution'],
          mcqs=[('Contribution per unit is', 'selling price per unit − variable cost per unit', ['selling price − total cost per unit', 'fixed costs ÷ units', 'revenue − fixed costs'], 'Contributes to fixed costs and profit'),
                ('Selling price $25; variable cost $15; 4,000 units sold; fixed costs $30,000. Profit is', '$10,000', ['$40,000', '$70,000', '$30,000'], '4,000 × 10 − 30,000'),
                ('In marginal costing, fixed costs are', 'treated as period costs and charged in full against contribution', ['absorbed into each unit', 'ignored completely', 'included in closing inventory'], 'Not product costs'),
                ('The contribution to sales (C/S) ratio is', 'contribution ÷ revenue', ['profit ÷ revenue', 'fixed costs ÷ revenue', 'variable cost ÷ revenue'], 'Also called P/V ratio'),
                ('If variable cost per unit rises and price is unchanged, contribution per unit', 'falls', ['rises', 'stays the same', 'becomes fixed'], 'SP − VC')],
          exps=[('Explain what is meant by contribution.', 'Contribution is selling price less variable costs; it is the amount each unit contributes first to covering fixed costs and then to profit.', 'SP − VC [1]; covers fixed costs then profit [1] [2]'),
                ('Explain why fixed costs are not included in the contribution per unit.', 'They do not change with output in the short run, so they are not affected by producing one more unit; spreading them per unit would give misleading decisions.', 'Do not vary with output [1]; misleading per unit [1] [2]')],
          disc=[('Discuss whether {f} should raise its selling price to increase contribution per unit.', 'A higher price raises contribution per unit but may cut sales volume; total contribution depends on price elasticity.', 'Per-unit gain [1]; volume risk [1]; judgement [1] [3]')])


@spec(t25_1)
def t251_cont(r, D):
    f = firm(r)
    sp, vc, cpu, fc, cap = _cvp(r)
    u = int(cap * r.choice([0.6, 0.7, 0.8, 0.9]))
    tc = u * cpu
    prof = tc - fc
    setup = f'{f} sells a product for {m2(sp)} per unit. Variable costs are {m2(vc)} per unit and fixed costs are {m(fc)} a year. It expects to sell {u:,} units.'
    parts = [('Calculate the contribution per unit and the total contribution.', f'{m2(cpu)} per unit; total {m(tc)}', f'{m2(sp)} − {m2(vc)} = {m2(cpu)} [1]; × {u:,} = {m(tc)} [1] [2]'),
             ('Calculate the expected profit or loss.', f'{"Profit" if prof >= 0 else "Loss"} {m(abs(prof))}', f'{m(tc)} − {m(fc)} = {m(prof)} [1]'),
             ('Calculate the contribution to sales ratio.', pc(cpu / sp * 100), f'{m2(cpu)} ÷ {m2(sp)} × 100 = {pc(cpu / sp * 100)} [1]')]
    wrong = u * sp - fc
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the expected profit?', *num_opts(m, prof, [wrong, tc, u * (sp - vc - fc / cap)]), f'{u:,} × {m2(cpu)} − {m(fc)}'),
            'err': (f'calculated profit as {m(wrong)}', 'variable costs were not deducted; profit = total contribution − fixed costs', m(prof), f'{u:,} × {m2(cpu)} − {m(fc)}', 'profit')}


t25_2 = A(25, 'Break-even point, margin of safety and target profit', ['break-even point, margin of safety and target profit', 'break-even point', 'margin of safety', 'target profit'],
          mcqs=[('Break-even point in units is', 'fixed costs ÷ contribution per unit', ['fixed costs ÷ selling price', 'total costs ÷ contribution', 'contribution ÷ fixed costs'], 'Contribution covers fixed costs'),
                ('Fixed costs $48,000; contribution per unit $12. Break-even output is', '4,000 units', ['576,000 units', '400 units', '3,600 units'], '48,000 ÷ 12'),
                ('The margin of safety is', 'budgeted sales minus break-even sales', ['break-even sales minus fixed costs', 'contribution minus fixed costs', 'actual profit'], 'Cushion before loss'),
                ('Units needed for a target profit are', '(fixed costs + target profit) ÷ contribution per unit', ['target profit ÷ contribution per unit', 'fixed costs ÷ (contribution + profit)', '(fixed costs − target profit) ÷ contribution'], 'Extra contribution required'),
                ('If fixed costs rise, the break-even point will', 'rise', ['fall', 'stay the same', 'become zero'], 'More contribution needed')],
          exps=[('Explain why the margin of safety is useful to managers.', 'It shows how far sales could fall before a loss is made, indicating the level of risk.', 'Fall in sales before loss [1]; risk [1] [2]'),
                ('Explain the effect on the break-even point of an increase in the selling price.', 'Contribution per unit rises, so fewer units are needed to cover fixed costs; break-even falls.', 'Contribution rises [1]; BEP falls [1] [2]')],
          disc=[('Advise {f} whether its margin of safety is sufficient.', 'Compare the margin of safety (%) with the volatility of demand; a small margin is risky in uncertain markets; options include cutting fixed costs or raising contribution.', 'Interpret margin [1]; risk/market [1]; advice [1] [3]')])


@spec(t25_2)
def t252_be(r, D):
    f = firm(r)
    sp, vc, cpu, fc, cap = _cvp(r)
    bu = fc / cpu
    bud = int(cap * r.choice([0.8, 0.9, 1.0]))
    mos = bud - bu
    tp = step(r, 5000, 40000, 1000)
    tu = (fc + tp) / cpu
    setup = f'{f} makes a product that sells for {m2(sp)}, with variable costs of {m2(vc)} per unit. Fixed costs are {m(fc)} a year and budgeted sales are {bud:,} units.'
    parts = [('Calculate the break-even point in units and in revenue.', f'{bu:,.0f} units; {m(bu * sp)}', f'{m(fc)} ÷ {m2(cpu)} = {bu:,.0f} units [1]; × {m2(sp)} = {m(bu * sp)} [1] [2]'),
             ('Calculate the margin of safety in units and as a percentage of budgeted sales.', f'{mos:,.0f} units; {pc(mos / bud * 100)}', f'{bud:,} − {bu:,.0f} = {mos:,.0f} [1]; ÷ {bud:,} = {pc(mos / bud * 100)} [1] [2]')]
    if D >= 3:
        parts.append((f'Calculate the number of units needed to earn a profit of {m(tp)}.', f'{-(-tu // 1):,.0f} units', f'({m(fc)} + {m(tp)}) ÷ {m2(cpu)} = {tu:,.1f} → {-(-tu // 1):,.0f} units [2]'))
    wrong = fc / sp
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the break-even point in units?', *num_opts(lambda x: f'{x:,.0f} units', bu, [wrong, fc / vc, bu * 1.5]), f'{m(fc)} ÷ {m2(cpu)}'),
            'err': (f'calculated break-even as {wrong:,.0f} units', 'fixed costs were divided by the selling price instead of the contribution per unit', f'{bu:,.0f} units', f'{m(fc)} ÷ ({m2(sp)} − {m2(vc)})', 'break-even point')}


t25_3 = A(25, 'Break-even charts and limitations of CVP analysis', ['break-even charts and limitations of cvp analysis', 'break-even charts', 'limitations of cvp'],
          mcqs=[('On a break-even chart, the break-even point is where', 'the total revenue line crosses the total cost line', ['the fixed cost line crosses the revenue line', 'total costs are at their lowest', 'the variable cost line starts'], 'Revenue = total cost'),
                ('The fixed cost line on a break-even chart is', 'horizontal', ['upward sloping from the origin', 'downward sloping', 'vertical'], 'Constant at all outputs'),
                ('The total cost line starts at', 'the level of fixed costs on the vertical axis', ['the origin', 'the break-even point', 'the maximum capacity'], 'TC = FC + VC'),
                ('Which is a limitation of break-even analysis?', 'It assumes all units produced are sold', ['It is easy to understand', 'It shows the margin of safety', 'It shows profit at different outputs'], 'Simplifying assumptions'),
                ('A steeper total revenue line on a break-even chart indicates', 'a higher selling price', ['higher fixed costs', 'lower contribution', 'a lower selling price'], 'Slope = price')],
          exps=[('State three assumptions of break-even analysis.', 'Selling price and variable cost per unit are constant; fixed costs are fixed; all output is sold; single product or constant sales mix.', 'Any three [1 each] [3]'),
                ('Explain how a break-even chart can help a business plan.', 'It shows visually the profit or loss at any output, the break-even point and margin of safety, and the effect of changes in price or costs.', 'Visual profit/loss at outputs [1]; what-if changes [1] [2]')],
          disc=[('Discuss how useful break-even analysis is to {f} when launching a new product.', 'It gives a quick target and shows risk, but estimates of price, costs and demand are uncertain and the assumptions may not hold.', 'Usefulness [1]; limitations [1]; judgement [1] [3]')])


@spec(t25_3)
def t253_chart(r, D):
    f = firm(r)
    sp, vc, cpu, fc, cap = _cvp(r)
    bu = fc / cpu
    setup = f'A break-even chart for {f} shows a horizontal fixed cost line at {m(fc)}, a total cost line rising from {m(fc)} to {m(fc + vc * cap)} at maximum capacity of {cap:,} units, and a total revenue line from the origin to {m(sp * cap)} at {cap:,} units.'
    parts = [('Calculate the selling price and variable cost per unit shown by the chart.', f'Price {m2(sp)}; variable cost {m2(vc)}', f'{m(sp * cap)} ÷ {cap:,} = {m2(sp)} [1]; ({m(fc + vc * cap)} − {m(fc)}) ÷ {cap:,} = {m2(vc)} [1] [2]'),
             ('Calculate the break-even output and the profit at maximum capacity.', f'{bu:,.0f} units; profit {m(cap * cpu - fc)}', f'{m(fc)} ÷ {m2(cpu)} = {bu:,.0f} [1]; {m(sp * cap)} − {m(fc + vc * cap)} = {m(cap * cpu - fc)} [1] [2]'),
             ('State two limitations of the chart.', 'Assumes constant price and variable cost per unit (no bulk discounts); assumes all output is sold; fixed costs may step up; single product.', 'Two limitations [1 each] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the break-even output?', *num_opts(lambda x: f'{x:,.0f} units', bu, [fc / sp, cap - bu, bu * 2]), f'{m(fc)} ÷ {m2(cpu)}'),
            'err': (f'read the profit at maximum capacity as {m(sp * cap - fc)}', 'variable costs were ignored; profit is the gap between total revenue and total cost', m(cap * cpu - fc), f'{m(sp * cap)} − {m(fc + vc * cap)}', 'profit at capacity')}


CHAPTERS[25] = [t25_1, t25_2, t25_3]


# ===================================================================== 26 Decision making using marginal costing
t26_1 = A(26, 'Special orders and pricing decisions', ['special orders and pricing decisions', 'special orders', 'pricing decisions'],
          mcqs=[('A special order should normally be accepted, on financial grounds, if', 'the price is above the variable (marginal) cost and there is spare capacity', ['the price is above full cost only', 'the price covers fixed costs', 'it is from a new customer'], 'Positive contribution'),
                ('Spare capacity; variable cost $18; special order price $22 for 1,000 units. Profit increases by', '$4,000', ['$22,000', '$18,000', '$40,000'], '1,000 × (22 − 18)'),
                ('Fixed costs are usually ignored in a special order decision because', 'they will be incurred whether or not the order is accepted', ['they are always zero', 'they are paid by the customer', 'they are variable'], 'Not relevant'),
                ('A risk of accepting a special order at a low price is that', 'regular customers may demand the same low price', ['contribution will be negative', 'fixed costs will fall', 'capacity will increase'], 'Market effects'),
                ('If there is no spare capacity, a special order must also cover', 'the contribution lost on normal sales displaced', ['only variable costs', 'nothing extra', 'only the fixed costs'], 'Opportunity cost')],
          exps=[('Explain why a business might accept an order at a price below its full cost.', 'If there is spare capacity, fixed costs are already covered; any price above variable cost adds contribution and increases profit.', 'Spare capacity/fixed costs unchanged [1]; positive contribution [1] [2]'),
                ('Explain two non-financial factors to consider before accepting a special order.', 'Effect on regular customers and prices; whether it leads to future orders; strain on staff and quality; customer reliability.', 'Two factors [1 each] [2]')],
          disc=[('Recommend whether {f} should accept the order.', 'Accept if contribution is positive and capacity allows, unless it damages regular prices or there are better uses of capacity.', 'Financial result [1]; non-financial factor [1]; recommendation [1] [3]')])


@spec(t26_1)
def t261_so(r, D):
    f = firm(r)
    sp, vc, cpu, fc, cap = _cvp(r)
    norm = int(cap * r.choice([0.6, 0.7, 0.75, 0.8]))
    q = step(r, 500, max(600, int(cap * 0.3)), 100)
    price = round(vc + cpu * r.choice([-0.2, 0.2, 0.4, 0.6]), 2)
    extra = q * (price - vc)
    if D >= 4:
        q = cap - norm + step(r, 200, 1500, 100)
    disp = max(0, norm + q - cap)
    lost = disp * cpu
    net = q * (price - vc) - lost
    fcu = fc / norm
    setup = f'{f} normally sells {norm:,} units a year at {m2(sp)}; variable cost is {m2(vc)} per unit and fixed costs are {m(fc)} (full cost {m2(vc + fcu)} per unit). Maximum capacity is {cap:,} units. A new customer offers to buy {q:,} units at {m2(price)} each; fixed costs will not change.'
    parts = [('Calculate the change in profit if the order is accepted.', f'{"Increase" if net >= 0 else "Decrease"} {m(abs(net))}', f'Contribution {q:,} × ({m2(price)} − {m2(vc)}) = {m(q * (price - vc))} [1]' + (f'; lost contribution {disp:,} × {m2(cpu)} = {m(lost)} [1]' if disp else '') + f'; net {m(net)} [1] [{3 if disp else 2}]'),
             ('Explain why the full cost per unit is not relevant to the decision.', 'Fixed costs are incurred anyway; only extra revenue and extra (variable) costs matter.', 'Fixed costs unchanged [1]; relevant costs only [1] [2]'),
             ('State one non-financial factor the business should consider.', 'Reaction of regular customers to the lower price; possibility of future orders; quality and staff workload.', 'Valid factor [1]')]
    wrong = q * (price - vc - fcu)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('By how much would profit change if the order is accepted?', *num_opts(m, net, [wrong, q * price, extra + lost if disp else -extra]), f'{q:,} × ({m2(price)} − {m2(vc)})' + (f' − {m(lost)}' if disp else '')),
            'err': (f'rejected the order because it would reduce profit by {m(abs(wrong))}', 'fixed overheads per unit were deducted; fixed costs do not change, so only contribution matters', f'profit {"increases" if net >= 0 else "decreases"} by {m(abs(net))}', f'{q:,} × ({m2(price)} − {m2(vc)})', 'effect on profit') if wrong < 0 < net else None}


t26_2 = A(26, 'Make or buy decisions', ['make or buy decisions', 'make or buy'],
          mcqs=[('In a make-or-buy decision, the cost of making should include', 'only the costs that would be avoided by buying', ['all absorbed fixed overheads', 'the selling price of the product', 'past costs already incurred'], 'Relevant costs'),
                ('Variable cost to make a component $14; outside price $16; fixed costs unavoidable. The business should', 'make the component, saving $2 per unit', ['buy the component, saving $2', 'buy because fixed costs are covered', 'stop making the product'], 'Compare marginal cost with price'),
                ('Which factor favours buying in a component?', 'Spare factory capacity can be used for a more profitable product', ['The supplier is unreliable', 'Quality control is easier when making', 'The outside price is higher than variable cost'], 'Opportunity cost'),
                ('Avoidable fixed costs are', 'fixed costs that would cease if production stopped', ['fixed costs that continue whatever happens', 'variable costs', 'sunk costs'], 'Relevant to the decision'),
                ('A sunk cost is', 'a cost already incurred that cannot be recovered', ['a future variable cost', 'an avoidable fixed cost', 'the price of buying in'], 'Irrelevant to decisions')],
          exps=[('Explain why unavoidable fixed costs are ignored in a make-or-buy decision.', 'They will be paid whether the item is made or bought, so they do not change the difference between the two options.', 'Incurred either way [1]; not relevant [1] [2]'),
                ('Explain two non-financial factors in a make-or-buy decision.', 'Reliability and quality of the supplier; loss of control/know-how; effect on employees (redundancies); confidentiality of designs.', 'Two factors [1 each] [2]')],
          disc=[('Advise {f} whether to make or buy the component.', 'Compare relevant cost of making with the purchase price, then weigh supplier reliability, quality and use of freed capacity.', 'Financial comparison [1]; non-financial [1]; advice [1] [3]')])


@spec(t26_2)
def t262_mob(r, D):
    f = firm(r)
    q = step(r, 2000, 20000, 500)
    dm, dl, vo = step(r, 200, 1500, 5) / 100, step(r, 200, 1500, 5) / 100, step(r, 50, 600, 5) / 100
    fo = step(r, 100, 800, 5) / 100
    vcu = dm + dl + vo
    buy = round(vcu + r.choice([-1.5, -0.8, 0.6, 1.2, 2.0]), 2)
    av = step(r, 2000, 15000, 500) if D >= 3 else 0
    make = q * vcu + av
    bc = q * buy
    diff = bc - make
    setup = (f'{f} makes {q:,} units a year of a component. Cost per unit: direct materials {m2(dm)}, direct labour {m2(dl)}, variable overheads {m2(vo)}, fixed overheads absorbed {m2(fo)}. An outside supplier will provide the component for {m2(buy)} per unit.' +
             (f' If the component is bought in, a supervisor costing {m(av)} a year would no longer be needed; other fixed costs would continue.' if av else ' Fixed costs would not change if the component were bought in.'))
    parts = [('Calculate the relevant cost of making and the cost of buying the annual quantity.', f'Make {m(make)}; buy {m(bc)}', f'Variable {m2(vcu)} × {q:,} = {m(q * vcu)}' + (f' + avoidable {m(av)}' if av else '') + f' = {m(make)} [2]; buy {q:,} × {m2(buy)} = {m(bc)} [1] [3]'),
             ('State, on financial grounds, whether the component should be made or bought, and the annual saving.', f'{"Make" if diff > 0 else "Buy"} – saving {m(abs(diff))} a year.', 'Correct decision [1]; saving [1] [2]')]
    wrong = bc - q * (vcu + fo)
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the annual saving from the better option?', *num_opts(m, abs(diff), [abs(wrong), q * fo, abs(diff) + av if av else abs(diff) * 2]), f'|{m(bc)} − {m(make)}|'),
            'err': (f'compared the purchase price with full cost of {m2(vcu + fo)} per unit and decided to {"buy" if wrong < 0 else "make"}', 'absorbed fixed overheads that will continue anyway were included; only avoidable costs are relevant', f'{"make" if diff > 0 else "buy"} (saving {m(abs(diff))})', f'{m(bc)} − {m(make)}', 'decision') if (wrong < 0) != (diff < 0) else None}


t26_3 = A(26, 'Limiting factor analysis: ranking by contribution per unit of scarce resource', ['limiting factor analysis: ranking by contribution per unit of scarce resource', 'limiting factor', 'scarce resource'],
          mcqs=[('When a resource is scarce, products should be ranked by', 'contribution per unit of the scarce resource', ['contribution per unit', 'selling price', 'profit per unit after fixed costs'], 'Maximise contribution from the constraint'),
                ('Product X: contribution $12, uses 3 kg. Product Y: contribution $10, uses 2 kg. Material is limited. The ranking is', 'Y first ($5 per kg), then X ($4 per kg)', ['X first, then Y', 'Both equal', 'Y only'], 'Per kg'),
                ('A limiting factor is', 'a resource in short supply that restricts output', ['a fixed cost', 'the selling price', 'any variable cost'], 'Constraint'),
                ('Which could be a limiting factor?', 'Skilled labour hours', ['Rent', 'Depreciation', 'Dividends'], 'Scarce input'),
                ('After ranking, resources are allocated', 'to the highest-ranked product up to its maximum demand, then to the next', ['equally to all products', 'to the product with the highest price', 'to the product with lowest cost'], 'Fill demand in order')],
          exps=[('Explain why contribution per unit is not the correct basis for ranking when a resource is scarce.', 'A product with high contribution per unit may use a lot of the scarce resource; what matters is the contribution earned from each unit of the scarce resource.', 'Uses of resource differ [1]; per unit of resource [1] [2]'),
                ('Explain two ways a business could overcome a shortage of materials.', 'Find alternative suppliers; use substitute materials; buy in finished components; redesign products to use less.', 'Two ways [1 each] [2]')],
          disc=[('Discuss whether {f} should stop making the lowest-ranked product.', 'It earns least per unit of the scarce resource, but may support the range, keep customers and contribute to fixed costs; the constraint may be temporary.', 'Financial point [1]; non-financial [1]; judgement [1] [3]')])


@spec(t26_3, D=(2, 3, 4, 5))
def t263_lf(r, D):
    f = firm(r)
    names = r.choice(PRODUCTS3)
    k = 2 if D <= 3 else 3
    prods = []
    for nm_ in names[:k]:
        c = step(r, 400, 3000, 50) / 100
        kg = r.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
        dem = step(r, 1000, 6000, 100)
        prods.append([nm_, c, kg, dem, c / kg])
    if len({round(p[4], 4) for p in prods}) < k:
        prods[0][1] += 1.0
        prods[0][4] = prods[0][1] / prods[0][2]
    need = sum(p[2] * p[3] for p in prods)
    avail = int(need * r.choice([0.55, 0.65, 0.75])) // 100 * 100
    rank = sorted(prods, key=lambda p: -p[4])
    left, plan, tot = avail, [], 0
    for p in rank:
        u = min(p[3], int(left // p[2]))
        plan.append((p[0], u))
        tot += u * p[1]
        left -= u * p[2]
    setup = f'{f} makes {", ".join(p[0] for p in prods[:-1])} and {prods[-1][0]}. Data per unit: ' + '; '.join(f'{p[0]} – contribution {m2(p[1])}, material {p[2]:g} kg, maximum demand {p[3]:,} units' for p in prods) + f'. Only {avail:,} kg of material is available next month.'
    parts = [('Calculate the contribution per kg for each product and rank the products.', '; '.join(f'{p[0]} {m2(p[4])}' for p in prods) + '; ranking ' + ', '.join(p[0] for p in rank),
              '; '.join(f'{p[0]} {m2(p[1])} ÷ {p[2]:g} = {m2(p[4])}' for p in prods) + f' [{k}]; ranking [1] [{k + 1}]'),
             ('Calculate the production plan that maximises contribution and the total contribution.', '; '.join(f'{n} {u:,} units' for n, u in plan) + f'; contribution {m(tot)}', 'Allocate in rank order up to demand [1]; ' + '; '.join(f'{n} {u:,}' for n, u in plan) + f' [1]; total {m(tot)} [1] [3]')]
    wr = sorted(prods, key=lambda p: -p[1])
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('Which product should be made first?', rank[0][0], [p[0] for p in prods if p[0] != rank[0][0]] + ['All products equally', 'The product with the highest selling price'], f'Highest contribution per kg: {rank[0][0]} {m2(rank[0][4])}'),
            'err': (f'ranked the products by contribution per unit, putting {wr[0][0]} first', 'when material is scarce the ranking must use contribution per kg of material', 'ranking ' + ', '.join(p[0] for p in rank), '; '.join(f'{p[0]} {m2(p[4])}/kg' for p in prods), 'ranking') if wr[0][0] != rank[0][0] else None}


PRODUCTS3 = [('Alpha', 'Beta', 'Gamma'), ('Standard', 'Deluxe', 'Premium'), ('Kappa', 'Sigma', 'Omega'), ('Lite', 'Pro', 'Max'), ('Orion', 'Vega', 'Lyra')]

t26_4 = A(26, 'Non-financial factors in decision making', ['non-financial factors in decision making', 'non-financial factors'],
          mcqs=[('Which is a non-financial factor in deciding whether to buy in a component?', 'The reliability of the supplier', ['The variable cost per unit', 'The purchase price', 'The contribution per unit'], 'Qualitative'),
                ('Closing a department may lead to', 'lower staff morale and loss of skills', ['higher contribution always', 'lower fixed costs only', 'no effect on employees'], 'Human factors'),
                ('A special order at a low price may', 'damage relationships with existing customers who pay full price', ['always increase sales to existing customers', 'reduce variable costs', 'remove the need for capacity'], 'Market effects'),
                ('Which stakeholder concern is non-financial?', 'The environmental impact of a new factory', ['The payback period', 'The break-even point', 'The margin of safety'], 'Qualitative factor'),
                ('Why are non-financial factors important in decisions?', 'They can affect long-term success even if not shown in the figures', ['They replace all financial analysis', 'They are required by IAS 2', 'They always increase profit'], 'Broader view')],
          exps=[('Explain why a decision that increases short-term profit might not be in the long-term interest of a business.', 'It may harm reputation, quality, staff morale or customer loyalty, which reduce future sales and profits.', 'Long-term effect named [1]; consequence [1] [2]'),
                ('Explain how the reliability of a supplier affects a make-or-buy decision.', 'An unreliable supplier may deliver late or poor-quality parts, stopping production and harming customers, so savings could be lost.', 'Late/poor supply [1]; effect on production/customers [1] [2]')],
          disc=[('Evaluate whether {f} should base its decision only on the financial figures.', 'Figures show the immediate gain, but staff, customers, quality and reputation also matter; a balanced judgement is required.', 'Financial point [1]; non-financial [1]; judgement [1] [3]')])

NFF = [('buy components from an overseas supplier instead of making them', ['supplier reliability and delivery times', 'quality control', 'redundancies and staff morale', 'exchange-rate risk']),
       ('close its loss-making repair department', ['loss of customers who use the repairs service', 'redundancies and morale', 'effect on reputation']),
       ('accept a large one-off order at a low price', ['reaction of regular customers', 'possibility of repeat orders', 'pressure on staff and quality']),
       ('replace skilled workers with automated machines', ['loss of skills and flexibility', 'redundancy costs and morale', 'quality and reliability of machines']),
       ('move production to a cheaper location', ['effect on local community and reputation', 'staff willingness to relocate', 'access to suppliers and customers'])]


@spec(t26_4, typ='short')
def t264_nff(r, D):
    f = firm(r)
    d, fs = r.choice(NFF)
    gain = step(r, 5000, 60000, 1000)
    setup = f'Financial analysis shows that {f} could increase annual profit by {m(gain)} if it decided to {d}.'
    parts = [('Identify two non-financial factors the business should consider.', f'{cap1(fs[0])}; {fs[1]}.', f'{fs[0]} [1]; {fs[1]} [1] [2]'),
             ('Explain how one of these factors could affect the long-term success of the business.', f'{cap1(fs[0])} could affect customers, quality or staff, reducing future revenue and outweighing the {m(gain)} gain.', 'Factor developed [1]; long-term consequence [1] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': (f'Which is a non-financial factor in the decision to {d}?', cap1(fs[0]), ['The increase in annual profit', 'The contribution per unit', 'The break-even point'], f'{fs[0]} is qualitative'),
            'err': None}


CHAPTERS[26] = [t26_1, t26_2, t26_3, t26_4]


# ===================================================================== 27 Comparing absorption and marginal costing
def _am(r, D):
    sp = step(r, 2000, 8000, 50) / 100
    vc = round(sp * r.choice([0.4, 0.5, 0.6]), 2)
    prod = step(r, 5000, 20000, 500)
    fpo = step(r, 30000, 150000, prod // 100 if prod % 100 == 0 else 500)
    fpu = fpo / prod
    oi = step(r, 0, 2000, 100) if D >= 3 else 0
    sold = prod + oi - step(r, 200, min(3000, prod // 3), 100)
    ci = oi + prod - sold
    if ci < 0:
        sold = prod + oi - 500
        ci = 500
    fna = step(r, 10000, 50000, 1000)
    mprof = sold * (sp - vc) - fpo - fna
    aprof = mprof + (ci - oi) * fpu
    return sp, vc, prod, fpo, fpu, oi, sold, ci, fna, mprof, aprof


t27_1 = A(27, 'Inventory valuation under absorption and marginal costing', ['inventory valuation under absorption and marginal costing', 'absorption and marginal costing inventory'],
          mcqs=[('Under marginal costing, closing inventory is valued at', 'variable production cost per unit', ['full production cost per unit', 'selling price', 'total cost including selling costs'], 'Fixed costs are period costs'),
                ('Under absorption costing, closing inventory includes', 'a share of fixed production overheads', ['no fixed costs', 'selling and administration costs', 'only direct materials'], 'Full production cost'),
                ('Variable production cost $12; fixed production overhead per unit $5; 800 units in closing inventory. Absorption costing value is', '$13,600', ['$9,600', '$4,000', '$17,600'], '800 × 17'),
                ('Which costing method values inventory in line with IAS 2 for published accounts?', 'Absorption costing', ['Marginal costing', 'Both equally', 'Neither'], 'IAS 2 requires production overheads'),
                ('Fixed production overheads are treated under marginal costing as', 'period costs written off in full', ['product costs carried in inventory', 'variable costs', 'capital expenditure'], 'Charged in the period')],
          exps=[('Explain why closing inventory has a higher value under absorption costing.', 'It includes a share of fixed production overheads in each unit, whereas marginal costing includes only variable production costs.', 'Absorption includes FPO [1]; marginal only variable [1] [2]'),
                ('Explain why absorption costing is required for published financial statements.', 'IAS 2 requires inventory cost to include all costs of bringing it to its present condition, including production overheads, matching costs to revenue.', 'IAS 2 [1]; matching/full cost [1] [2]')],
          disc=[('Discuss which method of inventory valuation gives the more useful information to the managers of {f}.', 'Marginal costing helps decisions (contribution) and avoids profit changing with inventory levels; absorption matches IAS 2 and full cost; managers may use both.', 'Marginal benefit [1]; absorption benefit [1]; judgement [1] [3]')])


@spec(t27_1)
def t271_val(r, D):
    f = firm(r)
    sp, vc, prod, fpo, fpu, oi, sold, ci, fna, mprof, aprof = _am(r, D)
    setup = f'{f} produced {prod:,} units and sold {sold:,} units this year' + (f' (opening inventory {oi:,} units)' if oi else ' (no opening inventory)') + f'. Variable production cost is {m2(vc)} per unit and fixed production overheads are {m(fpo)}, absorbed on actual production.'
    parts = [('Calculate the fixed production overhead per unit.', m2(fpu), f'{m(fpo)} ÷ {prod:,} = {m2(fpu)} [1]'),
             ('Calculate the value of closing inventory under marginal costing and under absorption costing.', f'Marginal {m(ci * vc)}; absorption {m(ci * (vc + fpu))}', f'Closing {ci:,} units [1]; × {m2(vc)} = {m(ci * vc)} [1]; × {m2(vc + fpu)} = {m(ci * (vc + fpu))} [1] [3]'),
             ('Explain which value would be used in the published financial statements.', 'Absorption cost, because IAS 2 requires production overheads to be included in inventory.', 'Absorption [1]; IAS 2 [1] [2]')]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the value of closing inventory under absorption costing?', *num_opts(m, ci * (vc + fpu), [ci * vc, ci * fpu, ci * sp]), f'{ci:,} × {m2(vc + fpu)}'),
            'err': (f'valued the closing inventory under absorption costing at {m(ci * vc)}', 'only variable cost was used; absorption costing adds the fixed production overhead per unit', m(ci * (vc + fpu)), f'{ci:,} × ({m2(vc)} + {m2(fpu)})', 'absorption value')}


t27_2 = A(27, 'Reconciling profits under the two methods', ['reconciling profits under the two methods', 'reconciling profits', 'profit reconciliation'],
          mcqs=[('When inventory levels rise during a period, absorption costing profit is', 'higher than marginal costing profit', ['lower than marginal costing profit', 'the same as marginal costing profit', 'always a loss'], 'Fixed overheads carried forward in inventory'),
                ('Inventory increases by 400 units; fixed overhead per unit $6. The profit difference is', '$2,400', ['$400', '$6', '$4,800'], '400 × 6'),
                ('When production equals sales, the two methods give', 'the same profit', ['different profits', 'a higher marginal profit', 'a higher absorption profit'], 'No change in inventory'),
                ('If inventory falls, absorption costing profit is', 'lower than marginal costing profit', ['higher than marginal costing profit', 'equal', 'zero'], 'Fixed overheads from last year released'),
                ('The profit difference between the methods is explained by', 'fixed production overheads in the change in inventory', ['variable costs', 'selling costs', 'sales revenue'], 'Reconciliation')],
          exps=[('Explain why absorption costing profit is higher than marginal costing profit when inventory increases.', 'Part of this period\'s fixed production overheads is carried forward in closing inventory under absorption costing, so less is charged against this period\'s profit.', 'FPO carried forward in inventory [1]; less charged this period [1] [2]'),
                ('Explain why managers might be tempted to over-produce under absorption costing.', 'Building up inventory defers fixed overheads to the next period and increases reported profit, even if the goods cannot be sold.', 'Defers overheads [1]; inflates profit [1] [2]')],
          disc=[('Discuss which profit figure {f}\'s managers should use to judge performance.', 'Marginal profit moves with sales and cannot be boosted by over-production; absorption profit is required externally; using marginal internally avoids manipulation.', 'Marginal point [1]; absorption point [1]; judgement [1] [3]')])


@spec(t27_2)
def t272_rec(r, D):
    f = firm(r)
    sp, vc, prod, fpo, fpu, oi, sold, ci, fna, mprof, aprof = _am(r, D)
    setup = (f'{f} sells its product at {m2(sp)}. Variable production cost is {m2(vc)} per unit; fixed production overheads are {m(fpo)} and fixed non-production overheads {m(fna)}. This year {prod:,} units were produced and {sold:,} sold' +
             (f'; opening inventory was {oi:,} units (valued at the same costs)' if oi else '; there was no opening inventory') + '. Fixed production overheads are absorbed on actual production.')
    parts = [('Calculate the profit under marginal costing.', m(mprof), f'Contribution {sold:,} × {m2(sp - vc)} = {m(sold * (sp - vc))} [1]; − {m(fpo)} − {m(fna)} = {m(mprof)} [1] [2]'),
             ('Calculate the profit under absorption costing.', m(aprof), f'Marginal profit + (closing − opening inventory) × FPO per unit [1]; {m(mprof)} + {ci - oi:,} × {m2(fpu)} = {m(aprof)} [1] [2]'),
             ('Reconcile the two profit figures.', f'Difference {m(aprof - mprof)} = change in inventory {ci - oi:,} units × {m2(fpu)}', f'Change in inventory {ci - oi:,} units [1]; × {m2(fpu)} = {m(aprof - mprof)} [1] [2]')]
    wrong = mprof - (ci - oi) * fpu
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('What is the profit under absorption costing?', *num_opts(m, aprof, [wrong, mprof, aprof + fna]), f'{m(mprof)} + {ci - oi:,} × {m2(fpu)}'),
            'err': (f'calculated absorption costing profit as {m(wrong)}', 'the inventory adjustment was made the wrong way: when inventory rises, absorption profit is higher because fixed overheads are carried forward', m(aprof), f'{m(mprof)} + {ci - oi:,} × {m2(fpu)}', 'absorption profit') if ci != oi else None}


t27_3 = A(27, 'Advantages and limitations of each costing method', ['advantages and limitations of each costing method', 'advantages and limitations of costing methods'],
          mcqs=[('An advantage of marginal costing is that', 'profit is not affected by changes in inventory levels', ['it complies with IAS 2', 'it includes all production costs in inventory', 'it ignores contribution'], 'Profit follows sales'),
                ('An advantage of absorption costing is that', 'it recognises that fixed production costs are part of the cost of making goods', ['it is better for short-term decisions', 'profit cannot be manipulated', 'it ignores overheads'], 'Full cost'),
                ('Marginal costing is particularly useful for', 'short-term decisions such as special orders', ['valuing inventory in published accounts', 'long-term pricing only', 'tax calculations'], 'Contribution approach'),
                ('A disadvantage of absorption costing is that', 'apportionment of overheads can be arbitrary', ['it ignores fixed costs', 'it is not allowed by IAS 2', 'it cannot be used for pricing'], 'Bases are approximate'),
                ('A disadvantage of marginal costing is that', 'pricing based on variable cost may fail to cover fixed costs', ['it is too complex', 'profit changes with inventory', 'it requires apportionment'], 'Under-pricing risk')],
          exps=[('Explain two advantages of marginal costing for management decision making.', 'Contribution shows the effect of changes in output; avoids arbitrary apportionment of fixed costs; profit is not distorted by inventory changes.', 'Two advantages explained [1 each] [2]'),
                ('Explain one limitation of absorption costing.', 'Profit can be increased by producing for inventory; overhead apportionment is arbitrary; full cost per unit can mislead short-term decisions.', 'Limitation [1]; explanation [1] [2]')],
          disc=[('Recommend which costing method {f} should use for setting prices of a new product.', 'Absorption cost-plus ensures all costs are covered in the long run; marginal pricing may be used for special orders; the choice depends on the market.', 'Absorption point [1]; marginal point [1]; recommendation [1] [3]')])

CMSCEN = [('wants to decide whether to accept a one-off order at a reduced price', 'marginal costing', 'only extra (variable) costs and contribution are relevant'),
          ('is preparing its published financial statements', 'absorption costing', 'IAS 2 requires production overheads in inventory'),
          ('wants to set long-term prices that cover all costs', 'absorption costing', 'full cost-plus ensures fixed costs are recovered'),
          ('finds that managers increase production at the year end to boost reported profit', 'marginal costing', 'profit then depends on sales, not on inventory build-up'),
          ('needs to rank products when labour hours are scarce', 'marginal costing', 'contribution per limiting factor is required')]


@spec(t27_3, typ='short')
def t273_adv(r, D):
    f = firm(r)
    s = r.sample(CMSCEN, 2 if D >= 3 else 1)
    setup = f'{f} ' + ' and also '.join(x[0] for x in s) + '.'
    parts = [('State which costing method is more appropriate in each case and explain why.', '; '.join(f'{x[1]} – {x[2]}' for x in s) + '.', '; '.join(f'{x[1]} [1]; {x[2]} [1]' for x in s) + f' [{2 * len(s)}]'),
             ('State one limitation of the method you chose first.', 'Marginal: may under-price, not IAS 2 compliant. Absorption: arbitrary apportionment, profit affected by inventory.', 'Valid limitation [1]')]
    o = s[0]
    return {'setup': setup, 'parts': parts, 'ctx': {'f': f},
            'mcq': ('Which costing method is more appropriate?', cap1(o[1]), ['Absorption costing' if o[1] == 'marginal costing' else 'Marginal costing', 'Neither method can be used', 'Standard costing only'], o[2]),
            'err': (f'recommended {"absorption" if o[1] == "marginal costing" else "marginal"} costing for the first situation', o[2], o[1], 'match the purpose to the method', 'method')}


CHAPTERS[27] = [t27_1, t27_2, t27_3]


# ----------------------------------------------------------------------------- marks from keys for fixed C2 items
for _ts in CHAPTERS.values():
    for _t in _ts:
        _t.templates = [x for x in _t.templates]
