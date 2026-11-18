"""Cambridge International AS Level Psychology 9990 (grade 11): research methods and the twelve core studies.

Items mirror Paper 1 (Approaches, issues and debates: short answers on the core studies and an
evaluation essay) and Paper 2 (Research methods: data-based items on novel studies and a planning
question). Each topic is built from a knowledge pack (key terms, multiple-choice facts, assertion-reason
items, explanations, claims to check, evaluation points, application scenarios, essays) by the generic
builders below, plus research-methods data engines (experiments with two conditions, correlations,
observations with two observers) that generate fresh numbers every time.

g12_psychology imports the builders from this module.
"""
import math
from decimal import Decimal, ROUND_HALF_UP
import re

from ._lib import topic, mcq, compose, person, two_people, city, fmt

PROFILE = {'mark_scale': {'long': (2, 2), 'case': (1.25, 1.25)}, 'wordy': True}
CHAPTERS = {}
_PH = re.compile(r'\{(\w+)\}')


def cap(s):
    return s[:1].upper() + s[1:]


def low(s):
    return s[:1].lower() + s[1:]


def T(name, *extra):
    return topic(name, name.lower(), *extra)


def ctx(r):
    a, b = two_people(r)
    return {'person': a, 'person2': b, 'city': city(r)}


def fill(s, d):
    return _PH.sub(lambda m: str(d.get(m.group(1), m.group(0))), s)


def hround(x, n=1):
    """Round half up (as candidates do by hand), avoiding float banker's rounding."""
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def d1(x):
    return f'{hround(x, 1):.1f}'


def d2(x):
    return f'{hround(x, 2):.2f}'


def dn(x):
    """Number without a trailing .0 (medians, percentages)."""
    return fmt(hround(x, 1), 1)


def _mean(xs):
    return sum(xs) / len(xs)


def _med(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def _sd(xs):
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _lst(xs):
    return ', '.join(str(x) for x in xs)


def _marks_from_key(q):
    m = re.findall(r'\[(\d+)\]', q['key'])
    if m and 'marks' not in q:
        q['marks'] = int(m[-1])
    return q


# ============================================================== generic builders

def add_terms(t, terms, foils=()):
    """terms: [(term, definition)] -> C1 MCQ (definition -> term) and C1 short 'define' items."""
    pool = [x for x, _ in terms] + list(foils)
    if len(pool) >= 4:
        for term, d in terms:
            def fn(r, D, term=term, d=d):
                lead = r.choice(['Which term describes', 'Which term is defined as', 'Identify the term for'])
                opts, a = mcq(r, cap(term), [cap(x) for x in pool if x != term])
                return {'stem': f'{lead} the following: “{cap(d)}”?' if lead != 'Identify the term for' else f'Identify the term for the following: “{cap(d)}”.',
                        'options': opts, 'answer': a, 'key': f'{cap(term)}: {d}. [1]'}
            fn.__name__ = 'term_mcq'
            t.add('C1', (1, 2), 'mcq')(fn)
    t.fixed('C1', (2, 3), [(r_, cap(d) + '.', f'{cap(term)}: {d}. 1 mark for a partial definition; 2 marks for a full, accurate definition [2]')
                           for term, d in terms for r_ in [f'Define the term ‘{term}’.' if len(term) % 2 else f'What is meant by ‘{term}’?']], type='short')


def add_mcq(t, entries, D=(1, 2, 3)):
    """entries: (stem, answer, [3+ distractors], key)."""
    for stem, ans, ds, key in entries:
        def fn(r, D_, stem=stem, ans=ans, ds=ds, key=key):
            opts, a = mcq(r, ans, list(ds))
            return {'stem': stem, 'options': opts, 'answer': a, 'key': key if re.search(r'\[\d+\]', key) else key + ' [1]'}
        fn.__name__ = 'mcq'
        t.add('C1', D, 'mcq')(fn)


AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.', 'Both A and R are true, but R is not the correct explanation of A.',
           'A is true, but R is false.', 'A is false, but R is true.']
AR_CODE = {'AR': 0, 'AnR': 1, 'A': 2, 'R': 3}


def add_ar(t, entries):
    """Assertion-reason MCQs: (assertion, reason, code in AR/AnR/A/R, why)."""
    for A, R, code, why in entries:
        def fn(r, D, A=A, R=R, code=code, why=why):
            return {'stem': f'Assertion (A): {A} Reason (R): {R} Choose the correct option.', 'options': list(AR_OPTS),
                    'answer': AR_OPTS[AR_CODE[code]], 'key': f'{why} [1]'}
        fn.__name__ = 'ar'
        t.add('C2', (2, 3), 'mcq')(fn)


def add_explain(t, entries, D=(2, 3, 4)):
    t.fixed('C2', D, entries, type='explain')


CLAIM_LEADS = ['A student writes:', 'In a revision session, a student says:', 'A revision website states:', 'A classmate claims:']


def add_claims(t, claims):
    ents = []
    for i, (c, ok, why) in enumerate(claims):
        ents.append((f'{CLAIM_LEADS[i % 4]} “{c}” Is this correct? Explain your answer.', ('Correct. ' if ok else 'Not correct. ') + why,
                     '1 mark: correct judgement; 1 mark: accurate explanation [2]'))
    t.fixed('C2', (1, 2, 3), ents, type='explain')


EVAL_LEADS = [
    'Explain one {kind} of {who} in terms of {issue}.',
    'With reference to {who}, explain one {kind} relating to {issue}.',
    '{Who} can be evaluated in terms of {issue}. Explain one {kind} of the study relating to this issue.',
    'Outline one {kind} of {who} that relates to {issue}.',
]


def add_evals(t, who, evals):
    """evals: [(issue, 'strength'|'weakness', point)] -> C2 explain items and C4 'two strengths and two weaknesses' essays."""
    def c2(r, D):
        issue, kind, pt = r.choice(evals)
        lead = r.choice(EVAL_LEADS)
        stem = lead.format(kind=kind, who=who, Who=cap(who), issue=issue)
        return {'stem': stem, 'answer': pt, 'key': f'1 mark: identifies a relevant {kind} linked to {issue}; 1 mark: explained using detail from the study [2]',
                'marks': 2, 'type': 'explain'}
    c2.__name__ = 'eval_c2'
    t.add('C2', (2, 3, 4), 'explain')(c2)

    def c2b(r, D):
        s = [e for e in evals if e[1] == 'strength']
        w = [e for e in evals if e[1] == 'weakness']
        if not s or not w:
            return None
        a, b = r.choice(s), r.choice(w)
        stem = r.choice([f'Explain one strength and one weakness of {who}. One of your points must be about {a[0]}.',
                         f'Explain one strength of {who} relating to {a[0]} and one weakness relating to {b[0]}.',
                         f'Outline one strength and one weakness of {who}, with one point about {b[0]}.'])
        return {'stem': stem, 'answer': f'Strength ({a[0]}): {a[2]} Weakness ({b[0]}): {b[2]}',
                'key': '2 marks for each point: 1 mark identification, 1 mark explanation in the context of the study [4]', 'marks': 4, 'type': 'explain'}
    c2b.__name__ = 'eval_sw'
    t.add('C2', (3, 4), 'explain')(c2b)

    def c4(r, D):
        s = [e for e in evals if e[1] == 'strength']
        w = [e for e in evals if e[1] == 'weakness']
        if len(s) < 2 or len(w) < 2:
            return None
        ss, ww = r.sample(s, 2), r.sample(w, 2)
        must = r.choice(ss + ww)[0]
        if D <= 2:
            stem = f'Evaluate {who} in terms of one strength and one weakness.'
            ss, ww = ss[:1], ww[:1]
        else:
            stem = r.choice([
                f'Evaluate {who} in terms of two strengths and two weaknesses. At least one of your evaluation points must be about {must}.',
                f'Evaluate {who}, including a discussion of {must}.',
                f'Discuss the strengths and weaknesses of {who}. Include at least one point about {must}.',
                f'“{cap(who)} has more strengths than weaknesses.” Evaluate this view, including {must} in your answer.',
            ])
        ans = ' '.join(f'Strength ({a}): {p}' for a, _, p in ss) + ' ' + ' '.join(f'Weakness ({a}): {p}' for a, _, p in ww) + \
            ' Conclusion: a reasoned judgement about the overall value of the study.'
        key = ('Levels of response. Top band: strengths and weaknesses are accurate, well explained and clearly linked to the study, the named issue is '
               'discussed, the answer is well organised and reaches a conclusion. Middle band: points are mostly accurate but one side is less developed '
               'or links to the study are general. Lower band: points are identified but brief, generic or one-sided. Description of the procedure '
               'without evaluation receives little credit.')
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long'}
    c4.__name__ = 'eval_c4'
    t.add('C4', (2, 3, 4, 5), 'long')(c4)


def add_apply(t, scenes, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    """scenes: [(intro with {person}/{city}, [(question, answer, key-with-[n])])]."""
    def mk(k, C):
        def fn(r, D):
            intro, parts = r.choice(scenes)
            d = ctx(r)
            pl = [(lambda r_, p=p: (fill(p[0], d), fill(p[1], d), fill(p[2], d))) for p in parts]
            return compose(r, fill(intro, d), pl, k=k, type_='case')
        fn.__name__ = 'apply_' + C
        return fn
    if C3:
        t.add('C3', C3, 'case')(mk((2, 3), 'C3'))
    if C4:
        t.add('C4', C4, 'case')(mk((3, 4), 'C4'))


ESSAY_FORMS = ['Evaluate the view that {p}.', 'To what extent do you agree that {p}?', 'Discuss the extent to which {p}.',
               '‘{P}.’ Discuss this view.', 'Assess the view that {p}.', '‘{P}.’ To what extent do you agree?',
               'Discuss whether {p}.', '‘{P}.’ Evaluate this statement, using evidence from psychology.']


def add_essays(t, essays, D=(2, 3, 4, 5)):
    """essays: [(claim, [for], [against], [hints])]."""
    def fn(r, D_):
        claim, pro, con, hints = r.choice(essays)
        if D_ <= 2:
            stem = f'Explain one argument for and one argument against the view that {claim}.'
            ans = f'For: {pro[0]} Against: {con[0]}'
            key = '2 marks: one argument for, explained; 2 marks: one argument against, explained [4]'
            return {'stem': stem, 'answer': ans, 'key': key, 'marks': 4, 'type': 'explain'}
        form = r.choice(ESSAY_FORMS)
        stem = form.replace('{p}', claim).replace('{P}', cap(claim))
        if hints and r.random() < 0.6:
            hs = r.sample(list(hints), min(len(hints), r.choice([2, 3])))
            stem += ' In your answer, you may refer to ' + ', '.join(hs[:-1]) + ' and ' + hs[-1] + '.'
        ans = 'Arguments for: ' + ' '.join(pro) + ' Arguments against: ' + ' '.join(con) + ' Conclusion: a supported judgement weighing the evidence on both sides.'
        key = ('Levels of response. Top band: accurate, detailed psychological knowledge (named studies/theories) used to build a two-sided argument; '
               'evaluation includes issues such as validity, reliability, generalisability, ethics or usefulness; a justified conclusion. '
               'Middle band: relevant knowledge with some evaluation, but one side or the conclusion is underdeveloped. '
               'Lower band: limited, mostly descriptive answer with little evaluation.')
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long'}
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)


# ---------------------------------------------------------------- research-methods data engines

DESIGNS = {
    'independent measures': ('different participants take part in each condition',
                             'participant variables (individual differences between the two groups) may explain the difference in the DV instead of the IV',
                             'randomly allocate participants to the conditions'),
    'repeated measures': ('the same participants take part in both conditions',
                          'order effects (practice, fatigue or boredom) may affect performance in the second condition',
                          'counterbalance the order, so half do condition A first and half do condition B first'),
    'matched pairs': ('participants are paired on a relevant variable and one member of each pair does each condition',
                      'matching is time-consuming and pairs can never be matched on every relevant variable',
                      'match participants on the most relevant variables before allocation'),
}

SAMPLES = [
    ('opportunity', 'people who were in the college canteen at lunchtime when {person} was collecting data',
     'only people present at that place and time could be chosen, so the sample may be biased and not representative of the target population'),
    ('volunteer', 'people who replied to an advertisement on a community website in {city}',
     'volunteers may share characteristics (for example being more curious or helpful), so the sample is self-selected and may not represent the target population'),
    ('random', 'students whose names were drawn at random from a list of every student at a college in {city}',
     'it needs a complete list of the target population and selected people may refuse, so the final sample may still be unrepresentative'),
    ('opportunity', 'shoppers who happened to pass {person} in a shopping centre in {city}',
     'only people at that shopping centre at that time could be chosen, so the sample may be biased and results may not generalise'),
    ('volunteer', 'people who responded to a poster in a library in {city} asking for participants',
     'only people who saw the poster and chose to respond took part, so the sample may be unrepresentative'),
    ('random', 'people selected from a full list of residents of {city} using a random number generator',
     'random selection does not guarantee a representative sample, especially when the sample is small, and some people may refuse'),
]

GRAPH_ANS = ('Bar chart, because the IV has separate (discrete) categories, so the mean for each condition is shown as a separate bar with gaps between bars.',
             '1 mark: bar chart; 1 mark: justification (discrete conditions / categories, not continuous data) [2]')


def _gen_two(r, S, D):
    lo, hi = S['range']
    sd = S.get('sd', (hi - lo) / 7)
    n = r.choice([6, 7, 8] if D <= 3 else [8, 9, 10])
    for _ in range(40):
        base = r.uniform(*S['base'])
        diff = r.uniform(*S['diff'])
        hiA = S.get('higher', 'A') == 'A'
        mA, mB = (base + diff, base) if hiA else (base, base + diff)
        xa = [min(hi, max(lo, int(round(r.gauss(mA, sd))))) for _ in range(n)]
        xb = [min(hi, max(lo, int(round(r.gauss(mB, sd))))) for _ in range(n)]
        out = None
        if D >= 3 and r.random() < 0.45:
            which = r.choice('AB')
            xs = xa if which == 'A' else xb
            m = _mean(xs)
            v = lo if (m - lo) > (hi - m) else hi
            xs[r.randrange(n)] = v
            if abs(v - _med(xs)) < 2.5 * sd:
                continue
            out = (which, v)
        a, b = _mean(xa), _mean(xb)
        if (a > b) != hiA or abs(a - b) < max(0.5, (hi - lo) * 0.05):
            continue
        if len(set(xa)) < 3 or len(set(xb)) < 3:
            continue
        return n, xa, xb, out
    return None


def _ana(S, n, xa, xb):
    return {'n': n, 'xa': xa, 'xb': xb, 'mA': _mean(xa), 'mB': _mean(xb), 'medA': _med(xa), 'medB': _med(xb),
            'rA': max(xa) - min(xa), 'rB': max(xb) - min(xb), 'sA': sum(xa), 'sB': sum(xb), 'sdA': _sd(xa), 'sdB': _sd(xb)}


