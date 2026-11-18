"""CBSE class 11 accountancy families, ch05-ch07 (BRS, Trial Balance and Rectification, Depreciation)."""
from __future__ import annotations

from qbank import mcq, inr
from g11_accountancy_kit import facts, FF, ctx, amt, entry

S = 'cbse-g11-accountancy-ch'


def pa(n):
    return f"{n}'s A/c"


# ---------------- ch05 Bank Reconciliation Statement
# effect: change to go from the cash book balance (favourable = +) to the pass book balance.
# amend: True if the item must be entered in the cash book when it is amended.

def _items(r):
    a = lambda lo, hi: amt(r, lo, hi, 100)
    return [
        ('nopres', f'Cheques of {inr(x := a(3000, 40000))} issued to suppliers were not presented for payment by 31 March.', x, False),
        ('noclear', f'Cheques of {inr(x := a(3000, 40000))} deposited into the bank were not credited (cleared) by 31 March.', -x, False),
        ('charges', f'Bank charges of {inr(x := a(100, 1500))} debited in the pass book were not entered in the cash book.', -x, True),
        ('interest', f'Interest of {inr(x := a(200, 4000))} credited by the bank appears only in the pass book.', x, True),
        ('direct', f'A customer deposited {inr(x := a(2000, 30000))} directly into the firm\'s bank account; no entry was made in the cash book.', x, True),
        ('dishonour', f'A cheque of {inr(x := a(2000, 20000))} deposited into the bank was dishonoured; this was not recorded in the cash book.', -x, True),
        ('premium', f'The bank paid an insurance premium of {inr(x := a(1000, 12000))} under standing instructions; it was not recorded in the cash book.', -x, True),
        ('dividend', f'The bank collected a dividend of {inr(x := a(1000, 15000))} on the firm\'s investments; the cash book has no entry for it.', x, True),
        ('notsent', f'A cheque of {inr(x := a(2000, 20000))} received and entered in the bank column of the cash book was not sent to the bank.', -x, False),
        ('undercast', f'The debit side of the bank column of the cash book was undercast by {inr(x := a(100, 2000))}.', x, True),
    ]


def _bal(x):
    return f'{inr(abs(x))} ({"favourable" if x >= 0 else "overdraft"})'


def _brs(r, n, start_od=False, from_pb=False, pool=None):
    d = ctx(r)
    items = [i for i in _items(r) if pool is None or i[0] in pool]
    sel = r.sample(items, n)
    cb = amt(r, 10000, 90000, 100) * (-1 if start_od else 1)
    tot = sum(e for _, _, e, _ in sel)
    pb = cb + tot
    if (pb >= 0) != (cb >= 0) or pb == 0:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t}' for i, (_, t, _, _) in enumerate(sel))
    if not from_pb:
        S_, T_, effs, sname, tname = cb, pb, [e for _, _, e, _ in sel], 'cash book', 'pass book'
        start = f'The cash book of {d["f"]} showed a {"debit" if cb >= 0 else "credit"} balance (bank column) of {inr(abs(cb))} on 31 March 2026'
    else:
        S_, T_, effs, sname, tname = pb, cb, [-e for _, _, e, _ in sel], 'pass book', 'cash book'
        start = f'The pass book of {d["f"]} showed a {"credit" if pb >= 0 else "debit"} balance of {inr(abs(pb))} on 31 March 2026'
    if S_ < 0:
        start += ' (overdraft)'
    sign = 1 if S_ >= 0 else -1
    adds = [f'({i + 1}) {inr(abs(e))}' for i, e in enumerate(effs) if e * sign > 0]
    less = [f'({i + 1}) {inr(abs(e))}' for i, e in enumerate(effs) if e * sign < 0]
    what = 'favourable balance' if S_ >= 0 else 'overdraft'
    stem = f'{start}. Prepare a bank reconciliation statement to find the balance as per the {tname}: {lines}'
    ans = f'Balance as per {tname} {_bal(T_)}'
    key = (f'Start with {what} as per {sname} {inr(abs(S_))}; add {", ".join(adds) or "nil"}; less {", ".join(less) or "nil"}; '
           f'{"balance" if T_ >= 0 else "overdraft"} as per {tname} {inr(abs(T_))}.')
    return {'stem': stem, 'answer': ans, 'key': key}


def _retry(f, *a, **k):
    for _ in range(40):
        try:
            return f(*a, **k)
        except ValueError:
            continue
    raise ValueError


def c5s3_brs3(r):
    q = _retry(_brs, r, 3, start_od=False, from_pb=r.random() < 0.4)
    q['key'] += ' (1 mark per item.)'
    return q


def c5s3_brs4(r):
    q = _retry(_brs, r, 4, start_od=r.random() < 0.5, from_pb=r.random() < 0.3)
    q['key'] += ' (1 mark per item.)'
    return q


def c5s3_brs6(r):
    q = _retry(_brs, r, 6, start_od=r.random() < 0.5, from_pb=r.random() < 0.5)
    q['key'] += ' (1 mark per item; correct format and final balance required.)'
    return q


def c5s3_od(r):
    q = _retry(_brs, r, 4, start_od=True, from_pb=False)
    q['key'] += ' With an overdraft, items that would raise a favourable balance reduce the overdraft, and vice versa.'
    return q


def c5s3_one(r):
    for _ in range(20):
        code, text, eff, _ = r.choice(_items(r))
        if code != 'undercast':
            break
    od = r.random() < 0.4
    cb = amt(r, 20000, 80000, 1000) * (-1 if od else 1)
    pb = cb + eff
    if (pb >= 0) != (cb >= 0):
        raise ValueError
    wrong = [cb - eff, cb, -pb]
    return {'stem': f'The cash book shows {"an overdraft" if od else "a favourable bank balance"} of {inr(abs(cb))}. {text} What is the balance as per the pass book?',
            'answer': _bal(pb), 'key': f'{"Overdraft as per cash book" if od else "Balance as per cash book"} {inr(abs(cb))}; this item {"increases" if eff > 0 else "reduces"} the pass book balance{" (reduces the overdraft)" if od and eff > 0 else (" (increases the overdraft)" if od else "")} by {inr(abs(eff))}: {_bal(pb)}.',
            'distractors': [_bal(w) for w in wrong if w != pb and w != 0]}


def c5s4_amend(r):
    d = ctx(r)
    its = _items(r)
    amend = r.sample([i for i in its if i[3]], 3)
    timing = r.sample([i for i in its if not i[3]], 2)
    sel = amend + timing
    r.shuffle(sel)
    cb = amt(r, 20000, 90000, 100)
    adj = cb + sum(e for _, _, e, a in sel if a)
    pb = adj + sum(e for _, _, e, a in sel if not a)
    if adj <= 0 or pb <= 0:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t}' for i, (_, t, _, _) in enumerate(sel))
    am = ', '.join(f'({i + 1}) {"+" if e > 0 else "−"}{inr(abs(e))}' for i, (_, _, e, a) in enumerate(sel) if a)
    tm = ', '.join(f'({i + 1}) {"+" if e > 0 else "−"}{inr(abs(e))}' for i, (_, _, e, a) in enumerate(sel) if not a)
    return {'stem': f'The bank column of the cash book of {d["f"]} showed a debit balance of {inr(cb)} on 31 March 2026. Prepare the amended cash book and then a bank reconciliation statement: {lines}',
            'answer': f'Amended cash book balance {inr(adj)}; balance as per pass book {inr(pb)}',
            'key': f'Amended cash book: {inr(cb)} with {am} = {inr(adj)} (3 marks). BRS from amended balance: {tm} = pass book {inr(pb)} (3 marks). Only items not yet in the cash book are entered in it; timing differences go to the BRS.'}


def c5s4_amended_only(r):
    d = ctx(r)
    its = [i for i in _items(r) if i[3]]
    sel = r.sample(its, 3)
    cb = amt(r, 20000, 90000, 100)
    adj = cb + sum(e for _, _, e, _ in sel)
    if adj <= 0:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t}' for i, (_, t, _, _) in enumerate(sel))
    return {'stem': f'The cash book of {d["f"]} shows a bank balance of {inr(cb)}. Find the amended cash book balance after considering: {lines}',
            'answer': inr(adj), 'key': f'{inr(cb)} ' + ' '.join(f'{"+" if e > 0 else "−"} {inr(abs(e))}' for _, _, e, _ in sel) + f' = {inr(adj)}.',
            'distractors': [inr(cb - sum(e for _, _, e, _ in sel)), inr(cb), inr(cb + sum(abs(e) for _, _, e, _ in sel))]}


AMEND_L = ['Bank charges debited by the bank', 'Interest credited by the bank', 'Amount deposited directly into the bank by a customer',
           'A deposited cheque dishonoured by the bank', 'Insurance premium paid by the bank under standing instructions', 'Dividend collected by the bank']
TIMING_L = ['Cheques issued but not yet presented for payment', 'Cheques deposited but not yet cleared', 'A cheque received and recorded but not yet sent to the bank']


