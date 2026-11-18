"""CBSE class 12 accountancy families, ch01-ch04 (partnership: basic concepts, admission, retirement and death,
dissolution). Theory is fact tables (g11_accountancy_kit.facts); problems are computed here with exact
fractions so every answer is checked arithmetic.

Shared helpers for the other g12 accountancy modules (fractions, ratios, partner names) live here too.
Mock kinds: 'm3', 'm4', 'm6' (practical problems), 'ar'; the build script maps them to Part A / Part B kinds.
"""
from __future__ import annotations

from fractions import Fraction as Fr
from math import gcd, lcm

from qbank import mcq, inr, GIRLS, BOYS
from g11_accountancy_kit import facts, FF, ctx, amt

S = 'cbse-g12-accountancy-ch'
YEAR = 'the year ended 31 March 2026'
MONTHS = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']


# ---------------------------------------------------------------- helpers

def I(x) -> int:
    """Exact rupee amount or ValueError (the builder then draws again)."""
    x = Fr(x)
    if x.denominator != 1:
        raise ValueError('not whole rupees')
    return int(x)


def money(x) -> str:
    """Rupees for an exact Fraction: whole rupees, else two decimals."""
    x = Fr(x)
    return inr(int(x)) if x.denominator == 1 else inr(round(float(x), 2))


def q(n) -> str:
    """Count with Indian digit grouping: 121000 -> 1,21,000."""
    return inr(n)[1:]