def _exp_parts(S, g, out, d, evaluative):
    A, B = S['A'], S['B']
    gA, gB = S['gA'], S['gB']
    design = S.get('design', 'independent measures')
    ddef, dweak, dfix = DESIGNS[design]
    meas = S['measure']
    P = []
    P.append(lambda r: ('Identify the independent variable (IV) and the dependent variable (DV) in this study.',
                        f'IV: {S["iv"]}. DV: {S["dv"]}.', '1 mark: IV; 1 mark: DV, operationalised [2]'))

    def hyp(r):
        kind = r.choice(['directional (one-tailed)', 'non-directional (two-tailed)', 'null'])
        if kind.startswith('directional'):
            a = f'{cap(gA)} {S["more"]} {gB}.'
        elif kind.startswith('non'):
            a = f'There will be a difference in {meas} between {gA} and {gB}.'
        else:
            a = f'There will be no difference in {meas} between {gA} and {gB}.'
        return (f'Write a {kind} hypothesis for this study.', a, '1 mark: IV and DV both included (operationalised); 1 mark: correct form of hypothesis [2]')
    P.append(hyp)
    P.append(lambda r: ('Calculate the mean score for each condition. Give your answers to one decimal place.',
                        f'{cap(A)}: {d1(g["mA"])}; {B}: {d1(g["mB"])}.',
                        f'{cap(A)}: {g["sA"]} ÷ {g["n"]} = {d1(g["mA"])}; {B}: {g["sB"]} ÷ {g["n"]} = {d1(g["mB"])}. 1 mark for each correct mean [2]'))

    def med(r):
        c = r.choice('AB')
        xs, lab, m = (g['xa'], A, g['medA']) if c == 'A' else (g['xb'], B, g['medB'])
        return (f'Calculate the median score for the {lab} condition.', dn(m),
                f'Ordered scores: {_lst(sorted(xs))}; median = {dn(m)}. 1 mark: data ordered; 1 mark: correct median [2]')
    P.append(med)
    P.append(lambda r: ('Calculate the range of scores for each condition.', f'{cap(A)}: {g["rA"]}; {B}: {g["rB"]}.',
                        f'{cap(A)}: {max(g["xa"])} − {min(g["xa"])} = {g["rA"]}; {B}: {max(g["xb"])} − {min(g["xb"])} = {g["rB"]}. 1 mark each [2]'))

    def pct(r):
        allv = sorted(g['xa'] + g['xb'])
        k = allv[len(allv) // 2]
        c = r.choice('AB')
        xs, lab = (g['xa'], A) if c == 'A' else (g['xb'], B)
        cnt = sum(1 for x in xs if x >= k)
        p = 100 * cnt / len(xs)
        return (f'Calculate the percentage of participants in the {lab} condition who scored {k} or more. Show your working.',
                f'{dn(p)}%', f'{cnt} out of {len(xs)} participants scored {k} or more: {cnt} ÷ {len(xs)} × 100 = {dn(p)}%. 1 mark working; 1 mark answer [2]')
    P.append(pct)
    if out:
        lab = A if out[0] == 'A' else B
        P.append(lambda r: (f'Explain why the median may be a better measure of central tendency than the mean for the {lab} condition.',
                            f'The score of {out[1]} is an extreme score (outlier) compared with the rest of the {lab} data; the mean is distorted by it, but the median is not affected by extreme values, so it is more representative.',
                            f'1 mark: identifies the outlier ({out[1]}); 1 mark: mean distorted / median unaffected by extreme scores [2]'))

    def concl(r):
        if g['mA'] > g['mB']:
            a = f'The {A} condition had a higher mean ({d1(g["mA"])}) than the {B} condition ({d1(g["mB"])}), suggesting that {S["concl_A"]}'
        else:
            a = f'The {B} condition had a higher mean ({d1(g["mB"])}) than the {A} condition ({d1(g["mA"])}), suggesting that {S["concl_B"]}'
        return ('Using the mean scores, state one conclusion that can be drawn from these results.', a,
                '1 mark: conclusion about the effect of the IV on the DV; 1 mark: supported with the means [2]')
    P.append(concl)
    P.append(lambda r: ('Name the experimental design used in this study and explain one weakness of using this design here.',
                        f'{cap(design)}: {ddef}. Weakness: {dweak}.', '1 mark: correct design; 1 mark: weakness explained in context [2]'))
    if S.get('controls'):
        P.append(lambda r: ('Describe one variable that should be controlled in this study and explain why.', cap(r.choice(S['controls'])) + '.',
                            '1 mark: relevant control identified; 1 mark: explains how it would otherwise act as a confounding variable [2]'))
    P.append(lambda r: ('Name a suitable type of graph to display the mean scores for the two conditions, and justify your choice.', GRAPH_ANS[0], GRAPH_ANS[1]))

    def sdp(r):
        more = A if g['sdA'] > g['sdB'] else B
        if abs(g['sdA'] - g['sdB']) < 0.15:
            return None
        return (f'The standard deviation for the {A} condition was {d2(g["sdA"])} and for the {B} condition was {d2(g["sdB"])}. Explain what these values show.',
                f'The {more} condition has the larger standard deviation, so its scores are more spread out around the mean; the other condition’s scores are more consistent.',
                '1 mark: identifies the condition with the larger spread; 1 mark: explains that a larger SD means scores are more spread around the mean [2]')
    P.append(sdp)

    def samp(r):
        s = r.choice(SAMPLES)
        return (f'The participants were {fill(s[1], d)}. Identify the sampling technique used and explain one weakness of it.',
                f'{cap(s[0])} sampling. Weakness: {s[2]}.', '1 mark: sampling technique; 1 mark: weakness explained [2]')
    if not S.get('nosample'):
        P.append(samp)
    if S.get('ethics'):
        P.append(lambda r: ('Explain one ethical issue that the researcher should consider in this study.', cap(r.choice(S['ethics'])) + '.',
                            '1 mark: ethical guideline named; 1 mark: applied to this study [2]'))
    if evaluative:
        hiA = S.get('higher', 'A') == 'A'
        xh, xl = (g['xa'], g['xb']) if hiA else (g['xb'], g['xa'])
        ov = min(xh) <= max(xl)
        P.append(lambda r: (f'To what extent do these results support the prediction that {gA} {S["more"]} {gB}? Use the data in your answer.',
                            f'Mean for {A} = {d1(g["mA"])} and {B} = {d1(g["mB"])}; the direction of the difference ' +
                            ('matches' if (g['mA'] > g['mB']) == hiA else 'does not match') +
                            (f' the prediction, but the scores in the two conditions overlap (ranges {g["rA"]} and {g["rB"]})' if ov else ' the prediction and the scores in the two conditions do not overlap') +
                            f' and the sample is small (n = {g["n"]} per condition), so the results ' + ('only partly support it' if ov else 'support it, although the small sample limits confidence') +
                            '; a statistical test would be needed to show the difference is significant.',
                            '1 mark: uses both means; 1 mark: judgement about direction; 1 mark: limitation such as overlap of scores, small sample or no statistical test [3]'))
        P.append(lambda r: ('Suggest one improvement to this study and explain how it would improve the validity or reliability of the results.',
                            cap(r.choice(S.get('improve', [f'use a larger sample with more participants in each condition, so that anomalous individuals have less effect and the results are more reliable and generalisable', dfix + ', to reduce the effect of ' + ('participant variables' if design != 'repeated measures' else 'order effects')]))) + '.',
                            '1 mark: improvement; 1 mark: how to do it; 1 mark: effect on validity/reliability explained [3]'))
        P.append(lambda r: (f'Explain why a {"repeated measures" if design != "repeated measures" else "independent measures"} design might have been used instead, and one problem this would cause.',
                            (f'Repeated measures removes participant variables because the same people do both conditions, but order effects (practice or fatigue) and demand characteristics become more likely; counterbalancing would be needed.'
                             if design != 'repeated measures' else
                             'Independent measures avoids order effects and makes it harder to guess the aim, but participant variables between the two groups could then explain the results, and more participants are needed.'),
                            '1 mark: advantage of the alternative design; 1 mark: problem it causes; 1 mark: applied to this study [3]'))
    return P


def add_exp(t, S, C3=(1, 2, 3, 4, 5), C4=(3, 4, 5)):
    """Two-condition experiment data. S: intro (list of frames with {person}/{city}/{n}/{A}/{B}), A, B, gA, gB, more, measure, iv, dv,
    range, base, diff[, sd, higher, design, controls, ethics, improve, concl_A, concl_B]."""
    def mk(evaluative, k):
        def fn(r, D):
            res = _gen_two(r, S, D)
            if not res:
                return None
            n, xa, xb, out = res
            g = _ana(S, n, xa, xb)
            d = ctx(r)
            d.update({'n': n, 'N': 2 * n if S.get('design', 'independent measures') != 'repeated measures' else n, 'A': S['A'], 'B': S['B']})
            intro = fill(r.choice(S['intro']), d)
            data = f'Table: {S["dvshort"]} — {cap(S["A"])}: {_lst(xa)}. {cap(S["B"])}: {_lst(xb)}.'
            if not evaluative and D <= 1:
                c = r.choice('AB')
                xs, lab = (xa, S['A']) if c == 'A' else (xb, S['B'])
                kind = r.choice(['mean', 'median', 'range'])
                if kind == 'mean':
                    ans = d1(_mean(xs)); ds = [d1(sum(xs) / (len(xs) - 1)), d1(_mean(xs) + 1), dn(_med(xs)) if dn(_med(xs)) != ans else d1(_mean(xs) - 1), d1(sum(xs) / (len(xs) + 1)), d1(_mean(xs) - 0.5)]
                    key = f'{sum(xs)} ÷ {len(xs)} = {ans} [1]'
                    q = f'What is the mean score for the {lab} condition, to one decimal place?'
                elif kind == 'median':
                    ans = dn(_med(xs)); ds = [dn(xs[len(xs) // 2]), d1(_mean(xs)), dn(_med(xs) + 1), dn(_med(xs) - 1), dn(_med(xs) + 0.5), str(max(set(xs), key=xs.count))]
                    key = f'Ordered: {_lst(sorted(xs))}; median = {ans} [1]'
                    q = f'What is the median score for the {lab} condition?'
                else:
                    ans = str(max(xs) - min(xs)); ds = [str(max(xs)), str(max(xs) - min(xs) + 1), str(max(xs) + min(xs)), str(max(xs) - min(xs) - 1), str(min(xs))]
                    key = f'{max(xs)} − {min(xs)} = {ans} [1]'
                    q = f'What is the range of scores for the {lab} condition?'
                ds = [x for x in ds if x != ans]
                if len(set(ds)) < 3:
                    return None
                opts, a = mcq(r, ans, ds)
                return {'stem': f'{intro} {data} {q}', 'options': opts, 'answer': a, 'key': key, 'type': 'mcq'}
            parts = _exp_parts(S, g, out, d, evaluative)
            if evaluative:
                ev = parts[-3:]
                q = compose(r, f'{intro} {data}', parts[:-3], k=(2,), type_='case')
                if not q:
                    return None
                q2 = compose(r, '', ev, k=(1, 2), type_='case')
                # merge: re-letter parts
                return _merge(q, q2)
            return compose(r, f'{intro} {data}', parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical' if D <= 3 else 'case')
        fn.__name__ = 'exp_' + ('c4' if evaluative else 'c3')
        return fn
    if C3:
        t.add('C3', C3, 'numerical')(mk(False, None))
    if C4:
        t.add('C4', C4, 'case')(mk(True, None))


def _split(q):
    """Split a composed question into (intro, [(text, answer, key)])."""
    st, an, ke = q['stem'], q['answer'], q['key']
    if not re.search(r'\(a\) ', st):
        return st, []
    intro, rest = st.split(' (a) ', 1) if ' (a) ' in st else (st.split('(a) ', 1)[0], st.split('(a) ', 1)[1])
    texts = re.split(r' \([b-h]\) ', rest)
    answers = re.split(r' \([b-h]\) ', an.split('(a) ', 1)[1])
    keys = re.split(r' \([b-h]\) ', ke.split('(a) ', 1)[1])
    return intro, list(zip(texts, answers, keys))


def _merge(q1, q2):
    """Append the parts of q2 (possibly a single part) to q1, re-lettering."""
    i1, p1 = _split(q1)
    if not p1:
        i1, p1 = '', [(q1['stem'], q1['answer'], q1['key'])]
    if re.search(r'\(a\) ', q2['stem']):
        _, p2 = _split(q2)
    else:
        p2 = [(q2['stem'].strip(), q2['answer'], q2['key'])]
    parts = p1 + p2
    L = 'abcdefgh'
    stem = i1.strip() + ' ' + ' '.join(f'({L[j]}) {x[0]}' for j, x in enumerate(parts))
    ans = ' '.join(f'({L[j]}) {x[1]}' for j, x in enumerate(parts))
    key = ' '.join(f'({L[j]}) {x[2]}' for j, x in enumerate(parts))
    marks = sum(int((re.findall(r'\[(\d+)\]', x[2]) or ['1'])[-1]) for x in parts)
    return {'stem': stem, 'answer': ans, 'key': key, 'marks': min(20, marks), 'minutes': round(max(1.0, marks * 1.25) * 2) / 2, 'type': 'case'}


def _pearson(x, y):
    mx, my = _mean(x), _mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0


def _strength(rv):
    a = abs(rv)
    s = 'strong' if a >= 0.7 else 'moderate' if a >= 0.4 else 'weak'
    return f'{s} {"positive" if rv > 0 else "negative"}'


def add_corr(t, S, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    """Correlation data. S: intro frames, x, y (co-variable names), xr, yr (ranges), sign (+1/-1), xs/ys short names, third (list of third variables)."""
    def fn(r, D, evaluative=False):
        n = r.choice([8, 9, 10])
        for _ in range(40):
            x = [r.randint(*S['xr']) for _ in range(n)]
            lo, hi = S['yr']
            mx = _mean(x)
            span = (S['xr'][1] - S['xr'][0]) or 1
            y = [min(hi, max(lo, int(round((lo + hi) / 2 + S['sign'] * (a - mx) / span * (hi - lo) * 0.8 + r.gauss(0, (hi - lo) * 0.12))))) for a in x]
            rv = _pearson(x, y)
            if abs(rv) >= 0.5 and (rv > 0) == (S['sign'] > 0) and len(set(x)) > 3:
                break
        else:
            return None
        d = ctx(r); d['n'] = n
        intro = fill(r.choice(S['intro']), d)
        data = 'Data (' + S['xs'] + ', ' + S['ys'] + ') for each participant: ' + '; '.join(f'({a}, {b})' for a, b in zip(x, y)) + '.'
        rr = round(rv, 2)
        P = [
            lambda r: ('State the type of correlation shown by these data.', f'A {"positive" if rv > 0 else "negative"} correlation: as {S["xs"]} increases, {S["ys"]} ' + ('increases.' if rv > 0 else 'decreases.'),
                       '1 mark: direction; 1 mark: described in terms of both co-variables [2]'),
            lambda r: (f'The correlation coefficient for these data is {rr:+.2f}. Describe what this shows about the relationship.', f'A {_strength(rr)} correlation between {S["x"]} and {S["y"]}.',
                       '1 mark: direction; 1 mark: strength [2]'),
            lambda r: ('Write a non-directional hypothesis for this study.', f'There will be a correlation between {S["x"]} and {S["y"]}.',
                       '1 mark: correlation (not difference) stated; 1 mark: both co-variables operationalised [2]'),
            lambda r: ('Write a directional hypothesis for this study.', f'There will be a {"positive" if S["sign"] > 0 else "negative"} correlation between {S["x"]} and {S["y"]}.',
                       '1 mark: direction; 1 mark: both co-variables operationalised [2]'),
            lambda r: (f'Explain why {d["person"]} cannot conclude that {S["xs"]} causes the change in {S["ys"]}.',
                       f'A correlation only shows that two variables are related; neither was manipulated, so the direction of cause is unknown and a third variable, such as {r.choice(S["third"])}, could affect both.',
                       '1 mark: no manipulation / relationship only; 1 mark: third variable or direction problem explained in context [2]'),
            lambda r: ('Name the type of graph that should be used to display these data and state what would be shown on each axis.',
                       f'A scatter graph, with {S["xs"]} on one axis (x-axis) and {S["ys"]} on the other (y-axis); each participant is one point.',
                       '1 mark: scatter graph; 1 mark: axes labelled with both co-variables [2]'),
            lambda r: (f'Calculate the mean {S["xs"]}. Give your answer to one decimal place.', d1(_mean(x)), f'{sum(x)} ÷ {n} = {d1(_mean(x))} [1]'),
            lambda r: (f'Calculate the range of the {S["ys"]} scores.', str(max(y) - min(y)), f'{max(y)} − {min(y)} = {max(y) - min(y)} [1]'),
            lambda r: ('Suggest one other variable that could explain this relationship.', cap(r.choice(S['third'])) + ', which could affect both co-variables.',
                       '1 mark: plausible third variable; 1 mark: explains how it could affect both [2]'),
        ]
        if evaluative:
            P += [
                lambda r: ('Explain one strength and one weakness of using a correlation to investigate this topic.',
                           'Strength: it can study variables that could not ethically or practically be manipulated, and shows the strength and direction of a relationship. Weakness: it cannot show cause and effect, because a third variable or reversed causation could explain the link.',
                           '2 marks: strength explained; 2 marks: weakness explained [4]'),
                lambda r: ('Describe an experiment that could test whether there is a causal relationship between these variables.',
                           f'Manipulate {S["xs"]} as the IV (for example two levels, with random allocation to conditions), keep other variables constant and measure {S["ys"]} as the DV; compare the means.',
                           '1 mark: IV manipulated; 1 mark: DV measured; 1 mark: control / allocation [3]'),
            ]
        return compose(r, f'{intro} {data}', P, k=(3, 4) if evaluative else ((2, 3) if D <= 3 else (3, 4)), type_='case' if evaluative else 'numerical')
    def c3(r, D):
        return fn(r, D)
    def c4(r, D):
        return fn(r, D, True)
    c3.__name__ = 'corr_c3'; c4.__name__ = 'corr_c4'
    if C3:
        t.add('C3', C3, 'numerical')(c3)
    if C4:
        t.add('C4', C4, 'case')(c4)


def add_obs(t, S, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    """Observation with two observers. S: intro frames, cats (behavioural categories), lo/hi tallies, kind (overt/covert...), ethics list, setting."""
    def fn(r, D, evaluative=False):
        cats = r.sample(S['cats'], 4 if D >= 3 else 3)
        o1 = [r.randint(*S['tally']) for _ in cats]
        o2 = [max(0, v + r.choice([-3, -2, -1, 0, 0, 1, 2, 3])) for v in o1]
        diffs = [abs(a - b) for a, b in zip(o1, o2)]
        if diffs.count(max(diffs)) > 1 or max(diffs) == 0:
            j = r.randrange(len(cats)); o2[j] = o1[j] + r.choice([4, 5, 6]); diffs = [abs(a - b) for a, b in zip(o1, o2)]
            if diffs.count(max(diffs)) > 1:
                return None
        worst = cats[diffs.index(max(diffs))]
        d = ctx(r)
        intro = fill(r.choice(S['intro']), d)
        data = 'Tallies — ' + '; '.join(f'{c}: Observer 1 = {a}, Observer 2 = {b}' for c, a, b in zip(cats, o1, o2)) + '.'
        j = r.randrange(len(cats))
        pc = 100 * o1[j] / sum(o1)
        P = [
            lambda r: ('Calculate the total number of behaviours recorded by each observer.', f'Observer 1: {sum(o1)}; Observer 2: {sum(o2)}.', f'{" + ".join(map(str, o1))} = {sum(o1)}; {" + ".join(map(str, o2))} = {sum(o2)}. 1 mark each [2]'),
            lambda r: ('Identify the behavioural category with the lowest inter-rater reliability. Explain your answer.', f'{cap(worst)}, because the two observers’ tallies differ the most ({max(diffs)}) for this category.',
                       '1 mark: correct category; 1 mark: largest difference between the observers’ tallies [2]'),
            lambda r: (f'Calculate the percentage of Observer 1’s total that was recorded as ‘{cats[j]}’. Give your answer to one decimal place.', f'{d1(pc)}%',
                       f'{o1[j]} ÷ {sum(o1)} × 100 = {d1(pc)}%. 1 mark working; 1 mark answer [2]'),
            lambda r: ('Explain how the researcher could check the inter-rater reliability of this observation.',
                       'Both observers record the same behaviour independently at the same time using the same categories; their tallies are then correlated, and a high positive correlation (for example above +0.8) shows good inter-rater reliability.',
                       '1 mark: two observers record the same behaviour independently; 1 mark: scores compared/correlated with a high positive correlation [2]'),
            lambda r: ('Suggest one way in which the inter-rater reliability of this observation could be improved.',
                       'Operationalise each behavioural category clearly with examples, and train the observers together on practice recordings before the study so that they interpret behaviours in the same way.',
                       '1 mark: operationalised categories or training; 1 mark: explained [2]'),
            lambda r: (f'This was {S["kind"]} observation. Explain one strength of this type of observation here.', S['kind_plus'],
                       '1 mark: strength identified; 1 mark: explained in context [2]'),
            lambda r: (f'Explain one weakness of {S["kind"]} observation in this study.', S['kind_minus'], '1 mark: weakness identified; 1 mark: explained in context [2]'),
            lambda r: ('Explain why the data collected in this observation are quantitative.', 'They are numerical counts (tallies) of how often each behavioural category occurred, so they can be totalled and compared.',
                       '1 mark: numerical tallies/frequencies; 1 mark: can be analysed statistically / compared [2]'),
        ]
        if S.get('ethics'):
            P.append(lambda r: ('Explain one ethical issue raised by this observation.', cap(r.choice(S['ethics'])) + '.', '1 mark: guideline; 1 mark: applied [2]'))
        if evaluative:
            P.append(lambda r: ('Evaluate the use of a structured observation with behavioural categories in this study.',
                                'Strengths: categories make recording quick and give quantitative data that can be compared and checked for inter-rater reliability. Weaknesses: behaviour that does not fit the categories is missed, so detail and validity are lost; observers may still interpret categories differently.',
                                '2 marks: strength(s) explained; 2 marks: weakness(es) explained [4]'))
        return compose(r, f'{intro} {data}', P, k=(3, 4) if evaluative else ((2, 3) if D <= 3 else (3, 4)), type_='case' if evaluative else 'numerical')
    def c3(r, D):
        return fn(r, D)
    def c4(r, D):
        return fn(r, D, True)
    c3.__name__ = 'obs_c3'; c4.__name__ = 'obs_c4'
    if C3:
        t.add('C3', C3, 'numerical')(c3)
    if C4:
        t.add('C4', C4, 'case')(c4)


METHODS = {
    'laboratory experiment': ('a laboratory experiment', 'Manipulate the IV in a controlled room; standardised procedure and instructions; measure the DV objectively.'),
    'field experiment': ('a field experiment', 'Manipulate the IV in a natural everyday setting; participants may not know they are being studied; standardise as much of the procedure as possible.'),
    'questionnaire': ('a questionnaire', 'Closed questions (for example rating scales from 1 to 5) for quantitative data and at least one open question for qualitative detail; pilot the questions; avoid leading questions.'),
    'interview': ('an interview', 'A structured or semi-structured interview with set questions asked in the same order; record and transcribe answers; train interviewers.'),
    'observation': ('an observation', 'Structured observation with operationalised behavioural categories and time sampling; two observers to check inter-rater reliability; overt or covert as appropriate.'),
    'correlation': ('a correlation', 'Measure both co-variables for each participant (for example with a rating scale) and plot a scatter graph; look for direction and strength of the relationship.'),
}
FEATURES = {
    'laboratory experiment': ['the experimental design', 'controls', 'how the dependent variable will be measured', 'the sampling technique', 'ethical issues', 'the type of data collected'],
    'field experiment': ['the experimental design', 'controls', 'how the dependent variable will be measured', 'the sampling technique', 'ethical issues'],
    'questionnaire': ['the types of questions', 'the sampling technique', 'how the data will be analysed', 'ethical issues', 'one example question'],
    'interview': ['the type of interview', 'the sampling technique', 'one example question', 'ethical issues', 'how the data will be analysed'],
    'observation': ['the type of observation', 'behavioural categories', 'how inter-rater reliability will be checked', 'the sampling technique', 'ethical issues'],
    'correlation': ['how each co-variable will be measured', 'the sampling technique', 'a hypothesis', 'ethical issues', 'how the data will be presented'],
}


def add_plan(t, aims, D=(3, 4, 5), lead='Plan'):
    """Planning question (Paper 2 Section B / Paper 4 style). aims: [(aim, iv_or_var1, dv_or_var2, [methods])]."""
    def fn(r, D_):
        aim, v1, v2, methods = r.choice(aims)
        m = r.choice(methods)
        art, desc = METHODS[m]
        feats = r.sample(FEATURES[m], 3 if D_ <= 3 else 4)
        d = ctx(r)
        frame = r.choice([
            f'{lead} {art} to investigate {aim}.',
            f'{d["person"]} wants to find out {aim}. {lead} {art} to investigate this.',
            f'A researcher in {d["city"]} is interested in {aim}. {lead} {art} to test this.',
        ])
        stem = frame + ' Your plan must include: ' + ', '.join(feats[:-1]) + ' and ' + feats[-1] + '.'
        if D_ >= 5:
            stem += ' Then explain one weakness of your plan and how it could be overcome.'
        ans = (f'Method: {art}. {desc} Variables: {v1}; {v2}. Sample: for example an opportunity or volunteer sample of about 30 people from the target population in {d["city"]}, '
               'with reasons. Design/procedure: clear, replicable steps, with standardised instructions and random allocation or counterbalancing where relevant. '
               'Ethics: informed consent, right to withdraw, protection from harm, confidentiality and a full debrief. Data: quantitative scores summarised with means and a suitable graph; '
               'qualitative answers analysed into themes where collected.' + (' Weakness: for example a small or biased sample; overcome by a larger, more representative sample.' if D_ >= 5 else ''))
        key = ('Levels of response. Top band: a detailed, accurate and replicable plan using the stated method; all required features are included and are appropriate '
               'to the aim; variables are operationalised; ethics are addressed. Middle band: a workable plan with most required features but some lack detail or are not '
               'justified. Lower band: a basic plan with few features or with errors in method.')
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long'}
    fn.__name__ = 'plan'
    t.add('C4', D, 'long')(fn)


def build(t, P):
    """Build a topic from a knowledge pack."""
    start = len(t.templates)
    if P.get('terms'):
        add_terms(t, P['terms'], P.get('foils', ()))
    if P.get('mcq'):
        add_mcq(t, P['mcq'])
    if P.get('ar'):
        add_ar(t, P['ar'])
    if P.get('explain'):
        add_explain(t, P['explain'])
    if P.get('claims'):
        add_claims(t, P['claims'])
    if P.get('evals'):
        add_evals(t, P['who'], P['evals'])
    if P.get('apply'):
        add_apply(t, P['apply'])
    if P.get('essays'):
        add_essays(t, P['essays'])
    for S in P.get('exp', []):
        add_exp(t, S)
    for S in P.get('corr', []):
        add_corr(t, S)
    for S in P.get('obs', []):
        add_obs(t, S)
    if P.get('plan'):
        add_plan(t, P['plan'], lead=P.get('plan_lead', 'Plan'))
    for tpl in t.templates[start:]:
        if tpl.name == 'fixed':
            f = tpl.fn
            tpl.fn = (lambda f: lambda r, D: (lambda q: _marks_from_key(q) if q else q)(f(r, D)))(f)
    return t


def chapter(order, topics, study=None):
    """Register a chapter; a study-level pack (shared data/evaluation/essays) is added to every topic."""
    if study:
        for t in topics:
            build(t, study)
    CHAPTERS[order] = topics


# ============================================================== CHAPTER 1: Research methods

RM_EXP = [
    dict(intro=['{person}, a psychology student in {city}, investigated whether listening to music while revising affects memory. {n} participants learned a list of 20 words in silence and {n} different participants learned the list while music with lyrics played. Each participant then wrote down as many words as they could recall.',
                'A researcher in {city} tested the effect of background music on recall. Participants were randomly allocated to learn 20 words either in silence or with song lyrics playing, then recalled the words.'],
         A='silence', B='music with lyrics', gA='participants who learn in silence', gB='participants who learn with music with lyrics playing',
         more='will recall more words than', measure='the number of words recalled', dvshort='Number of words recalled (out of 20)',
         iv='whether participants learned the words in silence or with music with lyrics playing', dv='the number of words (out of 20) correctly recalled',
         range=(3, 20), base=(8, 11), diff=(1.5, 4), sd=2.5,
         controls=['the same list of 20 words, presented for the same time to everyone, so that list difficulty cannot explain differences',
                   'the same volume and song for everyone in the music condition, so that the IV is standardised',
                   'the same recall time (for example 2 minutes) for all participants, so that differences are not due to having more time'],
         ethics=['informed consent: participants should be told they are taking part in a memory test and agree before starting',
                 'right to withdraw: participants who find the recall test stressful should be told they can leave at any time'],
         concl_A='learning in silence leads to better recall than learning with music with lyrics.', concl_B='learning with music with lyrics leads to better recall than silence.'),
    dict(intro=['{person} wanted to know whether caffeine affects reaction time. In a laboratory in {city}, the same {n} participants were tested once after drinking a caffeinated drink and once after drinking a decaffeinated drink that tasted the same, on different days. Reaction time to a light was measured in milliseconds.',
                'In a repeated measures experiment, {n} adults in {city} completed a computer reaction-time task after a caffeinated drink and, on another day, after an identical-tasting decaffeinated drink.'],
         A='caffeinated drink', B='decaffeinated drink', gA='participants after a caffeinated drink', gB='the same participants after a decaffeinated drink',
         more='will have faster (shorter) reaction times than', measure='reaction time', dvshort='Reaction time (ms)', higher='B',
         iv='whether the drink contained caffeine or not', dv='reaction time in milliseconds to respond to a light on a screen',
         range=(180, 420), base=(240, 270), diff=(20, 55), sd=25, design='repeated measures',
         controls=['the order of conditions, by counterbalancing, so that practice on the task does not make the second condition faster',
                   'the drinks tasting the same, so that participants do not know which condition they are in (single-blind)',
                   'the time of day of testing, because alertness changes during the day'],
         ethics=['protection from harm: participants who are sensitive to caffeine or pregnant should be excluded and offered water',
                 'debriefing: participants should be told the true aim and which drink they had at the end'],
         concl_A='caffeine increases reaction time (slows responses).', concl_B='caffeine reduces reaction time (speeds responses), as the caffeinated condition had the lower mean time.'),
    dict(intro=['A psychologist in {city} investigated whether being watched affects performance on a simple task. {n} participants sorted cards alone and {n} different participants sorted cards with an audience of three people. The number of cards sorted correctly in two minutes was recorded.',
                '{person} tested social facilitation: participants were randomly allocated to sort a pack of cards either alone or in front of an audience, and the number of cards sorted correctly in two minutes was counted.'],
         A='audience', B='alone', gA='participants who sort cards in front of an audience', gB='participants who sort cards alone',
         more='will sort more cards correctly than', measure='the number of cards sorted correctly', dvshort='Cards sorted correctly in 2 minutes',
         iv='whether participants performed with an audience present or alone', dv='the number of cards sorted correctly in two minutes',
         range=(15, 60), base=(30, 36), diff=(3, 8), sd=6,
         controls=['the same pack of cards and the same sorting rule for all participants', 'the same time limit of two minutes, timed with a stopwatch',
                   'the same audience members, who stay silent and neutral, so that their behaviour is standardised'],
         ethics=['protection from harm: some participants may feel anxious in front of an audience and should be reassured and able to stop',
                 'confidentiality: individual scores should not be shown to the audience or to others'],
         concl_A='the presence of an audience improves performance on a simple task.', concl_B='the presence of an audience makes performance on a simple task worse.'),
    dict(intro=['In a field experiment in a café in {city}, {person} investigated whether a smiling server receives more help. On some days the server smiled at every customer and on other days kept a neutral expression; the number of customers (out of 30 per session) who returned their tray was counted.',
                '{person} tested whether a smile increases helping. Over {n} sessions with a smiling server and {n} sessions with a neutral server in a café in {city}, the number of customers out of 30 who returned their tray was recorded.'],
         A='smiling server', B='neutral server', gA='customers served by a smiling server', gB='customers served by a neutral server',
         more='will return more trays than', measure='the number of trays returned', dvshort='Trays returned (out of 30) per session',
         iv='whether the server smiled or kept a neutral expression', dv='the number of customers out of 30 per session who returned their tray',
         range=(3, 30), base=(10, 14), diff=(2, 6), sd=3, nosample=True,
         controls=['the same server and the same time of day for all sessions', 'the same café and the same tray-return area throughout'],
         ethics=['informed consent is not obtained in a field experiment, so the study must be harmless and in a public place where people would expect to be observed',
                 'deception: customers do not know they are in a study, so no personal information should be recorded'],
         concl_A='a smiling server encourages more helpful behaviour from customers.', concl_B='a neutral server encourages more helpful behaviour from customers.'),
    dict(intro=['{person} matched {n} pairs of students in {city} on their previous test scores. One member of each pair revised using flash cards and the other by re-reading notes. Both then took the same 40-mark test.',
                'In a matched pairs design, students in {city} were paired on prior attainment; one of each pair revised with flash cards (self-testing) and the other re-read notes, before a 40-mark test.'],
         A='flash cards', B='re-reading', gA='students who revise with flash cards', gB='students who revise by re-reading notes',
         more='will score higher on the test than', measure='test score', dvshort='Test score (out of 40)', design='matched pairs',
         iv='whether students revised with flash cards or by re-reading notes', dv='score out of 40 on the same test',
         range=(8, 40), base=(21, 25), diff=(2, 6), sd=4.5,
         controls=['the same revision time for everyone (for example 30 minutes)', 'the same test, taken under the same exam conditions'],
         ethics=['students should be offered the more effective technique afterwards, so that no one is disadvantaged',
                 'confidentiality: test scores must not be shared with teachers without consent'],
         concl_A='revising with flash cards leads to higher test scores than re-reading.', concl_B='re-reading notes leads to higher test scores than flash cards.'),
]

c1a = T('Experiments: laboratory, field and natural; independent and dependent variables', 'laboratory field natural experiments')
build(c1a, {
    'terms': [
        ('independent variable', 'the variable that the researcher manipulates or changes between conditions'),
        ('dependent variable', 'the variable that is measured to see whether it has been affected by the independent variable'),
        ('laboratory experiment', 'an experiment conducted in a controlled, artificial setting in which the researcher manipulates the IV'),
        ('field experiment', 'an experiment conducted in the participants’ normal environment in which the researcher still manipulates the IV'),
        ('natural experiment', 'a study in which the IV varies naturally (it is not manipulated by the researcher) and the DV is measured'),
        ('operationalisation', 'defining a variable precisely so that it can be manipulated or measured'),
        ('extraneous variable', 'any variable other than the IV that might affect the DV if it is not controlled'),
        ('confounding variable', 'an uncontrolled variable that has affected the DV, so the results cannot be attributed to the IV'),
    ],
    'mcq': [
        ('Which type of experiment allows the most control over extraneous variables?', 'A laboratory experiment', ['A field experiment', 'A natural experiment', 'A case study', 'A naturalistic observation'], 'Laboratory experiments take place in controlled settings with standardised procedures.'),
        ('In a natural experiment, the independent variable is', 'not manipulated by the researcher but varies naturally', ['manipulated by the researcher in a laboratory', 'controlled by random allocation', 'always measured with a questionnaire'], 'The IV is a naturally occurring difference, such as age or a change in policy.'),
        ('A researcher compares the aggression of children who do and do not watch violent cartoons at home. The IV is', 'whether or not the children watch violent cartoons', ['the children’s level of aggression', 'the age of the children', 'the number of cartoons available'], 'The IV is the variable that differs between conditions; aggression is the DV.'),
        ('Which is an advantage of a field experiment over a laboratory experiment?', 'Higher ecological validity because behaviour occurs in a natural setting', ['Better control of extraneous variables', 'Easier to replicate exactly', 'Informed consent is always obtained'], 'Natural settings make behaviour more like everyday life.'),
        ('Which is the best operationalised dependent variable for a memory study?', 'The number of words correctly recalled from a list of 20 in two minutes', ['How good each participant’s memory is', 'Whether participants enjoyed the task', 'Memory'], 'A precise, measurable definition.'),
    ],
    'ar': [
        ('Laboratory experiments can have low ecological validity.', 'They take place in artificial settings and often use tasks unlike everyday behaviour.', 'AR', 'Both true; the artificial setting and tasks are the reason for low ecological validity.'),
        ('In a natural experiment participants can be randomly allocated to conditions.', 'The researcher does not manipulate the IV in a natural experiment.', 'R', 'A is false: because the IV occurs naturally, participants cannot be randomly allocated. R is true.'),
        ('Field experiments may raise ethical problems.', 'Participants in field experiments often do not know they are being studied.', 'AR', 'Lack of consent and debriefing in natural settings causes the ethical problem.'),
    ],
    'explain': [
        ('Explain the difference between a laboratory experiment and a field experiment.', 'Both manipulate an IV, but a laboratory experiment is in a controlled, artificial environment, whereas a field experiment is in the participants’ normal environment, so it has higher ecological validity but less control.', '1 mark: setting difference; 1 mark: consequence for control or validity [2]'),
        ('Explain why a natural experiment may be used instead of a laboratory experiment.', 'Some IVs (for example a disorder, age, or a natural disaster) cannot be manipulated ethically or practically, so the researcher studies groups for whom the IV already differs; behaviour is also more natural.', '1 mark: IV cannot be manipulated (ethics/practicality); 1 mark: example or validity benefit [2]'),
        ('Explain why it is important to operationalise the dependent variable.', 'An operationalised DV is precise and measurable, so the study can be replicated and the results checked for reliability, and different researchers measure the same thing.', '1 mark: precise/measurable; 1 mark: replication or reliability [2]'),
        ('Explain how a confounding variable could reduce the validity of an experiment.', 'If an uncontrolled variable (for example time of day) differs between conditions, it could be the real cause of the change in the DV, so the researcher cannot conclude that the IV caused the effect; the experiment lacks internal validity.', '1 mark: uncontrolled variable changes the DV; 1 mark: cannot attribute effect to IV [2]'),
    ],
    'claims': [
        ('In a field experiment the researcher does not manipulate the independent variable.', False, 'The researcher still manipulates the IV in a field experiment; it is only in a natural experiment that the IV varies naturally.'),
        ('Laboratory experiments are high in reliability because their standardised procedures can be repeated.', True, 'Controlled, standardised procedures allow exact replication to check whether results are consistent.'),
        ('The dependent variable is the one that the researcher changes.', False, 'The researcher changes the IV; the DV is measured.'),
    ],
    'apply': [
        ('{person} wants to find out whether students in {city} remember more vocabulary when tested in the same room in which they learned it. Half the students learn and are tested in the same classroom; half learn in a classroom and are tested in the library.',
         [('Identify the IV and the DV in this experiment.', 'IV: whether students are tested in the same room as learning or a different room. DV: the number of vocabulary items correctly recalled.', '1 mark IV; 1 mark operationalised DV [2]'),
          ('Is this a laboratory, field or natural experiment? Explain your answer.', 'A field experiment: the IV is manipulated by the researcher but the study takes place in the students’ normal school setting.', '1 mark: field; 1 mark: reason (manipulated IV, natural setting) [2]'),
          ('Suggest one extraneous variable that {person} should control and explain how.', 'The difficulty of the vocabulary list: use the same list for all students; or time of day: test all students at the same time.', '1 mark: relevant variable; 1 mark: how to control it [2]'),
          ('Explain one strength of conducting this study in a school setting.', 'Students are in their everyday environment, so their behaviour is natural and the findings have higher ecological validity for real learning.', '1 mark: natural setting; 1 mark: ecological validity/application [2]'),
          ('Explain one weakness of conducting this study in a school setting.', 'There is less control, so extraneous variables such as noise in the library or students talking may affect recall, lowering internal validity.', '1 mark: less control; 1 mark: example and effect [2]')]),
        ('After a new timetable began in a school in {city}, {person} compared stress scores of students before the change with those of students after the change. The school, not the researcher, had decided to change the timetable.',
         [('Identify the type of experiment and explain your answer.', 'A natural experiment, because the IV (the timetable) was changed by the school, not manipulated by the researcher.', '1 mark: natural; 1 mark: reason [2]'),
          ('Explain one strength of this type of experiment for this study.', 'It allows a real-life change to be studied that the researcher could not ethically or practically create, so it has high ecological validity.', '1 mark: strength; 1 mark: context [2]'),
          ('Explain one weakness of this type of experiment for this study.', 'Participants cannot be randomly allocated, so other differences between the two groups (participant variables) could explain any difference in stress.', '1 mark: no random allocation/control; 1 mark: effect on validity [2]'),
          ('Suggest how stress could be operationalised in this study.', 'A score on a self-report stress questionnaire, such as ratings from 1 (not stressed) to 10 (very stressed), or a physiological measure such as heart rate.', '1 mark: measurable definition; 1 mark: detail of scale [2]')]),
    ],
    'essays': [
        ('laboratory experiments are the most useful method in psychology',
         ['High control of extraneous variables allows cause-and-effect conclusions.', 'Standardised procedures make replication and checking reliability possible (for example Dement and Kleitman’s use of EEG).'],
         ['Artificial settings and tasks reduce ecological validity.', 'Demand characteristics may change behaviour.', 'Some topics cannot be studied ethically in a laboratory, so natural experiments or self-reports are needed.'],
         ['ecological validity', 'reliability', 'demand characteristics', 'ethics']),
    ],
    'exp': [RM_EXP[0], RM_EXP[2]],
})

c1b = T('Experimental designs, controls and sampling techniques', 'experimental designs controls sampling techniques')
build(c1b, {
    'terms': [
        ('independent measures design', 'an experimental design in which different participants take part in each condition'),
        ('repeated measures design', 'an experimental design in which the same participants take part in every condition'),
        ('matched pairs design', 'an experimental design in which participants are paired on relevant variables and each member of a pair does a different condition'),
        ('counterbalancing', 'a control in repeated measures designs in which half the participants do the conditions in one order and half in the reverse order'),
        ('random allocation', 'placing participants into conditions so that each has an equal chance of being in any condition'),
        ('opportunity sample', 'a sample of people who are available and willing to take part at the time of the study'),
        ('volunteer sample', 'a sample of people who choose to take part, for example by responding to an advertisement'),
        ('random sample', 'a sample chosen so that every member of the target population has an equal chance of being selected'),
        ('standardisation', 'keeping procedures and instructions the same for every participant'),
    ],
    'mcq': [
        ('Which problem is most associated with a repeated measures design?', 'Order effects such as practice and fatigue', ['Participant variables between groups', 'Needing twice as many participants', 'Difficulty matching participants'], 'The same people do both conditions, so performance can change because of order.'),
        ('Which design best controls participant variables without causing order effects?', 'Matched pairs', ['Repeated measures', 'Independent measures with no random allocation', 'A case study'], 'Pairing on key variables reduces individual differences; each person does only one condition.'),
        ('A researcher puts the names of all 500 students in a college into a computer and selects 50 using a random number generator. This is', 'a random sample', ['an opportunity sample', 'a volunteer sample', 'a snowball sample'], 'Every student has an equal chance of selection.'),
        ('Which technique is used to reduce order effects?', 'Counterbalancing', ['Random sampling', 'Matched pairs', 'Single-blind procedure'], 'Counterbalancing spreads order effects equally across conditions.'),
        ('Why are standardised instructions used in an experiment?', 'So that every participant is treated in the same way and results can be compared', ['So that participants can guess the aim', 'To increase the number of participants', 'To make participants feel anxious'], 'Standardisation removes the researcher’s instructions as an extraneous variable.'),
    ],
    'ar': [
        ('Independent measures designs need more participants than repeated measures designs.', 'In an independent measures design each participant takes part in only one condition.', 'AR', 'Each person gives data for only one condition, so more people are needed.'),
        ('A volunteer sample is always representative of the target population.', 'Volunteers choose to take part themselves.', 'R', 'A is false; because volunteers self-select, the sample may be biased. R is true.'),
        ('Counterbalancing removes order effects completely.', 'Counterbalancing spreads order effects across both conditions.', 'R', 'A is false: order effects still occur but are balanced out. R is true.'),
    ],
    'explain': [
        ('Explain one advantage and one disadvantage of using an opportunity sample.', 'Advantage: quick, easy and cheap because the researcher uses whoever is available. Disadvantage: the sample is likely to be biased and unrepresentative because only people in one place at one time can be chosen.', '1 mark advantage; 1 mark disadvantage [2]'),
        ('Explain why random allocation is used in an independent measures design.', 'It means that participant variables (for example ability or motivation) are likely to be spread evenly across the conditions, so differences in the DV are more likely to be due to the IV.', '1 mark: spreads participant variables; 1 mark: so effect can be attributed to IV [2]'),
        ('Explain how demand characteristics can be reduced in a repeated measures design.', 'Because participants do both conditions they may guess the aim; using a cover story, a single-blind procedure or a long gap between conditions makes this less likely.', '1 mark: why the problem arises; 1 mark: method to reduce it [2]'),
        ('Explain the difference between a target population and a sample.', 'The target population is the whole group the researcher wants to generalise to; the sample is the smaller group selected from it who actually take part.', '1 mark each definition, contrasted [2]'),
    ],
    'claims': [
        ('A matched pairs design means the same people take part in both conditions.', False, 'That is repeated measures; in matched pairs different but similar people (matched on key variables) do each condition.'),
        ('Random sampling guarantees a representative sample.', False, 'Random sampling gives everyone an equal chance of selection, but by chance the sample can still be unrepresentative, especially if it is small.'),
        ('Participant variables are not a problem in a repeated measures design.', True, 'The same people do each condition, so individual differences are the same across conditions.'),
    ],
    'apply': [
        ('{person} is testing whether people can solve anagrams faster in the morning or in the evening. {person} plans to use the same 20 participants in both conditions, with different anagrams each time.',
         [('Name the experimental design and explain one advantage of it here.', 'Repeated measures: the same participants do both conditions, so participant variables such as vocabulary ability are controlled.', '1 mark design; 1 mark advantage in context [2]'),
          ('Explain how {person} could use counterbalancing in this study.', 'Ten participants do the morning condition first and the evening condition second; the other ten do the evening condition first, so practice effects are balanced.', '1 mark split into two orders; 1 mark purpose [2]'),
          ('Explain why the two sets of anagrams must be equally difficult.', 'If one set is easier, the difficulty of the anagrams (not the time of day) could explain the difference in solving time, so it would be a confounding variable.', '1 mark: difficulty would confound; 1 mark: cannot conclude time of day caused the effect [2]'),
          ('{person} recruits participants by asking people in the college library. Identify this sampling technique and explain one weakness.', 'Opportunity sampling; people in a library may be more studious or better at word tasks, so the sample is biased and may not represent all students.', '1 mark technique; 1 mark weakness in context [2]')]),
        ('A psychologist in {city} wants to compare two methods of reducing exam anxiety. 40 students with high anxiety scores are available. The psychologist is worried that some students are naturally more anxious than others.',
         [('Explain why a matched pairs design would be suitable.', 'Students could be paired on their initial anxiety scores and one of each pair given each method, so differences in starting anxiety are controlled and there are no order effects.', '1 mark pairing on anxiety; 1 mark benefit [2]'),
          ('Explain why a repeated measures design would not be suitable.', 'Once a student has received one anxiety-reduction method its effects would carry over to the second method, so the effects could not be separated (order/carry-over effects).', '1 mark carry-over; 1 mark consequence [2]'),
          ('Suggest one ethical issue in this study and how it could be dealt with.', 'Protection from harm: anxious students might become more distressed; they should be monitored, given the right to withdraw and offered the more effective method afterwards.', '1 mark issue; 1 mark how dealt with [2]')]),
    ],
    'essays': [
        ('repeated measures is the best experimental design',
         ['It controls participant variables because the same people do each condition.', 'Fewer participants are needed.'],
         ['Order effects (practice, fatigue) can affect results, although counterbalancing helps.', 'Participants see both conditions so may guess the aim (demand characteristics).', 'It cannot be used when the conditions involve different groups, such as males and females, or when one condition would carry over.'],
         ['order effects', 'participant variables', 'demand characteristics']),
    ],
    'exp': [RM_EXP[1], RM_EXP[4]],
})

c1c = T('Self-reports, observations, case studies and longitudinal studies', 'self-reports observations case studies longitudinal')
build(c1c, {
    'terms': [
        ('self-report', 'a method in which participants give information about themselves, for example in a questionnaire or interview'),
        ('closed question', 'a question with a fixed set of possible answers, giving quantitative data'),
        ('open question', 'a question that allows participants to answer in their own words, giving qualitative data'),
        ('social desirability bias', 'participants giving answers that make them look good rather than truthful answers'),
        ('covert observation', 'an observation in which participants do not know they are being observed'),
        ('participant observation', 'an observation in which the observer joins in with the group being observed'),
        ('case study', 'an in-depth investigation of one person or a small group, often using several methods'),
        ('longitudinal study', 'a study in which the same participants are followed and tested repeatedly over a long period of time'),
        ('structured interview', 'an interview in which the same questions are asked in the same order to every participant'),
    ],
    'mcq': [
        ('Which question would produce qualitative data?', '“Describe how you felt on your first day at college.”', ['“How many hours did you sleep last night?”', '“Rate your mood from 1 to 10.”', '“Do you own a pet? Yes/No”'], 'Open questions allow answers in participants’ own words.'),
        ('Which study used a case study of a single child?', 'Saavedra and Silverman (2002)', ['Milgram (1963)', 'Andrade (2010)', 'Piliavin et al. (1969)'], 'Saavedra and Silverman studied one 9-year-old boy with a button phobia.'),
        ('Which is a weakness of a longitudinal study?', 'Participants may drop out over time (attrition), leaving a biased sample', ['It cannot show change over time', 'Participant variables between age groups confound results', 'It only produces qualitative data'], 'Attrition is a typical problem of studies lasting months or years.'),
        ('In a covert, non-participant observation the observer', 'watches without joining in and without the participants knowing', ['joins the group and tells them they are being studied', 'interviews each participant', 'joins in secretly with the group'], 'Covert = hidden; non-participant = not a member of the group.'),
        ('Which method is most likely to be affected by social desirability bias?', 'A face-to-face interview about honesty', ['An EEG recording', 'A laboratory reaction-time test', 'A count of trays returned in a café'], 'Self-reports about sensitive topics invite answers that make people look good.'),
    ],
    'ar': [
        ('Case studies have low generalisability.', 'Case studies usually focus on one person or a very small group.', 'AR', 'A unique individual may not represent others, so findings may not generalise.'),
        ('Covert observations avoid demand characteristics.', 'In covert observations participants give informed consent.', 'A', 'A is true; R is false: covert observations do not obtain consent, which is why participants behave naturally.'),
        ('Open questions are easier to analyse than closed questions.', 'Open questions produce qualitative data.', 'R', 'A is false: qualitative answers are harder and slower to analyse. R is true.'),
    ],
    'explain': [
        ('Explain one strength and one weakness of using closed questions in a questionnaire.', 'Strength: answers are quantitative, so they are quick to analyse and compare. Weakness: participants may be forced to choose an answer that does not reflect their true view, reducing validity.', '1 mark strength; 1 mark weakness [2]'),
        ('Explain why an interviewer might choose a semi-structured interview rather than a structured interview.', 'A semi-structured interview has some set questions but lets the interviewer ask follow-up questions, so richer and more detailed answers can be obtained; it is still partly comparable across participants.', '1 mark: definition/feature; 1 mark: benefit [2]'),
        ('Explain one ethical problem with covert observation.', 'Participants have not given informed consent and may be observed in situations they would regard as private, so their privacy may be invaded; they should be debriefed where possible.', '1 mark: no consent/privacy; 1 mark: explained [2]'),
        ('Explain why case studies often produce valid data.', 'They collect rich, detailed information using several methods (interviews, observations, tests) over time, so they give an in-depth understanding of the person’s real experience.', '1 mark: rich detail/multiple methods; 1 mark: depth/real experience [2]'),
    ],
    'claims': [
        ('A longitudinal study compares different age groups at the same point in time.', False, 'That is a cross-sectional study; a longitudinal study follows the same people over time.'),
        ('In an overt observation, participants know they are being observed.', True, 'Overt means open, so participants are aware, which may cause them to change their behaviour.'),
        ('Questionnaires are always more reliable than interviews.', False, 'Standardised questionnaires can be reliable, but structured interviews can also be reliable, and poorly worded questionnaires are not.'),
    ],
    'apply': [
        ('{person} wants to find out about the sleep habits of teenagers in {city}. {person} is deciding between a questionnaire and an interview.',
         [('Write one closed question {person} could use.', 'For example: “On a school night, how many hours do you usually sleep? Less than 6 / 6–7 / 7–8 / more than 8.”', '1 mark closed format; 1 mark relevant to sleep habits [2]'),
          ('Write one open question {person} could use.', 'For example: “Describe what you usually do in the hour before going to sleep.”', '1 mark open format; 1 mark relevant [2]'),
          ('Explain one reason why the teenagers might not answer truthfully.', 'Social desirability: they may report more sleep or less phone use than is true so that they appear sensible; or they may not remember accurately.', '1 mark reason; 1 mark explained in context [2]'),
          ('Explain one advantage of a questionnaire over an interview for this study.', 'A questionnaire can be given to many teenagers quickly and anonymously, so more data are collected and answers may be more honest.', '1 mark advantage; 1 mark explained [2]')]),
        ('A researcher in {city} observes children in a school playground to study sharing behaviour. The researcher sits on a bench, unseen by the children, and records behaviour every 30 seconds.',
         [('Identify two features of this observation.', 'Covert (children do not know) and non-participant (the researcher does not join in); also naturalistic and using time sampling.', '1 mark each feature [2]'),
          ('Explain one strength of observing the children covertly.', 'The children do not know they are being watched, so they behave naturally and there are no demand characteristics, increasing validity.', '1 mark: natural behaviour; 1 mark: validity [2]'),
          ('Explain one ethical issue in this observation and how it could be dealt with.', 'Children cannot give informed consent and are not aware; consent should be obtained from the school and parents beforehand and data kept confidential.', '1 mark issue; 1 mark solution [2]'),
          ('Explain why a second observer would improve the study.', 'Two observers recording independently allow inter-rater reliability to be checked by correlating their records.', '1 mark: two independent records; 1 mark: inter-rater reliability [2]')]),
    ],
    'essays': [
        ('self-report methods are too unreliable to be useful in psychology',
         ['Participants may give socially desirable answers or misremember (for example dream reports in Dement and Kleitman).', 'Open questions may be interpreted differently by different researchers.'],
         ['Standardised questionnaires such as the AQ have good test–retest reliability.', 'Self-reports are the only way to access thoughts and feelings (for example Saavedra and Silverman’s ratings of disgust).', 'Anonymity reduces social desirability bias.'],
         ['social desirability', 'test–retest reliability', 'qualitative and quantitative data']),
    ],
    'obs': [dict(intro=['{person} carried out a structured observation of children in a playground in {city}. Two observers watched the same children for 20 minutes and tallied behaviours.',
                        'Two observers in {city} recorded children’s behaviour at a park using the same behavioural categories during the same 20-minute period.'],
                 cats=['sharing a toy', 'hitting another child', 'pushing', 'helping another child', 'shouting at another child', 'taking turns'], tally=(3, 18),
                 kind='a covert, non-participant', kind_plus='The children do not know they are being observed, so they behave naturally and demand characteristics are avoided, increasing validity.',
                 kind_minus='The observers cannot ask the children why they behaved as they did, and there are ethical issues because consent cannot be gained from the children directly.',
                 ethics=['consent: parents and the park authority should give consent, and data must be anonymous', 'privacy: children should only be observed in a public place where they might expect to be seen']),],
})

c1d = T('Correlations, data types and descriptive statistics (mean, median, mode, range, standard deviation)', 'correlations data types descriptive statistics mean median mode range standard deviation')
build(c1d, {
    'terms': [
        ('positive correlation', 'a relationship in which, as one co-variable increases, the other also increases'),
        ('negative correlation', 'a relationship in which, as one co-variable increases, the other decreases'),
        ('median', 'the middle value when all scores are placed in rank order'),
        ('mode', 'the most frequently occurring score in a set of data'),
        ('range', 'the difference between the highest and lowest scores in a set of data'),
        ('standard deviation', 'a measure of how spread out scores are around the mean'),
        ('qualitative data', 'descriptive data in words, pictures or other non-numerical forms'),
        ('quantitative data', 'numerical data, for example scores, counts or measurements'),
    ],
    'foils': ['interval data', 'nominal data'],
    'mcq': [
        ('Which correlation coefficient shows the strongest relationship?', '−0.85', ['+0.45', '+0.10', '−0.30'], 'The sign gives direction; the size (closest to 1) gives strength.'),
        ('Which measure of central tendency is affected most by an extreme score?', 'The mean', ['The median', 'The mode', 'None of them'], 'The mean uses every value, so one extreme value distorts it.'),
        ('Which type of data are the categories “helped” and “did not help”?', 'Nominal data', ['Ordinal data', 'Interval data', 'Ratio data'], 'Named categories with no order are nominal.'),
        ('Which graph should be used to display data from a correlational study?', 'A scatter graph', ['A bar chart', 'A pie chart', 'A table of means'], 'Each point represents a participant’s scores on two co-variables.'),
        ('A large standard deviation shows that', 'scores are widely spread around the mean', ['scores are all close to the mean', 'the mean is high', 'the data are qualitative'], 'SD measures spread around the mean.'),
        ('The scores 4, 6, 6, 7, 12 have a mode of', '6', ['7', '12', '8'], '6 occurs most often (twice).'),
    ],
    'ar': [
        ('A correlation cannot show cause and effect.', 'In a correlation neither co-variable is manipulated.', 'AR', 'Without manipulation, a third variable or reversed causation could explain the relationship.'),
        ('The median is the best measure of central tendency for data with an outlier.', 'The median uses the value of every score in its calculation.', 'A', 'A is true; R is false: the median is not calculated from every value, which is why it is not distorted.'),
        ('The range is a weak measure of spread.', 'The range only uses the highest and lowest scores.', 'AR', 'Using only two scores makes the range easily distorted by an extreme value.'),
    ],
    'explain': [
        ('Explain one strength and one weakness of the mean as a measure of central tendency.', 'Strength: it uses every score, so it is the most sensitive measure. Weakness: it is distorted by extreme scores (outliers).', '1 mark strength; 1 mark weakness [2]'),
        ('Explain why a standard deviation is more informative than the range.', 'The standard deviation uses every score to show the average spread around the mean, whereas the range uses only the highest and lowest values and so is distorted by one extreme score.', '1 mark: SD uses all scores; 1 mark: range only two scores/outliers [2]'),
        ('Explain one strength of collecting qualitative data.', 'Qualitative data give rich, detailed descriptions of thoughts and feelings in the participants’ own words, so they may have higher validity.', '1 mark: rich detail; 1 mark: validity/insight [2]'),
        ('Explain the difference between a correlation and an experiment.', 'In an experiment the researcher manipulates an IV and measures a DV, so cause and effect can be inferred; in a correlation two co-variables are measured and the strength and direction of their relationship is found, but cause cannot be inferred.', '1 mark experiment; 1 mark correlation contrasted [2]'),
    ],
    'claims': [
        ('A correlation coefficient of −0.9 shows a weak relationship because the number is negative.', False, 'The sign shows direction only; −0.9 is a strong negative correlation.'),
        ('The median of 3, 8, 5, 10 is 6.5.', True, 'In order: 3, 5, 8, 10; the median is (5 + 8) ÷ 2 = 6.5.'),
        ('Qualitative data are easier to analyse than quantitative data.', False, 'Qualitative data must be interpreted or coded into themes, which is slow and can be subjective.'),
    ],
    'essays': [
        ('quantitative data are more useful than qualitative data in psychology',
         ['Quantitative data are objective and easy to analyse and compare, for example percentages of help in Piliavin et al.', 'They allow statistical analysis and checks of reliability.'],
         ['Qualitative data give depth and explain why people behave as they do, for example Milgram’s descriptions of tension.', 'Numbers can oversimplify experiences such as phobias.', 'Many studies combine both types for a fuller picture.'],
         ['objectivity', 'validity', 'examples from core studies']),
    ],
    'corr': [
        dict(intro=['{person} investigated whether the number of hours students in {city} spend on social media each day is related to their score on a sleep-quality questionnaire (0–30, higher = better sleep). {n} students took part.',
                    'A correlational study in {city} measured daily social-media use (hours) and sleep-quality score (0–30) for {n} students.'],
             x='daily hours spent on social media', y='sleep-quality score', xs='social-media hours', ys='sleep-quality score', xr=(0, 8), yr=(4, 28), sign=-1,
             third=['stress about school work', 'having a part-time job', 'caffeine intake']),
        dict(intro=['A researcher in {city} measured how many hours {n} students revised for a psychology test and their test score out of 50.',
                    '{person} recorded revision hours and test score (out of 50) for {n} students in a college in {city}.'],
             x='hours spent revising', y='test score out of 50', xs='revision hours', ys='test score', xr=(1, 12), yr=(10, 48), sign=1,
             third=['motivation to succeed', 'previous knowledge of psychology', 'quality of sleep before the test']),
    ],
    'exp': [RM_EXP[3]],
})

c1e = T('Hypotheses, reliability, validity, generalisability and ethical guidelines (BPS, animal research)', 'hypotheses reliability validity generalisability ethical guidelines bps animal research')
build(c1e, {
    'terms': [
        ('null hypothesis', 'a prediction that there will be no difference or no relationship between the variables'),
        ('test–retest reliability', 'the consistency of a measure when the same participants are tested on two occasions'),
        ('inter-rater reliability', 'the consistency between two or more observers or raters scoring the same behaviour'),
        ('ecological validity', 'the extent to which findings can be applied to real-life settings'),
        ('demand characteristics', 'features of a study that allow participants to guess the aim and change their behaviour'),
        ('generalisability', 'the extent to which findings from a sample can be applied to the wider population'),
        ('informed consent', 'agreement to take part given by a participant who knows what the study involves'),
        ('debriefing', 'explaining the true aims of a study to participants at the end and returning them to their original state'),
        ('right to withdraw', 'the participant’s right to leave a study at any time, including removing their data'),
    ],
    'mcq': [
        ('Which guideline concerns telling participants the true aim of the study when it is over?', 'Debriefing', ['Confidentiality', 'Informed consent', 'Protection from harm'], 'The debrief explains the aim and checks participant well-being.'),
        ('Which is a directional (one-tailed) hypothesis?', 'Students who sleep for 8 hours will recall more words than students who sleep for 4 hours.', ['There will be a difference in recall between students who sleep 8 hours and 4 hours.', 'There will be no difference in recall between students who sleep 8 or 4 hours.', 'Sleep affects memory in some way.'], 'A directional hypothesis predicts which condition will be higher.'),
        ('Which of these is one of the “3 Rs” for animal research?', 'Reduction: using the fewest animals possible', ['Rejection: refusing to use animals', 'Reinforcement: rewarding animals for taking part', 'Recording: filming all animals'], 'Replacement, Reduction and Refinement.'),
        ('A questionnaire gives similar scores when the same people complete it two weeks apart. This shows good', 'test–retest reliability', ['inter-rater reliability', 'ecological validity', 'generalisability'], 'Consistent scores over time = test–retest reliability.'),
        ('Which is a threat to the validity of a study?', 'Participants guessing the aim and behaving to please the researcher', ['Using standardised instructions', 'Using a large, varied sample', 'Two observers agreeing closely'], 'Demand characteristics reduce validity.'),
    ],
    'ar': [
        ('Deception can sometimes be acceptable in psychological research.', 'Some behaviour would change if participants knew the true aim.', 'AR', 'The BPS allows deception when it is necessary, harmless and followed by debriefing.'),
        ('Animal studies always generalise to humans.', 'Animals and humans share some biological processes.', 'R', 'A is false: there are important differences in brains, cognition and culture. R is true.'),
        ('A study can be reliable but not valid.', 'Reliability concerns consistency, whereas validity concerns whether the study measures what it intends to measure.', 'AR', 'A measure can be consistently wrong.'),
    ],
    'explain': [
        ('Explain the difference between reliability and validity.', 'Reliability is consistency: a study or measure gives the same results when repeated. Validity is accuracy: the study measures what it claims to measure and its findings are true and apply to real life.', '1 mark reliability; 1 mark validity [2]'),
        ('Explain why animal research must follow the principle of refinement.', 'Refinement means changing procedures to reduce pain, distress and suffering, for example better housing or less invasive measures; this protects animal welfare and is required by ethical guidelines.', '1 mark: definition; 1 mark: purpose/example [2]'),
        ('Explain how a single-blind procedure can increase validity.', 'Participants do not know which condition they are in, so they cannot change their behaviour to fit the expected result; demand characteristics are reduced.', '1 mark: participants unaware of condition; 1 mark: reduces demand characteristics [2]'),
        ('Explain why psychologists should protect participants’ confidentiality.', 'Personal data could embarrass or harm participants if identified; keeping data anonymous protects them and maintains trust in research.', '1 mark: what confidentiality is; 1 mark: why [2]'),
    ],
    'claims': [
        ('A null hypothesis predicts that the IV will have an effect on the DV.', False, 'A null hypothesis predicts no difference or relationship.'),
        ('Inter-rater reliability can be checked by correlating two observers’ scores.', True, 'A high positive correlation between the observers’ records shows good inter-rater reliability.'),
        ('Children can give their own informed consent to take part in research.', False, 'Children under 16 cannot give fully informed consent, so parental consent is needed as well as the child’s agreement.'),
    ],
    'apply': [
        ('{person} designs a questionnaire to measure stress in office workers in {city}. {person} gives the questionnaire to 30 workers on Monday and again to the same workers two weeks later.',
         [('Identify the type of reliability being tested and explain how.', 'Test–retest reliability: the two sets of scores are correlated; a strong positive correlation shows the questionnaire is consistent over time.', '1 mark type; 1 mark how [2]'),
          ('Explain one reason why the scores might not be consistent even if the questionnaire is reliable.', 'Workers’ real stress levels may have changed in two weeks (for example a deadline passed), so differences may reflect genuine change.', '1 mark reason; 1 mark explained [2]'),
          ('Explain one way to check the validity of the questionnaire.', 'Compare scores with another established measure of stress or a physiological measure such as cortisol level; if they agree, it has concurrent validity.', '1 mark method; 1 mark explained [2]'),
          ('Describe two ethical guidelines {person} should follow.', 'Informed consent before starting; confidentiality so that managers cannot see individual answers; right to withdraw.', '1 mark each guideline applied [2]')]),
        ('A researcher in {city} plans to study learning in rats by rewarding them with food for pressing a lever. The rats will be kept in cages in a laboratory for several weeks.',
         [('Explain how the researcher could apply the principle of reduction.', 'Use the smallest number of rats needed to obtain valid results, for example by using a good experimental design and statistics.', '1 mark: fewest animals; 1 mark: how [2]'),
          ('Explain how the researcher could apply the principle of refinement.', 'Provide suitable housing with companions and enrichment, handle rats gently and avoid food deprivation that causes distress.', '1 mark: reduce suffering; 1 mark: example [2]'),
          ('Explain one reason why findings from rats may not generalise to humans.', 'Human learning involves cognition, language and culture, so results from rats pressing levers may not explain complex human behaviour.', '1 mark difference; 1 mark consequence [2]')]),
    ],
    'essays': [
        ('the use of animals in psychological research can be justified',
         ['Animals allow research that would be unethical with humans, for example Hassett et al.’s study of toy preference without socialisation.', 'Findings can improve animal welfare, such as Fagen et al.’s positive-reinforcement training of elephants.', 'Guidelines (the 3 Rs) reduce suffering.'],
         ['Animals cannot consent and may suffer stress.', 'Findings may not generalise to humans because of differences in cognition and culture.', 'Alternatives such as computer models or human volunteers may be possible.'],
         ['the 3 Rs', 'generalisability', 'core studies using animals']),
        ('validity is more important than reliability in psychological research',
         ['A consistent but inaccurate measure is useless.', 'Ecologically valid studies such as Piliavin et al. tell us about real behaviour.'],
         ['Without reliability, results cannot be checked or trusted.', 'Standardised laboratory procedures (for example Milgram) allow replication.', 'Both are needed and are linked.'],
         ['ecological validity', 'test–retest and inter-rater reliability', 'standardisation']),
    ],
    'exp': [RM_EXP[4]],
    'plan': [
        ('whether eating breakfast affects concentration in students', 'IV: breakfast or no breakfast', 'DV: score on a 10-minute concentration task', ['laboratory experiment', 'field experiment']),
        ('whether there is a relationship between hours of exercise per week and self-rated mood', 'co-variable 1: hours of exercise per week', 'co-variable 2: mood rating from 1 to 10', ['correlation', 'questionnaire']),
        ('how often people hold doors open for others in a shopping centre', 'behaviour: holding the door', 'categories: holding door, not holding, thanking', ['observation']),
        ('students’ attitudes to homework', 'topic: attitudes to homework', 'measure: ratings and open answers', ['questionnaire', 'interview']),
    ],
})

CHAPTERS[1] = [c1a, c1b, c1c, c1d, c1e]


def add_tally_pct(t, intro, rows, labels, C=('C3', (2, 3, 4, 5)), extra=()):
    """Frequency table -> percentage calculations. rows: [(row label, (lo, hi) for col 1, (lo, hi) for col 2)], labels: (col1, col2, what)."""
    def fn(r, D):
        d = ctx(r)
        k = r.choice([3, 4]) if D >= 3 else 2
        rs = r.sample(rows, min(k, len(rows)))
        data = [(lab, r.randint(*a), r.randint(*b)) for lab, a, b in rs]
        c1, c2, what = labels
        tbl = '; '.join(f'{lab}: {c1} {x}, {c2} {y}' for lab, x, y in data)
        P = []
        lab, x, y = r.choice(data)
        P.append(lambda r_: (f'Calculate the percentage of {what} for {lab} that were “{c1}”. Give your answer to one decimal place.', f'{d1(100 * x / (x + y))}%',
                             f'{x} ÷ ({x} + {y}) × 100 = {x} ÷ {x + y} × 100 = {d1(100 * x / (x + y))}%. 1 mark working; 1 mark answer [2]'))
        tx, ty = sum(v[1] for v in data), sum(v[2] for v in data)
        P.append(lambda r_: (f'Calculate the overall percentage of {what} in the table that were “{c1}”.', f'{d1(100 * tx / (tx + ty))}%',
                             f'Total “{c1}” = {tx}; total = {tx + ty}; {tx} ÷ {tx + ty} × 100 = {d1(100 * tx / (tx + ty))}%. 1 mark totals; 1 mark answer [2]'))
        best = max(data, key=lambda v: v[1] / (v[1] + v[2]))
        if sum(1 for v in data if abs(v[1] / (v[1] + v[2]) - best[1] / (best[1] + best[2])) < 1e-9) == 1:
            P.append(lambda r_: (f'Identify which row has the highest proportion of “{c1}” {what}. Show how you worked this out.', f'{best[0]} ({d1(100 * best[1] / (best[1] + best[2]))}%)',
                                 '1 mark: percentages (or proportions) calculated for each row; 1 mark: correct row identified [2]'))
        return compose(r, fill(r.choice(intro), d) + ' ' + tbl + '.', P + [lambda r_, p=p: (fill(p[0], d), fill(p[1], d), p[2]) for p in extra], k=(2, 3), type_='numerical')
    fn.__name__ = 'tally_pct'
    t.add(C[0], C[1], 'numerical')(fn)



# ============================================================== CHAPTER 2: Dement and Kleitman (1957)

DK = 'Dement and Kleitman’s (1957) study of sleep and dreams'
DK_STUDY = {
    'who': DK,
    'evals': [
        ('the use of EEG', 'strength', 'The EEG and eye-movement recordings were objective, quantitative measures, so REM and NREM sleep were identified scientifically rather than by the researchers’ opinion; this increases validity and reliability.'),
        ('standardisation', 'strength', 'All participants followed the same procedure: they avoided caffeine and alcohol, arrived at their usual bedtime, were woken by a doorbell and spoke into a recording device, so the study can be replicated.'),
        ('quantitative data', 'strength', 'The number of awakenings with dream recall could be compared directly: 152 of 191 REM awakenings versus 11 of 160 NREM awakenings gave clear support for the link between REM and dreaming.'),
        ('ecological validity', 'weakness', 'Participants slept in a laboratory attached to electrodes and were woken by a doorbell several times a night, so their sleep and dreaming may not be the same as at home.'),
        ('generalisability', 'weakness', 'Only nine adults took part (seven men and two women), and five were studied intensively, so the sample is small and may not represent everyone’s sleep.'),
        ('the validity of dream reports', 'weakness', 'Dream recall was self-reported: participants may have forgotten or reconstructed details on waking, and judging whether a coherent dream was reported involved some interpretation.'),
        ('ethics', 'weakness', 'Being woken repeatedly during the night disrupted participants’ sleep, which could cause tiredness and distress the next day, so they needed the right to withdraw.'),
        ('ethics', 'strength', 'Participants were volunteers who knew they would be woken and recorded; the procedure was not physically harmful and the data were kept confidential.'),
    ],
    'essays': [
        ('dreaming can be studied scientifically',
         ['Dement and Kleitman used EEG and eye-movement recordings, which are objective and allow REM to be identified reliably.', 'Hypotheses were tested with controlled awakenings and quantitative comparisons (REM versus NREM recall).'],
         ['The content of dreams can only be known through self-report, which may be inaccurate or reconstructed.', 'The laboratory setting may change how people sleep and dream.', 'Eye movements and dream content were matched by interpretation.'],
         ['objectivity', 'self-report', 'ecological validity']),
        ('the biological approach provides the best explanation of dreaming',
         ['Dreaming is strongly associated with a measurable physiological state (REM sleep) that occurs in regular cycles.', 'Eye movements appeared to match the visual content of dreams.'],
         ['Biological measures do not explain the meaning or content of dreams.', 'Some dreams were recalled after NREM awakenings.', 'Psychological factors such as recent experiences also shape dream content.'],
         ['reductionism', 'REM sleep', 'nature versus nurture']),
    ],
    'exp': [dict(intro=['A sleep laboratory in {city} replicated part of Dement and Kleitman’s study. {n} volunteers were each woken ten times during REM sleep and ten times during NREM sleep on different nights, and the number of awakenings on which a dream was recalled was recorded.',
                        '{person} repeated Dement and Kleitman’s procedure with {n} participants in {city}: each was woken ten times from REM sleep and ten times from NREM sleep, and dream recall was recorded.'],
                 A='REM awakenings', B='NREM awakenings', gA='participants woken from REM sleep', gB='the same participants woken from NREM sleep',
                 more='will recall dreams on more awakenings than', measure='the number of awakenings with dream recall', dvshort='Awakenings with a dream recalled (out of 10)',
                 iv='whether participants were woken from REM or NREM sleep', dv='the number of awakenings out of 10 on which a coherent dream was reported',
                 range=(0, 10), base=(0.6, 2), diff=(5, 6.5), sd=1.1, design='repeated measures',
                 controls=['no caffeine or alcohol on the day of the study, because these affect sleep', 'the same waking method (a doorbell) for every awakening, so that the way of waking does not affect recall',
                           'waking participants in a random order of REM and NREM, so that they cannot learn the pattern'],
                 ethics=['protection from harm: repeated waking disrupts sleep, so participants should be allowed to withdraw', 'confidentiality: dream content may be personal and should be kept anonymous'],
                 concl_A='dreaming is much more likely to be recalled from REM sleep than from NREM sleep.', concl_B='dreaming is more likely to be recalled from NREM sleep.')],
    'corr': [dict(intro=['Researchers in {city} woke {n} participants after periods of REM sleep of different lengths and counted the number of words in each dream report.',
                         '{person} measured the length of the REM period (minutes) before waking and the number of words in the dream narrative for {n} awakenings.'],
                  x='the length of the REM period before waking (minutes)', y='the number of words in the dream narrative', xs='REM duration', ys='number of words in the narrative', xr=(3, 30), yr=(20, 300), sign=1,
                  third=['how sleepy the participant was on waking', 'the participant’s general vocabulary or talkativeness', 'how vivid the dream was'])],
    'plan': [('whether people who are woken from REM sleep report more vivid dreams than people woken from NREM sleep', 'IV: REM or NREM awakening', 'DV: vividness rating 1–10', ['laboratory experiment']),
             ('whether the number of hours slept is related to the number of dreams recalled in a dream diary', 'co-variable 1: hours slept', 'co-variable 2: dreams recalled per week', ['correlation', 'questionnaire'])],
}

c2a = T('Background: REM and NREM sleep, EEG and the biological approach', 'rem nrem sleep eeg biological approach')
build(c2a, {
    'terms': [
        ('REM sleep', 'a stage of sleep with rapid eye movements, fast low-voltage EEG activity similar to waking, and the most vivid dreaming'),
        ('NREM sleep', 'the stages of sleep without rapid eye movements, including deep sleep with slow, high-voltage EEG waves'),
        ('electroencephalograph (EEG)', 'a machine that records the electrical activity of the brain using electrodes placed on the scalp'),
        ('electro-oculogram (EOG)', 'a recording of eye movements using electrodes placed around the eyes'),
        ('sleep cycle', 'the repeating pattern of NREM and REM stages that occurs roughly every 90 minutes during the night'),
        ('biological approach', 'the view that behaviour and experience can be explained by physiology, such as the brain, nervous system, hormones and genes'),
    ],
    'foils': ['hypnagogic state', 'circadian rhythm'],
    'mcq': [
        ('In which stage of sleep are vivid dreams most likely to be reported?', 'REM sleep', ['Stage 1 NREM sleep', 'Stage 3 (deep) NREM sleep', 'The hypnagogic state on falling asleep'], 'Dement and Kleitman found most dream recall from REM awakenings.'),
        ('What does an EEG record?', 'Electrical activity of the brain', ['Heart rate', 'Hormone levels in the blood', 'Muscle strength'], 'EEG = electroencephalograph; scalp electrodes detect brain activity.'),
        ('Roughly how often does a sleep cycle repeat during the night?', 'About every 90 minutes', ['About every 10 minutes', 'About every 4 hours', 'Once a night'], 'REM periods recur at regular intervals of roughly 90 minutes.'),
        ('Which EEG pattern is typical of REM sleep?', 'Fast, low-voltage activity similar to being awake', ['Slow, high-voltage delta waves', 'No electrical activity', 'Sleep spindles and K-complexes only'], 'REM is sometimes called paradoxical sleep because the EEG resembles waking.'),
    ],
    'ar': [
        ('Dement and Kleitman’s study belongs to the biological approach.', 'It measured physiological activity (brain waves and eye movements) to investigate dreaming.', 'AR', 'Physiological measurement is the reason it is biological.'),
        ('REM sleep is the deepest stage of sleep.', 'In REM sleep the EEG shows fast, low-voltage activity.', 'R', 'A is false (stages 3–4 NREM are deepest); R is true.'),
    ],
    'explain': [
        ('Explain the difference between REM and NREM sleep.', 'REM sleep has rapid eye movements, fast low-voltage EEG activity and vivid dreams; NREM sleep has no rapid eye movements and, in deep stages, slow high-voltage waves with little dream recall.', '1 mark REM; 1 mark NREM, contrasted [2]'),
        ('Explain why an EEG is a useful tool for studying sleep.', 'It gives an objective, continuous record of brain activity, so stages of sleep can be identified without waking the sleeper or relying on self-report.', '1 mark objective; 1 mark identifies stages/no self-report [2]'),
        ('Explain why Dement and Kleitman’s study is an example of the biological approach.', 'It explains a psychological experience (dreaming) in terms of physiological activity, using EEG measures of brain waves and eye movements.', '1 mark physiological explanation; 1 mark EEG/eye movement evidence [2]'),
    ],
    'claims': [
        ('People only dream in REM sleep.', False, 'Dreams are much more likely to be recalled from REM, but some dream reports occur after NREM awakenings (11 of 160 in Dement and Kleitman).'),
        ('During REM sleep the brain is very active even though the body is asleep.', True, 'The EEG during REM is fast and low voltage, similar to the waking brain.'),
        ('Eye movements during sleep can be measured with an EEG.', True, 'Electrodes near the eyes (an EOG recording, part of the EEG set-up) detect eye movements.'),
    ],
    'apply': [
        ('{person} is spending a night in a sleep clinic in {city}. The EEG shows slow, high-voltage waves for 40 minutes, followed later by fast, low-voltage activity with rapid eye movements.',
         [('Identify the stage of sleep shown by the slow, high-voltage waves.', 'Deep (stage 3/4) NREM sleep.', '1 mark [1]'),
          ('Identify the stage shown by the fast, low-voltage activity with rapid eye movements, and state what {person} is likely to report if woken then.', 'REM sleep; {person} is likely to report a vivid dream.', '1 mark REM; 1 mark dream recall [2]'),
          ('Explain why researchers record eye movements as well as brain waves.', 'Rapid eye movements distinguish REM from other stages with similar EEG (such as stage 1), so REM can be identified accurately.', '1 mark distinguishes REM; 1 mark accuracy [2]'),
          ('Explain one reason why {person}’s sleep in the clinic may not represent normal sleep.', 'The unfamiliar setting, electrodes and wires may make it harder to sleep normally (first-night effect), lowering ecological validity.', '1 mark reason; 1 mark explained [2]')]),
    ],
})

c2b = T('Procedure and results: eye movements and dream recall', 'procedure results eye movements dream recall')
build(c2b, {
    'mcq': [
        ('How many adult participants took part in Dement and Kleitman’s study?', 'Nine (seven men and two women)', ['Five women', 'Forty men', 'Twenty students of each sex'], 'Nine adults; five were studied intensively.'),
        ('How were participants woken in Dement and Kleitman’s study?', 'By a doorbell ringing near the bed', ['By the researcher shaking them', 'By a bright light', 'By an alarm clock they set themselves'], 'The doorbell was loud enough to wake them, and they spoke into a recorder.'),
        ('Out of 191 awakenings from REM sleep, on how many did participants recall a dream?', '152', ['11', '39', '160'], '152 of 191 REM awakenings (about 80%) produced dream recall.'),
        ('Out of 160 awakenings from NREM sleep, on how many did participants recall a dream?', '11', ['152', '149', '92'], 'Only 11 of 160 NREM awakenings (about 7%) produced dream recall.'),
        ('Participants were woken after 5 or 15 minutes of REM and asked to estimate which. What did they find?', 'Most estimates were correct', ['Estimates were no better than chance', 'Participants always chose 15 minutes', 'No one could make an estimate'], '92 of 111 estimates were correct.'),
        ('A participant whose eyes moved mainly vertically reported a dream about', 'looking up and down at climbers on a cliff', ['two people throwing tomatoes at each other', 'driving a car and staring ahead', 'sitting in a dark room'], 'Vertical movements matched looking up and down in the dream.'),
        ('What were participants asked to avoid on the day of the study?', 'Alcohol and caffeine', ['Food after midday', 'Exercise of any kind', 'Talking to others'], 'Both affect sleep, so they were controlled.'),
    ],
    'ar': [
        ('Dement and Kleitman found a positive relationship between REM duration and the length of dream reports.', 'The number of words in dream narratives tended to be greater after longer REM periods.', 'AR', 'Longer REM → longer narratives (significant for four of five participants).'),
        ('Participants in Dement and Kleitman’s study were always told whether they were being woken from REM or NREM.', 'Researchers wanted to avoid demand characteristics.', 'R', 'A is false: participants were not told (and one was misled); avoiding expectations is the reason. R is true.'),
    ],
    'explain': [
        ('Describe the three aims (hypotheses) of Dement and Kleitman’s study.', 'To test whether (1) dream recall is greater after REM awakenings than NREM awakenings; (2) the estimated length of a dream relates to the length of the REM period; (3) the pattern of eye movements relates to the content of the dream.', '1 mark for each aim [3]'),
        ('Describe how the duration of dreams was investigated in Dement and Kleitman’s study.', 'Participants were woken after either 5 or 15 minutes of REM sleep and asked to say which they thought it was; the number of words in their dream report was also counted and compared with REM length.', '1 mark: 5 or 15 minutes; 1 mark: estimate; 1 mark: word count/correlation [3]'),
        ('Describe the findings about eye movements and dream content.', 'Mainly vertical eye movements matched dreams of looking up and down (such as climbers on a cliff, or climbing ladders); horizontal movements matched watching two people throw tomatoes at each other; few movements matched watching something far away, such as driving.', '1 mark vertical; 1 mark horizontal; 1 mark little/no movement [3]'),
        ('Explain what Dement and Kleitman concluded from their results.', 'Dreaming is closely associated with REM sleep, so REM is an objective indicator of dreaming; dream length relates to REM duration and eye movements may relate to what the dreamer is “looking at”.', '1 mark REM–dreaming; 1 mark duration or eye movement link [2]'),
    ],
    'claims': [
        ('Dement and Kleitman found that dream recall was equally likely from REM and NREM sleep.', False, 'Recall was reported on about 80% of REM awakenings but only about 7% of NREM awakenings.'),
        ('Participants in the study spoke their dream reports into a recording device.', True, 'This allowed the experimenter to listen later without influencing the report.'),
        ('REM periods in the study occurred at regular intervals during the night.', True, 'REM recurred in cycles, roughly every 90 minutes, and became longer later in the night.'),
    ],
})
add_tally_pct(c2b, ['The table shows the results of awakenings for some participants in a replication of Dement and Kleitman’s study in {city}.', '{person} recorded whether a dream was recalled on each awakening for several participants.'],
              [('Participant A (REM)', (12, 22), (1, 6)), ('Participant B (REM)', (14, 26), (2, 7)), ('Participant C (NREM)', (0, 3), (14, 26)), ('Participant D (NREM)', (1, 4), (12, 24)), ('Participant E (REM)', (8, 18), (3, 8))],
              ('dream recalled', 'no dream recalled', 'awakenings'))

c2c = T('Evaluation: validity, reliability, ecological validity and ethics', 'evaluation validity reliability ecological validity ethics')
build(c2c, {
    'mcq': [
        ('Which is the best example of a control in Dement and Kleitman’s study?', 'Participants avoided alcohol and caffeine on the day of the study', ['Participants chose when to be woken', 'Participants slept at home', 'Participants were woken by different methods each time'], 'Controlling substances that affect sleep.'),
        ('Why might Dement and Kleitman’s study lack ecological validity?', 'Participants slept in a laboratory with electrodes attached and were woken repeatedly', ['It used EEG recordings', 'It used quantitative data', 'It had a standardised procedure'], 'The setting and procedure were unlike normal sleep.'),
        ('Which feature of the study increased its reliability?', 'A standardised procedure that could be repeated with every participant', ['A small sample of nine adults', 'Dream reports in participants’ own words', 'Sleeping in an unfamiliar room'], 'Standardisation allows replication.'),
    ],
    'ar': [
        ('Dream reports in Dement and Kleitman’s study may lack validity.', 'Dream reports are self-reports given immediately on waking.', 'AnR', 'Both true, but immediacy is a strength; the validity problem is that reports can still be forgotten or reconstructed.'),
    ],
    'explain': [
        ('Explain why the small sample in Dement and Kleitman’s study is a weakness.', 'With only nine adults (mostly male), individual differences in sleep could strongly affect the results, and the findings may not generalise to women, children or the wider population.', '1 mark small/unrepresentative; 1 mark consequence for generalisation [2]'),
        ('Explain one way in which Dement and Kleitman tried to avoid demand characteristics.', 'Participants were not told whether they had been woken from REM or NREM sleep, and the experimenter did not speak to them while they recorded their dream, so they could not tailor their reports.', '1 mark method; 1 mark how it reduces demand characteristics [2]'),
        ('Explain one practical application of Dement and Kleitman’s findings.', 'Because REM can be identified objectively by EEG and eye movements, sleep clinics can study dreaming and diagnose sleep disorders without relying only on self-report.', '1 mark application; 1 mark link to findings [2]'),
    ],
    'claims': [
        ('Because EEG recordings are objective, Dement and Kleitman’s whole study was free of subjectivity.', False, 'The physiological recordings were objective, but dream recall depended on self-report and the researchers judged whether a coherent dream was reported.'),
        ('Waking participants several times a night raises an ethical issue about protection from harm.', True, 'Sleep disruption may cause tiredness or distress, so participants should be informed and able to withdraw.'),
    ],
    'apply': [
        ('{person} reads that Dement and Kleitman’s participants slept in a laboratory with electrodes on their scalp and near their eyes.',
         [('Explain how this could reduce the validity of the findings.', 'Sleeping in an unfamiliar place with electrodes may change normal sleep patterns and dreaming, so findings may not reflect typical sleep (low ecological validity).', '1 mark artificial setting; 1 mark effect on sleep/validity [2]'),
          ('Suggest how a modern researcher could investigate dreaming with higher ecological validity.', 'Use portable home EEG devices or smartphone apps so participants sleep in their own beds, and keep a dream diary on waking.', '1 mark method; 1 mark why more natural [2]'),
          ('Explain one problem with the method you have suggested.', 'Home recordings are less controlled (noise, partners, caffeine use) and dream diaries rely on accurate recall, so reliability may be lower.', '1 mark problem; 1 mark explained [2]')]),
    ],
})
chapter(2, [c2a, c2b, c2c], DK_STUDY)


# ============================================================== CHAPTER 3: Hassett et al. (2008)

HA = 'Hassett et al.’s (2008) study of monkey toy preferences'
HA_STUDY = {
    'who': HA,
    'evals': [
        ('controls', 'strength', 'Each test paired one wheeled and one plush toy, and different toys were used across sessions, so the preference was for the category of toy rather than one particular object.'),
        ('ecological validity', 'strength', 'The monkeys lived in a large social troop in an outdoor enclosure and were observed with their normal social group, so their behaviour was relatively natural.'),
        ('quantitative data', 'strength', 'Frequency and duration of interactions with each toy were recorded from video, so preferences of males and females could be compared objectively.'),
        ('generalisability', 'weakness', 'The findings come from rhesus monkeys, whose brains and social lives differ from humans’, so it cannot be assumed that the same explanation applies to children.'),
        ('reliability of observations', 'weakness', 'Decisions about what counted as an interaction were made by observers watching video; if only one observer coded each behaviour, inter-rater reliability may be limited.'),
        ('nature versus nurture', 'weakness', 'Even monkeys experience some social learning in a troop (for example from mothers), so the study cannot completely rule out the influence of socialisation.'),
        ('ethics', 'strength', 'The monkeys were not harmed or deprived; they were simply offered toys in their normal enclosure, which may even have been enriching.'),
    ],
    'essays': [
        ('sex differences in toy preference are mainly caused by biological factors',
         ['Male rhesus monkeys, who are not exposed to human gender stereotypes, preferred wheeled toys, as boys do (Hassett et al.).', 'Prenatal androgens are linked to masculine play (for example girls with congenital adrenal hyperplasia).'],
         ['Female monkeys showed no strong preference, unlike human girls, suggesting that human preferences are partly learned.', 'Children are rewarded and shown toys by parents and media (socialisation).', 'Monkeys may not generalise to humans.'],
         ['nature versus nurture', 'animal research', 'hormones']),
        ('the use of animals in Hassett et al.’s study can be justified',
         ['Monkeys allowed toy preference to be studied without human gender socialisation, which would be impossible with children.', 'The monkeys were not harmed and lived in their normal social group.'],
         ['Animals cannot consent, and keeping primates in captivity raises ethical questions.', 'The findings may not generalise to humans, so the benefit is uncertain.'],
         ['ethics of animal research', 'generalisability', 'usefulness']),
    ],
    'exp': [dict(intro=['In a replication of Hassett et al. at a primate centre near {city}, the time (seconds) that each of {n} male monkeys spent interacting with a wheeled toy and a plush toy in one 25-minute session was recorded.',
                        '{person} observed {n} male monkeys, each offered a wheeled toy and a plush toy at the same time, and recorded the seconds spent with each toy.'],
                 A='wheeled toy', B='plush toy', gA='male monkeys with a wheeled toy', gB='the same male monkeys with a plush toy',
                 more='will spend more time interacting with a wheeled toy than', measure='time spent interacting with the toy', dvshort='Time spent interacting (seconds)',
                 iv='the type of toy (wheeled or plush)', dv='the number of seconds each monkey spent interacting with each toy during the session',
                 range=(5, 120), base=(25, 40), diff=(18, 35), sd=12, design='repeated measures',
                 controls=['both toys placed the same distance from the monkeys at the same time, so that position does not bias choice', 'using toys of similar size and colour, so that only the category (wheeled or plush) differs'],
                 ethics=['the monkeys must not be stressed by the toys or by the observers; the session can be stopped if conflict occurs'],
                 concl_A='male monkeys prefer wheeled toys to plush toys.', concl_B='male monkeys prefer plush toys to wheeled toys.')],
    'obs': [dict(intro=['Two observers in {city} watched the same video of a monkey troop that had been given a wheeled and a plush toy, and tallied each type of interaction.',
                        '{person} and a colleague independently coded video of monkeys interacting with toys, using the same behavioural categories.'],
                 cats=['touching a toy', 'carrying a toy', 'pushing or rolling a toy', 'sitting with a toy', 'manipulating a toy with hands', 'chewing or biting a toy'], tally=(4, 20),
                 kind='a non-participant observation using video recordings', kind_plus='Video can be replayed, so behaviours are less likely to be missed and two observers can code the same footage to check inter-rater reliability.',
                 kind_minus='The camera may not capture every angle of the enclosure, so some interactions could be missed or mis-coded.',
                 ethics=['the animals should not be disturbed by the cameras or observers, in line with guidelines for animal research'])],
    'plan': [('whether young children prefer toys associated with their own gender', 'IV: gender of the child', 'DV: time spent playing with each toy', ['observation', 'laboratory experiment']),
             ('whether parents encourage boys and girls to play with different toys', 'topic: parental encouragement', 'measure: rating scales and open answers', ['questionnaire', 'interview'])],
}

c3a = T('Background: sex differences in toy preference; hormones and socialisation', 'sex differences toy preference hormones socialisation')
build(c3a, {
    'terms': [
        ('androgens', 'hormones, such as testosterone, that are present at higher levels in males and influence the development of masculine characteristics'),
        ('socialisation', 'the process by which individuals learn the norms and expectations of their culture, for example through parents, peers and media'),
        ('sex-typed behaviour', 'behaviour that is typically more common in one sex than the other, such as preferences for particular toys'),
        ('nature', 'the influence of inherited, biological factors such as genes and hormones on behaviour'),
        ('nurture', 'the influence of the environment and experience, such as upbringing and culture, on behaviour'),
        ('congenital adrenal hyperplasia (CAH)', 'a condition in which a foetus is exposed to unusually high levels of androgens before birth'),
    ],
    'mcq': [
        ('Why did Hassett et al. study monkeys rather than children?', 'Monkeys are not exposed to human gender socialisation about toys', ['Monkeys are easier to interview', 'Children do not play with toys', 'Monkeys are genetically identical to humans'], 'Removing human socialisation helps to test a biological explanation.'),
        ('Girls with congenital adrenal hyperplasia tend to show', 'more male-typical toy preferences', ['no interest in any toys', 'more female-typical toy preferences', 'a preference for plush toys only'], 'High prenatal androgens are linked to masculine play.'),
        ('Which explanation of toy preference belongs to the nurture side of the debate?', 'Parents reward children for playing with gender-typical toys', ['Prenatal testosterone shapes the developing brain', 'Toy preferences are inherited in genes', 'Brain structure differs between the sexes from birth'], 'Learning through rewards and modelling is environmental.'),
        ('Which hormone is the main androgen?', 'Testosterone', ['Oxytocin', 'Oestrogen', 'Melatonin'], 'Testosterone is the principal androgen.'),
    ],
    'ar': [
        ('Hassett et al.’s study is an example of the biological approach.', 'It aimed to test whether hormones, rather than socialisation, influence toy preferences.', 'AR', 'The focus on hormonal influence makes it biological.'),
        ('Human children’s toy preferences are entirely due to socialisation.', 'Children are given different toys by parents according to their sex.', 'R', 'A is false: biological factors such as androgens also play a part. R is true.'),
    ],
    'explain': [
        ('Explain how hormones might influence children’s toy preferences.', 'Exposure to androgens such as testosterone before birth may organise the developing brain in a more male-typical way, leading to interest in toys involving movement, such as vehicles.', '1 mark: prenatal androgens; 1 mark: effect on brain/preference [2]'),
        ('Explain how socialisation might influence children’s toy preferences.', 'Parents, peers and the media present certain toys as being for boys or girls, and children are praised or teased according to their choices, so they learn and imitate gender-typical preferences.', '1 mark: source of socialisation; 1 mark: mechanism (reinforcement/modelling) [2]'),
        ('Explain why studying monkeys can help to resolve the nature–nurture debate about toy preference.', 'Monkeys do not experience human gender stereotypes about toys, so if they still show sex differences, these are more likely to be due to biological factors.', '1 mark: no human socialisation; 1 mark: points to biology [2]'),
    ],
    'claims': [
        ('Hassett et al. aimed to find out whether monkeys could be taught to play with toys.', False, 'The aim was to compare male and female monkeys’ preferences for wheeled and plush toys, to see whether sex differences exist without human socialisation.'),
        ('Earlier research by Alexander and Hines (2002) found sex differences in toy preference in vervet monkeys.', True, 'Male vervet monkeys spent more time with masculine toys such as a ball and a car; Hassett et al. built on this.'),
    ],
    'apply': [
        ('{person} notices that their young son plays mostly with toy cars, while their daughter plays with dolls and cars equally. {person} wonders whether this is “natural”.',
         [('Use the biological approach to explain the son’s preference.', 'Higher prenatal androgen levels in boys may make toys with movement, such as cars, more attractive; Hassett et al. found the same preference in male monkeys.', '1 mark: androgens; 1 mark: link to evidence [2]'),
          ('Use socialisation to explain the son’s preference.', 'The boy may have been given cars more often and praised for playing with them, or have copied other boys and adverts.', '1 mark: socialisation source; 1 mark: mechanism [2]'),
          ('Explain how the daughter’s behaviour is similar to the findings of Hassett et al.', 'Female monkeys interacted with both wheeled and plush toys and did not show a strong preference, just as the daughter plays with both.', '1 mark: females no strong preference; 1 mark: link [2]')]),
    ],
})

c3b = T('Procedure and results: rhesus monkeys with wheeled and plush toys', 'procedure results rhesus monkeys wheeled plush toys')
build(c3b, {
    'mcq': [
        ('Where did the monkeys in Hassett et al.’s study live?', 'In a large social troop at the Yerkes National Primate Research Center field station', ['Alone in laboratory cages', 'In the wild in India', 'In a zoo in London'], 'A troop of 135 rhesus monkeys in an outdoor enclosure.'),
        ('Which of these was a plush toy in Hassett et al.’s study?', 'A teddy bear', ['A wagon', 'A dump truck', 'A shopping cart'], 'Plush toys included Winnie the Pooh, a teddy bear, a koala, an armadillo and a turtle.'),
        ('Which of these was a wheeled toy in Hassett et al.’s study?', 'A construction vehicle', ['A Raggedy Ann doll', 'A koala bear', 'A turtle'], 'Wheeled toys included a wagon, truck, car, construction vehicle and shopping cart.'),
        ('What did Hassett et al. find about male monkeys?', 'They preferred wheeled toys to plush toys', ['They preferred plush toys', 'They showed no interest in toys', 'They played only with toys their mothers chose'], 'Males interacted more frequently and for longer with wheeled toys.'),
        ('What did Hassett et al. find about female monkeys?', 'They interacted with both types of toy without a strong preference', ['They interacted only with wheeled toys', 'They avoided all toys', 'They preferred wheeled toys more strongly than males did'], 'Females’ preferences were more variable, similar to human girls in some research.'),
        ('How were the monkeys’ interactions with the toys recorded?', 'Using video recordings that were later coded', ['Through interviews with keepers', 'Using EEG recordings', 'Using questionnaires given to the monkeys’ handlers'], 'Video allowed frequency and duration to be measured.'),
    ],
    'ar': [
        ('Hassett et al. measured both the frequency and the duration of interactions.', 'They wanted to know how often and for how long each monkey interacted with each toy.', 'AR', 'Frequency and duration both indicate preference.'),
        ('In each session the monkeys were given only one type of toy.', 'Hassett et al. wanted to measure preference between two types of toy.', 'R', 'A is false: one wheeled and one plush toy were offered together; R is true.'),
    ],
    'explain': [
        ('Describe the procedure of Hassett et al.’s study.', 'A troop of rhesus monkeys in an outdoor enclosure was given one wheeled and one plush toy at the same time in each test session; sessions were videotaped and the frequency and duration of each monkey’s interactions with each toy were coded and compared by sex.', '1 mark: one wheeled and one plush toy together; 1 mark: video/observation; 1 mark: frequency and duration compared by sex [3]'),
        ('Explain why Hassett et al. used several different wheeled and plush toys.', 'So that preferences reflected the type of toy rather than features of one particular toy, such as colour or size; this increased validity.', '1 mark: avoids single-toy features; 1 mark: validity [2]'),
        ('Describe the results of Hassett et al.’s study.', 'Male monkeys consistently preferred wheeled toys, interacting with them more often and for longer; females interacted with both types and did not show a significant preference; the pattern was similar to human children’s toy preferences.', '1 mark males; 1 mark females; 1 mark comparison with humans [3]'),
        ('Explain the conclusion Hassett et al. drew from their results.', 'Because the monkeys had not experienced human gender socialisation, the males’ preference suggests that biological factors such as hormones contribute to sex differences in toy preference; human socialisation may strengthen these differences.', '1 mark biological factors; 1 mark reason (no socialisation) [2]'),
    ],
    'claims': [
        ('Hassett et al. found that female monkeys strongly preferred plush toys.', False, 'Females interacted with both types; their preference was much weaker and more variable than males’ preference for wheeled toys.'),
        ('Hassett et al. was an observation of monkeys in a social group.', True, 'Monkeys were observed (via video) interacting with toys within their normal troop.'),
    ],
})
add_tally_pct(c3b, ['The table shows the number of interactions with each type of toy for several monkeys in a replication of Hassett et al. near {city}.', '{person} counted interactions with a wheeled toy and a plush toy for several monkeys.'],
              [('Male monkey 1', (10, 25), (2, 8)), ('Male monkey 2', (8, 22), (3, 9)), ('Female monkey 1', (5, 15), (6, 16)), ('Female monkey 2', (4, 14), (5, 17)), ('Male monkey 3', (12, 24), (4, 10))],
              ('wheeled toy', 'plush toy', 'interactions'))

c3c = T('Evaluation: animal research, nature versus nurture and generalisability', 'evaluation animal research nature versus nurture generalisability')
build(c3c, {
    'mcq': [
        ('Which is the main strength of using monkeys in Hassett et al.’s study?', 'Monkeys have not been exposed to human gender stereotypes about toys', ['Monkeys can describe their preferences', 'Monkeys are genetically identical to humans', 'Monkeys cannot be observed'], 'This allows the influence of socialisation to be reduced.'),
        ('Which ethical principle for animal research means using the fewest animals necessary?', 'Reduction', ['Replacement', 'Refinement', 'Reinforcement'], 'Reduction = fewest animals for valid results.'),
        ('Hassett et al.’s findings support which side of the nature–nurture debate most strongly?', 'Nature (biological influences)', ['Nurture only', 'Neither side', 'Free will'], 'Sex differences without human socialisation suggest biological influence.'),
    ],
    'ar': [
        ('Hassett et al.’s findings may not generalise to humans.', 'Rhesus monkeys and humans differ in cognition and culture.', 'AR', 'Species differences are the reason for limited generalisation.'),
    ],
    'explain': [
        ('Explain why Hassett et al.’s study cannot completely rule out the influence of nurture.', 'The monkeys grew up in a social troop and could learn from mothers and peers, and they may have had earlier experience of objects, so some social learning is possible.', '1 mark: social learning possible in troop; 1 mark: so not purely biological [2]'),
        ('Explain one way in which Hassett et al.’s study was ethical.', 'The monkeys were not harmed or deprived; they were observed in their normal enclosure and the toys may have provided enrichment.', '1 mark: no harm; 1 mark: normal environment/enrichment [2]'),
        ('Explain how Hassett et al.’s study is relevant to the nature versus nurture debate.', 'It tests whether sex differences in toy preference exist without human socialisation; because male monkeys preferred wheeled toys, nature (for example hormones) appears to contribute, although nurture may increase the difference in humans.', '1 mark: tests without socialisation; 1 mark: supports nature with qualification [2]'),
    ],
    'claims': [
        ('Because Hassett et al. used monkeys, their study has no ethical issues.', False, 'Animal studies must still follow guidelines on housing, stress and the 3 Rs; captivity itself raises ethical questions.'),
        ('Using animals in research allows researchers to control factors that would be impossible with children.', True, 'For example, monkeys can be studied without exposure to gendered toy advertising.'),
    ],
})
chapter(3, [c3a, c3b, c3c], HA_STUDY)


# ============================================================== CHAPTER 4: Hölzel et al. (2011)

HO = 'Hölzel et al.’s (2011) study of mindfulness and brain grey matter'
HO_STUDY = {
    'who': HO,
    'evals': [
        ('the use of MRI', 'strength', 'MRI scans gave objective, quantitative measures of grey matter concentration, so changes in the brain could be measured scientifically rather than inferred from behaviour.'),
        ('controls', 'strength', 'A waiting-list control group was scanned at the same times, so changes found only in the MBSR group are more likely to be due to the programme than to time or repeated scanning.'),
        ('usefulness', 'strength', 'The findings suggest that an 8-week programme can change brain regions linked to learning, memory and emotion regulation, which supports using mindfulness to improve well-being.'),
        ('generalisability', 'weakness', 'The sample was small (16 in the MBSR group) and consisted of healthy volunteers interested in meditation, so the results may not apply to other people.'),
        ('participant variables', 'weakness', 'Participants were not randomly allocated to the MBSR and control groups, so the groups might have differed in motivation or lifestyle.'),
        ('self-report', 'weakness', 'Home practice time and mindfulness scores were self-reported, so participants may have exaggerated their practice (social desirability).'),
        ('ethics', 'strength', 'MRI is non-invasive, participants gave informed consent, and the control group was offered the MBSR course after the study.'),
    ],
    'essays': [
        ('psychological interventions can change the structure of the brain',
         ['Hölzel et al. found increased grey matter concentration in the left hippocampus, posterior cingulate cortex, temporo-parietal junction and cerebellum after MBSR.', 'Brain plasticity research shows experience changes neural structure.'],
         ['The sample was small and not randomly allocated.', 'MRI shows correlation with the programme, but other lifestyle changes may have contributed.', 'Changes in grey matter concentration do not necessarily mean changes in behaviour.'],
         ['brain plasticity', 'controls', 'usefulness']),
    ],
    'exp': [dict(intro=['A clinic in {city} compared stress scores (0–40, higher = more stress) after eight weeks for {n} adults who completed a mindfulness course and {n} adults on a waiting list.',
                        '{person} measured self-rated stress (0–40) in an 8-week mindfulness group and a waiting-list control group in {city}.'],
                 A='mindfulness course', B='waiting list', gA='adults who complete a mindfulness course', gB='adults on a waiting list',
                 more='will have lower stress scores than', measure='stress score', dvshort='Stress score (0–40)', higher='B',
                 iv='whether participants completed the 8-week mindfulness course or were on the waiting list', dv='stress score out of 40 on a self-report questionnaire after eight weeks',
                 range=(4, 40), base=(14, 18), diff=(4, 8), sd=4,
                 controls=['the same stress questionnaire, completed at the same time point by both groups', 'both groups recruited in the same way so that they are similar in initial stress'],
                 ethics=['the waiting-list group should be offered the course afterwards', 'participants with high stress should be given information about support services'],
                 concl_A='the mindfulness course increased stress.', concl_B='the mindfulness course reduced stress compared with being on a waiting list.')],
    'corr': [dict(intro=['{person} asked {n} participants in an 8-week mindfulness course in {city} to record average daily meditation practice (minutes) and measured their increase in mindfulness score.',
                         'In a mindfulness programme in {city}, daily practice time (minutes) and change in mindfulness score were recorded for {n} participants.'],
                  x='average daily meditation practice in minutes', y='increase in mindfulness score', xs='daily practice time', ys='increase in mindfulness score', xr=(5, 45), yr=(0, 30), sign=1,
                  third=['motivation to benefit from the course', 'free time available (less stressful lifestyle)', 'previous interest in meditation'])],
    'plan': [('whether a short daily mindfulness exercise reduces exam anxiety in students', 'IV: mindfulness exercise or no exercise', 'DV: anxiety rating on a questionnaire', ['field experiment', 'laboratory experiment'])],
}

c4a = T('Background: mindfulness-based stress reduction and brain plasticity', 'mindfulness-based stress reduction brain plasticity')
build(c4a, {
    'terms': [
        ('mindfulness', 'paying attention to present-moment experience in a non-judgemental way'),
        ('mindfulness-based stress reduction (MBSR)', 'an 8-week programme of weekly group sessions and daily home practice of mindfulness meditation'),
        ('neuroplasticity', 'the ability of the brain to change its structure and function in response to experience'),
        ('grey matter', 'brain tissue made mainly of neuron cell bodies, involved in processing information'),
        ('hippocampus', 'a brain structure involved in learning, memory and the regulation of emotion'),
    ],
    'foils': ['amygdala hijack', 'synaptic pruning'],
    'mcq': [
        ('How long is a standard MBSR programme?', 'Eight weeks', ['Two days', 'One year', 'Three weeks'], 'MBSR runs for eight weeks with weekly sessions and a retreat day.'),
        ('Which brain structure, linked to learning and memory, showed increased grey matter in Hölzel et al.’s study?', 'The left hippocampus', ['The medulla', 'The occipital lobe', 'The spinal cord'], 'The hippocampus was a region of interest that showed an increase.'),
        ('Neuroplasticity means that', 'the brain can change in response to experience', ['the brain is fixed after childhood', 'neurons cannot form new connections', 'behaviour has no biological basis'], 'Experience can alter brain structure.'),
    ],
    'explain': [
        ('Explain what is meant by brain plasticity and how it relates to Hölzel et al.’s study.', 'Plasticity is the brain’s ability to change with experience; Hölzel et al. tested whether 8 weeks of mindfulness practice would change grey matter concentration in particular regions.', '1 mark definition; 1 mark link to study [2]'),
        ('Explain why Hölzel et al.’s study belongs to the biological approach.', 'It measures physical changes in brain structure (grey matter concentration on MRI) to explain the effects of a psychological practice.', '1 mark brain structure; 1 mark MRI evidence [2]'),
    ],
    'claims': [
        ('MBSR involves taking medication to reduce stress.', False, 'MBSR is a psychological programme of meditation practices such as the body scan, mindful yoga and sitting meditation.'),
        ('Earlier studies had found differences in the brains of experienced meditators.', True, 'Cross-sectional studies compared meditators and non-meditators, but could not show that meditation caused the differences.'),
    ],
    'apply': [
        ('{person}, a nurse in {city}, feels stressed and is offered a place on an 8-week mindfulness-based stress reduction course.',
         [('Describe what {person} would be likely to do on the course.', 'Attend weekly group sessions of about 2.5 hours, a one-day retreat, and practise daily at home with recordings, including the body scan, mindful yoga and sitting meditation.', '1 mark sessions; 1 mark practices [2]'),
          ('Use Hölzel et al.’s findings to explain how the course might affect {person}’s brain.', 'It might increase grey matter concentration in regions such as the hippocampus, linked to learning, memory and emotional regulation.', '1 mark grey matter increase; 1 mark region and function [2]'),
          ('Explain one reason why the course might not work for everyone.', 'People who do not complete the home practice, or who have different reasons for stress, may not benefit; the study used a small sample of healthy volunteers.', '1 mark reason; 1 mark explained [2]')]),
    ],
})

c4b = T('Procedure and results: MRI scans and changes in grey matter density', 'procedure results mri scans grey matter density')
build(c4b, {
    'mcq': [
        ('How many participants completed the MBSR programme in Hölzel et al.’s study?', '16', ['5', '40', '135'], '16 MBSR participants and a waiting-list control group of 17.'),
        ('What type of control group did Hölzel et al. use?', 'A waiting-list group who were scanned at the same times', ['A group given a placebo pill', 'A group who meditated for one day only', 'No control group'], 'The control group was offered MBSR after the study.'),
        ('When were the participants’ brains scanned?', 'Before and after the eight-week period', ['Only after the programme', 'Every day during the programme', 'Only before the programme'], 'MRI about two weeks before and after.'),
        ('Which questionnaire measured mindfulness in Hölzel et al.’s study?', 'The Five Facet Mindfulness Questionnaire (FFMQ)', ['The Autism Spectrum Quotient', 'The Beck Depression Inventory', 'The Social Readjustment Rating Scale'], 'The FFMQ measures facets such as observing and acting with awareness.'),
        ('Roughly how many minutes per day did the MBSR participants report practising at home on average?', 'About 27 minutes', ['About 2 minutes', 'About 3 hours', 'About 90 minutes'], 'Average home practice was about 27 minutes a day.'),
    ],
    'explain': [
        ('Describe the procedure of Hölzel et al.’s study.', 'Healthy adults with no meditation experience took an 8-week MBSR course (weekly 2.5-hour sessions, a retreat day and home practice); MRI scans were taken before and after, as for a waiting-list control group, and grey matter concentration was compared.', '1 mark MBSR course; 1 mark MRI before/after; 1 mark control group comparison [3]'),
        ('Describe the results of Hölzel et al.’s study.', 'The MBSR group showed increased grey matter concentration in the left hippocampus, posterior cingulate cortex, temporo-parietal junction and cerebellum compared with the control group; mindfulness scores also increased.', '1 mark: increased grey matter; 1 mark: named regions; 1 mark: compared with controls [3]'),
        ('Explain why Hölzel et al. used a longitudinal (before-and-after) design.', 'Scanning the same people before and after the programme shows change over time within individuals, so the changes are more likely to be caused by the programme than by pre-existing differences.', '1 mark same people over time; 1 mark causal inference [2]'),
    ],
    'claims': [
        ('Hölzel et al. found that grey matter decreased in the hippocampus after MBSR.', False, 'Grey matter concentration increased in the left hippocampus.'),
        ('The control group in Hölzel et al.’s study did not receive any MBSR training during the study period.', True, 'They were on a waiting list and offered the course afterwards.'),
    ],
})

c4c = T('Evaluation: application to everyday life and controls', 'evaluation application everyday life controls')
build(c4c, {
    'mcq': [
        ('Which is the main purpose of the control group in Hölzel et al.’s study?', 'To show that brain changes were due to MBSR rather than the passage of time or repeated scanning', ['To give participants a placebo', 'To provide more people for the MBSR group', 'To check the MRI machine'], 'Controls rule out alternative explanations.'),
        ('Which is a weakness of Hölzel et al.’s sample?', 'It was small and made up of volunteers interested in meditation', ['It included thousands of participants', 'It included only experienced meditators', 'It included only children'], 'Self-selected, small sample.'),
    ],
    'explain': [
        ('Explain one way in which Hölzel et al.’s findings could be applied to everyday life.', 'Mindfulness courses could be offered at work or in schools to reduce stress and support emotional regulation, because the study suggests that 8 weeks can produce measurable brain changes.', '1 mark application; 1 mark link to findings [2]'),
        ('Explain why the lack of random allocation is a weakness of Hölzel et al.’s study.', 'Participants who chose to join the MBSR group may already have been more motivated or healthier, so differences in brain change could be due to participant variables rather than the programme.', '1 mark: not randomly allocated; 1 mark: participant variables explanation [2]'),
        ('Explain why self-reported practice time is a problem in Hölzel et al.’s study.', 'Participants may over-report how much they meditated to appear committed, so the link between practice and brain change may be inaccurate.', '1 mark: social desirability; 1 mark: consequence [2]'),
    ],
    'claims': [
        ('Hölzel et al.’s study proves that mindfulness reduces stress for everyone.', False, 'It used a small sample of healthy volunteers and measured grey matter, so it cannot prove that the effect applies to everyone.'),
        ('Hölzel et al. measured both brain structure and self-reported mindfulness.', True, 'MRI scans and the Five Facet Mindfulness Questionnaire were used.'),
    ],
    'apply': [
        ('A company in {city} reads about Hölzel et al.’s study and decides to offer all employees a mindfulness course.',
         [('Explain one reason why the company might expect benefits.', 'Hölzel et al. found MBSR increased grey matter in regions linked to memory and emotion regulation, suggesting that employees might cope better with stress.', '1 mark finding; 1 mark link to benefit [2]'),
          ('Explain one reason why the benefits may be smaller than expected.', 'Employees told to attend may be less motivated than volunteers and may not practise at home, so the results may not generalise.', '1 mark reason; 1 mark explained [2]'),
          ('Suggest how the company could measure whether the course works.', 'Measure stress before and after with a questionnaire (or sickness absence) for employees who take the course and a waiting-list comparison group.', '1 mark measure; 1 mark comparison group [2]')]),
    ],
})
chapter(4, [c4a, c4b, c4c], HO_STUDY)


# ============================================================== CHAPTER 5: Andrade (2010)

AN = 'Andrade’s (2010) study of doodling and concentration'
AN_STUDY = {
    'who': AN,
    'evals': [
        ('standardisation', 'strength', 'Every participant heard the same pre-recorded 2.5-minute telephone message in the same monotonous voice and received the same instructions, so the procedure was consistent and replicable.'),
        ('controls', 'strength', 'Participants were randomly allocated to the doodling and control groups and all had just completed another study, so both groups were similarly bored; differences in recall are more likely to be due to doodling.'),
        ('demand characteristics', 'strength', 'The recall test was a surprise, so participants could not deliberately try to remember the message, making recall a more valid measure of incidental memory.'),
        ('usefulness', 'strength', 'The finding that doodling improved recall by about 29% suggests that doodling could help people concentrate in boring situations such as long lectures or meetings.'),
        ('ecological validity', 'weakness', 'Shading shapes on a sheet is not the same as spontaneous doodling, and the message was artificial, so the task may not represent everyday listening.'),
        ('generalisability', 'weakness', 'The sample of 40 was mostly female (35 women) and recruited from one research panel in Cambridge, so the findings may not generalise to men or other populations.'),
        ('demand characteristics', 'weakness', 'Participants in the doodling group were asked to shade shapes, which might have suggested that doodling was being tested, and they may have tried harder.'),
        ('ethics', 'weakness', 'Participants were mildly deceived: they were not told that there would be a memory test, so they had to be debriefed afterwards.'),
    ],
    'essays': [
        ('doodling helps people to concentrate',
         ['Andrade found doodlers recalled 29% more information from a boring telephone message than controls.', 'Doodling may reduce daydreaming, which uses working memory resources.'],
         ['Shading set shapes is not real doodling, so the finding may not generalise.', 'Doodling may distract from tasks that need visual attention.', 'The sample was small and mostly female.'],
         ['working memory', 'ecological validity', 'usefulness']),
        ('cognitive psychology is useful in everyday life',
         ['Andrade’s findings can be applied to meetings and classrooms.', 'Pozzulo et al. and research on line-ups improve police procedures.'],
         ['Laboratory tasks are often artificial.', 'Findings from small samples may not generalise.'],
         ['usefulness', 'ecological validity', 'core studies from the cognitive approach']),
    ],
    'exp': [dict(intro=['{person} replicated Andrade’s study in {city}. {n} participants shaded shapes while listening to a boring telephone message and {n} participants just listened. All then had a surprise test of the names and places mentioned (out of 16).',
                        'In a replication of Andrade (2010) in {city}, participants were randomly allocated to a doodling group or a control group, listened to a 2.5-minute message and then recalled names and places (maximum 16).'],
                 A='doodling', B='control (no doodling)', gA='participants who doodle while listening', gB='participants who only listen',
                 more='will recall more names and places than', measure='the number of names and places recalled', dvshort='Names and places recalled (out of 16)',
                 iv='whether participants doodled (shaded shapes) while listening or just listened', dv='the number of names and places (out of 16) correctly recalled in a surprise test',
                 range=(1, 16), base=(5, 6.5), diff=(1.3, 2.6), sd=1.8,
                 controls=['the same recorded message played at the same volume, so that the message cannot explain differences', 'the same recall time and instructions for every participant',
                           'testing everyone at a similar time after another task, so that boredom levels are similar'],
                 ethics=['debriefing: participants were not told about the memory test, so the deception must be explained afterwards', 'right to withdraw: participants should know they can leave at any time'],
                 concl_A='doodling while listening improves recall of information.', concl_B='doodling while listening reduces recall of information.')],
    'plan': [('whether doodling helps students remember information from a lecture', 'IV: doodling or not doodling', 'DV: score on a recall test', ['laboratory experiment', 'field experiment']),
             ('how often students doodle in lessons', 'behaviour: doodling', 'categories: doodling, note-taking, looking at the teacher', ['observation'])],
}

c5a = T('Background: working memory, attention and daydreaming', 'working memory attention daydreaming')
build(c5a, {
    'terms': [
        ('working memory', 'a limited-capacity system that holds and processes information while a task is being carried out'),
        ('central executive', 'the component of working memory that directs attention and coordinates the other components'),
        ('phonological loop', 'the component of working memory that holds and rehearses speech-based (sound) information'),
        ('visuospatial sketchpad', 'the component of working memory that holds visual and spatial information'),
        ('daydreaming', 'thoughts that drift away from the current task to unrelated topics'),
        ('cognitive approach', 'the view that behaviour can be explained by internal mental processes such as attention, memory and thinking'),
    ],
    'mcq': [
        ('Andrade suggested that doodling might improve concentration because it', 'reduces daydreaming, which uses up working memory resources', ['increases arousal through physical exercise', 'replaces the need to listen', 'stores the message visually'], 'Doodling may use just enough attention to stop the mind wandering.'),
        ('Which component of working memory would hold a spoken telephone message?', 'The phonological loop', ['The visuospatial sketchpad', 'Long-term memory', 'The sensory register for vision'], 'Speech-based information is held in the phonological loop.'),
        ('Which approach does Andrade’s study belong to?', 'The cognitive approach', ['The biological approach', 'The learning approach', 'The social approach'], 'It studies attention and memory.'),
        ('Working memory is described as having', 'limited capacity', ['unlimited capacity', 'no role in attention', 'only one component'], 'Tasks compete for limited resources.'),
    ],
    'ar': [
        ('Doing two tasks at once can reduce performance.', 'Working memory has a limited capacity.', 'AR', 'Limited capacity explains why dual tasks interfere.'),
        ('Daydreaming improves concentration on a boring task.', 'Daydreaming uses the central executive.', 'R', 'A is false: daydreaming uses resources and impairs concentration; R is true.'),
    ],
    'explain': [
        ('Explain how doodling might help concentration, according to Andrade.', 'A boring task leads to low arousal and daydreaming, which uses the central executive and distracts from the task; doodling uses little capacity but keeps arousal up and stops daydreaming, so more attention stays on the message.', '1 mark: boredom/daydreaming uses resources; 1 mark: doodling prevents daydreaming; 1 mark: more attention to task [3]'),
        ('Explain why doodling might be expected to make concentration worse.', 'If doodling and listening compete for the same limited working memory resources (especially the central executive), doing both at once should reduce attention to the message.', '1 mark: dual task/limited capacity; 1 mark: consequence [2]'),
    ],
    'claims': [
        ('The working memory model says that the phonological loop and visuospatial sketchpad are controlled by the central executive.', True, 'The central executive allocates attention to the slave systems.'),
        ('Andrade thought that doodling would mainly use the phonological loop.', False, 'Shading shapes is a visual/motor task, so it would not compete strongly with the speech-based phonological loop.'),
    ],
    'apply': [
        ('{person}, a student in {city}, often finds that during long online lectures their mind wanders to plans for the weekend.',
         [('Identify the cognitive process that {person} is experiencing.', 'Daydreaming (mind-wandering), a lapse of attention.', '1 mark [1]'),
          ('Use Andrade’s findings to suggest one way {person} could improve concentration.', 'Doodle (for example shading shapes) while listening, which may stop daydreaming and improve recall.', '1 mark doodling; 1 mark reason [2]'),
          ('Explain, using working memory, why daydreaming could reduce what {person} remembers.', 'Daydreaming uses central executive resources, leaving less capacity for processing the lecture, so less is encoded.', '1 mark resources used; 1 mark less encoding [2]')]),
    ],
})

c5b = T('Procedure and results: shading task and recall of telephone message', 'procedure results shading task recall telephone message')
build(c5b, {
    'mcq': [
        ('How many participants took part in Andrade’s study?', '40', ['9', '72', '135'], '40 participants: 20 in each condition.'),
        ('What were the doodling participants asked to do?', 'Shade in printed squares and circles while listening', ['Draw whatever they liked', 'Write down every word they heard', 'Sit with their eyes closed'], 'Shading was used to standardise the doodling.'),
        ('How long was the telephone message in Andrade’s study?', 'About 2.5 minutes', ['About 30 seconds', 'About 20 minutes', 'About 1 hour'], 'A 2.5-minute monotonous message.'),
        ('About how much more did doodlers recall than controls?', 'About 29% more', ['About 2% more', 'About three times as much', 'About 29% less'], 'Mean recall 7.5 versus 5.8 items.'),
        ('Why had participants just finished another experiment before Andrade’s study?', 'To make them likely to be bored, so that daydreaming was likely', ['To make them tired so they fell asleep', 'To give them practice at the memory test', 'To check their hearing'], 'Boredom encourages daydreaming.'),
        ('What was the main task given to all participants while listening to the message?', 'To write down the names of people who would be coming to the party', ['To count the number of words spoken', 'To memorise every place mentioned', 'To rate how boring the message was'], 'The monitoring task concerned party-goers’ names.'),
    ],
    'ar': [
        ('Andrade’s doodling group recalled more information than the control group.', 'The doodlers were told in advance that there would be a memory test.', 'A', 'A is true; R is false: the recall test was a surprise for both groups.'),
    ],
    'explain': [
        ('Describe the procedure of Andrade’s study.', 'Forty participants were randomly allocated to a doodling or control group. All listened to a 2.5-minute monotonous telephone message about a party and wrote down the names of people coming. The doodling group shaded shapes while listening. Afterwards there was a surprise test of names and places mentioned.', '1 mark allocation/groups; 1 mark message and monitoring; 1 mark shading; 1 mark surprise recall [4]'),
        ('Describe the results of Andrade’s study.', 'The doodling group monitored the party-goers’ names more accurately and recalled more names and places in the surprise test (mean 7.5 versus 5.8 out of 16, about 29% more).', '1 mark monitoring better; 1 mark recall better with data [2]'),
        ('Explain why Andrade made the recall test a surprise.', 'If participants knew they would be tested they might deliberately rehearse the information, so the test would measure effort rather than the effect of doodling on attention.', '1 mark: avoid deliberate rehearsal; 1 mark: validity [2]'),
    ],
    'claims': [
        ('In Andrade’s study the doodling group were allowed to draw whatever they wanted.', False, 'They shaded printed squares and circles so that doodling was standardised.'),
        ('Andrade used an independent measures design.', True, 'Different participants were in the doodling and control conditions.'),
    ],
})

c5c = T('Evaluation: standardisation, demand characteristics and usefulness', 'evaluation standardisation demand characteristics usefulness')
build(c5c, {
    'mcq': [
        ('Which feature of Andrade’s study reduced demand characteristics?', 'The memory test was a surprise', ['Participants chose their group', 'The message was read live', 'Participants were told the aim'], 'Participants could not prepare for the test.'),
        ('Which feature made Andrade’s procedure standardised?', 'The same recorded message was played to every participant', ['Participants chose what to doodle', 'Each participant heard a different message', 'The test time varied'], 'Recording keeps the stimulus identical.'),
    ],
    'explain': [
        ('Explain why Andrade’s study might be useful.', 'It suggests that doodling during boring tasks (lectures, meetings, telephone calls) could improve attention and recall, so people should not be discouraged from doodling.', '1 mark application; 1 mark link to results [2]'),
        ('Explain one weakness of using a monotonous telephone message in Andrade’s study.', 'Real messages are usually more varied and interesting, so the task may not reflect everyday listening, lowering ecological validity.', '1 mark artificial; 1 mark consequence [2]'),
        ('Explain why the shading task in Andrade’s study may not represent real doodling.', 'Real doodling is spontaneous and varied, whereas shading set shapes is instructed; the effects of free doodling may differ.', '1 mark difference; 1 mark consequence [2]'),
    ],
    'claims': [
        ('Andrade’s study has high ecological validity because people often listen to telephone messages.', False, 'The message was deliberately boring and artificial and the doodling was instructed shading, so ecological validity is limited.'),
        ('A strength of Andrade’s study is that participants were randomly allocated to conditions.', True, 'Random allocation spreads participant variables across the doodling and control groups.'),
    ],
    'apply': [
        ('A manager in {city} notices that one employee, {person}, doodles throughout meetings and asks {person} to stop.',
         [('Use Andrade’s study to explain why {person} may be concentrating well.', 'Andrade found doodlers recalled about 29% more of a boring message, perhaps because doodling stops daydreaming.', '1 mark finding; 1 mark explanation [2]'),
          ('Explain one reason why Andrade’s findings may not apply to this situation.', 'Meetings may be interesting and involve speaking, and {person}’s free doodling differs from shading shapes; the sample was mostly female and small.', '1 mark difference; 1 mark explained [2]'),
          ('Suggest how the manager could test whether doodling helps employees remember meetings.', 'Randomly allocate employees to doodle or not during a recorded meeting, then give a surprise recall test and compare mean scores.', '1 mark IV; 1 mark DV/allocation [2]')]),
    ],
})
chapter(5, [c5a, c5b, c5c], AN_STUDY)


# ============================================================== CHAPTER 6: Baron-Cohen et al. (2001)

BC = 'Baron-Cohen et al.’s (2001) study of the Revised Eyes Test'
BC_STUDY = {
    'who': BC,
    'evals': [
        ('standardisation', 'strength', 'Every participant saw the same 36 photographs with the same four word choices and had access to a glossary, so the test was standardised and comparable across groups.'),
        ('quantitative data', 'strength', 'Eyes Test scores out of 36 allowed groups to be compared objectively (for example a mean of 21.9 for the AS/HFA group versus 28.0 for students).'),
        ('validity of the Eyes Test', 'strength', 'The revision added more items and four choices, reducing ceiling effects and chance guessing, and the AS/HFA group scored lowest as predicted, supporting the test’s validity.'),
        ('ecological validity', 'weakness', 'Judging emotions from still photographs of eyes is unlike everyday social interaction, where faces move and there are voices and context.'),
        ('generalisability', 'weakness', 'The AS/HFA group was small (15) and all male, so the findings may not apply to all autistic people, including women.'),
        ('the student sample', 'weakness', 'Group 3 were Cambridge students, who are not typical of the general population in age or education.'),
        ('individual versus situational explanations', 'strength', 'The study shows individual differences in theory of mind (and by sex), supporting an individual explanation of social understanding.'),
    ],
    'essays': [
        ('the Revised Eyes Test is a valid measure of theory of mind',
         ['Adults with AS/HFA scored significantly lower than all comparison groups, as predicted.', 'Scores correlated negatively with the AQ.', 'The revised version reduced ceiling effects and guessing.'],
         ['Recognising emotion in still photos of eyes is a narrow task, unlike real social interaction.', 'Some words are complex, so vocabulary may affect scores despite the glossary.', 'The photos were mostly of white faces, which may disadvantage other groups.'],
         ['ecological validity', 'standardisation', 'generalisability']),
        ('individual differences are more important than situational factors in explaining social behaviour',
         ['Baron-Cohen et al. show stable individual differences in theory of mind.', 'Perry et al. found oxytocin effects depended on empathy level.'],
         ['Milgram showed situational pressures strongly affect behaviour.', 'Piliavin et al. found helping depended on the type of victim (situation).'],
         ['individual and situational explanations', 'core studies']),
    ],
    'exp': [dict(intro=['{person} compared Eyes Test scores (out of 36) for {n} adults with an autism diagnosis and {n} adults without, matched for age and IQ, in {city}.',
                        'In {city}, Revised Eyes Test scores out of 36 were compared for {n} autistic adults and {n} matched comparison adults.'],
                 A='comparison group', B='autism group', gA='adults without autism', gB='autistic adults',
                 more='will score higher on the Revised Eyes Test than', measure='Eyes Test score', dvshort='Eyes Test score (out of 36)',
                 iv='whether participants had an autism diagnosis or not (a naturally occurring IV)', dv='the number of the 36 Eyes Test items answered correctly',
                 range=(10, 36), base=(21, 23.5), diff=(4, 7), sd=3.5, design='matched pairs',
                 controls=['the same photographs, word choices and glossary for everyone', 'matching groups on IQ and age so that these cannot explain the difference'],
                 ethics=['protection from harm: low scores could be upsetting, so scores should be confidential and explained sensitively', 'informed consent and the right to withdraw'],
                 concl_A='adults without autism are better at recognising mental states from the eyes than autistic adults.', concl_B='autistic adults are better at recognising mental states from the eyes.')],
    'corr': [dict(intro=['{person} gave {n} students in {city} both the Autism Spectrum Quotient (AQ, 0–50) and the Revised Eyes Test (0–36).',
                         'A study in {city} measured AQ scores and Eyes Test scores for {n} adults.'],
                  x='AQ score', y='Eyes Test score', xs='AQ score', ys='Eyes Test score', xr=(8, 38), yr=(16, 34), sign=-1,
                  third=['vocabulary or verbal ability', 'level of education', 'motivation and attention during testing'])],
    'plan': [('whether people are better at recognising emotions from whole faces than from eyes alone', 'IV: whole face or eyes only', 'DV: number of emotions correctly identified', ['laboratory experiment']),
             ('whether there is a relationship between empathy and the number of friends people have', 'co-variable 1: empathy score', 'co-variable 2: number of close friends', ['correlation', 'questionnaire'])],
}

c6a = T('Background: theory of mind and autism spectrum conditions', 'theory of mind autism spectrum conditions')
build(c6a, {
    'terms': [
        ('theory of mind', 'the ability to understand that other people have thoughts, beliefs and feelings that may differ from one’s own'),
        ('autism spectrum condition', 'a developmental condition involving differences in social communication and interaction, and restricted or repetitive interests'),
        ('Asperger syndrome', 'a form of autism in which language and intelligence develop typically but social understanding differs'),
        ('Autism Spectrum Quotient (AQ)', 'a 50-item self-report questionnaire measuring the number of autistic traits an adult has'),
        ('ceiling effect', 'when a test is too easy, so many people score near the maximum and differences between them cannot be detected'),
    ],
    'foils': ['false-belief task', 'central coherence'],
    'mcq': [
        ('Which ability does the Eyes Test aim to measure?', 'Theory of mind (recognising mental states)', ['Short-term memory span', 'Intelligence', 'Visual acuity'], 'It measures the ability to attribute mental states from the eye region.'),
        ('Why was the original Eyes Test revised?', 'It had problems such as ceiling effects and only two answer choices', ['It was too difficult for everyone', 'It used whole faces', 'It took several hours'], 'Too easy for many, and 50% chance of guessing.'),
        ('Which statement describes the extreme male brain theory?', 'Autism is an extreme form of a typically male cognitive style that is strong at systemising and weaker at empathising', ['Autism is caused by cold parenting', 'Males are always better at reading emotions', 'Autism is more common in females'], 'Baron-Cohen’s theory links autism to male-typical traits.'),
    ],
    'ar': [
        ('Adults with Asperger syndrome may pass simple theory of mind tests.', 'Simple tests designed for children are too easy for intelligent adults.', 'AR', 'Ceiling effects explain why a more advanced adult test was needed.'),
    ],
    'explain': [
        ('Explain what is meant by theory of mind and why it is important.', 'Theory of mind is understanding that others have their own beliefs, intentions and emotions; it allows us to predict and interpret behaviour and to communicate effectively.', '1 mark definition; 1 mark importance [2]'),
        ('Explain why Baron-Cohen et al. needed a more sensitive “advanced” test of theory of mind.', 'Adults with Asperger syndrome or high-functioning autism often pass simple false-belief tasks, yet still have social difficulties, so a harder test was needed to detect subtle differences.', '1 mark pass simple tasks; 1 mark subtle difficulties detected [2]'),
    ],
    'claims': [
        ('Theory of mind means being able to read other people’s minds accurately all the time.', False, 'It is the understanding that others have mental states, used to infer them; everyone makes mistakes.'),
        ('The AQ is completed by the participant as a self-report questionnaire.', True, 'It has 50 statements that participants agree or disagree with.'),
    ],
    'apply': [
        ('{person}, an adult in {city}, says that conversations at work are confusing because colleagues often mean something different from what they say.',
         [('Use the concept of theory of mind to explain {person}’s difficulty.', '{person} may find it harder to infer other people’s intentions and feelings from cues such as the eyes and tone, so implied meanings are missed.', '1 mark theory of mind; 1 mark application [2]'),
          ('Suggest how {person}’s theory of mind could be measured.', 'Using the Revised Eyes Test: choosing which of four words best describes what a person in a photo of the eyes is thinking or feeling (36 items).', '1 mark test; 1 mark description [2]'),
          ('Explain one reason why a low score would not prove that {person} is autistic.', 'The Eyes Test is not a diagnostic tool; scores also depend on vocabulary, attention and cultural familiarity with the faces.', '1 mark not diagnostic; 1 mark other factors [2]')]),
    ],
})

c6b = T('Procedure and results: Revised Eyes Test and AQ across four groups', 'procedure results revised eyes test aq four groups')
build(c6b, {
    'mcq': [
        ('How many items are in the Revised Eyes Test?', '36', ['25', '50', '16'], '36 photographs of the eye region.'),
        ('How many word choices accompany each photograph in the Revised Eyes Test?', 'Four', ['Two', 'Six', 'Ten'], 'One target word and three foils.'),
        ('Which group scored lowest on the Revised Eyes Test?', 'Adults with Asperger syndrome or high-functioning autism', ['Cambridge students', 'General population adults', 'IQ-matched controls'], 'Mean 21.9 compared with 26.2–30.9 for the other groups.'),
        ('Which group consisted of 103 undergraduates?', 'Group 3', ['Group 1', 'Group 2', 'Group 4'], 'Group 3 were Cambridge undergraduates.'),
        ('What relationship was found between AQ and Eyes Test scores?', 'A negative correlation', ['A positive correlation', 'No relationship', 'A perfect correlation'], 'Higher AQ was associated with lower Eyes Test scores.'),
        ('In the general population group, who scored higher on the Eyes Test on average?', 'Females', ['Males', 'There was no difference', 'People over 60'], 'Females scored slightly higher than males.'),
    ],
    'ar': [
        ('A glossary was provided during the Revised Eyes Test.', 'Some of the mental-state words were difficult and unfamiliar.', 'AR', 'The glossary reduced the effect of vocabulary on scores.'),
        ('Group 1 in Baron-Cohen et al.’s study included both males and females.', 'Group 1 was recruited through advertisements and clinics.', 'R', 'A is false: Group 1 (15 adults) were all male; R is true.'),
    ],
    'explain': [
        ('Describe the four groups of participants in Baron-Cohen et al.’s study.', 'Group 1: 15 adults with Asperger syndrome or high-functioning autism (all male). Group 2: 122 adults from the general population. Group 3: 103 Cambridge undergraduates. Group 4: 14 adults from the general population matched on IQ with Group 1.', '1 mark per group [4]'),
        ('Describe how the Revised Eyes Test was carried out.', 'Participants saw 36 black-and-white photographs of the eye region and chose which of four words best described what the person was thinking or feeling; a glossary was available; they also completed the AQ.', '1 mark photos; 1 mark four words; 1 mark glossary/AQ [3]'),
        ('Describe the main results of Baron-Cohen et al.’s study.', 'The AS/HFA group scored significantly lower on the Eyes Test (mean 21.9) than the other groups (26.2, 28.0, 30.9); they scored higher on the AQ; Eyes Test and AQ scores correlated negatively; females in the general population scored higher than males.', '1 mark AS/HFA lowest; 1 mark correlation; 1 mark sex difference [3]'),
    ],
    'claims': [
        ('In the Revised Eyes Test, participants saw photographs of whole faces.', False, 'They saw only the eye region.'),
        ('The AS/HFA group had higher AQ scores than the comparison groups.', True, 'They reported more autistic traits.'),
    ],
})
add_tally_pct(c6b, ['The table shows how many participants in a replication of the Eyes Test in {city} scored above and below 25 out of 36.', '{person} recorded the number of participants in each group scoring above or below 25 on the Revised Eyes Test.'],
              [('Autistic adults', (3, 8), (8, 14)), ('General population', (30, 60), (15, 30)), ('Students', (40, 70), (10, 25)), ('IQ-matched controls', (8, 13), (1, 4))],
              ('above 25', '25 or below', 'participants'))

c6c = T('Evaluation: validity of the Eyes Test and individual versus situational explanations', 'evaluation validity eyes test individual versus situational explanations')
build(c6c, {
    'mcq': [
        ('Which is a threat to the ecological validity of the Eyes Test?', 'It uses still photographs of eyes rather than real, moving faces in context', ['It has 36 items', 'It has a glossary', 'It uses four answer choices'], 'Real social cues are dynamic and contextual.'),
        ('Baron-Cohen et al.’s findings best support which type of explanation of social understanding?', 'An individual explanation', ['A situational explanation', 'An explanation based only on reinforcement', 'An explanation based on obedience'], 'Differences between individuals (diagnosis, sex) in theory of mind.'),
    ],
    'explain': [
        ('Explain why Baron-Cohen et al.’s study supports an individual explanation of behaviour.', 'Scores differed between individuals and groups (for example autistic adults and males scored lower), suggesting that social understanding depends on characteristics of the person rather than the situation.', '1 mark individual differences; 1 mark link to evidence [2]'),
        ('Explain one way in which the revised version of the Eyes Test was more valid than the original.', 'Four answer choices instead of two reduced the chance of guessing correctly (from 50% to 25%), and more items reduced ceiling effects, so scores better reflect real ability.', '1 mark change; 1 mark effect on validity [2]'),
        ('Explain why using photographs of mainly white faces could reduce the validity of the Eyes Test.', 'People from other cultures may be less familiar with these faces and expressions, so low scores could reflect cultural bias rather than theory of mind.', '1 mark cultural bias; 1 mark consequence [2]'),
    ],
    'claims': [
        ('Because all groups did the same test, Baron-Cohen et al.’s study has no problems with validity.', False, 'Standardisation helps reliability, but the still photos, vocabulary demands and cultural bias may still reduce validity.'),
        ('The IQ-matched group helped to show that low Eyes Test scores were not simply due to low intelligence.', True, 'Group 4 was matched on IQ with the AS/HFA group but scored much higher.'),
    ],
})
chapter(6, [c6a, c6b, c6c], BC_STUDY)


# ============================================================== CHAPTER 7: Pozzulo et al. (2009)

PZ = 'Pozzulo et al.’s (2009) study of children’s and adults’ line-up identifications'
PZ_STUDY = {
    'who': PZ,
    'evals': [
        ('standardisation', 'strength', 'All participants saw the same stimuli and were tested with the same line-up procedure and instructions, so children’s and adults’ performance could be compared fairly.'),
        ('the use of target-present and target-absent line-ups', 'strength', 'Including both types of line-up shows not only whether witnesses can recognise a target but also whether they wrongly choose someone when the target is absent, which matches real police situations.'),
        ('usefulness', 'strength', 'The findings can inform how police conduct line-ups with child witnesses, for example by warning that the culprit may not be present or using procedures that reduce pressure to choose.'),
        ('ecological validity', 'weakness', 'Watching stimuli in a study is not as stressful or emotional as witnessing a real crime, so identification accuracy may differ in real life.'),
        ('generalisability', 'weakness', 'The children were a narrow age range from one area, so the results may not apply to older children or to children from other cultures.'),
        ('ethics', 'weakness', 'Children cannot give fully informed consent, so parental consent was needed, and children may feel anxious about being “wrong”.'),
        ('demand characteristics', 'weakness', 'Children may believe the adult researcher expects them to choose someone from the line-up, so their choices may reflect social pressure rather than memory.'),
    ],
    'essays': [
        ('children are unreliable eyewitnesses',
         ['Children make more false identifications than adults in target-absent line-ups.', 'They may feel social pressure to choose someone to please an adult.'],
         ['Children can be as accurate as adults when the culprit is present in the line-up.', 'Procedures designed for children (for example elimination line-ups and clear instructions) can improve accuracy.'],
         ['target-present and target-absent line-ups', 'social and cognitive explanations', 'usefulness']),
        ('psychological research on line-ups is useful to the legal system',
         ['It shows that target-absent line-ups produce false identifications, so police can give unbiased instructions.', 'It supports special procedures for child witnesses.'],
         ['Laboratory studies lack the stress of real crimes.', 'Courts may still rely on confident witnesses.'],
         ['ecological validity', 'children and psychology debate']),
    ],
    'exp': [dict(intro=['{person} showed {n} children and {n} adults in {city} a short video of a staged event, then a target-absent line-up of six photographs. The number of correct rejections over 10 such line-ups was recorded for each participant.',
                        'In {city}, {n} children aged 5–6 and {n} adults each completed 10 target-absent line-ups; the number of correct rejections (saying “not there”) was counted.'],
                 A='adults', B='children', gA='adults', gB='children aged 5–6',
                 more='will make more correct rejections than', measure='the number of correct rejections', dvshort='Correct rejections (out of 10)',
                 iv='the age group of the participant (child or adult) — a naturally occurring IV', dv='the number of target-absent line-ups (out of 10) correctly rejected',
                 range=(0, 10), base=(3, 4.5), diff=(2.5, 4), sd=1.4,
                 controls=['the same video and line-up photographs for all participants', 'the same unbiased instruction (“the person may or may not be in the line-up”) for everyone'],
                 ethics=['parental consent for the children and their own agreement', 'children should be reassured and debriefed so that they do not feel they failed'],
                 concl_A='adults are better than children at correctly rejecting target-absent line-ups.', concl_B='children are better than adults at correctly rejecting target-absent line-ups.')],
    'plan': [('whether warning witnesses that the culprit may not be present reduces false identifications', 'IV: warning or no warning', 'DV: number of false identifications in target-absent line-ups', ['laboratory experiment']),
             ('what parents think about children giving evidence in court', 'topic: parents’ views on child witnesses', 'measure: rating scales and open answers', ['questionnaire', 'interview'])],
}

c7a = T('Background: eyewitness testimony, line-up identification and children’s errors', "eyewitness testimony line-up identification children's errors")
build(c7a, {
    'terms': [
        ('eyewitness testimony', 'evidence given by a person who saw an event, such as a crime, about what happened and who was involved'),
        ('line-up', 'a procedure in which a witness is shown a suspect among several other people (foils) to see whether they can identify the culprit'),
        ('target-present line-up', 'a line-up in which the culprit (target) is included'),
        ('target-absent line-up', 'a line-up in which the culprit is not included, so the correct response is to reject it'),
        ('foil', 'an innocent person in a line-up who resembles the description of the culprit'),
        ('correct rejection', 'correctly saying that the culprit is not in a target-absent line-up'),
        ('false positive identification', 'choosing an innocent person from a line-up'),
    ],
    'mcq': [
        ('In a target-absent line-up, the correct response is to', 'say that the culprit is not present', ['choose the person who looks most like the culprit', 'choose the first person shown', 'refuse to look at the line-up'], 'The target is absent, so any choice is a false identification.'),
        ('In a simultaneous line-up, the witness', 'sees all the line-up members at the same time', ['sees one member at a time', 'hears voices instead of seeing faces', 'sees only the suspect'], 'All faces are presented together.'),
        ('A social explanation of children’s line-up errors suggests that children', 'feel they should choose someone because an adult has asked them', ['have poorer eyesight than adults', 'cannot store faces in memory', 'are deliberately lying'], 'Pressure to give an answer is social.'),
        ('A cognitive explanation of children’s line-up errors suggests that', 'children’s memory for faces is less accurate than adults’', ['children want to please adults', 'children are afraid of the police', 'children are bored by line-ups'], 'Cognitive = memory/recognition processes.'),
    ],
    'ar': [
        ('Target-absent line-ups are important in research on eyewitnesses.', 'In real cases the police may have the wrong suspect.', 'AR', 'If the suspect is innocent, the line-up is effectively target-absent.'),
        ('Children always make more errors than adults in every type of line-up.', 'Children may feel pressure to choose someone.', 'R', 'A is false: in target-present line-ups children can be as accurate as adults; R is true.'),
    ],
    'explain': [
        ('Explain the difference between a target-present and a target-absent line-up.', 'In a target-present line-up the culprit is included among foils, so the correct response is to identify them; in a target-absent line-up the culprit is not included, so the correct response is to reject the line-up.', '1 mark each, contrasted [2]'),
        ('Explain why false identifications from line-ups are a serious problem.', 'An innocent person may be convicted because juries find eyewitness identification convincing, while the real culprit remains free.', '1 mark wrongful conviction; 1 mark culprit free/jury trust [2]'),
        ('Explain the difference between social and cognitive explanations of children’s errors in line-ups.', 'Cognitive explanations say children’s memory or face-recognition processes are weaker; social explanations say children have the memory but feel pressure to pick someone to please or comply with an adult.', '1 mark cognitive; 1 mark social [2]'),
    ],
    'claims': [
        ('A foil in a line-up is the person the police suspect.', False, 'A foil is a known-innocent person who resembles the description; the suspect is the person police think may be the culprit.'),
        ('Warning a witness that the culprit may not be present is designed to reduce false identifications.', True, 'An unbiased instruction reduces pressure to choose.'),
    ],
    'apply': [
        ('A 6-year-old, {person}, saw a man steal a bicycle in a park in {city}. The police plan to show {person} a line-up.',
         [('Explain why the police should tell {person} that the thief may not be in the line-up.', 'Children may feel they must choose someone; an unbiased warning reduces pressure and false identifications.', '1 mark pressure to choose; 1 mark reduces false IDs [2]'),
          ('Explain why {person} might identify an innocent person even if {person}’s memory is good.', 'Social pressure: {person} may want to please the adult questioner and assume they are expected to choose someone.', '1 mark social pressure; 1 mark applied [2]'),
          ('Suggest one other way the police could make the line-up more suitable for a child.', 'Use an elimination line-up (first choose who looks most like the thief, then decide if that person is the thief) or include a “not there” option such as a silhouette card.', '1 mark procedure; 1 mark explanation [2]')]),
    ],
})

c7b = T('Procedure and results: target-present and target-absent line-ups in children and adults', 'procedure results target-present target-absent line-ups children adults')
build(c7b, {
    'mcq': [
        ('Which two groups of participants were compared in Pozzulo et al.’s study?', 'Young children and adults', ['Teenagers and older adults', 'Police officers and lawyers', 'Children with and without autism'], 'Age group was a naturally occurring IV.'),
        ('In target-absent line-ups, children in Pozzulo et al.’s study were more likely than adults to', 'make a false identification', ['reject the line-up correctly', 'refuse to take part', 'identify the culprit'], 'Children chose someone more often when the target was absent.'),
        ('In target-present line-ups, children’s accuracy compared with adults’ was', 'similar', ['always much worse', 'zero', 'always perfect'], 'Children performed comparably when the culprit was present.'),
        ('Pozzulo et al.’s study is part of which approach?', 'The cognitive approach', ['The biological approach', 'The learning approach', 'The social approach only'], 'It investigates recognition memory.'),
    ],
    'explain': [
        ('Describe the general procedure of Pozzulo et al.’s study.', 'Children and adults were shown target stimuli and then asked to make identifications from line-ups that were either target-present or target-absent; their identification decisions (correct identifications, false identifications and correct rejections) were compared.', '1 mark groups; 1 mark TP and TA line-ups; 1 mark decisions compared [3]'),
        ('Describe the main finding of Pozzulo et al.’s study about target-absent line-ups.', 'Children made more false identifications (and fewer correct rejections) than adults when the target was absent, even though they were similar to adults when the target was present.', '1 mark TA more errors; 1 mark comparison with TP [2]'),
        ('Explain why Pozzulo et al. compared target-present and target-absent line-ups.', 'Comparing both shows whether children’s errors are due to poor recognition (which would affect TP too) or to a tendency to choose (which mainly affects TA).', '1 mark: separates recognition from choosing; 1 mark: explained [2]'),
    ],
    'claims': [
        ('Pozzulo et al. found that children were worse than adults at every type of line-up.', False, 'The main age difference appeared in target-absent line-ups.'),
        ('The age of participants in Pozzulo et al.’s study could not be manipulated by the researchers.', True, 'Age is a naturally occurring variable, so this is a quasi or natural experiment comparison.'),
    ],
})
add_tally_pct(c7b, ['The table shows identification decisions in a line-up study in {city}.', '{person} recorded correct and incorrect decisions for children and adults in different line-ups.'],
              [('Children, target-present', (14, 22), (8, 16)), ('Adults, target-present', (15, 23), (7, 15)), ('Children, target-absent', (5, 12), (14, 25)), ('Adults, target-absent', (14, 24), (6, 14))],
              ('correct decision', 'incorrect decision', 'decisions'))

c7c = T('Evaluation: applications to the legal system; children and psychology debate', 'evaluation applications legal system children psychology debate')
build(c7c, {
    'mcq': [
        ('Which change to police procedure is best supported by research on children’s line-up errors?', 'Telling the child that the culprit may or may not be present', ['Showing the suspect alone', 'Telling the child the culprit is definitely there', 'Rewarding the child for choosing someone'], 'Unbiased instructions reduce false identifications.'),
        ('The “children and psychology” debate concerns', 'how research with children should be conducted and what it shows about development', ['whether children should study psychology', 'how adults remember their childhood', 'whether animals can be compared with children'], 'It includes ethics, consent and developmental differences.'),
    ],
    'explain': [
        ('Explain how Pozzulo et al.’s findings could be applied to the legal system.', 'Police and courts should recognise that children may choose an innocent person from a target-absent line-up; line-ups for children should use unbiased instructions and procedures that make “not there” an easy response.', '1 mark issue; 1 mark specific application [2]'),
        ('Explain one ethical issue in research with child witnesses.', 'Children cannot give fully informed consent, so parents must consent; children may feel distressed or think they failed, so they must be reassured and debriefed.', '1 mark issue; 1 mark how dealt with [2]'),
    ],
    'claims': [
        ('Research on child witnesses suggests that children should never give evidence.', False, 'It suggests procedures should be adapted, because children can be accurate, especially when the culprit is present.'),
        ('The findings of line-up studies may lack ecological validity.', True, 'Participants are not as stressed and know the event is not real, unlike real witnesses.'),
    ],
    'apply': [
        ('A police force in {city} asks psychologists for advice on interviewing child witnesses after a series of incorrect identifications.',
         [('Use research on children’s line-up errors to explain why the incorrect identifications may have occurred.', 'Children may have chosen someone from target-absent line-ups because they felt pressure to give an answer, as research shows more false identifications by children when the culprit is absent.', '1 mark finding; 1 mark explanation [2]'),
          ('Suggest two changes the police could make.', 'Give unbiased instructions that the culprit may not be present; use an elimination or wildcard line-up with a clear “not there” option; make sure the officer does not know who the suspect is.', '1 mark each change [2]'),
          ('Explain one reason why laboratory findings might not apply to these real cases.', 'Real crimes are stressful and the stakes are high; children may be more anxious, so accuracy may differ from the study.', '1 mark difference; 1 mark consequence [2]')]),
    ],
})
chapter(7, [c7a, c7b, c7c], PZ_STUDY)


# ============================================================== CHAPTER 8: Bandura et al. (1961)

BA = 'Bandura et al.’s (1961) study of the transmission of aggression'
BA_STUDY = {
    'who': BA,
    'evals': [
        ('controls', 'strength', 'Children were matched on pre-existing aggression, and models followed a standardised script for ten minutes, so differences in imitation can be attributed to the model’s behaviour.'),
        ('inter-rater reliability', 'strength', 'Children’s aggression ratings were checked by two raters (r = 0.89), and the test-phase behaviour was observed through a one-way mirror by more than one observer, so the observations were reliable.'),
        ('quantitative data', 'strength', 'Imitative aggressive acts were counted in 5-second intervals over 20 minutes, giving numerical data that allowed clear comparisons between conditions.'),
        ('ecological validity', 'weakness', 'Children watched an unfamiliar adult attack a Bobo doll in an unfamiliar room for a short time, which is unlike learning aggression from family or media in everyday life.'),
        ('ethics', 'weakness', 'Children were exposed to aggressive models and were deliberately frustrated (mild aggression arousal), which may have caused distress and taught aggressive behaviour.'),
        ('generalisability', 'weakness', 'All 72 children came from one university nursery (Stanford) and were aged about 3–6, so the findings may not apply to other children.'),
        ('demand characteristics', 'weakness', 'A Bobo doll is designed to be hit, so children may have thought they were expected to hit it rather than imitating aggression.'),
    ],
    'essays': [
        ('aggression is learned through observation',
         ['Children who saw an aggressive model imitated specific physical and verbal acts that controls rarely showed.', 'Same-sex models were often imitated more, consistent with social learning theory.'],
         ['Boys were more physically aggressive than girls in all conditions, suggesting biological influences.', 'Hitting a Bobo doll may be play rather than real aggression.', 'The study measured immediate imitation, not long-term aggression.'],
         ['nature versus nurture', 'ecological validity', 'ethics']),
        ('the ethical problems of Bandura et al.’s study outweigh its usefulness',
         ['Children were exposed to violence and frustrated deliberately.', 'Children could not consent.'],
         ['The findings informed debates about violence in media and the importance of role models.', 'The aggression was directed at a toy and the procedure was short.'],
         ['protection from harm', 'usefulness', 'children and psychology']),
    ],
    'exp': [dict(intro=['A nursery in {city} carried out a small replication of Bandura et al. {n} children watched an aggressive model with a Bobo doll and {n} watched a non-aggressive model; the number of imitative aggressive acts in a 20-minute play session was recorded.',
                        '{person} counted imitative aggressive acts during 20 minutes of play for children who had seen either an aggressive or a non-aggressive adult model.'],
                 A='aggressive model', B='non-aggressive model', gA='children who observe an aggressive model', gB='children who observe a non-aggressive model',
                 more='will show more imitative aggressive acts than', measure='the number of imitative aggressive acts', dvshort='Imitative aggressive acts in 20 minutes',
                 iv='whether children observed an aggressive or a non-aggressive model', dv='the number of imitative aggressive acts (for example hitting Bobo with the mallet) recorded in 20 minutes',
                 range=(0, 40), base=(1, 4), diff=(8, 16), sd=4,
                 controls=['matching the children on their usual level of aggression before allocating them', 'the same model script, room and toys for every child', 'the same frustration stage before the test for every child'],
                 ethics=['protection from harm: children should not be distressed or taught aggression; the session should stop if a child is upset', 'parental consent and a debrief, with the child playing with the non-aggressive model afterwards'],
                 concl_A='children imitate aggression that they observe in an adult model.', concl_B='children imitate non-aggressive models more.')],
    'obs': [dict(intro=['Two observers watched the same 20-minute play session through a one-way mirror in a nursery in {city} and tallied children’s behaviours.',
                        '{person} and a second observer independently recorded the behaviour of children in a playroom using the same categories.'],
                 cats=['imitative physical aggression', 'imitative verbal aggression', 'mallet aggression', 'punching Bobo', 'aggressive gun play', 'non-aggressive play with tea set'], tally=(3, 20),
                 kind='a covert, controlled', kind_plus='The children could not see the observers behind the one-way mirror, so they behaved more naturally and demand characteristics were reduced.',
                 kind_minus='The playroom was an unfamiliar, artificial setting with specific toys, so behaviour may not reflect how children act at home or school.',
                 ethics=['parents must give consent because children are observed without knowing', 'children should not be left distressed after the frustration stage'])],
    'plan': [('whether children copy helpful behaviour that they see on video', 'IV: helpful or neutral video', 'DV: number of helpful acts in a play session', ['laboratory experiment', 'observation']),
             ('whether the amount of violent video games played is related to aggressive attitudes', 'co-variable 1: hours of violent games per week', 'co-variable 2: aggression questionnaire score', ['correlation', 'questionnaire'])],
}

c8a = T('Background: social learning theory and imitation', 'social learning theory imitation')
build(c8a, {
    'terms': [
        ('social learning theory', 'the theory that behaviour is learned by observing and imitating others, especially role models'),
        ('imitation', 'copying the behaviour of another person'),
        ('role model', 'a person whose behaviour is observed and copied, often because they are similar or have high status'),
        ('vicarious reinforcement', 'learning through seeing another person being rewarded for a behaviour'),
        ('identification', 'feeling similar to a model and wanting to be like them, which makes imitation more likely'),
        ('learning approach', 'the view that behaviour is acquired through experience, for example by conditioning or observation'),
    ],
    'mcq': [
        ('According to social learning theory, behaviour is learned mainly through', 'observing and imitating models', ['inherited genes', 'association of two stimuli only', 'unconscious conflicts'], 'Observational learning is the key process.'),
        ('Which model is a child most likely to imitate, according to social learning theory?', 'A same-sex adult with high status', ['A stranger who is punished', 'An animal', 'A model they cannot see'], 'Similarity and status increase identification.'),
        ('Watching an older sibling receive praise for tidying their room and then tidying your own is an example of', 'vicarious reinforcement', ['classical conditioning', 'negative punishment', 'extinction'], 'Learning from others’ rewards.'),
    ],
    'ar': [
        ('Bandura et al.’s study belongs to the learning approach.', 'It investigated whether aggression could be acquired by observing a model.', 'AR', 'Observational learning is part of the learning approach.'),
    ],
    'explain': [
        ('Explain how social learning theory differs from operant conditioning.', 'Operant conditioning requires the learner to perform a behaviour and be reinforced; social learning theory says behaviour can be learned simply by observing a model, without direct reinforcement.', '1 mark operant; 1 mark observational learning contrasted [2]'),
        ('Explain why children might imitate a same-sex model more than an opposite-sex model.', 'Children identify with models who are similar to them, and same-sex behaviour is more likely to be seen as appropriate and rewarded in their culture.', '1 mark similarity/identification; 1 mark appropriateness [2]'),
    ],
    'claims': [
        ('Social learning theory says children must be rewarded directly before they will copy a behaviour.', False, 'Children can learn by observation alone; vicarious reinforcement can increase imitation.'),
        ('Bandura et al. aimed to see whether children would imitate aggression in a new setting without the model present.', True, 'Imitation was tested in a different room after the model had gone.'),
    ],
    'apply': [
        ('{person}, aged 5, starts copying wrestling moves on a younger cousin after watching wrestling on television with an older brother in {city}.',
         [('Use social learning theory to explain {person}’s behaviour.', '{person} observed models (wrestlers, older brother) performing aggressive moves and imitated them; the wrestlers may have been seen as rewarded (cheered), which is vicarious reinforcement.', '1 mark observation/imitation; 1 mark vicarious reinforcement or identification [2]'),
          ('Explain why the older brother may be a particularly strong role model.', 'He is the same sex, familiar and of higher status, so {person} identifies with him.', '1 mark feature; 1 mark identification [2]'),
          ('Suggest how {person}’s parents could reduce the behaviour, using learning principles.', 'Model and praise gentle play, avoid watching violent programmes together, and do not reward the wrestling with attention.', '1 mark modelling/rewards; 1 mark explained [2]')]),
    ],
})

c8b = T('Procedure and results: Bobo doll experiment with aggressive and non-aggressive models', 'procedure results bobo doll aggressive non-aggressive models')
build(c8b, {
    'mcq': [
        ('How many children took part in Bandura et al.’s (1961) study?', '72', ['40', '24', '9'], '36 boys and 36 girls.'),
        ('How long did the model behave aggressively towards the Bobo doll?', 'About 10 minutes', ['About 30 seconds', 'About 2 hours', 'About 1 minute'], 'The model was in the room for about 10 minutes.'),
        ('What happened in the second stage (mild aggression arousal)?', 'Children were shown attractive toys and then told they were for other children', ['Children were punished', 'Children watched a second model', 'Children were praised for being calm'], 'The frustration took place about 2 minutes after they began playing.'),
        ('How long was each child observed in the final room?', '20 minutes', ['5 minutes', '1 hour', '10 seconds'], 'Behaviour was recorded in 5-second intervals.'),
        ('Through what were the children observed in the final stage?', 'A one-way mirror', ['A video link from another country', 'A hole in the door', 'They were not observed'], 'Observers were hidden behind a one-way mirror.'),
        ('Which group showed the most imitative physical aggression?', 'Boys who saw a male aggressive model', ['Girls who saw a female non-aggressive model', 'The control group', 'Girls who saw a male non-aggressive model'], 'Boys with a male aggressive model had the highest mean (25.8).'),
        ('How many children were in the control group, who saw no model?', '24', ['12', '48', '36'], '24 control and 48 experimental children.'),
    ],
    'ar': [
        ('Children were matched on aggression before the study.', 'Bandura et al. wanted to control for children’s pre-existing aggressiveness.', 'AR', 'Matching was the control for individual differences in aggression.'),
        ('Girls showed more imitative physical aggression than boys.', 'Both male and female models were used in the study.', 'R', 'A is false: boys showed more imitative physical aggression; R is true but does not support A.'),
    ],
    'explain': [
        ('Describe the three stages of Bandura et al.’s procedure.', 'Stage 1: each child played in a room while an adult model behaved aggressively or non-aggressively towards a Bobo doll (or there was no model). Stage 2: the child was taken to another room with attractive toys and mildly frustrated by being told they were for others. Stage 3: the child spent 20 minutes in a room with aggressive and non-aggressive toys, including a Bobo doll, observed through a one-way mirror.', '1 mark per stage [3]'),
        ('Describe how children were allocated to conditions in Bandura et al.’s study.', 'Children were rated for pre-existing aggression by an experimenter and a teacher, then matched in threes and allocated to aggressive model, non-aggressive model and control groups, with same- and opposite-sex models.', '1 mark rating; 1 mark matching in threes; 1 mark groups [3]'),
        ('Describe two findings of Bandura et al.’s study.', 'Children who saw aggressive models showed much more imitative physical and verbal aggression than other groups; boys were more physically aggressive than girls; same-sex models were often imitated more, especially by boys; male models had a greater influence.', '1 mark each finding [2]'),
        ('Explain why the children were frustrated before the test phase.', 'Being frustrated made them more likely to express aggression, so that differences in imitation would show; it also equalised arousal across conditions, including non-aggressive groups.', '1 mark increase likelihood of aggression; 1 mark same for all groups [2]'),
    ],
    'claims': [
        ('In Bandura et al.’s study, children were rewarded for copying the model.', False, 'No reinforcement was given; the study showed learning by observation alone.'),
        ('The model used specific verbal phrases such as “Sock him in the nose” and “Pow”.', True, 'Distinctive phrases allowed imitative verbal aggression to be identified.'),
    ],
})

c8c = T('Evaluation: ethics, validity and nature versus nurture', 'evaluation ethics validity nature versus nurture')
build(c8c, {
    'mcq': [
        ('Which finding of Bandura et al.’s study supports a nature (biological) explanation?', 'Boys were more physically aggressive than girls in every condition', ['Children imitated specific phrases', 'The control group showed little imitation', 'Children copied non-aggressive models'], 'A consistent sex difference could reflect biology.'),
        ('Which is the main ethical problem in Bandura et al.’s study?', 'Children were exposed to aggression and deliberately frustrated', ['Children were paid', 'Children were interviewed', 'Children were told the aims'], 'Risk of harm and learned aggression.'),
    ],
    'explain': [
        ('Explain why the Bobo doll study may not be a valid measure of real aggression.', 'Bobo is a toy designed to be hit, so hitting it may be play rather than intended harm, and the setting was unfamiliar; this may not reflect aggression towards people in everyday life.', '1 mark toy designed to be hit/play; 1 mark consequence [2]'),
        ('Explain how Bandura et al.’s study contributes to the nature versus nurture debate.', 'Children who saw aggression imitated it, supporting nurture (learning); but boys were more physically aggressive overall, suggesting nature also plays a part.', '1 mark nurture evidence; 1 mark nature evidence [2]'),
    ],
    'claims': [
        ('Bandura et al.’s study is high in ecological validity because it took place in a nursery.', False, 'The rooms were set up specially, the model was a stranger and exposure was brief, so the situation was artificial.'),
        ('Long-term effects on the children were not measured.', True, 'Imitation was measured immediately, so we do not know whether aggression lasted.'),
    ],
})
chapter(8, [c8a, c8b, c8c], BA_STUDY)


# ============================================================== CHAPTER 9: Fagen et al. (2014)

FA = 'Fagen et al.’s (2014) study of elephant learning'
FA_STUDY = {
    'who': FA,
    'evals': [
        ('ethics', 'strength', 'Positive reinforcement with food rewards replaced traditional training that relies on punishment, so the elephants were trained without fear or pain, improving their welfare.'),
        ('usefulness', 'strength', 'The trunk wash allows elephants to be tested for tuberculosis safely, and the method shows mahouts an effective, humane alternative to traditional training.'),
        ('ecological validity', 'strength', 'Training took place in the elephants’ normal environment with their own mahouts, so the behaviour was learned in real working conditions.'),
        ('quantitative data', 'strength', 'Progress was recorded as the number of sessions needed to reach each step, so learning could be compared across elephants.'),
        ('generalisability', 'weakness', 'Only five young elephants from one centre in Nepal were trained, so the results may not apply to older elephants or other species.'),
        ('controls', 'weakness', 'There was no control group trained with traditional methods, so we cannot be sure positive reinforcement was more effective than other methods.'),
        ('reliability', 'weakness', 'Each elephant had a different mahout and individual temperament, so the procedure was not identical for all animals and may be hard to replicate exactly.'),
    ],
    'essays': [
        ('operant conditioning is the most effective way of training animals',
         ['Fagen et al. trained young elephants to perform a complex trunk wash using shaping and positive reinforcement.', 'Reinforcement-based training is humane and builds cooperation.'],
         ['Not every animal learned the full behaviour, so individual differences matter.', 'There was no comparison with other methods.', 'Some behaviours may be learned by observation or be partly innate.'],
         ['positive reinforcement', 'shaping', 'animal welfare']),
        ('research using animals is justified when it improves animal welfare',
         ['Fagen et al.’s training helped elephants receive health checks without force.', 'Animals benefit directly, so the costs are low.'],
         ['Captive animals cannot consent and their captivity itself may cause stress.', 'Findings may not generalise.'],
         ['ethics of animal research', 'usefulness']),
    ],
    'exp': [dict(intro=['An elephant centre near {city} compared the number of training sessions needed to learn a trunk wash for {n} elephants trained with food rewards and {n} elephants trained with verbal praise only.',
                        '{person} recorded how many sessions young elephants needed to complete a trunk wash when trained with food rewards or with praise only.'],
                 A='food rewards', B='praise only', gA='elephants trained with food rewards', gB='elephants trained with praise only',
                 more='will need fewer training sessions than', measure='the number of sessions needed', dvshort='Training sessions needed', higher='B', nosample=True,
                 iv='whether the elephants were trained with food rewards or praise only', dv='the number of training sessions needed to complete the trunk wash correctly',
                 range=(8, 60), base=(18, 24), diff=(6, 14), sd=5,
                 controls=['the same steps of the shaping sequence for all elephants', 'sessions of the same length at the same time of day', 'elephants of similar age'],
                 ethics=['the elephants must not be deprived of food to increase motivation', 'training should stop if an elephant shows signs of stress'],
                 concl_A='food rewards slow down learning compared with praise.', concl_B='food rewards lead to faster learning than praise alone.')],
    'plan': [('whether dogs learn a new trick faster with food rewards or with praise', 'IV: food rewards or praise', 'DV: number of trials to learn the trick', ['field experiment']),
             ('how zoo visitors’ behaviour affects animals in an enclosure', 'behaviour: animal responses', 'categories: approaching, hiding, pacing', ['observation'])],
}

c9a = T('Background: operant conditioning, positive reinforcement and shaping', 'operant conditioning positive reinforcement shaping')
build(c9a, {
    'terms': [
        ('operant conditioning', 'learning in which the consequences of a behaviour change how likely it is to be repeated'),
        ('positive reinforcement', 'increasing a behaviour by adding something pleasant after it'),
        ('negative reinforcement', 'increasing a behaviour by removing something unpleasant after it'),
        ('punishment', 'a consequence that decreases the likelihood of a behaviour being repeated'),
        ('shaping', 'reinforcing successive approximations of a target behaviour until the full behaviour is performed'),
        ('bridging stimulus', 'a signal, such as a word or whistle, given at the exact moment of the correct behaviour to show that a reward will follow'),
        ('primary reinforcer', 'a reward that satisfies a biological need, such as food'),
    ],
    'mcq': [
        ('Giving an elephant a piece of fruit when it lifts its trunk on command is an example of', 'positive reinforcement', ['negative reinforcement', 'punishment', 'classical conditioning'], 'Something pleasant is added to increase the behaviour.'),
        ('Rewarding closer and closer approximations to a target behaviour is called', 'shaping', ['extinction', 'generalisation', 'flooding'], 'Successive approximations are reinforced.'),
        ('Which psychologist is most closely associated with operant conditioning?', 'B. F. Skinner', ['Ivan Pavlov', 'Albert Bandura', 'Stanley Milgram'], 'Skinner studied reinforcement with animals.'),
        ('Taking an umbrella to avoid getting wet is an example of', 'negative reinforcement', ['positive reinforcement', 'punishment', 'shaping'], 'Avoiding something unpleasant strengthens the behaviour.'),
    ],
    'ar': [
        ('A bridging stimulus helps animals learn which behaviour is being rewarded.', 'It marks the exact moment the correct behaviour occurs, before the food arrives.', 'AR', 'Precise timing links the behaviour and the reward.'),
        ('Negative reinforcement decreases the likelihood of a behaviour.', 'Negative reinforcement involves removing an unpleasant stimulus.', 'R', 'A is false: negative reinforcement increases behaviour; R is true.'),
    ],
    'explain': [
        ('Explain the difference between positive reinforcement and punishment.', 'Positive reinforcement adds a pleasant consequence so a behaviour becomes more likely; punishment gives an unpleasant consequence (or removes a pleasant one) so a behaviour becomes less likely.', '1 mark each, contrasted [2]'),
        ('Explain why shaping is needed to train a complex behaviour such as a trunk wash.', 'An animal is unlikely to perform the whole behaviour by chance, so each step (lifting the trunk, holding liquid, blowing into a bag) is reinforced in turn until the full sequence is produced.', '1 mark complex behaviour unlikely spontaneously; 1 mark steps reinforced [2]'),
    ],
    'claims': [
        ('Traditional elephant training in some countries has relied on punishment and fear.', True, 'Methods such as the use of a bullhook rely on pain, which is why reinforcement-based alternatives were tested.'),
        ('In shaping, the animal is only rewarded when it performs the complete behaviour perfectly.', False, 'Shaping rewards each closer approximation, not just the final behaviour.'),
    ],
    'apply': [
        ('{person} is training a puppy in {city} to sit and stay. {person} says “Yes!” the moment the puppy sits, then gives it a treat.',
         [('Identify the type of reinforcement {person} is using.', 'Positive reinforcement (adding a treat).', '1 mark [1]'),
          ('Explain the purpose of saying “Yes!” before giving the treat.', 'It is a bridging stimulus (secondary reinforcer) that marks the exact moment of sitting, so the puppy links the behaviour, not something it does later, with the reward.', '1 mark bridge; 1 mark timing [2]'),
          ('Describe how {person} could use shaping to teach the puppy to stay for 30 seconds.', 'Reward a stay of 2 seconds, then gradually increase the time required (5, 10, 20, 30 seconds) before rewarding.', '1 mark small steps; 1 mark gradually increased criterion [2]'),
          ('Explain why punishment would be less suitable than reinforcement.', 'Punishment may cause fear or aggression and does not show the puppy what to do instead; reinforcement builds a positive relationship.', '1 mark problem; 1 mark comparison [2]')]),
    ],
})

c9b = T('Procedure and results: training elephants for trunk wash in Nepal', 'procedure results training elephants trunk wash nepal')
build(c9b, {
    'mcq': [
        ('Why did the elephants in Fagen et al.’s study need to learn a trunk wash?', 'So that they could be tested for tuberculosis', ['So that they could perform for tourists', 'So that they could drink more water', 'So that they could be weighed'], 'Trunk-wash samples are used to detect TB.'),
        ('In which country were the elephants in Fagen et al.’s study trained?', 'Nepal', ['India', 'Kenya', 'Thailand'], 'The elephants were at a centre in Chitwan, Nepal.'),
        ('Who carried out the day-to-day training of the elephants?', 'Their mahouts (handlers), guided by the researchers', ['Veterinary surgeons only', 'Tourists', 'Other elephants'], 'Mahouts were taught positive reinforcement techniques.'),
        ('Which of these was a step in the trunk-wash behaviour?', 'Lifting the trunk so that saline solution could be put in', ['Lying down for an X-ray', 'Standing on a platform for weighing', 'Opening the mouth for a tooth check'], 'Trunk up, hold saline, lower trunk and blow into a container.'),
    ],
    'explain': [
        ('Describe how the elephants in Fagen et al.’s study were trained.', 'Mahouts used positive reinforcement: a bridging signal marked each correct response and food rewards followed; the trunk wash was broken into steps (target the trunk upwards, accept saline, hold, then lower and blow into a bag) and each step was shaped in sessions over several weeks.', '1 mark positive reinforcement/food; 1 mark bridge; 1 mark shaping steps [3]'),
        ('Describe the results of Fagen et al.’s study.', 'Most of the young elephants learned the complete trunk-wash behaviour within a few weeks of training, showing that positive reinforcement can teach a complex medical behaviour; elephants differed in how quickly they progressed.', '1 mark most learned; 1 mark individual differences/time [2]'),
        ('Explain why Fagen et al. used a target stick in training.', 'The elephant learns to touch or follow the target, so the trainer can guide the trunk into position (for example up) and reinforce it, making shaping easier.', '1 mark guides behaviour; 1 mark reinforced/shaping [2]'),
    ],
    'claims': [
        ('Fagen et al. used punishment to stop elephants moving during the trunk wash.', False, 'The study used positive reinforcement only, as an alternative to traditional punishment-based training.'),
        ('Fagen et al.’s study can be described as a series of case studies of individual elephants.', True, 'Each elephant’s progress was tracked separately.'),
    ],
})
add_tally_pct(c9b, ['The table shows the number of correct and incorrect trunk-wash attempts in the final week of training for several elephants near {city}.', '{person} recorded correct and incorrect attempts for each elephant during the last week of training.'],
              [('Elephant A', (15, 28), (1, 6)), ('Elephant B', (10, 22), (3, 9)), ('Elephant C', (6, 14), (6, 14)), ('Elephant D', (18, 30), (2, 5)), ('Elephant E', (12, 20), (4, 10))],
              ('correct', 'incorrect', 'attempts'))

c9c = T('Evaluation: animal ethics and application to captive animal welfare', 'evaluation animal ethics application captive animal welfare')
build(c9c, {
    'mcq': [
        ('Which is the strongest ethical strength of Fagen et al.’s study?', 'It used positive reinforcement instead of punishment', ['It used a large sample', 'It took place in a laboratory', 'It used deception'], 'Humane training improves welfare.'),
        ('How could Fagen et al.’s findings improve the welfare of captive animals?', 'By showing keepers how to obtain medical samples without force', ['By showing that animals cannot learn', 'By increasing the use of chains', 'By reducing food for animals'], 'Cooperative medical behaviours reduce stress.'),
    ],
    'explain': [
        ('Explain one way Fagen et al.’s study can be applied to captive animal welfare.', 'Zoos and sanctuaries can use positive reinforcement to train animals to cooperate with health checks (such as trunk washes or blood samples), reducing stress and the need for restraint.', '1 mark application; 1 mark welfare benefit [2]'),
        ('Explain why the small sample in Fagen et al.’s study is a weakness.', 'With only five young elephants, individual temperament strongly affects results, so we cannot be sure the method works for older elephants or all individuals.', '1 mark small; 1 mark consequence [2]'),
    ],
    'claims': [
        ('Because Fagen et al. used animals, their findings cannot be useful.', False, 'The findings are directly useful for the welfare and health care of elephants and other captive animals.'),
        ('A comparison group trained by traditional methods would have strengthened the study.', True, 'It would allow the effectiveness of the two methods to be compared, though it would raise ethical problems.'),
    ],
    'apply': [
        ('A zoo in {city} needs to take regular blood samples from its giraffes, which currently have to be restrained.',
         [('Use Fagen et al.’s study to suggest how keepers could train the giraffes.', 'Use shaping with positive reinforcement: reward the giraffe for standing at a station, then for allowing touch on the neck, then for a small needle, using a bridge and food rewards.', '1 mark shaping; 1 mark reinforcement detail [2]'),
          ('Explain one welfare benefit of this approach.', 'Animals cooperate voluntarily, so they are less stressed than when restrained and injuries are less likely.', '1 mark benefit; 1 mark explained [2]'),
          ('Explain one problem the keepers may face.', 'Each animal learns at a different rate and some may never complete the behaviour, so training takes time and staff must be trained.', '1 mark problem; 1 mark explained [2]')]),
    ],
})
chapter(9, [c9a, c9b, c9c], FA_STUDY)


# ============================================================== CHAPTER 10: Saavedra and Silverman (2002)

SS = 'Saavedra and Silverman’s (2002) case study of a button phobia'
SS_STUDY = {
    'who': SS,
    'evals': [
        ('the case study method', 'strength', 'Studying one boy in depth over time, with interviews, ratings and follow-up, gave detailed evidence about how the phobia developed and how disgust and distress changed during treatment.'),
        ('quantitative data', 'strength', 'Distress and disgust were rated on a feeling thermometer at each step of the hierarchy, so changes during treatment could be tracked objectively.'),
        ('usefulness', 'strength', 'The study suggests that when a phobia is based on disgust, imagery exposure targeting disgust can help where exposure alone is not enough.'),
        ('generalisability', 'weakness', 'It is a case study of one 9-year-old boy with an unusual phobia, so the findings may not apply to other children or other phobias.'),
        ('self-report', 'weakness', 'Ratings and reports came from the boy and his mother, so they may be affected by demand characteristics or a wish to show improvement.'),
        ('controls', 'weakness', 'Several treatment elements were combined and there was no control condition, so it is impossible to know which element caused the improvement.'),
        ('ethics', 'strength', 'The boy received treatment that helped him, his parents consented, and his identity was protected.'),
    ],
    'essays': [
        ('phobias are best explained by classical conditioning',
         ['The button phobia began after a single unpleasant event when buttons fell on the boy, consistent with conditioning.', 'Exposure therapy based on conditioning reduced his fear.'],
         ['Not everyone who has a bad experience develops a phobia, so individual factors matter.', 'Disgust, a cognitive and emotional response, had to be treated separately.', 'Biological preparedness may explain why some fears develop more easily.'],
         ['individual explanations', 'case studies', 'disgust']),
        ('case studies are the most useful way to study phobias',
         ['They allow rare phobias to be studied in depth, as Saavedra and Silverman did.', 'Detailed treatment records help clinicians.'],
         ['Findings from one person may not generalise.', 'There is no control group, so causes of improvement are unclear.'],
         ['generalisability', 'usefulness', 'validity']),
    ],
    'exp': [dict(intro=['A clinic in {city} compared distress ratings (0–8 feeling thermometer) after treatment for {n} children with phobias treated with exposure therapy and {n} children on a waiting list.',
                        '{person} measured fear on a 0–8 feeling thermometer after eight weeks for children given exposure therapy or placed on a waiting list.'],
                 A='exposure therapy', B='waiting list', gA='children who receive exposure therapy', gB='children on a waiting list',
                 more='will have lower distress ratings than', measure='distress rating', dvshort='Distress rating (0–8)', higher='B',
                 iv='whether children received exposure therapy or were on a waiting list', dv='distress rating on a 0–8 feeling thermometer when facing the feared object',
                 range=(0, 8), base=(2, 3), diff=(2, 3.5), sd=1.1,
                 controls=['the same feeling thermometer and instructions for every child', 'children of similar age and phobia severity in both groups'],
                 ethics=['the waiting-list children should be offered treatment afterwards', 'exposure must be gradual and stopped if a child becomes too distressed'],
                 concl_A='exposure therapy increases distress.', concl_B='exposure therapy reduces distress compared with no treatment.')],
    'plan': [('whether gradual exposure reduces children’s fear of dogs', 'IV: gradual exposure or no exposure', 'DV: distress rating on a feeling thermometer', ['field experiment']),
             ('how common disgust-based fears are among teenagers', 'topic: disgust-based fears', 'measure: ratings of disgust for objects and open answers', ['questionnaire', 'interview'])],
}

c10a = T('Background: classical conditioning, phobias and disgust', 'classical conditioning phobias disgust')
build(c10a, {
    'terms': [
        ('classical conditioning', 'learning in which a neutral stimulus becomes associated with an unconditioned stimulus, so that it comes to produce a conditioned response'),
        ('phobia', 'an intense, irrational and persistent fear of a specific object or situation, leading to avoidance'),
        ('unconditioned stimulus', 'a stimulus that naturally produces a response without learning'),
        ('conditioned response', 'a learned response to a previously neutral stimulus'),
        ('disgust', 'a strong feeling of revulsion that leads to avoidance of contamination'),
        ('extinction', 'the gradual disappearance of a conditioned response when the conditioned stimulus is repeatedly presented without the unconditioned stimulus'),
    ],
    'mcq': [
        ('In the classical conditioning explanation of a button phobia, buttons become', 'a conditioned stimulus', ['an unconditioned stimulus', 'an unconditioned response', 'a reinforcer'], 'A neutral stimulus paired with an unpleasant experience becomes a CS.'),
        ('What is the technical name for a fear of buttons?', 'Koumpounophobia', ['Agoraphobia', 'Arachnophobia', 'Claustrophobia'], 'Koumpounophobia is a rare phobia of buttons.'),
        ('Which researcher is associated with the conditioning of fear in “Little Albert”?', 'Watson', ['Skinner', 'Bandura', 'Freud'], 'Watson and Rayner (1920).'),
        ('Why was disgust important in Saavedra and Silverman’s case?', 'The boy’s main reaction to buttons was disgust rather than fear alone', ['Disgust cannot be learned', 'Disgust was the treatment', 'The boy had no emotional reaction'], 'Disgust-based phobias may need different treatment.'),
    ],
    'ar': [
        ('A phobia can develop after a single frightening experience.', 'Classical conditioning can occur after one strong pairing of a neutral stimulus with an unpleasant event.', 'AR', 'One-trial learning explains rapid onset.'),
    ],
    'explain': [
        ('Use classical conditioning to explain how the boy in Saavedra and Silverman’s study developed his button phobia.', 'Buttons (neutral stimulus) were paired with the shock and embarrassment of a bowl of buttons falling on him (unconditioned stimulus, producing distress); buttons became a conditioned stimulus that produced a conditioned response of distress and disgust.', '1 mark NS → CS; 1 mark UCS/UCR; 1 mark CR [3]'),
        ('Explain why disgust-based phobias may be harder to treat than fear-based phobias.', 'Disgust appears to extinguish more slowly than fear during exposure, so a person may stop feeling afraid but still feel disgusted and continue avoiding the object.', '1 mark disgust slower to extinguish; 1 mark consequence [2]'),
    ],
    'claims': [
        ('Classical conditioning can explain why a phobia is maintained over time.', False, 'Classical conditioning explains acquisition; maintenance is often explained by negative reinforcement of avoidance (operant conditioning).'),
        ('A phobia involves fear that is out of proportion to any real danger.', True, 'That is why it is described as irrational.'),
    ],
    'apply': [
        ('{person}, aged 10, from {city}, became very afraid of balloons after one burst loudly near her face at a party. She now leaves the room whenever she sees one.',
         [('Identify the neutral stimulus and the unconditioned stimulus.', 'Neutral stimulus: the balloon. Unconditioned stimulus: the loud bang near her face.', '1 mark each [2]'),
          ('Explain why {person} continues to avoid balloons.', 'Leaving the room reduces her anxiety, which negatively reinforces avoidance; she never learns that balloons are usually harmless, so the fear does not extinguish.', '1 mark negative reinforcement; 1 mark no extinction [2]'),
          ('Suggest how exposure could be used to help {person}.', 'Build a hierarchy from pictures of balloons to holding an uninflated balloon to being near inflated balloons, moving up only when distress falls.', '1 mark hierarchy; 1 mark gradual exposure [2]')]),
    ],
})

c10b = T('Procedure and results: exposure-based cognitive-behavioural therapy case study', 'procedure results exposure-based cognitive-behavioural therapy case study')
build(c10b, {
    'mcq': [
        ('How old was the boy at the start of treatment in Saavedra and Silverman’s study?', '9 years old', ['5 years old', '14 years old', '19 years old'], 'His phobia had started at age 5.'),
        ('What did the boy rate on the “feeling thermometer”?', 'His distress and disgust', ['His body temperature', 'His intelligence', 'His sleep quality'], 'Ratings from 0 to 8.'),
        ('Which buttons did the boy find most distressing?', 'Small plastic buttons', ['Large denim jeans buttons', 'Metal buttons on uniforms', 'Wooden toggles'], 'Small, clear plastic buttons were at the top of the hierarchy.'),
        ('How many steps were in the boy’s hierarchy?', '12', ['3', '50', '100'], 'A 12-step stimulus hierarchy was used.'),
        ('When was the boy’s progress followed up?', 'At 6 and 12 months after treatment', ['After one day', 'After ten years', 'It was not followed up'], 'Gains were maintained at follow-up.'),
    ],
    'ar': [
        ('Imagery exposure in Saavedra and Silverman’s study focused on disgust.', 'The boy’s disgust ratings had not fallen as much as his distress during exposure with rewards.', 'AR', 'Disgust remained, so disgust imagery was added.'),
    ],
    'explain': [
        ('Describe the treatment used by Saavedra and Silverman.', 'Exposure-based CBT: the boy worked through a 12-step hierarchy of buttons with contingency management (praise and rewards for approaching), then imagery exposure in which he imagined disgusting button-related scenes, plus self-control strategies (coping thoughts); he rated distress and disgust throughout.', '1 mark hierarchy/exposure; 1 mark reinforcement; 1 mark disgust imagery; 1 mark ratings [4]'),
        ('Describe the results of Saavedra and Silverman’s study.', 'Distress decreased during exposure with rewards, but disgust stayed higher until disgust-focused imagery was added; after treatment and at 6- and 12-month follow-up he no longer met the criteria for a phobia and could wear clothes with buttons.', '1 mark distress fell; 1 mark disgust needed imagery; 1 mark follow-up [3]'),
        ('Explain why a stimulus hierarchy was used in this treatment.', 'It allowed the boy to face buttons gradually, starting with the least distressing (large denim buttons) and moving to the most (small plastic buttons), so anxiety stayed manageable and could reduce at each step.', '1 mark graded; 1 mark manageable/extinction [2]'),
    ],
    'claims': [
        ('The boy in Saavedra and Silverman’s study developed his phobia after buttons fell on him at school.', True, 'At age 5 he knocked over a bowl of buttons in his kindergarten class and they fell on him.'),
        ('Saavedra and Silverman found that the boy’s disgust disappeared after the first session.', False, 'Disgust was slower to change and needed imagery-based exposure.'),
    ],
})

c10c = T('Evaluation: generalisability, individual explanations and usefulness', 'evaluation generalisability individual explanations usefulness')
build(c10c, {
    'mcq': [
        ('Why is it difficult to generalise from Saavedra and Silverman’s study?', 'It studied one boy with an unusual phobia', ['It used thousands of participants', 'It was a laboratory experiment', 'It used animals'], 'Case study of one person.'),
        ('The study suggests that treatment for some phobias should also target', 'disgust', ['intelligence', 'sleep patterns', 'obedience'], 'Disgust-focused imagery was needed.'),
    ],
    'explain': [
        ('Explain why Saavedra and Silverman’s study supports an individual explanation of behaviour.', 'The phobia developed from the boy’s own experience and disgust sensitivity, and treatment was tailored to him; other children with the same experience might not develop a phobia.', '1 mark individual experience/characteristics; 1 mark tailored treatment [2]'),
        ('Explain one way the study is useful to therapists.', 'It shows that measuring both fear and disgust is important, and that disgust-focused imagery can be added when exposure reduces fear but not disgust.', '1 mark use; 1 mark explained [2]'),
    ],
    'claims': [
        ('Because it is a case study, Saavedra and Silverman’s study has no value.', False, 'Case studies give detailed, useful insight into rare conditions and treatments, even though generalisation is limited.'),
        ('The follow-up at 12 months increases confidence that the treatment had lasting effects.', True, 'The improvement was maintained a year later.'),
    ],
    'apply': [
        ('A therapist in {city} is treating {person}, a teenager with a fear of cockroaches that involves strong disgust.',
         [('Use Saavedra and Silverman’s findings to suggest how the therapist should measure progress.', 'Ask {person} to rate both distress and disgust (for example on a 0–8 feeling thermometer) at each step of a hierarchy.', '1 mark both measures; 1 mark rating scale [2]'),
          ('Explain why exposure alone might not be enough.', 'Disgust may extinguish more slowly than fear, so {person} could stop being afraid but still avoid cockroaches because of disgust.', '1 mark disgust slower; 1 mark consequence [2]'),
          ('Explain one reason why a treatment that worked for the boy in Saavedra and Silverman’s case may not work for {person}.', 'The boy was a single case with a unique history; {person}’s phobia may have a different cause, and individual differences mean responses to treatment vary.', '1 mark single case; 1 mark individual differences [2]')]),
    ],
})
chapter(10, [c10a, c10b, c10c], SS_STUDY)


# ============================================================== CHAPTER 11: Milgram (1963)

MI = 'Milgram’s (1963) study of obedience'
MI_STUDY = {
    'who': MI,
    'evals': [
        ('standardisation', 'strength', 'The experimenter used the same four verbal prods, the learner gave the same pre-recorded responses and the shock generator was identical for all 40 participants, so the procedure was highly controlled and replicable.'),
        ('quantitative and qualitative data', 'strength', 'Milgram recorded the maximum voltage given (quantitative) and observed signs of tension such as sweating, trembling and nervous laughter (qualitative), giving a fuller picture.'),
        ('reliability', 'strength', 'Milgram repeated the procedure in many variations with similar baseline results, and later replications have found comparable obedience levels.'),
        ('ethics', 'weakness', 'Participants were deceived about the shocks, experienced severe stress (three had seizures) and the prods made withdrawal difficult, breaking guidelines on protection from harm and the right to withdraw.'),
        ('ethics', 'strength', 'Participants were debriefed, reunited with the unharmed learner, and in a follow-up 84% said they were glad to have taken part.'),
        ('generalisability', 'weakness', 'All 40 participants were American men from New Haven, so the results may not apply to women or other cultures.'),
        ('ecological validity', 'weakness', 'Punishing a learner with electric shocks in a laboratory is an unusual task, so obedience in this setting may not reflect obedience in everyday life.'),
        ('validity', 'strength', 'Signs of extreme tension suggest that participants believed the shocks were real, so their behaviour was genuine rather than role-play.'),
    ],
    'essays': [
        ('obedience is best explained by situational rather than individual factors',
         ['65% of ordinary men gave the maximum 450V shock when ordered by an experimenter in a prestigious setting.', 'Milgram’s variations showed obedience changed with the situation (for example location and proximity).'],
         ['35% defied the experimenter, showing individual differences.', 'Personality factors such as authoritarianism are linked to obedience.', 'Perry et al. and Baron-Cohen et al. show that individual differences matter in social behaviour.'],
         ['situational and individual explanations', 'ethics', 'generalisability']),
        ('Milgram’s study should not have been carried out',
         ['Participants suffered extreme stress, including seizures, and were deceived.', 'The prods undermined the right to withdraw.'],
         ['The findings are important for understanding atrocities such as the Holocaust.', 'Participants were debriefed and most were glad to have taken part.', 'Milgram could not predict the levels of distress.'],
         ['protection from harm', 'deception', 'usefulness']),
    ],
    'exp': [dict(intro=['In an ethical replication in {city}, {n} participants were instructed by an experimenter in a lab coat and {n} by an experimenter in casual clothes to continue an unpleasant but harmless task. The number of task steps (out of 15) completed before refusing was recorded.',
                        '{person} tested whether a uniform affects obedience: participants were randomly allocated to an experimenter in a lab coat or in casual clothes and the number of steps (out of 15) they completed was recorded.'],
                 A='lab coat', B='casual clothes', gA='participants instructed by an experimenter in a lab coat', gB='participants instructed by an experimenter in casual clothes',
                 more='will complete more steps of the task than', measure='the number of steps completed', dvshort='Steps completed (out of 15)',
                 iv='whether the experimenter wore a lab coat or casual clothes', dv='the number of steps of the task (out of 15) completed before the participant refused',
                 range=(0, 15), base=(6, 8), diff=(2, 4), sd=2.4,
                 controls=['the same experimenter, script and prods in both conditions', 'the same room and the same task for every participant'],
                 ethics=['participants must be able to withdraw at any point without pressure', 'a full debrief explaining the deception'],
                 concl_A='a symbol of authority (a lab coat) increases obedience.', concl_B='an experimenter in casual clothes obtains more obedience.')],
    'plan': [('whether people are more obedient to a teacher than to a fellow student', 'IV: status of the person giving the instruction', 'DV: whether the instruction is followed', ['field experiment']),
             ('people’s attitudes to obeying authority figures at work', 'topic: attitudes to obedience', 'measure: rating scales and open answers', ['questionnaire', 'interview'])],
}

c11a = T('Background: obedience to authority and the Holocaust', 'obedience authority holocaust')
build(c11a, {
    'terms': [
        ('obedience', 'following a direct order from a person in authority'),
        ('authority figure', 'a person who is perceived to have the right to give orders, such as a police officer or scientist'),
        ('agentic state', 'a state in which a person sees themselves as acting for an authority and so does not feel responsible for their actions'),
        ('dispositional explanation', 'an explanation of behaviour in terms of a person’s personality or characteristics'),
        ('situational explanation', 'an explanation of behaviour in terms of features of the environment or social situation'),
        ('conformity', 'changing behaviour or beliefs to fit in with a group, without a direct order'),
    ],
    'mcq': [
        ('Milgram’s research was motivated by the question of', 'how ordinary people could take part in atrocities such as the Holocaust', ['why people dream', 'how children learn language', 'whether animals have emotions'], 'Milgram tested the “Germans are different” hypothesis.'),
        ('Obeying an order differs from conforming because obedience involves', 'a direct instruction from an authority figure', ['copying a group of equals', 'no social influence', 'only private beliefs'], 'Obedience = direct order from authority.'),
        ('Which approach does Milgram’s study belong to?', 'The social approach', ['The biological approach', 'The cognitive approach', 'The learning approach'], 'It studies social influence.'),
        ('Before the study, how many people did a sample of Yale psychology students predict would give the maximum shock?', 'Very few (about 1–3%)', ['About 65%', 'About half', 'All of them'], 'The predictions were 0–3%, average about 1.2%.'),
    ],
    'ar': [
        ('The “Germans are different” hypothesis suggested that the Holocaust occurred because of a German personality type.', 'It is a dispositional explanation of obedience.', 'AR', 'It explains behaviour in terms of personality.'),
    ],
    'explain': [
        ('Explain the difference between situational and dispositional explanations of obedience.', 'Situational explanations say obedience is caused by features of the situation, such as the presence and status of an authority figure; dispositional explanations say it is caused by personality, such as an authoritarian personality.', '1 mark each, contrasted [2]'),
        ('Explain why Milgram’s study is relevant to understanding the Holocaust.', 'It showed that ordinary people would harm an innocent person when ordered by an authority, suggesting that the Holocaust may be partly explained by situational pressures to obey rather than by a unique national character.', '1 mark ordinary people obey; 1 mark situational explanation [2]'),
    ],
    'claims': [
        ('Milgram’s study tested conformity to a group of peers.', False, 'It tested obedience to a single authority figure (the experimenter).'),
        ('People in an agentic state see themselves as acting on behalf of someone else.', True, 'They transfer responsibility to the authority figure.'),
    ],
    'apply': [
        ('{person}, a junior nurse in {city}, is told by a senior doctor over the phone to give a patient a dose of medicine that is higher than the maximum on the label. {person} gives the dose.',
         [('Identify whether {person}’s behaviour is obedience or conformity, with a reason.', 'Obedience, because {person} followed a direct order from an authority figure (the doctor).', '1 mark obedience; 1 mark reason [2]'),
          ('Use a situational explanation to explain {person}’s behaviour.', 'The doctor has high status and legitimate authority in a hospital, and {person} may have entered an agentic state, seeing the doctor as responsible.', '1 mark authority/setting; 1 mark agentic state [2]'),
          ('Suggest one way the hospital could reduce this kind of obedience.', 'Train staff to question unsafe instructions, require written prescriptions, and make clear that nurses are responsible for their own actions.', '1 mark suggestion; 1 mark how it reduces obedience [2]')]),
    ],
})

c11b = T('Procedure and results: electric shock experiment with a learner and experimenter', 'procedure results electric shock experiment learner experimenter')
build(c11b, {
    'mcq': [
        ('How many participants took part in Milgram’s (1963) baseline study?', '40 men', ['72 children', '20 women', '103 students'], '40 men aged 20–50 from New Haven.'),
        ('How were Milgram’s participants recruited?', 'Through a newspaper advertisement and direct mail, paid $4.50', ['From prisons', 'From the US army', 'From psychology classes only'], 'A volunteer sample, paid $4.50.'),
        ('What was the maximum voltage on the shock generator?', '450 volts', ['100 volts', '300 volts', '1000 volts'], '30 switches from 15V to 450V.'),
        ('What percentage of participants went all the way to 450 volts?', '65%', ['1%', '12.5%', '100%'], '26 of 40 participants.'),
        ('Up to what voltage did all 40 participants continue?', '300 volts', ['15 volts', '150 volts', '450 volts'], 'No participant stopped before 300V.'),
        ('What was the first of the experimenter’s four prods?', '“Please continue” or “Please go on”', ['“You have no other choice, you must go on”', '“It is absolutely essential that you continue”', '“The experiment requires that you continue”'], 'Prods were used in sequence.'),
        ('Who played the learner, “Mr Wallace”?', 'A 47-year-old accountant who was a confederate', ['A real participant', 'A Yale student', 'Milgram himself'], 'The learner was trained to act the part.'),
    ],
    'ar': [
        ('All participants believed they had been chosen randomly to be the teacher.', 'The draw was rigged so that the participant was always the teacher.', 'AR', 'The rigged draw created the belief of random allocation.'),
        ('Milgram’s participants showed no signs of distress.', 'Milgram recorded nervous laughter, sweating and trembling.', 'R', 'A is false; R is true.'),
    ],
    'explain': [
        ('Describe the procedure of Milgram’s study.', 'A participant and a confederate drew lots (rigged) so the participant became the teacher. The learner was strapped into a chair in another room. The teacher gave word-pair memory tests and was told to give increasingly strong shocks (15V to 450V in 15V steps) for each wrong answer. At 300V the learner pounded on the wall and then stopped responding. If the teacher hesitated, the experimenter used four standard prods.', '1 mark rigged roles; 1 mark shock generator; 1 mark learner responses; 1 mark prods [4]'),
        ('Describe the quantitative results of Milgram’s study.', 'All 40 participants went to at least 300V; 5 (12.5%) stopped at 300V; 26 (65%) continued to the maximum 450V.', '1 mark 300V; 1 mark 65% / 26 of 40 [2]'),
        ('Describe the qualitative results of Milgram’s study.', 'Many participants showed extreme tension: sweating, trembling, stuttering, biting lips and groaning; 14 showed nervous laughter and three had uncontrollable seizures.', '1 mark signs; 1 mark examples/numbers [2]'),
        ('Explain why the learner was in a different room from the teacher.', 'So that the teacher could hear but not see him; this made the deception about shocks more convincing and standardised the learner’s responses (pounding the wall, then silence).', '1 mark maintain deception; 1 mark standardised responses [2]'),
    ],
    'claims': [
        ('In Milgram’s study the learner actually received electric shocks.', False, 'The learner was a confederate and received no shocks; only the teacher received a sample shock of 45V.'),
        ('Each participant was given a sample shock of 45 volts.', True, 'This convinced participants that the generator was real.'),
    ],
})
add_tally_pct(c11b, ['The table shows how many participants in different variations of an obedience study continued to the maximum level of the task in {city}.', '{person} recorded how many participants obeyed fully or stopped early in several versions of an obedience procedure.'],
              [('Baseline (experimenter present)', (22, 28), (12, 18)), ('Experimenter gives orders by phone', (6, 12), (28, 34)), ('Run-down office building', (16, 22), (18, 24)), ('Teacher and learner in same room', (14, 18), (22, 26)), ('Ordinary man gives orders', (6, 10), (30, 34))],
              ('obeyed fully', 'stopped early', 'participants'))

c11c = T('Evaluation: ethics, validity and situational versus individual explanations', 'evaluation ethics validity situational versus individual explanations')
build(c11c, {
    'mcq': [
        ('Which ethical guideline was most clearly broken by the experimenter’s prods?', 'The right to withdraw', ['Confidentiality', 'Debriefing', 'Use of animals'], 'Prods discouraged participants from leaving.'),
        ('Which evidence suggests Milgram’s participants believed the shocks were real?', 'They showed extreme tension such as sweating and trembling', ['They were paid in advance', 'They were all men', 'The study took place at Yale'], 'Signs of stress support internal validity.'),
        ('Which finding supports an individual explanation of obedience?', '35% of participants refused to continue to 450V', ['65% went to 450V', 'All went to 300V', 'Students predicted low obedience'], 'Not everyone obeyed in the same situation.'),
    ],
    'explain': [
        ('Explain one way in which Milgram tried to protect his participants.', 'All participants were debriefed, met the unharmed learner, were assured their behaviour was normal and were later sent a follow-up questionnaire; most said they were glad they took part.', '1 mark debrief/dehoax; 1 mark follow-up [2]'),
        ('Explain why Milgram’s study may lack ecological validity.', 'Giving electric shocks to a stranger in a laboratory is not an everyday act, and Yale’s prestige may have increased obedience, so obedience levels may not apply to real-life situations.', '1 mark unusual task/setting; 1 mark consequence [2]'),
        ('Explain how Milgram’s study supports a situational explanation of obedience.', 'Ordinary men, not selected for any personality type, obeyed to 450V because of the authority of the experimenter, the prestigious setting and the gradual increase in shocks.', '1 mark ordinary people; 1 mark situational features [2]'),
    ],
    'claims': [
        ('Milgram’s study proves that all people will obey destructive orders.', False, '35% defied the experimenter, and obedience varied across situations in later variations.'),
        ('Participants in Milgram’s study were deceived about the purpose of the study.', True, 'They were told it was a study of punishment and learning.'),
    ],
})
chapter(11, [c11a, c11b, c11c], MI_STUDY)


# ============================================================== CHAPTER 12: Perry et al. (2015)

PE = 'Perry et al.’s (2015) study of personal space and oxytocin'
PE_STUDY = {
    'who': PE,
    'evals': [
        ('controls', 'strength', 'The study was double-blind and placebo-controlled, so neither participants nor researchers knew who had oxytocin, reducing demand characteristics and researcher bias.'),
        ('repeated measures design', 'strength', 'Each participant was tested with both oxytocin and placebo in counterbalanced sessions, so individual differences in personal space did not affect the comparison.'),
        ('standardisation', 'strength', 'The Comfortable Interpersonal Distance (CID) task was computer-based, so every participant saw the same figures approaching in the same way.'),
        ('ecological validity', 'weakness', 'Pressing a key when a figure on a screen gets too close is unlike real face-to-face interaction, so personal-space preferences may differ in real life.'),
        ('generalisability', 'weakness', 'Participants were male students, so the results may not apply to women, for whom oxytocin effects may differ, or to other age groups.'),
        ('usefulness', 'strength', 'The findings suggest that oxytocin effects depend on individual empathy, which matters for possible treatments using oxytocin for social difficulties.'),
        ('validity of the empathy measure', 'weakness', 'Empathy was measured by self-report questionnaire, which may be affected by social desirability.'),
    ],
    'essays': [
        ('the effects of hormones on social behaviour depend on individual differences',
         ['Perry et al. found oxytocin affected personal space differently in low- and high-empathy participants.', 'Individual traits moderate biological effects.'],
         ['Situations (who is approaching) also changed preferred distance.', 'The task was artificial and used only male participants.'],
         ['individual and situational explanations', 'biological influences on social behaviour']),
    ],
    'exp': [dict(intro=['In a double-blind replication in {city}, the same {n} participants completed a personal-space task after a placebo nasal spray and, in another session, after an oxytocin spray. Preferred distance (cm) from an approaching figure was recorded.',
                        '{person} measured preferred interpersonal distance (cm) for {n} participants tested once with oxytocin and once with a placebo spray, in counterbalanced order.'],
                 A='oxytocin', B='placebo', gA='participants given oxytocin', gB='the same participants given a placebo',
                 more='will prefer a larger interpersonal distance than', measure='preferred interpersonal distance', dvshort='Preferred distance (cm)', design='repeated measures',
                 iv='whether participants received oxytocin or a placebo nasal spray', dv='preferred distance in cm at which they stopped an approaching figure',
                 range=(40, 160), base=(70, 85), diff=(8, 18), sd=10,
                 controls=['counterbalancing the order of oxytocin and placebo sessions', 'a double-blind procedure so expectations do not affect results', 'the same computer task and figures for all participants'],
                 ethics=['informed consent about receiving a hormone spray and possible side effects', 'participants should be screened for health conditions'],
                 concl_A='oxytocin increases the personal space people prefer (for these participants).', concl_B='oxytocin reduces the personal space people prefer.')],
    'plan': [('whether people stand further away from strangers than from friends', 'IV: stranger or friend', 'DV: distance in cm', ['field experiment', 'observation']),
             ('whether empathy scores are related to preferred personal space', 'co-variable 1: empathy questionnaire score', 'co-variable 2: preferred distance in cm', ['correlation'])],
}

c12a = T('Background: personal space, empathy and oxytocin', 'personal space empathy oxytocin')
build(c12a, {
    'terms': [
        ('personal space', 'the area around a person that they regard as their own and feel uncomfortable when others enter it'),
        ('oxytocin', 'a hormone and neurotransmitter involved in social bonding, trust and sensitivity to social cues'),
        ('empathy', 'the ability to understand and share the feelings of another person'),
        ('interpersonal distance', 'the physical distance people keep between themselves and others'),
        ('placebo', 'an inactive substance given to a control group so that they believe they may have received the real treatment'),
    ],
    'foils': ['vasopressin', 'serotonin reuptake'],
    'mcq': [
        ('Which hormone was investigated by Perry et al. (2015)?', 'Oxytocin', ['Testosterone', 'Adrenaline', 'Melatonin'], 'Oxytocin was given as a nasal spray.'),
        ('Oxytocin is thought to increase', 'sensitivity to social cues', ['the need for sleep', 'reaction time to lights', 'the size of the hippocampus'], 'The social salience hypothesis.'),
        ('Personal space is best described as', 'the invisible area around a person that others should not enter without discomfort', ['a person’s bedroom', 'the number of friends a person has', 'the space between buildings'], 'A comfort zone around the body.'),
    ],
    'explain': [
        ('Explain why Perry et al. expected the effect of oxytocin to depend on empathy.', 'The social salience idea suggests oxytocin makes social cues more noticeable; people with different empathy levels interpret those cues differently, so oxytocin might lead some to approach and others to keep more distance.', '1 mark social salience; 1 mark differing interpretation by empathy [2]'),
        ('Explain why Perry et al.’s study belongs to the social approach.', 'It investigates how people regulate personal space during social interactions, although it uses a biological (hormonal) manipulation.', '1 mark social behaviour; 1 mark context [2]'),
    ],
    'claims': [
        ('Oxytocin always makes people want to be closer to others.', False, 'Its effects depend on individual differences and context; Perry et al. found low-empathy participants preferred more distance after oxytocin.'),
        ('Personal space preferences vary between cultures and situations.', True, 'People allow friends closer than strangers, and norms differ across cultures.'),
    ],
    'apply': [
        ('{person}, a student in {city}, feels uncomfortable when a stranger on a bus sits very close, but happily sits close to friends.',
         [('Use the concept of personal space to explain {person}’s feelings.', 'The stranger entered {person}’s personal space, the area kept for close relationships, which causes discomfort; friends are allowed closer.', '1 mark definition; 1 mark stranger versus friend [2]'),
          ('Suggest how oxytocin might influence {person}’s reaction, according to Perry et al.', 'It could make the social cues from the stranger more salient; depending on {person}’s empathy level, {person} might want more distance (low empathy) or show little change (high empathy).', '1 mark salience; 1 mark depends on empathy [2]')]),
    ],
})

c12b = T('Procedure and results: oxytocin and placebo in high- and low-empathy participants', 'procedure results oxytocin placebo high- low-empathy participants')
build(c12b, {
    'mcq': [
        ('How was oxytocin given in Perry et al.’s study?', 'As a nasal spray', ['As an injection', 'In a drink', 'As a tablet'], 'Intranasal administration of 24 IU.'),
        ('What type of procedure prevented participants and researchers knowing who had oxytocin?', 'A double-blind procedure', ['A single-blind procedure', 'Covert observation', 'Random sampling'], 'Neither knew which spray was given.'),
        ('Which task measured personal space in Perry et al.’s study?', 'The Comfortable Interpersonal Distance (CID) paradigm', ['The Revised Eyes Test', 'The Bobo doll test', 'A memory span task'], 'Participants stopped an approaching figure on screen.'),
        ('How was empathy measured in Perry et al.’s study?', 'By a self-report empathy questionnaire', ['By an EEG', 'By observation in a park', 'By a blood test'], 'Participants were split into low- and high-empathy groups.'),
        ('In Perry et al.’s study, oxytocin increased the preferred distance mainly for', 'low-empathy participants', ['high-empathy participants', 'all participants equally', 'no participants'], 'The effect depended on empathy level.'),
    ],
    'explain': [
        ('Describe the procedure of Perry et al.’s study.', 'Male participants completed an empathy questionnaire and attended two sessions, receiving oxytocin or a placebo nasal spray (double-blind, counterbalanced). In the CID task they imagined standing in a room as a figure approached and pressed a key to stop it when they felt uncomfortable; preferred distance was recorded.', '1 mark empathy measure; 1 mark oxytocin/placebo double-blind; 1 mark CID task [3]'),
        ('Describe the main results of Perry et al.’s study.', 'Oxytocin changed preferred distance depending on empathy: low-empathy participants kept a larger distance after oxytocin than after placebo, especially from strangers, whereas high-empathy participants showed little or no increase.', '1 mark low-empathy increase; 1 mark high-empathy different [2]'),
    ],
    'claims': [
        ('Perry et al. used an independent measures design for oxytocin and placebo.', False, 'Each participant was tested in both conditions (repeated measures) in counterbalanced order.'),
        ('Perry et al. found that the effect of oxytocin depended on the participant’s empathy level.', True, 'This is the key finding.'),
    ],
})

c12c = T('Evaluation: validity, controls and usefulness', 'evaluation validity controls usefulness')
build(c12c, {
    'mcq': [
        ('Why did Perry et al. use a placebo spray?', 'To control for the effect of expecting a treatment', ['To make participants feel ill', 'To measure empathy', 'To increase personal space'], 'Expectation effects are equal in both conditions.'),
        ('Which is a weakness of Perry et al.’s study?', 'The computer task was unlike real social encounters', ['It was double-blind', 'It used counterbalancing', 'It used a placebo'], 'Low ecological validity.'),
    ],
    'explain': [
        ('Explain why a double-blind procedure increases the validity of Perry et al.’s study.', 'Participants could not respond to expectations about oxytocin, and researchers could not unconsciously influence results, so differences are more likely to be caused by the hormone.', '1 mark participants; 1 mark researchers [2]'),
        ('Explain one way Perry et al.’s findings could be useful.', 'Oxytocin has been suggested as a treatment for social difficulties; the findings warn that its effects may depend on individual empathy, so it may not help everyone.', '1 mark application; 1 mark caution [2]'),
    ],
    'claims': [
        ('Perry et al.’s findings can be generalised to all women.', False, 'Participants were men, and oxytocin may act differently in women.'),
        ('Counterbalancing the oxytocin and placebo sessions controlled for order effects.', True, 'Half had oxytocin first and half placebo first.'),
    ],
    'apply': [
        ('A pharmaceutical company in {city} wants to market oxytocin spray to help shy people feel comfortable in crowds.',
         [('Use Perry et al.’s findings to explain why the spray may not work for everyone.', 'Oxytocin’s effect on personal space depended on empathy; for low-empathy people it increased preferred distance, so it might make some users less comfortable.', '1 mark depends on empathy; 1 mark consequence [2]'),
          ('Explain one limitation of using Perry et al.’s study as evidence for the product.', 'The study used male students and an artificial computer task, so the results may not apply to real crowds or to women.', '1 mark limitation; 1 mark explained [2]')]),
    ],
})
chapter(12, [c12a, c12b, c12c], PE_STUDY)


# ============================================================== CHAPTER 13: Piliavin et al. (1969)

PI = 'Piliavin et al.’s (1969) subway Samaritan study'
PI_STUDY = {
    'who': PI,
    'evals': [
        ('ecological validity', 'strength', 'The study took place on a real New York subway train with ordinary passengers who did not know they were being studied, so their helping behaviour was natural.'),
        ('sample size', 'strength', 'About 4450 passengers were observed over 103 trials, a large and varied sample that increases generalisability to subway users.'),
        ('standardisation', 'strength', 'The victim always collapsed about 70 seconds after the train left the station, in the same area of the carriage, and behaved in the same way, so the trials were comparable.'),
        ('ethics', 'weakness', 'Passengers did not consent, were deceived into thinking someone had collapsed, could have been distressed and were not debriefed.'),
        ('controls', 'weakness', 'As a field experiment, the researchers could not control the number or type of passengers in each carriage, so extraneous variables may have affected helping.'),
        ('reliability', 'weakness', 'The two observers recorded many details at once in a crowded carriage, so some behaviour may have been missed and inter-rater reliability could not be fully checked.'),
        ('cost-reward model', 'strength', 'The results (more help for the cane victim) support the cost-reward model, which gives a useful explanation of when people help.'),
    ],
    'essays': [
        ('helping behaviour is best explained by the cost–reward model',
         ['The cane victim was helped in 95% of trials and the drunk victim in 50%, consistent with higher costs of helping a drunk person.', 'Arousal created by seeing a victim is reduced by helping or leaving.'],
         ['People also help because of empathy or personal norms.', 'The study did not measure passengers’ arousal or thought processes directly.', 'Situational and individual factors such as race and gender also played a part.'],
         ['diffusion of responsibility', 'situational and individual explanations', 'ecological validity']),
        ('field experiments are more useful than laboratory experiments in social psychology',
         ['Piliavin et al. observed real helping on a subway with high ecological validity.', 'Participants did not know they were being studied, avoiding demand characteristics.'],
         ['Less control over extraneous variables, such as the number of passengers.', 'Ethical problems: no consent or debriefing.', 'Laboratory studies such as Milgram allow precise control.'],
         ['ecological validity', 'ethics', 'controls']),
    ],
    'exp': [dict(intro=['In an ethical field experiment in {city}, a researcher dropped a pile of books in a shopping centre while either wearing a plaster cast or not. Over {n} trials per condition, the number of passers-by (out of 10) who helped was recorded.',
                        '{person} recorded how many of the next 10 passers-by helped a researcher who dropped papers, in {n} trials with an arm in a sling and {n} trials without.'],
                 A='sling (injured)', B='no sling', gA='a researcher wearing a sling', gB='a researcher without a sling',
                 more='will receive help from more passers-by than', measure='the number of passers-by who help', dvshort='Passers-by who helped (out of 10)', nosample=True,
                 iv='whether the researcher wore an arm sling or not', dv='the number of the next 10 passers-by who helped pick up the dropped items',
                 range=(0, 10), base=(3, 4.5), diff=(1.5, 3), sd=1.4,
                 controls=['the same researcher, clothing (apart from the sling) and items dropped in every trial', 'trials at the same time of day in the same location'],
                 ethics=['passers-by cannot consent, so the study must be harmless and not waste much of their time', 'helpers could be thanked and briefly debriefed'],
                 concl_A='people are more likely to help someone who appears injured.', concl_B='people are less likely to help someone who appears injured.')],
    'obs': [dict(intro=['Two observers on a train in {city} independently recorded passengers’ responses after a confederate appeared to faint, using the same categories.',
                        '{person} and another observer tallied passengers’ reactions to a staged emergency on public transport.'],
                 cats=['helped the victim', 'looked at the victim but did not help', 'moved away from the critical area', 'made a comment to another passenger', 'called for a staff member', 'ignored the event'], tally=(2, 15),
                 kind='a covert', kind_plus='Passengers did not know they were being observed, so they behaved naturally and there were no demand characteristics.',
                 kind_minus='Observers had to watch many people in a crowded carriage, so behaviours may have been missed, and passengers could not consent or be debriefed.',
                 ethics=['passengers may be distressed by the staged emergency and cannot consent', 'passengers should not be identifiable in any records'])],
    'plan': [('whether people are more likely to help a person who asks politely than one who demands help', 'IV: polite request or demand', 'DV: whether help is given', ['field experiment']),
             ('how people respond to someone in difficulty on public transport', 'behaviour: helping responses', 'categories: helping, looking, ignoring, moving away', ['observation'])],
}

c13a = T('Background: bystander behaviour and diffusion of responsibility', 'bystander behaviour diffusion responsibility')
build(c13a, {
    'terms': [
        ('bystander effect', 'the tendency for people to be less likely to help a victim when other people are present'),
        ('diffusion of responsibility', 'when responsibility for helping is shared among bystanders, so each feels less personally responsible'),
        ('prosocial behaviour', 'behaviour intended to benefit another person, such as helping'),
        ('cost–reward model', 'the idea that people decide whether to help by weighing up the costs and rewards of helping and of not helping'),
        ('arousal', 'an unpleasant emotional state caused by seeing someone in need, which motivates the bystander to reduce it'),
    ],
    'foils': ['social loafing', 'pluralistic ignorance'],
    'mcq': [
        ('The murder of Kitty Genovese in New York (1964) led to research on', 'bystander apathy', ['obedience', 'theory of mind', 'sleep and dreams'], 'Reports suggested many neighbours failed to help.'),
        ('According to diffusion of responsibility, a person is less likely to help when', 'there are many other bystanders', ['they are alone', 'the victim is a friend', 'the costs of helping are low'], 'Responsibility is shared.'),
        ('In the cost–reward model, which is a cost of helping?', 'Possible physical danger or embarrassment', ['Praise from others', 'Feeling good about oneself', 'Reduced arousal'], 'Costs of helping include effort, danger and embarrassment.'),
    ],
    'explain': [
        ('Explain what is meant by diffusion of responsibility.', 'When several bystanders are present, the responsibility to help is spread among them, so each person feels less obligated to act and assumes someone else will help.', '1 mark spread among bystanders; 1 mark each less likely to act [2]'),
        ('Explain the cost–reward model of helping.', 'Seeing a victim creates unpleasant arousal; the bystander reduces it by choosing the response with the lowest net cost, weighing the costs of helping (effort, danger, disgust) against the costs of not helping (guilt, blame).', '1 mark arousal; 1 mark weighing costs [2]'),
    ],
    'claims': [
        ('Diffusion of responsibility predicts that a victim is more likely to be helped in a crowded place.', False, 'It predicts less help, because each bystander feels less responsible.'),
        ('The cost–reward model includes the costs of not helping, such as guilt.', True, 'Both sides are weighed.'),
    ],
    'apply': [
        ('In a busy market in {city}, an elderly man falls and drops his shopping. Many people walk past before {person} stops to help.',
         [('Use diffusion of responsibility to explain why many people walked past.', 'With many bystanders, each person assumed someone else would help, so they felt less personal responsibility.', '1 mark shared responsibility; 1 mark applied [2]'),
          ('Use the cost–reward model to explain why {person} helped.', 'For {person} the costs of helping (a few minutes) were low and the costs of not helping (guilt, seeing him hurt) were high, so helping reduced arousal at the least cost.', '1 mark costs of helping; 1 mark costs of not helping [2]')]),
    ],
})

c13b = T('Procedure and results: field experiment with drunk and cane victims on the New York subway', 'procedure results field experiment drunk cane victims new york subway')
build(c13b, {
    'mcq': [
        ('How long was the non-stop journey used in Piliavin et al.’s study?', 'About 7.5 minutes', ['About 30 seconds', 'About 1 hour', 'About 20 minutes'], 'Between 59th Street and 125th Street.'),
        ('About how many passengers were present across all the trials?', 'About 4450', ['About 40', 'About 450', 'About 45,000'], '103 trials with about 4450 passengers.'),
        ('In what percentage of trials was the cane victim helped spontaneously?', 'About 95%', ['About 50%', 'About 7%', 'About 65%'], '62 of 65 trials.'),
        ('In what percentage of trials was the drunk victim helped spontaneously?', 'About 50%', ['About 95%', 'About 7%', 'About 81%'], '19 of 38 trials.'),
        ('How long after the train left the station did the victim collapse?', 'About 70 seconds', ['Immediately', 'About 5 minutes', 'Just before the next station'], 'A standardised time.'),
        ('Most first helpers in Piliavin et al.’s study were', 'male', ['female', 'children', 'staff members'], 'About 90% of first helpers were male.'),
        ('How did the drunk victim differ from the cane victim?', 'He smelled of alcohol and carried a bottle in a brown paper bag', ['He wore a smart suit', 'He was much older', 'He asked passengers for help'], 'Otherwise the victims were dressed the same.'),
    ],
    'ar': [
        ('Piliavin et al. found little evidence of diffusion of responsibility.', 'Larger groups of passengers did not lead to slower helping.', 'AR', 'Help was not reduced in larger groups, contrary to diffusion of responsibility.'),
        ('The model in Piliavin et al.’s study always helped immediately.', 'The model was used to see whether an example of helping increased help from others.', 'R', 'A is false: the model helped early (about 70 s) or late (about 150 s), and only if no one else had; R is true.'),
    ],
    'explain': [
        ('Describe the procedure of Piliavin et al.’s study.', 'Teams of four students (a victim, a model and two female observers) boarded New York subway trains. About 70 seconds after the train left a station, the male victim collapsed, either carrying a cane (ill) or smelling of alcohol (drunk). Observers recorded how many passengers helped, how quickly, and their sex, race and location. In some trials a model helped after about 70 or 150 seconds if no one else had.', '1 mark setting/team; 1 mark collapse and conditions; 1 mark observations recorded; 1 mark model [4]'),
        ('Describe the results of Piliavin et al.’s study.', 'The cane victim received spontaneous help in 62 of 65 trials (95%) and the drunk victim in 19 of 38 (50%); help for the cane victim usually came within seconds; 90% of first helpers were male; there was a slight same-race effect for the drunk victim; there was no diffusion of responsibility.', '1 mark cane/drunk percentages; 1 mark speed; 1 mark sex or race; 1 mark no diffusion [4]'),
        ('Explain why the victim collapsed in the “critical area” of the carriage.', 'So that all trials were standardised and passengers in the critical area (closest to the victim) could be compared with those in the adjacent area.', '1 mark standardisation; 1 mark comparison of areas [2]'),
    ],
    'claims': [
        ('Piliavin et al. carried out their study in a laboratory set up to look like a train.', False, 'It was a field experiment on real New York subway trains.'),
        ('The two observers in Piliavin et al.’s study were female.', True, 'Two female observers sat in the adjacent area and recorded responses.'),
    ],
})
add_tally_pct(c13b, ['The table shows trials with and without spontaneous help in a replication of Piliavin et al. in {city}.', '{person} recorded whether a collapsed victim received spontaneous help in each trial.'],
              [('Cane victim', (24, 34), (1, 4)), ('Drunk victim', (8, 16), (8, 16)), ('Cane victim, crowded train', (20, 30), (1, 5)), ('Drunk victim, quiet train', (6, 12), (8, 14))],
              ('helped', 'not helped', 'trials'))

c13c = T('Evaluation: ethics, ecological validity and cost-reward model', 'evaluation ethics ecological validity cost-reward model')
build(c13c, {
    'mcq': [
        ('Which is a strength of Piliavin et al.’s study?', 'High ecological validity because it used a real subway', ['It obtained informed consent', 'It controlled all extraneous variables', 'It had a small sample'], 'Natural setting and unaware passengers.'),
        ('Which is an ethical weakness of Piliavin et al.’s study?', 'Passengers were not able to consent and were not debriefed', ['The victims were real patients', 'The observers were paid', 'The study used animals'], 'Field experiments often lack consent and debriefing.'),
        ('According to the cost–reward model, why was the drunk victim helped less?', 'Helping a drunk person has higher costs, such as possible danger or disgust', ['Passengers could not see him', 'There was no one in the carriage', 'He did not need help'], 'Higher costs of helping.'),
    ],
    'explain': [
        ('Explain how Piliavin et al.’s results support the cost–reward model.', 'The drunk victim was helped less than the cane victim because the costs of helping him (danger, embarrassment, disgust) were higher and the costs of not helping were lower (he might be seen as responsible).', '1 mark result; 1 mark cost explanation [2]'),
        ('Explain one way Piliavin et al.’s study lacked control.', 'The number, sex and race of passengers varied between trials and could not be controlled, so these variables may have affected helping as well as the victim condition.', '1 mark uncontrolled variable; 1 mark effect [2]'),
    ],
    'claims': [
        ('Piliavin et al.’s study has high ecological validity but raises ethical issues.', True, 'Natural setting, but no consent, deception and possible distress without debrief.'),
        ('Piliavin et al.’s findings can be generalised to all countries and all time periods.', False, 'The study took place in New York in the late 1960s; norms about helping vary across cultures and over time.'),
    ],
    'apply': [
        ('A transport company in {city} wants to increase the number of passengers who help people who become ill on trains.',
         [('Use the cost–reward model to suggest one way of increasing helping.', 'Reduce the costs of helping, for example by training passengers in first aid or providing clear emergency buttons, so helping is easier and less risky.', '1 mark reduce costs; 1 mark example [2]'),
          ('Explain why people may be less likely to help someone who appears drunk.', 'The costs are higher (danger, mess, embarrassment) and the person may be blamed for their state, so the costs of not helping are lower.', '1 mark costs; 1 mark responsibility [2]'),
          ('Suggest one ethical way to test whether the change works.', 'Count real incidents of passengers helping before and after the change from staff reports, rather than staging emergencies.', '1 mark method; 1 mark ethical reason [2]')]),
    ],
})
chapter(13, [c13a, c13b, c13c], PI_STUDY)
