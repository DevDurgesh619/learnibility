#!/usr/bin/env python3
"""Generate the CBSE class 11 Legal Studies question bank (cbse-g11-legal-studies).

Fact tables per subtopic live in g11_legal_studies_a.py (chapters 1-6) and g11_legal_studies_b.py (chapters 7-12);
g12_hum_engine.py turns them into question families. Scenario (application) families below are added through
the engine's `extra` hook: each one describes a situation with Indian names and asks for the writ, court, law,
body or rule that applies; answers come from fixed, unambiguous scenario-answer tables.

Paper pattern (Legal Studies 074, 80 marks; class XII SQP layout used for class 11): 18 MCQ × 1 and 2
Assertion-Reason × 1, 8 × 2, 6 × 3, 2 case-based × 3, 4 long answers × 5 (40 questions, 80 marks).

Note: qbank.load_curriculum classifies an id as a subtopic when it contains '-st', which every id of this subject
does ('legal-studies'), so it loaded no chapters. A local loader is installed below; the framework fix is to test
for a trailing '-st<n>' with a regex instead.

Run: python3 scripts/questions/cbse/g11_legal_studies.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
from qbank import F, mcq  # noqa: E402
import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g11-legal-studies'
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (8, 2, 'short'), (6, 3, 'short3'), (2, 3, 'case'), (4, 5, 'long')]
DEFAULTS = {'long_marks': 5, 'case_marks': (1, 1, 1)}
S = 'cbse-g11-legal-studies-ch'


def _load_curriculum(sid, fallback=None):
    path = os.path.join(qbank.CUR_DIR, f'{sid}.json')
    with open(path) as fh:
        d = json.load(fh)
    st = {s['id']: s for s in d['subtopics']}
    chs = [{'id': c['id'], 'name': c['name'],
            'subtopics': [{'id': s, 'name': st[s]['name'], 'weight': st[s].get('weight', 'S')} for s in c['subtopicIds']]}
           for c in sorted(d['items'], key=lambda c: c['id'])]
    return {'chapters': chs, 'source': os.path.relpath(path, qbank.ROOT)}


qbank.load_curriculum = _load_curriculum

NAMES = ['Ravi', 'Meena', 'Arjun', 'Fatima', 'Suresh', 'Kavita', 'Imran', 'Priya', 'Harpreet', 'Anil', 'Lakshmi',
         'Joseph', 'Neha', 'Vikram', 'Sunita', 'Rahul', 'Ayesha', 'Deepak', 'Geeta', 'Manoj']
MALE = ['Ravi', 'Arjun', 'Suresh', 'Imran', 'Anil', 'Joseph', 'Vikram', 'Rahul', 'Deepak', 'Manoj']
FEMALE = ['Meena', 'Fatima', 'Kavita', 'Priya', 'Lakshmi', 'Neha', 'Sunita', 'Ayesha', 'Geeta']


def _fill(t, r):
    a, b = r.sample(NAMES, 2)
    return t.format(a=a, b=b, s1=r.choice(STATES), m=r.choice(MALE), f=r.choice(FEMALE))


def scenario(table, ask, why_word='because'):
    """table: list of (scenario template, answer, reason); answers are drawn from the same table as distractors."""
    answers = sorted({a for _, a, _ in table})

    def m(r):
        t, ans, why = r.choice(table)
        wrong = r.sample([x for x in answers if x != ans], 3)
        return mcq(f'{_fill(t, r)} {ask}', ans, wrong, f'{ans}, {why_word} {why}.', r)

    def x(r):
        t, ans, why = r.choice(table)
        return {'stem': f'{_fill(t, r)} {ask} Give a reason for your answer.',
                'answer': f'{ans}; {why}.', 'key': f'2 marks: 1 for {ans}, 1 for the reason ({why}).',
                'marks': 2, 'minutes': 3}
    return [F('C3', 'D2', 'mcq', m), F('C3', 'D3', 'explain', x, marks=2, minutes=3, gap='G3')]


WRITS = [
    ('{a} was arrested by the police and has been kept in custody for a week without being produced before a magistrate.',
     'Habeas corpus', 'it orders the authority to produce the detained person before the court and frees him if the detention is unlawful'),
    ('{a} has been held in a private house by relatives against {a}\'s will, and a friend, {b}, wants {a} released by the court.',
     'Habeas corpus', 'it lies against unlawful detention by the state or by a private person'),
    ('A municipal officer refuses, without any legal reason, to issue {a} a licence even though {a} meets every condition laid down by law.',
     'Mandamus', 'it commands a public authority to perform a public duty it is legally bound to perform'),
    ('A state board refuses to declare {a}\'s examination result although it is under a legal duty to do so.',
     'Mandamus', 'it commands a public authority to perform a public duty it is legally bound to perform'),
    ('A tribunal is hearing a dispute that lies outside its jurisdiction, and the case is still pending. {a} wants a higher court to stop it.',
     'Prohibition', 'it stops a lower court or tribunal from continuing a case beyond its jurisdiction while the case is pending'),
    ('A tribunal has already passed an order against {a} in a matter outside its jurisdiction. {a} wants the order quashed.',
     'Certiorari', 'it quashes an order already passed by a lower court or tribunal without jurisdiction or against law'),
    ('{a} has been appointed to a public office although {a} does not have the qualifications required by law. {b}, a citizen, challenges this.',
     'Quo warranto', 'it asks the person by what authority he holds a public office and removes him if he has no legal right to it'),
]

CIVCRIM = [
    ('{a} entered {b}\'s house at night and stole jewellery.', 'Criminal law', 'theft is an offence against society punished by the State'),
    ('{a} agreed to deliver 100 bags of rice to {b}\'s shop but did not deliver them, and {b} wants compensation.', 'Civil law', 'breach of contract is a private wrong remedied by damages'),
    ('{a} and {b} are brothers who disagree about how their late father\'s land should be divided.', 'Civil law', 'a dispute over property rights is a private matter decided by a civil court'),
    ('{a} attacked {b} with a rod during a quarrel and injured {b}.', 'Criminal law', 'causing hurt is an offence for which the State prosecutes and punishes'),
    ('{a}, a tenant, has not paid rent to the owner {b} for six months, and {b} wants the arrears.', 'Civil law', 'recovery of rent is a private claim for money'),
    ('{a} wants a divorce from a spouse on the ground of cruelty.', 'Civil law', 'matrimonial matters are private disputes decided by civil or family courts'),
    ('{a} cheated several people by collecting money for a fake job scheme.', 'Criminal law', 'cheating is an offence against society punished by the State'),
]

CUSTOM = [
    ('A practice in {a}\'s village began only five years ago and is now claimed to be a binding custom.',
     'Antiquity', 'a custom must have been followed for a long time'),
    ('A practice in {a}\'s community has been followed only now and then, with long breaks of many years.',
     'Continuity', 'a custom must have been observed without interruption'),
    ('{a} claims a custom that permits something that a valid Act of Parliament expressly forbids.',
     'Conformity with statute law', 'a custom cannot override a valid statute'),
    ('A claimed custom in {a}\'s area allows a creditor to make a debtor\'s child work for him until the debt is paid.',
     'Reasonableness and morality', 'a custom that is unreasonable, immoral or against public policy is not enforced'),
    ('{a} claims a custom whose terms are vague, and the villagers describe it differently each time.',
     'Certainty', 'a custom must be clear and definite'),
    ('A practice in {a}\'s area was followed only because a powerful landlord forced the villagers to obey it.',
     'Peaceable enjoyment', 'a custom must have been observed openly and peacefully, not by force'),
]

COURTS = [
    ('The Government of India and the state of {s1} have a legal dispute over their constitutional powers.',
     'Supreme Court – original jurisdiction (Article 131)', 'disputes between the Union and states lie only in the Supreme Court'),
    ('The President wants the Supreme Court\'s opinion on an important question of law before taking a decision.',
     'Supreme Court – advisory jurisdiction (Article 143)', 'the President may refer questions of law or fact of public importance to the Supreme Court'),
    ('{a} wants to challenge a state government order that violates a legal right given by a state Act but not a Fundamental Right.',
     'High Court – writ jurisdiction (Article 226)', 'a High Court can issue writs for any other purpose, while Article 32 is only for Fundamental Rights'),
    ('{a}\'s Fundamental Right to equality has been violated, and {a} wants to go directly to the highest court of the country.',
     'Supreme Court – writ jurisdiction (Article 32)', 'Article 32 lets a person move the Supreme Court directly for enforcing Fundamental Rights'),
    ('{a} is accused of murder, and the case is ready to be tried in the district.',
     'Court of Session', 'serious offences such as murder are tried by the Sessions Court of the district'),
    ('{a} wants to appeal to the Supreme Court against an order of a tribunal, although no regular appeal is provided by law.',
     'Supreme Court – special leave (Article 136)', 'Article 136 lets the Supreme Court grant special leave to appeal against any court or tribunal'),
]

ITOFF = [
    ('{a} secretly obtained {b}\'s net-banking password and used it to log in as {b}.', 'Section 66C (identity theft)',
     'fraudulently using another person\'s password or unique identification feature is identity theft'),
    ('{a} called people pretending to be a bank officer and, using a fake website, cheated them of money.', 'Section 66D (cheating by personation)',
     'cheating by pretending to be someone else using a computer resource is covered here'),
    ('{a} secretly captured and published images of the private area of {b} without consent.', 'Section 66E (violation of privacy)',
     'capturing or publishing images of a person\'s private area without consent violates privacy'),
    ('A group hacked into a power grid\'s control system to strike terror and threaten the security of India.', 'Section 66F (cyber terrorism)',
     'acts against computer resources to threaten the unity, security or sovereignty of India are cyber terrorism'),
    ('{a}, an employee, deliberately altered the source code of the company\'s software, which the law required to be kept.', 'Section 65 (tampering with source documents)',
     'knowingly altering or destroying computer source code required to be maintained is an offence'),
    ('{a} published obscene material on a website.', 'Section 67 (obscene material)',
     'publishing or transmitting obscene material in electronic form is an offence'),
]

CYBER = [
    ('{a} received an e-mail that looked like it came from a bank, asking for {a}\'s card number and OTP to be "verified" on a link.', 'Phishing',
     'fake messages from a trusted-looking source are used to steal personal or financial information'),
    ('{a} broke into the college\'s computer system without permission and changed records.', 'Hacking',
     'it is gaining unauthorised access to a computer system'),
    ('{a} keeps sending threatening messages to {b} on social media and tracks {b}\'s online activity.', 'Cyberstalking',
     'it is repeated use of electronic communication to harass and threaten a person'),
    ('A shop\'s computers were locked and its files encrypted; a message demanded payment to unlock them.', 'Ransomware attack',
     'malware encrypted the data and a ransom is demanded for its release'),
    ('A government website was flooded with fake traffic so that genuine users could not open it.', 'Denial of service attack',
     'the website was overloaded so that it could not serve genuine users'),
    ('{a} opened a social media account in {b}\'s name and photos and posted messages as {b}.', 'Identity theft',
     'another person\'s identity was used fraudulently'),
]

PERSONAL = [
    ('{m} and {f}, both Hindus, marry with Hindu rites.', 'Hindu Marriage Act, 1955', 'it governs marriages between Hindus'),
    ('{m}, a Jain, and {f}, a Buddhist, marry with the customary rites of one of them.', 'Hindu Marriage Act, 1955', 'it also applies to Jains, Buddhists and Sikhs'),
    ('{m}, a Hindu, and {f}, a Muslim, marry in a civil ceremony before a Marriage Officer without either changing religion.', 'Special Marriage Act, 1954', 'it allows a civil marriage between persons of any religion'),
    ('{m} and {f}, both Parsis, marry in a Parsi religious ceremony.', 'Parsi Marriage and Divorce Act, 1936', 'it governs marriage among Parsis'),
    ('{m} and {f}, both Christians, marry in a church.', 'Indian Christian Marriage Act, 1872', 'it governs marriage among Christians'),
]

JJ = [
    ('{a}, aged 15, is accused of stealing a mobile phone.', 'Juvenile Justice Board', 'it deals with children in conflict with law'),
    ('A seven-year-old child is found abandoned at a railway station.', 'Child Welfare Committee', 'it deals with children in need of care and protection'),
    ('A couple wants to adopt a child legally, and the adoption has to follow the official regulations.', 'Central Adoption Resource Authority', 'it is the statutory body that regulates adoption in India'),
    ('{a}, aged 17, is accused of a heinous offence, and the Board after preliminary assessment finds that the accused should be tried as an adult.', "Children's Court", 'the case is transferred to the Children\'s Court after the preliminary assessment'),
    ('An orphaned girl of twelve is found working as a domestic help and being beaten by her employer.', 'Child Welfare Committee', 'she is a child in need of care and protection'),
]

CHILDLAW = [
    ('A private unaided school refuses admission in class 1 to {a}\'s child from a poor family even though the 25% reserved seats are vacant.',
     'Right of Children to Free and Compulsory Education Act, 2009', 'it reserves 25% of entry-class seats in private unaided schools for disadvantaged children'),
    ('A 12-year-old boy is found employed in a fireworks factory.', 'Child and Adolescent Labour (Prohibition and Regulation) Act',
     'employment of children below 14 is prohibited'),
    ('A 10-year-old child is sexually abused by a neighbour.', 'Protection of Children from Sexual Offences Act, 2012',
     'it deals with sexual offences against any person below 18'),
    ('The parents of a 15-year-old girl arrange her marriage.', 'Prohibition of Child Marriage Act, 2006',
     'it fixes the marriageable age at 18 for females and 21 for males'),
]

STAGES_CIV = ['filing of the plaint', 'issue of summons', 'filing of the written statement', 'framing of issues',
              'evidence of the parties', 'final arguments', 'judgment and decree', 'execution of the decree']
STAGES_CRIM = ['registration of the FIR', 'investigation by the police', 'filing of the charge sheet', 'framing of the charge',
               'trial and examination of witnesses', 'judgment', 'sentence (if convicted)']


def stage_order(r):
    kind, st = r.choice([('civil suit', STAGES_CIV), ('criminal case', STAGES_CRIM)])
    idx = sorted(r.sample(range(len(st)), 4))
    right = [st[i] for i in idx]
    labels = ['I', 'II', 'III', 'IV']
    shown = right[:]
    r.shuffle(shown)
    code = lambda seq: ', '.join(labels[shown.index(x)] for x in seq)
    c = code(right)
    import itertools
    others = [code(list(p)) for p in itertools.permutations(right) if list(p) != right]
    wrong = r.sample(others, 3)
    stem = (f'Arrange the following stages of a {kind} in the correct order:\n'
            + '\n'.join(f'{labels[i]}. {x}' for i, x in enumerate(shown)))
    return mcq(stem, c, wrong, f'Correct order: {" → ".join(right)} ({c}).', r)


def standard_of_proof(r):
    t, ans, why = r.choice([
        ('{a} sues {b} for money due under a contract.', 'Preponderance of probabilities', 'it is a civil case'),
        ('{a} sues {b} for damage caused to {a}\'s car.', 'Preponderance of probabilities', 'it is a civil claim for compensation'),
        ('{a} is being tried for theft.', 'Proof beyond reasonable doubt', 'it is a criminal case'),
        ('{a} is being tried for causing grievous hurt to {b}.', 'Proof beyond reasonable doubt', 'it is a criminal case'),
    ])
    wrong = [w for w in ['Preponderance of probabilities', 'Proof beyond reasonable doubt', 'Proof beyond all possible doubt',
                         'No proof is needed'] if w != ans]
    return mcq(f'{_fill(t, r)} What standard of proof applies?', ans, wrong, f'{ans}, because {why}.', r)


STATES = ['Kerala', 'Punjab', 'Odisha', 'Karnataka', 'Bihar', 'Gujarat', 'Assam', 'Telangana']
EXTRA = {
    S + '10-st2': scenario(WRITS, 'Which writ is the most suitable remedy?') + scenario(COURTS, 'Which court or jurisdiction applies?'),
    S + '06-st2': scenario(CIVCRIM, 'Is this a matter of civil law or criminal law?'),
    S + '07-st1': scenario(CUSTOM, 'Which essential of a valid custom is NOT satisfied?'),
    S + '09-st2': scenario(ITOFF, 'Which provision of the IT Act, 2000 applies?'),
    S + '09-st1': scenario(CYBER, 'Which type of cybercrime is this?'),
    S + '11-st1': scenario(PERSONAL, 'Which law governs a marriage performed in this way?'),
    S + '12-st3': scenario(JJ, 'Which body or court will deal with this?'),
    S + '12-st2': scenario(CHILDLAW, 'Which law applies?'),
    S + '10-st4': [F('C3', 'D3', 'mcq', stage_order), F('C3', 'D2', 'mcq', standard_of_proof)],
}


def chapters():
    out = []
    for mod in ('g11_legal_studies_a', 'g11_legal_studies_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '9 random generated items per chapter (108 items), one full mock (40 items) and 16 scenario items re-solved '
              'by hand against the Constitution text, the named Acts and the NCERT/CBSE Legal Studies class 11 syllabus',
    'checked': 164,
    'mismatches': 2,
    'fixes': [
        'marriage scenarios now pair a male and a female name (random names had produced same-sex couples, which the '
        'Hindu Marriage Act and other personal laws do not cover)',
        'hand-written 4-mark items re-marked as 3 marks: the paper has no 4-mark section, so the key said "4 marks" '
        'for a 3-mark mock slot',
        'scenario stems no longer use he/she pronouns with randomly drawn names',
        'two near-identical reasons in ch06 civil and criminal law reworded so "best explains" options stay distinct',
    ],
}]

if __name__ == '__main__':
    E.run(SID, 'scripts/questions/cbse/g11_legal_studies.py', chapters(), MOCK_PATTERN, extra=EXTRA, accuracy=ACCURACY)
