"""CBSE class 12 accountancy families, ch05-ch06 (Accounting for Share Capital; Issue and Redemption of Debentures)."""
from __future__ import annotations

from fractions import Fraction as Fr

from qbank import mcq, inr
from g11_accountancy_kit import facts, FF, ctx, amt
from g12_accountancy_a import I, money, retry, q

S = 'cbse-g12-accountancy-ch'
CO = ['Ltd', 'Industries Ltd', 'Textiles Ltd', 'Steel Ltd', 'Pharma Ltd', 'Infotech Ltd', 'Foods Ltd', 'Motors Ltd', 'Cements Ltd', 'Paper Ltd', 'Chemicals Ltd', 'Solar Ltd']
CO_NAMES = ['Sunrise', 'Bharat', 'Kaveri', 'Himalaya', 'Ganga', 'Shakti', 'Prakash', 'Narmada', 'Vindhya', 'Aravali', 'Sahyadri', 'Kalinga',
            'Indus', 'Saraswati', 'Godavari', 'Nilgiri', 'Konark', 'Ajanta', 'Satpura', 'Malabar']


def company(r):
    return f'{r.choice(CO_NAMES)} {r.choice(CO)}'


def fv(r):
    return r.choice([10, 10, 10, 100])


# ================================================================ ch05 Share capital

CH05_ST1 = dict(
    cat='term related to share capital',
    terms=[
        ('Authorised capital', 'The maximum amount of share capital a company is authorised to raise, as stated in its memorandum of association.'),
        ('Issued capital', 'The part of authorised capital that is actually offered to the public and others for subscription.'),
        ('Subscribed capital', 'The part of issued capital that has been actually subscribed (taken up) by the public.'),
        ('Called-up capital', 'The part of subscribed capital that the company has asked its shareholders to pay.'),
        ('Paid-up capital', 'The part of called-up capital actually received from the shareholders.'),
        ('Reserve capital', 'The part of uncalled capital that a company, by special resolution, decides to call only in the event of its winding up.'),
        ('Preference shares', 'Shares that carry a preferential right to dividend at a fixed rate and to return of capital on winding up.'),
        ('Equity shares', 'Shares that are not preference shares; they carry voting rights and a dividend that varies with profit.'),
    ],
    lists=[('feat', 'features of a company', [
        ('Separate legal entity', 'A company is distinct from its members in the eyes of law.'),
        ('Perpetual succession', 'Its existence is not affected by the death or exit of members.'),
        ('Limited liability', 'Liability of members is limited to the unpaid amount on their shares.'),
        ('Transferability of shares', 'Shares of a public company can be transferred freely.'),
        ('Separation of ownership and management', 'Shareholders own it; elected directors manage it.'),
        ('Artificial person', 'It is created by law and acts through its directors.')], None)],
    pairs=[('equity shares', 'preference shares', [
        ('rate of dividend', 'varies with profit', 'fixed rate'),
        ('preference in dividend', 'paid after preference dividend', 'paid before equity dividend'),
        ('return of capital on winding up', 'returned after preference capital', 'returned before equity capital'),
        ('voting rights', 'normal voting rights on all matters', 'vote only on matters affecting their rights'),
        ('redemption', 'not redeemable during the life of the company', 'may be redeemed after a fixed period')])],
    scen=[('Which category of share capital is described?', ['Authorised capital', 'Issued capital', 'Subscribed capital', 'Called-up capital', 'Paid-up capital', 'Reserve capital'], [
        ('The memorandum of {f} Ltd allows it to raise up to ₹50 crore by issuing shares.', 'Authorised capital', 'The maximum capital in the memorandum.'),
        ('{f} Ltd offered 2,00,000 shares of ₹10 each to the public out of its authorised capital.', 'Issued capital', 'The part offered for subscription.'),
        ('The public applied for and was allotted 1,80,000 of the shares offered by {f} Ltd.', 'Subscribed capital', 'The part actually taken up.'),
        ('{f} Ltd has asked shareholders to pay ₹8 of the ₹10 per share so far.', 'Called-up capital', 'The amount demanded so far.'),
        ('{f} Ltd has actually received ₹7.80 per share on average after some calls remained unpaid.', 'Paid-up capital', 'The amount actually received.'),
        ('By special resolution, {f} Ltd decided that ₹2 per share uncalled would be called only on winding up.', 'Reserve capital', 'Uncalled capital reserved for winding up.')], None)],
    ars=[
        ('Reserve capital can be called only at the time of winding up of the company.', 'It is created by a special resolution of the company.', 'b', 'Both true, but R (how it is created) does not explain when it can be called.'),
        ('Paid-up capital can never exceed called-up capital.', 'Calls in advance are not part of paid-up capital.', 'a', 'Both true; R explains A.'),
        ('Liability of a shareholder is limited.', 'A shareholder is liable only up to the unpaid amount on his shares.', 'a', 'Both true; R explains A.'),
        ('Preference shareholders have voting rights on all matters.', 'They have a preferential right to dividend.', 'd', 'A is false: they vote only on matters affecting their rights. R is true.')],
    tf=('share capital', [
        'Authorised capital is stated in the memorandum of association.',
        'Paid-up capital = called-up capital − calls in arrears.',
        'Subscribed capital cannot exceed issued capital.'], [
        'Issued capital can exceed authorised capital.',
        'Calls in advance are added to paid-up capital.',
        'Reserve capital can be called at any time by the directors.',
        'Preference shares carry a dividend that varies with profit.']),
    cases=[('C4', 'D4', 4, '{f} Ltd was registered with an authorised capital of ₹1,00,00,000 in shares of ₹10 each. It offered 5,00,000 shares; 4,80,000 were subscribed. ₹8 per share has been called and all money was received except a call of ₹2 per share on 6,000 shares.',
            [('Find the subscribed and called-up capital.', 'Subscribed ₹48,00,000; called-up 4,80,000 × ₹8 = ₹38,40,000.'),
             ('Find the paid-up capital.', '₹38,40,000 − calls in arrears ₹12,000 = ₹38,28,000.')])],
)


