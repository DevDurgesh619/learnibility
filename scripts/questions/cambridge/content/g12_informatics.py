"""Cambridge International A Level Information Technology 9626 (syllabus topics 12-21), grade 12.

Paper 3 (Advanced Theory) style structured, multiple-choice and extended items and Paper 4 (Advanced
Practical) style tasks: data-mining support and confidence, password key spaces, biometric error rates,
packet counts, satellite latency, firewall rules, critical path analysis, bitmap and vector graphics
calculations, tweening and timelines, mail-merge filters and IF fields, HTML/CSS box model,
JavaScript output prediction and validation, test data, implementation methods and forward/backward
chaining in expert systems. Every computed answer is produced by the code that builds the stem.
The topic builder T() and helpers come from the AS module (g11_informatics).
"""
import math
import re
from itertools import combinations

from ._lib import mcq, CTX, PEOPLE  # noqa: F401
from .g11_informatics import (T as _T, MCQ, Q, code, fill, ctx, cap, num, money, nearest, tbl, finish, IND, like,  # noqa: F401
                              ch1_testdata, caesar)

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
DEFS = {}


def T(*a, **k):
    return _T(*a, registry=(CHAPTERS, DEFS), **k)


# =============================================================================== Chapter 1 IT in society
t = T(1, 'Digital currencies, cryptocurrencies and blockchain; electronic funds transfer', 'digital currencies, cryptocurrencies and blockchain', 'electronic funds transfer',
      defs=[('digital currency', 'Money that exists only in electronic form, with no physical notes or coins, and is transferred electronically.'),
            ('cryptocurrency', 'A digital currency that uses cryptography to secure transactions and is usually decentralised, not controlled by a central bank.'),
            ('blockchain', 'A decentralised, distributed ledger in which transactions are grouped into blocks, each linked to the previous block by its hash, so records cannot easily be altered.'),
            ('electronic funds transfer (EFT)', 'Moving money electronically from one bank account to another, without cash or paper cheques changing hands.'),
            ('hash (in a blockchain)', 'A fixed-length value calculated from a block\'s contents; any change to the block changes the hash, which breaks the link to the next block.')],
      mcqs=[('Why is it very difficult to alter a transaction recorded in a blockchain?', 'Each block contains the hash of the previous block, so changing one block breaks every later link and the change is rejected by the other copies', ['The blockchain is stored on one secure central server', 'Transactions are written in pencil', 'Blocks are deleted after one day'],
             'The ledger is distributed and chained by hashes.'),
            ('Which is a disadvantage of cryptocurrencies for consumers?', 'Their value can change very quickly', ['They can only be used in one country', 'They are printed by central banks', 'Every transaction is reversed after a week'], 'Volatility makes them risky stores of value.'),
            ('Which is an example of electronic funds transfer?', 'An employer paying salaries directly into employees\' bank accounts', ['Paying for shopping with banknotes', 'Writing a paper cheque', 'Keeping coins in a savings jar'], 'EFT moves money between accounts electronically.')],
      exps=[('Explain why a blockchain is described as decentralised.', 'Copies of the ledger are held by many computers (nodes) in a peer-to-peer network rather than one central authority, and transactions are verified by consensus among nodes.', '1 mark many copies/nodes; 1 mark no central authority/consensus. [2]'),
            ('Explain two advantages of electronic funds transfer for a business.', 'Payments are fast and arrive on time; less cash is held so there is less risk of theft; fewer bank visits and lower administrative costs; automatic records of every payment.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain two risks of using cryptocurrency.', 'High volatility means value can fall sharply; lost private keys mean funds are lost forever; exchanges can be hacked; limited regulation offers little protection; use in crime.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Describe the steps when a customer pays by contactless card in a shop.', 'Card/phone held near the reader; data sent by NFC; terminal sends encrypted request via the acquiring bank to the card issuer; issuer checks funds/limits and authorises; payment approved and money transferred by EFT.', '1 mark per step, max 4. [4]')],
      ars=[('Blockchain transactions are hard to tamper with.', 'Each block is linked to the previous block by a hash, and copies are held by many nodes.'),
           ('Cryptocurrencies are risky for savers.', 'Their exchange values can rise and fall sharply over short periods.'),
           ('EFT reduces the need to handle cash.', 'Money is moved electronically between bank accounts.')],
      falses=['A blockchain is stored on a single server owned by a bank.', 'Cryptocurrencies are issued by central banks as banknotes.', 'EFT requires a paper cheque to be posted.'],
      intros=['{org}, {aot} in {city}, is considering accepting cryptocurrency payments from customers.',
              '{org} in {city} is reviewing its payment methods, including electronic funds transfer and cryptocurrency.',
              '{p} is writing a report for {org} in {city} on how blockchain technology could be used to keep records.'],
      parts=[('Describe what is meant by a blockchain.', 'A distributed ledger of blocks of transactions; each block includes the previous block\'s hash; copies on many nodes.', '1 mark per point, max 2. [2]'),
             ('Explain two benefits of accepting cryptocurrency payments.', 'Attract new customers; low international transfer fees; fast cross-border payments; no chargebacks.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Explain two drawbacks of accepting cryptocurrency payments.', 'Price volatility; regulatory uncertainty; few customers use it; security of wallets; accounting/tax complexity.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Describe how electronic funds transfer is used to pay staff.', 'Payroll system produces a file of payments; sent to the bank; money moved from the company account to each employee\'s account on payday.', '1 mark per step, max 3. [3]')],
      ev=[('whether {org} should accept cryptocurrency as a form of payment', 'new customers; fast international payments; lower fees; innovative image.', 'volatile value; uncertain regulation; low demand; security and accounting issues.', 'it may be worthwhile only if payments are converted immediately to normal currency and demand exists.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_crypto(r, D):
    p0 = r.choice([18000, 24000, 32000, 41000, 56000, 63000])
    ch = r.choice([-25, -18, -12, -8, 6, 9, 15, 22, 30])
    p1 = p0 * (1 + ch / 100)
    amt = r.choice([0.05, 0.1, 0.25, 0.4, 0.5, 1.2])
    d = ctx(r)
    if D == 1:
        return MCQ(r, f'One unit of a cryptocurrency is worth ${p0:,}. How much is {amt} of a unit worth?', money(amt * p0), [money(amt * p0 * 10), money(p0 / amt), money(amt * p0 / 10)], f'{amt} × {p0:,} = {money(amt * p0)}.')
    stem = f'{d["p"]} buys {amt} units of a cryptocurrency at ${p0:,} per unit. A week later its value has changed by {ch:+}%. Calculate the value of {d["p"]}\'s holding after the change and the gain or loss.'
    v0, v1 = amt * p0, amt * p1
    key = f'initial value {amt} × {p0:,} = {money(v0)} [1]; new price {p0:,} × {1 + ch / 100:.2f} = {money(p1)}, holding = {money(v1)} [1]; {"gain" if v1 > v0 else "loss"} of {money(abs(v1 - v0))} [1]'
    ans = f'{money(v1)}; {"gain" if v1 > v0 else "loss"} of {money(abs(v1 - v0))}'
    m = 3
    if D >= 4:
        ch2 = r.choice([-20, -10, 10, 20])
        p2 = p1 * (1 + ch2 / 100)
        stem += f' The following week the value changes by a further {ch2:+}%. Calculate the overall percentage change and explain what this shows about the risk of holding cryptocurrency.'
        tot = (p2 / p0 - 1) * 100
        key += f'; overall (1 {ch:+}%) × (1 {ch2:+}%) − 1 = {tot:+.2f}% [1]; shows high volatility / value can change rapidly [1]'
        ans += f'; overall change {tot:+.2f}%; values are volatile so savings can lose value quickly.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


BASKETS = ['bread', 'milk', 'eggs', 'butter', 'tea', 'rice', 'juice']

t = T(1, 'Data mining and its use in business, medicine and security', 'data mining', 'business, medicine and security',
      defs=[('data mining', 'Searching large amounts of stored data, using software, to discover patterns, trends and relationships that were not previously known.'),
            ('association rule', 'A pattern found by data mining of the form "if A then B", such as customers who buy item A also tend to buy item B.'),
            ('support (of a rule)', 'The proportion of all transactions that contain every item in the rule.'),
            ('confidence (of a rule)', 'For a rule "if A then B", the proportion of transactions containing A that also contain B.'),
            ('big data', 'Data sets that are so large, fast-changing and varied that they need special software and techniques to store and analyse.')],
      mcqs=[('Which is a use of data mining in medicine?', 'Finding patterns in patient records that predict which patients are at risk of a disease', ['Printing prescriptions', 'Booking appointments online', 'Encrypting patient records'], 'Mining identifies risk factors and trends.'),
            ('How do supermarkets use data mining of loyalty-card data?', 'To find which products are often bought together and target offers', ['To print receipts', 'To check card PINs', 'To set the shop opening hours randomly'], 'Market-basket analysis.'),
            ('Which is a privacy concern about data mining?', 'Personal data may be used for purposes customers did not expect or agree to', ['Data mining deletes data', 'Data mining only uses public weather data', 'Data mining makes computers slower'], 'Inferences about individuals can be intrusive.')],
      exps=[('Explain how data mining can help banks to detect fraud.', 'It learns each customer\'s normal spending pattern; transactions that do not fit (unusual amount, place or time) are flagged for checking or blocked.', '1 mark normal patterns identified; 1 mark anomalies flagged. [2]'),
            ('Explain two benefits of data mining for a retailer.', 'Identify products bought together to place them nearby or bundle offers; predict demand to manage stock; target personalised promotions; identify customer segments.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain two concerns about the use of data mining.', 'Invasion of privacy; data used without consent; inaccurate conclusions (correlation is not causation); discrimination through profiling; security of large data stores.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('Data mining can help detect credit-card fraud.', 'Transactions that do not match a customer\'s usual pattern can be identified.'),
           ('A rule with high confidence may still have low support.', 'Confidence is measured only among transactions containing the first item.')],
      falses=['Data mining collects data by sending questionnaires.', 'Support is the proportion of transactions containing A that also contain B.'],
      intros=['{org}, {aot} in {city}, has collected five years of customer transaction data.',
              'A hospital group run by {org} in {city} wants to use its patient records to improve care.',
              'The security services in {city} have asked {org} to analyse travel and communication data.'],
      parts=[('Explain what is meant by data mining.', 'Analysing large data sets with software to find hidden patterns and relationships.', '1 mark large data; 1 mark hidden patterns. [2]'),
             ('Describe two ways the organisation could use data mining.', 'Market-basket analysis; predicting demand; fraud detection; identifying risk factors; customer segmentation; detecting suspicious behaviour.', '1 mark each, max 2. [2]'),
             ('Explain one ethical issue with this use of data mining.', 'Privacy/consent; profiling individuals; risk of discrimination or false suspicion.', '1 mark issue; 1 mark explanation. [2]'),
             ('Explain why the results of data mining should be checked by experts.', 'Patterns may be coincidental or correlations may not be causes; decisions need human judgement.', '1 mark correlation not causation; 1 mark human judgement. [2]')],
      ev=[('the use of data mining by {org}', 'finds valuable patterns; better decisions; fraud detection; targeted services.', 'privacy and consent; false patterns; cost of software and expertise; security of data.', 'beneficial if data is anonymised where possible, used with consent and conclusions are checked.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_assoc(r, D):
    n = 8 if D <= 3 else 10
    a, b = r.sample(BASKETS, 2)
    trans = []
    for _ in range(n):
        items = set(r.sample(BASKETS, r.randrange(2, 5)))
        if r.random() < 0.45:
            items |= {a, b}
        trans.append(sorted(items))
    na = sum(1 for x in trans if a in x)
    nab = sum(1 for x in trans if a in x and b in x)
    if na == 0:
        return None
    sup = nab / n * 100
    conf = nab / na * 100
    rows = [(f'T{i + 1}', ', '.join(x)) for i, x in enumerate(trans)]
    stem = f'A shop\'s data-mining software examines these {n} transactions:\n{tbl(["Transaction", "Items"], rows)}\n'
    if D == 1:
        return MCQ(r, stem + f'What is the support for the rule "if {a} then {b}"?', f'{num(round(sup, 1))}%', [f'{num(round(conf, 1))}%', f'{num(round(na / n * 100, 1))}%', f'{num(round((nab + 1) / n * 100, 1))}%'],
                   f'Support = transactions with both {a} and {b} / all = {nab}/{n} = {num(round(sup, 1))}%.') if num(round(sup, 1)) != num(round(conf, 1)) else None
    stem += f'For the rule "if {a} then {b}", calculate (a) the support and (b) the confidence, as percentages.'
    key = f'(a) {nab} transactions contain both / {n} = {num(round(sup, 1))}% [2] (b) {nab} / {na} transactions containing {a} = {num(round(conf, 1))}% [2]'
    ans = f'(a) {num(round(sup, 1))}% (b) {num(round(conf, 1))}%'
    m = 4
    if D >= 4:
        stem += ' (c) Explain how the shop could use this result.'
        key += f' (c) e.g. place {b} near {a} / offer a joint promotion if confidence is high; consider support to judge how often it applies [1]'
        ans += f' (c) If the confidence is high, place {b} near {a} or offer a bundle.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(1, 'Social networking, online gaming and the impact of IT on business, employment and education', 'social networking, online gaming', 'impact of it on business, employment and education',
      defs=[('social networking', 'Using websites or apps to create a profile, connect with other people and share content and messages.'),
            ('teleworking', 'Working from home or another location away from the office, using IT to communicate with the employer.'),
            ('online learning (e-learning)', 'Education delivered through the internet, such as video lessons, virtual learning environments and online tests.'),
            ('gig economy', 'A labour market in which people work short-term or task-by-task jobs, often arranged through apps.')],
      mcqs=[('Which job is most likely to have increased because of IT?', 'Website developer', ['Typesetter for printed newspapers', 'Bank cashier', 'Filing clerk'], 'New IT-based jobs have been created while some manual/clerical jobs fell.'),
            ('Which is a benefit of online learning for students?', 'They can learn at their own pace and revisit recorded lessons', ['They never need an internet connection', 'Teachers mark every task instantly by hand', 'It removes the need to read'], 'Flexibility of time and place.'),
            ('Which is a concern about online gaming for young people?', 'Addiction and spending too much time or money in games', ['Games improve broadband speeds', 'Games are only played offline', 'Games cannot be played with others'], 'Health, social and financial risks.')],
      exps=[('Explain two ways social networking is used by businesses.', 'Marketing and advertising to targeted audiences; customer service and feedback; building brand loyalty; recruitment.', '2 × (1 mark use, 1 mark explanation). [4]'),
            ('Explain two disadvantages of teleworking for employees.', 'Isolation from colleagues; difficulty separating home and work life; distractions at home; fewer opportunities for promotion or training; costs of heating/equipment.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain how IT has changed the skills employers want.', 'Many jobs now need digital skills such as using software, data analysis and online communication, while routine manual or clerical tasks are automated.', '1 mark new digital skills; 1 mark routine tasks automated. [2]')],
      ars=[('Teleworking can reduce a company\'s office costs.', 'Fewer staff need desks in the office.'),
           ('IT has reduced the number of some clerical jobs.', 'Tasks such as filing and data entry are automated.')],
      falses=['Social networks cannot be used for advertising.', 'Online learning always requires students to attend a classroom.'],
      intros=['{org}, {aot} in {city}, wants to make more use of social media and allow some staff to work from home.',
              '{org} in {city} is reviewing how it uses social media, teleworking and online learning.',
              '{p} is researching how IT has changed jobs at {org} in {city} over the last twenty years.'],
      parts=[('Describe two ways the organisation could use social networking.', 'Advertising; customer engagement; announcements; recruitment; feedback.', '1 mark each, max 2. [2]'),
             ('Explain two benefits of teleworking for the organisation.', 'Lower office costs; wider recruitment pool; increased productivity; fewer absences.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Explain two advantages and one disadvantage of online learning.', 'Flexible time/place; self-paced; recorded; lower costs. Disadvantage: needs devices and internet; less interaction; motivation.', '1 mark each point, max 3. [3]'),
             ('Explain how IT has affected employment.', 'Some jobs lost to automation; new IT jobs created; jobs changed/upskilling; more flexible and remote working.', '1 mark per point, max 3. [3]')],
      ev=[('whether the impact of IT on employment at organisations such as {org} has been mainly positive', 'new jobs and skills; flexible working; higher productivity; safer work.', 'jobs lost to automation; need for retraining; constant availability and stress; digital divide.', 'overall positive for skilled workers but disruptive for routine jobs, so retraining is essential.')])


CRIMES = [('An email that appears to be from a bank asks the user to click a link and confirm their password.', 'phishing'),
          ('A user types the correct address of their bank, but malicious code on their computer sends them to a fake website.', 'pharming'),
          ('A text message claims a parcel is held and asks for a fee through a link.', 'smishing'),
          ('A caller claiming to be from the IT help desk asks an employee for their login details.', 'vishing'),
          ('A person uses software to try millions of password combinations to get into a company server.', 'hacking (brute-force attack)'),
          ('Hidden software records every key pressed on the user\'s computer and sends it to a criminal.', 'keylogging (spyware)')]
CRIME_FIX = {'phishing': 'do not click links in unexpected emails; check the sender address; contact the bank directly; use spam filters',
             'pharming': 'use up-to-date anti-malware; check the padlock and certificate; use a trusted DNS service',
             'smishing': 'do not click links in unexpected texts; contact the company using its official number or app',
             'vishing': 'never give login details over the phone; verify the caller through official channels',
             'hacking (brute-force attack)': 'strong passwords; account lockout after failed attempts; two-factor authentication; firewalls',
             'keylogging (spyware)': 'anti-spyware software; on-screen keyboards or drop-down entry for passwords; two-factor authentication'}

t = T(1, 'Technology-enabled crime: phishing, pharming, smishing and hacking; protection methods', 'technology-enabled crime', 'phishing, pharming, smishing and hacking', 'protection methods',
      defs=[('phishing', 'Sending emails that pretend to be from a trusted organisation to trick people into revealing personal data such as passwords or bank details.'),
            ('pharming', 'Malicious code that redirects a user from a genuine website to a fake one, even when the correct address is typed, in order to steal data.'),
            ('smishing', 'Phishing carried out using SMS text messages.'),
            ('hacking', 'Gaining unauthorised access to a computer system, often to steal, change or delete data.'),
            ('two-factor authentication', 'A security method that requires two different types of evidence of identity, such as a password and a code sent to a phone.')],
      mcqs=[('Which crime can affect a user even when they type the correct web address?', 'Pharming', ['Phishing', 'Smishing', 'Vishing'], 'Pharming redirects via altered DNS or hosts files.'),
            ('Which measure best protects an account if its password is stolen?', 'Two-factor authentication', ['A longer screen timeout', 'Using a larger monitor', 'Turning off the firewall'], 'The second factor is still needed.'),
            ('What is the main aim of phishing?', 'To trick users into giving away personal or financial details', ['To slow down a network', 'To encrypt the user\'s files for ransom', 'To damage hardware'], 'Phishing is a social engineering attack.')],
      exps=[('Explain the difference between phishing and pharming.', 'Phishing tricks the user with a fake email/message to make them visit a fake site or give details; pharming uses malicious code to redirect the user to a fake site automatically, even if the correct address is typed.', '1 mark phishing; 1 mark pharming. [2]'),
            ('Explain how two-factor authentication protects online accounts.', 'Even if a criminal learns the password, they also need the second factor (e.g. a code sent to the owner\'s phone), which they do not have.', '1 mark two different factors; 1 mark stolen password alone not enough. [2]'),
            ('Explain why longer passwords using a mix of character types are harder to crack.', 'The number of possible combinations grows exponentially with length and character set size, so a brute-force attack would take far longer.', '1 mark more combinations; 1 mark brute force takes longer. [2]')],
      ars=[('Pharming can work even when the user types the correct web address.', 'Malicious code changes how the address is translated to an IP address.'),
           ('Account lockout helps defend against brute-force attacks.', 'The attacker cannot keep trying passwords after a few failures.'),
           ('Smishing uses text messages.', 'The attacker sends SMS messages containing links or requests for details.')],
      falses=['Phishing is only possible using telephone calls.', 'A firewall stops users from replying to phishing emails.', 'Short passwords are harder to crack than long ones.'],
      intros=['Staff at {org} in {city} have received several suspicious emails and text messages this month.',
              '{org}, {aot} in {city}, suffered a data breach after a hacker gained access to its server.',
              '{p} runs online banking security training for customers of {org} in {city}.'],
      parts=[('Describe what is meant by phishing.', 'Fake emails pretending to be from a trusted organisation to obtain personal details.', '1 mark fake email; 1 mark aim to steal details. [2]'),
             ('Explain how smishing differs from phishing.', 'Smishing uses SMS text messages rather than email.', '1 mark text messages; 1 mark otherwise same aim. [2]'),
             ('Describe three ways users can recognise a phishing message.', 'Generic greeting; urgent/threatening tone; spelling errors; suspicious sender address; links to unusual URLs; requests for passwords.', '1 mark each, max 3. [3]'),
             ('Explain two methods the organisation could use to protect its systems from hackers.', 'Firewall; strong passwords and lockout; two-factor authentication; encryption; updates/patches; intrusion detection.', '2 × (1 mark method, 1 mark explanation). [4]'),
             ('Explain why staff training is important in preventing these crimes.', 'Many attacks rely on tricking people (social engineering), so trained staff are less likely to click links or reveal details.', '1 mark social engineering; 1 mark effect of training. [2]')],
      ev=[('whether technical measures alone can protect {org} from technology-enabled crime', 'firewalls, anti-malware, filters and 2FA block many attacks automatically.', 'social engineering targets people; new attacks evade filters; insiders; users can disable protection.', 'technical measures must be combined with training, policies and monitoring.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def g12_crime(r, D):
    s, c = r.choice(CRIMES)
    if D <= 2:
        return MCQ(r, f'{s} Which type of crime is this?', c.capitalize(), [x[1].capitalize() for x in CRIMES if x[1] != c], f'{c}. Protection: {CRIME_FIX[c]}.')
    s2, c2 = r.choice([x for x in CRIMES if x[1] != c])
    return Q(f'Identify the type of crime in each situation and describe one way to protect against it: (1) {s} (2) {s2}', f'(1) {c}: {CRIME_FIX[c]}. (2) {c2}: {CRIME_FIX[c2]}.',
             f'(1) {c} [1]; protection e.g. {CRIME_FIX[c]} [1] (2) {c2} [1]; protection e.g. {CRIME_FIX[c2]} [1]. [4]', marks=4)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def g12_keyspace(r, D):
    sets = [('digits only', 10), ('lower-case letters only', 26), ('upper- and lower-case letters', 52), ('letters and digits', 62), ('letters, digits and 32 symbols', 94)]
    (n1, c1), (n2, c2) = sorted(r.sample(sets, 2), key=lambda x: x[1])
    L1 = r.choice([4, 6, 8])
    L2 = L1 + r.choice([0, 2, 4]) if D >= 4 else L1
    k1, k2 = c1 ** L1, c2 ** L2
    rate = r.choice([10 ** 6, 10 ** 8, 10 ** 9, 10 ** 10])

    def tt(k):
        s = k / rate
        if s < 1:
            from decimal import Decimal
            return f"{Decimal(str(float(f'{s:.3g}'))):f} seconds"
        if s < 120:
            return f'{num(round(s, 2))} seconds'
        if s < 7200:
            return f'{num(round(s / 60, 1))} minutes'
        if s < 3 * 86400:
            return f'{num(round(s / 3600, 1))} hours'
        if s < 3 * 365 * 86400:
            return f'{num(round(s / 86400, 1))} days'
        return f'{s / (365 * 86400):.3g} years'
    stem = (f'An attacker can test {rate:,} passwords per second. Password A has {L1} characters chosen from {n1} ({c1} possible characters); password B has {L2} characters chosen from {n2} ({c2} possible characters). '
            f'Calculate the number of possible passwords for each and the maximum time needed to try them all.')
    key = f'A: {c1}^{L1} = {k1:,} [1]; time {tt(k1)} [1]; B: {c2}^{L2} = {k2:,} [1]; time {tt(k2)} [1]'
    ans = f'A {k1:,} combinations, {tt(k1)}; B {k2:,} combinations, {tt(k2)}'
    m = 4
    if D >= 5:
        stem += ' Explain why account lockout makes a brute-force attack impractical even for short passwords.'
        key += '; lockout after a few failed attempts limits guesses to a handful, so the attack cannot try all combinations [1]'
        ans += '; lockout stops repeated guessing.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 2 New and emerging technologies
t = T(2, 'Nanotechnology, quantum cryptography and computer-assisted translation', 'nanotechnology', 'quantum cryptography', 'computer-assisted translation',
      defs=[('nanotechnology', 'Designing and manipulating materials and devices at the scale of atoms and molecules (1 to 100 nanometres).'),
            ('quantum cryptography', 'Using the properties of quantum physics, such as the polarisation of photons, to exchange encryption keys so that any eavesdropping is detected.'),
            ('computer-assisted translation (CAT)', 'Software that helps a human translator by suggesting translations, storing previously translated phrases (translation memory) and terminology.'),
            ('translation memory', 'A database in CAT software that stores sentences already translated so they can be reused.')],
      mcqs=[('Why is quantum key distribution considered very secure?', 'Measuring the photons changes their state, so any eavesdropper is detected', ['It uses very long passwords', 'It sends keys by post', 'It does not use any keys'], 'Observation disturbs quantum states.'),
            ('Which is a use of nanotechnology in IT?', 'Making smaller, faster transistors in processors', ['Writing web pages', 'Designing spreadsheets', 'Recording podcasts'], 'Nanoscale components increase density.'),
            ('Which is a limitation of computer-assisted translation?', 'It may miss idioms and context, so a human still needs to check it', ['It cannot store previous translations', 'It only works for numbers', 'It removes the need for dictionaries entirely'], 'Machine suggestions are not always correct in context.')],
      exps=[('Explain how translation memory speeds up the work of a translator.', 'Sentences translated before are stored and suggested automatically when they occur again, so the translator does not retranslate them and terminology stays consistent.', '1 mark reuse of stored sentences; 1 mark speed/consistency. [2]'),
            ('Explain one benefit and one concern about nanotechnology.', 'Benefit: smaller, faster, lower-power devices or targeted medicine. Concern: unknown health/environmental effects of nanoparticles; high cost.', '1 mark benefit; 1 mark concern. [2]')],
      ars=[('Quantum cryptography can reveal eavesdroppers.', 'Measuring a quantum state changes it.'),
           ('CAT software improves consistency of terminology.', 'It stores approved terms and earlier translations.')],
      falses=['Quantum cryptography sends keys by email.', 'CAT software never needs human checking.'],
      intros=['{org} in {city}, which translates technical manuals into eight languages, is reviewing emerging technologies.',
              '{p} is presenting to the directors of {org} in {city} on emerging technologies that could affect the business.'],
      parts=[('Describe what is meant by computer-assisted translation.', 'Software supporting human translators with suggestions, translation memory and terminology databases.', '1 mark support for human; 1 mark features. [2]'),
             ('Explain one advantage and one disadvantage of using CAT software.', 'Faster, consistent; but may miss context/idioms and needs checking; cost/training.', '1 mark each. [2]'),
             ('Describe how quantum cryptography could protect data sent by the organisation.', 'Keys exchanged using photons; eavesdropping disturbs them and is detected; then data encrypted with the key.', '1 mark per point, max 3. [3]'),
             ('Describe one use of nanotechnology.', 'Smaller transistors/memory; nanomedicine; stain-resistant materials; flexible screens.', '1 mark use; 1 mark description. [2]')],
      ev=[('whether {org} should rely on computer-assisted translation instead of employing more human translators', 'faster; cheaper per word; consistent terminology.', 'errors in context and tone; sensitive or legal texts need experts; software costs.', 'CAT should support, not replace, skilled translators.')])


t = T(2, 'Virtual reality, augmented reality and holographic imaging', 'virtual reality, augmented reality', 'holographic imaging',
      defs=[('virtual reality (VR)', 'A computer-generated 3D environment that a user is immersed in, usually through a headset, and can interact with.'),
            ('augmented reality (AR)', 'Technology that overlays computer-generated images or information on a live view of the real world, e.g. through a phone camera.'),
            ('holographic imaging', 'Creating three-dimensional images (holograms) using light interference, which can be viewed from different angles without a headset.')],
      mcqs=[('Which is an example of augmented reality?', 'A phone app that shows how a sofa would look in your living room through the camera', ['A headset that places the user in a fully virtual city', 'A 2D video call', 'A paper map'], 'AR overlays digital objects on the real view.'),
            ('Why is VR useful for training surgeons?', 'They can practise operations in a realistic environment without risk to patients', ['VR removes the need for anatomy knowledge', 'VR is cheaper than a pencil', 'VR headsets are worn during real operations only'], 'Safe, repeatable practice.')],
      exps=[('Explain the difference between virtual reality and augmented reality.', 'VR replaces the real world with a fully computer-generated environment; AR keeps the real world in view and adds digital information on top of it.', '1 mark VR replaces; 1 mark AR overlays. [2]'),
            ('Explain two problems with using VR headsets for long periods.', 'Motion sickness/nausea; eye strain and headaches; isolation from surroundings and risk of tripping; heavy headsets cause neck strain.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('AR can be used through a smartphone.', 'The camera view of the real world is combined with digital images on the screen.'),
           ('VR is used to train pilots and surgeons.', 'Dangerous tasks can be practised safely.')],
      falses=['AR completely replaces the user\'s view of the real world.', 'Holograms can only be seen through a VR headset.'],
      intros=['{org}, {aot} in {city}, is looking at VR and AR to improve its training and marketing.',
              '{p} is designing an AR app for visitors to {org} in {city}.'],
      parts=[('Describe one use of virtual reality for the organisation.', 'Training in a safe simulated environment; virtual tours; product design reviews.', '1 mark use; 1 mark description. [2]'),
             ('Describe one use of augmented reality for the organisation.', 'Overlay product information or directions on the camera view; try-before-you-buy; maintenance instructions.', '1 mark use; 1 mark description. [2]'),
             ('Explain two disadvantages of VR.', 'Cost of headsets and content; motion sickness; isolation; limited realism.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Explain how holographic imaging could be used.', 'Displaying 3D product models or medical images that can be viewed from all angles without headsets.', '1 mark use; 1 mark benefit. [2]')],
      ev=[('whether {org} should invest in virtual reality for staff training', 'safe practice of dangerous tasks; repeatable; engaging; reduces travel and equipment use.', 'high cost of hardware and content; motion sickness; not all skills transfer; content becomes outdated.', 'worthwhile for high-risk or expensive training if costs can be spread over many trainees.')])


t = T(2, 'Robotics, autonomous vehicles, biometrics and wearable computing', 'robotics, autonomous vehicles', 'biometrics', 'wearable computing',
      defs=[('robot', 'A programmable machine that can carry out a series of physical tasks automatically, often using sensors to respond to its surroundings.'),
            ('autonomous vehicle', 'A vehicle that uses sensors (cameras, radar, lidar, GPS) and software to drive itself without a human controlling it.'),
            ('biometrics', 'Identifying a person by measuring a unique physical or behavioural characteristic, such as a fingerprint, face, iris or voice.'),
            ('wearable computing', 'Small computing devices worn on the body, such as smart watches and fitness trackers, that collect data and communicate with other devices.'),
            ('false acceptance rate (FAR)', 'The proportion of attempts by unauthorised people that a biometric system wrongly accepts.'),
            ('false rejection rate (FRR)', 'The proportion of attempts by authorised people that a biometric system wrongly rejects.')],
      mcqs=[('Which sensor is used by autonomous vehicles to build a 3D map of their surroundings using laser pulses?', 'Lidar', ['Thermistor', 'pH sensor', 'Microphone'], 'Lidar measures distances with reflected laser light.'),
            ('Why are biometrics more secure than passwords?', 'A biometric characteristic cannot easily be forgotten, shared or guessed', ['Biometric data never needs storing', 'Biometric systems never make errors', 'Biometrics work without any hardware'], 'Characteristics are unique to the person.'),
            ('Which is a privacy concern about wearable fitness trackers?', 'Health and location data could be shared or sold without the user realising', ['They make phones heavier', 'They cannot connect to apps', 'They only measure time'], 'Sensitive personal data is collected continuously.')],
      exps=[('Explain two advantages of using robots on a car production line.', 'Robots work 24 hours without breaks; perform repetitive tasks with consistent accuracy/quality; can work in dangerous conditions such as paint spraying; lower long-term labour costs.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why a biometric system is set to balance the false acceptance and false rejection rates.', 'Making the system stricter lowers false acceptance (more secure) but raises false rejection (genuine users locked out, annoyance); the setting depends on how important security is compared with convenience.', '1 mark trade-off; 1 mark consequence of each. [2]'),
            ('Explain two concerns about the use of autonomous vehicles.', 'Who is liable in an accident; software errors or sensor failures in bad weather; hacking; loss of driving jobs; ethical decisions in unavoidable accidents.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('Lowering the false acceptance rate usually raises the false rejection rate.', 'A stricter match threshold rejects more borderline attempts, including genuine users.'),
           ('Robots can improve consistency on production lines.', 'They repeat tasks to the same standard every time.')],
      falses=['Biometric systems never wrongly reject genuine users.', 'Autonomous vehicles do not use sensors.'],
      intros=['{org}, {aot} in {city}, is investigating biometrics, robotics and wearable technology.',
              '{org} in {city} is introducing biometric staff entry and trialling autonomous vehicles and wearable devices.',
              '{p} is advising {org} in {city} on new technologies for its staff and operations.'],
      parts=[('Describe two types of biometric data.', 'Fingerprint; face; iris; retina; voice; hand geometry; signature dynamics.', '1 mark each, max 2. [2]'),
             ('Explain one advantage and one disadvantage of biometrics compared with passwords.', 'Cannot be forgotten/shared; but expensive, privacy issues, can be affected by injury, cannot be changed if stolen.', '1 mark each. [2]'),
             ('Describe how an autonomous vehicle senses its environment.', 'Cameras, radar, lidar, ultrasonic sensors and GPS feed data to software that identifies objects and plans movement.', '1 mark per point, max 3. [3]'),
             ('Explain two uses of wearable devices.', 'Health/fitness tracking; notifications; contactless payment; location tracking for safety; medical monitoring.', '2 × (1 mark use, 1 mark explanation). [4]')],
      ev=[('the use of biometric systems by {org} to control access', 'unique, cannot be lost or shared; fast; audit trail.', 'cost; privacy of stored biometric data; false rejections; data cannot be changed if leaked.', 'suitable for high-security areas if data is encrypted and a fallback method exists.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_farfrr(r, D):
    imp = r.choice([400, 500, 800, 1000, 2000])
    gen = r.choice([1000, 2000, 2500, 4000, 5000])
    fa = r.randrange(1, 25)
    fr = r.randrange(5, 120)
    far, frr = fa / imp * 100, fr / gen * 100
    sysn = r.choice(['fingerprint', 'face-recognition', 'iris-recognition', 'voice-recognition'])
    stem = f'A {sysn} system at {ctx(r)["org"]} is tested. Of {imp:,} attempts by unauthorised people, {fa} were wrongly accepted. Of {gen:,} attempts by authorised staff, {fr} were wrongly rejected.'
    if D == 1:
        return MCQ(r, stem + ' What is the false acceptance rate?', f'{num(round(far, 2))}%', [f'{num(round(frr, 2))}%', f'{num(round(fa / gen * 100, 2))}%', f'{num(round(100 - far, 2))}%'], f'FAR = {fa}/{imp} × 100 = {num(round(far, 2))}%.')
    stem += ' Calculate the false acceptance rate (FAR) and false rejection rate (FRR) as percentages.'
    key = f'FAR = {fa} / {imp:,} × 100 = {num(round(far, 2))}% [1]; FRR = {fr} / {gen:,} × 100 = {num(round(frr, 2))}% [1]'
    ans = f'FAR {num(round(far, 2))}%; FRR {num(round(frr, 2))}%'
    m = 2
    if D >= 3:
        stem += ' Explain what would happen to each rate if the matching threshold were made stricter.'
        key += '; stricter: FAR falls [1], FRR rises [1]'
        ans += '; a stricter threshold lowers FAR but raises FRR.'
        m = 4
    if D >= 5:
        stem += ' State, with a reason, which rate matters more for the entrance to a data centre.'
        key += '; FAR, because admitting an unauthorised person is a serious security breach [1]'
        ans += ' For a data centre, a low FAR matters most.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(2, 'Cloud computing, the Internet of Things and 3D printing', 'cloud computing', 'the internet of things', '3d printing',
      defs=[('cloud computing', 'Using storage, processing and software provided over the internet by a third party, usually paid for as it is used, instead of on local hardware.'),
            ('Internet of Things (IoT)', 'Everyday physical devices with sensors, processors and network connections that collect and exchange data, such as smart thermostats.'),
            ('3D printing', 'Making a three-dimensional object by building it up layer by layer from a digital model (additive manufacturing).'),
            ('software as a service (SaaS)', 'A cloud model in which software is run on the provider\'s servers and accessed through a browser, usually by subscription.')],
      mcqs=[('Which is a disadvantage of cloud storage?', 'Data cannot be accessed without an internet connection', ['Data can be accessed from anywhere', 'Storage can be increased easily', 'The provider maintains the hardware'], 'Cloud depends on connectivity.'),
            ('Which is an example of the Internet of Things?', 'A fridge that orders milk when it detects the carton is nearly empty', ['A paper calendar', 'A standalone calculator', 'A printed timetable'], 'Connected sensors and actuators.'),
            ('Which is a benefit of 3D printing in medicine?', 'Custom implants and prosthetics can be made to fit an individual patient', ['It replaces all surgeons', 'It makes X-rays unnecessary', 'It only prints flat images'], 'Personalised parts made from scans.')],
      exps=[('Explain two advantages of cloud computing for a small business.', 'No need to buy and maintain servers; pay only for what is used and scale up easily; access data from anywhere; provider handles backups and updates.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain two security concerns about the Internet of Things.', 'Devices often have weak default passwords and are rarely updated, so they can be hacked; they collect personal data; compromised devices can be used in botnets.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why 3D printing is useful for making prototypes.', 'A designer can print a physical model quickly and cheaply from a CAD file, test it and change the design before mass production.', '1 mark quick/cheap from digital model; 1 mark test and modify. [2]')],
      ars=[('Cloud services can be scaled up quickly.', 'The provider allocates more resources on demand.'),
           ('IoT devices can be a security risk.', 'Many have weak passwords and are not updated.')],
      falses=['Cloud computing works without an internet connection.', '3D printers cut objects out of solid blocks.'],
      intros=['{org}, {aot} in {city}, is reviewing new technologies, including cloud computing, IoT devices and 3D printing.',
              '{p}, the IT manager at {org} in {city}, is writing a report on cloud computing, IoT sensors and 3D printing for the directors.'],
      parts=[('Describe what is meant by cloud computing.', 'Using remote servers over the internet for storage/processing/software, provided by a third party.', '1 mark remote/internet; 1 mark third party/pay as used. [2]'),
             ('Explain two disadvantages of cloud computing for the organisation.', 'Dependence on internet; security/privacy of data on third-party servers; ongoing subscription costs; less control; data location laws.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Describe two uses of IoT devices in the buildings.', 'Smart thermostats; occupancy sensors controlling lighting; smart meters; security cameras; predictive maintenance sensors.', '1 mark each, max 2. [2]'),
             ('Explain two uses of 3D printing for the organisation.', 'Prototypes; spare parts on demand; customised products; models for presentations.', '2 × (1 mark use, 1 mark explanation). [4]')],
      ev=[('whether {org} should move all its data and software to the cloud', 'lower capital cost; scalability; remote access; provider handles backup and security updates.', 'internet dependence; privacy and legal concerns; ongoing costs; vendor lock-in; less control.', 'a hybrid approach keeps sensitive data local while using the cloud for scalable services.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def g12_cloud(r, D):
    srv = r.choice([12000, 18000, 25000, 40000])
    maint = r.choice([2000, 3000, 4500])
    staff = r.choice([5000, 8000, 10000])
    sub = r.choice([900, 1200, 1500, 2000])
    yrs = r.choice([3, 4, 5])
    onp = srv + (maint + staff) * yrs
    cl = sub * 12 * yrs
    d = ctx(r)
    stem = (f'{d["org"]} in {d["city"]} compares two options over {yrs} years. On-premises: servers cost ${srv:,} to buy, plus ${maint:,} per year maintenance and ${staff:,} per year for technician time. '
            f'Cloud: a subscription of ${sub:,} per month. Calculate the total cost of each option and state which is cheaper.')
    key = f'on-premises: {srv:,} + ({maint:,} + {staff:,}) × {yrs} = ${onp:,} [1]; cloud: {sub:,} × 12 × {yrs} = ${cl:,} [1]; cheaper: {"cloud" if cl < onp else ("on-premises" if onp < cl else "equal")} [1]'
    ans = f'on-premises ${onp:,}; cloud ${cl:,}; ' + ('cloud is cheaper' if cl < onp else ('on-premises is cheaper' if onp < cl else 'equal cost'))
    m = 3
    if D >= 4:
        stem += ' Give two non-financial factors the organisation should also consider.'
        key += '; non-financial: security/privacy, internet dependence, control, scalability, legal location of data [2]'
        ans += '; also consider security/privacy, reliance on the internet and scalability.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (1, 2, 3, 4), 'numerical')
def g12_3dprint(r, D):
    vol = r.choice([24, 40, 60, 90, 120, 150])
    rate = r.choice([6, 8, 10, 12, 15])
    cost = r.choice([0.05, 0.08, 0.1, 0.12])
    hrs = vol / rate
    c = vol * cost
    obj = r.choice(['a replacement gear', 'a prototype phone case', 'a model of a building', 'a custom prosthetic hand part'])
    if D == 1:
        return MCQ(r, f'A 3D printer prints {rate} cm³ of plastic per hour. How long will it take to print {obj} with a volume of {vol} cm³?', f'{num(round(hrs, 2))} hours',
                   [f'{num(round(vol * rate, 2))} hours', f'{num(round(rate / vol, 2))} hours', f'{num(round(hrs * 60, 2))} hours'], f'{vol} ÷ {rate} = {num(round(hrs, 2))} hours.')
    stem = f'A 3D printer builds objects at {rate} cm³ per hour using plastic costing ${cost:.2f} per cm³. Calculate the time and material cost to print {obj} with a volume of {vol} cm³.'
    key = f'time = {vol} ÷ {rate} = {num(round(hrs, 2))} hours [1]; cost = {vol} × {cost:.2f} = {money(c)} [1]'
    m = 2
    ans = f'{num(round(hrs, 2))} hours; {money(c)}'
    if D >= 3:
        n = r.choice([5, 10, 20])
        stem += f' Calculate the total time for {n} copies and explain why 3D printing is better suited to one-off items than to mass production.'
        key += f'; {n} copies: {num(round(hrs * n, 2))} hours [1]; slow per item and costs do not fall much with volume, unlike moulding [1]'
        ans += f'; {num(round(hrs * n, 2))} hours for {n}; slow per item, so best for customised or one-off items.'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 3 Communications technology
t = T(3, 'Network components and types: WLAN, WPAN, VPN and their uses', 'network components and types', 'wlan, wpan, vpn',
      defs=[('wireless local area network (WLAN)', 'A local area network in which devices connect using radio waves (Wi-Fi) through wireless access points rather than cables.'),
            ('wireless personal area network (WPAN)', 'A very short-range wireless network, such as Bluetooth, connecting devices around one person, e.g. a phone and earbuds.'),
            ('virtual private network (VPN)', 'A secure, encrypted connection (tunnel) over a public network such as the internet, allowing a remote user to access a private network as if connected locally.'),
            ('wireless access point (WAP)', 'A device that allows wireless devices to connect to a wired network using Wi-Fi.')],
      mcqs=[('Which network type connects a smart watch to a phone?', 'WPAN', ['WAN', 'WLAN', 'VPN'], 'Bluetooth WPAN covers a few metres.'),
            ('Why would a travelling sales manager use a VPN?', 'To access the company network securely over public Wi-Fi', ['To increase the battery life of the laptop', 'To print without a printer', 'To avoid needing an internet connection'], 'The VPN encrypts traffic through a tunnel.'),
            ('Which is a disadvantage of a WLAN compared with a wired LAN?', 'Signals can be intercepted and are affected by interference', ['Devices must be connected by cables', 'It cannot connect laptops', 'It has unlimited range'], 'Radio signals pass through walls and can be picked up.')],
      exps=[('Explain how a VPN keeps data secure.', 'It creates an encrypted tunnel between the user\'s device and the private network, so data sent over the internet cannot be read if intercepted; users must also authenticate.', '1 mark encrypted tunnel; 1 mark intercepted data unreadable/authentication. [2]'),
            ('Explain two advantages of a WLAN for an office.', 'Staff can move around with laptops; no cabling costs or disruption; easy to add devices; supports visitors and mobile devices.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('A VPN can protect data on public Wi-Fi.', 'Data travels through an encrypted tunnel.'),
           ('Bluetooth is an example of a WPAN.', 'It connects devices within a few metres of one person.')],
      falses=['A WPAN covers a whole city.', 'A VPN removes the need for internet access.'],
      intros=['{org}, {aot} in {city}, has staff who work in the office, at home and while travelling.',
              '{p} is planning the network for a new branch of {org} in {city}.'],
      parts=[('Describe what is meant by a WLAN.', 'A local network where devices connect wirelessly through access points.', '1 mark local; 1 mark wireless/access points. [2]'),
             ('Explain why staff working from home should use a VPN.', 'Encrypted tunnel protects data over the internet; access to internal resources as if in the office.', '1 mark each. [2]'),
             ('Describe one use of a WPAN by staff.', 'Bluetooth headset with phone; smart watch notifications; wireless keyboard/mouse.', '1 mark use; 1 mark description. [2]'),
             ('Explain two ways to secure the WLAN.', 'WPA2/WPA3 encryption; strong passphrase; hide SSID; MAC filtering; separate guest network.', '2 × (1 mark method, 1 mark explanation). [4]')],
      ev=[('whether {org} should rely on a WLAN rather than a cabled network in its new branch', 'mobility; cheaper and faster installation; flexible.', 'lower speed and reliability; interference; security risks; limited range.', 'a mix — cabled for fixed workstations and servers, wireless for mobile users.')])


PROTO = [('sending an email from a mail client to the mail server', 'SMTP'), ('reading emails stored on the server from several devices', 'IMAP'),
         ('uploading website files to a web server', 'FTP'), ('requesting a web page from a web server', 'HTTP (or HTTPS)'),
         ('making a telephone call over the internet', 'VoIP'), ('breaking data into packets and making sure they all arrive and are reassembled in order', 'TCP'),
         ('routing packets to the correct destination address', 'IP'), ('sending card details securely to an online shop', 'HTTPS')]
PNAMES = sorted({x[1] for x in PROTO})

t = T(3, 'Network protocols: TCP/IP, HTTP, FTP, SMTP, IMAP and VoIP', 'network protocols', 'tcp/ip, http, ftp, smtp, imap and voip',
      defs=[('protocol', 'A set of rules that governs how data is formatted, transmitted and received between devices on a network.'),
            ('TCP/IP', 'The suite of protocols used by the internet: TCP splits data into packets and ensures reliable, ordered delivery; IP addresses and routes the packets.'),
            ('SMTP', 'Simple Mail Transfer Protocol: used to send emails from a client to a server and between mail servers.'),
            ('IMAP', 'Internet Message Access Protocol: used to read and manage emails that stay stored on the mail server, so they can be synchronised across devices.'),
            ('FTP', 'File Transfer Protocol: used to transfer files between a client and a server, for example to upload web pages.'),
            ('VoIP', 'Voice over Internet Protocol: transmitting voice calls as data packets over the internet.')],
      mcqs=[('Which protocol keeps emails on the server so they can be read on a phone and a laptop?', 'IMAP', ['SMTP', 'FTP', 'POP3 with delete-after-download'], 'IMAP synchronises mailboxes on the server.'),
            ('Which part of TCP/IP is responsible for reassembling packets in the correct order?', 'TCP', ['IP', 'HTTP', 'FTP'], 'TCP uses sequence numbers and acknowledgements.'),
            ('Why can VoIP calls suffer from poor quality?', 'Packets can be delayed or lost when the network is congested', ['VoIP uses analogue telephone lines only', 'VoIP cannot use microphones', 'VoIP calls are always encrypted twice'], 'Latency, jitter and packet loss.')],
      exps=[('Explain why protocols are needed for communication on the internet.', 'Devices from different manufacturers and running different software must agree on rules for formatting, addressing and error checking, otherwise they could not understand each other\'s data.', '1 mark common rules; 1 mark different devices/interoperability. [2]'),
            ('Explain the roles of TCP and IP when a file is sent across the internet.', 'TCP splits the file into numbered packets, checks they arrive and requests resends, then reassembles them in order; IP adds source and destination addresses and routers use them to route each packet.', '1 mark TCP packets/sequence; 1 mark TCP acknowledgements/resend; 1 mark IP addressing/routing. [3]'),
            ('Explain the difference between HTTP and HTTPS.', 'HTTPS is HTTP sent over TLS: data is encrypted and the server is authenticated by a certificate, so it cannot be read if intercepted; HTTP is sent as plain text.', '1 mark encryption; 1 mark authentication/certificate. [2]')],
      ars=[('SMTP is used to send email.', 'It transfers messages from the client to the mail server and between servers.'),
           ('TCP can request lost packets to be resent.', 'The receiver acknowledges packets that arrive.'),
           ('FTP is used to upload website files.', 'It transfers files between a client and a server.')],
      falses=['IMAP is used to upload files to a web server.', 'IP reassembles packets in order.', 'VoIP sends calls through the post.'],
      intros=['{org} in {city} runs its own website, email system and internet telephone system.',
              '{p} is training new technicians at {org} in {city} about network protocols.'],
      parts=[('Explain what is meant by a protocol.', 'An agreed set of rules for data communication.', '1 mark rules; 1 mark for communication between devices. [2]'),
             ('State the protocol used to send email and the protocol used to read it on several devices.', 'SMTP to send; IMAP to read/synchronise.', '1 mark each. [2]'),
             ('Describe how TCP/IP transmits a file.', 'Split into packets with sequence numbers and addresses; routed independently; acknowledged; reassembled; lost packets resent.', '1 mark per point, max 4. [4]'),
             ('Explain one advantage and one disadvantage of VoIP.', 'Cheap/free calls, video, international; but quality depends on bandwidth, needs power/internet.', '1 mark each. [2]')],
      ev=[('whether {org} should replace its traditional telephone lines with VoIP', 'lower call costs; extra features (video, voicemail to email); works anywhere with internet.', 'quality depends on bandwidth; fails in power or internet outages; security of calls; emergency call location.', 'VoIP is usually worthwhile with a reliable connection and a backup line for emergencies.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def g12_proto(r, D):
    s, p = r.choice(PROTO)
    if D <= 2:
        return MCQ(r, f'Which protocol is used for {s}?', p, [x for x in PNAMES if x != p and not (p.startswith('HTTP') and x.startswith('HTTP'))], f'{p} is used for {s}.')
    picks = r.sample(PROTO, 3 if D == 3 else 4)
    lines = '\n'.join(f'{i + 1}. {cap(x[0])}' for i, x in enumerate(picks))
    return Q(f'Name the protocol used for each task.\n{lines}', '; '.join(f'{i + 1} {x[1]}' for i, x in enumerate(picks)), '1 mark each: ' + '; '.join(f'{i + 1} {x[1]}' for i, x in enumerate(picks)) + f'. [{len(picks)}]', marks=len(picks))


@t.add('C3', (2, 3, 4, 5), 'numerical')
def g12_packets(r, D):
    size_kb = r.choice([6, 12, 20, 45, 64, 100, 250])
    payload = r.choice([500, 1000, 1460])
    hdr = r.choice([20, 40])
    byt = size_kb * 1000
    n = math.ceil(byt / payload)
    tot = byt + n * hdr
    stem = f'A {size_kb} KB file (1 KB = 1000 bytes) is sent using TCP/IP. Each packet carries up to {payload} bytes of data plus a {hdr}-byte header. Calculate the number of packets needed and the total number of bytes transmitted.'
    key = f'packets = {byt:,} ÷ {payload} = {byt / payload:.2f} → {n} [1]; headers = {n} × {hdr} = {n * hdr:,} bytes [1]; total = {byt:,} + {n * hdr:,} = {tot:,} bytes [1]'
    ans = f'{n} packets; {tot:,} bytes'
    m = 3
    if D >= 4:
        lost = r.choice([2, 3, 5])
        stem += f' {lost} packets are lost and must be resent. Explain how TCP detects this and calculate the new total number of bytes sent (assume each resent packet is full size).'
        key += f'; missing sequence numbers / no acknowledgement so packets resent [1]; extra {lost} × {payload + hdr} = {lost * (payload + hdr):,}, total {tot + lost * (payload + hdr):,} bytes [1]'
        ans += f'; lost packets detected by missing acknowledgements/sequence numbers; total {tot + lost * (payload + hdr):,} bytes'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(3, 'Transmission media and mobile communication: fibre optic, satellites, GPS and 4G/5G', 'transmission media and mobile communication', 'fibre optic, satellites, gps', '4g/5g',
      defs=[('fibre-optic cable', 'A cable that transmits data as pulses of light along thin glass or plastic fibres, giving very high bandwidth over long distances with little interference.'),
            ('geostationary satellite', 'A satellite about 35 786 km above the equator that orbits at the same rate as the Earth rotates, so it stays above the same point.'),
            ('Global Positioning System (GPS)', 'A satellite navigation system in which a receiver calculates its position from the time taken for signals to arrive from at least four satellites.'),
            ('5G', 'The fifth generation of mobile network technology, offering much higher data rates, lower latency and support for many more connected devices than 4G.'),
            ('latency', 'The time delay between data being sent and being received.')],
      mcqs=[('Why does fibre-optic cable suffer less interference than copper cable?', 'It carries light, which is not affected by electromagnetic interference', ['It is thicker than copper cable', 'It carries radio waves', 'It is always buried deeper'], 'Light signals are immune to EMI.'),
            ('How many satellites must a GPS receiver normally receive signals from to calculate a 3D position?', 'At least four', ['One', 'Two', 'Exactly three, never more'], 'Four signals solve for position and clock error.'),
            ('Which is the main reason 5G suits autonomous vehicles better than 4G?', 'Much lower latency', ['It uses copper cables', 'It has fewer masts', 'It only works indoors'], 'Fast response is safety-critical.')],
      exps=[('Explain why communication via geostationary satellites has noticeable latency.', 'The signal must travel about 35 786 km up to the satellite and the same distance down, which takes around a quarter of a second even at the speed of light.', '1 mark long distance up and down; 1 mark time delay at speed of light. [2]'),
            ('Explain two advantages of fibre-optic cable over copper cable.', 'Higher bandwidth/faster; longer distances without repeaters; immune to electromagnetic interference; harder to tap; lighter.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Describe how a GPS receiver calculates its position.', 'Satellites broadcast signals with their position and exact time; the receiver measures how long each signal took; distance = speed × time; with four satellites it calculates its position (trilateration).', '1 mark per point, max 3. [3]')],
      ars=[('Fibre-optic cables are used for internet backbones.', 'They carry very large amounts of data over long distances.'),
           ('Satellite internet has high latency.', 'Signals travel tens of thousands of kilometres to geostationary satellites and back.')],
      falses=['GPS receivers send signals to satellites to find their position.', 'Fibre-optic cables carry electrical currents.'],
      intros=['{org} in {city} has a branch in a remote mountain area and a fleet of delivery vehicles.',
              '{org}, {aot} in {city}, is upgrading the links to its remote branch and the mobile data used by its delivery drivers.'],
      parts=[('Explain why fibre-optic cable would give a faster connection than copper cable.', 'Light pulses give much higher bandwidth with less signal loss and no interference.', '1 mark bandwidth; 1 mark less loss/interference. [2]'),
             ('Explain why satellite communication may be used for the remote site.', 'No cable infrastructure needed; covers remote areas.', '1 mark each. [2]'),
             ('Describe how GPS could be used to track the vehicles.', 'Receiver in each vehicle calculates position from satellite signals and sends it via mobile network to a tracking system.', '1 mark GPS position; 1 mark transmitted to base. [2]'),
             ('Explain two benefits of 5G for the organisation.', 'Higher speeds; lower latency; more devices; better for real-time tracking and video.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ev=[('whether {org} should use satellite rather than fibre-optic connections for its remote sites', 'available anywhere; quick to set up; no cable laying.', 'high latency; weather affects signal; higher cost per GB; lower bandwidth.', 'satellite is best where fibre is unavailable or too costly; fibre is preferred where it can be installed.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_latency(r, D):
    alt = r.choice([35786, 20200, 550, 1200])
    kind = {35786: 'geostationary', 20200: 'GPS (medium Earth orbit)', 550: 'low Earth orbit', 1200: 'low Earth orbit'}[alt]
    c = 3e5
    one = alt / c
    rt = 2 * alt / c
    if D == 1:
        return MCQ(r, f'A {kind} satellite is {alt:,} km above the ground. Radio signals travel at 300 000 km/s. How long does a signal take to go up to the satellite and back down?', f'{rt * 1000:.1f} ms',
                   [f'{one * 1000:.1f} ms', f'{rt * 1000 * 2:.1f} ms', f'{rt:.1f} ms'], f'2 × {alt:,} ÷ 300 000 = {rt:.4f} s = {rt * 1000:.1f} ms.')
    stem = f'A {kind} satellite orbits {alt:,} km above the Earth. Radio signals travel at 300 000 km/s. Calculate the time, in milliseconds, for a signal to travel from a ground station up to the satellite and down to another ground station (assume both are directly below).'
    key = f'distance = 2 × {alt:,} = {2 * alt:,} km [1]; time = {2 * alt:,} ÷ 300 000 = {rt:.4f} s [1] = {rt * 1000:.1f} ms [1]'
    ans = f'{rt * 1000:.1f} ms'
    m = 3
    if D >= 4:
        stem += ' For a video call the reply must also return the same way. Calculate the round-trip delay and explain its effect on the call.'
        key += f'; round trip = 2 × {rt * 1000:.1f} = {2 * rt * 1000:.1f} ms [1]; noticeable delay causes people to talk over each other [1]'
        ans += f'; round trip {2 * rt * 1000:.1f} ms, causing noticeable delays in conversation' if alt > 5000 else f'; round trip {2 * rt * 1000:.1f} ms, small enough for normal conversation'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4), 'numerical')
def g12_4g5g(r, D):
    size = r.choice([0.5, 1, 2, 4, 8])
    s4 = r.choice([20, 30, 40, 50])
    s5 = r.choice([200, 300, 500, 1000])
    bits = size * 8e9
    t4, t5 = bits / (s4 * 1e6), bits / (s5 * 1e6)
    stem = (f'A {num(size)} GB video (1 GB = 10⁹ bytes) is downloaded on a 4G connection at {s4} Mbps and on a 5G connection at {s5} Mbps (1 Mbps = 10⁶ bits per second). '
            f'Calculate the download time on each network, in seconds.')
    key = f'{num(size)} GB × 8 = {bits:,.0f} bits [1]; 4G: ÷ {s4 * 1e6:,.0f} = {num(round(t4, 1))} s [1]; 5G: ÷ {s5 * 1e6:,.0f} = {num(round(t5, 1))} s [1]'
    m = 3
    ans = f'4G {num(round(t4, 1))} s; 5G {num(round(t5, 1))} s'
    if D >= 4:
        stem += ' Explain why real download times are usually longer than these figures.'
        key += '; quoted speeds are maximums; shared bandwidth, distance from mast, interference, protocol overheads [1]'
        ans += '; speeds are shared and affected by signal strength and overheads.'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(3, 'Network security: firewalls, proxy servers and encryption', 'network security', 'firewalls, proxy servers and encryption',
      defs=[('firewall', 'Hardware or software that monitors traffic between a network and the outside world and blocks or allows packets according to a set of rules.'),
            ('proxy server', 'A server that acts as an intermediary between users and the internet, forwarding requests, hiding internal addresses, filtering content and caching web pages.'),
            ('packet filtering', 'A firewall technique that checks each packet\'s source and destination addresses and port numbers against rules.'),
            ('end-to-end encryption', 'Encryption in which only the sender and the recipient can decrypt the messages, not the service provider or anyone in between.')],
      mcqs=[('Which is a function of a proxy server?', 'Caching frequently visited web pages to speed up access', ['Converting analogue to digital signals', 'Storing users\' passwords in plain text', 'Assigning MAC addresses'], 'Proxies cache, filter and anonymise.'),
            ('A firewall rule blocks incoming traffic on port 23. What is the effect?', 'Telnet connections from outside are refused', ['All web browsing is blocked', 'Email can no longer be sent', 'The network becomes wireless'], 'Port 23 is Telnet.'),
            ('Which is a limitation of a firewall?', 'It cannot stop a user from opening an infected email attachment that it allowed through', ['It cannot block any ports', 'It cannot be configured', 'It only works on printers'], 'Firewalls do not replace anti-malware or user training.')],
      exps=[('Explain how a firewall protects a network.', 'It checks every packet entering or leaving against rules (addresses, ports, protocols) and blocks packets that are not allowed, preventing unauthorised access and some attacks.', '1 mark inspects traffic; 1 mark rules; 1 mark blocks unauthorised. [3]'),
            ('Explain two benefits of a proxy server for a school.', 'Filters inappropriate websites; caches pages so they load faster and save bandwidth; hides internal IP addresses; logs internet use.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('A proxy server can hide the IP addresses of internal computers.', 'Requests to websites appear to come from the proxy server.'),
           ('Firewalls can block traffic on specific ports.', 'Rules can match port numbers in packet headers.')],
      falses=['A firewall removes viruses from infected files.', 'Proxy servers make every web page load more slowly.'],
      intros=['{org}, {aot} in {city}, is reviewing its network security after an attack on a similar organisation.',
              '{p} manages the network at {org} in {city}, where staff use the internet every day.'],
      parts=[('Describe how a firewall works.', 'Monitors incoming/outgoing packets; compares with rules; blocks or allows.', '1 mark per point, max 3. [3]'),
             ('Explain two functions of a proxy server.', 'Content filtering; caching; anonymity; logging.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Explain why encryption is needed even with a firewall.', 'Data outside the network can be intercepted; encryption makes it unreadable.', '1 mark interception; 1 mark unreadable. [2]')],
      ev=[('whether a firewall and a proxy server are enough to keep the network of {org} secure', 'block unauthorised traffic; filter sites; hide addresses; log activity.', 'insider threats; phishing and malware via allowed traffic; encrypted traffic is harder to inspect; misconfiguration.', 'they are essential layers but must be combined with encryption, anti-malware, updates and training.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_firewall(r, D):
    ports = {80: 'HTTP', 443: 'HTTPS', 25: 'SMTP', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 3389: 'Remote Desktop', 143: 'IMAP'}
    plist = list(ports)
    allow = r.sample(plist, 3)
    deny_ip = f'203.0.113.{r.randrange(2, 250)}'
    rules = [f'1 DENY all traffic from {deny_ip}'] + [f'{i + 2} ALLOW incoming traffic to port {p} ({ports[p]})' for i, p in enumerate(allow)] + [f'{len(allow) + 2} DENY all other incoming traffic']
    n = 3 if D <= 2 else (4 if D <= 4 else 5)
    pk = []
    for _ in range(n):
        ip = deny_ip if r.random() < 0.25 else f'198.51.100.{r.randrange(2, 250)}'
        p = r.choice(plist)
        pk.append((ip, p))

    def decide(ip, p):
        if ip == deny_ip:
            return 'blocked (rule 1)'
        if p in allow:
            return f'allowed (rule {allow.index(p) + 2})'
        return f'blocked (rule {len(allow) + 2})'
    out = [decide(ip, p) for ip, p in pk]
    rt = code(rules)
    if D == 1:
        ip, p = pk[0]
        a = out[0].split(' ')[0].capitalize()
        return MCQ(r, f'A firewall applies these rules in order, stopping at the first match:\n{rt}\nAn incoming packet comes from {ip} to port {p}. What happens?', a, ['Blocked' if a == 'Allowed' else 'Allowed', 'Forwarded to the proxy for caching', 'Converted to a VPN packet'], f'{out[0]}.')
    stem = f'A firewall applies these rules in order, stopping at the first rule that matches:\n{rt}\nState whether each incoming packet is allowed or blocked, and which rule applies:\n' + '\n'.join(f'{i + 1}. from {ip} to port {p}' for i, (ip, p) in enumerate(pk))
    m = n
    key = '1 mark each: ' + '; '.join(f'{i + 1} {o}' for i, o in enumerate(out))
    if D >= 4:
        stem += '\nExplain why the order of the rules matters.'
        key += '; the first matching rule is applied, so a general rule placed too early would override more specific rules [1]'
        m += 1
    return Q(stem, '; '.join(f'{i + 1} {o}' for i, o in enumerate(out)), key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 4 Project management
t = T(4, 'Stages of the project life cycle: initiation, planning, execution, monitoring and closure', 'stages of the project life cycle', 'initiation, planning, execution, monitoring and closure',
      defs=[('initiation stage', 'The first stage of a project, in which the problem or opportunity is identified, aims and feasibility are agreed and a project manager is appointed.'),
            ('planning stage', 'The stage in which tasks, timescales, resources, budgets and risks are worked out, often using Gantt or PERT charts.'),
            ('execution stage', 'The stage in which the planned tasks are carried out and the product or system is built.'),
            ('monitoring and control', 'Checking progress against the plan throughout the project and taking action if tasks are late or over budget.'),
            ('closure stage', 'The final stage, in which the finished product is handed over, the project is evaluated and lessons learned are recorded.')],
      mcqs=[('In which stage of the project life cycle is a feasibility study usually carried out?', 'Initiation', ['Execution', 'Closure', 'Monitoring'], 'Initiation decides whether the project should go ahead.'),
            ('Which activity belongs to the closure stage?', 'Evaluating the project and recording lessons learned', ['Allocating resources to tasks for the first time', 'Writing the project brief', 'Building the system'], 'Closure reviews and hands over.'),
            ('Why is monitoring carried out throughout a project?', 'To compare progress with the plan and take action early if there are problems', ['To decide whether the project should start', 'To replace the project manager', 'To delete the plan'], 'Early detection of slippage.')],
      exps=[('Explain why a project must be planned before work starts.', 'Planning identifies tasks, their order, durations and resources, so a realistic deadline and budget can be set and problems anticipated.', '1 mark tasks/order/resources; 1 mark realistic deadlines/budgets/risks. [2]'),
            ('Explain the purpose of a project review at the closure stage.', 'It evaluates whether the aims were met on time and within budget and records lessons learned so future projects can avoid the same problems.', '1 mark evaluate success; 1 mark lessons for future. [2]'),
            ('Describe two tasks carried out by a project manager during execution.', 'Assigning tasks to team members; communicating with stakeholders; monitoring progress and budget; resolving problems; updating the plan.', '1 mark each, max 2. [2]')],
      ars=[('A feasibility study is part of the initiation stage.', 'It decides whether the project is worth carrying out.'),
           ('Monitoring continues throughout the project.', 'Progress must be compared with the plan at every stage.')],
      falses=['The closure stage is when the project aims are first agreed.', 'Planning happens only after the product is finished.'],
      intros=['{org}, {aot} in {city}, is starting a project to introduce a new online booking system.',
              '{p} has been appointed project manager at {org} in {city} to move the offices to a new building.'],
      parts=[('Describe what happens in the initiation stage.', 'Identify the problem/opportunity; set aims and objectives; feasibility study; appoint project manager; agree scope.', '1 mark per point, max 3. [3]'),
             ('Describe two activities in the planning stage.', 'Break project into tasks; estimate durations; allocate resources; set budget; create Gantt/PERT chart; risk assessment.', '1 mark each, max 2. [2]'),
             ('Explain why monitoring is important during execution.', 'Detect delays or overspending early so corrective action can be taken.', '1 mark detect problems; 1 mark take action. [2]'),
             ('Describe what happens at the closure stage.', 'Hand over product; sign-off by client; evaluate; release resources; document lessons learned.', '1 mark per point, max 3. [3]')],
      ev=[('the importance of the planning stage to the success of the project at {org}', 'clear tasks, deadlines and budgets; risks anticipated; resources allocated.', 'plans may be wrong if estimates are poor; too much planning delays work; monitoring and good communication also matter.', 'planning is vital but must be reviewed and updated through monitoring.')])

ACT_NAMES = ['Gather requirements', 'Design database', 'Design interface', 'Buy hardware', 'Write code', 'Install network',
             'Install system', 'Convert data', 'Test system', 'Review security', 'Write documentation', 'Train staff']


def cpa(r, D):
    n = 6 if D <= 3 else (7 if D == 4 else 8)
    for _ in range(80):
        dur = [r.randrange(1, 9) for _ in range(n)]
        pre = [[]]
        for i in range(1, n):
            k = r.choice([1, 1, 2]) if i > 1 else 1
            pre.append(sorted(r.sample(range(i), min(k, i))))
        succ = [[j for j in range(n) if i in pre[j]] for i in range(n)]
        if sum(1 for i in range(n) if not succ[i]) > 2:
            continue
        es = [0] * n
        ef = [0] * n
        for i in range(n):
            es[i] = max((ef[p] for p in pre[i]), default=0)
            ef[i] = es[i] + dur[i]
        T_ = max(ef)
        lf = [0] * n
        ls = [0] * n
        for i in reversed(range(n)):
            lf[i] = min((ls[s] for s in succ[i]), default=T_)
            ls[i] = lf[i] - dur[i]
        fl = [ls[i] - es[i] for i in range(n)]
        paths = []

        def walk(i, path):
            if not succ[i]:
                paths.append(path)
                return
            for s in succ[i]:
                walk(s, path + [s])
        for i in range(n):
            if not pre[i]:
                walk(i, [i])
        longest = [p for p in paths if sum(dur[x] for x in p) == T_]
        if len(longest) == 1 and any(f > 0 for f in fl):
            return dur, pre, es, ef, ls, lf, fl, T_, longest[0]
    return None


t = T(4, 'Project management tools: Gantt charts, PERT charts and critical path analysis', 'project management tools', 'gantt charts, pert charts', 'critical path analysis',
      defs=[('Gantt chart', 'A bar chart showing each task of a project against a timeline, with its start date, duration and how tasks overlap.'),
            ('PERT chart', 'A network diagram showing project tasks as linked nodes or arrows, with their dependencies and durations.'),
            ('critical path', 'The longest sequence of dependent tasks through a project; it determines the shortest possible project duration.'),
            ('float (slack)', 'The amount of time a task can be delayed without delaying the whole project.'),
            ('milestone', 'A significant point in a project, such as completing a stage, used to check progress.'),
            ('dependency', 'A relationship in which one task cannot start until another task has finished.')],
      mcqs=[('What happens if a task on the critical path is delayed by two days?', 'The whole project is delayed by two days', ['Nothing, because it has float', 'The project finishes two days early', 'Only the next task is affected'], 'Critical tasks have zero float.'),
            ('Which tool shows tasks as horizontal bars against time?', 'Gantt chart', ['PERT chart', 'Data flow diagram', 'Entity-relationship diagram'], 'Bars show duration and timing.'),
            ('What is the float of a task on the critical path?', 'Zero', ['Equal to its duration', 'Equal to the project duration', 'Always one day'], 'Any delay to a critical task delays the project.')],
      exps=[('Explain why the critical path is important to a project manager.', 'It shows which tasks cannot be delayed without delaying the project, so the manager can focus monitoring and resources on them; it gives the minimum project duration.', '1 mark minimum duration; 1 mark tasks with no float need close monitoring/resources. [2]'),
            ('Explain one advantage of a Gantt chart and one advantage of a PERT chart.', 'Gantt: easy to see when tasks happen and overlap and to track progress against dates. PERT: clearly shows dependencies between tasks and the critical path.', '1 mark Gantt; 1 mark PERT. [2]'),
            ('Explain how float can help a project manager allocate resources.', 'Tasks with float can be rescheduled within that float, so staff can be moved to critical tasks or work can be spread out without delaying the project.', '1 mark tasks can move within float; 1 mark resources moved/levelled. [2]')],
      ars=[('Delaying a critical task delays the project.', 'Critical tasks have no float.'),
           ('A Gantt chart can show tasks happening at the same time.', 'Bars for parallel tasks overlap on the timeline.')],
      falses=['The critical path is the shortest route through the project.', 'Tasks on the critical path have the most float.'],
      intros=['{p} is planning the installation of a new computer system for {org} in {city}.',
              '{org}, {aot} in {city}, is planning a project to launch a new website.'],
      parts=[('Explain what is meant by the critical path.', 'Longest chain of dependent tasks; determines minimum project time; no float.', '1 mark per point, max 2. [2]'),
             ('Explain what is meant by float.', 'Time a task can be delayed without delaying the project.', '1 mark meaning; 1 mark example/consequence. [2]'),
             ('Explain why a Gantt chart would be useful to the project team.', 'Shows when each task starts and ends, overlapping tasks and progress against the timeline.', '1 mark per point, max 2. [2]'),
             ('Describe how project management software could help with this plan.', 'Draws Gantt/PERT charts automatically; recalculates the critical path when durations change; allocates resources; tracks progress.', '1 mark per point, max 3. [3]')],
      ev=[('the use of critical path analysis by {org} for planning the project', 'shows minimum duration and critical tasks; helps prioritise; identifies float for resource planning.', 'depends on accurate duration estimates; complex for large projects; does not show resource limits on its own; plans change.', 'CPA is a valuable planning aid if it is updated regularly and combined with Gantt charts and monitoring.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_cpa(r, D):
    res = cpa(r, D)
    if not res:
        return None
    dur, pre, es, ef, ls, lf, fl, T_, cp = res
    n = len(dur)
    L = 'ABCDEFGH'
    names = sorted(r.sample(ACT_NAMES, n), key=ACT_NAMES.index)
    rows = [(L[i], names[i], dur[i], ', '.join(L[p] for p in pre[i]) or '–') for i in range(n)]
    table = tbl(['Task', 'Description', 'Duration (days)', 'Preceded by'], rows)
    cps = ' → '.join(L[i] for i in cp)
    d = ctx(r)
    lead = f'{d["org"]} in {d["city"]} is planning a project with these tasks:\n{table}\n'
    if D == 1:
        return MCQ(r, lead + 'What is the minimum time needed to complete the project?', f'{T_} days', [f'{sum(dur)} days', f'{T_ - 1} days', f'{T_ + 2} days', f'{max(dur)} days'], f'Critical path {cps} = {T_} days.')
    stem = lead + 'Identify the critical path and calculate the minimum project duration.'
    key = f'critical path {cps} [2]; duration {" + ".join(str(dur[i]) for i in cp)} = {T_} days [1]'
    ans = f'Critical path {cps}; {T_} days'
    m = 3
    nc = [i for i in range(n) if fl[i] > 0]
    if D >= 3:
        j = r.choice(nc)
        stem += f' Calculate the float for task {L[j]}.'
        key += f'; task {L[j]}: earliest start {es[j]}, latest start {ls[j]}, float = {ls[j]} − {es[j]} = {fl[j]} days [1]'
        ans += f'; float of {L[j]} = {fl[j]} days'
        m += 1
    if D >= 4:
        j = r.choice(range(n))
        dl = r.randrange(1, 5)
        newT = T_ + max(0, dl - fl[j])
        stem += f' Task {L[j]} is delayed by {dl} days. State the effect on the project completion time.'
        key += f'; {L[j]} has float {fl[j]}: ' + (f'delay ≤ float so project still {T_} days [1]' if dl <= fl[j] else f'project delayed by {dl} − {fl[j]} = {dl - fl[j]} days to {newT} days [1]')
        ans += f'; delaying {L[j]} by {dl} days gives a completion time of {newT} days'
        m += 1
    if D >= 5:
        stem += ' Give the earliest start time of every task.'
        key += '; earliest starts ' + ', '.join(f'{L[i]} {es[i]}' for i in range(n)) + ' [1]'
        ans += '; earliest starts ' + ', '.join(f'{L[i]} {es[i]}' for i in range(n))
        m += 1
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4), 'numerical')
def g12_gantt(r, D):
    n = 4 if D <= 3 else 5
    tasks = sorted(r.sample(ACT_NAMES, n), key=ACT_NAMES.index)
    starts, durs = [], []
    s = 1
    for i in range(n):
        dd = r.randrange(2, 7)
        if i and r.random() < 0.5:
            st = starts[-1] + r.randrange(0, durs[-1])
        else:
            st = (starts[-1] + durs[-1]) if i else 1
        starts.append(st)
        durs.append(dd)
    ends = [a + b - 1 for a, b in zip(starts, durs)]
    lines = [f'{tk}: starts day {a}, lasts {b} days' for tk, a, b in zip(tasks, starts, durs)]
    day = r.randrange(2, max(ends))
    active = [tk for tk, a, e in zip(tasks, starts, ends) if a <= day <= e]
    stem = 'A Gantt chart for a project shows:\n' + code(lines) + f'\nState (a) the day on which the project finishes and (b) which tasks are in progress on day {day}.'
    ans = f'(a) day {max(ends)} (b) ' + (', '.join(active) or 'none')
    key = f'(a) last task ends day {max(ends)} (start + duration − 1) [1] (b) {", ".join(active) or "none"} [1]. [2]'
    return Q(stem, ans, key, marks=2, typ='numerical')


t = T(4, 'Project management software: resource allocation, budgeting, communication and collaboration', 'project management software', 'resource allocation, budgeting', 'communication and collaboration',
      defs=[('project management software', 'Software used to plan and track projects, including scheduling tasks, drawing Gantt charts, allocating resources, tracking costs and sharing information.'),
            ('resource allocation', 'Assigning people, equipment and money to project tasks so that each task has what it needs when it needs it.'),
            ('budget', 'The planned amount of money available for a project, broken down by task or category, against which actual spending is tracked.'),
            ('collaboration tools', 'Features such as shared files, comments, task boards and messaging that let team members work together, often from different places.')],
      mcqs=[('Which feature of project management software warns that one employee has been given two tasks at the same time?', 'Resource allocation / over-allocation alerts', ['Spell checking', 'Mail merge', 'Data compression'], 'Resource views show over-allocated staff.'),
            ('How does project management software help with budgeting?', 'It compares actual spending with planned costs for each task', ['It prints money', 'It removes the need for a budget', 'It hides the cost of tasks'], 'Variance tracking.')],
      exps=[('Explain two ways project management software improves communication in a team.', 'Shared online plan everyone can see; automatic notifications of task changes; comments and file sharing in one place; dashboards for managers.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why it is useful that project management software recalculates the schedule automatically.', 'When a task\'s duration or dependency changes, the new dates and critical path are produced immediately, so the manager sees the effect and can act.', '1 mark automatic recalculation; 1 mark see effect/act quickly. [2]')],
      ars=[('Project management software can show over-allocated staff.', 'It compares each person\'s assigned tasks with their available hours.'),
           ('Collaboration tools help teams in different locations.', 'Files, tasks and messages are shared online.')],
      falses=['Project management software removes the need for a project manager.', 'Budgets cannot be tracked in project management software.'],
      intros=['{org} in {city} is running a large IT project with team members in three countries.',
              '{p} manages several projects at once at {org} in {city}.'],
      parts=[('Describe three features of project management software.', 'Gantt/PERT charts; scheduling; resource allocation; budgeting; progress tracking; reports; collaboration.', '1 mark each, max 3. [3]'),
             ('Explain how the software helps with resource allocation.', 'Assigns staff/equipment to tasks; shows availability; warns of over-allocation; levelling.', '1 mark per point, max 2. [2]'),
             ('Explain how the software supports collaboration.', 'Shared plans and documents; comments; notifications; online access from anywhere.', '1 mark per point, max 2. [2]')],
      ev=[('the benefits and drawbacks for {org} of using project management software', 'automatic scheduling; clear overview; resource and budget tracking; collaboration.', 'cost and training; data only as good as updates entered; can become complex; over-reliance on software.', 'beneficial for large or distributed projects if the team keeps it up to date.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def g12_budget(r, D):
    n = 3 if D <= 3 else 4
    tasks = r.sample(ACT_NAMES, n)
    rates = [r.choice([25, 30, 40, 50, 60]) for _ in tasks]
    hours = [r.choice([20, 30, 40, 60, 80]) for _ in tasks]
    plan = [a * b for a, b in zip(rates, hours)]
    actual_h = [h + r.choice([-10, 0, 5, 10, 20]) for h in hours]
    act = [a * b for a, b in zip(rates, actual_h)]
    rows = [(tk, f'${rt}', h, ah) for tk, rt, h, ah in zip(tasks, rates, hours, actual_h)]
    stem = 'A project\'s staff costs are tracked in project management software:\n' + tbl(['Task', 'Rate per hour', 'Planned hours', 'Actual hours'], rows) + '\nCalculate the planned cost, the actual cost and the variance (actual − planned).'
    key = f'planned = {" + ".join(f"{a}×{b}" for a, b in zip(rates, hours))} = ${sum(plan):,} [1]; actual = ${sum(act):,} [1]; variance = ${sum(act) - sum(plan):+,} [1]'
    ans = f'planned ${sum(plan):,}; actual ${sum(act):,}; variance ${sum(act) - sum(plan):+,}'
    m = 3
    if D >= 4:
        worst = max(range(n), key=lambda i: act[i] - plan[i])
        stem += ' Identify the task with the largest overspend and suggest one action the project manager could take.'
        key += f'; {tasks[worst]} (+${act[worst] - plan[worst]:,}) [1]; action e.g. reallocate staff, revise estimates, reduce scope, negotiate budget [1]'
        ans += f'; largest overspend: {tasks[worst]}'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 5 Graphics creation
FORMATS = [('JPEG', 'bitmap, lossy compression; good for photographs'), ('PNG', 'bitmap, lossless compression; supports transparency'), ('GIF', 'bitmap, lossless, limited to 256 colours; supports simple animation'),
           ('SVG', 'vector format based on XML; scales without loss of quality'), ('BMP', 'bitmap, usually uncompressed; large files'), ('TIFF', 'bitmap, often lossless; used in professional printing')]

t = T(5, 'Vector and bitmap graphics: properties, file formats and compression', 'vector and bitmap graphics', 'properties, file formats and compression',
      defs=[('bitmap (raster) graphic', 'An image stored as a grid of pixels, each with a colour value.'),
            ('vector graphic', 'An image stored as a list of objects (lines, shapes, curves) described by mathematical properties such as coordinates, colour and line width.'),
            ('resolution', 'The number of pixels in a bitmap image, often given as width × height or as pixels per inch (ppi).'),
            ('colour depth', 'The number of bits used to store the colour of each pixel; n bits give 2ⁿ possible colours.'),
            ('pixelation', 'The blocky appearance of a bitmap image when it is enlarged so much that individual pixels become visible.')],
      mcqs=[('Why does a logo stored as a vector graphic stay sharp when enlarged?', 'The shapes are recalculated from their mathematical descriptions at the new size', ['It contains more pixels than a bitmap', 'It is compressed with JPEG', 'It has a higher colour depth'], 'Vectors are resolution-independent.'),
            ('Which format is most suitable for a photograph on a website?', 'JPEG', ['SVG', 'BMP', 'TXT'], 'Lossy compression gives small files with acceptable quality.'),
            ('How many colours can be represented with a colour depth of 8 bits?', '256', ['8', '16', '65 536'], '2⁸ = 256.')],
      exps=[('Explain two advantages of vector graphics over bitmap graphics.', 'They can be scaled to any size without losing quality; file sizes are usually smaller for simple images; individual objects can be edited separately.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why photographs are stored as bitmaps rather than vectors.', 'Photographs contain continuous variations of colour and detail that cannot be described easily as geometric shapes; a pixel grid records each tiny area.', '1 mark complex continuous detail; 1 mark pixels record it. [2]'),
            ('Explain why JPEG is not suitable for an image that will be edited and saved many times.', 'JPEG is lossy: each save discards more data, so quality gets worse each time (artefacts).', '1 mark lossy; 1 mark repeated loss/artefacts. [2]')],
      ars=[('Vector graphics can be enlarged without pixelation.', 'They are stored as mathematical descriptions of shapes.'),
           ('Increasing colour depth increases bitmap file size.', 'More bits are stored for every pixel.'),
           ('PNG is suitable for logos with transparent backgrounds.', 'It supports transparency and uses lossless compression.')],
      falses=['JPEG is a vector format.', 'Bitmap images are stored as lists of shapes.', 'Doubling the colour depth halves the file size.'],
      intros=['{p} is designing a logo, posters and website images for {org} in {city}.',
              '{org} in {city} needs a new logo and product photographs for its website.'],
      parts=[('Explain why the logo should be created as a vector graphic.', 'Scales to any size (business card to billboard) without losing quality; editable objects; small file.', '1 mark per point, max 2. [2]'),
             ('Describe the difference between lossy and lossless compression.', 'Lossy permanently removes data for smaller files; lossless reduces size with no data lost.', '1 mark each. [2]'),
             ('Recommend a file format for the product photographs and justify your choice.', 'JPEG — small files via lossy compression, good for photos.', '1 mark format; 1 mark justification. [2]'),
             ('Explain what happens to a bitmap image when it is enlarged.', 'Pixels are enlarged/interpolated so the image becomes blocky or blurred (pixelation).', '1 mark pixels enlarged; 1 mark pixelation. [2]')],
      ev=[('whether {org} should create all its graphics as vectors', 'scalable without quality loss; small files; easy editing.', 'unsuitable for photographs and realistic images; some software/devices have limited support; complex vectors can be large.', 'use vectors for logos, icons and diagrams and bitmaps for photographs.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_bitmap(r, D):
    w, h = r.choice([(800, 600), (1024, 768), (1920, 1080), (640, 480), (3000, 2000), (1200, 900)])
    cd = r.choice([1, 8, 16, 24])
    byt = w * h * cd / 8
    if D == 1:
        return MCQ(r, f'How many different colours can be shown with a colour depth of {cd} bit{"s" if cd > 1 else ""}?', f'{2 ** cd:,}', [f'{cd * 2:,}', f'{2 ** (cd - 1):,}' if cd > 1 else '1', f'{cd ** 2:,}', f'{2 ** cd * 2:,}'], f'2^{cd} = {2 ** cd:,}.')
    stem = f'A bitmap image is {w} × {h} pixels with a colour depth of {cd} bit{"s" if cd > 1 else ""}. Calculate the file size in megabytes (1 MB = 1 000 000 bytes), ignoring the file header.'
    key = f'{w} × {h} = {w * h:,} pixels [1]; × {cd} bits ÷ 8 = {byt:,.0f} bytes [1]; = {num(round(byt / 1e6, 2))} MB [1]'
    ans = f'{num(round(byt / 1e6, 2))} MB'
    m = 3
    if D >= 3:
        ratio = r.choice([5, 8, 10, 15, 20])
        stem += f' It is saved as a JPEG with a compression ratio of {ratio}:1. Calculate the compressed size in kilobytes (1 KB = 1000 bytes).'
        key += f'; {byt:,.0f} ÷ {ratio} = {byt / ratio:,.0f} bytes = {num(round(byt / ratio / 1000, 1))} KB [1]'
        ans += f'; compressed {num(round(byt / ratio / 1000, 1))} KB'
        m = 4
    if D >= 5:
        nd = r.choice([x for x in (8, 16, 24) if x != cd])
        stem += f' State the effect on the uncompressed file size of changing the colour depth to {nd} bits.'
        key += f'; size × {nd}/{cd} = {num(round(byt * nd / cd / 1e6, 2))} MB [1]'
        ans += f'; at {nd} bits the uncompressed size becomes {num(round(byt * nd / cd / 1e6, 2))} MB'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (1, 2, 3), 'short')
def g12_fmt(r, D):
    uses = [('a photograph for a news website', 'JPEG'), ('a company logo that will be printed at many sizes', 'SVG'), ('a screenshot with sharp text and a transparent background', 'PNG'),
            ('a small looping animated icon with a few colours', 'GIF'), ('a high-quality scan for professional printing', 'TIFF')]
    u, f = r.choice(uses)
    fd = dict(FORMATS)
    if D <= 2:
        return MCQ(r, f'Which file format is most suitable for {u}?', f, [x[0] for x in FORMATS if x[0] != f], f'{f}: {fd[f]}.')
    u2, f2 = r.choice([x for x in uses if x[1] != f])
    return Q(f'Recommend a file format for each use and justify your choice: (1) {u}; (2) {u2}.', f'(1) {f}: {fd[f]}. (2) {f2}: {fd[f2]}.', '1 mark each format, 1 mark each justification. [4]', marks=4)


t = T(5, 'Creating and editing vector graphics: shapes, layers, gradients and grouping', 'creating and editing vector graphics', 'shapes, layers, gradients and grouping',
      defs=[('layer', 'A separate level in a graphic on which objects are placed; objects on higher layers appear in front of those on lower layers.'),
            ('grouping', 'Combining several objects so that they can be moved, resized or formatted together as a single object.'),
            ('gradient fill', 'A fill that changes smoothly from one colour to another across an object (linear or radial).'),
            ('node (anchor point)', 'A point on a vector path that can be moved to change the shape of the path.'),
            ('z-order', 'The stacking order of objects, which decides which object appears in front when objects overlap.')],
      mcqs=[('Why would a designer group the parts of a logo?', 'So all the parts can be moved and resized together without changing their positions relative to each other', ['To convert it to a bitmap', 'To delete hidden layers', 'To reduce the colour depth'], 'Grouped objects act as one.'),
            ('What happens when an object is sent to the back?', 'It appears behind all other overlapping objects', ['It is deleted', 'It becomes transparent', 'It is grouped with the background'], 'Changes the z-order.'),
            ('Why should the aspect ratio be locked when resizing a vector shape?', 'So it does not become stretched or squashed', ['So the colours change', 'So it turns into a bitmap', 'So the file is compressed'], 'Width and height change in proportion.')],
      exps=[('Explain why designers place different parts of a graphic on separate layers.', 'Each layer can be edited, hidden or locked without affecting the others, and the stacking order is easy to control.', '1 mark edit independently; 1 mark hide/lock/order. [2]'),
            ('Explain how a vector shape is changed using nodes.', 'Each node is a point on the path; dragging a node or its handles changes the position or curve of the line, so the shape changes while staying sharp.', '1 mark node = point on path; 1 mark moving it/handles changes curve. [2]')],
      ars=[('Grouped objects can be resized together.', 'Grouping makes several objects behave as one.'),
           ('Objects on a higher layer appear in front of lower layers.', 'Layers are drawn from the bottom up.')],
      falses=['Grouping merges objects into a bitmap.', 'A gradient fill uses a single flat colour.'],
      intros=['{p} is creating a vector poster for an event run by {org} in {city}.',
              'A designer at {org} in {city} is editing the company\'s vector logo.'],
      parts=[('Describe how layers would help in creating the poster.', 'Background, images and text on separate layers; edit/hide/lock independently; control which items are in front.', '1 mark per point, max 2. [2]'),
             ('Explain the purpose of grouping objects.', 'Move/resize/format several objects together keeping their arrangement.', '1 mark each part. [2]'),
             ('Describe how a gradient fill could be used.', 'A smooth blend of colours, e.g. sky from dark to light blue, linear or radial.', '1 mark description; 1 mark example. [2]'),
             ('Explain why the aspect ratio should be maintained when resizing the logo.', 'Prevents distortion so the brand looks correct.', '1 mark distortion; 1 mark brand image. [2]')],
      ev=[('the use of vector graphics software rather than bitmap software for the designs of {org}', 'scalable artwork; editable objects, layers and groups; small files.', 'not suitable for photo editing; learning curve; some effects are easier in bitmap software.', 'vector software suits logos and posters; bitmap software suits photographs — designers often use both.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_zorder(r, D):
    objs = r.sample(['Background', 'Logo', 'Title text', 'Photo frame', 'Star shape', 'Banner', 'Circle'], 4 if D <= 3 else 5)
    order = objs[:]
    ops_n = 2 if D <= 2 else (3 if D <= 4 else 4)
    ops = []
    for _ in range(ops_n):
        o = r.choice(order)
        op = r.choice(['Bring to Front', 'Send to Back', 'Bring Forward', 'Send Backward'])
        i = order.index(o)
        order.pop(i)
        if op == 'Bring to Front':
            order.insert(0, o)
        elif op == 'Send to Back':
            order.append(o)
        elif op == 'Bring Forward':
            order.insert(max(0, i - 1), o)
        else:
            order.insert(min(len(order), i + 1), o)
        ops.append(f'{op} on {o}')
    stem = (f'A vector graphic has these overlapping objects, listed from front (top) to back: {", ".join(objs)}. The designer then applies, in order: ' + '; '.join(ops) +
            '. (Bring Forward / Send Backward move an object one place.) State the new order from front to back.')
    if D == 1:
        return MCQ(r, stem.replace('State the new order', 'Which object is now at the front?').replace('from front to back.', ''), order[0], [x for x in objs if x != order[0]], 'Final order: ' + ', '.join(order))
    m = 2 if D <= 3 else 3
    return Q(stem, ', '.join(order), f'Final order front to back: {", ".join(order)} (lose 1 mark per object out of place). [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4), 'numerical')
def g12_scale(r, D):
    w = r.choice([40, 60, 80, 120, 150])
    h = r.choice([20, 30, 45, 60, 90])
    nw = r.choice([w * 2, int(w * 1.5), int(w * 0.75), w // 2, w + 30])
    nh = h * nw / w
    sh = r.choice(['rectangle', 'logo group', 'ellipse', 'banner'])
    stem = f'A vector {sh} is {w} mm wide and {h} mm high. With the aspect ratio locked, its width is changed to {nw} mm. Calculate the new height and the percentage scale factor.'
    key = f'height = {h} × {nw}/{w} = {num(round(nh, 2))} mm [1]; scale = {nw}/{w} × 100 = {num(round(nw / w * 100, 1))}% [1]'
    m = 2
    ans = f'{num(round(nh, 2))} mm; {num(round(nw / w * 100, 1))}%'
    if D >= 4:
        stem += ' Explain why the file size of the vector graphic hardly changes.'
        key += '; vector stores shape properties, not pixels, so only numbers change [1]'
        ans += '; only the stored dimensions change, not the number of pixels.'
        m = 3
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(5, 'Bitmap editing: cropping, resizing, colour adjustment, masking and filters', 'bitmap editing', 'cropping, resizing, colour adjustment', 'masking and filters',
      defs=[('cropping', 'Removing unwanted outer parts of an image to improve its composition or change its shape.'),
            ('resizing (resampling)', 'Changing the number of pixels in an image, which changes its dimensions and file size.'),
            ('mask', 'A layer that hides or reveals parts of an image without permanently deleting pixels, so edits can be applied to selected areas.'),
            ('filter', 'An effect applied to a bitmap that changes pixel values, such as blur, sharpen or sepia.'),
            ('aspect ratio', 'The ratio of an image\'s width to its height.')],
      mcqs=[('Which edit removes unwanted parts around the edges of a photograph?', 'Cropping', ['Masking', 'Grouping', 'Tweening'], 'Cropping cuts the outer area.'),
            ('Why is a mask better than deleting part of an image?', 'Hidden pixels can be revealed again later, so the edit is non-destructive', ['It makes the file smaller', 'It converts the image to a vector', 'It increases the resolution'], 'Masks hide rather than delete.'),
            ('What usually happens when a small bitmap is enlarged to twice its width and height?', 'It becomes blurred or pixelated', ['It becomes sharper', 'It becomes a vector', 'Its file size halves'], 'New pixels are estimated from existing ones.')],
      exps=[('Explain why maintaining the aspect ratio is important when resizing a photograph.', 'Changing width and height by different factors stretches or squashes the subject, making it look distorted.', '1 mark proportions kept; 1 mark distortion otherwise. [2]'),
            ('Explain how adjusting brightness and contrast can improve a photograph.', 'Brightness makes the whole image lighter or darker to correct exposure; contrast increases the difference between light and dark areas so details stand out.', '1 mark brightness; 1 mark contrast. [2]')],
      ars=[('Cropping a bitmap reduces its file size.', 'Fewer pixels are stored.'),
           ('Enlarging a bitmap can cause pixelation.', 'The software must create pixels that were not in the original.')],
      falses=['Cropping increases the number of pixels in an image.', 'A mask permanently deletes pixels.'],
      intros=['{p} is preparing photographs of staff and products for the website of {org} in {city}.',
              '{org} in {city} is producing a printed brochure from photographs taken by its staff.'],
      parts=[('Explain why the photographs should be cropped.', 'Remove distracting background; focus on subject; fit layout shape.', '1 mark per point, max 2. [2]'),
             ('Explain why the images should be resized before use on the website.', 'Smaller dimensions and files load faster; match the space on the page.', '1 mark each. [2]'),
             ('Describe how a mask could be used.', 'Hide the background or apply an effect to only part of the image without deleting pixels.', '1 mark hide/select; 1 mark non-destructive. [2]'),
             ('Describe two filters that could be applied.', 'Sharpen; blur; sepia/greyscale; noise reduction; vignette.', '1 mark each, max 2. [2]')],
      ev=[('the use of photo editing to alter images used by {org} in its advertising', 'improves quality and consistency; removes distractions; attracts customers.', 'heavy editing can mislead customers; ethical and legal concerns; time and skill needed.', 'moderate editing for quality is acceptable; edits that misrepresent products should be avoided.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_crop(r, D):
    w, h = r.choice([(4000, 3000), (3000, 2000), (2400, 1600), (1920, 1080), (1600, 1200)])
    cd = 24
    if D == 1:
        nw = w // 2
        return MCQ(r, f'A photo is {w} × {h} pixels. It is resized to {nw} pixels wide with the aspect ratio locked. What is the new height?', f'{h * nw // w} pixels',
                   [f'{h} pixels', f'{h // 4} pixels', f'{h * 2} pixels'], f'{h} × {nw}/{w} = {h * nw // w}.')
    cl, cr = r.choice([0, 200, 400]), r.choice([0, 200, 500])
    ct, cb = r.choice([0, 100, 300]), r.choice([0, 100, 200])
    cw, ch = w - cl - cr, h - ct - cb
    s0, s1 = w * h * 3, cw * ch * 3
    stem = (f'A 24-bit photograph is {w} × {h} pixels. It is cropped by removing {cl} pixels from the left, {cr} from the right, {ct} from the top and {cb} from the bottom. '
            f'Calculate the new dimensions and the uncompressed file size before and after cropping, in MB (1 MB = 1 000 000 bytes).')
    key = f'new size {cw} × {ch} [1]; before {w} × {h} × 3 = {s0:,} bytes = {num(round(s0 / 1e6, 2))} MB [1]; after {cw} × {ch} × 3 = {s1:,} bytes = {num(round(s1 / 1e6, 2))} MB [1]'
    ans = f'{cw} × {ch} pixels; {num(round(s0 / 1e6, 2))} MB before, {num(round(s1 / 1e6, 2))} MB after'
    m = 3
    if D >= 4:
        nw = r.choice([800, 1000, 1200])
        nh = ch * nw / cw
        stem += f' The cropped image is then resized to {nw} pixels wide with the aspect ratio locked. Calculate the new height to the nearest pixel.'
        key += f'; height = {ch} × {nw}/{cw} = {nh:.1f} → {round(nh)} pixels [1]'
        ans += f'; resized height {round(nh)} pixels'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 6 Animation
t = T(6, 'Principles of animation: frames, keyframes, tweening and frame rate', 'principles of animation', 'frames, keyframes, tweening and frame rate',
      defs=[('frame', 'A single still image in an animation; frames shown quickly one after another create the illusion of movement.'),
            ('keyframe', 'A frame in which the animator sets the position or properties of an object; frames between keyframes can be generated automatically.'),
            ('tweening', 'Automatically generating the in-between frames from one keyframe to the next, changing position, size, rotation, colour or shape gradually.'),
            ('frame rate', 'The number of frames shown per second (fps); a higher frame rate gives smoother movement.'),
            ('onion skinning', 'A feature that shows faint images of the previous and next frames so the animator can position objects accurately.')],
      mcqs=[('An animation runs at 24 fps and lasts 5 seconds. How many frames does it have?', '120', ['29', '24', '480'], '24 × 5 = 120.'),
            ('What is the main advantage of tweening?', 'The software creates the in-between frames, saving the animator time', ['It reduces the frame rate', 'It removes the need for keyframes', 'It converts vectors to bitmaps'], 'Only keyframes must be drawn.'),
            ('Why does an animation at 4 fps look jerky?', 'Too few frames are shown each second for smooth motion', ['The frames are too large', 'The animation uses keyframes', 'It has too many layers'], 'Higher frame rates appear smoother.')],
      exps=[('Explain the difference between a motion tween and a shape tween.', 'A motion tween moves or transforms an object (position, scale, rotation) between keyframes while keeping its shape; a shape tween morphs one shape into another.', '1 mark motion tween; 1 mark shape tween. [2]'),
            ('Explain why a higher frame rate increases the file size of an animation.', 'More frames must be stored for each second of animation, so there is more data.', '1 mark more frames per second; 1 mark more data stored. [2]')],
      ars=[('Tweening reduces the work of an animator.', 'In-between frames are generated automatically from keyframes.'),
           ('A higher frame rate gives smoother motion.', 'Smaller changes are shown between each displayed frame.')],
      falses=['Keyframes are created automatically by tweening.', 'Reducing the frame rate makes animation smoother.'],
      intros=['{p} is creating a 30-second animated advert for {org} in {city}.',
              'Students at {org} in {city} are learning to produce short animations.'],
      parts=[('Explain what is meant by a keyframe.', 'A frame where the animator defines an object\'s position/properties; tweens fill between keyframes.', '1 mark each part. [2]'),
             ('Explain how tweening is used.', 'Software calculates in-between frames between two keyframes, gradually changing properties.', '1 mark each part. [2]'),
             ('Explain the effect of choosing a frame rate of 12 fps rather than 30 fps.', 'Fewer frames: smaller file and less work, but jerkier motion.', '1 mark size/work; 1 mark smoothness. [2]'),
             ('Describe what onion skinning shows.', 'Faint images of neighbouring frames to help position objects.', '1 mark each part. [2]')],
      ev=[('the use of tweening rather than drawing every frame by hand for the animations of {org}', 'much faster; smooth, accurate motion; easy to change keyframes.', 'motion can look mechanical; complex character movement may still need frame-by-frame work; less artistic control.', 'tweening suits most commercial animation, with frame-by-frame work for detailed character movement.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_tween(r, D):
    fps = r.choice([12, 24, 25, 30])
    k1 = 1
    k2 = r.choice([11, 21, 25, 31, 41])
    prop = r.choice(['x', 'rot', 'opacity'])
    if prop == 'x':
        a, b = r.choice([0, 50, 100]), r.choice([300, 400, 500, 600])
        unit, what = 'px', 'x-coordinate'
    elif prop == 'rot':
        a, b = 0, r.choice([90, 180, 360, 720])
        unit, what = '°', 'rotation'
    else:
        a, b = 100, r.choice([0, 20, 40])
        unit, what = '%', 'opacity'
    f = r.randrange(k1 + 1, k2)
    v = a + (b - a) * (f - k1) / (k2 - k1)
    secs = (k2 - k1) / fps
    obj = r.choice(['a car', 'a logo', 'a ball', 'a bird', 'a cloud'])
    stem = f'In an animation at {fps} fps, {obj} has {'an' if what[0] in 'aeiouxAEIOUX' else 'a'} {what} of {a}{unit} at keyframe {k1} and {b}{unit} at keyframe {k2}, with a linear motion tween between them.'
    if D == 1:
        return MCQ(r, stem + f' How long, in seconds, does the tween last?', f'{num(round(secs, 3))} s', [f'{num(round(k2 / fps, 3))} s', f'{num(round(secs * 2, 3))} s', f'{k2 - k1} s'], f'({k2} − {k1}) ÷ {fps} = {num(round(secs, 3))} s.')
    stem += f' Calculate the {what} at frame {f}.'
    key = f'change per frame = ({b} − {a}) / ({k2} − {k1}) = {num(round((b - a) / (k2 - k1), 3))} [1]; at frame {f}: {a} + {f - k1} × {num(round((b - a) / (k2 - k1), 3))} = {num(round(v, 2))}{unit} [1]'
    ans = f'{num(round(v, 2))}{unit}'
    m = 2
    if D >= 3:
        stem += ' Also calculate how long the tween lasts in seconds.'
        key += f'; ({k2} − {k1}) ÷ {fps} = {num(round(secs, 3))} s [1]'
        ans += f'; {num(round(secs, 3))} s'
        m = 3
    if D >= 4:
        nf = r.choice([x for x in (12, 24, 30, 60) if x != fps])
        stem += f' If the frame rate is changed to {nf} fps and the tween must last the same time, how many frames will it span?'
        key += f'; {num(round(secs, 3))} × {nf} = {num(round(secs * nf, 2))} frames [1]'
        ans += f'; {num(round(secs * nf, 2))} frames at {nf} fps'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(6, 'Creating vector animations with motion paths, layers and timelines', 'creating vector animations', 'motion paths, layers and timelines',
      defs=[('timeline', 'The part of animation software that shows frames in order for each layer, where keyframes and tweens are placed.'),
            ('motion path', 'A line or curve drawn so that an animated object follows it during a tween.'),
            ('easing', 'Changing the speed of a tween so that movement starts or ends gradually instead of at a constant speed.'),
            ('animation layer', 'A separate track on the timeline holding one object or group, so it can be animated independently of others.')],
      mcqs=[('Why is each moving object usually placed on its own layer?', 'So each can be animated and edited independently on the timeline', ['To reduce the frame rate', 'To convert objects to bitmaps', 'To make them invisible'], 'Separate layers avoid tweening conflicts.'),
            ('What does an "ease out" setting do to a tween?', 'The object slows down towards the end of the movement', ['The object speeds up at the end', 'The object disappears', 'The tween becomes a shape tween'], 'Easing changes acceleration.'),
            ('How can a ball be made to follow a curved route?', 'Attach it to a motion path drawn as a curve', ['Increase the frame rate', 'Add a mask', 'Group it with the background'], 'Motion path guides the tween.')],
      exps=[('Explain why easing makes animation look more realistic.', 'Real objects speed up and slow down rather than moving at constant speed; easing changes the spacing between frames to imitate this.', '1 mark real motion accelerates/decelerates; 1 mark easing imitates. [2]'),
            ('Explain how a motion path is used in a vector animation.', 'A path is drawn on a guide layer; the object on the tween is snapped to the path, so in-between frames place it along the curve.', '1 mark path drawn; 1 mark object follows during tween. [2]')],
      ars=[('Separate layers let objects be animated independently.', 'Each layer has its own keyframes on the timeline.'),
           ('Easing can make an object appear to slow down.', 'The distance moved between frames is reduced.')],
      falses=['A motion path changes the colour of an object.', 'All objects must be on one layer to be animated.'],
      intros=['{p} is animating a logo reveal for {org} in {city}.',
              '{org} in {city} wants an animated banner for its website.'],
      parts=[('Explain why the timeline is important when creating the animation.', 'Shows frames and keyframes for each layer; controls timing and order of events.', '1 mark per point, max 2. [2]'),
             ('Describe how a motion path would be used.', 'Draw the path; attach the object; tween follows path between keyframes.', '1 mark per point, max 2. [2]'),
             ('Explain how layers would be organised.', 'Background, each moving object and text on separate layers; lock/hide layers.', '1 mark per point, max 2. [2]')],
      ev=[('the use of vector animation rather than video for the web banner of {org}', 'small file sizes; scalable; easy to edit.', 'less realistic; complex scenes are hard; browser support issues for some formats.', 'vector animation suits logos and banners; video suits real-world footage.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_timeline(r, D):
    fps = r.choice([10, 12, 24, 25])
    total = r.choice([3, 4, 5, 6]) * fps
    objs = r.sample(['Logo', 'Title', 'Car', 'Sun', 'Button', 'Slogan', 'Star'], 3 if D <= 3 else 4)
    spans = []
    for o in objs:
        a = r.randrange(1, total // 2)
        b = r.randrange(a + fps // 2, total + 1)
        spans.append((o, a, b))
    tsec = round(r.uniform(0.2, total / fps - 0.1), 1)
    frame = int(tsec * fps) + 1
    vis = [o for o, a, b in spans if a <= frame <= b]
    lines = [f'Layer "{o}": visible from frame {a} to frame {b}' for o, a, b in spans]
    stem = f'An animation runs at {fps} fps and has {total} frames. The timeline shows:\n' + code(lines)
    if D == 1:
        return MCQ(r, stem + '\nHow long does the animation last?', f'{num(total / fps)} seconds', [f'{total} seconds', f'{num(total / fps * 2)} seconds', f'{num(round(fps / total, 2))} seconds'], f'{total} ÷ {fps} = {num(total / fps)} s.')
    stem += f'\nFrame 1 is shown at time 0 s. State which objects are visible at time {tsec} s.'
    key = f'frame = {tsec} × {fps} + 1 = {frame} (whole frames) [1]; visible: {", ".join(vis) or "none"} [1]'
    ans = f'frame {frame}: ' + (', '.join(vis) or 'none')
    m = 2
    if D >= 4:
        o, a, b = r.choice(spans)
        stem += f' Also calculate for how many seconds "{o}" is visible.'
        key += f'; {o}: {b} − {a} + 1 = {b - a + 1} frames ÷ {fps} = {num(round((b - a + 1) / fps, 2))} s [1]'
        ans += f'; {o} is visible for {num(round((b - a + 1) / fps, 2))} s'
        m = 3
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(6, 'Exporting animations and choosing formats for an audience', 'exporting animations', 'choosing formats for an audience',
      defs=[('animated GIF', 'A bitmap file format that stores several frames in one file, limited to 256 colours, often used for short looping web animations.'),
            ('MP4', 'A compressed video file format (usually H.264) widely supported on websites, phones and social media.'),
            ('HTML5 animation', 'Animation created with HTML, CSS and JavaScript (or SVG) that runs in a web browser without plug-ins.')],
      mcqs=[('Which format is best for a short, looping, low-colour animated icon on a web page?', 'Animated GIF', ['WAV', 'TIFF', 'DOCX'], 'GIFs loop and are widely supported.'),
            ('Why might an animator export to MP4 rather than GIF?', 'MP4 supports millions of colours and better compression for long animations', ['MP4 cannot be compressed', 'GIF supports more colours', 'MP4 files cannot be played on phones'], 'GIF is limited to 256 colours.')],
      exps=[('Explain two factors an animator should consider when choosing an export format.', 'Where it will be shown (web, social media, TV) and device support; file size and download speed; colour and quality needed; whether interactivity or transparency is required.', '2 × (1 mark factor, 1 mark explanation). [4]')],
      ars=[('Animated GIFs can look grainy for photographic content.', 'GIF is limited to 256 colours.'),
           ('HTML5 animations run in modern browsers without plug-ins.', 'They use HTML, CSS, JavaScript or SVG.')],
      falses=['GIF supports millions of colours.', 'MP4 files cannot be compressed.'],
      intros=['{org} in {city} needs its animated advert in formats for its website, social media and a cinema screen.',
              '{p} is exporting a short animation made for {org} in {city}.'],
      parts=[('Recommend a format for social media and justify your choice.', 'MP4: widely supported, good compression, full colour.', '1 mark format; 1 mark justification. [2]'),
             ('Explain why an animated GIF might not be suitable.', '256-colour limit; large files for long animations; no sound.', '1 mark per point, max 2. [2]'),
             ('Explain why the audience\'s devices should be considered.', 'Formats and resolutions must be supported and load quickly on phones or slow connections.', '1 mark support; 1 mark speed/size. [2]')],
      ev=[('the choice of export format for the animations of {org}', 'MP4 gives quality and small size; GIF loops simply; HTML5 is interactive and scalable.', 'one format rarely suits every platform; compression reduces quality; older devices may not support some formats.', 'export several versions matched to each platform and audience.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def g12_gif(r, D):
    w, h = r.choice([(200, 200), (320, 240), (400, 300), (480, 270)])
    frames = r.choice([10, 12, 20, 24, 30])
    ratio = r.choice([2, 3, 4])
    fb = w * h * 1
    tot = fb * frames / ratio
    if D == 1:
        return MCQ(r, f'An animated GIF uses 8 bits per pixel. How many bytes does one uncompressed {w} × {h} frame need?', f'{fb:,}', [f'{fb * 8:,}', f'{fb * 3:,}', f'{fb // 8:,}'], f'{w} × {h} × 8 ÷ 8 = {fb:,} bytes.')
    stem = f'An animated GIF is {w} × {h} pixels with 8 bits per pixel and {frames} frames. Compression reduces the data to one {["", "", "half", "third", "quarter"][ratio]} of its original size. Calculate the file size in KB (1 KB = 1000 bytes).'
    key = f'one frame {w} × {h} × 1 byte = {fb:,} bytes [1]; × {frames} = {fb * frames:,} bytes [1]; ÷ {ratio} = {tot:,.0f} bytes = {num(round(tot / 1000, 1))} KB [1]'
    m = 3
    return Q(stem, f'{num(round(tot / 1000, 1))} KB', key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 7 Mail merge
SURN = ['Okafor', 'Silva', 'Tanaka', 'Haddad', 'Novak', 'Mensah', 'Reyes', 'Kowalski', 'Lindqvist', 'Patel', 'Moreau', 'Nguyen', 'Costa', 'Ivanova', 'Bakr', 'Hughes']
MCITIES = ['Lima', 'Nairobi', 'Doha', 'Lisbon', 'Manila']

t = T(7, 'Master documents, data sources and merge fields', 'master documents, data sources', 'merge fields',
      defs=[('mail merge', 'Combining a master document with records from a data source to produce many personalised documents automatically.'),
            ('master document', 'The document containing the fixed text and the merge fields that will be replaced by data from each record.'),
            ('data source', 'The file, such as a spreadsheet, database table or contacts list, that holds the records used in a mail merge.'),
            ('merge field', 'A placeholder in the master document, such as «FirstName», that is replaced by the matching field value from each record.')],
      mcqs=[('What replaces a merge field during a mail merge?', 'The value from the matching field of each record', ['The name of the data source file', 'A random value', 'The same text for every letter'], 'Each merged document uses one record.'),
            ('Which is the best data source for a mail merge to 2000 club members?', 'A database table or spreadsheet with one row per member', ['A scanned photograph', 'A paper list', 'A video file'], 'Structured records are needed.'),
            ('Why must field names in the data source be consistent?', 'So each merge field can be matched to the correct column of data', ['So the letter prints in colour', 'To encrypt the data', 'To make the file smaller'], 'Fields map by name.')],
      exps=[('Explain two advantages of mail merge over writing letters individually.', 'Hundreds of personalised letters are produced quickly from one master; fewer errors because data is copied automatically; easy to update and re-run; consistent layout.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why the data source should be checked before a mail merge is run.', 'Errors, missing values or duplicates in the data will appear in every affected letter, wasting paper/postage and looking unprofessional.', '1 mark errors copied to output; 1 mark consequence. [2]')],
      ars=[('Mail merge saves time when sending many personalised letters.', 'One master document is combined automatically with every record.'),
           ('A merge field is replaced by data from the data source.', 'Each output document uses the values of one record.')],
      falses=['The master document contains every customer\'s address typed in by hand.', 'A data source must be a scanned image.'],
      intros=['{org} in {city} sends a personalised letter to each of its 3000 customers every month.',
              '{p} is setting up a mail merge at {org} in {city} to invite members to an event.'],
      parts=[('Describe what is meant by the master document.', 'Fixed text plus merge fields used for every output document.', '1 mark each part. [2]'),
             ('Identify three merge fields that could be used.', 'Title, FirstName, Surname, Address lines, City, MembershipNumber, Balance.', '1 mark each, max 3. [3]'),
             ('Describe the steps to carry out the mail merge.', 'Create/choose master; select data source; insert merge fields; preview; filter/sort if needed; complete merge to printer/email/new document.', '1 mark per step, max 4. [4]'),
             ('Explain one problem that could occur.', 'Missing or incorrect data gives wrong letters; wrong field mapping; blank lines from empty fields.', '1 mark problem; 1 mark explanation. [2]')],
      ev=[('the use of mail merge by {org} to communicate with its customers', 'fast and personalised; consistent; fewer errors; easy to target groups.', 'errors in data affect many letters; impersonal if overused; data protection issues; set-up time.', 'mail merge is highly efficient if data is accurate and messages are relevant.')])


def mm_rows(r, n):
    rows = []
    for s in r.sample(SURN, n):
        rows.append({'Title': r.choice(['Mr', 'Ms', 'Dr', 'Mrs']), 'Surname': s, 'City': r.choice(MCITIES), 'Points': r.randrange(50, 1500, 10), 'Member': r.choice(['Yes', 'No'])})
    return rows


@t.add('C3', (1, 2, 3, 4), 'numerical')
def g12_merge(r, D):
    rows = mm_rows(r, 5)
    rec = r.choice(rows)
    d = ctx(r)
    master = f'Dear «Title» «Surname», thank you for shopping at {d["org"]} in «City». You have «Points» loyalty points.'
    out = f'Dear {rec["Title"]} {rec["Surname"]}, thank you for shopping at {d["org"]} in {rec["City"]}. You have {rec["Points"]} loyalty points.'
    table = tbl(['Title', 'Surname', 'City', 'Points', 'Member'], [[x[k] for k in ('Title', 'Surname', 'City', 'Points', 'Member')] for x in rows])
    if D == 1:
        return MCQ(r, f'The master document contains: {master} Data source:\n{table}\nHow many letters are produced if no filter is applied?', '5', ['1', '4', '6', '25'], 'One document per record: 5.')
    stem = f'The master document contains: {master}\nData source:\n{table}\nWrite out the merged text for {rec["Surname"]}.'
    m = 2
    key = f'{out} (1 mark correct fields substituted; 1 mark fixed text unchanged). [2]'
    if D >= 3:
        stem += ' State how many merged letters are produced and identify the merge fields used.'
        key = f'{out} [2]; 5 letters (one per record) [1]; fields Title, Surname, City, Points [1]. [4]'
        m = 4
        out += ' 5 letters; fields «Title», «Surname», «City», «Points».'
    return Q(stem, out, key, marks=m, typ='numerical')


t = T(7, 'Filtering, sorting and conditional (IF) fields in a mail merge', 'filtering, sorting and conditional (if) fields', 'mail merge',
      defs=[('filter (in mail merge)', 'Criteria that select which records from the data source are merged, so only matching recipients receive a document.'),
            ('sorting (in mail merge)', 'Putting the merged records in a chosen order, such as by postcode or surname, before the documents are produced.'),
            ('conditional (IF) field', 'A field that inserts different text depending on whether a condition about the record\'s data is true, e.g. IF Points > 1000 "Gold" "Silver".'),
            ('SKIPRECORD IF', 'A merge rule that leaves out the current record when a condition is true.')],
      mcqs=[('Why would letters be sorted by postcode before printing?', 'Postal services may offer discounts for pre-sorted mail and delivery is faster', ['To make each letter different', 'To delete duplicate fields', 'To encrypt addresses'], 'Sorted mail is cheaper/easier to deliver.'),
            ('What does a conditional IF field allow in a mail merge?', 'Different text to appear depending on the values in each record', ['All letters to be identical', 'The data source to be deleted', 'Images to be compressed'], 'Personalised wording.')],
      exps=[('Explain why a filter is used in a mail merge.', 'So only relevant recipients receive the document, e.g. customers in one city, saving printing/postage and avoiding irrelevant messages.', '1 mark selects records; 1 mark benefit. [2]'),
            ('Explain the advantage of using an IF field rather than two separate master documents.', 'One master document handles both cases automatically, so there is less to maintain and no risk of merging the wrong group with the wrong letter.', '1 mark one master; 1 mark fewer errors/less maintenance. [2]')],
      ars=[('A filter can limit a mail merge to members only.', 'Only records that meet the criteria are merged.'),
           ('An IF field can change the wording of individual letters.', 'Its output depends on the data in each record.')],
      falses=['Sorting removes records from the merge.', 'An IF field must give the same text in every letter.'],
      intros=['{org} in {city} wants to send different offers to members and non-members.',
              '{p} is preparing a targeted mailing for {org} in {city}.'],
      parts=[('Explain how a filter would be used in this mailing.', 'Set criteria (e.g. Member = Yes, City = X) so only matching records are merged.', '1 mark criteria; 1 mark only matching records. [2]'),
             ('Write a conditional field that prints "Gold member" if Points is over 1000 and "Member" otherwise.', '{IF {MERGEFIELD Points} > 1000 "Gold member" "Member"}', '1 mark condition; 1 mark both texts. [2]'),
             ('Explain why the records might be sorted before merging.', 'Postal discounts, easier distribution, or alphabetical output for filing.', '1 mark reason; 1 mark explanation. [2]')],
      ev=[('the use of filters and IF fields to personalise mailings from {org}', 'relevant messages; better response; fewer wasted letters.', 'complex rules can contain errors; relies on accurate data; customers may feel profiled.', 'well-tested filters and IF fields improve targeting; rules must be checked with test merges.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_filter(r, D):
    n = 6 if D <= 3 else 8
    rows = mm_rows(r, n)
    city = r.choice([x['City'] for x in rows])
    thr = r.choice([500, 800, 1000])
    crit = r.choice(['city', 'member', 'both']) if D >= 3 else r.choice(['city', 'member'])
    if crit == 'city':
        sel = [x for x in rows if x['City'] == city]
        ctext = f'City = "{city}"'
    elif crit == 'member':
        sel = [x for x in rows if x['Member'] == 'Yes']
        ctext = 'Member = "Yes"'
    else:
        sel = [x for x in rows if x['Member'] == 'Yes' or x['Points'] > thr]
        ctext = f'Member = "Yes" OR Points > {thr}'
    sel = sorted(sel, key=lambda x: x['Surname'])
    table = tbl(['Title', 'Surname', 'City', 'Points', 'Member'], [[x[k] for k in ('Title', 'Surname', 'City', 'Points', 'Member')] for x in rows])
    if D == 1:
        k = len(sel)
        return MCQ(r, f'Data source:\n{table}\nA mail merge uses the filter {ctext}. How many letters are produced?', str(k), [str(x) for x in (k + 1, k + 2, max(0, k - 1), n) if x != k], f'Matching: {", ".join(x["Surname"] for x in sel) or "none"}.')
    iff = f'{{IF {{MERGEFIELD Points}} > {thr} "You have earned a free gift." "Collect more points for a free gift."}}'
    stem = f'Data source:\n{table}\nA mail merge uses the filter {ctext} and sorts by Surname in ascending order.'
    ans = 'Letters in order: ' + (', '.join(x['Surname'] for x in sel) or 'none')
    m = 2
    key = f'{ans} [1 mark correct records, 1 mark correct order]'
    if D >= 3:
        stem += f' The letter also contains the field {iff}. State the order of the letters produced and the sentence printed by the IF field in each.'
        iftxt = '; '.join(f'{x["Surname"]}: {"You have earned a free gift." if x["Points"] > thr else "Collect more points for a free gift."}' for x in sel)
        ans += '; ' + (iftxt or 'no letters')
        m = 2 + max(1, min(3, len(sel)))
        key += f'; IF output: {iftxt or "none"} [{m - 2}]'
    else:
        stem += ' State the surnames on the letters, in the order they are produced.'
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(7, 'Mail merge for letters, labels and emails; automated document production', 'mail merge for letters, labels and emails', 'automated document production',
      defs=[('label merge', 'A mail merge that places records onto a sheet of labels, with several records on each page, e.g. for addressing envelopes.'),
            ('email merge', 'A mail merge that sends a personalised email to each record, using an email address field.'),
            ('automated document production', 'Generating many documents automatically from templates and data, such as invoices, certificates or contracts.')],
      mcqs=[('Which field must the data source contain for an email merge?', 'Email address', ['Fax number', 'Date of birth', 'Shoe size'], 'Each message needs a recipient address.'),
            ('In a label merge, what does «Next Record» do?', 'Moves to the next record so each label shows a different address', ['Prints a blank label', 'Deletes the record', 'Sorts the data'], 'Without it, each label repeats the same record.')],
      exps=[('Explain one advantage of an email merge over a printed letter merge.', 'No printing or postage costs and messages arrive immediately; links can be included and responses tracked.', '1 mark cost/speed; 1 mark explanation. [2]'),
            ('Explain why the label size must be set correctly before a label merge.', 'Otherwise addresses will not line up with the labels on the sheet, so text is cut off or printed across two labels, wasting sheets.', '1 mark alignment; 1 mark consequence. [2]')],
      ars=[('Label merges place several records on one page.', 'A sheet of labels holds many labels arranged in rows and columns.'),
           ('Email merges need an email address field.', 'Each message is sent to the address in its record.')],
      falses=['An email merge requires a printer.', 'Label merges can only print one label per sheet.'],
      intros=['{org} in {city} sends invoices, address labels and newsletters to customers every month.',
              '{p} is automating the production of letters, labels, emails and certificates at {org} in {city}.'],
      parts=[('Describe how a label merge is set up.', 'Choose label type/size; select data source; insert address fields in first label; update all labels; merge.', '1 mark per step, max 3. [3]'),
             ('Explain one advantage and one disadvantage of an email merge.', 'Cheap and fast; but may go to spam, addresses may be wrong, data protection rules.', '1 mark each. [2]'),
             ('Describe how certificates could be produced automatically.', 'Template with fields for name, course, date; data source of results; merge to PDF/print.', '1 mark per point, max 3. [3]')],
      ev=[('the benefits for {org} of automating document production', 'saves staff time; consistent; fewer errors; scalable.', 'set-up cost; errors repeated across many documents; less personal; staff need skills.', 'automation is strongly beneficial for repetitive documents if data and templates are checked.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_labels(r, D):
    cols = r.choice([2, 3])
    rws = r.choice([7, 8, 10])
    per = cols * rws
    recs = r.choice([150, 230, 365, 480, 1000])
    sheets = math.ceil(recs / per)
    left = sheets * per - recs
    if D == 1:
        return MCQ(r, f'A label sheet has {cols} columns and {rws} rows of labels. How many labels are on one sheet?', str(per), [str(cols + rws), str(per * 2), str(per - cols)], f'{cols} × {rws} = {per}.')
    stem = f'Address labels are printed on sheets with {cols} columns and {rws} rows. {ctx(r)["org"]} has {recs} customer records. Calculate the number of sheets needed and the number of unused labels on the last sheet.'
    key = f'{cols} × {rws} = {per} per sheet [1]; {recs} ÷ {per} = {recs / per:.2f} → {sheets} sheets [1]; unused {sheets} × {per} − {recs} = {left} [1]'
    ans = f'{sheets} sheets; {left} unused labels'
    m = 3
    if D >= 4:
        W = 210
        lm = r.choice([5, 7, 10])
        gap = r.choice([2, 3, 5])
        lw = (W - 2 * lm - (cols - 1) * gap) / cols
        stem += f' The A4 sheet is 210 mm wide with {lm} mm side margins and a {gap} mm gap between columns. Calculate the width of each label.'
        key += f'; (210 − 2 × {lm} − {cols - 1} × {gap}) ÷ {cols} = {num(round(lw, 2))} mm [1]'
        ans += f'; label width {num(round(lw, 2))} mm'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 8 Programming for the web
t = T(8, 'HTML structure and CSS styling of web pages', 'html structure and css styling', 'html', 'css',
      defs=[('HTML', 'HyperText Markup Language: the language of tags used to define the structure and content of a web page.'),
            ('CSS', 'Cascading Style Sheets: a language used to define the presentation of web pages, such as colours, fonts, spacing and layout.'),
            ('external style sheet', 'A separate .css file linked to many web pages so that they all share the same styles and can be restyled by changing one file.'),
            ('class selector', 'A CSS selector beginning with a full stop (e.g. .warning) that applies styles to every element with that class attribute.'),
            ('id selector', 'A CSS selector beginning with # (e.g. #header) that applies styles to the single element with that id.')],
      mcqs=[('Which tag creates a hyperlink?', '<a href="page.html">', ['<link src="page.html">', '<href a="page.html">', '<p link="page.html">'], 'The anchor tag with href creates a link.'),
            ('Why is the alt attribute added to <img> tags?', 'To provide text for screen readers and when the image cannot load', ['To make the image larger', 'To link to another page', 'To change the image format'], 'Accessibility and fallback.'),
            ('Which CSS rule makes all <h1> headings blue?', 'h1 { color: blue; }', ['#h1 { colour: blue }', '.h1 = blue;', '<h1 color="blue">'], 'Element selector with the color property.'),
            ('Which part of an HTML document contains the <title> element?', 'The <head> section', ['The <body> section', 'The <footer> element', 'An <li> element'], 'Metadata belongs in the head.')],
      exps=[('Explain why an external style sheet is preferred for a large website.', 'All pages link to one file, so the look of every page is consistent and can be changed by editing one file; pages download faster because the CSS is cached.', '1 mark consistency; 1 mark single place to change; 1 mark caching/smaller pages. [3]'),
            ('Explain the difference between a class selector and an id selector.', 'A class can be applied to many elements and is written .name; an id identifies one unique element and is written #name, and has higher specificity.', '1 mark class many/.; 1 mark id unique/#. [2]'),
            ('Explain why HTML and CSS are kept separate.', 'HTML defines structure and content while CSS defines presentation, so content can be restyled without editing it, and styles can be reused across pages.', '1 mark separation of structure and style; 1 mark benefit. [2]')],
      ars=[('An id should be used only once on a page.', 'It identifies a single, unique element.'),
           ('An external style sheet makes a website consistent.', 'Every page uses the same style rules.'),
           ('Alt text improves accessibility.', 'Screen readers read it aloud to blind users.')],
      falses=['CSS defines the structure of a web page.', 'A class selector starts with #.', 'The <title> element is placed inside <body>.'],
      intros=['{p} is building a website for {org} in {city} using HTML and CSS.',
              '{org} in {city} wants its 40-page website to have a consistent style.'],
      parts=[('Describe the purpose of the <head> and <body> sections of an HTML page.', 'Head: metadata, title, links to CSS/scripts. Body: visible content.', '1 mark each. [2]'),
             ('Write the HTML to display an image logo.png with suitable alternative text.', '<img src="logo.png" alt="Company logo">', '1 mark img/src; 1 mark alt. [2]'),
             ('Write a CSS rule that gives all paragraphs Arial font, size 14px and dark grey text.', 'p { font-family: Arial; font-size: 14px; color: #333333; }', '1 mark selector; 1 mark properties; 1 mark syntax. [3]'),
             ('Explain why an external style sheet should be used.', 'Consistent look; change all pages from one file; caching.', '1 mark per point, max 2. [2]')],
      ev=[('the use of a single external style sheet for the whole website of {org}', 'consistency; easy updates; smaller pages; caching.', 'one error affects every page; some pages need special styles; inline overrides can cause confusion.', 'an external style sheet is best practice, with page-specific rules kept to a minimum.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_box(r, D):
    w = r.choice([200, 250, 300, 400, 500])
    p = r.choice([5, 10, 15, 20])
    b = r.choice([1, 2, 3, 5])
    mg = r.choice([0, 5, 10, 20])
    tot = w + 2 * p + 2 * b
    space = tot + 2 * mg
    css = f'.box {{ width: {w}px; padding: {p}px; border: {b}px solid black; margin: {mg}px; }}'
    if D == 1:
        return MCQ(r, f'With the default box model, what is the total visible width (content + padding + border) of an element styled by: {css}', f'{tot}px', [f'{w}px', f'{space}px', f'{w + p + b}px'], f'{w} + 2×{p} + 2×{b} = {tot}px.')
    stem = f'An element uses the CSS rule {css} (default content-box model). Calculate (a) the total width of the element including padding and border and (b) the horizontal space it takes up including margins.'
    key = f'(a) {w} + 2 × {p} + 2 × {b} = {tot}px [1] (b) {tot} + 2 × {mg} = {space}px [1]'
    ans = f'(a) {tot}px (b) {space}px'
    m = 2
    if D >= 3:
        n = r.choice([2, 3, 4])
        cont = r.choice([960, 1000, 1200])
        fit = cont // space
        stem += f' (c) How many of these boxes fit side by side in a container {cont}px wide?'
        key += f' (c) {cont} ÷ {space} = {cont / space:.2f} → {fit} [1]'
        ans += f' (c) {fit}'
        m = 3
    if D >= 5:
        stem += ' (d) State the total width if box-sizing: border-box is added, and explain the difference.'
        key += f' (d) {w}px; padding and border are included inside the stated width [1]'
        ans += f' (d) {w}px, because border-box includes padding and border in the width.'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C2', (2, 3, 4), 'mcq')
def g12_cascade(r, D):
    cols = r.sample(['red', 'blue', 'green', 'orange', 'purple', 'black'], 3)
    el = r.choice(['p', 'h2', 'li'])
    cls, idn = r.choice(['note', 'alert', 'highlight']), r.choice(['intro', 'main', 'first'])
    has_id, has_cls = r.choice([(True, True), (False, True), (True, False), (False, False)])
    attrs = (f' id="{idn}"' if has_id else '') + (f' class="{cls}"' if has_cls else '')
    css = f'{el} {{ color: {cols[0]}; }} .{cls} {{ color: {cols[1]}; }} #{idn} {{ color: {cols[2]}; }}'
    ans = cols[2] if has_id else (cols[1] if has_cls else cols[0])
    why = 'an id selector is more specific than a class or element selector' if has_id else ('a class selector is more specific than an element selector' if has_cls else 'only the element selector matches')
    return MCQ(r, f'A style sheet contains: {css} What colour is the text of <{el}{attrs}>Hello</{el}>?', ans, [c for c in cols if c != ans] + ['the browser default'], f'{ans}: {why}.')


HTMLERR = [('<p>Welcome to our <b>new shop</p></b>', 'Tags are closed in the wrong order (incorrect nesting)', '<p>Welcome to our <b>new shop</b></p>'),
           ('<img src="team.jpg">', 'The alt attribute is missing, so screen readers cannot describe the image', '<img src="team.jpg" alt="Our team">'),
           ('<a href=contact.html>Contact us</a', 'The closing tag is incomplete (missing >) and the attribute value should be in quotes', '<a href="contact.html">Contact us</a>'),
           ('<ul><li>Tea<li>Coffee</ul>', 'The <li> elements are not closed', '<ul><li>Tea</li><li>Coffee</li></ul>'),
           ('<h1>Prices<h1>', 'The closing tag is missing its slash', '<h1>Prices</h1>'),
           ('<table><tr>Name</tr></table>', 'Table data must be inside a <td> (or <th>) cell', '<table><tr><td>Name</td></tr></table>')]


@t.add('C2', (2, 3, 4), 'explain')
def g12_htmlerr(r, D):
    e, why, fix = r.choice(HTMLERR)
    d = ctx(r)
    return {'stem': f'{d["p"]} wrote this HTML for the website of {d["org"]}: {e} Identify the error and write the corrected HTML.', 'answer': f'{why}. Correct: {fix}',
            'key': f'1 mark error identified ({why}); 1 mark corrected code {fix}. [2]', 'marks': 2, 'type': 'explain'}


def js_expr(r, D):
    """Return (code lines, output, explanation) for a JavaScript output-prediction item."""
    k = r.randrange(6 if D >= 3 else 4)
    a, b = r.randrange(3, 20), r.randrange(2, 9)
    if k == 0:
        lines = [f'let x = {a};', f'let y = "{b}";', 'console.log(x + y);']
        return lines, f'{a}{b}', 'y is a string, so + concatenates the two values'
    if k == 1:
        lines = [f'let x = {a};', f'let y = "{b}";', 'console.log(x * y);']
        return lines, str(a * b), 'the string "' + str(b) + '" is converted to a number for *'
    if k == 2:
        lines = [f'let n = {a};', f'console.log(n % {b});']
        return lines, str(a % b), f'% gives the remainder of {a} ÷ {b}'
    if k == 3:
        lines = [f'let total = {a};', f'total += {b};', 'total *= 2;', 'console.log(total);']
        return lines, str((a + b) * 2), f'total = ({a} + {b}) × 2'
    if k == 4:
        w = r.choice(['NETWORK', 'BROWSER', 'SCRIPT', 'ELEMENT', 'COOKIE'])
        i = r.randrange(len(w))
        lines = [f'let word = "{w}";', f'console.log(word.length + " " + word.charAt({i}));']
        return lines, f'{len(w)} {w[i]}', f'length is {len(w)}; charAt({i}) counts from 0'
    lines = [f'let a = {a};', f'let b = {b};', 'console.log(Math.floor(a / b) + " r " + (a % b));']
    return lines, f'{a // b} r {a % b}', f'{a} ÷ {b} = {a // b} remainder {a % b}'


t = T(8, 'JavaScript basics: variables, data types, operators and functions', 'javascript basics', 'variables, data types, operators and functions',
      defs=[('variable (JavaScript)', 'A named storage location for a value, declared with let, const or var.'),
            ('const', 'A keyword that declares a variable whose value cannot be reassigned after it is set.'),
            ('function (JavaScript)', 'A named block of code that carries out a task, can take parameters and can return a value.'),
            ('string', 'A data type that holds a sequence of characters, written inside quotation marks.'),
            ('modulus operator (%)', 'An operator that gives the remainder after one number is divided by another.')],
      mcqs=[('What is output by console.log(7 + "3");?', '73', ['10', '4', '21'], 'One operand is a string, so + concatenates.'),
            ('Which keyword should be used for a value that must never change, such as the VAT rate?', 'const', ['let', 'var', 'function'], 'const prevents reassignment.'),
            ('What is the value of 17 % 5?', '2', ['3', '3.4', '85'], '17 = 3 × 5 + 2.')],
      exps=[('Explain why "5" + 2 gives "52" in JavaScript but "5" * 2 gives 10.', 'With + and a string operand JavaScript concatenates, turning 2 into "2"; * is only numeric, so "5" is converted to the number 5 and multiplied.', '1 mark + concatenates with strings; 1 mark * converts to number. [2]'),
            ('Explain two advantages of using functions in JavaScript.', 'Code can be reused by calling the function many times; programs are easier to read, test and maintain because tasks are split into named parts; parameters let the same code work with different values.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain the difference between let and const.', 'A variable declared with let can be given a new value later; one declared with const cannot be reassigned.', '1 mark let reassignable; 1 mark const not. [2]')],
      ars=[('"3" + 4 evaluates to "34".', 'The + operator concatenates when either operand is a string.'),
           ('Functions make code easier to reuse.', 'The same block of code can be called many times with different arguments.')],
      falses=['const variables can be reassigned at any time.', 'The % operator gives the result of division as a decimal.'],
      intros=['{p} is learning JavaScript to add interactive features to the website of {org} in {city}.',
              '{org} in {city} wants a JavaScript price calculator on its booking page.'],
      parts=[('Explain the difference between a variable and a constant.', 'Variable can change while the program runs; constant is fixed.', '1 mark each. [2]'),
             ('Write a JavaScript function total(price, qty) that returns the price multiplied by the quantity.', 'function total(price, qty) { return price * qty; }', '1 mark header with parameters; 1 mark return of product. [2]'),
             ('State three JavaScript data types with an example of each.', 'Number (42), String ("Lima"), Boolean (true), Array ([1,2]), Object.', '1 mark each, max 3. [3]'),
             ('Explain why input from a form should be converted with Number() before adding.', 'Form values are strings, so + would concatenate instead of adding.', '1 mark strings; 1 mark concatenation. [2]')],
      ev=[('the use of JavaScript to add interactivity to the website of {org}', 'immediate feedback; calculators and validation without reloading; richer user experience.', 'may be disabled or behave differently in some browsers; security must not rely on client-side code; accessibility issues if poorly written.', 'JavaScript greatly improves usability but critical checks must be repeated on the server.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_js1(r, D):
    lines, out, why = js_expr(r, D)
    if D == 1:
        return None
    m = 2 if D <= 3 else 3
    stem = 'State the output of this JavaScript code.\n' + code(lines) + (' Explain your answer.' if D >= 4 else '')
    return Q(stem, out + (f' ({why})' if D >= 4 else ''), f'{out} [2]' + (f'; explanation: {why} [1]' if D >= 4 else '') + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_jsfunc(r, D):
    a, b = r.randrange(2, 6), r.randrange(1, 9)
    x = r.randrange(1, 6)
    nm = r.choice(['calc', 'change', 'process', 'step'])
    lines = [f'function {nm}(n) {{', f'{IND}return n * {a} + {b};', '}']
    v1 = x * a + b
    if D <= 2:
        lines.append(f'console.log({nm}({x}));')
        out = str(v1)
        why = f'{x} × {a} + {b} = {v1}'
        if D == 1:
            return MCQ(r, 'What is output by this JavaScript?\n' + code(lines), out, [str(x * (a + b)), str(v1 + a), str((x + b) * a)], why)
    else:
        lines.append(f'console.log({nm}({nm}({x})));')
        v2 = v1 * a + b
        out = str(v2)
        why = f'inner call {x} × {a} + {b} = {v1}; outer call {v1} × {a} + {b} = {v2}'
    m = 2 if D <= 3 else 3
    return Q('State the output of this JavaScript code and show how you obtained it.\n' + code(lines), out, f'{why} — {out} [{m}]', marks=m, typ='numerical')


t = T(8, 'JavaScript selection, loops and event handling with the DOM', 'javascript selection, loops and event handling', 'dom',
      defs=[('Document Object Model (DOM)', 'A tree structure in which the browser represents every element of a web page, which JavaScript can read and change.'),
            ('event handler', 'A function that runs when a particular event happens, such as a button being clicked (onclick) or a key being pressed.'),
            ('getElementById', 'A DOM method that returns the element with a given id so that its content or style can be changed.'),
            ('innerHTML', 'A property of an element that holds the HTML content inside it; setting it changes what is displayed.')],
      mcqs=[('Which line changes the text of <p id="msg"> to "Saved"?', 'document.getElementById("msg").innerHTML = "Saved";', ['document.msg = "Saved";', 'getElement("p") = "Saved";', 'console.log("msg", "Saved");'], 'Select by id, then set innerHTML.'),
            ('Which attribute runs a function when a button is clicked?', 'onclick', ['onload', 'href', 'src'], 'onclick is the click event.'),
            ('How many times does for (let i = 0; i < 5; i++) run its body?', '5', ['4', '6', '0'], 'i takes 0, 1, 2, 3, 4.')],
      exps=[('Explain how a button click can update a web page without reloading it.', 'The button has an event handler (e.g. onclick) that calls a JavaScript function; the function uses the DOM (getElementById) to change an element\'s innerHTML or style, so the page updates in the browser.', '1 mark event handler; 1 mark function called; 1 mark DOM changed. [3]'),
            ('Explain the difference between a for loop and a while loop in JavaScript.', 'A for loop is normally used when the number of repetitions is known, with initialisation, condition and update in one line; a while loop repeats while a condition is true, for an unknown number of times.', '1 mark for loop; 1 mark while loop. [2]')],
      ars=[('JavaScript can change a web page after it has loaded.', 'It can modify elements through the DOM.'),
           ('A for loop starting at 0 with i < 3 runs three times.', 'i takes the values 0, 1 and 2.')],
      falses=['innerHTML can only be read, never changed.', 'onclick runs when the page first loads.'],
      intros=['{p} is adding a quiz with buttons and instant feedback to the website of {org} in {city}.',
              '{org} in {city} wants a web page that counts visitors\' clicks and shows messages.'],
      parts=[('Explain what is meant by the DOM.', 'Tree representation of page elements that scripts can access and change.', '1 mark tree of elements; 1 mark accessed/changed by JS. [2]'),
             ('Write JavaScript that displays "Correct!" in an element with id "result".', 'document.getElementById("result").innerHTML = "Correct!";', '1 mark getElementById; 1 mark innerHTML assignment. [2]'),
             ('Explain how an event handler is used for a button.', 'onclick attribute/addEventListener calls a function when clicked.', '1 mark event; 1 mark function runs. [2]'),
             ('Write a loop that outputs the numbers 1 to 10.', 'for (let i = 1; i <= 10; i++) { console.log(i); }', '1 mark loop range; 1 mark output inside loop. [2]')],
      ev=[('the use of client-side JavaScript to provide instant feedback on the website of {org}', 'fast responses; less server load; engaging pages.', 'can be disabled; logic visible to users; inconsistent across browsers; needs server-side checks too.', 'excellent for usability, but important processing and checks must also happen on the server.')])


def js_loop(r, D):
    k = r.randrange(4)
    if k == 0:
        a, b, s = r.randrange(0, 4), r.randrange(8, 16), r.choice([1, 2, 3])
        lines = ['let total = 0;', f'for (let i = {a}; i <= {b}; i += {s}) {{', f'{IND}total += i;', '}', 'console.log(total);']
        vals = list(range(a, b + 1, s))
        return lines, str(sum(vals)), f'i = {", ".join(map(str, vals))}; total {sum(vals)}'
    if k == 1:
        x, lim, m = r.randrange(1, 5), r.randrange(30, 200), r.choice([2, 3])
        lines = [f'let x = {x};', 'let count = 0;', f'while (x < {lim}) {{', f'{IND}x = x * {m};', f'{IND}count++;', '}', 'console.log(x + " " + count);']
        c = 0
        v = x
        seq = [x]
        while v < lim:
            v *= m
            c += 1
            seq.append(v)
        return lines, f'{v} {c}', f'x = {", ".join(map(str, seq))}; loop runs {c} times'
    if k == 2:
        arr = [r.randrange(10, 99) for _ in range(5 if D < 4 else 6)]
        t_ = r.randrange(30, 70)
        lines = [f'let marks = [{", ".join(map(str, arr))}];', 'let n = 0;', 'for (let i = 0; i < marks.length; i++) {', f'{IND}if (marks[i] >= {t_}) {{', f'{IND}{IND}n++;', f'{IND}}}', '}', 'console.log(n);']
        c = sum(1 for v in arr if v >= t_)
        return lines, str(c), f'values ≥ {t_}: {", ".join(str(v) for v in arr if v >= t_) or "none"}'
    score = r.randrange(30, 100)
    a, b = sorted(r.sample(range(40, 90), 2))
    lines = [f'let score = {score};', 'let grade;', f'if (score >= {b}) {{', f'{IND}grade = "Distinction";', f'}} else if (score >= {a}) {{', f'{IND}grade = "Pass";', '} else {', f'{IND}grade = "Fail";', '}', 'console.log(grade);']
    g = 'Distinction' if score >= b else ('Pass' if score >= a else 'Fail')
    return lines, g, f'{score} compared with {b} then {a}'


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_js2(r, D):
    lines, out, why = js_loop(r, D)
    if D == 1:
        return MCQ(r, 'What is output by this JavaScript?\n' + code(lines), out, [out + '0', str(len(out)), 'undefined', 'NaN'], why)
    m = 2 if D <= 3 else 3
    return Q('State the output of this JavaScript code.' + (' Show your working.' if D >= 4 else '') + '\n' + code(lines), out, f'{why} — output {out} [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def g12_dom(r, D):
    start = r.randrange(0, 5)
    step = r.choice([1, 2, 5])
    clicks = r.randrange(2, 7)
    lim = start + step * r.randrange(1, clicks + 1)
    html = [f'<p id="count">{start}</p>', '<button onclick="add()">Add</button>', '<p id="msg"></p>', '<script>', f'let c = {start};', 'function add() {', f'{IND}c = c + {step};',
            f'{IND}document.getElementById("count").innerHTML = c;', f'{IND}if (c >= {lim}) {{', f'{IND}{IND}document.getElementById("msg").innerHTML = "Limit reached";', f'{IND}}}', '}', '</script>']
    c = start + step * clicks
    msg = 'Limit reached' if c >= lim else '(empty)'
    stem = 'A web page contains:\n' + code(html) + f'\nThe user clicks the button {clicks} times. State what is displayed in the paragraphs with id "count" and id "msg".'
    m = 2
    key = f'count: {start} + {clicks} × {step} = {c} [1]; msg: {msg} [1]'
    if D >= 4:
        stem += ' Explain the role of the onclick attribute.'
        key += '; onclick is an event handler that calls add() each time the button is clicked [1]'
        m = 3
    return Q(stem, f'count shows {c}; msg shows {msg}', key + f'. [{m}]', marks=m, typ='numerical')


VALJS = ['function check(age) {', f'{IND}if (age == "") {{', f'{IND}{IND}return "Required";', f'{IND}}}', f'{IND}if (isNaN(age)) {{', f'{IND}{IND}return "Not a number";', f'{IND}}}',
         f'{IND}if (age < MIN || age > MAX) {{', f'{IND}{IND}return "Out of range";', f'{IND}}}', f'{IND}return "OK";', '}']

t = T(8, 'Validating form input with JavaScript', 'validating form input with javascript', 'validating form input',
      defs=[('client-side validation', 'Checking form input in the browser, using JavaScript or HTML attributes, before the data is sent to the server.'),
            ('server-side validation', 'Checking submitted data on the web server, which cannot be bypassed by the user.'),
            ('isNaN()', 'A JavaScript function that returns true if a value is not a number (cannot be converted to a number).'),
            ('regular expression', 'A pattern used to test whether a string matches a format, such as an email address or postcode.')],
      mcqs=[('Why must server-side validation also be used when JavaScript validation is in place?', 'Users can disable or bypass JavaScript, so invalid or malicious data could still be submitted', ['JavaScript cannot check numbers', 'Server-side validation is faster for the user', 'Browsers delete form data'], 'Client-side checks are for convenience only.'),
            ('What does isNaN("abc") return?', 'true', ['false', '"abc"', '0'], '"abc" cannot be converted to a number.'),
            ('Which HTML attribute makes a form field compulsory?', 'required', ['alt', 'href', 'onclick'], 'The browser refuses to submit an empty required field.')],
      exps=[('Explain one advantage of validating form data with JavaScript.', 'Errors are reported immediately without sending data to the server and reloading the page, which is faster for the user and reduces server load.', '1 mark immediate feedback; 1 mark less server load/no reload. [2]'),
            ('Explain why client-side validation alone is not secure.', 'The user controls the browser: JavaScript can be turned off or the request edited, so the server must check the data again before using it.', '1 mark can be bypassed; 1 mark server must recheck. [2]')],
      ars=[('JavaScript validation gives instant feedback.', 'The check runs in the browser without contacting the server.'),
           ('Server-side validation is still needed.', 'Client-side checks can be bypassed.')],
      falses=['Client-side validation cannot be bypassed.', 'isNaN("42") returns true.'],
      intros=['{p} is creating an online registration form for {org} in {city}.',
              '{org} in {city} receives many incorrect entries from its web booking form.'],
      parts=[('Describe two checks JavaScript could carry out on the form.', 'Presence (not empty); range (age 18–99); type (isNaN); format of email/phone with regular expressions; password length.', '1 mark each, max 2. [2]'),
             ('Explain why server-side validation is still needed.', 'Client-side can be bypassed/disabled; security and data integrity.', '1 mark each. [2]'),
             ('Write a JavaScript condition that checks that an email value contains "@".', 'if (email.indexOf("@") == -1) { alert("Invalid email"); }  (or email.includes("@"))', '1 mark test for @; 1 mark action if missing. [2]')],
      ev=[('relying on JavaScript validation for the booking form of {org}', 'instant feedback; fewer errors; less server load.', 'can be bypassed; inconsistent browser behaviour; security risk if server trusts data.', 'use JavaScript for usability and always repeat validation on the server.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_valjs(r, D):
    lo, hi = r.choice([(18, 65), (16, 99), (1, 10), (0, 100), (5, 30)])
    lines = [x.replace('MIN', str(lo)).replace('MAX', str(hi)) for x in VALJS]
    cands = ['', 'abc', str(lo - 1), str(lo), str((lo + hi) // 2), str(hi), str(hi + 1), 'ten']

    def run(v):
        if v == '':
            return 'Required'
        try:
            x = float(v)
        except ValueError:
            return 'Not a number'
        return 'Out of range' if (x < lo or x > hi) else 'OK'
    vs = r.sample(cands, 3 if D <= 2 else (4 if D <= 4 else 5))
    if D == 1:
        v = vs[0]
        return MCQ(r, 'A form uses this JavaScript validation function:\n' + code(lines) + f'\nWhat does check("{v}") return?', run(v), [x for x in ('Required', 'Not a number', 'Out of range', 'OK') if x != run(v)], f'"{v}" → {run(v)}.')
    stem = 'A form uses this JavaScript validation function:\n' + code(lines) + '\nState the value returned for each input: ' + ', '.join(f'"{v}"' for v in vs) + '.'
    ans = '; '.join(f'"{v}" → {run(v)}' for v in vs)
    m = len(vs)
    key = '1 mark each: ' + ans
    if D >= 4:
        stem += ' Identify which inputs are extreme test data.'
        ext = [v for v in vs if v in (str(lo), str(hi))]
        key += f'; extreme: {", ".join(ext) or "none in this set"} [1]'
        ans += f'; extreme data: {", ".join(ext) or "none"}'
        m += 1
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 9 System life cycle
METHODS = {'questionnaire': ('many users can be surveyed quickly and cheaply, anonymously', 'low response rates; cannot ask follow-up questions; questions may be misunderstood'),
           'interview': ('detailed answers; follow-up questions; observe body language', 'time-consuming and expensive; few people; interviewees may give answers they think are wanted'),
           'observation': ('see the real system in use, including problems users do not mention', 'people may behave differently when watched; time-consuming; may miss infrequent tasks'),
           'document analysis': ('shows exactly what data is recorded and output; reveals volumes and formats', 'documents may be out of date; does not show problems or how staff really work')}
RESEARCH = [('finding the views of 400 staff spread across several sites', 'questionnaire'), ('finding out in detail what the finance manager needs from the new system', 'interview'),
            ('seeing how receptionists actually handle bookings during a busy morning', 'observation'), ('finding out which data fields are on the current paper order forms and invoices', 'document analysis')]

t = T(9, 'Analysis: research methods (questionnaires, interviews, observation, document analysis) and system requirements', 'analysis: research methods', 'questionnaires, interviews, observation, document analysis', 'system requirements',
      defs=[('analysis (systems life cycle)', 'The stage in which the current system is studied, using research methods, to identify its problems and the requirements of the new system.'),
            ('user requirements', 'What the users need the new system to do, stated in their own terms.'),
            ('system requirements', 'A specification of the hardware, software and functions the new system needs to meet the user requirements.'),
            ('document analysis', 'Examining the documents used in the current system, such as forms, invoices and reports, to find what data is input, processed and output.')],
      mcqs=[('Which research method is most suitable for gathering the opinions of 2000 customers?', 'Questionnaire', ['Interview', 'Observation', 'Document analysis'], 'Questionnaires reach many people cheaply.'),
            ('Why might staff behave differently during observation?', 'They know they are being watched, so they may work more carefully than usual', ['Observation is always secret', 'The analyst does the work for them', 'They are interviewed at the same time'], 'The Hawthorne effect.')],
      exps=[('Explain why the analysis stage is important.', 'It identifies the problems with the current system and the exact requirements of users, so the new system is designed to solve the right problems; mistakes here are costly to fix later.', '1 mark identifies problems/requirements; 1 mark consequence of poor analysis. [2]'),
            ('Explain one advantage and one disadvantage of interviews compared with questionnaires.', 'Advantage: detailed answers and follow-up questions. Disadvantage: time-consuming and expensive, so only a few people can be interviewed.', '1 mark advantage; 1 mark disadvantage. [2]')],
      ars=[('Questionnaires suit large numbers of users.', 'They can be distributed widely and answered at the same time.'),
           ('Interviews allow follow-up questions.', 'The analyst talks directly to the interviewee.')],
      falses=['Observation is quick and reaches thousands of users.', 'Document analysis shows how staff feel about the system.'],
      intros=['{org}, {aot} in {city}, has asked a systems analyst to replace its paper-based booking system.',
              '{p}, a systems analyst, is investigating the stock control system at {org} in {city}.'],
      parts=[('Describe two research methods the analyst could use, giving an advantage of each.', 'Questionnaire (many staff); interview (detail); observation (real use); document analysis (data items).', '2 × (1 mark method, 1 mark advantage). [4]'),
             ('Explain the difference between user requirements and system requirements.', 'User: what users need in their terms; system: hardware/software/functions to meet them.', '1 mark each. [2]'),
             ('Describe what the analyst would look for in the current documents.', 'Data items recorded; formats; volumes; outputs produced; duplication.', '1 mark per point, max 2. [2]')],
      ev=[('which research method the analyst at {org} should rely on most', 'interviews give detail; questionnaires reach many; observation shows reality; documents show data.', 'each method has weaknesses; relying on one gives an incomplete picture; time and cost limits.', 'a combination of methods is best, chosen to suit the size and type of organisation.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def g12_research(r, D):
    s, mth = r.choice(RESEARCH)
    pro, con = METHODS[mth]
    if D <= 2:
        return MCQ(r, f'Which research method is most suitable for {s}?', mth.capitalize(), [m.capitalize() for m in METHODS if m != mth], f'{mth}: {pro}.')
    d = ctx(r)
    return Q(f'An analyst at {d["org"]} in {d["city"]} needs to do the following: {s}. Recommend a research method, and give one advantage and one disadvantage of it.',
             f'{mth.capitalize()}. Advantage: {pro}. Disadvantage: {con}.', f'1 mark method ({mth}); 1 mark advantage ({pro}); 1 mark disadvantage ({con}). [3]', marks=3)


ERDS = [('CUSTOMER and ORDER: a customer can place many orders; each order is placed by one customer', 'one-to-many'),
        ('STUDENT and COURSE: a student takes many courses; each course has many students', 'many-to-many'),
        ('COUNTRY and CAPITAL CITY: each country has one capital; each capital belongs to one country', 'one-to-one'),
        ('DOCTOR and PATIENT (registered): each patient is registered with one doctor; a doctor has many patients', 'one-to-many'),
        ('AUTHOR and BOOK (co-written books allowed): an author writes many books; a book can have several authors', 'many-to-many'),
        ('EMPLOYEE and COMPANY CAR: each employee has at most one car; each car is assigned to one employee', 'one-to-one')]
DFDSYM = [('external entity', 'a source or destination of data outside the system, such as a customer'), ('process', 'an action that transforms data, such as "calculate invoice"'),
          ('data store', 'where data is held, such as a customer file'), ('data flow', 'the movement of data between entities, processes and stores, shown by an arrow')]

t = T(9, 'Design: data flow diagrams, system flowcharts, entity-relationship diagrams and input/output design', 'design: data flow diagrams', 'system flowcharts', 'entity-relationship diagrams', 'input/output design',
      defs=[('data flow diagram (DFD)', 'A diagram showing how data moves through a system between external entities, processes and data stores.'),
            ('system flowchart', 'A diagram showing the overall flow of data through a system, including inputs, processes, files and outputs, using standard symbols.'),
            ('entity-relationship diagram (ERD)', 'A diagram showing the entities in a system and the relationships (one-to-one, one-to-many, many-to-many) between them.'),
            ('input design', 'Planning how data will be captured and entered, including screen and form layouts, field order and validation.'),
            ('output design', 'Planning how information will be presented, such as screen layouts and report formats, to meet user needs.')],
      mcqs=[('In a DFD, what does an external entity represent?', 'A person or organisation outside the system that sends or receives data', ['A file of data', 'A calculation', 'A loop'], 'Sources and sinks.'),
            ('How is a many-to-many relationship usually resolved in a database design?', 'By adding a link entity with two one-to-many relationships', ['By deleting one entity', 'By merging all entities into one table', 'By making both keys foreign keys in the same entity'], 'A junction table.')],
      exps=[('Explain why the designer produces a DFD before writing any code.', 'It shows clearly what data enters, is processed, is stored and leaves the system, so the requirements can be checked with users and the processes and files can be designed correctly.', '1 mark shows data movement; 1 mark check/plan processes and files. [2]'),
            ('Explain two features of good input screen design.', 'Logical order matching source documents; clear labels and instructions; drop-down lists/validation; consistent layout; error messages; not overcrowded.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('A link entity resolves a many-to-many relationship.', 'Each original entity has a one-to-many relationship with the link entity.'),
           ('DFDs show data stores.', 'They show where data is held within the system.')],
      falses=['A DFD shows the exact screen layout of every form.', 'An ERD shows the order in which processes happen.'],
      intros=['{p} is designing a new ordering system for {org} in {city}.',
              '{org} in {city} has approved the analysis of its new booking system and design is starting.'],
      parts=[('Identify the four types of symbol used in a data flow diagram.', 'External entity, process, data store, data flow.', '1 mark each, max 4. [4]'),
             ('Explain what an entity-relationship diagram shows.', 'Entities and the type of relationship between them (1:1, 1:M, M:M).', '1 mark entities; 1 mark relationships. [2]'),
             ('Describe two features of a well-designed output report.', 'Clear title and headings; only relevant data; totals/summaries; sorted; date and page numbers.', '1 mark each, max 2. [2]'),
             ('Explain why test plans are designed at this stage.', 'To check later that the system meets the design and requirements.', '1 mark each part. [2]')],
      ev=[('the importance of thorough design documentation for the new system at {org}', 'guides developers; allows checking with users; supports testing and maintenance.', 'takes time and cost; may become outdated if requirements change; can delay development.', 'good design documents save much more time later than they cost, especially for maintenance.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def g12_erd(r, D):
    if D <= 2:
        if r.random() < 0.5:
            s, rel = r.choice(ERDS)
            return MCQ(r, f'Which relationship exists between {s}?', rel.capitalize(), [x.capitalize() for x in ('one-to-one', 'one-to-many', 'many-to-many', 'none') if x != rel], f'{rel}.')
        n, dsc = r.choice(DFDSYM)
        return MCQ(r, f'Which DFD element represents {dsc}?', n.capitalize(), [x[0].capitalize() for x in DFDSYM if x[0] != n] + ['Decision box'], f'{n}: {dsc}.')
    picks = r.sample(ERDS, 2 if D == 3 else 3)
    m = 2 * len(picks) if D >= 4 else len(picks)
    return Q('State the type of relationship in each case' + (' and explain how any many-to-many relationship would be implemented' if D >= 4 else '') + ': ' + '; '.join(f'({i + 1}) {x[0]}' for i, x in enumerate(picks)) + '.',
             '; '.join(f'({i + 1}) {x[1]}' for i, x in enumerate(picks)) + ('. Many-to-many relationships need a link table with a compound key.' if D >= 4 else ''),
             '1 mark each relationship' + ('; plus 1 mark each for correct justification or link-table explanation' if D >= 4 else '') + ': ' + '; '.join(f'({i + 1}) {x[1]}' for i, x in enumerate(picks)) + f'. [{m}]', marks=m)


t = T(9, 'Development and testing: test plans and test data (normal, abnormal, extreme)', 'development and testing', 'test plans and test data', 'normal, abnormal, extreme',
      defs=[('test plan', 'A document listing each test to be carried out, with its purpose, the test data, the expected result and space for the actual result.'),
            ('normal test data', 'Valid data that the system should accept and process correctly.'),
            ('abnormal (erroneous) test data', 'Invalid data that the system should reject, such as a value of the wrong type or outside the allowed range.'),
            ('extreme test data', 'Valid data at the boundaries (limits) of the allowed range, which should be accepted.'),
            ('alpha testing', 'Testing carried out in-house by the developers or testers before the system is released to users.'),
            ('beta testing', 'Testing of a nearly finished system by real users outside the development team, to find remaining problems.')],
      mcqs=[('A field accepts whole numbers from 1 to 50. Which is extreme test data?', '50', ['25', '51', '"fifty"'], 'Boundary values that should be accepted.'),
            ('Why is the expected result written in the test plan before testing?', 'So the actual result can be compared with it to decide whether the test passed', ['So the test can be skipped', 'To fill the space', 'So the programmer can change it afterwards'], 'Objective comparison.')],
      exps=[('Explain why both normal and abnormal test data are needed.', 'Normal data checks that the system processes valid input correctly; abnormal data checks that invalid input is rejected with a suitable message rather than crashing or being stored.', '1 mark normal purpose; 1 mark abnormal purpose. [2]'),
            ('Explain the difference between alpha and beta testing.', 'Alpha testing is done in-house by the developers/testers before release; beta testing is done by real users outside the company on a nearly complete version.', '1 mark alpha; 1 mark beta. [2]')],
      ars=[('Extreme data should be accepted by the system.', 'It is valid data at the limits of the range.'),
           ('A test plan includes expected results.', 'They are compared with the actual results.')],
      falses=['Abnormal data should be accepted and stored.', 'Beta testing is done only by the programmers.'],
      intros=['{p} is testing a new online booking system for {org} in {city}.',
              '{org} in {city} is about to release a new stock-control program.'],
      parts=[('Describe what should be included in a test plan.', 'Test number; description/purpose; test data; type of data; expected result; actual result; pass/fail.', '1 mark per item, max 3. [3]'),
             ('Explain why extreme test data is important.', 'Errors often occur at boundaries (e.g. < instead of <=).', '1 mark boundaries; 1 mark example error. [2]'),
             ('Explain the purpose of beta testing.', 'Real users find problems not found in-house before full release.', '1 mark real users; 1 mark find remaining bugs. [2]')],
      ev=[('whether {org} should release the system after alpha testing only', 'quicker release; lower cost; developers know the system.', 'developers miss real-world use cases; bugs found by customers damage reputation; beta testing gives user feedback.', 'beta testing is usually worthwhile for systems used by many people.')])

t.add('C3', (2, 3, 4, 5), 'numerical')(ch1_testdata)


@t.add('C3', (2, 3, 4, 5), 'short')
def g12_testplan(r, D):
    fld, lo, hi = r.choice([('number of tickets', 1, 8), ('age of a club member', 12, 18), ('percentage score', 0, 100), ('number of nights', 1, 14), ('quantity ordered', 1, 250)])
    rows = [('normal', str((lo + hi) // 2), 'accepted'), ('extreme', str(lo), 'accepted'), ('extreme', str(hi), 'accepted'), ('abnormal', str(hi + 1), 'rejected with error message'),
            ('abnormal', 'abc', 'rejected with error message')]
    k = 3 if D <= 3 else 5
    pick = rows[:k] if k == 5 else [rows[0], rows[1], rows[3]]
    d = ctx(r)
    stem = f'{d["org"]} in {d["city"]} has a field "{fld}" that must be a whole number from {lo} to {hi}. Complete a test plan with {k} tests, giving the test data, the type of test data and the expected result for each.'
    ans = '; '.join(f'{v} ({ty}) → {ex}' for ty, v, ex in pick)
    m = k + (1 if D >= 5 else 0)
    key = f'1 mark per correct row (data + type + expected result), e.g. {ans}'
    if D >= 5:
        stem += ' Explain why the expected result for abnormal data should include an error message.'
        key += '; the user must know why the input was rejected and how to correct it [1]'
        ans += '; error messages tell the user how to correct the input.'
    return Q(stem, ans, key + f'. [{m}]', marks=m)


IMPL = [('a hospital replacing its patient-records system, where any failure could put lives at risk', 'parallel', 'the old system keeps running, so if the new one fails nothing is lost; results can be compared'),
        ('a chain of 60 shops introducing a new point-of-sale system', 'pilot', 'it is tried in one or a few shops first, so problems are found before rolling out to all branches'),
        ('a small office replacing a spreadsheet with a simple off-the-shelf package over a weekend', 'direct', 'cheapest and quickest; the system is simple and low-risk'),
        ('a university introducing a large system with separate modules for admissions, timetabling and fees', 'phased', 'one module is introduced at a time, so staff learn gradually and problems are limited to one part'),
        ('a bank changing the software that calculates interest, where results must be checked against the old system', 'parallel', 'both systems run together so outputs can be compared'),
        ('a new law means a payroll system must be changed by a fixed date and the old version cannot be used afterwards', 'direct', 'the old system cannot legally be used after the deadline')]
MAINT = [('A bug causes invoices to show the wrong total when a discount is applied.', 'corrective'), ('A tax rate changes and the system must use the new rate.', 'adaptive'),
         ('Users ask for reports to load faster and for a new chart to be added.', 'perfective'), ('The system must be changed to run on a new operating system.', 'adaptive'),
         ('The program crashes when a customer surname contains an apostrophe.', 'corrective'), ('The menu layout is improved to make common tasks quicker.', 'perfective')]

t = T(9, 'Implementation methods (direct, parallel, pilot, phased), documentation, evaluation and maintenance', 'implementation methods', 'direct, parallel, pilot, phased', 'documentation, evaluation and maintenance',
      defs=[('direct changeover', 'Stopping the old system and starting the new one at the same moment.'),
            ('parallel running', 'Running the old and new systems together for a period, until the new one is shown to work correctly.'),
            ('pilot implementation', 'Introducing the new system in one part of the organisation (e.g. one branch) first, before the rest.'),
            ('phased implementation', 'Introducing the new system one module or part at a time until the whole system is in use.'),
            ('technical documentation', 'Documentation for people who will maintain or develop the system, such as program listings, data dictionaries, flowcharts and design details.'),
            ('user documentation', 'Documentation that explains how to use the system, such as how to log in, enter data, print reports and deal with error messages.')],
      mcqs=[('Which implementation method has the highest risk if the new system fails?', 'Direct changeover', ['Parallel running', 'Pilot implementation', 'Phased implementation'], 'There is no old system to fall back on.'),
            ('Which type of maintenance improves performance or adds new features requested by users?', 'Perfective maintenance', ['Corrective maintenance', 'Adaptive maintenance', 'Preventive changeover'], 'Perfective = improving.'),
            ('Which item belongs in user documentation?', 'How to recover from common error messages', ['Program code listings', 'The data dictionary', 'Variable names used'], 'User guides explain how to use the system.')],
      exps=[('Explain one advantage and one disadvantage of parallel running.', 'Advantage: if the new system fails, the old one is still working so no data is lost and outputs can be compared. Disadvantage: staff must do the work twice, which is costly and tiring.', '1 mark advantage; 1 mark disadvantage. [2]'),
            ('Explain why a system is evaluated after implementation.', 'To check whether it meets the original requirements and objectives, to identify problems and user feedback, and to decide what improvements or maintenance are needed.', '1 mark compare with requirements; 1 mark identify problems/improvements. [2]'),
            ('Explain the difference between technical and user documentation.', 'Technical documentation helps developers maintain and upgrade the system (code, data structures, design); user documentation helps users operate it (instructions, troubleshooting).', '1 mark technical; 1 mark user. [2]')],
      ars=[('Parallel running is expensive.', 'Staff must operate two systems at the same time.'),
           ('Adaptive maintenance is needed when tax rates change.', 'The system must be changed to fit new external requirements.')],
      falses=['Direct changeover is the safest method.', 'Corrective maintenance adds new features requested by users.'],
      intros=['{org}, {aot} in {city}, is about to implement a new computerised system.',
              '{p} is planning how to introduce a new system at {org} in {city}, which has several branches.'],
      parts=[('Describe two implementation methods that could be used.', 'Direct; parallel; pilot; phased — with brief descriptions.', '2 × (1 mark method, 1 mark description). [4]'),
             ('Describe four items that should be included in the user documentation.', 'How to load/log in; how to enter data; how to save/print; error messages and troubleshooting; hardware/software requirements; FAQs; glossary.', '1 mark each, max 4. [4]'),
             ('Explain how the new system would be evaluated.', 'Compare with requirements; gather user feedback; measure performance; identify limitations and improvements.', '1 mark per point, max 3. [3]'),
             ('Describe the three types of maintenance.', 'Corrective (fix bugs); adaptive (change for new requirements/environment); perfective (improve performance/features).', '1 mark each. [3]')],
      ev=[('which implementation method {org} should use for its new system', 'parallel is safest; pilot limits risk to one site; phased spreads training; direct is quickest and cheapest.', 'parallel is costly; pilot is slow to roll out; phased can cause compatibility issues between old and new parts; direct is risky.', 'the choice depends on how critical the system is, its size and the budget.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def g12_impl(r, D):
    if D <= 2:
        if r.random() < 0.5:
            s, mth, why = r.choice(IMPL)
            return MCQ(r, f'Which implementation method is most suitable for {s}?', mth.capitalize(), [x.capitalize() for x in ('direct', 'parallel', 'pilot', 'phased') if x != mth], f'{mth}: {why}.')
        s, k = r.choice(MAINT)
        return MCQ(r, f'{s} Which type of maintenance is needed?', k.capitalize(), [x.capitalize() for x in ('corrective', 'adaptive', 'perfective', 'emergency changeover') if x != k], f'{k} maintenance.')
    (s1, m1, w1), (s2, m2, w2) = r.sample(IMPL, 2)
    if m1 == m2:
        return None
    return Q(f'Recommend an implementation method for each situation and justify your choice: (1) {s1}; (2) {s2}.', f'(1) {m1}: {w1}. (2) {m2}: {w2}.',
             f'(1) {m1} [1]; justification: {w1} [1] (2) {m2} [1]; justification: {w2} [1]. [4]', marks=4)


# =============================================================================== Chapter 10 Expert systems
t = T(10, 'Components of an expert system: knowledge base, rules base, inference engine and user interface', 'components of an expert system', 'knowledge base, rules base, inference engine and user interface',
      defs=[('expert system', 'A computer system that imitates the decision-making of a human expert in a particular field, using stored knowledge and rules.'),
            ('knowledge base', 'The part of an expert system that stores facts about the subject area, collected from human experts.'),
            ('rules base', 'The set of IF ... THEN rules in an expert system that link facts to conclusions.'),
            ('inference engine', 'The part of an expert system that applies the rules to the facts and the user\'s answers to reach conclusions.'),
            ('explanation system', 'The part of an expert system that explains to the user how a conclusion was reached and why a question was asked.')],
      mcqs=[('Which component of an expert system applies the rules to reach a conclusion?', 'Inference engine', ['Knowledge base', 'User interface', 'Explanation system'], 'It does the reasoning.'),
            ('Which component asks the user questions and displays the conclusions?', 'User interface', ['Rules base', 'Knowledge base', 'Inference engine'], 'It handles input and output.'),
            ('Why does an expert system include an explanation system?', 'So users can see how a conclusion was reached and trust or check it', ['To store new rules', 'To compress the knowledge base', 'To encrypt answers'], 'Transparency of reasoning.')],
      exps=[('Describe how the components of an expert system work together to give advice.', 'The user interface asks questions and collects answers; the inference engine applies rules from the rules base to these answers and the facts in the knowledge base; it reaches a conclusion, which the interface displays with an explanation.', '1 mark per point, max 4. [4]'),
            ('Explain why an expert system cannot completely replace a human expert.', 'It only knows the rules and facts it has been given, cannot use common sense or deal with unusual cases, and has no empathy; its knowledge must be kept up to date.', '1 mark limited to programmed knowledge; 1 mark unusual cases/judgement/empathy. [2]')],
      ars=[('The inference engine is the reasoning part of an expert system.', 'It applies rules to the known facts to reach conclusions.'),
           ('Expert systems need regular updating.', 'Knowledge in the subject area changes over time.')],
      falses=['The knowledge base asks the user questions.', 'An expert system can reason about subjects it has no rules for.'],
      intros=['{org} in {city} is developing an expert system to help staff give advice to customers.',
              '{p} is explaining to trainees at {org} in {city} how an expert system works.'],
      parts=[('Describe the role of the knowledge base.', 'Stores facts about the domain collected from experts.', '1 mark each part. [2]'),
             ('Describe the role of the inference engine.', 'Applies rules to facts and user input to reach conclusions (forward/backward chaining).', '1 mark per point, max 2. [2]'),
             ('Explain why an explanation system is useful.', 'Shows reasoning so users trust/check advice; helps training.', '1 mark per point, max 2. [2]'),
             ('Describe the role of the user interface.', 'Asks questions, accepts answers and displays conclusions/explanations.', '1 mark per point, max 2. [2]')],
      ev=[('whether {org} should rely on an expert system rather than human specialists', 'consistent advice; available 24 hours; cheaper per query; stores knowledge of retiring experts.', 'lacks common sense and empathy; only as good as its rules; expensive to build and maintain; legal responsibility for wrong advice.', 'expert systems are best used to support, not replace, human specialists.')])


t = T(10, 'Uses of expert systems: medical diagnosis, mineral prospecting, car fault diagnosis and financial planning', 'uses of expert systems', 'medical diagnosis, mineral prospecting', 'car fault diagnosis and financial planning',
      defs=[('medical diagnosis expert system', 'An expert system that asks about symptoms and test results and suggests possible illnesses and their probabilities.'),
            ('mineral prospecting expert system', 'An expert system that uses geological data to suggest where deposits of minerals or oil are likely to be found.'),
            ('car fault diagnosis expert system', 'An expert system that uses information from sensors and the mechanic\'s answers to identify faults in a vehicle.'),
            ('financial planning expert system', 'An expert system that uses a client\'s financial details and rules to recommend investments, loans or pension plans.')],
      mcqs=[('Which input is used by a mineral prospecting expert system?', 'Geological survey data about rock types and structures', ['A patient\'s symptoms', 'Engine sensor readings', 'A client\'s credit history'], 'Prospecting uses geological data.'),
            ('How does a car fault diagnosis system usually receive data?', 'From the car\'s sensors through a diagnostic port and from the mechanic\'s answers', ['From a satellite only', 'From the driver\'s social media', 'From a weather station'], 'On-board diagnostics.')],
      exps=[('Explain two benefits of using an expert system for medical diagnosis.', 'Gives consistent, fast suggestions and considers many diseases, including rare ones; available where specialists are not; provides probabilities and explanations to support the doctor.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain one risk of using an expert system for financial planning.', 'The rules may not cover a client\'s unusual situation or recent market changes, so it could give unsuitable advice that loses the client money.', '1 mark limitation; 1 mark consequence. [2]')],
      ars=[('Expert systems can help doctors consider rare diseases.', 'Their knowledge base can include far more conditions than one person remembers.'),
           ('Car fault diagnosis systems use sensor data.', 'Modern cars record readings that can be read through a diagnostic port.')],
      falses=['Mineral prospecting expert systems diagnose patients.', 'Expert systems give advice without any rules.'],
      intros=['A rural health centre run by {org} near {city} has no specialist doctors on site.',
              '{org}, {aot} in {city}, is considering expert systems for several departments.'],
      parts=[('Describe how an expert system would be used for medical diagnosis.', 'Doctor enters symptoms/test results; inference engine applies rules; possible diagnoses with probabilities and explanations shown.', '1 mark per point, max 3. [3]'),
             ('Explain one advantage and one disadvantage of using the expert system.', 'Consistent, available, considers rare conditions; but lacks judgement/empathy, may be wrong, liability.', '1 mark each. [2]'),
             ('Describe one other use of expert systems.', 'Car fault diagnosis; mineral prospecting; financial planning; plant identification; tax advice.', '1 mark use; 1 mark description. [2]')],
      ev=[('the use of an expert system for diagnosis at {org}', 'consistent fast advice; considers many conditions; helps non-specialists; explanation supports learning.', 'cannot examine patients or show empathy; may be wrong; expensive to build/update; legal responsibility.', 'useful as a decision-support tool alongside qualified staff.')])


RULESETS = [
    ('car fault diagnosis', [(('engine will not start', 'lights are dim'), 'battery is flat'), (('battery is flat',), 'recharge or replace the battery'),
                              (('engine will not start', 'starter clicks'), 'starter motor fault'), (('starter motor fault',), 'replace the starter motor'),
                              (('engine overheats', 'coolant level low'), 'coolant leak'), (('coolant leak',), 'repair the radiator hose')],
     ['engine will not start', 'lights are dim', 'starter clicks', 'engine overheats', 'coolant level low']),
    ('plant health advice', [(('leaves are yellow', 'soil is wet'), 'plant is overwatered'), (('plant is overwatered',), 'water less often'),
                             (('leaves have white powder',), 'mildew infection'), (('mildew infection', 'weather is humid'), 'spray with fungicide'),
                             (('leaves are yellow', 'soil is dry'), 'plant is underwatered'), (('plant is underwatered',), 'water more often')],
     ['leaves are yellow', 'soil is wet', 'soil is dry', 'leaves have white powder', 'weather is humid']),
    ('loan advice', [(('income is regular', 'credit history is good'), 'low risk applicant'), (('low risk applicant', 'deposit is at least 10%'), 'approve the loan'),
                     (('credit history is poor',), 'high risk applicant'), (('high risk applicant',), 'refer to a manager'),
                     (('income is irregular', 'credit history is good'), 'medium risk applicant'), (('medium risk applicant',), 'offer a smaller loan')],
     ['income is regular', 'income is irregular', 'credit history is good', 'credit history is poor', 'deposit is at least 10%']),
]


def forward(rules, facts):
    known = list(facts)
    fired = []
    changed = True
    while changed:
        changed = False
        for i, (cond, concl) in enumerate(rules):
            if concl not in known and all(c in known for c in cond):
                known.append(concl)
                fired.append(i + 1)
                changed = True
    return known, fired


def backward(rules, goal, facts, asked):
    """Return True if goal can be proved; record base facts that would be asked."""
    if goal in facts:
        return True
    for cond, concl in rules:
        if concl == goal:
            if all(backward(rules, c, facts, asked) for c in cond):
                return True
    if not any(concl == goal for _, concl in rules):
        asked.append(goal)
    return False


t = T(10, 'Creating an expert system: gathering knowledge and building rules; forward and backward chaining', 'creating an expert system', 'gathering knowledge and building rules', 'forward and backward chaining',
      defs=[('forward chaining', 'Reasoning that starts from the known facts and applies rules whose conditions are met to derive new facts, until a conclusion is reached (data-driven).'),
            ('backward chaining', 'Reasoning that starts from a possible conclusion (goal) and works backwards through the rules to see whether the facts support it (goal-driven).'),
            ('knowledge engineer', 'A specialist who gathers knowledge from human experts and turns it into facts and rules for an expert system.'),
            ('rule (expert system)', 'A statement of the form IF condition(s) THEN conclusion, used by the inference engine.')],
      mcqs=[('Which reasoning method starts with a hypothesis and checks whether the facts support it?', 'Backward chaining', ['Forward chaining', 'Parallel running', 'Tweening'], 'Goal-driven reasoning.'),
            ('Who usually gathers knowledge from experts when an expert system is built?', 'A knowledge engineer', ['A network technician', 'A web designer', 'A data entry clerk'], 'Knowledge elicitation.'),
            ('Which is the first step in creating an expert system?', 'Gathering knowledge from human experts', ['Testing the inference engine', 'Designing the user manual', 'Training users'], 'Knowledge must be acquired before rules are written.')],
      exps=[('Describe the stages in creating an expert system.', 'Knowledge engineer interviews experts and studies documents; knowledge is organised into facts (knowledge base) and IF–THEN rules; inference engine and user interface designed; system tested against experts\' decisions and refined.', '1 mark per stage, max 4. [4]'),
            ('Explain the difference between forward and backward chaining.', 'Forward chaining starts from known facts and fires rules to reach conclusions; backward chaining starts with a goal and works back to find whether facts support it.', '1 mark forward; 1 mark backward. [2]')],
      ars=[('Forward chaining is data-driven.', 'It starts from the facts that are known.'),
           ('Experts\' decisions are used to test an expert system.', 'Its conclusions should match those of human experts on the same cases.')],
      falses=['Backward chaining starts from all the known facts.', 'Rules in an expert system are written without consulting experts.'],
      intros=['{org} in {city} is building an expert system with the help of its most experienced staff.',
              '{p} is a knowledge engineer working for {org} in {city}.'],
      parts=[('Describe how knowledge is gathered from experts.', 'Interviews; observation of experts at work; questionnaires; studying manuals and case records.', '1 mark per method, max 2. [2]'),
             ('Explain how the rules base is created.', 'Knowledge turned into IF–THEN rules linking conditions to conclusions; checked with experts.', '1 mark IF–THEN; 1 mark checked. [2]'),
             ('Explain how the expert system would be tested.', 'Compare its conclusions with experts\' decisions on real cases; correct rules; check explanations.', '1 mark per point, max 2. [2]')],
      ev=[('the difficulties {org} may face in creating an expert system', 'experts may struggle to explain intuitive knowledge; experts may disagree; time and cost; knowledge changes.', 'once built, the system captures expertise permanently and gives consistent advice; benefits may outweigh costs.', 'the system is worthwhile if experts are committed and it is maintained.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g12_fchain(r, D):
    dom, rules, base = r.choice(RULESETS)
    facts = r.sample(base, r.choice([2, 3]))
    known, fired = forward(rules, facts)
    rt = code([f'R{i + 1}: IF ' + ' AND '.join(c) + f' THEN {cl}' for i, (c, cl) in enumerate(rules)])
    new = known[len(facts):]
    if D == 1:
        return MCQ(r, f'An expert system for {dom} has these rules:\n{rt}\nKnown facts: {"; ".join(facts)}. Using forward chaining, how many new facts are derived?', str(len(new)),
                   [str(len(new) + 1), str(len(new) + 2), str(max(0, len(new) - 1)), str(len(rules))], f'New facts: {"; ".join(new) or "none"}.')
    stem = (f'An expert system for {dom} has these rules:\n{rt}\nThe known facts are: {"; ".join(facts)}. Using forward chaining (checking rules in order and repeating until no rule can fire), '
            f'state which rules fire, in order, and the new facts derived.')
    ans = f'Rules fired: {", ".join("R" + str(x) for x in fired) or "none"}; new facts: {"; ".join(new) or "none"}'
    m = max(2, min(4, len(fired) + 1))
    key = f'{ans} (1 mark per rule fired in correct order, 1 mark for conclusions, max {m}). [{m}]'
    if D >= 4:
        goal = r.choice([cl for _, cl in rules if not any(cl == c for cond, _ in rules for c in cond)])
        asked = []
        ok = backward(rules, goal, facts, asked)
        stem += f' Using backward chaining instead, explain whether the goal "{goal}" can be proved from the known facts.'
        ans += f'; backward chaining: "{goal}" ' + ('can be proved' if ok else 'cannot be proved') + (f' (missing facts that would be asked: {", ".join(dict.fromkeys(asked))})' if not ok and asked else '')
        key = key[:-len(f' [{m}]')] + f'; backward chaining result ({"proved" if ok else "not proved"}) with reasoning through the rules [2]. [{m + 2}]'
        m += 2
    return Q(stem, ans, key, marks=m, typ='numerical')


@t.add('C4', (3, 4, 5), 'multi_step')
def g12_rules(r, D):
    dom, rules, base = r.choice(RULESETS)
    d = ctx(r)
    i = r.randrange(len(rules))
    cond, cl = rules[i]
    stem = (f'{d["org"]} in {d["city"]} is building an expert system for {dom}. An expert says: "If ' + ' and '.join(cond) + f', then {cl}." '
            f'(a) Write this knowledge as a rule for the rules base. (b) Explain how the inference engine would use this rule in forward chaining. (c) Describe how the knowledge engineer would check that the rule is correct.')
    m = 6
    return Q(stem, f'(a) IF {" AND ".join(cond)} THEN {cl} (b) When all conditions are in the known facts, the rule fires and "{cl}" is added as a new fact, which may allow further rules to fire. (c) Discuss with experts, test with real cases and compare the system\'s conclusions with experts\' decisions.',
             f'(a) correct IF ... AND ... THEN form [2] (b) conditions matched against facts; rule fires; new fact added; may trigger other rules [2] (c) checked with experts / tested on cases with known outcomes [2]. [{m}]', marks=m, typ='multi_step')
finish(CHAPTERS)