def c5s4_which_amend(r):
    if r.random() < 0.6:
        good = r.choice(AMEND_L)
        return mcq('Which of the following items is entered in the cash book when it is amended before preparing a bank reconciliation statement?', good, TIMING_L[:],
                   'Items the business learns of only from the pass book are entered in the amended cash book; timing differences go to the BRS.', r)
    good = r.choice(TIMING_L)
    return mcq('Which of the following items is NOT entered in the amended cash book, but shown in the bank reconciliation statement?', good, r.sample(AMEND_L, 3),
               f'"{good}" is a timing difference already correctly recorded in the cash book.', r)


def c5s2_cause(r):
    its = _items(r)
    sign = r.choice([1, -1])
    good = r.choice([i for i in its if (i[2] > 0) == (sign > 0) and i[0] != 'undercast'])
    wrong = r.sample([i for i in its if (i[2] > 0) != (sign > 0)], 3)
    word = 'more' if sign > 0 else 'less'
    return mcq(f'Which of the following makes the pass book balance {word} than the cash book balance (favourable balances)?', good[1].rstrip('.'), [w[1].rstrip('.') for w in wrong],
               f'This item {"increases" if sign > 0 else "reduces"} the bank\'s balance without a matching cash book entry (or before it).', r)


CAUSES = ['Time gap: cheque issued but not presented', 'Time gap: cheque deposited but not cleared', 'Recorded by the bank only', 'Error in the cash book']
CH05_ST2 = dict(
    scen=[('Classify the cause of difference between the cash book and pass book balances.', CAUSES, [
        ('{f} issued a cheque to {f2} on 29 March; {f2} deposited it in its bank on 4 April.', 'Time gap: cheque issued but not presented', 'The cash book records it on issue; the bank debits it only when presented.'),
        ('{f} deposited a cheque from {p} on 30 March; the bank credited it on 2 April.', 'Time gap: cheque deposited but not cleared', 'The cash book records it on deposit; the bank credits it on clearance.'),
        ('The bank deducted ₹350 as charges for a cheque book issued to {f}.', 'Recorded by the bank only', 'The firm learns of the charge only from the pass book.'),
        ('The bank credited ₹1,200 as interest on the savings balance of {f}.', 'Recorded by the bank only', 'The firm learns of the interest only from the pass book.'),
        ('The cashier of {f} totalled the bank column on the debit side as ₹1,52,000 instead of ₹1,53,000.', 'Error in the cash book', 'A casting error made by the firm.'),
        ('A customer of {f} paid ₹15,000 directly into its bank account through NEFT without informing it.', 'Recorded by the bank only', 'The firm has no record until it sees the pass book.'),
        ('A cheque of ₹8,000 issued by {f} was recorded twice in its cash book.', 'Error in the cash book', 'An error of recording by the firm.'),
        ('{f} sent cheques of ₹22,000 for collection on 31 March; they were collected on 3 April.', 'Time gap: cheque deposited but not cleared', 'The credit in the pass book comes after clearing.')], None)],
    lists=[('causes', 'causes of difference between the cash book and the pass book', [
        ('Cheques issued but not yet presented for payment', 'Recorded in the cash book on issue; debited by the bank only when presented.'),
        ('Cheques deposited but not yet cleared', 'Recorded in the cash book on deposit; credited by the bank only after clearing.'),
        ('Bank charges', 'Debited by the bank; the firm learns of them from the pass book.'),
        ('Interest allowed by the bank', 'Credited by the bank directly.'),
        ('Direct deposits by customers', 'Credited in the pass book before the firm records them.'),
        ('Direct payments by the bank under standing instructions', 'Debited in the pass book first.'),
        ('Dishonour of cheques', 'Debited by the bank before the firm records it.'),
        ('Errors in the cash book or the pass book', 'Mistakes in totalling, posting or recording on either side.')], None)],
    ars=[
        ('Bank charges make the pass book balance less than the cash book balance.', 'Bank charges are debited by the bank before the firm records them.', 'a', 'Both true and R explains A.'),
        ('A cheque issued but not presented makes the pass book balance more than the cash book balance.', 'The cash book is credited on issue but the bank debits the account only on presentation.', 'a', 'Both true and R explains A.'),
        ('Interest credited by the bank makes the cash book balance more than the pass book balance.', 'Interest is credited in the pass book before the firm records it.', 'd', 'A is false: the pass book balance becomes more. R is true.'),
        ('A cheque deposited but not cleared makes the pass book balance less than the cash book balance.', 'The firm debits the bank column on deposit, but the bank credits only on clearance.', 'a', 'Both true and R explains A.'),
        ('Dishonour of a cheque increases the pass book balance.', 'A dishonoured cheque is debited by the bank to the customer\'s account.', 'd', 'A is false: dishonour reduces the pass book balance. R is true.')],
)

CH05_ST1 = dict(
    cat='term',
    terms=[
        ('Bank reconciliation statement', 'A statement prepared to reconcile the balance shown by the bank column of the cash book with the balance shown by the pass book, explaining the differences.'),
        ('Pass book', 'A copy of the customer\'s account in the books of the bank, given to the customer.'),
        ('Bank statement', 'A periodic statement of the customer\'s account issued by the bank, showing deposits, withdrawals and balance.'),
        ('Favourable balance', 'A debit balance in the bank column of the cash book, which appears as a credit balance in the pass book.'),
        ('Overdraft', 'A balance showing that the firm has withdrawn more than it has deposited; a credit balance in the cash book and a debit balance in the pass book.'),
    ],
    lists=[('need', 'reasons for preparing a bank reconciliation statement', [
        ('Detects errors', 'Errors in the cash book or pass book are brought to light.'),
        ('Explains the difference', 'The reasons for the difference between the two balances become clear.'),
        ('Updates the cash book', 'Items recorded only by the bank are found and recorded.'),
        ('Prevents fraud', 'Regular reconciliation discourages misappropriation by staff.'),
        ('Shows uncleared cheques', 'Delays in collection or presentation of cheques can be followed up.')], None)],
    pairs=[('cash book (bank column)', 'pass book', [
        ('prepared by', 'the business', 'the bank'),
        ('deposits recorded on', 'the debit side', 'the credit side'),
        ('withdrawals recorded on', 'the credit side', 'the debit side'),
        ('favourable balance', 'a debit balance', 'a credit balance'),
        ('overdraft', 'a credit balance', 'a debit balance')])],
    ars=[
        ('A favourable balance appears as a debit in the cash book and a credit in the pass book.', 'The bank owes the money to the customer.', 'a', 'Both true and R explains A.'),
        ('A bank reconciliation statement is a part of the double entry system.', 'It is prepared to explain the differences between the two balances.', 'd', 'A is false: it is only a statement, not an account. R is true.'),
        ('Deposits are credited in the pass book.', 'The pass book is a copy of the customer\'s account in the books of the bank.', 'a', 'Both true and R explains A.'),
        ('An overdraft is a debit balance in the cash book.', 'An overdraft means the firm owes money to the bank.', 'd', 'A is false: an overdraft is a credit balance in the cash book. R is true.')],
    tf=('the bank reconciliation statement', [
        'A bank reconciliation statement is usually prepared at the end of a month.',
        'A favourable cash book balance is a debit balance.',
        'An overdraft appears as a debit balance in the pass book.'], [
        'A bank reconciliation statement is an account in the ledger.',
        'Withdrawals are credited in the pass book.',
        'The pass book is prepared by the business.',
        'A favourable balance in the pass book is a debit balance.']),
    scen=[('What does this balance indicate?', ['Favourable balance as per cash book', 'Overdraft as per cash book', 'Favourable balance as per pass book', 'Overdraft as per pass book'], [
        ('The bank column of the cash book of {f} shows a debit balance of ₹48,000.', 'Favourable balance as per cash book', 'A debit balance in the bank column means money lies in the bank.'),
        ('The bank column of the cash book of {f} shows a credit balance of ₹15,000.', 'Overdraft as per cash book', 'A credit balance in the bank column means the firm owes the bank.'),
        ('The pass book of {f} shows a credit balance of ₹62,500.', 'Favourable balance as per pass book', 'The bank owes the customer; a credit balance in its books.'),
        ('The pass book of {f} shows a debit balance of ₹22,000.', 'Overdraft as per pass book', 'The customer owes the bank; a debit balance in the bank\'s books.'),
        ('{f} has withdrawn ₹30,000 more than it deposited, under an overdraft limit; its cash book shows this.', 'Overdraft as per cash book', 'The excess withdrawal is a credit balance in the cash book.'),
        ('The statement from the bank shows that the bank owes {f} ₹74,000.', 'Favourable balance as per pass book', 'A credit balance in the pass book.')], None)],
    cases=[('C4', 'D4', 4, 'The accountant of {f}, {c}, finds that the cash book shows a bank balance of ₹86,000 but the bank statement shows ₹1,04,000 on 31 March. The owner {p} suspects a fraud.',
            [('Give two reasons, other than fraud, that could explain the difference.', 'Cheques issued but not yet presented; interest or direct deposits credited by the bank but not recorded in the cash book.'),
             ('How will a bank reconciliation statement help {p}?', 'It lists and explains each cause of difference, shows whether any difference is unexplained (possible error or fraud) and identifies items to enter in the cash book.')]),
           ('C4', 'D5', 4, '{f} prepares a bank reconciliation statement only once a year. During the year a clerk deposited fewer cheques than he recorded, and the firm also missed several bank charges.',
            [('What would monthly reconciliation have achieved?', 'Errors and the clerk\'s fraud would have been detected early; bank charges would have been recorded promptly.'),
             ('Suggest one control along with reconciliation.', 'Different persons should handle cash and record the cash book (division of duties); counterfoils of pay-in-slips should be checked.')])],
)

