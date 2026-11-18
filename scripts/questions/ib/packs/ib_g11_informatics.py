"""IB DP Digital Society SL/HL (first assessment 2024) – ib-g11-informatics (slug informatics), year 1.

Content pack for the QB-IB engine. Year 1 covers the inquiry process, the seven concepts (2.1 change,
2.2 expression, 2.3 identity, 2.4 power, 2.5 space, 2.6 systems, 2.7 values and ethics), content areas
3.1 data, 3.2 algorithms, 3.3 computers and 3.4 networks and the internet, and the seven contexts.
Items use IB command terms and real, correctly described examples (Cambridge Analytica, GDPR, India's
DPDP Act, Aadhaar, COMPAS, Gender Shades, the Dutch childcare-benefits scandal, Ofqual 2020, net
neutrality, internet shutdowns, M-Pesa, e-waste at Agbogbloshie, ...). Parametric items compute their
own answers (binary and file sizes, compression, search/sort traces, error rates, growth, packets).

Mock = one exam set mirroring examPattern in targets.json (paper marks there are UNVERIFIED; the
section marks below are fixed so every mock carries the same total):
  Paper 1 – two structured questions on a real-world example, parts (a) 2, (b) 4, (c) 6, (d) 8 marks
  Paper 2 – source-based: Q1 identify [2], Q2 explain with the source [4], Q3 compare and contrast two
            sources [6], Q4 evaluate using the sources and own knowledge [12]
  Paper 3 (HL) – intervention brief: Q1 explain the challenge [4], Q2 analyse impacts on stakeholders
            [6], Q3 evaluate the intervention and recommend [12] (abridged to three questions)
Mock-only templates return None outside their own section style.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names, CITIES  # noqa: F401

CONFIG = {'minutesPerMark': 1.8, 'mcqMinutes': 1.0}

P2_CHAPTERS = [3, 6, 8, 10, 12, 13]
P3_CHAPTERS = [6, 8, 10, 12]

MOCK = [
    dict(section='Paper 1 – Question (a) define / identify', count=2, c=['C1'], d=[2], type='short', marks=2, style='p1a'),
    dict(section='Paper 1 – Question (b) explain', count=2, c=['C2'], d=[3], type='explain', marks=4, style='p1b'),
    dict(section='Paper 1 – Question (c) analyse a real-world example', count=2, c=['C3'], d=[3], type='short', marks=6, style='p1c'),
    dict(section='Paper 1 – Question (d) evaluate', count=2, c=['C4'], d=[4], type='long', marks=8, style='p1d'),
    dict(section='Paper 2 – Q1 identify (source-based)', count=1, c=['C3'], d=[2], type='case', marks=2, style='p2q1', chapters=P2_CHAPTERS),
    dict(section='Paper 2 – Q2 explain with reference to a source', count=1, c=['C3'], d=[3], type='case', marks=4, style='p2q2', chapters=P2_CHAPTERS),
    dict(section='Paper 2 – Q3 compare and contrast two sources', count=1, c=['C4'], d=[3], type='case', marks=6, style='p2q3', chapters=P2_CHAPTERS),
    dict(section='Paper 2 – Q4 evaluate using sources and own knowledge', count=1, c=['C4'], d=[4], type='long', marks=12, style='p2q4', chapters=P2_CHAPTERS),
    dict(section='Paper 3 (HL) – Q1 explain the challenge', count=1, c=['C3'], d=[3], type='case', marks=4, style='p3q1', chapters=P3_CHAPTERS),
    dict(section='Paper 3 (HL) – Q2 analyse impacts on stakeholders', count=1, c=['C3'], d=[4], type='case', marks=6, style='p3q2', chapters=P3_CHAPTERS),
    dict(section='Paper 3 (HL) – Q3 evaluate and recommend', count=1, c=['C4'], d=[5], type='long', marks=12, style='p3q3', chapters=P3_CHAPTERS),
]

BANDS = ('Markbands (five bands, scaled to the marks available): top – focused on the question; accurate use of Digital '
         'Society concepts, content and contexts; specific, well-explained real-world examples; balanced analysis of '
         'impacts and implications for different stakeholders; a clear, well-supported conclusion. Upper-middle – relevant '
         'examples and some balance; conclusion reasoned. Middle – some relevant knowledge, partly descriptive; conclusion '
         'stated. Lower – limited, general knowledge, mainly descriptive. Bottom – minimal relevant material.')
BANDS_8 = ('Markbands [8]: 7–8 – well-developed evaluation of impacts/implications, specific real-world example(s), '
           'balanced and with a supported conclusion; 5–6 – evaluation with relevant example(s) but uneven balance; '
           '3–4 – some relevant points, mainly descriptive, conclusion asserted; 1–2 – limited, general response.')
BANDS_12 = ('Markbands [12]: 10–12 – sustained, balanced evaluation that integrates the sources/stimulus with specific own '
            'knowledge and Digital Society concepts, and reaches a well-supported conclusion; 7–9 – evaluation with relevant '
            'evidence and some balance; 4–6 – some analysis, mostly descriptive or one-sided; 1–3 – limited, general '
            'points with little evaluation.')
STYLE = {'eval_marks': 8, 'essay_marks': 12, 'markband': BANDS}

R = Registry()
P2: dict = {}    # 'chNN' -> dict(src=[(text, attribution, identify_q, [points], explain_q, explain_answer)], cmp=[...], ev=[...])
INTV: dict = {}  # 'chNN' -> [(intervention, extract, challenge, [stakeholder impacts], [strengths], [limitations], recommendation)]


def templates(st):
    return R.build(st, STYLE)


def lc(s):
    w = s.split(' ', 1)[0]
    if len(w) > 1 and (w[1].isupper() or w[1].isdigit()) or w in ('I',):
        return s
    return s[0].lower() + s[1:]


def _key(slot):
    return slot.subtopic['id'].rsplit('-', 2)[-2] + '-' + slot.subtopic['id'].rsplit('-', 1)[-1]


def _ch(slot):
    return slot.subtopic['id'].rsplit('-', 2)[-2]


def pc(x, dp=1):
    """Percentage / decimal formatting without trailing zeros."""
    s = f'{x:.{dp}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s

def sci(x, sig=3):
    """Readable large numbers: commas below a million, otherwise a × 10ⁿ."""
    sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    if abs(x) < 1e6:
        return f'{float(f"{x:.{sig}g}"):,g}'
    m, e = f'{x:.{sig - 1}e}'.split('e')
    m = m.rstrip('0').rstrip('.')
    return f'{m} × 10' + str(int(e)).translate(sup)



# =============================================================================================
# Assertion–Reason helper (chapterMix: MCQ / Assertion-Reason)
# =============================================================================================
AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.',
           'Both A and R are true, but R is not the correct explanation of A.',
           'A is true, but R is false.',
           'A is false, but R is true.']


def AR(key, items):
    """items: (assertion, reason, code a/b/c/d, explanation)."""
    def fn(rng, slot):
        a, r, code, why = rng.choice(items)
        ans = AR_OPTS['abcd'.index(code)]
        return dict(stem=f'Assertion (A): {a}\nReason (R): {r}\nChoose the correct option.', options=list(AR_OPTS),
                    answer=ans, markingKey=f'{"ABCD"["abcd".index(code)]}. {why}', type='mcq')
    R.t.setdefault(key, []).append(T('C2', (2, 3), fn, 'mcq', None, 'ar'))


# =============================================================================================
# Mock-only templates
# =============================================================================================
def _p1a(rng, slot):
    f = R.f.get(_key(slot))
    if slot.style != 'p1a' or not f or not f.terms:
        return None
    t, d = rng.choice(f.terms)
    stem = rng.choice([f'Paper 1 – Question (a). Define the term "{t}". [2]',
                       f'Paper 1 – Question (a). Outline what is meant by "{t}" in the context of digital society. [2]'])
    return dict(stem=stem, answer=d[0].upper() + d[1:], type='short', marks=2,
                markingKey=f'{d[0].upper() + d[1:]}. 2 marks for a clear definition that includes the defining feature; 1 mark for a partial or vague definition.')


def _p1b(rng, slot):
    f = R.f.get(_key(slot))
    if slot.style != 'p1b' or not f or not f.why:
        return None
    q, a = rng.choice(f.why)
    return dict(stem=f'Paper 1 – Question (b). {q} [4]', answer=a, type='explain', marks=4,
                markingKey=f'{a} Award up to 4 marks: 1 mark per relevant point, up to 2 further marks for developing the explanation (cause → effect) and for a relevant example.')


def _p1c(rng, slot):
    f = R.f.get(_key(slot))
    if slot.style != 'p1c' or not f or not f.cases:
        return None
    case, what, concept, how = rng.choice(f.cases)
    return dict(stem=f'Paper 1 – Question (c). Real-world example: {what}\n\nAnalyse how this example illustrates {concept}. [6]',
                answer=how[0].upper() + how[1:], type='short', marks=6,
                markingKey=f'{how[0].upper() + how[1:]} 5–6: analysis that links specific features of the example to the concept and considers impacts on more than one stakeholder; 3–4: relevant explanation, partly developed; 1–2: description of the example with little analysis.')


def _p1d(rng, slot):
    f = R.f.get(_key(slot))
    if slot.style != 'p1d' or not f or not f.evaluate:
        return None
    claim, pro, con, judge = rng.choice(f.evaluate)
    stem = rng.choice([f'Paper 1 – Question (d). With reference to a real-world example you have studied, evaluate the claim that {lc(claim)} [8]',
                       f'Paper 1 – Question (d). "{claim}" Using a specific real-world example, discuss this view. [8]'])
    return dict(stem=stem, answer=judge, type='long', marks=8,
                markingKey='Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) + f'. Possible conclusion: {judge} ' + BANDS_8)


LAB = 'ABCD'


def _blk(ch, i):
    s = P2[ch]['src'][i]
    return f'Source {LAB[i]}\n{s[0]}\n— {s[1]}'


def _p2q1(rng, slot):
    ch = _ch(slot)
    if slot.style != 'p2q1' or ch not in P2:
        return None
    i = rng.randrange(len(P2[ch]['src']))
    s = P2[ch]['src'][i]
    return dict(stem=f'Paper 2 – Question 1. Read Source {LAB[i]}.\n\n{_blk(ch, i)}\n\n{s[2].replace("{S}", "Source " + LAB[i])} [2]',
                answer='; '.join(s[3]), type='case', marks=2, gap='G7',
                markingKey='Award 1 mark for each of the following, up to 2 marks: ' + '; '.join(s[3]) + '. Points must come from the source; accept close paraphrase.')


def _p2q2(rng, slot):
    ch = _ch(slot)
    if slot.style != 'p2q2' or ch not in P2:
        return None
    i = rng.randrange(len(P2[ch]['src']))
    s = P2[ch]['src'][i]
    return dict(stem=f'Paper 2 – Question 2. Read Source {LAB[i]}.\n\n{_blk(ch, i)}\n\n{s[4].replace("{S}", "Source " + LAB[i])} [4]',
                answer=s[5], type='case', marks=4, gap='G7',
                markingKey=f'{s[5]} 3–4 marks: clear explanation with explicit reference to the source; 1–2 marks: limited explanation or quotation without explanation.')


def _p2q3(rng, slot):
    ch = _ch(slot)
    if slot.style != 'p2q3' or ch not in P2:
        return None
    i, j, focus, sims, diffs = rng.choice(P2[ch]['cmp'])
    return dict(stem=f'Paper 2 – Question 3. Read Sources {LAB[i]} and {LAB[j]}.\n\n{_blk(ch, i)}\n\n{_blk(ch, j)}\n\n'
                     f'Compare and contrast what Source {LAB[i]} and Source {LAB[j]} reveal about {focus}. [6]',
                answer='Similarities: ' + '; '.join(sims) + '. Differences: ' + '; '.join(diffs) + '.', type='case', marks=6, gap='G7',
                markingKey='Similarities: ' + '; '.join(sims) + '. Differences: ' + '; '.join(diffs) +
                '. 1 mark per valid, source-referenced point (up to 6). If only similarities or only differences are given, maximum 3 marks. Reward a running comparison.')


def _p2q4(rng, slot):
    ch = _ch(slot)
    if slot.style != 'p2q4' or ch not in P2:
        return None
    i, j, claim, pro, con = rng.choice(P2[ch]['ev'])
    return dict(stem=f'Paper 2 – Question 4. Read Sources {LAB[i]} and {LAB[j]}.\n\n{_blk(ch, i)}\n\n{_blk(ch, j)}\n\n'
                     f'Using the sources and your own knowledge, evaluate the claim that {claim} [12]',
                answer='Supporting: ' + '; '.join(pro) + '. Challenging: ' + '; '.join(con) + '.', type='long', marks=12, gap='G5',
                markingKey='Supporting: ' + '; '.join(pro) + '. Challenging: ' + '; '.join(con) + '. ' + BANDS_12 +
                ' Responses that use only the sources or only own knowledge cannot reach the top band.')


def _intv(rng, slot, style):
    ch = _ch(slot)
    if slot.style != style or ch not in INTV:
        return None
    return rng.choice(INTV[ch])


def _p3q1(rng, slot):
    it = _intv(rng, slot, 'p3q1')
    if not it:
        return None
    title, ext, chal, sh, pro, con, rec = it
    return dict(stem=f'Paper 3 – Question 1. Read the extract from the intervention brief.\n\n{ext}\n\nExplain the challenge that {title} is intended to address. [4]',
                answer=chal, type='case', marks=4, gap='G7',
                markingKey=f'{chal} 1 mark for identifying the challenge; up to 3 marks for explaining its causes and who is affected, with reference to the extract.')


def _p3q2(rng, slot):
    it = _intv(rng, slot, 'p3q2')
    if not it:
        return None
    title, ext, chal, sh, pro, con, rec = it
    return dict(stem=f'Paper 3 – Question 2. Read the extract from the intervention brief.\n\n{ext}\n\nAnalyse the impact of {title} on two different stakeholders. [6]',
                answer='; '.join(sh), type='case', marks=6, gap='G5',
                markingKey='Possible stakeholder impacts: ' + '; '.join(sh) + '. Up to 3 marks per stakeholder: identification (1), analysis of the impact (1), link to the extract or own knowledge (1).')


def _p3q3(rng, slot):
    it = _intv(rng, slot, 'p3q3')
    if not it:
        return None
    title, ext, chal, sh, pro, con, rec = it
    return dict(stem=f'Paper 3 – Question 3. Read the extract from the intervention brief.\n\n{ext}\n\nEvaluate {title} as a response to this challenge and recommend one further step that could improve it. [12]',
                answer=rec, type='long', marks=12, gap='G5',
                markingKey='Strengths: ' + '; '.join(pro) + '. Limitations: ' + '; '.join(con) + f'. Possible recommendation: {rec} ' + BANDS_12 +
                ' A recommendation must be justified with reference to stakeholders and feasibility for the top band.')


BANK_ESSAY = [
    '"{C}" How far do you agree? Refer to at least one Digital Society concept in your answer.',
    'With reference to two real-world examples, discuss the claim that {c}',
]


def _bank_essay(rng, slot):
    f = R.f.get(_key(slot))
    if slot.style or not f or not f.evaluate:
        return None
    claim, pro, con, judge = rng.choice(f.evaluate)
    stem = rng.choice(BANK_ESSAY).format(c=lc(claim), C=claim)
    m = 12 if slot.d >= 5 else 8
    key = ('Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) +
           f'. Supported judgement: {judge} ' + (BANDS_12 if m == 12 else BANDS_8))
    return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=m, gap='G5')


MOCK_T = [(_p1a, 'C1', 'p1a', 'short', (2, 2)), (_p1b, 'C2', 'p1b', 'explain', (3, 3)), (_p1c, 'C3', 'p1c', 'short', (3, 3)),
          (_p1d, 'C4', 'p1d', 'long', (4, 4)), (_p2q1, 'C3', 'p2q1', 'case', (2, 2)), (_p2q2, 'C3', 'p2q2', 'case', (3, 3)),
          (_p2q3, 'C4', 'p2q3', 'case', (3, 3)), (_p2q4, 'C4', 'p2q4', 'long', (4, 4)), (_p3q1, 'C3', 'p3q1', 'case', (3, 3)),
          (_p3q2, 'C3', 'p3q2', 'case', (4, 4)), (_p3q3, 'C4', 'p3q3', 'long', (5, 5))]
_DONE = []


def init(subject_id):
    if _DONE:
        return
    _DONE.append(1)
    for key in list(R.f):
        for fn, c, sty, ty, d in MOCK_T:
            R.add(key, c, d, ty, style=sty)(fn)
        R.add(key, 'C4', (4, 5), 'long')(_bank_essay)


# =============================================================================================
# Parametric helpers
# =============================================================================================
def pct_change(a, b):
    return (b - a) / a * 100


# =============================================================================================
# ch01 Introduction to Digital Society and the inquiry process
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('digital society', 'the study of how digital systems and technologies interact with people, communities and societies, and the impacts and implications of those interactions'),
           ('digital system', 'a set of interacting components – hardware, software, data, networks and people – that processes information in digital (binary) form to achieve a purpose'),
           ('stakeholder', 'a person, group or organisation that affects, or is affected by, a digital system or decision about it'),
           ('impact', 'a direct effect of a digital system on people or communities, such as a change in how they work, learn or communicate'),
           ('implication', 'a wider or longer-term consequence that follows from an impact, often for values, rights or social structures'),
           ('online community', 'a group of people who interact regularly through a digital platform around a shared interest, identity or purpose')],
    facts=[('Which of the following is one of the seven key concepts of the IB Digital Society course?', 'Expression',
            ['Sovereignty', 'Scarcity', 'Evolution'], 'The concepts are change, expression, identity, power, space, systems, and values and ethics.'),
           ('Which of the following best describes the structure of the Digital Society course?', 'Concepts, content and contexts studied through an inquiry process',
            ['Programming, databases and networking studied through coding projects', 'Media studies only, analysed through film theory', 'Hardware engineering studied through laboratory practicals'],
            'The guide combines concepts (2.1–2.7), content (3.1–3.7) and contexts (4.1–4.7), with HL challenges and interventions.'),
           ('Which of the following is a content area of the Digital Society course?', 'Robots and autonomous technologies',
            ['Supply and demand', 'Cell biology', 'International relations theory'], 'The content areas are data, algorithms, computers, media, networks and the internet, AI, and robots and autonomous technologies.'),
           ('Which of the following is an example of a digital system rather than a single device?', "India's Unified Payments Interface (UPI) connecting banks, apps and users",
            ['A single USB memory stick', 'A printed bus timetable', 'A calculator with no connectivity'], 'UPI links apps, bank servers, networks, data and people to move money instantly.')],
    why=[('Explain why Digital Society studies people and communities as well as technologies.', 'Digital systems only have meaning through how people design, use and are affected by them; the same technology (e.g. WhatsApp) can strengthen family ties in one context and spread rumours that lead to violence in another, so impacts depend on people, values and contexts, not the device alone.'),
         ('Explain why the same digital system can have different impacts for different stakeholders.', 'Stakeholders have different interests, power and access: a ride-hailing app gives passengers convenience and drivers flexible income but also exposes drivers to algorithmic pay changes and gives the platform data and control, so one system creates winners and losers.'),
         ('Explain why it is useful to distinguish between impacts and implications when studying a digital system.', 'Impacts are immediate effects (e.g. video calls replace face-to-face lessons) while implications are wider, longer-term consequences (e.g. deepening inequality for students without devices); separating them helps an inquiry move from description to evaluation of significance.')],
    contrast=[('a digital system', 'a digital device', 'A device is a single piece of hardware (e.g. a smartphone); a digital system is the wider set of interacting hardware, software, data, networks and people that the device is part of (e.g. a mobile-money network such as M-Pesa).'),
              ('an impact', 'an implication', 'An impact is a direct effect of a digital system (e.g. faster banking through an app); an implication is a broader or longer-term consequence that follows (e.g. branch closures that exclude elderly people without smartphones).')],
    misc=[('Digital Society is mainly a course about learning to program computers.', 'Digital Society focuses on the impacts and implications of digital systems for people and communities; technical content (data, algorithms, networks) is studied so that its social effects can be analysed, not to write code.'),
          ('A digital technology has the same effect wherever it is used.', 'Impacts depend on context – political, economic, cultural – and on who uses it; social media helped organise protests in the Arab Spring but has also been used by governments for surveillance and propaganda.')],
    cases=[('M-Pesa in Kenya', 'Safaricom launched the M-Pesa mobile-money service in 2007, letting people send and store money by SMS on basic phones; it is now used by most Kenyan adults.', 'how a digital system interacts with people and communities',
            'it combines phones, the mobile network, agents and user trust to give unbanked people access to payments, changing household finance and small business in a way a single device could not.'),
           ("India's Unified Payments Interface (UPI)", 'UPI, launched in 2016 by the National Payments Corporation of India, lets users pay instantly by scanning QR codes; it processes billions of transactions each month.', 'the impact of a digital system on everyday life',
            'street vendors and large retailers alike accept instant payments, which reduces cash use and creates digital transaction records with implications for tax, credit and privacy.'),
           ('the move to online schooling during COVID-19', 'In 2020 school closures affected over 1.5 billion learners worldwide (UNESCO), and many systems moved lessons to video-conferencing and learning platforms.', 'how impacts differ between stakeholders',
            'students with devices and broadband continued learning, while those without access fell behind, showing that the same digital system had unequal impacts and long-term implications for educational inequality.')],
    sources=[('"For many of our members, the WhatsApp group is the village square: births, funerals and job offers are shared there first. But when a false rumour about child kidnappers spread in 2018, the same groups carried it to thousands of phones within hours."', 'Community worker in Maharashtra, India, interviewed for a 2019 report on messaging apps',
              'With reference to the source, explain one positive and one negative impact of messaging apps on communities.', 'Positive: groups act as a community hub, spreading news of births, funerals and jobs quickly. Negative: the same speed and reach spread a false kidnapping rumour widely in hours (such rumours were linked to mob attacks in India in 2018).'),
             ('"Digital technologies are neither good nor bad; nor are they neutral."', "Melvin Kranzberg, historian of technology, first law of technology (1986)",
              'Explain what the source suggests about how Digital Society students should study technology.', 'The source suggests technologies have real effects (they are not neutral) but those effects depend on context and use, so students should analyse specific impacts on specific people rather than labelling a technology simply good or bad.')],
    evaluate=[('The benefits of digital systems are shared equally by everyone in a society.',
               ['basic services such as mobile money and UPI have reached people previously excluded from banking', 'free platforms (search, messaging) lower the cost of information for all'],
               ['access, skills and affordability differ by income, gender, age and location', 'platform owners capture much of the value and data', 'some groups bear the harms (surveillance, misinformation, job loss)'],
               'Benefits are widespread but unevenly distributed; who gains depends on access, skills and power, so equality of benefit is not automatic.'),
              ('Studying the impacts of a digital system is more important than understanding how it works.',
               ['Digital Society is concerned with consequences for people and communities', 'stakeholders and policymakers need to judge impacts to act'],
               ['without understanding how a system works (data, algorithms) students cannot explain why impacts occur', 'technical misunderstandings lead to weak interventions'],
               'Both are needed: understanding how a system works explains its impacts, and impacts give that knowledge its significance.')],
    extended=[('Using one digital system you have studied, analyse its impacts on two different stakeholders and discuss one implication for the wider society.', 'Choose a specific system (e.g. M-Pesa, UPI, a ride-hailing platform); identify two stakeholders (e.g. users and small traders, or drivers and the platform); analyse a specific impact for each with evidence; then discuss one broader implication (e.g. financial inclusion, data concentration). Reward specific detail and balance.', 6, 'long')],
))

R.facts('ch01-st2', F(
    terms=[('inquiry process', 'the cycle of exploring, investigating, reflecting and sharing that Digital Society students use to study real-world digital systems'),
           ('inquiry focus', 'a clear, specific statement of what an inquiry will investigate about a digital system and its impacts on people and communities'),
           ('exploring', 'the inquiry stage in which students identify a real-world example, raise questions and narrow down a focus'),
           ('investigating', 'the inquiry stage in which students gather, analyse and evaluate sources and evidence from different perspectives'),
           ('reflecting', 'the inquiry stage in which students consider what they have learned, the limitations of their evidence and the ethical issues raised'),
           ('sharing', 'the inquiry stage in which students communicate their findings to an audience, for example in a multimedia presentation'),
           ('guiding question', 'an open question that directs an inquiry, for example "How has facial recognition changed policing in London?"')],
    facts=[('Which of the following lists the four stages of the Digital Society inquiry process?', 'Exploring, investigating, reflecting and sharing',
            ['Planning, coding, testing and evaluating', 'Observing, hypothesising, experimenting and concluding', 'Defining, designing, building and launching'],
            'Sections 1.1–1.4 of the guide set out exploring, investigating, reflecting and sharing.'),
           ('Which of the following is the best example of a focused inquiry question?', 'How has the use of live facial recognition by London police affected trust among young people?',
            ['Is technology good or bad?', 'What is the internet?', 'How do computers work?'], 'A good focus names a specific system, place and impact on a specific group.'),
           ('At which stage of the inquiry process would a student consider the limitations of their sources and the ethical issues raised?', 'Reflecting',
            ['Exploring', 'Sharing', 'Coding'], 'Reflecting looks back critically at evidence, perspectives and ethics.'),
           ('Which of the following is the IB Digital Society internal assessment?', 'An inquiry project presented as a multimedia presentation',
            ['A timed programming exam', 'A laboratory practical', 'An oral examination on a novel'], 'The IA is an inquiry into a real-world digital system shared as a multimedia presentation.')],
    why=[('Explain why the inquiry process is described as a cycle rather than a straight line.', 'Findings while investigating often raise new questions, which send students back to explore or refocus, and reflection can change how findings are shared; so the stages repeat and feed into each other rather than happening once in order.'),
         ('Explain why narrowing an inquiry focus improves the quality of an investigation.', 'A narrow focus (one system, one place, one group) lets students find specific evidence, compare perspectives in depth and evaluate impacts precisely, whereas a broad topic (e.g. "social media") leads to generalisations and descriptive answers.'),
         ('Explain why reflecting is an important stage of the inquiry process.', 'Reflection lets students recognise gaps or bias in their evidence, consider ethical issues (e.g. consent of interviewees), and judge the significance of findings, which turns a description into a critical, balanced conclusion.')],
    contrast=[('exploring', 'investigating', 'Exploring is about identifying a real-world example and forming a focus and questions; investigating is about systematically gathering and analysing evidence from different sources and perspectives to answer them.'),
              ('a broad topic', 'an inquiry focus', 'A broad topic names a general area (e.g. "AI in schools"); an inquiry focus states a specific system, context and impact to investigate (e.g. "How has an AI essay-feedback tool changed writing practices at one school in Lisbon?").')],
    misc=[('The inquiry process ends once you have collected enough sources.', 'Collecting sources is only part of investigating; students must also analyse and evaluate them, reflect on limitations and ethics, and share findings with an audience.'),
          ('A good inquiry question should be as broad as possible so that more information can be found.', 'Broad questions produce general, descriptive answers; a focused question about a specific digital system and stakeholder allows depth and evaluation.')],
    cases=[("a student inquiry into Singapore's TraceTogether app", 'TraceTogether was a Bluetooth contact-tracing app and token used in Singapore from 2020; in 2021 the government admitted its data could be accessed by police for serious criminal investigations, then legislated to limit this.', 'how an inquiry can move between exploring and investigating',
            'an initial exploration of contact tracing leads to a focused question on trust and privacy, and new evidence (the police-access revelation) sends the inquiry back to refocus – showing the cycle.'),
           ('an inquiry into food-delivery riders in Bogotá', 'Riders for platforms such as Rappi in Colombia have protested about pay and safety, while the platform argues that flexible work benefits riders and customers.', 'the importance of investigating different perspectives',
            'a balanced investigation would compare rider interviews, company statements and government data, rather than relying on one perspective, before reaching a conclusion.'),
           ("an inquiry into Wikipedia's coverage of women scientists", 'Studies have found that a minority of English Wikipedia biographies are about women; projects such as edit-a-thons and Women in Red have tried to close the gap.', 'how reflecting and sharing can lead to action',
            'reflecting on why the gap exists (editor demographics, notability rules) leads to sharing findings that may encourage interventions such as edit-a-thons.')],
    sources=[('"Our guiding question changed three times. We began with \'Is TikTok bad for teenagers?\', which was impossible to answer. We ended with \'How has TikTok\'s For You feed changed how students at our school discover music?\' – and then we could actually gather evidence."', 'Reflection by an IB Digital Society student, school blog, 2024',
              'With reference to the source, explain why the student changed their guiding question.', 'The first question was too broad and value-laden to answer with evidence; the final question names a specific system (the For You feed), group (students at one school) and impact (music discovery), so evidence could be collected and evaluated.'),
             ('"Data collection involving people must respect their informed consent and privacy. Anonymise interview data and do not publish identifiable images of minors."', 'School research ethics guidance for the Digital Society inquiry project',
              'Explain which stage of the inquiry process this guidance is most relevant to and why.', 'Mainly investigating (when collecting primary data from people) and reflecting (considering ethics); it ensures research is ethical and protects participants, which also affects how findings can be shared.')],
    evaluate=[('A personal, primary investigation is always more valuable than secondary sources in a Digital Society inquiry.',
               ['primary data (interviews, surveys) can capture local impacts not reported elsewhere', 'it gives direct insight into stakeholder perspectives'],
               ['small samples may not be representative', 'secondary sources (reports, academic studies) give scale and context', 'primary research raises ethical and time constraints'],
               'Primary evidence adds originality and local depth, but it is most valuable when combined with credible secondary sources that provide scale and context.'),
              ('The most important stage of the inquiry process is sharing findings with an audience.',
               ['communication makes the inquiry useful to others and may prompt action', 'the IA is assessed through a presentation'],
               ['sharing weak or biased findings is of little value', 'investigation and reflection determine the quality of what is shared'],
               'Sharing gives an inquiry impact, but its value depends on rigorous investigation and honest reflection earlier in the cycle.')],
    extended=[('A student wants to investigate "social media and politics". Using the inquiry process, explain how they should refine this topic into a focused inquiry and plan their investigation.', 'Exploring: choose a specific system and context (e.g. TikTok political content in the 2024 Indonesian election) and write a guiding question; investigating: identify a range of sources (platform reports, news, academic studies, interviews) and perspectives (voters, campaigners, regulators); reflecting: plan to assess bias, limitations and ethics; sharing: choose a format and audience. Reward a specific focus and a coherent plan.', 6, 'long')],
))

R.facts('ch01-st3', F(
    terms=[('claim', 'a statement presented as true that needs to be supported by evidence and reasoning'),
           ('perspective', 'the point of view from which a stakeholder interprets a digital system or issue, shaped by their interests, values and experience'),
           ('primary source', 'an original, first-hand record or piece of evidence, such as an interview, a company transparency report or a dataset'),
           ('secondary source', 'a source that interprets or analyses primary evidence, such as a news analysis or an academic review'),
           ('bias', 'a one-sided presentation or selection of evidence that favours a particular perspective or interest'),
           ('corroboration', 'checking whether a claim is supported by other independent and reliable sources'),
           ('peer review', 'the evaluation of research by independent experts in the same field before it is published')],
    facts=[('Which of the following is the best first step when checking a surprising claim about technology seen on social media?', 'Read laterally: open other tabs to see what independent, reliable sources say about the claim and its source',
            ['Share it so that others can decide', 'Check whether the post has many likes', 'Read the whole post carefully several times before searching elsewhere'],
            'Stanford History Education Group research found professional fact-checkers read laterally rather than staying on the page.'),
           ('Which of the following is an example of a primary source for an inquiry into content moderation?', "Meta's Community Standards Enforcement Report",
            ['A newspaper editorial about Meta', 'A textbook chapter on social media', 'A podcast summary of other reports'], 'Company transparency reports are first-hand data published by the platform.'),
           ('In the CRAAP test for evaluating sources, what does the second "A" stand for?', 'Accuracy',
            ['Accessibility', 'Algorithm', 'Audience'], 'CRAAP = Currency, Relevance, Authority, Accuracy, Purpose.'),
           ('Which of the following would most likely reduce the reliability of a report on the safety of a smart-home device?', 'It was funded and published by the company that sells the device',
            ['It cites independent laboratory tests', 'It was peer reviewed', 'It includes its methodology and data'], 'A conflict of interest may bias the selection and presentation of evidence.')],
    why=[('Explain why a source can be useful even if it is biased.', 'A biased source still reveals the perspective, interests and arguments of a stakeholder (e.g. a tech company blog shows how the firm justifies its product), which is valuable evidence when compared with other perspectives, as long as its limitations are recognised.'),
         ('Explain why claims about digital technology should be corroborated.', 'Claims spread quickly online and may be exaggerated, out of context or deliberately false; checking them against independent, reliable sources reduces the risk of building an argument on misinformation.'),
         ('Explain why the date of a source matters when evaluating claims about digital technology.', 'Digital systems, laws and usage change rapidly (e.g. platform policies, AI capabilities), so an older source may describe a situation that no longer applies; currency affects relevance and accuracy.')],
    contrast=[('a primary source', 'a secondary source', 'A primary source is first-hand evidence (e.g. a government dataset, an interview with a gig worker); a secondary source interprets or analyses such evidence (e.g. a journalist\'s article summarising several studies).'),
              ('a claim', 'evidence', 'A claim is an assertion that something is true (e.g. "smartphones harm teenagers\' sleep"); evidence is the data or testimony used to support or challenge it (e.g. results of a sleep study).')],
    misc=[('If a website looks professional and has a .org address, its claims must be reliable.', 'Design and domain names say little about reliability; anyone can register a .org domain, so authority, evidence, purpose and corroboration must be checked.'),
          ('A source with a clear perspective is useless for an inquiry.', 'Perspective-driven sources show how stakeholders see an issue; they are useful if their purpose is identified and they are compared with other sources.')],
    cases=[('the 2018 MIT study of false news on Twitter', 'Vosoughi, Roy and Aral (Science, 2018) studied about 126,000 rumour cascades and found that false news spread farther, faster and more broadly than true news, partly because it was more novel.', 'why claims online need careful evaluation',
            'because false claims reached people faster than corrections, users and researchers cannot rely on popularity as a sign of truth and must check sources and corroborate.'),
           ("Meta's transparency reports", 'Meta regularly publishes Community Standards Enforcement Reports with figures on content removed and the share found by its own systems before users reported it.', 'the value and limitations of primary sources',
            'they provide first-hand data at a scale no outsider could collect, but they are produced by the company itself and use its own definitions, so their figures should be corroborated by independent research.'),
           ('the "Pope in a puffer jacket" image (2023)', 'In March 2023 an AI-generated image of Pope Francis in a white puffer jacket, made with Midjourney, spread widely and was believed by many to be a real photograph.', 'the need to verify visual sources',
            'even realistic images can be synthetic, so students should check the origin of an image (reverse image search, credible reporting) before using it as evidence.')],
    sources=[('"Our app reduced screen time by 37% among teenage users in a 4-week trial."', 'Press release from the company that makes the screen-time app, 2024',
              'Identify two questions you would ask to evaluate the reliability of this claim.', 'For example: Who conducted and funded the trial (the company itself – conflict of interest)? How many participants were there and how were they chosen? Was there a control group? Is the data or method published and independently verified? Over what period was it measured?'),
             ('"A lie can travel halfway around the world while the truth is putting on its shoes."', 'Saying commonly misattributed to Mark Twain; versions date back to the 18th century',
              'Explain how this source itself illustrates a problem with evaluating claims.', 'The quotation is widely shared with a false attribution to Twain; it shows how easily claims (even about sources) are repeated without checking, so attribution and origin must be verified.')],
    evaluate=[('Professional journalism is always more reliable than social media as a source for a Digital Society inquiry.',
               ['journalists follow editorial standards, fact-checking and corrections', 'named authors and organisations can be held accountable'],
               ['social media can provide first-hand evidence from places journalists cannot reach (e.g. protests)', 'news organisations can also have bias and commercial pressures', 'reliability depends on the specific source, not the medium'],
               'Professional journalism is usually more reliable, but reliability must be judged source by source; social media can be valuable primary evidence if verified.'),
              ('Evaluating sources is now impossible because AI can fake any text, image or video.',
               ['generative AI makes convincing fake images, voices and documents cheaply', 'detection tools are unreliable'],
               ['lateral reading, provenance checks and corroboration still work', 'content credentials (C2PA) and trusted outlets help verify origin', 'most claims can be traced to accountable sources'],
               'AI makes evaluation harder and more important, but not impossible: verifying provenance and corroborating claims remain effective.')],
    extended=[('Two sources disagree about whether a city\'s smart-camera system has reduced crime: a council press release and a report by a civil liberties group. Explain how you would evaluate these sources and reach a conclusion.', 'Consider origin, purpose and possible bias of each (council promoting its policy; NGO campaigning on privacy); examine evidence quality (data, time period, methods, comparison areas); look for independent corroboration (police statistics, academic studies); recognise each perspective\'s value; reach a qualified conclusion based on the strongest evidence.', 6, 'long')],
))

# =============================================================================================
# ch02 Concepts 2.1–2.2: change and expression
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('disruptive innovation', 'an innovation that starts in a small or low-end market and eventually displaces established products, firms or practices (Clayton Christensen, 1997)'),
           ('causality', 'the relationship between a cause and its effect; in Digital Society, how a digital system leads to a change, often alongside other factors'),
           ('transformation', 'a deep, lasting change in how people, organisations or societies function, rather than a small improvement'),
           ('innovation', 'the introduction of a new or significantly improved product, process or way of doing things'),
           ('technological determinism', 'the view that technology is the main driver of social change, shaping society in largely predictable ways'),
           ('diffusion of innovations', 'the process by which an innovation spreads through a population over time, through groups from innovators to laggards (Everett Rogers, 1962)')],
    facts=[('Which of the following companies invented the first digital camera in 1975 but later filed for bankruptcy in 2012?', 'Kodak',
            ['Nokia', 'Polaroid', 'Sony'], 'Kodak engineer Steve Sasson built a digital camera in 1975; Kodak was slow to shift from film and filed for Chapter 11 in 2012.'),
           ("In Everett Rogers' diffusion of innovations model, what approximate share of adopters are 'innovators'?", '2.5%',
            ['13.5%', '34%', '16%'], 'Rogers: innovators 2.5%, early adopters 13.5%, early majority 34%, late majority 34%, laggards 16%.'),
           ('In which year did Encyclopaedia Britannica announce it would stop printing its encyclopaedia?', '2012',
            ['2001', '1995', '2020'], 'After 244 years in print, Britannica went online-only in 2012, partly due to competition from Wikipedia (2001).'),
           ('Which of the following is the best example of disruptive change caused by a digital system?', 'Streaming services replacing video rental shops',
            ['A faster model of an existing laptop', 'A new colour for a smartphone', 'A software update that fixes a bug'], 'Streaming (e.g. Netflix) displaced rental chains such as Blockbuster, which filed for bankruptcy in 2010.')],
    why=[('Explain why it is difficult to prove that a digital technology alone caused a social change.', 'Social changes have multiple interacting causes – economic, political, cultural – so a technology is usually one factor among many (e.g. social media in the Arab Spring alongside unemployment, food prices and repression); correlation in time does not prove causation.'),
         ('Explain why disruptive innovations often succeed against established firms.', 'Established firms focus on their most profitable customers and existing technology, so they ignore cheaper or simpler innovations that start in niche markets; as the innovation improves it captures mainstream customers (e.g. digital photography and Kodak).'),
         ('Explain why change caused by digital systems can be both incremental and transformative.', 'Some changes are small improvements to existing practices (e.g. faster processors), while others reshape whole sectors and behaviours (e.g. smartphones transforming banking, maps and communication); the same technology can begin incrementally and become transformative as it diffuses.')],
    contrast=[('incremental change', 'transformative change', 'Incremental change improves an existing process step by step (e.g. a faster checkout system); transformative change fundamentally alters how something is done or who does it (e.g. e-commerce reshaping retail and city centres).'),
              ('technological determinism', 'the social shaping of technology', 'Technological determinism holds that technology drives social change; the social shaping view argues that people, values, markets and politics shape how technologies are designed, adopted and used.')],
    misc=[('The internet caused the Arab Spring.', 'Social media helped protesters organise and spread images, but the uprisings had deep political and economic causes (authoritarian rule, unemployment, corruption); the internet was a contributing tool, not the sole cause.'),
          ('Every innovation is a disruptive innovation.', 'Most innovations are sustaining (improving existing products for existing customers); disruptive innovations specifically begin in low-end or new markets and displace incumbents.')],
    cases=[('Kodak and digital photography', 'Kodak dominated film photography and built an early digital camera in 1975, but protected its film business; smartphones and digital cameras eroded film sales and Kodak filed for bankruptcy in 2012.', 'disruption by digital systems',
            'a digital innovation from inside the firm displaced its own core product, showing how disruption can defeat even the inventor when incentives favour the old model.'),
           ('Wikipedia and printed encyclopaedias', 'Wikipedia, launched in 2001, grew into one of the most visited websites, written by volunteers; Encyclopaedia Britannica ended its print edition in 2012.', 'transformation of how knowledge is produced',
            'knowledge production shifted from paid experts to open, collaborative editing, changing ideas of authority and access to information.'),
           ('the smartphone after the 2007 iPhone launch', 'Touchscreen smartphones with app stores spread rapidly after 2007, combining camera, maps, music, banking and messaging in one device.', 'causality and change',
            'the smartphone triggered chains of change – app economies, ride-hailing, mobile banking – but its effects also depended on cheap data plans and networks, showing multiple causes.')],
    sources=[('"Netflix is a joke. They have no real business model."', 'Remark attributed to a senior Blockbuster executive in the mid-2000s, as reported in business histories of the company',
              'Explain what the source suggests about how established firms respond to disruptive innovation.', 'It suggests incumbents underestimate new entrants whose models look weak at first; Blockbuster dismissed streaming/mail-order rental and later filed for bankruptcy (2010), illustrating disruption theory.'),
             ('"We always overestimate the change that will occur in the next two years and underestimate the change that will occur in the next ten."', 'Bill Gates, The Road Ahead (1995)',
              'Explain what the source suggests about the pattern of technological change.', 'Change often appears slow at first because adoption, infrastructure and habits take time, but cumulative diffusion produces large long-term transformations; short-term hype and long-term underestimation are both common.')],
    evaluate=[('Digital technologies are the main cause of social change in the 21st century.',
               ['smartphones and platforms have transformed work, communication and politics', 'the speed of diffusion (e.g. ChatGPT reaching about 100 million users within two months) is unprecedented'],
               ['change is also driven by economics, demography, climate and politics', 'societies shape how technologies are adopted (social shaping)', 'technology often amplifies existing trends rather than starting them'],
               'Digital technologies are a powerful driver and amplifier of change, but they interact with social, economic and political causes; calling them the main cause overstates determinism.'),
              ('Disruption by digital systems always benefits consumers.',
               ['lower prices and more choice (streaming, e-commerce)', 'new services for under-served groups (mobile money)'],
               ['market concentration may later raise prices or reduce privacy', 'job losses and closure of local businesses harm communities', 'quality may fall (e.g. local journalism decline)'],
               'Consumers often gain in the short run, but long-term effects depend on competition, regulation and who bears the costs.')],
    extended=[('Using one example of disruption by a digital system, analyse the causes of the disruption and evaluate its consequences for two stakeholders.', 'Choose e.g. streaming vs video rental, ride-hailing vs taxis, or e-commerce vs local retail; explain causes (cheaper technology, networks, consumer convenience, incumbents\' choices); evaluate consequences for e.g. consumers and workers, using specific evidence; reach a judgement.', 6, 'long')],
))

R.facts('ch02-st2', F(
    terms=[('expression', 'the ways people communicate ideas, feelings, identities and beliefs, which digital media have widened through text, images, video, sound and code'),
           ('political expression', 'communicating views about power, government and public issues, for example through hashtags, livestreams or online petitions'),
           ('cultural expression', 'the creation and sharing of art, music, language and traditions that reflect a group\'s culture'),
           ('censorship', 'the suppression or control of expression by governments, platforms or other powerful actors'),
           ('freedom of expression', 'the right to seek, receive and impart information and ideas, protected by Article 19 of the Universal Declaration of Human Rights'),
           ('self-censorship', 'when people limit what they say because they fear consequences such as surveillance, punishment or harassment')],
    facts=[('Which article of the Universal Declaration of Human Rights protects freedom of opinion and expression?', 'Article 19',
            ['Article 1', 'Article 12', 'Article 26'], 'Article 19 protects the right to hold opinions and to seek, receive and impart information through any media.'),
           ('Which movement used the hashtag #EndSARS in 2020 to protest against police brutality?', 'A youth-led protest movement in Nigeria',
            ['A climate movement in Sweden', 'A labour strike in South Korea', 'A pro-democracy movement in Hong Kong'], '#EndSARS targeted the Nigerian police Special Anti-Robbery Squad.'),
           ('Following the death of Mahsa Amini in 2022, which country restricted internet access during protests?', 'Iran',
            ['Brazil', 'Japan', 'Canada'], 'Iran restricted mobile internet and blocked platforms such as Instagram and WhatsApp.'),
           ('Which of the following is an example of digital cultural expression?', 'Indigenous creators using TikTok to teach their language',
            ['A bank updating its mobile app', 'A government publishing tax data', 'A server backing up files'], 'Creators such as speakers of te reo Māori and other Indigenous languages use short video to share language and culture.')],
    why=[('Explain why digital platforms have increased the range of people who can express themselves publicly.', 'Low-cost devices and free platforms remove traditional gatekeepers (publishers, broadcasters), so anyone with a phone can publish text, video or music to a potentially global audience.'),
         ('Explain why online expression can lead to self-censorship.', 'When people know posts are permanent, searchable and monitored by employers, platforms or governments, or fear harassment, they may avoid controversial views, which narrows public debate even without formal censorship.'),
         ('Explain why platforms act as gatekeepers of expression even though anyone can post.', 'Platform rules and ranking algorithms decide what is removed, demoted or amplified, so visibility – and therefore the reach of expression – is controlled by private companies.')],
    contrast=[('government censorship', 'platform content moderation', 'Government censorship is the state suppressing expression, often by law or blocking (e.g. internet shutdowns); platform content moderation is a private company applying its own rules to remove or limit content on its service.'),
              ('freedom of expression', 'freedom of reach', 'Freedom of expression is the right to say something; "freedom of reach" refers to whether platforms amplify it – content may be allowed but demoted by algorithms.')],
    misc=[('Freedom of expression means platforms must allow any content.', 'Human rights law protects expression mainly against state interference and permits limits (e.g. incitement to violence); private platforms also set terms of service and must remove illegal content in many jurisdictions (e.g. under the EU DSA).'),
          ('Online expression is the same as offline expression, just faster.', 'Online expression differs in permanence, scale, searchability and algorithmic amplification, and can be anonymous; these features change both its power and its risks.')],
    cases=[('the #EndSARS protests in Nigeria (2020)', 'Young Nigerians used Twitter and Instagram to share videos of police abuse and organise protests; on 20 October 2020 soldiers opened fire on protesters at Lekki toll gate in Lagos, and the event was livestreamed.', 'digital political expression',
            'social media let young people document abuses and mobilise nationally and globally, but also exposed protesters to surveillance, showing both the power and risks of digital expression.'),
           ('Indigenous language content on TikTok and YouTube', 'Creators speaking languages such as te reo Māori, Sámi or Quechua post short lessons, songs and jokes, reaching young audiences.', 'digital cultural expression',
            'digital media allow minority cultures to express and revitalise identity on their own terms, though algorithms favouring dominant languages may limit reach.'),
           ("Iran's internet restrictions during the 2022 protests", 'After Mahsa Amini died in custody in September 2022, protests spread; authorities throttled mobile data and blocked Instagram and WhatsApp.', 'state control of expression',
            'the state limited the channels people used to share images and organise, showing that digital expression depends on infrastructure the state can control.')],
    sources=[('"With a phone and a hashtag, we became our own broadcasters. Nobody could tell us the story was not happening."', 'Nigerian #EndSARS protester, interviewed by a news outlet, 2020',
              'With reference to the source, explain how digital technology changed political expression for the protesters.', 'It removed dependence on traditional media gatekeepers: protesters could document and broadcast events themselves, making it harder for authorities to deny what was happening.'),
             ('"Everyone has the right to freedom of opinion and expression; this right includes freedom to hold opinions without interference and to seek, receive and impart information and ideas through any media and regardless of frontiers."', 'Universal Declaration of Human Rights, Article 19 (1948)',
              'Explain why the phrase "through any media and regardless of frontiers" is significant for digital society.', 'Although written in 1948, it applies to new media such as the internet and to cross-border communication, supporting arguments against blocking, shutdowns and censorship of online platforms.')],
    evaluate=[('Social media has strengthened freedom of expression more than it has threatened it.',
               ['ordinary people can publish and organise without gatekeepers (#EndSARS, #MeToo)', 'marginalised groups gain visibility'],
               ['surveillance and shutdowns target online speakers', 'harassment and pile-ons silence women and minorities', 'opaque moderation and algorithms decide reach'],
               'Social media has widened who can speak, but power over reach and visibility has shifted to platforms and states; the balance depends on context and regulation.'),
              ('Platforms should never remove lawful content.',
               ['removing lawful speech gives private firms excessive power', 'over-removal chills debate'],
               ['some lawful content is harmful (harassment, self-harm promotion)', 'platforms have rights to set community standards', 'lawful differs between countries'],
               'Platforms need clear, transparent rules and appeal processes; a blanket ban on removing lawful content is unworkable, but removals should be proportionate and accountable.')],
    extended=[('Analyse how one digital platform has both enabled and limited political expression in a specific country.', 'E.g. Twitter/X in Nigeria (#EndSARS, then a government ban June 2021–January 2022), or Telegram in Iran or Belarus; enabling: organisation, documentation, global reach; limiting: state blocking, surveillance, moderation decisions; conclude on overall effect.', 6, 'long')],
))

R.facts('ch02-st3', F(
    terms=[('meme', 'a unit of culture (image, phrase, video format) that is copied, varied and spread from person to person; the term was coined by Richard Dawkins in The Selfish Gene (1976)'),
           ('remix culture', 'a culture in which people create new works by combining and modifying existing material (Lawrence Lessig, Remix, 2008)'),
           ('participatory culture', 'a culture with low barriers to creating and sharing, where members believe their contributions matter (Henry Jenkins)'),
           ('Creative Commons', 'a set of free licences that let creators allow others to share and reuse their work on stated conditions, such as attribution (BY)'),
           ('fair use', 'a US legal doctrine permitting limited use of copyrighted material without permission, e.g. for commentary, criticism or parody'),
           ('user-generated content', 'material such as videos, posts, reviews or fan fiction created by ordinary users rather than professional media companies')],
    facts=[('Who coined the term "meme" in 1976?', 'Richard Dawkins', ['Marshall McLuhan', 'Henry Jenkins', 'Tim Berners-Lee'], 'Dawkins introduced "meme" in The Selfish Gene as a cultural analogue of the gene.'),
           ('What does the "BY" element of a Creative Commons licence require?', 'That the original creator is credited (attribution)',
            ['That the work is not used commercially', 'That no changes are made', 'That the work is bought'], 'BY = attribution; NC = non-commercial; ND = no derivatives; SA = share-alike.'),
           ('Which 2014 online challenge raised over US$100 million for the ALS Association in the United States?', 'The Ice Bucket Challenge',
            ['The Harlem Shake', 'Planking', 'The Mannequin Challenge'], 'The ALS Association reported about $115 million raised in summer 2014.'),
           ('Which fan-fiction archive won a Hugo Award in 2019?', 'Archive of Our Own (AO3)', ['Wattpad', 'Tumblr', 'DeviantArt'], 'AO3, run by the Organization for Transformative Works, won the Hugo for Best Related Work.')],
    why=[('Explain why memes spread so quickly online.', 'Memes are short, easy to copy and adapt, emotionally engaging or funny, and platforms make sharing one click; each variation reaches new networks, so they spread through participation rather than a single broadcaster.'),
         ('Explain why remix culture creates tension with copyright law.', 'Remixing depends on reusing existing works, but copyright gives creators exclusive rights to copy and adapt; automated systems such as YouTube Content ID may block remixes even when they could be fair use.'),
         ('Explain why participatory culture can be described as a change in the relationship between audiences and producers.', 'Audiences no longer only consume media; they create, remix and distribute it (fan fiction, reaction videos), blurring the line between producer and consumer and shifting some cultural power to communities.')],
    contrast=[('a meme', 'viral content', 'Viral content is any content that spreads rapidly (often unchanged); a meme spreads through imitation and variation, with users creating their own versions of a format.'),
              ('copyright', 'Creative Commons licensing', 'Copyright automatically reserves all rights to the creator; a Creative Commons licence is a choice by the creator to grant the public certain permissions in advance, under stated conditions.')],
    misc=[('Anything posted online is free to remix because it is public.', 'Online material is usually still protected by copyright; reuse needs permission, a licence (e.g. Creative Commons) or a legal exception such as fair use/fair dealing.'),
          ('Memes are trivial and have no political importance.', 'Memes are widely used for political commentary and propaganda (e.g. election campaigns, protest humour), shaping opinion and identity.')],
    cases=[('the Ice Bucket Challenge (2014)', 'Participants filmed themselves pouring iced water over their heads, nominated friends and donated; the ALS Association reported about US$115 million raised.', 'participatory culture',
            'ordinary users created and spread content themselves, turning a simple format into a global fundraising campaign through imitation and nomination.'),
           ('YouTube Content ID', 'YouTube\'s Content ID system automatically matches uploads against reference files from rights holders, who can block, track or monetise matching videos.', 'tension between remix culture and copyright',
            'automation protects rights holders at scale but can block or demonetise remixes, parodies and commentary that might be lawful, shifting power to large rights holders.'),
           ('the "Distracted Boyfriend" stock photo', 'A 2015 stock photograph by Antonio Guillem became a meme format in 2017, relabelled endlessly to comment on politics, brands and everyday life.', 'how memes create meaning through variation',
            'the same image template carries new meanings with each label, showing how meaning is co-created by users rather than fixed by the original creator.')],
    sources=[('"The 20th century was a read-only culture; the 21st can be read-write again, where people create by remixing the culture around them."', 'Paraphrase of Lawrence Lessig, Remix (2008)',
              'Explain what the source means by a "read-write" culture.', 'A culture where people do not only consume (read) media but also create and share their own versions (write), e.g. remixes, mash-ups and memes, enabled by digital tools.'),
             ('"Fan works are legitimate, transformative creations – not theft."', 'Mission statement summary, Organization for Transformative Works (runs AO3)',
              'Explain the perspective expressed in the source and one challenge to it.', 'The source argues fan fiction transforms originals and adds new meaning, so it should be protected; a challenge is that some authors and rights holders see it as unauthorised use of their characters and worlds.')],
    evaluate=[('Remix culture is more creative than original creation.',
               ['remixing produces new meanings and lets more people create', 'all culture builds on earlier works'],
               ['remixes can be low-effort copying', 'original creators may lose income or control', 'automated copyright tools limit remixing'],
               'Remixing is a genuine form of creativity, but it depends on, rather than replaces, original works; balanced rules (fair use, open licences) protect both.'),
              ('Memes have become one of the most powerful forms of political communication.',
               ['memes spread quickly and reach young audiences', 'they simplify complex issues and build group identity'],
               ['simplification can spread misinformation', 'impact on actual votes or policy is hard to prove', 'traditional media and campaigns still dominate agenda-setting'],
               'Memes are influential for framing and identity, especially among young people, but their power is hard to measure and often works alongside other media.')],
    extended=[('Using one example of participatory culture, analyse how it has changed the relationship between creators and audiences.', 'E.g. fan fiction on AO3, TikTok duets/remixes, or Wikipedia; explain audiences becoming producers, communities setting norms, conflicts with copyright holders, and benefits/limits; reach a judgement.', 6, 'long')],
))

# =============================================================================================
# ch03 Concepts 2.3–2.4: identity and power
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('digital identity', 'the information and representations that identify a person online, including accounts, profiles, credentials and data trails'),
           ('self-presentation', 'the way people choose to present themselves to others, which online includes profile photos, posts and curated images (after Erving Goffman, 1959)'),
           ('context collapse', 'the merging of different audiences (family, friends, employers) into one online audience, making self-presentation harder (Marwick and boyd, 2011)'),
           ('foundational digital ID', 'a government-issued digital identity used to prove who a person is across many services, such as India\'s Aadhaar or Estonia\'s e-ID'),
           ('anonymity', 'interacting without revealing one\'s real identity'),
           ('pseudonymity', 'using a consistent online name or handle that is not one\'s legal name')],
    facts=[('Which body issues the 12-digit Aadhaar number in India?', 'The Unique Identification Authority of India (UIDAI)',
            ['The Reserve Bank of India', 'The Election Commission of India', 'The Ministry of External Affairs'], 'UIDAI issues Aadhaar numbers linked to biometric data (fingerprints, iris scans, photograph).'),
           ('Which biometric data are collected for Aadhaar enrolment?', 'Fingerprints, iris scans and a facial photograph',
            ['DNA samples', 'Voice recordings only', 'Handwriting samples'], 'Aadhaar uses ten fingerprints, both irises and a photograph.'),
           ('Which sociologist described social life as a "performance" with front and back stages?', 'Erving Goffman', ['Michel Foucault', 'Shoshana Zuboff', 'Manuel Castells'], 'Goffman, The Presentation of Self in Everyday Life (1959).'),
           ('Which country has offered "e-Residency", a digital identity for non-residents, since 2014?', 'Estonia', ['Singapore', 'Finland', 'Japan'], 'Estonia\'s e-Residency lets foreigners run EU-based companies online.')],
    why=[('Explain why people may present different identities on different platforms.', 'Each platform has different audiences and norms (LinkedIn professional, Instagram curated, Finsta/private accounts informal), so people manage impressions by selecting what to show, as Goffman\'s idea of performance suggests.'),
         ('Explain why foundational digital ID systems can both include and exclude people.', 'They let people without paper documents access welfare, banking and SIM cards, but if biometric authentication fails (worn fingerprints, poor connectivity) or enrolment is hard, people can be denied services they are entitled to.'),
         ('Explain why anonymity online can be both protective and harmful.', 'Anonymity protects whistle-blowers, activists and LGBTQ+ people from persecution, but it can also reduce accountability and enable harassment, trolling and fraud.')],
    contrast=[('anonymity', 'pseudonymity', 'Anonymity means no stable identifier links actions to a person; pseudonymity uses a consistent alias that builds a reputation without revealing the legal name.'),
              ('a social (self-presented) identity', 'a legal digital identity', 'A social identity is how a person chooses to present themselves online (profiles, posts); a legal digital identity is an official credential that proves who they are (e.g. Aadhaar, e-ID).')],
    misc=[('Your digital identity consists only of what you choose to post.', 'Digital identity also includes data others post about you and passive data trails (location, browsing, purchases) collected and inferred by companies.'),
          ('Aadhaar is mandatory for every service in India, including private bank accounts.', 'In Puttaswamy (2018) the Supreme Court upheld Aadhaar for welfare and tax (PAN linking) but struck down Section 57, so private companies cannot make it mandatory, e.g. for bank accounts or mobile SIMs.')],
    cases=[("India's Aadhaar system", 'Aadhaar has enrolled over 1.3 billion residents since 2010; the Supreme Court in K.S. Puttaswamy (2017) declared privacy a fundamental right and in 2018 upheld Aadhaar while limiting private use.', 'digital identity and inclusion',
            'a biometric ID gave many people a portable identity for welfare and banking, but authentication failures and privacy concerns show how digital identity can also exclude and expose.'),
           ("Estonia's e-ID and e-Residency", "Estonian citizens use a chip-based ID card or Smart-ID to vote online, sign documents and access almost all public services; e-Residency (2014) extends a digital identity to foreigners.", 'digital identity as access to services and citizenship',
            'identity becomes a key to the state\'s digital services, enabling efficiency and remote participation, but concentrating trust in one system (a 2017 chip vulnerability forced certificate updates).'),
           ('context collapse on social media', 'Researchers Marwick and boyd (2011) showed that Twitter users imagine audiences and self-censor because friends, family and employers see the same posts.', 'self-presentation online',
            'when audiences merge, users must craft a single identity acceptable to all, changing how people express who they are.')],
    sources=[('"For the first time, my mother has an identity the bank accepts. But last month her thumbprint would not scan at the ration shop, and she went home without rice."', 'Resident of Jharkhand, India, quoted in a 2019 report on welfare and biometric authentication',
              'With reference to the source, explain one benefit and one problem of biometric digital identity.', 'Benefit: it gave the mother an accepted identity for banking (inclusion). Problem: biometric authentication failure meant she was denied food rations, showing exclusion when the system fails.'),
             ('"On the Internet, nobody knows you\'re a dog."', 'Caption of a cartoon by Peter Steiner, The New Yorker (1993)',
              'Explain what the source suggests about identity online and how this has changed since 1993.', 'It suggested the early internet allowed anonymity and freely chosen identities; today tracking, real-name policies, data profiling and digital ID mean platforms often know a great deal about who users are.')],
    evaluate=[('A single national digital ID does more good than harm.',
               ['inclusion of people without documents (Aadhaar)', 'efficient, less corrupt delivery of welfare and services (Estonia)'],
               ['exclusion through authentication failures', 'privacy and surveillance risks from centralised databases', 'function creep into areas beyond the original purpose'],
               'Digital ID can bring major benefits when backed by strong privacy law, offline alternatives and independent oversight; without them, harms can outweigh gains for the most vulnerable.'),
              ('People have more freedom to choose their identity online than offline.',
               ['avatars, pseudonyms and communities allow exploration of identity', 'LGBTQ+ youth can find support anonymously'],
               ['data profiles assign identities based on behaviour', 'real-name rules and context collapse constrain self-presentation', 'harassment targets visible identities'],
               'Online spaces offer new freedom to explore identity, but platforms and data systems also define and constrain identity in ways users do not control.')],
    extended=[('Compare how a social-media profile and a government digital ID shape a person\'s identity, and evaluate which has the greater impact on their life chances.', 'Compare self-presented vs assigned identity, control, audiences and consequences (e.g. Instagram vs Aadhaar/e-ID); evaluate impact on access to services, jobs and rights; support with examples.', 6, 'long')],
))

R.facts('ch03-st2', F(
    terms=[('power', 'the ability of a person, group or system to influence or control the behaviour of others and the outcomes of decisions'),
           ('gatekeeping', 'controlling which information, products or people gain access to an audience or market, as app stores and search engines do'),
           ('platform', 'a digital infrastructure that connects different groups (users, advertisers, sellers, developers) and sets the rules for their interactions'),
           ('network effects', 'the increase in a service\'s value to each user as more people use it, which helps large platforms dominate'),
           ('deplatforming', 'removing a person or group from a platform, taking away their access to its audience'),
           ('digital resistance', 'actions by users or groups that challenge or evade the power of platforms or states, such as encryption, VPNs, boycotts or hacktivism')],
    facts=[('In 2017 the European Commission fined Google €2.42 billion for abusing its dominance in which area?', 'Favouring its own comparison-shopping service in search results',
            ['Selling smartphones below cost', 'Failing to pay taxes in Ireland', 'Leaking user passwords'], 'The Google Shopping decision (upheld by the CJEU in 2024).'),
           ('Why did Apple remove Fortnite from its App Store in August 2020?', 'Epic Games added a direct payment option that bypassed Apple\'s in-app payment system',
            ['Fortnite contained malware', 'Epic stopped paying taxes', 'Fortnite was banned by the US government'], 'This led to Epic v. Apple over app-store gatekeeping power.'),
           ('Which body did Meta set up in 2020 to review some of its content-moderation decisions?', 'The Oversight Board', ['The Digital Services Coordinator', 'ICANN', 'The Internet Engineering Task Force'], 'The Oversight Board reviewed the suspension of Donald Trump in 2021.'),
           ('Which EU law designates large platforms as "gatekeepers" with special obligations on competition?', 'The Digital Markets Act (DMA)', ['The GDPR', 'The AI Act', 'The ePrivacy Directive'], 'The DMA (applies from 2023–24) targets gatekeepers such as Alphabet, Apple, Meta, Amazon, Microsoft and ByteDance.')],
    why=[('Explain why network effects give large platforms power.', 'Each new user makes the platform more valuable to others (more friends, sellers, buyers), so users stay even if they dislike its rules; rivals struggle to attract users, letting the dominant platform set terms for users, advertisers and businesses.'),
         ('Explain why app stores are an example of gatekeeping power.', 'Apple and Google decide which apps reach billions of phones, set commission rates (up to 30%) and rules, so developers depend on them for access to customers.'),
         ('Explain why the deplatforming of a political leader is an example of platform power.', 'When Twitter and Facebook suspended Donald Trump in January 2021, private companies removed an elected leader\'s main channel to millions of followers, showing that platforms can shape political communication beyond the control of voters or courts.')],
    contrast=[('hard power of the state online', 'platform power', 'State power online uses law and coercion (blocking, arrests, shutdowns); platform power comes from controlling infrastructure, rules and algorithms that decide visibility and access.'),
              ('gatekeeping', 'censorship', 'Gatekeeping is controlling access to an audience or market (e.g. app approval, search ranking) and may be commercial; censorship is the deliberate suppression of expression, usually for political or moral reasons.')],
    misc=[('Users have no power over large platforms.', 'Users can resist through collective action (boycotts, #DeleteFacebook), switching (e.g. to Signal in 2021), regulation pressure, and creators organising; regulators also act on their behalf (DMA, DSA).'),
          ('Platforms are neutral spaces that simply host content.', 'Platforms make design and ranking choices, set rules and monetise attention, so they actively shape what users see and do.')],
    cases=[('Epic Games v. Apple', 'Apple removed Fortnite from the App Store in 2020 after Epic introduced direct payments; a 2021 US ruling required Apple to allow links to outside payments, and the EU DMA later required alternative app stores in the EU.', 'gatekeeping power',
            'Apple\'s control of the only app store on iPhones let it set commissions and rules, and the case shows how courts and regulators try to limit that power.'),
           ('the deplatforming of Donald Trump (January 2021)', 'After the 6 January Capitol attack, Twitter permanently suspended Trump and Facebook suspended him; Meta\'s Oversight Board upheld the suspension but criticised its indefinite length.', 'the power of platforms over political communication',
            'private companies, not courts or voters, decided to cut off a head of state\'s main channel, raising questions about legitimacy and accountability of platform power.'),
           ('the Parler removal (2021)', 'In January 2021 Apple and Google removed the Parler app from their stores and Amazon Web Services stopped hosting it, taking it offline for weeks.', 'infrastructure power',
            'control over app stores and cloud hosting gave a few firms the power to remove an entire platform, showing power at several layers of the internet.')],
    sources=[('"If you want to reach iPhone users, there is only one door, and Apple holds the key and charges for entry."', 'Statement by an app developer at a 2021 hearing on app-store competition',
              'With reference to the source, explain how Apple exercises power over developers.', 'Apple controls the only route (the App Store) to iPhone users, so developers must accept its rules and commission; this is gatekeeping power based on control of access.'),
             ('"Our decisions are binding, and Meta must implement them unless doing so would violate the law."', 'Oversight Board, Charter summary (2020)',
              'Explain one way the Oversight Board might increase, and one way it might fail to increase, accountability of Meta\'s power.', 'Increase: independent review of specific cases, published reasoning and binding decisions. Fail: it reviews only a tiny number of cases, is funded by Meta via a trust, and its policy recommendations are not binding.')],
    evaluate=[('Large technology platforms now have more power than many governments.',
               ['they control communication infrastructure for billions of people', 'they can deplatform leaders and set global rules', 'their revenues exceed the GDP of many states'],
               ['states can still legislate, fine and ban (EU fines, Nigeria\'s Twitter ban, China\'s control of platforms)', 'platforms lack armies and taxation powers', 'states can force data localisation and takedowns'],
               'Platforms hold distinctive infrastructural and discursive power that rivals small states, but governments with large markets and strong laws can still constrain them.'),
              ('Regulation such as the EU Digital Markets Act can effectively limit platform power.',
               ['large fines (up to 10% of global turnover) and specific obligations (alternative app stores, interoperability)', 'the EU market is too large to ignore (Brussels effect)'],
               ['gatekeepers comply minimally or appeal', 'enforcement is slow and complex', 'network effects may keep users on dominant platforms anyway'],
               'The DMA can shift some power, especially over app stores and self-preferencing, but its effect depends on enforcement and on whether competitors and users actually switch.')],
    extended=[('Analyse two different forms of power exercised by one digital platform and evaluate how effectively they have been challenged.', 'E.g. Google: gatekeeping in search and Android; data power from advertising; challenges: EU fines (Shopping €2.42bn, Android €4.1bn), US antitrust ruling 2024 that Google is a search monopolist, DMA obligations; evaluate effectiveness.', 6, 'long')],
))

R.facts('ch03-st3', F(
    terms=[('digital citizenship', 'the responsible, ethical and informed participation in online communities and society, including rights and responsibilities'),
           ('attention economy', 'an economic system in which platforms compete for users\' limited attention, which they sell to advertisers'),
           ('online activism', 'using digital tools such as hashtags, petitions, crowdfunding and livestreams to campaign for social or political change'),
           ('slacktivism', 'low-effort online support for a cause (likes, shares) that may give a feeling of participation with little real-world impact'),
           ('persuasive design', 'interface design that uses psychological techniques (infinite scroll, autoplay, variable rewards) to keep users engaged'),
           ('hashtag activism', 'using a shared hashtag to raise awareness and connect people around a cause, as in #MeToo or #BlackLivesMatter')],
    facts=[('Who wrote that "a wealth of information creates a poverty of attention" (1971)?', 'Herbert Simon', ['Tim Berners-Lee', 'Marshall McLuhan', 'Eli Pariser'], 'Simon\'s observation is the origin of the attention economy idea.'),
           ('Who founded the "me too" movement in 2006, before the 2017 hashtag spread?', 'Tarana Burke', ['Alyssa Milano', 'Malala Yousafzai', 'Greta Thunberg'], 'Alyssa Milano\'s 2017 tweet popularised #MeToo, building on Burke\'s work.'),
           ('Which 2012 viral video by Invisible Children reached about 100 million views in six days?', 'Kony 2012', ['The Ice Bucket Challenge', 'Gangnam Style', '#BringBackOurGirls'], 'Kony 2012 is often cited in debates on slacktivism.'),
           ('Which of the following is an example of persuasive design?', 'Infinite scroll', ['End-to-end encryption', 'Two-factor authentication', 'Alt text for images'], 'Infinite scroll removes natural stopping points, increasing time on site.')],
    why=[('Explain why social media platforms are designed to maximise engagement.', 'Their main revenue is advertising, which depends on how much time and attention users give; more engagement produces more data and ad impressions, so features such as autoplay, notifications and infinite scroll are designed to keep users online.'),
         ('Explain why online activism may be criticised as slacktivism.', 'Liking or sharing requires little effort and may make people feel they have contributed without donating, volunteering or voting; campaigns like Kony 2012 achieved huge awareness but limited lasting change.'),
         ('Explain why digital citizenship involves responsibilities as well as rights.', 'Online actions affect others – sharing misinformation, harassment or private data can cause harm – so citizens have responsibilities to verify, respect others and protect privacy alongside rights to expression and access.')],
    contrast=[('online activism', 'slacktivism', 'Online activism uses digital tools as part of sustained action (organising, fundraising, protests); slacktivism refers to minimal, symbolic online support that does not translate into action.'),
              ('a user as a customer', 'a user as the product in the attention economy', 'A customer pays for a service; in the attention economy free services are funded by selling users\' attention and data to advertisers, so the user\'s attention is effectively what is sold.')],
    misc=[('Hashtag campaigns never lead to real-world change.', 'Some do: #MeToo contributed to investigations, resignations and law changes; #BlackLivesMatter organised protests and policy debates; online awareness can support offline action.'),
          ('Free social media apps are free because they cost nothing to run.', 'Platforms have huge costs (servers, staff); they are free to users because revenue comes from advertising based on attention and data.')],
    cases=[('#MeToo (2017)', 'After allegations against Harvey Weinstein, Alyssa Milano invited women to reply "me too"; the hashtag was used millions of times in many countries.', 'online activism',
            'a simple hashtag made the scale of sexual harassment visible and connected survivors globally, contributing to resignations, prosecutions and workplace policy changes.'),
           ('Kony 2012', 'A 30-minute video by Invisible Children about Ugandan warlord Joseph Kony was viewed about 100 million times within a week; Kony was never captured.', 'the limits of online activism (slacktivism)',
            'massive awareness did not achieve its stated goal and the campaign was criticised for oversimplification, illustrating the gap between attention and outcomes.'),
           ('autoplay and infinite scroll', 'Aza Raskin, who designed infinite scroll in 2006, later said he regretted how it was used to keep people scrolling.', 'the attention economy',
            'a design choice that removes stopping cues increases time on platforms, which converts attention into advertising revenue.')],
    sources=[('"If you are not paying for it, you\'re not the customer; you\'re the product being sold."', 'Comment by Andrew Lewis ("blue_beetle") on MetaFilter, 2010; widely quoted',
              'Explain what the source suggests about the attention economy.', 'Free platforms earn money by selling users\' attention and behavioural data to advertisers, so users\' time and data are the commodity, not the service itself.'),
             ('"Fridays for Future began with one girl and a sign. Within a year, millions of students in over 150 countries joined strikes organised largely through Instagram and WhatsApp."', 'Climate campaign report, 2020',
              'Explain how the source shows digital tools supporting activism beyond slacktivism.', 'Online tools spread Greta Thunberg\'s school strike and coordinated offline strikes by millions, showing digital organisation leading to physical collective action.')],
    evaluate=[('Online activism is more effective than traditional activism.',
               ['reaches global audiences quickly and cheaply (#MeToo, Fridays for Future)', 'lowers barriers to participation'],
               ['weak ties may not sustain long campaigns', 'easy to ignore or suppress (shutdowns, surveillance)', 'many campaigns produce awareness without policy change'],
               'Online activism is powerful for awareness and mobilisation, but is most effective when combined with organised offline action and institutions.'),
              ('Responsibility for limiting the harms of the attention economy lies with users, not platforms.',
               ['users can set limits, turn off notifications and choose alternatives', 'digital citizenship emphasises personal responsibility'],
               ['platforms deliberately design for compulsive use', 'children and teenagers are especially vulnerable', 'information asymmetry means users cannot see how design manipulates them'],
               'Users have some responsibility, but because platforms design and profit from engagement, they and regulators (e.g. design codes, the DSA) carry the greater responsibility.')],
    extended=[('Evaluate the impact of one hashtag campaign you have studied, considering both online and offline outcomes.', 'E.g. #MeToo, #BlackLivesMatter, #BringBackOurGirls, #EndSARS; describe the campaign; analyse reach, mobilisation, policy outcomes, backlash and limitations; reach a supported judgement.', 6, 'long')],
))
AR('ch03-st3', [
    ('Social media platforms use features such as infinite scroll and autoplay.', 'Their advertising-based business models earn more when users spend more time on the platform.', 'a',
     'Engagement-maximising design follows directly from the attention-based revenue model.'),
    ('#MeToo was started by Alyssa Milano in 2017.', 'Hashtags let survivors share experiences publicly and connect across countries.', 'd',
     'The movement was founded by Tarana Burke in 2006; Milano popularised the hashtag in 2017. R is true.'),
])

# =============================================================================================
# ch04 Concepts 2.5–2.7: space, systems, values and ethics
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('virtual space', 'a computer-generated environment in which people interact, such as an online game world or a metaverse platform'),
           ('cyberspace', 'the interconnected digital environment of networks, data and online interactions'),
           ('data sovereignty', 'the principle that data are subject to the laws of the country in which they are collected or stored'),
           ('data localisation', 'a legal requirement that certain data be stored on servers within a country\'s borders'),
           ('geo-blocking', 'restricting access to online content based on the user\'s geographic location'),
           ('time-space compression', 'the sense that distance and time matter less because digital networks allow instant communication across the world (David Harvey)')],
    facts=[('Which company renamed itself in October 2021 to reflect its focus on the "metaverse"?', 'Meta (formerly Facebook)', ['Alphabet', 'Microsoft', 'Tencent'], 'Facebook Inc. became Meta Platforms in October 2021.'),
           ('Which virtual world, launched in 2003, allowed users to buy virtual land with its own currency (Linden dollars)?', 'Second Life', ['Minecraft', 'Roblox', 'World of Warcraft'], 'Second Life by Linden Lab had an in-world economy convertible to real money.'),
           ('Which of the following is an example of data localisation?', 'A law requiring payment data about Indian users to be stored only in India',
            ['A user saving files to a USB drive', 'A company encrypting its emails', 'A website translating into Hindi'], 'The Reserve Bank of India required payment-system data to be stored in India from 2018.'),
           ('Which satellite internet service was activated in Ukraine in 2022 to maintain connectivity during the war?', 'Starlink', ['Iridium', 'Project Loon', 'OneWeb only'], 'SpaceX Starlink terminals were shipped to Ukraine from late February 2022.')],
    why=[('Explain why the internet can be described as both borderless and bordered.', 'Data flows globally and people communicate across countries instantly, but states impose borders through laws, data localisation, firewalls (e.g. the Great Firewall), geo-blocking and shutdowns, so access depends on place.'),
         ('Explain why physical place still matters in digital society.', 'Infrastructure (cables, data centres, towers) is physically located; connectivity and speed vary by location (urban/rural), and national laws apply where users and servers are, so place shapes digital experience.'),
         ('Explain why virtual spaces can have real-world consequences.', 'Interactions in virtual spaces involve real people, money and emotions: virtual items are sold for real currency, harassment in VR causes harm, and events (e.g. concerts in Fortnite) generate real income and culture.')],
    contrast=[('a physical space', 'a virtual space', 'A physical space has material location and boundaries (a school, a city); a virtual space is a digital environment where interaction is mediated by software and can be accessed from anywhere with a connection.'),
              ('data sovereignty', 'data localisation', 'Data sovereignty is the principle that data are governed by the laws of a country; data localisation is a specific policy requiring data to be physically stored within that country.')],
    misc=[('Data stored "in the cloud" is not located anywhere physical.', 'Cloud data is stored on servers in physical data centres in specific countries, subject to those countries\' laws and energy use.'),
          ('Being online means everyone has equal access to the same internet.', 'Access differs by place: censorship, geo-blocking, network quality and cost mean users in different countries or regions experience different internets.')],
    cases=[('the Travis Scott concert in Fortnite (2020)', 'In April 2020 Travis Scott\'s "Astronomical" virtual concert in Fortnite drew about 12.3 million concurrent players.', 'virtual space as a site of culture',
            'a game world became a venue for a global live event during COVID-19 lockdowns, showing how virtual space can replace and extend physical gathering places.'),
           ('Starlink in Ukraine', 'After Russia\'s invasion in February 2022, Starlink terminals helped Ukrainian civilians and the military stay connected when ground networks were damaged.', 'space, borders and connectivity',
            'satellite connectivity bypassed damaged national infrastructure, but it also gave a private company (SpaceX) power over a country\'s communications in wartime.'),
           ("China's Great Firewall", 'China blocks many foreign services (Google, Facebook, YouTube, WhatsApp) and promotes domestic platforms such as WeChat and Baidu.', 'digital borders',
            'the state builds a national digital space with its own platforms and rules, showing that cyberspace can be bordered like physical territory.')],
    sources=[('"Data may flow freely, but it always lives somewhere – in a building, in a country, under a law."', 'Report on data governance, think tank, 2022',
              'Explain what the source suggests about the concept of space in digital society.', 'Even though data seems placeless, it is stored in physical data centres in particular countries and is governed by their laws, so physical and legal space still shape digital systems.'),
             ('"In the metaverse you will be able to teleport instantly as a hologram to be at the office without a commute."', 'Mark Zuckerberg, founder\'s letter, October 2021',
              'Explain how the source illustrates the idea of time-space compression.', 'It claims virtual presence will make physical distance irrelevant (no commute, instant presence), compressing space and time through digital technology; it is also a promotional claim from a company investing heavily in the metaverse.')],
    evaluate=[('Digital technology has made geographical location irrelevant.',
               ['remote work and online learning across borders', 'instant global communication and virtual events'],
               ['infrastructure, cost and speed vary greatly by place', 'national laws, firewalls and geo-blocking', 'rural and low-income regions remain offline'],
               'Digital technology reduces the importance of distance for some people and activities, but location still shapes access, rights and experience.'),
              ('Data localisation laws protect citizens more than they harm them.',
               ['data subject to local privacy law and courts', 'protection from foreign surveillance; support local industry'],
               ['can help governments access data for surveillance', 'raises costs for small firms', 'fragments the internet ("splinternet")'],
               'Localisation can strengthen protection where strong local privacy law exists, but in states with weak rights it can increase surveillance; its value depends on governance.')],
    extended=[('Analyse how one virtual space has changed the way a community interacts, and evaluate whether it complements or replaces physical space.', 'E.g. Roblox/Minecraft for young people, VRChat, Discord communities, Fortnite events; analyse new interactions, economies, rules; evaluate complement vs replacement with evidence.', 6, 'long')],
))

R.facts('ch04-st2', F(
    terms=[('system', 'a set of interacting components that work together, with inputs, processes and outputs, within a boundary and environment'),
           ('feedback loop', 'a process in which the outputs of a system are fed back as inputs, either amplifying (positive feedback) or stabilising (negative feedback) the system'),
           ('emergent behaviour', 'patterns that arise from interactions between many parts of a system that cannot be predicted from any single part, such as a viral trend'),
           ('positive feedback', 'feedback that amplifies a change, for example content that gets engagement being shown to more people and getting even more engagement'),
           ('negative feedback', 'feedback that counteracts a change and keeps a system stable, such as a thermostat switching heating off when a temperature is reached'),
           ('interdependence', 'the mutual reliance of components or systems, so that a failure in one can spread to others')],
    facts=[('On 6 May 2010, US stock markets briefly lost about a trillion dollars in value within minutes. What is this event known as?', 'The Flash Crash', ['Black Monday', 'The Dot-com Crash', 'The Y2K bug'], 'Automated trading algorithms interacting rapidly amplified the fall – an emergent system effect.'),
           ('Which of the following is an example of positive feedback in a digital system?', 'A recommendation algorithm promoting videos that get many views, which then get even more views',
            ['A thermostat turning off heating at 21 °C', 'A spam filter blocking a known virus', 'A backup copying files every night'], 'Positive feedback amplifies an initial change.'),
           ('A faulty CrowdStrike software update in July 2024 crashed millions of Windows computers worldwide. Which systems concept does this best illustrate?', 'Interdependence',
            ['Anonymity', 'Remix culture', 'Data sovereignty'], 'About 8.5 million devices failed, disrupting airlines, banks and hospitals that depended on the same software.'),
           ('Which of the following is part of a system\'s environment rather than its components?', 'The laws and regulations a ride-hailing platform must follow',
            ['The app\'s matching algorithm', 'The drivers\' smartphones', 'The platform\'s servers'], 'The environment is what surrounds and affects the system from outside its boundary.')],
    why=[('Explain why predictive policing systems can create feedback loops.', 'If police are sent where the algorithm predicts crime, they record more crime there, which is fed back as training data, so the system predicts even more crime in the same areas – reinforcing existing patterns regardless of actual crime rates.'),
         ('Explain why emergent behaviour makes digital systems hard to control.', 'Outcomes such as viral trends, market crashes or misinformation cascades arise from millions of interactions rather than one designer\'s decision, so they cannot be fully predicted or controlled by changing one component.'),
         ('Explain why thinking in systems helps analyse the impacts of a digital technology.', 'A systems view looks at components, interactions, feedback and environment, so it reveals indirect and unintended effects (e.g. ride-hailing affecting congestion, public transport and labour law) that a focus on the device alone would miss.')],
    contrast=[('positive feedback', 'negative feedback', 'Positive feedback amplifies change (e.g. viral sharing); negative feedback counteracts change and stabilises the system (e.g. rate limits on forwarding messages).'),
              ('a component of a system', 'the environment of a system', 'A component is a part inside the system boundary that interacts with other parts (e.g. an algorithm, servers, users); the environment is outside the boundary but influences it (e.g. law, culture, economy).')],
    misc=[('If each part of a system works correctly, the whole system will behave as intended.', 'Interactions between correctly working parts can produce emergent, unintended behaviour (e.g. trading algorithms each following rules but together causing the 2010 Flash Crash).'),
          ('Feedback loops in digital systems are always harmful.', 'Negative feedback can stabilise systems (e.g. WhatsApp forwarding limits slowing rumours; thermostats in smart homes), and positive feedback can spread useful content quickly.')],
    cases=[('the 2010 Flash Crash', 'On 6 May 2010 the Dow Jones fell nearly 1,000 points in minutes and recovered within about half an hour; regulators linked it to a large automated sell order and interacting high-frequency trading algorithms.', 'emergent behaviour in systems',
            'no single algorithm intended a crash, but their rapid interactions produced a system-wide collapse, illustrating emergence and interdependence.'),
           ("WhatsApp's forwarding limits", 'After rumours spread on WhatsApp were linked to mob violence in India in 2018, WhatsApp limited forwarding (to five chats, then one chat for frequently forwarded messages in 2020).', 'negative feedback in a system',
            'adding friction slowed the amplifying loop of mass forwarding, showing how design changes can stabilise a system.'),
           ('the CrowdStrike outage (July 2024)', 'A faulty update to CrowdStrike\'s Falcon security software caused about 8.5 million Windows devices to crash, grounding flights and disrupting hospitals and banks.', 'interdependence',
            'because many organisations relied on the same component, one failure cascaded across sectors and countries.')],
    sources=[('"Each trading algorithm did exactly what it was programmed to do. Together, they did something no one programmed."', 'Financial journalist, commentary on the 2010 Flash Crash',
              'Explain how the source illustrates the concept of emergent behaviour.', 'The crash was not designed by any single program; it emerged from interactions among many algorithms, each behaving correctly, which is the definition of emergence.'),
             ('"When we limited forwards, the number of forwarded messages on WhatsApp fell by 25%."', 'WhatsApp blog post, 2019',
              'Explain how the intervention described works as negative feedback.', 'Limiting forwards adds friction to the sharing loop, reducing how quickly messages multiply; this counteracts the amplifying positive feedback of viral forwarding.')],
    evaluate=[('Complex digital systems are now too interconnected to be safe.',
               ['single failures cascade globally (CrowdStrike 2024)', 'emergent behaviour (Flash Crash) is hard to predict'],
               ['redundancy, circuit breakers and testing reduce risks', 'interconnection also allows rapid recovery and updates', 'most systems work reliably most of the time'],
               'Interconnection creates real systemic risk, but it can be managed through redundancy, diversity of suppliers and regulation; "too interconnected to be safe" overstates it.'),
              ('Designers are responsible for the emergent effects of the systems they create.',
               ['they choose features that make amplification likely', 'they can monitor and change designs (forward limits)'],
               ['emergent effects arise from users and environment beyond designer control', 'responsibility is shared with users, regulators and other systems'],
               'Designers carry significant responsibility for foreseeable effects and for responding once harms emerge, but responsibility is shared across the system.')],
    extended=[('Using a systems approach, analyse one digital system you have studied, identifying its components, a feedback loop and an emergent effect.', 'E.g. a recommendation system: components (users, content, algorithm, advertisers), feedback (engagement → more promotion), emergent effect (viral trends, polarisation); include environment (regulation). Reward clear system mapping and explanation.', 6, 'long')],
))

R.facts('ch04-st3', F(
    terms=[('consequentialism', 'an ethical approach that judges actions by their outcomes, such as utilitarianism\'s aim of the greatest good for the greatest number'),
           ('deontology', 'an ethical approach that judges actions by whether they follow moral duties or rules, regardless of consequences (associated with Immanuel Kant)'),
           ('virtue ethics', 'an ethical approach that asks what a person of good character (honest, fair, courageous) would do (associated with Aristotle)'),
           ('utilitarianism', 'a consequentialist theory (Bentham, Mill) that the right action produces the greatest overall happiness or well-being'),
           ('categorical imperative', 'Kant\'s principle that one should act only on rules that could be universal laws and treat people as ends, never merely as means'),
           ('ethical dilemma', 'a situation in which competing values or duties conflict, so that every option involves some moral cost')],
    facts=[('Which philosopher is most associated with deontological ethics and the categorical imperative?', 'Immanuel Kant', ['John Stuart Mill', 'Aristotle', 'Jeremy Bentham'], 'Kant, Groundwork of the Metaphysics of Morals (1785).'),
           ('Which ethical approach would most likely support mass surveillance if it prevented more harm than it caused?', 'Utilitarianism', ['Kantian deontology', 'Virtue ethics', 'Ethical egoism'], 'Utilitarianism weighs total outcomes.'),
           ('In 2016 Apple refused an FBI request to help unlock an iPhone used in which attack?', 'The San Bernardino shooting', ['The Boston Marathon bombing', 'The 9/11 attacks', 'The Christchurch mosque attacks'], 'Apple argued that creating a backdoor would endanger all users; the FBI later accessed the phone with outside help.'),
           ('Which of the following questions reflects a virtue ethics approach to a digital dilemma?', 'What would an honest and caring engineer do in this situation?',
            ['Which option produces the most total benefit?', 'Which rule must never be broken?', 'What is legal in this country?'], 'Virtue ethics focuses on character.')],
    why=[('Explain why a utilitarian and a deontologist might disagree about using facial recognition in public spaces.', 'A utilitarian may support it if it catches more criminals than the harm caused; a deontologist may oppose it because it treats everyone as a suspect and violates a duty to respect privacy and consent, regardless of benefits.'),
         ('Explain why ethical frameworks are useful when evaluating digital dilemmas.', 'They give structured ways to weigh competing values (privacy, safety, fairness), make reasoning explicit and reveal why reasonable people disagree, rather than relying on gut reactions.'),
         ('Explain why legal and ethical are not the same in digital society.', 'Laws lag behind technology and vary between countries; some legal practices (e.g. data brokers selling location data) may be unethical, while some ethical actions (whistle-blowing) may be illegal.')],
    contrast=[('consequentialism', 'deontology', 'Consequentialism judges an action by its outcomes (e.g. whether encryption backdoors prevent more harm than they cause); deontology judges it by whether it respects duties and rights (e.g. never deceiving users), regardless of outcomes.'),
              ('virtue ethics', 'rule-based ethics', 'Virtue ethics asks what a person of good character would do in context; rule-based (deontological) ethics asks which universal duties apply.')],
    misc=[('If a technology is legal, it must be ethical.', 'Legality and ethics differ: laws lag behind technology and differ by country (e.g. the sale of location data by brokers is legal in many places but raises serious ethical concerns).'),
          ('Utilitarianism always protects individual privacy.', 'Utilitarianism can justify sacrificing an individual\'s privacy if the total benefit (e.g. public health tracking) outweighs the harm; rights-based approaches give stronger protection.')],
    cases=[('Apple v FBI (2016)', 'The FBI obtained a court order asking Apple to create software to bypass security on the San Bernardino attacker\'s iPhone; Apple refused, and the FBI dropped the case after a third party unlocked the phone.', 'an ethical dilemma between security and privacy',
            'a utilitarian case for access (investigating terrorism) conflicted with a duty-based and consequential argument against weakening security for all users.'),
           ('the Cambridge Analytica scandal (2018)', 'Data from up to 87 million Facebook users were harvested through a personality-quiz app built by Aleksandr Kogan and used for political profiling.', 'deontological ethics and consent',
            'users (and their friends) were used as means to political ends without informed consent, which Kantian ethics condemns regardless of any benefits.'),
           ('COVID-19 contact-tracing apps', 'Many countries launched apps in 2020; some (e.g. using the Google/Apple exposure notification framework) stored data on phones, others used centralised databases.', 'consequentialist reasoning about public health and privacy',
            'governments weighed the health benefits of tracing against privacy harms, and design choices (decentralised vs centralised) changed that balance.')],
    sources=[('"The government is asking Apple to hack our own users and undermine decades of security advancements that protect our customers."', 'Tim Cook, "A Message to Our Customers", Apple, 16 February 2016',
              'Identify the ethical argument used in the source and explain it.', 'It is a rights/duty-based (and consequential) argument: Apple has a duty to protect customers\' security; creating a backdoor would harm all users, so it should refuse even for a legitimate investigation.'),
             ('"Act in such a way that you treat humanity, whether in your own person or in that of another, always as an end and never merely as a means."', 'Immanuel Kant, Groundwork of the Metaphysics of Morals (1785)',
              'Explain how this principle could be applied to targeted advertising based on personal data.', 'Using people\'s data to manipulate their choices without informed consent treats them merely as a means to profit; Kant\'s principle would require transparency and genuine consent, treating users as rational agents.')],
    evaluate=[('Consequentialism is the most useful ethical framework for judging new digital technologies.',
               ['digital impacts are measurable (harms, benefits, scale)', 'helps policymakers weigh trade-offs such as safety vs privacy'],
               ['consequences are uncertain and hard to predict', 'it can justify harming minorities for majority benefit', 'rights-based limits (privacy, dignity) are needed'],
               'Consequentialism is valuable for weighing large-scale impacts, but it should be combined with rights-based constraints so minorities are not sacrificed for aggregate gains.'),
              ('Technology companies should prioritise user privacy over law-enforcement requests.',
               ['strong encryption protects everyone, including against criminals and authoritarian states', 'backdoors cannot be limited to "good" actors'],
               ['serious crimes (child abuse, terrorism) may go uninvestigated', 'democratic legal processes have legitimate authority'],
               'Companies should resist blanket weakening of security but cooperate with lawful, targeted and proportionate requests; the balance depends on safeguards and the legal system.')],
    extended=[('Apply two ethical frameworks to one digital dilemma you have studied and evaluate which provides the more convincing guidance.', 'E.g. live facial recognition, end-to-end encryption, or children\'s use of social media; apply consequentialism (weigh benefits/harms) and deontology or virtue ethics (duties, rights, character); compare their conclusions and evaluate.', 6, 'long')],
))
AR('ch04-st3', [
    ('A utilitarian could support a contact-tracing app that collects location data.', 'Utilitarianism judges actions by whether they maximise overall well-being.', 'a',
     'If public-health benefits outweigh privacy harms, utilitarian reasoning supports it.'),
    ('Kantian ethics judges actions mainly by their consequences.', 'Kant argued that people must be treated as ends and never merely as means.', 'd',
     'Kant is deontological (duty-based), so A is false; R is a correct statement of the categorical imperative.'),
])

# Paper 2 source set – chapter 3 (identity and power)
P2['ch03'] = dict(
    src=[('"Since the government linked pensions to fingerprint authentication, elderly residents in our district have walked to the ration shop three or four times before the machine accepts them. Some give up. The system was meant to stop fraud, but the old and the sick are paying the price."', 'Field report by a welfare-rights organisation, Jharkhand, India, 2018',
          'Identify two problems with biometric authentication described in {S}.', ['repeated failed fingerprint scans / authentication failures', 'elderly and sick people giving up and losing access to rations (exclusion)'],
          'Explain why {S} might be considered a valuable source for an inquiry into digital identity.', 'It gives first-hand, ground-level evidence of how authentication works in practice for vulnerable people, a perspective often missing from official statistics; its value is limited by its campaigning purpose and local scope.'),
         ('"Aadhaar has saved the government tens of thousands of crore rupees by removing ghost and duplicate beneficiaries, and has given more than a billion residents a verifiable identity for the first time."', 'Statement attributed to a senior official of the Unique Identification Authority of India (UIDAI), 2019',
          'Identify two benefits of Aadhaar claimed in {S}.', ['removal of ghost/duplicate beneficiaries saving public money', 'a verifiable identity for over a billion residents'],
          'Explain one reason why the claims in {S} should be treated with caution.', 'The source comes from the agency that runs Aadhaar, so it has an interest in presenting it positively; the savings figures have been disputed by independent researchers, and the source does not mention exclusion errors.'),
         ('"Platforms do not just host speech; they decide what gets seen. That is a form of power no newspaper editor ever had over billions of people."', 'Technology policy researcher, interview with a European broadcaster, 2021',
          'Identify two ways in which platforms exercise power according to {S}.', ['deciding what content gets seen (ranking/visibility)', 'reaching/controlling billions of people at once'],
          'Explain what {S} suggests about the difference between platform power and traditional media power.', 'Platforms shape visibility through algorithms at a global scale for billions of users, while editors controlled a single publication; the power is larger and less visible.')],
    cmp=[(0, 1, 'the impacts of a digital identity system', ['both agree Aadhaar affects access to welfare', 'both concern the reliability of identification'],
          ['Source A stresses exclusion of vulnerable people; Source B stresses savings and inclusion', 'Source A is ground-level testimony; Source B is an official, aggregate claim', 'A presents the system as failing its users; B presents it as a success']),
         (1, 2, 'power held by organisations that run digital systems', ['both describe organisations with influence over very large populations', 'both imply control over access (to welfare or to visibility)'],
          ['Source B presents this power as beneficial and administrative; Source C presents it as a concern', 'B is about state power; C is about private platform power'])],
    ev=[(0, 1, 'digital identity systems empower citizens more than they control them.', ['identity enables access to banking and welfare (Source B)', 'Aadhaar reduced duplicate beneficiaries; Estonia\'s e-ID enables online services'],
         ['authentication failures exclude the vulnerable (Source A)', 'centralised data enables surveillance and function creep', 'the Supreme Court (2018) had to limit private use of Aadhaar']),
        (1, 2, 'organisations that control digital systems are accountable for how they use their power.', ['courts and regulators can intervene (Puttaswamy, DMA)', 'oversight bodies such as Meta\'s Oversight Board'],
         ['algorithmic decisions are opaque (Source C)', 'official sources may downplay harms (Source B)', 'affected people have little voice (Source A)'])],
)

# =============================================================================================
# ch05 Content 3.1 Data: types, collection and storage, representation
# =============================================================================================
DATA_ITEMS = [  # (item, qualitative/quantitative, structured/unstructured)
    ('the number of steps recorded by a fitness tracker each day', 'quantitative', 'structured'),
    ('customer reviews written in a free-text box on a shopping site', 'qualitative', 'unstructured'),
    ('a spreadsheet of students\' exam scores', 'quantitative', 'structured'),
    ('recorded voice messages sent on WhatsApp', 'qualitative', 'unstructured'),
    ('the temperature readings from a smart thermostat logged every minute', 'quantitative', 'structured'),
    ('photographs uploaded to Instagram', 'qualitative', 'unstructured'),
    ('the price and quantity of each item in a supermarket sales database', 'quantitative', 'structured'),
    ('transcripts of interviews with gig workers', 'qualitative', 'unstructured'),
    ('the heart rate (beats per minute) from a smartwatch', 'quantitative', 'structured'),
    ('videos of protests posted on social media', 'qualitative', 'unstructured'),
    ('the colour of cars recorded in a car-park database as a category field', 'qualitative', 'structured'),
    ('a table of country names and their internet-penetration rates', 'quantitative', 'structured'),
]


@R.add('ch05-st1', 'C3', (1, 3), 'short')
def classify_data(rng, slot):
    k = 2 if slot.d <= 1 else 3
    items = rng.sample(DATA_ITEMS, k)
    dim = rng.choice(['qq', 'su', 'both'] if slot.d >= 2 else ['qq', 'su'])
    lines = '\n'.join(f'({"abc"[i]}) {it[0]}' for i, it in enumerate(items))
    if dim == 'qq':
        q = 'State whether each of the following is qualitative or quantitative data.'
        ans = '; '.join(f'({"abc"[i]}) {it[1]}' for i, it in enumerate(items))
    elif dim == 'su':
        q = 'State whether each of the following is structured or unstructured data.'
        ans = '; '.join(f'({"abc"[i]}) {it[2]}' for i, it in enumerate(items))
    else:
        q = 'Classify each of the following as qualitative or quantitative, and as structured or unstructured.'
        ans = '; '.join(f'({"abc"[i]}) {it[1]}, {it[2]}' for i, it in enumerate(items))
    return dict(stem=f'{q}\n{lines}', answer=ans, type='short', marks=k if dim != 'both' else 2 * k,
                markingKey=f'{ans}. 1 mark per correct classification. Quantitative = numerical/measurable; structured = organised in a predefined format (fields, rows).')


R.facts('ch05-st1', F(
    terms=[('data', 'raw facts and figures, such as numbers, text, images or sounds, that can be processed to produce information'),
           ('information', 'data that has been processed, organised or given context so that it has meaning'),
           ('qualitative data', 'descriptive data about qualities or characteristics that is not measured numerically, such as opinions or images'),
           ('quantitative data', 'numerical data that can be counted or measured, such as temperature or the number of likes'),
           ('structured data', 'data organised in a predefined format, such as rows and fields in a database table, which is easy to search'),
           ('unstructured data', 'data without a predefined model, such as emails, photos, videos and social-media posts'),
           ('metadata', 'data about data, such as the time, location, author or device recorded with a photo or phone call'),
           ('semi-structured data', 'data that has some organising tags or markers but not a rigid table structure, such as JSON or XML files')],
    facts=[('Which of the following is an example of metadata?', 'The GPS coordinates stored in a photo\'s EXIF data',
            ['The people shown in the photo', 'The colours in the photo', 'A caption describing the photo'], 'EXIF metadata can include time, camera model and location.'),
           ('Which of the following is an example of semi-structured data?', 'A JSON file returned by a weather app\'s API',
            ['A handwritten letter', 'A video recording of a lecture', 'A relational database table with fixed columns'], 'JSON uses keys and values as tags without a rigid schema.'),
           ('In 2012, a photo posted online revealed the location of fugitive John McAfee in Guatemala. What revealed it?', 'GPS metadata in the photo\'s EXIF data',
            ['Facial recognition', 'A hacked email', 'His IP address in a tweet'], 'Vice published a photo whose EXIF data included GPS coordinates.'),
           ('Which of the following is quantitative data?', 'The number of hours a user spends on TikTok per day',
            ['A user\'s favourite type of video', 'Comments on a video', 'A user\'s profile picture'], 'It is a numerical measurement.')],
    why=[('Explain why metadata can reveal as much about a person as the content of their communications.', 'Metadata shows who contacted whom, when, where and how often; patterns over time reveal relationships, routines, health concerns or political links without reading any content, which is why intelligence agencies collect it in bulk.'),
         ('Explain why most of the data created today is unstructured.', 'Much data comes from photos, videos, voice messages, emails and social-media posts, which do not fit into predefined fields; this makes it harder to search and analyse without techniques such as machine learning.'),
         ('Explain why data only becomes information when it is given context.', 'A figure such as "38" has no meaning until we know what it measures (e.g. 38 °C body temperature), so data must be processed and placed in context to be useful for decisions.')],
    contrast=[('data', 'information', 'Data are raw facts without context (e.g. a list of step counts); information is data processed into meaningful form (e.g. "you walked 20% less this week than last").'),
              ('structured data', 'unstructured data', 'Structured data fits a predefined model such as database fields (easy to sort and query); unstructured data, such as images or free text, has no fixed model and needs more complex processing.'),
              ('qualitative data', 'quantitative data', 'Qualitative data describes qualities in words or images (e.g. interview responses); quantitative data is numerical and measurable (e.g. download speed in Mbps).')],
    misc=[('Metadata is harmless because it does not include the content of a message.', 'Metadata (who, when, where, how long) can reveal relationships, movements and habits; former NSA director Michael Hayden said "we kill people based on metadata".'),
          ('Qualitative data cannot be analysed by computers.', 'Qualitative data such as text and images can be analysed using techniques like sentiment analysis, image recognition and natural language processing.')],
    cases=[('the NSA telephone metadata programme', 'Documents leaked by Edward Snowden in 2013 showed the US National Security Agency collected phone metadata (numbers, times, durations) of millions of Americans under Section 215 of the Patriot Act.', 'the significance of metadata',
            'even without recording calls, bulk metadata allowed analysis of social networks and movements, showing metadata is highly revealing personal data.'),
           ('the Strava global heatmap (2018)', 'Strava published a heatmap of users\' running and cycling routes; analysts noticed it revealed the layout of military bases where soldiers exercised with fitness trackers.', 'how quantitative location data can reveal sensitive information',
            'aggregated, seemingly anonymous GPS data exposed sensitive locations, showing that data types combined at scale create new meanings and risks.'),
           ('sentiment analysis of tweets', 'Companies and researchers analyse millions of posts to classify them as positive, negative or neutral about brands or politicians.', 'turning unstructured data into structured information',
            'natural language processing converts free text (unstructured, qualitative) into scores and categories (structured, quantitative) that can be counted and compared.')],
    sources=[('"We kill people based on metadata."', 'General Michael Hayden, former director of the NSA and CIA, debate at Johns Hopkins University, 2014',
              'Explain what the source suggests about the value of metadata.', 'It suggests metadata alone (who called whom, when and where) is detailed enough to identify targets for lethal action, so it is highly sensitive and revealing personal data.'),
             ('"Each day the world produces quintillions of bytes of data – most of it in the form of images, video and text that fit no spreadsheet."', 'Technology industry report, 2023',
              'Explain one challenge that the type of data described in the source creates for organisations.', 'Most of it is unstructured, so it cannot be easily stored in database tables or searched; organisations need specialised storage and techniques such as machine learning to extract useful information.')],
    evaluate=[('Metadata should be protected by law as strongly as the content of communications.',
               ['metadata reveals relationships, health and political links', 'it is collected in bulk without users\' awareness'],
               ['security agencies argue metadata is essential and less intrusive than reading content', 'some metadata is needed to run networks'],
               'Because aggregated metadata can be as revealing as content, it deserves strong protection, with narrowly defined exceptions overseen by courts.'),
              ('Quantitative data is more reliable than qualitative data for understanding the impact of a digital system.',
               ['numbers allow comparison, scale and trends', 'less open to individual interpretation'],
               ['numbers can be selected or framed to mislead', 'qualitative data captures experiences, meanings and causes', 'some impacts (dignity, trust) are hard to quantify'],
               'Each answers different questions; quantitative data shows scale and pattern, qualitative data explains experience and meaning, so the strongest inquiries combine both.')],
    extended=[('A city installs smart bins that record fill level, collection times and photos of dumped rubbish. Classify the data collected and evaluate one benefit and one risk of combining it with residents\' metadata.', 'Fill level and times: quantitative, structured; photos: qualitative, unstructured; metadata: location/time stamps. Benefit: efficient collection routes and less fuel. Risk: photos and location/time data could identify individuals, raising privacy and surveillance concerns. Reward correct classification and balanced evaluation.', 6, 'long')],
))
AR('ch05-st1', [
    ('A photo shared online can reveal where it was taken even if the image shows no landmarks.', 'Many cameras and phones store GPS coordinates in the image\'s EXIF metadata.', 'a', 'Location metadata travels with the file unless removed.'),
    ('Unstructured data is easier to search than structured data.', 'Structured data is organised into predefined fields and records.', 'd', 'Structured data is easier to query because of its fixed format; A is false.'),
])


@R.add('ch05-st2', 'C3', (1, 4), 'numerical')
def sensor_volume(rng, slot):
    frames = [('A smart electricity meter in a home in {c} records a reading every {s} seconds.', 'reading'),
              ('An air-quality sensor at a school in {c} logs one measurement every {s} seconds.', 'measurement'),
              ('A fitness tracker records the wearer\'s heart rate every {s} seconds.', 'heart-rate reading'),
              ('A traffic sensor on a road in {c} counts vehicles and stores a record every {s} seconds.', 'record')]
    fr, unit = rng.choice(frames)
    s = rng.choice([5, 10, 15, 30, 60])
    h = rng.choice([1, 2, 6, 12, 24])
    b = rng.choice([4, 8, 16, 32])
    per = 3600 // s * h
    total = per * b
    stem = fr.format(c=rng.choice(CITIES), s=s)
    if slot.d <= 2:
        stem += f' Calculate how many {unit}s are recorded in {h} hour{"s" if h > 1 else ""}.'
        ans = f'{per:,} {unit}s'
        key = f'(3600 ÷ {s}) × {h} = {per:,} [M1 A1].'
    else:
        stem += f' Each {unit} is stored as {b} bytes. Calculate the storage needed for {h} hour{"s" if h > 1 else ""} of data, in kilobytes (1 kB = 1000 bytes).'
        ans = f'{total / 1000:g} kB'
        key = f'Number of {unit}s = (3600 ÷ {s}) × {h} = {per:,} [M1]; bytes = {per:,} × {b} = {total:,} [M1]; = {total / 1000:g} kB [A1].'
        if slot.d >= 4:
            n = rng.choice([1000, 5000, 20000])
            stem += f' Then calculate the total for {n:,} such devices over a year (365 days), in gigabytes (1 GB = 10⁹ bytes).'
            yearly = total / h * 24 * 365 * n / 1e9
            ans += f'; {sci(yearly)} GB per year for {n:,} devices'
            key += f' Per device per day = {total / h * 24:,.0f} bytes; × 365 × {n:,} = {sci(yearly)} GB [M1 A1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical')


@R.add('ch05-st2', 'C3', (2, 4), 'numerical')
def survey_bias(rng, slot):
    sent = rng.choice([400, 500, 800, 1200, 2000])
    rate = rng.choice([12, 15, 20, 25, 30, 40])
    resp = sent * rate // 100
    yes = rng.randint(int(resp * 0.55), int(resp * 0.85))
    ctx = rng.choice([('an online survey about smartphone use', 'said they use their phone for more than four hours a day'),
                      ('an app-based survey about attitudes to AI in schools', 'said they support using AI chatbots for homework'),
                      ('an email survey about online banking', 'said they prefer banking through an app'),
                      ('a social-media poll about remote working', 'said they would prefer to work from home')])
    stem = (f'A researcher sends {ctx[0]} to {sent:,} people. {resp:,} respond, and {yes:,} of the respondents {ctx[1]}. '
            f'(a) Calculate the response rate. (b) Calculate the percentage of respondents who {ctx[1].replace("said they ", "")}.')
    a1 = resp / sent * 100
    a2 = yes / resp * 100
    ans = f'(a) {pc(a1)}% (b) {pc(a2)}%'
    key = f'(a) {resp} ÷ {sent} × 100 = {pc(a1)}% [A1]; (b) {yes} ÷ {resp} × 100 = {pc(a2)}% [A1].'
    m = 2
    if slot.d >= 3:
        stem += ' (c) Explain one reason why this result may not represent the whole population.'
        ans += '; (c) self-selection/non-response bias – only a minority responded and an online/app survey excludes people without access or interest'
        key += ' (c) e.g. low response rate means self-selected respondents; online collection excludes people without internet or digital skills [R1 R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch05-st2', F(
    terms=[('digital footprint', 'the trail of data a person leaves through online activity, both actively (posts) and passively (browsing, location)'),
           ('active digital footprint', 'data a person knowingly shares, such as posts, comments, photos and form entries'),
           ('passive digital footprint', 'data collected without the person actively sharing it, such as IP address, location history and browsing behaviour'),
           ('cookie', 'a small text file stored by a website in a user\'s browser to remember information such as log-in status or browsing activity'),
           ('third-party cookie', 'a cookie set by a domain other than the website being visited, typically used by advertisers to track users across sites'),
           ('browser fingerprinting', 'identifying a device by combining many characteristics (screen size, fonts, browser version) without storing a cookie'),
           ('sensor', 'a device that detects a physical property such as light, temperature, motion or location and converts it into data')],
    facts=[('Which of the following is part of a passive digital footprint?', 'The location history recorded by a phone\'s operating system',
            ['A tweet you write', 'A photo you upload to Instagram', 'A review you post on a shopping site'], 'Passive data is collected without the user actively sharing it.'),
           ('Which type of cookie is most commonly used to track users across many different websites for advertising?', 'Third-party cookies',
            ['Session cookies set by the visited site', 'First-party cookies for log-in', 'Strictly necessary cookies'], 'Third-party cookies are set by ad networks embedded on many sites.'),
           ('Which sensor in a smartphone detects the orientation and movement of the phone?', 'Accelerometer/gyroscope', ['Ambient light sensor', 'Microphone', 'Proximity sensor only'], 'Accelerometers and gyroscopes measure motion and rotation, used in step counting.'),
           ('What is the main source of data in "web scraping"?', 'Content automatically extracted from public web pages',
            ['Data typed in by survey respondents', 'Sensor readings from IoT devices', 'Paper records scanned by hand'], 'Scrapers use programs to collect data at scale, as Clearview AI did with images.')],
    why=[('Explain why passive data collection raises greater privacy concerns than active data collection.', 'Users often do not know passive data is being collected (location, browsing, device identifiers), so they cannot give meaningful consent or control it, and it can be combined to build detailed profiles.'),
         ('Explain why online surveys may produce biased data.', 'Only people with internet access and interest choose to respond (self-selection), so the sample may not represent the population; question wording and anonymity also affect answers.'),
         ('Explain why sensors in the Internet of Things have greatly increased the volume of data collected.', 'Sensors collect data automatically and continuously (e.g. every second) from billions of devices – meters, cars, wearables – without human input, so volume grows enormously.')],
    contrast=[('an active digital footprint', 'a passive digital footprint', 'An active footprint is data you deliberately share (posts, photos); a passive footprint is data collected about you without deliberate sharing (IP address, location, cookies).'),
              ('a cookie', 'browser fingerprinting', 'A cookie is a file stored on the user\'s browser that the user can delete; fingerprinting identifies a device from its characteristics without storing anything, so it is harder to block.')],
    misc=[('Deleting your social-media posts removes your digital footprint.', 'Passive data, copies, screenshots, backups and data held by third parties (advertisers, data brokers) remain; deletion only removes part of the active footprint.'),
          ('Using private/incognito browsing makes you invisible online.', 'Incognito mode only stops the browser saving local history and cookies after the session; websites, internet providers and employers can still see activity, and fingerprinting still works.')],
    cases=[('Clearview AI', 'Clearview AI scraped billions of facial images from social media and websites to build a facial-recognition tool sold to police; regulators in several countries (e.g. Italy, France, the Netherlands, the UK) fined or ordered it to delete data.', 'data collection by web scraping',
            'images people shared for social purposes were collected without consent for a different purpose (identification), showing how public data can be repurposed.'),
           ("Target's pregnancy prediction (reported 2012)", 'The New York Times reported that the US retailer Target analysed purchases (e.g. unscented lotion, supplements) to predict which customers were pregnant and send baby-product coupons.', 'passive data and inference',
            'routine purchase data was combined to infer sensitive information customers had not shared, illustrating the power of passive data collection.'),
           ('smart electricity meters', 'Smart meters record household electricity use at short intervals and send it to energy companies.', 'sensor-based data collection',
            'fine-grained readings help manage the grid and bills, but patterns can reveal when people are home, asleep or away.')],
    sources=[('"I deleted my account in 2019. In 2023 I discovered my photos were part of a facial-recognition database used by police in three countries."', 'Testimony to a European data-protection authority, 2023',
              'With reference to the source, explain why deleting an account may not remove a person\'s digital footprint.', 'Data may already have been copied or scraped by third parties (e.g. Clearview AI) before deletion, and the person has no control over those copies.'),
             ('"By clicking Accept All, you agree to the use of cookies by us and our 847 partners."', 'Cookie consent banner on a news website, 2024',
              'Explain one problem with this form of consent.', 'Users cannot realistically read or understand the policies of 847 partners, so "consent" is not genuinely informed; banners often nudge users to accept (dark patterns).')],
    evaluate=[('Users are responsible for the size of their own digital footprint.',
               ['users choose what to post and which apps to use', 'privacy settings and ad blockers are available'],
               ['much data is collected passively and invisibly', 'consent banners are designed to nudge acceptance', 'others can post data about you'],
               'Users control part of their active footprint, but passive collection by platforms and data brokers means responsibility lies largely with organisations and regulators.'),
              ('Sensor data from smart devices does more good than harm.',
               ['efficiency in energy, transport and health monitoring', 'early warning (air quality, falls in elderly people)'],
               ['continuous monitoring reveals routines and habits', 'security weaknesses in IoT devices', 'data used for insurance or marketing without clear consent'],
               'Benefits are significant where data is minimised, secured and used for clear purposes; without these safeguards, the privacy harms can outweigh them.')],
    extended=[('Analyse how a smartphone collects both active and passive data during a single day of use, and evaluate how far users can control this.', 'Active: messages, posts, searches, photos; passive: GPS, Wi-Fi, accelerometer, app usage, cookies, advertising ID; control: permissions, settings, Apple App Tracking Transparency (2021), limits of control (pre-installed apps, data brokers); conclude.', 6, 'long')],
))

UNITS = [('kB', 10 ** 3), ('MB', 10 ** 6), ('GB', 10 ** 9), ('TB', 10 ** 12)]


@R.add('ch05-st3', 'C3', (1, 4), 'numerical')
def storage_calc(rng, slot):
    kind = rng.choice(['photos', 'videos', 'records', 'backup'])
    if kind == 'photos':
        n = rng.choice([500, 1200, 2500, 4000, 8000])
        size = rng.choice([2.5, 3, 4, 4.5, 6])
        tot = n * size
        stem = f'{name(rng)} has {n:,} photos on a phone, each about {size:g} MB. Calculate the total storage in GB (1 GB = 1000 MB).'
        ans = f'{tot / 1000:g} GB'
        key = f'{n:,} × {size:g} MB = {tot:,.0f} MB [M1]; ÷ 1000 = {tot / 1000:g} GB [A1].'
        if slot.d >= 3:
            plan = rng.choice([15, 50, 100, 200])
            stem += f' A cloud plan offers {plan} GB. State whether the photos fit and how much space remains or is lacking.'
            diff = plan - tot / 1000
            ans += f'; {"fits, " + format(diff, "g") + " GB remain" if diff >= 0 else "does not fit, " + format(-diff, "g") + " GB short"}'
            key += f' {plan} − {tot / 1000:g} = {diff:g} GB [A1].'
    elif kind == 'videos':
        mins = rng.choice([10, 30, 45, 90])
        rate = rng.choice([3, 5, 8, 25])  # Mbps
        mb = rate * mins * 60 / 8
        stem = (f'A streaming service sends video at {rate} megabits per second (Mbps). Calculate the amount of data used to watch a {mins}-minute programme, '
                f'in megabytes (8 bits = 1 byte).')
        ans = f'{mb:g} MB'
        key = f'{rate} × {mins} × 60 = {rate * mins * 60:,} megabits [M1]; ÷ 8 = {mb:g} MB [A1].'
        if slot.d >= 3:
            stem += ' Express this in gigabytes (1 GB = 1000 MB).'
            ans += f' = {mb / 1000:g} GB'
            key += f' ÷ 1000 = {mb / 1000:g} GB [A1].'
    elif kind == 'records':
        n = rng.choice([20000, 50000, 120000, 1500000])
        fields = rng.choice([(['name', 50], ['date of birth', 10], ['ID number', 12], ['email', 40]),
                             (['product code', 8], ['description', 60], ['price', 8], ['stock level', 4]),
                             (['student ID', 6], ['surname', 30], ['grade', 2], ['house', 12])])
        per = sum(f[1] for f in fields)
        tot = per * n
        stem = (f'A database table stores {n:,} records. Each record has the fields ' + ', '.join(f'{f[0]} ({f[1]} bytes)' for f in fields) +
                '. Calculate the size of the table in megabytes (1 MB = 10⁶ bytes), ignoring overheads.')
        ans = f'{tot / 1e6:g} MB'
        key = f'Bytes per record = {" + ".join(str(f[1]) for f in fields)} = {per} [M1]; × {n:,} = {tot:,} bytes [M1]; = {tot / 1e6:g} MB [A1].'
    else:
        tb = rng.choice([2, 5, 12, 40])
        mbps = rng.choice([100, 200, 500, 1000])
        secs = tb * 8e12 / (mbps * 1e6)
        hrs = secs / 3600
        stem = (f'A school in {rng.choice(CITIES)} wants to back up {tb} TB of data to a cloud data centre over a {mbps} Mbps connection. '
                f'Calculate how long the upload would take in hours, assuming the full speed is achieved (1 TB = 10¹² bytes).')
        ans = f'{hrs:.1f} hours'
        key = f'{tb} × 10¹² × 8 = {tb * 8:g} × 10¹² bits [M1]; ÷ ({mbps} × 10⁶) = {secs:,.0f} s [M1]; ÷ 3600 = {hrs:.1f} h [A1].'
        if slot.d >= 4:
            stem += ' Suggest one reason why the real upload would take longer.'
            ans += '; e.g. network congestion/shared bandwidth or protocol overheads'
            key += ' Reason e.g. contention, overheads, upload speed lower than download [R1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical')


SQL_ROWS = [('Amara', 'Nairobi', 17, 'HL'), ('Lukas', 'Vienna', 16, 'SL'), ('Priya', 'Mumbai', 17, 'HL'), ('Kenji', 'Seoul', 18, 'SL'),
            ('Sofia', 'Lima', 16, 'HL'), ('Omar', 'Dubai', 17, 'SL'), ('Mei', 'Hanoi', 18, 'HL'), ('Diego', 'Bogotá', 16, 'SL')]


@R.add('ch05-st3', 'C3', (2, 4), 'short')
def query_table(rng, slot):
    rows = rng.sample(SQL_ROWS, 6)
    tbl = 'Name | City | Age | Level\n' + '\n'.join(f'{r[0]} | {r[1]} | {r[2]} | {r[3]}' for r in rows)
    q = rng.choice(['age', 'level', 'both'])
    if q == 'age':
        a = rng.choice([16, 17])
        res = [r[0] for r in rows if r[2] > a]
        cond = f'Age > {a}'
    elif q == 'level':
        lv = rng.choice(['HL', 'SL'])
        res = [r[0] for r in rows if r[3] == lv]
        cond = f"Level = '{lv}'"
    else:
        lv = rng.choice(['HL', 'SL'])
        a = 16
        res = [r[0] for r in rows if r[3] == lv and r[2] > a]
        cond = f"Level = '{lv}' AND Age > {a}"
    if not res:
        return None
    stem = (f'A school database table Students contains:\n{tbl}\n\nState the names returned by the query: SELECT Name FROM Students WHERE {cond};')
    m = 2
    if slot.d >= 3:
        stem += ' Then identify the field that would be most suitable as a primary key if a StudentID field were not available, and explain why Name is a poor choice.'
        m = 4
    ans = ', '.join(res)
    key = f'{ans} [A1 for all correct, A1 for no extras].'
    if m == 4:
        ans += '; no existing field is guaranteed unique – Name can be repeated, so a unique StudentID should be added'
        key += ' Primary key must be unique for every record; names (and cities, ages) can repeat, so none is suitable – a unique ID is needed [R1 R1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='short', marks=m)


R.facts('ch05-st3', F(
    terms=[('database', 'an organised collection of structured data that can be stored, searched and updated efficiently'),
           ('relational database', 'a database that stores data in linked tables of rows (records) and columns (fields), queried with languages such as SQL'),
           ('primary key', 'a field whose value uniquely identifies each record in a database table'),
           ('cloud storage', 'storing data on remote servers owned by a provider and accessed over the internet'),
           ('data centre', 'a building housing large numbers of servers, storage and networking equipment, with power and cooling systems'),
           ('Software as a Service (SaaS)', 'a cloud model in which applications are hosted by a provider and used over the internet, such as Google Docs or Microsoft 365'),
           ('backup', 'a copy of data stored separately so that it can be restored if the original is lost or damaged')],
    facts=[('Which of the following is a cloud service model in which the provider supplies virtual servers and storage that customers manage themselves?', 'Infrastructure as a Service (IaaS)',
            ['Software as a Service (SaaS)', 'Platform as a Service (PaaS)', 'Peer-to-peer networking'], 'IaaS (e.g. Amazon EC2) provides computing infrastructure; customers install and manage their own software.'),
           ('Which language is most commonly used to query relational databases?', 'SQL', ['HTML', 'CSS', 'JSON'], 'Structured Query Language is the standard for relational databases.'),
           ('Approximately what share of the world\'s electricity do data centres use, according to recent IEA estimates?', 'About 1–2%', ['About 15–20%', 'About 40%', 'Less than 0.01%'], 'The IEA estimated around 1.5% of global electricity use in 2024 and rising with AI.'),
           ('Which company had the largest share of the global cloud infrastructure market in the mid-2020s?', 'Amazon Web Services', ['IBM', 'Oracle', 'Dropbox'], 'AWS led, followed by Microsoft Azure and Google Cloud.')],
    why=[('Explain why organisations increasingly store data in the cloud rather than on their own servers.', 'Cloud providers offer scalable storage on demand, lower upfront costs, automatic backups and access from anywhere; organisations pay for what they use instead of buying and maintaining hardware.'),
         ('Explain why a primary key is needed in a database table.', 'Each record must be uniquely identifiable so it can be found, updated or linked to other tables without confusion; names or dates can repeat, so a unique key avoids duplicates and errors.'),
         ('Explain why the location of data centres matters for digital society.', 'Data centres use large amounts of electricity and water, so their location affects local energy grids and environments; they are also subject to the laws of the country where they are, which affects privacy and government access.')],
    contrast=[('local storage', 'cloud storage', 'Local storage keeps data on devices the user owns (hard drive, USB); cloud storage keeps data on a provider\'s remote servers accessed over the internet, trading control for convenience and scalability.'),
              ('SaaS', 'IaaS', 'SaaS provides ready-to-use applications over the internet (e.g. Gmail); IaaS provides virtual hardware (servers, storage) on which customers run their own software.')],
    misc=[('Data in the cloud cannot be lost.', 'Cloud data can be lost through outages, accidental deletion, ransomware, account closure or provider failure (e.g. the 2021 OVHcloud data-centre fire in Strasbourg destroyed customer data).'),
          ('A database is just a big spreadsheet.', 'Databases enforce structure (data types, primary keys), link tables through relationships, support many simultaneous users and are queried with languages such as SQL, unlike a single spreadsheet.')],
    cases=[('the OVHcloud fire in Strasbourg (2021)', 'In March 2021 a fire destroyed one of OVHcloud\'s data-centre buildings in Strasbourg, taking millions of websites offline; some customers without off-site backups permanently lost data.', 'the physical reality of cloud storage',
            'the "cloud" is physical infrastructure that can fail, so backup strategies and redundancy across locations are essential.'),
           ("Ireland's data centres", 'Data centres used about a fifth of Ireland\'s metered electricity by 2023, according to the Central Statistics Office, prompting limits on new connections near Dublin.', 'environmental impacts of data storage',
            'growing demand for cloud storage and AI concentrates energy use in particular places, creating local trade-offs with housing and climate targets.'),
           ('Aadhaar\'s Central Identities Data Repository', 'India stores Aadhaar biometric and demographic data in a central database managed by UIDAI.', 'centralised data storage and security',
            'centralising data on over a billion people makes services efficient but creates a high-value target, so security failures could have national consequences.')],
    sources=[('"There is no cloud, it\'s just someone else\'s computer."', 'Popular slogan printed on stickers and T-shirts in the tech community, c. 2014',
              'Explain what the source suggests about cloud storage.', 'Cloud data is stored on physical servers owned and controlled by another organisation, so users depend on that provider for security, availability and privacy.'),
             ('"Data centres consumed 21% of all metered electricity in Ireland in 2023, up from 5% in 2015."', 'Central Statistics Office, Ireland, 2024',
              'Using the source, explain one implication of the growth of cloud storage.', 'Rapid growth of data centres increases electricity demand, which can strain the national grid and make climate targets harder to meet; Ireland responded by restricting new connections in the Dublin area.')],
    evaluate=[('Storing personal data in the cloud is safer than storing it on personal devices.',
               ['professional security, encryption and redundancy', 'automatic backups protect against device loss'],
               ['large providers are attractive targets for hackers', 'users lose control and depend on provider policies', 'governments may access data under local laws'],
               'For most users the cloud is safer against loss and many attacks, but it shifts risks to provider security and legal access; strong passwords, 2FA and encryption matter.'),
              ('The benefits of large data centres outweigh their environmental costs.',
               ['they power essential services and economies', 'they are more energy-efficient per task than many small server rooms'],
               ['huge electricity and water use; AI demand growing fast', 'local strain on grids (Ireland)', 'e-waste from hardware refresh cycles'],
               'Data centres are essential, but benefits only outweigh costs if they run on renewable energy, efficient cooling and are sited sensibly.')],
    extended=[('A hospital is deciding whether to move patient records from its own servers to a cloud provider. Evaluate this decision for two stakeholders.', 'Stakeholders: patients (privacy, availability), hospital (cost, scalability, security responsibility), staff (access), regulators (GDPR/HIPAA compliance, data location); consider breaches, outages, vendor lock-in; reach a recommendation.', 6, 'long')],
))


def to_bin(n, bits=8):
    return format(n, f'0{bits}b')


@R.add('ch05-st4', 'C3', (1, 3), 'numerical')
def binary_conv(rng, slot):
    mode = rng.choice(['d2b', 'b2d', 'hex'] if slot.d >= 2 else ['d2b', 'b2d'])
    n = rng.randint(5, 250) if slot.d >= 2 else rng.randint(3, 60)
    if mode == 'd2b':
        b = to_bin(n)
        return dict(stem=f'Convert the denary number {n} into an 8-bit binary number.', answer=b,
                    markingKey=f'{n} = ' + ' + '.join(str(2 ** i) for i in range(7, -1, -1) if n & (1 << i)) + f' → {b} [A1 A1].', type='numerical', marks=2)
    if mode == 'b2d':
        b = to_bin(n)
        return dict(stem=f'Convert the 8-bit binary number {b} into denary.', answer=str(n),
                    markingKey=f'Place values 128 64 32 16 8 4 2 1: ' + ' + '.join(str(2 ** i) for i in range(7, -1, -1) if n & (1 << i)) + f' = {n} [M1 A1].', type='numerical', marks=2)
    h = format(n, '02X')
    return dict(stem=f'Convert the denary number {n} into hexadecimal, showing your working.', answer=h,
                markingKey=f'{n} ÷ 16 = {n // 16} remainder {n % 16} → {h} (binary {to_bin(n)}) [M1 A1].', type='numerical', marks=2)


@R.add('ch05-st4', 'C3', (2, 5), 'numerical')
def media_size(rng, slot):
    kind = rng.choice(['image', 'sound', 'compress'])
    if kind == 'image':
        w, h = rng.choice([(640, 480), (800, 600), (1024, 768), (1920, 1080), (1280, 720)])
        depth = rng.choice([1, 8, 16, 24])
        bits = w * h * depth
        kb = bits / 8 / 1000
        stem = f'A bitmap image is {w} × {h} pixels with a colour depth of {depth} bit{"s" if depth > 1 else ""}. Calculate the file size in kilobytes (1 kB = 1000 bytes), ignoring metadata.'
        ans = f'{kb:g} kB'
        key = f'{w} × {h} × {depth} = {bits:,} bits [M1]; ÷ 8 = {bits // 8:,} bytes [M1]; = {kb:g} kB [A1].'
        if slot.d >= 4:
            stem += f' State how many different colours a colour depth of {depth} bit{"s" if depth > 1 else ""} can represent.'
            ans += f'; 2^{depth} = {2 ** depth:,} colours'
            key += f' 2^{depth} = {2 ** depth:,} colours [A1].'
    elif kind == 'sound':
        sr = rng.choice([8000, 22050, 44100, 48000])
        bd = rng.choice([8, 16, 24])
        ch = rng.choice([1, 2])
        sec = rng.choice([10, 30, 60, 180])
        bits = sr * bd * ch * sec
        mb = bits / 8 / 1e6
        stem = (f'A sound clip is recorded at a sample rate of {sr:,} Hz with a bit depth of {bd} bits, in {"mono" if ch == 1 else "stereo"}, for {sec} seconds. '
                f'Calculate the uncompressed file size in megabytes (1 MB = 10⁶ bytes).')
        ans = f'{mb:.3g} MB'
        key = f'{sr:,} × {bd} × {ch} × {sec} = {bits:,} bits [M1]; ÷ 8 = {bits // 8:,} bytes [M1]; ≈ {mb:.3g} MB [A1].'
    else:
        orig = rng.choice([4.8, 6, 12, 25, 40])
        comp = round(orig * rng.choice([0.08, 0.1, 0.2, 0.25, 0.4]), 2)
        saving = (orig - comp) / orig * 100
        fmt_ = rng.choice([('a photo saved as JPEG', 'lossy'), ('a document archive saved as ZIP', 'lossless'),
                           ('a song saved as MP3', 'lossy'), ('a song saved as FLAC', 'lossless')])
        if fmt_[1] == 'lossless' and comp / orig < 0.2:
            comp = round(orig * 0.55, 2)
            saving = (orig - comp) / orig * 100
        ratio = orig / comp
        stem = f'A file of {orig:g} MB is compressed to {comp:g} MB as {fmt_[0]}. Calculate (a) the compression ratio and (b) the percentage reduction in size.'
        ans = f'(a) {ratio:.3g} : 1 (b) {pc(saving)}%'
        key = f'(a) {orig:g} ÷ {comp:g} = {ratio:.3g} : 1 [A1]; (b) ({orig:g} − {comp:g}) ÷ {orig:g} × 100 = {pc(saving)}% [M1 A1].'
        if slot.d >= 3:
            stem += ' (c) State whether this compression is lossy or lossless and explain what that means.'
            ans += f'; (c) {fmt_[1]}'
            key += (' (c) Lossy – some data is permanently removed (e.g. detail the eye/ear barely notices) [A1 R1].' if fmt_[1] == 'lossy'
                    else ' (c) Lossless – the original can be reconstructed exactly; no data is lost [A1 R1].')
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical')


@R.add('ch05-st4', 'C3', (2, 4), 'numerical')
def rle(rng, slot):
    runs = []
    while len(runs) < rng.randint(3, 5):
        c = rng.choice('BW') if not runs else ('W' if runs[-1][0] == 'B' else 'B')
        runs.append((c, rng.randint(2, 9)))
    s = ''.join(c * k for c, k in runs)
    enc = ''.join(f'{k}{c}' for c, k in runs)
    stem = f'A row of pixels in a black-and-white image is stored as: {s}\nUsing run-length encoding (RLE), write the encoded form (e.g. 3W2B) and state how many characters are saved.'
    saved = len(s) - len(enc)
    return dict(stem=stem, answer=f'{enc}; saves {saved} characters ({len(s)} → {len(enc)})', type='numerical', marks=3,
                markingKey=f'Runs: ' + ', '.join(f'{k} × {c}' for c, k in runs) + f' → {enc} [A1 A1]; {len(s)} − {len(enc)} = {saved} characters saved [A1]. RLE is lossless.')


R.facts('ch05-st4', F(
    terms=[('binary', 'a number system with base 2 that uses only the digits 0 and 1, used by computers to represent all data'),
           ('bit', 'a single binary digit, 0 or 1 – the smallest unit of data'),
           ('byte', 'a group of 8 bits, which can represent 256 different values'),
           ('character encoding', 'a system that maps characters to binary codes, such as ASCII or Unicode (UTF-8)'),
           ('lossy compression', 'compression that permanently removes some data to reduce file size, such as JPEG or MP3'),
           ('lossless compression', 'compression that reduces file size without losing any data, so the original can be restored exactly, such as ZIP or PNG'),
           ('colour depth', 'the number of bits used to represent the colour of each pixel in an image'),
           ('sample rate', 'the number of times per second that an analogue sound wave is measured when it is digitised, measured in hertz')],
    facts=[('How many different values can be represented by 8 bits?', '256', ['8', '128', '512'], '2^8 = 256 (0 to 255).'),
           ('Which character encoding can represent characters from almost all of the world\'s writing systems, including emoji?', 'Unicode (e.g. UTF-8)', ['7-bit ASCII', 'Morse code', 'Binary-coded decimal'], 'ASCII has only 128 characters; Unicode covers over 150,000.'),
           ('Which of the following file formats uses lossless compression?', 'PNG', ['JPEG', 'MP3', 'MP4 (H.264 video)'], 'PNG preserves every pixel exactly.'),
           ('How many characters can standard 7-bit ASCII represent?', '128', ['256', '64', '1,024'], '2^7 = 128.')],
    why=[('Explain why computers use binary to represent data.', 'Digital electronics have two stable states (on/off, high/low voltage) that are reliable to store and distinguish, so all data – numbers, text, images and sound – is encoded as patterns of 0s and 1s.'),
         ('Explain why lossy compression is commonly used for streaming video and music.', 'It greatly reduces file size by removing detail people barely notice, so content can be streamed over limited bandwidth and stored cheaply, at the cost of some quality.'),
         ('Explain why Unicode replaced ASCII for most digital communication.', 'ASCII only encodes 128 mainly English characters, while Unicode can represent characters from almost every script (Devanagari, Arabic, Chinese) and emoji, enabling global multilingual communication.')],
    contrast=[('lossy compression', 'lossless compression', 'Lossy compression permanently removes some data to make files much smaller (JPEG, MP3); lossless compression shrinks files without losing data, so the original can be exactly restored (ZIP, PNG, FLAC).'),
              ('a bit', 'a byte', 'A bit is a single binary digit (0 or 1); a byte is a group of 8 bits that can represent 256 values, e.g. one ASCII character.')],
    misc=[('Compressing a file always reduces its quality.', 'Only lossy compression reduces quality; lossless compression (ZIP, PNG, FLAC) restores the original exactly.'),
          ('Increasing the colour depth of an image does not change its file size.', 'More bits per pixel means more data per pixel, so the file size increases proportionally (size = width × height × colour depth).')],
    cases=[('the spread of MP3 and file sharing', 'The MP3 format (developed at the Fraunhofer Institute in the early 1990s) shrank music files by about 90%; Napster (1999) let millions share them, disrupting the recorded-music industry.', 'how data representation shapes social change',
            'lossy compression made music small enough to share over slow internet connections, enabling peer-to-peer sharing and, later, streaming business models.'),
           ('Unicode and Indic scripts', 'Unicode encodes scripts such as Devanagari and Tamil, allowing Indian-language content, domain names and messaging to grow.', 'encoding and cultural inclusion',
            'a common encoding lets speakers of non-Latin scripts communicate and publish online in their own languages, supporting cultural expression.'),
           ('video calls during COVID-19', 'Platforms such as Zoom used video compression codecs to deliver calls over home broadband and mobile networks.', 'lossy compression and access',
            'compression reduced bandwidth needs, letting more people join calls, but low-bandwidth users still received poorer quality, reflecting the digital divide.')],
    sources=[('"Streaming accounted for the large majority of internet traffic in 2023; without modern video codecs, networks simply could not carry it."', 'Network traffic report, 2023',
              'Explain how compression makes the situation described in the source possible.', 'Codecs such as H.264/HEVC use lossy compression to reduce video data by large factors, so networks can carry far more streams with the same bandwidth.'),
             ('"Emoji are now part of Unicode, which means the same smiley sent from Lagos appears – more or less – the same in Lima."', 'Article on digital communication, 2022',
              'Explain why a shared encoding standard matters for communication.', 'A shared standard maps each character/emoji to the same code, so different devices and platforms interpret it consistently; without it, text would appear garbled across systems (though fonts may draw emoji differently).')],
    evaluate=[('The benefits of lossy compression outweigh its drawbacks.',
               ['enables streaming and video calls on limited bandwidth', 'reduces storage costs and energy'],
               ['permanent quality loss, problematic for archives, medical images and evidence', 'repeated compression degrades quality'],
               'For everyday media consumption benefits clearly outweigh drawbacks, but lossless formats remain essential where accuracy matters.'),
              ('Understanding binary is irrelevant for understanding digital society.',
               ['most impacts can be analysed without technical detail', 'users interact with interfaces, not bits'],
               ['representation explains file sizes, compression and bandwidth inequality', 'encoding choices affect languages included online', 'metadata and data formats shape privacy'],
               'Detailed binary arithmetic is not the focus, but understanding representation helps explain real impacts such as access, inclusion and privacy.')],
    extended=[('A charity in a rural area with slow internet wants to share training videos with volunteers. Explain how data representation and compression could help, and evaluate one trade-off.', 'Reduce resolution/frame rate, use lossy codecs (H.264), audio at lower sample rate, offer downloadable versions; trade-off: smaller files vs lower quality/readability of on-screen text; mention calculation of file size and bandwidth.', 6, 'long')],
))

# =============================================================================================
# ch06 Content 3.1 Data: uses, privacy and surveillance
# =============================================================================================
@R.add('ch06-st1', 'C3', (1, 4), 'numerical')
def data_growth(rng, slot):
    frames = [('A streaming platform stored {a} petabytes (PB) of viewing data in {y1}', 'PB'),
              ('A city\'s network of traffic sensors generated {a} terabytes (TB) of data in {y1}', 'TB'),
              ('A hospital group held {a} TB of patient imaging data in {y1}', 'TB'),
              ('A social-media company processed {a} PB of user data per day in {y1}', 'PB')]
    fr, u = rng.choice(frames)
    a = rng.choice([4, 6, 8, 12, 15, 20, 25])
    y1 = rng.choice([2018, 2019, 2020, 2021])
    mode = rng.choice(['pct', 'double'] if slot.d <= 2 else ['pct', 'double', 'cagr'])
    if mode == 'pct':
        b = round(a * rng.choice([1.25, 1.5, 1.8, 2.4, 3.0]), 1)
        y2 = y1 + rng.choice([1, 2, 3])
        p = pct_change(a, b)
        stem = fr.format(a=a, y1=y1) + f' and {b:g} {u} in {y2}. Calculate the percentage increase.'
        return dict(stem=stem, answer=f'{pc(p)}%', markingKey=f'({b:g} − {a}) ÷ {a} × 100 = {pc(p)}% [M1 A1].', type='numerical', marks=2)
    if mode == 'double':
        t = rng.choice([1, 2, 3])
        n = rng.choice([4, 6, 8, 9, 10, 12])
        val = a * 2 ** (n / t)
        stem = fr.format(a=a, y1=y1) + f'. If the volume doubles every {t} year{"s" if t > 1 else ""}, calculate the volume after {n} years.'
        return dict(stem=stem, answer=f'{val:,.4g} {u}', type='numerical', marks=3,
                    markingKey=f'Number of doublings = {n} ÷ {t} = {n / t:g} [M1]; {a} × 2^{n / t:g} = {val:,.4g} {u} [M1 A1].')
    r = rng.choice([20, 30, 40, 50])
    n = rng.choice([3, 4, 5])
    val = a * (1 + r / 100) ** n
    stem = fr.format(a=a, y1=y1) + f'. The volume grows by {r}% per year. Calculate the volume after {n} years, and explain one implication of this growth for the organisation.'
    return dict(stem=stem, answer=f'{val:.4g} {u}; implication e.g. rising storage/energy costs, need for big-data tools, greater security and privacy risk',
                type='numerical', marks=4,
                markingKey=f'{a} × {1 + r / 100:g}^{n} [M1] = {val:.4g} {u} [A1]; implication explained (storage cost, energy, analytics capability, breach impact) [R1 R1].')


R.facts('ch06-st1', F(
    terms=[('big data', 'data sets so large, fast or varied that they cannot be handled by traditional tools, often described by volume, velocity and variety'),
           ('datafication', 'turning aspects of life that were not previously quantified (friendships, movement, sleep) into data that can be analysed (Mayer-Schönberger and Cukier)'),
           ('data analytics', 'examining data to find patterns, relationships and trends that support decisions'),
           ('data mining', 'using algorithms to discover hidden patterns in large data sets'),
           ('veracity', 'the accuracy and trustworthiness of data – one of the "Vs" of big data'),
           ('predictive analytics', 'using historical data and statistical models to forecast future outcomes or behaviour'),
           ('velocity', 'the speed at which data is generated and must be processed – one of the "Vs" of big data')],
    facts=[('Which three "Vs" were originally used to describe big data (Doug Laney, 2001)?', 'Volume, velocity and variety', ['Value, vision and verification', 'Veracity, visibility and validity', 'Volume, value and voice'], 'Veracity and value were added later.'),
           ('Google Flu Trends was discontinued after it significantly overestimated flu levels in which season?', '2012–2013', ['2003–2004', '2019–2020', '2008–2009'], 'It predicted roughly double the CDC-reported level, showing limits of big-data correlation.'),
           ('Which of the following is the best example of datafication?', 'Sleep patterns being tracked and scored by a smartwatch',
            ['Writing a diary by hand', 'Reading a printed newspaper', 'Talking to a friend face to face'], 'Previously unquantified behaviour is turned into data.'),
           ('Which of the following is an example of predictive analytics?', 'A bank estimating the probability that a borrower will default',
            ['Counting how many customers visited a shop yesterday', 'Storing photos in the cloud', 'Encrypting an email'], 'It uses historical data to forecast.')],
    why=[('Explain why big data can find correlations but may not explain causes.', 'Analysing huge data sets reveals patterns (e.g. search terms rising with flu), but correlation does not show why; hidden factors or changes in behaviour (media coverage, algorithm changes) can break the pattern, as with Google Flu Trends.'),
         ('Explain why datafication changes relationships between individuals and organisations.', 'When behaviour is turned into data, organisations can measure, predict and influence individuals (insurers, employers, platforms), increasing their power, while individuals often cannot see or control the data held about them.'),
         ('Explain why the variety of big data creates challenges for analysis.', 'Data comes in many forms – text, images, sensor readings, transactions – often unstructured and from different sources, so it must be cleaned, combined and interpreted, which is complex and can introduce errors.')],
    contrast=[('data analytics', 'data mining', 'Data analytics is the broad process of examining data to answer questions and support decisions; data mining is a specific technique using algorithms to discover previously unknown patterns in large data sets.'),
              ('volume', 'velocity', 'Volume is the quantity of data (e.g. petabytes); velocity is the speed at which data is produced and must be processed (e.g. real-time sensor streams).')],
    misc=[('More data always produces more accurate predictions.', 'Large data sets can still be biased, unrepresentative or noisy; Google Flu Trends had vast data but overestimated flu, showing veracity and model quality matter more than size alone.'),
          ('Big data is only used by technology companies.', 'Governments (census, tax, health), hospitals, retailers, sports teams and scientists use big data – e.g. public health agencies tracking disease or cities managing traffic.')],
    cases=[('Google Flu Trends (2008–2015)', 'Google estimated flu levels from search queries; it worked at first but overestimated the 2012–13 season by about double and was shut down.', 'the limits of big data',
            'it showed that correlations found in massive data can break down when behaviour or algorithms change, so big data needs theory and validation.'),
           ('Netflix\'s use of viewing data', 'Netflix analyses what, when and how subscribers watch to recommend titles and guide commissioning decisions.', 'data analytics for decision-making',
            'detailed behavioural data allows personalisation and investment decisions, increasing engagement but also shaping cultural production around data.'),
           ('Transport for London\'s use of Oyster and contactless data', 'TfL analyses anonymised journey data from cards and Wi-Fi to plan services and manage crowding.', 'big data in public services',
            'aggregated travel data improves planning for millions of passengers, but raises questions about anonymisation and secondary use.')],
    sources=[('"Data is the new oil."', 'Clive Humby, mathematician, 2006 (popularised by The Economist, 2017)',
              'Explain one way in which the comparison in the source is useful and one way it is misleading.', 'Useful: data is a valuable resource that must be refined (analysed) to create value and drives economic power. Misleading: data is non-rival and can be copied endlessly, it is about people (raising rights issues), and it is not used up like oil.'),
             ('"With enough data, the numbers speak for themselves."', 'Chris Anderson, "The End of Theory", Wired, 2008',
              'Explain one weakness in the claim made in the source.', 'Numbers do not interpret themselves: data can be biased or incomplete, and correlations can mislead without causal theory, as Google Flu Trends showed.')],
    evaluate=[('Big data has improved decision-making in public services.',
               ['transport and health planning using real-time data', 'faster detection of outbreaks and fraud'],
               ['bias and errors in data lead to unfair decisions', 'privacy concerns about secondary use', 'over-reliance on correlation (Google Flu Trends)'],
               'Big data can improve decisions when combined with expert judgement, validation and privacy safeguards, but it is not automatically better.'),
              ('Datafication benefits individuals more than organisations.',
               ['personal insights (fitness, sleep, spending)', 'personalised services and recommendations'],
               ['organisations gain detailed profiles to predict and influence behaviour', 'data sold to third parties', 'individuals rarely see the value of their data'],
               'Individuals gain convenience and insight, but organisations capture most of the economic value and power, so benefits are unevenly distributed.')],
    extended=[('Analyse how one organisation uses big data analytics and evaluate the implications for the people whose data is used.', 'E.g. Netflix, Uber, a national health service, a supermarket loyalty scheme; describe data types and analytics; analyse benefits (personalisation, efficiency) and implications (privacy, profiling, consent, power); judge.', 6, 'long')],
))


@R.add('ch06-st2', 'C3', (2, 5), 'numerical')
def gdpr_fine(rng, slot):
    turn = rng.choice([150, 300, 450, 800, 2500, 12000, 40000, 117000])  # € million
    four = turn * 0.04
    cap = max(20.0, four)
    co = rng.choice(['an online retailer', 'a social-media company', 'a ride-hailing platform', 'a cloud provider', 'a fitness-app company', 'a bank'])
    stem = (f'Under the GDPR, the highest tier of fines is up to €20 million or 4% of a company\'s total worldwide annual turnover, whichever is higher. '
            f'{co[0].upper() + co[1:]} has an annual turnover of €{turn:,} million. Calculate the maximum fine it could face.')
    ans = f'€{cap:,.1f} million'.replace('.0 million', ' million')
    key = f'4% of €{turn:,}m = €{four:,.1f}m [M1]; compare with €20m; the higher is {ans} [A1].'
    m = 2
    if slot.d >= 4:
        stem += ' Explain why the GDPR links fines to global turnover rather than setting a fixed amount.'
        ans += '; fixed fines would be trivial for very large firms, so turnover-based fines keep penalties dissuasive and proportionate'
        key += ' Reasoning: proportionate and dissuasive for very large firms; a fixed fine could be treated as a cost of business [R1 R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch06-st2', F(
    terms=[('privacy', 'the right of individuals to control information about themselves and to be free from unwanted intrusion'),
           ('informed consent', 'agreement to data processing given freely, specifically and with a clear understanding of what will happen to the data'),
           ('General Data Protection Regulation (GDPR)', 'the EU law, applied from 25 May 2018, that sets rules for processing personal data and gives individuals rights over their data'),
           ('personal data', 'any information relating to an identified or identifiable living person, such as a name, ID number, location data or online identifier'),
           ('right to erasure', 'the GDPR right (Article 17) to have personal data deleted in certain circumstances, also called the "right to be forgotten"'),
           ('data fiduciary', 'under India\'s Digital Personal Data Protection Act 2023, an organisation that decides the purpose and means of processing personal data'),
           ('data minimisation', 'the principle that only data that is necessary for a specified purpose should be collected and kept')],
    facts=[('From which date did the GDPR apply across the EU?', '25 May 2018', ['1 January 2016', '17 February 2024', '1 August 2024'], 'Adopted in 2016, it applied from 25 May 2018.'),
           ('Within how many hours must an organisation normally report a personal-data breach to the supervisory authority under the GDPR?', '72 hours', ['24 hours', '7 days', '30 days'], 'Article 33 requires notification within 72 hours where feasible.'),
           ('In 2023 the Irish Data Protection Commission fined Meta €1.2 billion for what?', 'Transferring EU users\' personal data to the United States without adequate safeguards',
            ['Failing to remove hate speech', 'Abusing its dominance in advertising', 'Not paying digital services tax'], 'The record GDPR fine concerned EU–US transfers after the Schrems II ruling.'),
           ("Which law did India pass in 2023 to regulate the processing of digital personal data?", 'The Digital Personal Data Protection Act, 2023', ['The Information Technology Act, 2000', 'The Aadhaar Act, 2016', 'The Telecom Regulatory Act, 1997'], 'The DPDP Act creates data fiduciaries, data principals and a Data Protection Board.'),
           ('In which 2017 case did India\'s Supreme Court declare privacy a fundamental right?', 'Justice K.S. Puttaswamy v Union of India', ['Shreya Singhal v Union of India', 'Kesavananda Bharati v State of Kerala', 'Anuradha Bhasin v Union of India'], 'A nine-judge bench recognised privacy under Article 21.')],
    why=[('Explain why consent banners may not provide genuine informed consent.', 'They are often long, vague or use dark patterns (bright "Accept all", hidden "Reject"), and users face consent fatigue across many sites, so clicking accept is rarely free, specific and informed.'),
         ('Explain why the GDPR affects companies outside the EU.', 'It applies to any organisation that offers goods or services to, or monitors, people in the EU, wherever the company is based; large fines encourage global firms to apply GDPR standards worldwide (the "Brussels effect").'),
         ('Explain why data minimisation protects privacy.', 'If organisations collect and keep only the data they need, there is less to be breached, misused or repurposed, reducing harm if security fails.')],
    contrast=[('privacy', 'security', 'Privacy concerns who should have access to personal data and for what purposes; security concerns protecting data from unauthorised access or damage – data can be secure yet used in privacy-invasive ways.'),
              ('the GDPR', "India's DPDP Act 2023", 'Both give individuals rights and impose duties on organisations; the GDPR has several lawful bases and covers personal data broadly with fines up to 4% of turnover, while the DPDP Act relies mainly on consent and "legitimate uses", applies to digital personal data, exempts publicly available data and allows broad government exemptions, with fines up to ₹250 crore.')],
    misc=[('If you have nothing to hide, you have nothing to fear from data collection.', 'Privacy protects autonomy, freedom of expression and protection from discrimination; data can be misused, breached or reinterpreted, and everyone has information (health, beliefs, location) they legitimately keep private.'),
          ('The GDPR only applies to companies based in Europe.', 'It applies to any organisation processing personal data of people in the EU when offering them goods or services or monitoring their behaviour, regardless of where the company is located.')],
    cases=[('the Cambridge Analytica scandal', 'In 2014 an app by researcher Aleksandr Kogan collected data from Facebook users and their friends (up to 87 million people); the data was used by Cambridge Analytica for political profiling. Whistle-blower Christopher Wylie revealed it in March 2018, and the US FTC fined Facebook $5 billion in 2019.', 'the failure of informed consent',
            'most affected people never used the app; their data was taken through friends\' permissions, showing how consent mechanisms failed to protect privacy.'),
           ("Meta's €1.2 billion GDPR fine (2023)", 'The Irish Data Protection Commission fined Meta €1.2 billion and ordered it to stop transferring EU Facebook users\' data to the US, following the Schrems II ruling (2020).', 'enforcement of data-protection law',
            'it showed the GDPR can impose very large penalties on global firms and that data flows across borders depend on legal protections.'),
           ('the Puttaswamy judgment (India, 2017)', 'A nine-judge bench of India\'s Supreme Court unanimously held that privacy is a fundamental right under the Constitution.', 'privacy as a right',
            'the ruling created the constitutional basis for data protection in India and influenced the Aadhaar judgment (2018) and the DPDP Act (2023).')],
    sources=[('"We exploited Facebook to harvest millions of people\'s profiles. And built models to exploit what we knew about them and target their inner demons."', 'Christopher Wylie, former Cambridge Analytica employee, quoted in The Observer, March 2018',
              'With reference to the source, explain why the Cambridge Analytica case is seen as a privacy violation.', 'Data was harvested from millions of profiles without their informed consent and used to build psychological models for political targeting – a purpose users never agreed to.'),
             ('"Personal data shall be adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed."', 'GDPR, Article 5(1)(c)',
              'Identify the principle in the source and explain how it protects individuals.', 'Data minimisation: collecting only what is necessary reduces the risk of misuse, breaches and function creep, giving individuals more control.')],
    evaluate=[('The GDPR has successfully protected the privacy of EU citizens.',
               ['large fines (Meta €1.2bn, Amazon €746m in Luxembourg 2021)', 'new rights (access, erasure, portability)', 'global influence (Brussels effect)'],
               ['enforcement slow and concentrated in Ireland', 'consent fatigue and dark patterns persist', 'big firms can afford compliance; small firms struggle'],
               'The GDPR has raised standards and given individuals rights, but uneven enforcement and consent fatigue limit its effectiveness.'),
              ('Consent is the best basis for protecting personal data.',
               ['respects individual autonomy', 'easy to understand in principle'],
               ['people cannot read hundreds of policies; consent is often not informed', 'power imbalance (accept or lose service)', 'stronger limits on purpose and data minimisation may protect better'],
               'Consent matters, but on its own it is weak; rules on purpose limitation, minimisation and accountability give stronger protection.')],
    extended=[('Compare the GDPR and India\'s DPDP Act 2023 as approaches to protecting personal data, and evaluate which offers stronger protection for individuals.', 'Compare scope, lawful bases, rights, regulators (DPAs vs Data Protection Board), penalties (4% turnover vs up to ₹250 crore), government exemptions (wider under DPDP); evaluate with examples; reach a judgement.', 8, 'long')],
))
AR('ch06-st2', [
    ('The GDPR can fine companies based outside the EU.', 'The GDPR applies to organisations that offer goods or services to, or monitor, people in the EU.', 'a', 'Territorial scope (Article 3) covers non-EU firms targeting EU residents.'),
    ('Data that is securely encrypted cannot raise privacy concerns.', 'Privacy concerns who may access data and for what purposes.', 'd', 'Secure data can still be used for invasive purposes by those who hold it; A is false.'),
])


@R.add('ch06-st3', 'C3', (2, 5), 'numerical')
def frt_matches(rng, slot):
    crowd = rng.choice([10000, 25000, 50000, 80000, 100000])
    fpr = rng.choice([1000, 2000, 5000, 10000])  # 1 in fpr
    wanted = rng.choice([2, 3, 5, 8])
    tpr = rng.choice([70, 80, 90])
    ev = rng.choice(['a football match', 'a music festival', 'a busy shopping street on a Saturday', 'a carnival'])
    fp = crowd / fpr
    tp = wanted * tpr / 100
    stem = (f'Police use live facial recognition at {ev} in {rng.choice(CITIES)} attended by {crowd:,} people. The system wrongly flags about 1 in {fpr:,} innocent people as a match. '
            f'{wanted} people on the watch list attend, and the system correctly flags {tpr}% of them. Calculate the expected number of false alerts')
    if slot.d >= 3:
        stem += ' and the percentage of all alerts that are correct.'
        prec = tp / (tp + fp) * 100
        ans = f'{fp:g} false alerts; {pc(prec)}% of alerts correct'
        key = f'False alerts = {crowd:,} ÷ {fpr:,} = {fp:g} [M1 A1]; true alerts = {wanted} × {tpr}% = {tp:g} [A1]; correct share = {tp:g} ÷ ({tp:g} + {fp:g}) × 100 = {pc(prec)}% [M1 A1].'
        m = 5
        if slot.d >= 5:
            stem += ' Explain what this suggests about using the system on large crowds.'
            ans += '; even a low error rate produces many false alerts in large crowds, so most alerts may be wrong and innocent people are stopped'
            key += ' Base-rate effect explained [R1].'
            m = 6
    else:
        stem += '.'
        ans = f'{fp:g}'
        key = f'{crowd:,} ÷ {fpr:,} = {fp:g} [M1 A1] (people on the watch list are a negligible share of the crowd).'
        m = 2
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch06-st3', F(
    terms=[('surveillance', 'the systematic monitoring of people\'s behaviour, communications or movements, by states, companies or others'),
           ('surveillance capitalism', 'an economic logic in which companies extract behavioural data to predict and influence behaviour for profit (Shoshana Zuboff, 2019)'),
           ('behavioural surplus', 'in Zuboff\'s account, data collected beyond what is needed to provide a service, used to build prediction products'),
           ('mass surveillance', 'the monitoring of whole populations rather than specific suspects'),
           ('panopticon', 'a prison design by Jeremy Bentham in which inmates can always be watched, used by Michel Foucault as a metaphor for self-disciplining under constant possible observation'),
           ('spyware', 'software that secretly monitors a device and transmits data to another party, such as NSO Group\'s Pegasus'),
           ('chilling effect', 'when people avoid lawful activities (searching, speaking, protesting) because they believe they are being watched')],
    facts=[('Who leaked documents in 2013 revealing mass surveillance programmes such as PRISM?', 'Edward Snowden', ['Julian Assange', 'Christopher Wylie', 'Frances Haugen'], 'Snowden, an NSA contractor, gave documents to journalists including Glenn Greenwald.'),
           ('Which spyware, made by Israel\'s NSO Group, was investigated by the 2021 Pegasus Project?', 'Pegasus', ['Stuxnet', 'WannaCry', 'Mirai'], 'Journalists found it on phones of activists and journalists.'),
           ('Who wrote The Age of Surveillance Capitalism (2019)?', 'Shoshana Zuboff', ['Eli Pariser', 'Safiya Umoja Noble', 'Cathy O\'Neil'], 'Zuboff argues Google pioneered the logic of behavioural surplus.'),
           ('Which philosopher used Bentham\'s panopticon as a metaphor for modern disciplinary power?', 'Michel Foucault', ['John Locke', 'Karl Marx', 'Hannah Arendt'], 'Foucault, Discipline and Punish (1975).')],
    why=[('Explain why surveillance can change behaviour even when no one is actually watching.', 'As in the panopticon, people who believe they might be observed adjust their behaviour – avoiding searches, protests or speech – producing a chilling effect and self-discipline without direct intervention.'),
         ('Explain why corporate surveillance is described as surveillance capitalism.', 'Companies collect behavioural data beyond what services need (behavioural surplus), use it to predict and influence what people will do, and sell those predictions to advertisers, making surveillance the basis of profit.'),
         ('Explain why state and corporate surveillance are increasingly connected.', 'Governments can request or buy data held by companies (e.g. PRISM accessed data from US tech firms; agencies buy location data from brokers), so commercial data collection extends state surveillance capacity.')],
    contrast=[('state surveillance', 'corporate surveillance', 'State surveillance monitors people for security, policing or political control, backed by law and coercion; corporate surveillance monitors behaviour mainly for profit through data collection and advertising.'),
              ('targeted surveillance', 'mass surveillance', 'Targeted surveillance focuses on specific suspects, usually with a warrant; mass surveillance collects data on whole populations without individual suspicion.')],
    misc=[('Surveillance only affects people who break the law.', 'Mass surveillance collects data on everyone; it can chill lawful expression, enable discrimination and be misused against journalists, activists and minorities (e.g. Pegasus targeting).'),
          ('China\'s social credit system is a single national score that rates every citizen.', 'It is a fragmented set of mainly corporate and local government rating and blacklist schemes, especially for businesses and court debtors, rather than one unified score for every citizen.')],
    cases=[('the Snowden revelations (2013)', 'Edward Snowden leaked NSA documents showing bulk collection of phone metadata and the PRISM programme accessing data from companies such as Google, Facebook and Apple.', 'state mass surveillance',
            'governments had built population-wide surveillance using commercial platforms, prompting legal changes (USA Freedom Act 2015) and wider use of encryption.'),
           ('the Pegasus Project (2021)', 'A consortium of journalists and Amnesty International\'s Security Lab found that NSO Group\'s Pegasus spyware had targeted phones of journalists, activists and politicians in several countries.', 'surveillance as a threat to human rights',
            'zero-click spyware turned phones into tracking devices, chilling journalism and dissent and showing a market for state surveillance tools.'),
           ('live facial recognition in London', 'The Metropolitan Police has deployed live facial recognition vans scanning faces against watch lists; critics such as Big Brother Watch argue it is intrusive and inaccurate.', 'surveillance in public space',
            'automated identification turns public space into a monitored space, raising questions of consent, accuracy and proportionality.')],
    sources=[('"Surveillance capitalism unilaterally claims human experience as free raw material for translation into behavioral data."', 'Shoshana Zuboff, The Age of Surveillance Capitalism (2019)',
              'Explain what the source means by "free raw material".', 'Companies treat people\'s everyday behaviour (searches, movements, clicks) as a resource they can take without payment or real consent and turn into profitable prediction products.'),
             ('"Arguing that you don\'t care about the right to privacy because you have nothing to hide is no different than saying you don\'t care about free speech because you have nothing to say."', 'Edward Snowden, Reddit AMA, 2015',
              'Explain the argument made in the source.', 'Privacy, like free speech, is a right that protects everyone and society as a whole, not only those with secrets; rights matter even if an individual does not currently need them.')],
    evaluate=[('Mass surveillance is justified if it prevents terrorism.',
               ['security agencies claim it helps detect plots', 'utilitarian argument: protecting many lives'],
               ['evidence that bulk collection stopped attacks is limited (US review panels 2013–14)', 'violates privacy of millions', 'risk of misuse against dissent'],
               'Targeted, warrant-based surveillance can be justified, but mass surveillance is disproportionate given limited evidence of effectiveness and high rights costs.'),
              ('Corporate surveillance is a greater threat to individuals than state surveillance.',
               ['companies collect more detailed data on more people', 'manipulation of behaviour for profit'],
               ['states can arrest, imprison and use force', 'states access corporate data anyway', 'regulation (GDPR) can limit companies more easily than secret agencies'],
               'Corporate surveillance is more pervasive, but state surveillance carries coercive power; the greatest threat lies in their combination.')],
    extended=[('Evaluate the use of live facial recognition by police, considering accuracy, privacy and public safety.', 'Benefits (identifying wanted people, crowd safety); concerns (false positives, demographic differentials in accuracy, mass scanning, chilling effect, lack of consent); legal context (Bridges v South Wales Police 2020 ruled deployment unlawful; EU AI Act limits real-time remote biometric identification); judgement.', 8, 'long')],
))

P2['ch06'] = dict(
    src=[('"Facebook users who had downloaded the app gave it permission to access their friends\' data as well. Of the estimated 87 million people affected, only around 270,000 had installed the app themselves."', 'Summary of evidence to the UK Parliament\'s Digital, Culture, Media and Sport Committee, 2018',
          'Identify two pieces of information in {S} that show a failure of consent.', ['friends\' data was accessed through other users\' permissions', 'only about 270,000 of 87 million people had installed the app'],
          'Explain why {S} suggests the scale of the data harvest was so large.', 'Each app user exposed their friends\' data through Facebook\'s permission settings, so a few hundred thousand installations multiplied into data on tens of millions of people.'),
         ('"By clicking Accept All, you agree to the use of cookies by us and our 847 partners. You can change your preferences at any time."', 'Cookie consent banner on a European news website, 2024',
          'Identify two features of {S} that may make consent less than fully informed.', ['very large number of partners (847)', '"Accept All" presented as the main option / preferences hidden'],
          'Explain how {S} relates to the GDPR requirement for consent.', 'The GDPR requires consent that is freely given, specific, informed and unambiguous; a banner pushing "Accept all" for 847 partners makes genuinely informed choice unrealistic, which regulators have criticised.'),
         ('"Data protection is not about protecting data. It is about protecting people."', 'Speech by a European data-protection commissioner, 2019',
          'Identify two things {S} suggests data protection should focus on.', ['people / individuals rather than data itself', 'the effects of data use on people\'s lives and rights'],
          'Explain the perspective expressed in {S}.', 'It argues privacy law exists to protect people\'s autonomy, dignity and rights from harms caused by data use, not merely to keep files secure.')],
    cmp=[(0, 1, 'consent to the use of personal data', ['both show consent obtained in ways users may not understand', 'both involve many third parties receiving data'],
          ['Source A describes data taken from people who never consented at all; Source B describes a consent request that exists but is hard to understand', 'A is a past scandal; B is current routine practice']),
         (1, 2, 'the purpose of data-protection rules', ['both relate to the rights of individuals over their data'],
          ['Source B shows a practical consent mechanism; Source C states a principle', 'C implies B\'s approach may not truly protect people'])],
    ev=[(0, 2, 'consent is an effective way of protecting people\'s personal data.', ['consent respects autonomy and is required by GDPR in many cases', 'scandals like Cambridge Analytica led to stricter consent rules'],
         ['consent was bypassed through friends\' permissions (Source A)', 'protecting people requires limits beyond consent (Source C)', 'consent fatigue and dark patterns']),
        (1, 2, 'data-protection law has given individuals real control over their data.', ['GDPR rights of access, erasure and portability', 'fines such as Meta\'s €1.2 billion'],
         ['consent banners (Source B) show control is often illusory', 'enforcement is slow; individuals rarely use rights'])],
)

INTV['ch06'] = [
    ('the EU\'s General Data Protection Regulation (GDPR)', 'Since 2018 the GDPR has required organisations handling EU residents\' data to have a lawful basis, report breaches within 72 hours and respect rights such as access and erasure, with fines of up to 4% of global turnover. Critics note that most complaints are handled slowly and that consent banners have multiplied.',
     'Organisations collected and shared personal data with little transparency or user control, and existing laws were fragmented and weakly enforced, exposing people to profiling, breaches and misuse.',
     ['individuals – new rights of access and erasure, though consent fatigue limits real control', 'large technology companies – major compliance costs and fines (Meta €1.2bn) but resources to adapt', 'small businesses – proportionally higher compliance burden', 'regulators – new powers but heavy workloads and cross-border coordination problems'],
     ['enforceable rights and large penalties', 'global influence (Brussels effect) raising standards elsewhere', 'breach notification improves transparency'],
     ['slow, uneven enforcement concentrated in Ireland', 'consent banners and dark patterns undermine informed choice', 'compliance costs favour large incumbents'],
     'Strengthen enforcement capacity and coordination between national regulators for cross-border cases, ban manipulative consent designs and promote privacy-by-default settings.'),
    ('India\'s Digital Personal Data Protection Act 2023', 'The DPDP Act requires data fiduciaries to obtain consent for processing digital personal data, sets up a Data Protection Board and allows penalties of up to ₹250 crore. It also lets the central government exempt state agencies from its provisions.',
     'India\'s rapidly growing digital economy (UPI, Aadhaar-linked services, apps) generated vast amounts of personal data without a comprehensive data-protection law after the Puttaswamy (2017) ruling recognised privacy as a fundamental right.',
     ['citizens – new rights to information, correction and erasure', 'businesses and start-ups – compliance duties and penalties', 'government agencies – broad possible exemptions', 'civil-society groups – concerns about surveillance and independence of the Board'],
     ['first comprehensive data-protection law for over a billion people', 'clear duties on data fiduciaries and breach reporting', 'consent managers may simplify control'],
     ['wide government exemptions', 'Data Protection Board appointed by government, raising independence concerns', 'publicly available data excluded'],
     'Narrow and make transparent the government exemptions, with independent oversight of the Data Protection Board and public reporting of enforcement.'),
]

# =============================================================================================
# ch07 Content 3.2 Algorithms: nature and design, evaluation
# =============================================================================================
@R.add('ch07-st1', 'C3', (1, 5), 'numerical')
def trace_loop(rng, slot):
    n = 4 if slot.d <= 2 else 5 if slot.d <= 3 else 6
    vals = [rng.randint(1, 40) for _ in range(n)]
    ctx = rng.choice([('daily screen-time minutes', 'MINUTES'), ('likes on each post', 'LIKES'), ('steps (in hundreds) each day', 'STEPS'),
                      ('delivery times in minutes', 'TIMES'), ('ratings given to a video', 'RATINGS')])
    arr = ctx[1]
    kind = rng.choice(['sum', 'max', 'count'] if slot.d <= 3 else ['count', 'maxidx', 'avg'])
    t = rng.randint(10, 30)
    if kind == 'sum':
        code = f'TOTAL = 0\nloop I from 0 to {n - 1}\n    TOTAL = TOTAL + {arr}[I]\nend loop\noutput TOTAL'
        out = sum(vals)
        work = ' → '.join(str(sum(vals[:i + 1])) for i in range(n))
    elif kind == 'max':
        code = f'BEST = {arr}[0]\nloop I from 1 to {n - 1}\n    if {arr}[I] > BEST then\n        BEST = {arr}[I]\n    end if\nend loop\noutput BEST'
        out = max(vals)
        work = 'BEST takes values ' + ' → '.join(str(max(vals[:i + 1])) for i in range(n))
    elif kind == 'count':
        code = f'COUNT = 0\nloop I from 0 to {n - 1}\n    if {arr}[I] > {t} then\n        COUNT = COUNT + 1\n    end if\nend loop\noutput COUNT'
        out = sum(1 for v in vals if v > t)
        work = 'values above ' + str(t) + ': ' + (', '.join(str(v) for v in vals if v > t) or 'none')
    elif kind == 'maxidx':
        code = f'POS = 0\nloop I from 1 to {n - 1}\n    if {arr}[I] >= {arr}[POS] then\n        POS = I\n    end if\nend loop\noutput POS'
        pos = 0
        for i in range(1, n):
            if vals[i] >= vals[pos]:
                pos = i
        out = pos
        work = f'largest value {max(vals)}; last position holding it (>= comparison) is index {pos}'
    else:
        code = f'TOTAL = 0\nloop I from 0 to {n - 1}\n    TOTAL = TOTAL + {arr}[I]\nend loop\nAVERAGE = TOTAL / {n}\noutput AVERAGE'
        out = round(sum(vals) / n, 2)
        work = f'TOTAL = {sum(vals)}; {sum(vals)} / {n}'
    stem = (f'An array {arr} holds {ctx[0]}: [{", ".join(map(str, vals))}] (indexes start at 0).\n\n{code}\n\n'
            f'Trace the algorithm and state the output.')
    m = 2 if slot.d <= 2 else 3
    if slot.d >= 4:
        stem += ' Then state the purpose of the algorithm.'
        purpose = {'count': f'counts how many values are greater than {t}', 'maxidx': 'finds the index of the (last) largest value',
                   'avg': 'calculates the mean of the values', 'sum': 'calculates the total', 'max': 'finds the largest value'}[kind]
        return dict(stem=stem, answer=f'{out:g}; it {purpose}', markingKey=f'{work} [M1]; output {out:g} [A1]; purpose: {purpose} [A1].', type='numerical', marks=4)
    return dict(stem=stem, answer=f'{out:g}', markingKey=f'{work} [M1]; output {out:g} [A1].', type='numerical', marks=m)


R.facts('ch07-st1', F(
    terms=[('algorithm', 'a finite, ordered set of unambiguous instructions for solving a problem or completing a task'),
           ('input', 'data that is given to an algorithm or system to be processed'),
           ('output', 'the result produced by an algorithm after processing its inputs'),
           ('flowchart', 'a diagram that represents an algorithm using standard symbols (terminators, processes, decisions, inputs/outputs) connected by arrows'),
           ('pseudocode', 'a structured, language-independent way of writing an algorithm using programming-like statements'),
           ('selection', 'a control structure in which a decision (e.g. IF…THEN…ELSE) determines which instructions are carried out'),
           ('iteration', 'a control structure that repeats a set of instructions, for example a loop'),
           ('decomposition', 'breaking a complex problem into smaller, more manageable sub-problems')],
    facts=[('Which flowchart symbol is used to represent a decision?', 'A diamond', ['A rectangle', 'A parallelogram', 'An oval'], 'Diamonds hold yes/no questions; rectangles are processes; parallelograms are input/output; ovals are start/end.'),
           ('Which of the following is a property every algorithm must have?', 'It must finish after a finite number of steps', ['It must be written in Python', 'It must use artificial intelligence', 'It must run on a computer'], 'Algorithms are finite and unambiguous and can be followed by people too.'),
           ('Which control structure is used when an instruction needs to be repeated until a condition is met?', 'Iteration', ['Sequence', 'Selection', 'Decomposition'], 'Loops are iteration.'),
           ('The word "algorithm" derives from the name of which 9th-century mathematician?', 'Muhammad ibn Musa al-Khwarizmi', ['Euclid', 'Ada Lovelace', 'Alan Turing'], 'Al-Khwarizmi worked in Baghdad\'s House of Wisdom.')],
    why=[('Explain why algorithms must be unambiguous.', 'Computers follow instructions exactly and cannot interpret vague steps, so each step must have one clear meaning; ambiguity leads to errors or different results each time.'),
         ('Explain why decomposition is useful when designing an algorithm for a real-world system.', 'Breaking a large problem (e.g. a food-delivery app) into smaller parts (matching, routing, pricing, payments) makes each part easier to design, test and improve, and lets teams work in parallel.'),
         ('Explain why algorithms are central to digital society.', 'Algorithms automate decisions that affect people – what news they see, who gets a loan, which driver gets a job – at huge scale, so their design shapes opportunities and power in society.')],
    contrast=[('selection', 'iteration', 'Selection chooses which path to follow based on a condition (IF…THEN); iteration repeats a block of instructions (loops) while or until a condition holds.'),
              ('an algorithm', 'a program', 'An algorithm is the step-by-step logic for solving a problem, independent of language; a program is the implementation of an algorithm in a specific programming language that a computer can run.')],
    misc=[('Algorithms are only found in computers.', 'An algorithm is any precise set of steps – recipes, long division and route directions are algorithms; computers execute algorithms at speed and scale.'),
          ('An algorithm that produces the right answer once is correct.', 'An algorithm must work for all valid inputs, including edge cases (empty lists, ties, extreme values); one correct run does not prove correctness.')],
    cases=[('the Uber matching algorithm', 'Uber\'s system takes inputs such as rider location, driver locations, traffic and demand, and outputs a driver assignment, an estimated arrival time and a price (including surge pricing).', 'inputs, processes and outputs',
            'the algorithm transforms location and demand data into decisions that affect drivers\' income and riders\' costs, showing how algorithmic outputs shape people\'s lives.'),
           ('the UK A-level grading algorithm (2020)', 'With exams cancelled, Ofqual used an algorithm based on schools\' past results and teacher rankings; about 39% of teacher-assessed grades were lowered, and after protests the government reverted to teacher grades.', 'how algorithm design determines outcomes',
            'using historical school performance as an input meant individual students at historically lower-performing schools were downgraded, showing that design choices embed values.'),
           ('traffic-light control algorithms', 'Adaptive traffic systems such as SCOOT use sensor inputs to adjust signal timings in real time.', 'algorithms using selection and iteration',
            'the system repeatedly measures traffic (iteration) and changes timings when queues exceed thresholds (selection), reducing delays.')],
    sources=[('"The algorithm did not see me. It saw my school\'s history."', 'Student from a state school in northern England, interviewed by a newspaper after A-level results, August 2020',
              'With reference to the source, explain how the inputs of an algorithm can lead to unfair outputs.', 'The algorithm used the school\'s past results as an input, so an individual\'s grade depended on others\' historical performance rather than their own work; inappropriate inputs produced unfair individual outcomes.'),
             ('"An algorithm is an opinion embedded in code."', 'Cathy O\'Neil, mathematician, TED talk (2017)',
              'Explain what the source means.', 'Designers choose goals, inputs, weightings and definitions of success, so algorithms reflect human judgements and values rather than being neutral or objective.')],
    evaluate=[('Algorithms make fairer decisions than humans.',
               ['consistent rules applied to everyone', 'not affected by mood, fatigue or personal prejudice'],
               ['learn and reproduce historical bias (Ofqual 2020, COMPAS)', 'opaque and hard to challenge', 'consistency can spread one error to thousands of people'],
               'Algorithms can be more consistent, but fairness depends on design, data and oversight; they are not inherently fairer than humans.'),
              ('Everyone in a digital society needs to understand how algorithms work.',
               ['algorithms shape news, jobs and finance', 'understanding helps people challenge unfair decisions'],
               ['many algorithms are proprietary and secret', 'responsibility should lie with designers and regulators, not individuals', 'basic literacy matters more than technical detail'],
               'A basic algorithmic literacy is important for citizens, but accountability must not be shifted to individuals who cannot see inside proprietary systems.')],
    extended=[('Design an algorithm (in pseudocode or a flowchart) that a library could use to decide whether a member can borrow a book, then evaluate one way the algorithm could treat some members unfairly.', 'Inputs: membership status, number of books on loan, overdue fines; selection: IF member AND loans < limit AND fines = 0 THEN allow ELSE refuse; output decision. Unfairness: e.g. a fixed fine rule excludes low-income members; no human override. Reward correct structure and evaluation.', 6, 'long')],
))


@R.add('ch07-st2', 'C3', (1, 5), 'numerical')
def search_sort(rng, slot):
    kind = rng.choice(['linear', 'binary', 'bubble'] if slot.d >= 2 else ['linear', 'binary'])
    if kind == 'linear':
        n = rng.randint(6, 9)
        vals = rng.sample(range(5, 99), n)
        target = rng.choice(vals)
        pos = vals.index(target)
        stem = f'A linear search looks for {target} in the list [{", ".join(map(str, vals))}]. State how many comparisons are made before the item is found.'
        return dict(stem=stem, answer=str(pos + 1), markingKey=f'The search checks items in order from the start: {target} is item {pos + 1}, so {pos + 1} comparisons [A1].', type='numerical', marks=1)
    if kind == 'binary':
        n = rng.choice([7, 9, 11, 15])
        vals = sorted(rng.sample(range(2, 99), n))
        target = rng.choice(vals)
        lo, hi, steps, seq = 0, n - 1, 0, []
        while lo <= hi:
            mid = (lo + hi) // 2
            steps += 1
            seq.append(vals[mid])
            if vals[mid] == target:
                break
            if vals[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        stem = (f'A binary search (midpoint = (low + high) DIV 2, indexes from 0) looks for {target} in the sorted list [{", ".join(map(str, vals))}]. '
                f'List the values checked and state the number of comparisons.')
        m = 3
        if slot.d >= 4:
            stem += f' State the maximum number of comparisons a linear search would need for a list of this length, and explain why binary search is more efficient for large lists.'
            m = 5
            return dict(stem=stem, answer=f'{", ".join(map(str, seq))}; {steps} comparisons; linear worst case {n}', type='numerical', marks=m,
                        markingKey=f'Values checked: {", ".join(map(str, seq))} [M1 A1]; {steps} comparisons [A1]; linear worst case {n} [A1]; binary search halves the list each time (about log₂ n steps) so it grows very slowly with n, but it needs sorted data [R1].')
        return dict(stem=stem, answer=f'{", ".join(map(str, seq))}; {steps} comparisons', type='numerical', marks=m,
                    markingKey=f'Midpoints checked: {", ".join(map(str, seq))} [M1 A1]; {steps} comparisons [A1].')
    n = rng.choice([5, 6])
    vals = rng.sample(range(1, 60), n)
    a = vals[:]
    swaps = 0
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
            swaps += 1
    stem = f'Show the list [{", ".join(map(str, vals))}] after the first pass of a bubble sort into ascending order, and state the number of swaps made.'
    if swaps == 0:
        return None
    return dict(stem=stem, answer=f'[{", ".join(map(str, a))}]; {swaps} swaps', type='numerical', marks=3,
                markingKey=f'Compare adjacent pairs left to right, swapping when the left is larger [M1]; after pass 1: [{", ".join(map(str, a))}] [A1]; {swaps} swaps [A1]. The largest value {max(vals)} is now at the end.')


@R.add('ch07-st2', 'C3', (2, 5), 'numerical')
def rec_score(rng, slot):
    plat, feats = rng.choice([('a video platform', ('relevance to past viewing', 'popularity', 'recency')),
                              ('a music-streaming app', ('match to listening history', 'number of plays', 'newness')),
                              ('a news app', ('topic match', 'engagement', 'freshness')),
                              ('an online shop', ('similarity to past purchases', 'sales popularity', 'discount'))])
    w = rng.choice([(0.5, 0.3, 0.2), (0.6, 0.3, 0.1), (0.4, 0.4, 0.2), (0.5, 0.2, 0.3)])
    items = []
    for lab in 'XYZ':
        items.append((lab, [rng.randint(2, 10) for _ in range(3)]))
    scores = [(lab, round(sum(wi * fi for wi, fi in zip(w, f)), 2)) for lab, f in items]
    if len({s for _, s in scores}) < 3:
        return None
    best = max(scores, key=lambda x: x[1])
    tbl = '\n'.join(f'Item {lab}: {feats[0]} {f[0]}, {feats[1]} {f[1]}, {feats[2]} {f[2]}' for lab, f in items)
    stem = (f'{plat[0].upper() + plat[1:]} ranks items with the score = {w[0]} × {feats[0]} + {w[1]} × {feats[1]} + {w[2]} × {feats[2]} (each rated 0–10).\n{tbl}\n'
            f'Calculate the score for each item and state which is recommended first.')
    m = 3
    ans = '; '.join(f'{lab} = {s:g}' for lab, s in scores) + f'; {best[0]} first'
    key = '; '.join(f'{lab}: {w[0]}×{f[0]} + {w[1]}×{f[1]} + {w[2]}×{f[2]} = {s:g}' for (lab, f), (_, s) in zip(items, scores)) + f' [M1 A1]; {best[0]} ranked first [A1].'
    if slot.d >= 4:
        stem += f' Explain one consequence of giving "{feats[1]}" a large weighting.'
        ans += f'; popular items get more exposure and become more popular (feedback loop), reducing diversity and visibility of new or niche creators'
        key += ' Consequence: rich-get-richer feedback loop / reduced diversity / disadvantage to new creators [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch07-st2', F(
    terms=[('linear search', 'a search that checks each item in a list in turn until the target is found or the list ends'),
           ('binary search', 'a search on a sorted list that repeatedly checks the middle item and discards half of the remaining list'),
           ('bubble sort', 'a sorting algorithm that repeatedly compares adjacent items and swaps them if they are in the wrong order'),
           ('recommendation algorithm', 'an algorithm that predicts and suggests content or products a user is likely to engage with, based on their data and that of similar users'),
           ('collaborative filtering', 'a recommendation method that suggests items liked by users with similar behaviour ("people who watched this also watched…")'),
           ('ranking algorithm', 'an algorithm that orders results (search results, posts, products) according to calculated relevance or other criteria'),
           ('PageRank', 'Google\'s original ranking algorithm (Page and Brin, 1998) that rates a web page\'s importance by the number and quality of links pointing to it')],
    facts=[('What must be true of a list before a binary search can be used?', 'It must be sorted', ['It must contain fewer than 100 items', 'It must contain only numbers', 'It must have no duplicates'], 'Binary search relies on order to discard half the list.'),
           ('What is the maximum number of comparisons a binary search needs to find an item in a sorted list of 1,000 items?', '10', ['500', '1,000', '100'], '2^10 = 1,024 ≥ 1,000.'),
           ('Which ranking algorithm, developed by Larry Page and Sergey Brin, measured page importance using links?', 'PageRank', ['EdgeRank', 'BubbleRank', 'LinkSort'], 'Described in their 1998 paper at Stanford.'),
           ('"Customers who bought this item also bought…" is an example of which recommendation method?', 'Collaborative filtering', ['Binary search', 'Content moderation', 'Encryption'], 'It uses similarities between users\' behaviour.')],
    why=[('Explain why binary search is faster than linear search on large sorted lists.', 'Each comparison halves the remaining items, so the number of steps grows with log₂ n (about 20 for a million items) instead of n (up to a million for linear search).'),
         ('Explain why recommendation algorithms can create "rich-get-richer" effects.', 'Items that are already popular get recommended more, gain more views and are recommended even more (positive feedback), while new or niche creators struggle for visibility.'),
         ('Explain why the design of a ranking algorithm is a source of power.', 'Most users click the first few results, so whoever designs the ranking decides which businesses, news and views get attention, shaping markets and public opinion.')],
    contrast=[('linear search', 'binary search', 'Linear search checks items one by one and works on unsorted lists but is slow for large lists; binary search repeatedly halves a sorted list and is much faster but requires the data to be sorted first.'),
              ('collaborative filtering', 'content-based filtering', 'Collaborative filtering recommends items liked by similar users; content-based filtering recommends items with features similar to those the user already liked (e.g. same genre or keywords).')],
    misc=[('Search results are ranked purely by how relevant they are to the user.', 'Rankings also reflect commercial interests (ads, self-preferencing – Google was fined €2.42bn in 2017 for favouring Google Shopping), engagement signals and optimisation by website owners (SEO).'),
          ('Bubble sort is the most efficient sorting algorithm for large data sets.', 'Bubble sort is simple but slow (about n² comparisons); algorithms like merge sort or quicksort (about n log n) are much faster on large data.')],
    cases=[("TikTok's For You feed", 'TikTok\'s recommendation system ranks videos for each user using signals such as watch time, likes, shares and accounts followed, and can quickly learn a new user\'s interests.', 'recommendation algorithms',
            'small signals (rewatching, pausing) feed a model that personalises the feed, keeping users engaged but potentially narrowing what they see.'),
           ('Google PageRank', 'Larry Page and Sergey Brin developed PageRank at Stanford in the late 1990s, ranking pages by links; it helped Google become the dominant search engine.', 'ranking algorithms',
            'treating links as "votes" improved search quality and created an incentive to manipulate links, showing how ranking rules shape behaviour.'),
           ('YouTube recommendations', 'YouTube has said that recommendations drive a large share of viewing time; in 2019 it changed its system to reduce recommendations of "borderline content".', 'the power of recommendation design',
            'the platform\'s choice of what to recommend shapes what billions watch, so design changes can reduce or increase exposure to harmful content.')],
    sources=[('"More than 70% of the time people spend watching YouTube is driven by our recommendation algorithms."', 'Neal Mohan, YouTube Chief Product Officer, interview with CNET, 2018',
              'Explain what the source suggests about the power of recommendation algorithms.', 'Most viewing is chosen by the algorithm rather than direct search, so the platform\'s design largely decides what users watch and which creators succeed.'),
             ('"The best place to hide a dead body is page two of Google search results."', 'Popular joke among search-engine marketers',
              'Explain what the source suggests about ranking algorithms.', 'Users rarely look beyond the first page of results, so ranking position determines visibility; a low ranking effectively hides content, giving the ranking algorithm great power.')],
    evaluate=[('Recommendation algorithms benefit users more than they benefit platforms.',
               ['help users find relevant content among millions of items', 'save time and support discovery of niche creators'],
               ['designed to maximise engagement and advertising revenue', 'can narrow exposure and promote extreme content', 'users have little control or transparency'],
               'Users gain convenience, but algorithms are optimised for platform goals; benefits to users are real but secondary unless users get control (e.g. DSA non-profiling feed option).'),
              ('Search engines are neutral gateways to information.',
               ['they index vast amounts of information for free', 'ranking based on relevance signals'],
               ['self-preferencing (Google Shopping fine)', 'advertising and SEO shape results', 'biased results (Noble, Algorithms of Oppression, 2018)'],
               'Search engines are powerful curators rather than neutral gateways; their ranking choices reflect commercial and design decisions.')],
    extended=[('Explain how a recommendation algorithm on one platform works and evaluate its impact on content creators.', 'E.g. TikTok/YouTube/Spotify: inputs (watch time, likes, similar users), ranking, feedback loops; impacts on creators: discovery and income vs dependence, unpredictable changes, pressure to optimise; judgement.', 6, 'long')],
))
AR('ch07-st2', [
    ('Binary search cannot be used on an unsorted list.', 'Binary search discards half of the list after each comparison based on order.', 'a', 'Discarding halves only works if the list is ordered.'),
    ('Bubble sort is efficient for very large lists.', 'Bubble sort compares adjacent items and swaps them if they are out of order.', 'd', 'Bubble sort is O(n²), slow for large lists; R correctly describes it.'),
])


@R.add('ch07-st3', 'C3', (2, 5), 'numerical')
def complexity(rng, slot):
    kind = rng.choice(['growth', 'accuracy'])
    if kind == 'growth':
        n = rng.choice([1000, 10000, 100000, 1000000])
        f = rng.choice([2, 10])
        lin = n
        log2 = math.ceil(math.log2(n))
        quad = n * n
        stem = (f'An algorithm processes a list of {n:,} items. Estimate the number of steps for an algorithm that takes (a) n steps, (b) about log₂ n steps and (c) n² steps.')
        ans = f'(a) {lin:,} (b) about {log2} (c) {sci(quad)}'
        key = f'(a) n = {lin:,} [A1]; (b) log₂ {n:,} ≈ {log2} [A1]; (c) n² = {sci(quad)} [A1].'
        m = 3
        if slot.d >= 4:
            stem += f' If the list grows {f} times larger, state by what factor the n² algorithm\'s steps increase.'
            ans += f'; {f * f} times'
            key += f' ({f}n)² = {f * f}n², so {f * f} times [A1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    tp = rng.randint(40, 90)
    fn = rng.randint(5, 30)
    fp = rng.randint(5, 40)
    tn = rng.randint(200, 800)
    use = rng.choice(['flag fraudulent benefit claims', 'screen job applications', 'detect spam emails', 'flag possibly fraudulent card transactions'])
    tot = tp + fn + fp + tn
    acc = (tp + tn) / tot * 100
    prec = tp / (tp + fp) * 100
    stem = (f'An automated system is used to {use}. In a test of {tot} cases it correctly flagged {tp}, missed {fn}, wrongly flagged {fp} and correctly cleared {tn}. '
            f'Calculate (a) its accuracy and (b) the percentage of flagged cases that were genuinely positive.')
    ans = f'(a) {pc(acc)}% (b) {pc(prec)}%'
    key = f'(a) ({tp} + {tn}) ÷ {tot} × 100 = {pc(acc)}% [M1 A1]; (b) {tp} ÷ ({tp} + {fp}) × 100 = {pc(prec)}% [M1 A1].'
    m = 4
    if slot.d >= 4:
        stem += ' Explain why a high accuracy figure may still hide a problem for the people affected.'
        ans += f'; most cases are negatives, so accuracy is inflated; {fp} people were wrongly flagged and may face penalties without human review'
        key += ' Imbalanced data inflates accuracy; false positives harm individuals (e.g. Dutch childcare-benefits scandal) [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch07-st3', F(
    terms=[('efficiency', 'how much time (number of steps) and memory an algorithm needs as the size of its input grows'),
           ('accuracy', 'the proportion of an algorithm\'s outputs or predictions that are correct'),
           ('automated decision-making', 'decisions made by algorithms with little or no human involvement, such as automatic loan approvals'),
           ('false positive', 'an output that wrongly flags something as present or positive, such as an innocent person flagged as a fraud risk'),
           ('false negative', 'an output that wrongly fails to flag something that is present, such as a fraudulent transaction that is missed'),
           ('human in the loop', 'a design in which a human reviews or approves an algorithm\'s output before a decision takes effect'),
           ('Big O notation', 'a way of describing how an algorithm\'s running time grows with input size, e.g. O(n) or O(n²)')],
    facts=[('Which article of the GDPR gives people the right not to be subject to decisions based solely on automated processing that significantly affect them?', 'Article 22', ['Article 5', 'Article 17', 'Article 33'], 'Article 22 also requires safeguards such as human intervention.'),
           ('Which time complexity describes binary search?', 'O(log n)', ['O(n)', 'O(n²)', 'O(1) always'], 'It halves the search space each step.'),
           ('In Australia, which automated debt-recovery scheme was later found by a Royal Commission (2023) to be "crude and cruel" and unlawful?', 'Robodebt', ['My Health Record', 'COVIDSafe', 'Centrelink Express'], 'It averaged annual tax income to calculate alleged welfare overpayments.'),
           ('Which of the following is an example of a false negative?', 'A spam filter lets a phishing email into the inbox', ['A spam filter blocks a genuine email from a friend', 'A spam filter blocks a spam email', 'A spam filter lets a genuine email through'], 'A real positive was missed.')],
    why=[('Explain why efficiency matters for algorithms used by large platforms.', 'Platforms process billions of items and users; an inefficient algorithm (e.g. O(n²)) would be too slow or costly in energy and hardware at that scale, so efficient algorithms make real-time services possible.'),
         ('Explain why accuracy alone is not enough to evaluate an automated decision system.', 'An accurate system can still produce many harmful errors if cases are imbalanced, and errors may fall unevenly on certain groups; the type of error (false positive vs negative) and who bears it matter as much as the overall rate.'),
         ('Explain why keeping a human in the loop may reduce harm from automated decisions.', 'A human can spot unusual cases, contextual factors and obvious errors, explain decisions and take responsibility, which helps prevent a single algorithmic error affecting many people unchallenged – though humans may also over-trust the system (automation bias).')],
    contrast=[('a false positive', 'a false negative', 'A false positive wrongly flags something as positive (an innocent person flagged as a fraud risk); a false negative wrongly misses a real positive (a fraud that goes undetected).'),
              ('efficiency', 'accuracy', 'Efficiency is about the resources (time, memory) an algorithm uses; accuracy is about how often its outputs are correct – a fast algorithm can be inaccurate and vice versa.')],
    misc=[('Automating a decision always makes it more efficient and therefore better.', 'Automation can be faster, but if the algorithm is inaccurate or biased it spreads errors at scale (Robodebt raised hundreds of thousands of unlawful debts); efficiency is not the same as quality or fairness.'),
          ('A system with 95% accuracy will make very few mistakes.', 'On a large population 5% errors can affect thousands of people, and if positives are rare most flagged cases can still be wrong.')],
    cases=[('Robodebt (Australia, 2016–2019)', 'Services Australia\'s automated system compared averaged tax-office income with welfare records and issued debt notices; many debts were wrong, and a Royal Commission (2023) called the scheme "crude and cruel".', 'risks of automated decision-making',
            'removing human checks and reversing the burden of proof meant a flawed calculation was applied to hundreds of thousands of people, causing financial and psychological harm.'),
           ('the Dutch childcare-benefits scandal (toeslagenaffaire)', 'The Dutch tax authority used risk-scoring that, among other factors, treated dual nationality as a risk indicator; thousands of families were wrongly accused of fraud and the government resigned in January 2021.', 'false positives in automated decisions',
            'false positives fell disproportionately on families with migrant backgrounds and were enforced harshly, showing the human cost of errors.'),
           ('spam filters in email services', 'Gmail and other services use machine-learning filters to classify billions of emails as spam or not each day.', 'accuracy and error trade-offs',
            'tuning the filter to catch more spam (fewer false negatives) increases the chance that genuine emails are hidden (false positives), so designers must choose which error matters more.')],
    sources=[('"The scheme was a crude and cruel mechanism, neither fair nor legal, and it made many people feel like criminals."', 'Royal Commission into the Robodebt Scheme, Final Report, Australia, 2023',
              'With reference to the source, explain two impacts of the automated decision system.', 'It produced unfair and unlawful debts (legal and financial impact), and it caused psychological harm by making people feel like criminals (social/emotional impact).'),
             ('"Computer says no."', 'Catchphrase from the British comedy series Little Britain (2003–2006), widely used to describe inflexible automated systems',
              'Explain what the source suggests about automated decision-making.', 'It mocks systems where staff simply defer to a computer\'s output without explanation or discretion, highlighting the lack of transparency and human judgement in automated decisions.')],
    evaluate=[('Governments should use automated systems to make welfare decisions.',
               ['faster processing of large numbers of claims', 'consistent rules and lower administrative cost'],
               ['errors at scale (Robodebt, Dutch childcare scandal)', 'vulnerable people least able to challenge decisions', 'opacity and reversed burden of proof'],
               'Automation can support welfare administration, but final decisions with serious consequences need human review, transparency and easy appeal.'),
              ('The most important quality of an algorithm is its efficiency.',
               ['efficiency enables services at the scale of billions', 'reduces energy and cost'],
               ['accuracy and fairness matter more when decisions affect people', 'efficient but biased systems spread harm quickly'],
               'Efficiency is necessary for scale, but in decisions about people, accuracy, fairness and accountability are more important.')],
    extended=[('A city plans to use an algorithm to automatically flag "high-risk" tenants for housing inspections. Evaluate this plan, referring to efficiency, accuracy and the people affected.', 'Benefits: faster targeting of inspections; risks: false positives on certain neighbourhoods/groups, feedback loops, lack of explanation; safeguards: human review, audits, appeal; reach a judgement.', 8, 'long')],
))

# =============================================================================================
# ch08 Content 3.2 Algorithms: bias, transparency and accountability
# =============================================================================================
@R.add('ch08-st1', 'C3', (2, 5), 'numerical')
def group_fpr(rng, slot):
    ga, gb = rng.choice([('people in group A', 'people in group B'), ('applicants from district North', 'applicants from district South'),
                         ('women', 'men'), ('younger defendants', 'older defendants')])
    na = rng.choice([200, 300, 400, 500])
    nb = rng.choice([200, 300, 400, 500])
    fa = rng.randint(int(na * 0.25), int(na * 0.45))
    fb = rng.randint(int(nb * 0.08), int(nb * 0.22))
    sys_, neg = rng.choice([('a risk-assessment tool predicting reoffending', 'did not go on to reoffend'), ('a fraud-detection model for welfare claims', 'had made genuine claims'),
                            ('a CV-screening model that rejects "unsuitable" applicants', 'were later judged suitable for the job'), ('a credit-scoring model that flags "high-risk" borrowers', 'repaid their loans in full')])
    ra, rb = fa / na * 100, fb / nb * 100
    stem = (f'An audit of {sys_} looked only at people who {neg}. '
            f'Of {na} such {ga}, {fa} were wrongly flagged; of {nb} such {gb}, {fb} were wrongly flagged. Calculate the false positive rate for each group')
    if slot.d >= 3:
        stem += ' and how many times higher one rate is than the other.'
        ans = f'{ga}: {pc(ra)}%; {gb}: {pc(rb)}%; {ra / rb:.2g} times higher for {ga}'
        key = f'{fa} ÷ {na} × 100 = {pc(ra)}% [A1]; {fb} ÷ {nb} × 100 = {pc(rb)}% [A1]; {pc(ra)} ÷ {pc(rb)} ≈ {ra / rb:.2g} [M1 A1].'
        m = 4
        if slot.d >= 5:
            stem += ' Explain why this pattern is evidence of algorithmic bias even if the tool\'s overall accuracy is similar for both groups.'
            ans += '; innocent members of one group bear far more wrongful flags – unequal error rates harm that group, as ProPublica found for COMPAS (2016)'
            key += ' Unequal false positive rates mean the costs of errors fall disproportionately on one group (error-rate imbalance), even with equal overall accuracy [R1 R1].'
            m = 6
    else:
        stem += '.'
        ans = f'{ga}: {pc(ra)}%; {gb}: {pc(rb)}%'
        key = f'{fa} ÷ {na} × 100 = {pc(ra)}% [A1]; {fb} ÷ {nb} × 100 = {pc(rb)}% [A1].'
        m = 2
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch08-st1', F(
    terms=[('algorithmic bias', 'systematic and repeatable errors in an algorithmic system that create unfair outcomes for particular groups'),
           ('training data bias', 'bias that arises when the data used to build a model under-represents some groups or reflects past discrimination'),
           ('proxy variable', 'a variable that is not itself protected (e.g. postcode) but closely correlates with a protected characteristic (e.g. ethnicity), producing indirect discrimination'),
           ('historical bias', 'bias that exists in data because it records past unequal decisions or social inequalities, even if collected accurately'),
           ('feedback loop (bias)', 'when biased outputs influence future data, reinforcing the bias, as in predictive policing'),
           ('disparate impact', 'when a seemingly neutral rule or system disproportionately harms a protected group')],
    facts=[('In ProPublica\'s 2016 analysis of COMPAS in Broward County, Florida, what was the approximate false positive rate for Black defendants who did not reoffend, compared with white defendants?', 'About 45% compared with about 23%',
            ['About 10% compared with about 50%', 'About 23% compared with about 45%', 'Equal at about 30%'], 'Black defendants who did not reoffend were almost twice as likely to be labelled higher risk.'),
           ('The Gender Shades study (Buolamwini and Gebru, 2018) found the highest error rates of commercial gender-classification systems for which group?', 'Darker-skinned women', ['Lighter-skinned men', 'Lighter-skinned women', 'Darker-skinned men'], 'Error rates reached up to 34.7% for darker-skinned women vs 0.8% for lighter-skinned men.'),
           ('Why did Amazon abandon an experimental CV-screening tool (reported by Reuters in 2018)?', 'It had learned to downgrade CVs that included the word "women\'s"',
            ['It was too slow', 'It recommended only internal candidates', 'It was hacked'], 'It was trained on ten years of CVs submitted mostly by men.'),
           ('Which company developed the COMPAS risk-assessment tool?', 'Northpointe (now Equivant)', ['Palantir', 'IBM', 'Clearview AI'], 'COMPAS = Correctional Offender Management Profiling for Alternative Sanctions.')],
    why=[('Explain why an algorithm trained on historical data may discriminate even if it does not use race or gender as inputs.', 'Historical data records past discrimination, and other variables (postcode, school, gaps in employment) act as proxies for protected characteristics, so the model learns and reproduces the same unequal patterns.'),
         ('Explain why algorithmic bias can be more harmful than individual human bias.', 'An algorithm applies the same biased rule consistently to thousands or millions of cases, often invisibly and with an appearance of objectivity, making the harm larger and harder to detect and challenge.'),
         ('Explain why under-representation in training data leads to higher error rates for some groups.', 'If a model sees few examples of a group (e.g. darker-skinned faces), it learns their features poorly, so its predictions for that group are less accurate, as Gender Shades showed.')],
    contrast=[('training data bias', 'design bias', 'Training data bias comes from unrepresentative or historically unequal data; design bias comes from choices made by developers, such as which variables to use, the goal to optimise or the definition of "success".'),
              ('direct discrimination', 'indirect (proxy) discrimination', 'Direct discrimination uses a protected characteristic (e.g. gender) as an input; indirect discrimination arises when neutral-seeming variables (e.g. postcode) correlate with it and produce unequal outcomes.')],
    misc=[('Removing race from the input data guarantees that an algorithm is not racially biased.', 'Proxies such as postcode, income or arrest history correlate with race, so bias can persist; fairness must be tested on outcomes, not assumed from inputs.'),
          ('Algorithms are objective because they are based on mathematics.', 'Mathematics processes the data and goals chosen by people; biased data and design choices produce biased outputs, as COMPAS and Amazon\'s CV tool showed.')],
    cases=[('COMPAS (USA)', 'ProPublica\'s 2016 "Machine Bias" investigation of the COMPAS recidivism tool in Broward County found that Black defendants who did not reoffend were almost twice as likely as white defendants to be labelled higher risk; Northpointe disputed the analysis.', 'algorithmic bias in criminal justice',
            'unequal false positive rates meant the costs of errors fell disproportionately on Black defendants, influencing bail and sentencing decisions.'),
           ('Gender Shades (2018)', 'Joy Buolamwini and Timnit Gebru tested commercial facial-analysis systems from IBM, Microsoft and Face++ and found error rates up to 34.7% for darker-skinned women but 0.8% for lighter-skinned men.', 'bias from unrepresentative training data',
            'systems trained mostly on lighter-skinned, male faces performed worst on under-represented groups; the companies later improved their systems.'),
           ("Amazon's experimental hiring tool", 'Amazon built a machine-learning tool to rate CVs, trained on ten years of applications that came mostly from men; it penalised CVs containing "women\'s" and was abandoned (reported 2018).', 'historical bias',
            'the model learned past hiring patterns in a male-dominated industry and reproduced them, showing how historical inequality enters algorithms.')],
    sources=[('"If you train a machine on biased data, you get biased results – at scale and with a veneer of objectivity."', 'Joy Buolamwini, founder of the Algorithmic Justice League, interview 2019',
              'With reference to the source, explain two reasons why algorithmic bias is a serious concern.', 'It operates at scale, affecting many people at once, and it appears objective ("veneer of objectivity"), so people are less likely to question or challenge it.'),
             ('"Black defendants were often predicted to be at a higher risk of recidivism than they actually were."', 'ProPublica, "Machine Bias", May 2016',
              'Explain what kind of error the source describes and why it matters.', 'It describes false positives – people wrongly predicted to reoffend – which matter because they can lead to harsher bail or sentencing decisions for people who would not have reoffended.')],
    evaluate=[('Algorithmic bias is mainly a problem of biased data.',
               ['under-representation and historical bias in data (Gender Shades, Amazon)', 'better data can reduce error gaps'],
               ['design choices – goals, proxies, definitions of fairness – also create bias', 'deployment context (who uses it, how) matters', 'some fairness criteria cannot all be satisfied at once'],
               'Biased data is a major source, but bias also comes from design and deployment; fixing data alone is insufficient.'),
              ('Algorithms should not be used in criminal-justice decisions.',
               ['documented bias (COMPAS)', 'opacity and inability to challenge proprietary scores', 'liberty is at stake'],
               ['human judges are also biased and inconsistent', 'transparent, audited tools could reduce disparities', 'tools may help prioritise resources'],
               'Given the stakes, algorithms should at most advise, be transparent and independently audited; fully automated decisions are not justified.')],
    extended=[('Analyse the sources of bias in one algorithmic system you have studied and evaluate the measures taken to reduce it.', 'E.g. COMPAS, Gender Shades systems, Amazon CV tool, Dutch childcare benefits; sources: data, proxies, design, deployment; measures: retraining with diverse data, audits, regulation (NYC LL144, EU AI Act), abandonment; evaluate effectiveness.', 8, 'long')],
))
AR('ch08-st1', [
    ('An algorithm can discriminate by race even if race is not one of its inputs.', 'Variables such as postcode can act as proxies for race.', 'a', 'Proxies carry protected information indirectly.'),
    ('The Gender Shades study found the lowest error rates for darker-skinned women.', 'Facial-analysis systems were trained mainly on lighter-skinned male faces.', 'd', 'Error rates were highest for darker-skinned women; R is true.'),
])

R.facts('ch08-st2', F(
    terms=[('transparency', 'openness about how an algorithmic system works, what data it uses and how decisions are made'),
           ('explainability', 'the ability to give understandable reasons for a particular output of an algorithm'),
           ('black box', 'a system whose internal workings are hidden or too complex to understand, so only inputs and outputs are visible'),
           ('interpretable model', 'a model whose decision process humans can follow directly, such as a decision tree or a simple scoring rule'),
           ('trade secret', 'confidential business information, such as an algorithm\'s design, that companies protect from competitors'),
           ('counterfactual explanation', 'an explanation stating what would have needed to be different for a different outcome, e.g. "if your income were €5,000 higher, the loan would be approved"')],
    facts=[('In State v. Loomis (2016), which court upheld the use of COMPAS scores in sentencing while warning about their limitations?', 'The Wisconsin Supreme Court', ['The US Supreme Court', 'The European Court of Justice', 'The UK Supreme Court'], 'Loomis argued he could not challenge the proprietary algorithm.'),
           ('Which of the following is an example of an interpretable model?', 'A decision tree with a few clear yes/no rules', ['A deep neural network with millions of parameters', 'A large language model', 'An encrypted proprietary scoring system'], 'Its steps can be read and followed.'),
           ('Under the EU Digital Services Act, very large online platforms must offer users at least one recommender option that is not based on what?', 'Profiling of their personal data', ['Popularity', 'Advertising', 'Chronological order'], 'Article 38 DSA requires a non-profiling option.'),
           ('Which of these is a reason companies often give for not revealing how their algorithms work?', 'Protecting trade secrets and preventing manipulation (gaming)', ['Algorithms have no rules', 'It is illegal to publish code', 'Algorithms change every second'], 'Revealing ranking rules may help spammers game them.')],
    why=[('Explain why the "black box" problem makes it hard to challenge algorithmic decisions.', 'If neither the affected person nor the organisation can see why the system produced an output, the person cannot identify errors or bias, and the organisation cannot justify the decision, so appeals and accountability are weakened.'),
         ('Explain why there can be a trade-off between accuracy and explainability.', 'Complex models (deep neural networks) can find subtle patterns and be more accurate, but their millions of parameters make individual decisions hard to explain, while simpler, interpretable models may be less accurate.'),
         ('Explain why full transparency about an algorithm is not always desirable.', 'Publishing exact rules could let people game the system (spammers, fraudsters), expose trade secrets and personal data in training sets; meaningful explanation and independent audits may be better than publishing code.')],
    contrast=[('transparency', 'explainability', 'Transparency is openness about a system in general (purpose, data, logic, who uses it); explainability is being able to give reasons for a specific output (why this person was refused).'),
              ('an interpretable model', 'a black-box model', 'An interpretable model\'s logic can be followed by humans (e.g. a points-based score); a black-box model\'s internal workings are hidden or too complex to understand, so only inputs and outputs are observable.')],
    misc=[('Publishing an algorithm\'s source code makes it fully transparent and accountable.', 'Code alone may be unintelligible to most people and does not show the training data, how it is used or its effects; meaningful transparency needs explanations, documentation and audits.'),
          ('If an algorithm is accurate, it does not need to be explainable.', 'People affected by decisions have a right to understand and contest them, and explanations help find hidden bias; accuracy on average does not justify a particular decision.')],
    cases=[('State v. Loomis (Wisconsin, 2016)', 'Eric Loomis argued his sentence was influenced by a COMPAS score he could not examine because the algorithm was a trade secret; the court allowed its use but required warnings about its limitations.', 'the black box problem',
            'a proprietary algorithm influenced a liberty decision without the defendant being able to see or challenge its reasoning.'),
           ('the DSA recommender-transparency rules', 'From 2023–24 very large platforms in the EU must explain the main parameters of their recommender systems and offer a feed not based on profiling (e.g. TikTok and Instagram added chronological or non-personalised feeds in the EU).', 'regulation for transparency',
            'requiring explanations and alternatives gives users some insight and choice, without forcing companies to publish code.'),
           ('Apple Card credit limits (2019)', 'Some customers, including tech entrepreneur David Heinemeier Hansson, complained that women received much lower credit limits than their husbands; Goldman Sachs could not easily explain individual decisions. New York regulators later found no unlawful discrimination but criticised customer communication.', 'the need for explainability',
            'even without proven discrimination, the inability to explain decisions damaged trust and triggered an investigation.')],
    sources=[('"I could not cross-examine an algorithm."', 'Paraphrase of the argument made on behalf of Eric Loomis, State v. Loomis, 2016',
              'With reference to the source, explain why black-box algorithms raise concerns in justice systems.', 'Defendants have a right to challenge evidence used against them; if a proprietary algorithm\'s reasoning is secret, they cannot test its accuracy or bias, undermining due process.'),
             ('"The data subject shall have the right to obtain human intervention, to express his or her point of view and to contest the decision."', 'GDPR, Article 22(3)',
              'Explain how the right in the source relates to explainability.', 'Contesting a decision is only meaningful if the person understands the reasons for it, so the right implies some explanation of the logic involved and human review.')],
    evaluate=[('Companies should be required to explain every decision made by their algorithms.',
               ['people affected have a right to understand and contest decisions', 'explanations reveal bias and errors'],
               ['some models cannot give simple explanations', 'trade secrets and gaming risks', 'low-stakes decisions (song recommendations) may not need explanation'],
               'Explanation should be mandatory and meaningful for high-stakes decisions (credit, jobs, justice), while low-stakes systems need general transparency.'),
              ('Explainable AI solves the black box problem.',
               ['tools such as LIME, SHAP and counterfactuals give insight into decisions', 'interpretable models can be used for high-stakes cases'],
               ['explanations can be approximate or misleading', 'they may not reveal bias in training data', 'organisations still control what is disclosed'],
               'Explainability tools help but do not fully solve the problem; they need to be combined with audits, documentation and the right to contest.')],
    extended=[('A bank uses a complex machine-learning model to decide loan applications. Evaluate whether it should switch to a simpler, interpretable model.', 'Accuracy vs explainability trade-off; legal duties (GDPR Art 22, EU AI Act high-risk credit scoring); customer trust; possibility of explanation tools; recommendation with justification.', 8, 'long')],
))


@R.add('ch08-st3', 'C3', (2, 5), 'numerical')
def impact_ratio(rng, slot):
    ga, gb = rng.choice([('female applicants', 'male applicants'), ('applicants over 50', 'applicants under 50'),
                         ('Black applicants', 'white applicants'), ('applicants with a disability', 'applicants without a disability')])
    na = rng.choice([120, 200, 250, 400])
    nb = rng.choice([150, 300, 350, 500])
    sa = rng.randint(int(na * 0.15), int(na * 0.4))
    sb = rng.randint(int(nb * 0.3), int(nb * 0.5))
    ra, rb = sa / na, sb / nb
    if ra >= rb:
        return None
    ratio = ra / rb
    stem = (f'A bias audit of an automated CV-screening tool, of the kind required by New York City Local Law 144, found that {sa} of {na} {ga} and {sb} of {nb} {gb} were selected for interview. '
            f'Calculate the selection rate for each group and the impact ratio (lower rate ÷ higher rate).')
    ans = f'{pc(ra * 100)}% and {pc(rb * 100)}%; impact ratio {ratio:.2f}'
    key = f'{sa}/{na} = {pc(ra * 100)}% [A1]; {sb}/{nb} = {pc(rb * 100)}% [A1]; {pc(ra * 100)} ÷ {pc(rb * 100)} = {ratio:.2f} [M1 A1].'
    m = 4
    if slot.d >= 4:
        stem += ' Using the "four-fifths rule" used by US regulators as a rule of thumb, state whether this indicates possible adverse impact, and give one limitation of this test.'
        verdict = 'below 0.8, so possible adverse impact' if ratio < 0.8 else 'at least 0.8, so no adverse impact under the rule of thumb'
        ans += f'; {verdict}; limitation: e.g. small samples, ignores qualifications/other factors, only a rule of thumb'
        key += f' {ratio:.2f} is {verdict} [A1]; limitation e.g. statistical noise in small groups, does not show cause, intersectional groups missed [R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch08-st3', F(
    terms=[('algorithmic accountability', 'the principle that organisations deploying algorithms must be answerable for their impacts and able to justify and correct them'),
           ('algorithmic audit', 'an independent examination of an algorithmic system to check its accuracy, fairness, legality and impacts'),
           ('algorithmic impact assessment', 'a structured evaluation of the potential risks and effects of an algorithmic system before and during its use'),
           ('EU AI Act', 'the EU regulation (in force from August 2024) that classifies AI systems by risk – unacceptable, high, limited and minimal – with obligations for each level'),
           ('high-risk AI system', 'under the EU AI Act, an AI system used in areas such as hiring, credit scoring, education or law enforcement that must meet strict requirements'),
           ('right to contest', 'the right of a person affected by an automated decision to challenge it and obtain human review'),
           ('algorithm register', 'a public list of algorithms used by a government or city, describing their purpose and data (e.g. Amsterdam and Helsinki AI registers)')],
    facts=[('Which New York City law, enforced from July 2023, requires bias audits of automated employment decision tools?', 'Local Law 144', ['Local Law 97', 'Section 230', 'The SHIELD Act'], 'Employers must publish audit summaries and notify candidates.'),
           ('Under the EU AI Act, which of the following is banned as an "unacceptable risk"?', 'Social scoring of people by public authorities', ['Spam filters', 'AI in video games', 'Chatbots that disclose they are AI'], 'Prohibitions applied from February 2025.'),
           ('Which cities launched public AI/algorithm registers in 2020?', 'Amsterdam and Helsinki', ['Paris and Rome', 'Tokyo and Seoul', 'Lagos and Nairobi'], 'Registers describe the purpose, data and oversight of city algorithms.'),
           ('Which organisation, founded by Joy Buolamwini, campaigns for accountable AI?', 'The Algorithmic Justice League', ['The Electronic Frontier Foundation', 'Access Now', 'Privacy International'], 'Founded in 2016 after her research on facial analysis.')],
    why=[('Explain why accountability for algorithmic harms is difficult to assign.', 'Many actors are involved – data providers, developers, vendors, the organisation using the system and officials who rely on it – and opaque systems make it hard to show where the error arose, so each can shift blame ("the computer did it").'),
         ('Explain why independent audits are important for algorithmic accountability.', 'Organisations have incentives to present their systems positively; independent auditors can test outcomes across groups, check data and legality, and publish findings, giving external evidence on which regulators and the public can act.'),
         ('Explain why the EU AI Act uses a risk-based approach.', 'AI systems differ greatly in potential harm; banning or heavily regulating all AI would block harmless uses, so obligations are matched to risk – strict rules for high-risk uses such as hiring or policing and light rules for low-risk uses.')],
    contrast=[('an algorithmic audit', 'an algorithmic impact assessment', 'An audit examines an existing system\'s performance and effects (often independently, after deployment); an impact assessment anticipates risks and plans mitigations, usually before deployment and by the organisation itself.'),
              ('self-regulation by companies', 'legislation', 'Self-regulation relies on companies\' own ethics principles and voluntary measures (e.g. AI ethics boards); legislation imposes binding duties with penalties, such as the EU AI Act or NYC Local Law 144.')],
    misc=[('The EU AI Act bans all use of AI in hiring.', 'It classifies AI used in recruitment as high-risk, which is allowed but must meet requirements such as risk management, data quality, documentation, human oversight and transparency.'),
          ('If an algorithm makes a mistake, no human can be held responsible.', 'Organisations that design, buy and deploy algorithms remain legally and ethically responsible; in the Dutch childcare scandal the government resigned and the state paid compensation.')],
    cases=[('New York City Local Law 144', 'Since July 2023 employers in New York City using automated employment decision tools must commission an annual independent bias audit, publish a summary of impact ratios and notify candidates.', 'algorithmic audits as accountability',
            'it was one of the first laws requiring published audits, but critics note weak enforcement and that employers can decide their tools are out of scope.'),
           ('the EU AI Act (2024)', 'The AI Act entered into force on 1 August 2024, banning practices such as social scoring and setting strict obligations for high-risk systems, with fines of up to €35 million or 7% of global turnover for prohibited practices.', 'regulation of algorithms',
            'a binding, risk-based law gives regulators powers to require documentation, human oversight and conformity assessment before high-risk systems are used.'),
           ('the Dutch childcare-benefits scandal', 'After investigations showed a risk-scoring system and harsh enforcement wrongly accused thousands of families of fraud, the Dutch government resigned in 2021 and set up a compensation scheme; the data-protection authority fined the tax authority €2.75 million.', 'accountability after algorithmic harm',
            'political, legal and financial accountability followed, but only after years of harm, showing the need for earlier oversight.')],
    sources=[('"Providers of high-risk AI systems shall ensure that their systems are designed so that they can be effectively overseen by natural persons during the period in which they are in use."', 'Summary of EU AI Act, Article 14 (human oversight), 2024',
              'Explain how the requirement in the source contributes to accountability.', 'Human oversight means a responsible person can monitor, understand and override the system, so decisions are not left solely to the machine and someone can be held answerable.'),
             ('"We published our bias audit as required. Nobody told us what would happen if the ratios were poor."', 'HR manager at a New York employer, interviewed for a 2024 study of Local Law 144',
              'Explain one limitation of the law suggested by the source.', 'The law requires audits and publication but does not require employers to fix poor results or set clear consequences, so transparency may not lead to change.')],
    evaluate=[('Legislation is the most effective way to make algorithms accountable.',
               ['binding duties and penalties (EU AI Act fines up to 7%)', 'creates enforceable rights for affected people'],
               ['laws lag behind technology', 'enforcement capacity is limited', 'audits, journalism (ProPublica) and civil society often reveal harms first'],
               'Legislation is essential to make accountability enforceable, but it works best alongside independent audits, investigative journalism and public registers.'),
              ('Algorithm audits make automated hiring fair.',
               ['measure disparities such as impact ratios', 'public summaries create pressure to improve'],
               ['audits may only test limited groups and metrics', 'no obligation to change the tool (NYC LL144)', 'auditors may be paid by the employer'],
               'Audits improve visibility of bias but do not by themselves guarantee fairness without obligations to act and independent oversight.')],
    extended=[('Evaluate the effectiveness of one law or policy designed to make algorithms accountable.', 'E.g. EU AI Act, NYC Local Law 144, GDPR Art 22, Amsterdam/Helsinki registers; describe requirements; evaluate scope, enforcement, impact on stakeholders, loopholes; judgement.', 8, 'long')],
))

P2['ch08'] = dict(
    src=[('"Black defendants who did not reoffend were nearly twice as likely as white defendants to be misclassified as higher risk (45% versus 23%)."', 'ProPublica, "Machine Bias" investigation of COMPAS in Broward County, Florida, 2016',
          'Identify two pieces of evidence of bias in {S}.', ['Black defendants who did not reoffend were misclassified as higher risk at 45%', 'compared with 23% for white defendants – almost twice as likely'],
          'Explain why the evidence in {S} is significant for people affected by the tool.', 'Risk scores influence bail and sentencing; a higher false positive rate means innocent Black defendants were more often treated as dangerous, facing harsher outcomes.'),
         ('"Our analysis shows the tool is equally accurate for Black and white defendants: a given score means the same probability of reoffending in each group."', 'Summary of Northpointe\'s response to ProPublica, 2016',
          'Identify the measure of fairness used in {S}.', ['calibration / predictive parity', 'the same score means the same probability of reoffending across groups'],
          'Explain why {S} and the ProPublica findings could both be correct.', 'They use different definitions of fairness: equal calibration across groups and equal false positive rates cannot both hold when base rates of reoffending differ, so the tool can satisfy one and violate the other.'),
         ('"Unexplained algorithms should not decide who goes to prison."', 'Statement by a civil-liberties organisation following State v. Loomis, 2016',
          'Identify two concerns expressed or implied in {S}.', ['lack of explanation/transparency of the algorithm', 'serious consequences (liberty) of decisions based on it'],
          'Explain the perspective expressed in {S}.', 'It argues that when liberty is at stake, defendants must be able to understand and challenge evidence; secret, unexplained scores undermine due process.')],
    cmp=[(0, 1, 'the fairness of the COMPAS tool', ['both analyse COMPAS outcomes for Black and white defendants', 'both use statistical evidence'],
          ['Source A focuses on unequal false positive rates; Source B on equal calibration', 'A concludes the tool is biased; B concludes it is fair', 'A is an investigative journalist; B is the developer with a commercial interest']),
         (0, 2, 'concerns about algorithms in criminal justice', ['both raise concerns about using algorithms in justice decisions'],
          ['Source A provides statistical evidence of unequal errors; Source C makes a normative argument about transparency', 'A focuses on bias; C on explainability'])],
    ev=[(0, 1, 'algorithmic risk-assessment tools make criminal justice fairer.', ['consistent scores may reduce individual judges\' inconsistency', 'tool is calibrated across groups (Source B)'],
         ['unequal false positive rates (Source A)', 'proprietary and unexplained (Loomis)', 'historical arrest data embeds bias']),
        (1, 2, 'transparency is more important than accuracy for algorithms used in justice systems.', ['defendants must be able to challenge evidence (Source C)', 'transparency helps detect bias'],
         ['an accurate tool might reduce errors overall (Source B)', 'transparency alone does not fix bias'])],
)

INTV['ch08'] = [
    ('New York City Local Law 144', 'From July 2023, employers in New York City using automated employment decision tools must commission an independent bias audit every year, publish the selection rates and impact ratios by sex and race/ethnicity, and tell candidates that such a tool is used.',
     'Employers increasingly use automated tools to screen CVs and interviews, and evidence (e.g. Amazon\'s abandoned tool) showed such systems can reproduce discrimination invisibly at scale.',
     ['job candidates – more information about tools, but limited power to opt out or obtain changes', 'employers – audit costs and reputational pressure', 'tool vendors – need to provide audit data', 'auditors and regulators – new market, but limited enforcement'],
     ['first legal requirement for published bias audits', 'creates comparable metrics (impact ratios)', 'raises awareness among employers and candidates'],
     ['narrow definition lets employers claim tools are out of scope', 'no requirement to fix poor results', 'weak enforcement and few complaints'],
     'Broaden the definition of covered tools, require remediation when impact ratios fall below a threshold, and fund proactive enforcement.'),
    ('the EU AI Act\'s rules for high-risk AI systems', 'The EU AI Act (in force 2024) classifies AI used in recruitment, credit scoring, education and law enforcement as high-risk. Providers must manage risks, use quality data, keep logs, ensure human oversight and register systems before use; fines can reach €15 million or 3% of turnover for breaches of these duties.',
     'High-stakes decisions were increasingly made with opaque AI systems, with documented bias and few means for affected people to challenge them.',
     ['citizens – protection and transparency in high-stakes decisions', 'AI providers – compliance costs and documentation duties', 'EU start-ups – possible barrier to entry', 'national regulators – new supervisory tasks'],
     ['binding, risk-based obligations before deployment', 'EU-wide market influence (Brussels effect)', 'human oversight and logging enable accountability'],
     ['complex and slow to implement (phased to 2026–27)', 'standards still being developed', 'exemptions for national security'],
     'Provide clear technical standards and regulatory sandboxes for small firms, and give affected individuals an accessible complaints route.'),
]

# =============================================================================================
# ch09 Content 3.3 Computers: hardware, software and evolution
# =============================================================================================
@R.add('ch09-st1', 'C3', (1, 4), 'numerical')
def cpu_calc(rng, slot):
    kind = rng.choice(['cycles', 'ram'])
    if kind == 'cycles':
        ghz = rng.choice([1.8, 2.4, 3.0, 3.6, 4.2])
        cores = rng.choice([2, 4, 6, 8])
        dev = rng.choice(['a school laptop', 'a smartphone', 'a gaming PC', 'a library desktop'])
        stem = f'The processor in {dev} runs at {ghz} GHz and has {cores} cores. Calculate the number of clock cycles per second for one core, and for all cores together.'
        one = ghz * 1e9
        ans = f'{sci(one)} cycles per second per core; {sci(one * cores)} for all cores'
        key = f'{ghz} GHz = {ghz} × 10⁹ = {sci(one)} cycles/s [A1]; × {cores} = {sci(one * cores)} [A1].'
        m = 2
        if slot.d >= 3:
            stem += ' Explain why doubling the number of cores does not always double the speed of a program.'
            ans += '; many programs cannot be split into parallel tasks, and cores share memory and data'
            key += ' Not all tasks can be parallelised (sequential parts), plus overheads of coordination/memory [R1 R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    ram = rng.choice([4, 8, 16])
    os_ = rng.choice([2.5, 3, 3.5])
    apps = [(rng.choice(['a web browser with tabs', 'a video-call app', 'a photo editor', 'a music app', 'a word processor', 'a game']), rng.choice([0.5, 0.8, 1.2, 1.5, 2.5])) for _ in range(3)]
    if len({a for a, _ in apps}) < 3:
        return None
    used = os_ + sum(s for _, s in apps)
    free = ram - used
    stem = (f'A computer has {ram} GB of RAM. The operating system uses {os_:g} GB, and the user opens ' + ', '.join(f'{a} ({s:g} GB)' for a, s in apps) +
            '. Calculate the RAM still free, and state what happens if programs need more RAM than is available.')
    ans = f'{free:g} GB free' if free >= 0 else f'{-free:g} GB short'
    ans += '; the OS uses virtual memory (swapping to storage), which slows the computer'
    return dict(stem=stem, answer=ans, type='numerical', marks=3,
                markingKey=f'{ram} − ({os_:g} + ' + ' + '.join(f'{s:g}' for _, s in apps) + f') = {free:g} GB [M1 A1]; when RAM is full, data is swapped to secondary storage (virtual memory), which is much slower [R1].')


R.facts('ch09-st1', F(
    terms=[('central processing unit (CPU)', 'the component that fetches, decodes and executes instructions, carrying out the processing in a computer'),
           ('random-access memory (RAM)', 'volatile primary memory that holds data and programs currently in use; its contents are lost when power is off'),
           ('secondary storage', 'non-volatile storage such as SSDs and hard drives that keeps data when the power is off'),
           ('input device', 'hardware that sends data into a computer, such as a keyboard, microphone, camera or sensor'),
           ('output device', 'hardware that presents processed data to the user, such as a screen, speaker or printer'),
           ('graphics processing unit (GPU)', 'a processor designed for many parallel calculations, used for graphics and increasingly for training AI models'),
           ('clock speed', 'the number of cycles a processor performs per second, measured in hertz (e.g. 3 GHz = 3 billion cycles per second)')],
    facts=[('Which of these is volatile memory?', 'RAM', ['SSD', 'Hard disk drive', 'USB flash drive'], 'RAM loses its contents when power is removed.'),
           ('Which component is now essential for training large AI models because it performs many calculations in parallel?', 'GPU', ['Sound card', 'Optical drive', 'Keyboard controller'], 'Nvidia GPUs became central to AI training.'),
           ('Which of the following is an input device?', 'A touchscreen', ['A printer', 'A speaker', 'A projector'], 'A touchscreen is both input and output, but it is used for input here.'),
           ('What does the processor do in the fetch–decode–execute cycle?', 'Fetches an instruction from memory, decodes it and carries it out', ['Stores files permanently', 'Converts analogue sound to digital', 'Connects to the internet'], 'This cycle repeats billions of times per second.')],
    why=[('Explain why computers need both RAM and secondary storage.', 'RAM is fast, so the CPU can access running programs and data quickly, but it is volatile and expensive; secondary storage is slower but non-volatile and cheaper, so it keeps files and software when power is off.'),
         ('Explain why solid-state drives (SSDs) have largely replaced hard disk drives in laptops.', 'SSDs have no moving parts, so they are faster, more durable, quieter and use less power, which suits portable devices, even though they cost more per gigabyte.'),
         ('Explain why access to GPUs has become a source of power in digital society.', 'Training advanced AI models requires vast numbers of GPUs; a few firms (e.g. Nvidia as supplier, large cloud companies as buyers) control access, and governments impose export controls (e.g. US restrictions on chips to China), so compute shapes economic and geopolitical power.')],
    contrast=[('RAM', 'secondary storage', 'RAM is fast, volatile primary memory for data currently in use; secondary storage (SSD/HDD) is slower, non-volatile and keeps data permanently.'),
              ('a CPU', 'a GPU', 'A CPU has a few powerful cores optimised for general sequential tasks; a GPU has thousands of simpler cores optimised for parallel calculations such as graphics and AI training.')],
    misc=[('More RAM always makes a computer faster.', 'Extra RAM helps only if the computer is running out of memory; beyond that, speed depends on the CPU, storage and software.'),
          ('A higher clock speed always means a faster computer.', 'Performance also depends on the number of cores, architecture (instructions per cycle), cache, memory and software; a newer 3 GHz chip can outperform an older 4 GHz one.')],
    cases=[('Nvidia GPUs and the AI boom', 'Demand for Nvidia\'s data-centre GPUs for training AI models made it one of the world\'s most valuable companies by 2024; the US restricted exports of advanced chips to China from 2022.', 'hardware as a source of power',
            'control of a key component for AI gives companies and states leverage over who can build advanced AI.'),
           ('the global chip shortage (2020–2023)', 'Pandemic demand and supply disruptions caused shortages of semiconductors, forcing car makers to cut production.', 'interdependence of hardware supply chains',
            'many industries depend on a few chip manufacturers (e.g. TSMC in Taiwan), so disruption in one place affected economies worldwide.'),
           ('assistive input devices', 'Devices such as eye-tracking systems, switch controls and the Xbox Adaptive Controller (2018) let people with limited mobility use computers.', 'how input devices affect access',
            'adapting input hardware to different bodies makes computing usable by more people, showing hardware design shapes inclusion.')],
    sources=[('"Compute is the new oil."', 'Commentary on AI and semiconductors, technology magazine, 2023',
              'Explain what the source suggests about computer hardware in digital society.', 'Computing power (chips, GPUs, data centres) has become a strategic resource that determines who can build AI and digital services, giving economic and political power to those who control it.'),
             ('"About 90% of the world\'s most advanced chips are made by one company on one island."', 'Report on semiconductor supply chains, 2022 (referring to TSMC in Taiwan)',
              'Explain one implication of the situation described in the source.', 'Concentrated production creates vulnerability: a natural disaster, conflict or blockade affecting Taiwan could disrupt the global supply of advanced chips, so governments subsidise domestic production (e.g. US CHIPS Act 2022).')],
    evaluate=[('The most important component of a computer for digital society is its processor.',
               ['processing power enables AI, simulation and real-time services', 'GPUs drive the AI economy'],
               ['data storage and networks matter as much for most uses', 'input/output design determines accessibility', 'software and people determine impacts'],
               'Processors are crucial, but impacts depend on the whole system – storage, networks, interfaces and software.'),
              ('Concentrated production of computer chips is a serious risk to digital society.',
               ['shortages 2020–23 disrupted industries', 'geopolitical tension over Taiwan'],
               ['governments are diversifying production (US CHIPS Act, EU Chips Act)', 'specialisation lowers costs and spreads innovation'],
               'Concentration is a significant systemic risk, which current diversification policies reduce only slowly.')],
    extended=[('Explain the role of the CPU, RAM and secondary storage when a student opens and edits a video on a laptop, and evaluate which upgrade would most improve their experience.', 'Storage holds the video and editor; loaded into RAM; CPU/GPU process edits; bottlenecks: RAM (swapping), storage speed (HDD vs SSD), GPU for rendering; justify an upgrade.', 6, 'long')],
))

R.facts('ch09-st2', F(
    terms=[('operating system', 'system software that manages hardware, memory, files and processes and provides a user interface, such as Windows, macOS, Android or Linux'),
           ('application software', 'programs that let users carry out tasks, such as word processors, browsers and games'),
           ('open-source software', 'software whose source code is publicly available and can be studied, modified and shared under an open licence, such as Linux or Firefox'),
           ('proprietary software', 'software owned by a company whose source code is kept secret and whose use is restricted by licence, such as Microsoft Windows or Adobe Photoshop'),
           ('embedded system', 'a computer built into a larger device to perform a dedicated function, such as in a washing machine, car or pacemaker'),
           ('GNU General Public License (GPL)', 'an open-source licence that lets anyone use and modify software but requires modified versions that are distributed to remain open source ("copyleft")'),
           ('wearable device', 'a computer worn on the body, such as a smartwatch or fitness tracker')],
    facts=[('Which operating system is based on the Linux kernel?', 'Android', ['iOS', 'Windows', 'macOS'], 'Android uses a modified Linux kernel.'),
           ('Who created the Linux kernel in 1991?', 'Linus Torvalds', ['Richard Stallman', 'Bill Gates', 'Steve Wozniak'], 'Torvalds released Linux as a student in Helsinki.'),
           ('Which of these is an example of an embedded system?', 'The computer controlling a car\'s anti-lock brakes', ['A desktop PC', 'A cloud server', 'A laptop'], 'Embedded systems perform dedicated functions within devices.'),
           ('Which country\'s Kerala state moved its school computers to free and open-source software (IT@School)?', 'India', ['Brazil', 'France', 'South Africa'], 'Kerala\'s IT@School project adopted FOSS from the mid-2000s.')],
    why=[('Explain why some governments choose open-source software for public services.', 'It avoids licence fees and vendor lock-in, allows local developers to adapt and audit code for security, and keeps public data in open formats, supporting digital sovereignty.'),
         ('Explain why proprietary software companies can exercise power over users.', 'They control updates, file formats, pricing and which devices are supported, so users and organisations become dependent (lock-in) and must accept licence terms and data collection.'),
         ('Explain why the operating system is essential for using a computer.', 'It manages hardware resources (memory, CPU, storage), runs applications, handles security and provides an interface, so users and apps do not need to control hardware directly.')],
    contrast=[('open-source software', 'proprietary software', 'Open-source software publishes its source code for anyone to study, modify and share (Linux, LibreOffice); proprietary software keeps code secret and restricts use through licences (Windows, Photoshop).'),
              ('system software', 'application software', 'System software (operating systems, drivers) runs and manages the computer; application software helps users perform specific tasks (browsers, games).')],
    misc=[('Open-source software is less secure because anyone can see the code.', 'Visible code can be audited by many people, so flaws may be found and fixed quickly; security depends on maintenance and review (though under-funded projects can still have serious bugs, e.g. Heartbleed in OpenSSL, 2014).'),
          ('Open-source software is always free of charge and unsupported.', 'Open source refers to access to code and licence rights; companies (e.g. Red Hat) sell support, and many open-source projects are maintained by large organisations.')],
    cases=[('Android and open source', 'Google\'s Android is built on the open-source Linux kernel and the Android Open Source Project, but most phones also ship with proprietary Google services; the EU fined Google €4.34 billion in 2018 (reduced to €4.1 billion) over Android restrictions.', 'open source and platform power',
            'open-source code helped Android spread to billions of cheap phones, while control of proprietary services kept power with Google.'),
           ('Heartbleed (2014)', 'A bug in OpenSSL, open-source encryption software maintained by a handful of volunteers, exposed data on a large share of web servers.', 'the sustainability of open-source infrastructure',
            'critical infrastructure depended on under-funded volunteers, leading to the Core Infrastructure Initiative to fund key projects.'),
           ('Munich\'s LiMux project', 'Munich moved thousands of city computers from Windows to Linux (LiMux) from 2004, but the city council voted in 2017 to return to Windows, citing compatibility problems.', 'trade-offs between open-source and proprietary software',
            'the switch saved licence costs and reduced lock-in, but compatibility and user resistance showed the strength of proprietary ecosystems.')],
    sources=[('"Free software is a matter of liberty, not price. Think of free as in free speech, not as in free beer."', 'Richard Stallman, Free Software Foundation',
              'Explain what the source means.', 'The free/open software movement is about users\' freedom to run, study, modify and share software, not whether it costs money.'),
             ('"Roughly 70–90% of the code in a typical modern application is open source."', 'Industry software-supply-chain report, 2023',
              'Explain one implication of the claim in the source.', 'Most software depends on open-source components maintained by others, so vulnerabilities in widely used libraries (e.g. Log4Shell, 2021) can affect huge numbers of organisations at once.')],
    evaluate=[('Governments should use only open-source software.',
               ['no licence fees; avoids lock-in', 'transparency and ability to audit', 'supports local IT skills'],
               ['retraining and compatibility costs (Munich LiMux reversal)', 'some specialised software has no open alternative', 'support and security still need funding'],
               'Open source should be preferred where viable, but a pragmatic mix is often necessary; policies like "public money, public code" are a balanced approach.'),
              ('Operating systems give technology companies more power than any app.',
               ['control of app stores, defaults and permissions', 'iOS/Android duopoly on mobile'],
               ['regulation (DMA) forces openness', 'apps with network effects (WhatsApp) also have huge power', 'web apps bypass OS stores'],
               'Control of the operating system is a particularly strong form of power because it sits beneath all apps, though it is increasingly challenged by regulators.')],
    extended=[('A school must choose between proprietary and open-source software for its 500 computers. Evaluate the options for two stakeholders.', 'Students (skills, familiarity, cost of home access), teachers (training, compatibility), school (licence costs, support, lock-in), IT staff; examples (Kerala IT@School, Munich); recommendation.', 6, 'long')],
))


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def moore(rng, slot):
    start = rng.choice([(1971, 2300, 'the Intel 4004'), (1978, 29000, 'the Intel 8086'), (1993, 3100000, 'the Intel Pentium'),
                        (2000, 42000000, 'the Intel Pentium 4')])
    y0, t0, chip = start
    yrs = rng.choice([10, 20, 30]) if slot.d >= 3 else rng.choice([4, 6, 10])
    period = 2
    n = yrs / period
    pred = t0 * 2 ** n
    stem = f'{chip[0].upper() + chip[1:]} ({y0}) had about {t0:,} transistors. Assuming Moore\'s law (transistor counts double every two years), estimate the number of transistors on a chip {yrs} years later.'
    ans = f'about {sci(pred)}'
    key = f'{yrs} ÷ 2 = {n:g} doublings [M1]; {t0:,} × 2^{n:g} = {sci(pred)} [M1 A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain one reason why Moore\'s law is slowing down.'
        ans += '; transistors are approaching atomic scale, so further shrinking is physically harder, more expensive and generates heat'
        key += ' Physical limits (atomic scale, quantum tunnelling, heat) and rising fabrication costs [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch09-st3', F(
    terms=[('Moore\'s law', 'Gordon Moore\'s observation (1965, revised 1975) that the number of transistors on a chip doubles about every two years'),
           ('transistor', 'a tiny electronic switch that is the basic building block of processors and memory chips'),
           ('miniaturisation', 'the trend of making electronic components and devices smaller, more powerful and cheaper over time'),
           ('ubiquitous computing', 'computing embedded everywhere in everyday objects and environments, rather than only in desktop computers'),
           ('mainframe', 'a large, powerful computer used by organisations to process large volumes of data, dominant from the 1950s to 1970s'),
           ('personal computer', 'a general-purpose computer designed for individual use, which spread from the late 1970s and 1980s (e.g. the IBM PC, 1981)')],
    facts=[('In which year did Gordon Moore first publish his observation about the doubling of components on integrated circuits?', '1965', ['1945', '1981', '2007'], 'Published in Electronics magazine in 1965.'),
           ('Which early electronic general-purpose computer was unveiled in 1946 and filled a large room?', 'ENIAC', ['Apple II', 'IBM PC', 'Raspberry Pi'], 'ENIAC used about 18,000 vacuum tubes.'),
           ('Which product, launched in 2007, popularised the touchscreen smartphone with an app ecosystem?', 'The Apple iPhone', ['The IBM Simon', 'The Nokia 3310', 'The BlackBerry Pearl'], 'The App Store followed in 2008.'),
           ('Where was the transistor invented in 1947?', 'Bell Labs', ['IBM', 'CERN', 'Xerox PARC'], 'Bardeen, Brattain and Shockley won the 1956 Nobel Prize in Physics.')],
    why=[('Explain why Moore\'s law has had major social consequences.', 'Exponential growth in processing power at falling cost made computers small and cheap enough for homes, pockets and everyday objects, enabling smartphones, the internet economy and AI.'),
         ('Explain why mobile devices have had greater impact in many low-income countries than desktop computers.', 'Mobile phones are cheaper, need less power and infrastructure, and connect through mobile networks rather than fixed lines, so many people went straight to mobile internet ("leapfrogging"), e.g. M-Pesa in Kenya.'),
         ('Explain why wearable devices raise new privacy questions.', 'They collect continuous, intimate data (heart rate, sleep, location, menstrual cycles) that can reveal health conditions and routines, and this data may be shared with insurers, employers or law enforcement.')],
    contrast=[('a mainframe era', 'a mobile era', 'In the mainframe era computing was centralised in large machines owned by organisations and used by specialists; in the mobile era computing is personal, portable and connected, used by billions of individuals.'),
              ('Moore\'s law', 'a law of physics', 'Moore\'s law is an empirical observation of an industry trend that depended on investment and engineering and is now slowing; a law of physics describes a natural regularity that does not depend on business choices.')],
    misc=[('Moore\'s law says computers double in speed every year.', 'It refers to the number of transistors on a chip roughly doubling about every two years; speed does not simply double, and the trend is slowing.'),
          ('The history of computing is simply a story of technology getting better.', 'Changes in computing were shaped by military funding (ENIAC), markets, regulation and users, and brought new problems such as e-waste, surveillance and inequality.')],
    cases=[('the smartphone revolution', 'Smartphone ownership spread from almost zero in 2007 to billions of users, many of whom first accessed the internet by phone.', 'the evolution of computing',
            'computing moved from desks to pockets, enabling mobile banking, ride-hailing and social media for people who never owned a PC.'),
           ('Apple Watch and heart monitoring', 'The Apple Watch received US FDA clearance in 2018 for an ECG feature that can detect signs of atrial fibrillation.', 'wearable computing in health',
            'wearables bring medical-grade monitoring into everyday life, which can save lives but also creates anxiety from false alarms and new health-data privacy concerns.'),
           ('ENIAC (1946)', 'ENIAC was built for the US Army to calculate artillery tables, weighed about 27 tonnes and was programmed by six women mathematicians whose role was long overlooked.', 'the social history of computing',
            'early computing was driven by military needs and depended on women programmers, showing that computing history is also a history of people and power.')],
    sources=[('"The complexity for minimum component costs has increased at a rate of roughly a factor of two per year."', 'Gordon Moore, "Cramming more components onto integrated circuits", Electronics, 1965',
              'Explain how the trend described in the source was revised and why it matters.', 'Moore revised the rate to doubling roughly every two years (1975); the trend guided industry planning and led to cheap, powerful devices.'),
             ('"There is no reason anyone would want a computer in their home."', 'Remark attributed to Ken Olsen, founder of Digital Equipment Corporation, 1977 (he later said it referred to computers controlling homes)',
              'Explain what the source shows about predicting technological change.', 'Even experts underestimated how computers would spread; predictions are shaped by current uses, and the context of quotations is often lost, so sources must be checked.')],
    evaluate=[('Smartphones have been the most significant development in the history of computing.',
               ['brought computing and internet to billions, including in low-income countries', 'enabled new economies (apps, mobile money, gig work)'],
               ['the transistor, PC and internet made smartphones possible', 'cloud and AI may prove more transformative', 'smartphones raised problems of addiction and surveillance'],
               'Smartphones are arguably the most socially significant development so far because of their reach, though they built on earlier breakthroughs.'),
              ('Wearable devices do more good than harm.',
               ['early detection of health problems (AFib)', 'motivation for exercise and sleep improvement'],
               ['intimate data shared or sold', 'anxiety and over-diagnosis', 'unequal access by cost'],
               'Wearables bring real health benefits for users who can afford them, provided strong rules govern health data.')],
    extended=[('Analyse how one development in the history of computing (e.g. the personal computer, the smartphone, wearables) changed society, using at least two Digital Society concepts.', 'Choose development; describe; analyse change, identity, power, space or systems with examples; evaluate overall significance.', 6, 'long')],
))

# =============================================================================================
# ch10 Content 3.3 Computers: access, equity and environmental impact
# =============================================================================================
DIVIDE = [  # (group pair, context, rate a, rate b) – illustrative survey data
    ('urban households', 'rural households'), ('men', 'women'), ('households in the richest fifth', 'households in the poorest fifth'),
    ('people aged 16–24', 'people aged 65 and over'), ('students at private schools', 'students at government schools')]


@R.add('ch10-st1', 'C3', (1, 5), 'numerical')
def divide_calc(rng, slot):
    ga, gb = rng.choice(DIVIDE)
    pa = rng.randint(70, 95)
    pb = rng.randint(25, pa - 15)
    country = rng.choice(['a lower-middle-income country', 'a region of South Asia', 'a country in sub-Saharan Africa', 'a Latin American country', 'a Southeast Asian country'])
    measure = rng.choice(['used the internet in the last three months', 'own a smartphone', 'have a broadband connection at home'])
    gap = pa - pb
    stem = f'A survey in {country} found that {pa}% of {ga} and {pb}% of {gb} {measure}. Calculate the gap in percentage points'
    if slot.d >= 3:
        pop = rng.choice([2, 4, 8, 12, 30]) * 1_000_000
        stem += f' and, if there are {pop:,} {gb}, how many of them do not.'
        nn = pop * (100 - pb) // 100
        ans = f'{gap} percentage points; {nn:,} {gb}'
        key = f'{pa} − {pb} = {gap} percentage points [A1]; (100 − {pb})% × {pop:,} = {nn:,} [M1 A1].'
        m = 3
        if slot.d >= 4:
            stem = stem.rstrip('.') + f'. Also calculate the relative gap ({gb} rate as a percentage of the {ga} rate) and explain why percentage points and percentages differ.'
            rel = pb / pa * 100
            ans += f'; relative rate {pc(rel)}%'
            key += f' {pb} ÷ {pa} × 100 = {pc(rel)}% [A1]; percentage points are an absolute difference between rates, a percentage compares relative size [R1].'
            m = 5
    else:
        stem += '.'
        ans = f'{gap} percentage points'
        key = f'{pa} − {pb} = {gap} percentage points [A1].'
        m = 1
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch10-st1', F(
    terms=[('digital divide', 'the gap between those who have access to digital technologies and the skills to use them effectively and those who do not'),
           ('first-level digital divide', 'differences in physical access to devices and internet connections'),
           ('second-level digital divide', 'differences in digital skills and the ways people use technology'),
           ('third-level digital divide', 'differences in the benefits or outcomes people gain from using digital technology'),
           ('digital literacy', 'the skills needed to find, evaluate, create and communicate information using digital technologies safely and effectively'),
           ('gender digital divide', 'the gap between men and women in access to and use of digital technologies'),
           ('affordability', 'whether people can pay for devices and data; the UN target is that 1 GB of mobile data should cost less than 2% of average monthly income')],
    facts=[('According to the ITU, approximately how many people worldwide were still offline in 2024?', 'About 2.6 billion', ['About 200 million', 'About 5.5 billion', 'About 50 million'], 'About 5.5 billion (68%) were online and 2.6 billion offline.'),
           ('What affordability target for broadband was set by the UN Broadband Commission?', 'Entry-level broadband costing less than 2% of monthly gross national income per capita', ['Free internet for all by 2020', 'Data costing less than 10% of income', '1 GB costing less than US$10'], 'The "1 for 2" target: 1 GB for less than 2% of monthly income.'),
           ('Which level of the digital divide refers to differences in skills and how people use technology?', 'The second level', ['The first level', 'The third level', 'The zero level'], 'First = access, second = skills/use, third = outcomes.'),
           ('According to the GSMA, in low- and middle-income countries women are less likely than men to use mobile internet. Roughly how much less likely (2024 report)?', 'About 15%', ['About 1%', 'About 60%', 'About 90%'], 'The GSMA Mobile Gender Gap Report 2024 estimated a 15% gap.')],
    why=[('Explain why closing the access gap does not automatically close the digital divide.', 'Even with devices and connections, people may lack the skills, confidence, relevant content in their language, or time to use technology effectively, so inequalities in use and outcomes (second and third levels) persist.'),
         ('Explain why the digital divide can deepen existing inequalities.', 'As jobs, education, banking and government services move online, those without access or skills are excluded from opportunities and information, so the disadvantaged fall further behind.'),
         ('Explain why women in many countries have lower access to mobile internet than men.', 'Barriers include affordability (lower incomes), literacy and digital skills, social norms and family restrictions on phone use, and concerns about safety and harassment.')],
    contrast=[('the first-level digital divide', 'the second-level digital divide', 'The first level concerns physical access to devices and connectivity; the second concerns skills and how effectively people use that access.'),
              ('a global digital divide', 'a domestic digital divide', 'A global divide is between countries (e.g. most people online in Europe vs under half in many least developed countries); a domestic divide is within a country (urban/rural, rich/poor, young/old).')],
    misc=[('The digital divide only exists in low-income countries.', 'High-income countries also have divides by income, age, disability and rurality – e.g. students in the US "homework gap" lacking home broadband during COVID-19.'),
          ('Giving every student a laptop closes the digital divide.', 'Devices without connectivity, maintenance, teacher training and relevant content may have little effect; One Laptop per Child evaluations in Peru found no significant improvement in maths or reading.')],
    cases=[('remote learning during COVID-19', 'UNICEF estimated that at least 463 million schoolchildren could not be reached by remote learning when schools closed in 2020.', 'the digital divide in education',
            'unequal access to devices, connectivity and support turned school closures into unequal learning losses, deepening educational inequality.'),
           ('One Laptop per Child in Peru', 'Peru distributed hundreds of thousands of low-cost XO laptops from 2008; an Inter-American Development Bank evaluation found no significant effect on maths or reading scores.', 'why access alone does not close the divide',
            'devices without teacher training, connectivity and integration into teaching did not improve learning outcomes.'),
           ('the mobile gender gap', 'GSMA reports show women in low- and middle-income countries are less likely than men to use mobile internet, with the widest gaps in South Asia and sub-Saharan Africa.', 'the gender digital divide',
            'affordability, skills and social norms limit women\'s access, reducing their access to information, finance and work.')],
    sources=[('"Access to the internet is no longer a luxury. It is a prerequisite for participating in society, the economy and democracy."', 'ITU Secretary-General, Facts and Figures report foreword, 2023',
              'With reference to the source, explain why the digital divide is a serious issue.', 'If participation in society, work and democracy depends on internet access, those offline are excluded from opportunities and rights, so the divide becomes a form of social exclusion.'),
             ('"My daughter does her homework on my phone after I come home from work, using the data that is left."', 'Parent in Mexico City, interviewed for a 2021 study on remote learning',
              'Explain how the source illustrates more than one level of the digital divide.', 'Access: a single shared phone and limited data (first level); use: homework is limited by time and device suitability (second level); outcomes: the child may learn less than peers with laptops and broadband (third level).')],
    evaluate=[('Governments, not companies, should be responsible for closing the digital divide.',
               ['access is a public good linked to rights and services', 'markets under-serve poor and rural areas'],
               ['companies drive infrastructure and cheaper devices', 'public–private partnerships (BharatNet, Giga) combine strengths', 'civil society delivers skills training'],
               'Governments should lead and set targets, but closing the divide needs partnerships with companies and civil society.'),
              ('The digital divide is now mainly about skills rather than access.',
               ['mobile coverage reaches most of the world\'s population', 'many people with access lack skills (usage gap)'],
               ['2.6 billion people still offline', 'affordability and device costs remain major barriers', 'access quality (speed, data caps) varies hugely'],
               'Skills and usage gaps are growing in importance, but access and affordability remain the main barriers for billions; both must be addressed.')],
    extended=[('Analyse the causes of the digital divide in one country or community you have studied and evaluate one intervention designed to reduce it.', 'Causes: cost, infrastructure, skills, language, gender norms, disability; intervention e.g. BharatNet, Giga school connectivity, public Wi-Fi, digital skills training, device schemes; evaluate effectiveness and stakeholders.', 8, 'long')],
))


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def ewaste_energy(rng, slot):
    kind = rng.choice(['ewaste', 'energy', 'lifetime'])
    if kind == 'ewaste':
        gen = rng.choice([(62, 22.3, 'the world in 2022'), (0.9, 38, 'a European country'), (0.45, 5, 'a West African country'), (2.1, 15, 'a Southeast Asian country')])
        tot, rate, place = gen
        rec = tot * rate / 100
        stem = f'{place[0].upper() + place[1:]} generated about {tot:g} million tonnes of e-waste, of which {rate:g}% was formally collected and recycled. Calculate the amount NOT documented as recycled.'
        ans = f'{tot - rec:.3g} million tonnes'
        key = f'{rate:g}% of {tot:g} = {rec:.3g} Mt recycled [M1]; {tot:g} − {rec:.3g} = {tot - rec:.3g} Mt not recycled [A1].'
        m = 2
        if slot.d >= 3:
            stem += ' Explain one environmental and one social consequence of e-waste that is not formally recycled.'
            ans += '; e.g. toxic metals (lead, mercury) contaminating soil and water; informal workers (e.g. at Agbogbloshie, Ghana) exposed to harmful fumes from burning cables'
            key += ' Environmental (toxins, lost resources) [R1]; social/health (informal recycling, child labour, health harms) [R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    if kind == 'energy':
        watts = rng.choice([65, 120, 250, 400])
        hrs = rng.choice([4, 6, 8, 10])
        days = rng.choice([200, 250, 365])
        n = rng.choice([30, 120, 500])
        cf = rng.choice([0.2, 0.4, 0.7])
        kwh = watts * hrs * days * n / 1000
        co2 = kwh * cf
        stem = (f'A school has {n} computers, each using {watts} W, switched on for {hrs} hours a day on {days} days a year. Calculate the annual electricity use in kWh'
                + (f' and the CO₂ emitted if the grid produces {cf} kg CO₂ per kWh.' if slot.d >= 3 else '.'))
        ans = f'{kwh:,.0f} kWh' + (f'; {co2:,.0f} kg CO₂' if slot.d >= 3 else '')
        key = f'{watts} W × {hrs} h × {days} × {n} = {watts * hrs * days * n:,} Wh [M1]; ÷ 1000 = {kwh:,.0f} kWh [A1].' + (f' × {cf} = {co2:,.0f} kg CO₂ [A1].' if slot.d >= 3 else '')
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=3 if slot.d >= 3 else 2)
    emb = rng.choice([55, 70, 85])
    use = rng.choice([5, 8, 12])
    y1, y2 = rng.choice([(2, 4), (2, 5), (3, 5)])
    a1 = (emb + use * y1) / y1
    a2 = (emb + use * y2) / y2
    stem = (f'A smartphone causes about {emb} kg CO₂e in manufacturing and about {use} kg CO₂e per year in use. Calculate the average emissions per year of use if it is kept for {y1} years and for {y2} years, '
            f'and state what this suggests about device lifetimes.')
    ans = f'{a1:.1f} kg/yr vs {a2:.1f} kg/yr; keeping devices longer spreads manufacturing emissions, so longer lifetimes (repair, right to repair) reduce impact'
    return dict(stem=stem, answer=ans, type='numerical', marks=4,
                markingKey=f'({emb} + {use}×{y1}) ÷ {y1} = {a1:.1f} [M1 A1]; ({emb} + {use}×{y2}) ÷ {y2} = {a2:.1f} [A1]; most emissions are from manufacturing, so longer use reduces annual impact [R1].')


R.facts('ch10-st2', F(
    terms=[('e-waste', 'discarded electrical and electronic equipment, such as phones, computers and batteries'),
           ('embodied carbon', 'the greenhouse-gas emissions produced in extracting materials, manufacturing and transporting a product before it is used'),
           ('planned obsolescence', 'designing products to have a limited useful life or to become outdated so that consumers replace them'),
           ('right to repair', 'policies that require manufacturers to make spare parts, tools and repair information available so products can be repaired'),
           ('conflict minerals', 'minerals such as tin, tantalum (from coltan), tungsten and gold mined in conflict areas, where profits may fund armed groups'),
           ('power usage effectiveness (PUE)', 'a measure of data-centre efficiency: total facility energy divided by the energy used by IT equipment (1.0 is ideal)'),
           ('circular economy', 'an economic model that keeps products and materials in use through reuse, repair, refurbishment and recycling')],
    facts=[('According to the Global E-waste Monitor 2024, how much e-waste was generated worldwide in 2022?', 'About 62 million tonnes', ['About 6 million tonnes', 'About 620 million tonnes', 'About 1 million tonnes'], 'Only 22.3% was documented as formally collected and recycled.'),
           ('Which country produces around 70% of the world\'s mined cobalt, used in lithium-ion batteries?', 'The Democratic Republic of the Congo', ['Chile', 'Australia', 'China'], 'Cobalt mining in the DRC has been linked to child labour in artisanal mines.'),
           ('From when did the EU require new phones and many other small devices to use a USB-C charging port?', 'December 2024', ['January 2018', 'June 2030', 'March 2020'], 'The common-charger rule aims to cut e-waste.'),
           ('Which site in Accra, Ghana, became internationally known for informal e-waste processing?', 'Agbogbloshie', ['Dharavi', 'Kibera', 'Lagos Island'], 'Workers burned cables to recover copper; the scrapyard was demolished in 2021.')],
    why=[('Explain why most of the carbon footprint of a smartphone occurs before it is used.', 'Mining metals, manufacturing chips and screens and global transport use large amounts of energy, while a phone uses little electricity when charging, so manufacturing (embodied carbon) dominates its lifetime emissions.'),
         ('Explain why e-waste is often exported to lower-income countries.', 'Formal recycling is expensive in high-income countries, and used electronics can be exported labelled as "second-hand goods"; informal recyclers in places such as Ghana or Pakistan recover metals cheaply, often unsafely.'),
         ('Explain why the growth of AI is increasing concern about the environmental impact of computing.', 'Training and running large AI models require huge numbers of GPUs in data centres that consume large amounts of electricity and water for cooling, so demand for energy and hardware is rising quickly.')],
    contrast=[('embodied carbon', 'operational carbon', 'Embodied carbon is emitted in making and transporting a device; operational carbon is emitted from the electricity used while it runs.'),
              ('formal recycling', 'informal recycling', 'Formal recycling uses regulated facilities with safety and pollution controls; informal recycling is unregulated work, often burning or acid-stripping components, which harms workers and the environment.')],
    misc=[('Digital technology is environmentally friendly because it is "virtual".', 'Digital services depend on physical devices, mining, data centres and networks that use energy, water and minerals and create e-waste.'),
          ('Recycling solves the e-waste problem.', 'Only about a fifth of e-waste is formally recycled, and recycling recovers only some materials; reducing consumption, longer lifetimes and repair are also necessary.')],
    cases=[('Agbogbloshie, Accra', 'For years workers, including children, at Agbogbloshie burned cables and dismantled imported electronics to recover copper and other metals, exposing themselves to toxic fumes; the site was demolished by the authorities in 2021.', 'environmental and social impacts of e-waste',
            'the costs of global electronics consumption were borne by informal workers in a low-income country, illustrating environmental injustice.'),
           ('cobalt mining in the DRC', 'Amnesty International (2016) documented children working in artisanal cobalt mines in the DRC that supplied battery supply chains for major electronics brands.', 'the human cost of computing hardware',
            'demand for rechargeable devices drives mining with serious human-rights and environmental impacts far from consumers.'),
           ('Fairphone', 'The Dutch company Fairphone designs modular phones that users can repair, sources some fair-trade and conflict-free minerals and offers long software support.', 'design responses to environmental impact',
            'repairable design extends device life and reduces embodied emissions, though Fairphone remains a small niche in the market.')],
    sources=[('"In 2022, 62 million tonnes of e-waste were produced globally; only 22.3% was documented as formally collected and recycled."', 'Global E-waste Monitor 2024 (ITU and UNITAR)',
              'With reference to the source, explain one implication of these figures.', 'Most e-waste is not formally recycled, so valuable materials are lost and toxic substances may pollute the environment or harm informal recyclers; this suggests the need for better collection, repair and producer responsibility.'),
             ('"The greenest phone is the one you already own."', 'Slogan used by repair campaigners, e.g. Restart Project, UK',
              'Explain the argument in the source.', 'Because most emissions come from manufacturing, keeping and repairing existing devices avoids the embodied carbon and resources of making new ones.')],
    evaluate=[('Manufacturers should be legally responsible for the e-waste their products create.',
               ['extended producer responsibility (EU WEEE Directive) funds collection', 'creates incentives for repairable, recyclable design'],
               ['costs passed to consumers', 'hard to enforce globally and for exports', 'consumers\' replacement habits also matter'],
               'Producer responsibility is an effective tool when combined with right-to-repair laws and consumer awareness.'),
              ('The environmental costs of digital technology outweigh its environmental benefits.',
               ['e-waste, mining and data-centre energy', 'rapidly rising AI electricity demand'],
               ['smart grids, remote working and dematerialisation can cut emissions', 'environmental monitoring by satellites and sensors', 'efficiency gains (PUE improvements)'],
               'Digital technology can support sustainability, but only if its own footprint is managed through renewable energy, longer device lifetimes and recycling.')],
    extended=[('Evaluate one intervention designed to reduce the environmental impact of computing devices.', 'E.g. EU common charger (USB-C, 2024), right-to-repair rules, WEEE producer responsibility, Fairphone, Apple trade-in; analyse effects on e-waste and emissions, stakeholders, limitations; judgement.', 8, 'long')],
))


def _lum(v):
    c = v / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


@R.add('ch10-st3', 'C3', (2, 5), 'numerical')
def contrast_ratio(rng, slot):
    fg = rng.choice([0, 51, 85, 102, 119, 136])
    bg = rng.choice([255, 238, 221, 204])
    L1, L2 = round(_lum(bg), 3), round(_lum(fg), 3)
    ratio = (L1 + 0.05) / (L2 + 0.05)
    ok = ratio >= 4.5
    hexf = '#' + format(fg, '02X') * 3
    hexb = '#' + format(bg, '02X') * 3
    stem = (f'A website uses grey text {hexf} on a background {hexb}. Their relative luminances are {L2:.3f} and {L1:.3f}. '
            f'Using the WCAG formula contrast ratio = (L_lighter + 0.05) ÷ (L_darker + 0.05), calculate the contrast ratio and state whether it meets the WCAG AA minimum of 4.5:1 for normal text.')
    ans = f'{ratio:.2f}:1 – {"meets" if ok else "does not meet"} AA'
    key = f'({L1:.3f} + 0.05) ÷ ({L2:.3f} + 0.05) = {ratio:.2f} [M1 A1]; {"≥" if ok else "<"} 4.5 so it {"meets" if ok else "fails"} AA [A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain who benefits from sufficient contrast.'
        ans += '; people with low vision or colour-vision deficiency, older users, and everyone reading screens in bright sunlight'
        key += ' Beneficiaries: low-vision users, older people, situational limitations (sunlight) – the curb-cut effect [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch10-st3', F(
    terms=[('assistive technology', 'devices or software that help people with disabilities carry out tasks, such as screen readers, switch controls or hearing aids'),
           ('inclusive design', 'designing products and services to be usable by as many people as possible, including people with different abilities, ages and languages'),
           ('screen reader', 'software that converts on-screen text and interface elements into speech or braille, such as JAWS, NVDA or VoiceOver'),
           ('Web Content Accessibility Guidelines (WCAG)', 'international guidelines from the W3C for making web content accessible, organised around four principles: perceivable, operable, understandable and robust'),
           ('alt text', 'a short written description of an image that screen readers read aloud for people who cannot see it'),
           ('curb-cut effect', 'the idea that features designed for disabled people (like dropped kerbs) end up benefiting everyone'),
           ('universal design', 'designing environments and products so that they can be used by everyone without the need for adaptation')],
    facts=[('What are the four principles of WCAG, often remembered as POUR?', 'Perceivable, operable, understandable, robust', ['Private, open, usable, reliable', 'Portable, online, universal, readable', 'Physical, optical, user-friendly, responsive'], 'POUR underlies all WCAG success criteria.'),
           ('What is the WCAG AA minimum contrast ratio for normal-size text?', '4.5:1', ['2:1', '7:1', '10:1'], 'Large text needs 3:1; AAA requires 7:1.'),
           ('Which app connects blind and low-vision people with sighted volunteers through live video?', 'Be My Eyes', ['Duolingo', 'Signal', 'Waze'], 'Launched in Denmark in 2015.'),
           ('Which gaming controller, released by Microsoft in 2018, was designed with and for gamers with limited mobility?', 'The Xbox Adaptive Controller', ['The Kinect', 'The Wii Remote', 'The PlayStation Move'], 'It supports external switches and buttons.')],
    why=[('Explain why inclusive design benefits people without disabilities.', 'Features such as captions, voice control and high contrast help people in noisy places, people learning a language, older users or anyone using a phone in sunlight – the curb-cut effect.'),
         ('Explain why alt text is important for accessibility.', 'Screen-reader users cannot see images; alt text describes the content and purpose of an image so they receive the same information, and it also helps search engines and slow connections.'),
         ('Explain why accessibility is described as a human-rights issue.', 'The UN Convention on the Rights of Persons with Disabilities (2006) requires access to information and communications technology; inaccessible digital services exclude disabled people from education, work and public life.')],
    contrast=[('assistive technology', 'inclusive design', 'Assistive technology is a specific tool used by an individual to overcome a barrier (a screen reader); inclusive design removes barriers in the product itself so fewer adaptations are needed (a website that works with screen readers and keyboards).'),
              ('accessibility', 'usability', 'Accessibility means people with disabilities can perceive, use and understand a product; usability is how easy and efficient a product is for its users in general – accessible design usually improves usability.')],
    misc=[('Accessibility features are only needed by a very small number of people.', 'The WHO estimates about 1.3 billion people (around 16% of the population) experience significant disability, and many more benefit from captions, zoom and voice control.'),
          ('Adding a screen reader to a computer makes every website accessible.', 'Screen readers depend on websites being coded accessibly (alt text, labels, headings); poorly built sites remain unusable even with assistive technology.')],
    cases=[('Be My Eyes', 'Launched in 2015, Be My Eyes connects blind and low-vision users with millions of sighted volunteers through live video; in 2023 it added an AI "Be My AI" assistant based on GPT-4.', 'assistive technology enabling independence',
            'smartphone cameras and networks turned volunteers and AI into on-demand assistance, increasing independence while raising questions about reliability and privacy.'),
           ('the Xbox Adaptive Controller', 'Microsoft designed the 2018 controller with gamers with limited mobility and charities such as AbleGamers; it connects to switches, buttons and joysticks.', 'inclusive design',
            'designing with disabled users from the start produced a mainstream product that widened participation in gaming culture.'),
           ('the Domino\'s Pizza accessibility case (USA)', 'A blind customer, Guillermo Robles, sued Domino\'s because its website and app did not work with his screen reader; in 2019 the US Supreme Court declined to hear Domino\'s appeal, letting the case proceed.', 'legal pressure for digital accessibility',
            'the case signalled that the Americans with Disabilities Act can apply to websites and apps, pushing businesses to follow WCAG.')],
    sources=[('"Nothing about us without us."', 'Slogan of the disability rights movement, popularised by James Charlton (1998)',
              'Explain how this source applies to the design of digital technology.', 'Disabled people should be involved in designing technologies meant for them, because they understand the barriers best; inclusive design should be co-designed rather than imposed.'),
             ('"Solve for one, extend to many."', 'Microsoft Inclusive Design Toolkit (2016)',
              'Explain what the source means, using an example.', 'Designing for a specific disability can benefit many others: e.g. captions designed for deaf users help people in noisy places or learning a language.')],
    evaluate=[('Digital technology has done more to include than exclude people with disabilities.',
               ['screen readers, voice assistants and captions open access to information and work', 'remote work and online services reduce physical barriers'],
               ['many websites still fail basic accessibility (WebAIM finds most home pages have errors)', 'new technologies (CAPTCHAs, touch-only interfaces) create barriers', 'cost of assistive devices'],
               'Digital technology has greatly widened possibilities, but inclusion depends on accessible design being required and enforced.'),
              ('Accessibility should be a legal requirement for all websites.',
               ['ensures equal rights (CRPD)', 'the European Accessibility Act applies from June 2025'],
               ['costs for small businesses', 'enforcement challenges', 'guidelines may be applied as box-ticking'],
               'Legal requirements are justified and effective when supported by guidance and proportionate expectations for small organisations.')],
    extended=[('Evaluate how well one digital service you use meets the needs of people with disabilities, and recommend two improvements.', 'Apply POUR/WCAG (alt text, contrast, keyboard navigation, captions, clear language); evaluate with examples; recommend specific, justified improvements.', 6, 'long')],
))

P2['ch10'] = dict(
    src=[('"About 5.5 billion people – 68% of the world\'s population – are using the internet in 2024. In low-income countries, only 27% of the population is online."', 'ITU, Facts and Figures 2024',
          'Identify two facts about internet use in {S}.', ['68% / 5.5 billion people worldwide use the internet', 'only 27% online in low-income countries'],
          'Explain what {S} suggests about the global digital divide.', 'There is a large gap between global and low-income country usage, so people in poorer countries are much less able to benefit from online education, work and services.'),
         ('"We have 4G on the hill now, but a smartphone costs two months of my wages and data runs out in a week."', 'Farmer in rural Malawi, interviewed for a 2023 study on connectivity',
          'Identify two barriers to internet use described in {S}.', ['cost of a smartphone (two months\' wages)', 'cost of data / data running out quickly'],
          'Explain why {S} suggests coverage alone does not close the digital divide.', 'Network coverage exists (4G on the hill), but affordability of devices and data prevents use; the usage gap is about cost, not only infrastructure.'),
         ('"Every school connected by 2030."', 'Mission of Giga, a joint initiative of UNICEF and the ITU launched in 2019',
          'Identify two features of the intervention suggested in {S}.', ['focus on schools', 'universal target/deadline of 2030'],
          'Explain one reason why connecting schools might reduce the digital divide.', 'Schools are shared access points where young people can gain skills and access to information even if their households cannot afford connections.')],
    cmp=[(0, 1, 'barriers to internet access', ['both show that many people are still not using the internet', 'both relate to low-income contexts'],
          ['Source A gives global statistics; Source B gives one individual\'s experience', 'A emphasises the number offline; B emphasises affordability despite coverage']),
         (1, 2, 'how the digital divide might be closed', ['both concern rural or underserved populations'],
          ['Source B suggests cost is the main barrier; Source C proposes infrastructure/connectivity for schools', 'B is a user perspective; C is an organisational goal'])],
    ev=[(1, 2, 'improving infrastructure is the most effective way to close the digital divide.', ['many people still lack coverage, especially in rural areas', 'school connectivity (Source C) gives shared access'],
         ['coverage exists but devices and data are unaffordable (Source B)', 'skills and relevant content also matter', 'gender norms limit women\'s access']),
        (0, 1, 'the global digital divide is closing quickly.', ['68% now online (Source A)', 'mobile networks expanding'],
         ['only 27% online in low-income countries (Source A)', 'affordability barriers persist (Source B)', 'quality and skills gaps grow even as access spreads'])],
)

INTV['ch10'] = [
    ('Giga, the UNICEF–ITU school connectivity initiative', 'Giga, launched in 2019, maps schools and their connectivity, and works with governments and companies to finance internet connections for schools. It reports having connected thousands of schools and millions of students, but many countries still have large numbers of unconnected schools.',
     'Hundreds of millions of children attend schools without internet access, limiting their access to information and digital skills and widening inequality between and within countries.',
     ['students – access to online learning and skills', 'teachers – new resources but need for training', 'governments – need sustainable funding for ongoing costs', 'telecom providers – new contracts and markets'],
     ['clear target and mapping data', 'schools as community access points', 'combines public and private finance'],
     ['connection alone does not ensure learning', 'ongoing costs (data, maintenance, power)', 'devices and teacher skills may be missing'],
     'Pair connectivity with teacher training, devices and locally relevant content, and measure learning outcomes, not just connections.'),
    ('the EU common charger law', 'From December 2024 the EU requires phones, tablets, cameras, headphones and other small devices sold in the EU to use USB-C charging, with laptops following in 2026, and allows devices to be sold without a charger.',
     'Incompatible chargers created unnecessary e-waste (an estimated 11,000 tonnes a year in the EU from discarded chargers) and cost and inconvenience for consumers.',
     ['consumers – reuse chargers and save money', 'manufacturers such as Apple – had to switch from Lightning ports', 'environment – less charger e-waste', 'accessory makers – standardised market'],
     ['simple, enforceable standard', 'reduces e-waste and consumer costs', 'EU market size influenced global designs (Brussels effect)'],
     ['small share of total e-waste', 'may slow future charging innovation', 'does not address device lifetime or repair'],
     'Combine with right-to-repair rules and longer software-support requirements to tackle the larger share of device e-waste.'),
]

# =============================================================================================
# ch11 Content 3.4 Networks and the internet: structure and types
# =============================================================================================
@R.add('ch11-st1', 'C3', (1, 4), 'numerical')
def bandwidth_share(rng, slot):
    link = rng.choice([50, 100, 200, 500, 1000])
    users = rng.choice([10, 25, 40, 80, 120])
    ctx = rng.choice(['a school LAN', 'a café\'s Wi-Fi network', 'a small office network', 'a library\'s public Wi-Fi'])
    per = link / users
    stem = f'{ctx[0].upper() + ctx[1:]} has a {link} Mbps connection to the internet shared equally by {users} active users. Calculate the bandwidth available to each user'
    if slot.d >= 3:
        hd = rng.choice([3, 5, 8])
        stem += f', and state whether each user can stream HD video needing {hd} Mbps.'
        ans = f'{per:.3g} Mbps each; {"yes" if per >= hd else "no"}'
        key = f'{link} ÷ {users} = {per:.3g} Mbps [M1 A1]; {"≥" if per >= hd else "<"} {hd} Mbps, so {"yes" if per >= hd else "no"} [A1].'
        m = 3
    else:
        stem += '.'
        ans = f'{per:.3g} Mbps'
        key = f'{link} ÷ {users} = {per:.3g} Mbps [M1 A1].'
        m = 2
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch11-st1', F(
    terms=[('network', 'two or more devices connected so that they can share data and resources'),
           ('local area network (LAN)', 'a network covering a small geographical area, such as a home, school or office'),
           ('wide area network (WAN)', 'a network covering a large geographical area, connecting LANs across cities or countries; the internet is the largest WAN'),
           ('router', 'a device that forwards data packets between networks, choosing a path towards the destination'),
           ('server', 'a computer that provides services or resources (web pages, files, email) to other computers called clients'),
           ('cloud computing', 'delivering computing services – storage, processing, software – over the internet on demand from remote data centres'),
           ('client–server model', 'a network model in which clients request services and central servers provide them'),
           ('peer-to-peer (P2P) network', 'a network in which devices share resources directly with each other without a central server')],
    facts=[('Which device connects a home network to the internet and forwards packets between them?', 'A router', ['A monitor', 'A keyboard', 'A printer'], 'Home routers often combine a modem, switch and Wi-Fi access point.'),
           ('Which of the following is an example of a peer-to-peer network?', 'BitTorrent file sharing', ['Netflix streaming from data centres', 'A school\'s email server', 'Google Search'], 'In BitTorrent, users\' computers share file pieces directly.'),
           ('Approximately what share of intercontinental internet traffic is carried by undersea cables?', 'About 99%', ['About 10%', 'About 50%', 'About 1%'], 'Satellites carry only a small share; cables carry almost all.'),
           ('What type of network is the internet?', 'A global network of networks (WAN)', ['A single LAN owned by one company', 'A peer-to-peer network of phones only', 'A network of satellites only'], 'The internet interconnects tens of thousands of autonomous networks.')],
    why=[('Explain why most large online services use data centres rather than peer-to-peer networks.', 'Central servers in data centres let companies control content, security, updates and reliability, scale capacity and collect data; P2P is harder to control and monetise.'),
         ('Explain why undersea cables are critical infrastructure.', 'Almost all international internet traffic passes through a few hundred undersea cables; damage (e.g. the 2022 Tonga cable break, 2024 Red Sea cable cuts) can disconnect countries or slow traffic, and they are a geopolitical concern.'),
         ('Explain why cloud computing has changed how organisations use networks.', 'Instead of running their own servers, organisations rent computing over the internet; this makes them dependent on reliable, fast network connections and on a few large cloud providers.')],
    contrast=[('a LAN', 'a WAN', 'A LAN covers a small area (a school) and is usually owned by one organisation; a WAN covers large areas (countries) and connects many LANs, often using leased or public infrastructure.'),
              ('the client–server model', 'peer-to-peer networking', 'In client–server networks, central servers provide services to clients (e.g. a website); in P2P networks, devices share resources directly with each other (e.g. BitTorrent), with no central server.')],
    misc=[('The internet and the World Wide Web are the same thing.', 'The internet is the global network infrastructure; the Web is a service that runs on it (web pages linked by HTTP), alongside others such as email and messaging.'),
          ('Most international internet traffic travels by satellite.', 'About 99% of intercontinental traffic travels through undersea fibre-optic cables; satellites carry a small share, though services like Starlink are growing.')],
    cases=[('the 2022 Tonga cable break', 'The Hunga Tonga–Hunga Haʻapai volcanic eruption in January 2022 cut Tonga\'s single international undersea cable, leaving the country largely offline for about five weeks.', 'dependence on network infrastructure',
            'a single physical link meant one event disconnected a whole country, showing the vulnerability of networks without redundancy.'),
           ('2Africa undersea cable', 'Meta and telecom partners built 2Africa, one of the longest subsea cable systems, around Africa and to Europe and the Middle East.', 'who owns internet infrastructure',
            'private technology companies increasingly own the core infrastructure of the internet, giving them influence over connectivity.'),
           ('the AWS outage of December 2021', 'An outage in Amazon Web Services\' US-East-1 region disrupted services such as Disney+, Ring doorbells and delivery apps.', 'interdependence in cloud networks',
            'many services relied on the same cloud region, so a failure in one provider affected millions of users across many companies.')],
    sources=[('"If the cables are cut, a country can lose its connection to the world overnight."', 'Telecommunications analyst, BBC interview after the 2022 Tonga eruption',
              'Explain what the source suggests about the internet as a physical system.', 'The internet depends on physical infrastructure such as undersea cables; when these are damaged, connectivity is lost, so the "virtual" internet is vulnerable to physical events.'),
             ('"The internet is not a big truck. It\'s a series of tubes."', 'US Senator Ted Stevens, Senate speech on net neutrality, 2006 (widely mocked)',
              'Explain why the source is both mocked and partly accurate.', 'It was mocked as a simplistic description, but it partly captures that the internet consists of physical links with limited capacity that can become congested.')],
    evaluate=[('Cloud computing has made organisations more resilient.',
               ['redundant data centres and professional security', 'scales instantly to demand'],
               ['concentration on a few providers creates single points of failure (AWS 2021, CrowdStrike 2024)', 'dependence on network connectivity', 'vendor lock-in'],
               'The cloud improves resilience for many individual organisations but concentrates systemic risk in a few providers.'),
              ('Private companies should not own the core infrastructure of the internet.',
               ['risk of control and prioritisation of their own services', 'public interest in universal access'],
               ['private investment funds expensive cables quickly', 'states can regulate private owners', 'state ownership can enable censorship'],
               'Mixed ownership with strong regulation and open-access rules is more realistic than excluding private firms.')],
    extended=[('Describe the main components involved when a student in a school LAN loads a video from a streaming service, and evaluate one point where the system is vulnerable.', 'Device → Wi-Fi/switch → router → ISP → internet backbone/undersea cables → CDN/data-centre servers; vulnerabilities: bandwidth congestion, ISP outage, cloud provider outage, cable cuts; judgement.', 6, 'long')],
))


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def packets(rng, slot):
    kind = rng.choice(['packets', 'latency', 'ip'])
    if kind == 'packets':
        size_kb = rng.choice([30, 150, 500, 1200, 4500])
        payload = rng.choice([1000, 1400, 1460])
        n = math.ceil(size_kb * 1000 / payload)
        stem = f'A {size_kb} kB file (1 kB = 1000 bytes) is sent over the internet in packets that each carry {payload} bytes of data. Calculate the number of packets needed.'
        ans = f'{n:,} packets'
        key = f'{size_kb * 1000:,} ÷ {payload} = {size_kb * 1000 / payload:.2f} → round up to {n:,} packets [M1 A1].'
        m = 2
        if slot.d >= 3:
            stem += ' Explain why the packets may arrive in a different order and how TCP deals with this.'
            ans += '; packets may take different routes (packet switching); TCP uses sequence numbers to reorder and requests resending of missing packets'
            key += ' Different routes through routers [R1]; TCP sequence numbers/acknowledgements reassemble and resend [R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    if kind == 'latency':
        route = rng.choice([('London', 'New York', 5600), ('Singapore', 'Sydney', 6300), ('Mumbai', 'Marseille', 7000),
                            ('Lisbon', 'Fortaleza', 5600), ('Tokyo', 'Los Angeles', 8800)])
        a, b, km = route
        ms = km / 200000 * 1000
        stem = (f'A fibre-optic cable route from {a} to {b} is about {km:,} km long. Light travels through optical fibre at about 200,000 km/s. '
                f'Calculate the minimum one-way delay in milliseconds and the round-trip time.')
        ans = f'{ms:.0f} ms one way; {2 * ms:.0f} ms round trip'
        key = f'{km:,} ÷ 200,000 = {km / 200000:.3f} s = {ms:.0f} ms [M1 A1]; × 2 = {2 * ms:.0f} ms [A1].'
        m = 3
        if slot.d >= 4:
            stem += ' Explain why actual delays are usually longer.'
            ans += '; routes are not straight, and routers add queuing and processing delays'
            key += ' Cable routes are longer than straight lines; router processing/queuing; congestion [R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    octs = [rng.randint(1, 223), rng.randint(0, 255), rng.randint(0, 255), rng.randint(1, 254)]
    ip = '.'.join(map(str, octs))
    i = rng.randrange(4)
    stem = f'The IPv4 address {ip} is made of four 8-bit numbers. Convert the number {octs[i]} (part {i + 1}) into binary, and state how many bits an IPv4 address has in total and how many addresses this allows.'
    return dict(stem=stem, answer=f'{to_bin(octs[i])}; 32 bits; 2^32 ≈ 4.3 billion addresses', type='numerical', marks=3,
                markingKey=f'{octs[i]} = {to_bin(octs[i])} [A1]; 4 × 8 = 32 bits [A1]; 2^32 = 4,294,967,296 ≈ 4.3 billion [A1] (IPv6 uses 128 bits).')


R.facts('ch11-st2', F(
    terms=[('packet switching', 'sending data broken into small packets that travel independently across the network, possibly by different routes, and are reassembled at the destination'),
           ('protocol', 'an agreed set of rules for how data is formatted, sent and received across a network'),
           ('TCP/IP', 'the core suite of internet protocols: IP addresses and routes packets; TCP ensures reliable, ordered delivery'),
           ('IP address', 'a numerical label that identifies a device on a network so that packets can be routed to it'),
           ('HTTP/HTTPS', 'the protocol used to request and transfer web pages; HTTPS encrypts this communication using TLS'),
           ('Domain Name System (DNS)', 'the internet\'s directory that translates domain names (e.g. ibo.org) into IP addresses'),
           ('IPv6', 'the newer version of the Internet Protocol that uses 128-bit addresses, allowing about 3.4 × 10³⁸ addresses')],
    facts=[('How many bits are in an IPv4 address?', '32', ['8', '64', '128'], 'IPv4 = 32 bits (~4.3 billion addresses); IPv6 = 128 bits.'),
           ('On which date did ARPANET officially switch to TCP/IP, often called the birth of the internet?', '1 January 1983', ['29 October 1969', '6 August 1991', '1 January 2000'], 'The "flag day" migration from NCP to TCP/IP.'),
           ('Which system translates domain names into IP addresses?', 'DNS', ['HTTP', 'HTML', 'FTP'], 'DNS works like a phone book for the internet.'),
           ('What does the "S" in HTTPS indicate?', 'The connection is encrypted (secure) using TLS', ['The site is government-approved', 'The site is fast', 'The site uses static pages'], 'HTTPS protects data in transit from eavesdropping and tampering.')],
    why=[('Explain why the internet uses packet switching rather than dedicated circuits.', 'Packets from many users share the same links, using capacity efficiently; if a route fails, packets can be re-routed, making the network resilient – a design goal of ARPANET.'),
         ('Explain why IPv6 was introduced.', 'IPv4\'s 32-bit addresses allow only about 4.3 billion addresses, which ran out as billions of phones and IoT devices came online; IPv6\'s 128-bit addresses provide a practically unlimited number.'),
         ('Explain why open, shared protocols were important for the growth of the internet.', 'Because TCP/IP and HTTP are open standards, any manufacturer or developer can build compatible devices and services without permission, allowing the internet to grow rapidly and globally.')],
    contrast=[('TCP', 'IP', 'IP is responsible for addressing and routing each packet to the destination; TCP manages the connection, splitting data into packets, numbering them, checking delivery and resending lost packets.'),
              ('HTTP', 'HTTPS', 'HTTP sends web data in plain text that can be intercepted; HTTPS encrypts it with TLS, protecting confidentiality and integrity.')],
    misc=[('An IP address always identifies one specific person.', 'An IP address identifies a network connection or device, which may be shared (households, NAT, public Wi-Fi) or change over time; linking it to a person needs other data.'),
          ('HTTPS means a website is trustworthy.', 'HTTPS only means the connection is encrypted; phishing sites can also use HTTPS, so the padlock does not prove the site is legitimate.')],
    cases=[('the Facebook outage of October 2021', 'On 4 October 2021 a faulty configuration change to Facebook\'s BGP routing withdrew routes to its DNS servers, taking Facebook, Instagram and WhatsApp offline for about six hours.', 'protocols and routing',
            'when routing announcements disappeared, the rest of the internet could not find Facebook\'s servers, showing how services depend on protocols working correctly.'),
           ('the adoption of HTTPS', 'After the Snowden revelations (2013) and campaigns such as Let\'s Encrypt (free certificates from 2015), most web traffic shifted to HTTPS.', 'protocols as responses to surveillance',
            'encrypting web traffic by default protected users from interception, showing protocols evolve in response to social concerns.'),
           ('IPv4 exhaustion', 'The pool of unallocated IPv4 addresses held by IANA was exhausted in 2011, and regional registries later ran out; IPv4 addresses are now traded.', 'technical limits shaping access',
            'scarcity raised costs for new networks, particularly in regions that joined the internet later, while IPv6 adoption remains incomplete.')],
    sources=[('"We reject: kings, presidents and voting. We believe in: rough consensus and running code."', 'David Clark, Internet Engineering Task Force (IETF), 1992',
              'Explain what the source suggests about how internet protocols are developed.', 'Protocols are developed through open, technical consensus among engineers and working implementations, not by governments or votes – a multi-stakeholder, bottom-up process.'),
             ('"Be conservative in what you do, be liberal in what you accept from others."', 'Jon Postel\'s robustness principle, RFC 761 (1980)',
              'Explain how this principle helped the internet grow.', 'Systems that tolerate small variations in others\' messages while sending strictly correct ones can interoperate despite differences, enabling diverse networks to connect.')],
    evaluate=[('The open design of internet protocols is its greatest strength.',
               ['anyone can build services without permission (innovation)', 'resilient, decentralised routing'],
               ['early protocols lacked security (spam, spoofing, BGP hijacks)', 'openness enables abuse and surveillance', 'large platforms now centralise much of the internet anyway'],
               'Openness enabled the internet\'s growth and remains vital, but security had to be added later and centralisation now limits the benefits.'),
              ('Everyone needs to understand how the internet works to be a responsible digital citizen.',
               ['understanding HTTPS, IP addresses and DNS helps avoid scams and protect privacy', 'informs debates on governance and net neutrality'],
               ['most users rely on well-designed defaults', 'responsibility for security lies with providers', 'basic awareness may be enough'],
               'A basic understanding is valuable for safety and civic debate, but secure-by-default design matters more than individual expertise.')],
    extended=[('Explain, step by step, what happens when a user types a web address into a browser, and evaluate one point at which their privacy could be compromised.', 'DNS lookup → IP address; TCP connection; TLS handshake (HTTPS); HTTP request; server response in packets; routers; reassembly; privacy points: DNS queries visible to ISP, metadata, unencrypted HTTP, tracking cookies; judgement.', 6, 'long')],
))


@R.add('ch11-st3', 'C3', (1, 4), 'numerical')
def iot_count(rng, slot):
    b = rng.choice([8, 10, 12, 15])
    g = rng.choice([10, 12, 15, 18, 20])
    n = rng.choice([3, 4, 5, 6])
    y = rng.choice([2020, 2022, 2023])
    v = b * (1 + g / 100) ** n
    stem = f'An estimated {b} billion IoT devices were connected in {y}. If the number grows by {g}% a year, estimate the number connected in {y + n}.'
    ans = f'about {v:.3g} billion'
    key = f'{b} × {1 + g / 100:g}^{n} [M1] = {v:.3g} billion [A1].'
    m = 2
    if slot.d >= 3:
        stem += ' Explain one security risk created by this growth.'
        ans += '; many devices have weak default passwords and are rarely updated, so they can be hijacked into botnets (e.g. Mirai, 2016)'
        key += ' Weak defaults/no updates → botnets such as Mirai (2016 Dyn DDoS) [R1 R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch11-st3', F(
    terms=[('World Wide Web', 'a system of interlinked documents and resources (web pages) accessed over the internet using browsers and HTTP, invented by Tim Berners-Lee at CERN in 1989'),
           ('hyperlink', 'a clickable reference that takes the user from one web resource to another'),
           ('search engine', 'a system that crawls and indexes web pages and ranks them in response to user queries'),
           ('web crawler', 'a program that automatically visits web pages and follows links to collect content for a search engine\'s index'),
           ('Internet of Things (IoT)', 'the network of everyday physical objects (thermostats, cars, watches, sensors) that are connected to the internet and exchange data'),
           ('smart city', 'a city that uses networked sensors and data to manage services such as traffic, energy and waste'),
           ('botnet', 'a network of compromised devices controlled remotely, often used for spam or distributed denial-of-service attacks')],
    facts=[('Who proposed the World Wide Web in 1989 while working at CERN?', 'Tim Berners-Lee', ['Vint Cerf', 'Larry Page', 'Bill Gates'], 'His proposal "Information Management: A Proposal" led to the first website in 1991.'),
           ('Which 2016 botnet used hacked IoT devices such as cameras and routers to attack the DNS provider Dyn?', 'Mirai', ['Stuxnet', 'WannaCry', 'Conficker'], 'The attack disrupted sites such as Twitter, Netflix and Reddit.'),
           ('Which search engine had about 90% of the global search market in the mid-2020s?', 'Google', ['Bing', 'Baidu', 'DuckDuckGo'], 'StatCounter estimates around 90%.'),
           ('Which of the following is an IoT device?', 'A smart thermostat that can be controlled from a phone', ['A printed map', 'A mechanical wristwatch', 'A paper ticket'], 'It is a physical object connected to the internet.')],
    why=[('Explain why search engines have significant influence over what people know.', 'Most users click only the top results, so a search engine\'s ranking decides which information is seen; dominance by one engine (Google ~90%) concentrates this gatekeeping power.'),
         ('Explain why IoT devices are often less secure than computers.', 'They are cheap, sold with default passwords, rarely updated, have limited processing power for security and are often left unattended, making them easy targets for hackers (e.g. Mirai).'),
         ('Explain why the Web was designed to be open and free.', 'Berners-Lee and CERN released the Web\'s technology royalty-free in 1993 so anyone could publish and build on it, which enabled its rapid global growth.')],
    contrast=[('the World Wide Web', 'the Internet of Things', 'The Web is a system of linked documents and applications accessed by people through browsers; the IoT is a network of physical objects with sensors that exchange data, often without human interaction.'),
              ('a search engine index', 'the whole web', 'An index is the search engine\'s database of pages its crawlers have found and processed; much of the web (private, dynamic or blocked pages – the "deep web") is not indexed.')],
    misc=[('Search engines show the same results to everyone.', 'Results are personalised by location, language, search history and device, and change over time.'),
          ('IoT devices only collect data that users choose to share.', 'Many IoT devices continuously collect data (voice assistants listening for wake words, smart TVs tracking viewing via ACR) and send it to manufacturers, often by default.')],
    cases=[('the Mirai botnet attack (2016)', 'In October 2016 the Mirai botnet, made of hacked IoT cameras and routers with default passwords, launched a massive DDoS attack on DNS provider Dyn, disrupting major websites in the US and Europe.', 'security risks of the Internet of Things',
            'insecure everyday devices became weapons, showing that the security of the whole network depends on its weakest connected things.'),
           ('Songdo, South Korea', 'Songdo was planned as a smart city with sensors monitoring traffic, energy and waste, including pneumatic waste collection.', 'the smart city and IoT',
            'networked sensors improve efficiency, but critics note that the city has been slow to attract residents and that pervasive data collection raises privacy questions.'),
           ('Google\'s dominance in search', 'In August 2024 a US federal court ruled that Google illegally maintained a monopoly in search, partly through paying to be the default search engine on devices and browsers.', 'search engines and power',
            'control of the main gateway to web information gives one company power over what billions of people find and over online advertising markets.')],
    sources=[('"This is for everyone."', 'Tweet by Tim Berners-Lee displayed during the London 2012 Olympics opening ceremony',
              'Explain what the source suggests about the values behind the World Wide Web.', 'The Web was intended to be open and accessible to everyone, free of royalties and gatekeepers – a public resource rather than a private product.'),
             ('"The S in IoT stands for security."', 'Joke widely shared by security researchers',
              'Explain the point made by the source.', 'There is no "S" in IoT – the joke implies that security is missing from many IoT devices, which ship with weak defaults and little protection.')],
    evaluate=[('The benefits of the Internet of Things outweigh its risks.',
               ['efficiency in energy, transport and health (smart meters, remote monitoring)', 'convenience and accessibility for disabled and elderly users'],
               ['security weaknesses (Mirai botnet)', 'continuous data collection and surveillance', 'e-waste from short-lived devices'],
               'Benefits can outweigh risks if devices are secure by design (e.g. the UK PSTI Act 2024 banning default passwords) and data is minimised.'),
              ('One search engine dominating the market is harmful to society.',
               ['gatekeeping over information and advertising', 'less incentive to innovate or protect privacy', 'court ruled Google maintained monopoly illegally (2024)'],
               ['dominance may reflect quality and network effects', 'free service to users', 'alternatives exist and AI chatbots challenge search'],
               'Dominance concentrates information power and is harmful without regulation, even if the service is valued by users.')],
    extended=[('Analyse how the Internet of Things is used in one smart-city project and evaluate its impact on residents.', 'E.g. Songdo, Barcelona, Singapore Smart Nation, Toronto Quayside (cancelled 2020 after privacy concerns); analyse sensors, data, services; evaluate efficiency vs privacy, participation, cost; judgement.', 6, 'long')],
))

# =============================================================================================
# ch12 Content 3.4 Networks and the internet: governance, security and social impact
# =============================================================================================
@R.add('ch12-st1', 'C3', (2, 5), 'numerical')
def shutdown_cost(rng, slot):
    gdp = rng.choice([40, 90, 250, 450, 1200, 3500])  # US$ billion per year
    share = rng.choice([3, 5, 6, 8, 10])
    hours = rng.choice([12, 24, 72, 120, 240, 720])
    region = rng.choice(['a country', 'a state', 'a region'])
    daily = gdp * 1e9 * share / 100 / 365
    cost = daily * hours / 24
    stem = (f'The government of {region} with an annual GDP of US${gdp} billion orders a complete internet shutdown lasting {hours} hours. '
            f'Assume the digital economy contributes {share}% of GDP and is entirely stopped by the shutdown. Estimate the economic cost in US$ millions.')
    ans = f'about US${cost / 1e6:,.1f} million'
    key = f'Digital economy per day = {gdp} bn × {share}% ÷ 365 = US${daily / 1e6:,.1f} m [M1]; × {hours}/24 days = US${cost / 1e6:,.1f} m [M1 A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain one cost of the shutdown that this estimate does not include.'
        ans += '; e.g. lost access to health information and emergency services, education, freedom of expression and press reporting, long-term investor confidence'
        key += ' Non-economic/human-rights costs or longer-term effects identified and explained [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch12-st1', F(
    terms=[('internet governance', 'the development and application of shared principles, rules and decision-making processes that shape how the internet is run and used'),
           ('ICANN', 'the Internet Corporation for Assigned Names and Numbers, a non-profit (founded 1998) that coordinates domain names and IP address allocation through a multi-stakeholder model'),
           ('multi-stakeholder model', 'governance in which governments, companies, technical experts and civil society all participate in decision-making'),
           ('net neutrality', 'the principle that internet service providers should treat all data equally, without blocking, throttling or charging for priority based on content, source or user'),
           ('zero-rating', 'when a mobile operator does not count data used by certain apps against a user\'s data allowance, such as Facebook\'s Free Basics'),
           ('internet shutdown', 'an intentional disruption of internet or mobile data access by a government, for a population or region'),
           ('splinternet', 'the fragmentation of the global internet into national or regional networks with different rules and content')],
    facts=[('Which country recorded the most internet shutdowns in the world for several years, according to Access Now\'s #KeepItOn reports?', 'India', ['Canada', 'Japan', 'Germany'], 'Many were regional shutdowns, e.g. in Jammu and Kashmir.'),
           ('In 2016 India\'s telecom regulator TRAI effectively banned which service on net-neutrality grounds?', 'Facebook\'s Free Basics (differential pricing)', ['WhatsApp calling', 'Google Search', 'Netflix'], 'TRAI\'s 2016 regulation prohibited discriminatory tariffs based on content.'),
           ('In 2016, the US government ended its oversight role over which internet function?', 'The IANA functions (managed by ICANN)', ['The World Wide Web Consortium', 'Undersea cable licensing', 'Google\'s search index'], 'The IANA stewardship transition moved oversight to the global multi-stakeholder community.'),
           ('In Anuradha Bhasin v Union of India (2020), what did the Supreme Court of India hold about internet restrictions in Jammu and Kashmir?', 'Indefinite suspensions are not permissible and restrictions must be necessary and proportionate', ['Shutdowns are always unconstitutional', 'The courts cannot review shutdowns', 'Internet access is not related to free expression'], 'It recognised that free expression via the internet is constitutionally protected.')],
    why=[('Explain why governments order internet shutdowns.', 'They claim shutdowns prevent violence, the spread of rumours, exam cheating or unrest; critics argue they are used to suppress protests and reporting, and they cut off communication for everyone.'),
         ('Explain why net neutrality matters for innovation and fairness.', 'If ISPs could charge for priority or block services, large firms could pay for fast lanes while start-ups and non-profits were slowed, and ISPs could favour their own services, reducing competition and access to information.'),
         ('Explain why the multi-stakeholder model is used for internet governance.', 'The internet is run by many actors across borders – engineers, companies, governments, users – so decisions about domains and standards need technical expertise and broad legitimacy rather than control by one state.')],
    contrast=[('the multi-stakeholder model', 'the multilateral (state-led) model', 'The multi-stakeholder model includes companies, technical bodies and civil society alongside governments (e.g. ICANN); the multilateral model gives states the main decision-making role, as some governments propose through the UN\'s ITU.'),
              ('a full internet shutdown', 'throttling', 'A full shutdown cuts off internet access entirely in an area; throttling slows connections or specific services, making them nearly unusable while appearing to remain on.')],
    misc=[('Nobody controls the internet.', 'No single body controls it, but ICANN coordinates names and numbers, ISPs and states control access, standards bodies set protocols and large platforms control most traffic – power is distributed but real.'),
          ('Internet shutdowns only affect social media.', 'Shutdowns cut off banking, health information, emergency communication, education and businesses for everyone in the area.')],
    cases=[('the internet shutdown in Jammu and Kashmir (2019–2021)', 'After India revoked Article 370 in August 2019, internet access in Jammu and Kashmir was suspended; 2G mobile data was partly restored in 2020 but 4G was only restored in February 2021.', 'state control of networks',
            'a prolonged shutdown cut off education, business and health services for millions, prompting the Supreme Court\'s Anuradha Bhasin ruling on proportionality.'),
           ('Free Basics in India', 'Facebook\'s Free Basics offered free access to a limited set of websites; after a public campaign, TRAI banned differential data pricing in February 2016.', 'net neutrality',
            'critics argued a "free" but curated internet would let Facebook act as gatekeeper for new users, so India chose neutrality over zero-rating.'),
           ("Iran's National Information Network", 'Iran has built a domestic network that allows local services to keep running while international access is cut, as during the November 2019 fuel-price protests.', 'the splinternet',
            'a national intranet lets the state cut off global communication with less economic damage, fragmenting the internet along borders.')],
    sources=[('"Shutdowns don\'t stop violence; they stop people from calling an ambulance, from reporting abuse, from knowing if their families are safe."', 'Spokesperson for Access Now, #KeepItOn campaign, 2023',
              'With reference to the source, explain two impacts of internet shutdowns on people.', 'People cannot contact emergency services (health/safety impact) and cannot report abuses or check on family (human-rights and social impacts).'),
             ('"The internet treats censorship as damage and routes around it."', 'John Gilmore, co-founder of the Electronic Frontier Foundation, 1993',
              'Explain one way in which this source is still accurate and one way it is not.', 'Accurate: VPNs, Tor and mirrors let users bypass some blocks. Not accurate: states now control infrastructure – full shutdowns, national firewalls and deep packet inspection (China, Iran) are hard to route around.')],
    evaluate=[('Internet shutdowns are never justified.',
               ['they violate free expression and access to information (UN Human Rights Council)', 'large economic costs', 'evidence that they reduce violence is weak'],
               ['governments argue short, local shutdowns can stop incitement during riots', 'some cite exam cheating or emergencies'],
               'Shutdowns are almost never proportionate because they affect everyone; targeted, lawful measures against specific content are less harmful alternatives.'),
              ('Net neutrality should be protected by law.',
               ['protects start-ups and free expression', 'prevents ISPs favouring their own content'],
               ['ISPs argue it discourages network investment', 'zero-rating can give poor users free access', 'traffic management is technically necessary'],
               'Legal protection is justified to keep the internet open, with clear exceptions for reasonable traffic management.')],
    extended=[('Compare how two countries govern internet access and evaluate the impacts on their citizens.', 'E.g. China (Great Firewall, real-name rules), India (shutdowns, TRAI neutrality), EU (DSA, net neutrality regulation 2015), US (Section 230, shifting neutrality rules); compare and evaluate rights, economy, security.', 8, 'long')],
))


def caesar(s, k):
    out = []
    for ch in s:
        if ch.isalpha():
            out.append(chr((ord(ch) - 65 + k) % 26 + 65))
        else:
            out.append(ch)
    return ''.join(out)


@R.add('ch12-st2', 'C3', (1, 5), 'numerical')
def security_calc(rng, slot):
    kind = rng.choice(['brute', 'caesar', 'phish'])
    if kind == 'brute':
        cs = rng.choice([(10, 'digits only'), (26, 'lower-case letters only'), (62, 'upper- and lower-case letters and digits'), (94, 'all printable keyboard characters')])
        L = rng.choice([4, 6, 8, 10, 12])
        rate = rng.choice([1e6, 1e9, 1e10])
        comb = cs[0] ** L
        secs = comb / rate
        def human(t):
            for u, d in [('years', 3.156e7), ('days', 86400), ('hours', 3600), ('minutes', 60)]:
                if t >= d:
                    return f'{sci(t / d)} {u}'
            return f'{sci(t)} seconds'
        rs = {1e6: '10⁶', 1e9: '10⁹', 1e10: '10¹⁰'}[rate]
        stem = f'A password has {L} characters chosen from {cs[1]} ({cs[0]} possible characters). Calculate the number of possible passwords and the worst-case time to try them all at {rs} guesses per second.'
        ans = f'{cs[0]}^{L} = {sci(comb)}; about {human(secs)}'
        key = f'{cs[0]}^{L} = {sci(comb)} combinations [M1 A1]; ÷ {rs} = {sci(secs)} s ≈ {human(secs)} [A1].'
        m = 3
        if slot.d >= 4:
            stem += ' Explain why length increases security more than adding character types.'
            ans += '; each extra character multiplies the combinations by the character-set size, so length grows the search space exponentially'
            key += ' Combinations = charset^length, so length is the exponent [R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    if kind == 'caesar':
        word = rng.choice(['DATA', 'PRIVACY', 'NETWORK', 'SECURE', 'PHISHING', 'ROUTER', 'CONSENT'])
        k = rng.randint(2, 9)
        enc = caesar(word, k)
        if rng.random() < 0.5:
            stem = f'Using a Caesar cipher with a shift of {k} to the right, encrypt the word {word}.'
            ans = enc
        else:
            stem = f'The message {enc} was encrypted with a Caesar cipher using a shift of {k} to the right. Decrypt it.'
            ans = word
        m = 2
        key = f'Shift each letter {k} places ({word} ↔ {enc}) [A1 A1].'
        if slot.d >= 3:
            stem += ' Explain why a Caesar cipher is not secure.'
            ans += '; only 25 possible shifts, so it can be broken by trying them all (brute force) or by frequency analysis'
            key += ' Only 25 keys/brute force, letter-frequency patterns preserved [R1 R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    sent = rng.choice([500, 1200, 2500, 4000])
    clk = rng.choice([8, 12, 18, 25])
    cred = rng.choice([25, 40, 50])
    org = rng.choice(['a university', 'a hospital trust', 'a city council', 'a retail company'])
    c1 = sent * clk / 100
    c2 = c1 * cred / 100
    stem = (f'A simulated phishing test at {org} sends {sent:,} emails. {clk}% of recipients click the link, and {cred}% of those who click enter their password. '
            f'Calculate how many people entered their password.')
    ans = f'{c2:g} people'
    key = f'{clk}% × {sent:,} = {c1:g} clicked [M1]; {cred}% × {c1:g} = {c2:g} [A1].'
    m = 2
    if slot.d >= 3:
        stem += ' Suggest two measures, one technical and one human, to reduce the harm.'
        ans += '; e.g. multi-factor authentication / email filtering; staff awareness training and reporting procedures'
        key += ' Technical (MFA, filtering, link scanning) [R1]; human (training, reporting culture) [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch12-st2', F(
    terms=[('malware', 'malicious software such as viruses, worms, trojans, spyware and ransomware designed to damage systems or steal data'),
           ('ransomware', 'malware that encrypts a victim\'s files or systems and demands payment for the key'),
           ('phishing', 'fraudulent messages that trick people into revealing passwords or financial details or installing malware, often by impersonating a trusted organisation'),
           ('social engineering', 'manipulating people psychologically to bypass security, for example by pretending to be IT support'),
           ('multi-factor authentication (MFA)', 'verifying identity with two or more types of evidence – something you know, have or are'),
           ('distributed denial-of-service (DDoS) attack', 'overwhelming a server or network with traffic from many compromised devices so that it becomes unavailable'),
           ('encryption', 'converting data into a form that cannot be read without the correct key'),
           ('zero-day vulnerability', 'a software flaw unknown to the vendor, so no fix exists when attackers exploit it')],
    facts=[('Which 2017 ransomware attack disrupted the UK\'s National Health Service and computers in about 150 countries?', 'WannaCry', ['Mirai', 'Stuxnet', 'ILOVEYOU'], 'It spread using the EternalBlue exploit against unpatched Windows systems.'),
           ('Which US fuel pipeline was shut down by a ransomware attack in May 2021?', 'Colonial Pipeline', ['Keystone XL', 'Nord Stream', 'Trans-Alaska Pipeline'], 'The company paid about US$4.4 million in bitcoin; part was later recovered.'),
           ('Which of the following is an example of multi-factor authentication?', 'A password plus a code from an authenticator app', ['Two different passwords', 'A longer password', 'A security question and a password'], 'MFA requires different factor types (know + have).'),
           ('Which computer worm, discovered in 2010, damaged centrifuges at Iran\'s Natanz nuclear facility?', 'Stuxnet', ['WannaCry', 'NotPetya', 'Code Red'], 'Widely attributed to the US and Israel.')],
    why=[('Explain why humans are often described as the weakest link in cybersecurity.', 'Attackers exploit trust, urgency and curiosity through phishing and social engineering; one person clicking a link or reusing a password can bypass technical defences.'),
         ('Explain why ransomware attacks on hospitals are especially serious.', 'Hospitals depend on digital records and devices; encrypting them delays treatment and can endanger lives, which pressures hospitals to pay and makes them attractive targets.'),
         ('Explain why keeping software updated improves security.', 'Updates patch known vulnerabilities; WannaCry spread mainly through computers that had not installed a Microsoft patch released two months earlier.')],
    contrast=[('a virus', 'a worm', 'A virus attaches to a file or program and spreads when that file is run; a worm is standalone and spreads automatically across networks without user action (e.g. WannaCry).'),
              ('phishing', 'spear phishing', 'Phishing sends generic fraudulent messages to many people; spear phishing targets specific individuals with personalised messages using information about them.')],
    misc=[('Antivirus software makes a computer completely safe.', 'Antivirus cannot detect all threats (zero-days, phishing, social engineering); layered defences – updates, MFA, backups, user awareness – are needed.'),
          ('Only large companies are targeted by cyberattacks.', 'Small businesses, schools, hospitals and individuals are frequent targets because they often have weaker defences; automated attacks hit anyone vulnerable.')],
    cases=[('WannaCry (May 2017)', 'WannaCry ransomware spread across about 150 countries using a leaked NSA exploit (EternalBlue); in the UK NHS it disrupted many hospitals and GP practices, forcing thousands of appointments to be cancelled.', 'cybersecurity threats to critical services',
            'unpatched systems in a public service allowed a single worm to disrupt healthcare, showing the human consequences of security weaknesses.'),
           ('the Colonial Pipeline attack (2021)', 'A ransomware attack by the DarkSide group led Colonial Pipeline to shut down a major US fuel pipeline for several days, causing fuel shortages on the East Coast; attackers entered through a compromised password without MFA.', 'the importance of basic security measures',
            'a single leaked password without MFA led to the disruption of national fuel supply, showing how weak authentication creates systemic risk.'),
           ('Stuxnet (2010)', 'Stuxnet, a sophisticated worm widely attributed to the US and Israel, targeted industrial control systems and damaged centrifuges at Iran\'s Natanz facility.', 'cyber operations by states',
            'a digital weapon caused physical damage, opening a new era of state cyber conflict.')],
    sources=[('"Amateurs hack systems; professionals hack people."', 'Bruce Schneier, security technologist, 2000',
              'Explain what the source suggests about cybersecurity.', 'Skilled attackers target human behaviour (phishing, social engineering) because people are easier to manipulate than well-designed systems, so security must address people as well as technology.'),
             ('"The attackers got in using a single compromised password for a VPN account that did not have multi-factor authentication."', 'Testimony of Colonial Pipeline CEO to the US Senate, June 2021',
              'Explain how the source shows the value of multi-factor authentication.', 'With MFA, a stolen password alone would not have allowed access; one missing control enabled an attack that disrupted national fuel supply.')],
    evaluate=[('Organisations should never pay ransomware demands.',
               ['payment funds criminal groups and encourages more attacks', 'no guarantee data will be restored', 'possible sanctions violations'],
               ['hospitals may need to restore systems to save lives', 'paying may be cheaper than prolonged disruption', 'insurers sometimes cover payments'],
               'As a policy, not paying reduces incentives for attackers, but there may be rare life-critical cases; prevention and backups are the real solution.'),
              ('Cybersecurity is mainly the responsibility of individual users.',
               ['users choose passwords, click links and install updates', 'awareness training reduces phishing success'],
               ['organisations and vendors design systems and set defaults', 'governments set standards (e.g. bans on default passwords)', 'state-level attacks exceed individual capacity'],
               'Users play a part, but responsibility lies mostly with organisations, vendors and governments that design and regulate systems.')],
    extended=[('Analyse one major cyberattack and evaluate the measures that could have prevented or reduced its impact.', 'E.g. WannaCry, Colonial Pipeline, NotPetya; describe attack vector; analyse impacts on stakeholders; measures (patching, MFA, segmentation, backups, training, incident response); judgement.', 6, 'long')],
))
AR('ch12-st2', [
    ('WannaCry spread rapidly across networks in 2017.', 'WannaCry exploited a Windows vulnerability on computers that had not been patched.', 'a', 'Unpatched systems allowed worm-like spread via EternalBlue.'),
    ('A password and a security question together count as multi-factor authentication.', 'Multi-factor authentication requires two or more different types of factor.', 'd', 'Both are "something you know", so A is false.'),
])


@R.add('ch12-st3', 'C3', (1, 5), 'numerical')
def cascade(rng, slot):
    k = rng.choice([2, 3, 4, 5])
    gens = rng.choice([4, 5, 6, 8])
    start = rng.choice([1, 5, 10])
    plat = rng.choice(['a messaging app', 'a short-video platform', 'a social network', 'a group chat network'])
    total_new = start * k ** gens
    cum = sum(start * k ** i for i in range(gens + 1))
    stem = (f'A rumour is posted by {start} account{"s" if start > 1 else ""} on {plat}. In each round of sharing, every person who has just received it passes it to {k} new people. '
            f'Calculate how many people receive it in round {gens}')
    if slot.d >= 3:
        stem += f', and the total number reached after {gens} rounds (including the original poster{"s" if start > 1 else ""}).'
        ans = f'{total_new:,} in round {gens}; {cum:,} in total'
        key = f'{start} × {k}^{gens} = {total_new:,} [M1 A1]; total = ' + ' + '.join(f'{start * k ** i:,}' for i in range(gens + 1)) + f' = {cum:,} [A1].'
        m = 3
        if slot.d >= 4:
            stem += ' Explain how a forwarding limit could change this outcome.'
            ans += '; limiting forwards reduces k, and because growth is exponential, a small reduction in k greatly reduces total reach'
            key += f' e.g. k = {k - 1}: {start} × {k - 1}^{gens} = {start * (k - 1) ** gens:,} in round {gens} – negative feedback slows spread [R1].'
            m = 5
    else:
        stem += '.'
        ans = f'{total_new:,}'
        key = f'{start} × {k}^{gens} = {total_new:,} [M1 A1].'
        m = 2
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch12-st3', F(
    terms=[('filter bubble', 'a state of intellectual isolation that can result when personalisation algorithms show users mainly information that matches their past behaviour (Eli Pariser, 2011)'),
           ('echo chamber', 'an environment in which people mainly encounter views that reinforce their own because of their choices and networks'),
           ('polarisation', 'the growing division of opinion into opposing extremes'),
           ('virality', 'the rapid spread of content from person to person across networks'),
           ('social capital', 'the value people gain from their social networks and relationships, such as support, information and opportunities'),
           ('network effect (social)', 'the way a social platform becomes more useful – and harder to leave – as more of a person\'s contacts join it')],
    facts=[('Who popularised the term "filter bubble" in a 2011 book?', 'Eli Pariser', ['Cass Sunstein', 'Shoshana Zuboff', 'Sherry Turkle'], 'The Filter Bubble: What the Internet Is Hiding from You (2011).'),
           ('Which internal documents, leaked by Frances Haugen in 2021, revealed Facebook\'s own research on harms such as Instagram\'s effects on teenage girls?', 'The Facebook Files / Facebook Papers', ['The Panama Papers', 'The Pentagon Papers', 'The Snowden files'], 'Reported by the Wall Street Journal from September 2021.'),
           ('In 2018 WhatsApp limited message forwarding in India after rumours were linked to what?', 'Mob lynchings', ['Election fraud', 'Bank collapses', 'Power cuts'], 'Rumours about child kidnappers led to deadly attacks.'),
           ('Which UN mission found in 2018 that Facebook had played a "determining role" in spreading hate speech during the Rohingya crisis?', 'The Independent International Fact-Finding Mission on Myanmar', ['UNESCO', 'The UN Security Council', 'The World Health Organization'], 'Facebook later admitted it had been too slow to act.')],
    why=[('Explain why personalisation algorithms can create filter bubbles.', 'They rank content by predicted engagement based on past behaviour, so users see more of what they already like and less that challenges them, narrowing exposure over time.'),
         ('Explain why false or outrageous content often spreads faster than accurate content.', 'Novel, emotional and outrage-provoking content attracts more shares and comments, which engagement-based algorithms amplify; MIT research found false news spread farther and faster than true news.'),
         ('Explain why social media can both strengthen and weaken communities.', 'It helps people maintain ties and find communities (diaspora groups, patient support), but can also spread division, harassment and misinformation and displace local, face-to-face interaction.')],
    contrast=[('a filter bubble', 'an echo chamber', 'A filter bubble is created mainly by algorithms personalising what a user sees; an echo chamber is created mainly by users\' own choices of whom to follow and which groups to join – in practice the two reinforce each other.'),
              ('bonding social capital', 'bridging social capital', 'Bonding social capital comes from close ties with similar people (family, close friends); bridging social capital comes from weaker ties across different groups, which online networks can widen.')],
    misc=[('Filter bubbles mean people never see opposing views online.', 'Research (e.g. Bakshy et al., 2015; Reuters Institute studies) shows most users encounter some cross-cutting content; individual choices and offline networks also shape exposure, so the effect is real but often overstated.'),
          ('Social media is the main cause of political polarisation.', 'Polarisation began rising in some countries before social media, and is also driven by partisan media, economic inequality and party strategies; social media can amplify it.')],
    cases=[('Facebook in Myanmar', 'Facebook was the main gateway to the internet for many in Myanmar; hate speech against the Rohingya spread widely before and during the 2017 violence, and the UN fact-finding mission (2018) said Facebook played a "determining role".', 'the social impact of networks',
            'an engagement-driven platform with weak local-language moderation amplified hate in a fragile context, contributing to real-world violence.'),
           ('WhatsApp rumours in India (2018)', 'False messages about child kidnappers spread on WhatsApp and were linked to more than two dozen killings by mobs; WhatsApp limited forwarding and labelled forwarded messages.', 'virality in encrypted networks',
            'private, encrypted group sharing allowed rumours to spread without moderation, so design changes (forward limits) were used to slow virality.'),
           ('the Facebook Files (2021)', 'Leaked internal research showed Facebook knew some features (e.g. reshare amplification, Instagram for teens) could increase harms, and that a 2018 algorithm change towards "meaningful social interactions" rewarded outrage.', 'algorithms and social harm',
            'the company\'s own evidence linked design choices to divisive content, strengthening arguments for regulation such as the DSA.')],
    sources=[('"Our algorithms exploit the human brain\'s attraction to divisiveness. If left unchecked, they will feed users more and more divisive content."', 'Internal Facebook presentation, 2018, reported by the Wall Street Journal, May 2020',
              'With reference to the source, explain how algorithms can contribute to polarisation.', 'Engagement-optimised algorithms amplify content people react to most, and divisive content provokes strong reactions, so users are shown increasingly divisive material.'),
             ('"Most people\'s news diets are not bubbles: they include a range of sources, even if they prefer some over others."', 'Reuters Institute Digital News Report commentary, 2022',
              'Explain how this source challenges the filter-bubble claim.', 'It suggests evidence for strong filter bubbles is limited; most users see diverse sources, so the effect of algorithms may be weaker than popularly claimed.')],
    evaluate=[('Social media algorithms are responsible for increasing polarisation in society.',
               ['engagement optimisation amplifies divisive content (Facebook Files)', 'filter bubbles narrow exposure'],
               ['research finds limited bubble effects for most users', 'polarisation predates social media in some countries (e.g. the US)', 'partisan TV and offline networks matter'],
               'Algorithms can amplify division, especially for highly engaged users and in fragile contexts, but they are one contributor among several.'),
              ('Social media has strengthened communities more than it has divided them.',
               ['keeps diaspora and families connected', 'support communities (health, LGBTQ+, disability)'],
               ['harassment, misinformation and hate (Myanmar)', 'weaker local ties and attention displacement'],
               'Social media has created valuable new communities, but its divisive effects in some contexts are severe; outcomes depend on design, moderation and context.')],
    extended=[('Evaluate whether design changes by platforms can reduce the negative social impacts of networks, using at least one example.', 'E.g. WhatsApp forward limits, Twitter/X Community Notes, Instagram hiding like counts, chronological feeds under the DSA; analyse intended and unintended effects; consider evidence; judgement.', 8, 'long')],
))

P2['ch12'] = dict(
    src=[('"For 18 months my students had no 4G. Online classes were impossible, and many families sent their children out of the valley to study."', 'Teacher in Srinagar, Jammu and Kashmir, interviewed by a news agency, 2021',
          'Identify two impacts of the shutdown described in {S}.', ['online classes were impossible / education disrupted', 'families sent children away to study'],
          'Explain why {S} is useful for understanding the impacts of internet shutdowns.', 'It provides first-hand testimony about the long-term educational and family consequences, which aggregate economic estimates do not capture; it is limited to one perspective and place.'),
         ('"Restrictions on internet access were imposed to prevent misuse by anti-national elements and to maintain public order."', 'Statement by government authorities on internet suspensions in Jammu and Kashmir, 2019',
          'Identify two reasons given for the restrictions in {S}.', ['preventing misuse by "anti-national elements"', 'maintaining public order'],
          'Explain the perspective expressed in {S}.', 'It presents the shutdown as a security measure protecting public order, prioritising state security over access to information; it does not mention the costs to residents.'),
         ('"Freedom of speech and expression through the medium of internet is an integral part of Article 19(1)(a)... an order suspending internet services indefinitely is impermissible."', 'Supreme Court of India, Anuradha Bhasin v Union of India, January 2020',
          'Identify two points made by the court in {S}.', ['expression through the internet is constitutionally protected (Article 19(1)(a))', 'indefinite suspension of internet services is not permitted'],
          'Explain why {S} matters for internet governance.', 'It established that internet restrictions must be lawful, necessary and proportionate and subject to review, limiting the state\'s power to impose open-ended shutdowns.')],
    cmp=[(0, 1, 'internet shutdowns in Jammu and Kashmir', ['both refer to the same internet restrictions', 'both acknowledge the shutdown affected people\'s use of the internet'],
          ['Source A emphasises harms to education and families; Source B emphasises security and public order', 'A is a personal account; B is an official justification', 'A implies the shutdown was too long; B implies it was necessary']),
         (1, 2, 'the legitimacy of internet restrictions', ['both accept the state may in some cases restrict access'],
          ['Source B treats restrictions as justified by public order; Source C limits them by constitutional rights', 'C rejects indefinite suspensions'])],
    ev=[(0, 1, 'internet shutdowns are an effective way to maintain public order.', ['authorities argue shutdowns prevent coordination of violence and rumours (Source B)'],
         ['severe harm to education and families (Source A)', 'research suggests shutdowns may push protest towards violence and do not stop unrest', 'court ruling on proportionality (Source C)']),
        (1, 2, 'courts can effectively protect digital rights against state power.', ['Anuradha Bhasin established proportionality and review (Source C)', 'courts provide a route for citizens to challenge the state'],
         ['4G restrictions continued for a year after the ruling', 'governments can reissue orders; enforcement depends on the executive (Source B)'])],
)

INTV['ch12'] = [
    ('WhatsApp\'s message-forwarding limits', 'In 2018 WhatsApp limited forwarding in India to five chats at once and labelled forwarded messages; in 2020 it limited "highly forwarded" messages to one chat at a time, saying this reduced such forwards by 70%.',
     'False rumours spread rapidly through private, encrypted group chats and were linked to mob violence, but end-to-end encryption meant the platform could not read or moderate the messages.',
     ['users – slower sharing of both rumours and legitimate news', 'victims of rumour-driven violence – reduced risk', 'WhatsApp – keeps encryption while showing responsibility', 'governments – some demanded traceability of message originators instead'],
     ['design change preserves end-to-end encryption and privacy', 'measurable reduction in viral forwards', 'simple, global and low-cost'],
     ['rumours still spread through many small forwards and other apps', 'does not address content already shared', 'cannot distinguish harmful from useful content'],
     'Combine friction with in-app fact-checking tips (e.g. search-the-web button), partnerships with local fact-checkers and digital-literacy campaigns.'),
    ('the UK Product Security and Telecommunications Infrastructure (PSTI) regime', 'From April 2024 the UK banned default or easily guessable passwords on consumer connected devices, required manufacturers to publish a way to report vulnerabilities and to state how long security updates will be provided.',
     'Millions of insecure IoT devices with default passwords were being hijacked into botnets such as Mirai, threatening users and internet infrastructure.',
     ['consumers – more secure devices and information on update periods', 'manufacturers – compliance costs and redesign', 'retailers – duty not to sell non-compliant products', 'regulators – need to enforce against imported products'],
     ['tackles the most common weakness (default passwords)', 'clear, simple requirements', 'transparency about update periods helps consumers choose'],
     ['enforcement against online marketplaces and imports is difficult', 'only basic security covered', 'existing devices unaffected'],
     'Extend requirements to minimum update periods and coordinate with the EU Cyber Resilience Act to raise global standards.'),
]

# =============================================================================================
# ch13 Contexts and Paper 2 source-based skills
# =============================================================================================
CONTEXT_EX = [  # (example, best-fit context, reason)
    ('telemedicine consultations replacing some clinic visits in rural India (eSanjeevani)', 'health', 'it concerns access to medical care and well-being'),
    ('TikTok creators reviving interest in traditional Indigenous songs', 'cultural', 'it concerns traditions, language, arts and identity'),
    ('ride-hailing platforms changing taxi drivers\' incomes in Lagos', 'economic', 'it concerns work, markets and income'),
    ('data centres increasing water use during droughts in Arizona', 'environmental', 'it concerns natural resources and ecosystems'),
    ('micro-targeted political adverts during an election campaign', 'political', 'it concerns power, elections and governance'),
    ('Wikipedia editors debating the reliability of sources on a historical event', 'human knowledge', 'it concerns how knowledge is produced, shared and validated'),
    ('teenagers forming friendships through online multiplayer games', 'social', 'it concerns relationships, communities and social interaction'),
    ('AI tools used to transcribe and translate oral histories of elders', 'cultural', 'it concerns cultural heritage and language preservation'),
    ('satellite data used to monitor illegal deforestation in the Amazon', 'environmental', 'it concerns protection of ecosystems'),
    ('mobile money letting market traders in Kenya receive payments', 'economic', 'it concerns finance and livelihoods'),
    ('a government using facial recognition to monitor protests', 'political', 'it concerns state power and civil liberties'),
    ('fitness apps sharing users\' heart-rate data with insurers', 'health', 'it concerns health data and well-being'),
]
CTX7 = ['cultural', 'economic', 'environmental', 'health', 'human knowledge', 'political', 'social']


@R.add('ch13-st1', 'C3', (1, 3), 'mcq')
def context_mcq(rng, slot):
    ex, ctx, why = rng.choice(CONTEXT_EX)
    wrong = rng.sample([c for c in CTX7 if c != ctx], 3)
    return mcq(rng, f'Which Digital Society context does the following example most directly fit? Example: {ex}.', ctx, wrong,
               f'Best fit is the {ctx} context because {why}; examples can involve several contexts.')


@R.add('ch13-st1', 'C3', (2, 4), 'short')
def context_two(rng, slot):
    ex, ctx, why = rng.choice(CONTEXT_EX)
    return dict(stem=f'Identify two Digital Society contexts relevant to the following example and explain why each applies: {ex}.',
                answer=f'{ctx[0].upper() + ctx[1:]} ({why}), plus one other justified context, e.g. social, economic or political implications',
                markingKey=f'1 mark for each relevant context identified (the most direct is {ctx}); 1 mark for each explanation linking the example to that context. Accept any justified second context.',
                type='short', marks=4)


R.facts('ch13-st1', F(
    terms=[('context', 'in Digital Society, a broad area of human life in which digital systems have impacts: cultural, economic, environmental, health, human knowledge, political and social'),
           ('cultural context', 'the impacts of digital systems on arts, traditions, languages, beliefs and identities'),
           ('economic context', 'the impacts of digital systems on work, business, markets, trade and income'),
           ('environmental context', 'the impacts of digital systems on the natural world, resources, energy and climate'),
           ('health context', 'the impacts of digital systems on physical and mental well-being and on health care'),
           ('human knowledge context', 'the impacts of digital systems on how knowledge is created, shared, stored and judged reliable'),
           ('political context', 'the impacts of digital systems on power, government, elections, law and civic participation'),
           ('social context', 'the impacts of digital systems on relationships, communities, education and social groups')],
    facts=[('How many contexts are identified in the Digital Society guide?', 'Seven', ['Four', 'Five', 'Ten'], 'Cultural, economic, environmental, health, human knowledge, political and social.'),
           ('Which of the following is a Digital Society context?', 'Human knowledge', ['Ancient history', 'Organic chemistry', 'Mechanics'], 'Human knowledge covers how knowledge is produced and shared.'),
           ('An inquiry into how a national e-voting system affects trust in elections most directly fits which context?', 'Political', ['Health', 'Environmental', 'Cultural'], 'It concerns elections and governance.'),
           ('An inquiry into the energy used by AI data centres most directly fits which context?', 'Environmental', ['Cultural', 'Health', 'Human knowledge'], 'It concerns resources and climate.')],
    why=[('Explain why one real-world example can be analysed through several contexts.', 'Digital systems affect many areas of life at once: a ride-hailing platform has economic impacts (driver income), social impacts (safety, community), political ones (labour regulation) and environmental ones (congestion, emissions), so several lenses give a fuller analysis.'),
         ('Explain why contexts are useful for structuring a Digital Society inquiry.', 'They help students identify which kinds of impacts and stakeholders to investigate, make comparisons across examples and avoid looking only at technical features.'),
         ('Explain why the human knowledge context is particularly important in the age of generative AI.', 'Generative AI changes how information is produced and judged – it can write convincing but false text, raise questions of authorship and reliability, and reshape education and research.')],
    contrast=[('the social context', 'the cultural context', 'The social context focuses on relationships, communities and social groups (e.g. online friendships, inequality); the cultural context focuses on arts, traditions, languages and shared meanings (e.g. memes, heritage digitisation).'),
              ('the economic context', 'the political context', 'The economic context concerns work, markets and income (e.g. gig work pay); the political context concerns power, law and government (e.g. laws regulating gig platforms).')],
    misc=[('Each real-world example belongs to only one context.', 'Most examples cut across several contexts; students choose the most relevant ones for their focus and can analyse interactions between them.'),
          ('The environmental context only covers climate change.', 'It also covers e-waste, mining of minerals, water use by data centres, biodiversity monitoring and the use of technology for environmental protection.')],
    cases=[('eSanjeevani in India', 'India\'s national telemedicine service eSanjeevani had recorded well over 100 million consultations by 2023, connecting rural patients with doctors remotely.', 'the health context',
            'remote consultations widened access to care for rural patients, though connectivity and digital literacy limited who benefited.'),
           ('the digitisation of the Timbuktu manuscripts', 'Projects with Google Arts & Culture and other partners digitised thousands of historic manuscripts from Timbuktu, Mali, some of which had been smuggled to safety in 2012–13.', 'the cultural and human knowledge contexts',
            'digitisation preserves and shares cultural heritage globally, but raises questions about ownership and who controls access to the copies.'),
           ('Global Forest Watch', 'Global Forest Watch, run by the World Resources Institute, uses satellite imagery and algorithms to send near-real-time alerts of tree-cover loss.', 'the environmental context',
            'satellite data and alerts help governments and communities respond to deforestation, showing digital systems supporting environmental protection.')],
    sources=[('"Our grandmothers\' songs were only on cassette tapes. Now they are on YouTube with subtitles, and young people are learning them again."', 'Member of a Sámi cultural association, Norway, 2022',
              'Identify the context most relevant to the source and explain why.', 'Cultural context: digital platforms are being used to preserve and share traditional songs and language, supporting cultural identity among young people.'),
             ('"Telemedicine means my father no longer travels four hours to see a specialist – when the network works."', 'Resident of a rural district in Peru, 2023',
              'Explain which two contexts the source illustrates.', 'Health (access to specialist care) and social/economic (reduced travel time and cost, but unequal connectivity – the digital divide).')],
    evaluate=[('The economic context is the most important lens for understanding digital systems.',
               ['digital systems are driven by business models and profit', 'economic impacts (jobs, income) affect all other areas'],
               ['political, social and cultural impacts are not reducible to economics', 'some impacts (dignity, rights, knowledge) are non-economic', 'importance varies with the example'],
               'Economics is often central, but the most important lens depends on the example and inquiry focus; strong analysis connects several contexts.'),
              ('Digital technology has had a more positive impact in the health context than in any other context.',
               ['telemedicine, wearables and digital records improve access and care', 'disease surveillance and research'],
               ['mental-health harms from social media', 'health-data privacy breaches', 'unequal access'],
               'Health shows strong benefits, but they are uneven and matched by new harms; comparisons across contexts depend on the criteria used.')],
    extended=[('Choose one real-world digital system and analyse its impacts in three different contexts.', 'Select a specific system (e.g. TikTok, M-Pesa, Aadhaar, a smart-city project); analyse impacts in three contexts with evidence; show interactions between contexts; conclude on overall significance.', 8, 'long')],
))

SRC_DATA = [  # (title, years, values, unit) – rounded published figures
    ('Share of adults in Kenya with a mobile-money account (World Bank Global Findex)', (2014, 2017, 2021), (58, 73, 79), '%'),
    ('UPI transactions in India in December of each year (billions, NPCI)', (2018, 2020, 2023), (0.62, 2.23, 12.0), 'billion'),
    ('Share of the world population using the internet (ITU, approximate)', (2005, 2015, 2024), (16, 41, 68), '%'),
    ('Global e-waste generated (million tonnes, Global E-waste Monitor)', (2010, 2019, 2022), (34, 53.6, 62), 'Mt'),
]


@R.add('ch13-st2', 'C3', (2, 5), 'numerical')
def source_data(rng, slot):
    title, ys, vs, u = rng.choice(SRC_DATA)
    i, j = rng.choice([(0, 1), (1, 2), (0, 2)])
    ch = pct_change(vs[i], vs[j])
    tbl = '\n'.join(f'{y}: {v:g}' for y, v in zip(ys, vs))
    stem = f'Source (data): {title}\n{tbl}\n\nCalculate the percentage change between {ys[i]} and {ys[j]}.'
    ans = f'{pc(ch)}%'
    key = f'({vs[j]:g} − {vs[i]:g}) ÷ {vs[i]:g} × 100 = {pc(ch)}% [M1 A1].'
    m = 2
    if slot.d >= 3:
        stem += ' Identify one limitation of using this source on its own to make claims about digital society.'
        ans += '; e.g. it shows only one indicator and does not explain causes, who is included/excluded, or how the data was collected'
        key += ' Limitation: aggregate figures hide inequalities, no information on methodology or causes, single indicator [R1 R1].'
        m = 4
    if slot.d >= 5:
        stem += ' Suggest one other source that would help corroborate or extend it.'
        ans += '; e.g. a household survey by a national statistics office, an academic study or interviews with users'
        key += ' Relevant additional source with a reason [R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch13-st2', F(
    terms=[('origin (of a source)', 'who created a source, when and where, which helps judge its authority and possible bias'),
           ('purpose (of a source)', 'why a source was created – to inform, persuade, sell, entertain or record – which affects how it presents information'),
           ('value (of a source)', 'what a source is useful for in answering a specific question, given its origin, purpose and content'),
           ('limitation (of a source)', 'what a source cannot show or the ways in which it may be unreliable or incomplete for a specific question'),
           ('compare and contrast', 'IB command term: give an account of similarities and differences between two or more items, referring to both throughout'),
           ('own knowledge', 'relevant information, examples and concepts that a student brings from outside the sources provided'),
           ('corroborate', 'to confirm a claim by finding support for it in another independent source')],
    facts=[('In Paper 2, what does the command term "compare and contrast" require?', 'Both similarities and differences, referring to both sources throughout', ['Only similarities', 'A summary of each source separately', 'Only differences'], 'One-sided answers are capped.'),
           ('Which of the following is the best example of using "own knowledge" in an evaluation question?', 'Referring to the GDPR fine against Meta when evaluating a source about data protection', ['Quoting the source again', 'Describing the layout of the source', 'Stating the source\'s word count'], 'Own knowledge brings in relevant external examples.'),
           ('A company press release about its new AI tool is most likely to have which purpose?', 'To promote the company and its product', ['To provide neutral academic analysis', 'To criticise the company', 'To report independent test results'], 'Purpose shapes what is included and omitted.'),
           ('Which of these is a limitation of an infographic showing global internet-use percentages?', 'It may hide differences within countries, such as rural–urban or gender gaps', ['It contains numbers', 'It is visual', 'It is about the internet'], 'Aggregate figures conceal inequality.')],
    why=[('Explain why a source\'s purpose affects its value for an inquiry.', 'A source created to persuade or sell may select favourable evidence and omit costs, so it is valuable for showing a stakeholder\'s perspective but limited as evidence of actual impacts.'),
         ('Explain why answers to evaluation questions in Paper 2 should use both the sources and own knowledge.', 'The sources give specific evidence to analyse, while own knowledge adds wider examples, context and counter-arguments; together they allow a balanced, well-supported judgement, which markbands reward.'),
         ('Explain why visual sources such as cartoons need careful interpretation.', 'Cartoons use symbols, exaggeration and irony to make an argument, so the reader must identify the message, the cartoonist\'s perspective and the context rather than reading it literally.')],
    contrast=[('the value of a source', 'the reliability of a source', 'Value is how useful a source is for a specific question (even a biased source can be valuable for showing a perspective); reliability is how far its information can be trusted as accurate.'),
              ('a claim in a source', 'evidence in a source', 'A claim is what the source asserts (e.g. "AI will destroy jobs"); evidence is the data or examples it offers to support that claim (e.g. a survey of employers).')],
    misc=[('A biased source should be ignored in Paper 2.', 'Biased sources are often valuable for showing a stakeholder\'s perspective; the skill is to recognise the bias and evaluate the source in that light.'),
          ('Comparing two sources means describing each one in turn.', 'Strong comparison links the sources point by point (running comparison) and explains similarities and differences, rather than writing two separate summaries.')],
    cases=[('the COMPAS debate between ProPublica and Northpointe', 'ProPublica (2016) argued COMPAS was biased because of unequal false positive rates; Northpointe replied it was fair because scores were equally calibrated across groups.', 'comparing sources that use different evidence',
            'the sources reach opposite conclusions partly because they use different fairness definitions, showing why students must analyse how each source defines and measures its claims.'),
           ("Meta's transparency reports versus whistle-blower evidence", 'Meta\'s reports present high proactive detection rates for harmful content, while Frances Haugen\'s 2021 disclosures suggested internal research showed only a small share of hate speech was removed.', 'origin and purpose of sources',
            'the company\'s public reports and internal documents serve different purposes, so evaluating claims requires comparing origin, purpose and evidence.'),
           ('a cartoon about smartphone addiction', 'Cartoons often show families at a table all staring at phones to criticise the effect of devices on relationships.', 'interpreting visual sources',
            'the image makes an argument through exaggeration; students should identify the message, consider the cartoonist\'s perspective and test it against research evidence.')],
    sources=[('"Our AI tutor improved test scores by 30% in a pilot of 200 students."', 'Press release by an educational technology company, 2024',
              'Analyse one value and one limitation of this source for an inquiry into AI in education.', 'Value: shows the company\'s claimed outcomes and how it markets its product. Limitation: produced by the company (promotional purpose), small pilot, no information on control group, independence or which tests – needs corroboration.'),
             ('"Children who use screens more than seven hours a day show thinning of the brain\'s cortex."', 'Headline summarising early results from a US study of adolescent brain development, 2018',
              'Explain why this source should be evaluated carefully before being used as evidence.', 'A headline simplifies early findings; correlation does not show causation; the study\'s researchers cautioned against conclusions; the original study and later results should be checked.')],
    evaluate=[('Primary sources are more useful than secondary sources for Paper 2-style analysis.',
               ['first-hand evidence of stakeholder views and data', 'allow students to make their own interpretations'],
               ['secondary sources provide context, synthesis and expert analysis', 'primary sources can be narrow, biased or unrepresentative'],
               'Usefulness depends on the question; strong answers combine primary evidence with secondary context and own knowledge.'),
              ('Statistical sources are more reliable than personal testimony.',
               ['represent many cases and show scale', 'less influenced by individual emotion'],
               ['statistics depend on definitions and collection methods', 'can be selectively presented', 'testimony captures experiences and causes statistics miss'],
               'Statistics show scale and testimony shows experience; reliability depends on method and origin, not type.')],
    extended=[('Two sources disagree about whether TikTok harms teenagers\' mental health: a TikTok safety blog post and a survey by a children\'s charity. Explain how you would compare and evaluate them to answer a Paper 2 question.', 'Identify claims and evidence in each; analyse origin, purpose, methods (sample, questions); find similarities/differences; bring own knowledge (e.g. Facebook Files, US Surgeon General advisory 2023, research on correlation vs causation); reach a balanced judgement.', 8, 'long')],
))

R.facts('ch13-st3', F(
    terms=[('real-world example', 'a specific, named and accurately described case of a digital system and its impacts, used as evidence in Digital Society answers'),
           ('stakeholder analysis', 'identifying the people and groups affected by or influencing a digital system and analysing how impacts differ between them'),
           ('impacts and implications', 'the direct effects of a digital system (impacts) and their wider, longer-term consequences (implications)'),
           ('concept–content–context link', 'the Digital Society approach of analysing an example by connecting a concept (e.g. power), content (e.g. algorithms) and a context (e.g. political)'),
           ('evaluate', 'IB command term: make an appraisal by weighing up the strengths and limitations'),
           ('to what extent', 'IB command term: consider the merits or otherwise of an argument or concept, with opinions and conclusions clearly presented and supported')],
    facts=[('Which of the following answers best uses a real-world example?', '"In 2020 Ofqual\'s algorithm downgraded about 39% of teacher-assessed A-level grades in England."', ['"Some algorithms are unfair in some places."', '"Technology can be good or bad."', '"Many people use apps."'], 'Specific, accurate detail strengthens analysis.'),
           ('Which command term requires weighing strengths and limitations?', 'Evaluate', ['State', 'Identify', 'Define'], 'Evaluate = make an appraisal by weighing up strengths and limitations.'),
           ('A response analysing how TikTok\'s algorithm (content) shapes young people\'s identity (concept) in the cultural context is using which approach?', 'Linking concepts, content and contexts', ['Describing hardware only', 'Using only a definition', 'A purely technical explanation'], 'This is the course\'s core analytical framework.'),
           ('What does the command term "discuss" require?', 'Offer a considered and balanced review that includes a range of arguments, factors or hypotheses', ['List facts', 'Give a definition', 'Calculate a value'], 'Discuss requires balance and support with evidence.')],
    why=[('Explain why specific real-world examples are essential in Digital Society extended responses.', 'Markbands reward accurate, relevant and specific examples; precise details (names, dates, data) show understanding and turn general claims into supported analysis.'),
         ('Explain why analysing impacts on different stakeholders strengthens an answer.', 'It shows that a digital system creates winners and losers, reveals power relations and makes evaluation balanced rather than one-sided.'),
         ('Explain why a conclusion should follow from the analysis.', 'A judgement that weighs the evidence presented, rather than repeating the question or introducing new points, shows the reasoning behind the student\'s position, which is what evaluation questions assess.')],
    contrast=[('describing an example', 'analysing an example', 'Describing tells what happened (Robodebt sent debt letters); analysing explains why and how it matters, linking to concepts and stakeholders (automated averaging shifted the burden of proof onto vulnerable people, showing power and values issues).'),
              ('evaluate', 'explain', 'Explain asks for causes, reasons or mechanisms; evaluate asks for a judgement that weighs strengths and limitations.')],
    misc=[('Including as many examples as possible guarantees a high mark.', 'Examples must be relevant, accurate and analysed; a few well-developed examples linked to the question score higher than a list of names.'),
          ('A balanced answer should avoid reaching a conclusion.', 'Balance means considering different perspectives, but evaluation questions require a clear, supported judgement.')],
    cases=[('Ofqual\'s 2020 grading algorithm', 'With exams cancelled, an algorithm adjusted teacher grades using schools\' historical results; about 39% of grades were lowered and after protests ("Ditch the algorithm") the government reverted to teacher grades.', 'applying concepts, content and contexts',
            'the case links algorithms (content), power and values (concepts) and education/political contexts, making it a strong Paper 1 example.'),
           ('Uber v Aslam (UK Supreme Court, 2021)', 'The UK Supreme Court ruled in February 2021 that Uber drivers were "workers" entitled to minimum wage and holiday pay, not self-employed contractors.', 'power and the economic context of platforms',
            'the ruling shows how courts can rebalance power between platforms and workers, and how algorithmic management (pay, ratings) shaped the legal decision.'),
           ('the TikTok ban debate in the USA', 'In 2024 the US passed a law requiring ByteDance to divest TikTok or face a ban, citing national-security concerns about data and influence; the Supreme Court upheld the law in January 2025.', 'power, space and political context',
            'the case links data flows across borders, platform ownership and state power, illustrating multiple concepts in one example.')],
    sources=[('"Ditch the algorithm!"', 'Chant by students protesting outside the Department for Education, London, August 2020',
              'Explain what the source reveals about public attitudes to algorithmic decision-making.', 'Students rejected an algorithm deciding their futures, showing distrust of opaque automated decisions and a demand for human, individual judgement and accountability.'),
             ('"Uber drivers are workers, not independent contractors."', 'Summary of the UK Supreme Court judgment in Uber BV v Aslam, February 2021',
              'Explain how this source could be used in a Paper 1 answer about power.', 'It shows a legal intervention that limited platform power over workers, providing a specific example of resistance and regulation in the economic context.')],
    evaluate=[('Gig-economy platforms have given workers more freedom than traditional employment.',
               ['flexible hours and easy entry to work', 'income opportunities for migrants and students'],
               ['algorithmic management controls pay and access to jobs', 'lack of sick pay, pensions and protection', 'courts (Uber v Aslam) and the EU Platform Work Directive (2024) recognise imbalance'],
               'Platforms offer flexibility, but algorithmic control and weak protections mean freedom is often limited; regulation is reshaping the balance.'),
              ('The use of algorithms in education does more harm than good.',
               ['Ofqual 2020 downgrading', 'proctoring software errors and privacy invasion'],
               ['adaptive learning platforms personalise practice', 'automated feedback saves teachers time'],
               'Algorithms can support learning when used transparently with human oversight; harm arises when they make high-stakes decisions without accountability.')],
    extended=[('With reference to one real-world example, evaluate the impact of a digital system on one group of stakeholders, linking at least one concept and one context.', 'Specific example (e.g. Uber drivers, Aadhaar welfare recipients, A-level students in 2020); concept (power, identity, values) and context (economic, political, social); impacts with evidence; implications; balanced judgement.', 8, 'long')],
))

P2['ch13'] = dict(
    src=[('"Platform work offers me flexibility. I choose when I log in, and I can fit deliveries around my studies."', 'Food-delivery rider in Madrid, interviewed for a 2022 European Commission study',
          'Identify two benefits of platform work described in {S}.', ['flexibility / choosing when to log in', 'fitting work around studies'],
          'Explain why {S} might not represent all platform workers.', 'It is a single student worker whose income may be supplementary; full-time riders relying on the platform for their main income may experience pay, safety and algorithmic control differently.'),
         ('"The app decides everything – which orders I get, how much they pay, and whether I am deactivated. There is no one to talk to."', 'Ride-hailing driver in Nairobi, interviewed for a 2023 Fairwork report',
          'Identify two ways the platform controls work according to {S}.', ['allocates orders and sets pay through the app', 'can deactivate workers without human contact'],
          'Explain how {S} illustrates algorithmic management.', 'Decisions on work allocation, pay and discipline are made by the app\'s algorithms rather than human managers, with no clear route for appeal, which gives the platform power over workers.'),
         ('"Persons performing platform work should not be dismissed on the basis of decisions taken by automated systems without human review."', 'Summary of a provision in the EU Platform Work Directive, adopted 2024',
          'Identify two features of the intervention in {S}.', ['applies to people doing platform work', 'requires human review of automated decisions such as dismissal'],
          'Explain how {S} responds to concerns about platform power.', 'It limits automated control by requiring human oversight of significant decisions, giving workers protection against unexplained deactivation.')],
    cmp=[(0, 1, 'the experience of platform work', ['both describe working through an app', 'both refer to workers\' relationship with the platform'],
          ['Source A emphasises flexibility and choice; Source B emphasises control and lack of human contact', 'A is a part-time student in Madrid; B appears to depend on the work in Nairobi']),
         (1, 2, 'automated decisions in platform work', ['both concern automated decisions affecting workers, including deactivation'],
          ['Source B describes the problem from a worker\'s view; Source C describes a legal response', 'C introduces human review that B says is missing'])],
    ev=[(0, 1, 'platform work benefits workers more than it harms them.', ['flexibility (Source A)', 'low barriers to entry for students and migrants'],
         ['algorithmic control and deactivation (Source B)', 'need for legal protection (Source C, Uber v Aslam)', 'income instability and lack of benefits']),
        (1, 2, 'regulation can effectively protect platform workers from algorithmic management.', ['human review of deactivation (Source C)', 'Uber v Aslam gave worker rights in the UK'],
         ['enforcement across many countries is uneven', 'platforms may adjust models to avoid rules', 'workers outside the EU (Source B) not covered'])],
)
