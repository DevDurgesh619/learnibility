"""IB DP Digital Society SL/HL (first assessment 2024) – ib-g12-informatics (slug informatics), year 2.

Content pack for the QB-IB engine. Year 2 covers content areas 3.5 media, 3.6 artificial intelligence and
3.7 robots and autonomous technologies, the contexts in depth, the HL extension challenges (5.1 global
well-being, 5.2 governance and human rights, 5.3 sustainable development) and interventions (Paper 3),
Paper 1 extended-response skills and the internal assessment inquiry project. Items use IB command
terms and real, correctly described examples (deepfakes such as the 2022 Zelenskyy video and the 2024
Hong Kong video-call fraud, the EU DSA and AI Act, content moderation and the Meta Oversight Board,
COMPAS, gig platforms and Uber v Aslam, the Molly Russell inquest, internet shutdowns, Waymo and the
2018 Tempe crash, the MIT Moral Machine, Zipline drones, Paro, da Vinci, e-waste and PUE ...).
Parametric items compute their own answers (confusion matrices, nearest-neighbour classification,
perceptrons, fairness rates, cascades, streaming data, robot control traces, payback, PUE).

Mock = one exam set mirroring examPattern in targets.json (paper marks there are UNVERIFIED; section
marks below are fixed so every mock carries the same total):
  Paper 1 – two structured questions on a real-world example, parts (a) 2, (b) 4, (c) 6, (d) 8 marks
  Paper 2 – source-based: Q1 identify [2], Q2 explain with the source [4], Q3 compare and contrast two
            sources [6], Q4 evaluate using the sources and own knowledge [12]
  Paper 3 (HL) – intervention brief on an HL challenge: Q1 explain the challenge [4], Q2 analyse
            impacts on stakeholders [6], Q3 evaluate the intervention and recommend [12] (abridged)
Mock-only templates return None outside their own section style.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names, CITIES  # noqa: F401

CONFIG = {'minutesPerMark': 1.8, 'mcqMinutes': 1.0}

P2_CHAPTERS = [2, 4, 6, 9, 12]
P3_CHAPTERS = [8, 9, 10, 11]

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
# ch01 Content 3.5 Media: types, characteristics and evolution
# =============================================================================================
@R.add('ch01-st1', 'C3', (1, 4), 'numerical')
def stream_data(rng, slot):
    q = rng.choice([('standard definition (SD)', 3), ('high definition (HD, 1080p)', 5), ('4K ultra HD', 15), ('720p HD', 3.5)])
    hrs = rng.choice([1, 2, 3, 4])
    days = rng.choice([7, 30])
    gb_h = q[1] * 3600 / 8 / 1000
    stem = f'A video stream in {q[0]} uses about {q[1]:g} Mbps. Calculate the data used in one hour, in gigabytes (1 GB = 1000 MB, 8 bits = 1 byte).'
    ans = f'{pc(gb_h, 3)} GB per hour'
    key = f'{q[1]:g} Mb/s × 3600 s = {q[1] * 3600:,.0f} Mb [M1]; ÷ 8 = {q[1] * 450:,.0f} MB = {pc(gb_h, 3)} GB [A1].'
    m = 2
    if slot.d >= 3:
        stem += f' A student watches {hrs} hour{"s" if hrs > 1 else ""} a day for {days} days on a mobile plan with a 50 GB allowance. Calculate the total data used and state whether it fits the plan.'
        tot = gb_h * hrs * days
        ans += f'; {pc(tot, 2)} GB total – {"within" if tot <= 50 else "exceeds"} the 50 GB allowance'
        key += f' {pc(gb_h, 3)} × {hrs} × {days} = {pc(tot, 2)} GB [M1 A1]; compared with 50 GB [A1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch01-st1', F(
    terms=[('digital media', 'content such as text, images, audio, video and games that is created, stored and distributed in digital form'),
           ('multimedia', 'content that combines several media types, such as text, images, sound and video, in one product'),
           ('virtual reality (VR)', 'a fully computer-generated, immersive environment experienced through a headset that blocks out the physical world'),
           ('augmented reality (AR)', 'technology that overlays digital information or images on a live view of the physical world, as in Pokémon Go'),
           ('interactivity', 'the ability of users to respond to and change media content, as in games or interactive news'),
           ('convergence', 'the merging of previously separate media, devices and industries into digital platforms (Henry Jenkins, Convergence Culture, 2006)'),
           ('immersive media', 'media that surrounds the user\'s senses, such as VR, 360° video and spatial audio')],
    facts=[('Which 2016 mobile game brought augmented reality to a mass audience?', 'Pokémon Go', ['Minecraft', 'Fortnite', 'Tetris'], 'Niantic\'s game overlaid creatures on the real world via phone cameras and GPS.'),
           ('Who wrote "the medium is the message" in Understanding Media (1964)?', 'Marshall McLuhan', ['Henry Jenkins', 'Neil Postman', 'Noam Chomsky'], 'McLuhan argued the form of a medium shapes society as much as its content.'),
           ('Which of the following is the best example of convergence?', 'A smartphone used for phone calls, music, video, news and banking', ['A printed newspaper', 'A vinyl record', 'A landline telephone'], 'One device combines functions of many earlier media.'),
           ('What distinguishes virtual reality from augmented reality?', 'VR replaces the user\'s view with a computer-generated world; AR overlays digital content on the real world', ['VR uses sound only; AR uses video only', 'VR is always 2D', 'AR requires a full headset that blocks vision'], 'Examples: Meta Quest (VR); Pokémon Go, Snapchat filters (AR).')],
    why=[('Explain why digital media can be copied and distributed more easily than analogue media.', 'Digital media is stored as data that can be duplicated perfectly at almost no cost and sent instantly over networks, whereas analogue copies lose quality and need physical distribution.'),
         ('Explain why interactivity changes the relationship between media and audiences.', 'Interactive media lets users choose paths, comment, create and share, so audiences become participants and data sources rather than passive receivers.'),
         ('Explain why games are considered an important form of digital media.', 'Games reach billions of players, generate more revenue than film and music combined, create communities and cultures, and are used for education, storytelling and political messages.')],
    contrast=[('virtual reality', 'augmented reality', 'VR immerses users in a fully computer-generated environment that replaces the physical world; AR adds digital elements to the user\'s view of the real world.'),
              ('linear media', 'interactive media', 'Linear media is consumed in a fixed sequence chosen by the producer (a broadcast film); interactive media responds to user choices (a video game, a choose-your-path documentary).')],
    misc=[('Digital media is just traditional media in a different format.', 'Digital media is also searchable, copyable, interactive, networked and data-generating, which changes how it is produced, distributed, monetised and controlled.'),
          ('VR and AR are only used for entertainment.', 'They are used in surgical training, architecture, military simulation, education (virtual field trips), therapy (exposure therapy for PTSD) and retail.')],
    cases=[('Pokémon Go (2016)', 'Niantic\'s AR game was downloaded hundreds of millions of times in its first year, sending players into parks and streets to catch virtual creatures.', 'augmented reality and space',
            'the game layered digital content on physical places, changing how people moved through cities and raising safety and trespass issues.'),
           ('the growth of the games industry', 'Global games revenue (about US$180 billion a year in the early 2020s) exceeds that of film and recorded music combined.', 'games as a dominant digital medium',
            'games have become a central form of cultural expression and social interaction, not a niche hobby.'),
           ('VR exposure therapy', 'Clinicians use VR environments to treat phobias and PTSD by gradually exposing patients to feared situations in a controlled setting.', 'immersive media in the health context',
            'immersion allows safe, repeatable therapy that would be difficult in the real world.')],
    sources=[('"The medium is the message."', 'Marshall McLuhan, Understanding Media (1964)',
              'Explain how this source can be applied to TikTok.', 'The short, vertical, algorithmically served video format shapes attention, creativity and what kinds of messages succeed (fast, emotional, visual), so the format influences society regardless of individual videos\' content.'),
             ('"In VR, I was standing in a refugee camp. I could look around, and a girl looked back at me."', 'Viewer describing the UN VR film Clouds Over Sidra (2015)',
              'Explain one strength and one limitation of immersive media suggested by the source.', 'Strength: immersion creates empathy and presence. Limitation: the producer still frames what is seen; the experience may be emotionally manipulative or give an illusion of understanding.')],
    evaluate=[('Immersive media such as VR will replace traditional screen-based media.',
               ['deeper engagement and presence', 'large investment (Meta, Apple Vision Pro 2024)'],
               ['headsets are expensive, uncomfortable and isolating', 'adoption has been slower than predicted', 'screens remain convenient and social'],
               'Immersive media will grow in specific uses (training, gaming, therapy) but is unlikely to replace screens soon.'),
              ('Games are the most influential form of digital media for young people.',
               ['huge reach and time spent', 'social spaces (Fortnite, Roblox) and identity'],
               ['short video platforms dominate attention for many', 'influence varies by gender, culture and age', 'messaging apps shape daily communication more'],
               'Games are highly influential, but short-form video and messaging may matter as much or more for many young people.')],
    extended=[('Analyse how one type of digital media (e.g. games, short video, AR) has changed the way people create and consume content.', 'Choose a type; describe features (interactivity, convergence, algorithms); analyse changes for creators and audiences with examples; evaluate significance.', 6, 'long')],
))

R.facts('ch01-st2', F(
    terms=[('mass media', 'media that reaches large audiences from a small number of producers, such as newspapers, radio and television broadcasting'),
           ('social media', 'online platforms that let users create, share and interact with content and with each other'),
           ('participatory media', 'media in which audiences contribute content and shape communication, rather than only consuming it'),
           ('Web 2.0', 'a term popularised by Tim O\'Reilly in 2004 for websites built around user-generated content, interaction and collaboration'),
           ('citizen journalism', 'reporting of news events by members of the public, often using smartphones and social media'),
           ('gatekeeper (media)', 'a person or organisation, such as an editor, that decides which information reaches the public')],
    facts=[('Who popularised the term "Web 2.0" around 2004?', 'Tim O\'Reilly', ['Tim Berners-Lee', 'Mark Zuckerberg', 'Marshall McLuhan'], 'The O\'Reilly Web 2.0 conference (2004) helped spread the term.'),
           ('In which year was YouTube founded?', '2005', ['1998', '2010', '2001'], 'YouTube was founded in 2005 and bought by Google in 2006.'),
           ('Which event in 2009 was widely reported first through a tweeted photo by a passenger on a ferry?', 'The "Miracle on the Hudson" plane landing', ['The fall of the Berlin Wall', 'The first iPhone launch', 'The 2004 tsunami'], 'Janis Krums\' photo of US Airways Flight 1549 spread before news crews arrived.'),
           ('Which of the following is a characteristic of mass media rather than social media?', 'Content is produced by a few professional organisations for large audiences', ['Anyone can publish instantly', 'Audiences reply publicly in real time', 'Content is ranked by personalised algorithms'], 'Mass media is one-to-many with gatekeepers.')],
    why=[('Explain why the shift from mass media to social media has weakened traditional gatekeepers.', 'Anyone can publish to a potentially global audience without an editor\'s approval, so newspapers and broadcasters no longer control which stories reach the public – although platform algorithms have become new gatekeepers.'),
         ('Explain why citizen journalism can be both valuable and problematic.', 'It provides immediate, first-hand evidence from places journalists cannot reach (e.g. the video of George Floyd\'s murder in 2020), but it may lack verification, context and editorial standards, and can spread errors quickly.'),
         ('Explain why the business model of journalism has been disrupted by social media.', 'Advertising moved to platforms such as Google and Meta, which offer targeted ads and audiences at scale, while news is shared for free on platforms, reducing newspapers\' revenue and leading to closures of local newspapers.')],
    contrast=[('mass media', 'participatory media', 'Mass media is one-to-many, produced by professionals and controlled by gatekeepers; participatory media is many-to-many, with audiences creating and sharing content.'),
              ('citizen journalism', 'professional journalism', 'Citizen journalism is reporting by members of the public, often immediate and unedited; professional journalism follows editorial processes, verification and ethical codes, with accountable organisations.')],
    misc=[('Social media has removed all gatekeepers from the media.', 'Editors have lost power, but platform algorithms, content moderation and advertisers now act as powerful gatekeepers deciding what is visible.'),
          ('Traditional media no longer matters in the age of social media.', 'Television and established news outlets still set much of the agenda and much shared social-media content originates from professional news organisations.')],
    cases=[('the video of George Floyd\'s murder (2020)', 'Bystander Darnella Frazier filmed the murder of George Floyd by a Minneapolis police officer in May 2020; the video spread globally and was used as evidence in court. She received a special Pulitzer citation in 2021.', 'citizen journalism',
            'a smartphone video by a teenager provided crucial evidence and triggered worldwide protests, showing the power of participatory media.'),
           ('the decline of local newspapers', 'Research by Northwestern University found that the US had lost more than a third of its local newspapers since 2005, creating "news deserts".', 'the disruption of mass media',
            'advertising revenue shifted to platforms, and many communities lost local reporting on councils, courts and schools.'),
           ('the Arab Spring (2010–2011)', 'Protesters in Tunisia and Egypt used Facebook, Twitter and YouTube to share images and organise; Al Jazeera amplified citizen footage.', 'the interaction of social and mass media',
            'citizen content reached global audiences through both social platforms and broadcast media, showing convergence rather than replacement.')],
    sources=[('"There\'s a plane in the Hudson. I\'m on the ferry going to pick up the people. Crazy."', 'Tweet with photo by Janis Krums, 15 January 2009',
              'Explain how this source illustrates the change from mass media to participatory media.', 'An ordinary passenger, not a news organisation, broke the story with a phone photo shared instantly on Twitter, showing audiences acting as reporters and bypassing traditional gatekeepers.'),
             ('"The people formerly known as the audience."', 'Jay Rosen, journalism professor, blog post (2006)',
              'Explain what the source suggests about audiences in the digital age.', 'Audiences have become producers and distributors of content, no longer passive receivers of mass media.')],
    evaluate=[('Participatory media has improved the quality of public information.',
               ['more voices and first-hand evidence', 'faster reporting and accountability (George Floyd video)'],
               ['misinformation and lack of verification', 'loss of local journalism', 'algorithmic amplification of sensational content'],
               'Participatory media has widened information but not consistently improved its quality; it works best alongside professional journalism.'),
              ('Social media platforms are now more powerful than traditional news organisations.',
               ['control distribution and advertising revenue', 'algorithms decide visibility of news'],
               ['news organisations still produce most original reporting', 'trusted brands remain influential', 'platforms depend on news content and face regulation (e.g. Australia\'s News Media Bargaining Code 2021)'],
               'Platforms dominate distribution and revenue, but news organisations retain agenda-setting power and credibility.')],
    extended=[('Analyse how the evolution from mass media to social media has changed the role of the journalist.', 'Gatekeeping to curation/verification; competition with citizen journalism; business model changes; platform dependency; examples (Bellingcat open-source investigation, local news deserts); judgement.', 6, 'long')],
))


@R.add('ch01-st3', 'C3', (1, 5), 'numerical')
def creator_pay(rng, slot):
    kind = rng.choice(['stream', 'cpm'])
    if kind == 'stream':
        rate = rng.choice([0.003, 0.004, 0.005])
        streams = rng.choice([50000, 250000, 1000000, 4000000])
        share = rng.choice([15, 20, 50])
        gross = streams * rate
        artist = gross * share / 100
        stem = (f'A music-streaming service pays rights holders about US${rate} per stream. A song is streamed {streams:,} times, and the artist\'s contract gives them {share}% of the payment. '
                f'Calculate the artist\'s income.')
        ans = f'US${artist:,.2f}'
        key = f'{streams:,} × {rate} = US${gross:,.2f} [M1]; × {share}% = US${artist:,.2f} [A1].'
        m = 2
        if slot.d >= 3:
            target = rng.choice([1500, 2000, 3000])
            need = target / (rate * share / 100)
            stem += f' Calculate how many streams a month the artist would need to earn US${target:,} a month.'
            ans += f'; about {need:,.0f} streams a month'
            key += f' {target:,} ÷ ({rate} × {share}%) = {need:,.0f} streams [M1 A1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    views = rng.choice([200000, 800000, 2500000])
    cpm = rng.choice([2, 4, 6])
    monet = rng.choice([40, 60])
    share = 55
    rev = views * monet / 100 / 1000 * cpm
    creator = rev * share / 100
    stem = (f'A video gets {views:,} views; {monet}% are shown ads. Advertisers pay US${cpm} per 1,000 ad views (CPM), and the platform passes {share}% of ad revenue to the creator. Calculate the creator\'s income.')
    ans = f'US${creator:,.2f}'
    key = f'Ad views = {views:,} × {monet}% = {views * monet // 100:,} [M1]; revenue = {views * monet // 100:,} ÷ 1000 × {cpm} = US${rev:,.2f} [M1]; creator = {share}% = US${creator:,.2f} [A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain one way the platform holds power over creators.'
        ans += '; the platform sets the revenue share, controls the algorithm that decides views and can demonetise videos'
        key += ' Platform sets terms, algorithmic visibility and monetisation rules [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch01-st3', F(
    terms=[('platform economy', 'economic activity organised through digital platforms that connect producers and consumers and take a share of transactions'),
           ('creator economy', 'the economy of independent creators who earn income from content through advertising, sponsorship, subscriptions and fan funding'),
           ('streaming', 'delivering media content over the internet for immediate playback rather than download'),
           ('subscription model', 'a business model in which users pay a recurring fee for access to a library of content, as with Netflix or Spotify'),
           ('monetisation', 'earning revenue from content, for example through ads, subscriptions or sponsorships'),
           ('disintermediation', 'the removal of intermediaries (e.g. record labels, publishers) as creators reach audiences directly through platforms')],
    facts=[('In which year did Netflix begin offering streaming video?', '2007', ['1997', '2012', '2003'], 'Netflix started as a DVD-by-mail service in 1997.'),
           ('YouTube\'s Partner Programme typically gives creators about what share of advertising revenue on long-form videos?', '55%', ['10%', '90%', '30%'], 'YouTube keeps about 45%.'),
           ('Which platform, founded in 2013, lets fans pay creators a monthly subscription?', 'Patreon', ['Spotify', 'LinkedIn', 'Wikipedia'], 'Patreon supports direct fan funding.'),
           ('In 2024 Spotify stopped paying royalties for tracks with fewer than how many streams in the previous 12 months?', '1,000', ['10', '1,000,000', '100,000'], 'The policy redirected money to more-streamed tracks.')],
    why=[('Explain why streaming has changed how musicians earn money.', 'Income comes from fractions of a cent per stream rather than album sales, so only artists with very large numbers of streams earn substantial income; many rely more on touring, merchandise and fan funding.'),
         ('Explain why creators depend on platform algorithms.', 'Visibility, and therefore income, depends on recommendation algorithms that creators cannot control; a change to the algorithm or monetisation rules can cut views and earnings overnight.'),
         ('Explain why platforms can take a large share of revenue in the platform economy.', 'Network effects give them large audiences that creators and advertisers cannot reach elsewhere, so they can set terms, commission rates and rules.')],
    contrast=[('the creator economy', 'the traditional media industry', 'In the creator economy individuals produce and distribute content directly through platforms and fan funding; in the traditional industry, studios, labels and broadcasters financed, selected and distributed content.'),
              ('a subscription model', 'an advertising model', 'A subscription model charges users directly for access (Netflix); an advertising model gives free access and earns money by selling audience attention to advertisers (YouTube free tier).')],
    misc=[('Anyone can earn a full-time living as a creator on YouTube or TikTok.', 'Income is highly unequal: a small share of creators earn most of the money, while most earn little or nothing and depend on volatile algorithms.'),
          ('Streaming has made music distribution fairer for all artists.', 'Streaming lowered barriers to distribution, but pay per stream is tiny and contracts often give labels most of the money, so income is concentrated among the most-streamed artists.')],
    cases=[('Spotify\'s payment model', 'Spotify pays rights holders roughly in proportion to their share of total streams (a "pro-rata" model); in 2024 it stopped paying for tracks with fewer than 1,000 annual streams.', 'the platform economy',
            'the platform\'s rules decide how revenue is shared, favouring popular artists and showing platform power over cultural income.'),
           ('the 2023 Hollywood writers\' and actors\' strikes', 'The Writers Guild of America and SAG-AFTRA struck in 2023 over streaming residuals and the use of AI, winning new terms on pay and AI protections.', 'conflict over streaming economics',
            'workers challenged how streaming platforms share revenue and use technology, showing labour responses to platform business models.'),
           ('MrBeast and the creator economy', 'YouTuber Jimmy Donaldson (MrBeast) built one of the world\'s most-subscribed channels and businesses based on brand deals, merchandise and products.', 'how creators build businesses outside traditional media',
            'a single creator can reach audiences larger than TV networks, though such success is rare and depends on platform algorithms.')],
    sources=[('"I got a royalty statement for 1 million streams. It paid about the same as selling 300 CDs used to."', 'Independent musician, interview with a music-industry magazine, 2022',
              'With reference to the source, explain one impact of streaming on musicians.', 'Payment per stream is very low, so even large numbers of streams produce modest income compared with physical sales, making it hard for most musicians to earn a living from recordings.'),
             ('"The algorithm giveth and the algorithm taketh away."', 'Popular saying among YouTube creators',
              'Explain what the source suggests about the creator economy.', 'Creators\' success depends on platform algorithms; changes can bring sudden growth or collapse, showing creators\' lack of control and platform power.')],
    evaluate=[('Streaming platforms have been good for creators.',
               ['global distribution without labels or studios', 'new income streams (ads, fan funding)'],
               ['low pay per stream and unequal income', 'dependence on algorithms and changing rules', 'platforms capture much of the value'],
               'Platforms widened access to audiences, but most creators gain little income; benefits are concentrated among the most popular.'),
              ('The creator economy has made media more diverse.',
               ['creators from many backgrounds bypass gatekeepers', 'niche content finds audiences'],
               ['algorithms favour certain styles and languages', 'income inequality among creators', 'large creators become media companies'],
               'It has diversified who can publish, but visibility and income remain concentrated, so diversity of reach is more limited.')],
    extended=[('Evaluate the impact of streaming platforms on one creative industry (music, film or games).', 'E.g. music: Spotify pro-rata payments, label contracts, discovery, touring; film/TV: Netflix, residuals, 2023 strikes; evaluate for creators, audiences, platforms; judgement.', 8, 'long')],
))

# =============================================================================================
# ch02 Content 3.5 Media: influence, misinformation and platform power
# =============================================================================================
@R.add('ch02-st1', 'C3', (1, 5), 'numerical')
def misinfo_spread(rng, slot):
    kind = rng.choice(['ratio', 'cascade'])
    if kind == 'ratio':
        t = rng.choice([800, 1500, 2400])
        f = rng.choice([1.5, 1.7, 2.0])
        false = round(t * f)
        plat = rng.choice(['a social network', 'a short-video platform', 'a microblogging site'])
        stem = f'In a study on {plat}, a true news story was reshared {t:,} times on average, while a false story was reshared {false:,} times. Calculate how many percent more the false story was reshared.'
        p = pct_change(t, false)
        ans = f'{pc(p)}% more'
        key = f'({false:,} − {t:,}) ÷ {t:,} × 100 = {pc(p)}% [M1 A1].'
        m = 2
        if slot.d >= 3:
            stem += ' Suggest two reasons why false stories may be shared more than true ones.'
            ans += '; false stories are often more novel and emotionally arousing (surprise, disgust, outrage), and engagement-based algorithms amplify them'
            key += ' Novelty/emotion (Vosoughi et al. 2018) [R1]; algorithmic amplification or confirmation bias [R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    r = rng.choice([1.5, 2, 3])
    g = rng.choice([4, 5, 6])
    s0 = rng.choice([10, 20, 50])
    n = s0 * r ** g
    stem = (f'A deepfake video is first shared by {s0} accounts. Each new sharer leads, on average, to {r:g} further shares in the next hour. Estimate the number of new shares in hour {g}')
    if slot.d >= 3:
        lab = rng.choice([0.5, 0.6, 0.7])
        n2 = s0 * (r * lab) ** g
        stem += f'. A warning label reduces resharing by {round((1 - lab) * 100)}%. Estimate the new shares in hour {g} with the label.'
        ans = f'about {n:,.0f} without the label; about {n2:,.0f} with the label'
        key = f'{s0} × {r:g}^{g} = {n:,.0f} [M1 A1]; new rate {r:g} × {lab} = {r * lab:g}; {s0} × {r * lab:g}^{g} = {n2:,.0f} [M1 A1].'
        m = 4
        if slot.d >= 5:
            stem += ' Explain why small changes to sharing behaviour can have large effects.'
            ans += '; spread is exponential, so reducing the rate per sharer compounds each hour – if it falls below 1 the cascade dies out'
            key += ' Exponential compounding; threshold of 1 [R1 R1].'
            m = 6
    else:
        stem += '.'
        ans = f'about {n:,.0f}'
        key = f'{s0} × {r:g}^{g} = {n:,.0f} [M1 A1].'
        m = 2
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch02-st1', F(
    terms=[('misinformation', 'false or misleading information shared without the intention to deceive'),
           ('disinformation', 'false information deliberately created and spread to deceive or cause harm'),
           ('malinformation', 'genuine information shared to cause harm, such as leaking private information (Wardle and Derakhshan, 2017)'),
           ('deepfake', 'synthetic audio, image or video created with AI (e.g. generative adversarial networks or diffusion models) to make someone appear to say or do something they did not'),
           ('information disorder', 'Claire Wardle and Hossein Derakhshan\'s framework (Council of Europe, 2017) covering mis-, dis- and malinformation'),
           ('infodemic', 'an overabundance of information, including false information, during a crisis such as COVID-19 (term used by the WHO)'),
           ('coordinated inauthentic behaviour', 'networks of fake or coordinated accounts used to manipulate public debate, as defined by Meta')],
    facts=[('Which 2018 study in Science found that false news spread "farther, faster, deeper and more broadly" than the truth on Twitter?', 'Vosoughi, Roy and Aral (MIT)', ['Buolamwini and Gebru', 'Pariser', 'Wardle and Derakhshan'], 'False stories were about 70% more likely to be retweeted.'),
           ('In March 2022 a deepfake video appeared to show which leader telling soldiers to surrender?', 'Volodymyr Zelenskyy', ['Joe Biden', 'Emmanuel Macron', 'Narendra Modi'], 'It was quickly debunked and removed by platforms.'),
           ('In 2024 an employee of which engineering firm was tricked into transferring about US$25 million after a video call with deepfaked colleagues in Hong Kong?', 'Arup', ['Siemens', 'Boeing', 'Tata Consultancy Services'], 'Arup confirmed the fraud in May 2024.'),
           ('Which term describes genuine private information leaked to cause harm?', 'Malinformation', ['Misinformation', 'Disinformation', 'Satire'], 'From Wardle and Derakhshan\'s information-disorder framework.'),
           ('Days before Slovakia\'s September 2023 election, what kind of deepfake circulated?', 'An audio recording faking a party leader discussing election rigging', ['A fake video of the president resigning', 'A fake image of a bomb', 'A fake newspaper front page'], 'It spread during the pre-election silence period.')],
    why=[('Explain why disinformation spreads effectively on social media.', 'It is designed to be emotional, novel and identity-affirming, which drives engagement; recommendation algorithms amplify engaging content, sharing is instant, and corrections spread more slowly.'),
         ('Explain why deepfakes create a "liar\'s dividend".', 'When people know realistic fakes are possible, those caught on genuine recordings can claim the evidence is fake, so deepfakes undermine trust in all audio-visual evidence, not just in the fakes.'),
         ('Explain why the distinction between misinformation and disinformation matters for interventions.', 'Disinformation involves intent and often coordinated actors, so responses include investigating networks and sanctions; misinformation is shared innocently, so education, labels and friction may be more appropriate.')],
    contrast=[('misinformation', 'disinformation', 'Misinformation is false information shared without intent to deceive (e.g. a relative forwarding a fake cure); disinformation is deliberately created or spread to deceive (e.g. state-run troll campaigns).'),
              ('a deepfake', 'a cheapfake', 'A deepfake is created with AI to synthesise realistic fake media; a cheapfake uses simple editing (slowing, cropping, mislabelling) – e.g. the 2019 slowed-down video of Nancy Pelosi.')],
    misc=[('Deepfakes are mainly used to spread political lies.', 'Research (e.g. Sensity/Deeptrace 2019) found the vast majority of deepfakes online were non-consensual sexual images, mostly of women; political and fraud uses are growing but smaller in number.'),
          ('Only uneducated people believe misinformation.', 'Belief depends on identity, emotion, trust and repetition; highly educated people also share misinformation that fits their views (motivated reasoning).')],
    cases=[('the Zelenskyy deepfake (March 2022)', 'A low-quality deepfake of Ukraine\'s president appearing to tell soldiers to surrender was posted on a hacked Ukrainian news site and social media; Zelenskyy quickly posted a rebuttal and Meta removed it.', 'deepfakes as disinformation in conflict',
            'it showed how synthetic media can be weaponised in war, but also that rapid official rebuttal and platform action can limit its impact.'),
           ('the Arup deepfake fraud (2024)', 'An employee in Arup\'s Hong Kong office joined a video call with what appeared to be the CFO and colleagues – all deepfakes – and transferred about US$25 million to fraudsters.', 'deepfakes and trust in communication',
            'realistic synthetic video defeated normal verification, showing that seeing and hearing are no longer proof of identity.'),
           ('COVID-19 "infodemic"', 'During the pandemic false claims about cures, vaccines and 5G spread widely; the WHO launched campaigns and platforms added labels and removed some content.', 'the impact of misinformation on health',
            'false information contributed to vaccine hesitancy and harmful behaviour, showing that misinformation has real health consequences.')],
    sources=[('"Falsehood diffused significantly farther, faster, deeper, and more broadly than the truth in all categories of information."', 'Vosoughi, Roy and Aral, "The spread of true and false news online", Science, 2018',
              'With reference to the source, explain one implication for platforms.', 'Because false news naturally spreads faster, platforms that optimise for engagement will tend to amplify it unless they add friction, labels or ranking changes.'),
             ('"The danger is not just that people will believe fakes, but that they will stop believing anything."', 'Media researcher commenting on deepfakes, 2023',
              'Explain the concern expressed in the source.', 'The "liar\'s dividend": widespread fakes erode trust in all evidence, letting people dismiss genuine recordings and weakening shared facts needed for democracy.')],
    evaluate=[('Deepfakes are the greatest threat to democratic elections.',
               ['realistic fakes can damage candidates days before votes (Slovakia 2023, Biden robocall 2024)', 'liar\'s dividend undermines trust'],
               ['research on 2024 elections found limited measurable effect of AI fakes', 'cheapfakes, targeted ads and mass misinformation are more common', 'voter suppression and polarisation also threaten elections'],
               'Deepfakes are a serious and growing threat, but so far they are one of several, and not clearly the greatest, threat to elections.'),
              ('Misinformation is mainly a problem caused by technology.',
               ['algorithms amplify engaging falsehoods', 'cheap tools make fakes easy'],
               ['rumours and propaganda long predate the internet', 'demand side: polarisation, low trust and identity', 'political actors deliberately spread it'],
               'Technology amplifies and accelerates misinformation, but its causes are social and political as well as technical.')],
    extended=[('Analyse how one deepfake or disinformation campaign spread and evaluate the responses to it.', 'E.g. Zelenskyy deepfake, Slovakia audio, Biden robocall (New Hampshire, January 2024 – FCC then ruled AI voices in robocalls illegal), Arup fraud; spread mechanisms; responses by platforms, governments, media; effectiveness; judgement.', 8, 'long')],
))
AR('ch02-st1', [
    ('False news spreads faster than true news on Twitter.', 'False stories tend to be more novel and emotionally arousing.', 'a', 'Vosoughi et al. linked faster spread to novelty and emotional response.'),
    ('Most deepfakes found online in early studies were political.', 'Deepfakes are synthetic media made with AI.', 'd', 'Most were non-consensual sexual content; R is true.'),
])


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def moderation_calc(rng, slot):
    kind = rng.choice(['scale', 'appeals'])
    if kind == 'scale':
        posts = rng.choice([50, 200, 500, 1000])  # million per day
        flag = rng.choice([0.1, 0.2, 0.5])  # % flagged for review
        mods = rng.choice([5000, 15000, 40000])
        per = posts * 1e6 * flag / 100 / mods
        secs = 8 * 3600 / per
        stem = (f'A platform receives {posts} million posts a day; {flag}% are flagged for human review. It employs {mods:,} moderators working 8-hour shifts. '
                f'Calculate the number of flagged posts each moderator must review per day, and the average time available per post in seconds.')
        ans = f'{per:,.0f} posts per moderator; about {secs:.1f} s per post'
        key = f'{posts} × 10⁶ × {flag}% = {posts * 1e6 * flag / 100:,.0f} flagged [M1]; ÷ {mods:,} = {per:,.0f} [A1]; 28,800 s ÷ {per:,.0f} = {secs:.1f} s [A1].'
        m = 3
        if slot.d >= 4:
            stem += ' Explain one consequence of this workload for moderators and one for users.'
            ans += '; moderators face stress and trauma from rapid exposure to harmful content (e.g. Kenyan moderators\' lawsuits); users face errors, inconsistent decisions and slow appeals'
            key += ' Moderator well-being [R1]; accuracy/consistency for users [R1].'
            m = 5
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    rem = rng.choice([2_000_000, 5_000_000, 12_000_000])
    app = rng.choice([3, 5, 8])
    rest = rng.choice([10, 20, 30])
    a = rem * app / 100
    r = a * rest / 100
    stem = (f'A platform\'s transparency report states it removed {rem:,} pieces of content for hate speech in a quarter. {app}% of removals were appealed and {rest}% of appeals led to the content being restored. '
            f'Calculate the number of items restored and the restored items as a percentage of all removals.')
    ans = f'{r:,.0f} restored; {pc(r / rem * 100, 2)}% of removals'
    key = f'Appeals = {rem:,} × {app}% = {a:,.0f} [M1]; restored = {a:,.0f} × {rest}% = {r:,.0f} [A1]; {r:,.0f} ÷ {rem:,} × 100 = {pc(r / rem * 100, 2)}% [A1].'
    return dict(stem=stem, answer=ans, markingKey=key + ' (This is a minimum estimate of wrongful removals, because most users do not appeal.)', type='numerical', marks=3)


R.facts('ch02-st2', F(
    terms=[('content moderation', 'the process by which platforms review, remove, restrict or label user content according to their rules and the law'),
           ('community standards', 'a platform\'s rules setting out what users may and may not post'),
           ('Digital Services Act (DSA)', 'the EU regulation, fully applicable from 17 February 2024, that sets duties for online platforms on illegal content, transparency and systemic risks'),
           ('very large online platform (VLOP)', 'under the DSA, a platform with at least 45 million monthly active users in the EU, subject to the strictest duties'),
           ('notice and action', 'a system in which users or authorities notify a platform of illegal content and the platform must act on it'),
           ('Section 230', 'the provision of the US Communications Decency Act (1996) that generally protects platforms from liability for content posted by users'),
           ('Oversight Board', 'an independent body set up by Meta in 2020 to review selected content-moderation decisions')],
    facts=[('What is the maximum fine under the EU Digital Services Act?', '6% of global annual turnover', ['1% of EU turnover', '20% of global turnover', '€1 million'], 'Fines can reach 6% of worldwide annual turnover.'),
           ('What user threshold makes a platform a "very large online platform" under the DSA?', '45 million monthly active users in the EU', ['1 million users worldwide', '450 million users in the EU', '10,000 users'], 'About 10% of the EU population.'),
           ('Which German law (2017) required large social networks to remove "manifestly unlawful" content within 24 hours of a complaint?', 'NetzDG (Network Enforcement Act)', ['GDPR', 'DSA', 'Online Safety Act'], 'Critics worried it encouraged over-removal.'),
           ('In 2019, after the Christchurch mosque attacks were livestreamed, which initiative did New Zealand and France launch?', 'The Christchurch Call', ['The Paris Agreement', 'The Budapest Convention', 'The Tallinn Manual'], 'Governments and companies pledged to eliminate terrorist and violent extremist content online.'),
           ('In December 2023 the European Commission opened its first formal DSA proceedings against which platform?', 'X (formerly Twitter)', ['TikTok', 'Wikipedia', 'Zalando'], 'Concerning illegal content, Community Notes and blue checkmarks.')],
    why=[('Explain why content moderation at scale inevitably makes mistakes.', 'Billions of posts in hundreds of languages must be judged quickly; automated systems miss context (satire, reclaimed slurs) and human moderators have seconds per item, so both wrongful removals and missed harmful content occur.'),
         ('Explain why Section 230 has been important to the growth of the US internet.', 'By protecting platforms from liability for users\' posts while allowing them to moderate in good faith, it let services host user content at scale without reviewing everything first.'),
         ('Explain why the DSA focuses on "systemic risks" rather than individual posts.', 'Very large platforms shape public debate for millions; requiring them to assess and mitigate risks (disinformation, harm to minors, election integrity) and submit to audits targets the design and systems that drive harms, not only individual content decisions.')],
    contrast=[('the EU approach (DSA)', 'the US approach (Section 230)', 'The DSA imposes duties on platforms (notice and action, risk assessments, audits, transparency) with fines up to 6% of turnover; Section 230 gives broad immunity for user content and leaves moderation largely to platforms\' discretion.'),
              ('automated moderation', 'human moderation', 'Automated moderation uses algorithms (hash-matching, classifiers) to handle volume quickly but misses context; human moderation understands nuance but is slow, costly and harmful to moderators\' mental health.')],
    misc=[('Content moderation is just censorship.', 'Moderation includes removing illegal content (child sexual abuse material, terrorist content) and enforcing rules users agree to; it can over-reach, but it is also necessary for safe platforms and is required by law in many countries.'),
          ('AI can now moderate content perfectly without humans.', 'AI misses context, sarcasm and new forms of harm, performs worse in less-resourced languages, and needs human review and appeals.')],
    cases=[('the Christchurch Call (2019)', 'After an attacker livestreamed the Christchurch mosque shootings on Facebook in March 2019, New Zealand and France led governments and tech firms in a pledge to remove terrorist content, including crisis protocols.', 'cooperation to regulate platforms',
            'voluntary multi-stakeholder commitments improved crisis response, but enforcement depends on company goodwill.'),
           ('content moderators in Kenya', 'Moderators employed by Sama in Nairobi to review content for Meta brought legal cases from 2022 over working conditions and psychological harm; Kenyan courts allowed cases against Meta to proceed.', 'the human cost of moderation',
            'the hidden labour of moderation is outsourced to lower-wage countries, raising questions of responsibility and well-being.'),
           ('the DSA case against X', 'In December 2023 the European Commission opened formal proceedings against X under the DSA over illegal content, deceptive blue checkmarks and transparency; in 2024 it issued preliminary findings of breaches.', 'regulation of platforms',
            'the DSA gives the EU tools to investigate and fine very large platforms, testing whether regulation can change platform behaviour.')],
    sources=[('"Very large online platforms shall diligently identify, analyse and assess any systemic risks in the Union stemming from the design or functioning of their service."', 'EU Digital Services Act, Article 34',
              'Explain how this source shows a change in how platforms are regulated.', 'It moves from regulating individual posts to requiring platforms to assess the risks created by their design and systems (e.g. algorithms), making them responsible for structural harms.'),
             ('"We are the first line of defence, and we see the worst of humanity every day for a few dollars an hour."', 'Former content moderator in Nairobi, testimony reported in 2023',
              'Explain one issue raised by the source.', 'Content moderation relies on low-paid workers exposed to traumatic content, raising issues of labour rights, mental health and the outsourcing of platforms\' responsibilities.')],
    evaluate=[('Governments, rather than platforms, should decide what content is removed online.',
               ['democratic legitimacy and legal accountability', 'platforms have commercial interests'],
               ['governments may censor critics (internet shutdowns, blocking)', 'laws differ between countries', 'speed and scale require platform systems'],
               'Democratic laws should define illegal content and oversight (as in the DSA), but day-to-day moderation must be done by platforms under transparency and appeal rules.'),
              ('The Digital Services Act will make social media safer.',
               ['binding duties, audits and large fines', 'researcher data access and transparency'],
               ['enforcement is slow and contested', 'platforms may comply minimally', 'risk of over-removal of lawful speech'],
               'The DSA can improve safety and accountability, but its effect depends on vigorous enforcement and protection of free expression.')],
    extended=[('Compare the EU Digital Services Act and US Section 230 as approaches to regulating platforms, and evaluate which better balances safety and free expression.', 'Compare duties vs immunity, risk assessment, transparency, appeals, fines; examples (X proceedings, TikTok Lite withdrawal 2024, Christchurch); evaluate; judgement.', 8, 'long')],
))

R.facts('ch02-st3', F(
    terms=[('media literacy', 'the ability to access, analyse, evaluate, create and act using all forms of media'),
           ('lateral reading', 'checking a source by leaving it and searching what other reliable sources say about it, as professional fact-checkers do'),
           ('SIFT', 'Mike Caulfield\'s verification method: Stop, Investigate the source, Find better coverage, Trace claims to the original context'),
           ('reverse image search', 'searching with an image to find where else it has appeared online and its original source'),
           ('prebunking', 'warning people in advance about manipulation techniques so they are better able to resist them (inoculation theory)'),
           ('fact-checking', 'verifying the accuracy of claims, often by independent organisations following the International Fact-Checking Network code'),
           ('content provenance', 'information about the origin and edit history of digital content, such as C2PA "Content Credentials"')],
    facts=[('What does the "S" at the start of the SIFT method stand for?', 'Stop', ['Search', 'Share', 'Scan'], 'Stop, Investigate the source, Find better coverage, Trace claims.'),
           ('Which country has repeatedly ranked first in the European Media Literacy Index?', 'Finland', ['France', 'Hungary', 'Portugal'], 'Finland teaches media literacy across its curriculum.'),
           ('Which online game, developed by Cambridge researchers, "inoculates" players by letting them create fake news?', 'Bad News', ['Among Us', 'Papers, Please', 'Wordle'], 'Roozenbeek and van der Linden found it improved resistance to manipulation.'),
           ('Which feature on X (formerly Twitter) lets contributors add context notes to posts?', 'Community Notes', ['Fleets', 'Spaces', 'Blue Check'], 'Notes appear when raters with different views agree they are helpful.')],
    why=[('Explain why lateral reading is more effective than reading a website closely.', 'Misleading sites can look professional and cite sources; checking what independent sources say about the publisher and claim quickly reveals bias or falsehood, as Stanford research on fact-checkers showed.'),
         ('Explain why prebunking can be more effective than debunking.', 'Once misinformation is believed, corrections face resistance and the "continued influence effect"; warning people about techniques beforehand builds resistance across many false claims.'),
         ('Explain why media literacy is described as a responsibility shared by individuals and institutions.', 'Individuals need skills to verify, but schools, platforms (labels, provenance) and news organisations (transparency) shape the environment in which people judge information.')],
    contrast=[('prebunking', 'debunking', 'Prebunking warns people about manipulation techniques before exposure; debunking corrects a specific false claim after it has spread.'),
              ('fact-checking', 'media literacy', 'Fact-checking is professionals verifying specific claims; media literacy is the general set of skills that lets individuals analyse and evaluate media themselves.')],
    misc=[('If a claim appears in many places online, it must be true.', 'Repetition can come from copying the same false source or coordinated campaigns; claims must be traced to an original, reliable source.'),
          ('AI detection tools can reliably tell whether any image is fake.', 'Detection tools produce false positives and negatives and can be fooled; provenance, context and corroboration remain essential.')],
    cases=[('Finland\'s media-literacy education', 'Finland integrated media literacy into its national curriculum and public campaigns after Russian disinformation efforts following 2014; it ranks top in the European Media Literacy Index.', 'education as an intervention against misinformation',
            'a whole-society approach builds long-term resilience rather than relying on removing content.'),
           ('Google and Jigsaw\'s prebunking videos', 'In 2022 Google\'s Jigsaw ran short prebunking adverts in Poland, the Czech Republic and Slovakia about manipulation techniques used against Ukrainian refugees; studies showed improved recognition of the techniques.', 'prebunking at scale',
            'brief videos shown before exposure helped people recognise manipulation, suggesting scalable, content-neutral defences.'),
           ('C2PA Content Credentials', 'The Coalition for Content Provenance and Authenticity (Adobe, Microsoft, the BBC and others) created a standard that attaches tamper-evident information about how content was made and edited.', 'technical verification tools',
            'provenance labels help audiences and journalists verify origin, but only work if widely adopted and preserved by platforms.')],
    sources=[('"Fact-checkers read laterally, leaving a site after a quick scan and opening up new browser tabs to judge the credibility of the original site."', 'Wineburg and McGrew, Stanford History Education Group study, 2017',
              'With reference to the source, explain why lateral reading is an effective verification practice.', 'It uses independent sources to judge a site\'s credibility rather than trusting the site\'s own appearance and claims, which can be misleading.'),
             ('"Inoculating people against misinformation is like a vaccine: a weakened dose of the technique builds resistance."', 'Sander van der Linden, University of Cambridge, 2022',
              'Explain the analogy used in the source.', 'Exposure to a mild, explained example of a manipulation technique (e.g. emotional language, false experts) helps people recognise and resist it later, as a vaccine trains the immune system.')],
    evaluate=[('Media literacy education is the most effective response to misinformation.',
               ['builds long-term resilience across topics (Finland)', 'does not require censorship'],
               ['takes years and reaches mainly students', 'adults and the most exposed may not benefit', 'platform design and amplification also need regulation'],
               'Media literacy is essential and rights-respecting, but it works best combined with platform design changes and regulation.'),
              ('Community-based fact-checking such as Community Notes is better than professional fact-checking.',
               ['scales to many posts and is seen as less biased', 'notes appear only when people with differing views agree'],
               ['slow; many misleading posts never get notes', 'less expertise on complex topics', 'can be manipulated'],
               'Community notes are a useful complement but slower and less expert; they cannot replace professional fact-checking.')],
    extended=[('A viral video claims to show a recent flood in your city. Describe the verification steps you would take and evaluate their limitations.', 'Stop; check uploader/account history; reverse image/keyframe search (InVID); check weather data and local news; geolocate landmarks; check metadata/provenance; limitations: time, re-uploads, AI-generated content, missing metadata; conclusion.', 6, 'long')],
))

P2['ch02'] = dict(
    src=[('"Falsehood diffused significantly farther, faster, deeper, and more broadly than the truth in all categories of information, and the effects were more pronounced for false political news."', 'Vosoughi, Roy and Aral, Science, 2018',
          'Identify two findings reported in {S}.', ['falsehood spread farther, faster, deeper and more broadly than truth', 'effects were strongest for false political news'],
          'Explain why {S} is a valuable source on misinformation.', 'It is a peer-reviewed study in a leading journal based on a very large data set (about 126,000 cascades), so its findings carry authority; however it studied one platform (Twitter, 2006–2017).'),
         ('"We removed the video within hours and labelled re-uploads. Coordinated networks behind such content are taken down as soon as we identify them."', 'Statement by a platform spokesperson about a deepfake of a political leader, 2022',
          'Identify two actions the platform says it took in {S}.', ['removed the video within hours', 'labelled re-uploads / took down coordinated networks'],
          'Explain one reason why {S} should be treated with caution.', 'It is a public-relations statement by the platform about its own performance; it gives no data on how many people saw the content before removal or how many re-uploads were missed.'),
         ('"Those who receive a short prebunking video are significantly better at spotting manipulation techniques such as scapegoating and false dichotomies."', 'Summary of a field experiment on YouTube, Science Advances, 2022',
          'Identify two features of the intervention described in {S}.', ['short prebunking video', 'teaches recognition of manipulation techniques (scapegoating, false dichotomies)'],
          'Explain how {S} suggests a different approach from content removal.', 'It focuses on building users\' skills to resist manipulation before exposure, rather than platforms removing content after it spreads.')],
    cmp=[(0, 1, 'the challenge of misinformation on platforms', ['both show misinformation spreads on platforms and requires a response'],
          ['Source A shows falsehood spreads faster than truth; Source B claims rapid removal limits it', 'A is independent academic research; B is a self-interested company statement']),
         (1, 2, 'responses to misinformation', ['both describe interventions to reduce the impact of misinformation'],
          ['Source B describes removal and labelling (reactive); Source C describes prebunking (proactive)', 'B is a platform claim; C reports experimental evidence'])],
    ev=[(0, 1, 'platforms can effectively control the spread of misinformation.', ['removal and labelling within hours (Source B)', 'DSA duties and fact-checking partnerships'],
         ['falsehood spreads faster than truth (Source A)', 're-uploads and encrypted apps escape moderation', 'self-reported claims are hard to verify']),
        (0, 2, 'educating users is a more effective response to misinformation than moderating content.', ['prebunking improves recognition (Source C)', 'Finland\'s media literacy'],
         ['falsehood spreads too fast for individuals to counter (Source A)', 'education reaches some groups more than others', 'combined approaches needed'])],
)

# =============================================================================================
# ch03 Content 3.6 Artificial intelligence: types and machine learning
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('artificial intelligence (AI)', 'the capability of computer systems to perform tasks that normally require human intelligence, such as recognising speech, making decisions or translating language'),
           ('narrow AI', 'AI designed to perform a specific task, such as playing chess or recognising faces; all current AI is narrow (weak) AI'),
           ('artificial general intelligence (AGI)', 'hypothetical AI that could understand and learn any intellectual task a human can, across domains'),
           ('Turing test', 'a test proposed by Alan Turing (1950) in which a machine passes if a human judge cannot reliably tell its text conversation from a human\'s'),
           ('AI winter', 'a period of reduced funding and interest in AI after expectations were not met, as in the 1970s and late 1980s'),
           ('expert system', 'an AI program that uses a knowledge base of rules from human experts to make decisions, popular in the 1980s (e.g. MYCIN)'),
           ('symbolic AI', 'an approach to AI based on explicit rules and logic written by humans, rather than learning from data')],
    facts=[('In which paper did Alan Turing propose the "imitation game"?', '"Computing Machinery and Intelligence" (1950)', ['"On Computable Numbers" (1936)', '"Attention Is All You Need" (2017)', '"A Logical Calculus of Ideas" (1943)'], 'Published in the journal Mind.'),
           ('At which 1956 workshop was the term "artificial intelligence" adopted as the name of the field?', 'The Dartmouth Summer Research Project', ['The Macy Conferences', 'The Solvay Conference', 'The Bletchley Park meeting'], 'Organised by John McCarthy, Marvin Minsky, Claude Shannon and Nathaniel Rochester.'),
           ('In 1997 which IBM computer defeated world chess champion Garry Kasparov?', 'Deep Blue', ['Watson', 'AlphaZero', 'ENIAC'], 'Deep Blue used massive search rather than learning.'),
           ('In 2016 DeepMind\'s AlphaGo defeated which Go champion 4–1?', 'Lee Sedol', ['Ke Jie', 'Garry Kasparov', 'Fan Hui'], 'Move 37 in game 2 became famous for its creativity.'),
           ('Which 1966 chatbot by Joseph Weizenbaum imitated a psychotherapist?', 'ELIZA', ['SHRDLU', 'Watson', 'Siri'], 'Users attributed understanding to it – the "ELIZA effect".')],
    why=[('Explain why all current AI systems are described as narrow AI.', 'Each system performs well only on the task or type of data it was designed or trained for (e.g. image recognition, text generation) and cannot transfer understanding flexibly to unrelated tasks as humans can.'),
         ('Explain why the Turing test has been criticised as a measure of intelligence.', 'It tests whether a machine can imitate human conversation, not whether it understands; chatbots can pass short conversations by mimicry (the "ELIZA effect"), as Searle\'s Chinese Room argument suggests.'),
         ('Explain why AI has gone through cycles of hype and "AI winters".', 'Researchers made over-optimistic predictions; when systems failed to scale (limited computing power, data and brittle rules), funders such as governments cut support (e.g. after the 1973 Lighthill Report in the UK), until new methods and hardware revived interest.')],
    contrast=[('narrow AI', 'general AI', 'Narrow AI performs specific tasks (translation, playing Go); general AI would match human ability across any intellectual task and does not yet exist.'),
              ('symbolic AI', 'machine learning', 'Symbolic AI uses rules and logic written by humans (expert systems); machine learning lets systems learn patterns from data without being explicitly programmed with rules.')],
    misc=[('ChatGPT is an example of artificial general intelligence.', 'Large language models are powerful but still narrow systems trained to predict text; they lack reliable reasoning, grounded understanding and general competence across all tasks.'),
          ('AI is a recent invention of the 2020s.', 'AI research began in the 1950s (Turing 1950, Dartmouth 1956); recent advances result from more data, computing power (GPUs) and deep learning.')],
    cases=[('Deep Blue v Kasparov (1997)', 'IBM\'s Deep Blue beat Garry Kasparov in a six-game match in 1997, evaluating around 200 million positions per second.', 'narrow AI',
            'the system excelled at chess through brute-force search but could do nothing else, showing the narrowness of AI achievements.'),
           ('AlphaGo v Lee Sedol (2016)', 'DeepMind\'s AlphaGo, combining deep neural networks with reinforcement learning, defeated Lee Sedol 4–1 in Seoul; Lee later retired, saying AI "cannot be defeated".', 'the shift to machine learning',
            'unlike Deep Blue, AlphaGo learned from data and self-play in a game too complex for brute force, marking a turning point in AI.'),
           ('ELIZA (1966)', 'Joseph Weizenbaum\'s ELIZA used simple pattern-matching to respond like a therapist; some users became emotionally attached, which alarmed Weizenbaum.', 'the Turing test and anthropomorphism',
            'people attributed understanding to a simple program, showing that apparent intelligence in conversation can mislead.')],
    sources=[('"I propose to consider the question, \'Can machines think?\'"', 'Alan Turing, "Computing Machinery and Intelligence", Mind, 1950',
              'Explain how Turing proposed to answer the question in the source.', 'He replaced the question with the "imitation game": if a machine\'s text responses cannot be reliably distinguished from a human\'s by an interrogator, it can be said to behave intelligently.'),
             ('"Every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it."', 'Proposal for the Dartmouth Summer Research Project on Artificial Intelligence, 1955',
              'Explain what the source reveals about early expectations of AI.', 'Early researchers were highly optimistic that intelligence could be fully described and simulated, an expectation that later led to disappointment and AI winters.')],
    evaluate=[('Artificial general intelligence is likely to be achieved within the next decade.',
               ['rapid progress of large language models', 'huge investment in compute and talent'],
               ['current systems lack reliable reasoning and grounding', 'history of over-optimistic predictions', 'no agreed definition or test of AGI'],
               'Progress is rapid, but given unresolved limitations and past over-prediction, confident timelines are not justified.'),
              ('The Turing test is still a useful measure of machine intelligence.',
               ['simple, behavioural and influential', 'captures human-like communication ability'],
               ['tests imitation, not understanding (Chinese Room)', 'LLMs can fool people without general intelligence', 'ignores non-linguistic intelligence'],
               'It remains a useful thought experiment about behaviour, but not an adequate measure of intelligence.')],
    extended=[('Compare one example of symbolic AI and one example of machine-learning AI, and evaluate which approach is more significant for digital society today.', 'E.g. MYCIN/expert systems or Deep Blue vs AlphaGo or ChatGPT; compare rules vs learning, transparency, data needs, capabilities; evaluate significance with examples.', 6, 'long')],
))


@R.add('ch03-st2', 'C3', (1, 5), 'numerical')
def confusion(rng, slot):
    task = rng.choice([('detect pneumonia in chest X-rays', 'patients with pneumonia'), ('detect spam emails', 'spam emails'),
                       ('identify diseased crop leaves from photos', 'diseased leaves'), ('flag fraudulent card payments', 'fraudulent payments'),
                       ('recognise a wake word in audio clips', 'clips containing the wake word')])
    tp = rng.randint(30, 90)
    fn = rng.randint(5, 30)
    fp = rng.randint(5, 40)
    tn = rng.randint(100, 400)
    tot = tp + fn + fp + tn
    acc = (tp + tn) / tot * 100
    prec = tp / (tp + fp) * 100
    rec = tp / (tp + fn) * 100
    stem = (f'A supervised machine-learning model is trained to {task[0]}. On a test set of {tot} examples it gives: true positives {tp}, false negatives {fn}, false positives {fp}, true negatives {tn}. ')
    if slot.d <= 2:
        stem += 'Calculate the accuracy.'
        return dict(stem=stem, answer=f'{pc(acc)}%', markingKey=f'({tp} + {tn}) ÷ {tot} × 100 = {pc(acc)}% [M1 A1].', type='numerical', marks=2)
    stem += 'Calculate the accuracy, the precision (TP ÷ (TP + FP)) and the recall (TP ÷ (TP + FN)).'
    ans = f'accuracy {pc(acc)}%, precision {pc(prec)}%, recall {pc(rec)}%'
    key = f'Accuracy ({tp}+{tn})/{tot} = {pc(acc)}% [A1]; precision {tp}/({tp}+{fp}) = {pc(prec)}% [A1]; recall {tp}/({tp}+{fn}) = {pc(rec)}% [A1].'
    m = 3
    if slot.d >= 4:
        stem += f' For this use, explain whether false negatives or false positives are more serious.'
        ans += f'; e.g. for {task[1]}, missed cases (false negatives) usually matter more where harm from missing is high (medical, fraud), whereas false positives matter more if wrongly flagged cases are punished or annoy users'
        key += ' Justified judgement on error costs in context [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


@R.add('ch03-st2', 'C3', (2, 5), 'numerical')
def knn(rng, slot):
    feats = rng.choice([('hours of screen time', 'hours of sleep', 'tired', 'rested'), ('number of links', 'number of capital-letter words', 'spam', 'not spam'),
                        ('fruit weight (100 g)', 'colour score', 'orange', 'lemon'), ('daily steps (thousands)', 'resting heart rate (tens)', 'active', 'inactive')])
    pts = []
    labs = []
    for _ in range(5):
        p = (rng.randint(1, 9), rng.randint(1, 9))
        if p in pts:
            return None
        pts.append(p)
        labs.append(rng.choice([feats[2], feats[3]]))
    if len(set(labs)) < 2:
        return None
    q = (rng.randint(1, 9), rng.randint(1, 9))
    if q in pts:
        return None
    d = [((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5 for p in pts]
    order = sorted(range(5), key=lambda i: d[i])
    if abs(d[order[2]] - d[order[3]]) < 1e-9 or abs(d[order[0]] - d[order[1]]) < 1e-9:
        return None
    k = 3 if slot.d >= 3 else 1
    near = [labs[i] for i in order[:k]]
    pred = max(set(near), key=near.count)
    tbl = '\n'.join(f'P{i + 1} ({p[0]}, {p[1]}): {l}' for i, (p, l) in enumerate(zip(pts, labs)))
    stem = (f'A classifier uses two features ({feats[0]}, {feats[1]}). Labelled training points:\n{tbl}\n'
            f'Using k-nearest neighbours with k = {k} and straight-line (Euclidean) distance, classify the new point ({q[0]}, {q[1]}).')
    dist_txt = '; '.join(f'P{i + 1} {d[i]:.2f}' for i in order[:k])
    ans = f'{pred} (nearest: {dist_txt})'
    key = f'Distances: ' + ', '.join(f'P{i + 1} = {d[i]:.2f}' for i in range(5)) + f' [M1]; {k} nearest: ' + ', '.join(f'P{i + 1} ({labs[i]})' for i in order[:k]) + f' [A1]; majority → {pred} [A1].'
    m = 3
    if slot.d >= 5:
        stem += ' Explain why the choice of training data affects the fairness of such a classifier.'
        ans += '; predictions copy the labels of similar past examples, so unrepresentative or biased labels are reproduced for new cases'
        key += ' Model reproduces patterns/labels in training data; under-represented groups classified less accurately [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch03-st2', F(
    terms=[('machine learning', 'a branch of AI in which systems learn patterns from data to make predictions or decisions without being explicitly programmed with rules'),
           ('supervised learning', 'machine learning from labelled examples (inputs paired with correct outputs), used for classification and prediction'),
           ('unsupervised learning', 'machine learning that finds patterns or groups (clusters) in unlabelled data'),
           ('reinforcement learning', 'machine learning in which an agent learns by trial and error, receiving rewards or penalties for its actions'),
           ('training data', 'the data set used to teach a machine-learning model'),
           ('overfitting', 'when a model learns the training data too closely, including noise, and performs poorly on new data'),
           ('label', 'the correct answer attached to a training example, such as "spam" or "not spam"'),
           ('test set', 'data held back from training and used to evaluate how well a model performs on unseen examples')],
    facts=[('Which type of machine learning uses labelled examples?', 'Supervised learning', ['Unsupervised learning', 'Reinforcement learning', 'Symbolic reasoning'], 'Each training input has a known correct output.'),
           ('Grouping customers into segments by purchasing behaviour without predefined labels is an example of what?', 'Unsupervised learning (clustering)', ['Supervised learning', 'Reinforcement learning', 'An expert system'], 'e.g. k-means clustering.'),
           ('Which type of learning did AlphaGo Zero use to improve by playing millions of games against itself?', 'Reinforcement learning', ['Unsupervised clustering', 'Supervised learning from human labels only', 'Rule-based expert systems'], 'Rewards came from winning games.'),
           ('ImageNet, a data set of millions of labelled images, was largely labelled by whom?', 'Crowdworkers on Amazon Mechanical Turk', ['Medical doctors', 'Robots', 'Professional photographers'], 'Fei-Fei Li\'s team used crowdsourcing; such hidden labour is central to ML.'),
           ('Why is data split into training and test sets?', 'To evaluate the model on examples it has not seen', ['To make training faster only', 'To double the amount of data', 'To remove all bias'], 'Testing on unseen data reveals overfitting.')],
    why=[('Explain why the quality of training data determines the quality of a machine-learning model.', 'The model can only learn patterns present in its data; if data is incomplete, unrepresentative, wrongly labelled or historically biased, the model reproduces these flaws ("garbage in, garbage out").'),
         ('Explain why reinforcement learning is suited to games and robotics.', 'These tasks have clear goals and feedback (winning, reaching a target), so an agent can try actions, receive rewards and improve over many trials, often in simulation.'),
         ('Explain why machine learning depends on hidden human labour.', 'Data must be collected and labelled by people – often low-paid crowdworkers or outsourced workers (e.g. labelling images or toxic text) – so AI systems rely on human judgement and work that is rarely visible.')],
    contrast=[('supervised learning', 'unsupervised learning', 'Supervised learning trains on labelled examples to predict known categories or values; unsupervised learning finds structure or clusters in unlabelled data without predefined answers.'),
              ('training data', 'test data', 'Training data is used to fit the model\'s parameters; test data is kept separate to measure how well the model generalises to new examples.')],
    misc=[('A machine-learning model that is 99% accurate on its training data will work well in the real world.', 'High training accuracy may mean overfitting; performance must be measured on unseen test data and real-world conditions, which often differ (data drift).'),
          ('Machine learning systems understand what they learn.', 'They detect statistical patterns linking inputs to outputs; they can be fooled by small changes (adversarial examples) and do not understand meaning as humans do.')],
    cases=[('ImageNet and AlexNet (2012)', 'ImageNet, a data set of over 14 million labelled images, enabled the 2012 AlexNet deep-learning model to cut image-recognition error dramatically in the ImageNet challenge.', 'the role of training data in machine learning',
            'large labelled data sets combined with GPUs triggered the deep-learning boom, showing data as the fuel of machine learning.'),
           ('AlphaGo Zero (2017)', 'DeepMind\'s AlphaGo Zero learned Go only by playing against itself with reinforcement learning and surpassed the version that beat Lee Sedol within days.', 'reinforcement learning',
            'learning from rewards rather than human examples produced superhuman play, showing a different route to machine learning.'),
           ('data labelling in Kenya for ChatGPT', 'In 2023 TIME reported that workers in Kenya employed via Sama were paid less than US$2 an hour to label toxic text to make ChatGPT safer.', 'the human labour behind supervised learning',
            'AI safety relied on low-paid workers exposed to disturbing content, raising ethical questions about global AI supply chains.')],
    sources=[('"Data is to machine learning what fuel is to an engine: without enough of the right kind, nothing moves."', 'Andrew Ng, AI researcher, paraphrase of a 2018 lecture',
              'Explain what the source suggests about machine learning.', 'Machine-learning performance depends on large quantities of relevant, high-quality data; the algorithm alone cannot compensate for poor or insufficient data.'),
             ('"The workers were paid between $1.32 and $2 an hour to read and label graphic descriptions of violence and abuse."', 'TIME magazine investigation into data labelling for OpenAI, January 2023',
              'Explain one ethical issue raised by the source.', 'AI development relies on low-paid workers in the Global South exposed to traumatic content, raising issues of fair pay, mental health and exploitation in AI supply chains.')],
    evaluate=[('Supervised learning is more useful for society than unsupervised learning.',
               ['powers medical diagnosis, translation, spam filtering', 'performance can be measured against labels'],
               ['labelling is costly and can embed human bias', 'unsupervised methods find unknown patterns (fraud, genetics)', 'many advanced systems combine both (self-supervised pre-training)'],
               'Supervised learning drives many practical applications, but unsupervised and self-supervised methods are increasingly important; usefulness depends on the problem.'),
              ('More training data always makes a machine-learning model better.',
               ['more examples improve generalisation', 'large data sets enabled deep learning breakthroughs'],
               ['biased or low-quality data at scale amplifies harms', 'privacy and copyright problems', 'diminishing returns and higher energy costs'],
               'More data helps only if it is relevant, representative and lawfully obtained; quality matters as much as quantity.')],
    extended=[('A hospital wants to use machine learning to detect skin cancer from photos. Explain how the model would be trained and evaluated, and evaluate the risks for different patient groups.', 'Supervised learning on labelled images; train/test split; metrics (accuracy, recall); risk: training data mostly lighter skin → lower accuracy for darker skin (documented in dermatology data sets); need for diverse data, validation and clinician oversight; judgement.', 8, 'long')],
))
AR('ch03-st2', [
    ('A model can perform well on its training data but badly on new data.', 'Overfitting occurs when a model learns noise in the training data rather than general patterns.', 'a', 'Overfitting explains the gap.'),
    ('Unsupervised learning requires every training example to be labelled.', 'Unsupervised learning finds clusters or patterns in data.', 'd', 'Unsupervised learning uses unlabelled data; A is false.'),
])


@R.add('ch03-st3', 'C3', (1, 5), 'numerical')
def perceptron(rng, slot):
    n = 3 if slot.d >= 3 else 2
    xs = [rng.choice([0, 1]) for _ in range(n)]
    ws = [rng.choice([-1.0, -0.5, 0.3, 0.5, 0.8, 1.2]) for _ in range(n)]
    th = rng.choice([0.5, 0.7, 1.0])
    s = round(sum(x * w for x, w in zip(xs, ws)), 2)
    out = 1 if s >= th else 0
    ctx = rng.choice(['whether to recommend a video', 'whether an email is spam', 'whether a photo contains a cat', 'whether to approve an automatic reply'])
    stem = (f'A single artificial neuron (perceptron) decides {ctx}. Inputs: ' + ', '.join(f'x{i + 1} = {x}' for i, x in enumerate(xs)) +
            '; weights: ' + ', '.join(f'w{i + 1} = {w:g}' for i, w in enumerate(ws)) + f'. It outputs 1 if the weighted sum ≥ {th:g}, otherwise 0. Calculate the weighted sum and the output.')
    ans = f'sum = {s:g}; output {out}'
    key = 'Weighted sum = ' + ' + '.join(f'{x}×({w:g})' if w < 0 else f'{x}×{w:g}' for x, w in zip(xs, ws)) + f' = {s:g} [M1 A1]; {"≥" if out else "<"} {th:g} → output {out} [A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain what happens to the weights during training.'
        ans += '; weights are adjusted to reduce error between the output and the correct label (e.g. by the perceptron rule / backpropagation in deep networks)'
        key += ' Training adjusts weights in proportion to error over many examples [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch03-st3', F(
    terms=[('artificial neural network', 'a machine-learning model made of layers of connected artificial neurons whose weighted connections are adjusted during training'),
           ('deep learning', 'machine learning using neural networks with many layers, which can learn complex features from large data sets'),
           ('generative AI', 'AI that produces new content – text, images, audio, video or code – from patterns learned in training data'),
           ('large language model (LLM)', 'a deep-learning model trained on vast amounts of text to predict the next token, used to generate and summarise language (e.g. GPT, Claude, Gemini)'),
           ('hallucination', 'when a generative AI system produces fluent but false or fabricated output, such as invented citations'),
           ('transformer', 'a neural-network architecture based on "attention", introduced in the 2017 paper "Attention Is All You Need", which underlies most LLMs'),
           ('diffusion model', 'a generative model that creates images by learning to remove noise step by step, used in tools such as Stable Diffusion'),
           ('prompt', 'the input text or instruction given to a generative AI model')],
    facts=[('Which 2017 paper introduced the transformer architecture?', '"Attention Is All You Need"', ['"Computing Machinery and Intelligence"', '"ImageNet Classification with Deep CNNs"', '"Playing Atari with Deep RL"'], 'By Vaswani and colleagues at Google.'),
           ('When was ChatGPT released to the public?', 'November 2022', ['January 2019', 'June 2024', 'March 2016'], 'It reached an estimated 100 million users in about two months.'),
           ('Which of the following is an example of an LLM hallucination?', 'A chatbot inventing a court case that does not exist', ['A chatbot refusing an unsafe request', 'A chatbot translating correctly', 'A chatbot answering slowly'], 'In Mata v. Avianca (2023) lawyers were sanctioned for citing fake cases produced by ChatGPT.'),
           ('Who built the perceptron, an early artificial neuron, in 1958?', 'Frank Rosenblatt', ['Geoffrey Hinton', 'Alan Turing', 'Yann LeCun'], 'The Mark I Perceptron learned to classify simple images.')],
    why=[('Explain why large language models can produce confident but false answers.', 'They generate the statistically most likely continuation of text based on training patterns, not by checking facts against a source of truth, so fluent output can be fabricated (hallucination).'),
         ('Explain why deep learning needs large amounts of data and computing power.', 'Deep networks have millions or billions of parameters that must be adjusted through many passes over large data sets, requiring powerful GPUs and energy.'),
         ('Explain why generative AI raises new questions about trust in information.', 'It can cheaply produce realistic text, images, voices and video at scale, making it harder to know whether content is authentic or accurate and enabling misinformation and fraud.')],
    contrast=[('discriminative (predictive) AI', 'generative AI', 'Discriminative AI classifies or predicts from inputs (e.g. is this email spam?); generative AI creates new content resembling its training data (e.g. writing an email).'),
              ('a shallow neural network', 'a deep neural network', 'A shallow network has one or few hidden layers and learns simple patterns; a deep network has many layers that learn increasingly abstract features (edges → shapes → objects).')],
    misc=[('Neural networks work exactly like the human brain.', 'They are loosely inspired by neurons, but are mathematical functions with adjustable weights trained by optimisation; brains work very differently and are far more energy-efficient.'),
          ('Generative AI copies and pastes from its training data.', 'Models learn statistical patterns and generate new combinations; however, they can sometimes reproduce training data closely (memorisation), which raises copyright concerns.')],
    cases=[('ChatGPT (2022)', 'OpenAI released ChatGPT in November 2022; it reached an estimated 100 million users within about two months, prompting rapid adoption in schools and workplaces and policy responses.', 'generative AI and change',
            'a single release triggered rapid changes in education, work and regulation, showing the speed of diffusion of generative AI.'),
           ('Mata v. Avianca (2023)', 'Lawyers in New York submitted a brief citing six non-existent cases generated by ChatGPT; the judge sanctioned them.', 'hallucination',
            'fluent AI output was mistaken for reliable research, showing the need for verification when using LLMs.'),
           ('AlexNet (2012)', 'A deep convolutional neural network by Krizhevsky, Sutskever and Hinton, trained on GPUs, won the ImageNet competition by a large margin.', 'the rise of deep learning',
            'the result showed that deep networks plus big data and GPUs outperform earlier approaches, launching the modern AI boom.')],
    sources=[('"The judge found that the cases cited did not exist and imposed sanctions on the attorneys."', 'Summary of Mata v. Avianca, US District Court for the Southern District of New York, June 2023',
              'With reference to the source, explain one risk of using generative AI for research.', 'LLMs can fabricate plausible citations (hallucination); relying on them without checking can lead to serious professional and legal consequences.'),
             ('"ChatGPT is a blurry JPEG of the web."', 'Ted Chiang, The New Yorker, February 2023',
              'Explain the metaphor used in the source.', 'Like lossy compression, an LLM stores a compressed approximation of its training text; it reproduces the gist but can fill gaps with plausible but wrong details.')],
    evaluate=[('Generative AI will do more good than harm for education.',
               ['personalised tutoring and feedback at scale', 'support for language learners and students with disabilities'],
               ['academic integrity and over-reliance', 'hallucinations and bias', 'unequal access and data-privacy concerns'],
               'Generative AI can benefit education if used with clear guidance, teacher oversight and AI literacy; without these, harms may dominate.'),
              ('Deep learning has made AI more powerful but less trustworthy.',
               ['huge gains in perception and language', 'opaque models (black box)', 'hallucinations and adversarial vulnerability'],
               ['explainability tools and evaluation are improving', 'older rule-based systems were brittle in other ways', 'trust depends on governance, not only technique'],
               'Deep learning increased capability and opacity together; trustworthiness depends on testing, transparency and oversight.')],
    extended=[('Explain how a large language model generates text, and evaluate its impact on one profession.', 'Training on large text corpora; tokens; next-token prediction with a transformer; fine-tuning/RLHF; hallucination; impact on e.g. journalism, law, teaching, programming; benefits and risks; judgement.', 8, 'long')],
))

# =============================================================================================
# ch04 Content 3.6 AI: ethical, social and economic impacts
# =============================================================================================
@R.add('ch04-st1', 'C3', (2, 5), 'numerical')
def fairness_metrics(rng, slot):
    dom = rng.choice([('a hiring model that shortlists applicants', 'shortlisted', 'qualified applicants'),
                      ('a credit model that approves loans', 'approved', 'applicants who would repay'),
                      ('a predictive policing tool that flags people', 'flagged', 'people who did not offend')])
    ga, gb = rng.choice([('women', 'men'), ('group X', 'group Y'), ('applicants from rural areas', 'applicants from cities')])
    na, nb = rng.choice([200, 300, 400]), rng.choice([200, 300, 400])
    sa, sb = rng.randint(int(na * 0.2), int(na * 0.45)), rng.randint(int(nb * 0.3), int(nb * 0.6))
    ra, rb = sa / na * 100, sb / nb * 100
    stem = (f'An audit of {dom[0]} finds that {sa} of {na} {ga} and {sb} of {nb} {gb} were {dom[1]}. '
            f'Calculate the rate for each group and the difference in percentage points (a test of demographic parity).')
    ans = f'{ga} {pc(ra)}%, {gb} {pc(rb)}%; difference {pc(abs(ra - rb))} percentage points'
    key = f'{sa}/{na} = {pc(ra)}% [A1]; {sb}/{nb} = {pc(rb)}% [A1]; |{pc(ra)} − {pc(rb)}| = {pc(abs(ra - rb))} pp [A1].'
    m = 3
    if slot.d >= 4:
        stem += (f' Explain why equal rates (demographic parity) might not be the only fairness test, referring to "equal opportunity" (equal rates among {dom[2]}).')
        ans += f'; groups may differ in base rates, so parity may conflict with equal error rates; equal opportunity checks whether {dom[2]} are treated equally – different fairness definitions can conflict (as in the COMPAS debate)'
        key += ' Different fairness metrics (parity, equal opportunity, calibration) cannot all be satisfied when base rates differ; choice is a value judgement [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch04-st1', F(
    terms=[('AI bias', 'systematic unfairness in an AI system\'s outputs that disadvantages particular groups, arising from data, design or deployment'),
           ('fairness (in AI)', 'the principle that AI decisions should not unjustly disadvantage individuals or groups; it can be defined in several, sometimes conflicting, ways'),
           ('demographic parity', 'a fairness criterion requiring that different groups receive positive outcomes at equal rates'),
           ('equal opportunity (fairness)', 'a fairness criterion requiring equal true positive rates across groups – qualified people in each group are equally likely to be selected'),
           ('high-stakes decision', 'a decision with significant effects on a person\'s life, such as hiring, credit, policing, healthcare or immigration'),
           ('automation bias', 'the tendency of people to over-trust and defer to automated recommendations, even when they are wrong')],
    facts=[('Which 2019 study in Science found that a US healthcare algorithm underestimated the needs of Black patients because it used past healthcare costs as a proxy for need?', 'Obermeyer et al.', ['Buolamwini and Gebru', 'Vosoughi et al.', 'Frey and Osborne'], 'Fixing the proxy would have greatly increased the share of Black patients flagged for extra care.'),
           ('In 2020 Robert Williams was wrongly arrested in Detroit because of what?', 'A false match by facial-recognition software', ['A hacked email', 'A deepfake video', 'A credit-scoring error'], 'One of the first documented wrongful arrests from facial recognition in the US.'),
           ('Which US city banned police use of facial recognition in 2019, the first major city to do so?', 'San Francisco', ['New York', 'Chicago', 'Houston'], 'Several other cities followed.'),
           ('What is "automation bias"?', 'Over-trusting automated recommendations even when they are wrong', ['Bias in favour of robots in hiring', 'An algorithm\'s preference for automation', 'Bias caused by slow computers'], 'It weakens human oversight.')],
    why=[('Explain why using a proxy variable can make an AI system biased.', 'A proxy stands in for what we want to measure (e.g. healthcare spending for health need) but may reflect unequal access or past discrimination; the model then disadvantages groups for whom the proxy is systematically lower, as Obermeyer et al. found.'),
         ('Explain why different definitions of fairness can conflict.', 'When groups have different base rates, a system cannot simultaneously give equal selection rates, equal error rates and equal calibration; choosing which to prioritise is an ethical and political judgement, not a technical one.'),
         ('Explain why AI bias in high-stakes decisions is particularly concerning.', 'Errors affect people\'s liberty, livelihoods and health, are applied at scale, are hard for individuals to detect or challenge, and can reinforce historical inequalities.')],
    contrast=[('demographic parity', 'equal opportunity', 'Demographic parity requires equal selection rates across groups; equal opportunity requires that equally qualified people in each group have equal chances of selection (equal true positive rates).'),
              ('bias in data', 'bias in deployment', 'Bias in data comes from unrepresentative or historically unequal training data; bias in deployment comes from how a system is used – e.g. in which neighbourhoods, by whom, or with what level of human oversight.')],
    misc=[('Human oversight always prevents AI bias.', 'Automation bias means reviewers often accept AI outputs uncritically; oversight must be meaningful, informed and empowered to override.'),
          ('An AI system that is equally accurate for all groups is fair.', 'Equal overall accuracy can hide unequal types of error (false positives vs negatives) and unequal consequences; fairness also depends on how outputs are used.')],
    cases=[('the Obermeyer healthcare algorithm study (2019)', 'Researchers found a widely used US algorithm assigned Black patients the same risk score as white patients who were in fact healthier, because it predicted healthcare costs, which are lower for Black patients due to unequal access.', 'proxy bias in AI',
            'a seemingly neutral target variable embedded structural inequality in a high-stakes health decision.'),
           ('the wrongful arrest of Robert Williams (2020)', 'Detroit police arrested Robert Williams after facial-recognition software matched his driving-licence photo to blurry CCTV footage; the charges were dropped and a 2024 settlement limited police use of the technology.', 'AI bias and automation bias in policing',
            'officers relied on an algorithmic match without sufficient checks, and facial recognition is known to be less accurate for darker-skinned people.'),
           ('Amazon\'s abandoned recruiting tool', 'Reuters reported in 2018 that Amazon scrapped an AI tool that downgraded CVs containing the word "women\'s", having been trained on mostly male applicants\' CVs.', 'bias in hiring algorithms',
            'the model learned historical patterns of a male-dominated workforce and reproduced them.')],
    sources=[('"The algorithm was not designed to be racist. It was designed to predict costs, and in a system where less is spent on Black patients, cost became a biased measure of need."', 'Summary of findings by Ziad Obermeyer and colleagues, Science, 2019',
              'With reference to the source, explain how AI can be biased without discriminatory intent.', 'The developers chose a target (cost) that seemed neutral but reflected unequal spending; the model learned that pattern, so the outcome was biased even without intent.'),
             ('"I never thought I would have to explain to my daughters why Daddy got arrested… because a computer got it wrong."', 'Robert Williams, Washington Post op-ed, 2020',
              'Explain one impact of AI bias illustrated by the source.', 'A false facial-recognition match led to wrongful arrest, causing personal, family and psychological harm and undermining trust in police and technology.')],
    evaluate=[('AI should not be used in high-stakes decisions about people.',
               ['documented bias (Obermeyer, Williams)', 'opacity and difficulty of appeal', 'automation bias weakens oversight'],
               ['human decisions are also biased and inconsistent', 'well-audited AI can reduce some disparities', 'EU AI Act allows high-risk uses under strict conditions'],
               'AI can be used in high-stakes decisions only with strict safeguards – audits, transparency, meaningful human review and a right to contest; otherwise it should not be used.'),
              ('AI bias is a technical problem that can be solved with better algorithms.',
               ['fairness-aware algorithms and debiasing techniques exist', 'better data collection reduces errors'],
               ['fairness definitions conflict and require value choices', 'structural inequality in society shapes data', 'deployment and power relations matter'],
               'Technical fixes help, but AI bias is fundamentally socio-technical and requires ethical, legal and institutional responses.')],
    extended=[('Evaluate the use of facial recognition by police, with reference to bias and fairness.', 'Accuracy differences (Gender Shades, NIST 2019 demographic study); wrongful arrests (Williams, Detroit); benefits (finding suspects, missing persons); bans (San Francisco 2019) and EU AI Act limits; judgement.', 8, 'long')],
))


@R.add('ch04-st2', 'C3', (1, 5), 'numerical')
def automation_jobs(rng, slot):
    sector = rng.choice([('customer-service agents', 'a call-centre company'), ('warehouse pickers', 'a logistics firm'),
                         ('paralegals', 'a law firm'), ('translators', 'a translation agency'), ('bank tellers', 'a retail bank')])
    n = rng.choice([400, 1200, 2500, 6000])
    auto = rng.choice([15, 20, 30, 40])
    new = rng.choice([5, 8, 10, 12])
    lost = n * auto // 100
    created = n * new // 100
    net = created - lost
    stem = (f'{sector[1][0].upper() + sector[1][1:]} employs {n:,} {sector[0]}. It expects AI to automate {auto}% of these roles within five years, while creating new roles equal to {new}% of the current workforce. '
            f'Calculate the jobs lost, the jobs created and the net change.')
    ans = f'{lost:,} lost, {created:,} created, net change {net:+,}'
    key = f'{auto}% × {n:,} = {lost:,} [A1]; {new}% × {n:,} = {created:,} [A1]; {created:,} − {lost:,} = {net:+,} [A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain why the net figure may hide important impacts on workers.'
        ans += '; new jobs may need different skills, be in different places or pay differently, so displaced workers may not get them without retraining'
        key += ' Skills mismatch, location, wages, who gains vs loses [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch04-st2', F(
    terms=[('automation', 'using machines or software to perform tasks previously done by humans'),
           ('job displacement', 'the loss of jobs when tasks are automated or reorganised'),
           ('augmentation', 'using AI to assist and enhance human work rather than replace it'),
           ('reskilling', 'training workers in new skills so they can move into different roles'),
           ('upskilling', 'improving workers\' skills within their current field, for example learning to work with AI tools'),
           ('task-based approach', 'analysing automation by the tasks within jobs rather than whole jobs, since most jobs include tasks with different levels of exposure')],
    facts=[('Frey and Osborne (2013) estimated what share of US jobs were at high risk of computerisation?', 'About 47%', ['About 5%', 'About 90%', 'About 14%'], 'Later OECD studies using a task-based approach estimated about 14% across OECD countries.'),
           ('According to the IMF (January 2024), about what share of global employment is exposed to AI?', 'Almost 40%', ['About 5%', 'About 90%', 'Exactly 50%'], 'About 60% in advanced economies.'),
           ('Which 2023 strike won limits on the use of AI in writing film and TV scripts?', 'The Writers Guild of America strike', ['The UK rail strike', 'The French pension strike', 'The Amazon warehouse strike'], 'The agreement said AI cannot be credited as a writer.'),
           ('Which approach analyses which tasks within jobs can be automated rather than whole occupations?', 'The task-based approach', ['The jobs-replacement model', 'The Luddite model', 'The Turing approach'], 'It produces lower estimates of jobs fully automated.')],
    why=[('Explain why estimates of jobs lost to AI vary so widely.', 'Studies use different methods (whole occupations vs tasks), assumptions about adoption speed, costs and regulation, and whether new jobs and augmentation are counted, so estimates range from about 14% to 47% of jobs.'),
         ('Explain why generative AI affects different workers from earlier automation.', 'Earlier automation mainly replaced routine manual tasks (factories), while generative AI affects cognitive, creative and white-collar tasks such as writing, coding, translation and customer service.'),
         ('Explain why AI may increase inequality between workers.', 'Workers with skills that complement AI (and owners of AI capital) may see productivity and pay rise, while those doing automatable tasks may lose jobs or bargaining power, widening gaps.')],
    contrast=[('automation', 'augmentation', 'Automation replaces humans in tasks; augmentation uses AI to support humans, making them more productive (e.g. AI-assisted coding).'),
              ('reskilling', 'upskilling', 'Reskilling trains workers for different roles (a cashier becoming a data technician); upskilling improves skills in their current role (a journalist learning AI-assisted research).')],
    misc=[('AI will replace all jobs.', 'AI automates tasks rather than whole jobs in most cases; history shows technology also creates new jobs, though transitions can be painful and unequal.'),
          ('Only low-skilled jobs are threatened by AI.', 'Generative AI is highly exposed to tasks in professional work – writing, legal research, coding, design – so many high-skilled roles are affected.')],
    cases=[('the 2023 WGA strike', 'Hollywood writers struck for 148 days in 2023; the agreement stated that AI cannot write or rewrite literary material and that writers cannot be required to use AI.', 'workers responding to AI at work',
            'collective bargaining set rules on AI use, showing workers can shape how automation is adopted.'),
           ('Klarna\'s AI customer-service assistant (2024)', 'Swedish fintech Klarna said in 2024 its AI assistant was doing work equivalent to about 700 full-time agents; in 2025 it said it would hire more humans again to protect quality.', 'automation and job displacement',
            'AI replaced many customer-service tasks, but the later reversal showed limits of automation and the value of human service.'),
           ('a study of AI in customer support (Brynjolfsson et al., 2023)', 'Research on a generative-AI assistant for call-centre workers found productivity rose by about 14% on average, with the biggest gains for less experienced workers.', 'augmentation',
            'AI acted as a tool that raised the productivity of novice workers, narrowing skill gaps rather than replacing workers.')],
    sources=[('"AI will affect almost 40 percent of jobs around the world, replacing some and complementing others."', 'Kristalina Georgieva, Managing Director of the IMF, January 2024',
              'With reference to the source, explain the two different effects of AI on jobs.', 'Replacement – some jobs or tasks are automated, causing displacement; complementing – AI augments workers, raising productivity and possibly wages.'),
             ('"AI can\'t write or rewrite literary material, and AI-generated material will not be considered source material."', 'Summary of the WGA Minimum Basic Agreement, 2023',
              'Explain how this source shows workers shaping technological change.', 'Through collective bargaining, writers set limits on how studios use AI, protecting credit and pay rather than accepting automation on employers\' terms.')],
    evaluate=[('AI will create more jobs than it destroys.',
               ['historically, technology created new occupations', 'new AI-related roles and productivity growth'],
               ['generative AI affects a broad range of cognitive work quickly', 'new jobs may require skills displaced workers lack', 'gains may go to capital owners'],
               'AI may create as many jobs as it destroys in the long run, but transitions will be uneven and painful without reskilling and social protection.'),
              ('Governments should slow down the adoption of AI to protect jobs.',
               ['gives time for reskilling and social protection', 'protects vulnerable communities'],
               ['slowing adoption may reduce productivity and competitiveness', 'better to manage transitions than block innovation', 'hard to enforce globally'],
               'Rather than slowing adoption, governments should invest in reskilling, social safety nets and worker voice in how AI is introduced.')],
    extended=[('Analyse the likely impact of generative AI on one occupation and evaluate one intervention to support affected workers.', 'Occupation (translators, customer service, coders, illustrators); tasks automated vs augmented; evidence; interventions (reskilling programmes, collective agreements, Singapore SkillsFuture, universal basic income trials); judgement.', 8, 'long')],
))


@R.add('ch04-st3', 'C3', (2, 5), 'numerical')
def ai_act_fine(rng, slot):
    turn = rng.choice([80, 300, 900, 2400, 60000, 240000])  # € million
    tier = rng.choice([('a prohibited practice (e.g. social scoring)', 35, 7), ('breaching obligations for high-risk systems', 15, 3), ('supplying incorrect information to regulators', 7.5, 1)])
    pct = turn * tier[2] / 100
    mx = max(tier[1], pct)
    stem = (f'Under the EU AI Act, fines for {tier[0]} can reach €{tier[1]:g} million or {tier[2]}% of worldwide annual turnover, whichever is higher. '
            f'A company has a turnover of €{turn:,} million. Calculate the maximum fine.')
    ans = f'€{mx:,.1f} million'.replace('.0 million', ' million')
    key = f'{tier[2]}% × €{turn:,}m = €{pct:,.1f}m [M1]; compare with €{tier[1]:g}m → {ans} [A1].'
    m = 2
    if slot.d >= 4:
        stem += ' Explain why the Act has different fine levels.'
        ans += '; penalties are proportionate to the seriousness of the breach in a risk-based system – banned practices carry the highest'
        key += ' Proportionality / risk-based approach [R1 R1]. (SMEs pay the lower of the two amounts.)'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch04-st3', F(
    terms=[('AI governance', 'the laws, standards, institutions and practices that guide how AI is developed and used'),
           ('risk-based regulation', 'regulation that sets stricter rules for uses with greater potential harm, as in the EU AI Act'),
           ('general-purpose AI model', 'under the EU AI Act, an AI model (such as a large language model) that can perform a wide range of tasks and be integrated into many systems'),
           ('AI ethics principles', 'high-level values such as fairness, transparency, accountability, privacy and human oversight adopted by organisations and governments (e.g. OECD AI Principles, 2019)'),
           ('conformity assessment', 'the process of checking that a high-risk AI system meets legal requirements before it is placed on the market'),
           ('AI safety institute', 'a government body that tests and evaluates advanced AI models, such as the UK AI Safety Institute (2023)')],
    facts=[('On what date did the EU AI Act enter into force?', '1 August 2024', ['25 May 2018', '17 February 2024', '1 January 2030'], 'Its provisions apply in phases from 2025 to 2027.'),
           ('Which of these is classified as "high-risk" under the EU AI Act?', 'AI used to screen job applicants', ['Spam filters', 'AI in video games', 'A music recommendation system'], 'Employment is a listed high-risk area.'),
           ('Which country hosted the first global AI Safety Summit at Bletchley Park in November 2023?', 'The United Kingdom', ['France', 'South Korea', 'The United States'], 'It produced the Bletchley Declaration.'),
           ('Which international organisation adopted the first global standard on AI ethics, the Recommendation on the Ethics of AI, in 2021?', 'UNESCO', ['NATO', 'OPEC', 'FIFA'], 'Adopted by 193 member states.'),
           ('What does the EU AI Act require of chatbots and deepfakes?', 'Transparency – people must be told they are interacting with AI or that content is AI-generated', ['A complete ban', 'No rules at all', 'Approval by the UN'], 'These are "limited risk" transparency duties.')],
    why=[('Explain why many experts argue voluntary AI ethics principles are not enough.', 'Principles are vague, unenforceable and can be used for "ethics washing"; without legal duties, audits and penalties, companies under commercial pressure may ignore them.'),
         ('Explain why regulating general-purpose AI models is difficult.', 'They can be used for countless downstream tasks by other developers, so risks depend on use; regulators must decide what duties fall on the model provider versus deployers, and capabilities change rapidly.'),
         ('Explain why international cooperation matters for AI governance.', 'AI is developed and deployed across borders by global firms; national rules alone can be bypassed and create fragmentation, while risks such as misuse or unsafe frontier models are global.')],
    contrast=[('the EU approach to AI governance', 'the US approach to AI governance', 'The EU uses a comprehensive, binding, risk-based law (the AI Act); the US has relied more on sector-specific rules, voluntary commitments, executive orders and state laws.'),
              ('AI ethics principles', 'AI law', 'Ethics principles are voluntary values and guidance (e.g. OECD, UNESCO); AI law creates binding obligations with enforcement and penalties (e.g. EU AI Act).')],
    misc=[('The EU AI Act bans artificial intelligence.', 'It bans only a small set of "unacceptable risk" practices (e.g. social scoring, manipulative AI, most real-time remote biometric identification in public by police); most AI is minimal risk and largely unregulated.'),
          ('Only governments are responsible for AI governance.', 'Governance also includes company policies, technical standards bodies, auditors, civil society, researchers and international organisations.')],
    cases=[('the EU AI Act', 'The AI Act entered into force on 1 August 2024; bans applied from February 2025, duties for general-purpose AI models from August 2025 and most high-risk obligations from 2026–27.', 'risk-based AI governance',
            'it shows a comprehensive legal approach that classifies AI by risk, with the potential to influence global standards (the Brussels effect).'),
           ('the Bletchley Declaration (2023)', 'At the UK\'s AI Safety Summit, 28 countries including the US and China, plus the EU, signed a declaration on the risks of frontier AI and the need for international cooperation.', 'international AI governance',
            'it created a shared agenda on frontier AI safety but no binding commitments.'),
           ('China\'s generative AI rules (2023)', 'China\'s Interim Measures for generative AI services (in force August 2023) require providers to register algorithms, label AI content and ensure outputs reflect "core socialist values".', 'AI governance and political values',
            'AI regulation can serve both safety and state control, showing that governance reflects political systems.')],
    sources=[('"AI systems should be designed in a way that respects the rule of law, human rights, democratic values and diversity."', 'OECD AI Principles, 2019',
              'Explain one strength and one limitation of the approach in the source.', 'Strength: broad international agreement on values guiding AI. Limitation: voluntary and general, with no enforcement mechanism.'),
             ('"Providers shall ensure that AI systems intended to interact directly with natural persons are designed so that the persons are informed that they are interacting with an AI system."', 'EU AI Act, Article 50 (transparency obligations)',
              'Explain why this requirement is important.', 'It protects people from deception and allows them to judge information and relationships appropriately, which supports trust and autonomy.')],
    evaluate=[('The EU AI Act is the best model for governing AI globally.',
               ['comprehensive, binding, risk-based', 'protects fundamental rights; Brussels effect'],
               ['complex and costly for small firms', 'slow to adapt to fast-changing technology', 'different political systems and priorities elsewhere'],
               'The AI Act is an influential model, but other countries may adapt rather than copy it; its success depends on implementation.'),
              ('AI companies should be held legally responsible for harms caused by their systems.',
               ['they design and profit from systems', 'liability creates incentives for safety'],
               ['harms often arise from users\' misuse', 'complex supply chains complicate responsibility', 'excessive liability may deter open research'],
               'Responsibility should be shared along the AI value chain, with clear duties for providers and deployers proportionate to their control.')],
    extended=[('Compare two approaches to AI governance (e.g. EU, US, China, UNESCO) and evaluate their effectiveness in protecting citizens.', 'Compare binding vs voluntary, risk-based vs sectoral, rights-based vs state-control priorities; examples; evaluate effectiveness and trade-offs with innovation; judgement.', 8, 'long')],
))

R.facts('ch04-st4', F(
    terms=[('intellectual property (IP)', 'legal rights over creations of the mind, such as copyright, patents and trademarks'),
           ('copyright', 'the legal right of a creator to control copying, distribution and adaptation of an original work'),
           ('authorship', 'being recognised as the creator of a work; many copyright systems require a human author'),
           ('training data licensing', 'agreements that permit AI developers to use copyrighted works to train models, often for payment'),
           ('text and data mining (TDM) exception', 'a legal exception allowing automated analysis of works; the EU allows it unless rights holders opt out (2019 Copyright Directive)'),
           ('style mimicry', 'when generative AI produces works imitating a particular artist\'s recognisable style')],
    facts=[('In 2023, which US body ruled that images generated by Midjourney in the comic "Zarya of the Dawn" could not be copyrighted?', 'The US Copyright Office', ['The US Supreme Court', 'The European Patent Office', 'WIPO'], 'The text and arrangement by the human author were protected.'),
           ('Which newspaper sued OpenAI and Microsoft for copyright infringement in December 2023?', 'The New York Times', ['The Guardian', 'Le Monde', 'The Times of India'], 'It alleged millions of articles were used to train models without permission.'),
           ('Which image library sued Stability AI over the use of its photos to train Stable Diffusion?', 'Getty Images', ['Shutterstock', 'Flickr', 'Unsplash'], 'Cases were brought in the UK and US.'),
           ('An AI-generated image, "Théâtre D\'opéra Spatial", won a prize at which competition in 2022?', 'The Colorado State Fair fine arts competition', ['The Venice Biennale', 'The Turner Prize', 'The World Press Photo award'], 'Jason Allen created it with Midjourney, sparking debate.')],
    why=[('Explain why copyright law struggles with AI-generated works.', 'Copyright traditionally protects original works by human authors; when AI generates most of the content, it is unclear who (if anyone) is the author – the user, the developer or no one – and whether training on copyrighted works was lawful.'),
         ('Explain why artists object to generative AI trained on their work.', 'Their works were often used without consent or payment, AI can mimic their style and compete with them in the market, and they receive no credit or share of the value created.'),
         ('Explain why AI could also expand creativity.', 'AI tools lower barriers to producing music, images and video, let people experiment quickly and can be used by artists as collaborators, opening creative expression to more people.')],
    contrast=[('AI-assisted work', 'AI-generated work', 'AI-assisted work is created by a human who uses AI as a tool while making the key creative choices (likely protectable); AI-generated work is produced mainly by the AI with minimal human creative input (in the US, not copyrightable).'),
              ('inspiration', 'infringement', 'Inspiration is learning from or imitating general styles and ideas, which copyright does not protect; infringement is copying protected expression without permission or a legal exception.')],
    misc=[('Anything produced by AI is automatically owned by the person who typed the prompt.', 'In the US (Copyright Office guidance 2023; Thaler v Perlmutter) works without sufficient human authorship are not protected; ownership also depends on platform terms and national law.'),
          ('Using copyrighted works to train AI is clearly legal everywhere.', 'It is contested: some jurisdictions have TDM exceptions with opt-outs (EU), the US relies on fair use, which is being tested in court cases such as NYT v OpenAI and Getty v Stability AI.')],
    cases=[('Zarya of the Dawn (2023)', 'Kris Kashtanova\'s comic used Midjourney images; the US Copyright Office granted protection for the text and arrangement but not the AI-generated images.', 'AI and authorship',
            'it established that, in the US, human authorship is needed for copyright, so purely AI-generated images are not protected.'),
           ('New York Times v. OpenAI and Microsoft (filed 2023)', 'The Times alleged that millions of its articles were used without permission to train models that can reproduce its content and compete with it.', 'AI and intellectual property',
            'the case tests whether training on copyrighted works is fair use, with major implications for creators and AI companies.'),
           ('Théâtre D\'opéra Spatial (2022)', 'Jason Allen won the digital arts category at the Colorado State Fair with an image made using Midjourney; artists protested, and the Copyright Office later refused registration.', 'AI and the meaning of creativity',
            'the prize sparked debate about whether prompting AI is a creative act and what counts as art.')],
    sources=[('"The Office will not register works produced by a machine or mere mechanical process that operates randomly or automatically without any creative input or intervention from a human author."', 'US Copyright Office, Compendium and AI guidance, 2023',
              'With reference to the source, explain the Office\'s position on AI-generated works.', 'Copyright protection requires human creative input; works generated automatically by AI without such input cannot be registered.'),
             ('"They trained on our art without asking, and now clients ask the machine for \'something in her style\'."', 'Illustrator quoted in a 2023 article on generative AI',
              'Explain two concerns raised in the source.', 'Use of artists\' work without consent for training; economic harm because AI imitates their style and replaces paid commissions.')],
    evaluate=[('AI-generated works should be protected by copyright.',
               ['encourages investment in creative AI', 'users may contribute creative prompts and selection'],
               ['copyright exists to reward human creativity', 'protection could flood markets and crowd out human artists', 'unclear who the author is'],
               'Purely AI-generated works should not be protected, but works with significant human creative contribution using AI tools can be.'),
              ('Generative AI threatens human creativity more than it enhances it.',
               ['style mimicry and market substitution harm artists\' incomes', 'training without consent'],
               ['AI tools open creativity to more people', 'artists use AI as a collaborator', 'licensing deals and opt-outs may balance interests'],
               'AI both threatens and enhances creativity; outcomes depend on rules on consent, compensation and attribution.')],
    extended=[('Evaluate whether AI developers should pay creators whose works are used as training data.', 'Arguments: fairness, consent, market harm, licensing deals (e.g. news publishers\' agreements with OpenAI); counter: fair use, impracticality, benefits of open research; examples (NYT v OpenAI, Getty v Stability, EU opt-out); judgement.', 8, 'long')],
))

P2['ch04'] = dict(
    src=[('"AI will affect almost 40 percent of jobs around the world, replacing some and complementing others. In most scenarios, AI will likely worsen overall inequality."', 'Kristalina Georgieva, IMF blog, January 2024',
          'Identify two claims made in {S}.', ['AI will affect almost 40% of jobs worldwide', 'AI will likely worsen inequality'],
          'Explain why {S} might be considered an authoritative source.', 'It comes from the head of the IMF, drawing on the organisation\'s economic research across many countries; however it is a summary of scenarios, not certain predictions.'),
         ('"Our AI assistant is doing the equivalent work of 700 full-time agents, and customers are just as satisfied."', 'Klarna press release, February 2024',
          'Identify two claims about the AI assistant in {S}.', ['it does work equivalent to 700 full-time agents', 'customer satisfaction was as high as with human agents'],
          'Explain one limitation of {S} as evidence about AI and jobs.', 'It is a company press release with an interest in promoting its technology; it gives no independent data, and Klarna later said it would hire more human agents to protect quality.'),
         ('"Agents with access to the AI tool resolved 14% more issues per hour on average, with the greatest gains – about 34% – for the least experienced workers."', 'Brynjolfsson, Li and Raymond, "Generative AI at Work", NBER working paper, 2023',
          'Identify two findings in {S}.', ['productivity rose 14% on average', 'largest gains (about 34%) for least experienced workers'],
          'Explain what {S} suggests about augmentation.', 'AI acted as a tool that raised workers\' productivity – especially novices\' – rather than replacing them, suggesting augmentation can reduce skill gaps.')],
    cmp=[(1, 2, 'the effect of AI on customer-service work', ['both concern AI in customer service', 'both report productivity gains'],
          ['Source B suggests replacement of workers; Source C suggests augmentation of workers', 'B is a company claim; C is an academic study with data']),
         (0, 2, 'the distribution of AI\'s impacts on workers', ['both suggest AI affects workers unequally'],
          ['Source A predicts AI will worsen inequality; Source C finds AI narrowed skill gaps within one workplace', 'A is a global projection; C is a single-firm study'])],
    ev=[(1, 2, 'AI will mainly replace rather than complement human workers.', ['Klarna\'s assistant replaced the work of 700 agents (Source B)', 'generative AI exposes many cognitive tasks'],
         ['productivity gains for workers using AI (Source C)', 'IMF says AI complements as well as replaces (Source A)', 'Klarna later rehired human agents']),
        (0, 2, 'AI will increase inequality between workers.', ['IMF projects worsening inequality (Source A)', 'gains may go to capital owners and AI-skilled workers'],
         ['AI helped the least experienced workers most (Source C)', 'policy (reskilling, tax) can shape outcomes'])],
)

# =============================================================================================
# ch05 Content 3.7 Robots and autonomous technologies: characteristics and uses
# =============================================================================================
@R.add('ch05-st1', 'C3', (1, 5), 'numerical')
def control_trace(rng, slot):
    kind = rng.choice(['vacuum', 'thermo'])
    if kind == 'vacuum':
        d = [rng.randint(5, 60) for _ in range(5 if slot.d >= 3 else 4)]
        lim = rng.choice([15, 20, 25])
        acts = ['TURN' if x < lim else 'FORWARD' for x in d]
        code = (f'loop for each sensor reading DIST (cm)\n    if DIST < {lim} then\n        output "TURN"\n    else\n        output "FORWARD"\n    end if\nend loop')
        stem = f'A robot vacuum cleaner uses an ultrasonic distance sensor and this control algorithm:\n\n{code}\n\nThe sensor readings are {", ".join(map(str, d))}. State the outputs in order.'
        ans = ', '.join(acts)
        key = '; '.join(f'{x} {"<" if x < lim else "≥"} {lim} → {a}' for x, a in zip(d, acts)) + ' [A1 per two correct, max 2].'
        m = 2
        if slot.d >= 4:
            stem += ' Identify the sensor, the processing and the actuator in this robot, and explain why this is an example of a feedback loop.'
            ans += '; sensor: ultrasonic distance sensor; processing: the comparison in the controller; actuator: wheel motors; feedback: each movement changes the next sensor reading, which changes the next action'
            key += ' Sense–think–act identified [A1 A1 A1]; feedback explained [R1].'
            m = 5
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    target = rng.choice([19, 20, 21, 22])
    temps = [round(target + rng.uniform(-3, 3), 1) for _ in range(5)]
    acts = ['HEATER ON' if t < target - 0.5 else 'HEATER OFF' if t > target + 0.5 else 'NO CHANGE' for t in temps]
    stem = (f'A smart thermostat (target {target} °C) switches the heater ON if the temperature is below {target - 0.5} °C, OFF if above {target + 0.5} °C, and makes no change otherwise. '
            f'Readings: {", ".join(f"{t} °C" for t in temps)}. State the action for each reading.')
    ans = ', '.join(acts)
    key = '; '.join(f'{t} → {a}' for t, a in zip(temps, acts)) + ' [A1 A1].'
    m = 2
    if slot.d >= 3:
        stem += ' Explain why this is negative feedback.'
        ans += '; each action counteracts the deviation from the target, keeping temperature stable'
        key += ' Output opposes the change, stabilising the system [R1].'
        m = 3
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch05-st1', F(
    terms=[('robot', 'a programmable machine that can sense its environment, process information and act physically in the world, with some degree of autonomy'),
           ('sensor', 'a device that measures something in the environment (distance, light, temperature, position) and sends data to the robot\'s controller'),
           ('actuator', 'a component, such as a motor, hydraulic cylinder or gripper, that makes a robot move or act'),
           ('controller', 'the computer or processor that runs the robot\'s program, processing sensor data and sending commands to actuators'),
           ('degree of autonomy', 'how far a machine can operate without human control, from tele-operated to fully autonomous'),
           ('LiDAR', 'a sensor that measures distance by timing laser pulses, creating a 3D map of the surroundings, used in many autonomous vehicles'),
           ('end effector', 'the tool at the end of a robot arm, such as a gripper, welder or surgical instrument')],
    facts=[('Which play by Karel Čapek (1920) introduced the word "robot"?', 'R.U.R. (Rossum\'s Universal Robots)', ['I, Robot', 'Metropolis', 'Frankenstein'], 'From the Czech "robota", meaning forced labour.'),
           ('What was the first industrial robot, installed at a General Motors plant in 1961?', 'Unimate', ['ASIMO', 'Roomba', 'Shakey'], 'It lifted and stacked hot die-cast metal parts.'),
           ('How many levels of driving automation does the SAE J3016 standard define?', 'Six (Level 0 to Level 5)', ['Three', 'Ten', 'Four'], 'Level 0 = no automation; Level 5 = full automation in all conditions.'),
           ('Which component makes a robot arm move?', 'An actuator such as an electric motor', ['A sensor', 'A database', 'A camera'], 'Actuators convert energy into motion.')],
    why=[('Explain why sensors are essential for a robot to operate autonomously.', 'Without sensors a robot cannot detect obstacles, objects or changes in its environment, so it could only repeat fixed movements; sensor data lets the controller adjust actions in real time.'),
         ('Explain why the "sense–think–act" cycle describes how robots work.', 'Robots repeatedly gather data from sensors (sense), process it with algorithms to decide what to do (think) and move using actuators (act); the results change what is sensed next, forming a feedback loop.'),
         ('Explain why greater autonomy raises questions of responsibility.', 'As machines make more decisions without human control, it becomes harder to say who is responsible for errors – the designer, manufacturer, operator or owner – especially when behaviour emerges from machine learning.')],
    contrast=[('a sensor', 'an actuator', 'A sensor takes in information from the environment (input); an actuator produces movement or action in the environment (output).'),
              ('an automated machine', 'an autonomous robot', 'An automated machine repeats pre-programmed actions in a controlled setting (e.g. a fixed welding arm); an autonomous robot senses and adapts to changing environments, making some decisions without human input (e.g. a delivery robot).')],
    misc=[('A robot must look like a human.', 'Most robots are not humanoid – industrial arms, vacuum robots, drones and autonomous vehicles are robots defined by sensing, processing and acting.'),
          ('Self-driving cars on sale today are fully autonomous.', 'Most consumer systems (e.g. Tesla Autopilot) are SAE Level 2 driver assistance requiring constant supervision; robotaxis like Waymo operate at Level 4 only in defined areas.')],
    cases=[('Unimate at General Motors (1961)', 'Unimate, invented by George Devol and developed with Joseph Engelberger, handled hot metal parts at a GM plant in New Jersey.', 'the beginning of industrial robotics',
            'robots took over dangerous, repetitive tasks, beginning the automation of manufacturing.'),
           ('Waymo robotaxis', 'Waymo launched a public driverless ride-hailing service in Phoenix in 2020 and later expanded to San Francisco and Los Angeles, using LiDAR, radar and cameras.', 'sensors and high autonomy',
            'multiple sensors and machine learning allow Level 4 driving in mapped areas without a human driver.'),
           ('the Roomba (2002)', 'iRobot\'s Roomba vacuum used bump and cliff sensors and simple behaviours; later models map homes with cameras.', 'robots in everyday life',
            'a simple sense–act design brought robots into millions of homes, while home-mapping later raised privacy concerns.')],
    sources=[('"A robot may not injure a human being or, through inaction, allow a human being to come to harm."', 'Isaac Asimov, First Law of Robotics, "Runaround" (1942)',
              'Explain one reason why Asimov\'s law is difficult to apply to real robots.', 'Real robots cannot reliably interpret "harm" in complex situations; their sensors and algorithms have limits, and dilemmas (e.g. autonomous vehicles) may involve unavoidable harm.'),
             ('"Level 2 systems require the driver to supervise at all times and be ready to take over immediately."', 'Summary of SAE J3016 levels of driving automation',
              'Explain why the distinction in the source matters for safety.', 'Drivers who believe Level 2 cars drive themselves may stop paying attention (automation complacency), causing crashes; marketing names like "Autopilot" may encourage this.')],
    evaluate=[('Robots should be defined by their autonomy rather than their appearance.',
               ['autonomy determines capabilities, risks and responsibility', 'most robots are not humanoid'],
               ['appearance shapes how people interact with robots (anthropomorphism)', 'tele-operated machines are also robots'],
               'Autonomy is the more useful defining feature for analysis, but appearance matters for social impacts.'),
              ('Increasing the autonomy of robots always increases their benefits.',
               ['reduces human labour and risk in dangerous jobs', 'operates continuously and precisely'],
               ['reduces human control and accountability', 'errors in unpredictable environments', 'ethical concerns (weapons)'],
               'Greater autonomy brings benefits in controlled settings, but in complex or high-stakes settings meaningful human control remains important.')],
    extended=[('Using one robot you have studied, explain the role of its sensors, controller and actuators and evaluate how its degree of autonomy affects its impacts.', 'E.g. Waymo, Roomba, da Vinci, warehouse robots; identify components; level of autonomy; impacts on users, workers, safety, responsibility; judgement.', 6, 'long')],
))


@R.add('ch05-st2', 'C3', (1, 5), 'numerical')
def robot_numbers(rng, slot):
    kind = rng.choice(['density', 'drone'])
    if kind == 'density':
        robots = rng.choice([12000, 45000, 150000, 400000])
        workers = rng.choice([0.8, 1.5, 3, 6])  # million
        dens = robots / (workers * 1e6) * 10000
        country = rng.choice(['a manufacturing economy', 'a country', 'an industrial region'])
        stem = f'In {country}, {robots:,} industrial robots operate in a manufacturing sector employing {workers:g} million workers. Calculate the robot density (robots per 10,000 manufacturing employees).'
        ans = f'{dens:,.0f} robots per 10,000 employees'
        key = f'{robots:,} ÷ {workers * 1e6:,.0f} × 10,000 = {dens:,.0f} [M1 A1]. (For comparison, the IFR reported South Korea at over 1,000 per 10,000 in 2023.)'
        m = 2
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    speed = rng.choice([60, 80, 100, 110])  # km/h
    dist = rng.choice([10, 20, 30, 45])  # km one way
    ctx = rng.choice(['blood supplies to a rural clinic in Rwanda', 'vaccines to a health centre in Ghana', 'medicines to an island clinic', 'lab samples between hospitals'])
    mins = dist / speed * 60
    stem = f'A delivery drone flies at {speed} km/h carrying {ctx}, {dist} km away. Calculate the one-way flight time in minutes.'
    ans = f'{mins:.1f} minutes'
    key = f'{dist} ÷ {speed} = {dist / speed:.3f} h [M1]; × 60 = {mins:.1f} min [A1].'
    m = 2
    if slot.d >= 3:
        road = rng.choice([30, 40, 50])
        rmins = dist * 1.4 / road * 60
        stem += f' By road the route is 40% longer and vehicles average {road} km/h. Calculate the time saved by the drone.'
        ans += f'; road {rmins:.1f} min; saves {rmins - mins:.1f} min'
        key += f' Road: {dist} × 1.4 ÷ {road} × 60 = {rmins:.1f} min [M1]; saving {rmins - mins:.1f} min [A1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch05-st2', F(
    terms=[('industrial robot', 'a programmable robot arm or machine used in manufacturing for tasks such as welding, painting, assembly and packaging'),
           ('service robot', 'a robot that performs useful tasks for people outside industrial automation, such as cleaning, delivery or hospitality'),
           ('social robot', 'a robot designed to interact and communicate with people in a social way, such as Pepper or Paro'),
           ('surgical robot', 'a robot system that assists surgeons with precise movements, such as the da Vinci system, usually controlled by the surgeon'),
           ('unmanned aerial vehicle (UAV)', 'an aircraft without a human pilot on board, commonly called a drone, controlled remotely or autonomously'),
           ('autonomous vehicle', 'a vehicle that can sense its environment and drive with limited or no human input'),
           ('cobot', 'a collaborative robot designed to work safely alongside humans in shared spaces')],
    facts=[('Which company has delivered blood and medical supplies by drone in Rwanda since 2016?', 'Zipline', ['Amazon Prime Air', 'DJI', 'Wing'], 'Zipline later expanded to Ghana, Nigeria, Kenya and the US.'),
           ('Which country had the highest robot density in manufacturing in 2023, according to the IFR?', 'South Korea', ['Brazil', 'India', 'the United Kingdom'], 'Over 1,000 robots per 10,000 employees.'),
           ('Which surgical robot, made by Intuitive Surgical, received US FDA clearance for general surgery in 2000?', 'The da Vinci Surgical System', ['ASIMO', 'Atlas', 'Spot'], 'Surgeons control it from a console.'),
           ('Approximately how many industrial robots were operating worldwide in 2023, according to the IFR?', 'About 4 million', ['About 40,000', 'About 400 million', 'About 4 billion'], 'The IFR reported about 4.28 million operational units.'),
           ('Which company bought Kiva Systems in 2012 to automate its warehouses?', 'Amazon', ['Walmart', 'Alibaba', 'IKEA'], 'Kiva robots move shelves to human pickers.')],
    why=[('Explain why robots are widely used in car manufacturing.', 'Tasks such as welding and painting are repetitive, precise, heavy and hazardous; robots perform them consistently and continuously, improving quality and safety and reducing labour costs.'),
         ('Explain why drones are useful for delivering medical supplies in some countries.', 'Where roads are poor or congested, drones can fly directly and quickly to remote clinics, delivering urgent items (blood, vaccines) without needing drivers or roads.'),
         ('Explain why cobots are changing how robots are used in workplaces.', 'Cobots have sensors and force limits so they can work safely next to people without cages; they are cheaper and easier to program, allowing small firms to automate parts of tasks while workers do others.')],
    contrast=[('an industrial robot', 'a service robot', 'Industrial robots work in factories on manufacturing tasks, often in fenced cells; service robots perform tasks for people in homes, hospitals, shops or streets (cleaning, delivery, care).'),
              ('a surgical robot', 'an autonomous robot', 'A surgical robot such as da Vinci is controlled by a surgeon and enhances precision (tele-operated); an autonomous robot makes decisions and acts without continuous human control.')],
    misc=[('Surgical robots perform operations by themselves.', 'Systems like da Vinci are controlled by a surgeon at a console; the robot translates hand movements into precise instrument movements.'),
          ('Drones are only used by the military.', 'Drones are used in agriculture (crop spraying), mapping, disaster response, journalism, medical delivery (Zipline) and filmmaking.')],
    cases=[('Zipline in Rwanda', 'Since 2016 Zipline\'s fixed-wing drones have delivered blood and medical supplies to hospitals across Rwanda, parachuting packages to the destination.', 'robots in health logistics',
            'autonomous delivery overcame poor road access, reducing delivery times and waste of blood products.'),
           ('Amazon warehouse robots', 'After buying Kiva Systems in 2012, Amazon deployed hundreds of thousands of mobile robots that bring shelves to workers.', 'service and industrial robots in logistics',
            'robots increased efficiency but changed warehouse work, with workers reporting intensified pace and injury concerns.'),
           ('robots at Fukushima', 'After the 2011 Fukushima Daiichi nuclear disaster, remote-controlled robots were used to explore damaged reactors; several failed because of high radiation.', 'robots in dangerous environments',
            'robots let humans investigate places too dangerous to enter, though extreme conditions exposed their limits.')],
    sources=[('"Before the drones, we waited hours for blood to come by road. Now it arrives in about half an hour."', 'Nurse at a rural hospital in Rwanda, interviewed in 2019',
              'With reference to the source, explain one benefit of drone delivery.', 'It greatly reduces delivery time for urgent blood supplies, which can save lives in emergencies such as post-partum haemorrhage.'),
             ('"The robots never get tired. But we have to keep up with them."', 'Amazon warehouse worker, quoted in a 2021 investigation into warehouse injury rates',
              'Explain one impact of robots on workers suggested by the source.', 'Robots set a faster, continuous pace, intensifying work for humans and potentially increasing stress and injury risk.')],
    evaluate=[('Robots have improved working conditions more than they have worsened them.',
               ['take over dangerous, dirty and dull tasks (welding, nuclear inspection)', 'cobots reduce strain'],
               ['work intensification and surveillance in warehouses', 'job losses in routine manufacturing', 'deskilling'],
               'Robots have made some jobs safer but can intensify others; outcomes depend on how they are introduced and on worker voice.'),
              ('Drone delivery is the future of logistics in low-income countries.',
               ['overcomes poor infrastructure (Zipline)', 'fast and relatively cheap for urgent, light items'],
               ['limited payload and weather constraints', 'regulation and airspace', 'roads and local transport still needed for most goods'],
               'Drones are transformative for urgent medical supplies but are a complement to, not a replacement for, broader logistics infrastructure.')],
    extended=[('Compare the use of robots in two different sectors and evaluate their impact on people in each.', 'E.g. manufacturing (automotive welding) vs health (da Vinci, Zipline) or logistics (Amazon); compare tasks, autonomy, benefits, risks for workers/patients; judgement.', 8, 'long')],
))

R.facts('ch05-st3', F(
    terms=[('human–robot interaction (HRI)', 'the study and design of how humans and robots communicate and work together'),
           ('anthropomorphism', 'attributing human characteristics, emotions or intentions to non-human things such as robots'),
           ('uncanny valley', 'the hypothesis (Masahiro Mori, 1970) that robots that look almost, but not quite, human cause feelings of unease'),
           ('social presence', 'the sense that a robot or agent is "there" and socially engaged with a person'),
           ('trust calibration', 'matching how much people trust a robot to how reliable it actually is, avoiding over-trust and under-trust'),
           ('affective computing', 'technology that recognises, interprets or simulates human emotions')],
    facts=[('Who proposed the "uncanny valley" hypothesis in 1970?', 'Masahiro Mori', ['Isaac Asimov', 'Rodney Brooks', 'Sherry Turkle'], 'Mori was a Japanese robotics professor.'),
           ('Which humanoid robot was controversially granted citizenship by Saudi Arabia in 2017?', 'Sophia', ['Pepper', 'ASIMO', 'Atlas'], 'Made by Hanson Robotics; critics called it a publicity stunt.'),
           ('Which therapeutic robot, shaped like a baby harp seal, is used with people with dementia?', 'Paro', ['Aibo', 'Nao', 'Roomba'], 'Developed in Japan by AIST.'),
           ('Which MIT researcher wrote Alone Together (2011) about relationships with robots and technology?', 'Sherry Turkle', ['Kate Crawford', 'Joy Buolamwini', 'Cynthia Breazeal'], 'Turkle warns of substituting robots for human connection.')],
    why=[('Explain why people anthropomorphise robots.', 'Humans are social and tend to read intentions and emotions into things that move, respond or have faces; designers use eyes, voices and names to make robots engaging.'),
         ('Explain why anthropomorphism can be both helpful and harmful.', 'It can make robots easier and more pleasant to use (e.g. comforting dementia patients), but it can lead to over-trust, emotional dependence, deception and manipulation.'),
         ('Explain why trust calibration matters in human–robot interaction.', 'If people over-trust robots (e.g. following a faulty robot in an emergency) they may be harmed; if they under-trust, useful robots will not be used; trust should match real reliability.')],
    contrast=[('anthropomorphism', 'the uncanny valley', 'Anthropomorphism is our tendency to see human traits in robots; the uncanny valley is the discomfort felt when a robot looks almost human but not quite.'),
              ('a social robot', 'an industrial robot', 'A social robot is designed to interact with people through speech, gestures and expressions (Pepper, Paro); an industrial robot performs physical manufacturing tasks with little or no social interaction.')],
    misc=[('If a robot shows emotions, it must feel them.', 'Robots can simulate emotional expressions through programmed responses; there is no evidence that current robots have feelings or consciousness.'),
          ('Making robots look more human always makes people like them more.', 'According to the uncanny valley, near-human appearance can make people uncomfortable; many successful robots are deliberately cartoon-like or animal-like.')],
    cases=[('Paro in dementia care', 'Paro, a seal-like robot that responds to touch and voice, has been used in care homes in Japan, Europe and elsewhere; some trials report reduced agitation in dementia patients.', 'anthropomorphism in care',
            'patients relate to Paro as a pet, which can comfort them, but raises questions of deception and replacing human contact.'),
           ('Sophia\'s "citizenship" (2017)', 'Saudi Arabia announced citizenship for Hanson Robotics\' humanoid robot Sophia at a technology conference, drawing criticism given limited rights for many humans in the country.', 'anthropomorphism and its politics',
            'treating a robot as a person was a publicity act that highlighted confusion about robot capabilities and rights.'),
           ('the "emergency evacuation" trust experiment', 'In a 2016 Georgia Tech study, participants followed a robot during a simulated fire alarm even after it had previously malfunctioned and pointed towards a dark room.', 'over-trust in robots',
            'people over-trusted a robot in an emergency, showing the need for trust calibration in design.')],
    sources=[('"We expect more from technology and less from each other."', 'Sherry Turkle, Alone Together (2011)',
              'Explain the concern expressed in the source in relation to social robots.', 'People may turn to robots for companionship instead of human relationships, weakening human connection, especially for vulnerable groups like the elderly.'),
             ('"Mrs. T talks to Paro every morning. She is calmer, and she smiles more."', 'Care-home manager, interview in a 2018 study of social robots',
              'Explain one benefit and one ethical concern suggested by the source.', 'Benefit: improved mood and calm for a person with dementia. Concern: she may believe Paro is alive, raising deception and dignity issues, and robots might replace staff time.')],
    evaluate=[('Robots should be designed to appear as human as possible.',
               ['familiar forms ease communication', 'useful in some social roles (receptionists, companions)'],
               ['uncanny valley discomfort', 'deception and over-trust', 'raises expectations robots cannot meet'],
               'Robots should be designed for their function and to be honest about their nature; human-like appearance is rarely necessary and can mislead.'),
              ('Social robots can meet people\'s emotional needs.',
               ['comfort and companionship (Paro)', 'consistency and patience in care settings'],
               ['simulated, not real, empathy', 'may reduce human contact', 'privacy concerns from constant monitoring'],
               'Social robots can support emotional well-being but cannot replace genuine human relationships; they should complement human care.')],
    extended=[('Analyse how anthropomorphism shapes interactions with one robot and evaluate the ethical implications.', 'Choose e.g. Paro, Pepper, Sophia, a voice assistant; design features (face, voice, name); effects on users (comfort, trust, attachment); ethics (deception, dignity, privacy, dependence); judgement.', 6, 'long')],
))

# =============================================================================================
# ch06 Content 3.7 Robots and autonomous technologies: impacts and dilemmas
# =============================================================================================
@R.add('ch06-st1', 'C3', (2, 5), 'numerical')
def av_rates(rng, slot):
    miles_av = rng.choice([7, 22, 50, 96])  # million miles
    inc_av = rng.randint(10, 90)
    hum_rate = rng.choice([2.8, 3.2, 4.1, 4.8])  # per million miles (benchmark)
    r_av = inc_av / miles_av
    red = (hum_rate - r_av) / hum_rate * 100
    stem = (f'A robotaxi company reports {inc_av} injury-causing crashes over {miles_av} million driverless miles. A comparable human-driver benchmark in the same cities is {hum_rate} injury crashes per million miles. '
            f'Calculate the robotaxi rate per million miles and the percentage difference from the human benchmark.')
    ans = f'{r_av:.2f} per million miles; {abs(red):.0f}% {"lower" if red > 0 else "higher"} than human drivers'
    key = f'{inc_av} ÷ {miles_av} = {r_av:.2f} [M1 A1]; ({hum_rate} − {r_av:.2f}) ÷ {hum_rate} × 100 = {red:.0f}% [M1 A1].'
    m = 4
    if slot.d >= 4:
        stem += ' Give two reasons why this comparison might not prove that autonomous vehicles are safer.'
        ans += '; e.g. company-reported data; different road types, weather and times; small numbers of serious crashes; human benchmark definitions differ'
        key += ' Data source/independence; not like-for-like conditions; statistical uncertainty with rare events [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch06-st1', F(
    terms=[('trolley problem', 'a thought experiment (Philippa Foot, 1967) about whether to divert a runaway trolley to kill one person instead of five, used to discuss dilemmas for autonomous vehicles'),
           ('lethal autonomous weapon system (LAWS)', 'a weapon that can select and engage targets without further human intervention after activation'),
           ('meaningful human control', 'the principle that humans should retain sufficient understanding and control over weapons and critical systems to be morally and legally responsible'),
           ('responsibility gap', 'the problem that when an autonomous system causes harm, no human may clearly be morally or legally responsible'),
           ('moral machine', 'an MIT online experiment (published in Nature, 2018) that collected about 40 million decisions on how autonomous vehicles should resolve dilemmas'),
           ('operational design domain (ODD)', 'the specific conditions (roads, weather, speeds, areas) in which an automated driving system is designed to operate')],
    facts=[('In March 2018, who was killed in Tempe, Arizona, in the first known pedestrian death involving a self-driving test car?', 'Elaine Herzberg', ['Joshua Brown', 'Robert Williams', 'Molly Russell'], 'An Uber test vehicle struck her; the safety driver was later convicted of endangerment.'),
           ('Which 2017 German ethics commission rule says autonomous vehicles must not distinguish between people by personal features such as age or gender in unavoidable accidents?', 'The Ethics Commission on Automated and Connected Driving', ['The EU AI Act', 'The Geneva Convention', 'The SAE J3016 standard'], 'Its 20 guidelines prioritise protecting human life.'),
           ('A 2021 UN Panel of Experts report on Libya suggested that which drone may have attacked targets autonomously in 2020?', 'The STM Kargu-2', ['The MQ-9 Reaper', 'The Bayraktar TB2 only', 'The DJI Phantom'], 'It was described as a "lethal autonomous weapons system".'),
           ('Under which UN treaty framework have states discussed lethal autonomous weapons in Geneva since 2014?', 'The Convention on Certain Conventional Weapons (CCW)', ['The Paris Agreement', 'The Budapest Convention', 'The Ottawa Treaty'], 'A Group of Governmental Experts has met since 2017.'),
           ('In October 2023 California suspended the driverless permits of which robotaxi company after a pedestrian was dragged by one of its cars?', 'Cruise', ['Waymo', 'Zoox', 'Baidu Apollo'], 'Cruise was owned by General Motors.')],
    why=[('Explain why the trolley problem is criticised as a guide for autonomous-vehicle ethics.', 'Real crashes rarely involve clear choices between known victims; engineers focus on avoiding crashes, sensors give uncertain information, and the bigger ethical questions are about safety standards, testing, liability and who bears risk.'),
         ('Explain why autonomous weapons create a responsibility gap.', 'If a weapon selects targets itself and makes an unlawful attack, it is unclear whether the commander, programmer, manufacturer or state is responsible, because no human made the specific decision.'),
         ('Explain why the Tempe crash raised questions about responsibility.', 'The car\'s system failed to classify the pedestrian correctly, Uber had disabled automatic emergency braking, and the safety driver was distracted; responsibility was spread between company, software and operator, and only the driver was prosecuted.')],
    contrast=[('a utilitarian approach to AV dilemmas', 'a deontological approach to AV dilemmas', 'A utilitarian approach programs cars to minimise total harm (e.g. fewer deaths); a deontological approach sets rules that must not be broken (e.g. never deliberately target a person, or not discriminate by age), regardless of outcomes.'),
              ('an automated weapon', 'an autonomous weapon', 'An automated weapon follows fixed pre-set rules (e.g. a mine or a missile-defence system reacting to incoming projectiles); an autonomous weapon selects and engages targets in changing environments without human decision for each attack.')],
    misc=[('Self-driving cars are already programmed to choose whom to kill in a crash.', 'Developers focus on avoiding collisions and reducing speed; there is no evidence that deployed systems make explicit trolley-problem choices about victims.'),
          ('Autonomous weapons are banned under international law.', 'There is currently no specific treaty banning LAWS; states have debated them at the CCW, and the UN General Assembly has adopted resolutions, but general international humanitarian law still applies.')],
    cases=[('the Uber self-driving crash in Tempe (2018)', 'An Uber test SUV in autonomous mode struck and killed Elaine Herzberg; the NTSB found the system failed to classify her and Uber had weak safety culture; the backup driver later pleaded guilty to endangerment.', 'responsibility for autonomous vehicles',
            'the case shows how responsibility is distributed between software, company decisions and human supervisors, with gaps in accountability.'),
           ('the MIT Moral Machine experiment', 'Researchers collected about 40 million decisions from people in 233 countries and territories about whom an autonomous car should spare; preferences varied between cultural clusters.', 'values and ethics in AV design',
            'there is no universal moral code for machines, so programming ethical choices raises questions about whose values apply.'),
           ('the Kargu-2 in Libya', 'A 2021 UN Panel of Experts report said retreating forces in Libya in 2020 were "hunted down" by loitering munitions such as the Kargu-2 that may have operated without a data link to an operator.', 'autonomous weapons',
            'it may be the first reported use of a weapon attacking people autonomously, fuelling calls for international regulation.')],
    sources=[('"In the event of unavoidable accident situations, any distinction based on personal features (age, gender, physical or mental constitution) is strictly prohibited."', 'German Ethics Commission on Automated and Connected Driving, Rule 9, 2017',
              'With reference to the source, explain which ethical approach the rule reflects.', 'A deontological, rights-based approach: every person has equal dignity, so the car must not weigh lives by personal characteristics, even if a utilitarian calculation might favour it.'),
             ('"Machines with the power and discretion to take lives without human involvement are politically unacceptable, morally repugnant and should be prohibited by international law."', 'UN Secretary-General António Guterres, 2019',
              'Explain the arguments in the source against autonomous weapons.', 'Delegating life-and-death decisions to machines removes human moral judgement and accountability; it is seen as unacceptable both politically and morally, so a ban is called for.')],
    evaluate=[('Autonomous vehicles should be allowed on public roads only if they are proven safer than human drivers.',
               ['protects the public from unproven technology', 'human drivers cause most crashes, so the bar is meaningful'],
               ['proof requires billions of miles of testing on public roads', 'delay costs lives if AVs are already safer', 'safety varies by conditions (ODD)'],
               'AVs should be allowed in limited domains with strong safety data and independent oversight, expanding as evidence accumulates.'),
              ('Lethal autonomous weapons should be banned by an international treaty.',
               ['responsibility gap and lack of human judgement', 'risk of arms races and proliferation', 'UN Secretary-General and many states support limits'],
               ['some argue machines could reduce civilian casualties by being more precise', 'difficult to define and verify', 'major military powers oppose a ban'],
               'A treaty prohibiting weapons without meaningful human control and regulating others is ethically justified, though achieving it is politically difficult.')],
    extended=[('Evaluate who should be held responsible when an autonomous vehicle causes a fatal crash, using at least one real case.', 'Tempe 2018 (Uber, safety driver), Cruise 2023, Tesla Autopilot cases; manufacturer vs software developer vs operator vs regulator; product liability; UK Automated Vehicles Act 2024 (authorised self-driving entity responsible); judgement.', 8, 'long')],
))
AR('ch06-st1', [
    ('Most consumer cars with "self-driving" features still require constant driver supervision.', 'These systems are mainly SAE Level 2 driver assistance.', 'a', 'Level 2 needs a supervising human driver.'),
    ('An international treaty currently bans all lethal autonomous weapons.', 'States have discussed lethal autonomous weapons under the CCW in Geneva.', 'd', 'There is no specific ban treaty yet; R is true.'),
])


R.facts('ch06-st2', F(
    terms=[('care robot', 'a robot designed to assist with caring tasks, such as lifting patients, reminding them to take medicine or providing companionship'),
           ('telepresence robot', 'a robot with a screen and camera that lets a remote person see, talk and move around in a location, used by doctors or for isolated patients'),
           ('dignity (in care)', 'respect for a person\'s worth, autonomy and privacy, which care technologies should protect'),
           ('robot-assisted surgery', 'surgery in which a surgeon controls robotic instruments, often for minimally invasive procedures'),
           ('ageing society', 'a society in which the proportion of older people is growing, increasing demand for care'),
           ('exoskeleton', 'a wearable robotic frame that supports or strengthens the body, used in rehabilitation or to help carers lift')],
    facts=[('Which country has invested heavily in care robots partly because of a rapidly ageing population and labour shortages?', 'Japan', ['Nigeria', 'Brazil', 'Egypt'], 'About 29% of Japan\'s population was 65 or older in 2023.'),
           ('Which robot, developed in Japan, can lift patients from a bed into a wheelchair?', 'RIBA / ROBEAR', ['Roomba', 'Spot', 'Atlas'], 'Developed by RIKEN; it looks like a friendly bear.'),
           ('What is a main advantage of robot-assisted minimally invasive surgery?', 'Smaller incisions and more precise movements, often with shorter recovery', ['No surgeon is needed', 'It is always cheaper', 'It removes all risk'], 'Costs are high and benefits vary by procedure.'),
           ('Which type of robot lets a doctor examine a patient remotely while moving around the ward?', 'A telepresence robot', ['An industrial arm', 'A drone', 'A vacuum robot'], 'Used in remote consultations and during COVID-19.')],
    why=[('Explain why care robots are being developed for ageing societies.', 'There are too few care workers for growing numbers of older people; robots can assist with lifting, monitoring, reminders and companionship, reducing strain on carers and supporting independence.'),
         ('Explain why care robots raise concerns about dignity.', 'Replacing human contact with machines may make older people feel objectified or neglected, constant monitoring can invade privacy, and people with dementia may be deceived about what the robot is.'),
         ('Explain why robot-assisted surgery is not always better than conventional surgery.', 'It is expensive, requires specialist training, and for many procedures studies show similar outcomes to conventional laparoscopic surgery; benefits depend on the procedure and surgeon experience.')],
    contrast=[('a care robot that assists carers', 'a care robot that replaces carers', 'An assistive robot supports human carers (lifting, reminders) so they can spend more time on human interaction; a replacing robot substitutes for human contact, which raises greater dignity concerns.'),
              ('robot-assisted surgery', 'autonomous surgery', 'In robot-assisted surgery the surgeon controls every movement through the robot; autonomous surgery would have the robot perform steps itself – mostly still experimental (e.g. STAR robot suturing pig tissue in 2022).')],
    misc=[('Robots will soon replace nurses.', 'Robots can automate some tasks (lifting, delivering supplies), but nursing requires judgement, empathy and complex physical care that robots cannot provide.'),
          ('Robotic surgery has no risks because machines do not make mistakes.', 'Robotic surgery can have malfunctions and surgical errors, and lawsuits and FDA reports have documented injuries; the surgeon remains responsible.')],
    cases=[('care robots in Japan', 'Japan has funded robots such as Paro, the lifting robot ROBEAR and the communication robot Pepper in care homes; a 2023 study found uptake limited because robots often added work for staff.', 'robots in care',
            'care robots offer support in an ageing society, but practical problems and the value of human care limit their impact.'),
           ('the da Vinci Surgical System', 'Millions of procedures have been performed with da Vinci systems worldwide; studies show benefits for some procedures (e.g. prostatectomy blood loss) but high costs.', 'robot-assisted surgery',
            'precision tools enhance surgeons\' abilities, but costs and uneven evidence raise questions of value and equitable access.'),
           ('telepresence robots during COVID-19', 'Hospitals used telepresence robots to let doctors and families communicate with isolated patients while reducing infection risk.', 'robots and dignity in health care',
            'robots maintained contact during isolation, but some patients found screen-based contact impersonal.')],
    sources=[('"The robots were supposed to save us time. Instead we spent time charging them, fixing them and persuading residents to use them."', 'Paraphrase of care workers\' accounts in James Wright\'s ethnography Robots Won\'t Save Japan (2023)',
              'With reference to the source, explain one limitation of care robots.', 'They created extra work (charging, maintenance, encouragement) for staff rather than saving time, so their benefits in practice were limited.'),
             ('"Robotic assistance allowed me to operate through incisions smaller than a centimetre, and my patient went home the next day."', 'Urologist describing robot-assisted surgery, hospital newsletter, 2022',
              'Explain one benefit and one limitation of the source as evidence about robotic surgery.', 'Benefit: first-hand professional testimony about patient outcomes. Limitation: a single anecdote from a hospital publication with an interest in promoting its services; not systematic evidence.')],
    evaluate=[('Robots can solve the care crisis in ageing societies.',
               ['shortage of care workers; robots help with lifting, monitoring and companionship', 'can support independence at home'],
               ['limited abilities and practical problems (Japan study)', 'dignity and human contact concerns', 'cost and maintenance'],
               'Robots can ease parts of the care burden, but they cannot solve the crisis without investment in human carers.'),
              ('The benefits of robot-assisted surgery justify its costs.',
               ['precision, smaller incisions and faster recovery for some procedures', 'ergonomics for surgeons'],
               ['high purchase and maintenance costs', 'similar outcomes to laparoscopic surgery for many procedures', 'may widen inequality between hospitals'],
               'It is justified for procedures where evidence shows clear benefits, but not as a universal replacement.')],
    extended=[('Evaluate the use of robots in the care of older people, considering benefits, risks and the dignity of patients.', 'Examples (Paro, ROBEAR, Pepper, telepresence); benefits (support, safety, companionship); risks (isolation, deception, privacy, deskilling of care); stakeholders (patients, carers, families, governments); judgement.', 8, 'long')],
))


@R.add('ch06-st3', 'C3', (1, 5), 'numerical')
def robot_payback(rng, slot):
    cost = rng.choice([80000, 120000, 250000, 400000])
    saving = rng.choice([30000, 45000, 60000, 90000])
    maint = rng.choice([5000, 10000, 15000])
    net = saving - maint
    pb = cost / net
    firm = rng.choice(['A furniture factory', 'A food-packaging plant', 'A logistics warehouse', 'A car-parts supplier'])
    stem = (f'{firm} buys a robot for US${cost:,}. It saves US${saving:,} a year in labour costs but costs US${maint:,} a year to maintain. Calculate the payback period in years.')
    ans = f'{pb:.1f} years'
    key = f'Net annual saving = {saving:,} − {maint:,} = US${net:,} [M1]; {cost:,} ÷ {net:,} = {pb:.1f} years [A1].'
    m = 2
    if slot.d >= 3:
        stem += ' Explain one stakeholder who gains and one who loses from this investment.'
        ans += '; owners/shareholders gain lower costs; workers whose tasks are automated may lose jobs or hours'
        key += ' Gain (owners, consumers via prices, remaining workers if upskilled) [R1]; lose (displaced workers, local community) [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch06-st3', F(
    terms=[('automation dividend', 'the productivity and cost gains from automation, which can be shared between owners, workers and consumers'),
           ('robot tax', 'a proposed tax on companies that replace workers with robots, to fund retraining or social security (suggested by Bill Gates in 2017)'),
           ('reshoring', 'moving production back to a home country, which automation can make cheaper than producing in low-wage countries'),
           ('productivity', 'the amount of output produced per unit of input, such as per worker-hour'),
           ('precision agriculture', 'using robots, drones, sensors and data to apply water, fertiliser and pesticides exactly where needed'),
           ('embodied energy', 'the energy used to make a product, such as the materials and manufacturing of a robot')],
    facts=[('Who suggested in 2017 that robots that replace workers should be taxed?', 'Bill Gates', ['Elon Musk', 'Jeff Bezos', 'Tim Cook'], 'The European Parliament rejected a robot tax proposal in 2017.'),
           ('A study by Acemoglu and Restrepo (2020) estimated that each additional robot per 1,000 workers in US local labour markets reduced the employment-to-population ratio by about how much?', 'About 0.2 percentage points', ['About 20 percentage points', 'No effect', 'About 5 percentage points'], 'They also found negative wage effects.'),
           ('Which of these is an environmental benefit of agricultural robots?', 'Targeted spraying that reduces pesticide use', ['Increasing fuel use on farms', 'Removing all need for water', 'Producing more e-waste'], 'Weeding robots and smart sprayers can cut chemical use.'),
           ('Which country installed the most industrial robots in 2023 according to the IFR?', 'China', ['Germany', 'India', 'Mexico'], 'China accounted for about half of global installations.')],
    why=[('Explain why automation can increase productivity but also inequality.', 'Robots produce more output per worker-hour and lower costs, but the gains may go mainly to owners and highly skilled workers while displaced routine workers lose jobs or bargaining power.'),
         ('Explain why automation can lead to reshoring.', 'If robots make labour costs a small share of production, firms can manufacture closer to customers in high-wage countries, reducing transport costs and supply-chain risk, which may reduce jobs in low-wage exporting countries.'),
         ('Explain why robots can have both positive and negative environmental impacts.', 'They can cut waste and resource use (precision agriculture, efficient manufacturing), but their production uses energy, metals and rare minerals, they consume electricity and they create e-waste.')],
    contrast=[('job displacement', 'job creation from automation', 'Displacement is the loss of jobs when tasks are automated (e.g. assembly-line roles); creation includes new jobs in designing, installing, maintaining and programming robots and in growing firms.'),
              ('a robot tax', 'a retraining fund', 'A robot tax charges firms for automating to slow displacement or raise revenue; a retraining fund invests in workers\' skills to help them move to new jobs, regardless of the cause of displacement.')],
    misc=[('Robots always reduce the total number of jobs in an economy.', 'Robots can destroy jobs in some tasks and regions while productivity gains, lower prices and new industries create jobs elsewhere; net effects vary by country and time.'),
          ('Robots are always better for the environment than human workers.', 'Robots require energy, materials and minerals and create e-waste; their environmental impact depends on how they are used and powered.')],
    cases=[('Foxconn\'s automation', 'Electronics manufacturer Foxconn announced plans to automate large parts of its Chinese factories, reportedly replacing tens of thousands of workers with robots (2016).', 'economic impacts of robotics',
            'automation lowered dependence on labour in a major manufacturing hub, raising concerns about employment for low-skilled workers.'),
           ('agricultural robots and precision weeding', 'Companies such as Carbon Robotics have developed laser-weeding robots that identify and burn weeds without herbicides.', 'environmental impacts of robotics',
            'targeted treatment reduces chemical use and soil damage, though robots are expensive and suited mainly to large farms.'),
           ('Acemoglu and Restrepo\'s study of US robots', 'Their research on US labour markets (1990–2007) found that areas more exposed to industrial robots saw lower employment and wages.', 'automation and inequality',
            'the evidence shows that robot gains were not automatically shared with workers in exposed communities.')],
    sources=[('"Right now, the human worker who does, say, $50,000 worth of work in a factory, that income is taxed. If a robot comes in to do the same thing, you\'d think that we\'d tax the robot at a similar level."', 'Bill Gates, interview with Quartz, 2017',
              'With reference to the source, explain the argument for a robot tax.', 'When robots replace workers, governments lose income tax revenue; taxing robots would maintain revenue to fund retraining and social support, and might slow displacement.'),
             ('"One more robot per thousand workers reduces the employment-to-population ratio by about 0.2 percentage points and wages by 0.42%."', 'Acemoglu and Restrepo, "Robots and Jobs", Journal of Political Economy, 2020',
              'Explain what the source suggests about the impact of robots on workers.', 'In exposed US local labour markets, robots reduced employment and wages, suggesting automation benefits were not shared with affected workers.')],
    evaluate=[('A robot tax is the best way to manage the economic impacts of automation.',
               ['funds retraining and social security', 'slows sudden displacement'],
               ['hard to define a robot', 'may discourage productivity-raising investment', 'general taxes on capital or profits may be more effective'],
               'A specific robot tax is difficult to design; broader measures – reskilling, social protection and taxing capital income – are likely more effective.'),
              ('Robotics will help more than harm environmental sustainability.',
               ['precision agriculture reduces chemicals and water', 'efficient manufacturing and recycling robots (sorting e-waste)'],
               ['production uses energy, metals and rare minerals', 'more automation may increase consumption', 'e-waste at end of life'],
               'Robotics can support sustainability in targeted uses if powered by clean energy and designed for repair and recycling.')],
    extended=[('Evaluate the economic and environmental impacts of robotics in one industry.', 'E.g. agriculture (precision weeding, milking robots), manufacturing (Foxconn), logistics (Amazon); productivity, jobs, wages, local communities; energy, materials, waste; judgement.', 8, 'long')],
))

P2['ch06'] = dict(
    src=[('"The vehicle\'s system detected the pedestrian about six seconds before impact but did not correctly classify her as a pedestrian, and emergency braking was not enabled during computer control."', 'Summary of the US National Transportation Safety Board investigation into the Uber crash in Tempe, Arizona, 2019',
          'Identify two failures described in {S}.', ['the system did not correctly classify the pedestrian', 'emergency braking was not enabled during computer control'],
          'Explain why {S} is a reliable source about the crash.', 'It comes from the NTSB, an independent federal investigative agency using technical data from the vehicle; its purpose is to find causes and improve safety, not to assign blame for profit.'),
         ('"Our driverless vehicles had significantly fewer injury-causing crashes than human drivers over the same distance in the cities where we operate."', 'Robotaxi company safety report, 2024',
          'Identify two claims in {S}.', ['fewer injury-causing crashes than human drivers', 'comparison over the same distance in the same cities'],
          'Explain one reason why {S} should be treated with caution.', 'It is self-published by a company with commercial interests; data may not be independently verified and road conditions may differ from the human benchmark.'),
         ('"Who should die? Respondents preferred sparing more lives, sparing the young and sparing humans over animals – but preferences differed between cultures."', 'Summary of Awad et al., "The Moral Machine experiment", Nature, 2018',
          'Identify two preferences reported in {S}.', ['sparing more lives', 'sparing the young / humans over animals'],
          'Explain what {S} suggests about programming ethics into autonomous vehicles.', 'There is no universal agreement on moral choices; preferences vary by culture, so deciding whose values cars follow is a political and ethical choice, not just a technical one.')],
    cmp=[(0, 1, 'the safety of autonomous vehicles', ['both concern how safely autonomous vehicles operate', 'both use technical data about driving'],
          ['Source A describes a fatal failure of a test vehicle; Source B claims better safety than humans', 'A is an independent investigation; B is a company report']),
         (0, 2, 'decision-making by autonomous vehicles', ['both concern how AVs should respond to people on the road'],
          ['Source A shows a real perception failure; Source C considers hypothetical moral dilemmas', 'A is about technical reliability; C about values'])],
    ev=[(0, 1, 'autonomous vehicles will make roads safer for everyone.', ['company data show fewer injury crashes (Source B)', 'human error causes most crashes'],
         ['system failures can kill (Source A)', 'self-reported data (Source B)', 'vulnerable road users may bear new risks']),
        (1, 2, 'technical safety matters more than ethical programming for autonomous vehicles.', ['most harm prevention comes from avoiding crashes (Sources A and B)', 'dilemmas are rare'],
         ['values shape design choices and risk distribution (Source C)', 'public trust depends on ethical acceptability'])],
)

# =============================================================================================
# ch07 Contexts in depth: applying concepts and content to real-world examples
# =============================================================================================
@R.add('ch07-st1', 'C3', (1, 4), 'numerical')
def ad_targeting(rng, slot):
    budget = rng.choice([50000, 200000, 750000, 2000000])
    cpm = rng.choice([4, 8, 12, 20])
    rate = rng.choice([0.5, 1, 1.5, 2])
    imps = budget / cpm * 1000
    clicks = imps * rate / 100
    who = rng.choice(['A political campaign', 'An advocacy group', 'A party in a regional election'])
    stem = (f'{who} spends US${budget:,} on targeted social-media adverts at a cost of US${cpm} per 1,000 impressions. The click-through rate is {rate:g}%. '
            f'Calculate the number of impressions and clicks.')
    ans = f'{imps:,.0f} impressions; {clicks:,.0f} clicks'
    key = f'{budget:,} ÷ {cpm} × 1000 = {imps:,.0f} impressions [M1 A1]; × {rate:g}% = {clicks:,.0f} clicks [A1].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain one concern about micro-targeted political advertising.'
        ans += '; different voters see different, unaccountable messages (no shared public debate), and targeting may exploit personal data and vulnerabilities, as in the Cambridge Analytica case'
        key += ' Concern: opacity/fragmentation of debate, use of personal data, manipulation, limited fact-checking [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch07-st1', F(
    terms=[('gig economy', 'a labour market of short-term, task-based work, often allocated by digital platforms such as Uber, Deliveroo or Upwork'),
           ('algorithmic management', 'using algorithms to assign, monitor, evaluate and discipline workers, as on ride-hailing and delivery platforms'),
           ('micro-targeting', 'using personal data to deliver tailored political or commercial messages to small groups of people'),
           ('e-government', 'the use of digital technologies to deliver government services and engage citizens, as in Estonia'),
           ('digital public infrastructure (DPI)', 'shared digital systems such as digital ID, payments and data exchange that enable public and private services, e.g. India\'s Aadhaar–UPI "India Stack"'),
           ('platform cooperative', 'a digital platform owned and governed by its workers or users rather than investors')],
    facts=[('In Uber BV v Aslam (2021), what did the UK Supreme Court decide?', 'Uber drivers are "workers" entitled to minimum wage and holiday pay', ['Uber drivers are employees of the UK government', 'Uber must stop operating in London', 'Drivers are fully self-employed contractors'], 'The court pointed to Uber\'s control over pay, contracts and ratings.'),
           ('In which year did Estonia become the first country to allow online voting in a national parliamentary election?', '2007', ['1995', '2019', '2023'], 'In the 2023 election over half of votes were cast online.'),
           ('Which 2020 California ballot measure exempted app-based drivers from being classified as employees?', 'Proposition 22', ['Proposition 13', 'Proposition 8', 'Proposition 65'], 'Uber, Lyft and DoorDash spent over US$200 million supporting it.'),
           ('Which EU law adopted in 2024 introduces a presumption of employment for platform workers and rules on algorithmic management?', 'The Platform Work Directive', ['The Digital Markets Act', 'The GDPR', 'The Data Act'], 'Member states must transpose it by 2026.')],
    why=[('Explain why algorithmic management changes the balance of power between platforms and workers.', 'Platforms control job allocation, pay rates, ratings and deactivation through opaque algorithms, while workers lack information and bargaining power, even though they are classified as independent.'),
         ('Explain why digital technologies have become central to elections.', 'Campaigns use data analytics and targeted social-media ads to reach voters, citizens get news through platforms, and electoral systems use digital registration and sometimes voting, creating both opportunities and risks (disinformation, hacking).'),
         ('Explain why digital public infrastructure has been promoted as a model for development.', 'Shared, interoperable systems such as digital ID and instant payments (Aadhaar, UPI) lower costs for everyone, enable financial inclusion and allow private innovation on top of public rails.')],
    contrast=[('a gig worker', 'an employee', 'A gig worker is paid per task through a platform and usually classified as self-employed, lacking guaranteed hours and benefits; an employee has a contract with rights such as minimum wage, sick pay and protection from unfair dismissal.'),
              ('e-government', 'e-democracy', 'E-government uses technology to deliver services (tax filing, permits); e-democracy uses technology for citizen participation in decisions (e-voting, online consultations, petitions).')],
    misc=[('Gig work is always freely chosen and flexible.', 'Many gig workers depend on platform income, work long hours to earn enough, and are controlled by algorithms that penalise refusing jobs.'),
          ('Online voting automatically increases turnout.', 'Evidence from Estonia and elsewhere shows modest effects on overall turnout; online voting also raises security and trust concerns.')],
    cases=[('Uber v Aslam (UK Supreme Court, 2021)', 'The court ruled unanimously in February 2021 that Uber drivers are workers, because Uber sets fares, contracts and controls drivers through ratings.', 'economic context: the platform economy',
            'legal intervention redefined the employment status of platform workers, limiting platform power.'),
           ("Estonia's e-government (X-Road)", 'Estonia connects public and private databases through the X-Road data-exchange layer; almost all public services are online and over half of votes in 2023 were cast online.', 'political context: digital governance',
            'efficient digital government increases convenience and participation, but depends on high trust and strong cybersecurity.'),
           ('Cambridge Analytica and elections', 'Facebook data on up to 87 million people was used by Cambridge Analytica for political profiling linked to campaigns including Donald Trump\'s 2016 campaign.', 'political context: data and elections',
            'personal data was used to target voters without consent, raising concerns about manipulation and the integrity of elections.')],
    sources=[('"Uber sets the fares; Uber imposes the contract terms; drivers\' acceptance and cancellation rates are monitored and can lead to a log-off."', 'Summary of reasoning in Uber BV v Aslam, UK Supreme Court, 2021',
              'With reference to the source, explain why the court decided drivers were workers.', 'Uber controls key aspects of the work – pricing, contract terms and discipline through monitoring – so drivers are in a position of subordination and dependency, not genuinely independent businesses.'),
             ('"An Estonian can do everything online except marry, divorce and buy property."', 'Common description of Estonia\'s e-government (divorce was added online in 2024)',
              'Explain what the source suggests about digital governance in Estonia.', 'Almost all interactions with the state are digital, showing a highly developed e-government that saves time and costs; it also illustrates dependence on digital identity and secure systems.')],
    evaluate=[('Gig-economy platforms should be required to treat workers as employees.',
               ['algorithmic control makes workers dependent (Uber v Aslam)', 'employment rights reduce precarity'],
               ['many workers value flexibility', 'platforms may raise prices or reduce work', 'a "third category" (workers) may balance both'],
               'Platforms should give core protections (minimum pay, safety, transparency, appeal), as the EU Platform Work Directive aims, while allowing genuine flexibility.'),
              ('Digital technologies have strengthened democracy more than they have weakened it.',
               ['e-government and participation (Estonia, online petitions)', 'citizen journalism and transparency'],
               ['disinformation and micro-targeting', 'surveillance and shutdowns', 'polarisation'],
               'Digital technology strengthens democracy where institutions are strong and regulated, but weakens it where it is used for manipulation and control.')],
    extended=[('With reference to one real-world example, analyse the economic and political impacts of a digital platform and evaluate their implications for workers or citizens.', 'E.g. Uber (worker status, Prop 22, EU directive), Estonia\'s e-government, India Stack, Cambridge Analytica; analyse economic and political impacts; implications; judgement.', 8, 'long')],
))


@R.add('ch07-st2', 'C3', (1, 5), 'numerical')
def tele_wearable(rng, slot):
    kind = rng.choice(['tele', 'alarm'])
    if kind == 'tele':
        pts = rng.choice([400, 1200, 3000])
        km = rng.choice([30, 60, 90, 140])
        co2 = rng.choice([0.12, 0.17, 0.2])
        tot_km = pts * km * 2
        saved = tot_km * co2
        stem = (f'A rural telemedicine service in {rng.choice(["Peru", "India", "Kenya", "Canada", "Indonesia"])} replaces {pts:,} clinic visits a year. Each visit would have required a {km} km journey each way by car, emitting {co2} kg CO₂ per km. '
                f'Calculate the total distance and CO₂ avoided.')
        ans = f'{tot_km:,} km; {saved:,.0f} kg CO₂'
        key = f'{pts:,} × {km} × 2 = {tot_km:,} km [M1 A1]; × {co2} = {saved:,.0f} kg CO₂ [A1].'
        m = 3
        if slot.d >= 4:
            stem += ' Explain one limitation of telemedicine for these patients.'
            ans += '; poor connectivity or digital skills, inability to perform physical examinations, privacy at home'
            key += ' Limitation explained [R1].'
            m = 4
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)
    users = rng.choice([10000, 50000, 100000])
    prev = rng.choice([1, 2, 3])
    sens = rng.choice([90, 95])
    fpr = rng.choice([1, 2, 5])
    sick = users * prev / 100
    tp = sick * sens / 100
    fp = (users - sick) * fpr / 100
    ppv = tp / (tp + fp) * 100
    stem = (f'A smartwatch feature alerts users to a possible heart-rhythm problem. Among {users:,} users, {prev}% have the condition. The feature detects {sens}% of real cases and wrongly alerts {fpr}% of healthy users. '
            f'Calculate the number of true alerts, false alerts and the percentage of alerts that are correct.')
    ans = f'{tp:,.0f} true, {fp:,.0f} false; {pc(ppv)}% of alerts correct'
    key = f'Real cases = {sick:,.0f}; true alerts = {sens}% × {sick:,.0f} = {tp:,.0f} [A1]; false = {fpr}% × {users - sick:,.0f} = {fp:,.0f} [A1]; {tp:,.0f} ÷ ({tp:,.0f} + {fp:,.0f}) = {pc(ppv)}% [M1 A1].'
    m = 4
    if slot.d >= 5:
        stem += ' Explain one consequence for health services.'
        ans += '; many worried healthy users seek appointments, increasing demand and anxiety (over-diagnosis), though some real cases are caught early'
        key += ' Consequence for health services explained [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch07-st2', F(
    terms=[('telemedicine', 'providing health care remotely using telecommunications, such as video consultations and remote monitoring'),
           ('wearable health technology', 'devices worn on the body, such as smartwatches and fitness bands, that monitor health data like heart rate, sleep and activity'),
           ('remote patient monitoring', 'collecting health data from patients at home and sending it to clinicians, e.g. blood-glucose sensors'),
           ('smart grid', 'an electricity network that uses digital communication and sensors to balance supply and demand efficiently, including renewables'),
           ('environmental monitoring', 'using sensors, satellites and data analysis to observe environmental conditions such as air quality, deforestation or emissions'),
           ('digital twin', 'a virtual model of a physical system (a city, factory or ecosystem) updated with real-time data to simulate and plan')],
    facts=[('What is India\'s national telemedicine service called?', 'eSanjeevani', ['Aadhaar', 'DigiLocker', 'BharatNet'], 'It has delivered well over 100 million consultations.'),
           ('Which platform, run by the World Resources Institute, uses satellite data to send near-real-time deforestation alerts?', 'Global Forest Watch', ['Google Earth Engine only', 'Copernicus', 'OpenStreetMap'], 'GLAD alerts help authorities and communities respond.'),
           ('In 2016 Google DeepMind reported that machine learning cut the energy used for cooling in Google data centres by up to what share?', '40%', ['4%', '90%', '15%'], 'Later (2018) the AI was given direct, autonomous control of cooling.'),
           ('Which UK health-tech company, once valued at more than US$2 billion and offering AI symptom-checking, collapsed in 2023?', 'Babylon Health', ['DeepMind Health', 'Ada Health', 'Push Doctor'], 'Its business model proved unsustainable.')],
    why=[('Explain why telemedicine expanded rapidly during COVID-19.', 'Lockdowns and infection risks made in-person visits difficult, so governments relaxed rules and providers moved to video and phone consultations, which patients and doctors then became used to.'),
         ('Explain why wearable health data raises privacy concerns.', 'It is sensitive, continuous data that can reveal health conditions, pregnancy or habits; it may be shared with insurers, employers or advertisers, and is often less protected than medical records.'),
         ('Explain why digital technology can help reduce environmental impacts.', 'Sensors and data allow more efficient use of energy and resources (smart grids, precision agriculture), monitoring of pollution and deforestation, and remote working that reduces travel.')],
    contrast=[('telemedicine', 'in-person care', 'Telemedicine provides care remotely, saving travel time and reaching distant patients, but limits physical examination; in-person care allows full examination and relationship but requires travel.'),
              ('the environmental benefits of digital technology', 'the environmental costs of digital technology', 'Benefits include efficiency and monitoring (smart grids, Global Forest Watch); costs include energy use by data centres, mining of minerals and e-waste.')],
    misc=[('Telemedicine gives everyone equal access to health care.', 'Access depends on connectivity, devices, digital skills and language; without these, telemedicine can widen the health divide.'),
          ('Smart technology always saves energy.', 'Devices, networks and data centres consume energy and resources; rebound effects (using more because it is efficient) can cancel savings.')],
    cases=[('eSanjeevani (India)', 'India\'s eSanjeevani connects patients at health and wellness centres with doctors through video consultations; usage surged during and after COVID-19.', 'health context',
            'telemedicine extended specialist access to rural areas, though connectivity and digital literacy limit reach.'),
           ('Global Forest Watch', 'Global Forest Watch combines satellite imagery with algorithms to detect tree-cover loss and alert users within days; it has supported enforcement in countries such as Peru and Brazil.', 'environmental context',
            'open data makes deforestation visible to governments, journalists and communities, supporting accountability.'),
           ('DeepMind and data-centre cooling', 'Google used DeepMind machine learning to optimise cooling in its data centres, reporting up to 40% less cooling energy.', 'technology addressing its own environmental footprint',
            'AI improved efficiency, though overall data-centre energy demand has continued to grow with AI use.')],
    sources=[('"The Apple Watch ECG app is not intended to replace traditional methods of diagnosis."', 'Apple, ECG app labelling following US FDA clearance, 2018',
              'Explain why this warning is included.', 'Wearable readings can produce false positives and negatives; the device is a screening aid, and medical diagnosis requires clinicians and full tests.'),
             ('"Alerts from Global Forest Watch allowed rangers to reach illegal logging sites within days instead of months."', 'Conservation officer in Peru, interviewed for a 2021 report',
              'Explain how this source illustrates the use of digital technology in the environmental context.', 'Satellite monitoring and automated alerts speed up detection of deforestation, enabling faster enforcement and protection of forests.')],
    evaluate=[('Digital technology has improved health care more than any other area of life.',
               ['telemedicine, wearables and AI diagnosis', 'pandemic tracking and vaccine research'],
               ['data breaches and privacy risks', 'unequal access and over-diagnosis', 'other contexts (finance, communication) transformed as much'],
               'Digital health has brought major gains, but they are uneven and accompanied by new risks; comparisons with other contexts depend on criteria.'),
              ('Digital technology is essential for tackling climate change.',
               ['smart grids integrate renewables', 'monitoring and modelling (satellites, digital twins)'],
               ['ICT\'s own emissions and energy demand are rising (AI)', 'political will matters more than technology', 'rebound effects'],
               'Digital technology is an important tool but not sufficient; it must be paired with policy and its own footprint reduced.')],
    extended=[('Evaluate the impact of telemedicine or wearable technology on one community, considering health and social contexts.', 'Example (eSanjeevani, Apple Watch AFib, remote glucose monitoring); benefits (access, early detection); limitations (connectivity, skills, false alarms, privacy); stakeholders; judgement.', 8, 'long')],
))


@R.add('ch07-st3', 'C3', (1, 4), 'numerical')
def digitise_archive(rng, slot):
    items = rng.choice([40000, 120000, 500000, 2000000])
    rate = rng.choice([150, 400, 1000, 2500])  # per day
    days = rng.choice([220, 250])
    yrs = items / (rate * days)
    if yrs < 0.5:
        return None
    what = rng.choice(['historic manuscripts in a national library', 'audio recordings of oral histories', 'photographs in a city archive', 'pages of colonial-era newspapers'])
    stem = f'A heritage project must digitise {items:,} {what}. A digitisation team can scan {rate:,} items per working day, working {days} days a year. Calculate how many years digitisation will take.'
    ans = f'{yrs:.1f} years'
    key = f'{rate:,} × {days} = {rate * days:,} items/year [M1]; {items:,} ÷ {rate * days:,} = {yrs:.1f} years [A1].'
    m = 2
    if slot.d >= 3:
        stem += ' Explain one benefit and one risk of digitising cultural heritage.'
        ans += '; benefit: preservation and global access; risk: loss of control by source communities, long-term digital preservation (file formats, storage) or commercial ownership'
        key += ' Benefit [R1]; risk [R1].'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch07-st3', F(
    terms=[('cultural preservation (digital)', 'using digitisation, 3D scanning and online archives to protect and share cultural heritage'),
           ('digital colonialism', 'the domination of digital infrastructure, data and platforms by powerful (often foreign) companies or states, extracting value from other societies'),
           ('epistemic authority', 'recognised status as a reliable source of knowledge, traditionally held by experts and institutions'),
           ('knowledge commons', 'knowledge resources shared and governed collectively, such as Wikipedia or open-access research'),
           ('language technology gap', 'the shortage of AI and digital tools (translation, voice assistants) for low-resource languages'),
           ('Indigenous data sovereignty', 'the right of Indigenous peoples to govern the collection, ownership and use of data about their communities, expressed in the CARE principles')],
    facts=[('Approximately how many of the world\'s 7,000 languages are well supported by major AI language tools?', 'Only a small number (around 100 or fewer)', ['All of them', 'About 5,000', 'None'], 'Most languages are "low-resource" with little digital text.'),
           ('Which set of principles (Collective benefit, Authority to control, Responsibility, Ethics) guides Indigenous data governance?', 'The CARE principles', ['The FAIR principles', 'The POUR principles', 'The CRAAP test'], 'Developed by the Global Indigenous Data Alliance (2019).'),
           ('After the 2019 fire at Notre-Dame de Paris, which digital resource helped restoration?', 'Detailed 3D laser scans made earlier by art historian Andrew Tallon', ['A video game only', 'Social-media posts only', 'Satellite weather data'], 'Tallon scanned the cathedral in 2010.'),
           ('Which online encyclopaedia is written and edited by volunteers in over 300 languages?', 'Wikipedia', ['Britannica', 'Encarta', 'Baidu Baike only'], 'English is the largest edition.')],
    why=[('Explain why AI may threaten linguistic and cultural diversity.', 'AI tools are trained mostly on dominant languages such as English, so speakers of low-resource languages get poorer services and may shift to dominant languages, while AI-generated content reflects mainly dominant cultural perspectives.'),
         ('Explain why generative AI challenges traditional epistemic authority.', 'People increasingly get answers from chatbots rather than experts, libraries or encyclopaedias; AI outputs may be fluent but unreliable and unattributed, making it harder to know who is responsible for knowledge.'),
         ('Explain why digitising cultural heritage raises questions of ownership.', 'Digital copies may be controlled by museums in other countries or by tech companies, and source communities (e.g. Indigenous peoples) may not have consented or be able to decide how sacred or sensitive material is shared.')],
    contrast=[('digital preservation', 'digital repatriation', 'Digital preservation creates and stores digital copies to protect heritage; digital repatriation returns digital copies (and control over them) to source communities.'),
              ('a knowledge commons', 'proprietary knowledge platforms', 'A knowledge commons (Wikipedia, open-access journals) is shared and collectively governed; proprietary platforms (paywalled databases, closed AI models) are owned by companies that control access.')],
    misc=[('Digitising cultural artefacts always benefits the communities they come from.', 'Without consent and control, digitisation can expose sacred material, transfer value to outside institutions and continue colonial patterns of ownership.'),
          ('AI chatbots are neutral sources of knowledge.', 'They reflect the data, languages and values in their training and the choices of their developers, so they can reproduce bias and errors.')],
    cases=[('Notre-Dame de Paris 3D scans', 'Art historian Andrew Tallon used laser scanning in 2010 to create a detailed 3D model of Notre-Dame; after the 2019 fire, the data helped architects plan restoration.', 'cultural preservation',
            'digital records preserved knowledge of the building that physical damage destroyed, supporting cultural heritage.'),
           ('Masakhane and African-language NLP', 'Masakhane is a grassroots research community building natural-language-processing tools for African languages, created by African researchers.', 'closing the language technology gap',
            'community-led research challenges digital colonialism by building tools in and for under-served languages.'),
           ('Wikipedia and ChatGPT', 'Wikipedia is a major source of training data for large language models, while AI-generated summaries may reduce visits to Wikipedia and its volunteer editing base.', 'AI and the human knowledge context',
            'AI depends on a human knowledge commons it may also weaken, raising questions about the sustainability of shared knowledge.')],
    sources=[('"Data about us, without us, is not for us."', 'Slogan used in the Indigenous data sovereignty movement',
              'Explain what the source means.', 'Data about Indigenous communities collected or used without their participation and control does not serve their interests; communities should govern their own data.'),
             ('"If your language isn\'t on the internet, your children will think it doesn\'t matter."', 'Speaker of a minority language at a UNESCO event during the International Decade of Indigenous Languages (2022–2032)',
              'Explain how this source relates to cultural contexts in digital society.', 'Digital presence affects the status and survival of languages; absence from online spaces and AI tools can push young people towards dominant languages, threatening cultural identity.')],
    evaluate=[('AI will weaken human knowledge more than it strengthens it.',
               ['hallucinations and misinformation', 'erosion of expertise and sources (fewer Wikipedia visits)', 'homogenisation of perspectives'],
               ['faster access to information and translation', 'research acceleration (AlphaFold protein structures)', 'tools for low-resource languages'],
               'AI can strengthen knowledge where it is transparent, verifiable and supports human sources; it weakens knowledge when it replaces them uncritically.'),
              ('Digital technology is the best way to preserve endangered cultures.',
               ['recording languages, songs and stories', 'global access and education'],
               ['culture lives in communities, not files', 'digital preservation needs funding and formats can become obsolete', 'consent and ownership concerns'],
               'Digital tools are valuable when led by communities, but cannot replace intergenerational transmission and support for living cultures.')],
    extended=[('Analyse how a digital technology has affected one culture or knowledge system, linking the cultural and human knowledge contexts.', 'E.g. Masakhane, Wikipedia in minority languages, AI chatbots in education, digitisation of Timbuktu manuscripts or Indigenous archives; concepts (identity, power, values); impacts and implications; judgement.', 8, 'long')],
))

# =============================================================================================
# Shared HL helper: weighted decision matrix for evaluating interventions
# =============================================================================================
INTERVENTION_SETS = [
    ('reducing harm to teenagers on social media', ['age-verification law', 'default "teen accounts" with limits', 'school digital-wellbeing lessons']),
    ('closing the rural connectivity gap', ['satellite broadband vouchers', 'community Wi-Fi hubs', 'subsidised mobile data plans']),
    ('reducing e-waste from smartphones', ['right-to-repair law', 'deposit-return scheme for phones', 'longer software-support requirement']),
    ('protecting journalists from spyware', ['export controls on spyware', 'free security audits for journalists', 'a ban on government use of spyware']),
    ('reducing misinformation during elections', ['prebunking campaigns', 'labels on AI-generated content', 'limits on micro-targeted political ads']),
]


def decision_matrix(rng, slot):
    goal, opts = rng.choice(INTERVENTION_SETS)
    crit = rng.sample(['effectiveness', 'cost', 'feasibility', 'impact on rights', 'speed of implementation', 'equity'], 3)
    w = rng.choice([(0.5, 0.3, 0.2), (0.4, 0.4, 0.2), (0.6, 0.2, 0.2), (0.4, 0.3, 0.3)])
    sc = [[rng.randint(1, 5) for _ in range(3)] for _ in range(3)]
    tot = [round(sum(wi * s for wi, s in zip(w, row)), 2) for row in sc]
    if len(set(tot)) < 3:
        return None
    best = opts[tot.index(max(tot))]
    tbl = '\n'.join(f'{o}: ' + ', '.join(f'{c} {s}' for c, s in zip(crit, row)) for o, row in zip(opts, sc))
    stem = (f'A government is choosing an intervention for {goal}. Each option is scored 1–5 (5 = best) on {crit[0]} (weight {w[0]}), {crit[1]} (weight {w[1]}) and {crit[2]} (weight {w[2]}).\n{tbl}\n'
            f'Calculate the weighted score of each option and identify which should be recommended.')
    ans = '; '.join(f'{o} {t:g}' for o, t in zip(opts, tot)) + f'; recommend {best}'
    key = '; '.join(f'{o}: ' + ' + '.join(f'{wi}×{s}' for wi, s in zip(w, row)) + f' = {t:g}' for o, row, t in zip(opts, sc, tot)) + f' [M1 A1 A1]; highest = {best} [A1].'
    m = 4
    if slot.d >= 4:
        stem += ' Explain one limitation of using a weighted matrix to choose an intervention.'
        ans += '; scores and weights are subjective and may reflect the priorities of decision-makers rather than affected stakeholders; it may hide unintended consequences'
        key += ' Subjectivity of weights/scores; stakeholder voice; unmeasured effects [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


# =============================================================================================
# ch08 HL challenge 5.1 Global well-being
# =============================================================================================
@R.add('ch08-st1', 'C3', (1, 4), 'numerical')
def wellbeing_survey(rng, slot):
    n = rng.choice([800, 1500, 2400, 5000])
    a = rng.randint(25, 60)
    b = rng.randint(10, a - 5)
    harm = rng.choice(['say social media makes them feel worse about their body', 'report losing sleep because of late-night phone use', 'have experienced online bullying in the past year', 'feel "addicted" to a social-media app'])
    g1, g2 = rng.choice([('girls', 'boys'), ('14–16-year-olds', '11–13-year-olds'), ('heavy users (4+ hours a day)', 'light users (under 1 hour)')])
    stem = (f'A survey of {n:,} teenagers in {rng.choice(["the UK", "Australia", "Brazil", "South Korea", "Canada", "the Philippines"])} found that {a}% of {g1} and {b}% of {g2} {harm}. '
            f'Calculate the difference in percentage points and how many times more likely {g1} were to report this.')
    ans = f'{a - b} percentage points; {a / b:.2g} times'
    key = f'{a} − {b} = {a - b} pp [A1]; {a} ÷ {b} = {a / b:.2g} [M1 A1].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain why this survey does not prove that social media causes the harm.'
        ans += '; it shows correlation; self-reported data; other factors (e.g. existing anxiety) may cause both; direction of causation unclear'
        key += ' Correlation vs causation; self-report; confounders/reverse causation [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch08-st1', F(
    terms=[('global well-being', 'the physical, mental and social health and quality of life of people around the world, which digital technologies can improve or harm'),
           ('digital health', 'the use of digital technologies – telemedicine, apps, wearables, health records and AI – to improve health and health care'),
           ('online harms', 'harmful experiences online, such as cyberbullying, harassment, exposure to self-harm content, exploitation and scams'),
           ('problematic smartphone use', 'patterns of smartphone use that interfere with sleep, relationships, work or well-being'),
           ('cyberbullying', 'repeated bullying through digital technologies, such as threatening messages, exclusion or sharing humiliating content'),
           ('duty of care (online)', 'a legal or ethical obligation on platforms to take reasonable steps to protect users, especially children, from foreseeable harms')],
    facts=[('In 2022, a UK coroner concluded that online content contributed "in a more than minimal way" to the death of which teenager?', 'Molly Russell', ['Amanda Todd', 'Elaine Herzberg', 'Greta Thunberg'], 'The inquest examined Instagram and Pinterest content she had viewed.'),
           ('In 2023, which US official issued an advisory warning about the effects of social media on youth mental health?', 'The Surgeon General, Vivek Murthy', ['The Secretary of State', 'The FBI Director', 'The FCC Chair'], 'He later called for warning labels on social media (2024).'),
           ('Which 2021 leak showed that Instagram\'s internal research found it made body image issues worse for "one in three teen girls"?', 'The Facebook Files (Frances Haugen)', ['The Pentagon Papers', 'The Panama Papers', 'Vault 7'], 'Published by the Wall Street Journal.'),
           ('In 2024 which country passed a law setting a minimum age of 16 for social-media accounts?', 'Australia', ['Japan', 'Germany', 'Mexico'], 'The Online Safety Amendment (Social Media Minimum Age) Act 2024 took effect in December 2025.')],
    why=[('Explain why the impact of social media on teenagers\' mental health is difficult to establish.', 'Studies are mostly correlational and self-reported; effects vary by individual, platform and type of use; heavy use may be a symptom as well as a cause; and researchers have limited access to platform data.'),
         ('Explain why digital technologies can improve global well-being.', 'They extend health information and services (telemedicine, mobile health messaging), connect isolated people, support mental-health apps and crisis lines, and enable early warning in emergencies.'),
         ('Explain why online harms are a global rather than national challenge.', 'Platforms operate across borders, harmful content and abusers can be anywhere, and national laws reach only part of the problem, so cooperation and global platform standards are needed.')],
    contrast=[('online harms', 'offline harms', 'Online harms occur through digital platforms and can be persistent, anonymous, and spread rapidly to large audiences (e.g. cyberbullying 24/7); offline harms occur in physical settings and are usually more limited in reach and visibility.'),
              ('digital health opportunities', 'digital well-being risks', 'Opportunities include better access to care, monitoring and information; risks include addiction, misinformation, privacy breaches and exposure to harmful content.')],
    misc=[('Screen time is the main cause of the teenage mental-health crisis.', 'Researchers disagree: some (e.g. Jonathan Haidt) argue phones and social media are a major cause, while others (e.g. Candice Odgers, Amy Orben) find small average effects and point to other factors; type of use matters more than total time.'),
          ('Online harms only affect children.', 'Adults also face harassment, scams, misinformation and image-based abuse; women journalists and public figures are frequent targets.')],
    cases=[('the Molly Russell inquest (2022)', '14-year-old Molly Russell died in 2017 after viewing large amounts of self-harm and depression content on Instagram and Pinterest; the coroner concluded online content contributed to her death.', 'online harms and well-being',
            'the case linked recommendation algorithms to real harm and influenced the UK Online Safety Act 2023.'),
           ('the Facebook Files (2021)', 'Frances Haugen leaked internal research showing Meta knew Instagram could worsen body image and anxiety for some teenage girls.', 'corporate knowledge of digital harms',
            'evidence that a company knew of harms intensified calls for duties of care and transparency.'),
           ('mHealth messaging in Africa', 'Programmes such as MomConnect in South Africa (launched 2014) send pregnant women health information by SMS and WhatsApp, reaching millions of users.', 'digital technology improving well-being',
            'low-cost mobile messaging extended maternal health information at scale, showing positive impacts on well-being.')],
    sources=[('"We make body image issues worse for one in three teen girls."', 'Internal Instagram research slide (2019), published in the Wall Street Journal\'s Facebook Files, 2021',
              'With reference to the source, explain why it is significant evidence.', 'It comes from the company\'s own research, so it is hard to dismiss as outside criticism; it suggests the company knew its product could harm some users\' well-being.'),
             ('"It\'s time to require a surgeon general\'s warning label on social media platforms."', 'Vivek Murthy, US Surgeon General, New York Times op-ed, June 2024',
              'Explain the perspective expressed in the source.', 'It treats social media as a public-health risk comparable to tobacco, arguing that users and parents need warnings about potential harm to young people\'s mental health.')],
    evaluate=[('Social media does more harm than good to young people\'s well-being.',
               ['links to anxiety, body image issues, sleep loss (Facebook Files)', 'harmful content and cyberbullying (Molly Russell)'],
               ['support communities, creativity and connection', 'research shows small average effects and wide variation', 'benefits for marginalised youth (LGBTQ+)'],
               'Social media harms some young people significantly, especially vulnerable users, but benefits others; design and use matter more than presence or absence.'),
              ('Digital technologies have improved global health more than they have harmed it.',
               ['telemedicine, mHealth and disease surveillance', 'information access'],
               ['misinformation (COVID infodemic)', 'mental-health and sedentary-lifestyle concerns', 'unequal access'],
               'Overall health benefits are substantial, but harms to mental health and information quality require interventions.')],
    extended=[('With reference to one specific challenge to global well-being, analyse its causes and evaluate its impacts on different stakeholders.', 'E.g. teenage mental health and social media; online gambling; health misinformation; causes (design, business models, social factors); stakeholders (young people, parents, platforms, health services); evidence; judgement.', 8, 'long')],
))

R.facts('ch08-st2', F(
    terms=[('intervention', 'a deliberate action by a government, organisation or community to address a challenge, such as a law, design change or education programme'),
           ('Online Safety Act 2023 (UK)', 'a UK law giving Ofcom powers to require platforms to protect users, especially children, from illegal and harmful content'),
           ('safety by design', 'building protections into products from the start, such as private-by-default accounts for children'),
           ('Age Appropriate Design Code', 'the UK code (2021) requiring online services likely to be used by children to apply 15 standards, such as high privacy by default'),
           ('digital well-being features', 'tools such as screen-time limits, quiet modes and reminders that help users manage technology use'),
           ('age assurance', 'methods of estimating or verifying a user\'s age, such as ID checks or facial age estimation')],
    facts=[('Which regulator enforces the UK Online Safety Act?', 'Ofcom', ['The ICO', 'The BBC', 'The Competition and Markets Authority'], 'Fines can reach £18 million or 10% of global turnover.'),
           ('Which country limited online gaming for minors in 2021 to one hour on Fridays, weekends and public holidays?', 'China', ['South Korea', 'Japan', 'Finland'], 'The rule applied from 8 to 9 p.m.'),
           ('What did Instagram introduce in 2024 that places users under 18 into private, more restricted accounts by default?', 'Teen Accounts', ['Close Friends', 'Reels', 'Threads'], 'Under-16s need parental permission to change settings.'),
           ('Which UK code, in force from 2021, requires high privacy settings by default for children?', 'The Age Appropriate Design Code (Children\'s Code)', ['The Highway Code', 'The DSA', 'The Online Harms White Paper'], 'It influenced design changes by YouTube, TikTok and Instagram.')],
    why=[('Explain why design changes can be more effective than education alone in protecting users.', 'Defaults shape behaviour for millions automatically (most users never change settings), whereas education depends on individuals remembering and choosing to act.'),
         ('Explain why age verification is a controversial intervention.', 'It may protect children from harmful content, but requires collecting personal data or biometric scans, raises privacy and security risks, can exclude people without ID, and can be bypassed with VPNs.'),
         ('Explain why regulation of online harms often gives powers to an independent regulator.', 'Regulators such as Ofcom or Australia\'s eSafety Commissioner can set codes, investigate, demand information and fine platforms, providing ongoing oversight rather than relying on courts or company promises.')],
    contrast=[('a legislative intervention', 'a design intervention', 'A legislative intervention uses law to impose duties and penalties (e.g. Online Safety Act); a design intervention changes the product itself (e.g. private-by-default teen accounts).'),
              ('a ban', 'a duty of care', 'A ban prohibits an activity outright (e.g. under-16s on social media in Australia); a duty of care requires platforms to assess and reduce risks while still allowing use.')],
    misc=[('Banning children from social media will solve online harms.', 'Bans can be bypassed (false ages, VPNs), may push children to less regulated spaces, cut off benefits, and do not address harms to adults or platform design.'),
          ('Digital well-being features are designed mainly to help users.', 'They can help, but companies also introduce them in response to regulatory and public pressure; they are usually optional and may be less prominent than engagement features.')],
    cases=[('the UK Online Safety Act 2023', 'The Act requires platforms to assess and reduce risks of illegal content and protect children from harmful content, enforced by Ofcom with fines up to 10% of global turnover; children\'s codes applied from 2025.', 'a regulatory intervention for well-being',
            'it creates legal duties of care, but critics raise concerns about privacy (encryption) and over-removal.'),
           ("Australia's social-media minimum age law (2024)", 'Australia legislated that platforms must take reasonable steps to prevent under-16s having accounts, with fines up to A$49.5 million; it took effect in December 2025.', 'a ban as an intervention',
            'it is one of the strictest interventions globally, testing whether age-based bans can be enforced and whether they improve well-being.'),
           ("China's limits on minors' online gaming (2021)", 'Regulators limited under-18s to one hour of online gaming on Fridays, weekends and holidays, enforced by real-name verification.', 'state intervention in digital well-being',
            'strict limits reduced gaming time for many minors, but relied on identity verification and state control that raise privacy concerns.')],
    sources=[('"Settings must be \'high privacy\' by default, unless you can demonstrate a compelling reason for a different default setting."', 'UK Information Commissioner\'s Office, Age Appropriate Design Code, Standard 7',
              'Explain how this standard is an example of safety by design.', 'It requires protection to be built into default settings, so children are protected automatically without needing to change settings themselves.'),
             ('"Kids will find a way around it, and we\'ll push them into darker corners of the internet."', 'Digital-rights advocate commenting on Australia\'s under-16 social-media law, 2024',
              'Explain one possible unintended consequence of the intervention suggested by the source.', 'Children may lie about their age or use unregulated platforms, where harms may be greater and there are fewer protections.')],
    evaluate=[('Legislation is the most effective intervention for protecting young people online.',
               ['binding duties and fines (Online Safety Act, DSA)', 'changes platform incentives at scale'],
               ['enforcement is slow and complex', 'may harm privacy or free expression', 'education and parental support also necessary'],
               'Legislation is powerful when combined with safety-by-design requirements and education; on its own it is insufficient.'),
              ('Raising the minimum age for social media will improve young people\'s well-being.',
               ['reduces exposure to harmful content and comparison', 'gives parents support to set limits'],
               ['easy to bypass; age verification raises privacy issues', 'loss of social connection and support', 'evidence of causal benefit is limited'],
               'Age limits may help some young people, but effectiveness depends on enforcement and on improving platform design for all users.')],
    extended=[('Evaluate one intervention designed to improve young people\'s well-being online.', 'E.g. UK Online Safety Act, Australia\'s under-16 law, Instagram Teen Accounts, Children\'s Code; aims; evidence; stakeholders; unintended consequences; recommendation.', 8, 'long')],
))

R.add('ch08-st3', 'C3', (2, 5), 'numerical')(decision_matrix)

R.facts('ch08-st3', F(
    terms=[('stakeholder', 'any individual, group or organisation affected by or able to influence an intervention'),
           ('effectiveness', 'the extent to which an intervention achieves its intended goals'),
           ('unintended consequence', 'an outcome of an intervention that was not planned or expected, which may be positive or negative'),
           ('feasibility', 'how practical an intervention is to implement given costs, technology, politics and time'),
           ('trade-off', 'a situation in which gaining one benefit means accepting a cost or loss elsewhere, such as safety versus privacy'),
           ('evaluation criteria', 'the standards used to judge an intervention, such as effectiveness, cost, equity, rights and sustainability')],
    facts=[('Which of these is an example of an unintended consequence of an online safety intervention?', 'Age checks leading users to share ID documents with insecure third-party sites', ['Fewer children seeing harmful content', 'Platforms publishing risk assessments', 'Parents receiving guidance'], 'Unintended consequences can create new risks.'),
           ('Which criterion asks whether an intervention benefits different groups fairly?', 'Equity', ['Speed', 'Profitability', 'Popularity'], 'Equity considers distribution of benefits and burdens.'),
           ('In a Paper 3 response, which is the strongest way to evaluate an intervention?', 'Weigh its effectiveness and limitations for different stakeholders using evidence, then reach a justified conclusion', ['Describe the intervention in detail', 'List every stakeholder without analysis', 'Give only your personal opinion'], 'Evaluation requires balanced, evidence-based judgement.'),
           ('Which stakeholder is most directly affected by a platform\'s decision to remove "like" counts?', 'Users and content creators', ['Undersea-cable operators', 'Satellite manufacturers', 'Data-centre cooling engineers'], 'Instagram tested hiding like counts from 2019.')],
    why=[('Explain why the same intervention can affect stakeholders differently.', 'Stakeholders have different needs, resources and power: an age-verification law may protect children but burden adults\' privacy, cost small platforms more than large ones and exclude people without ID.'),
         ('Explain why unintended consequences should be considered when evaluating interventions.', 'Interventions change behaviour in complex systems; ignoring side effects (displacement, privacy loss, chilling effects) can make an intervention harmful overall even if it meets its main goal.'),
         ('Explain why evidence of effectiveness is often limited for digital interventions.', 'Many are new, platforms control the data, outcomes such as well-being are hard to measure, and it is difficult to isolate the effect of one intervention from other changes.')],
    contrast=[('effectiveness', 'efficiency', 'Effectiveness is whether an intervention achieves its goal; efficiency is whether it does so at reasonable cost relative to alternatives.'),
              ('short-term impacts', 'long-term implications', 'Short-term impacts are immediate effects (e.g. fewer accounts for under-16s); long-term implications are wider consequences over time (e.g. changes in youth culture, normalisation of ID checks online).')],
    misc=[('An intervention that achieves its main goal is a success.', 'It may still have serious unintended consequences or unfair impacts on some stakeholders, and may be too costly or infringe rights; evaluation must consider all of these.'),
          ('Stakeholder analysis only needs to consider the people the intervention is designed to help.', 'It should also consider those who implement it, pay for it, are restricted by it, or are indirectly affected.')],
    cases=[('Instagram hiding like counts (2019–2021)', 'Instagram tested hiding like counts to reduce social comparison; in 2021 it made hiding optional after finding mixed effects.', 'evaluating a design intervention',
            'results varied between users, showing that interventions can have uneven effects and need evaluation with data.'),
           ('WhatsApp forwarding limits', 'WhatsApp limited forwarding (2018–2020), reporting a 70% fall in highly forwarded messages, while preserving end-to-end encryption.', 'measuring effectiveness',
            'a clear metric showed the intervention changed behaviour, though its effect on actual harm (violence) is harder to measure.'),
           ('age verification for adult websites in parts of the US', 'Several US states required age verification for adult sites from 2023; some major sites withdrew from those states and VPN searches rose.', 'unintended consequences',
            'users shifted to VPNs and less regulated sites, showing how interventions can displace rather than reduce harm.')],
    sources=[('"Hiding like counts made some people feel better, but others found it annoying. So we\'re giving people the choice."', 'Paraphrase of Instagram\'s announcement, May 2021',
              'With reference to the source, explain why the intervention was changed.', 'Its effects were mixed across users – beneficial for some, unwelcome for others – so Instagram made it optional rather than universal.'),
             ('"After the law came into force and a major adult site withdrew from the state, demand for VPNs there rose by several hundred per cent within days."', 'VPN provider analysis following a US state age-verification law, 2023',
              'Explain what this source suggests about the effectiveness of the intervention.', 'Users may bypass the law with VPNs, so it may displace rather than reduce access, limiting effectiveness and creating unintended consequences.')],
    evaluate=[('The most important criterion for evaluating a digital intervention is its effectiveness.',
               ['an ineffective intervention wastes resources', 'effectiveness is the purpose of intervening'],
               ['rights, equity and unintended consequences matter', 'a highly effective intervention can be disproportionate (e.g. shutdowns)', 'feasibility and cost determine whether it can be sustained'],
               'Effectiveness is central, but must be weighed against rights, equity and side effects to judge whether an intervention is justified.'),
              ('Platforms should be required to share data so that interventions can be independently evaluated.',
               ['independent evidence on what works', 'DSA Article 40 researcher access'],
               ['privacy and security risks', 'commercial confidentiality', 'data may be misused'],
               'Vetted researcher access with privacy safeguards, as under the DSA, is justified to evaluate interventions properly.')],
    extended=[('Using a real intervention, evaluate its effectiveness for three stakeholders and recommend one improvement.', 'Choose (e.g. Australia under-16 law, Online Safety Act, Teen Accounts, WhatsApp limits); stakeholders (young people, parents, platforms, regulators); evidence; unintended consequences; justified recommendation.', 8, 'long')],
))

INTV['ch08'] = [
    ('Australia\'s social-media minimum age law', 'From December 2025 Australian law requires social-media platforms to take reasonable steps to stop under-16s from having accounts, with fines of up to A$49.5 million. The government argues it protects children\'s mental health; critics worry about privacy, age-checking technology and young people losing online support networks.',
     'Concern that social media harms young people\'s mental health through harmful content, social comparison, cyberbullying and compulsive use, while platforms have little incentive to restrict engagement.',
     ['under-16s – reduced exposure to harms but loss of social connection and support communities', 'parents – support in setting limits', 'platforms – age-assurance costs and loss of young users', 'all users – may need to prove age, raising privacy concerns'],
     ['clear rule that shifts responsibility to platforms', 'strong penalties', 'popular with many parents'],
     ['easy to bypass; age assurance imperfect', 'privacy risks of age checks', 'may push young people to less safe spaces; limited causal evidence'],
     'Combine the age limit with safety-by-design duties for all platforms and independent evaluation of well-being outcomes, with privacy-preserving age assurance.'),
    ('the UK Online Safety Act 2023', 'The Act gives Ofcom powers to require online services to assess and reduce risks of illegal content and protect children from harmful content such as self-harm and pornography, with fines up to £18 million or 10% of global turnover. The Molly Russell inquest was a key influence.',
     'Young people and adults were exposed to illegal and harmful content, often amplified by recommendation algorithms, with platforms largely self-regulating.',
     ['children – safer feeds and age checks', 'adults – possible privacy concerns and over-removal', 'large platforms – risk assessments and compliance', 'small services – disproportionate compliance burden', 'Ofcom – large new regulatory task'],
     ['duty-of-care approach targets systems, not only content', 'strong enforcement powers', 'children\'s codes specific and auditable'],
     ['complex and slow to implement', 'concerns about encryption and privacy', 'risk of over-cautious removal of lawful content'],
     'Publish clear, measurable outcomes for children\'s safety and require independent researcher access to platform data to evaluate impact.'),
    ('Instagram Teen Accounts', 'In 2024 Instagram placed users under 18 into "Teen Accounts" that are private by default, restrict messaging from strangers, limit sensitive content and send sleep-mode reminders; under-16s need parental permission to loosen settings.',
     'Teenagers on Instagram were exposed to unwanted contact, harmful content and late-night use, with growing regulatory and legal pressure on Meta.',
     ['teenagers – more protection but less autonomy', 'parents – more control and oversight tools', 'Meta – reputational benefit and possible reduced engagement', 'regulators – evidence of voluntary compliance'],
     ['protective defaults reach millions automatically', 'fast to implement', 'combines several protections'],
     ['depends on accurate age information', 'company self-assessment, limited independent evaluation', 'teens may move to other apps'],
     'Require independent audits of Teen Account effectiveness and strengthen age assurance in cooperation with regulators.'),
]

# =============================================================================================
# ch09 HL challenge 5.2 Governance and human rights
# =============================================================================================
@R.add('ch09-st1', 'C3', (1, 4), 'numerical')
def gov_requests(rng, slot):
    req = rng.choice([1200, 4500, 18000, 60000])
    comp = rng.choice([45, 60, 72, 85])
    accts = rng.choice([1.5, 2, 3])
    co = rng.choice(['a search company', 'a messaging app', 'a social network', 'a cloud provider'])
    n = req * comp / 100
    stem = (f'A transparency report from {co} shows it received {req:,} government requests for user data in six months and produced some data in {comp}% of cases. '
            f'On average each request concerned {accts:g} accounts. Calculate the number of requests where data was produced and the number of accounts affected.')
    ans = f'{n:,.0f} requests; about {n * accts:,.0f} accounts'
    key = f'{req:,} × {comp}% = {n:,.0f} [M1 A1]; × {accts:g} = {n * accts:,.0f} accounts [A1].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain why transparency reports matter for digital rights.'
        ans += '; they reveal the scale of state access to personal data, allowing public scrutiny and accountability, though they cannot show secret requests (e.g. gag orders)'
        key += ' Accountability/scrutiny of state surveillance; limitation (secret orders, aggregated data) [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch09-st1', F(
    terms=[('digital rights', 'human rights as they apply in the digital environment, including privacy, freedom of expression, access to information and freedom of assembly online'),
           ('right to privacy', 'the right to be free from arbitrary interference with one\'s privacy, family, home and correspondence (UDHR Article 12; ICCPR Article 17)'),
           ('freedom of expression', 'the right to seek, receive and impart information and ideas through any media (UDHR Article 19; ICCPR Article 19)'),
           ('access to information', 'the right to seek and receive information, including through the internet, which the UN Human Rights Council affirmed applies online (2012)'),
           ('proportionality', 'the human-rights principle that restrictions on rights must be necessary, the least intrusive option and balanced against their aim'),
           ('right to be forgotten', 'the right to have certain personal information removed from search results, established by the EU Court of Justice in Google Spain (2014)')],
    facts=[('In 2012 what did the UN Human Rights Council affirm about human rights online?', 'That the same rights people have offline must also be protected online', ['That the internet is outside human-rights law', 'That only governments have rights online', 'That privacy does not apply to digital data'], 'Resolution 20/8.'),
           ('Which 2014 EU Court of Justice case established a "right to be forgotten" in search results?', 'Google Spain v AEPD and Mario Costeja González', ['Schrems II', 'Puttaswamy', 'Loomis'], 'Search engines must consider delisting requests for outdated or irrelevant personal data.'),
           ('Which article of the ICCPR protects freedom of expression?', 'Article 19', ['Article 2', 'Article 9', 'Article 25'], 'Restrictions must be provided by law and necessary.'),
           ('Which 2020 EU Court of Justice ruling, brought by Max Schrems, invalidated the EU–US Privacy Shield?', 'Schrems II', ['Google Spain', 'Breyer', 'Digital Rights Ireland'], 'Concerns over US surveillance of EU data.')],
    why=[('Explain why privacy is described as an enabling right.', 'Privacy allows people to think, communicate, associate and express themselves without fear of surveillance, so it supports other rights such as free expression, assembly and freedom of belief.'),
         ('Explain why digital rights can conflict with each other.', 'Freedom of expression can conflict with privacy (publishing personal information), with protection from harm (hate speech) or with the right to be forgotten (public-interest information), requiring balancing.'),
         ('Explain why access to the internet is increasingly seen as a human right.', 'So many rights – education, work, expression, information, political participation – are exercised online that lack of access excludes people from enjoying them.')],
    contrast=[('a negative right', 'a positive right', 'A negative right requires others (especially states) not to interfere (e.g. no censorship); a positive right requires action to provide something (e.g. state measures to ensure internet access).'),
              ('privacy', 'data protection', 'Privacy is a broad right to a private life free from interference; data protection is a specific set of rules governing how personal data is processed (e.g. GDPR), recognised separately in the EU Charter.')],
    misc=[('Human-rights law only applies to governments, so platforms have no human-rights responsibilities.', 'The UN Guiding Principles on Business and Human Rights (2011) say companies have a responsibility to respect human rights, and laws like the DSA require platforms to consider fundamental rights.'),
          ('Freedom of expression means all speech must be allowed online.', 'Human-rights law permits restrictions that are lawful, necessary and proportionate, e.g. incitement to violence or child sexual abuse material.')],
    cases=[('Google Spain (2014)', 'Mario Costeja González asked Google to delist old newspaper notices about his debts; the EU Court of Justice ruled search engines must remove links to inadequate, irrelevant or outdated personal data on request, unless public interest outweighs privacy.', 'the right to be forgotten',
            'the case balanced privacy against access to information, and Google has since processed over a million delisting requests.'),
           ('Schrems II (2020)', 'Austrian activist Max Schrems challenged transfers of his Facebook data to the US; the EU Court of Justice invalidated the Privacy Shield because of US surveillance laws.', 'privacy across borders',
            'an individual\'s complaint reshaped global data flows, showing how rights litigation can constrain both states and companies.'),
           ('Puttaswamy v Union of India (2017)', 'India\'s Supreme Court unanimously recognised privacy as a fundamental right under Article 21 of the Constitution.', 'privacy as a constitutional right',
            'the ruling became the basis for limiting Aadhaar and for the DPDP Act 2023.')],
    sources=[('"The same rights that people have offline must also be protected online, in particular freedom of expression."', 'UN Human Rights Council Resolution 20/8, 2012',
              'With reference to the source, explain its significance for governments.', 'It confirms that existing human-rights obligations apply online, so states cannot censor, surveil or block online expression in ways that would be unlawful offline.'),
             ('"No one shall be subjected to arbitrary or unlawful interference with his privacy, family, home or correspondence."', 'International Covenant on Civil and Political Rights, Article 17 (1966)',
              'Explain how this source applies to mass digital surveillance.', 'Bulk interception of communications without individual suspicion may be "arbitrary interference" with correspondence, unless lawful, necessary and proportionate.')],
    evaluate=[('Internet access should be recognised as a human right.',
               ['access is necessary for exercising many other rights', 'UN resolutions and some states (e.g. Finland broadband right 2010) recognise it'],
               ['rights should protect fundamental values, not technologies', 'costly obligation for poor states', 'access alone does not guarantee rights (censorship)'],
               'Recognising access as a right, or as essential to other rights, is justified given how much of life is online, though implementation must be progressive.'),
              ('Privacy is the most important digital right.',
               ['enabling right for expression and association', 'surveillance and data exploitation are pervasive'],
               ['freedom of expression and access to information are equally fundamental', 'rights are interdependent', 'importance varies by context (shutdowns vs data brokers)'],
               'Privacy is foundational, but digital rights are interdependent; no single right should be treated as automatically most important.')],
    extended=[('Analyse how one court case has shaped digital rights, and evaluate its impact on different stakeholders.', 'E.g. Google Spain, Schrems II, Puttaswamy, Anuradha Bhasin; facts, ruling, rights balanced; impacts on individuals, companies, governments; limitations; judgement.', 8, 'long')],
))


@R.add('ch09-st2', 'C3', (2, 5), 'numerical')
def shutdown_hours(rng, slot):
    pop = rng.choice([2, 5, 12, 40])  # million affected
    hours = rng.choice([24, 72, 168, 720])
    pen = rng.choice([45, 60, 75])
    users = pop * pen / 100
    uh = users * hours
    stem = (f'A government cuts mobile internet in a region of {pop} million people for {hours} hours during protests. Internet penetration in the region is {pen}%. '
            f'Calculate the number of internet users affected and the total "user-hours" of lost access.')
    ans = f'{users:g} million users; {uh:,.0f} million user-hours'
    key = f'{pop} m × {pen}% = {users:g} m users [M1 A1]; × {hours} h = {uh:,.0f} million user-hours [A1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain why international human-rights bodies consider such shutdowns disproportionate.'
        ans += '; they affect everyone, not only those suspected of wrongdoing, blocking health, emergency, education, work and expression – failing necessity and proportionality tests'
        key += ' Blanket effect on whole population; less intrusive alternatives exist; UNHRC condemns shutdowns [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch09-st2', F(
    terms=[('censorship', 'the suppression or prohibition of information or expression considered objectionable or threatening by authorities'),
           ('internet shutdown', 'an intentional disruption of internet or electronic communications, making them inaccessible or unusable for a population or location'),
           ('throttling', 'deliberately slowing internet speeds to make services hard to use, as Russia did to Twitter in 2021'),
           ('deep packet inspection (DPI)', 'technology that examines the content of data packets, used for filtering, blocking and surveillance'),
           ('mercenary spyware', 'commercial surveillance software such as Pegasus or Predator sold to governments to hack phones'),
           ('Great Firewall', 'China\'s system of laws and technologies for blocking foreign websites and filtering internet content')],
    facts=[('According to Access Now, about how many internet shutdowns were recorded worldwide in 2023?', 'About 280', ['About 3', 'About 28,000', 'About 2,800'], 'Access Now recorded 283 shutdowns in 39 countries in 2023, the highest on record.'),
           ('Which spyware maker was added to the US Commerce Department\'s Entity List in 2021?', 'NSO Group', ['Kaspersky', 'Huawei only', 'Palantir'], 'Following the Pegasus Project revelations.'),
           ('Which country throttled Twitter in March 2021 for allegedly failing to remove banned content?', 'Russia', ['Canada', 'Japan', 'Norway'], 'Roskomnadzor slowed Twitter on mobile and fixed networks.'),
           ('In 2023, how long was Manipur in India under an internet shutdown after ethnic violence began?', 'About seven months (May to December)', ['About one day', 'About one week', 'Ten years'], 'Mobile internet was largely suspended from May 2023.')],
    why=[('Explain why governments use internet shutdowns rather than targeted censorship.', 'Shutdowns are technically simple, immediate and stop all coordination and reporting, whereas targeted censorship needs filtering technology and can be bypassed; but shutdowns affect everyone and harm the economy.'),
         ('Explain why spyware such as Pegasus is a threat to human rights.', 'It can secretly take over phones, reading messages, tracking location and turning on microphones, and has been used against journalists, activists and lawyers, chilling free expression and association.'),
         ('Explain why censorship is harder to detect online than offline.', 'Throttling, algorithmic down-ranking, selective blocking and deletion can look like technical problems, and users may not know what they cannot see.')],
    contrast=[('censorship', 'content moderation', 'Censorship is suppression of expression by authorities, often political; content moderation is a platform enforcing its rules or the law on its service – though states can pressure platforms to censor.'),
              ('a full shutdown', 'platform blocking', 'A full shutdown cuts all internet access in an area; platform blocking restricts specific services (e.g. X, WhatsApp) while leaving other access.')],
    misc=[('Internet shutdowns only happen in authoritarian states.', 'Democracies also impose shutdowns – India records many regional shutdowns – often citing public order or exams.'),
          ('Using a VPN always defeats censorship.', 'VPNs can be blocked, detected by deep packet inspection, banned by law or unusable during full shutdowns.')],
    cases=[('the Pegasus Project (2021)', 'A leak of 50,000 phone numbers of potential targets and forensic analysis by Amnesty International linked NSO\'s Pegasus to surveillance of journalists and activists, including people close to Jamal Khashoggi.', 'surveillance as a human-rights challenge',
            'commercial spyware gave states powerful tools to target civil society, prompting US sanctions and EU inquiries.'),
           ('the Manipur shutdown (2023)', 'Authorities suspended mobile internet in the Indian state of Manipur for months after ethnic violence broke out in May 2023; a video of an assault emerged only in July.', 'internet shutdowns',
            'the shutdown limited the spread of rumours, but also hid human-rights abuses and cut off services for millions.'),
           ('Russia\'s throttling of Twitter (2021) and blocking after 2022', 'Russia slowed Twitter in 2021 and blocked Facebook, Instagram and Twitter after its invasion of Ukraine in 2022, while VPN use surged.', 'state censorship',
            'the state used technical controls to restrict independent information, while citizens resisted with VPNs.')],
    sources=[('"Shutdowns are a blunt instrument: they cut off everyone – the doctor, the journalist, the student – to stop a few."', 'UN Special Rapporteur on freedom of expression, report to the Human Rights Council, 2022',
              'With reference to the source, explain why shutdowns fail the proportionality test.', 'They affect the entire population rather than targeting specific wrongdoing, so the harm to rights is excessive compared with their aim.'),
             ('"Pegasus could turn a phone into a 24-hour surveillance device."', 'Amnesty International Security Lab, Pegasus Project, 2021',
              'Explain one implication of the capability described in the source.', 'Journalists and activists cannot protect sources or communicate safely, which chills investigative journalism and dissent.')],
    evaluate=[('Internet shutdowns can be justified during periods of violent unrest.',
               ['governments claim they stop rumours and coordination of violence', 'short, local measures in emergencies'],
               ['evidence suggests shutdowns do not reduce violence and may increase it', 'block emergency services and reporting of abuses (Manipur)', 'violate proportionality'],
               'Shutdowns are almost never justified; targeted, lawful measures against specific illegal content are more proportionate.'),
              ('Commercial spyware should be banned internationally.',
               ['documented abuse against journalists and activists', 'impossible to prevent misuse'],
               ['law enforcement claims it is needed against serious crime', 'hard to define and enforce globally', 'export controls and licensing may be more realistic'],
               'A global moratorium until strong safeguards exist is justified, with strict export controls and accountability.')],
    extended=[('Evaluate the impacts of one internet shutdown or censorship measure on human rights and on different stakeholders.', 'E.g. Kashmir 2019–21, Manipur 2023, Iran 2019/2022, Russia 2022; rights affected; stakeholders (citizens, journalists, businesses, government); proportionality; responses (courts, VPNs, #KeepItOn); judgement.', 8, 'long')],
))

R.facts('ch09-st3', F(
    terms=[('digital constitutionalism', 'efforts to apply constitutional principles – rights, limits on power, accountability – to the digital environment, through laws, charters and court rulings'),
           ('civil society', 'non-governmental organisations, community groups, journalists and activists that act in the public interest, such as Access Now or the Electronic Frontier Foundation'),
           ('strategic litigation', 'bringing carefully chosen court cases to change law or policy, such as Max Schrems\' cases against Facebook'),
           ('UN Guiding Principles on Business and Human Rights', 'principles endorsed in 2011 stating that states must protect, and companies must respect, human rights, with access to remedy'),
           ('Council of Europe Framework Convention on AI', 'the first binding international treaty on AI and human rights, democracy and the rule of law, opened for signature in 2024'),
           ('Global Network Initiative', 'a multi-stakeholder organisation (founded 2008) of companies, NGOs and academics committed to freedom of expression and privacy in the tech sector')],
    facts=[('Which civil-society campaign, coordinated by Access Now, campaigns against internet shutdowns?', '#KeepItOn', ['#MeToo', '#DeleteFacebook', '#StopTheSteal'], 'It documents shutdowns and lobbies governments.'),
           ('In 2024 the Council of Europe opened for signature the first binding international treaty on what?', 'Artificial intelligence and human rights, democracy and the rule of law', ['Undersea cables', 'Cryptocurrency', 'Space debris'], 'Signed by the EU, UK, US and others.'),
           ('Which country adopted the Marco Civil da Internet (2014), sometimes called an internet "bill of rights"?', 'Brazil', ['Portugal', 'Argentina', 'Spain'], 'It protects net neutrality, privacy and freedom of expression.'),
           ('Which Austrian activist\'s complaints led to the invalidation of the Safe Harbour (2015) and Privacy Shield (2020) frameworks?', 'Max Schrems', ['Edward Snowden', 'Frances Haugen', 'Christopher Wylie'], 'His NGO is noyb.')],
    why=[('Explain why civil society plays an important role in protecting digital rights.', 'NGOs and journalists investigate abuses (Pegasus Project), document shutdowns, bring strategic litigation and advocate for laws, holding states and companies accountable when they are unwilling to regulate themselves.'),
         ('Explain why international law is often weak in protecting digital rights.', 'Enforcement depends on states\' willingness, many key actors are private companies, technology outpaces treaties and powerful states may refuse to sign or comply.'),
         ('Explain why digital constitutionalism has emerged.', 'Platforms and digital states exercise power over rights in ways traditional constitutions did not foresee, so courts, legislators and civil society seek to limit this power through rights charters and laws such as the DSA or Marco Civil.')],
    contrast=[('international law', 'national law', 'International law (treaties, UN resolutions) sets standards across states but has weak enforcement; national law (e.g. Brazil\'s Marco Civil, India\'s DPDP Act) is directly enforceable but limited to one country.'),
              ('strategic litigation', 'advocacy campaigns', 'Strategic litigation uses courts to create binding legal change (e.g. Schrems cases); advocacy campaigns use public pressure, research and lobbying (e.g. #KeepItOn) to influence governments and companies.')],
    misc=[('Only governments can protect digital rights.', 'Courts, civil-society organisations, journalists, standards bodies and companies (through encryption, transparency reports) also play key roles.'),
          ('International agreements on digital rights are binding on all countries.', 'Most UN resolutions are non-binding; treaties bind only states that ratify them, and enforcement mechanisms are limited.')],
    cases=[('Max Schrems and noyb', 'Austrian lawyer Max Schrems brought complaints that led the EU Court of Justice to invalidate Safe Harbour (2015) and Privacy Shield (2020); his NGO noyb has filed hundreds of GDPR complaints.', 'strategic litigation by civil society',
            'one activist used courts to force changes to transatlantic data flows, showing the power of rights-based litigation.'),
           ("Brazil's Marco Civil da Internet (2014)", 'Developed through online public consultation, the law sets principles of net neutrality, privacy and freedom of expression and limits intermediary liability.', 'digital constitutionalism',
            'a participatory process produced a rights-based framework for the internet at national level.'),
           ('the #KeepItOn coalition', 'Access Now\'s #KeepItOn coalition of hundreds of organisations tracks shutdowns, publishes annual reports and lobbies governments and telecom companies.', 'civil-society interventions',
            'documentation and advocacy raise the cost of shutdowns, though many governments continue to impose them.')],
    sources=[('"Business enterprises should respect human rights. This means that they should avoid infringing on the human rights of others and should address adverse human rights impacts with which they are involved."', 'UN Guiding Principles on Business and Human Rights, Principle 11 (2011)',
              'With reference to the source, explain the responsibility it places on technology companies.', 'Companies must avoid causing or contributing to human-rights harms (e.g. selling spyware, enabling censorship) and must act to address harms linked to their products, even where local law is weak.'),
             ('"We built the Marco Civil with the people, through the internet itself."', 'Brazilian official describing the online consultation for the Marco Civil, 2014',
              'Explain one strength of the process described in the source.', 'Public participation gave the law democratic legitimacy and incorporated many perspectives, making it more likely to reflect citizens\' rights and needs.')],
    evaluate=[('Civil society is more effective than international law in protecting digital rights.',
               ['investigations (Pegasus Project) and litigation (Schrems) produce concrete change', 'fast and flexible'],
               ['NGOs lack enforcement power', 'governments may restrict civil society', 'international standards give NGOs a basis for advocacy'],
               'Civil society and international law are complementary: NGOs use legal standards to hold actors accountable.'),
              ('National "internet bills of rights" are an effective intervention for digital rights.',
               ['enforceable rights and principles (Marco Civil)', 'democratic legitimacy through participation'],
               ['enforcement may be weak; courts slow', 'later laws or orders can override (Brazil\'s court-ordered WhatsApp blocks 2015–16, X suspension 2024)', 'limited power over global platforms'],
               'They provide an important legal basis, but their effectiveness depends on courts, enforcement and political will.')],
    extended=[('Evaluate one intervention by an international organisation, government or civil-society group designed to protect digital rights.', 'E.g. Council of Europe AI Convention, #KeepItOn, Marco Civil, US sanctions on NSO, GDPR; aims, stakeholders, effectiveness, limitations, recommendation.', 8, 'long')],
))

P2['ch09'] = dict(
    src=[('"In 2023 we documented 283 shutdowns in 39 countries – the highest number since we began monitoring."', 'Access Now, #KeepItOn annual report, 2024',
          'Identify two facts about internet shutdowns in {S}.', ['283 shutdowns in 2023', 'in 39 countries; highest number recorded'],
          'Explain one strength and one limitation of {S} as evidence.', 'Strength: systematic global monitoring by a specialist organisation. Limitation: it is an advocacy NGO with a campaigning purpose, and counting methods (e.g. treating regional or repeated orders as separate shutdowns) affect totals.'),
         ('"Mobile internet services will remain suspended to prevent the spread of false information and to maintain law and order."', 'Order issued by a state home department in India, 2023',
          'Identify two reasons for the shutdown given in {S}.', ['prevent the spread of false information', 'maintain law and order'],
          'Explain the perspective expressed in {S}.', 'It presents the shutdown as a security measure to stop misinformation fuelling violence, prioritising public order; it does not acknowledge costs to rights or services.'),
         ('"States should refrain from imposing internet shutdowns, which are inherently disproportionate in their impact on human rights."', 'UN Office of the High Commissioner for Human Rights, report on internet shutdowns, 2022',
          'Identify two points made in {S}.', ['states should not impose shutdowns', 'shutdowns are inherently disproportionate to rights'],
          'Explain why {S} is significant for governments.', 'It sets out the UN human-rights position that shutdowns violate international standards, giving civil society and courts authoritative grounds to challenge them.')],
    cmp=[(1, 2, 'the justification of internet shutdowns', ['both refer to internet shutdowns and their purpose'],
          ['Source B justifies shutdowns as necessary for order; Source C says they are inherently disproportionate', 'B is a government order; C is a UN human-rights body']),
         (0, 2, 'the scale and legitimacy of shutdowns', ['both are critical of internet shutdowns', 'both are concerned with human rights'],
          ['Source A provides statistics on frequency; Source C provides a legal/normative judgement', 'A is an NGO; C is an intergovernmental body'])],
    ev=[(1, 2, 'internet shutdowns are an effective tool for maintaining public order.', ['governments claim shutdowns stop rumours and coordination (Source B)'],
         ['UN says shutdowns are disproportionate (Source C)', 'record numbers suggest they are overused (Source A)', 'evidence that shutdowns increase violence; hide abuses (Manipur)']),
        (0, 2, 'international pressure can reduce the use of internet shutdowns.', ['UN standards and NGO documentation (Sources A and C)', 'court rulings like Anuradha Bhasin'],
         ['shutdowns reached a record high despite pressure (Source A)', 'governments prioritise security (Source B)', 'weak enforcement of international law'])],
)

INTV['ch09'] = [
    ('the #KeepItOn campaign', 'Access Now\'s #KeepItOn coalition of over 300 organisations documents internet shutdowns worldwide, publishes annual data, sends letters to governments and telecom companies before elections and supports legal challenges.',
     'Governments increasingly impose internet shutdowns during protests, elections and exams, violating rights to expression and information and harming economies.',
     ['citizens – advocacy for their access and rights', 'governments – reputational pressure and scrutiny', 'telecom companies – pressure to resist or disclose orders', 'journalists – data and support for reporting'],
     ['global, systematic documentation', 'coalition increases legitimacy and reach', 'supports litigation (e.g. in Togo, India)'],
     ['no enforcement power', 'shutdowns reached record levels in 2023', 'governments may ignore or restrict NGOs'],
     'Work with telecom companies and investors on transparency about shutdown orders, and support regional courts in setting binding precedents.'),
    ('US sanctions on spyware vendors', 'In 2021 the US Commerce Department added NSO Group and Candiru to its Entity List, restricting their access to US technology; later measures included visa bans on people involved in misusing spyware and an executive order limiting US government use of commercial spyware.',
     'Commercial spyware such as Pegasus was sold to governments and used to hack phones of journalists, activists and politicians, undermining privacy and free expression.',
     ['journalists and activists – reduced risk if vendors are weakened', 'spyware companies – loss of access to US technology and markets', 'governments using spyware – reputational and diplomatic pressure', 'tech companies (Apple, Meta) – support for lawsuits against vendors'],
     ['targets suppliers, not only users', 'signals that misuse has consequences', 'combined with lawsuits by Apple and WhatsApp'],
     ['vendors can rebrand or move to other jurisdictions', 'other countries may not follow', 'does not stop existing deployments'],
     'Build a multilateral export-control regime with allies and require independent human-rights due diligence for any surveillance technology sales.'),
    ('the Council of Europe Framework Convention on AI', 'Opened for signature in September 2024, the Convention requires parties to ensure that AI systems respect human rights, democracy and the rule of law, including transparency, oversight and remedies. It was signed by the EU, UK and US among others, but it largely exempts national security.',
     'AI systems used by states and companies can threaten privacy, equality and democratic processes, but there was no binding international treaty on AI and rights.',
     ['citizens – rights to remedies and transparency', 'governments – duties to regulate AI', 'AI companies – compliance with national implementing laws', 'civil society – a legal basis for advocacy'],
     ['first binding international AI treaty', 'open to non-European states', 'focus on rights and remedies'],
     ['broad language and flexible implementation', 'national-security exemptions', 'depends on ratification and national laws'],
     'Encourage wide ratification with clear national implementing laws and independent oversight bodies that can receive complaints.'),
]


# =============================================================================================
# ch10 HL challenge 5.3 Sustainable development
# =============================================================================================
@R.add('ch10-st1', 'C3', (1, 4), 'numerical')
def connectivity_growth(rng, slot):
    pop = rng.choice([8, 12, 25, 40, 60])  # million
    a = rng.randint(10, 40)
    b = rng.randint(a + 8, min(a + 45, 85))
    yrs = rng.choice([4, 5, 8, 10])
    pp = b - a
    rel = (b - a) / a * 100
    extra = pop * pp / 100
    stem = (f'In a low-income country with a population of {pop} million, the share of people using the internet rose from {a}% to {b}% over {yrs} years (assume the population is constant). '
            f'Calculate (i) the change in percentage points, (ii) the percentage increase, and (iii) the number of additional internet users.')
    ans = f'(i) {pp} percentage points; (ii) {pc(rel, 1)}%; (iii) {pc(extra, 2)} million people'
    key = f'(i) {b} − {a} = {pp} pp [A1]; (ii) {pp} ÷ {a} × 100 = {pc(rel, 1)}% [M1 A1]; (iii) {pop} m × {pp}% = {pc(extra, 2)} million [A1].'
    m = 4
    if slot.d >= 3:
        stem += f' Explain why this growth alone does not show progress towards SDG 4 (quality education).'
        ans += '; access is not the same as meaningful use – affordability, device quality, digital skills, relevant content and who gained access (gender, rural/urban) all matter'
        key += ' Access ≠ meaningful use / learning outcomes; distribution across groups unknown [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch10-st1', F(
    terms=[('Sustainable Development Goals (SDGs)', 'the 17 goals adopted by all UN member states in 2015 as part of the 2030 Agenda, covering poverty, health, education, equality, climate and more'),
           ('ICT for development (ICT4D)', 'the use of information and communication technologies to support social and economic development, especially in low- and middle-income countries'),
           ('mobile money', 'a service that lets people store, send and receive money using a mobile phone, often without a bank account, such as M-Pesa'),
           ('leapfrogging', 'skipping an older stage of technology, such as moving straight to mobile phones and mobile money without building landline and bank-branch networks'),
           ('rebound effect', 'when efficiency gains from technology lower costs and so increase overall use, cancelling out some of the expected environmental savings'),
           ('precision agriculture', 'using sensors, satellite data, drones and analytics to apply water, fertiliser and pesticides only where needed')],
    facts=[('In which year did UN member states adopt the 17 Sustainable Development Goals?', '2015', ['2000', '2010', '2020'], 'They replaced the Millennium Development Goals and target 2030.'),
           ('Which mobile money service was launched by Safaricom in Kenya in 2007?', 'M-Pesa', ['Paytm', 'Alipay', 'GCash'], 'A 2016 study in Science estimated it lifted about 2% of Kenyan households out of extreme poverty.'),
           ('Which company began delivering blood supplies by drone in Rwanda in 2016?', 'Zipline', ['Amazon Prime Air', 'Wing', 'DJI'], 'Drones deliver to rural clinics, reducing delivery times from hours to minutes.'),
           ('According to the ITU, roughly how many people remained offline worldwide in 2024?', 'About 2.6 billion', ['About 26 million', 'About 260 million', 'About 6 billion'], 'Roughly a third of the world\'s population.')],
    why=[('Explain how mobile money can contribute to SDG 1 (no poverty).', 'It gives unbanked people a safe way to save, receive remittances and pay, smoothing income shocks and enabling small businesses; studies of M-Pesa found reductions in poverty, especially for women-headed households.'),
         ('Explain why digital technologies can widen inequality even while supporting the SDGs.', 'Benefits go first to those who already have connectivity, devices and skills; groups without access (rural, women, poor, disabled people) fall further behind, and automation may displace low-skill jobs.'),
         ('Explain why the environmental footprint of digital technology is a risk for SDG 13 (climate action).', 'Manufacturing devices, running data centres and networks, and training AI models consume energy, water and minerals and create e-waste; rapid growth and the rebound effect can outweigh efficiency gains.')],
    contrast=[('access to technology', 'meaningful connectivity', 'Access means a connection is available; meaningful connectivity means regular use with an adequate device, affordable data, sufficient speed and the skills to benefit.'),
              ('an opportunity of digital technology for the SDGs', 'a risk', 'Opportunities include mobile money, telemedicine and precision agriculture; risks include e-waste, energy use, surveillance and widening digital divides.')],
    misc=[('Digital technology automatically helps achieve the SDGs.', 'Outcomes depend on design, governance, affordability, skills and local context; technology can also harm the environment or deepen inequality.'),
          ('Leapfrogging means older infrastructure is never needed.', 'Mobile networks still need electricity, backhaul fibre and regulation; leapfrogging skips some stages but depends on other infrastructure.')],
    cases=[('M-Pesa in Kenya', 'Launched by Safaricom in 2007, M-Pesa allowed people to send money by SMS through agents; a 2016 study by Suri and Jack estimated it lifted about 194,000 households (2%) out of extreme poverty.', 'digital technology supporting SDG 1 and SDG 5',
            'mobile money improved financial inclusion, especially for women, by leapfrogging traditional banking.'),
           ('Zipline drone delivery in Rwanda', 'Since 2016 Zipline has used fixed-wing drones to deliver blood and medical supplies to rural health facilities in Rwanda, later expanding to Ghana and other countries.', 'robots and autonomous technologies supporting SDG 3',
            'autonomous delivery reduced delivery times and waste of blood products, though it depends on government contracts and funding.'),
           ('Digital Green in India', 'Digital Green, which grew out of a Microsoft Research project, produces short videos of local farmers demonstrating techniques, shown in villages to share agricultural knowledge.', 'media and networks supporting SDG 2',
            'locally made content proved more trusted and cost-effective than traditional extension visits.')],
    sources=[('"Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet in least developed countries by 2020."', 'UN Sustainable Development Goals, Target 9.c (2015)',
              'With reference to the source, explain why this target was not achieved.', 'Universal, affordable access in least developed countries was not reached by 2020 because of infrastructure costs, high data and device prices relative to income, low digital skills and limited electricity.'),
             ('"Digital technologies can accelerate progress on the SDGs, but they can also widen existing divides."', 'Paraphrase of a common theme in UN Secretary-General reports on digital cooperation',
              'Explain one way digital technologies could widen existing divides.', 'Services moving online (banking, government, education) disadvantage people without access or skills, so those already marginalised lose out further.')],
    evaluate=[('Digital technologies are essential for achieving the Sustainable Development Goals.',
               ['mobile money, telemedicine, e-learning and precision agriculture show measurable gains', 'data improves monitoring of SDG progress'],
               ['environmental costs of devices and data centres', 'unequal access widens divides', 'many goals depend more on governance, funding and infrastructure'],
               'Digital technologies are an important enabler but not sufficient; their benefits depend on inclusive access and sustainable design.'),
              ('The benefits of digital technology for development outweigh its environmental costs.',
               ['efficiency gains (smart grids, dematerialisation)', 'improved health and incomes'],
               ['e-waste and energy growth', 'rebound effects', 'costs fall on poorer countries (e-waste dumping, mining)'],
               'Benefits can outweigh costs only with circular design, renewable energy and fair e-waste policies.')],
    extended=[('Evaluate the extent to which digital technologies help achieve one Sustainable Development Goal.', 'Choose an SDG; real examples (M-Pesa, Zipline, Digital Green); opportunities vs risks (inequality, environment, dependency); stakeholders; concepts (change, power, values); judgement.', 8, 'long')],
))

AR('ch10-st1', [
    ('M-Pesa is often described as an example of leapfrogging.', 'It allowed many Kenyans to use digital financial services without first having a bank account.', 'a', 'Both true; R explains A – people skipped traditional banking.'),
    ('Efficiency improvements in digital technology always reduce total energy use.', 'Lower costs from efficiency can increase overall demand.', 'd', 'A is false; R is true and describes the rebound effect, which is why A is false.'),
    ('The SDGs were adopted in 2015.', 'The SDGs replaced the Millennium Development Goals.', 'b', 'Both true, but replacing the MDGs does not explain the year of adoption.'),
])


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def pue_calc(rng, slot):
    it = rng.choice([4, 10, 20, 50, 80])  # GWh per year
    pue = rng.choice([1.1, 1.2, 1.4, 1.5, 1.6, 1.8])
    total = it * pue
    over = total - it
    new = rng.choice([1.1, 1.2])
    if new >= pue:
        return None
    save = it * (pue - new)
    stem = (f'A data centre\'s IT equipment uses {it} GWh of electricity a year. Its power usage effectiveness (PUE) is {pue}. '
            f'Calculate (i) the total facility energy use, (ii) the energy used for cooling and other overheads, and (iii) the saving if PUE is improved to {new}.')
    ans = f'(i) {pc(total, 2)} GWh; (ii) {pc(over, 2)} GWh; (iii) {pc(save, 2)} GWh per year'
    key = f'PUE = total ÷ IT, so total = {it} × {pue} = {pc(total, 2)} GWh [M1 A1]; overhead = {pc(total, 2)} − {it} = {pc(over, 2)} GWh [A1]; saving = {it} × ({pue} − {new}) = {pc(save, 2)} GWh [A1].'
    m = 4
    if slot.d >= 4:
        stem += ' Explain one limitation of PUE as a measure of a data centre\'s sustainability.'
        ans += '; PUE ignores how the electricity is generated (carbon intensity), water use, the efficiency of the IT itself and embodied emissions of hardware'
        key += ' PUE measures overhead only; ignores energy source, water, IT efficiency, embodied carbon [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


@R.add('ch10-st2', 'C3', (1, 4), 'numerical')
def ewaste_rate(rng, slot):
    gen = rng.choice([20, 35, 50, 120, 400])  # thousand tonnes
    rate = rng.choice([15, 22, 30, 45, 60])
    pop = rng.choice([2, 5, 10, 25])  # million
    coll = gen * rate / 100
    per = gen * 1000 / (pop * 1e6) * 1000  # kg per person
    stem = (f'A country of {pop} million people generates {gen} thousand tonnes of e-waste a year, of which {rate}% is formally collected and recycled. '
            f'Calculate (i) the tonnes formally recycled, (ii) the tonnes not formally recycled, and (iii) the e-waste generated per person in kg.')
    ans = f'(i) {pc(coll, 2)} thousand tonnes; (ii) {pc(gen - coll, 2)} thousand tonnes; (iii) {pc(per, 3)} kg per person'
    key = f'(i) {gen} × {rate}% = {pc(coll, 2)} kt [A1]; (ii) {gen} − {pc(coll, 2)} = {pc(gen - coll, 2)} kt [A1]; (iii) {gen},000 t × 1000 kg ÷ {pop},000,000 = {pc(per, 3)} kg [M1 A1].'
    m = 4
    if slot.d >= 3:
        stem += ' Suggest one intervention to raise the collection rate and explain how it would work.'
        ans += '; e.g. extended producer responsibility (EPR) making manufacturers fund take-back; deposit-return schemes; convenient collection points'
        key += ' Named intervention [R1]; mechanism (incentive/responsibility/convenience) [R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch10-st2', F(
    terms=[('power usage effectiveness (PUE)', 'the ratio of total data-centre facility energy to the energy used by IT equipment; 1.0 is the ideal'),
           ('circular economy', 'an economic model that keeps products and materials in use through repair, reuse, refurbishment and recycling rather than "take, make, dispose"'),
           ('extended producer responsibility (EPR)', 'a policy that makes manufacturers responsible for the collection and recycling of their products at end of life'),
           ('embodied emissions', 'the greenhouse gases released in mining materials, manufacturing and transporting a device before it is used'),
           ('right to repair', 'laws or principles requiring manufacturers to make spare parts, tools and repair information available so that devices can be repaired'),
           ('e-waste', 'discarded electrical and electronic equipment, which contains valuable metals and hazardous substances such as lead and mercury')],
    facts=[('According to the Global E-waste Monitor 2024, how much e-waste was generated worldwide in 2022?', 'About 62 million tonnes', ['About 6 million tonnes', 'About 620,000 tonnes', 'About 620 million tonnes'], 'Only about 22% was documented as formally collected and recycled.'),
           ('From the end of 2024, which connector did the EU require on new mobile phones sold in the EU?', 'USB-C', ['Lightning', 'Micro-USB', 'Mini-USB'], 'The common-charger directive aims to reduce e-waste and inconvenience.'),
           ('In 2022, which cryptocurrency switched from proof of work to proof of stake, cutting its energy use by over 99%?', 'Ethereum', ['Bitcoin', 'Dogecoin', 'Litecoin'], 'The switch was called "the Merge".'),
           ('Which Dutch company makes modular smartphones designed to be repaired by users?', 'Fairphone', ['Nokia', 'Philips', 'TomTom'], 'Founded in 2013, it also focuses on fairer sourcing of minerals.')],
    why=[('Explain why the manufacturing stage matters for the carbon footprint of a smartphone.', 'Most of a smartphone\'s lifetime emissions come from mining materials and manufacturing (embodied emissions), so keeping devices longer through repair and reuse saves more than reducing charging energy.'),
         ('Explain why e-waste is a global justice issue.', 'Much e-waste is exported or informally processed in poorer countries, where workers, often without protection, burn or dismantle devices and are exposed to toxic substances, while the benefits of the devices were enjoyed elsewhere.'),
         ('Explain why AI growth is raising concerns about data-centre sustainability.', 'Training and running large AI models needs large amounts of electricity and water for cooling, and rapid expansion of data centres can strain grids and delay climate targets.')],
    contrast=[('recycling', 'repair and reuse', 'Recycling recovers materials after a device is discarded but loses embodied energy; repair and reuse extend the life of the whole device and avoid new manufacturing, so they are higher in the waste hierarchy.'),
              ('PUE', 'carbon intensity', 'PUE measures how much extra energy a data centre uses beyond its IT load; carbon intensity measures how much CO2 is emitted per unit of electricity, which depends on the energy source.')],
    misc=[('Digital services are "weightless" and have no environmental impact.', 'Streaming, cloud storage and AI rely on physical data centres, networks and devices that use energy, water and raw materials.'),
          ('Recycling solves the e-waste problem.', 'Only about a fifth of e-waste is formally recycled, some materials cannot be recovered economically, and reducing and reusing devices matters more.')],
    cases=[('the EU common charger directive', 'The EU required USB-C charging ports on new phones, tablets and cameras sold from December 2024, with laptops following in 2026, and allowed chargers to be sold separately.', 'policy for sustainable computing',
            'standardisation reduces e-waste and costs for consumers, but critics argued it could slow innovation in connectors.'),
           ('DeepMind data-centre cooling (2016)', 'Google reported that DeepMind machine learning reduced the energy used for cooling its data centres by up to 40% by predicting and optimising settings.', 'AI for energy efficiency',
            'AI can improve efficiency, though growth in demand may outweigh savings (rebound effect).'),
           ('Agbogbloshie, Ghana', 'For years a site in Accra known for informal e-waste processing, where workers burned cables to recover copper, exposing themselves and residents to toxic fumes; the site was cleared by authorities in 2021.', 'global inequality in e-waste',
            'the costs of e-waste fall heavily on poor workers in the Global South, showing the need for EPR and fair recycling.')],
    sources=[('"Only 22.3% of the year\'s e-waste mass was documented as having been properly collected and recycled."', 'Global E-waste Monitor 2024 (UNITAR and ITU)',
              'With reference to the source, explain one consequence of the low collection rate.', 'Most e-waste ends up in landfill, incineration or informal recycling, losing valuable materials and releasing hazardous substances that harm health and the environment.'),
             ('"Fair materials, longer-lasting products and repairable design are at the heart of what we do."', 'Paraphrase of Fairphone\'s stated mission',
              'Explain one limitation of the approach described in the source as an intervention for sustainability.', 'Modular, repairable phones remain a small niche with higher prices; system-wide change needs regulation such as right-to-repair laws.')],
    evaluate=[('Right-to-repair laws are the most effective way to reduce e-waste.',
               ['extend device life, avoiding embodied emissions', 'EU Right to Repair Directive (2024) and ecodesign rules on spare parts'],
               ['consumers may still prefer new devices', 'software updates and design matter too', 'collection and EPR needed for end-of-life devices'],
               'Right-to-repair is highly effective when combined with longer software support, EPR and consumer incentives.'),
              ('Technology companies should be required to report the environmental impact of their AI services.',
               ['transparency enables accountability and comparison', 'informs users and regulators'],
               ['measurement is complex (embodied vs operational)', 'compliance costs', 'risk of greenwashing'],
               'Standardised mandatory reporting is justified as a first step towards regulating AI\'s environmental footprint.')],
    extended=[('Evaluate the effectiveness of one intervention designed to make computing more sustainable.', 'E.g. EU common charger, right-to-repair, EPR, renewable-powered data centres, Ethereum\'s Merge; aims; evidence; stakeholders (manufacturers, consumers, recyclers, workers); limitations; judgement.', 8, 'long')],
))


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def affordability(rng, slot):
    gni = rng.choice([600, 900, 1200, 2400, 3600, 6000])  # USD per year
    price = rng.choice([0.5, 1, 1.5, 2, 3, 4])
    monthly = gni / 12
    share = price / monthly * 100
    ok = share <= 2
    stem = (f'In a country, average income (GNI per capita) is US${gni:,} a year and 1 GB of mobile data costs US${price:g}. '
            f'The UN Broadband Commission target is that 1 GB should cost no more than 2% of average monthly income. '
            f'Calculate the cost of 1 GB as a percentage of average monthly income and state whether the target is met.')
    ans = f'{pc(share, 2)}%; target {"met" if ok else "not met"}'
    key = f'Monthly income = {gni:,} ÷ 12 = {pc(monthly, 3)} [M1]; {price:g} ÷ {pc(monthly, 3)} × 100 = {pc(share, 2)}% [A1]; {"≤" if ok else ">"} 2% so target {"met" if ok else "not met"} [A1].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain why an average figure may hide the affordability problem for some groups.'
        ans += '; income is unequally distributed – the poorest households, often rural or women, earn far below the average, so data costs a much larger share of their income'
        key += ' Inequality within population; average skewed by high earners; specific groups (rural, women) [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


@R.add('ch10-st3', 'C3', (2, 5), 'numerical')
def cost_per_connected(rng, slot):
    a_cost = rng.choice([2, 5, 8, 12])  # million USD
    a_n = rng.choice([40, 80, 100, 160])  # thousand people
    b_cost = rng.choice([1, 3, 6, 10])
    b_n = rng.choice([20, 50, 90, 150])
    ca = a_cost * 1e6 / (a_n * 1000)
    cb = b_cost * 1e6 / (b_n * 1000)
    if abs(ca - cb) < 1:
        return None
    best = 'A' if ca < cb else 'B'
    stem = (f'Two digital-inclusion projects are compared. Project A (community Wi-Fi hubs) cost US${a_cost} million and connected {a_n},000 people. '
            f'Project B (subsidised smartphones with digital-skills training) cost US${b_cost} million and connected {b_n},000 people. '
            f'Calculate the cost per person connected for each project and identify the more cost-effective project.')
    ans = f'A US${pc(ca, 3)} per person; B US${pc(cb, 3)} per person; Project {best} is more cost-effective'
    key = f'A: {a_cost},000,000 ÷ {a_n},000 = {pc(ca, 3)} [M1 A1]; B: {b_cost},000,000 ÷ {b_n},000 = {pc(cb, 3)} [A1]; lower cost = Project {best} [A1].'
    m = 4
    if slot.d >= 4:
        stem += ' Explain why cost per person connected should not be the only criterion for choosing a project.'
        ans += '; it ignores quality and sustainability of use, skills gained, who is reached (most marginalised), long-term running costs and outcomes such as income or learning'
        key += ' Outcomes vs outputs; equity of reach; sustainability/maintenance [R1 R1].'
        m = 6
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch10-st3', F(
    terms=[('digital inclusion', 'ensuring that all individuals and communities have the access, devices, affordability and skills needed to use digital technologies meaningfully'),
           ('digital literacy', 'the skills to find, evaluate, create and communicate information safely and effectively using digital technologies'),
           ('universal service fund', 'a fund, usually paid into by telecom operators, used to extend connectivity to areas that are not commercially profitable'),
           ('community network', 'a locally owned and operated communications network built by a community to meet its own connectivity needs'),
           ('zero-rating', 'when a mobile operator does not charge data for using particular apps or services, as in Facebook\'s Free Basics'),
           ('affordability threshold ("1 for 2")', 'the target that 1 GB of mobile data should cost no more than 2% of average monthly income')],
    facts=[('Which UNICEF and ITU initiative, launched in 2019, aims to connect every school in the world to the internet?', 'Giga', ['Starlink', 'Free Basics', 'Project Loon'], 'It maps schools and works with governments and companies on financing.'),
           ('In 2016, which country\'s telecom regulator (TRAI) effectively banned Facebook\'s Free Basics on net-neutrality grounds?', 'India', ['Kenya', 'Brazil', 'Indonesia'], 'TRAI prohibited discriminatory pricing of data services.'),
           ('Which Alphabet project used high-altitude balloons to provide internet access and was shut down in 2021?', 'Project Loon', ['Project Kuiper', 'Project Natick', 'Project Maven'], 'It provided service in Kenya and in Puerto Rico after Hurricane Maria.'),
           ('Which 2005 initiative led by Nicholas Negroponte aimed to give low-cost laptops to children in developing countries?', 'One Laptop per Child (OLPC)', ['Hole in the Wall', 'Giga', 'Code.org'], 'Evaluations in Peru found little effect on test scores in maths and language.')],
    why=[('Explain why providing devices alone often fails to improve learning.', 'Without teacher training, relevant content, maintenance, electricity and connectivity, devices are underused; OLPC evaluations in Peru found little impact on test scores.'),
         ('Explain why community networks can be effective in remote areas.', 'Local ownership keeps costs low, builds skills and trust, and meets local needs where commercial operators see no profit, as with Zenzeleni in South Africa.'),
         ('Explain why zero-rated services such as Free Basics are controversial.', 'They give free access to some services, but the operator and the platform decide which ones, violating net neutrality and potentially creating a "walled garden" controlled by one company.')],
    contrast=[('a supply-side intervention', 'a demand-side intervention', 'Supply-side interventions build infrastructure or lower prices (fibre, satellites, community Wi-Fi); demand-side interventions build skills, relevance and confidence to use technology (digital literacy training).'),
              ('Free Basics', 'Giga', 'Free Basics (Meta) offered zero-rated access to selected services through operators, raising net-neutrality concerns; Giga (UNICEF–ITU) aims to connect schools to the open internet with public and private financing.')],
    misc=[('Once an area has network coverage, everyone in it is connected.', 'Coverage does not mean use – the "usage gap" is caused by device costs, data prices, lack of skills, relevance and social barriers.'),
          ('Digital inclusion is only a problem in low-income countries.', 'Older people, low-income households, disabled people and rural communities in wealthy countries also face exclusion.')],
    cases=[('Free Basics in India (2015–16)', 'Facebook\'s zero-rated app offering free access to selected services was opposed by the Save the Internet campaign; TRAI ruled against discriminatory data pricing in February 2016.', 'net neutrality and power in digital inclusion',
            'the case showed that inclusion interventions controlled by one company can conflict with users\' rights and an open internet.'),
           ('One Laptop per Child in Peru', 'Peru bought hundreds of thousands of XO laptops for schools; an evaluation by the Inter-American Development Bank found no significant effect on maths or language test scores.', 'evaluating digital-literacy interventions',
            'hardware-focused programmes need teacher training and curricula to improve learning.'),
           ('Zenzeleni Networks, South Africa', 'A community-owned internet service provider in the rural Eastern Cape, set up with the University of the Western Cape, offering low-cost Wi-Fi powered by solar energy.', 'community-led connectivity',
            'local ownership can make connectivity affordable and sustainable, though scaling up and regulation are challenges.')],
    sources=[('"Connecting every school to the Internet and every young person to information, opportunity and choice."', 'Stated mission of Giga, UNICEF and ITU',
              'With reference to the source, explain one challenge in achieving this aim.', 'Many schools lack electricity and are far from fibre backbones, so connections are costly to build and maintain; ongoing funding for data and devices is also needed.'),
             ('"Free Basics is not the internet. It is Facebook deciding what the poor can see."', 'Paraphrase of arguments made by the Save the Internet campaign in India, 2015',
              'Explain the concern expressed in the source.', 'A single company acting as gatekeeper controls which services users can reach, limiting choice and competition and violating net neutrality.')],
    evaluate=[('Building infrastructure is more important than teaching digital literacy for digital inclusion.',
               ['without connectivity, skills cannot be used', 'billions remain offline'],
               ['the usage gap is larger than the coverage gap', 'skills determine safe and meaningful use', 'OLPC shows hardware alone fails'],
               'Both are necessary; demand-side interventions are often the missing piece where coverage already exists.'),
              ('Private technology companies should lead efforts to connect the unconnected.',
               ['capital, technology and speed (satellites)', 'commercial incentive for sustainability'],
               ['profit motive may exclude unprofitable areas', 'risk of control and data extraction (Free Basics)', 'Project Loon shut down when not viable'],
               'Public–private partnerships with public accountability and open-internet safeguards are preferable.')],
    extended=[('Evaluate one intervention designed to improve digital inclusion.', 'E.g. Giga, Free Basics, OLPC, community networks, India\'s PMGDISHA digital-literacy programme; aims; stakeholders; supply vs demand side; evidence; limitations; recommendation.', 8, 'long')],
))

INTV['ch10'] = [
    ('Giga (UNICEF and ITU)', 'Launched in 2019, Giga maps the location and connectivity of schools worldwide, helps governments design financing models, and works with providers to connect schools to the internet.',
     'Hundreds of millions of children attend schools with no internet connection, limiting access to learning resources and widening inequality.',
     ['students – access to online learning', 'teachers – resources and training', 'governments – planning data and financing models', 'telecom providers – new contracts and markets'],
     ['open data mapping of schools', 'backed by UN agencies with global reach', 'combines infrastructure with financing models'],
     ['connection alone does not guarantee learning', 'ongoing costs of data, devices and electricity', 'depends on government and donor funding'],
     'Combine school connectivity with teacher training and long-term funding for running costs, and measure learning outcomes as well as connections.'),
    ('the EU common charger and right-to-repair rules', 'The EU required USB-C charging ports on new phones and many other devices from December 2024, adopted ecodesign rules requiring spare parts for smartphones, and passed a Right to Repair Directive in 2024.',
     'Short device lifespans and incompatible chargers generate large volumes of e-waste and embodied emissions.',
     ['consumers – lower costs and longer-lasting devices', 'manufacturers – design and compliance costs', 'repair businesses – new opportunities', 'the environment – less e-waste'],
     ['legally binding across a large market', 'targets the design stage, not just disposal', 'can influence global product design'],
     ['benefits outside the EU uncertain', 'consumers may still upgrade often', 'enforcement and spare-part pricing issues'],
     'Extend minimum software-support periods and create repair incentives such as vouchers or tax reductions on repairs.'),
    ('Free Basics (Meta)', 'Launched as Internet.org in 2013, Free Basics offered zero-rated access to a selected set of online services through mobile operators in many countries; it was banned in India in 2016 after a net-neutrality campaign.',
     'Billions of people could not afford mobile data, preventing them from accessing information and services online.',
     ['low-income users – free access to some services', 'Meta – new users and data', 'local content providers – disadvantaged if excluded', 'regulators – net-neutrality concerns'],
     ['no data cost for users', 'used existing networks quickly', 'included health and information services'],
     ['company controlled which services were available', 'privacy and data concerns', 'evidence that many users already had internet access'],
     'Support open, affordable access through universal service funds and community networks instead of company-controlled zero-rating.'),
]


# =============================================================================================
# ch11 HL Paper 3: analysing interventions from the pre-released statement
# =============================================================================================
STAKE_SETS = [
    ('a national ban on smartphones in schools', ['the education ministry', 'students', 'parents', 'phone manufacturers', 'teachers']),
    ('a city using facial recognition in public spaces', ['the police', 'residents', 'civil-liberties NGOs', 'the technology vendor', 'local businesses']),
    ('a government requiring age verification for social media', ['the regulator', 'teenagers', 'platforms', 'privacy advocates', 'parents']),
    ('a right-to-repair law for electronics', ['legislators', 'consumers', 'manufacturers', 'independent repair shops', 'environmental groups']),
]


@R.add('ch11-st1', 'C3', (2, 5), 'numerical')
def stakeholder_grid(rng, slot):
    issue, people = rng.choice(STAKE_SETS)
    pick = rng.sample(people, 4)
    sc = [(rng.randint(1, 10), rng.randint(1, 10)) for _ in pick]
    if any(p == 5 or p == 6 or i == 5 or i == 6 for p, i in sc):
        return None  # avoid borderline cases

    def quad(p, i):
        if p > 5 and i > 5:
            return 'manage closely'
        if p > 5:
            return 'keep satisfied'
        if i > 5:
            return 'keep informed'
        return 'monitor'
    tbl = '; '.join(f'{s} (power {p}, interest {i})' for s, (p, i) in zip(pick, sc))
    res = '; '.join(f'{s} – {quad(p, i)}' for s, (p, i) in zip(pick, sc))
    stem = (f'A pre-released statement concerns {issue}. Stakeholders are scored 1–10 for power and interest: {tbl}. '
            f'Using a power–interest grid (high = above 5): high power/high interest – manage closely; high power/low interest – keep satisfied; '
            f'low power/high interest – keep informed; low power/low interest – monitor. Classify each stakeholder.')
    key = f'{res} [A1 for each pair of correct classifications, max A2]; correct use of the threshold [M1].'
    m = 3
    if slot.d >= 4:
        stem += ' Explain why a stakeholder with high interest but low power still matters when evaluating the intervention.'
        res += '; they are often the people most affected (e.g. students, residents), and ignoring them raises ethical and legitimacy concerns and may cause the intervention to fail'
        key += ' Most affected group; values/ethics and legitimacy; risk of resistance or unintended consequences [R1 R1].'
        m = 5
    return dict(stem=stem, answer=res, markingKey=key, type='numerical', marks=m)


R.facts('ch11-st1', F(
    terms=[('pre-released statement', 'a short statement issued to schools before the HL Paper 3 examination that identifies the challenge topic for the inquiry'),
           ('challenge', 'in Digital Society, a significant problem in the HL extension areas – global well-being, governance and human rights, or sustainable development – that digital systems create or could help address'),
           ('intervention', 'an action, policy, law, technology or programme by a stakeholder that responds to a challenge'),
           ('stakeholder', 'a person, group or organisation that affects, or is affected by, a digital system or intervention'),
           ('power–interest grid', 'a tool that maps stakeholders by how much power they have over an issue and how interested or affected they are'),
           ('local and global context', 'the setting of a challenge at different scales – the same challenge may look different in one community, country or across the world')],
    facts=[('Which Digital Society examination component is taken only by HL students and is based on a pre-released statement?', 'Paper 3', ['Paper 1', 'Paper 2', 'The internal assessment'], 'Paper 3 focuses on challenges and interventions.'),
           ('Which three areas form the HL extension "challenges and interventions" in Digital Society?', 'Global well-being, governance and human rights, and environmental/sustainable development', ['Data, algorithms and computers', 'Media, networks and AI', 'Identity, power and space'], 'The pre-released statement draws on these areas.'),
           ('In the IB command terms, what does "analyse" mean?', 'Break down in order to bring out the essential elements or structure', ['Give a brief account', 'Give a precise meaning', 'Provide an answer from a number of possibilities'], '"Identify" is providing an answer from possibilities; "define" gives a precise meaning.'),
           ('Which question should you ask first when unpacking a pre-released statement?', 'What is the challenge, and who does it affect, where?', ['Which answer will be the longest?', 'Which brand is most popular?', 'How many marks does each paper carry?'], 'Identifying the challenge, stakeholders and context focuses later research.')],
    why=[('Explain why it is important to research several real interventions before Paper 3.', 'The paper asks students to evaluate interventions and recommend steps; knowing varied real examples (laws, technologies, campaigns) at different scales gives evidence for comparison and judgement.'),
         ('Explain why identifying stakeholders is a key step in unpacking the pre-released statement.', 'The impacts of a challenge and intervention differ between stakeholders, so analysis and recommendations must consider who benefits, who is harmed and who has power to act.'),
         ('Explain why the context of a challenge must be considered when evaluating an intervention.', 'An intervention that works in one country or community may fail elsewhere because of differences in law, infrastructure, culture, resources and political power.')],
    contrast=[('a challenge', 'an intervention', 'A challenge is the problem (e.g. online harms to children); an intervention is a response to it (e.g. the UK Online Safety Act).'),
              ('a primary stakeholder', 'a secondary stakeholder', 'Primary stakeholders are directly affected by the challenge or intervention (e.g. users); secondary stakeholders are indirectly affected or influence it (e.g. advertisers, NGOs).')],
    misc=[('Paper 3 only tests knowledge of the pre-released statement itself.', 'The statement sets the topic, but students must apply wider knowledge of real interventions, concepts and stakeholders to unseen material.'),
          ('All stakeholders are affected by an intervention in the same way.', 'Impacts vary – a law can protect users while increasing costs for businesses and restricting some freedoms.')],
    cases=[('unpacking a statement on online harms to children', 'A pre-released statement on children\'s online safety could be unpacked by identifying the challenge (exposure to harmful content), stakeholders (children, parents, platforms, regulators) and interventions (UK Online Safety Act, Australia\'s under-16 social-media ban, Instagram Teen Accounts).', 'unpacking a challenge',
            'mapping challenge, stakeholders and interventions creates a framework for evaluation.'),
           ('unpacking a statement on e-waste', 'For a statement on e-waste, students could research the global scale (62 Mt in 2022), stakeholders (consumers, manufacturers, informal recyclers, governments) and interventions (EU right to repair, EPR laws, the Basel Convention).', 'local and global context',
            'linking local recycling practices to global flows reveals power and justice issues.'),
           ('unpacking a statement on misinformation in elections', 'Students could identify stakeholders (voters, platforms, election bodies, fact-checkers) and interventions (the EU DSA, prebunking campaigns, labels on AI content).', 'stakeholder analysis',
            'different stakeholders have different powers and interests, which shapes which interventions are feasible.')],
    sources=[('"Governments, technology companies and civil society share responsibility for addressing the harms that digital systems can cause."', 'Example pre-released statement style, Digital Society HL practice material',
              'Identify three stakeholders mentioned or implied in the statement and explain one responsibility of one of them.', 'Governments, technology companies, civil society; e.g. governments should create and enforce regulation that protects users\' rights.'),
             ('"An intervention that works in one country may not work in another."', 'Paraphrase of a common principle in development studies',
              'Explain why this principle is important when evaluating interventions.', 'Context – laws, infrastructure, culture, resources, political systems – affects effectiveness, so evidence from one place may not transfer.')],
    evaluate=[('Stakeholder analysis is the most important step in preparing for Paper 3.',
               ['impacts and power differ across stakeholders', 'needed for balanced evaluation'],
               ['knowledge of real interventions and evidence is also essential', 'context and concepts shape analysis'],
               'Stakeholder analysis is essential but must be combined with researched examples and contextual understanding.'),
              ('Global interventions are more effective than local ones in addressing digital challenges.',
               ['global problems such as e-waste and platform power cross borders', 'common standards'],
               ['local interventions fit context and community needs', 'global agreements may be weak or slow'],
               'The most effective responses combine global standards with locally adapted implementation.')],
    extended=[('Using a challenge from the HL extension, analyse the interests and power of three stakeholders and how they shape possible interventions.', 'Identify challenge and context; three stakeholders with power/interest; how each enables or blocks interventions; real examples; concepts (power, values); conclusion.', 12, 'long')],
))


R.add('ch11-st2', 'C3', (2, 5), 'numerical')(decision_matrix)


@R.add('ch11-st2', 'C3', (2, 5), 'numerical')
def before_after(rng, slot):
    what = rng.choice([('reports of cyberbullying per 1,000 students', 'a school digital-citizenship programme'),
                       ('hours of internet shutdown per year', 'a court ruling requiring published reasons for shutdowns'),
                       ('tonnes of e-waste collected per month', 'a deposit-return scheme for phones'),
                       ('complaints about harmful content per 10,000 users', 'a new platform reporting tool')])
    a = rng.randint(40, 120)
    b = rng.randint(int(a * 0.4), int(a * 1.4))
    if b == a:
        return None
    ch = (b - a) / a * 100
    if abs(ch) < 5:
        return None
    direction = 'increase' if b > a else 'decrease'
    stem = (f'Before {what[1]} was introduced, {what[0]} averaged {a}. One year later it averaged {b}. '
            f'Calculate the percentage change, and explain why this figure alone cannot prove the intervention was effective.')
    ans = (f'{pc(abs(ch), 1)}% {direction}; other factors may have changed at the same time (no control group), measurement or reporting may have changed, '
           f'and a change in the indicator may reflect more reporting rather than more harm')
    key = (f'({b} − {a}) ÷ {a} × 100 = {pc(ch, 1)}% [M1 A1]; no control/comparison group or confounding factors [R1]; '
           f'reporting/measurement effects or indicator validity [R1].')
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=4)


R.facts('ch11-st2', F(
    terms=[('evaluate (command term)', 'make an appraisal by weighing up the strengths and limitations'),
           ('recommend', 'propose a course of action and justify it with reasons and evidence'),
           ('effectiveness', 'the extent to which an intervention achieves its intended aims'),
           ('unintended consequence', 'an outcome of an intervention that was not planned, which may be positive or negative'),
           ('feasibility', 'how practical an intervention is to implement, given cost, technology, law and political support'),
           ('scalability', 'whether an intervention can be expanded to more people or places without losing effectiveness')],
    facts=[('In the IB command terms, what does "to what extent" require?', 'Consider the merits or otherwise of an argument or concept, with clear, supported conclusions', ['List the main points only', 'Give a precise definition', 'Describe without judgement'], 'It requires a judgement on a scale.'),
           ('Which is the best evidence that a digital intervention was effective?', 'Measured outcomes compared with a comparison group or baseline', ['A press release from the company', 'The number of downloads only', 'The cost of the intervention'], 'Outcomes, not outputs, show effectiveness.'),
           ('When Australia\'s under-16 social-media minimum-age law was passed in 2024, which stakeholder was given the legal duty to prevent under-16s holding accounts?', 'The platforms', ['Parents', 'Children', 'Schools'], 'Platforms face fines for failing to take reasonable steps.'),
           ('Which term describes a recommendation that addresses a limitation of an existing intervention?', 'A further step or modification', ['A definition', 'A stakeholder map', 'A source analysis'], 'Paper 3 recommendations should build on evaluation.')],
    why=[('Explain why a recommendation must be justified with reference to the evaluation.', 'A recommendation is convincing only if it addresses the limitations identified and builds on strengths, using evidence about stakeholders and context.'),
         ('Explain why unintended consequences should be considered when evaluating an intervention.', 'Interventions can create new harms – age verification can collect sensitive data, bans can push users to less safe platforms – so judging effectiveness only by intended aims is incomplete.'),
         ('Explain why outputs are not the same as outcomes when evaluating interventions.', 'Outputs (devices distributed, posts removed) measure activity; outcomes (learning, reduced harm) measure impact – an intervention can have many outputs and little impact, as with OLPC.')],
    contrast=[('effectiveness', 'feasibility', 'Effectiveness is how well an intervention achieves its aims; feasibility is whether it can practically be implemented given costs, technology, law and support.'),
              ('a strength of an intervention', 'a limitation', 'A strength is a feature that helps it achieve its aims (e.g. legally binding); a limitation reduces its effectiveness or causes harm (e.g. easy to circumvent).')],
    misc=[('A good recommendation simply repeats the existing intervention.', 'It should propose a new or modified step that responds to identified limitations, with justification.'),
          ('If an intervention has limitations, it should be rejected.', 'Most interventions have limitations; evaluation weighs them against strengths and alternatives and may recommend modifications.')],
    cases=[('evaluating Australia\'s under-16 social-media law', 'The 2024 law requires platforms to take reasonable steps to prevent under-16s holding accounts; supporters cite mental-health concerns, critics warn about privacy of age checks and young people moving to less regulated spaces.', 'evaluating an intervention',
            'balanced evaluation weighs protection against privacy, rights and enforceability.'),
           ('evaluating the EU Digital Services Act', 'The DSA (fully applicable from 2024) requires transparency, risk assessments and audits for very large platforms, with fines up to 6% of global turnover.', 'evaluating regulation',
            'its strengths are binding obligations; limitations include enforcement capacity and global reach.'),
           ('evaluating prebunking campaigns', 'Google Jigsaw and university researchers ran short videos teaching manipulation techniques; studies found improved recognition of misinformation techniques, though effects can fade.', 'evaluating an educational intervention',
            'evidence-based, low-cost interventions may need repetition to sustain effects.')],
    sources=[('"The law places the onus on platforms, not parents or young people."', 'Paraphrase of the Australian government\'s explanation of its 2024 social-media minimum-age law',
              'Explain one strength and one limitation of the approach described in the source.', 'Strength: platforms have the technical capacity and resources to act. Limitation: age verification may require collecting personal data and can be circumvented.'),
             ('"Short prebunking videos improved people\'s ability to recognise manipulation techniques."', 'Paraphrase of findings by Roozenbeek et al., Science Advances, 2022',
              'Explain how this evidence could inform a recommendation.', 'A recommendation could scale up prebunking through platforms and schools, while testing how long the effects last.')],
    evaluate=[('Regulation is more effective than education as an intervention for online harms.',
               ['binding obligations and fines change platform behaviour (DSA)', 'applies at scale'],
               ['education builds long-term resilience (prebunking)', 'regulation can be circumvented and slow', 'risks to rights'],
               'A combination is most effective: regulation for systemic risks, education for individual resilience.'),
              ('Bans are an effective intervention for digital challenges.',
               ['clear and simple', 'signal social norms (school phone bans)'],
               ['circumvention', 'removes benefits', 'enforcement and privacy problems'],
               'Bans can be effective for narrow, well-defined harms but are usually less effective than design changes and education.')],
    extended=[('Evaluate one intervention that addresses a challenge in the HL extension and recommend one further step.', 'Describe intervention and aims; stakeholders; strengths and limitations with evidence; unintended consequences; justified recommendation addressing a limitation.', 12, 'long')],
))


@R.add('ch11-st3', 'C3', (1, 4), 'numerical')
def exam_timing(rng, slot):
    total = rng.choice([60, 75, 90])
    marks = rng.choice([24, 30, 40])
    q = rng.choice([4, 6, 8, 12])
    if q > marks:
        return None
    read = rng.choice([5, 10])
    per = (total - read) / marks
    t = per * q
    stem = (f'In a practice paper, a student has {total} minutes for {marks} marks and plans {read} minutes for reading and planning. '
            f'Calculate the time per mark for writing and the time to spend on a {q}-mark question.')
    ans = f'{pc(per, 2)} minutes per mark; about {pc(t, 1)} minutes'
    key = f'({total} − {read}) ÷ {marks} = {pc(per, 2)} min per mark [M1 A1]; × {q} = {pc(t, 1)} min [A1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=3)


@R.add('ch11-st3', 'C3', (2, 4), 'numerical')
def markband_place(rng, slot):
    feats = [('identifies an intervention and describes it', 1),
             ('explains impacts on at least two stakeholders', 2),
             ('uses specific real-world evidence', 3),
             ('weighs strengths against limitations', 4),
             ('makes a justified recommendation that addresses a limitation', 5)]
    k = rng.randint(1, 5)
    shown = [f for f, lvl in feats if lvl <= k]
    band = {1: '1–3', 2: '4–6', 3: '4–6', 4: '7–9', 5: '10–12'}[k]
    stem = (f'A student self-assesses a 12-mark Paper 3 response. It: ' + '; '.join(shown) + '. '
            f'Using bands 1–3 (limited, general), 4–6 (some analysis, mostly descriptive), 7–9 (evaluation with evidence and some balance) and 10–12 (sustained, balanced evaluation with a well-supported recommendation), '
            f'identify the most appropriate band and one improvement.')
    imp = {1: 'explain impacts on specific stakeholders', 2: 'add specific real-world evidence', 3: 'weigh strengths against limitations',
           4: 'add a justified recommendation that addresses a limitation', 5: 'sustain balance and integrate concepts throughout'}[k]
    ans = f'Band {band}; improvement: {imp}'
    key = f'Band {band} [A1] – justified by the features present [R1]; improvement: {imp} [R1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=3)


R.facts('ch11-st3', F(
    terms=[('markband', 'a level descriptor that describes the qualities of responses in a range of marks, used to mark extended responses'),
           ('best-fit approach', 'marking by choosing the markband whose descriptor best matches the response overall, then placing it within the band'),
           ('timed practice', 'answering exam-style questions under exam time limits to build pacing and exam technique'),
           ('self-assessment', 'evaluating your own work against criteria or markbands to identify strengths and next steps')],
    facts=[('Which approach do IB examiners use when applying markbands to extended responses?', 'Best fit', ['Point counting only', 'Word counting', 'Random sampling'], 'The overall quality is matched to the descriptor.'),
           ('What is the main purpose of timed practice for Paper 3?', 'To build pacing so every question receives time in proportion to its marks', ['To memorise model answers word for word', 'To avoid reading the questions', 'To write as much as possible on question 1'], 'Spending time per mark avoids leaving the high-mark question unfinished.'),
           ('What typically distinguishes a top-band 12-mark response from a middle-band one?', 'Sustained, balanced evaluation with a well-supported conclusion or recommendation', ['Longer length only', 'More definitions', 'Use of bullet points'], 'Quality of evaluation, not length, determines the band.')],
    why=[('Explain why self-assessment against markbands improves performance.', 'It shows students what the top band requires (balance, evidence, justified conclusions), helping them identify gaps and target improvements.'),
         ('Explain why planning before writing an extended response is valuable.', 'A short plan organises arguments, evidence and stakeholders, ensuring balance and a clear conclusion within the time available.')],
    contrast=[('a point-based markscheme', 'a markband', 'A point-based markscheme awards marks for specific points; a markband describes overall quality levels and is applied using best fit.')],
    misc=[('Writing more always earns more marks.', 'Markbands reward quality – focus, evidence, balance and judgement – not length.')],
    cases=[('timed Paper 3 practice', 'A student practising a past-style Paper 3 allocates time per mark, plans each answer, then self-assesses with markbands and records improvements for the next attempt.', 'exam technique',
            'regular timed practice with feedback builds pacing and quality.'),
           ('peer marking with markbands', 'Students swap 12-mark responses, apply best fit using the markband, and justify the band with evidence from the response.', 'assessment literacy',
            'applying markbands deepens understanding of what examiners reward.')],
    sources=[('"Examiners should use a best-fit approach when deciding the appropriate markband."', 'Paraphrase of standard IB markscheme guidance',
              'Explain what a best-fit approach means for students.', 'A response does not need to meet every descriptor perfectly; overall quality decides the band, so strengths in evaluation can compensate for minor gaps.')],
    evaluate=[('Self-assessment is as useful as teacher feedback for Paper 3 preparation.',
               ['builds independence and understanding of criteria', 'immediate'],
               ['students may misjudge their work', 'teachers have experience of standards'],
               'Self-assessment is most useful when calibrated with teacher feedback.')],
    extended=[('Evaluate the usefulness of timed practice and markband self-assessment in preparing for Paper 3.', 'Pacing; understanding of criteria; feedback loops; limitations (misjudgement, stress); judgement.', 8, 'long')],
))

INTV['ch11'] = [
    ('Australia\'s social-media minimum-age law', 'In 2024 Australia passed a law requiring age-restricted social-media platforms to take reasonable steps to prevent under-16s from having accounts, with fines of up to A$49.5 million, taking effect from late 2025.',
     'Concern that social media harms young people\'s mental health, sleep and safety, and that platforms have not done enough to protect them.',
     ['under-16s – loss of access, possible protection from harms', 'parents – support for setting limits', 'platforms – compliance costs and age-assurance duties', 'privacy advocates – concerns about age verification data'],
     ['places responsibility on platforms', 'clear rule and strong penalties', 'strong public support'],
     ['age assurance can be inaccurate or intrusive', 'young people may move to unregulated spaces', 'removes benefits such as connection and support'],
     'Combine the law with privacy-preserving age assurance standards, safety-by-design duties and digital-literacy education, and evaluate outcomes independently.'),
    ('the EU Digital Services Act', 'The DSA requires online platforms to provide notice-and-action systems, transparency about recommender systems and ads, and requires very large platforms to assess and reduce systemic risks, with fines of up to 6% of global turnover.',
     'Illegal content, disinformation and opaque algorithms on large platforms harm users and democratic processes.',
     ['users – reporting tools and transparency', 'very large platforms – risk assessments and audits', 'researchers – data access', 'the European Commission – enforcement role'],
     ['legally binding with large fines', 'focus on systemic risks rather than individual posts', 'transparency and data access'],
     ['enforcement capacity and speed', 'concerns about over-removal of lawful speech', 'limited reach outside the EU'],
     'Strengthen researcher data access and independent audits, and coordinate with other jurisdictions on common standards.'),
    ('prebunking campaigns', 'Researchers and Google Jigsaw ran short videos and games that warn people about manipulation techniques (such as scapegoating or false dichotomies) before they encounter them, including campaigns in Central and Eastern Europe in 2022.',
     'Misinformation spreads quickly online and fact-checking after the fact reaches fewer people than the false claims.',
     ['users – improved ability to spot manipulation', 'platforms – a scalable, content-neutral tool', 'fact-checkers – reduced load', 'governments – an approach that avoids censorship'],
     ['content-neutral, avoiding censorship concerns', 'evidence from randomised experiments', 'low cost and scalable'],
     ['effects may fade over time', 'reaching people who distrust institutions is hard', 'does not address the incentives of platforms'],
     'Repeat prebunking messages regularly ("booster shots") and combine them with platform design changes that slow viral misinformation.'),
]

AR('ch11-st3', [
    ('A long 12-mark response can still be placed in a middle markband.', 'Markbands reward the quality of evaluation rather than length.', 'a', 'Both true; R explains A.'),
    ('Students should spend the same time on every question in Paper 3.', 'Questions in Paper 3 carry different numbers of marks.', 'd', 'A is false – time should be proportional to marks; R is true.'),
    ('Planning an extended response helps achieve balance.', 'Markbands are applied using a best-fit approach.', 'b', 'Both true, but best fit does not explain why planning helps balance.'),
    ('Self-assessment always gives an accurate mark.', 'Students understand markbands better by applying them.', 'd', 'A is false – students can misjudge their work; R is true.'),
])


# =============================================================================================
# ch12 Paper 1 extended response skills
# =============================================================================================
@R.add('ch12-st1', 'C3', (1, 4), 'numerical')
def trend_table(rng, slot):
    topic = rng.choice([('adults who say they get news from social media', '%'),
                        ('households with a smart speaker', '%'),
                        ('students using a generative-AI tool for homework', '%'),
                        ('people who have heard of deepfakes', '%')])
    yrs = [2020, 2022, 2024]
    v0 = rng.randint(10, 40)
    v1 = v0 + rng.randint(3, 20)
    v2 = v1 + rng.randint(-5, 20)
    if v2 == v1:
        return None
    tot = v2 - v0
    biggest = '2020–2022' if (v1 - v0) > (v2 - v1) else '2022–2024'
    if (v1 - v0) == (v2 - v1):
        return None
    stem = (f'A survey reports the share of {topic[0]} in a country: 2020 {v0}%, 2022 {v1}%, 2024 {v2}%. '
            f'Calculate the overall change in percentage points from 2020 to 2024 and identify the two-year period with the larger change.')
    ans = f'{tot:+d} percentage points; larger change in {biggest}'
    key = f'{v2} − {v0} = {tot:+d} pp [A1]; changes {v1 - v0:+d} and {v2 - v1:+d}, so {biggest} [M1 A1].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain one reason why survey data like this should be treated with caution in a Paper 1 answer.'
        ans += '; sample size, wording and who was surveyed are unknown; self-reported data; may not represent all groups'
        key += ' Sampling/representativeness, wording, self-report [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch12-st1', F(
    terms=[('define (command term)', 'give the precise meaning of a word, phrase, concept or physical quantity'),
           ('outline (command term)', 'give a brief account or summary'),
           ('explain (command term)', 'give a detailed account including reasons or causes'),
           ('describe (command term)', 'give a detailed account'),
           ('identify (command term)', 'provide an answer from a number of possibilities'),
           ('real-world example', 'a specific, named and accurately described case (who, what, where, when) used as evidence, such as Cambridge Analytica or Aadhaar')],
    facts=[('Which IB command term means "give a detailed account including reasons or causes"?', 'Explain', ['Identify', 'Outline', 'State'], '"Explain" needs reasons; "outline" is brief.'),
           ('A Paper 1 question asks you to "identify two" features. What is required?', 'Two correct features, briefly stated', ['A full paragraph per feature', 'A balanced evaluation', 'A diagram'], 'Identify = provide answers from possibilities.'),
           ('Which is the best real-world example for a question about algorithmic bias in criminal justice?', 'COMPAS risk scores, investigated by ProPublica in 2016', ['A fictional robot in a film', '"Some companies use AI"', 'A general claim that AI is biased'], 'Specific, named and dated examples earn credit.'),
           ('Which Digital Society concept is most directly relevant to a question about who controls personal data?', 'Power', ['Space', 'Expression', 'Change only'], 'Power concerns control and influence over people and data.')],
    why=[('Explain why specific real-world examples earn more credit than general statements.', 'They provide evidence that grounds claims in reality, show accurate knowledge, and allow analysis of real stakeholders and impacts rather than assumptions.'),
         ('Explain why it is important to respond to the command term in a structured question.', 'Each command term sets the depth required: "identify" needs brief answers, "explain" needs reasons; answering at the wrong depth either wastes time or loses marks.'),
         ('Explain why linking an answer to a Digital Society concept strengthens it.', 'Concepts such as power, identity or values and ethics give an analytical lens, showing why impacts matter, not just what happens.')],
    contrast=[('outline', 'explain', '"Outline" asks for a brief summary; "explain" asks for a detailed account with reasons or causes.'),
              ('a definition', 'an example', 'A definition gives the precise meaning of a term; an example shows the term in a specific real-world case.')],
    misc=[('Using more examples always earns more marks.', 'One well-developed, accurate example often earns more than several superficial ones.'),
          ('Definitions can be written in any vague way as long as the key word is used.', 'A definition must be precise and include the defining features, not repeat the term.')],
    cases=[('a structured answer on Aadhaar', 'For "Explain one impact of biometric identity systems", a strong answer names India\'s Aadhaar (over 1.3 billion enrolled), explains that it enabled direct benefit transfers, and links to identity and power, noting exclusion when authentication failed.', 'using a real-world example',
            'specific facts, a clear impact and a concept link make the answer precise.'),
           ('a definition of "algorithmic bias"', 'A strong definition: "systematic and unfair differences in an algorithm\'s outputs for different groups, often caused by biased training data or design choices", illustrated by Amazon\'s scrapped recruiting tool.', 'definitions and examples',
            'precise wording plus an example demonstrates understanding.'),
           ('an "identify" question on GDPR', 'For "Identify two rights of data subjects under the GDPR", the right of access and the right to erasure are sufficient.', 'matching depth to command terms',
            'brief, accurate answers are appropriate for low-mark questions.')],
    sources=[('"Answers should be supported by specific, relevant real-world examples."', 'Paraphrase of common IB Digital Society examiner guidance',
              'Explain how a student could follow this guidance in a question about content moderation.', 'Name a specific case – e.g. Meta\'s Oversight Board ruling on the suspension of Donald Trump (2021) – and explain how it shows the impacts of moderation decisions.'),
             ('"Many candidates described technologies without addressing their impacts."', 'Paraphrase of a typical examiner comment',
              'Explain how a student could avoid this weakness.', 'Move from description to analysis by explaining effects on specific stakeholders and linking to concepts such as power or values.')],
    evaluate=[('Learning precise definitions is the most important skill for Paper 1.',
               ['definitions earn marks in short questions', 'precision supports analysis'],
               ['extended responses require examples, analysis and evaluation', 'concepts and contexts matter'],
               'Definitions are necessary foundations, but analysis with real examples earns most marks.')],
    extended=[('Using a real-world example, explain how one digital system affects the identity of its users.', 'Name system (e.g. Aadhaar, Instagram); explain impacts on identity; link to concepts; accurate details.', 6, 'long')],
))

AR('ch12-st1', [
    ('"Outline" questions require a brief account.', 'Outline means to give a brief account or summary.', 'a', 'Both true; R explains A.'),
    ('A general statement such as "AI can be biased" is a strong real-world example.', 'Examples should be specific, named and accurately described.', 'd', 'A is false; R is true and explains why A is false.'),
    ('COMPAS is a good example for questions about algorithmic bias.', 'COMPAS was developed by a company.', 'b', 'Both true, but being made by a company does not explain why it is a good example of bias.'),
])


@R.add('ch12-st2', 'C3', (2, 5), 'numerical')
def market_share(rng, slot):
    sector = rng.choice(['search engine', 'mobile operating system', 'cloud computing', 'digital advertising'])
    tot = rng.choice([200, 400, 600, 800])  # billion units/revenue
    a = rng.randint(30, 60)
    b = rng.randint(10, 100 - a - 10)
    sa = tot * a / 100
    sb = tot * b / 100
    stem = (f'In a hypothetical {sector} market worth US${tot} billion, Company A has a {a}% share and Company B has {b}%. '
            f'Calculate the revenue of each company and the combined share of the two firms, and use the result to support one point in an evaluation of platform power.')
    ans = f'A US${pc(sa, 1)} bn; B US${pc(sb, 1)} bn; combined {a + b}%; a high combined share suggests market concentration, giving firms power over prices, data and rules'
    key = f'{tot} × {a}% = {pc(sa, 1)} [A1]; {tot} × {b}% = {pc(sb, 1)} [A1]; {a} + {b} = {a + b}% [A1]; linked point on concentration/power [R1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=4)


R.facts('ch12-st2', F(
    terms=[('evaluate (command term)', 'make an appraisal by weighing up the strengths and limitations'),
           ('discuss (command term)', 'offer a considered and balanced review that includes a range of arguments, factors or hypotheses, supported by evidence'),
           ('impact', 'an effect of a digital system on people, communities or environments, which may be positive or negative'),
           ('implication', 'a likely future consequence or wider significance of an impact, such as effects on rights, power or trust'),
           ('counterclaim', 'an argument that challenges the main claim, used to give balance in an evaluation'),
           ('judgement', 'a reasoned conclusion that weighs the evidence and answers the question directly')],
    facts=[('Which feature most distinguishes a top-band Paper 1 extended response?', 'Balanced evaluation with specific examples leading to a supported conclusion', ['A long list of technologies', 'Many definitions', 'A personal anecdote only'], 'Balance, evidence and judgement are rewarded.'),
           ('Which is the strongest conclusion to an essay on facial recognition in policing?', 'A judgement that weighs evidence and states under what conditions it is acceptable', ['"There are advantages and disadvantages."', '"Technology is changing fast."', 'A new argument not discussed earlier'], 'A conditional, evidence-based judgement answers the question.'),
           ('Which pair of concepts best frames an evaluation of Cambridge Analytica?', 'Power and values and ethics', ['Space and change', 'Expression and space', 'Systems and space'], 'The case concerned control of data and ethical misuse.'),
           ('Which real-world example illustrates the impact of generative AI on media trust?', 'A deepfake robocall imitating President Biden before the New Hampshire primary in January 2024', ['The launch of the iPod in 2001', 'The invention of the World Wide Web', 'The Y2K bug'], 'Regulators then ruled AI-generated voices in robocalls illegal under existing law.')],
    why=[('Explain why balance is required in an evaluative extended response.', 'Evaluation means weighing strengths and limitations; considering counterclaims and different stakeholders shows the judgement is reasoned rather than one-sided.'),
         ('Explain why distinguishing impacts from implications improves analysis.', 'Impacts describe direct effects; implications show wider significance (e.g. loss of trust, shifts in power), demonstrating deeper thinking.'),
         ('Explain why a conclusion should be conditional ("to the extent that…").', 'Digital systems have different effects in different contexts and for different stakeholders, so a nuanced judgement is more convincing than an absolute one.')],
    contrast=[('an impact', 'an implication', 'An impact is a direct effect (e.g. data was harvested); an implication is the wider consequence (e.g. erosion of trust in elections).'),
              ('description', 'evaluation', 'Description says what a system does; evaluation weighs its strengths and limitations for stakeholders and reaches a judgement.')],
    misc=[('Balance means giving exactly equal space to both sides.', 'Balance means considering significant counterclaims fairly; the conclusion can still favour one side if evidence supports it.'),
          ('The conclusion should introduce a new example.', 'The conclusion should weigh the arguments already made and answer the question directly.')],
    cases=[('an essay on Cambridge Analytica', 'A strong response explains how data from up to 87 million Facebook users was harvested through a quiz app, evaluates claims about its influence on elections against evidence that its effect was unproven, and links to power and values and ethics.', 'balanced evaluation',
            'the judgement distinguishes the privacy harm (clear) from the electoral influence (contested).'),
           ('an essay on gig platforms', 'A response on Uber can weigh flexibility and income opportunities against algorithmic management, low pay and lack of benefits, citing the UK Supreme Court ruling (2021) that drivers are workers.', 'impacts on different stakeholders',
            'different stakeholders experience different impacts, so the conclusion is conditional.'),
           ('an essay on deepfakes', 'A response can evaluate creative and accessibility uses (e.g. voice restoration) against harms such as non-consensual imagery and election robocalls, and interventions such as labelling and laws.', 'evaluating impacts and implications',
            'harms are significant, but responses can be targeted at misuse rather than the technology itself.')],
    sources=[('"Claims about the effectiveness of psychographic targeting were greatly exaggerated."', 'Paraphrase of conclusions reached by researchers and the UK Information Commissioner\'s Office after investigating Cambridge Analytica (2020)',
              'Explain how a student could use this claim as a counterclaim in an evaluation.', 'After arguing that Cambridge Analytica threatened democracy, the student can note that evidence of actual influence on votes is weak, so the main harm was to privacy and trust.'),
             ('"The question is not whether AI will change work, but who will benefit from the change."', 'Paraphrase of a common argument in debates about automation',
              'Explain how this idea could shape the conclusion of an essay on automation.', 'It focuses the judgement on distribution of impacts and power, leading to a conclusion about the conditions (policy, skills) under which automation is beneficial.')],
    evaluate=[('Using concepts is more important than using examples in a Paper 1 extended response.',
               ['concepts give analytical depth', 'link impacts to wider significance'],
               ['examples provide evidence', 'markbands require both'],
               'Both are required; the strongest answers use examples as evidence and concepts as the lens for evaluation.')],
    extended=[('Evaluate the impact of one digital system on power relationships between individuals and organisations.', 'Real example (e.g. Cambridge Analytica, Aadhaar, gig platforms); impacts and implications; counterclaims; concepts; supported judgement.', 12, 'long')],
))


R.facts('ch12-st3', F(
    terms=[('example portfolio', 'an organised collection of real-world examples with key facts, dates, stakeholders and links to concepts, for use in exams'),
           ('currency (of a source)', 'how recent a source or example is, which matters in fast-changing digital topics'),
           ('reliability', 'how trustworthy and accurate a source is, judged by its origin, purpose, evidence and corroboration')],
    facts=[('Which detail is most important to record for each example in a portfolio?', 'Who, what, where, when and the impacts on stakeholders', ['Only the company logo', 'Only the URL', 'The author\'s favourite colour'], 'Precise details make examples usable in answers.'),
           ('Which source is generally most reliable for facts about an EU regulation?', 'The official text or the European Commission\'s website', ['An anonymous social-media post', 'A meme', 'A comment section'], 'Primary official sources are authoritative.'),
           ('Why should a portfolio include examples from different regions?', 'To show how impacts vary across local and global contexts', ['Because examiners only accept foreign examples', 'To make the portfolio longer', 'Because local examples are not allowed'], 'Contexts shape impacts.')],
    why=[('Explain why a portfolio should link each example to Digital Society concepts.', 'Concept links make examples ready to use analytically in answers, showing why the impacts matter, not only what happened.'),
         ('Explain why examples should be checked against more than one source.', 'Corroboration reduces the risk of recording inaccurate facts or biased interpretations.')],
    contrast=[('a primary source', 'a secondary source', 'A primary source is original evidence (a law, a company report, a court ruling); a secondary source interprets it (a news article, an academic analysis).')],
    misc=[('Older examples are useless in Digital Society.', 'Older cases such as Cambridge Analytica (2018) remain highly relevant if their impacts and implications are explained.')],
    cases=[('a portfolio entry on the DSA', 'Entry: EU Digital Services Act (2022, fully applicable 2024); who – platforms, users, Commission; key features – risk assessments, transparency, fines up to 6%; concepts – power, values; example use – content moderation questions.', 'organising examples',
            'structured entries make recall quick and accurate.'),
           ('a portfolio entry on Aadhaar', 'Entry: India\'s Aadhaar biometric ID (from 2009); over 1.3 billion enrolled; Supreme Court 2018 upheld it with limits; impacts – inclusion in welfare, exclusion when authentication fails, privacy; concepts – identity, power.', 'linking examples to concepts',
            'one example can serve questions on identity, data and governance.')],
    sources=[('"Examples should be accurate, relevant and well explained."', 'Paraphrase of IB Digital Society assessment guidance',
              'Explain how a portfolio helps students meet this expectation.', 'Recording verified facts, stakeholders and concept links in advance means examples can be used accurately and explained clearly under exam conditions.')],
    evaluate=[('A small number of well-researched examples is better than many brief ones.',
               ['depth enables analysis', 'accuracy'],
               ['breadth allows choice for different questions'],
               'A balanced portfolio of several deep examples covering different content areas is best.')],
    extended=[('Evaluate the usefulness of keeping a portfolio of real-world examples for the Digital Society course.', 'Accuracy, recall, concept links, breadth vs depth, currency; judgement.', 8, 'long')],
))

AR('ch12-st3', [
    ('A portfolio entry should record dates and stakeholders.', 'Precise details make examples credible and usable in answers.', 'a', 'Both true; R explains A.'),
    ('Social-media posts are the most reliable sources for portfolio facts.', 'Official documents and reputable reporting can be corroborated.', 'd', 'A is false; R is true.'),
    ('Older examples can still be used in Digital Society answers.', 'Cambridge Analytica became public in 2018.', 'b', 'Both true, but the date alone does not explain why older examples remain useful.'),
])

P2['ch12'] = dict(
    src=[('"A political consultant arranged an AI-generated robocall imitating President Biden\'s voice, urging New Hampshire voters not to vote in the January 2024 primary."', 'Summary of reporting on the New Hampshire robocall, 2024',
          'Identify two features of the incident described in {S}.', ['the voice was AI-generated to imitate the President', 'it urged voters not to vote in a primary (voter suppression)'],
          'Explain why {S} is significant for elections.', 'It shows how cheap generative AI can impersonate trusted figures at scale to mislead voters, threatening electoral integrity; the US FCC then ruled AI-voiced robocalls illegal under existing law.'),
         ('"Providers of AI systems that generate synthetic audio, image, video or text content shall ensure that the outputs are marked in a machine-readable format and detectable as artificially generated."', 'EU AI Act, Article 50(2) (2024), abridged',
          'Identify two requirements set out in {S}.', ['outputs must be marked in a machine-readable format', 'outputs must be detectable as AI-generated'],
          'Explain one limitation of the approach in {S}.', 'Watermarks and metadata can be removed or not applied by open-source or non-EU tools, so labelling cannot guarantee that all synthetic content is detectable.'),
         ('"Voice-cloning tools helped people who have lost the ability to speak to communicate in their own voice."', 'Paraphrase of reports on AI voice banking for people with motor neurone disease',
          'Identify two points made in {S}.', ['AI voice cloning can restore a person\'s own voice', 'it helps people who have lost speech communicate'],
          'Explain how {S} presents a different perspective on synthetic media.', 'It shows a beneficial, consent-based use of the same technology, suggesting that harms come from misuse rather than the technology itself.')],
    cmp=[(0, 2, 'the impacts of AI voice cloning', ['both concern AI-generated voices', 'both show its power to imitate real people'],
          ['Source A shows harmful deception without consent; Source C shows beneficial use with consent', 'A concerns democracy; C concerns health and identity']),
         (0, 1, 'responses to synthetic media', ['both concern AI-generated content that can mislead', 'both imply a need to identify synthetic content'],
          ['Source A describes a harmful incident; Source B describes a regulatory requirement', 'A is reporting; B is legal text'])],
    ev=[(0, 1, 'labelling requirements are an effective response to the risks of deepfakes.', ['machine-readable marking aids detection (Source B)', 'regulators act after incidents (Source A)'],
         ['bad actors can strip labels or use unregulated tools', 'robocalls (Source A) may not carry labels', 'detection lags generation']),
        (0, 2, 'the harms of synthetic media outweigh its benefits.', ['electoral manipulation (Source A)', 'non-consensual imagery and fraud'],
         ['accessibility and creative uses (Source C)', 'harms come from misuse and can be targeted by law'])],
)


@R.add('ch12-st3', 'C3', (1, 4), 'numerical')
def portfolio_cov(rng, slot):
    areas = ['data', 'algorithms', 'computers', 'media', 'networks and the internet', 'AI', 'robots and autonomous technologies']
    cnt = {a: rng.randint(0, 6) for a in areas}
    tot = sum(cnt.values())
    if tot < 10:
        return None
    lo = min(cnt.values())
    gaps = [a for a in areas if cnt[a] == lo]
    top = max(cnt, key=cnt.get)
    tbl = ', '.join(f'{a} {n}' for a, n in cnt.items())
    stem = (f'A student\'s portfolio of real-world examples has the following counts by content area: {tbl}. '
            f'Calculate the percentage of examples in the largest area ({top}) and identify the area(s) where new examples are most needed.')
    share = cnt[top] / tot * 100
    ans = f'{pc(share, 1)}% ({cnt[top]} of {tot}); most needed: {", ".join(gaps)}'
    key = f'Total = {tot} [M1]; {cnt[top]} ÷ {tot} × 100 = {pc(share, 1)}% [A1]; lowest count ({lo}) = {", ".join(gaps)} [A1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=3)


# =============================================================================================
# ch13 Internal assessment: inquiry project
# =============================================================================================
R.facts('ch13-st1', F(
    terms=[('inquiry project', 'the Digital Society internal assessment, in which students investigate a real-world digital system and its impacts on people and communities'),
           ('inquiry focus', 'a clear, specific statement of the digital system and the impacts on people or communities that the inquiry will investigate'),
           ('digital system', 'a combination of technologies, people and processes that work together, such as a school learning platform, a city\'s bike-share app or a national ID system'),
           ('scope', 'the limits of an inquiry – which system, which stakeholders, which place and time – that keep it manageable'),
           ('guiding question', 'a question that directs the research, such as "How has a food-delivery app affected the working conditions of riders in my city?"')],
    facts=[('What must the Digital Society inquiry project investigate?', 'A real-world digital system and its impacts on people or communities', ['A fictional technology', 'Only the history of computers', 'A purely technical programming problem'], 'The focus is on impacts, not just how the system works.'),
           ('Which inquiry focus is best?', '"The impacts of a city\'s e-scooter rental app on pedestrians with disabilities"', ['"Technology"', '"Social media is bad"', '"The internet"'], 'A good focus names a specific system and specific people affected.'),
           ('Why is a local or personally relevant system often a good choice for the inquiry?', 'It allows access to primary evidence such as interviews and observations', ['Examiners only accept local systems', 'It needs no sources', 'It avoids analysing impacts'], 'Access to evidence supports depth.'),
           ('Is the Digital Society inquiry project completed at both SL and HL?', 'Yes – the internal assessment is the same task for SL and HL', ['Only at HL', 'Only at SL', 'Neither'], 'The weighting differs between SL and HL.')],
    why=[('Explain why a narrow inquiry focus leads to a stronger inquiry.', 'A specific system, stakeholder group and context allow in-depth research and analysis within the time and length limits, whereas a broad topic leads to general description.'),
         ('Explain why the inquiry should focus on impacts on people and communities.', 'Digital Society studies how digital systems affect people; analysing impacts and implications for stakeholders is what the assessment rewards.'),
         ('Explain why students should check that enough sources exist before fixing an inquiry focus.', 'Without varied, reliable sources with different claims and perspectives, the inquiry cannot be evaluated in depth.')],
    contrast=[('a topic', 'an inquiry focus', 'A topic is a broad area (e.g. social media); an inquiry focus names a specific system and its impacts on specific people (e.g. TikTok\'s recommendation system and the body image of teenagers at my school).'),
              ('a digital system', 'a single device', 'A digital system includes technologies, people, data and processes working together; a single device is only one component.')],
    misc=[('Any interesting technology is a suitable inquiry focus.', 'The focus must be a real-world digital system with identifiable impacts on people or communities that can be researched.'),
          ('A broader inquiry focus shows more ambition and earns more marks.', 'Broad foci usually lead to superficial description; a specific focus allows depth.')],
    cases=[('refining an inquiry focus', 'A student starts with "AI in education", narrows to "generative-AI tools in my school", and finally to "the impacts of a generative-AI tutoring tool on students\' independent learning at my school".', 'formulating an inquiry focus',
            'narrowing to a specific system, group and impact makes the inquiry manageable.'),
           ('a local delivery-app inquiry', 'A student investigates how a food-delivery platform\'s algorithmic management affects riders in their city, using interviews, the company\'s policies and news reports.', 'choosing a real-world system',
            'local relevance gives access to primary evidence and multiple perspectives.')],
    sources=[('"Students should select a digital system that is real and that has impacts on people and communities."', 'Paraphrase of IB Digital Society internal assessment guidance',
              'Explain how a student could check that their chosen system meets this requirement.', 'Identify the system\'s components and stakeholders, find evidence of actual effects on people, and confirm there are sources describing these impacts.')],
    evaluate=[('A local digital system is a better choice for the inquiry than a global one.',
               ['access to primary evidence', 'personal relevance and engagement'],
               ['fewer published sources', 'global systems have broader implications'],
               'A global system examined in a local context often combines the advantages of both.')],
    extended=[('Evaluate two possible inquiry foci and justify which is more suitable.', 'Specificity; real system; impacts on people; available sources; manageability; justified choice.', 6, 'long')],
))

AR('ch13-st1', [
    ('"Social media" is too broad as an inquiry focus.', 'A good inquiry focus names a specific system and specific people affected.', 'a', 'Both true; R explains A.'),
    ('The inquiry project should explain only how a system works technically.', 'The inquiry analyses impacts on people and communities.', 'd', 'A is false; R is true and explains why.'),
])


@R.add('ch13-st2', 'C3', (1, 4), 'numerical')
def survey_inquiry(rng, slot):
    sent = rng.choice([60, 80, 120, 200, 300])
    rr = rng.choice([25, 40, 50, 60, 75])
    resp = round(sent * rr / 100)
    yes = rng.randint(int(resp * 0.2), int(resp * 0.8))
    share = yes / resp * 100
    q = rng.choice(['use the school\'s learning app every day', 'have changed privacy settings on their phone', 'have seen a deepfake video', 'trust AI chatbots for homework answers'])
    stem = (f'For their inquiry, a student sends a questionnaire to {sent} students; {resp} reply. Of these, {yes} say they {q}. '
            f'Calculate the response rate and the percentage of respondents who {q}.')
    ans = f'response rate {pc(resp / sent * 100, 1)}%; {pc(share, 1)}% of respondents'
    key = f'{resp} ÷ {sent} × 100 = {pc(resp / sent * 100, 1)}% [M1 A1]; {yes} ÷ {resp} × 100 = {pc(share, 1)}% [A1].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain one limitation of this evidence and how the student could address it.'
        ans += '; small, self-selected sample may not be representative; corroborate with interviews, published studies or wider data, and acknowledge the limitation'
        key += ' Representativeness/self-selection/self-report [R1]; triangulation or acknowledgement [R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch13-st2', F(
    terms=[('claim', 'a statement presented as true by a source, such as "the app improves student engagement"'),
           ('perspective', 'the point of view from which a source presents information, shaped by its author\'s position, interests and values'),
           ('primary source', 'original evidence collected or produced first-hand, such as interviews, surveys, company policies or laws'),
           ('secondary source', 'a source that interprets or analyses primary evidence, such as a news article or academic review'),
           ('origin, purpose, value and limitation', 'a framework for evaluating sources by who produced them and when, why, what makes them useful and what restricts their usefulness'),
           ('triangulation', 'checking a claim using several independent sources or methods')],
    facts=[('Which is a primary source for an inquiry into a school learning app?', 'An interview with teachers who use the app', ['A news article summarising education apps', 'A textbook chapter on edtech', 'A Wikipedia page about the app'], 'Interviews are first-hand evidence.'),
           ('A company press release says its app "transforms learning". What is the main limitation of this source?', 'Its purpose is promotional, so it may exaggerate benefits', ['It is too old', 'It is a primary source', 'It is written in English'], 'Purpose affects reliability.'),
           ('Which checklist evaluates sources by currency, relevance, authority, accuracy and purpose?', 'The CRAAP test', ['The Turing test', 'The Bechdel test', 'The Mendelow grid'], 'Developed at California State University, Chico.'),
           ('Which is the best way to deal with conflicting claims from two sources?', 'Compare their origins, purposes and evidence and seek corroboration', ['Ignore both', 'Use whichever is longer', 'Use the most recent only'], 'Evaluation explains why sources differ.')],
    why=[('Explain why an inquiry should include sources with different perspectives.', 'Different stakeholders experience a system differently; including users, companies, critics and regulators gives a balanced understanding and supports evaluation.'),
         ('Explain why documenting claims from sources is important in the inquiry.', 'Recording who claims what, and on what evidence, allows the student to compare and evaluate claims rather than presenting them as facts.'),
         ('Explain why primary research by students should be conducted ethically.', 'Participants\' consent, privacy and anonymity must be protected, especially when collecting personal data from peers or minors.')],
    contrast=[('a claim', 'evidence', 'A claim is a statement a source asserts; evidence is the data or observation that supports or challenges it.'),
              ('value of a source', 'limitation of a source', 'Value is what makes the source useful (expertise, first-hand access); limitation is what restricts its usefulness (bias, small sample, age).')],
    misc=[('A source with a bias is useless.', 'Biased sources still show a perspective – for example a company\'s view – and are valuable if their purpose is recognised.'),
          ('Academic sources never need evaluating.', 'Academic studies can be outdated, narrow in sample or funded by interested parties, so they also need evaluation.')],
    cases=[('evaluating sources on a ride-hailing app', 'A student compares the company\'s statements on driver earnings with a union survey and an academic study; each gives a different picture because of different purposes and methods.', 'claims and perspectives',
            'evaluating origin and purpose explains why the claims differ.'),
           ('ethical interviews for an inquiry', 'A student interviewing classmates about a monitoring app gets informed consent, anonymises responses and stores notes securely.', 'ethical primary research',
            'ethical research protects participants and strengthens the credibility of the inquiry.')],
    sources=[('"Our app has increased student engagement by 40%."', 'Marketing page of an educational-technology company',
              'Evaluate the value and limitation of this source for an inquiry.', 'Value: shows the company\'s claims and perspective. Limitation: promotional purpose; the 40% figure lacks method, sample and definition of "engagement", so needs corroboration.'),
             ('"Many students said the app made them feel watched."', 'Student interview notes from an inquiry project',
              'Explain one value and one limitation of this source.', 'Value: first-hand perspective of affected users. Limitation: small, possibly unrepresentative sample; responses may be influenced by the interviewer.')],
    evaluate=[('Primary sources are more valuable than secondary sources for the inquiry project.',
               ['first-hand perspectives of affected people', 'local, specific evidence'],
               ['small samples', 'secondary sources give context, scale and expert analysis'],
               'Combining primary and secondary sources gives the most balanced and reliable inquiry.')],
    extended=[('Evaluate three sources a student could use for an inquiry into a digital system, considering claims and perspectives.', 'Identify sources of different types; claims; origin and purpose; value and limitation; how they combine.', 8, 'long')],
))


@R.add('ch13-st3', 'C3', (1, 4), 'numerical')
def presentation_plan(rng, slot):
    total = 10
    parts = rng.choice([('introduction and inquiry focus', 'claims and perspectives', 'analysis of impacts and implications', 'conclusion'),
                        ('the digital system and focus', 'evidence from sources', 'impacts and implications for stakeholders', 'conclusion and further inquiry')])
    pct = rng.choice([(10, 25, 50, 15), (15, 25, 45, 15), (10, 30, 45, 15), (10, 20, 55, 15)])
    mins = [total * p / 100 for p in pct]
    stem = (f'A student plans a {total}-minute inquiry presentation with sections: ' +
            ', '.join(f'{s} ({p}%)' for s, p in zip(parts, pct)) +
            '. Calculate the time for each section in minutes and seconds.')
    fmt = lambda m: f'{int(m)} min {int(round((m - int(m)) * 60))} s'
    ans = '; '.join(f'{s}: {fmt(m)}' for s, m in zip(parts, mins))
    key = '; '.join(f'{p}% × {total} = {pc(m, 2)} min = {fmt(m)}' for p, m in zip(pct, mins)) + ' [M1 A2].'
    m = 3
    if slot.d >= 3:
        stem += ' Explain why the analysis section is given the most time.'
        ans += '; analysis and evaluation of impacts and implications is the core of the inquiry and carries the most weight in assessment'
        key += ' Analysis of impacts/implications is central to the task [R1 R1].'
        m = 5
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=m)


R.facts('ch13-st3', F(
    terms=[('multimedia presentation', 'the recorded presentation in the Digital Society inquiry, combining speech with visuals such as images, data and video'),
           ('impacts', 'the effects of the digital system on people and communities that the presentation analyses'),
           ('implications', 'the wider or longer-term consequences of the impacts, such as effects on rights, equality or trust'),
           ('further inquiry', 'questions or directions for future investigation identified in the conclusion'),
           ('visual evidence', 'images, charts, screenshots or short clips that support claims in the presentation, with sources acknowledged')],
    facts=[('What is the maximum length of the recorded multimedia presentation in the Digital Society inquiry project?', '10 minutes', ['3 minutes', '30 minutes', '1 hour'], 'Students must plan time carefully.'),
           ('Which is the best use of visuals in the presentation?', 'Charts and images that support specific claims, with sources cited', ['Decorative animations on every slide', 'Long paragraphs of text', 'Unrelated memes'], 'Visuals should communicate evidence.'),
           ('What should the conclusion of the presentation include?', 'A judgement about impacts and implications that follows from the analysis', ['A list of all sources', 'A new topic', 'Only a thank-you slide'], 'The conclusion answers the inquiry focus.'),
           ('Which concept would best frame an inquiry into a workplace monitoring app?', 'Power', ['Space only', 'Expression only', 'None – concepts are not needed'], 'Monitoring concerns control and the balance of power between employers and workers.')],
    why=[('Explain why the presentation should analyse impacts on more than one stakeholder.', 'Different groups experience a system differently, so comparing impacts gives balance and supports a stronger evaluation.'),
         ('Explain why implications should be discussed as well as impacts.', 'Implications show the wider significance and future consequences, demonstrating deeper analysis than simply describing effects.'),
         ('Explain why sources should be acknowledged in the presentation.', 'Acknowledging sources shows academic honesty, lets the audience judge evidence and distinguishes the student\'s analysis from others\' claims.')],
    contrast=[('analysis', 'description', 'Description says what the system does; analysis explains how and why it affects people and what the implications are.'),
              ('a conclusion', 'a summary', 'A summary repeats points; a conclusion makes a judgement that answers the inquiry focus and may suggest further inquiry.')],
    misc=[('More slides make a better presentation.', 'Clarity, focus and well-chosen evidence matter more than the number of slides.'),
          ('The presentation can exceed the time limit if the content is good.', 'The time limit must be respected; planning and editing are part of the task.')],
    cases=[('a presentation on a school monitoring app', 'A student analyses a school laptop-monitoring app: impacts on safety, privacy and trust for students, teachers and parents; implications for surveillance norms; conclusion on proportionality.', 'analysing impacts and implications',
            'considering several stakeholders produces a balanced conclusion.'),
           ('a presentation on a city bike-share app', 'A student shows usage data and interviews, analysing benefits for commuters and the environment and barriers for people without smartphones or bank cards.', 'inclusion and access',
            'using local data and voices makes the analysis specific and credible.')],
    sources=[('"Visuals should support, not replace, the analysis."', 'Paraphrase of common advice on multimedia presentations',
              'Explain how a student could apply this advice.', 'Use each chart or image to illustrate a specific claim and explain what it shows, rather than relying on visuals without commentary.')],
    evaluate=[('A recorded multimedia presentation is an effective way to assess a Digital Society inquiry.',
               ['develops digital communication skills', 'allows evidence to be shown visually'],
               ['technical skills may affect quality', 'time limit restricts depth'],
               'It is effective when assessment focuses on analysis rather than production quality.')],
    extended=[('Plan the analysis section of a presentation on a digital system of your choice, evaluating its impacts and implications for two stakeholders.', 'Named system; two stakeholders; impacts; implications; evidence; concept; judgement.', 8, 'long')],
))


@R.add('ch13-st4', 'C3', (1, 3), 'numerical')
def process_doc_words(rng, slot):
    limit = 300
    parts = rng.choice([('inquiry focus and its development', 'selection of sources', 'reflection on the process'),
                        ('choosing the system', 'research and evaluation of sources', 'reflection and changes made')])
    used = [rng.randint(60, 120), rng.randint(60, 120)]
    left = limit - sum(used)
    if left < 20:
        return None
    stem = (f'The inquiry process document has a {limit}-word limit. A student writes {used[0]} words on {parts[0]} and {used[1]} words on {parts[1]}. '
            f'Calculate how many words remain for {parts[2]}, and the percentage of the limit already used.')
    ans = f'{left} words; {pc(sum(used) / limit * 100, 1)}% used'
    key = f'{limit} − ({used[0]} + {used[1]}) = {left} [M1 A1]; {sum(used)} ÷ {limit} × 100 = {pc(sum(used) / limit * 100, 1)}% [A1].'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=3)


R.facts('ch13-st4', F(
    terms=[('inquiry process document', 'a short written document (maximum 300 words) in which the student explains how the inquiry developed, including the focus, sources and reflection'),
           ('citation', 'a reference in the text or presentation to the source of information, following a consistent style'),
           ('reference list', 'a full list of the sources used, with details such as author, title, date and URL'),
           ('reflection', 'considering what went well, what was difficult and what was changed during the inquiry, and why'),
           ('academic integrity', 'honesty in academic work, including acknowledging the ideas, words and images of others and declaring the use of AI tools')],
    facts=[('What is the maximum length of the inquiry process document?', '300 words', ['50 words', '1,500 words', '4,000 words'], 'It must be concise.'),
           ('Which is an example of a complete reference?', 'Author, title, publisher or website, date and URL', ['Only "Google"', 'Only the website name', 'Only the date accessed'], 'References must allow the source to be found.'),
           ('If a student uses an AI tool during the inquiry, what should they do under IB academic-integrity guidance?', 'Acknowledge and cite its use', ['Hide it', 'Copy its output as their own work', 'Use it only for the conclusion without saying so'], 'The IB expects transparency about AI use.'),
           ('Which is the best reflection in a process document?', '"Interviews revealed concerns I had not found online, so I added a privacy perspective to my focus."', ['"It went well."', '"I liked the topic."', '"The internet was slow."'], 'Good reflection explains changes and their reasons.')],
    why=[('Explain why the process document should explain changes to the inquiry focus.', 'It shows the inquiry developed in response to evidence, demonstrating genuine investigation and critical thinking.'),
         ('Explain why consistent citations are required.', 'They give credit, avoid plagiarism and allow readers to check claims, supporting academic integrity and credibility.')],
    contrast=[('a citation', 'a reference', 'A citation is a brief in-text or on-slide acknowledgement; a reference is the full source details in the reference list.'),
              ('reflection', 'description of the process', 'Description lists steps taken; reflection evaluates why choices were made and what was learned or changed.')],
    misc=[('Only direct quotations need to be cited.', 'Paraphrased ideas, data, images and AI-generated content must also be acknowledged.'),
          ('The process document should repeat the content of the presentation.', 'It explains how the inquiry was carried out and developed, not its findings.')],
    cases=[('a process-document entry', 'A student explains that their original focus on "online gaming" was narrowed to "loot boxes in one popular game and spending by teenagers" after finding UK and Belgian regulatory reports.', 'documenting development of the inquiry',
            'concise reflection shows how evidence shaped the focus.'),
           ('citing an AI tool', 'A student who used a chatbot to brainstorm search terms states this in the process document and cites the tool and date, as IB guidance requires.', 'academic integrity',
            'transparent acknowledgement maintains integrity.')],
    sources=[('"Students must acknowledge all sources, including AI tools, used in their work."', 'Paraphrase of IB academic integrity policy guidance (2023)',
              'Explain why this requirement is important in the inquiry project.', 'It ensures assessment reflects the student\'s own work and lets examiners see how sources and tools contributed.')],
    evaluate=[('A 300-word limit is sufficient to document the inquiry process.',
               ['forces concise, focused reflection', 'reduces repetition'],
               ['complex inquiries may be hard to summarise', 'little space for detail'],
               'The limit is sufficient if students prioritise key decisions and reasons.')],
    extended=[('Write and justify the key points you would include in an inquiry process document for a project on a digital system.', 'Focus and its development; source selection and evaluation; reflection on changes; citations; concise.', 6, 'long')],
))

AR('ch13-st4', [
    ('Paraphrased ideas must be cited.', 'Academic integrity requires acknowledging others\' ideas, not only their exact words.', 'a', 'Both true; R explains A.'),
    ('The process document should report the findings of the inquiry.', 'The process document explains how the inquiry developed.', 'd', 'A is false; R is true and explains why.'),
])


# =============================================================================================
# Extra Paper 2 comparison / evaluation prompts (6 mocks need more variety per source set)
# =============================================================================================
P2['ch02']['cmp'].append((0, 2, 'the role of users in the spread of misinformation', ['both concern how people respond to misleading content'],
                          ['Source A shows people spread falsehood widely; Source C shows people can be trained to resist it', 'A is observational data; C is an experiment']))
P2['ch02']['ev'] += [
    (1, 2, 'platform self-regulation is sufficient to address misinformation.', ['rapid removal and labelling (Source B)', 'platforms fund prebunking research (Source C)'],
     ['self-reported claims cannot be verified (Source B)', 'falsehood still outpaces truth (Source A)', 'DSA shows regulators judged self-regulation insufficient']),
    (0, 2, 'misinformation is mainly a problem of human behaviour rather than technology.', ['people, not bots, drove the spread of falsehood (Source A)', 'skills training helps (Source C)'],
     ['recommender systems amplify engaging falsehoods', 'deepfakes make deception easier (Source B)', 'design changes can reduce spread']),
]
P2['ch04']['cmp'].append((0, 1, 'the impact of AI on jobs', ['both suggest AI will substitute for some human work'],
                          ['Source A is a global, cautious projection; Source B is a confident single-company claim', 'A stresses inequality; B stresses efficiency and customer satisfaction']))
P2['ch04']['ev'] += [
    (1, 2, 'companies, rather than governments, should manage the effects of AI on workers.', ['firms decide how AI is deployed (Source B)', 'augmentation within firms raises productivity (Source C)'],
     ['companies prioritise cost cutting (Source B)', 'inequality is a society-wide issue needing policy (Source A)', 'reskilling and safety nets require public action']),
    (0, 1, 'the benefits of generative AI for productivity outweigh its risks for employment.', ['14% productivity gains (Source C)', 'efficiency claims (Source B)'],
     ['40% of jobs affected and inequality may rise (Source A)', 'productivity gains may not be shared with workers', 'company claims are unverified']),
]
P2['ch06']['cmp'].append((1, 2, 'what makes autonomous vehicles acceptable to the public', ['both relate to public trust in AVs'],
                          ['Source B relies on statistical safety; Source C stresses moral preferences that vary by culture', 'B is a company report; C is an academic survey']))
P2['ch06']['ev'] += [
    (0, 1, 'autonomous vehicles should be allowed on public roads only after independent safety certification.', ['independent investigation revealed failures (Source A)', 'company data are self-reported (Source B)'],
     ['certification could delay safety benefits (Source B)', 'real-world testing is needed to improve systems', 'regulators may lack expertise']),
    (0, 2, 'responsibility for autonomous-vehicle crashes should lie with manufacturers.', ['design choices such as disabled braking caused harm (Source A)', 'manufacturers decide how vehicles weigh risks (Source C)'],
     ['safety drivers and operators also share responsibility', 'unclear legal frameworks', 'shared liability models may be fairer']),
]
P2['ch09']['cmp'].append((0, 1, 'the frequency and justification of shutdowns', ['both concern government use of internet shutdowns'],
                          ['Source A counts shutdowns globally as a problem; Source B justifies one shutdown as necessary', 'A is an NGO report; B is an official order']))
P2['ch09']['ev'] += [
    (0, 1, 'civil-society monitoring is the most effective way to limit internet shutdowns.', ['systematic documentation raises costs for governments (Source A)', 'litigation and campaigns'],
     ['governments still justify and impose shutdowns (Source B)', 'record numbers despite monitoring (Source A)', 'UN standards and courts may have more authority (Source C)']),
    (1, 2, 'national security can justify restrictions on internet access.', ['governments cite misinformation and public order (Source B)', 'some restrictions are lawful if necessary and proportionate'],
     ['UN says shutdowns are inherently disproportionate (Source C)', 'targeted measures exist', 'shutdowns hide abuses and harm services']),
]
P2['ch12']['cmp'].append((1, 2, 'how society should respond to synthetic media', ['both concern AI-generated audio or media'],
                          ['Source B focuses on controlling risks through labelling; Source C highlights beneficial uses', 'B is legal text; C reports user experiences']))
P2['ch12']['ev'] += [
    (0, 2, 'AI voice cloning should be banned.', ['used to deceive voters (Source A)', 'fraud and impersonation risks'],
     ['beneficial uses such as voice banking (Source C)', 'bans are hard to enforce', 'targeted laws against misuse and labelling (Source B) are more proportionate']),
    (1, 2, 'regulation can balance the benefits and risks of synthetic media.', ['labelling duties (Source B) leave beneficial uses allowed (Source C)', 'FCC ruling after the robocall (Source A)'],
     ['bad actors ignore regulation (Source A)', 'technical limits of watermarking', 'regulation varies between countries']),
]