def fs(x: Fr) -> str:
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def rstr(parts) -> str:
    """Ratio string from fractions or ints, reduced: [3/10, 2/10] -> '3:2'."""
    parts = [Fr(p) for p in parts]
    m = 1
    for p in parts:
        m = lcm(m, p.denominator)
    ints = [int(p * m) for p in parts]
    g = 0
    for x in ints:
        g = gcd(g, x)
    return ':'.join(str(x // g) for x in ints)


def shares(ratio) -> list:
    t = sum(ratio)
    return [Fr(x, t) for x in ratio]


def names(r, k=3) -> list:
    return r.sample(GIRLS + BOYS, k)


def andj(xs) -> str:
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def pa(n):
    return f"{n}'s Capital A/c"


def split(total, sh) -> list:
    return [I(total * s) for s in sh]


def retry(f, *a, **k):
    for _ in range(60):
        try:
            return f(*a, **k)
        except (ValueError, ZeroDivisionError):
            continue
    raise ValueError('retry failed')


R2 = [(3, 2), (2, 1), (1, 1), (3, 1), (5, 3), (4, 3), (7, 3), (3, 5), (2, 3), (5, 4)]
R3 = [(3, 2, 1), (2, 2, 1), (5, 3, 2), (4, 3, 3), (2, 1, 1), (1, 1, 1), (3, 3, 2), (4, 3, 2), (5, 4, 1), (3, 2, 2)]


def ratio_d(rt, others):
    """Ratio distractors as strings."""
    out = []
    for o in others:
        s = rstr(o)
        if s != rt and s not in out:
            out.append(s)
    return out


# ================================================================ ch01 Partnership: basic concepts

CH01_ST1 = dict(
    cat='partnership term',
    terms=[
        ('Partnership', 'The relation between persons who have agreed to share the profits of a business carried on by all or any of them acting for all (Section 4, Indian Partnership Act, 1932).'),
        ('Partnership deed', 'A written agreement among the partners containing the terms of partnership, such as capital, profit-sharing ratio, interest and salaries.'),
        ('Mutual agency', 'The feature that every partner is both an agent and a principal of the firm, so the act of one binds all.'),
        ('Unlimited liability', 'The liability of partners for the debts of the firm extends to their private assets.'),
        ('Firm', 'Persons who have entered into partnership with one another are collectively called this.'),
        ('Firm name', 'The name under which the business of the partners is carried on.'),
    ],
    lists=[
        ('feat', 'essential features of partnership', [
            ('Two or more persons', 'At least two persons are needed; the maximum is 50 under the Companies (Miscellaneous) Rules, 2014.'),
            ('Agreement', 'Partnership arises from an agreement, oral or written, not from status.'),
            ('Business', 'The agreement must be to carry on a lawful business.'),
            ('Mutual agency', 'Business is carried on by all or any of them acting for all.'),
            ('Sharing of profit', 'Partners agree to share profits (and losses) of the business.'),
            ('Unlimited liability', 'Partners are liable jointly and severally for the debts of the firm.')], None),
        ('deed', 'contents of a partnership deed', [
            ('Names and addresses of the firm and partners', 'Identifies the firm and each partner.'),
            ('Nature of business', 'States the business to be carried on.'),
            ('Capital contributed by each partner', 'Amount and form of capital of each partner.'),
            ('Profit-sharing ratio', 'The ratio in which profits and losses are shared.'),
            ('Interest on capital and drawings', 'Rates at which interest is allowed on capital and charged on drawings.'),
            ('Salary or commission to partners', 'Remuneration payable to working partners.'),
            ('Rules for admission, retirement and death', 'Treatment of goodwill and revaluation on reconstitution.'),
            ('Method of settling disputes', 'Arbitration or other method of resolving disputes.')], 'noact'),
        ('noact', 'provisions of the Indian Partnership Act, 1932 that apply in the absence of a partnership deed', [
            ('Profits and losses are shared equally', 'Irrespective of capital contributed.'),
            ('No interest on capital is allowed', 'Partners are not entitled to interest on capital.'),
            ('No interest is charged on drawings', 'Drawings carry no interest.'),
            ('No salary or commission to any partner', 'Partners are not entitled to remuneration.'),
            ('Interest on a partner\'s loan at 6% per annum', 'A partner who advances a loan beyond agreed capital gets 6% p.a.'),
            ('Every partner can take part in the business', 'Each partner has the right to participate in management.')], 'deed'),
    ],
    scen=[('Under the Indian Partnership Act, 1932 (no partnership deed), is the claim valid?',
           ['Valid', 'Not valid', 'Valid only with consent of all partners', 'Valid only if the firm earns a profit'], [
        ('{p} and {p2} are partners without a deed. {p} contributed twice the capital of {p2} and claims profit in the ratio 2:1.', 'Not valid', 'In the absence of a deed profits are shared equally.'),
        ('{p}, {p2} and {p3} have no partnership deed. {p} works full-time and claims a salary of ₹20,000 a month.', 'Not valid', 'No salary is allowed to a partner without a deed.'),
        ('{p} advanced a loan of ₹1,00,000 to the firm of {p} and {p2}. There is no deed. {p} claims interest at 6% p.a. on the loan.', 'Valid', 'Interest on a partner\'s loan is allowed at 6% p.a. even without a deed.'),
        ('{p} and {p2} have no deed. {p2} claims interest on capital at 10% p.a.', 'Not valid', 'No interest on capital is allowed without a deed.'),
        ('{p} and {p2} have no deed. {p} demands interest on {p2}\'s drawings at 8% p.a.', 'Not valid', 'No interest is charged on drawings without a deed.'),
        ('{p} and {p2} have no deed. {p} advanced a loan of ₹50,000 and claims interest at 12% p.a. on it.', 'Not valid', 'Interest on a partner\'s loan is limited to 6% p.a. without a deed.')], None)],
    ars=[
        ('In the absence of a partnership deed, partners share profits equally.', 'The Indian Partnership Act, 1932 provides for equal sharing when there is no agreement.', 'a', 'Both true; R explains A.'),
        ('Interest on a partner\'s loan is a charge against profit.', 'Interest on a partner\'s loan is payable even if the firm suffers a loss.', 'a', 'Both true; R explains A: being a charge, it is paid whether or not there is profit.'),
        ('A partner is entitled to a salary in the absence of a partnership deed.', 'Every partner has a right to take part in the conduct of business.', 'd', 'A is false: no salary without a deed. R is true.'),
        ('A partnership deed should be in writing.', 'A written deed helps settle disputes among partners.', 'a', 'Both true; R explains why a written deed is preferred (the law accepts an oral agreement too).'),
        ('The maximum number of partners in a firm is 50.', 'The Companies (Miscellaneous) Rules, 2014 prescribe this limit.', 'a', 'Both true; R explains A.'),
        ('Partners have limited liability.', 'Each partner is an agent of the firm.', 'd', 'A is false: liability is unlimited. R is true (mutual agency).')],
    tf=('the provisions applicable in the absence of a partnership deed', [
        'Profits and losses are shared equally.',
        'Interest on a partner\'s loan is allowed at 6% per annum.',
        'No interest is allowed on partners\' capitals.',
        'No partner is entitled to a salary.'], [
        'Profits are shared in the capital ratio.',
        'Interest on capital is allowed at 6% per annum.',
        'Interest on drawings is charged at 6% per annum.',
        'Interest on a partner\'s loan is allowed at 12% per annum.']),
    cases=[('C4', 'D4', 4, '{p}, {p2} and {p3} started a firm in {c} without a partnership deed. {p} contributed ₹3,00,000, {p2} ₹2,00,000 and {p3} ₹1,00,000. {p3} also gave the firm a loan of ₹60,000. At the year end {p} wants profits shared in the capital ratio and {p2}, who works full-time, wants a salary.',
            [('How will profit be shared and are the two demands valid?', 'Equally; neither demand is valid without a deed (no capital-ratio sharing, no salary).'),
             ('What is {p3} entitled to on the loan for a full year?', 'Interest at 6% p.a.: ₹3,600, a charge against profit.')]),
           ('C4', 'D5', 4, '{p} and {p2} are partners. A dispute arose because nothing was written down about interest on capital, drawings and salary. A friend advises them to draw up a partnership deed.',
            [('State four matters the deed should contain.', 'Capital of each partner; profit-sharing ratio; interest on capital and drawings; salary or commission; rules for admission and retirement (any four).'),
             ('Why is a written deed better than an oral agreement?', 'It is evidence of the terms, avoids disputes, and must be stamped and can be registered.')])],
)


def c1_loan(r):
    a, b = names(r, 2)
    L = amt(r, 40000, 200000, 10000)
    m = r.choice([12, 9, 6, 4, 3])
    st = MONTHS[12 - m]
    intr = I(Fr(L * 6 * m, 1200))
    P = amt(r, 20000, 150000, 2000)
    if r.random() < 0.25:
        P = intr - 2 * amt(r, 500, 3000, 500)
    rest = P - intr
    each = I(Fr(rest, 2))
    res = 'profit' if rest >= 0 else 'loss'
    return {'stem': f'{a} and {b} are partners without a partnership deed. On 1 {st} 2025 {a} advanced a loan of {inr(L)} to the firm. The profit for {YEAR}, before any interest on the loan, was {inr(P)}. Calculate the interest on the loan and each partner\'s share of {res}.',
            'answer': f'Interest on loan {inr(intr)}; {res} {inr(abs(rest))}, {inr(abs(each))} each',
            'key': f'Interest at 6% p.a. for {m} months: {inr(L)} × 6/100 × {m}/12 = {inr(intr)} (1 mark; a charge, allowed even if it creates a loss). Balance {inr(P)} − {inr(intr)} = {res} {inr(abs(rest))} shared equally, {inr(abs(each))} each (2 marks).',
            'distractors': [f'Interest on loan {money(Fr(L * 12 * m, 1200))}; balance shared equally', 'No interest is allowed without a deed; whole profit shared equally', f'Interest on loan {money(Fr(L * 6, 100))}; balance shared in the capital ratio']}


def c1_loan_mcq(r):
    a, b = names(r, 2)
    L = amt(r, 40000, 300000, 20000)
    m = r.choice([12, 9, 6, 3])
    st = MONTHS[12 - m]
    ans = I(Fr(L * 6 * m, 1200))
    w = [I(Fr(L * 12 * m, 1200)), L * 6 // 100 if m != 12 else I(Fr(L * 6 * 6, 1200)), I(Fr(L * 9 * m, 1200))]
    return mcq(f'There is no partnership deed between {a} and {b}. {a} gave the firm a loan of {inr(L)} on 1 {st} 2025. Interest on the loan for {YEAR} will be:',
               inr(ans), [inr(x) for x in w], f'6% p.a. for {m} months = {inr(ans)}.', r)


# ---- st2 capital accounts

CH01_ST2 = dict(
    cat='term',
    terms=[
        ('Fixed capital method', 'The method under which partners\' capitals remain unchanged unless capital is added or withdrawn by agreement, and adjustments go to current accounts.'),
        ('Fluctuating capital method', 'The method under which all adjustments such as interest, salary, drawings and share of profit are recorded in a single capital account of each partner.'),
        ('Partner\'s current account', 'The account, kept under the fixed capital method, to which interest on capital, salary, drawings, interest on drawings and share of profit are posted.'),
        ('Drawings', 'Money or goods withdrawn by a partner from the firm for personal use.'),
    ],
    pairs=[('the fixed capital method', 'the fluctuating capital method', [
        ('number of accounts', 'two accounts (capital and current) for each partner', 'only one account (capital) for each partner'),
        ('change in capital', 'capital remains unchanged except for additional capital or withdrawal of capital', 'capital changes every year'),
        ('balance', 'capital account always shows a credit balance', 'capital account may show a debit balance'),
        ('adjustments', 'interest, salary, drawings and profit are posted to current accounts', 'all adjustments are posted to the capital accounts'),
        ('provision in deed', 'must be specifically provided in the deed', 'followed when the deed is silent')])],
    scen=[('Under the fixed capital method, which account will the item be posted to?',
           ['Partner\'s Capital Account', 'Partner\'s Current Account', 'Profit and Loss Appropriation Account', 'Profit and Loss Account'], [
        ('{p} brought additional capital of ₹50,000 into the firm.', 'Partner\'s Capital Account', 'Additional capital changes the fixed capital itself.'),
        ('{p} was allowed interest on capital at 8% p.a.', 'Partner\'s Current Account', 'Under the fixed method interest on capital is credited to the current account.'),
        ('{p} withdrew ₹5,000 every month for personal use.', 'Partner\'s Current Account', 'Drawings are debited to the current account.'),
        ('{p} permanently withdrew ₹40,000 of capital with the consent of all partners.', 'Partner\'s Capital Account', 'Withdrawal of capital reduces the fixed capital.'),
        ('{p} was credited with a salary of ₹12,000 a month.', 'Partner\'s Current Account', 'Salary is credited to the current account.'),
        ('{p}\'s share of the year\'s profit was ₹64,000.', 'Partner\'s Current Account', 'Share of profit is credited to the current account.')], None)],
    ars=[
        ('Under the fixed capital method, a partner\'s capital account can show a debit balance.', 'All adjustments are made in the current account under this method.', 'd', 'A is false: fixed capital accounts always show credit balances. R is true.'),
        ('Under the fluctuating capital method, the capital account may show a debit balance.', 'Drawings and losses are debited to the capital account.', 'a', 'Both true; R explains A.'),
        ('Interest on capital is credited to the current account under the fixed capital method.', 'Under the fixed capital method only additional capital and withdrawal of capital go to the capital account.', 'a', 'Both true; R explains A.')],
    tf=('the methods of maintaining partners\' capital accounts', [
        'Under the fixed capital method each partner has a capital account and a current account.',
        'Under the fluctuating capital method there is only one account for each partner.',
        'When the deed is silent, capitals are treated as fluctuating.'], [
        'Under the fixed capital method drawings are debited to the capital account.',
        'Under the fluctuating capital method each partner has a current account too.',
        'A fixed capital account can show a debit balance.',
        'Interest on capital is credited to the profit and loss account.']),
)


def _cap_data(r):
    p = r.choice(GIRLS + BOYS)
    cap = amt(r, 100000, 500000, 10000)
    rate = r.choice([5, 6, 8, 10, 12])
    ioc = I(Fr(cap * rate, 100))
    dr = amt(r, 12000, 60000, 1200)
    iod = amt(r, 300, 3000, 100)
    sal = r.choice([0, amt(r, 12000, 60000, 6000)])
    prof = amt(r, 20000, 150000, 1000)
    return p, cap, rate, ioc, dr, iod, sal, prof


def c1_fluct(r):
    p, cap, rate, ioc, dr, iod, sal, prof = _cap_data(r)
    close = cap + ioc + sal + prof - dr - iod
    sal_t = f', salary {inr(sal)}' if sal else ''
    return {'stem': f'Under the fluctuating capital method, {p}\'s capital on 1 April 2025 was {inr(cap)}. During {YEAR}: interest on capital @ {rate}% p.a.{sal_t}, share of profit {inr(prof)}, drawings {inr(dr)} and interest on drawings {inr(iod)}. Find {p}\'s capital on 31 March 2026.',
            'answer': inr(close),
            'key': f'{inr(cap)} + interest on capital {inr(ioc)}{" + salary " + inr(sal) if sal else ""} + profit {inr(prof)} − drawings {inr(dr)} − interest on drawings {inr(iod)} = {inr(close)} (credits 1½, debits 1½).',
            'distractors': [inr(close + 2 * iod), inr(cap + prof - dr), inr(close - ioc)]}


def c1_fixed(r):
    p, cap, rate, ioc, dr, iod, sal, prof = _cap_data(r)
    opening = amt(r, 5000, 40000, 1000) * r.choice([1, -1])
    close = opening + ioc + sal + prof - dr - iod
    side = 'credit' if opening > 0 else 'debit'
    cs = 'credit' if close >= 0 else 'debit'
    return {'stem': f'{p}\'s fixed capital is {inr(cap)} and {p}\'s current account had a {side} balance of {inr(abs(opening))} on 1 April 2025. For {YEAR}: interest on capital @ {rate}% p.a.{", salary " + inr(sal) if sal else ""}, share of profit {inr(prof)}, drawings {inr(dr)}, interest on drawings {inr(iod)}. Find the balance of the current account on 31 March 2026 and the capital account balance.',
            'answer': f'Current account {cs} balance {inr(abs(close))}; capital account stays {inr(cap)}',
            'key': f'Current account: {"+" if opening > 0 else "−"}{inr(abs(opening))} + {inr(ioc)} interest{" + " + inr(sal) + " salary" if sal else ""} + {inr(prof)} profit − {inr(dr)} drawings − {inr(iod)} interest on drawings = {cs} {inr(abs(close))} (2 marks). Fixed capital unchanged at {inr(cap)} (1 mark).',
            'distractors': [f'Current account {cs} balance {inr(abs(close - opening))}; capital {inr(cap)}', f'Capital account {inr(cap + close)}; no current account', f'Current account {cs} balance {inr(abs(close + 2 * iod))}; capital {inr(cap)}']}


# ---- st3 appropriation

CH01_ST3 = dict(
    cat='term',
    terms=[
        ('Profit and Loss Appropriation Account', 'An extension of the profit and loss account of a firm that shows how net profit is distributed among partners after interest, salary and commission.'),
        ('Interest on capital', 'An appropriation of profit allowed to partners on their capitals at the rate agreed in the deed, only out of profits.'),
        ('Interest on drawings', 'An amount charged to partners on money withdrawn, credited to the profit and loss appropriation account.'),
        ('Divisible profit', 'The balance of the profit and loss appropriation account shared among partners in their profit-sharing ratio.'),
        ('Product method', 'Calculating interest on drawings by multiplying each drawing by the months it was outstanding and charging interest on the total of products for one month.'),
    ],
    scen=[('Where is the item shown?', ['Debit of Profit and Loss Appropriation A/c', 'Credit of Profit and Loss Appropriation A/c', 'Debit of Profit and Loss A/c', 'Credit of Profit and Loss A/c'], [
        ('Interest on capital allowed to {p} at 10% p.a.', 'Debit of Profit and Loss Appropriation A/c', 'Interest on capital is an appropriation of profit.'),
        ('Salary of ₹15,000 a month allowed to {p} as a partner.', 'Debit of Profit and Loss Appropriation A/c', 'Partner\'s salary is an appropriation.'),
        ('Interest charged on {p}\'s drawings.', 'Credit of Profit and Loss Appropriation A/c', 'Interest on drawings is a gain to the firm, credited to the appropriation account.'),
        ('Interest on a loan of ₹80,000 given by {p} to the firm.', 'Debit of Profit and Loss A/c', 'Interest on a partner\'s loan is a charge against profit.'),
        ('Rent paid to {p} for the partner\'s shop used by the firm.', 'Debit of Profit and Loss A/c', 'Rent to a partner is a charge against profit.'),
        ('Commission allowed to {p} at 5% of net profit.', 'Debit of Profit and Loss Appropriation A/c', 'Partner\'s commission is an appropriation.'),
        ('Net profit transferred from the profit and loss account.', 'Credit of Profit and Loss Appropriation A/c', 'The appropriation account starts with net profit on the credit side.'),
        ('Transfer of 10% of profit to general reserve.', 'Debit of Profit and Loss Appropriation A/c', 'Transfer to reserve is an appropriation.')], None)],
    ars=[
        ('Interest on capital is allowed only out of profits.', 'Interest on capital is an appropriation of profit, not a charge.', 'a', 'Both true; R explains A.'),
        ('Interest on drawings is credited to the profit and loss appropriation account.', 'Interest on drawings is a gain to the firm.', 'a', 'Both true; R explains A.'),
        ('When drawings are made at the end of every month, interest is charged for an average of 5½ months.', 'The average period for equal monthly drawings at the end of each month is (11 + 0)/2 months.', 'a', 'Both true; R explains A.'),
        ('If the firm makes a loss, interest on capital is still allowed.', 'Interest on capital is an appropriation of profit.', 'd', 'A is false: no interest on capital in a loss year. R is true.'),
        ('Rent paid to a partner is debited to the profit and loss appropriation account.', 'Rent to a partner is a charge against profit.', 'd', 'A is false: it goes to the profit and loss account. R is true.'),
        ('When drawings are made at the beginning of each quarter, interest is charged for 7½ months on the total.', 'The average period is (12 + 3)/2 months.', 'a', 'Both true; R explains A.')],
    tf=('the profit and loss appropriation account', [
        'It is an extension of the profit and loss account.',
        'Interest on drawings is shown on its credit side.',
        'Partner\'s salary and commission are shown on its debit side.'], [
        'Interest on a partner\'s loan is shown on its debit side.',
        'It is prepared to find the net profit of the firm.',
        'Interest on capital is shown on its credit side.',
        'Rent paid to a partner is shown on its debit side.']),
)

PERIOD = {('month', 'beginning'): (Fr(13, 2), 12), ('month', 'middle'): (Fr(6), 12), ('month', 'end'): (Fr(11, 2), 12),
          ('quarter', 'beginning'): (Fr(15, 2), 4), ('quarter', 'end'): (Fr(9, 2), 4)}


def c1_iod(r):
    p = r.choice(GIRLS + BOYS)
    (unit, when), (per, n) = r.choice(list(PERIOD.items()))
    x = amt(r, 2000, 20000, 1000)
    rate = r.choice([6, 8, 9, 10, 12])
    tot = x * n
    iod = I(tot * rate * per / 1200)
    return {'stem': f'{p}, a partner, withdrew {inr(x)} at the {when} of every {unit} during {YEAR}. Calculate interest on drawings @ {rate}% p.a.',
            'answer': inr(iod),
            'key': f'Total drawings {inr(tot)}; average period {float(per):g} months; {inr(tot)} × {rate}/100 × {float(per):g}/12 = {inr(iod)}.',
            'distractors': [money(Fr(tot * rate, 100)), money(tot * rate * (Fr(6) if per != 6 else Fr(13, 2)) / 1200),
                            money(tot * rate * {Fr(13, 2): Fr(11, 2), Fr(11, 2): Fr(13, 2), Fr(6): Fr(11, 2), Fr(15, 2): Fr(9, 2), Fr(9, 2): Fr(15, 2)}[per] / 1200)]}


def c1_iod_mcq(r):
    v = retry(c1_iod, r)
    ds = list(dict.fromkeys(d for d in v['distractors'] if d != v['answer']))
    if len(ds) < 3:
        raise ValueError
    return mcq(v['stem'], v['answer'], ds[:3], v['key'], r)


def c1_iod_product(r):
    p = r.choice(GIRLS + BOYS)
    k = r.choice([3, 4])
    idx = sorted(r.sample(range(1, 12), k))
    amts = [amt(r, 5000, 40000, 1000) for _ in idx]
    rate = r.choice([6, 9, 10, 12])
    prods = [a * (12 - i) for a, i in zip(amts, idx)]
    tp = sum(prods)
    iod = I(Fr(tp * rate, 1200))
    lst = '; '.join(f'1 {MONTHS[i]} {2025 if i < 9 else 2026} {inr(a)}' for a, i in zip(amts, idx))
    calc = ' + '.join(f'{inr(a)} × {12 - i}' for a, i in zip(amts, idx))
    return {'stem': f'{p} made the following drawings during {YEAR}: {lst}. Calculate interest on drawings @ {rate}% p.a. using the product method.',
            'answer': inr(iod),
            'key': f'Months to 31 March: products {calc} = {inr(tp)} (2 marks); interest {inr(tp)} × {rate}/100 × 1/12 = {inr(iod)} (1 mark).'}


def c1_commission(r):
    p = r.choice(GIRLS + BOYS)
    x = r.choice([5, 10, 20, 25, 4])
    after = r.random() < 0.6
    P = (100 + x) * amt(r, 500, 3000, 100) if after else amt(r, 50000, 300000, 1000)
    com = I(Fr(P * x, 100 + x)) if after else I(Fr(P * x, 100))
    other = I(Fr(P * x, 100)) if after else I(Fr(P * x, 100 + x)) if (P * x) % (100 + x) == 0 else P * x // (100 + x)
    how = 'after charging such commission' if after else 'before charging such commission'
    return mcq(f'{p}, a partner, is entitled to a commission of {x}% of the net profit {how}. The net profit before commission is {inr(P)}. {p}\'s commission is:',
               inr(com), [inr(other), inr(com + 1000), inr(com - 500) if com > 1000 else inr(com * 2)],
               f'{"Commission = profit × " + str(x) + "/" + str(100 + x) if after else "Commission = profit × " + str(x) + "/100"} = {inr(com)}.', r)


def _approp(r, n_part=None, insufficient=False):
    k = n_part or r.choice([2, 3])
    ns = names(r, k)
    ratio = r.choice(R2 if k == 2 else R3)
    sh = shares(ratio)
    caps = [amt(r, 100000, 500000, 20000) for _ in ns]
    rate = r.choice([5, 6, 8, 10, 12])
    ioc = [I(Fr(c * rate, 100)) for c in caps]
    tioc = sum(ioc)
    if insufficient:
        P = amt(r, tioc // 3, tioc - 1000, 500)
        given = [I(Fr(P * i, tioc)) for i in ioc]
        if sum(given) != P:
            raise ValueError
        caps_t = ', '.join(f'{n} {inr(c)}' for n, c in zip(ns, caps))
        return {'stem': f'{andj(ns)} are partners sharing profits in the ratio {":".join(map(str, ratio))}. Their capitals were {caps_t}. The deed allows interest on capital @ {rate}% p.a. The net profit for {YEAR} is {inr(P)}. Show the distribution of profit.',
                'answer': '; '.join(f'{n} {inr(g)}' for n, g in zip(ns, given)) + ' (profit distributed in the ratio of interest on capital)',
                'key': f'Interest on capital due: ' + ', '.join(f'{n} {inr(i)}' for n, i in zip(ns, ioc)) + f' = {inr(tioc)}, which exceeds the profit {inr(P)}. Interest on capital is allowed only out of profit, so the profit is distributed in the ratio of interest due ({rstr(ioc)}): ' + ', '.join(f'{n} {inr(g)}' for n, g in zip(ns, given)) + '. No profit is left for sharing in the profit-sharing ratio.'}
    sal_i = r.randrange(k)
    sal = amt(r, 3000, 15000, 1000) * 12
    com_i = r.randrange(k)
    cx = r.choice([0, 2, 5])
    dr_i = [amt(r, 400, 4000, 100) for _ in ns]
    P = amt(r, 200000, 900000, 1000)
    com = I(Fr(P * cx, 100)) if cx else 0
    div = P + sum(dr_i) - tioc - sal - com
    if div <= 0:
        raise ValueError
    sp = split(div, sh)
    caps_t = ', '.join(f'{n} {inr(c)}' for n, c in zip(ns, caps))
    stem = (f'{andj(ns)} are partners sharing profits in the ratio {":".join(map(str, ratio))}. Their capitals on 1 April 2025 were {caps_t}. '
            f'The deed provides: interest on capital @ {rate}% p.a.; salary to {ns[sal_i]} {inr(sal // 12)} per month'
            + (f'; commission to {ns[com_i]} @ {cx}% of the net profit (before charging commission)' if cx else '')
            + '. Interest on drawings: ' + ', '.join(f'{n} {inr(d)}' for n, d in zip(ns, dr_i))
            + f'. The net profit for {YEAR} was {inr(P)}. Prepare the Profit and Loss Appropriation Account.')
    ans = f'Divisible profit {inr(div)}: ' + ', '.join(f'{n} {inr(s)}' for n, s in zip(ns, sp))
    key = (f'Credit: net profit {inr(P)} + interest on drawings {inr(sum(dr_i))} = {inr(P + sum(dr_i))}. Debit: interest on capital '
           + ', '.join(f'{n} {inr(i)}' for n, i in zip(ns, ioc)) + f'; salary to {ns[sal_i]} {inr(sal)}'
           + (f'; commission to {ns[com_i]} {inr(com)}' if cx else '')
           + f'. Divisible profit {inr(div)} shared {":".join(map(str, ratio))}: ' + ', '.join(f'{n} {inr(s)}' for n, s in zip(ns, sp))
           + '. (1 mark each: interest on capital, salary/commission, interest on drawings, divisible profit; 2 marks for shares.)')
    return {'stem': stem, 'answer': ans, 'key': key}


def c1_approp(r):
    return retry(_approp, r)


def c1_approp_short(r):
    return retry(_approp, r, insufficient=True)


def c1_ioc_add(r):
    p = r.choice(GIRLS + BOYS)
    cap = amt(r, 100000, 600000, 20000)
    add = amt(r, 20000, 120000, 6000)
    m = r.choice([9, 8, 6, 4, 3])
    st = MONTHS[12 - m]
    rate = r.choice([6, 8, 10, 12])
    a = I(Fr(cap * rate, 100))
    b = I(Fr(add * rate * m, 1200))
    return {'stem': f'{p}\'s capital on 1 April 2025 was {inr(cap)}. {p} introduced additional capital of {inr(add)} on 1 {st} 2025. Calculate interest on capital @ {rate}% p.a. for {YEAR}.',
            'answer': inr(a + b),
            'key': f'{inr(cap)} × {rate}% = {inr(a)}; {inr(add)} × {rate}% × {m}/12 = {inr(b)}; total {inr(a + b)}.',
            'distractors': [inr(a), inr(I(Fr((cap + add) * rate, 100))), inr(a + I(Fr(add * rate * (12 - m), 1200)))]}


# ---- st4 guarantee and past adjustments

CH01_ST4 = dict(
    cat='term',
    terms=[
        ('Guarantee of profit', 'An assurance that a partner will receive a minimum amount of profit, any deficiency being borne by the guaranteeing partner or partners.'),
        ('Deficiency', 'The amount by which a partner\'s actual share of profit falls short of the guaranteed minimum.'),
        ('Past adjustments', 'Corrections made after the final accounts are closed for omissions or errors such as interest on capital or salary not recorded.'),
        ('Adjustment entry', 'A single journal entry passed through partners\' capital or current accounts to correct an omission without reopening the closed accounts.'),
    ],
    ars=[
        ('The deficiency of a guaranteed partner is borne by the guaranteeing partners.', 'The guaranteed partner must receive at least the guaranteed amount.', 'a', 'Both true; R explains A.'),
        ('Past adjustments are made through the profit and loss adjustment account or directly through partners\' capital accounts.', 'Accounts of the earlier year are already closed.', 'a', 'Both true; R explains A.'),
        ('If interest on capital was omitted, the partner with the highest capital always gains on adjustment.', 'Adjustment compares interest due with the share of that amount borne in the profit ratio.', 'd', 'A is false: the gain depends on capital relative to profit share, not capital alone. R is true.'),
        ('A guarantee given by the firm is borne by the old partners in their profit-sharing ratio.', 'A firm\'s guarantee is shared by all the other partners.', 'a', 'Both true; R explains A.')],
    tf=('guarantee of profit and past adjustments', [
        'A guarantee may be given by one partner or by the firm.',
        'If the guaranteed partner\'s share exceeds the guaranteed amount, no deficiency arises.',
        'Past adjustments do not reopen the closed profit and loss account.'], [
        'A guaranteed partner always gets exactly the guaranteed amount.',
        'Deficiency is always borne equally by all partners.',
        'Past adjustments require the profit and loss account to be prepared again.',
        'A guarantee is a charge against profit.']),
)


def c1_guarantee(r):
    ns = names(r, 3)
    ratio = r.choice(R3)
    sh = shares(ratio)
    P = amt(r, 60000, 300000, 6000)
    sp = split(P, sh)
    gi = r.randrange(3)
    G = sp[gi] + amt(r, 2000, 20000, 1000)
    defi = G - sp[gi]
    others = [i for i in range(3) if i != gi]
    mode = r.choice(['firm', 'one'])
    out = sp[:]
    out[gi] = G
    if mode == 'firm':
        osh = [ratio[i] for i in others]
        bear = [I(Fr(defi * o, sum(osh))) for o in osh]
        for i, b in zip(others, bear):
            out[i] -= b
        who = f'by the firm (deficiency borne by {ns[others[0]]} and {ns[others[1]]} in their ratio {rstr(osh)})'
        txt = f'The firm guaranteed {ns[gi]} a minimum profit of {inr(G)}.'
    else:
        j = r.choice(others)
        out[j] -= defi
        who = f'by {ns[j]} alone'
        txt = f'{ns[j]} guaranteed {ns[gi]} a minimum profit of {inr(G)}, any deficiency to be borne by {ns[j]}.'
    return {'stem': f'{andj(ns)} share profits in the ratio {":".join(map(str, ratio))}. {txt} The profit for {YEAR} is {inr(P)}. Show the distribution of profit.',
            'answer': ', '.join(f'{n} {inr(o)}' for n, o in zip(ns, out)),
            'key': f'Shares {":".join(map(str, ratio))}: ' + ', '.join(f'{n} {inr(s)}' for n, s in zip(ns, sp)) + f'. Deficiency of {ns[gi]} {inr(G)} − {inr(sp[gi])} = {inr(defi)}, borne {who}. Final: ' + ', '.join(f'{n} {inr(o)}' for n, o in zip(ns, out)) + '.'}


def c1_guar_mcq(r):
    ns = names(r, 3)
    ratio = r.choice(R3)
    sh = shares(ratio)
    P = amt(r, 60000, 300000, 6000)
    sp = split(P, sh)
    gi = r.randrange(3)
    G = sp[gi] + amt(r, 2000, 20000, 1000)
    defi = G - sp[gi]
    return mcq(f'{andj(ns)} share profits {":".join(map(str, ratio))}. {ns[gi]} is guaranteed a minimum profit of {inr(G)}. If the firm\'s profit is {inr(P)}, the deficiency to be made good is:',
               inr(defi), [inr(G), inr(sp[gi]), inr(defi * 2)], f'{ns[gi]}\'s share {inr(sp[gi])}; deficiency {inr(G)} − {inr(sp[gi])} = {inr(defi)}.', r)


def _past(r):
    k = r.choice([2, 3])
    ns = names(r, k)
    ratio = r.choice(R2 if k == 2 else R3)
    caps = [amt(r, 50000, 400000, 10000) for _ in ns]
    rate = r.choice([5, 6, 8, 10])
    due = [I(Fr(c * rate, 100)) for c in caps]
    tot = sum(due)
    borne = split(tot, shares(ratio))
    net = [d - b for d, b in zip(due, borne)]
    if all(x == 0 for x in net):
        raise ValueError
    dr = [(n, -x) for n, x in zip(ns, net) if x < 0]
    cr = [(n, x) for n, x in zip(ns, net) if x > 0]
    ent = '; '.join(f"{n}'s Capital A/c Dr {inr(x)}" for n, x in dr) + '; ' + '; '.join(f"To {n}'s Capital A/c {inr(x)}" for n, x in cr)
    stem = (f'{andj(ns)} were partners sharing profits {":".join(map(str, ratio))}, with fixed capitals ' + ', '.join(f'{n} {inr(c)}' for n, c in zip(ns, caps))
            + f'. After the accounts for {YEAR} were closed, it was found that interest on capital @ {rate}% p.a. had been omitted. Pass the adjustment entry.')
    key = ('Interest due: ' + ', '.join(f'{n} {inr(d)}' for n, d in zip(ns, due)) + f' (total {inr(tot)}). Borne in profit ratio: '
           + ', '.join(f'{n} {inr(b)}' for n, b in zip(ns, borne)) + '. Net: ' + ', '.join(f'{n} {"+" if x >= 0 else "−"}{inr(abs(x))}' for n, x in zip(ns, net))
           + f'. Entry: {ent}. (Capitals are fixed, so current accounts may be used instead of capital accounts.)')
    return {'stem': stem, 'answer': ent, 'key': key}


def c1_past(r):
    return retry(_past, r)


# ================================================================ ch02 Admission

CH02_ST1 = dict(
    cat='term related to goodwill',
    terms=[
        ('Goodwill', 'The value of the reputation of a firm in respect of the profits expected in future over and above normal profits.'),
        ('Super profit', 'The excess of the average actual profit over the normal profit of a business.'),
        ('Normal profit', 'The profit that a firm in the same industry normally earns on capital employed, at the normal rate of return.'),
        ('Normal rate of return', 'The rate at which profit is earned by similar businesses in the same industry under normal circumstances.'),
        ('Capital employed', 'Total assets (excluding goodwill and fictitious assets) less outside liabilities.'),
        ('Years\' purchase', 'The number of years for which the firm is expected to earn the same level of profit, used as a multiplier.'),
    ],
    lists=[('fac', 'factors affecting the value of goodwill', [
        ('Nature of business', 'A firm with stable demand and better products earns more profit and has higher goodwill.'),
        ('Location', 'A centrally located business attracts more customers.'),
        ('Efficiency of management', 'Efficient management increases productivity and profits.'),
        ('Market situation', 'A monopoly or limited competition allows higher profits.'),
        ('Special advantages', 'Import licences, patents, trademarks or a long-term contract raise goodwill.'),
        ('Quality of products', 'Good quality builds customer loyalty and repeat sales.')], None)],
    scen=[('Which method of valuing goodwill is being used?', ['Average profit method', 'Super profit method', 'Capitalisation of average profit method', 'Weighted average profit method'], [
        ('Goodwill of {f} is valued at 3 years\' purchase of the average profit of the last four years.', 'Average profit method', 'Goodwill = average profit × number of years\' purchase.'),
        ('Goodwill is valued at 2 years\' purchase of the excess of average profit over normal profit.', 'Super profit method', 'Super profit × years\' purchase.'),
        ('The average profit is capitalised at the normal rate of return and the net assets are deducted from it.', 'Capitalisation of average profit method', 'Capitalised value of average profit − net assets.'),
        ('Profits of the last three years are given weights 1, 2 and 3 and the result is multiplied by 2.', 'Weighted average profit method', 'Weights are applied because profits show a trend.')], None)],
    ars=[
        ('Goodwill is an intangible asset.', 'Goodwill cannot be seen or touched but has value.', 'a', 'Both true; R explains A.'),
        ('Goodwill is a fictitious asset.', 'Goodwill can be sold only along with the business.', 'd', 'A is false: goodwill is intangible, not fictitious. R is true.'),
        ('Weighted average profit is used when profits show a rising or falling trend.', 'Recent years are given more weight.', 'a', 'Both true; R explains A.'),
        ('If average profit is less than normal profit, goodwill under the super profit method is nil.', 'There is no super profit in that case.', 'a', 'Both true; R explains A.')],
    tf=('goodwill', [
        'Goodwill is an intangible asset.',
        'Goodwill arises from the ability to earn super profits.',
        'Under the capitalisation of super profit method, goodwill = super profit × 100 / normal rate of return.'], [
        'Goodwill is a fictitious asset.',
        'Self-generated goodwill is recorded in the books under AS 26.',
        'Goodwill is valued only at the time of dissolution.',
        'A firm earning only normal profit has a large goodwill.']),
)


def _profits(r, n):
    ps = [amt(r, 40000, 200000, 1000) for _ in range(n)]
    if n >= 4 and r.random() < 0.3:
        ps[r.randrange(n)] = -amt(r, 5000, 30000, 1000)
    return ps


YRS = ['2021-22', '2022-23', '2023-24', '2024-25', '2025-26']


def c2_avg(r):
    n = r.choice([3, 4, 5])
    ps = _profits(r, n)
    yp = r.choice([Fr(2), Fr(3), Fr(5, 2), Fr(4), Fr(3, 2)])
    avg = Fr(sum(ps), n)
    G = I(avg * yp)
    I(avg)
    lst = ', '.join(f'{y} {"loss " + inr(-p) if p < 0 else inr(p)}' for y, p in zip(YRS[-n:], ps))
    return {'stem': f'Calculate the goodwill of a firm at {fs(yp)} years\' purchase of the average profit of the last {n} years. Profits: {lst}.',
            'answer': inr(G),
            'key': f'Total {inr(sum(ps))} ÷ {n} = average {inr(I(avg))} (1 mark); × {fs(yp)} = {inr(G)} (1 mark).',
            'distractors': [inr(I(Fr(sum(ps)) * yp)) if n != 1 else '₹0', inr(I(avg)), inr(I(Fr(sum(abs(p) for p in ps), n) * yp)) if any(p < 0 for p in ps) else inr(G + I(avg))]}


def c2_avg_adj(r):
    n = r.choice([3, 4])
    ps = _profits(r, n)
    j = r.randrange(n)
    ab = amt(r, 2000, 15000, 1000)
    kind = r.choice(['gain', 'loss'])
    adj = ps[:]
    adj[j] = ps[j] - ab if kind == 'gain' else ps[j] + ab
    avg = Fr(sum(adj), n)
    yp = r.choice([Fr(2), Fr(3)])
    I(avg)
    G = I(avg * yp)
    rem = r.random() < 0.5
    mgr = amt(r, 1000, 3000, 500) * 12 if rem else 0
    G2 = I((avg - mgr) * yp) if rem else G
    lst = ', '.join(f'{y} {"loss " + inr(-p) if p < 0 else inr(p)}' for y, p in zip(YRS[-n:], ps))
    extra = f' The partners worked without remuneration; a fair remuneration would be {inr(mgr // 12)} per month in total.' if rem else ''
    word = 'an abnormal gain' if kind == 'gain' else 'an abnormal loss'
    return {'stem': f'Profits of a firm were {lst}. The profit of {YRS[-n:][j]} includes the effect of {word} of {inr(ab)}.{extra} Calculate goodwill at {fs(yp)} years\' purchase of the average profit.',
            'answer': inr(G2),
            'key': f'Adjusted profit of {YRS[-n:][j]}: {inr(adj[j]) if adj[j] >= 0 else "loss " + inr(-adj[j])} ({"less" if kind == "gain" else "add back"} {inr(ab)}). Average {inr(I(avg))}'
                   + (f'; less remuneration {inr(mgr)} = {inr(I(avg - mgr))}' if rem else '') + f'; × {fs(yp)} = {inr(G2)}.'}


def c2_super(r):
    ce = amt(r, 200000, 1000000, 10000)
    nrr = r.choice([8, 10, 12, 15, 20])
    normal = I(Fr(ce * nrr, 100))
    sp_ = amt(r, 5000, 60000, 1000)
    avg = normal + sp_
    yp = r.choice([2, 3, 4])
    method = r.choice(['yp', 'cap'])
    if method == 'yp':
        G = sp_ * yp
        how = f'at {yp} years\' purchase of super profit'
        k2 = f'Goodwill = {inr(sp_)} × {yp} = {inr(G)}'
    else:
        G = I(Fr(sp_ * 100, nrr))
        how = 'by capitalising the super profit'
        k2 = f'Goodwill = {inr(sp_)} × 100/{nrr} = {inr(G)}'
    return {'stem': f'A firm has capital employed of {inr(ce)} and an average profit of {inr(avg)}. The normal rate of return is {nrr}%. Calculate goodwill {how}.',
            'answer': inr(G),
            'key': f'Normal profit = {inr(ce)} × {nrr}% = {inr(normal)}; super profit = {inr(avg)} − {inr(normal)} = {inr(sp_)}; {k2}.',
            'distractors': [inr(avg * (yp if method == 'yp' else 1)), inr(normal), inr(G + sp_)]}


def c2_capavg(r):
    nrr = r.choice([8, 10, 12, 15, 20])
    avg = amt(r, 30000, 200000, 1000)
    cap_val = I(Fr(avg * 100, nrr))
    assets = amt(r, cap_val // 2, cap_val, 10000)
    liab = amt(r, 20000, 150000, 5000)
    net = assets - liab
    G = cap_val - net
    if G <= 0:
        raise ValueError
    return {'stem': f'The average profit of a firm is {inr(avg)} and the normal rate of return is {nrr}%. Its assets (excluding goodwill) are {inr(assets)} and outside liabilities {inr(liab)}. Calculate goodwill by the capitalisation of average profit method.',
            'answer': inr(G),
            'key': f'Capitalised value = {inr(avg)} × 100/{nrr} = {inr(cap_val)}; net assets = {inr(assets)} − {inr(liab)} = {inr(net)}; goodwill = {inr(cap_val)} − {inr(net)} = {inr(G)}.',
            'distractors': [inr(cap_val), inr(cap_val - assets) if cap_val > assets else inr(G + liab), inr(G + liab)]}


def c2_weighted(r):
    ps = [amt(r, 40000, 200000, 1000) for _ in range(3)]
    ps.sort()
    yp = r.choice([2, 3])
    w = [1, 2, 3]
    wa = Fr(sum(p * x for p, x in zip(ps, w)), 6)
    G = I(wa * yp)
    I(wa)
    lst = ', '.join(f'{y} {inr(p)}' for y, p in zip(YRS[-3:], ps))
    return {'stem': f'Profits of a firm for three years were {lst} (weights 1, 2 and 3 respectively). Calculate goodwill at {yp} years\' purchase of the weighted average profit.',
            'answer': inr(G),
            'key': f'Weighted profits {inr(ps[0])}×1 + {inr(ps[1])}×2 + {inr(ps[2])}×3 = {inr(sum(p * x for p, x in zip(ps, w)))}; ÷ 6 = {inr(I(wa))}; × {yp} = {inr(G)}.',
            'distractors': [inr(I(Fr(sum(ps), 3) * yp)) if sum(ps) % 3 == 0 else inr(G + 1000), inr(I(wa)), inr(G * 2)]}


# ---- st2 ratios on admission

CH02_ST2 = dict(
    cat='term',
    terms=[
        ('Sacrificing ratio', 'The ratio in which the old partners give up their share of profit in favour of the incoming partner.'),
        ('New profit-sharing ratio', 'The ratio in which all partners, including the new partner, share future profits.'),
        ('Admission of a partner', 'The entry of a new partner into an existing firm, which reconstitutes the firm.'),
        ('Reconstitution of a firm', 'A change in the existing agreement among partners, such as a change in ratio, admission, retirement or death.'),
    ],
    lists=[('rights', 'rights acquired by a new partner on admission', [
        ('Right to share the assets of the firm', 'The new partner gets a share in the firm\'s assets.'),
        ('Right to share future profits', 'The new partner is entitled to a share in profits.'),
        ('Right to take part in the business', 'The new partner can participate in management.')], None),
        ('adj', 'adjustments required at the time of admission of a partner', [
        ('New profit-sharing ratio and sacrificing ratio', 'To share future profits and compensate old partners.'),
        ('Valuation and treatment of goodwill', 'Old partners are compensated for their sacrifice.'),
        ('Revaluation of assets and reassessment of liabilities', 'Gains or losses up to admission belong to old partners.'),
        ('Distribution of accumulated profits and reserves', 'Past profits belong to old partners.'),
        ('Adjustment of capitals', 'Capitals may be made proportionate to the new ratio.')], None)],
    ars=[
        ('Sacrificing ratio is calculated on admission of a partner.', 'Old partners are compensated for the share they give up.', 'a', 'Both true; R explains A.'),
        ('If a new partner takes his share from the old partners in their old ratio, the sacrificing ratio is the old ratio.', 'Each old partner gives up a share in proportion to his old share.', 'a', 'Both true; R explains A.'),
        ('Sacrificing ratio = New ratio − Old ratio.', 'Old partners give up part of their share in favour of the new partner.', 'd', 'A is false: sacrifice = old share − new share. R is true.'),
        ('The new profit-sharing ratio need not be the same as the old ratio among old partners.', 'Old partners may sacrifice in any agreed ratio.', 'a', 'Both true; R explains A.'),
    ],
    tf=('admission of a partner', [
        'Sacrificing ratio = Old ratio − New ratio.',
        'Admission of a partner is a mode of reconstitution of the firm.',
        'A new partner acquires the right to share future profits.'], [
        'Sacrificing ratio = New ratio − Old ratio.',
        'The old firm is dissolved on admission of a partner.',
        'Only the new partner\'s capital account is affected on admission.',
        'The sacrificing ratio is always the old ratio.']),
)


def _new_ratio(r):
    a, b, c = names(r, 3)
    old = r.choice(R2)
    sh = shares(old)
    n = r.choice([4, 5, 6, 3, 8, 10])
    s_new = Fr(1, n)
    mode = r.choice(['old', 'equal', 'given', 'surrender'])
    if mode == 'old':
        na, nb = sh[0] * (1 - s_new), sh[1] * (1 - s_new)
        txt = f'{c} is admitted for a {fs(s_new)} share, taken from {a} and {b} in their old ratio'
        sac = [sh[0] - na, sh[1] - nb]
    elif mode == 'equal':
        na, nb = sh[0] - s_new / 2, sh[1] - s_new / 2
        txt = f'{c} is admitted for a {fs(s_new)} share, which {c} acquires equally from {a} and {b}'
        sac = [s_new / 2, s_new / 2]
    elif mode == 'given':
        x = Fr(1, r.choice([5, 6, 8, 10, 12, 20]))
        y = Fr(1, r.choice([5, 6, 8, 10, 12, 20]))
        s_new = x + y
        na, nb = sh[0] - x, sh[1] - y
        txt = f'{c} is admitted; {c} acquires {fs(x)} of the profit from {a} and {fs(y)} from {b}'
        sac = [x, y]
    else:
        fa = Fr(1, r.choice([3, 4, 5]))
        fb = Fr(1, r.choice([3, 4, 5, 6]))
        x, y = sh[0] * fa, sh[1] * fb
        s_new = x + y
        na, nb = sh[0] - x, sh[1] - y
        txt = f'{a} surrenders {fs(fa)} of {a}\'s share and {b} surrenders {fs(fb)} of {b}\'s share in favour of {c}, the new partner'
        sac = [x, y]
    if na <= 0 or nb <= 0:
        raise ValueError
    nr = rstr([na, nb, s_new])
    sr = rstr(sac)
    return dict(a=a, b=b, c=c, old=old, txt=txt, nr=nr, sr=sr, na=na, nb=nb, nc=s_new, sac=sac, mode=mode)


def c2_newratio(r):
    d = retry(_new_ratio, r)
    others = ratio_d(d['nr'], [[d['na'] + d['nc'] / 4, d['nb'], d['nc'] * 3 / 4], [d['old'][0], d['old'][1], 1], [1, 1, 1], [d['sac'][0], d['sac'][1], d['nc']], [d['old'][0] * 2, d['old'][1] * 2, 1]])
    return mcq(f'{d["a"]} and {d["b"]} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. The new profit-sharing ratio of {d["a"]}, {d["b"]} and {d["c"]} is:',
               d['nr'], others[:3], f'New shares: {d["a"]} {fs(d["na"])}, {d["b"]} {fs(d["nb"])}, {d["c"]} {fs(d["nc"])} → {d["nr"]}.', r)


def c2_newratio_calc(r):
    d = retry(_new_ratio, r)
    return {'stem': f'{d["a"]} and {d["b"]} share profits in the ratio {":".join(map(str, d["old"]))}. {d["txt"]}. Calculate the new profit-sharing ratio and the sacrificing ratio.',
            'answer': f'New ratio {d["nr"]}; sacrificing ratio {d["sr"]}',
            'key': f'New shares: {d["a"]} {fs(d["na"])}, {d["b"]} {fs(d["nb"])}, {d["c"]} {fs(d["nc"])} = {d["nr"]} (2 marks). Sacrifice = old − new: {d["a"]} {fs(d["sac"][0])}, {d["b"]} {fs(d["sac"][1])} = {d["sr"]} (1 mark).'}


def c2_sacr_mcq(r):
    d = retry(_new_ratio, r)
    others = ratio_d(d['sr'], [d['old'], [1, 1], [d['na'], d['nb']], [d['old'][1], d['old'][0]], [2, 1], [1, 2]])
    if len(others) < 3:
        raise ValueError
    return mcq(f'{d["a"]} and {d["b"]} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. The sacrificing ratio of {d["a"]} and {d["b"]} is:',
               d['sr'], others[:3], f'Sacrifice = old share − new share: {fs(d["sac"][0])} and {fs(d["sac"][1])} → {d["sr"]}.', r)


# ---- st3 goodwill on admission

CH02_ST3 = dict(
    cat='term',
    terms=[
        ('Premium for goodwill', 'The amount brought by the new partner in cash as compensation to the old partners for their sacrifice.'),
        ('Hidden goodwill', 'Goodwill inferred from the capital brought by the new partner when the firm\'s goodwill is not given.'),
        ('AS 26 (Intangible Assets)', 'The accounting standard under which only purchased goodwill is recorded in the books; self-generated goodwill is not.'),
        ('Existing goodwill', 'Goodwill already appearing in the books of the old firm, written off among old partners in the old ratio on admission.'),
    ],
    scen=[('Which journal entry records this?', [
        'Bank A/c Dr; To Premium for Goodwill A/c', 'New partner\'s Current A/c Dr; To Old partners\' Capital A/cs', 'Old partners\' Capital A/cs Dr; To Goodwill A/c', 'Goodwill A/c Dr; To Old partners\' Capital A/cs'], [
        ('{p} is admitted and brings {his} share of goodwill in cash.', 'Bank A/c Dr; To Premium for Goodwill A/c', 'Cash brought for goodwill is first credited to Premium for Goodwill.'),
        ('{p} is admitted but is unable to bring {his} share of goodwill in cash.', 'New partner\'s Current A/c Dr; To Old partners\' Capital A/cs', 'The new partner\'s current (or capital) account is debited and sacrificing partners credited.'),
        ('Goodwill of ₹60,000 already appears in the books when {p} is admitted.', 'Old partners\' Capital A/cs Dr; To Goodwill A/c', 'Existing goodwill is written off among old partners in the old ratio.')], None)],
    ars=[
        ('The premium for goodwill brought by a new partner is shared by the old partners in their sacrificing ratio.', 'Old partners are compensated in the proportion of the share they give up.', 'a', 'Both true; R explains A.'),
        ('Goodwill account is raised in the books on the admission of a partner.', 'AS 26 allows only purchased goodwill to be recorded.', 'd', 'A is false: goodwill is not raised on admission. R is true.'),
        ('Existing goodwill is written off in the old ratio on admission.', 'It was built up by the old partners.', 'a', 'Both true; R explains A.'),
        ('If the new partner cannot bring goodwill in cash, his current account is debited.', 'He must still compensate the sacrificing partners.', 'a', 'Both true; R explains A.')],
    tf=('treatment of goodwill on admission', [
        'Premium for goodwill is credited to the sacrificing partners in the sacrificing ratio.',
        'Under AS 26, goodwill is not raised in the books on admission.',
        'Existing goodwill is written off among old partners in the old ratio.'], [
        'Premium for goodwill is credited to all partners in the new ratio.',
        'Goodwill account is always opened at full value on admission.',
        'Premium for goodwill is credited to the new partner.',
        'Existing goodwill is written off in the new ratio.']),
)


def c2_premium(r):
    d = retry(_new_ratio, r)
    G = amt(r, 60000, 600000, 6000)
    prem = I(G * d['nc'])
    ss = [I(Fr(prem) * x / sum(d['sac'])) for x in d['sac']]
    cash = r.random() < 0.7
    ent = (f'Bank A/c Dr {inr(prem)}; To Premium for Goodwill A/c {inr(prem)}. Premium for Goodwill A/c Dr {inr(prem)}; To {d["a"]}\'s Capital A/c {inr(ss[0])}; To {d["b"]}\'s Capital A/c {inr(ss[1])}'
           if cash else f'{d["c"]}\'s Current A/c Dr {inr(prem)}; To {d["a"]}\'s Capital A/c {inr(ss[0])}; To {d["b"]}\'s Capital A/c {inr(ss[1])}')
    how = 'brings the share of goodwill in cash' if cash else 'is unable to bring any amount for goodwill'
    return {'stem': f'{d["a"]} and {d["b"]} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. The firm\'s goodwill is valued at {inr(G)}. {d["c"]} {how}. Pass the journal entries.',
            'answer': ent,
            'key': f'{d["c"]}\'s share of goodwill = {inr(G)} × {fs(d["nc"])} = {inr(prem)}; sacrificing ratio {d["sr"]}; {d["a"]} {inr(ss[0])}, {d["b"]} {inr(ss[1])}. Entries: {ent}.'}


def c2_premium_mcq(r):
    d = retry(_new_ratio, r)
    G = amt(r, 60000, 600000, 6000)
    prem = I(G * d['nc'])
    ss = [I(Fr(prem) * x / sum(d['sac'])) for x in d['sac']]
    wrong = [I(Fr(prem) * s) for s in shares(d['old'])]
    if wrong[0] == ss[0]:
        wrong = [ss[1], ss[0]]
    opts = [f'{d["a"]} {inr(ss[0])}, {d["b"]} {inr(ss[1])}', f'{d["a"]} {inr(wrong[0])}, {d["b"]} {inr(wrong[1])}',
            f'{d["a"]} {inr(I(Fr(prem, 2)))}, {d["b"]} {inr(prem - I(Fr(prem, 2)))}', f'{d["a"]} {inr(I(G * shares(d["old"])[0]))}, {d["b"]} {inr(I(G * shares(d["old"])[1]))}']
    return mcq(f'{d["a"]} and {d["b"]} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. Goodwill of the firm is {inr(G)} and {d["c"]} brings the share of goodwill in cash. The premium will be credited to:',
               opts[0], opts[1:], f'Premium {inr(prem)} shared in sacrificing ratio {d["sr"]}.', r)


def c2_hidden(r):
    a, b, c = names(r, 3)
    n = r.choice([3, 4, 5])
    cap_c = amt(r, 60000, 200000, 10000)
    old_caps = [amt(r, 50000, 300000, 10000) for _ in range(2)]
    tot = cap_c * n
    G = tot - sum(old_caps) - cap_c
    if G <= 0:
        raise ValueError
    return {'stem': f'{a} and {b} have capitals of {inr(old_caps[0])} and {inr(old_caps[1])} after all adjustments. {c} is admitted for a 1/{n} share and brings {inr(cap_c)} as capital. Calculate the hidden goodwill of the firm.',
            'answer': inr(G),
            'key': f'Total capital of new firm on the basis of {c}\'s capital = {inr(cap_c)} × {n} = {inr(tot)}; actual combined capital = {inr(sum(old_caps))} + {inr(cap_c)} = {inr(sum(old_caps) + cap_c)}; goodwill = {inr(G)}.',
            'distractors': [inr(tot), inr(tot - sum(old_caps)), inr(G + cap_c)]}


# ---- st4 revaluation and reserves

CH02_ST4 = dict(
    cat='term',
    terms=[
        ('Revaluation Account', 'A nominal account prepared on reconstitution to record changes in the values of assets and liabilities and find the gain or loss.'),
        ('Accumulated profits', 'Undistributed profits such as general reserve and profit and loss (credit) balance, belonging to the old partners.'),
        ('Workmen Compensation Reserve', 'A reserve created for claims of workmen; any excess over the actual claim is distributed among old partners.'),
        ('Investment Fluctuation Reserve', 'A reserve created to meet a fall in the value of investments; any excess over the fall belongs to old partners.'),
    ],
    scen=[('Which side of the Revaluation Account is affected?', ['Debit side (loss)', 'Credit side (gain)', 'Not shown in Revaluation Account', 'Both sides equally'], [
        ('Building is to be appreciated by 10%.', 'Credit side (gain)', 'An increase in an asset is a gain.'),
        ('Machinery is to be depreciated by ₹15,000.', 'Debit side (loss)', 'A decrease in an asset is a loss.'),
        ('A provision for doubtful debts is to be created on debtors.', 'Debit side (loss)', 'A new provision reduces the asset value.'),
        ('Creditors are to be paid ₹3,000 less than their book value.', 'Credit side (gain)', 'A decrease in a liability is a gain.'),
        ('An unrecorded liability of ₹5,000 for outstanding repairs is to be brought into books.', 'Debit side (loss)', 'An unrecorded liability is a loss.'),
        ('An unrecorded investment worth ₹8,000 is to be brought into books.', 'Credit side (gain)', 'An unrecorded asset is a gain.'),
        ('General reserve of ₹30,000 appears in the balance sheet.', 'Not shown in Revaluation Account', 'Reserves are transferred to old partners\' capital accounts in the old ratio.')], None)],
    ars=[
        ('Profit on revaluation at the time of admission is shared by old partners in the old ratio.', 'The change in values took place before the new partner joined.', 'a', 'Both true; R explains A.'),
        ('General reserve is credited to the Revaluation Account.', 'Reserves belong to the old partners.', 'd', 'A is false: reserves go directly to old partners\' capital accounts. R is true.'),
        ('A debit balance of profit and loss account is debited to old partners\' capital accounts.', 'It is an accumulated loss of the old partners.', 'a', 'Both true; R explains A.'),
        ('Excess of workmen compensation reserve over the claim is distributed among all partners including the new partner.', 'The reserve was created out of past profits.', 'd', 'A is false: only old partners get it, in old ratio. R is true.')],
    tf=('revaluation on admission', [
        'Revaluation gain is shared by old partners in the old ratio.',
        'Increase in a liability is debited to the Revaluation Account.',
        'Unrecorded assets are credited to the Revaluation Account.'], [
        'Revaluation gain is shared in the new ratio.',
        'General reserve is credited to the Revaluation Account.',
        'Decrease in an asset is credited to the Revaluation Account.',
        'The new partner bears a share of revaluation loss.']),
)


def _reval_items(r):
    b = amt(r, 100000, 500000, 10000)
    m = amt(r, 50000, 300000, 10000)
    deb = amt(r, 40000, 200000, 10000)
    cred = amt(r, 30000, 150000, 5000)
    pb = r.choice([5, 10, 20])
    pm = r.choice([5, 10, 15])
    pd = r.choice([2, 5, 10])
    items = [
        (f'Building ({inr(b)}) is appreciated by {pb}%', I(Fr(b * pb, 100))),
        (f'Machinery ({inr(m)}) is depreciated by {pm}%', -I(Fr(m * pm, 100))),
        (f'A provision for doubtful debts @ {pd}% is created on debtors of {inr(deb)}', -I(Fr(deb * pd, 100))),
        (f'Creditors ({inr(cred)}) include an amount of {inr(x := amt(r, 1000, 6000, 500))} not payable', x),
        (f'An outstanding electricity bill of {inr(y := amt(r, 1000, 8000, 500))} is unrecorded', -y),
        (f'An unrecorded investment worth {inr(z := amt(r, 2000, 20000, 1000))} is to be brought into books', z),
        (f'Stock is overvalued by {inr(w := amt(r, 2000, 15000, 1000))}', -w),
        (f'Prepaid insurance of {inr(v := amt(r, 1000, 5000, 500))} is to be recorded', v),
    ]
    return items


def _reval(r, k):
    ns = names(r, 3)
    old = r.choice(R2)
    sel = r.sample(_reval_items(r), k)
    net = sum(x for _, x in sel)
    if net == 0:
        raise ValueError
    sp = split(abs(net), shares(old))
    word = 'gain' if net > 0 else 'loss'
    lst = '; '.join(f'({i + 1}) {t}' for i, (t, _) in enumerate(sel))
    return ns, old, sel, net, sp, word, lst


def c2_reval(r):
    ns, old, sel, net, sp, word, lst = retry(_reval, r, r.choice([4, 5]))
    return {'stem': f'{ns[0]} and {ns[1]} share profits {":".join(map(str, old))}. On admitting {ns[2]}, it was agreed: {lst}. Prepare the Revaluation Account and show the {word} credited or debited to each old partner.',
            'answer': f'Revaluation {word} {inr(abs(net))}: {ns[0]} {inr(sp[0])}, {ns[1]} {inr(sp[1])}',
            'key': 'Items: ' + '; '.join(f'({i + 1}) {"gain" if x > 0 else "loss"} {inr(abs(x))}' for i, (_, x) in enumerate(sel))
                   + f'. Net {word} {inr(abs(net))} (3 marks for items), shared by old partners in old ratio {":".join(map(str, old))}: {ns[0]} {inr(sp[0])}, {ns[1]} {inr(sp[1])} (1 mark).'}


def c2_reval_mcq(r):
    ns, old, sel, net, sp, word, lst = retry(_reval, r, 3)
    wrong = [-net, sum(abs(x) for _, x in sel), sum(x for _, x in sel if x > 0)]
    f = lambda v: f'{"Gain" if v > 0 else "Loss"} of {inr(abs(v))}'
    w = [f(x) for x in wrong if x != net and x != 0]
    w = list(dict.fromkeys(w))
    if len(w) < 3:
        w.append(f(net + 1000))
    return mcq(f'On the admission of a partner: {lst}. The result of revaluation is:', f(net), w[:3],
               f'{"; ".join(("+" if x > 0 else "−") + inr(abs(x)) for _, x in sel)} = {f(net).lower()}.', r)


def c2_reserves(r):
    ns = names(r, 3)
    old = r.choice(R2)
    gr = amt(r, 10000, 90000, 1000)
    pl = amt(r, 5000, 60000, 1000) * r.choice([1, -1])
    wcr = amt(r, 10000, 40000, 1000)
    claim = amt(r, 0, wcr, 1000)
    tot = gr + pl + (wcr - claim)
    sp = split(tot, shares(old))
    return {'stem': f'{ns[0]} and {ns[1]} share profits {":".join(map(str, old))}. On {ns[2]}\'s admission their balance sheet shows general reserve {inr(gr)}, profit and loss account {"(credit) " + inr(pl) if pl > 0 else "(debit) " + inr(-pl)} and workmen compensation reserve {inr(wcr)}. The workmen compensation claim is {inr(claim)}. Calculate the amount credited (or debited) to each old partner\'s capital account for these items.',
            'answer': f'Net {inr(abs(tot))} {"credited" if tot > 0 else "debited"}: {ns[0]} {inr(abs(sp[0]))}, {ns[1]} {inr(abs(sp[1]))}',
            'key': f'General reserve {inr(gr)} {"+" if pl > 0 else "−"} P&L {inr(abs(pl))} + excess WCR {inr(wcr - claim)} = {inr(abs(tot))}; old ratio {":".join(map(str, old))}: {ns[0]} {inr(abs(sp[0]))}, {ns[1]} {inr(abs(sp[1]))}.'}


# ---- st5 capitals and balance sheet

CH02_ST5 = dict(
    cat='term',
    terms=[
        ('Proportionate capital', 'Capital of partners adjusted so that it is in the same proportion as their new profit-sharing ratio.'),
        ('Adjusted capital', 'A partner\'s capital after all adjustments for goodwill, revaluation and reserves.'),
        ('Surplus capital', 'The excess of a partner\'s adjusted capital over the required capital, withdrawn or transferred to current account.'),
        ('Deficient capital', 'The shortfall of a partner\'s adjusted capital from the required capital, brought in cash or debited to current account.'),
    ],
    ars=[
        ('Capitals of old partners may be adjusted on the basis of the new partner\'s capital.', 'Partners may agree that capitals be in the new profit-sharing ratio.', 'a', 'Both true; R explains A.'),
        ('Surplus capital of a partner must always be withdrawn in cash.', 'It may also be transferred to the partner\'s current account.', 'd', 'A is false: it may be withdrawn or transferred to current account. R is true.'),
        ('The balance sheet of the new firm shows assets at revalued figures.', 'Assets were revalued at the time of admission.', 'a', 'Both true; R explains A.')],
    tf=('adjustment of capitals on admission', [
        'Required capital of each partner = total capital × new share.',
        'Deficiency of capital may be brought in cash.',
        'Surplus capital may be transferred to current account.'], [
        'Capitals are always adjusted in the old ratio.',
        'Surplus capital is credited to the Revaluation Account.',
        'The new partner\'s capital is always equal to the old partners\' total.',
        'Deficient capital is credited to the partner\'s capital account without any cash.']),
)


def c2_capadj(r):
    d = retry(_new_ratio, r)
    cap_c = amt(r, 50000, 200000, 5000)
    tot = cap_c / d['nc']
    req = [I(tot * d['na']), I(tot * d['nb'])]
    adj = [x + r.choice([-1, 1]) * amt(r, 5000, 50000, 1000) for x in req]
    if min(adj) <= 0:
        raise ValueError
    diff = [a_ - q for a_, q in zip(adj, req)]
    word = lambda x: f'surplus {inr(x)} (withdrawn)' if x > 0 else f'deficit {inr(-x)} (brought in)' if x < 0 else 'nil'
    return {'stem': f'{d["a"]} and {d["b"]} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. {d["c"]} brings {inr(cap_c)} as capital. After all adjustments, the capitals of {d["a"]} and {d["b"]} are {inr(adj[0])} and {inr(adj[1])}. Their capitals are to be adjusted on the basis of {d["c"]}\'s capital in the new ratio. Find the amount to be brought in or withdrawn.',
            'answer': f'{d["a"]}: {word(diff[0])}; {d["b"]}: {word(diff[1])}',
            'key': f'New ratio {d["nr"]}; total capital = {inr(cap_c)} ÷ {fs(d["nc"])} = {inr(I(tot))}. Required: {d["a"]} {inr(req[0])}, {d["b"]} {inr(req[1])}. {d["a"]} {word(diff[0])}; {d["b"]} {word(diff[1])}.'}


def c2_newcap(r):
    return retry(_c2_newcap, r)


def _c2_newcap(r):
    d = retry(_new_ratio, r)
    adj = [amt(r, 60000, 300000, 5000) for _ in range(2)]
    old_share = d['na'] + d['nb']
    cap_c = I(Fr(sum(adj)) / old_share * d['nc'])
    return {'stem': f'{d["a"]} and {d["b"]} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. Their adjusted capitals are {inr(adj[0])} and {inr(adj[1])}. {d["c"]} is to bring capital proportionate to {d["c"]}\'s share. Calculate {d["c"]}\'s capital.',
            'answer': inr(cap_c),
            'key': f'Combined capital {inr(sum(adj))} for {fs(old_share)} share; total capital = {inr(I(Fr(sum(adj)) / old_share))}; {d["c"]}\'s capital = × {fs(d["nc"])} = {inr(cap_c)}.',
            'distractors': [inr(I(Fr(sum(adj)) * d['nc'])) if (sum(adj) * d['nc']).denominator == 1 else inr(cap_c + 5000), inr(I(Fr(sum(adj)) / old_share)), inr(cap_c * 2)]}


# ================================================================ ch03 Retirement and death

CH03_ST1 = dict(
    cat='term',
    terms=[
        ('Gaining ratio', 'The ratio in which the continuing partners acquire the share of the retiring or deceased partner.'),
        ('Retirement of a partner', 'The withdrawal of a partner from the firm while the remaining partners continue the business.'),
        ('Continuing partners', 'The partners who remain in the firm after a partner retires or dies.'),
        ('Executor', 'The legal representative of a deceased partner to whom the amount due is paid.'),
    ],
    pairs=[('sacrificing ratio', 'gaining ratio', [
        ('meaning', 'ratio in which old partners give up their share', 'ratio in which continuing partners acquire the outgoing partner\'s share'),
        ('when calculated', 'on admission of a partner', 'on retirement or death of a partner'),
        ('formula', 'old ratio − new ratio', 'new ratio − old ratio'),
        ('effect on partners', 'reduces the shares of old partners', 'increases the shares of continuing partners')])],
    ars=[
        ('Gaining ratio = New ratio − Old ratio.', 'Continuing partners acquire the share of the retiring partner.', 'a', 'Both true; R explains A.'),
        ('If continuing partners take the retiring partner\'s share in their old ratio, the gaining ratio equals their old ratio.', 'Each gains in proportion to his old share.', 'a', 'Both true; R explains A.'),
        ('Gaining ratio is calculated on admission of a partner.', 'On admission, old partners sacrifice.', 'd', 'A is false: gaining ratio arises on retirement or death. R is true.')],
    tf=('retirement of a partner', [
        'Gaining ratio = New ratio − Old ratio.',
        'Retirement is a mode of reconstitution of a firm.',
        'Gaining partners compensate the retiring partner for goodwill.'], [
        'Gaining ratio = Old ratio − New ratio.',
        'On retirement the retiring partner\'s share lapses and no one gains.',
        'The new ratio of continuing partners is always equal.',
        'Gaining ratio is the same as sacrificing ratio on admission.']),
)


def _gain(r):
    ns = names(r, 3)
    old = r.choice(R3)
    sh = shares(old)
    ri = r.randrange(3)
    rest = [i for i in range(3) if i != ri]
    mode = r.choice(['old', 'equal', 'given', 'one'])
    new = sh[:]
    new[ri] = Fr(0)
    if mode == 'old':
        t = sh[rest[0]] + sh[rest[1]]
        for i in rest:
            new[i] = sh[i] / t
        txt = f'{ns[ri]} retires and the continuing partners take {ns[ri]}\'s share in their old ratio'
    elif mode == 'equal':
        for i in rest:
            new[i] = sh[i] + sh[ri] / 2
        txt = f'{ns[ri]} retires and {ns[ri]}\'s share is taken equally by {ns[rest[0]]} and {ns[rest[1]]}'
    elif mode == 'one':
        new[rest[0]] = sh[rest[0]] + sh[ri]
        txt = f'{ns[ri]} retires and {ns[ri]}\'s entire share is taken by {ns[rest[0]]}'
    else:
        x = Fr(r.choice([1, 2, 3]), r.choice([4, 5]))
        if x >= 1:
            raise ValueError
        new[rest[0]] = sh[rest[0]] + sh[ri] * x
        new[rest[1]] = sh[rest[1]] + sh[ri] * (1 - x)
        txt = f'{ns[ri]} retires; {ns[rest[0]]} takes {fs(x)} of {ns[ri]}\'s share and {ns[rest[1]]} the rest'
    gain = [new[i] - sh[i] for i in rest]
    if any(g < 0 for g in gain):
        raise ValueError
    gr = rstr([g for g in gain if g > 0]) if all(g > 0 for g in gain) else (f'{ns[rest[0]]} alone' if gain[0] > 0 else f'{ns[rest[1]]} alone')
    nr = rstr([new[i] for i in rest])
    return dict(ns=ns, old=old, sh=sh, ri=ri, rest=rest, txt=txt, new=new, gain=gain, gr=gr, nr=nr, mode=mode)


def c3_gain_mcq(r):
    d = retry(_gain, r)
    if d['mode'] == 'one':
        raise ValueError
    rest = d['rest']
    others = ratio_d(d['gr'], [[d['old'][i] for i in rest][::-1], [1, 1], [d['new'][rest[0]], d['new'][rest[1]]], [d['old'][i] for i in rest], [2, 1], [3, 1]])
    if len(others) < 3:
        raise ValueError
    ns = d['ns']
    return mcq(f'{andj(ns)} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. The gaining ratio of {ns[rest[0]]} and {ns[rest[1]]} is:',
               d['gr'], others[:3], f'Gain = new − old: {fs(d["gain"][0])} and {fs(d["gain"][1])} → {d["gr"]}.', r)


def c3_gain_calc(r):
    d = retry(_gain, r)
    ns, rest = d['ns'], d['rest']
    return {'stem': f'{andj(ns)} share profits in the ratio {":".join(map(str, d["old"]))}. {d["txt"]}. Calculate the new profit-sharing ratio and the gaining ratio.',
            'answer': f'New ratio {ns[rest[0]]}:{ns[rest[1]]} = {d["nr"]}; gaining ratio {d["gr"]}',
            'key': f'New shares {ns[rest[0]]} {fs(d["new"][rest[0]])}, {ns[rest[1]]} {fs(d["new"][rest[1]])} → {d["nr"]} (2 marks); gain = new − old: {fs(d["gain"][0])}, {fs(d["gain"][1])} → {d["gr"]} (1 mark).'}


CH03_ST2 = dict(
    cat='term',
    terms=[
        ('Goodwill adjustment on retirement', 'Debiting the gaining partners and crediting the retiring partner with the retiring partner\'s share of goodwill, in the gaining ratio.'),
        ('Revaluation on retirement', 'Restating assets and liabilities at current values when a partner retires, with the gain or loss shared in the old ratio.'),
        ('Unrecorded asset', 'An asset of the firm not shown in the books, brought in at its value on reconstitution and credited to the Revaluation Account.'),
        ('Hidden goodwill on retirement', 'Goodwill inferred when the amount agreed to be paid to a retiring partner exceeds his capital after all adjustments.'),
    ],
    ars=[
        ('Retiring partner\'s share of goodwill is debited to the gaining partners in the gaining ratio.', 'Gaining partners benefit from the retiring partner\'s share of future profits.', 'a', 'Both true; R explains A.'),
        ('Revaluation profit on retirement is shared by continuing partners only.', 'The retiring partner is entitled to his share of increased asset values.', 'd', 'A is false: all partners share in old ratio. R is true.'),
        ('Accumulated reserves are distributed among all partners in the old ratio on retirement.', 'They were built up while the retiring partner was in the firm.', 'a', 'Both true; R explains A.')],
    tf=('treatment of goodwill and reserves on retirement', [
        'Gaining partners are debited with the retiring partner\'s share of goodwill.',
        'Revaluation gain on retirement is shared by all partners in the old ratio.',
        'Existing goodwill is written off among all partners in the old ratio.'], [
        'Goodwill is credited to the continuing partners on retirement.',
        'Reserves are shared only by the continuing partners.',
        'Revaluation gain is shared in the gaining ratio.',
        'The retiring partner bears the whole of existing goodwill.']),
)


def c3_goodwill(r):
    d = retry(_gain, r)
    ns, rest, ri = d['ns'], d['rest'], d['ri']
    G = amt(r, 60000, 600000, 6000)
    share = I(G * d['sh'][ri])
    tg = sum(d['gain'])
    deb = [I(Fr(share) * g / tg) for g in d['gain']]
    parts = [f"{ns[i]}'s Capital A/c Dr {inr(x)}" for i, x in zip(rest, deb) if x]
    ent = '; '.join(parts) + f"; To {ns[ri]}'s Capital A/c {inr(share)}"
    return {'stem': f'{andj(ns)} share profits {":".join(map(str, d["old"]))}. {d["txt"]}. The goodwill of the firm is valued at {inr(G)}. Pass the journal entry for goodwill.',
            'answer': ent,
            'key': f'{ns[ri]}\'s share = {inr(G)} × {fs(d["sh"][ri])} = {inr(share)}; debited to gaining partners in gaining ratio ({d["gr"]}). Entry: {ent}.'}


def c3_goodwill_mcq(r):
    d = retry(_gain, r)
    ns, ri = d['ns'], d['ri']
    G = amt(r, 60000, 600000, 6000)
    share = I(G * d['sh'][ri])
    return mcq(f'{andj(ns)} share profits {":".join(map(str, d["old"]))}. Goodwill of the firm is {inr(G)}. On {ns[ri]}\'s retirement, {ns[ri]}\'s capital account will be credited with:',
               inr(share), [inr(G), inr(I(Fr(G, 3))) if G % 3 == 0 and I(Fr(G, 3)) != share else inr(share * 2), inr(I(Fr(share, 2)))],
               f'{ns[ri]}\'s share of goodwill = {inr(G)} × {fs(d["sh"][ri])} = {inr(share)}.', r)


def c3_amount_due(r):
    ns = names(r, 3)
    old = r.choice(R3)
    sh = shares(old)
    ri = r.randrange(3)
    cap = amt(r, 80000, 400000, 5000)
    gr = amt(r, 12000, 90000, 6000)
    rev = amt(r, 6000, 60000, 6000) * r.choice([1, -1])
    G = amt(r, 60000, 300000, 6000)
    dr = amt(r, 0, 30000, 1000)
    parts = [I(gr * sh[ri]), I(rev * sh[ri]), I(G * sh[ri])]
    due = cap + sum(parts) - dr
    return {'stem': f'{andj(ns)} share profits {":".join(map(str, old))}. {ns[ri]} retires. {ns[ri]}\'s capital balance is {inr(cap)}; general reserve {inr(gr)}; revaluation {"gain" if rev > 0 else "loss"} {inr(abs(rev))}; goodwill of the firm {inr(G)}; {ns[ri]}\'s drawings for the current year {inr(dr)}. Calculate the amount due to {ns[ri]}.',
            'answer': inr(due),
            'key': f'Capital {inr(cap)} + reserve share {inr(parts[0])} {"+" if rev > 0 else "−"} revaluation share {inr(abs(parts[1]))} + goodwill share {inr(parts[2])} − drawings {inr(dr)} = {inr(due)}.',
            'distractors': [inr(due + dr * 2) if dr else inr(due + 1000), inr(cap + parts[0] - dr), inr(due - parts[2])]}


CH03_ST3 = dict(
    cat='term',
    terms=[
        ('Retiring partner\'s loan account', 'The account to which the amount due to a retiring partner is transferred when it is not paid immediately.'),
        ('Section 37 of the Indian Partnership Act', 'The provision under which an outgoing partner may claim either interest at 6% p.a. or a share of profit attributable to the use of his unpaid share.'),
        ('Payment in instalments', 'Settlement of the retiring partner\'s dues in equal instalments with interest on the unpaid balance.'),
        ('Lump sum payment', 'Payment of the entire amount due to a retiring partner in cash at the time of retirement.'),
    ],
    ars=[
        ('The amount due to a retiring partner may be transferred to his loan account.', 'The firm may not have enough cash to pay immediately.', 'a', 'Both true; R explains A.'),
        ('A retiring partner whose dues remain unpaid can claim interest at 6% p.a. in the absence of agreement.', 'Section 37 gives this option.', 'a', 'Both true; R explains A.'),
        ('Interest on the retiring partner\'s loan is calculated on the original amount for every year.', 'Interest is payable on the unpaid balance.', 'd', 'A is false: interest is on the outstanding balance. R is true.')],
    tf=('settlement of a retiring partner\'s dues', [
        'Unpaid dues may be transferred to the retiring partner\'s loan account.',
        'Interest is charged on the unpaid balance of the loan.',
        'Section 37 lets an outgoing partner claim interest at 6% p.a. or a share of profit.'], [
        'The retiring partner\'s dues must always be paid in cash on the day of retirement.',
        'Interest on the loan is always 12% p.a. under the Act.',
        'The retiring partner\'s loan is shown as an asset.',
        'Instalments do not include interest.']),
)


def c3_instal(r):
    p = r.choice(GIRLS + BOYS)
    n = r.choice([2, 3, 4, 5])
    inst = amt(r, 20000, 100000, 5000)
    L = inst * n
    rate = r.choice([6, 8, 10, 12])
    k = r.randrange(1, n + 1)
    bal = L - inst * (k - 1)
    intr = I(Fr(bal * rate, 100))
    pay = inst + intr
    return {'stem': f'{inr(L)} was due to {p}, a retiring partner, on 31 March 2026. It is to be paid in {n} equal annual instalments starting on 31 March 2027, with interest @ {rate}% p.a. on the unpaid balance. Calculate the total payment (instalment plus interest) to be made on 31 March {2026 + k}.',
            'answer': inr(pay),
            'key': f'Instalment {inr(inst)}; balance outstanding during year {k} = {inr(bal)}; interest {inr(bal)} × {rate}% = {inr(intr)}; payment {inr(pay)}.',
            'distractors': [inr(inst + I(Fr(L * rate, 100))) if k > 1 else inr(pay + inst), inr(inst), inr(pay + I(Fr(inst * rate, 100)))]}


CH03_ST4 = dict(
    cat='term',
    terms=[
        ('Deceased partner\'s executor\'s account', 'The account to which the amount due to a deceased partner is transferred, payable to his legal representative.'),
        ('Profit and Loss Suspense Account', 'A temporary account debited with the deceased partner\'s share of profit up to the date of death.'),
        ('Time basis', 'Estimating the deceased partner\'s share of profit till death on the basis of the previous year\'s or average profit for the period.'),
        ('Turnover (sales) basis', 'Estimating profit till death as the same percentage of sales up to that date as in the previous year.'),
    ],
    ars=[
        ('The deceased partner\'s share of profit till the date of death is debited to the Profit and Loss Suspense Account.', 'Accounts are not closed on the date of death.', 'a', 'Both true; R explains A.'),
        ('The amount due to a deceased partner is paid to his executor.', 'The executor is his legal representative.', 'a', 'Both true; R explains A.'),
        ('Share of profit till death is always calculated on the sales basis.', 'Time basis uses the previous year\'s or average profit.', 'd', 'A is false: either basis may be used. R is true.')],
    tf=('death of a partner', [
        'The deceased partner is entitled to his share of profit up to the date of death.',
        'The amount due is transferred to the executor\'s account.',
        'Share of profit till death may be calculated on time or turnover basis.'], [
        'The firm must prepare a full profit and loss account on the date of death.',
        'The deceased partner gets no share of goodwill.',
        'The executor\'s account is shown as an asset.',
        'Profit till death is credited to the continuing partners.']),
)


def c3_death_time(r):
    ns = names(r, 3)
    old = r.choice(R3)
    sh = shares(old)
    di = r.randrange(3)
    m = r.choice([2, 3, 4, 5, 6, 8, 9])
    mo = MONTHS[m - 1]
    day = {'April': 30, 'May': 31, 'June': 30, 'July': 31, 'August': 31, 'September': 30, 'November': 30, 'December': 31, 'October': 31}[mo]
    basis = r.choice(['last', 'avg'])
    if basis == 'last':
        P = amt(r, 60000, 600000, 12000)
        base = P
        txt = f'the profit of the previous year, {inr(P)}'
    else:
        ps = [amt(r, 60000, 400000, 3000) for _ in range(3)]
        base = Fr(sum(ps), 3)
        I(base)
        txt = f'the average profit of the last three years ({", ".join(inr(p) for p in ps)})'
    shr = I(Fr(base) * m / 12 * sh[di])
    return {'stem': f'{andj(ns)} share profits {":".join(map(str, old))}. {ns[di]} died on {day} {mo} 2025. {ns[di]}\'s share of profit till the date of death is to be calculated on the basis of {txt}. Calculate it and pass the journal entry.',
            'answer': f'{inr(shr)}; Profit and Loss Suspense A/c Dr {inr(shr)}; To {ns[di]}\'s Capital A/c {inr(shr)}',
            'key': f'{inr(I(base))} × {m}/12 × {fs(sh[di])} = {inr(shr)} (2 marks); entry: P&L Suspense A/c Dr; To {ns[di]}\'s Capital A/c (1 mark).',
            'distractors': [inr(I(Fr(base) * sh[di])), inr(I(Fr(base) * (12 - m) / 12 * sh[di])), inr(I(Fr(base) * m / 12))]}


def c3_death_sales(r):
    ns = names(r, 2)
    old = r.choice(R2)
    sh = shares(old)
    S = amt(r, 500000, 3000000, 100000)
    pr = r.choice([5, 8, 10, 12, 15, 20])
    P = I(Fr(S * pr, 100))
    s1 = amt(r, 100000, S // 2, 50000)
    m = r.choice([3, 4, 6, 9])
    share = I(Fr(s1 * pr, 100) * sh[0])
    return {'stem': f'{ns[0]} and {ns[1]} share profits {":".join(map(str, old))}. {ns[0]} died on {["30 June", "31 July", "30 September", "31 December"][[3, 4, 6, 9].index(m)]} 2025. Sales for the previous year were {inr(S)} and the profit was {inr(P)}. Sales from 1 April 2025 to the date of death were {inr(s1)}. Calculate {ns[0]}\'s share of profit till death on the basis of sales.',
            'answer': inr(share),
            'key': f'Profit rate = {inr(P)}/{inr(S)} = {pr}% of sales; profit till death = {inr(s1)} × {pr}% = {inr(I(Fr(s1 * pr, 100)))}; {ns[0]}\'s share × {fs(sh[0])} = {inr(share)}.',
            'distractors': [inr(I(Fr(s1 * pr, 100))), money(Fr(P) * m / 12 * sh[0]), inr(share * 2)]}


# ================================================================ ch04 Dissolution

CH04_ST1 = dict(
    cat='term',
    terms=[
        ('Dissolution of partnership', 'A change in the relation of partners without closing the business; the firm continues with a new agreement.'),
        ('Dissolution of firm', 'The breakdown of the relation of partnership among all the partners, after which the business is closed and accounts are settled.'),
        ('Compulsory dissolution', 'Dissolution when all or all but one partner become insolvent, or the business becomes illegal.'),
        ('Dissolution by court', 'Dissolution ordered by a court on the suit of a partner, for reasons such as insanity, permanent incapacity or misconduct of a partner.'),
        ('Dissolution by notice', 'Dissolution of a partnership at will when a partner gives written notice of intention to dissolve.'),
    ],
    pairs=[('dissolution of partnership', 'dissolution of firm', [
        ('termination of business', 'business continues', 'business is closed'),
        ('settlement of assets and liabilities', 'assets and liabilities are revalued and a new balance sheet drawn', 'assets are sold and liabilities paid off'),
        ('court\'s intervention', 'no court order is needed', 'a firm may be dissolved by order of the court'),
        ('economic relationship', 'the relationship continues among some partners', 'the relationship ends among all partners'),
        ('closure of books', 'books of account are not closed', 'books of account are closed')])],
    scen=[('Identify the mode of dissolution of the firm.', ['Dissolution by agreement', 'Compulsory dissolution', 'Dissolution on happening of certain contingencies', 'Dissolution by notice', 'Dissolution by court'], [
        ('All partners of {f} agree in writing to close the business.', 'Dissolution by agreement', 'Dissolution with the consent of all partners.'),
        ('A government notification makes the business carried on by {f} illegal.', 'Compulsory dissolution', 'The business has become unlawful.'),
        ('{f} was formed for a fixed term of five years and the term has expired.', 'Dissolution on happening of certain contingencies', 'Expiry of the fixed term.'),
        ('{f} is a partnership at will; {p} gives written notice to the other partners to dissolve it.', 'Dissolution by notice', 'In a partnership at will any partner can dissolve by notice.'),
        ('{p}, a partner of {f}, has become of unsound mind and another partner files a suit.', 'Dissolution by court', 'The court may order dissolution on a partner\'s insanity.'),
        ('{f} was formed to complete a single construction project, which is now over.', 'Dissolution on happening of certain contingencies', 'Completion of the venture.'),
        ('All the partners of {f} except one have been declared insolvent.', 'Compulsory dissolution', 'Insolvency of all or all but one partner.'),
        ('{p} has persistently breached the partnership agreement and the others go to court.', 'Dissolution by court', 'Persistent breach of agreement is a ground for the court.')], None)],
    ars=[
        ('Dissolution of partnership does not necessarily mean dissolution of the firm.', 'On reconstitution the business continues under a new agreement.', 'a', 'Both true; R explains A.'),
        ('A firm is compulsorily dissolved if its business becomes illegal.', 'A partnership must be for a lawful business.', 'a', 'Both true; R explains A.'),
        ('Dissolution of a firm always requires a court order.', 'The court can order dissolution on certain grounds.', 'd', 'A is false: firms may also be dissolved by agreement, notice or compulsorily. R is true.')],
    tf=('dissolution', [
        'Dissolution of a firm necessarily involves dissolution of partnership.',
        'A partnership at will may be dissolved by notice.',
        'Insolvency of all but one partner leads to compulsory dissolution.'], [
        'Dissolution of partnership always closes the business.',
        'Admission of a partner dissolves the firm.',
        'A court cannot dissolve a firm.',
        'Books are closed on dissolution of partnership.']),
    cases=[('C4', 'D4', 4, '{p}, {p2} and {p3} are partners in {f}, {c}. {p3} has become permanently incapable of performing the duties of a partner and {p} wants the firm closed, while {p2} wants to continue with a new partner.',
            [('Can the firm be dissolved by the court on this ground? Name the mode.', 'Yes: dissolution by court on permanent incapacity of a partner.'),
             ('If {p} and {p2} continue with a new partner instead, is it dissolution of partnership or of the firm? Why?', 'Dissolution of partnership (reconstitution): the business continues under a new agreement.')]),
           ('C4', 'D5', 4, '{f} was formed by {p} and {p2} for a fixed term of three years to run a trade fair stall in {c}. The term has ended but both want to continue for two more years.',
            [('What happens to the firm on expiry of the term if they do nothing?', 'It is dissolved on the happening of a contingency (expiry of the fixed term).'),
             ('If they continue without a new agreement, what kind of partnership is it?', 'A partnership at will on the same terms, which can later be dissolved by notice.')])],
)

CH04_ST2 = dict(
    cat='term',
    terms=[
        ('Realisation Account', 'A nominal account prepared on dissolution of a firm to record the sale of assets and payment of liabilities and find the profit or loss.'),
        ('Section 48', 'The provision of the Indian Partnership Act laying down the order of settlement of accounts on dissolution.'),
        ('Realisation expenses', 'Costs incurred in selling assets and settling liabilities on dissolution, debited to the Realisation Account.'),
        ('Profit on realisation', 'The credit balance of the Realisation Account, transferred to partners\' capital accounts in their profit-sharing ratio.'),
    ],
    lists=[('s48', 'items in the order of payment out of the firm\'s assets under Section 48', [
        ('Debts of the firm to third parties', 'Outside liabilities are paid first.'),
        ('Advances (loans) by partners', 'Then each partner is paid rateably what is due for advances as distinct from capital.'),
        ('Capitals of partners', 'Then each partner is paid rateably what is due on account of capital.'),
        ('Residue among partners', 'Any surplus is divided among partners in their profit-sharing ratio.')], None)],
    scen=[('Which account is debited/credited on dissolution?', ['Debit Realisation A/c; credit the asset account', 'Debit the liability account; credit Realisation A/c', 'Debit partner\'s Capital A/c; credit Realisation A/c', 'Debit Realisation A/c; credit Bank A/c'], [
        ('Transfer of machinery to the Realisation Account.', 'Debit Realisation A/c; credit the asset account', 'Assets (other than cash and fictitious) are transferred to the debit of Realisation A/c.'),
        ('Transfer of creditors to the Realisation Account.', 'Debit the liability account; credit Realisation A/c', 'Outside liabilities are transferred to its credit.'),
        ('{p}, a partner, takes over stock at an agreed value.', 'Debit partner\'s Capital A/c; credit Realisation A/c', 'Asset taken over by a partner is debited to his capital account.'),
        ('Creditors are paid in cash.', 'Debit Realisation A/c; credit Bank A/c', 'Payment of liabilities is debited to Realisation A/c.'),
        ('Realisation expenses are paid by the firm.', 'Debit Realisation A/c; credit Bank A/c', 'Expenses paid by the firm are debited to Realisation A/c.')], None)],
    ars=[
        ('Cash and bank balances are not transferred to the Realisation Account.', 'They are already in realised form.', 'a', 'Both true; R explains A.'),
        ('A partner\'s loan is transferred to the Realisation Account.', 'Partner\'s loan is paid after outside liabilities.', 'd', 'A is false: it is paid directly through cash/bank, not via Realisation A/c. R is true.'),
        ('Realisation profit is shared by partners in their profit-sharing ratio.', 'It is a gain made on winding up the business.', 'a', 'Both true; R explains A.'),
        ('Accumulated losses are credited to partners\' capital accounts on dissolution.', 'They reduce partners\' claims.', 'd', 'A is false: they are debited. R is true.')],
    tf=('the realisation account', [
        'Assets other than cash and fictitious assets are transferred to its debit.',
        'Outside liabilities are transferred to its credit.',
        'Its balance is profit or loss on realisation.'], [
        'Partners\' loans are transferred to its credit.',
        'Cash in hand is transferred to its debit.',
        'Its balance is transferred to the general reserve.',
        'Fictitious assets are transferred to its debit.']),
)


def _dissolve(r):
    ns = names(r, 2)
    ratio = r.choice(R2)
    sh = shares(ratio)
    A = dict(debtors=amt(r, 20000, 100000, 1000), stock=amt(r, 20000, 120000, 1000), machinery=amt(r, 50000, 300000, 5000),
             investments=amt(r, 10000, 80000, 1000))
    cash = amt(r, 5000, 40000, 1000)
    cred = amt(r, 20000, 100000, 1000)
    bp = amt(r, 5000, 30000, 1000)
    tot_a = sum(A.values()) + cash
    capital_total = tot_a - cred - bp
    if capital_total <= 20000:
        raise ValueError
    c0 = amt(r, capital_total // 4, capital_total * 3 // 4, 1000)
    caps = [c0, capital_total - c0]
    pct = lambda: r.choice([80, 85, 90, 95, 110, 120])
    real = {'debtors': I(Fr(A['debtors'] * r.choice([90, 95, 100]), 100)), 'stock': I(Fr(A['stock'] * pct(), 100)),
            'machinery': I(Fr(A['machinery'] * pct(), 100))}
    take = r.randrange(2)
    inv_val = I(Fr(A['investments'] * r.choice([90, 100, 110, 120]), 100))
    exp = amt(r, 1000, 8000, 500)
    disc = r.choice([0, 5, 10])
    cred_paid = I(Fr(cred * (100 - disc), 100))
    dr_side = sum(A.values()) + cred_paid + bp + exp
    cr_side = cred + bp + sum(real.values()) + inv_val
    profit = cr_side - dr_side
    psh = split(profit, sh) if profit >= 0 else [-x for x in split(-profit, sh)]
    final = [caps[i] + psh[i] - (inv_val if i == take else 0) for i in range(2)]
    if min(final) <= 0:
        raise ValueError
    bank = cash + sum(real.values()) - cred_paid - bp - exp
    if bank != sum(final):
        raise AssertionError('dissolution does not balance')
    stem = (f'{ns[0]} and {ns[1]} share profits {":".join(map(str, ratio))}. Their firm was dissolved on 31 March 2026, when the balance sheet showed: '
            f'creditors {inr(cred)}, bills payable {inr(bp)}, capitals {ns[0]} {inr(caps[0])} and {ns[1]} {inr(caps[1])}; debtors {inr(A["debtors"])}, stock {inr(A["stock"])}, '
            f'machinery {inr(A["machinery"])}, investments {inr(A["investments"])}, cash at bank {inr(cash)}. '
            f'Debtors realised {inr(real["debtors"])}, stock {inr(real["stock"])}, machinery {inr(real["machinery"])}; {ns[take]} took over the investments at {inr(inv_val)}. '
            + (f'Creditors were paid at a discount of {disc}%; ' if disc else 'Creditors were paid in full; ')
            + f'bills payable were paid in full. Realisation expenses were {inr(exp)}.')
    word = 'profit' if profit >= 0 else 'loss'
    return dict(ns=ns, ratio=ratio, stem=stem, profit=profit, psh=psh, final=final, bank=bank, take=take, inv=inv_val, word=word,
                dr=dr_side, cr=cr_side, caps=caps, cred_paid=cred_paid, assets=sum(A.values()), bp=bp, exp=exp)


def c4_realisation(r):
    d = retry(_dissolve, r)
    ns = d['ns']
    return {'stem': d['stem'] + ' Prepare the Realisation Account and find the profit or loss on realisation.',
            'answer': f'Realisation {d["word"]} {inr(abs(d["profit"]))}: {ns[0]} {inr(abs(d["psh"][0]))}, {ns[1]} {inr(abs(d["psh"][1]))}',
            'key': f'Debit: assets at book value {inr(d["assets"])}, creditors paid {inr(d["cred_paid"])}, bills payable {inr(d["bp"])}, expenses {inr(d["exp"])} = {inr(d["dr"])}. '
                   f'Credit: creditors and bills payable transferred, cash realised from assets and investments taken over by {ns[d["take"]]} {inr(d["inv"])} = {inr(d["cr"])}. '
                   f'{d["word"].capitalize()} {inr(abs(d["profit"]))} shared {":".join(map(str, d["ratio"]))}: {ns[0]} {inr(abs(d["psh"][0]))}, {ns[1]} {inr(abs(d["psh"][1]))}.'}


def c4_final(r):
    d = retry(_dissolve, r)
    ns = d['ns']
    return {'stem': d['stem'] + ' Prepare the Realisation Account, partners\' capital accounts and Bank Account.',
            'answer': f'Realisation {d["word"]} {inr(abs(d["profit"]))}; final payments {ns[0]} {inr(d["final"][0])}, {ns[1]} {inr(d["final"][1])}; bank total {inr(d["bank"])}',
            'key': f'Realisation A/c: debit {inr(d["dr"])}, credit {inr(d["cr"])}, {d["word"]} {inr(abs(d["profit"]))} (3 marks). Capital A/cs: {ns[0]} {inr(d["caps"][0])} {"+" if d["profit"] >= 0 else "−"} {inr(abs(d["psh"][0]))}'
                   + (f' − investments {inr(d["inv"])}' if d['take'] == 0 else '') + f' = {inr(d["final"][0])}; {ns[1]} {inr(d["caps"][1])} {"+" if d["profit"] >= 0 else "−"} {inr(abs(d["psh"][1]))}'
                   + (f' − investments {inr(d["inv"])}' if d['take'] == 1 else '') + f' = {inr(d["final"][1])} (2 marks). Bank A/c balances at {inr(d["bank"])} paid to partners (1 mark).'}


def c4_real_mcq(r):
    d = retry(_dissolve, r)
    f = lambda v: f'{"Profit" if v >= 0 else "Loss"} {inr(abs(v))}'
    w = list(dict.fromkeys([f(-d['profit']), f(d['profit'] + d['inv']), f(d['profit'] - 2000)]))
    return mcq(d['stem'] + ' The result of realisation is:', f(d['profit']), w, f'Realisation A/c credit {inr(d["cr"])} − debit {inr(d["dr"])} = {f(d["profit"]).lower()}.', r)


CH04_ST3 = dict(
    cat='term',
    terms=[
        ('Asset taken over by a partner', 'An asset accepted by a partner at an agreed value on dissolution, debited to his capital account and credited to Realisation Account.'),
        ('Liability taken over by a partner', 'A firm\'s liability that a partner agrees to pay, credited to his capital account.'),
        ('Final settlement', 'Payment of the balances of partners\' capital accounts in cash after all assets are realised and liabilities paid.'),
        ('Unrecorded asset on dissolution', 'An asset not shown in the books which, when sold on dissolution, is credited to the Realisation Account.'),
    ],
    scen=[('What is the journal entry on dissolution?', [
        'Realisation A/c Dr; To Partner\'s Capital A/c', 'Partner\'s Capital A/c Dr; To Realisation A/c', 'Partner\'s Loan A/c Dr; To Bank A/c', 'Partner\'s Capital A/c Dr; To Bank A/c'], [
        ('{p}, a partner, agreed to pay the realisation expenses of ₹4,000 out of {his} own pocket.', 'Realisation A/c Dr; To Partner\'s Capital A/c', 'Expenses paid by a partner are credited to his capital.'),
        ('{p} took over the firm\'s car at an agreed value.', 'Partner\'s Capital A/c Dr; To Realisation A/c', 'Asset taken over by a partner is debited to his capital.'),
        ('{p}\'s loan of ₹30,000 to the firm is repaid.', 'Partner\'s Loan A/c Dr; To Bank A/c', 'Partner\'s loan is paid directly in cash.'),
        ('The balance in {p}\'s capital account is paid off in final settlement.', 'Partner\'s Capital A/c Dr; To Bank A/c', 'Final payment closes the capital account.'),
        ('{p} agreed to take over the firm\'s creditors of ₹25,000.', 'Realisation A/c Dr; To Partner\'s Capital A/c', 'A liability taken over by a partner is credited to his capital.')], None)],
    ars=[
        ('Partner\'s loan is paid before partners\' capitals on dissolution.', 'Section 48 ranks advances by partners ahead of capital.', 'a', 'Both true; R explains A.'),
        ('When a partner takes over an asset, his capital account is credited.', 'He is receiving an asset of the firm.', 'd', 'A is false: his capital is debited. R is true.'),
        ('The bank account closes when partners are paid in final settlement.', 'All realised cash is used to pay liabilities and partners.', 'a', 'Both true; R explains A.')],
    tf=('settlement on dissolution', [
        'A partner\'s capital is debited with assets taken over by him.',
        'Partners\' loans are paid after outside liabilities.',
        'Final payments to partners close the bank account.'], [
        'Partners\' capitals are paid before outside liabilities.',
        'A partner\'s loan is transferred to the Realisation Account.',
        'An asset taken over by a partner is credited to his capital.',
        'Realisation loss is credited to partners\' capitals.']),
)


def c4_entry_mcq(r):
    p = r.choice(GIRLS + BOYS)
    x = amt(r, 5000, 80000, 1000)
    cases = [
        (f'{p}, a partner, took over stock of {inr(x)} at an agreed value.', f"{p}'s Capital A/c Dr {inr(x)}; To Realisation A/c {inr(x)}"),
        (f'Realisation expenses of {inr(x)} were paid by {p}, a partner.', f"Realisation A/c Dr {inr(x)}; To {p}'s Capital A/c {inr(x)}"),
        (f'{p}\'s loan of {inr(x)} was paid off.', f"{p}'s Loan A/c Dr {inr(x)}; To Bank A/c {inr(x)}"),
        (f'Creditors of {inr(x)} were paid in cash.', f'Realisation A/c Dr {inr(x)}; To Bank A/c {inr(x)}'),
        (f'An unrecorded asset was sold for {inr(x)}.', f'Bank A/c Dr {inr(x)}; To Realisation A/c {inr(x)}'),
    ]
    i = r.randrange(len(cases))
    t, a = cases[i]
    pool = [f"{p}'s Capital A/c Dr {inr(x)}; To Realisation A/c {inr(x)}", f"Realisation A/c Dr {inr(x)}; To {p}'s Capital A/c {inr(x)}",
            f"{p}'s Loan A/c Dr {inr(x)}; To Bank A/c {inr(x)}", f'Realisation A/c Dr {inr(x)}; To Bank A/c {inr(x)}',
            f'Bank A/c Dr {inr(x)}; To Realisation A/c {inr(x)}', f"Realisation A/c Dr {inr(x)}; To {p}'s Loan A/c {inr(x)}"]
    return mcq(f'On dissolution of a firm: {t} The journal entry is:', a, r.sample([q for q in pool if q != a], 3), a + '.', r)


# ================================================================ families

FAMILIES = {
    S + '01-st1': facts(CH01_ST1) + [FF('C3', 'D2', 'mcq', c1_loan_mcq), FF('C3', 'D3', 'numerical', c1_loan, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c1_loan, marks=3), FF('C2', 'D1', 'mcq', c1_loan_mcq)],
    S + '01-st2': facts(CH01_ST2) + [FF('C3', 'D2', 'numerical', c1_fluct, marks=3, kinds=('m3',)), FF('C3', 'D3', 'numerical', c1_fixed, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c1_fixed, marks=4, kinds=('m4',)), FF('C3', 'D1', 'numerical', c1_fluct, marks=2)],
    S + '01-st3': facts(CH01_ST3) + [FF('C3', 'D2', 'mcq', c1_iod_mcq), FF('C2', 'D2', 'mcq', c1_commission), FF('C3', 'D2', 'numerical', c1_ioc_add, marks=2),
                                     FF('C3', 'D3', 'numerical', c1_iod, marks=3, kinds=('m3',)), FF('C3', 'D3', 'numerical', c1_iod_product, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'long', c1_approp, marks=6, kinds=('m6',)), FF('C4', 'D3', 'multi_step', c1_approp_short, marks=4, kinds=('m4',)),
                                     FF('C3', 'D4', 'long', c1_approp, marks=6, kinds=('m6',)), FF('C3', 'D1', 'mcq', c1_commission), FF('C4', 'D5', 'multi_step', c1_approp_short, marks=4)],
    S + '01-st4': facts(CH01_ST4) + [FF('C3', 'D2', 'mcq', c1_guar_mcq), FF('C3', 'D3', 'numerical', c1_guarantee, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c1_guarantee, marks=4, kinds=('m4',)), FF('C4', 'D4', 'multi_step', c1_past, marks=4, kinds=('m4',)),
                                     FF('C3', 'D4', 'multi_step', c1_past, marks=3, kinds=('m3',)), FF('C2', 'D1', 'mcq', c1_guar_mcq)],
    S + '02-st1': facts(CH02_ST1) + [FF('C3', 'D2', 'numerical', c2_avg, marks=2), FF('C3', 'D3', 'numerical', c2_super, marks=3, kinds=('m3',)),
                                     FF('C3', 'D3', 'numerical', c2_capavg, marks=3, kinds=('m3',)), FF('C3', 'D2', 'numerical', c2_weighted, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c2_avg_adj, marks=4, kinds=('m4',)), FF('C4', 'D3', 'numerical', c2_super, marks=3), FF('C3', 'D1', 'numerical', c2_avg, marks=1),
                                     FF('C4', 'D5', 'multi_step', c2_avg_adj, marks=4)],
    S + '02-st2': facts(CH02_ST2) + [FF('C3', 'D2', 'mcq', c2_newratio), FF('C3', 'D2', 'mcq', c2_sacr_mcq), FF('C3', 'D3', 'numerical', c2_newratio_calc, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c2_newratio_calc, marks=3), FF('C2', 'D1', 'mcq', c2_sacr_mcq), FF('C3', 'D4', 'numerical', c2_newratio_calc, marks=3)],
    S + '02-st3': facts(CH02_ST3) + [FF('C3', 'D2', 'mcq', c2_premium_mcq), FF('C3', 'D3', 'multi_step', c2_premium, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c2_premium, marks=4, kinds=('m4',)), FF('C3', 'D3', 'numerical', c2_hidden, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c2_hidden, marks=3), FF('C2', 'D1', 'mcq', c2_premium_mcq), FF('C3', 'D4', 'multi_step', c2_premium, marks=4)],
    S + '02-st4': facts(CH02_ST4) + [FF('C3', 'D2', 'mcq', c2_reval_mcq), FF('C3', 'D3', 'multi_step', c2_reval, marks=4, kinds=('m4',)),
                                     FF('C3', 'D3', 'numerical', c2_reserves, marks=3, kinds=('m3',)), FF('C4', 'D4', 'long', c2_reval, marks=6, kinds=('m6',)),
                                     FF('C4', 'D3', 'numerical', c2_reserves, marks=3), FF('C2', 'D1', 'mcq', c2_reval_mcq)],
    S + '02-st5': facts(CH02_ST5) + [FF('C3', 'D3', 'multi_step', c2_capadj, marks=4, kinds=('m4',)), FF('C3', 'D2', 'numerical', c2_newcap, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c2_capadj, marks=4), FF('C4', 'D3', 'numerical', c2_newcap, marks=3), FF('C3', 'D4', 'long', c2_capadj, marks=6, kinds=('m6',))],
    S + '03-st1': facts(CH03_ST1) + [FF('C3', 'D2', 'mcq', c3_gain_mcq), FF('C3', 'D3', 'numerical', c3_gain_calc, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c3_gain_calc, marks=3), FF('C2', 'D1', 'mcq', c3_gain_mcq), FF('C3', 'D4', 'numerical', c3_gain_calc, marks=3)],
    S + '03-st2': facts(CH03_ST2) + [FF('C3', 'D2', 'mcq', c3_goodwill_mcq), FF('C3', 'D3', 'multi_step', c3_goodwill, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c3_goodwill, marks=4, kinds=('m4',)), FF('C3', 'D3', 'numerical', c3_amount_due, marks=4, kinds=('m4',)),
                                     FF('C4', 'D3', 'long', c3_amount_due, marks=6, kinds=('m6',)), FF('C2', 'D1', 'mcq', c3_goodwill_mcq), FF('C3', 'D4', 'multi_step', c3_goodwill, marks=3)],
    S + '03-st3': facts(CH03_ST3) + [FF('C3', 'D2', 'numerical', c3_instal, marks=2), FF('C3', 'D3', 'numerical', c3_instal, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c3_amount_due, marks=4, kinds=('m4',)), FF('C3', 'D4', 'numerical', c3_instal, marks=3),
                                     FF('C4', 'D4', 'long', c3_amount_due, marks=6, kinds=('m6',))],
    S + '03-st4': facts(CH03_ST4) + [FF('C3', 'D2', 'numerical', c3_death_time, marks=3, kinds=('m3',)), FF('C3', 'D3', 'numerical', c3_death_sales, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'numerical', c3_death_sales, marks=3), FF('C4', 'D4', 'numerical', c3_death_time, marks=4, kinds=('m4',)), FF('C3', 'D1', 'numerical', c3_death_time, marks=2)],
    S + '04-st1': facts(CH04_ST1),
    S + '04-st2': facts(CH04_ST2) + [FF('C3', 'D3', 'mcq', c4_real_mcq), FF('C3', 'D4', 'long', c4_realisation, marks=6, kinds=('m6',)),
                                     FF('C4', 'D4', 'long', c4_final, marks=6, kinds=('m6',)), FF('C4', 'D3', 'multi_step', c4_realisation, marks=4, kinds=('m4',)),
                                     FF('C2', 'D2', 'mcq', c4_entry_mcq), FF('C4', 'D5', 'long', c4_final, marks=6)],
    S + '04-st3': facts(CH04_ST3) + [FF('C3', 'D2', 'mcq', c4_entry_mcq), FF('C2', 'D1', 'mcq', c4_entry_mcq), FF('C4', 'D4', 'long', c4_final, marks=6, kinds=('m6',)),
                                     FF('C3', 'D3', 'mcq', c4_real_mcq), FF('C4', 'D3', 'multi_step', c4_final, marks=6)],
}
