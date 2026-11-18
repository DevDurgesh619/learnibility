"""IB DP Social and Cultural Anthropology SL/HL (first assessment 2019) – ib-g11-sociology.

The platform slug is "sociology"; the IB course nearest to it is Social and Cultural Anthropology (SCA).
Year 1: the language of anthropology and the key concepts (belonging, change, classification, culture,
identity, materiality, power, social relations, society, space-place-time), ethnography and fieldwork,
ethics, anthropological theory, reading ethnography, and two areas of inquiry (Classifying the world;
Health, illness and healing), plus Paper 1 unseen-text skills and the observation exercise.

Item styles
  * C1 knowledge: define / state / identify, MCQs on concepts, theorists and ethnographies,
  * C2 conceptual: explain / distinguish / correct a misconception,
  * C3 application: ethnographic case items, "with reference to an ethnography" items (Paper 2 Section B
    part (a) style), and Paper 1 Q1 (describe) and Q2 (explain / analyse) on short ORIGINAL ethnographic
    extracts written for this bank (fictional composites, labelled as such),
  * C4 evaluation: Paper 1 Q3 (compare the text with an ethnography studied), HL ethics question, HL
    "big question", Paper 2 essays and two-ethnography comparisons, all with markband keys.

Ethnographies are real and attributed (author, title, date, people and place); the catalogue E is shared
with the grade 12 pack (ib_g12_sociology.py imports Pack and E from this module).
"""
from __future__ import annotations

import re

from _common import F, Registry, T, mcq  # noqa: F401

CONFIG = {'minutesPerMark': 2.0, 'mcqMinutes': 1.5}

# One mock = Paper 1 (unseen text: Q1 describe 4, Q2 explain 6, Q3 compare 10; HL big question 10, HL ethics 10)
# + Paper 2 (Section A essay 15; Section B two questions, each (a) 5 + (b) 10).
# 10 items, 85 marks per mock. Paper 1 Q1–Q3 marks follow the SCA guide; the HL and Paper 2 splits are
# an assumption (targets.json marks the pattern UNVERIFIED).
MOCK = [
    dict(section='Paper 1 Section A Q1 – describe (unseen ethnographic text)', count=1, c=['C3'], d=[2, 3], type='case', marks=4, style='p1_describe'),
    dict(section='Paper 1 Section A Q2 – explain / analyse (unseen text)', count=1, c=['C3'], d=[3, 4], type='case', marks=6, style='p1_explain'),
    dict(section='Paper 1 Section A Q3 – compare and contrast with an ethnography studied', count=1, c=['C4'], d=[4], type='long', marks=10, style='p1_compare'),
    dict(section='Paper 1 (HL) – big question', count=1, c=['C4'], d=[4, 5], type='long', marks=10, style='big'),
    dict(section='Paper 1 (HL) – ethics question on the text', count=1, c=['C4'], d=[4], type='long', marks=10, style='ethics'),
    dict(chapters=[2, 5, 7, 8, 9, 10], section='Paper 2 Section A – area of inquiry essay (one ethnography in depth)', count=1, c=['C4'], d=[4, 5], type='long', marks=15, style='essay'),
    dict(chapters=[2, 7, 8, 9, 10], section='Paper 2 Section B Q2(a) – explain with one ethnography', count=1, c=['C3'], d=[3], type='case', marks=5, style='p2_a'),
    dict(chapters=[2, 7, 8, 9, 10], section='Paper 2 Section B Q2(b) – compare two ethnographies', count=1, c=['C4'], d=[4], type='long', marks=10, style='p2_b'),
    dict(chapters=[2, 7, 8, 9, 10], section='Paper 2 Section B Q3(a) – explain with one ethnography', count=1, c=['C3'], d=[3], type='case', marks=5, style='p2_a'),
    dict(chapters=[2, 7, 8, 9, 10], section='Paper 2 Section B Q3(b) – compare two ethnographies', count=1, c=['C4'], d=[4, 5], type='long', marks=10, style='p2_b'),
]

CL = {'belonging': 'belonging', 'change': 'change', 'classification': 'classification', 'culture': 'culture',
      'identity': 'identity', 'materiality': 'materiality', 'power': 'power', 'social_relations': 'social relations',
      'society': 'society', 'space': 'space, place and time'}

# ---------------------------------------------------------------------------------------------
# Markbands
# ---------------------------------------------------------------------------------------------
P1Q2_BANDS = [
    'limited understanding; mostly description or paraphrase of the text, concepts absent or misused',
    'some explanation with relevant points from the text; a key concept is used, though analysis is uneven',
    'clear, well-supported explanation that analyses the text using relevant anthropological concepts and terminology',
]
COMPARE_BANDS = [
    'limited knowledge; comparison implicit or absent; little reference to the text or to an ethnography',
    'some relevant ethnographic knowledge; mostly descriptive, the text and the ethnography treated separately',
    'relevant, contextualised ethnography (author, people, place, time); explicit comparison with some analysis of similarities and differences',
    'detailed, accurate ethnographic knowledge; developed comparison of similarities and differences linked to key concepts',
    'sustained, insightful comparison of similarities and differences; ethnography fully contextualised; concepts and theory used critically',
]
ESSAY_BANDS = [
    'little understanding of the question; generalised or inaccurate ethnographic material; mainly description',
    'some understanding; ethnographic material relevant but thin or poorly contextualised; limited use of concepts',
    'question understood; relevant ethnography with context; some analysis linked to key concepts, partly descriptive',
    'focused, well-structured answer; detailed, contextualised ethnography; clear analysis using concepts and theory; some evaluation of perspectives',
    'sharply focused, well-structured argument; detailed, accurate ethnography used critically; sophisticated use of concepts and theory; reasoned, supported conclusion',
]
ETHICS_BANDS = [
    'ethical issues identified only in general terms, with little reference to the text',
    'some relevant ethical issues (e.g. consent, harm) identified and partly explained with reference to the text',
    'relevant ethical issues explained with reference to the text and to professional principles',
    'well-developed discussion of several ethical issues and competing obligations, closely linked to the text',
    'insightful, balanced discussion of ethical dilemmas, competing obligations and possible responses, fully grounded in the text and professional codes',
]
BIG_BANDS = [
    'limited response to the big question; assertions with little anthropological support',
    'some relevant ideas; ethnographic or conceptual support is thin or general',
    'relevant response using a key concept and an ethnography, with some analysis',
    'clear argument that applies the key concept to ethnographic material and considers more than one perspective',
    'perceptive, well-argued response integrating key concepts, ethnography and theory, with a reasoned conclusion',
]
STYLE = {
    'essay_marks': 15, 'eval_marks': 10,
    'markband': ('IB SCA Paper 2 markbands scaled to the marks: top band – focused argument, detailed and contextualised '
                 'ethnography (author, people, place, time), key concepts and theory used critically, reasoned conclusion; '
                 'middle band – relevant ethnography and some analysis but partly descriptive; lower band – generalised, '
                 'little ethnographic support.'),
}


def bands(m: int, texts) -> str:
    n = len(texts)
    edges = [round(m * i / n) for i in range(n + 1)]
    out = ['0: does not reach the standard described below']
    for i in range(n):
        lo, hi = edges[i] + 1, edges[i + 1]
        if lo > hi:
            continue
        out.append(f'{lo}–{hi}: {texts[i]}' if lo != hi else f'{hi}: {texts[i]}')
    return 'Markbands – ' + '; '.join(reversed(out)) + '.'


# ---------------------------------------------------------------------------------------------
# Ethnography catalogue (shared with grade 12)
# ---------------------------------------------------------------------------------------------
E: dict[str, dict] = {}


def eth(key, cite, short, where, **c):
    E[key] = dict(cite=cite, short=short, where=where, c=c)


BIGQ = {
    'belonging': ['What does it mean to belong?', 'Who has the power to define a community and its boundaries?'],
    'change': ['Is change a threat to cultural identity, or a condition of it?', 'Why do people hold on to tradition in times of rapid change?'],
    'classification': ['Are the categories people use to order the world natural or made?', 'Why do humans divide the world into categories?'],
    'culture': ['Is culture something people have, or something people do?', 'Is there such a thing as a universal human experience?'],
    'identity': ['Are we who we say we are, or who others say we are?', 'Is change a threat to cultural identity, or a condition of it?'],
    'materiality': ['How far do material things make us who we are?', 'How are inequalities written onto human bodies?'],
    'power': ['Is resistance always possible?', 'How are inequalities written onto human bodies?'],
    'social_relations': ['What do people owe one another?', 'Is there such a thing as a universal human experience?'],
    'society': ['What holds a society together?', 'Is there such a thing as a universal human experience?'],
    'space': ['What makes a place home?', 'How do people make places meaningful?'],
}
BIGQ_ANY = ['Can an anthropologist ever fully understand another way of life?']

PROPER = {'Malinowski', 'Mead', 'Geertz', 'Boas', 'Bourdieu', 'Bourgois', 'Douglas', 'Dumont', 'Dirks', 'Kleinman',
          'Farmer', 'Ong', 'Holmes', 'Scheper-Hughes', 'Abu-Lughod', 'Ortner', 'Wolf', 'Lévi-Strauss', 'Radcliffe-Brown',
          'Evans-Pritchard', 'Tylor', 'Morgan', 'Indigenous', 'Western', 'European', 'Caste', 'Hindu', 'Ayurveda',
          'Ayurvedic', 'Turner', 'Carsten', 'Weston', 'Scott', 'Foucault', 'Gramsci', 'Barth', 'Augé', 'Low', 'Malkki',
          'Levitt', 'De', 'Internet', 'IB', 'Paper', 'AAA', 'ASA', 'Writing', 'Fieldwork'}


def lc_claim(c: str) -> str:
    w = c.split(' ', 1)[0]
    if w in PROPER or not w[:1].isupper() or (len(w) > 1 and w[1].isupper()):
        return c
    return c[0].lower() + c[1:]


class Pack:
    """Holds one grade's content; templates(st) returns fact templates plus SCA-specific templates."""

    def __init__(self):
        self.R = Registry()
        self.X: dict[str, dict] = {}
        self.claims: list[str] = []

    # -----------------------------------------------------------------------------------------
    def S(self, key, topic, concepts, eths, terms=(), facts=(), why=(), contrast=(), misc=(), cases=(), apply=(),
          ev=(), essays=(), ext=(), extended=(), sources=(), generic=False):
        for e in eths:
            assert e in E, (key, e)
        for c in concepts:
            assert c in CL, (key, c)
        for x in ext:
            assert len(x) == 8 and x[6] in CL, (key, x[:40])
        q = lambda c: c.replace('"', "'")
        misc = [(q(a), b) for a, b in misc]
        ev = [(q(e[0]),) + tuple(e[1:]) for e in ev]
        self.R.facts(key, F(terms=list(terms), facts=list(facts), why=list(why), contrast=list(contrast),
                            misc=list(misc), apply=list(apply), cases=list(cases), evaluate=list(ev),
                            extended=list(extended), sources=list(sources)))
        self.X[key] = dict(topic=topic, concepts=list(concepts), eths=list(eths), ext=list(ext), ev=list(ev),
                           essays=list(essays), generic=generic)
        self.claims += [m[0] for m in misc] + [e[0] for e in ev]

    # -----------------------------------------------------------------------------------------
    def templates(self, st):
        key = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
        out = [self._wrap(t) for t in self.R.build(st, STYLE)]
        if key in self.X:
            out += sca_templates(self.X[key])
        return out

    def _wrap(self, t):
        fn = t.fn
        claims = self.claims

        def fixed(rng, slot):
            o = fn(rng, slot)
            if o:
                for c in claims:
                    good = lc_claim(c)
                    if good != c:
                        o['stem'] = o['stem'].replace('that ' + c[:40], 'that ' + good[:40])
            return o
        t.fn = fixed
        return t


G_DESC = ['Refer to at least three specific details from the text.',
          'Focus on what the people in the text do and say, not on your interpretation of it.',
          'Use brief quotations from the text to support each point you make.',
          'Organise your answer as a series of clearly separated descriptive points.',
          'You do not need to refer to any other ethnography in this answer.',
          'Write in your own words and keep close to the evidence in the extract.']
G_EXPL = ['Make clear which key concept you are using and why it is relevant.',
          'Support each step of your explanation with evidence from the extract.',
          'You may consider more than one possible interpretation of the evidence.',
          'Link the actions described to wider social, economic or political conditions.',
          'Distinguish between what the text shows and what you infer from it.',
          'Use appropriate anthropological terminology throughout your answer.']
G_COMP = ['Your answer should identify both similarities and differences.',
          'Make sure you contextualise the ethnography: author, people, place and time.',
          'Keep the comparison running throughout rather than treating each case separately.',
          'Consider how the methods or theory of the ethnography might explain the differences.',
          'Refer to specific evidence from both the text and the ethnography.']
G_ETH = ['Refer to specific situations in the text rather than listing general principles.',
         'Consider the obligations owed to different people involved in the research.',
         'You may refer to ethical codes, but apply them to the situation described.',
         'Consider the ethics of publication as well as of the fieldwork itself.',
         'Suggest how the anthropologist might respond to the dilemmas you identify.']


def _q(rng, frame, pool):
    return frame + ' ' + rng.choice(pool)


ORIG = 'Original ethnographic extract written for this question bank (fictional composite)'


def _text_block(x):
    return f'Read the text below.\n\n{x[0]}\n— {ORIG}: {x[1]}.'


THEORY = {'douglas', 'levistrauss', 'radcliffe', 'morgan', 'ortner', 'auge', 'bowker', 'seeingstate', 'boas', 'wolf',
          'miner', 'barthethnic', 'dirks', 'dumont', 'bourdieu'}


def kind(e):
    return 'anthropological text' if e in THEORY else 'ethnography'


def _eth_pairs(X):
    out = []
    for e in X['eths']:
        own = [c for c in E[e]['c'] if c in X['concepts']]
        out += [(e, c) for c in (own or list(E[e]['c']))]
    return out


