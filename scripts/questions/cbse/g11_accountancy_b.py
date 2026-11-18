"""CBSE class 11 accountancy families, ch03-ch04 (Recording of Transactions I and II).

A transaction library (`TXNS`) gives, for each common transaction: narration, journal entry with the
nature of every account (modern approach), effect on the accounting equation, the book of original
entry, and the cash/bank effect. Generators for the journal, ledger, cash books and special purpose
books all work from it, so every answer is computed, not typed.
"""
from __future__ import annotations

from qbank import mcq, inr
from g11_accountancy_kit import facts, FF, ctx, firm, person, amt, entry, Cyc

S = 'cbse-g11-accountancy-ch'
MONTHS = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']


def pa(n):
    return f"{n}'s A/c" if not any(w in n for w in ('Traders', 'Enterprises', 'Stores', 'Sons', 'Industries', 'Agencies', 'Brothers', 'Retail')) else f'{n} A/c'


# Each builder returns dict(text, dr=[(acct, amt, nature)], cr=[...], eq=(dA, dL, dC) or None, book, cash=(col, +/-amt) list, contra)
def _t(text, dr, cr, eq, book, cash=(), alts=(), contra=False, eqtext=None, kind=''):
    return {'text': text, 'dr': dr, 'cr': cr, 'eq': eq, 'book': book, 'cash': list(cash), 'alts': list(alts),
            'contra': contra, 'eqtext': eqtext or text, 'kind': kind}


def t_capital_cash(r, d):
    x = amt(r, 100000, 800000, 10000)
    return _t(f'Commenced business with cash {inr(x)}', [('Cash A/c', x, 'asset')], [('Capital A/c', x, 'capital')], (x, 0, x), 'Cash Book',
              [('cash', x)], alts=[([('Capital A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Sales A/c', x)]), ([('Bank A/c', x)], [('Capital A/c', x)])], kind='capital')


def t_capital_bank(r, d):
    x = amt(r, 100000, 800000, 10000)
    return _t(f'Started business by depositing {inr(x)} in a bank account in the name of the firm', [('Bank A/c', x, 'asset')], [('Capital A/c', x, 'capital')],
              (x, 0, x), 'Cash Book', [('bank', x)], alts=[([('Capital A/c', x)], [('Bank A/c', x)]), ([('Cash A/c', x)], [('Capital A/c', x)]), ([('Bank A/c', x)], [('Cash A/c', x)])], kind='capital')


def t_deposit(r, d):
    x = amt(r, 5000, 80000, 1000)
    return _t(f'Deposited cash into bank {inr(x)}', [('Bank A/c', x, 'asset')], [('Cash A/c', x, 'asset')], (0, 0, 0), 'Cash Book',
              [('cash', -x), ('bank', x)], alts=[([('Cash A/c', x)], [('Bank A/c', x)]), ([('Bank A/c', x)], [('Capital A/c', x)]), ([('Cash A/c', x)], [('Capital A/c', x)])], contra=True, kind='contra')


def t_withdraw_office(r, d):
    x = amt(r, 2000, 30000, 1000)
    return _t(f'Withdrew {inr(x)} from bank for office use', [('Cash A/c', x, 'asset')], [('Bank A/c', x, 'asset')], (0, 0, 0), 'Cash Book',
              [('cash', x), ('bank', -x)], alts=[([('Drawings A/c', x)], [('Bank A/c', x)]), ([('Bank A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Drawings A/c', x)])], contra=True, kind='contra')


def t_purch_cash(r, d):
    x = amt(r, 5000, 90000, 500)
    return _t(f'Purchased goods for cash {inr(x)}', [('Purchases A/c', x, 'expense')], [('Cash A/c', x, 'asset')], (0, 0, 0), 'Cash Book',
              [('cash', -x)], alts=[([('Cash A/c', x)], [('Purchases A/c', x)]), ([('Purchases A/c', x)], [('Sales A/c', x)]), ([('Stock A/c', x)], [('Capital A/c', x)])],
              eqtext=f'Purchased goods for cash {inr(x)}', kind='purchase')


def t_purch_credit(r, d):
    x = amt(r, 5000, 120000, 500)
    s = d['f2']
    return _t(f'Purchased goods on credit from {s} {inr(x)}', [('Purchases A/c', x, 'expense')], [(pa(s), x, 'liability')], (x, x, 0), 'Purchases Book', [],
              alts=[([(pa(s), x)], [('Purchases A/c', x)]), ([('Purchases A/c', x)], [('Cash A/c', x)]), ([('Purchases A/c', x)], [('Sales A/c', x)])], kind='purchase')


def t_purch_cheque(r, d):
    x = amt(r, 5000, 90000, 500)
    return _t(f'Purchased goods and paid by cheque {inr(x)}', [('Purchases A/c', x, 'expense')], [('Bank A/c', x, 'asset')], (0, 0, 0), 'Cash Book', [('bank', -x)],
              alts=[([('Bank A/c', x)], [('Purchases A/c', x)]), ([('Purchases A/c', x)], [('Cash A/c', x)]), ([('Purchases A/c', x)], [('Capital A/c', x)])], kind='purchase')