CH05_ST3_F = dict(ars=[
    ('When the cash book shows an overdraft, cheques issued but not presented are deducted.', 'Such cheques make the pass book overdraft smaller.', 'a', 'Both true and R explains A.'),
    ('When starting from a favourable cash book balance, bank charges are added.', 'Bank charges reduce the pass book balance.', 'd', 'A is false: they are deducted. R is true.'),
    ('Direct deposits by customers are added to the cash book balance to find the pass book balance.', 'They are credited by the bank but not yet recorded in the cash book.', 'a', 'Both true and R explains A.')])

CH05_ST4_F = dict(ars=[
    ('Bank charges are entered in the amended cash book.', 'The firm learns of bank charges only from the pass book.', 'a', 'Both true and R explains A.'),
    ('Cheques issued but not presented are entered in the amended cash book.', 'They are already recorded in the cash book.', 'd', 'A is false: they are already recorded; they go to the BRS. R is true.'),
    ('After amending the cash book, only timing differences remain in the BRS.', 'All items recorded by the bank only have then been entered in the cash book.', 'a', 'Both true and R explains A.')],
    tf=('the amended cash book', [
        'Interest credited by the bank is entered in the amended cash book.',
        'A cheque dishonoured but not recorded is entered on the credit side of the amended cash book.',
        'The amended cash book balance is shown in the balance sheet.'], [
        'Cheques deposited but not cleared are entered in the amended cash book.',
        'Bank charges are entered on the debit side of the amended cash book.',
        'The pass book balance is always shown in the balance sheet.',
        'Direct deposits are entered on the credit side of the amended cash book.']))


# ---------------- ch06 Trial Balance and Rectification of Errors

DR_BAL = [('Cash in hand', 2000, 60000), ('Bank', 10000, 150000), ('Debtors', 20000, 200000), ('Stock (opening)', 20000, 150000),
          ('Purchases', 100000, 600000), ('Wages', 10000, 80000), ('Salaries', 20000, 120000), ('Rent', 6000, 60000), ('Furniture', 10000, 100000),
          ('Machinery', 50000, 400000), ('Drawings', 10000, 60000), ('Sales return', 2000, 20000), ('Carriage inwards', 1000, 15000),
          ('Discount allowed', 500, 5000), ('Bad debts', 500, 8000), ('Insurance', 2000, 20000), ('Bills receivable', 5000, 50000)]
CR_BAL = [('Sales', 200000, 900000), ('Creditors', 20000, 150000), ('Bills payable', 5000, 50000), ('Bank loan', 50000, 300000),
          ('Purchases return', 2000, 20000), ('Commission received', 1000, 20000), ('Discount received', 500, 5000), ('Interest received', 1000, 10000)]


def c6s1_side(r):
    if r.random() < 0.5:
        good = r.choice(CR_BAL)[0]
        wrong = [x[0] for x in r.sample(DR_BAL, 3)]
        side = 'credit'
    else:
        good = r.choice(DR_BAL)[0]
        wrong = [x[0] for x in r.sample(CR_BAL, 3)]
        side = 'debit'
    return mcq(f'Which of the following balances is shown in the {side} column of a trial balance?', good, wrong,
               f'{good} has a {side} balance (assets, expenses, losses and drawings are debit balances; capital, liabilities, incomes and gains are credit balances).', r)


def c6s1_capital(r):
    return _retry(_c6s1_capital, r)


def _c6s1_capital(r):
    d = ctx(r)
    drs = [(n, amt(r, lo, hi, 500)) for n, lo, hi in r.sample(DR_BAL, 7)]
    crs = [(n, amt(r, lo, hi, 500)) for n, lo, hi in r.sample(CR_BAL, 3)]
    if not any(n == 'Sales' for n, _ in crs):
        crs[0] = ('Sales', amt(r, 200000, 600000, 1000))
    D, C = sum(x for _, x in drs), sum(x for _, x in crs)
    cap = D - C
    if cap < 50000:
        raise ValueError
    items = drs + crs
    r.shuffle(items)
    lines = ', '.join(f'{n} {inr(x)}' for n, x in items)
    return {'stem': f'Prepare the trial balance of {d["f"]} as on 31 March 2026 from the following balances and find the capital (the balancing figure): {lines}.',
            'answer': f'Capital {inr(cap)}; trial balance totals {inr(D)}',
            'key': f'Debit balances: {", ".join(n for n, _ in drs)} = {inr(D)}. Credit balances: {", ".join(n for n, _ in crs)} = {inr(C)}. Capital = {inr(D)} − {inr(C)} = {inr(cap)}; both columns total {inr(D)}.'}


def c6s1_total(r):
    drs = [(n, amt(r, lo, hi, 500)) for n, lo, hi in r.sample(DR_BAL, 4)]
    crs = [(n, amt(r, lo, hi, 500)) for n, lo, hi in r.sample(CR_BAL, 2)]
    D = sum(x for _, x in drs)
    C = sum(x for _, x in crs)
    items = drs + crs
    r.shuffle(items)
    lines = ', '.join(f'{n} {inr(x)}' for n, x in items)
    return {'stem': f'From these balances, find the total of the debit column of the trial balance: {lines}.', 'answer': inr(D),
            'key': f'Debit balances: {" + ".join(inr(x) for _, x in drs)} = {inr(D)}.', 'distractors': [inr(C), inr(D + C), inr(abs(D - C))]}


CH06_ST1 = dict(
    cat='term',
    terms=[('Trial balance', 'A statement of the debit and credit balances of all ledger accounts on a date, prepared to check the arithmetical accuracy of the books.'),
           ('Balance method', 'Preparing a trial balance by listing the closing balance of each ledger account in the debit or credit column.'),
           ('Totals method', 'Preparing a trial balance by listing the totals of the debit and credit sides of each account.'),
           ('Suspense account', 'A temporary account opened to put the difference in the trial balance, pending location of errors.')],
    lists=[('obj', 'objectives of preparing a trial balance', [
        ('To check the arithmetical accuracy of ledger accounts', 'Equal totals show that debits equal credits in the ledger.'),
        ('To help in locating errors', 'A difference points to errors that must be found.'),
        ('To summarise ledger balances', 'All balances are seen at one place.'),
        ('To help in preparing financial statements', 'Final accounts are prepared from the trial balance.')], None)],
    ars=[
        ('Agreement of the trial balance is not conclusive proof of accuracy.', 'Some errors do not affect the agreement of the trial balance.', 'a', 'Both true and R explains A.'),
        ('Drawings appear in the debit column of the trial balance.', 'Drawings reduce capital.', 'a', 'Both true and R explains A (a decrease in capital is a debit).'),
        ('A trial balance is an account.', 'A trial balance is prepared on a particular date.', 'd', 'A is false: it is a statement, not an account. R is true.'),
        ('Purchases return has a credit balance.', 'Purchases return reduces purchases.', 'a', 'Both true and R explains A.')],
    tf=('the trial balance', [
        'A trial balance is a statement, not an account.',
        'A trial balance can be prepared on any date.',
        'Agreement of the trial balance does not prove that there are no errors.'], [
        'A trial balance is a part of the double entry system.',
        'Errors of principle make the trial balance disagree.',
        'Capital appears in the debit column of a trial balance.',
        'A trial balance is prepared only at the end of the year.']),
)