def c5_paidup(r):
    co = company(r)
    n = amt(r, 50000, 500000, 10000)
    f = fv(r)
    called = r.choice([f * 6 // 10, f * 7 // 10, f * 8 // 10, f])
    arr_n = amt(r, 500, 5000, 100)
    arr = r.choice([f // 5, f * 3 // 10, f // 10])
    if arr > called:
        raise ValueError
    ca = n * called
    pu = ca - arr_n * arr
    return {'stem': f'{co} issued {q(n)} equity shares of ₹{f} each, all subscribed. ₹{called} per share has been called up. A shareholder holding {q(arr_n)} shares has not paid the last call of ₹{arr} per share. Calculate the called-up and paid-up capital.',
            'answer': f'Called-up {inr(ca)}; paid-up {inr(pu)}',
            'key': f'Called-up = {q(n)} × ₹{called} = {inr(ca)}; calls in arrears {q(arr_n)} × ₹{arr} = {inr(arr_n * arr)}; paid-up = {inr(pu)}.',
            'distractors': [f'Called-up {inr(n * f)}; paid-up {inr(pu)}', f'Called-up {inr(ca)}; paid-up {inr(ca)}', f'Called-up {inr(ca)}; paid-up {inr(ca + arr_n * arr)}']}


def c5_paidup_mcq(r):
    co = company(r)
    n = amt(r, 50000, 500000, 10000)
    called = r.choice([6, 7, 8, 10])
    arr_n = amt(r, 500, 5000, 100)
    arr = r.choice([2, 3])
    ca = n * called
    pu = ca - arr_n * arr
    return mcq(f'{co} issued {q(n)} equity shares of ₹10 each, all subscribed. ₹{called} per share has been called up. Calls of ₹{arr} per share on {q(arr_n)} shares are unpaid. The paid-up capital is:',
               inr(pu), [inr(ca), inr(n * 10) if called != 10 else inr(ca + arr_n * arr), inr(ca + arr_n * arr) if called != 10 else inr(pu - arr_n * arr)],
               f'Called-up {q(n)} × ₹{called} = {inr(ca)} − calls in arrears {inr(arr_n * arr)} = {inr(pu)}.', r)


CH05_ST2 = dict(
    cat='term',
    terms=[
        ('Securities premium', 'The excess of the issue price of shares over their face (nominal) value, credited to the Securities Premium Account.'),
        ('Calls in arrears', 'The amount called up on shares but not paid by shareholders by the due date.'),
        ('Calls in advance', 'Money received from shareholders before the company has called it.'),
        ('Minimum subscription', 'The minimum amount (90% of the issue) that must be subscribed before a company can allot shares.'),
        ('Prospectus', 'The document inviting the public to subscribe to the shares of a company.'),
        ('Issue at par', 'Issue of shares at a price equal to their face value.'),
    ],
    lists=[('sec52', 'purposes for which securities premium may be used under Section 52 of the Companies Act, 2013', [
        ('Issue of fully paid bonus shares', 'Unissued shares may be issued to members as fully paid bonus shares.'),
        ('Writing off preliminary expenses', 'Expenses on formation of the company may be written off.'),
        ('Writing off expenses, commission or discount on issue of securities', 'Costs of issuing shares or debentures may be written off.'),
        ('Premium payable on redemption of preference shares or debentures', 'Premium payable on redemption may be provided.'),
        ('Buy-back of its own shares or securities', 'Under Section 68 the company may buy back its shares.')], None)],
    ars=[
        ('Securities premium cannot be used to pay dividend.', 'Section 52 lists the only purposes for which it may be used.', 'a', 'Both true; R explains A.'),
        ('Interest on calls in arrears may be charged at up to 10% p.a. under Table F.', 'Calls in arrears are amounts called but not paid.', 'b', 'Both true; R defines calls in arrears but does not explain the rate.'),
        ('Calls in advance are shown under share capital.', 'Calls in advance are a liability of the company.', 'd', 'A is false: calls in advance are shown under other current liabilities. R is true.'),
        ('A company cannot allot shares unless minimum subscription is received.', 'SEBI requires 90% of the issue to be subscribed.', 'a', 'Both true; R explains A.'),
        ('Interest on calls in advance is payable at up to 12% p.a. under Table F.', 'Calls in advance are a liability on which interest is paid.', 'a', 'Both true; R explains A.')],
    tf=('issue of shares', [
        'Securities premium is shown under Reserves and Surplus.',
        'Calls in arrears are deducted from subscribed capital in the notes to accounts.',
        'Table F allows interest on calls in advance up to 12% p.a.'], [
        'Securities premium can be used to pay dividend.',
        'Calls in arrears are shown as a current asset.',
        'Calls in advance are added to paid-up share capital.',
        'Table F allows interest on calls in arrears up to 12% p.a.']),
)


def _issue(r):
    co = company(r)
    n = amt(r, 20000, 200000, 1000)
    f = 10
    prem = r.choice([0, 0, 2, 3, 5])
    app, allot = r.choice([(3, 4), (2, 5), (3, 3), (4, 3), (2, 3)])
    call = f - app - allot
    if call < 0:
        raise ValueError
    return co, n, f, prem, app, allot, call


def c5_issue(r):
    co, n, f, prem, app, allot, call = _issue(r)
    pt = f' at a premium of ₹{prem} per share' if prem else ' at par'
    ct = f'and ₹{call} on first and final call' if call else ''
    sch = f'₹{app} on application, ₹{allot}{" (including premium ₹" + str(prem) + ")" if prem else ""} on allotment' + (f' {ct}' if call else '')
    allot_tot = allot + prem
    if prem:
        sch = f'₹{app} on application, ₹{allot_tot} (including premium) on allotment' + (f' and ₹{call} on first and final call' if call else '')
    ent = [f'Bank A/c Dr {inr(n * app)}; To Equity Share Application A/c {inr(n * app)}',
           f'Equity Share Application A/c Dr {inr(n * app)}; To Equity Share Capital A/c {inr(n * app)}',
           f'Equity Share Allotment A/c Dr {inr(n * allot_tot)}; To Equity Share Capital A/c {inr(n * allot)}' + (f'; To Securities Premium A/c {inr(n * prem)}' if prem else ''),
           f'Bank A/c Dr {inr(n * allot_tot)}; To Equity Share Allotment A/c {inr(n * allot_tot)}']
    if call:
        ent += [f'Equity Share First and Final Call A/c Dr {inr(n * call)}; To Equity Share Capital A/c {inr(n * call)}',
                f'Bank A/c Dr {inr(n * call)}; To Equity Share First and Final Call A/c {inr(n * call)}']
    return {'stem': f'{co} issued {q(n)} equity shares of ₹{f} each{pt}, payable {sch}. All shares were applied for and allotted and all money was received. Pass the journal entries.',
            'answer': ' | '.join(ent),
            'key': f'{len(ent)} entries, ½ to 1 mark each: ' + ' | '.join(ent) + f'. Share capital {inr(n * f)}' + (f'; securities premium {inr(n * prem)}.' if prem else '.')}


def c5_allot_mcq(r):
    co, n, f, prem, app, allot, call = _issue(r)
    if not prem:
        prem = r.choice([2, 3, 5])
    a = inr(n * (allot + prem))
    return mcq(f'{co} issued {q(n)} shares of ₹10 each at a premium of ₹{prem}, payable ₹{app} on application, ₹{allot} plus premium on allotment and the balance on call. All shares were allotted. The amount due on allotment is:',
               a, [inr(n * allot), inr(n * (app + allot + prem)), inr(n * (allot + prem) + n * app // 2)], f'{q(n)} × ₹{allot + prem} = {a}.', r)


def c5_arrears(r):
    co, n, f, prem, app, allot, call = _issue(r)
    if not call:
        raise ValueError
    k = amt(r, 200, 3000, 100)
    m = r.choice([2, 3, 4, 6])
    adv = r.random() < 0.5
    if adv:
        intr = money(Fr(k * call * 12 * m, 1200))
        return {'stem': f'{co} issued shares of ₹10 each payable ₹{app} on application, ₹{allot} on allotment and ₹{call} on first and final call. {ctx(r)["p"]}, holding {q(k)} shares, paid the call money along with the allotment money. The call was made {m} months after allotment. Calculate the interest payable on calls in advance as per Table F.',
                'answer': intr,
                'key': f'Calls in advance {q(k)} × ₹{call} = {inr(k * call)}; interest @ 12% p.a. (Table F) for {m} months = {intr}.',
                'distractors': [money(Fr(k * call * 10 * m, 1200)), money(Fr(k * call * 12, 100)), money(Fr(k * call * 6 * m, 1200))]}
    intr = money(Fr(k * call * 10 * m, 1200))
    return {'stem': f'{co} made the first and final call of ₹{call} per share. {ctx(r)["p"]}, holding {q(k)} shares, paid the call {m} months after the due date. Calculate the interest on calls in arrears as per Table F.',
            'answer': intr,
            'key': f'Calls in arrears {q(k)} × ₹{call} = {inr(k * call)}; interest @ 10% p.a. (Table F) for {m} months = {intr}.',
            'distractors': [money(Fr(k * call * 12 * m, 1200)), money(Fr(k * call * 10, 100)), money(Fr(k * call * 6 * m, 1200))]}


CH05_ST3 = dict(
    cat='term',
    terms=[
        ('Over-subscription', 'A situation in which applications are received for more shares than are offered.'),
        ('Pro-rata allotment', 'Allotment of shares in proportion to the shares applied for, when an issue is over-subscribed.'),
        ('Under-subscription', 'A situation in which applications are received for fewer shares than are offered.'),
        ('Excess application money', 'Application money received on shares applied for but not allotted, adjusted towards allotment (and calls) or refunded.'),
    ],
    scen=[('How should the company deal with the applications?', ['Reject some applications and refund their money', 'Allot shares on a pro-rata basis', 'Combine rejection and pro-rata allotment', 'Allot all shares applied for'], [
        ('{f} Ltd offered 1,00,000 shares and received applications for 1,30,000; it decided to refuse 30,000 applications outright.', 'Reject some applications and refund their money', 'Excess applications rejected in full; money refunded.'),
        ('{f} Ltd offered 1,00,000 shares and received applications for 1,50,000; every applicant got two shares for every three applied.', 'Allot shares on a pro-rata basis', 'Proportional allotment to all applicants.'),
        ('{f} Ltd received applications for 1,80,000 shares against 1,00,000 offered; it rejected 30,000 and allotted the rest pro rata.', 'Combine rejection and pro-rata allotment', 'Part rejection and part pro-rata.')], None)],
    ars=[
        ('Excess application money received on pro-rata allotment is adjusted towards the allotment amount.', 'Shareholders allotted fewer shares than applied for have paid more than needed on application.', 'a', 'Both true; R explains A.'),
        ('Application money on rejected applications is credited to share capital.', 'Rejected applicants get no shares.', 'd', 'A is false: it is refunded. R is true.'),
        ('Excess application money beyond allotment dues may be adjusted towards calls.', 'This is permitted only if the company\'s articles allow it; otherwise it is refunded.', 'a', 'Both true; R explains A.')],
    tf=('over-subscription', [
        'Money on rejected applications is refunded.',
        'Excess application money on pro-rata allotment is adjusted towards allotment.',
        'Shares cannot be allotted beyond the number offered.'], [
        'All applicants must be allotted the shares they applied for.',
        'Excess application money is credited to securities premium.',
        'Money on rejected applications is credited to share forfeiture.',
        'Over-subscription means fewer applications than shares offered.']),
)


def _prorata(r):
    co = company(r)
    off = amt(r, 50000, 300000, 10000)
    rat = r.choice([Fr(3, 2), Fr(2), Fr(5, 4), Fr(4, 3), Fr(5, 3)])
    applied = I(off * rat)
    app, allot = r.choice([(2, 3), (3, 3), (3, 4), (4, 3), (2, 4), (3, 5)])
    prem = r.choice([0, 2, 3])
    k_applied = amt(r, 300, 6000, 60)
    k_allot = I(Fr(k_applied) / rat)
    excess = (k_applied - k_allot) * app
    due = k_allot * (allot + prem)
    pay = due - excess
    return co, off, applied, rat, app, allot, prem, k_applied, k_allot, excess, due, pay


def c5_prorata(r):
    co, off, applied, rat, app, allot, prem, ka, kl, ex, due, pay = retry(_prorata, r)
    p = ctx(r)['p']
    pt = f' at a premium of ₹{prem}' if prem else ''
    al = f'₹{allot + prem} (including premium)' if prem else f'₹{allot}'
    res = f'pays {inr(pay)} on allotment' if pay > 0 else (f'gets a refund of {inr(-pay)}' if pay < 0 else 'pays nothing on allotment')
    return {'stem': f'{co} offered {q(off)} shares of ₹10 each{pt}, payable ₹{app} on application and {al} on allotment, the rest on calls. Applications were received for {q(applied)} shares and shares were allotted pro rata; excess application money was adjusted towards allotment and any surplus refunded. {p} applied for {q(ka)} shares. How many shares will {p} get and how much will {p} pay on allotment?',
            'answer': f'{q(kl)} shares; {res}',
            'key': f'Pro-rata {q(applied)}:{q(off)} = {fs_(rat)}; shares allotted {q(ka)} ÷ {fs_(rat)} = {q(kl)}. Paid on application {q(ka)} × ₹{app} = {inr(ka * app)}; needed {inr(kl * app)}; excess {inr(ex)}. Due on allotment {q(kl)} × ₹{allot + prem} = {inr(due)}; less excess = {inr(pay) if pay >= 0 else "refund " + inr(-pay)}.',
            'distractors': [f'{q(kl)} shares; pays {inr(due)} on allotment', f'{q(ka)} shares; pays {inr(ka * (allot + prem))} on allotment', f'{q(kl)} shares; pays {inr(abs(pay) + kl * app)} on allotment']}


def fs_(x):
    x = Fr(x)
    return f'{x.numerator}:{x.denominator}'


def c5_prorata_mcq(r):
    v = c5_prorata(r)
    return mcq(v['stem'], v['answer'], v['distractors'], v['key'], r)


def c5_prorata_entries(r):
    co, off, applied, rat, app, allot, prem, ka, kl, ex, due, pay = retry(_prorata, r)
    rej = r.choice([0, amt(r, 5000, 20000, 1000)])
    applied2 = applied + rej
    tot_app = applied2 * app
    ex_total = (applied - off) * app
    allot_total = off * (allot + prem)
    ent = [f'Bank A/c Dr {inr(tot_app)}; To Share Application A/c {inr(tot_app)}',
           f'Share Application A/c Dr {inr(tot_app)}; To Share Capital A/c {inr(off * app)}; To Share Allotment A/c {inr(ex_total)}' + (f'; To Bank A/c {inr(rej * app)}' if rej else ''),
           f'Share Allotment A/c Dr {inr(allot_total)}; To Share Capital A/c {inr(off * allot)}' + (f'; To Securities Premium A/c {inr(off * prem)}' if prem else ''),
           f'Bank A/c Dr {inr(allot_total - ex_total)}; To Share Allotment A/c {inr(allot_total - ex_total)}']
    if allot_total - ex_total <= 0:
        raise ValueError
    pt = f' at a premium of ₹{prem}' if prem else ''
    rj = f' Applications for {q(rej)} shares were rejected and their money refunded; the rest were allotted pro rata.' if rej else ' Shares were allotted pro rata.'
    return {'stem': f'{co} invited applications for {q(off)} shares of ₹10 each{pt}, payable ₹{app} on application and ₹{allot}{" plus premium" if prem else ""} on allotment. Applications were received for {q(applied2)} shares.{rj} Excess application money was adjusted towards allotment and all allotment money was received. Pass journal entries up to receipt of allotment.',
            'answer': ' | '.join(ent),
            'key': '1 mark for each entry, 2 marks for correct adjustment of excess: ' + ' | '.join(ent)}


CH05_ST4 = dict(
    cat='term',
    terms=[
        ('Forfeiture of shares', 'Cancellation of shares by the company for non-payment of allotment or call money, the amount already paid being retained.'),
        ('Reissue of forfeited shares', 'Sale of forfeited shares by the company, which may be at par, premium or discount up to the amount forfeited.'),
        ('Share Forfeiture Account', 'The account credited with the amount received on forfeited shares; its balance is shown under share capital until reissue.'),
        ('Capital reserve on reissue', 'The gain on forfeited shares remaining after reissue, transferred from Share Forfeiture Account.'),
    ],
    ars=[
        ('Discount on reissue of forfeited shares cannot exceed the amount forfeited on those shares.', 'Shares reissued must be treated as fully paid up to their face value.', 'a', 'Both true; R explains A.'),
        ('The balance of share forfeiture on reissued shares is transferred to Capital Reserve.', 'It is a capital profit.', 'a', 'Both true; R explains A.'),
        ('When shares issued at premium are forfeited after the premium is received, Securities Premium is debited.', 'Premium once received is not cancelled on forfeiture.', 'd', 'A is false: premium received is not debited. R is true.'),
        ('Share Forfeiture Account balance is shown under Reserves and Surplus.', 'It is added to paid-up capital in the notes to accounts.', 'd', 'A is false: it is shown under Share Capital. R is true.')],
    tf=('forfeiture and reissue of shares', [
        'Share capital is debited with the called-up amount of forfeited shares.',
        'Discount on reissue cannot exceed the amount forfeited.',
        'Gain on reissue is transferred to capital reserve.'], [
        'Share capital is debited with the face value of forfeited shares even if not fully called.',
        'Forfeited amount is credited to the statement of profit and loss.',
        'Forfeited shares cannot be reissued.',
        'Gain on reissue is transferred to general reserve.']),
)


def _forfeit(r):
    co = company(r)
    f = 10
    prem = r.choice([0, 2, 3])
    app, allot = r.choice([(3, 3), (2, 4), (3, 4), (2, 3)])
    call = f - app - allot
    n = amt(r, 100, 2000, 100)
    stage = r.choice(['allot', 'call']) if call else 'allot'
    if stage == 'allot':
        paid = app
        cap_dr = f if not call else app + allot
        called_note = 'allotment money' + (' and the first and final call' if call else '')
        sp_dr = prem
        unpaid_allot = allot + prem
        unpaid_call = call
        if call:
            cap_dr = f
    else:
        paid = app + allot
        cap_dr = f
        called_note = 'the first and final call'
        sp_dr = 0
        unpaid_allot = 0
        unpaid_call = call
    forf = n * paid
    return co, f, prem, app, allot, call, n, stage, paid, cap_dr, called_note, sp_dr, unpaid_allot, unpaid_call, forf


def c5_forfeit(r):
    co, f, prem, app, allot, call, n, stage, paid, cap_dr, note, sp_dr, ua, uc, forf = _forfeit(r)
    p = ctx(r)['p']
    pt = f' at a premium of ₹{prem}' if prem else ''
    al = f'₹{allot + prem} (including premium)' if prem else f'₹{allot}'
    cr = []
    if ua:
        cr.append(f'To Share Allotment A/c {inr(n * ua)}')
    if uc:
        cr.append(f'To Share First and Final Call A/c {inr(n * uc)}')
    cr.append(f'To Share Forfeiture A/c {inr(forf)}')
    dr = [f'Share Capital A/c Dr {inr(n * cap_dr)}'] + ([f'Securities Premium A/c Dr {inr(n * sp_dr)}'] if sp_dr else [])
    ent = '; '.join(dr + cr)
    return {'stem': f'{co} issued shares of ₹10 each{pt}, payable ₹{app} on application, {al} on allotment' + (f' and ₹{call} on first and final call' if call else '') + f'. {p}, holding {q(n)} shares, did not pay {note}. ' + ('After the first and final call was made, the shares were forfeited.' if call else 'The shares were forfeited.') + ' Pass the journal entry for forfeiture.',
            'answer': ent,
            'key': f'Share capital debited with called-up {q(n)} × ₹{cap_dr} = {inr(n * cap_dr)}' + (f'; securities premium not received, debited {inr(n * sp_dr)}' if sp_dr else '') + f'; unpaid amounts credited; amount received {q(n)} × ₹{paid} = {inr(forf)} credited to Share Forfeiture. Entry: {ent}.'}


def c5_reissue(r):
    co, f, prem, app, allot, call, n, stage, paid, cap_dr, note, sp_dr, ua, uc, forf = _forfeit(r)
    m = amt(r, 100, n, 100)
    disc = r.randrange(0, paid)
    price = f - disc
    per = Fr(forf, n)
    cr = I(per * m) - disc * m
    ent = (f'Bank A/c Dr {inr(price * m)}; Share Forfeiture A/c Dr {inr(disc * m)}; To Share Capital A/c {inr(f * m)}' if disc else f'Bank A/c Dr {inr(f * m)}; To Share Capital A/c {inr(f * m)}')
    ent += f'. Share Forfeiture A/c Dr {inr(cr)}; To Capital Reserve A/c {inr(cr)}' if cr else ''
    return {'stem': f'{q(n)} shares of ₹10 each, on which ₹{paid} per share had been received, were forfeited. {q(m)} of these shares were reissued at ₹{price} per share as fully paid. Pass the entries for reissue and the transfer to capital reserve.',
            'answer': ent,
            'key': f'Forfeited per share ₹{paid}; on {q(m)} reissued shares {inr(paid * m)}; discount allowed {inr(disc * m)}; capital reserve = {inr(paid * m)} − {inr(disc * m)} = {inr(cr)}. Entries: {ent}.'}


def c5_capres_mcq(r):
    n = amt(r, 200, 3000, 100)
    paid = r.choice([3, 4, 5, 6, 7])
    m = amt(r, 100, n, 100)
    disc = r.randrange(0, paid + 1)
    cr = (paid - disc) * m
    w = list(dict.fromkeys([inr(paid * n - disc * m), inr(paid * m), inr(disc * m) if disc * m != cr else inr(cr + 100), inr(paid * n)]))
    w = [x for x in w if x != inr(cr)]
    return mcq(f'{q(n)} shares of ₹10 each, on which ₹{paid} per share was paid, were forfeited. {q(m)} of them were reissued at ₹{10 - disc} per share fully paid. The amount transferred to capital reserve is:',
               inr(cr), w[:3], f'({paid} − {disc}) × {q(m)} = {inr(cr)}.', r)


def c5_forfeit_mcq(r):
    co, f, prem, app, allot, call, n, stage, paid, cap_dr, note, sp_dr, ua, uc, forf = _forfeit(r)
    return mcq(f'{q(n)} shares of ₹10 each, issued{" at a premium of ₹" + str(prem) if prem else " at par"}, on which ₹{paid} per share{" (excluding premium)" if prem and stage == "call" else ""} had been received, were forfeited for non-payment of {note}. The amount credited to Share Forfeiture Account is:',
               inr(forf), [inr(n * f), inr(n * (paid + prem)) if prem else inr(n * (f - paid)), inr(n * cap_dr - forf) if n * cap_dr - forf != forf else inr(forf + n)],
               f'Amount received towards capital: {q(n)} × ₹{paid} = {inr(forf)}.', r)


CH05_ST5 = dict(
    cat='term',
    terms=[
        ('Issue of shares for consideration other than cash', 'Allotment of fully paid shares to vendors in payment for assets purchased or services received.'),
        ('Private placement', 'An offer of securities to a select group of persons (not more than 200 in a financial year) other than by public issue.'),
        ('Employees Stock Option Plan (ESOP)', 'A scheme giving employees the option to buy shares of the company at a future date at a predetermined price.'),
        ('Sweat equity shares', 'Shares issued to directors or employees at a discount or for consideration other than cash for providing know-how or value additions.'),
        ('Vendor', 'The seller of assets or business to the company, who may be paid by allotment of shares.'),
    ],
    ars=[
        ('When shares are issued to a vendor, no cash is received.', 'Shares are allotted in consideration of assets purchased.', 'a', 'Both true; R explains A.'),
        ('Private placement can be made to any number of persons in a year.', 'Private placement is an offer to a select group of persons.', 'd', 'A is false: limited to 200 persons in a financial year (excluding QIBs and employees under ESOP). R is true.'),
        ('Sweat equity shares may be issued for providing know-how.', 'They reward value addition by employees or directors.', 'a', 'Both true; R explains A.')],
    tf=('issue of shares other than for cash', [
        'Number of shares to vendor = purchase consideration ÷ issue price.',
        'Shares issued to vendors are shown as issued for consideration other than cash.',
        'Private placement is limited to 200 persons in a financial year.'], [
        'Shares issued to vendors are partly paid.',
        'Number of shares = purchase consideration ÷ face value, even when issued at a premium.',
        'ESOP shares must be bought by employees immediately.',
        'Sweat equity shares are issued only to the public.']),
)


def c5_vendor(r):
    co = company(r)
    f = 10
    prem = r.choice([0, 2, 5, 10])
    price = f + prem
    n = amt(r, 5000, 100000, 500)
    pc = n * price
    cash = r.choice([0, amt(r, 10000, 100000, 2000)])
    tot = pc + cash
    assets = {'Building': amt(r, tot // 3, tot // 2, 1000)}
    assets['Machinery'] = amt(r, (tot - assets['Building']) // 3, (tot - assets['Building']) * 2 // 3, 1000)
    assets['Stock'] = tot - assets['Building'] - assets['Machinery']
    if assets['Stock'] <= 0:
        raise ValueError
    at = ', '.join(f'{k.lower()} {inr(v)}' for k, v in assets.items())
    ent = ('Building A/c Dr; Machinery A/c Dr; Stock A/c Dr; To Vendor A/c ' + inr(tot) + '. Vendor A/c Dr ' + inr(tot) + '; '
           + (f'To Bank A/c {inr(cash)}; ' if cash else '') + f'To Equity Share Capital A/c {inr(n * f)}' + (f'; To Securities Premium A/c {inr(n * prem)}' if prem else ''))
    pt = f'fully paid equity shares of ₹10 each at a premium of ₹{prem}' if prem else 'fully paid equity shares of ₹10 each at par'
    return {'stem': f'{co} purchased assets from a vendor: {at}. ' + (f'It paid {inr(cash)} in cash and the balance by issuing {pt}.' if cash else f'It paid the whole amount by issuing {pt}.') + ' Calculate the number of shares issued and pass the journal entries.',
            'answer': f'{q(n)} shares; {ent}',
            'key': f'Purchase consideration {inr(tot)}; paid in shares {inr(pc)}; number = {inr(pc)} ÷ ₹{price} = {q(n)} (1 mark). Entries: {ent} (2 marks).',
            'distractors': [f'{q(pc // f)} shares', f'{q(tot // price)} shares' if tot % price == 0 and cash else f'{q(n + 500)} shares', f'{q(n * 2)} shares']}


def c5_vendor_mcq(r):
    v = retry(c5_vendor, r)
    a = v['answer'].split(';')[0]
    d = [x for x in dict.fromkeys(v['distractors']) if x != a]
    if len(d) < 3:
        raise ValueError
    return mcq(v['stem'].replace(' Calculate the number of shares issued and pass the journal entries.', ' The number of shares issued is:'), a, d[:3], v['key'], r)


# ================================================================ ch06 Debentures

CH06_ST1 = dict(
    cat='type of debenture',
    terms=[
        ('Debenture', 'A written instrument acknowledging a debt, issued under the common seal or authority of a company, with a fixed rate of interest.'),
        ('Secured debentures', 'Debentures secured by a charge on the assets of the company.'),
        ('Unsecured debentures', 'Debentures that do not carry any charge on the assets of the company.'),
        ('Redeemable debentures', 'Debentures repayable on a specified date or after a specified period.'),
        ('Irredeemable debentures', 'Debentures not repayable during the life of the company, repayable only on winding up.'),
        ('Convertible debentures', 'Debentures that can be converted into equity shares after a specified period.'),
        ('Zero coupon debentures', 'Debentures carrying no specific rate of interest, issued at a large discount and redeemed at par.'),
        ('Registered debentures', 'Debentures whose holders\' names and particulars are recorded in the company\'s register; transferable only by a transfer deed.'),
        ('Bearer debentures', 'Debentures transferable by mere delivery, with interest paid to the holder.'),
    ],
    pairs=[('shares', 'debentures', [
        ('ownership', 'shareholders are owners of the company', 'debenture holders are creditors of the company'),
        ('return', 'dividend, paid out of profits', 'interest at a fixed rate, payable even if there is no profit'),
        ('repayment', 'not repaid during the life of the company (except buy-back/redemption of preference shares)', 'repaid after a fixed period'),
        ('voting rights', 'equity shareholders have voting rights', 'no voting rights'),
        ('security', 'not secured', 'generally secured by a charge on assets'),
        ('issue at discount', 'shares cannot be issued at a discount (except sweat equity)', 'can be issued at a discount'),
        ('convertibility', 'shares cannot be converted into debentures', 'debentures can be converted into shares')])],
    ars=[
        ('Interest on debentures is a charge against profit.', 'It is payable whether or not the company earns a profit.', 'a', 'Both true; R explains A.'),
        ('Debenture holders are owners of the company.', 'Debenture holders get a fixed rate of interest.', 'd', 'A is false: they are creditors. R is true.'),
        ('Zero coupon debentures are issued at a discount.', 'They carry no specific rate of interest; the discount is the return.', 'a', 'Both true; R explains A.'),
        ('Debentures can be issued at a discount, but shares generally cannot.', 'Section 53 prohibits issue of shares at a discount except sweat equity shares.', 'a', 'Both true; R explains A.')],
    tf=('debentures', [
        'A debenture holder is a creditor of the company.',
        'Interest on debentures is payable even if there is a loss.',
        'Debentures can be issued at a discount.'], [
        'Debenture holders have voting rights at general meetings.',
        'Interest on debentures is an appropriation of profit.',
        'Debentures cannot be converted into shares.',
        'Bearer debentures are transferable only by a transfer deed.']),
    cases=[('C4', 'D4', 4, '{f} Ltd needs ₹5 crore for expansion. {p}, its finance manager, compares issuing equity shares with issuing 9% debentures. The company has stable profits and its owners do not want to dilute control.',
            [('Which option suits the owners\' wish? Give two reasons.', 'Debentures: debenture holders have no voting rights, so control is not diluted; interest is tax-deductible and the cost is fixed.'),
             ('State one risk of choosing debentures.', 'Interest must be paid even in a loss year and the principal must be repaid; a charge on assets is created.')]),
           ('C4', 'D5', 4, '{p} holds debentures of {f} Ltd that can be exchanged for equity shares after three years, while {p2} holds debentures that carry no interest but were bought at ₹70 for ₹100 repayable after five years.',
            [('Identify the type of debentures held by each.', '{p}: convertible debentures; {p2}: zero coupon (deep discount) debentures.'),
             ('How does {p2} earn a return?', 'The difference between the issue price ₹70 and the redemption value ₹100 is the return.')])],
)

CASES6 = [('par', 'par'), ('discount', 'par'), ('premium', 'par'), ('par', 'premium'), ('discount', 'premium'), ('premium', 'premium')]


def _deb(r):
    co = company(r)
    n = amt(r, 1000, 20000, 500)
    fvd = 100
    rate = r.choice([8, 9, 10, 11, 12])
    iss, red = r.choice(CASES6)
    di = r.choice([5, 10]) if iss != 'par' else 0
    rp = r.choice([5, 10]) if red == 'premium' else 0
    price = fvd - di if iss == 'discount' else fvd + di if iss == 'premium' else fvd
    rv = fvd + rp
    return co, n, fvd, rate, iss, red, di, rp, price, rv


def _deb_txt(iss, red, di, rp):
    a = 'at par' if iss == 'par' else f'at a {"discount" if iss == "discount" else "premium"} of {di}%'
    b = 'redeemable at par' if red == 'par' else f'redeemable at a premium of {rp}%'
    return a, b


def c6_issue(r):
    co, n, fvd, rate, iss, red, di, rp, price, rv = _deb(r)
    a, b = _deb_txt(iss, red, di, rp)
    dr = [f'Bank A/c Dr {inr(n * price)}']
    if iss == 'discount' or rp:
        loss = n * ((di if iss == 'discount' else 0) + rp)
        dr.append(f'Loss on Issue of Debentures A/c Dr {inr(loss)}')
    cr = [f'To {rate}% Debentures A/c {inr(n * fvd)}']
    if iss == 'premium':
        cr.append(f'To Securities Premium A/c {inr(n * di)}')
    if rp:
        cr.append(f'To Premium on Redemption of Debentures A/c {inr(n * rp)}')
    ent = '; '.join(dr + cr)
    return {'stem': f'{co} issued {q(n)} {rate}% debentures of ₹100 each {a}, {b}. The whole amount was received with the application. Pass the journal entry for issue (application and allotment combined).',
            'answer': ent,
            'key': f'Cash received {q(n)} × ₹{price} = {inr(n * price)}. ' + ('Loss on issue = discount + premium on redemption. ' if (iss == 'discount' or rp) else '') + f'Entry: {ent}.'}


def c6_loss_mcq(r):
    co, n, fvd, rate, iss, red, di, rp, price, rv = _deb(r)
    if iss != 'discount' and not rp:
        raise ValueError
    a, b = _deb_txt(iss, red, di, rp)
    loss = n * ((di if iss == 'discount' else 0) + rp)
    w = list(dict.fromkeys([inr(n * di) if n * di != loss else inr(loss + n), inr(n * rp) if n * rp != loss and rp else inr(loss * 2), inr(n * abs(di - rp)) if n * abs(di - rp) not in (loss, 0) else inr(loss + 2 * n)]))
    w = [x for x in w if x != inr(loss)]
    if len(w) < 3:
        w.append(inr(n * 100))
    return mcq(f'{co} issued {q(n)} debentures of ₹100 each {a}, {b}. The amount debited to Loss on Issue of Debentures Account is:',
               inr(loss), w[:3], f'Loss = ({"discount ₹" + str(di) + " + " if iss == "discount" else ""}premium on redemption ₹{rp}) × {q(n)} = {inr(loss)}.' if rp else f'Discount ₹{di} × {q(n)} = {inr(loss)}.', r)


def c6_case_mcq(r):
    co, n, fvd, rate, iss, red, di, rp, price, rv = _deb(r)
    a, b = _deb_txt(iss, red, di, rp)
    return mcq(f'{co} issued {rate}% debentures of ₹100 each {a}, {b}. The amount received per debenture and the amount payable on redemption per debenture are:',
               f'₹{price} received; ₹{rv} payable', [f'₹{rv} received; ₹{price} payable', f'₹100 received; ₹{rv} payable' if price != 100 else f'₹{price + 5} received; ₹{rv} payable', f'₹{price} received; ₹100 payable' if rv != 100 else f'₹{price} received; ₹105 payable'],
               f'Issue price ₹{price}; redemption value ₹{rv}.', r)


CH06_ST2 = dict(
    cat='term',
    terms=[
        ('Issue at a discount', 'Issue of debentures at a price below their face value.'),
        ('Premium on redemption', 'The amount payable on redemption of debentures over their face value, a liability created at the time of issue.'),
        ('Loss on issue of debentures', 'The total of discount on issue and premium payable on redemption, debited at the time of issue.'),
        ('Redemption of debentures', 'Repayment of the amount of debentures by the company to the debenture holders.'),
    ],
    scen=[('Which account is credited for the premium element?', ['Securities Premium A/c', 'Premium on Redemption of Debentures A/c', 'Loss on Issue of Debentures A/c', 'No premium account is credited'], [
        ('{f} Ltd issued debentures of ₹100 each at ₹105, redeemable at par.', 'Securities Premium A/c', 'Premium on issue is credited to Securities Premium.'),
        ('{f} Ltd issued debentures of ₹100 each at par, redeemable at ₹110.', 'Premium on Redemption of Debentures A/c', 'Premium payable on redemption is a liability.'),
        ('{f} Ltd issued debentures of ₹100 each at par, redeemable at par.', 'No premium account is credited', 'No premium on issue or redemption.')], None)],
    ars=[
        ('Premium on redemption of debentures is a personal account.', 'It is a liability payable to debenture holders on redemption.', 'a', 'Both true; R explains A.'),
        ('Loss on issue of debentures includes premium payable on redemption.', 'The premium is a loss the company will bear in future.', 'a', 'Both true; R explains A.'),
        ('Premium on issue of debentures is credited to the statement of profit and loss.', 'It is a capital gain.', 'd', 'A is false: it goes to Securities Premium. R is true.')],
    tf=('issue of debentures', [
        'Premium on issue of debentures is credited to Securities Premium Account.',
        'Premium on redemption is credited to Premium on Redemption of Debentures Account.',
        'Loss on issue = discount on issue + premium on redemption.'], [
        'Premium on redemption is credited to Securities Premium Account.',
        'Discount on issue is credited to the debentures account.',
        'Debentures cannot be issued at par and redeemed at a premium.',
        'Loss on issue is credited at the time of issue.']),
)

CH06_ST3 = dict(
    cat='term',
    terms=[
        ('Debentures as collateral security', 'Debentures issued to a lender as additional security for a loan, over and above the primary security.'),
        ('Debenture Suspense Account', 'The account debited when debentures are issued as collateral security; shown as a deduction from debentures in the notes.'),
        ('Issue of debentures for consideration other than cash', 'Issue of debentures to vendors for the purchase of assets.'),
        ('Primary security', 'The main security offered against a loan, such as a charge on assets.'),
    ],
    ars=[
        ('No interest is paid on debentures issued as collateral security.', 'Interest is paid on the loan, not on such debentures.', 'a', 'Both true; R explains A.'),
        ('Debentures issued as collateral security can be recorded without any entry.', 'They may be shown only by a note below the loan in the balance sheet.', 'a', 'Both true; R explains A.'),
        ('Debentures issued to vendors are issued for cash.', 'Vendors receive debentures in return for assets.', 'd', 'A is false: they are issued for consideration other than cash. R is true.')],
    tf=('debentures as collateral security', [
        'The lender can sell collateral debentures only if the loan is not repaid.',
        'Debenture Suspense A/c is debited when an entry is passed.',
        'No interest is paid on collateral debentures.'], [
        'Interest is paid on both the loan and the collateral debentures.',
        'Collateral debentures are issued for cash.',
        'Debenture Suspense A/c is credited when collateral debentures are issued.',
        'Collateral debentures are primary security.']),
)


def c6_vendor(r):
    co = company(r)
    pc = amt(r, 100000, 2000000, 1000)
    mode = r.choice(['par', 'premium', 'discount'])
    x = r.choice([5, 10, 20])
    price = 100 if mode == 'par' else 100 + x if mode == 'premium' else 100 - x
    n = amt(r, 1000, 20000, 100)
    pc = n * price
    rate = r.choice([8, 9, 10, 12])
    cr = f'To {rate}% Debentures A/c {inr(n * 100)}' + (f'; To Securities Premium A/c {inr(n * x)}' if mode == 'premium' else '')
    dr = f'Vendor A/c Dr {inr(pc)}' + (f'; Discount on Issue of Debentures A/c Dr {inr(n * x)}' if mode == 'discount' else '')
    mt = 'at par' if mode == 'par' else f'at a {mode} of {x}%'
    return {'stem': f'{co} purchased machinery for {inr(pc)} and paid the vendor by issuing {rate}% debentures of ₹100 each {mt}. Calculate the number of debentures and pass the entry for their issue.',
            'answer': f'{q(n)} debentures; {dr}; {cr}',
            'key': f'Number = {inr(pc)} ÷ ₹{price} = {q(n)} (1 mark); entries: Machinery A/c Dr; To Vendor A/c {inr(pc)}; then {dr}; {cr} (2 marks).',
            'distractors': [f'{q(pc // 100)} debentures' if pc % 100 == 0 and price != 100 else f'{q(n + 10)} debentures', f'{q(n * 2)} debentures', f'{q(n - 10)} debentures']}


def c6_vendor_mcq(r):
    v = retry(c6_vendor, r)
    a = v['answer'].split(';')[0]
    d = [x for x in dict.fromkeys(v['distractors']) if x != a]
    return mcq(v['stem'].replace(' Calculate the number of debentures and pass the entry for their issue.', ' The number of debentures issued is:'), a, d[:3], v['key'], r)


def c6_collateral(r):
    co = company(r)
    L = amt(r, 500000, 5000000, 100000)
    n = I(Fr(L, 100) * r.choice([1, Fr(6, 5), Fr(5, 4)]))
    rate = r.choice([9, 10, 12])
    ent = f'Debenture Suspense A/c Dr {inr(n * 100)}; To {rate}% Debentures A/c {inr(n * 100)}'
    return {'stem': f'{co} took a bank loan of {inr(L)} and issued {q(n)} {rate}% debentures of ₹100 each as collateral security. Pass the journal entry (if the company records it) and show how it appears in the notes to accounts.',
            'answer': ent,
            'key': f'Bank A/c Dr {inr(L)}; To Bank Loan A/c {inr(L)} (1 mark). {ent} (1 mark). Notes: Long-term borrowings: Bank loan {inr(L)} (secured by issue of {inr(n * 100)} debentures as collateral); {rate}% debentures {inr(n * 100)} less Debenture Suspense {inr(n * 100)} = nil (1 mark).'}


CH06_ST4 = dict(
    cat='term',
    terms=[
        ('Writing off loss on issue of debentures', 'Transferring the loss on issue first from Securities Premium (if any) and the balance from the Statement of Profit and Loss.'),
        ('Interest on debentures', 'A fixed charge payable on debentures at the coupon rate on their face value.'),
        ('Tax deducted at source (TDS)', 'Income tax deducted by the company from debenture interest before payment and deposited with the government.'),
        ('Debenture Interest Account', 'The account debited with gross interest on debentures, transferred to the Statement of Profit and Loss.'),
    ],
    ars=[
        ('Discount on issue of debentures is written off first from Securities Premium.', 'Section 52 permits securities premium to be used to write off discount on issue of debentures.', 'a', 'Both true; R explains A.'),
        ('Interest on debentures is calculated on the issue price.', 'Interest is paid at the coupon rate.', 'd', 'A is false: interest is on the face value. R is true.'),
        ('Tax deducted at source is a liability of the company until deposited.', 'The company deducts it on behalf of the government.', 'a', 'Both true; R explains A.')],
    tf=('interest and writing off loss on debentures', [
        'Interest on debentures is calculated on face value.',
        'Debenture interest is transferred to the Statement of Profit and Loss.',
        'Loss on issue may be written off from Securities Premium.'], [
        'Interest on debentures is calculated on the issue price.',
        'Debenture interest is an appropriation of profit.',
        'TDS on debenture interest is income of the company.',
        'Loss on issue must be written off only from general reserve.']),
)


def c6_interest(r):
    co = company(r)
    n = amt(r, 1000, 20000, 500)
    rate = r.choice([8, 9, 10, 12])
    half = r.random() < 0.6
    tds = 10
    g = I(Fr(n * 100 * rate, 200 if half else 100))
    t = I(Fr(g * tds, 100))
    return {'stem': f'{co} has {q(n)} {rate}% debentures of ₹100 each. Interest is paid {"half-yearly on 30 September and 31 March" if half else "annually on 31 March"}, after deducting tax at source @ {tds}%. Pass the journal entries for interest {"for one half-year" if half else "for the year"}.',
            'answer': f'Debenture Interest A/c Dr {inr(g)}; To Debentureholders A/c {inr(g - t)}; To TDS Payable A/c {inr(t)}',
            'key': f'Gross interest {inr(n * 100)} × {rate}%{" × 6/12" if half else ""} = {inr(g)}; TDS {inr(t)}; net {inr(g - t)}. Entries: (i) Debenture Interest A/c Dr {inr(g)}; To Debentureholders A/c {inr(g - t)}; To TDS Payable A/c {inr(t)} (ii) Debentureholders A/c Dr; To Bank A/c {inr(g - t)} (iii) TDS Payable A/c Dr; To Bank A/c {inr(t)} (iv) Statement of P&L Dr; To Debenture Interest A/c {inr(g)}.'}


def c6_interest_mcq(r):
    co = company(r)
    n = amt(r, 1000, 20000, 500)
    rate = r.choice([8, 9, 10, 12])
    g = n * rate
    t = I(Fr(g, 10))
    return mcq(f'{co} has {q(n)} {rate}% debentures of ₹100 each; interest is paid annually after TDS @ 10%. The net amount paid to debenture holders for the year is:',
               inr(g - t), [inr(g), inr(t), inr(g + t)], f'Gross {inr(g)}; TDS {inr(t)}; net {inr(g - t)}.', r)


def c6_writeoff(r):
    co = company(r)
    n = amt(r, 1000, 20000, 500)
    di = r.choice([5, 10])
    rp = r.choice([0, 5, 10])
    loss = n * (di + rp)
    sp = r.choice([0, amt(r, 1000, loss, 1000), loss + amt(r, 1000, 20000, 1000)])
    from_sp = min(sp, loss)
    from_pl = loss - from_sp
    ent = (f'Securities Premium A/c Dr {inr(from_sp)}; ' if from_sp else '') + (f'Statement of Profit and Loss Dr {inr(from_pl)}; ' if from_pl else '') + f'To Loss on Issue of Debentures A/c {inr(loss)}'
    return {'stem': f'{co} issued {q(n)} debentures of ₹100 each at a discount of {di}%{", redeemable at a premium of " + str(rp) + "%" if rp else ", redeemable at par"}. The balance in Securities Premium Account was {inr(sp)}. Pass the entry to write off the loss on issue of debentures in the year of issue.',
            'answer': ent,
            'key': f'Loss on issue = {q(n)} × ₹{di + rp} = {inr(loss)}; written off from securities premium {inr(from_sp)} and statement of profit and loss {inr(from_pl)}. Entry: {ent}.'}


# ================================================================ families

FAMILIES = {
    S + '05-st1': facts(CH05_ST1) + [FF('C3', 'D2', 'mcq', c5_paidup_mcq), FF('C3', 'D3', 'numerical', c5_paidup, marks=3, kinds=('m3',)), FF('C4', 'D3', 'numerical', c5_paidup, marks=3)],
    S + '05-st2': facts(CH05_ST2) + [FF('C3', 'D2', 'mcq', c5_allot_mcq), FF('C3', 'D3', 'multi_step', c5_issue, marks=4, kinds=('m4',)), FF('C3', 'D3', 'numerical', c5_arrears, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'long', c5_issue, marks=6), FF('C4', 'D3', 'numerical', c5_arrears, marks=3), FF('C2', 'D1', 'mcq', c5_allot_mcq), FF('C3', 'D1', 'mcq', c5_allot_mcq)],
    S + '05-st3': facts(CH05_ST3) + [FF('C3', 'D2', 'mcq', c5_prorata_mcq), FF('C3', 'D3', 'numerical', c5_prorata, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'long', c5_prorata_entries, marks=6, kinds=('m6',)), FF('C4', 'D3', 'multi_step', c5_prorata_entries, marks=4, kinds=('m4',)),
                                     FF('C3', 'D4', 'numerical', c5_prorata, marks=3), FF('C2', 'D1', 'mcq', c5_prorata_mcq)],
    S + '05-st4': facts(CH05_ST4) + [FF('C3', 'D2', 'mcq', c5_forfeit_mcq), FF('C3', 'D2', 'mcq', c5_capres_mcq), FF('C3', 'D3', 'multi_step', c5_forfeit, marks=3, kinds=('m3',)),
                                     FF('C3', 'D3', 'multi_step', c5_reissue, marks=3, kinds=('m3',)), FF('C4', 'D4', 'multi_step', c5_reissue, marks=4, kinds=('m4',)),
                                     FF('C4', 'D3', 'multi_step', c5_forfeit, marks=4, kinds=('m4',)), FF('C3', 'D1', 'mcq', c5_capres_mcq), FF('C4', 'D5', 'multi_step', c5_reissue, marks=4)],
    S + '05-st5': facts(CH05_ST5) + [FF('C3', 'D2', 'mcq', c5_vendor_mcq), FF('C3', 'D3', 'multi_step', c5_vendor, marks=3, kinds=('m3',)), FF('C4', 'D3', 'multi_step', c5_vendor, marks=4, kinds=('m4',)),
                                     FF('C2', 'D1', 'mcq', c5_vendor_mcq)],
    S + '06-st1': facts(CH06_ST1) + [FF('C3', 'D2', 'mcq', c6_case_mcq), FF('C4', 'D3', 'mcq', c6_case_mcq)],
    S + '06-st2': facts(CH06_ST2) + [FF('C3', 'D2', 'mcq', c6_loss_mcq), FF('C3', 'D3', 'numerical', c6_issue, marks=3, kinds=('m3',)), FF('C3', 'D2', 'mcq', c6_case_mcq),
                                     FF('C4', 'D3', 'numerical', c6_issue, marks=3), FF('C4', 'D4', 'multi_step', c6_issue, marks=4, kinds=('m4',)), FF('C2', 'D1', 'mcq', c6_case_mcq), FF('C3', 'D1', 'mcq', c6_loss_mcq)],
    S + '06-st3': facts(CH06_ST3) + [FF('C3', 'D2', 'mcq', c6_vendor_mcq), FF('C3', 'D3', 'multi_step', c6_vendor, marks=3, kinds=('m3',)), FF('C3', 'D3', 'multi_step', c6_collateral, marks=3, kinds=('m3',)),
                                     FF('C4', 'D3', 'multi_step', c6_vendor, marks=3), FF('C4', 'D4', 'multi_step', c6_collateral, marks=3)],
    S + '06-st4': facts(CH06_ST4) + [FF('C3', 'D2', 'mcq', c6_interest_mcq), FF('C3', 'D3', 'multi_step', c6_interest, marks=3, kinds=('m3',)), FF('C3', 'D3', 'multi_step', c6_writeoff, marks=3, kinds=('m3',)),
                                     FF('C4', 'D4', 'multi_step', c6_writeoff, marks=4, kinds=('m4',)), FF('C4', 'D3', 'multi_step', c6_interest, marks=4, kinds=('m4',)), FF('C2', 'D1', 'mcq', c6_interest_mcq)],
}