def t_sale_cash(r, d):
    cost = amt(r, 5000, 80000, 500)
    x = cost + amt(r, 1000, cost // 2 + 1000, 500)
    return _t(f'Sold goods for cash {inr(x)}', [('Cash A/c', x, 'asset')], [('Sales A/c', x, 'revenue')], (x - cost, 0, x - cost), 'Cash Book', [('cash', x)],
              alts=[([('Sales A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Purchases A/c', x)]), ([('Cash A/c', x)], [('Capital A/c', x)])],
              eqtext=f'Sold goods costing {inr(cost)} for cash {inr(x)}', kind='sale')


def t_sale_credit(r, d):
    cost = amt(r, 5000, 90000, 500)
    x = cost + amt(r, 1000, cost // 2 + 1000, 500)
    c = d['p2']
    return _t(f'Sold goods to {c} on credit {inr(x)}', [(pa(c), x, 'asset')], [('Sales A/c', x, 'revenue')], (x - cost, 0, x - cost), 'Sales Book', [],
              alts=[([('Sales A/c', x)], [(pa(c), x)]), ([('Cash A/c', x)], [('Sales A/c', x)]), ([(pa(c), x)], [('Purchases A/c', x)])],
              eqtext=f'Sold goods costing {inr(cost)} to {c} on credit for {inr(x)}', kind='sale')


def _expense(label, acct, lo, hi):
    def f(r, d):
        x = amt(r, lo, hi, 100)
        return _t(f'Paid {label} {inr(x)}', [(acct, x, 'expense')], [('Cash A/c', x, 'asset')], (-x, 0, -x), 'Cash Book', [('cash', -x)],
                  alts=[([('Cash A/c', x)], [(acct, x)]), ([(acct, x)], [('Capital A/c', x)]), ([('Drawings A/c', x)], [('Cash A/c', x)])], kind='expense')
    return f


t_rent = _expense('rent', 'Rent A/c', 3000, 40000)
t_salary = _expense('salaries', 'Salaries A/c', 10000, 90000)
t_wages = _expense('wages', 'Wages A/c', 2000, 30000)
t_stationery = _expense('for stationery', 'Stationery A/c', 500, 6000)


def t_electricity(r, d):
    x = amt(r, 1000, 15000, 100)
    return _t(f'Paid electricity bill by cheque {inr(x)}', [('Electricity Charges A/c', x, 'expense')], [('Bank A/c', x, 'asset')], (-x, 0, -x), 'Cash Book', [('bank', -x)],
              alts=[([('Bank A/c', x)], [('Electricity Charges A/c', x)]), ([('Electricity Charges A/c', x)], [('Cash A/c', x)]), ([('Drawings A/c', x)], [('Bank A/c', x)])], kind='expense')


def t_commission(r, d):
    x = amt(r, 1000, 20000, 100)
    return _t(f'Received commission {inr(x)}', [('Cash A/c', x, 'asset')], [('Commission Received A/c', x, 'revenue')], (x, 0, x), 'Cash Book', [('cash', x)],
              alts=[([('Commission Received A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Capital A/c', x)]), ([('Commission Paid A/c', x)], [('Cash A/c', x)])], kind='income')


def t_drawings_cash(r, d):
    x = amt(r, 2000, 30000, 500)
    return _t(f'Withdrew cash for personal use {inr(x)}', [('Drawings A/c', x, 'capital')], [('Cash A/c', x, 'asset')], (-x, 0, -x), 'Cash Book', [('cash', -x)],
              alts=[([('Cash A/c', x)], [('Drawings A/c', x)]), ([('Capital A/c', x)], [('Drawings A/c', x)]), ([('Drawings A/c', x)], [('Bank A/c', x)])], kind='drawings')


def t_drawings_goods(r, d):
    x = amt(r, 1000, 20000, 500)
    return _t(f'Withdrew goods costing {inr(x)} for personal use', [('Drawings A/c', x, 'capital')], [('Purchases A/c', x, 'expense')], (-x, 0, -x), 'Journal Proper', [],
              alts=[([('Drawings A/c', x)], [('Sales A/c', x)]), ([('Purchases A/c', x)], [('Drawings A/c', x)]), ([('Drawings A/c', x)], [('Cash A/c', x)])], kind='drawings')


def t_life_premium(r, d):
    x = amt(r, 2000, 25000, 500)
    return _t(f'Paid the proprietor\'s life insurance premium {inr(x)} from business cash', [('Drawings A/c', x, 'capital')], [('Cash A/c', x, 'asset')], (-x, 0, -x), 'Cash Book', [('cash', -x)],
              alts=[([('Insurance Premium A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Drawings A/c', x)]), ([('Life Insurance A/c', x)], [('Capital A/c', x)])], kind='drawings')


def t_furniture_cash(r, d):
    x = amt(r, 5000, 80000, 500)
    return _t(f'Purchased furniture for cash {inr(x)}', [('Furniture A/c', x, 'asset')], [('Cash A/c', x, 'asset')], (0, 0, 0), 'Cash Book', [('cash', -x)],
              alts=[([('Purchases A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Furniture A/c', x)]), ([('Furniture A/c', x)], [('Capital A/c', x)])], kind='asset')


def t_computer_cheque(r, d):
    x = amt(r, 25000, 120000, 1000)
    return _t(f'Bought a computer for office use and paid by cheque {inr(x)}', [('Computer A/c', x, 'asset')], [('Bank A/c', x, 'asset')], (0, 0, 0), 'Cash Book', [('bank', -x)],
              alts=[([('Purchases A/c', x)], [('Bank A/c', x)]), ([('Bank A/c', x)], [('Computer A/c', x)]), ([('Office Expenses A/c', x)], [('Bank A/c', x)])], kind='asset')


def t_machinery_credit(r, d):
    x = amt(r, 50000, 400000, 5000)
    s = d['f2']
    return _t(f'Purchased machinery on credit from {s} {inr(x)}', [('Machinery A/c', x, 'asset')], [(pa(s), x, 'liability')], (x, x, 0), 'Journal Proper', [],
              alts=[([('Purchases A/c', x)], [(pa(s), x)]), ([('Machinery A/c', x)], [('Cash A/c', x)]), ([(pa(s), x)], [('Machinery A/c', x)])], kind='asset')


def t_pay_creditor_disc(r, d):
    y = amt(r, 5000, 80000, 500)
    dis = amt(r, 100, max(200, y // 20), 50)
    x = y - dis
    s = d['f2']
    return _t(f'Paid {inr(x)} in cash to {s} in full settlement of {inr(y)}', [(pa(s), y, 'liability')], [('Cash A/c', x, 'asset'), ('Discount Received A/c', dis, 'revenue')],
              (-x, -y, dis), 'Cash Book', [('cash', -x)],
              alts=[([(pa(s), x)], [('Cash A/c', x)]), ([(pa(s), y)], [('Cash A/c', y)]), ([(pa(s), x), ('Discount Allowed A/c', dis)], [('Cash A/c', y)])], kind='settle')


def t_recv_debtor_disc(r, d):
    y = amt(r, 5000, 80000, 500)
    dis = amt(r, 100, max(200, y // 20), 50)
    x = y - dis
    c = d['p2']
    return _t(f'Received {inr(x)} in cash from {c} in full settlement of {inr(y)}', [('Cash A/c', x, 'asset'), ('Discount Allowed A/c', dis, 'expense')], [(pa(c), y, 'asset')],
              (x - y, 0, -dis), 'Cash Book', [('cash', x)],
              alts=[([('Cash A/c', x)], [(pa(c), x)]), ([('Cash A/c', y)], [(pa(c), y)]), ([('Cash A/c', y)], [(pa(c), x), ('Discount Received A/c', dis)])], kind='settle')


def t_pay_creditor_cheque(r, d):
    x = amt(r, 5000, 90000, 500)
    s = d['f2']
    return _t(f'Paid {s} by cheque {inr(x)}', [(pa(s), x, 'liability')], [('Bank A/c', x, 'asset')], (-x, -x, 0), 'Cash Book', [('bank', -x)],
              alts=[([('Bank A/c', x)], [(pa(s), x)]), ([(pa(s), x)], [('Cash A/c', x)]), ([('Purchases A/c', x)], [('Bank A/c', x)])], kind='settle')


def t_recv_cheque_deposit(r, d):
    x = amt(r, 5000, 90000, 500)
    c = d['p2']
    return _t(f'Received a cheque of {inr(x)} from {c} and deposited it into bank the same day', [('Bank A/c', x, 'asset')], [(pa(c), x, 'asset')], (0, 0, 0), 'Cash Book', [('bank', x)],
              alts=[([(pa(c), x)], [('Bank A/c', x)]), ([('Cash A/c', x)], [(pa(c), x)]), ([('Bank A/c', x)], [('Sales A/c', x)])], kind='settle')


def t_fire(r, d):
    x = amt(r, 10000, 100000, 1000)
    y = amt(r, 5000, x - 2000, 1000)
    return _t(f'Goods costing {inr(x)} were destroyed by fire; the insurance company admitted a claim of {inr(y)}',
              [('Loss by Fire A/c', x - y, 'expense'), ('Insurance Claim A/c', y, 'asset')], [('Purchases A/c', x, 'expense')], (y - x, 0, y - x), 'Journal Proper', [],
              alts=[([('Loss by Fire A/c', x)], [('Purchases A/c', x)]), ([('Insurance Claim A/c', x)], [('Purchases A/c', x)]), ([('Loss by Fire A/c', x - y), ('Insurance Claim A/c', y)], [('Sales A/c', x)])], kind='loss')


def t_samples(r, d):
    x = amt(r, 1000, 15000, 500)
    return _t(f'Distributed goods costing {inr(x)} as free samples', [('Advertisement A/c', x, 'expense')], [('Purchases A/c', x, 'expense')], (-x, 0, -x), 'Journal Proper', [],
              alts=[([('Advertisement A/c', x)], [('Sales A/c', x)]), ([('Drawings A/c', x)], [('Purchases A/c', x)]), ([('Purchases A/c', x)], [('Advertisement A/c', x)])], kind='loss')


def t_loan(r, d):
    x = amt(r, 50000, 500000, 10000)
    bank = r.choice(['State Bank of India', 'Punjab National Bank', 'Bank of Baroda', 'Canara Bank'])
    return _t(f'Took a loan of {inr(x)} from {bank}; the amount was credited to the firm\'s bank account', [('Bank A/c', x, 'asset')], [(f'Loan from {bank} A/c', x, 'liability')],
              (x, x, 0), 'Cash Book', [('bank', x)],
              alts=[([(f'Loan from {bank} A/c', x)], [('Bank A/c', x)]), ([('Bank A/c', x)], [('Capital A/c', x)]), ([('Cash A/c', x)], [('Bank A/c', x)])], kind='loan')


def t_interest_loan(r, d):
    x = amt(r, 1000, 20000, 100)
    return _t(f'Paid interest on loan by cheque {inr(x)}', [('Interest on Loan A/c', x, 'expense')], [('Bank A/c', x, 'asset')], (-x, 0, -x), 'Cash Book', [('bank', -x)],
              alts=[([('Loan A/c', x)], [('Bank A/c', x)]), ([('Bank A/c', x)], [('Interest on Loan A/c', x)]), ([('Interest on Loan A/c', x)], [('Capital A/c', x)])], kind='expense')


def t_gst_purchase(r, d):
    x = amt(r, 10000, 100000, 1000)
    rate = r.choice([5, 12, 18])
    t = x * rate / 200
    return _t(f'Purchased goods for {inr(x)} plus CGST and SGST @ {rate / 2:g}% each, paying by cheque', [('Purchases A/c', x, 'expense'), ('Input CGST A/c', t, 'asset'), ('Input SGST A/c', t, 'asset')],
              [('Bank A/c', x + 2 * t, 'asset')], (0, 0, 0), 'Cash Book', [('bank', -(x + 2 * t))],
              alts=[([('Purchases A/c', x + 2 * t)], [('Bank A/c', x + 2 * t)]), ([('Purchases A/c', x), ('Output CGST A/c', t), ('Output SGST A/c', t)], [('Bank A/c', x + 2 * t)]),
                    ([('Purchases A/c', x), ('Input IGST A/c', 2 * t)], [('Bank A/c', x + 2 * t)])], kind='gst')


def t_gst_sale_inter(r, d):
    x = amt(r, 10000, 120000, 1000)
    rate = r.choice([5, 12, 18])
    t = x * rate / 100
    c = d['p2']
    return _t(f'Sold goods for {inr(x)} on credit to {c} of another state, charging IGST @ {rate}%', [(pa(c), x + t, 'asset')], [('Sales A/c', x, 'revenue'), ('Output IGST A/c', t, 'liability')],
              None, 'Sales Book', [],
              alts=[([(pa(c), x + t)], [('Sales A/c', x + t)]), ([(pa(c), x + t)], [('Sales A/c', x), ('Output CGST A/c', t / 2), ('Output SGST A/c', t / 2)]),
                    ([(pa(c), x + t)], [('Sales A/c', x), ('Input IGST A/c', t)])], kind='gst')


def t_purch_return(r, d):
    x = amt(r, 1000, 20000, 500)
    s = d['f2']
    return _t(f'Returned goods worth {inr(x)} to {s}', [(pa(s), x, 'liability')], [('Purchases Return A/c', x, 'expense')], (-x, -x, 0), 'Purchases Return Book', [],
              alts=[([('Purchases Return A/c', x)], [(pa(s), x)]), ([(pa(s), x)], [('Sales Return A/c', x)]), ([(pa(s), x)], [('Cash A/c', x)])], kind='return')


def t_sales_return(r, d):
    x = amt(r, 1000, 20000, 500)
    c = d['p2']
    return _t(f'{c} returned goods worth {inr(x)}', [('Sales Return A/c', x, 'revenue')], [(pa(c), x, 'asset')], None, 'Sales Return Book', [],
              alts=[([(pa(c), x)], [('Sales Return A/c', x)]), ([('Purchases Return A/c', x)], [(pa(c), x)]), ([('Sales Return A/c', x)], [('Cash A/c', x)])], kind='return')


def t_bad_debt(r, d):
    y = amt(r, 5000, 50000, 500)
    pct = r.choice([40, 50, 60, 75])
    x = y * pct // 100
    c = d['p2']
    return _t(f'{c}, who owed {inr(y)}, became insolvent and paid {pct} paise in the rupee in cash', [('Cash A/c', x, 'asset'), ('Bad Debts A/c', y - x, 'expense')], [(pa(c), y, 'asset')],
              (x - y, 0, x - y), 'Cash Book', [('cash', x)],
              alts=[([('Cash A/c', x)], [(pa(c), x)]), ([('Bad Debts A/c', y)], [(pa(c), y)]), ([('Cash A/c', x), ('Bad Debts A/c', y - x)], [('Sales A/c', y)])], kind='loss')


def t_trade_disc(r, d):
    lp = amt(r, 10000, 100000, 1000)
    td = r.choice([5, 10, 15, 20])
    net = lp * (100 - td) // 100
    s = d['f2']
    return _t(f'Purchased goods with a list price of {inr(lp)} from {s} on credit at {td}% trade discount', [('Purchases A/c', net, 'expense')], [(pa(s), net, 'liability')],
              (net, net, 0), 'Purchases Book', [],
              alts=[([('Purchases A/c', lp)], [(pa(s), lp)]), ([('Purchases A/c', lp)], [(pa(s), net), ('Discount Received A/c', lp - net)]), ([(pa(s), net)], [('Purchases A/c', net)])], kind='purchase')


def t_charity(r, d):
    x = amt(r, 500, 10000, 500)
    return _t(f'Paid {inr(x)} in cash as donation to a relief fund', [('Charity A/c', x, 'expense')], [('Cash A/c', x, 'asset')], (-x, 0, -x), 'Cash Book', [('cash', -x)],
              alts=[([('Cash A/c', x)], [('Charity A/c', x)]), ([('Charity A/c', x)], [('Capital A/c', x)]), ([('Purchases A/c', x)], [('Cash A/c', x)])], kind='expense')


def t_add_capital(r, d):
    x = amt(r, 20000, 200000, 5000)
    return _t(f'The proprietor brought in additional capital in cash {inr(x)}', [('Cash A/c', x, 'asset')], [('Capital A/c', x, 'capital')], (x, 0, x), 'Cash Book', [('cash', x)],
              alts=[([('Capital A/c', x)], [('Cash A/c', x)]), ([('Cash A/c', x)], [('Drawings A/c', x)]), ([('Cash A/c', x)], [('Loan A/c', x)])], kind='capital')


TXNS = [t_capital_cash, t_capital_bank, t_deposit, t_withdraw_office, t_purch_cash, t_purch_credit, t_purch_cheque, t_sale_cash, t_sale_credit,
        t_rent, t_salary, t_wages, t_stationery, t_electricity, t_commission, t_drawings_cash, t_drawings_goods, t_life_premium, t_furniture_cash,
        t_computer_cheque, t_machinery_credit, t_pay_creditor_disc, t_recv_debtor_disc, t_pay_creditor_cheque, t_recv_cheque_deposit, t_fire,
        t_samples, t_loan, t_interest_loan, t_gst_purchase, t_gst_sale_inter, t_purch_return, t_sales_return, t_bad_debt, t_trade_disc, t_charity, t_add_capital]
import random as _random
_R0 = _random.Random(0)
SIMPLE = [t for t in TXNS if len(t(_R0, ctx(_R0))['dr']) == 1 and len(t(_R0, ctx(_R0))['cr']) == 1]
EQ_TXNS = [t for t in TXNS if t not in (t_gst_sale_inter, t_sales_return)]


def strip(lst):
    return [(a, x) for a, x, *_ in lst]


def je(t):
    return entry(strip(t['dr']), strip(t['cr']))


def txn(r, pool=None, d=None):
    d = d or ctx(r)
    return r.choice(pool or TXNS)(r, d), d


# ---------------- ch03 st1 source documents

DOCS = ['Cash memo', 'Invoice (bill)', 'Receipt', 'Pay-in-slip', 'Cheque', 'Debit note', 'Credit note', 'Voucher']
CH03_ST1 = dict(
    cat='source document',
    terms=[
        ('Cash memo', 'Document issued by the seller for a cash sale, showing the goods, quantity, rate and amount received.'),
        ('Invoice (bill)', 'Document prepared by the seller for a credit sale, giving the details of goods sold and the amount due from the buyer.'),
        ('Receipt', 'Written acknowledgement given by the receiver of cash to the person paying it.'),
        ('Pay-in-slip', 'Printed form used to deposit cash or cheques into a bank account; the counterfoil is returned stamped by the bank.'),
        ('Cheque', 'Written order by an account holder directing the bank to pay a stated sum to a named person or to the bearer.'),
        ('Debit note', 'Document sent to a supplier stating that the supplier\'s account has been debited, for example for goods returned.'),
        ('Credit note', 'Document sent to a customer stating that the customer\'s account has been credited, for example for goods returned by him.'),
        ('Voucher', 'Documentary evidence prepared in support of a business transaction and used as the basis of recording it.'),
    ],
    scen=[('Which source document is used?', DOCS, [
        ('{f} sells {g} worth ₹3,200 to a walk-in customer who pays cash at the counter.', 'Cash memo', 'A cash sale is supported by a cash memo.'),
        ('{f} supplies {g} worth ₹48,000 to {f2} on 30 days\' credit.', 'Invoice (bill)', 'A credit sale is supported by an invoice or bill.'),
        ('{p} pays ₹15,000 in cash to {f} and asks for written proof of payment.', 'Receipt', 'A receipt acknowledges cash received.'),
        ('The cashier of {f} deposits the day\'s cash of ₹62,000 into the firm\'s bank account.', 'Pay-in-slip', 'Deposits are made with a pay-in-slip.'),
        ('{f} returns damaged {g} worth ₹4,000 to its supplier {f2} and informs it that its account has been debited.', 'Debit note', 'A debit note is sent to the supplier for purchase returns.'),
        ('A customer returns {g} worth ₹2,500 to {f}, which informs him that his account has been credited.', 'Credit note', 'A credit note is sent to the customer for sales returns.'),
        ('{f} pays its supplier ₹27,000 by an order on its bank account.', 'Cheque', 'A cheque orders the bank to pay the stated sum.'),
        ('The accountant of {f} prepares a document recording the debit and credit for payment of rent, attaching the landlord\'s receipt.', 'Voucher', 'An accounting voucher supports the entry.')], None)],
    lists=[('vtypes', 'types of accounting vouchers', [
        ('Cash voucher', 'Supports a cash transaction; debit voucher for payment, credit voucher for receipt.'),
        ('Debit voucher', 'Supports a payment and shows the account to be debited.'),
        ('Credit voucher', 'Supports a receipt and shows the account to be credited.'),
        ('Transfer voucher', 'Supports a non-cash (credit or adjustment) transaction.'),
        ('Complex (compound) voucher', 'Used when a transaction involves more than one debit or credit.')], None)],
    ars=[
        ('Every transaction should be supported by a source document.', 'Source documents provide evidence for recording transactions.', 'a', 'Both true and R explains A.'),
        ('A cash memo is issued for a credit sale.', 'An invoice shows the amount due from the buyer.', 'd', 'A is false: a cash memo is for a cash sale. R is true.'),
        ('A debit note is sent by the buyer to the supplier when goods are returned.', 'The buyer debits the supplier\'s account when goods are returned.', 'a', 'Both true and R explains A.'),
        ('A pay-in-slip is used to withdraw cash from a bank.', 'The counterfoil of a pay-in-slip is returned by the bank as proof.', 'd', 'A is false: a pay-in-slip is for deposits. R is true.')],
    tf=('source documents', [
        'A cash memo is issued by the seller for a cash sale.',
        'A credit note is sent by the seller to a customer for goods returned by him.',
        'Vouchers are the basis for recording transactions.'], [
        'An invoice is issued for every cash sale.',
        'A receipt is given by the person paying the money.',
        'A debit note is issued by the seller when he receives returned goods.',
        'A pay-in-slip is used to withdraw money from the bank.']),
    cases=[
        ('C4', 'D4', 4, 'During one day {f}, {c}: (a) sold {g} for ₹4,500 cash to a walk-in customer; (b) sold goods worth ₹36,000 to {f2} on credit; (c) returned defective goods worth ₹2,000 to its supplier; (d) deposited ₹20,000 in its bank account.',
         [('Name the source document for each of (a) to (d).', '(a) Cash memo (b) Invoice (bill) (c) Debit note (d) Pay-in-slip (counterfoil).'),
          ('Who prepares the document in (b) and (c)?', '(b) The seller, {f}; (c) the buyer, {f}, sends it to the supplier.')]),
        ('C4', 'D3', 4, 'The accountant of {f} prepares vouchers for: (a) payment of ₹8,000 rent in cash; (b) cash of ₹12,000 received from a customer; (c) credit purchase of a machine from {f2}; (d) salary paid partly in cash and partly by cheque.',
         [('Identify the type of voucher for each.', '(a) Debit (cash payment) voucher (b) Credit (cash receipt) voucher (c) Transfer voucher (d) Complex (compound) voucher.'),
          ('Why are vouchers needed at all?', 'They are documentary evidence supporting each entry, needed for checking and audit.')]),
        ('C4', 'D5', 4, '{p}, who runs {f}, does not issue cash memos for cash sales because "customers never ask for them". At the year end the tax officer questions the sales figure.',
         [('What problem does the lack of source documents create?', 'Sales cannot be verified; the records lose objectivity and reliability, and are not acceptable evidence for tax.'),
          ('Advise {p} on two practices to follow.', 'Issue a serially numbered cash memo for every cash sale; file all vouchers date-wise and record entries only from vouchers.')])],
)


# ---------------- ch03 st2 accounting equation

def c3s2_capital(r):
    a = amt(r, 200000, 2000000, 5000)
    l = amt(r, 20000, a // 2, 5000)
    v = r.choice(['c', 'a', 'l'])
    c = a - l
    if v == 'c':
        return {'stem': f'Total assets of a business are {inr(a)} and outside liabilities are {inr(l)}. Find the capital using the accounting equation.',
                'answer': inr(c), 'key': f'Capital = Assets − Liabilities = {inr(a)} − {inr(l)} = {inr(c)}.', 'distractors': [inr(a + l), inr(l), inr(a)]}
    if v == 'a':
        return {'stem': f'The capital of a business is {inr(c)} and its liabilities are {inr(l)}. Find its total assets.',
                'answer': inr(a), 'key': f'Assets = Liabilities + Capital = {inr(l)} + {inr(c)} = {inr(a)}.', 'distractors': [inr(c - l), inr(c), inr(a + l)]}
    return {'stem': f'Total assets of a business are {inr(a)} and the owner\'s capital is {inr(c)}. Find its liabilities.',
            'answer': inr(l), 'key': f'Liabilities = Assets − Capital = {inr(a)} − {inr(c)} = {inr(l)}.', 'distractors': [inr(a + c), inr(c), inr(a)]}


EFFECTS = {(1, 1, 0): 'Increase in assets and increase in liabilities', (1, 0, 1): 'Increase in assets and increase in capital',
           (-1, -1, 0): 'Decrease in assets and decrease in liabilities', (-1, 0, -1): 'Decrease in assets and decrease in capital',
           (0, 0, 0): 'Change in the form of assets only (no change in totals)'}


def _sgn(x):
    return (x > 0) - (x < 0)


def c3s2_effect(r):
    for _ in range(30):
        t, d = txn(r, EQ_TXNS)
        e = tuple(_sgn(x) for x in t['eq'])
        if e in EFFECTS:
            break
    else:
        raise ValueError
    good = EFFECTS[e]
    wrong = [v for k, v in EFFECTS.items() if k != e]
    return mcq(f'What is the effect on the accounting equation of the transaction: "{t["eqtext"]}"?', good, r.sample(wrong, 3),
               f'Assets {"+" if t["eq"][0] >= 0 else "−"}{inr(abs(t["eq"][0]))}, liabilities {"+" if t["eq"][1] >= 0 else "−"}{inr(abs(t["eq"][1]))}, capital {"+" if t["eq"][2] >= 0 else "−"}{inr(abs(t["eq"][2]))}.', r)


EQ_OUT = (t_pay_creditor_disc, t_recv_debtor_disc, t_bad_debt, t_pay_creditor_cheque, t_recv_cheque_deposit, t_purch_return, t_capital_cash, t_capital_bank)
GOODS_OUT = ('sale', 'drawings', 'loss')


def _eq_seq(r, n):
    d = ctx(r)
    first = r.choice([t_capital_cash, t_capital_bank])(r, d)
    big = amt(r, 100000, 250000, 5000)
    second = r.choice([
        _t(f'Purchased goods for cash {inr(big)}', [('Purchases A/c', big, 'expense')], [('Cash A/c', big, 'asset')], (0, 0, 0), 'Cash Book', [('cash', -big)]),
        _t(f'Purchased goods on credit from {d["f2"]} {inr(big)}', [('Purchases A/c', big, 'expense')], [(pa(d['f2']), big, 'liability')], (big, big, 0), 'Purchases Book')])
    seq = [first, second]
    used = {first['eqtext'], second['eqtext']}
    kinds = set()
    pool = [t for t in EQ_TXNS if t not in EQ_OUT]
    guard = 0
    while len(seq) < n:
        guard += 1
        if guard > 100:
            raise ValueError
        t = r.choice(pool)(r, d)
        if t['eqtext'] in used or t['text'].split(' ')[0] + t['kind'] in kinds:
            continue
        seq.append(t)
        used.add(t['eqtext'])
        kinds.add(t['text'].split(' ')[0] + t['kind'])
    A = sum(t['eq'][0] for t in seq)
    L = sum(t['eq'][1] for t in seq)
    C = sum(t['eq'][2] for t in seq)
    if A <= 0 or C <= 0 or L < 0:
        raise ValueError
    return d, seq, A, L, C


def c3s2_sequence(r):
    n = 4
    d, seq, A, L, C = _eq_seq(r, n)
    lines = ' '.join(f'({i + 1}) {t["eqtext"]}.' for i, t in enumerate(seq))
    steps = '; '.join(f'({i + 1}) A {num_s(t["eq"][0])}, L {num_s(t["eq"][1])}, C {num_s(t["eq"][2])}' for i, t in enumerate(seq))
    return {'stem': f'Show the accounting equation on the basis of the following transactions of {d["p"]}: {lines} Find the final assets, liabilities and capital.',
            'answer': f'Assets {inr(A)} = Liabilities {inr(L)} + Capital {inr(C)}',
            'key': f'Changes: {steps}. Totals: Assets {inr(A)} = Liabilities {inr(L)} + Capital {inr(C)} (¾ mark per transaction, 1 mark for the final equation).'}


def num_s(x):
    return ('+' if x >= 0 else '−') + inr(abs(x))[1:] if x else '0'


def c3s2_sequence6(r):
    d, seq, A, L, C = _eq_seq(r, 6)
    lines = ' '.join(f'({i + 1}) {t["eqtext"]}.' for i, t in enumerate(seq))
    steps = '; '.join(f'({i + 1}) A {num_s(t["eq"][0])}, L {num_s(t["eq"][1])}, C {num_s(t["eq"][2])}' for i, t in enumerate(seq))
    return {'stem': f'Prepare the accounting equation for the business of {d["p"]}, {d["c"]}, showing the effect of each transaction, and give the balance sheet totals at the end: {lines}',
            'answer': f'Assets {inr(A)} = Liabilities {inr(L)} + Capital {inr(C)}; balance sheet total {inr(A)}',
            'key': f'Changes (rupees): {steps}. Final: Assets {inr(A)} = Liabilities {inr(L)} + Capital {inr(C)} (5 marks for the six effects, 1 mark for the final equation).'}


def c3s2_missing(r):
    d = ctx(r)
    cap = amt(r, 200000, 600000, 10000)
    cred = amt(r, 40000, 150000, 1000)
    cost = amt(r, 20000, cred - 5000, 1000)
    sp = cost + amt(r, 5000, 40000, 1000)
    drw = amt(r, 5000, 20000, 1000)
    A = cap + cred + (sp - cost) - drw
    C = cap + sp - cost - drw
    return {'stem': f'{d["p"]} started business with cash {inr(cap)}, bought goods on credit for {inr(cred)}, sold goods costing {inr(cost)} for {inr(sp)} in cash and withdrew {inr(drw)} for personal use. Without listing every step, find the capital at the end and explain why total assets rose by more than capital.',
            'answer': f'Capital {inr(C)}; assets {inr(A)}, liabilities {inr(cred)}',
            'key': f'Capital = {inr(cap)} + profit {inr(sp - cost)} − drawings {inr(drw)} = {inr(C)} (2). Assets = {inr(C)} + creditors {inr(cred)} = {inr(A)}; the credit purchase raised assets and liabilities equally without changing capital (1).'}


def c3s2_which(r):
    good = r.choice([
        ('Purchased goods on credit', 'Increase in assets and increase in liabilities'),
        ('Paid a creditor in cash', 'Decrease in assets and decrease in liabilities'),
        ('Paid salaries in cash', 'Decrease in assets and decrease in capital'),
        ('Introduced additional capital in cash', 'Increase in assets and increase in capital'),
        ('Purchased furniture for cash', 'Change in the form of assets only (no change in totals)'),
        ('Received commission in cash', 'Increase in assets and increase in capital'),
        ('Took a bank loan', 'Increase in assets and increase in liabilities'),
        ('Deposited cash into bank', 'Change in the form of assets only (no change in totals)')])
    others = [x for x in ['Purchased goods on credit', 'Paid a creditor in cash', 'Paid salaries in cash', 'Introduced additional capital in cash',
                          'Purchased furniture for cash', 'Received commission in cash', 'Took a bank loan', 'Deposited cash into bank']
              if x != good[0] and _eff_of(x) != good[1]]
    return mcq(f'Which of the following transactions results in: {good[1].lower()}?', good[0], r.sample(others, 3), f'{good[0]}: {good[1].lower()}.', r)


def _eff_of(x):
    return {'Purchased goods on credit': 'Increase in assets and increase in liabilities', 'Paid a creditor in cash': 'Decrease in assets and decrease in liabilities',
            'Paid salaries in cash': 'Decrease in assets and decrease in capital', 'Introduced additional capital in cash': 'Increase in assets and increase in capital',
            'Purchased furniture for cash': 'Change in the form of assets only (no change in totals)', 'Received commission in cash': 'Increase in assets and increase in capital',
            'Took a bank loan': 'Increase in assets and increase in liabilities', 'Deposited cash into bank': 'Change in the form of assets only (no change in totals)'}[x]


CH03_ST2_FACTS = dict(
    ars=[
        ('Purchase of furniture for cash does not change the total of assets.', 'One asset increases and another asset decreases by the same amount.', 'a', 'Both true and R explains A.'),
        ('Payment of salary reduces capital.', 'Expenses reduce the owner\'s equity.', 'a', 'Both true and R explains A.'),
        ('Purchase of goods on credit increases capital.', 'Purchase of goods on credit increases assets and liabilities.', 'd', 'A is false; R is true.'),
        ('The accounting equation is based on the dual aspect concept.', 'Every transaction has two aspects of equal amount.', 'a', 'Both true and R explains A.'),
        ('Drawings reduce both assets and capital.', 'Drawings are an expense of the business.', 'c', 'A is true. R is false: drawings are not a business expense; they are a withdrawal of capital.')],
    tf=('the accounting equation', [
        'Assets = Liabilities + Capital at all times.',
        'Sale of goods at a profit increases capital by the amount of profit.',
        'Payment to a creditor reduces assets and liabilities.'], [
        'Purchase of machinery on credit reduces capital.',
        'Withdrawal of cash for personal use increases liabilities.',
        'Receipt of commission reduces capital.',
        'Capital = Assets + Liabilities.']),
)


# ---------------- ch03 st3 rules of debit and credit

DEBIT_RULES = ['Increase in assets', 'Decrease in liabilities', 'Decrease in capital', 'Increase in expenses', 'Decrease in revenues']
CREDIT_RULES = ['Decrease in assets', 'Increase in liabilities', 'Increase in capital', 'Decrease in expenses', 'Increase in revenues']


def c3s3_rule(r):
    side = r.choice(['debit', 'credit'])
    good = r.choice(DEBIT_RULES if side == 'debit' else CREDIT_RULES)
    wrong = r.sample(CREDIT_RULES if side == 'debit' else DEBIT_RULES, 3)
    return mcq(f'Under the modern (accounting equation) approach, which of the following is recorded on the {side} side of an account?', good, wrong,
               f'Debit: increase in assets/expenses, decrease in liabilities/capital/revenues; credit: the reverse. "{good}" is a {side}.', r)


def _treat(side, nat):
    inc = {('dr', 'asset'): True, ('cr', 'asset'): False, ('dr', 'expense'): True, ('cr', 'expense'): False,
           ('dr', 'liability'): False, ('cr', 'liability'): True, ('dr', 'capital'): False, ('cr', 'capital'): True,
           ('dr', 'revenue'): False, ('cr', 'revenue'): True}[(side, nat)]
    word = {'asset': 'assets', 'expense': 'expenses', 'liability': 'liabilities', 'capital': 'capital', 'revenue': 'revenues'}[nat]
    return f'{"Debited" if side == "dr" else "Credited"}, as an {"increase" if inc else "decrease"} in {word}'.replace('an decrease', 'a decrease')


ALL_TREAT = [_treat(s, n) for s in ('dr', 'cr') for n in ('asset', 'expense', 'liability', 'capital', 'revenue')]


def c3s3_treatment(r):
    for _ in range(30):
        t, d = txn(r)
        cands = [('dr', a, n) for a, x, n in t['dr']] + [('cr', a, n) for a, x, n in t['cr']]
        cands = [c for c in cands if not (c[1] in ('Purchases A/c', 'Purchases Return A/c', 'Sales Return A/c') and t['kind'] in ('drawings', 'loss', 'return'))]
        if cands:
            break
    side, a, n = r.choice(cands)
    good = _treat(side, n)
    oside = 'cr' if side == 'dr' else 'dr'
    others = [_treat(side, m) for m in NATS if m != n] + [_treat(oside, m) for m in NATS if m != n]
    pick = [_treat(oside, n)] + r.sample(others, 2)
    return mcq(f'Transaction: "{t["text"]}". Under the modern approach, how is {a} treated?', good, pick,
               f'Entry: {je(t)}. {a} is {good[0].lower() + good[1:]}.', r)


NATS = ('asset', 'expense', 'liability', 'capital', 'revenue')


def c3s3_analyse(r):
    t1, d = txn(r)
    t2 = r.choice(TXNS)(r, d)
    if t2['text'] == t1['text']:
        raise ValueError

    def rows(t):
        return '; '.join([f'{a}: {n}, {_treat("dr", n).lower()}' for a, x, n in t['dr']] + [f'{a}: {n}, {_treat("cr", n).lower()}' for a, x, n in t['cr']])
    return {'stem': f'Analyse the following transactions under the modern approach: state the accounts affected, the nature of each account and whether it is debited or credited. (i) {t1["text"]}. (ii) {t2["text"]}.',
            'answer': f'(i) {rows(t1)} (ii) {rows(t2)}',
            'key': f'(i) {rows(t1)} [entry: {je(t1)}] (ii) {rows(t2)} [entry: {je(t2)}]. 1½ marks per transaction.'}


def c3s3_nature(r):
    items = [('Cash', 'Asset'), ('Machinery', 'Asset'), ('Debtors', 'Asset'), ('Bills receivable', 'Asset'), ('Creditors', 'Liability'), ('Bills payable', 'Liability'),
             ('Bank loan', 'Liability'), ('Outstanding salary', 'Liability'), ('Drawings', 'Capital'), ('Rent paid', 'Expense'),
             ('Wages', 'Expense'), ('Discount allowed', 'Expense'), ('Bad debts', 'Expense'), ('Sales', 'Revenue'), ('Commission received', 'Revenue'),
             ('Discount received', 'Revenue'), ('Interest received', 'Revenue'), ('Purchases', 'Expense'), ('Insurance premium', 'Expense')]
    it, nat = r.choice(items)
    opts = ['Asset', 'Liability', 'Capital', 'Expense', 'Revenue']
    key = f'{it} is classified as {nat.lower()} under the accounting equation approach.' + (' (Drawings reduce capital.)' if it == 'Drawings' else '')
    return mcq(f'Under the accounting equation approach, "{it}" account is classified as …', nat, r.sample([o for o in opts if o != nat], 3), key, r)


CH03_ST3_FACTS = dict(
    ars=[
        ('An increase in an asset is debited.', 'Assets are on the left-hand side of the accounting equation.', 'a', 'Both true; debit is the left side, which is why increases in assets are debited.'),
        ('Drawings account is debited when the owner withdraws cash.', 'Drawings reduce the capital of the owner.', 'a', 'Both true and R explains A.'),
        ('Discount received is debited.', 'Discount received is a revenue.', 'd', 'A is false: an increase in revenue is credited. R is true.'),
        ('Expenses are debited.', 'Expenses reduce capital, and a decrease in capital is debited.', 'a', 'Both true and R explains A.'),
        ('A decrease in liabilities is credited.', 'Liabilities appear on the right-hand side of the accounting equation.', 'd', 'A is false: a decrease in liabilities is debited. R is true.')],
    tf=('rules of debit and credit', [
        'An increase in revenue is recorded on the credit side.',
        'A decrease in assets is recorded on the credit side.',
        'An increase in expenses is recorded on the debit side.'], [
        'An increase in liabilities is recorded on the debit side.',
        'An increase in capital is recorded on the debit side.',
        'A decrease in expenses is recorded on the debit side.',
        'Drawings are credited when the owner withdraws cash.']),
)


# ---------------- ch03 st4 journal

def c3s4_entry_mcq(r):
    t, d = txn(r)
    good = je(t)
    wrong = []
    swap = entry(strip(t['cr']), strip(t['dr']))
    for dr, cr in t['alts']:
        e = entry(dr, cr)
        if e != good and e not in wrong:
            wrong.append(e)
    if swap != good and swap not in wrong:
        wrong.append(swap)
    if len(wrong) < 3:
        raise ValueError
    return mcq(f'Which journal entry correctly records the following transaction? "{t["text"]}."', good, r.sample(wrong, 3), f'{good}.', r)


def _journalise(r, n, pool=None):
    d = ctx(r)
    seen, ts = set(), []
    while len(ts) < n:
        t = r.choice(pool or TXNS)(r, d)
        if t['kind'] in {x['kind'] for x in ts} and r.random() < 0.7:
            continue
        if t['text'] in seen:
            continue
        seen.add(t['text'])
        ts.append(t)
    ts.sort(key=lambda t: t['kind'] != 'capital')
    days = sorted(r.sample(range(1, 29), n))
    mon = r.choice(MONTHS)
    lines = ' '.join(f'{mon} {dd}: {t["text"]}.' for dd, t in zip(days, ts))
    ans = ' '.join(f'({i + 1}) {je(t)}.' for i, t in enumerate(ts))
    return d, lines, ans, ts


def c3s4_journalise3(r):
    d, lines, ans, ts = _journalise(r, 3)
    return {'stem': f'Journalise the following transactions in the books of {d["f"]}, {d["c"]}, for 2025: {lines}', 'answer': ans,
            'key': f'1 mark per correct entry (narration expected): {ans}'}


def c3s4_journalise4(r):
    d, lines, ans, ts = _journalise(r, 4)
    return {'stem': f'Pass journal entries for the following transactions of {d["p"]}, {d["c"]}: {lines}', 'answer': ans,
            'key': f'1 mark per correct entry: {ans}'}


HARD = [t_pay_creditor_disc, t_recv_debtor_disc, t_fire, t_samples, t_gst_purchase, t_gst_sale_inter, t_bad_debt, t_drawings_goods, t_trade_disc,
        t_life_premium, t_machinery_credit]


def c3s4_journalise6(r):
    d, lines, ans, ts = _journalise(r, 6, HARD + [t_capital_bank, t_loan, t_purch_credit, t_sale_credit])
    return {'stem': f'Journalise the following transactions in the books of {d["f"]}, {d["c"]} (GST where stated): {lines}', 'answer': ans,
            'key': f'1 mark per correct entry (compound and GST entries must balance): {ans}'}


def c3s4_hard_one(r):
    t, d = txn(r, HARD)
    return {'stem': f'Pass the journal entry for: "{t["text"]}". Give a reason for each account debited or credited.', 'answer': je(t),
            'key': f'{je(t)}. ' + '; '.join([f'{a} debited ({_treat("dr", n).split(", as ")[1]})' for a, x, n in t['dr']] + [f'{a} credited ({_treat("cr", n).split(", as ")[1]})' for a, x, n in t['cr']]) + '.',
            'gap': 'G3'}


def c3s4_compound_amount(r):
    t, d = txn(r, [t_pay_creditor_disc, t_recv_debtor_disc, t_bad_debt])
    acc_ = [a for a, x, n in t['dr'] + t['cr'] if a in ('Discount Received A/c', 'Discount Allowed A/c', 'Bad Debts A/c')][0]
    val = [x for a, x, n in t['dr'] + t['cr'] if a == acc_][0]
    others = [inr(val * 2), inr(val + 500), inr([x for a, x, n in t['dr'] + t['cr'] if a not in (acc_,)][0])]
    return {'stem': f'"{t["text"]}." By what amount is {acc_} affected in the journal entry?', 'answer': inr(val),
            'key': f'Entry: {je(t)}; {acc_} {inr(val)}.', 'distractors': others}


CH03_ST4_FACTS = dict(
    terms=[('Journal', 'The book of original entry in which transactions are first recorded in chronological order, showing the accounts to be debited and credited.'),
           ('Narration', 'A brief explanation of the transaction written below each journal entry.'),
           ('Compound entry', 'A journal entry in which more than one account is debited or credited.'),
           ('Journalising', 'The process of recording transactions in the journal.'),
           ('Ledger folio (L.F.)', 'The column of the journal in which the page number of the ledger account to which the entry is posted is written.')],
    cat='term',
    ars=[
        ('Goods withdrawn by the proprietor for personal use are credited to the Purchases account.', 'Such goods are no longer available for sale, so purchases are reduced.', 'a', 'Both true and R explains A.'),
        ('Goods distributed as free samples are debited to the Advertisement account.', 'Free samples are given to promote sales.', 'a', 'Both true and R explains A.'),
        ('Trade discount is recorded in the journal.', 'Purchases are recorded at the net amount after trade discount.', 'd', 'A is false; R is true.'),
        ('Input CGST is debited on purchase of goods.', 'Input CGST is a liability of the business.', 'c', 'A is true. R is false: input tax is an asset (credit receivable).'),
        ('Loss of goods by fire is credited to the Purchases account.', 'Goods destroyed are no longer available for sale.', 'a', 'Both true and R explains A.')],
    tf=('the journal', [
        'The journal records transactions in chronological order.',
        'A compound entry has more than one debit or more than one credit.',
        'Each journal entry should be followed by a narration.'], [
        'Trade discount is recorded in the journal.',
        'The journal is a book of final entry.',
        'In a journal entry the credit account is written first.',
        'Goods withdrawn for personal use are credited to the Sales account.']),
)


# ---------------- ch03 st5 ledger

def c3s5_cash_account(r):
    d = ctx(r)
    pool = [t_capital_cash, t_sale_cash, t_purch_cash, t_rent, t_wages, t_commission, t_drawings_cash, t_deposit, t_furniture_cash, t_recv_debtor_disc, t_pay_creditor_disc]
    ts = [t_capital_cash(r, d)]
    seen = {ts[0]['text']}
    while len(ts) < 6:
        t = r.choice(pool[1:])(r, d)
        if t['text'] not in seen:
            ts.append(t)
            seen.add(t['text'])
    dr_ = sum(x for t in ts for col, x in t['cash'] if col == 'cash' and x > 0)
    cr_ = -sum(x for t in ts for col, x in t['cash'] if col == 'cash' and x < 0)
    bal = dr_ - cr_
    if bal <= 0:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t["text"]}.' for i, t in enumerate(ts))
    return {'stem': f'Prepare the Cash Account of {d["f"]} from the following and find its balance: {lines}',
            'answer': f'Debit total {inr(dr_)}, credit items {inr(cr_)}; balance c/d {inr(bal)} (debit balance)',
            'key': f'Debit side (receipts) {inr(dr_)}; credit side (payments) {inr(cr_)}; Balance c/d {inr(bal)} written on the credit side; cash account shows a debit balance of {inr(bal)}.',
            'distractors': [inr(dr_ + cr_), inr(cr_), inr(dr_)]}


def c3s5_personal(r):
    d = ctx(r)
    c = d['p2']
    s1 = amt(r, 20000, 80000, 500)
    s2 = amt(r, 10000, 50000, 500)
    ret = amt(r, 1000, 5000, 500)
    recv = amt(r, 10000, s1 - 1000, 500)
    dis = amt(r, 100, 800, 50)
    bal = s1 + s2 - ret - recv - dis
    m = r.sample(MONTHS[:6], 4)
    m.sort(key=MONTHS.index)
    return {'stem': f'Prepare {c}\'s account in the books of {d["f"]}: {m[0]} 5: sold goods to {c} {inr(s1)}; {m[1]} 8: {c} returned goods {inr(ret)}; {m[2]} 12: received cash {inr(recv)} from {c} and allowed discount {inr(dis)}; {m[3]} 20: sold goods to {c} {inr(s2)}. Find the balance and state what it means.',
            'answer': f'Debit balance {inr(bal)}: {c} owes {inr(bal)} to the firm',
            'key': f'Debit: sales {inr(s1)} + {inr(s2)} = {inr(s1 + s2)}; credit: returns {inr(ret)}, cash {inr(recv)}, discount {inr(dis)} = {inr(ret + recv + dis)}; balance c/d {inr(bal)} (debit balance, {c} is a debtor).'}


def c3s5_balance_meaning(r):
    good = r.choice([
        ('A debit balance in a customer\'s account', 'The customer owes money to the business'),
        ('A credit balance in a supplier\'s account', 'The business owes money to the supplier'),
        ('A debit balance in the cash account', 'Cash in hand'),
        ('A credit balance in the capital account', 'Amount owed by the business to the owner'),
        ('A credit balance in the bank account (cash book)', 'Bank overdraft')])
    pool = ['The customer owes money to the business', 'The business owes money to the supplier', 'Cash in hand', 'Amount owed by the business to the owner', 'Bank overdraft']
    return mcq(f'{good[0]} indicates …', good[1], r.sample([p for p in pool if p != good[1]], 3), f'{good[0]} means: {good[1].lower()}.', r)


def c3s5_post(r):
    t, d = txn(r, SIMPLE)
    (da, dx, _), (ca, cx, _) = t['dr'][0], t['cr'][0]
    good = f'Debit side of {da} as "To {ca[:-4] if ca.endswith(" A/c") else ca}"; credit side of {ca} as "By {da[:-4] if da.endswith(" A/c") else da}"'
    wrong = [f'Debit side of {ca} as "To {da[:-4]}"; credit side of {da} as "By {ca[:-4]}"',
             f'Debit side of both {da} and {ca}',
             f'Credit side of {da} as "By {ca[:-4]}"; debit side of {ca} as "To {da[:-4]}"']
    if len({good, *wrong}) < 4:
        raise ValueError
    return mcq(f'The entry "{je(t)}" is posted to the ledger on the …', good, wrong, f'In the debit account the credit account\'s name is written with "To"; in the credit account the debit account\'s name with "By".', r)


CH03_ST5_FACTS = dict(
    terms=[('Ledger', 'The principal book of account in which all accounts of a business are kept, each showing its transactions classified at one place.'),
           ('Posting', 'The process of transferring entries from the journal to the respective accounts in the ledger.'),
           ('Balancing an account', 'Finding the difference between the totals of the two sides of an account and writing it on the shorter side.'),
           ('Balance c/d', 'The difference written on the shorter side of an account at the end of the period to make both sides equal.'),
           ('Balance b/d', 'The closing balance brought down to the opposite side as the opening balance of the next period.')],
    cat='ledger term',
    ars=[
        ('The ledger is called the principal book of account.', 'Final accounts are prepared from the balances of ledger accounts.', 'a', 'Both true and R explains A.'),
        ('Nominal accounts are not balanced but closed by transfer to the trading or profit and loss account.', 'Expense and revenue accounts relate to a single accounting period.', 'a', 'Both true and R explains A.'),
        ('A cash account can show a credit balance.', 'Payments of cash cannot exceed cash available.', 'd', 'A is false; R is true.'),
        ('Posting is done from the ledger to the journal.', 'The journal is the book of original entry.', 'd', 'A is false: posting is from the journal to the ledger. R is true.')],
    tf=('the ledger', [
        'The ledger is the book of final entry.',
        'The balance of an account is written on the shorter side as balance c/d.',
        'Expense accounts are closed by transfer to the trading or profit and loss account.'], [
        'Posting means writing transactions in the journal.',
        'A debit balance in a supplier\'s account means the business owes him money.',
        'The cash account can show a credit balance.',
        'Balance b/d is written on the same side as balance c/d.']),
)


def _f(spec):
    return facts(spec)


FAMILIES = {
    S + '03-st1': _f(CH03_ST1) + [FF('C2', 'D2', 'mcq', lambda r: _book_doc(r))],
    S + '03-st2': _f(CH03_ST2_FACTS) + [FF('C3', 'D1', 'numerical', c3s2_capital, marks=1), FF('C2', 'D2', 'mcq', c3s2_effect), FF('C2', 'D2', 'mcq', c3s2_which),
                                        FF('C3', 'D3', 'multi_step', c3s2_sequence, marks=4, kinds=('m4',)), FF('C3', 'D4', 'long', c3s2_sequence6, marks=6, kinds=('m6',)),
                                        FF('C4', 'D4', 'multi_step', c3s2_missing, marks=3, kinds=('m3',)), FF('C1', 'D2', 'mcq', c3s2_effect),
                                        FF('C4', 'D3', 'multi_step', c3s2_sequence, marks=4)],
    S + '03-st3': _f(CH03_ST3_FACTS) + [FF('C1', 'D1', 'mcq', c3s3_rule), FF('C1', 'D2', 'mcq', c3s3_nature), FF('C2', 'D2', 'mcq', c3s3_treatment),
                                        FF('C3', 'D3', 'mcq', c3s3_treatment), FF('C3', 'D3', 'explain', c3s3_analyse, marks=3, kinds=('m3',)),
                                        FF('C4', 'D4', 'explain', c3s3_analyse, marks=3), FF('C2', 'D1', 'mcq', c3s3_nature)],
    S + '03-st4': _f(CH03_ST4_FACTS) + [FF('C2', 'D2', 'mcq', c3s4_entry_mcq), FF('C3', 'D2', 'mcq', c3s4_entry_mcq), FF('C3', 'D3', 'multi_step', c3s4_journalise3, marks=3, kinds=('m3',)),
                                        FF('C3', 'D4', 'multi_step', c3s4_journalise4, marks=4, kinds=('m4',)), FF('C4', 'D4', 'long', c3s4_journalise6, marks=6, kinds=('m6',)),
                                        FF('C4', 'D3', 'explain', c3s4_hard_one, marks=2), FF('C3', 'D1', 'short', c3s4_compound_amount, marks=1),
                                        FF('C4', 'D5', 'long', c3s4_journalise6, marks=6)],
    S + '03-st5': _f(CH03_ST5_FACTS) + [FF('C3', 'D3', 'multi_step', c3s5_cash_account, marks=4, kinds=('m4',)), FF('C3', 'D3', 'multi_step', c3s5_personal, marks=3, kinds=('m3',)),
                                        FF('C2', 'D1', 'mcq', c3s5_balance_meaning), FF('C2', 'D2', 'mcq', c3s5_post), FF('C4', 'D4', 'multi_step', c3s5_personal, marks=3),
                                        FF('C3', 'D2', 'numerical', c3s5_cash_account, marks=4)],
}


def _book_doc(r):
    pairs = [('a cash sale', 'Cash memo'), ('a credit sale', 'Invoice (bill)'), ('a deposit of cash into the bank', 'Pay-in-slip'),
             ('goods returned to a supplier', 'Debit note'), ('goods returned by a customer', 'Credit note'), ('cash received from a customer, as proof given to the customer', 'Receipt')]
    a, b = r.choice(pairs)
    return mcq(f'Which source document normally supports {a}?', b, r.sample([x for x in DOCS if x != b], 3), f'{a[0].upper() + a[1:]}: {b}.', r)


# ---------------- ch04 Recording of Transactions II

CASH_ONLY = [t_sale_cash, t_purch_cash, t_rent, t_wages, t_salary, t_commission, t_drawings_cash, t_furniture_cash, t_recv_debtor_disc, t_pay_creditor_disc,
             t_charity, t_add_capital, t_stationery, t_life_premium, t_bad_debt]
NON_CASH = [t_purch_credit, t_sale_credit, t_drawings_goods, t_machinery_credit, t_samples, t_fire, t_purch_return, t_sales_return, t_trade_disc]


def _cash_seq(r, n, pool, d):
    if n > len(pool):
        raise ValueError
    return [f(r, d) for f in r.sample(pool, n)]


def _col(ts, col):
    rec = sum(x for t in ts for c, x in t['cash'] if c == col and x > 0)
    pay = -sum(x for t in ts for c, x in t['cash'] if c == col and x < 0)
    return rec, pay


def c4s1_balance(r):
    d = ctx(r)
    op = amt(r, 10000, 80000, 500)
    ts = _cash_seq(r, 6, CASH_ONLY, d)
    rec, pay = _col(ts, 'cash')
    bal = op + rec - pay
    if bal <= 0:
        raise ValueError
    mon = r.choice(MONTHS)
    days = sorted(r.sample(range(2, 29), 6))
    lines = ' '.join(f'{mon} {dd}: {t["text"]}.' for dd, t in zip(days, ts))
    return {'stem': f'Prepare a simple cash book of {d["f"]} for {mon} 2025: {mon} 1: cash in hand {inr(op)}. {lines} Find the closing cash balance.',
            'answer': f'Closing cash balance {inr(bal)}',
            'key': f'Debit (receipts) = opening {inr(op)} + {inr(rec)} = {inr(op + rec)}; credit (payments) = {inr(pay)}; balance c/d {inr(bal)}. Only the cash part of each transaction is entered (discount and bad debts are not cash).',
            'distractors': [inr(op + rec + pay), inr(rec - pay), inr(bal + op)]}


def c4s1_mixed(r):
    d = ctx(r)
    op = amt(r, 10000, 60000, 500)
    ts = _cash_seq(r, 5, CASH_ONLY, d) + _cash_seq(r, 2, NON_CASH, d)
    r.shuffle(ts)
    rec, pay = _col(ts, 'cash')
    bal = op + rec - pay
    if bal <= 0:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t["text"]}.' for i, t in enumerate(ts))
    skip = ', '.join(f'({i + 1})' for i, t in enumerate(ts) if not t['cash'])
    return {'stem': f'{d["p"]} has cash in hand of {inr(op)}. Record only what belongs in a simple cash book and find the closing balance: {lines}',
            'answer': f'Closing balance {inr(bal)}; items {skip} are not entered',
            'key': f'Items {skip} involve no cash and go to other books. Receipts {inr(rec)}, payments {inr(pay)}; balance = {inr(op)} + {inr(rec)} − {inr(pay)} = {inr(bal)}.'}


def c4s1_not_recorded(r):
    d = ctx(r)
    bad = r.choice(NON_CASH)(r, d)
    good = _cash_seq(r, 3, CASH_ONLY, d)
    return mcq('Which of the following transactions is NOT recorded in a simple (single column) cash book?', bad['text'], [t['text'] for t in good],
               f'"{bad["text"]}" involves no cash; it is recorded in the {bad["book"].lower()}.', r)


CH04_ST1_FACTS = dict(
    cat='term',
    terms=[('Cash book', 'A book of original entry in which all cash receipts are recorded on the debit side and all cash payments on the credit side.'),
           ('Simple cash book', 'A cash book with only one amount column on each side, recording cash transactions only.'),
           ('Cash in hand', 'The balance of the cash book on a date, always a debit balance.'),
           ('Cash transaction', 'A transaction in which cash is received or paid at the time it takes place.')],
    ars=[
        ('The cash book serves as both a journal and a ledger.', 'Cash transactions are first recorded in it and it also shows the cash account balance.', 'a', 'Both true and R explains A.'),
        ('A simple cash book can never show a credit balance.', 'Cash payments cannot exceed cash receipts plus the opening balance.', 'a', 'Both true and R explains A.'),
        ('Discount allowed is recorded in the amount column of a simple cash book.', 'Discount allowed does not involve the receipt or payment of cash.', 'd', 'A is false; R is true.'),
        ('When a cash book is kept, a separate cash account is not opened in the ledger.', 'The cash book itself works as the cash account.', 'a', 'Both true and R explains A.')],
    tf=('the simple cash book', [
        'Receipts are recorded on the debit side of the cash book.',
        'The cash book is both a book of original entry and a ledger account.',
        'Credit transactions are not recorded in the cash book.'], [
        'The cash book can have a credit balance.',
        'Credit purchases are recorded on the credit side of the cash book.',
        'A simple cash book has separate columns for cash and bank.',
        'Payments are recorded on the debit side of the cash book.']),
)

BANKY = [t_deposit, t_withdraw_office, t_purch_cheque, t_electricity, t_pay_creditor_cheque, t_recv_cheque_deposit, t_interest_loan, t_computer_cheque,
         t_sale_cash, t_purch_cash, t_rent, t_wages, t_commission, t_drawings_cash, t_recv_debtor_disc]


def c4s2_balance(r, n=6):
    for _ in range(30):
        try:
            return _c4s2(r, n)
        except ValueError:
            continue
    raise ValueError


def _c4s2(r, n):
    d = ctx(r)
    oc = amt(r, 10000, 50000, 500)
    ob = amt(r, 80000, 300000, 1000) if n <= 6 else amt(r, 200000, 500000, 5000)
    ts = _cash_seq(r, n, BANKY, d)
    if not any(t['contra'] for t in ts):
        ts[r.randrange(n)] = r.choice([t_deposit, t_withdraw_office])(r, d)
    rc, pc = _col(ts, 'cash')
    rb, pb = _col(ts, 'bank')
    c, b = oc + rc - pc, ob + rb - pb
    if c <= 0 or b <= 0:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t["text"]}.' for i, t in enumerate(ts))
    contra = ', '.join(f'({i + 1})' for i, t in enumerate(ts) if t['contra'])
    return {'stem': f'{d["f"]} had cash in hand {inr(oc)} and cash at bank {inr(ob)}. Prepare a double column (cash and bank) cash book from the following and find the closing balances: {lines}',
            'answer': f'Cash {inr(c)}, bank {inr(b)}',
            'key': f'Cash column: {inr(oc)} + {inr(rc)} − {inr(pc)} = {inr(c)}; bank column: {inr(ob)} + {inr(rb)} − {inr(pb)} = {inr(b)}. Contra entries {contra} are marked "C" in the L.F. column and appear on both sides.'}


def c4s2_long(r):
    q = c4s2_balance(r, 8)
    q['key'] += ' (4 marks for entries, 2 marks for balancing.)'
    return q


def c4s2_contra(r):
    d = ctx(r)
    good = r.choice([t_deposit, t_withdraw_office])(r, d)
    wrong = _cash_seq(r, 3, [t for t in BANKY if t not in (t_deposit, t_withdraw_office)], d)
    return mcq('Which of the following is a contra entry in a double column cash book?', good['text'], [t['text'] for t in wrong],
               f'"{good["text"]}" affects both the cash and the bank columns, so it is a contra entry marked "C".', r)


def c4s2_column(r):
    d = ctx(r)
    t = r.choice([t_recv_cheque_deposit, t_pay_creditor_cheque, t_electricity, t_deposit, t_withdraw_office, t_sale_cash, t_rent])(r, d)
    sides = []
    for c, x in t['cash']:
        sides.append(f'{"debit" if x > 0 else "credit"} side, {c} column')
    good = ' and '.join(sides)
    allopts = ['debit side, cash column', 'credit side, cash column', 'debit side, bank column', 'credit side, bank column',
               'credit side, cash column and debit side, bank column', 'debit side, cash column and credit side, bank column']
    wrong = [o for o in allopts if o != good]
    return mcq(f'In a double column cash book, "{t["text"]}" is recorded on the …', good, r.sample(wrong, 3), f'{t["text"]}: {good}.', r)


CH04_ST2_FACTS = dict(
    cat='term',
    terms=[('Double column cash book', 'A cash book with separate amount columns for cash and bank on each side.'),
           ('Contra entry', 'An entry affecting both the cash and the bank columns, such as depositing cash into the bank or withdrawing cash from the bank for office use.'),
           ('Bank overdraft', 'A credit balance in the bank column, showing that the business has drawn more than the amount deposited.'),
           ('Letter "C" in the L.F. column', 'The mark written against a contra entry to show that no posting to the ledger is needed.')],
    ars=[
        ('Depositing cash into the bank is a contra entry.', 'It is recorded on both sides of the cash book.', 'a', 'Both true and R explains A.'),
        ('The bank column of the cash book may show a credit balance.', 'A business may withdraw more than its deposit under an overdraft arrangement.', 'a', 'Both true and R explains A.'),
        ('Contra entries are posted to the ledger.', 'Both aspects of a contra entry are already in the cash book.', 'd', 'A is false: no posting is needed. R is true.'),
        ('A cheque received and deposited the same day is entered in the bank column.', 'The cheque is converted into a bank balance immediately.', 'a', 'Both true and R explains A.')],
    tf=('the double column cash book', [
        'The bank column of a cash book may show a credit balance, called an overdraft.',
        'Contra entries are marked with the letter C.',
        'Withdrawal of cash from bank for office use is a contra entry.'], [
        'The cash column can show a credit balance.',
        'Withdrawal of cash for personal use is a contra entry.',
        'Contra entries are posted to the ledger in both accounts.',
        'A cheque received and deposited the same day is entered in the cash column.']),
)

PETTY = [('postage', 'Postage'), ('stationery', 'Stationery'), ('auto fare (conveyance)', 'Conveyance'), ('cartage', 'Cartage'),
         ('tea and refreshments for staff', 'Sundries'), ('courier charges', 'Postage'), ('photocopying', 'Stationery'), ('taxi fare', 'Conveyance'),
         ('cleaning charges', 'Sundries'), ('speed post stamps', 'Postage')]


def _petty(r, n):
    items = r.sample(PETTY, n)
    return [(lbl, head, r.randrange(4, 60) * 10) for lbl, head in items]


def c4s3_imprest(r):
    d = ctx(r)
    imp = r.choice([3000, 4000, 5000, 6000, 8000, 10000])
    ex = _petty(r, 5)
    tot = sum(x for _, _, x in ex)
    if tot >= imp:
        raise ValueError
    lines = '; '.join(f'{lbl} {inr(x)}' for lbl, _, x in ex)
    return {'stem': f'The petty cashier of {d["f"]} is given an imprest of {inr(imp)} for the month. Payments: {lines}. How much will the head cashier pay him at the end of the month to restore the imprest?',
            'answer': inr(tot), 'key': f'Under the imprest system the amount spent is reimbursed: {inr(tot)}; balance in hand {inr(imp - tot)} + {inr(tot)} = imprest {inr(imp)}.',
            'distractors': [inr(imp - tot), inr(imp), inr(imp + tot)]}


def c4s3_analysis(r):
    d = ctx(r)
    imp = r.choice([5000, 6000, 8000, 10000])
    ex = _petty(r, 7)
    tot = sum(x for _, _, x in ex)
    if tot >= imp:
        raise ValueError
    heads = {}
    for _, h, x in ex:
        heads[h] = heads.get(h, 0) + x
    lines = '; '.join(f'{lbl} {inr(x)}' for lbl, _, x in ex)
    cols = ', '.join(f'{h} {inr(v)}' for h, v in sorted(heads.items()))
    return {'stem': f'Prepare an analytical petty cash book of {d["f"]} with columns for postage, stationery, conveyance, cartage and sundries. Imprest {inr(imp)}. Payments: {lines}. Give the column totals, the total spent and the closing balance.',
            'answer': f'{cols}; total {inr(tot)}; balance {inr(imp - tot)}',
            'key': f'Column totals: {cols} (2); total spent {inr(tot)}, balance c/d {inr(imp - tot)} (1); amount reimbursed to restore imprest {inr(tot)} (1).'}


def c4s3_restore(r):
    d = ctx(r)
    imp = r.choice([5000, 6000, 8000, 10000])
    left = r.randrange(5, 40) * 20
    ex = _petty(r, 4)
    tot = sum(x for _, _, x in ex)
    if tot >= imp:
        raise ValueError
    lines = '; '.join(f'{lbl} {inr(x)}' for lbl, _, x in ex)
    return {'stem': f'On 1 June the petty cashier of {d["f"]} had {inr(left)} left out of an imprest of {inr(imp)}. He received the amount needed to restore the imprest, then paid: {lines}. Find (i) the amount received on 1 June (ii) the balance on 30 June (iii) the amount to be received on 1 July.',
            'answer': f'(i) {inr(imp - left)} (ii) {inr(imp - tot)} (iii) {inr(tot)}',
            'key': f'(i) {inr(imp)} − {inr(left)} = {inr(imp - left)} (1). (ii) {inr(imp)} − {inr(tot)} = {inr(imp - tot)} (1). (iii) amount spent {inr(tot)} (1).'}


CH04_ST3_FACTS = dict(
    cat='term',
    terms=[('Petty cash book', 'A book kept by the petty cashier to record small, frequent payments such as postage, cartage and stationery.'),
           ('Imprest system', 'A system in which the petty cashier is given a fixed amount at the start of a period and is reimbursed the amount spent at its end.'),
           ('Petty cashier', 'The person who handles and records small payments in the petty cash book.'),
           ('Analytical petty cash book', 'A petty cash book with separate columns for each common type of small expense.')],
    lists=[('adv', 'advantages of the imprest system of petty cash', [
        ('Saves time of the main cashier', 'The head cashier is relieved of many small payments.'),
        ('Better control over small payments', 'The petty cashier can never spend more than the imprest.'),
        ('Saves effort in posting', 'Only the column totals are posted to the ledger.'),
        ('Easy checking', 'Cash in hand plus vouchers must always equal the imprest.')], None)],
    ars=[
        ('Under the imprest system, the petty cashier is reimbursed the amount spent.', 'This restores the petty cash to the original fixed amount.', 'a', 'Both true and R explains A.'),
        ('Only the column totals of an analytical petty cash book are posted to the ledger.', 'Each column collects expenses of the same kind.', 'a', 'Both true and R explains A.'),
        ('The petty cash book is used for large payments such as salaries.', 'The petty cash book is maintained by the petty cashier.', 'd', 'A is false: it is used for small payments. R is true.')],
    tf=('the petty cash book', [
        'Under the imprest system, the amount spent is reimbursed at the end of the period.',
        'An analytical petty cash book has separate columns for different expenses.',
        'The petty cash book records small payments.'], [
        'The petty cash book records credit purchases.',
        'Under the imprest system, the petty cashier receives a different amount every month without any link to spending.',
        'Each petty expense is posted individually to the ledger.',
        'Salaries of staff are paid through the petty cash book.']),
)

BOOKS = ['Cash Book', 'Purchases Book', 'Sales Book', 'Purchases Return Book', 'Sales Return Book', 'Journal Proper']


def c4s4_book(r):
    t, d = txn(r)
    return mcq(f'In which book of original entry is the following recorded? "{t["text"]}"', t['book'], r.sample([b for b in BOOKS if b != t['book']], 3),
               f'{t["book"]}. Entry: {je(t)}.', r)


def c4s4_books4(r):
    d = ctx(r)
    pool = [t_purch_credit, t_sale_credit, t_machinery_credit, t_drawings_goods, t_purch_return, t_sales_return, t_purch_cash, t_samples, t_trade_disc, t_fire]
    ts = _cash_seq(r, 4, pool, d)
    if len({t['book'] for t in ts}) < 3:
        raise ValueError
    lines = ' '.join(f'({i + 1}) {t["text"]}.' for i, t in enumerate(ts))
    ans = ' '.join(f'({i + 1}) {t["book"]}' for i, t in enumerate(ts))
    return {'stem': f'Name the book of original entry in which each transaction of {d["f"]} will be recorded, with a reason: {lines}', 'answer': ans,
            'key': '1 mark each: ' + ' '.join(f'({i + 1}) {t["book"]} ({_why_book(t)})' for i, t in enumerate(ts))}


def _why_book(t):
    return {'Cash Book': 'cash or bank is involved', 'Purchases Book': 'credit purchase of goods', 'Sales Book': 'credit sale of goods',
            'Purchases Return Book': 'goods returned to a supplier', 'Sales Return Book': 'goods returned by a customer',
            'Journal Proper': 'not a cash transaction and not a credit purchase or sale of goods'}[t['book']]


def c4s4_purch_total(r):
    d = ctx(r)
    lines, total, parts = [], 0, []
    sup = r.sample([x for x in [firm(r) for _ in range(8)]], 4)
    for i, s in enumerate(sup[:3]):
        lp = amt(r, 5000, 60000, 1000)
        td = r.choice([0, 5, 10, 20])
        net = lp * (100 - td) // 100
        total += net
        parts.append(inr(net))
        lines.append(f'bought goods from {s} on credit, list price {inr(lp)}' + (f', trade discount {td}%' if td else ''))
    x1 = amt(r, 5000, 30000, 500)
    x2 = amt(r, 10000, 60000, 1000)
    lines.insert(r.randrange(4), f'bought goods for cash {inr(x1)}')
    lines.insert(r.randrange(5), f'bought furniture on credit from {sup[3]} {inr(x2)}')
    body = '; '.join(f'({i + 1}) {l}' for i, l in enumerate(lines))
    return {'stem': f'From the following transactions of {d["f"]} for April, find the total of the purchases book: {body}.',
            'answer': inr(total), 'key': f'Only credit purchases of goods, at net price: {" + ".join(parts)} = {inr(total)}. The cash purchase goes to the cash book and the furniture to the journal proper.',
            'distractors': [inr(total + x1), inr(total + x2), inr(total + x1 + x2)]}


def c4s4_sales_total(r):
    d = ctx(r)
    lines, total, parts = [], 0, []
    cus = r.sample(['Ravi', 'Neha', 'Sunil', 'Farah', 'Joseph', 'Gurpreet', 'Anil', 'Shalini'], 3)
    for c in cus:
        n = r.randrange(5, 40)
        rate = r.randrange(20, 200) * 10
        td = r.choice([0, 5, 10])
        gross = n * rate
        net = gross * (100 - td) / 100
        total += net
        parts.append(inr(net))
        lines.append(f'sold {n} units at {inr(rate)} each to {c} on credit' + (f' less {td}% trade discount' if td else ''))
    x1 = amt(r, 5000, 30000, 500)
    lines.insert(r.randrange(4), f'sold goods for cash {inr(x1)}')
    x2 = amt(r, 5000, 20000, 500)
    lines.insert(r.randrange(5), f'sold old furniture on credit to Mohan {inr(x2)}')
    body = '; '.join(f'({i + 1}) {l}' for i, l in enumerate(lines))
    return {'stem': f'Prepare the sales book of {d["f"]} from the following and give its total: {body}.', 'answer': inr(total),
            'key': f'Credit sales of goods only, net of trade discount: {" + ".join(parts)} = {inr(total)} (cash sale and sale of furniture excluded).'}


CH04_ST4_FACTS = dict(
    cat='special purpose book',
    terms=[('Purchases Book', 'Records all credit purchases of goods in which the business deals.'),
           ('Sales Book', 'Records all credit sales of goods in which the business deals.'),
           ('Purchases Return Book', 'Records goods returned to suppliers that had been bought on credit.'),
           ('Sales Return Book', 'Records goods returned by customers that had been sold on credit.'),
           ('Journal Proper', 'Records transactions that do not fit any other book, such as opening entries, credit purchase of assets and rectification entries.'),
           ('Cash Book', 'Records all receipts and payments of cash and through the bank.')],
    ars=[
        ('Credit purchase of machinery is not recorded in the purchases book.', 'The purchases book records only credit purchases of goods.', 'a', 'Both true and R explains A.'),
        ('Special purpose books save time.', 'Different persons can record different types of transactions at the same time.', 'a', 'Both true and R explains A.'),
        ('Cash sales are recorded in the sales book.', 'The sales book records only credit sales of goods.', 'd', 'A is false; R is true.'),
        ('Goods withdrawn by the owner are recorded in the journal proper.', 'They are neither a cash transaction nor a credit purchase or sale.', 'a', 'Both true and R explains A.')],
    tf=('special purpose books', [
        'The purchases book records only credit purchases of goods.',
        'Opening entries are recorded in the journal proper.',
        'The sales book records sales at the net amount after trade discount.'], [
        'Cash purchases are recorded in the purchases book.',
        'Credit purchase of furniture is recorded in the purchases book.',
        'The sales return book records goods returned to suppliers.',
        'Trade discount is shown in a separate column of the ledger.']),
)

POST = [('The periodic total of the purchases book', 'Debit side of Purchases A/c'),
        ('Each individual entry of the purchases book', 'Credit side of the respective suppliers\' accounts'),
        ('The periodic total of the sales book', 'Credit side of Sales A/c'),
        ('Each individual entry of the sales book', 'Debit side of the respective customers\' accounts'),
        ('The periodic total of the purchases return book', 'Credit side of Purchases Return A/c'),
        ('Each individual entry of the purchases return book', 'Debit side of the respective suppliers\' accounts'),
        ('The periodic total of the sales return book', 'Debit side of Sales Return A/c'),
        ('Each individual entry of the sales return book', 'Credit side of the respective customers\' accounts')]


def c4s5_posting(r):
    a, b = r.choice(POST)
    return mcq(f'{a} is posted to the …', b, r.sample([y for x, y in POST if y != b], 3), f'{a} → {b.lower()}.', r)


def c4s5_net(r):
    d = ctx(r)
    if r.random() < 0.5:
        pb = amt(r, 100000, 500000, 1000)
        pr = amt(r, 2000, pb // 10, 500)
        cash = amt(r, 10000, 80000, 1000)
        return {'stem': f'For the year, {d["f"]} had: purchases book total {inr(pb)}, purchases return book total {inr(pr)} and cash purchases {inr(cash)}. Find the net purchases shown in the trading account.',
                'answer': inr(pb + cash - pr), 'key': f'Total purchases {inr(pb)} + {inr(cash)} = {inr(pb + cash)}; less returns {inr(pr)} = {inr(pb + cash - pr)}.',
                'distractors': [inr(pb - pr), inr(pb + cash + pr), inr(pb + cash)]}
    sb = amt(r, 100000, 500000, 1000)
    sr = amt(r, 2000, sb // 10, 500)
    cash = amt(r, 10000, 80000, 1000)
    return {'stem': f'For the year, {d["f"]} had: sales book total {inr(sb)}, sales return book total {inr(sr)} and cash sales {inr(cash)}. Find the net sales shown in the trading account.',
            'answer': inr(sb + cash - sr), 'key': f'Total sales {inr(sb)} + {inr(cash)} = {inr(sb + cash)}; less returns {inr(sr)} = {inr(sb + cash - sr)}.',
            'distractors': [inr(sb - sr), inr(sb + cash + sr), inr(sb + cash)]}


def c4s5_supplier(r):
    d = ctx(r)
    s = d['f2']
    p1, p2 = amt(r, 20000, 80000, 500), amt(r, 10000, 50000, 500)
    ret = amt(r, 1000, 6000, 500)
    paid = amt(r, 10000, p1 - 2000, 500)
    dis = amt(r, 100, 600, 50)
    bal = p1 + p2 - ret - paid - dis
    return {'stem': f'In the books of {d["f"]}: the purchases book shows goods bought from {s} for {inr(p1)} and {inr(p2)}; a debit note was issued to {s} for goods returned {inr(ret)}; the cash book shows {inr(paid)} paid to {s} with discount received {inr(dis)}. Prepare the account of {s} and state its balance.',
            'answer': f'Credit balance {inr(bal)}: amount owed to {s}',
            'key': f'Credit side: {inr(p1)} + {inr(p2)} = {inr(p1 + p2)}; debit side: returns {inr(ret)} + cash {inr(paid)} + discount {inr(dis)} = {inr(ret + paid + dis)}; balance c/d on debit side {inr(bal)}, i.e. a credit balance (creditor).'}


CH04_ST5_FACTS = dict(
    cat='document',
    terms=[('Debit note', 'A note prepared by the buyer and sent to the supplier when goods are returned, informing that the supplier\'s account has been debited.'),
           ('Credit note', 'A note prepared by the seller and sent to the customer when goods are returned by him, informing that his account has been credited.'),
           ('Invoice', 'A document prepared by the seller showing goods sold on credit, quantity, rate, trade discount and the net amount payable.'),
           ('Posting of special books', 'Transfer of individual entries to personal accounts and periodic totals to the nominal accounts in the ledger.')],
    pairs=[('debit note', 'credit note', [
        ('prepared by', 'the buyer (purchaser)', 'the seller'),
        ('sent to', 'the supplier', 'the customer'),
        ('occasion', 'goods returned to the supplier (purchases return)', 'goods returned by the customer (sales return)'),
        ('account affected in the sender\'s books', 'the supplier\'s account is debited', 'the customer\'s account is credited')])],
    ars=[
        ('A debit note is the basis of entries in the purchases return book.', 'A debit note is issued when goods are returned to the supplier.', 'a', 'Both true and R explains A.'),
        ('The total of the sales book is posted to the debit side of the Sales account.', 'Individual customers\' accounts are debited from the sales book.', 'd', 'A is false: the total is credited to the Sales account. R is true.'),
        ('A credit note is sent by the seller to the customer.', 'The customer\'s account is credited when he returns goods.', 'a', 'Both true and R explains A.')],
    tf=('posting of special purpose books', [
        'The total of the purchases book is posted to the debit side of the Purchases account.',
        'Individual entries of the sales book are debited to customers\' accounts.',
        'A debit note is the source document for the purchases return book.'], [
        'The total of the sales return book is credited to the Sales Return account.',
        'Individual entries of the purchases book are debited to suppliers\' accounts.',
        'A credit note is sent by the buyer to the supplier.',
        'The total of the purchases return book is debited to the Purchases Return account.']),
)

FAMILIES.update({
    S + '04-st1': _f(CH04_ST1_FACTS) + [FF('C3', 'D3', 'multi_step', c4s1_balance, marks=3, kinds=('m3',)), FF('C4', 'D4', 'multi_step', c4s1_mixed, marks=4, kinds=('m4',)),
                                        FF('C2', 'D2', 'mcq', c4s1_not_recorded), FF('C3', 'D2', 'mcq', c4s1_not_recorded), FF('C4', 'D3', 'multi_step', c4s1_mixed, marks=4)],
    S + '04-st2': _f(CH04_ST2_FACTS) + [FF('C3', 'D3', 'multi_step', c4s2_balance, marks=4, kinds=('m4',)), FF('C4', 'D4', 'long', c4s2_long, marks=6, kinds=('m6',)),
                                        FF('C2', 'D2', 'mcq', c4s2_contra), FF('C3', 'D2', 'mcq', c4s2_column), FF('C3', 'D1', 'mcq', c4s2_column),
                                        FF('C4', 'D3', 'multi_step', c4s2_balance, marks=4)],
    S + '04-st3': _f(CH04_ST3_FACTS) + [FF('C3', 'D2', 'numerical', c4s3_imprest, marks=2), FF('C3', 'D3', 'multi_step', c4s3_analysis, marks=4, kinds=('m4',)),
                                        FF('C4', 'D4', 'multi_step', c4s3_restore, marks=3, kinds=('m3',)), FF('C3', 'D1', 'numerical', c4s3_imprest, marks=1)],
    S + '04-st4': _f(CH04_ST4_FACTS) + [FF('C2', 'D2', 'mcq', c4s4_book), FF('C3', 'D2', 'mcq', c4s4_book), FF('C3', 'D3', 'explain', c4s4_books4, marks=4, kinds=('m4',)),
                                        FF('C3', 'D3', 'multi_step', c4s4_purch_total, marks=3, kinds=('m3',)), FF('C4', 'D4', 'multi_step', c4s4_sales_total, marks=3, kinds=('m3',)),
                                        FF('C4', 'D3', 'multi_step', c4s4_purch_total, marks=3), FF('C2', 'D1', 'mcq', c4s4_book)],
    S + '04-st5': _f(CH04_ST5_FACTS) + [FF('C2', 'D2', 'mcq', c4s5_posting), FF('C3', 'D2', 'numerical', c4s5_net, marks=2), FF('C4', 'D4', 'multi_step', c4s5_supplier, marks=4, kinds=('m4',)),
                                        FF('C3', 'D3', 'multi_step', c4s5_supplier, marks=3, kinds=('m3',)), FF('C2', 'D1', 'mcq', c4s5_posting), FF('C4', 'D3', 'numerical', c4s5_net, marks=2)],
})