def _errors(r):
    """(code, text, type, affects_tb, rect_dr, rect_cr) — rect lists of (acct, amt); 'Suspense A/c' used where needed after the trial balance."""
    d = ctx(r)
    p1, p2, f = d['p'], d['p2'], d['f2']

    def AB():
        A = amt(r, 1000, 40000, 100)
        return A, amt(r, 100, A - 100, 100)

    out = []
    A, B = AB()
    out.append(('E1', f'Purchase of furniture for {inr(A)} was debited to the Purchases account.', 'Error of principle', False, [('Furniture A/c', A)], [('Purchases A/c', A)]))
    A, B = AB()
    out.append(('E2', f'Repairs to machinery {inr(A)} were debited to the Machinery account.', 'Error of principle', False, [('Repairs A/c', A)], [('Machinery A/c', A)]))
    A, B = AB()
    out.append(('E3', f'Wages of {inr(A)} paid for installing a new machine were debited to the Wages account.', 'Error of principle', False, [('Machinery A/c', A)], [('Wages A/c', A)]))
    A, B = AB()
    out.append(('E4', f'Goods sold on credit to {p1} for {inr(A)} were debited to {p2}\'s account.', 'Error of commission', False, [(pa(p1), A)], [(pa(p2), A)]))
    A, B = AB()
    out.append(('E5', f'Cash {inr(A)} received from {p1} was credited to {p2}\'s account.', 'Error of commission', False, [(pa(p2), A)], [(pa(p1), A)]))
    A, B = AB()
    out.append(('E6', f'Credit purchase of goods from {f} for {inr(A)} was not recorded in the books at all.', 'Error of omission', False, [('Purchases A/c', A)], [(f'{f} A/c', A)]))
    A, B = AB()
    out.append(('E7', f'The sales book was undercast by {inr(A)}.', 'Error of commission', True, [('Suspense A/c', A)], [('Sales A/c', A)]))
    A, B = AB()
    out.append(('E8', f'The purchases book was overcast by {inr(A)}.', 'Error of commission', True, [('Suspense A/c', A)], [('Purchases A/c', A)]))
    A, B = AB()
    out.append(('E9', f'Rent paid {inr(A)} was not posted to the Rent account.', 'Error of omission', True, [('Rent A/c', A)], [('Suspense A/c', A)]))
    A, B = AB()
    out.append(('E10', f'Goods of {inr(A)} sold to {p1} were posted to {p1}\'s account as {inr(B)}.', 'Error of commission', True, [(pa(p1), A - B)], [('Suspense A/c', A - B)]))
    A, B = AB()
    out.append(('E11', f'Discount allowed to {p1}, {inr(B)}, was not posted to the Discount Allowed account.', 'Error of omission', True, [('Discount Allowed A/c', B)], [('Suspense A/c', B)]))
    A, B = AB()
    out.append(('E12', f'Returns inward of {inr(A)} were posted to the credit of the Returns Outward account.', 'Error of commission', True, [('Sales Return A/c', A), ('Purchases Return A/c', A)], [('Suspense A/c', 2 * A)]))
    A, B = AB()
    out.append(('E13', f'Goods costing {inr(A)} withdrawn by the proprietor for personal use were not recorded.', 'Error of omission', False, [('Drawings A/c', A)], [('Purchases A/c', A)]))
    A, B = AB()
    out.append(('E14', f'The sales book and the purchases book were both undercast by {inr(A)}.', 'Compensating error', False, [('Purchases A/c', A)], [('Sales A/c', A)]))
    A, B = AB()
    out.append(('E15', f'Cash paid to {f}, {inr(B)}, was debited to the account of {f} as {inr(A)}.', 'Error of commission', True, [('Suspense A/c', A - B)], [(f'{f} A/c', A - B)]))
    A, B = AB()
    out.append(('E16', f'Sale of old furniture for {inr(A)} was credited to the Sales account.', 'Error of principle', False, [('Sales A/c', A)], [('Furniture A/c', A)]))
    return out


ERR_TYPES = ['Error of omission', 'Error of commission', 'Error of principle', 'Compensating error']


def c6s2_type(r):
    code, text, typ, aff, _, _ = r.choice(_errors(r))
    return mcq(f'Classify the error: "{text}"', typ, [t for t in ERR_TYPES if t != typ], f'{typ}. It {"affects" if aff else "does not affect"} the agreement of the trial balance.', r)


def c6s2_affects(r):
    es = _errors(r)
    yes = [e for e in es if e[3]]
    no = [e for e in es if not e[3]]
    good = r.choice(no)
    wrong = r.sample(yes, 3)
    return mcq('Which of the following errors will NOT affect the agreement of the trial balance?', good[1].rstrip('.'), [w[1].rstrip('.') for w in wrong],
               f'"{good[1]}" is a {good[2].lower()} affecting both sides equally (or neither), so the trial balance still agrees.', r)


def c6s2_explain(r):
    es = r.sample(_errors(r), 3)
    lines = ' '.join(f'({i + 1}) {e[1]}' for i, e in enumerate(es))
    ans = ' '.join(f'({i + 1}) {e[2]}; {"affects" if e[3] else "does not affect"} the trial balance.' for i, e in enumerate(es))
    return {'stem': f'State the type of each error and whether it will affect the agreement of the trial balance: {lines}', 'answer': ans, 'key': f'1 mark each: {ans}'}


CH06_ST2 = dict(
    cat='type of error',
    terms=[('Error of omission', 'A transaction is omitted from the books wholly (not recorded in the book of original entry) or partially (not posted).'),
           ('Error of commission', 'A wrong amount, wrong account of the right class, wrong casting or wrong balancing is committed while recording or posting.'),
           ('Error of principle', 'A transaction is recorded against the fundamental principles of accounting, such as treating capital expenditure as revenue expenditure.'),
           ('Compensating error', 'Two or more errors whose effects cancel each other out.')],
    pairs=[('error of omission', 'error of commission', [
        ('meaning', 'a transaction is wholly or partly left out', 'a transaction is recorded wrongly (wrong amount, account or total)'),
        ('example', 'a credit purchase not recorded at all', 'a credit sale to A debited to B'),
        ('effect on trial balance', 'complete omission does not affect it; partial omission does', 'some (wrong casting, wrong posting of amount) affect it; others do not')])],
    ars=[
        ('An error of principle does not affect the agreement of the trial balance.', 'In an error of principle, the debit and credit are of the same amount though one account is wrong.', 'a', 'Both true and R explains A.'),
        ('Complete omission of a transaction affects the trial balance.', 'Both the debit and the credit are left out in a complete omission.', 'd', 'A is false; R is true.'),
        ('Compensating errors are difficult to locate.', 'They cancel each other\'s effect, so the trial balance agrees.', 'a', 'Both true and R explains A.'),
        ('Treating purchase of machinery as purchases of goods is an error of principle.', 'Capital expenditure is treated as revenue expenditure in this case.', 'a', 'Both true and R explains A.')],
)


def c6s3_suspense(r):
    es = [e for e in _errors(r) if e[3]]
    sel = r.sample(es, 3)
    dr = sum(x for e in sel for a, x in e[4] if a == 'Suspense A/c')
    cr = sum(x for e in sel for a, x in e[5] if a == 'Suspense A/c')
    bal = dr - cr
    if bal == 0:
        raise ValueError
    side = 'credit' if bal > 0 else 'debit'
    lines = ' '.join(f'({i + 1}) {e[1]}' for i, e in enumerate(sel))
    ent = ' '.join(f'({i + 1}) {entry(e[4], e[5])}.' for i, e in enumerate(sel))
    return {'stem': f'The trial balance of a trader did not agree and the difference was put to a suspense account. Later these errors were found: {lines} Pass the rectifying entries and find the original difference in the trial balance.',
            'answer': f'Suspense account had a {side} balance of {inr(abs(bal))}',
            'key': f'Entries: {ent} Suspense debited {inr(dr)}, credited {inr(cr)}; it closes, so it originally had a {side} balance of {inr(abs(bal))} (the {"debit" if side == "credit" else "credit"} side of the trial balance was larger).'}


def c6s3_side(r):
    e = r.choice([e for e in _errors(r) if e[3]])
    sd = 'debit' if any(a == 'Suspense A/c' for a, _ in e[4]) else 'credit'
    amt_ = sum(x for a, x in (e[4] if sd == 'debit' else e[5]) if a == 'Suspense A/c')
    good = f'Suspense A/c is {sd}ed with {inr(amt_)}'
    wrong = [f'Suspense A/c is {"credit" if sd == "debit" else "debit"}ed with {inr(amt_)}', 'Suspense A/c is not affected', f'Suspense A/c is {sd}ed with {inr(amt_ * 2)}']
    return mcq(f'After the trial balance, the following error is rectified: "{e[1]}" How is the suspense account affected?', good, wrong, f'Rectifying entry: {entry(e[4], e[5])}.', r)


