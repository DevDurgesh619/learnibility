"""IB DP Psychology (SL/HL, NEW guide, first assessment May 2027) - ib-g11-psychology.

Content pack for the QB-IB engine. The new guide is organised around six concepts (bias, causality,
change, measurement, perspective, responsibility), three content areas (biological, cognitive,
sociocultural), four contexts (health and well-being, human development, human relationships,
learning and cognition) and research methods (class practicals: experiment, observation, survey,
interview). Items use real, correctly attributed studies (researcher, year, aim, method, findings,
evaluation), IB command terms, and research-methods items whose numbers are COMPUTED.

This file also exports the shared machinery (Kit, methods generators, markbands) that the
ib_g12_psychology pack imports.

Mock = one examination set mirroring targets.json examPattern (HL):
  Paper 1 (35): Section A 2 short answers x 4 + Section B 2 applied short answers x 6 + Section C
                extended response, two options shown (answer one), 15 marks each, counted once per
                option in the item list -> 4 + 4 + 6 + 6 + 15 (option 1) ... see MOCK below.
  Paper 2 (35): 4 practical-based questions x 5 + evaluation of an unseen study 15.
  Paper 3 (30): 4 source-based questions 3 + 6 + 6 + 15.
Section marks are fixed so every mock carries the same total.
"""
from __future__ import annotations

import math
import statistics

from _common import F, Registry, T, mcq, name, two_names, CITIES  # noqa: F401

CONFIG = {'minutesPerMark': 1.8, 'mcqMinutes': 1.5}

# --------------------------------------------------------------------------------------------
# Markbands
# --------------------------------------------------------------------------------------------
MARKBAND_15 = ('Markbands (15), applied holistically: 13-15 - the response is focused on the command term and the '
               'question throughout; knowledge and understanding of the relevant concepts, theories and studies is '
               'accurate and detailed; research is clearly explained and explicitly linked to the argument; critical '
               'thinking is well developed (methodological, ethical and cultural evaluation, alternative explanations, '
               'the six concepts where relevant) and leads to a reasoned conclusion. 10-12 - focused; accurate knowledge; '
               'relevant research mostly linked to the question; evaluation present but uneven. 7-9 - partly focused; '
               'some accurate knowledge; research described more than used; evaluation limited or generic. 4-6 - '
               'limited focus; knowledge partly accurate; research only named or poorly linked; little evaluation. '
               '1-3 - very limited relevant knowledge, no evaluation. 0 - does not reach band 1.')
MARKBAND_GEN = ('Markbands (scaled to the marks available): top band - focused on the command term, accurate and detailed '
                'knowledge, research explicitly used as evidence, well-developed evaluation (methods, ethics, culture, '
                'alternative explanations) and a reasoned conclusion; middle band - mostly focused, relevant research '
                'partly linked, evaluation uneven; lower band - descriptive, research named but not used, little '
                'evaluation.')
UNSEEN_BANDS = ('Markbands (15): 13-15 - evaluation is focused on THIS study: design, sampling, measurement, '
                'control of variables, credibility/bias, generalisability and ethics are each explained with explicit '
                'reference to details in the stimulus; strengths and limitations are weighed and realistic '
                'improvements are justified. 10-12 - several relevant, mostly well-explained points linked to the '
                'stimulus. 7-9 - relevant points, some generic or not linked to the stimulus. 4-6 - mainly generic '
                'evaluation with limited reference to the study. 1-3 - very limited, largely descriptive. Generic '
                'points not applied to the study (e.g. "small sample") cannot reach the top bands.')
STYLE = {'eval_marks': 8, 'essay_marks': 15, 'markband': MARKBAND_15}

METHOD_TYPES = ['laboratory experiment', 'field experiment', 'natural experiment', 'quasi-experiment',
                'correlational study', 'case study', 'naturalistic observation', 'covert participant observation',
                'semi-structured interview', 'cross-cultural survey', 'meta-analysis', 'longitudinal study',
                'twin study', 'adoption study', 'focus group', 'randomised controlled trial', 'controlled observation',
                'questionnaire survey', 'ethnographic participant observation']
# labels that could also fairly describe a study of type X - never used as its distractors
AMBIG = {
    'laboratory experiment': {'quasi-experiment', 'randomised controlled trial', 'controlled observation'},
    'field experiment': {'natural experiment'},
    'natural experiment': {'quasi-experiment', 'longitudinal study', 'field experiment', 'correlational study'},
    'quasi-experiment': {'natural experiment', 'correlational study', 'laboratory experiment'},
    'correlational study': {'longitudinal study', 'questionnaire survey', 'cross-cultural survey', 'quasi-experiment'},
    'longitudinal study': {'correlational study', 'natural experiment', 'quasi-experiment', 'twin study', 'questionnaire survey', 'case study'},
    'twin study': {'correlational study', 'longitudinal study', 'questionnaire survey', 'quasi-experiment'},
    'case study': {'longitudinal study', 'naturalistic observation', 'semi-structured interview', 'quasi-experiment'},
    'cross-cultural survey': {'questionnaire survey', 'correlational study', 'quasi-experiment'},
    'questionnaire survey': {'cross-cultural survey', 'correlational study'},
    'controlled observation': {'laboratory experiment', 'naturalistic observation'},
    'randomised controlled trial': {'laboratory experiment', 'field experiment', 'longitudinal study'},
    'naturalistic observation': {'field experiment', 'correlational study'},
    'semi-structured interview': {'focus group', 'case study', 'questionnaire survey'},
    'covert participant observation': {'naturalistic observation', 'case study', 'ethnographic participant observation', 'field experiment'},
    'ethnographic participant observation': {'naturalistic observation', 'case study', 'covert participant observation'},
    'meta-analysis': set(),
}


def lc(s):
    w = s.split(' ', 1)[0]
    if len(w) > 1 and (w[1].isupper() or w[1].isdigit()):
        return s
    return s[0].lower() + s[1:]


def cap(s):
    return s[0].upper() + s[1:]


def _key(st):
    return st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]


AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.',
           'Both A and R are true, but R is not the correct explanation of A.',
           'A is true but R is false.',
           'A is false but R is true.']


# --------------------------------------------------------------------------------------------
# Kit: registry + psychology-specific template factories (shared with the g12 pack)
# --------------------------------------------------------------------------------------------
class Kit:
    def __init__(self, unseen=None, p3=None, practicals=None, p1_ch=None, p2_ch=None):
        self.R = Registry()
        self.S: dict[str, list] = {}       # key -> list of study dicts
        self.unseen = unseen or []
        self.p3 = p3 or []
        self.practicals = practicals or []
        self.p1_ch = p1_ch or []
        self.p2_ch = p2_ch or []
        self._init = False

    # ---------------------------------------------------------------- authored content
    def facts(self, key, f):
        self.R.facts(key, f)

    def all_studies(self):
        return [s for v in self.S.values() for s in v]

    def study(self, key, who, year, topic, aim, method, findings, link, strengths, limitations,
              mtype=None, iv=None, dv=None, ethics=None, wrong=None, culture=None):
        """One real study. Generates C1 (aim, method type, findings MCQ), C2 (link), C3 (use as
        evidence, IV/DV, ethics) and C4 (evaluate) items."""
        s = dict(who=who, year=year, topic=topic, aim=aim, method=method, findings=findings, link=link,
                 strengths=strengths, limitations=limitations, mtype=mtype, iv=iv, dv=dv, ethics=ethics,
                 wrong=wrong, culture=culture, key=key)
        self.S.setdefault(key, []).append(s)
        R = self.R
        ref = f'{who} ({year})'
        summary = f'{ref}. Aim: {aim}. Method: {method} Findings: {findings}'

        def aim_mcq(rng, slot, s=s):
            others = [o['aim'] for o in self.all_studies() if o is not s and o['aim'] != s['aim']]
            same = [o['aim'] for o in self.S.get(key, []) if o is not s]
            chap = [o['aim'] for o in self.all_studies() if o['key'][:4] == key[:4] and o is not s]
            rng.shuffle(same)
            rng.shuffle(chap)
            pool = list(dict.fromkeys(same + chap + rng.sample(others, min(len(others), 6))))
            if len(pool) < 3:
                return None
            return mcq(rng, f'Which of the following was the aim of the study by {ref} on {topic}?', cap(s['aim']),
                       [cap(x) for x in pool[:3]], f'{ref} aimed {s["aim"]}.')
        R.add(key, 'C1', (1, 3), 'mcq')(aim_mcq)

        if mtype:
            def mtype_mcq(rng, slot, s=s):
                wrongs = [m for m in METHOD_TYPES if m != s['mtype'] and m not in AMBIG.get(s['mtype'], set())]
                rng.shuffle(wrongs)
                return mcq(rng, f'Which research method best describes the study by {ref} on {topic}?', s['mtype'],
                           wrongs[:3], f'{ref}: {s["method"]}')
            R.add(key, 'C1', (1, 2), 'mcq')(mtype_mcq)

        if wrong:
            def find_mcq(rng, slot, s=s):
                return mcq(rng, f'Which of the following was a key finding of {ref} in their research on {topic}?',
                           cap(s['findings'].split('; ')[0].rstrip('.')), s['wrong'], f'{ref} found that {lc(s["findings"])}')
            R.add(key, 'C1', (1, 3), 'mcq')(find_mcq)

        def aim_short(rng, slot, s=s):
            v = rng.choice(['State the aim of the study by {r} on {t}.', 'Outline the aim and method of {r}.',
                            'Identify the research method used by {r} and state its aim.'])
            stem = v.format(r=ref, t=topic)
            ans = f'Aim: {aim}. Method: {method}'
            return dict(stem=stem, answer=ans, type='short', marks=2,
                        markingKey=f'1 mark for an accurate aim ({aim}); 1 mark for an accurate method or design ({lc(method)})')
        R.add(key, 'C1', (2, 3), 'short')(aim_short)

        def link_c2(rng, slot, s=s):
            fr = rng.choice([('Explain how the findings of {r} provide evidence about {l}.', 3),
                             ('Outline the findings of {r} and explain one conclusion about {l} that can be drawn from them.', 4),
                             ('Explain what the study by {r} suggests about {l}.', 3)])
            stem = fr[0].format(r=ref, l=link)
            m = fr[1] if slot.d >= 3 else 2
            return dict(stem=stem, answer=f'Findings: {findings.rstrip(".")}. Link: these results are evidence about {link}.', type='explain',
                        marks=m, markingKey=f'1 mark for accurate findings ({findings}); remaining marks for explicitly '
                        f'explaining what the findings show about {link} (not just restating them).')
        R.add(key, 'C2', (2, 4), 'explain')(link_c2)

        def use_c3(rng, slot, s=s):
            fr = rng.choice(['Using {r} as supporting evidence, explain {l}.',
                             'Describe the study by {r} and explain what it shows about {l}.',
                             'With reference to {r}, explain how research has investigated {l}.'])
            m = 4 if slot.d <= 3 else 6
            return dict(stem=fr.format(r=ref, l=link), answer=summary + f' Link: {link}.', type='short', marks=m,
                        markingKey=f'Up to {m // 2} marks for accurate description of the study (aim, method, findings: '
                        f'{findings}); up to {m - m // 2} marks for explicitly linking the findings to {link}. A study '
                        'that is described but not linked cannot score more than half marks.')
        R.add(key, 'C3', (2, 4), 'short')(use_c3)

        if iv and dv:
            def ivdv(rng, slot, s=s):
                stem = rng.choice([f'Identify the independent variable and the dependent variable in {ref}, and explain how the dependent variable was operationalised.',
                                   f'In {ref}, identify the IV and the DV, and suggest one extraneous variable that should have been controlled.'])
                return dict(stem=stem, answer=f'IV: {iv}. DV: {dv}.', type='short', marks=3,
                            markingKey=f'1 mark IV ({iv}); 1 mark DV ({dv}); 1 mark for an appropriate operationalisation '
                            'or a relevant extraneous variable (e.g. participant variables, demand characteristics, '
                            'order effects) with a brief justification.', gap='G3')
            R.add(key, 'C3', (1, 3), 'short')(ivdv)

        if ethics:
            def eth(rng, slot, s=s):
                stem = rng.choice([f'Explain one ethical consideration that is relevant to {ref}.',
                                   f'Discuss one ethical issue raised by the research of {ref} and how it could be addressed.'])
                m = 3 if stem.startswith('Explain') else 4
                return dict(stem=stem, answer=ethics, type='explain', marks=m,
                            markingKey=f'{ethics} 1 mark for identifying the issue; further marks for explaining it in '
                            'the context of this study and (for discuss) how it was or could be addressed.')
            R.add(key, 'C3', (2, 4), 'explain')(eth)

        def evaluate(rng, slot, s=s):
            fr = rng.choice([('Evaluate {r}.', 6), ('Evaluate the research by {r} on {t}.', 6),
                             ('Discuss the extent to which the study by {r} provides convincing evidence about {l}.', 8),
                             ('With reference to its method, evaluate the study by {r}.', 6)])
            m = fr[1] if slot.d >= 4 else 4
            key_ = ('Strengths: ' + '; '.join(strengths) + '. Limitations: ' + '; '.join(limitations) + '.'
                    + (f' Cultural consideration: {culture}.' if culture else '')
                    + ' Award marks for points explicitly applied to this study (generic points score at most 1). '
                    + MARKBAND_GEN)
            return dict(stem=fr[0].format(r=ref, t=topic, l=link), answer=f'Strengths: {"; ".join(strengths)}. Limitations: {"; ".join(limitations)}.',
                        type='long' if m >= 6 else 'case', marks=m, markingKey=key_, gap='G5')
        R.add(key, 'C4', (3, 5), 'long')(evaluate)

    def ar(self, key, items):
        """Assertion-reason MCQs. items: (assertion, reason, index into AR_OPTS, explanation)."""
        def fn(rng, slot):
            a, r, k, why = rng.choice(items)
            opts = list(AR_OPTS)
            return dict(stem=f'Assertion (A): {a}\nReason (R): {r}\nChoose the correct option.', options=opts,
                        answer=opts[k], markingKey=f'{"ABCD"[k]}. {why}', type='mcq')
        self.R.add(key, 'C2', (2, 4), 'mcq')(fn)

    def add(self, key, c, d, type='short', style=None):
        return self.R.add(key, c, d, type, style)

    # ---------------------------------------------------------------- mock templates
    def init(self):
        if self._init:
            return
        self._init = True
        for key in list(set(self.R.f) | set(self.S)):
            ch = int(key[2:4])
            if ch in self.p1_ch:
                self.R.add(key, 'C2', (1, 5), 'short', style='p1a')(self._p1a)
                self.R.add(key, 'C3', (1, 5), 'short', style='p1b')(self._p1b)
                self.R.add(key, 'C4', (1, 5), 'long', style='p1x')(self._p1x)
            if ch in self.p2_ch:
                self.R.add(key, 'C3', (1, 5), 'short', style='p2q')(self._p2q)
                self.R.add(key, 'C4', (1, 5), 'long', style='p2u')(self._p2u)
            for i, c in enumerate(['C3', 'C3', 'C4', 'C4']):
                self.R.add(key, c, (1, 5), 'case' if i < 3 else 'long', style=f'p3q{i + 1}')(self._p3(i + 1))
            if key in self.R.f and self.R.f[key].evaluate:
                self.R.add(key, 'C4', (4, 5), 'long')(self._bank_essay)

    def templates(self, st):
        return self.R.build(st, STYLE)

    def _p1a(self, rng, slot):
        if slot.style != 'p1a':
            return None
        key = _key(slot.subtopic)
        sts = self.S.get(key, [])
        f = self.R.f.get(key)
        if sts and rng.random() < 0.6:
            s = rng.choice(sts)
            stem = rng.choice([f'Paper 1, Section A. Outline the findings of one study related to {s["link"]}. [4]',
                               f'Paper 1, Section A. Describe one study investigating {s["topic"]}. [4]'])
            ans = f'For example {s["who"]} ({s["year"]}): aim {s["aim"]}; method: {s["method"]} Findings: {s["findings"]}'
            return dict(stem=stem, answer=ans, type='short', marks=4,
                        markingKey=f'{ans} 1 mark: relevant study identified; 1 mark: aim/procedure; 2 marks: accurate, '
                        'specific findings. Any relevant, accurately described study is credited.')
        if f and f.why:
            q, a = rng.choice(f.why)
            return dict(stem=f'Paper 1, Section A (short answer). {q} [4]', answer=a, type='explain', marks=4,
                        markingKey=f'{a} 4 marks: clear, accurate explanation with a relevant example or study; '
                        '2-3 marks: partial explanation; 1 mark: relevant point stated.')
        return None

    def _p1b(self, rng, slot):
        if slot.style != 'p1b':
            return None
        f = self.R.f.get(_key(slot.subtopic))
        if not f or not f.cases:
            return None
        case, what, concept, how = rng.choice(f.cases)
        stem = rng.choice([
            f'Paper 1, Section B (applied short answer). Read the scenario.\n\n{what}\n\nWith reference to one relevant study, explain how {concept} could be used to understand this situation. [6]',
            f'Paper 1, Section B. Scenario: {what}\n\nUsing psychological research, explain this scenario in terms of {concept}. [6]'])
        return dict(stem=stem, answer=how, type='case', marks=6,
                    markingKey=f'{how} 5-6: accurate explanation of {concept} explicitly applied to the scenario and '
                    'supported by a relevant, accurately described study; 3-4: relevant explanation with partial '
                    'application or weakly linked research; 1-2: generic knowledge, little application.', gap='G3')

    def _p1x(self, rng, slot):
        if slot.style != 'p1x':
            return None
        f = self.R.f.get(_key(slot.subtopic))
        if not f or not f.evaluate:
            return None
        claim, pro, con, judge = rng.choice(f.evaluate)
        fr = rng.choice(['Paper 1, Section C (extended response). Evaluate the claim that {c} [15]',
                         'Paper 1, Section C (extended response). "{C}" To what extent do you agree? Refer to research in your answer. [15]',
                         'Paper 1, Section C (extended response). Discuss the view that {c} Refer to at least two studies. [15]'])
        stem = fr.format(c=lc(claim), C=claim)
        return dict(stem=stem, answer=judge, type='long', marks=15, gap='G5',
                    markingKey='Arguments/evidence for: ' + '; '.join(pro) + '. Arguments/evidence against: ' + '; '.join(con)
                    + f'. Possible conclusion: {judge} ' + MARKBAND_15)

    def _p2q(self, rng, slot):
        if slot.style != 'p2q':
            return None
        if rng.random() < 0.5 and self.practicals:
            q, a = rng.choice(self.practicals)
            return dict(stem=f'Paper 2, practical-based question. {q} [5]', answer=a, type='short', marks=5,
                        markingKey=f'{a} 5 marks: accurate, specific to the practical and explained; 3-4: relevant but '
                        'partly generic; 1-2: identification only.', gap='G3')
        out = desc_two(rng, slot, paper2=True)
        if out:
            out['marks'] = 5
        return out

    def _p2u(self, rng, slot):
        if slot.style != 'p2u' or not self.unseen:
            return None
        title, text, points = rng.choice(self.unseen)
        return dict(stem=f'Paper 2, Section B. Read the description of the unseen study "{title}".\n\n{text}\n\n'
                         'Evaluate this study. In your answer refer to the research design, sampling, measurement, '
                         'credibility and ethics. [15]',
                    answer='; '.join(points), type='long', marks=15, gap='G5',
                    markingKey='Indicative content: ' + '; '.join(points) + '. ' + UNSEEN_BANDS)

    def _p3(self, qn):
        def fn(rng, slot):
            if slot.style != f'p3q{qn}' or not self.p3:
                return None
            if qn == 1:
                self._p3i = getattr(self, '_p3i', -1) + 1
            ps = self.p3[getattr(self, '_p3i', 0) % len(self.p3)]
            src = ps['sources']
            if qn == 1:
                i, q, a = ps['q1']
                body = f'Source {"ABCD"[i]}: {src[i]}'
                m, bands = 3, '1 mark per relevant, accurately identified point from the source (max 3).'
            elif qn == 2:
                i, q, a = ps['q2']
                body = f'Source {"ABCD"[i]}: {src[i]}'
                m, bands = 6, ('5-6: accurate interpretation of the data/text with explicit reference to the source; '
                               '3-4: mostly accurate, some reference; 1-2: limited or descriptive.')
            elif qn == 3:
                i, q, a = ps['q3']
                body = f'Source {"ABCD"[i]}: {src[i]}'
                m, bands = 6, ('5-6: evaluation explicitly applied to the source (method, sample, measurement, '
                               'credibility, bias); 3-4: relevant but partly generic; 1-2: limited.')
            else:
                q, a = ps['q4']
                body = '\n\n'.join(f'Source {"ABCD"[k]}: {t}' for k, t in enumerate(src))
                m, bands = 15, ('Markbands (15): 13-15 - synthesises evidence from all sources and relevant own '
                                'knowledge, weighs the quality of each source, and reaches a reasoned conclusion; '
                                '10-12 - uses most sources with some evaluation; 7-9 - uses sources mainly '
                                'descriptively; 4-6 - limited use of sources; 1-3 - little relevant content.')
            return dict(stem=f'Paper 3 - {ps["theme"]}. Question {qn}.\n\n{body}\n\n{q} [{m}]', answer=a,
                        type='long' if qn == 4 else 'case', marks=m, gap='G7' if qn < 4 else 'G5',
                        markingKey=f'{a} {bands}')
        fn.__name__ = f'p3q{qn}'
        return fn

    def _bank_essay(self, rng, slot):
        if slot.style:
            return None
        f = self.R.f.get(_key(slot.subtopic))
        if not f or not f.evaluate:
            return None
        claim, pro, con, judge = rng.choice(f.evaluate)
        fr = rng.choice(['"{C}" Evaluate this claim with reference to research.',
                         'Using two relevant studies, discuss the claim that {c}',
                         'Critically assess the view that {c} Consider at least one methodological and one ethical or cultural issue.',
                         'With reference to the six concepts of the course, discuss the claim that {c}'])
        m = 15 if slot.d >= 5 else 8
        return dict(stem=fr.format(c=lc(claim), C=claim), answer=judge, type='long', marks=m, gap='G5',
                    markingKey='For: ' + '; '.join(pro) + '. Against: ' + '; '.join(con) + f'. Supported conclusion: {judge} '
                    + (MARKBAND_15 if m == 15 else MARKBAND_GEN))


# --------------------------------------------------------------------------------------------
# Research-methods generators (answers are computed)
# --------------------------------------------------------------------------------------------
DATA_CTX = [
    ('the number of words correctly recalled from a 20-word list', 3, 18, 'words', 'memory', ('in silence', 'with music with lyrics playing')),
    ('reaction times in milliseconds on a Stroop colour-naming trial', 520, 980, 'ms', 'attention', ('for incongruent colour words', 'for congruent colour words')),
    ('scores on the Perceived Stress Scale (range 0-40)', 6, 36, 'points', 'stress', ('in the week before exams', 'in the week after a school holiday')),
    ('the number of aggressive acts recorded in a 10-minute playground observation', 0, 12, 'acts', 'aggression', ('after watching an aggressive cartoon', 'after watching a neutral cartoon')),
    ('the number of digits correctly recalled in a digit-span task', 3, 10, 'digits', 'short-term memory', ('in silence', 'while repeating "the" aloud')),
    ("eyewitness estimates of a car's speed in km/h after watching a crash video", 25, 75, 'km/h', 'eyewitness memory', ('when the question used the verb "smashed"', 'when the question used the verb "contacted"')),
    ('the number of errors made on a mirror-drawing task', 1, 20, 'errors', 'procedural learning', ('on the first day of practice', 'on the fifth day of practice')),
    ('self-rated anxiety (1-10) before giving a speech', 1, 10, 'points', 'anxiety', ('before speaking to an audience of 50', 'before speaking to a group of 3')),
    ('minutes spent checking a smartphone during a one-hour study session', 0, 35, 'minutes', 'distraction', ('with the phone on the desk', 'with the phone left in another room')),
    ('the number of anagrams solved in five minutes', 2, 15, 'anagrams', 'problem solving', ('in a quiet room', 'in a noisy room')),
    ('scores on a 30-item vocabulary test', 8, 30, 'marks', 'learning', ('after spaced practice', 'after massed practice')),
    ('the number of schema-consistent items falsely "recalled" from an office scene', 0, 8, 'items', 'schema processing', ('when tested after one week', 'when tested immediately')),
    ('seconds taken to complete a jigsaw puzzle', 45, 180, 's', 'problem solving', ('without the picture on the box', 'with the picture on the box')),
    ('ratings of trust (1-7) given to an unfamiliar partner in a trust game', 1, 7, 'points', 'trust', ('after a cooperative warm-up game', 'after a competitive warm-up game')),
    ('the number of words recalled from a 20-word list', 3, 18, 'words', 'memory', ('when tested in the room where the words were learned', 'when tested in a different room')),
    ('the number of idea units recalled from a short passage', 2, 18, 'idea units', 'comprehension', ('when the title was given before reading', 'when no title was given')),
]
DS_FRAMES = [
    '{n_} replicated a study in {city} and recorded {desc} for {k} participants. The raw data were: {data}.',
    'The raw data below show {desc} for {k} participants in a class practical: {data}.',
    'In an experiment carried out in {city}, {desc} were collected from {k} volunteers: {data}.',
    'A psychology student, {n_}, collected the following data on {desc}: {data}.',
]


def _f2(x):
    return f'{x:.2f}'


def _median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def _num(x):
    return str(int(x)) if float(x).is_integer() else _f2(x)


def desc_stats(rng, slot):
    desc, lo, hi, unit, area, _ = rng.choice(DATA_CTX)
    k = rng.choice({1: [7, 8], 2: [8, 9], 3: [9, 10], 4: [8, 10], 5: [10, 12]}[slot.d])
    data = [rng.randint(lo, hi) for _ in range(k)]
    stem0 = rng.choice(DS_FRAMES).format(n_=name(rng), city=rng.choice(CITIES), desc=desc, k=k,
                                         data=', '.join(map(str, data)))
    d = slot.d
    if d <= 2:
        meas = rng.choice(['mode', 'median', 'range', 'mean'] if d == 2 else ['mode', 'median', 'range'])
        if meas == 'mode':
            data[1] = data[2] = data[0]
            cnt = {x: data.count(x) for x in set(data)}
            top = max(cnt.values())
            if list(cnt.values()).count(top) > 1:
                return None
            mode = max(cnt, key=cnt.get)
            stem = rng.choice(DS_FRAMES).format(n_=name(rng), city=rng.choice(CITIES), desc=desc, k=k,
                                                data=', '.join(map(str, data)))
            return dict(stem=f'{stem} State the mode.', answer=f'{mode} {unit}', type='numerical', marks=1,
                        markingKey=f'A1: mode = {mode} (the most frequent value, occurring {cnt[mode]} times).')
        if meas == 'median':
            med = _median(data)
            return dict(stem=f'{stem0} Calculate the median.', answer=f'{_num(med)} {unit}', type='numerical', marks=2,
                        markingKey=f'M1: order the data: {", ".join(map(str, sorted(data)))}. A1: median = {_num(med)}'
                        + (' (mean of the two middle values).' if k % 2 == 0 else ' (middle value).'))
        if meas == 'range':
            return dict(stem=f'{stem0} Calculate the range and state what it shows.', answer=f'{max(data) - min(data)} {unit}',
                        type='numerical', marks=2,
                        markingKey=f'A1: range = {max(data)} - {min(data)} = {max(data) - min(data)}. R1: it shows the spread '
                        'between the highest and lowest score (but is distorted by extreme values).')
        m = statistics.mean(data)
        return dict(stem=f'{stem0} Calculate the mean, giving your answer to 2 decimal places.', answer=f'{_f2(m)} {unit}',
                    type='numerical', marks=2, markingKey=f'M1: sum = {sum(data)}, divided by {k}. A1: mean = {_f2(m)}.')
    if d == 3:
        if rng.random() < 0.5:   # cluster low and add one extreme (but in-range) score
            top = lo + max(2, (hi - lo) // 3)
            data = [rng.randint(lo, top) for _ in range(k - 1)] + [hi]
            stem0 = rng.choice(DS_FRAMES).format(n_=name(rng), city=rng.choice(CITIES), desc=desc, k=k,
                                                 data=', '.join(map(str, data)))
            out = True
        else:
            out = False
        m, med = statistics.mean(data), _median(data)
        better = ('the median, because the extreme score of ' + str(data[-1]) + ' inflates the mean') if out else \
                 'the mean, because there are no extreme scores and the data are at least interval-like, so the mean uses every value'
        return dict(stem=f'{stem0} Calculate the mean (to 2 decimal places) and the median, and explain which is the more appropriate measure of central tendency for these data.',
                    answer=f'Mean = {_f2(m)}; median = {_num(med)}; more appropriate: {better}.', type='numerical', marks=4,
                    markingKey=f'A1 mean = {sum(data)}/{k} = {_f2(m)}. A1 median = {_num(med)} (ordered: {", ".join(map(str, sorted(data)))}). '
                    f'R2: {better}.')
    m = statistics.mean(data)
    sd = statistics.stdev(data)
    dev = sum((x - m) ** 2 for x in data)
    stem = (f'{stem0} Calculate the mean and the sample standard deviation (to 2 decimal places).' if d == 4 else
            f'{stem0} Calculate the mean and the sample standard deviation (to 2 decimal places), and explain what the standard deviation indicates about the participants\' {area} scores.')
    interp = ('The SD is ' + ('large relative to the mean, so scores were widely spread and the mean is less representative.'
                              if sd / (m or 1) > 0.3 else 'small relative to the mean, so scores clustered closely around the mean and the mean is fairly representative.'))
    return dict(stem=stem, answer=f'Mean = {_f2(m)}; SD = {_f2(sd)}' + (f'. {interp}' if d == 5 else ''), type='numerical',
                marks=4 if d == 4 else 5,
                markingKey=f'M1 mean = {sum(data)}/{k} = {_f2(m)}. M1 sum of squared deviations = {_f2(dev)}. '
                f'M1 divide by n - 1 = {k - 1} and take the square root. A1 SD = {_f2(sd)}.' + (f' R1 {interp}' if d == 5 else ''))


def desc_two(rng, slot, paper2=False):
    """Two conditions: means/SDs computed from raw data; interpretation of direction and spread."""
    desc, lo, hi, unit, area, (hc, lc_) = rng.choice(DATA_CTX)
    k = rng.choice([6, 7, 8])
    shift = rng.choice([-1, 1, 1]) * max(1, (hi - lo) // rng.choice([4, 5, 6]))
    A = [rng.randint(lo, hi) for _ in range(k)]
    if rng.random() < 0.6:
        B = [min(max(x - shift + rng.randint(-(hi - lo) // 6, (hi - lo) // 6), lo), hi) for x in A]
    else:
        B = [rng.randint(lo, hi) for _ in range(k)]
    mA, mB = statistics.mean(A), statistics.mean(B)
    if abs(mA - mB) < 1e-9:
        return None
    sA, sB = statistics.stdev(A), statistics.stdev(B)
    if abs(sA - sB) < 0.01:
        return None
    supports = mA > mB          # condition A is the one predicted to be higher
    who = name(rng)
    frame = rng.choice([
        f'{who} tested the hypothesis that {desc} would be higher {hc} than {lc_}.',
        f'A class in {rng.choice(CITIES)} predicted that {desc} would be greater {hc} than {lc_}.',
        f'Directional hypothesis: {desc} will be higher {hc} than {lc_}.'])
    table = f'Condition A ({hc}): {", ".join(map(str, A))}\nCondition B ({lc_}): {", ".join(map(str, B))}'
    pre = 'Paper 2, practical-based question (data). ' if paper2 else ''
    q = ('Calculate the mean and sample standard deviation for each condition (to 2 decimal places). State whether the '
         'descriptive statistics are in the direction predicted by the hypothesis and compare the spread of the two conditions.')
    more = 'A' if sA > sB else 'B'
    ans = (f'Mean A = {_f2(mA)}, SD A = {_f2(sA)}; mean B = {_f2(mB)}, SD B = {_f2(sB)}. The means are '
           f'{"" if supports else "not "}in the predicted direction. Condition {more} has the larger SD, so its scores are more '
           'spread out (less consistent). Descriptive statistics alone cannot show that the difference is significant; an inferential test is needed.')
    key = (f'A1 means: A = {sum(A)}/{k} = {_f2(mA)}, B = {sum(B)}/{k} = {_f2(mB)}. A1 SD A = {_f2(sA)}. A1 SD B = {_f2(sB)}. '
           f'R1 direction: {"supports" if supports else "does not support"} the hypothesis. R1 spread: condition {more} is more variable.')
    if not paper2:
        key += ' R1 recognises that significance requires an inferential test.'
    return dict(stem=f'{pre}{frame}\n\n{table}\n\n{q}', answer=ans, type='numerical', marks=5 if paper2 else 6,
                markingKey=key, gap='G3')


SPEARMAN_CRIT = {5: 1.000, 6: 0.886, 7: 0.786, 8: 0.738, 9: 0.700, 10: 0.648}
CORR_CTX = [('hours of sleep the night before', 'score on a memory test'),
            ('weekly hours of social media use', 'score on a loneliness scale'),
            ('number of stressful life events in the past year', 'number of days off sick'),
            ('minutes of daily exercise', 'self-rated mood (1-20)'),
            ('years of experience as a taxi driver', 'posterior hippocampal volume rank'),
            ('hours of revision', 'exam percentage'),
            ('number of close friends', 'well-being score'),
            ('caffeine intake (mg per day)', 'self-reported anxiety'),
            ('age in months', 'number of conservation tasks passed'),
            ('daily screen time (hours)', 'sustained-attention score')]


def _ranks(xs):
    s = sorted(xs)
    return [s.index(x) + 1 for x in xs]


def spearman(rng, slot):
    n = rng.choice([6, 7] if slot.d <= 4 else [8, 9, 10])
    xv, yv = rng.choice(CORR_CTX)
    X = rng.sample(range(1, 40), n)
    rx = _ranks(X)
    trend = rng.choice([1, -1, 0])
    if trend == 0:
        ry = rng.sample(range(1, n + 1), n)
    else:
        base = rx if trend == 1 else [n + 1 - r for r in rx]
        ry = list(base)
        for _ in range(rng.randint(1, 3)):
            i, j = rng.sample(range(n), 2)
            ry[i], ry[j] = ry[j], ry[i]
    Y = [10 + 3 * r + rng.choice([0, 1]) for r in ry]   # distinct values whose ranks equal ry
    ry = _ranks(Y)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1 - 6 * d2 / (n * (n * n - 1))
    crit = SPEARMAN_CRIT[n]
    sig = abs(rho) >= crit
    rows = '\n'.join(f'P{i + 1}: {x} | {y}' for i, (x, y) in enumerate(zip(X, Y)))
    direction = 'positive' if rho > 0 else 'negative' if rho < 0 else 'no'
    strength = 'strong' if abs(rho) >= 0.7 else 'moderate' if abs(rho) >= 0.4 else 'weak'
    stem = (f'A researcher in {rng.choice(CITIES)} investigated the relationship between {xv} and {yv} in {n} participants.\n'
            f'Participant: {xv} | {yv}\n{rows}\n\nCalculate Spearman\'s rank correlation coefficient (rs) using '
            f'rs = 1 - 6Σd² / (n(n² - 1)), giving your answer to 3 decimal places. The critical value for n = {n} at '
            f'p = 0.05 (two-tailed) is {crit:.3f}. State whether the correlation is significant and what can be concluded.')
    return dict(stem=stem, answer=f'Σd² = {d2}; rs = {rho:.3f}; {strength} {direction} correlation; '
                f'{"significant" if sig else "not significant"} at p = 0.05.', type='numerical', marks=6 if slot.d >= 5 else 5,
                markingKey=f'M1 rank each variable separately (ranks X: {rx}; ranks Y: {ry}). M1 d² summed: Σd² = {d2}. '
                f'A1 rs = 1 - 6({d2})/({n}({n * n} - 1)) = {rho:.3f}. A1 |rs| {"≥" if sig else "<"} {crit:.3f}, so the correlation is '
                f'{"significant" if sig else "not significant"}; '
                f'{"reject" if sig else "retain"} the null hypothesis. R1 correlation does not show causation - a third variable could explain the relationship.',
                gap='G3')


def r_interpret(rng, slot):
    xv, yv = rng.choice(CORR_CTX)
    r = rng.choice([-0.82, -0.64, -0.45, -0.21, -0.08, 0.05, 0.18, 0.37, 0.56, 0.71, 0.89])
    direction = 'positive' if r > 0 else 'negative'
    strength = 'strong' if abs(r) >= 0.7 else 'moderate' if abs(r) >= 0.4 else 'weak' if abs(r) >= 0.1 else 'negligible (close to zero)'
    meaning = (f'as {xv} increases, {yv} tends to increase' if r > 0 else f'as {xv} increases, {yv} tends to decrease')
    third = rng.choice(['socio-economic status', 'general health', 'motivation', 'age', 'stress levels', 'personality'])
    stem = rng.choice([f'A correlational study found r = {r:.2f} between {xv} and {yv}. Describe this correlation and explain why it cannot be used to conclude that one variable causes the other.',
                       f'{name(rng)} reports a correlation coefficient of {r:.2f} between {xv} and {yv}. Interpret the direction and strength of this relationship, and suggest one third variable that could explain it.'])
    return dict(stem=stem, answer=f'A {strength} {direction} correlation: {meaning}. Correlation does not establish causation; '
                f'a third variable such as {third} could affect both, or causality could run in the opposite direction.',
                type='explain', marks=3,
                markingKey=f'1 mark direction ({direction}); 1 mark strength ({strength}, r = {r:.2f}); 1 mark causality: no IV is '
                f'manipulated, so third variables (e.g. {third}) or bidirectional causality cannot be ruled out.')


IRR_CTX = [('children\'s play in a nursery', {'S': 'solitary', 'P': 'parallel', 'C': 'cooperative'}),
           ('students\' behaviour in a lesson', {'N': 'on-task', 'F': 'off-task', 'D': 'disruptive'}),
           ('shoppers at a self-checkout', {'H': 'asks for help', 'I': 'independent', 'A': 'abandons'}),
           ('pedestrians at a crossing', {'W': 'waits for signal', 'J': 'crosses against signal', 'P': 'uses phone while crossing'}),
           ('interactions in a school canteen', {'P': 'prosocial', 'N': 'neutral', 'A': 'aggressive'})]


def irr(rng, slot):
    ctx, codes = rng.choice(IRR_CTX)
    n = rng.choice([10, 12, 15, 20])
    keys = list(codes)
    A = [rng.choice(keys) for _ in range(n)]
    dis = rng.randint(1, max(2, n // 3))
    B = list(A)
    for i in rng.sample(range(n), dis):
        B[i] = rng.choice([k for k in keys if k != A[i]])
    agree = sum(1 for x, y in zip(A, B) if x == y)
    pct = 100 * agree / n
    o1, o2 = two_names(rng)
    legend = ', '.join(f'{k} = {v}' for k, v in codes.items())
    stem = (f'{o1} and {o2} used time sampling to code {ctx} every 30 seconds ({legend}).\n'
            f'{o1}: {" ".join(A)}\n{o2}: {" ".join(B)}\n\n'
            'Calculate the percentage agreement between the two observers and explain whether inter-rater reliability is acceptable.')
    ok = pct >= 80
    return dict(stem=stem, answer=f'{agree}/{n} intervals agree = {pct:.1f}%; {"acceptable" if ok else "not acceptable"} (the usual benchmark is 80%).',
                type='numerical', marks=3,
                markingKey=f'M1 agreements counted: {agree} of {n}. A1 {agree}/{n} x 100 = {pct:.1f}%. R1 {"≥" if ok else "<"} 80%, so '
                f'reliability is {"acceptable" if ok else "too low - refine the behaviour categories and train observers, then re-test"}.',
                gap='G3')


def pct_table(rng, slot):
    cats = rng.choice([('secure', 'insecure-avoidant', 'insecure-resistant'), ('integration', 'assimilation', 'separation'),
                       ('helped', 'did not help', 'helped after a delay'), ('agree', 'neutral', 'disagree'),
                       ('System 1 answer', 'System 2 answer', 'no answer')])
    counts = [rng.randint(5, 60) for _ in cats]
    tot = sum(counts)
    who = name(rng)
    i = rng.randrange(len(cats))
    stem = (f'{who} recorded the following frequencies: ' + '; '.join(f'{c} = {n}' for c, n in zip(cats, counts)) +
            f'. Calculate the percentage of the total that was "{cats[i]}" (to 1 decimal place) and identify the modal category.')
    modal = cats[counts.index(max(counts))]
    if counts.count(max(counts)) > 1:
        return None
    return dict(stem=stem, answer=f'{100 * counts[i] / tot:.1f}%; modal category: {modal}', type='numerical', marks=2,
                markingKey=f'A1 {counts[i]}/{tot} x 100 = {100 * counts[i] / tot:.1f}%. A1 mode = {modal} ({max(counts)}).')


def methods(kit, key, *kinds):
    R = kit.R
    if 'desc' in kinds:
        R.add(key, 'C3', (1, 5), 'numerical')(desc_stats)
    if 'two' in kinds:
        R.add(key, ('C3', 'C4'), (3, 5), 'numerical')(desc_two)
    if 'spearman' in kinds:
        R.add(key, ('C3', 'C4'), (4, 5), 'numerical')(spearman)
    if 'r' in kinds:
        R.add(key, ('C2', 'C3'), (2, 4), 'explain')(r_interpret)
    if 'irr' in kinds:
        R.add(key, 'C3', (2, 4), 'numerical')(irr)
    if 'pct' in kinds:
        R.add(key, 'C3', (1, 3), 'numerical')(pct_table)


def scenarios(kit, key, items, c=('C3',), d=(1, 4)):
    """Research scenarios (scenario, IV, DV, design, extraneous variable + control, sampling) -> several questions each."""
    def fn(rng, slot):
        sc, iv, dv, design, ev, samp = rng.choice(items)
        q = rng.randrange(6)
        if q == 0:
            return dict(stem=f'{sc} Identify the independent variable and the dependent variable.', answer=f'IV: {iv}. DV: {dv}.',
                        type='short', marks=2, markingKey=f'1 mark IV: {iv}. 1 mark DV: {dv} (must be operationalised, not just named).')
        if q == 1:
            return dict(stem=f'{sc} Write a directional (one-tailed) hypothesis and a null hypothesis for this study.',
                        answer=f'H1: {iv} will affect {dv} in a stated direction; H0: there will be no significant difference in {dv} caused by {iv}.',
                        type='short', marks=3,
                        markingKey=f'2 marks: directional hypothesis that names both operationalised variables ({iv}; {dv}) and a direction. '
                        '1 mark: null hypothesis stating no significant difference/effect (any difference due to chance).')
        if q == 2:
            return dict(stem=f'{sc} Identify the experimental design used and explain one limitation of this design for this study.',
                        answer=f'{design}.', type='short', marks=3,
                        markingKey=f'1 mark design: {design}. 2 marks: limitation explained in context (independent samples - '
                        'participant variables; repeated measures - order effects such as practice/fatigue and demand '
                        'characteristics; matched pairs - matching is time-consuming and never perfect).')
        if q == 3:
            return dict(stem=f'{sc} Suggest one extraneous variable that could affect the results and explain how it could be controlled.',
                        answer=ev, type='short', marks=3,
                        markingKey=f'{ev} 1 mark: plausible extraneous variable; 1 mark: why it could affect the DV; 1 mark: '
                        'appropriate control (standardisation, random allocation, counterbalancing, matching).')
        if q == 4:
            return dict(stem=f'{sc} Identify the sampling technique and explain one way it limits the generalisability of the findings.',
                        answer=samp, type='short', marks=3,
                        markingKey=f'{samp} 1 mark technique; 2 marks: specific explanation of how the sample may be unrepresentative of the target population.')
        return dict(stem=f'{sc} Explain why this study can or cannot establish a cause-and-effect relationship.',
                    answer=f'Because {iv} is manipulated by the researcher and other variables are controlled, a causal '
                    f'claim about its effect on {dv} is possible - provided extraneous variables such as those noted are controlled.'
                    if 'quasi' not in design and 'natural' not in design else
                    f'Because {iv} is not randomly assigned ({design}), confounding participant variables mean causality is limited.',
                    type='explain', marks=3,
                    markingKey='1 mark: whether the IV is manipulated/randomly allocated; 1 mark: role of controls/confounds; '
                    '1 mark: conclusion about causality applied to this study.')
    kit.R.add(key, c, d, 'short')(fn)


# =============================================================================================
# Mock material (Paper 2 practical questions, unseen studies, Paper 3 source sets)
# =============================================================================================
PRACTICALS_G11 = [
    ('With reference to the experiment you conducted in class, explain how you operationalised the dependent variable.',
     'Answer names the DV of the student\'s own experiment and states exactly how it was measured (e.g. "number of words correctly recalled out of 20 within 2 minutes"), explaining why this precise definition allows replication and reliable scoring.'),
    ('Explain one way in which you controlled an extraneous variable in your class experiment.',
     'Names a specific extraneous variable (e.g. noise, time of day, instructions, order effects) and the control used (standardised instructions read from a script, same room, counterbalancing, random allocation), explaining how this protected internal validity.'),
    ('Explain why you chose the experimental design you used in your class practical.',
     'States the design (independent samples, repeated measures or matched pairs) and justifies it for that study, e.g. repeated measures to remove participant variables with counterbalancing to reduce order effects, or independent samples to avoid demand characteristics/practice effects.'),
    ('Describe how informed consent and the right to withdraw were ensured in your class observation.',
     'Describes the consent procedure (information sheet / verbal briefing; parental consent for under-16s, or observation only of public behaviour where consent is not required), how participants were told they could withdraw (including their data), confidentiality via codes, and debriefing.'),
    ('Explain one limitation of the sampling technique used in your class experiment and how it affects generalisability.',
     'Identifies the technique (usually opportunity sampling of classmates/IB students) and explains that participants share age, education and culture (WEIRD), so findings may not transfer to other populations; suggests random or stratified sampling from a wider population.'),
    ('Explain how you established inter-rater reliability in your class observation.',
     'Two (or more) observers coded the same behaviour independently using the same behaviour checklist, then agreement was calculated (percentage agreement or correlation); ≥80% was taken as acceptable; categories were refined and observers trained if agreement was low.'),
    ('Describe the behaviour categories used in your observation and explain why operational definitions were needed.',
     'Lists the categories (e.g. "on-task: eyes on worksheet or teacher"), explaining that clear, observable, mutually exclusive definitions reduce observer bias and allow consistent coding and replication.'),
    ('Explain one way in which demand characteristics may have affected the results of your class experiment.',
     'Participants (often classmates) may have guessed the aim and changed behaviour (e.g. trying harder in one condition); explains the likely direction of the effect and how a single-blind procedure or cover story could reduce it.'),
    ('Explain why you chose to use a covert or an overt observation in your class practical.',
     'Justifies the choice: covert reduces participant reactivity (Hawthorne effect) but raises consent issues and is only acceptable in public settings; overt is more ethical but behaviour may change; links to the specific setting observed.'),
    ('Describe the descriptive statistics you used to summarise the results of your experiment and justify your choice.',
     'States the measures used (mean/median and SD/range), linking the choice to the level of measurement (interval vs ordinal) and to whether there were outliers; mentions the graph used (bar chart of means).'),
    ('Suggest one modification to the procedure of your class experiment and explain how it would improve its validity.',
     'A specific modification (e.g. counterbalancing, larger random sample, a pilot study, standardised timing) with an explanation of which threat to validity it reduces.'),
    ('Explain one ethical consideration you had to take into account when replicating a published study in class.',
     'E.g. protection from harm when using a stress or memory task, deception about the true aim (avoid or debrief fully), confidentiality of scores, or the right to withdraw; explains how it was managed in the student\'s practical.'),
]

UNSEEN_G11 = [
    ('Music and revision', 'A teacher in Lisbon recruited 30 volunteers from her Grade 11 classes. Fifteen students revised a list of '
     '30 Portuguese-English word pairs while listening to pop music with lyrics; the other fifteen revised in silence. Students '
     'chose which group to join. After 10 minutes, all were tested in the same classroom. The silent group recalled a mean of 21.4 '
     'pairs (SD 3.1) and the music group 16.2 pairs (SD 5.8). The teacher concluded that music damages learning for all students.',
     ['independent samples design, but self-allocation to conditions means participant variables (e.g. students who prefer silence may be stronger learners) confound the IV',
      'volunteer sample from one teacher\'s classes - small, culturally narrow, may be motivated; limits generalisability',
      'DV is clearly operationalised (pairs recalled) and test conditions were standardised - a strength for replication',
      'larger SD in the music group suggests individual differences in response to music; the "all students" conclusion over-generalises',
      'no inferential test reported, so the difference may be due to chance',
      'teacher-researcher bias and demand characteristics: students may know the expected result; power relationship affects voluntary consent and right to withdraw',
      'improvement: random allocation, a different researcher, pilot, music without lyrics as a third condition']),
    ('Screen time and toddlers', 'Researchers in Seoul asked 120 parents of two-year-olds (recruited at three private clinics) to '
     'complete an online questionnaire estimating their child\'s daily screen time and to rate their child\'s vocabulary using a '
     'checklist. A correlation of r = -0.34 was found between screen time and vocabulary. Newspaper reports said "Screens slow '
     'down language development".',
     ['correlational design - no manipulation; the causal headline is not justified (bidirectionality, third variables such as parental education or time spent reading)',
      'parent self-report of screen time and vocabulary - social desirability and recall bias in measurement',
      'sample from private clinics - higher socio-economic status, limits generalisability to the wider population',
      'r = -0.34 is a weak-to-moderate negative correlation; much variance unexplained',
      'strengths: reasonably large sample, quick, ethical way to study a variable that could not be manipulated experimentally',
      'ethics: consent from parents, data privacy of online responses, responsibility of the media when reporting',
      'improvement: longitudinal design with objective screen-time logs and standardised language assessments by blind assessors']),
    ('Peer presence and risk-taking', 'In a laboratory in Melbourne, 40 university students (aged 18-21) played a computer driving game '
     'in which they could stop at amber lights or risk crossing. Each participant played once alone and once with two friends '
     'watching; the order was the same for all (alone first). Risky crossings rose from a mean of 4.1 to 7.3 with friends present.',
     ['repeated measures design controls participant variables', 'no counterbalancing - practice or boredom effects (order effects) confound peer presence',
      'high control in the lab but low ecological validity: a game is not real driving, no real consequences',
      'sample of university students aged 18-21 - WEIRD, narrow age band; cannot conclude about younger adolescents',
      'friends watching may create demand characteristics', 'ethics: low risk; informed consent and debriefing required; no deception needed',
      'improvement: counterbalance order, include adolescent and adult age groups (as Gardner and Steinberg, 2005, did)']),
    ('Leading questions in a police interview study', 'Sixty adults from a community centre in Nairobi watched a 40-second video of a '
     'shop theft. Half were asked "How tall was the large man who grabbed the bag?" and half "How tall was the man who took the '
     'bag?". The first group estimated the thief\'s height as 6 cm taller on average. The researchers concluded that eyewitness '
     'memory is unreliable in real crimes.',
     ['independent samples with a single manipulated IV (question wording) - allows a causal conclusion about leading questions in this setting',
      'video lacks the emotional arousal and consequences of a real crime (cf. Yuille and Cutshall, 1986) - limited ecological validity',
      'community-centre sample adds diversity beyond students but may not be random',
      'allocation method not stated - need random allocation', 'a 6 cm difference needs an inferential test and effect size',
      'ethics: mild deception about aim, no harm; debrief', 'conclusion about "real crimes" over-generalises']),
    ('Mindfulness app and stress', 'A technology company in Singapore tested its own mindfulness app. Employees who signed up for the '
     'app (n = 85) completed the Perceived Stress Scale before and after 6 weeks of use. Mean scores fell from 22.0 to 17.5. No '
     'control group was used. The company advertised that the app "reduces stress by 20%".',
     ['repeated measures but no control group - changes could be due to time, regression to the mean or placebo/expectancy effects',
      'self-selected sample: motivated employees; drop-outs not reported (attrition bias)',
      'funding bias / conflict of interest - the company tested its own product; researcher not independent',
      'PSS is a standardised, reliable measure - a strength', 'the 20% claim uses the drop in mean (4.5/22 = about 20%) but not significance or clinical meaning',
      'ethics: workplace pressure to participate; confidentiality of health data',
      'improvement: randomised controlled trial with waiting-list control, independent researchers, follow-up']),
]

P3_G11 = [
    dict(theme='Sleep and memory in adolescence',
         sources=['(Interview extract, hypothetical study of 12 students in Toronto) "When I sleep less than six hours before a test I '
                  'blank on things I definitely knew... I drink energy drinks so I can stay up revising, but then I remember less." '
                  '"My phone is the problem. I tell myself one video and then it\'s 2 a.m."',
                  '(Quantitative data, hypothetical experiment) Mean number of words recalled from a 30-word list after 8 hours\' sleep: '
                  '18.6 (SD 3.2); after 4 hours\' sleep: 13.1 (SD 4.9). n = 24, repeated measures, counterbalanced. Wilcoxon test: p = 0.003.',
                  '(Method summary, hypothetical survey) 1,500 adolescents in Lima completed an online survey on bedtime, phone use and '
                  'self-rated school performance. Later bedtimes correlated with lower self-rated performance (r = -0.29).'],
         q1=(0, 'Identify three factors that the students in Source A believe affect their memory.',
             'Short sleep (less than six hours); energy drinks / staying up late revising; phone use delaying sleep.'),
         q2=(1, 'Interpret the results presented in Source B.',
             'Recall was higher after 8 hours (mean 18.6) than after 4 hours (13.1), a difference of 5.5 words; greater SD after 4 hours (4.9 vs 3.2) means less consistent performance; p = 0.003 < 0.05, so the difference is significant and unlikely to be due to chance; the counterbalanced repeated-measures design supports a causal effect of sleep deprivation.'),
         q3=(2, 'Evaluate the research method described in Source C.',
             'Strength: large sample, quick, ecologically valid self-reports of real habits. Limitations: correlational - no causation (third variables such as stress or workload); self-rated performance is subjective and prone to social desirability; online sample may exclude students without internet; r = -0.29 is weak; single city limits generalisability.'),
         q4=('Using all the sources and your own knowledge, discuss how far the sources support the claim that lack of sleep impairs learning in adolescents.',
             'Source B gives the strongest causal evidence (controlled, counterbalanced, significant) but small sample and artificial task; Source C shows the pattern in real life with a large sample but is correlational and self-reported; Source A adds insight into mechanisms (phone use, energy drinks) but is a small qualitative sample. Triangulation across methods strengthens the claim; own knowledge: hippocampus and consolidation, adolescent circadian shift (later melatonin release). Conclusion: well supported for short-term recall, less certain for long-term learning.')),
    dict(theme='Social media and well-being',
         sources=['(Focus group extract, hypothetical study, Oslo) "I compare myself with influencers and feel ugly." "Group chats '
                  'are how I keep my friends - without them I\'d be lonely." "Likes make me check my phone all the time."',
                  '(Quantitative data, hypothetical experiment) Students randomly allocated to limit social media to 30 minutes a day '
                  'for 3 weeks (n = 70) reported a fall in loneliness scores from 42.1 to 36.4; the control group (n = 73) changed from '
                  '41.8 to 41.2. Mann-Whitney U test: p = 0.02.',
                  '(Method summary, hypothetical longitudinal study) 3,000 Canadian adolescents completed yearly questionnaires for '
                  'four years. Increases in a teenager\'s social media use were followed by small increases in depressive symptoms '
                  'the following year (β = 0.07).'],
         q1=(0, 'Identify three effects of social media described by the participants in Source A.',
             'Upward social comparison leading to negative body image ("feel ugly"); maintaining friendships / reducing loneliness through group chats; compulsive checking driven by likes (reward).'),
         q2=(1, 'Interpret the findings presented in Source B.',
             'The limited group\'s loneliness fell by 5.7 points vs 0.6 in controls; p = 0.02 < 0.05 so the difference between groups is significant; random allocation supports a causal conclusion that reducing use lowers loneliness, at least over 3 weeks.'),
         q3=(2, 'Evaluate the research method used in Source C.',
             'Strengths: large sample, longitudinal - shows temporal order (use precedes symptoms), within-person change. Limitations: still correlational - third variables (e.g. stress, family conflict); self-report; very small effect size (β = 0.07); attrition over four years; one culture.'),
         q4=('Using all the sources and your own knowledge, evaluate the claim that social media use harms adolescents\' well-being.',
             'A shows both harmful (comparison) and beneficial (connection) effects; B provides experimental support for a causal effect but short duration and student sample; C suggests a small longitudinal effect. Own knowledge: social comparison theory, dopamine and variable reinforcement, displacement of sleep. Conclusion: effects are real but small and depend on how social media is used; "harms" is too general.')),
    dict(theme='Acculturation and stress in international students',
         sources=['(Interview extract, hypothetical study of 10 students from Ghana studying in Vienna) "At home elders decide with you; '
                  'here everyone wants you to decide alone." "Speaking German in class makes me anxious." "The African student '
                  'association feels like family."',
                  '(Quantitative data, hypothetical survey, n = 240 international students) Acculturation strategy and mean '
                  'acculturative stress (1-5): integration 2.1; assimilation 2.8; separation 3.0; marginalisation 3.9.',
                  '(Method summary) Researchers translated an English acculturation questionnaire into Korean, Arabic and Spanish '
                  'without back-translation and gave it to students during orientation week.'],
         q1=(0, 'Identify three sources of acculturative stress or support mentioned in Source A.',
             'Differences in cultural norms (collectivist vs individualist decision making); language anxiety; social support from a co-national student association.'),
         q2=(1, 'Interpret the data in Source B with reference to Berry\'s acculturation model.',
             'Stress is lowest for integration (2.1) and highest for marginalisation (3.9), with assimilation and separation in between - consistent with Berry (1997) that maintaining heritage culture while engaging with the host culture is the most adaptive strategy; but the data are correlational and stress may also influence strategy.'),
         q3=(2, 'Evaluate the method described in Source C.',
             'No back-translation risks non-equivalence of meaning (imposed etic, measurement bias); orientation week is atypical (early in the process, high excitement or stress); questionnaire allows a large sample and comparison; suggest back-translation, pilot testing, and measuring at several time points.'),
         q4=('Using all the sources and your own knowledge, discuss what the sources suggest about the relationship between acculturation and mental health.',
             'Synthesises A (qualitative mechanisms: norms, language, support), B (pattern consistent with Berry), C (measurement concerns that weaken B-type evidence). Own knowledge: Lueck and Wilson (2010) - language discrimination and family conflict increase stress, bilingualism protects. Conclusion: integration is associated with better outcomes, but causality and measurement equivalence are uncertain.')),
    dict(theme='Eyewitness memory and police interviewing',
         sources=['(Interview extract, hypothetical study with police officers in Cape Town) "We used to ask \'Was he carrying a knife?\' '
                  'Now we say \'Tell me everything you remember.\'" "Witnesses who are terrified sometimes remember the weapon and '
                  'nothing else."',
                  '(Quantitative data, hypothetical experiment) Correct details recalled about a staged event: cognitive interview mean '
                  '41.2 (SD 6.0), standard interview mean 29.8 (SD 7.5); incorrect details: 4.1 vs 3.6. n = 30 per group.',
                  '(Method summary) Researchers interviewed 13 real witnesses to an armed robbery five months after the event and '
                  'compared their accounts with police records.'],
         q1=(0, 'Identify three points about eyewitness memory made by the officers in Source A.',
             'Leading/closed questions can distort recall; open free recall is now preferred; high fear may narrow attention to a weapon (weapon focus).'),
         q2=(1, 'Interpret the results in Source B.',
             'The cognitive interview produced 11.4 more correct details on average with a similar number of errors (4.1 vs 3.6), so it increased accuracy without a large increase in errors; SDs show reasonable consistency; an inferential test is needed to confirm significance.'),
         q3=(2, 'Evaluate the method in Source C.',
             'High ecological validity (real crime, real emotion) as in Yuille and Cutshall (1986); but very small sample, no control over what was originally seen, police records may themselves be incomplete, and witnesses who agreed may differ from those who refused; ethics of re-exposing witnesses to trauma.'),
         q4=('Using all the sources and your own knowledge, discuss the extent to which eyewitness testimony can be considered reliable.',
             'A and B suggest reliability depends on interview technique; C (and Yuille and Cutshall) suggests real witnesses can be accurate over months; own knowledge: Loftus and Palmer (1974) leading questions, Loftus and Pickrell (1995) false memories, schema theory. Conclusion: reliability is conditional - better with open, non-leading interviews and when the witness was not exposed to post-event information.')),
]

P1_CH_G11 = [1, 4, 5, 6, 7, 8, 9, 10]
P2_CH_G11 = [2, 3, 11, 12]
K = Kit(unseen=UNSEEN_G11, p3=P3_G11, practicals=PRACTICALS_G11, p1_ch=P1_CH_G11, p2_ch=P2_CH_G11)
R = K.R

MOCK = [
    dict(section='Paper 1, Section A - short answer', count=2, c=['C2'], d=[2, 3], marks=4, style='p1a', chapters=P1_CH_G11),
    dict(section='Paper 1, Section B - applied short answer', count=2, c=['C3'], d=[3, 4], marks=6, style='p1b', chapters=P1_CH_G11),
    dict(section='Paper 1, Section C - extended response (answer one of two)', count=2, c=['C4'], d=[4, 5], marks=15, style='p1x', chapters=P1_CH_G11),
    dict(section='Paper 2, Section A - practical-based questions', count=4, c=['C3'], d=[3, 4], marks=5, style='p2q', chapters=P2_CH_G11),
    dict(section='Paper 2, Section B - evaluation of an unseen study', count=1, c=['C4'], d=[5], marks=15, style='p2u', chapters=P2_CH_G11),
    dict(section='Paper 3 - Question 1 (source-based)', count=1, c=['C3'], d=[2], marks=3, style='p3q1'),
    dict(section='Paper 3 - Question 2 (source-based)', count=1, c=['C3'], d=[3], marks=6, style='p3q2'),
    dict(section='Paper 3 - Question 3 (source-based)', count=1, c=['C4'], d=[4], marks=6, style='p3q3'),
    dict(section='Paper 3 - Question 4 (source-based synthesis)', count=1, c=['C4'], d=[5], marks=15, style='p3q4'),
]


def init(subject_id):
    K.init()


def templates(st):
    return K.templates(st)


# =============================================================================================
# CONTENT
# =============================================================================================
# ---------------------------------------------------------------------------------------------
# ch01 Introduction to Psychology: concepts, content and contexts
# ---------------------------------------------------------------------------------------------
K.facts('ch01-st1', F(
    terms=[('psychology', 'the scientific study of behaviour and mental processes, using systematic, empirical methods'),
           ('biological approach', 'the approach that explains behaviour in terms of the brain, the nervous system, hormones and genetics'),
           ('cognitive approach', 'the approach that explains behaviour in terms of mental processes such as perception, memory, thinking and decision-making'),
           ('sociocultural approach', 'the approach that explains behaviour in terms of the influence of other people, groups and culture'),
           ('empirical evidence', 'evidence gathered through systematic observation or measurement rather than intuition or authority'),
           ('introspection', 'a method used by Wilhelm Wundt in which trained observers report on their own conscious experience under controlled conditions')],
    facts=[('Who opened the first laboratory dedicated to experimental psychology, in Leipzig in 1879?', 'Wilhelm Wundt', ['William James', 'Sigmund Freud', 'B. F. Skinner'],
            'Wundt\'s Leipzig laboratory (1879) is conventionally taken as the start of psychology as a separate experimental science.'),
           ('Which content area of the IB Psychology course would most directly study the effect of cortisol on memory?', 'Biological', ['Sociocultural', 'Developmental', 'Humanistic'],
            'Cortisol is a hormone; hormones are part of the biological content area (though the outcome, memory, is cognitive).'),
           ('Which of the following is one of the four contexts in the IB Psychology guide (first assessment 2027)?', 'Health and well-being', ['Abnormal psychology', 'Psychology of sport', 'Forensic psychology'],
            'The four contexts are health and well-being, human development, human relationships, and learning and cognition.'),
           ('Which of the following is NOT one of the six concepts in the IB Psychology course?', 'Free will', ['Bias', 'Causality', 'Responsibility'],
            'The six concepts are bias, causality, change, measurement, perspective and responsibility.')],
    why=[('Explain why psychology is considered a science.', 'It uses empirical methods (experiments, observations, surveys) to test hypotheses derived from theories, aims for objectivity, replication and peer review, and revises theories when evidence contradicts them - e.g. the multi-store model was revised as evidence for working memory emerged.'),
         ('Explain why the biological, cognitive and sociocultural approaches can explain the same behaviour differently.', 'Each focuses on a different level of explanation: aggression may be explained by testosterone and the amygdala (biological), hostile attribution bias (cognitive) or observational learning and cultural norms (sociocultural); each asks different questions and uses different methods.'),
         ('Explain why psychologists study both behaviour and mental processes.', 'Behaviour is observable but mental processes (memory, thinking, emotion) cause and shape it; mental processes cannot be observed directly so they are inferred from behaviour and measured indirectly, e.g. reaction times or brain imaging.')],
    contrast=[('the cognitive approach', 'the sociocultural approach', 'The cognitive approach locates explanations inside the individual\'s mental processes (e.g. schemas), whereas the sociocultural approach locates them in social and cultural influences on the individual (e.g. norms, group membership).'),
              ('the biological approach', 'the cognitive approach', 'The biological approach explains behaviour through physical structures and processes (neurons, hormones, genes), while the cognitive approach explains it through information processing (attention, memory, thinking), often without specifying the neural basis.')],
    misc=[('Psychology is just common sense.', 'Many findings contradict common sense - e.g. Milgram (1963) found 65% of participants obeyed to 450 V, while psychiatrists predicted about 0.1% would; systematic research is needed because intuition is biased.'),
          ('The three approaches are rival theories, so only one of them can be correct.', 'They are complementary levels of explanation; most behaviour (e.g. depression) is best explained by interacting biological, cognitive and sociocultural factors.'),
          ('Psychology only studies people with mental disorders.', 'Psychology studies all behaviour and mental processes - memory, relationships, learning, development - in typical as well as atypical populations.')],
    cases=[('a teenager in Mumbai who becomes anxious before exams', 'Priya, 16, studies in Mumbai. Before exams her heart races and she cannot sleep; she believes she will fail and disappoint her family, whose expectations are high.', 'the three approaches to behaviour', 'biological: activation of the HPA axis and cortisol release; cognitive: negative appraisal and catastrophising ("I will fail"); sociocultural: family expectations and a competitive, collectivist exam culture - each approach explains a different part of the anxiety'),
           ('a person who starts smoking at university', 'Mateo begins smoking in his first year at university in Bogotá after joining friends who smoke; he says it helps him relax.', 'the three approaches to behaviour', 'sociocultural: observational learning and group norms; cognitive: expectancy that smoking relieves stress; biological: nicotine acts as a dopamine-releasing agonist, reinforcing the behaviour'),
           ('the rise of a viral online challenge', 'Thousands of teenagers copy a risky stunt seen on short-video apps after influencers post it.', 'the sociocultural approach', 'it shows social learning (models rewarded with likes), conformity to group norms and the role of media in transmitting behaviour')],
    apply=[('A researcher wants to know why some people remember faces better than others. Suggest one question that each of the biological, cognitive and sociocultural approaches might ask.', 'Biological: is the fusiform face area more active or larger? Cognitive: do good recognisers use different encoding strategies or attention? Sociocultural: does exposure to faces of different ethnic groups (the own-race bias) affect recognition?', 3),
           ('Classify each of these research questions by approach: (a) Does oxytocin increase trust? (b) Do schemas distort recall? (c) Does group membership increase favouritism?', '(a) biological - hormone; (b) cognitive - mental representations; (c) sociocultural - social identity/group processes.', 3)],
    evaluate=[('Behaviour is best explained by a single approach.', ['parsimony: a single level is easier to test', 'some behaviours have strong single causes (e.g. HM\'s amnesia after surgery)'],
               ['most behaviours are multi-causal (Caspi et al., 2003: gene x environment)', 'reductionism ignores context and meaning', 'different approaches answer different questions'],
               'A single approach can be useful for a specific research question, but a full explanation usually needs interaction between levels.'),
              ('The biological approach provides the most scientific explanations of behaviour.', ['uses objective measures (fMRI, hormone assays)', 'controlled lab experiments allow causal conclusions'],
               ['cognitive and sociocultural research also uses experiments', 'brain correlates do not equal causes', 'biological measures still involve interpretation and bias'],
               'Biological methods are often more objective, but "scientific" refers to method, not content, so the claim is only partly true.')],
    extended=[('Using one behaviour of your choice, explain how it could be studied from the biological, cognitive and sociocultural approaches, and evaluate the benefit of combining them.', 'Choose a behaviour (e.g. stress, aggression); give a specific explanation and study at each level (e.g. Kiecolt-Glaser et al. 1984; appraisal; social support); evaluate: combining gives a fuller, less reductionist account but is harder to test and may lack parsimony.', 8, 'long')],
))
K.study('ch01-st1', 'Ebbinghaus', 1885, 'the forgetting of nonsense syllables', 'to measure how quickly learned information is forgotten over time',
        'Ebbinghaus learned lists of nonsense syllables (e.g. "WID") himself, then measured how much re-learning time was saved at intervals from 20 minutes to 31 days (the savings method).',
        'forgetting was rapid at first - over half was lost within the first hour or so - and then levelled off (the forgetting curve)',
        'the scientific study of cognitive processes',
        ['first systematic, quantitative study of memory', 'tight control (nonsense syllables avoid prior meaning)', 'the forgetting curve has been replicated (Murre and Dros, 2015)'],
        ['single participant (himself) - limited generalisability and risk of bias', 'nonsense syllables lack ecological validity', 'repeated testing may have produced interference'],
        wrong=['Forgetting was slow at first and then accelerated', 'Meaningful words were forgotten faster than nonsense syllables', 'No forgetting occurred after 24 hours'])
K.study('ch01-st1', 'Asch', 1951, 'conformity to a group majority', 'to investigate whether people conform to a clearly wrong majority judgement',
        '123 male American college students judged line lengths in groups where all other members were confederates who gave the same wrong answer on 12 of 18 critical trials.',
        'participants conformed on about 37% of critical trials; about 75% conformed at least once; in a control condition errors were under 1%',
        'the influence of the group on individual behaviour',
        ['high control and a clear, objective task', 'control condition shows errors were due to social pressure'],
        ['all-male American students in the 1950s (cultural and historical bias)', 'artificial task with low consequences', 'deception and distress'],
        mtype='laboratory experiment', iv='presence of a unanimous majority giving wrong answers (vs control)', dv='percentage of critical trials on which the participant gave the wrong answer',
        ethics='Deception about the aim and the confederates, and stress from disagreeing with the group; participants were debriefed but could not give fully informed consent.',
        wrong=['Participants almost never conformed when the majority was clearly wrong', 'Women conformed more than men', 'Conformity increased when one confederate gave the right answer'],
        culture='Bond and Smith (1996) found higher conformity in collectivist cultures in their meta-analysis of 133 Asch-type studies')
K.study('ch01-st1', 'Raine, Buchsbaum and LaCasse', 1997, 'brain activity in murderers', 'to investigate whether people who had committed murder showed differences in brain functioning',
        'PET scans of 41 people charged with murder who pleaded not guilty by reason of insanity were compared with 41 matched controls while they completed a continuous performance task.',
        'the murderers showed lower glucose metabolism in the prefrontal cortex and abnormal asymmetry in the amygdala and other limbic areas',
        'the role of brain structure and function in violent behaviour',
        ['objective measure of brain activity (PET)', 'matched controls for age and sex'],
        ['correlational - brain differences may be a result rather than a cause', 'special sample (insanity pleas) - not generalisable to all violent offenders', 'reductionist; ignores social factors such as childhood abuse'],
        mtype='quasi-experiment',
        ethics='Socially sensitive research: findings could be misused to argue that offenders are not responsible for their actions; researchers must report results carefully.',
        wrong=['Murderers showed higher prefrontal activity than controls', 'No brain differences were found', 'Differences were found only in the cerebellum'])

K.facts('ch01-st2', F(
    terms=[('bias', 'a systematic distortion in thinking, research design, measurement or interpretation that leads to inaccurate conclusions'),
           ('causality', 'the relationship in which one variable produces a change in another; established most clearly when the IV is manipulated and other variables are controlled'),
           ('measurement', 'the process of operationalising and quantifying (or systematically recording) behaviour and mental processes so that they can be studied'),
           ('perspective', 'the particular viewpoint - theoretical, cultural or personal - from which behaviour is studied and interpreted'),
           ('responsibility', 'the ethical obligations of researchers and practitioners towards participants, society and the use of findings'),
           ('change', 'how behaviour, mental processes, individuals, theories or methods develop or are modified over time'),
           ('confirmation bias', 'the tendency to seek, interpret and remember information that confirms existing beliefs'),
           ('researcher bias', 'the influence of the researcher\'s expectations or beliefs on how a study is designed, conducted or interpreted')],
    facts=[('Which concept is most directly involved when a researcher turns "aggression" into "number of hits on a Bobo doll in 20 minutes"?', 'Measurement', ['Perspective', 'Change', 'Responsibility'],
            'Operationalisation is part of measurement: defining a variable so it can be quantified.'),
           ('A researcher concludes that video games cause aggression from a correlation of r = 0.25. Which concept is the conclusion most clearly misusing?', 'Causality', ['Change', 'Measurement', 'Perspective'],
            'A correlation cannot establish cause and effect.'),
           ('Rosenthal and Jacobson (1968) showed that teacher expectations can change pupils\' performance. Which concept does this most directly illustrate?', 'Bias', ['Causality', 'Measurement', 'Change'],
            'Expectancy effects are a form of bias - expectations systematically distort outcomes.'),
           ('The decision to stop the Stanford Prison Experiment after six days relates most closely to which concept?', 'Responsibility', ['Measurement', 'Causality', 'Perspective'],
            'Researchers have a responsibility to protect participants from harm.')],
    why=[('Explain why measurement is a challenge in psychology.', 'Many variables (memory, stress, attachment) are constructs that cannot be observed directly, so they must be operationalised indirectly (recall scores, cortisol, Strange Situation behaviour); each operationalisation may capture only part of the construct and may introduce bias, so validity must be argued.'),
         ('Explain why perspective matters when interpreting research findings.', 'Researchers bring theoretical and cultural assumptions: a biological perspective may interpret depression as a neurochemical imbalance while a sociocultural one stresses poverty; WEIRD researchers may treat Western norms as universal (imposed etic).'),
         ('Explain why researchers have a responsibility that goes beyond protecting participants.', 'Findings affect society: research on group differences, intelligence or crime can be misreported or used to justify discrimination, so researchers must report results accurately and consider the consequences of publication (socially sensitive research).'),
         ('Explain how the concept of change applies to psychological theories.', 'Theories are revised when new evidence appears - e.g. the multi-store model\'s single STM store was replaced by Baddeley and Hitch\'s (1974) working memory model; neuroplasticity research changed the view that the adult brain is fixed.')],
    contrast=[('researcher bias', 'participant bias', 'Researcher bias comes from the investigator\'s expectations (e.g. how they score responses), whereas participant bias comes from participants changing behaviour because they are being studied (demand characteristics, social desirability).'),
              ('causality', 'correlation', 'Causality means one variable produces a change in another (established by manipulating an IV under control); correlation only shows that two variables co-vary, which may be due to a third variable or reverse causation.')],
    misc=[('If two variables are strongly correlated, one must cause the other.', 'Correlation does not establish causation: a third variable or reverse causality may explain the relationship; only manipulation of an IV with controls supports causal claims.'),
          ('Using a standardised questionnaire removes all bias from measurement.', 'Questionnaires can still be biased by social desirability, acquiescence, translation problems and culturally loaded items; standardisation improves reliability, not necessarily validity.'),
          ('The six concepts are separate topics studied in their own unit.', 'The concepts are lenses applied across all content and contexts, e.g. measurement in brain imaging, bias in eyewitness memory, responsibility in animal research.')],
    cases=[('the Pygmalion effect in classrooms', 'Teachers in a California elementary school were told (falsely) that some randomly chosen pupils were "intellectual bloomers"; a year later those pupils showed larger IQ gains, especially in the youngest grades.', 'bias', 'teachers\' expectations, not pupils\' ability, systematically changed outcomes - an expectancy (researcher/teacher) bias'),
           ('headlines claiming that "screens rot children\'s brains"', 'A newspaper in London reports a correlation between screen time and lower test scores as proof that screens damage the brain.', 'causality', 'correlational data are being presented as causal; family income or sleep could explain both, so the causal claim is unjustified'),
           ('a researcher measuring stress in nurses in Accra', 'A researcher in Accra wants to measure stress in nurses working night shifts and must decide between a questionnaire, saliva cortisol and interviews.', 'measurement', 'each method operationalises stress differently - self-report (subjective, social desirability), cortisol (objective but affected by time of day) and interviews (rich but hard to quantify) - so triangulating methods improves validity')],
    apply=[('A study finds that students who eat breakfast have higher grades. Using two of the six concepts, explain why caution is needed when interpreting this finding.', 'Causality: correlational, so breakfast may not cause grades - family income or routines could explain both. Measurement: how are "breakfast" and "grades" operationalised (self-report may be biased)? Bias/perspective: researchers expecting a link may interpret data selectively.', 4),
           ('A researcher in Hanoi uses a depression questionnaire developed in the USA. Identify one concept that is raised and explain the problem.', 'Measurement/bias (also perspective): items may not have equivalent meaning in Vietnamese culture (e.g. somatic expression of distress), so the questionnaire may under- or over-estimate depression - an imposed etic.', 3)],
    evaluate=[('Bias can never be fully removed from psychological research.', ['researchers are humans with expectations (Rosenthal)', 'participants react to being studied', 'cultural assumptions shape questions'],
               ['double-blind procedures and standardisation greatly reduce bias', 'replication and peer review correct biased findings', 'triangulation and reflexivity make bias visible'],
               'Bias cannot be eliminated entirely, but well-designed, replicated and reflexive research can reduce it to the point where conclusions are credible.'),
              ('Establishing causality is the main goal of psychological research.', ['experiments allow cause-effect conclusions needed for interventions', 'treatments must be shown to cause improvement'],
               ['many questions are descriptive or about meaning (qualitative research)', 'ethics often prevents manipulation of key variables (e.g. trauma)', 'correlational and longitudinal research is valuable for prediction'],
               'Causality is a central goal for explanation and intervention, but understanding, description and prediction are also legitimate aims.')],
    extended=[('With reference to one study, explain how at least three of the six concepts (bias, causality, change, measurement, perspective, responsibility) can be used to evaluate it.', 'E.g. Loftus and Palmer (1974): measurement - speed estimates as DV; causality - lab experiment with manipulated verb; bias - demand characteristics; responsibility - minimal harm; perspective - cognitive view of reconstructive memory. Strong answers apply each concept to specific details.', 8, 'long')],
))
K.ar('ch01-st2', [
    ('Correlational studies cannot establish causality.', 'In a correlational study the researcher does not manipulate an independent variable.', 0, 'Without manipulation and control, a third variable or reverse causation could explain the relationship.'),
    ('Double-blind procedures reduce bias.', 'In a double-blind procedure neither the participant nor the person collecting data knows the condition.', 0, 'Neither side\'s expectations can systematically influence the results.'),
    ('Operationalisation is a feature of the concept of measurement.', 'Operationalisation is only used in qualitative research.', 2, 'A is true; R is false - operationalisation is central to quantitative research.'),
    ('Responsibility is only relevant to researchers who use deception.', 'Researchers must consider the social consequences of their findings.', 3, 'A is false - responsibility applies to all research; R is true.'),
])
K.study('ch01-st2', 'Rosenthal and Jacobson', 1968, 'teacher expectations and pupil performance', 'to investigate whether teachers\' expectations can affect pupils\' intellectual development',
        'Pupils at a California elementary school took an IQ test; teachers were told about 20% (randomly chosen) were "bloomers" expected to make big gains. Pupils were retested after 8 months and a year.',
        'the "bloomers" gained significantly more IQ points than controls, particularly in first and second grade',
        'expectancy bias (the Pygmalion effect)',
        ['field setting gives high ecological validity', 'random selection of "bloomers" supports a causal conclusion'],
        ['effects were mainly in the youngest grades and later replications were mixed', 'ethical problems: deception of teachers and possible harm to control pupils', 'IQ test reliability for young children was questioned'],
        mtype='field experiment', iv='whether teachers were told a pupil was a "bloomer"', dv='gain in IQ test score over the year',
        ethics='Teachers were deceived and some pupils may have received less attention; the potential harm to the control group raises questions of justice and protection from harm.',
        wrong=['Teacher expectations had no measurable effect', 'Pupils labelled "bloomers" performed worse', 'Effects were largest in the oldest grades'])
K.study('ch01-st2', 'Orne', 1962, 'demand characteristics in experiments', 'to show that participants actively try to work out and conform to the purpose of an experiment',
        'Participants were asked to add rows of random numbers on sheets, then tear each completed sheet into pieces and start again; Orne also compared "hypnotised" participants with those simulating hypnosis.',
        'participants persisted for hours at a meaningless task, interpreting it as an endurance test, showing that the experimental setting itself shapes behaviour',
        'demand characteristics as a source of participant bias',
        ['influential demonstration of a real problem in lab research', 'led to the use of single-blind and cover-story procedures'],
        ['largely descriptive demonstrations rather than a single controlled study', 'American student samples'],
        wrong=['Participants quickly refused to continue the meaningless task', 'Participants\' behaviour was unaffected by the research setting', 'Only hypnotised participants persisted'])
K.study('ch01-st2', 'Rosenhan', 1973, 'the reliability of psychiatric diagnosis', 'to test whether psychiatrists could reliably distinguish sane from insane people',
        'Eight healthy pseudo-patients reported hearing voices ("empty", "hollow", "thud") to gain admission to 12 US psychiatric hospitals, then behaved normally.',
        'all were admitted, seven with a diagnosis of schizophrenia; they stayed 7-52 days (mean 19) and were discharged "in remission"; other patients often detected them but staff did not',
        'the reliability of measurement in psychiatric diagnosis',
        ['high ecological validity - real hospitals and staff', 'challenged diagnostic practice and influenced later manuals'],
        ['deception of hospital staff without consent', 'the accuracy of Rosenhan\'s account has since been questioned (Cahalan, 2019)', 'claimed symptoms were real reports, so admission was arguably reasonable'],
        mtype='covert participant observation',
        ethics='Hospital staff were deceived and observed without consent; the study could have damaged trust in psychiatric care.',
        wrong=['None of the pseudo-patients were admitted', 'Staff immediately detected the pseudo-patients', 'Most were diagnosed with depression and discharged within a day'])

K.facts('ch01-st3', F(
    terms=[('interactionism', 'the view that behaviour is best explained by the interaction of biological, cognitive and sociocultural factors rather than by any one alone'),
           ('reductionism', 'explaining a complex behaviour by breaking it down to a single, simpler level such as genes or neurotransmitters'),
           ('gene-environment interaction', 'when the effect of a gene on behaviour depends on the environment, or the effect of the environment depends on the gene'),
           ('diathesis-stress model', 'the model that a disorder develops when a pre-existing vulnerability (diathesis) is triggered by environmental stress'),
           ('epigenetics', 'changes in gene expression caused by environmental factors that do not alter the DNA sequence')],
    facts=[('Caspi et al. (2003) found that the effect of stressful life events on depression depended on which gene variant?', 'The 5-HTT serotonin transporter gene', ['The MAOA gene', 'The SRY gene', 'The FOXP2 gene'],
            'Participants with one or two short 5-HTT alleles were more likely to become depressed after stressful life events.'),
           ('Which model proposes that a disorder results from a vulnerability triggered by stress?', 'The diathesis-stress model', ['The multi-store model', 'The social exchange model', 'The two-factor model'],
            'Diathesis = vulnerability, stress = trigger.'),
           ('Which term describes explaining depression only as a lack of serotonin?', 'Biological reductionism', ['Holism', 'Interactionism', 'Triangulation'],
            'Reducing a complex disorder to one neurochemical is biological reductionism.')],
    why=[('Explain why most behaviour needs more than one level of explanation.', 'Biological, cognitive and sociocultural factors influence one another: genes affect sensitivity to stress, stress changes cognition and hormones, and culture shapes how stress is appraised and expressed - so one level alone gives an incomplete explanation.'),
         ('Explain how the environment can change the expression of genes.', 'Through epigenetic mechanisms such as DNA methylation: e.g. Weaver et al. (2004) showed that rat pups licked more by their mothers had altered methylation of the glucocorticoid receptor gene and lower stress responses.'),
         ('Explain why reductionist explanations are still useful.', 'They allow precise, testable hypotheses and can lead to effective treatments (e.g. SSRIs target serotonin), even though they do not capture the whole behaviour.')],
    contrast=[('reductionism', 'holism', 'Reductionism explains behaviour by breaking it down to one simpler level (e.g. neurotransmitters), whereas holism examines the whole person in context and the interaction of factors.'),
              ('a diathesis', 'a stressor', 'A diathesis is a pre-existing vulnerability (e.g. a gene variant or negative cognitive style); a stressor is the environmental trigger (e.g. bereavement) that activates it.')],
    misc=[('If a behaviour is partly genetic, the environment cannot change it.', 'Genes interact with the environment: Caspi et al. (2003) found the 5-HTT short allele increased depression risk only after stressful life events; environmental change can alter outcomes.'),
          ('Interactionist explanations are always better because they include everything.', 'Including many factors can make explanations vague and hard to test; good interactionist models specify how factors interact (e.g. diathesis-stress).')],
    cases=[('the emotion experienced on a high suspension bridge', 'Men in Vancouver who met an attractive female interviewer on a high, wobbly suspension bridge were more likely to phone her later than men who met her on a low, stable bridge.', 'the interaction of biological and cognitive factors', 'physiological arousal (biological) was misattributed to attraction (cognitive labelling), showing that emotion depends on both arousal and interpretation'),
           ('an adolescent in Seoul who develops depression after academic failure', 'Ji-ho, 17, has a family history of depression. After failing an entrance exam in a highly competitive system, he withdraws and blames himself.', 'the diathesis-stress model', 'a genetic/cognitive vulnerability (family history, self-blaming style) interacts with a sociocultural stressor (exam pressure and stigma of failure) to trigger depression')],
    apply=[('Using the diathesis-stress model, explain why two siblings who experience the same parental divorce may react differently.', 'They may differ in vulnerability (e.g. genetic variants such as the 5-HTT short allele, temperament, cognitive style), so the same stressor triggers depression in the more vulnerable sibling but not in the other; protective factors such as social support also differ.', 4)],
    evaluate=[('Genes determine behaviour.', ['twin studies show significant heritability (Kendler et al., 2006: about 38% for depression)', 'specific gene variants are linked to behaviour'],
               ['heritability is never 100%; environment explains much variance', 'gene effects depend on environment (Caspi et al., 2003)', 'epigenetics shows environment changes gene expression'],
               'Genes influence predispositions but do not determine behaviour; outcomes depend on gene-environment interaction.')],
    extended=[('Discuss how biological, cognitive and sociocultural factors interact in one behaviour you have studied.', 'Choose e.g. depression or stress; show how one factor influences another (gene x life events, cortisol affecting memory/appraisal, culture shaping symptom expression); use studies (Caspi et al., 2003; Dutton and Aron, 1974); evaluate complexity and testability.', 8, 'long')],
))
K.study('ch01-st3', 'Caspi et al.', 2003, 'genes, stress and depression', 'to investigate whether the 5-HTT gene moderates the effect of stressful life events on depression',
        'A longitudinal study of 847 New Zealanders from the Dunedin birth cohort, assessed for 5-HTT genotype, stressful life events between 21 and 26, and depression at 26.',
        'participants with one or two short alleles of 5-HTT showed more depression after stressful life events than those with two long alleles; genotype alone did not predict depression',
        'gene-environment interaction',
        ['large, prospective birth cohort with high retention', 'shows interaction rather than simple genetic determinism'],
        ['correlational - life events not manipulated', 'later meta-analyses (Risch et al., 2009) failed to replicate the effect consistently', 'self-reported life events'],
        mtype='longitudinal study', wrong=['The short allele predicted depression regardless of life events', 'Life events had no effect on depression', 'Only participants with two long alleles became depressed after stress'])
K.study('ch01-st3', 'Dutton and Aron', 1974, 'arousal and attraction on a suspension bridge', 'to investigate whether physiological arousal can be misattributed as sexual attraction',
        'An attractive female interviewer approached male passers-by on either the high, swaying Capilano Suspension Bridge or a low, stable bridge in Vancouver, asked them to complete a questionnaire and gave her phone number.',
        'more men on the suspension bridge called the interviewer (about half vs about an eighth) and wrote more sexual imagery in their stories',
        'the interaction of biological arousal and cognitive appraisal in emotion',
        ['field experiment with natural behaviour (high ecological validity)', 'objective behavioural DV (phone calls)'],
        ['participants not randomly allocated - bridge chosen by passers-by (thrill seekers may differ)', 'only men; heterosexual assumption', 'deception and no consent'],
        mtype='field experiment', iv='type of bridge (high-arousal suspension vs low-arousal stable)', dv='whether the man phoned the interviewer and sexual imagery in stories',
        ethics='Participants were unaware they were in a study (no informed consent) and were deceived about the interviewer\'s purpose.',
        wrong=['Men on the stable bridge called more often', 'Arousal reduced attraction', 'Neither group called the interviewer'])

# ---------------------------------------------------------------------------------------------
# ch02 Research methods: quantitative approaches
# ---------------------------------------------------------------------------------------------
SCEN_G11 = [
    ('A researcher in Oslo randomly allocates 40 students to learn a word list either in a quiet room or with background television on, then tests recall after 10 minutes.',
     'presence or absence of background television during learning', 'number of words correctly recalled out of 30 after 10 minutes', 'independent samples design',
     'Individual differences in memory ability could differ between groups; controlled by random allocation (or matched pairs on a pre-test).',
     'Likely opportunity/volunteer sampling of students from one school - unrepresentative of other ages and cultures.'),
    ('Twenty volunteers in Kuala Lumpur complete a Stroop test twice: once while hearing recorded traffic noise through headphones and once in silence, a week apart, with the order counterbalanced.',
     'traffic noise vs silence during the task', 'time in seconds to name the ink colours of 40 incongruent colour words', 'repeated measures design',
     'Practice effects from doing the Stroop test twice; controlled by counterbalancing (ABBA) and using different word lists.',
     'Self-selected (volunteer) sample - people interested in concentration tasks may volunteer, so findings may not generalise.'),
    ('In Nairobi, 30 pairs of children are matched on age and reading level; one child from each pair is taught with picture cards and the other with text only, then given a vocabulary test.',
     'teaching method (picture cards vs text only)', 'score on a 25-item vocabulary test', 'matched pairs design',
     'Teacher enthusiasm could differ between methods; controlled by using the same teacher and a standardised script.',
     'Children from participating schools selected by opportunity - schools that agree may differ from others.'),
    ('A psychologist in Toronto compares stress scores of nurses who work night shifts with nurses who work day shifts.',
     'shift type (night vs day) - a naturally occurring IV', 'score on the Perceived Stress Scale', 'quasi-experiment with independent groups',
     'Nurses choose their shifts, so age or family circumstances may confound the results; measure and statistically control them.',
     'Purposive sample of nurses at one hospital - may not generalise to other hospitals or countries.'),
    ('Participants in Singapore watch a car-crash video and are asked "About how fast were the cars going when they smashed into each other?" or "...hit each other?"',
     'verb used in the critical question (smashed vs hit)', 'estimated speed in km/h', 'independent samples design',
     'Driving experience could affect speed estimates; random allocation spreads it across groups.',
     'University students recruited by opportunity sampling - narrow age range and little driving experience.'),
    ('Researchers in Lima test whether people remember more words when tested in the same room where they learned them than in a different room. Each participant does both conditions with different word lists.',
     'testing context (same room vs different room)', 'number of words recalled from a 20-word list', 'repeated measures design',
     'Word lists may differ in difficulty; controlled by matching lists for word frequency and length and counterbalancing.',
     'Opportunity sample of students on campus - may not represent older adults.'),
    ('A study in Vienna compares the number of helping acts performed by children who watched a prosocial cartoon with those who watched a neutral cartoon.',
     'type of cartoon (prosocial vs neutral)', 'number of times the child helped pick up dropped pencils in a 5-minute test', 'independent samples design',
     'Existing differences in helpfulness between children; controlled by random allocation.',
     'Children whose parents gave consent - a self-selected sample biased towards cooperative families.'),
    ('In Mexico City, students rate their mood (1-10) after 20 minutes of exercise and after 20 minutes of sitting, on two different days.',
     'activity (exercise vs sitting)', 'self-rated mood on a 1-10 scale', 'repeated measures design',
     'Demand characteristics - participants may guess that exercise is expected to improve mood; use a cover story and a single-blind researcher.',
     'Volunteer sample from a sports club - unrepresentative of inactive people.'),
    ('A researcher in Dubai measures heart rate of participants who are told they will give a speech in 5 minutes compared with participants told they will read silently.',
     'expectation of giving a speech vs reading silently', 'heart rate in beats per minute', 'independent samples design',
     'Baseline fitness and caffeine intake differ between people; take a baseline reading and ask participants to avoid caffeine.',
     'Opportunity sample of staff at one company - limited age and cultural range.'),
    ('In Seoul, 50 adolescents and 50 adults play a computer driving game, and the number of risky decisions is recorded with or without peers watching.',
     'age group and peer presence', 'number of risky decisions (crossing on amber) in the game', 'mixed design: age is a quasi-IV (independent groups); peer presence could be repeated measures',
     'Familiarity with video games may differ between age groups; record gaming experience and match groups.',
     'Self-selected volunteers responding to an advertisement - gamers may be over-represented.'),
]
K.facts('ch02-st1', F(
    terms=[('independent variable (IV)', 'the variable the researcher manipulates or changes to see its effect on another variable'),
           ('dependent variable (DV)', 'the variable that is measured to see whether it is affected by the IV'),
           ('operationalisation', 'defining a variable precisely in terms of how it will be manipulated or measured, so it can be tested and replicated'),
           ('extraneous variable', 'any variable other than the IV that could affect the DV if not controlled'),
           ('confounding variable', 'an extraneous variable that varies systematically with the IV, so its effect cannot be separated from that of the IV'),
           ('null hypothesis', 'a statement that there will be no significant difference or relationship, and any observed effect is due to chance'),
           ('directional hypothesis', 'a prediction that states the direction of the expected difference or relationship (one-tailed)'),
           ('standardisation', 'keeping procedures, instructions and conditions the same for all participants')],
    facts=[('Which of the following is the best operationalised DV for "memory"?', 'Number of words correctly recalled from a 20-word list after 5 minutes', ['How good the participant\'s memory is', 'Whether the participant remembers things', 'Memory ability in general'],
            'An operationalised DV states exactly what is measured and how.'),
           ('In a laboratory experiment, which feature most allows a cause-and-effect conclusion?', 'The IV is manipulated while extraneous variables are controlled', ['Participants are observed in their natural environment', 'Data are collected using interviews', 'Participants are matched on age'],
            'Manipulation of the IV plus control of other variables isolates its effect on the DV.'),
           ('Which type of experiment involves an IV that changes naturally, which the researcher does not manipulate?', 'A natural experiment', ['A laboratory experiment', 'A field experiment', 'A correlational study'],
            'E.g. Charlton et al. (2000): the arrival of television on St Helena.'),
           ('Which of the following is a non-directional (two-tailed) hypothesis?', 'There will be a difference in recall between participants tested with and without music', ['Participants tested in silence will recall more words than those tested with music', 'Music will decrease recall', 'There will be no difference in recall'],
            'A two-tailed hypothesis predicts a difference without stating its direction.')],
    why=[('Explain why it is important to operationalise variables.', 'Operationalisation makes variables measurable and precise, so the hypothesis can be tested objectively, data can be scored consistently (reliability) and other researchers can replicate the study.'),
         ('Explain why laboratory experiments may lack ecological validity.', 'The artificial setting and tasks (e.g. learning word lists) differ from real life, and participants know they are being studied, so behaviour may not reflect how people act in everyday situations.'),
         ('Explain why random allocation to conditions is important.', 'It spreads participant variables (ability, motivation, personality) evenly across conditions by chance, so differences in the DV are more likely due to the IV rather than to pre-existing group differences.')],
    contrast=[('a laboratory experiment', 'a field experiment', 'Both manipulate an IV, but a lab experiment takes place in a controlled, artificial environment (high control, low ecological validity), whereas a field experiment takes place in the participants\' natural setting (higher ecological validity, less control, often no consent).'),
              ('an extraneous variable', 'a confounding variable', 'An extraneous variable is any uncontrolled variable that might affect the DV; it becomes a confounding variable when it varies systematically with the IV, so its effect cannot be separated from the IV\'s.'),
              ('a natural experiment', 'a quasi-experiment', 'In a natural experiment the IV is a naturally occurring event (e.g. arrival of TV); in a quasi-experiment the IV is a pre-existing characteristic of participants (e.g. gender, age) - in neither is it manipulated or randomly assigned.')],
    misc=[('A null hypothesis predicts that the IV will have the opposite effect to the experimental hypothesis.', 'The null hypothesis predicts no significant difference or relationship; any difference is due to chance.'),
          ('Field experiments always have higher validity than laboratory experiments.', 'Field experiments have higher ecological validity but lower control, so internal validity can be lower because extraneous variables are harder to control.')],
    cases=[('the arrival of television on St Helena', 'Television was introduced to the island of St Helena in 1995; researchers recorded children\'s playground behaviour before and after.', 'a natural experiment', 'the IV (presence of TV) changed naturally, not by the researcher, so the study has high ecological validity but cannot control other changes on the island'),
           ('a café study of music tempo', 'A researcher in Melbourne alternates fast and slow background music on different days in a café and records how quickly customers finish their drinks.', 'a field experiment', 'the IV (music tempo) is manipulated in a natural setting; customers behave naturally but do not consent and other variables (weather, crowding) vary')],
    apply=[('A researcher hypothesises that sleep deprivation affects reaction time. Operationalise both the IV and the DV.', 'IV: hours of sleep the night before testing, e.g. normal 8 hours vs restricted to 4 hours. DV: mean reaction time in milliseconds to press a key when a light appears, over 20 trials.', 3)],
    evaluate=[('Laboratory experiments are the most useful method in psychology.', ['allow causal conclusions', 'high control and replicability', 'precise measurement'],
               ['low ecological validity and demand characteristics', 'some variables cannot be manipulated ethically', 'WEIRD samples limit generalisability'],
               'Lab experiments are the strongest method for testing causal hypotheses, but their usefulness depends on the question; triangulation with field and qualitative methods is needed.')],
    extended=[('Design an experiment to test whether background music affects the recall of words. Refer to the IV, DV, hypotheses, design, sample and controls.', 'IV operationalised (lyrics vs silence); DV operationalised (words recalled out of 20 after 2 minutes); H1 and H0; design justified (independent samples with random allocation or repeated measures with counterbalancing); sample and technique; standardised instructions, same room, same time; ethics.', 8, 'multi_step')],
))
scenarios(K, 'ch02-st1', SCEN_G11, c=('C3',), d=(1, 4))
K.study('ch02-st1', 'Godden and Baddeley', 1975, 'context-dependent memory in divers', 'to investigate whether recall is better when it takes place in the same environment as learning',
        '18 divers learned lists of 36 words either on land or 6 m underwater and recalled them either on land or underwater, giving four conditions.',
        'recall was about 40% higher when the learning and recall environments matched than when they did not',
        'context-dependent retrieval in memory',
        ['realistic natural environments for divers', 'four-condition design isolates the effect of matching context'],
        ['small, specialised sample (divers)', 'difficult to control conditions underwater (e.g. cheating, equipment problems)', 'repeated measures may cause order effects'],
        mtype='field experiment', iv='whether the learning and recall environments matched (land/underwater)', dv='number of words correctly recalled out of 36',
        wrong=['Recall was best when learning and recall environments differed', 'Divers recalled more underwater regardless of where they learned', 'Environment had no effect on recall'])
K.study('ch02-st1', 'Charlton et al.', 2000, 'television and children\'s behaviour on St Helena', 'to investigate whether the introduction of television increased antisocial behaviour in children',
        'Children aged 3-8 on the island of St Helena were video-recorded in school playgrounds before (1993-1995) and up to five years after television arrived in 1995; behaviour was coded and teacher ratings were collected.',
        'there was no significant increase in antisocial behaviour after TV arrived; most measures of behaviour stayed the same',
        'natural experiments as a way to study an IV that cannot ethically be manipulated',
        ['natural setting - high ecological validity', 'longitudinal before/after measures'],
        ['no control over other changes on the island', 'small, close-knit community with strong social controls - limited generalisability'],
        mtype='natural experiment',
        wrong=['Aggression among children doubled after TV arrived', 'Prosocial behaviour disappeared after TV arrived', 'Boys became more aggressive but girls less'])

K.facts('ch02-st2', F(
    terms=[('independent samples design', 'an experimental design in which different participants take part in each condition'),
           ('repeated measures design', 'an experimental design in which the same participants take part in every condition'),
           ('matched pairs design', 'an experimental design in which participants are matched on relevant variables and one member of each pair is assigned to each condition'),
           ('order effects', 'changes in performance caused by the order of conditions, such as practice, fatigue or boredom, in a repeated measures design'),
           ('counterbalancing', 'a technique to control order effects in which half the participants do condition A then B and half do B then A'),
           ('participant variables', 'individual differences between participants (e.g. ability, age, personality) that may affect the DV')],
    facts=[('Which experimental design is most at risk from participant variables?', 'Independent samples', ['Repeated measures', 'Matched pairs', 'A within-subjects design'],
            'Different people in each condition means individual differences may confound the results.'),
           ('A researcher has half the participants do condition A then B and the other half B then A. What is this technique called?', 'Counterbalancing', ['Random allocation', 'Matching', 'Standardisation'],
            'Counterbalancing (ABBA) controls order effects.'),
           ('Which design was used by Stroop (1935), where all participants named ink colours for both congruent and incongruent words?', 'Repeated measures', ['Independent samples', 'Matched pairs', 'Quasi-experimental groups'],
            'The same participants completed both conditions.')],
    why=[('Explain why a matched pairs design reduces participant variables.', 'Each participant in one condition is paired with a similar participant (e.g. same age and IQ) in the other, so key individual differences are balanced across conditions without the order effects of repeated measures.'),
         ('Explain why repeated measures designs can increase demand characteristics.', 'Participants experience all conditions, so they are more likely to work out the aim of the study and change their behaviour to fit (or spoil) it.')],
    contrast=[('a repeated measures design', 'an independent samples design', 'In repeated measures the same participants do all conditions (controls participant variables but risks order effects); in independent samples different participants do each condition (no order effects but participant variables may differ).')],
    misc=[('Counterbalancing removes order effects completely.', 'Counterbalancing does not remove order effects; it balances them across conditions so they do not systematically favour one condition.'),
          ('Matched pairs designs need twice as many participants as repeated measures.', 'Matched pairs requires different participants in each condition (like independent samples), so it needs more participants than repeated measures, but the main issue is that matching is time-consuming and never perfect.')],
    cases=[('a revision-app trial in Accra', 'A school in Accra wants to compare two revision apps. Students differ widely in prior attainment, and each app covers the same material.', 'choosing an experimental design', 'repeated measures is unsuitable because the material is the same (practice effects), so matched pairs on prior attainment is best - it controls participant variables without order effects')],
    apply=[('A researcher wants to test whether chewing gum improves concentration. Explain which experimental design you would use and why.', 'Repeated measures with counterbalancing (gum vs no gum, different but equivalent tasks) controls individual differences in concentration; or independent samples if practice effects on the task are likely - justification must be linked to the study.', 4)],
    evaluate=[('Repeated measures is the best experimental design.', ['controls participant variables', 'needs fewer participants'],
               ['order effects and demand characteristics', 'not possible when conditions cannot be undone (e.g. teaching methods)', 'needs equivalent materials'],
               'The best design depends on the IV and DV: repeated measures is efficient where order effects can be counterbalanced; otherwise matched pairs or independent samples are preferable.')],
))
methods(K, 'ch02-st2', 'two')
scenarios(K, 'ch02-st2', SCEN_G11[::-1], c=('C3',), d=(2, 4))
K.study('ch02-st2', 'Mueller and Oppenheimer', 2014, 'laptop versus longhand note-taking', 'to investigate whether taking notes on a laptop or by hand affects learning from lectures',
        'Princeton students were randomly assigned to take notes on a laptop or by hand while watching TED talks, then answered factual and conceptual questions.',
        'both groups did similarly on factual questions, but longhand note-takers did better on conceptual questions; laptop users wrote more words and more verbatim notes',
        'the effect of note-taking method on deeper processing',
        ['random allocation to conditions', 'measured both factual and conceptual learning'],
        ['student sample from an elite US university', 'short-term test; a replication by Morehead et al. (2019) found weaker effects'],
        mtype='laboratory experiment', iv='note-taking method (laptop vs longhand)', dv='score on factual and conceptual questions about the lecture',
        wrong=['Laptop users performed better on conceptual questions', 'Longhand note-takers wrote more verbatim notes', 'Neither method affected conceptual understanding'])
K.study('ch02-st2', 'Stroop', 1935, 'interference in colour naming', 'to investigate whether the meaning of a colour word interferes with naming the ink colour',
        'Participants named the ink colours of colour words printed in incongruent colours (e.g. "RED" in blue ink) and of colour patches/congruent stimuli; times were compared within participants.',
        'naming the ink colour of incongruent words took significantly longer than naming colour patches (about 74% longer in one experiment)',
        'automatic processing of word meaning',
        ['repeated measures controls participant variables', 'highly replicable effect used widely in research'],
        ['order effects if not counterbalanced', 'artificial task; mainly literate American students'],
        mtype='laboratory experiment', iv='type of stimulus (incongruent colour words vs colour patches)', dv='time in seconds to name the ink colours of a list',
        wrong=['Incongruent words were named faster than colour patches', 'Word meaning had no effect on colour naming time', 'Only children showed interference'])

K.facts('ch02-st3', F(
    terms=[('correlation', 'a statistical relationship between two co-variables, expressed by a coefficient between -1 and +1'),
           ('positive correlation', 'a relationship in which, as one co-variable increases, the other also tends to increase'),
           ('negative correlation', 'a relationship in which, as one co-variable increases, the other tends to decrease'),
           ('co-variables', 'the two measured variables in a correlational study'),
           ('third variable problem', 'the possibility that an unmeasured variable causes both co-variables, producing a correlation without a direct causal link'),
           ('bidirectional ambiguity', 'the problem that, in a correlation, it is unclear which variable influences the other'),
           ('scattergram', 'a graph that plots each participant\'s scores on two co-variables to show the direction and strength of a correlation')],
    facts=[('A correlation coefficient of -0.85 indicates which of the following?', 'A strong negative correlation', ['A weak negative correlation', 'A strong positive correlation', 'No correlation'],
            'The sign gives direction and the size (close to 1) gives strength.'),
           ('Rahe, Mahan and Arthur (1970) found a correlation of about +0.118 between life change units and illness in navy personnel. How is this best described?', 'A weak positive correlation', ['A strong positive correlation', 'A weak negative correlation', 'A perfect correlation'],
            '+0.118 is positive but close to zero, so weak.'),
           ('Which of the following is a strength of correlational research?', 'It can study variables that cannot ethically be manipulated', ['It establishes cause and effect', 'It removes all extraneous variables', 'It always uses random samples'],
            'E.g. stress and illness cannot be manipulated, but can be measured and correlated.')],
    why=[('Explain why correlational studies cannot establish causality.', 'Neither variable is manipulated, so a third variable may cause both (e.g. poverty causing both stress and illness), and the direction of influence is unclear (bidirectional ambiguity).'),
         ('Explain why a correlation can still be useful even though it does not show causation.', 'It allows prediction, identifies relationships worth testing experimentally, and can study variables that cannot ethically or practically be manipulated (e.g. trauma, brain volume).')],
    contrast=[('a correlational study', 'an experiment', 'An experiment manipulates an IV and measures its effect on a DV, allowing causal conclusions; a correlational study measures two co-variables as they naturally occur and only shows whether they are related.')],
    misc=[('A correlation of 0.00 means there is a strong relationship between the variables.', 'A coefficient of 0 means no linear relationship; strength increases as the value approaches +1 or -1.'),
          ('A negative correlation means there is no relationship.', 'A negative correlation is a relationship in which one variable increases as the other decreases; it can be strong (e.g. -0.9).')],
    cases=[('the London taxi driver brain scans', 'Maguire et al. (2000) found that the longer people had worked as London taxi drivers, the larger their posterior hippocampi.', 'correlation and causality', 'the positive correlation suggests that navigation experience changes the brain, but because it is correlational, people with larger hippocampi might be more likely to become (and stay) taxi drivers'),
           ('screen time and well-being in adolescents', 'Large surveys of US adolescents found that more hours of daily screen use were associated with slightly lower well-being.', 'the third variable problem', 'factors such as loneliness, family conflict or poor sleep could cause both high screen use and low well-being, so screens cannot be assumed to be the cause')],
    apply=[('A school counsellor in Geneva finds r = -0.62 between hours of part-time work and exam grades. Write a suitable correlational hypothesis and explain one conclusion and one limitation.', 'H1: there will be a negative correlation between weekly hours of part-time work and exam grades. Conclusion: moderate negative relationship - students who work more tend to get lower grades. Limitation: cannot say work causes lower grades; e.g. family financial pressure could affect both.', 4)],
    evaluate=[('Correlational research is of limited value in psychology because it cannot show cause and effect.', ['cannot establish causality', 'third variables and bidirectionality'],
               ['allows study of variables that cannot be manipulated', 'large samples and real-world data', 'basis for experimental hypotheses and prediction'],
               'Correlations cannot show causation, but they are essential for prediction and for studying real-world variables; combined with longitudinal and experimental designs they contribute strongly.')],
))
methods(K, 'ch02-st3', 'r', 'spearman')
K.study('ch02-st3', 'Rahe, Mahan and Arthur', 1970, 'life events and illness in navy personnel', 'to investigate whether life change units were related to illness',
        'About 2,500 US Navy sailors on three cruisers completed the Schedule of Recent Experiences for the previous six months before a tour of duty; illness records were kept during the 6-8 month tour.',
        'there was a weak positive correlation (about +0.118) between life change units and illness scores',
        'the correlation between stress and health',
        ['large sample', 'illness measured from medical records rather than self-report'],
        ['weak correlation; cannot show causation', 'all-male, US military sample', 'retrospective self-report of life events may be inaccurate'],
        mtype='correlational study', wrong=['There was a strong negative correlation between life events and illness', 'Life change units had no relationship with illness', 'Illness caused sailors to report more life events'])
K.study('ch02-st3', 'Twenge and Campbell', 2018, 'screen time and adolescent well-being', 'to examine the association between screen time and psychological well-being in children and adolescents',
        'Analysis of a large US national survey of over 40,000 children aged 2-17, measuring hours of daily screen use and indicators such as curiosity, emotional stability and diagnoses of anxiety or depression.',
        'more hours of screen time were associated with lower well-being, with heavy users (7+ hours a day) more than twice as likely to have been diagnosed with anxiety or depression as light users',
        'the limits of correlational evidence about technology',
        ['very large, nationally representative sample'],
        ['correlational - direction of effect unknown', 'parent-reported screen time', 'small effect sizes; other analyses of similar data (Orben and Przybylski, 2019) found effects comparable to eating potatoes'],
        mtype='correlational study')

K.facts('ch02-st4', F(
    terms=[('target population', 'the group of people the researcher wants to generalise the findings to'),
           ('random sampling', 'a sampling technique in which every member of the target population has an equal chance of being selected'),
           ('opportunity sampling', 'a sampling technique that uses people who are available and willing at the time of the study'),
           ('self-selected sampling', 'a sampling technique in which participants volunteer, for example by responding to an advertisement'),
           ('purposive sampling', 'a sampling technique in which participants are deliberately chosen because they have characteristics relevant to the research question'),
           ('snowball sampling', 'a sampling technique in which initial participants recruit further participants from their own networks, used for hard-to-reach groups'),
           ('representative sample', 'a sample whose characteristics match those of the target population'),
           ('stratified sampling', 'a sampling technique in which the population is divided into subgroups and participants are randomly selected from each in proportion to their size')],
    facts=[('Milgram (1963) recruited participants through a newspaper advertisement. Which sampling technique is this?', 'Self-selected (volunteer) sampling', ['Random sampling', 'Opportunity sampling', 'Snowball sampling'],
            'Participants chose to respond to the advertisement.'),
           ('A researcher studying undocumented migrants asks each interviewee to introduce others they know. Which sampling technique is this?', 'Snowball sampling', ['Purposive sampling', 'Random sampling', 'Stratified sampling'],
            'Snowball sampling is used to reach hidden or hard-to-reach populations.'),
           ('Which sampling technique is most likely to produce a representative sample?', 'Stratified random sampling', ['Opportunity sampling', 'Self-selected sampling', 'Snowball sampling'],
            'Random selection within proportional strata reduces sampling bias.'),
           ('What does the acronym WEIRD stand for in the critique by Henrich, Heine and Norenzayan (2010)?', 'Western, educated, industrialised, rich and democratic', ['Western, empirical, individualist, rational and developed', 'White, educated, independent, rich and democratic', 'Western, ethical, industrial, reliable and diverse'],
            'They argued that most psychology samples come from WEIRD societies.')],
    why=[('Explain why opportunity samples may lead to biased findings.', 'The researcher selects whoever is available (often students in one place), so the sample may share age, education and culture and differ systematically from the target population, limiting generalisability.'),
         ('Explain why purposive sampling is often used in qualitative research.', 'Qualitative research seeks rich, in-depth data on a specific experience, so participants are chosen because they have that experience (e.g. survivors of an earthquake); representativeness is less important than relevance.'),
         ('Explain why self-selected samples can be biased.', 'Volunteers tend to be more motivated, curious or helpful than non-volunteers (volunteer bias), so they may respond differently from the wider population.')],
    contrast=[('random sampling', 'opportunity sampling', 'Random sampling gives every member of the target population an equal chance of selection (less bias but needs a full list and is time-consuming); opportunity sampling uses whoever is available (quick and cheap but likely to be unrepresentative).'),
              ('purposive sampling', 'snowball sampling', 'In purposive sampling the researcher selects participants with relevant characteristics; in snowball sampling participants recruit further participants, which helps reach hidden populations but may produce a network of similar people.')],
    misc=[('A random sample is always representative of the target population.', 'Random sampling reduces bias but a small random sample can still be unrepresentative by chance; larger samples and stratification help.'),
          ('Asking students in the school canteen to take part is random sampling.', 'This is opportunity sampling - only those present and willing can be selected, so not everyone has an equal chance.')],
    cases=[('the WEIRD critique', 'Arnett (2008) found that about 96% of participants in top psychology journals came from Western industrialised countries that make up about 12% of the world\'s population.', 'sampling bias and generalisability', 'findings from narrow samples may not generalise; Henrich et al. (2010) showed that even "basic" effects such as the Müller-Lyer illusion vary across cultures'),
           ('a study of nurses\' stress in Mumbai', 'A researcher in Mumbai wants to interview nurses who have worked in intensive care during a pandemic and asks the first nurses she interviews to put her in touch with colleagues.', 'snowball and purposive sampling', 'nurses are chosen because of their relevant experience (purposive) and then recruit others (snowball), giving access but risking a network of like-minded participants')],
    apply=[('A researcher wants to study the effect of social media on the self-esteem of 13-15-year-olds in Lisbon. Recommend a sampling technique and explain one strength and one limitation of it in this context.', 'E.g. stratified random sampling from school registers by age and gender: strength - more representative of 13-15-year-olds; limitation - needs access to registers and consent from many schools and parents, and those who decline may differ.', 4)],
    evaluate=[('Findings from WEIRD samples cannot be generalised to the rest of the world.', ['cultural differences in perception, cognition and social behaviour (Henrich et al., 2010)', '96% of samples from 12% of the population (Arnett, 2008)'],
               ['some processes (e.g. basic memory capacity, neurotransmitter effects) appear universal', 'cross-cultural replications sometimes confirm findings'],
               'WEIRD findings should not be assumed to be universal; generalisability must be tested by cross-cultural replication.')],
))
K.study('ch02-st4', 'Henrich, Heine and Norenzayan', 2010, 'the generalisability of findings from WEIRD samples', 'to review whether findings based on Western, educated, industrialised, rich and democratic samples can be generalised to humans in general',
        'A review of cross-cultural evidence across domains such as visual perception, fairness, cooperation, spatial reasoning and self-concept.',
        'WEIRD participants were frequently outliers - e.g. more susceptible to the Müller-Lyer illusion and more individualistic - so they are among the least representative populations',
        'the problem of sampling bias in psychology',
        ['large range of evidence across domains', 'highly influential in improving sampling practices'],
        ['a narrative review - selection of studies may be biased', 'the WEIRD category may hide large differences within Western societies'],
        mtype=None)
methods(K, 'ch02-st4', 'pct')

# ---------------------------------------------------------------------------------------------
# ch03 Research methods: qualitative approaches, ethics and evaluation
# ---------------------------------------------------------------------------------------------
K.facts('ch03-st1', F(
    terms=[('qualitative research', 'research that collects non-numerical data (words, meanings, experiences) to understand how people interpret their world'),
           ('semi-structured interview', 'an interview with a set of prepared questions or topics but flexibility to follow up and ask new questions'),
           ('case study', 'an in-depth investigation of a single individual, group or event using multiple methods, often over time'),
           ('focus group', 'a group interview of about 6-10 participants who discuss a topic guided by a moderator, so that interaction between participants generates data'),
           ('participant observation', 'an observation in which the researcher joins the group being studied'),
           ('covert observation', 'an observation in which the participants do not know they are being observed'),
           ('naturalistic observation', 'observing behaviour in its natural setting without the researcher intervening')],
    facts=[('Which qualitative method was used by Festinger, Riecken and Schachter (1956) to study a doomsday group?', 'Covert participant observation', ['Structured interview', 'Laboratory experiment', 'Focus group'],
            'Researchers joined the group posing as believers.'),
           ('Which method is most suitable for studying how a group of teenagers jointly construct opinions about vaping?', 'A focus group', ['A laboratory experiment', 'A correlational study', 'A twin study'],
            'Focus groups capture interaction and shared meaning-making.'),
           ('Curtiss (1977) studied "Genie", a girl isolated until age 13. Which method is this?', 'A case study', ['A field experiment', 'A cross-sectional survey', 'A natural experiment with a control group'],
            'An in-depth study of one individual using observations, tests and interviews over years.')],
    why=[('Explain why qualitative methods are useful for studying people\'s experiences.', 'They produce rich, detailed data in participants\' own words, revealing meanings, motives and context that numbers miss - e.g. Becker et al.\'s (2002) interviews showed Fijian girls linked thinness to social success after TV arrived.'),
         ('Explain why case studies are difficult to generalise.', 'They focus on one unique individual or group (e.g. HM, Genie), so findings may reflect their specific characteristics and history; however, they can disprove universal claims and generate hypotheses.'),
         ('Explain why covert observation raises ethical concerns.', 'Participants cannot give informed consent or exercise the right to withdraw, and their privacy may be invaded; it is usually only acceptable in public places where people would expect to be observed, or with strong justification and debriefing.')],
    contrast=[('a structured interview', 'an unstructured interview', 'A structured interview uses fixed questions in a fixed order for all participants (comparable, reliable data), while an unstructured interview is like a guided conversation with no fixed questions (rich, flexible data that are harder to compare).'),
              ('overt observation', 'covert observation', 'In overt observation participants know they are being observed (ethical, but risks reactivity), while in covert observation they do not (more natural behaviour, but no consent).')],
    misc=[('Qualitative research is unscientific because it does not use numbers.', 'Qualitative research is systematic and can be rigorous through credibility checks, triangulation, reflexivity and transparent analysis; its aim is understanding meaning rather than measuring variables.'),
          ('A focus group is simply several individual interviews done at the same time.', 'A focus group uses group interaction as data - participants respond to and build on each other\'s comments, which can reveal shared norms but also conformity.')],
    cases=[('the introduction of television in Fiji', 'After television arrived in Nadroga province, Fiji, in 1995, researchers surveyed adolescent girls in 1995 and 1998 and interviewed a subsample in 1998.', 'the value of interviews in mixed-methods research', 'the survey showed eating-disorder risk rose, while the interviews explained why: girls admired thin TV characters and linked thinness to career success'),
           ('a researcher joining an online gaming community in Seoul', 'A researcher creates a gaming account and spends six months in an online community to understand how young men build friendships there, without revealing she is a researcher.', 'covert participant observation', 'it gives access to natural interaction but raises issues of consent, deception and the researcher becoming too involved (going native)')],
    apply=[('A researcher in Cape Town wants to understand how adolescents experience moving to a new school. Recommend a qualitative method and justify your choice.', 'A semi-structured interview: allows comparison across a common set of topics while letting participants describe their own experiences in depth and the researcher probe further; a focus group could be used for shared experiences, but individual interviews protect privacy on sensitive issues.', 4)],
    evaluate=[('Case studies have little scientific value.', ['cannot be generalised', 'researcher bias and reliance on interpretation', 'cannot be replicated'],
               ['provide rich data on rare phenomena (HM, Genie)', 'can falsify universal claims', 'generate hypotheses for experiments'],
               'Case studies have limited generalisability but considerable scientific value, especially for rare cases and theory building.')],
))
K.study('ch03-st1', 'Festinger, Riecken and Schachter', 1956, 'a group that predicted the end of the world', 'to observe how members of a doomsday group would respond when their prophecy failed',
        'The researchers joined a small group in the USA whose leader predicted a flood on 21 December 1954, posing as believers and recording members\' behaviour before and after the date.',
        'when the flood did not happen, the most committed members did not abandon their beliefs but began recruiting more actively, consistent with reducing cognitive dissonance',
        'how belief is maintained when expectations are disconfirmed',
        ['naturalistic, in-depth data that could not be gained by an experiment', 'supported cognitive dissonance theory in a real setting'],
        ['the researchers\' presence may have strengthened the group\'s beliefs (reactivity)', 'notes written from memory in secret', 'unique group - limited generalisability'],
        mtype='covert participant observation', ethics='The researchers deceived the group and observed them without consent; they may also have influenced members\' beliefs.',
        wrong=['Members abandoned the group immediately after the prophecy failed', 'The leader admitted the prophecy was false', 'Members stopped talking to outsiders after the failed prophecy'])
K.study('ch03-st1', 'Becker et al.', 2002, 'television and eating attitudes in Fiji', 'to investigate the impact of the introduction of Western television on disordered eating attitudes in Fijian adolescent girls',
        'Ethnic Fijian schoolgirls completed the EAT-26 questionnaire in 1995 (just after TV arrived) and in 1998; in 1998 a subsample of 30 girls also took part in semi-structured interviews.',
        'the percentage scoring high on the EAT-26 rose from 12.7% to 29.2%, and self-induced vomiting to control weight rose from 0% to 11.3%; interviews revealed admiration for TV characters and a link between thinness and success',
        'the role of interviews in explaining cultural change in behaviour',
        ['mixed methods - triangulation of survey and interview data', 'natural before/after comparison'],
        ['different girls in 1995 and 1998 (not the same individuals)', 'other social changes in Fiji could explain the change', 'self-report and translation issues'],
        wrong=['Disordered eating attitudes fell after TV arrived', 'There was no change in EAT-26 scores', 'Only boys showed increased concern with weight'])
K.study('ch03-st1', 'Curtiss', 1977, 'Genie, a child deprived of language', 'to study the language development of a girl who had been severely isolated until age 13',
        'Genie was found in Los Angeles in 1970 after years of isolation and neglect; she was studied over several years with observations, language tests and recordings.',
        'Genie learned many words but never developed normal grammar, consistent with a critical period for language acquisition',
        'the critical period hypothesis for language',
        ['rich, longitudinal data on a rare case', 'tested a hypothesis that could never ethically be tested experimentally'],
        ['unique case - possible pre-existing developmental problems', 'conflicts between researchers\' roles (carers and scientists)', 'confidentiality and exploitation concerns'],
        mtype='case study', ethics='Genie could not give informed consent; the dual role of researchers and carers raised concerns about her being exploited for research rather than cared for.')

K.facts('ch03-st2', F(
    terms=[('informed consent', 'agreement to take part in research given freely by a participant who has been told the aims, procedures and risks'),
           ('deception', 'misleading participants or withholding information about the true aim or procedure of a study'),
           ('debriefing', 'giving participants full information about the study after it ends, including its true aim and any deception, and checking their well-being'),
           ('right to withdraw', 'the right of participants to leave the study at any time, and to withdraw their data, without penalty'),
           ('protection from harm', 'the obligation to ensure participants experience no more physical or psychological risk than in everyday life'),
           ('confidentiality', 'keeping participants\' personal data private and not identifying them in reports'),
           ('anonymity', 'ensuring that participants cannot be identified from the data, e.g. by not recording names'),
           ('cost-benefit analysis', 'weighing the potential benefits of research against the possible costs to participants before approving it')],
    facts=[('Which professional body publishes the Code of Human Research Ethics followed by many IB schools?', 'The British Psychological Society (BPS)', ['The World Health Organization', 'The International Baccalaureate Organization', 'UNESCO'],
            'The BPS and the APA publish the most widely used codes.'),
           ('Who must give consent for a 14-year-old to take part in a class practical?', 'The participant and a parent or guardian', ['Only the participant', 'Only the teacher', 'No one, if the study is anonymous'],
            'IB and BPS guidelines require parental consent for participants under 16.'),
           ('In Milgram\'s (1963) study, what percentage of participants continued to the maximum 450-volt level?', '65%', ['15%', '35%', '90%'],
            '26 of 40 participants obeyed to the end.'),
           ('Which ethical guideline was most clearly breached in Watson and Rayner (1920)?', 'Protection from harm', ['Confidentiality', 'Anonymity', 'Use of animals'],
            'Albert was conditioned to fear a white rat and was never deconditioned.')],
    why=[('Explain why deception is sometimes used in psychological research.', 'Knowing the true aim could change behaviour (demand characteristics), so mild deception may be needed for valid data - e.g. Asch could not tell participants about the confederates; it is acceptable only if justified, harmless and followed by full debriefing.'),
         ('Explain why debriefing is important.', 'It reveals the true aim and any deception, returns participants to their pre-study state, offers the right to withdraw data and checks for harm - e.g. Milgram\'s participants were reunited with the "learner".'),
         ('Explain why IB students must not use deception or harm in class practicals.', 'IB ethical guidelines prohibit practicals that cause stress, use deception that participants would object to, or involve ingesting substances such as food, drink or drugs; students are not trained to manage harm and participants are often peers who may feel unable to refuse.')],
    contrast=[('confidentiality', 'anonymity', 'Confidentiality means the researcher knows who the participants are but keeps their data private; anonymity means participants\' identities are not recorded at all, so data cannot be linked to them.'),
              ('informed consent', 'presumptive consent', 'Informed consent is given by each participant after being told about the study; presumptive consent is inferred by asking a similar group whether they would have agreed, used when informing participants would spoil the study.')],
    misc=[('If participants give informed consent, any procedure is ethical.', 'Consent does not override protection from harm; researchers must still minimise risk, respect the right to withdraw and debrief; consent can also be compromised by pressure or authority.'),
          ('The right to withdraw means participants can leave only before data collection begins.', 'Participants can withdraw at any point, including after the study, when they may ask for their data to be destroyed.'),
          ('Ethics only concerns how participants are treated during the study.', 'Ethics also covers how findings are reported and used (socially sensitive research), data storage and privacy, and the treatment of animals.')],
    cases=[('Milgram\'s obedience study', 'Participants believed they were giving increasingly strong electric shocks to a learner; many showed extreme stress - sweating, trembling, nervous laughter - yet the experimenter told them "you have no other choice, you must go on".', 'ethical guidelines in research', 'it breached protection from harm, used deception, and the prods undermined the right to withdraw; Milgram defended it with debriefing and a follow-up in which 84% said they were glad to have taken part'),
           ('a class practical on stress', 'Two IB students in Geneva plan to make classmates believe they will have to give a surprise speech, in order to measure their heart rate.', 'ethics in student research', 'it involves deception and potential psychological harm with peers who may feel pressured, so it breaches IB ethical guidelines; a safer alternative would use a non-stressful task with full consent')],
    apply=[('A student plans to observe how often classmates check their phones in the library, without telling them. Identify two ethical issues and suggest how each could be addressed.', 'Consent - it may be acceptable as a public-place observation, but participants should be debriefed afterwards or the observation made overt; confidentiality - record no names or identifying details; right to withdraw - offer to destroy data on request.', 4)],
    evaluate=[('Research that breaks ethical guidelines should never be carried out, however useful the findings.', ['protection of participants is fundamental', 'harm can be lasting (Little Albert)', 'trust in psychology depends on ethics'],
               ['some important findings (Milgram) depended on deception', 'cost-benefit analysis can justify minor breaches', 'guidelines change over time'],
               'Serious harm can never be justified, but minor deception with debriefing may be acceptable after an ethics committee\'s cost-benefit analysis.')],
))
K.study('ch03-st2', 'Milgram', 1963, 'obedience to authority', 'to investigate how far people would obey an authority figure who instructed them to harm another person',
        '40 male volunteers from New Haven, recruited by newspaper advertisement, acted as "teachers" giving apparent shocks of 15-450 V to a confederate "learner" at Yale University when he made errors; the experimenter used four standard prods.',
        '65% (26/40) went to the maximum 450 V and all went to at least 300 V; many showed extreme tension',
        'the power of situational factors in obedience',
        ['high control and standardised prods', 'many later variations isolated situational factors (e.g. proximity, location)'],
        ['deception and severe distress', 'all-male American volunteers', 'Perry (2013) found some participants doubted the shocks were real'],
        mtype='laboratory experiment', ethics='Participants were deceived about the shocks, experienced severe stress, and the prods made it difficult to exercise the right to withdraw; Milgram debriefed them and found 84% were glad to have participated.',
        wrong=['Only about 1% of participants went to 450 V', 'No participant went beyond 150 V', 'Women obeyed more than men in the original study'])
K.study('ch03-st2', 'Haney, Banks and Zimbardo', 1973, 'the Stanford prison simulation', 'to investigate how readily people would conform to the roles of guard and prisoner in a simulated prison',
        '24 male student volunteers, screened as psychologically healthy, were randomly assigned to be guards or prisoners in a mock prison in the basement of Stanford University; Zimbardo acted as superintendent.',
        'guards became increasingly abusive and prisoners passive and distressed; five prisoners were released early and the study was stopped after six days instead of fourteen',
        'the influence of social roles on behaviour',
        ['random allocation to roles', 'rich observational data'],
        ['Zimbardo\'s dual role created researcher bias', 'demand characteristics - guards may have acted as they thought was wanted (Le Texier, 2019)', 'small all-male sample'],
        mtype='laboratory experiment', ethics='Participants suffered psychological harm; the researcher\'s dual role as superintendent compromised his duty to protect them and to respect their right to withdraw.')
K.study('ch03-st2', 'Watson and Rayner', 1920, 'conditioned fear in an infant', 'to investigate whether a fear response could be classically conditioned in a human infant',
        'An 11-month-old infant, "Little Albert", was shown a white rat while a steel bar was struck loudly behind him; after several pairings he was shown the rat alone.',
        'Albert came to cry at the rat alone and the fear generalised to similar objects (a rabbit, a fur coat)',
        'classical conditioning of emotional responses',
        ['first demonstration that emotional responses can be conditioned in humans'],
        ['single participant', 'poorly controlled and subjectively measured', 'never deconditioned'],
        ethics='The infant was deliberately caused distress, his mother may not have given fully informed consent, and he was never deconditioned - a clear breach of protection from harm.')

K.facts('ch03-st3', F(
    terms=[('internal validity', 'the extent to which a study measures what it intends to and shows that changes in the DV are caused by the IV, not by other variables'),
           ('ecological validity', 'the extent to which findings can be generalised to real-life settings'),
           ('reliability', 'the consistency of a measure or finding - whether it would give the same results if repeated'),
           ('test-retest reliability', 'the consistency of a measure when the same people are tested on two occasions'),
           ('generalisability', 'the extent to which findings from a sample can be applied to the target population and other settings'),
           ('credibility', 'in qualitative research, the extent to which findings accurately reflect the participants\' experiences (similar to internal validity)'),
           ('replication', 'repeating a study, usually with new participants, to see whether the findings are the same'),
           ('social desirability bias', 'the tendency for participants to give answers that present them in a favourable light')],
    facts=[('The Open Science Collaboration (2015) attempted to replicate 100 psychology studies. Roughly what proportion of replications produced significant results?', 'About 36%', ['About 90%', 'About 75%', 'About 5%'],
            'Only about 36% of replications were significant, compared with 97% of the originals.'),
           ('A questionnaire gives very different scores when the same people complete it two weeks apart. Which quality does it lack?', 'Test-retest reliability', ['Ecological validity', 'Credibility', 'Generalisability'],
            'Inconsistency over time shows low reliability.'),
           ('Which of the following is the term for generalisability in qualitative research?', 'Transferability', ['Replicability', 'Objectivity', 'Standardisation'],
            'Transferability: the extent to which findings apply to other settings, judged by readers using thick description.')],
    why=[('Explain why a measure can be reliable but not valid.', 'A measure can give consistent results but measure the wrong thing - e.g. head circumference measured consistently is reliable but is not a valid measure of intelligence.'),
         ('Explain why replication is important in psychology.', 'Replication checks that findings are not due to chance, error or bias; the replication crisis (Open Science Collaboration, 2015) showed many published findings do not replicate, so confidence should depend on repeated evidence.'),
         ('Explain how demand characteristics threaten the validity of an experiment.', 'Participants who guess the aim may change behaviour to help or hinder the researcher, so changes in the DV may be due to their expectations rather than the IV.')],
    contrast=[('internal validity', 'external validity', 'Internal validity concerns whether the study really shows that the IV caused the change in the DV; external validity concerns whether the findings generalise beyond the study to other people, places and times.'),
              ('reliability', 'validity', 'Reliability is the consistency of a measure or finding; validity is whether it measures what it claims to and whether conclusions are accurate.')],
    misc=[('A large sample guarantees that a study is valid.', 'Sample size improves the precision of estimates but does not fix poor measurement, confounding variables or a biased sampling method.'),
          ('If a study has high ecological validity, its findings must be generalisable to all cultures.', 'Ecological validity concerns real-life settings; generalising to other cultures (population validity) requires samples from those cultures.')],
    cases=[('the marshmallow test replication', 'Watts, Duncan and Quan (2018) repeated the marshmallow test with about 900 more diverse children and found that the link between delay at age 4 and achievement at 15 was about half the original size and largely explained by family background.', 'generalisability and replication', 'the original Stanford sample was small and privileged; a more representative sample showed weaker effects, illustrating how sampling limits generalisability'),
           ('a happiness questionnaire in a job interview', 'Applicants to a company in Dubai are asked to rate their life satisfaction on a scale of 1-10 as part of a job interview.', 'social desirability bias', 'applicants will want to appear positive and stable, so scores will be inflated and invalid as a measure of their real well-being')],
    apply=[('A researcher finds that students who used a memory app scored higher in a test. Suggest two questions you would ask to evaluate the credibility of this finding.', 'Were students randomly allocated to use the app (or did keen students choose it - confounding)? Was the test the same and marked blind? Also: sample size, significance, replication, funding by the app company.', 4)],
    evaluate=[('Psychology is in a replication crisis, so its findings cannot be trusted.', ['only about 36% of replications were significant (OSC, 2015)', 'publication bias and p-hacking', 'small samples'],
               ['many core findings replicate well (Stroop, serial position)', 'reforms: pre-registration, open data, larger samples', 'non-replication may reflect cultural or historical change'],
               'The replication crisis shows the need for caution and reform, but it does not mean all findings are untrustworthy; well-replicated findings remain credible.')],
))
K.study('ch03-st3', 'Open Science Collaboration', 2015, 'the reproducibility of psychological research', 'to estimate how many published psychology findings could be reproduced',
        '270 researchers attempted to replicate 100 studies from three leading psychology journals (2008), using the original materials where possible and high-powered designs.',
        '97% of the original studies had significant results but only about 36% of the replications did; effect sizes in replications were about half the size',
        'the reliability of published psychological research',
        ['large, coordinated, transparent project with pre-registered protocols'],
        ['a single replication attempt per study', 'some replications differed from the originals in sample or culture (Gilbert et al., 2016)'],
        mtype='meta-analysis', wrong=['Over 90% of findings were replicated', 'Replication effect sizes were larger than the originals', 'No findings from social psychology could be replicated'])
K.study('ch03-st3', 'Watts, Duncan and Quan', 2018, 'replicating the marshmallow test', 'to test whether the link between early delay of gratification and later achievement replicated in a larger, more diverse sample',
        'Data from about 900 children in the US NICHD Study of Early Child Care were analysed; delay time at 54 months was correlated with achievement at age 15, controlling for family background and early cognitive ability.',
        'the association was about half the size of earlier findings and, once family background and early ability were controlled, it became very small',
        'the generalisability of findings from narrow samples',
        ['larger and more diverse sample than Mischel\'s Stanford children', 'statistical control of confounding variables'],
        ['correlational', 'the procedure differed slightly from the original'],
        mtype='longitudinal study')
K.study('ch03-st3', 'Mischel, Ebbesen and Zeiss', 1972, 'delay of gratification in pre-school children', 'to investigate how cognitive strategies affect children\'s ability to delay gratification',
        'Pre-school children at the Stanford University nursery were offered one treat now or two if they waited for the experimenter to return; conditions varied whether the treats were visible and whether children were given distraction instructions.',
        'children waited longer when the rewards were hidden or when they were given distracting thoughts; later follow-ups linked longer waiting to higher adolescent competence',
        'the role of cognitive strategies in self-control',
        ['controlled manipulation of attention and distraction'],
        ['small sample of children of Stanford staff and students', 'later replication (Watts et al., 2018) found weaker long-term links'],
        mtype='laboratory experiment', iv='whether rewards were visible and whether distraction instructions were given', dv='time in minutes the child waited before ringing the bell')

K.facts('ch03-st4', F(
    terms=[('triangulation', 'using more than one method, researcher, data source or theory to study the same phenomenon in order to increase credibility'),
           ('method triangulation', 'using different research methods (e.g. interviews and observations) to study the same question'),
           ('researcher triangulation', 'using several researchers to collect or analyse the same data to reduce individual researcher bias'),
           ('data triangulation', 'using data from different sources, times or groups of participants'),
           ('reflexivity', 'the researcher\'s critical reflection on how their own background, beliefs and role may have influenced the research'),
           ('personal reflexivity', 'reflection on how the researcher\'s own values, experiences and identity shaped the research'),
           ('epistemological reflexivity', 'reflection on how the research design and assumptions about knowledge shaped the findings'),
           ('member checking', 'returning findings to participants so they can confirm whether the researcher\'s interpretation is accurate')],
    facts=[('A study of bullying uses interviews with pupils, observations in the playground and teacher questionnaires. What is this?', 'Method triangulation', ['Reflexivity', 'Member checking', 'Counterbalancing'],
            'Different methods are used to study the same phenomenon.'),
           ('Which technique involves asking participants whether the researcher\'s interpretation of their interviews is accurate?', 'Member checking (credibility check)', ['Researcher triangulation', 'Inter-rater reliability', 'Pilot study'],
            'Participants validate the interpretation.'),
           ('A researcher writes a diary about how her experience as a former refugee may affect her interviews with refugees. This is an example of:', 'Personal reflexivity', ['Data triangulation', 'Snowball sampling', 'Debriefing'],
            'She is reflecting on how her identity may shape the research.')],
    why=[('Explain how triangulation increases the credibility of qualitative research.', 'If different methods, researchers or data sources lead to the same conclusion, it is less likely that findings reflect one method\'s weaknesses or one researcher\'s bias.'),
         ('Explain why reflexivity is important in qualitative research.', 'The researcher is the main instrument of data collection and interpretation, so their background and assumptions can shape what is asked and how answers are interpreted; reflexivity makes this influence visible and allows readers to judge credibility.')],
    contrast=[('researcher triangulation', 'method triangulation', 'Researcher triangulation uses several researchers to collect or interpret the same data; method triangulation uses different methods (e.g. interview and observation) to study the same question.'),
              ('personal reflexivity', 'epistemological reflexivity', 'Personal reflexivity concerns how the researcher\'s identity and values affected the study; epistemological reflexivity concerns how the design and assumptions about knowledge (e.g. choice of questions) shaped the findings.')],
    misc=[('Reflexivity means the researcher removes all personal bias from the study.', 'Reflexivity acknowledges that bias cannot be fully removed; it makes the researcher\'s influence explicit so it can be taken into account.'),
          ('Triangulation is only used in quantitative research.', 'Triangulation is especially important in qualitative research, where it is a key way to increase credibility.')],
    cases=[('a study of teachers\' burnout in Toronto', 'A research team interviews teachers about burnout, observes staff meetings and collects absence records; two researchers code the interviews independently and compare themes.', 'triangulation', 'it uses method (interviews, observation), data (records) and researcher triangulation (two coders), so consistent themes are more credible'),
           ('an interview study of migrant mothers by a researcher who is herself a migrant', 'A researcher who migrated from Syria to Germany interviews Syrian mothers about raising children in Berlin.', 'reflexivity', 'her shared background may build rapport and insight but may also lead her to assume understanding or project her own experience, so she should reflect on and report this')],
    apply=[('A student interviews three classmates about exam stress. Suggest two ways in which the credibility of the findings could be increased.', 'Member checking - ask the classmates to read the summary of themes; researcher triangulation - a second student codes the transcripts independently; reflexivity - note how being a classmate and friend may have influenced answers; method triangulation - add a brief questionnaire.', 4)],
    evaluate=[('Triangulation makes qualitative findings as trustworthy as experimental findings.', ['convergent evidence reduces method-specific bias', 'multiple researchers reduce individual bias'],
               ['triangulation does not establish causality', 'different methods may still share the same researcher\'s assumptions', 'it increases cost and time'],
               'Triangulation strengthens credibility but answers different questions from experiments; trustworthiness depends on the aims of the research.')],
))

# ---------------------------------------------------------------------------------------------
# ch04 Biological content: the brain and behaviour
# ---------------------------------------------------------------------------------------------
K.facts('ch04-st1', F(
    terms=[('localisation of function', 'the theory that specific areas of the brain are responsible for specific functions'),
           ('Broca\'s area', 'a region in the left inferior frontal lobe associated with speech production'),
           ('Wernicke\'s area', 'a region in the left posterior temporal lobe associated with language comprehension'),
           ('MRI', 'magnetic resonance imaging: a technique that uses magnetic fields and radio waves to produce detailed images of brain structure'),
           ('fMRI', 'functional MRI: a technique that measures changes in blood oxygenation (the BOLD signal) to show which brain areas are active during a task'),
           ('EEG', 'electroencephalography: recording of the brain\'s electrical activity through electrodes on the scalp, with excellent temporal but poor spatial resolution'),
           ('PET', 'positron emission tomography: imaging of brain activity by detecting a radioactive tracer, such as labelled glucose, taken up by active areas'),
           ('lateralisation', 'the specialisation of some functions in one hemisphere of the brain, such as language in the left hemisphere for most people')],
    facts=[('Which imaging technique has the best temporal resolution (millisecond accuracy)?', 'EEG', ['MRI', 'fMRI', 'PET'],
            'EEG records electrical activity in real time, but cannot locate deep structures precisely.'),
           ('Which imaging technique shows brain structure but not activity?', 'MRI', ['fMRI', 'PET', 'EEG'],
            'Structural MRI produces detailed images of anatomy; fMRI measures activity.'),
           ('What does fMRI actually measure?', 'Changes in blood oxygen levels (the BOLD signal)', ['Electrical activity of single neurons', 'Glucose metabolism using a radioactive tracer', 'Levels of neurotransmitters'],
            'Active neurons need more oxygenated blood; fMRI detects this haemodynamic response, a few seconds delayed.'),
           ('Damage to Broca\'s area typically causes which problem?', 'Difficulty producing fluent speech', ['Difficulty understanding speech', 'Loss of long-term memory', 'Blindness in one visual field'],
            'Broca\'s aphasia: slow, effortful speech with relatively preserved comprehension.')],
    why=[('Explain why brain imaging research cannot always show that a brain area causes a behaviour.', 'Imaging shows correlation between activity (or structure) and behaviour; the area may be active because of the task without being necessary for it, and the direction of causality is unclear - lesion or stimulation studies are needed for stronger causal claims.'),
         ('Explain why researchers often combine fMRI with EEG.', 'fMRI has good spatial resolution (where) but poor temporal resolution (seconds), while EEG has excellent temporal resolution (milliseconds) but poor spatial resolution; together they show both where and when activity occurs.'),
         ('Explain why strict localisation of function has been challenged.', 'Many functions depend on distributed networks of areas, and neuroplasticity allows other areas to take over functions after damage (e.g. language recovery after stroke), so functions are not fixed in single locations.')],
    contrast=[('MRI', 'fMRI', 'MRI produces static images of brain structure, while fMRI shows changes in brain activity over time by measuring blood-oxygen levels during tasks.'),
              ('Broca\'s area', 'Wernicke\'s area', 'Broca\'s area (left frontal lobe) is associated with speech production, while Wernicke\'s area (left temporal lobe) is associated with understanding language.')],
    misc=[('fMRI directly measures neurons firing.', 'fMRI measures blood-oxygen changes (the BOLD signal) that are an indirect, delayed indicator of neural activity.'),
          ('Each brain function is located in exactly one area.', 'Most functions involve networks of areas; localisation is a matter of degree, and plasticity allows reorganisation.')],
    cases=[('Phineas Gage', 'In 1848 a tamping iron passed through the frontal lobe of Phineas Gage, a railway foreman in Vermont; he survived but was reported to have become impulsive and irritable.', 'localisation of function', 'damage to the frontal lobe changed personality and self-control, suggesting that this region is involved in regulating behaviour - though accounts of his change were exaggerated over time'),
           ('a patient after a left-hemisphere stroke', 'Kenji, 62, from Hanoi, has a stroke in the left frontal lobe; he understands what people say but struggles to produce words.', 'localisation of language', 'his symptoms match Broca\'s aphasia, supporting the view that speech production is localised in the left inferior frontal lobe')],
    apply=[('A researcher wants to find out which brain areas are active when people make moral decisions. Recommend a brain imaging technique and explain one strength and one limitation.', 'fMRI: strength - good spatial resolution shows which areas (e.g. prefrontal cortex) are active, non-invasive; limitation - poor temporal resolution and an artificial lying-down setting, and activation shows correlation not causation.', 4)],
    evaluate=[('Brain imaging technology has shown that behaviour can be explained by localised brain functions.', ['fMRI and lesion studies identify specialised areas (Broca, fusiform face area)', 'split-brain studies show lateralisation (Sperry, 1968)'],
               ['activity is distributed across networks', 'imaging is correlational and interpretation is subjective', 'plasticity allows reorganisation'],
               'Imaging supports a degree of localisation, but behaviour is better explained by interacting networks than by single areas.')],
))
K.study('ch04-st1', 'Sperry', 1968, 'split-brain patients', 'to investigate the functions of the two hemispheres when the corpus callosum has been cut',
        'Patients whose corpus callosum had been severed to treat epilepsy were shown images briefly to one visual field and asked to name or select objects with one hand.',
        'objects shown to the right visual field (left hemisphere) could be named, while objects shown to the left visual field (right hemisphere) could not be named but could be selected with the left hand',
        'lateralisation of language in the left hemisphere',
        ['carefully controlled presentation to one visual field', 'clear evidence of hemispheric specialisation'],
        ['very small, unusual sample with long-term epilepsy (and medication)', 'brain organisation of patients may differ from typical brains'],
        mtype='quasi-experiment', wrong=['Patients could name objects shown to the left visual field but not the right', 'Cutting the corpus callosum produced no measurable effects', 'Both hemispheres could produce speech equally'])
K.study('ch04-st1', 'Broca', 1861, 'the brain of a patient who could only say "tan"', 'to identify the brain area associated with loss of speech',
        'Broca examined a patient, Leborgne, who could understand speech but could only say "tan"; after his death a post-mortem examination of the brain was carried out.',
        'Leborgne had a lesion in the left inferior frontal lobe; similar lesions were found in other patients with speech production problems',
        'localisation of speech production',
        ['early systematic evidence for localisation of function, later confirmed by imaging'],
        ['single case at first; post-mortem only', 'lesion was larger than "Broca\'s area" (Dronkers et al., 2007 MRI of preserved brains)'],
        mtype='case study')

K.facts('ch04-st2', F(
    terms=[('neuroplasticity', 'the brain\'s ability to change its structure and function in response to experience, learning or injury'),
           ('neural network', 'a group of interconnected neurons that work together to carry out a function'),
           ('synaptic pruning', 'the elimination of weak or unused synaptic connections, which makes neural networks more efficient'),
           ('dendritic branching', 'the growth of new dendrites, increasing the number of possible synaptic connections'),
           ('long-term potentiation', 'the long-lasting strengthening of a synapse after repeated stimulation, thought to underlie learning'),
           ('cortical remapping', 'the reorganisation of the cortex so that an area takes over a function previously served by another area, e.g. after injury'),
           ('functional recovery', 'the brain\'s ability to regain function after damage, through reorganisation of undamaged areas')],
    facts=[('Maguire et al. (2000) found which difference in London taxi drivers compared with controls?', 'Larger posterior hippocampi', ['Larger amygdalae', 'Smaller posterior hippocampi', 'Thicker visual cortex'],
            'Posterior hippocampal volume also correlated with years of experience.'),
           ('Draganski et al. (2004) found grey matter increased in which participants?', 'People who learned to juggle for three months', ['People who learned a second language', 'People deprived of sleep', 'People who meditated'],
            'Grey matter increased in mid-temporal and parietal areas and decreased again when juggling stopped.'),
           ('Which phrase best summarises Hebb\'s principle of learning?', 'Neurons that fire together wire together', ['Use it and you will lose it', 'Each function has one location', 'Neurons cannot regenerate'],
            'Repeated co-activation strengthens connections between neurons.')],
    why=[('Explain how neural networks are formed through learning.', 'Repeated practice causes neurons to fire together, strengthening synapses (long-term potentiation) and encouraging dendritic branching, so connections become more efficient - e.g. juggling practice increased grey matter (Draganski et al., 2004).'),
         ('Explain why synaptic pruning can be beneficial.', 'Removing unused connections allows resources to be directed to frequently used pathways, so networks become faster and more efficient; pruning is especially active in adolescence in the prefrontal cortex.')],
    contrast=[('dendritic branching', 'synaptic pruning', 'Dendritic branching creates new connections between neurons, while synaptic pruning removes unused connections; both are forms of neuroplasticity that shape neural networks.')],
    misc=[('Neuroplasticity only happens in childhood.', 'Adult brains also change: Draganski et al. (2004) found grey matter changes in adults after three months of juggling, and Maguire et al. (2000) in adult taxi drivers.'),
          ('Neuroplasticity always improves behaviour.', 'Plasticity can be maladaptive, e.g. phantom limb pain or the strengthening of networks involved in addiction.')],
    cases=[('stroke rehabilitation through constraint-induced movement therapy', 'After a stroke, Elena\'s left arm is weak; her therapist restrains her right arm for several hours a day so she must use the weak arm repeatedly.', 'neuroplasticity', 'forced, repeated use of the weak limb promotes cortical reorganisation so undamaged areas take over motor control'),
           ('learning to play the violin', 'Lukas starts violin at age 7 and practises daily; scans in adulthood show a larger cortical representation of his left-hand fingers.', 'neuroplasticity and experience', 'intensive use of the fingers strengthens and expands the relevant neural networks in the motor and somatosensory cortex')],
    apply=[('A 70-year-old in Lisbon starts learning Mandarin. Using neuroplasticity, explain why this might benefit her brain.', 'Learning new skills forms and strengthens neural networks through LTP and dendritic branching; adult brains remain plastic (Draganski et al., 2004), and cognitively demanding activity may build cognitive reserve.', 3)],
    evaluate=[('The brain is shaped more by experience than by genes.', ['plasticity research (Maguire et al., 2000; Draganski et al., 2004)', 'enriched environments change cortical thickness (Rosenzweig et al., 1972)'],
               ['basic brain structure is genetically programmed', 'genes influence plasticity itself', 'correlational evidence in humans'],
               'Genes set the basic architecture, but experience continually reshapes networks; both interact.')],
))
K.study('ch04-st2', 'Maguire et al.', 2000, 'the hippocampi of London taxi drivers', 'to investigate whether the brains of London taxi drivers differed from those of non-taxi drivers',
        'Structural MRI scans of 16 right-handed male London taxi drivers were compared with scans of 50 healthy right-handed males who did not drive taxis.',
        'taxi drivers had larger posterior hippocampi and smaller anterior hippocampi; posterior volume correlated positively with years of taxi-driving experience',
        'neuroplasticity in response to spatial learning',
        ['objective MRI measurement; analysts blind to participant group', 'correlation with experience suggests a dose-response relationship'],
        ['correlational/quasi-experimental - people with larger hippocampi might choose the job', 'small all-male sample'],
        mtype='quasi-experiment', wrong=['Taxi drivers had smaller posterior hippocampi', 'Hippocampal volume decreased with years of experience', 'There were no differences between drivers and controls'])
K.study('ch04-st2', 'Draganski et al.', 2004, 'juggling and grey matter', 'to investigate whether learning a new motor skill changes brain structure in adults',
        '24 volunteers with no juggling experience were scanned and randomly divided into jugglers (who learned a three-ball cascade over three months) and non-jugglers; scans were repeated after three months of practice and after three months without practice.',
        'jugglers showed increased grey matter in the mid-temporal area (hMT/V5) and left posterior intraparietal sulcus; this decreased again after they stopped juggling',
        'experience-dependent neuroplasticity in the adult brain',
        ['longitudinal experimental design with a control group', 'objective MRI measurement'],
        ['small sample', 'mechanism of grey-matter change unclear', 'cannot show that the structural change caused better juggling'],
        mtype='laboratory experiment', iv='learning to juggle vs not learning', dv='grey matter density in MRI scans')
K.study('ch04-st2', 'Rosenzweig, Bennett and Diamond', 1972, 'enriched environments and the rat brain', 'to investigate whether environmental stimulation affects brain development in rats',
        'Rats were raised for 30-60 days either in an enriched cage with toys and other rats or in an impoverished cage alone; their brains were then dissected.',
        'rats in the enriched environment had a thicker, heavier cortex, especially the occipital cortex',
        'how environmental stimulation changes brain structure',
        ['strict control of the environment; causal conclusion possible'],
        ['animal study - generalising to humans is limited', 'rats were killed for dissection - ethical cost'],
        mtype='laboratory experiment', ethics='Rats were kept in impoverished conditions and killed for dissection; justified under a cost-benefit analysis and the 3Rs, but the harm is significant.')

K.facts('ch04-st3', F(
    terms=[('neurotransmitter', 'a chemical messenger released by a neuron into the synaptic gap that binds to receptors on another neuron'),
           ('synaptic transmission', 'the process by which a nerve impulse is passed across the synaptic gap from one neuron to another by neurotransmitters'),
           ('agonist', 'a chemical that increases the action of a neurotransmitter, e.g. by mimicking it or blocking its reuptake'),
           ('antagonist', 'a chemical that reduces the action of a neurotransmitter, e.g. by blocking its receptors'),
           ('reuptake', 'the reabsorption of a neurotransmitter by the presynaptic neuron after it has been released'),
           ('excitatory neurotransmitter', 'a neurotransmitter that makes the postsynaptic neuron more likely to fire, such as glutamate'),
           ('inhibitory neurotransmitter', 'a neurotransmitter that makes the postsynaptic neuron less likely to fire, such as GABA'),
           ('acetylcholine', 'a neurotransmitter involved in memory, attention and muscle movement')],
    facts=[('Selective serotonin reuptake inhibitors (SSRIs) are an example of which type of drug?', 'Agonist', ['Antagonist', 'Hormone', 'Inhibitory neurotransmitter'],
            'Blocking reuptake leaves more serotonin in the synapse, increasing its action.'),
           ('Scopolamine blocks acetylcholine receptors. It is therefore:', 'An acetylcholine antagonist', ['An acetylcholine agonist', 'A serotonin reuptake inhibitor', 'A hormone'],
            'It reduces the effect of acetylcholine by blocking receptors.'),
           ('Which neurotransmitter is most associated with the brain\'s reward system?', 'Dopamine', ['GABA', 'Acetylcholine', 'Glutamate'],
            'Dopamine release in the nucleus accumbens is linked to reward and motivation.')],
    why=[('Explain the process of synaptic transmission.', 'An action potential reaches the axon terminal, vesicles release neurotransmitter into the synaptic gap, it binds to receptors on the postsynaptic membrane causing excitation or inhibition, and it is then removed by reuptake or enzymes.'),
         ('Explain how an agonist can affect behaviour.', 'By increasing a neurotransmitter\'s effect (mimicking it, increasing release or blocking reuptake), an agonist changes the activity of the brain systems that use it - e.g. citalopram (an SSRI) increased harm aversion in moral judgements (Crockett et al., 2010).')],
    contrast=[('an agonist', 'an antagonist', 'An agonist increases the effect of a neurotransmitter (e.g. SSRIs for serotonin), while an antagonist reduces it, typically by blocking receptors (e.g. scopolamine for acetylcholine).'),
              ('excitatory neurotransmitters', 'inhibitory neurotransmitters', 'Excitatory neurotransmitters (e.g. glutamate) make the receiving neuron more likely to fire, while inhibitory ones (e.g. GABA) make it less likely.')],
    misc=[('Each neurotransmitter controls a single behaviour.', 'Neurotransmitters act in many systems; serotonin, for example, is involved in mood, sleep, appetite and social behaviour.'),
          ('An antagonist increases the release of a neurotransmitter.', 'An antagonist reduces a neurotransmitter\'s effect, usually by blocking its receptors.')],
    cases=[('nicotine addiction', 'Omar, 19, in Dubai, finds he craves a cigarette whenever he is stressed; nicotine stimulates acetylcholine receptors and increases dopamine release in the reward pathway.', 'neurotransmitters and behaviour', 'nicotine acts as an agonist that increases dopamine in the nucleus accumbens, reinforcing smoking and producing craving')],
    apply=[('A new drug blocks the reuptake of dopamine. Predict its effect on synaptic transmission and suggest one possible effect on behaviour.', 'More dopamine remains in the synapse and binds repeatedly to receptors (agonist effect); behaviour may show increased motivation, alertness or reward-seeking, with risk of dependence (like cocaine, which blocks dopamine reuptake).', 3)],
    evaluate=[('Behaviour can be explained by the action of neurotransmitters.', ['drug studies show causal effects (Antonova et al., 2011; Crockett et al., 2010)', 'agonist/antagonist treatments change symptoms'],
               ['reductionist - ignores cognition and context', 'neurotransmitters interact in complex systems', 'lab tasks have limited ecological validity'],
               'Neurotransmitters clearly influence behaviour, but they are one level of a multi-level explanation.')],
))
K.study('ch04-st3', 'Antonova et al.', 2011, 'scopolamine and the hippocampus', 'to investigate the role of acetylcholine in the encoding of spatial memories',
        'In a double-blind, repeated measures study, 20 healthy young men were injected with scopolamine (an acetylcholine antagonist) or a placebo and completed a virtual "arena" spatial memory task during fMRI, with sessions 3-4 weeks apart.',
        'scopolamine reduced hippocampal activation during the encoding of spatial memories compared with placebo',
        'the role of acetylcholine in memory formation',
        ['double-blind, placebo-controlled; repeated measures controls participant variables', 'fMRI provides an objective measure'],
        ['small all-male sample', 'artificial virtual task', 'scopolamine affects other systems too'],
        mtype='laboratory experiment', iv='scopolamine vs placebo', dv='hippocampal activation (fMRI) during the encoding phase of a spatial memory task',
        ethics='Participants received an active drug with side effects; full informed consent, medical screening and the right to withdraw were essential.',
        wrong=['Scopolamine increased hippocampal activation', 'Scopolamine had no effect on brain activity', 'Placebo reduced hippocampal activation'])
K.study('ch04-st3', 'Crockett et al.', 2010, 'serotonin and moral judgement', 'to investigate whether increasing serotonin affects moral judgement and behaviour',
        'In a double-blind, placebo-controlled study, healthy volunteers received citalopram (an SSRI), atomoxetine or a placebo, then made judgements about moral dilemmas and played the ultimatum game.',
        'citalopram made participants less likely to judge harming one person to save others as acceptable, and less likely to reject unfair offers in the ultimatum game - it increased harm aversion',
        'how a neurotransmitter influences social behaviour',
        ['double-blind, placebo-controlled design', 'used both judgements and behaviour'],
        ['hypothetical dilemmas lack ecological validity', 'single dose; effects may differ with long-term use', 'Western student sample'],
        mtype='laboratory experiment', iv='drug condition (citalopram vs placebo)', dv='judgements of moral acceptability and rejection rates of unfair offers')

K.facts('ch04-st4', F(
    terms=[('the 3Rs', 'the principles of replacement, reduction and refinement that guide the ethical use of animals in research'),
           ('replacement', 'using alternatives to animals, such as computer models or cell cultures, where possible'),
           ('reduction', 'using the smallest number of animals needed for valid results'),
           ('refinement', 'modifying procedures to minimise pain and distress and improve animal welfare'),
           ('animal model', 'the use of a non-human species to study processes that are thought to be similar in humans'),
           ('speciesism', 'the view (Singer, 1975) that giving less moral consideration to other species is a prejudice similar to racism')],
    facts=[('The 3Rs for ethical animal research were first proposed by:', 'Russell and Burch (1959)', ['Milgram (1963)', 'the British Psychological Society in 2020', 'Harlow (1958)'],
            'Russell and Burch, The Principles of Humane Experimental Technique (1959).'),
           ('Olds and Milner (1954) found rats would press a lever repeatedly to:', 'Receive electrical stimulation in the septal area of the brain', ['Avoid an electric shock', 'Receive food pellets', 'Escape from a maze'],
            'This revealed a brain "reward" system.'),
           ('Which reason is most often given for using animals in biological psychology?', 'Procedures such as lesioning or drug trials would be unethical in humans', ['Animals behave exactly like humans', 'Animals are cheaper than computer models', 'Animals cannot be harmed'],
            'Animals allow invasive procedures and strict control of genes and environment.')],
    why=[('Explain why animal research is used in biological psychology.', 'It allows invasive procedures (lesions, drugs, gene manipulation) and full control of environment and genetics that would be unethical or impossible in humans, and short life spans allow developmental and generational studies.'),
         ('Explain why generalising from animal research to humans is problematic.', 'Brains and behaviour differ between species (e.g. a larger prefrontal cortex, language and culture in humans), so mechanisms found in rats may not operate in the same way in people.')],
    contrast=[('replacement', 'refinement', 'Replacement means using alternatives to animals altogether (e.g. computer modelling), while refinement means improving procedures so animals that are used suffer as little as possible.')],
    misc=[('Animal research is banned in psychology.', 'Animal research is permitted under strict regulation (e.g. licences, ethics committees and the 3Rs), although some procedures are restricted.'),
          ('Findings from rats can be directly applied to humans because both are mammals.', 'Shared mammalian biology makes rats useful models, but differences in brain complexity, cognition and culture limit direct generalisation.')],
    cases=[('Harlow\'s rhesus monkeys', 'Infant rhesus monkeys raised in isolation with wire and cloth surrogate mothers clung to the cloth mother even when only the wire mother provided milk, and later showed severe social problems.', 'the value and ethics of animal research', 'the research showed the importance of comfort in attachment but caused lasting harm, leading to debates about whether the benefits justified the suffering')],
    apply=[('A researcher wants to study the effect of a new drug on memory in rats. Explain how she could apply the 3Rs.', 'Replacement - test first on cell cultures or computer models; reduction - use power analysis to determine the minimum number of rats; refinement - use anaesthesia, enriched housing and humane endpoints to minimise suffering.', 3)],
    evaluate=[('The benefits of animal research in psychology outweigh the costs.', ['led to understanding of reward, memory and neurotransmitters', 'drug development depends on animal testing', 'strict regulation and 3Rs'],
               ['animal suffering is real (Harlow)', 'generalisability to humans is limited', 'alternatives are increasingly available'],
               'Some animal research has produced major benefits, but each study should be justified by a cost-benefit analysis and the 3Rs.')],
))
K.study('ch04-st4', 'Olds and Milner', 1954, 'electrical stimulation of the rat brain', 'to investigate whether stimulation of particular brain areas could act as a reward',
        'Electrodes were implanted in different brain areas of rats, which could press a lever to deliver a small electrical stimulation to their own brain.',
        'rats with electrodes in the septal area pressed the lever at high rates - up to thousands of times per hour - suggesting the brain has a reward system',
        'the discovery of a brain reward system',
        ['strict control of stimulation; clear behavioural measure', 'foundational for understanding dopamine and addiction'],
        ['invasive surgery on animals', 'generalising "pleasure" to humans is uncertain'],
        mtype='laboratory experiment', ethics='Invasive brain surgery was carried out on animals; the harm must be weighed against the value of discovering the reward system.')
K.study('ch04-st4', 'Martinez and Kesner', 1991, 'acetylcholine and memory in rats', 'to investigate the role of acetylcholine in the formation of spatial memory',
        'Rats were trained to run a maze, then injected with scopolamine (blocks acetylcholine receptors), physostigmine (blocks the enzyme acetylcholinesterase, increasing acetylcholine) or nothing, and re-tested.',
        'scopolamine rats were slower and made more errors; physostigmine rats were faster and made fewer errors than controls',
        'the role of acetylcholine in memory',
        ['clear causal design with a control group', 'consistent with human studies (Antonova et al., 2011)'],
        ['animal model - rat spatial memory may differ from human memory', 'drugs affect other systems'],
        mtype='laboratory experiment', iv='drug condition (scopolamine, physostigmine, control)', dv='time and number of errors to complete the maze',
        wrong=['Scopolamine improved maze performance', 'Physostigmine made rats slower', 'Neither drug affected maze performance'])

# ---------------------------------------------------------------------------------------------
# ch05 Biological content: hormones, pheromones and genetics
# ---------------------------------------------------------------------------------------------
K.facts('ch05-st1', F(
    terms=[('hormone', 'a chemical messenger secreted by an endocrine gland into the bloodstream that affects target organs'),
           ('cortisol', 'a stress hormone released by the adrenal cortex as part of the HPA axis response'),
           ('oxytocin', 'a hormone produced in the hypothalamus and released by the pituitary gland, linked to bonding, trust and childbirth'),
           ('testosterone', 'a steroid hormone produced mainly in the testes (and in smaller amounts in the ovaries and adrenal glands), linked to dominance and aggression'),
           ('HPA axis', 'the hypothalamic-pituitary-adrenal axis, the system that releases cortisol in response to stress'),
           ('endocrine system', 'the system of glands that secrete hormones into the bloodstream')],
    facts=[('Kosfeld et al. (2005) found that intranasal oxytocin increased:', 'Trust in an investment game', ['Aggression towards strangers', 'Memory for faces', 'Risk-taking in gambling with a computer'],
            '45% of the oxytocin group gave the maximum amount to a trustee vs 21% in the placebo group.'),
           ('Newcomer et al. (1999) found that high doses of cortisol impaired:', 'Verbal declarative memory', ['Procedural memory', 'Visual perception', 'Reaction time'],
            'Participants given high cortisol recalled less of a prose passage.'),
           ('Which gland releases cortisol?', 'The adrenal cortex', ['The pituitary gland', 'The pineal gland', 'The thyroid gland'],
            'ACTH from the pituitary stimulates the adrenal cortex to release cortisol.')],
    why=[('Explain how hormones differ from neurotransmitters in the way they affect behaviour.', 'Hormones travel in the bloodstream to target organs and act more slowly and for longer, while neurotransmitters act across synapses within milliseconds and locally.'),
         ('Explain how prolonged stress can affect memory.', 'Chronic stress keeps cortisol levels high, which can damage or reduce activity in the hippocampus (rich in cortisol receptors), impairing declarative memory - as Newcomer et al. (1999) showed with high doses.')],
    contrast=[('oxytocin', 'testosterone', 'Oxytocin is associated with bonding, trust and in-group cooperation, while testosterone is associated with dominance, status-seeking and, in some studies, aggression.')],
    misc=[('Testosterone directly causes violence in men.', 'The relationship is correlational and complex: testosterone is linked to dominance-seeking, which is expressed through aggression only in some contexts; social factors moderate the link.'),
          ('Oxytocin makes people trust everyone.', 'Oxytocin effects depend on context; De Dreu et al. (2010) found it increased trust and cooperation towards the in-group but could increase defensive aggression towards out-groups.')],
    cases=[('exam stress in medical students', 'During final exams, medical students in Melbourne report poor sleep and frequent colds; saliva samples show raised cortisol.', 'the role of cortisol in stress', 'activation of the HPA axis raises cortisol, which suppresses the immune system and can impair memory, explaining both illness and poorer recall under stress')],
    apply=[('A company in Seoul plans to use oxytocin nasal spray to improve teamwork. Using research, explain one reason for caution.', 'Kosfeld et al. (2005) found increased trust, but replications have been inconsistent, effects depend on context (in-group bias, De Dreu et al., 2010), and there are ethical issues of consent and manipulation.', 3)],
    evaluate=[('Hormones have a strong influence on human social behaviour.', ['oxytocin and trust (Kosfeld et al., 2005)', 'testosterone and dominance (Dabbs et al., 1995)', 'cortisol and memory (Newcomer et al., 1999)'],
               ['many findings are correlational', 'replication failures (oxytocin)', 'social and cognitive factors moderate hormone effects'],
               'Hormones influence social behaviour, but their effects are context-dependent and interact with cognitive and cultural factors.')],
))
K.study('ch05-st1', 'Newcomer et al.', 1999, 'cortisol and verbal memory', 'to investigate whether elevated cortisol levels interfere with verbal declarative memory',
        'Healthy volunteers were randomly assigned to receive a high dose of cortisol (160 mg/day), a low dose (40 mg/day) or a placebo for four days and tested on recall of a prose passage; the study was double-blind.',
        'the high-dose group showed impaired verbal declarative memory; memory returned to normal after the cortisol stopped',
        'the effect of the stress hormone cortisol on memory',
        ['randomised, double-blind, placebo-controlled', 'dose-response pattern'],
        ['artificial administration of cortisol does not equal natural stress', 'small sample'],
        mtype='laboratory experiment', iv='cortisol dose (high, low, placebo)', dv='recall of a prose paragraph',
        ethics='Participants received a drug that temporarily impaired memory; informed consent, monitoring and the reversibility of the effect were essential.',
        wrong=['The high-dose group showed improved verbal memory', 'Memory impairment remained permanent after treatment ended', 'The placebo group had the poorest memory'])
K.study('ch05-st1', 'Kosfeld et al.', 2005, 'oxytocin and trust', 'to investigate whether oxytocin increases trust between humans',
        '58 healthy male students received intranasal oxytocin or a placebo (double-blind) and played an investment game as investors deciding how much money to transfer to a trustee.',
        '45% of the oxytocin group transferred the maximum amount vs 21% of the placebo group; oxytocin did not affect risk-taking when playing against a computer',
        'the role of oxytocin in trust',
        ['double-blind and placebo-controlled', 'control condition with a computer separated trust from risk-taking'],
        ['all-male student sample', 'later replications failed to find the effect (Nave et al., 2015)'],
        mtype='laboratory experiment', iv='oxytocin vs placebo nasal spray', dv='amount of money transferred to the trustee',
        wrong=['Oxytocin reduced trust in the investment game', 'Oxytocin increased risk-taking against a computer', 'There was no difference between groups'])
K.study('ch05-st1', 'Dabbs et al.', 1995, 'testosterone and violent crime', 'to investigate the relationship between testosterone and criminal violence in prison inmates',
        'Saliva testosterone was measured in 692 adult male prison inmates and compared with the nature of their crimes and their behaviour in prison.',
        'inmates with higher testosterone were more likely to have committed violent crimes and to have violated prison rules more often',
        'the relationship between testosterone and aggression',
        ['large sample; objective hormone measurement'],
        ['correlational - violence and confrontation may raise testosterone', 'prison sample - limited generalisability', 'single saliva sample'],
        mtype='correlational study')

K.facts('ch05-st2', F(
    terms=[('pheromone', 'a chemical signal released by an organism that triggers a specific response in another member of the same species'),
           ('vomeronasal organ', 'a structure in the nasal cavity of many mammals that detects pheromones; in humans it is thought to be vestigial'),
           ('androstadienone', 'a steroid found in male sweat and proposed as a human sex pheromone'),
           ('estratetraenol', 'a steroid found in female urine proposed as a human sex pheromone'),
           ('major histocompatibility complex (MHC)', 'a group of genes involved in the immune system that may influence body odour and mate preference')],
    facts=[('Wedekind et al. (1995) found that women preferred the odour of T-shirts worn by men who:', 'Had MHC genes dissimilar to their own', ['Had MHC genes similar to their own', 'Were more physically attractive', 'Had higher testosterone'],
            'The preference was reversed in women taking oral contraceptives.'),
           ('Hare et al. (2017) found that androstadienone and estratetraenol:', 'Had no effect on ratings of attractiveness of opposite-sex faces', ['Strongly increased attractiveness ratings', 'Decreased attractiveness ratings', 'Only affected women taking contraceptives'],
            'The study found no evidence that these putative pheromones act as human sex pheromones.'),
           ('McClintock (1971) claimed that women living together showed:', 'Synchronised menstrual cycles', ['Increased stress hormones', 'Better memory', 'Lower body temperature'],
            'Later studies (e.g. Yang and Schank, 2006) failed to replicate menstrual synchrony.')],
    why=[('Explain why it is difficult to demonstrate that human pheromones exist.', 'No human pheromone has been chemically identified with certainty; humans rely heavily on vision and culture, the vomeronasal organ may be non-functional, and studies use putative compounds at unnatural concentrations with small samples and expectancy effects.'),
         ('Explain why the MHC T-shirt studies are considered evidence for an evolutionary function of odour.', 'Choosing a mate with dissimilar MHC genes would give offspring a more diverse immune system, so an odour-based preference would be adaptive and selected for.')],
    contrast=[('a pheromone', 'a hormone', 'A hormone is released into the bloodstream and acts within the same body, while a pheromone is released outside the body and affects the behaviour or physiology of another member of the species.')],
    misc=[('Perfumes containing "human pheromones" have been proven to increase attraction.', 'There is no reliable evidence for this; studies such as Hare et al. (2017) found putative pheromones had no effect on attractiveness ratings.'),
          ('Menstrual synchrony is a well-established effect of human pheromones.', 'McClintock\'s (1971) finding has not been reliably replicated (e.g. Yang and Schank, 2006), and apparent synchrony can arise by chance.')],
    cases=[('a fragrance company\'s advertising claim', 'A fragrance company in Paris advertises a cologne "with pheromones that make women find you irresistible".', 'the pheromone debate', 'the claim is not supported: candidate compounds like androstadienone have not been shown to change attraction in well-controlled studies such as Hare et al. (2017)')],
    apply=[('Design a double-blind study to test whether androstadienone affects mood. Outline two features that would improve its validity.', 'Double-blind administration of androstadienone vs a masked control (clove oil) so expectations cannot affect results; counterbalanced repeated measures; a standardised mood scale; a large sample with pre-registration.', 4)],
    evaluate=[('Pheromones play an important role in human behaviour.', ['MHC odour preference (Wedekind et al., 1995)', 'evolutionary plausibility from animal research'],
               ['no human pheromone identified', 'failed replications (Hare et al., 2017; menstrual synchrony)', 'small samples, expectancy effects, unnatural concentrations'],
               'Evidence is weak; odour may influence some preferences, but there is no convincing evidence that pheromones play an important role in human behaviour.')],
))
K.study('ch05-st2', 'Wedekind et al.', 1995, 'MHC and body-odour preference', 'to investigate whether women prefer the odour of men whose MHC genes differ from their own',
        '44 men wore the same cotton T-shirt for two nights while avoiding smells such as perfume; 49 women rated the odours of six T-shirts for pleasantness and sexiness; all were MHC-typed.',
        'women rated the odour of men with dissimilar MHC as more pleasant; the preference reversed for women taking oral contraceptives',
        'a possible role of body odour in mate choice',
        ['double-blind; objective genetic typing', 'evolutionary explanation is plausible'],
        ['small sample of students in Switzerland', 'odour is not proved to be a pheromone', 'ratings of T-shirts lack ecological validity'],
        mtype='laboratory experiment')
K.study('ch05-st2', 'Hare et al.', 2017, 'putative human sex pheromones', 'to test whether androstadienone and estratetraenol act as human sex pheromones',
        '94 heterosexual Caucasian participants rated the attractiveness of opposite-sex faces and judged the gender of neutral faces after exposure to androstadienone, estratetraenol or a control solution, in a double-blind repeated measures design.',
        'the compounds had no effect on attractiveness ratings or on gender judgements of neutral faces',
        'the lack of evidence for human sex pheromones',
        ['double-blind and repeated measures', 'larger sample than earlier studies'],
        ['only Caucasian participants', 'artificial tasks; one concentration'],
        mtype='laboratory experiment', iv='odour condition (androstadienone, estratetraenol, control)', dv='attractiveness ratings of opposite-sex faces')

K.facts('ch05-st3', F(
    terms=[('heritability', 'the proportion of variation in a trait within a population that can be attributed to genetic differences'),
           ('concordance rate', 'the probability that if one twin has a trait, the other twin will also have it'),
           ('monozygotic (MZ) twins', 'identical twins who develop from one fertilised egg and share almost 100% of their genes'),
           ('dizygotic (DZ) twins', 'non-identical twins who develop from two fertilised eggs and share about 50% of their genes on average'),
           ('adoption study', 'a study comparing adopted children with their biological and adoptive parents to separate genetic from environmental influences'),
           ('family study', 'a study that examines whether a trait is more common in close relatives of an affected person than in the general population'),
           ('genotype', 'the genetic make-up of an individual'),
           ('phenotype', 'the observable characteristics of an individual that result from the interaction of genotype and environment')],
    facts=[('Kendler et al. (2006) estimated the heritability of major depression in a Swedish twin sample to be about:', '38%', ['8%', '70%', '95%'],
            'Heritability was higher in women (about 42%) than men (about 29%).'),
           ('If MZ twins have a higher concordance rate than DZ twins, this suggests:', 'Genetic factors influence the trait', ['The trait is caused only by the environment', 'The trait is not inherited at all', 'Twins share no environment'],
            'MZ twins share more genes, so greater similarity implies a genetic contribution.'),
           ('Bouchard et al. (1990) found the IQ correlation for MZ twins reared apart was about:', '0.70', ['0.20', '0.40', '0.99'],
            'This was interpreted as about 70% of the variance in IQ in this sample being associated with genetic variation.')],
    why=[('Explain why twin studies are used to study the role of genes in behaviour.', 'MZ twins share almost all their genes and DZ twins about half, but both share similar environments; comparing concordance rates estimates the genetic contribution to a trait.'),
         ('Explain why adoption studies help separate genetic and environmental influences.', 'Adopted children share genes with biological parents but environment with adoptive parents, so similarity to biological parents suggests genetic influence and similarity to adoptive parents suggests environmental influence.'),
         ('Explain why a heritability estimate does not apply to an individual.', 'Heritability is a population statistic describing the proportion of variation between people due to genetic differences; it says nothing about how much of one person\'s trait is due to genes, and it changes with the environment of the population.')],
    contrast=[('MZ twins', 'DZ twins', 'MZ twins come from one egg and share nearly 100% of their genes, while DZ twins come from two eggs and share about 50%; comparing them estimates genetic influence.'),
              ('a twin study', 'an adoption study', 'Twin studies compare MZ and DZ concordance assuming similar environments; adoption studies compare adopted individuals with biological and adoptive relatives to separate genes and environment more directly.')],
    misc=[('A heritability of 40% means that 40% of a person\'s depression is caused by their genes.', 'Heritability refers to the proportion of variation in a population, not to any individual; it also depends on the environment in which the population lives.'),
          ('If MZ twins have a concordance rate below 100%, genes play no role.', 'A concordance rate below 100% shows that environment also matters, but a higher rate for MZ than DZ twins still indicates a genetic contribution.')],
    cases=[('MZ twins raised in different countries', 'Twins Ana and Isabel were separated at birth; one was raised in Spain and the other in Mexico. As adults both develop major depression.', 'genetic influences on behaviour', 'shared genes despite different environments suggest a genetic vulnerability, though a single case cannot establish this and both may have experienced stressors')],
    apply=[('In a twin study, the concordance rate for a disorder is 46% for MZ twins and 14% for DZ twins. Explain what these figures suggest.', 'MZ concordance is over three times DZ concordance, so genes contribute to the disorder; but MZ concordance is far below 100%, so environmental factors are also important; MZ twins may also share more similar environments (equal environments assumption).', 3)],
    evaluate=[('Twin studies provide strong evidence for the role of genes in behaviour.', ['large samples (Kendler et al., 2006)', 'consistent MZ > DZ concordance for many traits', 'twins reared apart (Bouchard et al., 1990)'],
               ['equal environments assumption may be false', 'reared-apart twins often had similar environments and contact', 'heritability is population-specific'],
               'Twin studies give useful evidence of genetic influence, but they cannot separate genes and environment perfectly; they are best combined with adoption and molecular studies.')],
))
K.study('ch05-st3', 'Bouchard et al.', 1990, 'twins reared apart', 'to estimate the genetic contribution to intelligence and personality using twins raised in different homes',
        'The Minnesota Study of Twins Reared Apart tested over 100 sets of twins or triplets separated early in life on IQ, personality and other measures during a week of assessments.',
        'MZ twins reared apart had an IQ correlation of about 0.70, similar to MZ twins reared together, suggesting about 70% of IQ variance was associated with genetic variation',
        'the contribution of genes to intelligence',
        ['rare sample that separates genes from shared family environment', 'extensive, standardised testing'],
        ['many twins were separated late or had contact, and were placed in similar homes', 'volunteer sample attracted by publicity', 'heritability estimates apply only to this population'],
        mtype='twin study', wrong=['MZ twins reared apart showed almost no similarity in IQ', 'DZ twins reared apart were more similar than MZ twins', 'IQ correlations were about 0.20'])
K.study('ch05-st3', 'Kendler et al.', 2006, 'heritability of major depression in Swedish twins', 'to estimate the heritability of major depression and whether it differs between men and women',
        'Over 42,000 twins from the Swedish Twin Registry were interviewed by telephone for lifetime major depression; MZ and DZ concordance rates were compared.',
        'heritability of major depression was about 38%, higher in women (about 42%) than men (about 29%)',
        'the genetic contribution to depression',
        ['very large, population-based sample', 'included opposite-sex twin pairs'],
        ['self-report telephone interviews may be inaccurate', 'one culture; heritability depends on environment', 'equal environments assumption'],
        mtype='twin study', wrong=['Heritability of depression was about 90%', 'Heritability was higher in men than in women', 'There was no genetic contribution to depression'])

K.facts('ch05-st4', F(
    terms=[('evolutionary psychology', 'the approach that explains behaviour as the product of natural selection acting on traits that helped ancestors survive and reproduce'),
           ('natural selection', 'the process by which heritable traits that increase survival and reproduction become more common over generations'),
           ('sexual selection', 'selection for traits that increase success in attracting or competing for mates'),
           ('environment of evolutionary adaptedness (EEA)', 'the ancestral environment in which a trait is thought to have evolved'),
           ('compensatory prophylaxis hypothesis', 'the hypothesis that disgust increases in the first trimester of pregnancy to protect the mother and foetus while the immune system is suppressed')],
    facts=[('Buss (1989) studied mate preferences in how many cultures?', '37', ['5', '12', '100'],
            'Buss surveyed over 10,000 people in 37 cultures.'),
           ('Fessler, Eng and Navarrete (2005) found that disgust sensitivity was highest in which stage of pregnancy?', 'The first trimester', ['The second trimester', 'The third trimester', 'After birth'],
            'Disgust, particularly food-related, was elevated when the immune system is suppressed.'),
           ('Which criticism is most often made of evolutionary explanations?', 'They are hard to test and can be "just-so stories"', ['They rely only on laboratory experiments', 'They ignore genetics', 'They have been tested in every culture'],
            'Ancestral environments cannot be observed directly, so explanations are often post hoc.')],
    why=[('Explain how an evolutionary explanation accounts for disgust.', 'Disgust motivates avoidance of pathogens (rotten food, bodily fluids); ancestors who felt disgust were less likely to become ill and more likely to survive and reproduce, so the response was selected for.'),
         ('Explain why evolutionary explanations are difficult to test.', 'We cannot observe the EEA or run experiments on evolution; evidence is indirect (cross-cultural universals, correlations) and alternative cultural explanations are often possible.')],
    contrast=[('evolutionary explanations', 'cultural explanations of mate preference', 'Evolutionary explanations attribute sex differences in mate preferences to selection pressures in ancestral environments, while cultural explanations attribute them to social roles and economic inequality (Eagly and Wood, 1999).')],
    misc=[('If a behaviour is universal, it must have an evolutionary cause.', 'Universality is consistent with evolution but could also result from shared cultural or ecological conditions; it is not proof of an adaptation.')],
    cases=[('food aversions in early pregnancy', 'Sana, in her first trimester, suddenly finds meat and fish disgusting, although she enjoyed them before.', 'an evolutionary explanation of behaviour', 'heightened disgust when the immune system is suppressed reduces the risk of food-borne infection, consistent with Fessler et al. (2005)')],
    apply=[('Using an evolutionary explanation, suggest why people may find spiders more frightening than cars, even though cars kill far more people.', 'Fear of ancestral threats (snakes, spiders) was selected for over millions of years (prepared learning, Seligman, 1971), whereas cars are too recent for evolved fear responses to have developed.', 3)],
    evaluate=[('Evolutionary explanations of behaviour are not scientific.', ['hard to falsify; post hoc', 'ignore cultural variation and social roles'],
               ['generate testable predictions (Fessler et al., 2005)', 'cross-cultural data (Buss, 1989) support predicted patterns'],
               'Evolutionary explanations can be scientific when they make specific, testable predictions, but many are speculative and need cultural evidence.')],
))
K.study('ch05-st4', 'Buss', 1989, 'mate preferences across 37 cultures', 'to test evolutionary predictions about sex differences in mate preferences across cultures',
        'Over 10,000 people in 37 cultures on six continents completed questionnaires rating and ranking characteristics in a potential mate.',
        'men valued physical attractiveness and youth more, and women valued financial prospects and ambition more, in most cultures',
        'evolutionary explanations of mate preference',
        ['very large cross-cultural sample', 'consistent pattern supports evolutionary predictions'],
        ['self-report of preferences, not actual choices', 'mostly urban, educated samples', 'differences can also be explained by economic inequality (Eagly and Wood, 1999)'],
        mtype='cross-cultural survey', wrong=['Women valued physical attractiveness more than men in all cultures', 'There were no sex differences in mate preferences', 'Men valued financial prospects more than women'])
K.study('ch05-st4', 'Fessler, Eng and Navarrete', 2005, 'disgust in pregnancy', 'to test whether disgust sensitivity increases in the first trimester of pregnancy',
        '496 pregnant women completed an online questionnaire about disgust sensitivity in different domains and reported their stage of pregnancy and nausea.',
        'disgust sensitivity, particularly for food, was higher in the first trimester than later in pregnancy',
        'an evolutionary explanation of disgust',
        ['tested a specific, falsifiable prediction', 'large sample'],
        ['correlational and cross-sectional', 'self-selected online sample', 'self-report measures'],
        mtype='correlational study')


@K.add('ch05-st3', 'C3', (2, 5), 'numerical')
def falconer(rng, slot):
    trait = rng.choice(['IQ scores', 'extraversion scores', 'anxiety scores', 'reading ability', 'height-adjusted body mass index',
                        'scores on a depression inventory', 'sensation-seeking scores'])
    rmz = rng.choice([0.52, 0.58, 0.64, 0.70, 0.76, 0.81, 0.86])
    rdz = round(rmz - rng.choice([0.12, 0.18, 0.22, 0.26, 0.30]), 2)
    if rdz <= 0.1:
        return None
    h2 = 2 * (rmz - rdz)
    if h2 > 1:
        return None
    c2 = rmz - h2
    e2 = 1 - rmz
    if c2 < -1e-9:   # requires rDZ >= rMZ / 2
        return None
    c2 = max(c2, 0.0)
    who = name(rng)
    stem = (f'{who} reads a twin study from {rng.choice(CITIES)} in which the correlation for {trait} was {rmz:.2f} for MZ twins and '
            f'{rdz:.2f} for DZ twins. Using Falconer\'s formula, h² = 2(rMZ - rDZ), estimate the heritability'
            + (' and the proportion of variance due to shared environment (c² = rMZ - h²) and non-shared environment (e² = 1 - rMZ).' if slot.d >= 4 else '.')
            + (' Explain one assumption on which the estimate depends.' if slot.d >= 3 else ''))
    ans = f'h² = 2({rmz:.2f} - {rdz:.2f}) = {h2:.2f} ({100 * h2:.0f}%)'
    if slot.d >= 4:
        ans += f'; c² = {rmz:.2f} - {h2:.2f} = {c2:.2f}; e² = 1 - {rmz:.2f} = {e2:.2f}'
    key = f'M1 substitution into the formula; A1 {ans}.'
    if slot.d >= 3:
        key += ' R1 equal environments assumption: MZ and DZ twins are assumed to share equally similar environments (if MZ twins are treated more alike, h² is overestimated).'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=2 + (slot.d >= 3) + (slot.d >= 4))


# ---------------------------------------------------------------------------------------------
# ch06 Cognitive content: cognitive processing and memory
# ---------------------------------------------------------------------------------------------
K.facts('ch06-st1', F(
    terms=[('multi-store model', 'Atkinson and Shiffrin\'s (1968) model in which information flows from sensory memory to short-term memory to long-term memory, with attention and rehearsal moving it between stores'),
           ('short-term memory', 'a limited-capacity store (about 7 ± 2 items, Miller, 1956) that holds information for about 18-30 seconds without rehearsal'),
           ('long-term memory', 'a store with potentially unlimited capacity and duration, mainly encoded semantically'),
           ('working memory model', 'Baddeley and Hitch\'s (1974) model of short-term memory as an active system with a central executive, phonological loop, visuospatial sketchpad and (added 2000) episodic buffer'),
           ('phonological loop', 'the component of working memory that holds speech-based information, including the articulatory rehearsal process'),
           ('central executive', 'the component of working memory that directs attention and coordinates the slave systems'),
           ('serial position effect', 'the tendency to recall items at the start (primacy) and end (recency) of a list better than items in the middle'),
           ('articulatory suppression', 'repeating an irrelevant word aloud to occupy the phonological loop during a memory task')],
    facts=[('According to Miller (1956), the capacity of short-term memory is about:', '7 ± 2 items', ['3 ± 1 items', '20 items', 'Unlimited'],
            'Miller\'s "magical number seven, plus or minus two"; later research (Cowan, 2001) suggests about 4 chunks.'),
           ('Peterson and Peterson (1959) found that recall of trigrams after 18 seconds of counting backwards fell to about:', '10%', ['50%', '90%', '0%'],
            'Preventing rehearsal showed STM duration is brief.'),
           ('In Glanzer and Cunitz (1966), a 30-second delay before recall eliminated which effect?', 'The recency effect', ['The primacy effect', 'The Stroop effect', 'The word length effect'],
            'The delay displaced the last items from STM, while primacy (LTM) remained.'),
           ('Which component was added to the working memory model by Baddeley in 2000?', 'The episodic buffer', ['The phonological loop', 'The visuospatial sketchpad', 'The central executive'],
            'The episodic buffer integrates information across systems and with LTM.')],
    why=[('Explain how the serial position effect supports the multi-store model.', 'Primacy reflects early items rehearsed into LTM and recency reflects items still in STM; Glanzer and Cunitz (1966) found a delay removed only recency, suggesting two separate stores.'),
         ('Explain why the working memory model replaced the idea of a single short-term store.', 'Dual-task studies show people can do a verbal and a visual task at the same time with little interference but not two verbal tasks, suggesting separate subsystems (phonological loop and visuospatial sketchpad) rather than one unitary store.'),
         ('Explain why case studies of brain damage challenge the multi-store model.', 'Patient KF (Shallice and Warrington, 1970) had impaired verbal STM but normal visual STM and LTM, suggesting STM is not a single store and that information can reach LTM without passing through an intact STM.')],
    contrast=[('the multi-store model', 'the working memory model', 'The multi-store model treats STM as a single passive store on the way to LTM, while the working memory model describes STM as an active, multi-component system for manipulating information.'),
              ('primacy', 'recency', 'Primacy is better recall of the first items in a list (thought to be due to rehearsal into LTM); recency is better recall of the last items (still held in STM).')],
    misc=[('The multi-store model says rehearsal is the only way information gets into long-term memory.', 'This is a criticism, not a strength: the model emphasises maintenance rehearsal, but levels-of-processing research (Craik and Lockhart, 1972) shows deep, meaningful processing transfers information without rehearsal.'),
          ('Working memory is the same as long-term memory.', 'Working memory is a temporary, limited-capacity system for holding and manipulating information; LTM is a durable store.')],
    cases=[('remembering a phone number', 'Hana reads a phone number, repeats it to herself and dials it; a minute later she cannot remember it.', 'the multi-store model', 'maintenance rehearsal kept the number in STM long enough to dial, but without further rehearsal or meaningful encoding it decayed or was displaced'),
           ('driving while talking', 'Felix can drive and listen to music easily, but finds it hard to navigate a new route while talking on a hands-free phone.', 'the working memory model', 'familiar driving and music use different, partly automatic systems, but navigation (visuospatial and central executive) and conversation both draw on the central executive, causing interference')],
    apply=[('A student revises vocabulary by repeating words aloud while also listening to a podcast. Using the working memory model, explain why this may be ineffective.', 'Both repeating words and listening to speech use the phonological loop, so the two tasks compete for the same limited-capacity subsystem and interfere, reducing encoding.', 3)],
    evaluate=[('The working memory model is a better explanation of short-term memory than the multi-store model.', ['dual-task evidence for separate subsystems', 'explains KF\'s selective deficit', 'Landry and Bartling (2011): articulatory suppression'],
               ['central executive is vague', 'mostly lab tasks', 'the MSM explains the STM-LTM distinction well'],
               'The working memory model explains STM processing better, but the MSM still usefully describes the flow between STM and LTM.')],
))
K.study('ch06-st1', 'Glanzer and Cunitz', 1966, 'the serial position effect', 'to investigate whether a delay before recall affects primacy and recency effects',
        'US army enlisted men heard lists of 15 words and recalled them either immediately or after a 10- or 30-second delay filled with counting.',
        'immediate recall showed both primacy and recency; with a 30-second delay the recency effect disappeared while primacy remained',
        'separate short-term and long-term stores in the multi-store model',
        ['controlled lab experiment; replicable', 'clear dissociation supports two stores'],
        ['word lists lack ecological validity', 'all-male military sample'],
        mtype='laboratory experiment', iv='delay before recall (0, 10 or 30 seconds)', dv='proportion of words recalled at each serial position',
        wrong=['A delay eliminated the primacy effect but not recency', 'Neither effect was affected by delay', 'Recall was best for words in the middle of the list'])
K.study('ch06-st1', 'Landry and Bartling', 2011, 'articulatory suppression and the phonological loop', 'to investigate whether articulatory suppression reduces serial recall of letters',
        'Students were randomly allocated to recall lists of phonologically dissimilar letters either normally or while repeating "1-2" aloud (articulatory suppression).',
        'the articulatory suppression group recalled significantly fewer letters in the correct order (about 45% vs 76%)',
        'the phonological loop in the working memory model',
        ['random allocation; standardised procedure', 'replicates earlier findings'],
        ['small student sample', 'artificial task'],
        mtype='laboratory experiment', iv='articulatory suppression vs control', dv='percentage of letters recalled in the correct serial position')
K.study('ch06-st1', 'Peterson and Peterson', 1959, 'the duration of short-term memory', 'to investigate how long information remains in short-term memory without rehearsal',
        '24 students heard consonant trigrams (e.g. "KTH") and counted backwards in threes from a given number for 3-18 seconds before recall.',
        'recall fell sharply: about 80% after 3 seconds and about 10% after 18 seconds',
        'the brief duration of short-term memory without rehearsal',
        ['high control; counting prevented rehearsal'],
        ['trigrams lack meaning', 'interference from earlier trials (not just decay) may explain forgetting (Keppel and Underwood, 1962)'],
        mtype='laboratory experiment', iv='retention interval (3-18 seconds)', dv='percentage of trigrams correctly recalled')

K.facts('ch06-st2', F(
    terms=[('schema', 'a mental representation of knowledge about an object, person, situation or event, based on prior experience, that guides perception and memory'),
           ('script', 'a schema for a sequence of actions in a familiar situation, such as visiting a restaurant'),
           ('self-schema', 'a schema containing beliefs about oneself'),
           ('top-down processing', 'perception guided by prior knowledge and expectations (schemas) rather than only by incoming sensory data'),
           ('assimilation (schema)', 'interpreting new information in terms of existing schemas'),
           ('rationalisation', 'distorting a memory so that it makes sense in terms of one\'s schemas, as in Bartlett\'s (1932) study')],
    facts=[('In Bartlett\'s (1932) "War of the Ghosts" study, participants\' recall became:', 'Shorter and more consistent with their own culture', ['Longer and more detailed', 'Completely accurate', 'More unusual and supernatural'],
            'Participants omitted and changed unfamiliar details to fit English cultural schemas.'),
           ('In Bransford and Johnson (1972), which group understood and recalled the passage about washing clothes best?', 'Those given the topic before reading it', ['Those given the topic after reading it', 'Those given no topic', 'Those who read it twice without a topic'],
            'Activating the schema before encoding improved comprehension and recall.'),
           ('Brewer and Treyens (1981) found participants falsely recalled which object in the office?', 'Books', ['A skull', 'A picnic basket', 'A typewriter'],
            'Books are schema-consistent with an office, although none were present.')],
    why=[('Explain how schemas can lead to errors in memory.', 'At encoding schemas direct attention to consistent information; at retrieval gaps are filled with schema-consistent details (reconstruction), so people recall what they expect - e.g. false recall of books in Brewer and Treyens (1981).'),
         ('Explain why schemas are useful.', 'They allow fast, efficient processing of information, make the world predictable, and help comprehension and recall of new information that fits existing knowledge.')],
    contrast=[('a schema', 'a script', 'A schema is any organised knowledge structure; a script is a specific type of schema about the expected sequence of events in a situation (e.g. a restaurant visit).')],
    misc=[('Schemas only affect memory, not perception.', 'Schemas influence perception through top-down processing - e.g. the same ambiguous figure is seen differently depending on expectations.'),
          ('Schema theory can be directly observed and measured.', 'Schemas are hypothetical constructs inferred from behaviour; it is hard to define and measure them directly, a common criticism of the theory.')],
    cases=[('a tourist ordering in a Tokyo restaurant', 'Lars, visiting from Sweden, expects to leave a tip and is surprised when the waiter runs after him to return the money.', 'schema theory', 'his restaurant script includes tipping, which is not part of the Japanese script, showing how culturally learned schemas guide expectations and behaviour')],
    apply=[('A teacher wants students to remember a complex text about photosynthesis. Using schema theory, suggest one strategy and explain why it would help.', 'Activate prior knowledge first (e.g. give the title, an advance organiser or an analogy) so that new information can be assimilated into an existing schema - as Bransford and Johnson (1972) found that context before reading improved recall.', 3)],
    evaluate=[('Schema theory provides a convincing explanation of memory distortion.', ['Bartlett (1932), Brewer and Treyens (1981)', 'explains cultural differences in recall'],
               ['schema is vague and hard to measure', 'does not explain how schemas are acquired', 'memories can be accurate (Yuille and Cutshall, 1986)'],
               'Schema theory explains many distortions well but is too vague to predict exactly when distortion will occur.')],
))
K.study('ch06-st2', 'Bartlett', 1932, 'the "War of the Ghosts" story', 'to investigate how cultural schemas affect the recall of an unfamiliar story',
        'English participants read a Native American folk tale, "The War of the Ghosts", and reproduced it several times over intervals (repeated reproduction) or passed it along a chain of people (serial reproduction).',
        'recall became shorter, unfamiliar details were omitted or changed to fit English culture (e.g. "canoes" became "boats"), and the story was rationalised',
        'the reconstructive nature of memory guided by schemas',
        ['high ecological validity - meaningful material', 'pioneered the study of memory as reconstruction'],
        ['no standardised instructions or controlled intervals', 'qualitative interpretation of changes', 'some changes may have been deliberate guessing'],
        mtype='laboratory experiment', wrong=['Recall became longer and more detailed over time', 'Participants recalled the story perfectly each time', 'Unfamiliar supernatural elements were emphasised and exaggerated'])
K.study('ch06-st2', 'Bransford and Johnson', 1972, 'context and comprehension of a passage', 'to investigate whether activating a schema before reading improves comprehension and recall',
        'Students listened to an ambiguous passage about washing clothes; one group was given the topic before, one after and one not at all, and they rated comprehension and recalled the passage.',
        'the group given the topic before the passage rated comprehension higher and recalled about twice as many idea units as the other groups',
        'the role of schemas in encoding',
        ['random allocation; standardised passage', 'clear support for encoding effects of schemas'],
        ['artificial, deliberately ambiguous passage', 'student sample'],
        mtype='laboratory experiment', iv='timing of the topic (before, after, none)', dv='number of idea units recalled and comprehension rating')
K.study('ch06-st2', 'Brewer and Treyens', 1981, 'schemas and memory for an office', 'to investigate whether schemas affect the recall of objects in a room',
        '30 participants waited individually for 35 seconds in an "office" containing schema-consistent and inconsistent objects, then unexpectedly had to recall what was in the room.',
        'participants recalled schema-consistent objects (desk, chair) best and some falsely recalled books, which had not been present',
        'schema-driven errors in memory',
        ['incidental learning - participants did not know they would be tested', 'realistic setting'],
        ['small sample', 'deception about the purpose of waiting'],
        mtype='laboratory experiment')

K.facts('ch06-st3', F(
    terms=[('dual-process model', 'the model that thinking involves two systems: a fast, automatic, intuitive System 1 and a slow, effortful, rational System 2'),
           ('System 1', 'fast, automatic, intuitive and effortless thinking that relies on heuristics'),
           ('System 2', 'slow, deliberate, effortful and analytical thinking that can override System 1'),
           ('heuristic', 'a mental shortcut that allows fast judgements but can lead to systematic errors'),
           ('cognitive reflection', 'the tendency to override an intuitive but wrong answer and engage in further reflection'),
           ('disfluency', 'difficulty in processing information (e.g. a hard-to-read font) that may trigger more analytical System 2 thinking')],
    facts=[('In Frederick\'s (2005) bat-and-ball problem, the intuitive but wrong answer is:', '10 cents', ['5 cents', '1 dollar', '1.05 dollars'],
            'The correct answer is 5 cents (bat = $1.05).'),
           ('The dual-process model is most associated with which researcher?', 'Daniel Kahneman', ['Elizabeth Loftus', 'Albert Bandura', 'Jean Piaget'],
            'Thinking, Fast and Slow (2011) popularised Systems 1 and 2.'),
           ('Alter et al. (2007) found that presenting the CRT in a hard-to-read font:', 'Reduced errors', ['Increased errors', 'Had no effect', 'Made participants answer faster'],
            'Disfluency triggered System 2 thinking.')],
    why=[('Explain why System 1 thinking can lead to errors.', 'It relies on heuristics and associations to produce quick answers, so in problems where the intuitive answer is wrong (e.g. the bat-and-ball problem) people accept it without checking.'),
         ('Explain why the dual-process model is useful for understanding decision-making.', 'It explains why people are often irrational (System 1 biases) yet capable of careful reasoning, and predicts when errors occur (time pressure, cognitive load) and how to reduce them (slow down, disfluency).')],
    contrast=[('System 1', 'System 2', 'System 1 is fast, automatic and effortless, using heuristics; System 2 is slow, controlled and effortful, using rules and analysis, and can override System 1.')],
    misc=[('System 1 is always wrong and System 2 is always right.', 'System 1 is usually efficient and accurate for familiar tasks; System 2 can also make errors, and expert intuition can be very accurate.')],
    cases=[('impulse buying online', 'Arjun buys a jacket in a "flash sale" countdown on a shopping app, then realises later he did not need it.', 'the dual-process model', 'time pressure and emotional cues triggered fast System 1 decisions before System 2 could evaluate the purchase')],
    apply=[('A bank wants customers to think carefully before taking out loans. Using the dual-process model, suggest one change to the loan application and explain why it might work.', 'Add a "cooling-off" pause and a question requiring calculation of total repayment - this slows decisions and engages System 2 instead of an intuitive System 1 response.', 3)],
    evaluate=[('The dual-process model provides an accurate account of human thinking.', ['CRT results (Frederick, 2005)', 'disfluency studies (Alter et al., 2007)', 'explains heuristics and biases'],
               ['two systems may be an oversimplification of a continuum', 'Alter\'s disfluency effect failed to replicate in large samples (Meyer et al., 2015)', 'hard to identify neural basis of each system'],
               'The model is a useful description of fast and slow processing, but may oversimplify thinking into two systems.')],
))
K.study('ch06-st3', 'Frederick', 2005, 'the Cognitive Reflection Test', 'to measure the tendency to override intuitive but incorrect answers',
        'Over 3,000 participants, mostly at US universities, answered three problems (e.g. the bat-and-ball problem) designed to elicit a fast, wrong answer.',
        'many participants gave the intuitive wrong answers; scores varied by university (e.g. MIT students scored highest) and correlated with patience and risk preferences',
        'the dual-process model of thinking',
        ['large sample; simple, objective measure', 'widely replicated'],
        ['mostly university students', 'the problems are now widely known, reducing validity'],
        mtype='correlational study')
K.study('ch06-st3', 'Alter et al.', 2007, 'disfluency and analytical thinking', 'to investigate whether processing difficulty triggers System 2 thinking',
        'Princeton students completed the three-item CRT printed either in an easy-to-read font or a hard-to-read, small grey italic font.',
        '90% of the fluent group made at least one error compared with 35% in the disfluent group',
        'how disfluency triggers System 2 thinking',
        ['random allocation; simple manipulation'],
        ['small sample (40 students)', 'large replications found no reliable effect (Meyer et al., 2015)'],
        mtype='laboratory experiment', iv='font fluency (easy vs hard to read)', dv='number of CRT errors',
        wrong=['The disfluent font increased errors', 'Font had no effect on errors in the original study', 'Participants with the easy font made fewer errors'])

K.facts('ch06-st4', F(
    terms=[('hippocampus', 'a structure in the medial temporal lobe involved in forming new declarative memories and in spatial memory'),
           ('anterograde amnesia', 'the inability to form new long-term memories after brain damage'),
           ('retrograde amnesia', 'the loss of memories formed before brain damage'),
           ('declarative memory', 'memory for facts (semantic) and events (episodic) that can be consciously recalled'),
           ('procedural memory', 'memory for skills and how to do things, often expressed without conscious recall'),
           ('memory consolidation', 'the process by which new memories are stabilised and stored in long-term memory, which involves the hippocampus')],
    facts=[('HM\'s surgery in 1953 removed parts of which brain region on both sides?', 'The medial temporal lobes, including much of the hippocampus', ['The occipital lobes', 'The prefrontal cortex', 'The cerebellum'],
            'Scoville removed medial temporal lobe tissue to treat severe epilepsy.'),
           ('Which ability did HM retain, showing improvement over days on a mirror-drawing task?', 'Procedural memory', ['Episodic memory for new events', 'Semantic memory for new facts', 'Memory of meeting the researchers'],
            'He improved without remembering having done the task before (Milner, 1962).'),
           ('Corkin et al. (1997) used which technique to study HM\'s brain?', 'MRI', ['EEG', 'PET', 'Post-mortem dissection only'],
            'MRI showed the extent of the lesion, including some remaining posterior hippocampal tissue.')],
    why=[('Explain what HM\'s case shows about the role of the hippocampus in memory.', 'After bilateral removal of the medial temporal lobes he could not form new declarative memories but kept STM and procedural learning, suggesting the hippocampus is needed to consolidate declarative memories into LTM but not for STM or skills.'),
         ('Explain why HM\'s case supports the idea of separate memory systems.', 'He had normal short-term memory and could learn new motor skills but could not form new declarative memories, showing that STM, procedural and declarative memory depend on different brain systems.')],
    contrast=[('anterograde amnesia', 'retrograde amnesia', 'Anterograde amnesia is the inability to form new memories after damage (HM\'s main problem); retrograde amnesia is the loss of memories formed before the damage.'),
              ('declarative memory', 'procedural memory', 'Declarative memory is conscious memory for facts and events; procedural memory is memory for skills, shown in performance rather than conscious recall.')],
    misc=[('HM lost all his memories after surgery.', 'HM retained most memories from before the surgery (though some retrograde loss for the years just before), his STM and his procedural learning; his main deficit was forming new declarative memories.')],
    cases=[('Clive Wearing', 'Clive Wearing, a British musician, developed severe amnesia in 1985 after a viral infection damaged his hippocampus; he could not remember events from minutes before but could still play the piano and conduct.', 'the brain basis of memory', 'damage to the hippocampus destroyed the ability to form new declarative memories, while procedural musical skills were preserved, supporting separate memory systems')],
    apply=[('An older adult with early Alzheimer\'s disease can still ride a bicycle but forgets conversations she had an hour ago. Using research on HM, explain this pattern.', 'Alzheimer\'s often damages the hippocampus early, impairing consolidation of new declarative memories (like HM), while procedural memory, which depends on other structures (cerebellum, basal ganglia), is relatively spared.', 3)],
    evaluate=[('Case studies of brain damage like HM provide convincing evidence about how memory works in typical brains.', ['detailed, longitudinal testing over 50 years', 'later confirmed by MRI and other patients'],
               ['unique case; epilepsy and medication may have altered the brain', 'damage was not limited to the hippocampus', 'cannot generalise to healthy brains'],
               'HM provides strong evidence for the role of the hippocampus, especially when combined with imaging and animal research, but must be generalised with care.')],
))
K.study('ch06-st4', 'Scoville and Milner', 1957, 'memory loss after medial temporal lobe surgery', 'to describe the effects of bilateral medial temporal lobe removal on memory',
        'Case study of HM (Henry Molaison), whose medial temporal lobes, including much of the hippocampus, were removed in 1953 to treat epilepsy; he was assessed with interviews, IQ and memory tests.',
        'HM had severe anterograde amnesia for new declarative information, with normal IQ and intact short-term memory',
        'the role of the hippocampus in forming new long-term memories',
        ['detailed testing over many years', 'unique opportunity to link a specific lesion to memory'],
        ['single case', 'extent of damage unknown until later MRI', 'consent issues - HM could not remember agreeing to take part'],
        mtype='case study', ethics='HM could not remember giving consent to repeated testing; consent was obtained from relatives, and his identity was protected until his death.',
        wrong=['HM lost all memories from before his surgery', 'HM\'s short-term memory was severely impaired', 'HM could not learn any new skills'])
K.study('ch06-st4', 'Corkin et al.', 1997, 'MRI of HM\'s brain', 'to determine the exact extent of HM\'s brain lesion',
        'Structural MRI scans of HM\'s brain were taken and analysed in detail.',
        'the lesion included the medial temporal pole, most of the amygdala, the entorhinal cortex and the anterior part of the hippocampus; about 2 cm of posterior hippocampus remained',
        'the localisation of memory consolidation in the medial temporal lobe',
        ['objective, detailed anatomical data', 'clarified which structures were damaged'],
        ['still a single case', 'cannot show which specific structure caused which deficit'],
        mtype='case study')

# ---------------------------------------------------------------------------------------------
# ch07 Cognitive content: reliability of cognitive processes and emotion
# ---------------------------------------------------------------------------------------------
K.facts('ch07-st1', F(
    terms=[('reconstructive memory', 'the idea that memories are not exact recordings but are rebuilt at retrieval, using schemas and later information, so they can be distorted'),
           ('leading question', 'a question that, by its form or content, suggests a particular answer'),
           ('misinformation effect', 'the distortion of a memory by misleading information presented after the event'),
           ('post-event information', 'information received after an event that can be incorporated into the memory of it'),
           ('false memory', 'a recollection of an event that did not happen or that is significantly distorted'),
           ('cognitive interview', 'a police interviewing technique based on memory research that uses context reinstatement, reporting everything, changing order and changing perspective')],
    facts=[('In Loftus and Palmer\'s (1974) first experiment, what was the mean speed estimate for the verb "smashed"?', '40.8 mph', ['31.8 mph', '20.5 mph', '55.2 mph'],
            '"Contacted" produced the lowest estimate (31.8 mph).'),
           ('In Loftus and Palmer\'s second experiment, how many of the 50 participants in the "smashed" condition falsely reported seeing broken glass?', '16', ['7', '6', '32'],
            '7 in the "hit" condition and 6 in the control condition reported broken glass.'),
           ('Loftus and Pickrell (1995) found that about what proportion of participants came to "remember" being lost in a shopping mall?', 'About 25%', ['About 75%', 'About 2%', 'About 50%'],
            '6 of 24 participants recalled the false event fully or partially.'),
           ('Yuille and Cutshall (1986) found that real witnesses to a shooting in Vancouver:', 'Remained accurate months later and resisted misleading questions', ['Were highly suggestible', 'Remembered nothing after four months', 'Invented the shooting'],
            'Their study challenged the ecological validity of lab research on eyewitness memory.')],
    why=[('Explain how leading questions can distort eyewitness testimony.', 'A leading question introduces post-event information (e.g. "smashed") that either biases the response or alters the stored memory itself, so the witness reconstructs the event in line with the question - as shown by more false reports of broken glass in Loftus and Palmer (1974).'),
         ('Explain why laboratory studies of eyewitness memory may lack ecological validity.', 'Participants watch short videos with no emotional involvement or consequences, whereas real witnesses experience arousal and know their testimony matters; Yuille and Cutshall (1986) found real witnesses were more accurate.')],
    contrast=[('response bias', 'memory distortion', 'Response bias means the question influences the answer without changing the memory; memory distortion means the post-event information changes the memory itself (supported by false reports of broken glass a week later).')],
    misc=[('Eyewitness memory is like a video recording that can be played back.', 'Memory is reconstructive: details are rebuilt from fragments, schemas and post-event information each time we recall, so it can change.'),
          ('Confident eyewitnesses are always accurate.', 'Confidence can be inflated by feedback and repeated questioning; DNA exonerations (the Innocence Project) show many confident witnesses were wrong.')],
    cases=[('a wrongful conviction later overturned by DNA', 'In 1984 Jennifer Thompson confidently identified Ronald Cotton as her attacker in North Carolina; he served over 10 years before DNA evidence identified another man.', 'reconstructive memory and eyewitness testimony', 'her memory was reconstructed through line-up procedures and repeated exposure to Cotton\'s face, showing that confident testimony can be inaccurate'),
           ('a police officer\'s questions after a traffic accident', 'At an accident in Lima, an officer asks a witness, "Did you see the car run the red light?"', 'leading questions', 'the question presupposes the car ran the light, which may bias the witness\'s answer or alter the memory itself')],
    apply=[('A police force in Nairobi wants to improve the accuracy of eyewitness statements. Using research, suggest two changes to interview procedures.', 'Avoid leading questions (Loftus and Palmer, 1974); use the cognitive interview (context reinstatement, report everything, change order and perspective); interview soon after the event before post-event information; record interviews.', 4)],
    evaluate=[('Eyewitness testimony is too unreliable to be used in court.', ['leading questions (Loftus and Palmer, 1974)', 'false memories (Loftus and Pickrell, 1995)', 'DNA exonerations'],
               ['real witnesses can be accurate (Yuille and Cutshall, 1986)', 'lab studies lack ecological validity', 'the cognitive interview improves accuracy'],
               'Eyewitness testimony can be accurate under the right conditions; it should be used with caution, good interview practice and corroborating evidence.')],
))
K.study('ch07-st1', 'Loftus and Palmer', 1974, 'leading questions and eyewitness testimony', 'to investigate whether the wording of a question affects eyewitness estimates of speed and memory of an event',
        'Experiment 1: 45 students watched clips of car accidents and were asked how fast the cars were going when they "smashed", "collided", "bumped", "hit" or "contacted" each other. Experiment 2: 150 students were asked with "smashed", "hit" or no speed question, and a week later asked if they had seen broken glass.',
        'speed estimates were highest for "smashed" (40.8 mph) and lowest for "contacted" (31.8 mph); in experiment 2, 16/50 "smashed" participants reported broken glass compared with 7/50 for "hit" and 6/50 controls',
        'reconstructive memory and the effect of leading questions',
        ['controlled lab experiment with a manipulated IV', 'experiment 2 suggests memory itself was altered'],
        ['students watching film clips - low ecological validity and no emotional arousal', 'students are poor at estimating speed', 'demand characteristics'],
        mtype='laboratory experiment', iv='verb used in the critical question (smashed, collided, bumped, hit, contacted)', dv='estimated speed in mph',
        ethics='Mild deception about the aim; no significant harm, so the study is generally considered ethical with debriefing.',
        wrong=['The verb "contacted" produced the highest speed estimates', 'Question wording had no effect on speed estimates', 'More control participants reported broken glass than "smashed" participants'])
K.study('ch07-st1', 'Yuille and Cutshall', 1986, 'real eyewitnesses to a shooting', 'to investigate the accuracy of eyewitness memory of a real crime',
        '13 of 21 witnesses to a fatal shooting in Vancouver were interviewed 4-5 months later, including two misleading questions; accounts were compared with the original police interviews and evidence.',
        'witnesses remained highly accurate after several months and were not misled by the leading questions; those most distressed at the time were among the most accurate',
        'the reliability of eyewitness memory in real-life settings',
        ['high ecological validity - real crime', 'compared with police records'],
        ['small, self-selected sample', 'no control over what witnesses saw, discussed or read in the media'],
        mtype='case study')
K.study('ch07-st1', 'Loftus and Pickrell', 1995, 'implanting a false childhood memory', 'to investigate whether a false memory of a childhood event can be implanted',
        '24 participants read booklets describing three true childhood events (from relatives) and one false event about being lost in a shopping mall, and were interviewed twice over several weeks.',
        'about 25% (6 of 24) came to remember the false event fully or partially; they rated it less clear than the true memories',
        'the creation of false memories through suggestion',
        ['used relatives to make false memory plausible', 'showed entire events can be implanted'],
        ['small sample', 'getting lost is common and plausible - may not apply to traumatic events', 'deception'],
        mtype='laboratory experiment', ethics='Participants were deceived and a false memory was deliberately implanted; full debriefing was needed to correct the memory and avoid distress.')

K.facts('ch07-st2', F(
    terms=[('cognitive bias', 'a systematic error in thinking that affects judgements and decisions'),
           ('anchoring bias', 'the tendency to rely heavily on an initial value (the anchor) when making an estimate'),
           ('framing effect', 'the tendency for choices to depend on whether options are presented in terms of gains or losses'),
           ('availability heuristic', 'judging the likelihood of events by how easily examples come to mind'),
           ('loss aversion', 'the tendency for losses to feel more powerful than equivalent gains'),
           ('representativeness heuristic', 'judging probability by how closely something resembles a typical case, ignoring base rates')],
    facts=[('In Tversky and Kahneman (1974), participants who saw the wheel stop at 65 gave a median estimate of the percentage of African countries in the UN of:', '45%', ['25%', '65%', '10%'],
            'Those who saw 10 estimated 25%.'),
           ('In Tversky and Kahneman\'s (1981) "Asian disease" problem, when options were framed as lives saved, most participants chose:', 'The certain option', ['The risky option', 'Neither option', 'Both equally'],
            '72% chose the certain option in the gain frame; 78% chose the risky option in the loss frame.'),
           ('People overestimate deaths from plane crashes compared with car accidents mainly because of:', 'The availability heuristic', ['Anchoring bias', 'The framing effect', 'Cognitive dissonance'],
            'Plane crashes are vivid and heavily reported, so they come to mind easily.')],
    why=[('Explain how the framing effect can influence decision-making.', 'The same outcome described as a gain or a loss triggers different reference points: people are risk-averse for gains and risk-seeking to avoid losses (prospect theory), so choices change with wording alone.'),
         ('Explain why heuristics are useful despite leading to bias.', 'They allow quick decisions with limited time and information, which are usually good enough; biases occur only in particular situations.')],
    contrast=[('anchoring bias', 'the availability heuristic', 'Anchoring is over-reliance on an initial number when estimating; availability is judging frequency or probability by how easily examples come to mind.')],
    misc=[('Anchoring only works when the anchor is relevant to the question.', 'Tversky and Kahneman (1974) showed that even a random number from a wheel of fortune biased estimates.')],
    cases=[('price labels in a shop in Dubai', 'A shop labels a watch "Was 900 AED, now 450 AED"; customers feel they are getting a bargain.', 'anchoring bias', 'the original price serves as an anchor, so 450 AED seems cheap even if the watch was never worth 900 AED'),
           ('a surgeon describing an operation', 'Doctors in Toronto tell one patient an operation has a "90% survival rate" and another a "10% mortality rate".', 'the framing effect', 'the same information framed as survival (gain) makes patients more likely to accept surgery than when framed as mortality (loss)')],
    apply=[('A government in Kuala Lumpur wants more people to register as organ donors. Using research on cognitive biases, suggest one strategy and explain why it might work.', 'Use an opt-out default and gain framing ("save up to eight lives"); defaults exploit status-quo bias and System 1 thinking, and positive framing increases acceptance (Tversky and Kahneman, 1981).', 3)],
    evaluate=[('Human decision-making is fundamentally irrational.', ['anchoring, framing, availability biases are robust', 'predictable deviations from rational choice'],
               ['heuristics are adaptive ("ecological rationality", Gigerenzer)', 'lab problems are artificial', 'experts often decide well in familiar domains'],
               'Decision-making is boundedly rational: biases are real, but heuristics are often effective in real environments.')],
))
K.study('ch07-st2', 'Tversky and Kahneman', 1974, 'anchoring in numerical estimates', 'to investigate whether an arbitrary number affects subsequent numerical estimates',
        'Participants watched a wheel of fortune (rigged to stop at 10 or 65) and then estimated whether the percentage of African countries in the UN was higher or lower than that number, and then gave an exact estimate.',
        'median estimates were 25% for the group that saw 10 and 45% for the group that saw 65',
        'the anchoring bias in judgement',
        ['simple, powerful manipulation; widely replicated'],
        ['artificial task with no consequences', 'student samples'],
        mtype='laboratory experiment', iv='the anchor number (10 or 65)', dv='estimated percentage of African countries in the UN',
        wrong=['The anchor had no effect on estimates', 'Participants who saw 10 gave higher estimates', 'Estimates were identical in both groups'])
K.study('ch07-st2', 'Tversky and Kahneman', 1981, 'the framing of decisions', 'to investigate whether the framing of options as gains or losses affects choices',
        'Students chose between two programmes to combat an "Asian disease" expected to kill 600 people; options were framed either in terms of lives saved or lives lost, with identical outcomes.',
        'in the gain frame 72% chose the certain option (200 saved); in the loss frame 78% chose the risky option',
        'the framing effect and loss aversion',
        ['identical outcomes isolate the framing', 'basis of prospect theory'],
        ['hypothetical choices', 'student samples in the USA and Canada'],
        mtype='laboratory experiment', iv='framing of options (gain vs loss)', dv='percentage choosing the certain vs risky option')
K.study('ch07-st2', 'Tversky and Kahneman', 1973, 'the availability heuristic and letter frequency', 'to investigate whether judgements of frequency depend on how easily examples come to mind',
        'Participants were asked whether letters such as K were more likely to appear as the first or the third letter in English words.',
        'about two-thirds judged K more likely in the first position, even though it is more common in the third, because words beginning with K are easier to retrieve',
        'the availability heuristic',
        ['simple, controlled task'],
        ['artificial question', 'only English speakers'],
        mtype='laboratory experiment')

K.facts('ch07-st3', F(
    terms=[('flashbulb memory', 'a vivid, detailed and long-lasting memory of the circumstances in which one learned of a surprising, emotionally significant event'),
           ('amygdala', 'an almond-shaped structure in the medial temporal lobe involved in processing emotion, especially fear, and in enhancing memory for emotional events'),
           ('consistency (memory)', 'the extent to which a person\'s account of an event remains the same over time, used to test flashbulb memories'),
           ('emotional arousal', 'the physiological activation associated with emotion, which can enhance memory consolidation'),
           ('rehearsal (overt)', 'retelling or discussing an event, which may strengthen but also alter flashbulb memories')],
    facts=[('Brown and Kulik (1977) coined the term "flashbulb memory". Which event did almost all participants recall vividly?', 'The assassination of John F. Kennedy', ['The moon landing', 'The Challenger explosion', 'The 9/11 attacks'],
            '79 of 80 participants had flashbulb memories of JFK\'s assassination.'),
           ('Neisser and Harsch (1992) studied memories of which event?', 'The Challenger space shuttle explosion', ['The 9/11 attacks', 'The death of Princess Diana', 'The JFK assassination'],
            'Memories collected the day after were compared with recall about two and a half years later.'),
           ('Sharot et al. (2007) found greater amygdala activation when recalling 9/11 in participants who were:', 'Close to the World Trade Center on the day', ['Far from Manhattan', 'Children at the time', 'Watching only on television'],
            'Personal proximity and emotion predicted amygdala involvement.')],
    why=[('Explain why flashbulb memories may not be as accurate as people believe.', 'They are reconstructed like other memories; Neisser and Harsch (1992) and Talarico and Rubin (2003) found accounts changed over time while confidence and vividness stayed high.'),
         ('Explain the role of the amygdala in emotional memory.', 'Emotional arousal activates the amygdala, which interacts with the hippocampus to enhance consolidation, making emotional events more memorable; stress hormones such as adrenaline contribute.')],
    contrast=[('the special-mechanism view of flashbulb memory', 'the ordinary-memory view', 'Brown and Kulik proposed a special neural "now print" mechanism; others argue flashbulb memories are ordinary memories that are rehearsed often and feel vivid, but are no more accurate.')],
    misc=[('Flashbulb memories are permanent and perfectly accurate.', 'They feel vivid and are held with confidence, but research shows they change over time (Neisser and Harsch, 1992).')],
    cases=[('memories of the COVID-19 lockdown announcement', 'Many people can describe exactly where they were when their government announced the first COVID-19 lockdown in March 2020.', 'flashbulb memory', 'the event was surprising, consequential and emotional, producing vivid memories; research predicts that details may still change over time despite high confidence')],
    apply=[('Design a study to test whether flashbulb memories of a recent major news event are more accurate than everyday memories. Outline the key features.', 'Collect reports of the news event and an everyday event within a day (test-retest); retest after weeks/months; compare consistency and confidence for both; repeated measures; ethical care with distressing events.', 4)],
    evaluate=[('Flashbulb memories are formed by a special memory mechanism.', ['vivid, confident, long-lasting (Brown and Kulik, 1977)', 'amygdala involvement (Sharot et al., 2007)'],
               ['inconsistent over time (Neisser and Harsch, 1992)', 'decline like ordinary memories (Talarico and Rubin, 2003)', 'rehearsal and media exposure can explain vividness'],
               'Emotion enhances confidence and vividness via the amygdala, but there is little evidence of a separate, accurate "special mechanism".')],
))
K.study('ch07-st3', 'Brown and Kulik', 1977, 'flashbulb memories of public events', 'to investigate whether people have especially vivid memories of surprising, consequential events',
        '80 American participants (40 white, 40 Black) answered questions about where they were when they heard about events such as the assassinations of John F. Kennedy and Martin Luther King.',
        'most had vivid memories of JFK\'s assassination; Black participants more often had flashbulb memories of the assassination of Martin Luther King, suggesting personal significance matters',
        'the role of emotion and personal significance in flashbulb memory',
        ['showed the role of personal relevance and consequentiality'],
        ['retrospective self-report with no way to check accuracy', 'correlational; long delays'],
        mtype='questionnaire survey')
K.study('ch07-st3', 'Neisser and Harsch', 1992, 'memories of the Challenger explosion', 'to test the accuracy of flashbulb memories over time',
        'The morning after the 1986 Challenger explosion, 106 students at Emory University wrote how they heard the news; about two and a half years later 44 of them completed the same questionnaire and rated their confidence.',
        'many accounts had changed substantially (mean accuracy about 2.95 out of 7), yet confidence remained high',
        'the reconstructive nature of flashbulb memories',
        ['compared memories with a baseline written the next day', 'longitudinal design'],
        ['attrition from 106 to 44 participants', 'the first report may itself have been inaccurate'],
        mtype='longitudinal study', wrong=['Accounts were almost identical after two and a half years', 'Confidence dropped sharply over time', 'Participants could not recall the event at all'])
K.study('ch07-st3', 'Sharot et al.', 2007, 'brain activity during recall of 9/11', 'to investigate the neural basis of flashbulb memories of the 9/11 attacks',
        'About three years after 9/11, 24 participants who had been in Manhattan recalled events from that day and from the summer of 2001 while in an fMRI scanner.',
        'participants who had been close to the World Trade Center (Downtown) showed greater amygdala activation for 9/11 memories than for summer memories; those further away (Midtown) did not',
        'the role of the amygdala in emotional memory',
        ['fMRI gives objective data on brain activity', 'within-subject comparison of events'],
        ['small sample', 'correlational; no measure of accuracy', 'possible distress from recalling trauma'],
        mtype='quasi-experiment')
K.study('ch07-st3', 'Talarico and Rubin', 2003, 'flashbulb and everyday memories of 9/11', 'to compare the consistency of flashbulb memories with everyday memories over time',
        'On 12 September 2001, 54 Duke University students recorded their memory of hearing about 9/11 and of a recent everyday event; they were retested after 1, 6 or 32 weeks.',
        'consistency declined at a similar rate for both types of memory, but ratings of vividness and confidence remained high only for the 9/11 memory',
        'whether flashbulb memories are more accurate than ordinary memories',
        ['baseline collected the day after', 'comparison with everyday memories'],
        ['student sample', 'everyday events differed in significance'],
        mtype='longitudinal study')

# ---------------------------------------------------------------------------------------------
# ch08 Sociocultural content: the individual, the group and culture
# ---------------------------------------------------------------------------------------------
K.facts('ch08-st1', F(
    terms=[('social identity theory', 'Tajfel and Turner\'s (1979) theory that part of a person\'s self-concept comes from group membership, and that people seek positive distinctiveness for their in-groups'),
           ('social categorisation', 'the process of classifying people, including oneself, into groups'),
           ('social identification', 'adopting the identity, norms and values of the group one has categorised oneself as belonging to'),
           ('social comparison', 'comparing one\'s in-group with out-groups in order to maintain positive self-esteem'),
           ('in-group favouritism', 'the tendency to favour members of one\'s own group over members of out-groups'),
           ('positive distinctiveness', 'the motivation to see one\'s in-group as different from and better than relevant out-groups'),
           ('minimal group paradigm', 'an experimental method in which participants are assigned to groups on trivial criteria to test whether categorisation alone produces in-group favouritism')],
    facts=[('In Tajfel et al. (1971), boys allocated points to anonymous group members. Which strategy did they often use?', 'Maximum difference, even at the expense of in-group profit', ['Maximum joint profit for all', 'Fairness at all times', 'Random allocation'],
            'They preferred a large difference in favour of their group to a larger absolute reward.'),
           ('Cialdini et al. (1976) found students wore university clothing more after their team:', 'Won a football game', ['Lost a football game', 'Was in the news for a scandal', 'Changed coach'],
            'This "basking in reflected glory" boosts self-esteem through group identity.'),
           ('Which is the correct order of the three stages in social identity theory?', 'Social categorisation, social identification, social comparison', ['Social comparison, social identification, social categorisation', 'Social identification, social categorisation, social comparison', 'Stereotyping, prejudice, discrimination'],
            'People categorise, identify, then compare.')],
    why=[('Explain why people show in-group favouritism even in minimal groups.', 'According to social identity theory, categorisation alone creates a social identity; to maintain positive self-esteem, people seek positive distinctiveness for their group, so they favour it even when groups are trivial and there is no conflict (Tajfel et al., 1971).'),
         ('Explain how social identity theory can explain prejudice.', 'Seeking positive distinctiveness through social comparison can lead to devaluing out-groups; when group status is threatened, people may derogate out-group members to protect their identity.')],
    contrast=[('personal identity', 'social identity', 'Personal identity is based on unique individual characteristics, while social identity is the part of the self-concept derived from membership of groups (e.g. nationality, team).')],
    misc=[('Social identity theory says group conflict always requires competition for resources.', 'That is realistic conflict theory; SIT holds that categorisation alone can produce in-group favouritism (minimal groups).')],
    cases=[('football fans after a derby', 'After their team wins a derby in Buenos Aires, fans wear club shirts to work and say "we won"; after a loss, they say "they lost".', 'social identity theory', 'fans bask in reflected glory to enhance self-esteem through the in-group and distance themselves after failure, consistent with Cialdini et al. (1976)'),
           ('a school house system', 'A school in Singapore divides students into four "houses" by random allocation; within weeks students cheer only for their house and tease others.', 'social categorisation and in-group favouritism', 'random categorisation is enough to create social identities and in-group bias, as in the minimal group paradigm')],
    apply=[('A company in Melbourne merges two teams who see each other as rivals. Using social identity theory, suggest one way to reduce in-group favouritism.', 'Create a superordinate, shared identity (new team name, common goals) so former out-group members become in-group members (recategorisation, the common in-group identity model).', 3)],
    evaluate=[('Social identity theory explains why people discriminate against out-groups.', ['minimal group studies (Tajfel et al., 1971)', 'BIRGing (Cialdini et al., 1976)'],
               ['in-group favouritism does not always mean out-group hostility', 'minimal group studies are artificial', 'cultural variation in group processes (Wetherell, 1982)'],
               'SIT explains in-group favouritism well, but other factors (competition, norms, personality) are needed to explain hostility.')],
))
K.study('ch08-st1', 'Tajfel et al.', 1971, 'minimal groups and intergroup discrimination', 'to investigate whether being categorised into a group is enough to produce in-group favouritism',
        '64 boys aged 14-15 from a school in Bristol were told they were in a group based on preference for paintings by Klee or Kandinsky (actually random), then allocated points to anonymous in-group and out-group members using matrices.',
        'boys favoured their in-group and often chose maximum difference between groups rather than maximum joint profit',
        'social categorisation and in-group favouritism',
        ['high control; trivial groups isolate categorisation', 'widely replicated'],
        ['artificial task with low consequences', 'demand characteristics', 'all-male British sample; collectivist samples may differ (Wetherell, 1982)'],
        mtype='laboratory experiment', iv='group membership (in-group vs out-group recipient)', dv='points allocated to in-group and out-group members',
        wrong=['Boys always chose maximum joint profit for both groups', 'Boys favoured the out-group', 'Boys allocated points randomly'],
        culture='Wetherell (1982) found Polynesian children in New Zealand were more generous to the out-group than white New Zealand children')
K.study('ch08-st1', 'Cialdini et al.', 1976, 'basking in reflected glory', 'to investigate whether people publicly associate themselves with successful in-groups',
        'Researchers recorded the wearing of university-identifying clothing by students at seven US universities on Mondays after football games, and coded pronoun use when students described the result.',
        'students wore more university clothing after wins and were more likely to say "we won" than "we lost"',
        'social identity and self-esteem',
        ['naturalistic observation of real behaviour', 'multiple universities'],
        ['correlational; other factors (weather) could affect clothing', 'US college sports culture'],
        mtype='naturalistic observation')

K.facts('ch08-st2', F(
    terms=[('social cognitive theory', 'Bandura\'s theory that behaviour is learned by observing others, and that cognition, behaviour and environment influence one another (reciprocal determinism)'),
           ('observational learning', 'learning by watching the behaviour of models and its consequences'),
           ('vicarious reinforcement', 'learning that occurs when an observer sees a model being rewarded for a behaviour'),
           ('self-efficacy', 'a person\'s belief in their ability to succeed in a specific task'),
           ('reciprocal determinism', 'Bandura\'s idea that personal factors, behaviour and environment continually influence each other'),
           ('modelling', 'the process of imitating the behaviour of a model')],
    facts=[('Which four processes did Bandura propose are needed for observational learning?', 'Attention, retention, reproduction and motivation', ['Encoding, storage, retrieval and rehearsal', 'Assimilation, accommodation, equilibration and schema', 'Perception, attention, motivation and reward'],
            'The observer must attend, remember, be able to reproduce the behaviour and be motivated to do so.'),
           ('In Bandura, Ross and Ross (1961), which group of children showed the most physical aggression?', 'Boys who observed an aggressive male model', ['Girls who observed an aggressive female model', 'Children who observed a non-aggressive model', 'The control group'],
            'Boys imitated physical aggression more, especially from a same-sex model.'),
           ('Bandura (1965) found that when children were offered rewards to imitate a model:', 'Differences between the reward, punishment and no-consequence conditions disappeared', ['Only the reward group imitated', 'No children could imitate', 'The punishment group imitated most'],
            'This showed the difference between learning and performance.')],
    why=[('Explain how vicarious reinforcement affects behaviour.', 'Observers learn the expected consequences of a behaviour by watching a model; seeing the model rewarded increases the motivation to imitate, while seeing punishment reduces it (Bandura, 1965).'),
         ('Explain why self-efficacy is important in social cognitive theory.', 'People only attempt behaviours they believe they can perform; higher self-efficacy increases effort and persistence, so it affects whether learned behaviour is reproduced.')],
    contrast=[('learning', 'performance', 'Bandura showed that children could learn a behaviour by observation (learning) but might not display it unless motivated to (performance); incentives revealed equal learning across conditions.')],
    misc=[('Observational learning only happens when the model is rewarded.', 'Learning can occur without reinforcement; reinforcement mainly affects whether the behaviour is performed (Bandura, 1965).')],
    cases=[('children copying a YouTuber', 'After watching a popular YouTuber perform dangerous "pranks" that get millions of views, a group of 10-year-olds in Lisbon start copying them at school.', 'social cognitive theory', 'children attend to an admired model, see vicarious reinforcement (views, fame), retain the actions and are motivated to reproduce them')],
    apply=[('A health campaign in Accra wants young people to wear seatbelts. Using social cognitive theory, suggest how the campaign could be designed.', 'Use similar, high-status models (local celebrities or peers) wearing seatbelts and being rewarded (approval), make the behaviour easy to reproduce, and build self-efficacy with simple steps.', 3)],
    evaluate=[('Social cognitive theory explains how children learn aggression.', ['Bandura et al. (1961) imitation of aggression', 'vicarious reinforcement (Bandura, 1965)'],
               ['Bobo doll is a toy designed to be hit - low ecological validity', 'Charlton et al. (2000) found no increase in aggression after TV arrived', 'ignores biological factors (testosterone, temperament)'],
               'SCT explains how specific aggressive acts are acquired, but whether they are performed depends on biological and social context.')],
))
K.study('ch08-st2', 'Bandura, Ross and Ross', 1961, 'imitation of aggressive models', 'to investigate whether children would imitate aggressive behaviour shown by an adult model',
        '72 children aged 3-6 from the Stanford University nursery were matched on aggressiveness and watched an adult model behave aggressively or non-aggressively towards a Bobo doll (or saw no model); they were then mildly frustrated and observed through a one-way mirror.',
        'children who saw the aggressive model imitated many of the specific aggressive acts; boys showed more physical aggression, and same-sex models were imitated more',
        'observational learning of aggression',
        ['controlled, standardised procedure with observers and inter-rater reliability', 'matched pairs controlled for initial aggressiveness'],
        ['Bobo doll invites hitting; low ecological validity', 'short-term effects only', 'ethical concerns: children were exposed to aggression and frustrated'],
        mtype='laboratory experiment', iv='type of model (aggressive, non-aggressive, none) and sex of model', dv='number of imitative aggressive acts in 20 minutes of observation',
        ethics='Children were exposed to aggressive behaviour and deliberately frustrated; parental consent and protection from harm are key concerns.',
        wrong=['Children who saw the non-aggressive model were most aggressive', 'Girls showed more physical aggression than boys', 'No children imitated the specific aggressive acts'])
K.study('ch08-st2', 'Bandura', 1965, 'vicarious reinforcement and imitation', 'to investigate whether the consequences to a model affect children\'s imitation of aggression',
        'Children watched a film of an adult behaving aggressively towards a Bobo doll and being rewarded, punished or receiving no consequences; they were then observed, and later offered incentives to reproduce the model\'s behaviour.',
        'children in the punished condition imitated least; when offered incentives, all groups imitated equally, showing learning had occurred in all conditions',
        'the distinction between learning and performance in social cognitive theory',
        ['separates learning from performance', 'controlled conditions'],
        ['artificial setting', 'short-term effects', 'children exposed to aggression'],
        mtype='laboratory experiment', iv='consequence to the model (reward, punishment, none)', dv='number of imitated aggressive acts')

K.facts('ch08-st3', F(
    terms=[('stereotype', 'a generalised, oversimplified belief about the characteristics of members of a group'),
           ('illusory correlation', 'the perception of a relationship between two variables (e.g. a minority group and negative behaviour) when no such relationship exists'),
           ('stereotype threat', 'the risk of confirming a negative stereotype about one\'s group, which can impair performance'),
           ('kernel of truth hypothesis', 'the idea that stereotypes may be based on some real, though exaggerated, group differences'),
           ('confirmation bias', 'the tendency to notice and remember information that confirms existing beliefs, which helps maintain stereotypes'),
           ('distinctiveness', 'the quality of being rare or unusual, which makes events more memorable and can create illusory correlations')],
    facts=[('In Steele and Aronson (1995), Black students underperformed on a verbal test when it was described as:', 'Diagnostic of intellectual ability', ['A problem-solving exercise', 'Unrelated to ability', 'A personality test'],
            'The diagnostic framing activated the stereotype threat.'),
           ('Hamilton and Gifford (1976) explained illusory correlation in terms of:', 'The co-occurrence of two distinctive (infrequent) events', ['Competition for resources', 'Genetic differences between groups', 'Observational learning'],
            'Minority-group members and undesirable behaviours were both rare, so their pairing was memorable.'),
           ('In Darley and Gross (1983), participants rated "Hannah" as more able when she was shown:', 'In a high socio-economic background and taking a test', ['In a low socio-economic background', 'Without taking a test', 'In a school uniform only'],
            'Stereotypes biased interpretation of the same ambiguous performance.')],
    why=[('Explain how stereotypes are formed through illusory correlation.', 'When two infrequent, distinctive things occur together (e.g. a minority group and an unusual negative behaviour), the pairing is highly memorable, so people overestimate how often they co-occur and form a stereotype (Hamilton and Gifford, 1976).'),
         ('Explain how stereotype threat can affect behaviour.', 'Awareness of a negative stereotype about one\'s group creates anxiety and cognitive load when performing a relevant task, reducing working memory capacity and performance, which may seem to "confirm" the stereotype.')],
    contrast=[('a stereotype', 'prejudice', 'A stereotype is a cognitive belief about a group; prejudice is a negative attitude or feeling towards the group, and discrimination is the behaviour.')],
    misc=[('Stereotypes are always negative.', 'Stereotypes can be positive (e.g. "Asians are good at maths"), but even positive stereotypes can be harmful, creating pressure or stereotype threat.')],
    cases=[('girls taking a maths test', 'Before a maths exam in Toronto, a teacher remarks that "boys usually do better on this test"; girls in the class then score lower than in previous tests.', 'stereotype threat', 'activating a negative stereotype increases anxiety and cognitive load, impairing performance (Spencer, Steele and Quinn, 1999)')],
    apply=[('A university in Cape Town wants to reduce stereotype threat in entrance exams. Suggest two strategies, based on research.', 'Present tests as non-diagnostic of ability; avoid asking for race or gender before the test; teach students about stereotype threat; use role models and growth-mindset messages.', 4)],
    evaluate=[('Stereotypes are formed mainly through cognitive processes.', ['illusory correlation (Hamilton and Gifford, 1976)', 'categorisation and schema processing'],
               ['social learning from media, family and peers', 'cultural transmission', 'kernel of truth from real social roles'],
               'Cognitive processes explain how stereotypes are formed and maintained, but their content is largely sociocultural.')],
))
K.study('ch08-st3', 'Steele and Aronson', 1995, 'stereotype threat and test performance', 'to investigate whether stereotype threat affects the performance of Black students on verbal tests',
        'Black and white Stanford students took a difficult verbal test from the GRE, described either as diagnostic of intellectual ability or as a non-diagnostic problem-solving task.',
        'Black students performed worse than white students in the diagnostic condition but equally well in the non-diagnostic condition, after controlling for SAT scores',
        'how stereotypes affect the behaviour of the stereotyped group',
        ['controlled for prior ability (SAT)', 'many replications across groups'],
        ['elite university sample', 'publication bias; some large replications show smaller effects (Flore and Wicherts, 2015)'],
        mtype='laboratory experiment', iv='test description (diagnostic vs non-diagnostic) and ethnicity of participant', dv='number of verbal test items answered correctly',
        wrong=['Black students outperformed white students in the diagnostic condition', 'Test description had no effect', 'White students underperformed in the non-diagnostic condition'])
K.study('ch08-st3', 'Hamilton and Gifford', 1976, 'illusory correlation in stereotype formation', 'to investigate whether stereotypes can form through illusory correlation',
        'Participants read 39 statements describing behaviours by members of group A (26: 18 desirable, 8 undesirable) or group B (13: 9 desirable, 4 undesirable), then estimated frequencies and rated the groups.',
        'participants overestimated the number of undesirable behaviours by the smaller group B and rated it less favourably, although the proportions were identical',
        'cognitive processes in the formation of stereotypes',
        ['controlled, artificial groups with identical ratios'],
        ['artificial groups and statements', 'student sample'],
        mtype='laboratory experiment')
K.study('ch08-st3', 'Darley and Gross', 1983, 'stereotypes and the interpretation of evidence', 'to investigate whether socio-economic stereotypes bias judgements of a child\'s ability',
        'Students watched a video of a girl, "Hannah", in either a high or low socio-economic setting; some then watched her take an ambiguous test and rated her ability.',
        'when they saw the test, participants rated Hannah as more able if they believed she came from a high socio-economic background',
        'how stereotypes bias the interpretation of information',
        ['controlled manipulation of background with identical test performance'],
        ['US student sample', 'artificial video task'],
        mtype='laboratory experiment')

K.facts('ch08-st4', F(
    terms=[('culture', 'the shared values, beliefs, norms, practices and artefacts of a group, transmitted across generations'),
           ('cultural norm', 'an expected, shared standard of behaviour within a cultural group'),
           ('cultural dimension', 'a scale on which cultures can be compared, such as individualism-collectivism (Hofstede)'),
           ('individualism', 'a cultural orientation emphasising personal goals, independence and the individual self'),
           ('collectivism', 'a cultural orientation emphasising group goals, interdependence and loyalty to the in-group'),
           ('power distance', 'the extent to which less powerful members of a society accept that power is distributed unequally'),
           ('uncertainty avoidance', 'the extent to which members of a culture feel threatened by ambiguity and prefer rules and structure'),
           ('long-term orientation', 'the extent to which a culture values persistence, saving and future rewards over short-term results and tradition')],
    facts=[('Hofstede\'s original cultural dimensions were based on survey data from employees of which company?', 'IBM', ['Toyota', 'Shell', 'Nestlé'],
            'Over 100,000 questionnaires from IBM employees in more than 50 countries (1967-1973).'),
           ('Berry (1967) found that the Temne of Sierra Leone conformed more than the Inuit of Baffin Island. He explained this by:', 'Differences in food-accumulating versus hunting economies', ['Genetic differences in conformity', 'Differences in IQ', 'The Temne being tested by a foreign researcher'],
            'Farming societies require cooperation and obedience; hunting societies reward independence.'),
           ('Which country typically scores highest on individualism in Hofstede\'s data?', 'The USA', ['Guatemala', 'China', 'Indonesia'],
            'The USA scored 91; Guatemala was among the lowest.')],
    why=[('Explain how cultural norms influence behaviour.', 'Norms define what is appropriate in a culture and are learned through enculturation; people conform to them to gain acceptance and avoid sanctions, e.g. norms of modesty affect how children describe good deeds (Fu et al., 2007).'),
         ('Explain why cultural dimensions should be used with caution.', 'They describe national averages, not individuals; cultures change over time; Hofstede\'s data came from one company decades ago; and dimensions can lead to stereotyping (ecological fallacy).')],
    contrast=[('individualism', 'collectivism', 'Individualist cultures emphasise personal goals, independence and personal achievement, while collectivist cultures emphasise group harmony, interdependence and duties to the in-group.'),
              ('high power distance', 'low power distance', 'In high power-distance cultures people accept hierarchy and defer to authority (e.g. Malaysia); in low power-distance cultures they expect equality and question authority (e.g. Denmark).')],
    misc=[('Everyone in a collectivist culture is collectivist.', 'Cultural dimensions describe averages; there is large individual variation within cultures (ecological fallacy).')],
    cases=[('a manager moving from Copenhagen to Kuala Lumpur', 'Ingrid, a Danish manager, asks her new team in Kuala Lumpur to criticise her plans openly; nobody does.', 'cultural dimensions', 'Malaysia has high power distance, so employees may avoid challenging a superior, unlike in low power-distance Denmark')],
    apply=[('A multinational company is training staff to work in Japan and the USA. Using one cultural dimension, explain how communication styles may differ.', 'Individualism-collectivism: US staff may value direct communication and individual credit; Japanese staff may value harmony, indirect communication and team credit - managers should adapt feedback styles accordingly.', 3)],
    evaluate=[('Hofstede\'s cultural dimensions are a valid way to explain cultural differences in behaviour.', ['very large data set', 'dimensions predict behaviour (e.g. conformity: Bond and Smith, 1996)'],
               ['data from one company in the 1970s', 'national level hides individual variation', 'Western-designed questionnaire (imposed etic)'],
               'The dimensions are a useful starting point for comparison but oversimplify cultures and must be supplemented by emic research.')],
))
K.study('ch08-st4', 'Hofstede', 1980, 'cultural dimensions in IBM employees', 'to identify dimensions on which national cultures differ',
        'Over 100,000 work-values questionnaires completed by IBM employees in more than 40 countries were analysed by factor analysis.',
        'four dimensions emerged: power distance, individualism-collectivism, uncertainty avoidance and masculinity-femininity (long-term orientation and indulgence were added later)',
        'cultural dimensions as a way of comparing cultures',
        ['very large data set; matched occupations across countries'],
        ['one company - may reflect IBM corporate culture', 'data from 1967-1973 may be out of date', 'nations are not cultures; ignores within-country variation'],
        mtype='cross-cultural survey', wrong=['Cultures were found to differ on only one dimension: wealth', 'There were no consistent differences between countries', 'Individualism was highest in Latin American countries'])
K.study('ch08-st4', 'Berry', 1967, 'conformity in the Temne and the Inuit', 'to investigate whether conformity differs between cultures with different economies',
        'Using an Asch-type line judgement task, Berry compared the conformity of Temne participants in Sierra Leone (a farming society) with Inuit participants on Baffin Island (a hunting society).',
        'the Temne conformed significantly more than the Inuit, which Berry linked to the need for cooperation in food-accumulating societies',
        'the influence of cultural norms on conformity',
        ['cross-cultural comparison with a standardised task', 'ecological explanation links culture to subsistence'],
        ['a Western task may have different meaning in each culture', 'researcher as outsider may influence responses'],
        mtype='quasi-experiment')

K.facts('ch08-st5', F(
    terms=[('enculturation', 'the process by which people learn the norms, values and practices of their own culture'),
           ('acculturation', 'the process of cultural and psychological change that occurs when two cultures come into contact'),
           ('integration', 'an acculturation strategy of maintaining one\'s heritage culture while also participating in the host culture'),
           ('assimilation', 'an acculturation strategy of adopting the host culture and giving up the heritage culture'),
           ('separation', 'an acculturation strategy of maintaining the heritage culture while avoiding the host culture'),
           ('marginalisation', 'an acculturation strategy, often not chosen, of losing contact with both heritage and host cultures'),
           ('acculturative stress', 'stress caused by the challenges of adapting to a new culture')],
    facts=[('Berry\'s (1997) acculturation model is based on two questions. What are they?', 'Is it valuable to maintain one\'s heritage culture, and to have relationships with the host culture?', ['Is the host culture individualist or collectivist, and is it wealthy?', 'Is the migrant young or old, and male or female?', 'Does the migrant speak the language, and have a job?'],
            'The answers create four strategies.'),
           ('Which acculturation strategy is generally associated with the lowest acculturative stress?', 'Integration', ['Assimilation', 'Separation', 'Marginalisation'],
            'Bicultural integration is usually most adaptive, though it depends on the host society\'s attitudes.'),
           ('Fu et al. (2007) found that, with age, Chinese children increasingly rated lying about their own good deeds as:', 'More positive (modesty)', ['More negative', 'Unimportant', 'Punishable'],
            'Canadian children rated such lies negatively, showing enculturation of norms.')],
    why=[('Explain how enculturation shapes children\'s moral behaviour.', 'Children learn cultural norms through observation, instruction and reinforcement from parents, teachers and peers; e.g. Chinese children learn modesty norms and come to approve of lying about good deeds (Fu et al., 2007).'),
         ('Explain why acculturation can cause stress.', 'Migrants face language barriers, discrimination, conflicting norms and loss of social support, which challenge identity and coping resources (Lueck and Wilson, 2010).')],
    contrast=[('enculturation', 'acculturation', 'Enculturation is learning one\'s own culture from birth; acculturation is change that occurs when a person or group comes into contact with another culture.'),
              ('integration', 'assimilation', 'Integration maintains the heritage culture while participating in the host culture; assimilation abandons the heritage culture in favour of the host culture.')],
    misc=[('Acculturation is a one-way process where migrants simply adopt the new culture.', 'Acculturation is two-way and multidimensional; people can maintain their heritage culture (integration or separation) and host cultures also change.')],
    cases=[('a Syrian family in Germany', 'Yusuf and his family arrived in Berlin in 2016. His children speak German at school and Arabic at home, celebrate Eid and join a local football club.', 'acculturation strategies', 'the children illustrate integration: they keep their heritage culture and participate in the host culture, associated with lower acculturative stress')],
    apply=[('A university in Melbourne wants to support international students. Using Berry\'s model, suggest one intervention and explain how it could reduce acculturative stress.', 'Encourage integration: buddy programmes with local students plus support for cultural associations, language classes and anti-discrimination policies - increasing host-culture contact while maintaining heritage identity.', 3)],
    evaluate=[('Integration is always the most successful acculturation strategy.', ['lower acculturative stress (Berry, 1997)', 'bilingualism protects (Lueck and Wilson, 2010)'],
               ['depends on host society\'s attitudes (multiculturalism vs assimilation policies)', 'correlational evidence; well-adjusted people may choose integration', 'self-report measures with translation issues'],
               'Integration is usually associated with better outcomes, but the effect depends on context and causality is unclear.')],
))
K.study('ch08-st5', 'Lueck and Wilson', 2010, 'acculturative stress in Asian Americans', 'to investigate factors associated with acculturative stress in Asian immigrants and Asian Americans',
        'Data from 2,095 Asian American participants in the National Latino and Asian American Study (NLAAS) were analysed for predictors of acculturative stress.',
        'language discrimination and family conflict were linked to higher acculturative stress, while bilingual proficiency and social networks were linked to lower stress',
        'factors affecting acculturative stress',
        ['large, nationally representative sample', 'identified protective factors'],
        ['correlational', 'self-report; "Asian American" includes very different groups'],
        mtype='correlational study')
K.study('ch08-st5', 'Fu et al.', 2007, 'cultural norms and children\'s evaluations of lying', 'to investigate how enculturation of modesty norms affects children\'s moral evaluations of lying',
        'Chinese and Canadian children aged 7, 9 and 11 heard stories in which a child performed a good deed and then either told the truth or lied about it, and rated the statements.',
        'with age, Chinese children rated lying about good deeds (modesty) more positively, while Canadian children rated it negatively',
        'enculturation of cultural norms',
        ['cross-cultural comparison with the same materials', 'shows developmental change'],
        ['cross-sectional; translation of stories', 'cultural groups not randomly assigned'],
        mtype='quasi-experiment')
K.study('ch08-st5', 'Berry', 1997, 'acculturation strategies', 'to propose a model of how individuals adapt when cultures come into contact',
        'Berry reviewed research on immigrants, refugees and indigenous groups and proposed a model based on two dimensions: maintaining the heritage culture and contact with the host culture.',
        'four strategies - integration, assimilation, separation and marginalisation - with integration usually linked to the best psychological adaptation and marginalisation to the worst',
        'acculturation strategies and adaptation',
        ['widely used, supported by many studies'],
        ['assumes individuals freely choose strategies', 'based mostly on Western host societies', 'categories may oversimplify'],
        mtype=None)

# ---------------------------------------------------------------------------------------------
# ch09 Context: health and well-being
# ---------------------------------------------------------------------------------------------
K.facts('ch09-st1', F(
    terms=[('biopsychosocial model', 'Engel\'s (1977) model that health and illness result from the interaction of biological, psychological and social factors'),
           ('biomedical model', 'the model that illness is caused by biological factors such as pathogens, genes or injury, and is treated by medical means'),
           ('health', 'according to the WHO (1948), a state of complete physical, mental and social well-being and not merely the absence of disease or infirmity'),
           ('subjective well-being', 'a person\'s own evaluation of their life satisfaction and emotional experience'),
           ('risk factor', 'a variable that increases the likelihood of developing a health problem'),
           ('protective factor', 'a variable that reduces the likelihood of developing a health problem or helps recovery')],
    facts=[('Who proposed the biopsychosocial model in the journal Science in 1977?', 'George Engel', ['Aaron Beck', 'Hans Selye', 'Martin Seligman'],
            'Engel argued that the biomedical model was too narrow.'),
           ('Which is the best example of a social factor in the biopsychosocial model?', 'Lack of social support', ['A genetic predisposition', 'High cortisol levels', 'Negative thinking patterns'],
            'Social support is part of the social environment.'),
           ('According to the WHO\'s 1948 definition, health is:', 'A state of complete physical, mental and social well-being, not merely the absence of disease', ['The absence of any diagnosed disease', 'Physical fitness and a healthy weight', 'Living to an old age'],
            'The WHO definition is holistic.')],
    why=[('Explain why the biopsychosocial model is more useful than the biomedical model for understanding health.', 'Many health problems (e.g. depression, heart disease) are influenced by stress, cognition, behaviour and social conditions as well as biology, so a model including all three explains variation and suggests a wider range of interventions.'),
         ('Explain why definitions of well-being vary across cultures.', 'Individualist cultures emphasise personal happiness and achievement, while collectivist cultures emphasise harmony and social roles; measures developed in one culture may not capture well-being in another.')],
    contrast=[('the biomedical model', 'the biopsychosocial model', 'The biomedical model explains illness by biological causes only and treats it medically; the biopsychosocial model sees illness as the interaction of biological, psychological and social factors and supports combined interventions.')],
    misc=[('The biopsychosocial model gives equal weight to each factor for every illness.', 'The model says all three levels may contribute, but their relative importance differs between people and conditions.')],
    cases=[('type 2 diabetes in a city office worker', 'Rafael, 45, in Mexico City, develops type 2 diabetes. He has a family history of diabetes, works long hours, eats fast food and feels too stressed to exercise.', 'the biopsychosocial model', 'biological (genetics, insulin resistance), psychological (stress, low self-efficacy for exercise) and social (work culture, food environment) factors interact, so treatment should address all three')],
    apply=[('A school counsellor in Hanoi wants to promote students\' well-being. Using the biopsychosocial model, suggest one strategy at each level.', 'Biological: promote sleep and exercise; psychological: teach coping and cognitive reframing; social: peer support, reduced exam pressure and family involvement.', 3)],
    evaluate=[('The biopsychosocial model is the best way to understand health and illness.', ['holistic; explains individual variation', 'supported by research on stress and immunity (Kiecolt-Glaser et al., 1984)'],
               ['too general; hard to test as a whole', 'does not specify how factors interact or which matters most', 'may dilute focus on effective biological treatments'],
               'It is the most comprehensive framework, but it must be made specific to be testable and useful.')],
))
K.study('ch09-st1', 'Engel', 1977, 'the need for a new medical model', 'to argue for a model of illness that includes psychological and social factors',
        'Engel wrote a theoretical article in Science, using clinical examples (e.g. diabetes and schizophrenia) to show the limitations of the biomedical model.',
        'he proposed the biopsychosocial model, in which illness and health result from interactions between biological, psychological and social systems',
        'holistic explanations of health and illness',
        ['influential in medicine and psychology; encouraged holistic care'],
        ['theoretical - not an empirical study', 'vague about how factors interact'],
        mtype=None)

K.facts('ch09-st2', F(
    terms=[('stress', 'a state of physiological and psychological arousal that occurs when a person perceives that the demands of a situation exceed their resources to cope'),
           ('major depressive disorder', 'a mental disorder involving persistent low mood or loss of interest for at least two weeks, with symptoms such as sleep and appetite change, fatigue and feelings of worthlessness (DSM-5)'),
           ('cognitive vulnerability', 'a pattern of negative thinking (e.g. negative attributional style) that increases the risk of depression when stressful events occur'),
           ('negative cognitive triad', 'Beck\'s idea that depressed people hold negative views of the self, the world and the future'),
           ('immunosuppression', 'the reduction of immune function, for example by prolonged cortisol release during stress'),
           ('vulnerability factor', 'a factor that increases the risk of a disorder when combined with a stressor, such as lack of an intimate relationship (Brown and Harris, 1978)')],
    facts=[('Kiecolt-Glaser et al. (1984) found that during exams, medical students showed reduced:', 'Natural killer cell activity', ['Cortisol levels', 'Heart rate', 'Memory for exam material'],
            'Immune function fell during the stressful exam period compared with one month before.'),
           ('Brown and Harris (1978) identified vulnerability factors for depression in women in Camberwell, London. Which was one of them?', 'Lack of an intimate, confiding relationship', ['Having a part-time job', 'Living in the countryside', 'Having one child under 14'],
            'Others: three or more children under 14 at home, loss of mother before age 11, no employment outside the home.'),
           ('In the Temple-Wisconsin Cognitive Vulnerability to Depression project, which students were more likely to develop first-onset depression?', 'Those with negative cognitive styles', ['Those with positive cognitive styles', 'Those with high IQ', 'Those who exercised regularly'],
            'About 17% of high-risk vs 1% of low-risk students developed a first episode of major depression (Alloy et al.).')],
    why=[('Explain how stress can affect the immune system.', 'Stress activates the HPA axis, releasing cortisol, which over long periods suppresses immune function (e.g. fewer natural killer cells), increasing vulnerability to illness (Kiecolt-Glaser et al., 1984).'),
         ('Explain how cognitive factors can contribute to depression.', 'Negative schemas and attributional styles (Beck\'s triad; hopelessness) make people interpret events as personal, permanent and pervasive failures, which maintains low mood when stressful events occur (Alloy et al., 1999).'),
         ('Explain how sociocultural factors can contribute to depression.', 'Social disadvantage, lack of support and stressful life events increase risk (Brown and Harris, 1978), and culture shapes how distress is expressed, perceived and treated.')],
    contrast=[('a biological explanation of depression', 'a cognitive explanation of depression', 'Biological explanations focus on genes (heritability ~38%, Kendler et al., 2006) and neurotransmitters such as serotonin; cognitive explanations focus on negative thought patterns and attributional styles.')],
    misc=[('Depression is caused by a chemical imbalance of serotonin.', 'The serotonin hypothesis is oversimplified; a 2022 umbrella review (Moncrieff et al.) found no consistent evidence of low serotonin in depression, and multiple biological, cognitive and social factors interact.')],
    cases=[('a carer under chronic stress', 'Mei, 52, in Singapore, cares full-time for her mother with dementia. She sleeps poorly, catches frequent infections and feels hopeless.', 'factors in stress and health', 'chronic stress raises cortisol and suppresses immunity (biological); hopeless appraisal (cognitive) and isolation (social) interact to increase illness and depression risk')],
    apply=[('Using the diathesis-stress model, explain why only some students who experience exam failure develop depression.', 'Students with a vulnerability (genetic, e.g. family history; cognitive, e.g. negative attributional style - Alloy et al.) are more likely to become depressed when a stressor such as exam failure occurs; social support may buffer the effect.', 4)],
    evaluate=[('Depression is best explained by cognitive factors.', ['negative cognitive style predicts onset (Alloy et al., 1999)', 'CBT is effective'],
               ['heritability ~38% (Kendler et al., 2006)', 'social factors such as poverty and loss (Brown and Harris, 1978)', 'negative thinking may be a symptom rather than a cause'],
               'Cognitive factors are important, especially as vulnerability, but depression is best explained by interacting biological, cognitive and social factors.')],
))
K.study('ch09-st2', 'Kiecolt-Glaser et al.', 1984, 'exam stress and the immune system', 'to investigate whether the stress of exams affects immune function',
        'Blood samples were taken from 75 medical students one month before final exams and on the first day of exams; questionnaires measured stress and loneliness.',
        'natural killer cell activity was lower during the exam period; it was lowest in students who reported high loneliness and stressful life events',
        'the effect of stress on health',
        ['natural stressor with objective immune measures', 'repeated measures controls participant variables'],
        ['correlational; other factors such as sleep and caffeine during exams', 'medical students only'],
        mtype='natural experiment', wrong=['Natural killer cell activity increased during exams', 'Loneliness had no relationship with immune function', 'Immune function was lowest one month before exams'])
K.study('ch09-st2', 'Brown and Harris', 1978, 'the social origins of depression', 'to investigate social factors associated with depression in women',
        'Interviews with 458 women in Camberwell, London, about life events, difficulties and depression over the previous year.',
        'severe life events and difficulties triggered depression, especially in women with vulnerability factors such as lack of an intimate relationship or three or more children under 14 at home',
        'sociocultural factors in depression',
        ['in-depth interviews in a community sample', 'introduced the idea of vulnerability factors'],
        ['correlational and retrospective', 'women only, in one area of London in the 1970s'],
        mtype='semi-structured interview')
K.study('ch09-st2', 'Alloy et al.', 1999, 'cognitive vulnerability to depression', 'to test whether negative cognitive styles predict the onset of depression',
        'In the Temple-Wisconsin project, non-depressed first-year students were classified as high or low risk based on cognitive style and followed for about 2.5 years with repeated assessments.',
        'high-risk students were much more likely to develop major depression (about 17% vs 1% for first onset)',
        'cognitive vulnerability as a cause of depression',
        ['prospective longitudinal design shows temporal order', 'participants were not depressed at the start'],
        ['university students only', 'cognitive style is not manipulated - third variables possible'],
        mtype='longitudinal study')

K.facts('ch09-st3', F(
    terms=[('cognitive behavioural therapy (CBT)', 'a structured psychological treatment that helps people identify and change dysfunctional thoughts and behaviours'),
           ('selective serotonin reuptake inhibitor (SSRI)', 'an antidepressant that blocks the reuptake of serotonin, increasing its availability in the synapse'),
           ('placebo effect', 'improvement in symptoms due to the expectation of treatment rather than the active treatment itself'),
           ('randomised controlled trial (RCT)', 'an experiment in which participants are randomly allocated to treatment or control groups to test effectiveness'),
           ('relapse', 'the return of symptoms after a period of improvement'),
           ('meta-analysis', 'a statistical technique that combines the results of many studies to estimate an overall effect')],
    facts=[('Kirsch et al. (2008) analysed trial data submitted to the US Food and Drug Administration and found that antidepressants:', 'Were only clearly more effective than placebo for the most severely depressed', ['Were much more effective than placebo for all patients', 'Were less effective than placebo', 'Had no side effects'],
            'The drug-placebo difference was small for mild and moderate depression.'),
           ('In the NIMH Treatment of Depression Collaborative Research Program (Elkin et al., 1989), which treatment produced the fastest improvement?', 'Imipramine plus clinical management', ['Placebo plus clinical management', 'Psychoanalysis', 'Exercise therapy'],
            'CBT and interpersonal therapy were also effective, especially for less severe depression.'),
           ('DeRubeis et al. (2005) found that for moderate-to-severe depression, cognitive therapy was:', 'As effective as antidepressant medication at 16 weeks', ['Much less effective than medication', 'No better than placebo', 'Only effective in combination with medication'],
            'About 58% responded to both treatments; cognitive therapy also had lower relapse after treatment ended.')],
    why=[('Explain how SSRIs are thought to reduce symptoms of depression.', 'They block the reuptake of serotonin into the presynaptic neuron, increasing its availability in the synapse; over weeks this may change receptor sensitivity and neuroplasticity, although the exact mechanism is debated.'),
         ('Explain why placebo control groups are important in evaluating treatments.', 'Patients may improve because they expect to (placebo effect) or because depression often improves over time; comparing with a placebo shows whether the active treatment adds anything.'),
         ('Explain why CBT may have lower relapse rates than drug treatment.', 'CBT teaches skills (challenging negative thoughts, behavioural activation) that people continue to use after therapy ends, whereas the effect of drugs may stop when they are discontinued.')],
    contrast=[('biological treatments', 'psychological treatments', 'Biological treatments (e.g. SSRIs) change brain chemistry and work relatively quickly with less effort from patients but have side effects; psychological treatments (e.g. CBT) change thoughts and behaviour, require engagement and may prevent relapse.')],
    misc=[('If a drug works, depression must be caused by the chemical it targets.', 'This is the treatment aetiology fallacy - aspirin relieves headaches but headaches are not caused by a lack of aspirin.')],
    cases=[('a patient deciding between treatments', 'Tomás, 34, in Lisbon, has moderate depression. His doctor offers sertraline (an SSRI) or 16 sessions of CBT.', 'treatment effectiveness', 'research suggests both are similarly effective for moderate depression (DeRubeis et al., 2005); CBT has lower relapse but needs effort and access, while SSRIs act on serotonin but have side effects')],
    apply=[('A health service in Accra has limited funding for depression treatment. Using research, recommend an approach and justify it.', 'E.g. stepped care: guided self-help or group CBT delivered by trained lay counsellors for mild-moderate depression, with medication for severe cases; justify with effectiveness (Kirsch et al., 2008; DeRubeis et al., 2005), cost and cultural acceptability (e.g. Friendship Bench in Zimbabwe).', 4)],
    evaluate=[('Psychological therapies are more effective than biological treatments for depression.', ['CBT equals medication and reduces relapse (DeRubeis et al., 2005)', 'drug-placebo differences small for mild depression (Kirsch et al., 2008)'],
               ['medication works faster for severe depression (Elkin et al., 1989)', 'therapy needs trained therapists and access', 'combined treatment often best'],
               'Neither is universally superior; effectiveness depends on severity, patient preference and context, and combined treatment is often most effective.')],
))
K.study('ch09-st3', 'Kirsch et al.', 2008, 'antidepressants versus placebo', 'to evaluate how effective antidepressants are compared with placebo, using all clinical trial data submitted to the FDA',
        'A meta-analysis of 35 trials of four antidepressants (fluoxetine, venlafaxine, nefazodone, paroxetine), including unpublished data.',
        'the difference between drug and placebo was small and below the threshold for clinical significance except in the most severely depressed patients',
        'the effectiveness of biological treatments for depression',
        ['included unpublished trials - reduces publication bias', 'large combined sample'],
        ['short trials (6-8 weeks)', 'relied on one rating scale (Hamilton)', 'later meta-analyses (Cipriani et al., 2018) found all 21 antidepressants more effective than placebo'],
        mtype='meta-analysis', wrong=['Antidepressants were far more effective than placebo for mild depression', 'Placebo was more effective than antidepressants for severe depression', 'Only published trials were analysed'])
K.study('ch09-st3', 'Elkin et al.', 1989, 'the NIMH treatment of depression trial', 'to compare the effectiveness of psychological and drug treatments for depression',
        '250 outpatients with major depression were randomly assigned to 16 weeks of CBT, interpersonal therapy, imipramine plus clinical management, or placebo plus clinical management at three US sites.',
        'all groups improved; imipramine worked fastest and was most effective for severe depression; the psychotherapies were similar to imipramine for less severe depression',
        'the relative effectiveness of biological and psychological treatments',
        ['randomised, multi-site, with a placebo control', 'standardised treatment manuals'],
        ['therapist differences between sites', 'placebo group still received clinical management', 'short follow-up'],
        mtype='randomised controlled trial')
K.study('ch09-st3', 'DeRubeis et al.', 2005, 'cognitive therapy versus medication', 'to compare cognitive therapy with antidepressant medication for moderate to severe depression',
        '240 patients were randomly assigned to cognitive therapy, paroxetine or placebo (placebo for 8 weeks only) and assessed over 16 weeks.',
        'at 16 weeks about 58% responded to both cognitive therapy and medication; at 8 weeks both outperformed placebo',
        'the effectiveness of psychological treatment for depression',
        ['randomised controlled trial with experienced therapists'],
        ['effectiveness varied by site (therapist experience)', 'placebo only for 8 weeks'],
        mtype='randomised controlled trial')

K.facts('ch09-st4', F(
    terms=[('health promotion', 'the process of enabling people to increase control over and improve their health (WHO Ottawa Charter, 1986)'),
           ('fear appeal', 'a persuasive message that aims to change behaviour by arousing fear about the consequences of not doing so'),
           ('health belief model', 'a model that health behaviour depends on perceived susceptibility, severity, benefits, barriers, cues to action and self-efficacy'),
           ('social marketing', 'the use of marketing techniques to promote socially beneficial behaviour'),
           ('primary prevention', 'interventions that aim to prevent a health problem from developing'),
           ('outcome evaluation', 'assessing whether a health campaign achieved its intended changes in behaviour or health')],
    facts=[('Farrelly et al. (2005) estimated that the US "truth" anti-smoking campaign accounted for about what share of the decline in youth smoking between 2000 and 2002?', 'About 22%', ['About 2%', 'About 50%', 'About 90%'],
            'Around 300,000 fewer young smokers were attributed to the campaign.'),
           ('Anderson (2010) evaluated the Montana Meth Project\'s graphic advertising and found:', 'No significant effect on methamphetamine use once trends were considered', ['A 90% reduction in meth use', 'Increased meth use', 'Large effects in all age groups'],
            'Declines also occurred in other states without the campaign.'),
           ('Which is a cue to action in the health belief model?', 'A reminder text message to attend a vaccination', ['Believing the disease is serious', 'High self-efficacy', 'Cost of the vaccine'],
            'Cues to action trigger the behaviour.')],
    why=[('Explain why fear appeals in health campaigns can be ineffective.', 'If fear is high but people feel unable to change (low self-efficacy), they may respond defensively (denial, avoidance) rather than changing behaviour; fear works best combined with clear, achievable actions.'),
         ('Explain why evaluating a health campaign is difficult.', 'Behaviour may change for other reasons (trends, laws, prices), there is rarely a randomised control group, and outcomes are often self-reported.')],
    contrast=[('a fear appeal', 'a social norms campaign', 'A fear appeal tries to change behaviour by emphasising threats; a social norms campaign corrects misperceptions of how common a behaviour is (e.g. "most students drink less than you think").')],
    misc=[('Showing shocking images is the most effective way to change health behaviour.', 'Fear appeals can backfire without efficacy messages; campaigns such as "truth" succeeded by changing social norms and image rather than fear alone.')],
    cases=[('Australia\'s "Slip, Slop, Slap" sun-safety campaign', 'From 1981, Australian campaigns urged people to slip on a shirt, slop on sunscreen and slap on a hat, using a cartoon seagull and later school programmes.', 'health promotion', 'a simple, memorable message, environmental changes (shade, school policies) and sustained campaigns contributed to changed behaviour and lower skin cancer rates in younger cohorts')],
    apply=[('Design a campaign to reduce vaping among 14-17-year-olds in Toronto. Using one model of health behaviour, justify two features.', 'Health belief model: increase perceived susceptibility and severity with relatable information, reduce barriers (quit support), cues to action (social media prompts), build self-efficacy; or social norms: show most teens do not vape; evaluate with pre/post surveys and a comparison city.', 4)],
    evaluate=[('Health promotion campaigns are effective in changing behaviour.', ['"truth" campaign (Farrelly et al., 2005)', 'Slip, Slop, Slap and skin cancer'],
               ['Montana Meth Project showed no effect (Anderson, 2010)', 'effects are small and hard to isolate', 'self-report outcomes'],
               'Some campaigns work, especially those based on theory, sustained over time and combined with policy; many have weak or no effects.')],
))
K.study('ch09-st4', 'Farrelly et al.', 2005, 'the "truth" anti-smoking campaign', 'to evaluate the effect of the national "truth" anti-smoking campaign on youth smoking in the USA',
        'Survey data on smoking among US secondary school students (1997-2002) were analysed in relation to the amount of "truth" advertising each media market received, controlling for other influences.',
        'greater exposure was associated with lower youth smoking; the campaign was estimated to account for about 22% of the decline (about 300,000 fewer youth smokers)',
        'the evaluation of a health promotion campaign',
        ['large national data set', 'dose-response analysis'],
        ['correlational; other factors (tax, laws) may confound', 'self-reported smoking'],
        mtype='correlational study')
K.study('ch09-st4', 'Anderson', 2010, 'the Montana Meth Project', 'to evaluate whether the Montana Meth Project\'s graphic advertising campaign reduced methamphetamine use among teenagers',
        'Youth Risk Behavior Survey data from Montana were compared with national trends and other states before and after the campaign began in 2005.',
        'after accounting for a national downward trend in meth use, there was no significant effect of the campaign on teen meth use',
        'the limits of fear-based health campaigns',
        ['used comparison states to control for trends'],
        ['self-reported drug use', 'cannot measure all exposure'],
        mtype='natural experiment')
K.study('ch09-st1', 'Kahneman and Deaton', 2010, 'income and well-being', 'to investigate whether higher income is associated with greater emotional well-being and life evaluation',
        'Analysis of over 450,000 responses to the Gallup-Healthways Well-Being Index from US residents in 2008-2009, measuring income, daily emotional experience and life evaluation (Cantril ladder).',
        'life evaluation rose steadily with log income, but emotional well-being rose with income only up to about $75,000 a year and then levelled off',
        'the distinction between emotional well-being and life evaluation',
        ['very large, representative sample', 'distinguished two components of well-being'],
        ['correlational; self-report', 'US data only; a later study (Killingsworth et al., 2023) found that for most people happiness kept rising above $75,000'],
        mtype='correlational study')
K.R.f['ch09-st1'].cases += [
    ('a refugee adolescent in a camp', 'Zara, 15, lives in a refugee camp in Jordan. She has recurring headaches and nightmares, lost her father in the conflict and has no school place.', 'the biopsychosocial model', 'physical symptoms (biological), trauma-related memories and hopelessness (psychological) and loss, poverty and lack of education (social) interact, so care should include medical, psychological and social support'),
    ('a heart-attack patient\'s recovery', 'After a heart attack, Lars in Oslo receives medication, attends a cardiac rehabilitation group and is helped to cut down his working hours.', 'holistic treatment based on the biopsychosocial model', 'treatment targets biological (medication), psychological (stress management, beliefs about recovery) and social (support group, work demands) factors, which together predict recovery better than medication alone')]
K.R.f['ch09-st1'].apply += [
    ('A survey in Seoul finds that people who report more close friendships report higher life satisfaction. Using the biopsychosocial model, suggest two explanations for this relationship and one reason for caution.', 'Social support may buffer stress (lower cortisol - biological) and promote positive appraisals and self-esteem (psychological); caution: the data are correlational - happier people may find it easier to make friends, and self-report may be biased.', 4),
    ('Explain how a psychological factor and a social factor could interact to affect recovery from a sports injury.', 'Low self-efficacy and catastrophising (psychological) may reduce adherence to physiotherapy, and this is worsened if the athlete loses the social support of the team (social); supportive team contact can raise self-efficacy and adherence.', 3)]

# ---------------------------------------------------------------------------------------------
# ch10 Context: human development
# ---------------------------------------------------------------------------------------------
K.facts('ch10-st1', F(
    terms=[('prefrontal cortex', 'the front part of the frontal lobe, involved in planning, impulse control and decision-making; one of the last areas to mature'),
           ('myelination', 'the formation of a fatty myelin sheath around axons, which speeds up neural transmission and increases with age into the twenties'),
           ('grey matter', 'brain tissue made up mainly of neuron cell bodies and synapses'),
           ('white matter', 'brain tissue made up mainly of myelinated axons that connect brain regions'),
           ('dual systems model', 'Steinberg\'s model that adolescent risk-taking results from an early-maturing reward system and a later-maturing cognitive control system'),
           ('sensitive period', 'a period in development during which the brain is especially responsive to particular experiences')],
    facts=[('Giedd et al. (1999) found that grey matter in the frontal lobes:', 'Increased until around puberty and then declined', ['Decreased steadily from birth', 'Remained constant throughout adolescence', 'Only increased after age 25'],
            'Frontal grey matter peaked at about 11 in girls and 12 in boys, consistent with synaptic pruning afterwards.'),
           ('Gogtay et al. (2004) found that grey matter matures in which order?', 'From back to front, with the prefrontal cortex last', ['From front to back', 'All regions at the same time', 'Left hemisphere before right'],
            'Higher-order association areas mature after primary sensory and motor areas.'),
           ('Gardner and Steinberg (2005) found that peers increased risk-taking in a driving game most for:', 'Adolescents (13-16)', ['Adults (24 and over)', 'Young adults (18-22)', 'Children under 10'],
            'Peer presence doubled risk-taking in adolescents but had little effect on adults.')],
    why=[('Explain how brain development may contribute to risk-taking in adolescence.', 'The limbic reward system (e.g. ventral striatum) becomes highly sensitive at puberty while the prefrontal cortex, which supports impulse control, matures more slowly into the mid-twenties, creating an imbalance - especially in the presence of peers.'),
         ('Explain why synaptic pruning is important for brain development.', 'Unused synapses are eliminated and used ones strengthened, making neural networks more efficient; this "use it or lose it" process shapes the brain to the individual\'s environment.')],
    contrast=[('grey matter development', 'white matter development', 'Grey matter increases in childhood and then decreases through pruning in adolescence, while white matter increases steadily through myelination into adulthood.')],
    misc=[('The adolescent brain is simply an immature adult brain.', 'Adolescence is a distinct period of reorganisation with heightened reward sensitivity and plasticity, which supports learning and social development as well as risk.')],
    cases=[('teenage drivers and passengers', 'Many countries, including Australia and parts of the USA, restrict the number of peer passengers for newly licensed teenage drivers.', 'adolescent brain development', 'peer presence activates the reward system in adolescents and increases risk-taking (Gardner and Steinberg, 2005), so restrictions reduce accidents while the prefrontal cortex is still maturing')],
    apply=[('A school in Lima is debating starting lessons later for adolescents. Using research on brain development, explain one argument for this change.', 'Adolescents experience a biological shift in circadian rhythm (later melatonin release), so early starts cause sleep deprivation, which impairs prefrontal functions such as attention and memory consolidation during a period of brain reorganisation.', 3)],
    evaluate=[('Adolescent behaviour can be explained by brain development.', ['grey matter pruning and late PFC maturation (Giedd et al., 1999; Gogtay et al., 2004)', 'peer effects on risk (Gardner and Steinberg, 2005)'],
               ['cultural variation in adolescent risk-taking', 'correlational imaging data', 'social context and parenting matter'],
               'Brain development contributes to adolescent behaviour but interacts with social and cultural context; it is not a complete explanation.')],
))
K.study('ch10-st1', 'Giedd et al.', 1999, 'brain development in childhood and adolescence', 'to map changes in grey and white matter from childhood to adulthood',
        'A longitudinal MRI study of 145 healthy children and adolescents (aged about 4-22) in the USA, scanned up to five times at two-year intervals.',
        'white matter increased steadily, while grey matter in the frontal and parietal lobes increased until around 11-12 years and then declined',
        'brain maturation and synaptic pruning in adolescence',
        ['longitudinal design tracks change within individuals', 'objective MRI data'],
        ['does not link changes directly to behaviour', 'mostly US sample'],
        mtype='longitudinal study', wrong=['Grey matter increased steadily throughout adolescence', 'White matter decreased from childhood to adulthood', 'There was no change in grey matter after age 5'])
K.study('ch10-st1', 'Gardner and Steinberg', 2005, 'peer influence on risk-taking', 'to investigate whether the presence of peers increases risk-taking more in adolescents than in adults',
        '306 participants in three age groups (13-16, 18-22, 24 and over) played a video driving game ("Chicken") alone or with two friends present, and completed risk questionnaires.',
        'peers doubled risky driving in adolescents, increased it by about half in young adults and had no significant effect in adults',
        'the role of peers and the developing brain in adolescent risk-taking',
        ['controlled task; comparison across age groups'],
        ['video game lacks real consequences', 'friends chose to come - not random', 'US sample'],
        mtype='laboratory experiment', iv='age group and presence of peers', dv='risk-taking score in the driving game')
K.study('ch10-st1', 'Gogtay et al.', 2004, 'the sequence of cortical maturation', 'to map the sequence in which grey matter matures across the cortex',
        '13 healthy children were scanned with MRI every two years for 8-10 years, starting at age 4-8, and cortical grey matter density was mapped over time.',
        'grey matter loss proceeded from back to front: sensory and motor areas matured first and the prefrontal cortex last',
        'the late maturation of the prefrontal cortex',
        ['longitudinal; detailed maps'],
        ['very small sample', 'correlation with behaviour not tested'],
        mtype='longitudinal study')

K.facts('ch10-st2', F(
    terms=[('schema (Piaget)', 'an organised mental structure that represents some aspect of the world and is developed through experience'),
           ('assimilation', 'incorporating new information into an existing schema'),
           ('accommodation', 'changing an existing schema, or creating a new one, to fit new information'),
           ('equilibration', 'the process of restoring balance between existing schemas and new experiences, which drives cognitive development'),
           ('conservation', 'understanding that quantity stays the same despite changes in appearance, achieved in the concrete operational stage'),
           ('object permanence', 'understanding that objects continue to exist when they cannot be seen'),
           ('zone of proximal development (ZPD)', 'the gap between what a child can do alone and what they can do with guidance from a more knowledgeable other'),
           ('scaffolding', 'temporary, adjustable support given by a more knowledgeable other to help a learner within the ZPD')],
    facts=[('In which of Piaget\'s stages do children typically first succeed on conservation tasks?', 'Concrete operational (about 7-11 years)', ['Sensorimotor (0-2 years)', 'Preoperational (2-7 years)', 'Formal operational (11+ years)'],
            'Preoperational children focus on one dimension (centration).'),
           ('McGarrigle and Donaldson (1974) found that when a "naughty teddy" rearranged counters, the proportion of 4-6-year-olds who conserved number:', 'Increased to about 62%', ['Fell to about 5%', 'Stayed the same as when the adult rearranged them', 'Reached 100%'],
            'Only 16% conserved when the experimenter rearranged the counters.'),
           ('Baillargeon and DeVos (1991) found that infants of about 3.5 months:', 'Looked longer at an "impossible" event, suggesting object permanence', ['Showed no object permanence until 8 months', 'Could not see the carrots', 'Cried when objects disappeared'],
            'This suggests Piaget underestimated infants.'),
           ('Who proposed the zone of proximal development?', 'Lev Vygotsky', ['Jean Piaget', 'Jerome Bruner', 'John Bowlby'],
            'Vygotsky emphasised social interaction and language in development.')],
    why=[('Explain how equilibration drives cognitive development in Piaget\'s theory.', 'When new experiences do not fit existing schemas, the child experiences disequilibrium; accommodation of schemas restores equilibrium, producing more complex understanding.'),
         ('Explain why Vygotsky emphasised social interaction in cognitive development.', 'He believed higher mental functions develop first between people (intermental) and are then internalised (intramental), through language and guidance from more knowledgeable others in the ZPD; culture provides the tools of thinking.')],
    contrast=[('Piaget\'s theory', 'Vygotsky\'s theory', 'Piaget saw the child as an independent "scientist" developing through universal stages driven by maturation and discovery; Vygotsky saw development as social and cultural, driven by interaction and language within the ZPD.'),
              ('assimilation', 'accommodation', 'Assimilation fits new information into an existing schema (calling a zebra a "horse"); accommodation changes the schema to fit new information (creating a "zebra" schema).')],
    misc=[('Piaget showed that young children are incapable of logical thought.', 'Later research (McGarrigle and Donaldson, 1974; Baillargeon and DeVos, 1991) suggests Piaget underestimated young children because his tasks were confusing or relied on verbal answers.')],
    cases=[('a child learning to use chopsticks', 'Aiko, 4, in Osaka, cannot use chopsticks alone; her grandmother first holds her fingers, then gives verbal hints, then just watches as Aiko manages alone.', 'scaffolding in the zone of proximal development', 'support is adjusted to Aiko\'s level and gradually withdrawn as competence grows, showing learning within the ZPD')],
    apply=[('A teacher in Nairobi notices that 5-year-olds think a tall, thin glass holds more juice than a short, wide one. Using Piaget\'s theory, explain this and suggest how the teacher could help.', 'Preoperational children show centration (focusing on height) and lack reversibility, so they fail conservation; hands-on pouring activities create disequilibrium and support accommodation; Vygotskian guided questioning can also help.', 4)],
    evaluate=[('Piaget\'s theory provides an accurate account of cognitive development.', ['conservation and stages widely replicated in Western samples', 'influential in education (discovery learning)'],
               ['underestimated children (McGarrigle and Donaldson, 1974; Baillargeon and DeVos, 1991)', 'underestimated social and cultural influences (Vygotsky)', 'stages are less fixed than proposed'],
               'Piaget described major changes in thinking but underestimated young children and the role of culture and social interaction.')],
))
K.study('ch10-st2', 'Piaget', 1952, 'conservation of number in young children', 'to investigate when children understand that number stays the same despite changes in arrangement',
        'Children were shown two equal rows of counters and asked if they were the same; one row was then spread out while they watched, and the question was repeated.',
        'children in the preoperational stage (under about 7) typically said the longer row had more counters, failing to conserve',
        'stages of cognitive development',
        ['simple, replicable tasks', 'influential theory of stages'],
        ['asking the question twice may suggest the answer should change (McGarrigle and Donaldson, 1974)', 'small samples, often Piaget\'s own children'],
        mtype=None)
K.study('ch10-st2', 'McGarrigle and Donaldson', 1974, 'the "naughty teddy" conservation study', 'to test whether children\'s failure on conservation tasks was due to the way the task was presented',
        '80 Scottish children aged 4-6 did number conservation tasks in which either the experimenter deliberately rearranged the counters or a "naughty teddy" messed them up "accidentally".',
        'about 62% conserved number in the naughty teddy condition compared with 16% when the experimenter changed the row',
        'whether Piaget underestimated children\'s abilities',
        ['repeated measures controls participant variables', 'challenged Piaget\'s methodology'],
        ['teddy may have distracted children so they did not notice the change', 'one cultural group'],
        mtype='laboratory experiment', iv='who changed the row (naughty teddy vs experimenter)', dv='percentage of children who correctly said the number was the same',
        wrong=['Fewer children conserved in the naughty teddy condition', 'All children conserved regardless of condition', 'Only children over 7 conserved'])
K.study('ch10-st2', 'Baillargeon and DeVos', 1991, 'object permanence in young infants', 'to investigate whether infants younger than Piaget proposed understand object permanence',
        'Infants aged about 3.5 months watched a short or tall carrot pass behind a screen with a window; in the impossible event the tall carrot did not appear in the window. Looking time was measured.',
        'infants looked longer at the impossible event, suggesting they expected the tall carrot to remain visible and understood it continued to exist behind the screen',
        'early object permanence in infancy',
        ['looking-time method avoids the motor demands of Piaget\'s search tasks'],
        ['looking time may reflect novelty or perceptual differences rather than understanding', 'small sample'],
        mtype='laboratory experiment')
K.study('ch10-st2', 'Wood, Bruner and Ross', 1976, 'tutoring and scaffolding', 'to investigate how adults tutor young children in a problem-solving task',
        'A tutor helped 30 children aged 3, 4 and 5 to build a pyramid from interlocking blocks; her interventions were recorded and analysed.',
        'effective tutoring was contingent: the tutor gave more help when the child struggled and less as the child succeeded; the term "scaffolding" was introduced',
        'scaffolding in the zone of proximal development',
        ['detailed observation of tutor-child interaction', 'practical application in teaching'],
        ['one tutor and a single task', 'small sample'],
        mtype='controlled observation')

K.facts('ch10-st3', F(
    terms=[('attachment', 'a strong, enduring emotional bond between an infant and a caregiver that provides security'),
           ('monotropy', 'Bowlby\'s idea that infants form one primary attachment that is more important than all others'),
           ('internal working model', 'a mental representation of relationships based on the early attachment, which guides later relationships'),
           ('Strange Situation', 'Ainsworth\'s standardised procedure of eight short episodes used to classify infants\' attachment type'),
           ('secure attachment (type B)', 'an attachment type in which the infant is distressed when the caregiver leaves, easily comforted on reunion and uses the caregiver as a secure base'),
           ('insecure-avoidant attachment (type A)', 'an attachment type in which the infant shows little distress at separation and avoids the caregiver on reunion'),
           ('insecure-resistant attachment (type C)', 'an attachment type in which the infant is very distressed at separation and both seeks and resists contact on reunion'),
           ('critical period', 'Bowlby\'s proposed period (about the first 2.5 years) during which an attachment must form for normal development')],
    facts=[('In Ainsworth\'s Baltimore sample, roughly what percentage of infants were classified as securely attached?', 'About 70%', ['About 15%', 'About 40%', 'About 95%'],
            'Approximately 70% B, 15% A and 15% C.'),
           ('Van IJzendoorn and Kroonenberg (1988) found that insecure-resistant attachment was relatively common in:', 'Israel and Japan', ['Germany and the USA', 'Great Britain and Sweden', 'The Netherlands and the USA'],
            'Avoidant attachment was relatively common in West Germany.'),
           ('Harlow (1958) found that infant rhesus monkeys spent most time with:', 'A cloth-covered surrogate mother, even when the wire mother gave milk', ['The wire mother that gave milk', 'Other infant monkeys only', 'No surrogate at all'],
            'Contact comfort was more important than food.'),
           ('In Bowlby\'s (1944) "44 thieves" study, how many of the 14 "affectionless psychopaths" had experienced early prolonged maternal separation?', '12', ['2', '5', '14'],
            'Only 2 of the 44 controls had experienced such separation.')],
    why=[('Explain how an internal working model may affect later relationships.', 'Early experiences with a responsive (or unresponsive) caregiver create expectations about oneself and others; these guide behaviour in later relationships, e.g. securely attached children expect support and trust others.'),
         ('Explain why the Strange Situation may not be valid across cultures.', 'It was developed in the USA and assumes that distress and reunion behaviours mean the same everywhere; in Japan, infants are rarely separated from mothers, so high distress may reflect unfamiliarity rather than insecurity (imposed etic).')],
    contrast=[('secure attachment', 'insecure-avoidant attachment', 'Securely attached infants are distressed by separation, seek comfort on reunion and explore using the caregiver as a base; avoidant infants show little distress and ignore or avoid the caregiver on reunion.')],
    misc=[('Bowlby showed that maternal separation causes delinquency.', 'The 44 thieves study was retrospective and correlational, relied on Bowlby\'s own interviews and diagnoses, and could not establish causation.'),
          ('Attachment type is fixed for life.', 'Attachment can change with circumstances (e.g. family stress or improved caregiving), and it is better seen as a relationship pattern than a fixed trait.')],
    cases=[('children in Romanian orphanages', 'After 1989 many children from severely deprived Romanian orphanages were adopted into UK families (Rutter et al.); those adopted after 6 months showed more disinhibited attachment.', 'the effects of early deprivation on attachment', 'late adoption after severe deprivation was associated with lasting attachment difficulties, partially supporting a sensitive period')],
    apply=[('A nursery in Vienna is designing its settling-in policy for 1-year-olds. Using attachment research, recommend two features.', 'A key-worker system so each infant can form a secondary attachment; gradual separations with the parent present at first; consistency of carers; sensitivity to cultural differences in separation.', 4)],
    evaluate=[('Attachment patterns are universal across cultures.', ['secure attachment most common in all countries (Van IJzendoorn and Kroonenberg, 1988)', 'Harlow: biological basis of contact comfort'],
               ['different distributions of insecure types across cultures', 'variation within cultures 1.5 times greater than between', 'Strange Situation may be an imposed etic'],
               'The tendency to form attachments appears universal, but how attachment is expressed and measured is culturally shaped.')],
))
K.study('ch10-st3', 'Ainsworth and Bell', 1970, 'the Strange Situation', 'to investigate individual differences in attachment between infants and their mothers',
        'Infants aged 12-18 months from middle-class families in Baltimore were observed through a one-way mirror during eight 3-minute episodes involving mother, a stranger, separations and reunions; behaviour was coded.',
        'three attachment types were identified: secure (about 70%), insecure-avoidant (about 15%) and insecure-resistant (about 15%)',
        'individual differences in attachment',
        ['standardised, replicable procedure with good inter-rater reliability', 'controlled observation'],
        ['US middle-class sample - imposed etic', 'artificial setting', 'mild distress to infants'],
        mtype='controlled observation', ethics='Infants were deliberately put in mildly stressful situations; episodes were shortened if distress became too great.',
        wrong=['Most infants were classified as insecure-avoidant', 'Infants showed no response to the stranger', 'Only one attachment type was found'])
K.study('ch10-st3', 'Van IJzendoorn and Kroonenberg', 1988, 'cross-cultural patterns of attachment', 'to investigate cross-cultural variation in attachment types using the Strange Situation',
        'A meta-analysis of 32 studies in 8 countries, involving about 2,000 infants assessed with the Strange Situation.',
        'secure attachment was the most common type in all countries; avoidant attachment was relatively common in West Germany and resistant attachment in Israel and Japan; variation within countries was about 1.5 times greater than between countries',
        'cultural variation in attachment',
        ['large combined sample', 'compared within- and between-country variation'],
        ['countries are not cultures', 'Strange Situation may lack validity in non-Western cultures', 'unequal sample sizes'],
        mtype='meta-analysis', culture='The Strange Situation was designed in the USA; its meaning may differ in Japan, where infants are rarely left with strangers')
K.study('ch10-st3', 'Harlow', 1958, 'contact comfort in rhesus monkeys', 'to investigate whether infant monkeys attach to the source of food or of comfort',
        'Infant rhesus monkeys were separated from their mothers and raised with two surrogate "mothers": one made of wire and one covered in soft cloth; in some conditions only the wire mother gave milk.',
        'the infants spent most of their time clinging to the cloth mother and ran to her when frightened, even when the wire mother provided food',
        'the importance of contact comfort in attachment',
        ['controlled experiment showing that comfort, not food, drives attachment'],
        ['animal research - generalisation to humans', 'severe, lasting harm: monkeys later showed abnormal social behaviour'],
        mtype='laboratory experiment', ethics='Infant monkeys were deliberately separated from their mothers and suffered long-term psychological harm, raising serious questions about the cost-benefit balance.')
K.study('ch10-st3', 'Bowlby', 1944, 'the "44 thieves"', 'to investigate whether early maternal separation is linked to later emotional problems and delinquency',
        'Bowlby interviewed 44 adolescents referred to his child guidance clinic for stealing and 44 controls with emotional problems who did not steal, along with their families.',
        '14 of the thieves were "affectionless psychopaths", and 12 of these had experienced prolonged separation from their mothers before age 5, compared with 2 of the 44 controls',
        'the long-term effects of maternal deprivation',
        ['detailed interviews; included a control group'],
        ['retrospective and correlational', 'Bowlby both interviewed and diagnosed - researcher bias', 'other factors (poverty, conflict) not controlled'],
        mtype='case study')

K.facts('ch10-st4', F(
    terms=[('gender identity', 'a person\'s internal sense of their own gender'),
           ('gender role', 'the behaviours, attitudes and activities considered appropriate for a gender within a culture'),
           ('gender schema', 'a mental framework containing beliefs about gender that guides attention and behaviour (Martin and Halverson, 1981)'),
           ('gender constancy', 'Kohlberg\'s final stage of gender development, at about 6-7 years, in which a child understands that gender remains stable across time and situations'),
           ('social role theory', 'Eagly and Wood\'s theory that gender differences arise from the different social roles men and women occupy'),
           ('gender stereotype', 'a generalised belief about the characteristics of males or females')],
    facts=[('In the "Baby X" study by Smith and Lloyd (1978), mothers playing with an infant they believed was a boy were more likely to:', 'Offer a hammer-shaped rattle and encourage physical activity', ['Offer a doll', 'Speak more softly', 'Ignore the infant'],
            'Adults treated the same infant differently depending on the perceived sex.'),
           ('Perry and Bussey (1979) found that children aged 8-9 were most likely to imitate:', 'The choices of several models of their own sex', ['The choices of any adult', 'Opposite-sex models', 'Models of their own sex only when rewarded'],
            'Children imitated behaviour performed consistently by same-sex models.'),
           ('Margaret Mead (1935) studied three societies in Papua New Guinea. Which society did she describe as having gentle, cooperative men and women?', 'The Arapesh', ['The Mundugumor', 'The Tchambuli', 'The Trobriand Islanders'],
            'She described the Tchambuli as reversing Western gender roles, a conclusion later disputed.')],
    why=[('Explain how social learning contributes to gender role development.', 'Children observe and imitate same-sex models (Perry and Bussey, 1979), and are reinforced for gender-appropriate behaviour by parents, peers and media, so gender roles are learned and maintained.'),
         ('Explain how gender schemas influence behaviour.', 'Once children identify with a gender, they attend to and remember information consistent with their gender schema and prefer "in-group" activities, which strengthens gender-typed behaviour.')],
    contrast=[('gender identity', 'gender role', 'Gender identity is a person\'s internal sense of their gender; a gender role is the set of behaviours a culture expects of people of that gender.')],
    misc=[('Gender roles are the same in all cultures because they are biologically determined.', 'Gender roles vary considerably across cultures and over time (Mead, 1935; changes in women\'s employment), showing strong sociocultural influences, although biology also plays a part.')],
    cases=[('a toy shop removing "boys\' and girls\'" sections', 'A large toy shop chain in the UK removed "boys" and "girls" signs in 2015 after campaigns arguing they reinforced stereotypes.', 'sociocultural influences on gender roles', 'labels act as environmental cues and models that reinforce gender schemas; removing them may reduce gender-typed choices')],
    apply=[('Using one theory, explain why a 5-year-old in Melbourne might insist that "only girls can be nurses".', 'Gender schema theory: the child has formed a schema that links nursing with females, based on observation and media, and processes information selectively; before gender constancy, children apply rigid rules; social learning: few male nurse models.', 3)],
    evaluate=[('Gender roles are mainly the result of sociocultural factors.', ['Baby X (Smith and Lloyd, 1978)', 'modelling (Perry and Bussey, 1979)', 'cross-cultural variation (Mead, 1935)'],
               ['prenatal hormones influence play (e.g. CAH studies)', 'some sex differences are found cross-culturally', 'Mead\'s findings have been criticised'],
               'Gender roles are strongly shaped by sociocultural factors, interacting with biological predispositions.')],
))
K.study('ch10-st4', 'Smith and Lloyd', 1978, 'adults\' treatment of "Baby X"', 'to investigate whether adults treat infants differently based on perceived sex',
        '32 mothers played individually with an unfamiliar 6-month-old infant who was dressed and named as a boy or a girl (regardless of actual sex); toys and behaviour were recorded.',
        'infants believed to be boys were offered more "masculine" toys (e.g. a hammer) and encouraged in gross motor activity; infants believed to be girls were offered dolls',
        'sociocultural influences on gender development',
        ['controlled design using the same infants as boys or girls', 'behavioural measures'],
        ['short, artificial interaction with a stranger\'s baby', 'small British sample in the 1970s'],
        mtype='laboratory experiment')
K.study('ch10-st4', 'Perry and Bussey', 1979, 'same-sex models and gender role learning', 'to investigate whether children learn gender-typed behaviour by imitating same-sex models',
        '8-9-year-old children watched eight adult models (four male, four female) choose between pairs of gender-neutral items such as fruit; models of the same sex made the same choices.',
        'children tended to choose the items selected by the same-sex models, especially when a model\'s choices were consistent with others of their sex',
        'observational learning in gender development',
        ['controlled, neutral items avoid existing stereotypes'],
        ['artificial task', 'US sample'],
        mtype='laboratory experiment')
K.study('ch10-st4', 'Mead', 1935, 'gender roles in three societies in Papua New Guinea', 'to investigate whether gender-typed behaviour varies across cultures',
        'Mead conducted ethnographic fieldwork with the Arapesh, Mundugumor and Tchambuli, observing and interviewing members of each society.',
        'she reported that both sexes were gentle among the Arapesh and aggressive among the Mundugumor, and that Tchambuli women were dominant, suggesting gender roles are culturally constructed',
        'cultural variation in gender roles',
        ['rich, in-depth ethnographic data', 'challenged biological determinism'],
        ['researcher bias; Mead later moderated her conclusions', 'interpretations disputed by later anthropologists'],
        mtype='ethnographic participant observation')

# ---------------------------------------------------------------------------------------------
# ch11 Class practical 1: conducting an experiment
# ---------------------------------------------------------------------------------------------
REPLICATIONS = [
    ('Glanzer and Cunitz (1966)', 'recall immediately vs after a 30-second filled delay', 'number of words recalled from the last five positions of a 15-word list'),
    ('Loftus and Palmer (1974)', 'verb in the critical question (smashed vs contacted)', 'estimated speed in km/h'),
    ('Bransford and Johnson (1972)', 'title given before vs no title', 'number of idea units recalled from the passage'),
    ('Stroop (1935)', 'congruent vs incongruent colour words', 'time in seconds to name the ink colours of 20 words'),
    ('Landry and Bartling (2011)', 'articulatory suppression vs no suppression', 'number of letters recalled in the correct serial position'),
    ('Tversky and Kahneman (1981)', 'gain frame vs loss frame', 'number of participants choosing the certain option'),
    ('Tversky and Kahneman (1974)', 'low anchor (10) vs high anchor (65)', 'estimate of the percentage of African countries in the UN'),
    ('Alter et al. (2007)', 'easy-to-read vs hard-to-read font', 'number of correct answers on the Cognitive Reflection Test'),
]


@K.add('ch11-st1', 'C3', (1, 5), 'short')
def replication(rng, slot):
    study, iv, dv = rng.choice(REPLICATIONS)
    who = name(rng)
    q = rng.randrange(5)
    lead = rng.choice([f'{who} is planning a class replication of {study}.', f'For her IA-style practical, {who} replicates {study} with classmates in {rng.choice(CITIES)}.',
                       f'A Grade 11 group decides to replicate {study}.'])
    if q == 0:
        return dict(stem=f'{lead} The IV is {iv}. Write an operationalised directional hypothesis for the study.',
                    answer=f'Participants will differ in {dv} in the direction found by {study}, according to {iv} (both variables operationalised).',
                    markingKey=f'1 mark: IV operationalised ({iv}); 1 mark: DV operationalised ({dv}); 1 mark: direction stated consistent with the original study.',
                    type='short', marks=3)
    if q == 1:
        return dict(stem=f'{lead} Describe two features of a standardised procedure that should be used.',
                    answer='Same written instructions read from a script to all participants; same materials, timing, room and order of tasks; same debrief; data recorded in the same way.',
                    markingKey='1 mark per feature identified, 1 mark per feature explained (why it improves reliability/replicability), up to 4.', type='short', marks=4)
    if q == 2:
        return dict(stem=f'{lead} The DV is {dv}. Explain one way of controlling an extraneous variable in this replication.',
                    answer='E.g. random allocation to conditions to spread participant variables, or counterbalancing in a repeated measures design to control order effects, or testing all participants at the same time of day in a quiet room.',
                    markingKey='1 mark: relevant extraneous variable identified for this study; 1 mark: control described; 1 mark: explanation of how it protects internal validity.', type='short', marks=3)
    if q == 3:
        return dict(stem=f'{lead} Suggest a suitable experimental design and justify your choice.',
                    answer=f'For {iv}: independent samples if exposure to one condition would reveal the aim or create practice effects; repeated measures with counterbalancing if equivalent materials exist and participant variables are a concern.',
                    markingKey='1 mark: design named; 2 marks: justification linked to the specific IV and possible order effects or participant variables.', type='short', marks=3)
    return dict(stem=f'{lead} Identify two ethical considerations and explain how each would be addressed.',
                answer='Informed consent (signed form; parental consent if under 16); right to withdraw (stated at start, data removed on request); debriefing (true aim revealed, especially if mild deception about the aim was used); confidentiality (participant codes, no names).',
                markingKey='1 mark for each consideration and 1 mark for each way it is addressed in this study (max 4). No credit for deception or harm being "accepted".', type='short', marks=4)


K.facts('ch11-st1', F(
    terms=[('replication', 'repeating a published study using the same or very similar procedure to check whether its findings hold'),
           ('aim', 'a general statement of what a study intends to investigate'),
           ('research hypothesis', 'a precise, testable prediction about the relationship between the operationalised IV and DV'),
           ('standardised procedure', 'a set procedure followed in exactly the same way for all participants'),
           ('standardised instructions', 'identical instructions given to all participants, usually read from a script'),
           ('pilot study', 'a small-scale trial run of a study to identify problems with materials or procedures before the main study'),
           ('materials', 'the stimuli, apparatus and documents used in a study, such as word lists, consent forms and response sheets')],
    facts=[('Why should a class replication use a pilot study?', 'To test materials and procedures and fix problems before collecting real data', ['To increase the sample size', 'To make the hypothesis directional', 'To avoid needing informed consent'],
            'A pilot reveals unclear instructions, ceiling/floor effects or timing problems.'),
           ('Which of the following is a properly operationalised DV?', 'Number of words correctly written down from a 15-word list within 90 seconds', ['How well participants remember', 'Memory performance', 'Whether participants enjoyed the task'],
            'It specifies exactly what is counted and under what conditions.')],
    why=[('Explain why a replication should follow the original study\'s procedure as closely as possible.', 'If the procedure differs, any difference in results could be due to the changes rather than to the original findings being unreliable; close replication tests reliability.'),
         ('Explain why standardised instructions are important.', 'They ensure every participant receives the same information, so differences in the DV are not due to differences in how the task was explained, which increases reliability and internal validity.')],
    contrast=[('an aim', 'a hypothesis', 'An aim is a general statement of the purpose of the study; a hypothesis is a precise, testable prediction about the operationalised variables.')],
    misc=[('A null hypothesis predicts that the experiment will fail.', 'A null hypothesis predicts no significant difference or relationship between the conditions; it is the statement tested by inferential statistics.')],
    cases=[('a ceiling effect in a pilot', 'In a pilot of a word-recall replication in Vienna, almost every participant recalls all 10 words in both conditions.', 'the value of a pilot study', 'the task was too easy (ceiling effect), so differences could not appear; a longer list or shorter study time is needed before the main study')],
    apply=[('Write standardised instructions for participants in a replication of the Stroop effect (no more than five sentences).', 'E.g. "You will see a list of words printed in coloured ink. Name the colour of the ink, not the word, as quickly and accurately as you can. Start when I say go and stop at the last word. I will time you with a stopwatch. You may stop at any time."', 3)],
    evaluate=[('Class replications of published studies are of little scientific value.', ['small, opportunity samples of peers', 'ethical constraints change procedures', 'demand characteristics'],
               ['test reliability in a new cultural context', 'develop understanding of methods', 'can reveal limitations of original studies'],
               'Class replications are mainly educational, but well-designed ones can provide useful evidence about the reliability and generalisability of findings.')],
))
scenarios(K, 'ch11-st1', SCEN_G11[2:] + SCEN_G11[:2], c=('C3',), d=(2, 5))

LEVELS = [('the number of words recalled from a list', 'ratio'), ('reaction time in milliseconds', 'ratio'),
          ('temperature in degrees Celsius in a classroom', 'interval'), ('whether a participant helped or did not help', 'nominal'),
          ('attachment type (A, B or C)', 'nominal'), ('rank order of finishing in a puzzle race', 'ordinal'),
          ('self-rated mood on a 1-10 scale', 'ordinal'), ('agreement on a 5-point Likert item', 'ordinal'),
          ('nationality of participants', 'nominal'), ('time in seconds to complete a maze', 'ratio'),
          ('position in a class ranking of essay quality', 'ordinal'), ('number of aggressive acts observed', 'ratio'),
          ('the acculturation strategy a migrant reports', 'nominal'), ('height in centimetres', 'ratio')]


@K.add('ch11-st2', ('C1', 'C2'), (1, 3), 'mcq')
def level_mcq(rng, slot):
    m, lv = rng.choice(LEVELS)
    return mcq(rng, f'What level of measurement is {m}?', lv, [x for x in ['nominal', 'ordinal', 'interval', 'ratio'] if x != lv],
               {'nominal': 'Categories with no order.', 'ordinal': 'Ordered data where intervals between values are not equal or known.',
                'interval': 'Equal intervals but no true zero.', 'ratio': 'Equal intervals and a true zero.'}[lv])


@K.add('ch11-st2', 'C3', (2, 4), 'short')
def level_choice(rng, slot):
    m, lv = rng.choice(LEVELS)
    ct = {'nominal': 'the mode', 'ordinal': 'the median', 'interval': 'the mean', 'ratio': 'the mean'}[lv]
    disp = {'nominal': 'no meaningful measure of dispersion (report frequencies/percentages)', 'ordinal': 'the range or interquartile range',
            'interval': 'the standard deviation', 'ratio': 'the standard deviation'}[lv]
    return dict(stem=f'A study in {rng.choice(CITIES)} records {m}. Identify the level of measurement and state the most appropriate measure of central tendency and of dispersion.',
                answer=f'{cap(lv)} data; central tendency: {ct}; dispersion: {disp}.', type='short', marks=3,
                markingKey=f'1 mark level ({lv}); 1 mark {ct}; 1 mark {disp}. (Accept the median for interval/ratio data if outliers are mentioned.)')


K.facts('ch11-st2', F(
    terms=[('raw data', 'the original, unprocessed scores collected from each participant'),
           ('nominal data', 'data in separate categories with no order, such as yes/no or attachment type'),
           ('ordinal data', 'data that can be ranked but where the intervals between values are not necessarily equal, such as ratings on a scale'),
           ('interval data', 'data measured on a scale with equal intervals between values but no true zero'),
           ('ratio data', 'data on a scale with equal intervals and a true zero, such as time or number of words recalled'),
           ('frequency table', 'a table that shows how often each value or category occurs'),
           ('quantitative data', 'numerical data that can be analysed statistically'),
           ('qualitative data', 'non-numerical data such as words, descriptions or images')],
    facts=[('Ratings of anxiety on a 1-10 scale are usually treated as which level of measurement?', 'Ordinal', ['Nominal', 'Ratio', 'Interval with a true zero'],
            'Ratings can be ordered, but the gap between 3 and 4 may not equal the gap between 8 and 9.'),
           ('Which is the best way to present the raw data of a class experiment in an IA-style report?', 'In an appendix, with summary descriptive statistics in the results section', ['Only in the results section, without summaries', 'Not at all, to protect confidentiality', 'As a pie chart'],
            'Results should show summarised data; raw data are kept in an appendix with participant codes.')],
    why=[('Explain why the level of measurement affects which descriptive statistics should be used.', 'Calculations such as the mean assume equal intervals between values; for nominal data only the mode makes sense and for ordinal data the median is more appropriate, so choosing the wrong statistic misrepresents the data.'),
         ('Explain why raw data should be stored with participant codes rather than names.', 'Codes protect confidentiality and anonymity while allowing the researcher to link each participant\'s scores across conditions and to delete data if a participant withdraws.')],
    contrast=[('ordinal data', 'interval data', 'Ordinal data can be ranked but the gaps between values are not equal (e.g. Likert ratings); interval data have equal gaps between values (e.g. temperature in Celsius).'),
              ('quantitative data', 'qualitative data', 'Quantitative data are numerical and can be analysed statistically; qualitative data are descriptive (words, meanings) and are analysed thematically.')],
    misc=[('A bar chart and a histogram are the same thing.', 'A bar chart shows separate categories or condition means with gaps between bars; a histogram shows the distribution of continuous data with no gaps.')],
    cases=[('a recall experiment with a scoring problem', 'In a class experiment in Bogotá, two students scored recall differently: one counted misspelled words as correct, the other did not.', 'organising and scoring data', 'without a clear operational scoring rule the data are unreliable; a coding rule must be agreed before scoring and applied to all participants')],
    apply=[('Construct a summary table for an experiment with two conditions (music vs silence) and 10 participants in each. State what should appear in the table and its title.', 'Title stating IV and DV (e.g. "Mean and standard deviation of words recalled (out of 20) in the music and silence conditions"); rows/columns: condition, mean, SD (and n); units given.', 3)],
    evaluate=[('Using the mean is always the best way to summarise data.', ['uses all scores; basis for further statistics'],
               ['distorted by outliers', 'inappropriate for nominal/ordinal data', 'may not be a real value'],
               'The mean is best for interval/ratio data without extreme scores; otherwise the median or mode should be used.')],
))
methods(K, 'ch11-st2', 'pct')

K.facts('ch11-st3', F(
    terms=[('mean', 'the arithmetic average: the sum of all scores divided by the number of scores'),
           ('median', 'the middle value when scores are placed in order'),
           ('mode', 'the most frequently occurring value in a data set'),
           ('range', 'the difference between the highest and lowest score'),
           ('standard deviation', 'a measure of the average spread of scores around the mean'),
           ('outlier', 'an extreme score that is very different from the rest of the data'),
           ('bar chart', 'a graph that shows the values of separate categories or conditions, such as condition means, with gaps between bars'),
           ('descriptive statistics', 'statistics that summarise and describe data, such as measures of central tendency and dispersion')],
    facts=[('Which measure of central tendency is least affected by an extreme score?', 'The median', ['The mean', 'The range', 'The standard deviation'],
            'The median depends only on the middle value(s).'),
           ('A large standard deviation indicates that:', 'Scores are widely spread around the mean', ['Most scores are close to the mean', 'The mean is very high', 'There are no outliers'],
            'SD measures spread.'),
           ('Which graph is most appropriate for comparing the mean scores of two conditions in an experiment?', 'A bar chart', ['A scattergram', 'A pie chart', 'A histogram of raw data'],
            'Separate conditions are shown as separate bars.')],
    why=[('Explain why it is useful to report both a measure of central tendency and a measure of dispersion.', 'Two conditions can have the same mean but very different spreads; dispersion shows how consistent the scores are and how representative the mean is.'),
         ('Explain why the standard deviation is usually better than the range.', 'The range uses only two scores and is distorted by outliers, whereas the SD uses every score to show the average spread around the mean.')],
    contrast=[('the mean', 'the median', 'The mean uses every score and is sensitive to outliers; the median is the middle value and is not affected by extreme scores.')],
    misc=[('If the mean of one condition is higher, the IV has definitely had an effect.', 'Descriptive statistics only describe the sample; an inferential test is needed to decide whether the difference is likely to be due to chance.')],
    cases=[('a reaction-time experiment with one very slow participant', 'In a class experiment in Seoul, nine participants have reaction times between 300 and 420 ms but one took 1,900 ms because he was distracted.', 'the choice of descriptive statistics', 'the outlier inflates the mean and SD; the median and range (or reporting the outlier and its cause) give a more accurate summary')],
    apply=[('A student reports: "Condition A: mean 12, SD 1.2; Condition B: mean 12, SD 5.8." Interpret these results.', 'The average performance is the same, but scores in B are much more spread out (less consistent); B may contain participants who were helped and others who were hindered by the condition.', 3)],
    evaluate=[('Descriptive statistics are sufficient to draw conclusions from an experiment.', ['summarise patterns clearly', 'show direction of effect and spread'],
               ['cannot show whether differences are due to chance', 'can be distorted by outliers', 'do not show effect size relative to variability without further analysis'],
               'Descriptive statistics are essential for describing results, but inferential statistics are needed to draw conclusions about the population.')],
))
methods(K, 'ch11-st3', 'desc', 'two')

K.facts('ch11-st4', F(
    terms=[('internal validity', 'the extent to which the study shows that changes in the DV were caused by the IV'),
           ('demand characteristics', 'cues in a study that lead participants to guess the aim and change their behaviour'),
           ('order effects', 'changes in performance in a repeated measures design caused by practice, fatigue or boredom'),
           ('ceiling effect', 'when a task is so easy that most participants score near the maximum, hiding differences between conditions'),
           ('floor effect', 'when a task is so hard that most participants score near the minimum'),
           ('single-blind procedure', 'a procedure in which participants do not know which condition they are in or the aim of the study')],
    facts=[('In a class replication, most participants scored 19 or 20 out of 20 in both conditions. This is:', 'A ceiling effect', ['A floor effect', 'An order effect', 'Demand characteristics'],
            'The task was too easy to show differences.'),
           ('Which change would most increase the generalisability of a class experiment?', 'Using a larger random sample from a wider population', ['Using only classmates', 'Shortening the instructions', 'Telling participants the hypothesis'],
            'A larger, more representative sample improves population validity.')],
    why=[('Explain why using classmates as participants is a limitation of many class practicals.', 'Classmates are a small opportunity sample of similar age, education and culture; they may know the study\'s aim (demand characteristics) and feel pressure to take part, reducing validity, generalisability and voluntary consent.'),
         ('Explain why a significant result in a class replication does not prove the original theory.', 'A single small study can produce significant results by chance (type I error), samples are unrepresentative, and other explanations (demand characteristics, confounds) may account for the result.')],
    contrast=[('a limitation of the design', 'a limitation of the sample', 'A design limitation concerns how the study was set up (e.g. order effects, lack of control); a sample limitation concerns who took part (e.g. size, representativeness).')],
    misc=[('A study with no ethical problems is automatically valid.', 'Ethics and validity are separate: a study can be ethical but poorly controlled, or valid but unethical.')],
    cases=[('a memory replication in a noisy hall', 'In Accra, a group tested half their participants in a quiet library and half in a noisy hall because rooms were unavailable.', 'internal validity', 'noise varied systematically with the conditions and became a confounding variable, so differences in recall cannot be attributed to the IV')],
    apply=[('Suggest two modifications to a class Stroop replication that used 12 classmates and found no significant difference, and explain how each could improve the study.', 'Larger and more varied sample (increases power and generalisability); counterbalance conditions to control order effects; use a longer word list to avoid floor/ceiling effects; time with software rather than stopwatches (more reliable).', 4)],
    evaluate=[('The main limitation of class practicals is their sample.', ['small opportunity samples of peers', 'WEIRD, limited generalisability'],
               ['procedural limitations (order effects, stopwatch timing)', 'demand characteristics', 'ethical constraints'],
               'Sampling is a major limitation, but design and measurement issues are often equally important.')],
))
methods(K, 'ch11-st4', 'two', 'r')

# ---------------------------------------------------------------------------------------------
# ch12 Class practical 2: conducting an observation
# ---------------------------------------------------------------------------------------------
K.facts('ch12-st1', F(
    terms=[('naturalistic observation', 'observation of behaviour in its natural setting without intervention by the researcher'),
           ('controlled observation', 'observation in a structured environment set up by the researcher, often a laboratory'),
           ('participant observation', 'observation in which the researcher joins the group being studied'),
           ('non-participant observation', 'observation in which the researcher observes from outside the group'),
           ('covert observation', 'observation in which participants do not know they are being observed'),
           ('overt observation', 'observation in which participants know they are being observed'),
           ('Hawthorne effect', 'a change in behaviour that occurs because people know they are being observed (participant reactivity)'),
           ('structured observation', 'an observation that uses predetermined behaviour categories and a systematic sampling method')],
    facts=[('Ainsworth\'s Strange Situation is best described as:', 'A controlled observation', ['A naturalistic observation', 'A covert participant observation', 'A field experiment'],
            'It takes place in a laboratory playroom with a standardised sequence of episodes.'),
           ('Which type of observation is most likely to produce the Hawthorne effect?', 'Overt observation', ['Covert observation', 'Content analysis of old diaries', 'Observation through hidden cameras in a public space'],
            'People change behaviour when they know they are observed.'),
           ('Festinger et al. (1956) joined a doomsday group pretending to be believers. This is:', 'Covert participant observation', ['Overt non-participant observation', 'Controlled observation', 'Structured interview'],
            'They were members of the group and concealed their identity.')],
    why=[('Explain why naturalistic observations have high ecological validity.', 'Behaviour is recorded in its everyday setting without manipulation, so it reflects how people really behave; however, extraneous variables are uncontrolled.'),
         ('Explain why participant observation can lead to bias.', 'By joining the group the researcher may lose objectivity ("going native"), influence the group\'s behaviour, and record selectively what they see.')],
    contrast=[('a naturalistic observation', 'a controlled observation', 'A naturalistic observation records behaviour in its natural setting with no intervention (high ecological validity); a controlled observation takes place in a structured setting designed by the researcher (more control and replicability).'),
              ('participant observation', 'non-participant observation', 'In participant observation the researcher joins the group, gaining insight but risking bias; in non-participant observation the researcher watches from outside, staying more objective but with less insight.')],
    misc=[('Observations can show the cause of behaviour.', 'Observations record what happens but do not manipulate an IV, so they cannot establish causality on their own.')],
    cases=[('observing children\'s play at break time', 'Two IB students in Geneva observe how many children play in mixed-gender groups during break time, sitting on a bench with notebooks.', 'overt naturalistic observation', 'behaviour is natural, but children may notice the students and change behaviour (reactivity); public setting reduces consent issues but parents and the school should agree')],
    apply=[('A student wants to observe whether people hold doors open for others at a shopping centre in Kuala Lumpur. Recommend a type of observation and justify it.', 'Covert, non-participant naturalistic observation: people\'s helping behaviour is natural if they do not know they are observed; acceptable ethically as it is a public place where people expect to be seen, with no identifying data recorded.', 3)],
    evaluate=[('Covert observation is the best way to study real behaviour.', ['avoids reactivity (Hawthorne effect)', 'natural behaviour - high ecological validity'],
               ['no informed consent; privacy concerns', 'cannot ask participants about motives', 'harder to record reliably'],
               'Covert observation gives the most natural data in public settings, but ethical limits mean overt or controlled observation is often preferable.')],
))
K.facts('ch12-st2', F(
    terms=[('behaviour checklist', 'a list of operationally defined behaviour categories that observers record'),
           ('coding scheme', 'a system of codes for categories of behaviour, used to record observations consistently'),
           ('inter-rater reliability', 'the extent to which two or more observers recording the same behaviour agree'),
           ('time sampling', 'recording behaviour at set time intervals, e.g. every 30 seconds'),
           ('event sampling', 'recording every occurrence of a specified behaviour during the observation period'),
           ('operational definition (observation)', 'a precise description of an observable behaviour so that observers can identify it consistently'),
           ('percentage agreement', 'a measure of inter-rater reliability: the number of agreements divided by the total number of observations, multiplied by 100')],
    facts=[('A common benchmark for acceptable inter-rater reliability using percentage agreement is:', 'At least 80%', ['At least 20%', 'Exactly 50%', '100%'],
            'Correlations of +0.8 or more are similarly treated as acceptable.'),
           ('Recording what a child is doing every 15 seconds is an example of:', 'Time sampling', ['Event sampling', 'Snowball sampling', 'Random sampling'],
            'Behaviour is recorded at fixed intervals.'),
           ('Which is the best operational definition for "aggression" in a playground observation?', 'Hitting, kicking or pushing another child', ['Being in a bad mood', 'Acting aggressively', 'Not being friendly'],
            'It lists specific, observable acts.')],
    why=[('Explain why behaviour categories must be operationally defined.', 'Clear, observable and mutually exclusive definitions mean different observers record the same behaviour in the same way, increasing inter-rater reliability and reducing observer bias.'),
         ('Explain how inter-rater reliability can be improved.', 'Train observers together using example videos, refine ambiguous categories, use a pilot observation, and calculate agreement until it reaches an acceptable level (e.g. 80%).')],
    contrast=[('time sampling', 'event sampling', 'Time sampling records behaviour at set intervals (good for frequent behaviour, may miss brief events); event sampling records every occurrence of a target behaviour (good for infrequent events, harder when behaviour is frequent).')],
    misc=[('High inter-rater reliability means the observation is valid.', 'Observers can agree consistently and still measure the wrong thing (e.g. a poorly chosen category); reliability is necessary but not sufficient for validity.')],
    cases=[('two observers coding on-task behaviour', 'In a classroom observation in Nairobi, two observers disagreed often about whether students looking out of the window were "off-task".', 'inter-rater reliability', 'the category was ambiguous; adding a clear operational definition (e.g. "eyes not on work or teacher for more than 5 seconds") would increase agreement')],
    apply=[('Design a behaviour checklist with four categories for observing helping behaviour in a school canteen. Give an operational definition for each.', 'E.g. holding a door (keeps door open for another person for 2+ seconds); picking up a dropped item for someone; offering to share food or a seat; giving directions/help when asked - categories observable and mutually exclusive.', 4)],
    evaluate=[('Structured observations with behaviour checklists provide reliable data.', ['clear categories enable high inter-rater agreement', 'quantitative data can be analysed'],
               ['categories may miss important behaviour', 'observer bias and drift over time', 'reliability does not guarantee validity'],
               'Checklists increase reliability, but researchers must pilot and refine categories and check agreement during the observation.')],
))
methods(K, 'ch12-st2', 'irr', 'pct')
K.facts('ch12-st3', F(
    terms=[('observer bias', 'when the observer\'s expectations or beliefs affect what they notice and record'),
           ('observer drift', 'a gradual change in how observers apply the coding scheme over time'),
           ('blind observer', 'an observer who does not know the hypothesis or the condition being observed'),
           ('privacy', 'the right of people not to have their personal lives observed without permission, especially in non-public places'),
           ('public setting', 'a place where people would expect to be seen by strangers, where observation without consent may be acceptable')],
    facts=[('Which strategy reduces observer bias?', 'Using observers who are blind to the hypothesis', ['Telling observers the expected results', 'Using only one observer', 'Making the categories vaguer'],
            'Blind observers cannot record selectively to support the hypothesis.'),
           ('According to most ethical guidelines, covert observation without consent is acceptable mainly when:', 'Behaviour is in a public place where people would expect to be observed', ['Participants are children', 'The researcher is a student', 'The behaviour is private'],
            'Privacy must be respected in non-public settings.')],
    why=[('Explain why observer bias is a problem in observational research.', 'Observers may see what they expect - e.g. interpreting rough play as aggression in boys more than girls - so data reflect the observer\'s expectations rather than the behaviour.'),
         ('Explain why observing people in a non-public place raises ethical issues.', 'People have a reasonable expectation of privacy (e.g. in homes or private chats); recording them without consent breaches privacy and the right to withdraw.')],
    contrast=[('observer bias', 'participant reactivity', 'Observer bias comes from the observer\'s expectations affecting what is recorded; participant reactivity is a change in participants\' behaviour because they know they are being observed.')],
    misc=[('Using video recordings removes all ethical issues in observation.', 'Video increases accuracy but raises additional issues of consent, data storage and identifiability.')],
    cases=[('observing customers on a café\'s CCTV', 'A student asks a café owner in Melbourne for CCTV footage to observe how often customers use their phones while eating with friends.', 'ethical issues in observation', 'customers did not consent to research use of their images; identifiable footage raises privacy and data-protection concerns - live public observation without recording identities would be more ethical')],
    apply=[('Two students observing gender differences in sharing among 6-year-olds both expect girls to share more. Suggest two ways of reducing observer bias in their study.', 'Use observers blind to the hypothesis; operationalise "sharing" precisely; record on video and code independently; calculate inter-rater reliability; observe in short time samples to reduce drift.', 4)],
    evaluate=[('Observer bias makes observational research unscientific.', ['expectations affect recording', 'interpretation of behaviour is subjective'],
               ['operational definitions and blind observers reduce bias', 'inter-rater reliability checks', 'bias exists in all methods'],
               'Observer bias is a real threat, but it can be reduced to an acceptable level by careful design.')],
))
K.facts('ch12-st4', F(
    terms=[('practical-based question', 'a Paper 2 question that asks students to apply knowledge of the class practicals they conducted, or to a described study'),
           ('unseen study', 'a description of a study not previously studied, which students must evaluate using their knowledge of research methods'),
           ('credibility (of a study)', 'the extent to which a study\'s findings can be trusted, based on its design, controls, sampling and analysis'),
           ('limitation (of a study)', 'a feature of a study\'s design, sample, measurement or ethics that reduces the confidence that can be placed in its conclusions')],
    facts=[('When evaluating an unseen study, which point is most likely to gain high marks?', 'A limitation explained with explicit reference to the details of that study', ['A list of general strengths of experiments', 'A description of a famous study', 'A summary of the study\'s procedure'],
            'Evaluation must be applied to the specific study.'),
           ('In Paper 2, a question asks you to "explain one way you controlled extraneous variables in your experiment". The best answer:', 'Names a specific variable and control from your own practical and explains its effect on validity', ['Defines extraneous variables', 'Describes Loftus and Palmer\'s controls', 'Lists all possible extraneous variables'],
            'Practical-based questions require reference to your own practical.')],
    why=[('Explain why generic evaluation points ("the sample was small") gain few marks when evaluating an unseen study.', 'The examiner expects evaluation applied to the specific study: why the sample size or composition matters for these findings and this conclusion, with a realistic improvement; generic points show little understanding.')],
    contrast=[('describing a study', 'evaluating a study', 'Describing states what was done and found; evaluating judges the strengths and limitations of how it was done and how far the conclusions are justified.')],
    misc=[('Evaluating a study means only listing its weaknesses.', 'Evaluation weighs strengths and limitations and judges how much they affect the conclusions.')],
    cases=[('an unseen study on music and exercise', 'An unseen study reports that 20 gym members in Toronto ran longer with fast music than slow music; members chose which session to attend.', 'evaluating an unseen study', 'self-selection to conditions confounds the IV (motivated runners may choose fast music); the gym sample limits generalisability; random allocation and counterbalancing would improve validity')],
    apply=[('A study reports that students who sleep with their phone in the bedroom have lower grades (r = -0.31, n = 200, one school in Hanoi). Write two practical-based evaluation points that a Paper 2 answer could include.', 'Correlation does not show causation (third variables such as stress, workload); a single school limits generalisability; self-reported phone use may be inaccurate; r = -0.31 is weak-moderate; a large sample is a strength.', 4)],
    evaluate=[('Experiments are the most useful class practical for understanding behaviour.', ['causal conclusions', 'control and replication'],
               ['observations give ecological validity', 'interviews and surveys give insight and breadth', 'triangulation across practicals is strongest'],
               'Each practical answers different kinds of questions; experiments are best for causality, but combining methods gives the fullest understanding.')],
))
methods(K, 'ch12-st4', 'desc', 'irr')
scenarios(K, 'ch12-st4', SCEN_G11, c=('C3', 'C4'), d=(3, 5))

# --- extra content for the practical chapters --------------------------------------------------
K.ar('ch11-st1', [
    ('A pilot study should be carried out before a class replication.', 'A pilot study allows problems with instructions, materials and timing to be fixed before real data are collected.', 0, 'R explains why pilots are recommended.'),
    ('A directional hypothesis should be used when previous research predicts the direction of the effect.', 'A directional hypothesis states that there will be no difference between conditions.', 2, 'A is true; R describes a null hypothesis, so it is false.'),
    ('Standardised instructions increase the reliability of an experiment.', 'Standardised instructions mean every participant receives the same information in the same way.', 0, 'Consistency of procedure allows replication and reduces variation not caused by the IV.'),
    ('Replications must always use exactly the same sample as the original study.', 'Replications test whether findings hold with new participants.', 3, 'A is false - replications use new samples; R is true.'),
    ('Operationalising the DV makes a study easier to replicate.', 'Operationalisation states precisely how a variable is measured.', 0, 'Precise measurement can be copied exactly by other researchers.'),
])
K.R.f['ch11-st1'].why += [
    ('Explain why a class replication may produce different results from the original study.', 'Differences in sample (age, culture, size), setting, materials (e.g. translated word lists), procedure changes made for ethical reasons, and chance variation can all lead to different results, especially with small samples.'),
    ('Explain why a hypothesis must include operationalised variables.', 'Only operationalised variables can be measured and tested; a hypothesis such as "music affects memory" cannot be shown to be true or false until "music" and "memory" are defined in measurable terms.'),
    ('Explain why researchers write a null hypothesis as well as a research hypothesis.', 'Inferential statistics test the null hypothesis: if the probability of the results under H0 is below the significance level, H0 is rejected in favour of the research hypothesis.'),
    ('Explain why ethical guidelines may require changes to the procedure of a published study when it is replicated in class.', 'IB rules forbid deception that would upset participants, stress or harm, and the use of under-16s without parental consent, so procedures such as Milgram\'s or Loftus and Pickrell\'s cannot be replicated as published; changes must be justified and may affect comparability.')]
K.R.f['ch11-st1'].contrast += [
    ('a directional hypothesis', 'a non-directional hypothesis', 'A directional (one-tailed) hypothesis predicts the direction of the difference (e.g. silence > music); a non-directional (two-tailed) hypothesis predicts a difference without stating its direction.'),
    ('standardised instructions', 'a standardised procedure', 'Standardised instructions are the identical words given to all participants; a standardised procedure covers everything done in the study - instructions, materials, timing, order and setting.')]
K.R.f['ch11-st1'].misc += [
    ('A pilot study is the same as the main study but with the results counted twice.', 'A pilot study is a small trial run whose purpose is to check materials and procedures; its data are not included in the main results.'),
    ('If a replication finds a different result, the original study must have been fraudulent.', 'Different results may reflect sampling, cultural or procedural differences or chance; replication failures call for further research, not automatic accusations.')]

K.ar('ch12-st1', [
    ('Covert observation reduces the Hawthorne effect.', 'Participants who do not know they are observed are less likely to change their behaviour.', 0, 'Reactivity depends on awareness of being observed.'),
    ('Controlled observations have higher ecological validity than naturalistic observations.', 'Controlled observations take place in settings designed by the researcher.', 3, 'A is false - controlled settings are more artificial; R is true.'),
    ('Participant observation can give insight into a group\'s meanings.', 'In participant observation the researcher joins the group being studied.', 0, 'Joining the group gives an insider view of its meanings and norms.'),
])
K.R.f['ch12-st1'].cases += [
    ('observing study habits in a university library', 'A researcher in Lisbon sits in a library and records every 2 minutes whether students are using laptops for study, social media or messaging; students are not told.', 'covert non-participant observation', 'the researcher stays outside the group and is hidden, so behaviour is natural, but consent is not obtained and categories (study vs social media) are hard to judge from a distance'),
    ('a researcher who works as a waiter', 'To study how staff deal with rude customers, a researcher takes a job as a waiter in a busy restaurant in Mumbai and keeps notes after each shift.', 'covert participant observation', 'it gives insider access and natural behaviour, but notes written later rely on memory, the researcher may lose objectivity, and colleagues have not consented'),
    ('a controlled observation of toddler sharing', 'In a university playroom in Toronto, pairs of toddlers are given one attractive toy while researchers film them through a one-way mirror.', 'controlled observation', 'the standardised setting allows comparison and replication, but the unfamiliar room may change behaviour and limits ecological validity'),
    ('a primatologist living with chimpanzees', 'Jane Goodall spent years observing chimpanzees at Gombe, Tanzania, recording tool use and social behaviour in their natural habitat.', 'naturalistic observation', 'long-term observation in the natural habitat revealed behaviour (e.g. termite fishing with tools) that controlled settings would not show, though the observer\'s presence could affect the animals')]
K.R.f['ch12-st1'].apply += [
    ('A student wants to study how pupils behave when a substitute teacher takes the lesson. Compare two possible types of observation she could use.', 'Overt non-participant observation (ethical, consent possible, but pupils may change behaviour) vs covert participant observation as a member of the class (natural behaviour but no consent and risk of bias); a compromise is overt observation over several lessons so pupils habituate.', 4),
    ('Explain how an observer could reduce participant reactivity in an overt observation of a nursery.', 'Spend time in the nursery before recording so children become used to the observer (habituation); sit unobtrusively; use video from a fixed position; avoid interacting.', 3)]
K.study('ch12-st1', 'Piliavin, Rodin and Piliavin', 1969, 'helping on the New York subway', 'to investigate the effect of the victim\'s condition (drunk or ill) and race on helping behaviour in a natural setting',
        'On the New York subway, a confederate "victim" carrying a cane (ill) or smelling of alcohol (drunk) collapsed in a carriage; covert observers recorded who helped and how quickly over about 4,450 passengers.',
        'the "ill" victim received spontaneous help on 95% of trials and the "drunk" victim on about 50%; there was no diffusion of responsibility in this setting',
        'helping behaviour in a naturalistic setting',
        ['high ecological validity - real passengers', 'large opportunity sample'],
        ['no informed consent or debriefing', 'passengers may have been distressed', 'observers\' recording may be inaccurate in a crowded carriage'],
        mtype='field experiment', ethics='Passengers were deceived, could not consent, were not debriefed and may have been distressed by a collapse.')
K.study('ch12-st1', 'Whyte', 1943, 'a street-corner gang in Boston', 'to understand the social structure of an Italian-American neighbourhood and its street-corner gangs',
        'Whyte lived for about three years in the North End of Boston ("Cornerville"), joining the "Norton Street gang" with the help of its leader "Doc", who knew he was a researcher; he kept detailed field notes.',
        'he found a highly organised social structure with clear hierarchies and obligations, challenging the view that slums were disorganised',
        'participant observation of a social group',
        ['rich, long-term insider data', 'key informant gave access and checked interpretations'],
        ['researcher became involved (e.g. voting several times in an election) - loss of objectivity', 'one neighbourhood; hard to replicate'],
        mtype='ethnographic participant observation')

K.R.f['ch12-st3'].cases += [
    ('a teacher observing her own class', 'A teacher in Singapore observes her own pupils for a project on cooperative learning and expects her new method to increase cooperation.', 'observer bias', 'her investment in the method may lead her to interpret ambiguous interactions as cooperative; a second, blind observer and clear categories would reduce bias'),
    ('observing teenagers in an online forum', 'A researcher in London collects posts from a password-protected teenage support forum to study how users discuss self-harm.', 'ethical issues in observational research', 'the forum is not truly public, users are minors and the topic is sensitive, so consent from moderators and users, anonymisation and safeguarding plans are required'),
    ('observing drivers at a junction', 'Students in Bogotá stand at a busy junction and record whether drivers stop fully at a stop sign.', 'ethics of public observation', 'observing public behaviour without consent is generally acceptable because drivers expect to be seen, provided no identifying data (e.g. number plates) are recorded'),
    ('a long observation session', 'Two observers in Oslo code playground aggression for 90 minutes without a break; by the end they are recording fewer pushes than at the start for similar behaviour.', 'observer drift and fatigue', 'tiredness and gradual changes in applying definitions reduce reliability; shorter sessions, breaks and re-checking agreement would help')]
K.R.f['ch12-st3'].apply += [
    ('Explain two ethical issues that would arise if a student secretly filmed classmates in the school canteen to study eating behaviour.', 'Privacy/consent: classmates did not agree to be filmed and video is identifiable; confidentiality and data storage: footage could be shared; power/peer pressure; better: overt observation with consent or recording without identifying people.', 4),
    ('A researcher observing a religious ceremony is a member of that faith. Explain one advantage and one disadvantage of this for the observation.', 'Advantage: understands meanings and is accepted (insider perspective, access); disadvantage: may take behaviour for granted or interpret it in line with own beliefs (bias), and may find it hard to report negative findings.', 4),
    ('Suggest how a researcher could protect participants\' confidentiality when observing patients\' behaviour in a hospital waiting room.', 'Gain permission from the hospital ethics board; record behaviour categories only, without names or descriptions that identify people; store notes securely; report results as group data; display a notice about the research.', 3)]
K.R.f['ch12-st3'].why += [
    ('Explain why observers should not know the hypothesis of a study.', 'Knowing the hypothesis can lead them, consciously or not, to notice and record behaviour that supports it (observer/expectancy bias); blind observers record more objectively.')]
K.study('ch12-st3', 'Rosenthal and Fode', 1963, 'experimenter expectancy with rats', 'to investigate whether experimenters\' expectations influence the results they record',
        'Psychology students were each given rats to train in a maze; half were told their rats were "maze-bright" and half "maze-dull", although the rats were randomly assigned.',
        'rats labelled "maze-bright" were recorded as learning the maze faster, showing that experimenters\' expectations biased the results',
        'observer and experimenter expectancy bias',
        ['random assignment of labels isolates the effect of expectations'],
        ['students may have handled rats differently (a real effect) or recorded results inaccurately - mechanism unclear', 'deception of student experimenters'],
        mtype='laboratory experiment', iv='expectation given to the student (maze-bright vs maze-dull)', dv='recorded number of correct maze runs')

K.ar('ch12-st4', [
    ('Evaluation of an unseen study should refer to specific details of that study.', 'Generic evaluation points apply equally to any study.', 0, 'Because generic points do not show understanding of the particular study, applied evaluation is required.'),
    ('Correlational unseen studies cannot support causal conclusions.', 'In correlational studies the researcher manipulates the IV.', 2, 'A is true; R is false - variables are measured, not manipulated.'),
    ('Self-selected samples may limit the generalisability of an unseen study.', 'Volunteers can differ systematically from non-volunteers.', 0, 'Volunteer bias explains the limited generalisability.'),
    ('A study with a large sample cannot have sampling bias.', 'A sample is biased when it systematically differs from the target population.', 3, 'A is false - large samples can still be biased (e.g. one city); R is true.'),
])
K.R.f['ch12-st4'].why += [
    ('Explain why it is important to identify the research method before evaluating an unseen study.', 'The method determines which evaluation points apply - e.g. causality is relevant to experiments, credibility and reflexivity to qualitative studies, and the third-variable problem to correlations.'),
    ('Explain why an improvement suggested for an unseen study must be realistic.', 'Examiners reward improvements that address a specific limitation and could be carried out (e.g. random allocation, counterbalancing), and explain how the change would improve validity, reliability or ethics.'),
    ('Explain how the six concepts can structure an evaluation of an unseen study.', 'Measurement (operationalisation, reliability), causality (design), bias (sampling, demand characteristics, researcher), perspective (cultural assumptions), responsibility (ethics) and change (replication over time) give a checklist that keeps evaluation focused.')]
K.R.f['ch12-st4'].contrast += [
    ('a strength of an unseen study', 'a limitation of an unseen study', 'A strength is a feature that increases confidence in the conclusions (e.g. random allocation); a limitation is a feature that reduces it (e.g. a self-selected sample); both must be linked to the study\'s claims.'),
    ('a practical-based question about your own practical', 'a question about an unseen study', 'Practical-based questions ask you to explain decisions made in the practical you conducted; unseen-study questions ask you to evaluate a study you have not seen before, using research-methods knowledge.')]
K.R.f['ch12-st4'].misc += [
    ('In Paper 2 you can answer practical-based questions using any famous study instead of your own practical.', 'Practical-based questions require reference to the practical you carried out; descriptions of published studies gain little credit.'),
    ('A good evaluation of an unseen study lists as many weaknesses as possible.', 'Quality matters more than quantity: a few well-explained, applied points with balance and justified improvements score highly.')]