def sca_templates(X: dict) -> list:
    topic, ext, eths, concepts = X['topic'], X['ext'], X['eths'], X['concepts']
    out = []
    pairs = _eth_pairs(X)

    def pick(rng, pool):
        # skill/method subtopics: drop stems that embed the subtopic phrase as if it were a social process
        if X.get('generic'):
            pool = [p for p in pool if topic not in p]
        return rng.choice(pool)

    # ---- Paper 2 Section B (a) style: one ethnography and one concept -------------------------
    if pairs:
        def eth_concept(rng, slot):
            e, c = rng.choice(pairs)
            d = E[e]
            m = slot.marks or (3 if slot.d <= 2 else 4 if slot.d == 3 else 5)
            cl = CL[c]
            stem = pick(rng, [
                f'With reference to {d["cite"]}, explain how the key concept of {cl} helps us to understand {topic}.',
                f'Using {d["short"]} ({d["where"]}) as your example, describe how {cl} is shown.',
                f'Explain how {d["short"]} illustrates the concept of {cl}. Refer to the people, place and time of the ethnography.',
                f'Outline how {cl} shapes {topic}, using evidence from {d["short"]}.',
                f'With reference to one {kind(e)} you have studied, for example {d["short"]}, explain the relevance of {cl} to {topic}.',
                f'Identify one way in which {cl} matters in {d["short"]} ({d["where"]}) and explain its significance.',
            ])
            ans = d['c'][c]
            return dict(stem=stem, answer=ans, type='case', marks=m, minutes=float(2.5 * m),
                        markingKey=(f'Indicative content: {ans} Award up to [{m}]: 1 mark for accurate ethnographic context '
                                    f'({d["cite"]}, {d["where"]}); further marks for specific ethnographic detail and an explicit, '
                                    f'developed link to {cl}. Credit another accurate ethnography if the question allows it.'),
                        gap='G3')
        out.append(T('C3', (2, 4), eth_concept, 'case', 'p2_a', 'eth_concept'))

    # ---- Paper 2 Section B (b) style: two ethnographies -----------------------------------------
    two = [(a, b, c) for i, a in enumerate(eths) for b in eths[i + 1:] for c in E[a]['c'] if c in E[b]['c']]
    if not two and len(eths) >= 2:
        two = [(eths[0], eths[1], None)]
    if two:
        def eth_compare(rng, slot):
            a, b, c = rng.choice(two)
            A, B = E[a], E[b]
            if rng.random() < 0.5:
                A, B = B, A
            m = slot.marks or (10 if slot.d <= 4 else 15)
            if c:
                cl = CL[c]
                sa, sb = A['c'][c], B['c'][c]
            else:
                cl = CL[concepts[0]]
                sa, sb = next(iter(A['c'].values())), next(iter(B['c'].values()))
            stem = pick(rng, [
                f'Compare and contrast how {cl} is shown in {A["cite"]} and {B["cite"]}.',
                f'With reference to two anthropological studies, such as {A["short"]} and {B["short"]}, compare and contrast the role of {cl} in {topic}.',
                f'Compare and contrast {A["short"]} and {B["short"]} as accounts of {topic}, focusing on the key concept of {cl}.',
                f'"{cl[0].upper() + cl[1:]} is central to understanding {topic}." Compare and contrast two anthropological studies, for example {A["short"]} and {B["short"]}, in the light of this claim.',
                f'Using {A["short"]} and {B["short"]}, compare the ways in which {cl} is experienced and contested by the people studied.',
            ])
            ans = (f'{A["short"]} ({A["where"]}): {sa} {B["short"]} ({B["where"]}): {sb} '
                   f'Similarities and differences should be made explicit, e.g. how far {cl} is imposed by wider structures or '
                   f'negotiated by the people themselves in each context, and how the methods and theoretical approach of each '
                   f'ethnographer shape the account.')
            return dict(stem=stem, answer=ans, type='long', marks=m, minutes=float(min(60, 2.5 * m)),
                        markingKey=f'Indicative content: {ans} {bands(m, COMPARE_BANDS)}', gap='G5')
        out.append(T('C4', (3, 5), eth_compare, 'long', 'p2_b', 'eth_compare'))

    # ---- Paper 1 on original extracts ----------------------------------------------------------
    if ext:
        def describe(rng, slot):
            x = rng.choice(ext)
            m = slot.marks or (3 if slot.d <= 1 else 4)
            q = rng.choice([
                f'Describe {x[2]}, as presented in the text.',
                f'Using evidence from the text, describe {x[2]}.',
                f'Identify and describe {x[2]}. Refer closely to the text.',
                f'Outline what the text reveals about {x[2]}.',
                f'Describe, with examples from the text, {x[2]}.',
            ])
            q = _q(rng, q, G_DESC)
            return dict(stem=_text_block(x) + '\n\n' + q, answer=x[3], type='case', marks=m, minutes=float(2.5 * m),
                        markingKey=(f'{x[3]} Award 1 mark per relevant descriptive point supported by the text (or 2 for a point '
                                    f'developed with a quotation or specific detail), up to [{m}]. Description only is required; '
                                    f'do not credit outside ethnography in this question.'), gap='G7')
        out.append(T('C3', (1, 3), describe, 'case', 'p1_describe', 'p1_describe'))

        def explain(rng, slot):
            x = rng.choice(ext)
            m = slot.marks or (4 if slot.d <= 2 else 6)
            cl = CL[x[6]]
            q = rng.choice([
                f'Explain {x[4]}, using one or more anthropological concepts.',
                f'Analyse {x[4]}. Support your answer with evidence from the text.',
                f'Using the key concept of {cl}, explain {x[4]}.',
                f'With reference to the concept of {cl}, analyse {x[4]}.',
                f'Explain, with close reference to the text, {x[4]}.',
            ])
            q = _q(rng, q, G_EXPL)
            return dict(stem=_text_block(x) + '\n\n' + q, answer=x[5], type='case', marks=m, minutes=float(2.5 * m),
                        markingKey=f'Indicative content: {x[5]} {bands(m, P1Q2_BANDS)}', gap='G7')
        out.append(T(('C3', 'C4'), (2, 4), explain, 'case', 'p1_explain', 'p1_explain'))

        def compare(rng, slot):
            x = rng.choice(ext)
            c = x[6]
            cands = [e for e in eths if c in E[e]['c'] and e not in THEORY]
            if len(cands) < 2:
                cands += [e for e in E if c in E[e]['c'] and e not in cands and e not in THEORY][:4 - len(cands)]
            e = rng.choice(cands)
            d = E[e]
            m = slot.marks or 10
            cl = CL[c]
            q = rng.choice([
                f'Compare and contrast the role of {cl} in the text with {cl} in one ethnography you have studied, such as {d["short"]}.',
                f'Compare and contrast how {cl} is experienced by the people in the text and by the people in one other ethnography you have studied (for example {d["cite"]}).',
                f'Compare the significance of {cl} in the text with its significance in {d["short"]}. Refer explicitly to the ethnographic context of both.',
                f'With reference to {cl}, compare and contrast the text with one ethnography you have studied. You might choose {d["short"]}.',
            ])
            q = _q(rng, q, G_COMP)
            ans = (f'Text: {x[5]} Ethnography – {d["cite"]}, {d["where"]}: {d["c"][c]} Comparison: similarities and differences '
                   f'in how {cl} is produced, expressed or contested in the two settings, with explicit links between them.')
            return dict(stem=_text_block(x) + '\n\n' + q, answer=ans, type='long', marks=m, minutes=float(min(60, 3 * m)),
                        markingKey=(f'Indicative content: {ans} Any well-contextualised ethnography is acceptable. '
                                    f'{bands(m, COMPARE_BANDS)}'), gap='G5')
        out.append(T('C4', (3, 5), compare, 'long', 'p1_compare', 'p1_compare'))

        def ethics(rng, slot):
            x = rng.choice(ext)
            m = slot.marks or 10
            q = rng.choice([
                'Discuss the ethical issues an anthropologist would need to consider when carrying out the fieldwork described in the text.',
                'Evaluate the ethical challenges of researching, writing and publishing an account such as the one in the text.',
                'With reference to the text and to professional guidelines such as the AAA Principles of Professional Responsibility, discuss the ethical responsibilities of the anthropologist.',
                'To what extent could the research described in the text be carried out ethically? Refer to informed consent, harm and representation.',
            ])
            q = _q(rng, q, G_ETH)
            ans = (f'{x[7]} General principles: informed and ongoing consent; do no harm; anonymity and confidentiality '
                   f'(pseudonyms, protecting data); weighing obligations to participants, funders and the public; '
                   f'reflexivity about the researcher\'s power and representation of people.')
            return dict(stem=_text_block(x) + '\n\n' + q, answer=ans, type='long', marks=m, minutes=float(min(60, 3 * m)),
                        markingKey=f'Indicative content: {ans} {bands(m, ETHICS_BANDS)}', gap='G5')
        out.append(T('C4', (3, 5), ethics, 'long', 'ethics', 'ethics'))

    # ---- HL big question ------------------------------------------------------------------------
    if pairs:
        def big(rng, slot):
            e, c = rng.choice(pairs)
            d = E[e]
            bq = rng.choice(BIGQ[c] + BIGQ_ANY)
            m = slot.marks or 10
            cl = CL[c]
            stem = pick(rng, [
                f'Big question: "{bq}" Discuss with reference to the key concept of {cl} and at least one {kind(e)} you have studied, such as {d["short"]}.',
                f'Respond to the big question "{bq}" by drawing on {topic}, the concept of {cl} and {d["cite"]} or another {kind(e)}.',
                f'"{bq}" With reference to {d["short"]} and the key concept of {cl}, evaluate possible answers to this question.',
            ])
            ans = (f'A strong answer takes a position on the big question, applies {cl} explicitly and uses ethnography: {d["c"][c]} '
                   f'It weighs a contrasting perspective (another ethnography or theory) and reaches a reasoned conclusion.')
            return dict(stem=stem, answer=ans, type='long', marks=m, minutes=float(min(60, 3 * m)),
                        markingKey=f'Indicative content: {ans} {bands(m, BIG_BANDS)}', gap='G5')
        out.append(T('C4', (4, 5), big, 'long', 'big', 'big'))

    # ---- Paper 2 Section A essays ---------------------------------------------------------------
    if X['ev'] or X['essays']:
        def essay(rng, slot):
            m = slot.marks or 15
            pool = [('E', e) for e in X['essays']] + [('V', e) for e in X['ev']]
            kind, e = rng.choice(pool)
            if kind == 'E':
                stem, pts, judge = e
                pts = list(pts)
            else:
                claim, pro, con, judge = e
                pts = list(pro) + list(con)
                stem = rng.choice([
                    f'"{claim}" Discuss with reference to at least one ethnography you have studied.',
                    f'To what extent do you agree that {lc_claim(claim).rstrip(".")}? Answer with reference to one ethnography in depth.',
                    f'Evaluate the claim that {lc_claim(claim)} Support your answer with ethnographic material and anthropological theory.',
                ])
            sug = ', '.join(E[k]['short'] for k in eths[:3])
            key = (f'Indicative content: {"; ".join(pts)}. Suitable ethnographies include {sug}. A strong answer reaches a judgement '
                   f'such as: {judge} {bands(m, ESSAY_BANDS)}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=m, minutes=float(min(60, 3 * m)), gap='G5')
        out.append(T('C4', (3, 5), essay, 'long', 'essay', 'essay'))
    return out


P = Pack()


def init(subject_id):
    pass


def templates(st):
    return P.templates(st)


# =============================================================================================
# Ethnography catalogue
# =============================================================================================
eth('malinowski', 'Bronisław Malinowski, Argonauts of the Western Pacific (1922)', "Malinowski's Argonauts of the Western Pacific",
    'among the Trobriand Islanders of Papua New Guinea (fieldwork 1915–1918)',
    social_relations='In the kula ring, men on different islands keep lifelong partnerships through the ceremonial exchange of shell valuables: soulava necklaces travel clockwise and mwali armshells anticlockwise, creating alliances between communities rather than profit.',
    materiality='Kula valuables are rarely worn or used; their value lies in their histories and the names of past holders, so objects carry social biographies and prestige rather than utility.',
    power='Holding famous kula valuables and keeping many partners brings renown; chiefs and successful kula men gain status through generosity, so prestige rather than accumulation underpins influence.',
    culture='Malinowski argued that institutions such as the kula and garden magic meet social and psychological needs, and insisted on grasping "the native\'s point of view" through long-term participant observation.')
eth('weiner', 'Annette Weiner, Women of Value, Men of Renown: New Perspectives in Trobriand Exchange (1976)', "Weiner's Women of Value, Men of Renown",
    'in Kiriwina, Trobriand Islands, revisiting Malinowski\'s field site in the 1970s',
    power='Weiner showed that women\'s wealth – bundles of banana leaves and fibre skirts distributed at mortuary ceremonies (sagali) – gives Trobriand women public power that Malinowski had largely overlooked.',
    materiality='Banana-leaf bundles have little use value but are essential in mortuary exchanges that restore the dead person\'s matrilineal (dala) identity, so humble objects carry cosmological value.',
    identity='Through mortuary distributions women reproduce the identity of the matrilineage, so female identity is bound up with regenerating the dala across generations.',
    change='Her restudy shows how anthropological knowledge changes: a male ethnographer\'s access shaped what was recorded, and a later female ethnographer revealed women\'s exchange.')
eth('mead', 'Margaret Mead, Coming of Age in Samoa (1928)', "Mead's Coming of Age in Samoa",
    'among adolescent girls on Ta\'ū in the Manu\'a Islands of American Samoa (fieldwork 1925–1926)',
    culture='Mead argued that adolescence in Samoa was relatively free of the stress seen in the United States, supporting Boas\'s view that culture rather than biology shapes development; Derek Freeman\'s 1983 critique disputed her findings.',
    identity='Mead described girls\' identities as shaped by communal child-rearing and relaxed attitudes to sexuality, which she contrasted with the conflicts of American adolescence.',
    change='Mead used Samoa as a mirror to argue that American child-rearing and sexual norms could be changed, presenting ethnography as cultural critique of her own society.')
eth('geertz', 'Clifford Geertz, "Deep Play: Notes on the Balinese Cockfight" (1972; reprinted in The Interpretation of Cultures, 1973)', 'Geertz\'s "Deep Play"',
    'in a Balinese village (fieldwork with Hildred Geertz, 1958)',
    culture='Geertz read the cockfight as a text – "a story they tell themselves about themselves" – to be interpreted through thick description of its layered meanings.',
    power='In "deep" matches between high-status men the money matters less than the status symbolically at stake, so the cockfight dramatises the village status hierarchy without actually changing it.',
    identity='Men identify closely with their cocks, and the Balinese word for cock is used metaphorically for heroes, champions and ladies\' men, so the fights express masculine identity and rivalry.',
    social_relations='Men bet on the cocks of their own kin group or village and never against them, so patterns of betting map kinship, alliance and rivalry.')
eth('bourgois', 'Philippe Bourgois, In Search of Respect: Selling Crack in El Barrio (1995)', "Bourgois's In Search of Respect",
    'among Puerto Rican crack dealers in East Harlem, New York (fieldwork 1985–1990)',
    power='Bourgois links street violence and drug dealing to structural forces: the loss of factory jobs, racism, and the humiliation dealers felt in service-sector office jobs.',
    identity='Dealers built a "street culture" of resistance in which they sought the respect and dignity denied to them in mainstream work, yet that culture also drew them into self-destruction and violence.',
    change='New York\'s shift from a manufacturing to a service economy left young Puerto Rican men without the jobs that had sustained their parents, unsettling masculine roles and family life.',
    social_relations='As women entered wage work while men lost status, gender relations were renegotiated, and Bourgois documents how this contributed to domestic conflict and violence.')
eth('scheper', 'Nancy Scheper-Hughes, Death without Weeping: The Violence of Everyday Life in Brazil (1992)', "Scheper-Hughes's Death without Weeping",
    'among shantytown women of the Alto do Cruzeiro, Bom Jesus da Mata, north-east Brazil (fieldwork 1960s–1980s)',
    power='She describes the "everyday violence" of poverty, in which hunger is medicalised as nervos and treated with tranquillisers and vitamins, hiding the political causes of suffering.',
    social_relations='Facing very high infant mortality, some mothers delayed emotional attachment to babies judged weak and let them die "without weeping" – a contested argument about how scarcity shapes maternal love.',
    materiality='The hungry body becomes the site where inequality is felt: nervos expresses the weakness, trembling and anger produced by sugar-cane labour and malnutrition.',
    culture='She argues that mother love is not a universal instinct but is shaped by economic and demographic conditions, challenging Western assumptions about motherhood.')
eth('abulughod', 'Lila Abu-Lughod, Veiled Sentiments: Honor and Poetry in a Bedouin Society (1986)', "Abu-Lughod's Veiled Sentiments",
    'among the Awlad \'Ali Bedouin of Egypt\'s Western Desert (fieldwork from 1978)',
    identity='Honour and modesty (hasham) define ideal personhood; in public people present themselves as autonomous and invulnerable, especially before those of higher status.',
    power='Women and young men – those with less power – express love, loss and vulnerability through short ghinnawa poems, a socially acceptable channel for sentiments that would breach the honour code if spoken directly.',
    culture='Two discourses coexist – the code of honour and the poetic discourse of vulnerability – showing that a culture is not one seamless system but contains tensions.',
    social_relations='Abu-Lughod was received as a dutiful "daughter" in her host household, and her gender and partly Arab background shaped which relationships and sentiments she could access.')
eth('ong', 'Aihwa Ong, Spirits of Resistance and Capitalist Discipline: Factory Women in Malaysia (1987)', "Ong's Spirits of Resistance and Capitalist Discipline",
    'among young Malay women working in Japanese-owned electronics factories in Kuala Langat, Selangor, Malaysia (late 1970s)',
    power='Episodes of spirit possession on the shop floor halted production; Ong interprets them as protest against the strict time discipline and male supervision of factory work.',
    change='Industrialisation drew rural Malay daughters into wage work, changing family relations and provoking moral panic about "factory girls" as well as Islamic revivalist responses.',
    identity='Factory women negotiated identities between village (kampung) norms, consumer modernity and religious expectations of modesty.',
    space='Factories imposed clock time and spatial control – bounded workstations, microscopes, supervisors – that clashed with the rhythms of village life.')
eth('ongflex', 'Aihwa Ong, Flexible Citizenship: The Cultural Logics of Transnationality (1999)', "Ong's Flexible Citizenship",
    'among wealthy Chinese business families moving between Hong Kong, South-East Asia and North America (1990s)',
    belonging='Elite families accumulate passports and homes in several countries, treating citizenship as a flexible strategy rather than exclusive loyalty to one nation.',
    power='States court wealthy migrants with investor visas while restricting poorer ones, so the ability to move and belong is unequally distributed.',
    space='"Astronaut" fathers commute across the Pacific while "parachute kids" study abroad, stretching family life across space.',
    identity='Chinese identities are reworked transnationally as family business networks and education strategies cross borders.')
eth('holmes', 'Seth M. Holmes, Fresh Fruit, Broken Bodies: Migrant Farmworkers in the United States (2013)', "Holmes's Fresh Fruit, Broken Bodies",
    'with Triqui Indigenous migrants from Oaxaca, Mexico, on berry farms in Washington State and in California (fieldwork 2003–2005)',
    classification='Farm labour is organised in an ethnic-citizenship hierarchy: white and Asian American owners, then mestizo Mexican supervisors, with undocumented Triqui pickers at the bottom doing the most physically damaging work.',
    power='Holmes uses Bourdieu\'s idea of symbolic violence to show how this hierarchy is naturalised: supervisors, doctors and sometimes workers themselves explain Triqui suffering by their bodies or culture rather than by labour conditions.',
    space='Holmes crossed the US–Mexico border with Triqui companions and was detained by the Border Patrol, showing how the border distributes risk unequally between bodies.',
    materiality='Picking berries while bent over for hours damages backs and knees, so the body records structural inequality as chronic pain and injury.')
eth('kleinman', 'Arthur Kleinman, Patients and Healers in the Context of Culture (1980)', "Kleinman's Patients and Healers in the Context of Culture",
    'among patients, families, shamans (tâng-ki) and doctors in Taiwan (fieldwork 1969–1978)',
    culture='Kleinman distinguishes disease (biological malfunction) from illness (the lived experience of sickness), and shows that patients and practitioners hold different explanatory models of cause, course and treatment.',
    classification='He divides the health care system into popular, folk and professional sectors; most episodes of sickness are managed in the popular sector of family and community.',
    power='When explanatory models clash, biomedical practitioners often discount patients\' models, which affects trust, adherence and satisfaction.',
    social_relations='Healing is a social process: families negotiate which practitioner to consult and how to interpret symptoms.')
eth('farmer', 'Paul Farmer, AIDS and Accusation: Haiti and the Geography of Blame (1992)', "Farmer's AIDS and Accusation",
    'in Do Kay, a village in rural central Haiti settled by people displaced by the Péligre hydroelectric dam',
    power='Farmer argues that HIV spread in Haiti along lines of structural violence – poverty, loss of land to the Péligre dam, gender inequality and US economic dominance – not because of "risky culture".',
    classification='In 1983 the US Centers for Disease Control listed Haitians among AIDS "risk groups", a classification that stigmatised Haitians and blamed them for the epidemic.',
    change='Villagers\' explanations of AIDS shifted over time, from sorcery accusations towards accounts linking the disease to poverty and exploitation.',
    space='A "geography of blame" linked Haiti and the United States: the epidemic moved along routes of migration, tourism and economic dependence, yet blame flowed towards the poorer country.')
eth('douglas', 'Mary Douglas, Purity and Danger (1966)', "Douglas's Purity and Danger",
    'drawing on her fieldwork among the Lele of the Kasai (Democratic Republic of the Congo) and on the dietary rules of Leviticus',
    classification='Douglas argued that dirt is "matter out of place": ideas of pollution arise wherever a system of classification produces anomalies that do not fit its categories.',
    culture='She explained the abominations of Leviticus by the logic of classification rather than hygiene: the pig, for example, has a cloven hoof but does not chew the cud, so it breaks the category of clean livestock.',
    society='Douglas treated the body as a symbol of society: anxieties about bodily margins and orifices mirror anxieties about the boundaries of the group.',
    power='Pollution beliefs uphold moral and social order, since danger is attributed to those who cross boundaries; among the Lele, the anomalous pangolin was avoided by most but eaten in a special initiates\' cult.')
eth('dumont', 'Louis Dumont, Homo Hierarchicus: The Caste System and Its Implications (1966; English 1970)', "Dumont's Homo Hierarchicus",
    'drawing on Indian textual sources and his fieldwork among the Pramalai Kallar of Tamil Nadu',
    classification='Dumont argued that caste rests on a single ideological opposition between the pure and the impure, with Brahmins at the top and "Untouchable" castes at the bottom.',
    power='For Dumont religious status encompasses political and economic power, so a king could be wealthier and more powerful than a Brahmin yet lower in ritual rank.',
    society='He contrasted hierarchical Indian society (homo hierarchicus) with Western societies built on individualism and equality (homo aequalis).')
eth('dirks', 'Nicholas B. Dirks, Castes of Mind: Colonialism and the Making of Modern India (2001)', "Dirks's Castes of Mind",
    'a historical anthropology of British colonial rule in India',
    classification='Dirks argued that caste as a rigid, all-India system was substantially shaped by colonial rule, through censuses (from 1871–1872), ethnographic surveys and legal codes that fixed and ranked castes.',
    power='Colonial knowledge was a technology of rule: classifying Indians by caste helped the state govern, recruit and control, and placed Brahmanical ideals at the centre.',
    change='Fluid, politically negotiated pre-colonial identities hardened as communities petitioned census officials for higher rank.')
eth('srinivas', 'M. N. Srinivas, Religion and Society among the Coorgs of South India (1952) and later essays on caste', "Srinivas's work on Sanskritisation and the dominant caste",
    'among the Coorgs (Kodavas) of Karnataka and in the village of Rampura, Mysore (fieldwork 1940s–1950s)',
    change='Srinivas coined "Sanskritisation" for the process by which lower castes raise their status by adopting the rituals, diet and customs of higher castes, showing that caste ranking can change.',
    power='His concept of the "dominant caste" showed that numerical strength, land ownership and political power, not only ritual purity, determine a caste\'s position in a village.',
    classification='Caste in practice is a system of many local jatis whose relative ranks are disputed, rather than the four fixed varnas of Hindu texts.')
eth('bowker', 'Geoffrey Bowker and Susan Leigh Star, Sorting Things Out: Classification and Its Consequences (1999)', "Bowker and Star's Sorting Things Out",
    'on classification systems such as the International Classification of Diseases and apartheid South Africa\'s race classification',
    classification='Bowker and Star show that every classification system valorises some points of view and silences others, and that categories become invisible infrastructure once established.',
    power='Under apartheid, the Population Registration Act (1950) assigned every person a race, and reclassification decisions determined where people could live, work and marry.',
    identity='People "torque" between categories: their lives are twisted when an official category does not fit their biography, as with families split by apartheid reclassification.')
eth('seeingstate', 'James C. Scott, Seeing Like a State: How Certain Schemes to Improve the Human Condition Have Failed (1998)', "Scott's Seeing Like a State",
    'a comparative study of state schemes such as scientific forestry, permanent surnames, villagisation in Tanzania and Brasília',
    classification='Scott argues that states simplify complex local realities into standardised, "legible" categories – surnames, cadastral maps, censuses – in order to tax, conscript and govern.',
    power='High-modernist schemes imposed from above, such as compulsory villagisation in Tanzania in the 1970s, often failed because they ignored local practical knowledge (mētis).',
    change='Making populations legible transformed how people were named, where they lived and how land was owned.')
eth('azande', 'E. E. Evans-Pritchard, Witchcraft, Oracles and Magic among the Azande (1937)', "Evans-Pritchard's Witchcraft, Oracles and Magic among the Azande",
    'among the Azande of the southern Sudan (fieldwork 1926–1930)',
    culture='Witchcraft explains the particular misfortune: Azande know that termites ate the supports of a granary, but witchcraft explains why it collapsed when particular people were sitting beneath it.',
    social_relations='Witchcraft accusations follow tensions between neighbours and rivals, and consulting the poison oracle (benge) channels conflict into a recognised procedure.',
    power='The verdicts of princes\' poison oracles were final, so control over divination supported political authority.')
eth('nuer', 'E. E. Evans-Pritchard, The Nuer (1940)', "Evans-Pritchard's The Nuer",
    'among Nuer cattle pastoralists of the Upper Nile, southern Sudan (fieldwork 1930–1936)',
    space='Nuer "oecological time" follows seasonal movement between wet-season villages and dry-season cattle camps, while "structural time" is reckoned by distances between age-sets and lineages.',
    social_relations='Political order rested on segmentary lineages that united against more distant groups and divided when conflict arose within, giving order without a state.',
    power='The research was requested by the Anglo-Egyptian Sudan government after Nuer resistance to colonial rule, raising questions about anthropology\'s colonial uses.',
    materiality='Cattle are central to Nuer life – the medium of bridewealth, sacrifice and personal names – so material goods carry social and spiritual value.')
eth('boas', 'Franz Boas\'s historical particularism (e.g. "The Limitations of the Comparative Method of Anthropology", 1896)', "Boas's historical particularism",
    'in his work on the Kwakwaka\'wakw of British Columbia and on immigrants in New York',
    culture='Boas argued that each culture is the product of its own history and must be understood in its own terms (historical particularism), rejecting rankings of cultures as "savage" or "civilised".',
    classification='His study of immigrants\' children showed head shape changing within one generation in the United States, challenging fixed racial classifications.',
    materiality='He argued that museum objects should be displayed by people and culture area, not by evolutionary stage, because artefacts make sense only in their cultural context.')
eth('radcliffe', 'A. R. Radcliffe-Brown, The Andaman Islanders (1922) and Structure and Function in Primitive Society (1952)', "Radcliffe-Brown's structural-functionalism",
    'drawing on fieldwork in the Andaman Islands (1906–1908) and comparative work on African and Australian kinship',
    society='Radcliffe-Brown compared society to an organism: institutions such as ritual and law function to maintain the social structure as a whole.',
    social_relations='In "The Mother\'s Brother in South Africa" (1924) he explained joking and respect relationships by the structural positions of kin rather than by historical survivals.',
    culture='In The Andaman Islanders he argued that ceremonies express and transmit the collective sentiments on which social cohesion depends.')
eth('morgan', 'Lewis Henry Morgan, Ancient Society (1877)', "Morgan's Ancient Society",
    'drawing on his work with the Haudenosaunee (Iroquois) and a worldwide survey of kinship terms',
    classification='Morgan classified societies into stages of savagery, barbarism and civilisation, each marked by an invention such as pottery, the bow or phonetic writing.',
    social_relations='In Systems of Consanguinity and Affinity of the Human Family (1871) he compared kinship terminologies worldwide, founding the comparative study of kinship.',
    change='He assumed all societies pass through the same sequence of stages, an idea later adopted by Marx and Engels.')
eth('levistrauss', 'Claude Lévi-Strauss, The Elementary Structures of Kinship (1949) and The Raw and the Cooked (1964)', "Lévi-Strauss's structuralism",
    'in comparative analyses of kinship and of Amerindian myths from South America',
    culture='Lévi-Strauss argued that the human mind orders the world through binary oppositions such as raw/cooked and nature/culture, and that myths work through these oppositions.',
    social_relations='In alliance theory, the incest taboo forces groups to exchange women in marriage, creating bonds between groups; the taboo marks the passage from nature to culture.',
    classification='Totemic classifications show that natural species are chosen not only because they are "good to eat" but because they are "good to think" with.')
eth('bourdieu', 'Pierre Bourdieu, Outline of a Theory of Practice (1972; English 1977)', "Bourdieu's Outline of a Theory of Practice",
    'based on fieldwork among the Kabyle of Algeria (1950s–1960s)',
    power='Bourdieu showed how domination is reproduced through habitus – embodied dispositions that make inequality feel natural (doxa) – and through symbolic capital such as honour.',
    space='The Kabyle house is organised by oppositions (male/female, light/dark, high/low), so moving through domestic space inscribes the gender order in the body.',
    social_relations='Gift exchange depends on a time interval between gift and counter-gift, which disguises self-interest and turns exchange into honour and obligation.')
eth('ortner', 'Sherry Ortner, "Is Female to Male as Nature Is to Culture?" (Feminist Studies, 1972; reprinted 1974 in Woman, Culture, and Society)', 'Ortner\'s essay "Is Female to Male as Nature Is to Culture?"',
    'in a comparative feminist analysis of gender symbolism across societies',
    power='Ortner argued that the widespread lower valuation of women is linked to their symbolic association with nature, while men are associated with culture, which is valued as transcending nature.',
    identity='Gender identity is a cultural construction: nothing in biology dictates women\'s lower status; the nature/culture association is symbolic and could change.')
eth('wolf', 'Eric Wolf, Europe and the People Without History (1982)', "Wolf's Europe and the People Without History",
    'in a Marxist historical anthropology of global capitalism from 1400 to 1900',
    power='Wolf showed that supposedly isolated "tribal" peoples were drawn into the fur trade, the slave trade and plantation economies, so their cultures were shaped by unequal relations of global capitalism.',
    change='He rejected the image of timeless "people without history", insisting that all societies have been transformed by connections with others.',
    society='Wolf criticised treating societies as bounded "billiard balls", proposing instead to analyse webs of interconnection and modes of production.')
eth('miner', 'Horace Miner, "Body Ritual among the Nacirema" (1956)', 'Miner\'s "Body Ritual among the Nacirema"',
    'in a satirical article in American Anthropologist describing everyday American hygiene as exotic ritual',
    culture='By describing Americans ("Nacirema" is American spelled backwards) brushing teeth and visiting doctors as magical rites, Miner showed how ethnographic language can make the familiar strange.',
    classification='The article exposes how labelling other people\'s practices "magic" and one\'s own "science" reflects ethnocentric classification.')
eth('rosaldo', 'Renato Rosaldo, "Grief and a Headhunter\'s Rage" (1989, in Culture and Truth)', 'Rosaldo\'s "Grief and a Headhunter\'s Rage"',
    'among the Ilongot of northern Luzon, the Philippines (fieldwork 1967–1969 and 1974)',
    identity='Rosaldo only grasped older Ilongot men\'s statement that the rage born of grief drove headhunting after the accidental death of his wife, Michelle Rosaldo, in 1981 – showing how the ethnographer\'s positioned experience shapes understanding.',
    culture='He argued that the force of emotion is missed when ritual is treated only as a code to be decoded; the ethnographer must be positioned to grasp it.')
eth('briggs', 'Jean Briggs, Never in Anger: Portrait of an Eskimo Family (1970)', "Briggs's Never in Anger",
    'with an Utku Inuit family at Chantrey Inlet in the Canadian Arctic (fieldwork 1963–1965)',
    social_relations='Briggs lived as an adopted daughter in an Utku household; after she spoke angrily to visiting white fishermen who wanted to borrow the Utku canoe, she was quietly ostracised for months.',
    culture='Utku adults valued emotional restraint; displays of anger were seen as dangerous and childish and were carefully controlled.',
    identity='Her outburst revealed her as an outsider who did not share the Utku emotional code, showing how fieldwork mistakes can produce insight into culture and positionality.')
eth('basso', 'Keith Basso, Wisdom Sits in Places: Landscape and Language among the Western Apache (1996)', "Basso's Wisdom Sits in Places",
    'among the Western Apache of Cibecue, Arizona',
    space='Western Apache place-names recall ancestral events and make the landscape a store of moral stories; places "stalk" people by reminding them of right conduct.',
    identity='Speaking place-names and their stories ties personal morality and Apache identity to particular locations.',
    belonging='Knowing the names and stories of the land is part of belonging to the community and links people across generations.')
eth('miller', 'Daniel Miller, A Theory of Shopping (1998) and The Comfort of Things (2008)', "Miller's studies of shopping and household objects",
    'among households on streets in North London',
    materiality='Miller argued that everyday shopping is largely an act of love and sacrifice for family members, and that the objects people keep at home express and sustain their relationships.',
    social_relations='Routine purchases – a partner\'s preferred food, children\'s clothes – are ways of making and maintaining relationships rather than simply individual consumption.',
    identity='Through the arrangement of their possessions households create an order or "aesthetic" that expresses who they are.')
eth('whywepost', 'Daniel Miller and colleagues, How the World Changed Social Media (Why We Post project, 2016)', 'the Why We Post project',
    'in a comparative digital ethnography by nine anthropologists in nine field sites, including Brazil, Chile, England, India, Italy, Trinidad, Turkey and two sites in China',
    materiality='Social media are treated as places where people live, not just technologies, and what people post varies sharply from site to site.',
    change='Rather than social media changing people everywhere in the same way, people changed social media to fit local norms – the "attainment" of each site\'s values.',
    social_relations='Social media mostly extend existing relationships – such as ties with migrant kin – rather than creating entirely new ones.')
eth('boellstorff', 'Tom Boellstorff, Coming of Age in Second Life: An Anthropologist Explores the Virtually Human (2008)', "Boellstorff's Coming of Age in Second Life",
    'through participant observation inside the virtual world Second Life, conducted via his avatar (2004–2006)',
    identity='Residents created avatars and virtual selves, showing identity to be crafted and performed in virtual space.',
    space='Second Life is treated as a real place of social life, with its own norms, property and events, so place need not be physical.',
    social_relations='Friendships, romances and communities formed between avatars, showing that virtual sociality is genuine sociality.')
eth('carsten', 'Janet Carsten, The Heat of the Hearth: The Process of Kinship in a Malay Fishing Community (1997)', "Carsten's The Heat of the Hearth",
    'on the island of Langkawi, Malaysia (fieldwork 1980s)',
    social_relations='Kinship is created by living together and sharing food, especially rice cooked on the same hearth, so people become kin through feeding and co-residence, not only through birth.',
    belonging='Fostered children and incoming spouses become relatives by eating together, so belonging to a house is a process.',
    space='The house and its hearth are the centre of kinship; relatedness is produced in domestic space.')
eth('weston', 'Kath Weston, Families We Choose: Lesbians, Gays, Kinship (1991)', "Weston's Families We Choose",
    'among lesbians and gay men in the San Francisco Bay Area (fieldwork 1985–1986)',
    social_relations='"Chosen families" of friends, lovers and ex-lovers gave support often denied by biological families after coming out, defining kinship through love and commitment.',
    belonging='Belonging rested on choice and care rather than blood, challenging the assumption that "real" kinship is biological.',
    identity='Coming out could cost people their ties with biological kin, so sexual identity reshaped kinship.')
eth('gough', 'Kathleen Gough, "The Nayars and the Definition of Marriage" (1959)', "Gough's study of the Nayar",
    'on the Nayar of Kerala, south India, as they lived before twentieth-century legal reforms',
    social_relations='Nayar girls underwent a tali-tying rite before puberty; later they could take several visiting sambandham partners, while children belonged to their mother\'s matrilineal household (taravad).',
    change='Colonial-era laws and economic change in the late nineteenth and twentieth centuries broke up taravads and promoted conjugal, nuclear households.',
    classification='Gough used the Nayar case to propose a broader definition of marriage based on establishing the legitimacy of children rather than on co-residence of spouses.')
eth('sanday', 'Peggy Reeves Sanday, Women at the Center: Life in a Modern Matriarchy (2002)', "Sanday's Women at the Center",
    'among the Minangkabau of West Sumatra, Indonesia (fieldwork from 1981)',
    power='Sanday calls the Minangkabau a "matriarchy" in the sense that women are at the symbolic and social centre, controlling ancestral houses and land, without ruling over men.',
    social_relations='Houses, land and lineage pass through women; men traditionally migrate (merantau) and hold authority as mother\'s brothers (mamak) in their sisters\' lineage.',
    change='Matrilineal custom (adat) coexists and negotiates with Islam and Indonesian state law, showing adaptation rather than disappearance.')
eth('turner', 'Victor Turner, The Forest of Symbols (1967) and The Ritual Process (1969)', "Turner's studies of Ndembu ritual",
    'among the Ndembu of north-western Zambia (fieldwork 1950s)',
    belonging='In the liminal phase of rites of passage initiates are "betwixt and between" and experience communitas, an intense bond of equality and comradeship.',
    identity='Rites of passage transform social identity, as in the boys\' circumcision rite (mukanda) that turns boys into men.',
    culture='Dominant symbols such as the milk tree (mudyi) are multivocal, standing at once for breast milk, matriliny and the unity of Ndembu society.')
eth('malkki', 'Liisa Malkki, Purity and Exile: Violence, Memory, and National Cosmology among Hutu Refugees in Tanzania (1995)', "Malkki's Purity and Exile",
    'among Hutu refugees from Burundi who fled the 1972 killings, in Mishamo refugee camp and Kigoma township, Tanzania (fieldwork 1985–1986)',
    identity='Camp refugees constructed a "mythico-history" in which they were the true, pure Hutu nation in exile, while town refugees adopted fluid, cosmopolitan identities and avoided the refugee label.',
    space='The bounded, administered space of the camp encouraged a strong collective refugee identity, whereas dispersed town life encouraged assimilation.',
    belonging='Camp refugees saw exile as a moral trial and Burundi as the homeland to which they truly belonged; town refugees sought to belong locally.',
    power='Camp administration regulated movement and livelihoods, and refugees\' narratives of persecution were also a response to their marginal position.')
eth('levitt', 'Peggy Levitt, The Transnational Villagers (2001)', "Levitt's The Transnational Villagers",
    'among migrants from Miraflores, Dominican Republic, and their community in Jamaica Plain, Boston',
    change='"Social remittances" – ideas, behaviours and identities – flowed from Boston to Miraflores, changing gender roles, politics and religious practice in the village.',
    belonging='Migrants belonged to two places at once, joining village development and politics from Boston.',
    space='A transnational social field linked a Boston neighbourhood and a Dominican village so closely that life in each depended on the other.')
eth('scott', 'James C. Scott, Weapons of the Weak: Everyday Forms of Peasant Resistance (1985)', "Scott's Weapons of the Weak",
    'in "Sedaka", a pseudonymous rice-growing village in Kedah, Malaysia (fieldwork 1978–1980)',
    power='After double-cropping and combine harvesters cut work for poor villagers, they resisted through foot-dragging, gossip, pilfering and slander against rich farmers rather than open revolt.',
    change='Green Revolution mechanisation transformed village relations, eroding customary obligations of the rich to employ the poor and give them alms (zakat).',
    social_relations='Poor villagers used gossip and reputation to remind rich households of their moral obligations, contesting the meaning of generosity.')
eth('barth', 'Fredrik Barth, Nomads of South Persia: The Basseri Tribe of the Khamseh Confederacy (1961)', "Barth's Nomads of South Persia",
    'among Basseri pastoralists of Fars province, Iran (fieldwork 1958)',
    space='The Basseri migrate along a recognised route (il-rah) between winter pastures in the south and summer pastures in the mountains, with rights to use it at particular times.',
    power='The chief (khan) coordinated the migration and mediated between the tribe, the state and settled villagers.',
    change='Both the richest herders (who invested in land) and the poorest (who lost their flocks) tended to settle, so sedentarisation regulated the nomadic population.')
eth('barthethnic', 'Fredrik Barth (ed.), Ethnic Groups and Boundaries (1969)', "Barth's Ethnic Groups and Boundaries",
    'in a comparative theory of ethnicity',
    identity='Barth argued that ethnic identity is maintained by boundaries – processes of inclusion and exclusion – rather than by "the cultural stuff" a group contains.',
    classification='Ethnic categories persist even when people move across them and cultural traits change, because they rest on ascription by self and others.',
    belonging='Belonging to an ethnic group is signalled by selected markers (dress, language, lifestyle) used to separate "us" from "them".')
eth('vitebsky', 'Piers Vitebsky, The Reindeer People: Living with Animals and Spirits in Siberia (2005)', "Vitebsky's The Reindeer People",
    'among Eveny reindeer herders of Sebyan-Küöl, Sakha Republic (Yakutia), Siberia (fieldwork from 1988)',
    change='Soviet collectivisation turned herding into state-farm work and sent children to boarding schools, and the collapse of the USSR in 1991 brought economic crisis to the herders.',
    space='Herders move with their reindeer through taiga and mountains, a landscape understood as inhabited by spirits.',
    social_relations='Soviet policy separated men in the herding brigades from women in the village, changing gender and family relations.')
eth('hodgson', 'Dorothy Hodgson, Once Intrepid Warriors: Gender, Ethnicity, and the Cultural Politics of Maasai Development (2001)', "Hodgson's Once Intrepid Warriors",
    'among Maasai pastoralists in northern Tanzania',
    power='Colonial and post-colonial development projects treated Maasai men as owners of cattle, eroding women\'s rights over livestock and products such as milk.',
    identity='The image of Maasai as "intrepid warriors" was partly produced by colonial representation, and Maasai men and women reworked ethnicity and gender in response.',
    change='Development schemes, loss of land and market integration transformed pastoral livelihoods and gender relations.')
eth('deleon', 'Jason De León, The Land of Open Graves: Living and Dying on the Migrant Trail (2015)', "De León's The Land of Open Graves",
    'on the US–Mexico border in the Sonoran Desert, Arizona, through the Undocumented Migration Project',
    power='US "Prevention Through Deterrence" policy funnels migrants into remote desert, using the terrain as a weapon so that deaths appear natural rather than political.',
    materiality='De León combines archaeology, forensic science and ethnography, analysing discarded water bottles, backpacks and clothing as traces of migrants\' experience.',
    space='He describes the desert as a "hybrid collectif" of humans, animals, heat, terrain and policy that together produce migrant deaths.')
eth('auge', 'Marc Augé, Non-Places: Introduction to an Anthropology of Supermodernity (1992; English 1995)', "Augé's Non-Places",
    'in a theoretical essay on spaces of transit such as airports, motorways and supermarkets',
    space='Augé contrasts "anthropological places", which are relational, historical and concerned with identity, with the "non-places" of supermodernity through which people pass as solitary individuals.',
    identity='In non-places identity is reduced to that of passenger or customer, checked through tickets, passports and codes.')
eth('low', 'Setha Low, On the Plaza: The Politics of Public Space and Culture (2000)', "Low's On the Plaza",
    'on two plazas in San José, Costa Rica',
    space='Low shows that public space is both socially produced (by history, politics and design) and socially constructed (given meaning through everyday use).',
    power='The municipality\'s redesign of the Parque Central sparked conflict, as marginal users such as shoeshiners and pensioners were displaced or regulated.',
    belonging='Different groups claimed the plaza as their own, so who belongs in public space was continually negotiated.')
eth('herzfeld', 'Michael Herzfeld, A Place in History: Social and Monumental Time in a Cretan Town (1991)', "Herzfeld's A Place in History",
    'in the old town of Rethemnos (Rethymno), Crete',
    space='Residents of the historic quarter clashed with heritage conservation officials who controlled alterations to their old houses.',
    change='Herzfeld contrasts the "monumental time" of official heritage with the "social time" of residents\' everyday lives and memories.',
    power='The state used heritage to promote national history, restricting residents\' ability to adapt their own homes.')
eth('theidon', 'Kimberly Theidon, Intimate Enemies: Violence and Reconciliation in Peru (2013)', "Theidon's Intimate Enemies",
    'in Quechua-speaking highland communities of Ayacucho, Peru, after the 1980–2000 armed conflict with Shining Path',
    power='Because violence involved neighbours and kin, communities had to live alongside former perpetrators after the war.',
    social_relations='Communities negotiated the return of former Shining Path members through public confession, repentance and community justice.',
    change='Local, gendered practices of reconciliation developed alongside the national Truth and Reconciliation Commission (2001–2003).')
eth('das', 'Veena Das, Life and Words: Violence and the Descent into the Ordinary (2007)', "Das's Life and Words",
    'with survivors of the 1947 Partition of India and of the 1984 anti-Sikh violence in Delhi',
    power='Das shows how violence against women\'s bodies during Partition was bound up with the making of national and religious communities.',
    social_relations='Survivors rebuilt everyday life – a "descent into the ordinary" – through small acts of care rather than public testimony.')
eth('simpson', 'Audra Simpson, Mohawk Interruptus: Political Life Across the Borders of Settler States (2014)', "Simpson's Mohawk Interruptus",
    'in Kahnawà:ke, a Mohawk community near Montreal, Canada',
    power='Simpson describes a politics of "refusal": many Kahnawà:ke Mohawks refuse Canadian and US citizenship, travel on Haudenosaunee passports and assert sovereignty.',
    belonging='Community membership rules are debated as Mohawks decide who belongs in the face of colonial definitions imposed by the Indian Act.',
    identity='Simpson is herself from Kahnawà:ke and practises "ethnographic refusal", declining to publish some internal matters.')
eth('tsing', 'Anna Lowenhaupt Tsing, Friction: An Ethnography of Global Connection (2005)', "Tsing's Friction",
    'in the Meratus Mountains of South Kalimantan, Indonesia, and among Indonesian environmental activists',
    change='Global connections such as logging, environmentalism and investment produce "friction" – awkward, unequal encounters that generate new cultural forms.',
    power='Alliances between Meratus Dayak villagers, students and nature lovers challenged logging and plantation companies.',
    space='The rainforest was remade as a "frontier" of resource extraction, where rules were suspended and wealth seized.')
eth('ferguson', 'James Ferguson, The Anti-Politics Machine: "Development," Depoliticization, and Bureaucratic Power in Lesotho (1990)', "Ferguson's The Anti-Politics Machine",
    'on the World Bank–supported Thaba-Tseka development project in Lesotho (1975–1984)',
    power='Development discourse portrayed Lesotho as an isolated farming economy needing technical fixes, ignoring its role as a labour reserve for South African mines; the project failed but expanded state bureaucratic power.',
    change='The project\'s unintended effect was to depoliticise poverty while extending government control into the mountains.')
eth('martin', 'Emily Martin, The Woman in the Body: A Cultural Analysis of Reproduction (1987)', "Martin's The Woman in the Body",
    'among women in Baltimore, USA, and in medical textbooks',
    classification='Medical textbooks described menstruation and menopause as failed production or breakdown, using industrial metaphors that framed women\'s bodies negatively.',
    power='Middle-class women tended to accept the medical model of their bodies, while working-class women more often resisted it.')
eth('lindenbaum', 'Shirley Lindenbaum, Kuru Sorcery: Disease and Danger in the New Guinea Highlands (1979)', "Lindenbaum's Kuru Sorcery",
    'among the Fore of the Eastern Highlands, Papua New Guinea',
    culture='The Fore attributed kuru, a fatal neurological disease, to sorcery; medical research linked it to mortuary feasts in which women and children consumed deceased relatives.',
    social_relations='Kuru killed mainly women, upsetting gender ratios and kin relations, and sorcery accusations intensified tensions between groups.',
    change='After mortuary cannibalism ended in the 1950s kuru declined, showing the interaction of cultural practice and disease.')
eth('richards', 'Paul Richards, Ebola: How a People\'s Science Helped End an Epidemic (2016)', "Richards's Ebola",
    'in Sierra Leone during the 2014–2015 West African Ebola epidemic',
    change='Communities adapted care and burial practices, developing safer burials and local quarantine, which Richards calls "people\'s science".',
    social_relations='Funeral practices such as washing the corpse expressed obligations to kin but spread the virus; safe and dignified burials needed community trust.',
    power='Top-down responses that ignored local knowledge produced distrust, while co-operation with chiefs and communities proved more effective.')
eth('janzen', 'John Janzen, The Quest for Therapy in Lower Zaire (1978)', "Janzen's The Quest for Therapy in Lower Zaire",
    'among BaKongo communities of Lower Zaire (now the Democratic Republic of the Congo), fieldwork 1960s',
    social_relations='Decisions about treatment were taken not by the patient alone but by a "therapy management group" of kin who negotiated which healers to consult.',
    culture='People combined Western clinics, prophets and traditional nganga healers, distinguishing "illnesses of God" (natural) from "illnesses of people" (caused by social conflict or witchcraft).',
    power='Senior kin controlled the therapy management group, so authority within the family shaped who received which treatment.')
eth('lock', 'Margaret Lock, Encounters with Aging: Mythologies of Menopause in Japan and North America (1993)', "Lock's Encounters with Aging",
    'comparing middle-aged women in Japan with women in Canada and the United States',
    culture='Japanese women experiencing kōnenki reported hot flushes far less often than North American women, and kōnenki was understood as a gradual life-stage change rather than a disease of oestrogen deficiency.',
    materiality='Lock coined "local biologies" to show that bodily experience itself differs between populations through the interaction of biology, diet and culture.',
    power='North American medicine framed menopause as a deficiency disease requiring hormone therapy, whereas Japanese doctors placed more emphasis on women\'s family duties, so medical models carried moral and gendered expectations.')
eth('fassin', 'Didier Fassin, When Bodies Remember: Experiences and Politics of AIDS in South Africa (2007)', "Fassin's When Bodies Remember",
    'in South Africa during the AIDS epidemic and the controversy over President Thabo Mbeki\'s AIDS policies (around 2000)',
    power='Fassin links the epidemic to the "embodied history" of apartheid – migrant labour, poverty and violence – and analyses why AIDS denialism found support as a response to racist representations.',
    change='Activism by the Treatment Action Campaign (founded 1998) and court rulings forced the state to provide antiretroviral drugs, changing the politics of health.',
    space='Apartheid geography – townships, homelands and mine hostels – shaped the routes along which HIV spread.')
eth('petryna', 'Adriana Petryna, Life Exposed: Biological Citizens after Chernobyl (2002)', "Petryna's Life Exposed",
    'in Ukraine after the 1986 Chernobyl nuclear disaster',
    identity='People sought recognition as radiation sufferers, a "biological citizenship" in which proof of bodily damage became the basis of claims on the post-Soviet state.',
    power='Scientific and bureaucratic commissions determined whose illnesses counted as Chernobyl-related, controlling access to welfare.',
    change='In the economic collapse after 1991, disability status became one of the few reliable sources of income.')
eth('fadiman', 'Anne Fadiman, The Spirit Catches You and You Fall Down (1997), a journalist\'s ethnographic account', "Fadiman's The Spirit Catches You and You Fall Down",
    'about Lia Lee, a Hmong child with epilepsy, her family and her doctors in Merced, California (1980s)',
    culture='Lia\'s parents understood her seizures as qaug dab peg – "the spirit catches you and you fall down" – a loss of soul that might also mark a future shaman, while doctors diagnosed epilepsy.',
    power='Doctors\' complex drug regimes and the removal of Lia into foster care for non-compliance show biomedicine overriding a family\'s explanatory model.')
eth('chagnon', 'Napoleon Chagnon, Yanomamö: The Fierce People (1968)', "Chagnon's Yanomamö: The Fierce People",
    'among Yanomami communities of southern Venezuela and northern Brazil (fieldwork from 1964)',
    power='Critics argued that the portrayal of the Yanomami as "fierce" was used by gold miners and politicians to justify encroachment on Yanomami land.',
    social_relations='The controversy after Patrick Tierney\'s Darkness in El Dorado (2000) raised questions about gifts of steel tools, consent to the 1960s blood sampling, and the anthropologist\'s effect on relations between villages.')
eth('hurston', 'Zora Neale Hurston, Mules and Men (1935)', "Hurston's Mules and Men",
    'collecting African American folklore in Eatonville, Florida, and hoodoo practice in New Orleans (late 1920s)',
    identity='Hurston, a Black woman raised in Eatonville and trained by Boas, studied her own community, raising questions about insider positionality.',
    culture='She presented folktales and hoodoo as living, creative traditions rather than as survivals of a primitive past.')
eth('nanda', 'Serena Nanda, Neither Man nor Woman: The Hijras of India (1990)', "Nanda's Neither Man nor Woman",
    'among hijra communities in India',
    identity='Hijras are culturally recognised as neither man nor woman, a third gender with a ritual role linked to devotion to the goddess Bahuchara Mata.',
    social_relations='Hijras live in households organised around guru–chela (teacher–disciple) relationships that function as a form of kinship.',
    classification='The hijra case challenges the assumption that sex/gender classification is everywhere binary.')
eth('stack', 'Carol Stack, All Our Kin: Strategies for Survival in a Black Community (1974)', "Stack's All Our Kin",
    'among poor African American families in "The Flats", a pseudonymous neighbourhood of a Midwestern US city (late 1960s)',
    social_relations='Networks of kin and "fictive" kin swapped goods, childcare and money, so domestic groups stretched across several households as a survival strategy.',
    power='Welfare rules penalised sharing and marriage, so the state shaped household composition and kept families in poverty.')
eth('fergusonexp', 'James Ferguson, Expectations of Modernity: Myths and Meanings of Urban Life on the Zambian Copperbelt (1999)', "Ferguson's Expectations of Modernity",
    'among mineworkers on the Zambian Copperbelt during the economic decline of the 1980s',
    change='When copper prices collapsed, the promised path to urban modernity reversed; many mineworkers returned to rural areas, undermining linear stories of progress.',
    identity='Workers performed "cosmopolitan" or "localist" cultural styles, showing urban identity as a matter of performed style rather than fixed stage.')


S = P.S

# =============================================================================================
# ch01 Engaging with Anthropology: The Language of Anthropology
# =============================================================================================
S('ch01-st1', 'the holistic and comparative study of human societies', ['culture', 'society', 'social_relations'],
  ['malinowski', 'miner', 'boas', 'mead'],
  terms=[('social and cultural anthropology', 'the comparative study of human societies and cultures, based mainly on long-term fieldwork, that seeks to understand how people make sense of and organise their social lives'),
         ('holism', 'the principle of studying any practice in relation to the wider social, economic, political, religious and historical context of which it is part'),
         ('emic perspective', 'an insider\'s view: the categories, meanings and explanations used by members of the group being studied'),
         ('etic perspective', 'an outsider\'s or analyst\'s view: categories and explanations developed by the observer to describe and compare across societies'),
         ('comparison', 'the anthropological method of placing practices from different societies side by side to identify similarities, differences and broader patterns')],
  facts=[('Which of the following best describes an emic account?', 'An explanation of a ritual in the terms used by its participants',
          ['A statistical comparison of rituals across 50 societies', 'An analysis of a ritual using Marxist theory', 'A description of a ritual from a tourist brochure'],
          'Emic accounts use insiders\' own categories and meanings.'),
         ('Which of the following is the best example of holism in anthropology?', 'Studying a harvest festival in relation to land tenure, kinship, religion and the market',
          ['Counting how many people attend a harvest festival', 'Interviewing one festival organiser', 'Recording the festival songs only'],
          'Holism links a practice to the wider context of which it is part.'),
         ('Which method is most closely associated with social and cultural anthropology?', 'Long-term participant observation',
          ['Laboratory experiments', 'National opinion polls', 'Carbon dating of artefacts'],
          'Long-term participant observation (fieldwork) is the defining method of SCA.'),
         ('Which of the following questions is most clearly comparative?', 'How do gift-giving practices differ between Trobriand islanders and London households?',
          ['What time does the market open?', 'Who is the oldest person in the village?', 'How many goats does one household own?'],
          'Comparison sets practices from different societies side by side.')],
  why=[('Explain why anthropologists value both emic and etic perspectives.', 'Emic accounts show how people themselves understand their practices, avoiding distortion by outside categories; etic analysis allows comparison and can reveal patterns or structures (e.g. power, economy) of which participants are unaware. Combining them gives a fuller, more rigorous account.'),
       ('Explain why holism is important for understanding a single practice such as bridewealth.', 'Bridewealth only makes sense in relation to kinship (which group gains rights to children), economy (cattle or money), politics (alliances) and values (respect); studying it in isolation could mislead an observer into seeing it as "buying a wife".'),
       ('Explain why anthropology is said to make "the strange familiar and the familiar strange".', 'By explaining unfamiliar practices in their context, anthropology makes them intelligible (strange made familiar); by applying the same analysis to our own customs, as Miner did with the "Nacirema", it exposes taken-for-granted assumptions (familiar made strange).'),
       ('Explain why comparison is central to anthropological knowledge.', 'Comparison tests whether a practice is universal or culturally specific, shows the range of human possibilities, and allows generalisation about concepts such as kinship, power or exchange while respecting local differences.')],
  contrast=[('an emic perspective', 'an etic perspective', 'An emic perspective uses the meanings and categories of the people studied; an etic perspective uses the analyst\'s categories, which allow cross-cultural comparison but may not be recognised by participants.'),
            ('social and cultural anthropology', 'sociology', 'Both study social life, but anthropology traditionally relies on long-term participant observation and holistic, comparative study of small-scale or local settings, whereas sociology more often uses surveys and statistics to study large-scale patterns in industrial societies; the boundary is now blurred.')],
  misc=[('Anthropologists only study small, remote, "traditional" societies.', 'Anthropologists study every kind of society, including cities, corporations, hospitals and online worlds; Bourgois studied crack dealers in New York and Boellstorff studied Second Life.'),
        ('An etic account is always more objective and therefore better than an emic one.', 'Etic categories are also cultural products of the analyst\'s background; emic and etic accounts answer different questions and are strongest when combined.')],
  cases=[('Malinowski\'s fieldwork in the Trobriand Islands (1915–1918)', 'Malinowski lived among Trobrianders for long periods, learned the language and traced how the kula exchange was linked to magic, canoe-building, chiefship and myth.',
          'holism', 'he showed that the kula could only be understood by connecting exchange to politics, religion, technology and kinship rather than treating it as trade alone.'),
         ('Horace Miner\'s "Body Ritual among the Nacirema" (1956)', 'Miner described Americans\' bathroom routines, dentists and doctors as strange magical rites of the "Nacirema".',
          'the familiar made strange', 'it shows that an outsider\'s (etic) description can make one\'s own culture look exotic, revealing ethnocentric assumptions in how "others" are described.')],
  ev=[('Social and cultural anthropology can never be truly comparative, because every culture is unique.',
       ['Boas\'s historical particularism stresses that each culture has its own history', 'concepts such as "marriage" may not translate between societies (Gough on the Nayar)'],
       ['comparison need not deny uniqueness; it uses shared concepts to highlight difference', 'comparative work, such as on exchange (Malinowski, Weiner), has produced powerful insights', 'IB key concepts provide a framework for comparing across contexts'],
       'Comparison is possible and valuable if concepts are used carefully and local meanings are respected.'),
      ('The emic perspective should always take priority over the etic perspective.',
       ['it respects people\'s own understandings and avoids imposing outside categories', 'it counters the colonial history of describing others in the observer\'s terms'],
       ['insiders may not see wider structures such as global markets or state power', 'people within a group disagree, so there is rarely a single emic view', 'etic concepts enable comparison and critique'],
       'Neither should always dominate: good ethnography moves between emic and etic perspectives.')],
  ext=[('At the bus depot on the edge of the city, Wairimu sells boiled eggs and peeled oranges from a tray balanced on a crate. "I am not a hawker," she tells me firmly. "Hawkers run. I have my place." Her place is a square of pavement she rents informally from the man who sweeps the depot each morning. When conductors shout the names of destinations, she calls back their nicknames. On Sundays she brings eggs to the sweeper\'s family instead of money. Twice a month the county askaris clear the pavement, and on those days Wairimu sits on the bus with her tray, "travelling" until they leave.',
        'fieldnotes from a bus depot in a Kenyan town', 'the ways in which Wairimu secures her place to trade',
        'She rents a square of pavement informally from the sweeper; she pays partly in eggs (gifts) to his family rather than money; she maintains friendly relations with conductors through nicknames; she avoids the county officers by sitting on a bus during clearances; she distinguishes herself from "hawkers" who run.',
        'why Wairimu insists that she is "not a hawker"', 'Her claim is an emic category that asserts status and identity: having "a place" signals legitimacy, belonging and respectability compared with mobile hawkers. Her security rests on social relations (sweeper, conductors) rather than legal title, so identity and place are produced through relationships and contested by state power (askaris).',
        'identity', 'Traders in informal economies may be vulnerable to state officers, so anonymity, pseudonyms and care with details of the informal rental and avoidance tactics are essential; consent must be informed and ongoing; the researcher must avoid drawing official attention to the depot.')])

S('ch01-st2', 'the analysis of everyday social life', ['belonging', 'power', 'materiality', 'change'],
  ['malinowski', 'geertz', 'bourgois', 'basso'],
  terms=[('belonging', 'the ways people come to feel and be recognised as members of groups, places or communities, and the processes of inclusion and exclusion that this involves'),
         ('materiality', 'the significance of physical objects, bodies and environments in social life, including how things shape and express relationships, identities and meanings'),
         ('power', 'the capacity to influence or control people, resources and meanings, exercised through force, institutions, knowledge and everyday practice'),
         ('space-place-time', 'the key concept that examines how people give meaning to locations (turning space into place) and how they understand, organise and remember time'),
         ('classification', 'the culturally specific ways in which people order people, things and experiences into categories, and the consequences of those categories'),
         ('social relations', 'the patterned ties – of kinship, friendship, exchange, hierarchy or conflict – that connect people to one another')],
  facts=[('Which of the following is one of the key concepts of IB Social and Cultural Anthropology?', 'Materiality',
          ['Sovereignty', 'Supply and demand', 'Natural selection'], 'Materiality is one of the course key concepts; the others belong to politics, economics and biology.'),
         ('A student analyses how a Western Apache place-name carries a moral story. Which key concept is most directly involved?', 'Space-place-time',
          ['Materiality', 'Classification', 'Society'], 'Basso\'s study of Apache place-names is a classic example of space-place-time.'),
         ('An anthropologist studies how kula valuables gain value from their histories of ownership. Which key concept is the focus?', 'Materiality',
          ['Belonging', 'Change', 'Identity'], 'The meaning and value of objects is the concern of materiality.'),
         ('Which statement best describes the anthropological concept of power?', 'It operates through institutions, knowledge and everyday practices as well as force',
          ['It belongs only to governments and armies', 'It exists only in societies with states', 'It is the same as wealth'],
          'Anthropologists, drawing on Foucault and Gramsci among others, see power as diffuse as well as coercive.')],
  why=[('Explain why the key concepts are useful when reading an unfamiliar ethnography.', 'They provide a common analytical vocabulary that directs attention to recurring dimensions of social life (power, identity, materiality, etc.), so a reader can analyse new material systematically and compare it with other ethnographies.'),
       ('Explain why change is treated as a key concept even when studying "traditional" practices.', 'Practices labelled traditional are always being reproduced, adapted and contested; studying change avoids presenting societies as timeless and shows how history, markets and states shape culture.'),
       ('Explain why the key concepts overlap with one another.', 'Social life is integrated: belonging involves power over who is included, identity is often expressed through materiality, and classification shapes social relations, so one ethnographic example usually illustrates several concepts.'),
       ('Explain why materiality matters to anthropologists who study meaning.', 'Meanings are carried and made by things – clothing, houses, gifts, bodies – so analysing objects shows how values and relationships become tangible and durable.')],
  contrast=[('society', 'culture', 'Society refers to the organised relationships and institutions connecting a group of people; culture refers to the learned, shared and contested meanings, values and practices through which they make sense of life.'),
            ('identity', 'belonging', 'Identity is how individuals and groups define who they are (and are defined by others); belonging is the experience and recognition of membership in a group or place, including who is included or excluded.')],
  misc=[('Materiality simply means how much money or property people have.', 'Materiality concerns the social meanings and effects of objects, bodies and environments, not only wealth; a kula armshell or a banana-leaf bundle may have little monetary value but great social significance.'),
        ('Power is only visible when someone uses violence.', 'Power is often hidden in everyday routines, norms and categories – for example in the status contests of Geertz\'s cockfight or in the symbolic violence described by Holmes.')],
  cases=[('Geertz\'s study of the Balinese cockfight', 'Men wagered on cocks according to kin and village ties, and deep matches between high-status men put status symbolically at stake.',
          'how one practice illustrates several key concepts', 'the cockfight shows power (status hierarchy), identity (masculinity), social relations (betting alliances) and culture (a text Balinese tell about themselves).'),
         ('Basso\'s work with the Western Apache of Cibecue', 'Apache speakers used place-names and their stories to remind wrongdoers of ancestral lessons.',
          'space-place-time', 'it shows that space becomes place through names, stories and memory, and that places carry moral and historical meaning.')],
  ev=[('Power is the most important key concept in social and cultural anthropology.',
       ['power shapes classification, belonging and identity', 'ethnographies such as Bourgois and Holmes show structural power explaining suffering'],
       ['an exclusive focus on power can neglect meaning, emotion and creativity', 'concepts such as materiality and space-place-time reveal dimensions of life not reducible to power', 'the concepts are interdependent'],
       'Power is pervasive and frequently central, but its importance depends on the question and it is best analysed together with other concepts.'),
      ('Key concepts impose Western categories on non-Western societies.',
       ['concepts such as "identity" or "society" emerged from European social thought', 'emic categories may not map onto them'],
       ['the concepts are deliberately broad and open to local definition', 'anthropologists from many regions use and reshape them', 'without shared concepts comparison would be impossible'],
       'The concepts carry a history, but used reflexively alongside emic categories they aid rather than distort understanding.')],
  ext=[('In the Saturday clothing market of Kotei, sellers unpack bales of second-hand garments shipped from Europe. Buyers call the clothes "dead white men\'s clothes", though the sellers prefer "obroni wawu". Ama, who has sold there for twenty years, opens each bale like a lottery. "One bale feeds my children for a month, another one is rags." Her stall is her late mother\'s, and older traders still greet her by her mother\'s name. When a city council project proposed moving the market to a new concrete building, the traders marched with their best garments draped across their shoulders.',
        'fieldnotes from a second-hand clothing market in Ghana', 'how the traders in the text depend on and use clothing',
        'Bales are opened unseen and their contents determine income ("feeds my children" or "rags"); clothing has names that carry meaning ("obroni wawu"); stalls are inherited (Ama\'s mother\'s stall); traders wore their best garments during the protest march.',
        'how the second-hand clothes connect the market traders to wider relations of power', 'The bales link traders to global flows of discarded Western goods, over which they have no control; the names given to the clothes comment on that inequality; the council\'s relocation plan shows state power over space; the traders turn the clothes into a symbol in protest, showing materiality as a resource for resisting power.',
        'materiality', 'The researcher must obtain consent from traders who may fear the council, avoid identifying individuals involved in protests, and consider how publishing names (e.g. Ama, her mother\'s name) might expose them; findings should be shared with the traders\' association.')])

S('ch01-st3', 'the way people judge other ways of life', ['culture', 'classification', 'power'],
  ['miner', 'boas', 'abulughod', 'scheper'],
  terms=[('ethnocentrism', 'judging other cultures by the standards and values of one\'s own, usually assuming one\'s own ways are natural or superior'),
         ('cultural relativism', 'the methodological principle that practices and beliefs should be understood in terms of their own cultural context before they are judged'),
         ('moral relativism', 'the philosophical position that there are no universal moral standards, so practices cannot be judged across cultures'),
         ('othering', 'representing a group as fundamentally different from and inferior to "us", often by stressing exotic or unchanging traits'),
         ('universalism', 'the view that certain standards or rights, such as human rights, apply to all people regardless of culture')],
  facts=[('Which anthropologist is most closely associated with establishing cultural relativism as a principle of American anthropology?', 'Franz Boas',
          ['Lewis Henry Morgan', 'Herbert Spencer', 'Bronisław Malinowski'], 'Boas and his students (Mead, Benedict) championed cultural relativism against evolutionism.'),
         ('What was the main purpose of Horace Miner\'s "Body Ritual among the Nacirema" (1956)?', 'To show how ethnographic description can make familiar practices seem exotic',
          ['To describe a newly discovered tribe in South America', 'To defend evolutionary rankings of cultures', 'To report a survey of American dentists'],
          'The "Nacirema" are Americans; the satire exposes ethnocentric description.'),
         ('Lila Abu-Lughod\'s essay "Do Muslim Women Really Need Saving?" (2002) mainly criticises:', 'the use of images of oppressed Muslim women to justify Western intervention',
          ['the practice of anthropological fieldwork', 'Islamic law in Egypt', 'the ethics of photography'],
          'She argued that "saving" rhetoric after 2001 reproduced othering and ignored women\'s own views and the effects of war.')],
  why=[('Explain why cultural relativism is described as a methodological principle rather than a moral position.', 'It asks the anthropologist to suspend judgement in order to understand a practice in its context; this does not require accepting that every practice is morally right, so an anthropologist can still take ethical positions after understanding.'),
       ('Explain why ethnocentrism is a problem for ethnographic research.', 'If the researcher judges through their own categories, they misinterpret what they observe, ignore insiders\' meanings and may produce representations that justify domination, as in colonial accounts of "savages".'),
       ('Explain why othering can have political consequences.', 'Representing groups as backward or dangerous can justify intervention, discrimination or exclusion – for example colonial rule or the "saving Muslim women" rhetoric criticised by Abu-Lughod.')],
  contrast=[('cultural relativism', 'moral relativism', 'Cultural relativism is a method: understand a practice in its own context before evaluating it. Moral relativism is a philosophical claim that no cross-cultural moral judgement is possible; most anthropologists accept the first but not necessarily the second.'),
            ('ethnocentrism', 'cultural relativism', 'Ethnocentrism judges others by one\'s own standards and assumes their superiority; cultural relativism seeks to understand practices in terms of their own cultural logic before judging.')],
  misc=[('Cultural relativism means anthropologists must accept every practice as morally good.', 'Cultural relativism is a method for understanding; anthropologists such as Scheper-Hughes argue for ethical engagement after understanding (the "primacy of the ethical").'),
        ('Only Westerners are ethnocentric.', 'Ethnocentrism is a general human tendency found in all societies; anthropology tries to counter it everywhere, including in the anthropologist\'s own assumptions.')],
  cases=[('Abu-Lughod\'s critique of the "saving Muslim women" discourse after 2001', 'She showed how images of veiled Afghan women were used to justify the war in Afghanistan, while ignoring women\'s own priorities and the harms of intervention.',
          'othering and the limits of ethnocentric judgement', 'it shows that portraying women as passive victims of "their culture" erases their agency and serves political ends; she argues for respecting different ideas of a good life while still opposing injustice.'),
         ('Scheper-Hughes\'s "The Primacy of the Ethical" (1995)', 'Scheper-Hughes argued that anthropologists cannot hide behind relativism when faced with suffering such as the infant deaths she witnessed in north-east Brazil.',
          'the limits of cultural relativism', 'she calls for a "militant" anthropology that understands context but also takes moral responsibility, showing that relativism as method need not mean moral neutrality.')],
  ev=[('Cultural relativism prevents anthropologists from criticising harmful practices.',
       ['strict relativism could imply no basis for criticism', 'relativist arguments have sometimes been used to defend abuses as "tradition"'],
       ['relativism is primarily a method of understanding, not a moral endpoint', 'Scheper-Hughes and Abu-Lughod show anthropologists combining contextual understanding with ethical judgement', 'insiders themselves often contest harmful practices, so there is no single "cultural" view'],
       'Methodological relativism does not prevent criticism; it makes criticism better informed and more respectful of local voices.'),
      ('Ethnocentrism can never be fully overcome by an anthropologist.',
       ['researchers always interpret through their own background (positionality)', 'language and categories carry assumptions'],
       ['reflexivity, long-term fieldwork and learning the language reduce ethnocentrism', 'collaboration with participants and critique by colleagues expose bias'],
       'It cannot be eliminated completely, but it can be recognised and greatly reduced through reflexive practice.')],
  ext=[('The volunteer group arrived in the village with a truck of solar cookers. At the meeting, their leader explained that cooking over wood fires was "unhealthy and backward". The women listened politely. Three months later most cookers stood in a storeroom. Kadi explained to me that the evening fire is where daughters learn recipes and where neighbours stop to talk, and that the solar cooker "works only when the sun is at its highest, when we are in the fields". She uses hers to dry chillies. "They wanted us to be modern," she laughed, "but they never asked when we cook."',
        'fieldnotes from a rural village in the Sahel region of West Africa', 'how the women in the text responded to the solar cookers',
        'They listened politely at the meeting; most cookers were left in a storeroom; Kadi explained why the evening fire matters (learning recipes, talking with neighbours); she pointed out the timing problem (sun at midday while women are in the fields); she repurposed the cooker to dry chillies.',
        'why the volunteers\' project can be described as ethnocentric', 'The volunteers judged wood fires as "backward" by their own standards and assumed their technology was superior; they did not study when, how and why women cook (an emic perspective); the fire\'s social meaning (teaching daughters, sociability) and the women\'s work schedule were ignored, so the project failed, while women reinterpreted the object in their own terms.',
        'culture', 'The anthropologist must avoid further embarrassing either the villagers or the volunteers, obtain consent from Kadi and the women, protect identities, and consider their own possible role in development projects; quoting laughter or criticism could damage relations with the NGO on which the village depends.')])

# =============================================================================================
# ch02 Engaging with Anthropology: Culture, Society and Identity
# =============================================================================================
S('ch02-st1', 'the learning, sharing and contesting of culture', ['culture', 'power', 'change'],
  ['geertz', 'abulughod', 'boas', 'mead', 'wolf'],
  terms=[('culture (Tylor)', 'in E. B. Tylor\'s 1871 definition, "that complex whole which includes knowledge, belief, art, morals, law, custom, and any other capabilities and habits acquired by man as a member of society"'),
         ('enculturation', 'the process by which a person learns the norms, values and practices of their culture, mainly in childhood'),
         ('thick description', 'Geertz\'s term for ethnographic writing that interprets the layered meanings of an action for those involved, rather than just recording behaviour'),
         ('symbol', 'something – an object, gesture, word or image – that stands for something else by convention, so that its meaning must be learned'),
         ('contested culture', 'the view that culture is not uniformly shared but is debated, negotiated and used by differently positioned people, often in relation to power')],
  facts=[('Who defined culture as a "complex whole" acquired by humans as members of society (1871)?', 'E. B. Tylor',
          ['Clifford Geertz', 'Bronisław Malinowski', 'Pierre Bourdieu'], 'Tylor\'s definition opens Primitive Culture (1871).'),
         ('Clifford Geertz described culture as:', '"webs of significance" that humans themselves have spun',
          ['an adaptation to the natural environment', 'a set of biological instincts', 'a stage on the ladder of social evolution'],
          'In The Interpretation of Cultures (1973) Geertz saw culture as a public system of meanings to be interpreted.'),
         ('Which example best shows culture as learned rather than inherited?', 'A child adopted from Korea into a Danish family grows up speaking Danish and celebrating Danish holidays',
          ['Children everywhere grow teeth at a similar age', 'Humans sweat when hot', 'Infants cry when hungry'],
          'Language and festivals are acquired through enculturation, not genes.'),
         ('Lila Abu-Lughod\'s essay "Writing Against Culture" (1991) argued that:', 'the concept of culture can freeze differences and present groups as homogeneous and timeless',
          ['culture is determined by the environment', 'anthropologists should stop doing fieldwork', 'culture is the same as race'],
          'She proposed "ethnographies of the particular" to counter the homogenising effect of the culture concept.')],
  why=[('Explain why many anthropologists now describe culture as contested rather than simply shared.', 'Within any group people differ by gender, age, class and power, and they argue over values and practices; treating culture as uniformly shared hides these differences and often privileges the views of dominant members.'),
       ('Explain why Geertz compared the cockfight to a text.', 'He treated it as a public set of symbols that Balinese "read" and that the anthropologist can interpret – "a story they tell themselves about themselves" – so its significance lies in meanings about status, not only in gambling.'),
       ('Explain why culture is said to be symbolic.', 'Humans relate to the world through shared, learned meanings: a gesture, colour or object (e.g. a wedding ring) has meaning only by convention, so understanding behaviour requires grasping the symbols involved.')],
  contrast=[('culture as shared', 'culture as contested', 'Seeing culture as shared emphasises common values that hold a group together; seeing it as contested emphasises disagreement, power and change, as different members claim and redefine what "our culture" is.'),
            ('Tylor\'s definition of culture', 'Geertz\'s definition of culture', 'Tylor treated culture as a complex whole of acquired capabilities, arranged on an evolutionary scale; Geertz treated culture as public webs of meaning to be interpreted through thick description, with no evolutionary ranking.')],
  misc=[('Culture is something people are born with because it is passed down through families.', 'Culture is learned through enculturation; families transmit it socially, not genetically, and people can acquire new cultures.'),
        ('All members of a culture share exactly the same beliefs.', 'Culture is shared in part but also contested: Abu-Lughod showed Awlad \'Ali Bedouin voicing sentiments in poetry that contradicted the public honour code.')],
  cases=[('Abu-Lughod\'s study of ghinnawa poetry among the Awlad \'Ali Bedouin', 'People who publicly upheld the honour code expressed love, longing and vulnerability in short sung poems.',
          'culture as contested and multi-layered', 'it shows two coexisting discourses within one culture, so culture is not a single, consistent system shared equally by all.'),
         ('Mead\'s Coming of Age in Samoa and Freeman\'s critique', 'Mead (1928) portrayed Samoan adolescence as relatively untroubled; Derek Freeman (1983) argued she had been misled and ignored violence and strict sexual norms.',
          'debates about culture versus biology', 'the controversy shows how claims about culture can be contested and how the ethnographer\'s theory and informants shape what is found.')],
  ev=[('Geertz\'s interpretive approach is the most useful way to understand culture.',
       ['thick description captures meanings from the actors\' point of view', 'it treats culture as public and observable rather than hidden in minds'],
       ['it can neglect power and inequality (critiqued by Asad and Roseberry)', 'the ethnographer\'s interpretation may be privileged over participants\' own', 'it can present a culture as more coherent than it is'],
       'Interpretation is essential, but it is most useful when combined with attention to power, history and internal disagreement.'),
      ('The concept of culture is more misleading than helpful.',
       ['it can freeze groups as homogeneous and timeless (Abu-Lughod, "Writing Against Culture")', 'it has been used politically to justify exclusion'],
       ['it remains the best term for learned, shared meanings', 'reflexive use attentive to change and contest avoids the problems'],
       'The concept is helpful if used critically, stressing that culture is learned, contested and changing.')],
  ext=[('Every December the elders of the Nakamura neighbourhood association repair the paper lanterns for the shrine festival. This year the young men who carry the portable shrine asked to add LED strips. Mr Kato, who has led the festival for thirty years, refused: "The flame must flicker. That is how the kami know we are here." His granddaughter, filming on her phone, rolled her eyes. "He says the same thing about the music, but he changed the route when the new road came." In the end, the LEDs were allowed on the trucks that follow the shrine, but not on the shrine itself.',
        'fieldnotes from a neighbourhood shrine festival in urban Japan', 'the disagreement about the festival lanterns',
        'Young shrine bearers asked to add LED strips; Mr Kato refused because "the flame must flicker" for the kami; his granddaughter pointed out he had already changed the route when a road was built; a compromise allowed LEDs on the trucks but not on the shrine.',
        'how the text shows culture as contested rather than simply shared', 'Members of the same community disagree about what the tradition requires: an elder with authority defends a symbolic meaning (the flicker communicates with the kami), younger people propose change, and the granddaughter exposes that tradition has already been adapted. The compromise shows culture being negotiated through power (seniority) and change.',
        'culture', 'Filming and quoting identifiable people in a small neighbourhood association could create family or community conflict; consent from Mr Kato and the granddaughter, careful use of video and anonymisation of the neighbourhood are needed, as is sensitivity to sacred practices.')])

S('ch02-st2', 'the formation of identities based on ethnicity, gender, class and nation', ['identity', 'belonging', 'classification'],
  ['barthethnic', 'abulughod', 'bourgois', 'malkki', 'nanda'],
  terms=[('identity', 'the sense of who a person or group is, constructed through self-identification and recognition (or ascription) by others'),
         ('ethnicity', 'a form of identity based on a claimed shared origin, history or culture, which is maintained through boundaries between "us" and "them"'),
         ('imagined community', 'Benedict Anderson\'s term (1983) for the nation, whose members will never meet most others yet imagine a deep, horizontal comradeship'),
         ('intersectionality', 'the idea, developed by Kimberlé Crenshaw (1989), that identities such as gender, race and class interact to produce particular experiences of privilege or disadvantage'),
         ('ascribed identity', 'an identity assigned by others or by birth, such as caste or citizenship, rather than chosen by the individual')],
  facts=[('Fredrik Barth\'s Ethnic Groups and Boundaries (1969) argued that ethnic groups are defined mainly by:', 'the social boundaries maintained between groups',
          ['the cultural traits shared inside each group', 'shared biological ancestry', 'the territory they occupy'], 'Barth shifted attention from "cultural stuff" to boundary maintenance.'),
         ('Who coined the term "imagined communities" to describe nations?', 'Benedict Anderson',
          ['Ernest Gellner', 'Fredrik Barth', 'Margaret Mead'], 'Anderson\'s Imagined Communities (1983) links nationalism to print capitalism.'),
         ('Hijras in India are best described as:', 'a culturally recognised third gender with a ritual role',
          ['a caste of priests', 'a political party', 'an ethnic minority from Nepal'], 'Serena Nanda\'s Neither Man nor Woman (1990) describes hijra identity.')],
  why=[('Explain why anthropologists see identity as constructed rather than fixed.', 'Identities are produced through social interaction, history and power: people stress different identities in different contexts, categories change over time, and others\' recognition or ascription shapes who one can be.'),
       ('Explain why people may hold multiple identities at the same time.', 'A person can be, for example, Kurdish, a woman, a migrant and a student; different identities become salient in different settings, and they intersect to shape experience.'),
       ('Explain why belonging always involves exclusion.', 'Defining who belongs to a group, nation or place requires boundaries that mark others as outsiders, as Barth showed for ethnic groups and as citizenship rules show for nations.')],
  contrast=[('an ascribed identity', 'an achieved identity', 'An ascribed identity is assigned by birth or by others (e.g. caste, nationality at birth); an achieved identity is gained through actions or choices (e.g. becoming a doctor, converting religion), though the line between them is often blurred.'),
            ('ethnicity', 'race', 'Ethnicity is identity based on claimed shared culture, origin or history; race is a classification based on supposed physical differences. Anthropologists see both as social constructions, but race has been used to justify biologically based hierarchies.')],
  misc=[('Ethnic groups exist because their members share an ancient, unchanging culture.', 'Barth showed that ethnic groups persist through boundary maintenance even when cultural traits change and people move between groups.'),
        ('Gender is simply determined by biological sex in all societies.', 'Gender is culturally constructed: societies recognise different gender categories and roles, such as hijras in India.')],
  cases=[('Malkki\'s research with Hutu refugees in Tanzania (1985–1986)', 'Refugees in Mishamo camp narrated a "mythico-history" of themselves as the true Hutu nation in exile, while refugees in Kigoma town blended in and avoided the refugee label.',
          'identity as situational and shaped by place', 'it shows the same national/ethnic origin producing different identities depending on spatial and social conditions.'),
         ('Bourgois\'s study of crack dealers in East Harlem', 'Young Puerto Rican men refused humiliating office jobs and sought respect through street culture.',
          'intersections of class, ethnicity and gender in identity', 'their identity as respected men was shaped by class marginality, ethnic discrimination and masculine ideals, showing identities intersect.')],
  ev=[('Identity is chosen by individuals rather than imposed by society.',
       ['people perform and switch identities situationally (Malkki\'s town refugees)', 'online and urban life offer new identity options'],
       ['ascribed categories such as caste, race and citizenship are imposed by states and others', 'symbolic violence makes imposed identities feel natural (Holmes)', 'structural constraints shape what is possible (Bourgois)'],
       'Identity is negotiated: individuals choose within limits set by classification, power and recognition by others.'),
      ('Ethnic identity is mainly a product of boundaries rather than of shared culture.',
       ['Barth\'s argument that boundaries persist despite cultural change', 'ethnic markers are selected and changed strategically'],
       ['shared language, history and practices give ethnicity emotional force', 'states and censuses also create ethnic categories from above'],
       'Boundaries are central, but shared memories and state classification also shape ethnicity.')],
  ext=[('At the football academy, the coach divides the boys into "locals" and "internationals" for the Saturday match. Tomasz, born in the city to Polish parents, plays for the internationals. "At home I am Polish, at school I am British, here I am international," he shrugs. The local boys tease the internationals by imitating accents, but when the academy plays a team from the next town, everyone sings the same chant. After the match, the parents stand in separate groups by the car park: Polish, Somali, and "the English ones", as Tomasz\'s mother calls them.',
        'fieldnotes from a youth football academy in an English city', 'how Tomasz describes his identity',
        'He says he is Polish at home, British at school and "international" at the academy; he was born in the city to Polish parents; he is placed by the coach in the internationals group; he shrugs, suggesting identities are routine and situational.',
        'how belonging is created and limited in the text', 'The coach\'s classification (locals/internationals) creates groups; teasing about accents marks boundaries (Barth); a shared chant against another town shows a wider "us" that includes everyone (situational belonging); parents\' separation by nationality shows boundaries persisting in adult social relations.',
        'belonging', 'The participants are minors, so consent is needed from parents/guardians and the academy as well as assent from the boys; teasing and ethnic labels are sensitive, so names must be changed and the academy anonymised to avoid stigma.')])

S('ch02-st3', 'the organisation of roles, status and networks', ['social_relations', 'society', 'power'],
  ['malinowski', 'nuer', 'stack', 'geertz', 'bourdieu'],
  terms=[('social structure', 'the relatively enduring pattern of relationships, institutions and roles that organises a society'),
         ('institution', 'an established, rule-governed pattern of behaviour organised around a social need, such as marriage, the market or the law'),
         ('status', 'a recognised social position (e.g. elder, chief, mother) carrying expectations, rights and a degree of prestige'),
         ('role', 'the expected behaviour attached to a social status'),
         ('social network', 'the web of ties linking an individual to others, which can be mapped and used to analyse support, influence and the flow of resources'),
         ('reciprocity', 'the exchange of goods, services or favours that creates obligations; Marshall Sahlins distinguished generalised, balanced and negative reciprocity')],
  facts=[('Marshall Sahlins described exchange among close kin, where no immediate return is expected, as:', 'generalised reciprocity',
          ['balanced reciprocity', 'negative reciprocity', 'redistribution'], 'Generalised reciprocity is typical of close kin; balanced between equals; negative between strangers.'),
         ('Which anthropologist is associated with the structural-functionalist view of society as a system of social relations?', 'A. R. Radcliffe-Brown',
          ['Clifford Geertz', 'Franz Boas', 'Lila Abu-Lughod'], 'Radcliffe-Brown analysed social structure as a network of relations maintaining society.'),
         ('Carol Stack\'s All Our Kin (1974) showed that poor African American families survived by:', 'sharing goods and childcare through networks of kin and fictive kin',
          ['relying on government housing alone', 'forming nuclear households', 'migrating to the countryside'], 'Swapping across households was a survival strategy.')],
  why=[('Explain why anthropologists distinguish between status and role.', 'Status is the position a person occupies, while role is the behaviour expected of it; the distinction lets anthropologists analyse how people perform, stretch or fail to meet expectations of a position.'),
       ('Explain why network analysis is useful in urban anthropology.', 'In cities people are not contained in bounded villages; networks trace the ties through which they find jobs, housing and support (as in Stack\'s study), revealing structure across households and neighbourhoods.'),
       ('Explain why exchange creates social relations.', 'Gifts create obligations to receive and repay (Mauss); the return keeps a relationship alive, as with kula partners, so exchange is a way of making and maintaining ties, not only transferring goods.')],
  contrast=[('generalised reciprocity', 'balanced reciprocity', 'Generalised reciprocity is giving without expecting a specific or immediate return, usual among close kin; balanced reciprocity expects an equivalent return within a set time, usual between more distant equals.'),
            ('social structure', 'agency', 'Social structure is the enduring pattern of institutions and relations that constrains people; agency is people\'s capacity to act, choose and change those patterns. Practice theorists such as Bourdieu analyse how the two interact.')],
  misc=[('Social structure means the buildings and infrastructure of a society.', 'Social structure refers to patterned relationships, institutions and roles, not physical buildings.'),
        ('In kin-based societies people have no individual choice because their roles are fixed.', 'Even where kinship organises roles, people negotiate, manipulate and contest them – for example by choosing which kin to rely on or which obligations to honour.')],
  cases=[('the kula ring described by Malinowski', 'Trobriand men maintained lifelong exchange partners on other islands through which shell valuables circulated in opposite directions.',
          'exchange as the basis of social relations', 'the gifts create durable obligations and alliances between islands, showing exchange producing social structure.'),
         ('Stack\'s study of "The Flats"', 'Women swapped food, money and childcare across households, and welfare rules discouraged marriage and saving.',
          'networks as social structure', 'domestic life was organised through networks rather than nuclear households, and state rules shaped these relations.')],
  ev=[('Social structure determines individual behaviour.',
       ['institutions and roles shape expectations from birth', 'structural-functionalists such as Radcliffe-Brown emphasised stability'],
       ['people negotiate and change roles (Abu-Lughod\'s poets, Scott\'s resisting peasants)', 'Bourdieu\'s practice theory shows structure reproduced through agents\' practices, which can change it'],
       'Structure strongly constrains behaviour but is itself reproduced and modified through people\'s practices.'),
      ('Reciprocity is the foundation of all social relations.',
       ['Mauss and Malinowski showed gifts creating obligations', 'networks of exchange sustain survival (Stack)'],
       ['hierarchy, coercion and inheritance also structure relations', 'some relations (e.g. parent–infant care) are not experienced as exchange'],
       'Reciprocity is fundamental to many relations but not the only basis; power and hierarchy matter too.')],
  ext=[('In the tower block, the WhatsApp group "Floor 9 Aunties" has forty-two members. Mrs Okafor, who has lived there longest, posts each morning: who needs a lift to the clinic, whose son has a job interview. When the lift broke for a week, members took turns carrying shopping for Mr Lindqvist, the retired sailor on the top floor. "We don\'t keep accounts," says Mrs Okafor, "but everyone knows who helps." New tenants are added only after someone has "met them properly". Last year a young man was removed from the group after he refused to lend his ladder.',
        'fieldnotes from a council housing block in a European city', 'how the residents support one another',
        'They use a WhatsApp group; Mrs Okafor posts daily needs (lifts to the clinic, job interviews); members took turns carrying Mr Lindqvist\'s shopping when the lift broke; no accounts are kept; new tenants are admitted after being "met properly".',
        'how the WhatsApp group creates and regulates social relations', 'The group is a network that redistributes help through generalised reciprocity ("we don\'t keep accounts") yet reputation tracks who helps; Mrs Okafor\'s long residence gives her status and a coordinating role; admission and removal (the ladder) show boundaries and sanctions that enforce obligations.',
        'social_relations', 'Reading a private group chat requires the consent of all members, not only the administrator; health and employment details are sensitive; the removed young man should not be identifiable; the anthropologist\'s own membership might change relations in the group.')])

S('ch02-st4', 'the use and exchange of objects', ['materiality', 'identity', 'social_relations'],
  ['malinowski', 'weiner', 'miller', 'deleon'],
  terms=[('material culture', 'the objects, buildings and technologies people make and use, studied for what they reveal about social life and meaning'),
         ('commodity', 'a thing produced or acquired for exchange, usually through the market, whose value is expressed in price'),
         ('social life of things', 'Arjun Appadurai\'s idea (1986) that objects move through phases – commodity, gift, heirloom – and acquire biographies and changing values'),
         ('conspicuous consumption', 'Thorstein Veblen\'s term (1899) for spending on visible goods to display wealth and status'),
         ('inalienable possession', 'Annette Weiner\'s term for objects that cannot be given away permanently because they embody a group\'s identity, such as heirlooms or sacred objects')],
  facts=[('Who edited The Social Life of Things (1986), arguing that objects have biographies?', 'Arjun Appadurai',
          ['Daniel Miller', 'Marcel Mauss', 'Mary Douglas'], 'Appadurai\'s introduction argues that things move in and out of the commodity state.'),
         ('Marcel Mauss\'s The Gift (1925) argued that gifts involve three obligations:', 'to give, to receive and to reciprocate',
          ['to buy, to sell and to profit', 'to save, to invest and to inherit', 'to produce, to distribute and to consume'], 'These obligations make gifts "total social facts".'),
         ('In Daniel Miller\'s A Theory of Shopping (1998), everyday shopping in North London is mainly an expression of:', 'love and care for family members',
          ['individual hedonism', 'rejection of family obligations', 'pure economic calculation'], 'Miller saw provisioning as devotion and sacrifice.')],
  why=[('Explain why anthropologists study ordinary objects rather than only "exotic" artefacts.', 'Everyday things – clothes, phones, food – carry identities, relationships and values; studying them shows how social life is made material in all societies, including the anthropologist\'s own.'),
       ('Explain why a gift is not the same as a commodity.', 'A commodity transfer ends the relationship once paid for, whereas a gift creates an obligation to reciprocate and so maintains a relationship and carries the identity of the giver.'),
       ('Explain why objects can change meaning as they move.', 'Value depends on context: a mass-produced item becomes a gift, an heirloom or a museum piece, gaining new meanings through the relationships and histories attached to it (Appadurai).')],
  contrast=[('a gift', 'a commodity', 'A gift is embedded in relationships and creates obligation and identity links between giver and receiver; a commodity is exchanged impersonally for a price, ending the relationship once the transaction is complete.'),
            ('use value', 'symbolic value', 'Use value is an object\'s practical usefulness; symbolic value is the meaning, prestige or identity it carries, as with kula valuables that are rarely worn.')],
  misc=[('Material culture only tells us about technology, not about meaning.', 'Objects encode meanings, relationships and power: Weiner\'s banana-leaf bundles express matrilineal identity and women\'s power.'),
        ('Consumption is a purely individual and selfish activity.', 'Miller showed shopping as care for others, and consumption often expresses and builds social relationships and group identities.')],
  cases=[('Weiner\'s study of Trobriand women\'s wealth', 'At mortuary ceremonies women distributed thousands of banana-leaf bundles and fibre skirts to repay those who had cared for the dead.',
          'materiality and gendered power', 'objects with little use value became the means through which women displayed status and regenerated matrilineal identity.'),
         ('De León\'s Undocumented Migration Project', 'Researchers collected backpacks, water bottles and clothing left by migrants crossing the Sonoran Desert.',
          'material traces as ethnographic evidence', 'the objects reveal migrants\' bodily experiences and the effects of border policy, giving voice to people who cannot easily be interviewed.')],
  ev=[('Objects are more reliable evidence of culture than what people say.',
       ['objects show what people actually do, not just what they claim (De León)', 'they reveal patterns people do not articulate'],
       ['objects are interpreted by the anthropologist and may be misread', 'meanings of objects can only be grasped through what people say about them (Miller\'s interviews)'],
       'Objects and talk complement each other; neither is reliable alone.'),
      ('Global consumer goods are making cultures more alike.',
       ['the same brands and phones are found worldwide', 'consumption of global goods can displace local crafts'],
       ['people localise goods, giving them new meanings (Why We Post)', 'second-hand clothing and phones are used in culturally specific ways'],
       'Global goods spread, but local appropriation means they often increase diversity of meaning rather than homogenise.')],
  ext=[('In Hanh\'s family altar room in Ho Chi Minh City, a plastic Rolex sits beside her grandfather\'s photograph. Every year on the anniversary of his death, the family burn paper replicas – a motorbike, a smartphone, US dollars – so he can use them "on the other side". Hanh buys them from a shop on Hàng Mã street that also sells paper iPads. Her brother, who works in Singapore, sends money for the best models. "My grandfather never had a watch when he was alive," Hanh says. "Now he is a rich man."',
        'fieldnotes from a household in Vietnam', 'the objects used in the death anniversary ritual',
        'A plastic Rolex beside the grandfather\'s photograph; paper replicas of a motorbike, a smartphone and US dollars, which are burned; they are bought from a specialist shop that also sells paper iPads; the brother sends money from Singapore for the best models.',
        'how material objects sustain relationships between the living and the dead in the text', 'Burning paper goods transfers them to the ancestor, so objects maintain an ongoing exchange relationship across death; choosing luxury items expresses care and raises the grandfather\'s (and family\'s) status; migrant remittances finance the ritual, linking transnational family ties to ancestor care; consumer modernity is absorbed into ritual.',
        'materiality', 'Ancestor rituals are private and religious, so the family\'s consent to observe and photograph is essential; the anthropologist must avoid mocking or exoticising beliefs, protect the family\'s identity and handle information about remittances carefully.')])

# =============================================================================================
# ch03 The Practice of Anthropology: Ethnography and Fieldwork Methods
# =============================================================================================
S('ch03-st1', 'the experience of long-term fieldwork', ['culture', 'social_relations', 'power'],
  ['malinowski', 'bourgois', 'geertz', 'briggs', 'holmes'],
  terms=[('participant observation', 'the core anthropological method of living with and taking part in the everyday life of a group over a long period while systematically observing and recording it'),
         ('ethnography', 'both the method of long-term fieldwork and the written (or filmed) account that results from it'),
         ('rapport', 'a relationship of trust and mutual understanding between the anthropologist and the people studied, which makes access to everyday life possible'),
         ('gatekeeper', 'a person who controls or facilitates the researcher\'s access to a group or setting'),
         ('imponderabilia of actual life', 'Malinowski\'s phrase for the small, routine details of daily life that can only be observed by living among people'),
         ('key informant', 'a participant with whom the anthropologist works closely and who provides extended explanation and guidance (now often called an interlocutor)')],
  facts=[('Malinowski\'s fieldwork method was set out most famously in the introduction to:', 'Argonauts of the Western Pacific (1922)',
          ['The Nuer (1940)', 'Coming of Age in Samoa (1928)', 'Purity and Danger (1966)'], 'The introduction to Argonauts describes long-term immersion and learning the language.'),
         ('Why did Geertz and his wife gain acceptance in their Balinese village?', 'They fled with villagers from a police raid on a cockfight',
          ['They paid the village headman', 'They were Balinese by birth', 'They brought medicine for the villagers'], 'Sharing the villagers\' flight made them insiders in the villagers\' eyes.'),
         ('Which of the following is the main strength of participant observation?', 'It reveals the gap between what people say and what they do',
          ['It produces statistically representative samples', 'It requires no relationship with participants', 'It can be completed in a single day'], 'Long-term presence shows practice, not only stated norms.'),
         ('Philippe Bourgois carried out his fieldwork in East Harlem while:', 'living in the neighbourhood with his family for several years',
          ['posing as a police officer', 'conducting an online survey', 'visiting for one week each year'], 'He lived in El Barrio from 1985 to 1990.')],
  why=[('Explain why participant observation usually takes a long time.', 'Rapport takes time to build, people behave less for the observer as they get used to them, seasonal and life-cycle events must be seen, and learning the language and implicit rules requires extended immersion.'),
       ('Explain why participant observation helps to reveal the difference between ideal and real behaviour.', 'Interviews capture norms people state, whereas living alongside them shows what they actually do in everyday situations, including contradictions, compromises and unspoken rules.'),
       ('Explain why participant observation is described as a tension between closeness and distance.', 'The anthropologist must participate enough to understand insiders\' meanings, yet keep enough distance to observe, record and analyse critically; too much detachment misses meaning, too much immersion ("going native") can block analysis.')],
  contrast=[('participant observation', 'a structured survey', 'Participant observation involves long-term, flexible immersion that yields rich qualitative understanding of meanings in context; a structured survey asks many people the same fixed questions, giving comparable, quantifiable data but little insight into context or practice.'),
            ('participation', 'observation', 'Participation means taking part in activities to experience them from within; observation means watching and recording systematically. Ethnographers balance both, and the balance shapes the data obtained.')],
  misc=[('Participant observation is unscientific because the researcher is involved.', 'Participant observation is systematic (field notes, cross-checking, long duration) and its involvement is a strength that yields valid insider understanding; reflexivity addresses bias.'),
        ('The longer an anthropologist stays, the more objective the research becomes.', 'Longer fieldwork deepens understanding but does not remove the researcher\'s positionality; involvement may also increase, so reflexivity is still required.')],
  cases=[('Bourgois\'s fieldwork in East Harlem (1985–1990)', 'Bourgois lived in El Barrio, spent nights in crack houses, recorded conversations with dealers and witnessed violence.',
          'the strengths and risks of participant observation', 'immersion gave him access to dealers\' own accounts of respect and humiliation, but also exposed him to danger and difficult ethical choices about what to record and publish.'),
         ('Holmes\'s fieldwork with Triqui migrants (2003–2005)', 'Holmes picked berries, lived in labour camps and crossed the border with Triqui companions.',
          'embodied participant observation', 'sharing the work and the border crossing let him experience bodily suffering and the labour hierarchy first-hand, while his US citizenship meant he was treated differently by the Border Patrol.')],
  ev=[('Participant observation is the only reliable method for social and cultural anthropology.',
       ['it captures practice and meaning in context', 'it reveals the gap between what people say and do'],
       ['interviews, genealogies, surveys, archives and digital data add depth and breadth', 'some settings (elites, the past, online worlds) need other methods', 'all methods are shaped by the researcher\'s position'],
       'Participant observation is central, but it is most reliable in combination with other methods.'),
      ('Participant observation inevitably changes the behaviour of the people being studied.',
       ['the observer effect: people may perform for the researcher', 'gifts and presence can alter relations (Chagnon controversy)'],
       ['over time people habituate to the observer', 'reflexive accounts can analyse the researcher\'s effects as data'],
       'Some influence is unavoidable, but long-term fieldwork and reflexivity reduce and account for it.')],
  ext=[('By my third week on the fishing boat I had stopped being sick. The crew no longer laughed when I fell over; they shouted at me to coil the ropes instead. During the night shift, Rui told me the real reason they avoid the northern grounds: not the weather, as the captain says in interviews, but because "the Spanish boats take everything and the inspectors never come". I wrote this down on my phone in the toilet, where nobody could see. The next morning the captain asked what I was always typing. I said I was writing to my mother.',
        'fieldnotes from a fishing boat off the coast of Portugal', 'how the anthropologist\'s relationship with the crew changes in the text',
        'At first the crew laughed at the anthropologist\'s falls; by the third week they gave instructions (coil the ropes), treating them as a working member; Rui shared a confidential explanation during the night shift; the captain became curious about the note-taking.',
        'what the text shows about the strengths and difficulties of participant observation', 'Sharing work built rapport, so Rui revealed information that contradicts the captain\'s public interview account – showing the gap between official and private explanations. But it also creates difficulties: covert note-taking, a misleading answer to the captain, and the risk of betraying Rui\'s confidence, raising questions of consent and honesty.',
        'social_relations', 'The anthropologist deceives the captain about note-taking, so informed consent is compromised; Rui\'s criticism of inspectors and foreign boats could harm him if published; the anthropologist should be open about research, renegotiate consent and anonymise the boat and crew.')])

S('ch03-st2', 'the collection of ethnographic data', ['social_relations', 'materiality', 'classification'],
  ['malinowski', 'mead', 'deleon', 'basso'],
  terms=[('semi-structured interview', 'an interview guided by a list of topics or questions but flexible enough for the participant to raise their own concerns'),
         ('field notes', 'the written records an ethnographer makes during and after observation, ranging from brief jottings to full descriptive and reflective notes'),
         ('genealogical method', 'the technique, systematised by W. H. R. Rivers (1910), of recording kin relationships to map kinship terms, marriage, inheritance and social organisation'),
         ('visual anthropology', 'the use and study of photography, film and other images both as research methods and as objects of anthropological analysis'),
         ('life history', 'an extended account of one person\'s life, gathered over several interviews, used to show how wider social processes shape individual experience')],
  facts=[('Who systematised the genealogical method in anthropology?', 'W. H. R. Rivers',
          ['Franz Boas', 'Clifford Geertz', 'Marcel Mauss'], 'Rivers developed it during the 1898 Torres Strait Expedition and published it in 1910.'),
         ('Gregory Bateson and Margaret Mead\'s Balinese Character (1942) is notable for its use of:', 'thousands of photographs to analyse behaviour',
          ['statistical surveys', 'archaeological excavation', 'online questionnaires'], 'It pioneered photographic analysis in ethnography.'),
         ('Which type of field note is written up in full, usually at the end of the day?', 'Full descriptive field notes',
          ['Jottings', 'Interview transcripts', 'Census returns'], 'Jottings made in the moment are expanded into full notes as soon as possible.')],
  why=[('Explain why anthropologists write field notes as soon as possible after observing.', 'Memory fades and is reshaped quickly; writing promptly preserves concrete detail, sequences and quotations, and separating description from interpretation improves the reliability of the record.'),
       ('Explain why interviews alone may give a misleading picture of social life.', 'People describe ideal norms or what they think the researcher wants to hear, and may not articulate taken-for-granted practices; observation is needed to see what actually happens.'),
       ('Explain why genealogies remain useful even when kinship is not the topic.', 'They map who is related to whom, revealing inheritance, residence, alliances, migration and who participates in events, so they provide a framework for understanding social relations.')],
  contrast=[('a structured interview', 'an unstructured interview', 'A structured interview uses a fixed set of questions in the same order for comparability; an unstructured interview is a guided conversation that follows the participant\'s concerns, producing richer but less comparable data.'),
            ('descriptive field notes', 'reflexive field notes', 'Descriptive notes record what was seen and heard in concrete detail; reflexive notes record the anthropologist\'s feelings, assumptions and role, helping later analysis of positionality.')],
  misc=[('A photograph is an objective record that needs no interpretation.', 'Photographs are framed, selected and interpreted; they reflect the photographer\'s choices and power, and their meanings depend on context and audience.'),
        ('Field notes are the finished ethnography.', 'Field notes are raw data; the ethnography is a later analytical and written product that selects, interprets and theorises from them.')],
  cases=[('De León\'s Undocumented Migration Project', 'The project combined interviews with migrants, photography, forensic science and the archaeology of discarded objects in the Sonoran Desert.',
          'mixed methods in ethnography', 'combining material, visual and interview data documented experiences that no single method could capture, especially the deaths of migrants who could not be interviewed.'),
         ('Rivers and the Torres Strait Expedition (1898)', 'Members of the Cambridge expedition led by A. C. Haddon collected genealogies, measurements and recordings in the Torres Strait islands.',
          'the genealogical method', 'genealogies allowed Rivers to map kinship terms and social organisation systematically, a technique still used today.')],
  ev=[('Visual methods give a more truthful account of social life than written ethnography.',
       ['images capture detail and gesture that words miss (Bateson and Mead)', 'participants can engage with images directly'],
       ['images are framed and edited, so they are interpretations too', 'they can expose participants\' identities and raise ethical risks', 'meaning still needs explanation and context'],
       'Visual methods add valuable evidence but are not more truthful; they need the same critical and ethical scrutiny.'),
      ('Interviews are less valuable than participant observation.',
       ['people may say what they think the researcher wants', 'interviews capture norms rather than practice'],
       ['interviews reveal meanings, memories and life histories that cannot be observed', 'they give participants a voice in their own terms'],
       'Interviews and observation answer different questions and are strongest together.')],
  ext=[('I spread the family tree on the floor of the courtyard. Grandmother Sita corrected me at once: her late husband\'s brother\'s son should not be on the same line as her own sons "because they eat separately since the quarrel". She asked me to remove a woman I had included as a cousin: "She married outside; we do not count her." Her granddaughter, Priya, quietly added the woman back when Sita went inside. Later I photographed the family; Sita insisted that the sons stand at the front and the daughters-in-law behind.',
        'fieldnotes from a joint household in rural Nepal', 'how the members of the household responded to the genealogy and the photograph',
        'Sita corrected the placement of her husband\'s brother\'s son because the families "eat separately"; she asked for a woman who married outside to be removed; Priya added her back when Sita left; Sita arranged the photograph with sons in front and daughters-in-law behind.',
        'what the text reveals about the genealogical and visual methods', 'Both methods are not neutral records: the genealogy is shaped by present relationships (commensality, quarrels) and by judgements about who "counts" (exclusion after marriage outside), and different members (Sita, Priya) contest it; the photograph stages hierarchy by gender and generation. The methods reveal classification and power within the household.',
        'classification', 'Including the excluded woman or the quarrel could cause conflict; Priya\'s quiet act could expose her to criticism; photographs make family members identifiable, so consent for each image and its use is needed; the anthropologist should consider whose version of the family tree to publish.')])

S('ch03-st3', 'the relationship between ethnographer and participants', ['identity', 'power', 'social_relations'],
  ['rosaldo', 'briggs', 'abulughod', 'hurston', 'weiner'],
  terms=[('reflexivity', 'the practice of critically examining how the anthropologist\'s own background, assumptions and presence shape the research and its account'),
         ('positionality', 'the social position of the researcher – gender, age, ethnicity, class, nationality, religion – relative to the people studied, which affects access and interpretation'),
         ('insider (native) anthropology', 'research carried out by an anthropologist within a community to which they themselves belong'),
         ('halfie', 'Lila Abu-Lughod\'s term for anthropologists of mixed national or cultural identity who are partly insiders and partly outsiders'),
         ('the "reflexive turn"', 'the movement in the 1980s, associated with Writing Culture (Clifford and Marcus, 1986), that questioned ethnographic authority and urged attention to the author\'s role')],
  facts=[('Which book (1986) is most associated with the "crisis of representation" in anthropology?', 'Writing Culture, edited by James Clifford and George Marcus',
          ['The Interpretation of Cultures by Clifford Geertz', 'Purity and Danger by Mary Douglas', 'Argonauts of the Western Pacific by Bronisław Malinowski'], 'Writing Culture questioned the authority of the ethnographic text.'),
         ('Renato Rosaldo came to understand the Ilongot link between grief and rage after:', 'the accidental death of his wife, Michelle Rosaldo, in 1981',
          ['learning to hunt with Ilongot men', 'reading Malinowski\'s diaries', 'a court case in Manila'], 'His own grief positioned him to understand.'),
         ('Jean Briggs was ostracised by her Utku hosts because she:', 'openly expressed anger at visiting fishermen',
          ['refused to eat seal meat', 'took photographs without consent', 'left the camp without permission'], 'Anger was unacceptable to the Utku.'),
         ('Malinowski\'s private fieldwork diary, published in 1967, caused controversy because it:', 'revealed his frustration with and contempt for some Trobrianders',
          ['showed he had never visited the Trobriands', 'contained secret kula maps', 'was written in Kiriwinian'], 'A Diary in the Strict Sense of the Term exposed a gap between his public ethos and private feelings.')],
  why=[('Explain why positionality affects the data an anthropologist can collect.', 'Gender, age, ethnicity and status determine who will talk to the researcher, where they can go and what is shared; e.g. Abu-Lughod as a young woman accessed women\'s worlds and poetry that a male researcher might not.'),
       ('Explain why reflexivity is important for the validity of ethnography.', 'By making the researcher\'s assumptions, emotions and relationships explicit, reflexivity lets readers assess how the account was produced and reduces the risk of presenting a partial view as objective truth.'),
       ('Explain why being an insider is not automatically an advantage in fieldwork.', 'Insiders may take practices for granted, be positioned within local factions, face pressure to represent the group positively, or be denied access because of their own gender, class or family; outsiders may be allowed to ask "naive" questions.')],
  contrast=[('an insider anthropologist', 'an outsider anthropologist', 'An insider shares membership of the community studied and may have easier access and language skills but may overlook the familiar; an outsider must learn the culture and may see the taken-for-granted more clearly but may misunderstand meanings. Most anthropologists are partly both.'),
            ('reflexivity', 'self-indulgence', 'Reflexivity analyses how the researcher\'s presence shapes knowledge in order to improve the account; self-indulgence makes the researcher\'s feelings the main subject, displacing the people studied.')],
  misc=[('A good anthropologist removes all personal feelings from the research.', 'Feelings cannot be removed; reflexive anthropologists use them as data (Rosaldo\'s grief, Briggs\'s anger) and analyse how they shape interpretation.'),
        ('Positionality only matters when the anthropologist is a foreigner.', 'Positionality also shapes insider research, through gender, class, age and family ties within one\'s own community (e.g. Hurston in Eatonville).')],
  cases=[('Briggs\'s fieldwork among the Utku Inuit (1963–1965)', 'Briggs lost her temper with visiting fishermen, and her hosts responded with months of cold silence.',
          'positionality and reflexivity', 'her mistake made the Utku norm of emotional restraint visible, and her honest reflexive account turned a personal failure into ethnographic insight.'),
         ('Weiner\'s restudy of the Trobriand Islands (1970s)', 'As a woman, Weiner was invited into women\'s mortuary exchanges that Malinowski had largely ignored.',
          'gendered positionality', 'the ethnographer\'s gender shaped which activities were seen and valued, so Weiner\'s account corrected a male-centred picture of exchange.')],
  ev=[('Reflexivity makes ethnography less objective.',
       ['foregrounding the researcher may make accounts subjective and self-focused', 'readers may struggle to separate data from the author\'s feelings'],
       ['all ethnography is positioned; reflexivity makes this transparent', 'transparency allows readers to judge the evidence, increasing rigour', 'Rosaldo and Briggs show reflexivity producing new insight'],
       'Reflexivity strengthens rather than weakens rigour, provided it serves the analysis of the people studied.'),
      ('Insider anthropologists produce better ethnography than outsiders.',
       ['language skills and access (Hurston, Simpson)', 'less risk of exoticising'],
       ['insiders may overlook the familiar or be constrained by loyalties', 'outsiders can ask naive questions', 'the insider/outsider distinction is a continuum (Abu-Lughod\'s "halfie")'],
       'Neither position is inherently better; quality depends on reflexive awareness of the position held.')],
  ext=[('When I first arrived at the hostel for nursing students, the women called me "auntie" and stopped talking when I entered the kitchen. I was forty, foreign and childless, and they were nineteen. Everything changed the evening I burned the rice: they laughed until they cried and showed me how to soak it first. After that, Grace began to tell me about the senior nurses who shout at students in front of patients. "You won\'t write that," she said, half asking. I realised that my age, which had kept me out, now made her see me as someone who might complain on her behalf.',
        'fieldnotes from a nursing students\' hostel in the Philippines', 'how the students\' treatment of the anthropologist changes',
        'At first they called the anthropologist "auntie" and stopped talking in the kitchen; after the rice was burned they laughed and taught the anthropologist; Grace then shared criticisms of senior nurses; she asked, half-questioning, whether it would be written.',
        'how the anthropologist\'s positionality shapes the research in the text', 'Age, nationality and childlessness first created distance ("auntie"); a shared, humbling domestic mistake reduced status differences and created rapport; later the same age and outsider status made Grace see the researcher as a potential advocate, so positionality shapes both access and the expectations participants place on the researcher. Reflexive notes make this visible.',
        'identity', 'Grace\'s criticism of senior nurses could put her training at risk; her question signals uncertain consent, so the anthropologist must clarify what will be published, anonymise the hostel and avoid raising expectations of advocacy that cannot be met.')])

S('ch03-st4', 'research that follows people across places and online', ['space', 'change', 'social_relations'],
  ['boellstorff', 'whywepost', 'holmes', 'levitt'],
  terms=[('multi-sited ethnography', 'George Marcus\'s term (1995) for fieldwork that follows people, things, metaphors or conflicts across several connected locations'),
         ('digital ethnography', 'ethnographic research on social life in or through digital media, including online communities, platforms and virtual worlds'),
         ('collaborative ethnography', 'research in which participants are co-researchers who help shape questions, interpretation and writing'),
         ('netnography', 'Robert Kozinets\'s term for ethnographic research adapted to online communities'),
         ('avatar', 'a digital representation of a person in a virtual world, through which they interact with others')],
  facts=[('Who proposed "multi-sited ethnography" in 1995?', 'George Marcus',
          ['Clifford Geertz', 'Tom Boellstorff', 'Margaret Mead'], 'Marcus urged anthropologists to "follow the people, the thing, the metaphor".'),
         ('Tom Boellstorff\'s fieldwork for Coming of Age in Second Life was conducted:', 'entirely inside the virtual world, through his avatar',
          ['in a university computer laboratory', 'through an online survey of users', 'by interviewing software developers'], 'He treated Second Life as a field site in its own right.'),
         ('The Why We Post project compared social media use across:', 'nine field sites in different countries',
          ['one town in England', 'two US cities', 'forty online forums'], 'Nine anthropologists worked in nine sites, published in 2016.')],
  why=[('Explain why multi-sited ethnography has become more common.', 'Globalisation, migration and commodity chains mean that social life is spread across places; studying one site would miss the connections that shape people\'s lives, such as migrants\' ties between home and destination.'),
       ('Explain why online worlds can be legitimate field sites.', 'People form real relationships, norms, economies and identities online; participant observation in those spaces reveals social life as it is lived there (Boellstorff).'),
       ('Explain why collaborative ethnography is seen as more ethical.', 'Sharing control over questions, interpretation and writing reduces the researcher\'s power over representation and makes the research more useful and accountable to participants.')],
  contrast=[('single-sited ethnography', 'multi-sited ethnography', 'Single-sited ethnography studies one bounded location in depth; multi-sited ethnography follows connections across locations, gaining breadth but sometimes losing depth in each site.'),
            ('online ethnography', 'offline ethnography', 'Online ethnography studies interaction mediated by digital platforms, where presence, consent and identity are harder to establish; offline ethnography studies face-to-face interaction in physical places. Most research now combines both.')],
  misc=[('Online interactions are not "real" and so cannot be studied ethnographically.', 'Online interaction produces genuine relationships, norms and identities, as Boellstorff and the Why We Post project show.'),
        ('Multi-sited ethnography is simply visiting many places briefly.', 'It is defined by following meaningful connections (people, things, ideas) between sites, and still requires sustained engagement in each.')],
  cases=[('the Why We Post project (2016)', 'Nine anthropologists spent about fifteen months each in sites from Trinidad to rural China studying what people post and why.',
          'comparative digital ethnography', 'it showed that social media are shaped by local cultures, so "the same" platform is used very differently in different places.'),
         ('Holmes\'s research following Triqui migrants', 'Holmes worked with Triqui families in Oaxaca, crossed the border with them, and followed them to farms in Washington and California.',
          'multi-sited ethnography', 'following people across sites revealed connections between village poverty, border policy and farm labour hierarchies that no single site could show.')],
  ev=[('Digital ethnography is as valid as traditional fieldwork.',
       ['online life is real social life with its own norms', 'it reaches dispersed or hidden communities'],
       ['researchers may miss offline contexts that shape online behaviour', 'consent and identity verification are difficult', 'platforms control access and data'],
       'Digital ethnography is valid when it applies the same rigour and links online and offline contexts.'),
      ('Multi-sited ethnography sacrifices depth for breadth.',
       ['less time in each site', 'harder to build rapport everywhere'],
       ['it captures connections central to globalised life', 'depth can be achieved by following the same people across sites (Holmes)'],
       'There is a trade-off, but well-designed multi-sited work gains essential depth about connections.')],
  ext=[('Mariam runs a Facebook group for women from her village who now live in Doha, Milan and Leeds. Each Friday they post photographs of what they have cooked, and the women still in the village comment on whether the dough has been rolled thinly enough. When Mariam\'s cousin in Milan posted a cake bought from a shop, three aunts left the group in protest, then rejoined a week later. Mariam has asked me to help write a booklet of the recipes, "so the girls born abroad will have them". We decided together which recipes and which family names to include.',
        'fieldnotes from an online community linking a Moroccan village with its migrants', 'the activities that take place in the Facebook group',
        'Women post photographs of Friday cooking; village women comment on the quality (thin dough); a shop-bought cake prompted three aunts to leave and later rejoin; Mariam and the anthropologist are co-writing a booklet of recipes for girls born abroad.',
        'how the text illustrates multi-sited and collaborative ethnography', 'The field is spread across a village and three cities, connected online, so the anthropologist follows relationships rather than a place; online food posts maintain belonging and moral judgement across distance; the recipe booklet is collaborative – Mariam and the anthropologist decide together what to include, sharing control over representation.',
        'space', 'Posts in a closed group are not public, so the consent of members (not only the administrator) is needed; photographs and family names in the booklet raise questions of anonymity versus credit; the aunts\' protest is a sensitive family matter.')])

# =============================================================================================
# ch04 Ethics in Anthropology
# =============================================================================================
S('ch04-st1', 'the ethical conduct of fieldwork', ['power', 'social_relations', 'identity'],
  ['bourgois', 'chagnon', 'scheper', 'holmes'],
  terms=[('informed consent', 'the voluntary agreement of participants to take part in research, based on a clear understanding of its purpose, methods, risks and uses; in anthropology it is usually an ongoing process rather than a single signature'),
         ('do no harm', 'the first principle of the AAA Principles of Professional Responsibility (2012): researchers must avoid causing physical, psychological, social, economic or legal harm to participants'),
         ('anonymity', 'protecting participants\' identities, for example by using pseudonyms and disguising places and details so that individuals cannot be recognised'),
         ('confidentiality', 'the commitment not to disclose information shared by participants beyond agreed limits, and to store data securely'),
         ('covert research', 'research in which participants do not know they are being studied; most anthropological codes permit it only in exceptional, justified cases')],
  facts=[('Which of the following is the first principle listed in the AAA Principles of Professional Responsibility (2012)?', 'Do no harm',
          ['Publish quickly', 'Maximise sample size', 'Remain neutral at all times'], 'The AAA statement begins with "Do No Harm".'),
         ('Why do anthropologists often prefer oral, ongoing consent to signed consent forms?', 'Written forms may be confusing or threatening in some settings, and consent must be renegotiated as research develops',
          ['Oral consent is legally binding everywhere', 'Signed forms are banned by the IB', 'Participants never need to understand the research'], 'Consent is a process of continuing negotiation suited to the context.'),
         ('Which professional body publishes Ethical Guidelines for Good Research Practice for anthropologists in the UK and Commonwealth?', 'The Association of Social Anthropologists (ASA)',
          ['The Royal Society', 'UNESCO', 'The British Medical Association'], 'The ASA guidelines were revised in 2011 and 2021.'),
         ('Which scandal of 1964–1965, involving US Army funding of social research on counterinsurgency in Latin America, prompted the AAA to develop its first ethics statement?', 'Project Camelot',
          ['The Human Terrain System', 'The Torres Strait Expedition', 'The Manhattan Project'], 'Project Camelot was cancelled in 1965; the AAA adopted its first Principles of Professional Responsibility in 1971.')],
  why=[('Explain why informed consent in anthropology is described as a process.', 'Fieldwork is long and open-ended; research questions change, new people become involved and relationships deepen, so consent must be revisited and participants must be able to withdraw at any time.'),
       ('Explain why anonymity can be difficult to guarantee in ethnography.', 'Ethnographies describe small communities in rich detail; even with pseudonyms, insiders can recognise people from roles, events or quotations, and online publication makes texts widely accessible.'),
       ('Explain why anthropologists may owe obligations to more than one group.', 'They have duties to participants, colleagues, funders, host governments and the public, which can conflict – e.g. a funder wants information that could harm participants – so the AAA asks them to weigh competing obligations, with participants\' welfare first.')],
  contrast=[('anonymity', 'confidentiality', 'Anonymity means the identity of participants is hidden in the research output; confidentiality means information shared with the researcher is not passed on beyond agreed limits. A participant can be anonymised yet information can still breach confidentiality if shared improperly.'),
            ('overt research', 'covert research', 'In overt research participants know they are being studied and can consent; in covert research they do not, which breaches informed consent and is justified only in exceptional cases such as exposing serious harm.')],
  misc=[('Once a participant signs a consent form, the anthropologist has no further ethical obligations.', 'Consent is ongoing; researchers must protect participants from harm, maintain confidentiality, allow withdrawal and consider the effects of publication long after consent is given.'),
        ('Using pseudonyms always fully protects participants.', 'Pseudonyms reduce but do not remove risk, as insiders may recognise people from details; researchers must also disguise places, change details and consider what to omit.')],
  cases=[('Bourgois\'s fieldwork with crack dealers in East Harlem', 'Bourgois witnessed illegal acts and violence, changed names and details, and reflected on the risk that his descriptions might reinforce negative stereotypes of Puerto Ricans.',
          'competing ethical obligations', 'he had to protect participants from legal harm while still describing violence honestly, and to avoid representations that could harm the wider community.'),
         ('the Havasupai blood-samples case (settled 2010)', 'Blood samples given by members of the Havasupai Tribe in Arizona for diabetes research were later used without consent for studies of schizophrenia, inbreeding and migration origins; Arizona State University settled, paying compensation and returning samples.',
          'the limits of informed consent', 'it shows that consent applies to specific uses; using data for purposes participants did not agree to – especially research contradicting their origin stories – causes real harm.')],
  ev=[('Anthropologists should never carry out covert research.',
       ['covert research breaches informed consent and trust', 'it can damage the reputation of the discipline and future access'],
       ['some harms (e.g. organ trafficking, which Scheper-Hughes investigated partly undercover) can only be exposed covertly', 'in public settings consent from everyone is impossible'],
       'Covert research should be avoided except in rare, carefully justified cases where the public interest is great and harm to participants minimal.'),
      ('Ethical codes such as the AAA principles are sufficient to guide anthropologists in the field.',
       ['they provide clear principles such as do no harm and informed consent', 'they are regularly revised (AAA 2012, ASA 2021)'],
       ['codes are general and fieldwork dilemmas are specific and unpredictable', 'local ideas of consent and harm may differ', 'codes cannot resolve conflicts between obligations'],
       'Codes are necessary guides but must be applied through reflexive judgement in context.')],
  ext=[('The headteacher agreed that I could observe classes at the girls\' school and signed the permission letter. In the staffroom, though, Ms Haddad asked me not to write about her lessons: "If the inspectors read that I speak Arabic in the English class, I lose my job." Two pupils showed me a group chat where they share answers before tests and asked if I would "put it in the book". One of them added, laughing, "Use my real name, I want to be famous." When I returned the following term, a new headteacher knew nothing about my research.',
        'fieldnotes from a secondary school in Jordan', 'the different responses to the research described in the text',
        'The headteacher signed a permission letter; Ms Haddad asked not to be written about, fearing inspectors; two pupils showed a group chat about sharing test answers and asked whether it would be in the book; one wanted her real name used; a new headteacher did not know about the research.',
        'why consent in the text cannot be settled by the headteacher\'s letter alone', 'Gatekeeper permission does not equal consent from each participant: Ms Haddad withdraws consent for her lessons; pupils are minors and their consent requires guardians; the request to use a real name conflicts with protecting a minor from harm; a new headteacher means consent must be renegotiated. Consent is ongoing and relational.',
        'power', 'Do no harm: Ms Haddad\'s job and the pupils\' academic standing could be damaged; minors require parental consent and their wish for fame does not override protection; anonymise the school; renegotiate access with the new headteacher; store chat screenshots securely or not at all.')])

S('ch04-st2', 'relationships of power between researchers and participants', ['power', 'social_relations', 'identity'],
  ['scheper', 'chagnon', 'bourgois', 'briggs'],
  terms=[('reciprocity in fieldwork', 'the expectation that the anthropologist gives something back – time, help, gifts, payment, advocacy or shared results – in return for participants\' time and knowledge'),
         ('representation', 'how people are portrayed in ethnographic texts, images and films, and who has the authority to portray them'),
         ('advocacy', 'the use of anthropological knowledge to support the interests or rights of the people studied'),
         ('vulnerable groups', 'participants such as children, refugees, prisoners or undocumented migrants who face higher risks of harm and need additional protection'),
         ('dual use', 'the possibility that research produced for one purpose may be used by others – such as militaries or corporations – for purposes that harm participants')],
  facts=[('Which US military programme (2007–2014) that embedded social scientists with combat units was condemned by the AAA Executive Board in 2007?', 'The Human Terrain System',
          ['Project Camelot', 'The Marshall Plan', 'The Peace Corps'], 'The AAA argued it could not meet the requirements of informed consent and do no harm.'),
         ('Patrick Tierney\'s book Darkness in El Dorado (2000) made ethical accusations about research among the:', 'Yanomami of Venezuela and Brazil',
          ['Nuer of South Sudan', 'Trobriand Islanders', 'Azande'], 'It concerned Napoleon Chagnon and geneticist James Neel.'),
         ('Nancy Scheper-Hughes\'s idea of the "primacy of the ethical" (1995) argues that anthropologists should:', 'be morally engaged witnesses rather than neutral observers',
          ['avoid all political issues', 'prioritise publication over participants', 'study only their own society'], 'She called for a "militant" or engaged anthropology.')],
  why=[('Explain why reciprocity raises ethical questions in fieldwork.', 'Giving back is fair, but gifts or payments can create dependence, distort relations or behaviour (Chagnon\'s steel tools were criticised for fuelling rivalry), and the researcher has greater resources, so the form of reciprocity must be considered carefully.'),
       ('Explain why representation is an ethical issue as well as a methodological one.', 'How people are portrayed can affect how they are treated by states, media and outsiders: an image of a group as "fierce" or "deviant" can justify discrimination, land seizure or policing.'),
       ('Explain why power imbalances between the anthropologist and participants matter.', 'Researchers usually control the questions, the writing and the benefits (careers, publications), while participants bear the risks; recognising this imbalance underpins consent, reciprocity and collaborative approaches.')],
  contrast=[('engaged (advocacy) anthropology', 'detached anthropology', 'Engaged anthropology uses research to support participants\' rights and interests (Scheper-Hughes, Farmer); detached anthropology aims to remain neutral to preserve objectivity. Critics of detachment argue neutrality can mean complicity, while critics of advocacy fear bias.'),
            ('reciprocity', 'payment', 'Reciprocity is a broad, relational obligation to give back in culturally appropriate ways (help, gifts, shared results); payment is a monetary transaction that may be fair but can turn participation into employment and influence what people say.')],
  misc=[('Giving gifts to participants is always ethical because it repays them.', 'Gifts can create dependence, inequality or conflict and can shape what people tell the researcher, so their form and effects must be considered.'),
        ('Advocacy is incompatible with good anthropology.', 'Many anthropologists argue engaged research can be rigorous; Farmer and Scheper-Hughes combine detailed ethnography with advocacy, though they must be transparent about their positions.')],
  cases=[('the Yanomami controversy following Darkness in El Dorado (2000)', 'Critics accused Chagnon of portraying the Yanomami as "fierce" and of distributing steel goods that intensified conflict; Yanomami leaders later demanded the return of blood samples taken in the 1960s.',
          'the ethics of representation and reciprocity', 'it shows how gifts, consent and the image of a people in widely read texts can affect their relations and political position, and how communities now challenge researchers.'),
         ('the Human Terrain System (2007–2014)', 'Social scientists embedded with US military units in Iraq and Afghanistan gathered cultural information for commanders.',
          'dual use and do no harm', 'information given to the military could be used to target people, and consent was compromised in a war zone; the AAA judged participation incompatible with its ethics.')],
  ev=[('Anthropologists have a duty to act as advocates for the people they study.',
       ['researchers witness suffering and have a voice participants may lack (Scheper-Hughes, Farmer)', 'neutrality in the face of injustice can be complicity'],
       ['communities are divided, so whose interests are advocated?', 'advocacy may bias research or endanger participants', 'participants may not want an advocate'],
       'Anthropologists have a duty not to harm and often a responsibility to engage, but advocacy should be negotiated with participants and transparent.'),
      ('It is impossible to represent another people fairly.',
       ['the writer\'s authority and selection always shape the account (Writing Culture)', 'audiences may read texts through stereotypes'],
       ['collaboration, reflexivity and multiple voices improve fairness', 'insider and Indigenous anthropologists challenge outsider representations'],
       'Perfect fairness is unattainable, but collaborative and reflexive methods can make representation more accountable.')],
  ext=[('Every evening, Nadia brings me tea and asks about visas. She knows I have a British passport, and her son wants to study in London. At first I answered vaguely; then I helped him complete an online application. Since then, Nadia introduces me to neighbours as "the one who helps with papers", and three families have asked me for the same help. When I wrote about a dispute between Nadia and her brother over the family land, she asked to read my notes. I hesitated: her brother had told me his side in confidence.',
        'fieldnotes from a neighbourhood in Amman, Jordan, during research with Syrian refugee families', 'what Nadia and her neighbours expect from the anthropologist',
        'Nadia asks about visas because of the British passport; after the anthropologist helped her son apply, she introduced the anthropologist as "the one who helps with papers"; three families asked for the same help; Nadia asked to read the field notes about her land dispute.',
        'how the anthropologist\'s help creates ethical dilemmas of reciprocity and power', 'Helping with the visa is a form of reciprocity but changes the anthropologist\'s role and status ("the one who helps with papers"), raises expectations that cannot be met for every family and may influence what people say. Nadia\'s request to read notes conflicts with the confidence of her brother, so obligations to different participants clash.',
        'social_relations', 'Refugees are vulnerable: do no harm, avoid raising false hopes about visas, keep the brother\'s confidence, explain clearly the limits of the researcher\'s role, protect identities of families with uncertain legal status, and consider sharing findings in ways that do not expose internal disputes.')])

S('ch04-st3', 'the representation of colonised peoples', ['power', 'classification', 'change'],
  ['nuer', 'dirks', 'boas', 'simpson', 'wolf'],
  terms=[('colonialism', 'the political, economic and cultural domination of one people by another, typically through conquest and settlement, as in European empires from the fifteenth to twentieth centuries'),
         ('Orientalism', 'Edward Said\'s term (1978) for Western representations that portrayed "the Orient" as exotic, backward and unchanging, justifying domination'),
         ('decolonising anthropology', 'efforts to confront the discipline\'s colonial legacies by centring the knowledge, voices and control of formerly colonised and Indigenous peoples'),
         ('repatriation', 'the return of human remains, sacred objects or cultural property from museums and collections to the communities from which they were taken'),
         ('salvage anthropology', 'early twentieth-century research that aimed to record cultures assumed to be disappearing, often presenting them as frozen in the past')],
  facts=[('Who edited Anthropology and the Colonial Encounter (1973), which examined anthropology\'s relationship with colonial rule?', 'Talal Asad',
          ['Edward Said', 'Clifford Geertz', 'Eric Wolf'], 'Asad\'s volume critically analysed British social anthropology in the colonial context.'),
         ('Which 1990 US law requires museums to return Native American human remains and sacred objects to tribes?', 'The Native American Graves Protection and Repatriation Act (NAGPRA)',
          ['The Indian Removal Act', 'The Dawes Act', 'The Civil Rights Act'], 'NAGPRA (1990) established repatriation procedures.'),
         ('Evans-Pritchard\'s research among the Nuer was originally requested by:', 'the government of the Anglo-Egyptian Sudan',
          ['the Nuer prophets', 'the United Nations', 'the American Anthropological Association'], 'The administration wanted knowledge of a people who had resisted colonial rule.'),
         ('Vine Deloria Jr\'s Custer Died for Your Sins (1969) is known for:', 'a Native American critique of anthropologists who studied Indigenous peoples without benefiting them',
          ['a history of the Battle of the Little Bighorn', 'a defence of salvage anthropology', 'a guide to collaborative methods'], 'His chapter "Anthropologists and Other Friends" was widely influential.')],
  why=[('Explain why anthropology has been described as "the child of colonialism".', 'The discipline developed as European empires expanded: colonial administrations funded or used research, fieldwork depended on colonial access and security, and early theories (e.g. evolutionism) ranked colonised peoples as inferior.'),
       ('Explain why repatriation of museum collections is an ethical issue for anthropologists.', 'Many objects and human remains were taken under colonial conditions without consent; keeping them continues that injustice, while returning them acknowledges communities\' rights over their heritage and ancestors.'),
       ('Explain why the "ethnographic present" has been criticised.', 'Writing in the present tense about past fieldwork presents societies as timeless and unchanging, ignoring colonial history and change, and so reproduces an image of "people without history" (Wolf).')],
  contrast=[('salvage anthropology', 'decolonising anthropology', 'Salvage anthropology recorded cultures believed to be vanishing, usually by outsiders for outside audiences; decolonising anthropology seeks to shift authority to the communities themselves and to analyse colonial power rather than freezing cultures in time.'),
            ('Orientalism', 'cultural relativism', 'Orientalism represents others as exotic and inferior, serving domination; cultural relativism seeks to understand others in their own terms without ranking, although critics note relativism can also exoticise.')],
  misc=[('Colonialism is only a historical issue with no relevance to anthropology today.', 'Colonial legacies persist in museum collections, unequal research relations, global inequality and representations of formerly colonised peoples, so they shape current ethics.'),
        ('All early anthropologists simply served colonial governments.', 'Relations varied: some worked for administrations, others (like Boas) challenged racism, and many were ambivalent; Asad stresses structural complicity rather than individual intent.')],
  cases=[('the Benin Bronzes', 'Thousands of brass and ivory works were looted from Benin City by a British punitive expedition in 1897 and dispersed to European museums; several institutions began returning them in the 2020s.',
          'colonial power and the ethics of representation', 'museum displays long presented the objects as "primitive art" divorced from the violence of their acquisition; repatriation debates show communities reclaiming control over their heritage.'),
         ('Dirks\'s analysis of the colonial census in India', 'British censuses from 1871–1872 recorded and ranked castes and became a basis for administration.',
          'how colonial knowledge produced classifications', 'anthropological and administrative knowledge did not merely describe caste; it helped to fix and rank it, showing knowledge as a form of power.')],
  ev=[('Anthropology cannot escape its colonial origins.',
       ['inequalities in funding, publishing and access persist', 'museums still hold colonial collections', 'representations of "others" still dominate'],
       ['Indigenous and Global South anthropologists reshape the discipline (Simpson, Tuhiwai Smith)', 'collaborative and decolonising methods redistribute authority', 'anthropology has also critiqued colonialism and racism (Boas, Asad, Wolf)'],
       'Its colonial legacy remains, but the discipline has developed tools to confront it; escape requires ongoing structural change, not just self-critique.'),
      ('Museums should return all objects acquired during the colonial period.',
       ['many were taken by force or under unequal conditions', 'communities have rights to their heritage and ancestors'],
       ['some objects were traded or commissioned legitimately', 'communities may prefer loans, shared stewardship or digital access', 'decisions should be made with source communities'],
       'Return should be the default where acquisition was coercive, but the form of restitution should be decided with source communities.')],
  ext=[('In the museum\'s storeroom, the curator unwrapped a carved house post. The label from 1911 read: "Idol of a vanished tribe." Mere, an elder from the iwi that had travelled to view it, laid her hand on the wood and spoke to it for several minutes before speaking to us. "He is not vanished," she said. "He is our ancestor and we are here." The curator explained that the trustees would need a formal claim and provenance research. Mere\'s nephew filmed the encounter on his phone; later he posted it with the caption: "Visiting our tupuna in prison."',
        'fieldnotes from a European museum storeroom during a visit by a Māori delegation', 'how the different people in the text treat the carved post',
        'The 1911 label calls it an "idol of a vanished tribe"; Mere touches and speaks to it as an ancestor; the curator treats it as an object requiring a formal claim and provenance research; the nephew films it and posts it as "visiting our tupuna in prison".',
        'how the text reveals the colonial legacy of anthropological classification', 'The 1911 label reflects salvage anthropology and colonial classification (idol, vanished tribe), denying the iwi\'s continued existence; Mere\'s emic view classifies the post as a living ancestor; the curator\'s bureaucratic procedures show institutional power over heritage; the nephew\'s caption reframes the museum as a prison, contesting representation and asserting change.',
        'classification', 'The encounter is sacred and emotional; the anthropologist needs consent from the delegation and the museum, should follow the iwi\'s protocols about images of ancestors, avoid publishing film without permission, and consider supporting the repatriation claim.')])

# =============================================================================================
# ch05 Anthropological Thought: Theories and Paradigms
# =============================================================================================
S('ch05-st1', 'early explanations of cultural difference', ['culture', 'classification', 'change'],
  ['morgan', 'boas', 'mead', 'wolf'],
  terms=[('unilineal evolutionism', 'the nineteenth-century theory that all societies progress through the same fixed sequence of stages, from "savagery" to "civilisation"'),
         ('diffusionism', 'the theory that cultural traits spread mainly by borrowing and migration from a few centres of invention, rather than being invented independently'),
         ('historical particularism', 'Franz Boas\'s approach that each culture is the product of its own particular history and must be studied on its own terms'),
         ('psychic unity of mankind', 'the idea, held by evolutionists such as Tylor, that all humans share the same mental capacities, so similar stages arise independently'),
         ('armchair anthropology', 'the practice of nineteenth-century scholars who theorised from missionaries\' and travellers\' reports rather than doing fieldwork themselves')],
  facts=[('In Ancient Society (1877), Lewis Henry Morgan divided human history into which stages?', 'Savagery, barbarism and civilisation',
          ['Hunting, herding and farming', 'Band, tribe and state', 'Feudalism, capitalism and socialism'], 'Morgan\'s scheme ranked societies by technological inventions.'),
         ('Which anthropologist argued in "The Limitations of the Comparative Method of Anthropology" (1896) against evolutionary schemes?', 'Franz Boas',
          ['E. B. Tylor', 'Herbert Spencer', 'Grafton Elliot Smith'], 'Boas argued that similar traits can have different histories.'),
         ('Grafton Elliot Smith is associated with the "heliocentric" diffusionist claim that civilisation spread from:', 'ancient Egypt',
          ['ancient Greece', 'China', 'the Andes'], 'This extreme diffusionism was soon discredited.')],
  why=[('Explain why unilineal evolutionism has been rejected by modern anthropologists.', 'It ranked societies on a single scale with Europe at the top, assumed a fixed sequence that ethnography contradicts, ignored the histories and connections of peoples, and justified colonial rule.'),
       ('Explain why Boas\'s historical particularism changed the direction of American anthropology.', 'By insisting on detailed fieldwork, the study of each culture\'s history and the rejection of racial and evolutionary rankings, Boas established cultural relativism and trained a generation (Mead, Benedict, Hurston) who studied culture rather than "race".'),
       ('Explain why diffusionism, despite its exaggerations, contained an important insight.', 'It recognised that societies are connected and borrow ideas and technologies from one another, an insight later developed in studies of globalisation and in Wolf\'s critique of isolated societies.')],
  contrast=[('evolutionism', 'historical particularism', 'Evolutionism assumes all societies pass through universal stages and can be ranked; historical particularism holds that each culture has its own unique history and cannot be ranked on a single scale.'),
            ('diffusionism', 'independent invention', 'Diffusionism explains similar traits by borrowing and migration from a common source; independent invention explains them as separate responses arising in different places.')],
  misc=[('Evolutionist anthropologists based their theories on long-term fieldwork.', 'Most were "armchair" scholars who relied on reports by missionaries, traders and administrators; Morgan was a partial exception with his Haudenosaunee work.'),
        ('Boas believed that cultures could be ranked from simple to complex.', 'Boas rejected ranking cultures and argued that each must be understood in its own historical context.')],
  cases=[('Boas\'s study of immigrants\' children in New York (1910–1912)', 'Measurements showed that children of immigrants born in the United States differed in head shape from their parents.',
          'the critique of racial classification', 'the findings undermined the assumption that "racial" types were fixed, supporting Boas\'s argument that culture and environment, not race, explain human differences.'),
         ('Morgan\'s research with the Haudenosaunee (Iroquois)', 'Morgan studied Seneca kinship and political organisation and compared kinship terminologies worldwide.',
          'evolutionism', 'his data were valuable, but he fitted societies into a sequence of stages, ranking the Haudenosaunee in "barbarism", illustrating the strengths and flaws of evolutionism.')],
  ev=[('Nineteenth-century evolutionism has nothing to offer anthropology today.',
       ['its ranking of societies was ethnocentric and served colonialism', 'ethnography refuted fixed stages'],
       ['it asked big comparative questions about long-term change', 'Morgan founded kinship studies', 'neo-evolutionists (White, Steward) developed more careful models of cultural ecology'],
       'Its racist ranking must be rejected, but its comparative ambition and some data remain useful.'),
      ('Boas was the most important figure in the history of anthropology.',
       ['he established cultural relativism and the critique of scientific racism', 'his students shaped American anthropology'],
       ['Malinowski established modern fieldwork in Britain', 'Lévi-Strauss and Geertz transformed theory', 'importance depends on national tradition'],
       'Boas was foundational for American anthropology and the critique of racism, though others shaped method and theory elsewhere.')],
  ext=[('In the regional museum, the 1930s display still stands in the hall: glass cases arranged in a line from "Stone Age Hunters" through "Primitive Farmers" to "Modern Civilisation", which ends with a model of a steam train. Schoolchildren walk past it on the way to the cafe. The new curator, Dr Achieng, has added handwritten cards: "These people were our grandparents\' neighbours, not our ancestors from the Stone Age." A teacher told me she uses the display "to show how wrong we used to be". The museum board has not yet agreed to remove it.',
        'fieldnotes from a regional museum in East Africa', 'how the museum display is arranged and used',
        'Glass cases arranged in a line from "Stone Age Hunters" to "Primitive Farmers" to "Modern Civilisation", ending with a steam train; schoolchildren pass on the way to the cafe; the curator has added handwritten cards challenging it; a teacher uses it to show past errors; the board has not agreed to remove it.',
        'how the display reflects nineteenth-century evolutionist thinking and how it is being challenged', 'The linear sequence ranks contemporary peoples as earlier stages of humanity and places industrial Europe (the train) at the summit – classic unilineal evolutionism. The curator\'s cards insist these peoples were contemporaries (coeval), in the spirit of Boas and Wolf; the teacher turns the display into a lesson about the history of ideas, while the board\'s reluctance shows institutional power over representation.',
        'classification', 'Descendants of the people displayed may be offended; the anthropologist should seek consent from staff and consider how criticism of the board may affect the curator\'s position; representation of communities in the display raises questions of who should be consulted.')])

S('ch05-st2', 'the maintenance of social order', ['society', 'social_relations', 'culture'],
  ['malinowski', 'radcliffe', 'nuer', 'azande'],
  terms=[('functionalism', 'Malinowski\'s theory that cultural institutions exist to satisfy basic biological and psychological needs of individuals'),
         ('structural-functionalism', 'Radcliffe-Brown\'s theory that institutions function to maintain the social structure and the stability of society as a whole'),
         ('social structure (Radcliffe-Brown)', 'the network of actually existing social relations between persons, ordered by institutions and roles'),
         ('equilibrium', 'the assumed state of balance or stability that functionalist theories believed societies tend to maintain'),
         ('synchronic analysis', 'the study of a society at one point in time, typical of functionalism, rather than diachronic study of change over time')],
  facts=[('Which anthropologist argued that culture responds to individuals\' basic needs such as food, shelter and reproduction?', 'Bronisław Malinowski',
          ['A. R. Radcliffe-Brown', 'Franz Boas', 'Claude Lévi-Strauss'], 'Malinowski\'s functionalism centred on human needs.'),
         ('Radcliffe-Brown compared society to:', 'a living organism whose parts maintain the whole',
          ['a machine built by individuals', 'a text to be read', 'a language with grammar'], 'The organic analogy is central to structural-functionalism.'),
         ('A common criticism of functionalism is that it:', 'cannot explain social change and conflict well',
          ['relied too heavily on statistics', 'ignored fieldwork', 'focused only on individuals\' emotions'], 'Its synchronic focus on equilibrium neglects history and change.'),
         ('According to Malinowski, why did Trobrianders use magic for deep-sea fishing but not for lagoon fishing?', 'Deep-sea fishing was dangerous and uncertain, so magic reduced anxiety',
          ['Lagoon fish were sacred', 'Magic was forbidden in the lagoon', 'Only chiefs fished in the deep sea'], 'In Magic, Science and Religion (1925/1948) magic answers uncertainty.')],
  why=[('Explain why functionalism was an advance over evolutionism.', 'It explained institutions by their present role in a living society, based on fieldwork, rather than as survivals from earlier stages, and it showed that apparently strange customs made sense in context.'),
       ('Explain why structural-functionalism has difficulty explaining change.', 'By assuming institutions maintain equilibrium, it treats conflict as dysfunction and studies societies synchronically, so it underplays history, colonialism and internal contestation that drive change.'),
       ('Explain why Evans-Pritchard\'s The Nuer is often seen as a structural-functionalist ethnography.', 'It shows how segmentary lineages, age-sets and feud mechanisms maintain order without a state, explaining institutions by their contribution to social structure.')],
  contrast=[('Malinowski\'s functionalism', 'Radcliffe-Brown\'s structural-functionalism', 'Malinowski explained institutions by the individual biological and psychological needs they satisfy; Radcliffe-Brown explained them by their role in maintaining the social structure as a whole.'),
            ('a synchronic approach', 'a diachronic approach', 'A synchronic approach studies a society as a system at one moment; a diachronic approach studies it through time, emphasising history and change.')],
  misc=[('Functionalists believed every custom is good for every individual.', 'Functionalists claimed institutions contribute to social stability or meet needs, not that they benefit everyone; critics note that the theory can hide inequality.'),
        ('Functionalism has no influence on anthropology today.', 'Its emphasis on holism, fieldwork and the interconnection of institutions remains central, even though its equilibrium model has been abandoned.')],
  cases=[('Malinowski\'s analysis of Trobriand fishing magic', 'Trobrianders performed elaborate magic before dangerous open-sea fishing but not for safe lagoon fishing.',
          'functionalism', 'magic met the psychological need to manage anxiety in uncertain situations, illustrating Malinowski\'s needs-based explanation.'),
         ('Evans-Pritchard\'s The Nuer (1940)', 'Nuer lineages fused against outsiders and split in internal disputes, with leopard-skin chiefs mediating feuds.',
          'structural-functionalism', 'the segmentary system is analysed as maintaining order without a state, explaining institutions by their contribution to social structure.')],
  ev=[('Functionalism presents an overly harmonious picture of society.',
       ['the equilibrium model treats conflict as dysfunction', 'it ignored colonial power that shaped the societies studied', 'it struggles with change'],
       ['Max Gluckman (Manchester School) showed conflict can be functional, e.g. rituals of rebellion', 'its holism explained how institutions interconnect'],
       'Functionalism did often over-emphasise harmony, but later functionalists began to analyse conflict and its holistic insights endure.'),
      ('Malinowski\'s contribution to method was more important than his theory.',
       ['his model of long-term participant observation defines the discipline', 'his functionalist theory has been largely abandoned'],
       ['his theory encouraged holistic analysis', 'method and theory were linked: needs-based theory led him to observe daily life'],
       'His methodological legacy is greater, though his theory shaped how that method was used.')],
  ext=[('In the village, every household sends a son to the annual repair of the irrigation channel. Nobody is paid. The work lasts three days and ends with a feast at which the eldest man of each lineage receives the first portion of meat. Thabo, home from his job in Johannesburg, paid a cousin to go in his place this year. The elders accepted the money but placed Thabo\'s family last in the line for the feast. "The channel brings water to all," the headman told me. "When a family does not dig, the water still comes, but the respect does not."',
        'fieldnotes from a rural village in Lesotho', 'what happens during the annual repair of the irrigation channel',
        'Every household sends a son; the work is unpaid and lasts three days; it ends with a feast; the eldest man of each lineage receives the first portion; Thabo paid a cousin to go in his place; his family was placed last in the line for the feast.',
        'how a functionalist might explain the channel repair, and what the text suggests about the limits of that explanation', 'A functionalist would argue the collective work meets the material need for water (Malinowski) and maintains social structure and solidarity, with the feast reaffirming lineage seniority (Radcliffe-Brown). But Thabo\'s substitution shows change from migrant wage labour and money entering obligations, and the sanction on his family shows tension and negotiation that an equilibrium model underplays.',
        'society', 'Thabo\'s family may be shamed if identified; the headman\'s statement about respect could affect village relations; anonymise the village and individuals and consider how migrants and elders might read the account.')])

S('ch05-st3', 'the meanings of myth, ritual and symbols', ['culture', 'classification', 'power'],
  ['levistrauss', 'geertz', 'turner', 'douglas'],
  terms=[('structuralism', 'Lévi-Strauss\'s approach seeking the universal, unconscious structures of the human mind, especially binary oppositions, beneath myths, kinship and classification'),
         ('binary opposition', 'a pair of contrasting categories, such as nature/culture or raw/cooked, through which, according to structuralists, humans order experience'),
         ('interpretive anthropology', 'Geertz\'s approach treating culture as public systems of symbols and meaning to be interpreted, like texts, through thick description'),
         ('multivocality', 'Victor Turner\'s term for the capacity of a dominant symbol to carry many meanings at once'),
         ('liminality', 'the in-between phase of a rite of passage, when participants have left one status but not yet entered the next (van Gennep, Turner)')],
  facts=[('Which anthropologist wrote The Raw and the Cooked (1964)?', 'Claude Lévi-Strauss',
          ['Clifford Geertz', 'Mary Douglas', 'Victor Turner'], 'It is the first volume of his Mythologiques.'),
         ('Geertz\'s phrase "thick description" was borrowed from the philosopher:', 'Gilbert Ryle',
          ['Ferdinand de Saussure', 'Karl Marx', 'Michel Foucault'], 'Ryle distinguished a twitch from a wink using thin and thick description.'),
         ('Victor Turner\'s ethnographic research on ritual symbols was carried out among the:', 'Ndembu of Zambia',
          ['Nuer of Sudan', 'Azande', 'Kabyle of Algeria'], 'Turner worked among the Ndembu in the 1950s.')],
  why=[('Explain why Lévi-Strauss focused on binary oppositions.', 'Drawing on structural linguistics, he argued that meaning arises from contrasts, so the human mind classifies by opposing categories (nature/culture, raw/cooked); myths work through and mediate these oppositions.'),
       ('Explain why Geertz argued that anthropology is "not an experimental science in search of law but an interpretive one in search of meaning".', 'Human action is meaningful within a culture\'s webs of significance; the task is to interpret what actions mean to those involved, like reading a text, rather than to discover universal laws.'),
       ('Explain why interpretive anthropology has been criticised for neglecting power.', 'By treating culture as a shared text, it can ignore who controls meanings, whose interpretations prevail and how symbols serve inequality; Talal Asad and William Roseberry raised such criticisms.')],
  contrast=[('structuralism', 'interpretive anthropology', 'Structuralism seeks universal, unconscious mental structures beneath cultural forms; interpretive anthropology seeks the particular, conscious meanings that symbols hold for specific people in specific contexts.'),
            ('thin description', 'thick description', 'Thin description records observable behaviour (a contraction of the eyelid); thick description interprets its meaning in context (a wink, a parody of a wink), which requires understanding the cultural codes involved.')],
  misc=[('Structuralists studied what individual people consciously think about their myths.', 'Structuralists sought unconscious structures of thought that people are usually unaware of, revealed by comparing many myths.'),
        ('Thick description means writing very long, detailed accounts of behaviour.', 'Thick description means interpreting the layered meanings of actions in context, not merely adding detail.')],
  cases=[('Geertz\'s "Deep Play"', 'Geertz analysed the cockfight as a text in which Balinese men dramatise status rivalries.',
          'interpretive anthropology', 'the cockfight is read as a symbolic story about status hierarchy rather than explained by function or gambling.'),
         ('Turner\'s analysis of the Ndembu milk tree (mudyi)', 'The milk tree, which exudes white latex, is central in girls\' puberty rites.',
          'multivocal symbols', 'the tree stands simultaneously for breast milk, motherhood, matrilineal descent and Ndembu unity, showing how one symbol condenses many meanings.')],
  ev=[('Structuralism tells us more about the anthropologist\'s mind than about the people studied.',
       ['binary oppositions may be imposed by the analyst', 'it ignores emic meanings and history'],
       ['comparative evidence shows recurring oppositions across cultures', 'it revealed logical patterns in myth and kinship that were not obvious'],
       'Structuralism risks imposing analytic categories, but it provided powerful comparative insights.'),
      ('Interpretive anthropology is more useful than structuralism.',
       ['it is grounded in specific ethnographic contexts', 'it attends to people\'s own meanings'],
       ['structuralism allows broad comparison', 'interpretive approaches can neglect power and variation within a culture'],
       'Interpretive anthropology is more context-sensitive, but both have limits and complement attention to power.')],
  ext=[('At the wedding in Izmir, the bride\'s family serves rice with pine nuts and the groom\'s family brings roasted lamb. Aunt Fatma explains: "Rice is for the house, meat is for the guests." The henna night before the wedding is only for women; the bride\'s hands are painted while the older women sing laments about a daughter leaving her mother. The bride, Elif, a software engineer, laughed during the songs, then cried. "I live ten minutes away," she told me. "But tonight I am leaving forever."',
        'fieldnotes from a wedding in western Turkey', 'the food and ritual practices described in the text',
        'The bride\'s family serves rice with pine nuts; the groom\'s family brings roasted lamb; Fatma says rice is for the house and meat for guests; the henna night is for women only; the bride\'s hands are painted while older women sing laments; Elif laughed and then cried.',
        'how a structuralist and an interpretive anthropologist might each analyse the wedding', 'A structuralist would identify binary oppositions: rice/meat, house/guests, bride\'s side/groom\'s side, women\'s henna night/public wedding, staying/leaving – mental structures organising the ritual. An interpretive anthropologist would read the henna night as a text about a daughter\'s transition, using Elif\'s laughter and tears and her words ("tonight I am leaving forever") to interpret its emotional, symbolic meaning despite living ten minutes away.',
        'culture', 'Weddings are family occasions; the anthropologist needs the family\'s permission to observe the women-only henna night and to quote Elif\'s emotional moment; photographs of women may be sensitive; anonymity of the family is needed.')])

S('ch05-st4', 'inequality and everyday practice', ['power', 'change', 'identity'],
  ['wolf', 'ortner', 'bourdieu', 'weiner', 'scott'],
  terms=[('political economy', 'an approach, influenced by Marx, that analyses culture in relation to production, class and global relations of power and exchange'),
         ('mode of production', 'Eric Wolf\'s (from Marx) concept for the way labour is mobilised and organised, such as kin-ordered, tributary or capitalist'),
         ('habitus', 'Pierre Bourdieu\'s term for the durable, embodied dispositions, acquired through upbringing, that shape how people perceive and act'),
         ('practice theory', 'an approach, associated with Bourdieu, Giddens and Ortner, that examines how social structures are reproduced and changed through people\'s everyday practices'),
         ('cultural capital', 'Bourdieu\'s term for culturally valued knowledge, skills and tastes that confer advantage, such as education or "good taste"')],
  facts=[('Who wrote Europe and the People Without History (1982)?', 'Eric Wolf',
          ['Sherry Ortner', 'Pierre Bourdieu', 'Michel Foucault'], 'Wolf traced the integration of the world\'s peoples into capitalism.'),
         ('Sherry Ortner\'s essay "Is Female to Male as Nature Is to Culture?" argued that:', 'women\'s lower status is linked to their symbolic association with nature',
          ['women are biologically weaker than men', 'gender roles are identical in all cultures', 'matriarchies were once universal'], 'She proposed a symbolic explanation of gender inequality.'),
         ('Bourdieu\'s theory of practice drew on his fieldwork among the:', 'Kabyle of Algeria',
          ['Nuer of Sudan', 'Trobriand Islanders', 'Ndembu of Zambia'], 'His analysis of the Kabyle house is famous.'),
         ('Annette Weiner\'s Women of Value, Men of Renown (1976) is an example of a feminist critique because it:', 'revealed women\'s exchange and power that Malinowski had overlooked',
          ['argued women should not do fieldwork', 'studied only men\'s kula exchange', 'rejected participant observation'], 'It restudied the Trobriands from women\'s perspective.')],
  why=[('Explain why Marxist anthropologists insisted on the importance of history and global connection.', 'They argued that local cultures are shaped by relations of production and by incorporation into capitalism, colonialism and trade, so analysing a society as isolated and timeless misses the causes of its forms and inequalities (Wolf).'),
       ('Explain why feminist anthropology criticised earlier ethnographies.', 'Early ethnographies were mostly written by men from male informants, treating men\'s activities as "society" and women as marginal; feminist restudies (Weiner) showed women\'s roles, power and perspectives had been missed.'),
       ('Explain why Bourdieu\'s concept of habitus helps explain the reproduction of inequality.', 'Habitus makes social dispositions feel natural, so people tend to act in ways that fit their position (e.g. "choosing" what is realistic), reproducing class and gender hierarchies without explicit coercion.')],
  contrast=[('structure', 'agency', 'Structure is the set of enduring social patterns and constraints; agency is the capacity of people to act and change them. Practice theory sees each as produced through the other.'),
            ('Marxist anthropology', 'interpretive anthropology', 'Marxist anthropology explains culture through material production, class and power; interpretive anthropology explains culture as systems of meaning to be read; the first asks whose interests culture serves, the second what it means.')],
  misc=[('Feminist anthropology is only about studying women.', 'Feminist anthropology analyses gender as a system of power affecting everyone, including masculinity, and questions male bias in theory and method.'),
        ('Practice theory claims that individuals are completely free to choose their actions.', 'Practice theory stresses that action is shaped by habitus and structure, even though it can also reproduce or transform them.')],
  cases=[('Bourdieu\'s analysis of the Kabyle house', 'The house is divided by oppositions such as light/dark, high/low, male/female, and daily movement through it follows these divisions.',
          'habitus and the embodiment of power', 'children absorb the gender order through bodily routines in space, so domination becomes taken for granted.'),
         ('Wolf\'s account of the North American fur trade', 'Indigenous groups reorganised hunting, alliances and settlement around supplying furs to European traders.',
          'political economy', 'what earlier anthropologists described as "traditional" culture was shaped by participation in global capitalism.')],
  ev=[('Marxist approaches explain culture better than interpretive approaches.',
       ['they reveal inequality and global connections (Wolf)', 'they explain change'],
       ['they may reduce meaning to economics', 'interpretive approaches capture what practices mean to participants (Geertz)'],
       'Each explains different aspects; the strongest analyses combine meaning with political economy.'),
      ('Ortner\'s nature/culture argument successfully explains gender inequality.',
       ['it identified a widespread symbolic pattern', 'it stimulated feminist theory'],
       ['the nature/culture opposition is itself a Western construct (MacCormack and Strathern, 1980)', 'gender status varies widely (Weiner, Sanday)', 'Ortner later revised her view'],
       'It was influential but too universal; gender inequality must be explained in specific historical and cultural contexts.')],
  ext=[('At the call centre in Pune, the trainers teach new staff to "neutralise" their accents and to choose an English name for the night shift. Rohan becomes "Ryan" at 9 p.m. The best performers win vouchers for coffee shops where, Rohan tells me, he would not have felt comfortable two years ago. His father, a retired railway clerk, calls the job "selling your sleep to America". Rohan sends half his salary home and has bought his mother a washing machine. "Ryan pays for it," he laughs, "Rohan enjoys it."',
        'fieldnotes from a call centre in India', 'the changes the call centre job brings to Rohan\'s life',
        'He trains to neutralise his accent and uses the name "Ryan" on the night shift; he wins vouchers and feels comfortable in coffee shops he previously avoided; he sends half his salary home and bought his mother a washing machine; his father criticises the job as "selling your sleep to America".',
        'how Marxist and practice-theory approaches could analyse Rohan\'s experience', 'A Marxist approach highlights global capitalism: Indian workers sell labour time (night shifts) to US firms, and their accents and names are disciplined to serve foreign customers. Practice theory highlights how Rohan\'s habitus is reshaped (new tastes, cultural capital, comfort in coffee shops) and how he uses agency, splitting identities ("Ryan pays… Rohan enjoys") to gain resources for his family, partly reproducing and partly transforming class position.',
        'power', 'Employer surveillance and confidentiality agreements mean Rohan could lose his job if identified; the company should not be named without permission; family comments are private; consent should cover how his dual identity is presented.')])

# =============================================================================================
# ch06 Reading Ethnography: Analysing Ethnographic Texts
# =============================================================================================
S('ch06-st1', 'how ethnographers build their arguments', ['culture', 'power', 'identity'],
  ['bourgois', 'scheper', 'holmes', 'abulughod', 'ong'],
  terms=[('ethnographic context', 'the people, place, time and wider social, political and economic setting in which an ethnography was carried out'),
         ('research question', 'the central problem or puzzle an ethnographer sets out to investigate, which shapes what is observed and how it is analysed'),
         ('argument (thesis)', 'the main claim an ethnographer makes on the basis of their evidence, often in dialogue with existing theory'),
         ('evidence', 'the observations, quotations, case histories, images and other data an ethnographer uses to support the argument'),
         ('interlocutor', 'a term increasingly used instead of "informant" for the people with whom an anthropologist works and converses')],
  facts=[('When summarising an ethnography for IB Paper 2, which details establish its context?', 'The author, the people studied, the place and the time of the fieldwork',
          ['The publisher, the price and the page count', 'Only the title and the author', 'The anthropologist\'s home address'], 'Context means who, where and when, plus the wider setting.'),
         ('What is the main argument of Bourgois\'s In Search of Respect?', 'Crack dealing and street culture are responses to structural marginalisation, but they also become self-destructive',
          ['Crack dealers are biologically prone to violence', 'Puerto Rican culture causes drug use', 'The drug trade has no link to the economy'], 'Bourgois combines political economy with attention to culture.'),
         ('Which method did Seth Holmes rely on most for Fresh Fruit, Broken Bodies?', 'Participant observation as a berry picker and migrant',
          ['A national survey of farmworkers', 'Archival research only', 'Laboratory testing of pesticides'], 'He worked and lived alongside Triqui pickers.')],
  why=[('Explain why it is important to identify an ethnographer\'s research question.', 'The question determines what the ethnographer looked for, which methods they used and what they may have overlooked, so it helps readers evaluate the evidence and compare ethnographies fairly.'),
       ('Explain why an ethnography\'s argument must be distinguished from its description.', 'Description reports what was observed; the argument is the interpretation the author builds, often contested, so separating them lets a reader assess whether the evidence supports the conclusions.'),
       ('Explain why knowing the methods used helps a reader evaluate an ethnography.', 'Methods determine the type and limits of evidence – participant observation shows practice, interviews show meanings, archival work shows history – and reveal possible biases such as access to only one gender or group.')],
  contrast=[('ethnographic description', 'ethnographic argument', 'Description records people, events and practices observed; argument interprets them to make a claim, e.g. that nervos medicalises hunger (Scheper-Hughes).'),
            ('an informant', 'an interlocutor', '"Informant" suggests a passive source of data for the researcher; "interlocutor" stresses dialogue and the participant\'s active role in producing knowledge.')],
  misc=[('An ethnography is simply a neutral description of a culture.', 'An ethnography is an argued interpretation shaped by the author\'s question, methods, theory and position.'),
        ('Knowing the date of fieldwork does not matter for understanding an ethnography.', 'Dates matter because societies change and because the theoretical debates of the time shape the analysis; Mead\'s 1920s Samoa is not Samoa today.')],
  cases=[('Scheper-Hughes\'s Death without Weeping', 'Drawing on work in the Alto do Cruzeiro over decades, she argued that chronic scarcity shaped mothers\' responses to infant death and that hunger was medicalised as nervos.',
          'the relationship between research question, evidence and argument', 'her question about maternal love and infant death led her to collect reproductive histories and observe clinics, and the evidence supports her contested argument about everyday violence.'),
         ('Ong\'s Spirits of Resistance and Capitalist Discipline', 'Ong asked how Malay village women experienced factory work and why spirit possession broke out on the shop floor.',
          'identifying an ethnography\'s argument', 'she argues possession was a form of resistance to capitalist discipline, combining political economy and cultural interpretation.')],
  ev=[('The methods an anthropologist uses determine the conclusions they reach.',
       ['access to only some people limits what can be known (Malinowski and women\'s exchange)', 'participant observation reveals practice not seen in interviews'],
       ['theory and the research question also shape conclusions', 'triangulation of methods reduces the dependence of findings on one method'],
       'Methods strongly shape but do not alone determine conclusions; theory, question and positionality matter too.'),
      ('An ethnography written decades ago has little value for understanding the present.',
       ['societies have changed, so old accounts may mislead', 'theories and ethics of the time may be outdated'],
       ['it is a historical record that allows study of change (Weiner\'s restudy of Malinowski)', 'its arguments may still illuminate concepts'],
       'Older ethnographies remain valuable if situated in their time and read critically.')],
  ext=[('I spent eighteen months on night shifts at the delivery depot, sorting parcels and later riding with drivers. My question was simple: why do drivers who complain constantly about the app\'s algorithm refuse to join the union? Kemal laughed when I asked. "The app is my boss, but the app is also my freedom. If I join the union, my cousin\'s company won\'t give me shifts." I recorded 46 interviews and kept a diary of the shifts I worked. I argue that drivers experience the platform not only as control but as a space of self-employment that they are reluctant to give up.',
        'from the introduction to an ethnography of delivery drivers in Berlin', 'the research question, methods and argument presented in the text',
        'Question: why drivers who complain about the algorithm refuse to join the union. Methods: eighteen months of night-shift participant observation (sorting parcels, riding with drivers), 46 interviews, a diary of shifts. Argument: drivers experience the platform as both control and a space of self-employment they are reluctant to give up.',
        'how the anthropologist\'s methods support the argument in the text', 'Long-term participant observation in the same shifts shows the work from within and builds rapport (Kemal\'s frank answer); interviews give drivers\' own explanations; Kemal\'s statement directly illustrates the ambivalence (control/freedom) and reveals kinship ties (cousin\'s company) that shape decisions – evidence for the argument that platform power is experienced ambivalently.',
        'power', 'Drivers risk losing shifts if identified as critical; Kemal\'s comment about his cousin\'s company is sensitive; the anthropologist worked for the depot, so the employer\'s role in consent and confidentiality must be clarified; data from 46 interviews must be stored securely.')], generic=True)

S('ch06-st2', 'the changing contexts of ethnographic research', ['space', 'change', 'culture'],
  ['mead', 'malinowski', 'weiner', 'geertz', 'nuer'],
  terms=[('ethnographic present', 'the convention of writing about a society in the present tense, which can make it seem timeless and unchanging'),
         ('theoretical approach', 'the framework of ideas (e.g. functionalism, interpretive, political economy, feminist) that shapes the questions an ethnographer asks and how evidence is interpreted'),
         ('restudy', 'a later ethnography of the same community or topic that reveals change over time and/or the effect of the first researcher\'s perspective'),
         ('historical context', 'the events and conditions (colonial rule, war, economic change) prevailing at the time of the fieldwork'),
         ('field site', 'the location – or set of connected locations – in which ethnographic research is carried out')],
  facts=[('Which of the following is an example of a restudy?', 'Annette Weiner\'s fieldwork in the Trobriand Islands in the 1970s',
          ['Geertz\'s first study of Bali', 'Mead\'s first trip to Samoa', 'Holmes\'s research on berry farms'], 'Weiner returned to Malinowski\'s field site.'),
         ('Derek Freeman\'s critique of Margaret Mead (1983) partly rested on the claim that:', 'Mead\'s young informants had been joking with her',
          ['Mead never visited Samoa', 'Mead used only statistics', 'Mead studied Tonga by mistake'], 'Freeman argued she was misled; the claim is itself disputed.'),
         ('Which theoretical approach most clearly shapes Geertz\'s "Deep Play"?', 'Interpretive (symbolic) anthropology',
          ['Unilineal evolutionism', 'Structural-functionalism', 'Cultural materialism'], 'Geertz interprets the cockfight as a text.')],
  why=[('Explain why the time of fieldwork matters when reading an ethnography.', 'The society described may have changed since, and the historical context (colonialism, war, economic crisis) shaped what the ethnographer saw and could do; ignoring time risks treating a past snapshot as a permanent truth.'),
       ('Explain why two anthropologists can produce different accounts of the same place.', 'They may have worked at different times, asked different questions, used different theories, or had different positionality and access (Mead and Freeman in Samoa; Malinowski and Weiner in the Trobriands).'),
       ('Explain why the theoretical approach of an ethnography should be identified.', 'Theory directs attention: a functionalist will look for how institutions maintain order, a feminist for gendered power, a political economist for global inequality; knowing the approach helps evaluate and compare accounts.')],
  contrast=[('the ethnographic present', 'a historically situated account', 'The ethnographic present describes a society in the present tense as if timeless; a historically situated account specifies dates and context and recognises change.'),
            ('a restudy', 'a comparative study', 'A restudy returns to the same people or place to examine change or an earlier account; a comparative study sets different societies side by side to identify similarities and differences.')],
  misc=[('If two ethnographies of the same society disagree, one of them must be wrong.', 'Differences can reflect change over time, different questions, theories, positionality and informants; both may be partial truths.'),
        ('Theory is something added after fieldwork is finished.', 'Theory shapes the research question, what is observed and how notes are taken; it interacts with fieldwork throughout.')],
  cases=[('the Mead–Freeman controversy', 'Mead described relaxed Samoan adolescence in 1925–1926; Freeman, who worked in Western Samoa from the 1940s, described rivalry, violence and strict virginity norms.',
          'situating ethnographies in time, place and theory', 'their differences reflect different islands and decades, different informants (adolescent girls vs. chiefs) and theoretical commitments (cultural determinism vs. biology).'),
         ('Evans-Pritchard\'s The Nuer (1940)', 'The fieldwork took place in the 1930s, shortly after British punitive campaigns against the Nuer, and the account is written largely in the ethnographic present.',
          'the importance of historical context', 'the colonial situation shaped Nuer suspicion of the anthropologist and his access, yet the text presents Nuer society as a timeless system.')],
  ev=[('Ethnographies are more a product of their authors\' theories than of the societies they describe.',
       ['Mead and Freeman reached opposite conclusions about Samoa', 'Writing Culture stressed the constructed nature of texts'],
       ['ethnographies rest on extensive evidence that constrains interpretation', 'restudies often confirm as well as revise earlier findings'],
       'Theory shapes ethnography significantly, but evidence from long-term fieldwork limits how far authors can impose their views.'),
      ('Restudies are the best way to evaluate an ethnography.',
       ['they reveal change and correct earlier bias (Weiner)', 'they test claims empirically'],
       ['the society will have changed, so differences may not show earlier error', 'restudies have their own biases', 'internal critique of evidence and method is also important'],
       'Restudies are valuable but must themselves be situated; they complement rather than replace critical reading.')],
  ext=[('When I arrived in Mutare in 2009, the shops had no prices: the Zimbabwe dollar had just been abandoned, and people paid in US dollars, South African rand and, for small amounts, sweets. My earlier fieldwork in 1998 had described weekly savings clubs among market women as "rotating and stable". Now Mai Chipo told me the club had collapsed twice and been rebuilt "with new rules, and only women we can see every day". I realise that my first book wrote about the clubs as though they had always existed and always would.',
        'fieldnotes from a market town in Zimbabwe', 'how the savings clubs had changed between the two periods of fieldwork',
        'In 1998 the clubs were described as rotating and stable; by 2009 Mai Chipo\'s club had collapsed twice and been rebuilt; the new club has new rules and includes only women members see every day; the economic context had changed (abandonment of the Zimbabwe dollar, multiple currencies, sweets as change).',
        'what the text shows about the importance of situating an ethnography in time', 'The anthropologist\'s first book used the ethnographic present, portraying the clubs as timeless; returning after hyperinflation reveals change driven by economic crisis, and new rules show people adapting social relations (trust limited to those seen daily). Situating the account in time (1998 vs 2009) and context avoids presenting a snapshot as permanent.',
        'change', 'Savings clubs involve money and trust, so describing their collapse could embarrass members or expose them to theft; the anthropologist should anonymise Mai Chipo and the club and reflect on the effects of the earlier publication.')])

S('ch06-st3', 'similar processes in different societies', ['identity', 'power', 'social_relations'],
  ['bourgois', 'holmes', 'scott', 'ong', 'malkki', 'abulughod'],
  terms=[('cross-cultural comparison', 'the systematic examination of similarities and differences between practices in different societies to understand a concept or test a generalisation'),
         ('point of comparison', 'a specific concept, practice or question (e.g. how resistance is expressed) that is used to compare two ethnographies'),
         ('controlled comparison', 'Fred Eggan\'s (1954) method of comparing societies that share history or region so that differences can be linked to specific variables'),
         ('generalisation', 'a broader claim derived from comparing several cases, such as "the less powerful often resist through hidden means"'),
         ('integrated comparison', 'a comparison in which both ethnographies are discussed together point by point, rather than one after the other')],
  facts=[('In a Paper 1 comparison question, which approach usually earns the highest marks?', 'Point-by-point comparison of similarities and differences, with both contexts explained',
          ['Describing the text and then summarising an ethnography separately', 'Listing key concepts without examples', 'Retelling the text in more detail'], 'Integrated, explicit comparison is rewarded in the top markbands.'),
         ('Which pair of ethnographies could be compared on the theme of everyday resistance?', 'Scott\'s Weapons of the Weak and Ong\'s Spirits of Resistance and Capitalist Discipline',
          ['Morgan\'s Ancient Society and Tylor\'s Primitive Culture', 'Augé\'s Non-Places and Douglas\'s Purity and Danger', 'Boas on head form and Rivers on genealogies'], 'Both analyse subtle resistance by less powerful groups.'),
         ('Who proposed the method of "controlled comparison"?', 'Fred Eggan',
          ['Franz Boas', 'Edward Said', 'Marc Augé'], 'Eggan outlined it in 1954.')],
  why=[('Explain why comparing two ethnographies can deepen understanding of a key concept.', 'Seeing a concept such as power operate differently in two contexts shows which features are general and which depend on local conditions, refining the concept and avoiding generalising from one case.'),
       ('Explain why a strong comparison must include context for both ethnographies.', 'Similarities and differences only make sense if the reader knows who, where, when and under what conditions each was studied; otherwise comparison becomes superficial.'),
       ('Explain why comparison must consider differences in method and theory as well as content.', 'Differences between ethnographies may result from how they were researched and theorised rather than from the societies; recognising this avoids false conclusions.')],
  contrast=[('a comparison', 'a contrast', 'A comparison identifies similarities between cases; a contrast identifies differences. IB "compare and contrast" questions require both, linked explicitly.'),
            ('an integrated comparison', 'a sequential (end-on) comparison', 'An integrated comparison discusses both cases together point by point; a sequential comparison describes one case and then the other, leaving links implicit and usually scoring lower.')],
  misc=[('A comparison is complete if both ethnographies are described in detail.', 'Description alone is not comparison; the answer must explicitly identify and explain similarities and differences.'),
        ('Ethnographies can only be compared if they study the same type of society.', 'Ethnographies from very different settings (e.g. Bourgois in New York and Holmes on US farms) can be compared through a shared concept such as structural violence or identity.')],
  cases=[('a comparison of Bourgois and Holmes', 'Both study marginalised Latino workers in the United States – Puerto Rican crack dealers in New York and Triqui farmworkers in Washington – and link suffering to structural forces.',
          'comparing ethnographies through a shared concept', 'both use structural and symbolic violence, but Bourgois stresses an oppositional street culture while Holmes stresses an ethnic-citizenship hierarchy that workers partly accept.'),
         ('a comparison of Scott and Ong', 'Scott\'s Malay peasants resist through gossip and foot-dragging; Ong\'s Malay factory women resist through spirit possession.',
          'everyday forms of resistance', 'both show hidden resistance by the less powerful in Malaysia, but one is rural class conflict over mechanisation and the other gendered resistance to factory discipline expressed in spiritual idioms.')],
  ev=[('Comparing ethnographies from very different societies produces superficial conclusions.',
       ['contexts differ so much that similarities may be misleading', 'concepts may mean different things in each'],
       ['shared concepts (power, identity) allow meaningful comparison', 'difference itself is illuminating', 'Bourgois–Holmes or Scott–Ong comparisons reveal general processes'],
       'Comparison across difference is valuable when context is explained and concepts are used carefully.'),
      ('Similarities between ethnographies matter more than differences.',
       ['similarities support generalisations about human societies', 'they reveal common structural processes'],
       ['differences show how local history and culture shape processes', 'emphasising similarity risks erasing particularity'],
       'Both matter; the best comparisons explain why similarities and differences arise.')],
  ext=[('On the tea estate, the women pluckers sing while they work. The supervisor, Mr Perera, says the songs "keep the rhythm and the quota". Kamala translated one for me: "Leaves for the master\'s cup / Our hands are green, his hands are clean." When the manager walks past, they switch to a hymn. Kamala\'s daughter will not work on the estate; she studies nursing in Colombo. "My mother sings," she says. "I will speak."',
        'fieldnotes from a tea estate in the highlands of Sri Lanka', 'the singing practices of the tea pluckers',
        'Women sing while plucking; the supervisor believes songs keep the rhythm and the quota; one song contrasts the workers\' green hands with the master\'s clean hands; they switch to a hymn when the manager passes; Kamala\'s daughter refuses estate work and studies nursing.',
        'how the songs can be understood as a form of resistance', 'The songs carry hidden criticism of inequality ("our hands are green, his hands are clean") understood by workers but not by supervisors, who see only productivity; switching to a hymn conceals the critique from the manager – a hidden transcript of the less powerful. The daughter\'s "I will speak" points to change from hidden to open resistance through education and mobility.',
        'power', 'Translating and publishing a song critical of management could expose the pluckers to punishment; Kamala acts as translator and could be identified; estate management may control access, so the anthropologist must protect workers\' anonymity and consider whose consent is needed.')])

# =============================================================================================
# ch07 Area of Inquiry 1: Classifying the World – Systems of Classification
# =============================================================================================
S('ch07-st1', 'the ordering of nature, purity and danger', ['classification', 'culture', 'society'],
  ['douglas', 'levistrauss', 'azande', 'miner'],
  terms=[('folk taxonomy', 'a culturally specific system for naming and ordering plants, animals and other things, which may differ from scientific taxonomy'),
         ('anomaly', 'something that does not fit neatly into a culture\'s categories and is therefore often treated as dangerous, polluting or sacred'),
         ('pollution (ritual)', 'a state of impurity caused by contact with substances, people or events defined as out of place, which must be removed by ritual or avoidance'),
         ('"matter out of place"', 'Mary Douglas\'s definition of dirt: anything that offends against a system of order and classification'),
         ('primitive classification', 'Durkheim and Mauss\'s idea (1903) that systems for classifying nature are modelled on the organisation of society')],
  facts=[('Mary Douglas defined dirt as:', '"matter out of place"',
          ['a source of disease', 'anything natural', 'a sign of poverty'], 'Dirt is defined relative to a system of classification.'),
         ('Ralph Bulmer\'s essay "Why is the cassowary not a bird?" (1967) concerned the classification of animals by the:', 'Kalam (Karam) of the New Guinea Highlands',
          ['Nuer of Sudan', 'Inuit of Canada', 'Maasai of Tanzania'], 'The Kalam classify the cassowary separately from birds for social and cosmological reasons.'),
         ('Who wrote Primitive Classification (1903), arguing that classifications of nature mirror social organisation?', 'Émile Durkheim and Marcel Mauss',
          ['Franz Boas and Margaret Mead', 'Mary Douglas and Victor Turner', 'Karl Marx and Friedrich Engels'], 'They linked logical categories to social categories such as clans.'),
         ('Brent Berlin and Paul Kay\'s Basic Color Terms (1969) argued that:', 'languages add basic colour terms in a broadly predictable order',
          ['all languages have exactly eleven colour terms', 'colour perception is entirely arbitrary', 'only European languages distinguish blue and green'], 'Their work fuelled debate between universalism and relativism in classification.')],
  why=[('Explain why anomalies are often treated as dangerous or sacred.', 'Things that cross or confuse categories threaten the order a classification creates, so societies handle them with avoidance, taboo or special ritual – sometimes treating them as polluting (pigs in Leviticus), sometimes as powerful (the Lele pangolin).'),
       ('Explain why Douglas rejected hygienic explanations of food taboos.', 'Hygiene cannot explain why certain animals are banned while equally risky ones are allowed; the pattern makes sense only as the logic of a classification in which banned animals are anomalous.'),
       ('Explain why classification is a key concept in anthropology.', 'Classifications shape perception, behaviour and social order: they decide what is food, who can marry whom and who is pure or impure, and they are tied to power, so studying them reveals how cultures organise reality.')],
  contrast=[('a folk taxonomy', 'a scientific taxonomy', 'A folk taxonomy orders the world according to local purposes, meanings and social concerns; a scientific (Linnaean) taxonomy orders organisms by shared descent and morphology. Scientific taxonomy is also a cultural product with its own history.'),
            ('pollution', 'dirt in the hygienic sense', 'Ritual pollution is impurity defined by a symbolic order and removed by ritual; hygienic dirt is defined by germ theory. Douglas argued that modern ideas of dirt also follow symbolic classification.')],
  misc=[('Classification systems simply reflect natural differences that exist in the world.', 'Classifications are cultural: the same animal can be classed differently (the Kalam cassowary), and categories reflect social concerns, not only nature.'),
        ('Pollution beliefs only exist in "traditional" religious societies.', 'Douglas showed that modern ideas of dirt and cleanliness also express symbolic order, e.g. shoes on the dining table are "dirty" even when clean.')],
  cases=[('Douglas\'s analysis of the abominations of Leviticus', 'The rules forbid animals such as the pig, which has a cloven hoof but does not chew the cud, and water creatures without fins and scales.',
          'classification and anomaly', 'animals that do not fit the defining features of their class are unclean, so the rules express a concern with order and holiness as wholeness.'),
         ('Bulmer\'s study of Kalam animal classification', 'The Kalam do not class the cassowary as a bird (yakt), associating it instead with forest spirits and with kin categories such as cross-cousins.',
          'cultural classification of nature', 'it shows a classification shaped by social and cosmological meanings rather than by morphology alone.')],
  ev=[('Classification systems are mainly determined by the structure of the human mind.',
       ['Lévi-Strauss found recurring binary oppositions', 'Berlin and Kay found regularities in colour terms'],
       ['Douglas and Durkheim linked classification to social order', 'ethnography shows wide variation (Kalam cassowary)', 'power and history shape categories (Dirks, Bowker and Star)'],
       'Mental universals may constrain classification, but its content is shaped mainly by society, culture and power.'),
      ('Mary Douglas\'s theory of pollution applies to all societies.',
       ['her theory explains taboos in Leviticus, the Lele and modern domestic order', 'many societies treat anomalies specially'],
       ['some taboos may have ecological explanations (Marvin Harris)', 'it can underplay individual variation and change', 'not every anomaly is polluting'],
       'Her theory is widely useful but needs to be combined with ecological, historical and political explanations.')],
  ext=[('In the hospital laundry, Lina sorts sheets into four trolleys: white for "normal", yellow for "infectious", red for "foul", and a small blue bin for "patient property". A pair of child\'s socks arrives in the yellow bag. Lina hesitates: "Infectious, but they are property." She puts them in the blue bin, then takes them out again and washes them by hand in the staff sink. "Rules are rules," she tells me, "but a child wants his socks." Her supervisor, seeing this, says nothing, but writes "procedure" on the whiteboard.',
        'fieldnotes from a hospital laundry in Canada', 'the system of categories used in the laundry',
        'Four trolleys/colours: white for normal, yellow for infectious, red for foul, blue for patient property; items are sorted according to these categories; a child\'s socks arrive in a yellow bag; Lina treats them by hand in the staff sink.',
        'why the child\'s socks cause a problem for Lina', 'The socks are an anomaly: they belong to two categories at once (infectious and property), so the classification system cannot place them – "matter out of place" in Douglas\'s sense. Lina resolves the anomaly through a special, improvised procedure, guided by moral concern for the child, while the supervisor\'s "procedure" note reasserts the institutional order and its power.',
        'classification', 'The supervisor\'s response could lead to disciplinary action if Lina is identifiable; hospital laundries involve infection-control rules and patient privacy, so permission from the hospital and anonymity for staff and patients are essential.')])

S('ch07-st2', 'the construction of caste, race, ethnicity and class', ['classification', 'power', 'identity'],
  ['dirks', 'bowker', 'holmes', 'boas', 'barthethnic'],
  terms=[('social construction', 'the process by which categories such as race or caste are produced and maintained by social practices, institutions and beliefs rather than given by nature'),
         ('race', 'a system of classifying people by perceived physical differences into ranked groups; biologically, human variation is continuous and does not divide into discrete races'),
         ('class', 'a social stratum defined by people\'s relationship to economic resources, occupation, wealth and, in Bourdieu\'s terms, cultural capital'),
         ('caste', 'a hereditary, endogamous social category ranked in a hierarchy, associated in South Asia with ideas of purity and pollution'),
         ('racialisation', 'the process by which a group comes to be defined and treated in racial terms')],
  facts=[('The American Anthropological Association\'s Statement on Race (1998) states that:', 'human populations are not unambiguous, clearly demarcated, biologically distinct groups',
          ['races are fixed biological types', 'race determines intelligence', 'there are exactly five human races'], 'The AAA stresses that race is a social invention with real consequences.'),
         ('In colonial Rwanda, the Belgian administration from 1933 required:', 'identity cards recording each person as Hutu, Tutsi or Twa',
          ['all Rwandans to speak French', 'abolition of the monarchy', 'a single national ethnicity'], 'The cards fixed previously more fluid categories and were later used in the 1994 genocide.'),
         ('Which South African law of 1950 classified every person by race?', 'The Population Registration Act',
          ['The Natives Land Act', 'The Group Areas Act', 'The Bantu Education Act'], 'Bowker and Star analyse its classification procedures.')],
  why=[('Explain why anthropologists say race is socially constructed but still real.', 'Racial categories do not correspond to discrete biological groups, but because societies act on them – in law, housing, employment and policing – they have real effects on people\'s lives and identities.'),
       ('Explain why states often create or harden social categories.', 'To count, tax, govern and allocate rights, states need fixed, legible categories (Scott); censuses and identity cards turn fluid identities into official ones (colonial India, Rwanda).'),
       ('Explain why categories such as class and ethnicity intersect.', 'People experience them together: in Holmes\'s farm, ethnicity (Triqui), citizenship and class position combine to place pickers at the bottom of the labour hierarchy.')],
  contrast=[('caste', 'class', 'Caste is ascribed at birth, hereditary and endogamous, justified by ideas of purity; class is based on economic position and, in principle, allows mobility. In practice the two overlap and both are socially constructed.'),
            ('race', 'ethnicity', 'Race classifies by supposed physical traits and has been used to claim biological hierarchy; ethnicity classifies by claimed shared culture and origin. Both are social constructions that can be imposed or claimed.')],
  misc=[('Because race is a social construct, it has no real effects.', 'Socially constructed categories have powerful material effects through discrimination, law and inequality.'),
        ('Caste in India has always been the same rigid system described in ancient texts.', 'Caste has changed over time; colonial censuses (Dirks) hardened it, and Sanskritisation, politics and law continue to reshape it.')],
  cases=[('Belgian identity cards in Rwanda (from 1933)', 'Colonial officials recorded Rwandans as Hutu, Tutsi or Twa, partly by cattle ownership, and favoured Tutsi in administration.',
          'the construction of ethnic categories', 'fluid, partly economic categories were fixed into hereditary "ethnic" identities, later mobilised in the 1994 genocide.'),
         ('apartheid race classification in South Africa', 'The Population Registration Act (1950) assigned race using appearance, descent and "general acceptance"; officials sometimes used tests such as the "pencil test" on hair.',
          'classification and power', 'arbitrary categories determined where people lived, married and worked, and reclassification could split families, showing the human cost of state classification.')],
  ev=[('Social categories such as race and caste are imposed from above rather than created from below.',
       ['states and colonial regimes fixed categories through censuses and laws (Dirks, Rwanda, apartheid)', 'symbolic violence makes them seem natural'],
       ['people also claim and reshape categories (Sanskritisation, Dalit movements)', 'everyday practices of marriage and commensality reproduce them'],
       'Categories are produced both by state power from above and by everyday practice and resistance from below.'),
      ('Class is a more useful concept than ethnicity for understanding inequality.',
       ['economic position explains access to resources', 'Marxist approaches highlight exploitation'],
       ['ethnicity and race shape who ends up in which class (Holmes)', 'identity and recognition matter in their own right'],
       'Neither alone suffices; inequality is best analysed intersectionally.')],
  ext=[('The census enumerator, a university student named Ivan, sits at Mrs Petrova\'s kitchen table with a tablet. The form asks for "ethnicity" with a drop-down list. Mrs Petrova, whose father was Roma and whose mother was Bulgarian, asks him to choose "Bulgarian". Her grandson, listening from the doorway, protests: "Grandma, say Roma! They need to count us." She waves him away. "When they count us," she says, "they come for us." Ivan quietly selects Bulgarian and moves to the next question.',
        'fieldnotes from a census visit in Bulgaria', 'what happens during the census visit',
        'Ivan uses a tablet with a drop-down "ethnicity" list; Mrs Petrova, of Roma and Bulgarian parentage, asks to be recorded as Bulgarian; her grandson urges her to say Roma so that Roma are counted; she replies that being counted leads to persecution; Ivan selects Bulgarian.',
        'why Mrs Petrova and her grandson disagree about her ethnic classification', 'Classification is a matter of power and history: for Mrs Petrova, being officially counted as Roma recalls discrimination and state targeting, so she chooses the majority category for safety; for her grandson, official recognition is a political resource for rights and resources. Ethnicity here is situational and strategic, and the census turns a mixed identity into one box.',
        'classification', 'Ethnic data are sensitive, especially for a historically persecuted minority; the anthropologist must protect Mrs Petrova\'s identity, avoid exposing a family disagreement, and consider the confidentiality of census information observed.')])

S('ch07-st3', 'rules about food, taboo and the body', ['classification', 'materiality', 'identity'],
  ['douglas', 'levistrauss', 'dumont', 'martin'],
  terms=[('taboo', 'a prohibition, often with religious or moral force, on contact with certain things, people, foods or actions'),
         ('commensality', 'eating together, which expresses and creates social relations; rules about who may eat with whom often mark boundaries'),
         ('food taboo', 'a rule forbidding certain foods to some or all members of a group, often marking religious, gender, age or group identity'),
         ('the social body', 'the idea (Douglas) that the physical body is a symbol of society, so concerns about bodily boundaries mirror concerns about social boundaries'),
         ('cultural materialism', 'Marvin Harris\'s approach explaining cultural practices, such as food taboos, by their practical, ecological and economic advantages')],
  facts=[('Marvin Harris explained the sacredness of cattle in India mainly by:', 'their ecological and economic usefulness as draught animals and sources of dung and milk',
          ['their anomalous position in classification', 'the preferences of British colonists', 'a genetic dislike of beef'], 'Harris\'s 1966 article is a classic of cultural materialism.'),
         ('Lévi-Strauss\'s "culinary triangle" is formed by:', 'the raw, the cooked and the rotted',
          ['the sweet, the sour and the bitter', 'the hunted, the herded and the farmed', 'breakfast, lunch and dinner'], 'He used it to explore nature/culture transformations.'),
         ('In Hindu caste practice, rules about accepting cooked food from others are mainly concerned with:', 'preventing ritual pollution between castes',
          ['saving money', 'avoiding food poisoning', 'gender equality'], 'Commensality rules mark caste boundaries (Dumont).')],
  why=[('Explain why food rules are often used to mark group identity.', 'Eating is daily, public and bodily, so shared food rules (halal, kosher, vegetarianism) repeatedly display membership and separate "us" from "them".'),
       ('Explain why Douglas and Harris give different explanations for food taboos.', 'Douglas explains taboos symbolically, as the logic of classification and boundaries; Harris explains them materially, by their ecological and economic benefits. They disagree about whether meaning or practical advantage comes first.'),
       ('Explain why the body is a common site for classification.', 'Bodies are visible and can be marked (dress, scarification, diet), and bodily substances cross boundaries, so societies use the body to signal gender, age, caste or purity and to police social boundaries.')],
  contrast=[('a symbolic explanation of taboo', 'a materialist explanation of taboo', 'A symbolic explanation (Douglas) sees taboo as expressing a system of classification and social boundaries; a materialist explanation (Harris) sees it as an adaptation that brings practical benefits.'),
            ('commensality', 'food taboo', 'Commensality concerns who eats together and so marks social relations; a food taboo concerns what may not be eaten, marking identity or purity.')],
  misc=[('Food taboos exist because the forbidden foods are unhealthy.', 'Many taboos cannot be explained by health; anthropologists explain them through classification (Douglas), identity, or ecology (Harris).'),
        ('Rules about the body only matter in religious contexts.', 'Secular institutions also classify bodies – for instance medical textbooks framing menstruation as failure (Martin) or school uniform rules.')],
  cases=[('Harris\'s analysis of India\'s sacred cattle (1966)', 'Harris argued that protecting cattle preserved draught animals for ploughing, dung for fuel and fertiliser, and milk, which was more valuable than beef.',
          'materialist explanation of taboo', 'he argued that the taboo, though religious in form, is ecologically rational, challenging purely symbolic explanations.'),
         ('Martin\'s The Woman in the Body (1987)', 'Martin analysed medical textbooks and interviewed women in Baltimore about menstruation, birth and menopause.',
          'classification of the body', 'medical language classified female bodily processes as failed production, showing how authoritative knowledge shapes bodily experience.')],
  ev=[('Food taboos are better explained by symbolic meaning than by practical advantage.',
       ['Douglas\'s Leviticus analysis explains the pattern as a whole', 'taboos mark identity even when costly'],
       ['Harris shows many taboos have ecological benefits', 'meaning and material conditions may interact'],
       'Symbolic explanations account for the logic of taboo, but material conditions help explain why particular taboos persist.'),
      ('Rules about the body reflect rules about society.',
       ['Douglas\'s social body: concern with orifices mirrors concern with group boundaries', 'caste purity rules govern bodies and food'],
       ['bodies are also experienced individually and can resist (Ong\'s possession)', 'biomedical classifications are not simply social mirrors'],
       'The body is a powerful symbol of society, but bodily experience is also shaped by biology, power and individual agency.')],
  ext=[('At the end of Ramadan, the Hassan family invites the neighbours to break the fast. Mrs Hassan has bought a separate set of plates "for guests who drink". Mr Oduya from next door brings a cake; she thanks him warmly and places it on the guest table. Later, her teenage daughter Yasmin whispers that the cake contains gelatine. Mrs Hassan smiles: "We do not need to eat it to accept it." At the end of the evening, she sends the leftover cake home with the Oduya children.',
        'fieldnotes from a neighbourhood in Manchester, England', 'the food practices at the Hassans\' evening meal',
        'The Hassans break the fast with neighbours; Mrs Hassan uses a separate set of plates for guests who drink alcohol; Mr Oduya brings a cake, which is placed on the guest table; Yasmin notices it contains gelatine; the family does not eat it but accepts it and sends leftovers back with the Oduya children.',
        'how Mrs Hassan balances food rules with neighbourly relations', 'Food classification (halal/haram, the separate plates) maintains religious purity and identity, yet commensality and gift exchange create neighbourly ties; Mrs Hassan accepts the gift symbolically ("we do not need to eat it to accept it") and returns it, managing a classification boundary without breaking the relationship.',
        'classification', 'Religious practices and private family moments require consent; Yasmin\'s whisper could embarrass her or the neighbours if identifiable; the anthropologist should avoid presenting the family as representative of all Muslims.')])

# =============================================================================================
# ch08 Area of Inquiry 1: Classifying the World – Ethnographic Case Studies
# =============================================================================================
S('ch08-st1', 'caste hierarchy in South Asia', ['classification', 'power', 'change'],
  ['dumont', 'dirks', 'srinivas', 'douglas'],
  terms=[('varna', 'the four-fold ranking of Hindu society in classical texts: Brahmin (priests), Kshatriya (warriors and rulers), Vaishya (merchants) and Shudra (labourers), with "Untouchables" outside the system'),
         ('jati', 'the many local, endogamous caste groups, often linked to hereditary occupations, through which caste is lived in practice'),
         ('Sanskritisation', 'M. N. Srinivas\'s term for the process by which lower castes seek higher status by adopting the customs of higher castes'),
         ('Dalit', 'a self-chosen name, meaning "broken" or "oppressed", used by people from formerly "Untouchable" castes, associated with political movements for dignity and rights'),
         ('dominant caste', 'Srinivas\'s term for a caste that dominates a village through numbers, landownership and political power'),
         ('reservations', 'India\'s policy of reserving places in education, government jobs and legislatures for Scheduled Castes, Scheduled Tribes and Other Backward Classes')],
  facts=[('Louis Dumont argued that the caste system rests on the opposition between:', 'purity and impurity',
          ['wealth and poverty', 'urban and rural', 'men and women'], 'Homo Hierarchicus centres on the pure/impure opposition.'),
         ('Who led the struggle for Dalit rights and chaired the drafting committee of India\'s Constitution?', 'B. R. Ambedkar',
          ['Mahatma Gandhi', 'Jawaharlal Nehru', 'M. N. Srinivas'], 'Ambedkar, himself a Dalit, opposed caste and later converted to Buddhism (1956).'),
         ('Which article of the Indian Constitution (1950) abolished "untouchability"?', 'Article 17',
          ['Article 1', 'Article 370', 'Article 50'], 'Article 17 abolishes untouchability and forbids its practice.'),
         ('Nicholas Dirks argued that modern caste was profoundly shaped by:', 'British colonial knowledge and administration',
          ['Mughal architecture', 'the Green Revolution', 'Portuguese missionaries only'], 'Castes of Mind (2001).')],
  why=[('Explain why Dirks challenged Dumont\'s account of caste.', 'Dumont presented caste as an ancient, religious system based on purity; Dirks argued that colonial censuses and ethnography made caste the central, rigid category of Indian society, so caste\'s modern form is historical and political rather than timeless.'),
       ('Explain why Sanskritisation shows that caste ranking is not completely fixed.', 'Lower castes can rise in local estimation by adopting vegetarianism, Brahmanical rituals and other high-caste customs over generations, showing that caste position is negotiated and changes.'),
       ('Explain why caste persists in contemporary India despite legal abolition of untouchability.', 'Caste is reproduced through endogamous marriage, kinship networks, local politics, occupation and everyday discrimination; it has also become a basis of political mobilisation and of reservation policies.')],
  contrast=[('varna', 'jati', 'Varna is the four-fold ideal hierarchy of classical texts; jati refers to the thousands of local endogamous groups through which caste is actually lived, whose ranks are often disputed.'),
            ('Dumont\'s view of caste', 'Dirks\'s view of caste', 'Dumont saw caste as an enduring religious ideology of hierarchy based on purity; Dirks saw its modern form as a product of colonial power and knowledge.')],
  misc=[('Caste is simply a Hindu religious belief and has nothing to do with politics.', 'Caste is tied to land, power and the state: dominant castes control villages, colonial censuses fixed castes, and caste parties shape modern politics.'),
        ('The caste system disappeared when untouchability was abolished in 1950.', 'Caste remains significant in marriage, politics and discrimination, and reservations are themselves organised by caste categories.')],
  cases=[('Srinivas\'s research on the Coorgs and in Rampura', 'Srinivas observed lower castes adopting vegetarianism, teetotalism and Sanskritic rituals, and a peasant caste dominating village politics through land.',
          'change and power in caste', 'Sanskritisation and the dominant caste show caste rank shaped by mobility and material power, not only by ritual purity.'),
         ('the colonial census of India (from 1871–1872)', 'British officials asked Indians to state their caste, ranked castes in tables, and received petitions from groups claiming higher status.',
          'classification and power', 'the census turned flexible identities into fixed, ranked categories, and caste associations formed to contest rankings – showing classification as political.')],
  ev=[('Caste in India is a colonial invention.',
       ['colonial censuses fixed and ranked castes (Dirks)', 'colonial law and ethnography privileged Brahmanical texts'],
       ['caste-like hierarchy and purity rules are documented long before colonialism', 'Dumont shows deep religious roots', 'the claim risks denying Dalits\' experience of long-standing oppression'],
       'Colonialism transformed and hardened caste but did not invent it; caste has deep roots reshaped by modern power.'),
      ('Purity and impurity are the key to understanding caste.',
       ['Dumont\'s argument; commensality and marriage rules', 'occupational pollution (leatherwork, sweeping)'],
       ['land, labour and political power also determine rank (Srinivas)', 'Dalit perspectives stress exploitation over purity'],
       'Purity is central to caste ideology, but power and economic relations are equally important for its practice.')],
  ext=[('In the WhatsApp group of the village youth association, someone posts a photograph of the new temple doors. Prakash, whose family were leatherworkers, writes that his cousins were not allowed to help carry the doors. Within minutes, several members reply with folded-hands emojis; one writes "politics should stay out of the temple". The next morning, Prakash posts a photograph of Ambedkar. That evening the group administrator removes him, then adds him back after his uncle, a schoolteacher respected by all castes, telephones the administrator\'s father.',
        'fieldnotes from a village in Maharashtra, India', 'what happens in the youth association\'s WhatsApp group',
        'A photograph of new temple doors is posted; Prakash reports his cousins were not allowed to carry the doors; others reply with folded-hands emojis and "politics should stay out of the temple"; Prakash posts an image of Ambedkar; he is removed by the administrator and then re-added after his uncle telephones the administrator\'s father.',
        'how caste hierarchy is both maintained and challenged in the text', 'Exclusion from carrying temple doors reflects purity-based exclusion of a formerly "untouchable" leatherworking caste (Dumont); others try to depoliticise it ("politics should stay out"), maintaining hierarchy; Prakash challenges it by invoking Ambedkar, symbol of Dalit rights; removal and re-admission show power operating through networks and respect (the schoolteacher uncle), so caste is contested in new digital spaces.',
        'power', 'Caste discrimination is a sensitive and potentially dangerous topic; Prakash and his family could face retaliation; the anthropologist must anonymise the village, avoid reproducing screenshots and obtain consent from Prakash and the administrator.')])

S('ch08-st2', 'struggles over social categories', ['classification', 'power', 'change'],
  ['dirks', 'srinivas', 'farmer', 'bowker', 'barthethnic', 'nanda'],
  terms=[('contestation', 'challenging or disputing a category, its boundaries or its meaning, often by those who are disadvantaged by it'),
         ('reclassification', 'moving people or things from one category to another, whether by official decision or by social struggle'),
         ('strategic essentialism', 'Gayatri Spivak\'s term for a group temporarily presenting a shared, fixed identity in order to achieve political goals'),
         ('stigma', 'Erving Goffman\'s term (1963) for an attribute that discredits a person and reduces them "from a whole and usual person to a tainted, discounted one"'),
         ('recognition', 'official or social acknowledgement of a group\'s identity and rights, often sought through legal or political struggle')],
  facts=[('In 1983 the US Centers for Disease Control included which national group among AIDS "risk groups"?', 'Haitians',
          ['Jamaicans', 'Mexicans', 'Canadians'], 'The classification stigmatised Haitians; Farmer analysed it in AIDS and Accusation.'),
         ('In 2014 the Supreme Court of India, in the NALSA judgment, recognised:', 'transgender people, including hijras, as a "third gender"',
          ['caste as unconstitutional', 'English as the national language', 'the abolition of reservations'], 'National Legal Services Authority v. Union of India (2014).'),
         ('Who coined the term "strategic essentialism"?', 'Gayatri Chakravorty Spivak',
          ['Mary Douglas', 'Benedict Anderson', 'Pierre Bourdieu'], 'Spivak used it for marginalised groups mobilising around shared identity.')],
  why=[('Explain why marginalised groups sometimes embrace categories that were imposed on them.', 'An imposed label can become a basis for solidarity and rights claims: "Dalit" was adopted as a political identity, and groups may use official categories to claim reservations or recognition (strategic essentialism).'),
       ('Explain why classifications of disease can be political.', 'Labelling a group as a "risk group" (Haitians in 1983) shifts blame onto them, affects tourism, employment and migration, and diverts attention from structural causes, so medical categories carry power.'),
       ('Explain why categories change over time.', 'Categories are social products, so they shift with power relations, social movements, legal decisions and new knowledge – e.g. census categories adding mixed-race options or courts recognising third genders.')],
  contrast=[('a category imposed from above', 'a category claimed from below', 'An imposed category is defined by states, experts or dominant groups for their purposes (colonial caste tables); a claimed category is adopted and redefined by members themselves for solidarity and rights (Dalit identity).'),
            ('recognition', 'redistribution', 'Recognition seeks acknowledgement of a group\'s identity and dignity; redistribution seeks a fairer share of material resources. Movements often seek both.')],
  misc=[('Once a category is official, it cannot be changed.', 'Official categories are regularly revised through politics and law, e.g. the removal of Haitians as an AIDS risk group in 1985 and the recognition of a third gender in India in 2014.'),
        ('Contesting a category always means rejecting it completely.', 'Groups may also rework a category\'s meaning or use it strategically, as in strategic essentialism.')],
  cases=[('Farmer\'s analysis of the "4H" AIDS risk groups', 'Early US public health reports listed homosexuals, heroin users, haemophiliacs and Haitians as risk groups, and Haitians suffered discrimination in the United States and a collapse of tourism in Haiti.',
          'classification, power and stigma', 'the category blamed a poor nation for the epidemic and hid the role of structural violence and links with the US; Haitian protests helped remove the category.'),
         ('the recognition of hijras as a "third gender" in India (NALSA, 2014)', 'After activism by transgender and hijra groups, the Supreme Court recognised a third gender and ordered welfare measures.',
          'how categories are transformed', 'a culturally long-standing but marginalised category gained legal recognition through contestation, though activists debate whether the category fits all transgender people.')],
  ev=[('Classification is primarily a tool of the powerful.',
       ['states and experts create categories to govern (Scott, Dirks)', 'risk-group labels stigmatise the poor (Farmer)'],
       ['marginalised groups use categories for solidarity and rights (Dalit, hijra)', 'everyday classifications are made by everyone'],
       'Powerful institutions shape classification most strongly, but categories are also resources for those seeking change.'),
      ('Contesting categories is more effective than abolishing them.',
       ['reworking categories brings recognition and resources (reservations, third gender)', 'abolition can erase experiences of discrimination'],
       ['strategic use can entrench the categories it seeks to escape', 'some categories (apartheid race) needed abolition'],
       'The best strategy depends on the category; harmful legal categories need abolition, while identity categories are often reworked.')],
  ext=[('At the regional assembly, the Indigenous delegation from the river villages arrive in feathered headdresses that they rarely wear at home. Their spokesperson, Raimunda, a law graduate, reads out the government\'s definition: "communities maintaining traditional ways of life". "When we use phones, they say we are no longer Indigenous," she says. "So today we wear what they expect, and tomorrow we will take our land." Afterwards, in the car park, the young men change back into football shirts. Raimunda tells me: "The costume is for them. The land is for us."',
        'fieldnotes from a regional assembly in the Brazilian Amazon', 'how the delegation presents itself at the assembly',
        'They wear feathered headdresses rarely worn at home; Raimunda, a law graduate, reads the government definition of Indigenous communities; she criticises the claim that phone use means they are no longer Indigenous; she states their aim to reclaim land; young men change into football shirts afterwards.',
        'how the delegation contests and uses the government\'s classification', 'The state defines Indigeneity as "traditional ways of life", which threatens recognition if people modernise. The delegation strategically performs the expected image (strategic essentialism) to claim land rights while privately living modern lives, showing classification as a resource in a power struggle and showing identity as both performed and real.',
        'classification', 'Revealing the "costume" strategy could be used by opponents to deny the group\'s land claims, so the anthropologist must weigh do no harm against honesty, consult Raimunda on publication and anonymise individuals.')])

S('ch08-st3', 'bureaucratic and digital classification', ['classification', 'power', 'identity'],
  ['bowker', 'seeingstate', 'whywepost', 'dirks'],
  terms=[('algorithm', 'a set of computational rules that sorts, ranks or predicts, increasingly used to classify people for credit, policing, welfare or advertising'),
         ('legibility', 'James C. Scott\'s term for the state\'s effort to make society readable and governable through standard categories such as surnames, maps and censuses'),
         ('biometric identification', 'identifying people by physical traits such as fingerprints or iris scans, as in India\'s Aadhaar system'),
         ('algorithmic bias', 'systematic disadvantage produced when automated classification reproduces inequalities in its data or design'),
         ('infrastructure (classification)', 'Bowker and Star\'s idea that established classifications become invisible background systems that shape action')],
  facts=[('Which book (1999) by Geoffrey Bowker and Susan Leigh Star examines classification systems and their consequences?', 'Sorting Things Out',
          ['Seeing Like a State', 'Purity and Danger', 'Imagined Communities'], 'It analyses the ICD and apartheid race classification.'),
         ('India\'s Aadhaar system, launched in 2009–2010, gives residents:', 'a 12-digit identity number linked to biometric data',
          ['a passport for foreign travel', 'a caste certificate', 'a driving licence'], 'Aadhaar is the world\'s largest biometric ID system.'),
         ('In Seeing Like a State, James C. Scott uses which concept for practical, local knowledge that state schemes ignore?', 'Mētis',
          ['Habitus', 'Communitas', 'Doxa'], 'Mētis is practical knowledge gained through experience.')],
  why=[('Explain why algorithms are a concern for anthropologists of classification.', 'Algorithms classify people at scale, often invisibly, using categories and data that reflect existing inequalities; their decisions on credit, policing or welfare affect life chances, yet people cannot easily see or contest them.'),
       ('Explain why bureaucratic categories can "torque" people\'s lives.', 'When a person\'s complex biography does not fit official categories (e.g. a mixed family under apartheid, a migrant without documents), the system forces them into a box with real consequences for rights and relationships.'),
       ('Explain why states need legibility.', 'To tax, conscript, plan and deliver services, states need standardised information about people and land, so they create censuses, surnames and identity cards that simplify local complexity.')],
  contrast=[('a census category', 'an algorithmic category', 'A census category is a publicly defined, relatively stable official classification used for counting populations; an algorithmic category is often hidden, dynamic and inferred from behaviour data, and can change without people knowing.'),
            ('legibility', 'surveillance', 'Legibility is making a population readable through standard categories for governance; surveillance is the continuous monitoring of people\'s behaviour. Digital systems increasingly combine both.')],
  misc=[('Computer algorithms are objective because they are based on mathematics.', 'Algorithms rely on human-designed categories and historical data, so they can reproduce bias; their outputs are social as well as technical.'),
        ('Digital identification systems benefit everyone equally.', 'Systems like biometric ID can improve access to services but also exclude those whose fingerprints fail or who lack documents, and raise surveillance concerns.')],
  cases=[('India\'s Aadhaar biometric identity system', 'More than a billion residents were enrolled with fingerprints and iris scans, and Aadhaar was linked to food rations, banking and welfare.',
          'digital classification and power', 'it made the population legible to the state and widened access for some, while fingerprint failures excluded some poor workers from rations, and critics raised privacy concerns, leading to a 2018 Supreme Court ruling limiting its compulsory use.'),
         ('the International Classification of Diseases analysed by Bowker and Star', 'The ICD, maintained by the World Health Organization, standardises causes of death and disease for statistics worldwide.',
          'classification as invisible infrastructure', 'its categories shape which deaths are counted and funded, and reflect negotiations between national and medical interests, showing that technical classifications carry values.')],
  ev=[('Digital classification is more dangerous than earlier forms of bureaucratic classification.',
       ['algorithms work at huge scale and are opaque', 'data are combined across systems for surveillance'],
       ['earlier paper classifications (apartheid, colonial censuses, Rwandan ID cards) caused immense harm', 'digital systems can be audited and regulated'],
       'Digital classification intensifies old dangers of legibility through scale and opacity, but the underlying problem of power over categories is not new.'),
      ('Ethnography is the best method for studying algorithms.',
       ['it shows how people experience and work around algorithms', 'it reveals the human choices of engineers (Nick Seaver\'s Computing Taste)'],
       ['code and data require technical analysis', 'corporations restrict access'],
       'Ethnography is essential for understanding the social life of algorithms, ideally combined with technical analysis.')],
  ext=[('The welfare office in Rotterdam introduced a "risk score" last year. Caseworker Annelies shows me the dashboard: applicants are coloured green, amber or red. "I don\'t know how it decides," she admits. "But if it\'s red, I must ask for six extra documents." She points out that many red cases live in two postcodes. Mr Yilmaz, an applicant in red, arrives with a folder of documents in plastic sleeves. "My neighbour told me to bring everything," he says. "The computer does not know us, so we must show it."',
        'fieldnotes from a municipal welfare office in the Netherlands', 'how the risk score affects the caseworker and the applicant',
        'Applicants are coloured green, amber or red on a dashboard; Annelies does not know how the score is calculated; a red score requires six extra documents; many red cases live in two postcodes; Mr Yilmaz brings a folder of documents on his neighbour\'s advice.',
        'how the risk score illustrates the relationship between classification and power', 'An opaque algorithm classifies applicants, and even the caseworker cannot explain it, so power lies in the system\'s categories; clustering of red cases in two postcodes suggests algorithmic bias reproducing spatial and ethnic inequality; applicants adapt (Mr Yilmaz\'s folder), making themselves legible to "the computer", which shows classification shaping behaviour and identity.',
        'classification', 'Welfare data and applicants\' status are confidential; the anthropologist needs permission from the municipality, consent from applicants and staff, and must avoid making identifiable claims about postcodes that could stigmatise neighbourhoods.')])

# =============================================================================================
# ch09 Area of Inquiry 2: Health, Illness and Healing – Concepts and Explanatory Models
# =============================================================================================
S('ch09-st1', 'the experience and explanation of sickness', ['culture', 'classification', 'power'],
  ['kleinman', 'fadiman', 'azande', 'martin', 'lock'],
  terms=[('disease', 'in Kleinman\'s distinction, a biological or psychological malfunction as defined and diagnosed by practitioners, especially in biomedicine'),
         ('illness', 'the lived, subjective experience of being unwell, shaped by culture, including how symptoms are perceived, named and endured'),
         ('sickness', 'in Allan Young\'s usage, the social role and recognition of being unwell – how a society labels and responds to disease and illness'),
         ('explanatory model', 'Kleinman\'s term for the notions held by patients, families and practitioners about the cause, onset, course, treatment and meaning of an episode of sickness'),
         ('biomedicine', 'the dominant medical system in industrialised societies, based on biology and laboratory science, treated by anthropologists as one cultural system among others')],
  facts=[('Who developed the concept of explanatory models of illness?', 'Arthur Kleinman',
          ['Paul Farmer', 'Mary Douglas', 'Victor Turner'], 'Kleinman set it out in Patients and Healers in the Context of Culture (1980).'),
         ('In Kleinman\'s model of the health care system, where are most episodes of sickness first managed?', 'The popular sector of family and community',
          ['The professional sector of hospitals', 'The folk sector of specialist healers', 'The state sector of ministries'], 'Self-treatment and family advice handle most sickness.'),
         ('The Hmong phrase qaug dab peg, used for Lia Lee\'s seizures in Fadiman\'s book, means:', '"the spirit catches you and you fall down"',
          ['"the body is weak"', '"the blood is too hot"', '"the doctor knows best"'], 'Her parents saw the seizures as soul loss with spiritual significance.'),
         ('Azande witchcraft beliefs, as described by Evans-Pritchard, mainly answer the question:', 'why misfortune happened to a particular person at a particular time',
          ['how termites damage wood', 'which plants cure fever', 'how to make a poison oracle'], 'Witchcraft explains the "why me, why now".')],
  why=[('Explain why the distinction between disease and illness is useful for anthropologists.', 'It separates the biological condition diagnosed by practitioners from the patient\'s experience and meaning of being unwell, showing why people with the same disease may suffer differently and why treatment that ignores illness may fail.'),
       ('Explain why conflicting explanatory models can affect health outcomes.', 'If doctors and patients disagree about cause and treatment, patients may not follow prescriptions or may seek other healers, and trust breaks down – as with Lia Lee\'s family and her doctors in Merced.'),
       ('Explain why biomedicine can be analysed as a cultural system.', 'Biomedicine has its own categories, metaphors, rituals and hierarchies (e.g. Martin\'s industrial metaphors for the female body), and its practice varies between countries (Lock on menopause), so it is not a culture-free view from nowhere.')],
  contrast=[('disease', 'illness', 'Disease is the biological malfunction diagnosed by practitioners; illness is the lived experience and cultural meaning of being unwell for the sufferer and their family.'),
            ('a personalistic explanation of sickness', 'a naturalistic explanation of sickness', 'A personalistic explanation attributes sickness to the actions of an agent such as a witch, spirit or ancestor; a naturalistic explanation attributes it to impersonal forces such as germs, humoral imbalance or cold (George Foster, 1976).')],
  misc=[('Explanatory models are only held by patients from non-Western cultures.', 'Everyone, including biomedical doctors, holds explanatory models; Kleinman applied the concept to practitioners as well as to patients.'),
        ('If a disease is diagnosed correctly, the patient\'s beliefs about it are irrelevant.', 'Beliefs shape how patients experience illness, whether they follow treatment and how they seek care, so they affect outcomes.')],
  cases=[('the case of Lia Lee in Fadiman\'s The Spirit Catches You and You Fall Down', 'Doctors in Merced treated Lia\'s epilepsy with complex drug regimes; her Hmong parents, who saw the seizures as qaug dab peg, adjusted the medicines and Lia was placed in foster care for a time.',
          'conflicting explanatory models', 'the breakdown came from incompatible explanatory models and unequal power, not simply non-compliance; Kleinman\'s questions were later used to train doctors in cultural competence.'),
         ('Lock\'s comparison of menopause in Japan and North America', 'Fewer Japanese women reported hot flushes, and kōnenki was not defined as a deficiency disease.',
          'local biologies and explanatory models', 'bodily experience and its medical interpretation vary between societies, challenging the universality of biomedical categories.')],
  ev=[('Kleinman\'s explanatory models approach is the best way to understand illness.',
       ['it reveals differences between patients\' and practitioners\' understandings', 'it is practically useful for doctors'],
       ['it focuses on individual beliefs and can neglect structural causes (Farmer)', 'it may treat culture as a barrier to biomedicine'],
       'It is valuable for understanding meaning but must be combined with attention to political economy and structural violence.'),
      ('Biomedicine is simply more correct than other medical systems.',
       ['biomedicine has proven efficacy for many diseases (antibiotics, vaccines)', 'it rests on experimental evidence'],
       ['it is also a cultural system with its own metaphors and biases (Martin, Lock)', 'other systems address meaning and social relations', 'efficacy depends on access and trust'],
       'Biomedicine is highly effective for many diseases, but its practice is cultural and it does not address all dimensions of illness.')],
  ext=[('The doctor at the district clinic tells Grandfather Osei that his blood pressure is "very high" and gives him tablets. On the walk home he tells his grandson that the pressure comes from "thinking too much" since his land was taken by his nephew. He takes the tablets only on days when he has quarrelled. His grandson, a nursing student, explains that the tablets must be taken daily. "The tablets are for the body," the old man replies. "The thinking needs a family meeting." The following week, the elders call the nephew to a meeting.',
        'fieldnotes from a rural district in Ghana', 'how Grandfather Osei understands and responds to his high blood pressure',
        'He receives tablets for "very high" blood pressure; he attributes it to "thinking too much" after his nephew took his land; he takes tablets only on days he has quarrelled; he says the tablets are for the body but the thinking needs a family meeting; the elders call the nephew to a meeting.',
        'how the text illustrates differing explanatory models of sickness', 'The doctor\'s model locates hypertension in the body and prescribes daily medication (disease); Grandfather Osei\'s model links his illness to a social conflict over land (personalistic and social cause) and so adapts the treatment; he combines biomedicine with a family meeting to treat the social cause, illustrating Kleinman\'s disease/illness distinction and medical pluralism within the popular sector.',
        'culture', 'Health information is confidential; the land dispute is a sensitive family matter; the grandson\'s dual position as nursing student and family member must be considered; anonymise the family and clinic.')])

S('ch09-st2', 'the body and culturally specific illness', ['identity', 'materiality', 'culture'],
  ['scheper', 'lock', 'ong', 'martin', 'fadiman'],
  terms=[('personhood', 'the cultural understanding of what makes someone a person – when personhood begins and ends, and how it is composed of body, soul and relationships'),
         ('dividual', 'a concept (McKim Marriott for South Asia; Marilyn Strathern for Melanesia) of the person as composed of relationships and exchanged substances rather than as a bounded individual'),
         ('culture-bound syndrome', 'a pattern of distress recognised as an illness in a particular cultural setting, such as susto or amok; DSM-5 (2013) calls these "cultural concepts of distress"'),
         ('embodiment', 'the idea that social experience, culture and inequality are lived and expressed through the body'),
         ('the three bodies', 'Scheper-Hughes and Lock\'s (1987) framework of the individual body, the social body (body as symbol) and the body politic (bodies regulated by power)')],
  facts=[('Susto, an illness recognised in many parts of Latin America, is attributed to:', 'a fright that causes the soul to leave the body',
          ['eating too much meat', 'a vitamin deficiency', 'too much sun'], 'Susto involves soul loss after a frightening event.'),
         ('Who, with Margaret Lock, proposed the framework of "the three bodies" in "The Mindful Body" (1987)?', 'Nancy Scheper-Hughes',
          ['Mary Douglas', 'Emily Martin', 'Arthur Kleinman'], 'They distinguished the individual body, the social body and the body politic.'),
         ('In north-east Brazil, Scheper-Hughes found that hunger was often reinterpreted as:', 'nervos, a nervous illness treated with tranquillisers',
          ['susto, a soul loss', 'amok, a violent frenzy', 'koro, a fear of genital retraction'], 'The medicalisation of hunger hid its political causes.'),
         ('Amok, which gave English the phrase "running amok", was first described as a culture-bound syndrome in:', 'the Malay world',
          ['Japan', 'Peru', 'Ireland'], 'It refers to a sudden episode of violent frenzy followed by amnesia.')],
  why=[('Explain why the concept of culture-bound syndromes has been criticised.', 'It implied that only non-Western societies have culturally specific illnesses, whereas conditions like anorexia nervosa or premenstrual syndrome are also shaped by Western culture; it can also exoticise distress and obscure its social causes.'),
       ('Explain why ideas about personhood affect medical decisions.', 'When a person is thought to begin or end – at conception, birth or naming; at heartbeat cessation or brain death – shapes decisions about abortion, organ donation and end-of-life care, as Lock showed for brain death in Japan and North America.'),
       ('Explain why anthropologists say the body is shaped by society.', 'Diet, labour, violence and medical intervention leave marks on bodies (Holmes\'s injured pickers, Scheper-Hughes\'s nervos), and cultural meanings shape how bodies are experienced and displayed.')],
  contrast=[('the individual', 'the dividual', 'The individual is a bounded, autonomous self, as in Western thought; the dividual is a person composed of relationships and shared substances, partible and exchanged, as described for Melanesia and South Asia.'),
            ('the social body', 'the body politic', 'The social body is the body used as a symbol to think about society (Douglas); the body politic refers to how bodies are regulated, disciplined and controlled by power and the state.')],
  misc=[('Culture-bound syndromes are not real illnesses.', 'They involve genuine suffering and recognised symptoms; what is culturally specific is how distress is expressed, named and treated.'),
        ('Ideas about when life begins and ends are purely medical facts.', 'They are also cultural and legal judgements; Lock showed that Japan and North America treated brain death differently.')],
  cases=[('Ong\'s account of spirit possession among Malay factory women', 'Groups of young women fell into screaming fits, saying they had seen spirits in the factory, and production stopped.',
          'culturally specific expressions of distress', 'possession expressed distress and resistance through a Malay idiom of spirits, which managers medicalised as "mass hysteria".'),
         ('Scheper-Hughes on nervos in the Alto do Cruzeiro', 'Exhausted, hungry sugar-cane workers and their families complained of nervos – trembling, weakness, headaches – and clinics prescribed tranquillisers and vitamins.',
          'the body politic and embodiment', 'hunger produced by inequality was turned into an individual nervous illness, depoliticising suffering written on the body.')],
  ev=[('Culture shapes how illness is experienced more than biology does.',
       ['Lock\'s local biologies: kōnenki differs from menopause', 'nervos and susto show distress expressed in cultural idioms'],
       ['biological processes set limits (infection, injury)', 'biology and culture interact rather than compete'],
       'Illness experience is shaped by both; anthropologists emphasise their inseparable interaction.'),
      ('The concept of culture-bound syndromes should be abandoned.',
       ['it exoticises non-Western suffering', 'Western conditions are also culture-bound'],
       ['it draws attention to cultural variation in distress', 'DSM-5\'s "cultural concepts of distress" offers a more balanced replacement'],
       'The original concept is flawed, but the insight that distress is culturally shaped should be retained in reformulated terms.')],
  ext=[('After the earthquake, Doña Teresa\'s granddaughter stopped eating and slept all day. The clinic doctor said she was "depressed" and suggested pills. Doña Teresa called the curandera instead, who swept the girl\'s body with an egg and herbs and called her name at the place where the wall had fallen. "Her spirit stayed there when she ran," Doña Teresa explained. Three days later the girl asked for tortillas. Her mother, who works in the city, now keeps the clinic leaflet and the curandera\'s herbs on the same shelf.',
        'fieldnotes from a town in highland Guatemala', 'how the granddaughter\'s condition was understood and treated',
        'After the earthquake the girl stopped eating and slept all day; the doctor diagnosed depression and suggested pills; the curandera swept her body with an egg and herbs and called her name where the wall fell; Doña Teresa believed her spirit had stayed there; the girl recovered appetite after three days; the mother keeps both leaflet and herbs.',
        'how the text illustrates the relationship between the body, personhood and a culturally specific illness', 'The girl\'s condition is understood as susto: a fright separated her spirit from her body, so personhood is seen as composed of body and spirit that can become detached; healing restores the person by calling the spirit back at the place of loss. The doctor\'s "depression" is a biomedical model; the mother\'s shelf shows pluralism.',
        'identity', 'The patient is a child who has experienced trauma; consent from guardians and sensitivity to the curandera\'s practice are needed; health details and the curandera\'s identity (healers may face disapproval) should be protected.')])

S('ch09-st3', 'the work of healers', ['culture', 'power', 'social_relations'],
  ['levistrauss', 'kleinman', 'janzen', 'lindenbaum'],
  terms=[('shaman', 'a ritual specialist who, often in a trance, communicates with or travels to the spirit world to heal or to divine; the word comes from the Evenki language of Siberia'),
         ('Ayurveda', 'a South Asian medical system, set out in texts such as the Charaka Samhita, that explains health as a balance of three doshas – vata, pitta and kapha'),
         ('symbolic healing', 'healing that works through shared symbols, narratives and ritual to transform the patient\'s experience, as in Lévi-Strauss\'s "The Effectiveness of Symbols"'),
         ('efficacy', 'the capacity of a treatment to produce a desired effect, judged differently in different healing systems (biological cure, social reconciliation, relief of suffering)'),
         ('placebo (meaning) response', 'improvement produced by the meaning and context of treatment rather than its pharmacological content, as discussed by Daniel Moerman')],
  facts=[('In Ayurveda, the three doshas are:', 'vata, pitta and kapha',
          ['yin, yang and qi', 'blood, phlegm and bile', 'prana, karma and dharma'], 'Health is a balance of the three doshas.'),
         ('The word "shaman" comes from:', 'the Evenki (Tungus) language of Siberia',
          ['ancient Greek', 'Sanskrit', 'Arabic'], 'It was adopted into Russian and then European languages.'),
         ('In "The Sorcerer and His Magic" (1949), Lévi-Strauss told the story of Quesalid, a Kwakwaka\'wakw man who:', 'set out to expose shamans as frauds but became a celebrated healer',
          ['invented a new vaccine', 'refused all healing', 'became a Catholic priest'], 'Quesalid\'s success shows healing depends on collective belief.'),
         ('Lévi-Strauss\'s "The Effectiveness of Symbols" analyses a song sung by a Guna (Cuna) shaman of Panama to:', 'help a woman through a difficult childbirth',
          ['bring rain', 'win a war', 'find lost cattle'], 'The song gives the woman a mythic language for her pain.')],
  why=[('Explain why anthropologists study healing systems rather than just medicines.', 'Healing involves diagnosis, explanation, ritual, relationships and authority, so understanding why people use a healer requires studying the whole system of meanings and social relations, not only the substances used.'),
       ('Explain why symbolic healing can be effective.', 'Shared symbols and narratives give the patient a way to understand and reorganise their experience, reduce anxiety and mobilise social support, which can relieve suffering and sometimes affect physiology (Lévi-Strauss, placebo research).'),
       ('Explain why healers derive authority from more than technical skill.', 'Their authority depends on recognition by the community, initiation, lineage, spiritual calling or professional credentials, and on success stories that reinforce collective belief (Quesalid).')],
  contrast=[('shamanism', 'biomedicine', 'Shamanism treats sickness through communication with spirits and ritual restoring cosmic and social order; biomedicine treats disease through biological diagnosis and pharmaceutical or surgical intervention. Both rely on authority, ritual and belief.'),
            ('Ayurveda', 'biomedicine', 'Ayurveda explains health as the balance of doshas, treated through diet, herbs and lifestyle; biomedicine explains disease through pathogens and physiology. In India they coexist and Ayurveda is professionalised in state colleges.')],
  misc=[('Non-biomedical healers only treat imaginary problems.', 'They treat real suffering, often addressing social and emotional dimensions of illness; patients also use them for chronic and serious conditions.'),
        ('Biomedicine involves no ritual or symbolism.', 'Biomedicine has rituals (ward rounds, white coats, prescriptions) and symbols that shape patients\' experience and trust.')],
  cases=[('Lévi-Strauss\'s account of Quesalid', 'Quesalid learned shamans\' techniques, including hiding a tuft of down in the mouth and producing it bloody as the extracted sickness, and patients recovered under his care.',
          'the social basis of healing', 'his success shows that healing depends on the shared beliefs of patient, healer and community, not only on technique.'),
         ('Janzen\'s study of therapy management in Lower Zaire', 'Kin groups combined hospital medicine with prophets and nganga healers, choosing according to whether an illness was "of God" or "of people".',
          'healing systems and social relations', 'healers were chosen by family groups according to how the illness was explained, showing healing as a social process.')],
  ev=[('Symbolic healing is as effective as biomedical treatment.',
       ['symbolic healing relieves suffering and anxiety (Lévi-Strauss)', 'placebo research shows meaning has physiological effects'],
       ['biomedicine is clearly more effective for infections and surgery', 'efficacy is defined differently in each system'],
       'Their efficacy cannot be compared on one scale; symbolic healing addresses meaning and suffering, biomedicine biological disease.'),
      ('Traditional healing systems should be integrated into national health services.',
       ['they are trusted and accessible (WHO recognises traditional medicine)', 'Ayurveda is already institutionalised in India'],
       ['integration may bureaucratise and change them', 'safety and quality are hard to regulate', 'patients already integrate systems themselves'],
       'Some integration can improve access and trust, but it must respect the systems\' own logics and protect patient safety.')],
  ext=[('In the Ayurvedic clinic in Kochi, Dr Menon takes Mr Rao\'s pulse for several minutes before speaking. "Your pitta is high," she says, recommending he stop eating fried fish at night and take a herbal paste. Mr Rao, an engineer with diabetes, also takes metformin from his endocrinologist. He tells me: "The English doctor fixes the sugar number. Dr Menon fixes why I feel hot and angry all the time." On the clinic wall hang both a portrait of the god Dhanvantari and Dr Menon\'s degree certificate from the state Ayurveda college.',
        'fieldnotes from an Ayurvedic clinic in Kerala, India', 'how Dr Menon diagnoses and treats Mr Rao',
        'She takes his pulse for several minutes; diagnoses high pitta; recommends stopping fried fish at night and a herbal paste; Mr Rao also takes metformin from an endocrinologist; the clinic displays both Dhanvantari and a state college degree.',
        'why Mr Rao uses both Ayurveda and biomedicine', 'He sees the systems as treating different aspects: biomedicine treats the disease measured as a number (blood sugar), while Ayurveda treats his illness experience (feeling hot and angry) through dosha balance and lifestyle. Dr Menon\'s authority combines religious symbolism (Dhanvantari) and professional credentials, showing the legitimacy of a professionalised healing system in medical pluralism.',
        'culture', 'Patients\' medical details are confidential; both practitioners might be affected by how their roles are represented; consent from Dr Menon and Mr Rao, and care not to present Ayurveda as either superior or inferior, are needed.')])

# =============================================================================================
# ch10 Area of Inquiry 2: Health, Illness and Healing – Medical Pluralism and Case Studies
# =============================================================================================
S('ch10-st1', 'the choices people make when seeking treatment', ['culture', 'social_relations', 'power'],
  ['janzen', 'kleinman', 'fadiman', 'farmer'],
  terms=[('medical pluralism', 'the coexistence and combined use of several medical systems – such as biomedicine, Ayurveda, herbalism and spiritual healing – within a society'),
         ('health-seeking behaviour', 'the sequence of actions people take to address illness, from self-treatment to consulting healers and doctors'),
         ('hierarchy of resort', 'Lola Romanucci-Ross\'s term (1969) for the order in which people turn to different healers, which may change as treatment fails'),
         ('therapy management group', 'John Janzen\'s term for the kin and friends who collectively decide how a sick person is treated'),
         ('popular sector', 'in Kleinman\'s model, the lay arena of self-care, family and community where most health decisions are made')],
  facts=[('Who coined the term "therapy management group"?', 'John Janzen',
          ['Arthur Kleinman', 'Paul Farmer', 'Charles Leslie'], 'Janzen used it in The Quest for Therapy in Lower Zaire (1978).'),
         ('The concept of a "hierarchy of resort" was proposed by Lola Romanucci-Ross based on research in:', 'the Admiralty Islands (Manus), Papua New Guinea',
          ['Haiti', 'Kerala', 'Bali'], 'She found people moved between European and indigenous medicine in an order of resort.'),
         ('Which edited volume (1976) helped establish the study of medical pluralism in Asia?', 'Asian Medical Systems, edited by Charles Leslie',
          ['Purity and Danger', 'Writing Culture', 'The Social Life of Things'], 'It compared Ayurvedic, Chinese and other systems.')],
  why=[('Explain why people in many societies use more than one medical system.', 'Different systems address different aspects of illness (biological symptoms, social causes, spiritual meaning), differ in cost and accessibility, and failure of one prompts resort to another; people combine them pragmatically.'),
       ('Explain why health-seeking decisions are often collective.', 'Illness affects families economically and socially; kin share costs, transport and knowledge, and senior relatives may hold authority over decisions (Janzen\'s therapy management group).'),
       ('Explain why medical pluralism involves power relations.', 'Systems are not equal: biomedicine usually has state backing, while others may be marginalised or banned; doctors may dismiss other healers, and patients may hide their use of them.')],
  contrast=[('the popular sector', 'the folk sector', 'The popular sector is lay care by individuals, families and communities; the folk sector consists of non-professional specialist healers such as herbalists, shamans or bone-setters (Kleinman).'),
            ('medical pluralism', 'medical syncretism', 'Medical pluralism is the coexistence and combined use of distinct systems; medical syncretism is the blending of elements of systems into a new form, such as healers who combine injections with prayer.')],
  misc=[('People turn to traditional healers only because they cannot afford biomedicine.', 'Cost matters, but people also choose healers for cultural fit, explanations of "why me", trust and social causes of illness; wealthy people also use multiple systems.'),
        ('Medical pluralism only exists in developing countries.', 'Pluralism is found everywhere: in Europe and North America people use homeopathy, acupuncture, chiropractic and religious healing alongside biomedicine.')],
  cases=[('Janzen\'s BaKongo therapy management groups', 'Kin collectively decided whether to take a patient to a hospital, a prophet or an nganga, depending on whether the illness was attributed to God or to people.',
          'medical pluralism and collective decision-making', 'treatment choices followed explanatory models and kin authority, showing health-seeking as a social process.'),
         ('the Lee family in Merced, California', 'Lia\'s parents used Hmong spiritual healing and herbal remedies alongside, and at times instead of, prescribed anticonvulsants.',
          'pluralism and power', 'the hospital\'s authority and the legal system overrode the family\'s choices, showing unequal power between systems.')],
  ev=[('Medical pluralism benefits patients.',
       ['patients can address different dimensions of illness', 'more options improve access'],
       ['contradictory treatments or delays can cause harm', 'patients may face stigma or legal penalties for using non-biomedical healers'],
       'Pluralism can benefit patients when systems communicate and respect each other; otherwise it may expose them to risk.'),
      ('Health-seeking behaviour is mainly determined by economic factors.',
       ['cost and distance limit choices', 'structural violence restricts access (Farmer)'],
       ['explanatory models and trust shape choices', 'kin authority and social relations shape decisions (Janzen)'],
       'Economic factors set constraints, but cultural explanations and social relations shape choices within them.')],
  ext=[('When baby Amina developed a fever, her grandmother first tied a protective amulet around her wrist and gave her a herbal drink. On the second day, her father bought paracetamol from the kiosk. On the third day, when the fever had not broken, the family borrowed money from an uncle and took her to the district hospital, where she was diagnosed with malaria. "We went to the hospital last because it is far and costly," her mother explained. "But the amulet stays. The medicine kills the fever; the amulet keeps away the eye that sent it."',
        'fieldnotes from a village in northern Nigeria', 'the steps the family takes to treat Amina\'s fever',
        'Day 1: her grandmother ties an amulet and gives a herbal drink; Day 2: her father buys paracetamol from a kiosk; Day 3: the family borrows money from an uncle and takes her to the district hospital, where malaria is diagnosed; the amulet stays on.',
        'how the text illustrates medical pluralism and health-seeking behaviour', 'The family follows a hierarchy of resort from home remedies (popular sector) to kiosk medicines to the hospital (professional sector), shaped by cost and distance; decisions involve several kin (grandmother, father, uncle), like a therapy management group; the amulet addresses a different cause (the "eye") so biomedicine and protective practice are combined rather than seen as alternatives.',
        'social_relations', 'The child is a minor and the account involves health and household finances; consent from parents, anonymity, and care not to portray the delay as ignorance (which could stigmatise the family) are needed.')])

S('ch10-st2', 'inequalities in health', ['power', 'classification', 'materiality'],
  ['farmer', 'holmes', 'scheper', 'bourgois', 'fassin'],
  terms=[('structural violence', 'Johan Galtung\'s term (1969), developed by Paul Farmer, for harm done to people by social structures – poverty, racism, gender inequality – that prevent them from meeting their basic needs'),
         ('symbolic violence', 'Bourdieu\'s term for domination that is accepted as natural by those dominated, as when inequalities are explained by the supposed characteristics of the victims'),
         ('social determinants of health', 'the conditions in which people are born, grow, work and age – income, housing, education, discrimination – that shape health outcomes'),
         ('syndemic', 'Merrill Singer\'s term for interacting epidemics that worsen each other under conditions of social inequality, such as substance abuse, violence and AIDS (SAVA)'),
         ('pathologies of power', 'Paul Farmer\'s phrase (book, 2003) for the ways political and economic inequality produce disease and suffering')],
  facts=[('Who first introduced the concept of structural violence (1969)?', 'Johan Galtung',
          ['Paul Farmer', 'Michel Foucault', 'Antonio Gramsci'], 'Galtung, a Norwegian peace researcher; Farmer brought it into medical anthropology.'),
         ('Paul Farmer co-founded which health organisation in 1987?', 'Partners In Health',
          ['Médecins Sans Frontières', 'The World Health Organization', 'Oxfam'], 'Partners In Health began in Haiti.'),
         ('In Fresh Fruit, Broken Bodies, Holmes argues that Triqui pickers\' injuries are often explained away by:', 'claims that Indigenous people are naturally suited to stooped labour',
          ['lack of medical facilities in Washington', 'genetic diseases', 'a shortage of berries'], 'This is an example of symbolic violence.'),
         ('Farmer illustrated structural violence in "On Suffering and Structural Violence" (1996) with the stories of:', 'Acéphie and Chouchou, two young Haitians',
          ['Lia Lee and her family', 'Quesalid and his patients', 'Wairimu and the bus conductors'], 'Acéphie died of AIDS and Chouchou was killed by soldiers.')],
  why=[('Explain why structural violence is described as "invisible".', 'It is built into ordinary institutions and economic arrangements, has no single identifiable perpetrator, and its effects (illness, early death) appear as natural or as individual misfortune, so its causes are hidden.'),
       ('Explain why Farmer criticises "cultural" explanations of disease.', 'Blaming the culture of the poor (e.g. "risky" behaviour or belief in sorcery in Haiti) diverts attention from poverty, inequality and international power that actually shape exposure and access to treatment.'),
       ('Explain why symbolic violence helps to sustain health inequality.', 'When those who suffer and those who treat them accept explanations that naturalise suffering (Triqui "bodies made for picking"), inequality is not challenged and the structures producing it continue.')],
  contrast=[('structural violence', 'symbolic violence', 'Structural violence is harm produced by social and economic structures that deny people\'s basic needs; symbolic violence is the process by which such inequality is made to seem natural and legitimate, even to its victims.'),
            ('direct violence', 'structural violence', 'Direct violence is physical harm inflicted by identifiable actors; structural violence is harm caused indirectly by social arrangements, with no single perpetrator.')],
  misc=[('Health inequality is mainly the result of poor people\'s unhealthy choices.', 'Choices are constrained by poverty, work, housing and access to care; structural violence shapes exposure to disease and the options available.'),
        ('Structural violence means the same thing as poverty.', 'Structural violence includes poverty but also racism, gender inequality, political repression and legal status, and emphasises that these are socially produced harms.')],
  cases=[('Farmer\'s account of Acéphie in Do Kay, Haiti', 'Acéphie\'s family lost their land to the Péligre dam; to survive she traded with soldiers, became involved with one, was infected with HIV and died of AIDS.',
          'structural violence', 'her death resulted from displacement, poverty, gender inequality and militarisation rather than individual choice.'),
         ('Holmes\'s account of injured Triqui pickers', 'Pickers developed back and knee injuries; clinicians sometimes blamed their culture or their failure to seek care.',
          'symbolic violence in health care', 'medical explanations naturalised suffering produced by the farm labour hierarchy and immigration status.')],
  ev=[('Structural violence is the most important cause of ill health in the world.',
       ['poverty and inequality shape exposure, nutrition and access to care', 'Farmer, Holmes and Scheper-Hughes document its effects'],
       ['biological, environmental and genetic factors also matter', 'the concept can be so broad that it explains everything and nothing', 'people exercise agency even under structural constraint'],
       'Structural violence is a major and often neglected cause, but must be combined with other explanations and attention to agency.'),
      ('Anthropologists studying health inequality have a duty to act, not only to describe.',
       ['Farmer combined research with Partners In Health', 'witnessing suffering carries moral responsibility (Scheper-Hughes)'],
       ['advocacy can compromise analysis', 'participants should decide what action is wanted'],
       'Engagement is justified and often necessary, provided it is collaborative and transparent.')],
  ext=[('The construction workers sleep in a dormitory of bunk beds, twelve to a room, at the edge of the highway. Ravi, who came from Nepal two years ago, shows me the pills he buys from a pharmacy without prescription for his back. "The company doctor only gives a day off if you fall," he says. "Pain is not falling." His friend Bishnu laughs: "Nepalis are strong, we carry mountains." When Bishnu\'s kidney problem got worse, he was sent home before his contract ended. Ravi sends money to Bishnu\'s family every month.',
        'fieldnotes from a labour camp in a Gulf state', 'the living and working conditions of the workers',
        'Twelve workers share a room of bunk beds at the edge of the highway; Ravi buys pills without prescription for back pain; the company doctor only gives time off for falls; Bishnu was sent home with a kidney problem before his contract ended; Ravi sends money to Bishnu\'s family.',
        'how the text illustrates structural and symbolic violence', 'Structural violence: migrant status, crowded housing, dangerous work and company control over health care produce pain and kidney disease and remove sick workers (Bishnu sent home). Symbolic violence: Bishnu\'s "Nepalis are strong, we carry mountains" naturalises suffering as an ethnic trait, as Holmes found among Triqui pickers. Ravi\'s remittances show solidarity under constraint.',
        'power', 'Migrant workers may lose their jobs or visas if identified as critical; the company and country should be anonymised; health information is confidential; the researcher must avoid exposing workers to employer retaliation.')])

S('ch10-st3', 'responses to epidemics', ['change', 'power', 'social_relations'],
  ['richards', 'farmer', 'lindenbaum', 'fassin', 'petryna'],
  terms=[('global health', 'the field of research and practice aiming to improve health worldwide, involving international organisations, states, NGOs and communities'),
         ('safe and dignified burial', 'the WHO-promoted approach during the 2014–2016 Ebola epidemic that adapted funeral practices to prevent transmission while respecting religious and family obligations'),
         ('biological citizenship', 'Adriana Petryna\'s term for claims on the state based on recognised bodily injury, as among Chernobyl-affected Ukrainians'),
         ('therapeutic citizenship', 'Vinh-Kim Nguyen\'s term for forms of belonging and rights organised around access to treatment, such as among people living with HIV in West Africa'),
         ('community engagement', 'involving local people and leaders in designing and running health interventions so that they are trusted and appropriate')],
  facts=[('The West African Ebola epidemic of 2014–2016 mainly affected:', 'Guinea, Liberia and Sierra Leone',
          ['Kenya, Uganda and Tanzania', 'Nigeria, Ghana and Togo', 'Egypt, Libya and Tunisia'], 'These three countries had over 28,000 cases.'),
         ('Kuru among the Fore of Papua New Guinea was transmitted through:', 'mortuary practices in which relatives consumed the dead',
          ['mosquito bites', 'contaminated water', 'sexual contact'], 'Kuru is a prion disease; Lindenbaum documented Fore explanations of sorcery.'),
         ('Which South African organisation, founded in 1998, campaigned successfully for antiretroviral treatment?', 'The Treatment Action Campaign',
          ['Partners In Health', 'The African National Congress Youth League', 'The Red Cross'], 'TAC won a Constitutional Court case in 2002 on mother-to-child transmission.')],
  why=[('Explain why anthropologists were called on to help during the 2014–2016 Ebola epidemic.', 'Transmission was linked to caregiving and funeral practices and to distrust of authorities; anthropologists could explain local meanings, help design safe and dignified burials and improve communication between responders and communities.'),
       ('Explain why top-down epidemic responses can fail.', 'They may ignore local knowledge, violate cultural obligations (e.g. burial rites), rely on coercion that breeds distrust, and overlook the structural conditions – poverty, weak health systems – that drive the epidemic.'),
       ('Explain why epidemics often produce blame and stigma.', 'Fear seeks a cause, and blame is directed at marginalised groups or other nations (Haitians and AIDS), reflecting existing power relations and classifications.')],
  contrast=[('a top-down health intervention', 'a community-led health intervention', 'A top-down intervention is designed and imposed by outside authorities, often efficiently but with little local trust; a community-led intervention is shaped by local people, building trust and fit, though it may be slower to scale.'),
            ('biological citizenship', 'therapeutic citizenship', 'Biological citizenship is claiming rights from the state on the basis of bodily damage (Chernobyl); therapeutic citizenship is belonging and claims organised around access to treatment, often through NGOs and global programmes (HIV in West Africa).')],
  misc=[('Local cultural practices were the main cause of the Ebola epidemic.', 'Practices such as caring for the sick and washing the dead mattered, but weak health systems, poverty and distrust of authorities were crucial, and communities themselves adapted their practices to end the epidemic (Richards).'),
        ('Global health programmes are culturally neutral.', 'They carry assumptions about bodies, risk and behaviour, and their categories and priorities reflect the power of donors and international organisations.')],
  cases=[('Richards\'s study of Ebola in Sierra Leone', 'Villagers developed their own quarantine, caregiving and burial adaptations, and cases fell where communities and responders co-operated.',
          'local responses to epidemics', 'a "people\'s science" of observation and adaptation complemented biomedical knowledge and helped end the epidemic.'),
         ('Fassin\'s study of AIDS in post-apartheid South Africa', 'The government of Thabo Mbeki questioned the link between HIV and AIDS and delayed antiretroviral roll-out until activism and court rulings forced change.',
          'the politics of epidemics', 'responses to the epidemic were shaped by the history of apartheid, racism and suspicion of Western science, as well as by activism.')],
  ev=[('Local knowledge is as important as biomedical knowledge in controlling epidemics.',
       ['communities adapted burial practices to stop Ebola (Richards)', 'trust determines whether interventions are accepted'],
       ['biomedical knowledge identified pathogens, vaccines and treatments', 'local knowledge can include harmful practices or rumours'],
       'Both are essential: biomedical tools are effective only when combined with local knowledge and trust.'),
      ('Epidemics reveal existing inequalities more than they create new ones.',
       ['HIV followed structural violence in Haiti and South Africa', 'the poor are more exposed and less able to access treatment'],
       ['epidemics also create new forms of identity and activism (TAC, therapeutic citizenship)', 'they can trigger new stigma and changes in practice'],
       'Epidemics both expose and transform inequalities and social relations.')],
  ext=[('When the health team arrived in white suits to take Pa Sesay\'s body, his sons blocked the path. "He will not go in a plastic bag like rubbish," the eldest said. After hours of talk, the team leader agreed that the imam could pray over the body and that the family could watch the burial from behind a rope. The sons dug the grave themselves. Weeks later, the village set up its own checkpoint, and Mamie Kamara, the women\'s leader, insisted that anyone returning from the city stay in a hut by the stream for twenty-one days.',
        'fieldnotes from a village in Sierra Leone during the 2014–2015 Ebola epidemic', 'how the burial of Pa Sesay was negotiated',
        'The sons blocked the health team in white suits; they objected to the body going "in a plastic bag like rubbish"; after hours of talk the team allowed the imam to pray and the family to watch from behind a rope; the sons dug the grave; later the village set up a checkpoint and a 21-day stay for returnees.',
        'how the text illustrates change in response to an epidemic', 'Initial resistance reflected the obligation to bury the dead with dignity; negotiation produced a compromise similar to "safe and dignified burial", combining biomedical rules with religious rites; the village then made its own quarantine rules (21 days, the incubation period), showing local adaptation and leadership (Mamie Kamara) – Richards\'s "people\'s science".',
        'change', 'Grief and death are deeply sensitive; family members may be stigmatised as Ebola-affected; the anthropologist must consider personal safety and infection risk, obtain consent from bereaved relatives, and anonymise the village.')])

# =============================================================================================
# ch11 Paper 1 Unseen Text Skills and Fieldwork Observation Exercise
# =============================================================================================
S('ch11-st1', 'the interpretation of ethnographic texts', ['culture', 'identity', 'social_relations'],
  ['geertz', 'malinowski', 'abulughod', 'bourgois'],
  terms=[('describe (command term)', 'give a detailed account; in Paper 1 Q1, set out what the text shows without explaining it'),
         ('explain (command term)', 'give a detailed account including reasons or causes'),
         ('analyse (command term)', 'break down in order to bring out the essential elements or structure'),
         ('observation (in an ethnographic text)', 'a statement of what the ethnographer saw or heard, such as actions, words and settings'),
         ('interpretation (in an ethnographic text)', 'the ethnographer\'s or reader\'s explanation of what observed actions mean, often linked to concepts or theory')],
  facts=[('In Paper 1 Q1, which response best answers "Describe the ways in which the traders secure their place"?', 'A detailed account of the specific actions in the text, using its evidence',
          ['A comparison with an ethnography studied in class', 'An evaluation of the ethnographer\'s methods', 'A general definition of power'], 'Q1 asks for description drawn from the text.'),
         ('Which of the following is an interpretation rather than an observation?', 'The women\'s laughter shows they reject the volunteers\' authority',
          ['The women laughed when the volunteers left', 'The cookers stood in a storeroom', 'Kadi said the sun is highest at midday'], 'Attributing meaning to the laughter is interpretation.'),
         ('According to IB command terms, "compare and contrast" requires:', 'an account of similarities and differences between two items, referring to both throughout',
          ['a description of one item only', 'a list of definitions', 'a judgement without evidence'], 'Both items must be addressed throughout.')],
  why=[('Explain why candidates should separate observation from interpretation when reading an unseen text.', 'Q1 rewards accurate description from the text, while Q2 rewards interpretation using concepts; mixing them can lose marks, and separating them shows awareness of how ethnographic knowledge is constructed.'),
       ('Explain why identifying key concepts in an unseen text helps with Paper 1 Q2 and Q3.', 'Naming concepts such as power or belonging turns description into analysis (Q2) and provides the point of comparison with a studied ethnography (Q3).'),
       ('Explain why candidates should quote or refer closely to the text in Paper 1.', 'Marks depend on evidence from the text; close reference shows that claims are grounded and prevents unsupported generalisation.')],
  contrast=[('describing a text', 'explaining a text', 'Describing gives a detailed account of what the text shows; explaining gives reasons or causes for what is shown, typically using anthropological concepts.'),
            ('observation', 'interpretation', 'Observation records actions, words and settings as seen and heard; interpretation proposes what they mean and why they happen.')],
  misc=[('In Paper 1 Q1 you should show your knowledge of other ethnographies to gain top marks.', 'Q1 asks for description from the text; outside ethnography is not credited there and belongs in Q3.'),
        ('An unseen text should be summarised in full before answering any question.', 'Answers should be selective and focused on the command term and the question; full summaries waste time and marks.')],
  cases=[('Geertz\'s opening of "Deep Play"', 'Geertz begins with the police raid on a cockfight and his flight with villagers before interpreting the fight\'s meaning.',
          'moving from observation to interpretation', 'the vivid observed episode is followed by an interpretive argument about status, showing how ethnographic texts build interpretation on description.'),
         ('Abu-Lughod\'s presentation of ghinnawa poems', 'She quotes poems and the situations in which they were recited, then interprets them as a discourse of vulnerability.',
          'evidence and interpretation', 'quotation provides observed evidence, and the interpretation links it to concepts of honour and power.')],
  ev=[('Description is less important than interpretation in Paper 1.',
       ['higher-mark questions (Q2, Q3) reward interpretation and comparison', 'concepts and analysis show understanding'],
       ['interpretation must rest on accurate description', 'Q1 explicitly rewards description', 'misreading the text undermines all later answers'],
       'Interpretation earns more marks, but it depends on accurate, selective description.'),
      ('An unseen ethnographic text can be fully understood without knowing its wider context.',
       ['the text contains evidence that can be analysed directly', 'key concepts allow analysis of any setting'],
       ['meaning depends on history, economy and power beyond the extract', 'candidates must be cautious about generalising'],
       'An extract can be analysed but not fully understood; good answers acknowledge the limits of the text.')],
  ext=[('In the corridor of the immigration office, the queue forms at 5 a.m. Men and women stand in separate lines, though no sign tells them to. A young man sells plastic folders for documents and "a place in the queue" for twenty dirhams. When the doors open at eight, a guard calls out surnames from a list nobody else can see. An older woman, Hajja Fatima, is allowed in first; people step aside for her. A Senegalese student behind me whispers: "Here you learn who matters before you even reach the desk."',
        'fieldnotes from an immigration office in Morocco', 'the organisation of the queue at the immigration office',
        'The queue forms at 5 a.m.; men and women stand in separate lines without any sign; a young man sells folders and places in the queue; at eight a guard calls surnames from a hidden list; Hajja Fatima is allowed in first and people step aside for her.',
        'how the text shows power and hierarchy operating informally', 'Unwritten rules (gender separation), an informal market in places, and the guard\'s private list show that access depends on informal power and knowledge rather than official procedure; respect for age and religious status (Hajja) produces precedence; the student\'s comment interprets the queue as a lesson in hierarchy and belonging for migrants.',
        'social_relations', 'People in an immigration queue may have insecure legal status; observing and writing about them requires care with consent, anonymity and avoiding exposure of the informal "place-selling" or the guard; the researcher\'s own status may affect how they are treated.')], generic=True)

S('ch11-st2', 'the experiences of people living at the margins', ['power', 'identity', 'belonging'],
  ['bourgois', 'holmes', 'scheper', 'ong', 'scott', 'malkki'],
  terms=[('ethnographic material', 'specific ethnographies studied, cited with author, title, people, place and time of fieldwork'),
         ('contextualisation', 'situating an ethnography by stating who was studied, where, when and by whom, and the wider conditions of the research'),
         ('similarity', 'a feature shared by the text and the chosen ethnography, such as the use of hidden forms of resistance'),
         ('difference', 'a feature that distinguishes the text from the chosen ethnography, such as scale, setting or the form power takes'),
         ('running comparison', 'a comparison that moves between the text and the ethnography throughout the answer rather than treating them separately')],
  facts=[('In a Paper 1 comparison answer, which opening best contextualises an ethnography?', '"Holmes (2013) studied Triqui migrant farmworkers from Oaxaca on berry farms in Washington State in 2003–2005."',
          ['"Holmes wrote a book about fruit."', '"In a study I read, workers were poor."', '"Anthropologists have studied migrants."'], 'Author, date, people, place and time give context.'),
         ('Which ethnography would best compare with a text about hidden criticism of employers?', 'Scott\'s Weapons of the Weak',
          ['Morgan\'s Ancient Society', 'Douglas\'s Purity and Danger', 'Augé\'s Non-Places'], 'Scott analyses everyday resistance by the less powerful.'),
         ('Which feature most distinguishes a top-band comparison answer?', 'Explicit, developed similarities and differences linked to key concepts',
          ['Long quotation from the text', 'A list of ethnographies', 'A description of the anthropologist\'s life'], 'Markbands reward sustained, explicit comparison.')],
  why=[('Explain why candidates should choose their comparative ethnography according to the concept in the question.', 'Comparison is meaningful only on a shared point; an ethnography rich in that concept allows specific, developed similarities and differences rather than vague parallels.'),
       ('Explain why differences can be as valuable as similarities in a comparison.', 'Differences reveal how context (history, economy, power) shapes a concept, which shows deeper understanding than listing parallels.'),
       ('Explain why a comparison should mention the methods or theory of the ethnography.', 'Differences between the text and the ethnography may arise from how each was researched or theorised; noting this shows critical understanding of ethnographic knowledge.')],
  contrast=[('a running comparison', 'an end-on comparison', 'A running comparison links the text and the ethnography point by point throughout; an end-on comparison discusses one after the other, leaving links implicit.'),
            ('contextualising an ethnography', 'summarising an ethnography', 'Contextualising states author, people, place and time briefly to situate the evidence; summarising retells the content at length, which wastes time unless linked to the comparison.')],
  misc=[('Any ethnography can be used for any comparison question as long as it is described well.', 'The ethnography must be relevant to the concept in the question; a well-described but irrelevant ethnography earns few marks.'),
        ('A comparison only needs similarities.', '"Compare and contrast" requires both similarities and differences, addressed explicitly.')],
  cases=[('using Bourgois to compare with a text about young unemployed men', 'Bourgois shows Puerto Rican men in East Harlem rejecting humiliating service jobs and seeking respect in the street economy.',
          'comparison through identity and power', 'it allows a comparison of how structural marginalisation shapes masculine identity, while differences in setting, legality and economy can be analysed.'),
         ('using Malkki to compare with a text about refugees', 'Malkki contrasts camp refugees\' "mythico-history" with town refugees\' fluid identities in Tanzania.',
          'comparison through belonging and space', 'it allows analysis of how the spatial setting of displacement shapes identity and belonging in both the text and the ethnography.')],
  ev=[('Choosing the right ethnography is the most important factor in a successful comparison answer.',
       ['relevance determines whether specific comparison is possible', 'a well-matched ethnography supplies concepts and detail'],
       ['the quality of explicit comparison matters more than the choice', 'contextualisation and use of the text are also rewarded'],
       'Choice matters greatly, but marks depend on how explicitly and analytically the comparison is made.'),
      ('Comparing a short unseen text with a whole ethnography is unfair because the two are unequal.',
       ['an extract offers limited evidence while a book offers depth', 'the text\'s context is unknown'],
       ['the task tests the ability to identify concepts and transfer knowledge', 'candidates can acknowledge the limits of the extract'],
       'The imbalance is real, but recognising it and comparing at the level of concepts turns it into an analytical strength.')],
  ext=[('The cleaners at the hotel start before dawn. They are paid per room, not per hour, so Fatou never takes the lunch break written in her contract. She keeps her own list of "good floors" where guests leave tips and "bad floors" of business travellers. The supervisor, Mme Laurent, gives the good floors to the women who bring her pastries on Fridays. When the hotel advertised its "green policy" of not washing towels daily, Fatou laughed: "Green for them, more rooms for us."',
        'fieldnotes from a hotel in Paris', 'how Fatou and the other cleaners organise their work',
        'They start before dawn; they are paid per room, so Fatou skips the lunch break; she classifies floors as "good" (tips) and "bad" (business travellers); Mme Laurent allocates good floors to women who bring her pastries; Fatou notes the green policy means more rooms for cleaners.',
        'how power shapes the cleaners\' working lives', 'Piece-rate pay pushes workers to forgo breaks (structural power of the employer); informal gifts (pastries) buy favour from the supervisor, so power also operates through personal relations and patronage; the green policy shows corporate rhetoric shifting costs onto workers, and Fatou\'s irony is a hidden critique.',
        'power', 'Hotel cleaners, often migrants with insecure contracts, risk losing work if critical comments are traced; the hotel and supervisor should be anonymised and consent obtained from the workers rather than only the management.')])

S('ch11-st3', 'the use of public space', ['space', 'social_relations', 'culture'],
  ['malinowski', 'auge', 'low', 'miller'],
  terms=[('observation site', 'the public or semi-public location chosen for the observation exercise, such as a market, café, sports ground or place of worship'),
         ('jottings', 'brief notes made during observation to record key details, words and times for later expansion'),
         ('thick field notes', 'full notes written soon after observation that describe settings, actions and words in concrete detail and separate description from interpretation'),
         ('research question (observation)', 'a focused question that guides what to observe, e.g. "How do customers and vendors negotiate price at the Saturday market?"'),
         ('triangulation', 'checking findings by comparing data from different methods, times or participants')],
  facts=[('Which research question is most suitable for a short observation exercise?', 'How do people share space at the bus stop during the morning rush?',
          ['What is the meaning of life for city residents?', 'How has the global economy changed since 1945?', 'Why do all humans form families?'], 'A good question is focused and observable in a limited time and place.'),
         ('Which of the following is a descriptive field note rather than an interpretation?', 'At 8.05 a.m. three teenagers stood apart from the queue, looking at one phone',
          ['The teenagers felt excluded by the adults', 'The bus stop is a space of generational conflict', 'Young people reject public norms'], 'It records observable detail and time.'),
         ('When observing in a public place, which is the most important ethical step?', 'Avoid recording identifying details and respect people\'s privacy',
          ['Photograph everyone for accuracy', 'Ask people to change their behaviour', 'Record names from overheard conversations'], 'Anonymity and privacy remain essential even in public.')],
  why=[('Explain why a focused research question improves a short observation exercise.', 'It tells the observer what to look for in a limited time, prevents unfocused description and allows analysis using a relevant key concept.'),
       ('Explain why field notes should separate description from interpretation.', 'Keeping them separate lets the observer check interpretations against the evidence, reconsider them later and show the reader how conclusions were reached.'),
       ('Explain why a reflexive section is important in an observation report.', 'It shows how the observer\'s presence, position and assumptions may have affected what was seen and recorded, which strengthens the credibility of the analysis.')],
  contrast=[('a jotting', 'a full field note', 'A jotting is a brief note made during observation to aid memory; a full field note is a detailed account written soon after, describing setting, actions and words and distinguishing description from interpretation.'),
            ('an overt observer', 'a covert observer', 'An overt observer is known to be researching; a covert observer is not. In public places observers are often not noticed, so they must take particular care with privacy and anonymity.')],
  misc=[('Observing in a public place raises no ethical issues.', 'Even in public, people have expectations of privacy; observers must avoid identifying people, intrusive recording and harm.'),
        ('A good observation report should record everything that happened.', 'Observation must be selective and guided by a research question; the report analyses relevant evidence using concepts.')],
  cases=[('Low\'s observation of plazas in San José, Costa Rica', 'Low mapped who used different areas of the plazas at different times and how users and officials interacted.',
          'systematic observation of public space', 'behavioural mapping and repeated observation showed how space was socially produced and contested, a model for small-scale observation projects.'),
         ('Augé\'s analysis of airports and motorways as non-places', 'Augé described how travellers pass through transit spaces guided by signs, tickets and screens.',
          'choosing an observation site', 'such sites allow students to observe how space shapes interaction and identity, e.g. how people avoid or create contact in a station.')],
  ev=[('A short observation exercise cannot produce valid anthropological knowledge.',
       ['limited time prevents rapport and depth', 'the observer cannot learn insiders\' meanings'],
       ['focused observation reveals patterns of space and interaction', 'it develops ethnographic skills and reflexivity', 'findings can be presented as tentative'],
       'It produces limited but genuine knowledge if its limits are acknowledged.'),
      ('Observing places familiar to the student is better than observing unfamiliar ones.',
       ['familiarity aids access and understanding', 'it reduces risk'],
       ['familiar practices may go unnoticed (the need to make the familiar strange)', 'personal relationships may bias observation'],
       'Either can work; familiar sites require deliberate effort to make the familiar strange.')],
  ext=[('Observation notes, Saturday 10.00–11.30, public library reading room. 10.04: A man in a suit chooses the table nearest the window and spreads three newspapers across it. 10.20: Two teenagers sit at the end of the same table; he moves one newspaper closer to himself without looking up. 10.41: A librarian walks past and says "Good morning, Mr Haddad." 10.55: An older woman asks the teenagers to lower their voices; they put on earphones. 11.12: The man leaves; the teenagers spread out their books across the whole table within two minutes.',
        'observation notes written by a student in a public library', 'how people use the table in the reading room',
        'The man spreads three newspapers across the window table; when teenagers sit, he moves one paper closer without looking up; the librarian greets him by name; an older woman asks the teenagers to lower their voices and they put on earphones; after he leaves, the teenagers spread their books across the whole table within two minutes.',
        'what the notes suggest about how space is claimed in the library', 'Space is claimed through objects (newspapers, books) and bodily signals rather than words; familiarity and recognition (the librarian knows Mr Haddad) give him authority over the "best" table; the teenagers negotiate by adjusting behaviour (earphones) and claim space once he leaves. Space becomes place through regular use, status and informal rules.',
        'space', 'The student recorded a real name (Mr Haddad) heard in public, which should be removed; library users did not consent, so notes must avoid identifying details; permission from library staff is advisable; the student should reflect on their own presence.')])

S('ch11-st4', 'ethical dilemmas in research', ['power', 'belonging', 'change'],
  ['chagnon', 'scheper', 'bourgois', 'simpson', 'holmes'],
  terms=[('ethical issue', 'a question about what is right in research – such as consent, harm, confidentiality or representation – raised by a particular situation'),
         ('competing obligations', 'duties the anthropologist owes to different parties (participants, colleagues, funders, the public) that may conflict'),
         ('big question', 'a broad question about human experience, such as "What does it mean to belong?", answered through key concepts and ethnographic evidence'),
         ('evaluate (command term)', 'make an appraisal by weighing up the strengths and limitations'),
         ('discuss (command term)', 'offer a considered and balanced review that includes a range of arguments, factors or hypotheses, with conclusions supported by evidence')],
  facts=[('In an ethics question on an unseen text, which response is strongest?', 'One that identifies specific ethical issues in the text and weighs competing obligations',
          ['One that lists all ethical principles without reference to the text', 'One that summarises the text', 'One that argues ethics do not apply to anthropology'], 'Answers must be grounded in the text.'),
         ('According to IB command terms, "to what extent" asks candidates to:', 'consider the merits or otherwise of an argument or concept, reaching a supported conclusion',
          ['describe a single example', 'list definitions', 'state a fact'], 'A judgement must be reached and justified.'),
         ('Which ethical issue is most clearly raised when an anthropologist witnesses illegal activity, as Bourgois did?', 'Protecting participants from legal harm while describing their lives honestly',
          ['The need to publish quickly', 'The cost of travel', 'The choice of field notebook'], 'Do no harm and confidentiality conflict with full description.')],
  why=[('Explain why ethics questions reward discussion of dilemmas rather than rules.', 'Real fieldwork situations involve conflicting principles (honesty versus harm, advocacy versus neutrality) that codes cannot settle; discussing how to weigh them shows deeper understanding.'),
       ('Explain why a big question response needs both concepts and ethnography.', 'Key concepts give the analytical lens, while ethnography provides the evidence that turns a philosophical question into an anthropological argument.'),
       ('Explain why representation is an ethical issue in an unseen text.', 'How people are portrayed may affect them if they are identifiable, and may reinforce stereotypes about a group, so the ethics of writing extends beyond fieldwork.')],
  contrast=[('an ethical principle', 'an ethical dilemma', 'An ethical principle is a general rule such as "do no harm"; an ethical dilemma is a specific situation in which principles conflict, requiring judgement.'),
            ('a big question', 'an area-of-inquiry question', 'A big question addresses broad human issues across contexts (e.g. belonging); an area-of-inquiry question focuses on a defined field such as health or classification.')],
  misc=[('An ethics answer should list as many ethical principles as possible.', 'Listing without application earns little; the answer should analyse specific issues in the text and weigh obligations.'),
        ('A big question has one correct answer.', 'Big questions are open; credit goes to well-argued, ethnographically supported responses that consider alternative perspectives.')],
  cases=[('Simpson\'s "ethnographic refusal" in Mohawk Interruptus', 'Simpson chose not to publish certain internal community matters she learned in Kahnawà:ke.',
          'the ethics of representation', 'she shows that responsible ethnography may involve deciding what not to write, protecting the community\'s sovereignty over its own knowledge.'),
         ('Holmes\'s border crossing with Triqui migrants', 'Holmes crossed the US–Mexico border without documents alongside his companions and was arrested and released, while they were deported.',
          'ethical dilemmas of participation', 'the case raises questions about legal risk, unequal consequences for researcher and participants, and the value of shared experience for understanding.')],
  ev=[('The most important ethical obligation of an anthropologist is to the people studied.',
       ['the AAA\'s first principle is do no harm', 'participants bear the greatest risks'],
       ['anthropologists also owe honesty to the public and colleagues', 'communities are divided, so obligations conflict', 'funders and host states impose obligations'],
       'Obligations to participants come first, but they must be balanced with honesty and other responsibilities.'),
      ('Big questions are too broad to be answered anthropologically.',
       ['they invite philosophical generalisation', 'ethnography is specific'],
       ['key concepts and comparison allow ethnography to speak to broad questions', 'anthropology has always addressed what it means to be human'],
       'Big questions can be answered anthropologically when grounded in specific ethnographic comparison.')],
  ext=[('The researcher had been invited by the mining company to study "community relations" in the valley. On her first day, villagers assumed she worked for the company and refused to speak to her. She moved out of the company guesthouse and rented a room from Doña Rosa, whose son had been injured in a protest against the mine. Within weeks, protest leaders were asking her to share what she knew about the company\'s plans. The company manager, meanwhile, emailed asking for "a short list of key troublemakers".',
        'fieldnotes from a mining region in the Andes of Peru', 'the different groups the researcher deals with in the text',
        'The mining company, which invited her to study community relations; villagers who assumed she worked for the company and refused to talk; Doña Rosa, her landlady, whose son was injured in a protest; protest leaders who asked her to share information; the company manager who asked for a list of troublemakers.',
        'how the researcher\'s position shapes her relationships in the text', 'Her initial link to the company (funding, guesthouse) made villagers suspicious, so positionality limited access; moving in with Doña Rosa repositioned her within the community; both sides then try to use her as a source of information, showing how power and competing interests turn the researcher into a resource and create pressures on neutrality.',
        'power', 'This is a classic dual-use dilemma: providing a list of "troublemakers" would breach do no harm and confidentiality and could endanger people; she must be transparent with villagers about her funding, refuse to pass on identifying information, consider whether she can continue under company funding and protect Doña Rosa\'s family.')])