CH06_ST3 = dict(
    cat='term',
    terms=[('Suspense account', 'A temporary account to which the difference in the trial balance is transferred until the errors are located and rectified.'),
           ('One-sided error', 'An error that affects only one account, so it disturbs the agreement of the trial balance.'),
           ('Two-sided error', 'An error that affects two or more accounts equally, so the trial balance still agrees.'),
           ('Casting error', 'A mistake in totalling a book or an account.')],
    lists=[('steps', 'steps to locate errors when the trial balance does not agree', [
        ('Recheck the totals of the trial balance', 'Re-add both columns.'),
        ('Check that every ledger balance is included', 'Compare the list of accounts with the ledger.'),
        ('Check the balancing of each account', 'Re-calculate balances, especially cash and personal accounts.'),
        ('Check the totals of subsidiary books', 'Recast the purchases, sales and returns books.'),
        ('Divide the difference by 2', 'A balance put on the wrong side causes a difference of double its amount.'),
        ('Divide the difference by 9', 'If divisible, a transposition of digits (e.g. 54 as 45) is likely.')], None)],
    ars=[
        ('A suspense account is opened when the trial balance does not agree.', 'It holds the difference temporarily until the errors are found.', 'a', 'Both true and R explains A.'),
        ('Errors of principle are rectified through the suspense account.', 'Errors of principle do not affect the trial balance.', 'd', 'A is false: they are rectified without the suspense account. R is true.'),
        ('If the difference in the trial balance is divisible by 9, a transposition error is possible.', 'Transposing two digits changes a number by a multiple of 9.', 'a', 'Both true and R explains A.'),
        ('The suspense account remains in the books permanently.', 'It is a temporary account closed when all errors are rectified.', 'd', 'A is false; R is true.')],
)


def c6s4_rect_mcq(r):
    e = r.choice(_errors(r))
    good = entry(e[4], e[5])
    if e[3]:
        alt1 = entry(e[5], e[4])
        nos = [(a, x) for a, x in e[4] + e[5] if a != 'Suspense A/c']
        alt2 = 'No entry is needed; the trial balance will agree'
        alt3 = entry([(a, x) for a, x in e[5]], [(a, x) for a, x in e[4]]).replace('Suspense A/c', 'Capital A/c')
        wrong = [alt1, alt2, alt3]
    else:
        wrong = [entry(e[5], e[4]), entry(e[4], [('Suspense A/c', sum(x for _, x in e[5]))]), entry([('Suspense A/c', sum(x for _, x in e[4]))], e[5])]
    if len({good, *wrong}) < 4:
        raise ValueError
    return mcq(f'Which entry rectifies the following error (found after the trial balance was prepared, with a suspense account)? "{e[1]}"', good, wrong, f'{good}.', r)


def c6s4_rect3(r):
    es = r.sample(_errors(r), 3)
    lines = ' '.join(f'({i + 1}) {e[1]}' for i, e in enumerate(es))
    ans = ' '.join(f'({i + 1}) {entry(e[4], e[5])}.' for i, e in enumerate(es))
    return {'stem': f'Rectify the following errors, found after the preparation of the trial balance (use a suspense account where needed): {lines}', 'answer': ans,
            'key': f'1 mark each: {ans}'}


def c6s4_rect6(r):
    es = r.sample(_errors(r), 5)
    if sum(e[3] for e in es) < 2:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {e[1]}' for i, e in enumerate(es))
    ans = ' '.join(f'({i + 1}) {entry(e[4], e[5])}.' for i, e in enumerate(es))
    dr = sum(x for e in es for a, x in e[4] if a == 'Suspense A/c')
    cr = sum(x for e in es for a, x in e[5] if a == 'Suspense A/c')
    bal = dr - cr
    if bal == 0:
        raise ValueError
    side = 'credit' if bal > 0 else 'debit'
    return {'stem': f'The trial balance of a firm did not agree and the difference was put to a suspense account. The following errors were later found. Pass rectifying entries and prepare the suspense account to find the original difference: {lines}',
            'answer': f'{ans} Original difference: suspense {side} balance {inr(abs(bal))}.',
            'key': f'Entries, 1 mark each: {ans} Suspense account (1 mark): debits {inr(dr)}, credits {inr(cr)}; opening {side} balance {inr(abs(bal))}.'}


def c6s4_before(r):
    e = r.choice([e for e in _errors(r) if e[3] and len(e[4]) == 1 and len(e[5]) == 1])
    side, acct, x = ('credit', e[5][0][0], e[5][0][1]) if e[4][0][0] == 'Suspense A/c' else ('debit', e[4][0][0], e[4][0][1])
    return {'stem': f'The following error is found BEFORE the trial balance is prepared. How will you rectify it? "{e[1]}"',
            'answer': f'Record {inr(x)} on the {side} side of {acct} (no journal entry; one-sided error)',
            'key': f'A one-sided error found before the trial balance is rectified by an explanatory entry on the {side} side of {acct} for {inr(x)}; no suspense account is needed. (After the trial balance it would be {entry(e[4], e[5])}.)'}


CH06_ST4_F = dict(
    ars=[
        ('One-sided errors found before the trial balance are rectified without a journal entry.', 'Only one account is affected by such errors.', 'a', 'Both true and R explains A.'),
        ('An error of commission affecting two personal accounts is rectified through the suspense account.', 'Such an error does not affect the agreement of the trial balance.', 'd', 'A is false: it is rectified by a journal entry between the two accounts, without suspense. R is true.'),
        ('Undercasting of the sales book is rectified by crediting the Sales account.', 'Undercasting means the total was recorded less than the correct amount.', 'a', 'Both true and R explains A.'),
        ('Rectification of errors affects the net profit when nominal accounts are involved.', 'Nominal accounts are transferred to the profit and loss account.', 'a', 'Both true and R explains A.')],
    tf=('rectification of errors', [
        'Two-sided errors are rectified by a journal entry.',
        'After the trial balance, one-sided errors are rectified through the suspense account.',
        'Overcasting of the purchases book is rectified by crediting the Purchases account.'], [
        'Errors of principle are rectified through the suspense account.',
        'Undercasting of the sales book is rectified by debiting the Sales account.',
        'Complete omission of a transaction is rectified through the suspense account.',
        'Rectification entries are never needed if the trial balance agrees.']),
)


def c6s4_profit_effect(r):
    d = ctx(r)
    es = [e for e in _errors(r) if e[0] in ('E1', 'E2', 'E3', 'E7', 'E8', 'E9', 'E11', 'E13', 'E14', 'E16')]
    sel = r.sample(es, 3)
    np_ = amt(r, 50000, 300000, 1000)
    eff = 0
    parts = []
    nominal = {'Purchases A/c': 1, 'Wages A/c': 1, 'Repairs A/c': 1, 'Rent A/c': 1, 'Discount Allowed A/c': 1, 'Sales A/c': -1}
    for e in sel:
        ch = 0
        for a, x in e[4]:
            if a in nominal:
                ch -= x if nominal[a] == 1 else x
        for a, x in e[5]:
            if a in nominal:
                ch += x if nominal[a] == 1 else x
        eff += ch
        parts.append(f'{e[0]}: {"+" if ch >= 0 else "−"}{inr(abs(ch))}')
    lines = ' '.join(f'({i + 1}) {e[1]}' for i, e in enumerate(sel))
    exp = '; '.join(f'({i + 1}) {"+" if p.split(": ")[1][0] == "+" else "−"}{p.split(": ")[1][1:]}' for i, p in enumerate(parts))
    return {'stem': f'{d["f"]} showed a net profit of {inr(np_)} before the following errors were found. Find the corrected net profit: {lines}',
            'answer': inr(np_ + eff), 'key': f'Effect on profit: {exp}; corrected profit {inr(np_)} {"+" if eff >= 0 else "−"} {inr(abs(eff))} = {inr(np_ + eff)}. (Debiting an expense or the Sales account reduces profit; crediting them increases it.)'}


# ---------------- ch07 Depreciation, Provisions and Reserves

CH07_ST1 = dict(
    cat='term',
    terms=[('Depreciation', 'A decline in the value of a fixed asset due to use, passage of time or obsolescence; the systematic allocation of its depreciable cost over its useful life.'),
           ('Depletion', 'The reduction in the quantity of a natural resource, such as a mine or quarry, as it is extracted.'),
           ('Amortisation', 'Writing off the cost of an intangible asset such as a patent or copyright over its useful life.'),
           ('Obsolescence', 'Loss in the usefulness of an asset because a better technology or a change in demand makes it outdated.'),
           ('Residual (scrap) value', 'The estimated net amount an asset will fetch at the end of its useful life.'),
           ('Useful life', 'The period over which an asset is expected to be used by the enterprise.')],
    lists=[('causes', 'causes of depreciation', [
        ('Wear and tear due to use', 'Physical deterioration of the asset as it is used.'),
        ('Expiry of legal rights', 'Assets such as patents or leases lose value as the right expires.'),
        ('Obsolescence', 'A newer technology makes the asset outdated.'),
        ('Abnormal factors', 'Accidents, fire or floods reduce the asset\'s value.')], 'factors'),
        ('factors', 'factors affecting the amount of depreciation', [
        ('Cost of the asset', 'Purchase price plus freight, installation and other costs to bring it into use.'),
        ('Estimated net residual value', 'Amount expected at the end of the useful life.'),
        ('Depreciable cost', 'Cost less estimated net residual value.'),
        ('Useful life', 'Period over which the asset is expected to be used.')], 'causes'),
        ('need', 'reasons for charging depreciation', [
        ('Matching of costs and revenue', 'The cost of the asset is charged against the revenues it helps to earn.'),
        ('Consideration of tax', 'Depreciation is a deductible expense for tax purposes.'),
        ('True and fair financial position', 'Assets are not overstated in the balance sheet.'),
        ('Compliance with law', 'Companies must charge depreciation under the Companies Act.')], None)],
    scen=[('Which cause of depreciation is illustrated?', ['Wear and tear due to use', 'Expiry of legal rights', 'Obsolescence', 'Abnormal factors'], [
        ('A delivery van of {f} has run 1,50,000 km and its engine and tyres are worn out.', 'Wear and tear due to use', 'Physical deterioration through use.'),
        ('{f} took a shop on a 10-year lease; 7 years have now passed.', 'Expiry of legal rights', 'The value of the lease falls as its term runs out.'),
        ('The old printing machine of {f} still works but buyers now want digital prints that it cannot produce.', 'Obsolescence', 'New technology has made the asset outdated.'),
        ('A flood in {c} damaged the machinery of {f}.', 'Abnormal factors', 'An accident or natural calamity reduced its value.'),
        ('{f} bought a 20-year patent for a {g} design; it has 4 years left.', 'Expiry of legal rights', 'The patent loses value as the period expires.'),
        ('The billing computers of {f} cannot run the new GST software.', 'Obsolescence', 'Change in technology made them out of date.')], None)],
    ars=[
        ('Depreciation is a non-cash expense.', 'No cash is paid when depreciation is charged.', 'a', 'Both true and R explains A.'),
        ('Depreciation is charged on land.', 'Land generally has an unlimited useful life.', 'd', 'A is false: land is not depreciated. R is true.'),
        ('Depreciation is charged to follow the matching concept.', 'The cost of an asset is spread over the periods that benefit from it.', 'a', 'Both true and R explains A.'),
        ('Depletion is used for intangible assets.', 'Depletion relates to natural resources such as mines.', 'd', 'A is false: amortisation is used for intangibles. R is true.')],
    tf=('depreciation', [
        'Depreciation reduces the book value of an asset.',
        'Depreciation is charged on fixed assets, not on current assets.',
        'Depreciation is a non-cash expense.'], [
        'Depreciation is a source of cash for the business.',
        'Depreciation is charged on the market value of the asset each year.',
        'Land is depreciated like buildings.',
        'Depreciation applies to natural resources as depletion and to stock as obsolescence.']),
    cases=[('C4', 'D4', 4, '{p}, owner of {f}, bought a delivery van for ₹6,00,000 three years ago. {He} has not charged any depreciation because "the van is still running well".',
            [('What is the effect on the profit and the balance sheet?', 'Profit is overstated every year and the van is shown above its true value, so statements are not true and fair.'),
             ('Give two reasons why depreciation must be charged.', 'Matching of cost with revenue; true financial position; tax deduction; compliance with law (any two).')]),
           ('C4', 'D5', 4, '{f} uses a computer system that is in perfect working condition but its software is no longer supported and competitors use faster systems.',
            [('Which cause of depreciation applies? Explain.', 'Obsolescence: the asset loses usefulness due to new technology even without physical wear.'),
             ('How should this affect the estimate of useful life?', 'Useful life should be estimated shorter than physical life, so depreciation per year is higher.')])],
)


def _asset(r):
    d = ctx(r)
    kind = r.choice(['machine', 'delivery van', 'computer system', 'generator', 'printing press', 'air-conditioning plant'])
    cost = amt(r, 50000, 600000, 5000)
    extra = amt(r, 1000, cost // 10, 500)
    life = r.choice([4, 5, 8, 10])
    scrap = amt(r, 0, cost // 8, 1000)
    dep = (cost + extra - scrap) / life
    if dep != int(dep):
        raise ValueError
    return d, kind, cost, extra, life, scrap, int(dep)


def c7s2_slm(r):
    d, kind, cost, extra, life, scrap, dep = _retry(_asset, r)
    return {'stem': f'{d["f"]} bought a {kind} for {inr(cost)} and spent {inr(extra)} on its transport and installation. Its useful life is {life} years and residual value {inr(scrap)}. Calculate the annual depreciation by the straight line method.',
            'answer': inr(dep), 'key': f'Depreciation = (cost + installation − residual value) ÷ life = ({inr(cost)} + {inr(extra)} − {inr(scrap)}) ÷ {life} = {inr(dep)}.',
            'distractors': [inr((cost - scrap) / life), inr((cost + extra) / life), inr((cost + extra + scrap) / life)]}


def c7s2_rate(r):
    d, kind, cost, extra, life, scrap, dep = _retry(_asset, r)
    tc = cost + extra
    rate = dep * 100 / tc
    return {'stem': f'A {kind} costing {inr(tc)} (including installation) has a residual value of {inr(scrap)} after {life} years. Find the annual depreciation and the rate of depreciation on original cost under the straight line method.',
            'answer': f'{inr(dep)} per year; rate {rate:.2f}%'.replace('.00%', '%'),
            'key': f'Depreciation = ({inr(tc)} − {inr(scrap)}) ÷ {life} = {inr(dep)}; rate = {inr(dep)} ÷ {inr(tc)} × 100 = {rate:.2f}%.'.replace('.00%', '%')}


def c7s2_wdv(r):
    d = ctx(r)
    cost = amt(r, 100000, 800000, 10000)
    rate = r.choice([10, 15, 20, 25])
    n = r.choice([2, 3])
    bv = cost
    deps = []
    for _ in range(n):
        x = round(bv * rate / 100, 2)
        deps.append(x)
        bv = round(bv - x, 2)
    return {'stem': f'{d["f"]} purchased machinery for {inr(cost)} on 1 April 2023. Depreciation is charged at {rate}% per annum on the written down value method; accounts close on 31 March. Find the depreciation for each of the first {n} years and the book value at the end of year {n}.',
            'answer': f'Depreciation: {", ".join(inr(x) for x in deps)}; book value {inr(bv)}',
            'key': f'Year-wise depreciation = {rate}% of opening book value: {", ".join(inr(x) for x in deps)}; book value = {inr(cost)} − {inr(sum(deps))} = {inr(bv)}.',
            'distractors': [f'Depreciation: {", ".join(inr(cost * rate / 100) for _ in deps)}; book value {inr(cost - n * cost * rate / 100)}',
                            f'Depreciation: {", ".join(inr(x) for x in deps)}; book value {inr(cost - deps[0])}',
                            f'Depreciation: {", ".join(inr(x) for x in deps)}; book value {inr(round(bv * (1 - rate / 100), 2))}']}


def c7s2_part_year(r):
    d = ctx(r)
    cost = amt(r, 60000, 600000, 6000)
    rate = r.choice([10, 15, 20])
    mon = r.choice([('1 July', 9), ('1 October', 6), ('1 January', 3), ('1 August', 8)])
    meth = r.choice(['straight line', 'written down value'])
    dep1 = cost * rate / 100 * mon[1] / 12
    if meth == 'straight line':
        dep2 = cost * rate / 100
    else:
        dep2 = (cost - dep1) * rate / 100
    return {'stem': f'A machine costing {inr(cost)} was bought on {mon[0]} 2024. Depreciation is {rate}% p.a. by the {meth} method; the accounting year ends on 31 March. Find the depreciation for 2024-25 and 2025-26.',
            'answer': f'2024-25: {inr(dep1)}; 2025-26: {inr(dep2)}',
            'key': f'2024-25: {rate}% × {inr(cost)} × {mon[1]}/12 = {inr(dep1)} (1½). 2025-26: {rate}% of {inr(cost) if meth == "straight line" else inr(cost - dep1)} = {inr(dep2)} (1½).'}


def c7s2_compare(r):
    cost = amt(r, 100000, 500000, 10000)
    rate = r.choice([10, 20])
    y = 3
    slm = cost * rate / 100
    bv = cost
    for _ in range(y - 1):
        bv -= bv * rate / 100
    wdv3 = bv * rate / 100
    return {'stem': f'An asset costs {inr(cost)}. Compare the depreciation charged in the third year at {rate}% under the straight line method and the written down value method, and explain why they differ.',
            'answer': f'SLM {inr(slm)}; WDV {inr(wdv3)}',
            'key': f'SLM: {rate}% of original cost every year = {inr(slm)} (1). WDV: book value at the start of year 3 = {inr(bv)}, depreciation {inr(wdv3)} (1). WDV charges decline because the rate applies to a falling book value; SLM is constant (1).'}


def c7s2_mcq_method(r):
    good, wrong = r.choice([
        ('Straight line method', ['Written down value method', 'Diminishing balance method', 'Reducing instalment method']),
        ('Written down value method', ['Straight line method', 'Fixed instalment method', 'Original cost method'])])
    desc = {'Straight line method': r.choice(['the same amount of depreciation is charged every year', 'depreciation is charged at a fixed rate on the original cost', 'the book value of the asset can become zero at the end of its life']),
            'Written down value method': r.choice(['depreciation is charged at a fixed rate on the reducing book value', 'the amount of depreciation falls year after year', 'the book value of the asset never becomes zero'])}[good]
    return mcq(f'Which method of depreciation has this feature: {desc}?', good, wrong, f'{good}: {desc}.', r)


CH07_ST2_F = dict(
    pairs=[('straight line method', 'written down value method', [
        ('basis of charge', 'original cost', 'book value at the beginning of each year'),
        ('annual depreciation', 'remains the same every year', 'decreases every year'),
        ('book value', 'can become zero at the end of the life', 'never becomes zero'),
        ('total charge for repairs and depreciation', 'increases over the years as repairs rise', 'remains more or less equal over the years'),
        ('suitability', 'assets with small repairs and certain life, such as leases and patents', 'assets needing more repairs as they age, such as plant and machinery'),
        ('recognition by income tax law', 'not generally accepted for tax', 'accepted by income tax authorities')])],
    ars=[
        ('Under the written down value method the book value of an asset never becomes zero.', 'Depreciation is charged at a fixed rate on the reducing balance.', 'a', 'Both true and R explains A.'),
        ('The straight line method is suitable for patents and leases.', 'The value of such assets falls evenly over a fixed period.', 'a', 'Both true and R explains A.'),
        ('Under the straight line method depreciation falls every year.', 'The rate is applied to the original cost.', 'd', 'A is false: SLM depreciation is the same every year. R is true.'),
        ('Installation charges are added to the cost of a machine for depreciation.', 'They are needed to bring the asset into working condition.', 'a', 'Both true and R explains A.')],
)


def c7s3_disposal(r):
    d = ctx(r)
    cost = amt(r, 100000, 500000, 10000)
    rate = r.choice([10, 20])
    meth = r.choice(['straight line', 'written down value'])
    n = r.choice([2, 3])
    bv = cost
    tot = 0
    for _ in range(n):
        x = cost * rate / 100 if meth == 'straight line' else bv * rate / 100
        tot += x
        bv -= x
    sale = round(bv + r.choice([-1, 1]) * amt(r, 2000, max(3000, int(bv) // 5), 500))
    pl = sale - bv
    return {'stem': f'{d["f"]} bought a machine for {inr(cost)} on 1 April 2022 and charged depreciation at {rate}% p.a. by the {meth} method (year ends 31 March). The machine was sold on 31 March {2022 + n} for {inr(sale)}. Find the book value on the date of sale and the profit or loss on sale.',
            'answer': f'Book value {inr(bv)}; {"profit" if pl >= 0 else "loss"} {inr(abs(pl))}',
            'key': f'Total depreciation for {n} years {inr(tot)}; book value {inr(cost)} − {inr(tot)} = {inr(bv)} (2). Sale {inr(sale)} − {inr(bv)} = {"profit" if pl >= 0 else "loss"} of {inr(abs(pl))} (1).'}


def c7s3_provision(r):
    d = ctx(r)
    cost = amt(r, 100000, 600000, 10000)
    rate = r.choice([10, 15, 20])
    n = r.choice([2, 3, 4])
    dep = cost * rate / 100
    prov = dep * n
    return {'stem': f'{d["f"]} bought machinery for {inr(cost)} and charges depreciation at {rate}% p.a. on original cost, credited to a Provision for Depreciation account. What is the balance of the provision for depreciation account after {n} years, and at what amount is the machinery account shown?',
            'answer': f'Provision {inr(prov)}; machinery account {inr(cost)}',
            'key': f'Annual depreciation {inr(dep)} × {n} = {inr(prov)} in the provision account; under this method the asset account stays at original cost {inr(cost)} (shown less provision in the balance sheet).',
            'distractors': [f'Provision {inr(prov)}; machinery account {inr(cost - prov)}', f'Provision {inr(dep)}; machinery account {inr(cost)}', f'Provision {inr(prov)}; machinery account {inr(cost - dep)}']}


def c7s3_entry(r):
    x = amt(r, 5000, 80000, 500)
    meth = r.choice(['asset', 'provision'])
    if meth == 'asset':
        good = entry([('Depreciation A/c', x)], [('Machinery A/c', x)])
        wrong = [entry([('Machinery A/c', x)], [('Depreciation A/c', x)]), entry([('Depreciation A/c', x)], [('Provision for Depreciation A/c', x)]),
                 entry([('Profit and Loss A/c', x)], [('Machinery A/c', x)])]
        txt = 'when depreciation is charged to the asset account'
    else:
        good = entry([('Depreciation A/c', x)], [('Provision for Depreciation A/c', x)])
        wrong = [entry([('Depreciation A/c', x)], [('Machinery A/c', x)]), entry([('Provision for Depreciation A/c', x)], [('Depreciation A/c', x)]),
                 entry([('Machinery A/c', x)], [('Provision for Depreciation A/c', x)])]
        txt = 'when a provision for depreciation account is maintained'
    return mcq(f'Which entry records depreciation of {inr(x)} on machinery {txt}?', good, wrong, f'{good}.', r)


def c7s3_disposal_entries(r):
    d = ctx(r)
    cost = amt(r, 100000, 500000, 10000)
    rate = r.choice([10, 20])
    n = r.choice([2, 3, 4])
    acc_ = cost * rate / 100 * n
    bv = cost - acc_
    sale = round(bv + r.choice([-1, 1]) * amt(r, 2000, 20000, 500))
    pl = sale - bv
    ent = [entry([('Asset Disposal A/c', cost)], [('Machinery A/c', cost)]), entry([('Provision for Depreciation A/c', acc_)], [('Asset Disposal A/c', acc_)]),
           entry([('Bank A/c', sale)], [('Asset Disposal A/c', sale)])]
    ent.append(entry([('Asset Disposal A/c', pl)], [('Profit and Loss A/c', pl)]) if pl > 0 else entry([('Profit and Loss A/c', -pl)], [('Asset Disposal A/c', -pl)]))
    return {'stem': f'A machine costing {inr(cost)}, on which accumulated depreciation of {inr(acc_)} stands in the provision for depreciation account, is sold by {d["f"]} for {inr(sale)} by cheque. Pass the journal entries using an asset disposal account.',
            'answer': ' '.join(f'({i + 1}) {e}.' for i, e in enumerate(ent)),
            'key': f'1 mark each: ' + ' '.join(f'({i + 1}) {e}.' for i, e in enumerate(ent)) + f' Book value {inr(bv)}; {"profit" if pl > 0 else "loss"} {inr(abs(pl))}.'}


CH07_ST3_F = dict(
    cat='term',
    terms=[('Provision for depreciation account', 'An account to which depreciation is credited every year, while the asset account continues at original cost; also called accumulated depreciation account.'),
           ('Asset disposal account', 'An account opened on sale of an asset, to which the cost, accumulated depreciation and sale proceeds are transferred to find the profit or loss.'),
           ('Book value', 'Cost of an asset less the depreciation charged on it till date.'),
           ('Accumulated depreciation', 'Total depreciation charged on an asset from the date of purchase till date.')],
    ars=[
        ('Under the provision method, the asset appears at original cost in the ledger.', 'Depreciation is credited to the provision for depreciation account, not to the asset account.', 'a', 'Both true and R explains A.'),
        ('Profit on sale of an asset is credited to the profit and loss account.', 'It is a gain not arising from normal operations.', 'b', 'Both true, but R does not explain the treatment; the profit is credited because it is a gain of the period.'),
        ('Depreciation account is closed by transfer to the trading account.', 'Depreciation is an expense.', 'd', 'A is false: it is transferred to the profit and loss account. R is true.')],
)

CH07_ST4 = dict(
    cat='term',
    terms=[('Provision', 'An amount charged against profit to provide for a known liability or a loss whose amount cannot be determined with substantial accuracy.'),
           ('Reserve', 'An amount set aside out of profits to strengthen the financial position or for future needs; an appropriation of profit.'),
           ('Revenue reserve', 'A reserve created out of revenue profits from normal operations, available for distribution as dividend.'),
           ('Capital reserve', 'A reserve created out of capital profits, such as profit on sale of fixed assets or premium on issue of shares; not usually available for dividend.'),
           ('General reserve', 'A revenue reserve not created for any specific purpose, to strengthen the business.'),
           ('Specific reserve', 'A reserve created for a particular purpose, such as a dividend equalisation reserve or debenture redemption reserve.'),
           ('Secret reserve', 'A reserve not disclosed in the balance sheet, created by undervaluing assets or overvaluing liabilities.')],
    pairs=[('provision', 'reserve', [
        ('nature', 'a charge against profit', 'an appropriation of profit'),
        ('purpose', 'to provide for a known liability or expected loss', 'to strengthen the financial position'),
        ('presentation', 'deducted from the asset or shown as a liability', 'shown under reserves and surplus'),
        ('effect on profit', 'reduces net profit', 'does not reduce net profit; divisible profit is reduced'),
        ('dividend', 'cannot be used for dividends', 'revenue reserves can be used for dividends'),
        ('compulsion', 'must be made even if there is no profit', 'created only when there is profit')])],
    scen=[('Identify the item as a provision or a type of reserve.', ['Provision', 'General reserve', 'Capital reserve', 'Specific reserve', 'Secret reserve'], [
        ('{f} sets aside 5% of debtors for doubtful debts.', 'Provision', 'It is a charge for an expected loss.'),
        ('{f} transfers 10% of its net profit to strengthen its position, without any specific purpose.', 'General reserve', 'A revenue reserve for no specific purpose.'),
        ('{f} keeps the profit earned on sale of its old building aside.', 'Capital reserve', 'Created out of a capital profit.'),
        ('{f} sets aside profits every year to redeem its debentures.', 'Specific reserve', 'Created for a particular purpose (debenture redemption).'),
        ('{f} deliberately charges excess depreciation, so that assets are shown at less than their true book value.', 'Secret reserve', 'Undervaluing assets creates an undisclosed reserve.'),
        ('{f} charges an amount against profit for taxes payable for the year.', 'Provision', 'It provides for a known liability of uncertain amount.'),
        ('{f} sets aside profit to keep its dividend rate steady over years.', 'Specific reserve', 'Dividend equalisation is a specific purpose.')], None)],
    ars=[
        ('A provision must be created even if there is a loss.', 'A provision is a charge against profit.', 'a', 'Both true and R explains A.'),
        ('A secret reserve is shown in the balance sheet.', 'A secret reserve is created by undervaluing assets.', 'd', 'A is false: it is not disclosed. R is true.'),
        ('Reserves are an appropriation of profit.', 'Reserves are created only out of profits.', 'a', 'Both true and R explains A.'),
        ('Capital reserve is freely used for paying dividends.', 'Capital reserve arises from capital profits.', 'd', 'A is false; R is true.')],
    tf=('provisions and reserves', [
        'Provision for doubtful debts is a provision, not a reserve.',
        'General reserve is a revenue reserve.',
        'Profit on revaluation of fixed assets is a capital profit.'], [
        'Reserves are a charge against profit.',
        'A provision is created only when there is profit.',
        'A secret reserve is always disclosed in the notes.',
        'Capital reserve is created out of normal trading profits.']),
    cases=[('C4', 'D4', 4, '{f} earned a profit of ₹6,00,000. It (a) set aside 5% of debtors of ₹4,00,000 for doubtful debts, (b) transferred ₹50,000 to general reserve, and (c) kept aside ₹30,000 profit on sale of land.',
            [('Classify each of (a), (b) and (c).', '(a) Provision (charge against profit, ₹20,000) (b) Revenue (general) reserve (appropriation) (c) Capital reserve.'),
             ('Which of these reduces the net profit shown in the profit and loss account?', 'Only (a), the provision of ₹20,000; reserves are appropriations made out of profit.')]),
           ('C4', 'D5', 4, 'The directors of {f} want to show lower profits by charging depreciation at 40% on machinery whose real fall in value is about 15%, to avoid demands for higher dividends.',
            [('What is created by this practice?', 'A secret reserve (assets are undervalued).'),
             ('Is it acceptable? Give one argument for and one against.', 'For: it strengthens the business and follows prudence. Against: it violates full disclosure; statements no longer show a true and fair view and shareholders are misled.')])],
)


FAMILIES = {
    S + '05-st1': facts(CH05_ST1),
    S + '05-st2': facts(CH05_ST2) + [FF('C2', 'D2', 'mcq', c5s2_cause), FF('C3', 'D2', 'mcq', c5s2_cause), FF('C3', 'D1', 'mcq', c5s3_one),
                                     FF('C4', 'D3', 'numerical', c5s3_brs3, marks=3, kinds=('m3',))],
    S + '05-st3': facts(CH05_ST3_F) + [FF('C1', 'D2', 'mcq', c5s2_cause), FF('C2', 'D2', 'mcq', c5s3_one), FF('C3', 'D2', 'numerical', c5s3_one, marks=1),
                                       FF('C3', 'D3', 'multi_step', c5s3_brs3, marks=3, kinds=('m3',)), FF('C3', 'D4', 'multi_step', c5s3_brs4, marks=4, kinds=('m4',)),
                                       FF('C4', 'D3', 'multi_step', c5s3_od, marks=4, kinds=('m4',)), FF('C4', 'D4', 'long', c5s3_brs6, marks=6, kinds=('m6',)),
                                       FF('C4', 'D5', 'long', c5s3_brs6, marks=6), FF('C2', 'D3', 'mcq', c5s3_one), FF('C3', 'D1', 'mcq', c5s3_one)],
    S + '05-st4': facts(CH05_ST4_F) + [FF('C1', 'D2', 'mcq', c5s4_which_amend), FF('C3', 'D2', 'numerical', c5s4_amended_only, marks=3, kinds=('m3',)),
                                       FF('C4', 'D4', 'long', c5s4_amend, marks=6, kinds=('m6',)), FF('C3', 'D3', 'numerical', c5s4_amended_only, marks=3),
                                       FF('C4', 'D3', 'long', c5s4_amend, marks=6), FF('C2', 'D1', 'mcq', c5s4_which_amend)],
    S + '06-st1': facts(CH06_ST1) + [FF('C2', 'D1', 'mcq', c6s1_side), FF('C2', 'D2', 'mcq', c6s1_side), FF('C3', 'D2', 'numerical', c6s1_total, marks=1),
                                     FF('C3', 'D3', 'multi_step', c6s1_capital, marks=4, kinds=('m4',)), FF('C4', 'D4', 'multi_step', c6s1_capital, marks=4)],
    S + '06-st2': facts(CH06_ST2) + [FF('C2', 'D2', 'mcq', c6s2_type), FF('C3', 'D2', 'mcq', c6s2_type), FF('C3', 'D3', 'mcq', c6s2_affects),
                                     FF('C3', 'D3', 'explain', c6s2_explain, marks=3, kinds=('m3',)), FF('C4', 'D4', 'explain', c6s2_explain, marks=3), FF('C2', 'D1', 'mcq', c6s2_type)],
    S + '06-st3': facts(CH06_ST3) + [FF('C3', 'D2', 'mcq', c6s3_side), FF('C3', 'D3', 'mcq', c6s3_side), FF('C4', 'D4', 'multi_step', c6s3_suspense, marks=4, kinds=('m4',)),
                                     FF('C4', 'D3', 'multi_step', c6s3_suspense, marks=4)],
    S + '06-st4': facts(CH06_ST4_F) + [FF('C2', 'D2', 'mcq', c6s4_rect_mcq), FF('C3', 'D2', 'mcq', c6s4_rect_mcq), FF('C3', 'D3', 'multi_step', c6s4_rect3, marks=3, kinds=('m3',)),
                                       FF('C3', 'D4', 'long', c6s4_rect6, marks=6, kinds=('m6',)), FF('C4', 'D4', 'long', c6s4_rect6, marks=6),
                                       FF('C3', 'D2', 'explain', c6s4_before, marks=2), FF('C4', 'D3', 'numerical', c6s4_profit_effect, marks=3, kinds=('m3',)),
                                       FF('C4', 'D5', 'numerical', c6s4_profit_effect, marks=4, kinds=('m4',)), FF('C1', 'D1', 'mcq', c6s4_rect_mcq)],
    S + '07-st1': facts(CH07_ST1),
    S + '07-st2': facts(CH07_ST2_F) + [FF('C1', 'D1', 'mcq', c7s2_mcq_method), FF('C1', 'D2', 'mcq', c7s2_mcq_method), FF('C3', 'D2', 'numerical', c7s2_slm, marks=2),
                                       FF('C3', 'D2', 'numerical', c7s2_rate, marks=2), FF('C3', 'D3', 'numerical', c7s2_wdv, marks=3, kinds=('m3',)),
                                       FF('C3', 'D4', 'numerical', c7s2_part_year, marks=3, kinds=('m3',)), FF('C4', 'D3', 'explain', c7s2_compare, marks=3, kinds=('m3',)),
                                       FF('C4', 'D4', 'numerical', c7s2_part_year, marks=3), FF('C3', 'D1', 'numerical', c7s2_slm, marks=1)],
    S + '07-st3': facts(CH07_ST3_F) + [FF('C2', 'D2', 'mcq', c7s3_entry), FF('C3', 'D2', 'mcq', c7s3_entry), FF('C3', 'D3', 'numerical', c7s3_disposal, marks=3, kinds=('m3',)),
                                       FF('C3', 'D2', 'numerical', c7s3_provision, marks=2), FF('C4', 'D4', 'multi_step', c7s3_disposal_entries, marks=4, kinds=('m4',)),
                                       FF('C4', 'D3', 'numerical', c7s3_disposal, marks=3), FF('C4', 'D5', 'multi_step', c7s3_disposal_entries, marks=4)],
    S + '07-st4': facts(CH07_ST4),
}
